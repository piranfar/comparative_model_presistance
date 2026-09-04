"""
Fit the closed-form models and test whether their parameters are identifiable.

Run:  python -m src.experiments.exp02_fit_and_identifiability

The preprint's validation section reports one number, R-squared > 0.9, against
an unnamed dataset. This script does three things that number cannot do.

  1. It shows that R-squared does not discriminate between the printed Eq. 4 and
     the biexponential replacement: both exceed 0.9 on the same data, so the
     reported statistic is compatible with a model that resurrects the
     population at the transition.
  2. It shows by profile likelihood that the printed four-parameter Eq. 4 is
     structurally non-identifiable at the sampling density the paper's own
     Methods describe: the transition time can be moved over a wide range with
     no meaningful change in fit quality, because k_fast, k_slow and f can
     compensate for it.
  3. It reports the diagnostics that do discriminate: AIC, BIC, the residual
     runs test and the Jacobian condition number.

IMPORTANT. There is no experimental data in this project, so the data fitted
here is SYNTHETIC, drawn from the mechanistic model with known ground truth.
That supports conclusions about the estimator and about identifiability. It
supports no conclusion about either organism, and every output file and figure
generated from it is tagged accordingly.

Writes:
  results/tables/fit_summary.csv        parameter estimates and CIs
  results/tables/fit_diagnostics.csv    R2, AIC, BIC, runs test, condition no.
  results/tables/profile_tc.csv         profile likelihood of t_c
  results/processed/synthetic_fits.npz  arrays for figure 3
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ..inference.fitting import fit_log10, profile_likelihood
from ..inference.synthetic import SCHEDULES, SYNTHETIC_TAG, generate
from ..models.corrected import (biexponential_log10, persistence_as_printed_log10)
from ..models.mechanistic import PD_SPECIES, apparent_transition_time
from ..models.parameters import LOD_CFU_ML, SPECIES

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
PROCESSED = ROOT / "data" / "processed"
RECEIPTS = ROOT / "results" / "receipts"

C_XMIC = 4.0
N0 = 1.0e6

# ----------------------------------------------------------------- models ----
# Both models are parameterised on the log10 scale with an unconstrained logit
# for the dormant fraction, so the optimiser sees a well-scaled problem and any
# non-identifiability that shows up is structural rather than numerical.

PRINTED = {
    "name": "Eq. 4 as printed (4 rate parameters + N0)",
    "fn": persistence_as_printed_log10,
    "params": ["log10_N0", "k_fast", "k_slow", "logit_f", "t_c"],
    "theta0": [6.0, 0.2, 0.005, -4.0, 40.0],
    "bounds": ([4.0, 1e-4, 1e-6, -12.0, 1.0],
               [9.0, 5.0, 1.0, 2.0, 1000.0]),
}

BIEXP = {
    "name": "biexponential (3 rate parameters + N0)",
    "fn": biexponential_log10,
    "params": ["log10_N0", "k_fast", "k_slow", "logit_f"],
    "theta0": [6.0, 0.2, 0.005, -4.0],
    "bounds": ([4.0, 1e-4, 1e-6, -12.0],
               [9.0, 5.0, 1.0, 2.0]),
}


def derived_tc(k_fast: float, k_slow: float, logit_f: float) -> float:
    f = 1.0 / (1.0 + np.exp(-logit_f))
    if k_fast <= k_slow:
        return float("nan")
    return float(np.log((1.0 - f) / f) / (k_fast - k_slow))


def main() -> int:
    for d in (TABLES, PROCESSED, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict] = []
    diag_rows: list[dict] = []
    profile_rows: list[dict] = []
    store: dict[str, np.ndarray] = {}

    for short, pd_par in PD_SPECIES.items():
        knee = apparent_transition_time(pd_par, C_XMIC)
        for design_name, sched in SCHEDULES[short].items():
            ds = generate(pd_par, C_XMIC, t_sample=sched, N0=N0,
                          sigma=0.25, lod=LOD_CFU_ML, n_replicates=3,
                          seed=20250212 + len(design_name),
                          label=f"{short} {C_XMIC:g}xMIC {design_name}")
            key = f"{short}|{design_name}"
            store[f"t|{key}"] = ds.t
            store[f"y|{key}"] = ds.log10_cfu
            store[f"cens|{key}"] = ds.censored.astype(float)

            for spec in (PRINTED, BIEXP):
                fit = fit_log10(spec["fn"], ds.t, ds.log10_cfu,
                                spec["theta0"], spec["params"], spec["name"],
                                censored=ds.censored, bounds=spec["bounds"])
                for row in fit.summary_rows():
                    row.update({"species": short, "design": design_name,
                                "tag": SYNTHETIC_TAG})
                    summary_rows.append(row)

                th = dict(zip(spec["params"], fit.theta))
                tc_derived = derived_tc(th["k_fast"], th["k_slow"], th["logit_f"])
                diag_rows.append({
                    "species": short,
                    "design": design_name,
                    "model": spec["name"],
                    "n_obs": fit.n_obs,
                    "n_par": fit.n_par,
                    "r_squared": fit.r_squared,
                    "rmse_log10": fit.rmse_log10,
                    "aic": fit.aic,
                    "aicc": fit.aicc,
                    "bic": fit.bic,
                    "runs_test_z": fit.runs_test_z,
                    "jacobian_condition_number": fit.jac_cond,
                    "max_rel_se_pct": (float(np.nanmax(
                        [r["rel_se_pct"] for r in fit.summary_rows()
                         if r["rel_se_pct"] is not None]))
                        if fit.stderr is not None else np.nan),
                    "t_c_fitted_h": th.get("t_c", np.nan),
                    "t_c_hit_bound": (
                        bool(np.isclose(th["t_c"], spec["bounds"][0][4]) or
                             np.isclose(th["t_c"], spec["bounds"][1][4]))
                        if "t_c" in th else False),
                    "t_c_derived_from_rates_h": tc_derived,
                    "mechanistic_knee_h": knee,
                    "n_censored": int(ds.censored.sum()),
                    "tag": SYNTHETIC_TAG,
                })

                # store the fitted curve for figure 3
                t_fine = np.linspace(0.0, float(ds.t.max()), 601)
                store[f"fit|{key}|{spec['name']}"] = np.asarray(
                    spec["fn"](t_fine, *fit.theta), dtype=float)
                store[f"tfine|{key}"] = t_fine

                # profile the transition time of the printed model, and the
                # slow rate of both, to show which parameters are determined
                to_profile = ["t_c"] if spec is PRINTED else ["k_slow"]
                for pname in to_profile:
                    idx = spec["params"].index(pname)
                    prof = profile_likelihood(
                        spec["fn"], ds.t, ds.log10_cfu, fit.theta, idx,
                        censored=ds.censored, span=0.95, n_points=41,
                        bounds=spec["bounds"])
                    width = prof["ci95"][1] - prof["ci95"][0]
                    profile_rows.append({
                        "species": short,
                        "design": design_name,
                        "model": spec["name"],
                        "parameter": pname,
                        "estimate": float(fit.theta[idx]),
                        "ci95_low": prof["ci95"][0],
                        "ci95_high": prof["ci95"][1],
                        "ci95_width": width,
                        "ci_open_at_low_end": prof["open_low"],
                        "ci_open_at_high_end": prof["open_high"],
                        "identifiable": bool(
                            not prof["open_low"] and not prof["open_high"]
                            and np.isfinite(width)
                            and width < 1.0 * abs(float(fit.theta[idx]))),
                        "tag": SYNTHETIC_TAG,
                    })
                    store[f"prof_grid|{key}|{spec['name']}|{pname}"] = prof["grid"]
                    store[f"prof_sse|{key}|{spec['name']}|{pname}"] = prof["sse"]
                    store[f"prof_thresh|{key}|{spec['name']}|{pname}"] = np.array(
                        [prof["threshold"]])

    summary = pd.DataFrame(summary_rows)
    diag = pd.DataFrame(diag_rows)
    prof_df = pd.DataFrame(profile_rows)

    summary.to_csv(TABLES / "fit_summary.csv", index=False)
    diag.to_csv(TABLES / "fit_diagnostics.csv", index=False)
    prof_df.to_csv(TABLES / "profile_tc.csv", index=False)
    np.savez_compressed(PROCESSED / "synthetic_fits.npz", **store)

    # How much does R-squared discriminate, compared with AICc?
    piv = diag.pivot_table(index=["species", "design"], columns="model",
                           values=["r_squared", "aicc"])
    comp_rows = []
    for (sp_name, design_name), row in piv.iterrows():
        r2p = row[("r_squared", PRINTED["name"])]
        r2b = row[("r_squared", BIEXP["name"])]
        ap = row[("aicc", PRINTED["name"])]
        ab = row[("aicc", BIEXP["name"])]
        comp_rows.append({
            "species": sp_name, "design": design_name,
            "r2_printed": r2p, "r2_biexponential": r2b,
            "delta_r2": float(r2b - r2p),
            "aicc_printed": ap, "aicc_biexponential": ab,
            "delta_aicc_printed_minus_biexp": float(ap - ab),
            "both_r2_above_0.9": bool(min(r2p, r2b) > 0.9),
        })
    comp = pd.DataFrame(comp_rows)
    comp.to_csv(TABLES / "r2_vs_aicc_discrimination.csv", index=False)

    receipt = {
        "script": "src/experiments/exp02_fit_and_identifiability.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data": SYNTHETIC_TAG,
        "concentration_xMIC": C_XMIC,
        "inoculum_cfu_ml": N0,
        "lod_cfu_ml": LOD_CFU_ML,
        "min_r_squared_across_all_fits": float(diag["r_squared"].min()),
        "n_fits": int(len(diag)),
        "n_nonidentifiable_parameters": int((~prof_df["identifiable"]).sum()),
        "n_profiles": int(len(prof_df)),
        "printed_tc_nonidentifiable_in_all_designs": bool(
            (~prof_df.loc[prof_df["parameter"] == "t_c",
                          "identifiable"]).all()),
        "max_delta_aicc_printed_minus_biexp": float(
            comp["delta_aicc_printed_minus_biexp"].max()),
        "n_designs_where_both_r2_above_0.9": int(
            comp["both_r2_above_0.9"].sum()),
        "n_designs": int(len(comp)),
    }
    (RECEIPTS / "exp02_receipt.json").write_text(
        json.dumps(receipt, indent=2), encoding="utf-8")

    short_model = {PRINTED["name"]: "printed Eq.4",
                   BIEXP["name"]: "biexponential"}
    show = diag.assign(model=diag["model"].map(short_model))
    cols = ["species", "design", "model", "n_obs", "n_censored", "r_squared",
            "aicc", "runs_test_z", "jacobian_condition_number",
            "t_c_fitted_h", "t_c_hit_bound", "t_c_derived_from_rates_h",
            "mechanistic_knee_h"]
    print(f"DATA: {SYNTHETIC_TAG}\n")
    print(show[cols].to_string(index=False, float_format=lambda v: f"{v:,.3g}"))
    print("\n-- R-squared versus AICc as discriminators --")
    print(comp.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print("\n-- profile likelihood --")
    pshow = prof_df.assign(model=prof_df["model"].map(short_model))
    print(pshow[["species", "design", "model", "parameter", "estimate",
                 "ci95_low", "ci95_high", "ci_open_at_low_end",
                 "ci_open_at_high_end", "identifiable"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3g}"))
    print(f"\nt_c of the printed equation is non-identifiable in "
          f"{int((~prof_df.loc[prof_df['parameter'] == 't_c', 'identifiable']).sum())}"
          f" of {int((prof_df['parameter'] == 't_c').sum())} designs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
