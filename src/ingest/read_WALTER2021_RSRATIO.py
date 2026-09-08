"""WALTER2021_RSRATIO -- Nature Communications Source Data, PMC8131613.

THE DEPOSIT IS THE ZIP, NOT JUST THE WORKBOOK.  PROVENANCE.json records one
downloaded file, PMC8131613_supplementary.zip, and that archive holds the
Source Data workbook (41467_2021_22833_MOESM4_ESM.xlsx), the six main-text
figure images, and three PDFs -- among them the Supplementary Information,
41467_2021_22833_MOESM1_ESM.pdf.  Only the xlsx was ever unpacked into
_unpacked/, and an earlier pass of this reader looked no further and recorded
"no floor" for the in vitro series on the strength of it.  That was wrong: the
Supplementary Information states a detection limit as a number, and this reader
now opens the PDF (from _unpacked/ if it is there, otherwise straight out of the
zip) and PARSES the number rather than trusting any note.  If the PDF cannot be
read, the floors it carries go blank and say why; nothing is hard-coded.

Ten sheets, of which seven carry viable counts: one in vitro time-kill series
(5 drugs plus a day-0 control, up to 9 sampling times), one in vitro
resistant-mutant series, and five BALB/c mouse experiments reporting CFU per
LUNG.  Three sheets carry no counts at all and are not read: 'Fig 1b & Sup
Fig 1a' (RS ratio and growth rate in an oxygen-depletion model), 'Fig 6a' and
'Fig 6b' (rRNA synthesis ratio and rifampin AUC in patient sputum).

WHAT THE DEPOSIT SAYS, AND WHAT IT DOES NOT

  * ORGANISM.  The workbook never names it -- its whole shared-string table
    contains no species and no strain.  The Supplementary Information PDF does,
    in its title: "Mycobacterium tuberculosis precursor rRNA as a measure of
    treatment-shortening activity of drugs and regimens", and its Supplementary
    Fig. 1b legend calls the CFU-per-lung column of sheet 'Fig 1c & Sup Fig 1b'
    the "Mtb burden".  `organism` is filled from that parse and is blank if the
    parse fails.  NO STRAIN is named anywhere in the deposit, so `strain` stays
    blank on every row.

  * CONCENTRATION IS NEVER GIVEN.  The in vitro arms are labelled only RIF, INH,
    STR, EMB, BDQ; the mouse arms carry a bare number ("RIF 10", "STR 200",
    "PZA 150 + RIF 10") whose unit the workbook never states.  A mouse dose is
    not a concentration in any case, so `concentration` and `conc_unit` are
    blank throughout and the label survives verbatim in `arm`.  The drug
    abbreviations and the regimen codes (2HRZE/3HR, PaMZ, BPaL, BPaMZ, HRZE) are
    expanded nowhere in the deposit and are passed through unexpanded.

  * IN VIVO COUNTS ARE PER LUNG, NOT PER mL.  Sheets 'Fig 1c', 'Fig 4a-c',
    'Fig 5a-d', 'Sup Fig 8b' and 'Sup Fig 11' head their count column "CFU per
    lung".  The value goes in cfu_per_ml because the schema has no per-organ
    column, and `readout` on every one of those rows says the denominator is a
    whole lung.  No volume is invented to convert it.  (The published Fig. 4c
    labels its axis "CFU/ml" for the same numbers the workbook heads "CFU per
    lung"; the workbook's own header is what this reader follows.)

  * NO PLATED VOLUME AND NO DILUTION, anywhere in the workbook or the PDFs.  No
    floor here is derived by arithmetic from a volume; every one is stated.

FLOORS, AND THE RULE USED TO SCOPE THEM.  The deposit states a detection limit
in words for two of its seven count columns, and merely marks individual
below-limit cells in three others.  Those are different facts and are recorded
differently:

  A LEGEND THAT NAMES A LIMIT scopes to the assay it describes.
    - IN VITRO, both CFU-per-mL columns ('Fig 3a-e & Sup Fig 5' and 'Sup Fig
      5g-j'): the Supplementary Information's legend to Supplementary Fig. 5 g-j
      ends "The dashed line represents the limit of detection (13 CFU ml-1)."
      That legend covers panels g-j, which plot total plateable and resistant
      bacteria for rifampin, bedaquiline, isoniazid and streptomycin.  The
      deposit runs one in vitro CFU-per-mL plating and states no other limit for
      it, so 13 CFU/mL is applied to every in vitro reading, the ethambutol arm
      and the day-0 control included, and floor_basis says so on each row.
    - 'Fig 4a-c & Sup Fig 7-8', RESISTANT column: the Supplementary Fig. 8a
      legend says "CFU of <2.18 indicates the lower level of detection" -- the
      deposit's own statement that the "< 2.18" cells mark a detection limit,
      not just a bound.  The value recorded is 150 CFU per lung, not 10**2.18:
      the sheet writes its smallest detected value as 2.176091259, which is
      log10(150) to every digit it prints, and every other detected value in the
      column is log10 of an exact multiple of 150 (300, 600, 750, 1200, 1500,
      2250, 2700, 4500) -- one colony is 150 CFU per lung and 2.18 is that,
      rounded.  It is NOT carried to the total-CFU column of the same sheet: the
      legend scopes it to "Drug resistant CFU", a different plating on
      drug-containing plates, and that column's smallest value is 630.

  A BARE "<x" CELL WITH NO SUCH SENTENCE bounds THAT CELL and no other.  Sheets
  'Fig 5a-d' ("<3.26"), 'Sup Fig 8b' ("<1.6") and 'Sup Fig 11' ("<0.88",
  "< 0.88") carry markers that no legend in the deposit explains, so the bound
  is parsed from the cell and recorded on the cell.  Readings that carry a
  number get NO floor and say why.  This is the convention the sister deposit's
  reader (read_DIDEAGOSSOU2022, the same relapsing-mouse experiment, whose cells
  read "<3.26086956521739") argues for at length, and 'Fig 5a-d' shows why it is
  right: its counts mix granularities -- some are exact multiples of 3.26 and
  others of 7.5 -- so the one-colony equivalent varies from mouse to mouse and
  3.26 is not shown to be the column's floor.  An earlier pass of this reader
  put 3.26 on all 335 of that sheet's rows, 7.59 on all 24 of 'Sup Fig 11' and
  39.8 on all 12 of 'Sup Fig 8b'.  Those fills are removed.

  NO MARKER AND NO SENTENCE, so nothing at all: 'Fig 1c' (CFU per lung) and the
  total-CFU column of 'Fig 4a-c'.

BELOW-LIMIT READINGS carry no number in this workbook -- "<3.26" says only that
the count was under 3.26.  Those rows keep cfu_per_ml BLANK, are marked
censored = yes, and carry the bound as their floor; a censored-data model has
everything it needs and nothing has been made up.  The one place the deposit
writes a bare 0 is the resistant column of 'Sup Fig 5g-j', a log10 column: a 0
there is either 10**0 = 1 CFU/mL or "none detected" and the sheet does not say
which, so no count is recorded -- but BOTH readings of the cell lie under the
stated 13 CFU/mL, so those 29 readings are marked censored = yes on that
ground, with the ambiguity in notes.  Two cells of the same column are written
as DETECTED values that are themselves below the stated limit (0.82 and
0.8239 log10, i.e. 6.6 and 6.7 CFU/mL); they are recorded as written and the
discrepancy is noted.

TIME.  Each sheet gets its own conversion and each row says which was used.
  * 'Fig 3a-e' and 'Sup Fig 5g-j': "Treatment days" x 24 (day 0.25 = 6 h).
  * 'Fig 4a-c': treated rows are 28 days of treatment = 672 h.  This sheet's two
    time columns swap meaning between its baseline and its treated rows -- the
    baseline arms read (1, 0) and (11, 0), matching their own labels "Day 1 post
    infection" and "Pre-Rx", while the treated arms read (28, 39) with
    39 = 11 + 28.  'Sup Fig 11' prints the same pair of columns under the
    opposite headers, which is how the pairing was settled.
  * 'Fig 5a-d': "Day of sacrifice" x 24, counted from treatment start (checked
    across the sheet: it equals "Days of treatment" on and at end of treatment,
    and "Days of treatment" + 84 at relapse assessment, the 12-week holiday).
  * 'Sup Fig 8b': its caption says 28-day treatment and every row shares
    "Day of sacrifice" 53, so all rows are 672 h.
  * 'Sup Fig 11': from the arm label, "(4 weeks)" = 672 h, "(8 weeks)" = 1344 h.
  * 'Fig 1c': untreated animals only.  time_h there is hours after AEROSOL
    INFECTION, not after drug exposure, and every row says so.
  Four kinds of row cannot be given a time and get a blank one rather than a
  guessed one: 'Fig 4a-c' "Day 1 post infection" (10 days before treatment
  started, so not time zero of treatment); the two 'Fig 4a-c' mice whose comment
  says "mouse euthanized early, day 18" / "day 17" while their Days-of-treatment
  column still reads 28, a contradiction the sheet does not resolve; and
  'Fig 5a-d' UNTX animals, whose day columns read "NA".

REPEATED READINGS.  Two are flagged rather than dropped: the day-0 Control of
'Fig 3a-e' Set 4 appears twice with one CFU value and two RS ratios, and the
three untreated mice of 'Sup Fig 8b' are the same animals, with the same
numbers, as the day-53 untreated mice of 'Fig 1c' -- on two different clocks,
because each sheet is read on its own.

NOT A READING, and skipped: 35 "not plated" cells in the resistant column of
'Fig 4a-c' and 4 "Not tested" cells in 'Sup Fig 5g-j'.  The 2 "Too numerous to
count" cells of 'Sup Fig 5g-j' and the 2 "nd" cells of 'Sup Fig 11' ARE kept,
with a blank count and the verbatim string in notes, because a reading was
attempted in each.
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

from src.ingest import empty

BOOK = "_unpacked/PMC8131613_supplementary/41467_2021_22833_MOESM4_ESM.xlsx"
ZIP = "PMC8131613_supplementary.zip"
SI_PDF = "41467_2021_22833_MOESM1_ESM.pdf"

# ---------------------------------------------------------------- readouts
R_ML = "CFU per mL (the source's column is 'CFU per mL (log10)')"
R_ML_RES = ("resistant CFU per mL, colonies on drug-containing plates (the "
            "source's column is 'Resistant CFU per mL (log10)')")
R_LUNG = ("CFU per mouse lung (the source's column is 'CFU per lung'; the "
          "denominator is a whole lung, NOT a mL)")
R_LUNG_RES = ("resistant CFU per mouse lung, colonies on drug-containing plates "
              "(the source's column is 'Resistant CFU per lung (log10)'; the "
              "denominator is a whole lung, NOT a mL)")

# ------------------------------------------------------- parsing the deposit
# "... The dashed line represents the limit of detection (13 CFU ml-1)."
LOD_ML = re.compile(r"limit of detection\s*\(\s*([\d.]+)\s*CFU\s*ml\s*-?\s*1\s*\)",
                    re.I)
# "CFU of <2.18 indicates the lower level of detection; nd indicates not determined."
LOD_RES = re.compile(r"CFU of\s*<\s*([\d.]+)\s*indicates the lower level of "
                     r"detection", re.I)
ORG_RE = re.compile(r"\b(Mycobacterium tuberculosis)\b")
# a below-limit cell, whatever column it is in
LT = re.compile(r"^<\s*([0-9.]+)$")

# ---------------------------------------------------------------- floors
F_ML = ('stated by the deposit: its Supplementary Information PDF (%s) says, in '
        'the legend to Supplementary Fig. 5 g-j, "%s" -- a limit of detection '
        'of %s CFU per mL. That legend covers panels g-j, which plot total '
        'plateable and resistant bacteria for rifampin, bedaquiline, isoniazid '
        'and streptomycin; the deposit runs one in vitro CFU-per-mL plating and '
        'states no other limit for it, so the number is applied to every in '
        'vitro reading, including the ethambutol arm and the day-0 control, '
        'which those panels do not show. The workbook itself gives no limit, no '
        'plated volume and no dilution')
N_ML = ('no floor: the workbook gives no detection limit, no plated volume and '
        'no dilution for the in vitro counts and writes no below-limit marker '
        'in this column, and the deposit\'s Supplementary Information PDF, '
        'which is where such a statement would be, could not be read here (%s)')

F_FIG4_RES = ('stated in the sheet and named in the deposit: the Supplementary '
              'Information PDF (%s) says of this experiment "%s", so the '
              'sheet\'s "< 2.18" cells mark a detection limit and not merely a '
              'bound. The value recorded is 150 CFU per lung rather than '
              '10**2.18: the sheet writes its smallest detected value as '
              '2.176091259, which is log10(150) = 2.1760912590556813 to every '
              'digit it prints, and every other detected value in the column is '
              'log10 of an exact multiple of 150 (300, 600, 750, 1200, 1500, '
              '2250, 2700, 4500), so one colony is 150 CFU per lung and 2.18 is '
              'that figure rounded')
F_FIG4_ODD = ('stated in the deposit: its Supplementary Information PDF (%s) '
              'says "%s", so the floor of this column is 10**%s CFU per lung. '
              'NOTE that this disagrees with the sheet, whose below-limit cells '
              'read "< 2.18" and whose smallest detected value is log10(150)')
F_FIG4_CELL = ('stated in the sheet: this cell itself reads "%s", which bounds '
               'this reading above in log10 CFU per lung. The deposit\'s '
               'Supplementary Information PDF names this column\'s detection '
               'limit, but it could not be read here (%s), so the bound is '
               'recorded where the sheet puts it -- on this cell -- and is not '
               'asserted for the column')
N_FIG4_RES = ('no floor for this reading: the deposit\'s Supplementary '
              'Information PDF, which names this column\'s detection limit, '
              'could not be read here (%s), and the sheet states no limit, no '
              'plated volume and no dilution of its own')

F_CELL = ('stated in the sheet: this cell itself reads "%s", which bounds this '
          'reading above at %s %s. No legend anywhere in the deposit says what '
          'that mark is -- it is not called a limit of detection -- so the '
          'bound is recorded where the sheet puts it, on this cell, and is not '
          'asserted for the readings in this column that carry a number')
N_CELL = ('no floor for this reading: the deposit states no detection limit, no '
          'plated volume and no dilution for this sheet\'s %s column. The mark '
          '"<%s" appears on %d of its cells and bounds those cells; that bound '
          'is not carried onto this one%s')

N_FIG1C = ('no floor: this sheet gives no detection limit, plated volume or '
           'dilution for its "CFU per lung (log10)" column and writes no '
           'below-limit marker, and no legend in the deposit supplies one')
N_FIG4_TOT = ('no floor: this sheet\'s "CFU per lung (log10)" column carries no '
              'below-limit marker, no plated volume and no dilution, and the '
              'deposit\'s only detection-limit sentence for this experiment is '
              'scoped to "Drug resistant CFU" -- a different plating, on '
              'drug-containing plates. Its 150 CFU per lung is therefore not '
              'carried over; the smallest value in this column is 630')

# ---------------------------------------------------------------- notes
NO_ORG = ("the workbook names no organism and no strain; %s")
ORG_FOUND = ('organism from the deposit\'s Supplementary Information PDF (%s), '
             'whose title reads "%s" and whose Supplementary Fig. 1b legend '
             'calls the CFU per lung of sheet \'Fig 1c & Sup Fig 1b\' the "Mtb '
             'burden"; no strain is named anywhere in the deposit')
ORG_BLANK = ('the Supplementary Information PDF, which names it, could not be '
             'read here (%s), so the organism column is left blank')
NO_CONC = ("the workbook states no drug concentration and no dose unit; the "
           "arm label is the source's own and the drug abbreviations are "
           "expanded nowhere in the deposit")
DOSE_NOTE = ("the number in the arm label is the dose the sheet writes; the "
             "workbook never gives its unit, so it is not put in the "
             "concentration column")
BLANK_NOTE = ('the sheet gives no number for this reading, only that it is '
              'below the limit, so cfu_per_ml is left blank and the floor '
              'carries the information')
BELOW = ('this reading is written as a DETECTED value but lies below the '
         '%s CFU/mL limit of detection the deposit states for this assay; it is '
         'recorded as written')

T_FIG3 = "time_h is the sheet's 'Treatment days' column x 24 (day 0.25 = 6 h)"
T_FIG1C = ("time_h is hours after AEROSOL INFECTION, not after drug exposure: "
           "every mouse in this sheet is untreated and the sheet's only time "
           "column is 'Day of sacrifice', counted from infection")
T_FIG4 = ("time_h is hours of treatment: this sheet's treated rows read 28 in "
          "'Days of treatment' and 39 in 'Day of sacrifice', and 39 - 28 = 11 "
          "is the day treatment began; its two baseline arms read (1, 0) and "
          "(11, 0), which match their own labels 'Day 1 post infection' and "
          "'Pre-Rx' only if the two columns swap meaning on those rows, and "
          "sheet 'Sup Fig 11' prints the same pair under the opposite headers")
T_FIG5 = ("time_h is this sheet's 'Day of sacrifice' x 24, counted from "
          "treatment start: it equals 'Days of treatment' for on-treatment and "
          "end-of-treatment rows and 'Days of treatment' + 84 for the relapse "
          "rows, the 84 days being the drug-free holiday")
T_S8B = ("time_h is 28 days x 24: this sheet's caption says '28-day treatment' "
         "and every row shares 'Day of sacrifice' 53, so treated and untreated "
         "animals were taken on the same day")
T_S11 = ("time_h is from the arm label ('4 weeks' = 28 d, '8 weeks' = 56 d), "
         "which matches the column this sheet prints under 'Day of sacrifice' "
         "(28, 56); this sheet's two time headers are swapped with respect to "
         "their values -- the column headed 'Days of treatment' holds 39 and "
         "67, which are 11 + 28 and 11 + 56, days from infection")

LOG0 = ('the sheet writes 0 in a log10 column; it does not say whether that '
        'means 10**0 = 1 CFU/mL or "none detected", so no count is recorded '
        'and the cell is reported here instead of being interpreted. Either '
        'reading of the cell lies below the limit of detection the deposit '
        'states for this assay, which is why the reading is marked censored '
        'with no count')
ND_NOTE = ('the deposit defines "nd" as "not determined" in the legend to '
           'Supplementary Fig. 8a, which is a different figure, so no count is '
           'recorded here')


def _n(v) -> str:
    """A header or text cell, newlines and doubled spaces collapsed."""
    return re.sub(r"\s+", " ", str(v)).strip()


def _sentence(text: str, m: re.Match) -> str:
    """The full sentence of `text` that contains match `m`."""
    start = text.rfind(".", 0, m.start()) + 1
    end = text.find(".", m.end())
    return text[start: end + 1 if end >= 0 else len(text)].strip()


def _si(d: Path) -> dict:
    """What the deposit's Supplementary Information PDF states, parsed.

    The PDF is part of the deposit -- PROVENANCE.json records one download, the
    zip, and the PDF is inside it -- and it is the only place in this deposit
    where a detection limit is written as a number.  It is read from _unpacked/
    if it has been extracted and straight out of the zip if not.  Every number
    it yields is parsed here, so a changed deposit blanks the floor instead of
    leaving a stale one behind.
    """
    out = {"where": "", "why": "", "ml": None, "ml_quote": "",
           "res": None, "res_quote": "", "organism": "", "title": ""}
    blob = None
    loose = sorted(d.rglob(SI_PDF))
    if loose:
        blob = loose[0].read_bytes()
        out["where"] = loose[0].relative_to(d).as_posix()
    elif (d / ZIP).exists():
        try:
            with zipfile.ZipFile(d / ZIP) as zf:
                if SI_PDF in zf.namelist():
                    blob = zf.read(SI_PDF)
                    out["where"] = "%s::%s" % (ZIP, SI_PDF)
        except (zipfile.BadZipFile, OSError) as exc:      # pragma: no cover
            out["why"] = "the deposit's zip could not be opened: %s" % exc
            return out
    if blob is None:
        out["why"] = "%s is not in this deposit directory or its zip" % SI_PDF
        return out
    try:
        import pymupdf
    except ImportError:                                    # pragma: no cover
        try:
            import fitz as pymupdf                         # PyMuPDF < 1.24
        except ImportError:
            out["why"] = "PyMuPDF is not installed, so the PDF cannot be read"
            return out
    try:
        with pymupdf.open(stream=blob, filetype="pdf") as doc:
            text = "".join(page.get_text() for page in doc)
    except Exception as exc:                               # pragma: no cover
        out["why"] = "the PDF would not open: %s" % exc
        return out
    text = re.sub(r"\s+", " ", text).strip()

    m = LOD_ML.search(text)
    if m:
        out["ml"], out["ml_quote"] = float(m.group(1)), _sentence(text, m)
    m = LOD_RES.search(text)
    if m:
        out["res"], out["res_quote"] = float(m.group(1)), _sentence(text, m)
    m = ORG_RE.search(text[:400])
    if m:
        out["organism"] = m.group(1)
        out["title"] = text[m.start():m.start() + 110].strip()
    if out["ml"] is None and out["res"] is None:
        out["why"] = ("the PDF was read but neither of its detection-limit "
                      "sentences was found in it")
    return out


def _header(ws) -> tuple[int, dict]:
    """(row index, {header text -> column index}) for a sheet of this workbook."""
    for r in range(1, 12):
        vals = {_n(ws.cell(row=r, column=c).value): c
                for c in range(1, ws.max_column + 1)
                if ws.cell(row=r, column=c).value is not None}
        if "Mouse" in vals or "Set" in vals:
            return r, vals
    raise ValueError("%s: no header row" % ws.title)


def _caption(ws, hdr: int) -> str:
    """The sheet's own title lines, above the header row."""
    out = []
    for r in range(1, hdr):
        for c in range(1, ws.max_column + 1):
            v = ws.cell(row=r, column=c).value
            if isinstance(v, str) and v.strip():
                out.append(_n(v))
    return "; ".join(out)


