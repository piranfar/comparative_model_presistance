"""
Every denominator in the paper, traced to the exclusion that produced it.

Run:  python -m src.experiments.exp37_analysis_flow

WHY THIS TEST EXISTS. Peer review counted the analysis sets in circulation and
found them irreconcilable from the text alone: 217, 210, 203, 202, 197, 196 for
the clinical deposit; 174, 168, 167, 162, 161 for its baseline stratum; 90, 72,
67, 42, 360, 288, 261 for the six-laboratory deposit. Each is correct for the
analysis that produced it, and the manuscript never said which was which. A
reader cannot check an n against a claim if the n has no derivation.

This builds the derivation, per deposit, as a table of successive exclusions with
a reason and a count on every line. Every denominator that appears anywhere in
the manuscript must be findable in it.

It also fulfils a promise the Methods already make and the analysis had not kept:
that the dropped rows are compared with the retained ones on starting density and
susceptibility, so a reader can see whether an exclusion is plausibly ignorable.

Writes:
  results/tables/exp37_analysis_flow.csv
  results/tables/exp37_dropped_vs_retained.csv
  results/receipts/exp37_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
TB = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
ERA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

LEVELS = ("Low", "Medium", "High")


def clinical_flow(d: pd.DataFrame) -> list[dict]:
    rows = []

    def step(panel, stratum, label, keep, prev):
        n = int(keep.sum())
        rows.append({"deposit": "Vijay clinical", "panel": panel,
                     "stratum": stratum, "stage": label, "n": n,
                     "excluded_here": (prev - n) if prev is not None else 0,
                     "appears_in_manuscript_as": ""})
        return n

    for age in (15, 60):
        lab = d[f"Tolerant_level_D5_{age}"]
        n0 = pd.to_numeric(d[f"mpn_T0_{age}days"], errors="coerce")
        n5 = pd.to_numeric(d[f"mpn_T5_{age}days"], errors="coerce")
        growth = pd.to_numeric(d["Time_to_0.4"], errors="coerce")
        sus = d["INH-Suceptibility"]
        for stratum, base in (("all isolates", pd.Series(True, index=d.index)),
                              ("baseline only (0M)", d["Time_point"] == "0M")):
            p = f"{age}-day"
            prev = step(p, stratum, "rows in the deposit", base, None)
            k = base & lab.notna()
            prev = step(p, stratum, "tolerance label present", k, prev)
            k = k & lab.isin(LEVELS)
            prev = step(p, stratum, "label is Low, Medium or High (drops 'MDR')", k, prev)
            k = k & n0.notna() & n5.notna()
            prev = step(p, stratum, "starting and day-5 readings present", k, prev)
            k = k & sus.isin(["IS", "IR"])
            prev = step(p, stratum, "susceptibility is IS or IR", k, prev)
            k = k & growth.notna()
            step(p, stratum, "growth proxy present (association family)", k, prev)
    return rows


def era_flow() -> list[dict]:
    e = pd.read_csv(ERA, encoding="latin-1")
    s = pd.read_csv(TABLES / "exp17_survival.csv")
    r = pd.read_csv(TABLES / "exp32_recrossing.csv")
    k = pd.read_csv(TABLES / "exp17_kill_rates.csv")
    inv = pd.read_csv(TABLES / "exp23_inversions.csv")
    nf = lambda df: df.groupby(["Institute", "Sample", "Replicate"]).ngroups
    no_inoc = e[e.Sample != "Inoculum TKA"]
    treated = no_inoc[no_inoc.Sample != "untreated"]
    out = [
        ("readings in the file", len(e), 0),
        ("excluding inoculum controls", len(no_inoc), len(e) - len(no_inoc)),
        ("flasks (institute x arm x replicate)", nf(no_inoc), 0),
        ("treated flasks", nf(treated), nf(no_inoc) - nf(treated)),
        ("treated flasks with a usable starting density",
         int(s[s.arm != "untreated"].start_log10.notna().sum()),
         nf(treated) - int(s[s.arm != "untreated"].start_log10.notna().sum())),
        ("laboratory-by-arm cells", len(k), 0),
        ("cells with a fitted kill rate", int(k.kill_rate_tobit.notna().sum()),
         len(k) - int(k.kill_rate_tobit.notna().sum())),
        ("series under the plating key (flasks x 4 platings)", len(r), 0),
        ("treated series", int((r.arm != "untreated").sum()),
         len(r) - int((r.arm != "untreated").sum())),
        ("cross-laboratory pairs in the same arm", len(inv), 0),
    ]
    return [{"deposit": "ERA4TB six-laboratory", "panel": "-", "stratum": "-",
             "stage": a, "n": b, "excluded_here": c,
             "appears_in_manuscript_as": ""} for a, b, c in out]


def dropped_vs_retained(d: pd.DataFrame) -> pd.DataFrame:
    """The comparison the Methods promise: are the exclusions plausibly ignorable?"""
    rows = []
    for age in (15, 60):
        lab = d[f"Tolerant_level_D5_{age}"]
        n0 = np.log10(pd.to_numeric(d[f"mpn_T0_{age}days"], errors="coerce"))
        growth = pd.to_numeric(d["Time_to_0.4"], errors="coerce")
        sus = d["INH-Suceptibility"]
        keep = lab.isin(LEVELS) & sus.isin(["IS", "IR"]) & growth.notna()
        for name, drop in (("label missing or 'MDR'", ~lab.isin(LEVELS)),
                           ("growth proxy missing", lab.isin(LEVELS) & growth.isna())):
            if not drop.any():
                continue
            a, b = n0[keep].dropna(), n0[drop].dropna()
            p_n0 = stats.mannwhitneyu(a, b).pvalue if len(b) else np.nan
            kr = int((sus[keep] == "IR").sum()); kn = int(keep.sum())
            dr = int((sus[drop] == "IR").sum()); dn = int(drop.sum())
            p_r = stats.fisher_exact([[kr, kn - kr], [dr, dn - dr]])[1] if dn else np.nan
            rows.append({
                "panel": f"{age}-day", "exclusion": name,
                "n_dropped": dn, "n_retained": kn,
                "median_start_log10_retained": float(a.median()),
                "median_start_log10_dropped": float(b.median()) if len(b) else np.nan,
                "start_density_mannwhitney_p": float(p_n0) if len(b) else np.nan,
                "pct_resistant_retained": 100 * kr / kn if kn else np.nan,
                "pct_resistant_dropped": 100 * dr / dn if dn else np.nan,
                "resistance_fisher_p": float(p_r) if dn else np.nan,
            })
    return pd.DataFrame(rows)


def main() -> int:
    d = pd.read_excel(TB)
    flow = pd.DataFrame(clinical_flow(d) + era_flow())
    flow.to_csv(TABLES / "exp37_analysis_flow.csv", index=False)

    dvr = dropped_vs_retained(d)
    dvr.to_csv(TABLES / "exp37_dropped_vs_retained.csv", index=False)

    denominators = sorted({int(n) for n in flow.n})
    (RECEIPTS / "exp37_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp37_analysis_flow.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "distinct_denominators": denominators,
        "clinical": flow[flow.deposit == "Vijay clinical"].to_dict("records"),
        "era4tb": flow[flow.deposit != "Vijay clinical"].to_dict("records"),
        "dropped_vs_retained": dvr.to_dict("records"),
    }, indent=2, default=str), encoding="utf-8")

    print("\n-- clinical deposit --")
    print(flow[flow.deposit == "Vijay clinical"]
          [["panel", "stratum", "stage", "n", "excluded_here"]].to_string(index=False))
    print("\n-- six-laboratory deposit --")
    print(flow[flow.deposit != "Vijay clinical"][["stage", "n", "excluded_here"]]
          .to_string(index=False))
    print("\n-- are the exclusions plausibly ignorable? --")
    print(dvr.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
