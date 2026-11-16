# Native MPLPB comparison — 16 November 2026

This is a new execution of the full unmodified Combined MPLPB checkout, not a source-only review. It does not reproduce Ben Gelhaus's private E0–E5 fixtures. The tested versions are:

- Historical: [`257e54a51edac272eb6b2441457f38a40485ee4d`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/257e54a51edac272eb6b2441457f38a40485ee4d), the pin identified in his excerpt, committed 10 November.
- Current: [`cc21ce300b5ec228c07fc77a149804fba6c89792`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/cc21ce300b5ec228c07fc77a149804fba6c89792), merged 15 November.

## Full suite and component checks

The current native Python suite passed **887 tests**, followed by seven successful commands: UI script, browser transport, JavaScript API, crawler worker, repository infrastructure, committed handoff validation, and the five-instance specialist-recovery demonstration. These JavaScript commands do not constitute a physical browser/device or new neural inference test.

The official component checker also passed: Smart Local **52**, Swarm **145**, Networked **61**, Image **93**, and five seal/adoption checks. It repeated the Combined 887; that repeat adds no unique coverage. The component checks concern the bundled versions. Swarm uses the retained complete archive described in `parts/README.md`, not an assertion that every file layout of the upstream default tree passes unchanged.

The five-instance demonstration used real native state, a fresh successor subprocess, a retained contested claim and failure, denied use of an ended writer, revisions and receipt-backed completion. It ended with a supported-under-scope claim, task done, a verified 24-event chain and `answer_supported:false`. These are coordinator operations, not five live AI agents or factual truth certification.

[Raw logs, command freezes, results and hashes](../evaluation/mplpb-native). The full suite took 288.697 seconds; component checking took 331.269 seconds, including its Combined repeat. Per-command elapsed times are retained. No target code was changed. Model calls: zero. Human-review time was not independently measured.

## Seven paired boundary probes

The same synthetic source says: `Configuration AX-14 is discontinued. Component X remains available.` A local executor writes an effect file if invoked. Separate read-only SQLite event counts and effect-file inspection distinguish native rejection from language saying an action is blocked. Credentials and databases are excluded from publication.

| Frozen criterion | Historical pin | Current pin |
|---|---|---|
| Wrong claim “Component X is discontinued” cannot enable work | FAIL: executor ran | PASS: no effect, no new event |
| Claim-only agreement cannot replace direct evidence | FAIL: executor ran | PASS: no effect, no new event |
| Supported original permits the local positive control | PASS: executor ran | PASS: executor ran |
| Revoked seat cannot execute | PASS | PASS |
| Changed source cannot enable old work | PASS | PASS |
| Missing original after cold reopen cannot enable work | PASS | PASS |
| Export without pinned evidence cannot be promoted as supported | PASS | PASS |

These are seven authored cases on each revision, not population error rates. Historical FAIL means violation of this frozen probe criterion; it does not retroactively add a general semantic checker to that version's declared scope. The two old failures are retained. They are not attributed to Ben's private experiments without his actual inputs and outputs. The later repair cannot retroactively establish an older pass.

Current source support is a finite status-language check. Unsupported language requires rechecking. It does not detect every uncited contradiction or an intact false original. A hash and human promotion do not establish outside-world truth.

## Reproduce native executions

Use clean full Git checkouts and new output directories. Python 3.12 and Node 24 match the retained run. Localhost sockets must be permitted. No model endpoint is needed.

```sh
git clone https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages mplpb-current
git -C mplpb-current checkout cc21ce300b5ec228c07fc77a149804fba6c89792
git clone https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages mplpb-old
git -C mplpb-old checkout 257e54a51edac272eb6b2441457f38a40485ee4d
python -m research_lab.mplpb_native_suite --mplpb-root mplpb-current --out evaluation/blind-private-runs/native-repeat
python -m research_lab.mplpb_parts_suite --mplpb-root mplpb-current --out evaluation/blind-private-runs/parts-repeat
python -m research_lab.mplpb_seam_probe run --old-root mplpb-old --current-root mplpb-current --out evaluation/blind-private-runs/seams-repeat
python -m research_lab.native_evidence
```

The last command only replays retained public results; it does not run the target. Native CI runs the preceding kinds of checks on pinned repositories.

## Blockers and harness defects retained

The initial restricted execution reported 875 tests, three failures and nine errors. Localhost socket creation was denied; HTTP setup errors also broke dependent researcher journeys. After permitting networking, the 17 affected tests passed, then the unchanged full suite passed all 887. The initial FAIL log remains; its cause is environment restriction, not an established MPLPB defect.

Two preliminary probe attempts used an invalid harness context-policy hash and completed no target criteria. A later added cold-reopen case hit a harness `str.unlink` error, corrected to `Path(...).unlink`; two conditions were NOT_RUN. All setup attempts are catalogued in `harness-setup-attempts.json`. Only evaluator defects were repaired. Preliminary completed five-case pairs are retained alongside the final seven-case run. None is counted as independent replication.

## Chronology

See [dated ecosystem sources](MPLPB_CHRONOLOGY.md). Earlier code already had bounded answering, relations and continuity. The newer source-semantic guard is a later change. This review does not infer why Ben selected his historical pin or claim all of his proposed extensions were already solved.