def _body(ws, hdr: int, key: int):
    """Data rows: those with something in the Mouse/Set column."""
    for r in range(hdr + 1, ws.max_row + 1):
        if ws.cell(row=r, column=key).value is not None:
            yield r


def _num(v):
    return float(v) if isinstance(v, (int, float)) and np.isfinite(v) else None


def _drug(arm: str) -> str:
    """The arm label with its dose figures stripped. '' where there is no drug."""
    a = arm.strip()
    if a.lower() in {"control", "untreated", "untx", "pre-rx", "pre-treatment",
                     "day 1 post infection"}:
        return ""
    parts = []
    for p in a.split("+"):
        p = re.sub(r"\s*\(.*?\)\s*", "", p)          # drop "(4 weeks)"
        parts.append(re.sub(r"\s*\d+(\.\d+)?\s*$", "", p).strip())  # drop "100"
    return " + ".join(p for p in parts if p)


def _join(*bits) -> str:
    return "; ".join(b for b in bits if b)


def _invitro_floor(si: dict) -> tuple[float | None, str]:
    """13 CFU/mL and the sentence that states it, or nothing and why."""
    if si["ml"] is None:
        return None, N_ML % (si["why"] or "the sentence was not found")
    return si["ml"], F_ML % (si["where"], si["ml_quote"], "%g" % si["ml"])


