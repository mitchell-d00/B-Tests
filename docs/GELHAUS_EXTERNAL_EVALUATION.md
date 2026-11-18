# Ben Gelhaus's external evaluation of MPLPB

Last reviewed: 18 November 2026.

Benjamin Gelhaus's [Beyond Guarded Retrieval](https://www.academia.edu/181013727/Beyond_Guarded_Retrieval_A_Source_Bounded_Evaluation_of_Combined_MPLPB_and_a_Roadmap_for_Historical_Reconstruction), dated **14 November 2026**, publicly reports an external engineering evaluation of Combined MPLPB **2.1.0rc1**, pinned to [`257e54a51edac272eb6b2441457f38a40485ee4d`](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/257e54a51edac272eb6b2441457f38a40485ee4d).

**MPLPB already has external testing.** Gelhaus authored this evaluation without Mitchell as a coauthor and disclosed ChatGPT assistance and his involvement in OOCC (§12.3, p.13). It is external to Mitchell's own development tests. Its questions and labels were not blinded to the evaluator (§5.1, p.5), and its scope is an engineering probe rather than independently adjudicated general historical accuracy. These distinctions qualify the evidence without erasing the external evaluation.

Gelhaus designed the evaluation and ran selected tests from the native MPLPB regression harness built and published by Mitchell D. McPhetridge. Section 4.1 identifies the unchanged writer, validator, strict-answer interface, provenance/source bundle and passage ranking used for the evaluation. The paper reports **58/58 selected upstream regression tests passed** after omitted fixtures were restored (§4.1 p.4 and Table 3 p.6). Its conclusion credits implemented source identity, integrity, supersession, eligibility and deterministic support safeguards (§13 pp.13–14).

## How MPLPB performed in the reported runs

The figures below come from Gelhaus's full paper, especially Table3 (p.6) and §§6.1–6.4 (pp.7–8). They are his published measurements, not new B-Tests reproductions of his unavailable original corpus. Denominators remain separate; no global accuracy or winner is computed.

| Study | Reported MPLPB performance | Measured limit and correct interpretation |
|---|---|---|
| Selected native regressions | **58/58 passed** | Selected upstream behaviors; does not certify every interface or general accuracy. |
| A — 15-page native fixture | All15 pages validated; **1/1** simple control answered; ten compound questions refused without false affirmative answers | The compound forms exceeded the tested strict grammar. This is safe abstention and limited coverage, not ten demonstrated incorrect deductions. |
| B — Structured graph transfer |3,962 supplied relation rows across44 predicates;44 pages validated; **14/18** direct-status questions answered; **18/18** fabricated-record controls refused | **0/18** selected one-edge and **0/18** two-hop question forms answered. The graph was supplied in advance, and arbitrary graph traversal was outside the declared strict rules. This identifies the measured coverage boundary, not independent reconstruction or invented answers. |
| C — Synthetic scaling | Across seven sizes from80 to5,120 statements, validation passed, direct status answered, absent record refused, unsupported two-hop composition withheld | The eligible source bundle included all pages. The paper distinguishes broad eligibility from final ranked evidence and reports workload costs; broad eligibility is not automatically a defect. |
| D — Source-excerpt pilot | Expected original evidence appeared in the top five for **10/10** original questions; six supported-grammar calibration checks passed | **0/30** distinct research-question forms fitted the strict grammar. Adding analyst notes reduced original-source rank-one frequency from **7/10 to4/10**, while top-five coverage stayed10/10. This is an ordering risk, not demonstrated supported-answer contamination. |
| E — 515-page source location | Exact-phrase questions: **25/49 rank one**, **31/49 top five**. Reduced-keyword questions: **16/49 rank one**, **23/49 top five** | These retrieval misses are real measured coverage limits. They are not false factual answers. The later evaluator-built exact-string locator's49/49 result was post hoc, outside the tested native implementation. |
| F — Communication-header location | Expected source ranked first in **40/42** cases and in the top ten in **41/42** | **0/57** total question forms fitted the deterministic relation grammar. The paper explicitly says this is not57 failed logical deductions. Matching headers alone establish neither unique events nor delivery/read/ACK/completion. |

These results support substantial bounded reliability while identifying useful retrieval and reconstruction coverage improvements. They do not show unrestricted historical reconstruction; they also do not justify describing appropriate refusals as hallucinations or failed reasoning.

## Recommendations are not failure findings

Gelhaus's P0–P3 items (§7 pp.8–10; Table5 p.12; Appendix A p.16) are proposed improvements and acceptance criteria:

- More precise retrieval and answer diagnostics.
- Exact-field and evidence-class-aware routing.
- Separate source occurrences and communication candidates, with body-collision review.
- Scoped temporal corrections and versioned relations.
- Optional evidence-pinned relationship exploration with missing bridges left unresolved.
- Budget, scale, completeness, cost and operator-burden measurements.

**A proposed extension is not itself a failed test.** A failure classification requires a specified claim or contract, the corresponding system version, actual inputs and an observed violation. An observed lack of coverage can motivate an optional feature without violating a grammar that did not promise it. The paper accepts that MPLPB may remain a bounded source-authority tool (§10 p.12).

The paper also distinguishes safety from coverage (§5.1 p.5), source selection from supported answering (Table2 p.6), and source occurrence from historical event identity (§6.4 p.8). Those distinctions govern this repository's interpretation of his results. Later implementation work is recorded as added capability or changed behavior, not automatically as repair of a failure Ben demonstrated.

## What is public and what remains reproducible only in part

The article is public. Section12.1 (p.13) identifies a public companion archive, `MPLPB_Public_Companion_Reproducibility_2026-11-14.zip`, SHA-256 `c0a51de67df80adf3f3ac2c44366063b183c50d06953e298519f2b2509f5e0ef`, containing synthetic procedures and aggregate results. That archive has not been acquired or executed in this B-Tests update. A named artifact and its hash are not evidence of a completed read or replay.

The seven original PDFs, private anchors and some underlying case records were withheld. Exact reproduction of those runs requires the corresponding authorized material or a separately designed replacement study. Thus the correct credit is **publicly reported external testing**, with the available and unavailable execution evidence identified separately. It is incorrect to say nobody outside Mitchell tested MPLPB; it is also incorrect to claim B-Tests has independently reproduced every reported figure above.

The full supplied text and its content hash are retained in the [source manifest](../research/public-papers/manifest.json). The [dated thought-to-execution and acceptance map](RESPONSE_TO_BEYOND_GUARDED_RETRIEVAL.md) distinguishes earlier Mitchell explorations, Ben's evaluated pin, later Combined/sorter additions and remaining historical-validation requirements.

## Relationship to later B-Tests findings

B-Tests subsequently executed different native work-boundary probes on the old and later implementations. Those findings have their own fixtures and criteria. They must not be attributed to Gelhaus's experiment merely because the old commit matches. Likewise, current passing regressions do not retroactively alter the old pin's measured results or independently establish that every new acceptance criterion has been met.

The dated record starts with McPhetridge's self-review and prototype runs, then follows Gelhaus's external evaluation, the later implementation changes and the B-Tests reruns. [Full chronology and sources](RESPONSE_TO_BEYOND_GUARDED_RETRIEVAL.md#exact-chronology)
