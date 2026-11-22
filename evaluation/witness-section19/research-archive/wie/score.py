"""Score verdict files against the sealed key.

Per judge:
  E  detection rate   = REJECT on planted-incorrect cases / planted-incorrect cases
  F  false-alarm rate = REJECT on correct cases / correct cases
  J  discrimination   = E - F   (Youden's J; 0 = no better than a coin, 1 = perfect)
  coverage            = share of cases not ABSTAIN
ABSTAIN never counts as a detection and never as a false alarm; it shows up in
coverage. 95% intervals are Wilson score intervals.

Paired comparisons use an exact McNemar test on the same planted-incorrect
cases (did judge A catch it, did judge B catch it).
"""

import json
import math
from pathlib import Path

from . import ABSTAIN, CLASSES, REJECT
from .freeze import verify
from .util import dump_json, read_jsonl


def wilson(k: int, n: int, z: float = 1.959964):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact p for discordant counts b (A only) and c (B only)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def _level(label: str) -> str:
    return label.split("_", 1)[0]


def score(run_dir: Path, key_path: Path = None, comparisons=None) -> dict:
    run_dir = Path(run_dir)
    key_path = Path(key_path or run_dir / "sealed" / "key.jsonl")
    manifest = verify(run_dir, key_path)
    key = {r["case_id"]: r for r in read_jsonl(key_path)}
    vfiles = sorted((run_dir / "verdicts").glob("*.jsonl"))
    if not vfiles:
        raise FileNotFoundError("no verdict files in verdicts/")
    judges = {}
    detected = {}
    for vf in vfiles:
        label = vf.stem
        rows = {r["case_id"]: r["verdict"] for r in read_jsonl(vf)}
        if set(rows) != set(key):
            raise ValueError(f"{vf.name}: verdicts do not cover exactly the frozen cases")
        inc = [c for c, k in key.items() if k["expected"] == REJECT]
        cor = [c for c, k in key.items() if k["expected"] != REJECT]
        tp = sum(rows[c] == REJECT for c in inc)
        fp = sum(rows[c] == REJECT for c in cor)
        abst = sum(v == ABSTAIN for v in rows.values())
        E, F = tp / len(inc), fp / len(cor)
        per_class = {}
        for cls in CLASSES:
            ids = [c for c, k in key.items() if k["class"] == cls]
            if not ids:
                continue
            rej = sum(rows[c] == REJECT for c in ids)
            ab = sum(rows[c] == ABSTAIN for c in ids)
            per_class[cls] = {"n": len(ids), "rejected": rej, "abstained": ab,
                              "reject_rate": rej / len(ids), "expected": key[ids[0]]["expected"]}
        judges[label] = {
            "level": _level(label), "n_cases": len(key), "n_incorrect": len(inc), "n_correct": len(cor),
            "E": E, "E_ci95": wilson(tp, len(inc)), "F": F, "F_ci95": wilson(fp, len(cor)),
            "J": E - F, "coverage": 1 - abst / len(key), "abstained": abst, "per_class": per_class,
        }
        detected[label] = {c: rows[c] == REJECT for c in inc}

    pairs = comparisons or _default_pairs(list(judges))
    paired = []
    for a, b in pairs:
        if a not in detected or b not in detected:
            continue
        only_a = sum(detected[a][c] and not detected[b][c] for c in detected[a])
        only_b = sum(detected[b][c] and not detected[a][c] for c in detected[a])
        paired.append({"a": a, "b": b, "caught_by_a_only": only_a, "caught_by_b_only": only_b,
                       "mcnemar_p": mcnemar_exact(only_a, only_b)})

    story_state = None
    if "I0_self_assessment" in detected and "I4_retained_state" in detected:
        diverge = sum(detected["I4_retained_state"][c] and not detected["I0_self_assessment"][c]
                      for c in detected["I0_self_assessment"])
        story_state = {"incorrect_cases_where_report_passed_but_state_failed": diverge}

    result = {"root_sha256": manifest["root_sha256"], "judges": judges, "paired": paired,
              "story_vs_state": story_state}
    out = run_dir / "results"
    dump_json(out / "results.json", result)
    (out / "RESULTS.md").write_text(_markdown(result), encoding="utf-8")
    return result


def _default_pairs(labels):
    lab = sorted(labels)
    lowest = [l for l in lab if l.startswith("I0")]
    return [(a, b) for a in lowest for b in lab if b != a]


def _pct(x):
    return "—" if x is None else f"{100 * x:.1f}%"


def _ci(ci):
    return "—" if ci[0] is None else f"{100 * ci[0]:.0f}–{100 * ci[1]:.0f}%"


def _markdown(r) -> str:
    L = ["# Witness-Independence Experiment: results", "",
         f"Frozen run root hash: `{r['root_sha256']}`", "",
         "E = detection of planted-incorrect states. F = false alarms on correct states. "
         "J = E − F (discrimination). ABSTAIN counts as neither.", "",
         "| Judge | Level | E | E 95% CI | F | F 95% CI | J | Coverage |",
         "|---|---|---|---|---|---|---|---|"]
    for name, j in sorted(r["judges"].items()):
        L.append(f"| {name} | {j['level']} | {_pct(j['E'])} | {_ci(j['E_ci95'])} | {_pct(j['F'])} | "
                 f"{_ci(j['F_ci95'])} | {j['J']:+.2f} | {_pct(j['coverage'])} |")
    L += ["", "## Reject rate by case class", "",
          "Rows marked (correct) should be near 0%; the rest should be near 100%.", ""]
    names = sorted(r["judges"])
    L.append("| Class | " + " | ".join(names) + " |")
    L.append("|---|" + "---|" * len(names))
    for cls in CLASSES:
        cells = []
        for n in names:
            pc = r["judges"][n]["per_class"].get(cls)
            cells.append("—" if pc is None else _pct(pc["reject_rate"]))
        tag = " (correct)" if r["judges"][names[0]]["per_class"].get(cls, {}).get("expected") != REJECT else ""
        L.append(f"| {cls}{tag} | " + " | ".join(cells) + " |")
    if r["paired"]:
        L += ["", "## Paired comparisons on planted-incorrect cases (exact McNemar)", "",
              "| A | B | caught by A only | caught by B only | p |", "|---|---|---|---|---|"]
        for p in r["paired"]:
            L.append(f"| {p['a']} | {p['b']} | {p['caught_by_a_only']} | {p['caught_by_b_only']} | "
                     f"{p['mcnemar_p']:.3g} |")
    if r["story_vs_state"]:
        L += ["", f"Story vs. state: {r['story_vs_state']['incorrect_cases_where_report_passed_but_state_failed']} "
                  "planted-incorrect cases where the runtime's self-assessment said PASS and the retained state said FAIL."]
    return "\n".join(L) + "\n"
