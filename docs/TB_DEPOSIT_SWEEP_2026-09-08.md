# Systematic sweep for mycobacterial time-kill deposits

Search date **2026-09-08**. Six territories, twelve agents, 1,040 tool calls.
Every floor and starting density below was read in a file or article the agent
opened; nothing is inferred from a secondary description.

**151 distinct candidates assessed.**

## Qualifies (25)

### ALPE2026

**Citation** Rodriguez-Blanco et al. (BioVersys / Institut Pasteur de Lille / Univ. Lille, TRIC-TB). Alpibectir-Ethionamide combination (AlpE) for the treatment of tuberculosis. Nat Commun 2026;17:4954. doi:10.1038/s41467-026-71460-6. PMC13234193. IMI2 JU grant 853800 (TRIC-TB).

**Organism** M. tuberculosis H37Rv and an isogenic H37Rv delta-adhD mutant in vitro; M. tuberculosis H37Rv in BALB/c mouse lung after intravenous infection (confirmed in the Results text I read: 'Mice were intravenously (IV) infected with M. tuberculosis H37Rv').

**Drug** Ethionamide (2.5 and 25 mg/L) alone and with the VirS-targeting booster alpibectir (0.003, 0.03, 0.3 mg/L); isoniazid 2.5 mg/L; alpibectir alone. In vivo: ethionamide 5/15/50/100/200 mg/kg, alpibectir 0.1/0.5/1.6 mg/kg, and nine combinations, plus INH 25 mg/kg.

**Deposit** Source Data file 41467_2026_71460_MOESM6_ESM.xlsx, 325,550 bytes, 23 sheets. I downloaded it from the Europe PMC supplementary bundle for PMC13234193 and confirmed both the sheet count and the byte size. CFU lives in 'Fig 6' (in vitro), 'Fig 7' and 'Supp Tables 7A and 7B' (in vivo).

**Obtainable** YES, no access request. https://doi.org/10.1038/s41467-026-71460-6 -> Source Data; or the whole bundle at https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13234193/supplementaryFiles (2,679,187 bytes, 20 files).

**Measured N0** YES, with a caveat worth stating in his paper. Sheet 'Fig 6', row Day 0: H37Rv 6.30, 6.31, 5.88 log10 CFU/mL; H37Rv delta-adhD 5.70, 5.95, 5.66. The Methods say the flasks were 'inoculated with 10 mL of M. tuberculosis H37Rv WT or delta-adhD cultures diluted to an OD600 nm of 0.005 (theoretically corresponding to 5 x 10^5 CFU/mL)' — the measured day-0 sits about four-fold above the nominal, exactl

**Floor** STATED, BOTH COMPARTMENTS — this is the upgrade. IN VITRO, 10^2 CFU/mL, given three independent ways: (a) Results, 'never reaching the limit of detection of 10^2 CFU/mL'; (b) Results, 'driving bacterial counts down to the detection limit (10^2 CFU/mL) within 7 days'; (c) Methods, derived from the plated volume — 'cultures were 10-fold serially diluted (up to 10^-7) and 10 uL of each serial dilution and of the non-diluted culture were plated ... The lowest possible number of countable CFUs (limit of detection) is 1 when plating 10 uL of a non-diluted culture, which amounts to a log10 CFU/mL of 

**Timepoints** IN VITRO, sheet 'Fig 6': 6 timepoints, days 0, 2, 4, 7, 14, 21. Two strains x 8 arms (no drug; INH 2.5; alpibectir 0.3; Eto 2.5; Eto 25; Eto 2.5 + alpibectir at 0.003, 0.03, 0.3 mg/L) x 3 biological replicates = 48 replicate-level series, all six points populated in every column. IN VIVO, sheets 'Fi

**Licence** CC BY 4.0. The article XML carries 'This article is licensed under a Creative Commons Attribution 4.0 International License' and 'http://creativecommons.org/licenses/by/4.0/'. Source Data inherits it.

**Verdict** QUALIFIES, and now the strongest of the set. Open CC BY Source Data, per-replicate log10 CFU/mL over six timepoints, a measured (if shared) time-zero that visibly contradicts the nominal inoculum, and a detection floor stated as a number for BOTH the in vitro and the in vivo experiment. The booster 

---

### BARR2021_OSF

**Citation** Barr DA, Schutz C, Balfour A, et al. Flow cytometry method for absolute counting and single-cell phenotyping of mycobacteria. Sci Rep 2021;11:18661. PMID 34545154. DOI 10.1038/s41598-021-98176-5

**Organism** Mycobacterium bovis BCG in 7H9 broth

**Drug** 

**Deposit** OSF project https://osf.io/gwhpd/ (node public: true). The time-kill data are in tkc.csv (17,890 bytes, 385 data rows, 10 columns) with the analysis in tkc_analysis.R (31,499 bytes). read_me.rtf (5,877 bytes) documents both. The full node holds 25 items including a 134 MB and a 56 MB raw FCS export.

**Obtainable** YES — https://osf.io/download/5py7g/ (tkc.csv), https://osf.io/download/8nmwd/ (tkc_analysis.R), https://osf.io/download/n8ds2/ (read_me.rtf). No login, no view-only token needed despite the paper quoting one. I downloaded and opened all three.

**Measured N0** YES. Column 'cfu.ml' at 'timepoint' = 0, present for 76 of the 77 series (the single gap is amx = R, conc = 2.0, rep = C, where the whole row is NA). The day-0 values range from 9000 to 113000 CFU/mL across series and vary independently between replicates — a measured baseline, not a normalisation. The paper's nominal is 'grown to a density of ~ 2 x 10^6 CA+ cells per ml', so as with BOSCH2026 the

**Floor** 6.67 CFU/mL as reported, 20 CFU/mL per colony per plate segment, derived by arithmetic from the stated plated volume. Methods, verbatim (PubMed Central, PMC8452731, DOI 10.1038/s41598-021-98176-5): 'Each segment of a plate was inoculated with 50uL of serial dilutions and spread using disposable, sterile loop spreaders. CFU counts were performed with threefold technical replicates and counts averaged. Colony counts between 1 and 100 per segment were accepted and, after adjustment for dilution, averages across dilutions were made where available.' 50 uL per segment with counts reported per mL gi

**Timepoints** 5 timepoints per series — 'timepoint' takes values 0, 1, 2, 3, 5 (days), matching the paper's 'bacilli quantified at 0, 24, 48, 72 and 120 h'. 77 series = amx x conc x rep, with amx in {CTRL_A, CTRL_B, E, H, K, R} (ethambutol, isoniazid, kanamycin, rifampicin plus two control arms), conc in multiple

**Licence** OSF node declares no licence (node_license null). The Sci Rep article is CC BY 4.0. He should note the deposit itself is unlicensed.

**Verdict** QUALIFIES. Confirmed at the bytes on all three criteria — measured t = 0 in cfu.ml for 76 of 77 series, a floor recoverable from a stated 50 uL plating volume and corroborated by the data's own thirds-of-20 quantum, and 5 timepoints x 77 series. Its distinctive value is unchanged: it is the only dep

---

### BC1_NATCOMM2025

**Citation** Nature Communications 2025; "The role of cytochrome bc1 inhibitors in future tuberculosis treatment regimens". DOI 10.1038/s41467-025-64427-6 (PMID 41125580, PMC12546632).

**Organism** Mycobacterium tuberculosis — BALB/c and C3HeB/FeJ-type mouse lung across five in vivo studies (A, B, C, D, E) plus a sixth acute study (F) using clinical isolate Mtb-N1283; also H37Rv and clinical isolates in vitro.

**Drug** Telacebec (Q203), JNJ-2901 and JNJ-4052 (cytochrome bc1 inhibitors) in combination with bedaquiline, pretomanid, linezolid, clofazimine, moxifloxacin, pyrazinamide, rifampicin, isoniazid and ethambutol. One file spans most of the territory drug list.

**Deposit** Nature Communications Source Data file, 41467_2025_64427_MOESM6_ESM.xlsx (38,852 bytes), with a second statistics workbook MOESM3 and a 30-page supplementary PDF MOESM1. Fourteen sheets: 'Fig. 1b', 'Fig. 1c', 'Fig. 1d', 'Fig. 2', 'Fig. 3a'-'Fig. 3e', 'Supp. Fig. 2', 'Supp. Table 4', 'Supp. Table 8',

**Obtainable** YES, and I downloaded and read it. Direct URL that works without any access request: https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-64427-6/MediaObjects/41467_2025_64427_MOESM6_ESM.xlsx . The nature.com article page redirects a fetch through idp.nature.com and the PMC mirror now 

**Measured N0** YES — measured, per animal, and with a pre-baseline as well as a baseline. The mouse sheets carry explicit columns 'Day -13' and 'Day 0' (Supp. Table 4, Studies A and B), 'day-13' and 'day 0' (Supp. Table 8, Study C), '-2wks', 'Day 0' and '2 wks' (Supp. Table 11, Study D), and 'Day -10' and 'Day 0' (Supp. Table 12, Study E). These are harvested log10 CFU/lung per mouse, not the nominal aerosol imp

**Floor** PRESENT AND EXACT, but NOT where the brief said. CORRECTION: the claimed "0.4 log10 CFU/lung — stated in the paper for Study E" is not stated in the paper. I grepped the full article text and all 30 pages of the supplementary PDF for 'detection', 'detection limit', 'LOD', 'limit' and '0.4 log' and found no such statement; the only hits for 'detect' are 'No colonies were detected' and 'underpowered to detect statistically significant differences'. The floor is instead visible as a literal recurring censoring value in the deposited numbers, and it reconstructs exactly from the per-study plating 

**Timepoints** Study A: Day -13, Day 0, 4 weeks, 8 weeks, plus 8wk+12wk relapse — 4 CFU timepoints on treatment, 6 regimens (BPaL, BPaM, BPaMJ, BPaMZ, BPaC, BPaCJ) plus SoTX control, n=5 per arm rising to 16 in the relapse columns. Study B: Day -13, Day 0, 8 weeks, 12 weeks, plus relapse — 6 regimens. Study C: day

**Licence** CC BY 4.0 — the article carries a Creative Commons Attribution 4.0 statement, and Nature Communications Source Data files are covered by the article licence.

**Verdict** QUALIFIES, rank second. Per-animal log10 CFU/lung, a measured pre-baseline AND a measured Day 0, four or more on-treatment timepoints in Studies A and D, and a floor that is exact and per-study once you read it out of the numbers. Its distinctive value for a paper about what a time-kill assay can re

---

### BISHAI2023_JHU083

**Citation** Glutamine metabolism inhibition has dual immunomodulatory and antibacterial activities against Mycobacterium tuberculosis. Nat Commun 2023;14. doi:10.1038/s41467-023-43304-0. PMC10654700, PMID 37973991.

**Organism** Mycobacterium tuberculosis H37Rv; 129S2 mice (aerosol), BALB/c SCID mice, C3HeB/FeJ mice; plus bone-marrow-derived macrophages for the intracellular series. Lung burden.

**Drug** JHU083 (orally bioavailable glutamine-antagonist prodrug of DON) 1 mg/kg daily for 5 days then 0.3 mg/kg 5/7; rifampicin 12.5 mg/kg comparator; PBS control. In vitro/intracellular: DON, JHU083, INH at 10x MIC.

**Deposit** Journal-hosted Source Data workbook 41467_2023_43304_MOESM6_ESM.xlsx (20 sheets, labelled 'source data') plus Supplementary Data 1 as MOESM4 (metabolomics).

**Obtainable** YES, downloaded and parsed. https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-43304-0/MediaObjects/41467_2023_43304_MOESM6_ESM.xlsx (381,405 bytes, HTTP 200). No access request. The data availability statement's claim that this is the raw data holds up: the sheets are per-mouse, ind

**Measured N0** YES, verified at row level — AND it contradicts the Methods, which is the reason to keep this one. Sheet 'Fig 2' block 'Fig 2b | Lung CFU (Log10)' has columns Week 0, Week 2, Week 5 and rows labelled per animal (WT-PBS-Lung-M1 through M5). The Week 0 values are 1.8976270912904414, 1.8195439355418688, 2.089905111439398, 2.0530784434834195 — i.e. roughly 66-123 CFU, mean 10^1.965 = about 92 CFU. The

**Floor** NONE. I swept all 20 sheets for LOD, limit-of-detection, plated, dilution and volume strings: no numeric floor, no plated volume, no homogenate volume, no censoring flag. Sheet 'Fig 1' block 'Fig 1e' (MBC assay) records 'CFU per tube (log10)' as a bare 0 at 64 and 32 microgram/mL, which is a censored zero with no declared limit. Do not assert a floor.

**Timepoints** In vivo (sheet 'Fig 2b'): THREE timepoints — Week 0, Week 2, Week 5 — across three arms (PBS, JHU083, RIF), 4-5 mice per arm per timepoint, per-animal rows. Intracellular (sheet 'Fig 1f'): THREE timepoints — Day 0, Day 3, Day 5 — across four arms (BMDM alone, +DON, +JHU083, +INH) in triplicate, givi

**Licence** CC BY 4.0 (Nature Communications open access).

**Verdict** QUALIFIES — confirmed, and I would accept it, though it sits exactly on the three-timepoint boundary. It meets the deposit and measured-N0 tests cleanly and fails the floor test outright. Two things earn it a place: the measured Week 0 of about 92 CFU against a nominal ~275 CFU in the Methods is a c

---

### BOSCH2026_NATMICRO

**Citation** Bosch B, et al. Transcription co-inhibition alters drug resistance evolution and enhances Mycobacterium tuberculosis clearance from granulomas. Nat Microbiol 2026. PMID 41339746, PMCID PMC12858399. DOI 10.1038/s41564-025-02201-6

**Organism** Mycobacterium tuberculosis H37Rv (WT) in 7H9 broth. The isogenic rpoB S450L and H445Y strains appear in the deposit only as OD600 growth and percent-growth-inhibition tables, not as CFU.

**Drug** 

**Deposit** Nature Microbiology Source Data PDFs attached to the article. The two that matter are 'Source Data Fig. 5' = 41564_2025_2201_MOESM6_ESM.pdf (314,590 bytes) and 'Source Data Extended Data Fig. 6' = 41564_2025_2201_MOESM12_ESM.pdf (32,392 bytes). I downloaded MOESM3 through MOESM12 and read all ten.

**Obtainable** YES — https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-025-02201-6/MediaObjects/41564_2025_2201_MOESM6_ESM.pdf and .../41564_2025_2201_MOESM12_ESM.pdf. No login, no request. Note two access traps for the strategy: www.nature.com/articles/s41564-025-02201-6 returns a 303 to idp.nature.c

**Measured N0** YES, and genuinely measured rather than nominal. Source Data Fig. 5, Panel a, row 'Days = 0' reads verbatim: '0 3650000 3550000 3750000 3000000 3750000 8050000 5800000 3400000 3000000 6600000 2200000 3800000' — twelve different values across six conditions in duplicate, spanning 2.2e6 to 8.05e6. Source Data Extended Data Fig. 6, Panel a, row 0 reads '0 3650000 3550000 3750000 3000000 4750000 34000

**Floor** 10 CFU/mL, substituted into the deposited numbers by the authors. It is not written in words anywhere — no LOD sentence, and the Methods say only 'the cultures were serially diluted and plated on 7H10 charcoal agar' with no volume. But the arithmetic is unambiguous. In Source Data Fig. 5 Panel a the day-14 row reads '14 1e+009 1e+009 10 10 10 10 10 10 5600000 2800000 21000 7700000' — the value 10 appears six times, once for each replicate of RIF, RIF+AAP-SO2 (10X) and RIF+AAP-SO2 (20X). In Source Data ED Fig. 6 Panel a the value 10 appears twice at day 14 and six times at day 24. Across both t

