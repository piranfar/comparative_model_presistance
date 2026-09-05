# Published TB pharmacodynamic parameters, verified against primary sources

> 15-agent verification, 2026-09-05. All seven references in docs/15 resolved to
> real papers with confirmed PMIDs. This file supersedes docs/15, which stays as
> the record of what was originally claimed.

# Reconciliation of published TB pharmacodynamic parameters against `boccarella.py`

## 0. Units, established from the code before any magnitudes are compared

Read `E:\Research\Modeling of Antibiotic Resistance\src\models\boccarella.py` and `src\models\mechanistic.py`. The project's psi is **a natural-log per-capita rate in h⁻¹**, not log10. Three independent confirmations in the code:

- `net_rates` builds psi from a birth–death bookkeeping, `psi_max_r = b_r - D_S` with `b_r ≈ 1.99032 h⁻¹` and `D_S = 1.0 h⁻¹`;
- `survival()` and `persister_survival_factor()` propagate it as `np.exp(psi * tau)`;
- the resulting `psi_max_S = 0.99032 h⁻¹` gives a doubling time of `ln2/0.99032 = 0.700 h` (42 min), which is only sensible on an ln basis.

So the project baseline, restated in every unit needed below:

| Project constant | as coded | ln h⁻¹ | log10 h⁻¹ | log10 d⁻¹ |
|---|---|---|---|---|
| `psi_max_S` (at MIC = 2) | 0.99032 | +0.99032 | +0.4301 | +10.32 |
| `PSI_MIN_S` | −6.0 | −6.0 | −2.606 | −62.5 |
| ratio `−psi_min/psi_max` | — | 6.059 | 6.059 | 6.059 |
| `KAPPA` | 2.0 | dimensionless | | |

**Unresolved provenance flag, and it must be stated in the manuscript.** Because Regoes 2004 reports psi in log10 h⁻¹ while this code consumes psi in ln h⁻¹, the number −6.0 is ambiguous at the source. Inside Boccarella's own birth–death model it is internally consistent as ln h⁻¹. But if −6.0 was adopted because Regoes' E. coli psi_min values sit around −4 to −9, then a log10 rate is being fed into `np.exp()` and the intended kill is understated by ln10 = 2.303× (−6 log10 h⁻¹ = −13.82 ln h⁻¹). I could not resolve which from the code, and no verified extraction covers Regoes 2004. Every comparison below is against −6.0 ln h⁻¹, the value the code actually uses; if the other reading is correct, every discrepancy factor doubles.

---

## 1. Clean parameter table — only what survived verification

Rates are given as published and converted to the project's ln h⁻¹ axis. Nothing in this table is a Hill coefficient except the one row that says so.

### 1a. Usable

