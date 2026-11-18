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