def _lt_cells(ws, col: int) -> tuple[int, str]:
    """(how many cells of this column are written "<x", the x they write)."""
    n, mark = 0, ""
    for r in range(1, ws.max_row + 1):
        v = ws.cell(row=r, column=col).value
        if isinstance(v, str):
            m = LT.match(_n(v))
            if m:
                n, mark = n + 1, m.group(1)
    return n, mark


# --------------------------------------------------------------- the sheets

def _fig1c(ws, si) -> list[dict]:
    """Untreated BALB/c chronic infection: CFU per lung, days 1-53 after infection."""
    hdr, col = _header(ws)
    cap = _caption(ws, hdr)
    out = []
    for r in _body(ws, hdr, col["Mouse"]):
        mouse = ws.cell(row=r, column=col["Mouse"]).value
        arm = _n(ws.cell(row=r, column=col["Treatment"]).value)
        day = _num(ws.cell(row=r, column=col["Day of sacrifice"]).value)
        v = _num(ws.cell(row=r, column=col["CFU per lung (log10)"]).value)
        if v is None:
            continue
        dup = ("this mouse and its numbers appear again on sheet 'Sup Fig 8b' "
               "as one of that sheet's untreated controls, where they are put "
               "on the treated animals' clock instead of this one"
               if day == 53 else "")
        out.append({
            "sheet": ws.title, "arm": arm, "drug": _drug(arm),
            "replicate": "fig1c mouse %s" % mouse,
            "time_h": None if day is None else day * 24.0,
            "cfu_per_ml": 10.0 ** v,
            "floor_basis": N_FIG1C, "readout": R_LUNG,
            "notes": _join(cap, T_FIG1C, dup, NO_CONC,
                           "sheet value %r log10 CFU per lung" % v),
        })
    return out


