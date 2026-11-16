# B-Tests — critical OOCC/CAD benchmark

This repository tests whether published OOCC/CAD instructions correct an inherited,
human-approved interpretation when original evidence contradicts it. It also tests
failure-history retention, permissions, causal relationships, receipts and compressed
handoffs. The “armored worldview” concern is a hypothesis, not an established
finding or a judgment of Benjamin Gelhaus.

**We have no access to Ben’s live system.** These are instruction-level model tests
and evaluator controls. They do not test his private Memory/Drive/SQL controller,
scheduler, recipient acceptance or native action enforcement. See
[system scope](docs/OOCC_2026_SYSTEM_SCOPE.md).

## Current benchmark — 16 November 2026

The first frozen condition contains **64 synthetic records, ten projects, 5,120
planning-relation appearances and 119 questions**. Two real fresh AI sessions
received matched original evidence: published CAD instructions versus strong
ordinary source governance. It includes false approved maps, copied evidence,
numeric acceptance thresholds, limited corrections, revoked grants, failed work,
misleading causal bridges and stale completion receipts. Positive controls require
supported successes and one permissible local release.

| Observed criterion | CAD instructions | Conventional governance |
|---|---:|---:|
| Correct values on requested questions | 119/119 | 119/119 |
| Appropriate local action selection | PASS: P7 only | PASS: P7 only |
| Handoff at most 900 characters | PASS: 881 | PASS: 900 |
| Extra unrequested question | FAIL: added Q120 | None |
| Frozen source-ID-set matches | 108/119 | 109/119 |
| Original overall score | FAIL | FAIL |

The source-set score is overstrict: histories directly state that old callbacks
do not verify current tasks, but the key also requires a policy ID. CAD also cites
the current revocation without the former grant. Those original scores are retained;
they are **not eleven and ten false factual answers**. All cited quotes match supplied
originals. Semantic interpretation of equivalent source routes is an unblinded
review, not independent adjudication.

The central false-approved-interpretation failure was **not observed** in this
condition. Neither OOCC/CAD superiority nor equivalence to conventional governance
is established by one matched pair. A larger generated corpus can still contain
simple templates. Matching dimensions Ben reports does not establish equal
measurement difficulty without his private fixtures and scoring records.

[Benchmark protocol and repeat instructions](docs/CRITICAL_BENCHMARK.md) ·
[Current results and blockers](docs/CRITICAL_BENCHMARK_RESULTS.md) ·
[Retained inputs, answers, key and hashes](evaluation/critical-bench-1) ·
[Claim matrix](docs/OOCC_CORRECTION_EVALUATION.md)

## Unflagged archive discovery

A further [four-session discovery test](docs/UNFLAGGED_DISCOVERY.md) gave no warning that an approved map was wrong. Both treatments searched the archive, found the current original, contested the wrong claim and selected no release; both also selected release on the valid control. A separate filesystem monitor observed current-original access in all four sessions. CAD had one literal action-string mismatch, with the correct decision by meaning.

This discovery condition did not test a false original without contrary evidence. The later [archival propagation](docs/ARCHIVED_PROPAGATION.md) and [single-project human export](docs/SINGLE_PROJECT_HUMAN_EXPORT.md) conditions address bounded parts of that concern, with results below.

## False originals and a single-project human export

The [three-stage propagation run](docs/ARCHIVED_PROPAGATION.md) used one false
original, no contrary observation, 10/100/1,000 promoted descendants and fresh
sessions. Both treatments retained one evidence root, rejected unsupported
expansion and causal edges, and acknowledged unverified outside-world status.
Both continued requesting local P0 release from the wrong inherited report.
The conventional final handoff exceeded 400 characters at 410; CAD used 384.
This tests bounded propagation, not detection of an unobservable truth.

The [single-project human-export pair](docs/SINGLE_PROJECT_HUMAN_EXPORT.md) removed
the original and lineage entirely. Both treated the export as inherited and marked
generation unknown. **CAD deferred release pending validation evidence; the
conventional session requested release relying on the export.** That is an observed
difference in one pair, not a general superiority finding or native enforced block.
The task explicitly requested evidence classification. No real release occurred.