| # | Quantity | As published | Units as published | ln h⁻¹ | Identifier (verified) | Organism state | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Kg_max, intracellular | 0.033 (D.T. 21.0 h) | ln h⁻¹ | +0.033 | PMID 28356552 / DOI 10.1038/s41598-017-00529-6 | H37Rv-GFP inside PMA-differentiated THP-1, aerobic, 5 d, slowly but actively replicating | **usable as psi_max** |
| 2 | psi_min RIF, intracellular | Kg_max − E_max = 0.033 − 0.055 | ln h⁻¹ | **−0.0220** (−0.00955 log10 h⁻¹; −0.229 log10 d⁻¹) | same | same | **usable as psi_min** (readout caveat, row 1b-i) |
| 3 | psi_min ETB, intracellular | 0.033 − 0.053 | ln h⁻¹ | **−0.0200** (−0.209 log10 d⁻¹) | same | same | **usable as psi_min** |
| 4 | psi_min PZA, intracellular | 0.033 − 0.043 | ln h⁻¹ | **−0.0100** (−0.104 log10 d⁻¹) | same | same | usable as psi_min but **physiologically implausible** (EC50 45.5 ng/mL at pH 7.4); do not transplant |
| 5 | psi_min INH, intracellular | 0.033 − 0.041 | ln h⁻¹ | **−0.0080** (−0.083 log10 d⁻¹) | same | same | usable as psi_min, **least reliable** (difference of 0.041 vs 0.033) |
| 6 | Kg_max, extracellular | 0.0769 (D.T. 9.0 h) | ln h⁻¹ | +0.0769 | same | planktonic mid-log H37Rv, stirred aerobic 7H9 | usable as psi_max; the paper's cell also prints 0.045, which does not reproduce the stated 9.0 h |
| 7 | psi_min RIF, extracellular | 0.0769 − 0.178 | ln h⁻¹ | −0.1011 (−1.05 log10 d⁻¹) | same | same | **provisional only** — pooled column (see 1b-ii) |
| 8 | psi_min ETB, extracellular | 0.0769 − 0.142 | ln h⁻¹ | −0.0651 (−0.68 log10 d⁻¹) | same | same | **provisional only** |
| 9 | psi_min INH, extracellular | 0.0769 − 0.710 **or** 0.0769 − 0.055 | ln h⁻¹ | −0.6331 **or +0.0219** | same | same | **not usable** — the two published values differ 13-fold and flip the sign of psi_min |
| 10 | kd (Emax analogue), bedaquiline | 0.022 ± 0.0025; also printed 0.23 ± 0.03 log10 CFU/mL/d | ln h⁻¹ | +0.022 | PMID 34871099 / DOI 10.1128/AAC.01636-21 | Mtb in sputum, 56 adults with drug-susceptible pulmonary TB, in vivo, near-stationary, single homogeneous population | rate confirmed (0.022 × 24/ln10 = 0.2293 = published 0.23) |
| 11 | psi_min bedaquiline | lambda − kd = 0.00098 − 0.022 | ln h⁻¹ | **−0.0210** (−0.00913 log10 h⁻¹; −0.219 log10 d⁻¹) | same | same | **usable as psi_min**, with the structural hazard in 1b-iii |
| 12 | **H (Hill), bedaquiline** | 1.0 ± 0.1 | dimensionless | — | same | same | **the only Hill exponent in the verified set that occupies kappa's structural slot** — but adopt as an assumption, not a measurement (Section 2) |
| 13 | alpha, kill-onset delay | 0.025 ± 0.0043; 1/alpha = 40 ± 7 h | h⁻¹ | +0.025 | same | same | genuine rate; **no slot exists for it in the Regoes form** |
| 14 | psi_max, log-phase | 0.069 (95% CI 0.059–0.079) | log10 CFU/mL/d | +0.00662 | PMID 24041886 / DOI 10.1128/AAC.00829-13 | H37Rv, 7H9+OADC, shaking, 37 °C, drug-free | usable as psi_max **only with the caveat that this implies a 105 h doubling time** — it is a 7-day net slope, not an exponential-phase rate |
| 15 | psi_max, semidormant (acid) | 0.013 (0.007–0.018) | log10 CFU/mL/d | +0.00125 | same | acidified 7H9 without OADC, pH not stated for the first-line rows | usable as psi_max by state |
| 16 | psi_max, non-replicating | 0.005 (0.001–0.009) | log10 CFU/mL/d | +0.00048 | same | Wayne gradual oxygen depletion, anaerobic | usable as psi_max by state |
| 17 | HFS kill slope, amikacin | 0.23 (CI printed −0.29 to −0.17; sign corrupted in the paper) | log10 CFU/mL/d | −0.0221 | PMID 27458215 / DOI 10.1128/AAC.00961-16 | H37Ra log-phase, hollow-fibre | genuine rate but **pooled across all regimens including sub-optimal ones** — not psi_min, not usable as one |

### 1b. Caveats attaching to the usable rows

- **(i)** Rows 2–5 rest on a GFP-positive-object-area readout, not CFU. E_max there is a rate of loss of intracellular GFP signal area and conflates killing with growth arrest, loss of GFP expression, and macrophage clearance. No confidence intervals are published for Kg_max, E_max or EC50 anywhere in that paper. psi_min is a difference of two similar numbers (0.041–0.055 against 0.033); a 10 % error in intracellular INH E_max moves psi_min by ~50 %. A 20–48 h lag is absorbed into E_max by a model with no delay term, biasing E_max downward.
- **(ii)** Rows 7–9: the extracellular E_max column is pooled from in-house data plus DOI 10.1093/jac/dks483 and DOI 10.1093/jac/dkq374, with different media, inocula and readouts, and the Kg_max cell prints two values ("0.0769–0.045"). Forming psi_min by subtracting one source's Kg_max from another's E_max is not warranted. These rows are provisional until those two JAC papers are read directly.
- **(iii)** Row 11 was fitted to a single homogeneous population with **no persister or phenotype structure**. Importing it into the susceptible compartment of a two-state model overstates total kill; assigning it to both states erases the distinction the model exists to make. This is a structural hazard, not a numerical one, and it is the largest single risk in the whole transplant.
- **(iv)** Row 11's psi_max (lambda) is an **unestimated prior**, and it is a sputum-accumulation constant, not a replication rate. Everything that divides by it — the ratio 21.4 and the implied zMIC 0.075 mg/L total plasma — inherits that.

