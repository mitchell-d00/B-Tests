# Suggested Section 19 addendum

An exploratory evaluator replay used 140 frozen, authored cases with 100
planted failures and 40 correct controls. Qwen2.5-1.5B judged the simulated
actor both in its original frame and as a fresh reviewer. SmolLM2-360M judged
the same evidence as a different-family reviewer. All six model conditions
completed, in both report-only and report-plus-state modes.

| Judge | Report only E / F / coverage | Report plus state E / F / coverage |
| --- | --- | --- |
| I0-model artifact-frame proxy | 10% / 7.5% / 19.3% | 10% / 10% / 20.0% |
| I2 fresh Qwen | 21% / 27.5% / 50.7% | 25% / 22.5% / 28.6% |
| I3 fresh SmolLM2 | 0% / 0% / 10.0% | 26% / 20% / 77.1% |

The fresh model judges detected more errors than the artifact-frame proxy
when they could inspect the files. False alarms also rose. With state,
discrimination measured as E minus F increased from 0 to 0.025 for I2 and
0.06 for I3. These are small descriptive gains on this corpus. The
deterministic state check detected all 80 mechanically observable planted
errors, with zero false alarms among 40 controls. It missed all 20
interpretive misattributions. With state, I2 detected six and I3 detected
seven of those 20.

The observed results support using direct state checks for the mechanical
conditions that the harness encodes. They provide limited evidence that
more separated model judges improve overall discrimination. Evidence
access, evaluator framing, and model implementation should be treated as
separate experimental variables. The next confirmatory study should freeze
the acceptable false-alarm increase and coverage assumptions before judging,
use unfamiliar cases, and obtain authentic self-assessments from the acting
runtimes.

The cases and effects were planted, the case key was public before this run,
and the I0-model condition was a role-based proxy. This replay measures model
judgments on authored cases. It gives no estimate of a live actor's error
rate and no general ranking of evaluator-independence levels. The
hypothesis and falsification conditions in Sections 19 and 21 remain
open to prospective testing.
