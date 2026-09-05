"""
The Boccarella et al. (2026) survival model, re-implemented from their code.

Source: Boccarella G, Ruelens P, Berrios-Caro E, Van den Bergh B, Cool L,
Michiels J, van den Berg P. "Bacterial Persistence Modulates the Speed,
Magnitude, and Onset of Antibiotic Resistance Evolution." Mol Biol Evol.
2026;43(8):msag180. doi:10.1093/molbev/msag180. Code and data deposited at
doi:10.6084/m9.figshare.31389142 under CC BY 4.0.

Every constant below is taken from their deposited `magnitude_of_evolution_
simulations.py`, not from the manuscript, because the two disagree in two
places that are recorded in DISCREPANCIES at the bottom of this file.

The object of interest is the fraction of a population that survives one
antibiotic pulse of duration tau at concentration c:

    S(alpha) = (1 - alpha) * exp(psi_n * tau) + alpha * exp(psi_p * tau)

where psi_n and psi_p are the net per-capita growth rates of the normal and
persister compartments, each built from a Regoes-type pharmacodynamic function.
alpha is the fraction of cells that enter the protected state at pulse onset.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# ---- constants, verbatim from their deposited simulation script ------------
B_S = 1.7          # module-level birth rate, used as min_bR in main()
D_S = 1.0          # death rate, normal cells
B_P = 0.0          # birth rate, persisters: they do not replicate
D_P = 0.1          # death rate, persisters
MAX_BR = 2.0       # mic_to_br upper anchor
MIN_MIC, MAX_MIC = 1.0, 32.0
PSI_MAX_PR = 0.05          # persister maximum net growth rate
MIN_VALUE = -0.5           # persister psi_min anchor at MIC = MIN_MIC
MIN_MIC_THRESHOLD = 6.25   # above this MIC the persister psi_min is 0

# values set in their main() loop, which override the function defaults
KAPPA = 2.0        # Hill coefficient
PSI_MIN_S = -6.0   # normal-cell minimum net growth rate
PERS_COST = 0.0    # growth cost of persistence
TAU_TREAT = 5.0    # antibiotic exposure per daily cycle, hours
TAU_GROW = 19.0    # regrowth per daily cycle, hours
MIC_WT = 2.0       # wild-type MIC, ug/mL

# the two persistence levels they simulate
ALPHA_HIGH = 0.8
ALPHA_LOW = 5e-5


def mic_to_br(mic: float, min_br: float = B_S) -> float:
    """Birth rate as a function of MIC, their `mic_to_br`."""
    return MAX_BR - (MAX_BR - min_br) * (mic - MIN_MIC) / (MAX_MIC - MIN_MIC)


def mic_mapping(mic: float, min_value: float = MIN_VALUE,
                min_mic_threshold: float = MIN_MIC_THRESHOLD) -> float:
    """Persister psi_min as a function of MIC, their `mic_mapping`."""
    if mic >= min_mic_threshold:
        return 0.0
    return min_value + (0.0 - min_value) * (mic - MIN_MIC) / (min_mic_threshold - MIN_MIC)


def _regoes_reduction(x: float, psi_max: float, psi_min: float,
                      kappa: float) -> float:
    """The `a` term of the Regoes pharmacodynamic function, as they code it.

        a = (psi_max - psi_min) * x^k / (x^k - psi_min/psi_max),   x = c / MIC

    The net growth rate is then psi_max - a. Written this way to match their
    implementation exactly, including its behaviour when psi_max is small.
    """
    xk = x ** kappa
    return (psi_max - psi_min) * xk / (xk - psi_min / psi_max)


def net_rates(c: float, mic: float = MIC_WT, alpha: float = 0.0,
              d_p: float = D_P, psi_max_pr: float = PSI_MAX_PR,
              min_value: float = MIN_VALUE, psi_min_s: float = PSI_MIN_S,
              kappa: float = KAPPA,
              min_mic_threshold: float | None = None) -> tuple[float, float]:
    """Net per-capita growth rates (psi_normal, psi_persister) at concentration c.

    Reproduces their per-capita birth and death bookkeeping at low density,
    where the density term N/K is negligible relative to the birth rate.

    NOTE on min_mic_threshold. Their `mic_mapping` carries a default of 6.25,
    but `run_simulation_with_mic` overrides it with `min_mic_threshold = c`,
    tying the persister pharmacodynamic anchor to the antibiotic concentration.
    That override is what the published runs used, so it is the default here.
    Missing it makes the persister compartment look more drug-tolerant than the
    authors' model actually is.
    """
    b_r = mic_to_br(mic)
    if c <= 0:
        return b_r * (1.0 - PERS_COST * alpha) - D_S, B_P - d_p
    if min_mic_threshold is None:
        min_mic_threshold = c

    psi_max_r = b_r - D_S
    a_r = _regoes_reduction(c / mic, psi_max_r, psi_min_s, kappa)
    psi_n = b_r * (1.0 - PERS_COST * alpha) - (D_S + a_r)

    psi_min_pr = mic_mapping(mic, min_value=min_value,
                             min_mic_threshold=min_mic_threshold)
    a_pr = _regoes_reduction(c / mic, psi_max_pr, psi_min_pr, kappa)
    # their birth term for persisters is max(0, b_P - N/K), which is 0
    psi_p = 0.0 - (d_p + a_pr)
    return psi_n, psi_p


def survival(alpha, c: float, tau: float = TAU_TREAT, mic: float = MIC_WT,
             **kw):
    """Surviving fraction after one pulse. `alpha` may be an array."""
    alpha = np.asarray(alpha, dtype=float)
    psi_n, psi_p = net_rates(c, mic=mic, alpha=float(np.mean(alpha)), **kw)
    return (1.0 - alpha) * np.exp(psi_n * tau) + alpha * np.exp(psi_p * tau)


def persister_survival_factor(c: float, tau: float = TAU_TREAT,
                              mic: float = MIC_WT, **kw) -> float:
    """exp(psi_p * tau): the fraction of persisters that survive one pulse.

    This is the quantity that multiplies alpha. Because the normal-cell term is
    of order 1e-11 at the concentrations used in the experiment, the observed
    survival is essentially alpha times this factor, which is why the two cannot
    be estimated separately from survival data alone.
    """
    _, psi_p = net_rates(c, mic=mic, **kw)
    return float(np.exp(psi_p * tau))


def normal_survival_factor(c: float, tau: float = TAU_TREAT,
                           mic: float = MIC_WT, **kw) -> float:
    """exp(psi_n * tau): the fraction of normal cells that survive one pulse."""
    psi_n, _ = net_rates(c, mic=mic, **kw)
    return float(np.exp(psi_n * tau))


@dataclass(frozen=True)
class Discrepancy:
    item: str
    manuscript: str
    deposited_code: str
    consequence: str


# Differences between the printed manuscript and the deposited code. Both were
# checked directly; neither is a criticism of the result, but any re-use has to
# pick one and say which.
DISCREPANCIES = [
    Discrepancy(
        item="sigma, the standard deviation of the log-normal distribution of "
             "mutational effects on MIC",
        manuscript="Table 1 gives sigma = 0.07",
        deposited_code="main() sets sigma_values = [0.7]",
        consequence="a ten-fold difference in the spread of mutational effect "
                    "sizes, which is the quantity the large-effect versus "
                    "small-effect argument rests on",
    ),
    Discrepancy(
        item="Hill coefficient kappa",
        manuscript="Table 1 gives h = 2",
        deposited_code="function default is kappaS = 3, but main() overrides "
                       "it to 2, so the manuscript value is the one used",
        consequence="none for the published runs; a trap for anyone who calls "
                    "the function without setting kappaS",
    ),
]