def _fig3(ws, si) -> list[dict]:
    """In vitro time-kill: 5 drugs plus a day-0 control, CFU per mL (log10)."""
    hdr, col = _header(ws)
    cap = _caption(ws, hdr)
    floor, basis = _invitro_floor(si)
    out, seen = [], set()
    for r in _body(ws, hdr, col["Set"]):
        st = ws.cell(row=r, column=col["Set"]).value
        arm = _n(ws.cell(row=r, column=col["Group"]).value)
        day = _num(ws.cell(row=r, column=col["Treatment days"]).value)
        v = _num(ws.cell(row=r, column=col["CFU per mL (log10)"]).value)
        if v is None or day is None:
            continue
        k = (st, arm, day, v)
        dup = ("this sheet writes the same reading twice, on two rows that "
               "differ only in their RS ratio; both are kept and this is the "
               "repeat" if k in seen else "")
        seen.add(k)
        ctrl = ("'Control' appears in this sheet only at treatment day 0: it is "
                "the pre-treatment reading, not an untreated arm followed over "
                "time" if arm.lower() == "control" else "")
        out.append({
            "sheet": ws.title, "arm": arm, "drug": _drug(arm),
            "replicate": "fig3 set %s" % st,
            "time_h": day * 24.0, "cfu_per_ml": 10.0 ** v,
            "floor_cfu_per_ml": floor, "floor_basis": basis, "readout": R_ML,
            "notes": _join(cap, T_FIG3, ctrl, dup, NO_CONC,
                           "sheet value %r log10 CFU per mL" % v),
        })
    return out


