# Preregistration (fill in, commit, and publish the hash before any model judging)

Commit this file with the run's root hash. Anything changed after that is an
exploratory result, labelled as such.

## 1. Run

- Generator version: ______ (record the version from run.json)
- Seed: ______ (drawn how: ______)
- Cases per class: ______  (total = 7 × per-class)
- Root sha256 from `wie freeze`: ______
- Where the sealed key is kept, and who can read it: ______

## 2. Pilot (optional, its own seed, never reused)

- Pilot seed: ______
- What the pilot is for: estimating variance and the size of differences only.
- Per-class count chosen for the confirmatory run, and why: ______

## 3. Judges

| Label | Model and version / person | Session rules (fresh? memory off?) | Evidence modes |
|---|---|---|---|
| I0_model | | given ARTIFACT.md | report_only, report_plus_state |
| I2_fresh | | fresh session, same family as I0_model | both |
| I3_cross | | different family | both |
| I5_human (optional) | | | |

Every model judge sees each batch once. No retries unless output is malformed;
malformed batches are rerun in a new session and the rerun is logged here: ______

## 4. Primary comparisons (fixed now)

On the same planted-incorrect cases, exact McNemar, two-sided, alpha = ______:

1. I0_model vs I2_fresh, report_plus_state
2. I2_fresh vs I3_cross, report_plus_state
3. I0_model report_only vs I0_model report_plus_state (information access, not separation)
4. Best model judge vs I4_retained_state on interpretive_misattribution

## 4b. Headline test (fixed now)

`wie separation`, balanced accuracy vs separation level, one-sided stratified
permutation test, ______ permutations (≥5000), Holm across evidence modes,
alpha = ______. Strata: model judges within `report_only`, and within
`report_plus_state`. Mixed-evidence results are reported but are not a verdict.

## 5. Decision rules (from §19.7, §19.8 and §21)

The paper **gains support** if, on preregistered comparisons:
- a more separated judge has higher E at the same or similar evidence mode, and
- its F is not higher by more than ______ percentage points, so J improves.

The paper **is weakened** if:
- I0_model matches I2_fresh and I3_cross on E within ______ points, or
- separated judges gain E only with an equal or larger rise in F (J flat), or
- the evidence-mode difference explains all of the gain (comparison 3 is large,
  comparisons 1–2 are null).

Mixed results: the framework contracts to the separations that improved J.

## 6. Exclusions

Cases excluded only for: ______ (decide now; "the judge did badly" is not one).

## 7. Deviations

Anything done differently from the above, with date and reason: ______
