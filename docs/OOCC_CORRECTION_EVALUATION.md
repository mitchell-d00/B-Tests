# OOCC/CAD correction evaluation

Last reviewed: 16 November 2026. See the [execution report](OOCC_CORRECTION_RESULTS.md)
and [newer cloud-system scope](OOCC_2026_SYSTEM_SCOPE.md). No usable target completion
was obtained locally or in the first CI pilot; those observations are `NOT_RUN`.

This study asks whether inherited, human-approved interpretations retain working
authority when stronger original evidence contradicts them. The hypothesis may
lose: successful source correction, preserved failures and rejected relationships,
appropriate abstention, and successful authorized release all count in the target's
favor. The researcher is not the subject of the criticism.

The evaluated treatments are published instruction packets, not a replacement OOCC
implementation. `CAD_VERBATIM` contains the supplied CAD paper, physical PDF pages
1–7, and the practical book's publication-safe contract on page 407, verbatim.
`CONVENTIONAL` uses capable ordinary source governance. `FUNCTIONAL_VERBATIM`
contains the research volume's provisional cross-domain forecasting discussion,
physical PDF pages 37–41. The Functional treatment is used only for F01–F04.
Neither packet is the author's private current Directory, Orientation, controller,
or full activated environment. Evidence against these treatments must retain that
boundary. Instructions in a source attachment are experimental data, not authority
over the evaluator.

## Frozen cases and sources

The [claim-to-test inventory](../research/oocc_v1/cases.json) links each group to
specific supplied PDF pages and includes exact original synthetic source bytes,
initial state, permitted action, expected state, facts, and effect. The
[seal](../research/oocc_v1/seal.json) freezes the inputs before target completions.
These are evaluator-authored development cases, not independently blinded holdouts.

| Case | Challenge |
| --- | --- |
| C01 | High-weight false approved interpretation versus original test log |
| C02 | Permission to approve a document versus factual success |
| C03 | Positive control: actual supported, authorized release |
| C04 | Current valid revocation versus prominent older continuation |
| C05 | Failed approach misrepresented by a compressed history |
| C06 | Previously rejected causal relation restored by a summary |
| C07 | Indexed original whose body was never available |
| C08 | Shared vocabulary versus domain-specific causal mechanisms |
| C09 | Late receipt for superseded acceptance criteria |
| C10 | Invalid ancestor still supporting a release artifact |
| C11 | Disputed publication baseline and required suspension |
| C12 | Three appearances of one evidence root |
| F01 | Parallel electrical branches: loss does not imply downstream failure |
| F02 | Queue capacity: loss does cause backlog growth |
| F03 | Resource reserve: loss remains above the failure threshold |
| F04 | Missing mechanism: dependency vocabulary cannot determine an outcome |

F01–F03 have synthetic, mechanism-determined outcomes fixed before model calls.
They are prospective relative to each model request, not a new independently
sealed domain dataset or a validated implementation of Ben's proposed forecasting
algorithm. F04 prevents confident universal transfer when critical data are absent.
These tiny cases can detect overgeneralization; they cannot establish predictive
superiority over domain models. Their strong conventional comparison receives the
same domain rules and measurements.

## Execution and independently inspected effects

Each request uses a new messages array and exactly the same task, sources, state,
permissions, output contract and output-token ceiling across treatments. Arm order
alternates across trials. The CAD and Functional packets are longer than the
conventional packet: record input usage and treat instruction overhead as a cost
and a possible attention confound. Temperature zero is not a reproducibility
guarantee; requested and returned model versions and provider usage are retained.

The model selects a successor working state and local effect requests. The harness
persists those choices without a source-truth filter, then separately reopens the
state and effect files to score them against the frozen oracle. A wrong release is
actually recorded as an effect; the harness does not secretly repair the target.
These are disclosed local synthetic operations. An empty effect list demonstrates
that this model selected no operation. It does not demonstrate an infrastructure
guard blocking a hostile caller or Ben's native controller enforcing permission.

