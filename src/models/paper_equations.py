"""
Equations 1-4 of the preprint, implemented EXACTLY as printed.

These functions are deliberately faithful, including the defects.  They exist so
that every numerical claim in the paper can be recomputed from its own stated
mathematics, and so that the corrected forms in `corrected.py` can be compared
against them on the same axes.  Do not "fix" anything in this file.
"""
from __future__ import annotations

import numpy as np


def logistic_growth(t, N0: float, K: float, r: float):
    """Eq. 1.  Logistic growth, no antibiotic.

        N(t) = K / (1 + ((K - N0)/N0) e^{-rt})

    Correct and dimensionally consistent.  Note that K appears in no other
    equation in the paper, so the carrying capacity is declared and then never
    applied to any antibiotic-exposure scenario.
    """
    t = np.asarray(t, dtype=float)
    return K / (1.0 + ((K - N0) / N0) * np.exp(-r * t))


def resistance_as_printed(t, N0: float, r: float, k_R: float):
    """Eq. 2.  Resistance.

        N_R(t) = N0 e^{(r - k_R) t}

    Unbounded exponential growth: no carrying-capacity term.  Also note this is
    structurally identical to Eq. 3 with a different constant, so as printed the
    model does not distinguish resistance from tolerance.  Resistance is an
    MIC/EC50 shift, not a smaller first-order kill constant.
    """
    t = np.asarray(t, dtype=float)
    return N0 * np.exp((r - k_R) * t)


def tolerance_as_printed(t, N0: float, k_T: float):
    """Eq. 3.  Tolerance.

        N_T(t) = N0 e^{-k_T t}

    Mono-exponential decay is the correct signature of tolerance.  The defect is
    definitional rather than algebraic: tolerance is defined only relative to a
    susceptible comparator (increased MDK at unchanged MIC), and the model
    contains no comparator.
    """
    t = np.asarray(t, dtype=float)
    return N0 * np.exp(-k_T * t)


def persistence_as_printed(t, N0: float, k_fast: float, k_slow: float,
                           f_dormant: float, t_c: float):
    """Eq. 4.  Persistence / biphasic killing, exactly as printed.

        N_P(t) = N0 e^{-k_fast t}                      for t <  t_c
               = N_d + (N0 - N_d) e^{-k_slow (t-t_c)}  for t >= t_c

    with N_d = f_dormant * N0.

    Four defects, all reproduced here:
      (i)   discontinuity: at t = t_c the second branch equals exactly N0,
            regardless of how much killing happened in phase 1, so the
            population is resurrected upward at the transition;
      (ii)  lim_{t->inf} N_P(t) = N_d > 0, a permanent floor: no regimen of any
            duration can sterilise;
      (iii) N_d carries units of CFU in Eq. 4 but is a dimensionless fraction in
            Table 1;
      (iv)  t_c is treated as a free parameter although in a biexponential
            population it is determined by k_fast, k_slow and f.
    """
    t = np.asarray(t, dtype=float)
    N_d = f_dormant * N0
    fast = N0 * np.exp(-k_fast * t)
    slow = N_d + (N0 - N_d) * np.exp(-k_slow * (t - t_c))
    return np.where(t < t_c, fast, slow)


def transition_jump(N0: float, k_fast: float, f_dormant: float, t_c: float):
    """Size of the Eq. 4 discontinuity at t_c.

    Returns (N_left, N_right, fold_change, log10_fold_change) where N_left is
    the limit from below and N_right the value of the second branch at t_c.
    """
    N_left = N0 * np.exp(-k_fast * t_c)
    N_right = f_dormant * N0 + (N0 - f_dormant * N0) * 1.0
    fold = N_right / N_left
    return N_left, N_right, fold, float(np.log10(fold))


def implied_t_c(k_fast: float, k_slow: float, f_dormant: float) -> float:
    """The crossover time implied by a true biexponential population.

        N(t) = N0[(1-f) e^{-k_fast t} + f e^{-k_slow t}]

    The two terms are equal when

        t_c = ln((1-f)/f) / (k_fast - k_slow)

    so t_c is an OUTPUT of (k_fast, k_slow, f), not a fourth free parameter.
    """
    return float(np.log((1.0 - f_dormant) / f_dormant) / (k_fast - k_slow))


def euler_solution(rhs, N0: float, t_max: float, dt: float):
    """Explicit Euler, as described in Methods 2.3.1 (dt = 0.5 h).

    Provided so the paper's stated "cross-validation" can be reproduced and its
    logic examined: every model in Methods 2.1 is a closed-form algebraic
    solution, so there is nothing for a solver to integrate and agreement
    between Euler and an analytic formula tests the arithmetic of Euler, not the
    model.
    """
    n = int(round(t_max / dt)) + 1
    t = np.linspace(0.0, t_max, n)
    N = np.empty(n, dtype=float)
    N[0] = N0
    for i in range(n - 1):
        N[i + 1] = N[i] + dt * rhs(t[i], N[i])
    return t, N
