"""
Formal causal mediation: resistance → log10 N0 → tolerance class (Exp34).

Run:  python -m src.experiments.exp34_mediation

WHY THIS TEST EXISTS. Exp22 reports that the resistance coefficient on the
published tolerance label attenuates by roughly two thirds once starting density
enters the model. Attenuation percent is a descriptive ratio of two OLS
coefficients. It is not a mediation estimate with uncertainty. A Resource /
Methods paper that asks a referee to treat inoculum as the pathway needs ACME,
ADE and total effects with bootstrap confidence intervals, and a baseline-only
sensitivity that removes the 43 follow-up isolates (Exp31).

IDENTIFICATION (linear, Baron–Kenny / product method, no covariates beyond the
stated exposure and mediator). Exposure X = INH resistance (IR=1, IS=0).
Mediator M = log10(mpn_T0_15days). Outcome Y = Tolerant_level_D5_15 coded
Low=0, Medium=1, High=2 (same linear coding as Exp22/31). Paths:

  M ~ X                 gives a
  Y ~ X + M             gives b (mediator) and c' (ADE)
  Y ~ X                 gives c  (total)
  ACME = a * b          (= c - c' under linear models with no interactions)

Bootstrap percentile intervals (B = 5000, seed fixed). No claim of unmeasured
confounding absence: this is the structural decomposition the manuscript cites
in place of attenuation percent alone.

Writes:
  results/tables/exp34_mediation.csv
  results/tables/exp34_mediation_paths.csv
  results/receipts/exp34_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

LEVEL = {"Low": 0, "Medium": 1, "High": 2}
BASELINE_TIMEPOINT = "0M"
N_BOOT = 5000
SEED = 20260906


def ols(y: np.ndarray, X: np.ndarray):
    """OLS with intercept; returns beta, se, p for columns [1, X]."""
    A = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    df = max(len(y) - A.shape[1], 1)
    s2 = float((resid @ resid) / df)
    try:
        cov = s2 * np.linalg.inv(A.T @ A)
        se = np.sqrt(np.diag(cov))
    except np.linalg.LinAlgError:
        se = np.full(A.shape[1], np.nan)
    t = beta / se
    p = 2 * stats.t.sf(np.abs(t), df)
    return beta, se, p


def load_panel(baseline_only: bool = False) -> pd.DataFrame:
    d = pd.read_excel(DATA)
    d = d[d["INH-Suceptibility"].isin(["IS", "IR"])].copy()
    if baseline_only:
        d = d[d["Time_point"].astype(str) == BASELINE_TIMEPOINT]
    m = pd.DataFrame({
        "y": d["Tolerant_level_D5_15"].map(LEVEL),
        "x": (d["INH-Suceptibility"] == "IR").astype(float),
        "m": np.log10(pd.to_numeric(d["mpn_T0_15days"], errors="coerce")),
    }).dropna()
    return m.reset_index(drop=True)


def mediate(m: pd.DataFrame) -> dict:
    """Point estimates for total, ADE, ACME and path coefficients."""
    y = m["y"].to_numpy(float)
    x = m[["x"]].to_numpy(float)
    xm = m[["x", "m"]].to_numpy(float)
    med = m[["x"]].to_numpy(float)
    med_y = m["m"].to_numpy(float)

    b_tot, se_tot, p_tot = ols(y, x)
    b_out, se_out, p_out = ols(y, xm)
    b_med, se_med, p_med = ols(med_y, med)

    a = float(b_med[1])
    b = float(b_out[2])
    c_prime = float(b_out[1])
    c = float(b_tot[1])
    acme = a * b
    return {
        "n": int(len(m)),
        "a_x_to_m": a,
        "a_se": float(se_med[1]),
        "a_p": float(p_med[1]),
        "b_m_to_y": b,
        "b_se": float(se_out[2]),
        "b_p": float(p_out[2]),
        "ade_c_prime": c_prime,
        "ade_se": float(se_out[1]),
        "ade_p": float(p_out[1]),
        "total_c": c,
        "total_se": float(se_tot[1]),
        "total_p": float(p_tot[1]),
        "acme": acme,
        "acme_via_difference": float(c - c_prime),
        "prop_mediated": float(acme / c) if abs(c) > 1e-12 else np.nan,
    }


def residual_correlation_sensitivity(m: pd.DataFrame) -> dict:
    """Imai–Keele–Yamamoto ACME as a function of Corr(ε_M, ε_Y) = ρ.

    Under the linear structural equations M ~ X and Y ~ X + M the closed form is

        ACME(ρ) = a · [ b − ρ · (σ_Y/σ_M) / √(1−ρ²) ]

    with σ_M the residual sd of M on X and σ_Y the residual sd of Y on X and M.
    Only the SECOND term carries the 1/√(1−ρ²); an earlier version divided the
    whole bracket by it, which inflated the direct-path correction and every
    ACME at ρ ≠ 0, and pushed the nullifying correlation away from zero. The
    form here recovers a·b at ρ = 0, and crosses zero at
    ρ* = k/√(1+k²) with k = b·σ_M/σ_Y — not at k itself, which is what the
    earlier version reported and which overstates how much unmeasured
    mediator-outcome confounding the estimate can absorb.

    This is a sensitivity parameterisation, not a test of sequential
    ignorability.
    """
    y = m["y"].to_numpy(float)
    x = m["x"].to_numpy(float)
    med = m["m"].to_numpy(float)
    A = np.column_stack([np.ones(len(m)), x])
    a_coef, *_ = np.linalg.lstsq(A, med, rcond=None)
    e_m = med - A @ a_coef
    B = np.column_stack([np.ones(len(m)), x, med])
    b_coef, *_ = np.linalg.lstsq(B, y, rcond=None)
    e_y = y - B @ b_coef
    a, b = float(a_coef[1]), float(b_coef[2])
    sm, sy = float(e_m.std(ddof=1)), float(e_y.std(ddof=1))
    # ACME(rho) = 0 needs rho/sqrt(1-rho^2) = b*sigma_M/sigma_Y, so the
    # nullifying correlation is k/sqrt(1+k^2), not k. Reporting k overstates
    # it, and overstating it makes the estimate look more robust to
    # unmeasured mediator-outcome confounding than it is.
    _k = float(b * sm / sy) if sy > 0 else np.nan
    rho_null = float(_k / np.sqrt(1.0 + _k * _k)) if sy > 0 else np.nan

    def acme_at(rho: float) -> float:
        return float(a * (b - rho * (sy / sm) / np.sqrt(1.0 - rho * rho)))

    grid = []
    for rho in np.round(np.linspace(-0.5, 0.5, 11), 2):
        grid.append({"rho": float(rho), "acme": acme_at(float(rho))})
    return {
        "sigma_m": sm, "sigma_y": sy,
        "rho_nullifying_acme": rho_null,
        "acme_at_rho0": acme_at(0.0),
        "grid": grid,
        "note": ("|ρ| at or beyond |rho_nullifying_acme| would bring ACME to "
                 "zero under this linear sensitivity model"),
    }


def bootstrap_effects(m: pd.DataFrame, n_boot: int = N_BOOT, seed: int = SEED
                      ) -> dict:
    rng = np.random.default_rng(seed)
    n = len(m)
    acme, ade, total = [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        est = mediate(m.iloc[idx])
        acme.append(est["acme"])
        ade.append(est["ade_c_prime"])
        total.append(est["total_c"])
    def ci(arr):
        a = np.asarray(arr, float)
        return float(np.quantile(a, 0.025)), float(np.quantile(a, 0.975))
    return {
        "acme_ci": list(ci(acme)),
        "ade_ci": list(ci(ade)),
        "total_ci": list(ci(total)),
        "n_boot": n_boot,
        "seed": seed,
    }


def run_stratum(name: str, baseline_only: bool) -> tuple[dict, dict]:
    m = load_panel(baseline_only=baseline_only)
    point = mediate(m)
    boots = bootstrap_effects(m)
    point["stratum"] = name
    point["baseline_only"] = baseline_only
    point.update(boots)
    # CI excludes zero?
    for key, ci_key in (("acme", "acme_ci"), ("ade_c_prime", "ade_ci"),
                        ("total_c", "total_ci")):
        lo, hi = boots[ci_key]
        point[f"{key}_ci_excludes_zero"] = bool(lo > 0 or hi < 0)
    return point, {
        "stratum": name,
        "path": ["a (X→M)", "b (M→Y|X)", "c' ADE (X→Y|M)", "c total (X→Y)",
                 "ACME = a·b"],
        "estimate": [point["a_x_to_m"], point["b_m_to_y"], point["ade_c_prime"],
                     point["total_c"], point["acme"]],
        "se_analytic": [point["a_se"], point["b_se"], point["ade_se"],
                        point["total_se"], np.nan],
        "p_analytic": [point["a_p"], point["b_p"], point["ade_p"],
                       point["total_p"], np.nan],
        "boot_ci_low": [np.nan, np.nan, point["ade_ci"][0], point["total_ci"][0],
                        point["acme_ci"][0]],
        "boot_ci_high": [np.nan, np.nan, point["ade_ci"][1], point["total_ci"][1],
                         point["acme_ci"][1]],
    }


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    full, paths_full = run_stratum("all_IS_IR", baseline_only=False)
    base, paths_base = run_stratum("baseline_0M", baseline_only=True)
    sens = residual_correlation_sensitivity(load_panel(baseline_only=False))
    pd.DataFrame(sens["grid"]).to_csv(
        TABLES / "exp34_mediation_sensitivity.csv", index=False)

    summary = pd.DataFrame([
        {"stratum": r["stratum"], "n": r["n"],
         "total_c": r["total_c"], "total_ci_low": r["total_ci"][0],
         "total_ci_high": r["total_ci"][1],
         "ade_c_prime": r["ade_c_prime"], "ade_ci_low": r["ade_ci"][0],
         "ade_ci_high": r["ade_ci"][1],
         "acme": r["acme"], "acme_ci_low": r["acme_ci"][0],
         "acme_ci_high": r["acme_ci"][1],
         "prop_mediated": r["prop_mediated"],
         "acme_ci_excludes_zero": r["acme_ci_excludes_zero"],
         "ade_ci_excludes_zero": r["ade_c_prime_ci_excludes_zero"],
         "total_ci_excludes_zero": r["total_c_ci_excludes_zero"],
         "a_x_to_m": r["a_x_to_m"], "b_m_to_y": r["b_m_to_y"],
         "attenuation_vs_total": (r["total_c"] - r["ade_c_prime"]) / r["total_c"]
         if abs(r["total_c"]) > 1e-12 else np.nan}
        for r in (full, base)
    ])
    summary.to_csv(TABLES / "exp34_mediation.csv", index=False)

    path_rows = []
    for block in (paths_full, paths_base):
        for i, p in enumerate(block["path"]):
            path_rows.append({
                "stratum": block["stratum"], "path": p,
                "estimate": block["estimate"][i],
                "se_analytic": block["se_analytic"][i],
                "p_analytic": block["p_analytic"][i],
                "boot_ci_low": block["boot_ci_low"][i],
                "boot_ci_high": block["boot_ci_high"][i],
            })
    pd.DataFrame(path_rows).to_csv(TABLES / "exp34_mediation_paths.csv", index=False)

    receipt = {
        "script": "src/experiments/exp34_mediation.py",
        "utc": datetime.now(timezone.utc).isoformat(),
        "exposure": "INH-Suceptibility IR vs IS",
        "mediator": "log10(mpn_T0_15days)",
        "outcome": "Tolerant_level_D5_15 (Low=0, Medium=1, High=2)",
        "method": "linear product-of-coefficients mediation; bootstrap percentile CI",
        "n_boot": N_BOOT,
        "seed": SEED,
        "full": full,
        "baseline_only": base,
        "residual_correlation_sensitivity": sens,
        "note": ("No unmeasured-confounding claim. Linear coding of the ordinal "
                 "label matches Exp22/31 so ACME is comparable to the published "
                 "attenuation percent. Sensitivity: ACME(ρ) under Corr(ε_M,ε_Y)=ρ."),
    }
    (RECEIPTS / "exp34_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str), encoding="utf-8")

    print("Exp34 causal mediation (resistance -> log10 N0 -> tolerance D5_15)")
    for r in (full, base):
        print(f"\n  {r['stratum']}  n={r['n']}")
        print(f"    total c  = {r['total_c']:+.4f}  "
              f"CI [{r['total_ci'][0]:+.4f}, {r['total_ci'][1]:+.4f}]")
        print(f"    ADE  c'  = {r['ade_c_prime']:+.4f}  "
              f"CI [{r['ade_ci'][0]:+.4f}, {r['ade_ci'][1]:+.4f}]")
        print(f"    ACME     = {r['acme']:+.4f}  "
              f"CI [{r['acme_ci'][0]:+.4f}, {r['acme_ci'][1]:+.4f}]  "
              f"({'excludes 0' if r['acme_ci_excludes_zero'] else 'includes 0'})")
        print(f"    prop mediated ~ {100 * r['prop_mediated']:.0f}%")
    print(f"\n  residual-corr sensitivity: ACME crosses 0 at rho = "
          f"{sens['rho_nullifying_acme']:+.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
