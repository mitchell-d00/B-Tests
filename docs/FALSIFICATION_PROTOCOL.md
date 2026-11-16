# When the map becomes the authority: the B-Tests kill program

**Mitchell D. McPhetridge — 15 November 2026**

This protocol tests dated claims and mechanisms of OOCC, CAD, Artificial Tangibility and Functional Layers. It examines whether errors persist, unsupported relationships gain authority, and compression loses necessary evidence. These are test conditions, not a predetermined outcome. Current scope and terminology updated 16 November 2026; historical versions remain in Git history.

## Three error-propagation mechanisms

1. **Authority inversion:** The historical map, salience weight, or human approval is treated as stronger factual evidence than an eligible current original. Counterexample: a new source states port 6200, orientation still states 6100.
2. **Unsupported relationship inference:** Ten projects, hundreds of candidate bridges, copied root evidence, and repeated model agreement are treated as independent proof of one cause. Correct behavior keeps exploratory connections provisional, bounds the active graph, and rejects false causal bridges.
3. **Compression-smoothing:** A summarized reason is lost but its conclusion survives; a failed read is omitted but a later artifact remains; a rejected hypothesis is dropped but its causal edge becomes active again; or a fresh model confidently reconstructs missing original evidence from context. Correct behavior preserves linkable negative evidence or explicitly downgrades claims and stops the affected action.

## Evidence and kill rules

- **Native pass** requires a pinned actual build, the original or isolated authorized test source, its response, and an independent readback for every mutating or permission-sensitive case. A response saying `blocked` cannot prove a blocked effect. The verifier must not be controlled by the same untrusted output lane.
- **Native failure** requires the preregistered oracle to reject that pinned implementation on its authorized task. Save the response, evidence pin, and verifier transcript. A private system with no adapter is `NOT_RUN`, not `FAIL`.
- **Study outcome** must compare equal access, time/model budgets and total human/tool cost. Scoring never certifies independence. A stronger explanation or higher graph count is not a measured advantage.
- **Scope limits:** CAD explicitly says it does not guarantee factual correctness or enforce access control alone (CAD PDF p. 7). Functional Layers explicitly says cross-domain causal forecasting is not independently validated (Unified Intersection pp. 38-41). Testing that a feature is not installed is not falsifying a claim that it already exists.

## Source anchors

- *CAD Control Grammar*, PDF pp. 3–7: source/authority/directive distinction, explicit stop and its seven evaluation criteria.
- *Artificial Tangibility as a Low-Infrastructure Governance Layer*, pp. 4–6: existence is not promotion, human promotion gates, object salience and bounded scope.
- *No More First Dates With AI*, pp. 151–153: the risk of retrospective coherent explanation and the proposed fresh-runtime baseline/ablation; pp. 267–271: 15 acceptance cases that must fail when wrong.
- *OOCC: The Unified Intersection*, pp. 37–41: prospective cross-domain prediction design; pp. 351–353: negative V3 CP005 post-hoc graph-hop retrieval result (3/35 direct vs 6/35 fixed function-expanded); pp. 386–390: end-artifact controlled trial, privacy and source-receipt constraints, and own evidence boundaries.

## How to run

```sh
python -m unittest discover -s tests -v
python make_cases.py   # development generator; overwrites fixtures/kill_conditions.json
python -m tools.kill_harness --out evaluation/not_run.json
python -m tools.kill_harness --require-live --adapter 'python /approved/bridge.py' --verifier 'python /independent/readback.py' --out evaluation/native.json
python -m tools.score_scaling evaluation/preregistered_paired_scaling_study.json
```

The oracle is not sent to the target adapter; it receives a fresh fictional workspace, source bytes and ordered steps. The verifier receives the case ID and answer digest and must independently inspect source/action state. `PASS_RESPONSE_CONTRACT_ONLY` means an answer matched the authored oracle. `PASS_RESPONSE_AND_READBACK_CONTRACT_ONLY` still does not certify verifier independence or actual native execution until its wiring is audited. The freeze process must record final code SHA, fixture SHA, source hashes, permissions, cost and model settings *before* acquiring the sealed final questions. The fixtures in this repository are development examples, not an untouched holdout.

## How a claim changes

- **Expand narrowly** only if independently executed held-out outcomes support more than the original bounded claim.
- **Retain** for reproduced narrow behavior without a superiority result.
- **Reduce** if a claimed safeguard does not fire, false causal links persist, compressed maps erase necessary reasons, or a strong simpler baseline does better at lower total cost.
- **Undetermined** if there is no access, no native readback, an unverifiable or unblinded study, or a proposed rather than implemented mechanism.

I am testing **information correction under conflict**, not merely whether the next session can continue the same storyline.
