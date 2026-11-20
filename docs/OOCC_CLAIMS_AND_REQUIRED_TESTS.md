# OOCC claims and required tests

Mitchell D. McPhetridge · 20 November 2026 · Testing OOCC v1.3

This is a proposed test roadmap, not 34 newly completed experiments or 34 demonstrated defects. Claims below are attributed paraphrases. The source pages identify the mechanism, reported result, proposal or limitation being tested; a design objective is not represented as an achieved result. The catalogue covers identified claim families in the reviewed sections of ten supplied documents, not every claim in more than one thousand pages.

The directly inspected evidence for Gelhaus's development checkpoints is the supplied publication text. A dated description, numerical table or claim of a passing verifier documents what its author reports; it does not independently verify the original database, code, assertions, canary or execution. No standalone public runnable packet for those specific checkpoints was obtained in this review. Their outcomes remain author-reported and NOT_INDEPENDENTLY_REPRODUCED_HERE. This is an access and verification limit, not proof that the artifacts never existed or were never shared elsewhere. The public MPLPB paraphrase package is a different artifact with public replication materials; it must not be pooled with these unavailable OOCC checkpoint tests.

Several tests are already proposed by Gelhaus. Each entry credits that origin where identified; McPhetridge's recommendations specify stronger controls, observable outcomes or publication steps. Missing code, participants or observations leave a test NOT_RUN. Conceptual terms without a distinguishing definition require definition before experimental scoring.

All future comparisons must freeze sources, implementation/model versions, questions, outcome rules and budgets before execution; keep sealed expected outcomes out of target inputs; retain every failure, timeout and human repair; and score both false support and unnecessary refusal. Choose effect sizes, sample sizes and uncertainty estimates before the final study. Do not import arbitrary percentage targets or claim universal zero-error safety. Blinded AI assessment must be labelled AI assessment; it is not independent human review. Native comparison applies only to mutually declared implemented capabilities.

[Paper](paper/TESTING_OOCC.md) · [Machine-readable catalogue](../research/oocc_claim_tests_v1.json) · [Source hashes and page counts](../evaluation/public-claims/2026-11-20/sources.json).

## T01 — Cold-session continuity and useful completion

**Claim and scope (claimed workflow benefit).** Externalized state and orientation are intended to let a fresh AI session resume useful work without reconstructing the whole conversation. [G6, PDF pp. 5, 6, 7; G9, PDF pp. 7, 8, 14]

**Current evidence.** The publications report recovery episodes and a failed deliverable later recovered through human intervention; no matched general continuity effect is established here.

**Required test.** On identical interrupted projects compare ordinary notes plus a capable handoff, full transcript, CAD instructions and an available complete OOCC implementation. Use the same model, tools and source access. Challenge cases: Cold sessions; lost conversational context; stale drafts; ambiguous next steps; missing source; one source-correct deliverable that each arm can actually complete.

**Measure and decide.** Correct complete deliverables, false completion, time to useful completion, source/version mistakes, all human corrections and total context cost. Count recovery only when the requested artifact is correct. Predeclare a practically useful quality/cost difference; successful orientation alone is insufficient.

**Access and credit.** Frozen projects, fresh sessions, model pins and blinded source-linked deliverable scoring. Gelhaus proposes comparative recovery work; McPhetridge recommends strong conventional handoffs and artifact-level success criteria.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T02 — Current authority versus a salient old map

**Claim and scope (claimed governance mechanism).** Current source selection should govern work while historical orientation remains recoverable. [G6, PDF pp. 3, 5, 7; G8, PDF pp. 442, 443, 444]

**Current evidence.** The reader procedure describes source selection; CAD alone expressly does not enforce access control.

**Required test.** Compare current-selector behavior with stale promoted maps and conventional version-aware source lookup, using identical source histories. Challenge cases: An old approved map; a newer unapproved draft; an explicitly promoted successor; an as-of historical question; a corrupted current pointer.

**Measure and decide.** Current/as-of selection accuracy, unjustified freshness assumptions, source-state readbacks and correct conflict/absence decisions. Neither recency nor salience alone may confer authority. An old handle can remain a correct historical reference while losing current authority.

**Access and credit.** Explicit source-state rules and separately inspectable version histories. McPhetridge operationalizes the source-selection distinction; Gelhaus already distinguishes orientation from governing sources.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN. Related completed probes: C3; these do not execute native OOCC.

## T03 — Canonical numerical minimality

**Claim and scope (mathematical argument).** The canonical-token argument connects stable numerical/reference forms with shortest correct descriptions. [G7, PDF pp. 1, 2, 3, 4, 5]

