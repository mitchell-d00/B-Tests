# Five seeded d100 sorter runs

On 19 November 2026, B-Tests ran five fresh synthetic batches against
Combined MPLPB at
[`bbf6690d69b32d16969cc10e5ce9d380427ead40`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/bbf6690d69b32d16969cc10e5ce9d380427ead40).
The test harness was B-Tests revision
[`52cd9a95042d9fb34577e7a22d2fca1a45548283`](https://github.com/mitchell-d00/B-Tests/tree/52cd9a95042d9fb34577e7a22d2fca1a45548283).
Each batch used 25 separately built ledgers, four scenarios per ledger,
and 100 distinct web-sourced topic names. Topics can recur across
batches. The five samples covered 375 distinct topics.

## Results

| Batch | Seed | Cases passed | Workspace replays passed |
|---|---:|---:|---:|
| [01](batch-01/run/summary.json) | `9345879386501493789` | 100/100 | 100/100 |
| [02](batch-02/run/summary.json) | `13985914196358497236` | 100/100 | 100/100 |
| [03](batch-03/run/summary.json) | `2531403106825998858` | 100/100 | 100/100 |
| [04](batch-04/run/summary.json) | `16772941843601119137` | 100/100 | 100/100 |
| [05](batch-05/run/summary.json) | `12380574512768247101` | 100/100 | 100/100 |
| **Total** | **Five seeds** | **500/500** | **500/500** |

Each expected decision passed 125 times. Eligible originals supported
125 answers, competing owners led to 125 clarification outcomes,
processed-only material remained available for review in 125 cases,
and 125 eligible originals lacked enough evidence for a strict answer.
The review workspaces transferred no approval and used zero strict
proof slots. [Aggregate result](summary.json)

The runs used fictional records and a frozen catalog of topic names
and links. The evaluator checked the expected decisions and the native
replay status. The results measure software behavior on repeatable
synthetic inputs. They leave historical accuracy on unseen originals
and human review effort unmeasured.

## Reproduce all five batches

Use Python 3.12 and clean side-by-side clones of B-Tests and Combined
MPLPB. From the B-Tests checkout, set `TARGET` to the Combined checkout
and create a fresh output directory. The retained freezes record the
runtime version, code and catalog hashes, all packet hashes, and the
dice log hash.

```sh
set -eu
TARGET=../combined
REVISION=bbf6690d69b32d16969cc10e5ce9d380427ead40
REPLAY=$(mktemp -d)
test "$(git -C "$TARGET" rev-parse HEAD)" = "$REVISION"

number=0
for seed in \
  9345879386501493789 13985914196358497236 2531403106825998858 \
  16772941843601119137 12380574512768247101
do
  number=$((number + 1))
  batch=$(printf 'batch-%02d' "$number")
  python -m research_lab.sorter_random_batches prepare \
    --revision "$REVISION" --seed "$seed" --out "$REPLAY/$batch"
  python -m research_lab.sorter_random_batches run \
    --mplpb-root "$TARGET" --out "$REPLAY/$batch"
done
printf 'Replay output: %s\n' "$REPLAY"
```

The seeded generation check reproduced every recorded packet hash,
dice log, and evaluator key hash. On a new run, compare scenario
outcomes, citations, and replay status. Native artifacts and command
records may carry fresh timestamps or absolute paths.

Each `batch-XX` directory includes the original freeze and dice rolls,
the per-case summary and user log, and a replay index with the
original workspace, source-map, and command-receipt digests.
The commands regenerate the full packets, evaluator keys, ledgers,
workspaces, source maps, and command receipts in the output directory.