### 1c. Not transferable (verified as such; excluded from the usable set)

| Value(s) | Identifier | Why excluded |
|---|---|---|
| Emax 5.74 / 5.72 / 5.24 / 6.13 / 2.45 / 2.38 log10 CFU/mL and Hill 1.90, 1.94, etc. (Table 4) | PMID 24041886 | Effect axis is day-7 (day-21 for PZA) terminal log10 CFU. Four of six first-line rows have a fitted plateau at or below the plating floor; two imply a final burden below zero CFU. |
| EC50 30.24 / 8.65 / 51.95 mg/L, Hill 3.03 / 1.18, Emax 1.05 / 0.80 / 1.47 / 2.93 log10 CFU/mL | PMID 27211555 / DOI 10.1016/j.ebiom.2016.02.040 | Day-14 endpoint; H37Ra; and the human-macrophage arm had **no net kill at any concentration** — transplanting it as a kill curve inverts the paper's finding. |
| Emax 5.39 / 4.87, Hill 2.96 / 5.88, EC50 0.99× / 0.58× MIC | PMID 27458215 | Day-7 single terminal readout; Emax 5.39 exceeds the 5.18 log10 starting inoculum; Hill 5.88 has a 95 % CI of 1.19–10.57. |
| Emax 6.4 / 7.5 / 7.3 / 5.7 log10, Hill 1.6–2.2 (Table 1) and 1.36–3.55 (Table 2) | PMID 29061753 / DOI 10.1128/AAC.01413-17 | Day-7 endpoint; three of four RIF Emax values exceed the 5.70 log10 inoculum; the paper's own two fits of the same experiments disagree by more than their CI widths. |
| Hill 0.48 (intracellular) and 0.7 (broth), Emax 2.1 and 6 log10 CFU/mL, EC50 810 and 296.9 | DOI 10.1128/AAC.47.7.2118-2124.2003 (PMC161844) | Fitted on an **AUC/MIC axis** — a C×T exposure index pooled across days 1–9 — against a log10 CFU endpoint. Not an exponent on concentration and not a rate. |
| H_BI = 0.48, H_BE = 0.7, **H_BN = 0.7** | PMC4332617 | H_BN is annotated by its own authors as "Assumed same as extracellular." It is not a measurement of anything. |

### 1d. Unverified — must not be printed as support for any of these numbers

- **DOI 10.3389/fphar.2022.1063453 (PMID 36569287) contains no pharmacodynamic equation, no Hill coefficient and no Emax.** "Hill", "Emax", "sigmoidicity" and "0.48" occur zero times. Any citation of it for H = 0.48, H = 0.7, or an INH-vs-RIF Hill/Emax contrast is a miscitation and must be replaced.
- **Regoes 2004**: no PMID or DOI was verified in this pass. I am not printing one. The log-base question in Section 0 cannot be closed without it.
- **Authorship conflict, unresolved**: DOI 10.1128/AAC.01413-17 / PMID 29061753 is attributed to two different first authors across the two extractions. The identifier is consistent; cite by DOI until the author list is checked.
- **Author attribution for PMID 28356552** was hedged in the extraction ("Sarathy/Ahmad-style"). The PMID, PMCID and DOI are firm and the equations were verified verbatim against the JATS source; the author list was not. Cite by identifier.
- `KAPPA = 2.0` and `PSI_MIN_S = −6.0` in `boccarella.py` are supported by **no verified mycobacterial source**. Boccarella is recorded in the repo as DOI 10.1093/molbev/msag180 (from the file header, not re-verified here).

---

## 2. The kappa problem: 0.48 versus 1.90