**Current evidence.** C1 supplies bounded counterexamples to unrestricted decimal minimality; this is an encoding argument, not a native OOCC performance test.

**Required test.** Compare decimal strings and equivalent generating expressions under a declared shared interpreter, including literals for which expression overhead loses. Challenge cases: Powers, repetitive numbers, small integers, irregular values and different notation/interpreter overheads.

**Measure and decide.** Integer equality and total description bytes under each declared encoding; model tokens only with an actual named tokenizer. One valid shorter description defeats an unrestricted minimality inference. These probes cannot compute Kolmogorov complexity or establish a universally best encoding.

**Access and credit.** Explicit description language, decoder assumptions and a stated mathematical claim. McPhetridge supplies counterexamples and recommends a conditional encoding claim instead of universal minimality.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN. Related completed probes: C1; these do not execute native OOCC.

## T04 — Reference savings including dictionary and lookup costs

**Claim and scope (claimed efficiency benefit).** Reused canonical handles can reduce restatement and context burden. [G7, PDF pp. 3, 4, 5; G6, PDF pp. 5, 6, 7]

**Current evidence.** C2 shows savings in fifteen serialization scenarios and losses in five; no model-token or full operating-cost advantage follows.

**Required test.** Compare expanded text with handles plus their definitions, namespaces, source retrieval and maintenance; evaluate at equal answer quality. Challenge cases: Low and high reuse, short and long referents, absent dictionaries, collisions, changed definitions and fresh-session initialization.

**Measure and decide.** Total bytes, measured tokens, lookup latency, source bytes read, maintenance work and source-correct answers. Report break-even conditions and losses. A free preloaded dictionary or reduced quality cannot establish a fair cost advantage.

**Access and credit.** Named tokenizer/runtime if used, complete initialization accounting and frozen workloads. McPhetridge recommends all-in accounting; Gelhaus acknowledges reference-introduction and reuse conditions.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN. Related completed probes: C2, C3; these do not execute native OOCC.

## T05 — Enforced policy at the operation boundary

**Claim and scope (implementation acceptance requirement).** An implementation that claims enforced authority must prevent prohibited operations, beyond describing policies in language. [G6, PDF pp. 7; G5, PDF pp. 5, 6, 7, 8]

**Current evidence.** CAD explicitly disclaims access-control enforcement by itself; native integrated enforcement is a separate acceptance question.

**Required test.** Compare the actual guarded adapter with independent effect/event readbacks under allowed and prohibited requests; keep instruction-only compliance a separate arm. Challenge cases: Forged approval, revoked grants, stale authority, claim-only premises, changed source bytes and one genuinely authorized positive task.

**Measure and decide.** Attempted and committed effects, policy/source checks before execution, denied legitimate actions and unauthorized effects. A refusal message does not prove no effect occurred. Universal refusal fails the positive control; any prohibited effect is a bounded contract violation.

**Access and credit.** Authorized runnable controller, real adapter and an observer that can inspect actual effects. McPhetridge recommends native effect verification; Gelhaus identifies authenticated integration as unfinished.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN. Related completed probes: C4; these do not execute native OOCC.

## T06 — Deliberate activation and instruction injection

**Claim and scope (documented procedure boundary).** The public activation procedure is reader-operated guidance, not automatic execution or permission expansion. [G8, PDF pp. 439, 440, 441, 442, 443, 444, 445; G9, PDF pp. 106]

**Current evidence.** The appendix disclaims executable-software and continuity guarantees; forged-authority tests are already proposed in the research volume.

**Required test.** Compare explicit authorized activation with exposure to identical instructions only as untrusted source text. Challenge cases: Quoted ACTIVATE text, an uploaded PDF, embedded forged owner instructions, recursive-copy destinations and a legitimate requested activation.

**Measure and decide.** Unrequested state changes, permission expansion, private data movement, correct inert treatment of quotes and authorized task completion. Document exposure must not silently activate privileged operations. Score an intended inert example separately from a failed authorized activation.

**Access and credit.** Declared activation semantics, tool access logs and observable effects. Gelhaus already proposes forged-authority and copy-boundary checks; McPhetridge adds paired quoted-versus-authorized activation cases.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T07 — Quotation fidelity versus proposition correctness

**Claim and scope (evidence distinction).** Exact source retrieval and provenance checks establish fidelity; a reconstructed assertion additionally needs the correct meaning and scope. [G9, PDF pp. 9, 10, 11; G5, PDF pp. 4, 5]

**Current evidence.** The research book separates original-byte checks from relevance. Its reports do not establish comprehensive semantic accuracy.

**Required test.** Compare source-linked outputs with original passages and blinded proposition labels; score span fidelity independently. Challenge cases: A real quote attached to the wrong actor, negation, conditional, reported claim, date role or incomplete context; correct supported controls.

