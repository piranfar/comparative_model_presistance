"""MANUSE2021 -- PLoS Biology 10.1371/journal.pbio.3001194, S1 Data.

The supplementary zip unpacks to four workbooks. Three are tables of strains,
plasmids and primers (s011, s012, s013) with no measurements in them. The fourth,
pbio.3001194.s015.xlsx, is the numerical raw data: 22 sheets, one or two per
figure panel.

Two kinds of sheet are returned.

  Fig S1A   the only viable-count time course in the deposit. A1 says `CFU/mL`,
            A2 says `Time (hours)`, and three group headings -- MG1655, DaceA,
            Dicd -- each span nine columns, one per culture. Times 0, 1, 3, 5.

  Fig S2A left / right, S2B left / right, S2C left / right, S2D
            28,772 plate-reader readings on a ten-minute grid. A1 says `OD600`,
            A2 says `Time (hours)`, and the group headings name the strain and
            the carbon source (`MG1655`, `pyr_MG1655_DicdA`, `ace_W310D`, and so
            on). These are drug-free growth curves, not kill curves, and an OD
            is never turned into a count: cfu_per_ml is blank on all of them,
            readout says OD600 and the value rides in notes, which is how every
            other reader in this corpus carries a non-count reading.

            An earlier version of this reader left them out on the grounds that
            they would swamp the corpus. That was a judgement about summary
            statistics, not about the data, and it made this deposit
            inconsistent with LEON2025 in the same batch, whose OD600 rows are
            kept. They are in. Filter on readout to get the counts back.

The other fifteen sheets are NOT returned, and here is what each of them is, so
that nobody has to reopen a 3 MB workbook to find out:

    Fig 1D                      `% Survival` by fluorescence bin (Dim / Middle
                                / Bright). No time axis, and the denominator is
                                not on the sheet
    Fig 2C, S1B, S4B            single-cell 488ex/405ex ATP-reporter ratios
    Fig 2D, 2E, S1C, S4C        `RLU/OD600` against an arsenate concentration.
                                No time axis. Arsenate is the treatment named,
                                and it is not an antibiotic, so putting it in
                                the drug column would say something the corpus
                                would misread
    Fig 3CDE and Fig S7A,
    Fig S10                     per-cell 488ex fluorescence against
                                `Time (Frames/30 minutes)` -- roughly 180,000
                                cells x frames. A time axis, but the unit of
                                observation is one cell, not one culture, and
                                the schema's replicate is a culture
    Fig S6B, S7BC, S8AB         per-persister fluorescence, area, division time
    Fig S3                      fluorescence before and after ciprofloxacin

WHAT THE DEPOSIT DOES NOT SAY, and is therefore blank here:

  * the drug and its concentration. Sheet Fig S1A names neither, and neither
    does any Fig S2 sheet. Ciprofloxacin is named in the deposit, but on a
    different sheet (Fig S3, "Before / After ciprofloxacin", a fluorescence
    comparison), which says nothing about what was used for the Fig S1A kill
    curve. drug and concentration stay blank on every row returned here.
  * the organism. `MG1655`, `DaceA`, `Dicd` and the Fig S2 headings are
    recorded as strain, as the sheets write them. No species is named anywhere.
  * plated volume, dilution, limit of detection -- searched cell by cell across
    all four workbooks and absent. The only value unit stated anywhere is the
    single `CFU/mL` in Fig S1A A1 and the `OD600` in the Fig S2 sheets.

TWO CELLS CARRY AN UNEXPLAINED FLAG. O5 reads `1060000.0*` and H6 reads
`260000.000000*`, both as text rather than numbers, and no legend for the
asterisk exists anywhere in the four workbooks. Both are returned with the
number as written and a note saying the flag's meaning is unknown -- filter on
that note if the flag turns out to mean "excluded".
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import openpyxl
import pandas as pd

from src.ingest import empty, finish

STUDY = "MANUSE2021"
SOURCE = "_unpacked/PMC8084331_supplementary/pbio.3001194.s015.xlsx"
COUNT_SHEET = "Fig S1A"
OD_SHEETS = ("Fig S2A left", "Fig S2A right", "Fig S2B left", "Fig S2B right",
             "Fig S2C left", "Fig S2C right", "Fig S2D")
SYMBOL_DELTA = ""
TIME_ANCHOR = re.compile(r"^\s*time\s*\(\s*hours?\s*\)\s*$", re.I)
FLAGGED = re.compile(r"^\s*([0-9]*\.?[0-9]+)\s*\*\s*$")

FLOOR_BASIS = ("no plated volume, dilution or limit of detection anywhere in "
               "the four workbooks of this deposit")
OD_FLOOR_BASIS = ("not applicable: an optical-density sheet, not a colony "
                  "count. The deposit states no OD blank or threshold either")


def _txt(v) -> str:
    return "" if v is None else str(v).replace("\xa0", " ").strip()


def _value(v) -> tuple[float | None, str]:
    """Number, and a note when the workbook wrote it with a flag on it."""
    if isinstance(v, bool) or v is None:
        return None, ""
    if isinstance(v, (int, float)):
        return float(v), ""
    s = _txt(v)
    m = FLAGGED.match(s)
    if m:
        return float(m.group(1)), (
            f"the workbook writes this cell as {s!r}, as text; the asterisk is "
            f"not explained anywhere in the deposit, so its meaning is unknown "
            f"and the number is recorded as written")
    try:
        return float(s), ""
    except ValueError:
        return None, ""


def _panel(ws, sheet: str) -> list[dict]:
    """One `Time (hours)` anchor, group headings to its right, readings below.

    Fig S1A and all seven Fig S2 sheets share this geometry exactly: the value
    unit alone in A1, `Time (hours)` in A2, merged group headings across row 2,
    one column per culture and one row per timepoint.
    """
    g = {}
    for row in ws.iter_rows():
        for cell in row:
            g[(cell.row, cell.column)] = cell.value

    anchor = next(((r, c) for r in range(1, ws.max_row + 1)
                   for c in range(1, ws.max_column + 1)
                   if TIME_ANCHOR.match(_txt(g.get((r, c))))), None)
    if anchor is None:
        return []
    ar, ac = anchor

    unit = ""                                  # the sheet's own value unit
    for r in range(1, ar):
        for c in range(1, ws.max_column + 1):
            t = _txt(g.get((r, c)))
            if t.lower().replace(" ", "") in {"cfu/ml", "od600"}:
                unit = t
    flat = unit.lower().replace(" ", "")
    readout = "CFU" if flat == "cfu/ml" else "OD600" if flat == "od600" else ""
    is_count = readout == "CFU"

    times = []
    rr = ar + 1
    while rr <= ws.max_row:
        v, _ = _value(g.get((rr, ac)))
        if v is None:                          # the grid ends at the first gap
            break
        times.append((rr, v))
        rr += 1

    heads = [c for c in range(ac + 1, ws.max_column + 1) if _txt(g.get((ar, c)))]
    out = []
    for i, h in enumerate(heads):
        end = heads[i + 1] - 1 if i + 1 < len(heads) else ws.max_column
        strain = _txt(g.get((ar, h)))
        delta = (f"the sheet writes the deletion mark in this heading as "
                 f"U+F044, a Symbol-font capital delta; it is kept verbatim and "
                 f"is the same mark Fig S1A writes as a plain 'D'"
                 if SYMBOL_DELTA in strain else "")
        rep = 0
        for c in range(h, end + 1):
            vals = [(r, t) + _value(g.get((r, c))) for r, t in times]
            if all(v is None for _, _, v, _ in vals):
                continue
            rep += 1
            for _, t, v, flag in vals:
                if v is None:
                    continue
                out.append({
                    "source_file": SOURCE, "sheet": sheet, "organism": "",
                    "strain": strain, "drug": "", "concentration": None,
                    "conc_unit": "", "arm": strain,
                    "replicate": f"{sheet}/{strain}-rep{rep}",
                    "tech_replicate": "",
                    "time_h": t, "cfu_per_ml": v if is_count else None,
                    "readout": readout,
                    "floor_basis": FLOOR_BASIS if is_count else OD_FLOOR_BASIS,
                    "notes": "; ".join(x for x in [
                        "source time in hours",
                        f"sheet states its value unit as {unit!r}" if unit
                        else "the sheet states no value unit",
                        "" if is_count else
                        (f"value={v!r} {unit or 'unstated quantity'}; the schema "
                         f"has no column for a non-count reading, so the value "
                         f"is kept here and cfu_per_ml is left blank -- an "
                         f"optical density is NEVER converted to a count"),
                        "the sheet names no drug and no concentration",
                        delta, flag,
                    ] if x),
                })
    return out


def read(d: Path) -> pd.DataFrame:
    path = d / SOURCE
    if not path.is_file():
        return empty()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(path, data_only=True)

    out = []
    for sheet in (COUNT_SHEET,) + OD_SHEETS:
        if sheet in wb.sheetnames:
            out.extend(_panel(wb[sheet], sheet))
    if not out:
        return empty()
    return finish(pd.DataFrame(out), STUDY)
