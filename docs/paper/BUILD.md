# Paper formats and reproduction

Canonical text: [Markdown](WHEN_THE_MAP_BECOMES_THE_AUTHORITY.md). Generated
[plain text](WHEN_THE_MAP_BECOMES_THE_AUTHORITY.txt) and
[PDF](WHEN_THE_MAP_BECOMES_THE_AUTHORITY.pdf) contain the same paper.
These are a research draft, not peer-reviewed validation. Link destinations are
printed in TXT/PDF so they remain recoverable outside Markdown. The legacy
filename is retained for links; the current title is MPLPB and OOCC/CAD:
Comparative Experiments.

Experiment execution and result replay use only Python's standard library.
Regenerating document formats additionally requires `pandoc`, DejaVu fonts and
`reportlab==4.4.9`:

```sh
python -m pip install reportlab==4.4.9
python tools/build_critical_paper.py
python tools/build_critical_paper.py --check
```

Generate and verify the separate [MPLPB Mixed Dump manuscript](MPLPB_MIXED_DUMP.md)
with the same renderer:

```sh
python tools/build_critical_paper.py --paper mixed-dump
python tools/build_critical_paper.py --paper mixed-dump --check
```

Generate and verify [Probabilistic Prompts and MPLPB Deterministic Contracts](PROBABILISTIC_PROMPTS_AND_MPLPB_CONTRACTS.md):

```sh
python tools/build_critical_paper.py --paper switch-test
python tools/build_critical_paper.py --paper switch-test --check
```

Install pandoc/DejaVu through the host's package manager if absent. The build uses
fixed PDF metadata for repeatability; a different renderer/font version may change
PDF bytes. Do not infer different research findings from that formatting difference.
Original supplied PDFs and private correspondence are not included.
