"""PZA_PARP1_2023 -- Nature Communications 2023 (41467_2023_43937), Source Data.xlsx.

WHAT THIS DEPOSIT IS, AND WHAT IT IS NOT.

  It is a 15-sheet GraphPad-export workbook for a mouse study of pyrazinamide
  and the host enzyme PARP1.  Most of it is biochemistry: melting curves,
  western blots, Luminex cytokines, histology.  Six panels carry viable counts
  and are read here:

      Fig 4  / "Figure 4 b"              lung CFU, end of treatment, C3HeB/FeJ
      Fig 5  / "Figure 5 b"              lung CFU, end of treatment, WT vs PARP1-/-
      Fig 6  / "Figure 6 b"              lung CFU, DAY 1 post infection
      Fig 6  / "Figure 6 c"              lung CFU, start of treatment
      Fig 6  / "Figure 6 d"              lung CFU, end of treatment
      Fig S3 / "Supplementary Fig. 3 c"  lung CFU at treatment start

  It is NOT a time-kill deposit.  There is no in vitro kill curve anywhere in
  the workbook, and no panel is a series of counts through treatment.  What the
  deposit gives is a cross-sectional endpoint per mouse: different animals are
  killed at each stage, and only the Figure 6 experiment has more than one
  stage.  Every row here is one mouse, one lung, one plating.

  THE TIME AXIS IS MOSTLY MISSING, and that is a finding, not an oversight of
  this reader.  Two cells in the whole workbook state an absolute time, and
  neither gives a treatment duration: Figure 6 b's title, "CFU - DAY 1 post
  infection", and Supplementary Fig. 3 a's, "Uncropped Western blots (PAR,
  b-Actin at the start of treatment / 1 month post infection)".  That month is
  stated for the Supplementary Fig. 3 mice and for no others.  Nowhere does the
  workbook say how long treatment lasted.  So:

      * "Start of treatment" (Figure 6 c) and "at treatment start"
        (Supplementary Fig. 3 c) are time_h = 0 -- treatment begins there.
      * "End of treatment" (Figures 4 b, 5 b, 6 d) has NO time_h.  The elapsed
        hours are not stated and are not inferred; the notes say so on every
        such row.
      * "DAY 1 post infection" (Figure 6 b) is a pre-treatment reading taken
        one day after infection; how long after infection this experiment's
        treatment began is not stated anywhere in the workbook.  It is not time
        zero of treatment, so it carries no time_h either, and its notes say
        what it is.  It is kept rather than dropped because it is a real plate
        count and the schema has no way to express a negative time.

  THE FLOOR IS NOT STATED, ANYWHERE.  No cell in the workbook gives a detection
  limit, a plated volume, a dilution or a homogenate volume for any CFU panel.
  The only "limit of detection" text in the file (Fig 5 r24, Fig S10 r24)
  concerns the multiplex cytokine ELISA -- IL-12 and IL-10 in pg/ml -- and says
  nothing about plate counts.  floor_cfu_per_ml is therefore blank on every row
  and floor_basis records exactly that.

  WHICH MATTERS HERE, because Figure 4 b's RIF + PZA arm reports SIX OF TEN
  mice as exactly 0 in a column headed "Lung bacterial burden (log10 CFU)".
  Taken at face value, 0 on that scale is one colony per lung; it is at least
  as likely to be the depositor's placeholder for no colonies recovered.  The
  deposit never says which, and with no stated limit there is nothing to check
  it against.  The zeros are demonstrably treated as ordinary log10 numbers by
  the depositor's own arithmetic: the mean of that arm's ten values, zeros
  included, is 0.48356, and Supplementary Fig. 6 a reports the RIF + PZA mean
  as 0.4836 +/- 0.2524.  This reader records cfu_per_ml = 10**value throughout,
  which puts those six lungs at 1 CFU, and flags every one of them in notes.
  No row is marked censored, because censoring cannot be established without a
  floor -- and carrying that absence forward is the point.

WHAT IS DELIBERATELY LEFT OUT.

  * "Figure 3 d" is headed "CFU fold change" and its Vehicle column sums to
    zero: it is a normalised fold change, not a count.  It is also not new
    data -- every one of its 33 values is a Figure 4 b log10 CFU from the same
    arm minus a single constant, 7.3873613 (checked; largest residual 4.3e-6,
    the deposit's own rounding) -- so reading it would double-count as well.
  * "Supplementary Fig. 4 b-e" list lung CFU (log10) again for the mice that
    also had PAR measured.  Every value is a duplicate of a Figure 4 b value
    (checked to 1e-5; the deposit writes 8.575483 in one place and 8.575484 in
    the other).  Reading them would double-count mice, so they are skipped.
  * "Supplementary Fig. 6 a" holds the Figure 4 b group mean and SEM on its
    left, and on its right all sixty per-mouse Figure 4 b log10 CFU values
    again (every one checked identical).  Reading it would double-count the
    same mice, so it is skipped.

OTHER THINGS THE DEPOSIT DOES NOT SAY, left blank rather than filled.

  * No dose and no concentration for PZA, RIF or Tp -- concentration and
    conc_unit are blank on every row.
  * The workbook never expands its abbreviations.  PZA, RIF and Tp are carried
    verbatim into `drug`, and "M.tb" verbatim into `organism`.  Supplementary
    Fig. 3 c's title names neither organism nor strain: its strain is left
    blank, and its "M.tb" is carried from the workbook's other CFU panel
    titles, which the notes on those five rows say outright.
  * The deposit never names or numbers its animals.  Mice are numbered by
    position within their block and the Excel cell address of every reading is
    carried in notes, so a number here is this reader's index, not the
    depositor's.
  * cfu_per_ml holds a count PER LUNG, not per mL.  The deposit gives no
    homogenate volume, so no conversion is possible or attempted, and every
    row's notes say the column is a misnomer here.
  * Where a value carries a trailing asterisk the sheet's own footnote reads
    "*outlier removed from analysis".  The number is kept as a reading -- it was
    measured -- and the flag is recorded in notes.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

REL = "_unpacked/41467_2023_43937_MOESM4_ESM/Source Data.xlsx"

# A cell like "15*": a reading the sheet's footnote says was dropped from the
# statistics.  It is still a reading.
STARRED = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*\*\s*$")
# The panel-id cells that open a block, e.g. "Figure 4 b", "Supplementary Fig. 3 c"
PANEL_ID = re.compile(r"^(Figure|Supplementary Fig\.)\s", re.I)
# "M.tb H37Rv ..." in a panel title, with an optional delta-mutant suffix
STRAIN_RE = re.compile("M\\.tb\\s+(H37Rv(?:\\s*Δ\\s*\\w+)?)", re.I)
# the mouse line, as the titles write it
MOUSE_RE = re.compile(r"in\s+(.+?)\s+mice", re.I)

SEX = {"male", "female"}

FLOOR_BASIS = (
    "no floor: the workbook states no detection limit, plated volume, dilution "
    "or homogenate volume for any CFU panel; its only 'limit of detection' "
    "remark (Fig 5 r24, Fig S10 r24) is about the multiplex cytokine ELISA in "
    "pg/ml, not about plate counts")

ORGAN_NOTE = ("in vivo lung burden: cfu_per_ml holds the count PER LUNG, not "
              "per mL; the deposit gives no homogenate volume so no conversion "
              "is possible")
DOSE_NOTE = "the workbook states no dose or concentration for any arm"
ABBR_NOTE = ('the workbook never expands its abbreviations (PZA, RIF, Tp) or '
             'the organism "M.tb"; all are recorded as written')

END_NOTE = ("end-of-treatment reading; the deposit never states how long "
            "treatment lasted, so hours since treatment began cannot be filled "
            "and time_h is left blank")

# One entry per block of counts.  row_role says what the label in column 0 of a
# data row means, which differs between panels; time_h and its justification come
# from the panel's own title text and nothing else.
PANELS = [
    dict(sheet="Fig 4", anchor="Figure 4 b", row_role="treatment",
         time_h=None, time_note=END_NOTE),
    dict(sheet="Fig 5", anchor="Figure 5 b", row_role="host",
         time_h=None, time_note=END_NOTE),
    dict(sheet="Fig 6", anchor="Figure 6 b", row_role="host", time_h=None,
         time_note="DAY 1 post infection, a pre-treatment reading; the workbook "
                   "nowhere states how long after infection this experiment's "
                   "treatment began, so the gap to time zero is unknown; it is "
                   "not time zero of treatment, and the schema cannot hold a "
                   "negative time, so time_h is blank"),
    dict(sheet="Fig 6", anchor="Figure 6 c", row_role="host", time_h=0.0,
         time_note='time_h = 0 because the panel title reads "CFU - Start of '
                   'treatment"; no drug had been given when these lungs were '
                   "plated"),
    dict(sheet="Fig 6", anchor="Figure 6 d", row_role="host",
         time_h=None, time_note=END_NOTE),
]

# Supplementary Fig. 3 c is transposed -- its rows are quantities and its columns
# are the five mice -- so it is read separately.
S3C = dict(sheet="Fig S3", anchor="Supplementary Fig. 3 c", time_h=0.0,
           time_note='time_h = 0 because the panel title reads "(at treatment '
                     'start)"; Supplementary Fig. 3 a dates that start as "1 '
                     'month post infection", the workbook\'s only statement of '
                     "an infection-to-treatment interval, and it is stated for "
                     "these mice",
           arm="start of treatment")


def _a1(row: int, col: int) -> str:
    """Excel address, for provenance in notes."""
    s, c = "", col
    while True:
        s = chr(ord("A") + c % 26) + s
        c = c // 26 - 1
        if c < 0:
            break
    return f"{s}{row + 1}"


def _value(cell):
    """(number, starred) for a data cell, or (None, False) if it is not one."""
    if isinstance(cell, str):
        m = STARRED.match(cell)
        return (float(m.group(1)), True) if m else (None, False)
    if isinstance(cell, (int, float, np.number)) and np.isfinite(cell):
        return float(cell), False
    return None, False


def _block_end(raw: pd.DataFrame, start: int) -> int:
    for r in range(start + 1, len(raw)):
        v = raw.iat[r, 0]
        if isinstance(v, str) and PANEL_ID.match(v.strip()):
            return r
    return len(raw)


def _anchor(raw: pd.DataFrame, text: str) -> int:
    for r in range(len(raw)):
        v = raw.iat[r, 0]
        if isinstance(v, str) and v.strip() == text:
            return r
    raise ValueError(f"panel {text!r} not found")


def _title(raw: pd.DataFrame, r: int) -> str:
    for c in range(1, raw.shape[1]):
        v = raw.iat[r, c]
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _stop_col(raw: pd.DataFrame, rows: list) -> int:
    """First column of the GraphPad statistics block sitting to the right.

    Data cells are numbers, or numbers with an outlier asterisk; the statistics
    that share the same rows start with a text label, so the leftmost text cell
    across the block's data rows bounds the readings.
    """
    stop = raw.shape[1]
    for r in rows:
        for c in range(1, raw.shape[1]):
            cell = raw.iat[r, c]
            if isinstance(cell, str) and cell.strip() and _value(cell)[0] is None:
                stop = min(stop, c)
                break
    return stop


def _bands(raw: pd.DataFrame, rows: list, stop: int):
    """Column -> sex and column -> treatment, from the label rows above the data.

    A band row whose labels are all Male/Female is a sex band; any other band row
    is the treatment band.  A label applies rightwards until the next one.
    """
    sex, treat = {}, {}
    for r in rows:
        labels = [(c, str(raw.iat[r, c]).strip()) for c in range(1, stop)
                  if isinstance(raw.iat[r, c], str) and str(raw.iat[r, c]).strip()]
        if not labels:
            continue
        target = sex if all(t.lower() in SEX for _, t in labels) else treat
        pos = dict(labels)
        cur = ""
        for c in range(1, stop):
            cur = pos.get(c, cur)
            target[c] = cur
    return sex, treat


def _drug(treatment: str) -> str:
    """The sheet's own arm label as a drug name; blank for a control arm."""
    t = treatment.strip()
    return "" if t.lower() in {"vehicle", "untreated", ""} else t


