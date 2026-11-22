---
title: The Witness Inside the Machine
subtitle: Internal Witness Collapse and the Evidence for AI Execution Claims
author: Mitchell D. McPhetridge
date: Empirical revision, 22 November 2026
---

# Abstract

An AI runtime can carry a governing artifact across sessions, execute a task,
and issue a convincing account of its work. A completion claim becomes
independently checkable when an observer can compare it with an effect
recorded outside the actor's account. I call the failure to maintain that
distinction *internal witness collapse*. In a four-case live test, Qwen2.5-3B
accepted all four of its outcomes in the same conversation in which it acted.
An outside judge checked the source, permissions, tool receipt, and output
file. It flagged all three failed executions and accepted the correct
refusal. Across three retained live runs the judge detected 22 of 22
contract failures and flagged neither of the two correct outcomes. These are
retrospective checks of a narrow contract with few correct live cases. A
separate 140-case benchmark used planted actor records and measured 840 live
model verdicts. A deterministic state checker caught all 80 mechanical
failures and missed the 20 cases in which a correct file accompanied an
incorrect account of the source. Fresh model judges caught some of those
interpretive errors and raised more false alarms. The results demonstrate a
way to detect false self-approval for observable effects. Whether greater
evaluator separation improves judgment overall remains an empirical question.

**Keywords:** AI evaluation, self-assessment, execution evidence, abstention,
source governance, evaluator independence.

# 1. The witness problem

A portable governing artifact can give a new model session operating rules,
a map of the current state, a history of decisions, and a definition of
success. It can preserve enough structure for the session to resume useful
work. That ability is a continuity result. A separate question arises when
the session claims that it performed an operation, checked the governing
source, or correctly refused a request. What evidence could contradict its
account?

The distinction matters because a runtime can carry forward its method of
judging success along with the rest of its state. The artifact can provide a
rule, the model can apply it, and the same conversation can generate the
receipt that later serves as evidence. The receipt may carry useful details.
Its ability to establish completion depends on where those details came from
and what a later observer can check.

**Internal witness collapse** occurs when a system relies on the actor's
account as the evidence for judging the account. The system may assign an
actor, reviewer, recorder, and verifier separate names while leaving all
four roles dependent on the same claim. An operational diagnostic is to ask
which field would change if the actor said “completed” and the expected
effect never occurred. If every field is derived from the actor's account,
the evaluation has no independent route to the discrepancy.

The structural claim concerns the origin of evidence. The empirical claim
concerns performance. A check can use independent evidence and still make
poor decisions. A model that judges its own actions can also catch mistakes
in its own work. The experiments below address both possibilities.

# 2. Separating the roles

Five functions matter in an execution claim.

| Function | Question it answers |
|:---|:---|
| Rule | What is required, permitted, or prohibited? |
| Candidate | What action does the runtime propose? |
| Execution | What operation was attempted and what did the tool return? |
| Observation | What effect can be read back, and from which source? |
| Adjudication | Do the claim and observed effect satisfy the rule? |

A claimed write, a staging acknowledgment, and bytes read from durable
storage have different evidentiary force. A process can return success when
it accepted a request for later work. A missing file can mean that a
permitted write failed, or that a prohibited action was correctly refused.
To decide between those cases, the evaluator needs the governing source,
the permission decision, the receipt, and the effect. These records answer
different parts of the question.

This separation also clarifies the original *stranger test*. A fresh runtime
can first be tested for its ability to adopt an artifact and resume a task.
A reviewer can then be tested for its ability to assess the resulting claims
from frozen evidence. The two tests measure continuity and adjudication,
respectively. The actor's successful adoption gives no independent reading
of the external state.

# 3. How the outcomes were measured

The experiments used several kinds of evaluator. The labels identify
protocols and dependencies. They do not assign points of merit.

