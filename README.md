# B-Tests: testing OOCC against its own claims

**Mitchell D. McPhetridge — November 15, 2026**

Ben asked me to test his work. This repository is my attempt to do that rigorously. I am testing **Object-Oriented Cognition and Continuity (OOCC), the Continuity–Authority–Directive (CAD) grammar, Artificial Tangibility, and Functional Layers** against the claims, warnings, limitations, and proposed falsifiers in Ben's own manuscripts.

**I am trying to falsify the claims, not repair the system.** A result should either strengthen a precisely defined claim, narrow it, or leave it unestablished. A persuasive explanation does not pass a test.

## Why I am testing the map

My central concern is simple: **what happens when the map becomes the authority?**

A continuity map may help a new AI session find the right work. But an outdated map, a strong priority weight, or an approved document may also mislead that session. If a system begins treating its own relational interpretation as proof, it could turn an organizing vocabulary into an enforced single explanation across unrelated domains. I call this the **monism/over-unification risk**. I am testing that risk as a possible system behavior, not accusing the researcher of holding it.

The critical questions are:

1. Does a current original source defeat a stale or high-weight orientation map?
2. Can a human-approved false statement be kept separate from what evidence establishes?
3. Does OOCC preserve multiple historical explanations without inventing causal influence?
4. Can fresh runtimes actually recover **verified final work** better than strong alternatives under matched access and cost?
5. Are source reads, worker acknowledgments, revocations, device execution, and completed artifacts independently observable?
6. Can Functional Layers forecast unseen outcomes better than domain-only and generic dependency baselines, using rules frozen *before* the outcomes?
7. When an experiment yields no advantage—or makes things worse—does the claim contract rather than absorb the failure as another confirming pattern?

## What counts as evidence

| Result | Meaning |
|---|---|
| **DOCUMENTED** | I located the exact claim or limitation in a versioned paper. Not an implementation result. |
| **PASS_NATIVE** | The tested, pinned OOCC implementation satisfied the specified observable criterion, including necessary independent readback. |
| **FAIL_NATIVE** | The tested implementation violated a preregistered criterion. Preserve its logs and version. |
| **PASS_STUDY / FAIL_STUDY** | A properly controlled study produced the prespecified comparative result. |
| **NOT_RUN** | I did not have the executable, source permission, participants, device, or holdout required to make the measurement. |
| **INCONCLUSIVE** | The run took place but evidence cannot decide the result. |
| **OUT_OF_SCOPE** | The requirement was not claimed for that version. It cannot be used as a manufactured failure. |

My independent reference code is a **control fixture**, not Ben's software. When those tests pass, only the control fixture passes. A source passage being present does not prove the claim it describes. A worker writing “ACK” does not prove a different worker read anything.

## What I am using from Ben's own work

I am testing his **seven CAD evaluation criteria**, **four Canonical Tokens criteria**, **five OOCC v0.16 experiment families**, the **15 named failure tests** in *No More First Dates With AI*, the **Headmaster three-arm learning study**, the **2×2 role/enactment trial**, Artificial Tangibility's promotion and provenance boundaries, and the **blinded prospective Functional Layers prediction protocol**.

Ben's own publication also supplies negative evidence: in the reported V3 CP005 post-hoc top-five retrieval ablation, unconditional graph-hop produced **3/35 direct results**, versus **6/35** for function expansion. It was *not* an independently adjudicated holdout. I retain that negative result rather than rewriting it as proof of relational improvement (*OOCC: The Unified Intersection*, physical PDF pp. 351–353).

Ben explicitly calls complete continuous autonomy, causal proof from graph matches, and general comparative advantage unestablished in the supplied version (*Unified Intersection*, pp. 386–390). The goal is to test those boundaries and future stronger claims, not pretend he has already claimed to prove them.

## Repository map

- [PROTOCOL.md](PROTOCOL.md): twenty adversarial acceptance scenarios and falsifiers.
- [fixtures/reciprocal_development_manifest.json](fixtures/reciprocal_development_manifest.json): synthetic development sources and case definitions; **not** a sealed holdout.
- [oocc_lab/engine.py](oocc_lab/engine.py): my independent CAD-style control implementation; **not** an OOCC reproduction.
- [tests/](tests/): executable local negative controls and regression checks.
- [docs/AUTHOR_FALSIFIERS.md](docs/AUTHOR_FALSIFIERS.md): test coverage traced to the individual source papers.
- [tools/run_author_falsifiers.py](tools/run_author_falsifiers.py): black-box runner for the additional paper-derived cases.

**Known boundary:** the current uploaded materials do not include an authenticated, callable copy of Ben's native Android controller or private source archives. Those end-to-end tests remain **NOT_RUN** until a pinned implementation and lawful test access are supplied.

## The rule

I won't patch a failing implementation and pretend the original passed. I won't count a missing experiment as a failure. I won't allow a friendly substitute implementation to validate the author’s native system. I will preserve negative results and the source evidence behind them.

**The tests decide how far the claim goes—not the other way around.**