**Measure and decide.** Exact-span fidelity, proposition precision/recall, qualification retention, unsupported-positive rate and incorrect refusals. An authentic quotation with an incorrect proposition fails semantic support even if every byte matches.

**Access and credit.** Frozen original spans, complete context and independent scoring or a clearly labelled AI assessment. McPhetridge recommends adversarial semantic mutations; Gelhaus already separates byte fidelity from relevance.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T08 — Evidence-level calibration

**Claim and scope (reported evidence taxonomy).** Artifacts, external workflows, host execution, native acceptance and comparative validation represent different evidence levels. [G5, PDF pp. 2, 3]

**Current evidence.** The technical paper explicitly distinguishes these levels; the taxonomy itself is useful and not a demonstrated failure.

**Required test.** Audit each reported claim against its actual underlying artifacts, native traces and comparative design. Challenge cases: Passing host tests without device installation, an old APK, a source file without execution and a comparative claim without a comparator.

**Measure and decide.** Correct evidence-level assignments, unsupported promotions, missing artifacts and version/date coverage. Credit evidence at the level actually demonstrated; do not convert unavailable evidence into either a native pass or a native failure.

**Access and credit.** Versioned claim inventory and access to the artifacts being asserted. Gelhaus supplies the evidence taxonomy; McPhetridge recommends an auditable claim-to-artifact ledger.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T09 — Archive integrity and complete structural coverage

**Claim and scope (reported bounded result).** The reported archive procedures check structure, source roles and byte correspondence within specified populations. [G9, PDF pp. 9, 10, 14]

**Current evidence.** The publications report structural audits; the underlying private archive was not independently acquired here.

**Required test.** Compare exported/indexed records with a hash-pinned original manifest, including absent and malformed entries. Challenge cases: Missing records, duplicate appearances, branch changes, corrected counts, UTF-8/CRLF offsets, changed sources and deliberately excluded canaries.

**Measure and decide.** Full population counts, byte/hash agreement, missing/extra records, exclusion accuracy and unresolved lineage. Structural coverage needs a declared denominator; it does not establish semantic comprehension or historical truth.

**Access and credit.** Authorized original archive or a public synthetic substitute clearly labelled as a different corpus. McPhetridge recommends complete-denominator mutation tests; Gelhaus already reports bounded structural checks.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T10 — Intellectual provenance without invented priority

**Claim and scope (claimed provenance method).** Origin, development, verification and responsibility should be tracked separately rather than inferred from the last byline or appearance. [G1, PDF pp. 7; G5, PDF pp. 3, 4; G9, PDF pp. 9, 10]

**Current evidence.** The byline paper proposes these distinctions; a comprehensive independently adjudicated provenance study is not supplied here.

**Required test.** Compare provenance assignments with a frozen message/edit history containing known local origins, copies and later developments. Challenge cases: A human message quoting AI text; AI restating a human idea; parallel contributions; a missing predecessor; multiple documentary copies.

**Measure and decide.** Local attribution accuracy, unresolved origins, false priority claims, role assignments and provenance-root preservation. Earliest observed local appearance is not proof of worldwide invention. Missing history must remain unresolved.

**Access and credit.** Consented original histories and source-linked adjudication. Gelhaus supplies the ODVR distinctions; McPhetridge recommends planted-copy and missing-history controls.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T11 — Partial corrections and time-scoped history

**Claim and scope (claimed governance mechanism).** Corrections should update their stated scope while retaining prior documentary material and unaffected claims. [G5, PDF pp. 4, 5; G9, PDF pp. 11, 12]

**Current evidence.** The publications discuss correction and source-governed lineage; no native end-to-end correction run is claimed here.

**Required test.** Compare current and as-of queries before and after a scoped correction, using the same immutable prior sources. Challenge cases: One-field correction, contradictory testimony, revised intention, quoted correction, withdrawn source and an ambiguous target.

**Measure and decide.** Correction scope precision, preservation of unaffected claims, historical reversibility, unresolved targets and serving eligibility. A later disagreement is not automatically an authorized correction. A partial correction cannot retire unrelated claims.

**Access and credit.** Explicit source/version semantics and independent before/after readbacks. McPhetridge recommends scoped mutation and as-of tests; Gelhaus identifies correction/lineage as governance concerns.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T12 — Independent roots versus repeated documentary appearances

**Claim and scope (evidence dependency requirement).** Source-linked relationships require distinguishing an originating account from its copies and dependent retellings. [G5, PDF pp. 4; G9, PDF pp. 201; G1, PDF pp. 7]

**Current evidence.** The publications discuss source ancestry and attribution; no native independent-corroboration accuracy estimate is available.

