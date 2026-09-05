"""
What the concentration axis is worth, and when it stops being worth anything.

Run:  python -m src.experiments.exp20_regimen_design

WHY THIS EXISTS. Everything else in this project is diagnostic: it establishes
that pharmacodynamic parameters are condition-dependent and that duration
endpoints confound drug action with the starting state. That is worth
establishing, but it tells nobody what to do differently. This script asks the
constructive question. Given a dose-by-time grid measured on a slow grower,
what does it actually say about how these drugs should be given and, more
sharply, about when a regimen should be judged?

THE DATA. figshare 26462791, CC BY 4.0: apramycin and amikacin against
Mycobacterium tuberculosis at 128, 32, 8, 4 and 1 ug/mL, triplicate log10 CFU at
days 0, 3, 7 and 14, with a concurrent drug-free control at every visit. A
32-fold concentration range crossed with a fourfold time range, in one
laboratory, with one readout. That crossing is what makes the question
answerable: neither axis alone would settle it.

THREE FINDINGS, and they do not all point the same way.

  1. THERE IS A THRESHOLD, AND BELOW IT TIME MAKES THINGS WORSE. At 1 ug/mL the
     apramycin arm does not merely fail to kill: the population rises from 7.02
     to 8.17 log10 over fourteen days. Amikacin at the same concentration ends
     at 6.82, barely below where it started, against a control that reached
     9.35. Sub-threshold exposure held for a long time is the one regimen the
     data condemn outright, because it combines no killing with continuous
     selection. Whatever else follows, that is the arm to avoid.

  2. ABOVE THE THRESHOLD, THE VALUE OF CONCENTRATION IS FRONT-LOADED. Comparing
     128 against 4 ug/mL, the ratio of kill rates is 3.16 over days 0 to 3, 1.68
     over days 3 to 7, and 0.66 over days 7 to 14. The high dose decelerates while
     the low dose accelerates, and by the last interval the measured ranking has
     reversed, though see below for why that reversal is not claimed as real.
     Concentration buys speed early and much less late.

  3. BUT MORE DRUG IS NOT SIMPLY BETTER, AND THE SCRIPT SAYS SO. Thirty-two
     times the concentration buys 0.71 log10 of additional kill by day 14, at
     thirty-two times the cumulative exposure. On a drug whose toxicity accumulates
     this is not a free choice, and a reading of these data as "give more"
     would be selective. What the data support is giving enough, early, rather
     than giving more for longer.

THE FINDING THAT IS ACTUALLY NEW, and it is about measurement rather than
dosing. The separation between the top and bottom of a 32-fold concentration
range is 6.9-fold in survivors at day 3, 48.2-fold at day 7, and 5.2-fold at day
14. An experiment or a trial that reads out at fourteen days sees almost no dose
response across a 32-fold range, and would conclude the drug is dose-insensitive.
The same experiment read at seven days sees a 48-fold separation. The dose
information is not absent; it has been destroyed by the choice of endpoint.

WHETHER THE LATE INVERSION IS REAL. It cannot be established from these data,
and the script says so rather than claiming it. By day 14 the high-dose arm is
at 65 CFU/mL and the source records no limit of quantification anywhere. An arm
sitting at or below such a limit has been censored, and a censored count
understates the killing, so its apparent rate is a LOWER bound on the true one.
At any limit of 2.0 log10 or above the high arm is censored, and 10 uL plating,
routine for mycobacteria, puts the limit exactly there; exp17 measures that same
ladder directly in another laboratory.

So the claim that the low dose overtakes the high one is not made. The claim
that survives needs no assumption about the floor at all: whether the ranking
inverts or merely collapses, a 32-fold concentration range separates 48-fold at
day 7 and 5-fold at day 14, so the late endpoint cannot resolve the dose. That
is the part a regimen decision would rest on, and it holds either way.

Writes:
  results/tables/exp20_kill_grid.csv
  results/tables/exp20_endpoint_separation.csv
  results/tables/exp20_exposure_efficiency.csv
  results/tables/exp20_floor_sensitivity.csv
  results/receipts/exp20_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "apramycin_mtb" / "Raw Data.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

HIGH, LOW = 128.0, 4.0          # top and bottom of the range that kills


def load() -> tuple[pd.DataFrame, float, pd.Series]:
    d = pd.read_excel(DATA, sheet_name="Kill kinetics", header=None)
    base = float(d.iloc[3, 7])
    k = d.iloc[4:, 1:8].copy()
    k.columns = ["day", "compound", "conc", "r1", "r2", "r3", "avg"]
    k["day"] = k["day"].ffill()
    k["compound"] = k["compound"].ffill()
    k = k[pd.to_numeric(k["avg"], errors="coerce").notna()].copy()
    k["avg"] = k["avg"].astype(float)
    k["dayn"] = k["day"].astype(str).str.extract(r"(\d+)").astype(float)
    ctrl = k[k["compound"] == "Cell control"].set_index("dayn")["avg"]
    return k, base, ctrl


def grid_for(k: pd.DataFrame, base: float, drug: str) -> pd.DataFrame:
    g = k[k["compound"] == drug].pivot_table(index="conc", columns="dayn", values="avg")
    g.insert(0, 0.0, base)
    return g.sort_index()


def interval_rates(g: pd.DataFrame) -> pd.DataFrame:
    cols = list(g.columns)
    return pd.DataFrame(
        {f"d{int(a)}-{int(b)}": (g[a] - g[b]) / (b - a)
         for a, b in zip(cols[:-1], cols[1:])}, index=g.index)


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; see the docstring for its source")
    pd.set_option("display.width", 210)

    k, base, ctrl = load()
    ap = grid_for(k, base, "Apramycin")
    am = grid_for(k, base, "Amikacin")
    rates = interval_rates(ap)

    out = ap.copy()
    out.columns = [f"log10_day{int(c)}" for c in out.columns]
    out = out.join(rates)
    out.to_csv(TABLES / "exp20_kill_grid.csv")

    print(f"-- apramycin, log10 CFU/mL (inoculum {base:.2f}, control reaches "
          f"{ctrl.max():.2f} by day {int(ctrl.idxmax())}) --")
    print(ap.to_string(float_format=lambda v: f"{v:6.2f}"))
    print("\n-- interval kill rate, log10 per day --")
    print(rates.to_string(float_format=lambda v: f"{v:+7.3f}"))

    # -- 1. the threshold ---------------------------------------------------
    print("\n-- 1. below the threshold, time makes it worse --")
    for name, g in (("apramycin", ap), ("amikacin", am)):
        lowest = g.index.min()
        change = g.loc[lowest, 14.0] - base
        verb = "GREW" if change > 0 else "fell"
        print(f"   {name} at {lowest:g} ug/mL: {base:.2f} -> {g.loc[lowest, 14.0]:.2f} log10, "
              f"{verb} by {abs(change):.2f} log10 over 14 days")
    print("   Sub-threshold exposure held for two weeks combines no killing with")
    print("   continuous selection. It is the one arm these data condemn outright.")

    # -- 2. the dose effect is front-loaded ---------------------------------
    print("\n-- 2. concentration buys speed early and nothing late --")
    print(f"   {'interval':<10}{f'{HIGH:g} ug/mL':>12}{f'{LOW:g} ug/mL':>12}{'ratio':>9}")
    front = []
    for c in rates.columns:
        hi, lo = rates.loc[HIGH, c], rates.loc[LOW, c]
        front.append({"interval": c, "rate_high": hi, "rate_low": lo,
                      "ratio_high_over_low": hi / lo if lo else np.nan})
        print(f"   {c:<10}{hi:>+12.3f}{lo:>+12.3f}{hi/lo:>9.2f}")

    # -- 3. more drug is not simply better ----------------------------------
    eff = []
    for c in ap.index:
        if c < LOW:
            continue
        for day in (3.0, 7.0, 14.0):
            drop = base - ap.loc[c, day]
            auc = c * day                       # ug/mL x days, a crude exposure
            eff.append({"conc_ug_ml": c, "day": day, "log10_killed": drop,
                        "cumulative_exposure_ug_d_ml": auc,
                        "log10_per_unit_exposure": drop / auc if auc else np.nan})
    eff = pd.DataFrame(eff)
    eff.to_csv(TABLES / "exp20_exposure_efficiency.csv", index=False)

    d14 = eff[eff["day"] == 14.0].set_index("conc_ug_ml")
    extra = d14.loc[HIGH, "log10_killed"] - d14.loc[LOW, "log10_killed"]
    cost = d14.loc[HIGH, "cumulative_exposure_ug_d_ml"] / d14.loc[LOW, "cumulative_exposure_ug_d_ml"]
    print("\n-- 3. but more drug is not simply better --")
    print(f"   {HIGH:g} vs {LOW:g} ug/mL at day 14: {extra:+.2f} log10 of extra kill "
          f"for {cost:.0f}x the cumulative exposure.")
    print("   On an aminoglycoside, whose toxicity accumulates, that is not a free")
    print("   choice. The support is for giving enough early, not more for longer.")

    # -- 4. the endpoint decides what can be seen ---------------------------
    sep = []
    for day in (3.0, 7.0, 14.0):
        s = 10 ** (ap.loc[LOW, day] - ap.loc[HIGH, day])
        sep.append({"day": day, "survivor_ratio_low_over_high": s,
                    "log10_separation": ap.loc[LOW, day] - ap.loc[HIGH, day]})
    sep = pd.DataFrame(sep)
    sep.to_csv(TABLES / "exp20_endpoint_separation.csv", index=False)
    best = sep.loc[sep["survivor_ratio_low_over_high"].idxmax()]
    worst = sep.loc[sep["survivor_ratio_low_over_high"].idxmin()]

    print(f"\n-- 4. the endpoint decides whether a {HIGH/LOW:.0f}-fold dose range is visible --")
    print(sep.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
    print(f"\n   Read at day {int(best['day'])}, the same 32-fold range separates "
          f"{best['survivor_ratio_low_over_high']:.0f}-fold.")
    print(f"   Read at day {int(worst['day'])}, it separates "
          f"{worst['survivor_ratio_low_over_high']:.0f}-fold, and the drug looks")
    print("   dose-insensitive. The information is not absent; the endpoint destroyed it.")

    # -- 5. is the late inversion real, or a floor? -------------------------
    # An arm sitting at or below a quantification limit has been censored, and a
    # censored observation understates the killing: the true count is somewhere
    # below the limit, so the true rate is FASTER than the one computed from it.
    # The observed rate is therefore a lower bound, and an inversion built on it
    # is unproven rather than established. The limits tested span the plating
    # volumes ordinarily used for mycobacteria: 100 uL undiluted gives one
    # colony per 10 CFU/mL, 10 uL gives 100 CFU/mL, 2.5 uL gives 400 CFU/mL,
    # matching the ladder measured directly in exp17.
    hi14, lo14 = ap.loc[HIGH, 14.0], ap.loc[LOW, 14.0]
    floors = []
    for lod, why in ((1.0, "100 uL plated, 10 CFU/mL"),
                     (1.7, "50 uL plated, 20 CFU/mL"),
                     (2.0, "10 uL plated, 100 CFU/mL"),
                     (2.6, "2.5 uL plated, 400 CFU/mL")):
        hi_cens, lo_cens = hi14 <= lod, lo14 <= lod
        floors.append({
            "assumed_loq_log10": lod, "corresponds_to": why,
            "high_arm_censored": bool(hi_cens), "low_arm_censored": bool(lo_cens),
            "observed_rate_high": (ap.loc[HIGH, 7.0] - hi14) / 7.0,
            "observed_rate_low": (ap.loc[LOW, 7.0] - lo14) / 7.0,
            "high_rate_is_lower_bound": bool(hi_cens),
            "inversion_established": bool(not hi_cens),
        })
    fl = pd.DataFrame(floors)
    fl.to_csv(TABLES / "exp20_floor_sensitivity.csv", index=False)

    print("\n-- 5. is the late inversion real, or the high arm hitting a floor? --")
    print(f"   at day 14 the high arm is at {hi14:.2f} log10 = {10**hi14:,.0f} CFU/mL, "
          f"the low arm at {lo14:.2f} = {10**lo14:,.0f} CFU/mL")
    print(fl[["assumed_loq_log10", "corresponds_to", "high_arm_censored",
              "inversion_established"]].to_string(index=False,
                                                  float_format=lambda v: f"{v:,.1f}"))
    unproven = fl[~fl["inversion_established"]]
    if len(unproven):
        lo_lim = float(unproven["assumed_loq_log10"].min())
        print(f"\n   At any limit of {lo_lim:.1f} log10 ({10**lo_lim:,.0f} CFU/mL) or above, the")
        print("   high arm is censored, its observed rate is only a lower bound, and the")
        print("   inversion cannot be established. The source records no limit anywhere,")
        print("   and 10 uL plating, which is routine for mycobacteria, puts it exactly")
        print("   there. So the claim that the low dose OVERTAKES the high one is NOT")
        print("   made here.")
    print("\n   What is claimed is the weaker statement, which needs no assumption about")
    print("   the floor: by day 14 a 32-fold concentration range separates only")
    print(f"   {sep['survivor_ratio_low_over_high'].iloc[-1]:.0f}-fold in survivors, against "
          f"{sep['survivor_ratio_low_over_high'].max():.0f}-fold at day 7. Whether the")
    print("   ranking truly inverts or merely collapses, the late endpoint cannot resolve")
    print("   the dose, and that is the part a regimen decision would rest on.")

    (RECEIPTS / "exp20_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp20_regimen_design.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_doi": "10.6084/m9.figshare.26462791.v1",
        "licence": "CC BY 4.0",
        "organism": "Mycobacterium tuberculosis",
        "drugs": ["apramycin", "amikacin"],
        "inoculum_log10": base,
        "subthreshold_conc_ug_ml": float(ap.index.min()),
        "subthreshold_change_log10": float(ap.loc[ap.index.min(), 14.0] - base),
        "front_loading": front,
        "extra_log10_for_32x_dose_at_day14": float(extra),
        "exposure_cost_fold": float(cost),
        "endpoint_separation": sep.to_dict(orient="records"),
        "best_endpoint_day": float(best["day"]),
        "worst_endpoint_day": float(worst["day"]),
        "floor_sensitivity": fl.to_dict(orient="records"),
        "inversion_established_at_any_plausible_loq": bool(
            fl["inversion_established"].all()),
        "high_arm_day14_cfu_per_ml": float(10 ** ap.loc[HIGH, 14.0]),
        "claim_made": ("above a threshold the value of concentration is front-loaded, and "
                       "a late endpoint cannot resolve a 32-fold dose range; the claim "
                       "that a low dose overtakes a high one is NOT made"),
    }, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
