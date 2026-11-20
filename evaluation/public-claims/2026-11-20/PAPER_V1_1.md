# Testing OOCC v1.1 — paper revision and verification record

20 November 2026. Author: Mitchell D. McPhetridge. Prior published branch revision:
`44cda23fd35216684e6f39932db7fcf5ff49ef3d`.

This iteration rewrites the paper, not either target engine. It adds 34 attributed
claim/test families, individual comparisons, challenge cases, outcome measurements,
access prerequisites, proposal credit and McPhetridge's engineering recommendations.
The tests are a roadmap: not 34 executed experiments or 34 demonstrated failures.
Claims are paraphrases with physical PDF pages, not fabricated quotations.

Several experimental designs originate in Gelhaus's publications, including the
role-enactment factorial design, weight ablations, forged-authority/revocation
checks and prospective Functional Layers baselines. The revision credits these
and recommends their execution/publication rather than claiming their invention.

The first edition's MD/TXT/PDF and manifest are preserved unchanged in
`docs/papers/archive/testing-oocc-v1.0/`. The archive now indexes 14 editions and
37 format entries. Three previously documented acquisition gaps remain gaps.
The original witness ZIP, prior papers, frozen experimental observations and
all native/model result files are unchanged. No new native OOCC or model trials
were run. Native OOCC, fresh model trials and independent human assessment remain
NOT_RUN; unknown performance metrics remain null.

## Reproducible checks

From B-Tests, with the recorded renderer environment in the paper manifest:

```
python -m tools.verify_oocc_claim_roadmap
python -m tools.build_critical_paper --paper testing-oocc --check
python -m unittest discover -s tests -q
pdfinfo docs/paper/TESTING_OOCC.pdf
```

Observed outcomes, all exit 0:

- Structural checker: 34 unique ordered test IDs in the JSON catalogue and both
  Markdown copies; valid source IDs/page bounds; NOT_RUN/null labels; matching
  current/archive hashes; first edition preserved. This checks consistency,
  not the correctness of the paraphrases against the supplied PDF wording.
- Renderer check: TXT and PDF match current canonical Markdown under the pinned
  renderer environment. PDF is 21 pages, author Mitchell D. McPhetridge, subtitle
  “Claims, Required Tests, and a Roadmap to Verified Behavior.” Fixed PDF metadata
  dates are intentional deterministic-renderer values, not experimental dates.
- B-Tests software regression: 130 tests passed. These are software checks, not
  independent validation of Gelhaus's work or historical semantics.
- Representative first, roadmap and final PDF pages were visually inspected.
- Changed-file inspection against `44cda23` confirms original frozen observation
  directories, witness results and public-claims runtime/tests were not modified.

During document assembly, an overly broad numeric replacement introduced a
repeated test heading and altered a copied ZIP hash. Consistency review caught
both before publication; headings and the original hash were restored. These were
editorial errors, not new observed system outcomes; no experimental result was
changed or scored through them. Final checks above verify the corrected artifacts.

## Scope and remaining work

No controlled superiority, native OOCC failure count, learning benefit, independent
semantic accuracy or universal safety guarantee is asserted. Proposed tests need
their specified implementation, access, participants and/or observers. The catalogue
covers identified families in the reviewed sections, not every sentence of every
supplied book. Existing C1–C4 observations retain their original, separate units;
C5/C6 remain unexecuted. MPLPB's incomplete historical answers remain visible.
