"""BIOENERGETIC2025 -- Nature Communications Source Data, 75 sheets.

10.1038/s41467-025-60302-6, file 41467_2025_60302_MOESM13_ESM.xlsx.
CC BY-NC-ND: used here, not redistributed.

Every sheet carries its own prose caption in row 2, which is how the drug, the
concentration, the strains and the medium were established for each one; the
caption is quoted verbatim in the notes of every row read from it. Seventeen
sheets carry a quantity against "Time (hours)"; those are read. The other fifty-eight
are metabolite pools, oxygen-consumption and acidification rates, mutation
rates, resistance-evolution MIC curves, expression values, flow cytometry and
checkerboards, and are not.

THE THING THAT MATTERS ABOUT THIS DEPOSIT: THERE ARE ALMOST NO COUNTS IN IT.
Fourteen of the fifteen time courses report "Fraction survival" -- CFU divided
by the CFU of the same culture at time 0 (the Fig. 1h caption says so: "Data
reported as change in colony forming units (CFUs) relative to time 0"). The
denominator is nowhere in the file. So the absolute counts cannot be recovered,
cfu_per_ml is BLANK on those rows, and the fraction is carried in notes as
fraction_survival=... rather than being written into a count column it is not.
Only 'Ext. Fig. 4e' reports CFU/mL outright, and that is a growth experiment
under a respiratory inhibitor, not a kill curve: 24 readings, against 924
fractions.

That absence propagates. With no starting density there is no headroom, and
with no absolute count a detection floor could not be applied to these data even
if the paper had stated one, which it does not: no plated volume, no dilution,
no colony count, no limit of detection appears anywhere in the workbook.
floor_cfu_per_ml is blank throughout and every row says why.

REPLICATES. Each arm is four (sometimes three) unlabelled adjacent columns. The
deposit gives no replicate identifiers, only column position, so replicates are
named rep1..repN by position and that is stated on every row.

ORGANISM. Recorded as E. coli, on the deposit's own word: the Fig. 1a caption
reads "E. coli MG1655 cells", Fig. 3c "wildtype MG1655, dAtpA, and dCyoA dCydB
dAppB (dETC) E. coli cells", and Fig. 6a "wildtype MG1655 cells expressing
pEmpty, pF1, or pNOX".

SHEETS DELIBERATELY NOT READ, AND WHY
  'Ext. Fig. 1a', 'Ext. Fig. 1b'   MISLABELLED IN THE DEPOSIT. Both print the
      words "Fraction survival" over their data, but their captions read
      "Oxygen consumption rates (OCR)" and "Extracellular acidification rates
      (ECAR)", their x-axis is "Time (minutes)", and their values run 117-412 --
      not survival fractions. The stray label is a copy from the neighbouring
      lethality sheets. Reading them as survival would have put respirometry in
      the corpus as killing data.
  'Ext. Fig. 4f'                   the same fault the other way round: labelled
      "CFU/mL", captioned "OCR for exponential phase MG1655 cells", x-axis in
      minutes, values 66-201. Not counts.
  'Ext. Fig. 1d'                   the 4 h fraction survivals of Fig. 1h with no
      time column: a duplicate of rows already read.
  the "4 hour fraction survival" sub-blocks at the foot of 'Ext. Fig. 1f',
      'Ext. Fig. 1g' and 'Ext. Fig. 1h' -- likewise the t = 4 rows repeated.
  sixteen whole series that this workbook prints on two or three sheets each --
      see _dedupe() below. The deposit admits the habit in two captions ("These
      data are replicated from Figure 1"), and does it silently elsewhere: the
      pF1 and pNOX curves of 'Fig. 1h' reappear as the "MOPS rich" arm of
      'Fig. 5e' and the "WT" arm of 'Ext. Fig. 2e'; the MG1655 curve of
      'Fig. 4a' reappears on 'Fig. 5a' and 'Ext. Fig. 1e'; the dAtpA curve of
      'Fig. 5a' reappears on 'Fig. 5d'. Kept once each, on the first sheet that
      prints them, with the other sheets named in the notes -- 140 readings that
      would otherwise have been counted twice or three times.
  'Fig. 1f', 'Ext. Fig. 4d'        OD600 against a CONCENTRATION axis
      (ciprofloxacin, piceatannol), not against time. Dose-response, not kill.
      ('Fig. 1c' and 'Ext. Fig. 7a' ARE read: they are OD600 against time in
      hours, the quantity named by the deposit, with no drug -- growth-control
      rows, which the schema takes with drug blank.)
  'Fig. 1a', 'Fig. 1b', 'Ext. Fig. 7c', 'Ext. Fig. 7d'   metabolite pools
  'Fig. 1d', 'Fig. 1e', 'Fig. 3c', 'Ext. Fig. 4a', 'Ext. Fig. 7b'  OCR / ECAR
  'Fig. 1g', 'Fig. 3g'-'Fig. 3j', 'Fig. 6a'-'Fig. 6e', 'Ext. Fig. 1c',
      'Ext. Fig. 4c', 'Ext. Fig. 4g', 'Ext. Fig. 4h', 'Ext. Fig. 8a'-'8e'
      resistance evolution: fold-change in MIC50 over serial passages, and areas
      under those curves. A passage index is not a kill-curve time axis and the
      quantity is an MIC, not a count.
  'Fig. 2a'-'Fig. 2c'              genome-scale model predictions
  'Fig. 2d'-'Fig. 2f', 'Fig. 3d'-'Fig. 3f', 'Ext. Fig. 4b'  H2O2, carbonylated
      protein, 8-oxo-dG assays
  'Fig. 3a', 'Fig. 3b'             Luria-Delbruck mutation rates
  'Fig. 5b'                        energetic ratios
  'Fig. 6f', 'Ext. Fig. 2b'-'2d', 'Ext. Fig. 3'   normalised expression
  'Ext. Fig. 6a'-'6f'              biosensor fluorescence and flow cytometry
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

XLSX = "41467_2025_60302_MOESM13_ESM.xlsx"

FLOOR_BASIS = ("not stated, and not applicable to a normalised readout: the "
               "workbook gives no plated volume, dilution, colony count or limit "
               "of detection, and the survival sheets report a ratio whose "
               "denominator is not in the deposit, so no floor could be applied "
               "to them even if one had been published")

ORGANISM_NOTE = ("organism from the deposit's own captions -- Fig. 1a 'E. coli "
                 "MG1655 cells', Fig. 3c '... (dETC) E. coli cells', Fig. 6a "
                 "'wildtype MG1655 cells expressing pEmpty, pF1, or pNOX'")

TIME_HDR = re.compile(r"^time\s*\(hours\)", re.I)
CONC_IN_LABEL = re.compile(r"\(([\d.]+)\s*(ng/mL|ug/mL|µg/mL|uM|µM|mg/L)\)", re.I)

# What each sheet's own caption says the exposure was. Nothing here comes from
# outside the workbook; the caption is also copied into notes row by row.
#   strain: "group" -> the column-group label is the strain
#           "block" -> the strain is the sub-block label ("Data: pF1")
#           anything else -> that literal strain
CFG: dict[str, dict] = {
    "Fig. 1h": dict(drug="ciprofloxacin", conc=18.0, unit="ng/mL", strain="group"),
    "Fig. 4a": dict(drug="ciprofloxacin", conc=16.0, unit="ng/mL", strain="group"),
    "Fig. 4b": dict(drug="ciprofloxacin", conc=18.0, unit="ng/mL", strain="group",
                    extra="co-treated with 12.5 uM piceatannol (PA)"),
    "Fig. 4c": dict(drug="ciprofloxacin", conc=18.0, unit="ng/mL", strain="group",
                    extra="co-treated with 15 U/mL catalase (CAT)"),
    "Fig. 4d": dict(drug="ciprofloxacin", conc=18.0, unit="ng/mL", strain="group"),
    "Fig. 4e": dict(drug="ciprofloxacin", conc=18.0, unit="ng/mL", strain="group"),
    "Fig. 5a": dict(drug="ciprofloxacin", conc=16.0, unit="ng/mL", strain="group",
                    extra="MOPS rich media"),
    "Fig. 5d": dict(drug="ciprofloxacin", conc=16.0, unit="ng/mL",
                    strain="∆atpA",
                    extra="the column groups are media conditions, not strains"),
    "Fig. 5e": dict(drug="ciprofloxacin", conc=18.0, unit="ng/mL", strain="block",
                    extra="the column groups are media conditions, not strains"),
    "Ext. Fig. 1e": dict(drug="ciprofloxacin", conc=None, unit="ng/mL",
                         strain="group",
                         extra="the concentration is named in each column-group "
                               "label and is taken from there"),
    "Ext. Fig. 1f": dict(drug="ciprofloxacin", conc=128.0, unit="ng/mL",
                         strain="group"),
    "Ext. Fig. 1g": dict(drug="gentamicin", conc=200.0, unit="ng/mL",
                         strain="group"),
    "Ext. Fig. 1h": dict(drug="ampicillin", conc=100.0, unit="ug/mL",
                         strain="group"),
    "Ext. Fig. 2e": dict(drug="ciprofloxacin", conc=18.0, unit="ng/mL",
                         strain="group",
                         extra="the sub-block label gives the plasmid the strain "
                               "carries"),
}

# The one sheet with absolute counts. Its groups are the treatments.
# Two sheets are plain optical density against time in hours, with the quantity
# named by the deposit itself ("OD600" printed over the data) and NO drug in
# them -- growth controls, which the schema takes with drug left blank. They are
# returned as OD600 readings; an optical density is never turned into a count.
OD_SHEETS = {
    "Fig. 1c": "Growth curves for pEmpty, pF1, and pNOX cells grown in MOPS "
               "rich media",
    "Ext. Fig. 7a": "Growth curves for MG1655 and dAtpA cells grown in MOPS "
                    "rich media",
}

CFU_SHEET = "Ext. Fig. 4e"
CFU_ARMS = {
    "+ 1% DMSO": ("", np.nan, ""),
    "+ 100 μM PA": ("piceatannol", 100.0, "uM"),
}


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def _txt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    s = str(v).replace("\xa0", " ").strip()
    return "" if s.lower() in {"nan", "nat"} else s


def _headers(df: pd.DataFrame) -> list[int]:
    return [i for i in range(df.shape[0]) if TIME_HDR.match(_txt(df.iat[i, 0]))]


def _groups(df: pd.DataFrame, hrow: int) -> list[tuple[str, int, int]]:
    starts = [c for c in range(1, df.shape[1]) if _txt(df.iat[hrow, c])]
    out = []
    for k, c in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else df.shape[1]
        out.append((_txt(df.iat[hrow, c]), c, end))
    return out


def read(d: Path) -> pd.DataFrame:
    path = d / XLSX
    xl = pd.ExcelFile(path)
    rows: list[dict] = []

    for sheet in xl.sheet_names:
        if sheet not in CFG and sheet != CFU_SHEET and sheet not in OD_SHEETS:
            continue
        df = pd.read_excel(path, sheet_name=sheet, header=None)
        caption = _txt(df.iat[1, 0])
        cfg = CFG.get(sheet, {})

        for hrow in _headers(df):
            block = _txt(df.iat[hrow - 2, 0]) if hrow >= 2 else ""
            block = block[len("Data:"):].strip() if block.lower().startswith("data:") \
                else ("" if block.lower() == "data" else block)
            quantity = _txt(df.iat[hrow - 1, 1]) if hrow >= 1 else ""

            times = []
            for i in range(hrow + 1, df.shape[0]):
                t = _num(df.iat[i, 0])
                if np.isnan(t):
                    break
                times.append((i, t))
            if not times:
                continue

            for label, c0, c1 in _groups(df, hrow):
                cols = [c for c in range(c0, c1)
                        if any(not np.isnan(_num(df.iat[i, c])) for i, _ in times)]
                for k, c in enumerate(cols):
                    for i, t in times:
                        v = _num(df.iat[i, c])
                        if np.isnan(v):
                            continue
                        row = {
                            "source_file": XLSX, "sheet": sheet,
                            "organism": "E. coli",
                            "arm": " | ".join(x for x in [block, label,
                                                          cfg.get("extra", "")] if x),
                            "replicate": "rep" + str(k + 1),
                            "time_h": t,
                            "floor_basis": FLOOR_BASIS,
                        }
                        if sheet in OD_SHEETS:
                            row.update({
                                "strain": label, "drug": "",
                                "concentration": np.nan, "conc_unit": "",
                                "readout": "OD600",
                                "floor_basis": "not applicable: an optical "
                                               "density, not a count",
                                "notes": ("od600=" + format(v, ".6g")
                                          + ". The schema has no column for a "
                                            "non-count reading, so the value is "
                                            "kept here and cfu_per_ml is left "
                                            "blank -- an optical density is "
                                            "never converted to a count. The "
                                            "quantity is the deposit's own: "
                                            "'" + quantity + "' is printed over "
                                            "these columns and the axis is '"
                                            "Time (hours)'. No drug is present "
                                            "in this experiment, so drug is "
                                            "blank. Replicates are named by "
                                            "column position, the deposit gives "
                                            "no identifiers. Sheet caption: '"
                                          + caption + "'. " + ORGANISM_NOTE),
                            })
                        elif sheet == CFU_SHEET:
                            drug, conc, unit = CFU_ARMS.get(label, ("", np.nan, ""))
                            row.update({
                                "strain": "MG1655", "drug": drug,
                                "concentration": conc, "conc_unit": unit,
                                "cfu_per_ml": v, "readout": "CFU",
                                "notes": ("the only sheet in this workbook that "
                                          "reports absolute counts; its own "
                                          "column label is 'CFU/mL'. Replicates "
                                          "are named by column position, the "
                                          "deposit gives no identifiers. Sheet "
                                          "caption: '" + caption + "'. "
                                          + ORGANISM_NOTE),
                            })
                        else:
                            conc = cfg.get("conc")
                            m = CONC_IN_LABEL.search(label)
                            if m:
                                conc = float(m.group(1))
                            strain_mode = cfg.get("strain", "group")
                            strain = (label if strain_mode == "group"
                                      else block if strain_mode == "block"
                                      else strain_mode)
                            if m:   # "MG1655 (16 ng/mL)" -> strain "MG1655"
                                strain = CONC_IN_LABEL.sub("", strain).strip()
                            row.update({
                                "strain": strain,
                                "drug": cfg.get("drug", ""),
                                "concentration": np.nan if conc is None else conc,
                                "conc_unit": cfg.get("unit", ""),
                                "readout": "fraction survival (CFU relative to "
                                           "time 0)",
                                "notes": ("fraction_survival=" + format(v, ".6g")
                                          + ". cfu_per_ml is BLANK because this "
                                            "deposit reports only the ratio: the "
                                            "quantity printed over the data is '"
                                          + quantity + "' and the time-0 counts "
                                            "it was divided by are not in the "
                                            "file, so no absolute count and no "
                                            "starting density can be recovered. "
                                            "Replicates are named by column "
                                            "position, the deposit gives no "
                                            "identifiers. Sheet caption: '"
                                          + caption + "'. " + ORGANISM_NOTE),
                            })
                        row["_series"] = "␟".join(
                            [sheet, block, label, str(k)])
                        row["_value"] = v
                        rows.append(row)

    if not rows:
        return empty()
    return finish(_dedupe(pd.DataFrame(rows)), "BIOENERGETIC2025")


def _dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """Drop series this workbook prints on more than one sheet.

    This deposit replots the same cultures in several panels and says so in two
    places itself -- 'Fig. 6a' is captioned "These data are replicated from
    Figure 1 to facilitate comparisons" and 'Ext. Fig. 8a' "replicated from
    Extended Data Figure 1c". The same habit runs through the lethality sheets
    without a caption to warn of it: sixteen four-point series appear on two or
    three sheets each, identical value for identical value --

      pF1 and pNOX under 18 ng/mL ciprofloxacin: 'Fig. 1h', again as the
        "MOPS rich" arm of 'Fig. 5e', and again as the "WT" arm of 'Ext. Fig. 2e'
      MG1655 under 16 ng/mL: 'Fig. 4a', again as "MOPS rich" on 'Fig. 5a',
        and again as "MG1655 (16 ng/mL)" on 'Ext. Fig. 1e'
      dAtpA under 16 ng/mL: 'Fig. 5a', again as "MOPS rich" on 'Fig. 5d'

    A series is kept once, on the first sheet the workbook prints it on, and
    every sheet and arm it also appears under is named in the notes of the rows
    that are kept. Without this the corpus would count 140 of these 1,004
    readings twice or three times, and no downstream reader could tell which.
    """
    df = df.copy()
    values: dict[str, list] = {}
    for series, g in df.groupby("_series", sort=False):
        values[series] = tuple(zip(g["time_h"], g["_value"]))
    order = {s: i for i, s in enumerate(df["_series"].drop_duplicates())}
    alias: dict[tuple, list[str]] = {}
    for series, v in values.items():
        alias.setdefault(v, []).append(series)
    drop: set[str] = set()
    extra: dict[str, str] = {}
    for v, members in alias.items():
        if len(members) == 1:
            continue
        members.sort(key=lambda s: order[s])
        drop |= set(members[1:])
        extra[members[0]] = (
            "; the identical series is also printed on this workbook's "
            + ", ".join("'" + m.split("␟")[0] + "' ("
                        + " / ".join(x for x in m.split("␟")[1:3] if x)
                        + ")" for m in members[1:])
            + " -- the same cultures replotted, returned ONCE here so they are "
              "not counted twice")
    df["notes"] = df["notes"] + df["_series"].map(lambda s: extra.get(s, ""))
    df = df[~df["_series"].isin(drop)]
    return df.drop(columns=["_series", "_value"])