def _sup5gj(ws, si) -> list[dict]:
    """In vitro resistant mutants: 'Resistant CFU per mL (log10)', days 0-8."""
    hdr, col = _header(ws)
    cap = _caption(ws, hdr)
    floor, basis = _invitro_floor(si)
    out = []
    for r in _body(ws, hdr, col["Set"]):
        st = ws.cell(row=r, column=col["Set"]).value
        arm = _n(ws.cell(row=r, column=col["Group"]).value)
        day = _num(ws.cell(row=r, column=col["Treatment days"]).value)
        raw = ws.cell(row=r, column=col["Resistant CFU per mL (log10)"]).value
        cfu, cens, extra = None, "", ""
        if isinstance(raw, str):
            if _n(raw).lower() == "not tested":
                continue                      # no reading was taken
            extra = 'the sheet writes this reading as "%s"' % _n(raw)
        else:
            v = _num(raw)
            if v is None:
                continue
            if v == 0:
                # A 0 in a log10 column is 1 CFU/mL or nothing at all; the sheet
                # does not say which, so no count is written. Both readings are
                # under the stated limit, so the censoring call is safe even
                # though the count is not.
                extra = LOG0
                if floor is not None:
                    cens = "yes"
            else:
                cfu = 10.0 ** v
                if floor is not None and cfu < floor:
                    extra = BELOW % ("%g" % floor)
        out.append({
            "sheet": ws.title, "arm": arm, "drug": _drug(arm),
            "replicate": "sup5gj set %s" % st,
            "time_h": None if day is None else day * 24.0,
            "cfu_per_ml": cfu, "censored": cens,
            "floor_cfu_per_ml": floor, "floor_basis": basis,
            "readout": R_ML_RES,
            "notes": _join(cap, T_FIG3, extra, NO_CONC, "sheet value %r" % raw),
        })
    return out


