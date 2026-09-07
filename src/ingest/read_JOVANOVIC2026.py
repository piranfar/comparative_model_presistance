"""JOVANOVIC2026 -- Nature Microbiology Source Data, ten workbooks.

Almost none of this deposit is a colony count.  It is a single-cell time-lapse
microscopy study: the time courses in it (MOESM7 "Fig 1c/1de/1g", MOESM8
"Fig 2a", MOESM9 "Fig 3b", MOESM11 "Fig 6d curves", MOESM12 "ED 1b/1e/1g/1h")
report a FRACTION OF LIVE CELLS, a propidium-iodide intensity, or a number of
tracked cells per field.  Those are genuine time-resolved survival data, but the
schema's only quantitative columns are colonies and cfu_per_ml, and a live-cell
fraction is neither; writing 0.11 into cfu_per_ml would be a lie.  They are
therefore left out, and named here so nobody has to rediscover them.  MOESM12
"ED 1f" gives piNEG/piPOS cell numbers per field, which are counts but not
colonies and not per mL, so they are left out for the same reason.  MOESM6,
MOESM10, MOESM13, MOESM15 and the remaining MOESM8/MOESM9 sheets are MICs, AUCs,
growth rates, normalised ODs from a checkerboard, qPCR fold changes and
regimen-ranking tables -- no time-resolved counts.

ONE sheet in the deposit carries CFU: MOESM14_ESM.xlsx, "ED 5 abc", columns
"mc27000_<condition>_mean_log10CFU_day_<n>".  Those are read here, with one
caveat made unmissable: they are MEANS over an unstated number of replicates,
not individual readings.  To stop them being silently counted as readings, their
readout is written as "mean log10 CFU (summary, not a single reading)", so any
downstream filter on readout == "CFU" skips them.

The sheet states no limit of detection.  It is worth recording that 41 of the
130 PBS-starved day-3 and day-7 values sit at exactly 1.30103, which is
log10(20) to six figures -- the signature of a floor substituted for a
below-detection result.  The split is 10 at day 3 and 31 at day 7; there are
none at day 0 and none anywhere in the logGrowth condition.  The deposit never
says so, so floor_cfu_per_ml stays blank.

Day 0 is a SHARED value, not a per-regimen reading.  The PBS-starved day-0
column holds only two distinct numbers across the 65 regimens (7.56017 for the
first 36 rows, 6.459751 for the remaining 29) and the logGrowth day-0 column
only two (6.784427 and 6.801404), so the 130 day-0 rows this reader emits stand
on at most four inoculum measurements.  That is recorded on every row.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

WORKBOOK = "41564_2025_2217_MOESM14_ESM.xlsx"
SHEET = "ED 5 abc"
# "mc27000_PBSstarved_mean_log10CFU_day_3"
CFU_COL = re.compile(
    r"^(?P<strain>[^_]+)_(?P<condition>.+?)_mean_log10CFU_day_(?P<day>\d+)$")

FLOOR_BASIS = (
    "not stated: neither the sheet nor any other file in the deposit gives a "
    "limit of detection. 41 of the 130 PBS-starved day-3 and day-7 values are "
    "exactly 1.30103, which is log10(20) to six figures -- 10 at day 3 and 31 "
    "at day 7, none at day 0 and none anywhere in the logGrowth condition. That "
    "looks like a floor substituted for a below-detection result, but the "
    "deposit never says so and no floor is recorded here"
)


def read(d: Path) -> pd.DataFrame:
    hits = list(d.rglob(WORKBOOK))
    if not hits:
        return empty()
    path = hits[0]
    rel = str(path.relative_to(d)).replace("\\", "/")

    df = pd.read_excel(path, sheet_name=SHEET)
    cols = {c: CFU_COL.match(str(c).strip()) for c in df.columns}
    cfu_cols = {c: m for c, m in cols.items() if m}
    if not cfu_cols:
        return empty()

    if "RegimenAbbreviation" not in df.columns or "RegimenName" not in df.columns:
        raise ValueError("%s: expected RegimenAbbreviation and RegimenName" % SHEET)

    out = []
    for _, row in df.iterrows():
        abbr = str(row["RegimenAbbreviation"]).strip()
        name = str(row["RegimenName"]).strip()
        if not abbr or abbr.lower() == "nan":
            continue
        for c, m in cfu_cols.items():
            v = row[c]
            if not (isinstance(v, (int, float, np.number)) and np.isfinite(v)):
                continue
            cond = m.group("condition")
            out.append({
                "source_file": rel, "sheet": SHEET,
                "organism": "", "strain": m.group("strain"),
                "drug": name, "concentration": np.nan, "conc_unit": "",
                "arm": "%s (%s)" % (abbr, cond),
                "replicate": "", "tech_replicate": "",
                "time_h": float(m.group("day")) * 24.0,
                "cfu_per_ml": float(10.0 ** float(v)),
                "floor_basis": FLOOR_BASIS,
                "readout": "mean log10 CFU (summary, not a single reading)",
                "notes": ('column "%s"; the culture condition for this row is '
                          '"%s" as the column name gives it' % (c, cond)),
            })

    if not out:
        return empty()

    res = pd.DataFrame(out)
    common = (
        "THIS ROW IS A MEAN, NOT A READING: the column is named "
        "mean_log10CFU and the deposit nowhere states how many replicates the "
        "mean is over, so it cannot be split into readings; readout is marked "
        "accordingly so it is not counted as a colony count. cfu_per_ml is "
        "10**(the mean of log10), which is the sheet's own quantity "
        "back-transformed, not a mean count. Day converted to hours (source in "
        "days). DAY 0 IS SHARED, NOT PER REGIMEN: the day-0 column of each "
        "condition holds only two distinct values across all 65 regimens "
        "(PBS-starved 7.56017 and 6.459751; logGrowth 6.784427 and 6.801404), "
        "so the 130 day-0 rows in this frame stand on at most four inoculum "
        "measurements and must not be counted as 130 independent readings. "
        "No drug concentration is given on this sheet, so concentration "
        "is blank. Organism left blank: the sheet names only the strain "
        '("mc27000") and never the species. No colony count, dilution or plated '
        "volume appears anywhere in the deposit."
    )
    res["notes"] = [n + "; " + common for n in res["notes"]]
    return finish(res, "JOVANOVIC2026")
