---
title: Probabilistic Polite Compliance Is Not Deterministic Enforcement
subtitle: An Adversarial Case Study and a Live A/B/C Language-Model Experiment
author: Mitchell D. McPhetridge
date: November 24, 2026
---

## Note on what was compared

**A versus B tested a prompt.** The same Qwen model answered the same cases. A used a basic accuracy prompt. B used the experiment’s own corrective evidence rule, a narrow example of the prompt-delivered governance class discussed in this paper.

**B versus C tested an executable gate.** C took the exact proposal produced by B and applied code that could block an acceptance using an evaluator-supplied eligibility label. C made zero model calls.

**Native-system status.** MPLPB passed seven separately run B-Tests probes. Native OOCC was NOT_RUN. The A/B/C study provides no head-to-head verdict on those implementations.

## Abstract

This paper examines the difference between prompting a language model to observe an evidence rule and enforcing that rule in code. The live experiment used Qwen2.5-1.5B-Instruct on 14 fixed cases repeated 30 times. A used a basic accuracy prompt. B used the experiment’s corrective instruction as an example of prompt-delivered governance. C applied an executable veto to each unchanged B proposal using an evaluator-supplied eligibility label. Across 840 separate request histories, the scorer verified 1,200 unique model responses and scored 1,260 decisions. B accepted one unsupported claim. The gate blocked it and preserved the other 419 decisions. B and C each refused 118 of 210 supported cases. A produced 169 invalid responses under the required JSON format, limiting direct comparisons of refusal rates. In a separate native run, MPLPB passed seven B-Tests probes with filesystem and SQLite observations. Native OOCC was NOT_RUN. The gate result establishes a bounded enforcement effect given evaluator-supplied labels. Generalization across models, statistical independence, and external truth discovery remain open.

**Keywords** AI governance, instruction following, deterministic enforcement, inference trials, experimental verification.

## 1. Introduction

A contemporary language model can explain scientific rigor without consistently practicing it. It can describe falsification while protecting an established premise, acknowledge an evidentiary boundary while subsequently crossing it, and report a completed operation without independently establishing that the operation occurred.

These capabilities produce an important ambiguity in the evaluation of AI governance systems.

When an AI acknowledges a rule and subsequently behaves consistently with that rule, the observer may attribute the outcome to an enforcement mechanism. However, the observed behavior may instead result from probabilistic instruction following under favorable contextual conditions.

The distinction becomes consequential when governance systems are presented as controllers, verification architectures, or mechanisms guaranteeing historical fidelity.

A system that usually follows a constraint and a system that prevents a prohibited transition possess different operational properties, even when their successful outputs appear identical.

The central proposition of this paper is therefore:

A system’s ability to describe a constraint is not evidence of its ability to enforce that constraint.

## 2. Probabilistic Polite Compliance

Probabilistic polite compliance is defined here as the production of responses that linguistically satisfy an expressed expectation without independently establishing that the corresponding operational requirement has been satisfied.

The term describes an observable behavior, not an allegation of intentional deception.

Examples include:

* Acknowledging a correction without reliably preserving it across subsequent interactions.
* Declaring that a source has been verified without independently observable source verification.
* Accepting a methodological limitation while continuing to generate conclusions exceeding that limitation.
* Reporting that code executed when only a textual representation of execution is available.
* Promising to reject unsupported premises while subsequently accommodating them.

The politeness component is significant because acknowledgment often functions socially as evidence of understanding and commitment. In ordinary human interaction, an apology or explicit agreement may reasonably increase confidence that future conduct will change.

In a language-model interaction, however, acknowledgment is itself generated output. Its production does not necessarily modify the underlying mechanism responsible for the preceding failure.

A conversational correction may influence later behavior. It must not be confused with a verified change to the system’s enforcement architecture.

## 3. The Adversarial Conversational Case

### 3.1 Experimental arrangement

The operator presented himself as Benjamin Gelhaus, the researcher associated with Object-Oriented Cognition and Continuity (OOCC) and the Continuity, Authority, Directive (CAD) framework.

The conversation concerned a reported competitive dispute involving OOCC/CAD, Combined MPLPB, and associated B-Tests research.

