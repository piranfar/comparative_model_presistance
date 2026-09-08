"""
Apply the two boundaries to every corpus deposit that carries the three fields.

Run:  python -m src.experiments.exp42_boundaries_across_the_corpus

WHY THIS EXISTS, AND WHAT IT CORRECTS. Section 8 of the manuscript says a search
"returned one deposit carrying all three fields the boundaries require". That was
true of the search it describes. It is no longer true of this repository: the
corpus assembled afterwards contains more, and a claim that the project's own
data contradicts cannot go into a submitted paper. This script settles the
number mechanically instead of asserting it, so it stays right as the corpus
grows.

THE THREE FIELDS, tested against the FILE and not against the paper's prose:
  1. a MEASURED starting density -- a count at the earliest timepoint of a
     series, never a nominal inoculum from a Methods section
  2. a floor with a VALUE, stated by the depositor or derived from a recorded
     plated volume; a below-limit flag with no number fixes nothing
  3. quantified counts at three or more timepoints

WHAT IS ACTUALLY TESTED, and it can fail. Headroom h = log10(N0/L) is the
deepest reduction a series could report. So no series may report a drop deeper
than its own h. That is not a prediction about biology -- it is a consistency
condition between a deposit's declared detection limit and its own numbers, and
a deposit that breaks it is telling us its stated floor is not the floor it
worked at. Every violation is printed with the series that produced it rather
than summarised away, because a violation is the most informative thing this
script can find.

Writes:
  results/tables/exp42_corpus_boundaries.csv        one row per deposit
  results/tables/exp42_corpus_series.csv            one row per series
  results/receipts/exp42_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
LONG = ROOT / "data" / "processed" / "corpus_long.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

MIN_TIMEPOINTS = 3
# Floating-point slack on a comparison of two logarithms. A drop that exceeds
# its headroom by less than this is rounding, not a refutation.
TOL = 1e-6


def series_table(d: pd.DataFrame) -> pd.DataFrame:
    """One row per series, with its starting density, floor and headroom."""
    rows = []
    keyed = d.dropna(subset=["cfu_per_ml", "time_h"])
    for (sid, arm, rep), s in keyed.groupby(
            ["study_id", "arm", "replicate"], dropna=False):
        s = s.sort_values("time_h")
        if s.time_h.nunique() < MIN_TIMEPOINTS:
            continue
        t0 = s.time_h.min()
        # A reading taken an hour into ampicillin is not a starting density, and
        # a headroom computed from one is not headroom -- it is whatever was
        # left after the drug had already been working. Two corpus deposits
        # (Kollerova, earliest reading at 1.00 h; Alexander, at 0.12 h) have no
        # pre-treatment reading at all, and including them put two deposits with
        # median headroom near one log into a table whose other members sit
        # above five. They are measured and reported, but flagged, and the
        # headline count uses the strict criterion the manuscript states.
        base = s[s.time_h == t0]
        n0 = float(base.cfu_per_ml.mean())
        if not np.isfinite(n0) or n0 <= 0:
            continue
        floors = s.floor_cfu_per_ml.dropna()
        if floors.empty:
            continue
        # The lowest floor the series was read at is the one that sets the
        # deepest reportable reduction, exactly as in the prospective
        # experiment: a series read neat at the end can go deeper than its own
        # heavily diluted day-zero reading suggests.
        floor = float(floors.min())
        if not np.isfinite(floor) or floor <= 0:
            continue
        # UNCENSORED readings only, and this distinction is the whole test.
        #
        # A file may legitimately carry raw values below its own declared limit.
        # The Acinetobacter deposit here is a NONMEM dataset fitted by Beal's M3
        # method: its DV column keeps the actual sub-limit plate readings while
        # model.txt uses LOQ=LOG10(LOD) to treat them as "known only to be below
        # the limit" at fit time. That is correct practice, not a contradiction.
        # Counting those readings as reported measurements made this script
        # report seven violations on its first run, every one of them an
        # artefact of the test rather than a fault in the deposit -- exactly the
        # error the manuscript accuses others of, committed here first.
        #
        # So the question is narrowed to the one that can actually indict a
        # deposit: does it present, AS A MEASUREMENT, a value its own floor says
        # it could not have measured?
        measured = s.cfu_per_ml[(s.cfu_per_ml > 0) & (s.censored != "yes")]
        deepest = (float(np.log10(n0 / measured.min())) if len(measured)
                   else np.nan)
        h = float(np.log10(n0 / floor))
        rows.append({
            "study_id": sid, "arm": str(arm), "replicate": str(rep),
            "t0_h": float(t0), "n0": n0, "floor": floor, "headroom": h,
            "deepest_reported_drop": deepest,
            "n_timepoints": int(s.time_h.nunique()),
            "n_censored": int((s.censored == "yes").sum()),
            "violates_headroom": bool(np.isfinite(deepest) and deepest > h + TOL),
            "excess_log10": (float(deepest - h)
                             if np.isfinite(deepest) and deepest > h + TOL
                             else 0.0),
        })
    return pd.DataFrame(rows)


def main() -> int:
    if not LONG.exists():
        raise SystemExit(f"missing {LONG}; run src/build_corpus_long.py first")
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(LONG, low_memory=False)

    ser = series_table(d)
    if ser.empty:
        print("no deposit in the corpus carries all three fields")
        return 0
    ser.to_csv(TABLES / "exp42_corpus_series.csv", index=False)

    print(f"{d.study_id.nunique()} deposits in the corpus; "
          f"{ser.study_id.nunique()} carry a measured starting density, a floor "
          f"with a value,\nand three or more timepoints -- so the boundaries can "
          f"be computed on them.\n")

    rows = []
    for sid, s in ser.groupby("study_id"):
        org = sorted({str(x) for x in d[d.study_id == sid].organism.dropna()
                      if str(x).strip()})
        drg = sorted({str(x) for x in d[d.study_id == sid].drug.dropna()
                      if str(x).strip()})
        basis = d[d.study_id == sid].floor_basis.dropna()
        stated = bool(basis.str.contains(
            r"stated in the sheet|LOD column|limit of detection",
            case=False, regex=True, na=False).any())
        rows.append({
            "study_id": sid,
            "organism": "; ".join(org)[:44] or "not named",
            "drugs": "; ".join(drg)[:60] or "not named",
            "n_series": len(s),
            "baseline_is_pre_treatment": bool((s.t0_h == 0).all()),
            "earliest_reading_h": float(s.t0_h.min()),
            "floor_declared_by_depositor": stated,
            "floors_used": ", ".join(f"{v:g}" for v in
                                     sorted(s.floor.unique())[:5]),
            "median_n0": float(s.n0.median()),
            "headroom_min": float(s.headroom.min()),
            "headroom_median": float(s.headroom.median()),
            "headroom_max": float(s.headroom.max()),
            "series_short_of_4_logs": int((s.headroom < 4).sum()),
            "series_short_of_5_logs": int((s.headroom < 5).sum()),
            "n_censored_readings": int(s.n_censored.sum()),
            "series_violating_headroom": int(s.violates_headroom.sum()),
            "worst_excess_log10": float(s.excess_log10.max()),
        })
    t = pd.DataFrame(rows).sort_values("n_series", ascending=False)
    t.to_csv(TABLES / "exp42_corpus_boundaries.csv", index=False)

    print(f"   {'deposit':16}{'series':>7}{'floor':>9}{'h med':>7}"
          f"{'<4log':>7}{'<5log':>7}{'viol':>6}  organism")
    for r in t.itertuples():
        print(f"   {r.study_id[:16]:16}{r.n_series:>7}"
              f"{'stated' if r.floor_declared_by_depositor else 'derived':>9}"
              f"{r.headroom_median:>7.2f}{r.series_short_of_4_logs:>7}"
              f"{r.series_short_of_5_logs:>7}"
              f"{r.series_violating_headroom:>6}  {r.organism[:34]}")

    # ---- the part that can fail ---------------------------------------
    bad = ser[ser.violates_headroom]
    print(f"\n-- the consistency test: no series may present, AS A MEASUREMENT, "
          f"a drop deeper\n   than its own declared floor allows --")
    if bad.empty:
        print(f"   {len(ser)} series across {ser.study_id.nunique()} deposits, "
              f"0 violations.")
        print(f"   Every declared floor is consistent with every number the "
              f"deposit reports beside it.")
    else:
        print(f"   {len(bad)} of {len(ser)} series REPORT A DROP DEEPER THAN "
              f"THEIR FLOOR ALLOWS.")
        print(f"   That is a deposit contradicting its own stated detection "
              f"limit, and it is worth\n   more than a confirmation. The worst "
              f"are:")
        for r in bad.nlargest(min(8, len(bad)), "excess_log10").itertuples():
            print(f"      {r.study_id[:16]:16} {str(r.arm)[:20]:20} "
                  f"{str(r.replicate)[:14]:14} h = {r.headroom:5.2f}, "
                  f"reported {r.deepest_reported_drop:5.2f}  "
                  f"(+{r.excess_log10:.2f})")

    # ---- what this means for the manuscript's count --------------------
    others = t[t.study_id != "PIRANFAR2026"]
    strict = others[others.baseline_is_pre_treatment]
    loose = others[~others.baseline_is_pre_treatment]
    print(f"\n-- what Section 8 may claim --")
    print(f"   {len(strict)} PUBLISHED deposits carry all three fields on the "
          f"STRICT test: a count taken\n   BEFORE the drug, a floor with a "
          f"value, and three or more timepoints.")
    for r in strict.itertuples():
        how = ("declared by the depositor" if r.floor_declared_by_depositor
               else "derived from a recorded volume")
        print(f"      {r.study_id:14} {r.organism[:28]:28} floor {how}, "
              f"{r.n_series} series")
    if len(loose):
        print(f"   {len(loose)} more carry a floor and counts but NO "
              f"pre-treatment reading, so they have")
        print(f"   no starting density and no headroom: "
              + ", ".join(f"{r.study_id} (earliest {r.earliest_reading_h:g} h)"
                          for r in loose.itertuples()))
    print(f"   Organisms on the strict test: "
          + "; ".join(sorted({o for o in strict.organism if o != 'not named'})))

    (RECEIPTS / "exp42_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp42_boundaries_across_the_corpus.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "corpus_deposits": int(d.study_id.nunique()),
        "deposits_with_all_three_fields": int(ser.study_id.nunique()),
        "published_deposits_with_all_three_strict": int(len(strict)),
        "strict_study_ids": strict.study_id.tolist(),
        "no_pre_treatment_reading": loose.study_id.tolist(),
        "qualifying_study_ids": sorted(ser.study_id.unique().tolist()),
        "min_timepoints_required": MIN_TIMEPOINTS,
        "n_series": int(len(ser)),
        "n_series_violating_headroom": int(len(bad)),
        "violations": bad[["study_id", "arm", "replicate", "headroom",
                           "deepest_reported_drop", "excess_log10"]]
                      .to_dict("records") if len(bad) else [],
    }, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
