"""
Computational strengtheners requested by the external review (Exp35).

Run:  python -m src.experiments.exp35_review_strengthen

Not prose recommendations — calculations:

  1. IR → log10 N0 confounder scan across every usable column in the Vijay file
     (what the deposit can and cannot rule out for the 10-fold seeding gap).
  2. Binary-outcome mediation robustness (High vs rest; not-Low vs Low) with
     bootstrap CIs, beside the linear 0/1/2 ACME of Exp34.
  3. Dense residual-correlation sensitivity grid (ACME vs ρ) with the ρ that
     nullifies the point ACME and the ρ that drives it through zero of the
     Exp34 bootstrap CI.
  4. ERA4TB Δh at 100 µL with full-digit cluster-bootstrap CI (range statistic
     note preserved).
  5. Apramycin separation recomputed with explicit 1 µg/mL exclusion
     (LOW=4, HIGH=128 → 32-fold).

Writes:
  results/tables/exp35_ir_seeding_confounders.csv
  results/tables/exp35_binary_mediation.csv
  results/tables/exp35_mediation_sensitivity_dense.csv
  results/tables/exp35_delta_h_ci.csv
  results/tables/exp35_apramycin_exclusion.csv
  results/receipts/exp35_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from src.experiments.exp34_mediation import (
    LEVEL, N_BOOT, SEED, bootstrap_effects, load_panel, mediate, ols,
    residual_correlation_sensitivity,
)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw"
TB = DATA / "tb" / "elife93243_supp2.xlsx"
ERA = DATA / "tb" / "era4tb_timekill.csv"  # unused; Δh taken from exp31 receipt
KAUR = DATA / "apramycin_mtb" / "Raw Data.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

SKIP_AS_CONFOUNDER = {
    "Index", "Archive", "Sample-ID", "INH-Suceptibility",
    "INH-R-sequential isolates",  # defined from resistance status; not a confounder
    "mpn_T0_15days", "mpn_T0_15days_log10",
    # outcomes / descendants of N0 or the label itself
    "Survival_T2_15days", "Survival_T5_15days",
    "Tolerant_level_D2_15", "Tolerant_level_D5_15",
    "Tolerant_level_D2_60", "Tolerant_level_D5_60",
    "MDK_90_15day_new", "MDK_99_15day_new", "MDK_99_99_15day_new",
    "MDK_90_60day_new", "MDK_99_60day_new", "MDK_99_99_60day_new",
    "mpn_T2_15days", "mpn_T2_15days_log10",
    "mpn_T5_15days", "mpn_T5_15days_log10",
    # later MPN panels are downstream of the same cultures, not pretreatment confounders
    "mpn_T0_30days", "mpn_T2_30days", "mpn_T5_30days",
    "Survival_T2_30days", "Survival_T5_30days",
    "mpn_T0_60days", "mpn_T0_60days_log10",
    "mpn_T2_60days", "mpn_T2_60days_log10",
    "mpn_T5_60days", "mpn_T5_60days_log10",
    "Survival_T2_60days", "Survival_T5_60days",
    "Relative_growth_T0", "Relative_growth_T2", "Relative_growth_T5",
}


def ir_seeding_confounders() -> pd.DataFrame:
    d = pd.read_excel(TB)
    d = d[d["INH-Suceptibility"].isin(["IS", "IR"])].copy()
    d["IR"] = (d["INH-Suceptibility"] == "IR").astype(float)
    d["start"] = np.log10(pd.to_numeric(d["mpn_T0_15days"], errors="coerce"))
    rows = []
    # unadjusted
    m0 = d[["start", "IR"]].dropna()
    b0, se0, p0 = ols(m0["start"].to_numpy(), m0[["IR"]].to_numpy())
    rows.append({
        "covariate": "(none)", "kind": "unadjusted", "n": len(m0),
        "beta_IR": float(b0[1]), "se": float(se0[1]), "p": float(p0[1]),
        "attenuation_of_IR_beta": 0.0,
        "note": "reference: IR coefficient on log10 N0",
    })
    base_beta = float(b0[1])

    for col in d.columns:
        if col in SKIP_AS_CONFOUNDER or col in ("IR", "start"):
            continue
        s = d[col]
        if pd.api.types.is_numeric_dtype(s):
            frame = d[["start", "IR", col]].apply(pd.to_numeric, errors="coerce").dropna()
            if len(frame) < 40 or frame[col].nunique() < 2:
                continue
            X = frame[["IR", col]].to_numpy(float)
            b, se, p = ols(frame["start"].to_numpy(float), X)
            rows.append({
                "covariate": col, "kind": "numeric", "n": len(frame),
                "beta_IR": float(b[1]), "se": float(se[1]), "p": float(p[1]),
                "attenuation_of_IR_beta": float((base_beta - b[1]) / base_beta)
                if abs(base_beta) > 1e-12 else np.nan,
                "note": f"adjusted for numeric {col}",
            })
        else:
            nun = int(s.nunique(dropna=True))
            if nun < 2 or nun > 20:
                continue
            dum = pd.get_dummies(s.astype(str), drop_first=True, dtype=float)
            frame = pd.concat([d[["start", "IR"]], dum], axis=1).dropna()
            if len(frame) < 40:
                continue
            cols_x = ["IR"] + list(dum.columns)
            X = frame[cols_x].to_numpy(float)
            b, se, p = ols(frame["start"].to_numpy(float), X)
            rows.append({
                "covariate": col, "kind": f"categorical(k={nun})", "n": len(frame),
                "beta_IR": float(b[1]), "se": float(se[1]), "p": float(p[1]),
                "attenuation_of_IR_beta": float((base_beta - b[1]) / base_beta)
                if abs(base_beta) > 1e-12 else np.nan,
                "note": f"adjusted for {nun}-level {col}; deposit has no site/batch field",
            })
    out = pd.DataFrame(rows).sort_values("attenuation_of_IR_beta",
                                         key=lambda s: s.abs(), ascending=False)
    return out


def binary_mediation() -> pd.DataFrame:
    d = pd.read_excel(TB)
    d = d[d["INH-Suceptibility"].isin(["IS", "IR"])].copy()
    lab = d["Tolerant_level_D5_15"]
    rows = []
    for name, y in (
        ("high_vs_rest", (lab == "High").astype(float)),
        ("notlow_vs_low", lab.isin(["Medium", "High"]).astype(float)),
        ("linear_012", lab.map(LEVEL).astype(float)),
    ):
        m = pd.DataFrame({
            "y": y,
            "x": (d["INH-Suceptibility"] == "IR").astype(float),
            "m": np.log10(pd.to_numeric(d["mpn_T0_15days"], errors="coerce")),
        }).dropna()
        point = mediate(m)
        boots = bootstrap_effects(m, n_boot=N_BOOT, seed=SEED)
        rows.append({
            "outcome": name, "n": point["n"],
            "total_c": point["total_c"],
            "ade": point["ade_c_prime"],
            "acme": point["acme"],
            "prop_mediated": point["prop_mediated"],
            "total_ci_low": boots["total_ci"][0],
            "total_ci_high": boots["total_ci"][1],
            "ade_ci_low": boots["ade_ci"][0],
            "ade_ci_high": boots["ade_ci"][1],
            "acme_ci_low": boots["acme_ci"][0],
            "acme_ci_high": boots["acme_ci"][1],
            "acme_ci_excludes_zero": bool(
                boots["acme_ci"][0] > 0 or boots["acme_ci"][1] < 0),
        })
    return pd.DataFrame(rows)


def dense_sensitivity() -> tuple[pd.DataFrame, dict]:
    m = load_panel(False)
    # reuse closed form but denser grid + CI-nullification search
    sens = residual_correlation_sensitivity(m)
    # rebuild denser
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

    def acme_at(rho: float) -> float:
        return float(a * (b - rho * sy / sm) / np.sqrt(1.0 - rho * rho))

    boots = bootstrap_effects(m)
    acme_lo = boots["acme_ci"][0]
    grid = []
    for rho in np.round(np.linspace(-0.9, 0.9, 37), 3):
        if abs(rho) >= 0.999:
            continue
        val = acme_at(float(rho))
        grid.append({"rho": float(rho), "acme": val,
                     "below_boot_ci_low": bool(val < acme_lo),
                     "nonpositive": bool(val <= 0)})
    g = pd.DataFrame(grid)
    # smallest |ρ| with ACME<=0 on the side that moves toward null
    neg = g[g["nonpositive"] & (g["rho"] < 0)]
    rho_point_null = float(sens["rho_nullifying_acme"])
    rho_ci_null = float(neg["rho"].max()) if len(neg) else np.nan
    meta = {
        "rho_nullifies_point_acme": rho_point_null,
        "rho_drives_acme_to_boot_ci_low_boundary": float(
            g.loc[(g["rho"] < 0) & g["below_boot_ci_low"], "rho"].max())
        if ((g["rho"] < 0) & g["below_boot_ci_low"]).any() else np.nan,
        "rho_makes_acme_nonpositive": rho_ci_null,
        "acme_boot_ci": boots["acme_ci"],
        "acme_at_0": acme_at(0.0),
    }
    return g, meta


def delta_h_full_digits() -> pd.DataFrame:
    receipt = RECEIPTS / "exp31_receipt.json"
    if not receipt.exists():
        raise SystemExit("exp31 receipt missing; run exp31 first")
    r = json.loads(receipt.read_text(encoding="utf-8"))
    dh = r.get("era4tb_headroom_spread_100ul", {})
    by_lab = r.get("era4tb_headroom_100ul_by_laboratory", {})
    rows = [{
        "statistic": "delta_h_max_minus_min",
        "n_laboratories": dh.get("n_laboratories"),
        "estimate": dh.get("observed_range"),
        "ci_low": dh.get("cluster_bootstrap_range_ci", [None, None])[0],
        "ci_high": dh.get("cluster_bootstrap_range_ci", [None, None])[1],
        "note": ("percentile CI of lab-cluster bootstrap of a range; upper "
                 "equals the observed range by construction under resampling "
                 "with replacement of 4 laboratories"),
        "laboratories": ",".join(sorted(by_lab)) if by_lab else "",
        "lab_headrooms": json.dumps(by_lab),
    }, {
        "statistic": "between_lab_sd",
        "n_laboratories": dh.get("n_laboratories"),
        "estimate": dh.get("observed_between_lab_sd"),
        "ci_low": dh.get("cluster_bootstrap_sd_ci", [None, None])[0],
        "ci_high": dh.get("cluster_bootstrap_sd_ci", [None, None])[1],
        "note": "preferred dispersion measure; not biased downward like the range",
        "laboratories": ",".join(sorted(by_lab)) if by_lab else "",
        "lab_headrooms": json.dumps(by_lab),
    }]
    return pd.DataFrame(rows)


def apramycin_exclusion() -> pd.DataFrame:
    d = pd.read_excel(KAUR, sheet_name="Kill kinetics", header=None)
    base = float(d.iloc[3, 7])
    k = d.iloc[4:, 1:8].copy()
    k.columns = ["day", "compound", "conc", "r1", "r2", "r3", "avg"]
    k["day"] = k["day"].ffill()
    k["compound"] = k["compound"].ffill()
    k = k[pd.to_numeric(k["avg"], errors="coerce").notna()].copy()
    k["avg"] = k["avg"].astype(float)
    k["dayn"] = k["day"].astype(str).str.extract(r"(\d+)").astype(float)
    k["conc"] = pd.to_numeric(k["conc"], errors="coerce")
    ap = k[k["compound"] == "Apramycin"]
    concs = sorted(ap["conc"].dropna().unique())
    g = ap.pivot_table(index="conc", columns="dayn", values="avg")
    g.insert(0, 0.0, base)
    low, high = 4.0, 128.0
    rows = []
    for day in (3.0, 7.0, 14.0):
        # with exclusion (analysis convention)
        sep = float(g.loc[low, day] - g.loc[high, day])
        ratio = float(10 ** sep)
        # if 1 ug/mL included as "low"
        sep1 = float(g.loc[1.0, day] - g.loc[high, day]) if 1.0 in g.index else np.nan
        rows.append({
            "day": day,
            "grid_concentrations_ug_ml": ",".join(f"{c:g}" for c in concs),
            "excluded_arm_ug_ml": 1.0,
            "excluded_reason": "net growth / sub-threshold; not a kill arm",
            "low_ug_ml": low, "high_ug_ml": high,
            "fold_range_used": high / low,
            "log10_separation_4_vs_128": sep,
            "survivor_ratio_4_over_128": ratio,
            "log10_separation_1_vs_128_if_included": sep1,
            "survivor_ratio_1_over_128_if_included":
                float(10 ** sep1) if np.isfinite(sep1) else np.nan,
        })
    return pd.DataFrame(rows)


def fraction_determinism() -> dict:
    d = pd.read_excel(TB)
    s = pd.to_numeric(d["Survival_T5_15days"], errors="coerce")
    lab = d["Tolerant_level_D5_15"]
    ok = s.notna() & lab.isin(LEVEL)
    pred = np.where(s < 1e-3, "Low", np.where(s <= 1e-2, "Medium", "High"))
    match = (pred[ok.to_numpy()] == lab[ok].to_numpy())
    # Per class, the span of recorded fractions the cuts have to separate. The
    # table that reports this needs the ranges, not only the agreement count.
    classes = []
    for level in ("Low", "Medium", "High"):
        sel = ok & (lab == level)
        if not sel.any():
            continue
        f = s[sel]
        agree = (pred[sel.to_numpy()] == level)
        classes.append({
            "label": level,
            "n": int(sel.sum()),
            "min_fraction": float(f.min()),
            "max_fraction": float(f.max()),
            "disagreements": int((~agree).sum()),
        })
    return {
        "n_usable": int(ok.sum()),
        "n_agree": int(match.sum()),
        "n_disagree": int((~match).sum()),
        "cuts": "Low < 1e-3 <= Medium <= 1e-2 < High",
        "classes": classes,
    }


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    print("-- 1. IR seeding confounder scan --")
    conf = ir_seeding_confounders()
    conf.to_csv(TABLES / "exp35_ir_seeding_confounders.csv", index=False)
    top = conf[conf["covariate"] != "(none)"].head(5)
    print(top[["covariate", "kind", "n", "beta_IR", "attenuation_of_IR_beta"]].to_string(
        index=False))
    has_site = any("site" in c.lower() or "batch" in c.lower() or "hosp" in c.lower()
                   or "refer" in c.lower() for c in pd.read_excel(TB).columns)
    print(f"   referring-site / processing-batch columns present: {has_site}")

    print("\n-- 2. binary mediation robustness --")
    binm = binary_mediation()
    binm.to_csv(TABLES / "exp35_binary_mediation.csv", index=False)
    print(binm[["outcome", "n", "acme", "acme_ci_low", "acme_ci_high",
                "acme_ci_excludes_zero", "prop_mediated"]].to_string(index=False))

    print("\n-- 3. dense mediation sensitivity --")
    dens, meta = dense_sensitivity()
    dens.to_csv(TABLES / "exp35_mediation_sensitivity_dense.csv", index=False)
    print(f"   rho nullifies point ACME: {meta['rho_nullifies_point_acme']:+.4f}")
    print(f"   rho makes ACME <= 0:      {meta['rho_makes_acme_nonpositive']:+.4f}")
    print(f"   ACME boot CI:             {meta['acme_boot_ci']}")

    print("\n-- 4. delta-h CI full digits --")
    dh = delta_h_full_digits()
    dh.to_csv(TABLES / "exp35_delta_h_ci.csv", index=False)
    print(dh[["statistic", "estimate", "ci_low", "ci_high"]].to_string(index=False))

    print("\n-- 5. apramycin exclusion --")
    ap = apramycin_exclusion()
    ap.to_csv(TABLES / "exp35_apramycin_exclusion.csv", index=False)
    print(ap[["day", "fold_range_used", "survivor_ratio_4_over_128",
              "survivor_ratio_1_over_128_if_included"]].to_string(index=False))

    det = fraction_determinism()
    print(f"\n-- fraction->label determinism: {det['n_agree']}/{det['n_usable']} --")

    receipt = {
        "script": "src/experiments/exp35_review_strengthen.py",
        "utc": datetime.now(timezone.utc).isoformat(),
        "has_site_or_batch_column": has_site,
        "ir_seeding_top_attenuations": top.to_dict(orient="records"),
        "binary_mediation": binm.to_dict(orient="records"),
        "mediation_sensitivity": meta,
        "delta_h": dh.to_dict(orient="records"),
        "apramycin": ap.to_dict(orient="records"),
        "fraction_determinism": det,
    }
    (RECEIPTS / "exp35_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str), encoding="utf-8")
    print(f"\nwrote {RECEIPTS / 'exp35_receipt.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
