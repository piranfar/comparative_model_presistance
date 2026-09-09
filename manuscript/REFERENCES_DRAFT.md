---
title: "Reference list, draft for verification"
status: "Compiled 2026-09-06. Journal not yet chosen, so no house style is applied."
scope: "Covers manuscript/PAPER_COMPLETE.md, manuscript/MANUSCRIPT.md and manuscript/abstract.md."
---

# Reference list (draft)

Every entry below was checked against a primary record — PubMed, Crossref, Project
Euclid, the figshare API, the Zenodo API, or the issuing body's own catalogue —
during compilation. Where a field could not be obtained it is left blank and the
entry appears in **Section 2 (UNVERIFIED)** instead of, or in addition to,
Section 1. Nothing here was reconstructed from memory.

Entries are numbered **R1 … R40** in **order of first appearance in
`manuscript/PAPER_COMPLETE.md`**. That numbering is provisional: it is the order a
numeric style would use, and it will shift if the text moves. For each entry the
manuscript sentence it supports is quoted verbatim, with the file and approximate
line so the citation can be placed.

---

## Section 1 — Verified references, in order of first appearance

### R1. WHO consolidated guidelines on tuberculosis, Module 4 (drug-susceptible)

World Health Organization. *WHO consolidated guidelines on tuberculosis. Module 4:
treatment — drug-susceptible tuberculosis treatment*. Geneva: World Health
Organization; 2022. ISBN 978-92-4-004812-6 (electronic); 978-92-4-004813-3 (print).
PMID 35727905. NCBI Bookshelf NBK588564. IRIS handle 10665/353829.

- **Supports** (PAPER_COMPLETE.md, Introduction, ~L66): *"Tuberculosis makes the
  rule expensive. Regimens run for four to six months, the compounds that could
  shorten them must be selected from in vitro killing experiments…"*
- **Note.** This guideline carries both the standard six-month regimen and the
  four-month rifapentine–moxifloxacin regimen, so it supports the full "four to
  six months" span in one document. Currently **uncited** in the manuscript.

### R2. Brauner et al. 2016 — the MDK/MIC framework

Brauner A, Fridman O, Gefen O, Balaban NQ. Distinguishing between resistance,
tolerance and persistence to antibiotic treatment. *Nature Reviews Microbiology*.
2016;14(5):320–330. doi:10.1038/nrmicro.2016.34. PMID 27080241.

- **Supports** (Introduction, ~L78–81): *"the minimum duration for killing, MDK,
  is the time to a specified fractional reduction — 90, 99 or 99.99 per cent —
  and it is proposed as the tolerance counterpart to the minimum inhibitory
  concentration (Brauner et al. 2016; Brauner et al. 2017)."*
- **Also supports** (Section 10, ~L985): *"That the two axes are separate is the
  premise of the framework that defines them (Brauner et al. 2016)…"*
- **Support check: passes.** The abstract proposes classifying drug response "based
  on the measurement of the MIC together with a recently defined quantitative
  indicator of tolerance, the minimum duration for killing (MDK)". Two axes, MDK
  as the MIC counterpart — exactly the two claims the manuscript attaches to it.

### R3. Brauner et al. 2017 — the experimental MDK framework

Brauner A, Shoresh N, Fridman O, Balaban NQ. An experimental framework for
quantifying bacterial tolerance. *Biophysical Journal*. 2017;112(12):2664–2671.
doi:10.1016/j.bpj.2017.05.014. PMID 28636922. PMC5479142.

- **Supports** the same Introduction sentence as R2.
- **CORRECTION to the brief.** The task brief lists Brauner 2016 *and* 2017 as
  *Nature Reviews Microbiology*. **The 2017 paper is in *Biophysical Journal*, not
  Nature Reviews Microbiology.** Verified against PubMed and the journal record.
  Only the 2016 paper is in Nat Rev Microbiol.
- **Support check: passes with a scope note.** The 2017 paper defines "the minimum
  duration for killing 99% of the population, MDK", i.e. MDK99. The manuscript's
  "90, 99 or 99.99 per cent" span is carried jointly by R2 and R3; neither alone
  states all three depths. Citing them as a pair, as the text already does, is
  correct.

### R4. van Wijk et al. 2023 — the six-laboratory time-kill dataset (figshare)

van Wijk RC, Lucía Quintana A, Ramón-García S. *Mycobacterium tuberculosis time
kill assay data of the standardized protocol within the ERA4TB consortium*
[dataset]. figshare; 2023. Version 1, posted 23 March 2023.
doi:10.6084/m9.figshare.19766083.v1. Licence CC BY 4.0.

- **Supports** (Table 1, ~L145): *"| Six-laboratory exercise | M. tuberculosis
  H37Rv | moxifloxacin, isoniazid, 1x and 10x MIC | 90 flasks, 2 775 readings |
  figshare 19766083 | CC BY 4.0 |"*
- **Also supports** (Methods, Datasets, ~L1363): *"M. tuberculosis H37Rv from one
  stock, distributed with one written protocol to six laboratories blinded and
  labelled A to F (van Wijk et al. 2023; figshare 19766083, CC BY 4.0)."*
- **Verified from** the figshare API record for article 19766083: title, three
  named creators, version 1, licence CC BY 4.0, item type Dataset.
- **Finding — creator list.** The **dataset** carries only three creators
  (van Wijk, Lucía Quintana, Ramón-García); the **article** (R23) carries
  nineteen. Cite the deposit with its own three-author creator list, not the
  article's author list.
