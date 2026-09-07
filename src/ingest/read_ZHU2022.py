"""ZHU2022 -- Nature Communications Supplementary Data 8, 31 sheets.

10.1038/s41467-022-30967-4, file 41467_2022_30967_MOESM11_ESM.xlsx.

Streptococcus pneumoniae TIGR4 wild type against single-gene deletion mutants,
killed at 5x or 10x MIC. The eleven sheets whose names contain TOLERA hold the
kill data: for each of two (on one sheet, more) strains, four replicate cultures
lettered A-D, sampled at 0, 8 and 24 hours. Each count block is followed by a
computed "Fraction" block (each value over its own time-0 value) and a "Fold"
block; neither is a reading, and neither is read here.

WHAT THE UNIT IS, AND HOW MUCH OF THAT IS THE DEPOSIT'S WORD. The workbook never
writes "CFU", never writes "/mL", and never names the species. The values are
read as CFU/mL on the strength of three things inside the file itself: the
sheets are titled TOLERANCE and sit beside a Fraction block that is each value
over its time-0 value; the time-0 values are 1.4e6 to 1.2e8, the scale of an
inoculum; and several sheets carry a hand-written note that "at 24hr no WT could
be recovered", recovery being of colonies. If that reading is wrong then every
count here is wrong the same way, so it is flagged on every row. organism stays
BLANK: the workbook names a strain (TIGR4 WT on the growth sheets, WT on the
kill sheets) and SP_ locus tags, but never states a species, and a species is
not something to supply from outside the file.

THE FLOOR, AND THE ONE PLACE THE DEPOSIT ADMITS TO IT. No plated volume, no
dilution, no colony count and no numeric limit of detection anywhere, so
floor_cfu_per_ml is blank throughout. But the value 0.1 recurs at 24 h across
sheets -- and on six sheets the depositor wrote underneath, in prose, "N.B. at
24hr no WT could be recovered, and thus the fold enrichment maybe bigger than
...". That is the deposit itself saying those readings are non-detections. On
those sheets the wild-type 24 h readings are marked censored = yes with the
sentence quoted in notes, while floor_cfu_per_ml still stays blank, because
"nothing grew" is not a number. The 0.1 and 1 values elsewhere are left
censored = unknown: the same placeholder is plainly visible, but the deposit
does not say so there, and inferring it is what this corpus exists to avoid.

'1888 VAN TOLERANCE' HAS A WRONG HEADER. Its two block headers read
"WT_10X Gentamicin" and "d1888_10X Gentamicin", copied from the gentamicin
sheet, while the sheet is named VAN and the workbook's own summary sheet
"TOLERANCE DATA COMBINED" lists this experiment as "SP_1888 VANC" beneath a VAN
column. Two independent labels in the file say vancomycin against one stale
copy, so drug is recorded as VAN and the conflict is stated on every row of that
sheet. The same stale-copy habit appears harmlessly in the Fraction blocks of
'0829 FEP TOLERANCE' and '1097 1645 & DBL FEP TOLERA', which say Gentamicin
above cefepime data; those blocks are not read.

THE SAME CULTURES ARE REPORTED MORE THAN ONCE. Wild-type control blocks are
shared between experiments and re-printed on each sheet that uses them, so a
naive read counts some readings two or three times. Blocks are therefore
de-duplicated on their full content (every replicate letter, time and value):
where two or more blocks are identical AND carry the same strain, drug and
multiple of MIC, one copy is returned and the notes name every sheet it appears
on. Three such families exist -- the 10x ciprofloxacin wild type shared by
'1068 CIP TOLERANCE' and '1544 CIP TOLERANCE', the 5x gentamicin wild type
shared by '2065 GEN TOLERANCE' and '2066 GEN TOLERANCE', and the 5x cefepime
wild type printed once on '0829 FEP TOLERANCE' and twice more on
'1097 1645 & DBL FEP TOLERA'.

AND ONE FAMILY WHERE THE LABELS CONTRADICT EACH OTHER. The four series starting
18600000 / 22150000 / 18150000 / 16650000 appear twice: headed
"0829_5X MIC CEFEPIME" on '0829 FEP TOLERANCE', and headed "WT_5X CEFEPIME" in
the right-hand half of '1097 1645 & DBL FEP TOLERA', where they serve as the
denominator of the SP_1645 fold enrichment. One of those two labels is wrong and
nothing in the deposit says which. They are ONE set of cultures, so they are
returned ONCE -- with `strain` BLANK, because that is the field the deposit
contradicts itself on, and both printed headers quoted in `arm` and in the
notes. The drug (cefepime) and the multiple of MIC (5x) agree between the two
labels and are kept. Censoring is left unknown for that block: the sheet's
"no WT could be recovered" note is about the wild type, and whether this block
is the wild type is precisely what is in dispute.

WHAT IS NOT READ, AND WHY
  the 19 sheets whose names end GROWTH -- '1888 1890 noABX GROWTH',
  '1888 1890 GEN GROWTH', '1888 1890 VAN GROWTH', '1888 1890 CIP GROWTH',
  '0006_MFD GEN GROWTH', '0288 SXT AMX GROWTH', '1068 CIP GROWTH',
  '1544 CIP GROWTH', '2175 2176 GEN MEM GROWTH', '2066 GEN MEM GROWTH',
  '2065 GEN MEM GROWTH', '0848 LVX GROWTH', '0829 0846 & DBL  SYN GROWTH',
  '0473 GEN GROWTH', '1505 DAP VAN GROWTH', '0831 1097 1645 & DBL FEP GROWTH',
  '0829 FEP GROWTH', '1396 MEM GROWTH'.
      About 9,000 values on a 0.08-0.4 scale against "Time (Hours)", grouped by
      strain and drug into three or four replicates. They are almost certainly
      plate-reader absorbance, but the workbook states NO quantity, NO unit and
      NO wavelength for them: the letters OD do not appear anywhere in the file.
      This schema has no column that can hold a number whose quantity is
      unknown, and writing OD600 in the readout field would be a guess dressed
      as data. They are left out and reported here instead. What is lost is the
      growth-curve half of the deposit; the kill data are complete.
  'GROWTH & Tn-Seq DATA COMBINED'  per-gene fitness values, no time axis
  'TOLERANCE DATA COMBINED'        fold-enrichment summaries recomputed from the
                                   TOLERANCE sheets; derived, not readings
  the Fraction and Fold blocks inside each TOLERANCE sheet, for the same reason
  the empty '24-alt' rows on '1068 CIP TOLERANCE' and '1544 CIP TOLERANCE'
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

XLSX = "41467_2022_30967_MOESM11_ESM.xlsx"

FLOOR_BASIS = ("not stated: no plated volume, dilution, colony count or numeric "
               "limit of detection anywhere in the workbook; the recurring 0.1 "
               "is a placeholder the deposit never defines")

UNIT_CAVEAT = ("the workbook never writes CFU or a unit; read as CFU/mL from the "
               "sheet titles (TOLERANCE), the companion Fraction block (value / "
               "value at t=0) and the deposit's own note that no colonies could "
               "be recovered")

NB = re.compile(r"N\.B\..*?no WT could be recovered[^\n]*", re.I)

HEADER = re.compile(r"^(?P<strain>.+?)_(?P<x>[\d.]+)\s*X\s*(MIC\s*)?(?P<drug>.+)$",
                    re.I)


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def _txt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    s = str(v).strip()
    return "" if s.lower() in {"nan", "nat"} else s


def _letter_groups(df: pd.DataFrame, r: int) -> list[list[int]]:
    """Columns of row r holding a single replicate letter, split into runs."""
    cols = [c for c in range(df.shape[1])
            if len(_txt(df.iat[r, c])) == 1 and _txt(df.iat[r, c]).isalpha()]
    groups, run = [], []
    for c in cols:
        if run and c != run[-1] + 1:
            groups.append(run)
            run = []
        run.append(c)
    if run:
        groups.append(run)
    return [g for g in groups if len(g) >= 2]


def _time_col(df: pd.DataFrame, letter_row: int, first: int) -> int | None:
    """The time column serving a block: to its left, blank in the letter row,
    numeric in the first data row."""
    for j in range(first - 1, -1, -1):
        if _txt(df.iat[letter_row, j]):
            continue
        if not np.isnan(_num(df.iat[letter_row + 1, j])):
            return j
    return None


def _blocks(df: pd.DataFrame):
    """Yield every COUNT block on a sheet: a run of replicate letters with a
    non-empty group header above it, a time column beside it, a time-0 row, and
    time-0 values that are not all 1 (which is what the derived Fraction blocks
    look like). Fold blocks are excluded by the same two tests: they have no
    header row above and no time 0."""
    for r in range(1, df.shape[0] - 1):
        for grp in _letter_groups(df, r):
            header = ""
            for j in range(grp[0], -1, -1):
                header = _txt(df.iat[r - 1, j])
                if header:
                    break
            if not header:
                continue
            tcol = _time_col(df, r, grp[0])
            if tcol is None:
                continue
            data = []
            for i in range(r + 1, df.shape[0]):
                t = _num(df.iat[i, tcol])
                if np.isnan(t):
                    break
                data.append((i, t))
            if not any(t == 0 for _, t in data):
                continue
            zero = [_num(df.iat[i, c]) for i, t in data if t == 0 for c in grp]
            zero = [v for v in zero if not np.isnan(v)]
            if zero and all(v == 1 for v in zero):
                continue
            yield header, tcol, data, grp, r


def read(d: Path) -> pd.DataFrame:
    path = d / XLSX
    xl = pd.ExcelFile(path)

    found = []
    for sheet in xl.sheet_names:
        if "TOLERA" not in sheet.upper() or "COMBINED" in sheet.upper():
            continue
        df = pd.read_excel(path, sheet_name=sheet, header=None)

        nb = ""
        for v in df.to_numpy().ravel():
            m = NB.search(str(v))
            if m:
                nb = m.group(0).strip()
                break

        for header, tcol, data, grp, letter_row in _blocks(df):
            m = HEADER.match(header)
            strain = m.group("strain").strip() if m else header
            conc = _num(m.group("x")) if m else np.nan
            drug = m.group("drug").strip() if m else ""
            head_note = "block header as printed: '" + header + "'"
            if sheet.strip().upper().startswith("1888 VAN"):
                drug = "VAN"
                head_note += (" -- WRONG IN THE DEPOSIT. It says Gentamicin, but "
                              "the sheet is named '1888 VAN TOLERANCE' and the "
                              "workbook's 'TOLERANCE DATA COMBINED' sheet lists "
                              "this experiment as 'SP_1888 VANC' in its VAN "
                              "column, so the drug is recorded as VAN")
            readings = []
            for i, t in data:
                for c in grp:
                    v = _num(df.iat[i, c])
                    if np.isnan(v):
                        continue
                    readings.append((_txt(df.iat[letter_row, c]), t, v))
            if not readings:
                continue
            found.append({
                "sheet": sheet, "header": header, "strain": strain,
                "drug": drug, "conc": conc, "nb": nb, "head_note": head_note,
                "readings": readings,
                "sig": tuple(sorted(readings)),
                # drug names are spelled inconsistently across sheets (Cipro
                # against CIP for the same experiment), so the label key that
                # decides whether two identical blocks agree uses the first
                # three letters only.
                "label": (strain.upper(), drug.upper()[:3], conc),
            })

    # Blocks whose full content is identical are the SAME cultures printed
    # more than once. One copy is returned, whatever the labels say, so that a
    # reading is never counted twice; where the labels agree, that label is
    # used, and where they contradict each other the contradicted field is left
    # blank rather than resolved by guesswork.
    by_sig: dict[tuple, list[dict]] = {}
    for b in found:
        by_sig.setdefault(b["sig"], []).append(b)

    rows: list[dict] = []
    for sig, same in by_sig.items():
        b = dict(same[0])
        b["nb"] = next((x["nb"] for x in same if x["nb"]), "")
        labels = {x["label"] for x in same}
        printed = ", ".join(sorted({"'" + x["header"] + "' on '" + x["sheet"]
                                    + "'" for x in same}))
        dup = ""
        if len({x["sheet"] for x in same}) > 1 or len(same) > 1:
            dup = ("; the identical block -- every replicate letter, time and "
                   "value -- is printed as " + printed + ". It is returned ONCE, "
                   "not once per printing, so that the same cultures are not "
                   "counted twice")
        contradicted = len(labels) > 1
        if contradicted:
            # the parts of the label the copies still agree on may be kept; a
            # part they disagree on is blanked and the disagreement recorded.
            strains = {x["strain"] for x in same}
            drugs = {x["drug"].upper()[:3] for x in same}
            concs = {x["conc"] for x in same}
            if len(strains) > 1:
                b["strain"] = ""
            if len(drugs) > 1:
                b["drug"] = ""
            if len(concs) > 1:
                b["conc"] = np.nan
            b["head_note"] = ("block headers as printed, and they disagree: "
                              + printed)
            dup += ("; CONTRADICTION IN THE DEPOSIT: these same readings carry "
                    "two different labels -- " + printed + ". Nothing in the "
                    "file says which is right, so the fields they disagree on "
                    "are left BLANK here and both printed headers are recorded "
                    "in this note. Do not treat the two as independent "
                    "experiments; they are one set of cultures")
        for letter, t, v in b["readings"]:
            censored = ""
            note = (UNIT_CAVEAT + "; " + b["head_note"]
                    + "; concentration is the multiple of MIC named in that "
                      "header, the workbook gives no mg/L value" + dup)
            if b["nb"] and t == 24 and not contradicted                     and b["strain"].upper().startswith("WT"):
                censored = "yes"
                note += ("; the deposit states on this sheet: '" + b["nb"]
                         + "'. That is the source's own word that these 24 h "
                           "wild-type readings are non-detections, so they "
                           "are marked censored -- but no floor value is "
                           "recorded, because 'no colonies recovered' is not "
                           "a number")
            elif b["nb"] and t == 24 and contradicted:
                note += ("; the sheet carries the note '" + b["nb"] + "', but "
                         "censoring is left UNKNOWN for this block: that note "
                         "is about the wild type, and whether this block is the "
                         "wild type is exactly what the deposit contradicts "
                         "itself about")
            rows.append({
                "source_file": XLSX, "sheet": b["sheet"],
                "strain": b["strain"], "drug": b["drug"],
                "concentration": b["conc"],
                "conc_unit": "xMIC" if not np.isnan(b["conc"]) else "",
                "arm": " / ".join(sorted({x["header"] for x in same})),
                "replicate": letter,
                "time_h": t, "cfu_per_ml": v, "censored": censored,
                "floor_basis": FLOOR_BASIS, "readout": "CFU", "notes": note,
            })

    if not rows:
        return empty()
    return finish(pd.DataFrame(rows), "ZHU2022")