**They are different quantities. Not the same quantity measured differently, and not a genuine disagreement.** There is nothing here to reconcile, because the two numbers are not estimates of the same parameter and neither is an estimate of kappa.

Three axis mismatches, in decreasing order of how often they are missed:

1. **Different independent variable.** The 0.48 (and 0.7) were fitted on **AUC/MIC** — explicitly constructed as a concentration × time product divided by the MIC, pooled across sampling days 1–9. The 1.90 was fitted on **absolute static concentration in mg/L**. An exponent on a cumulative exposure index folds time-dependence into the exponent; an exponent on concentration does not. The same paper reports its fitted EC50 on the AUC/MIC axis *decreasing from day 1 to day 9*, which is the axis telling you it is not a concentration axis. (The mg/L-versus-c/zMIC difference in the 1.90 row is, by contrast, harmless for an *exponent*: (c/k)^H = c^H/k^H, so rescaling is absorbed into EC50. That is not the problem.)

2. **Different dependent variable, and it disqualifies both.** kappa is the steepness of an instantaneous net growth rate psi. Both of these are the steepness of a cumulative log10 CFU endpoint at one frozen timepoint (day 4 for the 0.48, day 7 for the 1.90). Kappa cannot be read off either.

3. **The 1.90 is additionally floor-censored, demonstrably.** In its own table, log-phase Econ at day 7 is ~6.48 log10 CFU/mL and the fitted RIF Emax is 5.74, putting the fitted lower plateau at +0.74 log10 — the plating floor. The companion RIF/SDB row puts it at **−0.15 log10**, i.e. below zero CFU. Where the plateau is set by the inoculum running out rather than by drug effect saturating, the fitted exponent measures assay geometry (inoculum size, window length, detection limit), not the drug. Raise the inoculum or shorten the window and the number changes with nothing about rifampicin changing. That same row also has its EC50 point estimate (0.67 mg/L) sitting **outside its own published 95 % CI (0.37–0.56)**.

4. **Provenance correction that matters for how the pair is described.** The 0.7 is the *in vitro broth* fit (9-day window), not the in vivo murine lung fit as commonly repeated. The murine lung fit carries **no Hill exponent at all** (N = 1, EC50 = 933 on AUC24/MIC, Emax 4.44 log10 CFU/lung, 6 days). There is no in vivo Hill coefficient for rifampicin anywhere in that citation chain.

**What a careful modeller should do.**

- Adopt neither 0.48, 0.7 nor 1.90 as kappa, and stop describing them as being in conflict. Say in the manuscript that they are exponents on different independent variables fitted to different dependent variables over different windows in different organism states, and that a difference between them carries no information about pharmacodynamic steepness.
- The only verified value that structurally occupies kappa's slot is **H = 1.0 ± 0.1** (row 12), fitted as an exponent on concentration inside a differential equation for N. Adopt **kappa = 1** — but declare it as a *modelling assumption*, not a measurement: the posterior sits exactly at the value where the Hill function collapses to a plain Emax, it came from four dose arms spanning only 4-fold with identical loading doses, its priors were fixed to point estimates from an earlier EBA study, and the time-delay term and rising plasma concentrations are confounded over the observation window. Note also that the PMID 28356552 model *silently* assumes kappa = 1 (its concentration term is plain `c/(C_50 + c)` with no exponent, inherited from DOI 10.1093/infdis/jit164). Two of the verified sources are therefore consistent with kappa = 1, but neither measured it.
- Then **sweep kappa over 0.5–3 and report whether any conclusion survives**, because the sensitivity is enormous and is quantifiable directly in this code. At the project's own operating point (c = 12.5 µg/mL, MIC = 2, tau = 5 h), holding everything else fixed:

| kappa | psi_n (ln h⁻¹) | normal-cell survival over one 5 h pulse |
|---|---|---|
| 0.5 | −1.052 | 5.21 × 10⁻³ |
| 1.0 | −2.559 | 2.77 × 10⁻⁶ |
| **2.0 (current)** | **−5.061** | **1.02 × 10⁻¹¹** |
| 3.0 | −5.831 | 2.18 × 10⁻¹³ |

Moving kappa from the currently assumed 2.0 to the only defensible verified value, 1.0, changes single-pulse survival of the normal compartment by **2.7 × 10⁵-fold**. `KAPPA` is not a cosmetic input.

