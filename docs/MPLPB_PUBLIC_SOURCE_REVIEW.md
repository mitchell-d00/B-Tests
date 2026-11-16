# Focused review of current public MPLPB

Inspected revision: [`cc21ce300b5ec228c07fc77a149804fba6c89792`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/cc21ce300b5ec228c07fc77a149804fba6c89792), 16 November 2026.
The complete Git tree contained 2,016 entries. Forty-eight relevant public files
were acquired and verified against their Git blob identities; the
[manifest](../research/mplpb-method-audit.json) also records SHA-256 identities.
This is a focused static review, not an exhaustive reading of every file or a
fresh execution by itself. Subsequent [native executions](MPLPB_NATIVE_COMPARISON.md) ran the complete pinned checkout and bundled component checks; reported historical results remain separate.

## Concrete mechanisms inspected

- `mplpb_combined/record.py`, `ledger.py`, `provenance_gate.py`, `reader.py` and
  `retrieval.py`: identities, hash pins, origin/depth, derivation, supersession,
  eligibility and retrieval distinct from supported answering.
- `mplpb_answers/pipeline.py`, `evidence_contract.py`, `support.py`,
  `relation_graph.py`, `operational_evidence.py`, `procedures.py`, `local_reader.py`:
  finite source-language proof paths, qualifications, partial/conflict/refusal
  diagnostics, and probabilistic assisted reading that stays unsupported as a
  deterministic answer. Current documentation describes fourteen relation families.
- `mplpb_work/source_support.py`: `work-source-status-v1`, a finite unconditional
  status checker. It requires exact subject/polarity support from directly pinned
  source quotes, examines the cited full body, contests opposing assertions and
  returns `needs_recheck` for assumptions, unsupported language or unresolved context.
- `mplpb_work/store.py`, especially `_source`, `_effective`, `_permission`, `_view`,
  `handoff`, `_validate_record` and `execute`: current source loading, revisable
  assessments, dependency rechecks, capabilities/fencing, work-state projections,
  receipt-backed completion and fresh dispatch checks. Claim-only agreement is
  explicitly not direct source support. Handoffs include `answer_supported:false`,
  `content_truth_verified:false` and checker-specific support status.
- `tests/test_specialist_continuity.py`: stored regressions for pre-challenge
  contradiction blocking, old claimed support being recomputed, claim-only chains,
  negation/scope, altered source invalidation, independent roots, stale receipts,
  task contract substitution and authentic host-boundary restrictions. Inspection
  of these assertions is not a new test run.
- `evaluation/no-unverified-promotion/`: retained baseline failures, fixed-contract
  results, domain-specific exceptions and limits of the proposed general principle.
  The report classifies it as an existing principle expressed in MPLPB terminology,
  not an independently validated new law.

## Ben's proposed acceptance criteria against the current public implementation

| Criterion in supplied Beyond Guarded Retrieval excerpt | Relevant public mechanism | What remains unestablished here |
|---|---|---|
| Preserve source authority | Native eligibility, pins, supersession, delivery profiles | No fresh replay of his E0–E5 originals |
| Honest refusal diagnostics | Answer contract separates unsupported grammar, missing eligible passages, conflict, clarification and budget states | Diagnostic quality on his unavailable cases |
| Exact fields without false pruning | Unique source-ID/hash matching and separate passage routing | Complete held-out exact-identifier benchmark and contradictory-match recall |
| Distinct event identities | Work events, instance/task/receipt identities and source revisions | Arbitrary historical-message occurrence reconstruction from unprepared records |
| Scoped correction | Claim revisions and dependency invalidation; source supersession | General semantic partial-message correction, beyond declared contracts |
| Candidate stays candidate | Assisted/candidate channels do not acquire deterministic answer support; unsupported claim language requires recheck | General inference efficacy and independently calibrated assisted semantics |
| Operational receipt boundaries | Started/failed/indeterminate execution, validated completion, fencing and current task checks | Independent AI-provider READ/ACK or arbitrary external-world outcome verification |
| Operator burden | Explicitly acknowledged and proposed metrics | Independently measured end-to-end labor or cost advantage |

This matrix neither awards a feature because a document names it nor treats a
capability outside declared scope as an engineering defect. The inspected code
supplies concrete enforcement mechanisms; its actual guarantees still depend on
specified grammar, host integrity, source availability and threat assumptions.
The current source checker does not validate arbitrary propositions or detect
every uncited contradiction. An intact source can be false. A hash does not
certify truth or authorship. A work-state projection deliberately says so.

Ben's excerpt pins an older revision, `257e54a51edac272eb6b2441457f38a40485ee4d`.
Later code cannot retroactively pass that test; a historical limitation cannot be
automatically assigned to this revision. No conclusion that its broad
original-record reconstruction challenge has been solved is drawn here.

## Related public work

The pinned [Portable Evidence Runtime](https://github.com/mitchell-d00/portable-evidence-runtime/tree/4fdc20193c01f82baea0598b4c7d8ef3040772d5)
README distinguishes a self-sealed editable ledger from an externally expected-root
capsule verifier. It disclaims signatures, factual accuracy and independent hosted
comparison. The [residual experiment](https://github.com/mitchell-d00/mplpb-residual-experiment/tree/1ec160051ba306ce61d74ba3186f0aa5873694c5)
README distinguishes raw/newest-history ablations, native gates and a conventional
reference gate; its maintained/refusal claim expressly avoids truth certification.
Those materials inform comparison design. Their reported counts were not newly
reproduced in this study and are not evidence of OOCC performance.
