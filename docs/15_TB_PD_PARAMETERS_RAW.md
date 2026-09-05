> **STATUS: UNVERIFIED SOURCE MATERIAL. DO NOT CITE FROM THIS FILE.**
>
> Supplied by the author on 2026-09-05 as a compilation produced by a language
> model, with reference markers of the form `[7 dagger L6]` that are retrieval
> anchors rather than citations. Nothing here has been checked against a primary
> source at the time of writing. It is kept because the underlying papers are
> named and therefore checkable, not because the numbers are established.
>
> This project has already had to discard two PMIDs recalled from memory and has
> documented several fabricated references in the original draft (see
> `docs/04_REFERENCE_VERIFICATION.md`). Every number below must be traced to the
> paper and confirmed against the published table before it appears in any
> manuscript. Verified values, once established, belong in a separate file; this
> one stays as the record of what was claimed and by whom.
>
> Two specific traps identified on receipt:
>
> 1. `Emax` is reported in two incompatible ways in the same table: as a total
>    log10 CFU/mL reduction over a fixed window (7 or 21 days), and as a rate in
>    per-hour units. Only the second is comparable to `psi_min` in the Regoes
>    form. A Hill coefficient fitted to the first saturates when the population is
>    exhausted, not when the drug effect is, so it is not the same quantity as
>    `kappa` even though both are called a Hill coefficient.
> 2. Rifampicin's Hill coefficient appears as 0.49 and 0.61 in one study and 1.90
>    in another, both from 7-day static time-kill. That fourfold disagreement must
>    be resolved before either value is used.

---

# Pharmacodynamic Parameters for *Mycobacterium tuberculosis*

This document compiles published pharmacodynamic (PD) parameters—specifically the Hill coefficient (κ or *h*) and maximum kill rate (often denoted as *E_max* or *k_max*)—for *Mycobacterium tuberculosis* (*Mtb*), derived from hollow-fiber and static time-kill studies.

---

## Core Pharmacodynamic Parameter Summary

| Drug | Bacterial State / Model | Hill Coefficient (*h*) | Maximum Effect (*E_max*) | Notes | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rifampin (RIF)** | Extracellular / Model Parameter | 0.5 | 0.019 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Intracellular / Model Parameter | 0.5 | 0.014 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Strain IMV (7-day static time-kill) | 0.49 [0.41–0.58] | 7.1 [6.6–7.7] (log₁₀ CFU/mL decrease) | Static time-kill | [16†L9-L14] |
| | Strain 4MBE (7-day static time-kill) | 0.61 [0.49–0.74] | 6.9 [6.1–7.7] (log₁₀ CFU/mL decrease) | Static time-kill | [16†L9-L14] |
| | Log-phase growth cells (7-day) | 1.90 (1.29–2.52) | 5.74 (5.00–6.48) (log₁₀ CFU/mL) | Static time-kill | [8†L3-L5] |
| | Intracellular (macrophage) | — | 0.055 (h⁻¹) | *E_max* in h⁻¹ | [7†L6] |
| | Extracellular (liquid culture) | — | 0.178 (h⁻¹) | *E_max* in h⁻¹ | [7†L6] |
| **Isoniazid (INH)** | Extracellular / Model Parameter | 1 | 0.0056 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Intracellular / Model Parameter | 1 | 0.0056 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Log-phase growth cells (7-day) | 0.82 (0.49–1.15) | 5.72 (4.73–6.71) (log₁₀ CFU/mL) | Static time-kill | [8†L6-L8] |
| | Intracellular (macrophage) | — | 0.041 (h⁻¹) | *E_max* in h⁻¹ | [7†L7-L8] |
| | Extracellular (liquid culture) | — | 0.710 / 0.055 (h⁻¹) | *E_max* in h⁻¹ | [7†L7-L8] |
| **Ethambutol (EMB)** | Extracellular / Model Parameter | 1.5 | 0.025 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Intracellular / Model Parameter | 2.5 | 0.026 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Intracellular (macrophage) | — | 0.053 (h⁻¹) | *E_max* in h⁻¹ | [7†L7] |
| | Extracellular (liquid culture) | — | 0.142 (h⁻¹) | *E_max* in h⁻¹ | [7†L7] |
| **Pyrazinamide (PZA)** | Extracellular / Model Parameter | 1 | 0.007 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Intracellular / Model Parameter | 3.2 | 0.0006 (1/model time step) | Fitted parameter | [1†L15-L16] |
| | Human THP-1 Macrophages (hollow-fiber) | 3.03 ± 0.79 | 1.05 ± 0.13 (log₁₀ CFU/mL) | Hollow-fiber model | [6†L7-L10] |
| | Murine J774A.1 Macrophages (hollow-fiber) | 1.18 ± 0.44 | 1.47 ± 0.14 (log₁₀ CFU/mL) | Hollow-fiber model | [6†L18-L22] |
| | Semidormant bacilli (SDB, 21-day) | 1.94 (0–5.42) | 2.38 (0–4.83) (log₁₀ CFU/mL) | Static time-kill | [8†L10-L11] |
| | Intracellular (macrophage) | — | 0.043 (h⁻¹) | *E_max* in h⁻¹ | [7†L8-L9] |
| **Amikacin** | Log-phase (hollow-fiber) | — | 5.39 (95% CI: 4.91–5.63) (log₁₀ CFU/mL) | Hollow-fiber system | [9†L15-L17] |
| | Semidormant at pH 5.8 (hollow-fiber) | — | 4.88 (95% CI: 4.46–5.22) (log₁₀ CFU/mL) | Hollow-fiber system | [9†L15-L17] |
| **Bedaquiline** | Pulmonary TB patients (PK/PD model) | — | 0.23 ± 0.03 (log₁₀ CFU/mL sputum/day) | Maximum drug kill rate constant | [10†L17-L19] |

