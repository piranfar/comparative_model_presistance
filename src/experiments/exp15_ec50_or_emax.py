"""
Does nutrient limitation shift potency, or lower the ceiling? The question that
decides whether dose can compensate.

Run:  python -m src.experiments.exp15_ec50_or_emax

WHY IT MATTERS. exp14 measured a 19-fold span in the ordinary-cell kill rate
across the nutrient axis. How much that matters clinically depends entirely on
which parameter it moves.

  If nutrient limitation shifts EC50, it is a potency effect. The curves move
  right, more drug is needed for the same killing, and at a high enough dose
  full killing returns. Every term already in a pharmacodynamic model behaves
  this way: tissue penetration, protein binding, and the pH effect on
  aminoglycosides, which Baudoux et al. showed explicitly preserves Emax.

  If it lowers Emax, it is a ceiling effect. The curves flatten at different
  heights, and no concentration recovers the difference. Nothing on the
  concentration axis of a model can absorb it.

Hall et al. 2019 (AAC 63(10), doi:10.1128/AAC.01313-19) restored tobramycin
killing in tolerant Pseudomonas by feeding fumarate rather than by raising the
dose, which argues for the second reading, but that is an argument and not a
measurement on this system.

THE TEST. The Windels grid has both axes: six concentrations spanning 32-fold at
each of six nutrient levels. Two signatures separate the hypotheses.

  Under a pure EC50 shift the curves converge at high concentration, so the
  ratio between the best-fed and worst-fed condition falls towards one as
  concentration rises.

  Under a pure Emax effect the ratio is flat in concentration.

Partial convergence means both, and the quantity that matters is then how much
of the gap survives at the top of the range, because that part cannot be dosed
away.

A CAVEAT THAT BOUNDS THE ANSWER. If the response has not saturated by 400 ug/mL,
the ceiling is not observed and only a lower bound on the surviving gap can be
given. The script tests for saturation rather than assuming it.

Data: Windels et al. 2024, ISME J 18(1):wrae070, Zenodo 7550302, CC BY 4.0.
Drug: amikacin.

Writes:
  results/tables/exp15_kill_rate_grid.csv
  results/tables/exp15_convergence.csv
  results/receipts/exp15_receipt.json
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

RICH, POOR = 0.90, 0.00       # best-fed and worst-fed levels with a full series


def kill_grid(d: pd.DataFrame) -> pd.DataFrame:
    """Maximum instantaneous kill rate at each nutrient level and concentration."""
    rows = []
    for (nut, c), g in d.groupby(["nutrient_conc", "AB_conc"]):
        s = (g.groupby("time")["surv_frac"]
             .apply(lambda v: float(np.exp(np.log(v).mean()))))
        s = np.log(s.dropna())
        if len(s) < 2:
            continue
        r = -np.diff(s.values) / np.diff(s.index.values.astype(float))
        rows.append({"nutrient_conc": nut, "AB_conc": c,
                     "kill_rate_per_h": float(np.nanmax(r)),
                     "n_intervals": int(len(r))})
    return pd.DataFrame(rows)


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)

    d = pd.read_csv(DATA)
    d = d[d["surv_frac"] > 0]          # keep t=0: the first interval is the fast phase
    grid = kill_grid(d)
    grid.to_csv(TABLES / "exp15_kill_rate_grid.csv", index=False)

    piv = grid.pivot(index="AB_conc", columns="nutrient_conc",
                     values="kill_rate_per_h")
    pd.set_option("display.width", 200)
    print("-- maximum kill rate per hour, by concentration and nutrient level --")
    print(piv.to_string(float_format=lambda v: f"{v:6.2f}"))

    # Signature 1: does the rich-to-poor ratio fall as concentration rises?
    rows = []
    for c in piv.index:
        if RICH in piv.columns and POOR in piv.columns:
            a, b = piv.loc[c, RICH], piv.loc[c, POOR]
            if np.isfinite(a) and np.isfinite(b) and b > 0:
                rows.append({"AB_conc": c, "rich": a, "poor": b, "ratio": a / b})
    conv = pd.DataFrame(rows)
    conv.to_csv(TABLES / "exp15_convergence.csv", index=False)

    print(f"\n-- ratio between nutrient {RICH:g} and nutrient {POOR:g} --")
    print(conv.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))

    lr = stats.linregress(np.log2(conv["AB_conc"]), np.log(conv["ratio"]))
    print(f"\nratio against log2 concentration: slope {lr.slope:+.3f} per doubling, "
          f"p = {lr.pvalue:.3g}")
    if lr.pvalue < 0.05 and lr.slope < 0:
        print("   the curves converge as dose rises, which is an EC50 signature")
    elif lr.pvalue >= 0.05:
        print("   no significant convergence, which is an Emax signature")

    # Signature 2: has the response saturated by the top concentration?
    top2 = sorted(piv.index)[-2:]
    sat = []
    for nut in piv.columns:
        v = piv.loc[top2, nut].dropna()
        if len(v) == 2:
            sat.append({"nutrient_conc": nut, "at_second_highest": v.iloc[0],
                        "at_highest": v.iloc[1],
                        "still_rising": bool(v.iloc[1] > v.iloc[0] * 1.05)})
    sat = pd.DataFrame(sat)
    print(f"\n-- has killing saturated between {top2[0]:g} and {top2[1]:g} ug/mL? --")
    print(sat.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))

    surviving = float(conv["ratio"].iloc[-1]) if len(conv) else np.nan
    initial = float(conv["ratio"].iloc[0]) if len(conv) else np.nan

    (RECEIPTS / "exp15_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp15_ec50_or_emax.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_doi": "10.5281/zenodo.7550302",
        "antibiotic": "amikacin",
        "rich_nutrient": RICH, "poor_nutrient": POOR,
        "ratio_at_lowest_concentration": initial,
        "ratio_at_highest_concentration": surviving,
        "convergence_slope_per_doubling": float(lr.slope),
        "convergence_p": float(lr.pvalue),
        "n_levels_still_rising_at_top": int(sat["still_rising"].sum()) if len(sat) else 0,
        "n_levels_tested": int(len(sat)),
        "interpretation": ("partial convergence: an EC50 component plus a surviving gap"
                           if lr.pvalue < 0.05 and lr.slope < 0 and surviving > 1.5
                           else "see printed output"),
    }, indent=2), encoding="utf-8")

    print(f"\nthe gap falls from {initial:.0f}-fold at the lowest concentration to "
          f"{surviving:.1f}-fold at the highest.")
    print("Whatever survives at the top of the range is the part no dose recovers,")
    print("subject to the saturation check above.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
