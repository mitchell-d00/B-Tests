# Testing OOCC
## Published Instructions, Executable Controls, and Evidence Boundaries

**Mitchell D. McPhetridge**

20 November 2026 · Technical research paper · Version 1.0 · Author-review draft

## Abstract

Object-Oriented Cognition and Continuity (OOCC) combines source-linked project state, human-readable governance, research workflows and reported software development. A useful evaluation must distinguish these components. This paper reviews ten supplied Benjamin Gelhaus documents, examines their evidence boundaries, and adds reproducible B-Tests probes. The new observations compare decimal representations with equivalent exponentiation expressions, repeated descriptions with indexed handles including dictionary cost, reference resolution with current authority in an evaluator-owned CAD implementation, and requested MPLPB actions with independently inspected local effects. They do not constitute an execution of Gelhaus's native controller. In a seeded sample of 512 powers of ten, all 512 exponentiation expressions were shorter than their decimal expansions under the stated encoding; this challenges a general decimal-minimality argument, not OOCC's overall performance. Indexed handles were cheaper in 15 of 20 serialization scenarios and more expensive in five. Four evaluator-reference controls and seven native MPLPB boundary probes met their criteria. New paired model trials and native OOCC comparisons remain NOT_RUN. The review credits useful distinctions in Gelhaus's work, identifies specific unresolved claims, clarifies the evidence level of earlier supplied test-design scripts, and applies the same limitations to MPLPB.

## 1. The question and the objects being tested

The important question is whether a claimed mechanism produces its specified result under inspectable conditions. Counting documents, governance labels, test assertions or retrieved passages does not answer that question by itself.

Gelhaus's public-facing work is not accurately reduced to a single prompt. It includes conceptual arguments, a portable reader procedure, external research and retrieval reports, and descriptions of software prototypes. The October technical paper expressly distinguishes documented artifacts, external workflows, host execution, historical application runs, current native acceptance and comparative validation [G5, PDF pp. 2–3]. The distinction is sound. The present evaluation adopts it.

Three different objects must therefore remain separate: published instructions supplied to a model; an evaluator's implementation of selected ideas; and Gelhaus's actual versioned controller and applications. A fourth object, Combined MPLPB, is a separately developed executable system. Testing one does not automatically test the others.

This is a developer-authored technical review, not an independent certification. The author develops MPLPB and B-Tests and therefore has a direct comparative interest. No new human-reviewed historical accuracy estimate or educational effectiveness result is claimed.

## 2. Materials, provenance and access

The review uses ten supplied PDFs [G1–G10]. Physical PDF page numbers are used throughout; original manuscript-page identifiers inside the research books can differ. File-level SHA-256 values and page counts are retained in `evaluation/public-claims/2026-11-20/sources.json`. Review concentrated on claims, implementation/evidence sections, limitations, attribution and the activation appendix. It is not a line-by-line certification of every page or external reference.

The books preserve overlapping historical manuscripts and checkpoints. Repeated accounts across editions are documentary appearances, not independent replications. The November 3 research edition explicitly preserves earlier source text and distinguishes later supplements from new experimental verification [G9, PDF pp. 1, 7].

The technical paper cites `https://github.com/MrMeNotU/OOCC` and development PR 2 [G5, PDF p. 10]. Both routes returned HTTP 404 during this review on 20 November 2026. This records access failure through those routes. It does not establish whether the project is private, renamed, removed, accessible through another account, or historically nonexistent. No controller was fabricated to fill that access gap.

The underlying private exports, device state and source-held audit packages were not independently acquired or rerun. Their outcomes are attributed to the publications. The new tests use public code and synthetic fixtures only; they do not expose private correspondence or grant access to Gelhaus's accounts.

## 3. Explicit comparison matrix

The six comparisons below have distinct units. Their counts must not be pooled into an architectural accuracy score.

1. **C1 — Numeral encoding.** Compare the decimal spelling of a power of ten with an equivalent Python exponentiation expression. Observe ASCII byte lengths and integer equality, with the shared notation stated explicitly.
2. **C2 — Reference encoding.** Compare repeated expanded referent text with handle uses plus a serialized dictionary entry. Observe total UTF-8 bytes, including the definition.
3. **C3 — Reference versus authority.** Compare B-Tests CADLab handle resolution with that program's separately checked source state and query. Observe scoped resolution, historical-reference status and grant behavior. This is our program.
4. **C4 — Request versus native effect.** Compare a requested action through actual MPLPB with read-only event counts and a local executor marker. Observe whether the guarded adapter actually ran.
5. **C5 — Instruction treatment.** Compare selected published CAD passages with strong conventional instructions, using the same fresh base model and source/task packet. This is a proposed model comparison, NOT_RUN here.
6. **C6 — Native systems.** Compare Gelhaus's runnable native OOCC controller with native MPLPB under matched operations and budgets. This requires actual controller access and independent readbacks; it is NOT_RUN here.

