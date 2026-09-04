# Recalculation of every quantitative claim

Generated 2026-09-03T17:09:45+00:00

Each row recomputes one claim from the paper's own equations and Table 1 values. No experimental data is involved, so every verdict is reproducible from the manuscript alone.

| # | Where | As stated | Recomputed | Verdict |
|---|---|---|---|---|
| 1 | Methods Eq. 4 with Results 3.3 (t_c = 80 h) | biphasic decay, monotone decreasing | upward jump x2,981 (3.47 log10) at t_c | **FAIL** |
| 2 | Methods Eq. 4 with Results 3.3 (t_c = 12 h) | biphasic decay, monotone decreasing | upward jump x403.4 (2.61 log10) at t_c | **FAIL** |
| 3 | Methods Eq. 4 with Abstract (t_c = 80 h) | biphasic decay, monotone decreasing | upward jump x2.354e+17 (17.37 log10) at t_c | **FAIL** |
| 4 | Methods Eq. 4, Discussion 4.2 | persisters decline slowly under prolonged therapy | lim N(t) = 35,800 CFU/mL, constant for all t | **FAIL** |
| 5 | Methods Eq. 4, Discussion 4.2 | persisters decline slowly under prolonged therapy | lim N(t) = 500 CFU/mL, constant for all t | **FAIL** |
| 6 | Results 3.3, Table 1 | t_c = 80 h, fitted independently | t_c implied by k_fast, k_slow, f is 33.27 h (2.40x discrepancy) | **FAIL** |
| 7 | Results 3.3, Table 1 | t_c = 12 h, fitted independently | t_c implied by k_fast, k_slow, f is 15.51 h (0.77x discrepancy) | **FAIL** |
| 8 | Methods Eq. 2, Results 3.1 | resistant subpopulation continues growing under antibiotic | N(240 h) = 1e8.9 CFU/mL, 0.829x the carrying capacity declared in Eq. 1 | **PASS** |
| 9 | Methods Eq. 2, Results 3.1 | resistant subpopulation continues growing under antibiotic | N(240 h) = 1e57.1 CFU/mL, 1.18e+48x the carrying capacity declared in Eq. 1 | **FAIL** |
| 10 | Methods Eq. 2 with Table 1 S. aureus values | exponential resistant growth over the 240 h simulation window | 1e57.1 CFU/mL, which is 1e26.4x the estimated total prokaryotic population of Earth | **FAIL** |
| 11 | Methods Eq. 3, Results 3.2 | tolerance in Mtb: bacteria survive transiently before declining at k_T = 0.05/h | Eq. 3 contains no replication term, yet Table 1 gives r = 0.03/h, so the net rate is -0.020/h and the population declines, but 60% more slowly than Eq. 3 shows | **PARTIAL** |
| 12 | Methods Eq. 3, Results 3.2 | tolerance in S. aureus: bacteria survive transiently before declining at k_T = 0.2/h | Eq. 3 contains no replication term, yet Table 1 gives r = 0.5/h, so the net rate is +0.300/h and the population GROWS to the carrying capacity | **FAIL** |
| 13 | Abstract, Results 3.3, Conclusion | M. tuberculosis survives extended antibiotic exposure whereas S. aureus declines sharply | under the continuous-piecewise fix the two species differ by only 1.13x at 240 h (0.05 log10) | **FAIL** |
| 14 | Abstract, Results 3.3 | same | under the biexponential fix the ratio at 240 h is 620.9x (2.79 log10) in favour of Mtb survival | **PARTIAL** |
| 15 | Methods Eq. 4, Discussion 4.2 | prolonged therapy eradicates M. tuberculosis | time to reach the 100 CFU/mL limit of detection is infinite for 2 of 6 species-formulation combinations, all of them the printed Eq. 4 | **FAIL** |
| 16 | Abstract | S. aureus killing rate 0.2/h versus M. tuberculosis 0.001/h, a 200-fold difference | 0.2/h is k_T from Eq. 3 (tolerance) and 0.001/h is k_slow from Eq. 4 (persistence); the like-for-like pairs are k_T 0.2 vs 0.05 (4x) and k_slow 0.01 vs 0.001 (10x) | **FAIL** |
| 17 | Abstract versus Results 3.3 | the transition from fast to slow killing occurs significantly earlier in S. aureus (80 hours) | Results 3.3 gives S. aureus 12 h and Mtb 80 h; the Abstract attaches Mtb's value to S. aureus while asserting the smaller of the two | **FAIL** |
| 18 | Discussion 4.2 | the persistence fraction (~3.58%) was consistent with prior research | 3.58% lies inside the assumed input range 1-5% of Table 1; no fit exists that could have produced it | **FAIL** |
| 19 | Methods 2.3.3 | a two-sample Kolmogorov-Smirnov test yielded a significant difference (p < 0.05) between M. tuberculosis and S. aureus | the p-value is controlled entirely by the simulation grid density: it crosses 0.05 at n = 25 grid points and reaches 0.00e+00 at n = 5000, with the KS statistic itself changing by only 4.0 percentage points | **FAIL** |
| 20 | Methods 2.3.2, Results 3.3, Discussion 4.1 | persistence duration in Mtb was most sensitive to k_slow, and in S. aureus variations in k_T had the largest effect; these findings underscore the biological relevance of biphasic killing rates | for any t > t_c the printed Eq. 4 contains k_slow and f only, and k_fast has an elasticity of exactly 0; the ranking is a property of which symbols appear in which branch, computed here in closed form | **FAIL** |
| 21 | Methods 2.3.1 | SciPy odeint (LSODA) was used to solve the differential equations, and Euler with dt = 0.5 h cross-validated the results | all four models in Methods 2.1 are closed-form algebraic solutions, so no differential equation is integrated anywhere in the paper; Euler at dt = 0.5 h differs from the exact exponential by up to 6.0% over 24 h, which measures the error of Euler, not the validity of the model | **FAIL** |
| 22 | Methods 2.1 Eq. 1 | bacterial population dynamics were modelled using a logistic growth equation with carrying capacity K | K appears in Eq. 1 and in none of Eqs. 2, 3 or 4, so no antibiotic-exposure result in the paper uses it | **FAIL** |
| 23 | Methods 2.3, 2.3.3, Figure 3 | Pandas was used for handling large datasets, and simulated survival curves were compared with published experimental time-kill studies with R-squared > 0.9 | no dataset is named anywhere in the manuscript, no fit table is reported, and the project's data directory is empty | **FAIL** |

