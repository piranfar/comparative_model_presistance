# What this project still needs from outside

> Produced by a 20-agent audit on 2026-09-05. Each availability claim was
> checked live. Treat the citations as leads to verify, not as verified.

# What this project still needs from outside — prioritised

Sixty-eight needs were logged by the audit. After live checking, **four require you; most of the rest do not.** The single largest finding is that a great deal of the "missing" material is already free, already downloaded, or already in `data/raw/`.

**Urgent housekeeping, not a request:** the audit left **804 files** in the session scratchpad (`…/5583ba58-…/scratchpad/`), including the Peyrusson Source Data workbook, the Nguyen supplement, the Ferro PDF, the Carvalho supplement and the Vogwill full-text XML. That directory is session-local temp and will vanish. Staging the keepers into `data/raw/` with `PROVENANCE.json` is a one-hour job that would close roughly a dozen audit items with no external help at all. `data/digitized/` is still empty.

---

## 1. Things the project does not need help with

Do not ask the PI for any of these. Every one is free or already on disk.

| Audit item | Reality | Where |
|---|---|---|
| FERRO2014 "UNUSABLE, paywalled" | Publisher's version is free (Taverne Art. 25fa). Already downloaded this session. | https://repository.ubn.ru.nl/handle/2066/154302 |
| GUMBO2004 institutional PDF (€39) | Not worth buying. The Mtb × moxifloxacin cell is already covered twice over. | `data/raw/tb/era4tb_timekill.csv` (2,775 rows, 11 time points, 6 labs, already in repo) + Drusano 2021, PMC8097450, free, 9 exposure arms vs Gumbo's handful |
| Vogwill dose units + exposure duration | **Resolved.** Duration is **4 h**, not the 5 h exp11 assumes. Doses are exact doublings: 1×/2×/4× genus-max MIC = ciprofloxacin 60/120/240 ng/mL, rifampicin 15/30/60 µg/mL. | PMC5021160, free; Europe PMC JATS XML |
| Windels MIC in µg/mL, zMIC mapping | **Already in repo**, MD5-identical to Zenodo 10.5281/zenodo.7550302. Endpoint MIC for all nine conditions incl. 12.5 × 0.25 (n=20, geometric mean 2.64 µg/mL). | `data/raw/windels2024/phenotypes_after_evol.csv` — currently read by *no script in `src/`* |
| Simsek & Kim per-cell lag times | A table **4× finer** than the log bins exp12 hard-codes is already on disk: SI p.6, "Data presented in Fig. 2a" — 16 and 19 rows instead of 5 and 6 bins. Continuous per-cell times do not exist for anyone; the assay is interval-censored by design. | `data/raw/external_survival/pnas.1903836116.sapp.pdf` |
| Peyrusson 2020 Source Data (the only numeric S. aureus source) | Free direct download, already fetched. | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-020-15966-7/MediaObjects/41467_2020_15966_MOESM3_ESM.xlsx` |
| Second independent two-state persistence model + calibration data | **Two found, both free, both non-Leuven.** Carvalho 2017 (Clermont/INRAE), PMC5658594 — and its numeric killing curves are recoverable from the supplement's chart XML, already extracted. Singh 2023, PMC9882918 — model *and* data on public GitHub. | doi:10.1111/1751-7915.12739; doi:10.1371/journal.pcbi.1010243 |
| "Zero datasets for Klebsiella" (docs/12 ESKAPE tally) | Carvalho 2017 **is** *K. pneumoniae* CH1440 + ciprofloxacin with killing curves. One of the three empty genera is fillable today. | as above |
| Quantitative biofilm effect on kill rate | Walters 2003, PMC148957 — the only paired planktonic-vs-biofilm measurement at same drug, concentration and time. Ciprofloxacin 3.40 → 0.610 /h (5.6×); tobramycin 2.99 /h → **net growth** (+0.09 log at 4 h). | doi:10.1128/AAC.47.1.317-323.2003 |
| Apramycin Mtb raw data ("READY" but never ingested) | CC-BY 4.0, one 27 KB xlsx, no login. Includes a biofilm arm. | doi:10.6084/m9.figshare.26462791.v1 (journal not PubMed-indexed; no PMID exists) |
| Galvanin 2013 supplementary material | The **four ESM files are not paywalled** (HTTP 200, no auth), even though the body is. Read these before spending a library request. | `…/esm/art%3A10.1007%2Fs10928-013-9321-5/MediaObjects/10928_2013_9321_MOESM1–4_ESM.docx` |
| Antia 1996 (paywalled until ~2066) | Chakraborty & Ganusov 2024, PMC11793202, CC-BY, restates the model verbatim and names *f* and *g* as dormancy and reactivation rates — plus records that Antia's parameters were ad hoc and never fitted to data, which is *more* useful to you than the original. | doi:10.3389/fams.2024.1355373 |
| LOD for FERRO2015 and NGUYEN2021 | Not needed. Ferro: burden never fell below the 10⁶ inoculum (authors' own abstract). Nguyen: fitted lower plateau 4.0–5.0 log₁₀ CFU/mL (Supp Table S2). Censoring is not operative in either. | PMC4775936; PMC8715871 |
| Kristoffersson PAGE 2011 abstract 2243 | Free, retrieved and confirmed (PopED, 5→7 sampling points, autocorrelation half-life ~7.5 h). | https://www.page-meeting.org/?abstract=2243 |
| CRyPTIC MIC compendium | Open FTP, no DUA. | `ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/` |
| pH × O₂ × nutrient compounding | Two free primary sources: Bren 2023 PNAS (PMC10742385, kill-*rate* axis, nutrient × stress crossed) and Gold 2012 PNAS (PMC3479555, pH × O₂ × carbon deconstructed on a killing readout). | doi:10.1073/pnas.2312651120; doi:10.1073/pnas.1214188109 |

---

## 2. Things only the PI can unblock

Four requests, ranked. The first two are worth more than everything below them combined.

**1 — One email to Françoise Van Bambeke (UCLouvain, `francoise.vanbambeke@uclouvain.be`).**
One message covers four things because she is senior author on all of them. Request: (a) the non-normalised replicate-level CFU behind NGUYEN2021 Supplementary Fig. S4, with the plating limit of detection, which the paper never states; (b) the Mahieu 2025 *iScience* datasets — the data statement says "available upon request from the lead contact" (PMC11930174, doi:10.1016/j.isci.2025.112076); (c) written permission to redistribute digitised values from Mahieu 2025, which is **CC-BY-NC-ND**, not CC-BY as docs/06 records — the ND clause currently blocks including it in any released corpus.
*What it buys:* the S. aureus × moxifloxacin cell goes from 5 time points (Peyrusson) to **11 static time points over 24 h plus a dynamic hollow-fibre arm** against ATCC 29213. That is the difference between a fitted slow-phase rate and an assertion. The paper explicitly invites the request ("without undue reservation").

**2 — One email to Giorgio Boccarella and Pieter van den Berg (KU Leuven, `giorgio.boccarella@kuleuven.be`, `piet.vandenberg@kuleuven.be` — note *piet*, not *pieter*).**
The public record is now exhausted: the second figshare deposit (10.6084/m9.figshare.30833897) that looked like an undeposited script variant is **byte-identical** (MD5 edfa8330a7bc692c3b518276d69c650f) to the cited one; his ORCID lists only three works; Crossref shows no preprint. Only the authors can explain the residual.
The ask has **shrunk from four questions to one plus confirmations**: σ = 0.7 is settled (all four deposited drivers set it; Table 1's 0.07 is wrong by 10×), and *b* = 1.7 is settled (it fixes ψ_max via `psimaxS = bS − dS`; the realised birth rate is `mic_to_br(...)` = 2.0). What remains genuinely open is **the excess non-evolving populations (8/48 vs their 3/500)**, plus a *fifth* discrepancy the audit had not found: `psiminPR` is not the flat −0.5 that Table 1 states — all four drivers reassign `min_mic_threshold = c`, making the persister kill rate a function of both MIC and antibiotic concentration, documented nowhere.
*What it buys:* docs/08 sets a standing rule that no statement about their conclusions enters any manuscript until this is explained. That rule currently gates exp05, exp08, exp10 and **the whole of Section 5 of the shielding manuscript**. Both paper and deposit are CC-BY 4.0, so if they do not reply the analysis can be published independently — but the rule has to be lifted deliberately, by you.

**3 — Interlibrary loan: de Steenwinkel et al., *J Antimicrob Chemother* 2010;65(12):2582-9, doi:10.1093/jac/dkq374, PMID 20947621.**
Paywalled, no PMC, no supplement (per the project's own feasibility audit; not independently re-checked in this pass). Routine ILL, 1–3 days, free.
*What it buys:* this is the only published Mtb design crossing an aminoglycoside concentration series with a metabolic-activity contrast — and its stated conclusion runs *against* the project's central transfer (amikacin equally effective irrespective of metabolic state, versus the ~19-fold nutrient dependence exp14 reads off amikacin in *E. coli*). It is the falsification test, not a supporting citation. That is exactly why it should be got.

**4 — One email to the Florida hollow-fibre group (`gdrusano@ufl.edu`, `Ashley.Brown@medicine.ufl.edu`).**
Request the plating volume and the CFU/mL treated as below-detection in the HFIM quantitative cultures for DRUSANO2018 and BROWN2015 (same lab, one message).
*What it buys:* the LOD is genuinely absent from all four corpus papers — I searched the full texts (7,954 / 9,510 / 8,610 / 14,019 words) for every phrasing including figure-legend dashed-line markers: zero matches. But it only *matters* for DRUSANO2018, where eradication is reported at day 21 against an untreated control standing at just 3.37 log₁₀. A defensible bound already exists (200 µL zero-dilution plate → 5 CFU/mL = 0.70 log₁₀, derivable from the stated methods); confirmation would let the censored fit be presented as measured rather than inferred.

**Second tier — worth an ILL slip only if convenient:**
Galvanin 2013 body (doi:10.1007/s10928-013-9321-5, PMID 23733369; Springer $39.95 — **read the four free ESM files first**); Clewe 2016 raw CFU from the Simonsson group, Uppsala (doi:10.1093/jac/dkv416, PMID 26702921 — 8–9 static rifampicin concentrations in two physiological states, the only Mtb design able to identify ψ_max, ψ_min, zMIC and κ jointly); the eLife 93243 depositing group for a rifampicin concentration series on 20–30 of the 217 isolates (citation from the project's own audit, not re-verified here); Pasipanodya 2015 *Clin Infect Dis* for the index of 22 HFS-TB experiments.

**Explicitly do not bother:** GUMBO2004 (substitutes are free and richer); Antia 1996 (substitute is better); Bryant 1992 and König 1993 (only the ratios are wanted and they are in the free abstracts); Reynolds 1976 (citation unverified — no DOI or PMID is recorded anywhere in the repo, so an ILL slip cannot even be filled out).

---

## 3. Things that need a decision, not a download

**The FERRO2014 finding is the one to look at first.** Having read the paper: it reports **no time-kill curves for linezolid or moxifloxacin against *M. abscessus***. Figure 1 is cefoxitin, amikacin, clarithromycin only. The linezolid and moxifloxacin time-kill in that paper is against ***M. fortuitum* ATCC 6841** — a different organism. Digitising it fills **zero** of the two cells docs/02 assigns it, and the "highest value per hour" ranking rests on that error. Your call, and it is a design decision no one else can make: (a) change the middle row of the 3×2 from *M. abscessus* to *M. fortuitum*, in which case one experiment in one lab does fill both cells with published Emax/EC50/Hill already tabulated — but the "*M. abscessus* is essentially not killed" narrative goes; or (b) keep *M. abscessus* and substitute Maurer 2014 (PMC4068550, free), accepting three time points to 24 h and no persister tail.

**What is the primary estimand?** Ferro's Table 2 already gives Emax, EC50, Hill slope and R² with CIs for all seven fitted species-drug pairs. If the estimand is Emax/EC50, that is a transcription job of minutes and no digitisation is needed. If it is a slow-phase rate, digitisation is unavoidable — though cheaper than feared (the Ferro figures are **vector, not raster**: 804 moveto / 3013 lineto operators on the Figure 1 page, so extraction is scriptable in ~2 h, not the 8+ h docs/06 budgets).

**The novelty claims.** Galvanin's published nomenclature — visible outside the paywall — already includes "D: Detectability threshold". So "practical identifiability under a detection floor" is a weaker differentiator than docs/05 assumes. The defensible differentiators are persistence-vs-resistance and profile-likelihood-vs-Fisher-information. Separately, one targeted PAGE check already flipped Q3 from "gap" to "already done", and ACoP/ECCMID/ASM abstracts were never searched. Decision: reframe as "first systematic treatment" without priority claims, or commission the abstract sweep before writing.

**The 0.20–0.68 /h slow-phase range.** `exp13_slow_phase_fits.csv` at ≥50 µg/mL spans **0.140 to 1.055 /h** across six nutrient levels. The quoted range silently drops the 0.90 and 0.95 nutrient levels, where measured persister killing reaches 0.81 and 1.05 /h — the levels that would contradict the abstract's pivot that the model's 0.45 /h "matches the measured one". Either state and defend the selection rule, or widen the range and rewrite the abstract. This is an integrity call, not a data gap.

**Attribution of the 1.7-fold contrast.** The manuscript credits "about 1.7-fold" to Boccarella et al.; 1.719 is the repo's own re-run, and their deposited Fig-3 output gives 2.02-fold. The attribution and the arithmetic disagree in the same paragraph.

**Does biofilm enter the site-variable table at all?** Walters' own conclusion is that biofilm tolerance tracks oxygen limitation and low metabolic activity, *not* poor penetration — i.e. it is the same PMF/metabolic axis Block B already carries, not a fourth multiplicative term. Adding it separately would repeat exactly the error §2 warns about. Note also that Ceri 1999 (PMC84946) and Walters flatly disagree on tobramycin against *P. aeruginosa* (2–4× vs total failure of killing); different strain, different assay, both primary. Pick, or report both.

**Is compounding a gap or a finding?** Bryant 1992 censors at >10.4× at the assay ceiling, and Gold 2012 reports that at low pH "the activity … was indistinguishable at O₂ levels of 21% and 1%". Both point the same way: the second stress adds little once the first is applied. That is reportable as *redundancy, not multiplication* — a result, rather than a hole awaiting an experiment nobody has run.

**Author-only statements** (all placeholders in the drafts, none obtainable by anyone else): the LLM-use human-verification statement (`BMB_MANUSCRIPT.md:226-228`), CRediT author contributions (`:358`), and the archived release DOI or commit hash for the reproducibility claim (`:367-368`).

**The Wallis "special populations hypothesis"** has no PubMed record under that phrase. As a microbiologist you may simply know the source; otherwise it should be dropped or re-attributed to the verified Wallis 2016 (PMID 27242697). This is recall, not retrieval.

---

## 4. What is not a gap at all

- **"The S. aureus × moxifloxacin cell has no kinetic data" (docs/02 constraint 5) is wrong.** NGUYEN2021 Figure 5A *is* a time-resolved kill curve — moxifloxacin 100 mg/L against stationary-phase and biofilm cultures, triplicate, plateau at 5–10 h, persister fractions ~0.01% and 0.04%, with the authors' own two-phase fit (R² > 0.997) and an MDK table at 1-, 2- and 3-log. What is genuinely missing is concentration-*resolved* kinetics and kinetics for the clinical isolates. Reword the constraint; do not chase the data.
- **The zMIC / µg-mL "unit mismatch" does not exist.** Both axes are µg/mL anchored at MIC_WT = 2 µg/mL — stated in two Windels figure legends and hard-coded in the Boccarella deposit (`initial_MIC = 2`) and in `src/models/boccarella.py:46`. Every evolution concentration is supra-MIC (6.25× to 200×). This concession should be **withdrawn**, along with the claim that it "alone can generate the whole discrepancy".
- **The empty 12.5 × 0.25 cell is not lost data.** The Windels Fig. 4A legend states no measurements were made because no evolutionary adaptation was observed. The endpoint MIC exists (n=20, median 2). Usefully, this also *kills* the "resistance evolved" explanation for the 0.958 survival at that condition — which strengthens the nutrient-dependent kill-rate reading rather than weakening it.
- **"The Virkar–Clauset refit is impossible from binned counts" is backwards.** Virkar & Clauset 2014 (*Ann Appl Stat* 8(1):89-119, doi:10.1214/13-AOAS710; free preprint arXiv:1208.3524) is *specifically the binned-data version* of the framework. Binned counts are its intended input. Expect the honest outcome to be "power law not rejected, lognormal and truncated power law not distinguishable" — tails of 53 and 171 cells are at the practical floor for the method.
- **No data deposit exists for Galvanin 2013, and none should.** It is a pure simulation study on synthetic data generated from the Tam and Campion models; the Campion model is free in full at PMC538881.
- **The Boccarella "undeposited script variant" hypothesis is closed.** Second figshare item is byte-identical; ORCID lists three works; no preprint. Stop searching the public record.

**Four items the audit called external gaps are actually internal work, and running them would cost less than any email above.** I verified all four: `grep` finds **no Fisher's exact test anywhere in `src/`** (the p = 2×10⁻⁷ in Section 5 is unreproducible); **no script sets Emax_P to zero** and no table holds the 370 h / 20 h counterfactual; nothing in `results/tables/` produces the 0.70 mid-pulse-waking figure; and `exp11` line 153 passes the raw dose-level index (1, 2, 3) into a `log2` regression, compressing the x-range by 1.585/2 — with the now-confirmed 1×/2×/4× axis, the ciprofloxacin slope corrects from −3.72 to **−3.08** and the headline drops from 13.4-fold to **11.1-fold** (it still exceeds the model ceiling; rifampicin still does not).

Finally, two literal tab characters where `\times` was intended, confirmed by byte inspection at `SHIELDING_MANUSCRIPT.md:256` and `:269` — both Section 5 p-values currently typeset as `$p = 2<TAB>imes10^{-6}$`.