C1 and C2 are analytical and serialization probes. C3 is explicitly our reference implementation, not Gelhaus's software. C4 runs real MPLPB, not an in-memory function labelled "MPLPB-style." C5 uses physical CAD pages 3, 4 and 7, not every OOCC book, personal Memory state or private Orientation. C6 requires the actual system and independently checked effects.

The C5 packets contain identical fictional sources, questions and output requirements. Instructions differ in both wording and length; those lengths are recorded. Any future comparison must hold model snapshot, tools, sampling, output budget and source access constant, use fresh conversations, retain interventions and report truncation. Equal tasks do not remove the instruction-length confound. Exact fact and citation scoring does not by itself certify general semantic correctness.

## 4. What CAD declares and what enforces it

CAD separates Continuity, Authority and Directive. These categories can make task state clearer and errors easier to diagnose. The paper also says CAD is not a conventional compiled programming language and does not enforce access control by itself [G6, PDF pp. 4, 7]. Artificial Tangibility similarly distinguishes human-readable orientation from durable execution infrastructure [G3, PDF pp. 3–5]. Those qualifications should be preserved.

A declaration that a source is current, a draft is unpromoted or an action is forbidden is useful information. It is not evidence that every route to the relevant operation checks that declaration. A model may apply the rule correctly; an application may independently enforce it; a human may supervise it. These are different mechanisms with different failure conditions.

The relevant executable test asks whether a prohibited request reaches an actual adapter, and whether current source and permission checks precede that effect. A natural-language refusal is an observed response. A separate effect file and event-store read can establish a bounded local effect or its absence. Neither observation automatically establishes outside-world truth or completion of a larger task.

This does not refute CAD as a workflow. It limits what follows from its vocabulary alone. Code could enforce CAD-derived policies; such enforcement must be demonstrated in the particular implementation. The same requirement applies to MPLPB: its gates govern checked software entry points, not every action a person or unrelated program could take.

## 5. Canonical tokens: a useful convention and an unsupported inference

The canonical-token paper recommends stable names and handles and connects their reuse to minimal-description ideas. It also makes stronger claims about numbers and references already being at their shortest correct form [G7, PDF pp. 1–3]. These propositions need to be separated.

Stable handles can reduce repeated explanation. That practical observation does not establish that a familiar numeral is a shortest description in algorithmic information theory. For example, `10**1000` specifies the same integer as a decimal one followed by 1,000 zeros, using far fewer characters under a shared exponentiation notation. More generally, a short procedure can generate a highly regular string. A chosen conventional representation and a shortest generating program are different things. Minimal-program length also depends on the chosen interpreter; this experiment does not compute Kolmogorov complexity.

C1 samples 512 distinct exponents uniformly without replacement from 1 through 2,048, using seed 20261120. There is no performance-based acceptance filter. For each exponent, ordinary bounded Python arithmetic checks equality between the decimal string's integer and the corresponding power. The report retains decimal length, expression length and a hash of the decimal spelling. All 512 sampled expressions were shorter. Ten small-integer controls also retain cases where an ordinary literal is shorter than an equivalent expression formed by adding zero.

These numbers describe a deliberately structured family of integers. They are not a random sample of all practical numbers, a tokenizer study, a latency result or 512 independent OOCC failures. One valid counterexample is enough to reject an unrestricted minimality inference; many similar examples do not establish broad performance superiority.

C2 includes the dictionary rather than treating it as free. Four referent lengths and five reuse counts produce 20 serialization scenarios. Handle-plus-dictionary encoding is smaller in 15 scenarios and larger in five. This supports a conditional efficiency claim: indirection can save space when reuse amortizes its definition cost. It does not establish a universal shortest representation, lower model-token use, or cheaper retrieval.

The paper's distinction between documentation and tokenizer internals is appropriate [G7, PDF pp. 3–5]. It does not, however, supply the missing proof of minimality. A stronger formulation would specify the encoding, index availability, reuse count and measured total cost.

## 6. Reference identity is separate from current authority