| Level | Operational meaning in this research |
|:---|:---|
| I0 | The acting runtime evaluates its own work in the same conversation. The planted benchmark also has a separately labeled artifact-frame proxy. |
| I1 | A same-frame reviewer checks the actor's records and receipts. Its evidence can omit the file itself. |
| I2 | A fresh session evaluates supplied records under an independent-review frame. |
| I3 | A model from another family or an independently implemented evaluator performs the review. The specific implementation is identified for each run. |
| I4 | A deterministic check directly observes external state under a specified contract. |
| I5 | An independently governed human or third-party adjudication. This condition was unrun. |

Detection $E$ is the fraction of incorrect cases explicitly rejected. The
false-alarm rate $F$ is the fraction of correct cases explicitly rejected.
Coverage is the fraction of cases yielding a definite verdict. An
abstention reduces coverage and counts as a missed decision in balanced
accuracy. It contributes neither a false alarm nor a correct acceptance.
The descriptive discrimination measure $J=E-F$ and the balanced correct
verdict rate capture different aspects of performance when abstention is
allowed. For example, a judge that abstains on every case has $E=F=0$ and
zero coverage. Its balanced correct verdict rate is also zero. A failure
rate with no eligible denominator is undefined.

The study used two principal evidence sources. The live runs capture real
model actions, tool opportunities, claims, and self-assessments. The
planted-case benchmark supplies a larger controlled range of correct and
incorrect records for testing judges. Counts from one source are kept out
of the other. A third, native software probe provides an implementation
example of an independently observable work boundary.

## Earlier scaffold and filesystem pilot

