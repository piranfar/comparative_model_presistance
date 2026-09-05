# 06 — Data Feasibility Audit

**Audit date:** 2026-09-03
**Scope:** Can the "no experimental data" blocker on the persistence PD modelling paper
(*M. tuberculosis* + *S. aureus*) be removed inside ~2 weeks?
**Method:** every candidate in `data/manifests/datasets.csv` was opened (PMC full text,
publisher page, or supplementary bundle) and the actual location of the CFU numbers was
checked. Repositories (figshare, Zenodo, Dryad) were searched via their APIs, not via
web search. Files that were found were downloaded and their contents inspected directly.

---

## BLUNT SUMMARY

**Three datasets can be in hand today with zero digitisation. Two of them are
*M. tuberculosis*; one is *S. aureus*. All three were downloaded during this audit and
their contents verified column-by-column.**

- **READY (numbers, no digitisation): 3.** ERA4TB Mtb time-kill (figshare, CC-BY,
  2,120 numeric log10 CFU values), Apramycin Mtb raw data (figshare, CC-BY 4.0),
  Peyrusson 2020 *S. aureus* Nat Commun Source Data (CC-BY xlsx).
- **DIGITISE (worth the effort): 4.** Van Bambeke HFIM 2025 (*S. aureus*, biphasic,
  11 time points), DRUSANO2018, BROWN2015, TSUJI2012.
- **UNUSABLE / deprioritise: 6.** GUMBO2004, FERRO2014, FERRO2015, DESTEENWINKEL2010,
  MAURER2014, NGUYEN2021 (see correction below).

**Realistic two-week outcome:** 3 READY datasets + 2–3 digitised ones = a fittable
corpus for both organisms, with roughly 30–45 h of extraction work total. The blocker
can be removed in well under two weeks. The *Mtb* side is essentially solved on day one;
the *S. aureus* side needs either the Peyrusson source data (thin in time) or ~5 h of
digitisation of the 2025 hollow-fibre paper to get a proper long biphasic curve.

**Two corrections to the existing manifest — both material:**

1. **NGUYEN2021 is mis-catalogued.** The manifest says
   `data_source = supp_table (Supp Table 2 = non-normalized CFU)`. It is not.
   Supplementary Table S2 (inside `Data_Sheet_1.PDF`) is a table of *fitted Hill
   parameters* (Top, Bottom, EC50 with CIs) — the non-normalised CFU values live in
   Supplementary **Figure** S4, as pixels. Worse, the design is 2 time points (0 and
   24 h): it is a concentration–response experiment, not a time-kill. **It cannot be
   used to fit a persister tail at all.** Downgrade to `PRIOR_ONLY`.
2. **Pasipanodya 2015 (CID 61 Suppl 1:S10-7, PMID 26224767) does not tabulate the
   underlying data.** It is paywalled, has no PMC record, and Europe PMC reports
   `hasSuppl = N`. It catalogues 22 HFS-TB experiments (12 combination, 10 monotherapy)
   and reports PK/PD targets, not CFU-vs-time. **Value = bibliography only.** Its 10
   monotherapy studies are the best mining list for further HFS-TB candidates, but each
   would still need digitising.

---

## RANKED TABLE

