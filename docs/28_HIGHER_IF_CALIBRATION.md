# Manuscript idea calibration — IF ≈ 10–15 Resource / Methods stack

**Date:** 2026-09-06 (updated after alt-methods stack: Exp33–34 + `assay_geometry`)  
**Against:** evidence-honest draft + Bayesian/conformal floor, formal mediation, shipped CLI  
**Skill:** manuscript-idea-calibration  
**Literature:** live search (Brauner/Balaban MDK framework; Vijay eLife 93243; van Wijk iScience 2023 ERA4TB; Balaban persistence guidelines; PK/PD BLOQ/M3 practice)

Access notes: Brauner 2017 MDK framework — **open (PMC5479142)**; Balaban et al. persistence definitions — **paywalled / Nature**; Vijay 2024 — **open (eLife)**; van Wijk 2023 — **open (iScience)**; confidence in closest-paper mapping: **high**.

---

## 1. Claim statement

**Intended claim (pre-audit ambition):** Deep MDK / log-reduction tolerance calls are inoculum-dependent artefacts of assay geometry, so published tolerance phenotypes in clinical *M. tuberculosis* are largely misassigned.

**Supported claim (write this paper):** In published time-kill and MDK deposits, a *q*-log reduction endpoint is **unobservable** whenever starting density *N₀* and operational assay floor *L* violate definitional reachability / floor-identifiability boundaries; *L* is learned under uncertainty with a refusal rule; the resistance–tolerance association decomposes as an **ACME through log10 *N₀*** with bootstrap CIs; and a shipped CLI reproduces the isolate-level contracts (clinical 33/12/6, Dubey 5/20). Laboratory contrasts remain geometry/ordering, not flask-independent significance tests.

**Gap vs Nature Micro mechanism tier:** Still one tier below a new killing mechanism or prospective matched-headroom re-call. That gap is **accepted**; the stack does not try to close it with a neural net.

**Honesty bound:** Does **not** claim Nature Microbiology mechanism tier; does **not** claim a universal kill-curve AI; constrains when MDK is measurable.

---

## 2. Why this stack (not “fix the net”)

| Approach | Status in this project | Role in the paper |
|---|---|---|
| Unconstrained NN on *N*_reach = *L* · 10^*q* | Fails OOD by ~3 log10 (`docs/22`, `src/learn_boundaries.py`) | **Negative control** |
| PySR / log-linear recovery | Recovers exact law (`docs/23`, `src/symbolic_boundaries.py`) | **Positive control** |
| Bayesian / discrete floor posterior + refusal | Exp33; `src/floor_posterior.py`; `docs/29` | **Inference contribution** |
| Formal linear mediation (ACME/ADE) | Exp34 | **Causal-structure contribution** |
| `python -m src.assay_geometry` | Vignettes PASS | **Software / Resource contribution** |

Docs 24–25: trajectories have per-flask shape, no pooled law. Do **not** invent a global kill-curve model.

---

## 3. Novelty (three closest papers)

| Paper | Establishes | Leaves open | Forecloses this claim? |
|---|---|---|---|
| **Brauner et al. 2016/2017** | MDK as metric; MIC vs MDK | Observability when floor is reachable; forced vs undecidable | **No** |
| **Vijay et al. 2024** | Clinical MDK labels; IR–tolerance link | Algebra that names isolates; *N₀*-mediated pathway with CIs | **No** |
| **van Wijk et al. 2023** | Six-lab standardisation; BQL practice | Geometry that forces duration endpoints; inversions | **No** |

**Contribution type:** **Resource / analytical method** — definitional boundaries + probabilistic floor + mediation + multi-deposit audit + CLI. Not a new killing mechanism.

---

## 4. Premise audit (unchanged core)

| Premise | Disposition |
|---|---|
| *L* is a validated LOQ | Use **operational assay floor**; Exp33 adds interval + refusal |
| Tolerance label = biology | Name forced / undecidable; refuse when *L* soft |
| 217 independent isolates | Census OK; inference → baseline-only (Exp34 n=168 IS/IR) |
| Six labs ≈ independent flasks | Between-lab *p*-values not available |

---

## 5. Venue and article type — **IF ≈ 10–15 Resource / Methods**

| Tier | Fit under this stack? |
|---|---|
| **Nature Microbiology Article** | **No** without prospective matched-headroom re-scoring |
| **Nature Communications / eLife Tools / similar IF ~10–15 Resource** | **Yes — primary target** |
| **High specialty Article** (*mBio*, *AAC*, *JAC*) | **Yes — backup** |
| Unconstrained “AI predicts MDK” framing | **Hurts** any IF>10 referee |

**Recommendation:** Submit as **Resource / Methods** (or eLife Tools-equivalent) whose first-class deliverables are (1) boundaries under uncertain *L*, (2) mediation with CIs, (3) CLI vignettes. Do **not** aim Nature Micro until prospective work exists. Do **not** add a deep-learning-predicts-MDK figure.

**Target shortlist (descending ambition within reachable IF 10–15):** *Nature Communications* (Resource/Methods); *eLife* Tools/Resource; *mBio* Methods/Resource; *Antimicrobial Agents and Chemotherapy* Methods; *iScience* (same family as van Wijk).

---

## 6. Success criteria (this stack)

| Criterion | Status |
|---|---|
| Exp33 calibrated floors + refusal on NONE | **Done** (7/7 deposits) |
| Exp34 ACME with bootstrap CIs + baseline sensitivity | **Done** (ACME excludes 0; ADE does not) |
| `assay_geometry` reproduces Dubey 5/20 and clinical 33/12/6 | **Done** |
| docs/28 points at IF 10–15 Resource/Methods | **This document** |
| Manuscript Methods/Results cite net (−), symbolic (+), mediation, CLI | **Done** |

---

## 7. Key figure (skeptic figure)

1. Reachability plane with forced / undecidable marked.  
2. Dubey cold application (5-log set).  
3. Mediation path diagram (ACME vs ADE) *or* CLI vignette output — not a neural net.

---

## 8. Three hardest referee objections

1. **“You overclaim that tolerance is wrong.”**  
   Answer: measurement/reporting + ACME through *N₀*; growth survives; no universal artefact claim.

2. **“Your floor is inferred.”**  
   Answer: Exp29 + Exp33 posterior/refusal; Dubey DERIVED; refuse Windels/Kaur.

3. **“Why not a predictive ML model for IF?”**  
   Answer: docs/22–23 — nets learn the training box; the law is closed form; shipping the law is the product.

---

## 9. Gap list that still moves venue upward (unchanged)

1. **Prospective:** matched-headroom re-score of forced isolates.  
2. **Second non-*Mtb* clinical MDK deposit** with stated plated volume.  

Items that do **not** move venue: retraining nets on *L* · 10^*q*; inventing a pooled kill-curve AI; parallel `MANUSCRIPT.md` maintenance.

---

## Bottom line

Worth writing — as an **IF ≈ 10–15 Resource / analytical-methods paper**: infer *L* under uncertainty, derive observability downstream, cite formal mediation, ship the CLI.  
**Most damaging weakness (avoided):** treating unconstrained nets as the path to higher IF.  
**Reformulated claim:** deep fractional MDK endpoints fail observability under stated *N₀* and *L*; published deposits already contain forced and undecidable calls the boundaries name; resistance→tolerance travels largely through inoculum (ACME).  
**Venue:** Nature Communications / eLife Tools–class Resource; Nature Micro only after prospective matched-headroom work.
