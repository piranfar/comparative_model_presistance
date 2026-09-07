# Supplemental material

**The detection floor bounds what a time-kill assay can report: minimum duration for killing and log-reduction endpoints in five published deposits and a prospective test**

Vahhab Piranfar

This file contains 10 supplemental tables, Table S1 to Table S10, each with its legend. Every one is cited in the manuscript text.

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

**Table S8.** Every conclusion this paper draws from the two primary deposits, against uncertainty recomputed at the level the observations are actually independent. 20 survive unchanged, 6 survive with materially wider uncertainty, 5 do not survive, and 1 is withdrawn because its null is false before any data are seen. Each verdict applies to the claim as it was originally stated. Three of the five failures are gone from the text entirely; for the other two a weaker statement is retained and is marked as such where it appears -- the Cox coefficient trade is now reported as hazard ratios with no p-value, and institute C as the laboratory whose crossings its starting density does not account for rather than as a tested contrast. The five that fail are all between-laboratory p-values computed on flasks: every flask in a laboratory shares a starting culture, so a comparison that looks like 67 flasks is six laboratories, and for a three-against-three split of six clusters the smallest attainable two-sided p is 0.10. They are deleted rather than corrected, because there is nothing to correct them to.

| Section | Conclusion as originally stated | Units treated as independent | Independent clusters | Method used instead | Verdict |
| --- | --- | --- | ---: | ---: | ---: |
| 4 | the difference between panels in the growth association is itself supported (interaction p = 0.0072) | unknown isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | not recomputable | NOT SUPPORTED |
| 5 | starting density separates flasks that ever crossed below the assay floor from those that never did (AUC 0.974, p = 1.2e-10) | 67 flask | 6 | exact laboratory-level test (3 crossed vs 3 did not); cluster bootstrap over laboratories; permutation of crossing within laboratory, and within laboratory AND treatment arm | NOT SUPPORTED |
| 5 | in a Cox model, institutes D, E and F carry p = 0.015, 0.016, 0.015, which adjustment for starting density moves to 0.138, 0.172, 0.576 | 67 flask | 6 | cluster-robust sandwich on six clusters | NOT SUPPORTED |
| 5 | the log-rank test separates the six laboratories on time to first crossing | 67 flask | 6 | none available: the grouping variable is the cluster | NOT SUPPORTED |
| 5 | institute C remains distinguishable after adjustment (HR 5.27, p < 0.001) | 67 flask | 1 | none available | NOT SUPPORTED |
| 1 | all 33 short isolates are at the ceiling; 88.0% of the rest are (Fisher p = 0.030) | 217 isolate | 174 patients min | none: the null is arithmetically impossible | WITHDRAWN |
| 5 | at ten times MIC of moxifloxacin the kill rate spans 5.2-fold between laboratories (0.090 to 0.464) | 6 laboratory-arm cell | 6 | cluster bootstrap over whole laboratories | WEAKENED |
| 5 | at one times MIC five of six laboratories record net growth | 6 laboratory-arm cell | 6 | Jeffreys interval on six clusters | WEAKENED |
| 5 / 7 | the laboratory effect lands on the duration endpoint and not on the rate; the rate is 'far more reproducible' | 42 flask | 6 | permutation of the laboratory label across flasks, within arm for the rate | WEAKENED |
| 6 | the deepest demonstrable kill differs by 2.33 log10 between laboratories at one plating volume | 12 day-zero reading | 4 | cluster bootstrap over whole laboratories | WEAKENED |
| 7 | 36.6% of 191 cross-laboratory pairs are inversions (95% CI 30.1-43.6) | 191 pair of flasks | 6 | cluster bootstrap over whole laboratories; also over flasks within laboratory; also delete-one-laboratory jackknife | WEAKENED |
| 7 | under the strictest rate separation the inversion rate is 21.3% of 94 pairs (95% CI 13.9-30.3) | 94 pair of flasks | 6 | cluster bootstrap over whole laboratories | WEAKENED |
| 1 | 33 of 217 isolates (15.2%) lack the headroom for a 4-log endpoint | 217 isolate | 174 patients min | baseline-only recount | SUPPORTED |
| 1 / 2 | 18 isolates rest on the floor at 15 days and 6 at 60 | 217 + 210 isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | exact McNemar on the paired binary | SUPPORTED |
| 10 | no MIC-MDK association survives Benjamini-Hochberg | 6 tests isolate | 174 patients min | baseline-only family of six | SUPPORTED |
| 2 | 18 isolates at the floor; their survival span IS their inoculum span | 217 isolate | 174 patients min | baseline-only recount | SUPPORTED |
| 2 | 185 determinable, 12 forced by the inoculum, 6 undecidable | 203 isolate | 174 patients min | baseline-only reclassification | SUPPORTED |
| 2 | at 60 days the observability counts are 191, 6 and none, 'because the cultures are denser and few readings reach the floor' | 203 + 197 isolate-panel (each of 210 isolates counted once per panel) | 197 isolates | exact McNemar on the paired binary | SUPPORTED |
| 2 / 4 | the deep endpoint is unreachable for 26.2% of resistant against 7.6% of susceptible isolates | 217 isolate | 174 patients min | baseline-only Fisher exact | SUPPORTED |
| 4 | resistant isolates enter the assay ten-fold lower | 217 isolate | 174 patients min | baseline-only Mann-Whitney | SUPPORTED |
| 4 | the resistance-tolerance association attenuates once starting density enters the model, and its interval then spans zero | 202 isolate | 174 patients min | baseline-only refit | SUPPORTED |
| 4 | growth state predicts the tolerance class and survives adjustment (beta = +0.027, p = 0.0025) | 202 isolate | 174 patients min | baseline-only refit | SUPPORTED |
| 4 | resistant isolates do not grow measurably more slowly (p = 0.24) | 217 isolate | 174 patients min | baseline-only Mann-Whitney | SUPPORTED |
| 4 | the confound thins between panels: 15.2% short of headroom at 15 days against 3.3% at 60 | 217 + 210 isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | exact McNemar on the paired binary | SUPPORTED |
| 4 | the 60-day cultures are denser, so headroom is larger there | 420 treated as independent isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | Wilcoxon signed-rank on the within-isolate change | SUPPORTED |
| 4 | the spread of starting densities more than halves between panels (IQR 1.00 to 0.42 log10) | 420 isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | paired bootstrap resampling whole isolates | SUPPORTED |
| 5 | of 64 treated series the final step is not a decline in 48 (75%) | 64 series (one per treated flask) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| 5 | 44 of 64 series end more than one log10 above their own nadir | 64 series (one per treated flask) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| 5 / Limitations | 87.0% of the variance in flask starting density lies between laboratories | 85 flask | 6 | permutation of the laboratory label across flasks | SUPPORTED |
| 6 | including the choice of plated volume widens the spread in measurable depth to 4.40 log10 | up to 4 volumes x 5 laboratories laboratory-by-volume channel | 6 | no resampling required for the volume term | SUPPORTED |
| 7 | the criterion D_A/D_B > b_A/b_B calls 83.8% of pairs correctly | 191 pair of flasks | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| Methods | 83 of 498 below-limit flags (16.7%) are contradicted by another plating of the same sample at the same visit | 498 flag (one reading) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |

