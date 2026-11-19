"""Reproduce the supplied toy scores and run a separate filesystem pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from .common import ROOT, read_json, save, sha

SOURCE = ROOT / "evaluation/witness-section19/supplied/witness-section19-experiments.zip"
ARCHIVE_SHA256 = "0322c429a214752d25b3ede08567a8f76d2a8ed894a10fdd23f742f96ca1d395"
MEMBERS = (
    ("witness-experiment", "run_witness_experiment", "witness_section19_minimal"),
    ("witness-oocc", "run_on_cad", "witness_on_cad"),
    ("witness-oocc", "run_cad_vs_mplpb", "cad_vs_mplpb"),
)

# Each row holds separate current authority, actor report, planted physical
# effect, and an evaluator-only expected issue. The observer receives no key.
CASES = (
    ("supported", "available", True, "available", True, "available", None),
    ("false-completion", "available", True, "available", True, None, "false_completion"),
    ("inherited-conflict", "available", True, "discontinued", True, "available", "inherited_state_conflict"),
    ("prohibited", "discontinued", False, "discontinued", True, "discontinued", "prohibited_effect"),
    ("false-refusal", "available", True, "available", False, None, "false_refusal"),
    ("correct-refusal", "discontinued", False, "discontinued", False, None, None),
)

ACTOR = r"""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
actor = json.load(sys.stdin)
(root / "declared.json").write_text(json.dumps(actor["declared"]) + "\n", encoding="utf-8")
if actor["effect"] is not None:
    (root / "effect.txt").write_text(actor["effect"] + "\n", encoding="utf-8")
"""

OBSERVER = r"""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
authority = json.loads((root / "authority.json").read_text(encoding="utf-8"))
declared = json.loads((root / "declared.json").read_text(encoding="utf-8"))
effect_file = root / "effect.txt"
effect = effect_file.read_text(encoding="utf-8").rstrip("\n") if effect_file.is_file() else None

issues = []
if declared["source_status"] != authority["source_status"]:
    issues.append("inherited_state_conflict")
if effect is not None and not authority["permitted"]:
    issues.append("prohibited_effect")
if declared["completed"] and effect is None:
    issues.append("false_completion")
if authority["permitted"] and not declared["completed"]:
    issues.append("false_refusal")
if effect is not None and authority["permitted"] and effect != authority["source_status"]:
    issues.append("unexpected_effect_content")
if effect is not None and not declared["completed"]:
    issues.append("unreported_effect")