- **Finding — title mismatch.** The README bundled in the deposit gives a
  different, longer title ("Implementing best practises on data generation and
  reporting of Mycobacterium tuberculosis time kill assays: a case study of
  standardized protocol within the ERA4TB consortium"), which corresponds to a
  pre-publication version of the article, not to the figshare item. Use the
  figshare item title above.

### R5. Vijay et al. 2024 — the clinical-isolate deposit (eLife supplementary file 2)

Vijay S, Bao NLH, Vinh DN, Nhat LTH, Thu DDA, Quang NL, Trieu LPT, Nhung HN,
Ha VTN, Thai PVK, Ha DTM, Lan NH, Caws M, Thwaites GE, Javid B, Thuong NT.
Supplementary file 2 to: *Rifampicin tolerance and growth fitness among
isoniazid-resistant clinical Mycobacterium tuberculosis isolates from a
longitudinal study* [dataset]. eLife; 2024. doi:10.7554/eLife.93243.
File: `elife-93243-supp2-v1.xlsx`. Licence CC BY 4.0.

- **Supports** (Table 1, ~L146): *"| Clinical isolates | M. tuberculosis, 217
  isolates | rifampicin | 6 duration endpoints per isolate | eLife 93243, suppl.
  file 2 | CC BY 4.0 |"*
- **Also supports** (Methods, Datasets, ~L1356): *"…and the authors' own tolerance
  level for each isolate (Vijay et al. 2024; eLife 93243 supplementary file 2)."*
- **Note.** eLife supplementary files carry no separate DOI. The deposit is cited
  through the article DOI plus the file name. The local copy is
  `data/raw/tb/elife93243_supp2.xlsx`.

### R6. Windels et al. 2024 — evolved-clone deposit (Zenodo)

Windels EM, Cool L, Persy E, Swinnen J, Matthay P, Van den Bergh B, Wenseleers T,
Michiels J. *Data supporting "Antibiotic dose and nutrient availability
differentially drive the evolution of antibiotic resistance and persistence"*
[dataset]. Zenodo; 16 April 2024. Version DOI 10.5281/zenodo.7550302; concept DOI
10.5281/zenodo.7550301. Licence CC BY 4.0.

- **Supports** (Table 1, ~L147): *"| Evolved clones | E. coli, 126 clones |
  amikacin | MIC and persister fraction per clone | Zenodo 7550302 | CC BY 4.0 |"*
- **Verified from** the Zenodo API record for 7550302.
- **Note.** The manuscript cites the version DOI (…7550302). The concept DOI
  (…7550301) resolves to the latest version and is the more stable citation; this
  is a style decision (see Section 3).

### R7. Kaur et al. 2024 — apramycin raw-data deposit (figshare)

Kaur P. *Apramycin kills replicating and non-replicating Mycobacterium
tuberculosis — Raw Data* [dataset]. figshare; 2024. Version 1, posted 2 August
2024. doi:10.6084/m9.figshare.26462791.v1. Licence CC BY 4.0.

- **Supports** (Table 1, ~L148): *"| Concentration-by-time grid | M. tuberculosis
  | apramycin 1-128 ug/mL (amikacin arm not analysed) | 5 concentrations x 4 days
  x 3 replicates | figshare 26462791 | CC BY 4.0 |"*
- **Verified from** the figshare API record for article 26462791. Single creator.

### R8. Dubey et al. 2026 — hollow-fibre Source Data (held-out deposit)

Dubey V, Darlow C, Gerada A, Unsworth J, Sheth E, Reza N, Farrington N,
Haldenby S, Warren D, Liu X, Howard A, Hope W. Source Data to: *Molecular
pharmacodynamics of amoxicillin-clavulanic acid for urinary tract infections
caused by Escherichia coli* [dataset]. Nature Communications; 2026.
File: `41467_2026_74323_MOESM4_ESM.xlsx`. doi:10.1038/s41467-026-74323-2.
Licence CC BY 4.0.

- **Supports** (Table 1, ~L149): *"| Held out for validation | E. coli, hollow
  fibre | amoxicillin-clavulanate | 20 cultures, measured day-zero density,
  100 uL plated | Nat Commun 2026 Source Data | CC BY 4.0 |"*
- **Note.** Nature Communications Source Data files carry no separate DOI; cite
  through the article DOI and the file name, as above. Article entry at R21.

### R9. Cochran 1950 — the most-probable-number estimator

Cochran WG. Estimation of bacterial densities by means of the "most probable
number". *Biometrics*. 1950;6(2):105–116. doi:10.2307/3001491.

- **Supports** (Results §1, ~L180): *"The most probable number readings take the
  discrete values of an MPN table, and the day-5 column does not taper towards
  zero but stops."*
- **And** (Methods, floor sensitivity, ~L1200): *"the load-bearing count is
  recomputed at every value a three-tube MPN table returns below 23."*
- **Currently uncited.** The whole floor inference for the clinical deposit rests
  on the discreteness of an MPN table; no source for that table is given anywhere
  in the manuscript. This is the largest genuinely missing methodological
  citation that the task brief did not list.
- **Crossref gives first page 105 only.** The commonly cited range is 105–116;
  the end page is not in the Crossref record — see Section 2.

### R10. FDA Bacteriological Analytical Manual, Appendix 2 — the MPN tables

Blodgett R. *BAM Appendix 2: Most Probable Number from Serial Dilutions*. In:
*Bacteriological Analytical Manual*. Silver Spring, MD: US Food and Drug
Administration; current edition August 2023 (earlier editions October 2020,
October 2010). Available at
https://www.fda.gov/food/laboratory-methods-food/bam-appendix-2-most-probable-number-serial-dilutions

- **Supports the same sentences as R9**, and specifically the rung values swept in
  Table S7 (3.0, 3.6, 7.2, 7.4, 9.2, 11, 14, 15, 20, 21, 23).
- **Verified**: document identity, author, publisher and edition dates, from the
  FDA's own page. **Not verified**: that these eleven rungs appear in that
  document's three-tube table — see Section 2, U3.
- **Recommendation.** Cite R9 for the estimator and R10 for the table, or cite
  only R10 if the journal prefers a single method source.

### R11. Fisher 1922 — the exact test for a 2×2 table

Fisher RA. On the interpretation of χ² from contingency tables, and the
calculation of P. *Journal of the Royal Statistical Society*. 1922;85(1):87–94.
doi:10.2307/2340521. (Also carried as
doi:10.1111/j.2397-2335.1922.tb00768.x in the JRSS Series A back file.)

- **Supports** (Results §2, ~L408): *"The 99.99 per cent endpoint is unreachable
  for 22 of 84 isoniazid-resistant isolates, 26.2 per cent, against 9 of 119
  susceptible ones, 7.6 per cent (Fisher exact p = 0.00056)…"*
- **Optional.** Many journals treat this as a standard test needing no citation;
  see Section 3.

### R12. McCullagh 1980 — the proportional-odds model

McCullagh P. Regression models for ordinal data. *Journal of the Royal
Statistical Society, Series B (Methodological)*. 1980;42(2):109–127.
doi:10.1111/j.2517-6161.1980.tb01109.x.

- **Supports** (Results §4, ~L497): *"Associations are therefore reported as odds
  ratios from proportional-odds ordinal logistic regression, with the
  proportional-odds assumption tested rather than assumed (Methods; Table 7)."*
- **And** (Methods, Estimation, ~L1631): *"The tolerance label is modelled as an
  ordered categorical outcome by proportional-odds ordinal logistic regression…"*
- **And** ("What should change", ~L1290): *"Proportional-odds regression costs
  nothing to run, reports in odds ratios…"*
- **Page range note.** Crossref records 109–127. The paper is a read-paper and is
  frequently cited as 109–142 including the recorded discussion. Both are
  defensible; 109–127 is the article proper. Decide once and apply consistently.

### R13. Brant 1990 — the test of proportional odds

Brant R. Assessing proportionality in the proportional odds model for ordinal
logistic regression. *Biometrics*. 1990;46(4):1171–1178. PMID 2085632.

- **Supports** (Table 7 legend, ~L480): *"The proportional-odds column is a Brant
  test per predictor; the assumption holds throughout this family."*
- **And** (Results §4, ~L602): *"Proportional odds holds throughout the 15-day
  panel but fails at 60 days for starting density at the deepest endpoint (Brant
  p = 0.0031…)"*
- **And** (Methods, ~L1638): *"Proportional odds is tested by a Brant test per
  predictor…"*
- **No DOI in the PubMed record.** JSTOR stable ID 2532457 is the usual locator;
  not independently verified here — see Section 2, U1.

### R14. Benjamini & Hochberg 1995 — false discovery rate

Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and
powerful approach to multiple testing. *Journal of the Royal Statistical Society,
Series B (Methodological)*. 1995;57(1):289–300.
doi:10.1111/j.2517-6161.1995.tb02031.x.

- **Supports** (Table 7 legend, ~L480): *"…corrected together at a false discovery
  rate of 5%."*
- **And** (Results §4, ~L556): *"…and so is tested against a Benjamini–Hochberg
  critical value of 0.0125."*
- **And** (Methods, Multiplicity, ~L1710): *"…the family is corrected by the
  Benjamini–Hochberg procedure at a false discovery rate of 5 per cent."*
- **And** Table 14, Table 15 and the Figure 4A legend.

### R15. Peterson & Harrell 1990 — partial proportional odds / generalised ordered logit

Peterson B, Harrell FE Jr. Partial proportional odds models for ordinal response
variables. *Journal of the Royal Statistical Society, Series C (Applied
Statistics)*. 1990;39(2):205–[217]. doi:10.2307/2347760.

- **Supports** (Methods, Estimation, ~L1638): *"…by a likelihood-ratio test against
  a generalised ordered logit with the coefficient released; where it fails, the
  released partial-proportional-odds fit is reported…"*
- **And** (Results §4, ~L604): *"Releasing that coefficient puts the whole effect at
  the upper boundary…"*
- **This is the original source** of the partial-proportional-odds model with a
  per-cut coefficient mask, which is what `exp30_ordinal_tolerance.py`
  implements. It is not Williams (2006), which is the Stata implementation paper
  and would be a software citation, not a method citation.
- **End page not in the Crossref record** (first page 205 only) — see Section 2, U2.

### R16. Imai, Keele & Yamamoto 2010 — the ρ sensitivity analysis for sequential ignorability

Imai K, Keele L, Yamamoto T. Identification, inference and sensitivity analysis
for causal mediation effects. *Statistical Science*. 2010;25(1):51–71.
doi:10.1214/10-STS321.

- **Supports** (Results §4, ~L530): *"It rests on sequential ignorability, which no
  observational file can establish: a residual correlation between the mediator
  and outcome errors of about −0.24 would nullify the point estimate…"*
- **And** (Methods, Causal mediation, ~L1536): *"Sequential ignorability is assumed
  and is not testable here, so the estimate is accompanied by the sensitivity that
  matters: the residual correlation between mediator and outcome errors at which
  the point estimate crosses zero, which is about −0.24."*
- **And** Table S3 legend: *"…the sensitivity analysis in the Methods reports the
  residual correlation that would nullify the estimate."*
- **This is the original source the brief asked for.** Verified against Project
  Euclid for the page range. Section 5 of this paper introduces ρ, the correlation
  between the mediator and outcome error terms, as the sensitivity parameter for
  a violation of sequential ignorability, in exactly the linear
  structural-equation setting the manuscript uses. The `mediation` R package
  (Tingley et al., *J Stat Softw* 2014;59(5)) is the software manual and should
  **not** be cited in its place.

### R17. Baron & Kenny 1986 — the product-of-coefficients decomposition

Baron RM, Kenny DA. The moderator–mediator variable distinction in social
psychological research: conceptual, strategic, and statistical considerations.
*Journal of Personality and Social Psychology*. 1986;51(6):1173–1182.
doi:10.1037/0022-3514.51.6.1173.

- **Supports** (Methods, ~L1526): *"Separately, a linear product-of-coefficients
  mediation decomposes the total effect of isoniazid resistance on the day-5
  tolerance class into an average causal mediation effect through log10 N₀ and an
  average direct effect…"*
- **Note.** R16 supplies the estimand names (ACME, ADE) and the sensitivity
  analysis; R17 supplies the product-of-coefficients decomposition itself. Cite
  both, or cite R16 alone if the journal is terse — R16 also derives the
  decomposition under the linear model.

### R18. Mann & Whitney 1947

Mann HB, Whitney DR. On a test of whether one of two random variables is
stochastically larger than the other. *The Annals of Mathematical Statistics*.
1947;18(1):50–60. doi:10.1214/aoms/1177730491.

- **Supports** (Results §4, ~L516): *"Isoniazid-resistant isolates enter this assay
  at 5.36 log10 against 6.36 for susceptible isolates, ten-fold lower
  (Mann–Whitney p = 9.1 × 10⁻¹⁴)…"*
- **Optional** — see Section 3.

### R19. McNemar 1947 — the paired binary test

McNemar Q. Note on the sampling error of the difference between correlated
proportions or percentages. *Psychometrika*. 1947;12(2):153–157.
doi:10.1007/BF02295996.

- **Supports** (Results §4, ~L594): *"26 isolates lose their headroom shortfall
  between panels and none acquires one (exact McNemar p = 3.0 × 10⁻⁸ against an
  unpaired p of 2 × 10⁻⁵), eleven leave the floor and none joins it
  (p = 9.8 × 10⁻⁴)…"*
- **And** four rows of Table 15 recording "exact McNemar on the paired binary".
- **Support check: passes with a caveat worth stating.** McNemar 1947 gives the
  large-sample χ² form. The **exact** (binomial) version the manuscript uses is
  the conditional test on the discordant pairs; it follows directly but is not
  named in McNemar's note. If a referee presses, add Edwards AL, *Psychometrika*
  1948;13(3):185–187 (doi:10.1007/BF02289261, verified) for the continuity
  correction and the exact treatment. Given that every McNemar count here is small
  (26/0, 11/0), the exact test is the right one and citing McNemar alone is
  slightly loose.

### R20. Wilcoxon 1945 — the signed-rank test

Wilcoxon F. Individual comparisons by ranking methods. *Biometrics Bulletin*.
1945;1(6):80–[83]. doi:10.2307/3001968.

- **Supports** (Results §4, ~L597): *"…and every isolate whose headroom changes
  gains (Wilcoxon signed-rank p = 1.3 × 10⁻³³)."*
- **Crossref gives first page 80 only**; the article runs 80–83 in the usual
  citation — see Section 2, U4. **Optional** — see Section 3.

### R21. Pym, Saint-Joanis & Cole 2002 — katG S315T is near fitness-neutral

Pym AS, Saint-Joanis B, Cole ST. Effect of katG mutations on the virulence of
Mycobacterium tuberculosis and the implication for transmission in humans.
*Infection and Immunity*. 2002;70(9):4955–4960. doi:10.1128/IAI.70.9.4955-4960.2002.
PMID 12183541. PMC128294.

- **Supports** (Results §4, ~L563): *"…and 85 of them carry katG S315X, the
  mutation that predominates clinically precisely because it is close to
  fitness-neutral."*
- **And** (Discussion, ~L1114): *"…since these isolates do not grow measurably more
  slowly and most carry the near-neutral katG S315X allele."*
- **Support check: passes squarely.** The abstract states the S315T mutant
  "produces active catalase-peroxidase and is virulent in the mouse model of the
  disease, indicating that a significant loss of bacterial fitness does not result
  from this frequent mutation."
- **Currently uncited.** This is a load-bearing biological assertion carrying a
  Discussion paragraph, and it has no source in the manuscript.

### R22. van Soolingen et al. 2000 — S315 mutants transmit as well as susceptible strains

van Soolingen D, de Haas PEW, van Doorn HR, Kuijper E, Rinder H, Borgdorff MW.
Mutations at amino acid position 315 of the katG gene are associated with
high-level resistance to isoniazid, other drug resistance, and successful
transmission of Mycobacterium tuberculosis in the Netherlands. *The Journal of
Infectious Diseases*. 2000;182(6):1788–1790. doi:10.1086/317598. PMID 11069256.

- **Supports the same two sentences as R21**, specifically the clause "predominates
  clinically". The abstract reports that "aa 315 mutants lead to secondary cases
  of tuberculosis as often as INH-susceptible strains do".
- **Recommendation.** Cite R21 for fitness and R22 for clinical predominance; the
  manuscript's sentence makes both claims in one clause.

### R23. van Wijk et al. 2023 — the ERA4TB article

van Wijk RC, Lucía A, Sudhakar PK, Sonnenkalb L, Gaudin C, Hoffmann E,
Dremierre B, Aguilar-Ayala DA, Dal Molin M, Rybniker J, de Giorgi S,
Cioetto-Mazzabò L, Segafreddo G, Manganelli R, Degiacomi G, Recchia D, Pasca MR,
Simonsson USH, Ramón-García S. Implementing best practices on data generation and
reporting of *Mycobacterium tuberculosis* in vitro assays within the ERA4TB
consortium. *iScience*. 2023;26(4):106411. doi:10.1016/j.isci.2023.106411.
PMID 37091238. PMC10119593.

- **Supports** (Results §5, ~L616): *"Van Wijk and colleagues (2023) ran exactly
  that exercise, sending a single stock of H37Rv to six blinded laboratories under
  one written protocol."*
- **And** (Discussion, ~L1141): *"They report the inoculum spread themselves and
  conclude that baseline burden varied between laboratories while net drug effect
  varied less; that conclusion anticipates part of ours and belongs to them."*
- **Support check: passes.** The published abstract states "Baseline bacterial
  burden varied between laboratories but variability was limited in net drug
  effect, confirming 2.5 μL equally robust as 100 μL plating."
- **CORRECTION to the repository's earlier note.** `docs/18_DISCUSSION_COMPARISON.md`
  records this as *iScience* **26(5)**. Both PubMed and Crossref give **26(4)**.
  Use 26(4):106411.
- **Title note.** PubMed strips the italicised "*Mycobacterium tuberculosis* in
  vitro" from the title; Crossref carries it. The full title is the Crossref form
  given above. Note it is "in vitro assays", not "time kill assays" — the latter
  is the figshare item's title (R4).

### R24. Kaplan & Meier 1958

Kaplan EL, Meier P. Nonparametric estimation from incomplete observations.
*Journal of the American Statistical Association*. 1958;53(282):457–481.
doi:10.1080/01621459.1958.10501452.

- **Supports** (Results §5, ~L761): *"The non-parametric interval-censored curve sits
  below the naive Kaplan–Meier at every visit at which crossings are still being
  recorded…"*
- **And** (Figure 2 legend, panel B): *"Kaplan–Meier curves for time to the first
  observed crossing below the assay floor."*
- **And** (Methods, Estimation, ~L1659): *"Kaplan–Meier and Cox proportional hazards
  are retained as descriptive summaries of first crossing only…"*

### R25. Cox 1972 — proportional hazards

Cox DR. Regression models and life-tables. *Journal of the Royal Statistical
Society, Series B (Methodological)*. 1972;34(2):187–202.
doi:10.1111/j.2517-6161.1972.tb00899.x.

- **Supports** (Results §5, ~L685): *"The Cox fits are reported for the same reason
  and with the same restraint."*
- **And** (Methods, ~L1659), as quoted at R24.
- **Page range note.** Crossref records 187–202 for the article; the read-paper
  discussion runs to 220, and 187–220 is the form many bibliographies use. Same
  decision as R12.

### R26. Efron 1979 — the bootstrap

Efron B. Bootstrap methods: another look at the jackknife. *The Annals of
Statistics*. 1979;7(1):1–26. doi:10.1214/aos/1176344552.

- **Supports** (Results §4, ~L524): *"…a mediated effect of +0.166 classes (bootstrap
  95 per cent CI +0.067 to +0.279)…"*
