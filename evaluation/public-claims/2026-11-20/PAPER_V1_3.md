# Testing OOCC v1.3 — M6 attribution correction

20 November 2026. Documentation-only correction to main revision
`109299c52bc92ce66e783a453c521a1e9c53db1a`.

- M6 is described as an additional component Gelhaus adds, attributed to
  McPhetridge's clarification; it is absent from the supplied public ZIP.
- The incorrect phrase “McPhetridge's private M6” is withdrawn. An erratum and
  archive notice identify the error; the first response did not make that claim.
- Newly supplied response.pdf matches the already archived field-access response
  byte-for-byte. Exact SHA-256 and PDF pages 2/7 are recorded in the audit and P4.
- MPLPB and B-Tests authorship remains McPhetridge's. No private M6 implementation,
  performance or precise execution role was independently inspected or verified.
- Version 1.2 formats/manifest are preserved unchanged; current MD/TXT/PDF,
  README, navigation, catalogue metadata, attribution audit and ZIP are updated.
- Existing raw experiments, frozen results and engine/test implementations are
  unchanged. No native, model or new semantic experiment was run for this erratum.

Artifact checks (exit 0):

```
python -m tools.verify_oocc_claim_roadmap
python -m tools.build_critical_paper --paper testing-oocc --check
git diff --check
```

Current PDF correction page visually inspected. Source attachment and archived
first-response SHA-256 equality verified. No new software regression claim is made
for this documentation-only correction; previous 130-test results retain their
own revision and verification record.
