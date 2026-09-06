"""
Three things about the six-laboratory deposit that this paper had understated.

Run:  python -m src.experiments.exp24_trajectory_and_flag_audit

WHY THIS TEST EXISTS. A design review of a prediction pipeline built on the same
tidy extracts checked three properties of the ERA4TB deposit that no experiment
here had measured, and all three bear on claims this manuscript already makes.
They are checked here rather than accepted, and each is reported whether or not
it helps the argument.

ONE. HOW OFTEN DOES KILLING REVERSE? Section 3.4 says that seventeen of the
thirty-two flasks which fell below the limit were detectable again later. That
is true and it understates the picture. Measured over the most sensitive plating
volume, most treated series do not end on a decline at all, and most rebound more
than a log from their lowest point. This matters because the crossing-time
decomposition of Section 2.5 fits ONE slope across the window: on a trajectory
that falls and then regrows, that slope is an average over two regimes and not a
kill rate. The inversion count is unaffected, because it uses observed crossings
rather than the fitted slope, but the variance decomposition is a decomposition
of that averaged slope and the manuscript should say so.

TWO. ARE THE CENSORING FLAGS SELF-CONSISTENT? A sample is plated at four volumes
at the same visit. If the 2.5 uL drop is blank while the 100 uL quadruplicate of
the same sample returns a count above the 2.5 uL limit, the blank drop is not
evidence that the culture was below that limit; it is evidence that the drop
missed. Counting those cases measures how much of the deposit's censoring is a
property of the plating rather than of the culture, and it is the strongest
available argument for judging each reading against ITS OWN volume's limit rather
than pooling.

THREE. IS THE COX ADJUSTMENT SEPARATING TWO THINGS OR ONE? Section 3.4 reports
that adding starting density to a Cox model on laboratory removes the laboratory
effect for three of four institutes. If starting density is nearly a function of
laboratory, that adjustment is not separating two variables; it is replacing a
label with a number that carries the same information. The fraction of variance
in starting density explained by laboratory is computed here so the reader can
judge, rather than being left to assume the covariates are distinct.

Writes:
  results/tables/exp24_trajectory_shape.csv
  results/tables/exp24_flag_consistency.csv
  results/receipts/exp24_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

MOST_SENSITIVE_UL = 100.0        # limit 1.0 log10 CFU/mL
REBOUND_LOGS = 1.0               # what counts as a rebound rather than noise


def load() -> pd.DataFrame:
    d = pd.read_csv(DATA, encoding="latin-1")
    d["loq"] = np.log10(1000.0 / d["Volume"])
    d["y"] = pd.to_numeric(d["CFUlog10"], errors="coerce")
    return d


def trajectory_shape(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Does killing continue to the end of the window, or reverse?"""
    s = d[(d["Volume"] == MOST_SENSITIVE_UL) & (d["BQL"] != 1) & (d["AQL"] != 1)
          & (d["Time"] >= 0)].dropna(subset=["y"])
    rows = []
    for (inst, arm, rep), g in s.groupby(["Institute", "Sample", "Replicate"]):
        if arm == "untreated" or arm == "Inoculum TKA":
            continue
        g = g.sort_values("Time")
        if len(g) < 3:
            continue
        nadir = float(g["y"].min())
        last = float(g["y"].iloc[-1])
        rows.append({
            "institute": inst, "arm": arm, "replicate": int(rep),
            "n_points": int(len(g)),
            "start_log10": float(g["y"].iloc[0]),
            "nadir_log10": nadir,
            "final_log10": last,
            "terminal_step_log10": last - float(g["y"].iloc[-2]),
            "rebound_from_nadir_log10": last - nadir,
            "terminal_step_is_decline": bool(last < float(g["y"].iloc[-2])),
            "rebounds": bool(last - nadir > REBOUND_LOGS),
        })
    t = pd.DataFrame(rows)
    summ = {
        "n_treated_series": int(len(t)),
        "n_terminal_step_not_a_decline": int((~t["terminal_step_is_decline"]).sum()),
        "fraction_terminal_step_not_a_decline": float((~t["terminal_step_is_decline"]).mean()),
        "n_rebound_over_1_log": int(t["rebounds"].sum()),
        "fraction_rebound_over_1_log": float(t["rebounds"].mean()),
        "median_rebound_log10": float(t["rebound_from_nadir_log10"].median()),
        "max_rebound_log10": float(t["rebound_from_nadir_log10"].max()),
    }
    return t, summ