| # | Dataset | Organism | Drug(s) | Open access | WHERE the numbers are | Est. hours | Verdict |
|---|---------|----------|---------|-------------|----------------------|-----------|---------|
| 1 | **ERA4TB / van Wijk & Lucia 2023**, *iScience*, `10.1016/j.isci.2023.106411`, PMC10119593 | *M. tuberculosis* H37Rv | moxifloxacin, isoniazid (1× and 10× MIC) | Yes, CC-BY | **figshare CSV — `10.6084/m9.figshare.19766083`.** Tidy 2,775-row CSV + readme. 2,120 numeric `CFUlog10` values | **2–4** | **READY** |
| 2 | **Apramycin Mtb raw data**, figshare `26462791` | *M. tuberculosis* | apramycin, amikacin (128/32/8/4/1 µg/mL) | Yes, CC-BY 4.0 | **figshare XLSX**, 5 sheets: Kill kinetics, Intracellular efficacy, Biofilm ×2, In-vivo. Triplicate log10 CFU | **2–3** | **READY** |
| 3 | **Peyrusson 2020**, *Nat Commun* 11:2200, `10.1038/s41467-020-15966-7`, PMC7198484 | *S. aureus*, intracellular (THP-1/J774) + broth | oxacillin, clarithromycin, moxifloxacin | Yes, CC-BY | **Source Data XLSX** (`41467_2020_15966_MOESM3_ESM.xlsx`, 13 sheets). Fig 1a/1h = 11-point concentration–response ×3 reps; Fig 1b/1i = time-kill 0/1/3/6/24 h ×3 reps, intracellular vs extracellular | **3–4** | **READY** |
| 4 | **Van Bambeke HFIM 2025**, *iScience*, PMC11930174 | *S. aureus* ATCC 29213, intracellular + extracellular | ciprofloxacin 400 mg q12h, moxifloxacin 400 mg q24h (monotherapy, dynamic) | **CC-BY-NC-ND, not CC-BY** — the no-derivatives clause blocks releasing digitised values without written permission from the corresponding author | **Figures only.** Data statement = "available upon request from the lead contact". 11 time points (0, 0.5, 1, 2, 4, 6, 8, 10, 12, 22, 24 h), 2–3 independent runs. Paper *explicitly* attributes the plateau to persisters | **4–6** | **DIGITISE (top S. aureus pick)** |
| 5 | **DRUSANO2018**, `10.1128/AAC.00221-18`, PMC6105790 | *M. tuberculosis*, acid-phase **and** non-replicating-persister phase | linezolid, monotherapy, 6 exposures (300/600/900 q24h; 600/1200/1800 q48h) + control | Free in PMC (no OA licence) | **Figures only** (Figs 1 and 3). No supplementary material. Tables 1–3 are PK/PD parameters, not CFU. 29 days; **n = 1 per arm** ("the experiment with the seven arms was performed once") | **8–12** | **DIGITISE** |
| 6 | **BROWN2015**, `10.1128/mBio.01741-15`, PMC4631805 | *M. tuberculosis* H37Rv, log-phase | linezolid, monotherapy, 5 exposures (342/600/858/1116 q24h, 300 q12h) + control | Yes, CC-BY | **Figures only** (Fig 5A total pop., 5B resistant subpop.). Supplement = 3 TIF figures (PK profiles + pred-vs-obs), **no data tables**. 21 days, 2 independent HFIM runs pooled as mean ± SEM, MIC 1 mg/L, inoculum 1×10⁵ CFU/mL | **6–10** | **DIGITISE** |
| 7 | **TSUJI2012**, `10.1128/AAC.05453-11`, PMC3393439 | *S. aureus* MRSA USA300 | linezolid, monotherapy, 5 regimens (600 q12h + 4 front-loaded) | Free in PMC, `isOpenAccess = N` | **Figures only.** Europe PMC: `hasSuppl = N`. 8 time points (0/24/48/72/96/144/192/240 h), inoculum 1e6 CFU/mL, **LOD 1e2 CFU/mL**, quintuplicate plating. Caution: paper reports eradication and *does not* discuss a tail | **6–8** | **DIGITISE (low priority — weak tail)** |
| 8 | **FERRO2015**, `10.1128/AAC.02282-15`, PMC4775936 | *M. abscessus* (wrong organism) | amikacin, 8 exposures | `isOpenAccess = N` (PMC author manuscript) | Figures only | 6–8 | **DEPRIORITISE — wrong organism** |
| 9 | **GUMBO2004**, `10.1086/424849` | *M. tuberculosis* | moxifloxacin | **No** — paywalled, no PMC, no supplement | Figures only, behind paywall | 8+ | **UNUSABLE without institutional PDF** |
| 10 | **FERRO2014**, `10.1093/jac/dku431` | *M. abscessus* | 5 drugs | **No** — paywalled, no PMC, `hasSuppl = N` | Figures only | 8+ | **UNUSABLE** |
| 11 | **DESTEENWINKEL2010**, `10.1093/jac/dkq374` | *M. tuberculosis*, high vs low metabolic activity | RIF/INH/EMB/AMK | **No** — paywalled, no PMC, `hasSuppl = N` | Figures only | 8+ | **UNUSABLE** (design is attractive — metabolic-state contrast — but the data is inaccessible) |
| 12 | **MAURER2014**, `10.1128/AAC.02448-14`, PMC4068550 | *M. abscessus* | 4 drugs | `isOpenAccess = N`, `hasSuppl = N` | Figures only | 8+ | **UNUSABLE** |
| 13 | **NGUYEN2021**, `10.3389/fmicb.2021.785573`, PMC8715871 | *S. aureus* biofilm + stationary planktonic | moxifloxacin | Yes, CC-BY | **Supp Table S2 = fitted Hill parameters, NOT raw CFU** (verified by extracting `Data_Sheet_1.PDF`). Raw CFU is in Supp **Fig** S4. Only 2 time points (0, 24 h) | n/a | **PRIOR_ONLY — cannot fit a tail** |
| 14 | **Pasipanodya 2015**, `10.1093/cid/civ425`, PMID 26224767 | *M. tuberculosis* (review of 22 HFS-TB studies) | various | **No** — paywalled, no PMC, no supplement | Does **not** tabulate underlying CFU | n/a | **BIBLIOGRAPHY ONLY** |
| 15 | **HFS-TB reproducibility 2023**, `10.1093/jac/dkad029`, PMC10068422 | *M. tuberculosis* | HRZE, HRZM, RMZE, high-dose RZM | Yes | 1,026 individual CFU counts claimed; single 27 KB .docx supplement, contents not the raw counts. **All arms are combination therapy** | n/a | **UNUSABLE — combination only** |
| 16 | **Epetraborole HFS-TB**, PMC12587543 | *M. tuberculosis* XDR | epetraborole (monotherapy, 6 doses) | Yes | Figures only. Data statement: "available with the corresponding author, upon a reasonable request" | 6–8 | Reserve — DIGITISE if more Mtb arms needed |