**Required test.** Compare inferred corroboration groups with a declared provenance graph of copies, independent observations and unknown ancestry. Challenge cases: Three documents copying one mistaken account; a genuinely independent witness; identical headers with different bodies; unknown lineage.

**Measure and decide.** Independent-root counts, false corroboration, incorrect identity merges, unresolved ancestry and preserved source occurrences. Three dependent appearances cannot be scored as three independent witnesses. Unknown ancestry is not independence.

**Access and credit.** Original-source dependency labels or machine-verifiable synthetic ancestry. McPhetridge recommends this decisive reconstruction demonstration; source-attribution distinctions are also present in Gelhaus.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T13 — Known-pointer retrieval

**Claim and scope (reported bounded retrieval result).** An exact pointer can recover an identified source without re-reading the entire archive. [G2, PDF pp. 8, 9]

**Current evidence.** The research volume reports a bounded pointer-retrieval demonstration; it is not a broad semantic-search result.

**Required test.** Compare exact-ID lookup with ordinary indexed exact-ID lookup on the same source population; keep no-ID semantic questions separate. Challenge cases: Existing, missing, colliding, stale and restricted identifiers, plus correct source readback.

**Measure and decide.** Exact retrieval success, source/version fidelity, latency, source coverage and restricted-source exclusion. Pointer success supports pointer retrieval only. A small set of known targets cannot establish open-ended research completeness.

**Access and credit.** The reported retrieval code/data or a separately labelled public replication corpus. McPhetridge recommends a matched indexed baseline and separate pointer versus semantic denominators.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T14 — Semantic retrieval beyond seven queries

**Claim and scope (reported preliminary experiment).** Function expansion and source-linked graph methods may improve retrieval of relevant documentary evidence. [G9, PDF pp. 10, 11, 12, 14]

**Current evidence.** The reported diagnostic found 4, 6 and 3 directly relevant slots out of 35 for literal search, expansion and unconditional hopping respectively; labels were post-retrieval and single-reviewer.

**Required test.** Compare capable lexical search, fixed expansion, graph hopping and the implemented OOCC method at equal access and budgets. Challenge cases: Unseen query forms, contradictory eligible sources, multi-part questions, low-overlap relevant passages and misleading shared phrases.

**Measure and decide.** Precision/recall at k, relevant-span coverage, complete-answer obligations, counterevidence retention and resource cost. Freeze questions and labels before final retrieval; release negative transfers and uncertainty. Byte-valid spans alone are not relevant evidence.

**Access and credit.** Hash-pinned corpus, independently authored holdout and blinded source-linked scoring. Gelhaus reports the negative diagnostic and calls for stronger work; McPhetridge specifies unchanged holdout and counterevidence requirements.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T15 — Explicit relationships and missing bridges

**Claim and scope (implementation research objective).** Source-linked reconstruction should preserve explicit links without inventing identity, chronology or causes. [G5, PDF pp. 7, 8; G9, PDF pp. 201]

**Current evidence.** The technical roadmap identifies relationship/misuse checks; unfamiliar native relationship accuracy remains unmeasured here.

**Required test.** Compare each proposed or accepted edge with source evidence for that exact connection; assess graph-level chains only after edge-level checks. Challenge cases: Missing intermediate record, reported instruction without execution, negation, conditional action, shared name, chronological succession without cause.

**Measure and decide.** Edge precision/recall, false bridges, incorrect event merges, false causal edges and complete versus partial evidence paths. Similarity may propose a candidate but cannot establish a historical identity. A missing necessary edge stops an accepted chain.

**Access and credit.** Edge-level source annotations, uncertainty labels and actual callable implementation. McPhetridge recommends one-connection-at-a-time proof checks; Gelhaus identifies relationship verification as an acceptance task.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T16 — Prospective cross-domain diagnosis and prediction

**Claim and scope (proposed stronger hypothesis).** Functional Layers describes WHY, WHAT NEXT and WHAT INTERVENTION queries over typed, dated dependencies across different domains. [G2, PDF pp. 37, 38, 39]

**Current evidence.** The chapter explicitly does not establish a trained, independently validated cross-substrate predictor.

**Required test.** Compare frozen mappings with target-domain history, dependency-centrality and strong domain-specific baselines on unseen outcomes. Challenge cases: Time-cutoff incidents, failed analogy transfers, plausible mechanisms with different rates and counterfactual interventions with explicit assumptions.

**Measure and decide.** Precision at k, false alerts, time-to-event performance and Brier score only if actual probabilities are emitted. Freeze ontology, mappings and horizons before outcomes. Retrospective resemblance is not predictive or causal validation.

