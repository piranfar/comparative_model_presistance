# Supplemental material

**Score only the kill the assay can see: starting density and the floor bound every MDK**

Vahhab Piranfar

This file contains 7 supplemental tables, Table S1 to Table S7, each with its legend. Every one is cited in the manuscript text.

---

Held here so the Results stay on one line of reasoning. Table S6 supports Section 10 and Table S5 supports Section 6.

**Table S1.** The comparison the Methods promise: rows dropped from the association family against rows retained, on starting density and susceptibility. The MDR exclusion differs in susceptibility by construction, since those isolates are outside the resistant-versus-susceptible contrast the family tests. The one difference not by construction is in the 60-day panel, where the dropped rows sit higher in starting density (p = 0.027); it affects 20 rows and no conclusion drawn from that panel.

| Panel | Exclusion | Dropped | Retained | Median log10 N0 retained | Median log10 N0 dropped | p | Resistant, retained | Resistant, dropped | p  |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 15-day | label missing or 'MDR' | 14 | 202 | 5.79 | 5.36 | 0.198 | 41% | 0% | 0.001 |
| 15-day | growth proxy missing | 1 | 202 | 5.79 | 6.79 | 0.149 | 41% | 100% | 0.414 |
| 60-day | label missing or 'MDR' | 20 | 196 | 7.36 | 7.79 | 0.027 | 40% | 20% | 0.093 |
| 60-day | growth proxy missing | 1 | 196 | 7.36 | 7.36 | 0.749 | 40% | 100% | 0.406 |

**Table S2.** The ordinal reanalysis against the linear model it replaces, member for member. The linear model scores the ordering 0, 1, 2, which assumes the two class steps are equal; the ordinal model does not. Every direction agrees and the same two members survive correction under both, so the linear treatment did not manufacture the result -- but the coefficients it reports are in a unit that does not exist, which is why the ordinal fit is the one in the main table.

| Predictor | Prior culture | Reading day | Linear beta | p (linear) | Survives BH | Odds ratio | p (ordinal) | Survives BH  | Same direction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| time to OD 0.4 | 15 d | day 5 | +0.0266 | 0.0025 | yes | 1.096 | 0.0030 | yes | yes |
| resistance | 15 d | day 5 | +0.2589 | 0.0035 | yes | 2.317 | 0.0042 | yes | yes |
| time to OD 0.4 | 60 d | day 2 | -0.0195 | 0.0590 | no | 0.933 | 0.0470 | no | yes |
| time to OD 0.4 | 15 d | day 2 | +0.0116 | 0.0812 | no | 1.068 | 0.0618 | no | yes |
| resistance | 15 d | day 2 | +0.0515 | 0.4446 | no | 1.295 | 0.4529 | no | yes |
| time to OD 0.4 | 60 d | day 5 | -0.0041 | 0.6999 | no | 0.976 | 0.4605 | no | yes |
| resistance | 60 d | day 2 | -0.0551 | 0.5486 | no | 0.836 | 0.5400 | no | yes |
| resistance | 60 d | day 5 | +0.0389 | 0.6797 | no | 1.111 | 0.7150 | no | yes |

**Table S3.** Decomposition of the isoniazid-resistance association with the tolerance class into a path through log10 starting density and a direct path, by the product of coefficients with bootstrap percentile intervals. The mediated path excludes zero in every specification and the direct path covers zero in every one. This replaces the percentage attenuation the earlier analysis quoted, which is a descriptive ratio rather than an estimand. Sequential ignorability is assumed and is not testable here; the sensitivity analysis in the Methods reports the residual correlation that would nullify the estimate.

| Outcome and stratum | n | Total effect c (95% CI) | Direct effect c' (95% CI) | Mediated effect (95% CI) | Proportion mediated |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linear 0/1/2, all IS/IR | 203 | +0.256 (+0.087, +0.425) | +0.091 (-0.116, +0.287) | +0.166 (+0.067, +0.279) | 65% |
| Linear 0/1/2, baseline isolates | 168 | +0.226 (+0.038, +0.409) | +0.067 (-0.157, +0.294) | +0.159 (+0.053, +0.295) | 70% |
| High versus rest | 203 | +0.121 | +0.013 | +0.108 (+0.037, +0.189) | 89% |
| Not-low versus low | 203 | +0.135 | +0.077 | +0.058 (+0.003, +0.121) | 43% |

