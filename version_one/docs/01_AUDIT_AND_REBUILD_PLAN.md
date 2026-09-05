# Rebuilding *Comparative Modeling of Antibiotic Resistance, Tolerance, and Persistence in M. tuberculosis and S. aureus*

**Target preprint:** bioRxiv 10.1101/2025.02.12.637810 (posted 14 Feb 2025, not peer reviewed)
**Repo:** github.com/piranfar/comparative_model_presistance
**Audit date:** 2026-08-20
**Status:** Stage 1 audit + Stage 2 first-pass data scan + Stages 3–8 design proposal. No large computation run. No data downloaded.

> **⚠️ Part 3 (study design) is superseded by [02_STUDY_DESIGN_3x2.md](02_STUDY_DESIGN_3x2.md).**
> The design moved from a two-species Mtb/*S. aureus* comparison to a three-organism × two-drug matrix spanning ~50× in replication rate, and the primary estimand moved from sterilization time to Emax/EC50. Parts 1, 2 and 4–9 below still stand.

---

## PART 0 — THE SIX ANSWERS

**0.1 What the paper actually establishes.**
It establishes a *vocabulary and a figure set*, not a result. The defensible content is: (a) the framing that resistance, tolerance and persistence are three distinct survival strategies with different mathematical signatures; (b) the observation that Mtb and *S. aureus* sit at opposite ends of a growth-rate/persistence spectrum; (c) a set of illustrative curves. Everything numerical — killing rates, transition times, the 3.58% persister fraction, R²>0.9, the KS test — is either an assumption re-reported as a finding or a claim with no traceable computation behind it. There is currently **zero experimental data in the project**: the GitHub repo contains only `LICENSE` and `README.md` (single "Initial commit", no code or data ever committed). The claim "validated against experimental time-kill studies" is unsupported as written and is the item that would sink the paper at any serious journal.

**0.2 What must be corrected mathematically.** Five hard errors, quantified in §1.3. The headline one: the biphasic equation resurrects the population at `t_c`. Because the second branch is `N_d + (N_0 − N_d)e^{−k_slow(t−t_c)}`, at `t = t_c` it evaluates to exactly `N_0`. The population jumps **×2,981 (3.5 log10) for Mtb** and **×403 (2.6 log10) for *S. aureus*** at the transition — ×2.4×10¹⁷ under the abstract's parameter set. It also converges to a permanent nonzero floor (3.58% of inoculum for Mtb, forever), i.e. the model asserts TB can never be sterilized by any drug at any duration.

**0.3 Which real datasets appear obtainable.** Several, verified to exist (§2). Strongest anchors: the **hollow-fiber system for TB (HFS-TB)** literature, EMA-qualified and systematically catalogued (22 published HFS-TB experiments) by Pasipanodya et al. 2015; **de Steenwinkel et al. 2010 JAC**, reporting time-kill of rifampicin/isoniazid/ethambutol/amikacin against metabolically *high* vs *low* activity Mtb with resistance emergence — which maps almost exactly onto the tolerance/persistence distinction the preprint wants; **Budha et al. 2009** (open access, in-vitro dynamic PK/PD with INH concentration–time profiles); **Conlon et al. 2013 Nature** for *S. aureus* persister/biofilm CFU time courses; and the **CRyPTIC compendium** (12,289 Mtb genomes with MICs to 13 drugs, public on the EBI FTP) for the resistance arm. Most time-kill data will require documented figure digitization — normal and acceptable if the workflow is transparent and versioned.

**0.4 The three strongest directions.** (A) focused two-species mechanistic persistence model; (B) cross-pathogen framework; (C) treatment-optimization framework. Full specs in §3.

**0.5 Recommended design.** A refinement of A×C, **A′ — the counterfactual decomposition**. One unified state-structured PD model, species-specific parameters estimated from real time-kill data, then a formal decomposition of *why* Mtb takes months and *S. aureus* days: how much is growth rate, how much is achievable drug exposure, how much is phenotypic heterogeneity? Then counterfactual swaps ("give *S. aureus* Mtb's growth rate, keep its drug exposure — does it become hard to sterilize?"). Produces a genuinely new *number*, rescues the preprint's comparative intent, and structurally fixes its fatal flaw of comparing incommensurable rate constants. Title in §3.4.

**0.6 What justifies the server.** Nothing in Stages 1–4 and most of Stage 5 needs it — fitting, profile likelihood, digitization and Morris screening run on a laptop in minutes to hours. The server earns its keep for exactly four things: hierarchical Bayesian NLME across studies, Sobol global sensitivity (~10⁶ ODE solves), Monte Carlo regimen/PTA simulation (10⁵–10⁶ virtual subjects × regimens), and stochastic (Gillespie) extinction-probability estimation at low copy number. Details and runtimes in §6. **Recommendation: do not provision anything yet.** The binding constraint is data extraction, not FLOPs.

---

## PART 1 — FORENSIC AUDIT

### 1.1 Claims vs. support

| Element | As stated | Actually supported? |
|---|---|---|
| Research question | Compare resistance/tolerance/persistence in Mtb vs *S. aureus* | Legitimate and publishable — keep it |
| Model | Logistic growth + three closed-form survival laws | Closed-form only; not mechanistic; see §1.3 |
| Parameters | "obtained from published experimental studies (Table 1)" | No traceable extraction; citations do not contain these numbers (§1.2) |
| Figures 1–2 | Simulated curves | Genuine outputs of the stated equations — but Fig. 2 must be wrong if drawn from Eq. 4 as printed (§1.3) |
| Figure 3 | "Experimental data vs. model fitting" | **No experimental dataset is identified anywhere in the paper.** Highest severity |
| Validation | `curve_fit`, MSE, R²>0.9, KS test p<0.05 | Not reproducible; no data, no code, no fit table |
| Sensitivity | OAT ±10% | Computed, but conclusions are tautological (§1.4) |
| Clinical conclusions | Long TB therapy; early aggressive therapy for *S. aureus* | True statements — but they are *inputs* to the model, not findings from it |

**The circularity problem.** The two headline conclusions ("Mtb persistence is driven by slow dormancy, needing long therapy"; "*S. aureus* persistence is transient") are direct algebraic consequences of the Table 1 parameters (`k_slow` 0.001 vs 0.01; dormant fraction 1–5% vs 0.01–0.1%). Nothing was learned that was not assumed. This must be broken by estimating parameters *from data*.

### 1.2 Parameter provenance ledger

Every row is class **(b) adopted-from-literature-without-extraction** or worse. Nothing is class (a) traceable measurement.

| Parameter | Value (Mtb / Sa) | Cited as | Verdict |
|---|---|---|---|
| Growth rate `r` | 0.03 / 0.5 h⁻¹ | [6,7] = WHO Global TB Report 2021; Levin & Rozen, *Non-inherited antibiotic resistance* | **Source mismatch.** Neither contains a growth rate. Values are plausible (t_d ≈ 23 h and ≈ 1.4 h) but must be re-sourced |
| Resistance kill `k_R` | 0.002 / 0.01 h⁻¹ | [8,9] = Brauner 2016 (definitions review); Conlon 2016 (ATP depletion) | **Source mismatch.** Neither reports `k_R` |
| Tolerance kill `k_T` | 0.05 / 0.2 h⁻¹ | [10–12] | **Source mismatch**; undefined without a susceptible reference strain |
| Fast kill `k_fast` | 0.1 / 0.5 h⁻¹ | [13,14] | **Source mismatch**; ref [13] does not exist as cited (§1.5) |
| Slow kill `k_slow` | 0.001 / 0.01 h⁻¹ | [15,16] | **Source mismatch** |
| Dormant fraction | 1–5% / 0.01–0.1% | [17,18] | Order of magnitude consistent with the persister literature, but no extraction |
| Persister fraction "3.58%" | Discussion §4.2 | — | **Reported as a fitted result; lies inside the assumed 1–5% prior range.** Cannot stand as a finding |
| Transition time `t_c` | 12 h / 80 h | — | Not identifiable as a free parameter (§1.3, item iv) |

**Critical omission: no drug, no concentration, no MIC.** Every killing rate is drug- and concentration-agnostic, yet the Discussion draws drug-specific conclusions (bedaquiline, rifampicin). "0.5/h" for *S. aureus* is meaningless without naming the antibiotic and the multiple of MIC. This alone makes the parameters non-comparable across species and unfalsifiable.

### 1.3 Mathematical audit

**Eq. 1 — logistic growth.** Correct and dimensionally consistent, but **never used**: none of the three survival laws contain `K`. Declaring a carrying capacity then omitting it is an inconsistency a reviewer catches immediately.

**Eq. 2 — resistance, `N_R(t) = N₀e^{(r−k_R)t}`.** Unbounded exponential growth:

| | t = 24 h | t = 240 h |
|---|---|---|
| Mtb | ×10^0.3 | ×10^2.9 |
| *S. aureus* | ×10^5.1 | **×10^51** |

10⁵¹-fold expansion exceeds the bacterial biomass of the planet; the logistic cap must be applied. More fundamentally, **this is not a model of resistance.** Resistance is an *MIC shift* — a change in the concentration–response relationship — not a smaller first-order kill constant. As written, "resistance" and "tolerance" are the same equation with different numbers, contradicting the Brauner/Balaban framework the paper cites as its backbone.

**Eq. 3 — tolerance, `N_T(t) = N₀e^{−k_T t}`.** Mono-exponential decay is the *correct* signature of tolerance, so the structure is right. But tolerance is defined only *relative to a susceptible reference* (increased MDK99 at unchanged MIC). With no comparator in the model, `k_T` is just "a kill rate".

**Eq. 4 — persistence. Four separate defects.**

*(i) Discontinuity — the population is resurrected at `t_c`.* The second branch at `t = t_c` gives `N_d + (N₀ − N_d)·e⁰ = N₀`, regardless of how much killing occurred in phase 1.

```
Species / parameter set          N(t_c⁻)/N₀    N(t_c⁺)/N₀    upward jump
Mtb   (k_f=0.1, t_c=80 h)         3.36e-04        1.000       ×2,981   (3.47 log10)
Sa    (k_f=0.5, t_c=12 h)         2.48e-03        1.000       ×403     (2.61 log10)
Sa    (abstract's t_c=80 h)       4.25e-18        1.000       ×2.35e17 (17.4 log10)
```

Since Figure 2 shows no 3-log vertical jump, **the figure was almost certainly generated by different code than the equation printed in the Methods.** That discrepancy must be resolved and disclosed.

*(ii) Long-time behaviour is biologically wrong.* `lim_{t→∞} N_P(t) = N_d`. With the reported 3.58% dormant fraction and a 10⁶ CFU/mL inoculum, the model asserts a permanent floor of 3.6×10⁴ CFU/mL — **no regimen of any duration can ever sterilize.** Persisters die slowly; they are not immortal.

*(iii) Dimensional/definitional inconsistency.* In Eq. 4 `N_d` must carry units of CFU (it is added to a count). In Table 1 it is a dimensionless *fraction* `N_D/N₀` (1–5%). Never reconciled.

*(iv) `t_c` is not an independent parameter.* In a true biexponential population `N(t) = N₀[(1−f)e^{−k_fast t} + f·e^{−k_slow t}]`, the crossover is *determined* by the other parameters: `t_c = ln((1−f)/f)/(k_fast − k_slow)`. Under the paper's own values this implies **t_c = 33.3 h for Mtb** (paper asserts 80 h, off by 2.4×) and **15.5 h for *S. aureus*** (paper asserts 12 h). Treating `f`, `k_fast`, `k_slow` and `t_c` as four free parameters over-parameterizes a three-parameter system — structurally non-identifiable.

**Minimum correct replacements** (drop-in, both defensible):

```
Continuous piecewise:  N(t≥t_c) = N(t_c)·e^{−k_slow(t−t_c)}                  [continuous; not differentiable at t_c]
Biexponential:         N(t)     = N₀[(1−f)e^{−k_fast t} + f e^{−k_slow t}]   [C^∞; t_c emerges as an output]
```

With the continuous fix, Mtb reaches 2.86e-04·N₀ at 240 h and *S. aureus* 2.54e-04·N₀ — the two species become **indistinguishable at 10 days under the paper's own parameters**. The preprint's central comparative claim does not survive its own numbers once the equation is fixed. This is exactly why the rebuild must go mechanistic rather than patch the algebra.

**Are the three mechanisms genuinely distinct here?** No. All three are first-order exponential decay with different constants; only persistence gets a second phase. They must be re-encoded as: **resistance → shift in EC50/MIC**, **tolerance → reduced Emax / slower kill at unchanged MIC**, **persistence → subpopulation structure**. That is the core of the Stage 4 rebuild.

**Numerical-methods claims.** Methods say `odeint`/LSODA solved differential equations and Euler (Δt = 0.5 h) cross-validated. But every model in §2.1 is a **closed-form algebraic solution** — nothing to integrate, and "cross-validating" an analytic function with Euler is not a meaningful check. Likewise "Pandas for handling large datasets" with no dataset present. Remove or make true.

### 1.4 Internal inconsistencies

1. **The 12 h / 80 h contradiction.** Abstract: *"The transition from fast to slow killing occurs significantly earlier in S. aureus (80 hours)"* — attaches Mtb's value to *S. aureus* and asserts "earlier" while quoting the larger number. Results §3.3: *S. aureus* ~12 h, Mtb ~80 h. The Results version is internally consistent; the abstract is wrong on both count and label.
2. **Apples-to-oranges in the abstract.** Compares *S. aureus*'s `k_T` (0.2/h) against Mtb's `k_slow` (0.001/h) — two different parameters from two different equations — and presents the ratio as a biological finding.
3. **"3.58%"** presented in the Discussion as fitted; it is inside the assumed prior range and no fit exists.
4. **Sensitivity conclusions are tautologies.** "Mtb persistence duration is most sensitive to `k_slow`" is forced by the structure (`k_slow` governs the long-time branch by construction). Same for `k_T`. Properties of the equations, not the bacteria.
5. **KS test is inapplicable.** A two-sample KS test compares *empirical distributions of samples*. Applied to deterministic simulated curves it yields a p-value with no inferential meaning — with enough grid points any two distinct curves give p<0.05. Delete.
6. **R² > 0.9 against unnamed data** cannot be retained until recomputed against a named, versioned dataset.
7. **§2.3.5 is currently false**: "a public GitHub repository will be maintained for access to source code and dataset files" — the repo exists but contains no code or data.

### 1.5 Reference audit

Verified against PubMed. **20 of 30 references resolve cleanly and are appropriate** as background: Lewis 2007 [1] ([10.1038/nrmicro1557](https://doi.org/10.1038/nrmicro1557)), Zhang & Yew 2009 [2], Balaban et al. 2019 [3] ([10.1038/s41579-019-0196-3](https://doi.org/10.1038/s41579-019-0196-3)), Dhar & McKinney 2010 [4], Levin & Rozen 2006 [7], Brauner et al. 2016 [8] ([10.1038/nrmicro.2016.34](https://doi.org/10.1038/nrmicro.2016.34)), Conlon et al. 2016 [9], Wilmaerts et al. 2019 [10], Zhang et al. 2014 [14], Fisher et al. 2017 [15], Schumacher et al. 2015 [16], Maisonneuve & Gerdes 2014 [17] ([10.1016/j.cell.2014.02.050](https://doi.org/10.1016/j.cell.2014.02.050)), Hurdle et al. 2011 [18], Wakamoto et al. 2013 [21], Windels et al. 2019 [22], Fauvart et al. 2011 [23], Levin-Reisman et al. 2017 [25], Adams et al. 2011 [26], Aldridge et al. 2012 [27], Schumacher et al. 2009 [28], Wood et al. 2013 [29], Pu et al. 2019 [30].

**Five could not be located in PubMed as cited and must be corrected or removed:**

| # | As cited | Finding |
|---|---|---|
| 11 | Javid B et al. "Mtb persisters are tolerant to immune killing." *Nat Med.* 2018;24(8):1119-21 | No such record. Javid's 2018 output is the eLife kasugamycin paper ([10.7554/eLife.36782](https://doi.org/10.7554/eLife.36782)). Citation appears synthesized |
| 12 | Sebastian J et al. *mBio.* 2017;8(3):e00720-17 | No match at that locus. The group's real 2017 paper is in *Antimicrob Agents Chemother* — **title and journal garbled** |
| 13 | Koul A et al. "Diarylquinolines target ATP synthase..." *Science.* 2007;317(5839):223-7 | **Conflation of two papers**: Andries et al. *Science* **2005**;307:223 and Koul et al. *Nat Chem Biol* 2007. The cited locus does not exist |
| 19 | Fung DK et al. *Microb Pathog.* 2010;48(6):301-9 | Not found |
| 20 | van den Berg van Saparoea HB et al. "Bacterial persistence and immunity." *Biomed J.* 2019;42(5):312-32 | Not found; no such title in that journal |

**One is real but wildly mis-cited:** [24] Regev-Yochay et al., on *pneumococcal–staphylococcal colonization interference*, is cited in the Conclusion to support "persister-targeting compounds". Unrelated.

The pattern — plausible author names, plausible journals, invalid volume/page loci, occasional conflation of two real papers into one — is the signature of an LLM-generated bibliography. **All 30 references must be re-verified against DOI before resubmission**, and the reference-to-claim mapping (especially Table 1's sources) rebuilt from scratch. If a reviewer spots this, the paper is finished regardless of its modelling merits.

---

## PART 2 — REAL DATA (Stage 2, first pass)

**Scope note, stated plainly:** this is a *verified first-pass shortlist*, not a completed systematic inventory. Each entry has been confirmed to exist via PubMed. What has **not** yet been done: opening each paper to confirm whether CFU values are in a supplementary table or only in figures, and recording replicate counts and LOD. That per-paper confirmation is the first concrete task of Phase 1 and is the real bottleneck.

### 2.1 Verified anchor sources

**Mtb — dynamic exposure / time-kill**

| Source | Why it matters | Availability |
|---|---|---|
| **de Steenwinkel et al. 2010, *J Antimicrob Chemother* 65(12):2582-9** — [10.1093/jac/dkq374](https://doi.org/10.1093/jac/dkq374) | Time-kill of RIF, INH, EMB, amikacin against **metabolically highly active vs lowly active Mtb**, with resistance emergence. Closest published analogue to the tolerance-vs-persistence axis the preprint wants, with real CFU kinetics. Reports lowly-active cells needing **64× higher INH and 4× higher RIF**, while amikacin was state-independent — a quantitative, testable anchor | Likely figure digitization |
| **Budha et al. 2009, *Tuberculosis* 89(5):378-85** — [10.1016/j.tube.2009.08.002](https://doi.org/10.1016/j.tube.2009.08.002), PMC2783979 | In-vitro **dynamic** PK/PD: *M. bovis* BCG exposed to human INH concentration–time profiles (25/100/300 mg/day, fast vs slow acetylators), viable counts over time, fitted with a semi-mechanistic model with adaptive IC50. Directly reusable structure | **Open access (PMC)** |
| **Pasipanodya et al. 2015, *Clin Infect Dis* 61(Suppl 1):S10-7** — [10.1093/cid/civ425](https://doi.org/10.1093/cid/civ425) | Systematic analysis cataloguing **22 published HFS-TB experiments** (12 combination, 10 monotherapy) incl. log-phase, semi-dormant at pH 5.8, and **non-replicating persisters at ≤10 ppb oxygen**. Master index for mining the HFS-TB corpus | Roadmap → individual papers |
| **Cavaleri & Manolis 2015, *Clin Infect Dis* 61(Suppl 1):S1-4** — [10.1093/cid/civ484](https://doi.org/10.1093/cid/civ484) | EMA qualification of HFS-TB as regulatory-grade methodology — makes HFS-derived parameters defensible to reviewers | Open |

**Mtb — resistance (MIC) at scale**

| Source | Why it matters | Availability |
|---|---|---|
| **CRyPTIC compendium** — 12,289 Mtb clinical isolates, WGS + **quantitative MICs to 13 drugs in a single assay** ([10.1371/journal.pbio.3001721](https://doi.org/10.1371/journal.pbio.3001721)) | Turns "resistance" from an assumed rate constant into a **measured, drug-specific MIC/EC50 distribution** with genotype. Highest-value public dataset for the resistance arm | **Public**: `ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/`. Take MIC tables only (~tens of MB), *not* the genomes |
| EUCAST MIC distribution database | Species-wide MIC distributions for both organisms; sets EC50 priors | Public web download |

***S. aureus* — persisters / tolerance**

| Source | Why it matters | Availability |
|---|---|---|
| **Conlon et al. 2013, *Nature* 503(7476):365-70** — [10.1038/nature12790](https://doi.org/10.1038/nature12790), PMC4031760 | ADEP4 + rifampicin **eradicating** *S. aureus* biofilm in vitro and in a mouse chronic-infection model. Persister-killing CFU time courses and a genuine sterilization endpoint — the counterexample to the "persisters are immortal" asymptote | PMC; figure digitization |
| **Conlon et al. 2016, *PLoS Pathog* 12(7):e1005983** (already ref [9]) | Persister formation linked to ATP depletion — mechanistic support for a dormancy compartment | Open |

**Method/framework references to adopt**
- Brauner, Fridman, Gefen & Balaban 2016, *Nat Rev Microbiol* 14:320-30 — [10.1038/nrmicro.2016.34](https://doi.org/10.1038/nrmicro.2016.34). The MIC-vs-MDK formalism. **This should become the paper's operational definition set**, not just a background citation.
- Regoes et al. — pharmacodynamic (Hill/Emax) functions for bacterial killing.
- Nielsen & Friberg — semi-mechanistic PK/PD models for antibacterials incl. resistant subpopulations; the standard structure to build on.

### 2.2 Extraction schema (one row per experimental arm)

```
study_id | doi | pmid | species | strain | drug(s) | drug_class | mono_or_combo |
concentration (+units, ×MIC) | MIC_reported | static_or_dynamic_exposure | exposure_duration_h |
sampling_times_h | readout (CFU/mL, CFU/lung, log10) | n_replicates | LOD | censored_points |
system (broth / HFS / biofilm / macrophage / murine) | inoculum | growth_state (log / stationary / hypoxic / pH5.8) |
data_source (supp_table | source_data | figure_digitized) | extraction_method | extractor | date | checksum |
role (train | calibrate | external_validation)
```

**Non-negotiable rule:** `role` is assigned **before** any fitting, and external-validation studies are not looked at until the model is frozen.

### 2.3 Search channels still to run
PubMed/Embase systematic queries per drug × species × "time-kill | hollow fiber | post-antibiotic effect | persister"; the 22 HFS-TB papers from Pasipanodya's index; supplementary/source-data files of every hit; Dryad, Zenodo, Figshare, institutional repositories; ClinicalTrials.gov EBA studies for Mtb; ATCC/CLSI reference-strain QC time-kills for *S. aureus*.

### 2.4 On broadening beyond two species
Only if it answers a question two species cannot. For design A′, **two species is correct** — the contrast is the point. A third would be justified only to test whether the decomposition generalizes (natural candidate: *P. aeruginosa*, mid-range growth rate, strong tolerance literature). Defer.

---

## PART 3 — THREE STUDY DESIGNS (Stage 3)

### Design A — focused two-species mechanistic persistence model
- **Hypothesis:** The biphasic kill of Mtb and *S. aureus* is generated by the same subpopulation-switching structure, with species differences confined to a few interpretable parameters.
- **Contribution:** First side-by-side calibration of one model structure to both organisms with shared identifiability analysis.
- **Data:** ≥4 time-kill datasets/species, ≥2 drugs each, ≥5 sampling times. **Minimum viable:** 2 datasets/species, 1 drug each, if both include a slow/non-replicating arm.
- **Complexity:** low–moderate (3–4 state ODE). **Validation:** leave-study-out. **Compute:** laptop.
- **Figures:** ~6. **Strength:** clean, honest, publishable. **Limitation:** incremental — the structure is not new, only the comparison is. **Clinically interpretable:** partly (MDK/sterilization times).

### Design B — cross-pathogen resistance–tolerance–persistence framework
- **Hypothesis:** A single parameterization (growth rate, heterogeneity, EC50 distribution) explains sterilization difficulty across ≥5 clinically important species.
- **Contribution:** a comparative "phenotype map" of survival strategies.
- **Data:** large heterogeneous multi-species corpus. **Minimum viable:** 5 species × 2 drugs — realistically 40–60 digitized datasets.
- **Complexity:** high. **Validation:** leave-species-out. **Compute:** server (hierarchical Bayesian across species).
- **Strength:** high impact if it works. **Limitation:** extraction burden *is* the project, and heterogeneous protocols make between-species parameters confounded with between-lab effects. **Highest risk of the three.**

### Design C — treatment-optimization framework
- **Hypothesis:** Optimal regimens for persistence-dominated infections differ systematically from those chosen by conventional AUC/MIC targets.
- **Contribution:** regimen rankings with uncertainty; PTA under persistence.
- **Data:** time-kill **plus** PK models per drug; regrowth-after-withdrawal data.
- **Complexity:** moderate–high. **Validation:** hardest — needs clinical or HFS outcome data for genuine external validation. **Compute:** server (Monte Carlo, response surfaces).
- **Strength:** directly clinical. **Limitation:** without real outcome validation this degenerates into "an elaborate simulation" — the exact failure mode of the current preprint.

### 3.4 RECOMMENDED: Design A′ — counterfactual decomposition

**Working title:**
> *Growth rate, drug exposure, or phenotypic heterogeneity? Decomposing the determinants of antibiotic sterilization time in* Mycobacterium tuberculosis *and* Staphylococcus aureus *using a unified pharmacodynamic model calibrated to published time-kill data*

**The question nobody has answered quantitatively:** everyone *asserts* TB needs months because Mtb is slow-growing and dormant. Nobody has partitioned the effect. With one model structure fitted to both organisms you can ask: hold heterogeneity fixed and give *S. aureus* Mtb's growth rate — how much of the sterilization-time gap closes? Hold growth fixed and swap achievable drug exposure? Swap only the persister fraction and its exit rate?

**Why this is the right call:**
- Produces a **new number** (an effect decomposition with credible intervals), not a prettier curve.
- **Rescues the preprint's comparative intent** while structurally repairing its fatal flaw — the counterfactual runs *inside a single calibrated model*, so the species are never compared via incommensurable raw rate constants.
- **Feasible on data that demonstrably exists** (§2.1), unlike B.
- Has a **built-in negative-result path**: if exposure dominates over heterogeneity, that is itself publishable and clinically pointed.
- **Earns the server honestly** — the decomposition *is* global sensitivity analysis plus Monte Carlo.

**Anticipated finding shape** (to be determined by data, not assumed): *"X% of the Mtb–S. aureus sterilization-time gap is attributable to achievable drug exposure, Y% to replication rate, Z% to persister subpopulation structure (95% CrI ...)"*.

---

## PART 4 — REBUILT MODEL (Stage 4)

Replace all four closed-form equations with one state-structured ODE system under dynamic exposure.

**States:** `S` fast-growing susceptible, `T` slow-growing/tolerant, `P` dormant persister, `R` resistant (**included only if data support it** — otherwise omitted and reported as such).

```
dS/dt = r_S·S·(1 − N/K) − k_ST·S + k_TS·T − E_S(C)·S − μ·S
dT/dt = r_T·T·(1 − N/K) + k_ST·S − k_TS·T − k_TP·T + k_PT·P − E_T(C)·T
dP/dt = k_TP·T − k_PT·P − E_P(C)·P
dR/dt = r_R·R·(1 − N/K) + μ·S − E_R(C)·R          (r_R = r_S·(1−c), c = fitness cost)
N = S + T + P + R
E_X(C) = Emax_X · C^H / (EC50_X^H + C^H)
```

**How the three mechanisms become genuinely distinct — the key design decision:**

| Mechanism | Encoded as | Observable signature |
|---|---|---|
| **Resistance** | ↑ EC50 (MIC shift), separate compartment, mutation supply μ, fitness cost c | Concentration–response shifts right; MIC changes |
| **Tolerance** | ↓ Emax and/or ↓ r (whole population), **EC50 unchanged** | MDK99 increases at unchanged MIC; kill stays mono-exponential |
| **Persistence** | Subpopulation `P` with slow exit `k_PT` and low `E_P` | **Biphasic** kill; MDK99 ≈ unchanged, MDK99.99 ↑↑ |

Crucially `E_P > 0`: persisters die slowly, not never. This removes the permanent-floor pathology of Eq. 4.

**Dynamic exposure.** `C(t)` from a 1-compartment (or literature) PK model per drug, supporting continuous infusion, intermittent dosing, and the static case (`C(t)=C₀`) for broth experiments. Where combination data exist, a GPDI/Bliss-independence interaction term — **only where data support it.**

**`t_c` is abolished as a parameter.** The transition time becomes a *derived observable*. This alone resolves defects (i)–(iv) of §1.3.

**Observables:** MDK50/90/99/99.99; time to 1-, 2-, 3-log reduction; time to eradication (defined LOD); P(regrowth) after withdrawal; residual persister burden; persistence duration; PTA; P(treatment failure).

**Model comparison ladder (pre-declared):** mono-exponential → biexponential → S/T/P mechanistic → S/T/P + R → stochastic. Report AIC/BIC and WAIC/LOO **and** out-of-study predictive error. If the mechanistic model does not beat the biexponential out-of-sample, say so.

**Stochastic layer.** At low copy number near eradication, deterministic ODEs mislead — extinction is probabilistic. Gillespie/tau-leaping for P(extinction) and regrowth probability. This is where the server is genuinely required.

---

## PART 5 — ESTIMATION & VALIDATION (Stage 5)

1. **Acquisition & versioning:** every dataset gets a manifest row (§2.2), a checksum, a provenance receipt. Digitization via WebPlotDigitizer with the calibration file **committed**, plus double extraction by two operators and a reported discrepancy metric.
2. **Transformation:** model on log10 CFU; never fit raw counts.
3. **Censoring:** explicit left-censored likelihood at the LOD (Beal M3-type). Silent treatment of "0 CFU" points would badly bias `k_slow`.
4. **Likelihood:** replicate-aware, with a between-study random effect — this is what makes it hierarchical rather than naive pooling.
5. **Priors:** biologically bounded and *documented* — growth rates from doubling-time literature, EC50 from EUCAST/CRyPTIC MIC distributions, persister fractions from measured ranges. Every prior gets a source row in the evidence table.
6. **Identifiability:** structural (SIAN / StructuralIdentifiability.jl) **before** fitting; practical via profile likelihood. Any non-identifiable parameter is fixed or removed — and that decision is reported.
7. **Uncertainty:** Bayesian posteriors (preferred) or nonparametric bootstrap; credible intervals, never bare point estimates.
8. **Validation:** leave-study-out CV internally; **a fully held-out set of studies, chosen and sealed before modelling, for external validation.** Posterior predictive checks. Comparison against the baseline ladder.
9. **Pre-declaration:** primary endpoint (e.g. out-of-study RMSE on log10 CFU trajectories), secondary endpoints, and the decomposition estimand — written into a frozen analysis plan **before** the external set is unsealed.
10. **Sensitivity:** Morris screening → Sobol first/total indices. The ±10% OAT approach is retired.

**Discipline rule:** no R², no p-value, no CI, no "validated" appears anywhere in the manuscript until computed from real data by committed code.

---

## PART 6 — WHAT ACTUALLY NEEDS THE SERVER (Stage 6)

Order-of-magnitude estimates, assuming ~5–20 ms per ODE solve.

| Experiment | Payoff | Est. runtime | RAM | Storage | Local? |
|---|---|---|---|---|---|
| Digitization + manifest build | **The actual bottleneck** | days (human) | — | <1 GB | **Local** |
| Deterministic fits, profile likelihood (per study) | Core results | minutes–1 h | <4 GB | <1 GB | **Local** |
| Structural identifiability | Prevents a fatal reviewer catch | minutes | <4 GB | — | **Local** |
| Morris screening | Parameter triage | minutes | <4 GB | — | **Local** |
| Baseline model-comparison ladder | Required for credibility | ~1 h | <8 GB | <1 GB | **Local** |
| **Hierarchical Bayesian NLME across studies** | Proper uncertainty + between-study variance | hours–2 days | 8–32 GB | <5 GB | **Server** (chains parallelize perfectly) |
| **Sobol global SA** (12 params, N=2¹⁶ → ~9×10⁵ solves) | Replaces the tautological OAT | ~3–5 CPU-h → **~10 min on 32 cores** | <16 GB | <1 GB | **Server** |
| **Monte Carlo regimen/PTA** (10⁵–10⁶ subjects × regimens) | Clinical translation | 1–10 CPU-h/regimen set | <16 GB | 1–5 GB | **Server** |
| **Gillespie extinction probability** (low copy number, many realizations) | P(regrowth), P(sterilization) — unobtainable from ODEs | 10–100 CPU-h | <16 GB | 1–5 GB | **Server** |
| **Leave-study-out CV × model ladder** | Honest external performance | N_studies × M_models × fit cost | <16 GB | <2 GB | Server if N large |
| Combination response surfaces | Only if combination data found | scales with grid | <16 GB | 1–5 GB | Server |

**Total projected download: well under 10 GB** (papers, supplementary tables, CRyPTIC MIC tables only — explicitly *not* the CRyPTIC genomes).

**Conditions that would justify provisioning the server — none met yet:**
1. ≥8 datasets extracted, manifested and checksummed; **and**
2. the S/T/P model fitted and structurally identifiable on ≥2 datasets locally; **and**
3. the analysis plan frozen and the external-validation set sealed.

Until all three hold, the server would burn cycles on a model we have not yet earned the right to fit. No cloud computation, no database installation, and no contact with PlasmidCall / PortabilityRisk / the ceftazidime–avibactam project without explicit authorization.

---

## PART 7 — PROJECT ARCHITECTURE (Stage 7)

Standalone; no shared environment or code with the other projects. The only reuse worth arguing for is *methodological*: if PortabilityRisk already has a validated left-censored-likelihood or leave-study-out CV implementation, porting that pattern (copied, not imported) saves real time. Flagged for decision, not done.

```
Modeling of Antibiotic Resistance/
├── docs/            01_AUDIT_AND_REBUILD_PLAN.md, analysis_plan_FROZEN.md, decisions_log.md
├── data/
│   ├── raw/         downloaded supplements, figure images (immutable, checksummed)
│   ├── manifests/   datasets.csv (schema §2.2), sources.bib
│   ├── digitized/   *.csv + WebPlotDigitizer project files + calibration
│   └── processed/   tidy long-format CFU tables
├── evidence/        parameter_evidence_table.csv (param → value → source DOI → page/figure → extractor)
├── src/
│   ├── models/      ode_stp.py, pk.py, pd_hill.py, stochastic_gillespie.py, baselines.py
│   ├── inference/   likelihood_censored.py, nlme.py, bayes_stan/, identifiability/
│   ├── experiments/ exp_*.yaml  (one file per computational experiment, hash-pinned)
│   └── figures/     fig01_*.py … fig08_*.py
├── results/         tables/, figures/, posteriors/, receipts/
├── env/             environment.yml, requirements.lock, Dockerfile
└── manuscript/
```

Rules: raw data immutable; every figure regenerated by a numbered script from `results/`; every run writes a provenance receipt (git SHA, config hash, seed, environment hash); the frozen analysis plan is committed and tagged before the external set is unsealed.

---

## PART 8 — MANUSCRIPT PLAN (Stage 8)

**Title:** as §3.4.

**Novelty statement (draft):** Antibiotic sterilization of *M. tuberculosis* requires months while *S. aureus* infections resolve in days, a contrast universally attributed to slow replication and dormancy but never quantitatively partitioned. We calibrate a single state-structured pharmacodynamic model — distinguishing resistance (EC50 shift), tolerance (reduced maximal kill at unchanged EC50) and persistence (a slowly-exiting dormant subpopulation) — to published time-kill data for both organisms under documented drug exposures, and use counterfactual parameter exchange with global sensitivity analysis to decompose the sterilization-time gap into contributions from replication rate, achievable drug exposure, and phenotypic heterogeneity. [Result sentence written only after the analysis.]

**Hypotheses:** H1 one structure fits both organisms with species-specific parameters; H2 the mechanistic model out-predicts biexponential/mono-exponential baselines out-of-study; H3 the sterilization-time gap is *not* dominated by heterogeneity alone (directional, falsifiable); H4 persistence parameters, not exposure, govern P(regrowth) after withdrawal.

**Methods architecture:** data sources & extraction → definitions (Brauner framework, operationalized) → model → exposure/PK → observation & censoring model → estimation → identifiability → validation & pre-declared endpoints → sensitivity → computational environment.

**Results architecture:** (1) dataset landscape; (2) model selection vs baselines; (3) parameter estimates with CrI, both species; (4) identifiability & fit diagnostics; (5) **the decomposition — the headline**; (6) counterfactual swaps; (7) regimen/PTA implications; (8) external validation.

**Figures (8):** F1 model schematic + the three mechanisms' distinct signatures; F2 data landscape/manifest summary; F3 observed vs predicted time-kill, both species, all studies; F4 model-comparison ladder (out-of-study error); F5 posterior parameter distributions, species overlaid; F6 **decomposition of the sterilization-time gap** (the money figure); F7 counterfactual swap panels; F8 regimen simulation / P(regrowth) & PTA surfaces. Supplementary: identifiability profiles, PPCs, Sobol indices, digitization QC.

**Tables:** T1 dataset manifest; T2 parameter estimates + CrI + identifiability status; T3 model comparison; T4 decomposition estimands. Supp: full evidence table, priors + sources, censoring summary, environment lockfile.

**Discussion frame:** what the decomposition changes about *why* TB therapy is long; implications for persister-targeting drugs vs exposure optimization; whether "shorten TB therapy" strategies targeting dormancy pay off given the partition; honest limits (in vitro → in vivo, no immune compartment unless data found, digitization error, between-lab confounding).

**Journal shortlist** (decide after results): *PLOS Computational Biology*; *Antimicrobial Agents and Chemotherapy*; *Journal of Antimicrobial Chemotherapy*; *CPT: Pharmacometrics & Systems Pharmacology*; *eLife*; *mSystems*. If the decomposition is strong and clinically pointed, *Nature Communications* is not unreasonable — decide on evidence, not hope.

**Phased plan:**
- **Phase 1 (2–3 wk, local):** verify all 30 references; build manifest; extract ≥8 datasets with double digitization; build the evidence table. *Milestone: manifest + evidence table committed.*
- **Phase 2 (2 wk, local):** implement S/T/P + PK/PD; structural identifiability; fit 2–3 datasets; baseline ladder. *Milestone: model beats mono-exponential on held-out points; identifiability report done.*
- **Phase 3 (1 wk):** freeze analysis plan; seal external set. *Milestone: tagged commit.* **← server decision point**
- **Phase 4 (2–3 wk, server):** hierarchical Bayesian fit; Sobol; Monte Carlo; Gillespie; LOSO CV.
- **Phase 5 (1 wk):** unseal external set, run once, report whatever it says.
- **Phase 6 (2–3 wk):** figures, manuscript, repo release with DOI.

---

## PART 9 — DECISIONS NEEDED

1. **Design:** confirm A′, or pick A / B / C.
2. **Drug scope:** proposed Mtb = isoniazid + rifampicin; *S. aureus* = one cell-wall agent + rifampicin. Narrow scope is what makes calibration honest. Agree?
3. **Digitization labour:** double extraction needs a second operator. Who — or do we accept single extraction with a documented error estimate?
4. **The old preprint:** post a corrected v2 to bioRxiv (recommended — the discontinuity is a genuine erratum), or supersede it entirely with the new paper?
5. **Authorship/scope** of the rebuilt study.

---

*Reference verification in §1.5 and the dataset shortlist in §2.1 were checked against PubMed. Dataset availability (supplementary table vs figure-only), replicate counts and limits of detection have **not** yet been confirmed per paper — that is Phase 1, task 1. No experimental values, validation results, or performance metrics are reported anywhere in this document; none have been computed.*
