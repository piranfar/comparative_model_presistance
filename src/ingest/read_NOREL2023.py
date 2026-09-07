"""NOREL2023 -- Zenodo record 10277562, persister time-kill workbooks.

Twelve .xlsx, one per numbered experiment (M7, M13, M14, M18, M19, M20, M28,
M56, M70, M77, M96, M97). Each sheet opens with three free-text header lines in
column A:

    Precultures : grown in LB for 18 h (stationary-phase of growth)
    Medium for persisters : LB
    Antibiotic : ampicillin 100 mg/ml

followed by a strain block (sometimes a two-column `strain number` / `Genotype`
legend, sometimes an unkeyed list of genotypes), then one or more data blocks.
A block is anchored on a cell reading `time (min)` / `TIME (min)`; the column
labels run to its right, a `CFU/ml` unit row usually sits one row above, and the
readings run downwards. Several sheets carry two blocks side by side (M28, M56).
M7 is transposed: `Time (hours)` with the time grid running across the row and
one series per row beneath it.

WHAT THIS DEPOSIT DOES NOT SAY, and is therefore left blank here:

  * organism. No sheet in these twelve files contains the words Salmonella,
    enterica or Typhimurium. `WT=ATCC14028` is a strain designation and is all
    the workbooks give, so organism stays blank and the strain text is recorded
    as written.
  * plated volume, dilution, limit of detection. Nothing of the kind appears in
    any cell of any of the twelve files. The Zenodo record also carries a
    PROTOCOL.pdf which is NOT among the files shipped into this directory, so
    nothing from it is used here. floor_cfu_per_ml is blank.
  * the concentration unit is recorded exactly as the sheet writes it,
    `mg/ml`, even though 100 mg/ml of ampicillin is three orders of magnitude
    above any plausible working concentration. Correcting it would be an
    inference; it is flagged in notes instead.

TWO SMALLER POINTS. The drug name is kept exactly as the sheet spells it, so
`Data M20` contributes 32 rows whose drug reads `ciprofloxaxin`; correcting the
spelling would be an edit to the source, and the corpus can fold it in later if
it wants to. And M96 and M97 each carry two sheets, one per antibiotic, under a
single experiment number, so their replicate ids read `M96/persisters Ampi` and
`M96/persisters cipro` -- those are different cultures and must not collapse
into one series.

ONE INTERPRETIVE CALL, made deliberately and flagged on every row it touches:
sheet `Data M19` labels its time column just `time` and has no `CFU/ml` unit
row, unlike the other eleven workbooks, which use an identical template. Its
minutes-and-CFU/mL reading is taken from that template, every M19 row says so in
notes, and -- so that the caveat survives into a structured column and not only
into free text -- those 32 rows carry readout `CFU (this sheet states no value
unit)` rather than a bare `CFU`. Nothing else in this reader is inferred.

CHECKED AND FOUND ABSENT, cell by cell across all twelve workbooks: the strings
cfu-with-a-volume, dilut*, plate*, micro/ul/µ/μ, detect*, LOD and limit. The only
micro sign anywhere is in the MgSO4 concentrations of the M77 column headings
(`M63 10mM glucose/500μM MgSO4`), which is a medium recipe, not a plated volume.
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import openpyxl
import pandas as pd

from src.ingest import empty, finish

STUDY = "NOREL2023"

TIME_HEADER = re.compile(r"^\s*time\b", re.I)
MINUTES = re.compile(r"\(\s*min", re.I)
HOURS = re.compile(r"\(\s*h(ou)?r?s?", re.I)
# "Antibiotic : ampicillin 100 mg/ml"  ->  name, value, unit
ANTIBIOTIC = re.compile(
    r"^\s*antibiotic\s*:\s*([A-Za-z]+)\s*([0-9]+(?:\.[0-9]+)?)?\s*([A-Za-z/]+)?", re.I)
# M7 block label "AMPI 100"
BLOCK_DRUG = re.compile(r"^\s*([A-Za-z]+)\s+([0-9]+(?:\.[0-9]+)?)\s*$")

FLOOR_BASIS = ("no plated volume, dilution or limit of detection anywhere in "
               "the workbook; the record's PROTOCOL.pdf is not shipped in this "
               "dataset directory and is not used")

M7_ABBREV = {"AMPI": "ampicillin", "CIPRO": "ciprofloxacin"}


def _num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return None
    return None


def _txt(v) -> str:
    if v is None:
        return ""
    return str(v).replace("\xa0", " ").strip()


def _grid(ws) -> list[list]:
    """1-indexed cell grid; grid[r][c] with r, c starting at 1."""
    g = [[None] * (ws.max_column + 2) for _ in range(ws.max_row + 2)]
    for row in ws.iter_rows():
        for cell in row:
            g[cell.row][cell.column] = cell.value
    return g


def _sheet_meta(g: list[list]) -> dict:
    meta = {"preculture": "", "medium": "", "antibiotic": ""}
    for r in range(1, min(len(g), 14)):
        for c in range(1, min(len(g[r]), 4)):
            t = _txt(g[r][c])
            low = t.lower()
            if low.startswith("precultures") and not meta["preculture"]:
                meta["preculture"] = t
            elif low.startswith("medium for persisters") and not meta["medium"]:
                meta["medium"] = t
            elif low.startswith("antibiotic :") and not meta["antibiotic"]:
                meta["antibiotic"] = t
    return meta


def _drug_from_line(line: str) -> tuple[str, float | None, str]:
    """Split 'Antibiotic : ciprofloxacin 5 mg/ml'. Verbatim, no normalising."""
    if " or " in line.lower():          # M7 names both drugs; blocks decide
        return "", None, ""
    m = ANTIBIOTIC.match(line)
    if not m:
        return "", None, ""
    name = (m.group(1) or "").lower()
    val = float(m.group(2)) if m.group(2) else None
    unit = (m.group(3) or "").strip()
    return name, val, unit


def _legend(g: list[list]) -> dict[str, str]:
    """strain-number -> genotype, only where the sheet gives that legend."""
    out: dict[str, str] = {}
    for r in range(1, min(len(g), 30)):
        if _txt(g[r][1]).lower() == "strain number":
            rr = r + 1
            while rr < len(g):
                key, gen = _txt(g[rr][1]), _txt(g[rr][2])
                if not key or not gen:
                    break
                out[key] = gen
                rr += 1
            break
    return out


def _time_headers(g: list[list]) -> list[tuple[int, int, str]]:
    hits = []
    for r in range(1, len(g)):
        for c in range(1, len(g[r])):
            t = _txt(g[r][c])
            if t and TIME_HEADER.match(t):
                hits.append((r, c, t))
    return hits


def _to_hours(value: float, header: str) -> tuple[float | None, str]:
    if MINUTES.search(header):
        return value / 60.0, "source time in minutes"
    if HOURS.search(header):
        return value, "source time in hours"
    return None, "source gives no time unit"


def _header_note(meta: dict) -> str:
    """The sheet's own three header lines, compactly, plus the unit caveat."""
    bits = []
    if meta["antibiotic"]:
        bits.append(meta["antibiotic"].replace("Antibiotic :", "abx:").strip())
    if meta["medium"]:
        bits.append(meta["medium"].replace("Medium for persisters :", "medium:").strip())
    if meta["preculture"]:
        bits.append(meta["preculture"].replace("Precultures :", "preculture:").strip())
    bits.append("concentration and its unit are verbatim from the sheet")
    return " | ".join(bits)


