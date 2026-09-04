# Study Design — 3×2 Growth-Rate Matrix

**Supersedes Part 3 of [01_AUDIT_AND_REBUILD_PLAN.md](01_AUDIT_AND_REBUILD_PLAN.md).**
Status: design fixed; feasibility verified against PubMed and open-access full texts on 2026-08-21. No modelling run yet.

---

## 1. The design

Three organisms spanning ~50× in replication rate, two drugs from different classes, each used clinically against all three organisms.

| | **Linezolid** (oxazolidinone, 50S ribosome) | **Moxifloxacin** (fluoroquinolone, gyrase/topo IV) |
|---|---|---|
| ***S. aureus*** — t_d ≈ 0.5 h | TSUJI2012 | NGUYEN2021 |
| ***M. abscessus*** — t_d ≈ 4 h | FERRO2014 | FERRO2014 |
| ***M. tuberculosis*** — t_d ≈ 24 h | DRUSANO2018, BROWN2015 | GUMBO2004 |

All six cells have a named, verified source. Full extraction status in [`data/manifests/datasets.csv`](../data/manifests/datasets.csv).

**Why two drugs from different classes:** linezolid is bacteriostatic-leaning, moxifloxacin bactericidal. If the growth-rate effect is real it should appear under both; if it appears under only one, the effect is drug-class-specific — which is itself a finding. This is the internal replication of the study.

### Rejected alternatives, and why

- **Rifampicin as bridge** — rejected. Rifampicin is never given as monotherapy against *S. aureus* (rapid `rpoB` resistance), so essentially all published *S. aureus* data is combination therapy. Monotherapy kill kinetics cannot be separated from resistance emergence.
- **Amikacin as second drug** — rejected for the same structural reason. Searches returned synergy studies, natural-product screens, and combination work; no clean monotherapy concentration–response series against *S. aureus*. Aminoglycosides are not used alone for staphylococcal infection.
- **5×5 or 7×7 ESKAPE matrix** — rejected as a *starting point*. Three reasons: (a) all ESKAPE organisms are fast growers (t_d ≈ 0.5 h), collapsing the growth axis from 50× to ~2×; (b) the matrix is block-diagonal by biology, not full — Gram-positive and Gram-negative drugs barely overlap; (c) ~50–75 papers to extract at 2–4 h each is 150–300 h before the first fit, and between-study variance across ~50 labs would swamp between-species variance. Deferred to a follow-up study once the pipeline is validated.

---

## 2. The finding that changed the estimand

***M. abscessus* is essentially not killed by these drugs.** Three independent sources:

- **Maurer et al. 2014** ([10.1128/AAC.02448-14](https://doi.org/10.1128/AAC.02448-14)) — none of amikacin, moxifloxacin, tigecycline or linezolid showed bactericidal activity against *M. abscessus*.
- **Ferro et al. 2015** ([10.1128/AAC.02282-15](https://doi.org/10.1128/AAC.02282-15)) — in the hollow-fibre system, "on the day of the most extensive microbial kill, the bacillary burden did not fall below the starting inoculum."
- **Ferro et al. 2014** ([10.1093/jac/dku431](https://doi.org/10.1093/jac/dku431)) — "the total effect observed for all antibiotics was low."

**Consequence:** time-to-sterilization, MDK99, and time-to-3-log are undefined for the middle organism. A decomposition of "sterilization time" across three organisms is not estimable when one never reaches the endpoint.

**Why this is a feature.** *M. abscessus* replicates ~6× faster than *M. tuberculosis* yet is harder to kill. If replication rate were the dominant determinant of killing difficulty, the ordering would be reversed. The three organisms therefore give a natural experiment in which each is dominated by a different mechanism:

| Organism | Dominant mechanism | Signature |
|---|---|---|
| *S. aureus* | tolerance / persistence | killed, but with a persister tail |
| *M. tuberculosis* | persistence / dormancy | killed slowly; distinct NRP phase |
| *M. abscessus* | **intrinsic resistance** (`aac(2')`, `erm(41)`, `BlaMab`, wall impermeability) | barely killed at any exposure |

This is the resistance/tolerance/persistence triad the original preprint claimed to separate but did not — now with an experimental representative for each.

### Estimand (revised)

**Primary:** `Emax` and `EC50` from a Hill/Emax concentration–response, per organism × drug.
**Secondary:** MDK at 1-, 2-, 3-log; time to LOD — reported as *not attained* wherever that is the truth.

Rationale beyond the *M. abscessus* problem: Emax/EC50 are measurable for all three organisms even at zero net kill; they are identifiable from concentration–response data (FERRO2014 has seven concentrations, NGUYEN2021 spans 0.001–1000 mg/L); and unlike time-to-sterilization they are not confounded by inoculum and LOD, which differ across studies.

---

## 3. Feasibility findings from full-text inspection

Verified by reading Methods sections directly (PubMed / PMC, 2026-08-21).

**What we have that is better than expected**

- **NGUYEN2021** is the strongest single source. Table 1 already reports `Emax`, `EC50`, `C-1log` and `C20%`; Supplementary Table 2 holds non-normalized CFU; MDK at 1/2/3-log is tabulated in Fig. 5; and isolates are pre-classified into susceptible/low-persister, susceptible/high-persister and resistant/high-persister groups via a relative persister fraction. Resistance and persistence are operationally separated *within one dataset, one drug*. Raw data offered on request.
- **FERRO2015** reports `EC50 = 2.22 ± 0.44`, `Emax = 2.40 ± 0.22 log10 CFU/mL`, `Hill = 3.79 ± 2.44`, with eight exposure levels over 14 days and eight sampling points.
- **TSUJI2012** states its limit of detection (10² CFU/mL), uses quintuplicate plating, samples at eight points over 240 h, and has already fitted **a mechanism-based two-subpopulation model** — structurally the S/P model proposed here.
- Inoculum is ~10⁶ CFU/mL in both TSUJI2012 and FERRO2015 — an unplanned but useful consistency across the fast and middle organisms.

**Three published Hill/Emax fits (FERRO2015, NGUYEN2021, TSUJI2012) become a built-in reproducibility check**: our re-fit must recover their published parameters before any new claim is made. This validation costs no new data.

**Constraints that must be declared in the manuscript**

1. **Replication is thin.** DRUSANO2018 states the seven-arm experiment "was performed once" — n = 1 per arm. Within-study residual variance is therefore not identifiable from that study; it must come from between-study random effects or informative priors, and this must be stated rather than hidden by a pooled fit.
2. **LOD is reported only by TSUJI2012** (10² CFU/mL). Others are unstated and must be estimated from the lowest plotted non-zero point, or obtained by contacting authors. Since left-censoring bias falls directly on the slow-kill phase — the parameter of interest — this is not a cosmetic issue.
3. **No study has a data availability statement except NGUYEN2021** ("available on request"). Figure digitization is the primary route; author contact is worth attempting for DRUSANO2018, TSUJI2012 and FERRO2015.
4. **Temperature confound.** FERRO2014 was run at **30 °C** (standard for rapidly growing mycobacteria) while the *S. aureus* and Mtb work is at 37 °C. Temperature shifts both growth and kill rates. Must be modelled or declared as a limitation.
5. **NGUYEN2021 time-kill has only two time points (0 h, 24 h).** Excellent for concentration–response, insufficient for kill *kinetics*. The *S. aureus* × moxifloxacin cell needs a supplementary kinetic source — an open Phase-1 task.

---

## 4. Working title

> *Replication rate does not predict killing difficulty: comparative pharmacodynamics of* Staphylococcus aureus, Mycobacterium abscessus *and* Mycobacterium tuberculosis *under two shared antibiotic classes*

## 5. Hypotheses

- **H1** — A single Hill/Emax structure with organism- and drug-specific parameters describes all six cells.
- **H2** — `Emax` does **not** decrease monotonically with replication rate; *M. abscessus* breaks the ordering.
- **H3** — The *M. abscessus* deficit is carried by `EC50` (a resistance signature) rather than by `Emax` (a tolerance signature).
- **H4** — Persister fraction, where measurable, is independent of replication rate.
- **H5** — Any growth-rate effect is present under both drug classes; if not, it is drug-class-specific.

## 6. Immediate next steps (all local, no server)

1. Fill the `UNVERIFIED` fields in the manifest for BROWN2015, FERRO2014, GUMBO2004, DESTEENWINKEL2010, MAURER2014.
2. Find a supplementary kinetic source for *S. aureus* × moxifloxacin (constraint 5).
3. Request raw data from NGUYEN2021 authors; attempt the same for DRUSANO2018, TSUJI2012, FERRO2015.
4. Digitize FERRO2014 concentration–response (highest value per hour — it fills two cells from one experiment, controlling for lab).
5. Implement the Hill/Emax fit and reproduce the three published parameter sets as the reproducibility gate.

Server remains unjustified until the three conditions in Part 6 of the audit document are met.
