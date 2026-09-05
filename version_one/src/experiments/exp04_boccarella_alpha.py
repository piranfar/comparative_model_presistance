"""
Estimate the persistence level alpha from Boccarella et al.'s own survival data.

Run:  python -m src.experiments.exp04_boccarella_alpha

Boccarella et al. (2026, Mol Biol Evol 43:msag180, doi:10.1093/molbev/msag180)
simulate two persistence levels, alpha = 0.8 and alpha = 5e-5, and justify the
labels "high persistence" and "low persistence" by reference to a measured
difference in survival between two nutrient conditions. Their supplementary
survival data is deposited (doi:10.6084/m9.figshare.31389142, CC BY 4.0) and is
reused here under that licence.

alpha is never estimated in that paper. Their S1 figure is a boxplot. This
script asks the question the boxplot does not: what value of alpha does that
survival data actually imply, and is alpha identifiable from it at all?

Three analyses:

  A. Estimate alpha per condition with the persister kill parameters fixed at
     the authors' values, and compare with the simulated 0.8 and 5e-5.
  B. Free the persister death rate d_P and profile the joint likelihood. The
     survival function contains alpha and d_P only through the product
     alpha * exp(-(d_P + a_PR) * tau), so the data determines a curve in the
     (alpha, d_P) plane and not a point.
  C. Report what the product does determine, which is the only quantity that
     survival data can supply.

Writes:
  results/tables/exp04_alpha_estimates.csv
  results/tables/exp04_identifiability_ridge.csv
  results/tables/exp04_survival_summary.csv
  data/processed/exp04_profile.npz
  results/receipts/exp04_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import chi2

from ..models import boccarella as bc

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent          # data/ is shared with the current paper
RAW = REPO / "data" / "raw" / "boccarella2026" / "survival_S1.csv"
TABLES = ROOT / "results" / "tables"
PROCESSED = REPO / "data" / "processed"
RECEIPTS = ROOT / "results" / "receipts"

# Their labelling: 25% MHB is the high-persistence arm, 80% MHB the low one.
ARM_LABEL = {0.25: "high persistence (25% MHB)",
             0.50: "intermediate (50% MHB, unused in the paper)",
             0.80: "low persistence (80% MHB)"}
ARM_ALPHA_SIMULATED = {0.25: bc.ALPHA_HIGH, 0.80: bc.ALPHA_LOW}


# --------------------------------------------------------------- likelihood --

def _loglik(alpha: float, y_log: np.ndarray, c: float, d_p: float) -> float:
    """Gaussian log-likelihood on log survival, sigma profiled out.

    Survival spans four orders of magnitude, so the natural scale is the log.
    Sigma is concentrated out, giving a profile likelihood in alpha alone.
    """
    if not (0.0 < alpha <= 1.0):
        return -np.inf
    s = bc.survival(alpha, c, d_p=d_p)
    if not np.isfinite(s) or s <= 0:
        return -np.inf
    resid = y_log - np.log(float(s))
    n = resid.size
    sse = float(resid @ resid)
    if sse <= 0:
        return np.inf
    return -0.5 * n * (np.log(2 * np.pi * sse / n) + 1.0)


def fit_alpha(y_log: np.ndarray, c: float, d_p: float = bc.D_P):
    """Maximum-likelihood alpha on (0, 1], with a likelihood-ratio interval."""
    obj = lambda la: -_loglik(np.exp(la), y_log, c, d_p)
    res = minimize_scalar(obj, bounds=(np.log(1e-12), np.log(1.0)),
                          method="bounded",
                          options={"xatol": 1e-10, "maxiter": 500})
    a_hat = float(np.exp(res.x))
    ll_hat = -res.fun
    at_bound = a_hat > 0.999

    # 95% likelihood-ratio interval
    thresh = ll_hat - 0.5 * chi2.ppf(0.95, 1)
    g = lambda la: _loglik(np.exp(la), y_log, c, d_p) - thresh
    lo = hi = np.nan
    try:
        if g(np.log(1e-12)) < 0:
            lo = float(np.exp(brentq(g, np.log(1e-12), res.x, xtol=1e-10)))
    except ValueError:
        pass
    try:
        if g(np.log(1.0)) < 0:
            hi = float(np.exp(brentq(g, res.x, np.log(1.0), xtol=1e-10)))
        else:
            hi = 1.0
    except ValueError:
        hi = 1.0
    return a_hat, lo, hi, ll_hat, at_bound


# ---------------------------------------------------------------------------

def main() -> int:
    for d in (TABLES, PROCESSED, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)
    if not RAW.exists():
        raise SystemExit(f"missing {RAW}; stage the figshare data first")

    df = pd.read_csv(RAW)
    df = df[df["surv_frac"] > 0].copy()
    df["log_surv"] = np.log(df["surv_frac"])

    # ------------------------------------------------ survival, described ---
    summ = (df.groupby(["AB_conc", "nutrient_conc", "time"])
              .agg(n=("surv_frac", "size"),
                   geo_mean=("log_surv", lambda v: float(np.exp(v.mean()))),
                   min=("surv_frac", "min"), max=("surv_frac", "max"))
              .reset_index())
    summ["arm"] = summ["nutrient_conc"].map(ARM_LABEL)
    summ.to_csv(TABLES / "exp04_survival_summary.csv", index=False)

    # ------------------------------------- A. alpha at the authors' d_P -----
    rows = []
    for (c, nut, t), g in df.groupby(["AB_conc", "nutrient_conc", "time"]):
        y = g["log_surv"].to_numpy()
        if y.size < 2:
            continue
        a_hat, lo, hi, ll, at_bound = fit_alpha(y, c)
        pf = bc.persister_survival_factor(c)
        nf = bc.normal_survival_factor(c)
        sim = ARM_ALPHA_SIMULATED.get(nut, np.nan)
        rows.append({
            "AB_conc": c, "nutrient_conc": nut, "arm": ARM_LABEL.get(nut),
            "time_day": t, "n_populations": int(y.size),
            "geo_mean_survival": float(np.exp(y.mean())),
            "alpha_hat": a_hat, "alpha_ci_low": lo, "alpha_ci_high": hi,
            "alpha_hits_upper_bound": at_bound,
            "alpha_simulated_by_authors": sim,
            "ratio_hat_over_simulated": (a_hat / sim) if sim == sim else np.nan,
            "persister_survival_factor": pf,
            "normal_survival_factor": nf,
            "max_survival_at_alpha_1": pf,
        })
    est = pd.DataFrame(rows).sort_values(["AB_conc", "nutrient_conc", "time_day"])
    est.to_csv(TABLES / "exp04_alpha_estimates.csv", index=False)

    # ------------------------- B. the (alpha, d_P) ridge: non-identifiability
    ridge_rows = []
    store = {}
    dp_grid = np.linspace(0.02, 0.60, 40)
    for (c, nut, t), g in df.groupby(["AB_conc", "nutrient_conc", "time"]):
        y = g["log_surv"].to_numpy()
        if y.size < 2 or t != 2:
            continue
        alphas, lls = [], []
        for dp in dp_grid:
            a_hat, _, _, ll, _ = fit_alpha(y, c, d_p=dp)
            alphas.append(a_hat)
            lls.append(ll)
        alphas, lls = np.array(alphas), np.array(lls)
        key = f"{c}|{nut}|{t}"
        store[f"dp|{key}"] = dp_grid
        store[f"alpha|{key}"] = alphas
        store[f"ll|{key}"] = lls
        ok = np.isfinite(lls)
        span = float(np.nanmax(lls[ok]) - np.nanmin(lls[ok])) if ok.any() else np.nan
        inside = alphas[ok][lls[ok] >= np.nanmax(lls[ok]) - 0.5 * chi2.ppf(0.95, 1)]
        ridge_rows.append({
            "AB_conc": c, "nutrient_conc": nut, "arm": ARM_LABEL.get(nut),
            "time_day": t,
            "d_P_range": f"{dp_grid.min():.2f}-{dp_grid.max():.2f}",
            "alpha_range_over_ridge_low": float(np.nanmin(alphas)),
            "alpha_range_over_ridge_high": float(np.nanmax(alphas)),
            "alpha_fold_range": float(np.nanmax(alphas) / np.nanmin(alphas)),
            "loglik_span_over_ridge": span,
            "alpha_within_95pct_low": float(inside.min()) if inside.size else np.nan,
            "alpha_within_95pct_high": float(inside.max()) if inside.size else np.nan,
            "alpha_fold_within_95pct": (float(inside.max() / inside.min())
                                        if inside.size else np.nan),
        })
    ridge = pd.DataFrame(ridge_rows)
    ridge.to_csv(TABLES / "exp04_identifiability_ridge.csv", index=False)
    np.savez_compressed(PROCESSED / "exp04_profile.npz", **store)

    receipt = {
        "script": "src/experiments/exp04_boccarella_alpha.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source_doi": "10.6084/m9.figshare.31389142",
        "paper_doi": "10.1093/molbev/msag180",
        "licence": "CC BY 4.0",
        "n_observations": int(len(df)),
        "tau_hours": bc.TAU_TREAT,
        "kappa": bc.KAPPA,
        "authors_alpha_high": bc.ALPHA_HIGH,
        "authors_alpha_low": bc.ALPHA_LOW,
        "manuscript_code_discrepancies": [d.__dict__ for d in bc.DISCREPANCIES],
    }
    (RECEIPTS / "exp04_receipt.json").write_text(json.dumps(receipt, indent=2),
                                                 encoding="utf-8")

    # ------------------------------------------------------------- report ---
    pd.set_option("display.width", 200)
    print("Data: Boccarella et al. 2026 supplementary survival data, "
          "CC BY 4.0 (doi:10.6084/m9.figshare.31389142)\n")
    print("-- observed survival --")
    print(summ[["AB_conc", "arm", "time", "n", "geo_mean", "min", "max"]]
          .to_string(index=False, float_format=lambda v: f"{v:,.5g}"))

    print("\n-- ceiling of the model: survival when every cell is a persister "
          "(alpha = 1) --")
    for c in sorted(df["AB_conc"].unique()):
        print(f"   c = {c:>5g} ug/mL : persisters {bc.persister_survival_factor(c):.4g}"
              f"   normal cells {bc.normal_survival_factor(c):.3g}")

    print("\n-- A. alpha estimated from the authors' own survival data --")
    cols = ["AB_conc", "arm", "time_day", "n_populations", "geo_mean_survival",
            "alpha_hat", "alpha_ci_low", "alpha_ci_high",
            "alpha_hits_upper_bound", "alpha_simulated_by_authors",
            "ratio_hat_over_simulated"]
    print(est[cols].to_string(index=False, float_format=lambda v: f"{v:,.4g}"))

    print("\n-- B. is alpha identifiable? Free the persister death rate d_P --")
    print(ridge[["AB_conc", "arm", "d_P_range", "alpha_within_95pct_low",
                 "alpha_within_95pct_high", "alpha_fold_within_95pct",
                 "loglik_span_over_ridge"]].to_string(
        index=False, float_format=lambda v: f"{v:,.4g}"))
    print("\n   loglik_span_over_ridge is the total change in log-likelihood "
          "across the whole d_P range.\n   A span near zero means the data "
          "cannot distinguish any point on the ridge from any other.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
