"""
Extract the Vijay 2024 clinical-isolate deposit (eLife 93243, supplementary file 2)
into the project's common tidy schema.

Source : data/raw/tb/elife93243_supp2.xlsx, sheet "raw data", 217 rows x 48 cols.
Content: 217 clinical M. tuberculosis isolates exposed to rifampicin, MPN/mL read at
         T0, T2 and T5 (days) for three culture ages (15, 30, 60 days).

UNITS
-----
y_log10 and n0_log10 are log10 of MPN per mL (most-probable-number, not CFU).
time_days is days of rifampicin exposure.

LIMIT OF QUANTIFICATION
-----------------------
Verified empirically, not assumed - see verify_floor(). Across all 1932 MPN readings
in the deposit the minimum is exactly 23 MPN/mL and nothing falls below it. The MPN
indices form a decade ladder (2.3, 6.1, 1.3, 4.9 ... x 10^k); the lowest rung ever
reported is 23, and it appears only in T5 columns (never T0, never T2), which is the
signature of an assay floor rather than of a coincidence. A reading at 23 is therefore
carried as CENSORED with limit_log10 = log10(23), and y_log10 is left NaN.

DOSE
----
The deposit records NO rifampicin concentration. dose_value, dose_unit and dose_xmic
are left absent rather than filled in from the paper text. MIC_RIF is present per
isolate, so dose_xmic becomes derivable the moment the exposure concentration is
sourced and recorded.
"""

import os
import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "data", "raw", "tb", "elife93243_supp2.xlsx")
OUT = os.path.join(ROOT, "data", "processed", "tidy_vijay.csv")

DATASET = "vijay2024_elife93243"
ORGANISM = "M. tuberculosis"
DRUG = "rifampicin"

MPN_FLOOR = 23.0                       # MPN per mL
LIMIT_LOG10 = float(np.log10(MPN_FLOOR))

AGES = [15, 30, 60]
TIMEPOINTS = {"T0": 0.0, "T2": 2.0, "T5": 5.0}

COVARIATES = [
    "MIC_INH",
    "MIC_RIF",
    "INH-Suceptibility",      # deposit's own spelling, kept for traceability
    "Time_to_0.4",
    "Time_point",
    "Tolerant_level_D5_15",
    "Tolerant_level_D5_60",
]

SCHEMA = [
    "dataset", "organism", "state", "state_numeric", "drug",
    "dose_value", "dose_unit", "dose_xmic", "unit_group",
    "n0_log10", "time_days", "y_log10", "censored", "limit_log10", "notes",
]


def load():
    return pd.read_excel(SRC, sheet_name="raw data")


def verify_floor(df):
    """Pool every MPN reading and report the low end of the distribution."""
    cols = [f"mpn_{t}_{a}days" for a in AGES for t in TIMEPOINTS]
    pooled = pd.concat([df[c] for c in cols]).dropna().astype(float)
    vc = pooled.value_counts().sort_index()
    report = {
        "n_readings": int(len(pooled)),
        "min": float(pooled.min()),
        "n_below_23": int((pooled < MPN_FLOOR).sum()),
        "n_at_23": int((pooled == MPN_FLOOR).sum()),
        "lowest_six_distinct": [(float(v), int(n)) for v, n in vc.head(6).items()],
        "at_23_by_column": {c: int((df[c] == MPN_FLOOR).sum()) for c in cols},
    }
    return report


def build(df):
    rows = []
    for age in AGES:
        t0col = f"mpn_T0_{age}days"
        for _, r in df.iterrows():
            n0 = r[t0col]
            if pd.isna(n0):
                continue                      # isolate has no series at this culture age
            n0_log10 = float(np.log10(float(n0)))
            n0_cens = float(n0) <= MPN_FLOOR
            for tp, day in TIMEPOINTS.items():
                v = r[f"mpn_{tp}_{age}days"]
                if pd.isna(v):
                    continue                  # absent reading: not emitted, never imputed
                v = float(v)
                cens = v <= MPN_FLOOR
                note = ["MPN/mL", "RIF concentration not recorded in deposit"]
                if cens:
                    note.append("at assay floor 23 MPN/mL")
                if n0_cens:
                    note.append("T0 itself at floor")
                rec = {
                    "dataset": DATASET,
                    "organism": ORGANISM,
                    "state": f"culture_age_{age}d",
                    "state_numeric": float(age),
                    "drug": DRUG,
                    "dose_value": np.nan,
                    "dose_unit": "",
                    "dose_xmic": np.nan,
                    "unit_group": f"vijay_{int(r['Index']):03d}_age{age}d",
                    "n0_log10": n0_log10,
                    "time_days": day,
                    "y_log10": np.nan if cens else float(np.log10(v)),
                    "censored": bool(cens),
                    "limit_log10": LIMIT_LOG10,
                    "notes": "; ".join(note),
                    "isolate_index": int(r["Index"]),
                    "sample_id": r["Sample-ID"],
                    "mpn_raw": v,
                }
                for c in COVARIATES:
                    rec[c] = r[c]
                rows.append(rec)

    out = pd.DataFrame(rows)
    extras = ["isolate_index", "sample_id", "mpn_raw"] + COVARIATES
    return out[SCHEMA + extras]


def main():
    df = load()
    floor = verify_floor(df)
    print("FLOOR CHECK")
    for k, v in floor.items():
        print(f"  {k}: {v}")

    tidy = build(df)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tidy.to_csv(OUT, index=False)
    print(f"\nwrote {OUT}  rows={len(tidy)}")


if __name__ == "__main__":
    main()
