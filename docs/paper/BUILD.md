# Paper formats and reproduction

Canonical text: [Markdown](WHEN_THE_MAP_BECOMES_THE_AUTHORITY.md). Generated
[plain text](WHEN_THE_MAP_BECOMES_THE_AUTHORITY.txt) and
[PDF](WHEN_THE_MAP_BECOMES_THE_AUTHORITY.pdf) contain the same paper.
These are a research draft, not peer-reviewed validation.

Experiment execution and result replay use only Python's standard library.
Regenerating document formats additionally requires `pandoc`, DejaVu fonts and
`reportlab==4.4.9`:

```sh
python -m pip install reportlab==4.4.9
python tools/build_critical_paper.py
python tools/build_critical_paper.py --check
```

Install pandoc/DejaVu through the host's package manager if absent. The build uses
fixed PDF metadata for repeatability; a different renderer/font version may change
PDF bytes. Do not infer different research findings from that formatting difference.
Original supplied PDFs and private correspondence are not included.
