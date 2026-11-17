# Current Combined MPLPB and sorter rerun — 17 November 2026

Evaluated Combined: `ccbb5804eb47f78c2338d57c142ad087b47be710` (PR49). Sorter runtime: `30f0d89c5954b1f1226d0e30c78dc671011849e1`; current sorter source SHA matches `20a8625676e998ce282283629709f3b5dc7a8b9281ffff10457e5a0595a28e73`. Unchanged pre-sorter reader: `3df2c6e22f0ef454f3ee67b88d43402a42f63443`. Earlier repositories: Portable `4fdc20193c01f82baea0598b4c7d8ef3040772d5`, residual `1ec160051ba306ce61d74ba3186f0aa5873694c5`; residual reproduction uses its required Combined `257e54a51edac272eb6b2441457f38a40485ee4d`.

## Fresh outcomes

| Executed condition | Outcome | Scope |
|---|---|---|
| Full current native Python suite | 1,186 PASS | Authored software tests, not historical accuracy |
| Seven additional native commands | All PASS | UI script, browser transport, JS API, crawler worker, infrastructure, committed handoff, five-instance recovery |
| Seven B-Tests work-boundary probes | All PASS | Real local positive effect; actual blocked negative effects with state readback |
| Ten applicable legacy query fixtures | Ten PASS_CONTRACT | Explicitly retargeted unchanged fixtures/scoring; six instruction cases OUT_OF_SCOPE |
| Public evidence evaluation | 52 pass | Bounded published developer controls, no independent gold |
| Sorter mode, export, compatibility and withholding | PASS | 176 identical nodes;264 raw edges;77 added review edges; zero eligible snapshot sources in all three profiles |
| Smart Local / Swarm / Networked / Image | 52 /145 /61 /93 PASS | Bundled component native suites; no root-suite repeat |
| Local Mirror and five adoption checks | PASS | Current native ledger sealing and validation |
| Existing twelve public-paper queries | All outputs identical except temporary root | Six page returns, five ambiguous, one not_in_corpus; no answer_supported field |
| B-Tests laboratory tests | 121 PASS | Harness controls, not new target trials |
| Historical native evidence replay | PASS | Zero new target execution; historical pins retained |
| Portable Python tests | 29 PASS | Earlier capsule verifier software |
| Portable JS strict / authoring checks | 11 /10 PASS | Two distinct runtime surfaces |
| Portable synthetic scenarios | 15/15 PASS | Pinned exact-key synthetic cases |
| Portable offline Chromium | 13/13 PASS | Identical HTML in memory; direct file loading blocked by managed policy |
| Residual run and verifier | PASS | 56 case/arm rows,14 C/D paired cases;132 logged operations |

The sorter paper's1,184-test figure belongs to its earlier frozen run. It is not rewritten as the current1,186. Native JavaScript checks are not fresh current-Combined Chromium/WASM release or deployed-site tests; those were not run in this B-Tests refresh. The separately identified Portable browser probe was a real Chromium execution.

The old source-query entrypoint intentionally requires its original pin. The new `run_checks.py` defines an explicit new-version condition and calls the unchanged fixture/scoring function after independently verifying current HEAD and tracked cleanliness. Its raw `frozen_function_output.repo_pin` remains the function's historical constant; `evaluated_revision` records the actual new target. No frozen CLI guard was weakened and no old result relabeled.

The public-paper repeat uses the existing hash-pinned first-15-page texts and original concluding excerpt. The newly supplied full Ben paper is documentary input to the comparison matrix, not silently substituted into that frozen fixture. All full returned Answer dictionaries are retained. These are source-selection observations, not verified answers to every proposition.

## Native sorter evidence

The official `tools.evaluate_sorter` was invoked with `--reader-checkout` pointing to a genuine unchanged worktree at the pre-sorter pin. It compared all native ledger/answer Python file bytes before validation, show, gate and ask calls. Both source and node arrays were identical across modes; raw edges were an unchanged prefix. New edges were comparison-only. The source-read counter was2,804 bytes per mode across two passes of1,402 source bytes.

The exported snapshot was intact, retired, machine-origin and external=no. `validate` and `show` exited0. Native gate/ask exited3 as expected for lab, internal and external, with no supported claims. External policy is the first exclusion there, while lab/internal report retirement. The reports preserve per-command expected/actual exit codes and local cost observations. A supported answer cannot be inferred from a valid stored graph.

## Earlier-repository reproduction and limits

Portable commands ran on a Git-archive copy of the pinned public repository, preserving the source clone and its historical recorded results. Its scenario/browser scripts write new results only into the disposable copy; those new results were retained here. Browser requests remained empty. Managed Chromium blocked file://, so the script used offline in-memory set_content of the identical standalone HTML. Direct-file and physical-device transfer remain unverified.

The residual experiment's original scripts ran against their required unchanged November10 Combined pin. The verifier checked56 case/arm rows and14 paired C/D cases, fixture hashes and132 logged operations. The conventional reference gate matched native decisions on those authored cases. That is retained as a limit on uniqueness/superiority, not hidden as a negative for Mitchell. Raw/newest-history conditions are specified ablations, not all conventional systems. Reproduction today does not independently authenticate the original execution date.

## No target changes or new model trials

Only B-Tests is edited. All evaluated repositories retained clean tracked source before/after. Models were not invoked; native Ben controller access, independent READ/ACK, private benchmark originals, reciprocal blinded scoring, human maintenance/re-entry studies and independently adjudicated historical accuracy remain NOT_RUN or INCONCLUSIVE as specified in the [acceptance matrix](../../../docs/RESPONSE_TO_BEYOND_GUARDED_RETRIEVAL.md).

Current runs produced no target-code failure in the criteria above. Previous PR46 component socket failures and successful permission-only retries remain in the separate prior report. Their negative records were not erased or counted as new current failures. Relative cost advantages are not inferred from shared-host timings.

Some freezes retain local B-Tests candidate commit6d408dd; it was an unpublished evidence candidate based on public d935be6. Executable baseline modules match that public version, and each new evaluator's exact SHA is retained. The new evaluation script hashes and published tree, rather than assuming a local candidate hash is remotely fetchable, identify this experiment.

## Repeat

Run from B-Tests with the pinned clean public targets above, Python3.12 and Node. Permit localhost sockets for HTTP tests; install Playwright/Chromium only for the optional Portable browser probe. No model endpoint is needed. Use new output paths.

```sh
python -m research_lab.mplpb_native_suite --mplpb-root /workspace/mplpb --revision ccbb5804eb47f78c2338d57c142ad087b47be710 --out /tmp/current-native-repeat
python evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_checks.py --out /tmp/current-checks-repeat
python evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_components.py --out /tmp/current-components-repeat
python evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_extras.py --out /tmp/current-extras-repeat
python evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_frozen_papers.py --out /tmp/current-papers-repeat
python evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/run_predecessors.py --out /tmp/current-predecessors-repeat
```

From the pinned Combined checkout:

```sh
python -m tools.evaluate_sorter --reader-checkout /tmp/mplpb-reader-before-sorter --output /tmp/current-sorter-repeat
```

Prepare `/tmp/mplpb-reader-before-sorter` at3df2c6e and `/tmp/mplpb-residual-baseline257e` at257e54a, and clone both earlier repositories under `/workspace`; the scripts verify their exact pins. Extraction is not needed for `run_frozen_papers.py`: the retained public texts and SHA manifest are sufficient. Temporary absolute paths, timestamps and measured costs can differ. Frozen fixtures, target pins, profile decisions and content identities are the repeatable comparison.