def _rows_column_block(g, r, c, header, meta, legend, src, sheet, rep, m19):
    """Labels run right of the anchor; readings run down."""
    labels: list[tuple[int, str]] = []
    cc = c + 1
    while cc < len(g[r]) and _txt(g[r][cc]):
        labels.append((cc, _txt(g[r][cc])))
        cc += 1
    if not labels:
        return [], 0

    units = {cc: _txt(g[r - 1][cc]) if r - 1 >= 1 else "" for cc, _ in labels}
    drug, conc, unit = _drug_from_line(meta["antibiotic"])
    header_note = _header_note(meta)

    out, skipped = [], 0
    rr = r + 1
    while rr < len(g):
        t_raw = _num(g[rr][c])
        if t_raw is None:
            break
        t_h, t_note = _to_hours(t_raw, header)
        if t_h is None and m19:
            t_h, t_note = t_raw / 60.0, ("time unit not stated on this sheet; "
                                         "read as minutes from the template the "
                                         "other 11 workbooks of this deposit use")
        for cc, label in labels:
            v = _num(g[rr][cc])
            if v is None:
                if _txt(g[rr][cc]):
                    skipped += 1
                continue
            unit_txt = units.get(cc, "")
            if unit_txt.lower().replace(" ", "") == "cfu/ml":
                is_count, readout, val_note = True, "CFU", ""
            elif m19:
                # The sheet omits the unit row the other eleven workbooks carry.
                # The value is kept, but readout says so, so that a downstream
                # filter on readout == "CFU" does not pick it up unnoticed.
                is_count = True
                readout = "CFU (this sheet states no value unit)"
                val_note = ("no value unit on this sheet; read as CFU/mL from "
                            "the template the other 11 workbooks of this "
                            "deposit use")
            else:
                is_count, readout = False, ""
                val_note = "value unit not stated on this sheet"
            strain = ""
            first = label.split()[0] if label.split() else ""
            if first in legend:
                strain = legend[first]
            note = "; ".join(x for x in [
                t_note, val_note, header_note,
                "" if strain else "arm label carries strain and condition "
                                  "together and the sheet gives no key for it",
            ] if x)
            out.append({
                "source_file": src, "sheet": sheet, "organism": "", "strain": strain,
                "drug": drug, "concentration": conc, "conc_unit": unit,
                "arm": label, "replicate": rep, "tech_replicate": "",
                "time_h": t_h, "cfu_per_ml": v if is_count else None,
                "readout": readout, "floor_basis": FLOOR_BASIS, "notes": note,
            })
        rr += 1
    return out, skipped


