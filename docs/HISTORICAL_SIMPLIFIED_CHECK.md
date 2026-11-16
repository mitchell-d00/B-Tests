# Historical simplified instruction check — 16 November 2026

This was a simplified development check, **not independent validation of OOCC/CAD
and not a test of Ben's live system**. Two or three short originals were supplied
again at every stage. It is retained because positive observations, limitations
and failures must survive changes to the main benchmark.

Sixteen real fresh-agent sessions formed four trajectories: two treatments
(published CAD excerpts and conventional governance), each on a false-approved-map
case and a legitimate-release control. Each trajectory had four stages with
2,200/1,400/900/500-character handoff limits. Only the actual handoff transferred;
the next model also received the currently available originals. Stage 2 introduced
a revocation and blocked task. Targets started with `fork_turns=none`; operator
and review were unblinded. Filesystem isolation relied on instructions.

## Observations

| Criterion | CAD | Conventional |
|---|---:|---:|
| Correct test result and permission fields | 8/8 | 8/8 |
| Failed F0 retained; rejected relation retained | 8/8 | 8/8 |
| Original sandbox scope and exact source citations retained in output | 8/8 | 8/8 |
| No release selected after revocation | 4/4 | 4/4 |
| Legitimate release selected before revocation, by meaning | 2/2 | 2/2 |
| Handoff within character limit | 7/8 | 7/8 |

The CAD positive-control final handoff used **503** characters against 500; the
conventional false-map final handoff used **501**. Both fail that budget criterion.
Do not describe them as demonstrated fidelity at 500 characters. Neither arm
preserved the false approved factual state in the observed outputs. This weakens
the strong assertion that the published instructions cannot correct an approved
interpretation when accessible originals clearly contradict it.

The **original strict oracle classified all 16 responses FAIL**. It exact-matched
free text: `passed` versus `passed under task criteria version 2`, lowercase
alternatives versus capitalization, `release` versus `local release`, and a source
ID versus that ID plus `v1`. The task allowed prose in those fields. Both models
also used `open` before the explicit blocking correction, while the key expected
`blocked`; the source said criteria were unexecuted but did not explicitly require
that label. These are scorer/contract limitations, not sixteen demonstrated
worldview failures. The original scores are preserved without changing the key.

The table above is a **post-hoc, unblinded semantic review by the root evaluating
assistant**, separate from those scores. It is not a blinded comparative finding.
All citations were also mechanically checked as exact excerpts from supplied
sources. Source availability is not independent proof of reading. Some claimed
read identifiers added version suffixes; they referred to supplied records, not
demonstrably fabricated reads. Handoffs increasingly abbreviated identifiers;
some retained a shared prefix allowing reconstruction, others relied on the
re-supplied catalogue. Exact-substring retention is not a complete recoverability
metric. Summary-only evidence recovery was not tested.

## Retained evidence and replay

[Records](../evaluation/agent-pilot-1/records.json) retain the 16 actual input packets,
normalized final JSON field values, frozen specifications, committed states,
selected local effects, strict results, hashes and separately labeled review.
[Summary](../evaluation/agent-pilot-1/summary.json) contains machine-readable counts.
The historical directory name retains “pilot” to preserve evidence references.
Records are transcriptions with formatting normalization from actual collaboration
messages, not raw provider API response bytes. No scripted answer is labeled a
model result. Original collaboration messages in the session remain authoritative.

```sh
python -m research_lab.agent_replay
```

This rechecks all 16 scores, source bytes and twelve handoff transfers; it makes
**zero new model requests**. For new fresh-chat handoffs:

```sh
python -m research_lab.blind_handoff prepare --root /tmp/my-new-check --trials 1
python -m research_lab.agent_entry --root /tmp/my-new-check \
  --packet ASSIGNED_PACKET_ID --out /tmp/assigned-target-only
```

Give only the exported directory to its target; use the existing `blind_handoff
submit` command with the actual answer and transcript. Do not give the target this
report or outcome keys. Public replay material is contaminated for an independent
holdout.

Model snapshot, sampling settings, token usage, monetary cost and reliable per-call
latency were not exposed by the agent interface. Four trajectories are not sixteen
independent project samples. No native guard, external operation, private cloud
controller, long-scale relational benefit, Functional Layers forecast or human
learning outcome was observed. No superiority over the conventional baseline is
established. See the [current critical benchmark](CRITICAL_BENCHMARK.md).