---

## 3. The psi_min question

**Genuine rates (effect axis is an instantaneous per-capita rate inside an ODE):** rows 1–11 and 13–17 of the table — i.e. only two of the six extracted studies, PMID 28356552 and PMID 34871099, plus the drug-free slopes of PMID 24041886 and the hollow-fibre slope of PMID 27458215.

**Total log reductions over a fixed window (no time in the denominator; cannot become psi_min by division):** every Emax in PMID 24041886 Table 4 (7 d, 21 d for PZA), PMID 27211555 (14 d), PMID 27458215 test-tube arm (7 d), PMID 29061753 (7 d), and DOI 10.1128/AAC.47.7.2118-2124.2003 (4 d and 9 d). In four of these the fitted Emax **exceeds the entire starting inoculum**, which is positive proof the plateau is the detection floor and not the drug.

**Comparison against `PSI_MIN_S = −6.0` (ln h⁻¹, as the code consumes it).** Direction is the same in every case: **the assumed value overstates the maximum achievable kill rate, by between one and three orders of magnitude.**

| Source | Drug / state | psi_min (ln h⁻¹) | log10 d⁻¹ | −psi_min/psi_max | Factor by which −6.0 exceeds it |
|---|---|---|---|---|---|
| PMID 28356552 | RIF, intracellular THP-1 | −0.0220 | −0.229 | 0.667 | **273×** |
| PMID 28356552 | ETB, intracellular | −0.0200 | −0.209 | 0.606 | **300×** |
| PMID 28356552 | PZA, intracellular | −0.0100 | −0.104 | 0.303 | **600×** |
| PMID 28356552 | INH, intracellular | −0.0080 | −0.083 | 0.242 | **750×** |
| PMID 34871099 | bedaquiline, in vivo sputum | −0.0210 | −0.219 | (21.4, prior-driven) | **285×** |
| PMID 28356552 | RIF, extracellular (provisional) | −0.1011 | −1.05 | 1.315 | 59× |
| PMID 28356552 | ETB, extracellular (provisional) | −0.0651 | −0.68 | 0.847 | 92× |
| PMID 28356552 | INH, extracellular (provisional, higher value) | −0.6331 | −6.59 | 8.23 | 9.5× |

Four things follow, and all four belong in the manuscript.

1. **The two independent rate-axis sources agree to 4.5 %.** Intracellular rifampicin gives −0.0220 ln h⁻¹ and in vivo sputum bedaquiline gives −0.0210 ln h⁻¹ (−0.229 and −0.219 log10 CFU/d), despite sharing no drug, no readout (GFP-object area versus CFU/TTP), no system (macrophage monolayer versus human lung) and no fitting framework. Both land at the clinical early-bactericidal-activity scale of ~0.2 log10/day. That convergence is the strongest single result in this reconciliation. It could be coincidence between two drugs; it should be reported as an order-of-magnitude anchor, not as a two-point replication.

2. **The shape is wrong as well as the scale.** The Regoes curve depends on psi_min and psi_max only through the ratio r = −psi_min/psi_max plus the overall scale psi_max. The project uses r = 6.06. Intracellular Mtb gives r = 0.24–0.67 — the drug barely outruns growth. So rescaling psi_max from 0.990 to 0.033 ln h⁻¹ while keeping r = 6.06 would give psi_min = −0.200 ln h⁻¹, **still 9.1× more aggressive than the measured −0.0220**. Both numbers have to move.

3. **psi_max is off by 30× too.** 0.99032 ln h⁻¹ (42 min doubling) against 0.033 (21 h, intracellular) or 0.0769 (9 h, planktonic) — and against 0.00098 ln h⁻¹ in vivo. Note also that the two verified sources disagree on "log phase": 0.033–0.0769 ln h⁻¹ versus 0.00662 ln h⁻¹ from PMID 24041886 (a 105 h doubling time), because the latter is a 7-day net slope through saturation. Do not mix them.

