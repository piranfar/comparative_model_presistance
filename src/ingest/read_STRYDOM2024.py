"""STRYDOM2024 -- TBI-223 and linezolid, one figshare CSV holding many stacked blocks.

47111650.csv is not a table.  It is a sequence of blocks, each introduced by a
figure line in column 0 and a panel line in column 1, then its own header row
(always ending FIGURE, SECTION), then its rows, then a blank line.  ELEVEN
blocks in all, and every row of the file belongs to one of them: 330 + 238 +
45 + 45 + 31 + 32 + 333 + 258 + 16 + 490 + 122 data rows, plus the figure,
panel, header and blank lines between them.

READ (the six that carry counts):
    Figure 2  Panel A: Mono-therapy         ID, TIME_DAY, LOGCFU, DRUG,
    Figure 2  Panel B: Mono-therapy           TOTAL_WEEKLY_DOSE, FREQ
    Figure 2  Panel A: Combination therapy  TIME_DAY, LOGCFU, DOSE, DRUG
    Figure 2  Panel B: Combination therapy
    Figure 3  Panel A: LZD monotherapy      TIME_DAY, LOG10CFU, SD, DOSE, DRUG
    Figure 3  Panel B: NIX-TB observations  ID, TIME_DAY, LOG10CFU, DRUG

NOT READ: the pharmacokinetic blocks (Figure 2 Panels A and B
Pharmacokinetics, Panel C TBI-223, Panel C LZD, Figure 3 Panel E LZD 300 mg
lesions).  Those report drug concentrations in plasma, lung, lesion and caseum,
not bacterial counts.  They are worth one remark: the PK blocks carry a BLQ
column flagging readings below the limit of quantification, so this deposit
knows perfectly well how to record a censored measurement -- and records none
for any of its CFU blocks.

THE DENOMINATOR.  The count columns are labelled only LOGCFU and LOG10CFU.  The
file never says per what: per mL, per sputum sample, per lung.  The counts are
therefore carried into cfu_per_ml as 10**value, and readout says in words that
the denominator is not stated, so nothing downstream can quietly read them as
per-mL without noticing.  (Contrast the EDOO2026 reader, which drops that
study's mouse blocks precisely BECAUSE their header says "log CFU/lungs": a
value the source states is not per mL must never be written into a per-mL
column.  A value whose denominator the source does not state is a different
case, and is kept with the doubt attached.)

NEGATIVE TIMES.  Two of the blocks report pre-treatment baselines at TIME_DAY
-17, -3, -2 and -1.  The schema's time_h cannot be negative, so those rows keep
their reading but their time_h is left blank, with the source's own day written
into notes.

Figure 3 Panel A is not a set of readings at all: its own preamble says it is
"Data from LZD EBA studies in Dietze 2008 study", with 10 subjects on QD and 9
on BID, and it carries an SD column.  Those rows are means of another study's
subjects, and their readout says so.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

FILENAME = "47111650.csv"
CFU_COLS = ("LOGCFU", "LOG10CFU")
# "15 mg/kg BID", "100 mg/kg QD" -- take the dose only where a unit is written
DOSE_RE = re.compile(r"^\s*([\d.]+)\s*(mg/kg|mg)\b", re.I)
CONTROL = re.compile(r"control|untreated", re.I)

FLOOR_BASIS = (
    "not stated: no block of this file gives a limit of detection or "
    "quantification for its colony counts. The file's pharmacokinetic blocks do "
    "carry a BLQ flag for drug concentrations, so the deposit records censoring "
    "where it has it -- and records none for the counts"
)


def _blocks(raw: pd.DataFrame):
    """Yield (figure, panel, header_cols, positions, first_row, last_row)."""
    figure = panel = ""
    i = 0
    n = len(raw)
    while i < n:
        row = [str(x).strip() for x in raw.iloc[i]]
        if row[0]:
            figure, panel = row[0], ""
        if len(row) > 1 and row[1]:
            panel = row[1]
        nonempty = [(j, v) for j, v in enumerate(row) if v and j >= 2]
        names = [v for _, v in nonempty]
        if "FIGURE" in names and "SECTION" in names:
            pos = [j for j, _ in nonempty]
            start = i + 1
            j = start
            while j < n:
                r2 = [str(x).strip() for x in raw.iloc[j]]
                if r2[0] or (len(r2) > 1 and r2[1]):
                    break
                if not any(r2[k] for k in pos):
                    break
                j += 1
            yield figure, panel, names, pos, start, j
            i = j
            continue
        i += 1


def read(d: Path) -> pd.DataFrame:
    path = d / FILENAME
    if not path.exists():
        hits = list(d.rglob(FILENAME))
        if not hits:
            return empty()
        path = hits[0]

    raw = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)

    out = []
    for figure, panel, names, pos, start, stop in _blocks(raw):
        cfu_name = next((c for c in names if c in CFU_COLS), None)
        if cfu_name is None:
            continue                       # a pharmacokinetic block
        blk = raw.iloc[start:stop, pos].copy()
        blk.columns = names

        is_mean = "SD" in names
        # Free-text lines that the block puts between its panel title and its
        # header. A preamble line has exactly one filled cell from column 2 on;
        # anything wider is a data row belonging to the block above.
        preamble_lines = []
        for k in range(max(0, start - 4), start - 1):
            cells = [str(raw.iat[k, c]).strip() for c in range(2, raw.shape[1])]
            filled = [c for c in cells if c]
            if len(filled) == 1 and filled[0] not in names:
                preamble_lines.append(filled[0])
        preamble = " | ".join(preamble_lines)

        for _, r in blk.iterrows():
            try:
                val = float(r[cfu_name])
            except (TypeError, ValueError):
                continue
            if not np.isfinite(val):
                continue

            day_note = ""
            time_h = np.nan
            if "TIME_DAY" in names:
                try:
                    day = float(r["TIME_DAY"])
                except (TypeError, ValueError):
                    day = np.nan
                if np.isfinite(day):
                    if day < 0:
                        day_note = ("the source gives TIME_DAY = %g, a "
                                    "pre-treatment baseline; time_h cannot be "
                                    "negative in this schema so it is left "
                                    "blank" % day)
                    else:
                        time_h = day * 24.0

            label = str(r["DOSE"]).strip() if "DOSE" in names else ""
            if not label and "TOTAL_WEEKLY_DOSE" in names:
                label = "TOTAL_WEEKLY_DOSE=%s, FREQ=%s" % (
                    str(r["TOTAL_WEEKLY_DOSE"]).strip(), str(r["FREQ"]).strip())
            arm = label or str(r.get("SECTION", "")).strip()

            drug = str(r["DRUG"]).strip() if "DRUG" in names else ""
            zero_dose = False
            if "TOTAL_WEEKLY_DOSE" in names:
                zero_dose = str(r["TOTAL_WEEKLY_DOSE"]).strip() in ("0", "0.0")
            control = bool(CONTROL.search(label)) or zero_dose
            drug_note = ""
            if control and drug:
                drug_note = ('an untreated / control row, so drug is left blank; '
                             'the file still files it under DRUG = "%s" because '
                             "that is the panel it belongs to" % drug)
                drug = ""

            cval, cunit = np.nan, ""
            m = DOSE_RE.match(label)
            if m and not control:
                cval, cunit = float(m.group(1)), m.group(2).lower()
            elif label and not control and re.match(r"^\s*[\d.]+\s", label):
                drug_note = "; ".join(x for x in (drug_note, (
                    'the dose label "%s" gives a number with no unit, so '
                    "concentration is left blank and the label is kept verbatim "
                    "in arm" % label)) if x)
            elif label.startswith("TOTAL_WEEKLY_DOSE=") and not control:
                drug_note = "; ".join(x for x in (drug_note, (
                    "the file's TOTAL_WEEKLY_DOSE and FREQ columns carry no "
                    "unit, so concentration is left blank and both values are "
                    "kept verbatim in arm")) if x)

            sd_note = ""
            if is_mean:
                try:
                    sd_note = "the block's SD for this point is %g" % float(r["SD"])
                except (TypeError, ValueError):
                    sd_note = ""

            readout = ("mean log10 CFU (summary, not a single reading); the "
                       "denominator is not stated by the source"
                       if is_mean else
                       "CFU; the denominator is not stated by the source -- the "
                       "column is labelled only %s" % cfu_name)

            out.append({
                "source_file": FILENAME, "sheet": "%s / %s" % (figure, panel),
                "organism": "", "strain": "",
                "drug": drug, "concentration": cval, "conc_unit": cunit,
                "arm": arm,
                "replicate": str(r["ID"]).strip() if "ID" in names else "",
                "time_h": time_h,
                "cfu_per_ml": float(10.0 ** val),
                "floor_basis": FLOOR_BASIS,
                "readout": readout,
                "notes": "; ".join(x for x in (day_note, drug_note, sd_note,
                                               preamble) if x),
            })

    if not out:
        return empty()

    df = pd.DataFrame(out)
    common = (
        "the block reports log10 CFU; cfu_per_ml here is 10**value, not the "
        "log. Day converted to hours (source in days). NO DENOMINATOR IS "
        "STATED for the counts anywhere in the file, so whether they are per "
        "mL, per sputum sample or per organ is unknown and readout says so. No "
        "limit of detection, colony count, dilution or plated volume appears "
        "anywhere in the file. Organism and strain are blank because no CFU "
        "block names the bacterium; the STRAIN column that does appear belongs "
        "to the pharmacokinetic blocks and names the host animal (balbc, c57, "
        "beagle, Sprague-Dawley), not the organism being counted."
    )
    df["notes"] = [("; ".join(x for x in (n, common) if x)) for n in df["notes"]]
    return finish(df, "STRYDOM2024")