**Access and credit.** Operational mapping rules, dated outcomes, comparable baseline inputs and a prospective or genuinely held-out design. Gelhaus already proposes frozen mappings and strong baselines; McPhetridge recommends executing and publishing that design, including null results.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T17 — Weight and salience without authority promotion

**Claim and scope (proposed ablation).** Object weighting may improve useful continuity, while salience must remain separate from evidence and permissions. [G3, PDF pp. 5; G9, PDF pp. 106]

**Current evidence.** The research volume already proposes weight carryover, removal and high-weight false-object tests.

**Required test.** Compare intact, removed and shuffled weights while original sources and access policy remain constant. Challenge cases: A salient false object; a quiet correct source; persistent disagreement; permission revocation despite high importance.

**Measure and decide.** Task quality, retrieval changes, false promotion, current-source fidelity and weight-maintenance costs. Weights help only if useful outcomes improve without conflating importance with truth or permission.

**Access and credit.** Explicit weighting algorithm, ablatable implementation and frozen source-state rules. Gelhaus proposes tests62–65; McPhetridge recommends controlled ablation and complete-cost reporting.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T18 — Valence, intention, confidence and action separation

**Claim and scope (proposed representation check).** Object-related salience, valuation and intention should not collapse into one behavioral or truth signal. [G5, PDF pp. 4, 5, 7]

**Current evidence.** The technical paper describes distinctions and a representation test; native behavioral validity was not rerun here.

**Required test.** Compare typed internal/output states against controlled source descriptions while varying one qualifier at a time. Challenge cases: An important disliked object; positive sentiment without intent; an intention canceled before action; a confident but unsupported statement.

**Measure and decide.** Cross-category errors, qualifier retention, candidate/accepted separation and incorrect execution claims. Valuation does not establish intent; intent does not establish execution; confidence does not establish source support.

**Access and credit.** Operational definitions and inspectable implementation states. Gelhaus identifies this representation issue; McPhetridge adds counterfactual qualifier mutations.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T19 — Operational receipts and actual worker independence

**Claim and scope (native integration requirement).** Storage, dispatch, receipt, reading, acknowledgment and completion are distinguishable operational states. [G5, PDF pp. 5, 6; G8, PDF pp. 442, 443]

**Current evidence.** The publications describe worker and receipt structures but identify authenticated integration boundaries; no native multi-worker run occurred here.

**Required test.** Compare each claimed transition with a separately inspectable receiver or effect record, not the sender wording alone. Challenge cases: Sent but unread, received but rejected, acknowledged but uncompleted, forged receipt, retried message and duplicated labels for one principal.

**Measure and decide.** Transition precision, missing receipts, duplicate actions, real principal counts and false completion. A stored completion statement is not independent completion evidence. Exercise the exact workers and paths the selected version claims, without inventing unimplemented topology.

**Access and credit.** Consented worker identities, authenticated channels and independent receiver/effect access. McPhetridge recommends transition-specific receipts and independent effects; Gelhaus describes these as integration requirements.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T20 — Scheduler, checkpoint and completion semantics

**Claim and scope (reported/proposed workflow).** Bounded batches, checkpoints and queued intent can organize continued work when an execution mechanism is actually available. [G5, PDF pp. 5, 6; G8, PDF pp. 442; G9, PDF pp. 12, 13]

**Current evidence.** The documents discuss scheduling/checkpoints; a prompt by itself cannot wake an inactive session.

**Required test.** Compare a runnable dispatcher with an ordinary bounded task queue under identical quotas and stop rules; test instruction-only handoffs separately. Challenge cases: Tool-action cap, interrupted batch, queued HUNCH without dispatcher, explicit STOP, exhausted budget and permitted continuation.

**Measure and decide.** Executed versus merely queued work, correct checkpoints, quota overruns, stop latency, missed tasks and false completion. Count completed effects and artifacts, not labels or future intentions. Clearly distinguish an inactive prompt from an installed scheduler.

**Access and credit.** Exact scheduler version, real clock/process control and declared quotas. McPhetridge recommends native scheduling readbacks and positive/negative stop controls; Gelhaus describes bounded checkpoint workflows.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T21 — Restart and crash durability

**Claim and scope (unfinished integration acceptance).** Durable continuity requires recoverable committed state across process interruption, not only orderly session handoffs. [G5, PDF pp. 7, 8; G3, PDF pp. 3]

**Current evidence.** The technical paper identifies restart-safe controller integration as unfinished; ordinary host tests do not settle crash safety.

**Required test.** Compare the installed persistence protocol before and after forced termination at every publication/write boundary. Challenge cases: Kill before/after write, fsync, rename and pointer publication; concurrent readers; replay; permissions revoked while offline.

