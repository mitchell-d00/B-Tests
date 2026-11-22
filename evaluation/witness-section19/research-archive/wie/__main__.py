"""Command line: python -m wie <command> ..."""

import argparse
import sys
from pathlib import Path

from .export import CONDITIONS, EVIDENCE, export, export_packets, import_verdicts
from .freeze import TamperError, freeze, verify
from .generate import generate
from .judges import run_deterministic
from .score import score
from .separation import separation_effect


def main(argv=None):
    ap = argparse.ArgumentParser(prog="wie", description="Witness-Independence Experiment")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="create a new run of cases")
    g.add_argument("run_dir"); g.add_argument("--seed", type=int, required=True)
    g.add_argument("--per-class", type=int, default=20)

    f = sub.add_parser("freeze", help="hash the run; publish the root hash before judging")
    f.add_argument("run_dir"); f.add_argument("--key")

    v = sub.add_parser("verify", help="check nothing changed since freeze")
    v.add_argument("run_dir"); v.add_argument("--key"); v.add_argument("--no-key", action="store_true")

    j = sub.add_parser("judge", help="run deterministic judges I0_self_assessment, I1_same_frame, I4_retained_state")
    j.add_argument("run_dir")

    e = sub.add_parser("export", help="write paste-ready batches for model judges")
    e.add_argument("run_dir"); e.add_argument("--condition", choices=CONDITIONS, required=True)
    e.add_argument("--evidence", choices=EVIDENCE, required=True)
    e.add_argument("--batch-size", type=int, default=10)

    k = sub.add_parser("packets", help="paste-ready I2/I3 (and I0_model) packets, both evidence modes")
    k.add_argument("run_dir"); k.add_argument("--batch-size", type=int, default=10)

    i = sub.add_parser("import", help="validate pasted model verdicts into verdicts/<label>.jsonl")
    i.add_argument("run_dir"); i.add_argument("--label", required=True,
                                               help="e.g. I3_cross__report_plus_state__grok")
    i.add_argument("files", nargs="+"); i.add_argument("--allow-missing", action="store_true")

    s = sub.add_parser("score", help="verify the freeze, then score every verdict file")
    s.add_argument("run_dir"); s.add_argument("--key")

    x = sub.add_parser("separation", help="test the effect of evaluator separation on overall judgment")
    x.add_argument("run_dir"); x.add_argument("--key")
    x.add_argument("--perms", type=int, default=5000); x.add_argument("--alpha", type=float, default=0.05)

    a = ap.parse_args(argv)
    try:
        if a.cmd == "generate":
            m = generate(Path(a.run_dir), a.seed, a.per_class)
            print(f"generated {m['n_cases']} cases (seed {a.seed}) in {a.run_dir}")
        elif a.cmd == "freeze":
            m = freeze(Path(a.run_dir), a.key)
            print(f"frozen. root sha256: {m['root_sha256']}")
            print("Publish this hash now, and move sealed/ somewhere the judges and fixers can't read.")
        elif a.cmd == "verify":
            m = verify(Path(a.run_dir), a.key, need_key=not a.no_key)
            print(f"ok: unchanged since freeze. root sha256: {m['root_sha256']}")
        elif a.cmd == "judge":
            verify(Path(a.run_dir), need_key=False)
            for label, p in run_deterministic(Path(a.run_dir)).items():
                print(f"{label}: {p}")
        elif a.cmd == "export":
            verify(Path(a.run_dir), need_key=False)
            ps = export(Path(a.run_dir), a.condition, a.evidence, a.batch_size)
            print(f"wrote {len(ps)} batches to {ps[0].parent}")
        elif a.cmd == "packets":
            verify(Path(a.run_dir), need_key=False)
            for name, ps in export_packets(Path(a.run_dir), a.batch_size).items():
                print(f"{name}: {len(ps)} batches in {ps[0].parent}")
        elif a.cmd == "import":
            p = import_verdicts(Path(a.run_dir), a.label, [Path(x) for x in a.files], a.allow_missing)
            print(f"imported: {p}")
        elif a.cmd == "separation":
            separation_effect(Path(a.run_dir), a.key, perms=a.perms, alpha=a.alpha)
            print((Path(a.run_dir) / "results" / "SEPARATION.md").read_text(encoding="utf-8"))
        elif a.cmd == "score":
            r = score(Path(a.run_dir), a.key)
            print((Path(a.run_dir) / "results" / "RESULTS.md").read_text(encoding="utf-8"))
    except (TamperError, ValueError, FileExistsError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
