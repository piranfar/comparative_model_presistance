"""
CT-BP: Censored Trajectory + Blank-Plate observation model. Pure functions only.

No I/O, no fitting, no data. Everything here is either exact arithmetic (the
hidden burden, the gap, the stochastic sterility offset) or a closed-form
observation probability (the blank-plate Poisson term). The experiment script
src/experiments/exp24_clearance_prediction.py imports these and does the rest.

UNITS DISCIPLINE. Every rate argument in this module is named either
*_log10_per_day or *_per_day_ln. There is exactly one converter between them,
and the constant 2.302585092994046 appears exactly once, as LN10. If a number
reaches a table without one of those two suffixes attached to its name, that is
a bug.

THE ARITHMETIC THIS MODULE EXISTS FOR.

    H = L + log10(V_mL)                                     [log10 cells]

is the HIDDEN BURDEN: the number of living cells still in the whole culture at
the instant a plate of that geometry first reads blank. L is the limit of
quantification in log10 CFU per mL, which for a plated volume v uL and counts
reported per mL is log10(1000/v). H is exact. It contains no biology, no fitted
parameter and no extrapolation. It is the distance, in logs, that a
time-to-detection-limit endpoint is guaranteed to fall short of extinction.

    Delta = H / b_tail                                      [days]

is the gap between the plate going blank and the expected number of survivors in
the whole culture falling below one, on the terminal-linear extrapolation. Only
the denominator is inferred. b_tail is SIGN FREE: where it is <= 0 the
population is not declining at the end of observation, Delta is +inf, and the
regimen never sterilises on this model. gap() returns numpy.inf there, never a
large finite number.

    T_ext(q) = T_ext(0.368) + ln(1 / -ln q) / (b_tail * LN10)

is the additional time needed for the probability of extinction to reach q,
given a Poisson bridge from the expected count. It does not involve N0: the
stochastic correction is a pure function of the terminal rate and the confidence
demanded. E[N] < 1 is NOT sterility - under the Poisson bridge it is
P(extinct) = e^-1 = 0.368.
"""
from __future__ import annotations

import numpy as np

LN10 = 2.302585092994046

# Fixed 21-node Gauss-Hermite rule, computed once. Used to integrate the plate
# blanking probability over the plating-noise distribution of the log density.
_GH_N = 21
_GH_X, _GH_W = np.polynomial.hermite.hermgauss(_GH_N)
GH_NODES = _GH_X
GH_WEIGHTS = _GH_W / np.sqrt(np.pi)


# ----------------------------------------------------------------- units ----
def log10_per_day_to_per_day_ln(rate_log10_per_day):
    """log10 per day -> natural log per day. The one converter."""
    return np.asarray(rate_log10_per_day) * LN10


def per_day_ln_to_log10_per_day(rate_per_day_ln):
    """natural log per day -> log10 per day. The one converter, inverted."""
    return np.asarray(rate_per_day_ln) / LN10


# ------------------------------------------------------- trajectory shape ----
def segment_elapsed(t, knots, xp=np):
    """Elapsed time inside each piecewise-linear segment at time t.

    knots is a strictly increasing sequence k_0 < k_1 < ... < k_M, giving M
    segments. Time before k_0 contributes nothing. Time after k_M is charged
    ENTIRELY to the final segment: that is the terminal-linear extrapolation,
    and it is why the whole T_ext claim reduces to one scalar, b_tail.

    Returns an array of shape t.shape + (M,).
    """
    t = xp.asarray(t)
    k = np.asarray(knots, dtype=float)
    lo = k[:-1]
    hi = k[1:].copy()
    hi[-1] = np.inf  # the final segment is open on the right
    tt = t[..., None]
    return xp.clip(tt - lo, 0.0, hi - lo)


def piecewise_linear_mu(t, a, b_log10_per_day, knots, xp=np):
    """mu(t) = a - sum_m b_m * (time elapsed in segment m by t).

    a is the latent log10 density at the first knot. b_log10_per_day is the
    vector of DECLINE rates, one per segment, in log10 per day, sign free: a
    negative entry is net growth and is an ordinary fitted value, not a special
    case.
    """
    w = segment_elapsed(t, knots, xp=xp)
    b = xp.asarray(b_log10_per_day)
    return xp.asarray(a) - xp.sum(w * b, axis=-1)


# ------------------------------------------------ blank-plate observation ----
def p_blank(mu_log10, sigma_log10, plated_volume_uL, xp=np):
    """P(a plate of this volume receives zero colonies), integrated over noise.

    A plate is blank because it received no colonies, which is a Poisson event
    at expected count 10**x * v/1000 when x is the true log10 density per mL and
    v is the plated volume in uL. Integrating over x ~ Normal(mu, sigma):

        P(blank) = int N(x; mu, sigma) exp(-10**x * v/1000) dx

    evaluated by the fixed 21-node Gauss-Hermite rule above. This has ZERO free
    parameters per detection limit: the four ERA4TB plating volumes become four
    predictions from one latent density and one sigma, which is what makes the
    plate-holdout test a test rather than a refit.
    """
    mu = xp.asarray(mu_log10)[..., None]
    sd = xp.asarray(sigma_log10)
    sd = sd[..., None] if getattr(sd, "ndim", 0) else sd
    v = xp.asarray(plated_volume_uL)[..., None]
    x = mu + np.sqrt(2.0) * sd * GH_NODES
    lam = xp.power(10.0, x) * v / 1000.0
    return xp.sum(GH_WEIGHTS * xp.exp(-lam), axis=-1)


