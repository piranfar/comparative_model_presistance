"""MABS_CF_FIGSHARE2025 -- figshare 28398275, "Data on Fig 4": intracellular
CFU/mL of an ATCC reference strain and sixteen clinical isolates in THP-1-style
infection, with and without amikacin, at 2, 24, 48 and 72 hours.

THE LAYOUT. One sheet, "Sheet1", holding two blocks of identical shape:

    row 1   caption, in column B, the only prose in the file
    row 2   header: "Time (hours) " in column A, then a strain label every third
            column -- "ATCC", then the integers 1..16 -- each merged across the
            three replicate columns beneath it (B2:D2, E2:G2, ... AX2:AZ2)
    rows 3-6  one row per sampling time: 2, 24, 48, 72

and the same again from row 8. The two captions are the file's own words for the
two arms:

    "Intracellular growth (CFU/mL) of smooth and rough strains under
     amikacin-free conditions, measured in triplicates for each strain."
    "Intracellular growth (CFU/mL) of smooth and rough strains under
     amikacin condition, measured in triplicates for each strain."

17 strains x 3 replicates x 4 times x 2 arms = 408 readings, and 408 numeric
cells is exactly what the sheet holds. The arm label, the drug, the readout and
the replicate count are all PARSED out of those two captions rather than typed
in here, so a changed deposit is noticed rather than silently absorbed.

THERE IS NO FLOOR IN THIS DEPOSIT, BY ANY ROUTE, and that is checkable rather
than asserted: the workbook contains exactly four distinct text strings -- the
two captions above, "Time (hours) " and "ATCC" -- and nothing else. No limit of
detection, no limit of quantification, no plated volume, no dilution, no colony
count, no README, no cell comment, no defined name. floor_cfu_per_ml is blank on
all 408 rows and floor_basis says so. Nor is there an implicit floor to find: no
value is zero, the smallest is 6.0e3, and nothing repeats at the bottom of the
distribution the way a substituted limit would (the twelve smallest distinct
values occur between once and three times each). Every count is an integer
multiple of 1,000, which is the sheet's reporting granularity and is consistent
with a back-calculation from a plate count -- but the workbook states neither
the dilution nor the volume, so no floor follows from it and none is invented.

WHAT THE WORKBOOK DOES NOT SAY, and is therefore left blank here:

  * THE SPECIES. "smooth and rough strains" is the only description; the file
    never names an organism, so `organism` is blank. (The corpus manifest
    records M. abscessus for this study from outside the deposit; that is not
    transcribed into the data, per the schema's rule.)
  * THE STRAINS, beyond the labels themselves. `strain` carries the workbook's
    own "ATCC" and "1".."16" verbatim. Which isolates are smooth and which
    rough is not stated per strain, only collectively in the caption.
  * THE AMIKACIN CONCENTRATION and the exposure schedule. Neither appears in
    the workbook, so `concentration` and `conc_unit` are blank. The corpus
    manifest's entry for this study records the article's own methods wording;
    that is where to look, and nothing from it is put into a numeric column.
  * WHEN EXPOSURE BEGAN relative to the sheet's clock. The header says only
    "Time (hours)". time_h is that column verbatim; the earliest reading is 2 h,
    so THERE IS NO TIME ZERO in this deposit and none is manufactured.
  * WHETHER THE TRIPLICATES ARE BIOLOGICAL OR TECHNICAL. The caption says
    "measured in triplicates for each strain" and stops there, so the three
    columns are numbered 1-3 in `replicate` and `tech_replicate` stays blank.

The counts are intracellular -- bacteria recovered from infected cells -- and
the deposit labels them CFU/mL, so they go into cfu_per_ml under the source's
own label, but they are not the density of a broth culture and should not be
read as one.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

FILE = "Data_on_Fig_4.xlsx"
SHEET = "Sheet1"

TIME_HDR = re.compile(r"^time\s*\(hours?\)$", re.I)
# "...under amikacin-free conditions, measured in triplicates..."
COND_RE = re.compile(r"\bunder\s+(?P<cond>.+?)\s+conditions?\b", re.I)
# "Intracellular growth (CFU/mL) of ..."
UNIT_RE = re.compile(r"\((CFU)\s*/\s*mL\)", re.I)
FREE_RE = re.compile(r"^(?P<drug>.+?)[- ]free$", re.I)

# Anything that would state or fix a floor. Searched over every string in the
# workbook so that the claim "this deposit states no limit" is tested on each
# run rather than trusted from the day the reader was written.
FLOOR_WORDS = re.compile(
    r"limit of detection|detection limit|\bL\.?O\.?D\b|\bL\.?O\.?Q\b|"
    r"limit of quantification|quantitation|below\s+(the\s+)?limit|"
    r"plated|plating|\bul\b|\bµl\b|\bmicrolit|dilution|undetect|censored",
    re.I)

FLOOR_BASIS = (
    "blank because the workbook fixes no floor by any route: its only text is "
    'the two block captions, the header "Time (hours) " and the label "ATCC" '
    "-- no detection or quantification limit, no plated volume, no dilution "
    "and no colony count anywhere in the file, and no zero or repeated "
    "minimum in the 408 values that would betray a substituted limit")


def _blocks(raw: pd.DataFrame) -> list[tuple[int, int]]:
    """(caption row, header row) for each block, found by the time header."""
    out = []
    for i in range(len(raw)):
        v = raw.iat[i, 0]
        if isinstance(v, str) and TIME_HDR.match(v.strip()):
            out.append((i - 1, i))
    return out


def _caption(raw: pd.DataFrame, row: int) -> str:
    if row < 0:
        return ""
    for j in range(raw.shape[1]):
        v = raw.iat[row, j]
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def read(d: Path) -> pd.DataFrame:
    src = d / FILE
    if not src.exists():
        return empty()

    raw = pd.read_excel(src, sheet_name=SHEET, header=None)

    # Re-check the no-floor claim against the file itself, every run.
    strings = [str(v).strip() for v in raw.values.ravel()
               if isinstance(v, str) and str(v).strip()]
    hits = sorted({s for s in strings if FLOOR_WORDS.search(s)})
    if hits:
        raise ValueError(
            "%s: the workbook now carries text that may state or fix a "
            "detection limit, which it did not when this reader was written; "
            "read it before trusting the blank floor: %r" % (FILE, hits))

    blocks = _blocks(raw)
    if not blocks:
        raise ValueError("%s: no 'Time (hours)' header row" % FILE)

    rows = []
    for cap_row, hdr in blocks:
        caption = _caption(raw, cap_row)

        cm = COND_RE.search(caption)
        if not cm:
            raise ValueError("%s: block at row %d states no condition: %r"
                             % (FILE, hdr, caption))
        arm = cm.group("cond").strip()
        fm = FREE_RE.match(arm)
        # "amikacin-free" is the control: the drug is named but not given.
        drug = "" if fm else arm.lower()
        withheld = fm.group("drug").lower() if fm else ""

        um = UNIT_RE.search(caption)
        readout = um.group(1).upper() if um else ""

        # strain labels: every non-empty cell of the header row past column A,
        # each merged over the replicate columns that follow it
        labels = [(c, raw.iat[hdr, c]) for c in range(1, raw.shape[1])
                  if pd.notna(raw.iat[hdr, c])]
        if not labels:
            raise ValueError("%s: no strain labels in header row %d"
                             % (FILE, hdr))
        bounds = [c for c, _ in labels] + [raw.shape[1]]

        # data rows: below the header, until column A stops being a number
        times = []
        for i in range(hdr + 1, len(raw)):
            v = raw.iat[i, 0]
            if isinstance(v, str) and TIME_HDR.match(v.strip()):
                break
            try:
                t = float(v)
            except (TypeError, ValueError):
                continue
            if np.isfinite(t):
                times.append((i, t))
        if not times:
            raise ValueError("%s: no numeric time rows under header %d"
                             % (FILE, hdr))

        note = [
            'the workbook says of this block, verbatim: "%s"' % caption,
            'time is the sheet\'s own "Time (hours)" column, taken as stated; '
            "the workbook does not say when exposure began relative to that "
            "clock, and the earliest reading is %g h, so this deposit has no "
            "t = 0" % min(t for _, t in times),
            "intracellular counts recovered from infected cells; the deposit "
            "labels them CFU/mL and they are carried under that label, but "
            "they are not a broth-culture density",
            "the caption says \"measured in triplicates\" and does not say "
            "whether the three columns are biological or technical replicates, "
            "so they are numbered 1-3 and tech_replicate is left blank",
            "strain label is the workbook's own; the file never names the "
            "species, and does not say which isolates are smooth and which "
            "rough",
            "every count in the sheet is an integer multiple of 1,000, the "
            "sheet's reporting granularity; the workbook states no dilution "
            "or plated volume, so no floor follows from it",
        ]
        if drug:
            note.append("the workbook states no amikacin concentration or "
                        "exposure schedule, so concentration and conc_unit "
                        "are blank")
        elif withheld:
            note.append("%s-free block: the no-drug counterpart of the %s "
                        "arm -- the same 17 strain labels at the same times in "
                        "the same sheet" % (withheld, withheld))

        for k, (lcol, label) in enumerate(labels):
            strain = (("%g" % label) if isinstance(label, (int, float,
                                                           np.number))
                      else str(label).strip())
            cols = list(range(lcol, bounds[k + 1]))
            for i, t in times:
                for rep, c in enumerate(cols, start=1):
                    v = raw.iat[i, c]
                    if isinstance(v, str) and v.strip():
                        # A deposit writes a below-limit reading as text
                        # ("<10", "ND", "0 (below L.O.D)"). Dropping such a
                        # cell silently would erase the censoring this corpus
                        # exists to count, so refuse rather than continue.
                        raise ValueError(
                            "%s: sheet row %d, strain %s, replicate %d holds "
                            "the text %r where a count is expected; read it "
                            "before trusting this reader's blank floor"
                            % (FILE, i + 1, strain, rep, v.strip()))
                    if not isinstance(v, (int, float, np.number)) \
                            or not np.isfinite(v):
                        continue
                    rows.append({
                        "source_file": FILE,
                        "sheet": SHEET,
                        "organism": "",
                        "strain": strain,
                        "drug": drug,
                        "concentration": np.nan,
                        "conc_unit": "",
                        "arm": arm,
                        "replicate": str(rep),
                        "tech_replicate": "",
                        "time_h": float(t),
                        "colonies": np.nan,
                        "dilution": np.nan,
                        "plated_volume_ul": np.nan,
                        "cfu_per_ml": float(v),
                        "floor_cfu_per_ml": np.nan,
                        "floor_basis": FLOOR_BASIS,
                        "readout": readout,
                        "notes": "; ".join(note),
                    })

    return finish(pd.DataFrame(rows), "MABS_CF_FIGSHARE2025")
