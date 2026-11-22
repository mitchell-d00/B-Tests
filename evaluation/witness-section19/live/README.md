# Witness-independence replication

Does increasing separation between an acting AI runtime and its evaluator
improve detection of incorrect execution claims without increasing false
alarms beyond a predeclared limit? This is a fixed 12-case exploratory pilot
of Section 19. Each case produces one live trajectory. All conditions evaluate
that same trajectory. A separately frozen eight-case follow-up uses a larger
local model and clearer action instructions to exercise the real write path.
Its results are summarized separately. See the [paper](../../../docs/paper/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.md),
[original archive audit](AUDIT.md), and [pilot report](REPORT.md).

## Conditions and evidence

| Condition | What runs |
| --- | --- |
| I0 | The acting model sees its own action, operation receipt and report in the continued conversation, and self-assesses against the rubric and evidence packet. |
| I2 | A new stateless inference request to the same model receives the same rubric and evidence, with no governing artifact, legacy memo or acting conversation. The inference server can reuse computations for identical token prefixes. There is no conversation or Memory in the I2 request. |
| I3 | A separately implemented rule evaluator assesses the normalized evidence packet without the governing artifact. I3’s heterogeneity comes from its implementation. |
| I4 | An external observer subprocess reads the actual source, policy and marker files. A deterministic checker compares its readbacks to the requested action and reported claim. |

The acting model requests one operation through a fixed JSON interface.
Only the broker can invoke the writer. The permitted operation is an atomic
replacement of one synthetic status file. Current permission is checked by
the writer. A tool subprocess can return an interrupted staging acknowledgment,
return a controlled I/O failure, or commit a file. In two prohibited-effect
cases a separate test-operator subprocess commits to the synthetic slot
despite the policy. Its trace is labeled `operator` and its effect must never
be attributed to the model. No files outside the fixture slot are targeted.
The model does not see the operator injection, fault settings, case labels,
expected results or oracle. It receives source records, the task, and its
operation receipt. It sees the common evaluator evidence only after its actual
report has been saved.

The predeclared oracle classifies *realized* cases using the authorized
action, expected final state and reported outcome. A false completion or a
false refusal is counted only if the model produces it. The prohibited-effect
control guarantees physically observable forbidden state through a test
injection. The study keeps both supported execution and correct refusal
controls. [Case design, rubric, thresholds, and exclusions](protocol.json)

I3, I4 and the oracle share the contract semantics. I3 has normalized
readbacks. I4 uses observations collected from the external slot. Their
scores demonstrate mechanically observable aspects of this particular
contract and cannot isolate evaluator separation from evaluator design.
Both observer and harness run under the same local OS account. Independent
external-state readback is implemented. Separate administrative trust and
third-party adjudication are outside this pilot.

OOCC is recorded as `OOCC_NOT_RUN`. This pilot neither activates the published
OOCC workflow nor supplies its ChatGPT Memory, authorized external sources
or source-governance procedures. MPLPB is `NOT_RUN` in this pilot. I1 and I5
are `NOT_RUN`. The neighboring archived probes may be examined separately.
[Earlier archival replay and native MPLPB probes](../RESULTS.md)

## Reproduce

Linux x86-64, CPU inference, Python 3.12 or newer, standard library only,
roughly 1.2 GB disk for downloaded assets, available loopback sockets, and
a workspace with write access. No model account or Google Drive credentials
are needed. Download and verify the pinned release and model before running.
From this directory:

```bash
set -eu
asset_dir="$(mktemp -d)"
output_dir="$(mktemp -d)"
curl -fL https://github.com/ggml-org/llama.cpp/releases/download/b12622/llama-b12622-bin-ubuntu-x64.tar.gz -o "$asset_dir/llama.tar.gz"
curl -fL https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf -o "$asset_dir/qwen.gguf"
printf '%s  %s\n' \
  194c0a81fe2be4a8316013b514c23d55431982178321add6d533b235133a01a3 "$asset_dir/llama.tar.gz" \
  6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e "$asset_dir/qwen.gguf" | sha256sum -c
tar -xzf "$asset_dir/llama.tar.gz" -C "$asset_dir"
python run.py --server "$asset_dir/llama-b12622/llama-server" --weights "$asset_dir/qwen.gguf" --out "$output_dir/live"
python score.py "$output_dir/live" --out "$output_dir/live/scores.json"
```