def blank_mixture(pi_misread, mu_log10, sigma_log10, plated_volume_uL, xp=np):
    """P(this row carries a below-limit flag).

    pi_misread is the probability the flag means the plate could not be read and
    is therefore uninformative about the culture. In ERA4TB 125 of 498 flags are
    logically contradicted by another plating of the SAME sample at the SAME
    visit reading above that limit, so pi is not a nuisance bolted on for
    robustness - it is a rate the deposit forces on any honest likelihood.
    """
    return pi_misread + (1.0 - pi_misread) * p_blank(
        mu_log10, sigma_log10, plated_volume_uL, xp=xp
    )


def limit_log10_from_volume(plated_volume_uL):
    """L = log10(1000 / v). Counts are per mL; one colony in v uL is 1000/v per mL."""
    return np.log10(1000.0 / np.asarray(plated_volume_uL, dtype=float))


def volume_from_limit_log10(limit_log10):
    """Inverse of limit_log10_from_volume, used to audit the tidy files."""
    return 1000.0 / np.power(10.0, np.asarray(limit_log10, dtype=float))


# ------------------------------------------------------- exact bookkeeping ----
def hidden_burden(limit_log10, V_mL):
    """H = L + log10(V_mL), in log10 cells. Exact. No biology. No fitting.

    The number of living cells still in the whole culture at the moment a plate
    of that geometry first reads blank.
    """
    return np.asarray(limit_log10, dtype=float) + np.log10(np.asarray(V_mL, dtype=float))


def gap(H_log10_cells, b_tail_log10_per_day):
    """Delta = H / b_tail in days, +inf wherever b_tail <= 0.

    Returns numpy.inf, not a large number. A non-positive terminal rate means
    the population is not declining at the end of observation and the regimen
    never sterilises on this model; in this corpus that is the common case, not
    an exception branch.
    """
    H = np.asarray(H_log10_cells, dtype=float)
    b = np.asarray(b_tail_log10_per_day, dtype=float)
    ok = b > 0
    return np.where(ok, H / np.where(ok, b, 1.0), np.inf)


def sterility_offset_days(b_tail_log10_per_day, q):
    """Days ABOVE the E[N]=1 crossing at which P(extinct) reaches q.

    offset = ln(1 / -ln q) / (b_tail * LN10). Independent of N0 - the stochastic
    correction is a pure function of the terminal rate and the confidence
    demanded. q must lie strictly in (0, 1); q = e^-1 = 0.3679 returns 0.
    """
    q = float(q)
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0, 1)")
    b = np.asarray(b_tail_log10_per_day, dtype=float)
    num = np.log(1.0 / (-np.log(q)))
    ok = b > 0
    return np.where(ok, num / (np.where(ok, b, 1.0) * LN10), np.inf)


def t_ext_expected_one(mu_at_last_knot, b_tail_log10_per_day, last_knot_day, V_mL):
    """First t with mu(t) < -log10(V_mL): the E[N] = 1 crossing, in days.

    This is P(extinct) = e^-1 = 0.368 under a Poisson bridge, NOT sterility.
    Solved on the terminal segment only, which is valid whenever the crossing
    lies at or beyond the last knot - it always does in this corpus, because
    nothing was ever observed within two logs of extinction.
    """
    target = -np.log10(float(V_mL))
    mu = np.asarray(mu_at_last_knot, dtype=float)
    b = np.asarray(b_tail_log10_per_day, dtype=float)
    ok = b > 0
    dt = (mu - target) / np.where(ok, b, 1.0)
    return np.where(ok, float(last_knot_day) + np.maximum(dt, 0.0), np.inf)


def t_blank(mu_on_grid, plated_volume_uL, sigma_log10, p, t_grid):
    """First time on t_grid at which P(blank) >= p. NaN if it never happens.

    mu_on_grid is the latent log10 density evaluated on t_grid. This is the
    observable T_LOD and the only endpoint in this project that can be
    validated against data.
    """
    t_grid = np.asarray(t_grid, dtype=float)
    v = np.full(t_grid.shape, float(plated_volume_uL))
    pb = p_blank(np.asarray(mu_on_grid, dtype=float), sigma_log10, v)
    hit = np.nonzero(pb >= p)[0]
    return float(t_grid[hit[0]]) if hit.size else np.nan


def required_b_tail_log10_per_day(H_log10_cells, target_gap_days):
    """The b_tail a stated gap target implies: b = H / X. The tipping point."""
    return np.asarray(H_log10_cells, dtype=float) / float(target_gap_days)
