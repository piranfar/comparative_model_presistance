"""BISHAI2023_JHU083 -- Nature Communications Source Data for JHU083 (a
glutamine-antagonist prodrug) against tuberculosis, one workbook of twenty
sheets, one sheet per figure.

WHAT IS IN THE FILE, and what this reader takes.

Only three of the twenty sheets carry a viable count against any kind of time
axis, and this reader takes those three panels and nothing else:

  Fig 1  :: Fig 1f   "Log10CFU" in infected BMDM wells, Day 0 / 3 / 5, four
                     arms (BMDM alone, and BMDM + 10X DON / JHU083 / INH),
                     three wells each, labelled C1-C3 by the sheet.
  Fig 2  :: Fig 2b   "Lung CFU (Log10)", Week 0 / 2 / 5, one row per mouse,
                     the sheet's own ids WT-PBS-Lung-M1 ... WT-RIF-Lung-M5.
                     Its week axis has no stated origin and yields NO time_h
                     -- see below.
  Fig S1 :: Fig S1a  "Log10CFU", Days 1 / 3 / 5, arms PBS / INH / 1X DON /
                     10X DON across merged three-column blocks.

So the only usable time axis in this deposit is in vitro: Fig 1f at 0 / 72 /
120 h and Fig S1a at 24 / 72 / 120 h. Time zero exists only in Fig 1f.

Everything else in the workbook is either not a count (flow cytometry in Fig 4,
5, S9-S15; metabolomics in Fig 6, S16-S18; body weight, lung weight, survival,
granuloma area, western blot) or is a count with NO time attached, which cannot
be placed on a time axis without going outside the deposit:

  Fig 1e   MBC assay: CFU per tube (log10) against JHU083 2-64 ug/ml. No
           sampling time anywhere on the sheet. Worth recording even though it
           is not read here: the two highest concentrations are written as a
           literal 0 in a column headed "CFU per tube (log10)", i.e. log10 = 0,
           one CFU per tube -- a no-growth placeholder, not a measured count,
           and the sheet says nothing about what it means.
  Fig 3b   SCID lung CFU, one endpoint, no week or day stated.
  Fig S2a  Lung CFU for JHU083 given daily (D) or on alternate days (A), one
           endpoint, no time stated.
  Fig S3a  C3HeB/FeJ lung CFU and Fig S3b C3H lung CFU, one endpoint each, no
           time stated; "*" there means "Mouse died prematurely" (the sheet
           says so) and is not a censored count.

THE FLOOR. There is none, and this was checked rather than assumed: a scan of
every string cell on all twenty sheets finds no detection limit, no limit of
quantification, no plated volume, no dilution factor, no raw colony count and
no plating medium. Every CFU panel reports log10 values only. So
floor_cfu_per_ml is blank on every row and floor_basis says why. Nothing in the
workbook fixes a floor by arithmetic either -- there are no colonies and no
volumes to work from.

WHAT THE WORKBOOK DOES NOT SAY, and is therefore left blank here.

  * The organism. The only place the workbook names it is the Fig 2 sheet,
    whose panel Fig 2c is headed "DON concentration in Mtb infected lungs". So
    the Fig 2b rows carry organism "Mtb" -- the sheet's own abbreviation,
    unexpanded -- and the Fig 1f and Fig S1a rows carry a blank organism, with
    a note, because those sheets never name what was cultured.
  * The bacterial strain: never named on any sheet. "WT", "SCID", "C3HeB/FeJ"
    and "C3H" are mouse genotypes, not bacterial strains, so `strain` stays
    blank and the mouse genotype goes in notes.
  * What "10X" is ten times. Panel Fig S1b, on the same sheet as Fig S1a,
    writes the same treatments as "1XMIC DON", "10X MIC DON" and "32XMIC INH",
    which points at the MIC -- but Fig S1a itself writes only "1X DON" and
    "10X DON", and its INH arm carries no multiplier at all. So conc_unit is
    the source's own "X", not "xMIC", and the discrepancy is in notes.
  * The dose of JHU083 and RIF in Fig 2b: the arms are labelled by drug name
    only, so `concentration` is blank.
  * The denominator of the counts. Fig 1f and Fig S1a are headed "Log10CFU"
    with no volume; Fig 2b is CFU per lung. cfu_per_ml holds those numbers as
    the file gives them (10 ** the log10 value); no volume was invented to
    convert them, and every row says so in notes.

TWO THINGS A LATER READER SHOULD KNOW ABOUT THE READINGS THEMSELVES.

  * Fig 1f's Day 0 column is the same three numbers (4.99, 5.08, 5.09) under
    all four arms. One inoculum reading per well, reported once per arm: the
    twelve Day 0 rows are three readings, not twelve. They are kept as the
    sheet writes them and flagged.
  * FIG 2b GETS NO TIME, and this is the one place where taking the sheet at
    face value would have been wrong. The axis reads "Week 0 / Week 2 /
    Week 5" and the workbook never says what week zero counts from. Week 0 is
    not the start of drug exposure, and the deposit's own numbers show it: the
    four Week 0 readings are 79-123 CFU per lung against 10**6.4-10**7.4 in
    the same panel at Week 2 -- an implantation-level count, not a treatment
    baseline -- and Week 0 exists only under the PBS-labelled mice, so it is a
    separate, earlier sacrifice group rather than a time zero shared with the
    JHU083 and RIF arms. Once Week 0 is not exposure zero, Week 2 and Week 5
    have no known origin either, and 336 h and 840 h of drug exposure would be
    numbers this deposit does not contain. All 31 readings are kept with their
    counts; time_h is blank on every one and the notes carry the sheet's own
    "Week n" label and the reasoning. This follows what the corpus already
    does with an unanchored in vivo sacrifice (PZA_PARP1_2023's "DAY 1 post
    infection" and "end of treatment" panels, WALTER2021_RSRATIO's mice whose
    two day columns disagree).
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty

FILE = "41467_2023_43304_MOESM6_ESM.xlsx"

NO_FLOOR = (
    "no floor is recoverable: a scan of every string cell on all twenty sheets "
    "of this workbook finds no stated detection limit, no plated volume, no "
    "dilution factor, no raw colony count and no plating medium; every CFU "
    "panel reports log10 values only, so nothing fixes a floor by arithmetic "
    "either")

LOG_NOTE = ("the sheet reports log10 values; cfu_per_ml is 10 ** that value, "
            "no other transformation")

NO_DENOM = ('the sheet heads this panel "Log10CFU" and states no volume or '
            "other denominator, so cfu_per_ml holds the count as the file "
            "gives it")

X_NOTE = ("concentration unit is the sheet's own \"X\": the workbook does not "
          "say what the multiplier is a multiple of")

MIC_NOTE = ("panel Fig S1b on this same sheet writes the same treatments as "
            "\"1XMIC DON\", \"10X MIC DON\" and \"32XMIC INH\", which points "
            "at the MIC, but panel Fig S1a itself writes only \"1X DON\" / "
            "\"10X DON\" and gives its INH arm no multiplier, so xMIC is not "
            "assumed here")

NO_ORGANISM = ("this sheet does not name the organism; only the Fig 2 sheet "
               "does, in its panel Fig 2c header \"DON concentration in Mtb "
               "infected lungs\"")

# Fig 2b carries no usable time.  The sheet's axis is "Week 0 / Week 2 /
# Week 5" and nothing in the workbook says what week zero counts from, so
# hours since drug exposure began are not recoverable -- and the deposit's own
# numbers rule out the reading that would make the axis a treatment clock.
# See the docstring for the arithmetic.  Handled the way the corpus already
# handles this case (PZA_PARP1_2023 Figure 6 b, WALTER2021_RSRATIO's
# euthanized-early mice): keep the count, leave time_h blank, say why.
WEEK_NOTE = (
    "no time_h: the sheet's axis is \"Week 0 / Week 2 / Week 5\" and the "
    "workbook nowhere states what week zero counts from. It is not the start "
    "of drug exposure: the Week 0 readings are 79-123 CFU per lung against "
    "10**6.4-10**7.4 in the same panel at Week 2, an implantation-level count "
    "rather than a treatment baseline, and Week 0 exists only for the "
    "PBS-labelled mice -- a separate, earlier sacrifice group, not a time "
    "zero shared by the JHU083 and RIF arms. Hours since exposure began are "
    "therefore not in this deposit and none is invented here")


def _grid(path: Path, sheet: str) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet, header=None)


def _find(raw: pd.DataFrame, text: str) -> tuple[int, int]:
    """Row and column of the first cell whose stripped text is `text`."""
    for i in range(raw.shape[0]):
        for j in range(raw.shape[1]):
            v = raw.iat[i, j]
            if isinstance(v, str) and v.strip() == text:
                return i, j
    raise ValueError(f"{FILE}: anchor {text!r} not found")


def _num(v) -> float:
    return float(v) if isinstance(v, (int, float, np.number)) \
        and not isinstance(v, bool) and np.isfinite(v) else np.nan


def _drug_conc(label: str) -> tuple[str, float, str]:
    """Drug, concentration and unit from an arm label, as the sheet writes it.

    "BMDM alone" and "PBS" are the untreated arms and carry no drug.
    "10X DON" gives DON at 10 "X"; "INH" alone gives INH at no stated
    concentration.
    """
    s = re.sub(r"^BMDM\s*\+\s*", "", label.strip())
    if s.lower() in ("bmdm alone", "pbs"):
        return "", np.nan, ""
    m = re.match(r"^(\d+(?:\.\d+)?)\s*X\s*(.+)$", s)
    if m:
        return m.group(2).strip(), float(m.group(1)), "X"
    return s, np.nan, ""


def _row(**kw) -> dict:
    base = dict(source_file=FILE, readout="CFU", floor_cfu_per_ml=np.nan,
                floor_basis=NO_FLOOR, strain="", tech_replicate="")
    base.update(kw)
    return base


def _fig1f(path: Path) -> list[dict]:
    """Fig 1 :: Fig 1f -- Log10CFU in infected BMDM wells, Day 0 / 3 / 5."""
    raw = _grid(path, "Fig 1")
    hdr, gcol = _find(raw, "Groups")

    days = []
    for c in range(gcol + 1, raw.shape[1]):
        m = re.fullmatch(r"Day\s+(\d+(?:\.\d+)?)", str(raw.iat[hdr, c]).strip())
        if m:
            days.append((c, float(m.group(1))))
    if not days:
        raise ValueError(f"{FILE}: Fig 1f has no 'Day N' columns")

    out = []
    for i in range(hdr + 1, raw.shape[0]):
        lab = raw.iat[i, gcol]
        lab = lab.strip() if isinstance(lab, str) else ""
        if not lab:
            continue
        if lab.lower().startswith(("average", "p-value")):
            break
        m = re.fullmatch(r"(?P<arm>.+?)\s+(?P<rep>C\d+)", lab)
        if not m:
            continue
        arm, rep = m.group("arm").strip(), m.group("rep")
        drug, conc, unit = _drug_conc(arm)
        for c, day in days:
            v = _num(raw.iat[i, c])
            if not np.isfinite(v):
                continue
            note = [LOG_NOTE,
                    "day converted to hours (the sheet's axis is days)",
                    NO_DENOM,
                    "intracellular counts from infected BMDM wells; C1-C3 are "
                    "the sheet's own labels for the three wells, and it does "
                    "not say whether they are biological or technical "
                    "replicates",
                    NO_ORGANISM]
            if unit:
                note.append(X_NOTE)
            if day == 0:
                note.append("Day 0 is the same three numbers (4.99, 5.08, "
                            "5.09) under all four arms of this panel: one "
                            "inoculum reading per well, repeated once per arm, "
                            "so the twelve Day 0 rows are three readings")
            out.append(_row(
                sheet="Fig 1 :: Fig 1f", organism="", drug=drug,
                concentration=conc, conc_unit=unit, arm=arm, replicate=rep,
                time_h=day * 24.0, cfu_per_ml=10.0 ** v,
                notes="; ".join(note)))
    return out


def _fig2b(path: Path) -> list[dict]:
    """Fig 2 :: Fig 2b -- lung CFU (log10) per mouse, Week 0 / 2 / 5."""
    raw = _grid(path, "Fig 2")
    anchor, acol = _find(raw, "Lung CFU (Log10)")
    hdr = anchor + 1

    weeks = []
    for c in range(acol, raw.shape[1]):
        m = re.fullmatch(r"Week\s+(\d+(?:\.\d+)?)",
                         str(raw.iat[hdr, c]).strip())
        if m:
            weeks.append((c, float(m.group(1))))
    if not weeks:
        raise ValueError(f"{FILE}: Fig 2b has no 'Week N' columns")

    # the organism, in the sheet's own abbreviation, from the Fig 2c header
    organism = "Mtb" if any(
        isinstance(v, str) and "Mtb infected" in v for v in raw.values.ravel()
    ) else ""
    org_note = ("organism from the Fig 2c header on this sheet, \"DON "
                "concentration in Mtb infected lungs\"; \"Mtb\" is left "
                "unexpanded" if organism else NO_ORGANISM)

    out = []
    for i in range(hdr + 1, raw.shape[0]):
        lab = raw.iat[i, 0]
        lab = lab.strip() if isinstance(lab, str) else ""
        m = re.fullmatch(r"(?P<host>\w+)-(?P<arm>.+?)-Lung-(?P<rep>M\d+)", lab)
        if not m:
            continue
        arm = m.group("arm")
        drug, conc, unit = _drug_conc(arm)
        for c, week in weeks:
            v = _num(raw.iat[i, c])
            if not np.isfinite(v):
                continue
            note = [LOG_NOTE,
                    f"the sheet's own time label for this reading is "
                    f"\"Week {week:g}\"",
                    WEEK_NOTE,
                    "in vivo organ burden: this is CFU per lung, not per mL; "
                    "cfu_per_ml carries the per-organ count because that is "
                    "the column the schema has, and no volume was invented to "
                    "convert it",
                    f"mouse genotype {m.group('host')} as the row label writes "
                    "it; the workbook never names a bacterial strain",
                    f"the sheet's own row id is \"{lab}\"",
                    org_note,
                    "the arm is labelled by drug name only, so no "
                    "concentration or dose is available" if drug else
                    "PBS arm: the sheet's untreated control"]
            if week == 0:
                note.append("Week 0 is present only for the PBS-labelled mice, "
                            "and only for four of the five")
            out.append(_row(
                sheet="Fig 2 :: Fig 2b", organism=organism, drug=drug,
                concentration=conc, conc_unit=unit, arm=arm, replicate=lab,
                time_h=np.nan, cfu_per_ml=10.0 ** v,
                notes="; ".join(note)))
    return out


def _figS1a(path: Path) -> list[dict]:
    """Fig S1 :: Fig S1a -- Log10CFU, Days 1 / 3 / 5, merged arm blocks."""
    raw = _grid(path, "Fig S1")
    hdr, dcol = _find(raw, "Days")

    # data rows: numeric day in the Days column, until the block ends
    body = []
    for i in range(hdr + 1, raw.shape[0]):
        day = _num(raw.iat[i, dcol])
        if np.isfinite(day):
            body.append((i, day))
        elif body:
            break
    if not body:
        raise ValueError(f"{FILE}: Fig S1a has no numeric Day rows")
    idx = [i for i, _ in body]

    # the row above the header carries the "Average" and "P-value" bands; the
    # readings stop where the first of those begins
    stop = raw.shape[1]
    if hdr > 0:
        for c in range(dcol + 1, raw.shape[1]):
            v = raw.iat[hdr - 1, c]
            if isinstance(v, str) and v.strip():
                stop = c
                break

    out, arm, rep = [], "", 0
    for c in range(dcol + 1, stop):
        v = raw.iat[hdr, c]
        if isinstance(v, str) and v.strip():
            arm, rep = v.strip(), 0
        if not arm:
            continue
        col = [_num(raw.iat[i, c]) for i in idx]
        if not any(np.isfinite(x) for x in col):
            continue        # spacer column between the blocks
        rep += 1
        drug, conc, unit = _drug_conc(arm)
        for (i, day), x in zip(body, col):
            if not np.isfinite(x):
                continue
            note = [LOG_NOTE,
                    "day converted to hours (the sheet's axis is days)",
                    NO_DENOM,
                    "the three columns under each arm carry no labels, so "
                    "they are numbered 1-3; the sheet does not say whether "
                    "they are biological or technical replicates",
                    "this panel has no Day 0: its first reading is Day 1",
                    NO_ORGANISM]
            if unit:
                note += [X_NOTE, MIC_NOTE]
            elif drug:
                note.append("this arm is labelled with a drug name only, no "
                            "multiplier; " + MIC_NOTE)
            out.append(_row(
                sheet="Fig S1 :: Fig S1a", organism="", drug=drug,
                concentration=conc, conc_unit=unit, arm=arm,
                replicate=str(rep), time_h=day * 24.0, cfu_per_ml=10.0 ** x,
                notes="; ".join(note)))
    return out


def read(d: Path) -> pd.DataFrame:
    path = d / FILE
    if not path.exists():
        return empty()
    rows = _fig1f(path) + _fig2b(path) + _figS1a(path)
    return pd.DataFrame(rows) if rows else empty()
