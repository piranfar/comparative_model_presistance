# Variables that change antibiotic effect between broth and an infection site

41 values, each confirmed against its primary source by an agent that
opened the paper rather than reading the abstract.

---

## 1. What changes between broth and an infection site

Split by axis, because the distinction is the whole point: a model with a concentration axis already absorbs the first block; nothing in it absorbs the second.

### Block A — variables that change the CONCENTRATION reaching the bacteria

| Variable | Drug / setting | Fold effect | Direction |
|---|---|---|---|
| Abscess penetration (encapsulated pus) | Cefpirome, 12 human abscesses; Cmax 12 vs 183 mg/L | ~15x (derived ratio-of-means, not the paper's own statistic); individual spread ≥470x | ↓ |
| Abscess penetration, within-drug spread | Moxifloxacin, 10 human abscesses, ≤0.01–9.2 mg/L | ≥920x lower bound (left-censored) | ↓, unpredictable |
| Abscess penetration, between beta-lactams | Piperacillin 2.06 vs imipenem 0.02 (C_IAA/C_plasma), same lesion type, n=36 | ~103x between drugs | mixed |
| Antifungal abscess penetration | Fluconazole 0.85 vs caspofungin 0.11 vs anidulafungin 0.0 | >8x, effectively ∞ for anidulafungin | ↓ |
| Bioactivity loss to pus binding | Gentamicin/polymyxin/colistin + purulent sediment, 100 → 3–6 µg/mL | 17–33x, **saturable** (~700 µg gentamicin, ~1500 µg polymyxin bound per mL sediment); carbenicillin unaffected | ↓, class-specific |
| Purulent vs sterile pleural fluid | Amikacin 31% vs 80–99% penetration; gentamicin and netilmicin undetectable | 2.6–3.2x (amikacin); censored for the other two | ↓ |
| Population spread in lung penetration | Meropenem, 9,999-subject Monte Carlo, 10th pct 3.67% → 90th 177.9% | 48x between individuals on the same dose | variability, not a mean shift |
| CSF penetration | Vancomycin 0.07; meropenem 0.15 (ventriculitis, TDM continuous infusion) | 14x; 6.7x | ↓ |
| ELF penetration, aminoglycosides | Amikacin 0.502 (median individual 0.461, BSV 84.4%); tobramycin 0.642; gentamicin 0.600; netilmicin 1.00 | 2.0x / 1.6x / 1.7x / 1.0x | ↓ (netilmicin none) |
| ELF penetration, meropenem | 0.32–0.36, continuous infusion, ICU pneumonia | 3.1x | ↓ |
| ELF penetration, vancomycin | 0.18 critically ill; median 0.474 healthy volunteers | 5.6x vs 2.1x — **same drug, 2.5x worse in the sick lung** | ↓ |
| Regional V/Q mismatch (atelectasis) | Levofloxacin lung tissue/plasma AUC 0.3 (CPB) vs 0.7 (off-pump) | 2.3x, same drug, dose and ICU | ↓ |
| Infected bone cavity vs healthy contralateral bone | Vancomycin 0.20 vs 0.59; cefuroxime 0.50 vs 0.79 (pigs) | 3.0x; 1.6x — but **2.1x and 1.5x** against the genuinely adjacent compartment (0.42, 0.74) | ↓ |
| Septic shock, muscle/fat interstitium | Piperacillin, ~0.1–0.2 x free plasma, n=6 | 5–10x | ↓ (partly confounded by Vd expansion) |
| Generic interstitial penetration, unbound | Meta-analysis, 96 studies in healthy volunteers, PR_u 0.78 [0.71–0.85], PI 0.35–1.75 | 1.3x | ↓ |
| **Protein binding** | Same meta-analysis: PR_tot 0.41 [0.35–0.48] vs PR_u 0.78 | **1.9x** — this is the whole protein-binding term, and it is small | ↓ |
| Bone penetration, uninfected | Fosfomycin 0.43 bone / 0.76 subcutis | 2.3x | ↓ |
| Counterexamples (no deficit) | Linezolid 1.09–1.32; daptomycin 1.08–1.44 (inflamed 0.98); moxifloxacin/cipro ISF 0.38–0.86 of free plasma; netilmicin ELF 1.00 | 1.0–1.5x, some >1 | ↑ or none |

### Block B — variables that change the EFFECT of a given concentration

| Variable | Drug / setting | Fold effect | Direction |
|---|---|---|---|
| Acid pH, potency | Gentamicin EC50 vs S. aureus: 0.36 → 113.8 mg/L, pH 7.4 → 5.0 | **316x on mg/L**, but only **2.7x in MIC-normalised units** (MIC itself moves 72x) | ↓ |
| Acid pH, MIC | Gentamicin/S. aureus pH 7.4→5.0 | 72x | ↓ |
| Acid pH, MIC | Amikacin/E. coli pH 7.2→6.0 | 8.3x | ↓ |
| Anaerobiosis | Amikacin/E. coli, pH 7.2 | 6.25x | ↓ |
| Anaerobiosis / hypercapnia | Gentamicin: S. aureus up to 20x; gram-negatives 2.5–15x | up to 20x | ↓ |
| Acid + anaerobic together | Amikacin/E. coli, 2x2 grid | **>10.4x, censored at the assay ceiling** | ↓ |
| Simulated abdominal-site conditions | Aminoglycosides median MIC ratio 4, rising to 8 at pH 6.4 + anaerobiosis; quinolones 2; clindamycin 2; cephalosporins 1; penicillins/vancomycin 0.5 | 4–8x aminoglycoside penalty; 2x beta-lactam **bonus** | mixed by class |
| Same, categorical | % MICs still susceptible under high inoculum + pathological conditions: penicillins 78, cephalosporins 73, aminoglycosides 22, quinolones 11, clindamycin 0 | reclassification, not a fold | ↓ |
| Cytoplasmic drug at acid pH | pH 7.3→5.7: gentamicin −62%, amikacin −51%, apramycin −11% | 2.6x / 2.0x / 1.1x | ↓ |
| Beta-lactam rescue of uptake | Cefotaxime + tobramycin/amikacin under low pH + low pO2 | 14x / 7x uptake restored | ↑ |
| Acid pH, opposite sign | Oxacillin MIC 8–10x lower, EC50 ~15x lower at pH 5.0 | 8–15x more potent | ↑ |
| **Nutrient availability (our measurement)** | Amikacin, E. coli, Windels grid, ordinary cells 0.56 → 10.43 /h | **19x**; dormant cells 5.3x | ↓ |
| **Biofilm** | — | **no confirmed value in this set** | — |

Nothing in the confirmed set quantifies biofilm, inoculum as a fold shift, or PMF magnitude measured in situ.

## 2. How many act through PMF / metabolic state, and do they compound?

**Five of the effect-side variables act on the same step**: acid pH, anaerobiosis, nutrient limitation, the direct cytoplasmic-uptake measurement, and the cefotaxime rescue that identifies the step as uptake. The class-specificity is the internal control: in every experiment where a beta-lactam was run alongside, it moved the other way (oxacillin 8–15x *more* potent at pH 5.0; penicillins median MIC ratio 0.5; carbenicillin unaffected by pus binding; cefotaxime restores aminoglycoside uptake). This is not a general "sick tissue" effect. It is a PMF effect.

**But be careful whose voice the mechanism is in.** Only Becker 2021 states proton motive force in its own words. Bryant 1992 never mentions PMF; Reynolds 1976 attributes its result to growth-driven medium pH; König 1993 makes no mechanistic claim at all; Baudoux 2007 attributes its pH effect to gentamicin ionization, not PMF, and reaches PMF only through a cited reference. The PMF reading is well-founded but it is a synthesis across papers, not a quotation from any of them except Becker.

**Does the literature support compounding?** Two experiments tested it, and both came in *below* multiplicative:

- Bryant 1992, the only 2x2 grid: pH alone 8.33x, anaerobiosis alone 6.25x. Multiplicative predicts 52x; additive-on-MIC predicts 65x. The observed cell is **>10.4x, censored at a 50 µg/mL ceiling** — which sits almost exactly where a multiplicative prediction would land, so the experiment cannot discriminate between the two models, or between either and a much smaller number. The authors' word is "additive," but that word is doing no arithmetic work here.
- König 1993 measured the stack directly: pathological pH/pO2 gives 4x; making it *more* extreme (pH 6.4 plus full anaerobiosis) gives 8x. Adding a second, stronger hit bought **2x**, not the 6x an independent anaerobic term would predict.

**Combined fold effect for an abscess-like site (acidic, hypoxic, nutrient-poor), aminoglycoside:**

- *Effect side.* Fully-multiplicative arithmetic gives 8.3 × 6.25 × 19 ≈ **990x — and no measurement supports it.** Fully-redundant (one saturating mechanism) gives the largest single term, **~19x**. The two stacking experiments sit between, closer to the redundant end. Defensible working range: **20–60x, with 8x as a hard measured floor** (König's own site-simulating condition) and ~1000x as an unsupported ceiling.
- *Concentration side.* 3x (amikacin, measured, purulent empyema) to ~15x (cefpirome, human abscess, different class), plus a further bioactivity loss of up to 17–33x from pus binding, which is saturable and which concentration assays do not see because they measure total drug.
- *Total in vivo/broth gap:* roughly **60–900x**, and the single nutrient-replete kill rate that current persistence models use sits at the optimistic end of every one of those ranges simultaneously.

## 3. Which values are model-grade

**Carry as parameters (point estimate, dispersion, and a defined denominator):**

- Aminoglycoside ELF penetration with equilibration half-lives — Shin 2024 gives ratio *and* t½,eq (amikacin 0.502 / 5.80 h; tobramycin 0.642 / 3.38 h; gentamicin 0.600 / 0.857 h; netilmicin 1.00 / 1.68 h). These support a real transfer compartment, not a scalar multiplier.
- Meropenem ELF as a full percentile distribution (Lodise 2011, Table 3) and vancomycin ELF percentiles in healthy volunteers (Lodise 2011b) — samplable directly.
- Pooled generic penetration: PR_u 0.78 [0.71–0.85], prediction interval 0.35–1.75; PR_tot 0.41 [0.35–0.48]. The best default prior in the whole set, and the only one with a proper CI on a pooled estimate.
- Gentamicin EC50 vs pH, four levels with CIs, Emax pinned (Baudoux 2007 Table 1). **This is the only true environment-vs-dose-response surface in the set**, and it has the right shape for a PD model: shift EC50, hold Emax. Use it in MIC-normalised units (2.7x), not mg/L (316x), or you will double-count the MIC shift.
- Bryant 1992 as *ratios only* (8.33x, 6.25x). The absolute 1992 MICs are method-specific and should not be transported.
- Becker 2021 uptake fractions (−62/−51/−11% at three pH values, n=4) — usable as a mechanistic constraint linking pH to an uptake rate constant.
- Bryant 1974 pus binding as a **capacity** (700–1500 µg per mL sediment), not a fold shift. Table 6 shows the fold shift collapses from 33x to nothing as sediment drops to 5% v/v.
- Our own nutrient/kill-rate grid — five levels, rates read directly off curves, already on the kill-rate axis. The most model-ready quantity here.

**Qualitative only:**

- Every abscess penetration value. Heavy-tailed, left-censored, one destructive sample per lesion at variable times, n=10–12, and — decisively — **no covariate predicts it**: not pH, not surface-area-to-volume, not plasma PK. Two separate papers report that null independently.
- Empyema aminoglycosides (two of three drugs censored; between-patient, not paired).
- Septic-shock piperacillin 5–10x (n=6, no CI, confounded with a 40.7 L Vd).
- König's median ratios (medians across drugs and species, quantised to 2-fold dilution steps).
- Reynolds 1976 (abstract only, "up to 20x", 1976 methods).
- Porcine bone cavity values (median only, n=8–10).
- Biofilm: absent entirely.

**Must be fitted, not assumed:**

1. **The composite site-effect multiplier.** No experiment measures pH, oxygen and nutrient together on a kill rate, and the two stacking experiments disagree with the multiplicative rule. Fit one scalar; do not build it from three literature factors.
2. **Between-patient penetration variability.** Amikacin BSV 84.4% CV; meropenem 48x from 10th to 90th percentile. This must be a random effect. A fixed 0.5 is wrong in a way that matters more than the mean.
3. **Abscess/pus penetration.** Sample from a heavy-tailed left-censored distribution; a normal(1.9, 3.4) draw produces negative concentrations for a large fraction of samples.
4. **Free fraction**, wherever unbound plasma was derived rather than measured (Zeitlinger's 0.85 rests on an assumed 35% binding in hypoalbuminaemic patients; at fu = 0.8 it falls to ~0.72).

## 4. Where the 19x sits

Ranked against every confirmed single-factor effect: 19x sits in the **top quartile, and at the top of anything a model can act on**.

Above it: gentamicin MIC vs pH in *S. aureus* (72x); the raw mg/L EC50 shift (316x, but that number double-counts the MIC move); the between-drug and within-lesion spreads in abscesses (100x, 920x — variability, not a mean effect); the meropenem population spread (48x).

Level with it: pus binding at high solids (17–33x); gentamicin under anaerobiosis in *S. aureus* (up to 20x).

**Below it — and this is the answer to the question as asked:**

| Term | Fold |
|---|---|
| Nutrient limitation (ours) | **19x** |
| Abscess penetration, cefpirome | 15x |
| Vancomycin CSF | 14x |
| Amikacin acid pH | 8.3x |
| Aminoglycoside, full simulated abdominal site | 8x |
| Meropenem CSF | 6.7x |
| Amikacin anaerobiosis | 6.25x |
| Piperacillin, septic shock interstitium | 5–10x |
| Vancomycin ELF, critically ill | 5.6x |
| Meropenem ELF | 3.1x |
| Vancomycin, infected bone cavity | 3.0x |
| Amikacin, purulent empyema | 2.6–3.2x |
| Atelectatic lung | 2.3x |
| **Protein binding (PR_tot vs PR_u)** | **1.9x** |
| Daptomycin, inflamed vs healthy tissue | 1.5x |
| Generic interstitial penetration | 1.3x |
| Linezolid | 1.0x |
| Biofilm | no confirmed value |

Nutrient limitation is **larger than every routine tissue-penetration term, which clusters at 1.3–3x**; larger than the entire protein-binding correction (1.9x); larger than the single-factor pH effect on the same drug and organism (8.3x); larger than the single-factor oxygen effect (6.25x); and larger than the whole simulated-abdominal-site MIC shift for its class (4–8x).

Two caveats that keep this honest:

- **The units are not the same.** Almost everything else in the table is a fold change in concentration or in an endpoint (MIC, EC50). Ours is a fold change in a rate. These are interconvertible only under a Hill-1 model in the linear regime; near saturation a 19x concentration drop costs far less than 19x on kill rate.
- **Which is exactly why ours may be the more damaging kind.** Baudoux's pH effect is explicitly a potency shift with Emax preserved — raise the concentration and full killing returns. Our starved-end kill rate of 0.56/h is measured at a fixed drug exposure, so we cannot yet distinguish an EC50 shift from an Emax collapse. But the mechanism argues for the latter: Hall 2019 restores tobramycin killing in tolerant *Pseudomonas* by feeding fumarate, not by raising the dose. **If the nutrient axis is an Emax axis, no term on the concentration axis can compensate for it, at any dose.** That is the experiment this measurement points at and does not yet settle.

## 5. The single most important omitted variable

**The metabolic state of the target cell as a modifier of the achievable kill rate — operationally, nutrient availability, at 19x.**

Judged on size alone it beats every penetration term and the protein-binding term combined. But size is not the strongest part of the argument. Three things are:

1. **It is not on the axis the model already has.** A concentration axis silently absorbs penetration ratios, protein binding, and EC50 shifts. A ceiling on the kill rate is not absorbable; it cannot be dosed away.
2. **It is not independent of the pH and oxygen terms.** All three act on PMF-driven uptake, and the two experiments that tested stacking both landed far below multiplicative. So the correct parameterisation is one fitted "site metabolic state" scalar, not three literature factors multiplied — and building it the naive way inflates the gap by a factor of ~50.
3. **It corrupts the very quantity persistence models are estimating.** In our own grid the ordinary-to-dormant kill ratio is 3.6x at nutrient 0, 27.0x at nutrient 0.50, 11.2x at 0.95. The kill-rate ratio between "normal" and "persister" cells — the signature by which a distinct dormant phenotype is identified — **varies 7.5-fold with nutrient level, and nearly vanishes at the starved end.** A model that fixes one kill rate at the nutrient-replete value is estimating persistence against a reference that is 19x too favourable, on an axis where the phenotypic contrast it is trying to measure is itself a function of the environment.

Runner-up, and it deserves naming: **abscess penetration**, whose confirmed spread (≥920x within one drug, ~103x between beta-lactams in one lesion type) dwarfs everything else in the table. It is not the answer because it is unusable — two independent studies report that no measured covariate predicts it. It is a variance term, not a parameter.

## Where the evidence runs out — stated plainly

- **Biofilm has no confirmed value here at all.** It cannot be placed in the table, ranked, or parameterised from this evidence base.
- **No study measures pH, oxygen and nutrient together on a kill rate.** The compounding hypothesis that motivated this search is, on the confirmed record, untested. Bryant's 2x2 is censored precisely where the answer lies; König's stack is quantised to 2-fold dilutions.
- **Every effect-side value except our own is an MIC or an EC50 — an endpoint, not a rate.** A PD model needs rates. This is a real gap, and our measurement is the only thing filling it.
- **There is no measurement of any aminoglycoside concentration in a human abscess.** The nearest is Thys 1988 in empyema, where two of three drugs were below detection.
- **PMF is never measured in situ** in any of these studies; it is inferred from class-specificity and from Becker's uptake data.

### Widely repeated numbers that do not survive contact with their sources

- **"Sepsis impairs target-site penetration 5–10x."** Traces to a single n=6 study (Joukhadar 2001), concentration-based not AUC-based, and confounded by a markedly expanded Vd. The pooled meta-analysis finds **septic vs non-septic RPR_u = 0.55, 95% CI 0.22–1.37, not significant, k=4** — as are inflammation (1.09) and ischaemia (0.81). The pooled evidence does not support sepsis as a penetration term. Obesity, at 0.60 [0.39–0.94], is the one patient covariate that does reach significance, and it is rarely quoted.
- **"Infection cuts bone penetration 3-fold."** That 0.20-vs-0.59 pair was read from a review table (Nielsen 2024) whose comparator label is wrong: 0.59 and 0.79 are **contralateral** limbs, not adjacent tissue. Against the genuinely adjacent compartment the loss is 2.1x for vancomycin and 1.5x for cefuroxime — and for cefuroxime, adjacent infected bone versus healthy bone is 1.07x, essentially nothing. Cite Bue 2018 and Tottrup 2016, not the review.
- **Cefpirome's "0.066 abscess penetration ratio"** is our own ratio-of-two-means. The paper reports no penetration ratio, and with an abscess Cmax SD (16) larger than its mean (12) the individual ratios are heavily skewed.
- **Bryant 1992 and Reynolds 1976 as PMF citations.** Neither paper mentions proton motive force. Attributing PMF to them is a miscitation; the PMF claim belongs to Taber 1987, Becker 2021, and the mechanistic literature.
- **Piperacillin/tazobactam ELF "56.8%".** It is the mean of individual patient ratios, not the ratio of the group means (2.1/2.4 = 87.5%, not the reported 91.3% for tazobactam). A model must not reconstruct site concentration as mean plasma × mean penetration.