def _read_panel(raw: pd.DataFrame, spec: dict) -> list:
    a = _anchor(raw, spec["anchor"])
    end = _block_end(raw, a)
    title = _title(raw, a)

    axis = next((r for r in range(a, end)
                 if isinstance(raw.iat[r, 0], str)
                 and "bacterial burden" in str(raw.iat[r, 0]).lower()), None)
    if axis is None:
        raise ValueError(f"{spec['anchor']}: no 'Lung bacterial burden' label")
    axis_label = str(raw.iat[axis, 0]).strip()
    log10_scale = bool(re.search(r"log ?10", axis_label, re.I))

    data_rows = [r for r in range(axis + 1, end)
                 if isinstance(raw.iat[r, 0], str) and str(raw.iat[r, 0]).strip()
                 and any(_value(raw.iat[r, c])[0] is not None
                         for c in range(1, raw.shape[1]))]
    if not data_rows:
        raise ValueError(f"{spec['anchor']}: no data rows")

    stop = _stop_col(raw, data_rows)
    sex, treat = _bands(raw, list(range(a + 1, axis + 1)), stop)

    sm = STRAIN_RE.search(title)
    strain = re.sub(r"\s+", " ", sm.group(1)).strip() if sm else ""
    mm = MOUSE_RE.search(title)
    mouse = mm.group(1).strip() if mm else ""

    out = []
    for r in data_rows:
        label = str(raw.iat[r, 0]).strip()
        n = 0
        for c in range(1, stop):
            v, starred = _value(raw.iat[r, c])
            if v is None:
                continue
            n += 1
            host = label if spec["row_role"] == "host" else ""
            treatment = treat.get(c, "") or (
                label if spec["row_role"] == "treatment" else "")
            arm = ", ".join(x for x in (host, treatment) if x) or label

            note = [f"{spec['anchor']}: {title}",
                    f'the sheet heads this column "{axis_label}"']
            if log10_scale:
                note.append("the sheet reports log10; cfu_per_ml is 10**value")
            if mouse:
                note.append(f"mouse line as the title states it: {mouse}")
            if sex.get(c):
                note.append(f"sex band: {sex[c]}")
            note.append(f"cell {_a1(r, c)}")
            note.append(spec["time_note"])
            if v == 0 and log10_scale:
                note.append("the sheet writes this reading as 0 in a log10 CFU "
                            "column: at face value one colony per lung, but it "
                            "may be a placeholder for no colonies recovered, and "
                            "the deposit says neither which nor any detection "
                            "limit to judge it by")
            elif v == 0:
                note.append("the sheet writes this reading as 0")
            if starred:
                note.append("the sheet writes this value with an asterisk and "
                            'footnotes it "*outlier removed from analysis"; the '
                            "reading is kept here")
            note += [ORGAN_NOTE, DOSE_NOTE, ABBR_NOTE]

            out.append({
                "source_file": REL,
                "sheet": f"{spec['sheet']}: {spec['anchor']}",
                "organism": "M.tb",
                "strain": strain,
                "drug": _drug(treatment),
                "arm": arm,
                "replicate": f"{spec['anchor']} | {arm}"
                             + (f" | {sex[c]}" if sex.get(c) else "")
                             + f" | mouse {n}",
                "time_h": spec["time_h"],
                "cfu_per_ml": 10.0 ** v if log10_scale else v,
                "floor_basis": FLOOR_BASIS,
                "readout": "CFU",
                "notes": "; ".join(note),
            })
    return out


