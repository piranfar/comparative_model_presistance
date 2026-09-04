"""
Nonlinear least squares on log10 CFU, with the diagnostics the paper omits.

The preprint reports "R-squared values (R2 > 0.9) were computed to confirm a
strong fit". Three things are wrong with that as a validation strategy and are
addressed here.

  1. R-squared on a monotone decaying curve is close to 1 for almost any
     decreasing function, because the total sum of squares is dominated by the
     spread of the data across orders of magnitude. It does not discriminate
     between candidate models. AIC, BIC and a residual runs test do.
  2. Fits on the raw CFU scale are dominated by the first one or two points.
     Time-kill data are homoscedastic on log10 CFU, so the fit belongs there.
  3. No parameter uncertainty is reported, so the reader cannot tell whether the
     four fitted parameters are identifiable. Here the covariance matrix,
     correlation matrix, Jacobian condition number and profile likelihood are
     all reported alongside the point estimates.

Left-censored observations at the limit of detection are handled by Beal's M3:
such a point contributes log Phi((LOD - mu)/sigma) to the log-likelihood, the
probability that the observation fell below the limit. Sigma is estimated
alongside the parameters. Every reported criterion -- AIC, AICc, BIC, the
standard errors and the profile intervals -- comes from that likelihood.

An earlier version instead gave a censored point a zero residual whenever the
prediction was below the limit and derived the criteria from the resulting sum
of squares. That objective is smooth and optimises sensibly, but it is not a
likelihood, so the information criteria and likelihood intervals built on it did
not mean what they were reported to mean.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np
from scipy.optimize import least_squares, minimize
from scipy.stats import chi2, norm


@dataclass
class FitResult:
    """Everything needed to judge a fit, not just its point estimate."""

    model_name: str
    param_names: list[str]
    theta: np.ndarray
    residuals: np.ndarray
    sigma: float
    n_obs: int
    n_par: int
    sse: float
    rmse_log10: float
    r_squared: float
    aic: float
    aicc: float
    bic: float
    cov: np.ndarray | None
    stderr: np.ndarray | None
    corr: np.ndarray | None
    jac_cond: float
    runs_test_z: float
    profiles: dict = field(default_factory=dict)

    def summary_rows(self) -> list[dict]:
        rows = []
        for i, name in enumerate(self.param_names):
            se = None if self.stderr is None else float(self.stderr[i])
            rows.append({
                "model": self.model_name,
                "parameter": name,
                "estimate": float(self.theta[i]),
                "std_error": se,
                "ci95_low": None if se is None else float(self.theta[i] - 1.96 * se),
                "ci95_high": None if se is None else float(self.theta[i] + 1.96 * se),
                "rel_se_pct": None if se is None or self.theta[i] == 0
                else float(100.0 * abs(se / self.theta[i])),
            })
        return rows


def _censored_residuals(pred: np.ndarray, obs: np.ndarray,
                        censored: np.ndarray) -> np.ndarray:
    """Residuals that ignore a censored point once the model is below the LOD.

    This is a smooth objective and a reasonable *starting point* for the
    optimiser, but it is not a likelihood: setting a residual to zero assigns
    no probability to the event that was actually observed. It is used here
    only to initialise the censored maximum likelihood fit below. Every
    reported criterion comes from `neg_log_lik`.
    """
    res = pred - obs
    res = np.where(censored & (pred <= obs), 0.0, res)
    return res


def neg_log_lik(pred: np.ndarray, obs: np.ndarray, censored: np.ndarray,
                sigma: float) -> float:
    """Negative log-likelihood on log10 CFU with left-censored observations.

    This is Beal's M3. An uncensored point contributes the usual Gaussian
    density. A point recorded as below the limit of detection contributes the
    probability that it fell below the limit,

        log Phi((LOD - mu) / sigma),

    where `obs` holds the limit for those points. Giving such a point a zero
    residual instead, as the least-squares objective above does, is not a
    likelihood, and information criteria or profile intervals derived from the
    resulting sum of squares do not have their usual meaning.

    Beal SL. Ways to fit a PK model with some data below the quantification
    limit. J Pharmacokinet Pharmacodyn 2001;28:481-504. PMID 11768292.
    """
    sigma = max(float(sigma), 1e-12)
    ll = 0.0
    seen = ~censored
    if seen.any():
        z = (obs[seen] - pred[seen]) / sigma
        ll += float(np.sum(-np.log(sigma) - 0.5 * np.log(2 * np.pi)
                           - 0.5 * z * z))
    if censored.any():
        z = (obs[censored] - pred[censored]) / sigma
        ll += float(np.sum(norm.logcdf(z)))
    return -ll


def _hessian(f: Callable, x: np.ndarray, rel: float = 1e-4) -> np.ndarray:
    """Central-difference Hessian, with steps scaled to each parameter."""
    x = np.asarray(x, dtype=float)
    n = x.size
    h = np.maximum(np.abs(x) * rel, 1e-7)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ei, ej = np.zeros(n), np.zeros(n)
            ei[i], ej[j] = h[i], h[j]
            H[i, j] = H[j, i] = (
                f(x + ei + ej) - f(x + ei - ej)
                - f(x - ei + ej) + f(x - ei - ej)) / (4.0 * h[i] * h[j])
    return H


def _fit_mle(model: Callable, t: np.ndarray, y: np.ndarray,
             cens: np.ndarray, theta0: np.ndarray,
             bounds: tuple) -> tuple[np.ndarray, float, float]:
    """Maximise the censored likelihood over the parameters and sigma.

    Returns (theta, sigma, log-likelihood). Sigma is estimated on the log
    scale, which keeps it positive without a constraint.
    """
    p = theta0.size
    lo, hi = np.broadcast_to(bounds[0], (p,)), np.broadcast_to(bounds[1], (p,))

    resid = np.asarray(model(t, *theta0), dtype=float) - y
    free = resid[~cens] if (~cens).any() else resid
    s0 = float(np.std(free)) if free.size > 1 else 0.1
    v0 = np.concatenate([theta0, [np.log(max(s0, 1e-3))]])

    def nll(v):
        pred = np.asarray(model(t, *v[:p]), dtype=float)
        if not np.all(np.isfinite(pred)):
            return 1e12
        return neg_log_lik(pred, y, cens, np.exp(v[p]))

    box = [(a, b) for a, b in zip(lo, hi)] + [(np.log(1e-4), np.log(10.0))]
    sol = minimize(nll, v0, method="L-BFGS-B", bounds=box,
                   options={"maxiter": 50_000, "maxfun": 50_000})
    return sol.x[:p], float(np.exp(sol.x[p])), float(-sol.fun)


def fit_log10(model: Callable, t: np.ndarray, log10_obs: np.ndarray,
              theta0: Sequence[float], param_names: Sequence[str],
              model_name: str, censored: np.ndarray | None = None,
              bounds: tuple | None = None) -> FitResult:
    """Fit `model(t, *theta) -> log10 CFU` by least squares on log10 CFU."""
    t = np.asarray(t, dtype=float)
    y = np.asarray(log10_obs, dtype=float)
    cens = np.zeros_like(y, dtype=bool) if censored is None else np.asarray(censored, bool)
    theta0 = np.asarray(theta0, dtype=float)
    if bounds is None:
        bounds = (-np.inf, np.inf)

    def fun(theta):
        return _censored_residuals(np.asarray(model(t, *theta), dtype=float), y, cens)

    sol = least_squares(fun, theta0, bounds=bounds, method="trf",
                        x_scale="jac", max_nfev=200_000)

    res = sol.fun
    n, p = y.size, theta0.size

    # The least-squares pass above only supplies a starting point. Everything
    # reported comes from the censored maximum likelihood fit.
    theta, sigma, ll = _fit_mle(model, t, y, cens, sol.x, bounds)
    pred = np.asarray(model(t, *theta), dtype=float)
    res = pred - y

    # Sum of squares and R-squared describe the fit to the points that were
    # actually measured. Including censored points would credit the model for
    # matching a detection limit, which is not an observation of anything.
    seen = ~cens
    res_seen = res[seen] if seen.any() else res
    sse = float(res_seen @ res_seen)
    y_seen = y[seen] if seen.any() else y
    sst = float(((y_seen - y_seen.mean()) ** 2).sum())
    r2 = 1.0 - sse / sst if sst > 0 else float("nan")

    k = p + 1  # +1 for sigma, which is estimated
    aic = 2 * k - 2 * ll
    aicc = aic + (2 * k * (k + 1)) / max(n - k - 1, 1)
    bic = k * np.log(n) - 2 * ll

    # Standard errors from the observed information of the censored
    # likelihood, not from the least-squares Jacobian, so that censored points
    # contribute the information they actually carry.
    try:
        H = _hessian(lambda th: neg_log_lik(
            np.asarray(model(t, *th), dtype=float), y, cens, sigma), theta)
        cov = np.linalg.pinv(H)
        stderr = np.sqrt(np.clip(np.diag(cov), 0.0, np.inf))
        d = np.where(stderr > 0, stderr, np.nan)
        corr = cov / np.outer(d, d)
    except (np.linalg.LinAlgError, ValueError):
        cov = stderr = corr = None

    J = sol.jac
    sv = np.linalg.svd(J, compute_uv=False)
    jac_cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")

    return FitResult(
        model_name=model_name,
        param_names=list(param_names),
        theta=theta,
        residuals=res,
        sigma=sigma,
        n_obs=n,
        n_par=p,
        sse=sse,
        rmse_log10=float(np.sqrt(sse / n)),
        r_squared=float(r2),
        aic=float(aic),
        aicc=float(aicc),
        bic=float(bic),
        cov=cov,
        stderr=stderr,
        corr=corr,
        jac_cond=jac_cond,
        runs_test_z=runs_test(res),
    )


def runs_test(residuals: np.ndarray) -> float:
    """Wald-Wolfowitz runs test z-score on the sign sequence of residuals.

    Detects the systematic sign pattern that a structurally wrong model leaves
    behind even when R-squared is high. |z| > 1.96 indicates non-random
    residuals at the 5% level.
    """
    s = np.sign(np.asarray(residuals, dtype=float))
    s = s[s != 0]
    if s.size < 3:
        return float("nan")
    n_pos = int((s > 0).sum())
    n_neg = int((s < 0).sum())
    if n_pos == 0 or n_neg == 0:
        # every residual has the same sign: maximally non-random, but the
        # normal approximation is undefined, so report it as missing rather
        # than as a spuriously large z.
        return float("nan")
    runs = 1 + int((s[1:] != s[:-1]).sum())
    n = n_pos + n_neg
    mu = 2.0 * n_pos * n_neg / n + 1.0
    var = (2.0 * n_pos * n_neg * (2.0 * n_pos * n_neg - n)) / (n * n * (n - 1.0))
    if var <= 0:
        return float("nan")
    return float((runs - mu) / np.sqrt(var))


def profile_likelihood(model: Callable, t: np.ndarray, log10_obs: np.ndarray,
                       theta_hat: np.ndarray, index: int,
                       censored: np.ndarray | None = None,
                       span: float = 1.0, n_points: int = 41,
                       bounds: tuple | None = None):
    """Profile the objective along one parameter, refitting all others.

    Returns a dict whose `sse` entry holds the profiled negative log-likelihood
    at each grid point (kept under that key for the callers that read it) and
    whose `ci95` is the interval where 2*(profile - minimum) stays below the
    chi-square(1) 95% quantile. A profile that is flat, or whose interval is
    open at either end, is direct evidence of non-identifiability. This is the
    diagnostic that distinguishes "the fit converged" from "the parameter is
    determined by the data".
    """
    t = np.asarray(t, dtype=float)
    y = np.asarray(log10_obs, dtype=float)
    cens = np.zeros_like(y, dtype=bool) if censored is None else np.asarray(censored, bool)
    theta_hat = np.asarray(theta_hat, dtype=float)
    p = theta_hat.size
    lo_b, hi_b = ((-np.inf, np.inf) if bounds is None else bounds)
    lo_b = np.full(p, -np.inf) if np.isscalar(lo_b) else np.asarray(lo_b, float)
    hi_b = np.full(p, np.inf) if np.isscalar(hi_b) else np.asarray(hi_b, float)

    centre = theta_hat[index]
    scale = max(abs(centre), 1e-3)
    grid = np.linspace(centre - span * scale, centre + span * scale, n_points)
    grid = grid[(grid > lo_b[index]) & (grid < hi_b[index])]

    free = [i for i in range(p) if i != index]

    def nll_at(fixed_value):
        """Minimised negative log-likelihood with this parameter held fixed.

        Sigma is re-estimated at every grid point along with the other
        parameters, so the profile is a genuine profile likelihood rather than
        a profile of the sum of squares at a fixed error scale.
        """
        def build(free_theta):
            theta = theta_hat.copy()
            theta[index] = fixed_value
            for j, i in enumerate(free):
                theta[i] = free_theta[j]
            return theta

        def obj(v):
            pred = np.asarray(model(t, *build(v[:-1])), dtype=float)
            if not np.all(np.isfinite(pred)):
                return 1e12
            return neg_log_lik(pred, y, cens, np.exp(v[-1]))

        r0 = np.asarray(model(t, *build(theta_hat[free])), dtype=float) - y
        s0 = float(np.std(r0[~cens])) if (~cens).any() else 0.1
        v0 = np.concatenate([theta_hat[free], [np.log(max(s0, 1e-3))]])
        box = ([(a, b) for a, b in zip(lo_b[free], hi_b[free])]
               + [(np.log(1e-4), np.log(10.0))])
        sol = minimize(obj, v0, method="L-BFGS-B", bounds=box,
                       options={"maxiter": 20_000, "maxfun": 20_000})
        return float(sol.fun)

    nll_hat = nll_at(centre)
    nll_grid = np.array([nll_at(v) for v in grid])

    # Likelihood-ratio interval: 2*(profile - minimum) below the chi-square(1)
    # 95% quantile. The earlier version compared a ratio of sums of squares,
    # which is the corresponding statistic only when nothing is censored.
    sse_hat = nll_hat
    sse_grid = nll_grid
    inside = grid[2.0 * (nll_grid - nll_hat) <= chi2.ppf(0.95, 1)]
    if inside.size:
        ci = (float(inside.min()), float(inside.max()))
        open_low = bool(np.isclose(ci[0], grid.min()))
        open_high = bool(np.isclose(ci[1], grid.max()))
    else:
        ci, open_low, open_high = (float("nan"), float("nan")), True, True

    return {
        "grid": grid,
        "sse": sse_grid,          # profiled negative log-likelihood
        "sse_hat": sse_hat,       # its minimum
        "threshold": float(nll_hat + 0.5 * chi2.ppf(0.95, 1)),
        "ci95": ci,
        "open_low": open_low,
        "open_high": open_high,
    }