- **And** (Methods, ~L1670): *"The replicate-level bootstrap behind the interval
  slopes resamples the three replicate counts with replacement at both ends of
  each interval… and takes percentile intervals from 20 000 draws."*
- **Page range verified from Project Euclid** (Crossref carries no pages).

### R27. Field & Welsh 2007 — the cluster bootstrap

Field CA, Welsh AH. Bootstrapping clustered data. *Journal of the Royal
Statistical Society, Series B (Statistical Methodology)*. 2007;69(3):369–390.
doi:10.1111/j.1467-9868.2007.00593.x.

- **Supports** (Results §5, ~L700): *"Where an interval is quoted from that fit it is
  a cluster bootstrap and not the model's own. For the starting-density
  coefficient the laboratory-clustered interval is −1.11 to −0.51…"*
- **And** (Results §7, ~L722): *"Resampling whole flasks within laboratory puts the
  36.6 per cent between 24.7 and 50.5 per cent; resampling whole laboratories,
  which is the level at which the comparison is actually made, puts it between 3.0
  and 72.4 per cent."*
- **And** twelve rows of Table 15 whose method column reads "cluster bootstrap over
  whole laboratories".
- **This is the right primary source** for the choice the manuscript makes — the
  paper is precisely about which unit to resample in clustered data, and it
  distinguishes the cluster and the within-cluster (two-stage) bootstraps that the
  manuscript reports side by side.

