# B-Tests — Falsification Diagnostics for OOCC, CAD, and Functional Layers

**Research and critical testing:** Mitchell D. McPhetridge  
**Research examined:** Benjamin Gelhaus's Object-Oriented Cognition and Continuity (OOCC), Continuity–Authority–Directive (CAD), Artificial Tangibility, and Functional Layers  
**Date of initial challenge:** November 15, 2026

## Why this repository exists

Mitchell reports that Benjamin Gelhaus asked him to run diagnostics and develop real test harnesses in the context of their critical exchange. **B-Tests is an independent attempt to falsify and delimit claims, not a project to repair, implement on Ben's behalf, or advocate for OOCC.** The request is described from Mitchell's account; private correspondence has not been independently authenticated here.

Ben's research must be judged against its own **dated, version-specific claims**. A capability explicitly presented as unimplemented, proposed, or unvalidated is not scored as an established operational result. Conversely, a strong claim of real functionality must survive a reproducible test of the actual system, not simply a demonstration with a substitute implementation.

The research question is **not** whether CAD vocabulary can be used to organize arbitrary topics. It is whether **Gelhaus's claimed mechanisms**, as implemented or experimentally demonstrated, produce outcomes that survive adversarial testing and outperform appropriately matched simpler methods where a comparative advantage is claimed.

## Central risk: when the map becomes the authority

The hypothesis under test is that an OOCC continuity map, typed relationship graph, authority record, or high-weight orientation could become **self-reinforcing**: downstream agents might treat an earlier interpretation as governing evidence even when original sources disagree. A related hypothesis is **governance-enforced monism**: CAD's broad categories could be used to force many unrelated phenomena into one explanatory frame, promoting analogy into causality or a proposed common theory into established fact.

These are **possible failure modes to test**, not assertions that Ben's code currently does this, nor judgments about his personality or mental state. Ben's published writing also warns against retrospective overfitting and unproven cross-domain analogies. The test must determine whether the operational workflow respects those warnings.

A good test tries to break both possibilities: a map that genuinely preserves accurate provenance should withstand the challenge; a map that outranks contradictory originals or invents causal links should not.

## Non-negotiable evidence discipline

- **Quote the exact claim and pin its version.** Label it demonstrated, bounded report, proposed mechanism, or explicitly not established. Test only the level actually asserted.
- **Challenge exactly what OOCC claims.** Separate its implemented contracts, historical field reports, proposed extensions, and speculative theoretical generalizations. Test the promised version and scope.
- **Original evidence can overturn orientation.** An approved or canonical object grants documentary/operational authority, not empirical truth; stale maps must not silence current originals.
- **Do not promote relations into causes.** Shared titles, chronology, similar functions, copied summaries, and repeated AI agreement are not independently proven influence or a universal mechanism.
- **Use controls that could beat OOCC.** Compare strong summary-and-search, current-source selection, conventional permissioned ledgers, and generic dependency baselines at matched access and effort.
- **Separate executed tests from proposed ones.** A passing independent CAD-inspired reference implementation tests only that implementation. Documentary consistency tests are not evidence of Ben's native runtime. Missing access means NOT_RUN, not PASS or FAIL.
- **Publish negative results without fixing the target.** Freeze fixtures and scoring; do not tune the tested implementation mid-run and then call the revised result a validation of the original.
- **Record cost.** Source reads, human repairs, map maintenance, reviewer time, latency, CPU, and successful verified deliverables all count.

## The falsification program

| Challenge | Test that could narrow OOCC | Evidence that could strengthen OOCC |
|---|---|---|
| Stale-map authority | A returning worker follows a high-weight map despite a contradictory current original | The worker detects the conflict, cites the original, and does not self-promote a correction |
| Human authorization versus truth | An approved false statement becomes a factual finding | Authorization, source authority, and empirical support remain separately represented |
| Relational reconstruction | Matching concepts are reported as proven historical influence without exposure evidence | Candidate links remain uncertain; false-bridge rates are low on blinded originals |
| Versioned correction | Partial changes overwrite unrelated history or reactivate retired material | Bounded, auditable corrections preserve original provenance and non-affected claims |
| Durable coordination | STORED becomes READ/ACK/COMPLETED without independent recipient evidence | Separate actor-authored, independently checked receipts survive interruption |
| Re-entry advantage | A strong summary/search baseline recovers the same verified deliverables at lower total cost | OOCC improves verified completion or another pre-registered outcome enough to justify overhead |
| Cross-domain Functional Layers | A frozen ontology predicts no better than within-domain or generic dependency baselines | On held-out outcomes, pre-registered forecasts outperform matched baselines without post-hoc remapping |
| Monist overreach | CAD labels or high-weight graph edges are treated as proof of one law across unrelated domains | System explicitly rejects unsupported universality and preserves domain-specific mechanisms |

## What the source record already permits us to say

Gelhaus reports a bounded V3 post-hoc retrieval ablation (November 1, 2026): function-expanded retrieval found 6 directly relevant items in 35 slots, while unconditional graph-hop found 3/35. This is **negative evidence for automatic graph expansion in that setup**, not proof that all relational architecture fails; there was no independent holdout. See *OOCC: The Unified Intersection*, PDF pp. 351–353.

Gelhaus also explicitly classifies fully autonomous cross-session execution, causation from structural graph matches, and controlled comparative recovery benefit as **not established**. Calling these already-proven claims “disproven” would misstate his position. See *OOCC: The Unified Intersection*, PDF pp. 386–390 and *No More First Dates With AI*, pp. 151–153.

We test whether **the actual implementation and subsequent claims** respect those boundaries. Passing a stated limitation in prose is not a software pass.

## How outcomes change the claim

- **EXPAND (conditionally):** A version-pinned implementation passes independently scored, held-out tests and defeats matched baselines on pre-registered measures. Expand only the demonstrated scope.
- **RETAIN (bounded):** A specific implementation behavior is replicated, but no general or comparative advantage is shown.
- **NARROW:** The target fails its declared acceptance criterion, produces unjustified causal claims, or incurs greater total cost without compensating measured benefit.
- **NOT_ESTABLISHED:** Published proposal, inaccessible private implementation, unsupported outcome, or inadequate independent evidence. Neither a victory nor a failure.
- **OUT_OF_SCOPE:** A proposed demand falls outside the version's declared mission. Report separately; do not quietly score it as a product defect.

## Files and results

- [PROTOCOL.md](PROTOCOL.md) — falsifiable cases and evidence tiers.
- [fixtures/reciprocal_development_manifest.json](fixtures/reciprocal_development_manifest.json) — synthetic development fixtures, not sealed independent holdouts.
- [oocc_lab/engine.py](oocc_lab/engine.py) — independently authored CAD-style **control implementation**, not Ben's code and not proof of his software.
- [tests/](tests/) — regression and harness experiments where available.

**Current native OOCC verdict:** No independently executed, version-pinned live OOCC controller result is established by these repository materials. Do not relabel reference-implementation passes as Ben-native acceptance.

## Research position

B-Tests is an attempt to make both critiques answerable to evidence. A relational map might improve discontinuous collaboration. It might only reorganize information a simpler method already handles. Or under some conditions it might harden a provisional interpretation into governing authority. **All three outcomes are admissible.**

The rule is simple: **test the claims, preserve the originals, and let the results either expand or reduce the theory.**
