"""STEWART2012 -- Stewart & Rozen archived data (Dryad, Zenodo mirror).

One legacy .xls (xlsx internally).  Sheet 'Timekill curves' is a 195 x 23 grid
holding three side-by-side drug blocks whose names sit in row 0 at columns A,
I and Q: AMPICILLIN, STREPTOMYCIN, NORFLOXACIN.  Within a block each strain is
an eight-row unit -- a banner row naming the ECOR isolate, a header row, then
five rows for 0, 60, 120, 180 and 240 minutes.  The seven columns of a block
are Time(min), Rep1, Rep2, then Rep1, Rep2, Mean and SE again; the second set
is the first divided by its own t=0 value, which the sheet says outright in
its footer, "BOLD VALUES INDICATE NORMALISED VALUES".  Only the two raw
columns are ingested; the four derived ones are not.

THREE THINGS THE SHEET DOES NOT SAY, AND SO ARE BLANK OR FLAGGED HERE.

1. The organism.  ECOR is a named collection of Escherichia coli isolates, but
   this workbook never writes that down, so `organism` is blank and only the
   isolate label goes in `strain`.

2. The unit of the two raw columns.  They are headed "Rep1"/"Rep2" and nothing
   else.  They are recorded as cfu_per_ml because the sheet's own normalised
   columns are these divided by the t=0 value and because ~1e7 at t=0 cannot
   be a plate colony count -- but that is an inference from the deposit's
   internal arithmetic, not a statement in it.  Every row carries the token
   `unit_inferred=cfu_per_ml` at the front of its notes, so all 658 can be
   found and dropped with one grep by anyone who would rather not have them.

3. The floor.  No plated volume, no dilution, no stated limit of detection:
   floor_cfu_per_ml is blank.  Sixteen readings are exactly 1, which is not a
   density anyone measures; they are almost certainly a placeholder that lets
   a zero be plotted on a log axis, but the sheet does not say so, so they are
   ingested as deposited, flagged in notes, and NOT converted to a floor.

The second sheet, 'Competitions', is a pairwise competition assay counted in
rounds of competition rather than time, and is not read.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingest import empty

BLOCKS = [(0, "ampicillin"), (8, "streptomycin"), (16, "norfloxacin")]
SHEET = "Timekill curves"

_UNIT_NOTE = (
    "unit_inferred=cfu_per_ml; "
    "the sheet heads the two raw columns only 'Rep1'/'Rep2' and states no "
    "unit; recorded as CFU/mL because the sheet's own normalised columns are "
    "these divided by the t=0 value and ~1e7 at t=0 cannot be a plate count; "
    "source time unit: minutes, converted to hours"
)


def read(d: Path) -> pd.DataFrame:
    xls = list(d.glob("*.xls")) + list(d.glob("*.xlsx"))
    if not xls:
        return empty()
    path = xls[0]
    g = pd.read_excel(path, SHEET, header=None)

    rows = []
    for c0, drug in BLOCKS:
        header = g.iat[0, c0]
        if not isinstance(header, str) or header.strip().lower() != drug:
            continue
        r = 1
        while r < len(g):
            banner = g.iat[r, c0]
            if isinstance(banner, str) and banner.strip().startswith("ECOR"):
                strain = banner.strip()
                rr = r + 2  # skip the banner and the column-header row
                while rr < len(g) and isinstance(g.iat[rr, c0], (int, float)) \
                        and pd.notna(g.iat[rr, c0]):
                    minutes = float(g.iat[rr, c0])
                    for k, rep in ((1, "Rep1"), (2, "Rep2")):
                        v = g.iat[rr, c0 + k]
                        if not isinstance(v, (int, float)) or pd.isna(v):
                            continue
                        note = _UNIT_NOTE
                        if float(v) == 1.0:
                            note += ("; this reading is exactly 1, which is "
                                     "not a measurable density -- almost "
                                     "certainly a stand-in for zero, but the "
                                     "sheet does not say so and no floor is "
                                     "inferred from it")
                        rows.append({
                            "source_file": path.name, "sheet": SHEET,
                            "organism": "", "strain": strain, "drug": drug,
                            "arm": drug, "replicate": rep,
                            "time_h": minutes / 60.0,
                            "cfu_per_ml": float(v), "readout": "CFU",
                            "notes": note,
                        })
                    rr += 1
                r = rr
            else:
                r += 1
    if not rows:
        return empty()
    return pd.DataFrame(rows)