def _fig4(ws, si) -> list[dict]:
    """BALB/c, 28 days of monotherapy: total and resistant CFU per lung."""
    hdr, col = _header(ws)
    cap = _caption(ws, hdr)
    ctot = col["CFU per lung (log10)"]
    cres = col["Resistant CFU per lung (log10)"]

    # The deposit's own legend calls this column's "< 2.18" cells a lower level
    # of detection, which is what lets the floor cover the column rather than
    # only the cells that carry the mark. Without that sentence the reader falls
    # back to the per-cell rule the other sheets use.
    if si["res"] is None:
        col_floor, col_basis = None, N_FIG4_RES % (si["why"] or "no sentence")
    elif abs(si["res"] - 2.18) > 1e-9:                     # pragma: no cover
        col_floor = 10.0 ** si["res"]
        col_basis = F_FIG4_ODD % (si["where"], si["res_quote"], si["res"])
    else:
        col_floor = 150.0
        col_basis = F_FIG4_RES % (si["where"], si["res_quote"])

    out = []
    for r in _body(ws, hdr, col["Mouse"]):
        mouse = ws.cell(row=r, column=col["Mouse"]).value
        arm = _n(ws.cell(row=r, column=col["Treatment"]).value)
        d_treat = _num(ws.cell(row=r, column=col["Days of treatment"]).value)
        d_sac = _num(ws.cell(row=r, column=col["Day of sacrifice"]).value)
        comment = ws.cell(row=r, column=col["CFU comment"]).value
        comment = _n(comment) if isinstance(comment, str) else ""

        when, why = None, ""
        if arm == "Pre-Rx":
            when = 0.0
            why = ("this is the pre-treatment reading, day 0 of treatment; the "
                   "sheet's own columns read 11 and 0, the 11 being the day "
                   "after infection on which treatment started")
        elif arm == "Day 1 post infection":
            why = ("no time: this reading is 10 days BEFORE treatment started "
                   "(day 1 after infection, treatment began on day 11), so it "
                   "is not time zero of treatment and no negative time is "
                   "invented for it")
        elif "euthanized early" in comment:
            why = ("no time: the sheet's 'Days of treatment' column reads %s for "
                   "this mouse while its own comment says it was euthanized "
                   "early, and the sheet does not say whether that day is "
                   "counted from infection or from treatment start, so the two "
                   "disagree and neither is used" % d_treat)
        elif d_treat is not None:
            when = d_treat * 24.0
            if d_sac is not None and abs(d_sac - d_treat - 11) > 1e-9:
                why = ("this row's 'Day of sacrifice' is %s, which is not "
                       "'Days of treatment' + 11 as it is on every other "
                       "treated row of the sheet" % d_sac)

        base = {"sheet": ws.title, "arm": arm, "drug": _drug(arm),
                "replicate": "fig4 mouse %s" % mouse, "time_h": when}
        common = _join(cap, T_FIG4, why, comment and
                       'the sheet\'s CFU comment column says "%s"' % comment,
                       NO_CONC, DOSE_NOTE)

        v = _num(ws.cell(row=r, column=ctot).value)
        if v is not None:
            out.append({**base, "cfu_per_ml": 10.0 ** v,
                        "floor_basis": N_FIG4_TOT, "readout": R_LUNG,
                        "notes": _join(common,
                                       "sheet value %r log10 CFU per lung" % v)})

        raw = ws.cell(row=r, column=cres).value
        cfu, cens, extra = None, "", ""
        floor, basis = col_floor, col_basis
        if isinstance(raw, str):
            if _n(raw).lower() == "not plated":
                continue                      # the assay was not done
            cfu, cens = None, "yes"
            extra = _join('the sheet writes this reading as "%s"' % _n(raw),
                          BLANK_NOTE)
            m = LT.match(_n(raw))
            if col_floor is None and m:       # pragma: no cover
                floor = 10.0 ** float(m.group(1))
                basis = F_FIG4_CELL % (_n(raw), si["why"] or "no sentence")
        else:
            v = _num(raw)
            if v is None:
                continue
            cfu = 10.0 ** v
            if v == 2.176091259:
                extra = ("this is the sheet's censoring value itself, one "
                         "colony = 150 CFU per lung: a detection at the floor, "
                         "not a below-limit reading")
            elif abs(v - 2.176091259) < 5e-4:
                extra = ("the sheet writes this reading as %r, which is the "
                         "same one-colony value it writes elsewhere as "
                         "2.176091259 = log10(150), rounded; taken as written "
                         "it lands a thousandth of a CFU ABOVE the floor, so "
                         "the censored flag on this row reads 'no' for a "
                         "reading that is in fact at the floor" % v)
        out.append({**base, "cfu_per_ml": cfu, "censored": cens,
                    "floor_cfu_per_ml": floor, "floor_basis": basis,
                    "readout": R_LUNG_RES,
                    "notes": _join(common, extra, "sheet value %r" % raw)})
    return out