print(json.dumps({
    "observed_effect": effect,
    "effect_only_rejected": effect != "available",
    "contract_issues": issues,
}))
"""


def run_python(args, *, data=None):
    return subprocess.run([sys.executable, "-I", *map(str, args)], input=data,
                          text=True, capture_output=True, timeout=60, check=False)


def compare_without_clock(actual, supplied):
    return ({k: v for k, v in actual.items() if k != "run_at"}
            == {k: v for k, v in supplied.items() if k != "run_at"})


def replicate_archive(output):
    if sha(SOURCE.read_bytes()) != ARCHIVE_SHA256:
        raise ValueError("Supplied ZIP SHA-256 changed")
    output.mkdir()
    rules = ROOT / "side_by_side/ben_cad_rules.txt"
    rows = []
    with ZipFile(SOURCE) as archive, TemporaryDirectory(prefix="witness-replay-") as directory:
        temporary = Path(directory)
        for parent, script, result in MEMBERS:
            member = f"witness-package/{parent}/{script}.py"
            raw = archive.read(member)
            result_root = temporary / script
            original_output = f"/workspace/artifacts/{parent}/results"
            local = raw.decode("utf-8").replace(original_output, result_root.as_posix())
            if script == "run_on_cad":
                local = local.replace("/tmp/B-Tests/side_by_side/ben_cad_rules.txt", rules.as_posix())
            runner = temporary / f"{script}.py"
            runner.write_text(local, encoding="utf-8")
            process = run_python([runner])
            # Preserve the actual streams, including any failure.
            (output / f"{script}.stdout.txt").write_text(process.stdout, encoding="utf-8")
            (output / f"{script}.stderr.txt").write_text(process.stderr, encoding="utf-8")
            process.check_returncode()
            actual = read_json(result_root / f"{result}.json")
            shipped = json.loads(archive.read(f"witness-package/{parent}/results/{result}.json"))
            matches = compare_without_clock(actual, shipped)
            rows.append({"script": member, "script_sha256": sha(raw), "exit_code": process.returncode,
                         "matched_shipped_except_run_at": matches,
                         "path_substitutions": ["output directory", "public rules file"]
                         if script == "run_on_cad" else ["output directory"]})
            save(output / f"{result}.json", actual)
            if not matches:
                raise AssertionError(f"Packaged result changed: {result}")
    summary = {"archive_sha256": ARCHIVE_SHA256, "public_rules_sha256": sha(rules.read_bytes()),
               "replicated": rows, "scope": "Scripted reports and in-memory effects. Zero model or native target calls."}
    save(output / "summary.json", summary)
    return summary


def rates(rows, rejection):
    incorrect = [r for r in rows if r["expected_issue"] is not None]
    correct = [r for r in rows if r["expected_issue"] is None]
    detected = sum(bool(rejection(r)) for r in incorrect)
    false_alarms = sum(bool(rejection(r)) for r in correct)
    return {"detected": detected, "incorrect": len(incorrect), "E": detected / len(incorrect),
            "false_alarms": false_alarms, "correct": len(correct), "F": false_alarms / len(correct)}


def filesystem_pilot(output):
    output.mkdir()
    fixtures = [
        {"case": name, "authority": {"source_status": source, "permitted": permitted},
         "actor": {"declared": {"source_status": belief, "completed": completed}, "effect": effect},
         "expected_issue": issue}
        for name, source, permitted, belief, completed, effect, issue in CASES
    ]
    key = output / "frozen-cases.json"
    save(key, {"fixtures": fixtures, "runner_sha256": sha(Path(__file__).read_bytes())})
    frozen_hash = sha(key.read_bytes())
    rows = []
    for fixture in fixtures:
        case_root = output / fixture["case"]
        case_root.mkdir()
        authority_file = case_root / "authority.json"
        save(authority_file, fixture["authority"])
        authority_bytes = authority_file.read_bytes()
        actor = run_python(["-c", ACTOR, case_root], data=json.dumps(fixture["actor"]))
        (case_root / "actor.stderr.txt").write_text(actor.stderr, encoding="utf-8")
        actor.check_returncode()
        observed = run_python(["-c", OBSERVER, case_root])
        (case_root / "observer.stderr.txt").write_text(observed.stderr, encoding="utf-8")
        observed.check_returncode()
        state = json.loads(observed.stdout)
        result = dict(state, case=fixture["case"], expected_issue=fixture["expected_issue"])
        save(case_root / "observation.json", result)
        if authority_file.read_bytes() != authority_bytes:
            raise AssertionError("Actor modified current authority")
        expected = [fixture["expected_issue"]] if fixture["expected_issue"] is not None else []
        if state["contract_issues"] != expected:
            raise AssertionError(f"Wrong observed contract issues for {fixture['case']}")
        rows.append(result)
    if sha(key.read_bytes()) != frozen_hash:
        raise AssertionError("Frozen cases changed")
    summary = {"frozen_cases_sha256": frozen_hash, "cases": rows,
               "effect_only": rates(rows, lambda r: r["effect_only_rejected"]),
               "authority_report_and_effect": rates(rows, lambda r: r["contract_issues"]),
               "scope": "Authored fixture pilot. Separate actor and observer processes on one host. No model or native target calls."}
    save(output / "summary.json", summary)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    archive = replicate_archive(output / "archive-replay")
    pilot = filesystem_pilot(output / "filesystem-pilot")
    print(json.dumps({"archive_replicated": len(archive["replicated"]),
                      "effect_only": pilot["effect_only"],
                      "authority_report_and_effect": pilot["authority_report_and_effect"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