def flag_consistency(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Is a below-limit flag corroborated by the other platings of that sample?

    A flag is contradicted when another plating of the SAME flask at the SAME
    visit, whose own limit is at least as sensitive, returns a quantified count
    above the flagged reading's limit.
    """
    rows = []
    for (inst, arm, rep, t), g in d.groupby(["Institute", "Sample", "Replicate", "Time"]):
        flagged = g[g["BQL"] == 1]
        if flagged.empty or len(g) < 2:
            continue
        quant = g[(g["BQL"] != 1) & (g["AQL"] != 1)].dropna(subset=["y"])
        for _, r in flagged.iterrows():
            better = quant[quant["loq"] <= r["loq"]]
            contradicted = bool(len(better) and better["y"].max() > r["loq"])
            rows.append({
                "institute": inst, "arm": arm, "replicate": int(rep), "time": float(t),
                "flagged_volume_ul": float(r["Volume"]),
                "flagged_limit_log10": float(r["loq"]),
                "best_quantified_log10": float(better["y"].max()) if len(better) else np.nan,
                "contradicted": contradicted,
            })
    f = pd.DataFrame(rows)
    n_flags = int((d["BQL"] == 1).sum())
    summ = {
        "n_bql_flags_total": n_flags,
        "n_flags_checkable": int(len(f)),
        "n_contradicted": int(f["contradicted"].sum()) if len(f) else 0,
        "fraction_of_all_flags_contradicted":
            float(f["contradicted"].sum() / n_flags) if n_flags else np.nan,
        "by_volume": (f[f["contradicted"]]["flagged_volume_ul"].value_counts()
                      .to_dict() if len(f) else {}),
    }
    return f, summ


def collinearity(d: pd.DataFrame) -> dict:
    """How much of the starting density is just the laboratory?

    One-way analysis of variance on the flask-level starting density, reported
    as the fraction of variance between laboratories.
    """
    s = d[(d["Volume"] == MOST_SENSITIVE_UL) & (d["BQL"] != 1) & (d["AQL"] != 1)
          & (d["Time"] <= 1) & (d["Time"] >= 0)].dropna(subset=["y"])
    per_flask = (s.groupby(["Institute", "Sample", "Replicate"])["y"].mean()
                 .reset_index())
    grand = per_flask["y"].mean()
    ss_total = float(((per_flask["y"] - grand) ** 2).sum())
    ss_between = float(sum(
        len(g) * (g["y"].mean() - grand) ** 2
        for _, g in per_flask.groupby("Institute")))
    return {
        "n_flasks": int(len(per_flask)),
        "n_laboratories": int(per_flask["Institute"].nunique()),
        "variance_explained_by_laboratory": ss_between / ss_total if ss_total else np.nan,
        "between_lab_range_log10": float(
            per_flask.groupby("Institute")["y"].mean().max()
            - per_flask.groupby("Institute")["y"].mean().min()),
        "median_within_lab_sd_log10": float(
            per_flask.groupby("Institute")["y"].std().median()),
    }


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    d = load()

    traj, traj_s = trajectory_shape(d)
    flags, flag_s = flag_consistency(d)
    coll = collinearity(d)

    traj.to_csv(TABLES / "exp24_trajectory_shape.csv", index=False)
    flags.to_csv(TABLES / "exp24_flag_consistency.csv", index=False)

    (RECEIPTS / "exp24_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp24_trajectory_and_flag_audit.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "van Wijk et al. 2023, figshare 19766083",
        "most_sensitive_plated_volume_ul": MOST_SENSITIVE_UL,
        "rebound_threshold_log10": REBOUND_LOGS,
        "trajectory_shape": traj_s,
        "flag_consistency": flag_s,
        "starting_density_vs_laboratory": coll,
    }, indent=2, default=str), encoding="utf-8")

    print("-- does killing continue to the end of the window? --")
    print(f"   treated series with 3+ quantified points at 100 uL : "
          f"{traj_s['n_treated_series']}")
    print(f"   final step is NOT a decline                        : "
          f"{traj_s['n_terminal_step_not_a_decline']} "
          f"({100*traj_s['fraction_terminal_step_not_a_decline']:.0f}%)")
    print(f"   rebound more than {REBOUND_LOGS:.0f} log10 from the nadir       : "
          f"{traj_s['n_rebound_over_1_log']} "
          f"({100*traj_s['fraction_rebound_over_1_log']:.0f}%)")
    print(f"   median rebound                                     : "
          f"{traj_s['median_rebound_log10']:.2f} log10, "
          f"largest {traj_s['max_rebound_log10']:.2f}")

    print("\n-- are the below-limit flags corroborated by the other platings? --")
    print(f"   flags in the deposit                : {flag_s['n_bql_flags_total']}")
    print(f"   contradicted by a more sensitive")
    print(f"   plating of the same flask and visit : {flag_s['n_contradicted']} "
          f"({100*flag_s['fraction_of_all_flags_contradicted']:.1f}%)")
    print("   This is the argument for judging every reading against its own")
    print("   volume's limit: a blank 2.5 uL drop and a blank 100 uL quadruplicate")
    print("   are not the same event, and the deposit contains the proof.")

    print("\n-- is starting density separable from laboratory? --")
    print(f"   flasks {coll['n_flasks']}, laboratories {coll['n_laboratories']}")
    print(f"   variance in starting density explained by laboratory : "
          f"{100*coll['variance_explained_by_laboratory']:.1f}%")
    print(f"   between-laboratory range of means                    : "
          f"{coll['between_lab_range_log10']:.2f} log10")
    print(f"   median within-laboratory SD                          : "
          f"{coll['median_within_lab_sd_log10']:.2f} log10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