def _rows_transposed_block(g, r, c, header, meta, src, sheet, rep, stop_at, last_head):
    """M7: the time grid runs across the anchor row, one series per row below."""
    times: list[tuple[int, float]] = []
    cc = c + 1
    while cc < len(g[r]):
        v = _num(g[r][cc])
        if v is None:
            break
        times.append((cc, v))
        cc += 1
    if not times:
        return [], 0, last_head

    # What the label columns left of the anchor are called. A repeated block
    # leaves them blank, so the last row that named them stands.
    header_note = _header_note(meta)
    head = dict(last_head)
    for k in range(1, c):
        if _txt(g[r][k]):
            head[k] = _txt(g[r][k])
    out, skipped = [], 0
    rr = r + 1
    while rr < len(g) and rr < stop_at:
        unit_txt = _txt(g[rr][c])
        if not unit_txt:
            break
        parts = [(k, _txt(g[rr][k])) for k in range(1, c) if _txt(g[rr][k])]
        if not parts:
            break
        arm = " | ".join(v for _, v in parts)

        drug, conc, unit = "", None, ""
        for k, v in parts:
            m = BLOCK_DRUG.match(v)
            if m and m.group(1).upper() in M7_ABBREV:
                drug = M7_ABBREV[m.group(1).upper()]
                conc = float(m.group(2))
                um = re.search(r"\(([^)]*)\)", head.get(k, ""))
                unit = um.group(1).strip() if um else ""
        is_count = unit_txt.lower().replace(" ", "") == "cfu/ml"
        readout = "CFU" if is_count else ""
        for cc, t_raw in times:
            v = _num(g[rr][cc])
            if v is None:
                if _txt(g[rr][cc]):
                    skipped += 1
                continue
            t_h, t_note = _to_hours(t_raw, header)
            note = "; ".join(x for x in [
                t_note, header_note,
                "" if readout else f"value unit on the sheet is {unit_txt!r}",
            ] if x)
            out.append({
                "source_file": src, "sheet": sheet, "organism": "", "strain": "",
                "drug": drug, "concentration": conc, "conc_unit": unit,
                "arm": arm, "replicate": rep, "tech_replicate": "",
                "time_h": t_h, "cfu_per_ml": v if is_count else None,
                "readout": readout, "floor_basis": FLOOR_BASIS, "notes": note,
            })
        rr += 1
    return out, skipped, head


def read(d: Path) -> pd.DataFrame:
    rows, skipped = [], 0
    for path in sorted(d.glob("*.xlsx")):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wb = openpyxl.load_workbook(path, data_only=True)
        src = path.name
        exp = path.stem.split("_")[0]          # M13, M96, ...
        m19 = exp.upper() == "M19"
        multi = len(wb.worksheets) > 1
        for ws in wb.worksheets:
            # M96 and M97 put ampicillin and ciprofloxacin on separate sheets of
            # one experiment: different cultures, so different replicate ids.
            rep = f"{exp}/{ws.title}" if multi else exp
            g = _grid(ws)
            meta = _sheet_meta(g)
            legend = _legend(g)
            anchors = _time_headers(g)
            last_head: dict[int, str] = {}
            for i, (r, c, header) in enumerate(anchors):
                nxt = next((rr for rr, _, _ in anchors[i + 1:] if rr > r), len(g))
                right = _num(g[r][c + 1]) if c + 1 < len(g[r]) else None
                below = _num(g[r + 1][c]) if r + 1 < len(g) else None
                if right is not None and below is None:
                    got, sk, last_head = _rows_transposed_block(
                        g, r, c, header, meta, src, ws.title, rep, nxt, last_head)
                else:
                    got, sk = _rows_column_block(
                        g, r, c, header, meta, legend, src, ws.title, rep, m19)
                rows.extend(got)
                skipped += sk

    if not rows:
        return empty()
    df = pd.DataFrame(rows)
    if skipped:
        df["notes"] = df["notes"] + f"; {skipped} non-numeric data cell(s) in this deposit were skipped"
    return finish(df, STUDY)
