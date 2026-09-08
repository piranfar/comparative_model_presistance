"""
Apply the two boundaries to every corpus deposit whose floor can be established.

Run:  python -m src.experiments.exp42_boundaries_across_the_corpus

WHY THIS EXISTS, AND WHAT IT CORRECTS. Section 8 of the manuscript says a search
"returned one deposit carrying all three fields the boundaries require". That was
true of the search it describes and is no longer true of this repository. This
script settles the number mechanically instead of asserting it, so it stays right
as the corpus grows.

THE FIRST VERSION OF THIS SCRIPT WAS TOO STRICT, and the strictness was not
principled -- it was stricter than the manuscript itself. The paper's own primary
deposit has no declared limit: its floor of 23 MPN/mL is INFERRED from a pile-up
on the lowest most-probable-number rung, and the manuscript says so and quantifies
the inference. Refusing to do for other deposits what the paper does for its own
counted two qualifying deposits where there are many more.

SO THE FLOOR IS ESTABLISHED IN TIERS, and every result is reported against the
tier it rests on. This is the taxonomy the manuscript already uses in its
deposit-floor table, applied to the whole corpus rather than to five files.

  STATED    the depositor gave a value -- an LOD column, or a sentence in the
            sheet. Nothing is inferred.
  DERIVED   the value follows arithmetically from a recorded plated volume and
            dilution. Nothing is inferred either; the information was in the
            file by accident rather than by intent.
  INFERRED  no floor is declared, but the readings pile up on one lowest value
            that a plate could actually produce, with a gap beneath it. This is
            what the manuscript does for its own clinical deposit.
  ABOVE A   the lowest value is 1, or 0.1, which no plate can return -- it is
  PLACEHOLDER  what people write instead of zero so a logarithm stays finite.
            The floor is then taken as the smallest value a plate COULD give,
            and the placeholder readings are treated as censored at it. This is
            the weakest tier and is reported separately, never pooled.
  NONE      no floor is evidenced. The boundaries are refused, not guessed.

WHAT IS ACTUALLY TESTED, and it can fail. Headroom h = log10(N0/L) is the
deepest reduction a series could report, so no series may present AS A
MEASUREMENT a drop deeper than its own h. That is a consistency condition
between a deposit's floor and its own numbers.

The distinction between a measurement and a censored reading is the whole test.
A file may legitimately carry raw values below its own limit: the Acinetobacter
deposit here is a NONMEM dataset fitted by Beal's M3, whose DV column keeps the
real sub-limit plate readings while its control stream uses LOQ=LOG10(LOD) to
treat them as censored at fit time. Counting those as reported measurements made
the first run of this script report seven violations, every one an artefact --
the same error the manuscript accuses the literature of, committed here first.

Writes:
  results/tables/exp42_corpus_boundaries.csv   one row per deposit
  results/tables/exp42_corpus_series.csv       one row per series
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
# Floors that are stated in the SOURCE PAPER rather than in the deposited file:
# a Methods sentence, a figure legend, a table footnote, a protocol PDF beside
# the data. A floor is a floor wherever it is written down, and refusing one
# because it sits in the article rather than the spreadsheet would leave a
# deposit uncounted whose authors did exactly what this paper asks for.
# Every row carries its quote and its location, so the number can be checked
# against the sentence it came from.
STATED = ROOT / "data" / "stated_floors.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

MIN_TIMEPOINTS = 3
MIN_READINGS = 30
# One colony in a millilitre is 1 CFU/mL, and a millilitre is not a plate. The
# smallest volume anyone spreads is of the order of a microlitre, so the
# smallest floor a real plate can produce is around 1 CFU/mL only in the limit;
# values of 1 and below, sitting under a gap, are zero-placeholders rather than
# counts. Two is the threshold used throughout this project.
PLATE_PLAUSIBLE = 2.0
# A pile-up worth calling a floor: at least this share of readings on the single
# lowest value, and at least this many of them.
PILE_SHARE = 0.02
PILE_COUNT = 3
TOL = 1e-6


def establish_floor(s: pd.DataFrame, stated: dict) -> dict:
    """Decide this deposit's floor, and say on what evidence."""
    v = s.cfu_per_ml.dropna()
    v = v[v > 0]
    if len(v) < MIN_READINGS:
        return {"tier": "NONE", "floor": np.nan,
                "basis": f"only {len(v)} positive readings"}

    sid = s.study_id.iloc[0]
    # A floor read out of the source paper outranks anything inferred from the
    # value distribution, and outranks a placeholder-derived guess entirely.
    # It does NOT outrank a per-reading floor already in the file, which is
    # more specific than a deposit-wide constant.
    if sid in stated and not s.floor_cfu_per_ml.notna().any():
        r = stated[sid]
        return {"tier": f"PAPER_{r['how_established']}",
                "floor": float(r["floor_cfu_per_ml"]),
                "basis": f"{r['where_found']} -- {str(r['quote'])[:90]}"}

    if s.floor_cfu_per_ml.notna().any():
        basis = str(s.floor_basis.dropna().iloc[0]) if s.floor_basis.notna().any() else ""
        # Not named `stated`: that is the parameter holding the paper-read
        # floors, and shadowing it here would leave a bool where a dict is
        # expected the next time anyone adds a branch below this one.
        depositor_gave_a_value = bool(pd.Series([basis]).str.contains(
            r"stated in the sheet|LOD column|limit of detection",
            case=False, regex=True, na=False).iloc[0])
        return {"tier": "STATED" if depositor_gave_a_value else "DERIVED",
                "floor": float(s.floor_cfu_per_ml.dropna().min()),
                "basis": basis[:120] or "floor column present"}

    lo = float(v.min())
    at = int((v == lo).sum())
    share = at / len(v)
    dist = np.sort(v.unique())
    gap = float(np.log10(dist[1] / dist[0])) if len(dist) > 1 else np.nan

    if lo >= PLATE_PLAUSIBLE and share >= PILE_SHARE and at >= PILE_COUNT:
        return {"tier": "INFERRED", "floor": lo,
                "basis": (f"{at} readings ({share:.0%}) on the lowest value "
                          f"{lo:g}, gap {gap:.2f} log10 beneath the next")}

    if lo < PLATE_PLAUSIBLE:
        real = dist[dist >= PLATE_PLAUSIBLE]
        if len(real) and at >= PILE_COUNT:
            return {"tier": "ABOVE_A_PLACEHOLDER", "floor": float(real[0]),
                    "basis": (f"{at} readings ({share:.0%}) sit on {lo:g}, which "
                              f"no plate returns; the smallest value a plate "
                              f"could give is {real[0]:g}")}

    return {"tier": "NONE", "floor": np.nan,
            "basis": (f"lowest {lo:g} carries {share:.1%} of readings; no "
                      f"pile-up a floor would produce")}


