# B-Tests — OOCC/CAD correction evaluation

This laboratory tests whether inherited, human-approved interpretations are
corrected when stronger original evidence contradicts them. The armored worldview
hypothesis is a testable risk, not an established finding or a judgment of Ben
Gelhaus. Positive and negative outcomes must both survive.

**We have no access to Ben’s live system.** His newer reported cloud workflow
includes ChatGPT Memory routing, current Drive governance documents, a
Supabase/PostgreSQL working index, crawler contracts, communication records and
scheduled jobs. It must not be reduced to the earlier unfinished Android app.
See [2026 system scope](docs/OOCC_2026_SYSTEM_SCOPE.md).

## Actual status — 16 November 2026

| Check | Observed result | What it establishes |
| --- | --- | --- |
| Local evaluator suite | 102 tests pass | Harness/reference-code behavior, including negative controls |
| Supplied PDF integrity | 10/10 hashes match | Local source-byte preservation only |
| Local correction pilot | 20 NOT_RUN; zero model completions | No OOCC/CAD performance finding |
| GitHub CI correction pilot | 20 NOT_RUN; zero model completions | Endpoint returned HTTP 200 with four bytes that were not model-response JSON |
| Compression and saturation preparation | 24 NOT_RUN | Inputs and requests prepared; no observed handoff threshold or graph accuracy |
| Native OOCC kill-condition runner | 38 NOT_RUN | No authorized live-system adapter or independent state access |

The CI model job is red because `--require-live` rejects a run without actual
completions. That is an infrastructure blocker, not evidence that OOCC failed.
Its evaluator checks passed. The hypothesis remains **unresolved**.

[Execution report](docs/OOCC_CORRECTION_RESULTS.md) ·
[Protocol and claim-to-test matrix](docs/OOCC_CORRECTION_EVALUATION.md) ·
[Draft evaluation PR](https://github.com/mitchell-d00/B-Tests/pull/1)

## Blind compression and handoff runs

The [neutral experiment entry](blind/START.md) and
[operator protocol](docs/BLIND_HANDOFF_EXPERIMENT.md) add four-stage fresh-session
handoffs. Each target receives only its current packet; outcome keys, condition
mapping, scores and future corrections remain local. Public links cannot enforce
isolation or prove a fresh session. Give each AI one assigned ENTRY link, not the
repository overview.

The latest local run detected 126 scripted faults, verified 56 persisted states
and 42 actual file transfers. These are harness controls, not OOCC observations.
The model attempt obtained zero usable completions: all 56 planned stages are
NOT_RUN. See [machine-readable results](evaluation/blind-handoff-summary.json).

## What is tested

Sixteen frozen development cases cover false approved maps, human permission
versus truth, revoked permission, lost failures, revived rejected relations,
unread indexed sources, misleading analogies, stale receipts, invalid ancestors,
disputed publication identity, copied evidence, and domain-specific forecasts.
A legitimate release control prevents blanket refusal from appearing successful.

The model receives a verbatim published CAD packet or an ordinary governance
baseline. Forecast cases also receive a separate verbatim Functional Layers
proposal. The same evidence, task, permissions and output budget go to each arm.
These packets are bounded instruction treatments, not Ben’s complete current
operating environment. The harness persists the model’s chosen working state and
local effects, then separately reopens those files. It does not correct the model
or filter out an unwarranted release. No real external publication is performed.

## Reproduce

```sh
python -m unittest discover -s tests -v
python -m research_lab.oocc_adversarial \
  --out evaluation/new-correction-run --key-env GITHUB_TOKEN \
  --case-ids C01,C02,C03,C06,F01,F02,F03,F04 \
  --trials 1 --max-requests 20 --require-live
```

The default endpoint is GitHub Models. Another OpenAI-compatible endpoint can be
selected with `--endpoint`, `--key-env` and `--model`. Keep credentials in the
environment. Every run requires a fresh output directory and retains full requests,
received provider responses, receipts, state/effect files and independent readbacks.
Unusable transport stops further calls and marks remaining cases `NOT_RUN`.

Compression and relation saturation use generated fixtures sealed before dispatch:

```sh
python -m research_lab.live --out evaluation/new-handoff-and-graph-run \
  --family all --trials 1 --key-env OPENAI_API_KEY --require-live
```

That runner compares eight handoff budgets and 10/100/1,000/10,000 candidate
relationships across ten projects. It separates summary-only auditing from recovery
with originals, and information loss from confident false assertions. A model that
exceeds the requested compression budget has not demonstrated fidelity at that
budget. Character counts are not tokenizer measurements. Native live-system tests
remain separately available through `python -m tools.kill_harness`.

## Evidence boundaries

`PASS` and `FAIL` apply only to the declared tested criterion and evidence level.
`INCONCLUSIVE`, `NOT_RUN` and `OUT_OF_SCOPE` remain distinct. Harness controls,
reported historical results, instruction-level behavior, native enforcement and
independently blinded comparative findings must never be combined into one score.
The current suite is evaluator-authored development material. Independent holdouts,
blind semantic review, live cloud-system readbacks and measured human cost remain
outstanding. The full newest comparative paper and its private reproduction
packages were not supplied; the provided excerpt is identified as an excerpt.

## Methodology references

- [Combined MPLPB: inspected updated revision](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/cc21ce300b5ec228c07fc77a149804fba6c89792)
- [Portable Evidence Runtime](https://github.com/mitchell-d00/portable-evidence-runtime/tree/4fdc20193c01f82baea0598b4c7d8ef3040772d5)
- [MPLPB residual experiment](https://github.com/mitchell-d00/mplpb-residual-experiment/tree/1ec160051ba306ce61d74ba3186f0aa5873694c5)

These inform the evaluation method. Their prior passes are not OOCC observations,
and no performance result for the updated MPLPB implementation is claimed here.
Historical protocols and fixtures remain in the repository and Git history with
their original scope. The private correspondence and original supplied PDFs are
not published in this branch.