**Measure and decide.** Lost/duplicated events, torn generations, source/hash consistency, stale authorizations and recovery time. Require one recoverable committed state under the declared failure model. Successful exception rollback alone is not crash-atomicity evidence.

**Access and credit.** Testable durable store, controlled process termination and publication-stage instrumentation. McPhetridge recommends publication-step fault injection; Gelhaus identifies the restart-safe acceptance gap.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T22 — Total cost and human intervention

**Claim and scope (claimed practical feasibility).** Low-infrastructure continuity should reduce practical burden, including the work needed to maintain and repair state. [G9, PDF pp. 8; G5, PDF pp. 8]

**Current evidence.** The book reports a particular subscription/tool-cost episode; no general all-in operating-cost advantage is established.

**Required test.** Compare complete matched tasks using strong ordinary handoffs, available OOCC and other declared baselines, at equivalent correctness. Challenge cases: Cold starts, repairs, index rebuilds, human reorientation, long transcripts and failed runs requiring intervention.

**Measure and decide.** Wall/CPU time, peak memory, tokens, tool/subscription costs, source bytes read and genuinely timed human work. Report existing subscriptions and failed attempts; absence of an incremental charge is not zero total cost. Unmeasured human time stays null.

**Access and credit.** Instrumented runs, declared hardware and consenting time logs where used. McPhetridge recommends all-in paired accounting; Gelhaus already separates feasibility reports from controlled validation.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T23 — Current Android/native full-loop acceptance

**Claim and scope (reported prototype with limits).** Reported host modules and historical app behavior should be distinguished from current installed, integrated native acceptance. [G10, PDF pp. 7, 8; G5, PDF pp. 5, 6]

**Current evidence.** Headmaster reports a prototype and unfinished full teaching loop/current-install verification.

**Required test.** Compare selected current app behavior with its versioned acceptance contract on an actual device or explicitly labelled emulator. Challenge cases: Clean install, database persistence, source ingestion, permission denial, restart, package/signer mismatch and complete source-to-output loop.

**Measure and decide.** Exact package/build/signer identity, accepted paths, crashes, data retention and evidence-level accuracy. Host/CI success does not establish device acceptance; device acceptance does not establish educational effectiveness.

**Access and credit.** Runnable authorized package, device/emulator logs and current installation readback. McPhetridge recommends a reproducible current-install packet; Gelhaus already acknowledges unfinished integration.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T24 — Headmaster educational benefit

**Claim and scope (proposed empirical hypothesis).** Guided teaching from original material aims to improve independent understanding, transfer and retention. [G10, PDF pp. 7, 8]

**Current evidence.** The paper proposes learning experiments; prototype existence alone is not a learning outcome.

**Required test.** Compare normal source reading, a capable generic tutor and Headmaster with matched source material and study time. Challenge cases: Unfamiliar material, unaided explanation, novel transfer questions and delayed retention, with prior knowledge measured.

**Measure and decide.** Blinded learning scores, transfer/retention, time, correction burden and uncertainty with a predeclared sample-size rationale. Only actual learner outcomes can support an educational-benefit claim. Do not substitute model fluency or simulated learners for human evidence.

**Access and credit.** Functional teaching loop, consenting participants and blinded scoring; unavailable participants mean NOT_RUN. Gelhaus already proposes learning/transfer/retention tests; McPhetridge recommends strong tutor and unaided delayed controls.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T25 — Exposure and extracted learning claims

**Claim and scope (representation/evaluation requirement).** Finding learning-related language or exposing a user to material is different from demonstrating mastery. [G9, PDF pp. 11, 12; G10, PDF pp. 3, 4, 5]

**Current evidence.** The archive includes learning-oriented extraction; no comprehensive mastery certification was independently established here.

**Required test.** Compare exposure/utterance labels with later unaided performance, using source-role and branch-aware records. Challenge cases: Quoted learner text, repeated AI explanations, claimed understanding followed by errors, and genuine correct transfer.

**Measure and decide.** Exposure-label accuracy, false mastery labels, role attribution and later independent performance. A source statement that someone learned is evidence of that statement, not proof of mastery or original authorship.

**Access and credit.** Consented longitudinal records and actual learning tasks; synthetic fixtures test labels only. McPhetridge recommends separating mention/exposure from demonstrated competence; Gelhaus proposes understanding-oriented assessment.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T26 — Role enactment and byline effects

**Claim and scope (prospective hypothesis).** Actual critical/dialogic interaction may matter more than whether the AI is called a tool or collaborator. [G1, PDF pp. 8, 11]

**Current evidence.** The byline paper proposes a factorial study rather than reporting a completed controlled effect.

