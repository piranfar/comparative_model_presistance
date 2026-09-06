"""
How many of the published tolerance calls are actually determinable?

Run:  python -m src.experiments.exp25_observability_classes

WHY THIS TEST EXISTS. This paper shows that a reading resting on the assay floor
yields a recorded surviving fraction of L/N0 and that the deposited tolerance
labels are a threshold on that fraction. It has been reporting the consequence as
though every affected label were suspect. That is not right, and this experiment
is what makes it precise.

THE DIRECTION OF THE BOUND MATTERS, AND IT IS NOT SYMMETRIC. When the day-5
reading sits at the floor, the true count is somewhere between zero and the
floor, so the true surviving fraction is at most L/N0. Lower fraction means lower
tolerance. The recorded class is therefore an UPPER BOUND on the true class: such
an isolate may belong to a lower tolerance class than recorded, and can never
belong to a higher one.

This has an asymmetric consequence that the manuscript had missed. An isolate
recorded in the LOWEST class is bounded above by a class it already occupies, so
its label stands: it cannot be less tolerant than the least tolerant category.
Only an isolate recorded ABOVE the lowest class has a label that could be wrong.

So a tolerance call falls into one of three observability classes:

  DETERMINABLE     the day-5 reading is above the floor; the fraction is measured
                   and the label is a measurement
  BOUNDED, TIGHT   the reading is at the floor, and the recorded class is already
                   the lowest available; the bound cannot move the label
  BOUNDED, LOOSE   the reading is at the floor and the recorded class is above the
                   lowest; the true class may be lower, and the label is not
                   determinable from this assay

Counting them says how much of a published classification survives its own
measurement, which is a different and more useful number than counting how many
isolates hit the floor.

The same logic is applied to the deepest duration endpoint, where the constraint
is headroom rather than a floor-level reading: an isolate without the dynamic
range for a q-log reduction has an unreachable endpoint, and its record carries
no information about the drug at all.

Writes:
  results/tables/exp25_observability_classes.csv
  results/tables/exp25_observability_by_group.csv
  results/receipts/exp25_receipt.json
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

MPN_FLOOR = 23.0
DEEP_ENDPOINT_LOGS = 4.0            # the 99.99 per cent endpoint
CLASS_ORDER = {"Low": 0, "Medium": 1, "High": 2}
LOWEST_CLASS = "Low"


def classify(d: pd.DataFrame, age: int) -> pd.DataFrame:
    n0 = d[f"mpn_T0_{age}days"].astype(float)
    n5 = d[f"mpn_T5_{age}days"].astype(float)
    lab = d[f"Tolerant_level_D5_{age}"]
    usable = n0.notna() & n5.notna() & lab.isin(CLASS_ORDER)

    at_floor = n5 <= MPN_FLOOR
    lowest = lab == LOWEST_CLASS
    klass = np.where(~at_floor, "determinable",
                     np.where(lowest, "bounded, tight", "bounded, loose"))

    return pd.DataFrame({
        "culture_age_days": age,
        "usable": usable,
        "start_log10": np.log10(n0),
        "headroom_log10": np.log10(n0 / MPN_FLOOR),
        "day5_at_floor": at_floor,
        "recorded_class": lab,
        "observability": klass,
        "deep_endpoint_reachable": np.log10(n0 / MPN_FLOOR) >= DEEP_ENDPOINT_LOGS,
        "inh": d["INH-Suceptibility"],
    })[usable].reset_index(drop=True)


def summarise(c: pd.DataFrame) -> dict:
    n = len(c)
    out = {"n_calls": n}
    for k in ("determinable", "bounded, tight", "bounded, loose"):
        m = int((c["observability"] == k).sum())
        out[k.replace(", ", "_").replace(" ", "_")] = m
        out[k.replace(", ", "_").replace(" ", "_") + "_pct"] = 100 * m / n if n else np.nan
    loose = c[c["observability"] == "bounded, loose"]
    out["loose_recorded_classes"] = loose["recorded_class"].value_counts().to_dict()
    out["n_deep_endpoint_unreachable"] = int((~c["deep_endpoint_reachable"]).sum())
    out["pct_deep_endpoint_unreachable"] = 100 * (~c["deep_endpoint_reachable"]).mean()
    return out


def by_group(c: pd.DataFrame) -> pd.DataFrame:
    """Does observability differ between the groups a study would compare?

    If it does, a comparison of tolerance between those groups is partly a
    comparison of how well each group could be measured.
    """
    rows = []
    for g, sub in c[c["inh"].isin(["IS", "IR"])].groupby("inh"):
        rows.append({
            "group": g, "n": len(sub),
            "pct_determinable": 100 * (sub["observability"] == "determinable").mean(),
            "pct_deep_endpoint_unreachable": 100 * (~sub["deep_endpoint_reachable"]).mean(),
            "median_headroom_log10": float(sub["headroom_log10"].median()),
        })
    t = pd.DataFrame(rows)
    if len(t) == 2:
        ir = c[(c["inh"] == "IR")]; is_ = c[(c["inh"] == "IS")]
        tab = [[int((~ir["deep_endpoint_reachable"]).sum()), int(ir["deep_endpoint_reachable"].sum())],
               [int((~is_["deep_endpoint_reachable"]).sum()), int(is_["deep_endpoint_reachable"].sum())]]
        t["fisher_p_unreachable"] = stats.fisher_exact(tab)[1]
    return t


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    d = pd.read_excel(DATA)

    frames, summ, groups = [], {}, {}
    for age in (15, 60):
        c = classify(d, age)
        frames.append(c)
        summ[f"{age}d"] = summarise(c)
        g = by_group(c)
        groups[f"{age}d"] = g.to_dict(orient="records")
        if age == 15:
            g.to_csv(TABLES / "exp25_observability_by_group.csv", index=False)

    allc = pd.concat(frames, ignore_index=True)
    allc.to_csv(TABLES / "exp25_observability_classes.csv", index=False)

    (RECEIPTS / "exp25_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp25_observability_classes.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "eLife 93243 supplementary file 2",
        "mpn_floor_per_ml": MPN_FLOOR,
        "deep_endpoint_logs": DEEP_ENDPOINT_LOGS,
        "observability": summ,
        "by_susceptibility_group": groups,
    }, indent=2, default=str), encoding="utf-8")

    for age in (15, 60):
        s = summ[f"{age}d"]
        print(f"\n-- {age}-day panel: how much of the classification survives its "
              f"own measurement? (n={s['n_calls']}) --")
        print(f"   determinable, reading above the floor : "
              f"{s['determinable']:3d}  ({s['determinable_pct']:.1f}%)")
        print(f"   bounded but the bound is tight        : "
              f"{s['bounded_tight']:3d}  ({s['bounded_tight_pct']:.1f}%)  "
              f"already the lowest class, so the label stands")
        print(f"   bounded and the label may be wrong    : "
              f"{s['bounded_loose']:3d}  ({s['bounded_loose_pct']:.1f}%)  "
              f"{s['loose_recorded_classes']}")
        print(f"   deepest endpoint unreachable          : "
              f"{s['n_deep_endpoint_unreachable']:3d}  "
              f"({s['pct_deep_endpoint_unreachable']:.1f}%)")

    print("\n-- does observability differ between the groups a study would compare? --")
    print(pd.DataFrame(groups["15d"]).to_string(index=False,
                                                float_format=lambda v: f"{v:,.3g}"))
    print("\n   A tolerance comparison between these groups is in part a comparison")
    print("   of how well each group could be measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
