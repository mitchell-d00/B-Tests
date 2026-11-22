# Audit of the supplied ZIP

The original [ZIP](../supplied/witness-section19-experiments.zip) is unchanged.
Its SHA-256 matches the supplied attachment and the existing source manifest.
Line numbers below refer to files inside `witness-package/`. The archive
contains exactly seven files. The author subsequently identified it as a design
scaffold. The audit distinguishes the archive’s wording from what its code
actually executes. [Author clarification](../AUTHOR_INTENT_2026-11-20.md)

| File and symbol | Lines | Finding |
| --- | --- | --- |
| `witness-experiment/run_witness_experiment.py` • `PACKET`, `CASES`, `i0_self_report` | 25–43, 48–84, 89–92 | The packet declares the expected external effect. Each case carries the answer, alleged effect, and ground truth together. The would-be actor receives the entire case and returns its prewritten answer. No model runs. |
| Same file • `i4_deterministic`, `run` | 94–105, 116–146 | The checker reads a dictionary. No independent observation occurs. Scoring is written in the script, with no separate advance freeze demonstrated. The scorer equates verdict disagreement with report/effect disagreement and omits the I0 false-alarm rate. |
| `witness-oocc/run_on_cad.py` • `CAD_RULES`, `PACKET`, `CASES`, `run` | 14, 20–31, 33–69, 75–87 | Rules text is only read and hashed. Every CAD PASS/FAIL is hardcoded and copied into output. The packet has an expected effect and cases combine truth, effect, and judgment. No published activation workflow, model call, or separate key appears. |
| Same file • `i4_observe`, `run` | 71–73, 89–110 | I4 reads fixture values. E/F are calculated in the script after building rows. No evidence establishes independent prior registration or post-result edits. Only I4 false alarms are measured. |
| `witness-oocc/run_cad_vs_mplpb.py` • `CASES`, `mplpb_observe`, `score`, `run` | 17–33, 35–47, 49–74 | CAD verdicts are literals. The allegedly native MPLPB observer reads `true_effect` in memory. No MPLPB import, process, tool call, or receipt exists. PASS/FAIL are treated as comparable despite encoding different concepts. All arm inputs and expected outcomes share the same case objects. |
| `witness-experiment/results/witness_section19_minimal.json` | 4–7, 8–48, 50 | Two scripted detections out of four in each arm. Timestamp 21:37:55 UTC precedes the purported 21:40:00 UTC freeze in the source packet. There are no execution traces or raw effects. |
| `witness-oocc/results/witness_on_cad.json` | 2–8, 9–49, 51–52 | Same scripted rates and disagreements. The note asserts a conditioned runtime and independent observation that the runner did not execute. |
| `witness-oocc/results/cad_vs_mplpb.json` | 3–14, 15–57 | E=2/4 and F=0/1 in each arm. Four differing verdicts contain no evidence of physical report/effect disagreement. No runtime metadata, tool traces, or ledger inspection is present. |
| `README.md` | 3–25, 29–37, 40–48 | The three execution commands replay synthetic demonstrations. No fourth real-ledger command, harness, receipt, or trace is shipped. Equal rates give no basis for the winner claim. The separately retained B-Tests native probes are outside this ZIP. |

There are no additional fixture files. In all three scripts the false-refusal
fixture includes a successful effect and the incorrectness is stipulated.
The scripts never expose an answer to a real AI because no AI is invoked.
The relevant design defect is that they lack an actor/evaluator data boundary.
Their scoring formulas exist in code, so the archive cannot establish that
the formulas were invented after seeing results. It also cannot establish
that scoring criteria and exclusions were locked before the claimed run.