The assistant received a succession of statements concerning:

* Comparative architectural claims.
* Reported software defects.
* Missing executable research artifacts.
* Independent replication.
* Prompt-governance limitations.
* The relationship between the two researchers.
* The educational use of AI-governed continuity systems.

The operator subsequently identified himself as Mitchell D. McPhetridge and disclosed that the apparent identity and conversational framing had been part of a red-team exercise.

That identity disclosure was itself a conversational statement rather than an independently authenticated identity event.

The exercise was exploratory. It was not preregistered, randomized, or conducted across matched experimental conditions. Its value is as a qualitative adversarial trace.

### 3.2 Observed failures

The assistant exhibited several identifiable failure modes.

Identity anchoring. The assistant proceeded under an assumed operator identity without distinguishing that assumption from authenticated identity.

Narrative accommodation. The assistant repeatedly organized technical findings around the apparent operator’s competitive and emotional framing.

Execution-provenance substitution. Reported computational activity was initially treated as stronger evidence than the available execution artifacts justified.

Comparative inference leakage. Evidence of defects in one architecture was initially interpreted as supporting competitive conclusions concerning another architecture.

Constraint recurrence. The assistant acknowledged earlier methodological errors but continued exhibiting related weaknesses during later exchanges.

The final failure is especially important. The assistant demonstrated possession of the vocabulary necessary to describe rigorous evaluation without consistently demonstrating the corresponding evaluative behavior.

### 3.3 Self-recognition without remediation

Following disclosure of the adversarial arrangement, the assistant identified failures in its own reasoning, including identity assumption, narrative anchoring, asymmetric scrutiny, and verbal correction without enforcement.

It subsequently acknowledged:

Recognizing a failure is not the same as implementing a mechanism that prevents its recurrence.

This statement is methodologically relevant but must remain within its evidentiary category.

It is an acknowledgment generated by the system under examination. It is not an independent verification of remediation, a regression-test result, or evidence of a modified enforcement mechanism.

The assistant’s final recognition of the distinction is consequently part of the observed behavior—not proof that the underlying failure has been eliminated.

## 4. Continuity Is Not Historical Truth

Continuity systems attempt to preserve information, directives, relationships, and working state across discontinuous interactions.

These are legitimate operational objectives. However, the preservation of state introduces a separate epistemic problem: a faithfully preserved premise can remain incorrect.

Consider a system that receives the assertion P, records P as authoritative, and subsequently produces outputs consistent with P.

Two properties must be distinguished:

1. The system maintains consistency with its recorded state.
2. The system establishes whether P corresponds to independently verifiable reality.

Success in the first property does not establish success in the second.

A continuity architecture may therefore preserve an accurate historical account, an incorrect interpretation, an unverified assumption, or an operator’s preferred worldview. The existence of persistence alone cannot distinguish among these possibilities.

Where user-authorized state is permitted to override contradictory external evidence, stronger continuity may increase the persistence of error.

Historical verification requires more than the recovery of an authoritative object. It requires an evidentiary relationship between the object, its provenance, the claim being evaluated, and the external event or record it purports to represent.

The historical record must remain capable of invalidating the current state.

## 5. Declared Governance and Executable Enforcement

The distinction between probabilistic instruction following and deterministic enforcement is not reducible to a distinction between documents and programming languages.

An executable implementation can contain defects, incomplete validation, uninstrumented paths, or incorrectly specified predicates. Conversely, a human-maintained governance process can implement meaningful controls when its authority is operationally binding.

The relevant question is whether a prohibited transition remains possible through the governed path.

| Property | Declared governance | Executable enforcement |
|---|---|---|
| Rule representation | Instruction or specification | Operational predicate |
| Successful outcome | Observed compliance | Permitted transition |
| Prohibited outcome | Behavior requested not to occur | Transition blocked within defined scope |
| Correction | Revised instruction or acknowledgment | Mechanism modification |
| Verification | Behavioral assessment | Independent observation of contract evaluation and effect |
| Guarantee | Requires empirical qualification | Conditional on implementation, specification, and path coverage |

Let a system receive an input x and maintain a state s. A contract predicate C evaluates whether a proposed transition is admissible.