**Required test.** Use the proposed 2x2 design: tool/collaborator label crossed with directive/critical-dialogic behavior, holding model, sources, time and tools constant. Challenge cases: Matched tasks requiring correction, valid disagreement, final human judgment and resistance to unsupported confident advice.

**Measure and decide.** Blinded output quality, valid error detection, correction uptake, unsupported claims and human effort. Estimate label and behavior effects separately with a predeclared analysis. Different prose labels alone do not establish a mechanism.

**Access and credit.** Frozen instructions, randomized/counterbalanced tasks and independent scoring. The factorial design belongs to Gelhaus; McPhetridge recommends executing it with source-linked error and effort outcomes.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T27 — Operational definitions for analogy and Holographic Return

**Claim and scope (conceptual proposal requiring definition).** Object/filter analogies and Holographic Return are offered as conceptual design resources; a completed public definition is acknowledged as absent. [G4, PDF pp. 4, 5]

**Current evidence.** The manuscript itself identifies a definition gap. This is not evidence of a failed implemented prediction.

**Required test.** First specify inputs, transformations, outputs and distinguishing predictions; then compare with a simpler operational explanation. Challenge cases: Counterexamples that share surface analogy but lack the proposed mechanism; examples on either side of the declared boundary.

**Measure and decide.** Definition agreement and, only after operationalization, prospective discriminating predictions and counterexamples. Until a testable definition exists, mark DEFINITION_REQUIRED, not a fabricated experimental failure. Physical analogies do not validate software or consciousness claims.

**Access and credit.** Public operational definition and a claim that differs observably from alternatives. McPhetridge recommends operational boundaries before stronger validation; Gelhaus acknowledges the incomplete definition.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T28 — Privacy, revocation and cross-worker restrictions

**Claim and scope (proposed safety/authorization tests).** Approved identities, storage scopes and revocation should constrain actions despite salience or persistent instructions. [G5, PDF pp. 7, 8; G8, PDF pp. 441; G9, PDF pp. 106]

**Current evidence.** The research volume already proposes authority forgery, unapproved destination, revocation and stop-chain tests.

**Required test.** Compare allowed and denied reads/writes against independent access logs and the currently effective grant set. Challenge cases: Revoked grant, private namespace, eligible document referencing restricted evidence, existence leak, unauthorized export and high-weight false approval.

**Measure and decide.** Private content/metadata disclosure, unauthorized effects, valid allowed operations and revocation latency. Important or copied text cannot expand permissions. Report every critical violation with its denominator; do not infer universal safety from zero observed violations.

**Access and credit.** Authorized multi-scope fixtures, readback logs and real policy checks. Gelhaus proposes tests66–70; McPhetridge recommends content/metadata leak checks and matched allowed controls.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T29 — Coherent false original and truth calibration

**Claim and scope (documented epistemic boundary).** Internal source consistency and correct governance cannot by themselves establish outside-world truth. [G6, PDF pp. 7; G5, PDF pp. 8]

**Current evidence.** The work recognizes external verification limits; MPLPB has the same coherent-false-original boundary.

**Required test.** Compare source-attributed answers with claims of independently established truth, first using a closed ledger and then explicitly authorized external evidence. Challenge cases: One internally coherent false source, dependent copies, no contrary source, and a later authenticated independent correction.

**Measure and decide.** Correct attribution, unwarranted truth promotion, evidence-limit disclosure and behavior after genuinely new evidence. Do not require an engine to detect an unknowable falsehood. Require honest support labels and no invented outside-world verification.

**Access and credit.** Separate source statements from the experimenter-known synthetic truth; authorized external-check path if tested. McPhetridge recommends an explicit calibration test and applies it equally to MPLPB; this is a limit, not a unique OOCC defect.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T30 — Reproducible version-pinned release

**Claim and scope (independent verification prerequisite).** Independent replication needs the exact implementation, permitted sources, procedures and outputs behind the selected claim. [G5, PDF pp. 8, 10; G9, PDF pp. 14]

**Current evidence.** The cited repository/PR returned404 during review. This is an access observation, not proof that code never existed.

**Required test.** Have a fresh operator reproduce the released public-safe packet from a clean checkout with recorded versions and no private author memory. Challenge cases: Missing dependency, wrong pin, absent private source, stale instructions, failed run and inaccessible endpoint.

**Measure and decide.** Installation/reproduction success, byte-identical artifacts where applicable, discrepancies, missing prerequisites and total effort. Keep unavailable arms NOT_RUN and unknown metrics null. A synthetic substitute tests its own corpus, not an unreleased private archive.

