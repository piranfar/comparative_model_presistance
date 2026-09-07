"""OFORI2024 -- Nature Communications Source Data (41467_2024_53933_MOESM8).

katG and bedaquiline killing. The Source Data workbook is almost entirely
dose-response curves and expression values. Only blocks whose sheet NAMES the
quantity it holds are read; every unlabelled block is left alone.

WHAT IS READ
  1. Sheet 'Figure 1c', the block headed "CFU/mL" with a "Day" column: ten
     strains (H37Rv and nine TDR-* clinical isolates) at day 0 and day 30, one
     value per strain per day. 20 readings, the only counts in the deposit.
  2. Sheets 'Figure 3b', 'Figure 3c' and 'Supp Fig 3c', which each hold two
     blocks the sheet labels explicitly in column A -- "BacTiter-Glo"
     (luminescence) and "OD600" -- over a "[BDQ] (uM)" concentration axis, for
     H37Rv and delta-katG in triplicate at eight concentrations. 288 readings.
     These are NOT counts and are never converted to any: readout carries the
     sheet's own word and cfu_per_ml is left blank on every one of them. They
     have no time axis at all, so time_h is blank too.

WHAT IS DELIBERATELY NOT READ, AND WHY
  - 'Figure 1c' also carries a derived "30-Day % Survival" block computed from
    the same twenty numbers. Reading it would double-count.
  - 'Figure 1e' and 'Figure 1f' have a "Day" column (0, 3, 8, 16, 30) and three
    values per strain, but the sheet states NO unit and no readout for those
    values. They are near 100 at day 0 and fall to 0.003, which is consistent
    with a percentage of the day-0 count, but the deposit does not say so. They
    are left out rather than guessed at.
  - Figures 1a, 1b, 1d, 2a, 2b, 2d, 4b, 4c, 4d, 5b, 5c and Supplementary
    Figures 1a, 1b, 2a, 2b, 2c, 4b, 6c, 6d are drug-, CCCP-, nigericin- or
    H2O2-concentration series with no time axis AND no stated readout: column A
    names only the concentration, and nothing on the sheet says what the numbers
    in the body are. Many of them floor at ~0.045, which is what an unsubtracted
    OD blank looks like -- but the sheets do not say so, and guessing would put
    an invented readout into the corpus. They are left out. (Contrast Figures
    3b/3c and Supp Fig 3c, which have the SAME shape but do label their blocks,
    and are therefore read.)
  - Figures 2c, 2e, 2f, 2g, 3a, 4a, 5a, Supplementary Figures 3a, 3b, 5a-c, 6a,
    6b are expression, CellROX fluorescence or statistics. Figure 2e's blocks
    are labelled ("CellROX Fluorescence"), but a redox-dye signal is not a
    measure of how many bacteria are present, so it is not returned as a
    reading; half of that sheet is in any case a derived BDQ/UT ratio.
  - MOESM4 (normalised expression), MOESM5 (RNAseq clusters, GO) and MOESM6
    (iEK1011 flux simulations) contain no colony counts.

WHAT THE DEPOSIT DOES NOT SAY
  - The block gives "CFU/mL" and "Day" and nothing else: no drug is named
    anywhere on that sheet, so `drug` is blank on every row. (The statistics
    block above it compares INH-susceptible with INH-resistant isolates, which
    describes the strains, not the treatment.)
  - No organism is named. Strain labels are kept as given.
  - No plated volume, dilution or limit of detection anywhere, so
    floor_cfu_per_ml is blank.
  - There is one value per strain per day: no replicates.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

from src.ingest import COLUMNS

BOOK = "_unpacked/PMC11561320_supplementary/41467_2024_53933_MOESM8_ESM.xlsx"

NOT_READ = (
    "Figure 1e/1f have a day axis but the sheet states no unit or readout for "
    "their values; the other concentration series (1a, 1b, 1d, 2a, 2b, 2d, 4b, "
    "4c, 4d, 5b, 5c, Supp 1a, 1b, 2a, 2b, 2c, 4b, 6c, 6d) have neither a time "
    "nor a stated readout, so what they measure cannot be established from the "
    "deposit; Figure 2e is CellROX redox-dye fluorescence, not a measure of "
    "bacterial quantity; the rest are expression or statistics; the derived "
    "'30-Day % Survival' block of Figure 1c is not re-read"
)

# Blocks whose sheet writes the readout in column A. Nothing else is read.
LABELLED = ("Figure 3b", "Figure 3c", "Supp Fig 3c")
READOUTS = {
    "BacTiter-Glo": "BacTiter-Glo luminescence (the sheet's own label; NOT a "
                    "count and not converted to one)",
    "OD600": "OD600 (the sheet's own label; NOT a count and not converted "
             "to one)",
}


def _txt(v) -> str:
    return "" if v is None else str(v).replace("\xa0", " ").strip()


def _num(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    return np.nan


def read(d: Path) -> pd.DataFrame:
    wb = load_workbook(d / BOOK, data_only=True)
    ws = wb["Figure 1c"]
    rows: list[dict] = []

    unit_row = next((r for r in range(1, ws.max_row + 1)
                     if _txt(ws.cell(row=r, column=1).value) == "CFU/mL"), None)
    hdr = next((r for r in range(1, ws.max_row + 1)
                if _txt(ws.cell(row=r, column=1).value) == "Day"), None)
    strains = {} if (unit_row is None or hdr is None or hdr != unit_row + 1) \
        else {c: _txt(ws.cell(row=hdr, column=c).value)
              for c in range(2, ws.max_column + 1)
              if _txt(ws.cell(row=hdr, column=c).value)}
    r = (hdr or 0) + 1
    while strains and r <= ws.max_row:
        day = _num(ws.cell(row=r, column=1).value)
        if np.isnan(day):
            break
        for c, strain in strains.items():
            val = _num(ws.cell(row=r, column=c).value)
            if np.isnan(val):
                continue
            rows.append({
                "source_file": BOOK, "sheet": "Figure 1c",
                "organism": "", "strain": strain, "drug": "",
                "arm": strain, "replicate": "",
                "time_h": day * 24.0, "cfu_per_ml": val,
                "readout": "CFU/mL",
                "notes": "block headed 'CFU/mL' with a 'Day' column; days "
                         "converted to hours. The sheet names NO drug for this "
                         "killing experiment, so drug is blank; it names no "
                         "organism either. One value per strain per day -- the "
                         "deposit gives no replicates.",
            })
        r += 1

    # ---- Figures 3b, 3c and Supp Fig 3c: labelled BacTiter-Glo / OD600 ----
    # Each sheet: column A holds the readout name, the row below it the
    # concentration axis and the strain headers (merged over three replicate
    # columns), then eight concentrations. No time axis anywhere on them.
    for name in LABELLED:
        ws = wb[name]
        for r in range(1, ws.max_row + 1):
            label = _txt(ws.cell(row=r, column=1).value)
            if label not in READOUTS:
                continue
            hrow = r + 1
            axis = _txt(ws.cell(row=hrow, column=1).value)
            m = re.match(r"^\[(.+?)\]\s*\((.+?)\)\s*$", axis)
            if not m:
                continue
            drug, unit = m.group(1).strip(), m.group(2).strip()
            grp, cur = {}, ""
            for c in range(2, ws.max_column + 1):
                v = _txt(ws.cell(row=hrow, column=c).value)
                if v:
                    cur = v
                grp[c] = cur
            n = {}
            rr = hrow + 1
            while rr <= ws.max_row:
                conc = _num(ws.cell(row=rr, column=1).value)
                if np.isnan(conc):
                    break
                n.clear()
                for c in range(2, ws.max_column + 1):
                    strain = grp.get(c, "")
                    val = _num(ws.cell(row=rr, column=c).value)
                    if not strain or np.isnan(val):
                        continue
                    n[strain] = n.get(strain, 0) + 1
                    rows.append({
                        "source_file": BOOK, "sheet": name,
                        "organism": "", "strain": strain, "drug": drug,
                        "concentration": conc, "conc_unit": unit,
                        "arm": f"{strain} [{label}]",
                        "replicate": f"rep{n[strain]}",
                        "time_h": np.nan, "cfu_per_ml": np.nan,
                        "readout": READOUTS[label],
                        "notes": f"{name}: block headed '{label}' in column A "
                                 f"over the '{axis}' axis. This is NOT a colony "
                                 f"count -- the value is left out of "
                                 f"cfu_per_ml entirely and lives only in the "
                                 f"reading's readout label; the sheet gives no "
                                 f"time axis, so time_h is blank; it names no "
                                 f"organism. value_as_deposited={val!r} "
                                 f"({label}), which is why cfu_per_ml is "
                                 f"blank -- the corpus's convention for a "
                                 f"reading that is not a count",
                    })
                rr += 1

    df = pd.DataFrame(rows)
    for c in COLUMNS:
        if c not in df.columns:
            df[c] = np.nan if c in ("concentration", "time_h", "colonies",
                                    "dilution", "plated_volume_ul",
                                    "cfu_per_ml", "log10_cfu_per_ml",
                                    "floor_cfu_per_ml") else ""
    df["floor_basis"] = ("no plated volume, dilution or limit of detection "
                         "appears anywhere in this workbook")
    return df[COLUMNS]
