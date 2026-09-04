# Comparative modelling of antibiotic resistance, tolerance and persistence

Code and results for bioRxiv preprint
[10.1101/2025.02.12.637810](https://doi.org/10.1101/2025.02.12.637810),
*A state-structured pharmacodynamic framework separating resistance, tolerance
and persistence, applied to Mycobacterium tuberculosis and Staphylococcus aureus*.

> **Version 2 corrects errors in version 1 that change its conclusions.**
> Readers of version 1 should treat its quantitative results as withdrawn. The
> full list of corrections, each tied to the computation that establishes it, is
> in [`manuscript/CORRECTIONS_LOG.md`](manuscript/CORRECTIONS_LOG.md).

```bash
pip install -r requirements.txt
python run_all.py
```

Regenerates every number and every figure in the manuscript in about two minutes.
No network access. Needs numpy, scipy, pandas and matplotlib; the pinned versions
this was last verified on are in [`requirements.txt`](requirements.txt), and every
stage writes the versions it actually ran under to `results/receipts/`.

## What is here

| | |
|---|---|
| [`manuscript/`](manuscript/) | the version 2 manuscript and the corrections log |
| [`submission/biorxiv_v2/`](submission/biorxiv_v2/) | the submitted document and figure files |
| [`src/models/`](src/models/) | the version 1 equations implemented exactly as printed, the corrected closed forms, and the state-structured replacement |
| [`src/inference/`](src/inference/) | log-scale fitting with censoring, information criteria, profile likelihood, and the synthetic data generator |
| [`src/experiments/`](src/experiments/) | the three analysis stages |
| [`src/figures/`](src/figures/) | one module per figure; each also writes the numbers behind its panels |
| [`results/`](results/) | tables, figures and run receipts recording library versions |
| [`docs/`](docs/) | the audit that motivated the revision, the study design, and the reference verification |

## The corrections, in one table

Twenty-three quantitative claims from version 1 were recomputed from its own
equations and its own parameter table. Twenty fail, two are partial, one passes.

| Claim in version 1 | Recomputed |
|---|---|
| Biphasic killing, Eq. 4 | rises by 2,981-fold (3.47 log₁₀) at the transition, for *M. tuberculosis* |
| Prolonged therapy clears *M. tuberculosis* | time to sterilisation is infinite under the printed equation |
| Transition time 80 h, fitted | 33.3 h implied by the other three parameters; not identifiable from realistic data |
| Resistant growth, Eq. 2 | 10⁵⁷ CFU/mL at 240 h, exceeding the prokaryotic biomass of Earth |
| Tolerance kills *S. aureus*, Eq. 3 | net rate is +0.30/h; the population grows |
| The two species differ markedly | 1.13-fold apart at 240 h once the discontinuity is removed |
| R² > 0.9 confirms the model | both a correct and a broken model exceed 0.9 while AICc differs by 81.5 |
| Kolmogorov–Smirnov p < 0.05 | the p-value is set by the simulation grid density, not by the biology |

Full table with verdicts: [`results/tables/claim_recalculation.md`](results/tables/claim_recalculation.md).

## Status of the data

**There is no experimental data in this project.** Version 1's experimental-data figure was
captioned "experimental data vs. model fitting" and named no dataset; it is
withdrawn. Figures built on synthetic data carry a `SYNTHETIC DATA` stamp, and
figures using unfitted parameters carry `ILLUSTRATIVE PARAMETERS`. Neither
supports any quantitative claim about either organism.

Candidate real datasets, verified to exist, are catalogued in
[`data/manifests/datasets.csv`](data/manifests/datasets.csv). Fitting the
state-structured model to them requires no change to any model code.

## References

All thirty references in version 1 were checked against PubMed. Seventeen
verified, eleven required correction, two do not exist and are removed. The audit
is in [`docs/04_REFERENCE_VERIFICATION.md`](docs/04_REFERENCE_VERIFICATION.md)
and every PubMed-indexed entry in the version 2 list carries its PMID.

## Licence

Code under the MIT licence, see [`LICENSE`](LICENSE). Documentation and figures
under CC BY 4.0.

## Citation

Piranfar V. *A state-structured pharmacodynamic framework separating resistance,
tolerance and persistence, applied to Mycobacterium tuberculosis and
Staphylococcus aureus.* bioRxiv 2025.02.12.637810, version 2.