---

## DETAIL ON THE THREE READY DATASETS

### 1. ERA4TB Mtb time-kill — the single best find
`https://doi.org/10.6084/m9.figshare.19766083` → `[SUPP] 20220211_RC van Wijk et al_TKAdata.csv` (177 KB) + readme.

Verified structure (columns): `Group, Replicate, Time, CFU, CFUlog10, Condition, Volume,
AQL, BQL, Institute, Sample, Comments`.

- **Groups (monotherapy, stated concentration):** 0 = untreated; 1 = 1× MIC moxifloxacin;
  2 = 10× MIC MXF; 3 = 1× MIC isoniazid; 4 = 10× MIC INH. Reference MICs: MXF 0.06 µg/mL,
  INH 0.5 µg/mL.
- **Time points:** −3, 0, 1, 2, 3, 7, 10, 14, 15, 21, 28 days (11 levels; 9–11 per group).
- **Replicates:** 3 technical replicates × **6 independent laboratories** (blinded A–F)
  × **4 plating conditions** (100 µL quad / 10 µL 4-drop / 10 µL single / 2.5 µL single).
- **Rows:** 2,775 total, **2,120 with a numeric `CFUlog10`**. Restricting to the standard
  100 µL quad plating still gives 535 usable observations.
- **Inoculum:** 1e4 CFU/mL pre-inoculum at t = −3 d, ~1e5 CFU/mL at treatment start.
- **Range:** log10 CFU 1.00 → 9.45. Censoring is explicit via the `AQL` / `BQL` flags
  (no flagged rows among the numeric values — censored observations carry `CFU = NA`).
- **Persister/tail behaviour:** the paper reports three profiles — limited inhibition at
  1× MIC, bactericidal at 10× MIC, and **regrowth after initial decline under INH**.
  A slow phase is present; the 6-lab replication also gives a genuine between-lab
  random effect to model.
- **Caveat:** static concentrations, not a dynamic PK profile, and no dedicated
  non-replicating-persister arm. It is a clean two-population fit, not an NRP experiment.

### 2. Apramycin Mtb raw data (figshare 26462791, CC-BY 4.0)
Single file `Raw Data.xlsx`, 5 sheets. The `Kill kinetics` sheet is a genuine
concentration × time monotherapy design:

- **Drugs:** apramycin and amikacin, both at 128 / 32 / 8 / 4 / 1 µg/mL, plus a cell control.
- **Time points:** day 0 (baseline), 3, 7, 14.
- **Replicates:** 3 per cell, log10 CFU given per replicate plus mean and log-drop.
- **Starting inoculum:** ~7.0 log10 CFU/mL. Values reach 1.7–1.9 log10 by day 14 at
  128 µg/mL, so there is a wide dynamic range and a visible flattening.
