"""
Is the mediation a tautology? Refit it with the floored isolates removed.

Run:  python -m src.experiments.exp41_mediation_without_floor

THE OBJECTION, WHICH IS FAIR. Peer review put it plainly: the mediator is the
denominator of the outcome. For an isolate whose day-5 reading sits at the assay
floor the recorded fraction is L/N0 exactly, so the tolerance class is a function
of the starting density and nothing else, and decomposing the resistance effect
into a path "through" N0 recovers an arithmetic relation rather than a biological
one. That criticism cannot be answered by conceding it in the Discussion, which
is what the manuscript currently does.

IT CAN BE ANSWERED WITH A NUMBER. The tautology holds only where the reading is
censored. Eighteen of the 203 isolates with an ordered label ended at the floor;
for the other 185 the recorded fraction has a numerator that was actually
measured and can vary independently of N0. So refit the mediation on those 185
alone. If the mediated path survives, the effect is not an artefact of the
censored subset. If it collapses, the reviewer is right and the analysis has to
go.

That is a real test with a real way to fail, which is what the objection deserves.

Writes:
  results/tables/exp41_mediation_without_floor.csv
  results/receipts/exp41_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TB = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

LEVELS = {"Low": 0, "Medium": 1, "High": 2}
FLOOR = 23.0          # MPN per mL, the lowest rung of the three-tube table
N_BOOT = 5000
SEED = 20260907


def load() -> pd.DataFrame:
    d = pd.read_excel(TB)
    out = pd.DataFrame({
        "label": d["Tolerant_level_D5_15"],
        "n0": pd.to_numeric(d["mpn_T0_15days"], errors="coerce"),
        "n5": pd.to_numeric(d["mpn_T5_15days"], errors="coerce"),
        "inh": d["INH-Suceptibility"],
        "timepoint": d["Time_point"],
    })
    out = out[out.label.isin(LEVELS) & out.n0.notna() & out.n5.notna()
              & out.inh.isin(["IS", "IR"])].copy()
    out["y"] = out.label.map(LEVELS).astype(float)
    out["x"] = (out.inh == "IR").astype(float)
    out["m"] = np.log10(out.n0)
    # A reading at the floor is where the recorded fraction becomes L/N0 and the
    # class stops being a measurement of the surviving population.
    out["at_floor"] = out.n5 <= FLOOR
    return out


def mediate(d: pd.DataFrame, rng) -> dict:
    """Product of coefficients, with a percentile bootstrap."""
    def once(s):
        a = np.polyfit(s.x, s.m, 1)[0]                       # x -> m
        X = np.column_stack([np.ones(len(s)), s.x, s.m])
        b_full, *_ = np.linalg.lstsq(X, s.y, rcond=None)
        c_total = np.polyfit(s.x, s.y, 1)[0]
        return a * b_full[2], b_full[1], c_total             # ACME, ADE, total

    acme, ade, tot = once(d)
    boots = np.empty((N_BOOT, 3))
    idx = np.arange(len(d))
    for i in range(N_BOOT):
        s = d.iloc[rng.choice(idx, len(d), replace=True)]
        try:
            boots[i] = once(s)
        except Exception:
            boots[i] = np.nan
    boots = boots[~np.isnan(boots).any(axis=1)]
    lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    return {"n": int(len(d)), "acme": float(acme), "acme_lo": float(lo[0]),
            "acme_hi": float(hi[0]), "ade": float(ade), "ade_lo": float(lo[1]),
            "ade_hi": float(hi[1]), "total": float(tot),
            "prop_mediated": float(acme / tot) if tot else np.nan,
            "n_boot_used": int(len(boots))}


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    d = load()
    rng = np.random.default_rng(SEED)

    n_floor = int(d.at_floor.sum())
    print(f"{len(d)} isolates with an ordered label and both readings")
    print(f"   {n_floor} ended at or below the floor of {FLOOR:g} MPN/mL")
    print(f"   {len(d) - n_floor} did not, and for those the recorded fraction has")
    print(f"      a numerator that was measured rather than imposed\n")

    rows = []
    for name, sub in (("all isolates with an ordered label", d),
                      ("floored isolates only", d[d.at_floor]),
                      ("FLOORED ISOLATES REMOVED", d[~d.at_floor])):
        if len(sub) < 20:
            print(f"   {name}: n = {len(sub)}, too few to bootstrap")
            continue
        r = mediate(sub, np.random.default_rng(SEED))
        r["stratum"] = name
        rows.append(r)
        star = " <-- the reviewer's test" if name.startswith("FLOORED") else ""
        print(f"   {name:36} n = {r['n']:3d}")
        print(f"      mediated  {r['acme']:+.3f}  ({r['acme_lo']:+.3f}, "
              f"{r['acme_hi']:+.3f}){star}")
        print(f"      direct    {r['ade']:+.3f}  ({r['ade_lo']:+.3f}, "
              f"{r['ade_hi']:+.3f})")
        print(f"      total     {r['total']:+.3f}   proportion mediated "
              f"{r['prop_mediated']:.2f}")

    t = pd.DataFrame(rows)
    t.to_csv(TABLES / "exp41_mediation_without_floor.csv", index=False)

    off = t[t.stratum.str.startswith("FLOORED")]
    verdict = "not established"
    if len(off):
        r = off.iloc[0]
        survives = (r.acme_lo > 0) == (r.acme > 0) and r.acme_lo * r.acme_hi > 0
        verdict = ("the mediated path survives with the censored isolates removed, "
                   "so it is not an artefact of the subset where the class is "
                   "arithmetic" if survives else
                   "the mediated path does not survive once the censored isolates "
                   "are removed, and the objection stands")
        print(f"\n   VERDICT: {verdict}")

    (RECEIPTS / "exp41_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp41_mediation_without_floor.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "objection": ("peer review: the mediator is the denominator of the "
                      "outcome, so the mediation is a tautology"),
        "floor_mpn_per_ml": FLOOR, "n_total": int(len(d)), "n_floored": n_floor,
        "n_boot": N_BOOT, "seed": SEED,
        "strata": rows, "verdict": verdict,
    }, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
