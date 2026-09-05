# Calibration of the shielding manuscript

Produced by the manuscript-idea-calibration skill, run as a 14-agent
workflow with live literature search, before submission rather than after.
Two of its most damaging findings were independently re-verified against
the repository and the primary source before being accepted.

---

# CALIBRATION — "Dormant bacteria are less protected than two-state persistence models assume"

Repository facts below were verified directly against `E:\Research\Modeling of Antibiotic Resistance\results\tables\` and `\src\experiments\` during this assessment.

---

## 1. CLAIM

**Intended claim (as written):** Dormant bacteria are less protected from antibiotics than two-state persistence models assume, and the resulting error is negligible where killing is fast but decisive where treatment duration is decided.

**Strongest claim the evidence actually supports:** In one published pharmacodynamic-evolution simulation (Boccarella et al. 2026), the drug-effect function is held nutrient-independent for replicating cells; refitting the Windels et al. 2024 deposit shows the replicating-cell kill rate varies ~19-fold with nutrient level (0.56–10.4/h, `exp14_kill_rates_by_nutrient.csv`) against the model's single 7.06/h, while the persister kill rate the model uses (0.51/h at 12.5 µg/mL) sits *inside* the measured range (0.15–0.81/h), so the protective advantage of dormancy collapses from 27-fold at intermediate nutrient to 3.6-fold under starvation and the model cannot represent that.

**The gap.** Four scope levels separate these: one parameter file → one model → "two-state persistence models" as a class → bacteria. The evidence reaches level one and touches level two. Level three rests on n=1 simulation driver plus a second deposit **from the same lab** (Michiels/Van den Bergh are authors on both Boccarella and Windels), so it is not a survey of a class. Level four — bacteria — is not reached at all: no physiology is measured anywhere in this work.

**Is the model-versus-bacteria gap fatal or repairable?** Repairable by re-scoping — *except in the direction the manuscript points*. The manuscript's own code contradicts its title. `src/experiments/exp14_nutrient_dependent_pd.py`, docstring, verbatim: *"exp13 located the cause in the ordinary-cell compartment rather than the dormant one, since the model's persister kill rate already matches the measured one."* The paper is titled after the compartment its own analysis exonerates. That is not a scope problem; it is a sign error in the thesis, and all three referee panels found it independently. Fatal as written; the underlying analysis survives under a different title.

---

## 2. NOVELTY

**Three closest papers.**

1. **Abel zur Wiesch et al. 2015, Sci Transl Med 7:287ra73** (doi:10.1126/scitranslmed.aaa8760) — *forecloses F1's qualitative content.* It states the target assumption, attributes concentration-independence to the Balaban lineage by name, reports measured concentration-dependent persistence (streptomycin p=0.012; ciprofloxacin p=0.011; rifampicin in patients), and concludes subpopulation models cannot explain it. Worse: it reanalysed the Regoes 2004 E. coli series — very likely the manuscript's own flagship dataset — and reported ampicillin persistence **concentration-independent**, the opposite of `exp11_slopes.csv`. The manuscript currently lists this paper as an example of shielding, which is backwards. **Remaining to F1:** the exact-cancellation identity (α cancels to 3e-6 log units), the closed-form 2.75-log ceiling, and the counter-intuitive Hill-coefficient result. Not the observation.

2. **Şimşek & Kim 2019, PNAS 116:17635** — *forecloses F2 outright.* "Power-law tail in lag time distribution underlies bacterial persistence" is the title, the significance statement, the exponent (~−2, theoretically derived), and the exponential-vs-power-law contrast. F2 re-derives its own source. Add **Rebelo et al. 2021 (bioRxiv 2021.01.20.427471)**, exponent −2.1, same argument; **Kaplan et al. 2021 Nature 600:290**, from Balaban's own lab, ageing not constant-rate; **Gokhale et al. 2021 PLoS CB**, non-exponential dormancy as thesis. **Remaining to F2:** the window-dependence corollary only, and that is compromised (§4 below).

3. **Jacobs et al. 2016, PLoS CB 12:e1004782** — *forecloses F3's general point.* Non-identifiability of interconversion parameters in persister-model classes from total-count kill data is established there. **Hofsteenge et al. 2013 (BMC Microbiol 13:25)** and **Patra & Klumpp 2013 (PLoS ONE 8:e62814)** publish both halves of F3's recovery method — single-time-point confounding, and recovery from the biphasic shape. Windels et al. use the estimator themselves in their own Methods (`P0`, initial persister fraction). **Remaining to F3:** the algebraic degeneracy at fixed τ, and the Windels-specific numbers — and those numbers do not survive §4.

**Already published, named:** F2 (Şimşek & Kim 2019). F1's headline conclusion (Abel zur Wiesch 2015; also Martinecz et al. 2023 PLoS CB for rifampicin in patients). F3's method and its general caveat (Hofsteenge 2013; Patra & Klumpp 2013; Jacobs 2016). **F4 alone has no prior art** — and F4 is the one the evidence contradicts.

---

## 3. PREMISE AUDIT

| Premise | Verdict | Load-bearing for |
|---|---|---|
| P1 — models assume a shielded dormant compartment | **Fails as stated; survives narrowed to the parameter** | F1, framing |
| P2 — models assume a constant resuscitation rate | **Fails against this paper's own targets** | F2 |
| P3 — Şimşek & Kim's power law supports F2's numbers | **Fails past ~2,000 min** | F2 |
| P4 — slow-phase intercept recovers α | **Holds** (it is Windels' own estimator) | F3 |
| P5 — treatment duration is decided in the deep tail | **Fails as a general claim; holds for TB, endocarditis, PJI** | F4, abstract |

**Survived:** P4 only, and P5 in a named minority class.

**Specific kills.** P1: Regoes 2004 is a single-population PD function with no persister compartment and does not belong in the list; Levin & Udekwu 2010 and Boccarella 2026 both give persisters a *full* Hill function, so the assumption is in the parameter (−0.5/h, −0.001/h), not the structure. P2: Windels make the back-switching rate nutrient-linear; Boccarella has **no resuscitation term at all** — §3.4 concedes this, which reads as the section's premise collapsing mid-argument. P3: the source bounds its own power law at "nearly 2,000 mins" (SI Note 1), longest observed lag 1,220 min; §3.2's 160 h row, the 16,700 h figure, §3.3's 2,000,000-min window and the abstract's "eleven orders of magnitude within a week" are all 1–3 decades outside it. P5: 87% of 315 duration trials concluded shorter is non-inferior; BALANCE (n=3,608) found 7 ≈ 14 days.

---

## 4. ALTERNATIVE EXPLANATIONS, WITH DISPOSITION

**F1 (concentration-response)**
- Evolved MIC differs between populations — **must be conceded.** `exp09_concentration_ratio.csv` row 1: geometric-mean survival at 12.5 µg/mL = **0.958**, n=2. The model's maximum survival at 12.5 at α=1 is ~0.078. These points lie 12-fold outside the model's entire support at any persistence level. This is not persister survival; it is a population whose MIC is no longer 2 µg/mL, in a dose-escalating evolution experiment where concentration is not randomised.
- Concentration is sub- or near-MIC — **must be conceded.** The MIC in µg/mL for the simulated condition is never stated, so the reader cannot tell which of six concentrations are supra-MIC.
- Unit mismatch between the model's zMIC axis and the assay's µg/mL — **must be conceded**; unaddressed, and it alone can generate the whole discrepancy.
- Drug decay / β-lactamase release over 90-min ampicillin pulses — **must be conceded.** Wiuff 2005 and Johnson & Levin 2013 formally tested and rejected these; referees will require the same.
- Heteroresistance / heterotolerance — **must be conceded.** Van den Bergh et al. 2025 (same lab as both targets) and Martinecz et al. 2023 supply a mechanism that steepens the slow phase without touching the persister death rate.
- Non-monotone persister response (Sandvik 2015, ~40-fold swing upward) — **must be conceded**: it invalidates "fold per doubling" as a summary statistic.
- Small-n and unpaired comparison — **controllable by analysis.** Use the four populations measured at both concentrations (nutrient 0.8, cycle 2): ratios 8.6, 20.1, 51.7, 753.8; paired geometric mean ≈51, not the reported 75. One of four falls **below** the model's own ceiling.

**F2 (lag distribution)**
- Log-binned OLS with R² model selection manufactures power laws (Clauset 2009) — **must be conceded**, and it is fixable: Virkar & Clauset 2014 give the MLE+KS+LR procedure for binned data.
- Lognormal, gamma, stretched exponential, truncated power law untested — **must be conceded** (Ardré 2022: lognormal; Moreno-Gámez 2020: gamma).
- Finite-window truncation — **must be conceded**; the source sets the ceiling itself.
- Internal contradiction: at the fitted exponents −2.1147 and −2.2460 (`exp12_lag_fits.csv`) **the mean converges** (≈963 and ≈500 min). §3.3 argues from exponent exactly −2, which was not fitted. **Must be conceded and corrected** — a referee gets this for free.
- Empirically contested (Fang & Allison 2023: *accelerating* resuscitation, increasing hazard) — **must be conceded**, resolvable by restricting to stationary-phase-derived, disrupted arrest.

**F3 (identifiability)**
- Estimator invalidity — **must be conceded.** `exp13_slow_phase_fits.csv`: α̂ = **2.947** (CI 1.06–8.21) at nutrient 0.0, 25 µg/mL — a fraction above one falsifies the model that generated it. R² as low as 0.017. At nutrient 0.25 α̂ drifts monotonically 0.596 → 0.00067 across concentration (900-fold) for a quantity defined before drug exposure. At nutrient 0.8, α̂ spans 6.4e-8 to 1.06e-4 and **the simulated 5e-5 lies inside that range** (`exp13_alpha_estimates.csv`: simulated/fitted = 13.7, not a discrepancy at all). The 461-fold headline is a geometric mean over mutually inconsistent fits; taken at 12.5 µg/mL it is 1.34-fold.
- F2 forbids F3 — **must be conceded.** A heavy-tailed dormancy time means no exponential slow phase, so the intercept is not α, and the concentration drift above is exactly the signature. The two findings cannot both stand as written.
- Cross-system transfer (Windels amikacin → Boccarella scenario parameter) — **must be conceded.** Persister fraction is culture × drug × medium × inoculum-specific (Joers 2010), and α in Boccarella is a scenario setting, not a claimed calibration.
- Window (2–8 h) and drug-induced persisters — **conceded but favourable**: both make the intercept an *upper* bound.
- **Controlled by analysis and immune to all of the above:** α ≈ 0.8 caps the total fast-phase drop at ~0.1 log; Windels' curves fall several logs; therefore α ≪ 0.8 with no regression, no window choice, no fit. Lead with this sentence and F3's load-bearing step becomes unattackable.

**F4 (consequence)**
- Wrong compartment repaired — **must be conceded**; the authors' own exp14 says so.
- The imposed value is outside the measured range — **must be conceded.** `exp10_recalibrated_pd.py` sets MIN_VALUE = −3.5824 (persister kill ≈3.0/h max) against measured 0.15–0.81/h: 3.7-fold above the highest measured value, ~8-fold above the median at the relevant nutrient level. The abstract calls this "matched to the data"; §5 calls it "a sensitivity analysis and not a recalibration"; the code labels the scenario `calibrated`. Three incompatible descriptions of one number.
- Survivorship conditioning — **controllable by analysis.** `exp10_recalibrated_contrast.csv`: n_low 40 → 21, extinction_fraction 0.2375, frac_never_evolved_low 0.100 → 0.048. The 2.01 → 2.05 comparison is between different cohorts, and the dropped populations are enriched for non-evolvers — biasing the contrast in exactly the direction that makes it "survive". Redo as competing risks on the full 40.
- One-factor-at-a-time recalibration of a jointly misspecified model — **must be conceded.**
- Simulation p-values (2e-6) set by the analyst's replicate count — **delete.**

---

## 5. INDEPENDENCE

**Five records; three independent data sources; effectively one lab for the load-bearing chain.**

- F1: two deposit cells (n=2 vs 22; n=20 vs 4) from **one** experiment, plus five strata from **two** external studies. Of those five, `exp11_slopes.csv` shows **two do not exceed the model ceiling at all** (ampicillin pulse 2 at 2.83; rifampicin at 4.55 vs a 2.75-log ceiling → `exceeds_model_ceiling = False`), and the largest figure in the paper (13.4-fold) rests on an axis the file itself labels *"relative dose levels 1-3, units unconfirmed"* — a slope "per doubling" on an axis where a doubling is not confirmed. Independent exceedances after these deductions: **two studies, each with a named defect.** Not "four independent datasets".
- F2: **one study**, two series, tails of **53 and 170 cells** in 5 and 6 bins, terminal bins of 1 and 5 cells. The 12,800 figure describes the parent experiment, not the tail.
- F3: **one deposit**, and internally inconsistent by 900–1,650-fold within single conditions.
- F4: **one simulation**, one parameter change.
- Boccarella and Windels share authors. F1, F3 and F4 therefore rest on data from a single research group, and F2 on a single other group. There are four findings and effectively two independent experimental programmes behind them.

---

## 6. NULL RESULT VALUE

Two null results here, of unequal worth.

**Worth publishing:** the persister kill rate in the published model is *correct* — 0.51/h against a measured 0.15–0.81/h. That is a genuine, checkable negative that removes a plausible suspect and redirects attention to the replicating compartment. It is currently buried in a docstring while the title asserts the opposite.

**Worth reporting but not a paper:** the published evolutionary conclusion survives every correction attempted (2.01 → 2.05; arms separate). §6.2 already concedes this. It is a robustness confirmation of someone else's 2026 result, and it removes the manuscript's claim on MBE entirely — there is no evolutionary inference in this work that anything in it changes.

---

## 7. THE KEY FIGURE

**The figure the current claim needs and cannot produce:** persister-phase survival versus concentration, model prediction band overlaid, restricted to conditions where a persister phase demonstrably exists. It cannot be produced, because the condition carrying the headline number (12.5 µg/mL, nutrient 0.25) has survival 0.958, no fast phase and no biphasic break by the authors' own account — there is no persister phase there to plot, and n=2.

**The figure the evidence can produce, today, from `exp14_kill_rates_by_nutrient.csv`:** replicating-cell and persister kill rate versus nutrient level on one panel, with the model's fixed 7.06/h drawn as a horizontal line through both, and the ratio (the selective advantage of dormancy) on a second panel falling from 27-fold to 3.6-fold. That figure shows a real misspecification, shows which compartment carries it, shows the mechanism (aminoglycoside uptake is PMF-dependent), and shows the consequence — the model over-states the value of dormancy precisely under starvation. It is the paper.

---

## 8. THE THREE HARDEST OBJECTIONS

1. **"You repaired the compartment your own analysis exonerates."** Raised independently by all three panels; graded *likely fatal* by two. Answered nowhere in the manuscript, and answered *against* it by `exp14_nutrient_dependent_pd.py`. Not answerable by revision — only by reformulation. The required test is one the authors can run this week: refit the normal-cell Emax/EC50/Hill to the same curves at matched exposure, leaving the persister floor at −0.5/h, and report whether the 12.5→25 gap closes.

2. **"Your headline number comes from a condition where nothing was killed."** Survival 0.958, n=2, above the model's maximum at α=1. Answerable only by deletion. Restricted to unambiguously bactericidal concentrations (25–400 µg/mL) the discrepancy is ~4.5-fold across a 16-fold range — a calibration offset, not the collapse of a concentration axis, and it cannot carry a claim about how a field represents dormancy.

3. **"F2 reports its source's title as a finding, and F2 forbids F3."** The first half is answerable cheaply: credit Şimşek & Kim, keep only the window-dependence corollary, refit by MLE with a likelihood-ratio test, and truncate every consequence at 2,000 min. The second half is not cheap: a heavy tail means the slow-phase intercept is not α, which is F3's estimator. Either reconcile them explicitly (test whether a heavy-tailed dormancy model removes F3's concentration drift — if it does, that is a better result than either finding alone) or drop one.

---

## 9. VENUE AND ARTICLE TYPE

**Not MBE** — the evolutionary conclusion is confirmed, not changed; §6.2 says so. **Not eLife/Nat Comms** — the general-interest claim requires a measurement of dormant-cell drug action that this work does not contain and does not propose to obtain. **Not PLOS Comp Biol at the present statistical standard** — R²-based model selection on 5 bins, an estimator that returns α̂ = 2.95, and geometric means over three-order-of-magnitude spreads will not clear it.

**For the claim that survives:** *Antimicrobial Agents and Chemotherapy* or *Journal of Antimicrobial Chemotherapy*, as a full research article on pharmacodynamic model misspecification — nutrient dependence of the replicating-cell kill rate, its absence from persistence-evolution models, and the resulting mis-placement of the dormancy advantage. PLOS Computational Biology becomes reachable *if* the compartment attribution is done formally: fit the two-compartment PD to the full 6×6×6 Windels grid and report profile likelihoods showing which compartment's parameters the data constrain and where the published values fall outside those intervals. The Boccarella-specific elimination-count result is a short **Letter/Matters Arising**, not a section of the main paper, and only after it is redone by correcting nutrient dependence rather than the persister floor — on which I expect it not to survive, since the floor was doing all the work.

---

## BOTTOM LINE

Worth writing — but not this paper: the analysis is sound and the title is the negation of its own result. The single most damaging weakness is that `src/experiments/exp14_nutrient_dependent_pd.py` states in its own docstring that the model's persister kill rate already matches the data and the defect lies in the ordinary-cell compartment, while F4 generates the headline consequence by driving the persister floor to −3.58 (≈3.0/h) against a measured 0.15–0.81/h, and the abstract calls that "matched to the data". Write instead: *"Pharmacodynamic models of persistence hold the replicating-cell kill rate fixed across nutrient conditions; refitting the Windels et al. deposit shows it varies 19-fold (0.56–10.4/h) while the persister rate barely moves (0.15–0.81/h), so the modelled advantage of dormancy is over-stated by roughly sevenfold under starvation — the condition in which these models are used to reason about treatment duration."* Delete F2 or reduce it to a cited corollary; replace F3's headline with the fit-free bound (α ≈ 0.8 caps the fast-phase drop at ~0.1 log, the curves fall several logs, so α ≪ 0.8); re-run F4 by correcting nutrient dependence, on the full 40 populations with extinction as a competing outcome, and drop the simulation p-values. Send the result to AAC or JAC, not MBE.