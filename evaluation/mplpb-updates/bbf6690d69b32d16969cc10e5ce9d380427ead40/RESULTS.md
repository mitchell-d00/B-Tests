# B-Tests rerun for Combined MPLPB PR52

Run date **18 November 2026**. Combined revision
[`bbf6690d69b32d16969cc10e5ce9d380427ead40`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/bbf6690d69b32d16969cc10e5ce9d380427ead40).
The native commands ran against a clean checkout. These were development tests
on public and synthetic inputs. No model requests were made.

## Native, historical, and repository-documentation runs

| Check | Result |
|---|---|
| [Native suite and seven additional commands](native/summary.json) | 1,267 Python tests passed. UI script, browser transport, JavaScript API, crawler worker, repository infrastructure, handoff and five-instance recovery passed. |
| [Focused sorter, candidate workspace and witness admission](native/focused-workspace.log) | 81 tests passed. |
| [Work-boundary probes](native/work-boundaries/) | Seven passed. The allowed local operation produced the expected effect and all six prohibited cases produced none. |
| [Public evidence controls](native/public-evidence.json) | 52 passed, with zero false-supported links observed in these controls. |
| [Isolated wheel check](native/wheel-workspace.json) | Installed artifact reproduced the workspace and preserved strict support and approval boundaries. |
| [Direct historical replay](historical/native-comparison.json) | All 22 decisions, exact citations and missing-information lists matched the frozen baseline. The totals were 2 complete, 1 partial, 3 conflicts and 16 abstentions. H05 kept four source passages. |
| [Public-source candidate workspaces](historical/workspace-cases.json) | Five replays retained 39 displayed processed passages, 15 exact-match candidates and 49 wording-review candidates. Exploration charged zero strict slots. |
| [MPLPB repository documentation sorter](repository-sorter/compare.json) | Eight Markdown inputs, 491 observations, 555 observation edges and 54 additional review links. The original-byte replay passed. Phrase-key, token and repeated-group limits were reached. |

## Mixed processed dumps

The [fresh mixed-dump rerun](mixed/summary.json) passed all five users.
Each had a separate ledger. The [user source maps](mixed/) cover 19 passed-in
files, 60 extracted statements and 11 candidate links. CSV and JSON inputs
were outside the supported sorter formats and appear in the maps as excluded.
The strict decision held for every user at both exploration budgets.

The first mailbox check expected an exact-match candidate from a CRLF
export. The [original workspace](mixed/initial-crlf-workspace.json) instead
shows a wording-review candidate because the extracted span includes a
trailing CRLF. The revised fixture keeps that source, checks its wording class,
and adds a separate literal-copy positive control. The
[initial passing run](mixed/initial-passing-summary.json) and the
[first final run](mixed/first-final-summary.json) remain inspectable alongside
the fresh rerun.

## Randomized d100 batch

The final [100-case result](d100/summary.json) passed all **25 separately built
ledgers**. Each ledger ran four scenarios in randomized order. Across the five
sets, there were 25 supported answers, 25 competing-owner decisions,
25 processed-only cases and 25 cases with an eligible owner whose original
lacked answer support.

- [Frozen inputs](d100/freeze.json) record seed **502548331403503517**, the
  target pin, catalog and generator hashes, and every packet file hash.
- [d100 charts and rolls](d100/d100-rolls.json) record 748 rolls used to choose
  the topics and assignments. The same seed recreated every packet and roll.
  A new seed produced a different selection.
- [Per-case source maps and workspaces](d100/cases/) retain all 100 final
  classifications and their source spans. [Replay checks](d100/replays.json)
  record successful native replay for each case and the original receipt hash.
- [Pilot runs](d100/pilots/) retain the progression from fixed test question
  labels to web-topic question labels and the d100 run that preceded the
  final target-freeze format. All three pilots completed 25 ledgers each.
  Their recorded code and input hashes refer to those earlier executions.

The generator uses Wikipedia topic names and URLs for variety. The exercise
records are fictional and the operator key is outside the native input
packets. The five roles are scripted users. Historical event accuracy and
human workflow outcomes require independent unseen sources and review.

## Reproduce

From B-Tests, use a clean checkout at the Combined revision above and a
fresh output directory for each run.

```sh
python -m unittest discover -s tests -q
python -m research_lab.mplpb_native_suite --mplpb-root ../combined --revision bbf6690d69b32d16969cc10e5ce9d380427ead40 --out /tmp/mplpb-pr52-native
python -m research_lab.sorter_mixed_users --mplpb-root ../combined --out /tmp/mplpb-pr52-mixed
python -m research_lab.sorter_random_batches prepare --seed 502548331403503517 --out /tmp/mplpb-pr52-d100
python -m research_lab.sorter_random_batches run --mplpb-root ../combined --out /tmp/mplpb-pr52-d100
```

The full native suite needs localhost sockets for its HTTP fixtures. The
historical run used the checkout’s Bubblewrap-isolated
[`tools.sorter_first_study`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/bbf6690d69b32d16969cc10e5ce9d380427ead40/tools/sorter_first_study.py)
direct arm, followed by native workspace execution and the original-span
comparison. [Upstream commands](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/bbf6690d69b32d16969cc10e5ce9d380427ead40/evaluation/candidate-review-workspace/2026-11-18-runtime/REPORT.md#reproduce)
