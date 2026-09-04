# Recalculation and figure code

**Target preprint:** bioRxiv 10.1101/2025.02.12.637810
**Written:** 2026-09-03
**Supersedes nothing.** This is the executable companion to
[01_AUDIT_AND_REBUILD_PLAN.md](01_AUDIT_AND_REBUILD_PLAN.md) §1.3: everything that document
asserted about the mathematics is now computed, versioned and reproducible.

```bash
python run_all.py
```

Runs in about two minutes, writes 22 tables, 7 figures (PNG + PDF) and 3 receipts.
No network access, no downloads. Requires numpy, scipy, pandas, matplotlib.

---

## 1. What this code establishes

23 quantitative claims from the manuscript were recomputed from the paper's own
equations and its own Table 1. **20 fail, 2 are partial, 1 passes.** Full table with
verdicts and notes: [`results/tables/claim_recalculation.md`](../results/tables/claim_recalculation.md).

The single most consequential result is not in the audit document, because it required
running the corrected equations:

> **The paper's central comparative conclusion does not survive the correction of
> Equation 4.** With the discontinuity removed and nothing else changed, *M. tuberculosis*
> and *S. aureus* differ by only **1.13-fold (0.05 log₁₀) at 240 h** under the paper's own
> Table 1 parameters. The contrast in the published Figure 2 is produced by the discontinuity,
> not by the biology. Patching the algebra therefore is not enough; the model has to
> become mechanistic. That is what `src/models/mechanistic.py` provides.

### The headline numbers

| Quantity | Paper | Recomputed | Source |
|---|---|---|---|
| Eq. 4 at `t_c`, Mtb | biphasic decay | **rises ×2,981 (3.47 log₁₀)** | `eq4_discontinuity.csv` |
| Eq. 4 at `t_c`, *S. aureus* | biphasic decay | **rises ×403 (2.61 log₁₀)** | same |
| Eq. 4 at `t_c`, abstract's parameters | biphasic decay | **rises ×2.4×10¹⁷ (17.4 log₁₀)** | same |
| `t_c` Mtb | 80 h, fitted | **33.27 h implied** (2.41× off) | `tc_identifiability.csv` |
| `t_c` *S. aureus* | 12 h, fitted | **15.51 h implied** (0.77× off) | same |
| Time to sterilisation | prolonged therapy clears Mtb | **infinite** under printed Eq. 4 | `model_endpoints.csv` |
| Eq. 2, *S. aureus* at 240 h | resistant growth | **10⁵⁷ CFU/mL**, 10²⁶× all prokaryotes on Earth | `eq2_unbounded_growth.csv` |
| Eq. 3, *S. aureus* | 15 logs of killing | net rate is **+0.30/h — the population grows** | `eq3_omits_replication.csv` |
| Abstract's implied 200-fold | 0.2/h vs 0.001/h | different equations; like-for-like ratios are **4× (tolerance) and 10× (slow killing)** | claim table |
| Persister fraction | "~3.58%", fitted | inside the assumed 1–5% input range; no fit exists | claim table |
| KS test | p < 0.05 | p ranges 5×10⁻² to 0 purely with **grid density** | `ks_test_grid_dependence.csv` |
| Sensitivity to `k_fast` at 240 h | biologically relevant | **exactly 0** — `k_fast` is absent from that branch | `analytic_elasticities.csv` |
| R² > 0.9 | confirms the model | clears 0.9 for **both** models in 3 of 4 designs, while AICc differs by up to **84** | `r2_vs_aicc_discrimination.csv` |

### Two findings not in the original audit

**Equation 3 omits replication, and this reverses its verdict.** Table 1 gives
*S. aureus* r = 0.5/h and k_T = 0.2/h. The printed tolerance equation has no growth
term, so it reports a 15-log decline; the net rate implied by the same table is
**+0.30/h**, i.e. the population grows to carrying capacity. For Mtb the sign is
correct (r = 0.03 < k_T = 0.05) but the magnitude is still wrong. A tolerance equation
without a replication term cannot be used for an organism whose replication rate is
in the same table.

