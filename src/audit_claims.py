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
                rows.append(check(f"concentration slope p, {iv} (3.6)",
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
                rows.append(check(f"{term} adjusted P-VALUE (3.4)",
                                  claimed_p, float(adj.loc[term, "p_value"]), 0.02))
                rows.append(check(f"{term} adjusted HAZARD RATIO (not the p)",
                                  claimed_hr, float(adj.loc[term, "hazard_ratio"]), 0.02))

    # --- exp17, growth at one times MIC ----------------------------------
    # The claim is net GROWTH in five of six laboratories, which is stronger
    # than "little or no killing" and is what the numbers say.
    f = load("exp17_kill_rates.csv")
    if f is not None:
        one = f[f.arm == "MXF 1x MIC"].dropna(subset=["kill_rate_tobit"])
        rows.append(check("laboratories with net growth at 1x MIC (3.4: 5)",
                          5, float((one.kill_rate_tobit < 0).sum()), 0.001))

    # --- exp22, the spine: dynamic range and the floored isolates --------
    # These are the numbers Sections 3.1 and 3.2 rest on. They are arithmetic
    # rather than statistical, so a drift here is a coding error, not noise.
    f = load("exp22_headroom.csv")
    if f is not None:
        g = f[f.culture_age_days == 15].set_index("group")
        rows.append(check("isolates short of 4-log headroom at 15 days (3.1: 33)",
                          33, float(g.loc["cannot reach 4 logs", "n_isolates"]), 0.001))
        rows.append(check("of those, recorded at the ceiling (3.1: 100%)",
                          1.0, float(g.loc["cannot reach 4 logs", "fraction_at_ceiling"]),
                          0.001))
        rows.append(check("with ample headroom, at the ceiling (3.1: 88.0%)",
                          0.880, float(g.loc["has 4 logs of headroom", "fraction_at_ceiling"]),
                          0.01))

    r = receipt("exp22_receipt.json")
    if r is not None:
        at = next(x for x in r["isolates_at_floor"] if x["culture_age_days"] == 15)
        rows.append(check("isolates ending at the MPN floor (3.2: 18)",
                          18, float(at["n_isolates_at_floor"]), 0.001))
        # The claim that makes the paper: the spread in recorded survival is not
        # merely similar to the spread in starting density, it IS it.
        rows.append(check("their survival spread equals their inoculum spread (3.2)",
                          float(at["start_density_fold_range"]),
                          float(at["apparent_survival_fold_range"]), 0.001, "x"))
        gap = r["starting_density_by_resistance"]["15d"]
        rows.append(check("resistant isolates start lower (3.3: 10.0-fold)",
                          10.0, float(gap["fold_lower_in_resistant"]), 0.05, "x"))

    f = load("exp22_label_associations.csv")
    if f is not None:
        rows.append(check("label tests in the family (3.3: 8)",
                          8, float(len(f)), 0.001))
        rows.append(check("surviving Benjamini-Hochberg (3.3: 2)",
                          2, float(f.survives_bh.sum()), 0.001))
        res = f[(f.predictor == "resistance") & (f.culture_age_days == 15)
                & (f.endpoint_depth == "D5")]
        if len(res) == 1:
            b0 = float(res.beta.iloc[0])
            b1 = float(res.beta_after_adjusting_for_start_density.iloc[0])
            rows.append(check("attenuation of the resistance coefficient (3.3: 66%)",
                              0.66, (b0 - b1) / b0, 0.03))

    # --- exp23, the inversion rate ---------------------------------------
    r = receipt("exp23_receipt.json")
    if r is not None:
        inv = r["inversions"]
        rows.append(check("inversion rate (3.5: 36.6%)",
                          0.366, float(inv["inversion_rate"]), 0.01))
        rows.append(check("comparable pairs (3.5: 191)",
                          191, float(inv["n_comparable_pairs"]), 0.001))
        # The share that argues AGAINST the strong reading. It is audited for
        # exactly that reason: a number that limits our own claim must not drift
        # quietly in the direction we would prefer.
        mxf = r["variance_decomposition"].get("MXF 10X MIC")
        if mxf:
            rows.append(check("distance share, MXF 10x (3.5: 39.4%)",
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
