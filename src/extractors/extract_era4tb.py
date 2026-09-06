"""
Extract the ERA4TB six-laboratory M. tuberculosis time-kill deposit into the
common tidy schema.

Source:  data/raw/tb/era4tb_timekill.csv   (encoding='latin-1'; the Comments
         column contains a Latin-1 micro sign in "100ul quad" etc.)
Target:  data/processed/tidy_era4tb.csv

Rules applied, and why:

  * A BQL=1 reading is CENSORED, not missing and not zero. It is kept, with
    y_log10 = NaN, censored = True, and limit_log10 = the limit of the plating
    volume that produced THAT reading.
  * An AQL=1 reading (plate too full to count) carries no magnitude and is not
    left-censored either. Those rows are DROPPED and counted.
  * A row with no CFU and neither flag is a value the depositors did not report.
    It is kept as absent (y_log10 = NaN, censored = False) with an explicit
    note, so the design layout survives and nothing is silently invented.
  * limit_log10 = log10(1000 / Volume_uL), because CFU is reported per mL and
    one colony on a plate of V uL is 1000/V CFU/mL. Verified against the data:
    the smallest uncensored count at each volume is exactly that single-colony
    floor (10 at 100 uL, 100 at 10 uL, 400 at 2.5 uL) and no uncensored reading
    falls below its own limit.
  * No MIC in ug/mL appears anywhere in the deposit, so dose is recorded in
    multiples of MIC only and dose_value == dose_xmic.

Run:  python -m src.extractors.extract_era4tb
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
OUT = ROOT / "data" / "processed" / "tidy_era4tb.csv"

SCHEMA = [
    "dataset", "organism", "state", "state_numeric", "drug",
    "dose_value", "dose_unit", "dose_xmic", "unit_group", "n0_log10",
    "time_days", "y_log10", "censored", "limit_log10", "notes",
]

# Sample string -> (drug, dose in multiples of MIC)
SAMPLE_MAP = {
    "untreated":    ("none", 0.0),
    "Inoculum TKA": ("none", 0.0),
    "MXF 1X MIC":   ("moxifloxacin", 1.0),
    "MXF 10X MIC":  ("moxifloxacin", 10.0),
    "INH 1X MIC":   ("isoniazid", 1.0),
    "INH 10X MIC":  ("isoniazid", 10.0),
}

SLUG = {
    "untreated": "untreated",
    "Inoculum TKA": "inoculumTKA",
    "MXF 1X MIC": "MXF1x",
    "MXF 10X MIC": "MXF10x",
    "INH 1X MIC": "INH1x",
    "INH 10X MIC": "INH10x",
}


def main() -> None:
    raw = pd.read_csv(RAW, encoding="latin-1")
    n_raw = len(raw)

    unknown = set(raw["Sample"].unique()) - set(SAMPLE_MAP)
    if unknown:
        raise ValueError(f"unmapped Sample values: {unknown}")

    # --- drop the above-quantification rows, having counted them -------------
    n_aql = int((raw["AQL"] == 1).sum())
    n_bql = int((raw["BQL"] == 1).sum())
    n_both = int(((raw["AQL"] == 1) & (raw["BQL"] == 1)).sum())
    if n_both:
        raise ValueError(f"{n_both} rows flagged AQL and BQL at once")
    if raw.loc[raw["BQL"] == 1, "CFU"].notna().any():
        raise ValueError("a BQL row carries a CFU value; censoring is not clean")
    if raw.loc[raw["AQL"] == 1, "CFU"].notna().any():
        raise ValueError("an AQL row carries a CFU value")

    df = raw[raw["AQL"] != 1].copy()

    # --- build the tidy frame ------------------------------------------------
    out = pd.DataFrame(index=df.index)
    out["dataset"] = "era4tb"
    out["organism"] = "M. tuberculosis"
    out["state"] = "standard"
    out["state_numeric"] = np.nan
    out["drug"] = df["Sample"].map(lambda s: SAMPLE_MAP[s][0])
    out["dose_value"] = df["Sample"].map(lambda s: SAMPLE_MAP[s][1])
    out["dose_unit"] = "xMIC"
    out["dose_xmic"] = out["dose_value"]

    out["unit_group"] = (
        "era4tb_" + df["Institute"].astype(str)
        + "_" + df["Sample"].map(SLUG)
        + "_r" + df["Replicate"].astype(int).astype(str)
    )

    out["time_days"] = df["Time"].astype(float)
    out["censored"] = df["BQL"] == 1
    out["y_log10"] = np.where(out["censored"], np.nan, df["CFUlog10"])
    out["limit_log10"] = np.log10(1000.0 / df["Volume"])

    # --- notes: plating geometry + why a value is absent ---------------------
    def note(r: pd.Series) -> str:
        bits = [f"plated_volume_uL={r.Volume:g}" if pd.notna(r.Volume)
                else "plated_volume_uL=absent"]
        bits.append(f"plating_condition={int(r.Condition)}")
        if r.BQL == 1:
            bits.append("below_limit_of_quantification")
        elif pd.isna(r.CFU):
            bits.append("no_value_reported_not_censored")
        if pd.isna(r.Volume):
            bits.append("plating_volume_absent_so_limit_undefined")
        if r.Volume == 50.0:
            bits.append("volume_50uL_disagrees_with_comment_100uL_quad")
        if r.Time < 0:
            bits.append("pre_inoculation_reading_time_-3d")
        if r.Sample == "Inoculum TKA":
            bits.append("inoculum_arm_not_a_treatment_arm")
        return "; ".join(bits)

    out["notes"] = df.apply(note, axis=1)

    # --- n0_log10: mean of uncensored 100 uL readings on days 0 and 1 --------
    base = df[
        (df["Volume"] == 100.0)
        & (df["Time"].isin([0, 1]))
        & (df["BQL"] == 0)
        & (df["CFU"].notna())
    ]
    key = (
        "era4tb_" + base["Institute"].astype(str)
        + "_" + base["Sample"].map(SLUG)
        + "_r" + base["Replicate"].astype(int).astype(str)
    )
    n0 = base.groupby(key.values)["CFUlog10"].mean()
    out["n0_log10"] = out["unit_group"].map(n0)

    # Record which visits actually supplied n0. Only laboratories C and D
    # sampled the treated flasks on day 0; at A, B, E and F every treated
    # flask's n0 is a day-1 reading taken AFTER the drug was added.
    src = base.groupby(key.values)["Time"].apply(
        lambda s: ",".join(str(int(x)) for x in sorted(s.unique()))
    )
    src_map = out["unit_group"].map(src)
    out["notes"] = out["notes"] + np.where(
        src_map.isna(), "; n0_source=none_available",
        "; n0_source_days=" + src_map.astype(str)
    )

    # Flag every censored reading that another plating volume of the SAME
    # sample at the SAME visit contradicts. If the 100 uL plate reads 6.9
    # log10 CFU/mL, a 2.5 uL drop of that sample cannot be below 2.6 log10;
    # such a BQL flag records a plate that could not be read, not a culture
    # below the limit. Derived here, not asserted by the depositors.
    contra = pd.Series(0.0, index=out.index)
    for _, g in out.groupby(["unit_group", "time_days"]):
        cen = g[g["censored"]]
        unc = g[g["y_log10"].notna()]
        if len(cen) and len(unc):
            top = unc["y_log10"].max()
            for i, c in cen.iterrows():
                if pd.notna(c["limit_log10"]) and top > c["limit_log10"]:
                    contra.loc[i] = top - c["limit_log10"]
    hit = contra > 0
    out.loc[hit, "notes"] = (
        out.loc[hit, "notes"]
        + "; bql_contradicted_by_another_plating_of_same_sample_by_"
        + contra[hit].round(2).astype(str) + "_log10"
    )

    out = out[SCHEMA].sort_values(
        ["unit_group", "time_days", "limit_log10"], kind="mergesort"
    ).reset_index(drop=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)

    print(f"raw rows                       {n_raw}")
    print(f"AQL=1 rows dropped             {n_aql}")
    print(f"BQL=1 rows kept as censored    {n_bql}")
    print(f"rows written                   {len(out)}")
    print(f"unit_groups                    {out.unit_group.nunique()}")
    print(f"unit_groups with n0_log10      {out.groupby('unit_group').n0_log10.first().notna().sum()}")
    print(f"contradicted BQL flags         {int(hit.sum())}")
    print(f"written to                     {OUT}")


if __name__ == "__main__":
    main()