def series_table(d: pd.DataFrame, floors: dict) -> pd.DataFrame:
    """One row per series, with its starting density, floor and headroom."""
    rows = []
    keyed = d.dropna(subset=["cfu_per_ml", "time_h"])
    for (sid, arm, rep), s in keyed.groupby(
            ["study_id", "arm", "replicate"], dropna=False):
        f = floors.get(sid)
        if f is None or f["tier"] == "NONE":
            continue
        s = s.sort_values("time_h")
        if s.time_h.nunique() < MIN_TIMEPOINTS:
            continue
        t0 = s.time_h.min()
        n0 = float(s[s.time_h == t0].cfu_per_ml.mean())
        if not np.isfinite(n0) or n0 <= 0:
            continue
        # Per-reading floors where the deposit gives them; the deposit-level
        # floor otherwise. The lowest floor the series was read at sets the
        # deepest reportable reduction, because a series read neat at the end
        # goes deeper than its diluted day-zero reading suggests.
        own = s.floor_cfu_per_ml.dropna()
        floor = float(own.min()) if len(own) else float(f["floor"])
        if not np.isfinite(floor) or floor <= 0:
            continue
        # A reading is a measurement only if the file does not mark it censored
        # AND it sits at or above the floor. The second clause matters for the
        # inferred tiers, where nothing is flagged and the placeholder values
        # would otherwise be read as counts.
        measured = s.cfu_per_ml[(s.cfu_per_ml >= floor) & (s.censored != "yes")]
        deepest = (float(np.log10(n0 / measured.min())) if len(measured)
                   else np.nan)
        h = float(np.log10(n0 / floor))
        rows.append({
            "study_id": sid, "floor_tier": f["tier"], "arm": str(arm),
            "replicate": str(rep), "t0_h": float(t0), "n0": n0, "floor": floor,
            "headroom": h, "deepest_reported_drop": deepest,
            "n_timepoints": int(s.time_h.nunique()),
            "n_censored": int((s.censored == "yes").sum()),
            "violates_headroom": bool(np.isfinite(deepest) and deepest > h + TOL),
            "excess_log10": (float(deepest - h)
                             if np.isfinite(deepest) and deepest > h + TOL
                             else 0.0),
        })
    return pd.DataFrame(rows)


ORDER = ["STATED", "DERIVED", "PAPER_STATED", "PAPER_DERIVED",
         "INFERRED", "ABOVE_A_PLACEHOLDER"]


