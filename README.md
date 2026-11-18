# B-Tests — MPLPB and OOCC/CAD comparative experiments

This repository tests whether published OOCC/CAD instructions correct an inherited,
human-approved interpretation when original evidence contradicts it. It also tests
failure-history retention, permissions, causal relationships, receipts and compressed
handoffs. Findings are limited to recorded executions and specified criteria; no
claim of a global architectural victory is made.

**We have no access to Ben’s live system.** These are instruction-level model tests
and evaluator controls, alongside separate native MPLPB executions. They do not test his private Memory/Drive/SQL controller,
scheduler, recipient acceptance or native action enforcement. See
[system scope](docs/OOCC_2026_SYSTEM_SCOPE.md).

## What the testbench has tested

B-Tests supplies the test cases, published instructions, fresh-session procedures,
scoring code and retained logs needed to examine Ben's published OOCC/CAD ideas.
**I have the testbench; I do not have Ben's private system to put on it.** His papers
refer to private controller components and primary records that have not been
available to this evaluation. Testing that system requires its exact runnable
version, setup, authorized source access, adapter and independently checked state
readbacks. Those native-system tests remain **NOT_RUN**.

We have run **30 real fresh AI sessions** using published CAD instructions and
strong conventional governance instructions. The cases tested false approved maps,
contradictory sources, archive discovery, failed-work history, permissions, receipts,
unsupported relationships, compressed handoffs, false originals and a simulated
human export. Both instruction treatments corrected accessible contradictions and
rejected unsupported relationship expansion. Specific output/budget failures and
results favorable to CAD are retained. These runs did not establish a consistent
CAD advantage over the tested conventional instructions.

We also executed **MPLPB's actual program**: native source and permission checks,
real local action controls, the sorter and public evidence probes. A valid control
really invoked a local executor; invalid cases were blocked and checked through
effect files and event counts. These checks execute through guarded software
interfaces, without relying on a model agreeing to follow a prompt. MPLPB packages
its bounded rules and verification for supported runtimes without requiring a
particular AI provider or conversation.

In plain language: **we tested how AI follows the published instructions and how
MPLPB's software enforces its checks. We have not tested Ben's private controller.**
The [recorded instruction results](docs/CRITICAL_BENCHMARK_RESULTS.md),
[archive discovery](docs/UNFLAGGED_DISCOVERY.md),
[handoff propagation](docs/ARCHIVED_PROPAGATION.md),
[human export](docs/SINGLE_PROJECT_HUMAN_EXPORT.md) and
[native software results](evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/RESULTS.md)
show the exact scope and outcomes. A written refusal and a verified blocked
operation are different observations.

## Ben's native MPLPB run — 14 November 2026