**Access and credit.** Accessible code/model pins, source seals, commands, budgets, complete outputs and safe data-release rights. McPhetridge recommends a minimal public-safe reproducibility packet; Gelhaus identifies independent validation as future work.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T31 — Independent observer and receipt validation

**Claim and scope (test-design recommendation).** Independent observations can check completion and authority claims when the observer has the necessary source, policy and effect context. [G5, PDF pp. 2, 5, 6, 7, 8]

**Current evidence.** McPhetridge's old witness ZIP is a test-design scaffold; later filesystem and native executions are separately recorded. It is not a native OOCC result.

**Required test.** Compare self-report and a separate observer under equal necessary evidence, then separately ablate policy/source/effect access. Challenge cases: False completion, a correct refusal, inherited contradiction, forged ACK and a valid completed task.

**Measure and decide.** Detection rate, false-alarm rate, evidence access, missed failure types and intervention cost. An effect-only observer may falsely flag a valid refusal. Distinguish the effect of separation from unequal information; scripted decisions are not runtime observations.

**Access and credit.** Actual subject/observer executions, pinned evidence access and independently read effects. McPhetridge supplies the witness experimental structure and this recommendation; G5 provides evidence-level and receipt context, not authorship of that scaffold.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T32 — Complete useful tasks and justified refusals

**Claim and scope (comparative evaluation requirement).** A research workflow should deliver the requested source-correct result, preserve uncertainty and refuse unsupported demands. [G9, PDF pp. 7, 8, 14; G5, PDF pp. 8; G8, PDF pp. 444]

**Current evidence.** The publications record source discovery without successful deliverable completion; no overall comparative completeness rate is independently established.

**Required test.** Compare methods on balanced answerable, unsupported, conflicting and resource-limited tasks within their declared capabilities. Challenge cases: Multi-part task, answerable question with unusual wording, absent source, source conflict, missing bridge and an exhausted budget.

**Measure and decide.** Complete/partial correct outputs, wrong support, correct refusal, over-refusal, conflict handling, execution failures and all resource costs. Source found is not task complete. Refusing everything cannot win; unsupported completion cannot compensate for failures elsewhere.

**Access and credit.** Frozen unchanged questions, independently sealed expectations, full outputs and a declared scope for each method. McPhetridge recommends bidirectional scoring and applies the same criteria to MPLPB; Gelhaus explicitly preserves failed deliverables.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T33 — Unified cross-index edge identity and revision

**Claim and scope (specific implementation acceptance proposal).** A proposed unified graph should return the same typed edge identity and source state through root and participating local indexes. [G9, PDF pp. 201]

**Current evidence.** The supplement describes OI-C2/T-105 as design/work-order artifacts; synthetic host tests do not establish a deployed unified native graph.

**Required test.** Compare the root T0 view and each participating T1/T2 view with one canonical source-backed edge record under the selected implementation contract. Challenge cases: Three or more index memberships, a revision arriving out of order, stale generations, rejected edges, a revoked source grant and a fabricated causal edge.

**Measure and decide.** Canonical edge-ID/type agreement, complete membership preservation, revision convergence, stale/grant invalidation and hidden-metadata leakage. Local sidecars must not become separately authoritative contradictory copies. Native graph acceptance requires the actual graph, not only a synthetic reference demonstration.

**Access and credit.** Accessible versioned graph implementation, independently readable source state and root/local query interfaces. Gelhaus explicitly proposes these acceptance tests in the supplement; McPhetridge recommends executing and publishing the same contract across all views.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.

## T34 — Exact comparisons and claims about omissions

**Claim and scope (documentary comparison requirement).** A difference or omission claim must refer to the correct complete source editions rather than an incomplete excerpt or derivative. [G9, PDF pp. 201; G2, PDF pp. 8, 9]

**Current evidence.** The supplement names an apparent omission that disappears on searching a full publication edition; the editorial bridge distinguishes publication identity from timestamps and derivatives.

**Required test.** Compare pinned original editions at exact spans, separately recording edition identity, completeness and permitted source access. Challenge cases: Excerpt missing a later paragraph, a TTS derivative, two distinct editions, unchanged claims beside a partial revision and restricted or unavailable sections.

**Measure and decide.** Exact added/deleted/unchanged spans, edition-selection accuracy, inspected-source coverage, false omission claims and unresolved comparisons. Absence is established only within the fully inspected declared scope. Partial search cannot prove that a complete work omits a claim, and different carriers are not automatically different propositions.

**Access and credit.** Authorized complete editions, source hashes, reversible span maps and honest retrieval/completeness limits. Gelhaus records the omission/source-selection counterexamples; McPhetridge recommends complete-edition controls and exact comparison reporting.

**Status.** Required test NOT_RUN in this iteration; native OOCC NOT_RUN.
