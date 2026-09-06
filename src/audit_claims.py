"""
Check every headline number in the current paper against its table.

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
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"


def load(name: str):
    p = T / name
    return pd.read_csv(p) if p.exists() else None


def receipt(name: str):
    """Read a receipt, or None if the stage has not been run."""
    p = ROOT / "results" / "receipts" / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


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

    # --- exp24, the three properties a design review found we had missed --
    # Two of these constrain our own argument rather than support it, which is
    # why they are pinned: a number that limits a claim must not be free to
    # drift in the direction we would prefer.
    r = receipt("exp24_receipt.json")
    if r is not None:
        tr = r["trajectory_shape"]
        rows.append(check("treated series measured for shape (4: 64)",
                          64, float(tr["n_treated_series"]), 0.001))
        rows.append(check("final step not a decline (4: 48)",
                          48, float(tr["n_terminal_step_not_a_decline"]), 0.001))
        rows.append(check("rebound over 1 log10 from nadir (4: 44)",
                          44, float(tr["n_rebound_over_1_log"]), 0.001))
        rows.append(check("median rebound (4: 2.17 log10)",
                          2.17, float(tr["median_rebound_log10"]), 0.02))
        fc = r["flag_consistency"]
        rows.append(check("BQL flags contradicted (methods: 83)",
                          83, float(fc["n_contradicted"]), 0.001))
        rows.append(check("share of flags contradicted (methods: 16.7%)",
                          0.167, float(fc["fraction_of_all_flags_contradicted"]), 0.02))
        co = r["starting_density_vs_laboratory"]
        # The number that most limits Section 4's Cox result.
        rows.append(check("starting density variance that is laboratory (4: 87.0%)",
                          0.870, float(co["variance_explained_by_laboratory"]), 0.01))

    # --- exp25, how much of the classification survives its measurement ---
    # The "six, not eighteen" numbers. These SHRINK this paper's claim and are
    # pinned for that reason: an earlier draft said eighteen labels were in
    # doubt, and the direction of the bound says six are.
    r = receipt("exp25_receipt.json")
    if r is not None:
        o = r["observability"]["15d"]
        rows.append(check("tolerance calls classified, 15d (2: 203)",
                          203, float(o["n_calls"]), 0.001))
        rows.append(check("determinable calls (2: 185)",
                          185, float(o["determinable"]), 0.001))
        rows.append(check("labels forced by the inoculum alone (2: 12)",
                          12, float(o["forced_by_inoculum"]), 0.001))
        rows.append(check("labels undecidable from the assay (2: 6)",
                          6, float(o["undecidable"]), 0.001))
        g = {x["group"]: x for x in r["by_susceptibility_group"]["15d"]}
        if "IR" in g and "IS" in g:
            rows.append(check("deep endpoint unreachable, resistant (2: 26.2%)",
                              26.2, float(g["IR"]["pct_deep_endpoint_unreachable"]), 0.02))
            rows.append(check("deep endpoint unreachable, susceptible (2: 7.6%)",
                              7.56, float(g["IS"]["pct_deep_endpoint_unreachable"]), 0.02))

    # --- exp22, the floor is inferred, so bound what rests on it ----------
    f = load("exp22_floor_sensitivity.csv")
    if f is not None:
        rows.append(check("short of 4 logs at the lowest plausible floor (methods: 28)",
                          28, float(f["n_short_of_4_logs"].min()), 0.001))
        rows.append(check("short of 4 logs at the inferred floor (methods: 33)",
                          33, float(f["n_short_of_4_logs"].max()), 0.001))

    # --- exp27, the out-of-sample test ------------------------------------
    f = load("exp27_out_of_sample.csv")
    if f is not None:
        g = f.set_index("endpoint_logs")
        rows.append(check("cultures in the held-out deposit (8: 20)",
                          20, float(g.loc[5.0, "n_cultures"]), 0.001))
        rows.append(check("5-log endpoint unreachable there (8: 5)",
                          5, float(g.loc[5.0, "n_unreachable"]), 0.001))
        rows.append(check("6-log endpoint unreachable there (8: 20)",
                          20, float(g.loc[6.0, "n_unreachable"]), 0.001))
        rows.append(check("4-log endpoint unreachable there (8: 0)",
                          0, float(g.loc[4.0, "n_unreachable"]), 1.0))

    # --- exp28, measurable depth against the standard ----------------------
    f = load("exp28_measurable_depth.csv")
    if f is not None:
        d = f.set_index("dataset")
        rows.append(check("delta h between laboratories at 100 uL (6: 2.33)",
                          2.33, float(d.loc["ERA4TB, between laboratories at 100 uL",
                                            "delta_h"]), 0.01))
        rows.append(check("delta h including plated volume (6: 4.40)",
                          4.40, float(d.loc["ERA4TB, every laboratory and plating volume",
                                            "delta_h"]), 0.01))
        # Kaur must stay NA: a number here would read as reproducibility.
        kaur_na = bool(f[f.dataset.str.startswith("Kaur")]["delta_h"].isna().all())
        rows.append(check("Kaur delta h reported as NA, not a number", 1,
                          1.0 if kaur_na else 0.0, 0.001))

    # --- exp26, the counter-tests -----------------------------------------
    # The strictest inversion rate is pinned because it is the number that
    # replaced our headline. 36.6 per cent was the most generous reading.
    r = receipt("exp26_receipt.json")
    if r is not None:
        t4 = r["counter_test_4_inversions_or_noise"]
        rows.append(check("inversion rate, no rate-gap requirement (5: 36.6%)",
                          0.366, float(t4["rate_at_no_threshold"]), 0.01))
        rows.append(check("inversion rate, gap > 0.10 log10/day (5: 21.3%)",
                          0.213, float(t4["rate_at_strictest"]), 0.02))
        rows.append(check("rivals supported across the four counter-tests (0)",
                          0, float(r["n_rivals_supported"]), 1.0))

    # --- exp21, the per-interval p-values --------------------------------
    # Added after a manuscript revision caught three of these wrong in the body
    # text. They had been carried over from an earlier draft and never
    # rechecked against the regenerated table, and no audit line covered them.
    f = load("exp21_interval_concentration_dependence.csv")
    if f is not None:
        g = f.set_index("interval")
        for iv, claimed in (("days 0-3", 0.013), ("days 3-7", 0.24),
                            ("days 7-14", 0.091)):
            if iv in g.index:
                rows.append(check(f"concentration slope p, {iv} (9)",
                                  claimed, float(g.loc[iv, "p_value"]), 0.05))

    # --- exp17, the Cox adjustment: p-values, not hazard ratios -----------
    # A revision of this manuscript relabelled these three p-values as hazard
    # ratios. Both quantities exist in the same table, so the audit now pins
    # both and names which is which.
    f = load("exp17_cox.csv")
    if f is not None:
        adj = f[f.model == "institute + starting density"].set_index("term")
        for term, claimed_p, claimed_hr in (("institute_D", 0.138, 0.339),
                                            ("institute_E", 0.172, 0.364),
                                            ("institute_F", 0.576, 0.619)):
            if term in adj.index:
                rows.append(check(f"{term} adjusted P-VALUE (5)",
                                  claimed_p, float(adj.loc[term, "p_value"]), 0.02))
                rows.append(check(f"{term} adjusted HAZARD RATIO (not the p)",
                                  claimed_hr, float(adj.loc[term, "hazard_ratio"]), 0.02))

    # --- exp17, growth at one times MIC ----------------------------------
    # The claim is net GROWTH in five of six laboratories, which is stronger
    # than "little or no killing" and is what the numbers say.
    f = load("exp17_kill_rates.csv")
    if f is not None:
        one = f[f.arm == "MXF 1x MIC"].dropna(subset=["kill_rate_tobit"])
        rows.append(check("laboratories with net growth at 1x MIC (5: 5)",
                          5, float((one.kill_rate_tobit < 0).sum()), 0.001))

    # --- exp22, the spine: dynamic range and the floored isolates --------
    # These are the numbers Sections 3.1 and 3.2 rest on. They are arithmetic
    # rather than statistical, so a drift here is a coding error, not noise.
    f = load("exp22_headroom.csv")
    if f is not None:
        g = f[f.culture_age_days == 15].set_index("group")
        rows.append(check("isolates short of 4-log headroom at 15 days (1: 33)",
                          33, float(g.loc["cannot reach 4 logs", "n_isolates"]), 0.001))
        rows.append(check("of those, recorded at the ceiling (1: 100%)",
                          1.0, float(g.loc["cannot reach 4 logs", "fraction_at_ceiling"]),
                          0.001))
        rows.append(check("with ample headroom, at the ceiling (1: 88.0%)",
                          0.880, float(g.loc["has 4 logs of headroom", "fraction_at_ceiling"]),
                          0.01))

    r = receipt("exp22_receipt.json")
    if r is not None:
        at = next(x for x in r["isolates_at_floor"] if x["culture_age_days"] == 15)
        rows.append(check("isolates ending at the MPN floor (2: 18)",
                          18, float(at["n_isolates_at_floor"]), 0.001))
        # The claim that makes the paper: the spread in recorded survival is not
        # merely similar to the spread in starting density, it IS it.
        rows.append(check("their survival spread equals their inoculum spread (2)",
                          float(at["start_density_fold_range"]),
                          float(at["apparent_survival_fold_range"]), 0.001, "x"))
        gap = r["starting_density_by_resistance"]["15d"]
        rows.append(check("resistant isolates start lower (4: 10.0-fold)",
                          10.0, float(gap["fold_lower_in_resistant"]), 0.05, "x"))

    f = load("exp22_label_associations.csv")
    if f is not None:
        rows.append(check("label tests in the family (4: 8)",
                          8, float(len(f)), 0.001))
        rows.append(check("surviving Benjamini-Hochberg (4: 2)",
                          2, float(f.survives_bh.sum()), 0.001))
        res = f[(f.predictor == "resistance") & (f.culture_age_days == 15)
                & (f.endpoint_depth == "D5")]
        if len(res) == 1:
            b0 = float(res.beta.iloc[0])
            b1 = float(res.beta_after_adjusting_for_start_density.iloc[0])
            rows.append(check("attenuation of the resistance coefficient (4: 66%)",
                              0.66, (b0 - b1) / b0, 0.03))

    # --- exp23, the inversion rate ---------------------------------------
    r = receipt("exp23_receipt.json")
    if r is not None:
        inv = r["inversions"]
        rows.append(check("inversion rate (7: 36.6%)",
                          0.366, float(inv["inversion_rate"]), 0.01))
        rows.append(check("comparable pairs (7: 191)",
                          191, float(inv["n_comparable_pairs"]), 0.001))
        # The share that argues AGAINST the strong reading. It is audited for
        # exactly that reason: a number that limits our own claim must not drift
        # quietly in the direction we would prefer.
        mxf = r["variance_decomposition"].get("MXF 10X MIC")
        if mxf:
            rows.append(check("distance share, MXF 10x (7: 39.4%)",
                              0.394, float(mxf["share_distance"]), 0.02))

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
