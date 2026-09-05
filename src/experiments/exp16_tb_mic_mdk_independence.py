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
ENDPOINTS = {
    "MDK_90_15day_new": "MDK90",
    "MDK_99_15day_new": "MDK99",
    "MDK_99_99_15day_new": "MDK99.99",
}


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
    for col, name in ENDPOINTS.items():
        s = d.dropna(subset=["MIC_RIF", col])
        for label, sub in [("all", s), ("uncensored", s[s[col] < CEILING_DAYS])]:
            if len(sub) < 10 or sub[col].nunique() < 2:
                continue
            r = stats.spearmanr(np.log2(sub["MIC_RIF"]), sub[col])
            n = len(sub)
            # the correlation the design could have detected at 95%
            bound = float(np.tanh(1.96 / np.sqrt(n - 3)))
            rows.append({
                "endpoint": name, "sample": label, "n": n,
                "spearman_rho": float(r.statistic), "p_value": float(r.pvalue),
                "detectable_rho_at_95pct": bound,
                "independent": bool(r.pvalue >= 0.05 and abs(r.statistic) < bound),
            })
    out = pd.DataFrame(rows)
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

    print(f"\nMIC range: {mic.min()} to {mic.max()} ug/mL, {mic.nunique()} distinct "
          f"values, {mic.max()/mic.min():.0f}-fold")
    top2 = mic.value_counts(normalize=True).nlargest(2)
    print(f"   {100*top2.sum():.0f}% of isolates sit at {list(top2.index)} ug/mL, so this")
    print("   tests independence among largely susceptible isolates, not across a")
    print("   wide resistance range.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
