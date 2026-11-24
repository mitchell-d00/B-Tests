# Probabilistic Polite Compliance — live replication, 24 November 2026

This archive records a fresh local inference run of Mitchell D. McPhetridge’s v0.2 protocol. It retains both original companion packages, frozen cases, exact requests, raw response envelopes, independent rescoring, fixture controls and a separate native MPLPB execution. [Reproduction](REPRODUCTION.md) · [Mox Cult of Personality (MoxCOP)](moxcop/README.md)

## Live A/B/C results

Qwen2.5-1.5B-Instruct Q4_K_M ran locally through llama.cpp b12622. Each arm covers the same seven case families, with 210 supported and 210 unsupported decision opportunities per arm. There were 30 repeats of 14 frozen cases.

| Treatment | Correct accepts | False refusals | Correct refusals | False accepts | Invalid |
| --- | ---: | ---: | ---: | ---: | ---: |
| A — baseline model | 97 | 19 | 124 | 11 | 169 |
| B — corrective instructions | 92 | 118 | 209 | 1 | 0 |
| C — B output plus deterministic gate | 92 | 118 | 210 | 0 | 0 |

B authorized one unsupported execution claim. C refused that same proposal and left the other 419 valid B decisions unchanged. B and C returned 118 false refusals out of 210 supported opportunities (56.2%). B produced fewer strict unsupported accepts than A and yielded valid structured decisions on all cases. A’s 169 invalid responses included 94 supported and 75 unsupported opportunities, so a comparison of valid refusals alone would omit those cases. [Machine-readable scores](scored/summary.json)

An exploratory format check could parse 133 of A’s invalid outputs by removing a single Markdown fence. Those parsed decisions included 18 unsupported accepts. This diagnostic was added after the live run started and leaves primary scoring unchanged. The gate uses the frozen evaluator eligibility label. The result measures a bounded enforcement property for this decision interface, with external truth detection and free-text fidelity outside its scope.

## What establishes separate trials

There were 420 A histories and 420 B histories. Every history was rebuilt from the treatment’s system prompt and the assigned case. The client used no thread or conversation ID. In 180 histories per arm, the first user turn requested a correction acknowledgment. Its actual reply was carried forward only in that history. The scorer reconstructed all messages, verified the raw HTTP response envelopes, and found 1,200 unique provider response IDs with no transport errors (840 decision responses and 360 correction responses). C used the exact B output, with no extra inference. The shared model server establishes the scope of this result at the client request and context levels. Statistical independence of repeated observations remains unestablished. [Frozen schedule](live/frozen.json) · [Raw responses](live/trials.jsonl.gz) · [Runtime details](runtime.json)

The supplied v0.2 30-repeat experiment replayed authored fixtures. The older B-Tests governance-prompt study recorded 30 fresh target sessions with procedural separation and dependent handoff stages, and retained normalized outputs. Provider receipts for those older sessions are unavailable. This run supplies direct request-level evidence for the PPC replication. [MoxCOP verification method and older-study scope](moxcop/README.md)

## Correction review

The study assistant reviewed a packet of 36 correction replies with treatment and later outcome fields withheld. Thirty-one indicated acknowledgment without describing the rule and five lacked acknowledgment. Zero replies explicitly restated the rule. The single B false accept occurred on a case without a correction exchange, so the trial leaves open whether an explicit acknowledgment can be followed by such an authorization. Independent human review remains pending. [Rubric](CORRECTION_REVIEW.md) · [Sample](correction-review/packet.json) · [Review counts](correction-review/summary.json)

## Native and fixture runs

The native check ran all seven B-Tests probes at B-Tests e646f82 against Combined MPLPB e3990bf. All seven passed. The supported control invoked its local adapter and wrote the marker. The other cases produced no marker. Post-process SQLite checks matched the retained event counts. The same checks passed from the extracted offline checkout. These native B-Tests probes cover related work boundaries. PPC treatment C used the companion gate. Native OOCC was NOT_RUN. [Native summary](native/summary.json) · [Offline native confirmation](native/offline-extracted-summary.json)

The original v0.2 companion passed five unit tests. Its 30-repeat fixture replay and 11,192-check stress run were repeated as software controls, without any additional model observations. The original ZIPs and paper copies are preserved byte for byte. [Fixture results](fixture) · [Original packages](original)

MoxCOP was also exercised in a separate live smoke test using one-turn and two-turn trial definitions. It verified all four planned trials and six unique responses. [Tool and exact usage](moxcop/README.md) · [Smoke verification](moxcop/example-run/verification.json)
