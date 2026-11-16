# Side-by-side: published CAD instruction method vs pinned MPLPB strict reader

Last reviewed: 16 November 2026. This is the legacy development comparison.
Use the [targeted correction study](../docs/OOCC_CORRECTION_EVALUATION.md) and
[execution report](../docs/OOCC_CORRECTION_RESULTS.md) for the new OOCC hypothesis.
No usable model completions were obtained in its local or first CI attempts.

I am evaluating *what actually happens* under adversarial original-source conditions. I am not modifying either target to make it pass.

The shared source-query cases SH01–SH10 exercise the pinned, unmodified MPLPB strict reader **as executable code** and compare with fresh AI sessions given Ben-derived CAD instructions or a strong ordinary governance prompt. Cases CAD11–CAD16 are instruction-only: I do **not** count an MPLPB strict-reader refusal on a general historical-causation/agent-action task as a defect. Each arm receives exactly the same fictional sources. The source governance prompts differ; the facts and questions do not.

The CAD rules are an annotated, bounded interpretation of Gelhaus (2026), *Continuity, Authority, Directive*, sections 3–7, 12–13, *Artificial Tangibility*, sections 6, 8–10, and *No More First Dates With AI*, chapter 52 and Build Unit 7. This is a test of that **published instruction method**, not a reproduction of unseen private controller code. Ben's own wording should be tested as another frozen treatment when a precise versioned instruction packet is provided.

The historical pin is MPLPB commit `257e54a51edac272eb6b2441457f38a40485ee4d`.
The runner now verifies the acquired executable-package bytes against retained
upstream Git blob hashes, rather than trusting HEAD alone. This supports a verified
partial snapshot and rejects dirty executable packages. All 16 fixtures are
**development material**, not independently blinded holdouts. This version is not
the updated MPLPB implementation linked in the new study.

## Real runtime commands

```sh
# Place an unmodified clone of the pinned source outside the B-Tests repo.
git clone https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages.git /tmp/mplpb-pinned
git -C /tmp/mplpb-pinned checkout 257e54a51edac272eb6b2441457f38a40485ee4d
python -m unittest discover -s tests -v
python -m side_by_side.run --mplpb-root /tmp/mplpb-pinned --out evaluation/paired_mplpb.json
```

### AI arm

A model adapter command reads *one JSON object per invocation* from stdin, with `system` (the frozen CAD or strong-baseline instruction), `user` (the same original source pack), and `fresh_session=true`. It must call the selected real AI model in a new session and output `{"decision":"ANSWER|REFUSE|CONFLICT","answer":"...","evidence_ids":["S1"],"missing":"...","next_action":"..."}` as JSON to stdout. No model result is scored without an actual model invocation. Make sure your command does not read prior calls. Set the model name, provider/version, sampling parameters and limits in the separate audit record.

```sh
python -m side_by_side.run --mplpb-root /tmp/mplpb-pinned \
  --model-command "python /secure/location/your_actual_model_adapter.py" \
  --out evaluation/paired_live.json --require-live
```

No API credentials are provided by this repository. If `--model-command` is absent, both AI arms report `NOT_RUN`, not failure or success.

## Interpretation

Model replies that meet the label/substring contract remain `INCONCLUSIVE` pending
independent semantic review; they no longer receive a pass from those fields alone.
Original requests and adapter stdout are retained. SH05's agreeing-source ambiguity
is a strict MPLPB ownership rule, not a general factual contradiction. SH07's
tamper metadata is also represented differently at the AI and native interfaces.
These legacy cases must not be treated as an independently matched reasoning study.

A source-supported claim, a good refusal and a correct conflict are different results. Exact field grammar is a declared MPLPB boundary. The CAD instruction method has broader proposed semantics; that breadth needs actual live model testing and independent grading to support a performance claim. False source promotion, causal overreach, loss of rejected mistakes through compaction, and unsupported stop receipts are specifically tested in CAD11–CAD16. A text response alone never certifies a real state mutation.

The CLI outputs individual observed replies, exact branch pin, fixture hash and errors. Do not infer independent experimental superiority from the results on authored fixtures.