---

## Additional Notes

- **Parameter Definitions**: The **Hill coefficient (κ or *h*)** represents the slope of the concentration-effect curve. The **maximum effect (*E_max* or *k_max*)** represents the maximum bactericidal rate achievable by the drug.
- **Data Heterogeneity**: PD parameter values vary significantly depending on bacterial strain, experimental system (hollow-fiber vs. static), bacterial metabolic state (intracellular vs. extracellular, replicating vs. non-replicating), and model structure. For example, pyrazinamide's Hill coefficient differs markedly between human and murine macrophage models [6†L7-L10][6†L18-L22].
- **Literature Sources**: These parameters are primarily derived from pharmacokinetic/pharmacodynamic (PK/PD) modeling studies. Raw data originate from *in vitro* experiments and are obtained through model fitting.
- **Static Time-Kill Studies**: In static time-kill experiments, drug concentration remains fixed over time, and bacterial response is measured as change in optical density and/or colony-forming units (CFU) [5†L25-L27].

---

## References

1. Table 1: Comparison of growth and pharmacodynamic killing kinetics for planktonic (extracellular liquid culture) and intracellular (macrophage) *M. tuberculosis*. *Nature* (2017). [7†L2-L9]

2. Table 4: Antibiotic pharmacodynamic parameters (EC₅₀, E_max, Hill factor) for *M. tuberculosis* populations. *PMC* (2013). [8†L2-L19]

3. A Long-term Co-perfused Disseminated Tuberculosis-3D Liver Hollow Fiber Model for Both Drug Efficacy and Hepatotoxicity in Babies. *Europe PMC* (2016). [6†L2-L24]

4. Amikacin Optimal Exposure Targets in the Hollow-Fiber System Model of Tuberculosis. *Antimicrobial Agents and Chemotherapy* (2016). [9†L3-L19]

5. Pharmacodynamics and Bactericidal Activity of Bedaquiline in Pulmonary Tuberculosis. *Antimicrobial Agents and Chemotherapy* (2021). [10†L3-L20]

6. Assessing the Combined Antibacterial Effect of Isoniazid and Rifampin on Four *Mycobacterium tuberculosis* Strains Using In Vitro Experiments and Response-Surface Modeling. *Antimicrobial Agents and Chemotherapy* (2017). [16†L9-L14]

7. Pharmacokinetics and pharmacodynamics of anti-tuberculosis drugs: An evaluation of in vitro, in vivo methodologies and human studies. *Frontiers in Pharmacology* (2022). [5†L3-L28]