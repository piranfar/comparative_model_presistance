"""ENOBLOCK -- BioStudies SourceData for the A. baumannii enolase-inhibitor
paper.  Two files were obtained, and NEITHER of them is a colony count.

Both hold the same thing in two formats: a 24-hour growth curve read every
20 minutes for four conditions in duplicate (N1, N2).  The layout is a two-row
header -- condition names spanning pairs of columns, then N1/N2 -- above a
Time column and eight value columns.

WHAT THE FILES DO NOT SAY, AND WHY THAT MATTERS HERE.

  * The readout is unlabelled.  The values run from 0.005 to 1.65 and the
    files are called "Bacterial growth", but nothing in either file writes
    OD, OD600, absorbance or any other unit.  `readout` therefore says the
    signal is unlabelled and `cfu_per_ml` is empty.  The schema has no column
    for a non-count value, so the number itself is carried in `notes` as
    "value_as_deposited=<x>"; nothing here may be turned into a density.
  * The time unit is unlabelled.  The column is headed only "Time" and runs
    0 to 23.67 in steps of 0.3333.  Read as hours; said so in every note.
  * There is no plated volume, dilution or limit of detection, because there
    is no plating at all.  The floor is blank.

ONE CONFLICT THE DEPOSIT LEAVES UNRESOLVED, AND WHY THAT MAKES A FIELD BLANK.
The file named Bacterial_growth_Ab_CR17_Col_ENO.xlsx carries, inside its
sheet, exactly the same condition headers as the ATCC 17978 file, naming
"Ab ATCC 17978" and not CR17.  The two files are not copies -- their values
differ throughout -- so one of the two labels on this file is wrong and the
deposit does not say which.  `strain` is therefore BLANK for every row from
that file, with both claims written out in `notes`.  Taking the in-sheet
header at face value would be worse than blank: it would put this file's 576
readings under the same strain label as the other file's, and anyone grouping
by strain would silently merge two different experiments.  The ATCC file,
where filename and header agree, keeps its strain.

The organism is written only as "Ab" in the headers, so `organism` is blank.

ONE MORE MERGE HAZARD.  Because both files use the same four condition banners
and the same N1/N2 replicate labels, a series here is (source_file, arm,
replicate) and NOT (arm, replicate): grouping without source_file silently
folds the two experiments into one.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from src.ingest import empty

CONC_RE = re.compile(r"\(([\d.]+)\s*(mg/L|mg/l|ug/mL|µg/mL)?\)")
READOUT = "unlabelled growth signal (no unit given in the file)"
TIME_NOTE = ("the file heads the time column only 'Time', with values 0 to "
             "23.67 in steps of 0.3333; read as hours")


def _condition(header: str) -> tuple[str, str, float | None, str]:
    """-> (strain, drug, concentration, conc_unit) from a column banner."""
    h = header.strip()
    parts = [p.strip() for p in h.split("+")]
    strain = parts[0]
    if strain.lower().startswith("enoblock"):
        strain = ""  # the banner names only the drug
    drugs, concs, units = [], [], []
    for p in parts if strain == "" else parts[1:]:
        name = CONC_RE.sub("", p).strip()
        m = CONC_RE.search(p)
        if name:
            drugs.append(name)
        if m:
            concs.append(float(m.group(1)))
            units.append(m.group(2) or "")
    drug = " + ".join(drugs)
    if len(concs) == 1:
        return strain, drug, concs[0], units[0]
    return strain, drug, None, ""


def _num(v):
    """A cell as a float, or None.  The CSV comes back all-string because its
    first two rows are headers, so every value needs coercing."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).strip())
    except ValueError:
        return None


def _table(path: Path) -> pd.DataFrame | None:
    if path.suffix.lower() == ".csv":
        g = pd.read_csv(path, sep=";", header=None, encoding="utf-8-sig")
    elif path.suffix.lower() in (".xlsx", ".xls"):
        g = pd.read_excel(path, sheet_name=0, header=None)
    else:
        return None
    return g


def read(d: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(d.iterdir()):
        if path.suffix.lower() not in (".csv", ".xlsx", ".xls"):
            continue
        g = _table(path)
        if g is None or g.shape[1] < 3:
            continue
        banners: dict[int, str] = {}
        for c in range(1, g.shape[1]):
            v = g.iat[0, c]
            if isinstance(v, str) and v.strip():
                banners[c] = v.strip()
        if not banners:
            continue
        cols = sorted(banners)
        # A file whose name and whose own header disagree about the strain
        # cannot supply one: the row keeps neither claim, and states both.
        filename_conflict = (
            "STRAIN UNRESOLVED: the filename says CR17 while the sheet header "
            "inside it names '" + str(g.iat[0, 1]).strip() + "'; the deposit "
            "does not say which is right, so strain is left blank rather than "
            "merged with the other file's series"
            if "CR17" in path.name else "")

        for r in range(2, len(g)):
            t = _num(g.iat[r, 0])
            if t is None:
                continue
            for i, c in enumerate(cols):
                stop = cols[i + 1] if i + 1 < len(cols) else g.shape[1]
                for c2 in range(c, stop):
                    v = _num(g.iat[r, c2])
                    if v is None:
                        continue
                    rep = g.iat[1, c2]
                    strain, drug, conc, unit = _condition(banners[c])
                    if filename_conflict:
                        strain = ""
                    note = (f"value_as_deposited={v:g} (unitless, see readout); "
                            f"{TIME_NOTE}; "
                            "no plating, so no volume, dilution or limit of "
                            "detection exists in this deposit; organism "
                            "written only as 'Ab' in the header")
                    if not strain and not filename_conflict:
                        note += ("; this column's banner names only the drug, "
                                 "so no strain is recorded for it")
                    if filename_conflict:
                        note += "; " + filename_conflict
                    rows.append({
                        "source_file": path.name,
                        "sheet": "Hoja1" if path.suffix.lower() != ".csv" else "",
                        "organism": "", "strain": strain, "drug": drug,
                        "concentration": conc, "conc_unit": unit,
                        "arm": banners[c],
                        "replicate": str(rep) if isinstance(rep, str) else "",
                        "time_h": t, "readout": READOUT,
                        "notes": note,
                    })
    if not rows:
        return empty()
    return pd.DataFrame(rows)
