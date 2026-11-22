"""Descriptive, matched-evidence analysis for a crossed Witness judge replay."""

import argparse
from fractions import Fraction
import json
from pathlib import Path


LEVELS = ("I0_model", "I2_fresh", "I3_cross")
MODES = ("report_only", "report_plus_state")
VERDICTS = {"ACCEPT", "REJECT", "ABSTAIN"}


def read_rows(path, field, allowed):
    rows = {}
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            case = row["case_id"]
            value = row[field]
            if case in rows or value not in allowed:
                raise ValueError(f"{path}: duplicate case or invalid {field}: {case}")
            rows[case] = value
    return rows


def metrics(truth, verdicts):
    wrong = [case for case in truth if truth[case] == "REJECT"]
    correct = [case for case in truth if truth[case] == "ACCEPT"]
    tp = sum(verdicts[case] == "REJECT" for case in wrong)
    fp = sum(verdicts[case] == "REJECT" for case in correct)
    tn = sum(verdicts[case] == "ACCEPT" for case in correct)
    coverage_wrong = Fraction(sum(verdicts[case] != "ABSTAIN" for case in wrong), len(wrong))
    coverage_correct = Fraction(sum(verdicts[case] != "ABSTAIN" for case in correct), len(correct))
    e, f = Fraction(tp, len(wrong)), Fraction(fp, len(correct))
    return {
        "E": e, "F": f, "J": e - f,
        "balanced_correct_verdict_rate": (e + Fraction(tn, len(correct))) / 2,
        "coverage": Fraction(sum(verdict != "ABSTAIN" for verdict in verdicts.values()), len(truth)),
        "coverage_incorrect": coverage_wrong, "coverage_correct": coverage_correct,
    }


def contrast(truth, before, after, false_alarm_cap, coverage_drop_cap):
    missing_before = sorted(truth.keys() - before.keys())
    missing_after = sorted(truth.keys() - after.keys())
    if missing_before or missing_after or set(truth.values()) != {"ACCEPT", "REJECT"}:
        return {"status": "INCONCLUSIVE", "missing_before": missing_before, "missing_after": missing_after,
                "missing_class": set(truth.values()) != {"ACCEPT", "REJECT"}}
    baseline, candidate = metrics(truth, before), metrics(truth, after)
    delta = {key: candidate[key] - baseline[key] for key in baseline}
    reasons = []
    if delta["E"] > 0 and delta["F"] >= delta["E"]:
        reasons.append("detection_gain_offset_by_false_alarms")
    if delta["J"] <= 0 or delta["balanced_correct_verdict_rate"] <= 0:
        reasons.append("no_gain_on_both_quality_measures")
    if delta["F"] > false_alarm_cap:
        reasons.append("false_alarm_increase_exceeds_limit")
    if any(delta[key] < -coverage_drop_cap for key in ("coverage_incorrect", "coverage_correct")):
        reasons.append("coverage_loss_exceeds_limit")
    wins = sum(after[c] == truth[c] and before[c] != truth[c] for c in truth)
    losses = sum(before[c] == truth[c] and after[c] != truth[c] for c in truth)
    return {"status": "QUALITY_GAIN" if not reasons else "CRITERIA_NOT_MET",
            "detection_claim_met": not reasons and delta["E"] > 0,
            "reasons": reasons, "before": baseline, "after": candidate, "delta": delta,
            "correct_verdict_switches": {"wins": wins, "losses": losses}}


def analyze(truth, arms, false_alarm_cap=Fraction(1, 10), coverage_drop_cap=Fraction(0)):
    if any(value not in {"ACCEPT", "REJECT"} for value in truth.values()):
        raise ValueError("Ground truth must be ACCEPT or REJECT")
    if not all(0 <= cap <= 1 for cap in (false_alarm_cap, coverage_drop_cap)):
        raise ValueError("Limits must be between 0 and 1")
    for verdicts in arms.values():
        if verdicts.keys() - truth.keys() or any(v not in VERDICTS for v in verdicts.values()):
            raise ValueError("Unknown case or invalid verdict")

    def compare(before, after):
        return contrast(truth, arms.get(before, {}), arms.get(after, {}), false_alarm_cap, coverage_drop_cap)

    steps = tuple(zip(LEVELS, LEVELS[1:]))
    matched = {mode: {f"{a}->{b}": compare((a, mode), (b, mode)) for a, b in steps} for mode in MODES}
    information = {level: compare((level, MODES[0]), (level, MODES[1])) for level in LEVELS}
    interactions = {}
    for a, b in steps:
        label = f"{a}->{b}"
        only, plus = (matched[mode][label].get("delta") for mode in MODES)
        if only is not None and plus is not None:
            interactions[label] = {key: plus[key] - only[key] for key in only}
    measured = [row for steps_by_mode in matched.values() for row in steps_by_mode.values()]
    all_measured = all(row["status"] != "INCONCLUSIVE" for row in measured)
    any_gain = any(row["status"] == "QUALITY_GAIN" for row in measured)
    return {
        "scope": "Descriptive. Context, rubric, and model implementation can differ between levels.",
        "cases": len(truth),
        "limits": {"max_false_alarm_increase": false_alarm_cap, "max_coverage_drop_per_class": coverage_drop_cap},
        "by_matched_evidence": matched,
        "evidence_added_within_judge": information,
        "interaction_added_state_minus_report_only": interactions,
        "monotonic_quality_gain": all(row["status"] == "QUALITY_GAIN" for row in measured) if all_measured else None,
        "monotonic_detection_gain": all(row["detection_claim_met"] for row in measured) if all_measured else None,
        "evidence_gain_without_matched_separation_gain": (
            not any_gain and any(row["status"] == "QUALITY_GAIN" for row in information.values())
            if all_measured else None
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="Scored WIE run directory")
    parser.add_argument("--key", type=Path, help="Override run/sealed/key.jsonl")
    parser.add_argument("--max-false-alarm-increase", type=Fraction, default=Fraction(1, 10))
    parser.add_argument("--max-coverage-drop", type=Fraction, default=Fraction(0))
    args = parser.parse_args()
    truth = read_rows(args.key or args.run / "sealed/key.jsonl", "expected", {"ACCEPT", "REJECT"})
    arms = {}
    for level in LEVELS:
        for mode in MODES:
            files = sorted((args.run / "verdicts").glob(f"{level}__{mode}__*.jsonl"))
            if len(files) > 1:
                parser.error(f"Ambiguous arm {level} {mode}: provide one verdict file per condition")
            if files:
                arms[level, mode] = read_rows(files[0], "verdict", VERDICTS)
    analysis = analyze(truth, arms, args.max_false_alarm_increase, args.max_coverage_drop)
    analysis["verdict_files"] = sorted(
        p.name for level, mode in arms for p in (args.run / "verdicts").glob(f"{level}__{mode}__*.jsonl")
    )
    print(json.dumps(analysis, indent=2, default=float))


if __name__ == "__main__":
    main()
