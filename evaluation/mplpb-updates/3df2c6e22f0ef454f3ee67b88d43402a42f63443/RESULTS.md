# Updated MPLPB against B-Tests — 17 November 2026

Evaluated MPLPB: [`3df2c6e22f0ef454f3ee67b88d43402a42f63443`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/3df2c6e22f0ef454f3ee67b88d43402a42f63443), PR #46 merge. B-Tests baseline: `d935be6c68c82388d932d99674568a7b7dbf5ff9`. Both public repositories were fetched and checked out at these exact revisions. No MPLPB source file was changed. Earlier frozen results and defaults remain unchanged.

## Executed results

| Check | Observed result | Evidence level |
|---|---|---|
| Complete current MPLPB Python suite | 1,157 tests PASS | Native repository development tests |
| UI script, browser transport, JavaScript API, crawler worker, source infrastructure, committed handoff, five-instance recovery | Seven commands PASS | Native checks/local demonstration; not new browser or model efficacy |
| Existing seven work-boundary probes | Seven PASS | Actual adapter effect and separate event-count observations |
| Existing ten applicable legacy source-query fixtures | Ten PASS_CONTRACT | Native CLI on unchanged authored fixture/scoring logic, explicitly retargeted |
| Six instruction-only legacy cases | OUT_OF_SCOPE for native strict reader | Not counted as MPLPB failures or passes |
| Public-paper strict-reader queries | Six return, five ambiguous, one not_in_corpus | Whole-source selection, not proposition truth certification |
| Public 52-case evidence evaluation | 52 pass; no reported capability gaps or regressions | Native authored public developer evaluation |
| Original-paper crawl | Four expected originals reached, three stages passed | Native source-linked documentary observations |
| B-Tests laboratory suite | 121 tests PASS | Harness tests, not 121 native target trials |
| Historical native-evidence replay | PASS | Rechecks public retained records; zero new target executions |

`summary.json` indexes the machine-readable results. Full inputs/versions, stdout/stderr and native outputs remain in the subdirectories. The seven boundary probes cover contradictory propositions, claim-only chains, a supported positive control, revoked seats, changed sources, missing originals after cold reopen, and human exports lacking evidence. The valid control invoked a real local adapter; the six rejection cases did not. Source/capability checks remain bounded, not universal error detection.

The 12 complete paper-query records match the previous PR #43 implementation (`614b18cc34f5270d4cb7dfbbf8239391a9f83b31`) after excluding only the temporary ledger root. Their native Answer still lacks `answer_supported`; absence is not true. The France question remained not_in_corpus. The named original-record phrase merely routes to the public paper discussing it; that does not test the referenced private benchmark.

The original-paper crawl verified four byte-pinned public source documents, recorded 31 checked documentary observations, traversed six declared relations and retained 15 unresolved relations. It ended with `answer_supported:false` and `truth_verified:false`. Documentary observation is not historical truth or general answer completeness.

## Component results and retained environment failures

Smart Local passed 52 tests; Swarm passed 145; Networked passed 61 after retry; Image passed 93 after retry. Local Mirror validation and five native seal/adoption checks passed. Component commands were read from the current published `tools/check_parts.py`; the root suite was omitted here because the separate full native run already covered it. This is a component-only execution, not a claim the entire official aggregate command ran.

The initial component run was launched without local network permission. Networked had one HTTP socket-setup PermissionError; Image had four such setup errors. Their raw command statuses remain FAIL in `components/`. With networking permitted, the unchanged Networked and Image suites passed in `networked-retry/` and `image-retry/`. Only execution permissions changed. These are demonstrated environment blockers, not established target-code regressions. Initial successful tests and repeated successful suites do not add independent coverage. Image also emitted warnings from intentionally malformed EXIF fixtures, retained in its logs.

## What changed since the earlier paper run

PR #44 added a public original-record challenge and prose inspection path. PR #45 added source-bound documentary checking. PR #46 added bounded reconstruction and solo-work support. Source changes include documentary units and exact offsets, an independently re-reading finite statement checker, reversible prose relationship proposals, literal source comparisons, question-part evidence display, bounded content parsing caches and host-side local-artifact byte checks. The current native suite exercised reconstruction and solo-work tests, including source changes, conditional/quoted assertions, event separation and artifact mutation.

The reconstruction documentation reports limited complete-answer classes and unresolved obligations. Those published original-record aggregate performance numbers were not separately rerun here and are not inherited as new B-Tests findings. The unchanged public-paper strict-reader probe does not measure every new reconstruction capability.

## Version and scoring safeguards

`research_lab.mplpb_native_suite` has an explicit `--revision` parameter, used with this new pin. Its historical default remains unchanged. The native boundary worker likewise accepts the evaluated revision explicitly.

The legacy CLI entrypoint deliberately rejects revisions that differ from its frozen November 10 protocol. This update does not weaken that check. `run_checks.py` defines a separate new-version condition, verifies the new HEAD and clean tracked source, and reuses the unchanged `run_mplpb` fixture/scoring function. That historical function stamps its constant old pin in raw metadata; this is retained verbatim under `frozen_function_output`, while `evaluated_revision` independently records the actual new checkout. The old metadata must not be read as evidence that the historical checkout was executed in this condition. Fixture and evaluator hashes are frozen before execution.

No new OOCC/CAD or conventional AI sessions were executed. Native Ben controller operation, private source packages, recipient acceptance, real AI READ/ACK, independent external readbacks, human maintenance costs, and reciprocal blinded scoring remain NOT_RUN. A replay of old sessions is not a new model experiment. These runs establish bounded contract behavior, not a global architectural victory or general historical accuracy.

## Repeat

Use the exact public checkouts above; run from B-Tests with Python 3.12, Node and, for extraction, PyMuPDF 1.26.6. Permit localhost sockets. Use fresh output/ledger paths and preserve failures. The executed scripts and freeze files record exact commands. Native model calls: zero.

```sh
python -m research_lab.mplpb_native_suite --mplpb-root /workspace/mplpb --revision 3df2c6e22f0ef454f3ee67b88d43402a42f63443 --out /tmp/update-native-repeat
python evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_checks.py --out /tmp/update-checks-repeat
python evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_components.py --out /tmp/update-components-repeat
python evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/run_extras.py --out /tmp/update-extras-repeat
python evaluation/public-papers/run.py --mplpb-root /workspace/mplpb --ledger /tmp/update-paper-ledger-repeat --output /tmp/update-papers-repeat
```

The paper command additionally uses the attached public PDFs/TXT staged at `/workspace/attachments`; extracted text hashes and complete source identities are retained. The separate `retry_component.py` can rerun an environment-blocked Networked or Image suite with networking permitted. Native task IDs, questions and frozen fixtures are unchanged. Wall times, temporary paths and OS scheduling are not deterministic and do not establish an efficiency advantage. Independent human-review time and monetary computation cost were not measured.
