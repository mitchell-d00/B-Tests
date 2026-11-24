# What B-Tests compared and who supplied each part

**The 30 fresh AI sessions compared two governance prompt treatments.**
One used Benjamin Gelhaus’s published OOCC/CAD instructions. The other
used a strong conventional governance prompt prepared by B-Tests.
Combined MPLPB was not either prompt arm. A separate native experiment
compared two versions of Mitchell D. McPhetridge’s Combined MPLPB.
**B-Tests did not execute Gelhaus’s native OOCC/CAD controller or M6.**
[Machine-readable scope](../research/comparison-scope.json) ·
[Evidence inventory](../evaluation/findings-index.json) · [Test index](TEST_INDEX.md)

## The 30 instruction-level sessions

The runs used fresh AI sessions and matched underlying evidence, tasks,
and handoff limits within each condition. The instructions differed. Some
sessions continued a trajectory by receiving a retained handoff. The
count refers to target sessions, including dependent stages. The exact
provider snapshot and token usage were unavailable. The archive preserves
normalized responses and checks rather than provider API transcripts.
Gelhaus’s CAD material supplied a prompt-delivered governance treatment.
His publications describe broader workflows and report software development.

| Condition | Target sessions | What the records show |
| --- | ---: | --- |
| Historical simplified check | 16 | Both corrected false approved states when supplied originals contradicted them. CAD wrote 503 characters against a 500-character limit. The conventional arm wrote 501. [Records](../evaluation/agent-pilot-1/records.json) |
| Critical benchmark | 2 | Both answered the 119 requested values correctly. CAD emitted an unrequested Q120. Exact-source-set scoring was kept separately. [Records](../evaluation/critical-bench-1/summary.json) |
| Unflagged archive discovery | 4 | Both opened the relevant current original and corrected the false map. An OS monitor recorded file access. [Records](../evaluation/discovery-1/summary.json) |
| False-original propagation | 6 | Both rejected unsupported expansion and carried forward an inherited false report whose error could not be distinguished from the available observations. The conventional final handoff used 410 characters against a limit of 400. [Records](../evaluation/propagation-1/summary.json) |
| Single-project simulated human export | 2 | CAD deferred release pending evidence. The conventional arm requested release based on inherited completion. The test recorded the models’ decisions, and no release occurred. [Records](../evaluation/human-export-1/summary.json) |

The handoff limits were measured in **characters**, not tokens. The three
budget overruns were one CAD overrun and two conventional overruns.
Correcting accessible contradictions and resisting unsupported causal
expansion were shared observations within the prompt trials. Those
observations establish behavior in the recorded sessions.

### What established separate sessions

Separate target sessions received the assigned experimental inputs. Later stages
of a trajectory specifically received the retained state and handoff, so those
stages depend on earlier stages. The archive records the outputs and workflow
checks, and includes operating-system file-read observations for the discovery
condition. Provider receipts and complete API transcripts are unavailable for
these historical sessions. The later PPC live run records evidence for each
separate inference request, a procedure made reusable in
[MoxCOP](../evaluation/ppc-live/2026-11-24/moxcop/README.md).
[Verified PPC run](../evaluation/ppc-live/2026-11-24/README.md)

## The separate native MPLPB runs

The November 16 comparative paper reports seven authored B-Tests boundary
probes on two actual Combined MPLPB checkouts. The older version
`257e54a` met five of seven criteria. It let a contradictory claim and a
claim-only dependency chain reach a local adapter. The newer tested pin
`cc21ce3` met all seven, blocked those two cases before the adapter and
before a new ledger event, and still executed the supported control.
B-Tests authored the exact probes in response to the critique. The study
did not reproduce Gelhaus’s unseen private fixtures. Independent marker
files and read-only event counts checked the native effects. That paper
also reports a separate 887-test development-suite pass at `cc21ce3`.
Later native runs retain their own pins, counts, and reports.
[Native method](MPLPB_NATIVE_COMPARISON.md) ·
[Seven-probe results](../evaluation/mplpb-native/final-seven-case-pairs/summary.json)

## Code provenance and unavailable tests

- **Benjamin Gelhaus** wrote the published OOCC/CAD governance materials used
  for the instruction treatment and published evaluations of MPLPB. In
  *Beyond Guarded Retrieval* he reports selecting and running upstream
  MPLPB regression tests on `257e54a`, with 58 of 58 passing after omitted
  fixtures were restored. This is an attributed report. B-Tests did not
  repeat that exact selection with his original private inputs.
  [External evaluation record](GELHAUS_EXTERNAL_EVALUATION.md)
- **Mitchell D. McPhetridge** built Combined MPLPB and its existing native
  test machinery, and built B-Tests. Gelhaus’s later public MPLPB benchmark
  package includes a reproduction script with fixture-generation and
  query-template code. Its inspected engine imports are McPhetridge’s
  MPLPB writer, answer pipeline, and reader profiles. The package’s
  publication does not settle who authored the wrapper. File inspection
  supplies no separate runnable Gelhaus-native OOCC controller or M6.
  [Package and import audit](../evaluation/public-claims/2026-11-20/attribution-audit.json)