In [Beyond Guarded Retrieval](https://www.academia.edu/181013727/Beyond_Guarded_Retrieval_A_Source_Bounded_Evaluation_of_Combined_MPLPB_and_a_Roadmap_for_Historical_Reconstruction),
Benjamin Gelhaus evaluated Combined MPLPB 2.1.0rc1 at pinned commit
[`257e54a51edac272eb6b2441457f38a40485ee4d`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/257e54a51edac272eb6b2441457f38a40485ee4d).
Gelhaus selected and ran 58 tests from the native MPLPB regression harness I
built and published with the release. For his evaluation probes he used the
unchanged writer, validator, strict-answer interface, provenance/source bundle
and passage ranking. He designed the evaluation and reported the results.

**All 58 selected native regression tests passed.** His reported retrieval results
included **31/49** exact-phrase targets in the top five and **40/42**
communication-header targets ranked first. The linked paper documents the runs.

**Thank you, Ben, for running MPLPB and publishing the results.**

I’m looking for more people willing to run MPLPB and repeat the public tests.
[Follow the pinned run instructions](evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/RESULTS.md#repeat)
and [share your results in an issue](https://github.com/mitchell-d00/B-Tests/issues/new),
including the exact commit, commands, output logs and any failures you find.

## Two projects I was working on before Ben's critique

In my May 2026 self-review, I revisited and withdrew the completion claims in
my own research account. *The Residual of Logic* traces how that self-correction
led to a software question about preserving the ability to reject stale claims
after recovery. [Self-review account](https://github.com/mitchell-d00/mplpb-residual-experiment/blob/1ec160051ba306ce61d74ba3186f0aa5873694c5/paper/The_Residual_of_Logic.md#2-the-research-arc-the-method-corrects-its-writer)

I was already working on both projects on **10 November 2026**, the day I made
the Combined MPLPB commit Ben later tested. GitHub records that commit at
**15:17:53 UTC**. Both projects have public commits and recorded runs on
**11 November 2026**, before Ben's paper dated **14 November 2026**.

- **MPLPB Residual Experiment** tested whether the ledger still enforces
  ownership, eligibility and refusal after recovery. The pilot started at
  **13:05:28 UTC** on November 11 and used the same Combined pin Ben tested.
  [Repository](https://github.com/mitchell-d00/mplpb-residual-experiment) · [Pinned run record](https://github.com/mitchell-d00/mplpb-residual-experiment/blob/1ec160051ba306ce61d74ba3186f0aa5873694c5/results/pilot-1/environment.json)
- **Portable Evidence Runtime** tested offline transfer of a package containing
  records, rules and a verifier. Its November 11 record shows **15/15 synthetic
  cases passed** at **14:59:48 UTC**.
  [Repository](https://github.com/mitchell-d00/portable-evidence-runtime) · [Pinned run record](https://github.com/mitchell-d00/portable-evidence-runtime/blob/4fdc20193c01f82baea0598b4c7d8ef3040772d5/experiment/results/synthetic_run.json)

[Timeline through November 18, including the response to Ben’s critique](docs/RESPONSE_TO_BEYOND_GUARDED_RETRIEVAL.md#exact-chronology)

## MPLPB then and now

**Then.** Ben tested Combined MPLPB 2.1.0rc1 at [`257e54a`][mplpb-ben-pin].
It already had sealed sources, integrity and lineage checks, supersession,
profile eligibility, passage ranking, finite source-body proof, an evidence
graph and a specialist work coordinator. Ben used the upstream harness and
reported 58/58 selected regressions passed. His source-location and
historical-question results describe that exact release.
[Ben's results by experiment](docs/GELHAUS_EXTERNAL_EVALUATION.md)

**Now.** As of 18 November 2026, Combined main is [`6350988`][mplpb-now-pin].
The [pinned Git comparison][mplpb-pin-diff] spans 68 commits. The merged PRs
below show which capabilities were added, which existing behavior was extended,
and where an observed defect was repaired.

### What changed after Ben’s pin

| Combined PR | Added or changed |
|---|---|
| [#40][mplpb-pr40] | The work coordinator now rechecks finite source-body support before handoff, dependency use and dispatch. Direct evidence is required and contradictory or claim-only dependencies stop downstream work. Prior assessments and failed attempts remain in history. [Source-support checker][mplpb-work-support] |
| [#41][mplpb-pr41] | Added an opt-in documentary investigation with documentary, chronology and separately parsing verification roles. It follows explicit, bounded references with citations and stop reasons, retains separate event appearances and body variants, and adds explicit scoped correction that preserves the predecessor and unaffected text. Added the published 52-case evaluation. [Investigation code][mplpb-investigation] |
| [#42][mplpb-pr42] | Added the original-record study runner with pinned inputs, sealed question and gold commitments, isolated execution, source-cited reviewer submissions and adjudication. This gives an outside evaluator a runnable protocol on unchanged originals. [Study protocol][mplpb-study] |
| [#43][mplpb-pr43] | Added exact ID/hash and unique body-field routing, distinct diagnostic reasons and conflict retention under display budgets. Separated declared event IDs, repeated event keys and source appearances. Added field/time correction windows, read-only as-of views, up to two source-quoted relation steps, separation of receipts from claim support, and optional operator-time recording. [Scoped evidence contracts][mplpb-scoped] |
| [#44][mplpb-pr44] | Extended gated passage discovery for ordinary prose and reverse mapping to original bytes. Improved candidate dates and relations, retained unresolved links, and published raw-original transfer tests, omissions and failed attempts. [Prose recovery report][mplpb-prose] |
| [#45][mplpb-pr45] | Added a fresh-source documentary assertion checker and compound-question handling. Each checked part carries quotes, qualifications and provenance. Missing obligations and contrary evidence stay visible, including in the browser. [Documentary verifier][mplpb-doc-verify] |
| [#46][mplpb-pr46] | Added checked literal wording comparisons and proof of limited arrangements explicitly recorded in the source. Added source-unit inspection, candidate graphs, typed historical review, clearer refusals, bounded parsing reuse, native local-artifact storage checks and raw crawler identity rehashing. [Reconstruction engine][mplpb-reconstruction] |
| [#47][mplpb-pr47] | Added the offline dual-mode sorter, source-anchored candidate graphs and verified retired-ledger export that the pre-sorter reader can open. Published the technical paper and reproduction tooling. [Sorter code][mplpb-sorter-code] |
| [#48][mplpb-pr48], [#49][mplpb-pr49] | Revised the sorter paper front matter and consolidated the package, installation and authority guides. The reader’s proof rules remained in place. [Package guide][mplpb-package] |
| [#50][mplpb-pr50] | Fixed a sorter defect where quoted or fenced identifier headers could create false occurrence boundaries and enter primary identity clusters. Embedded headers retain their spans and review annotations. [Before/after report][mplpb-header-report] |
| [#51][mplpb-pr51] | Added the optional strict-first local narrator for Ollama, llama.cpp and local OpenAI-compatible endpoints. An accepted rendering preserves the checked answer, and a fresh source and policy check runs before it is returned. Refusals, conflicts and partials bypass narration. [Narrator code][mplpb-narrator] |

### How the sorter works

The sorter runs offline on UTF-8 text and Markdown. It records occurrences,
headers, dates, references, correction cues and other observations with the
original file hash and exact character and byte spans. PDF and image sources
need text extraction first. [Sorter guide][mplpb-sorter-guide]

| Mode | Output |
|---|---|
| `not-compared` | Source observations and textual links such as containment or co-occurrence. These let a reviewer see what each source says in context. |
| `compare` | The same sources, nodes, spans and observation edges, plus review edges for possible duplicates, different bodies under the same identifier, possible corrections and explicit references. Ambiguous or missing reference targets stay unresolved. |

The earlier fixture retained **176 identical nodes** and **264 observation
edges**, with **77 review edges** added in compare mode. A verified graph can
be stored as a sealed, retired, machine-origin snapshot. The unchanged
pre-sorter reader showed the snapshot for inspection and withheld it from
answers under lab, internal and external profiles. Candidate links carry no
answer support. In a later defect probe, classifying embedded headers first
changed **three occurrence partitions to two** and removed the quoted example
from the primary identity cluster while preserving its text. [B-Tests sorter
rerun](evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/RESULTS.md#native-sorter-evidence)
· [Header-scope regression][mplpb-header-report] · [Technical paper](docs/papers/README.md)

### Ben’s criticism and my response in code

| What Ben measured or asked for | What I implemented | What the evidence establishes |
|---|---|---|
| **P0 · Make refusals and retrieval gaps legible.** The existing contract already separated several answer states, but a user needed to distinguish unsupported grammar, absent eligible evidence, conflict, insufficient support and budget exhaustion. | Added more specific native diagnostic categories and bounded investigation stop reasons. [#43][mplpb-pr43] · [#46][mplpb-pr46] | Public controls exercise those failure categories. Cross-adapter consistency and whether the labels improve operators’ decisions still need measurement. |
| **P1 · Improve access to the right original passages.** Exact phrases reached the expected source in the top five on **31/49** queries, even though rich communication headers ranked it first on **40/42**. Analyst notes could displace originals at rank one. | Exact ID/hash and body-field routing, conflict retention, source-layer inspection, gated prose search and mapping back to original spans. [#43][mplpb-pr43] · [#44][mplpb-pr44] · [#46][mplpb-pr46] | Zero/one/multiple-match and contradiction controls pass. The prose recovery run located **18/23** reference spans on a different development set. Ben’s 515-page comparison still needs the authorized originals or a matched replacement. [Prose recovery report][mplpb-prose] |
| **P1 · Separate appearances from communication identity.** One message can appear in several places, equal subjects can refer to distinct messages, and matching headers can accompany conflicting bodies. | Separate source occurrences and event candidates, explicit identifier namespaces, body-variant review, and sorter scope checks for quoted or forwarded headers. [#41][mplpb-pr41] · [#43][mplpb-pr43] · [#50][mplpb-pr50] | Public controls and the repaired sorter probe demonstrate these distinctions on the tested inputs. Unseen event-identity precision and recall remain open. |
| **P2 · Keep partial corrections and time provenance.** A later correction can change one claim while earlier text remains historically relevant. | Exact-span scoped corrections preserve predecessor text and unaffected fields. Field/time windows and read-only as-of views retain historical inspection without authorizing current work on retired sources. [#41][mplpb-pr41] · [#43][mplpb-pr43] | Public controls cover partial corrections, ambiguous spans, stale bases and scoped history. Uncertain dates and real partial retractions need independent scoring. |
| **P2 · Reconstruct justified relationships from originals.** The old strict grammar abstained on **57** event-question forms. A supplied graph or plausible bridge leaves historical reconstruction unmeasured. | Opt-in source-quoted relation exploration stops at missing bridges. Separate documentary proofs check particular source assertions, wording comparisons and recorded arrangements with citations, qualifications and missing obligations. [#41][mplpb-pr41] · [#43][mplpb-pr43] · [#45][mplpb-pr45] · [#46][mplpb-pr46] | On **22 unchanged development questions**, native complete source support moved **0 → 1 → 2** across the reported reconstruction stages. The latest fresh-context AI assessment rated **2 complete correct, 4 correct refusals and 16 errors or over-refusals**. Independent human scoring and general historical reconstruction remain open. [Solo evaluation][mplpb-solo] |
| **Appendix A · Preserve authority and distinguish operational receipts.** A stored, sent or narrated claim supplies no proof of delivery, acknowledgment or completion. | Recheck source bodies before downstream work, keep storage and host receipt types distinct, and require strict proof before optional narration. [#40][mplpb-pr40] · [#43][mplpb-pr43] · [#46][mplpb-pr46] · [#51][mplpb-pr51] | At the old pin a contradictory component-status claim and a claim-only chain both reached the executor. The repaired pin blocked both and still ran the direct-source positive control. Independent external delivery, READ/ACK and completion trials remain open. [Paired native probes](docs/MPLPB_NATIVE_COMPARISON.md#seven-paired-boundary-probes) |
| **P3 · Measure scale, missed evidence and review effort.** Compare budgets, coverage, false bridges, compute and human labor. | Added source/hop/discovery limits, explicit stop reasons, bounded immutable parsing reuse, workload metrics and optional operator time. The study harness preserves pinned inputs, receipts and reviewer disagreements. [#41][mplpb-pr41] · [#42][mplpb-pr42] · [#43][mplpb-pr43] · [#46][mplpb-pr46] | A matched solo replay recorded lower worker CPU on that workload. Repeated scaling on matched corpora and actual human review and correction times remain open. [Solo evaluation][mplpb-solo] |

The [same 52 public software controls][mplpb-public-baseline] recorded **10 passes
and 42 capability gaps** at Ben’s pin and **52/52** at the fixed PR41 implementation.
The gaps describe missing or unimplemented capabilities in that developer suite.
At the subsequent narrator implementation freeze, the [upstream report][mplpb-narrator-report]
records **1,219 native tests** and **52/52 public controls** passing. These
measurements cover software behavior. The 22-question study measures a separate,
much narrower reconstruction result. [Full acceptance matrix](docs/RESPONSE_TO_BEYOND_GUARDED_RETRIEVAL.md#requirement-by-requirement-map)

### What would narrow the remaining criticism

1. **Replay Ben’s released synthetic benchmark on both pins.** Obtain and
   hash-check his named public companion archive. Run its original probes at
   `257e54a` and `6350988` using the same corpus, questions and machine budgets.
   Report source-location recall, refusals, occurrence/body collisions, scoped
   corrections and false bridges. Record missing interfaces and any harness
   adaptation explicitly. [Companion archive and replay limits](docs/GELHAUS_EXTERNAL_EVALUATION.md#what-is-public-and-what-remains-reproducible-only-in-part)
2. **Run a blinded historical evaluation on unseen originals.** An outside
   custodian freezes the source bytes and hidden questions. Two independent
   reviewers score exact citations, distinct events, corrections, qualifying
   language, justified relationships and appropriate refusals against a
   predeclared rubric. Compare the old strict reader, current strict reader,
   and current reader with sorter-assisted discovery under matched budgets.
   In the sorter arm, reviewers use candidate links to locate originals and
   the reader checks the originals under the same authority rules. Keep labels
   and expected links out of the input corpus. [Existing study protocol][mplpb-study]
3. **Measure whether the sorter saves reviewers work.** Compare manual review
   with sorter-assisted review on the same task types. Time source location,
   adjudication and re-entry after an interruption. Report missed originals,
   false identity groups and bridges, reviewer disagreement, bytes read,
   CPU and memory. Preserve corpus sizes, repeated-run variation and regressions
   after withdrawal or correction. [Current sorter limits][mplpb-sorter-guide]

[mplpb-ben-pin]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/257e54a51edac272eb6b2441457f38a40485ee4d
[mplpb-now-pin]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/6350988a2f64d8e5fa53bd187d368f4397bf4f4c
[mplpb-pin-diff]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/compare/257e54a51edac272eb6b2441457f38a40485ee4d...6350988a2f64d8e5fa53bd187d368f4397bf4f4c
[mplpb-pr40]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/40
[mplpb-pr41]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/41
[mplpb-pr42]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/42
[mplpb-pr43]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/43
[mplpb-pr44]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/44
[mplpb-pr45]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/45
[mplpb-pr46]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/46
[mplpb-pr47]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/47
[mplpb-pr48]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/48
[mplpb-pr49]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/49
[mplpb-pr50]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/50
[mplpb-pr51]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/51
[mplpb-work-support]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/mplpb_work/source_support.py
[mplpb-investigation]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/mplpb_work/investigation.py
[mplpb-study]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/docs/ORIGINAL_RECORD_STUDY.md
[mplpb-scoped]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/docs/SCOPED_EVIDENCE_EXTENSIONS.md
[mplpb-prose]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/ff386a6f22b00d703d91665d5efc4ab284a34bf5/evaluation/unprepared-originals/2026-11-16-recovery/REPORT.md
[mplpb-doc-verify]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/mplpb_answers/documentary_verify.py
[mplpb-reconstruction]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/docs/HISTORICAL_RECONSTRUCTION_ENGINE.md
[mplpb-sorter-code]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/mplpb_work/sorter.py
[mplpb-package]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/docs/PACKAGE_GUIDE.md
[mplpb-header-report]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/evaluation/preprocessing-sorter/2026-11-17-header-scope/REPORT.md
[mplpb-narrator]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/mplpb_answers/local_narrator.py
[mplpb-sorter-guide]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/docs/PREPROCESSING_SORTER.md
[mplpb-solo]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/evaluation/solo-milestone/2026-11-17/RESULTS.md
[mplpb-public-baseline]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/4fe099ca14175399f58369efcc39153c203a5677/evaluation/historical-experts/final-comparison.json
[mplpb-narrator-report]: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/evaluation/general-reader/2026-11-17-local-narrator/REPORT.md

## Latest B-Tests native rerun — 17 November 2026, PR49

Current Combined pin **ccbb5804eb47f78c2338d57c142ad087b47be710** passed
**1,186 native tests**, seven additional checks, seven B-Tests boundary probes,
ten applicable legacy query contracts and52 public-evidence controls. The sorter
kept176 identical nodes across modes, added77 review edges and exported a snapshot
that the unchanged pre-sorter reader withheld under all three profiles.

[Requirement-by-requirement response to Ben](docs/RESPONSE_TO_BEYOND_GUARDED_RETRIEVAL.md)
marks already-present, partial, newly added and still-open portions separately from
software PASS and independent acceptance. [Exact fresh results and commands](evaluation/mplpb-updates/ccbb5804eb47f78c2338d57c142ad087b47be710/RESULTS.md)
include reproductions of both November 11 experiments. Combined later merged the
optional strict-first narrator in PR51. Its separate upstream report records
1,219 native tests at the frozen implementation revision. [Upstream validation](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/6350988a2f64d8e5fa53bd187d368f4397bf4f4c/evaluation/general-reader/2026-11-17-local-narrator/REPORT.md)

**Substantial implementation coverage is demonstrated; independent historical
accuracy and general reconstruction remain unestablished.** Inspection, graph
packaging and human promotion do not establish source support or historical truth.
Only B-Tests was edited. No new OOCC/CAD sessions or private controller trials ran.

[Sorter paper and response paper: MD/TXT/PDF](docs/papers/README.md) ·
[Ben's original paper](https://www.academia.edu/181013727/Beyond_Guarded_Retrieval_A_Source_Bounded_Evaluation_of_Combined_MPLPB_and_a_Roadmap_for_Historical_Reconstruction)

## Earlier PR46 rerun — 17 November 2026

Updated main [`3df2c6e22f0ef454f3ee67b88d43402a42f63443`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/3df2c6e22f0ef454f3ee67b88d43402a42f63443)
passed **1,157 native tests**, seven additional checks, seven work-boundary probes,
ten applicable legacy source-query contracts and the 52-case public-evidence
suite. The 12 public-paper reader outputs are unchanged from PR #43.

Component suites passed with their required environment permissions. Initial
Networked/Image socket-setup failures and unchanged-code successful retries are
both retained. No MPLPB source files were changed and no new OOCC/CAD model
sessions were run.

[Versioned report, logs, exact commands and limitations](evaluation/mplpb-updates/3df2c6e22f0ef454f3ee67b88d43402a42f63443/RESULTS.md).
The earlier results below retain their original versions and dates.

## Earlier native MPLPB results — 16 November 2026

The full unmodified MPLPB checkout at
[`cc21ce300b5ec228c07fc77a149804fba6c89792`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/cc21ce300b5ec228c07fc77a149804fba6c89792)
passed **887 Python tests and seven additional native checks**. Bundled components
also passed: **Swarm 145, Networked 61, Smart Local 52 and Image 93**, plus
adoption checks. The component checker repeated the Combined 887; that repeat is
not additional coverage. No target code was modified.

Seven paired native probes used the current version and the older
`257e54a51edac272eb6b2441457f38a40485ee4d` pin identified by Ben. The older version
allowed a contradictory claim and claim-only chain to invoke a real local executor;
the current version blocked both. Current results: **7 PASS**. Historical results:
**5 PASS, 2 FAIL against these probe criteria**. Valid controls really executed;
blocked cases were checked through effect files and separate database readback.
These are not reproductions of Ben's unavailable private benchmarks.

[Native results, blockers and exact rerun commands](docs/MPLPB_NATIVE_COMPARISON.md) ·
[Raw logs and hashes](evaluation/mplpb-native) ·
[Dated ecosystem and all repository links](docs/MPLPB_CHRONOLOGY.md)

An initial restricted-environment run failed because localhost sockets were denied;
its logs remain. The unchanged full suite passed after that environment restriction
was removed. A finite source checker is not a general factual truth guarantee.
Native authored-suite counts are not comparable performance scores against AI
session counts.

## Current benchmark — 16 November 2026

The first frozen condition contains **64 synthetic records, ten projects, 5,120
planning-relation appearances and 119 questions**. Two real fresh AI sessions
received matched original evidence: published CAD instructions versus strong
ordinary source governance. It includes false approved maps, copied evidence,
numeric acceptance thresholds, limited corrections, revoked grants, failed work,
misleading causal bridges and stale completion receipts. Positive controls require
supported successes and one permissible local release.

| Observed criterion | CAD instructions | Conventional governance |
|---|---:|---:|
| Correct values on requested questions | 119/119 | 119/119 |
| Appropriate local action selection | PASS: P7 only | PASS: P7 only |
| Handoff at most 900 characters | PASS: 881 | PASS: 900 |
| Extra unrequested question | FAIL: added Q120 | None |
| Frozen source-ID-set matches | 108/119 | 109/119 |
| Original overall score | FAIL | FAIL |

The source-set score is overstrict: histories directly state that old callbacks
do not verify current tasks, but the key also requires a policy ID. CAD also cites
the current revocation without the former grant. Those original scores are retained;
they are **not eleven and ten false factual answers**. All cited quotes match supplied
originals. Semantic interpretation of equivalent source routes is an unblinded
review, not independent adjudication.

The central false-approved-interpretation failure was **not observed** in this
condition. Neither OOCC/CAD superiority nor equivalence to conventional governance
is established by one matched pair. A larger generated corpus can still contain
simple templates. Matching dimensions Ben reports does not establish equal
measurement difficulty without his private fixtures and scoring records.

[Benchmark protocol and repeat instructions](docs/CRITICAL_BENCHMARK.md) ·
[Current results and blockers](docs/CRITICAL_BENCHMARK_RESULTS.md) ·
[Retained inputs, answers, key and hashes](evaluation/critical-bench-1) ·
[Claim matrix](docs/OOCC_CORRECTION_EVALUATION.md)

## Unflagged archive discovery

A further [four-session discovery test](docs/UNFLAGGED_DISCOVERY.md) gave no warning that an approved map was wrong. Both treatments searched the archive, found the current original, contested the wrong claim and selected no release; both also selected release on the valid control. A separate filesystem monitor observed current-original access in all four sessions. CAD had one literal action-string mismatch, with the correct decision by meaning.

This discovery condition did not test a false original without contrary evidence. The later [archival propagation](docs/ARCHIVED_PROPAGATION.md) and [single-project human export](docs/SINGLE_PROJECT_HUMAN_EXPORT.md) conditions address bounded parts of that concern, with results below.

## False originals and a single-project human export

The [three-stage propagation run](docs/ARCHIVED_PROPAGATION.md) used one false
original, no contrary observation, 10/100/1,000 promoted descendants and fresh
sessions. Both treatments retained one evidence root, rejected unsupported
expansion and causal edges, and acknowledged unverified outside-world status.
Both continued requesting local P0 release from the wrong inherited report.
The conventional final handoff exceeded 400 characters at 410; CAD used 384.
This tests bounded propagation, not detection of an unobservable truth.

The [single-project human-export pair](docs/SINGLE_PROJECT_HUMAN_EXPORT.md) removed
the original and lineage entirely. Both treated the export as inherited and marked
generation unknown. **CAD deferred release pending validation evidence; the
conventional session requested release relying on the export.** That is an observed
difference in one pair, not a general superiority finding or native enforced block.
The task explicitly requested evidence classification. No real release occurred.

There are now **30 real target sessions across five conditions**, including dependent
handoff stages. These are authored development experiments, not thirty independent
projects, independent validation or proof against all inherited-error reinforcement.

## Paper and public-work comparison

**MPLPB and OOCC/CAD: Comparative Experiments**, by Mitchell D. McPhetridge, research draft
16 November 2026: [Markdown](docs/paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.md) ·
[TXT](docs/paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.txt) ·
[PDF](docs/paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.pdf).
The [build instructions](docs/paper/BUILD.md) regenerate TXT/PDF from Markdown.

The paper reports the observed seams, including results favorable to CAD, and
addresses the supplied *Beyond Guarded Retrieval* excerpt against the
[focused current MPLPB source review](docs/MPLPB_PUBLIC_SOURCE_REVIEW.md).
The initial 48-file source review was followed by complete-checkout native
execution. Neither is an exhaustive semantic audit. Enforced finite contracts and successful instruction following remain
separate evidence levels.

## Repeat with any AI

An operator prepares a new local study, then gives each fresh AI only its own
assigned packet directory. Keep outcome keys, other treatments and repository
results away from the target. Follow the packet’s `ENTRY.txt`, retain the complete
conversation and save the untouched JSON answer.

```sh
python -m research_lab.critical_bench prepare \
  --root evaluation/blind-private-runs/my-study \
  --seed 20261116 --pages 64 --relations 5120

python -m research_lab.critical_bench submit \
  --root evaluation/blind-private-runs/my-study --packet ASSIGNED_PACKET_ID \
  --response answer.json --transcript original-transcript.txt
```

Use a new directory for every condition. `--pages 515` and
`--relations 100`, `1000` or `10000` prepare separate scale conditions; **they have
not yet received model executions here**. Same-seed replay is a public development
test, not an untouched holdout. Public links cannot prove a fresh session or enforce
isolation. Record truncation, unavailable sources and interventions explicitly.

## Verify retained results and the harness

```sh
python -m unittest discover -s tests -v
python -m research_lab.critical_bench replay
python -m research_lab.agent_replay
python -m research_lab.discovery_bench replay --root evaluation/discovery-1
python -m research_lab.propagation_bench replay --root evaluation/propagation-1
python -m research_lab.human_export_bench replay --root evaluation/human-export-1
python -m research_lab.native_evidence
```

The local suite passes **121 tests**. Public evidence is retained as inspectable UTF-8 JSON and JSONL. Replay verifies
original input hashes; optional lossless gzip input remains supported. Replay recomputes retained scores and file
transfers; it makes **zero new model requests**. Unit-test passes are not target
passes. Submitted local state/effects are saved before evaluation, without a hidden
truth guard rewriting the model’s choices. A selected local release is not a
verified external operation.

## Retained earlier work and remaining limits

The earlier 16-session run is retained as a
[historical simplified instruction check](docs/HISTORICAL_SIMPLIFIED_CHECK.md).
Its two- or three-source fixtures and repeatedly supplied originals were too
simple to establish independent or live-system validation. Both arms corrected
false approved claims and respected revocation; each exceeded one final compression
limit. The original strict scores and their defects remain available.

Earlier HTTP experiments returned no usable model completion and retain their
`NOT_RUN` classifications in the [execution history](docs/OOCC_CORRECTION_RESULTS.md).
The native kill-condition runner remains **38 NOT_RUN** because Ben’s live adapter
and independent readbacks are unavailable. Missing access is not an architectural
failure. Functional Layers forecasting, human learning, summary-only recovery,
long handoff chains and native enforcement remain unresolved. The
[existing compression/handoff protocol](docs/BLIND_HANDOFF_EXPERIMENT.md) and API
runners remain available; unavailable transport must not be reported as a model
answer.

The benchmark applies source pins, negative controls, per-case evidence and explicit
limits drawn from [MPLPB’s evaluation methods](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/main/evaluation/README.md).
Updated MPLPB findings concern the pinned native suites and seven authored probes;
they do not establish a general accuracy or workflow advantage. Private correspondence, original supplied
PDFs and unused private outcomes are excluded from publication. Exhaustive reading
and claim extraction across every supplied book is not claimed.