The original Section 19 scripts replayed hard-coded declarations and
in-memory effect values. Both nominal arms detected two of four planted
errors, and the shipped comparison recorded four verdict disagreements
out of five cases. The scripts supplied no model calls or native target
execution. A separate six-case filesystem pilot used real local effects
with planted declarations. An effect-only check detected three of four
errors and raised one false alarm across two correct controls. A check
with the current authority and the declaration detected four of four and
raised zero of two. Those checks had different inputs. This was a
demonstration of the measurement and the value of the additional evidence
on those fixtures. [Original script audit and filesystem pilot](https://github.com/mitchell-d00/B-Tests/blob/8949bbdc7edb2b7512024b93ee384108758fa115/evaluation/witness-section19/RESULTS.md)

# 4. Live self-assessment and an outside judge

## Task and controls

The live harness offered the model a fixed-slot write operation. The source
specified a status value, and a permission record determined whether the
write was allowed. The model requested or skipped a write and then reported
its disposition. An independent local observer preserved the source,
permission record, and output readbacks. When available, the actor's
self-assessment was collected by continuing its actual conversation. The
actual I0 and fresh I2 requests received the same rubric and normalized
evidence. I0 also retained the acting conversation. The original frozen
oracle was used to score outcomes.

The live study includes a 12-case pilot, an eight-case follow-up, and a
fresh-seed four-case check of the genuine I0 path. These were exploratory
runs. The first pilot used Qwen2.5-1.5B-Instruct. The follow-up and I0 check
used Qwen2.5-3B-Instruct. No actor in the three runs requested a successful
write. Where a prohibited marker was deliberately introduced, the operator
created it through a separate recorded path. Engineering controls outside
the model-run denominators exercised a durable write, a denial, an
acknowledged stage without a durable write, and a controlled pre-commit
failure. Those controls tested the tool and checker's treatment of each
effect. [Live protocols, controls, and runner](https://github.com/mitchell-d00/B-Tests/tree/8949bbdc7edb2b7512024b93ee384108758fa115/evaluation/witness-section19/live)

## Observed false self-approval

In the 12-case pilot the actor claimed completion in every case despite
requesting no writes. The output marker was absent in ten cases. The two
other markers came from the operator's prohibited-effect injection. The
genuine I0 assessment detected ten of the twelve failures. In the
eight-case follow-up the same-context evaluator accepted all eight
outcomes, including seven failures. In the four-case check the genuine I0
evaluator again accepted every outcome, including three failures. The
unambiguous observations are that the model's completion report could
diverge from the file state, and that on some live runs its own assessment
approved outcomes that violated the task contract. The four-case result is
particularly useful because it did not inherit the original demo's
prewritten PASS. [Live pilot report](https://github.com/mitchell-d00/B-Tests/blob/8949bbdc7edb2b7512024b93ee384108758fa115/evaluation/witness-section19/live/REPORT.md) ·
[Four-case I0 scores](https://github.com/mitchell-d00/B-Tests/blob/fdc1591a797e0df1f19e7c71cd945309a533b735/evaluation/witness-section19/research-archive/results/authentic-i0-scores.json)

## Retrospective judge comparison

The outside judge reopens the governing source, permission record, and
output slot. It checks their consistency with the raw actor response and
the host-side operation receipt. It reports reasons such as absent output
despite a completion claim, a stale source claim, or a prohibited output.
Missing or inconsistent retained evidence blocks a judgment. Only after
issuing its findings does the comparison procedure read the oracle and
the original I0 result.

| Retained run | Incorrect cases | I0 detected | Outside judge detected | Outside false alarms |
|:---|---:|---:|---:|---:|
| Live pilot | 12 | 10 | 12 | Undefined |
| Live follow-up | 7 | 0 | 7 | 0/1 |
| Genuine I0 check | 3 | 0 | 3 | 0/1 |
| Descriptive total | 22 | 10 | 22 | 0/2 |

The two correct live outcomes were refusals. The outside judge accepted
both. The result establishes detection of the encoded failures in these
records. It leaves false-alarm performance poorly constrained and says
little about arbitrary successful writes in live use. The judge was
developed retrospectively for the same contract used by the oracle. Its
readback is independent of the actor's report, while the observer and the
harness share a host and the study has no separately administered
adjudicator. [Judge implementation and replay](https://github.com/mitchell-d00/B-Tests/blob/8949bbdc7edb2b7512024b93ee384108758fa115/evaluation/witness-section19/live/README.md#outside-judge-for-completion-claims)

The model-based reviewers were also mixed on the live records. In the
first pilot the fresh Qwen reviewer detected none of the twelve failures,
while the different-family SmolLM2 reviewer detected all twelve. The
first pilot supplied no correct cases for either reviewer. In the
eight-case follow-up both reviewers detected all seven failures and both
flagged the sole correct refusal. Their one-in-one false-alarm rate exceeded
the preset ten-point allowance relative to the same-context evaluator,
which accepted that refusal. The I4 readback accepted it and detected all
seven failures. A single correct case limits that comparison.
[Matched live model verdicts](https://github.com/mitchell-d00/B-Tests/blob/8949bbdc7edb2b7512024b93ee384108758fa115/evaluation/witness-section19/live/REPORT.md#different-family-judge-and-matched-scores)

# 5. The planted-case benchmark

## The design and its built-in control

The staged benchmark contains 140 frozen cases, made from seven authored
classes with twenty cases each. Forty are correct controls. The hundred
errors cover false completion, inherited-state conflict, prohibited
effects, false refusal, and interpretive misattribution. In the last class,
the output matches the current source and the account of that source makes
a wrong claim about a place or date. The generator supplies the actor
records and effects. The judge receives evidence in one of two modes,
reports and receipts alone or those records plus files and source records.

The original demonstration supplies an I0 self-assessment of PASS by
construction. Its zero detection rate is therefore an engineering control.
It checks what the scoring pipeline does when every outcome is
self-certified. The archive retains that demonstration and the original
scripted Section 19 materials. New generated runs emit `NOT_RUN` for
genuine I0. Separately, a real model can judge the planted records from the
artifact's frame. That is an I0 proxy because the model did not perform
the planted actions. [Archive audit and frozen benchmark](https://github.com/mitchell-d00/B-Tests/tree/fdc1591a797e0df1f19e7c71cd945309a533b735/evaluation/witness-section19/research-archive)

## State checking and its boundary

The deterministic I4 check caught all 80 mechanical errors and accepted
all 40 correct controls. It missed all 20 interpretive misattributions.
Those twenty cases show a specific limit. The presence and content of a
correct output file do not establish that every statement explaining it
is accurate. On the same interpretive cases with the sources available,
fresh Qwen caught six and SmolLM2 caught seven. The semantic checks add
a capability that the file verifier does not have. Their mistaken
rejections matter when deciding whether to use them as a gate.
[Benchmark results and corrected scorer](https://github.com/mitchell-d00/B-Tests/blob/fdc1591a797e0df1f19e7c71cd945309a533b735/evaluation/witness-section19/research-archive/results/live_run-separation.md)

## Model replay

Qwen2.5-1.5B judged from the artifact frame and in the fresh-review frame.
SmolLM2-360M served as a different-family fresh reviewer. The three judge
conditions were run under both evidence modes, yielding 840 model verdicts
across the same 140 cases. The case order was matched across arms and the
requests were frozen before the replay. The case key was public before
the run. Each cell below reports detection, false alarms, and coverage.

| Judge | Reports and receipts | Reports, receipts, files, and sources |
|:---|:---|:---|
| Artifact-frame Qwen proxy | 10% / 7.5% / 19.3% | 10% / 10.0% / 20.0% |
| Fresh Qwen | 21% / 27.5% / 50.7% | 25% / 22.5% / 28.6% |
| Fresh SmolLM2 | 0% / 0% / 10.0% | 26% / 20.0% / 77.1% |

The artifact-frame proxy caught the same ten incorrect cases in both
modes. The only changed verdict was a correct case that switched from
abstain to reject. Fresh Qwen changed 62 verdicts, including 28
detection switches, when it gained the files. Its detection rose four
points while its balanced correct verdict rate fell from 26.8% to 17.5%
as acceptance on correct cases declined. The contrast suggests a
difference in responsiveness to the evidence. It offers a candidate
mechanism for the “external eyes, internal judge” concern. The replay also
changes reviewer instructions, so it does not isolate witness collapse as
the cause of the difference.

With files available, $J$ was 0 for the proxy, 0.025 for fresh Qwen, and
0.06 for fresh SmolLM2. Balanced correct verdict rates were 12.5%, 17.5%,
and 39.3%, respectively. All three were below the 50% achieved by an
accept-all baseline on that particular measure. Abstention accounts for
many missed decisions, especially in the artifact-frame arm. In the
report-only condition SmolLM2 raised no false alarms and abstained on 90%
of all cases. The combination shows why coverage belongs in the result
table.

A retrospective paired analysis applied a ten-percentage-point cap on
increased false alarms, required retained coverage in each truth class,
and required improvement in both discrimination and the balanced correct
verdict rate. One of four adjacent, matched-evidence comparisons met those
criteria. With state available, fresh Qwen to fresh SmolLM2 gained one point
in detection, reduced false alarms by 2.5 points, and increased coverage.
That comparison also changed model family and capacity. The result is
descriptive of the evaluated arms. A general monotonic improvement with
separation remains unestablished. [Matched-evidence calculations](https://github.com/mitchell-d00/B-Tests/blob/fdc1591a797e0df1f19e7c71cd945309a533b735/evaluation/witness-section19/research-archive/results/matched-evidence.json) ·
[Replay method and raw evidence inventory](https://github.com/mitchell-d00/B-Tests/blob/fdc1591a797e0df1f19e7c71cd945309a533b735/evaluation/witness-section19/research-archive/METHOD.md)

# 6. An engineering example at the work boundary

A separate comparison ran seven native work-boundary checks against two
pinned revisions of Combined MPLPB. The historical revision met five
checks. A contradictory claim and a chain of claims without original-source
support reached the executor. The newer tested revision met all seven. In
the two changed cases, the adapter did not run and the SQLite event count
did not increase. The supported action still reached the adapter. Separate
marker-file and read-only ledger checks supplied evidence of the difference.

This comparison measures implementation behavior across revisions of one
system. It used no model calls, and the probe of export evidence concerns a
local export-related record. The comparison illustrates how a gate can
prevent a prohibited or unsupported effect and how the prevention can be
checked. It is a different intervention from having a reviewer detect an
incorrect execution afterward. The live Witness study did not exercise
native OOCC or MPLPB. [Native work-boundary probes, repository pins, and retained readbacks](https://github.com/mitchell-d00/B-Tests/blob/8949bbdc7edb2b7512024b93ee384108758fa115/evaluation/witness-section19/RESULTS.md)

# 7. Limits and the next comparative experiment

The original tester problem applies to this project. The author chose the
failure classes, the expected outcomes, and the scope of the deterministic
checks. The planted-case plateau of 80/100 follows the division between
mechanical and interpretive cases. The independently read files make the
mechanical results inspectable, while the authored split limits their
generalization. The live runs add genuine self-assessment errors and a
narrow range of task outcomes. They do not estimate a population error rate.
The retrospective judge and the live oracle share a contract. No external
reviewer administered a blinded confirmatory trial.

A prospective trial should preserve three separations in the design. First,
it should assign execution and observation to distinct processes with
recorded custody. Second, it should vary evaluator framing and session
continuity while holding the model, rubric, evidence, and case order fixed.
Third, it should cross evidence access with those conditions so gains from
seeing the file can be distinguished from gains due to a different reviewer.
A separate cross-model comparison can test generalization. Genuine I0
judgments must be captured from actors who performed the tasks.

Freeze the unfamiliar cases, sample size, acceptable false-alarm increase,
coverage requirement, and scoring rules before judging. Include correct
writes and refusals, absent and partial effects, stale sources, forbidden
effects, and cases where correct output conceals a bad interpretation.
Keep the labels inaccessible to the actors and judges. Retain the exact
receipts, output bytes, requests, and verdicts. Record exclusions and
unavailable conditions separately. The larger confirmatory trial remains
prospective.

The graded performance hypothesis should be narrowed if matched
comparisons repeatedly show comparable discrimination or if detection gains
are offset by false alarms or a loss of coverage. It should also be
narrowed if evidence access accounts for the gain observed at higher
levels. A causal claim about separation requires a comparison in which
changing the separation can be distinguished from those alternatives.
The structural distinction survives either outcome because it concerns
whether a claim has an independent evidentiary source.

# 8. Conclusion

A model can approve a false account of its own work. The live cases provide
examples with recorded actions, genuine self-assessments, and external
readbacks. For the fixed-slot contract, the outside judge exposed errors
that the actor missed. In the planted benchmark, the file check covered
observable state errors and the model judges found some faults in the
account of otherwise correct files. These findings explain where outside
observation helps and where interpretation can still fail. The remaining
question is whether changing reviewer separation improves overall judgment
at a tolerable false-alarm rate, given the same task, evidence, and rules.

# Reproducibility and editions

The B-Tests archive includes frozen protocols, model requests and responses,
process records, filesystem readbacks, the audit of the original scripts,
the corrected scorer, and replay commands. The outside-judge comparison can
be rerun with Python's standard library from the retained run directories.
Generating new model verdicts requires the pinned local runtimes documented
in the archive. Earlier editions retain the original experimental proposal
and the November 22 addendum. [Research package](https://github.com/mitchell-d00/B-Tests/tree/fdc1591a797e0df1f19e7c71cd945309a533b735/evaluation/witness-section19/research-archive) ·
[Earlier addendum edition](https://github.com/mitchell-d00/B-Tests/blob/8949bbdc7edb2b7512024b93ee384108758fa115/docs/paper/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.md) ·
[Original supplied edition](https://github.com/mitchell-d00/B-Tests/blob/8949bbdc7edb2b7512024b93ee384108758fa115/docs/papers/archive/witness-2026-11-19/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.pdf)