**`t_c` is not merely over-parameterised, it is unidentifiable in practice.**
Profile likelihood on synthetic data at four sampling designs: the 95% interval for
`t_c` runs to the edge of the searched range in **4 of 4 designs**, and the point
estimate sits on the optimiser bound in 3 of them. The Jacobian condition number for
the printed model reaches 5×10¹⁷ against ~500 for the biexponential.

### One finding that replaces the paper's sensitivity conclusion

The published claim ("Mtb persistence is most sensitive to `k_slow`") is an algebraic
identity. Run properly on a model where every parameter acts at every time, the answer
is different and clinically actionable:

> **87% of the first-order variance in Mtb time-to-sterilisation is carried by
> `k_P→S`, the rate at which dormant cells resume replication** (total-order index
> 0.90). A dormant cell that wakes becomes killable, so the resuscitation rate, not
> the dormant-cell kill rate, sets treatment duration. This is a statement about a
> drug target. The printed equation is structurally incapable of making it.

For *S. aureus* the picture is different again: **61% of the variance in time to
sterilisation comes from parameter interactions**, so no one-at-a-time analysis of
that organism can be trusted regardless of how carefully it is run.

---

## 2. The corrected equations, for the manuscript

Drop-in replacements, all implemented and tested in `src/models/`.

**Eq. 1 — logistic growth.** Correct as printed. The problem is that `K` appears
nowhere else. Apply it.

**Eq. 2 — resistance.** Replace

```
N_R(t) = N₀ e^{(r − k_R)t}                                   ✗ unbounded
dN/dt  = r N (1 − N/K) − k_R N                               ✓ capped at K
```

and note in the text that this is still not a model of resistance. Resistance is an
MIC/EC50 shift, which requires a concentration term (Eq. 5 below).

**Eq. 3 — tolerance.** Replace

```
N_T(t) = N₀ e^{−k_T t}                                       ✗ no replication
dN/dt  = r N (1 − N/K) − k_T N                               ✓ net rate r − k_T
```

**Eq. 4 — persistence.** Two defensible replacements. Prefer the second.

```
                                                             ✗ as printed:
N_P(t) = N_d + (N₀ − N_d) e^{−k_slow(t−t_c)},  t ≥ t_c          jumps to N₀ at t_c
                                                                floors at N_d forever
                                                                4 free parameters

N(t) = N₀ e^{−k_fast t_c} e^{−k_slow(t−t_c)},  t ≥ t_c       ✓ continuous
                                                                sterilises
                                                                t_c still imposed

N(t) = N₀[(1−f) e^{−k_fast t} + f e^{−k_slow t}]             ✓✓ smooth everywhere
                                                                sterilises
                                                                f dimensionless
                                                                3 parameters, identifiable
       with  t_c = ln((1−f)/f) / (k_fast − k_slow)              t_c is an OUTPUT
```

**Eq. 5 (new) — the pharmacodynamic function that makes the three strategies distinct.**

```
k(C) = E_max · C^H / (EC50^H + C^H)

  resistance   →  EC50 increases          MIC moves,  MDK unchanged
  tolerance    →  metabolism slows        MIC unchanged, MDK ×fold
                  (r and E_max together)
  persistence  →  a dormant subpopulation MIC and MDK99 unchanged, MDK99.99 rises
```

Verified numerically in `results/tables/fig06_mic_mdk.csv`:

| variant | MIC fold | MDK99 | MDK99.99 |
|---|---|---|---|
| wild type | 1.0 | 29 h | 152 h |
| resistant (EC50 ×16) | **16.0** | 29 h | 152 h |
| tolerant (metabolism /4) | 1.0 | **117 h** | 257 h |
| persistent (dormancy ×10) | 1.0 | 32 h | **352 h** |

Three orthogonal directions. Note that dividing `E_max` alone is **not** tolerance:
it moves the MIC by about `fold^(1/H)`, which is partial resistance. Tolerance is
`r` and `E_max` scaled together, which is what leaves the MIC exactly invariant.

