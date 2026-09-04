"""
Corrected closed-form replacements for Equations 1-4.

Each function here fixes one named defect of the printed equation while staying
as close to the original structure as possible, so a reader of the paper can see
exactly what changed. The deeper structural fix, encoding resistance, tolerance
and persistence as genuinely different mechanisms rather than as one exponential
with three different constants, is in `mechanistic.py`.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


# ---------------------------------------------------------------- growth ----

def logistic_with_kill(t, N0: float, K: float, r: float, k: float):
    """Logistic growth with a first-order kill term, closed form.

        dN/dt = r N (1 - N/K) - k N

    This is again logistic, with an effective growth rate and carrying capacity

        r_eff = r - k        K_eff = K (r - k) / r

    so the solution is

        N(t) = K_eff / (1 + ((K_eff - N0)/N0) e^{-r_eff t})

    Fixes the defect that Eq. 2 grows without bound: applying the carrying
    capacity the Methods already declare removes the 10^51-fold expansion.
    """
    t = np.asarray(t, dtype=float)
    r_eff = r - k
    if abs(r_eff) < 1e-12:
        # dN/dt = -r N^2 / K
        return N0 / (1.0 + r * N0 * t / K)
    K_eff = K * r_eff / r
    a = (K_eff - N0) / N0
    return K_eff / (1.0 + a * np.exp(-r_eff * t))


# ------------------------------------------------------- persistence, fix 1 --

def persistence_continuous(t, N0: float, k_fast: float, k_slow: float,
                           t_c: float):
    """Continuous piecewise biphasic decay, the minimum correct patch to Eq. 4.

        N(t) = N0 e^{-k_fast t}                              t <  t_c
             = N0 e^{-k_fast t_c} e^{-k_slow (t - t_c)}      t >= t_c

    Removes defect (i) the resurrection at t_c, (ii) the immortal floor, and
    (iii) the units clash, because the dormant fraction no longer appears as an
    additive count. Continuous but not differentiable at t_c, and t_c is still
    imposed rather than emergent, so defect (iv) survives.
    """
    t = np.asarray(t, dtype=float)
    N_tc = N0 * np.exp(-k_fast * t_c)
    return np.where(t < t_c,
                    N0 * np.exp(-k_fast * t),
                    N_tc * np.exp(-k_slow * np.maximum(t - t_c, 0.0)))


# ------------------------------------------------------- persistence, fix 2 --

def biexponential(t, N0: float, k_fast: float, k_slow: float, f: float):
    """Two-subpopulation biexponential decay, the recommended replacement.

        N(t) = N0 [ (1 - f) e^{-k_fast t} + f e^{-k_slow t} ]

    Smooth everywhere, sterilises as t grows, f is dimensionless throughout, and
    the transition time is an OUTPUT rather than a fitted parameter:

        t_c = ln((1-f)/f) / (k_fast - k_slow)

    Three parameters describe a three-parameter system, so the model is
    structurally identifiable where the printed four-parameter version is not.
    """
    t = np.asarray(t, dtype=float)
    return N0 * ((1.0 - f) * np.exp(-k_fast * t) + f * np.exp(-k_slow * t))


def biexponential_log10(t, log10_N0: float, k_fast: float, k_slow: float,
                        logit_f: float):
    """Biexponential on the log10 scale, in a fitting-friendly parameterisation.

    CFU data span orders of magnitude and are homoscedastic in log space, so
    fits must be done on log10 CFU. The dormant fraction is passed through a
    logit so the optimiser works on an unconstrained space.
    """
    N0 = 10.0 ** log10_N0
    f = 1.0 / (1.0 + np.exp(-logit_f))
    return np.log10(np.maximum(biexponential(t, N0, k_fast, k_slow, f), 1e-300))


def persistence_as_printed_log10(t, log10_N0: float, k_fast: float,
                                 k_slow: float, logit_f: float, t_c: float):
    """The printed four-parameter Eq. 4 on the log10 scale.

    Used only to demonstrate that fitting four free parameters to a
    three-parameter system is structurally non-identifiable.
    """
    from .paper_equations import persistence_as_printed
    N0 = 10.0 ** log10_N0
    f = 1.0 / (1.0 + np.exp(-logit_f))
    val = persistence_as_printed(t, N0, k_fast, k_slow, f, t_c)
    return np.log10(np.maximum(val, 1e-300))


# ------------------------------------------------- pharmacodynamic functions --

def hill_kill(C, Emax: float, EC50: float, H: float = 1.0):
    """Sigmoid Emax (Hill) kill rate as a function of drug concentration.

        k(C) = Emax C^H / (EC50^H + C^H)

    This is the function that makes the three survival strategies distinct.
    Resistance raises EC50, so the concentration-response curve shifts right and
    the MIC changes. Tolerance lowers Emax, so the maximum achievable kill rate
    falls while the MIC is unchanged and MDK rises. Persistence adds a
    subpopulation with its own much smaller Emax, so population MIC and bulk
    Emax are unchanged and only the tail of the kill curve moves.
    """
    C = np.asarray(C, dtype=float)
    return Emax * C ** H / (EC50 ** H + C ** H)


# ------------------------------------------------------------------ metrics --

def _first_crossing(curve, t_grid, target: float):
    """First time at which `curve` falls to `target`, by bracketing + brentq."""
    vals = np.asarray(curve(t_grid), dtype=float)
    below = np.where(vals <= target)[0]
    if below.size == 0:
        return float("inf")
    i = int(below[0])
    if i == 0:
        return 0.0
    lo, hi = float(t_grid[i - 1]), float(t_grid[i])

    def g(x):
        return float(np.atleast_1d(curve(np.array([x])))[0]) - target

    try:
        return float(brentq(g, lo, hi, xtol=1e-9))
    except ValueError:
        return hi


def _adaptive_crossing(curve, target: float, t_max: float, n: int,
                       t_cap: float) -> float:
    """Search for a crossing, doubling the window until `t_cap` before giving up.

    Returning inf therefore means "no crossing exists up to t_cap", which for a
    model with a permanent floor above `target` is the correct answer, and is
    distinguishable from a search window that was merely too short.
    """
    window = float(t_max)
    while True:
        hit = _first_crossing(curve, np.linspace(0.0, window, n), target)
        if np.isfinite(hit):
            return hit
        if window >= t_cap:
            return float("inf")
        window = min(window * 4.0, t_cap)


def mdk(curve, N0: float, percent: float, t_max: float = 5.0e3,
        n: int = 50_001, t_cap: float = 1.0e6) -> float:
    """Minimum duration for killing, MDK_x.

    Time at which the surviving fraction first reaches (1 - percent/100).
    MDK99 is a 2-log drop, MDK99.99 a 4-log drop. Returns inf only when no
    crossing exists within `t_cap` hours, which for the printed Eq. 4 is a
    genuine consequence of its permanent floor rather than a truncated search.
    """
    target = N0 * (1.0 - percent / 100.0)
    return _adaptive_crossing(curve, target, t_max, n, t_cap)


def time_to_lod(curve, lod: float, t_max: float = 5.0e3,
                n: int = 50_001, t_cap: float = 1.0e6) -> float:
    """Time at which the population first falls below a limit of detection."""
    return _adaptive_crossing(curve, lod, t_max, n, t_cap)


def log10_drop(curve, N0: float, t: float) -> float:
    """log10 reduction from inoculum at time t. Positive means killing."""
    val = float(np.atleast_1d(np.asarray(curve(np.array([t])), dtype=float))[0])
    return float(np.log10(N0) - np.log10(max(val, 1e-300)))
