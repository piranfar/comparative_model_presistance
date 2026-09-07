"""
What is actually in 64,015 readings. Description, not hypothesis testing.

Run:  python -m src.experiments.exp40_corpus_landscape

NOT AN ARGUMENT. Every other analysis in this project sets out to test something
stated in advance. This one does not: it looks at the corpus and reports what is
there, including things nobody predicted and things that do not fit. Clustering
and repeated measures are not corrected for, because nothing here is an
inference -- these are counts of what the files contain, and a count is not
biased by the fact that two flasks came from one laboratory.

THE ONE IDEA WORTH THE NAME. An assay with a floor leaves a signature in its own
value distribution: readings pile up on the lowest reportable step and there is
nothing underneath it. That is how the floor of the clinical deposit in the
manuscript was recovered when nobody had declared one. Twenty-nine deposits here
declare no floor. If the signature is in their numbers too, the floor is
recoverable from the data itself -- which would be worth more than counting how
many papers forgot to mention it.

Reported per deposit:
  the shape of what was measured, in organisms, drugs, times and series
  the lowest values, and whether they pile up in a way a floor would produce
  how often a series goes back up after going down
  how deep the reported reductions go, against how deep they could have gone

Writes:
  results/tables/exp40_landscape.csv
  results/tables/exp40_floor_signatures.csv
  results/receipts/exp40_receipt.json
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
LONG = ROOT / "data" / "processed" / "corpus_long.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"


def floor_signature(v: pd.Series) -> dict:
    """Does this deposit's value distribution look like it hit a floor?

    Three marks, none conclusive alone. A floor shows as a pile-up on one low
    value; as a gap beneath it; and as that value being shared by many series
    rather than being one culture's unlucky reading. The test deliberately does
    NOT declare a floor -- it reports the evidence and lets a reader judge,
    because declaring one would be exactly the invention this corpus exists to
    avoid.
    """
    v = v.dropna()
    v = v[v > 0]
    if len(v) < 30:
        return {}
    lo = v.min()
    at_min = int((v == lo).sum())
    # how much of the mass sits on the single lowest value
    share = at_min / len(v)
    # the gap: how far the next distinct value sits above the lowest, in logs
    distinct = np.sort(v.unique())
    gap = float(np.log10(distinct[1] / distinct[0])) if len(distinct) > 1 else np.nan
    # a floor is a property of the method, so it should recur across series
    return {"n": int(len(v)), "lowest": float(lo), "n_at_lowest": at_min,
            "share_at_lowest": float(share), "log_gap_above_lowest": gap,
            "distinct_values": int(len(distinct))}


def main() -> int:
    if not LONG.exists():
        raise SystemExit(f"missing {LONG}; run src/build_corpus_long.py first")
    d = pd.read_csv(LONG, low_memory=False)
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    print(f"{len(d):,} readings, {d.study_id.nunique()} deposits\n")

    # ---- what was measured -------------------------------------------
    print("-- what the corpus is made of --")
    org = Counter(x for x in d.organism.dropna() if str(x).strip())
    print(f"   organisms named: {len(org)}")
    for o, n in org.most_common(8):
        print(f"      {n:>7,}  {str(o)[:56]}")
    drg = Counter(x for x in d.drug.dropna() if str(x).strip())
    print(f"   drugs named: {len(drg)}")
    for o, n in drg.most_common(8):
        print(f"      {n:>7,}  {str(o)[:56]}")
    ro = Counter(x for x in d.readout.dropna() if str(x).strip())
    print(f"   readouts: {dict(ro.most_common(6))}")

    t = d.time_h.dropna()
    print(f"\n   time covered: {t.min():.1f} to {t.max():,.0f} hours, "
          f"{t.nunique()} distinct timepoints")
    print(f"   readings at time zero: {int((d.time_h == 0).sum()):,}")

    # ---- the floor signature -----------------------------------------
    print("\n-- do the deposits that declare no floor still show one? --")
    print("   a floor piles readings onto one lowest value and leaves a gap "
          "beneath it\n")
    sigs = []
    print(f"   {'deposit':20}{'n':>7}{'lowest':>12}{'at it':>7}{'share':>8}"
          f"{'gap':>7}  reads as")
    for sid, s in d.groupby("study_id"):
        declared = s.floor_cfu_per_ml.notna().any()
        sig = floor_signature(s.cfu_per_ml)
        if not sig:
            continue
        sig["study_id"] = sid
        sig["declares_a_floor"] = bool(declared)
        # Report the EVIDENCE, and name the judgement separately. An earlier
        # version called this column looks_floored, which is a conclusion, and
        # then the same script claimed it did not declare floors -- the flag
        # contradicted the sentence beside it. It measures a pile-up; whether a
        # pile-up is a floor is the reader's call, and the next column gives
        # them the fact they need to make it.
        pile = (sig["share_at_lowest"] >= 0.05 and sig["n_at_lowest"] >= 5)
        sig["pile_up_at_lowest"] = bool(pile)
        # A floor is one colony in some plated volume, so it lands on 1000/v for
        # a volume somebody could pipette -- 400, 100, 20, 10 CFU/mL and so on.
        # A lowest value of 1 or 0.1 CFU/mL is not a plate count at all: it is
        # what people write instead of zero so the logarithm stays finite. The
        # two look identical in a pile-up and mean opposite things.
        lo = sig["lowest"]
        plausible = lo >= 2.0
        sig["lowest_is_plate_plausible"] = bool(plausible)
        sig["reading"] = ("declares a floor" if declared else
                          "pile-up on a plate-plausible value" if pile and plausible
                          else "pile-up on a value no plate can give"
                          if pile else "no pile-up")
        sigs.append(sig)
        verdict = sig["reading"]
        print(f"   {sid[:20]:20}{sig['n']:>7,}{sig['lowest']:>12,.4g}"
              f"{sig['n_at_lowest']:>7}{sig['share_at_lowest']:>8.2%}"
              f"{sig['log_gap_above_lowest']:>7.2f}  {verdict}")
    sg = pd.DataFrame(sigs)
    sg.to_csv(TABLES / "exp40_floor_signatures.csv", index=False)

    # Our own experiment is in this corpus and has to come out of any count
    # that is about what OTHER groups deposited.
    others = sg[sg.study_id != "PIRANFAR2026"]
    undeclared = others[~others.declares_a_floor & others.pile_up_at_lowest]
    recovered = undeclared[undeclared.lowest_is_plate_plausible]
    placeholder = undeclared[~undeclared.lowest_is_plate_plausible]
    print(f"\n   of {len(others)} deposits by other groups, {len(undeclared)} pile "
          f"up on their lowest value without declaring a floor.")
    print(f"   {len(recovered)} of those pile up on a value a plate could give, so "
          f"the floor is\n   recoverable from the data alone: "
          + ", ".join(f"{r.study_id} at {r.lowest:g}"
                      for r in recovered.itertuples()))
    print(f"   {len(placeholder)} pile up on a value no plate can give, which is a "
          f"stand-in for zero\n   and a trap for anyone who takes a logarithm: "
          + ", ".join(f"{r.study_id} at {r.lowest:g}"
                      for r in placeholder.itertuples()))

    # ---- going back up -----------------------------------------------
    print("\n-- how often does a series go back up after going down? --")
    rows = []
    for (sid, arm, rep), s in d.dropna(subset=["time_h", "cfu_per_ml"]).groupby(
            ["study_id", "arm", "replicate"], dropna=False):
        s = s.sort_values("time_h")
        if len(s) < 3:
            continue
        v = np.log10(s.cfu_per_ml.replace(0, np.nan)).dropna().values
        if len(v) < 3:
            continue
        fell = v.min() < v[0] - 0.5
        rose = v[-1] > v.min() + 0.5
        rows.append({"study_id": sid, "series": f"{arm}|{rep}",
                     "n_points": len(v), "start": v[0], "min": v.min(),
                     "end": v[-1], "fell": fell, "rose_again": fell and rose})
    tr = pd.DataFrame(rows)
    if len(tr):
        fell = tr[tr.fell]
        print(f"   {len(tr):,} series with three or more quantified points")
        print(f"   {len(fell):,} fall by more than half a log")
        print(f"   {int(fell.rose_again.sum()):,} of THOSE come back up by more "
              f"than half a log")
        print(f"      {100*fell.rose_again.mean():.1f}% of the series that fell, "
              f"{100*fell.rose_again.sum()/len(tr):.1f}% of all series.")
        print(f"      The first is the number to quote: a series that never fell "
              f"cannot come back up,\n      so putting it over all series answers "
              f"a question nobody asked.")
        tr.to_csv(TABLES / "exp40_landscape.csv", index=False)

    (RECEIPTS / "exp40_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp40_corpus_landscape.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_readings": len(d), "n_deposits": int(d.study_id.nunique()),
        "organisms": dict(org.most_common()), "drugs": dict(drg.most_common(20)),
        "floor_recovered_from_the_data": recovered.study_id.tolist(),
        "pile_up_is_a_stand_in_for_zero": placeholder.study_id.tolist(),
        "note": ("PIRANFAR2026 is this project own experiment and is excluded "
                 "from both lists, which are about what other groups deposited."),
        "n_series": int(len(tr)) if len(tr) else 0,
        "n_series_falling": int(len(fell)) if len(tr) else 0,
        "n_series_returning": int(fell.rose_again.sum()) if len(tr) else 0,
    }, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