- **B-Tests CADLab** is McPhetridge’s evaluator-owned reference/control
  implementation. Its checks report CADLab behavior. They do not execute
  Gelhaus’s controller. [Reference controls and attribution](../evaluation/public-claims/2026-11-20/RESULTS.md)
- **Gelhaus’s native OOCC/CAD and M6** were unavailable for an independent
  code-level run in B-Tests. The cited OOCC GitHub repository returned 404
  again on 23 November 2026. That establishes the access result at the cited
  location. The publications describe prototype components and author-reported
  outcomes. Native controller enforcement and M6 behavior remain `NOT_RUN`
  here. [Native system scope](OOCC_2026_SYSTEM_SCOPE.md) ·
  [M6 correction](paper/TESTING_OOCC_ERRATA.md)

### What the public benchmark driver actually does

B-Tests reverified the public ZIP and all 59 manifest entries on 23 November.
The benchmark package provides 50 synthetic records and 900 positive field
questions. The question CSV records whether an answer is expected. The fixture
CSV supplies the field values. At its default settings, `reproduce.py` generates
the records and questions from templates and adds 200 negative controls.
It does not load either CSV or feed an answer key to the engine. It tallies the
native support flags and errors. The prior field-access response separately
checked the returned field values against the public benchmark data.

The script creates the actual ledger pages through `mplpb_combined.ledger.write`.
It asks each question through `mplpb_answers.pipeline.answer_query` and selects
the external profile via `mplpb_combined.reader.PROFILES`. Those are pieces of
McPhetridge’s existing MPLPB engine. The benchmark contributes the cases,
expectations, orchestration and reporting. The older regression suite is
another existing MPLPB artifact. The source package establishes where the
benchmark was published and leaves individual authorship of the wrapper and
CSV files unverified.

Running the unchanged driver against its cited pin `bbf6690` reproduced
150/150 canonical supported answers, 0/750 supported paraphrases and 200/200
rejected negative controls. These are strict-engine support counts.
[Fresh verification and exact call sites](../evaluation/public-claims/2026-11-23/public-driver-verification.json) ·
[Field-value reproduction](papers/archive/field-access-response/response.md)

The later *Testing OOCC* paper distinguishes the earlier 30 sessions from
its newly prepared C5 prompt comparison and C6 native systems comparison.
C5 and C6 were `NOT_RUN` in that paper. Its 34-family roadmap is a catalogue
of required tests and includes links to existing narrow probes.
[Current paper](paper/TESTING_OOCC.md) · [Catalogue](OOCC_CLAIMS_AND_REQUIRED_TESTS.md)

## Paper audit and editions

The review checked the attribution and execution boundaries in the current
paper set and the repository’s 18 previously tracked PDF editions.
Archived editions remain preserved as source records. Use the current
clarifications below when quoting across editions.

| Paper or archive group | Evidence boundary checked |
| --- | --- |
| *MPLPB and OOCC/CAD: Comparative Experiments* and the separately supplied earlier PDF | The 30 sessions were CAD instructions versus conventional instructions. Native probes were MPLPB versus MPLPB. The earlier edition’s excerpt-only source access reflects its original review date. The full public paper was subsequently reviewed without acquiring the private fixtures. [Current paper](paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.md) · [Later source review](GELHAUS_EXTERNAL_EVALUATION.md) |
| *Testing OOCC* v1.0–v1.4 | Separate the author’s claims and proposed tests, B-Tests CADLab, native MPLPB probes, prepared prompt comparison, and unavailable native OOCC arm. The v1.2 M6 attribution error was corrected in v1.3. v1.4 clarifies the comparison scope. [Edition archive](papers/archive/README.md) |
| *From Paraphrase Refusal to Bounded Field Access* | The public reproduction script imports upstream MPLPB writer, reader and answer code. The response documents what was run and says the supplied package lacks M6. [Archived response](papers/archive/field-access-response/response.md) |
| *The Witness Inside the Machine*, original and empirical revision | The original design scaffold had scripted responses. Later live self-assessments, outside-judge replays, planted-case model verdicts, and native MPLPB probes are distinct. Native OOCC was not run. [Empirical revision](paper/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.md) · [Original edition](papers/archive/witness-2026-11-19/THE_WITNESS_INSIDE_THE_MACHINE_REVISED.md) |
| *Probabilistic Prompts and MPLPB Deterministic Contracts*, *MPLPB Mixed Dump*, and *A Dual-Mode Sorter for MPLPB* | The switch and sorter papers identify MPLPB test machinery and measured boundaries. The sorter distinguishes processed candidates from approved originals. These are not native OOCC comparisons. [Paper index](papers/README.md) |
| Combined MPLPB manuscript editions, *Portable Evidence Runtime*, and *The Residual of Logic* | These describe McPhetridge’s systems or experiments. Their outcomes are not additional executions of Gelhaus’s controller. [Preserved papers](papers/archive/README.md) |
| *Executable Gates and Human-Maintained Indexing* | The retained executable and mediation controls concern Git and MPLPB. Scope follows the commands and artifacts actually checked. [Reproduction](../comparative-tests/executable-gates/REPRODUCTION.md) |
