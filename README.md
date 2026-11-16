# B-Tests — OOCC/CAD falsification harness

**Mitchell D. McPhetridge | Research diagnostics | November 2026**

This is my attempt to break the claims in Benjamin Gelhaus's OOCC, CAD and Functional Layers research. I am investigating whether continuity maps can become self-protecting interpretations: an **armored worldview engine**. That is a falsifiable hypothesis, not a result or a personal accusation. The most important distinction is between preserving a human-approved explanation and maintaining independently recoverable, correction-ready information state.

I test incorrect promoted maps, revoked permissions, fabricated causation, compressed-away failures, missing original evidence, misleadingly smooth answers, context exhaustion, and 10/100/1000-edge saturation. I also use the failure conditions Ben published in *No More First Dates With AI*, pp. 267–271, and the measurements he proposes in *OOCC: The Unified Intersection*, pp. 386–390.

## Verified local status

- 38 **authored development** black-box cases, each with a paper anchor, oracle, and source-byte hash where a source is supplied.
- 32 local evaluator and negative-control tests **pass** on this checkout. They test the scoring machinery, not the author's implementation.
- 38/38 actual native results are **NOT_RUN** without an approved, version-pinned executable adapter and independent state readback.
- No independent comparative study, production Android test, or prospective Functional Layers forecast is claimed as completed.

## Execute

```sh
python -m unittest discover -s tests -v
python -m tools.kill_harness --out evaluation/not_run.json
python -m tools.kill_harness --require-live --adapter 'python /path/to/authorized_oocc_adapter.py' --verifier 'python /path/to/separate_readback.py' --out evaluation/native.json
python -m tools.score_scaling /path/to/preregistered_paired_study.json --out evaluation/scaling.json
```

Without an adapter, `NOT_RUN` is the correct output and `--require-live` returns exit code 2. An adapter says what the system **claims** happened. A separately controlled verifier must inspect what **actually** happened. Passing these schemas alone does not certify independent verification.

See [docs/FALSIFICATION_PROTOCOL.md](docs/FALSIFICATION_PROTOCOL.md) for the falsifiers and source anchors, and [fixtures/kill_conditions.json](fixtures/kill_conditions.json) for exact development stimuli and expected outcomes.
