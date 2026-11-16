# Public-paper comparison

MPLPB commit: `614b18cc34f5270d4cb7dfbbf8239391a9f83b31` (post-PR #43 main observed at acquisition).

B-Tests commit: `4eae0a8a2fd2db252220390b31c2d0ac1183994c`.

Profile: `Profile("open", None, True)`; page timestamp: `2026-11-01T00:00Z`.

## Materials and extraction

Ten supplied PDF documents were extracted with PyMuPDF 1.26.6, first 15 physical pages or full if shorter. Text is unedited `get_text("text")` output concatenated in physical page order; PDF extraction can affect layout and reading order. The separately supplied Beyond Guarded Retrieval TXT is included verbatim as an additional source, not described as an extracted PDF. Pages after 15 are absent from this run. No inferred definitions, scope synonyms or answers were added.

The requested clone/attachment paths initially did not exist. Fresh public clones were acquired at the requested paths. Nine PDFs and the TXT came from the current attachment batch; the earlier attached No More First Dates PDF supplies the tenth PDF. Source-byte hashes, page ranges, extracted-text hashes and sealed ledger identities are in `manifest.json`. These hashes permit matching supplied files independently of their local filenames.

| Paper | Pages extracted / total | Extracted-text SHA-256 |
|---|---|---|
| Artificial_Tangibility_as_a_Low_Infrastr.txt | 6 / 6 | `dfe5e7a8c4e16b262c628777dde75301275e6d355b74ca295756fb382f19d5ff` |
| CAD_Control_Grammar_Continuity_Authority.txt | 8 / 8 | `d25dce7f65533947dc4e743f5fbb96e0ac9fad9006d3064d8bf017174ca0ecb3` |
| Canonical_Tokens_A_Minimal_Representatio.txt | 6 / 6 | `aa989e813e03d13ccbaf665f5c84fd0acf0a2c219d908affc7215d2083991376` |
| Condensed_technical_paper_derived_from_t.txt | 10 / 10 | `4c6824b821560a244e91b271b5791cca7f068454135e34c844235054c03c54bd` |
| From_Verbatim_Evidence_to_Independent_Un.txt | 10 / 10 | `1117f6629ba26b0083e503be893576dd37f29df102cc50c5ac77770fd2d12e3d` |
| No_More_First_Dates_With_AI_updated_Publ.txt | 15 / 445 | `5a639ac128a340b58aaf4a65b11614765375e0e24a493a12df7361c28bd78bd6` |
| OOCC_FUNCTIONAL_LAYERS_MASTER_RESEARCH_B.txt | 15 / 439 | `b72c344a35c5cfadbce55a251527f0efa05bf5838227af1c3a7e14d1889fb8db` |
| OOCC_Research_Book_with_longitudinal_add.txt | 15 / 202 | `f80423d2bfc621a688b04c5352f1ac57825c57644677d66acee4cf4f782ecc52` |
| THE_CONTRIBUTION_IS_NOT_THE_BYLINE.txt | 12 / 12 | `94f84234dc3ccdb90190932e0560360c0c03c6d65ac8a90bad49322aaf17c61f` |
| The_Object_as_Filter_The_Object_as_Filte.txt | 7 / 7 | `f015638de135cb51372fa5bc845b5f7e033bd2a8ffdf30e0b9a409e0fa98e4d0` |
| BEYOND-GUARDED-RETRIEVAL.txt | Supplied TXT (full) | `de8177334db54542a88515fe4d24a0c4fa531dbe03a53d652890ff4d4e21fd11` |

## Ledger and source status

All extracted texts and the supplied TXT were loaded through native `write`, with title and scope equal to each short name, and native `seal` was explicitly called after each write. Native `write` already produces hash-sealed records, so the subsequent `seal` calls return empty lists; every page was independently reloaded and its hash/intact state checked, and all pages were servable. No ratification, extra relationship, promotion, hand-edited source metadata or model-generated answer was added. The imported page's origin metadata follows `write`'s default; source authorship is explicitly unknown. Sealing proves the local content identity, not factual correctness or independently authenticated authorship.

## Complete query results

`queries.json` retains the complete native `Answer.to_dict()` (including full returned text and diagnostics), dataclass fields, and preview. The table shows the requested 250-character preview. “Absent” means this reader's Answer has no `answer_supported` field; it must not be interpreted as true. `return` selects a whole source page, not an independently inferred answer to a proposition.

| Query | kind | text[:250] | answer_supported | Diagnostic |
|---|---|---|---|---|
| What is Continuity in CAD? | return | CAD Control Grammar Continuity Authority<br>CAD Control Grammar Continuity, Authority, Directive: A Plain-Language Control Grammar for AI Work Benjamin Gelhaus Independent Researcher Abstract Long-running AI-assisted work often fails not because the sys | Absent | {"reason": "exactly one current page owns this question by declared scope", "known": ["cad", "continuity"], "unknown": [], "matched_on": "scope", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0002", "path": "paper-0002.html", "scope": "CAD Control Grammar Continuity Authority", "matched": ["cad", "continuity"]}], "withheld": [], "set_aside": []} |
| What does Authority distinguish? | ambiguous |  | Absent | {"reason": "no page owns this by scope, and two or more contain every word of it", "known": ["authority", "distinguish"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0001", "path": "paper-0001.html", "scope": "Artificial Tangibility as a Low Infrastr", "matched": ["authority", "distinguish"]}, {"id": "PAPER-0002", "path": "paper-0002.html", "scope": "CAD Control Grammar Continuity Authority", "matched": ["authority", "distinguish"]}, {"id": "PAPER-0004", "path": "paper-0004.html", "scope": "Condensed technical paper derived from t", "matched": ["authority", "distinguish"]}, {"id": "PAPER-0007", "path": "paper-0007.html", "scope": "OOCC FUNCTIONAL LAYERS MASTER RESEARCH B", "matched": ["authority", "distinguish"]}, {"id": "PAPER-0011", "path": "paper-0011.html", "scope": "BEYOND GUARDED RETRIEVAL", "matched": ["authority", "distinguish"]}], "withheld": [], "set_aside": []} |
| Is CAD only prompt-level guidance? | ambiguous |  | Absent | {"reason": "no page owns this by scope, and two or more contain every word of it", "known": ["cad", "guidance", "level", "prompt"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0002", "path": "paper-0002.html", "scope": "CAD Control Grammar Continuity Authority", "matched": ["cad", "guidance", "level", "prompt"]}, {"id": "PAPER-0006", "path": "paper-0006.html", "scope": "No More First Dates With AI updated Publ", "matched": ["cad", "guidance", "level", "prompt"]}], "withheld": [], "set_aside": []} |
| What is Directive? | ambiguous |  | Absent | {"reason": "no page owns this by scope, and two or more contain every word of it", "known": ["directive"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0001", "path": "paper-0001.html", "scope": "Artificial Tangibility as a Low Infrastr", "matched": ["directive"]}, {"id": "PAPER-0002", "path": "paper-0002.html", "scope": "CAD Control Grammar Continuity Authority", "matched": ["directive"]}, {"id": "PAPER-0003", "path": "paper-0003.html", "scope": "Canonical Tokens A Minimal Representatio", "matched": ["directive"]}, {"id": "PAPER-0006", "path": "paper-0006.html", "scope": "No More First Dates With AI updated Publ", "matched": ["directive"]}, {"id": "PAPER-0009", "path": "paper-0009.html", "scope": "THE CONTRIBUTION IS NOT THE BYLINE", "matched": ["directive"]}, {"id": "PAPER-0010", "path": "paper-0010.html", "scope": "The Object as Filter The Object as Filte", "matched": ["directive"]}], "withheld": [], "set_aside": []} |
| What is Artificial Tangibility? | return | Artificial Tangibility as a Low Infrastr<br>Artificial Tangibility as a Low-Infrastructure Governance Layer for AI State Management Benjamin Gelhaus Independent Researcher Abstract This companion paper situates Artificial Tangibility in relation to cont | Absent | {"reason": "exactly one current page owns this question by declared scope", "known": ["artificial", "tangibility"], "unknown": [], "matched_on": "scope", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0001", "path": "paper-0001.html", "scope": "Artificial Tangibility as a Low Infrastr", "matched": ["artificial", "tangibility"]}], "withheld": [], "set_aside": []} |
| Does retrieval alone determine authority? | ambiguous |  | Absent | {"reason": "no page owns this by scope, and two or more contain every word of it", "known": ["alone", "authority", "determine", "retrieval"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0001", "path": "paper-0001.html", "scope": "Artificial Tangibility as a Low Infrastr", "matched": ["alone", "authority", "determine", "retrieval"]}, {"id": "PAPER-0002", "path": "paper-0002.html", "scope": "CAD Control Grammar Continuity Authority", "matched": ["alone", "authority", "determine", "retrieval"]}], "withheld": [], "set_aside": []} |
| What is the DHS Translation Protocol? | return | From Verbatim Evidence to Independent Un<br>HEADMASTER From Verbatim Evidence to Independent Understanding A Function-First, Source-Grounded AI Teaching System<br>Benjamin Gelhaus Object-Oriented Cognition and Continuity (OOCC) / Voltron Research manuscrip | Absent | {"reason": "no page owns this by scope; exactly one contains every word of it", "known": ["dhs", "protocol", "translation"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0005", "path": "paper-0005.html", "scope": "From Verbatim Evidence to Independent Un", "matched": ["dhs", "protocol", "translation"]}], "withheld": [], "set_aside": []} |
| Does Headmaster preserve the learner's original answers? | return | From Verbatim Evidence to Independent Un<br>HEADMASTER From Verbatim Evidence to Independent Understanding A Function-First, Source-Grounded AI Teaching System<br>Benjamin Gelhaus Object-Oriented Cognition and Continuity (OOCC) / Voltron Research manuscrip | Absent | {"reason": "no page owns this by scope; exactly one contains every word of it", "known": ["answers", "headmaster", "learner", "original", "preserve"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0005", "path": "paper-0005.html", "scope": "From Verbatim Evidence to Independent Un", "matched": ["answers", "headmaster", "learner", "original", "preserve"]}], "withheld": [], "set_aside": []} |
| source authority | ambiguous |  | Absent | {"reason": "no page owns this by scope, and two or more contain every word of it", "known": ["authority", "source"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0001", "path": "paper-0001.html", "scope": "Artificial Tangibility as a Low Infrastr", "matched": ["authority", "source"]}, {"id": "PAPER-0002", "path": "paper-0002.html", "scope": "CAD Control Grammar Continuity Authority", "matched": ["authority", "source"]}, {"id": "PAPER-0003", "path": "paper-0003.html", "scope": "Canonical Tokens A Minimal Representatio", "matched": ["authority", "source"]}, {"id": "PAPER-0004", "path": "paper-0004.html", "scope": "Condensed technical paper derived from t", "matched": ["authority", "source"]}, {"id": "PAPER-0006", "path": "paper-0006.html", "scope": "No More First Dates With AI updated Publ", "matched": ["authority", "source"]}, {"id": "PAPER-0007", "path": "paper-0007.html", "scope": "OOCC FUNCTIONAL LAYERS MASTER RESEARCH B", "matched": ["authority", "source"]}, {"id": "PAPER-0010", "path": "paper-0010.html", "scope": "The Object as Filter The Object as Filte", "matched": ["authority", "source"]}, {"id": "PAPER-0011", "path": "paper-0011.html", "scope": "BEYOND GUARDED RETRIEVAL", "matched": ["authority", "source"]}], "withheld": [], "set_aside": []} |
| Continuity Authority Directive | return | CAD Control Grammar Continuity Authority<br>CAD Control Grammar Continuity, Authority, Directive: A Plain-Language Control Grammar for AI Work Benjamin Gelhaus Independent Researcher Abstract Long-running AI-assisted work often fails not because the sys | Absent | {"reason": "exactly one current page owns this question by declared scope", "known": ["authority", "continuity", "directive"], "unknown": [], "matched_on": "scope", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0002", "path": "paper-0002.html", "scope": "CAD Control Grammar Continuity Authority", "matched": ["authority", "continuity"]}], "withheld": [], "set_aside": []} |
| What is the capital of France? | not_in_corpus |  | Absent | {"reason": "no current page declares most of this question, and no page contains every word of it", "known": [], "unknown": ["capital", "france"], "matched_on": "", "quarantined": 0, "route": [], "candidates": [], "withheld": [], "set_aside": []} |
| unprepared original source records | return | BEYOND GUARDED RETRIEVAL<br>BEYOND GUARDED RETRIEVAL \| GELHAUS 2026 The most practical path forward preserves the existing source-authority machinery and introduces targeted extensions: precise refusal diagnostics, exact-field source routing, event cand | Absent | {"reason": "no page owns this by scope; exactly one contains every word of it", "known": ["original", "records", "source", "unprepared"], "unknown": [], "matched_on": "prose", "quarantined": 0, "route": [], "candidates": [{"id": "PAPER-0011", "path": "paper-0011.html", "scope": "BEYOND GUARDED RETRIEVAL", "matched": ["original", "records", "source", "unprepared"]}], "withheld": [], "set_aside": []} |

## Public B-Tests commands

- `unittest`: **PASS**, exit 0; complete stdout/stderr retained next to this report.
- `native_evidence`: **PASS**, exit 0; complete stdout/stderr retained next to this report.

Unit-test count: **121**. These are laboratory tests, not additional OOCC/CAD target trials.

`research_lab.native_evidence` reads public retained files only and makes zero new target executions or model requests. Its historical pins are not the current MPLPB pin above; replaying those records does not newly validate the PR #43 implementation. No private adapter was needed or used.

## Not tested because not public

- Live OOCC controller.
- Memory/Drive/SQL scheduler.
- Recipient acceptance.
- Unprepared original source records (matching the private benchmark packages).
- Live adapter and independent readbacks.
- E4 native integration acceptance.
- E5 comparative validation.
- Controlled operator-burden and re-entry measurements.
- Reciprocal blinded scoring.

These labels follow the requested unavailable-evidence list; labels alone do not establish that a private package was examined. Matching a phrase in a public paper does not test the underlying private records. No private Drive, SQL, or controller paths were accessed. The temporary local ledger is a public-text fixture, not Ben's live system.

## Observed source-authority behavior

On these public-text excerpts, the strict reader produced 5 ambiguous, 1 not_in_corpus, 6 return, returning only selected sealed page text and abstaining on unresolved ownership; these outputs do not independently verify the papers' factual claims.

This is the complete inspectable public comparison **within the requested first-15-pages, strict-reader and public-command scope**; it is not an exhaustive evaluation of every published page or all MPLPB capabilities. Private items remain **NOT_RUN** until furnished under the same version pins and blinded scoring. There is no global architectural victory claim.

## Reproduction

The public clones and supplied attached PDFs/TXT are the only evidence inputs. Extraction requires `PyMuPDF==1.26.6`; repository source files are unmodified. `freeze.json` records the implementation pins, query list, profile, extractor version and runner hash before execution. Original PDFs are not copied into the evaluation directory.

```sh
python evaluation/public-papers/run.py --mplpb-root /workspace/mplpb --b-tests-root /workspace/b-tests --attachments /workspace/attachments --ledger /tmp/public-paper-ledger-repeat --output /tmp/public-paper-repeat
```

Use a fresh ledger path for each run. Exact text hashes, record content hashes and query decisions are deterministic with identical input bytes, PyMuPDF version and code pins. Temporary-root paths, unit-test durations and incidental diagnostic log paths can differ. Preserve original filenames from the attachment staging described above so short-name scopes remain identical.

A fresh-ledger repeat at `/tmp/public-paper-ledger-repeat` produced identical extracted-text/ledger manifests and identical complete query records after excluding only the temporary `root` path. See `determinism-check.json`. Repeated laboratory tests passed again; they do not add independent coverage.
