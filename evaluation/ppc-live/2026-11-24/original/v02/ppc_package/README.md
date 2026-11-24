# Probabilistic Polite Compliance — companion package v0.2

Paper by Mitchell D. McPhetridge; companion implementation AI-assisted, pending author review. Python 3.10+, standard library only. No network required for offline mode.

## Run

    python -m unittest -v
    python run.py --mode fixture --out results/replay.json

Fixture mode uses deliberately authored proposals, NOT model outputs. It reproduces the logical failure pattern and verifies a bounded gate, not the historical chat or an empirical model failure rate. A/B fixtures are illustrative, not estimated probabilities. The gate uses evaluator-owned synthetic evidence labels; it does not authenticate arbitrary real-world evidence. It protects only the represented state-write path, not prose or external effects.

## Fresh experiment (optional, NOT RUN in delivered results)

Use an OpenAI-compatible chat-completions endpoint (local or remote), with an explicitly chosen model. Set MODEL_API_KEY if needed. Remote use transmits synthetic prompts to that provider and may cost money.

    python run.py --mode live --endpoint http://localhost:11434/v1/chat/completions --model YOUR_MODEL --repeats 30 --out results/live.json

A and B use matched synthetic records and different system instructions. C applies a gate to the identical B proposal (paired intervention). Each case starts a fresh message history; selected cases include an actual correction exchange. Seed randomizes case order, not model generation. Raw responses, prompts, errors, model IDs and outcomes are retained. Invalid responses are separate from refusals; C fails closed. The endpoint must support the specified schema and temperature parameter. No native OOCC or MPLPB comparison is implied. A live run is a structured decision experiment, not a full free-text conversational replication. Independent review of raw outputs, correction acknowledgment, and semantic fidelity is required; self-reported acknowledgment is not proof. No claims of statistical significance are made.

## Paper crosswalk

- Sections 2–3: identity, execution, comparison and recurrence fixtures; partial trace excerpts.
- Section 4: history positive/negative pair.
- Section 5: gate, malformed inputs and bypass pair; positive controls expose false refusal.
- Section 6: supplied offline-run archive, preserved unchanged; not re-executed here.
- Sections 7–8: comparison pair; native systems NOT_RUN.
- Section 9: education pair tests evidence admission, not learning effectiveness.
- Section 10: A/B/C harness, 14 matched cases, seven families; fresh model run optional.
- Section 11: limitations above; full historical transcript and independent source reconciliation outstanding.

## Evidence status

The paper is preserved from the supplied text with formatting changes only. `evidence/trace-excerpts.md` is incomplete and contains retrospective statements, not an independent witness. `evidence/reported-offline-runs.zip` is the supplied developer archive, not a new execution. The supplied archive README reports 72/72 and 148/148 and 20/20 repeats (0.609–0.732 s), zero unclosed-database warnings, and unresolved original cutoff. This is consistent with the paper's reported figures, but not independent verification. Before publication: obtain full original chat export, hash it, redact a separate public copy, have independent reviewers annotate original turns against the paper's claims, reconcile companion references and run the live protocol. Preserve failures, invalid responses and missing records.

## v0.2 execution update

The original paper body is preserved; Appendix A adds current results. Original fixture artifacts and historical evidence are retained. New results: five unit tests passed, 30 deterministic fixture repeats (1,260 rows), and 11,192 synthetic gate checks with zero mismatches. Run `python stress.py` from the package directory to reproduce. The live model and native architectures were not executed. See HANDOFF.md for continuation. The previous statement that the paper was preserved with formatting changes only describes v0.1, not this appendix.