A stable identifier may correctly designate an old object. It does not follow that the old object currently governs a new action. A fresh session may also lack its dictionary, encounter a namespace collision, or retain a source pointer after permission has been revoked.

C3 uses the existing B-Tests CADLab program to make those distinctions inspectable. It registers a handle for source S1, then creates a valid successor S2. The handle still correctly resolves to S1, while S1 is historical and the current query returns S2's value. Other controls test an unscoped name shared across two namespaces, an absent reference, and a private-source grant before and after revocation. All four controls meet their criteria.

These are successful controls in an evaluator-owned structured workbench. They are neither failures nor passes of Gelhaus's native software. The result also does not refute stable naming: the original handle remains a valid historical reference. It demonstrates why reference resolution, current source status and operation permission should be separately checked.

Gelhaus acknowledges ambiguous introduction and handle reuse as boundary conditions [G7, PDF p. 5]. The remaining empirical question is how reliably a real implementation maintains and verifies those conditions across changes and cold-session recovery.

## 7. Retrieval, continuity and educational evidence

The research book provides unusually useful negative evidence. Its seven-query retrieval diagnostic uses 35 top-five slots per condition. Literal TF-IDF returned 4 directly relevant results, fixed function expansion 6, and unconditional shared-reference graph hopping 3. A hybrid's selected source spans passed 35 of 35 original-byte checks, but that did not establish their semantic relevance. Labels came from a single reviewer after retrieval, and the hybrids reused those labels [G9, PDF pp. 10–12].

The defensible conclusion is narrow: function expansion helped this direct-relevance count, while unconditional graph hopping and several hybrids did not reliably improve it. These measurements do not establish general retrieval quality or a controlled advantage of the whole OOCC architecture. They also cannot be compared numerically with MPLPB's complete-answer rate, because retrieval slots and answer obligations have different denominators and meanings.

The same volume reports a useful recovery episode and a failed requested-manuscript revision despite successful source discovery. It explicitly says the initial failure should not be credited as success because later human intervention recovered the deliverable [G9, PDF pp. 7–8]. The reported archive checks establish bounded structural fidelity, not complete semantic understanding. Those distinctions strengthen the account; they are not evidence of an attempt to conceal every failure.

Headmaster reports an Android prototype and implemented components, while identifying the complete teaching loop, current installed-version verification and independent learning assessment as unfinished [G10, PDF pp. 7–8]. Reported prototype operation is evidence about a prototype. Improved unaided explanation, transfer and retention require the proposed educational experiments. The public activation book likewise says its procedure is not executable software or guaranteed cross-instance continuity [G8, PDF pp. 439–445].

The Object as Filter offers cross-domain conceptual parallels, but acknowledges that Holographic Return lacks a completed public definition in that document [G4, PDF pp. 4–5]. Such analogies may guide design; their recurrence is not a validation of a software mechanism. The byline paper's role-enactment effects are also identified as prospective hypotheses rather than completed controlled outcomes [G1, PDF p. 11].

## 8. Actual native MPLPB controls and their limits

C4 reuses the existing seven-case B-Tests seam adapter against unmodified Combined MPLPB commit `61cc7c04ebdfa84c8d783e005c6e7857c07600b2`. The cases concern a contradictory premise, a claim-only dependency chain, a supported control, a revoked seat, a changed source, an unavailable original, and an export-related supported record without evidence. Read-only SQLite event counts and a real local adapter marker provide effect checks. All seven meet their specified criteria [M1].

The positive control matters: refusing every request would not satisfy the suite. The source and worker files, source pins, command logs and observed results are retained. This is an execution of native MPLPB under authored conditions, not an instruction-level model comparison or a test of Ben's unavailable controller.

MPLPB's own broader limits remain substantial. At the recorded native freeze, the unchanged expanded stress set improved from 168 to 189 complete matches out of 420 with 580 expected refusals preserved. The separate 4,096-case known-weakness study produced 657 complete matches from 1,262 authored answerable cases, 605 misses in eleven classes, and 2,834 expected refusals. Thirty-seven sorter graphs disclosed repeated-phrase budget limits. The historical replay remained three native complete answers, two partials, three conflicts and fourteen abstentions across 22 unchanged questions [M2–M3].

These are different populations, not one combined success rate. They are developer measurements, not independent historical certification. A correctly hashed source can be false. A permitted action can rest on insufficient evidence. A finite checker can contain bugs. A matching citation is not automatically semantic proof. MPLPB's useful software boundary does not establish that the general historical-reconstruction problem is solved.