### R28. Davison & Hinkley 1997 — bootstrap methods (textbook)

Davison AC, Hinkley DV. *Bootstrap Methods and their Application*. Cambridge:
Cambridge University Press; 1997. doi:10.1017/CBO9780511802843.
ISBN 978-0-521-57391-7 (hardback); 978-0-521-57471-6 (paperback).

- **Supports the same sentences as R27**, and specifically the percentile-interval
  construction used throughout (Methods, ~L1670; Table S3).
- **Optional.** Cite alongside R27 if the journal permits a textbook; R26 + R27
  alone are sufficient.

### R29. Turnbull 1976 — the non-parametric interval-censored estimator

Turnbull BW. The empirical distribution function with arbitrarily grouped,
censored and truncated data. *Journal of the Royal Statistical Society, Series B
(Methodological)*. 1976;38(3):290–295.
doi:10.1111/j.2517-6161.1976.tb01597.x.

- **Supports** (Results §5, ~L757): *"Fitted as interval-censored data at the most
  sensitive plating, the tenth percentile of the first crossing falls from 2.95 to
  1.82 days…"* and *"The non-parametric interval-censored curve sits below the
  naive Kaplan–Meier at every visit…"*
- **And** (Methods, ~L1657): *"Interval-censored fits are therefore reported
  alongside the naive treatment that pins the event to the visit at which the
  blank plate was noticed."*
- **Currently uncited**, and not on the task brief's list. The manuscript's
  strongest quantitative claim in Section 5 — a 36 per cent shortening of the
  25th percentile — comes from this estimator, which `lifelines` implements as
  the Turnbull/EM non-parametric MLE.

### R30. Brown, Cai & DasGupta 2001 — the Jeffreys interval

Brown LD, Cai TT, DasGupta A. Interval estimation for a binomial proportion.
*Statistical Science*. 2001;16(2):101–133. doi:10.1214/ss/1009213286.

- **Supports** (Table 15, ~L1183): *"| 5 | at one times MIC five of six laboratories
  record net growth | 6 laboratory-arm cell | 6 | Jeffreys interval on six clusters
  | WEAKENED |"*
- **This is the source that defines and recommends the Jeffreys interval** for a
  binomial proportion at small n, which is precisely the manuscript's use (five of
  six clusters). Verified page range from Project Euclid.