**Table S9.** The deepest reduction each culture in the prospective experiment could report, at each of its two platings. *h* = log10(*N*₀/*L*) with *L* one colony in the pooled volume plated, taken at the lowest dilution the series was read at, which is where the floor is lowest and the reportable depth greatest. The two platings of one flask share a row: at the standard inoculum the 10 µL plating ceiling runs 3.71 to 3.93 logs and the 100 µL ceiling 4.88 to 5.05, so a four-log endpoint is unreportable at one plating and reportable at the other in the same culture. The gain column is close to the log10(10) = 1.00 that plating ten times the volume buys; it is not exactly 1.00 because each plating measures its own *N*₀ and the two measurements differ.

| Arm | Flask | *N*₀ at 10 µL (per mL) | *N*₀ at 100 µL (per mL) | *h* at 10 µL | *h* at 100 µL | Gain |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| High | 1 | 3,600,000 | 4,050,000 | 4.86 | 5.91 | +1.05 |
| High | 2 | 4,450,000 | 3,300,000 | 4.95 | 5.82 | +0.87 |
| High | 3 | 4,450,000 | 3,950,000 | 4.95 | 5.90 | +0.95 |
| Low | 1 | 58,000 | 78,000 | 3.06 | 4.19 | +1.13 |
| Low | 2 | 42,500 | 65,000 | 2.93 | 4.11 | +1.18 |
| Low | 3 | 45,500 | 50,000 | 2.96 | 4.00 | +1.04 |
| Mid | 1 | 425,000 | 565,000 | 3.93 | 5.05 | +1.12 |
| Mid | 2 | 340,000 | 380,000 | 3.83 | 4.88 | +1.05 |
| Mid | 3 | 255,000 | 375,000 | 3.71 | 4.88 | +1.17 |

**Table S10.** How often one culture receives two different tolerance labels from its two platings, swept across the class threshold. That two platings report different fractions is arithmetic; that those fractions land either side of a cut is not, and this is the quantity that could have come out zero. At a cut of one per cent the window is nearly shut. At one in a thousand, where the clinical classification reanalysed here cuts its lowest class, it is one sample-time in six.

| Class threshold *c*₁ | Sample-times whose two platings straddle it | Share |
| --- | ---: | ---: |
| 10^-2 | 1 of 54 | 2% |
| 10^-3 | 9 of 54 | 17% |
| 10^-4 | 8 of 54 | 15% |
