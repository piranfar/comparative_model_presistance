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

Left-censored observations at the limit of detection are handled by an M3-style
substitution: a censored point contributes a residual only when the model
predicts a value above the LOD, which avoids the bias of treating LOD as a
measured value while keeping the objective smooth.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2


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
    """Residuals with M3-style handling of left-censored points."""
    res = pred - obs
    # A censored point is satisfied by any prediction at or below the LOD.
    res = np.where(censored & (pred <= obs), 0.0, res)
    return res


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
    sse = float(res @ res)
    dof = max(n - p, 1)
    sigma2 = sse / dof
    sigma = float(np.sqrt(sigma2))

    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - sse / sst if sst > 0 else float("nan")

    # Gaussian log-likelihood at the optimum, profile sigma
    ll = -0.5 * n * (np.log(2 * np.pi * sse / n) + 1.0)
    k = p + 1  # +1 for sigma
    aic = 2 * k - 2 * ll
    aicc = aic + (2 * k * (k + 1)) / max(n - k - 1, 1)
    bic = k * np.log(n) - 2 * ll

    J = sol.jac
    try:
        JTJ = J.T @ J
        cov = sigma2 * np.linalg.pinv(JTJ)
        stderr = np.sqrt(np.clip(np.diag(cov), 0.0, np.inf))
        d = np.where(stderr > 0, stderr, np.nan)
        corr = cov / np.outer(d, d)
    except np.linalg.LinAlgError:
        cov = stderr = corr = None

    sv = np.linalg.svd(J, compute_uv=False)
    jac_cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")

    return FitResult(
        model_name=model_name,
        param_names=list(param_names),
        theta=sol.x,
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

    Returns (grid, delta_sse, ci95) where delta_sse is SSE(profile) - SSE(hat)
    and ci95 is the interval where the likelihood-ratio statistic stays below
    the chi-square(1) 95% quantile. A profile that is flat, or whose interval is
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

    def sse_at(fixed_value):
        def fun(free_theta):
            theta = theta_hat.copy()
            theta[index] = fixed_value
            for j, i in enumerate(free):
                theta[i] = free_theta[j]
            pred = np.asarray(model(t, *theta), dtype=float)
            return _censored_residuals(pred, y, cens)

        if free:
            sol = least_squares(fun, theta_hat[free],
                                bounds=(lo_b[free], hi_b[free]),
                                method="trf", x_scale="jac", max_nfev=50_000)
            return float(sol.fun @ sol.fun)
        r = fun(np.array([]))
        return float(r @ r)

    sse_hat = sse_at(centre)
    sse_grid = np.array([sse_at(v) for v in grid])

    n = y.size
    thresh = sse_hat * np.exp(chi2.ppf(0.95, 1) / n)
    inside = grid[sse_grid <= thresh]
    if inside.size:
        ci = (float(inside.min()), float(inside.max()))
        open_low = bool(np.isclose(ci[0], grid.min()))
        open_high = bool(np.isclose(ci[1], grid.max()))
    else:
        ci, open_low, open_high = (float("nan"), float("nan")), True, True

    return {
        "grid": grid,
        "sse": sse_grid,
        "sse_hat": sse_hat,
        "threshold": float(thresh),
        "ci95": ci,
        "open_low": open_low,
        "open_high": open_high,
    }