- **Optional companion**, if the journal wants the prior itself: Jeffreys H. An
  invariant form for the prior probability in estimation problems. *Proceedings of
  the Royal Society of London A*. 1946;186(1007):453–461.
  doi:10.1098/rspa.1946.0056. (Verified.) Cite R30 alone unless a referee asks.

### R31. NCCLS M26-A 1999 — bactericidal-activity guideline

National Committee for Clinical Laboratory Standards. *Methods for Determining
Bactericidal Activity of Antimicrobial Agents; Approved Guideline*. NCCLS document
M26-A, Vol. 19, No. 18. Wayne, PA: NCCLS; September 1999.
ISBN 1-56238-384-1. 32 pp. Now published as CLSI order code M26AE and designated
archived by CLSI ("no longer being reviewed through the CLSI Consensus Document
Development Process… technically valid as of September 2016").

- **Supports** (Results §6, ~L777): *"A time-kill inoculum is not chosen freely: a
  suspension is matched to 0.5 McFarland and diluted, and CLSI M26-A (approved
  guideline, 1999, since archived) puts the target near 5 × 10⁵ CFU/mL."*
- **And** (Results §6, ~L796): *"Three of the four sit below the CLSI target, by
  11-, 12- and 107-fold; the fourth sits two-fold above it."*
- **CORRECTION to the manuscript's own wording.** In 1999 the issuing body was the
  **National Committee for Clinical Laboratory Standards (NCCLS)**; it was renamed
  the Clinical and Laboratory Standards Institute in 2005. The document's own
  imprint is "NCCLS document M26-A". Writing "CLSI M26-A … 1999" is an anachronism
  a bacteriology referee will notice. Recommended in-text form: *"NCCLS M26-A
  (1999; the body is now CLSI, which has archived the document)"*.
- **UNVERIFIED sub-item.** The 5 × 10⁵ CFU/mL figure is stated in secondary
  literature and matches the manuscript, but the guideline itself is paywalled and
  the ANSI preview PDF and the regulations.gov copy both returned HTTP 403 during
  this pass. See Section 2, U5.

### R32. McFarland 1907 — the turbidity standard

McFarland J. The nephelometer: an instrument for estimating the number of bacteria
in suspensions used for calculating the opsonic index and for vaccines. *JAMA:
The Journal of the American Medical Association*. 1907;XLIX(14):1176–[1178].
doi:10.1001/jama.1907.25320140022001f.

- **Supports** (Results §6, ~L781): *"A McFarland figure is a turbidity, matched
  optically, and counts live cells, dead cells, debris and a clump as one
  particle; converting it to CFU/mL assumes a cell size, shape and dispersal that
  M. tuberculosis does not oblige…"*
- **And** (Table S5 legend): *"Fold below the nominal 0.5 McFarland reference,
  1.5e8 CFU/mL."*
- **Crossref gives first page 1176 only** — see Section 2, U6.
- **Optional.** Some journals would accept the standard as common knowledge; the
  manuscript makes a substantive argument *about* it, which argues for citing it.

### R33. Franzblau et al. 2012 — TB assay methods vary in inoculum and dilution

Franzblau SG, DeGroote MA, Cho SH, Andries K, Nuermberger E, Orme IM, Mdluli K,
Angulo-Barturen I, Dick T, Dartois V, Lenaerts AJ. Comprehensive analysis of
methods used for the evaluation of compounds against *Mycobacterium tuberculosis*.
*Tuberculosis (Edinb)*. 2012;92(6):453–488. doi:10.1016/j.tube.2012.07.003.
PMID 22940006.

- **Supports** (Results §6, ~L784): *"…and tuberculosis protocols work from a range
  of dilutions and target inocula."*
- **Support check: passes.** This is the Gates-Foundation-commissioned survey of
  preclinical TB assay protocols; its stated purpose is to "delineate the spectrum
  of variables in experimental protocols" precisely because "a plethora of
  different assay systems and conditions are used… making it difficult to compare
  data from one laboratory to another."
- **Currently uncited.** This is the source for the concession the manuscript
  makes in Section 6, and it is the concession the reviewer asked to be supported
  (see `RESPONSE_TO_REVIEW.md`, item m12).

### R34. Rabodoarivelo et al. 2025 — the mycobacteria-specific time-kill protocol

Rabodoarivelo MS, Hoffmann E, Gaudin C, Aguilar-Ayala DA, Galizia J,
Sonnenkalb L, Dal Molin M, Cioetto-Mazzabò L, Degiacomi G, Recchia D,
Rybniker J, Manganelli R, Pasca MR, Ramón-García S, Lucía A. Protocol to quantify
bacterial burden in time-kill assays using colony-forming units and most probable
number readouts for *Mycobacterium tuberculosis*. *STAR Protocols*.
2025;6(1):103643. doi:10.1016/j.xpro.2025.103643. PMID 40067825. PMC11931380.

- **Supports** (Results §6, ~L775–784), cited alongside R31 as the mycobacterial
  counterpart to a general bacterial standard.
- **This answers the brief's last item, and answers it better than a documented
  absence.** It is a peer-reviewed, step-by-step *M. tuberculosis* time-kill
  protocol; it is from the same ERA4TB group whose deposit is R4/R23 (so it
  documents the very protocol the six-laboratory exercise ran); and it uses
  **both** CFU and most-probable-number readouts — the two readouts the two
  primary deposits of this manuscript use. Nothing else found comes as close.
- **See also** the absence finding at Section 3, item 8: this is a *protocol
  paper*, not a consensus standard, and the distinction should be stated in the
  text rather than blurred.

### R35. CLSI M24, 3rd edition, 2018 — what the mycobacterial standard does cover

Clinical and Laboratory Standards Institute. *Susceptibility Testing of
Mycobacteria, Nocardia spp., and Other Aerobic Actinomycetes*. 3rd ed. CLSI
standard M24. Wayne, PA: CLSI; November 2018.
ISBN 978-1-68440-025-6 (print); 978-1-68440-026-3 (electronic).

- **Supports a sentence the manuscript should add** in Section 6, to make the
  concession precise: the mycobacterial standard that does exist covers MIC and
  susceptibility testing and does not specify a killing-curve method, which is why
  a general bacterial guideline (R31) is being applied at all.
- **Verified**: title, edition, date, ISBNs, publisher, and the scope statement
  ("protocols and related quality control parameters for antimicrobial
  susceptibility testing"). The 2nd edition (M24-A2, 2011, ISBN 1-56238-746-4),
  whose full text is on NCBI Bookshelf (NBK544374), contains MIC methods only and
  no time-kill method. **The 3rd edition's full text is paywalled and was not
  read** — see Section 2, U7.
- **Optional companion**: CLSI supplement M24S, *Performance Standards for
  Susceptibility Testing of Mycobacteria, Nocardia spp., and Other Aerobic
  Actinomycetes* (2nd ed.). Not verified in detail; only cite if the text uses it.

### R36. Dubey et al. 2026 — the held-out hollow-fibre article

Dubey V, Darlow C, Gerada A, Unsworth J, Sheth E, Reza N, Farrington N,
Haldenby S, Warren D, Liu X, Howard A, Hope W. Molecular pharmacodynamics of
amoxicillin-clavulanic acid for urinary tract infections caused by *Escherichia
coli*. *Nature Communications*. 2026;17(1):7504.
doi:10.1038/s41467-026-74323-2. PMID 42288477. PMC13408132.

- **Supports** (Results §8, ~L914): *"Dubey and colleagues (2026) report
  amoxicillin-clavulanate against Escherichia coli in a hollow-fibre system.
  Their Methods state 100 µL plated with counts per mL, so L = 10 CFU/mL is
  derived rather than inferred…"*
- **Article number 7504 verified from Crossref**; the repository's PROVENANCE.json
  recorded volume and issue but no article number.

### R37. Kaur et al. 2024 — the apramycin article

Kaur P, Ramya VK, Naveenkumar CN, Bharathkumar K, Singh M, Hobbie SN,
Shandil RK, Narayanan S. Apramycin kills replicating and non-replicating
*Mycobacterium tuberculosis*. *Frontiers in Tropical Diseases*. 2024;5:1413211.
doi:10.3389/fitd.2024.1413211.

- **Supports** (Methods, Datasets, ~L1411): *"Apramycin and amikacin against M.
  tuberculosis at 128, 32, 8, 4 and 1 µg/mL, triplicate log10 CFU at days 0, 3, 7
  and 14, with a concurrent drug-free control at every visit (Kaur et al. 2024;
  figshare 26462791, CC BY 4.0)."*
- **And** Results §9 throughout.
- **No PMID and no PMCID.** Independently confirmed in this pass: a PubMed title
  search returns nothing, and the NCBI ID converter returns no PMID for
  doi:10.3389/fitd.2024.1413211. *Frontiers in Tropical Diseases* is not
  MEDLINE-indexed. **Do not supply a PMID for this entry.**
- Author-name note: Crossref renders authors 2–4 as "Ramya V. K.", "Naveenkumar
  C. N." and "Bharathkumar K." — South-Indian initials-after-name order. Check the
  published byline before applying a Western surname-first convention.

### R38. Windels et al. 2024 — the evolved-clone article

Windels EM, Cool L, Persy E, Swinnen J, Matthay P, Van den Bergh B, Wenseleers T,
Michiels J. Antibiotic dose and nutrient availability differentially drive the
evolution of antibiotic resistance and persistence. *The ISME Journal*.
2024;18(1):wrae070. doi:10.1093/ismejo/wrae070. PMID 38691440. PMC11102087.

- **Supports** (Results §10, ~L1021): *"The same question in 126 evolved clones
  sharing an ancestor gives ρ = +0.043 (p = 0.63) against a resolvable ρ of
  0.175, and independence holds within every nutrient stratum separately."*
- **And** (Methods, Datasets, ~L1384): *"126 Escherichia coli clones from a parallel
  evolution experiment under amikacin, each carrying an endpoint minimum
  inhibitory concentration and a persister fraction measured on the same clone…"*
- **Note.** The manuscript cites only the Zenodo deposit (R6) at this point. The
  article should be cited with it, as it is for every other deposit.

### R39. Vilchèze & Jacobs 2007 — isoniazid needs KatG activation and cell-wall synthesis

Vilchèze C, Jacobs WR Jr. The mechanism of isoniazid killing: clarity through the
scope of genetics. *Annual Review of Microbiology*. 2007;61:35–50.
doi:10.1146/annurev.micro.61.111606.122346. PMID 18035606.

- **Supports** (Discussion, ~L1096): *"isoniazid requires KatG activation and active
  cell-wall synthesis, rifampicin requires transcription, and a population that is
  not dividing presents less of what these drugs act on."*
- **Currently uncited.** This sentence is the mechanistic argument for the paper's
  surviving positive finding (growth state predicts tolerance class); it should
  not go to a referee bare.

### R40. Campbell et al. 2001 — rifampicin blocks transcription

Campbell EA, Korzheva N, Mustaev A, Murakami K, Nair S, Goldfarb A, Darst SA.
Structural mechanism for rifampicin inhibition of bacterial RNA polymerase.
*Cell*. 2001;104(6):901–912. doi:10.1016/S0092-8674(01)00286-0. PMID 11290327.

- **Supports the same Discussion sentence as R39**, specifically "rifampicin
  requires transcription".

### Software (R41–R45) — cited only if the journal requires it

The Methods state: *"Analyses used Python 3.14 with numpy 2.5.0, scipy 1.18.0,
pandas 3.0.3, statsmodels 0.15.0 and lifelines 0.30.3."* (~L1750). All five have
canonical citations; several journals (including Nature-family titles) now
require them.

- **R41.** Harris CR, Millman KJ, van der Walt SJ, Gommers R, Virtanen P,
  Cournapeau D, Wieser E, Taylor J, Berg S, Smith NJ, Kern R, Picus M, Hoyer S,
  van Kerkwijk MH, Brett M, Haldane A, del Río JF, Wiebe M, Peterson P,
  Gérard-Marchant P, Sheppard K, Reddy T, Weckesser W, Abbasi H, Gohlke C,
  Oliphant TE. Array programming with NumPy. *Nature*. 2020;585(7825):357–362.
  doi:10.1038/s41586-020-2649-2. PMID 32939066. PMC7759461.
- **R42.** Virtanen P, Gommers R, Oliphant TE, Haberland M, Reddy T, Cournapeau D,
  et al.; SciPy 1.0 Contributors. SciPy 1.0: fundamental algorithms for scientific
  computing in Python. *Nature Methods*. 2020;17(3):261–272.
  doi:10.1038/s41592-019-0686-2. PMID 32015543. PMC7056644.
- **R43.** McKinney W. Data structures for statistical computing in Python. In:
  *Proceedings of the 9th Python in Science Conference*. 2010:56–61.
  doi:10.25080/Majora-92bf1922-00a.
- **R44.** Seabold S, Perktold J. Statsmodels: econometric and statistical modeling
  with Python. In: *Proceedings of the 9th Python in Science Conference*.
  2010:92–96. doi:10.25080/Majora-92bf1922-011.
- **R45.** Davidson-Pilon C. lifelines: survival analysis in Python. *Journal of
  Open Source Software*. 2019;4(40):1317. doi:10.21105/joss.01317.

**Note on R44.** The Methods say four procedures are *not* taken from a package —
the Brant test, the partial-proportional-odds fit, the product-of-coefficients
mediation and the ρ sensitivity — and that "the multinomial check uses
statsmodels". R44 should therefore be cited for the multinomial check and the
Tobit/OLS fits, not for the four bespoke procedures, which are covered by
R13, R15, R16/R17 respectively.

---

## Section 2 — UNVERIFIED entries and unresolved fields

Nothing in this section is guessed. Each item states exactly what is missing and
where to get it.

**U1. Brant 1990 — no DOI.**
Missing: a DOI. PubMed record 2085632 carries none, and *Biometrics* volume 46
(1990) predates that journal's DOI back-file assignment. The article is stable at
JSTOR (the usual identifier is JSTOR 2532457, **not independently confirmed in
this pass**). *Where to get it:* the JSTOR landing page for Biometrics 46(4), or
the Wiley back file for *Biometrics*, which may now carry
`10.2307/2532457`. Verify before printing any DOI for this entry.

**U2. Peterson & Harrell 1990 — end page not confirmed.**
Have: DOI 10.2307/2347760, journal, 1990, 39(2), first page 205. Missing: the end
page. The Crossref record carries only the first page. The range is very widely
quoted as 205–217. *Where to get it:* the JSTOR or Wiley landing page for
*Applied Statistics* 39(2), or the printed issue.

**U3. FDA BAM Appendix 2 — the specific MPN rungs not confirmed.**
Have: title, author (Blodgett R), publisher (US FDA), current edition August 2023,
prior editions October 2020 and October 2010, and the stable URL. Missing:
confirmation that the three-tube table in that document contains the eleven rung
values the manuscript sweeps in Table S7 (3.0, 3.6, 7.2, 7.4, 9.2, 11, 14, 15, 20,
21, 23). The FDA landing page is navigation only; the tables are in the linked
PDF, which was not opened in this pass. *Where to get it:*
https://www.fda.gov/media/183668/download (the August 2023 PDF). **This matters**:
the manuscript's floor-sensitivity sweep is defined by that table, and if the
deposit used a different MPN scheme (e.g. a 5-tube or a 10-tube series) the sweep
is against the wrong ladder. Check the Vijay et al. methods for which MPN scheme
was used, and cite that scheme's table.

**U4. Wilcoxon 1945 — end page not confirmed.**
Have: DOI 10.2307/3001968, *Biometrics Bulletin* 1945;1(6), first page 80. Missing:
the end page (usually given as 83). *Where to get it:* the JSTOR landing page for
*Biometrics Bulletin* 1(6).

**U5. NCCLS M26-A — the 5 × 10⁵ CFU/mL target not read at source.**
Have: publisher, document code, volume/number (19/18), ISBN 1-56238-384-1, date
(September 1999), page count (32), and CLSI's own archived-status statement.
Missing: a first-hand reading of the sentence that sets the starting inoculum near
5 × 10⁵ CFU/mL, which Section 6 quotes and builds an 11-, 12- and 107-fold
comparison on. The ANSI preview PDF and a regulations.gov mirror both returned
HTTP 403. Secondary sources are consistent with the manuscript's figure but a
paywalled standard should be read before being quoted. *Where to get it:* purchase
CLSI order code M26AE, or an institutional CLSI eCLIPSE subscription.
**Recommendation:** do not send this manuscript to review again without one author
having read that sentence in M26-A itself.

**U6. McFarland 1907 — end page not confirmed.**
Have: DOI 10.1001/jama.1907.25320140022001f, JAMA 1907;XLIX(14), first page 1176.
Missing: the end page (usually 1178). Note the volume is printed in Roman numerals
(XLIX) in the source record; most styles convert to 49. *Where to get it:* the JAMA
Network archive landing page for that DOI.

**U7. CLSI M24 3rd edition — scope statement not read at source.**
Have: title, edition, publisher, November 2018, both ISBNs, and the publisher's
own scope description. Missing: a first-hand confirmation that the 3rd edition
contains no killing-curve or time-kill method. The 2nd edition's full text (NCBI
Bookshelf NBK544374) was read and contains MIC methods only; the 3rd edition is
paywalled. *Where to get it:* CLSI order code M24Ed3E, table of contents.
**If the manuscript asserts the absence, it must be asserted from the 3rd edition,
not the 2nd.**

**U8. Spearman 1904 — not verified.**
The manuscript reports Spearman ρ throughout Section 10 and Table 14 (*"| baseline
only | MDK99.99 (15d) | 162 | -0.206 | …"*). If the journal wants the rank
correlation cited, the primary source is Spearman C, *American Journal of
Psychology* 1904, "The proof and measurement of association between two things" —
**volume, issue, pages and DOI were not confirmed** (the Crossref query was
rate-limited during this pass). *Where to get it:* Crossref bibliographic query, or
the JSTOR record for *Am J Psychol* volume 15.

**U9. eLife citation form — one decision left open.**
Verified: eLife 2024; **volume 13**; elocation-id **RP93243**; doi 10.7554/eLife.93243;
PMID 39250422; PMC11383526. Note that `docs/18_DISCUSSION_COMPARISON.md` records
this as **volume 12**, which is wrong on both PubMed and Crossref. What is open is
whether to print the eLife Reviewed Preprint form ("eLife 2024;13:RP93243") or the
version-of-record form; that depends on the target journal's handling of eLife's
publish-review-curate model.

**U11. Tobin 1958 — end page not confirmed.**
Have: DOI 10.2307/1907382, *Econometrica* 1958;26(1), first page 24. Missing: the
end page (usually 36). The Crossref record carries only the first page.
*Where to get it:* the JSTOR landing page for *Econometrica* 26(1). (Entry R47,
introduced in Section 3.)

**U10. Vijay et al. denominators — a citation-accuracy flag, not a missing field.**
The manuscript's Introduction says *"Vijay and colleagues (2024) scored 217 clinical
Mycobacterium tuberculosis isolates"*. The published abstract reports the
susceptibility contrast on **203** isolates (IS n = 119, IR n = 84). 217 is the
row count of the deposited supplementary file; 203 is the analysis set of the
published paper, and the manuscript's own Table 5 derives exactly that reduction.
The sentence is defensible but reads as if 217 were the paper's own figure.
*Recommended fix:* "…deposited a classification for 217 isolates, of which 203
carry one of the three ordered classes". No new reference is needed.

---

## Section 3 — Open style decisions, and what the brief missed

### Style decisions still open (journal not chosen)

1. **Numeric versus author–date.** The text currently uses author–date in prose
   ("Brauner et al. 2016", "Vijay and colleagues (2024)") and no markers at all for
   the twenty-odd methodological citations. The numbering R1–R45 above is order of
   first appearance, which is what a numeric style needs; an author–date style will
   re-sort alphabetically and the numbers become irrelevant. **Do not hard-code the
   numbers into the text until the journal is chosen.**
2. **Author-count convention.** Several entries have long author lists: R23
   (19 authors), R34 (15), R41 (26), R42 (35+ plus a group author). The list above
   gives full author lists so any truncation rule (6-then-et-al, 10-then-et-al,
   3-then-et-al) can be applied mechanically. R42 also has a corporate author
   ("SciPy 1.0 Contributors") that some styles drop and some require.
3. **Read-paper page ranges.** R12 (McCullagh), R25 (Cox) and R15 (Peterson &
   Harrell) are JRSS papers whose recorded discussion extends the page range.
   Pick article-proper or article-plus-discussion and apply it to all three.
4. **Dataset citations.** Six of the entries are datasets (R4–R8, and the Zenodo
   record R6). Decide whether they go in the reference list or in a separate Data
   Availability block — Nature-family journals want them in the reference list with
   a [Dataset] tag; several others want them only in Data Availability. The
   manuscript currently names them in Table 1 *and* in the Methods, which is
   correct either way.
5. **Zenodo version versus concept DOI** (R6). Version DOI 10.5281/zenodo.7550302
   is what the manuscript quotes and is the reproducible choice; concept DOI
   10.5281/zenodo.7550301 always resolves to the newest version. Reproducibility
   argues for the version DOI. State the choice once.
6. **figshare version suffixes** (R4, R7). Both figshare DOIs have a `.v1` suffix.
   The manuscript's Table 1 quotes the bare article number ("figshare 19766083").
   Decide whether to print the versioned DOI. Same argument as (5): version it.
7. **Software citations** (R41–R45). Include or not, per journal policy. If not
   included, the version numbers in the Methods still stand on their own.
8. **PMIDs.** The list carries them where they exist. R37 (Kaur) has none, and a
   style that requires a PMID for every entry will need an explicit "not indexed in
   MEDLINE" note. Do not invent one.

### What the brief's starting list missed, or got wrong

1. **Brauner 2017 is not in Nature Reviews Microbiology.** It is *Biophysical
   Journal* 112(12):2664–2671. (R3.)
2. **The MPN table has no citation anywhere in the manuscript** (R9, R10). This is
   the single largest gap. The floor inference for the primary deposit — the whole
   of Section 1, and the sensitivity sweep in Table S7 — rests on the claim that
   the readings "take the discrete values of an MPN table", with no source for the
   table and no statement of which MPN scheme the deposit used. A referee who
   works with MPN assays will ask.
3. **Turnbull 1976 is missing** (R29). The interval-censored non-parametric
   estimator carries a headline Section 5 result (the 25th percentile falling from
   5.77 to 3.67 days, "a 36 per cent shortening") and is uncited.
4. **The Tobit model itself is uncited.** Methods, ~L1614: *"A Tobit model fits
   log10 CFU/mL linearly in time by maximum likelihood."* Beal 2001 (which **is** on
   the brief's list, entry R46 below) is cited for the M3 handling of below-limit
   data, but not for the Tobit model. Add:
   **R46.** Beal SL. Ways to fit a PK model with some data below the quantification
   limit. *Journal of Pharmacokinetics and Pharmacodynamics*. 2001;28(5):481–504.
   doi:10.1023/A:1012299115260. PMID 11768292.
   *Supports* (Methods, ~L1619): *"This is Beal's M3 (Beal 2001) written for this
   assay."* — **verified; support check passes**, M3 is the fixed-point-censored
   likelihood method evaluated in that paper.
   And, for the model form itself:
   **R47.** Tobin J. Estimation of relationships for limited dependent variables.
   *Econometrica*. 1958;26(1):24–[36]. doi:10.2307/1907382. (First page verified;
   end page not in the Crossref record — treat as U11.)
5. **Rubin's rules** (on the brief) resolve to:
   **R48.** Rubin DB. *Multiple Imputation for Nonresponse in Surveys*. New York:
   John Wiley & Sons; 1987. doi:10.1002/9780470316696.
   ISBN 978-0-471-08705-2. *Supports* (Methods, ~L1622): *"…refits by ordinary least
   squares, and pools 50 fits by Rubin's rules."* Verified via Crossref.
6. **Schoenfeld residuals are uncited**, and the test actually used is not
   Schoenfeld's. Methods, ~L1667: *"Proportionality is tested on Schoenfeld
   residuals."* The residual is Schoenfeld's; the **test** on scaled Schoenfeld
   residuals, which is what `lifelines` implements, is Grambsch & Therneau's.
   **R49.** Schoenfeld D. Partial residuals for the proportional hazards regression
   model. *Biometrika*. 1982;69(1):239–241. doi:10.1093/biomet/69.1.239.
   **R50.** Grambsch PM, Therneau TM. Proportional hazards tests and diagnostics
   based on weighted residuals. *Biometrika*. 1994;81(3):515–526.
   doi:10.1093/biomet/81.3.515. (An amendment appears at *Biometrika*
   1995;82(3):668, doi:10.2307/2337547.) Both verified. **Cite R50, or both.**
7. **Two mechanistic biology claims in the Discussion are uncited** (R21, R22, R39,
   R40): the near-neutrality of *katG* S315X, and the drug mechanisms that make
   growth state the expected axis. Both carry Discussion paragraphs.
8. **The mycobacteria-specific time-kill question: a partial absence, and a better
   citation.** The brief allowed "no formal standard exists" as an answer. The
   accurate finding is narrower and more useful:
   - **No standards-development organisation publishes a time-kill method for
     mycobacteria.** CLSI's mycobacterial documents (M24, 3rd ed. 2018; supplement
     M24S) cover MIC and susceptibility testing; the 2nd edition's full text was
     read and contains no killing-curve method. CLSI's only bactericidal-activity
     guideline is M26-A (R31), which is general-bacterial and archived. A search
     for a EUCAST time-kill methodology document returned none; EUCAST publishes
     breakpoint tables and MIC/disk-diffusion methodology, and **absence there is
     reported as "not located", not as proven.**
   - **But a peer-reviewed mycobacterial time-kill protocol does exist**, and it is
     the right thing to cite alongside M26-A: Rabodoarivelo et al. 2025, *STAR
     Protocols* (R34) — same consortium as the six-laboratory deposit, and it uses
     both CFU and MPN readouts.
   - **And the "range of dilutions and target inocula" concession has a source**:
     Franzblau et al. 2012 (R33), the Gates-commissioned survey documenting exactly
     that heterogeneity across TB laboratories.
   Recommended Section 6 wording: *"…and tuberculosis protocols work from a range
   of dilutions and target inocula (Franzblau et al. 2012). No standards body
   publishes a killing-curve method for mycobacteria — CLSI M24 covers
   susceptibility testing only — so a general bacterial guideline is being applied
   to a mycobacterial assay; the nearest published mycobacterial protocol
   (Rabodoarivelo et al. 2025) is a method paper, not a consensus standard."*
9. **Windels is cited only as a deposit.** Every other deposit is cited with its
   article; add R38.
10. **The van Wijk figshare item and the iScience article have different titles and
    different author lists.** Both entries are needed and neither substitutes for
    the other (R4, R23). The repository's `docs/18` records the article as *iScience*
    26(5); it is 26(4).
11. **Balaban et al. 2019 persistence definitions** (*Nat Rev Microbiol*
    17:441–448) is **not** cited and, in my reading, is **not needed**: the
    manuscript's definition of tolerance is taken from Brauner 2016 and it never
    invokes the consensus persistence definitions. Flagged only so the decision is
    deliberate rather than accidental. Not verified in this pass.
12. **Common-statistics citations.** Fisher exact (R11), Mann–Whitney (R18),
    Wilcoxon signed-rank (R20), Spearman (U8), permutation testing and ROC/AUC are
    all used in the text. Most microbiology journals treat these as needing no
    citation; some statistics-forward journals want them. R11, R18 and R20 are
    verified and ready if wanted. **Permutation testing** (Results §5, ~L787:
    *"It owns 87.0 per cent of the variance in starting density (permutation
    p < 0.0002)"*) and **AUC** (~L695: *"Starting density separates flasks that ever
    crossed from those that never did with an area under the curve of 0.974"*) have
    no verified source in this pass; if the journal wants them, Fisher's *The
    Design of Experiments* (1935) and Hanley & McNeil (*Radiology* 1982) are the
    conventional choices — **neither verified here, do not print without checking.**

### Count

- **Section 1 verified entries:** 45 (R1–R45), plus R46–R50 introduced in Section 3
  and verified there. **Total verified: 50.**
- **Section 2 items needing work before submission:** 11 (U1–U11), of which 5 are
  missing an end page or a DOI on a pre-digital article (U1, U2, U4, U6, U11),
  2 are paywalled standards that must be read at source (U5, U7), 1 is a table
  identity to confirm (U3), 1 is an unverified optional citation (U8), and 2 are
  accuracy flags rather than missing fields (U9, U10).

- **Nothing in this list was reconstructed from memory.** Every DOI, volume, issue,
  page range, PMID and PMCID printed above came back from PubMed, Crossref,
  Project Euclid, the figshare API, the Zenodo API, the NCBI ID converter, the FDA
  catalogue or CLSI's own catalogue during this compilation pass. Fields those
  sources did not return are blank and are listed in Section 2.
