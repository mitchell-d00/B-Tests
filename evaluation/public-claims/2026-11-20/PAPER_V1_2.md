# Testing OOCC v1.2 — checkpoint status and machinery attribution

20 November 2026. Author: Mitchell D. McPhetridge. Previous edition commit:
`8ce1bfbb74c37d4d9516a14db5e19faa2804b41d`.

The author requested a replacement edition making clear that a described test is
not a supplied runnable test or an independently reproduced result. The amendment:

- Labels unavailable OOCC checkpoint outcomes AUTHOR_REPORTED /
  NOT_INDEPENDENTLY_REPRODUCED_HERE; a publication is not execution verification.
- Keeps G9's CP050/predecessor archive totals distinct from its CP045 verifier.
- Marks the discussion's specific HLC CP014 account as not located in reviewed
  extracted text, rather than adopting it as verified or claiming it never existed.
- Explicitly attributes MPLPB, its writer, strict pipeline and pre-existing native
  tests to McPhetridge; Gelhaus's benchmark framing, test selection and reporting
  are not authorship of the engine or automated test machinery. Inclusion of a
  script in his package does not establish that he authored a separate driver.
- Inspects the supplied public package code rather than inferring a private harness.
  `reproduce.py` imports upstream `answer_query`, `write` and `PROFILES`; the package
  does not supply M6 or a B-Tests implementation. No use of private M6 is established.
- Preserves v1.1 and v1.0 formats/manifests unchanged. No original experimental
  outputs, engine implementation, public-claims test code or frozen benchmark is
  altered. The roadmap remains 34 proposed families, not 34 demonstrated defects.

The new ZIP supplied at attachment path ending
`DC90D431-B7C6-42EC-9C10-4FBE86760546/1-Ben-MPLPB_Oct2026_Publication_Package.zip`
is byte-identical to the earlier attachment. SHA-256:
`f4d1c8263dbb8dcf9f7ddbc9fc85be5d005864db4c74fce1a93cda1bb4865718`.
Actual package inspection verified 59/59 manifest entries; AST inspection identified
the imported upstream APIs. These are file-integrity and code-provenance checks,
not a new native engine benchmark. Exact package/script hashes and imports are
in `attribution-audit.json`. The G12 bibliography entry cites the public package.

Validation commands (all exit 0):

```
python -m tools.verify_oocc_claim_roadmap
python -m tools.build_critical_paper --paper testing-oocc --check
python -m unittest discover -s tests -q
git diff --check
```

Observed: 34-family artifact consistency check passed; deterministic TXT/PDF check
passed; 130 software tests passed; representative amendment/PDF pages visually
inspected. These do not certify semantic accuracy. Checkpoint verifier/native
OOCC/model/human trials remain NOT_RUN. Prior native CI results are attached to
their own exact revision; new CI results must be read at the latest PR head.

An initial attribution draft credited wrapper authorship to Gelhaus without a
source history establishing it. The author challenged that inference; it was
removed before this replacement edition was published. Code imports prove what
machinery is called, not who authored every line of the packaged script.