The follow-up uses the same CPU runtime and its own pinned weights and
protocol. It needs roughly 2.2 GB of additional disk for the model. Starting
from the shell above:

```bash
lock=profiles/follow-up.runtime.json
model_url="$(python -c 'import json,sys; print(json.load(open(sys.argv[1]))["weights_url"])' "$lock")"
model_sha="$(python -c 'import json,sys; print(json.load(open(sys.argv[1]))["weights_sha256"])' "$lock")"
curl -fL "$model_url" -o "$asset_dir/qwen3b.gguf"
printf '%s  %s\n' "$model_sha" "$asset_dir/qwen3b.gguf" | sha256sum -c
python run.py --protocol profiles/follow-up.protocol.json --runtime-lock "$lock" \
  --server "$asset_dir/llama-b12622/llama-server" --weights "$asset_dir/qwen3b.gguf" \
  --out "$output_dir/follow-up"
python score.py "$output_dir/follow-up" --out "$output_dir/follow-up/scores.json"
```

To verify the retained runs, extract each raw archive and use its frozen scorer. It checks content hashes,
reopens the saved external files, validates observer traces, and derives the
tables from the actual model responses and evaluator judgments:

```bash
verify_dir="$(mktemp -d)"
tar -xzf evidence/pilot.raw.tar.gz -C "$verify_dir"
pilot="$verify_dir/witness-section19-live-pilot"
python "$pilot/frozen/score.py" "$pilot" --out "$verify_dir/pilot.scores.json"
cmp "$verify_dir/pilot.scores.json" evidence/pilot.scores.json
tar -xzf evidence/follow-up.raw.tar.gz -C "$verify_dir"
follow="$verify_dir/witness-section19-live-follow-up"
python "$follow/frozen/score.py" "$follow" --out "$verify_dir/follow-up.scores.json"
cmp "$verify_dir/follow-up.scores.json" evidence/follow-up.scores.json
(cd evidence && sha256sum -c SHA256SUMS)
```

- `manifest.json` records the pre-run freeze time, hashed protocol and source,
  runtime digests and server arguments. It is a local freeze, without
  external preregistration.
- Each case’s `fixture.json` preserves evaluator-only settings. The
  `*.request.json` files hold the exact prompts, schemas and sampling options sent to the runtime.
  Response JSON and transport files preserve what the server returned.
- Each case’s `*.trace.json` files record actual subprocess commands, times,
  exit status, stdout and stderr. The `external/` directory contains the final
  files. The before/after state JSON preserves bytes and hashes.
- Each case’s `result.json` records the realized contract outcome and the verdicts.
  `scores.json` reports confusion matrices, E/F, paired deltas, per-class
  results and disagreements. Missing denominators are `null`.
- PASS/FAIL refer to the actual task contract. BLOCKED is an attempted run
  that cannot be scored under the frozen rules. NOT_RUN records an unavailable
  dependency. An evaluator's actual output is separately recorded as FLAG or
  ACCEPT.

The independent researcher may inspect the operator intervention and reject
or change the contract in a *new, separately frozen* study. CPU and runtime
differences can affect generation even at the recorded sampling settings.
The original ZIP is retained byte-for-byte. The frozen source bundle and
recorded observations can be scored without downloading model weights.

## Judge frozen declarations with a different model family

`judge.py` consumes a retained run directory, including the original
declarations, before/after readbacks, evaluator rubric, and predeclared oracle.
It freezes a digest of that run before it asks for judgments. I0 uses the
continued acting context, I2 receives only the rubric and evidence, and I3
receives the same fresh packet as I2 in a separate **SmolLM2** model process.
I4 rechecks the retained filesystem evidence and deterministic result.

Use `--reuse-i0-i2` to retain actual I0 and I2 responses already recorded on
the exact same packet. To generate both again, replace that option with
`--actor-weights "$asset_dir/qwen.gguf"` for the first pilot, or supply the
pinned Qwen 3B weights for the follow-up. Missing model inputs produce
`NOT_RUN` for the dependent levels.