def _fig5(ws, si) -> list[dict]:
    """The relapsing mouse model: CFU per lung, linear, 16 sacrifice days."""
    hdr, col = _header(ws)
    cap = _caption(ws, hdr)
    ccfu = col["CFU per lung"]
    n_lt, mark = _lt_cells(ws, ccfu)

    # Why the "<3.26" bound is not carried onto the counted readings: the column
    # mixes granularities, so the one-colony equivalent is not the same for
    # every mouse and 3.26 is not shown to be the column's floor. Counted here
    # rather than asserted.
    vals = [v for r in _body(ws, hdr, col["Mouse"])
            for v in [_num(ws.cell(row=r, column=ccfu).value)] if v is not None]
    a = sum(1 for v in vals if abs(v / 3.26 - round(v / 3.26)) < 1e-6)
    b = sum(1 for v in vals if abs(v / 7.5 - round(v / 7.5)) < 1e-6)
    quantum = (", because of the %d counted readings in this column %d are "
               "exact multiples of 3.26 and %d are exact multiples of 7.5: the "
               "one-colony equivalent varies from mouse to mouse, so this "
               "column's readings were not all read at the same dilution"
               % (len(vals), a, b))
    no_floor = N_CELL % ('"CFU per lung"', mark, n_lt, quantum)

    out = []
    for r in _body(ws, hdr, col["Mouse"]):
        mouse = ws.cell(row=r, column=col["Mouse"]).value
        arm = _n(ws.cell(row=r, column=col["Treatment"]).value)
        stage = _n(ws.cell(row=r, column=col["Stage at which sacrificed"]).value)
        d_treat = ws.cell(row=r, column=col["Days of treatment"]).value
        d_sac = _num(ws.cell(row=r, column=col["Day of sacrifice"]).value)
        raw = ws.cell(row=r, column=ccfu).value
        if raw is None:
            continue

        when, why = None, ""
        if d_sac is not None:
            when = d_sac * 24.0
        elif stage == "Pre-Treatment":
            when = 0.0
            why = ("the sheet's day columns read 'NA' here; this arm is labelled "
                   "'Pre-Rx' at the 'Pre-Treatment' stage, so it is day 0 of "
                   "treatment")
        else:
            why = ("no time: the sheet writes 'NA' in both day columns for these "
                   "untreated animals and says nowhere when they were taken")

        cfu, cens, extra = None, "", ""
        floor, basis = None, no_floor
        if isinstance(raw, str):
            m = LT.match(_n(raw))
            cfu, cens = None, "yes"
            extra = _join('the sheet writes this reading as "%s"' % _n(raw),
                          BLANK_NOTE)
            if m:
                floor = float(m.group(1))
                basis = F_CELL % (_n(raw), m.group(1), "CFU per lung")
        else:
            cfu = _num(raw)
            if cfu is None:
                continue
        out.append({
            "sheet": ws.title, "arm": arm, "drug": _drug(arm),
            "replicate": "fig5 mouse %s" % mouse, "time_h": when,
            "cfu_per_ml": cfu, "censored": cens,
            "floor_cfu_per_ml": floor, "floor_basis": basis,
            "readout": R_LUNG,
            "notes": _join(cap, T_FIG5, why,
                           "the sheet's stage for this animal is '%s'" % stage,
                           "the sheet's 'Days of treatment' cell reads %r"
                           % d_treat,
                           NO_CONC, DOSE_NOTE,
                           "sheet value %r CFU per lung" % raw),
        })
    return out


def _sup8b(ws, si) -> list[dict]:
    """Low-dose aerosol BALB/c, 28-day treatment: CFU per lung (log10)."""
    hdr, col = _header(ws)
    cap = _caption(ws, hdr)
    ccfu = col["CFU per lung (log10)"]
    n_lt, mark = _lt_cells(ws, ccfu)
    no_floor = N_CELL % ('"CFU per lung (log10)"', mark, n_lt, "")
    out = []
    for r in _body(ws, hdr, col["Mouse"]):
        mouse = ws.cell(row=r, column=col["Mouse"]).value
        arm = _n(ws.cell(row=r, column=col["Treatment"]).value)
        d_sac = _num(ws.cell(row=r, column=col["Day of sacrifice"]).value)
        raw = ws.cell(row=r, column=ccfu).value
        if raw is None:
            continue
        cfu, cens, extra = None, "", ""
        floor, basis = None, no_floor
        if isinstance(raw, str):
            m = LT.match(_n(raw))
            cfu, cens = None, "yes"
            extra = _join('the sheet writes this reading as "%s"' % _n(raw),
                          BLANK_NOTE)
            if m:
                floor = 10.0 ** float(m.group(1))
                basis = F_CELL % (_n(raw), "10**%s" % m.group(1),
                                  "CFU per lung")
        else:
            v = _num(raw)
            if v is None:
                continue
            cfu = 10.0 ** v
        untx = ("this animal was never treated; the 672 h is the day the treated "
                "animals of this sheet reached, which it shares; the same mouse, "
                "with the same numbers, is also the day-53 untreated animal of "
                "sheet 'Fig 1c & Sup Fig 1b', where it is put on the "
                "hours-after-infection clock instead" if _drug(arm) == "" else "")
        out.append({
            "sheet": ws.title, "arm": arm, "drug": _drug(arm),
            "replicate": "sup8b mouse %s" % mouse,
            "time_h": 28 * 24.0, "cfu_per_ml": cfu, "censored": cens,
            "floor_cfu_per_ml": floor, "floor_basis": basis,
            "readout": R_LUNG,
            "notes": _join(cap, T_S8B, untx, extra,
                           "the sheet's 'Day of sacrifice' cell reads %r" % d_sac,
                           NO_CONC, DOSE_NOTE,
                           "sheet value %r" % raw),
        })
    return out


