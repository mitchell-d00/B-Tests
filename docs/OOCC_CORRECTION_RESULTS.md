# Execution history and current-result links

Last reviewed: 16 November 2026.

**Current results:** the [false-original propagation](ARCHIVED_PROPAGATION.md) and [single-project human export](SINGLE_PROJECT_HUMAN_EXPORT.md) add eight further target sessions; the [unflagged archive-discovery condition](UNFLAGGED_DISCOVERY.md) has four further target outputs; the [critical benchmark](CRITICAL_BENCHMARK_RESULTS.md) now has two real fresh-agent outputs, and the [historical simplified check](HISTORICAL_SIMPLIFIED_CHECK.md) retains sixteen earlier outputs. The transport failures below remain historical NOT_RUN records; they do not describe all later execution routes. We still have no access to Ben's live system. The untested broader failure mechanisms remain unresolved.

## What actually ran

The earlier local evaluator suite passed **96 tests**. The new blind-handoff
extension brought that revision to **102 passing tests**; the current suite has **118**. These include reference-code
checks, scorer boundaries, oracle non-disclosure, wrong-state persistence,
wrong-effect detection, citation checks, and the distinction between information
loss, honest uncertainty and confidently wrong assertions. These test the
laboratory, not OOCC behavior.

The first published candidate,
[`dffcc38eba7dccf189122e15aef249d1ce377bfb`](https://github.com/mitchell-d00/B-Tests/commit/dffcc38eba7dccf189122e15aef249d1ce377bfb),
passed all **94 then-existing evaluator tests** in GitHub CI. Its
[real-model pilot](https://github.com/mitchell-d00/B-Tests/actions/runs/43788854947)
made one HTTP request for C01/CAD_VERBATIM. The response was HTTP 200 with four
bytes that did not parse as model-response JSON. The runner retained the received
bytes and receipt, stopped additional transport attempts, and marked all **20
planned observations NOT_RUN**. The local correction pilot behaved the same way.
The subsequent two uncertainty tests bring the local suite to 96; they do not
retroactively change that first candidate's 94-test result.

The CI job's failure is the deliberate `--require-live` exit code 2. It is not a
failed CAD criterion, a false claim from a model, or a finding about Ben's
architecture. Complete requests, the raw response and receipts are retained in
the run's `oocc-correction-original-requests-and-results` artifact, ID
`14191238541`, ZIP digest
`f6357f83d99f9b5b8a43f25830571ec7bf1a1c79e93c8ac0a65349970a41d258`.
The [machine-readable summary](../evaluation/oocc-correction-summary.json) includes
result rows reconstructed from the original GitHub job log and labels that
derivation. It is not presented as a downloaded original artifact.

The installed local Codex client also failed initialization because its application
server required writes to a read-only location. It produced no target completion.
No invented or scripted answer is presented as a live model response.

## Other available checks

All ten supplied PDF copies matched their retained hashes. This establishes
local document integrity; it does not verify the empirical studies described in
those papers or certify full semantic reading of all 1,145 pages.

The compression/relationship runner generated and sealed exact input bytes before
dispatch: eight compression budgets, and 10/100/1,000/10,000 candidate relationships
across ten projects. Its local attempt obtained no completion; all **24 planned
records are NOT_RUN**. No cycle-to-first-error, evidence-retention rate, relationship
accuracy or predictive gain is measurable. A functioning endpoint is still needed.

The native OOCC kill-condition runner produced **38 NOT_RUN** records because no
authorized current-system adapter and independent readback were available. This
is missing access, not 38 architectural failures. A simulated stop, a model
selecting no action, and a native guard rejecting an operation remain distinct.

## Correct system and chronology

The [newer reported cloud workflow](OOCC_2026_SYSTEM_SCOPE.md) uses Memory routing,
current Drive documents, a SQL working index, communication records and scheduled
jobs. The supplied correspondence describes controller-like operation without
requiring the unfinished mobile application. Its operation has not been
independently examined here. The instruction packets are not claimed to reproduce
that entire environment or inherit its actual current authority state.

The newest *Beyond Guarded Retrieval* material available here is the user's excerpt
from pages 14–16. The E0–E5 reproduction packages, private raw-source maps, and full
newest paper were not supplied. The earlier V3 negative graph-hop result remains
**reported historical evidence**, not a rerun. Later outcomes cannot be assigned
to another version. The inspected updated MPLPB revision and portable/residual
experiments are methodology references; no performance finding about the updated
MPLPB implementation is included.

## What would change the conclusion

Actual fresh-session outputs could support or weaken the hypothesis. A useful
positive outcome must correct successor state, preserve original and contradictory
evidence, retain relevant failures and rejected relations, and select permissible
actions. The authorized-release control must also succeed. Failures must be tied
to the exact packet, fixture and model.

Repeated trials, independently authored holdouts, blind semantic review and measured
human cost remain necessary for comparative claims. Ben's live cloud system also
requires authorized current snapshots and independent source, state, recipient and
scheduler readbacks. Missing access cannot establish whether that system corrects
or reinforces an inherited interpretation.

## Added blind handoff experiment

The [blind-handoff protocol](BLIND_HANDOFF_EXPERIMENT.md) adds seven synthetic
case families, two matched treatments, and four stages per chain. A target sees
only its current task and treatment. The next packet receives the model's actual
handoff text, not a replacement summary or a hidden structured answer. Source
reads are logged and later-stage corrections are unavailable early.

Executed evaluator controls detected 126 of 126 planted faults, independently
reopened 56 submitted states, and checked 42 actual handoff transfers. These
scripted results validate the harness; they are not target-model observations.
The API attempt made one HTTP request, received no usable model completion, and
recorded 56 NOT_RUN stages. This creates no finding for or against OOCC.

Specific blockers: the configured endpoint returns non-model data despite HTTP
200; the installed alternative client fails initialization on a read-only
filesystem, including after a scoped write-permission attempt; Ben's live
Directory, Memory, SQL state and independent execution readbacks are inaccessible.
The exact failing write path was not established. No missing-access condition
is classified as an architecture failure.

Two answer-hidden entry packets are prepared for manual fresh-chat use. Their
original source bytes are supplied separately from instructions; private outcome
keys and future corrections are not exported. These are development packets,
not independently authored holdouts. A public URL cannot prevent external
browsing, verify identity, erase account Memory, or establish a blind session.
Those limits remain part of the report.
