"""LEON2025 -- figshare 10.6084/m9.figshare.29892218, raw data per figure.

Twelve workbooks, ~45 panels. Every panel is one of three shapes:

  row-wise    a `Time (hours)` anchor in column B, the grid (0, 1, 3, 5, 7) on
              the row below it, then one row per biological replicate with the
              condition named in column A on the first of them. The deposit says
              so itself, at the top of every sheet: "Note: Each row in each
              table is a separate biological replicate."
  column-wise a `Time (hour)` anchor in column A with the condition named in
              column B, time running down column A and one replicate per column
              (S4_Fig only, which is OD600).
  untimed     Fig4, where column groups are named two rows above and the
              quantity is named in column A ("CFU/mL relative to 0 uM IPTG",
              "Survival Fraction").

THE THING THAT MATTERS ABOUT THIS DEPOSIT: there is not one absolute count in
it. Every time-kill panel is a surviving fraction normalised to its own t = 0,
which is written as 1. The denominator -- the count at t = 0 -- appears nowhere
in any of the twelve files, so no row here can be turned into CFU/mL and none is:
cfu_per_ml, colonies, dilution and plated_volume_ul are blank on every row.

That leaves the schema with nowhere to put the number, because it has no column
for a value that is not a count. Rather than drop the readings, each row carries
its value in notes with a `value=` prefix and names the quantity in readout, so
the reading survives and cannot be mistaken for a count. All 12 files and every
panel in them are covered; nothing in this deposit is left unread.

Fractions in the deposit reach 8.3e-07, which implies a starting population
around 1e6 to 1e7 and a floor well below it -- but that is arithmetic on an
unstated denominator, so floor_cfu_per_ml stays blank and floor_basis says why.

WHAT THE DEPOSIT DOES SAY and is recorded:

  * strain, from the condition labels: PAO1, MG1655, MRSN 1612 and their
    mutants. The species is never named, so organism stays blank.
  * the drug, in exactly three places -- S6_Fig, whose labels read
    "+ 10 ug/mL CIP", "+ 2 ug/mL CIP", "+ 1.25 ug/mL CIP", and Fig4 sheet C,
    which contrasts "CIP" with "Control". Every other panel names no drug, and
    those rows have drug blank even though the deposit is a ciprofloxacin
    persister study, because the panel itself does not say it.
  * time in hours, as the headers state.

WHAT THE DEPOSIT DOES NOT SAY, AND WHICH THIS READER WORKS OUT AND MARKS: the
same cultures are printed under several panels. 239 of the 611 series returned
here -- 1,255 of the 3,203 rows -- are value-for-value reprints of a series that
appears earlier in the deposit. The fifteen `PAO1 WT Survival Fractions`
replicates of Fig1 sheet A come back in Fig2/A, Fig3/A, S1_Fig/A (relabelled
`PAO1 WT (Parent)`), S2_Fig/A, S2_Fig/B, S5_Fig/A and S5_Fig/B; the three
`MG1655 WT OD600 measurements` of S4_Fig sheet C come back on sheet E as
`MG1655 WT in succinate` and on sheet G as `MG1655 WT with pregrowth`. Nothing on
any sheet says so, and two of those reprints carry a different label from the
original, so a label-based check would not find them. Every reprint is kept --
the panels are reprints, not errors, and the deposit does not say which copy is
primary -- but each one says in notes which earlier series it duplicates, so
that a model fitted on this deposit is not handed eight copies of one control as
eight independent experiments.
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import openpyxl
import pandas as pd

from src.ingest import empty, finish

STUDY = "LEON2025"

TIME_ANCHOR = re.compile(r"^\s*time\s*\(\s*hours?\s*\)\s*$", re.I)
STRAIN = re.compile(r"^\s*(PAO1|MG1655|MRSN\s*\d+)\b", re.I)
# "PAO1 DrecA + 10 ug/mL CIP Survival Fractions"
DOSE = re.compile(r"\+\s*([0-9]+(?:\.[0-9]+)?)\s*([µμu]g\s*/\s*m[lL])\s*"
                  r"([A-Za-z]+)", re.U)
TRAILING = re.compile(r"\s*(survival fractions?|od600 measurements?)\s*$", re.I)

FLOOR_BASIS = ("no plated volume, dilution or limit of detection in the "
               "deposit; the panels are normalised fractions, so no count is "
               "available to compare a floor with")
NO_DENOM = ("reported only as a fraction of its own t=0; the deposit gives no "
            "count at t=0, so this reading cannot be turned into CFU/mL")


def _num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip())
        except ValueError:
            return None
    return None


def _txt(v) -> str:
    return "" if v is None else str(v).replace("\xa0", " ").strip()


def _condition(label: str) -> tuple[str, str, float | None, str]:
    """label -> (arm, strain, concentration, conc_unit), reading only."""
    arm = TRAILING.sub("", label).strip()
    m = STRAIN.match(arm)
    strain = m.group(1).strip() if m else ""
    d = DOSE.search(arm)
    if d:
        return arm, strain, float(d.group(1)), d.group(2).replace(" ", "")
    return arm, strain, None, ""


def _drug(label: str) -> str:
    d = DOSE.search(label)
    if d:
        return d.group(3)
    if re.search(r"\bCIP\b", label):
        return "CIP"
    return ""


def _grid(ws):
    g = {}
    for row in ws.iter_rows():
        for cell in row:
            g[(cell.row, cell.column)] = cell.value
    return g


def _row_wise(g, ws, r, c, src, sheet, bi, panel):
    """Anchor in column B: time grid on the next row, replicates below it."""
    cols = []
    cc = c
    while cc <= ws.max_column:
        t = _num(g.get((r + 1, cc)))
        if t is None:
            break
        cols.append((cc, t))
        cc += 1
    if not cols:
        return []

    label, rows = "", []
    rr = r + 2
    while rr <= ws.max_row:
        if TIME_ANCHOR.match(_txt(g.get((rr, c)))) or \
           TIME_ANCHOR.match(_txt(g.get((rr, 1)))):
            break
        if not label:
            label = _txt(g.get((rr, 1)))
        if all(_num(g.get((rr, cc))) is None for cc, _ in cols):
            break
        rows.append(rr)
        rr += 1
    if not label or not rows:
        return []

    arm, strain, conc, unit = _condition(label)
    drug = _drug(label)
    out = []
    for i, rr in enumerate(rows, 1):
        for cc, t in cols:
            v = _num(g.get((rr, cc)))
            if v is None:
                continue
            out.append({
                "source_file": src, "sheet": sheet, "organism": "",
                "strain": strain, "drug": drug, "concentration": conc,
                "conc_unit": unit, "arm": arm,
                "replicate": f"{panel}-{sheet}-b{bi}-rep{i}",
                "tech_replicate": "",
                "time_h": t, "readout": "CFU (surviving fraction only)",
                "floor_basis": FLOOR_BASIS, "_v": v,
                "notes": (f"value={v!r} surviving fraction; {NO_DENOM}; "
                          f"source time in hours; panel label {label!r}"),
            })
    return out


def _column_wise(g, ws, r, src, sheet, bi, panel):
    """Anchor in column A: time runs down, one replicate per column."""
    label = _txt(g.get((r, 2)))
    if not label:
        return []
    rows = []
    rr = r + 1
    while rr <= ws.max_row:
        t = _num(g.get((rr, 1)))
        if t is None:
            break
        rows.append((rr, t))
        rr += 1
    cols = [cc for cc in range(2, ws.max_column + 1)
            if any(_num(g.get((rr, cc))) is not None for rr, _ in rows)]
    if not rows or not cols:
        return []

    arm, strain, conc, unit = _condition(label)
    drug = _drug(label)
    readout = "OD600" if re.search(r"od\s*600", label, re.I) else ""
    out = []
    for i, cc in enumerate(cols, 1):
        for rr, t in rows:
            v = _num(g.get((rr, cc)))
            if v is None:
                continue
            out.append({
                "source_file": src, "sheet": sheet, "organism": "",
                "strain": strain, "drug": drug, "concentration": conc,
                "conc_unit": unit, "arm": arm,
                "replicate": f"{panel}-{sheet}-b{bi}-rep{i}",
                "tech_replicate": "",
                "time_h": t, "readout": readout,
                "floor_basis": FLOOR_BASIS, "_v": v,
                "notes": (f"value={v!r} {readout or 'quantity not named'}; "
                          f"the schema has no column for a non-count value, so "
                          f"it is kept here; source time in hours; "
                          f"panel label {label!r}"),
            })
    return out


def _untimed(g, ws, r, src, sheet, panel):
    """Fig4: quantity named in column A, column groups named two rows above."""
    quantity = _txt(g.get((r, 1)))
    heads = {}
    for cc in range(2, ws.max_column + 1):
        parts = [_txt(g.get((rr, cc))) for rr in (r - 2, r - 1)]
        parts = [p for p in parts if p]
        if parts:
            heads[cc] = " ".join(parts)
    if not heads:
        return []
    axis = _txt(g.get((r - 3, 2)))

    rows = [rr for rr in range(r, ws.max_row + 1)
            if any(_num(g.get((rr, cc))) is not None for cc in heads)]
    out = []
    for cc, head in heads.items():
        i = 0
        for rr in rows:
            v = _num(g.get((rr, cc)))
            if v is None:
                continue
            i += 1
            out.append({
                "source_file": src, "sheet": sheet, "organism": "",
                "strain": "", "drug": _drug(head), "concentration": None,
                "conc_unit": "",
                "arm": head, "replicate": f"{panel}-{sheet}-c{cc}-rep{i}",
                "tech_replicate": "", "time_h": None,
                "readout": ("CFU (ratio to control only)"
                            if "cfu" in quantity.lower()
                            else "CFU (surviving fraction only)"),
                "floor_basis": FLOOR_BASIS, "_v": v,
                "notes": (f"value={v!r} {quantity!r}; {NO_DENOM}; this panel "
                          f"has no time axis; column axis {axis!r}"
                          + (f"; the number in the column heading is an "
                             f"inducer level on that axis, not a drug dose, so "
                             f"it is not put in concentration"
                             if re.search(r"iptg", axis, re.I) else "")),
            })
    return out


def read(d: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(d.glob("*.xlsx")):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wb = openpyxl.load_workbook(path, data_only=True)
        panel = re.sub(r"^Raw_Data_", "", path.stem)
        for ws in wb.worksheets:
            g = _grid(ws)
            bi = 0
            for r in range(1, ws.max_row + 1):
                for c in range(1, min(ws.max_column, 3) + 1):
                    if not TIME_ANCHOR.match(_txt(g.get((r, c)))):
                        continue
                    bi += 1
                    got = (_column_wise(g, ws, r, path.name, ws.title, bi, panel)
                           if c == 1 else
                           _row_wise(g, ws, r, c, path.name, ws.title, bi, panel))
                    rows.extend(got)
                    break
            if bi == 0:                     # no time axis: the Fig4 shape
                for r in range(1, ws.max_row + 1):
                    q = _txt(g.get((r, 1)))
                    if q and re.search(r"cfu|fraction", q, re.I) and r >= 3:
                        rows.extend(_untimed(g, ws, r, path.name, ws.title, panel))
                        break
    if not rows:
        return empty()
    _flag_reprinted_series(rows)
    for r in rows:
        r.pop("_v", None)
    return finish(pd.DataFrame(rows), STUDY)


def _flag_reprinted_series(rows: list[dict]) -> None:
    """Mark every series that is a verbatim reprint of an earlier one.

    This deposit prints the same control cultures under several figure panels:
    the fifteen `PAO1 WT Survival Fractions` replicates of Fig1 sheet A appear
    again, value for value, in Fig2/A, Fig3/A, S1_Fig/A (relabelled `PAO1 WT
    (Parent)`), S2_Fig/A, S2_Fig/B, S5_Fig/A and S5_Fig/B. Nothing on the sheets
    says so. Left unmarked they would enter the corpus as eight independent
    experiments and collapse the between-experiment variance they are the best
    evidence for, which is the same failure the NOREL2023 / SALMONELLA2023
    duplicate check exists to prevent -- only inside one deposit rather than
    across two.

    Nothing is dropped: the panels are reprints, not errors, and which copy is
    the "real" one is not stated. The first occurrence in file-then-sheet order
    is left clean and every later copy says in notes where it was already seen,
    so a downstream analysis can keep one per group.
    """
    seen: dict[tuple, str] = {}
    order: list[tuple] = []
    series: dict[tuple, list[dict]] = {}
    for r in rows:
        key = (r["source_file"], r["sheet"], r["replicate"])
        if key not in series:
            series[key] = []
            order.append(key)
        series[key].append(r)

    for key in order:
        rs = series[key]
        sig = tuple(sorted((r["time_h"], r["_v"]) for r in rs
                           if r["_v"] is not None))
        if len(sig) < 3:                    # too short to identify anything
            continue
        first = seen.get(sig)
        if first is None:
            seen[sig] = f"{key[0]}/{key[1]}/{key[2]}"
            continue
        for r in rs:
            r["notes"] += (
                f"; DUPLICATE: this series is value-for-value identical to "
                f"{first}, which the deposit prints earlier -- the same culture "
                f"reported under more than one panel, so do not count both")
