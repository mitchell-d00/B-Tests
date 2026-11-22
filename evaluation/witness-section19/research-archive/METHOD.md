# Method for the live judge replay

This exploratory replay uses all 140 cases in the supplied Witness-Independence
Experiment ZIP. Its frozen case manifest is
`a87a121bdeccbc6371ab1ca24751df4f0ca5c62bcc9974ae2a664e93a307c9dd`.
The dataset includes 100 planted failures and 40 correct controls. The simulated
actor's reports, receipts, and output files are the source material.

A pinned Qwen2.5-1.5B model rejudges the simulated actor in the artifact frame
(I0-model proxy) and as an independent reviewer (I2). A separate SmolLM2-360M
server uses the I2 criteria (I3). Each request has a fresh message list.
Each level receives all cases under both report-only and report-plus-state.
The same seeded batch order is used in every arm. The published prompt frames
are retained, with a compact case view and a constrained verdict-only output
format. The compact view preserves paths by alias, action and receipt facts,
digest agreement, final audit status, report claims, and source lineage and
bodies in the state arms. The full original exports are a separate prompt
format. I5 human adjudication is outside the automated replay.

The driver freezes its code digest, input manifest, model digests and exact
requests before it starts collecting model outputs. The demo key is already
published in the source archive. This is a local freeze and an exploratory
replay. The driver only reads case data and the manifest. The scoring step
uses the original key and unmodified scoring module after inference.
Each complete model arm has 140 verdicts. The archive keeps raw model
responses, the case-to-verdict mapping, source hashes and scorer output. It
reports the original deterministic I0, I1 and I4 controls alongside model arms.

## Reproduction

Extract the supplied ZIP and verify the original demo with
`python -m wie verify demo_run` from its root. The standard library is the only
Python dependency. Use Linux x86-64, Python 3.12 and the pinned llama.cpp
b12622 release and model weights listed in the B-Tests live replication
configuration. The driver currently resolves their names in
`/workspace/scratch/witness-model`, including `bin/llama-b12622/llama-server`,
`qwen.gguf` and `smol.gguf`. Those filenames and digests match the published
B-Tests weights. The inference server listens only on loopback.

```bash
python run_full.py /path/to/witness-independence-experiment/demo_run output
python score_live.py /path/to/witness-independence-experiment/demo_run output scored-run
```

The test probes decision quality on authored cases. Comparing I0 with I2 also
changes the evaluation frame. Comparing I2 with I3 changes family and model
capacity. Coverage is reported with E and F because abstentions lower measured
detection and can also lower false alarms. Dependence among generated templates
limits interpretation of inferential statistics.
