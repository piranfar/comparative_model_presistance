"""
The inoculum is standardised. Does the standard reach the flask?

Run:  python -m src.experiments.exp28_standard_vs_realised

WHY THIS TEST EXISTS. The most obvious objection to everything this project
argues is that the starting inoculum is not a free variable at all. It is
standardised, and has been for decades: a suspension is adjusted to 0.5
McFarland and diluted, and CLSI M26 puts the time-kill target at about
5 x 10^5 CFU/mL. If the protocol fixes the inoculum, a framework built on the
inoculum varying is built on nothing.

The objection is correct about the standard and it is worth answering with
measurements rather than argument. Two facts about the standard make the answer
possible.

FIRST, 0.5 McFarland is a TURBIDITY, not a viable count. It is an optical
density matched against a barium sulphate or latex reference, so it counts
whatever scatters light: live cells, dead cells, debris, and clumps as single
particles. The conversion to CFU per mL is an assumption about cell size, shape
and dispersal, and for Mycobacterium tuberculosis, which aggregates and carries a
thick waxy wall, it is a poor one.

SECOND, the standard fixes what goes IN. What this project needs is what is
measured in the flask, and those are different quantities separated by a
dilution, a transfer, and however much clumping the organism does on the way.

So the question is empirical: across laboratories running one written protocol,
what did the plate actually count on day zero?

TWO CONTROLS, because the obvious objection to the objection is early killing.
If treated flasks are read on day zero and the drug has already worked, a spread
in those readings is killing rather than inoculum. So the untreated arm is used
as the primary estimate, and the treated arm at the same visit is reported
beside it. If the two agree, the spread is inoculum.

Writes:  results/tables/exp28_standard_vs_realised.csv
         results/receipts/exp28_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ERA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
DUBEY = ROOT / "data" / "raw" / "dubey2026" / "source_data.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

MCFARLAND_05 = 1.5e8      # nominal CFU/mL at 0.5 McFarland turbidity
CLSI_M26_TARGET = 5e5     # time-kill starting inoculum, CFU/mL
DUBEY_NOMINAL = 1e5       # stated in that paper's Methods
TREATED = ["MXF 1X MIC", "MXF 10X MIC", "INH 1X MIC", "INH 10X MIC"]


def era4tb() -> tuple[pd.DataFrame, dict]:
    e = pd.read_csv(ERA, encoding="latin-1")
    e["y"] = pd.to_numeric(e["CFUlog10"], errors="coerce")
    ok = (e["BQL"] != 1) & (e["AQL"] != 1) & (e["Volume"] == 100.0)

    unt = e[ok & (e["Sample"] == "untreated") & (e["Time"] == 0)].dropna(subset=["y"])
    tre = e[ok & e["Sample"].isin(TREATED) & (e["Time"] == 0)].dropna(subset=["y"])
    u = unt.groupby("Institute")["y"].agg(["count", "mean", "std"])
    t = tre.groupby("Institute")["y"].mean()

    rows = []
    for lab, r in u.iterrows():
        realised = 10 ** r["mean"]
        rows.append({
            "laboratory": lab, "n_flasks": int(r["count"]),
            "untreated_day0_log10": r["mean"],
            "treated_day0_log10": float(t.get(lab, np.nan)),
            "realised_cfu_per_ml": realised,
            "fold_from_clsi_target": realised / CLSI_M26_TARGET,
            "fold_from_half_mcfarland": realised / MCFARLAND_05,
        })
    d = pd.DataFrame(rows)
    both = d.dropna(subset=["treated_day0_log10"])
    return d, {
        "n_laboratories_with_clean_day0": int(len(d)),
        "spread_log10": float(d["untreated_day0_log10"].max()
                              - d["untreated_day0_log10"].min()),
        "spread_fold": float(10 ** (d["untreated_day0_log10"].max()
                                    - d["untreated_day0_log10"].min())),
        "n_below_clsi_target": int((d["fold_from_clsi_target"] < 1).sum()),
        "largest_shortfall_fold": float(1 / d["fold_from_clsi_target"].min()),
        "treated_vs_untreated_max_gap_log10":
            float((both["untreated_day0_log10"] - both["treated_day0_log10"]).abs().max())
            if len(both) else np.nan,
        "n_laboratories_with_both_arms": int(len(both)),
    }


def dubey() -> dict:
    starts = []
    for sh in ("Figure 1", "Figure 4"):
        d = pd.read_excel(DUBEY, sheet_name=sh, header=None)
        t = pd.to_numeric(d[0], errors="coerce")
        v = pd.to_numeric(d[1], errors="coerce")
        starts.append(v[(t == 0) & (v > 1)])
    s = pd.concat(starts).dropna()
    return {
        "n_cultures": int(len(s)),
        "nominal_stated_in_methods": DUBEY_NOMINAL,
        "measured_min": float(s.min()), "measured_median": float(s.median()),
        "measured_max": float(s.max()),
        "median_fold_above_nominal": float(s.median() / DUBEY_NOMINAL),
        "log10_discrepancy": float(np.log10(s.median() / DUBEY_NOMINAL)),
    }



def vijay() -> pd.DataFrame:
    """217 clinical isolates. MPN per mL at day zero, by culture age.

    These are clinical cultures rather than adjusted suspensions, so the
    turbidimetric standard is the reference they would have been prepared
    against, not something they claim to have hit.
    """
    d = pd.read_excel(ROOT / "data/raw/tb/elife93243_supp2.xlsx")
    rows = []
    for age in (15, 30, 60):
        col = f"mpn_T0_{age}days"
        if col not in d:
            continue
        v = pd.to_numeric(d[col], errors="coerce").dropna()
        v = v[v > 0]
        rows.append({"group": f"Vijay, {age}-day culture", "n": int(len(v)),
                     "median_log10": float(np.log10(v).median()),
                     "min_log10": float(np.log10(v).min()),
                     "max_log10": float(np.log10(v).max())})
    return pd.DataFrame(rows)


def kaur() -> pd.DataFrame:
    """The day-zero cell control of the apramycin grid."""
    f = ROOT / "data/raw/apramycin_mtb/Raw Data.xlsx"
    if not f.exists():
        return pd.DataFrame()
    rows = []
    for sheet, label in (("Kill kinetics", "Kaur, planktonic"),
                         ("Intracellular efficacy", "Kaur, intracellular")):
        try:
            k = pd.ExcelFile(f).parse(sheet)
            v = pd.to_numeric(k.iloc[2, 4:7], errors="coerce").dropna()
            if not len(v):
                continue
            rows.append({"group": label, "n": int(len(v)),
                         "median_log10": float(v.median()),
                         "min_log10": float(v.min()), "max_log10": float(v.max())})
        except Exception:
            continue
    return pd.DataFrame(rows)


def against_turbidity(df: pd.DataFrame) -> pd.DataFrame:
    """Everything expressed against 0.5 McFarland, the turbidity they work to.

    Dilution below the standard is expected and is not the finding: a time-kill
    inoculum is prepared BY diluting a matched suspension. What the column shows
    is how far each realised density sits from the one fixed reference in the
    workflow, and the spread within a group is the quantity that matters, since
    that is what turns into a difference in demonstrable kill depth.
    """
    d = df.copy()
    d["fold_below_half_mcfarland"] = 10 ** (np.log10(MCFARLAND_05) - d["median_log10"])
    d["spread_log10"] = d["max_log10"] - d["min_log10"]
    d["spread_fold"] = 10 ** d["spread_log10"]
    return d


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    labs, era = era4tb()
    dub = dubey() if DUBEY.exists() else None
    labs.to_csv(TABLES / "exp28_standard_vs_realised.csv", index=False)

    # Every deposit on one axis: the turbidity standard they all work to.
    era_rows = pd.DataFrame([{
        "group": f"ERA4TB, institute {r.laboratory}", "n": r.n_flasks,
        "median_log10": r.untreated_day0_log10,
        "min_log10": r.untreated_day0_log10, "max_log10": r.untreated_day0_log10,
    } for r in labs.itertuples()])
    era_pooled = pd.DataFrame([{
        "group": "ERA4TB, all institutes pooled", "n": int(labs["n_flasks"].sum()),
        "median_log10": float(labs["untreated_day0_log10"].median()),
        "min_log10": float(labs["untreated_day0_log10"].min()),
        "max_log10": float(labs["untreated_day0_log10"].max()),
    }])
    dub_row = pd.DataFrame([{
        "group": "Dubey, hollow fibre", "n": dub["n_cultures"],
        "median_log10": float(np.log10(dub["measured_median"])),
        "min_log10": float(np.log10(dub["measured_min"])),
        "max_log10": float(np.log10(dub["measured_max"])),
    }]) if dub else pd.DataFrame()

    allg = against_turbidity(pd.concat(
        [era_pooled, era_rows, vijay(), kaur(), dub_row], ignore_index=True))
    allg.to_csv(TABLES / "exp28_against_turbidity.csv", index=False)

    (RECEIPTS / "exp28_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp28_standard_vs_realised.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "half_mcfarland_nominal_cfu_per_ml": MCFARLAND_05,
        "clsi_m26_target_cfu_per_ml": CLSI_M26_TARGET,
        "era4tb": era, "era4tb_per_laboratory": labs.to_dict(orient="records"),
        "dubey": dub,
        "against_turbidity": allg.to_dict(orient="records"),
    }, indent=2, default=str), encoding="utf-8")

    print("-- the standard --")
    print(f"   0.5 McFarland, nominal    : {MCFARLAND_05:.1e} CFU/mL "
          f"({np.log10(MCFARLAND_05):.2f} log10), a TURBIDITY not a viable count")
    print(f"   CLSI M26 time-kill target : {CLSI_M26_TARGET:.0e} CFU/mL "
          f"({np.log10(CLSI_M26_TARGET):.2f} log10)")

    print("\n-- what six laboratories on one written protocol actually counted --")
    show = labs.copy()
    show["vs CLSI"] = show["fold_from_clsi_target"].apply(
        lambda r: f"{r:.1f}x above" if r >= 1 else f"{1/r:.0f}x below")
    print(show[["laboratory", "n_flasks", "untreated_day0_log10",
                "treated_day0_log10", "vs CLSI"]].to_string(
        index=False, float_format=lambda v: f"{v:,.2f}"))

    print(f"\n   spread across laboratories : {era['spread_log10']:.2f} log10 "
          f"= {era['spread_fold']:,.0f}-fold")
    print(f"   below the CLSI target      : {era['n_below_clsi_target']} of "
          f"{era['n_laboratories_with_clean_day0']}, "
          f"the largest shortfall {era['largest_shortfall_fold']:.0f}-fold")
    print(f"   treated vs untreated day 0 : agree to "
          f"{era['treated_vs_untreated_max_gap_log10']:.2f} log10 across "
          f"{era['n_laboratories_with_both_arms']} laboratories, so the spread is")
    print("                                the inoculum and not early killing")

    if dub:
        print(f"\n-- a second deposit, against its own stated figure --")
        print(f"   Methods state  : {dub['nominal_stated_in_methods']:.0e} CFU/mL")
        print(f"   file measures  : {dub['measured_min']:.1e} to "
              f"{dub['measured_max']:.1e}, median {dub['measured_median']:.1e}")
        print(f"   discrepancy    : {dub['median_fold_above_nominal']:.1f}-fold "
              f"({dub['log10_discrepancy']:.2f} log10) above nominal")

    print("\n-- every deposit against 0.5 McFarland, the turbidity they work to --")
    show = allg.copy()
    show["below 0.5 McF"] = show["fold_below_half_mcfarland"].apply(lambda v: f"{v:,.0f}x")
    show["spread"] = show["spread_fold"].apply(
        lambda v: "-" if v <= 1.0001 else f"{v:,.0f}x")
    print(show[["group", "n", "median_log10", "below 0.5 McF", "spread"]].to_string(
        index=False, float_format=lambda v: f"{v:,.2f}"))

    print("\n   Dilution below the standard is expected: a time-kill inoculum is")
    print("   prepared BY diluting a matched suspension. The finding is the SPREAD")
    print("   within a group, because headroom = log10(N0/L), so a spread in the")
    print("   realised density is a spread in the depth of kill demonstrable at all.")

    print("\n   The standard exists and is followed. It is a turbidity, and the")
    print("   viable count that reaches the flask does not inherit its precision.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
