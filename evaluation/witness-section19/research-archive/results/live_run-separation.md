# Effect of evaluator separation on overall judgment

Frozen run root hash: `a87a121bdeccbc6371ab1ca24751df4f0ca5c62bcc9974ae2a664e93a307c9dd`

**Result: MIXED** (basis: model judges within one evidence mode)

- adding state changed BA by ≥0.05 in 2 of 3 paired conditions; compare that with the separation slope before crediting separation

BA averages detection on incorrect cases and acceptance on correct cases. Abstentions count as missed decisions in BA. F counts only rejections of correct cases. J = E − F. Coverage counts non-abstaining verdicts. Slope = change in BA per separation level; p = one-sided stratified permutation test (5000 permutations, alpha 0.05).

## model_report_only

Slope: -0.004 BA per level, p = 0.6127. I0 → I3: ΔE -0.10, ΔF -0.07, ΔBA -0.05.

| Judge | Level | BA | E | F | J | Coverage |
|---|---|---|---|---|---|---|
| I0_model__report_only__qwen2.5-1.5b | I0 | 0.125 | 10.0% | 7.5% | +0.025 | 19.3% |
| I2_fresh__report_only__qwen2.5-1.5b | I2 | 0.268 | 21.0% | 27.5% | -0.065 | 50.7% |
| I3_cross__report_only__smollm2-360m | I3 | 0.075 | 0.0% | 0.0% | +0.000 | 10.0% |

## model_report_plus_state

Slope: +0.080 BA per level, p = 0.0002. I0 → I3: ΔE +0.16, ΔF +0.10, ΔBA +0.27.

| Judge | Level | BA | E | F | J | Coverage |
|---|---|---|---|---|---|---|
| I0_model__report_plus_state__qwen2.5-1.5b | I0 | 0.125 | 10.0% | 10.0% | +0.000 | 20.0% |
| I2_fresh__report_plus_state__qwen2.5-1.5b | I2 | 0.175 | 25.0% | 22.5% | +0.025 | 28.6% |
| I3_cross__report_plus_state__smollm2-360m | I3 | 0.393 | 26.0% | 20.0% | +0.060 | 77.1% |

## all_judges

Slope: +0.064 BA per level, p = 0.0002. I0 → I4: ΔE +0.73, ΔF -0.06, ΔBA +0.65.

| Judge | Level | BA | E | F | J | Coverage |
|---|---|---|---|---|---|---|
| I0_model__report_only__qwen2.5-1.5b | I0 | 0.125 | 10.0% | 7.5% | +0.025 | 19.3% |
| I0_model__report_plus_state__qwen2.5-1.5b | I0 | 0.125 | 10.0% | 10.0% | +0.000 | 20.0% |
| I0_self_assessment | I0 | 0.500 | 0.0% | 0.0% | +0.000 | 100.0% |
| I1_same_frame | I1 | 0.710 | 42.0% | 0.0% | +0.420 | 100.0% |
| I2_fresh__report_only__qwen2.5-1.5b | I2 | 0.268 | 21.0% | 27.5% | -0.065 | 50.7% |
| I2_fresh__report_plus_state__qwen2.5-1.5b | I2 | 0.175 | 25.0% | 22.5% | +0.025 | 28.6% |
| I3_cross__report_only__smollm2-360m | I3 | 0.075 | 0.0% | 0.0% | +0.000 | 10.0% |
| I3_cross__report_plus_state__smollm2-360m | I3 | 0.393 | 26.0% | 20.0% | +0.060 | 77.1% |
| I4_retained_state | I4 | 0.900 | 80.0% | 0.0% | +0.800 | 100.0% |

## Evidence access at a fixed level

| Level | Model | BA report only | BA report + state | Δ |
|---|---|---|---|---|
| I0 | qwen2.5-1.5b | 0.125 | 0.125 | +0.000 |
| I2 | qwen2.5-1.5b | 0.268 | 0.175 | -0.093 |
| I3 | smollm2-360m | 0.075 | 0.393 | +0.318 |
