"""Falsification-first paired evaluation. No adapter = no AI observations.

The MPLPB arm calls the pinned repository's real Python CLI; the CAD and
strong-baseline arms call a user-supplied *real AI* command, once per arm/case.
No deterministic simulation of a model is labeled an AI test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
PIN = "257e54a51edac272eb6b2441457f38a40485ee4d"
ARMS = ("CAD", "BASELINE", "MPLPB")
DECISIONS = ("ANSWER", "REFUSE", "CONFLICT")


def load_manifest(path: Path = BASE / "cases.json") -> dict:
    raw = path.read_bytes()
    o = json.loads(raw)
    if o.get("schema") != "btests-side-by-side-1":
        raise ValueError("Unsupported manifest schema")
    if o.get("mplpb_pin") != PIN:
        raise ValueError("MPLPB pin differs from frozen protocol")
    ids = [c["id"] for c in o["cases"]]
    if len(ids) != len(set(ids)) or len(ids) < 12:
        raise ValueError("Duplicate or incomplete case inventory")
    for c in o["cases"]:
        if c["expected"] not in DECISIONS:
            raise ValueError("Bad oracle: " + c["id"])
        if c["category"] not in ("shared_query", "instruction_only"):
            raise ValueError("Unexpected case type")
        sids = [s["id"] for s in c["sources"]]
        if len(set(sids)) != len(sids):
            raise ValueError("Duplicate source identifiers")
    o["_sha256"] = hashlib.sha256(raw).hexdigest()
    return o


def prompt(case: dict, arm: str) -> dict:
    if arm not in ("CAD", "BASELINE"):
        raise ValueError("MPLPB is an executable arm, not an LLM instruction")
    rules = (BASE / ("ben_cad_rules.txt" if arm == "CAD" else "strong_baseline_rules.txt")).read_text()
    # Identical evidence bytes across the two AI prompt arms.
    evidence = json.dumps({"case_id": case["id"], "query": case["query"], "sources": case["sources"]},
                          sort_keys=True, ensure_ascii=False)
    return {"schema": "btests-model-input-1", "arm": arm, "case_id": case["id"],
            "system": rules, "user": evidence, "fresh_session": True,
            "output_schema": {"decision": "ANSWER|REFUSE|CONFLICT", "answer": "string", "evidence_ids": ["source-id"]}}


def validate_model_response(case: dict, value: dict) -> tuple[str, dict]:
    if not isinstance(value, dict) or value.get("decision") not in DECISIONS:
        return "INVALID_RESPONSE", {"error": "Missing/invalid decision"}
    if not isinstance(value.get("answer"), str) or not isinstance(value.get("evidence_ids"), list):
        return "INVALID_RESPONSE", {"error": "Missing answer/evidence_ids types"}
    actual_sources = {s["id"] for s in case["sources"]}
    used = value["evidence_ids"]
    if any(not isinstance(x, str) or x not in actual_sources for x in used):
        return "FAIL", {"error": "Fabricated source reference"}
    if value["decision"] != case["expected"]:
        return "FAIL", {"expected": case["expected"], "observed": value["decision"]}
    if case["expected"] == "ANSWER":
        if case.get("expected_source") not in used:
            return "FAIL", {"error": "Correct result without required original source citation"}
        if case.get("expected_phrase", "").lower() not in value["answer"].lower():
            return "FAIL", {"error": "Expected complete information missing"}
    if case["expected"] != "ANSWER" and value["answer"].strip():
        # Text explaining refusal is permissible; only incorrect decisive output is prohibited.
        pass
    return "PASS_RESPONSE_CONTRACT", {}


def call_model(case: dict, arm: str, command: str, timeout: int) -> dict:
    request = prompt(case, arm)
    start = time.perf_counter()
    try:
        p = subprocess.run(shlex.split(command), input=json.dumps(request), text=True,
                           capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "ADAPTER_ERROR", "error": str(exc), "arm": arm, "case_id": case["id"]}
    rec = {"arm": arm, "case_id": case["id"], "elapsed_seconds": round(time.perf_counter()-start, 6),
           "exit_code": p.returncode, "stderr_excerpt": p.stderr[:700]}
    if p.returncode:
        return rec | {"status": "ADAPTER_ERROR", "error": "Model adapter nonzero"}
    try:
        obj = json.loads(p.stdout)
        if "response" in obj and isinstance(obj["response"], dict):
            obj = obj["response"]
    except ValueError:
        return rec | {"status": "INVALID_RESPONSE", "error": "Model adapter did not emit JSON", "raw": p.stdout[:800]}
    status, diagnostic = validate_model_response(case, obj)
    return rec | {"status": status, "diagnostic": diagnostic, "response": obj}


def run_cli(repo: Path, args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", *args], cwd=repo, capture_output=True,
                          text=True, timeout=timeout, check=False)


def _write_source(repo: Path, root: Path, source: dict) -> str:
    cmd = ["mplpb_combined", "write", str(root), "--title", "Fixture " + source["id"],
           "--scope", "source evidence test", "--body", source["body"], "--origin", "human", "--prefix", "PROBE"]
    p = run_cli(repo, cmd)
    if p.returncode:
        raise RuntimeError("write failed: " + p.stderr[:1300])
    match = re.search(r"\bwrote\s+([A-Za-z0-9_-]+)\s+", p.stdout)
    if not match:
        raise RuntimeError("Could not parse genuine ledger-written document id: " + p.stdout[:300])
    ident = match.group(1)
    if source.get("state") == "retired":
        z = run_cli(repo, ["mplpb_combined", "withdraw", str(root), ident])
        if z.returncode:
            raise RuntimeError("withdraw failed: " + z.stderr[:300])
    if source.get("tamper_after_seal"):
        pages = [p for p in root.rglob("*.html") if p.stem.casefold() == ident.casefold()]
        if len(pages) != 1:
            raise RuntimeError("Cannot uniquely locate sealed source page for tamper test")
        pth = pages[0]
        text = pth.read_text(encoding="utf-8")
        if source["body"] not in text:
            raise RuntimeError("Exact source body missing from sealed HTML page")
        pth.write_text(text.replace(source["body"], source["tamper_after_seal"]), encoding="utf-8")
    return ident


def run_mplpb(case: dict, repo: Path) -> dict:
    base = {"arm": "MPLPB", "case_id": case["id"], "repo_pin": PIN}
    if case["category"] != "shared_query":
        return base | {"status": "OUT_OF_SCOPE", "reason": "This is not a declared strict MPLPB query capability"}
    if not repo.is_dir() or not (repo / "mplpb_answers" / "pipeline.py").is_file():
        return base | {"status": "NOT_RUN", "reason": "MPLPB checkout not present"}
    start = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory(prefix="btests-paired-") as folder:
            folder = Path(folder)
            id_map = {s["id"]: _write_source(repo, folder, s) for s in case["sources"]}
            p = run_cli(repo, ["mplpb_answers", "ask", str(folder), case["query"], "--json"], timeout=45)
            try:
                reply = json.loads(p.stdout)
            except ValueError:
                return base | {"status": "ADAPTER_ERROR", "reason": "No JSON response", "stdout": p.stdout[:800], "stderr": p.stderr[:800]}
            kind = reply.get("kind")
            decision = {"return": "ANSWER", "not_in_corpus": "REFUSE", "ambiguous": "CONFLICT"}.get(kind)
            if decision is None:
                return base | {"status": "INVALID_RESPONSE", "kind": kind, "raw": reply}
            # Strict supported answers must identify the complete expected source-body phrase.
            serialization = json.dumps(reply, ensure_ascii=False).lower()
            ok = decision == case["expected"]
            if ok and case["expected"] == "ANSWER":
                ok = case.get("expected_phrase", "").lower() in serialization
                # Source IDs are dynamically allocated by the real ledger; return the mapping.
            return base | {"status": "PASS_CONTRACT" if ok else "FAIL_CONTRACT",
                           "observed_decision": decision, "expected_decision": case["expected"],
                           "elapsed_seconds": round(time.perf_counter()-start, 6),
                           "source_id_map": id_map, "native_reply": reply,
                           "stderr_excerpt": p.stderr[:400], "returncode": p.returncode}
    except Exception as exc:
        return base | {"status": "ADAPTER_ERROR", "error": str(exc)}


def execute(manifest: dict, mplpb_repo: Path | None, model_command: str | None, timeout: int, max_cases: int = 0) -> dict:
    cases = manifest["cases"][:max_cases] if max_cases else manifest["cases"]
    results = []
    for case in cases:
        results.append(run_mplpb(case, mplpb_repo) if mplpb_repo else
                       {"arm": "MPLPB", "case_id": case["id"], "status": "OUT_OF_SCOPE" if case["category"] != "shared_query" else "NOT_RUN"})
        for arm in ("CAD", "BASELINE"):
            results.append(call_model(case, arm, model_command, timeout) if model_command else
                           {"arm": arm, "case_id": case["id"], "status": "NOT_RUN", "reason": "No real AI adapter configured"})
    counts = {}
    for a in ARMS:
        counts[a] = {status: sum(1 for r in results if r["arm"] == a and r["status"] == status)
                     for status in sorted({r["status"] for r in results if r["arm"] == a})}
    return {"schema": "btests-paired-results-1", "scope": "pinned native MPLPB vs Ben-derived CAD instructions vs matched governance baseline",
            "manifest_sha256": manifest["_sha256"], "mplpb_pin": PIN, "model_command_supplied": bool(model_command),
            "native_mplpb_checked": bool(mplpb_repo and (mplpb_repo / "mplpb_answers" / "pipeline.py").exists()),
            "arms": counts, "results": results,
            "warning": "Passing instructions are observed behavior of the selected AI model, not proof of Ben's native OOCC controller. This is authored development data, not an independent holdout."}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=BASE / "cases.json")
    p.add_argument("--mplpb-root", type=Path, help="REAL checkout of pinned MPLPB repository")
    p.add_argument("--model-command", help="Real AI adapter command; stdin request JSON, stdout response JSON")
    p.add_argument("--timeout", type=int, default=50)
    p.add_argument("--max-cases", type=int, default=0)
    p.add_argument("--out", type=Path, default=BASE / "results.json")
    p.add_argument("--require-live", action="store_true", help="Exit 2 when a required target was not actually run")
    args = p.parse_args(argv)
    m = load_manifest(args.manifest)
    if args.mplpb_root:
        pin = subprocess.run(["git", "-C", str(args.mplpb_root), "rev-parse", "HEAD"],
                             capture_output=True, text=True)
        if pin.returncode or pin.stdout.strip() != PIN:
            print("REFUSED: MPLPB checkout is not at the frozen commit " + PIN, file=sys.stderr)
            return 2
    result = execute(m, args.mplpb_root, args.model_command, args.timeout, args.max_cases)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"arms": result["arms"], "manifest_sha256": result["manifest_sha256"]}, indent=2))
    absent = any(r["status"] == "NOT_RUN" for r in result["results"])
    bad = any(r["status"] in ("FAIL_CONTRACT", "FAIL", "ADAPTER_ERROR", "INVALID_RESPONSE") for r in result["results"])
    if args.require_live and absent:
        return 2
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
