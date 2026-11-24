# Reproduce the fresh instance

The original v0.2 companion is in `original/v02/ppc_package`. The earlier ZIP is preserved under `original`. Verify `SHA256SUMS` from the replication root and the original checksum manifest from inside the v0.2 directory. The frozen protocol is in [PROTOCOL.md](PROTOCOL.md). Python 3.10 or later and the standard library suffice to rescore the results. Local live execution uses a Linux x86-64 CPU build of llama.cpp, Qwen GGUF weights, Bash, curl and SHA-256 utilities. Native replication requires Git and the pinned MPLPB checkout.

## Rescore offline

```sh
sha256sum -c SHA256SUMS
python score.py --package original/v02/ppc_package \
  --frozen live/frozen.json --traces live/trials.jsonl.gz --out rescored
cmp rescored/summary.json scored/summary.json
cmp rescored/correction-texts.json scored/correction-texts.json
```

The trace file preserves lossless HTTP envelopes, message histories, response IDs and errors. The scorer reconstructs the scheduled cases and messages, checks the response bodies, then calculates strict JSON outcomes and the paired gate effect. It creates a new directory.

## Run a fresh live trial

Use the exact releases and paths in [asset-provenance.json](asset-provenance.json). Cache the model and llama.cpp binary before disconnecting. The shell example below fetches public artifacts only. During the actual experiment, requests go to loopback.

```sh
mkdir assets
curl -fL https://github.com/ggml-org/llama.cpp/releases/download/b12622/llama-b12622-bin-ubuntu-x64.tar.gz -o assets/llama.tar.gz
curl -fL https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf -o assets/qwen.gguf
printf '%s  %s\n' 194c0a81fe2be4a8316013b514c23d55431982178321add6d533b235133a01a3 assets/llama.tar.gz | sha256sum -c
tar -xf assets/llama.tar.gz -C assets
bash run-local.sh assets original/v02/ppc_package fresh-run
```

For a fully disconnected rerun, use the separate optional `ppc-local-qwen-assets.tar` delivered with the experiment. It contains the exact public llama.cpp release archive and GGUF weights listed in the provenance record. Check its companion SHA-256 file, extract it into `assets`, then unpack `assets/llama.tar.gz` and run the same command. The model assets are large and distributed separately from the GitHub experiment archive.

The shell runner checks the server binary and weights. The earlier B-Tests asset record lists a one-slot server profile. This trial uses four slots as recorded in the protocol, shell runner and server log. Seed 42 orders cases only. Fresh stochastic outputs can differ.

## Run the separate B-Tests native check

The experiment includes a verified, sparse Git checkout of the exact pinned MPLPB commit with the three runtime packages used by this test. It has no remotes and omits unrelated source blobs and history. The archived B-Tests runner also works with a full checkout of the same commit. In either case it rereads SQLite and marker files after the worker exits.

```sh
tar -xf offline-mplpb-native.tar.gz
python native.py --mplpb offline-mplpb --out fresh-native
```

To use the full source from GitHub instead:

```sh
git clone --filter=blob:none https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages.git mplpb
git -C mplpb checkout --detach e3990bf98ac6fb2e3b991a2eb251347ca571e873
python native.py --mplpb mplpb --out fresh-native-full
```

Use `native/summary.json` for the original result, and each case directory for the process record, actual ledger, SQLite database and marker evidence.

## Review the correction responses

```sh
python review_sample.py live/trials.jsonl.gz review-copy
```

Give only `review-copy/packet.json` to the reviewer. Keep its join key with the evaluator until labels are returned. See [the rubric](CORRECTION_REVIEW.md).

## Reproduce the fixture controls offline

Copy the v0.2 directory before running stress.py because it writes a relative results path that already exists in the original.

```sh
cp -R original/v02/ppc_package fixture-copy
cd fixture-copy
python -m unittest -v
python run.py --mode fixture --repeats 30 --out results/fixture-reproduced.json
python stress.py
```