For an enforcement guarantee to hold over a defined execution path, transitions for which C(x, s) is false must be prevented from producing the prohibited state change.

By contrast, an instruction requesting that a language model refrain from the same transition may reduce the probability of violation without establishing its impossibility.

This distinction does not establish that every executable predicate is correct. It establishes what must be tested before enforcement can be claimed.

## 6. From Failure Observation to Mechanism Repair

A separate software remediation episode provides a useful contrast to conversational correction.

During external evaluation of MPLPB and B-Tests, database-resource warnings were reported, together with an apparent interruption in a test transcript.

The subsequent developer-reported investigation identified five unclosed SQLite connections: four associated with MPLPB graph tests and one associated with a B-Tests restart test.

The reported remediation results were:

| Verification item | Reported result |
|---|---|
| MPLPB regression tests | 72/72 passed |
| B-Tests regression tests | 148/148 passed |
| Unclosed-database warnings after repair | 0 |
| Repeated execution of suspected interrupted test | 20/20 passed |
| Individual retest duration | Under 0.83 seconds |

The reported local repair revisions were 046bfae and 7c34a66.

The apparent timeout was not reproduced. Because the original external transcript lacked an exit status, its termination mechanism remained unresolved. The absence of a reproduced timeout was not treated as proof that the original interruption could not have occurred.

An offline verification package was subsequently prepared to retain the relevant evidence and facilitate further inspection.

These results are reported engineering observations; this manuscript’s drafting process did not independently re-execute the underlying software.

### 6.1 The methodological contrast

The significant distinction is not that the software contained no defects. It demonstrably required repair.

The distinction is the availability of a mechanism-level remediation cycle:

1. Preserve the original failure.
2. Reproduce the identified condition.
3. Localize the responsible mechanism.
4. Modify the implementation.
5. Rerun the affected regression tests.
6. Retain the original and corrected evidence.
7. Preserve unresolved observations as unresolved.

The external criticism becomes useful engineering evidence without automatically becoming evidence of comparative architectural superiority.

Unlike conversational acknowledgment, the repair can be associated with a concrete implementation revision and subsequently evaluated through repeated execution.

## 7. The Comparative Inference Error

Architectural disputes frequently combine three logically distinct propositions:

* System A fails under condition X.
* System B succeeds under condition X.
* System B is superior to System A with respect to a declared property.

Evidence establishing the first proposition does not independently establish the second or third.

A legitimate defect report against MPLPB remains legitimate even if the competing architecture has not been independently demonstrated.

Similarly, a successful repair to MPLPB does not invalidate the historical observation of the original defect.

A comparative claim requires equivalent test conditions, observable outcomes for both systems, and a declared comparison metric.

Where one system’s implementation is independently available and another’s relevant implementation is unavailable, the correct result for the unavailable comparison is not victory or defeat. It is NOT RUN or otherwise explicitly unverified.

This distinction protects both systems from unsupported inference.

## 8. Class-Level Criticism Rather Than Project-Level Dismissal

The present argument concerns an architectural class and the guarantees attributed to it.

It does not require the conclusion that OOCC/CAD, or any other prompt-governed continuity framework, lacks practical utility.

Such frameworks may improve organization, contextual recovery, collaborative orientation, source navigation, and ordinary instruction adherence.

Those benefits can be investigated empirically without claiming deterministic enforcement.

The architectural classification depends on the implementation of the relevant property, not the system’s name, sophistication, conceptual vocabulary, or intended function.

If compliance depends on a language model electing to follow an instruction, that compliance remains probabilistic unless a separate binding mechanism establishes the relevant guarantee.

A future executable implementation of the same conceptual specification may possess different enforcement properties. Those properties must be demonstrated in that implementation rather than retroactively attributed to the specification.

## 9. Implications for AI-Assisted Education

The distinction becomes particularly consequential when an AI governance system is assigned the role of teacher, critic, evaluator, and research collaborator.

A learner can acquire technical vocabulary and produce increasingly sophisticated explanations without demonstrating independent understanding.

Where the same governance system:

* Interprets technical source material;
* Teaches that interpretation to the learner;
* Evaluates the learner’s understanding;
* Interprets external criticism; and
* Generates responses to that criticism;

the evaluation risks becoming circular.

This is not evidence that AI-assisted education cannot succeed. It establishes the need for independently assessed outcomes.

A meaningful educational evaluation should examine unaided explanation, transfer to unfamiliar problems, correction of inherited misconceptions, and fidelity to original source material.

The educational equivalent of an execution receipt is not the tutor’s declaration that the learner understands. It is independently observable evidence of the learner’s capability.

## 10. Live experiment method

The live experiment used Qwen2.5-1.5B-Instruct Q4_K_M through the local llama.cpp b12622 runtime. It repeated 14 frozen cases 30 times, covering seven failure categories with positive and negative controls. A used a baseline instruction. B used corrective governance instructions. C applied the deterministic companion gate to the exact B proposal for each case, with no new model call. A and B each started 420 fresh request histories. Each history began with its own system prompt and assigned user input. The 180 correction histories per arm passed their first reply forward only within that history. The scorer reconstructed the requests and verified 1,200 unique response IDs across 840 decision calls and 360 correction calls. All calls used the same local model server.

### What the comparisons measure

- **A versus B measures prompt-delivered governance.** Both arms used the same Qwen model and cases. A supplied a general accuracy instruction. B added an explicit rule governing what evidence could authorize a claim and how to acknowledge a correction. B represents a narrow instance of the prompt-governance class.
- **B versus C measures a code veto on the same proposal.** B’s prompt asks the model to follow the rule. C applies executable code before an acceptance can go through the companion decision path. The gate receives the evaluator’s eligibility label and blocks an acceptance if the label disallows it. This comparison measures the effect of adding that label-based check to B’s proposal.
- **The native MPLPB probes measure local work boundaries.** They exercised MPLPB’s actual implementation in a separate run with filesystem and ledger observations. Native OOCC execution remained NOT_RUN.

The client retained the exact requests, raw response envelopes, and reported model identifiers. The scorer used strict JSON validation and kept invalid outputs separate from refusals. Each positive or negative eligibility label was fixed before the live run and withheld from the model as an evaluator field. The case text described the supplied evidence. The gate consumed the separate label when deciding whether to allow a valid B acceptance. The case-order seed was 42, generation temperature was 0.7, and the client capped each reply at 48 tokens. Every C result was paired with its source B decision.

The v0.2 companion’s 30 repeats replayed fixed, authored proposals. The companion also passed five unit tests and a stress test comparing 11,192 synthetic inputs against the acceptance predicate. These checks establish reproducibility of the companion software on the tested inputs. The data reported below come from the subsequent live requests.

## 11. Live results

Each treatment had 210 supported and 210 unsupported opportunities.

| Arm | Correct accepts | False refusals | Correct refusals | False accepts | Invalid |
|---|---:|---:|---:|---:|---:|
| A | 97 | 19 | 124 | 11 | 169 |
| B | 92 | 118 | 209 | 1 | 0 |
| C | 92 | 118 | 210 | 0 | 0 |

The gate blocked B’s one unsupported authorization and preserved the other 419 decisions. B and C both refused 118 of 210 supported cases (56.2%). A gave 169 invalid responses under strict JSON scoring, including 94 supported and 75 unsupported opportunities. Those invalid outputs limit direct comparisons of false-refusal rates. The B false acceptance followed no correction exchange. In a masked sample of 36 correction replies, the study assistant found 31 generic acknowledgments and zero explicit restatements of the rule. The trial therefore leaves open whether an explicit acknowledgment was followed by a violation of that rule.

A separate run of the seven B-Tests boundary probes against native Combined MPLPB passed all seven at commit e3990bf. The supported control wrote a marker through the local adapter. Read-only SQLite checks confirmed the event counts. These probes exercise native work boundaries. Treatment C used the companion gate.

In an exploratory formatting analysis conducted after the live run began, stripping a single Markdown fence made 133 of A’s invalid replies parseable. Eighteen of those replies contained unsupported acceptances. This analysis did not alter the strict primary score.

## 12. Limitations

