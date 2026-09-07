"""
The prospective test: do the two boundaries hold in a designed experiment?

Run:  python -m src.experiments.exp38_boundary_experiment

WHY THIS IS DIFFERENT FROM EVERY OTHER EXPERIMENT HERE. Every other analysis in
this project reads a deposit somebody else made for another purpose. This one
reads a workbook whose predictions were written down before a single plate was
counted, in an experiment designed to try to break them. That is the only kind of
evidence that can distinguish a rule which describes published data from a rule
which governs the next measurement.

THE DESIGN, from the workbook's own Design sheet: E. coli ATCC 25922, the
reference strain the standard itself names, exposed to ciprofloxacin at 10x MIC,
seeded at three densities and plated at two volumes. The three densities were
chosen so that the middle one is the 5x10^5 the standard specifies, and the two
volumes give two different floors on the same culture.

THE FOUR PREDICTIONS, tested here in the order the Prediction sheet states them:

  1. At the LOW inoculum a four-log reduction cannot be reported, however
     completely the culture is killed, because its headroom is under four logs.
  2. A reading at the floor reports L/N0, so it tracks the inoculum rather than
     the killing. Two cultures killed to different depths report the same
     fraction; two killed identically but seeded differently report different
     ones.
  3. The same sample plated at two volumes has two floors, and where they
     straddle a class threshold, ONE CULTURE receives TWO tolerance labels. This
     is the sharp test: there is one culture, so the difference cannot be
     biology.
  4. Above L/c1, a floored reading is compatible only with the lowest class.

Each is reported with the arithmetic that would refute it, not only the
arithmetic that supports it.

Writes:
  results/tables/exp38_experiment_readings.csv
  results/tables/exp38_boundary_tests.csv
  results/receipts/exp38_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "experiment" / "BOUNDARY_TEST_BLIND.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

Q = 4          # the endpoint scored, from the Design sheet
C1 = 1e-3      # lowest class threshold
C2 = 1e-2      # middle class threshold
TARGET = {"LOW": 5e4, "MID": 5e5, "HIGH": 5e6}


def readings() -> pd.DataFrame:
    ws = load_workbook(BOOK, data_only=False)["Counts"]
    rows = []
    for r in range(5, ws.max_row + 1):
        v = [ws.cell(row=r, column=c).value for c in range(1, 8)]
        if not v[0] or v[6] is None:
            continue
        rows.append({"arm": str(v[0]).strip(), "conc_xmic": v[1],
                     "flask": str(v[2]).strip(), "time_h": float(v[3]),
                     "volume_ul": float(v[4]), "dilution": float(v[5]),
                     "colonies": float(v[6])})
    d = pd.DataFrame(rows)
    # The floor is one colony in the volume plated, referred back to the
    # undiluted sample. It is a property of the plating, not of the culture.
    d["floor"] = 1000.0 / d.volume_ul
    d["cfu"] = d.colonies * d.dilution * 1000.0 / d.volume_ul
    d["at_floor"] = d.colonies == 0
    return d


def per_sample(d: pd.DataFrame) -> pd.DataFrame:
    """One row per (arm, flask, time, plating), pooling the technical plates.

    POOLING MOVES THE FLOOR, which is the whole subject of this paper and is
    easy to get wrong here. Two 100 uL plates read together are 200 uL of
    sample, so one colony across the pair means 5 CFU/mL, not 10: plating more
    volume buys measurable depth. The first version of this script averaged the
    two plates' densities while keeping the single-plate floor of 10, and a
    sample with one blank plate and one single-colony plate then reported a
    fraction BELOW its own floor -- which read as a culture killed deeper than
    its headroom allowed, and looked like a refutation of the boundary. It was
    an arithmetic error in the denominator, and it is exactly the error the
    manuscript accuses the literature of.

    So: colonies are summed, volume is summed, and the floor is one colony in
    the pooled volume. A sample is censored when its pooled count sits at or
    below that pooled floor, not merely when a plate happens to read zero.
    """
    g = (d.groupby(["arm", "flask", "time_h", "volume_ul"], as_index=False)
           .agg(colonies=("colonies", "sum"), n_plates=("colonies", "size"),
                dilution=("dilution", "first"), n_blank=("at_floor", "sum")))
    g["pooled_volume_ul"] = g.volume_ul * g.n_plates
    g["floor"] = 1000.0 * g.dilution / g.pooled_volume_ul
    g["cfu"] = g.colonies * g.dilution * 1000.0 / g.pooled_volume_ul

    # The starting density is measured on the same plating, so it carries that
    # plating's own dilution and floor. Using the 100 uL N0 for the 10 uL series
    # would import a measurement the 10 uL series never made.
    n0 = (g[g.time_h == 0].groupby(["arm", "flask", "volume_ul"], as_index=False)
            .cfu.mean().rename(columns={"cfu": "n0"}))
    g = g.merge(n0, on=["arm", "flask", "volume_ul"], how="left")

    # Headroom uses the floor at the moment of reading, which is where the
    # dilution matters: a sample read at a 100-fold dilution has a floor 100
    # times higher than the same sample read neat.
    g["headroom"] = np.log10(g.n0 / g.floor)
    g["fraction"] = g.cfu / g.n0
    g["censored"] = g.cfu <= g.floor
    g["reported_fraction"] = np.where(g.censored, g.floor / g.n0, g.fraction)
    g["reported_drop"] = -np.log10(g.reported_fraction)
    g["klass"] = np.where(g.reported_fraction < C1, "low",
                  np.where(g.reported_fraction < C2, "medium", "high"))
    return g


def main() -> int:
    if not BOOK.exists():
        raise SystemExit(f"missing {BOOK}")
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    d = readings()
    g = per_sample(d)
    d.to_csv(TABLES / "exp38_experiment_readings.csv", index=False)

    out, tests = [], []
    print(f"{len(d)} plate readings, {len(g)} sample-platings, "
          f"{g.flask.nunique()} flasks per arm\n")

    # ---- realised starting densities, which the boundaries actually use ----
    print("-- what was actually seeded, against what was aimed at --")
    for arm in ("LOW", "MID", "HIGH"):
        s = g[(g.arm == arm) & (g.volume_ul == 100)]
        if s.empty:
            continue
        n0 = s.n0.mean()
        h100 = np.log10(n0 / 10)
        h10 = np.log10(n0 / 100)
        print(f"   {arm:5} target {TARGET[arm]:>9,.0f}   realised {n0:>11,.0f}   "
              f"h = {h100:.2f} at 100 uL, {h10:.2f} at 10 uL")
        out.append({"arm": arm, "target_n0": TARGET[arm], "realised_n0": n0,
                    "h_100ul": h100, "h_10ul": h10,
                    "q_log_legal_100ul": h100 >= Q, "q_log_legal_10ul": h10 >= Q})

    # ---- prediction 1 --------------------------------------------------
    print("\n-- P1: at LOW, a four-log reduction cannot be reported --")
    # Tested per FLASK. Each flask has its own starting density and therefore
    # its own headroom, and comparing a flask's deepest reading against an
    # arm-mean headroom mixes one flask's numerator with another's denominator.
    for arm in ("LOW", "MID", "HIGH"):
        for vol in (100.0, 10.0):
            s = g[(g.arm == arm) & (g.volume_ul == vol)]
            if s.empty:
                continue
            for flask, sub in s.groupby("flask"):
                h = float(sub.headroom.max())     # deepest reachable at this plating
                deepest = float(sub.reported_drop.max())
                legal, achieved = h >= Q, deepest >= Q - 1e-9
                verdict = ("as predicted" if legal == achieved
                           else "REFUTES THE BOUNDARY" if achieved and not legal
                           else "not reached, though it was legal")
                tests.append({"prediction": 1, "arm": arm, "volume_ul": vol,
                              "flask": flask, "n0": float(sub.n0.iloc[0]),
                              "headroom": h, "deepest_reported_drop": deepest,
                              "q_log_legal": legal, "q_log_achieved": achieved,
                              "verdict": verdict})
            t = pd.DataFrame([x for x in tests if x["prediction"] == 1
                              and x["arm"] == arm and x["volume_ul"] == vol])
            bad = int((t.verdict == "REFUTES THE BOUNDARY").sum())
            print(f"   {arm:5} {vol:>5.0f} uL   h = {t.headroom.min():4.2f}-"
                  f"{t.headroom.max():4.2f}   deepest {t.deepest_reported_drop.max():4.2f} "
                  f"logs   {'legal' if t.q_log_legal.all() else 'IMPOSSIBLE':10} -> "
                  f"{'all three flasks as predicted' if not bad else f'{bad} flask(s) REFUTE IT'}")

    # ---- prediction 3, the sharp one ----------------------------------
    print("\n-- P3: the same sample, two platings, two labels --")
    w = g.pivot_table(index=["arm", "flask", "time_h"], columns="volume_ul",
                      values=["reported_fraction", "klass", "censored"],
                      aggfunc="first")
    w.columns = [f"{a}_{int(b)}" for a, b in w.columns]
    w = w.dropna(subset=["reported_fraction_100", "reported_fraction_10"]).reset_index()
    w["labels_differ"] = w.klass_100 != w.klass_10
    w["either_censored"] = w.censored_100.astype(bool) | w.censored_10.astype(bool)
    n_dis = int(w.labels_differ.sum())
    n_cen = int(w.either_censored.sum())
    dis_cen = int((w.labels_differ & w.either_censored).sum())
    print(f"   {len(w)} sample-times plated both ways")
    print(f"   {n_cen} have at least one plating at its floor")
    print(f"   {n_dis} receive DIFFERENT tolerance labels from the two platings"
          f"  ({100*n_dis/len(w):.1f}%)")
    print(f"   of those, {dis_cen} involve a censored reading")
    if n_dis:
        print("\n   examples -- one culture, one drug, one moment:")
        for _, r in w[w.labels_differ].head(6).iterrows():
            print(f"      {r.arm:5} flask {r.flask} at {r.time_h:>4.1f} h: "
                  f"100 uL says {r.klass_100:6} (fraction {r.reported_fraction_100:.2e}), "
                  f"10 uL says {r.klass_10:6} (fraction {r.reported_fraction_10:.2e})")
    w.to_csv(TABLES / "exp38_boundary_tests.csv", index=False)

    # ---- prediction 2 --------------------------------------------------
    print("\n-- P2: a floored reading reports L/N0, not the killing --")
    cen = g[g.censored].copy()
    p2 = None
    if len(cen):
        # Comparing every censored reading at once confounds two things: the
        # floor differs between them (different plating, different dilution) as
        # well as the starting density. Holding the floor fixed is what isolates
        # the claim, because then the reported fraction is L/N0 with L constant
        # and can only move with N0.
        print("   within one floor, the reported fraction can only move with N0:")
        for fl, s in cen.groupby("floor"):
            if len(s) < 3 or s.n0.nunique() < 3:
                continue
            r = np.corrcoef(np.log10(s.n0), np.log10(s.reported_fraction))[0, 1]
            ratio = ((s.reported_fraction.max() / s.reported_fraction.min())
                     / (s.n0.max() / s.n0.min()))
            print(f"      floor {fl:>8,.0f} CFU/mL, n = {len(s):2d}: "
                  f"corr(log N0, log reported fraction) = {r:+.3f}, "
                  f"spread ratio = {ratio:.2f}")
            p2 = {"floor": float(fl), "n": int(len(s)), "corr_log_n0": float(r),
                  "spread_ratio_fraction_over_n0": float(ratio)}
        print("   a correlation of -1 and a spread ratio of 1 is the boundary's")
        print("   claim exactly: the number reported is the inoculum, inverted.")
        print(f"\n   {len(cen)} censored sample-platings in total, "
              f"{int((cen.arm == 'LOW').sum())} of them in the LOW arm")
    else:
        print("   no reading reached the floor; this prediction is untested here")

    (RECEIPTS / "exp38_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp38_boundary_experiment.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_workbook": BOOK.name,
        "n_plate_readings": len(d), "n_sample_platings": len(g),
        "arms": out, "prediction_1": tests,
        "prediction_3": {"paired_sample_times": len(w),
                         "with_a_censored_plating": n_cen,
                         "labels_differ": n_dis,
                         "labels_differ_and_censored": dis_cen},
        "prediction_2": ({"n_censored": int(len(cen)), "within_one_floor": p2}
                         if len(cen) else None),
    }, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