**Table S4.** Isoniazid-resistant isolates enter this assay ten-fold lower than susceptible ones, and we do not know why. This is what the deposit can and cannot rule out. The verdict column is decided on the two recorded-rate columns beside it: PROXY means the covariate is recorded for no isolate in one of the two exposure groups, so its missingness is the exposure; PARTIAL means both groups record it but the missingness is still tied to the exposure (Fisher exact p < 10⁻⁶); INDEPENDENT means it is not. Seven of the nine covariates are therefore unusable, and they fail in two ways. Five are recorded almost exclusively for resistant isolates: the two susceptibility calls, the two Mykrobe calls and the mutation identity. The susceptibility calls are missing on identical rows, which is why they return identical coefficients, and the Mykrobe calls carry a single value wherever they are recorded in this stratum, so no model can be fitted for them and no coefficient is printed. The other two are the drug MICs, recorded for every susceptible isolate and 67 of 84 resistant ones; the isoniazid MIC separates the two groups completely, so adjusting for it conditions on a graded reading of the exposure. A negative attenuation is an amplification: the adjusted coefficient sits further from zero than the unadjusted one, which is what the isoniazid MIC does at 13 per cent. A coefficient is printed wherever one exists so the circularity is visible, but none of these seven bounds anything. Only 2 covariates are recorded at rates unrelated to susceptibility, and adjusting for either leaves the coefficient within five per cent of its unadjusted value. The file records no referring site and no processing batch, so those cannot be tested at all.

| Covariate | Recorded, resistant | Recorded, susceptible | Can it adjust? | Resistance coefficient | Attenuation |
| --- | ---: | ---: | ---: | ---: | ---: |
| INH_MGIT_DST | 82/84 | 0/119 | PROXY | -0.851 | -0% |
| RIF_MGIT_DST | 82/84 | 0/119 | PROXY | -0.851 | -0% |
| INH_mutation | 79/84 | 1/119 | PARTIAL | -0.662 | 22% |
| INH_Mykrobe | 76/84 | 0/119 | PROXY | - | - |
| RIF_Mykrobe | 76/84 | 0/119 | PROXY | - | - |
| MIC_INH | 67/84 | 119/119 | PARTIAL | -0.963 | -13% |
| MIC_RIF | 67/84 | 119/119 | PARTIAL | -0.853 | -0% |
| Time_to_0.4 | 83/84 | 119/119 | INDEPENDENT | -0.807 | 5% |
| Time_point | 84/84 | 119/119 | INDEPENDENT | -0.818 | 4% |

**Table S5.** Fold below the nominal 0.5 McFarland reference, 1.5e8 CFU/mL. Descriptive only, and not a protocol-compliance metric. A time-kill inoculum is prepared by diluting from a suspension matched to that turbidity, so every entry is expected to sit far below it; the conversion of a turbidity to CFU/mL depends on species, cell aggregation and preparation and is least reliable for mycobacteria. The clinical rows are most probable numbers divided by a reference stated in CFU/mL, so those two ratios cross units and are the least meaningful in the table.

| Dataset | Median log10 N0 | Fold below nominal 0.5 McFarland |
| --- | ---: | ---: |
| ERA4TB, between laboratories at 100 uL | 4.63 | 3,525x |
| ERA4TB, every laboratory and plating volume | 4.29 | 7,751x |
| Vijay, 15-day culture | 5.79 | 246x |
| Vijay, 60-day culture | 7.36 | 7x |
| Kaur, planktonic | 7.03 | 14x |
| Kaur, intracellular | 5.94 | 170x |
| Dubey, hollow fibre | 6.08 | 123x |

**Table S6.** The same nominal concentration expressed in multiples of the minimum inhibitory concentration each population actually evolved to. At 25 ug/mL the same number denotes a sub-inhibitory exposure in one nutrient condition and a strongly inhibitory one in another.

| Nominal concentration (ug/mL) | Nutrient levels | Lowest exposure (x MIC) | Highest exposure (x MIC) | Spread | Straddles the MIC |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12.5 | 3 | 1.49 | 4.74 | 3.2x | no |
| 25 | 3 | 0.55 | 9.47 | 17.1x | yes |
| 50 | 2 | 5.08 | 10.95 | 2.2x | no |
| 100 | 1 | 9.72 | 9.72 | 1.0x | no |

**Table S7.** Sensitivity of the load-bearing counts to the choice of floor. Each deposit is sensitive to a different thing, so the table is long rather than wide: one row per deposit, floor scenario and quantity. The clinical sweep steps through every three-tube most-probable-number rung at or below 23 per mL, and the number of isolates short of four logs of headroom moves only between 28 and 33 across the whole range, which is why the inferred floor is safe to use. The six-laboratory rows price what pooling the four plating volumes to one floor would cost. The Kaur deposit records no plated volume, so its rows show what assuming one would do: the four-log endpoint stays reachable throughout while the headroom itself moves by 1.6 log10.

