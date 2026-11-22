"""Run a four-level comparison on frozen declarations and observed effects."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import socket
import subprocess

from run import (Invalid, JUDGMENT, Unavailable, digest, generate, message,
                 read, save, stamp, start_server)
from score import metrics, require, summary as verify_source, unpack


LEVELS = ("I0", "I2", "I3", "I4")
HERE = Path(__file__).resolve().parent


def source_digest(root):
    fingerprints = {p.relative_to(root).as_posix(): digest(p) for p in sorted(root.rglob("*"))
                    if p.is_file() and "__pycache__" not in p.parts}
    return hashlib.sha256(json.dumps(fingerprints, sort_keys=True).encode()).hexdigest()


def start(name, binary, weights, lock, output):
    if binary is None or weights is None:
        return None, None, "No pinned binary and weights supplied."
    if digest(binary) != lock["server_binary_sha256"] or digest(weights) != lock["weights_sha256"]:
        return None, None, "Runtime hashes differ from the lock."
    with socket.socket() as temp:
        temp.bind(("127.0.0.1", 0))
        port = temp.getsockname()[1]
    command = [str(binary.resolve()), "--model", str(weights.resolve()), "--alias", name,
               "--host", "127.0.0.1", "--port", str(port), *lock["server_args"]]
    url = f"http://127.0.0.1:{port}"
    output.mkdir()
    save(output / "start.json", {"at": stamp(), "command": command,
                                "binary_sha256": lock["server_binary_sha256"],
                                "weights_sha256": lock["weights_sha256"]})
    process, blocker = start_server(output, url, command)
    return process, url, blocker


def end(process, root):
    if process is None:
        return
    active = process.poll() is None
    if active:
        process.terminate()
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    save(root / "exit.json", {"exit_code": process.returncode, "terminated_by_harness": active})


def evaluate(model, messages, name, root, sampling):
    url, blocker = model
    if blocker:
        return {"status": "NOT_RUN", "reason": blocker}
    try:
        verdict, _ = generate(url, name, messages, JUDGMENT, root, name, sampling)
        return {"status": "MEASURED", **verdict}
    except (Invalid, Unavailable) as exc:
        return {"status": "NOT_RUN" if isinstance(exc, Unavailable) else "BLOCKED", "reason": str(exc)}


def run_cases(source, output, protocol, same_model, other_model, reuse):
    for case in protocol["cases"]:
        original = source / case["id"]
        row = read(original / "result.json")
        root = output / case["id"]
        root.mkdir()
        if row["status"] in ("PASS", "FAIL"):
            packet = message("user", protocol["rubric"] + "\n" + json.dumps(read(original / "evidence.json")))
            if not reuse:
                acting = read(original / "report.request.json")["body"]["messages"]
                reply = read(original / "report.response.json")["choices"][0]["message"]["content"]
                continued = [*acting, message("assistant", reply), packet]
                row["evaluators"]["I0"] = evaluate(same_model, continued, "I0", root, protocol["sampling"])
                row["evaluators"]["I2"] = evaluate(same_model, [packet], "I2", root, protocol["sampling"])
            row["evaluators"]["I3"] = evaluate(other_model, [packet], "I3", root, protocol["sampling"])
            row["provenance"] = {"I0": "source transcript" if reuse else "replayed continued context",
                                 "I2": "source fresh request" if reuse else "new fresh request",
                                 "I3": "SmolLM2 fresh request", "I4": "source deterministic readback, reverified"}
        save(root / "result.json", row)
        print(case["id"], {k: v["status"] for k, v in row["evaluators"].items()}, flush=True)


def rescore(source, output):
    verify_source(source)
    baseline = read(output / "freeze.json")
    require(baseline["source_digest"] == source_digest(source), "Frozen source run was modified")
    for name, expected in baseline["snapshot"].items():
        require(digest(output / "frozen" / name) == expected, f"Replay source modified: {name}")
    protocol = read(source / "frozen/protocol.json")
    rows = []
    for case in protocol["cases"]:
        case_id = case["id"]
        root = output / case_id
        original = source / case_id
        row = read(root / "result.json")
        prior = read(original / "result.json")
        require({k: v for k, v in row.items() if k not in ("evaluators", "provenance")} ==
                {k: v for k, v in prior.items() if k != "evaluators"}, f"Realized outcome changed: {case_id}")
        require(row["evaluators"]["I4"] == prior["evaluators"]["I4"], f"I4 changed: {case_id}")
        if row["status"] in ("PASS", "FAIL"):
            same = ("I0", "I2")
            if baseline["reuse_i0_i2"]:
                for key in same:
                    require(row["evaluators"][key] == prior["evaluators"][key], f"Original judgment changed: {case_id} {key}")
            for key in (("I3",) if baseline["reuse_i0_i2"] else (*same, "I3")):
                e = row["evaluators"][key]
                if e["status"] == "MEASURED":
                    require(e == {"status": "MEASURED", **unpack(root, key)}, f"Reply differs: {case_id} {key}")
                    messages = read(root / f"{key}.request.json")["body"]["messages"]
                    packet = message("user", protocol["rubric"] + "\n" + json.dumps(read(original / "evidence.json")))
                    require(messages[-1] == packet and (key == "I0" or messages == [packet]),
                            f"Unexpected evidence messages: {case_id} {key}")
        rows.append(row)
    realized = [r for r in rows if r["status"] in ("PASS", "FAIL")]
    scores = {key: {**metrics(realized, key), "statuses": dict(Counter(r["evaluators"][key]["status"]
                                                                     for r in rows))}
              for key in LEVELS}
    pairs = {}
    for level in LEVELS[1:]:
        common = [r for r in realized if all(r["evaluators"][k]["status"] == "MEASURED" for k in ("I0", level))]
        base, separate = metrics(common, "I0"), metrics(common, level)
        delta_e = separate["E"] - base["E"] if base["E"] is not None else None
        delta_f = separate["F"] - base["F"] if base["F"] is not None else None
        signal = None if delta_e is None or delta_f is None else (
            delta_e > 0 and delta_f <= protocol["maximum_acceptable_false_alarm_increase"])
        pairs[level] = {"matched_cases": [r["id"] for r in common], "delta_E": delta_e,
                        "delta_F": delta_f, "descriptive_signal": signal}
    return {"cases": len(rows), "realized": len(realized), "evaluators": scores, "matched_comparisons": pairs,
            "source_digest": baseline["source_digest"]}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("source", type=Path)
    cli.add_argument("--out", type=Path, required=True)
    cli.add_argument("--server", type=Path)
    cli.add_argument("--actor-weights", type=Path)
    cli.add_argument("--other-weights", type=Path)
    cli.add_argument("--reuse-i0-i2", action="store_true")
    cli.add_argument("--rescore", action="store_true")
    args = cli.parse_args()
    source, output = args.source.resolve(), args.out.resolve()
    if args.rescore:
        print(json.dumps(rescore(source, output), indent=2))
        return
    verify_source(source)
    protocol = read(source / "frozen/protocol.json")
    other_lock = read(HERE / "profiles/heterogeneous.runtime.json")
    output.mkdir(parents=True, exist_ok=False)
    frozen = output / "frozen"
    frozen.mkdir()
    sources = [HERE / name for name in ("judge.py", "run.py", "score.py", "effects.py", "judgments.py")]
    sources.append(HERE / "profiles/heterogeneous.runtime.json")
    for path in sources:
        shutil.copyfile(path, frozen / path.name)
    save(output / "freeze.json", {"frozen_at": stamp(), "source_digest": source_digest(source),
                                 "snapshot": {p.name: digest(p) for p in sorted(frozen.iterdir())},
                                 "reuse_i0_i2": args.reuse_i0_i2,
                                 "comparison": "Original per-case oracle and paired threshold. Fresh I3 receives the same rubric and evidence as I2."})
    dependencies = [("other", args.other_weights, other_lock)]
    if not args.reuse_i0_i2:
        dependencies.append(("same", args.actor_weights, read(source / "frozen/runtime.json")))
    started = {}
    try:
        for label, weights, lock in dependencies:
            try:
                started[label] = start(label, args.server, weights, lock, output / label)
            except OSError as exc:
                started[label] = (None, None, str(exc))
        same = started.get("same", (None, None, "Reusing original I0 and I2."))
        run_cases(source, output, protocol, same[1:], started["other"][1:], args.reuse_i0_i2)
    finally:
        for label, (process, _, _) in started.items():
            end(process, output / label)
    save(output / "scores.json", rescore(source, output))


if __name__ == "__main__":
    main()
