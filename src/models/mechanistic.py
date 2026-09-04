"""
State-structured pharmacodynamic model: the structural fix.

The printed paper encodes resistance, tolerance and persistence as one
first-order exponential with three different rate constants, which makes them
mathematically indistinguishable. This module encodes them as three different
things, following the operational definitions of Brauner, Fridman, Gefen and
Balaban (2016), Nat Rev Microbiol 14:320-30:

    resistance   an MIC/EC50 shift            -> EC50 multiplier
    tolerance    slower kill at unchanged MIC -> Emax multiplier
    persistence  subpopulation structure      -> a dormant compartment with its
                                                 own Emax, plus switching rates

Two compartments, S (actively replicating) and P (dormant persister):

    dS/dt = r S (1 - (S+P)/K) - kill_S(C) S - k_SP S + k_PS P
    dP/dt =                   - kill_P(C) P + k_SP S - k_PS P

with kill_i(C) = Emax_i C^H / (EC50_i^H + C^H).

Properties the printed Eq. 4 lacks:
  * biphasic killing emerges from the two compartments, it is not imposed by a
    hand-placed breakpoint, and there is no discontinuity anywhere;
  * the population sterilises for any Emax_P > 0, so treatment duration is a
    finite computed quantity rather than infinite by construction;
  * the transition time is a derived observable;
  * the carrying capacity is actually used;
  * concentration enters explicitly, so MIC and MDK are separate observables and
    the three strategies have different signatures in the (MIC, MDK) plane.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from .corrected import hill_kill


@dataclass(frozen=True)
class PDParams:
    """Pharmacodynamic parameters for one species and drug pair."""

    label: str
    r: float          # replication rate of S, 1/h
    K: float          # carrying capacity, CFU/mL
    Emax_S: float     # maximum kill rate of the replicating compartment, 1/h
    Emax_P: float     # maximum kill rate of the dormant compartment, 1/h
    EC50: float       # concentration for half-maximal kill, in units of MIC
    H: float          # Hill coefficient
    k_SP: float       # switching S -> P, 1/h
    k_PS: float       # switching P -> S, 1/h
    EC50_P_ratio: float = 1.0   # EC50 of P relative to S

    @property
    def persister_fraction_eq(self) -> float:
        """Dormant fraction where switching balances and the population is not
        growing, k_SP/(k_SP+k_PS). This is the stationary-phase inoculum: it
        holds at carrying capacity, where replication has stopped. It is not
        the right value for an inoculum taken from exponential growth, because
        replication keeps refilling the replicating compartment; use
        `persister_fraction_growing` for that.
        """
        return self.k_SP / (self.k_SP + self.k_PS)

    def persister_fraction_growing(self, N0: float) -> float:
        """Dormant fraction in a population growing at density `N0`.

        With S and P both growing exponentially at rate lambda, the ratio P/S
        settles at k_SP/(lambda+k_PS), so the dormant fraction is
        k_SP/(lambda+k_PS+k_SP), where lambda solves

            lambda^2 + lambda(k_SP + k_PS - r_eff) - r_eff*k_PS = 0

        for r_eff = r(1 - N0/K). At r_eff = 0 this returns lambda = 0 and the
        expression collapses to `persister_fraction_eq`, as it must. While the
        population grows it is smaller, roughly fourfold for the slow grower of
        Section 2.6 and sixfold for the fast one, because replication dilutes
        the dormant pool faster than switching refills it.
        """
        r_eff = self.r * (1.0 - N0 / self.K)
        if r_eff <= 0.0:
            return self.persister_fraction_eq
        b = self.k_SP + self.k_PS - r_eff
        lam = 0.5 * (-b + math.sqrt(b * b + 4.0 * r_eff * self.k_PS))
        return self.k_SP / (lam + self.k_PS + self.k_SP)

    def with_resistance(self, fold: float) -> "PDParams":
        """Resistance: multiply EC50 by `fold`. MIC shifts, Emax unchanged."""
        return replace(self, label=f"resistance x{fold:g}",
                       EC50=self.EC50 * fold)

    def with_tolerance(self, fold: float) -> "PDParams":
        """Tolerance: slow the whole metabolism by `fold`.

        Replication and both kill rates are divided by the same factor. This is
        tolerance by slowed growth, the mechanism Brauner et al. describe, and
        it is the encoding that leaves the MIC exactly invariant: the MIC is the
        concentration where kill balances replication, and scaling both sides
        equally does not move that balance point. Killing everywhere else is
        `fold` times slower, so MDK rises by `fold` while the MIC does not
        change at all.

        Dividing Emax alone would not be tolerance. It lowers the maximum kill
        rate without slowing replication, which shifts the balance point and so
        moves the MIC by roughly fold^(1/H): that is partial resistance, and
        conflating the two is exactly the confusion this model exists to avoid.
        """
        return replace(self, label=f"tolerance /{fold:g}",
                       r=self.r / fold,
                       Emax_S=self.Emax_S / fold, Emax_P=self.Emax_P / fold)

    def with_persistence(self, fold: float) -> "PDParams":
        """Persistence: enlarge the dormant subpopulation `fold`-fold."""
        return replace(self, label=f"persistence x{fold:g}",
                       k_SP=self.k_SP * fold)


def _rhs(t, y, p: PDParams, C: float):
    S, P = y
    total = S + P
    kS = float(hill_kill(C, p.Emax_S, p.EC50, p.H))
    kP = float(hill_kill(C, p.Emax_P, p.EC50 * p.EC50_P_ratio, p.H))
    dS = p.r * S * (1.0 - total / p.K) - kS * S - p.k_SP * S + p.k_PS * P
    dP = -kP * P + p.k_SP * S - p.k_PS * P
    return [dS, dP]


def simulate(p: PDParams, C: float, t_eval, N0: float = 1.0e6,
             f0: float | None = None, lod: float = 0.0):
    """Integrate the two-compartment model.

    `C` is the drug concentration in multiples of the reference MIC, held
    constant. `f0` is the initial dormant fraction; when None it is taken from
    the growing state at density `N0`, which is the state the simulation then
    starts in. Using the no-growth equilibrium k_SP/(k_SP+k_PS) here instead,
    as earlier versions did, asserts a stationary-phase inoculum and then
    integrates it as an exponentially growing one; it overstates the dormant
    pool by about fourfold for the slow grower and sixfold for the fast one.
    Pass `f0` explicitly to model a genuinely stationary-phase inoculum.
    """
    t_eval = np.asarray(t_eval, dtype=float)
    f = p.persister_fraction_growing(N0) if f0 is None else f0
    y0 = [N0 * (1.0 - f), N0 * f]
    sol = solve_ivp(_rhs, (float(t_eval[0]), float(t_eval[-1])), y0,
                    t_eval=t_eval, args=(p, C), method="LSODA",
                    rtol=1e-10, atol=1e-6)
    if not sol.success:
        raise RuntimeError(
            f"integration failed for {p.label} at C={C}: {sol.message}")
    S = np.maximum(sol.y[0], 0.0)
    P = np.maximum(sol.y[1], 0.0)
    total = S + P
    if lod > 0:
        total = np.maximum(total, lod)
    return {"t": t_eval, "S": S, "P": P, "total": total}


def total_curve(p: PDParams, C: float, N0: float = 1.0e6,
                f0: float | None = None):
    """A callable t -> total CFU/mL, for use with the metric helpers."""

    def curve(t):
        t = np.atleast_1d(np.asarray(t, dtype=float))
        grid = np.unique(np.concatenate([[0.0], t]))
        out = simulate(p, C, grid, N0=N0, f0=f0)
        idx = np.searchsorted(grid, t)
        return out["total"][idx]

    return curve


def net_growth_rate(p: PDParams, C: float, N0: float = 1.0e6) -> float:
    """Initial net growth rate of the bulk population, 1/h.

    Used to locate the MIC: the concentration at which net growth is zero.
    The composition is the one the inoculum actually starts from, so that the
    MIC and the simulations it scales are defined on the same population.
    """
    f = p.persister_fraction_growing(N0)
    y = [N0 * (1.0 - f), N0 * f]
    dS, dP = _rhs(0.0, y, p, C)
    return (dS + dP) / N0


def mic(p: PDParams, c_lo: float = 1e-6, c_hi: float = 1e6) -> float:
    """MIC in units of the reference MIC: lowest C giving non-positive growth."""
    if net_growth_rate(p, c_lo) <= 0:
        return float(c_lo)
    if net_growth_rate(p, c_hi) > 0:
        return float("inf")
    return float(brentq(lambda c: net_growth_rate(p, c), c_lo, c_hi,
                        xtol=1e-12, rtol=8.9e-16))


def apparent_transition_time(p: PDParams, C: float, t_max: float = 2000.0,
                             n: int = 4001, N0: float = 1.0e6,
                             lod: float = 1.0e2) -> float:
    """Transition time as an emergent observable, not an input parameter.

    Defined as the time of maximum curvature of log10 N(t), the knee of the
    biphasic curve, searched only over the interval where the population is
    still above the limit of detection. Under the printed Eq. 4 this quantity is
    a free parameter fitted independently of the rates; here it is computed from
    them, so it cannot contradict them.
    """
    t = np.linspace(0.0, t_max, n)
    out = simulate(p, C, t, N0=N0)
    y = np.log10(np.maximum(out["total"], 1e-300))
    d2 = np.gradient(np.gradient(y, t), t)
    mask = out["total"] > lod
    mask[:3] = False
    mask[-3:] = False
    if not mask.any():
        return float("nan")
    return float(t[mask][np.argmax(d2[mask])])


# --------------------------------------------------------------- parameters --
#
# Values below are ILLUSTRATIVE and are labelled as such wherever they are
# plotted. They are chosen to reproduce documented qualitative behaviour, Mtb
# doubling near 23 h with a deep non-replicating persister compartment and
# S. aureus doubling near 1.4 h with a shallow transient tolerant state, not to
# assert measured constants. Replacing them with values fitted to the
# hollow-fibre datasets listed in data/manifests/datasets.csv is Stage 4 of the
# rebuild plan and requires no change to any code in this module.

MTB_PD = PDParams(
    label="M. tuberculosis (illustrative)",
    r=0.03,
    K=1.0e9,
    Emax_S=0.25,
    Emax_P=0.004,
    EC50=1.0,
    H=1.5,
    k_SP=1.01e-4,     # equilibrium dormant fraction 1.0%
    k_PS=1.0e-2,
    EC50_P_ratio=3.0,
)

SAUREUS_PD = PDParams(
    label="S. aureus (illustrative)",
    r=0.5,
    K=1.0e9,
    Emax_S=1.20,
    Emax_P=0.05,
    EC50=1.0,
    H=1.5,
    k_SP=1.0e-4,      # equilibrium dormant fraction 0.10%
    k_PS=1.0e-1,
    EC50_P_ratio=3.0,
)

PD_SPECIES = {"Mtb": MTB_PD, "S. aureus": SAUREUS_PD}