| Deposit | Floor assumed | Quantity | Value |
| --- | --- | --- | ---: |
| Vijay 2024 | floor = 3 MPN/mL | isolates short of 4 logs | 28 |
| Vijay 2024 | floor = 3 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 3 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 3 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 3 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 3 MPN/mL | short of 4 logs, baseline only | 17 |
| Vijay 2024 | floor = 3.6 MPN/mL | isolates short of 4 logs | 28 |
| Vijay 2024 | floor = 3.6 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 3.6 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 3.6 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 3.6 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 3.6 MPN/mL | short of 4 logs, baseline only | 17 |
| Vijay 2024 | floor = 7.2 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 7.2 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 7.2 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 7.2 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 7.2 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 7.2 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 7.4 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 7.4 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 7.4 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 7.4 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 7.4 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 7.4 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 9.2 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 9.2 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 9.2 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 9.2 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 9.2 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 9.2 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 11 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 11 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 11 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 11 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 11 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 11 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 14 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 14 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 14 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 14 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 14 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 14 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 15 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 15 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 15 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 15 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 15 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 15 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 20 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 20 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 20 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 20 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 20 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 20 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 21 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 21 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 21 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 21 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 21 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 21 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 23 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 23 MPN/mL | isolates at the floor | 18 |
| Vijay 2024 | floor = 23 MPN/mL | calls resting on a measured fraction | 185 |
| Vijay 2024 | floor = 23 MPN/mL | calls with one compatible class | 12 |
| Vijay 2024 | floor = 23 MPN/mL | calls with several compatible classes | 6 |
| Vijay 2024 | floor = 23 MPN/mL | short of 4 logs, baseline only | 21 |
| ERA4TB | per-volume (as analysed) | genuine counts a pooled floor discards (%) | 0 |
| ERA4TB | per-volume (as analysed) | below-limit flags contradicted (%) | 16.67 |
| ERA4TB | pooled at the most sensitive volume, 100 uL | genuine counts a pooled floor discards (%) | 0 |
| ERA4TB | pooled at the most sensitive volume, 100 uL | below-limit flags contradicted (%) | 43.17 |
| ERA4TB | pooled at the modal volume, 10 uL | genuine counts a pooled floor discards (%) | 1.13 |
| ERA4TB | pooled at the modal volume, 10 uL | below-limit flags contradicted (%) | 28.71 |
| ERA4TB | pooled at the least sensitive volume, 2.5 uL | genuine counts a pooled floor discards (%) | 5.94 |
| ERA4TB | pooled at the least sensitive volume, 2.5 uL | below-limit flags contradicted (%) | 15.26 |
| ERA4TB | pooled at the geometric mean of the per-volume floors | genuine counts a pooled floor discards (%) | 1.04 |
| ERA4TB | pooled at the geometric mean of the per-volume floors | below-limit flags contradicted (%) | 38.96 |
| Dubey 2026 | the below-limit placeholder taken literally | median headroom (log10) | 6.08 |
| Dubey 2026 | the below-limit placeholder taken literally | cultures short of 4 logs | 0 |
| Dubey 2026 | 100 uL plated, as the deposit's staging record gives | median headroom (log10) | 5.08 |
| Dubey 2026 | 100 uL plated, as the deposit's staging record gives | cultures short of 4 logs | 0 |
| Dubey 2026 | 50 uL plated | median headroom (log10) | 4.78 |
| Dubey 2026 | 50 uL plated | cultures short of 4 logs | 0 |
| Dubey 2026 | 10 uL plated | median headroom (log10) | 4.08 |
| Dubey 2026 | 10 uL plated | cultures short of 4 logs | 5 |
| Kaur 2024 | 100 uL plated, if it had been stated | headroom (log10) | 6.03 |
| Kaur 2024 | 100 uL plated, if it had been stated | 4-log endpoint reachable | True |
| Kaur 2024 | the observed minimum, which occurs once | headroom (log10) | 5.43 |
| Kaur 2024 | the observed minimum, which occurs once | 4-log endpoint reachable | True |
| Kaur 2024 | 10 uL plated, if it had been stated | headroom (log10) | 5.03 |
| Kaur 2024 | 10 uL plated, if it had been stated | 4-log endpoint reachable | True |
| Kaur 2024 | 2.5 uL plated, if it had been stated | headroom (log10) | 4.43 |
| Kaur 2024 | 2.5 uL plated, if it had been stated | 4-log endpoint reachable | True |
| Windels 2024 | no floor is recoverable | readings written as exact zero | 6 |
