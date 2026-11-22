# Effect of evaluator separation on overall judgment

Frozen run root hash: `a87a121bdeccbc6371ab1ca24751df4f0ca5c62bcc9974ae2a664e93a307c9dd`

**Result: CONFOUNDED_NO_VERDICT** (basis: all judges, mixed evidence (confounded: no clean stratum available yet))

- BA rises with level across these judges, but they see different evidence (I4 reads state, I0/I1 don't), so separation and information access can't be told apart. Add model judges at two or more levels in the same evidence mode.

BA averages detection on incorrect cases and acceptance on correct cases. Abstentions count as missed decisions in BA. F counts only rejections of correct cases. J = E − F. Coverage counts non-abstaining verdicts. Slope = change in BA per separation level; p = one-sided stratified permutation test (5000 permutations, alpha 0.05).

## all_judges

Slope: +0.092 BA per level, p = 0.0002. I0 → I4: ΔE +0.80, ΔF +0.00, ΔBA +0.40.

| Judge | Level | BA | E | F | J | Coverage |
|---|---|---|---|---|---|---|
| I0_self_assessment | I0 | 0.500 | 0.0% | 0.0% | +0.000 | 100.0% |
| I1_same_frame | I1 | 0.710 | 42.0% | 0.0% | +0.420 | 100.0% |
| I4_retained_state | I4 | 0.900 | 80.0% | 0.0% | +0.800 | 100.0% |