- Sheets `Intracellular efficacy` (macrophage, day 3) and `Biofilm 1/2` (drug-tolerant
  state, 1×–64× MIC) give a second, tolerance-relevant comparison in the same numeric format.
- **Caveat:** only 4 time levels. Good for exposure–response; thin for a two-phase kill
  rate unless combined with dataset 1.

### 3. Peyrusson 2020 *S. aureus* Source Data (Nat Commun, CC-BY)
`41467_2020_15966_MOESM3_ESM.xlsx`, 13 sheets, one per figure panel. The relevant ones:

- **Fig 1a** — concentration–response, log conc −2.52 → 2 (×MIC), 11 levels, 3 replicates,
  for **moxifloxacin, oxacillin, clarithromycin** (intracellular).
- **Fig 1h** — same 11-level concentration–response for exponential-phase vs
  macrophage-recovered bacteria, 3 replicates. Note the −4.2 floor = limit of detection.
- **Fig 1b / 1i** — the time-kill: t = 0, 1, 3, 6, 24 h, 3 replicates, **intracellular vs
  extracellular**, three drugs at **50× MIC**. Inoculum 1e6 CFU/mL.
- The paper's headline result is exactly the thing being modelled: biphasic killing, with
  the bulk of the population rapidly killed and a slower-killed subpopulation persisting,
  plateauing intracellularly from ~3 h.
- **Caveat and the reason this is not a slam dunk:** only 5 time points, all inside 24 h.
  The plateau is visible but the slow phase rests on 3 points. Pair it with dataset 4
  (digitised) for a defensible *S. aureus* fit.

---

## WHAT WAS SEARCHED AND CAME UP EMPTY

Recording these so the search is not repeated.

- **Zenodo API** (`Staphylococcus aureus time-kill`, `S. aureus persister CFU`,
  `tuberculosis time-kill CFU`, `antibiotic time-kill curve dataset`): nothing relevant.
  The only near-hit is record `16753477` (photodynamic inactivation of *S. aureus*
  persisters) — not antibiotic PD.
- **Dryad API** (`S. aureus persister`, `time-kill antibiotic`, `Mtb antibiotic killing`):
  nothing relevant. Closest is an *A. baumannii* meropenem colony-count dataset.
- **figshare API** by author (van Wijk / Simonsson / Ramón-García): no further deposits
  beyond `19766083`.
- **A published compilation or re-analysis that has already digitised time-kill curves
  for these organisms does not appear to exist.** Searches for a digitised time-kill
  database / WebPlotDigitizer meta-analysis returned only single-organism PD modelling
  papers (*N. gonorrhoeae*, calf respiratory pathogens). **This is a gap — and arguably a
  contribution the paper can claim**, i.e. release the digitised corpus itself.
- **A directly competing preprint exists:** "Comparative Modeling of Antibiotic
  Resistance, Tolerance, and Persistence in Mycobacterium tuberculosis and
  Staphylococcus aureus", bioRxiv `10.1101/2025.02.12.637810` (Feb 2025). It is
  **simulation-only** — parameters taken from the literature, no CFU data fitted, and its
  promised GitHub repo was not live at posting. That is both a warning (someone is in
  this space) and an opening (fitting real data is the differentiator).
- **PLOS supplements are figure-only** for the two obvious *S. aureus* persister papers
  (PLOS Genetics `10.1371/journal.pgen.1003123` supplements are .ppt/.docx figures;
  PLOS ONE daptomycin/glucose `10.1371/journal.pone.0150907` S1–S6 are all figures).
  Both are also 2-point or short designs.
- **Combination-only, therefore excluded:** the 1,026-CFU-count HFS-TB reproducibility
  study (`10.1093/jac/dkad029`) is entirely HRZE/HRZM/RMZE regimens — no monotherapy arm.

---

## RECOMMENDED PLAN

**Days 1–2 (zero risk):** ingest the three READY datasets. Move them into `data/raw/`
with provenance files and write the loaders. This alone converts "no data" into
"three datasets, two organisms, CC-BY".

