# Executed checks and unresolved target results

Last reviewed: 16 November 2026.

**No OOCC/CAD success or failure has been established by this pilot.** Local and
GitHub model transports returned no usable model completion. We have no access
to Ben's live system. The armored worldview hypothesis remains unresolved.

## What actually ran

The final local evaluator suite passed **96 tests**. These include reference-code
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