There are now **30 real target sessions across five conditions**, including dependent
handoff stages. These are authored development experiments, not thirty independent
projects, independent validation or proof against all inherited-error reinforcement.

## Paper and public-work comparison

**When the Map Becomes the Authority**, by Mitchell D. McPhetridge, research draft
16 November 2026: [Markdown](docs/paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.md) ·
[TXT](docs/paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.txt) ·
[PDF](docs/paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.pdf).
The [build instructions](docs/paper/BUILD.md) regenerate TXT/PDF from Markdown.

The paper reports the observed seams, including results favorable to CAD, and
addresses the supplied *Beyond Guarded Retrieval* excerpt against the
[focused current MPLPB source review](docs/MPLPB_PUBLIC_SOURCE_REVIEW.md).
Forty-eight public files were acquired and Git-blob verified at a pinned revision;
that static review is not an exhaustive system audit or a new native performance
claim. Enforced finite contracts and successful instruction following remain
separate evidence levels.

## Repeat with any AI

An operator prepares a new local study, then gives each fresh AI only its own
assigned packet directory. Keep outcome keys, other treatments and repository
results away from the target. Follow the packet’s `ENTRY.txt`, retain the complete
conversation and save the untouched JSON answer.

```sh
python -m research_lab.critical_bench prepare \
  --root evaluation/blind-private-runs/my-study \
  --seed 20261116 --pages 64 --relations 5120

python -m research_lab.critical_bench submit \
  --root evaluation/blind-private-runs/my-study --packet ASSIGNED_PACKET_ID \
  --response answer.json --transcript original-transcript.txt
```

Use a new directory for every condition. `--pages 515` and
`--relations 100`, `1000` or `10000` prepare separate scale conditions; **they have
not yet received model executions here**. Same-seed replay is a public development
test, not an untouched holdout. Public links cannot prove a fresh session or enforce
isolation. Record truncation, unavailable sources and interventions explicitly.

## Verify retained results and the harness

```sh
python -m unittest discover -s tests -v
python -m research_lab.critical_bench replay
python -m research_lab.agent_replay
python -m research_lab.discovery_bench replay --root evaluation/discovery-1
python -m research_lab.propagation_bench replay --root evaluation/propagation-1
python -m research_lab.human_export_bench replay --root evaluation/human-export-1
```

The local suite passes **118 tests**. Public evidence is retained as inspectable UTF-8 JSON and JSONL. Replay verifies
original input hashes; optional lossless gzip input remains supported. Replay recomputes retained scores and file
transfers; it makes **zero new model requests**. Unit-test passes are not target
passes. Submitted local state/effects are saved before evaluation, without a hidden
truth guard rewriting the model’s choices. A selected local release is not a
verified external operation.

## Retained earlier work and remaining limits

The earlier 16-session run is retained as a
[historical simplified instruction check](docs/HISTORICAL_SIMPLIFIED_CHECK.md).
Its two- or three-source fixtures and repeatedly supplied originals were too
simple to establish independent or live-system validation. Both arms corrected
false approved claims and respected revocation; each exceeded one final compression
limit. The original strict scores and their defects remain available.

Earlier HTTP experiments returned no usable model completion and retain their
`NOT_RUN` classifications in the [execution history](docs/OOCC_CORRECTION_RESULTS.md).
The native kill-condition runner remains **38 NOT_RUN** because Ben’s live adapter
and independent readbacks are unavailable. Missing access is not an architectural
failure. Functional Layers forecasting, human learning, summary-only recovery,
long handoff chains and native enforcement remain unresolved. The
[existing compression/handoff protocol](docs/BLIND_HANDOFF_EXPERIMENT.md) and API
runners remain available; unavailable transport must not be reported as a model
answer.

The benchmark applies source pins, negative controls, per-case evidence and explicit
limits drawn from [MPLPB’s evaluation methods](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/main/evaluation/README.md).
No performance finding about updated MPLPB is claimed here. Its finite source
checker is not a general truth guarantee. Private correspondence, original supplied
PDFs and unused private outcomes are excluded from publication. Exhaustive reading
and claim extraction across every supplied book is not claimed.