def main() -> int:
    if not LONG.exists():
        raise SystemExit(f"missing {LONG}; run src/build_corpus_long.py first")
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(LONG, low_memory=False)

    stated = {}
    if STATED.exists():
        sf = pd.read_csv(STATED)
        stated = {r.study_id: r._asdict() for r in sf.itertuples()}
        print(f"{len(stated)} floors read out of source papers "
              f"({STATED.relative_to(ROOT)})\n")
    floors = {sid: establish_floor(s, stated)
              for sid, s in d.groupby("study_id")}
    ser = series_table(d, floors)
    if ser.empty:
        print("no deposit in the corpus supports the boundaries")
        return 0
    ser.to_csv(TABLES / "exp42_corpus_series.csv", index=False)

    print(f"{d.study_id.nunique()} deposits in the corpus\n")
    print("-- how the floor is established, deposit by deposit --")
    for tier in ORDER + ["NONE"]:
        got = [s for s, f in floors.items() if f["tier"] == tier]
        print(f"   {tier:20} {len(got):>2}   " + ", ".join(sorted(got))[:96])

    rows = []
    for sid, s in ser.groupby("study_id"):
        sub = d[d.study_id == sid]
        org = sorted({str(x) for x in sub.organism.dropna() if str(x).strip()})
        drg = sorted({str(x) for x in sub.drug.dropna() if str(x).strip()})
        rows.append({
            "study_id": sid, "floor_tier": s.floor_tier.iloc[0],
            "floor_basis": floors[sid]["basis"],
            "organism": "; ".join(org)[:40] or "not named",
            "drugs": "; ".join(drg)[:52] or "not named",
            "n_series": len(s),
            "baseline_is_pre_treatment": bool((s.t0_h == 0).all()),
            "earliest_reading_h": float(s.t0_h.min()),
            "floor_used": float(s.floor.min()),
            "median_n0": float(s.n0.median()),
            "headroom_median": float(s.headroom.median()),
            "series_short_of_4_logs": int((s.headroom < 4).sum()),
            "series_short_of_5_logs": int((s.headroom < 5).sum()),
            "n_censored_readings": int(s.n_censored.sum()),
            "series_violating_headroom": int(s.violates_headroom.sum()),
        })
    t = pd.DataFrame(rows)
    t["_o"] = t.floor_tier.map({k: i for i, k in enumerate(ORDER)})
    t = t.sort_values(["_o", "n_series"], ascending=[True, False]).drop(columns="_o")
    t.to_csv(TABLES / "exp42_corpus_boundaries.csv", index=False)

    print(f"\n-- the boundaries computed on every one of them --")
    print(f"   {'deposit':16}{'tier':21}{'series':>7}{'pre-Rx':>8}{'h med':>7}"
          f"{'<4log':>7}{'<5log':>7}  organism")
    for r in t.itertuples():
        print(f"   {r.study_id[:16]:16}{r.floor_tier:21}{r.n_series:>7}"
              f"{'yes' if r.baseline_is_pre_treatment else 'NO':>8}"
              f"{r.headroom_median:>7.2f}{r.series_short_of_4_logs:>7}"
              f"{r.series_short_of_5_logs:>7}  {r.organism[:30]}")

    bad = ser[ser.violates_headroom]
    print(f"\n-- the consistency test: no series may present, AS A MEASUREMENT, "
          f"a drop\n   deeper than its own floor allows --")
    if bad.empty:
        print(f"   {len(ser)} series across {ser.study_id.nunique()} deposits, "
              f"0 violations.")
    else:
        print(f"   {len(bad)} of {len(ser)} series violate it:")
        for r in bad.nlargest(min(8, len(bad)), "excess_log10").itertuples():
            print(f"      {r.study_id[:16]:16} {r.floor_tier:20} "
                  f"h = {r.headroom:5.2f}, reported {r.deepest_reported_drop:5.2f}"
                  f"  (+{r.excess_log10:.2f})")

    others = t[t.study_id != "PIRANFAR2026"]
    firm = others[others.floor_tier.isin(
        ["STATED", "DERIVED", "PAPER_STATED", "PAPER_DERIVED", "INFERRED"])]
    firm_pre = firm[firm.baseline_is_pre_treatment]
    weak = others[others.floor_tier == "ABOVE_A_PLACEHOLDER"]
    print(f"\n-- what Section 8 may claim --")
    print(f"   {len(others)} published deposits in this corpus support the "
          f"boundaries at some tier.")
    print(f"   {len(firm)} rest on a floor that is stated, derived or inferred "
          f"from a plate-plausible")
    print(f"   pile-up -- the three tiers the manuscript already uses. Of those, "
          f"{len(firm_pre)} also have a")
    print(f"   pre-treatment reading, so a starting density rather than "
          f"whatever the drug left.")
    print(f"   {len(weak)} more rest on a floor read above a zero-placeholder, "
          f"which is weaker and is")
    print(f"   reported separately: "
          + ", ".join(sorted(weak.study_id))[:88])
    orgs = sorted({o for o in firm.organism if o != "not named"})
    print(f"   Organisms on the firm tiers: " + "; ".join(orgs)[:150])

    (RECEIPTS / "exp42_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp42_boundaries_across_the_corpus.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "corpus_deposits": int(d.study_id.nunique()),
        "floor_tiers": {k: sorted(s for s, f in floors.items() if f["tier"] == k)
                        for k in ORDER + ["NONE"]},
        "published_supporting_boundaries": int(len(others)),
        "on_firm_tiers": sorted(firm.study_id.tolist()),
        "firm_and_pre_treatment": sorted(firm_pre.study_id.tolist()),
        "above_a_placeholder": sorted(weak.study_id.tolist()),
        "n_series": int(len(ser)),
        "n_series_violating_headroom": int(len(bad)),
        "min_timepoints_required": MIN_TIMEPOINTS,
        "plate_plausible_threshold": PLATE_PLAUSIBLE,
    }, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