```bash
lock=profiles/heterogeneous.runtime.json
model_url="$(python -c 'import json,sys; print(json.load(open(sys.argv[1]))["weights_url"])' "$lock")"
model_sha="$(python -c 'import json,sys; print(json.load(open(sys.argv[1]))["weights_sha256"])' "$lock")"
curl -fL "$model_url" -o "$asset_dir/smol.gguf"
printf '%s  %s\n' "$model_sha" "$asset_dir/smol.gguf" | sha256sum -c
python judge.py "$pilot" --out "$output_dir/judged-pilot" \
  --server "$asset_dir/llama-b12622/llama-server" \
  --other-weights "$asset_dir/smol.gguf" --reuse-i0-i2
python judge.py "$follow" --out "$output_dir/judged-follow-up" \
  --server "$asset_dir/llama-b12622/llama-server" \
  --other-weights "$asset_dir/smol.gguf" --reuse-i0-i2
```

Both archived rounds can be rescored offline after extracting the raw judgment
archives into the same verification directory:

```bash
for round in pilot follow-up; do
  tar -xzf "evidence/judges-$round.raw.tar.gz" -C "$verify_dir"
  judged="$verify_dir/witness-judges-$round"
  python "$judged/frozen/judge.py" "$verify_dir/witness-section19-live-$round" \
    --out "$judged" --rescore > "$verify_dir/judges-$round.scores.json"
  cmp "$verify_dir/judges-$round.scores.json" "evidence/judges-$round.scores.json"
done
```

The rule-based I3 remains in the original pilot records. The judge-only replay
uses the different-family I3 in its own score files. Both reuse the original
fixed thresholds and ground truth. Inputs, recorded answers, exclusion
decisions, and matched denominators are available in each archive.

The [tool controls](evidence/tool-controls.summary.json) exercise the
subprocess writer, including a permitted commit and an independently
observed file. They have their own [raw records](evidence/tool-controls.raw.tar.gz)
and are excluded from model scores. Repeat them with
`python check_tools.py --out "$output_dir/tool-controls"`.

## Case generator and model-window export

Generate a repeatable set before any actor or judge sees it. The seed shuffles
the fixed templates and assigns opaque case IDs. Additional rounds are
dependent repeats of those templates.

```bash
python handoff.py generate --seed 19226 --rounds 1 --out "$output_dir/frozen-cases"
# Pass --protocol "$output_dir/frozen-cases/protocol.json" to run.py.
python handoff.py export "$pilot" --out "$output_dir/window-packets"
```

Extract the [ready-made pilot and follow-up packets](evidence/window-packets.tar.gz) or export your own. Paste one `*.prompt.txt` into each fresh evaluator window. The I2 window
should use the acting model at the same settings. I3 must use a different
model family. Each window receives the same packet. Keep the answer key and
original acting context out of both judge windows. Record each actual
response as `replies/I2/<case>.json` or `replies/I3/<case>.json`, using this
shape:

```json
{
  "packet_sha256": "<digest for that case from pack.json>",
  "fresh_context": true,
  "model": "<exact model and version used>",
  "model_family": "<model family used>",
  "response": {"verdict": "<FLAG or ACCEPT>", "reason": "<verbatim reason>"}
}
```

```bash
python handoff.py score "$pilot" --packets "$output_dir/window-packets" \
  --replies "$output_dir/replies" --actor-family Qwen2.5 > "$output_dir/window-scores.json"
```

The scorer verifies frozen packets, requires model identity and fresh-context
attestation for pasted answers, and marks missing answers `NOT_RUN`. The
deterministic I0 adapter reuses the acting AI's actual self-judgment. I1 is a
deterministic same-frame receipt comparator that sees the records the actor
used, including its operation receipt. It cannot reopen the output slot.
I4 independently checks external state. The scorer reports each level’s
E/F, confusion matrix, and measured versus missing cases. The I1 comparator
is a reference condition in this workflow. A separate same-frame model
assessment remains outside the measured pilot.