## 9. Earlier responses and the supplied witness scripts

The earlier response papers and Section 19 material are prior work, not additional new replications [P1–P3]. Gelhaus's earlier Beyond Guarded Retrieval evaluated MPLPB, not the native OOCC controller [G11]. The present paper examines published OOCC/CAD claims and separately identified program controls; the two evaluation directions must not be conflated. The supplied switch-test Markdown matches the existing B-Tests bytes. The supplied witness ZIP matches the already retained archive. The supplied map-response PDF differs from the currently stored edition and is preserved separately with its own hash.

The newly supplied revised Witness PDF is byte-identical to the revised paper already in B-Tests. Its Section 19 specifies a proposed experiment with detection and false-alarm measures, not a claim that the old ZIP constitutes a completed native comparison. The revised paper, the retained historical ZIP, the later filesystem pilot and the actual native probes are distinct artifacts. The limitation below belongs to the old scripted demonstration; it is not presented as an unfixed defect in the revised paper or as evidence that the later real tests did not occur.

The author clarified on 20 November 2026 that the old ZIP was the structure he built to think through ways of testing OOCC and MPLPB. It should therefore be classified as a test-design scaffold: frozen-packet examples, planted error classes, candidate observation functions and proposed detection/false-alarm measures. Prewritten decisions are appropriate for illustrating that structure. They are not observations of how a live model or native controller behaved.

The historical script labels and README must be read under that scope. The scripts produce two-of-four detection counts for their authored values and four-of-five decision disagreements; these demonstrate the scoring arrangement, not an empirical architectural winner. In particular, an effect-only observer can miss an inherited contradiction or misclassify a correct refusal if it lacks current authority and reporting context. That is a reason to improve the experiment design, not evidence that the author had no real tests.

The later B-Tests filesystem pilot uses actual subprocess-created files, and its native probes invoke the real MPLPB program. Their observations are documented separately [P3]. The original ZIP remains unchanged; a dated author-intent note accompanies it. This review credits the design contribution, the revised paper and the later executions without double-counting their evidence or attributing native performance to the scaffold.

## 10. Credit, reproducibility and the next fair test

The supplied research volume explicitly credits McPhetridge's Dual-System Architecture, bridge-language load testing and externalized cognitive-runtime work [G2, PDF p. 143]. It would be inaccurate to say these papers never acknowledge that influence. Citation does not independently resolve every priority or implementation-provenance question, but such questions require actual source histories and code comparisons.

Likewise, an evaluator may legitimately test MPLPB through its native writer and answer API. The implementation and pre-existing test infrastructure remain McPhetridge's contribution; newly authored fixtures, questions and analysis remain the evaluator's contribution. These ten OOCC papers do not establish that a particular later evaluation used M6. No unavailable harness is inferred or given an invented capability.

The next discriminating study should compare published CAD instructions with strong conventional source governance using the same model and source access, and compare native systems only when both are available. It should freeze tasks and criteria before execution, include supported actions as well as prohibited ones, preserve missing and contradictory evidence, and retain every failure. An evaluator-owned reference program belongs in a labelled control arm.

Primary outcomes should be correct bounded deliverables, unnecessary refusals, incorrect answers, source/version fidelity, verified effects, preservation of corrections, human intervention and resource costs. Fresh-session transfer must be observed rather than asserted. New model configuration, usage, independent semantic accuracy, human review time and native OOCC performance remain null or NOT_RUN in the present release.

## 11. Conclusion

OOCC contains useful distinctions and reported engineering work that deserve direct examination. Its public reader method is a structured procedure delivered through instructions; its broader architecture also includes reported workflows and software components. Declared rules, prototype existence, exact source retrieval, reference resolution, native integration and comparative benefit are distinct evidentiary achievements.

The present probes expose a bounded mathematical overstatement, demonstrate conditional reference compression, and verify selected behavior in two explicitly identified programs. They do not establish a global winner. Testing OOCC fairly means making its claims executable and inspectable where possible, preserving unavailable tests as unavailable, and applying the same standards to MPLPB.

## References

G1–G10 identify Benjamin Gelhaus's ten supplied papers. G11 is his earlier MPLPB evaluation, cited as prior context rather than newly reproduced here. Page references identify physical PDF pages. Exact supplied filenames, hashes and page counts are in the companion source inventory; the original third-party PDFs are not redistributed here.