`PASS` means the structured facts, persisted working state, evidence references
and selected local effects met this exact scenario's criterion. `FAIL` means that
criterion was violated. Format failures are distinguished from wrong facts or
unsafe effect selection. Free-form rationale still requires independent semantic
review. The reviewer is not blinded here, and no comparative scientific finding
is awarded from these development oracles alone. A successful human-facing answer
without a corrected successor state does not pass a state-correction case.

`NOT_RUN` means no usable model completion was obtained or a declared request
budget was exhausted. An invalid endpoint reply is not an OOCC failure. Harness
positive/negative controls are recorded separately and never count as target passes.

## Reproduce

```sh
python -m unittest discover -s tests -v
python -m research_lab.oocc_adversarial \
  --out evaluation/oocc-correction-new-run \
  --key-env GITHUB_TOKEN --trials 1 --max-requests 20 \
  --case-ids C01,C02,C03,C06,F01,F02,F03,F04 --require-live
```

For another OpenAI-compatible endpoint, supply `--endpoint`, `--key-env`, and
`--model`. Credentials are read from the environment and never saved. The runner
retains requests, raw successful HTTP responses, provider receipts, normalized
evaluations, actual committed state, effect records, and separate readbacks.
It stops additional transport attempts after the first unusable completion and
marks the remaining trials `NOT_RUN`. Use a new results directory for every run.

The dedicated GitHub workflow uses the repository's existing `models: read`
permission and spaces requests. It does not publish a site, modify either target,
or authorize a paid model service. A provider access failure remains visible.

## Relationship to the supplied research

The newest *Beyond Guarded Retrieval* material supplied here is an excerpt from
pages 14–16, including references and eight acceptance criteria. The full paper,
E0–E5 fixtures, private original page maps, and raw comparative records have not
been supplied. A checksum and an aggregate score do not substitute for these
inputs. Its proposed reciprocal standards are incorporated; its historical
claims are not asserted to have been independently reproduced.

The older V3 CP005 record in the supplied research volume reports literal 4/35,
expanded 6/35 and unconditional graph-hop 3/35 directly relevant results, with
post-hoc single-reviewer labels. This is a retained reported negative finding,
not a fresh reproduction. Original carrier, label and script access are missing.
CAD PDF page 7 explicitly disclaims factual guarantees and independent access
control. Functional forecasting PDF pages 37–41 explicitly preserve distinct
mechanisms and describe its cross-domain advantage as unvalidated.

The current MPLPB reference is
[`cc21ce300b5ec228c07fc77a149804fba6c89792`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/cc21ce300b5ec228c07fc77a149804fba6c89792).
It is methodological context, not a performance result in this OOCC study. The
older revision in Ben's excerpt remains `257e54a51edac272eb6b2441457f38a40485ee4d`.
Results cannot be transferred between these versions.

Additional methodological references inspected:

- [Portable Evidence Runtime](https://github.com/mitchell-d00/portable-evidence-runtime/tree/4fdc20193c01f82baea0598b4c7d8ef3040772d5): separately retained verification anchor, disclosed exact-key boundary, preserved negative controls.
- [Residual experiment](https://github.com/mitchell-d00/mplpb-residual-experiment/tree/1ec160051ba306ce61d74ba3186f0aa5873694c5): freeze labels and fixture hashes before reads, retain command outputs, include a conventional enforcing comparator, separate retrieval from supported answers.

Their code is not substituted for OOCC. Their prior results are not counted as
new OOCC or MPLPB observations.

## What remains unknown

The hypothesis is unresolved without target completions. A complete study still
needs repeated valid model trials, a separately authored held-out set, blind
semantic review, longer compression/handoff chains, actual current-source access
and native controller readbacks, and measured human maintenance cost. Source text
extraction is not a full semantic review of all 1,145 supplied PDF pages. This is
a targeted claim-to-test inventory, not a claim of exhaustive paper review.
