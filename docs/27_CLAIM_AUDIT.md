# Claim audit — assay-floor / tolerance manuscript

**Date:** 2026-09-06  
**Canonical text:** `manuscript/PAPER_COMPLETE.md`  
**Seed:** `results/tables/exp31_recomputed_inference.csv` (20 SUPPORTED / 7 WEAKENED / 5 NOT SUPPORTED) plus Exp29–32 receipts.

Status codes: **SUPPORTED** | **WEAKENED** | **NOT SUPPORTED** | **TERMINOLOGY** | **HARD ERROR** | **STRUCTURE**

---

## Blocking fixes (must land in Phase B)

| Issue | Location | Status | Fix |
|---|---|---|---|
| Keywords / prose use “limit of quantification” for *L* | YAML keywords; Abstract; Methods | TERMINOLOGY | Use **operational assay floor / minimum reportable positive count**; reserve “LOQ” for stating sources do *not* provide one (Exp29: 0/5 deposits state LOQ with a value) |
| “2,775 readings, of which 19.3% are flagged” | Methods (ERA4TB) | HARD ERROR | 19.3% is of the **2,580**-row analysis set; of 2,775 file rows it is **17.9%** (498 flags) |
| AUC 0.974 + Mann–Whitney p = 1.2e−10 as inference | §5 | NOT SUPPORTED | Keep AUC as description of lab ordering; drop flask-level p; note lab-level exact p = 0.10 (design floor) |
| Cox institute p-values / HR 5.27 p < 0.001; log-rank | §5 | NOT SUPPORTED | Report coefficient trade descriptively only; no between-lab Wald / log-rank p |
| Growth × panel interaction p = 0.0072 | §4 | NOT SUPPORTED | Cut; no generating code in repo |
| Ceiling Fisher p = 0.030 as headline support | §1 | WEAKENED | Lead with **counts** (100% vs ~88%); note baseline-only Fisher p = 0.137 |
| Δh = 2.33 without lab count / CI | §6 | WEAKENED | Attach **4 laboratories** (B,C,D,F) and bootstrap CI [0.047, 2.3]; lead with volume-driven **4.40** |
| Conclusion “no admissible count would have changed the answer” | Conclusion | OVERSTATE | Applies to the **12 forced** only; the **6 undecidable** remain open |
| Intro `H = log10(N0/L)` vs Methods `H` as ratio, `h` as log10 | Intro / Methods | STRUCTURE | Harmonise: *H* = N0/*L*, *h* = log10(*H*) |
| Supplementary tables between Results §8 and §9–§10 | Structure | STRUCTURE | Move Supp tables after Results §10 |
| Implicit / project 74.8% recrossing | §5 / supplements | HARD ERROR if quoted | Honest plating-key return rate is **84/140 = 60%** (Exp32) |

---

## Claim ledger (load-bearing)

### Algebra / geometry (spine — keep)

| Claim | Evidence | Verdict |
|---|---|---|
| Two definitional boundaries: reachability N0 ≥ L·10^q; identifiability at floor N0 > L/c1 | `docs/19_MATHEMATICS.md`; Methods | SUPPORTED |
| Clinical *L* = 23 MPN/mL INFERRED; 33 readings on 23; 0 below | Exp29; `docs/21_FLOOR_INFERENCE.md` | SUPPORTED |
| 0/217 short of 1- or 2-log; **33/217 (15.2%)** short of 4-log; all 33 at ceiling | Exp22/31; Table 2 | SUPPORTED (census) |
| Among 184 with headroom, 162 (88.0%) at ceiling; Fisher p = 0.030 | Exp31 | WEAKENED as *p*; counts SUPPORTED |
| Baseline-only: 21/174 (12.1%) short; ceiling Fisher p = 0.137 | Exp31 | Report as sensitivity |
| 18 at floor; survival span = N0 span (265×); 12 Low / 6 Medium | Exp25/31 | SUPPORTED |
| 185 determinable / 12 forced / 6 undecidable of 203 (15 d) | Exp25/29/31 | SUPPORTED |
| Baseline-only: 156 / 10 / 2 of 168 | Exp31 | Add as sensitivity column |
| Unreachable IR vs IS: 26.2% vs 7.6% (Fisher p = 0.00056) | Exp25/31 | SUPPORTED (survives baseline-only at 22.4% vs 7.6%, p = 0.016) |
| Boundaries predict 33 / 12 / 6 isolate-by-isolate | Exp25 | SUPPORTED |

### Associations / biology

| Claim | Evidence | Verdict |
|---|---|---|
| Growth adj. N0: β ≈ +0.0266, p = 0.0025; survives BH | Exp22/30/31 | SUPPORTED |
| Resistance unadj. β ≈ +0.259, p = 0.0035 → adj. +0.089, p = 0.374 (~66% attenuation) | Exp22/31 | SUPPORTED (72% on baselines) |
| ACME through log10 N0 ≈ +0.166 (boot CI excludes 0); ADE spans 0 | Exp34 | SUPPORTED (formal mediation) |
| Ordinal logit: same 2 BH survivors; growth OR 1.10; resistance OR 2.32 | Exp30 | SUPPORTED (Table 4 not scoring artefact) |
| Resistance ordinal fails BH on baseline-only (OR 2.11, p = 0.031) | Exp30 | Note precision loss / BH drop |
| IR vs IS start: 5.36 vs 6.36 log10 (10×) | Exp31 | SUPPORTED |
| Growth IR vs IS null (p = 0.24) | Exp31 | SUPPORTED |
| Panel shortfall 15.2% → 3.3%; unpaired Fisher | Exp31 | Replace with **McNemar** (26 lost / 0 gained, p = 3.0e−8) |
| Headroom denser at 60 d; unpaired MW | Exp31 | Replace with **signed-rank** (median +1.58; 193 up / 0 down) |
| IQR start 1.00 → 0.42 | Exp31 | SUPPORTED; add paired bootstrap CI [−0.58, −0.54] |
| Interaction p = 0.0072 | — | NOT SUPPORTED — cut |
| MIC–MDK: 0 survive BH | Exp16/31 | SUPPORTED |

### Six-laboratory / ERA4TB

| Claim | Evidence | Verdict |
|---|---|---|
| Kill-rate span 5.2-fold at MXF 10× | Exp17/31 | WEAKENED — attach CI [1.3, 5.2] |
| Clearance ~ N0: AUC 0.974 | Exp17/31 | SUPPORTED as **description**; p NOT SUPPORTED |
| Cox / log-rank institute p-values | Exp17/31 | NOT SUPPORTED |
| 87% of starting-density variance between labs | Exp31 | SUPPORTED |
| Rate also has lab share ~33% (p = 0.0048) | Exp31 | Soften “rate far more reproducible” |
| Rebound: 48/64 final step not decline; 44/64 end >1 log above nadir | Exp24/31 | SUPPORTED |
| First crossing reversible: 84/140 = 60% (plating key) | Exp32 | Replace any absorbing-clearance language |
| 17/32 returned at most-sensitive plating | Exp24 / Exp32 100 µL stratum | Keep with stratum defined |
| Flag contradictions 83/498 (16.7%) | Exp24/29/31 | SUPPORTED |
| Flag rate 19.3% of 2,775 | Methods | HARD ERROR — fix denominator |
| Δh = 2.33 at 100 µL | Exp28/31 | WEAKENED (4 labs + CI) |
| Δh = 4.40 with plated volume | Exp28/31 | SUPPORTED — lead with this |
| Inversions 36.6% (CI 30.1–43.6) | Exp23/31 | WEAKENED CI → lab bootstrap ~[3%, 72%] |
| At Δb>0.10: 21.3%; D/b criterion 83.8% | Exp23/31 | WEAKENED / SUPPORTED respectively |
| Dubey holdout: 5/20 cannot show 5-log; L = 10 | Exp27/29 | SUPPORTED |

---

## Exp29–32 integration map

| Exp | Role in manuscript |
|---|---|
| **29** Floor provenance | Methods terminology; Supp provenance table; denominator hygiene; pooling cost |
| **30** Ordinal tolerance | Parallel ORs beside Table 4; BH agreement note |
| **31** Clustering audit | Soften §1 p; paired panel tests; strip §5 between-lab p; Δh / inversion CIs; Supp verdict sheet |
| **32** Crossing events | Relabel §5 event; 60% return; interval-censoring note; Supp transitions |

---

## Completeness (not science blockers)

- Authors, correspondence, funding, COI, contributions, archive commit: placeholders
- References deliberately not compiled
- `MANUSCRIPT.md`: lineage duplicate — do not maintain in parallel
- CLI headroom tool: deferred to publication

---

## Bottom line for Phase B

The floor/censoring spine (33 / 18 / 12 / 6, algebraic boundaries, resistance–N0 confounding, Dubey, Δh 4.40, inversions point estimate) stands. Highest revision risk is **§5 laboratory inference** and the **unsupported interaction p**, plus LOQ wording and the **19.3%/2,775** hard error.