## Notes

1. **EQ4-DISC-Mtb-80** - second branch equals N0 exactly at t = t_c regardless of phase-1 killing, so the printed equation increases the population at the transition; Figure 2 shows no such jump, so the figure was not drawn from the printed equation
2. **EQ4-DISC-Saureus-12** - second branch equals N0 exactly at t = t_c regardless of phase-1 killing, so the printed equation increases the population at the transition; Figure 2 shows no such jump, so the figure was not drawn from the printed equation
3. **EQ4-DISC-Saureus-80** - second branch equals N0 exactly at t = t_c regardless of phase-1 killing, so the printed equation increases the population at the transition; Figure 2 shows no such jump, so the figure was not drawn from the printed equation
4. **EQ4-FLOOR-Mtb** - with a 1,000,000 CFU/mL inoculum the model asserts a permanent floor at 3.58% of inoculum, i.e. no regimen of any duration can sterilise; the floor is 358x the assay limit of detection
5. **EQ4-FLOOR-Saureus** - with a 1,000,000 CFU/mL inoculum the model asserts a permanent floor at 0.05% of inoculum, i.e. no regimen of any duration can sterilise; the floor is 5x the assay limit of detection
6. **TC-IDENT-Mtb** - in a biexponential population t_c = ln((1-f)/f)/(k_fast - k_slow), so treating f, k_fast, k_slow and t_c as four free parameters over-parameterises a three-parameter system
7. **TC-IDENT-Saureus** - in a biexponential population t_c = ln((1-f)/f)/(k_fast - k_slow), so treating f, k_fast, k_slow and t_c as four free parameters over-parameterises a three-parameter system
8. **EQ2-UNBOUNDED-Mtb** - Eq. 1 declares a carrying capacity K that appears in none of the three survival laws; applying it caps growth at K and removes the excursion
9. **EQ2-UNBOUNDED-Saureus** - Eq. 1 declares a carrying capacity K that appears in none of the three survival laws; applying it caps growth at K and removes the excursion
10. **EQ2-EARTH-Saureus** - order-of-magnitude sanity bound from Whitman et al. 1998 PNAS (5e30 cells); a model output exceeding it by 27 orders of magnitude cannot be reported as a simulation of an infection
11. **EQ3-NO-REPLICATION-Mtb** - dropping replication from the tolerance equation is not a simplification, it changes the sign of the result: under the paper's own Table 1 values S. aureus replicates 2.5x faster than the tolerance kill rate removes cells, so the printed equation reports 15 logs of killing where the parameters imply net growth
12. **EQ3-NO-REPLICATION-Saureus** - dropping replication from the tolerance equation is not a simplification, it changes the sign of the result: under the paper's own Table 1 values S. aureus replicates 2.5x faster than the tolerance kill rate removes cells, so the printed equation reports 15 logs of killing where the parameters imply net growth
13. **CENTRAL-CLAIM-SURVIVES-FIX** - the qualitative contrast in Figure 2 is produced by the discontinuity, not by the parameters; once the equation is made continuous the paper's own Table 1 values make the two species nearly identical at 10 days, so the comparative conclusion must be rebuilt on a mechanistic model rather than patched
14. **CENTRAL-CLAIM-BIEXP** - the biexponential form does preserve a Mtb-versus-S. aureus difference, because it retains the dormant fraction as a weight rather than discarding it; this is the formulation to adopt if a closed form is required
15. **ENDPOINT-STERILISATION** - the endpoint the paper's clinical conclusions rest on is not computable from the printed equation; it becomes finite under both corrected forms
16. **ABSTRACT-MISMATCHED-PARAMS** - the headline ratio compares parameters from two different equations; the like-for-like ratios are 4x for tolerance and 10x for slow killing, not the 200x the abstract implies
17. **ABSTRACT-TC-LABEL** - internally contradictory: the number and the label disagree, and the word earlier disagrees with the number quoted
18. **PERSISTER-FRACTION-3.58** - presented in the Discussion as an output of model fitting, but it is an input drawn from the middle of the assumed prior range; the third decimal place implies a precision no procedure in the paper delivers
19. **KS-TEST-INAPPLICABLE** - a two-sample KS test compares empirical distributions of random samples; applied to two deterministic curves it tests whether the curves are identical, which is known a priori, and any two distinct curves can be made significant by sampling them more densely; the test carries no inferential content here and should be deleted
20. **SENSITIVITY-TAUTOLOGY** - the sensitivity ranking is forced by the structure of the equation and would be unchanged for any parameter values or any organism, so it cannot support a biological conclusion; a defensible analysis needs a global method on a model where all parameters act at all times, which is exp03
21. **NUMERICS-NOTHING-TO-SOLVE** - the sentence describes a computation that the paper's mathematics does not contain; either remove it or move to a genuine ODE model, which is what mechanistic.py provides
22. **EQ1-K-UNUSED** - declaring a carrying capacity and then omitting it is what permits the unbounded resistance excursion in claim EQ2-UNBOUNDED
23. **PANDAS-NO-DATA** - Figure 3 is captioned as experimental data versus model fitting but no experimental data exists; this is the highest-severity item and cannot be repaired by recomputation, only by extracting real data
