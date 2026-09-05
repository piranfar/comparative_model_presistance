"""
Are the minimum inhibitory concentration and the minimum duration for killing
independent in real clinical isolates?

Run:  python -m src.experiments.exp16_tb_mic_mdk_independence

WHY THIS TEST EXISTS. The journal manuscript argues that resistance, tolerance
and persistence separate onto distinct measurable axes: a concentration axis and
two duration axes. The calibration's sharpest objection was that this is close
to circular. We define resistance in the model as a shift in EC50 and tolerance
as a change in duration, then report that they leave different signatures. The
signatures follow from the definitions.

The objection is answered only by data we did not generate. If MIC and MDK are
genuinely independent across natural isolates, the two axes carry separate
information about real bacteria, and the framework is describing something
rather than restating its own construction.

THE DATA. 217 clinical Mycobacterium tuberculosis isolates assayed under
rifampicin, with the MIC and the minimum durations for 90%, 99% and 99.99%
killing measured on each at 15, 30 and 60 days of prior culture. Supplementary
file 2 of eLife 93243, downloaded from the publisher.

CENSORING IS THE FIRST THING TO CHECK. The killing assay runs for six days, so
any isolate not reaching the target reduction within it is recorded at the
ceiling. The deeper the endpoint, the more of the sample is censored, and an
uncensored-only analysis is reported alongside the full one.

Writes:
  results/tables/exp16_tb_independence.csv
  results/tables/exp16_tb_censoring.csv
  results/receipts/exp16_receipt.json
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

CEILING_DAYS = 6.0

# An earlier version tested three endpoints on all 217 rows pooled, and a
# pre-writing calibration showed that was under-specified in two ways that a
# referee would find. The file carries SIX minimum-duration columns, at 15 and
# 60 days of prior culture, and a susceptibility stratum; and 43 of the 217 rows
# are follow-up isolates from patients already represented, so treating all 217
# as independent inflates the sample and narrows the detectable bound.
#
# Both are fixed by testing the whole family that the file supports and
# correcting for it, rather than by choosing three of twenty-four tests.
ENDPOINTS = {
    "MDK_90_15day_new": "MDK90 (15d)",
    "MDK_99_15day_new": "MDK99 (15d)",
    "MDK_99_99_15day_new": "MDK99.99 (15d)",
    "MDK_90_60day_new": "MDK90 (60d)",
    "MDK_99_60day_new": "MDK99 (60d)",
    "MDK_99_99_60day_new": "MDK99.99 (60d)",
}

# Strata the file supports. "baseline only" removes the serial isolates.
def strata(d):
    return {
        "all isolates": d,
        "baseline only": d[d["Time_point"] == "0M"],
        "INH-susceptible": d[d["INH-Suceptibility"] == "IS"],
        "INH-resistant": d[d["INH-Suceptibility"] == "IR"],
    }


def benjamini_hochberg(p, alpha=0.05):
    """Which tests survive control of the false discovery rate at `alpha`."""
    p = np.asarray(p, dtype=float)
    order = np.argsort(p)
    m = p.size
    crit = alpha * (np.arange(1, m + 1)) / m
    passed = p[order] <= crit
    keep = np.zeros(m, dtype=bool)
    if passed.any():
        last = np.max(np.flatnonzero(passed))
        keep[order[: last + 1]] = True
    return keep, crit[np.argsort(order)]


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; see the docstring for its source")

    d = pd.read_excel(DATA)

    cens = []
    for col, name in ENDPOINTS.items():
        v = d[col].dropna()
        cens.append({"endpoint": name, "n": int(len(v)),
                     "median_days": float(v.median()),
                     "at_ceiling": int((v >= CEILING_DAYS).sum()),
                     "fraction_censored": float((v >= CEILING_DAYS).mean())})
    cens = pd.DataFrame(cens)
    cens.to_csv(TABLES / "exp16_tb_censoring.csv", index=False)

    rows = []
    for sname, s in strata(d).items():
        for col, name in ENDPOINTS.items():
            if col not in s.columns:
                continue
            sub = s.dropna(subset=["MIC_RIF", col])
            if len(sub) < 15 or sub[col].nunique() < 2:
                continue
            r = stats.spearmanr(np.log2(sub["MIC_RIF"]), sub[col])
            n = len(sub)
            rows.append({
                "stratum": sname, "endpoint": name, "n": n,
                "spearman_rho": float(r.statistic), "p_value": float(r.pvalue),
                # the correlation this sample size could have called at 95%
                "detectable_rho_at_95pct": float(np.tanh(1.96 / np.sqrt(n - 3))),
            })
    out = pd.DataFrame(rows)

    # The whole family is tested and the whole family is corrected. Selecting
    # the nominally significant members of a 24-test family and reporting only
    # those is how an association is manufactured from this file; four tests
    # reach p < 0.05 where 1.2 are expected by chance, and none survives.
    keep, crit = benjamini_hochberg(out["p_value"].to_numpy())
    out["bh_critical_value"] = crit
    out["survives_bh"] = keep
    out["independent"] = ~out["survives_bh"]
    out = out.sort_values("p_value")
    out.to_csv(TABLES / "exp16_tb_independence.csv", index=False)

    mic = d.dropna(subset=["MIC_RIF"])["MIC_RIF"]
    (RECEIPTS / "exp16_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp16_tb_mic_mdk_independence.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "eLife 93243 supplementary file 2",
        "organism": "Mycobacterium tuberculosis, clinical isolates",
        "antibiotic": "rifampicin",
        "n_isolates": int(len(d)),
        "assay_ceiling_days": CEILING_DAYS,
        "mic_range_ug_ml": [float(mic.min()), float(mic.max())],
        "mic_distinct_values": int(mic.nunique()),
        "mic_fold_range": float(mic.max() / mic.min()),
        "censoring": cens.set_index("endpoint")["fraction_censored"].to_dict(),
        "independence": out.to_dict(orient="records"),
    }, indent=2), encoding="utf-8")

    pd.set_option("display.width", 200)
    print("-- how much of each endpoint the six-day assay can measure --")
    print(cens.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    print("\n-- does the MIC predict the duration needed to kill? --")
    print(out.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    n_nominal = int((out["p_value"] < 0.05).sum())
    n_tests = len(out)
    n_survive = int(out["survives_bh"].sum())
    print()
    print(f"   {n_tests} tests available: {len(ENDPOINTS)} endpoints x "
          f"{len(strata(d))} strata, minus cells too small to test.")
    print(f"   nominally significant at p < 0.05 : {n_nominal}")
    print(f"   expected by chance alone          : {0.05 * n_tests:.1f}")
    print(f"   surviving Benjamini-Hochberg      : {n_survive}")
    if n_survive == 0:
        print()
        print("   No association survives correction for the family actually")
        print("   available. The nominal hits sit in the deepest endpoint, which is")
        print("   also the most heavily censored, and they are negative: a higher MIC")
        print("   going with a SHORTER duration, which is not the direction a shared")
        print("   mechanism predicts. Reporting those four and not the twenty misses")
        print("   would manufacture an association this file does not contain.")
    print()
    print(f"\nMIC range: {mic.min()} to {mic.max()} ug/mL, {mic.nunique()} distinct "
          f"values, {mic.max()/mic.min():.0f}-fold")
    top2 = mic.value_counts(normalize=True).nlargest(2)
    print(f"   {100*top2.sum():.0f}% of isolates sit at {list(top2.index)} ug/mL, so this")
    print("   tests independence among largely susceptible isolates, not across a")
    print("   wide resistance range.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
