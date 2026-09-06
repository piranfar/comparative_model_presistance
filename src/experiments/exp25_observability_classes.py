"""
How much of a published tolerance classification rests on a measured fraction?

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

An earlier version of this experiment stopped there and concluded that an isolate
recorded in the lowest class keeps its label, since a class cannot be bounded
below its own floor. That conceded too much, and the concession was wrong in our
own disfavour. Whether the recorded label survives the bound is not the question.
The question is whether the measurement could ever have returned a different one.

Sweeping the true count across the entire range the floor admits, zero to L,
gives the set of classes compatible with the observation. Where that set has one
member, the published rule has no other label available and the reading adds
nothing to what the starting density and the floor already imply.

Say exactly what that does and does not mean, because an earlier version of this
file overstated it. It does NOT mean the phenotype was settled before the drug
was added. Whether a culture reaches the floor at all depends on the drug: the
population has to fall by the isolate's entire headroom for the reading to be
censored, and the starting density does not by itself decide that. What the
starting density settles is narrower and still consequential: GIVEN a censored
reading, it fixes which classes remain compatible with it.

So a tolerance call falls into one of three classes:

  MEASURED                     the day-5 reading is above the floor; the
                               surviving fraction is observed and the label is a
                               measurement of it
  SINGLE COMPATIBLE CLASS      the reading is censored at the floor and only one
                               class is compatible with it; the label follows
                               from N0 and the floor, not from the reading
  MULTIPLE COMPATIBLE CLASSES  the reading is censored and more than one class
                               is compatible; the rule cannot choose

Counting them says how much of a published classification rests on an observed
fraction and how much on the censoring rule, which is a different and more useful
number than counting how many isolates hit the floor. It says nothing about how
much drug effect each isolate experienced; the true count below the floor is
unknown, and two isolates with the same censored reading may have fallen by
quite different amounts.

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
# The deposited thresholds on the recorded surviving fraction, recovered in
# exp22 by showing the classes do not overlap on it.
CLASS_CUTS = (1e-3, 1e-2)


def _class_of(fraction: float) -> str:
    """Which tolerance class the deposited thresholds assign to a fraction."""
    lo, hi = CLASS_CUTS
    return "Low" if fraction < lo else ("Medium" if fraction <= hi else "High")

LOWEST_CLASS = "Low"


def classify(d: pd.DataFrame, age: int) -> pd.DataFrame:
    n0 = d[f"mpn_T0_{age}days"].astype(float)
    n5 = d[f"mpn_T5_{age}days"].astype(float)
    lab = d[f"Tolerant_level_D5_{age}"]
    usable = n0.notna() & n5.notna() & lab.isin(CLASS_ORDER)

    at_floor = n5 <= MPN_FLOOR
    lowest = lab == LOWEST_CLASS

    # An earlier version of this experiment called a floored reading in the
    # lowest class "bounded, tight" and let its label stand, on the argument
    # that the class cannot be bounded below its own floor. That conceded too
    # much. The right question is not whether the recorded label survives the
    # bound, but which labels the rule could have returned given a censored
    # reading. Sweep the true count across the whole range the floor admits, 0
    # to L, and see which classes stay compatible. Where only one does, the
    # label follows from N0 and the floor rather than from the reading. This is
    # conditional on the reading being censored; it is not a claim that the
    # starting density decided whether the culture reached the floor.
    reachable_low = np.array([_class_of(0.0)] * len(n0))          # count 0
    reachable_high = np.array([_class_of(MPN_FLOOR / v) if v > 0 else None
                               for v in n0])                       # count at L
    single = at_floor & (reachable_low == reachable_high)
    klass = np.where(~at_floor, "measured",
                     np.where(single, "single compatible class",
                              "multiple compatible classes"))

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
    for k in ("measured", "single compatible class",
              "multiple compatible classes"):
        m = int((c["observability"] == k).sum())
        out[k.replace(", ", "_").replace(" ", "_")] = m
        out[k.replace(", ", "_").replace(" ", "_") + "_pct"] = 100 * m / n if n else np.nan
    loose = c[c["observability"] == "multiple compatible classes"]
    out["multiple_compatible_classes_recorded"] = (
        loose["recorded_class"].value_counts().to_dict())
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
            "pct_measured": 100 * (sub["observability"] == "measured").mean(),
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
        print(f"\n-- {age}-day panel: what each tolerance call rests on "
              f"(n={s['n_calls']}) --")
        print(f"   measured, reading above the floor     : "
              f"{s['measured']:3d}  ({s['measured_pct']:.1f}%)")
        print(f"   censored, one compatible class        : "
              f"{s['single_compatible_class']:3d}  "
              f"({s['single_compatible_class_pct']:.1f}%)  "
              f"the rule has no other label available")
        print(f"   censored, several compatible classes  : "
              f"{s['multiple_compatible_classes']:3d}  "
              f"({s['multiple_compatible_classes_pct']:.1f}%)  "
              f"{s['multiple_compatible_classes_recorded']}")
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