4. **The pulse architecture breaks before the parameters do.** With `TAU_TREAT = 5.0` h and `TAU_GROW = 19.0` h, substituting the verified intracellular rates gives, **at infinite antibiotic concentration**, a treatment-phase survival of exp(−0.0220 × 5) = 0.896 (0.048 log10 killed) and a regrowth-phase gain of exp(0.033 × 19) = 1.874, i.e. a **net 1.68-fold population increase per daily cycle**. A 5-hour pulse is calibrated to a 42-minute doubling time; against a slow grower it does essentially nothing. Transplanting mycobacterial rates into the existing 5 h / 19 h daily cycle produces a model in which the antibiotic cannot clear the population at any dose. The exposure window has to be re-specified alongside the rates, and that is a structural change, not a parameter change.

---

## 4. Intracellular versus extracellular

Only **one** verified source measures both arms on a rate axis (PMID 28356552), and its extracellular column is pooled and provisional. Everything quantitative below therefore hangs on that single paper, and the two figures should be reported separately because they have different exposure to the pooling problem: the **E_max ratio does not require Kg_max** and is the defensible number; the **psi_min ratio does** and inherits the ambiguity.

| Drug | E_max extra → intra (ln h⁻¹) | E_max fold drop | psi_min extra → intra (ln h⁻¹) | psi_min fold drop | EC50 intra / EC50 extra | Interpretation |
|---|---|---|---|---|---|---|
| RIF | 0.178 → 0.055 | **3.24×** | −0.1011 → −0.0220 | 4.60× | 18.4 / 5.60 = **3.29× higher inside** | Both a ceiling drop and a potency loss; only the potency half is dose-compensable |
| ETB | 0.142 → 0.053 | **2.68×** | −0.0651 → −0.0200 | 3.25× | 79.5 / 264 = **0.30× (more potent inside)** | Pure **Emax ceiling**; not dose-compensable |
| INH | 0.710 → 0.041 | **17.3×** | −0.6331 → −0.0080 | 79× | 32.1 / 790 = **0.041× (24× more potent inside)** | Pure **Emax ceiling**; not dose-compensable. But see the sign problem below |
| PZA | NA → 0.043 | no comparator | — | — | — | No extracellular arm; and the intracellular EC50 of 45.5 ng/mL at pH ~7.4 is implausible |

**Answer to the question as posed: for three of the four drugs the intracellular deficit is an Emax ceiling, not an EC50 shift, and is therefore not dose-compensable.** For ETB and INH the EC50 actually *falls* inside macrophages (3.3× and 24× more potent) while the achievable kill rate collapses — raising the dose moves you up a curve whose ceiling has dropped. For RIF the two effects compound: 3.3× less potent *and* a 3.2× lower ceiling. Since psi_min is by construction the c → ∞ asymptote, the entire 3.3–4.6× fall in psi_min for RIF and ETB is ceiling, by definition.

**Do not report the INH number without its caveat.** The extracellular INH cell prints two values, 0.710 and 0.055 ln h⁻¹, differing 13-fold. With 0.055 the maximal kill rate is *below* the growth rate, psi_min is **+0.0219 ln h⁻¹** — positive — no zMIC exists and the Regoes form cannot be constructed at all. The 17.3× intracellular deficit becomes a 0.75× intracellular *advantage*. The two values must not be averaged, and until the underlying JAC papers are read the INH contrast is undetermined in both magnitude and sign.

**Corroboration from the non-rate sources, qualitative only.** PMID 27211555 found pyrazinamide produced **no net kill at any tested concentration** in human macrophages while killing ~2 log below day 0 in acid broth — that is a ceiling failure by definition, not a potency shift, and the paper's mechanism (bacterial neutralisation of phagosomal pH from ~72 h) explains it. DOI 10.1128/AAC.47.7.2118-2124.2003 reports rifampicin intracellular Emax 2.1 versus extracellular 6 log10 CFU/mL, same direction, but on incomparable axes (AUC/MIC) and different windows (4 d versus 9 d), so it corroborates the direction and nothing more. The ranking — kill inside macrophages is worse, and the deficit is ceiling-shaped — is consistent across three independent papers. The magnitude rests on one.

---

## 5. What is still missing

**Experiments that would have to be done or found.**

