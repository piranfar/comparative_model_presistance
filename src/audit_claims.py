"""
Check every headline number against the table that is supposed to contain it.

Run:  python -m src.audit_claims

Numbers drift. A figure gets regenerated, a filter changes, a section is
rewritten, and a value quoted in three places stops agreeing with itself. This
has already happened twice in this project, both times caught by accident. This
script checks on purpose.

Each entry names the claim, where it is asserted, and how to recompute it from
the results tables. A claim that cannot be recomputed is reported as such rather
than passed.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"


def load(name: str):
    p = T / name
    return pd.read_csv(p) if p.exists() else None


def check(label: str, claimed, computed, tol=0.05, unit=""):
    """Compare a claimed value with a recomputed one, on relative tolerance."""
    if computed is None or (isinstance(computed, float) and not np.isfinite(computed)):
        return {"claim": label, "claimed": claimed, "computed": None,
                "status": "CANNOT RECOMPUTE"}
    ok = abs(computed - claimed) <= tol * max(abs(claimed), 1e-12)
    return {"claim": label, "claimed": f"{claimed:g}{unit}",
            "computed": f"{computed:.4g}{unit}",
            "status": "ok" if ok else "MISMATCH"}


def main() -> int:
    rows = []

    # --- persister kill rate, exp13 --------------------------------------
    f = load("exp13_slow_phase_fits.csv")
    if f is not None:
        s = f[(f.AB_conc >= 50) & (f.nutrient_conc.isin([0.25, 0.5, 0.8]))]
        rows.append(check("persister kill rate, low end (manuscript: 0.2/h)",
                          0.2, float(s.persister_kill_rate_per_h.min()), 0.35, " /h"))
        rows.append(check("persister kill rate, high end (manuscript: 0.68/h)",
                          0.68, float(s.persister_kill_rate_per_h.max()), 0.05, " /h"))

    # --- alpha, exp13 ----------------------------------------------------
    a = load("exp13_alpha_estimates.csv")
    if a is not None:
        v = a[a.nutrient_conc == 0.25].alpha_geomean
        if len(v):
            rows.append(check("alpha at nutrient 0.25 (manuscript: 1.7e-3)",
                              1.7e-3, float(v.iloc[0]), 0.10))
            rows.append(check("ratio simulated 0.8 over fitted (manuscript: 461x)",
                              461, 0.8 / float(v.iloc[0]), 0.10, "x"))

    # --- nutrient span, exp14 vs exp15 -----------------------------------
    n = load("exp14_kill_rates_by_nutrient.csv")
    if n is not None:
        span = float(n.normal_kill_median_per_h.max() / n.normal_kill_median_per_h.min())
        rows.append(check("ordinary-cell span across nutrient (exp14 medians: 19x)",
                          19, span, 0.10, "x"))
        adv = n.normal_over_persister
        rows.append(check("dormancy advantage, minimum (manuscript: 3.6x)",
                          3.6, float(adv.min()), 0.10, "x"))
        rows.append(check("dormancy advantage, maximum (manuscript: 27x)",
                          27, float(adv.max()), 0.10, "x"))

    g = load("exp15_kill_rate_grid.csv")
    if g is not None:
        g = g[g.kill_rate_per_h > 0]
        X = np.column_stack([np.ones(len(g)), np.log2(g.AB_conc), g.nutrient_conc,
                             np.log2(g.AB_conc) * g.nutrient_conc])
        b, *_ = np.linalg.lstsq(X, np.log(g.kill_rate_per_h), rcond=None)
        rows.append(check("nutrient gap from the exp15 regression (reported: 41x)",
                          41, float(np.exp(b[2] * 0.9)), 0.10, "x"))
        rows.append({"claim": "THE TWO NUTRIENT NUMBERS DISAGREE BY DESIGN",
                     "claimed": "19x (exp14, empirical medians)",
                     "computed": f"{np.exp(b[2]*0.9):.0f}x (exp15, fitted linear trend to 0.9)",
                     "status": "EXPLAIN OR PICK ONE"})

    # --- extinction and contrast, exp10 ----------------------------------
    c = load("exp10_recalibrated_contrast.csv")
    r = load("exp10_recalibrated_replicates.csv")
    if c is not None:
        for scen, claimed in (("published", 2.01), ("calibrated", 2.05)):
            v = c[c.scenario == scen].ratio_low_over_high
            if len(v):
                rows.append(check(f"contrast, {scen} (manuscript: {claimed})",
                                  claimed, float(v.iloc[0]), 0.05, "x"))
    if r is not None:
        lo = r[(r.scenario == "calibrated") & (r.arm == "low")]
        rows.append(check("extinctions, calibrated low arm (manuscript: 19 of 40)",
                          19, float(lo.extinct.sum()), 0.001))
        lo2 = r[(r.scenario == "published")]
        rows.append(check("extinctions, published, both arms (manuscript: 0 of 80)",
                          0, float(lo2.extinct.sum()), 1.0))

    # --- exp16, the family correction ------------------------------------
    f = load("exp16_tb_independence.csv")
    if f is not None:
        rows.append(check("MIC-MDK tests available (docs/18: 24)",
                          24, float(len(f)), 0.001))
        rows.append(check("nominally significant (docs/18: 4)",
                          4, float((f.p_value < 0.05).sum()), 0.001))
        rows.append(check("surviving Benjamini-Hochberg (docs/18: 0)",
                          0, float(f.survives_bh.sum()), 1.0))

    # --- exp17, the two censoring estimators must agree -------------------
    f = load("exp17_kill_rates.csv")
    if f is not None:
        g = f.dropna(subset=["kill_rate_tobit", "kill_rate_mi"])
        rows.append(check("max |Tobit - imputation| (docs/18: 0.003 log10/day)",
                          0.003, float((g.kill_rate_tobit - g.kill_rate_mi).abs().max()),
                          0.35, " log10/d"))

    # --- exp18, the conclusion must hold on both unit readings ------------
    f = load("exp18_unit_sensitivity.csv")
    if f is not None:
        rows.append(check("smallest psi_min gap, either unit reading (273x)",
                          273, float(f.fold_gap.min()), 0.02, "x"))
        rows.append(check("largest psi_min gap, either unit reading (658x)",
                          658, float(f.fold_gap.max()), 0.02, "x"))

    # --- exp20, the endpoint that decides what is visible -----------------
    f = load("exp20_endpoint_separation.csv")
    if f is not None:
        s = f.set_index("day")["survivor_ratio_low_over_high"]
        for day, claimed in ((7.0, 48.2), (14.0, 5.2)):
            if day in s.index:
                rows.append(check(f"32-fold dose range separates at day {int(day)}",
                                  claimed, float(s.loc[day]), 0.05, "x"))

    out = pd.DataFrame(rows)
    pd.set_option("display.width", 210)
    pd.set_option("display.max_colwidth", 62)
    print(out.to_string(index=False))

    bad = out[out.status.isin(["MISMATCH", "CANNOT RECOMPUTE", "EXPLAIN OR PICK ONE"])]
    print(f"\n{len(out) - len(bad)} of {len(out)} checks agree with the tables")
    if len(bad):
        print(f"{len(bad)} need attention:")
        for _, x in bad.iterrows():
            print(f"   [{x.status}] {x.claim}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
