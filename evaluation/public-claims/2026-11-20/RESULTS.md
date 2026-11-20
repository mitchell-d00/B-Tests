# Testing OOCC — new claim probes, 20 November 2026

This is an authored development study, not independent validation. Native OOCC and
new model instruction comparisons are **NOT_RUN**. No fabricated model responses
or private-controller substitutes are included. The prior B-Tests unit baseline
was123 tests passed at7771497; those are software checks, not123 OOCC trials.

## What is compared with what

| ID | Actual left arm | Actual right arm | Observation and limit |
|---|---|---|---|
| C1 |512 sampled decimal powers of ten|Equivalent Python exponentiation expressions|512 shorter expressions; ASCII bytes and integer equality, not model tokens or computed Kolmogorov complexity. Structured number family, not a representative number population.|
| C2 |Expanded strings at4 referent lengths and5 reuse counts|Serialized dictionary plus handle uses|15 of20 indexed encodings cheaper,5 more expensive; one specified encoding, not a universal efficiency result.|
| C3 |B-Tests' own CADLab handle resolver|Its current source/query and grant checks|4/4 controls met; explicitly evaluator-owned, not Gelhaus's implementation.|
| C4 |Seven requests through actual MPLPB61cc7c0|Read-only SQLite event counts and local adapter effect file|7/7 native criteria met, including a real allowed control; no live OOCC head-to-head or real-world completion claim.|
| C5 |Selected CAD physical pages3,4,7 with a fresh model|Strong conventional source-governance instructions, same base model and task|Prepared source-complete packets only; NOT_RUN. Instructions differ in length; no model identity, latency or accuracy measured.|
| C6 |Gelhaus's actual native controller|Native MPLPB on matched operations|NOT_RUN: no runnable authorized controller/adapters/readbacks available. No zero score assigned.|

[Machine-readable comparison matrix](comparisons.json) records the unit, actual
implementation and excluded inference for every arm. [Observed results](observed/summary.json)
are not pooled into one OOCC success rate. The source inventory identifies the ten
supplied papers; their private experiments are reported by those sources, not
newly executed here. `cad-passages.json` preserves the selected original text and
PDF hash; it is test stimulus, not governing instructions for this repository.

## Execution pins and artifacts

The producer is retained as `producer.py`; its SHA-256 equals the pre-execution
`observed/freeze.json` record. Base B-Tests ancestry7771497 is not falsely described
as containing the new uncommitted producer. Native MPLPB is exactly
61cc7c04ebdfa84c8d783e005c6e7857c07600b2, with tracked files checked clean before
and after. The existing `research_lab.mplpb_seam_probe` adapter is reused without
altering target code or its seven cases.

Final run:1.549s wall,0.042s parent CPU,16,121,856-byte peak parent RSS. Parent metrics
exclude native subprocess CPU and maximum RSS; those totals remain unmeasured.
Model calls0; independent semantic/human assessment NOT_RUN; model quality,
relationship accuracy and human-review time null. This run does not reproduce the
entire MPLPB regression suite or its historical benchmark. Their retained reports
keep their own revisions and denominators.

`observed/native/` contains actual worker results, stdout/stderr and local effect
artifacts. `observed/reference.sqlite` is a synthetic evaluator-owned database.
`observed/analytical.json` contains every sampled exponent and encoding count.
`observed/sha256.json` pins the observed artifacts. No failure or timeout was
removed from the completed denominator.

## Repeat

From B-Tests and a clean MPLPB checkout at61cc7c0, use NEW paths:

```sh
python -m research_lab.public_claims comparisons
python -m research_lab.public_claims run --out /tmp/new-public-claims --mplpb-root /path/to/pinned/mplpb
python -m research_lab.public_claims prepare-model --out /tmp/new-instruction-packets --cad-source evaluation/public-claims/2026-11-20/cad-passages.json
python -m research_lab.public_claims score-model --root /tmp/new-instruction-packets --responses /tmp/operator-supplied-responses --output /tmp/new-instruction-score.json
python -m unittest discover -s tests -q
python -m tools.build_critical_paper --paper testing-oocc --check
```

Only give a future model its assigned `packets/ID/request.json`; keep custody,
assignments and expected values out of its inputs. Use identical model settings
and record actual provider outputs. Missing responses remain NOT_RUN, never zero
accuracy. The response scorer checks typed values and required exact source spans;
it does not certify model identity, fresh-session isolation, external effects or
unrestricted semantic reasoning. These public developer keys are not an unseen
holdout. Unit fixtures exercising the scorer are not model executions.

## Earlier evidence and duplicate handling

The newly supplied witness ZIP is byte-identical to
`evaluation/witness-section19/supplied/witness-section19-experiments.zip`.
The switch-test Markdown matches the existing paper. The supplied map-response
PDF differs and is separately retained in the paper archive. [Prior-material map](prior-materials.json)
records exact source paths and hashes. [The existing audit](../../witness-section19/RESULTS.md)
distinguishes the authored test-design scaffold from live CAD or native MPLPB
results, and identifies which filesystem/native runs were actually observed. The
author clarified on20November that the ZIP was his structure for thinking through
how to test both systems; it is credited as design, not treated as a failed native
experiment. The dated author-intent note preserves that context alongside the
unchanged historical ZIP. Repeated files and reruns do not add independent sample size.

[Paper MD](../../../docs/paper/TESTING_OOCC.md) · [TXT](../../../docs/paper/TESTING_OOCC.txt)
· [PDF](../../../docs/paper/TESTING_OOCC.pdf) · [Mitchell paper archive](../../../docs/papers/archive/README.md)


## Harness validation and retained initial variant

The full B-Tests software suite passes130 tests (exit0), compared with123 before
these additions. The extra-field negative control first failed: a response with
correct finite answers plus an unrequested claim could receive a perfect fact
score. The strict response-contract parser now rejects extra fields, duplicate
JSON fields, non-finite constants and responses over1,000,000bytes. This is a
general schema repair, not a change to expected case answers or a new model run.
Initial artifacts/producer are retained under `observed-initial`,
`producer-initial.py` and `prepared-instructions-initial`; final versions are
separate. C1–C4 conclusions are unchanged. No model responses were generated.
The initial and final replay are not pooled as additional independent cases.