**Days 3–6:** digitise the Van Bambeke 2025 HFIM figures (*S. aureus*, 11 time points,
2 fluoroquinolone monotherapy arms, intracellular + extracellular, explicitly biphasic).
This is the single highest-value digitisation on the list: it is the *S. aureus* curve
with a real tail and enough time resolution to identify a slow-phase rate constant.
In parallel, email the lead contact — the paper says data are available on request, and a
positive reply removes the digitisation entirely.

**Days 7–10:** digitise DRUSANO2018 (acid-phase and NRP-phase *Mtb*, 6 linezolid
exposures). This is the only candidate in the whole list with an explicit
**non-replicating-persister** arm, which is the mechanistic centrepiece of the paper.
Budget generously — it is 2 figures × 7 arms × ~10 points, and n = 1 per arm means
there are no error bars to anchor the weighting.

**Days 11–14:** BROWN2015 as the *Mtb* log-phase companion to DRUSANO2018 (same drug,
same lab, same model system — a clean log-phase vs acid/NRP contrast within one drug),
plus write-up of the extraction protocol.

**Do not spend time on:** GUMBO2004, FERRO2014, FERRO2015, DESTEENWINKEL2010,
MAURER2014 (paywalled and/or wrong organism), NGUYEN2021 as a time-kill source, and
the Pasipanodya supplement (it does not exist).

**Contact-the-authors shortlist** (parallel, costs an hour, may pay off big):
1. F. Van Bambeke (UCLouvain) — HFIM 2025 *S. aureus* datasets, stated available on
   request. The same group authored Peyrusson 2020 and Nguyen 2021, so one email covers
   three papers.
2. S. Ramón-García / R. van Wijk (ERA4TB) — they already deposit openly; ask whether the
   MPN readouts and any additional drugs were released.
3. G. Drusano / A. Louie (Institute for Therapeutic Innovation) — DRUSANO2018 and
   BROWN2015 raw HFIM CFU.

---

## VERDICT COUNTS

- **READY (numbers directly available, no digitisation): 3**
  — ERA4TB Mtb (figshare CSV), Apramycin Mtb (figshare XLSX), Peyrusson *S. aureus*
  (Nat Commun Source Data XLSX).
- **DIGITISE (worth doing): 4** — Van Bambeke 2025, DRUSANO2018, BROWN2015, TSUJI2012.
- **UNUSABLE / deprioritised: 6** — GUMBO2004, FERRO2014, FERRO2015, DESTEENWINKEL2010,
  MAURER2014, NGUYEN2021-as-time-kill.
- **Reference only: 2** — Pasipanodya 2015 (bibliography), dkad029 (combination only).

**Fastest path per organism:**
- ***M. tuberculosis*** → the **ERA4TB figshare CSV** (`10.6084/m9.figshare.19766083`).
  Monotherapy, two drugs, two exposure levels, 11 time points, 6 labs, 2,120 numeric
  log10 CFU values, CC-BY, already downloaded. Fittable this afternoon.
- ***S. aureus*** → the **Peyrusson 2020 Nat Commun Source Data file** for immediate
  numbers, immediately followed by digitising the **Van Bambeke 2025 iScience HFIM
  figures** (~5 h) to get the time resolution the Peyrusson panels lack.

---

*Sources verified through PubMed / PubMed Central, Europe PMC, and the figshare, Zenodo
and Dryad APIs. Key DOIs:
[10.1016/j.isci.2023.106411](https://doi.org/10.1016/j.isci.2023.106411),
[10.6084/m9.figshare.19766083](https://doi.org/10.6084/m9.figshare.19766083),
[10.1038/s41467-020-15966-7](https://doi.org/10.1038/s41467-020-15966-7),
[10.1128/AAC.00221-18](https://doi.org/10.1128/AAC.00221-18),
[10.1128/mBio.01741-15](https://doi.org/10.1128/mBio.01741-15),
[10.1128/AAC.05453-11](https://doi.org/10.1128/AAC.05453-11),
[10.3389/fmicb.2021.785573](https://doi.org/10.3389/fmicb.2021.785573),
[10.1093/cid/civ425](https://doi.org/10.1093/cid/civ425),
[10.1093/jac/dkad029](https://doi.org/10.1093/jac/dkad029).*
