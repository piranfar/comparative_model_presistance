"""
Synthetic time-kill data generator.

WHY THIS EXISTS, STATED PLAINLY. The preprint's Figure 3 is captioned
"Experimental data vs. model fitting" but the paper names no dataset, and
`data/digitized/` is empty. There is therefore no experimental data in this
project to fit, and none is invented here and passed off as real.

What this module provides instead is a synthetic generator with a KNOWN ground
truth, which supports two legitimate uses:

  1. a self-consistency check on the fitting machinery: given data produced by a
     model, does the estimator recover the parameters that produced it, and are
     the reported confidence intervals honest?
  2. a structural identifiability test: can the printed four-parameter Eq. 4 be
     estimated at all from data of the type and density the paper's own Methods
     describe?

Neither is validation against experiment, and no figure or table produced from
this module may be labelled as such. Every output carries a SYNTHETIC tag.

The noise model follows the datasets in data/manifests/datasets.csv: additive
Gaussian noise on log10 CFU/mL (plating error is multiplicative on the count
scale), left-censoring at a limit of detection, and replicate plating.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..models.mechanistic import PDParams, simulate

SYNTHETIC_TAG = "SYNTHETIC (no experimental data in project)"


@dataclass(frozen=True)
class SyntheticDataset:
    """One synthetic time-kill arm."""

    label: str
    t: np.ndarray            # sampling times, h
    log10_cfu: np.ndarray    # observed log10 CFU/mL, censored at LOD
    censored: np.ndarray     # bool, True where the observation is at the LOD
    sigma: float             # noise SD on log10 CFU/mL
    lod: float               # limit of detection, CFU/mL
    n_replicates: int
    truth: dict              # ground-truth parameters used to generate it
    tag: str = SYNTHETIC_TAG


# Sampling schedules.
#
# A schedule must span the organism's own kill window, otherwise most
# observations land at the limit of detection and the comparison measures the
# design rather than the model. Published studies do exactly this: the 240 h
# schedule below is TSUJI2012's from data/manifests/datasets.csv, appropriate
# for a slow grower, while fast-killing arms are sampled over 48 h.
#
# Two densities are provided for each window so the identifiability verdict can
# be attributed to the model structure rather than to sparse sampling.

SLOW_SPARSE_H = np.array([0., 24., 48., 72., 96., 144., 192., 240.])
SLOW_DENSE_H = np.array([0., 6., 12., 24., 36., 48., 72., 96., 120., 144.,
                         168., 192., 216., 240.])

FAST_SPARSE_H = np.array([0., 2., 4., 8., 12., 24., 36., 48.])
FAST_DENSE_H = np.array([0., 1., 2., 3., 4., 6., 8., 10., 12., 16., 20., 24.,
                         30., 36., 42., 48.])

# Kept as aliases so older call sites keep working.
HFIM_SAMPLING_H = SLOW_SPARSE_H
DENSE_SAMPLING_H = SLOW_DENSE_H

SCHEDULES = {
    "Mtb": {"sparse (8-point, 240 h)": SLOW_SPARSE_H,
            "dense (14-point, 240 h)": SLOW_DENSE_H},
    "S. aureus": {"sparse (8-point, 48 h)": FAST_SPARSE_H,
                  "dense (16-point, 48 h)": FAST_DENSE_H},
}


def generate(p: PDParams, C: float, t_sample=HFIM_SAMPLING_H,
             N0: float = 1.0e6, sigma: float = 0.25, lod: float = 1.0e2,
             n_replicates: int = 3, seed: int = 20250212,
             label: str = "") -> SyntheticDataset:
    """Draw one synthetic arm from the mechanistic model.

    `sigma` is the SD of additive noise on log10 CFU/mL for a single plate;
    the reported value is the mean of `n_replicates` plates, so its SD is
    sigma/sqrt(n_replicates).
    """
    rng = np.random.default_rng(seed)
    t_sample = np.asarray(t_sample, dtype=float)
    out = simulate(p, C, t_sample, N0=N0)
    true_log10 = np.log10(np.maximum(out["total"], 1e-300))

    se = sigma / np.sqrt(n_replicates)
    obs = true_log10 + rng.normal(0.0, se, size=true_log10.shape)

    lod_log10 = np.log10(lod)
    censored = obs < lod_log10
    obs = np.where(censored, lod_log10, obs)

    return SyntheticDataset(
        label=label or f"{p.label} at {C:g}xMIC",
        t=t_sample,
        log10_cfu=obs,
        censored=censored,
        sigma=se,
        lod=lod,
        n_replicates=n_replicates,
        truth={
            "source_model": "two-compartment mechanistic (mechanistic.py)",
            "C_xMIC": C,
            "N0": N0,
            "Emax_S": p.Emax_S,
            "Emax_P": p.Emax_P,
            "EC50": p.EC50,
            "H": p.H,
            "k_SP": p.k_SP,
            "k_PS": p.k_PS,
            "r": p.r,
            "persister_fraction_eq": p.persister_fraction_eq,
        },
    )