[G1] Gelhaus, Benjamin. The Contribution Is Not the Byline: Role-Enacted Human–AI Collaboration, Intellectual Provenance, and Accountable Research. Revised edition v1.1, 7 November 2026. 12 pages.

[G2] Gelhaus, Benjamin. OOCC / Functional Layers master research volume, supplied public reader edition. File OOCC_FUNCTIONAL_LAYERS_MASTER_RESEARCH_B.pdf. 439 pages. Use the file hash to distinguish editions; this review does not infer one publication date for every incorporated chapter.

[G3] Gelhaus, Benjamin. Artificial Tangibility as a Low-Infrastructure Governance Layer for AI State Management. Supplied manuscript, 2026. 6 pages.

[G4] Gelhaus, Benjamin. The Object as Filter: Holographic Return, AI Continuity, and Human-Readable Interfaces. Supplied manuscript, 2026. 7 pages.

[G5] Gelhaus, Benjamin. From Work Exhaust to Source-Governed Collaborative Continuity. OOCC Research Paper v0.16, 26 October 2026. 10 pages. Supplied filename begins Condensed_technical_paper_derived_from_t.

[G6] Gelhaus, Benjamin. Continuity, Authority, Directive: A Plain-Language Control Grammar for AI Work. Supplied CAD Control Grammar manuscript, 2026. 8 pages.

[G7] Gelhaus, Benjamin. Canonical Tokens: A Minimal-Representation Principle for AI-Assisted Continuity. Supplied manuscript, 2026. 6 pages.

[G8] Gelhaus, Benjamin. No More First Dates With AI. Supplied updated public reader edition. 445 pages; activation appendix at physical PDF pages 439–445.

[G9] Gelhaus, Benjamin. OOCC / Voltron: Complete Native-Source Research Edition + Longitudinal Feasibility Addendum. Original research dated 2 November 2026; PDF conversion dated 3 November 2026. 202 physical PDF pages.

[G10] Gelhaus, Benjamin. Headmaster: From Verbatim Evidence to Independent Understanding. November 2026 manuscript. 10 pages.

[G11] Gelhaus, Benjamin. Beyond Guarded Retrieval: A Source-Bounded Evaluation of Combined MPLPB and a Roadmap for Historical Reconstruction. Stated 14 November 2026. https://www.academia.edu/181013727/Beyond_Guarded_Retrieval_A_Source_Bounded_Evaluation_of_Combined_MPLPB_and_a_Roadmap_for_Historical_Reconstruction . Prior attribution and pinned-run scope are retained in B-Tests `docs/GELHAUS_EXTERNAL_EVALUATION.md`; no private benchmark reproduction is claimed here.

[M1] McPhetridge, Mitchell D. B-Tests public-claims experiment, 20 November 2026. `research_lab/public_claims.py`; `evaluation/public-claims/2026-11-20/observed`. Native MPLPB source: https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/tree/61cc7c04ebdfa84c8d783e005c6e7857c07600b2 . Code and result hashes identify this experiment separately from its B-Tests baseline ancestry.

[M2] McPhetridge, Mitchell D. Source-grounded field-alias iteration. 20 November 2026. https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/61cc7c04ebdfa84c8d783e005c6e7857c07600b2/evaluation/field-aliases/2026-11-20/REPORT.md .

[M3] McPhetridge, Mitchell D. D% known-weakness study. 20 November 2026. https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/blob/61cc7c04ebdfa84c8d783e005c6e7857c07600b2/evaluation/dpercent-known-weaknesses/2026-11-20/REPORT.md .

[P1] McPhetridge, Mitchell D. Probabilistic Prompts and MPLPB Deterministic Contracts: The 8 a.m. Switch Test for Instructions and Effects. 18 November 2026. `docs/paper/PROBABILISTIC_PROMPTS_AND_MPLPB_CONTRACTS.md`.

[P2] McPhetridge, Mitchell D. MPLPB and OOCC/CAD: Comparative Experiments / When the Map Becomes the Authority. Prior supplied and repository editions are distinguished by the paper archive manifest. `docs/paper/WHEN_THE_MAP_BECOMES_THE_AUTHORITY.md`.

[P3] McPhetridge, Mitchell D. The Witness Inside the Machine, Section 19 experiments and B-Tests replication audit. `evaluation/witness-section19/RESULTS.md`; supplied experiment ZIP SHA-256 0322c429a214752d25b3ede08567a8f76d2a8ed894a10fdd23f742f96ca1d395 . Original scripted records, later filesystem controls and native execution records are separate evidence.
