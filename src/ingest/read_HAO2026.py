"""HAO2026 -- figshare deposit "Contezolid and polymyxin B nonapeptide".

Five per-figure workbooks.  Two of them hold bacterial counts over time and
are read here; the other three do not, and are listed at the bottom with the
reason each was left alone.

Figure_2.xlsx -- the time-kill.  One sheet per strain (Fig. 2A = Ab19606,
2B = Ab1605, 2C = Ab9R65, each named in the sheet's own arm headers).  The
ORGANISM is named too, in the title cell each of those sheets opens with:
"Time-kill assay of A. baumannii strains using the drugs alone or in
combination".  It is taken from there and nowhere else -- the reader looks for
that literal in the sheet's own first cell and leaves organism blank if it is
not there.  A sheet
is four stacked two-row units: a row giving the time ("1 h", "6 h", "12 h",
"24 h") and the four arm labels at columns 1, 4, 7 and 10, then a row headed
"Log10 CFU/mL" with three replicate values under each arm.  The arm label
carries both the strain and the treatment, e.g. "Ab19606+Contezolid"; CP is
the deposit's own name for the contezolid/PBNP combination and is kept as
written rather than expanded.

Figure_5.xlsx sheet 'Fig. 5A-5C' -- bacterial loads recovered from MH-S cells
at 1, 6 and 12 h, four arms, six replicates each, also in Log10 CFU/mL.  Its
title cell says only "Bacterial loads in MH-S cell treated by the drugs": it
names neither organism nor strain, so both are blank on those 72 rows even
though other workbooks in the same deposit say A. baumannii.  Those are
different assays and the association is not stated.

NOT READ, and why:
  Figure_1.xlsx      checkerboard: a concentration grid with no time axis.
  Figure_4.xlsx      biofilm OD595/OD600 at a single unstated time.
  Figure_5 'Fig. 5D-5F'  host-cell viability (%), not a bacterial readout.
  Figure_6.xlsx      C. elegans survival scored 0/1 per worm, not a density.

NO FLOOR.  Nothing in any of the five workbooks states a plated volume, a
dilution or a limit of detection, so floor_cfu_per_ml is blank throughout.
NO TIME ZERO either: the first sampling point in the time-kill is 1 h, so the
deposit contains no inoculum density.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from src.ingest import empty

TIME_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*h\s*$", re.I)
# taken only if the sheet's own title cell contains it -- see the docstring
ORGANISM_IN_TITLE = "A. baumannii"
FLOOR_NOTE = ("no plated volume, dilution or limit of detection anywhere in "
              "the deposit")


def _hours(cell) -> float | None:
    if isinstance(cell, str):
        m = TIME_RE.match(cell)
        if m:
            return float(m.group(1))
    return None


def _timekill(path: Path) -> list[dict]:
    rows = []
    xl = pd.ExcelFile(path)
    for sheet in xl.sheet_names:
        g = xl.parse(sheet, header=None)
        title = g.iat[0, 0] if len(g) else None
        organism = (ORGANISM_IN_TITLE
                    if isinstance(title, str) and ORGANISM_IN_TITLE in title
                    else "")
        for r in range(len(g)):
            t = _hours(g.iat[r, 0])
            if t is None or r + 1 >= len(g):
                continue
            label = g.iat[r + 1, 0]
            if not (isinstance(label, str) and "cfu" in label.lower()):
                continue
            # arm headers sit on row r, values on row r+1, three per arm
            for c in range(1, g.shape[1]):
                arm = g.iat[r, c]
                if not isinstance(arm, str) or not arm.strip():
                    continue
                arm = arm.strip()
                strain = arm.split("+")[0].strip()
                treat = arm.split("+", 1)[1].strip() if "+" in arm else ""
                for k in range(3):
                    if c + k >= g.shape[1]:
                        break
                    v = g.iat[r + 1, c + k]
                    if not isinstance(v, (int, float)) or pd.isna(v):
                        continue
                    rows.append({
                        "source_file": path.name, "sheet": sheet,
                        "organism": organism, "strain": strain,
                        "drug": "" if treat.upper() == "PBS" else treat,
                        "arm": arm, "replicate": f"rep{k + 1}",
                        "time_h": t, "cfu_per_ml": 10.0 ** float(v),
                        "readout": "CFU",
                        "floor_basis": FLOOR_NOTE,
                        "notes": ("sheet gives Log10 CFU/mL directly; the "
                                  "organism is taken from this sheet's own "
                                  "title cell, which names A. baumannii; the "
                                  "PBS arm is read as the no-drug arm and CP "
                                  "is the deposit's own label for the "
                                  "contezolid+PBNP combination, kept "
                                  "unexpanded -- neither is spelled out in "
                                  "the workbook, and the raw label is in "
                                  "`arm`; source time unit: hours; first "
                                  "sampling point is 1 h, so there is no "
                                  "inoculum reading"),
                    })
    return rows


def _mhs(path: Path) -> list[dict]:
    rows = []
    xl = pd.ExcelFile(path)
    if "Fig. 5A-5C" not in xl.sheet_names:
        return rows
    g = xl.parse("Fig. 5A-5C", header=None)
    for r in range(len(g)):
        t = _hours(g.iat[r, 0])
        if t is None or r + 1 >= len(g):
            continue
        label = g.iat[r + 1, 0]
        if not (isinstance(label, str) and "cfu" in label.lower()):
            continue
        for c in range(1, g.shape[1]):
            arm = g.iat[r, c]
            if not isinstance(arm, str) or not arm.strip():
                continue
            arm = arm.strip()
            for k in range(6):
                if c + k >= g.shape[1]:
                    break
                v = g.iat[r + 1, c + k]
                if not isinstance(v, (int, float)) or pd.isna(v):
                    continue
                rows.append({
                    "source_file": path.name, "sheet": "Fig. 5A-5C",
                    "organism": "", "strain": "",
                    "drug": "" if arm.upper() == "PBS" else arm,
                    "arm": arm, "replicate": f"rep{k + 1}",
                    "time_h": t, "cfu_per_ml": 10.0 ** float(v),
                    "readout": "CFU",
                    "floor_basis": FLOOR_NOTE,
                    "notes": ("intracellular bacterial load recovered from "
                              "MH-S cells, Log10 CFU/mL as given; this "
                              "sheet's title names neither organism nor "
                              "strain, so both are left blank -- other "
                              "workbooks in the deposit say A. baumannii but "
                              "for different assays; source time unit: hours"),
                })
    return rows


def read(d: Path) -> pd.DataFrame:
    rows = []
    f2 = d / "Figure_2.xlsx"
    if f2.exists():
        rows += _timekill(f2)
    f5 = d / "Figure_5.xlsx"
    if f5.exists():
        rows += _mhs(f5)
    if not rows:
        return empty()
    return pd.DataFrame(rows)
