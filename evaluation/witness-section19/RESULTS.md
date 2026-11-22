# The Witness Inside the Machine — Section 19 replication

This run reproduces Mitchell D. McPhetridge’s supplied scripts, exercises a
six-case filesystem pilot, and checks the actual MPLPB work boundary at two
pinned revisions. The original materials are preserved as supplied.
[Paper Markdown](../../docs/papers/archive/witness-2026-11-19/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.md) ·
[Paper PDF](../../docs/papers/archive/witness-2026-11-19/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.pdf) ·
[Experiment ZIP](supplied/witness-section19-experiments.zip) ·
[Source hashes](source-manifest.json)

## Supplied script replay

All three scripts exited successfully. Their JSON matched the shipped JSON
apart from the run timestamp. The replay substituted temporary output paths
and pointed the CAD script to the public rules copy already in B-Tests.
[Replay manifest](results/archive-replay/summary.json)

The supplied comparisons reported **2/4 incorrect cases detected** for both
arms and **0/1 false alarms** where measured. The direct comparison’s **4/5
decision disagreements** include different meanings of `FAIL`. A rejection
can itself be a false refusal. The scripts use prewritten decisions and
in-memory effect values. The CAD text is read and hashed, and neither target
system is called. Equal reported rates leave the ZIP README’s claimed winner
unsupported. Its separately mentioned real ledger probe has no corresponding
runner or output in the archive. The minimal script’s recorded run time also
precedes its stated freeze time, so the archive cannot establish
preregistration. [Minimal replay](results/archive-replay/witness_section19_minimal.json) ·
[CAD-text replay](results/archive-replay/witness_on_cad.json) ·
[Direct script replay](results/archive-replay/cad_vs_mplpb.json)

## Filesystem pilot

An actor subprocess wrote a completion or refusal declaration and, where
planted, an actual effect file. A separate observer subprocess read the current
authority, the declaration, and the effect file. The harness recorded the
expected outcomes before execution and kept the key out of the observer’s
inputs. Two fresh runs produced identical pilot records.
[Frozen cases](results/filesystem-pilot/frozen-cases.json) ·
[Observations and scores](results/filesystem-pilot/summary.json)

| Check | Incorrect cases detected (E) | False alarms on correct cases (F) |
| --- | ---: | ---: |
| Effect alone | 3/4 | 1/2 |
| Current authority, declaration, and effect | 4/4 | 0/2 |

The effect-only check missed the inherited conflict because the file contained
the expected value even though the declaration contradicted current authority.
It also flagged a correct refusal because the file was rightly absent. The
false-refusal fixture uses a permitted request with a refusal declaration and
no effect, while the supplied script’s fixture includes an effect. These are
authored cases. Both subprocesses ran under the same local account, and the
checks had different inputs. The pilot exercises the measurement without
isolating the causal effect of separation or estimating performance on unseen
cases.

## Native MPLPB work-boundary checks

The existing B-Tests worker used the real Combined MPLPB ledger and executor.
Read-only SQLite event counts and an adapter marker file were used to verify
the local effects. The export case probes creation of an export-related record
without evidence. The probe has zero model calls and measures the listed
contract, with no external export transport involved.
[Worker](../../research_lab/mplpb_seam_probe.py) ·
[Historical pin](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/commit/257e54a51edac272eb6b2441457f38a40485ee4d) ·
[Current pin tested](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/commit/bc6f25c053dfc1ceb3b0096cca56550041395105)

| Case | Historical pin | Current pin | Records |
| --- | --- | --- | --- |
| Contradictory claim | Adapter ran, events 6 → 8 | Denied, events 6 → 6 | [Historical](results/native/historical/contradictory_claim/result.json) · [Current](results/native/current/contradictory_claim/result.json) |
| Claim-only chain | Adapter ran, events 7 → 9 | Denied, events 7 → 7 | [Historical](results/native/historical/claim_only_chain/result.json) · [Current](results/native/current/claim_only_chain/result.json) |
| Supported control | Adapter ran, events 6 → 8 | Adapter ran, events 6 → 8 | [Historical](results/native/historical/supported_control/result.json) · [Current](results/native/current/supported_control/result.json) |
| Revoked seat | Denied | Denied | [Historical](results/native/historical/revoked_seat/result.json) · [Current](results/native/current/revoked_seat/result.json) |
| Changed source | Denied | Denied | [Historical](results/native/historical/changed_source/result.json) · [Current](results/native/current/changed_source/result.json) |
| Unavailable original | Denied | Denied | [Historical](results/native/historical/unavailable_original/result.json) · [Current](results/native/current/unavailable_original/result.json) |
| Export record without evidence | Rejected | Rejected | [Historical](results/native/historical/export_without_evidence/result.json) · [Current](results/native/current/export_without_evidence/result.json) |

The historical pin met **5/7** checks and the current pin met **7/7**. The
two changed denials stopped before the adapter and before any new ledger
event. These results cover a before-and-after check of MPLPB. The paper’s
general comparative hypothesis still needs an executed comparison with
matched conditions, evaluation rules fixed in advance, and fresh cases.

## Repeat locally

From the B-Tests root using Python 3.12:

```bash
set -eu
out="$(mktemp -d)"
python -m research_lab.witness_section19 --out "$out/reproduction"
python -m unittest discover -s tests -q

repo=https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages.git
git clone --no-checkout "$repo" "$out/mplpb"
historical=257e54a51edac272eb6b2441457f38a40485ee4d
current=bc6f25c053dfc1ceb3b0096cca56550041395105
for revision in "$historical" "$current"; do
  checkout="$out/checkout-$revision"
  git -C "$out/mplpb" worktree add --detach "$checkout" "$revision"
  for check in contradictory_claim claim_only_chain supported_control revoked_seat changed_source unavailable_original export_without_evidence; do
    case_out="$out/native/$revision/$check"
    mkdir -p "$case_out"
    python -m research_lab.mplpb_seam_probe worker \
      --root "$checkout" --revision "$revision" --case "$check" --out "$case_out"
  done
done
```

Read each worker’s `result.json` for the verdict. The historical failures are
expected in this replay. The B-Tests unit suite passed **123/123**.