1. **A concentration-resolved, time-resolved Mtb time-kill under maintained static concentrations.** ≥8 concentrations spanning ~0.1–32× MIC, ≥5 CFU sampling times per concentration, inoculum chosen high enough (10⁷–10⁸ CFU/mL) that 5 logs of kill remain above the plating floor, the detection limit stated and handled with a left-censored (Tobit) likelihood, and a net rate psi(c) fitted **per concentration** before any Hill function is fitted to those rates. This is the single missing experiment. It is what produces kappa and psi_min simultaneously, and no verified source has it: five of six studies fit a sigmoid to one terminal timepoint, and the sixth (PMID 34871099) has no in vitro concentration control.
2. **A direct determination of zMIC** — the concentration at which net growth is exactly zero — rather than a broth MIC. **None of the six papers reports one.** Without it the concentration axis cannot be anchored. The only available route, zMIC = EC50 × psi_max/|psi_min|, is valid only under an unfitted kappa = 1, and for the intracellular rows it divides by a difference of two similar numbers (0.008–0.022): a 10 % error in E_max moves the derived zMIC by ~50 %, so those zMICs (27.6, 131, 132, 150 ng/mL) are order-of-magnitude at best.
3. **The same experiment in a non-replicating state.** There is **no measured Hill coefficient for non-replicating M. tuberculosis anywhere in the verified chain** — the value routinely quoted (0.7) is annotated by its own source as assumed. For a persistence model this is the load-bearing gap: the parameters that exist describe the actively replicating compartment, which is defined by not being the one the model is about.
4. **A viability readout paired with the imaging readout.** The intracellular psi_min values come from GFP-positive object area, which conflates killing with growth arrest and GFP loss. Running the same THP-1 assay with parallel CFU would calibrate the two and tell you how much of E_max is killing.
5. **Replication with confidence intervals.** No CIs, SEs or credible intervals are published for Kg_max, E_max or EC50 in PMID 28356552. psi_min there is a difference of two similar numbers with no error bars at all. Three independent replicates with reported uncertainty would convert rows 2–5 from point estimates into usable priors.
6. **An explicit lag or delay term, fitted.** PMID 28356552 reports a 20–48 h lag absorbed into a model with no delay compartment (biasing E_max downward over a 120 h window); PMID 34871099 fits one explicitly (alpha = 0.025 h⁻¹, 1/alpha = 40 h, so the kill factor is only 0.63 at 40 h and 0.91 at 96 h). The Regoes form is time-invariant and has no slot for it. Either carry it as an extra term or the transplant is wrong over exactly the first week that TB models care about.

**Specific papers to obtain.**

- **Regoes 2004 itself** — to fix the log base and the exact definition of psi. No identifier was verified in this pass, and Section 0's ambiguity cannot be closed without it. This is the highest-priority retrieval.
- **DOI 10.1093/jac/dks483** and **DOI 10.1093/jac/dkq374** — the two external sources pooled into the extracellular E_max column of PMID 28356552. Reading them directly resolves caveat 1b-ii, the ambiguous Kg_max ("0.0769–0.045"), and the 13-fold INH contradiction, and may supply the underlying time-kill curves.
- **DOI 10.1093/infdis/jit164** — the origin of the kappa = 1 structural assumption inherited by PMID 28356552. Needed to say whether kappa = 1 was ever tested or merely adopted.
- **The raw day-3/5/7/10 CFU series behind DOI 10.1128/AAC.01413-17** — four sampling times across four strains and two drugs exist but only the day-7 fit was published. Those data, refitted per concentration with the floor censored, are the cheapest published route to a rate-axis kappa for INH and RIF. It would require a data request.

**In-house resource already present, worth stating.** `data/raw/tb/elife93243_supp2.xlsx` (recorded in the repo as eLife 93243; not re-verified in this pass) holds 217 clinical Mtb isolates under rifampicin with MIC and MDK90/99/99.99. From `results/tables/exp16_tb_censoring.csv`: median MDK90 = 1.40 d (5.1 % censored), median MDK99 = 3.0 d (21.2 % censored), median MDK99.99 = 6.0 d (**89.9 % censored**). The first two imply a window-averaged kill rate of −0.71 and −0.67 log10 CFU/d, which sits between the verified intracellular (−0.229) and extracellular (−1.05) rifampicin values and is a usable sanity check. It is **not** psi_min: it is a window-averaged rate at one unstated concentration, to a fixed endpoint, and the deepest endpoint is 90 % censored. It can validate a fitted curve; it cannot fit one.