**Eq. 6 (new) — the structural replacement.**

```
dS/dt = r S (1 − (S+P)/K) − kill_S(C) S − k_SP S + k_PS P
dP/dt =                   − kill_P(C) P + k_SP S − k_PS P
```

Biphasic killing emerges rather than being imposed; there is no `t_c` anywhere in the
model; sterilisation time is finite and computable; concentration enters explicitly,
so MIC, dose and regimen become expressible.

---

## 3. What must be removed from the manuscript

These cannot be repaired by recomputation.

1. **Figure 3 and its caption.** "Experimental data vs. model fitting" — no dataset is
   named anywhere in the manuscript and `data/digitized/` is empty. The replacement
   Figure 3 in `results/figures/` is built on **synthetic** data with a known ground
   truth and is stamped as such on the figure itself. It supports conclusions about the
   estimator and about identifiability; it supports no conclusion about either organism.
2. **"R² > 0.9" and the KS test** (Methods 2.3.3). Recompute R² against a named,
   versioned dataset or delete it; delete the KS test outright.
3. **"SciPy odeint (LSODA) was used to solve the differential equations"** and the Euler
   cross-validation (Methods 2.3.1). Every model in Methods 2.1 is closed-form. Either
   delete the sentence or move to the ODE model, where it becomes true.
4. **"Pandas for handling large datasets"** (Methods 2.3). There is no dataset.
5. **The abstract's transition-time sentence.** It attaches Mtb's 80 h to *S. aureus*
   and calls the larger number "earlier".
6. **The abstract's 0.2/h vs 0.001/h comparison.** Two different parameters from two
   different equations.
7. **"~3.58%"** presented as a fitted persistence fraction.
8. **Sensitivity conclusions** as currently written. Replace with the global analysis.
9. **Five references that do not resolve** and one that is unrelated — see audit §1.5.
   Unchanged and still outstanding.

---

## 4. Code map

```
src/models/
  parameters.py       Table 1 as data, with the OCR column offset resolved
                      and every value flagged as literature-adopted, not extracted
  paper_equations.py  Eqs. 1-4 EXACTLY as printed, defects included. Do not fix.
  corrected.py        drop-in replacements + MDK / time-to-LOD / log-drop metrics
  mechanistic.py      the two-compartment ODE model, MIC, emergent transition time
src/inference/
  synthetic.py        synthetic time-kill generator with known ground truth
  fitting.py          log-scale NLS, censoring, AICc, runs test, profile likelihood
src/experiments/
  exp01_recalculate_equations.py     23 claims -> claim_recalculation.{csv,md}
  exp02_fit_and_identifiability.py   fits, profiles, identifiability verdicts
  exp03_sensitivity.py               OAT (printed + mechanistic) and Sobol
src/figures/
  style.py            one place that decides how every figure looks
  fig01 .. fig07      one module per figure; each also writes its own CSV
run_all.py            reproduces everything in one command
```

Every figure module writes the numbers behind its panels to
`results/tables/figNN_*.csv`, so no figure is the only record of a result.

---

## 5. Deliberate limits

- **Mechanistic parameters are illustrative, not fitted.** They reproduce documented
  qualitative behaviour and are labelled `ILLUSTRATIVE PARAMETERS - not fitted to data`
  on every figure that uses them. Replacing them with values fitted to the hollow-fibre
  datasets in [`data/manifests/datasets.csv`](../data/manifests/datasets.csv) is Stage 4
  of the rebuild plan and requires **no change to any model code**.
- **The synthetic data is a self-consistency check, not validation.** It answers "does
  the estimator recover what generated the data, and are the intervals honest?" It does
  not answer anything about *M. tuberculosis* or *S. aureus*.
- **The Sobol analysis uses ±50% log-uniform ranges** around the illustrative point.
  Once parameters are fitted, rerun it over the posterior instead.
- **`results/tables/model_endpoints.csv` reports `inf`** where an endpoint is genuinely
  unreachable, never a truncated search: the metric functions extend the search window
  up to 10⁶ h before returning infinity.
