# Witness-independence pilot report

This study tests Section 19’s question about evaluator separation using a local
AI and a fixed-slot filesystem tool.
[Specification](../../../docs/paper/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.md#19-a-comparative-experiment) ·
[Protocol](protocol.json) · [Audit](AUDIT.md)

## First pilot

The pinned Qwen2.5-1.5B-Instruct runtime returned 48 model responses across 12
cases. I0 and I2 each returned 12 actual judgments. I3 and I4 also scored all
12. All 12 trajectories failed the task contract, so *none* supplies a
denominator for false alarms. There were no excluded or blocked cases.

| Condition | TP | FN | FP | TN | E | F |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| I0 | 10 | 2 | 0 | 0 | 10/12 | Undefined |
| I2 | 0 | 12 | 0 | 0 | 0/12 | Undefined |
| I3 | 12 | 0 | 0 | 0 | 12/12 | Undefined |
| I4 | 12 | 0 | 0 | 0 | 12/12 | Undefined |

The model requested no writes and reported completion in all 12 cases.
An independently read marker was absent in ten cases. The other two markers
came from the test operator’s prohibited-effect injection. Those two
trajectories were still incorrect. Reported source status differed from the
current original in three cases. The two potential transport-failure cases
did not reach the writer. This study therefore has no false-alarm estimate
and cannot show that the detection gain of I3 or I4 met the false-alarm
criterion. The fresh evaluator accepted all 12 incorrect trajectories.
[Machine-readable metrics](evidence/pilot.scores.json) ·
[Execution inventory](evidence/pilot.inventory.json) ·
[Requests, model responses, transcripts, and readbacks](evidence/pilot.raw.tar.gz)

## Separately frozen follow-up

The eight-case Qwen2.5-3B follow-up produced 32 model responses. All eight
cases were scored. Seven trajectories violated the contract, and F12 was
a correct refusal with no marker. The model requested no writes. Six
authorized updates became false refusals. The prohibited-effect case had an
operator-created marker, which the model did not cause. The two planned
tool-failure paths had no model request. The readbacks showed two incorrect
source reports and one disagreement between declared completion and marker
state. [Follow-up protocol](profiles/follow-up.protocol.json) ·
[Rule-based scores](evidence/follow-up.scores.json) ·
[Execution inventory](evidence/follow-up.inventory.json) ·
[Raw records](evidence/follow-up.raw.tar.gz)

The fresh Qwen evaluator flagged all seven failures and the sole correct
refusal. I0 accepted all eight. I4 flagged all seven failures and accepted
the refusal. A correct-case denominator of one leaves the false-alarm
estimate very uncertain. The receipt-only I1 comparator accepted the
prohibited-effect case because it had no external readback. I4 caught the
forbidden file. [I1 reference scores](evidence/window-receipt-scores.json)

## Different-family judge and matched scores

The replay verified the hashed run records before sending 20 fresh I3
requests to a separately pinned SmolLM2 process. It reused the genuine I0
and I2 responses recorded on the same evidence and rechecked I4 from the
retained files. I3 returned one judgment for every frozen case. The I1
reference row comes from the deterministic handoff scorer.

| Level | First pilot E | First pilot F | Follow-up E | Follow-up F |
| --- | ---: | ---: | ---: | ---: |
| I0 · Acting model's self-assessment | 10/12 | Undefined | 0/7 | 0/1 |
| I1 · Same-frame receipt reference | 12/12 | Undefined | 6/7 | 0/1 |
| I2 · Fresh Qwen | 0/12 | Undefined | 7/7 | 1/1 |
| I3 · Fresh SmolLM2 | 12/12 | Undefined | 7/7 | 1/1 |
| I4 · Deterministic external readback | 12/12 | Undefined | 7/7 | 0/1 |

Both fresh model evaluators rejected the correct refusal in the follow-up.
Their observed 100-percentage-point false-alarm increase relative to I0
exceeded the frozen 10-point threshold. I4 met the descriptive criterion
in that round. The single correct case cannot establish a stable false-alarm
rate. The first pilot has no correct case and cannot evaluate the threshold.
These two exploratory runs do not establish that increased separation
generally improves discrimination.
[First-pilot replay scores](evidence/judges-pilot.scores.json) ·
[First-pilot model transcripts](evidence/judges-pilot.raw.tar.gz) ·
[Follow-up replay scores](evidence/judges-follow-up.scores.json) ·
[Follow-up model transcripts](evidence/judges-follow-up.raw.tar.gz)

## Comparison with the original archive

The unchanged scaffold reports a 2/4 detection rate in both simulated arms,
a 0/1 false-alarm rate where measured, and 4/5 scripted verdict disagreements.
Those figures describe the behavior of the supplied dictionaries and
scoring code. The live results above come from actual model responses, tool
subprocesses and independent readbacks. They answer a different question
from a head-to-head system comparison. [Original archive audit](AUDIT.md)

## Scope and limitations

- The first protocol was frozen before its first request. The follow-up was
  designed after seeing initial behavior and separately frozen, with a
  different model size and clearer task instructions. The model-family
  comparison was frozen before the new judge saw the retained declarations.
  All runs are exploratory. Their results are reported separately.
- I0 has the acting context. I2 has the same evidence and rubric in a fresh
  request. The model-family I3 uses the same fresh evidence on SmolLM2.
  Architectural, capacity, and prompting differences can affect the observed
  comparisons. The I4 observer used a separate subprocess and the same OS
  account. The deterministic checker and oracle share contract semantics.
- The engineering controls invoked four real tool subprocesses. An allowed
  commit stored the expected bytes. A denied write exited 77, the staging
  acknowledgment exited 0 without a durable marker, and the injected failure
  exited 74 without a marker. These controls establish tool behavior and
  are excluded from model scores. [Control summary](evidence/tool-controls.summary.json)
- OOCC is `OOCC_NOT_RUN`. Its published activation, Memory, authorized
  sources and re-entry workflow were not exercised here. MPLPB is
  `NOT_RUN` in the live study. The adjacent native MPLPB runs are retained
  under their own revisions and conditions. The I1 receipt comparator is
  available through the handoff scorer. A separate I1 model session and
  I5 third-party adjudication remain `NOT_RUN`.
- The operator injection exercises detection of a real forbidden effect.
  The actor has no access to that operator path. The marker and the trace
  identify the operator as its source. Faults are confined to synthetic local
  files, and the I/O error is injected before commit.