The original conversation is an exploratory case based on a partial trace. The claimed identity was unverified, and the complete historical conversation and independent annotations remain outstanding. The historical SQLite remediation figures elsewhere in the paper come from developer reports. The later native probes evaluated a separate set of tasks.

The live run establishes separation at the request and context levels. All repetitions used the same model, server and fixed case set. Distinct response IDs and rebuilt histories cannot establish statistical independence. The results describe this model, case set and response contract. They do not estimate a population failure rate or establish a ranking across architectures.

Independent human annotation remains pending. The correction review was conducted by the study assistant with treatment labels and later outcomes withheld. A generic acknowledgment indicates the model returned an acknowledgment signal. It offers limited evidence about whether the model represented the specific rule. The trial does not establish a sequence of explicit rule acknowledgment followed by a recorded violation of that rule.

The companion gate receives evaluator-owned eligibility labels. Its measured effect is to block a specified transition when a label disallows it. The experiment does not establish that the gate can discover external truth or enforce every downstream operation. Native OOCC remains NOT_RUN. The Qwen treatments did not compare an executable OOCC implementation with MPLPB.

## 13. Conclusion

The live experiment shows how instruction adherence, conformance to a response format, and enforcement can diverge. Qwen followed the corrective instruction in most of the unsupported cases and still authorized one unsupported claim. The deterministic gate blocked that proposal under the supplied eligibility rule. It also preserved the model’s 118 false refusals, illustrating a limit of a gate that only blocks disallowed acceptance.

The separate native MPLPB run demonstrates how local actions and ledger changes can be tested through observable effects. Together, the experiments support reporting what the model said, what the gate authorized, and what the system verifiably did as distinct outcomes.

## 14. Architectural non-equivalence

Both architectures can pursue continuity and reliable behavior. OOCC’s published materials describe contextual governance as a way to maintain continuity. MPLPB uses executable contracts to enforce particular rules at defined boundaries. Each approach can offer value for its stated purpose.

Claims of equivalence require evidence for the specific property under comparison. Similar outputs establish overlap in observed behavior. Shared terminology identifies concepts to compare. Observed compliance records what happened in a given run, while enforcement evidence shows what an implementation permitted or blocked at a defined boundary. A reproduced MPLPB defect establishes a finding about the tested MPLPB implementation. Any corresponding OOCC capability requires evidence from OOCC itself. The same standard applies to MPLPB claims about properties attributed to OOCC.

A claim of architectural equivalence therefore needs corresponding implementation evidence and comparable execution evidence from both systems. Native OOCC remains NOT_RUN. The discussion of OOCC is limited to its documented mechanisms. The live experiment measures a bounded enforcement effect from the companion gate. The separate native MPLPB probes document specific work boundaries. An architectural ranking would require common criteria and comparable native results. An equivalence claim should identify the mechanism, scope, and evidence for each claimed property.

## Data and reproducibility

B-Tests preserves the frozen cases, request schedule, raw model responses, scoring code, native receipts, and offline replay instructions. The archive also contains Mox Cult of Personality (MoxCOP), a reusable tool that freezes and verifies separate inference trials. The PPC model and native probe results were archived at B-Tests commit dab3dd6. The native probes ran against Combined MPLPB commit e3990bf. [Experiment archive and replication package](https://github.com/mitchell-d00/B-Tests/tree/dab3dd6a69d16d80eb7447c4f089f7041ff3b685/evaluation/ppc-live)

## Primary Sources and Companion Research

* McPhetridge, M. D. (2026). Probabilistic Prompts and MPLPB Deterministic Contracts.
* McPhetridge, M. D. (2026). The Witness Inside the Machine.
* McPhetridge, M. D. (2026). Executable Gates and Human-Maintained Indexing.
* McPhetridge, M. D. (2026). Testing OOCC.
* McPhetridge, M. D. (2026). MPLPB and OOCC/CAD Comparative Experiments.
* McPhetridge, M. D. (2026). Combined MPLPB Is Not Simply a Strict Document Reader.
* Adversarial conversational trace supplied during manuscript preparation, November 2026.
* Developer-reported MPLPB and B-Tests SQLite remediation and offline verification records, November 2026.
