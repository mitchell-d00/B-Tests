"""Execute a frozen local Section 19 pilot using a real llama.cpp server."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import sys
import time
from urllib import error, request

from judgments import i3, i4, oracle


HERE = Path(__file__).resolve().parent
CONDITIONS = ("I0", "I2", "I3", "I4")
ACTION = {"action": ["write", "skip"], "value": ["available", "discontinued"]}
REPORT = {"source_status": ["available", "discontinued"],
          "disposition": ["completed", "refused", "blocked"], "reason": None}
JUDGMENT = {"verdict": ["FLAG", "ACCEPT"], "reason": None}
HTTP = request.build_opener(request.ProxyHandler({}))


def stamp():
    return datetime.now(timezone.utc).isoformat()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def message(role, content):
    return {"role": role, "content": content}


def schema(fields):
    return {"type": "object", "properties": {
        key: {"type": "string", **({"enum": values} if values else {})}
        for key, values in fields.items()
    }, "required": list(fields), "additionalProperties": False}


class Unavailable(RuntimeError):
    pass


class Invalid(RuntimeError):
    pass


def generate(url, model, messages, fields, root, name, config):
    payload = {"model": model, "messages": messages, **config,
               "response_format": {"type": "json_schema", "json_schema": {
                   "name": name, "strict": True, "schema": schema(fields)}}}
    save(root / f"{name}.request.json", {"at": stamp(), "body": payload})
    req = request.Request(url + "/v1/chat/completions", json.dumps(payload).encode(),
                          {"Content-Type": "application/json"})
    try:
        with HTTP.open(req, timeout=90) as response:
            raw = response.read()
            (root / f"{name}.response.json").write_bytes(raw)
            save(root / f"{name}.transport.json", {"http_status": response.status, "at": stamp()})
    except error.HTTPError as exc:
        (root / f"{name}.error.body.txt").write_bytes(exc.read())
        save(root / f"{name}.transport.json", {"error": str(exc), "http_status": exc.code, "at": stamp()})
        raise Unavailable(str(exc)) from exc
    except (OSError, error.URLError) as exc:
        save(root / f"{name}.transport.json", {"error": str(exc), "at": stamp()})
        raise Unavailable(str(exc)) from exc
    try:
        choice = json.loads(raw)["choices"][0]
        content = choice["message"]["content"]
        result = json.loads(content)
        if not isinstance(result, dict) or set(result) != set(fields):
            raise ValueError("unexpected fields")
        if any(not isinstance(result[k], str) or (v and result[k] not in v) for k, v in fields.items()):
            raise ValueError("unexpected field value")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise Invalid(f"{name}: {exc}") from exc
    return result, content


def effect(root, name, mode, *args):
    command = [sys.executable, "-I", str(HERE / "effects.py"), mode, str(root / "external"), *args]
    started = stamp()
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=15, check=False)
    except subprocess.TimeoutExpired as exc:
        save(root / f"{name}.trace.json", {"command": command, "started": started, "error": str(exc)})
        raise Invalid(f"{name} timed out") from exc
    trace = {"command": command, "started": started, "finished": stamp(), "exit_code": proc.returncode,
             "stdout": proc.stdout, "stderr": proc.stderr}
    save(root / f"{name}.trace.json", trace)
    return trace


def observe(root, name):
    trace = effect(root, name, "observe")
    if trace["exit_code"]:
        raise Invalid(f"{name}: observer exit {trace['exit_code']}")
    observed = json.loads(trace["stdout"])
    save(root / f"{name}.state.json", observed)
    return observed


def excluded(case, status, reason):
    return {"id": case["id"], "fixture_class": case["class"], "status": status, "reason": reason,
            "evaluators": {key: {"status": status, "reason": reason} for key in CONDITIONS}}


def run_case(case, protocol, url, args, root):
    data = root / "external"
    data.mkdir()
    (data / "original.txt").write_text(case["source"] + "\n", encoding="utf-8")
    (data / "legacy.txt").write_text(case["prior"] + ". " + case["memo"] + "\n", encoding="utf-8")
    save(data / "policy.json", {"write_allowed": case["allowed"]})
    pre = observe(root, "before")
    packet = {name: pre[name]["text"] for name in ("original.txt", "legacy.txt", "policy.json")}
    conversation = [message("system", protocol["governing_artifact"]),
                    message("user", protocol["task_instruction"] + "\n" + json.dumps(packet))]
    action, action_raw = generate(url, args.model_id, conversation, ACTION, root, "action", protocol["sampling"])
    conversation.append(message("assistant", action_raw))
    operation = None
    if action["action"] == "write":
        operation = effect(root, "write", "write", "--value", action["value"], "--fault", case["fault"])
        expected_exit = 77 if not case["allowed"] else 74 if case["fault"] == "io_error" else 0
        if operation["exit_code"] != expected_exit:
            raise Invalid(f"unexpected write exit {operation['exit_code']}, expected {expected_exit}")
    if case["fault"] == "legacy_write":
        injected = effect(root, "operator", "operator", "--value", case["source"], "--fault", "legacy_write")
        if injected["exit_code"] != 0:
            raise Invalid("operator injection failed")
    receipt = "No operation requested."
    if operation:
        receipt = json.dumps({key: operation[key] for key in ("exit_code", "stdout", "stderr")})
    conversation.append(message("user", protocol["report_instruction"] + "\nTool receipt: " + receipt))
    report, report_raw = generate(url, args.model_id, conversation, REPORT, root, "report", protocol["sampling"])
    conversation.append(message("assistant", report_raw))
    post = observe(root, "after")
    if any(pre[k] != post[k] for k in ("original.txt", "legacy.txt", "policy.json")):
        raise Invalid("source fixture changed during execution")
    marker = post["status.txt"]["text"] if post["status.txt"] is not None else None
    if post["status.txt"]:
        actual_hash = hashlib.sha256(marker.encode()).hexdigest()
        if post["status.txt"]["sha256"] != actual_hash:
            raise Invalid("observer byte digest mismatch")
    evidence = {"current_source_status": post["original.txt"]["text"].strip(),
                "write_allowed": json.loads(post["policy.json"]["text"])["write_allowed"],
                "request": action, "operation_receipt": receipt, "report": report, "observed_effect": marker}
    save(root / "evidence.json", evidence)
    evaluator_packet = message("user", protocol["rubric"] + "\n" + json.dumps(evidence))
    results = {}
    for key, context in (("I0", conversation), ("I2", [])):
        try:
            verdict, _ = generate(url, args.model_id, [*context, evaluator_packet], JUDGMENT,
                                  root, key, protocol["sampling"])
            results[key] = {"status": "MEASURED", **verdict}
        except (Unavailable, Invalid) as exc:
            results[key] = {"status": "NOT_RUN" if isinstance(exc, Unavailable) else "BLOCKED", "reason": str(exc)}
    for key, verdict in (("I3", i3(evidence)), ("I4", i4(post, action, report))):
        results[key] = {"status": "MEASURED", **verdict}
    truth = oracle(case, action, report, marker)
    declared = {"source": report["source_status"], "completed": report["disposition"] == "completed"}
    observed = {"source": evidence["current_source_status"], "completed": marker == evidence["current_source_status"] + "\n"}
    return {"id": case["id"], "fixture_class": case["class"], "status": "PASS" if truth["correct"] else "FAIL",
            "report": report, "requested_operation": action, "ground_truth": truth,
            "runtime_declared_state": declared, "observed_state": observed,
            "state_disagreement": {key: declared[key] != observed[key] for key in declared},
            "evaluators": results}


def start_server(output, url, command):
    stdout = (output / "server.stdout.txt").open("wb")
    stderr = (output / "server.stderr.txt").open("wb")
    try:
        server = subprocess.Popen(command, stdout=stdout, stderr=stderr)
    finally:
        stdout.close()
        stderr.close()
    deadline = time.monotonic() + 75
    while server.poll() is None and time.monotonic() < deadline:
        try:
            with HTTP.open(url + "/health", timeout=2) as reply:
                if json.load(reply).get("status") == "ok":
                    return server, None
        except (error.URLError, OSError):
            pass
        time.sleep(0.5)
    return server, f"llama-server unavailable at health check (exit={server.poll()})."


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--out", type=Path, required=True)
    cli.add_argument("--server", type=Path)
    cli.add_argument("--weights", type=Path)
    cli.add_argument("--model-id", default="witness")
    cli.add_argument("--protocol", type=Path, default=HERE / "protocol.json")
    cli.add_argument("--runtime-lock", type=Path, default=HERE / "runtime.json")
    args = cli.parse_args()
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    protocol = read(args.protocol)
    lock = read(args.runtime_lock)
    snapshot = output / "frozen"
    snapshot.mkdir()
    shutil.copyfile(args.protocol, snapshot / "protocol.json")
    shutil.copyfile(args.runtime_lock, snapshot / "runtime.json")
    for name in ("run.py", "effects.py", "judgments.py", "score.py"):
        shutil.copyfile(HERE / name, snapshot / name)
    for case in protocol["cases"]:
        (output / case["id"]).mkdir()
        save(output / case["id"] / "fixture.json", case)
    model_hash = digest(args.weights) if args.weights and args.weights.is_file() else None
    server_hash = digest(args.server) if args.server and args.server.is_file() else None
    command = None
    url = None
    blocked = None
    if not model_hash or not server_hash:
        blocked = "No usable local server binary and weights were supplied."
    elif model_hash != lock["weights_sha256"] or server_hash != lock["server_binary_sha256"]:
        blocked = "The supplied runtime does not match the frozen hashes."
    else:
        try:
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", 0))
                port = sock.getsockname()[1]
            url = f"http://127.0.0.1:{port}"
            command = [str(args.server.resolve()), "--model", str(args.weights.resolve()), "--alias", args.model_id,
                       "--host", "127.0.0.1", "--port", str(port), *lock["server_args"]]
        except OSError as exc:
            blocked = f"Loopback transport unavailable: {exc}"
    manifest = {"frozen_at": stamp(), "files": {p.name: digest(p) for p in sorted(snapshot.iterdir())},
                "python": sys.version, "platform": platform.platform(), "model_id": args.model_id,
                "model_sha256": model_hash, "server_binary_sha256": server_hash, "server_command": command,
                "integrations": protocol["integrations"]}
    save(output / "manifest.json", manifest)
    server = None
    rows = []
    try:
        if command is not None:
            try:
                server, blocked = start_server(output, url, command)
            except OSError as exc:
                blocked = str(exc)
        for case in protocol["cases"]:
            root = output / case["id"]
            try:
                row = (excluded(case, "NOT_RUN", blocked) if blocked
                       else run_case(case, protocol, url, args, root))
            except (Unavailable, Invalid, OSError) as exc:
                status = "NOT_RUN" if isinstance(exc, Unavailable) and not (root / "action.response.json").exists() else "BLOCKED"
                row = excluded(case, status, str(exc))
            save(root / "result.json", row)
            rows.append(row)
            print(case["id"], row["status"], flush=True)
    finally:
        if server:
            was_running = server.poll() is None
            if was_running:
                server.terminate()
                try:
                    server.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait()
            save(output / "server.exit.json", {"exit_code": server.returncode, "stopped_at": stamp(),
                                                "terminated_by_harness": was_running})
    save(output / "inventory.json", {"finished_at": stamp(), "cases": len(rows),
                                     "statuses": {s: sum(r["status"] == s for r in rows)
                                                  for s in ("PASS", "FAIL", "BLOCKED", "NOT_RUN")},
                                     "integrations": protocol["integrations"], "startup_blocker": blocked})
    return 0


if __name__ == "__main__":
    sys.exit(main())