def _sup11(ws, si) -> list[dict]:
    """BALB/c, 4 or 8 weeks of HRZE or BPaL: CFU per lung (log10)."""
    hdr, col = _header(ws)
    cap = _caption(ws, hdr)
    ccfu = col["CFU per lung (log10)"]
    n_lt, mark = _lt_cells(ws, ccfu)
    no_floor = N_CELL % ('"CFU per lung (log10)"', mark, n_lt, "")
    # This sheet's two time headers are swapped with respect to their values;
    # the arm label carries the treatment length, so use it and check it.
    out = []
    for r in _body(ws, hdr, col["Mouse"]):
        mouse = ws.cell(row=r, column=col["Mouse"]).value
        arm = _n(ws.cell(row=r, column=col["Treatment"]).value)
        printed = _num(ws.cell(row=r, column=col["Day of sacrifice"]).value)
        other = _num(ws.cell(row=r, column=col["Days of treatment"]).value)
        raw = ws.cell(row=r, column=ccfu).value
        if raw is None:
            continue
        m = re.search(r"\((\d+)\s*weeks?\)", arm)
        when = float(m.group(1)) * 7 * 24.0 if m else None
        why = ""
        if when is not None and printed is not None and \
                abs(printed * 24.0 - when) > 1e-9:
            why = ("the arm label and the sheet's own day columns disagree for "
                   "this row (label %s, columns %s and %s)" % (arm, printed, other))
        cfu, cens, extra = None, "", ""
        floor, basis = None, no_floor
        if isinstance(raw, str):
            s = _n(raw)
            mm = LT.match(s)
            if mm:
                cfu, cens = None, "yes"
                floor = 10.0 ** float(mm.group(1))
                basis = F_CELL % (s, "10**%s" % mm.group(1), "CFU per lung")
                extra = _join('the sheet writes this reading as "%s"' % s,
                              BLANK_NOTE)
            else:
                extra = _join('the sheet writes this reading as "%s"' % s,
                              ND_NOTE if s.lower() == "nd" else
                              "the deposit does not say what that stands for, "
                              "so no count is recorded")
        else:
            v = _num(raw)
            if v is None:
                continue
            cfu = 10.0 ** v
            if mark and abs(v - float(mark)) < 1e-9:
                extra = ("the sheet writes this reading as a DETECTED value "
                         "equal to the bound its own '<%s' cells carry, so it "
                         "is one colony on this plating; the deposit still "
                         "states no detection limit for the column, and none "
                         "is supplied for this row" % mark)
        out.append({
            "sheet": ws.title, "arm": arm, "drug": _drug(arm),
            "replicate": "sup11 mouse %s" % mouse,
            "time_h": when, "cfu_per_ml": cfu, "censored": cens,
            "floor_cfu_per_ml": floor, "floor_basis": basis,
            "readout": R_LUNG,
            "notes": _join(cap, T_S11, why, extra,
                           "this sheet's day cells read %r under 'Day of "
                           "sacrifice' and %r under 'Days of treatment'"
                           % (printed, other),
                           NO_CONC, DOSE_NOTE,
                           "sheet value %r" % raw),
        })
    return out


SHEETS = {
    "Fig 1c & Sup Fig 1b": _fig1c,
    "Fig 3a-e & Sup Fig 5": _fig3,
    "Sup Fig 5g-j": _sup5gj,
    "Fig 4a-c & Sup Fig 7-8": _fig4,
    "Fig 5a-d & Sup Fig 9-10": _fig5,
    "Sup Fig 8b": _sup8b,
    "Sup Fig 11": _sup11,
}

# no bacterial counts in these; kept here so the omission is deliberate
NOT_READ = ("'Fig 1b & Sup Fig 1a' (RS ratio, ITS1/23S and growth rate in an "
            "oxygen-depletion model), 'Fig 6a' and 'Fig 6b' (patient sputum "
            "rRNA synthesis ratio and rifampin AUC) hold no bacterial counts")


def read(d: Path) -> pd.DataFrame:
    book = d / BOOK
    if not book.exists():
        return empty()
    si = _si(d)
    wb = load_workbook(book, data_only=True, read_only=False)

    rows = []
    for name, fn in SHEETS.items():
        if name not in wb.sheetnames:
            continue
        rows.extend(fn(wb[name], si))
    if not rows:
        return empty()

    df = pd.DataFrame(rows)
    df["source_file"] = BOOK
    # The organism is named in the deposit, but only in the PDF; the workbook
    # names neither it nor the strain, and the strain is named nowhere at all.
    df["organism"] = si["organism"]
    df["strain"] = ""
    org = NO_ORG % (ORG_FOUND % (si["where"], si["title"]) if si["organism"]
                    else ORG_BLANK % (si["why"] or "no title line was found"))
    df["notes"] = df["notes"] + "; " + org + \
        ("; not read from this workbook: " + NOT_READ)
    return df