def _read_s3c(raw: pd.DataFrame, spec: dict) -> list:
    """Supplementary Fig. 3 c: rows are quantities, columns are the mice."""
    a = _anchor(raw, spec["anchor"])
    end = _block_end(raw, a)
    title = _title(raw, a)

    row = next((r for r in range(a, end)
                if isinstance(raw.iat[r, 0], str)
                and "cfu" in str(raw.iat[r, 0]).lower()), None)
    if row is None:
        raise ValueError(f"{spec['anchor']}: no CFU row")
    label = str(raw.iat[row, 0]).strip()            # "CFU (log10)"
    log10_scale = bool(re.search(r"log ?10", label, re.I))
    stop = _stop_col(raw, [row])

    out, n = [], 0
    for c in range(1, stop):
        v, starred = _value(raw.iat[row, c])
        if v is None:
            continue
        n += 1
        note = [f"{spec['anchor']}: {title}",
                f'the sheet labels this row "{label}"']
        if log10_scale:
            note.append("the sheet reports log10; cfu_per_ml is 10**value")
        note.append(f"cell {_a1(row, c)}")
        note.append(spec["time_note"])
        note.append("these five mice are the infected animals whose PAR levels "
                    'Supplementary Fig. 3 b lists as "Infected": the PAR row of '
                    "this same block repeats those five values exactly")
        # This panel's title names no organism, so say where "M.tb" came from
        # rather than let it look like the panel's own word.
        note.append("this panel's title names neither organism nor strain: "
                    'strain is left blank, and organism "M.tb" is carried from '
                    "the titles of the workbook's other CFU panels, not from "
                    "this one")
        if starred:
            note.append("the sheet writes this value with an asterisk "
                        '("*outlier removed from analysis"); it is kept here')
        if v == 0:
            note.append("the sheet writes this reading as 0")
        note += [ORGAN_NOTE, DOSE_NOTE, ABBR_NOTE]

        out.append({
            "source_file": REL,
            "sheet": f"{spec['sheet']}: {spec['anchor']}",
            "organism": "M.tb",
            "strain": "",           # this panel's title names no strain
            "drug": "",             # no drug given at the start of treatment
            "arm": spec["arm"],
            "replicate": f"{spec['anchor']} | {spec['arm']} | mouse {n}",
            "time_h": spec["time_h"],
            "cfu_per_ml": 10.0 ** v if log10_scale else v,
            "floor_basis": FLOOR_BASIS,
            "readout": "CFU",
            "notes": "; ".join(note),
        })
    return out


def read(d: Path) -> pd.DataFrame:
    src = d / REL
    if not src.exists():
        return empty()

    book = pd.ExcelFile(src)
    rows = []
    for spec in PANELS:
        rows += _read_panel(book.parse(sheet_name=spec["sheet"], header=None),
                            spec)
    rows += _read_s3c(book.parse(sheet_name=S3C["sheet"], header=None), S3C)

    return finish(pd.DataFrame(rows), "PZA_PARP1_2023")