**Timepoints** Two tables. Source Data Fig. 5 Panel a: 5 timepoints (days 0, 2, 4, 10, 14) x 6 conditions (DMSO, RIF, RIF+AAP-SO2 10X, RIF+AAP-SO2 20X, AAP-SO2 10X, AAP-SO2 20X) x 2 replicates = 12 series. Source Data Extended Data Fig. 6 Panel a: 6 timepoints (days 0, 2, 4, 10, 14, 24) x 4 conditions (DMSO, RIF, 

**Licence** Nature Portfolio; article open access via PMC12858399. The Source Data PDFs carry no separate licence statement.

**Verdict** QUALIFIES, and it is now the most valuable of the eleven. It brings a drug class nothing in the manifest has (AAP-SO2, an RNA-polymerase transcription co-inhibitor) plus fidaxomicin and two-drug combinations with rifampicin; it has a measured, replicate-varying day 0; and its deposited numbers carry

---

### DIDEAGOSSOU2022

**Citation** NEW, found via Table S1 of the TBDA relapse preprint — not on the exclusion list. Dide-Agossou C, Bauman AA, Ramey ME, Rossmassler K, ... Walter ND, Robertson GT, et al. Combination of Mycobacterium tuberculosis RS Ratio and CFU Improves the Ability of Murine Efficacy Experiments to Distinguish between Drug Treatments. Antimicrob Agents Chemother 2022;66(4):e0231021. doi:10.1128/aac.02310-21. PMC9

**Organism** M. tuberculosis in BALB/c mouse lung, across three experiments at two institutions (Johns Hopkins and Colorado State).

**Drug** Experiment 1: rifampin, isoniazid, streptomycin, ethambutol, pyrazinamide, bedaquiline monotherapies plus untreated. Experiment 2 (JHU): HRZE, PMZ, BMZ, BMZRb. Experiment 3 (CSU): HRZE, PaMZ, BPaMZ, BPaL.

**Deposit** Supplemental file 2, Data Set S1: aac.02310-21-s0002.xlsx, 25,853 bytes, 5 sheets — 'Experiment1 PD markers data', 'Experiment2 PD markers data', 'Experiment3 PD markers data', 'Experiment2 relapse data', 'Experiment3 relapse data'. Data availability statement: 'All primary data is included in the s

**Obtainable** YES, no access request. https://doi.org/10.1128/aac.02310-21 -> Supplemental file 2; or the bundle at https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9017352/supplementaryFiles (767,368 bytes).

**Measured N0** YES, per mouse. Experiment 2 sheet has a 'PreRx' group at Time (days) = 0 with per-mouse CFU 7.20, 7.22, 7.18, 7.37, 7.42 log10. Experiment 3 sheet has a 'PreRx' group at Time = 0 with per-mouse RAW counts 20,600,000; 12,700,000; 20,200,000; 20,400,000; 15,900,000; 15,700,000. Experiment 1 has no time column at all — every row is a single sacrifice point.

**Floor** PARTIAL, and only by cross-reference. Nothing numeric in this paper: the article says only that 'CFU burdens were estimated by serial dilutions of lung homogenates and plating on 7H11-oleic acid-albumin-dextrose-catalase (OADC) agar using 0.4% activated charcoal', and the 11-page supplemental methods PDF adds no volume, no fraction and no LOD — I searched it for 'limit of detection', 'detection limit', 'LOD', 'plated', 'dilution' and 'undetect' and the only quantitative statement is the relapse one, 'tissues were homogenized in PBS and plated in their entirety'. HOWEVER: Experiment 1's per-mou

**Timepoints** Experiment 3 is the prize: Time (days) 0 (PreRx), 7, 14, 21, 28 — FIVE timepoints — for four regimens (HRZE, PaMZ, BPaMZ, BPaL), 90 per-mouse rows carrying paired CFU, RS ratio, 16S and 23S rRNA burden. Experiment 2: Time 0 (PreRx), 14, 28 — three timepoints — for HRZE, PMZ, BMZ, BMZRb, 44 rows. Exp

**Licence** CC BY (Europe PMC core record: isOpenAccess Y, license 'cc by').

**Verdict** QUALIFIES on data, with an overlap warning he must handle before citing. Open CC BY, per-mouse raw values, measured day-0 baselines, and a genuine five-point murine series in Experiment 3. What it ADDS is Experiment 2: the BMZ, BMZRb and PMZ regimens run at Johns Hopkins are not in Walter 2021 or an

---

### ERNEST2024_TBI223

**Citation** Ernest JP, et al. Dose optimization of TBI-223 for enhanced therapeutic benefit compared to linezolid in antituberculosis regimen. Nat Commun 2024;15. doi:10.1038/s41467-024-50781-4. PMC11344811, PMID 39181887.

**Organism** Mycobacterium tuberculosis H37Rv; female BALB/c mice (acute and chronic aerosol models). Also beagle, Sprague-Dawley and C57 PK, and a human Nix-TB sputum block.

**Drug** TBI-223 and linezolid as dose-fractionated monotherapy (300/1000/3000 mg/kg per week at QD/BID and 3-7 days per week) and in combination with bedaquiline + pretomanid (12.5/25/50 mg/kg BID and 100 mg/kg QD linezolid; 15/30/45 mg/kg BID and 100 mg/kg QD TBI-223).

**Deposit** figshare, DOI 10.6084/m9.figshare.26054098.v1 — a single stacked multi-block file, source_data_tbi223.csv (120,694 bytes, 1,976 rows).

**Obtainable** YES, downloaded and re-parsed end to end. https://doi.org/10.6084/m9.figshare.26054098.v1; direct file https://ndownloader.figshare.com/files/47111650 (HTTP 200, 120,694 bytes, text/csv). No access request.

**Measured N0** YES, verified at row level. The 'Panel A: Combination therapy' and 'Panel B: Combination therapy' blocks (columns TIME_DAY, LOGCFU, DOSE, DRUG) carry rows at TIME_DAY = -17, the implantation count, and TIME_DAY = 0, the measured burden at treatment start, before the 28-day rows. The 'Panel A/B: Mono-therapy' blocks (columns ID, TIME_DAY, LOGCFU, DRUG, TOTAL_WEEKLY_DOSE, FREQ) carry TIME_DAY = 1 an

**Floor** NONE — confirmed by re-parsing rather than assumed. There is no LOD or LOQ column for counts and no censoring flag in any CFU block. The file DOES contain a column named BLQ, but it appears only in the two Pharmacokinetics blocks alongside CONC_MGL, i.e. it flags drug concentrations below the limit of quantification, not colony counts. No plated volume or homogenate volume is recorded anywhere in the deposit, and the Methods give neither. This is the cleanest 'no floor' case in the set.

**Timepoints** Corrected from the prior description. Monotherapy blocks: FOUR timepoints — TIME_DAY 1, 6, 28, 34 — 45 rows each for TBI-223 and linezolid, across TOTAL_WEEKLY_DOSE of 0/300/1000/3000 and FREQ of 0/12/24/48 h. Combination blocks: THREE timepoints — TIME_DAY -17, 0, 28 — 31 and 32 rows, across five d

**Licence** CC BY 4.0 — confirmed from the figshare v2 API record (license.name 'CC BY 4.0', url creativecommons.org/licenses/by/4.0/), published 2024-06-18.

**Verdict** QUALIFIES on data and measured N0; FAILS on floor, confirmed by re-parsing the whole file rather than inferred. Worth keeping for precisely that reason: a fully public, CC BY, per-mouse murine kill dataset with two measured pre-treatment timepoints, four timepoints in the monotherapy arms, roughly 3

---

### HEINRICH2025_BTZ043

**Citation** The clinical-stage drug BTZ-043 accumulates in murine tuberculosis lesions and efficiently acts against Mycobacterium tuberculosis. Nat Commun 2025;16. doi:10.1038/s41467-025-56146-9. PMC11742723, PMID 39827265.

**Organism** Mycobacterium tuberculosis H37Rv; female BALB/c mice (aerosol) and IL-13 transgenic mice with necrotic lesions. Lung burden, plus granuloma-level CFU/mm3 by MBLA.

**Drug** BTZ-043 (DprE1 inhibitor) at 2.5, 5, 50, 250, 500 and 1000 mg/kg/day, QD versus BID dose fractionation; isoniazid 25 mg/kg comparator; vehicle.

**Deposit** Journal-hosted Source Data workbook 41467_2025_56146_MOESM13_ESM.xlsx (16 sheets, labelled 'source data' on the article page) plus eight Supplementary Data workbooks MOESM4-MOESM11.

**Obtainable** YES, downloaded and parsed, all nine workbooks. https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-56146-9/MediaObjects/41467_2025_56146_MOESM13_ESM.xlsx (55,601 bytes, HTTP 200). No access request.

**Measured N0** YES, verified at row level, and measured at TWO pre-treatment points. Sheet '1a&b' has row labels '3 weeks before therapy' with per-mouse raw counts 176, 182, 162, 176, 159 CFU — the implantation count — and 'therapy start (0)' with 3450000, 23700000, 18600000, 9900000, 13800000. Sheet '1c' has 'therapy start (0)' 1012501, 553334.3, 49501. Sheet '3a' has 'before therapy' 222857143, 955846154, 1539

**Floor** NONE. I swept every cell of the Source Data workbook and all eight Supplementary Data workbooks for LOD, limit-of-detection, plated, dilution and volume strings: no LOD value, no homogenate volume, no plated volume, no censoring flag anywhere in the deposit. The paper gives a plated volume for the dose-fractionation study only ('0.5 mL aliquots were plated') without the total homogenate volume, so the arithmetic does not close there either. One artefact worth noting instead: sheet '1c' values carry a systematic +1 (1012501, 490001, 325001, 157501, 50001, 110001, 82501), i.e. a pseudo-count add

**Timepoints** Sheet '1a&b' (main dose-response): FIVE timepoints — 3 weeks before therapy, therapy start (0), 4 weeks, 6 weeks, 8 weeks of treatment — with up to 50 columns of per-mouse counts across the no-treatment control and the BTZ-043 dose arms plus INH. Sheet '1c' (dose fractionation): two timepoints, 62 c

**Licence** CC BY 4.0 (Nature Communications open access).

**Verdict** QUALIFIES on data and on measured N0 — promoted from NEEDS A LOOK now that the workbooks are open — but FAILS on floor, definitively rather than provisionally. I checked all nine deposited workbooks and there is no recoverable detection limit. That makes it the strongest 'no floor' exemplar in the s

---

### JINDANI1980_SGUL

**Citation** Jindani A, Doré CJ, Mitchison DA. Bactericidal and sterilizing activities of antituberculosis drugs during the first 14 days. Am J Respir Crit Care Med 2003;167:1348-1354. PMID 12519740, DOI 10.1164/rccm.200210-1125OC. Data deposit: St George's, University of London figshare, posted 25 November 2024, DOI 10.24376/rd.sgul.27862029.v1. CORRECTION to the candidate record: the deposit's own 'reference

**Organism** Mycobacterium tuberculosis in human sputum, pulmonary TB patients (in vivo, human)

**Drug** 

**Deposit** https://sgul.figshare.com/articles/dataset/_b_Bactericidal_and_Sterilizing_Activities_of_Antituberculosis_Drugs_during_the_First_14_Days_b_EBA_Study_/27862029 — one file, 'Jindani 1980.xlsx', 64,648 bytes, one worksheet named 'Jindani 1980', 113 rows x 49 columns.

**Obtainable** YES — direct file at https://ndownloader.figshare.com/files/50649807, no login, no request, CC BY 4.0. I downloaded it and opened it with openpyxl. (The sgul.figshare.com HTML page returns 403 to a bare curl, but the ndownloader link and the api.figshare.com record both work.)

**Measured N0** YES, in duplicate, and it is the best-documented baseline of the eleven. The worksheet carries two independent pre-treatment specimens per patient, columns C-G ('Day-0 A Ct1', 'Day-0 A Ct2', 'Diln', 'cfu', 'Log cfu') and columns H-L ('Day-0 B Ct1', 'Day-0 B Ct2', 'Diln', 'cfu', 'Log cfu'), with column M 'Mn Log cfu' holding the mean of the two day-0 log values. 112 of 112 patients have a Day-0 A c

**Floor** 24 CFU/mL per colony at the lowest dilution used, derived by arithmetic entirely from inside the deposit. No LOD, LOQ or plated volume appears in the figshare record, and the 2003 AJRCCM paper is not open access (Europe PMC: inEPMC N, isOpenAccess N), so nothing had to be taken from the paper. The workbook stores, for every timepoint, two raw colony counts (Ct1, Ct2), a dilution index (Diln, integer 1-6), and the resulting cfu. I checked the mapping across all 977 populated cells: Diln 1 -> x48, Diln 2 -> x480, Diln 3 -> x4800, Diln 4 -> x48000, Diln 5 -> x480000, Diln 6 -> x4800000, with a si

**Timepoints** 9 measurement blocks per patient across 8 distinct sampling days: Day-0 A, Day-0 B (duplicate pre-treatment specimens), then Day-2, Day-4, Day-6, Day-8, Day-10, Day-12, Day-14. 112 patients (NOT the 100 the deposit description claims) across 24 distinct regimen codes (NOT 22): Z (n=9), R20 (8), R10 

**Licence** CC BY 4.0

**Verdict** QUALIFIES, and it is second only to BOSCH2026 on what it adds. It is the only human in-vivo bacterial-load series here, the only one with an untreated arm ('Nil') alongside 23 drug regimens including monotherapy dose-ranging (H150/H300/H600, R5/R10/R20), and the only deposit of the eleven that gives

---

### JINDANI2003_SGUL

**Citation** Jindani A, Doré CJ, Mitchison DA. Bactericidal and Sterilizing Activities of Antituberculosis Drugs during the First 14 Days (EBA Study). Dataset, St George's, University of London, posted 25 Nov 2024, v1. DOI 10.24376/rd.sgul.27862029. CITATION CAVEAT: the record links to Am J Respir Crit Care Med 2003;167(10):1348-54 (DOI 10.1164/rccm.200210-1125OC), but the deposited file is named 'Jindani 1980

**Organism** Mycobacterium tuberculosis, clinical strains, in sputum from adults with pulmonary TB (human in vivo)

**Drug** 24 regimen arms, verified from the 'reg' column with patient counts: Z (9), R20 (8), R10 (8), T (8), SHRZM (4), SHRZ (4), SHR (4), SHZ (4), HRM (4), SH (4), SR (4), RM (4), HR (4), HZ (4), SZ (4), HM (4), H600 (4), H300 (4), H150 (4), M (4), S (4), Nil (4), PAS (4), R5 (3). Note two features nothing

**Deposit** figshare institutional instance sgul.figshare.com, item 27862029. Single file 'Jindani 1980.xlsx', 64,648 bytes, md5 f36e9a2067bbc8a34e6bad436cc935a5 (supplied md5 == computed md5 == the md5 of the file I downloaded). One worksheet, 'Jindani 1980', 113 rows x 49 columns.

**Obtainable** YES. Direct file: https://ndownloader.figshare.com/files/50649807 — I downloaded it, 64,648 bytes, md5 matches the record. Landing page: https://sgul.figshare.com/articles/dataset/_b_Bactericidal_and_Sterilizing_Activities_of_Antituberculosis_Drugs_during_the_First_14_Days_b_EBA_Study_/27862029 (the

**Measured N0** YES. Columns 3-13 of the sheet: 'Day-0 A Ct1', 'Day-0 A Ct2', 'Diln', 'cfu', 'Log cfu', then 'Day-0 B Ct1', 'Day-0 B Ct2', 'Diln', 'cfu', 'Log cfu', then 'Mn Log cfu'. Two independent pre-treatment sputum specimens (A and B) per patient, each plated in duplicate, giving four raw plate counts before a drop of drug. 112 of 112 patients have a Day-0 'Mn Log cfu'; 111 have both A and B specimens and 1

**Floor** DERIVED BY ME, NOT STATED BY THE AUTHORS — 24 CFU/mL, and I am flagging the derivation rather than dressing it as an author statement. There is no LOD or LOQ anywhere in the deposit: no column, no footnote, no README, no code, and the sheet ends at the last data row with no legend (I checked every row after the last populated ID). What the file does give is its own exact count-to-density arithmetic, which I reverse-engineered and then verified: cfu = (Ct1 + Ct2) x 2.4 x 10^Diln, holding in 976 of 977 populated cells (the single exception is a corrupt cell in the last row, id 1747206132 Day-14,

**Timepoints** 9 columns of viable count per patient: Day-0 A, Day-0 B (combined into 'Mn Log cfu'), then Day 2, 4, 6, 8, 10, 12, 14 — i.e. 8 distinct timepoints on the Day-0-mean basis, or 9 series columns if the two baseline specimens are kept separate. 112 patient-level series (112 distinct IDs, one row each). 

**Licence** CC BY 4.0 (figshare record, license.value 1, https://creativecommons.org/licenses/by/4.0/)

**Verdict** QUALIFIES, and rank it first. It clears all three tests: measured N0 in duplicate-of-duplicate, a floor with a value (derived from the file's own verified arithmetic, flagged as derived), and 8 timepoints across 112 series. It adds more than anything else in this territory: human sputum rather than 

---

### MABS_CF_FIGSHARE2025

**Citation** PLOS One 2025; "Infection model of THP-1 cells, growth dynamics, and antimicrobial susceptibility of clinical Mycobacterium abscessus isolates from cystic fibrosis patients: Results from a multicentre study". DOI 10.1371/journal.pone.0319710 (PMC11957364). NOTE: I established the DOI from the supplementary filenames (pone.0319710.s001-s004); the brief gave only the PMC ID.

**Organism** Mycobacterium abscessus — ATCC reference strain plus 16 clinical isolates from cystic fibrosis patients across four Madrid hospitals, both smooth and rough morphotypes, growing intracellularly in THP-1 macrophages.

**Drug** Amikacin, and it is a SUSTAINED exposure, not the extracellular-killing pulse I first suspected. Methods verbatim: cells were "either treated or not with amikacin (250 ug/mL) for 1 h. Further, cells were washed again three times in dPBS and subsequently maintained in IM with or without 50 ug/mL amik

**Deposit** Five separate figshare records, all open and all CC BY 4.0. The killing data is in 10.6084/m9.figshare.28398275.v2, titled "Data on Fig 4", described verbatim as "Intracellular growth (CFU/mL) measurements of smooth and rough strains under amikacin and amikacin-free conditions, performed in triplica

**Obtainable** YES, confirmed by downloading and reading the workbook, not by inference. The figshare HTML pages return HTTP 403 to a fetch but the figshare v2 API is fully open: https://api.figshare.com/v2/articles/28398275 returns the metadata and licence, and the file downloads without authentication from https

**Measured N0** YES in the amikacin-free arm, QUALIFIED in the amikacin arm. The Fig 4 workbook's first block is headed verbatim "Intracellular growth (CFU/mL) of smooth and rough strains under amikacin-free conditions, measured in triplicates for each strain" and its first row is Time = 2 hours, giving a measured pre-drug intracellular count for every strain in triplicate (ATCC: 110000, 90000, 80000; strain 3: 6

**Floor** NONE, by any route, and I looked hard. There is no LOD or LOQ statement, no figure-legend dashed line with a number, no README, no analysis code, and no plated volume anywhere in the article. The only plating sentences are "Viable counts were obtained by plating serial dilutions on Columbia + 5% sheep blood agar plates" and "bacterial suspensions and cell debris were serially diluted and plated on Columbia + 5% sheep blood agar plates" — neither gives a volume, so the arithmetic route is closed too. I grepped the full text for 'limit of detection', 'detection limit', 'LOD', 'LLOQ' and for any 

**Timepoints** Four timepoints — 2, 24, 48 and 72 hours post-infection — for 17 strains (ATCC plus isolates 1-16), each in triplicate, under two conditions. That is 17 x 3 x 4 x 2 = 408 raw CFU/mL values, structured as 34 killing/growth series (17 strains x 2 conditions) with triplicate replication. Amikacin arm s

**Licence** CC BY 4.0, confirmed from the figshare API 'license' field on all five records, and the PLOS One article is CC BY.

**Verdict** QUALIFIES — upgraded from the previous 'needs a look'. Access is confirmed at the byte level, the amikacin arm is a genuine sustained exposure with four timepoints and a matched control, the design is triplicated across 17 clinical strains, and the licence is clean. It should be ranked third. What i

---

### MERCHAN2025

**Citation** Merchan Ruiz C. Testing the efficacy of two mycobacteriophage-antibiotic combinations against Mycobacterium abscessus biofilms. Master internship report, Radboud UMC Medical Microbiology (supervisors J. van Ingen, M. McDaniel). Zenodo, 2025. doi:10.5281/zenodo.17037904.

**Organism** Mycobacterium abscessus GD01 (rough clinical isolate), planktonic and pre-established biofilm, in cation-adjusted Mueller-Hinton and 7H9

**Drug** Cefoxitin (8 and 16 ug/mL planktonic; 16 and 64 biofilm), tigecycline (0.25 and 0.5 planktonic; 0.5 and 2 biofilm), mycobacteriophages Muddy and 8UZL, each alone and in every phage-antibiotic pairing, with growth and ferrous-ammonium-sulfate controls

**Deposit** Zenodo, record type 'Report' (a thesis PDF plus eight data workbooks and a README) — it will not surface in dataset-type-filtered searches

**Obtainable** YES, no access request. Record https://zenodo.org/records/17037904 ; ten open files. Direct pattern https://zenodo.org/api/records/17037904/files/<name>/content — e.g. Planktonic_Muddyvs8UZL_FOX.xlsx (13,415 bytes), Planktonic_Muddyvs8UZL_TGC.xlsx (13,382), Biofilm_Muddyvs8UZL_TGC.xlsx (12,661), Bio

**Measured N0** YES, twice over, and better than previously reported. (1) An explicit in-series Day 0: sheet 'Planktonic CFU' of Planktonic_Muddyvs8UZL.xlsx, row DAY=0, gives 2500, 2600, 2300 CFU/mL across all four arms (shared inoculum); sheet 'Biofilm CFU' row DAY=0 gives 13400, 10000, 10500. The previous pass missed these. (2) A separate counted inoculum block in each antibiotic workbook: the planktonic pair c

**Floor** 100 CFU/mL, AUTHOR-STATED — this is the finding that changes the verdict. The previous pass could not extract the deposited PDF and left the floor as NONE FOUND; plain 'pdftotext -layout' reads it without difficulty. Stated twice: Figure 1 legend, 'Data points represent means from three independent experiments with three technical replicates. LOD = limit of detection (2log10 CFU/mL for bacteria, 2log10 PFU/mL for phages).' And Fig. S1 legend, 'LOD (limit of detection) = 2log10 CFU/mL MAB GD01'. 2 log10 CFU/mL = 100 CFU/mL. Consistent with the data, where 100 is the smallest non-zero value and 

**Timepoints** Antibiotic workbooks, planktonic (FOX and TGC): 5 timepoints — 24 h, 3 d, 5 d, 7 d, 10 d (dated 12/02, 14/02, 16/02, 18/02, 21/02) x 9 arms x 3 biological replicates = 27 CFU series each. FOX arms: Growth, Muddy, 8UZL, Fox 8, Fox 16, Fox 8+M, Fox 16+M, Fox 8+8UZL, Fox 16+8UZL. TGC arms: same shape w

**Licence** CC BY 4.0

**Verdict** QUALIFIES — upgraded from NEEDS A LOOK. Organism, exposure (cefoxitin and tigecycline are real antibiotics, so the phage question does not arise here), readout, timepoints, series count and measured t0 all clear comfortably, and the one criterion it previously failed is now met by an author-stated n

---

### MERCHAN2025_ZENODO

**Citation** Merchán Ruiz C, Pozuelo Torres M, Janssen S, Terschlüsen E, van Ingen J, McDaniel M. Testing the efficacy of two mycobacteriophage-antibiotic combinations against Mycobacterium abscessus biofilms. Zenodo, 2 September 2025. DOI 10.5281/zenodo.17037904

**Organism** Mycobacterium abscessus GD01, rough clinical isolate, planktonic and pre-established biofilm

**Drug** 

**Deposit** https://zenodo.org/records/17037904 — 10 files. I downloaded and opened all eight xlsx plus README.txt and the 21-page report PDF. Note a naming trap: 'Planktonic_Muddyvs8UZL.xlsx' actually contains four sheets — 'Biofilm CFU', 'Biofilm PFU', 'Planktonic CFU', 'Planktonic PFU' — so the biofilm phage

**Obtainable** YES — https://doi.org/10.5281/zenodo.17037904, CC BY 4.0, no login. One caveat for the strategy: zenodo.org intermittently returned HTTP 504 on individual file downloads and several files had to be retried across three attempts before all eight came down intact.

**Measured N0** YES, in every workbook, but it is not where you would look for it. Two forms. (a) In 'Planktonic_Muddyvs8UZL.xlsx', sheet 'Planktonic CFU', the DAY column starts at 0 with 2500, 2600, 2300 CFU/mL repeated across all four arms (a shared inoculum measured in triplicate); sheet 'Biofilm CFU' likewise starts at DAY 0 with 13400, 10000, 10500. (b) In the four antibiotic-combination workbooks the time s

**Floor** 100 CFU/mL (= 2 log10 CFU/mL), stated by the authors AND independently confirmed by the granularity of the deposited numbers. Verbatim from the deposited report PDF, figure legend: 'LOD = limit of detection (2log 10 CFU/mL for bacteria, 2log10 PFU/mL for phages).' Repeated in the Fig. S1 legend: 'LOD (limit of detection) = 2log10 CFU/mL MAB GD01'. Plating method, verbatim from the deposited Methods: 'the pellet was resuspended and plated using a drip dilution method on Middlebrook 7H10 + OADC plates to quantify viable bacteria', with ferrous ammonium sulfate added before plating to inactivate 

**Timepoints** Four independent CFU experiments, all meeting the bar. (1) Planktonic_Muddyvs8UZL_FOX.xlsx and _TGC.xlsx, sheet 'Planktonic': 5 timepoints ('24hr (12/02)', '3 days (14/02)', '5 days (16/02)', '7 days (18/02)', '10 days (21/02)') x 9 conditions x 3 replicates = 27 series each. FOX conditions: Growth,

**Licence** CC BY 4.0

**Verdict** QUALIFIES. Upgraded on two counts the record missed: there IS a measured starting density (day-0 rows in one workbook, a labelled 'GD01 Inoculum' block at the bottom of the sheet in the other four), and the stated 2 log10 LOD is corroborated by the data's own 100 CFU/mL quantum. Ranked third because

---

### PETHE2026_PMD_Q203

**Citation** A bactericidal tuberculosis drug regimen driven by inhibition of the terminal oxidases by pretomanid. EMBO Mol Med 2026. doi:10.1038/s44321-026-00378-9. PMC12988230, PMID 41652042. (Pethe/Berney laboratories.)

**Organism** Mycobacterium tuberculosis H37Rv and H37Rv delta-cydAB; BALB/c mice, lung AND spleen burden. Plus replicating and nutrient-starved in vitro cultures.

**Drug** Pretomanid (20 and 75 mg/kg in vivo, 10 microM in vitro) and the cytochrome bcc inhibitor Q203/telacebec (10 mg/kg in vivo, 100 nM in vitro), alone and in combination; DMSO control.

**Deposit** BioStudies record S-SCDT-10_1038-S44321-026-00378-9, mirrored as per-figure Source Data archives on the journal site: 44321_2026_378_MOESM5-9_ESM.zip = Source Data Figures 1-5. Inside MOESM9 are 'In vivo CFU Fig 5A.xlsx' through '5D.xlsx'; inside MOESM8 are 'Kill kinetics Fig 4A.xlsx' and '4C.xlsx';

**Obtainable** YES, downloaded, extracted and parsed. https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs44321-026-00378-9/MediaObjects/44321_2026_378_MOESM9_ESM.zip (33,426 bytes, HTTP 200) and the sibling MOESM7/MOESM8 archives. Also at https://www.ebi.ac.uk/biostudies/studies/S-SCDT-

**Measured N0** YES, verified at row level. Every in vivo sheet (Fig 5A-5D) carries a per-mouse column headed 'BT (before treatment)': Fig 5A lung 1775000, 1242500, 1012500, 1275000; Fig 5B lung 322500, 650000, 310000, 310000; Fig 5C lung 5250000, 9500000, 15700000, 5000000, 12900000, 6000000; Fig 5D spleen 57000, 58000, 49500, 60500, 79000, 240000. In vitro, 'Kill kinetics Fig 4A' row Day 0 gives 2000000, 220000

**Floor** YES — and this is the case the brief anticipated: the in vivo floor is stated as a NUMBER only inside the deposited workbooks and nowhere in the paper. Sheet 'Figure 5' of 'In vivo CFU Fig 5C.xlsx' contains the cell 'L.O.D. was 100CFU'; 'In vivo CFU Fig 5D.xlsx' contains 'L.O.D. was 100 CFU'. Both sit beside the footnote '*L.O.D: limit of detection (Points in figure shows limit of detection for CFU during plating; dotted line)' and the censoring token '0 (below L.O.D)'. I confirmed from the Europe PMC full text of PMC12988230 that the paper itself gives NO number for the organ floor — it says 

**Timepoints** In vitro 'Kill kinetics Fig 4A' and '4C': SIX timepoints — days 0, 5, 10, 15, 20, 30 — in triplicate, four arms (DMSO, Q203 100 nM, PMD 10 microM, PMD+Q203), in two strains (H37Rv and delta-cydAB). 'CFU Nutrient starvation Fig 3B-3E': four further multi-timepoint non-replicating series. In vivo Fig 

**Licence** CC BY 4.0 — confirmed from the creativecommons.org/licenses/by/4.0/ statement in the PMC12988230 record.

**Verdict** QUALIFIES on the in vitro kill kinetics (six timepoints, measured day 0, floor 20 CFU/mL stated in both paper and deposit); the in vivo panels fail the three-timepoint bar at two timepoints each, though they carry a measured per-mouse BT column and a floor. RETURNED WITH A DUPLICATION FLAG, and I am

---

### PZA_PARP1_2023

**Citation** Inhibition of host PARP1 contributes to the anti-inflammatory and antitubercular activity of pyrazinamide. Nat Commun 2023;14. doi:10.1038/s41467-023-43937-1. PMC10710439, PMID 38071218.

**Organism** Mycobacterium tuberculosis H37Rv and the PZA-resistant H37Rv delta-pncA (A146V) mutant; female C3HeB/FeJ mice, and male and female PARP1-null and 129S1 wild-type mice. Aerosol, lung burden.

**Drug** Pyrazinamide 150 mg/kg, rifampicin 10 mg/kg, and the PARP inhibitor talazoparib 0.5 mg/kg, alone and in combination, 5 days/week for 2 months from 1 month post infection.

**Deposit** Journal-hosted Source Data archive 41467_2023_43937_MOESM4_ESM.zip containing 'Source Data.xlsx' (15 sheets, 1,066,596 bytes) and 'Uncropped Western Blots.pdf'.

**Obtainable** YES, downloaded, extracted and parsed. https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-43937-1/MediaObjects/41467_2023_43937_MOESM4_ESM.zip (1,365,600 bytes, HTTP 200). No access request.

**Measured N0** YES, verified at row level, and the sheet is unusually explicit about it. Sheet 'Fig 6' contains three separately labelled CFU blocks in sequence: 'Figure 6 b | CFU - DAY 1 post infection' with per-mouse raw counts (WT: 100, 15*, 60, 95, 110, 95, 85, 105, 80; PARP1-/-: 45, 60, 90, 50, 35, 110, 100, 130) and an annotation '*outlier removed from analysis'; 'Figure 6 c | CFU - Start of treatment' as 

**Floor** NO STATED VALUE — derivable by arithmetic from the Methods only. I swept all 15 sheets: no LOD, no LOQ for CFU, no plated volume in the workbook (the only 'lower limit of detection' strings in the deposit refer to IL-12 and IL-10 multiplex ELISA readings, not to counts). The floor follows from the Methods as the brief describes: lungs placed in 2.5 mL sterile PBS and homogenised, with 0.5 mL plated, so one colony on the undiluted plate equals 5 CFU in the plated portion; and because only section A goes to CFU while the intact-lung and section-B weights are recorded, the whole-lung floor is 5 C

**Timepoints** THREE timepoints in the PARP1-/- experiment (sheet 'Fig 6'): day 1 post-infection, start of treatment at 1 month, end of treatment at 2 months of dosing, across WT and PARP1-/- and untreated versus PZA. Sheet 'Fig 4' adds a six-arm end-of-treatment comparison in C3HeB/FeJ (Vehicle, Tp, PZA, RIF, RIF

**Licence** CC BY 4.0 (Nature Communications open access).

**Verdict** QUALIFIES — confirmed at the bytes. Three explicitly labelled CFU timepoints in one sheet (day 1 / start of treatment / end of treatment), per-mouse and sexed, with a measured implantation count that includes an annotated outlier removal. It meets the three-timepoint bar exactly and no more, and the

---

### RIFAPENTINE_LAI2023

**Citation** Chang HH, et al. "Using Dynamic Oral Dosing of Rifapentine and Rifabutin to Simulate Exposure Profiles of Long-Acting Formulations in a Mouse Model of Tuberculosis Preventive Therapy." Antimicrobial Agents and Chemotherapy 2023. DOI 10.1128/aac.00481-23 (PMC10353356). NOTE: I established the DOI, which the brief did not carry — the supplementary filenames are aac.00481-23-*.

**Organism** Mycobacterium tuberculosis H37Rv AND Mycobacterium bovis rBCG30 (recombinant BCG), co-resident in BALB/c mouse lung and enumerated separately on selective agar. Both organisms are in scope; M. bovis BCG is explicitly on his organism list.

**Drug** Rifapentine and rifabutin under dynamic oral dosing designed to simulate long-acting injectable exposure profiles, plus rifampin and isoniazid (the 1HP/2HP comparator). Rifapentine and high-dose rifamycin exposure are directly in the territory.

**Deposit** Three supplementary workbooks hosted with the article: aac.00481-23-s0002.xlsx (Data File S1, PK in uninfected mice), aac.00481-23-s0003.xlsx (Data File S2, Study 1 CFU+PK), aac.00481-23-s0004.xlsx (Data File S3, Study 2 CFU+PK). The paper's sentence "All individual mouse CFU and PK data and the sta

**Obtainable** YES, and I downloaded and read all three. Direct route that works today: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10353356/supplementaryFiles?includeInlineImage=false (a zip containing all four files, 2.66 MB). The publisher route https://journals.asm.org/doi/suppl/10.1128/aac.00481-23/ s

**Measured N0** YES — measured, per mouse, and better than a single baseline. Sheet 'S3.3. Day 0 CFUs' is captioned verbatim "Data S3.3. Individual mouse CFU data, Day 0 time point (day of treatment initiation)." and gives, for each mouse and each agar type, the raw colony count at each 10-fold dilution plus the derived CFU/lung and log10 CFU/lung. Study 2 additionally carries two pre-Day-0 harvests (sheets 'S3.1

**Floor** 5 CFU/lung, RECOVERABLE FROM INSIDE THE DEPOSIT — this is the case his brief predicted, where the floor is stated in the deposited file and nowhere in the paper. The 'General information' sheet of both CFU workbooks states verbatim, under a heading 'Calculations': "Culture volume was 500 uL per agar plate." and "Shaded cells were used to calculate CFU/lung." and "CFU/lung (x) was log-transformed as log10 (x+1)." The plated fraction is not stated, so I derived it and then verified it: a multiplier of exactly 5 reproduces the deposited CFU/lung from the raw colony count and its dilution. Worked 

**Timepoints** Six CFU timepoints in EACH study, and the earlier judgement that Study 1 is unusable is wrong. Study 1 (Data File S2 / s0003): Week -19, Week -13, Week -7, Day 0, Week 3, Week 3+1.5 days. Study 2 (Data File S3 / s0004): Week -12, Week -6, Day 0, Week 2, Week 4, Week 8. Study 2 arms, read verbatim fr

**Licence** CC BY 4.0. The article carries an American Society for Microbiology / Creative Commons Attribution 4.0 licence statement; copyright 2023 Chang et al.

**Verdict** QUALIFIES, and this is now the strongest deposit in the set — it should be ranked first. It was previously going to be recorded as having NO floor, which would have limited it to whatever part of his argument does not need one; in fact it is one of the very few deposits anywhere that gives RAW PLATE

---

### RUEDAS2025_FIGSHARE

**Citation** Ruedas-López A, López-Roa P, Prados-Rosales R, et al. Infection model of THP-1 cells, growth dynamics, and antimicrobial susceptibility of clinical Mycobacterium abscessus isolates from cystic fibrosis patients: results from a multicentre study. PLoS ONE 2025;20(3):e0319710. PMID 40163512. DOI 10.1371/journal.pone.0319710

**Organism** Mycobacterium abscessus — ATCC reference strain plus 16 smooth and rough clinical isolates from cystic fibrosis patients, inside THP-1 macrophages

**Drug** 

**Deposit** figshare 10.6084/m9.figshare.28398275.v2, 'Data on Fig 4', single file 'Data on Fig 4.xlsx' (12,236 bytes), one worksheet 'Sheet1', 13 rows x 52 columns, two stacked blocks. The other four figshare items are OD600 (28398227), internalisation indices (28398398), THP-1 viability (28398944) and demogra

**Obtainable** YES — direct file at https://ndownloader.figshare.com/files/52298045, no login, CC BY 4.0. I downloaded and opened it.

**Measured N0** YES at the earliest measured point, and I can name the cell. Sheet1 row 3, column A = 2 (hours), with the amikacin-free block's 2 h CFU/mL running across columns B onward: 110000, 90000, 80000 for ATCC; 100000, 120000, 109000 for strain 1; 312000, 292000, 382000 for strain 2; and so on. Row 10 is the same 2 h row for the amikacin block: 81000, 62000, 83000 for ATCC, etc. There is no pre-uptake t =

**Floor** NONE. No LOD anywhere in the deposit or the paper — I searched the PLOS ONE article and no LOD statement exists. The plating sentence gives no volume: verbatim, 'bacterial suspensions and cell debris were serially diluted and plated on Columbia + 5% sheep blood agar plates', so nothing follows by arithmetic either. The only thing the bytes offer is a reporting resolution: all 408 numeric values are exact multiples of 1000 CFU/mL, minimum 6000, maximum 9.8e7. That is a rounding convention, not a detection limit, and he must not report it as one.

**Timepoints** 4 timepoints (2, 24, 48 and 72 hours post-infection) x 17 strains (ATCC plus clinical isolates numbered 1 to 16) x 3 replicates x 2 conditions (amikacin-free, amikacin) = 102 series. The two conditions are stacked in one sheet: rows 1-6 are headed 'Intracellular growth (CFU/mL) of smooth and rough s

**Licence** CC BY 4.0

**Verdict** QUALIFIES, and upgraded — the candidate record's caveat about amikacin being a decontamination step is wrong, and I checked the paper to settle it. Verbatim from the Methods: cells were 'treated or not with amikacin (250 µg/mL) for 1 h. Further, cells were washed again three times in dPBS and subseq

---

### SHEE2026_SENOLYTIC

**Citation** Shee S, Bhattacharya W, Kumar I, et al. Elimination of senescent cells with senolytic drugs as adjunctive host-directed therapy reduces tuberculosis progression in mice. Nat Commun 2026. doi:10.1038/s41467-026-72874-y. PMC13357804, PMID 42098153.

**Organism** Mycobacterium tuberculosis H37Rv; B6.Sst1S, young wild-type C57BL/6 and aged (>72 wk) wild-type C57BL/6 mice, aerosol. Lung AND spleen burden.

**Drug** Senolytic cocktail DQF (dasatinib + quercetin + fisetin) as host-directed therapy, alone and with ethambutol, with a rifampicin lead-in. Deposited arms are Veh, DQF, ETH and DQF+ETH.

**Deposit** Journal-hosted Source Data archive 41467_2026_72874_MOESM10_ESM.zip (22.4 MB, labelled 'source data'), containing 'Source Data File 033026/Source data Fig1-7.xlsx' (31 sheets), 'Source data Supp. Figs.xlsx', and raw microscopy/Western images. NOTE: the prior pass pointed at MOESM4-8; those are Suppl

**Obtainable** YES, downloaded, extracted and parsed. https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-72874-y/MediaObjects/41467_2026_72874_MOESM10_ESM.zip (22,381,646 bytes, HTTP 200). No access request.

**Measured N0** YES, verified at row level, and strikingly low. Sheet 'Fig. 5f' row 'Day 1' gives per-mouse lung counts 8, 13, 11.25, 10, 12 for B6.Sst1S and 112.5, 135, 117.5, 133.75, 133.75 for aged B6 (the young B6 block repeats the latter). Sheet 'Fig. 5b' row 'Day 1' gives 115, 100, 80, 70. These are measured day-1 implantation counts and they sit at or barely above the stated 10 CFU detection limit, which i

**Floor** YES, stated — but the deposit contradicts it, and that contradiction is the useful finding. The Fig. 1 legend states verbatim: 'Square indicates CFU below the limit of detection ( = 10 CFU).' (verified in the Europe PMC full text of PMC13357804). However the deposited sheets encode below-detection values as 1, not 10: sheet 'Fig. 5g' row 'Week 2' contains the literal cells '0(=1)' and sheet 'Fig. 5f' row 'Week 8' contains '0 (1)', with an adjacent note reading 'No CFU detec[ted]'. So the author-stated floor (10 CFU) and the value actually substituted in the data (1) disagree by a factor of ten

**Timepoints** Lung (sheet 'Fig. 5f'): FOUR timepoints — Day 1, Week 2, Week 5, Week 8 — for B6.Sst1S; three for aged B6 (Day 1, Week 2, Week 5). Spleen (sheet 'Fig. 5g'): THREE timepoints — weeks 2, 5, 8. Four arms in each block (Veh, DQF, ETH, DQF+ETH) across three mouse groups (B6.Sst1S, aged B6, young B6), wit

**Licence** CC BY-NC-ND 4.0 — NOT plain CC BY. Confirmed from the creativecommons.org/licenses/by-nc-nd/4.0/ statement in the PMC13357804 record. The NoDerivatives term is a real constraint on republishing transf

**Verdict** QUALIFIES — confirmed, with two corrections. The deposit is in MOESM10, not MOESM4-8. The licence is CC BY-NC-ND 4.0, not CC BY. Its distinctive value is threefold: a host-directed agent given with an antibiotic (a design not otherwise represented), day-1 densities measured at 8-13 CFU that are bare

---

### TABOR2025_MINDTHEGAP

**Citation** Tabor ST, Friesen AD, Reichlen MJ, Dide-Agossou C, McGrath M, Peterson R, Ganusov VV, Robertson GT, Voskuil MI, Walter ND. Mind the gap: Understanding discordance between culture- and a non-culture-based measure of bacterial burden in murine tuberculosis treatment models. bioRxiv, posted 18 December 2025. doi:10.64898/2025.12.18.695164. PMC12724693, PMID 41446251.

**Organism** Mycobacterium tuberculosis; BALB/c mice across the Gates-BC-Rel-01, TBDA-BC-Rel-01 and Crush-TB-Substudy studies plus untreated, single-drug, rebound and in vitro datasets. Lung burden.

**Drug** Nine-plus regimens and single agents: HRZE, BPaMZ, PaMZ, BPaL, BDOS, BPaOS, BZM, BZMRb, PZM, plus single-drug arms including BDQ25, and HRZE.HR continuation with washout.

**Deposit** Two public GitHub repositories. Raw data at https://github.com/SamuelTaborCU/Mtb-16S-rRNA-vs-CFU in DataRaw/ ('Manuscript Datasets.xlsx', 6 sheets; 'Modeling data.csv', 272 rows), with eight R analysis scripts in Code/ and derived outputs in DataProcessed/. Second repository https://github.com/allan

**Obtainable** YES, downloaded and parsed — confirmed at per-mouse granularity, which was the open question. https://raw.githubusercontent.com/SamuelTaborCU/Mtb-16S-rRNA-vs-CFU/main/DataRaw/Manuscript%20Datasets.xlsx (69,418 bytes) and .../DataRaw/Modeling%20data.csv (54,019 bytes), both HTTP 200, no access reques

**Measured N0** YES, verified at row level. A 'PreRx' group is present with Treatment.days = 0 and Days.since.Tx.start = 0, carrying per-mouse CFU values 20600000, 12700000, 20200000 and further rows (20 PreRx rows in Modeling data.csv). These are measured pre-treatment counts, not a nominal inoculum. The untreated sheet separately gives day-7 counts 6300.6, 5850.6, 4950.5.

**Floor** NO STATED VALUE — but derivable from the deposit, and the way it is encoded is itself the point. There IS a column literally named CFU_LOD in Modeling data.csv; I checked all 272 rows and every value is NA. No LOD appears anywhere in the eight R scripts (I grepped for lod, limit of detect, detection limit, censor, floor, plated, dilution: zero hits). Culture.status gives only POSITIVE/NEGATIVE — a flag with no number. However the imputation is transparent: in '3 RMM studies dataset' the 351 culture-negative rows carry exactly one of three values, 1.5, 1.5625 or 1.63, while the smallest positiv

**Timepoints** TWELVE distinct timepoints in Modeling data.csv: Days.since.Tx.start = 0, 7, 14, 21, 28, 42, 56, 70, 84, 98, 112, 140, spanning on-treatment and post-treatment follow-up. Six sheets: Untreated mice (25 rows), Single drug (67), Multi drugs regimen (297), Rebound (125, with washout period recorded per

**Licence** NO REUSE GRANT — this is a downgrade and it matters. The bioRxiv posting carries the most restrictive option: 'The copyright holder for this preprint is the author/funder, who has granted bioRxiv a li

**Verdict** QUALIFIES on data, measured N0 and timepoints — promoted from NEEDS A LOOK, and it is the richest single deposit in this set by row count and by timepoint span. But two caveats to carry: (1) the licence position is 'all rights reserved' plus unlicensed repositories, so plan to request permission rat

---

### TBM_ETO_2026

**Citation** Chen X, Ruiz-Gonzalez CE, Masias-Leon Y, Singh M, Shambles M, Peloquin CA, Jain SK. Ethionamide versus ethambutol-containing first-line regimens for TB meningitis. Antimicrob Agents Chemother 2026. doi:10.1128/aac.00190-26. PMC13336335, PMID 42294653.

**Organism** Mycobacterium tuberculosis H37Rv; female C3HeB/FeJ mice, intracranial inoculation via burr hole. Whole-brain AND whole-lung burden as log10 CFU/g.

**Drug** HRZ (isoniazid 10, rifampin 10, pyrazinamide 150 mg/kg/day), HRZE (+ ethambutol 100 mg/kg/day) and HRZEt (+ ethionamide 50 mg/kg/day), 5 days/week with adjunctive dexamethasone 2 mg/kg/day.

**Deposit** ASM journal-hosted supplemental file aac.00190-26-s0001.xlsx, captioned 'Source data', 8 sheets. Supplemental methods and figures in aac.00190-26-s0002.docx.

**Obtainable** YES — obtainable, though NOT from the publisher directly. journals.asm.org returned HTTP 403 for both files from this environment. Both come down cleanly from the Europe PMC mirror: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13336335/supplementaryFiles returns a 670,628-byte zip containing 

**Measured N0** YES, verified at row level — this was the open question and it resolves affirmatively. Sheets 'Figure S1A' (brain) and 'Figure S1B' (lung) carry a leading time column reading 0, 2, 6 (weeks). The row at time 0 holds per-animal log10 CFU/g: brain 6.50168945, 6.50776359, 6.67330801, 6.46953603, 6.32176073, 6.65068649; lung 4.46597389, 5.25701317, 5.6414905, 4.82896046, 4.47538754, 4.89440203. Six an

**Floor** NONE. I extracted the full text of the supplemental methods docx and searched it: it contains the animal infection paragraph, neuroinflammation assays and the statistical analysis paragraph, but NO limit of detection, NO plated volume, NO homogenate volume and NO organ fraction. The main text gives lower limits of quantification only for the drug assays (0.05 microgram/mL ethambutol, 0.1 microgram/mL ethionamide), not for counts. In the deposited lung sheets the censoring value is a bare 0, used heavily at week 6 (e.g. the HRZE week-6 column reads 1.747, 0, 2.345, 0, 0, 0, 0, 0). A flag with n

**Timepoints** THREE timepoints — week 0 (treatment start), week 2 and week 6 — in sheets 'Figure S1A' and 'Figure S1B'. EIGHT series: four arms (Untreated, HRZ, HRZE, HRZEt) times two organs (brain, lung), with 6-13 animals per group per timepoint; the untreated arm runs to week 2 only. Sheets 'Figure 1B' and 'Fi

**Licence** Open access under a Creative Commons licence (the PMC copy carries a CC statement; ASM permissions govern the supplemental material).

**Verdict** QUALIFIES on data, measured N0 and timepoints — promoted from NEEDS A LOOK; FAILS on floor, now confirmed rather than assumed. What it adds that nothing else here does is the CNS compartment: brain burden alongside lung, in the same animals, under three closely related first-line regimens. The lung 

---

### WALL2025_BC1

**Citation** Wall RJ, Lamprecht DA, et al. The role of cytochrome bc1 inhibitors in future tuberculosis treatment regimens. Nat Commun 2025. doi:10.1038/s41467-025-64427-6. PMC12546632, PMID 41125580.

**Organism** Mycobacterium tuberculosis H37Rv, Erdman and clinical isolate N1283; mice across six studies at six institutions (Evotec Toulouse, Sorbonne, Johns Hopkins, Colorado State, LSHTM). Lung burden.

**Drug** Bedaquiline, pretomanid, clofazimine, linezolid, moxifloxacin, pyrazinamide, rifampicin, isoniazid, ethambutol, telacebec, and the novel cytochrome bc1 inhibitors JNJ-2901 and JNJ-4052, in regimens BPaL, BPaM, BPaMJ, BPaMZ, BPaC, BPaCJ, BPaLJ, BPaLM, RHZ, CZ, CZT, BCZ, BCZT, HRZE.

**Deposit** Journal-hosted Source Data workbook 41467_2025_64427_MOESM6_ESM.xlsx (14 sheets) plus Supplementary Data 1 as 41467_2025_64427_MOESM3_ESM.xlsx, both at nature.com under the article DOI.

**Obtainable** YES, downloaded and parsed. https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-64427-6/MediaObjects/41467_2025_64427_MOESM6_ESM.xlsx (38,852 bytes, HTTP 200). No access request.

**Measured N0** YES, verified at row level, and measured TWICE per study. The sheets carry explicit pre-treatment columns by name: 'Supp. Table 4' has 'Day -13' (4.46, 4.63, 4.56, 4.25, 4.39...) and 'Day 0' (7.16, 7.19, 7.45, 7.40, 6.95...); 'Supp. Table 12' and the 'Fig. 2' sheet have 'Day -10' (4.13, 4.20, 4.15, 4.34, 4.17) and 'Day 0' (7.05, 7.03, 6.93, 7.03, 7.03); 'Supp. Table 8' has 'day-13' and 'day 0'; 'S

**Floor** YES — stated numerically AND present as the literal censoring value in the deposit. The Fig. 2 legend reads verbatim: 'Limit of detection (dotted line) was 0.4 log10 CFU lung-1' (verified in the Europe PMC full text of PMC12546632). In the deposited 'Fig. 2' and 'Supp. Table 12' sheets the value 0.4 recurs as the floor across the CQZ, BCZ and BCZQ columns exactly as the legend describes. Note the convention is NOT uniform across sites: 'Supp. Table 4' and 'Supp. Table 11' use 0 as the censored value, and 'Supp. Table 11' also contains recurring values 0.3521825181113625 (= log10 2.25) and 0.54

**Timepoints** 'Supp. Table 4': FIVE timepoints — Day -13, Day 0, 4 wk, 8 wk, and 8 wk + 12 wk relapse — across six regimens (BPaL, BPaM, BPaMJ, BPaMZ, BPaC, BPaCJ), 20 columns. 'Supp. Table 11': SEVEN timepoints — -2 wks, Day 0, 2 wks, BPaL 8 wks, 12 wks, 16 wks, 16 wks + 16 wks — across four continuation arms (B

**Licence** CC BY 4.0 — confirmed from the creativecommons.org/licenses/by/4.0/ statement in the PMC12546632 record.

**Verdict** QUALIFIES — confirmed at the bytes, and it remains the best in vivo record in this set. Deposited per-mouse numeric data, two measured pre-treatment densities per study, an author-stated floor that appears as the actual censoring value in the data, up to seven timepoints including post-treatment rel

---

### WALLER2023

**Citation** Waller NJE, Cheung C-Y, Cook GM, McNeil MB. Waller et al_2023_Collateral TB_Source Data.xlsx. figshare, 2023. doi:10.6084/m9.figshare.22152056.v2. Source data for: The evolution of antibiotic resistance is associated with collateral drug phenotypes in Mycobacterium tuberculosis. Nat Commun 2023;14:1517. doi:10.1038/s41467-023-37184-7 (PMID 36934122, PMC10024696).

**Organism** Mycobacterium tuberculosis mc2 6206 (auxotrophic H37Rv derivative), plus isogenic drug-resistant mutants (INH-1, AZ7-11, KAN-32, STRP-8, Q203-1) and CRISPRi knockdown strains (FbiA, FbiB, FbiC, FbiD, Ddn, Fgd1, Rv0965c)

**Drug** Isoniazid, bedaquiline, Q203/telacebec, pretomanid (PA824), thioacetazone, clofazimine, rifampicin, levofloxacin, linezolid, kanamycin, streptomycin, capreomycin, nitrofurantoin, TB47 — singly and as INH 9x MIC plus a sub-inhibitory (0.3x MIC) partner

**Deposit** figshare (standalone deposit, not a journal-hosted supplement)

**Obtainable** YES, no access request. Record https://figshare.com/articles/dataset/22152056 ; direct file https://ndownloader.figshare.com/files/39444559 (69,198 bytes, one .xlsx, 11 worksheets). Downloaded and parsed from raw XML; all values below were read out of the cells.

**Measured N0** YES, and confirmed as measured by the paper's own Methods. Sheet 'Figure 6' block A/B/C/D, row 'Time (days)' = 0 carries per-series counts: 50000, 31000, 71000, 60000, 26000, 60000, 42000, 32000, 116666.7, 41000, 43000, 31000, 21000, 90000, 50000, 50000, 32000, 20000, 37000. Blocks E-H carry their own day-0 rows (800000/800000/600000/200000; 80000/60000/140000/60000; 400000/800000/600000/180000; 2

**Floor** 200 CFU/mL. DERIVED, not author-stated, but from a Methods-stated plated volume and corroborated three independent ways. Methods (PMC10024696): 'The transferred samples were diluted along a 3-point, 10-fold dilution curve in 7H9 with pantothenic acid and leucine. 5 uL of each dilution was spotted onto 7H11 supplemented with OADC, leucine and pantothenate acid.' A 5 uL spot reported per mL gives 200 CFU/mL. The time-kill Methods route back to the same procedure: 'Culture was removed on stated days to measure OD as well as diluted and spotted as described above for MBC to determine the number of

**Timepoints** Substantially more than previously reported. Sheet 'Figure 6' holds SIX time-course blocks, not one. Block A/B/C/D: 9 timepoints (days 0, 4, 7, 10, 14, 21, 28, 35, 42) x 10 arms x 2 replicates = 20 series, ragged at the tail (several arms stop at day 21/28/35). Block E: 6 timepoints (0, 3, 7, 10, 14

**Licence** CC BY 4.0

**Verdict** QUALIFIES, and ranks first. All three criteria met. The reason it leads the field is not merely that it passes: it is censored at both the floor (runs of 200 sustained from day 14 to day 42 in single replicates while the paired replicate regrows) and the ceiling (2e7), across 42 days and ten drugs i

---

### WALTER2021_RSRATIO

**Citation** Walter ND, Born SEM, Robertson GT, Reichlen M, Dide-Agossou C, Ektnitphong VA, et al. Mycobacterium tuberculosis precursor rRNA as a measure of treatment-shortening activity of drugs and regimens. Nat Commun 2021;12:2899. doi:10.1038/s41467-021-22833-6. PMC8131613. Gates Foundation OPP1213947; NIH 1R21AI135652-01; Veterans Affairs.

**Organism** M. tuberculosis in axenic 7H9 culture; M. tuberculosis in BALB/c mouse lung (high-dose aerosol efficacy model and the relapsing mouse model); C3HeB/FeJ mouse lung for the imaging arm.

**Drug** In vitro: rifampin, isoniazid, streptomycin, ethambutol, bedaquiline, untreated control. Mouse monotherapy: EMB 100, INH 25, STR 200, PZA 150, RIF 10, RIF 30, PZA 150 + RIF 10, BDQ 5, BDQ 25 mg/kg. Relapsing mouse: 2HRZE/3HR, PaMZ, BPaL, BPaMZ, untreated.

**Deposit** Source Data file 41467_2021_22833_MOESM4_ESM.xlsx, 61,147 bytes, 10 sheets (the previous pass said nine; there are ten). CFU sheets: 'Fig 3a-e & Sup Fig 5', 'Sup Fig 5g-j', 'Fig 4a-c & Sup Fig 7-8', 'Sup Fig 8b', 'Fig 5a-d & Sup Fig 9-10', 'Sup Fig 11', 'Fig 1c & Sup Fig 1b'. The floors are NOT in t

**Obtainable** YES, no access request. https://doi.org/10.1038/s41467-021-22833-6 -> Source Data; whole bundle at https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8131613/supplementaryFiles (3,427,391 bytes, 16 files).

**Measured N0** YES, everywhere. In vitro sheet 'Fig 3a-e & Sup Fig 5' has explicit Treatment-days-0 rows per Set: Control 7.674861140737812, 7.598790506763115, 7.594392550375427, 7.513217600067939 log10 CFU per mL. Mouse sheet 'Fig 4a-c & Sup Fig 7-8' carries two measured baselines — a 'Day 1 post infection' group (3.40654018, 4.306425028, 3.77815125 log10 CFU per lung) and a 'Pre-Rx' group at treatment day 11 (

**Floor** STATED, BOTH COMPARTMENTS — this is the upgrade, and the previous pass was wrong to record no number. IN VITRO, 13 CFU/mL: Supplementary Information PDF, legend to Supplementary Fig. 5 g-j ('Total plateable bacteria (black lines) and resistant bacteria (red lines with fill) over time in cultures treated with g, rifampin h, bedaquiline i, isoniazid, and j, streptomycin ... The dashed line represents the limit of detection (13 CFU ml-1).'). Those panels are exactly the deposited 'CFU per mL (log10)' series. IN VIVO, 2.18 log10 CFU: same PDF, legend to Supplementary Fig. 8a ('Drug resistant CFU a

**Timepoints** IN VITRO 'Fig 3a-e & Sup Fig 5': 133 CFU values, treatment days 0, 0.25, 1, 2, 3, 4, 8 for all six arms plus 12 and 20 for a subset — 7 to 9 timepoints; arms Control, RIF, INH, STR, EMB, BDQ; multiple independent Sets per arm; CFU per mL (log10) ranges 4.23 to 8.30, so the series never approaches th

**Licence** CC BY 4.0 (Creative Commons Attribution 4.0 International, licence URL in the article XML).

**Verdict** QUALIFIES. Open CC BY Source Data, genuine multi-timepoint viable counts in vitro (up to 9 points) and in vivo (up to 11 points in the relapsing model), measured baselines throughout, and author-stated numeric floors for both compartments — found only in the supplementary PDF, which is itself a poin

---

### YANG2024_PHAGE

**Citation** Yang F, Labani-Motlagh A, Bohorquez JA, et al. Source data for 'Bacteriophage therapy for the treatment of Mycobacterium tuberculosis infections in humanized mice'. figshare, 2024. doi:10.6084/m9.figshare.25254571.v1. Paper: Commun Biol 2024;7:294. doi:10.1038/s42003-024-06006-x (PMID 38461214, PMC10924958).

**Organism** Mycobacterium tuberculosis H37Rv and H37Rv-GFP; 7H9 broth, primary human monocyte-derived macrophages from five donors, and humanized NSG-SGM3 mouse lung and spleen

**Drug** Mycobacteriophages DS6A, D29 and Chah (Chah as non-killing control) at MOI 1, plus a D29 MOI 1/10/100 series. NO chemical antibiotic anywhere in the study — macrophage cultures are explicitly maintained 'in the absence of antibiotic'.

**Deposit** figshare (standalone source-data deposit, cited in the paper's Statistics and reproducibility section)

**Obtainable** YES, no access request. Record https://figshare.com/articles/dataset/25254571 ; 15 GraphPad Prism .pzfx files. Fig 1d https://ndownloader.figshare.com/files/44617477 (18,932 bytes); Fig 2b /44617480 (8,648); Fig 2d /44617483 (47,687); Fig 3c /44617444 (6,578); Fig 4c lung /44617447 (15,655); Fig 4c 

**Measured N0** YES, but for one panel only. Fig 1d row 'Day 0' carries 101250, 168750, 168750 CFU/mL, repeated identically across all four arms because they share one inoculum. The non-round values indicate counting rather than the nominal 1e5 of the Methods. Fig 2d has a 'Day 0' row populated for the 'Mtb Control' arm only (6400, 2870, then two empty cells) and EMPTY for both 'Mtb + BPS' and 'Mtb + DS-6A' — so 

**Floor** 100 CFU/mL. DERIVED from a Methods-stated plated volume, and — importantly — NOT visible anywhere in the deposited data. Methods (PMC10924958): 'At days 3, 6, and 9, 10 uL of 10-fold serial dilutions of the culture were plated on 7H10 agar plates, and CFU were counted after cultured at 37 C for 2-3 weeks.' A 10 uL spot reported per mL gives 100 CFU/mL. The macrophage assay uses the same volume: 'After making dilutions, 10 uL of cellular lysate was plated on 7H10 agar plates in duplicates.' The caution is that the deposit records censored points as hard 0 rather than as the floor — Fig 1d DS6A 

**Timepoints** DOWNGRADED from the previous pass, which overstated this. The only qualifying viable-count time course in the whole deposit is Fig 1d: 4 timepoints (Day 0, 3, 6, 9) x 4 arms (Ctrl, D29, Chah, DS6A) x 3 replicates = 12 series, 9 days of follow-up. Fig 2b as deposited is a TwoWay table with row titles

**Licence** CC BY 4.0

**Verdict** QUALIFIES ON THE MECHANICS, BUT FLAG THE EXPOSURE AND EXPECT LESS THAN ADVERTISED. It clears all three criteria — measured t0, a floor derivable from a stated 10 uL volume, and 4 timepoints x 12 series — but only through the single Fig 1d panel, and I have had to cut the earlier claim that Fig 2b an

---

### ZAINABADI_JID2024

**Citation** Zainabadi K, Walsh KF, Vilbrun SC, et al., Fitzgerald DW, Ocheretina O. A Bedaquiline, Pyrazinamide, Levofloxacin, Linezolid, and Clofazimine Second-line Regimen for Tuberculosis Displays Similar Early Bactericidal Activity as the Standard Rifampin-Based First-line Regimen. J Infect Dis 2024;230(2):e447. PMID 38060827, PMC11326837, DOI 10.1093/infdis/jiad564. Floor sourced from the paper its Metho

**Organism** Mycobacterium tuberculosis in overnight sputum from 31 adults with drug-susceptible and 23 with drug-resistant pulmonary TB, GHESKIO Centers, Port-au-Prince, Haiti (human in vivo)

**Drug** Second line: bedaquiline + pyrazinamide + levofloxacin + linezolid + clofazimine (DR-TB cohort). First line: rifampin + isoniazid + ethambutol + pyrazinamide (DS-TB cohort). The bedaquiline/linezolid/clofazimine combination in humans is not represented anywhere else in this territory.

**Deposit** Supplementary archive attached to the article, no repository record. Reachable as: Europe PMC supplementaryFiles bundle for PMC11326837 -> jiad564_supplementary_data.zip (125,372 bytes) -> two files: 'Table S1.xlsx' (85,752 bytes) and 'Supp Tables 2-12 (CLEAN) 11-20-2023.docx' (48,154 bytes). Table 

**Obtainable** YES, once you know where to look. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11326837/supplementaryFiles returns the whole bundle (454,804 bytes) with no registration and no request; the inner jiad564_supplementary_data.zip is inside it. Also linked from the article page at https://academic

**Measured N0** YES. Sheet 'ALL (DS + DR)', row 1 group header 'Day 0 Culture' spanning columns 66-70, row 2 sub-headers 'CFU', 'MPN-CF', 'MPN+CF', 'Mtb Max', 'TTP'; one row per patient, 54 patients. Day 0 CFU is numeric in 52 of 54 (min 420, max 7.6e7 Mtb/mL); Day 0 MPN-CF in 53, MPN+CF in 52, Mtb Max in 53, TTP in 53. The units are Mtb per mL of sputum — the supplementary docx repeatedly labels the derived quan

**Floor** YES, with a value, and the deposited data confirm the code. The JID Methods delegate wholesale — 'Decontamination of sputum, preparation of culture filtrate (CF), and colony-forming unit (CFU), limiting dilution (LD), and BACTEC MGIT assays were conducted as previously reported' — and state no LOD, no plated volume; the supplementary workbook and docx state none either (I searched the docx for limit of detection / LOD / LOQ / plated / mL / dilut / below / undetect and found only the units labels, and the only footnote-like rows in the workbook are 'R = resistant / S = sensitive / I = indetermi

**Timepoints** Three timepoints — Day 0 (pre-treatment), Week 2, Month 2 — which is exactly the stated minimum. Five parallel readouts at each: CFU, MPN-CF, MPN+CF, Mtb Max, TTP. 54 patient-level series on the 'ALL (DS + DR)' sheet. Completeness: Day 0 CFU numeric in 52, Week 2 in 45, Month 2 in 35 (one 'contam');

**Licence** Not stated in the deposit. The article is in PMC as an author manuscript / OUP supplementary material; the supplementary bundle carries no licence file. Treat as article-supplementary terms and check 

**Verdict** QUALIFIES, rank it second. Upgraded from NEEDS A LOOK: the archive opened, the CFU columns are real and per mL, the measured Day 0 is per patient, and the floor now has a number (3 Mtb/mL) traceable to the methods paper the article delegates to, corroborated by the substituted 2 sitting in the data.

---

## Assessed and not taken (126)

| id | reason |
| --- | --- |
| AAC2026_FORGIVENESS | NO — data not obtainable; figure digitisation would be required, which the brief excludes. Returned because it is the best-designed murine time course |
| AGNO3_MABS2025 | NO — rejected, and now firmly rather than provisionally. As deposited and as designed, the CFU data are a four-level dose-response read at a single te |
| ALLEN2023_MABS_PHAGE | NO — the treated series carry only two timepoints (day 0 and day 2), short of the three-timepoint minimum, and the only series with 4 timepoints has n |
| ANKOMAH_MARINUM | NO — the deposit is figures and two unreadable legacy .doc tables; the kill curves are undeposited main-text figures. Worth naming because this is one |
| APRAMYCIN_MABS_JAC2026 | NO — rejected on access, with no measured N0 and no numeric floor either. Flagged here mainly so it is not confused with the catalogued apramycin figs |
| AVIUM2026_SEQMONO | REJECT, on obtainability. The design is genuinely the best-suited in the whole set for his purpose — five timepoints including two measured pre-treatm |
| BATES2026_ELIFE_MABS | NO — kill curves are figure-only. Worth naming because it is a 2026 eLife paper squarely in the tolerance territory (Stanley and Penn labs) and becaus |
| BC1_2025 | NEEDS A LOOK, and I am UNSURE whether it duplicates his manifest. His already-catalogued list mentions 'a pretomanid/Q203 dataset' and includes PRETOM |
| BDQ_PBIO_MOUSE | NO — two timepoints, short of the three-timepoint minimum, and no detection floor. A clean, small rejection. |
| BDQ_RES_PLOS2014 | NO — rejected because the supporting information is a figure, not deposited values. Textbook case of a "data fully available without restriction" stat |
| BGA_TBA7371_MOUSE2024 | NO — rejected on access; the supplement carries dose-ranging and PK/PD, not per-animal CFU. |
| BLONDIAUX2017_DRYAD_SMART420 | NO — wrong readout. The second of the two mycobacterial 'antibiotic resistance' deposits in Dryad that turn out to be sequencing. |
| BLONDIAUX2017_SMART420 | NO — sequencing data only. The mouse CFU data in the paper were not deposited. Explicit rejection. |
| BOSCH2026_CASEUM | DOWNGRADED to a qualified accept, and the scope question resolves itself. The ex vivo rabbit caseum killing series is NOT deposited as raw counts: Sou |
| BTZ043_2025 | NEEDS A LOOK, unchanged, and now for a firmer reason. The data are open, CC BY, per-mouse and raw, and sheet '1a&b' is a real 4-point-per-arm dose-res |
| BTZ043_C3HEB2023 | REJECT — the claim that Supplementary Tables S1-S3 hold the CFU data is false, and I established this by reading the file rather than by failing to re |
| BTZ043_PPCA_CODE | NO — code without data. Returned because it is a textbook example of the pattern the paper is documenting: the analysis is reproducible in form and ir |
| CHENGALROYEN2022_DCTB | NO — no numeric deposit. This is the single biggest loss in my territory: seven timepoints, four parallel viability readouts on the same specimens, 80 |
| CHUNG2026_ZENODO_ALDRIDGE | NO — the exposure (ethambutol) and the organism are in scope, and the deposit is exemplary in every other way, but the readout is a survival fraction  |
| CPTR_RMM_AAC2022 | NO, on two counts: the readout is a binary relapse indicator rather than viable counts at three or more timepoints, and the pooled data are not public |
| CPTR_RMM_DATABASE | NO — the data are not publicly deposited. Returned deliberately, because a rejection with a stated reason is the point. This is the single most import |
| CTGOV_EBA_RESULTS | NO — fails the three-timepoints test as a class. I checked two independently and both behave the same way, so I am rejecting the whole ClinicalTrials. |
| DARTOIS2025_PNAS_RIFAMYCINS | NO, and the candidate's lean was right. I opened Dataset S01, S02 and S03 and none contains a time series — they are chemistry/MIC, pharmacokinetics,  |
| DATAINBRIEF_SWEEP | NO — reportable negative. Data in Brief, the journal whose entire purpose is publishing datasets, has never published a mycobacterial CFU time-kill da |
| DAY2026_ZENODO_MACROHET | NO, on the readout criterion. Resolved rather than left open: the deposit measures intracellular Mtb by fluorescent AREA per macrophage from live-cell |
| DBLTEAM_DMP | NO — a plan, not a deposit. Returned for two reasons: it is the only non-tuberculous mycobacterial human EBA record my sweep surfaced, and it tells Va |
| DCTB_DRTB_2022 | NO as a deposit, but return it: MPN is an in-scope readout, the design has 3+ timepoints, and the group is the main source of human MPN time-course da |
| DEJAGER_RIF_EBA_2025 | NO — no deposit. Recorded because it is the most recent large EBA trial with paired CFU and TTP, and a referee may well ask whether the search reached |
| DIAMOND_TB10 | NO — rejected, and now on direct inspection rather than inference. It fails the readout criterion outright: the deposit contains dose-response and int |
| DRYAD_MYCO_SWEEP | NO — and this is a reportable negative. Apart from the two records handled separately above (dryad.kd8cj and dryad.t1g1jwt8h), Dryad holds no mycobact |
| DRYAD_PROANO2018_COUGH | NO — rejected on readout, and the deposit's own record says so. The landing page states verbatim: 'Sputum samples (n=426) were tested with microscopic |
| DRYAD_PROANO2019_CAVITY | NO — rejected on readout, same reason and same source as its sibling. The landing page states that 'sputum samples were evaluated using microscopic-ob |
| ELIFE2024_BPAS | NO — fewer than three timepoints. Rejected on the readout requirement, not on access. Returned because it is the clearest case of the pattern I kept h |
| EPETRA_HFS_TB2025 | NO — fails on access, and additionally lacks both a measured N0 and a floor. |
| ERA4TB_GSK286_2026 | NO — data not obtainable. Painful, because it is the one paper in the territory that states its floor as an unambiguous number in a figure legend (400 |
| ERA4TB_STAR_2025 | NO as a dataset — no new deposit, and it points to a manifest entry he already has. Returned because it is the citable source for the 2.6 log10 CFU/mL |
| ERA4TB_TBAJ587_2026 | NO — data not obtainable. A 9-timepoint, 108-condition ERA4TB time-kill with paired drug measurement, and none of the counts are deposited; only the W |
| FEILCKE2025_MABS_LOP | NO — figure-only, no deposit and no data availability statement. Named because it is a current, purpose-built hypoxic non-replicating mycobacterial ki |
| FLUOROPHORE_PERSISTER | NO — microscopy image archives, not viable-count tables. Recording the rejection because these records rank high on 'mycobacteria AND persister' searc |
| FRONTIERS_HFIM_SET | NO for all six — these are supplementary figure files, not data. This matters for the completeness claim: the hollow-fibre M. abscessus and M. tubercu |
| GANFEBOROLE_NATMED2024 | NO — no deposit. Included because a Nature Medicine phase 2a EBA trial is exactly where one would expect a Source Data file, and there isn't one; that |
| GATESOPEN_MGIA | NO — fails both the exposure test (no antimicrobial) and the three-timepoint test. Recorded because the Gates Open Access repository was named in the  |
| GSK286_AAC2026 | NO — fails on access alone. Everything else about it is exactly what he wants (measured day-0, a stated numeric quantification floor, six to eight tim |
| HASENOEHRL2019_ASPARTATE | NO on scope, not on access. The exposure is conditional gene silencing (tetracycline/anhydrotetracycline Dual-Control system), with doxycycline acting |
| HFSTB_JAC2023_CPTR | NO — data not obtainable. Content-wise this is close to ideal for him (three teams, nine experiments, five-plus timepoints, three metabolic states, an |
| HFS_MABS_SYSREV2026 | REJECT — the highest-value unresolved lead in the previous pass, and it collapses on inspection. The hoped-for prize was an author-digitised CFU-versu |
| HFS_TOOLKIT_ISCI2026 | NO — this is a drug-fibre adsorption/compatibility study with no organism and no CFU at all. It surfaces high in every hollow-fibre search (the widely |
| JOVANOVIC_ASCT_ALREADY_HELD | NO — already catalogued as JOVANOVIC2026. Recorded here only so the search log shows it was encountered twice (once as the 2024 bioRxiv preprint, once |
| KREUTZFELDT2022_CINA | NO — figure-only. This is the flagship Schnappinger/Ehrt multidrug-tolerance paper and the single most conspicuous absence from the deposited record i |
| LAMPRECHT2025_NATURE_PURINE | NO — the released source data does not cover the CFU panels, and the drug-exposure CFU arms are endpoints rather than three-or-more-timepoint series.  |
| LAM_NEXGEN_4COHORT | NO as a deposit, but flagged prominently: NexGen EBA is probably the largest single human serial-CFU dataset of the modern era (178 patients, daily sp |
| LODHIYA2026_ELIFE_ATP | NO — figure-only. Named because it is a 2026 eLife mycobacterial killing-mechanism paper with over 20 figures and source data released only for the om |
| LOUIE2026_PLOSONE_COMBINATIONS | NO — figure-only despite a PLOS mandatory data availability statement. Named because it is the Drusano/Louie group's current combination paper and DRU |
| MABS_MOUSE_MODELS2025 | NO — rejected on access. Six timepoints and a properly stated floor, but nothing deposited and no measured day-0 count; only the nominal inoculum. |
| MABS_POTASSIUM_STARVATION_2025 | NO — out of scope on exposure. The paper does not treat with any antibiotic. Its only antibiotic content is a review sentence about other studies, ver |
| MABS_ROS_ELIFE2026 | NO, and worth writing down precisely because of why. This is a CC BY paper in a journal with a mandatory data policy, whose data availability statemen |
| MACROPHAGE_TOL2025 | NO — rejected on access. Included because it covers eight of my listed drugs in one intracellular assay and has a properly staged pre-treatment count, |
| MALAWI_HIV_CLEARANCE | NO as a deposit, but this is the second-best email to write after PanACEA. Six timepoints, 118 participants, real colony counts, and a smear-negative  |
| MARCH2025_AAC | NO. I opened Data S1 and it contains no CFU column at all. The 'Experimental_Data' sheet's ten columns are Strain, Lineage, SubLineage, BDQ MDK95, BDQ |
| MATERN2021_MAVIUM | NO — three timepoints and a derivable floor, but the CFU numbers are in a supplemental figure and the only deposit is sequencing plus analysis code. N |
| MAVIUM_CHRONIC_MOUSE2025 | NO — rejected on access. Five timepoints and a measured baseline harvest, but the only supplementary file is the statistical analysis rather than the  |
| MAVIUM_HFS_BDQ2025 | REJECT — resolved from 'needs a look' by opening the docx, which was the single check the previous pass could not perform. All 22 tables are PK parame |
| MBLA_UCL2022 | NO — rejected, and the earlier suspicion that the design might hide more sampling occasions is now ruled out rather than left open. It fails criterion |
| MBX4132 | NO — the deposited workbooks are transcriptomics and transposon-fitness data. The paper's kill curves are figures only. |
| MCAULAY2018_MBIO | NO — rejected on the timepoint rule, and only on that. It is human, open, per-mL, with a measured baseline and an explicitly stated floor of 3 Mtb/mL, |
| MISTRETTA2024_NC | NO, on criterion 1 and criterion 2 together. The starting density is normalised to 10^7 by the authors' own statement and every series in every CFU sh |
| MTB_RIF_STM_SCIREP2025 | NO — the deposit is sequence reads, not CFU. Another instance of the pattern where a paper deposits the omics and leaves the viable counts in figures. |
| NANDAKUMAR2014_DRYAD_ICL | NO — wrong readout. A title-level false positive for anyone searching Dryad for mycobacterial tolerance; worth naming for that reason, since it is one |
| NANDAKUMAR2014_ICL | NO — the deposit contains only metabolomic profiling. The paper's CFU survival curves exist but were never deposited; they would have to be digitised  |
| NOLAN2026_HONEY | NO — the readout is optical density, not viable counts. This is a textbook example of a deposit that says 'time-kill' in its own description and conta |
| OSF_SWEEP | NO — and a reportable negative. Title searches on OSF nodes and registrations for 'tuberculosis', 'mycobacter', 'abscessus', 'time-kill' and 'time kil |
| PANACEA_HIGHRIF1 | NO as a deposit — it is not obtainable — but it is the highest-value email to write. It is the one human dataset in this territory that has serial CFU |
| PA_VS_DLM_MOUSE2026 | NO — rejected on access only. It satisfies both of his other tests (measured 6.83 log10 CFU baseline; a numeric floor of <0.83 log10 CFU) and is the c |
| PEM2026_PERSISTER_ENRICHMENT | NO — no numeric deposit. A prominent 2026 persistence paper with a 2–4 log tolerance effect and nothing behind the figures but an SRA accession (and a |
| PENN_MABS2026 | NEEDS A LOOK — but downgraded from the previous read, because obtainability is now positively disconfirmed rather than merely unproven. Five URL forms |
| PETERSON2023_MTRA | NO — the deposit exists but holds code and Tn-seq, not viable counts. Named because a Zenodo DOI in the resources table can look like a data deposit a |
| PHAGE_MABS_DRYAD2024 | NEEDS A LOOK, and the question is scope rather than quality. As a deposit it is close to exemplary: public, CC0, file-level, checksummed, with a READM |
| PHUA2025_MENDELEY | NO — the 'dataset' is the manuscript and its SI PDF, not data. The CFU values would have to be digitised. A good cautionary example for the search-str |
| PLOSBIO_OSF2021 | NO — the OSF deposit is real but contains the screening data, not the kill-curve CFU; and there is no measured N0 and no floor. A good example of a de |
| PPAT1013924 | NO — wrong organism. Included because it is the top hit for 'log10 CFU' plus weekly time course in the repository indexes and will recur in anyone's s |
| PREDICTTB | NO — fails the readout test and is gated. Named because PredictTB is the obvious 'treatment response bacteriology' trial to check in this territory, a |
| PREDICTTB_PROGRAMME | NO — no public deposit located. Recording it explicitly so the search strategy shows the programme was looked for and came up empty rather than being  |
| PYRAZOLE2025 | NO — the time-kill result exists only as a figure in the paper; the deposit is synthetic chemistry supporting information. Digitisation would be requi |
| Q203_MAVIUM2026 | REJECT — decisively, and on two independent grounds that only opening the files could establish. First, the in vitro arm is not a kill curve at all: I |
| RABODOARIVELO2025_STAR | NO — duplicate of an already-catalogued deposit (ERA4TB figshare 19766083). But keep the citation: it is the formal protocol behind the 2.5 µL plating |
| REJECTED_NO_DEPOSIT_SET | NO — data not obtainable. Returned as a group to document that the NTM and guinea pig corners of this territory were searched and are empty of deposit |
| REJECTED_SINGLE_TIMEPOINT_SET | NO — fewer than three viable-count timepoints in vivo. Grouped and returned together because they document the commonest failure mode in this territor |
| REPOSITORY_SWEEP_NEGATIVE | NO — the general repositories are effectively empty for this territory, and that is a reportable finding. ZENODO: seven queries returned only mirrored |
| RESEQTB | NO — wrong data type entirely. No killing over time, no counts. Recorded as a stated rejection so the platform is visibly covered. |
| RESPIRI_TB_NTM | NO — no deposits. Recorded so the two NTM-facing AMR Accelerator projects are visibly covered; note that these are the natural place to look for M. ab |
| RIF_BDQ_PKPD_MICE2022 | NO — rejected on access. Worth naming because the high-dose rifampicin dose-ranging series is otherwise unrepresented and this is the closest deposite |
| SARATHY2025_MABS_ORAL | NO — figure-only. Named because it is the Sarathy/Dartois M. abscessus combination paper, it is squarely in the drug-tolerance territory, and its lege |
| SCHMALSTIG2024_DRYAD | DOWNGRADED to NO. Two independent reasons, both established from the mBio full text. First, the only file with three or more timepoints (Fig2ABCD.csv, |
| SCIREP2025_LONGTERM_SURVIVAL | NO — three timepoints and a biphasic-kill design, but nothing deposited beyond sequencing. |
| SCIREP_INH_RIF2022 | NO — fails twice over: the readout is MGIT-TTP rather than CFU, and the only deposits are sequence reads and a model file. Described in searches as "s |
| SGUL_RIFAQUIN | NO — rejected on readout. The LJ data are culture positivity plus a 1+/2+/3+ growth grade; genuine colony counts exist for 19 observations across the  |
| SGUL_RIFASHORT | NO, on the floor — and this is the closest miss in the territory, so state the reason precisely rather than waving at it. It passes the measured-basel |
| SGUL_RIFATOX | NO — rejected twice over: two timepoints, below the three-timepoint threshold, and the colony field is a 0-3 grade rather than a count. Confirmed at t |
| SGUL_STUDYA | NO — rejected on readout. The counts are right-censored at 20 colonies, have no volume and so no density, and only 14 patients reach three true numeri |
| SLOAN_COLONYGROWTH_2016 | NO — no deposit, and the attrition (19 to 10 to 6 positive samples) means most series would be censored anyway. Returned because the censoring pattern |
| SMART420_ZENODO_5021631 | NO — sequencing deposit only. Returned because it is the sole mycobacterial drug-killing 'Data from:' record surfaced by the Zenodo dataset-type searc |
| STARPROT_TKA2025 | NO as a dataset — but worth keeping as a CITABLE FLOOR SOURCE. It supplies a published, quotable detection limit for the 2.5 µL spot method used by th |
| SULDUR_HFS_MABS2026 | NO — rejected on access. This is the single most painful rejection in my territory: seven timepoints, ~15 arms, three isolates, and an explicitly meas |
| SUTEZOLID_EBA | NO — the only supplementary table is adverse events. Named explicitly because 'Sutezolid EBA' is the top hit for hollow-fibre and EBA searches in the  |
| TBAPEX_CPATH | NO as a public deposit — it fails the access test outright, since obtaining the data requires registration, a research proposal, steering-committee re |
| TBDA_MOUSE_NODEPOSIT | NO — a class-level rejection covering the mainstream TB Drug Accelerator and NIAID-contract murine efficacy literature. Returned as a single grouped e |
| TBDA_MULTIMODAL_2025 | NO — wrong readout. A well-deposited TBDA study whose deposits are transcriptomic and morphological; the viability measurement is a single-timepoint r |
| TBDA_RELAPSE_PREPRINT_2026 | NO as a deposit — the data are not obtainable without an access request — but PROMOTE IT to the most useful lead in this search, because its Table S1  |
| TBI223_DARQ_MOUSE2023 | NO — rejected on access. Notable because it is the densest single source of TBI-223 and sutezolid mouse CFU I found, and none of it is deposited. |
| TBI223_FIGSHARE_2024 | NO, on two independent grounds, but keep it in the search record. (1) No detection floor exists anywhere — not the article, not the Methods, not the C |
| TBPACTS | NO on access, and name it in the search strategy as the largest gated reservoir. It is the right thing to cite as the boundary of what an open search  |
| TBPACTS_CPATH | NO, on two grounds, and the scope ground should be settled first. His stated scope is in vitro and in vivo mouse lung or spleen; TB-PACTS is human spu |
| TBPRACTECAL_NC2026 | NO — rejected on READOUT, not on access. Bactericidal activity is measured as time-to-positivity in BACTEC MGIT liquid culture, not as viable counts.  |
| TBPRACTECAL_PKPD | NO on the readout — MGIT time-to-positivity is a time, not a viable count, so it fails the CFU/MPN/log10-density requirement. Returning it anyway beca |
| TBRU_SERIALTB_CODE | NO — wrong readout. Serial sampling of a patient is not the same as serial counting; this deposit tracks population genetics, not burden. Recorded bec |
| UNITE4TB_PROGRAMME | NO — the consortium's mandate-driven deposits in this period are clinical and modelling outputs, not preclinical killing kinetics. Recorded so the str |
| VANRIJN2024_TBAJ876 | REJECT, on obtainability — and keep it in the rejected column deliberately, because it makes the paper's point better than any accepted record. This i |
| VANWIJK2026_ZENODO | NO — data not obtainable. Worth reporting as an explicit rejection: it is exactly the shape of deposit the paper wants and it is publicly indexed but  |
| VIVLI_TMC207_EBA | NO on access. Keep it in the search strategy as the one bedaquiline EBA study in this territory that has a registered dataset DOI, precisely to make t |
| WALSH_NITAZOXANIDE_EBA | NO — counts and timepoints are right, the deposit does not exist. Recorded as a clean example of the dominant failure mode in human EBA work. |
| WALTERPAE2026 | NO, on three grounds, each sufficient. (1) The deposited CFU are medians, not observations — there are no replicate-level values anywhere, so nothing  |
| WHO_TBIPD_UCL | NO — fails the readout test, and is gated besides. Named in the report because it is the obvious platform a referee will ask about and it should be vi |
| WONG2023_ELIFE_CAMP | NO — five timepoints and a stated floor, but the numbers are not deposited. Worth keeping in the rejected list precisely because of the quotable 100 C |
| WYNN2025_AAC_MOUSE | NO. The supplementary data are real and downloadable, but they are gene-set enrichment tables, not viable counts. This settles the WALTER2025 ambiguit |
| YOON2026_AAC_ALDRIDGE | NO — wrong readout (OD600, not CFU/MPN) and only two timepoints. Included because it is the Aldridge lab's current combination-therapy paper in a lipi |
| ZENODO_RIF_SLOWPHASE_CODE | NO — code without data, the same pattern as the BTZ-043 repository. Two independent instances of it in this territory is itself worth a sentence in th |

## Search strategy, verbatim

Reproduced here because the manuscript will report it.

### By drug: bedaquiline, pretomanid, delamanid, linezolid, sutezolid, clo

```
All strings verbatim; run 8 September 2026.

PubMed (via search_articles):
1. "bedaquiline time-kill Mycobacterium tuberculosis CFU kill curve data availability"
2. "hollow fiber system tuberculosis pharmacokinetic pharmacodynamic CFU time-kill"
3. "Emergence of phenotypic and genotypic antimicrobial resistance Mycobacterium tuberculosis static kill curve isoniazid rifampicin Scientific Reports"
4. "Pharmacokinetics bactericidal activity toxicity short oral regimens rifampicin-resistant tuberculosis TB-PRACTECAL"
5. "Protocol quantify bacterial burden time-kill assays colony-forming units most probable number Mycobacterium tuberculosis STAR Protocols"
6. "role of cytochrome bc1 inhibitors in future tuberculosis treatment regimens Nature Communications 2025"

Web search (general index):
7. "zenodo Mycobacterium tuberculosis CFU time-kill dataset bedaquiline"
8. "figshare dataset Mycobacterium tuberculosis kill curve CFU pretomanid linezolid"
9. "\"hollow fiber\" tuberculosis \"source data\" CFU bedaquiline pretomanid moxifloxacin deposited dataset"
10. "Mycobacterium abscessus time-kill CFU dataset zenodo figshare \"data availability\""
11. "\"Mycobacterium tuberculosis\" mouse lung CFU \"source data\" Nature Communications bedaquiline OR pretomanid OR linezolid regimen relapse"
12. "Zenodo dataset \"time-kill\" mycobacteria CFU rifampicin isoniazid deposited data record"
13. "eLife \"Reactive Oxygen Detoxification\" Mycobacterium abscessus antibiotic survival Dryad source data linezolid tigecycline CFU"
14. "telacebec Q203 OR \"BTZ-043\" OR macozinone OR quabodepistat OR ganfeborole Mycobacterium tuberculosis CFU time course \"data availability\" repository"
15. "\"Mycobacterium tuberculosis\" OR \"M. abscessus\" kill curve CFU \"deposited\" Dryad OR \"Mendeley Data\" antibiotic time course"
16. "\"data availability\" figshare OR zenodo Mycobacterium tuberculosis \"log10 CFU\" supplementary dataset bactericidal activity 2024 2025 2026"
17. "\"sutezolid\" OR \"TBI-223\" OR \"GSK-286\" OR \"sorfequiline\" Mycobacterium tuberculosis CFU mouse OR hollow-fiber supplementary data table log10"
18. "Mycobacterium tuberculosis antibiotic CFU killing \"Source Data\" file Nature OR \"Scientific Reports\" OR \"Nature Communications\" 2024 2025 rifampicin isoniazid bedaquiline"
19. "\"Mycobacterium smegmatis\" OR \"Mycobacterium bovis BCG\" OR \"Mycobacterium marinum\" antibiotic time-kill CFU dataset zenodo OR figshare OR \"source data\" deposited"
20. "\"rifapentine\" OR \"high-dose rifampicin\" OR \"levofloxacin\" tuberculosis mouse lung CFU supplementary table individual mouse data \"log10 CFU\" available"
21. "PLOS \"S1 Data\" tuberculosis OR mycobacterium time-kill CFU \"colony forming units\" underlying data bedaquiline OR moxifloxacin OR rifampicin"
22. "site:figshare.com tuberculosis CFU dataset time kill bactericidal"
23. "github repository \"kill curve\" OR \"time-kill\" Mycobacterium tuberculosis CFU data model fitting deposited csv"
24. "delamani
```

### HUMAN DATA — published, publicly deposited datasets of mycobacterial k

```
All strings verbatim, run 8 September 2026.

WEB SEARCH (WebSearch tool):
1. early bactericidal activity trial deposited data sputum CFU individual participant
2. serial sputum colony counting SSCC dataset supplementary CFU tuberculosis
3. Zenodo sputum "log10 CFU" tuberculosis early bactericidal activity dataset deposited
4. TB-PACTS Critical Path Institute tuberculosis clinical trial data platform individual participant data REMoxTB
5. "early bactericidal activity" tuberculosis "data availability" GitHub sputum CFU model code dataset
6. Dryad OR Zenodo OR figshare dataset "sputum" tuberculosis "colony forming units" treatment "day 14" repository data
7. differentially culturable tubercle bacteria sputum most probable number treatment time course data available Chengalroyen
8. Gates Open Research OR Wellcome Open Research dataset tuberculosis sputum colony forming unit serial counts treatment underlying data
9. Vivli tuberculosis early bactericidal activity study data request individual participant data sputum CFU
10. "gatesopenresearch.org" tuberculosis sputum culture data "underlying data"
11. Lancet Microbe isoniazid essential first 14 days tuberculosis trial data sharing statement appendix individual CFU Dooley
12. Zainabadi Walsh GHESKIO Haiti tuberculosis early bactericidal activity molecular bacterial load supplementary data CFU individual patients
13. "Scientific Data" OR "data descriptor" tuberculosis clinical trial sputum bacteriology dataset published repository CFU time to positivity
14. PredictTB trial data sharing repository deposited sputum culture MGIT dataset NIAID Zenodo
15. ReSeqTB relational sequencing TB data platform what data phenotypic MIC access request row level
16. Nature Medicine OR Nature Communications tuberculosis trial "source data" sputum "log10 CFU" bactericidal activity patients
17. World Health Organization tuberculosis treatment individual patient data platform University College London access sputum culture
18. site:zenodo.org tuberculosis sputum CFU colony counts patients treatment dataset
19. site:figshare.com dataset tuberculosis patients sputum "colony forming" counts day 14 bactericidal
20. Jindani Dore Mitchison 2003 "Bactericidal and sterilizing activities of antituberculosis drugs during the first 14 days" methods sputum dilutions plated selective 7H11
21. "TB-PACTS" list of studies NC-001 NC-002 NC-005 CDAP Critical Path early bactericidal activity colony forming units available
22. Sloan 2015 Clinical Infectious Diseases bacillary elimination rates lipid bodies sputum supplementary data individual CFU Malawi serial sputum colony counting

PUBMED (E-utilities via MCP search_articles):
A. differentially culturable tubercle bacteria treatment response most probable number sputum
B. "early bactericidal activity"[Title] AND (sputum OR tuberculosis)   [date_from=2014, sort=pub_date; 69 records, 40 retrieved]
C. ganfeborole leucyl-tRNA synthetase inhibitor phase 2a rifampicin-susceptible tuberculosis
D. P
```

### Mouse and other in vivo models: mycobacterial organ burden (lung, sple

```
All strings verbatim. Date of search: 2026-09-08.

=== WebSearch (Google-backed) ===
1. mouse tuberculosis lung CFU data deposited figshare source data bacterial burden
2. Mycobacterium tuberculosis mouse model CFU "source data" Nature Communications lung burden treatment
3. Zenodo dataset mouse Mycobacterium tuberculosis lung CFU bacterial burden antibiotic treatment
4. figshare dataset "Mycobacterium tuberculosis" mouse lung spleen CFU treatment relapse deposited
5. "C3HeB/FeJ" mouse tuberculosis CFU supplementary data table treatment weeks limit of detection
6. Nature Communications tuberculosis mouse "Source Data" file CFU lung bedaquiline OR pretomanid OR rifampicin regimen relapse
7. macaque granuloma CFU dataset deposited Flynn tuberculosis bacterial burden data availability
8. Berg 2022 "model-based meta-analysis" relapsing mouse model CPTR database tuberculosis data availability public access
9. PLOS "S1 Data" mouse tuberculosis lung CFU treatment supporting information dataset log10
10. "Selection and prioritization of candidate combination regimens" tuberculosis Science Translational Medicine data file mouse relapse CFU supplementary
11. bioRxiv 2026 mouse tuberculosis CFU dataset deposited zenodo "data availability" lung bacterial burden treatment
12. guinea pig tuberculosis drug treatment lung spleen CFU supplementary data file deposited log10 counts

=== PubMed (esearch via MCP) ===
13. (tuberculosis OR mycobacter*) AND (mouse OR mice OR murine) AND (CFU OR "colony-forming") AND ("source data" OR "data availability" OR figshare OR zenodo OR dryad)   [2 hits — PubMed does not index data-availability statements; abandoned this route]
14. "cytochrome bc1 inhibitors in future tuberculosis treatment regimens"

=== NCBI E-utilities, db=pmc (full text) ===
15. ("source data file"[All Fields]) AND (tuberculosis[All Fields]) AND (mice[All Fields]) AND (CFU[All Fields])   [224 hits]

=== Europe PMC REST search (full text; strings shown decoded) ===
16. ("source data" AND tuberculosis AND mice AND "CFU" AND (lung OR spleen) AND (treatment OR antibiotic OR drug)) AND HAS_SUPPL:Y
17. (tuberculosis OR mycobacterium) AND (mouse OR mice OR murine) AND "CFU" AND ("zenodo" OR "figshare" OR "dryad")   [331 hits]
18. ("guinea pig" OR rabbit OR macaque OR marmoset) AND tuberculosis AND "CFU" AND ("source data" OR "supplementary data" OR zenodo OR figshare OR dryad) AND (treatment OR drug OR antibiotic)   [544 hits]
19. ("Mycobacterium abscessus" OR "Mycobacterium avium" OR "Mycobacterium marinum" OR "BCG") AND (mouse OR mice OR zebrafish) AND "CFU" AND ("source data" OR zenodo OR figshare OR dryad OR "Mendeley Data")
20. JOURNAL:"Antimicrob Agents Chemother" AND (tuberculosis OR mycobacterium) AND (mice OR mouse OR murine OR "guinea pig" OR rabbit) AND "source data"
21. (tuberculosis OR mycobacteri*) AND (mice OR mouse) AND ("lung CFU" OR "CFU/lung" OR "log10 CFU") AND ("supplementary data" OR "Supplementary Data 1" OR "Data S1" OR "S1 Data") AND (treat
```

### TB consortia and funded programmes that deposit under mandate: ERA4TB 

```
Run 2026-09-08. Verbatim strings, by database.

A. WebSearch (US web index):
1. ERA4TB Zenodo community dataset Mycobacterium tuberculosis time-kill CFU
2. UNITE4TB data sharing Zenodo dataset tuberculosis CFU deposit
3. "STAR Protocols" ERA4TB "time-kill" Mycobacterium tuberculosis colony-forming units most probable number 2025 data availability
4. PreDiCT-TB consortium hollow fibre model tuberculosis dataset deposited supplementary CFU
5. RespiriTB RespiriNTM IMI AMR Accelerator dataset deposited Zenodo Mycobacterium abscessus CFU
6. "TB Drug Accelerator" Gates Foundation dataset deposited Dryad Zenodo mouse lung CFU source data
7. Critical Path Institute CPTR preclinical tuberculosis database mouse model data sharing "data" access public
8. TB Alliance data sharing policy preclinical datasets public repository mouse CFU
9. "PreDiCT-TB" IMI project results data repository hollow fibre mouse model publications deliverables open data
10. RePORT International data sharing tuberculosis "data access" repository specimen sputum colony forming units serial

B. Zenodo REST API, https://zenodo.org/api/records?q=<string>&size=25 :
  ERA4TB
  tuberculosis time-kill
  Mycobacterium tuberculosis CFU kinetics
  UNITE4TB
  TRIC-TB
  RespiriNTM
  Mycobacterium abscessus colony forming units
  hollow fibre tuberculosis
and with &type=dataset&sort=bestmatch :
  Mycobacterium tuberculosis drug killing
  tuberculosis bactericidal activity CFU dataset
plus direct record fetch https://zenodo.org/api/records/5021631

C. figshare REST API, POST https://api.figshare.com/v2/articles/search with {"search_for": "<string>", "page_size": 50} :
  ERA4TB
  tuberculosis time-kill CFU
  Mycobacterium tuberculosis colony forming units time-kill assay
plus direct record fetch https://api.figshare.com/v2/articles/26054098

D. Europe PMC REST search, https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<string>&format=json&pageSize=25&resultType=core (default field searches full text of OA records):
  "time-kill" AND "Mycobacterium tuberculosis" AND "zenodo"
  "ERA4TB" AND ("CFU" OR "colony forming")
  "853989" AND ("time-kill" OR "CFU")
  "853989" AND ("zenodo" OR "figshare" OR "Dryad" OR "Source Data")
  "UNITE4TB"
  "853800" AND ("CFU" OR "time-kill")
  ("RespiriTB" OR "RespiriNTM") AND "CFU"
  "Mycobacterium tuberculosis" AND "lung CFU" AND ("Dryad" OR "zenodo" OR "figshare" OR "source data")
  "TB Alliance" AND ("figshare" OR "zenodo" OR "Dryad") AND ("CFU" OR "colony-forming")
  "TB Drug Accelerator" AND ("CFU" OR "colony-forming")
  "Mycobacterium" AND "time-kill" AND "Source data are provided with this paper"
  "Mycobacterium tuberculosis" AND "kill" AND "Innovative Medicines Initiative" AND ("figshare" OR "zenodo" OR "Source data")
  "PreDiCT-TB"
  PMCID:"PMC13276577" OR PMCID:"PMC13237350" OR PMCID:"PMC12612876" OR PMCID:"PMC12382802"
Note: the FULL_TEXT: field prefix returns zero hits in this API; unprefixed quoted phrases do search full text and were used inste
```

### Mycobacterial persistence, tolerance, dormancy and methods literature 

```
DATE OF SEARCH: 8 September 2026.

PubMed (NCBI E-utilities, bio-research MCP), verbatim:
"Mycobacterium tuberculosis drug tolerance persisters CFU kill kinetics source data deposited"
"differentially culturable tubercle bacilli resuscitation promoting factor most probable number treatment"
(Both over-expanded via PubMed automatic term mapping and returned 0 and 1 records respectively; the productive searching was done in Europe PMC full text and directly against repository APIs.)

Europe PMC REST full-text search (https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=...&format=json&resultType=lite), verbatim query strings:
"Mycobacterium" AND "colony forming units" AND "figshare"   [102 hits, first 50 reviewed]
"Mycobacterium" AND "time-kill" AND ("zenodo" OR "Dryad" OR "Mendeley Data")
("Mycobacterium tuberculosis" OR "Mycobacterium abscessus" OR "Mycobacterium smegmatis") AND "Source Data" AND ("time-kill" OR "kill curve" OR "killing curve" OR "CFU over time")
"Mycobacterium" AND ("CFU" OR "colony-forming") AND ("Dryad" OR "Mendeley Data" OR "Open Science Framework") AND ("tolerance" OR "persister" OR "persistence")
"Mycobacterium" AND ("persister" OR "drug tolerance" OR "nonreplicating" OR "non-replicating") AND ("figshare" OR "Zenodo" OR "Dryad" OR "Mendeley Data" OR "osf.io")
"Mycobacterium" AND ("Wayne model" OR "hypoxic dormancy" OR "nutrient starvation" OR "streptomycin-starved" OR "18b" OR "caseum") AND ("figshare" OR "Zenodo" OR "Dryad" OR "Mendeley Data" OR "source data" OR "Supporting Information")
"Mycobacterium" AND ("lung CFU" OR "bacterial burden") AND ("deposited at figshare" OR "deposited in Zenodo" OR "Dryad Digital Repository" OR "Mendeley Data" OR "publicly available as of the date of publication")
("Mycobacterium") AND ("osf.io") AND ("CFU" OR "colony-forming")
DOI:"10.1128/aac.00996-25" ; DOI:"10.1038/s41467-022-29832-1" OR DOI:"10.1038/s41467-019-12224-3" OR DOI:"10.7554/eLife.81177" OR DOI:"10.1038/s41467-020-19959-4" OR DOI:"10.1016/j.celrep.2023.112875" OR DOI:"10.1038/s41467-024-48269-2" OR DOI:"10.1038/s41598-021-98176-5" OR DOI:"10.1016/j.xpro.2025.103643" OR DOI:"10.1038/s41467-023-38844-4" OR DOI:"10.1038/nature22361" ; DOI:"10.1128/aac.01849-25" OR DOI:"10.1128/aac.01310-24" OR DOI:"10.1128/spectrum.00246-21" OR DOI:"10.3390/microorganisms11020286" OR DOI:"10.1038/s41564-025-02201-6" ; DOI:"10.3390/antibiotics14030299" OR DOI:"10.1021/acsinfecdis.4c00948" OR DOI:"10.1021/acsinfecdis.5c00298" OR DOI:"10.1073/pnas.2423842122" OR DOI:"10.1038/s41586-025-09177-7"
Europe PMC full-text XML retrieved for PMC8452731, PMC11939544, PMC12216072, PMC12328218, PMC11099131, PMC12689514.

Dryad REST API (https://datadryad.org/api/v2/search):
q=Mycobacterium&per_page=100
q=tuberculosis&per_page=100

Zenodo (https://zenodo.org/api/records and record pages):
q="Mycobacterium" AND ("CFU" OR "colony forming"), type=dataset, size=40
q=mycobacterium AND antibiotic, size=25
records/20438984, records/17037904, records/20819399 
```

### Byte-level qualification of nine pre-identified candidate deposits of 

```
All strings below were issued on 8 September 2026 and are reproduced verbatim.

WEB SEARCH (WebSearch tool):
1. "dryad.4xgxd25pv" Mycobacterium abscessus reactive oxygen detoxification
2. Srivastava Gumbo hollow fiber Mycobacterium abscessus 12 studies systematic quantitative analyses data availability publicly available

REPOSITORY / API QUERIES:
3. https://datadryad.org/dataset/doi:10.5061/dryad.4xgxd25pv  -> HTTP 404
4. https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.4xgxd25pv  -> "Identifier cannot be viewed. Either you lack permission to view it, or it is missing required elements."
5. https://doi.org/10.5061/dryad.4xgxd25pv  -> HTTP 404 at the DOI resolver itself
6. https://datadryad.org/api/v2/search?q=Mycobacterium%20abscessus%20antibiotic%20survival  -> returns only doi:10.5061/dryad.t1g1jwt8h; the Penn record is absent
7. https://datadryad.org/api/v2/search?q=reactive%20oxygen%20detoxification  -> five unrelated records; the Penn record is absent
8. https://datadryad.org/dataset/doi:10.5061/dryad.t1g1jwt8h
9. https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.t1g1jwt8h  -> license https://spdx.org/licenses/CC0-1.0.html, versionStatus submitted, publicationDate 2023-11-27
10. https://datadryad.org/api/v2/versions/266463/files  -> CSV-20231114T155212Z-001.zip (4964 bytes) + README.md (1485 bytes), with SHA-256 digests
11. https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.t1g1jwt8h/download  -> {"error":"Unauthorized, must have current bearer token"}
12. https://datadryad.org/downloads/file_stream/2739463 and /2739458  -> Anubis proof-of-work bot challenge; not circumvented

FIGSHARE API (all five DOIs from the PLOS data availability statement):
13. https://api.figshare.com/v2/articles/28398944  -> "Data on Figs 5, 6 and S2 Table", CC BY 4.0
14. https://api.figshare.com/v2/articles/28398398  -> "Data on Fig 3", CC BY 4.0
15. https://api.figshare.com/v2/articles/28398227  -> "Data on Fig 2 and Table 3.", CC BY 4.0
16. https://api.figshare.com/v2/articles/28398899  -> "Data on Table 1. Demographics", CC BY 4.0
17. https://api.figshare.com/v2/articles/28398275  -> "Data on Fig 4", CC BY 4.0
18. https://ndownloader.figshare.com/files/52298045  (Data on Fig 4.xlsx, 12236 bytes — downloaded and read)
19. https://ndownloader.figshare.com/files/52298096  (Data on Fig 3.xlsx, 10207 bytes — downloaded and read)

EUROPE PMC SUPPLEMENTARY-FILE REST ENDPOINT (used after PMC imposed a proof-of-work download gate):
20. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10353356/supplementaryFiles?includeInlineImage=false
21. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10648937/supplementaryFiles?includeInlineImage=false
22. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12057361/supplementaryFiles?includeInlineImage=false
23. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13228079/supplementaryFiles?includeInlineImage=false
24. https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13387744/supplementaryFile
```

### Human/clinical-trial deposits of serial mycobacterial viable counts: t

```
All searches run 8 September 2026. Verbatim strings and endpoints:

REPOSITORY APIs (direct, no search engine)
1. figshare v2 item records: https://api.figshare.com/v2/articles/27862029 ; /27861990 ; /27861975 ; /27861846 ; /25524034 (title, description, licence, file list, md5, related materials)
2. figshare v2 file list: https://api.figshare.com/v2/articles/27862029/files
3. figshare search (POST https://api.figshare.com/v2/articles/search) body: {"search_for":"tuberculosis","institution":623,"item_type":3,"page_size":100,"order":"published_date","order_direction":"desc"} — returned 0 results (institution id wrong); superseded by DataCite enumeration below.
4. DataCite REST, full enumeration of the St George's prefix: https://api.datacite.org/dois?query=prefix:10.24376&page[size]=1000&fields[dois]=doi,titles,publicationYear,types — 374 DOIs returned, filtered on title substrings: tubercul | myco | sputum | bacter | rifa | TB | EBA | isoniaz | culture | jindani | moxi
5. DataCite REST, targeted: https://api.datacite.org/dois?query=prefix:10.24376 AND (tuberculosis OR bactericidal OR sputum OR mycobacterium)&page[size]=100
6. Dryad API v2 dataset records: https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.gv234 and .../doi%3A10.5061%2Fdryad.8pt77k0
7. Dryad API v2 file manifests: https://datadryad.org/api/v2/versions/2905/files and /api/v2/versions/15500/files
8. Dryad download attempts (all refused): /api/v2/datasets/.../download ; /api/v2/files/19303/download ; /downloads/file_stream/19303 ; /stash/downloads/file_stream/19303 ; /downloads/download_resource/2905 — 401 "Unauthorized, must have current bearer token" or an Anubis JS bot-check page.
9. Europe PMC supplementary-file service: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11326837/supplementaryFiles and .../PMC6247085/supplementaryFiles

FILES ACTUALLY DOWNLOADED AND OPENED
https://ndownloader.figshare.com/files/50649807 (Jindani 1980.xlsx, 64,648 B, md5 f36e9a2067bbc8a34e6bad436cc935a5)
https://ndownloader.figshare.com/files/50648709 (RIFASHORT_dataset.zip, 3,721,755 B, 34 SAS files + Data Dictionary.xlsx)
https://ndownloader.figshare.com/files/50648154 (RIFAQUIN orig download.zip, 852,619 B, 20 CSVs + CRF PDFs + data dictionary)
https://ndownloader.figshare.com/files/45414019 (rifatoxinitialsremoved.ods, 99,498 B)
https://ndownloader.figshare.com/files/50648763 (TB-1030 Study A.zip, 253,009 B, a_bact/a_data SAS + Mapping Spec + data notes)
Europe PMC PMC11326837 supplementary bundle -> jiad564_supplementary_data.zip -> Table S1.xlsx + "Supp Tables 2-12 (CLEAN) 11-20-2023.docx"
Europe PMC PMC6247085 supplementary bundle -> mbo006184173st1.docx (McAulay Table S1)

PUBMED / PMC (via the PubMed MCP server; PubMed is the source and DOIs are given inline)
10. Zainabadi K[Author] AND (differentially culturable OR limiting dilution OR sputum OR tuberculosis)
11. Differentially Detectable Mycobacterium tuberculosis Cells in Sputum from Treatment-Naive Subjects in Haiti
12. Full
```

### Repositories searched directly, hunting for the FILE rather than the p

```
VERBATIM QUERY STRINGS, BY DATABASE. Date run: 2026-09-08.

ZENODO — GET https://zenodo.org/api/records?q=<Q>&size=25&sort=bestmatch
"Mycobacterium tuberculosis" AND "time-kill" | "Mycobacterium tuberculosis" AND CFU | mycobacteria AND "killing kinetics" | "log10 CFU" AND tuberculosis | tuberculosis AND "colony forming units" | "minimum duration for killing" | MDK AND tuberculosis | mycobacterial AND persister AND CFU | "Mycobacterium abscessus" AND CFU | "Mycobacterium smegmatis" AND CFU | "Mycobacterium avium" AND CFU | tuberculosis AND "hollow fiber" | tuberculosis AND "hollow-fibre" | "Mycobacterium bovis BCG" AND antibiotic | "Mycobacterium marinum" AND antibiotic | "antibiotic tolerance" AND mycobacterium | "time-kill" | "time kill assay" | H37Rv | "Mycobacterium tuberculosis" AND dataset | "Mycobacterium abscessus" | "nontuberculous mycobacteria" | tuberculosis AND pharmacodynamics | mycobacterium AND "colony forming" | tuberculosis AND CFU | "Mycobacterium tuberculosis" AND bactericidal | "drug tolerance" AND tuberculosis | "Mycobacterium smegmatis" | resource_type.type:dataset AND (mycobacter* OR tuberculosis) [facet syntax unsupported, returned nothing] | type=dataset URL filter [504 timeout, unusable]

FIGSHARE — POST https://api.figshare.com/v2/articles/search {"search_for": <Q>, "page_size":100}
:title: time kill AND :title: tuberculosis | mycobacterium time kill assay CFU | Mycobacterium abscessus time kill CFU | killing kinetics mycobacteria colony forming units | log10 CFU mouse lung tuberculosis treatment | mycobacterium killing kinetics | abscessus time kill | tuberculosis CFU raw data | mycobacteria persister CFU | tuberculosis bactericidal source data | avium killing kinetics | H37Rv CFU | most probable number tuberculosis | MPN Mycobacterium tuberculosis | kill curve tuberculosis | bedaquiline CFU | moxifloxacin tuberculosis CFU | rifampicin H37Rv kinetics | tuberculosis limit of detection CFU | time-kill assay dataset | tuberculosis raw data CFU excel | mycobacterium source data killing | nontuberculous mycobacteria time kill | Mycobacterium chimaera drug discovery | tuberculosis persistence dataset CFU | growth dynamics mycobacterial populations | Source Data Mycobacterium tuberculosis | Source data mycobacterial killing | Mycobacterium tuberculosis viability days DMSO | McNeil Mycobacterium source data | Jowsey Mycobacterium | Cheung Mycobacterium tuberculosis source data | collateral drug Mycobacterium source data | Mycobacterium tuberculosis source data CFU | Otago Mycobacterium tuberculosis | Waller Collateral TB Source Data | Collateral_TB | clofazimine Mycobacterium CFU | Mycobacterium bovis BCG killing CFU dataset | pretomanid CFU time | linezolid Mycobacterium CFU
Also GET https://api.figshare.com/v2/articles?search_for="Mycobacterium tuberculosis" time-kill&item_type=3 [search term silently ignored by the GET endpoint — returns date-sorted noise; do not use this form]

DRYAD — GET https://datadryad.org/api/v2/searc
```

### Mycobacterial killing-over-time deposits, qualified at the bytes: the 

```
Verbatim strings and endpoints, run 8 September 2026.

NCBI esummary (verification of all 13 citations): https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=41125580,42098153,39181887,38071218,41446251,42294653,41416484,39827265,37973991,41946736,38941358,41652042,41339746&retmode=json

Deposit retrieval endpoints (all returned HTTP 200):
- https://static-content.springer.com/esm/art%3A10.1038%2F<doi-suffix>/MediaObjects/<file> for s41467-025-64427-6, s41467-026-72874-y, s41467-023-43937-1, s41467-025-56146-9, s41467-023-43304-0, s41467-026-71460-6
- https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2F<doi-suffix>/MediaObjects/<file> for s41564-025-02201-6 and s44321-026-00378-9
- https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/supplementaryFiles for PMC13336335, PMC13017726, PMC11646583 (this is what defeated the journals.asm.org 403 and academic.oup.com 403)
- https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML for PMC12546632, PMC13357804, PMC12988230, PMC13234193, PMC11646583
- https://api.figshare.com/v2/articles/26054098 and https://ndownloader.figshare.com/files/47111650
- https://api.github.com/repos/SamuelTaborCU/Mtb-16S-rRNA-vs-CFU/git/trees/main?recursive=1 and .../allanfriesen/CFU16SrRNAgap/git/trees/main?recursive=1; raw files from https://raw.githubusercontent.com/SamuelTaborCU/Mtb-16S-rRNA-vs-CFU/main/DataRaw/Manuscript%20Datasets.xlsx and .../DataRaw/Modeling%20data.csv
- https://api.github.com/repos/<repo>/license (both returned 404 = unlicensed)
- https://www.biorxiv.org/content/10.64898/2025.12.18.695164v1 (licence check)

Endpoints that FAILED and should not be retried: https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=<PMCID> (404, service moved); https://pmc.ncbi.nlm.nih.gov/utils/oa/oa.fcgi?id=<PMCID> (returns HTML shell); https://journals.asm.org/doi/suppl/10.1128/aac.00190-26/suppl_file/aac.00190-26-s0002.docx (403); https://academic.oup.com/jid/article/doi/10.1093/infdis/jiaf640 (403); Europe PMC supplementaryFiles for PMC12724693 (404, bioRxiv preprints carry none).

Content searches run inside every downloaded deposit (regex, case-insensitive, over all sheets/cells, R code and PDF text): "l\.?o\.?[dq]\.?", "limit of (detection|quantif)", "below detect", "detect\w* limit", "censor", "floor", "plated", "dilut", "µL|uL", "CFU". This is what surfaced the PETHE 100 CFU in vivo floor and the TABOR CFU_LOD column.

PubMed (mcp bio-research, 2023 onward, 0 results — recorded because it shows the limit of the approach): (Mycobacterium tuberculosis OR mycobacterial) AND (time-kill OR "colony forming unit" OR CFU) AND ("source data" OR "data availability" OR figshare OR Zenodo OR Dryad) AND (kinetics OR "over time")

Zenodo/Dryad REST (https://zenodo.org/api/records, type=dataset): "Mycobacterium tuberculosis time-kill CFU"; "mycobacteria kill curve colony forming units antibiotic"; "Mycobacterium abscessus time kill CFU" — heavily diluted by MALDI-TOF an
```

### Published, publicly deposited mycobacterial viable-count-over-time dat

```
Search date 2026-09-08. All strings verbatim.

EUROPE PMC REST (article XML and supplementary bundles opened directly):
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13234193/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13234193/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8131613/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8131613/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11742723/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11742723/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11344811/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11344811/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9017352/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9017352/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13128115/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13128115/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13387744/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13387744/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12546632/supplementaryFiles
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12546632/fullTextXML
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID%3A42018569&resultType=core&format=json
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A%2210.1128/aac.02398-21%22&resultType=core&format=json
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A%2210.1128/aac.02310-21%22&resultType=core&format=json
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22Reactive%20Oxygen%20Detoxification%22%20AND%20abscessus&resultType=core&format=json
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A%2210.1038/s41467-025-64427-6%22&resultType=core&format=json

PUBMED (via bio-research pubmed MCP, E-utilities syntax):
"Walter ND[Author] AND (tuberculosis OR Mycobacterium)"  [date_from 2024, date_to 2026, sort pub_date, max_results 25]
"Physiologic recovery of Mycobacterium tuberculosis from drug injury post antibiotic effect[Title]"

WEB SEARCH:
"Mycobacterium tuberculosis" time-kill CFU "source data" site:figshare.com OR site:zenodo.org OR site:datadryad.org
"Mycobacterium abscessus" OR "Mycobacterium avium" kill kinetics CFU dataset deposited zenodo dryad supplementary "limit of detection"
"BALB/c" mouse tuberculosis lung CFU "source data" nature communications 2025 2026 supplementary "limit of detection" log10 CFU

REPOSITORY APIs AND RECORDS:
https://api.figshare.com/v2/articles/26054098                      (TBI-223; CC BY 4.0, is_public true)
https://ndownloader.figshare.com/files/47111650                    (source_data_tbi223.csv, 120,694 bytes)
https://zenodo.org/api/records/21397999                            (relapse model code; metadata public)
https://zeno
```

### Re-qualification at the bytes of six candidate deposits (figshare x3, 

```
Tool loading (verbatim): ToolSearch query "select:WebSearch,WebFetch,mcp__plugin_bio-research_pubmed__search_articles,mcp__plugin_bio-research_pubmed__get_full_text_article", max_results 4; then ToolSearch query "select:mcp__plugin_bio-research_pubmed__convert_article_ids", max_results 1.

PubMed (search_articles), verbatim query strings:
1. "Culture-Free Enumeration of Mycobacterium tuberculosis in Mouse Tissues Using the Molecular Bacterial Load Assay" — 1 hit, PMID 35208914.
2. "silver nitrate Mycobacterium abscessus biofilms showerhead" — 1 hit, PMID 40492006.
3. "McNeil MB[Author] AND Mycobacterium tuberculosis AND (time kill OR bactericidal OR CFU)" — 7 hits, PMIDs 41202651, 35210534, 34984329, 34346123, 33996738, 32423951, 30456352.

PubMed ID conversion (convert_article_ids, id_type pmid): ["35208914"] -> PMC8876813; ["40492006"] -> PMC12146310.

PubMed Central full text (get_full_text_article), verbatim pmc_ids: ["PMC10024696"] (Waller 2023); ["PMC10924958"] (Yang 2024); ["PMC8876813"] (MBL assay 2022); ["PMC12146310"] (silver nitrate 2025).

WebSearch, verbatim: figshare OR zenodo Mycobacterium tuberculosis time-kill CFU source data deposit "limit of detection" CFU/mL — top hit was the ERA4TB six-laboratory exercise, already in the manifest; no new deposit surfaced.

Repository APIs queried directly (reproducible, no auth):
- https://api.figshare.com/v2/articles/22152056 (Waller)
- https://api.figshare.com/v2/articles/25254571 (Yang)
- https://api.figshare.com/v2/articles/19175153 (UCL MBL)
- https://zenodo.org/api/records/17037904 (Merchan)
- https://zenodo.org/api/records/14791314 (silver nitrate)
- https://data.mendeley.com/public-api/datasets/m2y7jpz4wz/files?folder_id=root&version=1 (DiaMOND)

Local verification commands actually run: pdftotext -layout merchan.pdf merchan.txt, then grep -n -i -E "limit of detection|detection limit|LOD|plated|plating|spot|serial dilut|drop|10 ul|100 .l|CFU/mL|dilution" merchan.txt; md5sum on the two Merchan Muddyvs8UZL workbooks; a custom Python parser over xl/sharedStrings.xml and every xl/worksheets/sheetN.xml for all nine .xlsx files; a custom parser over the Prism .pzfx XML (RowTitlesColumn, YColumn Title, Subcolumn) for six Yang files; and a full shared-strings dump of the DiaMOND cube to confirm the absence of any CFU column.
```

### Mycobacterial viable-count-over-time deposits: qualification pass at t

```
This was a qualification pass, so most retrieval was by direct address rather than keyword search. Verbatim strings and endpoints, all executed 8 September 2026:

REPOSITORY / FILE RETRIEVALS (curl, exact URLs)
figshare API: https://api.figshare.com/v2/articles/27862029 ; https://api.figshare.com/v2/articles/28398275 ; https://api.figshare.com/v2/articles/28398227 ; https://api.figshare.com/v2/articles/28398398 ; https://api.figshare.com/v2/articles/28398899 ; https://api.figshare.com/v2/articles/28398944 ; https://api.figshare.com/v2/articles/30259192
figshare file downloads: https://ndownloader.figshare.com/files/50649807 (Jindani 1980.xlsx) ; https://ndownloader.figshare.com/files/52298045 (Data on Fig 4.xlsx) ; https://ndownloader.figshare.com/files/52298096 (Data on Fig 3.xlsx)
OSF API: https://api.osf.io/v2/nodes/gwhpd/files/osfstorage/?page=1 (and pages 2, 3)
OSF file downloads: https://osf.io/download/5py7g/ (tkc.csv) ; https://osf.io/download/8nmwd/ (tkc_analysis.R) ; https://osf.io/download/n8ds2/ (read_me.rtf) ; https://osf.io/download/cz6hy/ (BCG_12.13.csv)
Zenodo API: https://zenodo.org/api/records/17037904 ; https://zenodo.org/api/records/20819399 ; https://zenodo.org/api/records/20831464
Zenodo file downloads: https://zenodo.org/api/records/17037904/files/<NAME>/content for README.txt, Planktonic_Muddyvs8UZL.xlsx, Planktonic_Muddyvs8UZL_FOX.xlsx, Planktonic_Muddyvs8UZL_TGC.xlsx, Planktonic_7H9vsCAMH.xlsx, Biofilm_Muddyvs8UZL.xlsx, Biofilm_Muddyvs8UZL_FOX.xlsx, Biofilm_Muddyvs8UZL_TGC.xlsx, Biofilm_7H9vsCAMH.xlsx, Mercha%CC%81n_Ruiz_2025.pdf
Dryad API: https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.t1g1jwt8h ; https://datadryad.org/api/v2/versions/266463/files ; download attempts against https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.t1g1jwt8h/download , https://datadryad.org/api/v2/files/2739458/download , https://datadryad.org/downloads/file_stream/2739458 , https://datadryad.org/downloads/download_resource/266463
Europe PMC supplementary-file packages: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12691649/supplementaryFiles ; .../PMC12858399/supplementaryFiles ; .../PMC11099131/supplementaryFiles ; .../PMC12067261/supplementaryFiles ; .../PMC11823617/supplementaryFiles
Europe PMC full text: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11099131/fullTextXML ; .../PMC10790704/fullTextXML ; .../PMC8452731/fullTextXML (returned 0 bytes; obtained instead through the PubMed Central MCP tool)
Europe PMC bibliographic: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:38059609&resultType=core&format=json ; https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:12519740&resultType=core&format=json
Springer static content (Nature Microbiology Source Data): https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-025-02201-6/MediaObjects/41564_2025_2201_MOESM3_ESM.pdf through ..._MOESM12_ESM.pdf

PAGE FETCHES (WebFetch)
https://datadryad.org/dataset/doi:10.5061/dr
```
