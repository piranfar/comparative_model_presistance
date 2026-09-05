"""
Estimate the persistence level from the full time-kill grid, which makes it
identifiable.

Run:  python -m src.experiments.exp13_alpha_from_timekill

WHAT CHANGED. exp04 showed that the persistence level alpha is not identifiable
from survival measured at a single exposure duration: survival contains alpha
and the persister death rate only through the product
alpha * exp(-(d_P + a_PR) * tau), so one duration determines one number and the
model uses two. That was a correct statement about the data then available, a
95-row slice with two concentrations and one exposure duration per treatment
cycle.

The full deposit behind those numbers carries six exposure durations
(0, 1, 2, 3, 5 and 8 h), six antibiotic concentrations spanning 32-fold, and six
nutrient levels, at three replicates: Windels et al. 2024, ISME J 18(1):wrae070,
data at doi:10.5281/zenodo.7550302 under CC BY 4.0. With the duration axis the
degeneracy is gone, because

    ln S(tau) = ln alpha - (d_P + a_PR) * tau

is a straight line in tau whose INTERCEPT is alpha and whose SLOPE is the
persister kill rate. Both are recoverable, separately, from the slow phase of
the curve. This is the standard reading of a biphasic kill curve, and it is
available here only because the deposit has the duration axis.

WHAT THIS SCRIPT DOES. For every concentration and nutrient level it fits the
slow phase and reports alpha with a confidence interval, then compares with the
two values simulated in Boccarella et al. 2026 (Mol Biol Evol 43:msag180), which
label 25% MHB as high persistence with alpha = 0.8 and 80% MHB as low
persistence with alpha = 5e-5.

The antibiotic is amikacin, an aminoglycoside, not ampicillin. Killing by
aminoglycosides requires active transport and so is strongly growth-dependent,
which is why survival rises as nutrients fall in this dataset.

Writes:
  results/tables/exp13_alpha_estimates.csv
  results/tables/exp13_slow_phase_fits.csv
  results/receipts/exp13_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "windels2024" / "timekill.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

# Hours from which the curve is taken to be in its slow phase. The fast phase is
# over within an hour at the high concentrations; requiring three points keeps
# the intercept from resting on two.
SLOW_PHASE_FROM_H = 2.0
MIN_POINTS = 3

# What Boccarella et al. simulate, by nutrient level.
SIMULATED = {0.25: ("high persistence", 0.8), 0.8: ("low persistence", 5e-5)}


def fit_slow_phase(t, ln_s):
    """Least squares line through the slow phase; intercept is ln alpha."""
    t = np.asarray(t, float)
    ln_s = np.asarray(ln_s, float)
    if t.size < MIN_POINTS or np.ptp(t) == 0:
        return None
    res = stats.linregress(t, ln_s)
    n = t.size
    if n > 2:
        tcrit = float(stats.t.ppf(0.975, n - 2))
        lo = res.intercept - tcrit * res.intercept_stderr
        hi = res.intercept + tcrit * res.intercept_stderr
    else:
        lo = hi = np.nan
    return {
        "n_points": int(n),
        "alpha_hat": float(np.exp(res.intercept)),
        "alpha_ci_low": float(np.exp(lo)),
        "alpha_ci_high": float(np.exp(hi)),
        "persister_kill_rate_per_h": float(-res.slope),
        "kill_rate_stderr": float(res.stderr),
        "r_squared": float(res.rvalue ** 2),
    }


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; see the docstring for its source")

    d = pd.read_csv(DATA)
    d = d[(d["surv_frac"] > 0) & (d["time"] > 0)].copy()
    d["ln_s"] = np.log(d["surv_frac"])

    rows = []
    for (ab, nut), g in d.groupby(["AB_conc", "nutrient_conc"]):
        slow = g[g["time"] >= SLOW_PHASE_FROM_H]
        fit = fit_slow_phase(slow["time"], slow["ln_s"])
        if fit is None:
            continue
        label, sim = SIMULATED.get(nut, (None, np.nan))
        rows.append({
            "AB_conc": ab, "nutrient_conc": nut,
            "boccarella_arm": label, "alpha_simulated": sim, **fit,
            "ratio_simulated_over_fitted": sim / fit["alpha_hat"]
            if np.isfinite(sim) else np.nan,
        })
    fits = pd.DataFrame(rows).sort_values(["nutrient_conc", "AB_conc"])
    fits.to_csv(TABLES / "exp13_slow_phase_fits.csv", index=False)

    # One estimate per nutrient level, pooling the concentrations at which the
    # slow phase is actually resolved. Below 50 ug/mL the fast phase has not
    # finished by 8 h, so the intercept there is not a persister fraction.
    resolved = fits[fits["AB_conc"] >= 50]
    summary = (resolved.groupby("nutrient_conc")
               .agg(n_concentrations=("alpha_hat", "size"),
                    alpha_geomean=("alpha_hat", lambda v: float(np.exp(np.log(v).mean()))),
                    alpha_min=("alpha_hat", "min"), alpha_max=("alpha_hat", "max"),
                    kill_rate_mean=("persister_kill_rate_per_h", "mean"),
                    r2_min=("r_squared", "min"))
               .reset_index())
    summary["boccarella_arm"] = summary["nutrient_conc"].map(
        lambda n: SIMULATED.get(n, (None, None))[0])
    summary["alpha_simulated"] = summary["nutrient_conc"].map(
        lambda n: SIMULATED.get(n, (None, np.nan))[1])
    summary["simulated_over_fitted"] = (summary["alpha_simulated"]
                                        / summary["alpha_geomean"])
    summary.to_csv(TABLES / "exp13_alpha_estimates.csv", index=False)

    arms = summary.dropna(subset=["alpha_simulated"])
    contrast_fitted = np.nan
    if len(arms) == 2:
        a = arms.set_index("nutrient_conc")["alpha_geomean"]
        contrast_fitted = float(a.loc[0.25] / a.loc[0.8])

    (RECEIPTS / "exp13_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp13_alpha_from_timekill.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_doi": "10.5281/zenodo.7550302",
        "paper_doi": "10.1093/ismejo/wrae070",
        "licence": "CC BY 4.0",
        "antibiotic": "amikacin",
        "slow_phase_from_h": SLOW_PHASE_FROM_H,
        "concentrations_used_for_summary": ">= 50 ug/mL",
        "n_fits": int(len(fits)),
        "alpha_by_nutrient": summary.set_index("nutrient_conc")["alpha_geomean"].to_dict(),
        "fitted_contrast_high_over_low": contrast_fitted,
        "simulated_contrast_high_over_low": 0.8 / 5e-5,
    }, indent=2), encoding="utf-8")

    pd.set_option("display.width", 220)
    print("-- slow-phase fits, one per concentration and nutrient level --")
    print(fits[["nutrient_conc", "AB_conc", "n_points", "alpha_hat",
                "alpha_ci_low", "alpha_ci_high", "persister_kill_rate_per_h",
                "r_squared"]].to_string(index=False,
                                        float_format=lambda v: f"{v:,.4g}"))

    print("\n-- persistence level by nutrient level, concentrations >= 50 ug/mL --")
    print(summary[["nutrient_conc", "boccarella_arm", "n_concentrations",
                   "alpha_geomean", "alpha_min", "alpha_max",
                   "alpha_simulated", "simulated_over_fitted"]].to_string(
        index=False, float_format=lambda v: f"{v:,.4g}"))

    if np.isfinite(contrast_fitted):
        print(f"\ncontrast between the two arms:")
        print(f"   fitted from the data: {contrast_fitted:,.1f}x")
        print(f"   as simulated:         {0.8/5e-5:,.0f}x")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
