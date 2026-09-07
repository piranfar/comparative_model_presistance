"""MOLECULAR2026 -- Nature Communications source data, 17 sheets.

10.1038/s41467-026-74323-2, file 41467_2026_74323_MOESM4_ESM.xlsx.

Amoxicillin / clavulanate kill curves. Three sheets carry counts against time:
"Figure 1", "Figure 4" and the top block of "Figure 7". Each is laid out as a
stack of small blocks, one per treatment arm, with a free-text arm label above
each block, a Time column in hours, and TWO count columns which the deposit
heads "Drug Free ... CFU/mL" and "Drug ... CFU/mL". What those two columns
distinguish is not defined anywhere in the file, so this reader does not
interpret them: it keeps the deposit's own words in `arm` and returns both as
separate series.

THE HEADERS SAY log10 AND THE VALUES ARE NOT. Every one of those headers reads
"log10 CFU/mL" (variously "Drug Free Log10 CFU//mL", "Drug free log10 cfu/mL",
"Drug Free log10(CFU/mL)") while the values beneath them are 1, 250, 1110000,
91000000000. 9.1e10 is not a log10. The values are therefore recorded as
cfu_per_ml, and finish() takes the log itself.

THE FLOOR. Not stated. What the file does show is the tell: values bottom out at
a repeated constant, in both count columns and across unrelated arms and
timepoints -- 1 on Figures 1 and 4 (29 and 40 readings of exactly 1), 10 on
Figure 7 (29 readings of exactly 10). That is the signature of a plotting
placeholder standing in for "nothing grew", but the deposit never says so and
never gives a plated volume, a dilution or a limit of detection. floor_cfu_per_ml
is left blank and those readings are returned at face value; deciding they are
censored is exactly the inference this corpus exists to avoid making silently.

CONCENTRATIONS. The arm labels mix doses in mg ("AMX 500 mg/CLV 125 mg", a
regimen) with concentrations in mg/L ("AMX 40 mg/L / CLV 125 mg q8h"). A dose in
mg is not a concentration, and a two-drug label has two concentrations where the
schema has one field. `concentration` is therefore filled only where a block
label gives a single unambiguous mg/L value; everywhere else it is blank and the
label survives verbatim in `arm`.

WHAT IS NOT READ, AND WHY
  Figure 2                 A: 6 unlabelled paired values per timepoint on a
                           1.6-3.4 scale, quantity not stated. B: qPCR Ct values.
                           E: mutant frequency against drug concentration, no
                           time axis. None is a count against time.
  Figure 3A, 3B            RNA-seq log2 fold changes and a gene/pathway table
  Figure 5                 qPCR Ct values for 16S and TEM-1
  Figure 7 panels B-E      checkerboard absorbance grids, an IS-element count
                           table -- no time axis
  Supplementary S1, S4, S7 amoxicillin and clavulanate CONCENTRATIONS against
                           time (pharmacokinetics), not bacterial counts
  Supplementary S3         pathway summary counts
  Supplementary S5         3 replicate traces per arm rising from 0 to about 1
                           over hours. Almost certainly growth, but the sheet
                           states no quantity, no unit and no wavelength, so
                           there is no honest readout to record. NOT READ, and
                           flagged here rather than guessed at.
  Supplementary S6         pharmacokinetic parameters (half life, Vd, Cl)
  Supplementary Figure 8   checkerboard absorbance grids with an annotated MIC
  Gel Images, Flow Cytometry  captions only, no data

An orphan value (10) sits in the drug column of the Figure 7 "CLV alone-Urine
PK" block with no time beside it; it is skipped.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

XLSX = "41467_2026_74323_MOESM4_ESM.xlsx"

FLOOR_BASIS = ("not stated: no plated volume, dilution, colony count or limit of "
               "detection anywhere in the deposit; the drug-plate columns bottom "
               "out at a repeated constant (1 in Figures 1 and 4, 10 in Figure 7) "
               "which looks like a placeholder but is never declared as one")

# Verbatim block label -> (drug, concentration, unit, extra note).
# Nothing here is supplied from outside the label itself.
ARMS: dict[str, tuple[str, float, str, str]] = {
    # Figure 1
    "Untreated E. coli B50": ("", np.nan, "", ""),
    "Untreated E. coli K35": ("", np.nan, "", ""),
    "Untreated E. coli K67": ("", np.nan, "", ""),
    "B50 AMX 500 mg/CLV 125 mg": ("AMX + CLV", np.nan, "", "dose regimen in mg"),
    "B50 AMX 1000 mg/CLV 125 mg": ("AMX + CLV", np.nan, "", "dose regimen in mg"),
    "K35 AMX 500 mg/CLV 125 mg": ("AMX + CLV", np.nan, "", "dose regimen in mg"),
    "K35 AMX 1000 mg/CLV 125 mg": ("AMX + CLV", np.nan, "", "dose regimen in mg"),
    "K67 AMX 500 mg/CLV 125 mg": ("AMX + CLV", np.nan, "", "dose regimen in mg"),
    "K67 AMX 1000 mg/CLV 125 mg": ("AMX + CLV", np.nan, "", "dose regimen in mg"),
    # Figure 4
    "Untreated": ("", np.nan, "", ""),
    "500 mg AMX": ("AMX", np.nan, "",
                   "the label gives a 500 mg dose, not a concentration"),
    "40 mg/L q8h infusion": ("", 40.0, "mg/L",
                             "the label gives a concentration but names no drug, "
                             "so drug is left blank"),
    "80mg/L q8h infusion": ("", 80.0, "mg/L",
                            "the label gives a concentration but names no drug, "
                            "so drug is left blank"),
    "160mg/L q8h infusion": ("", 160.0, "mg/L",
                             "the label gives a concentration but names no drug, "
                             "so drug is left blank"),
    "AMX 500 mg/1m/L CLV": ("AMX + CLV", np.nan, "",
                            "two agents, one dose in mg and one concentration "
                            "('1m/L', as printed), so concentration is blank"),
    "AMX 500 mg/2.5 m/L CLV": ("AMX + CLV", np.nan, "",
                               "two agents, one dose in mg and one concentration, "
                               "so concentration is blank"),
    "AMX 500 mg/5 m/L CLV": ("AMX + CLV", np.nan, "",
                             "two agents, one dose in mg and one concentration, "
                             "so concentration is blank"),
    "AMX 40 mg/L / CLV 125 mg q8h": ("AMX + CLV", np.nan, "",
                                     "two agents with two different units, so "
                                     "concentration is blank"),
    "AMX 80 mg/L / CLV 125 mg q8h": ("AMX + CLV", np.nan, "",
                                     "two agents with two different units, so "
                                     "concentration is blank"),
    "AMX 160 mg/L / CLV 125 mg q8h": ("AMX + CLV", np.nan, "",
                                      "two agents with two different units, so "
                                      "concentration is blank"),
    # Figure 7
    "AMX alone-Urine PK": ("AMX", np.nan, "", "urine pharmacokinetic profile arm"),
    "CLV alone-Urine PK": ("CLV", np.nan, "", "urine pharmacokinetic profile arm"),
    "AMX CLV-Urine PK": ("AMX + CLV", np.nan, "",
                         "urine pharmacokinetic profile arm"),
}


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def _txt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    s = str(v).replace(" ", " ").strip()
    return "" if s.lower() in {"nan", "nat"} else s


def _arm_fields(label: str) -> tuple[str, float, str, str]:
    if label in ARMS:
        return ARMS[label]
    return ("", np.nan, "",
            "block label not recognised by the reader; drug and concentration "
            "left blank rather than parsed out of free text")


def _emit(rows, sheet, label, t, drug_free, drug_col, organism, strain,
          col_names):
    drug, conc, unit, note = _arm_fields(label)
    for value, which in ((drug_free, col_names[0]), (drug_col, col_names[1])):
        v = _num(value)
        if np.isnan(v):
            continue
        rows.append({
            "source_file": XLSX, "sheet": sheet,
            "organism": organism, "strain": strain,
            "drug": drug, "concentration": conc, "conc_unit": unit,
            "arm": label + " | " + which,
            "time_h": t,
            "cfu_per_ml": v,
            "floor_basis": FLOOR_BASIS,
            "readout": "CFU",
            "notes": ("count column headed '" + which + "'; what separates the "
                      "deposit's two count columns is not defined anywhere in "
                      "the file, so it is left as the deposit words it. The "
                      "header says log10 but the values are plain counts (up to "
                      "9.1e10), so they are read as CFU/mL. Time in hours as "
                      "given" + ("; " + note if note else "")),
        })


def read(d: Path) -> pd.DataFrame:
    path = d / XLSX
    rows: list[dict] = []

    # ------------------------------------------------------------------ Fig 1
    # Block label sits alone in column D; Time in A, the two count columns in
    # B and E. Organism: the untreated blocks of this sheet read "Untreated
    # E. coli B50/K35/K67", which is where both organism and strain come from;
    # the treated blocks of the same sheet then use the bare strain code.
    df = pd.read_excel(path, sheet_name="Figure 1", header=None)
    label, strain = "", ""
    for _, r in df.iterrows():
        lab = _txt(r[3])
        if lab and not _txt(r[0]):
            label = lab
            for s in ("B50", "K35", "K67"):
                if s in label:
                    strain = s
            continue
        t = _num(r[0])
        if np.isnan(t) or not label:
            continue
        _emit(rows, "Figure 1", label, t, r[1], r[4], "E. coli", strain,
              ("Drug Free Log10 CFU//mL", "Drug log10 CFU/mL"))

    # ------------------------------------------------------------------ Fig 4
    # Block label alone in column A; header row "time | Drug free | Drug".
    # No organism or strain is named anywhere on this sheet, so both stay blank.
    df = pd.read_excel(path, sheet_name="Figure 4", header=None)
    label = ""
    for _, r in df.iterrows():
        a = _txt(r[0])
        if a and np.isnan(_num(a)) and not _txt(r[1]) and not _txt(r[2]):
            label = a
            continue
        t = _num(r[0])
        if np.isnan(t) or not label:
            continue
        _emit(rows, "Figure 4", label, t, r[1], r[2], "", "",
              ("Drug free log10 cfu/mL", "Drug log10 cfu/mL"))

    # ------------------------------------------------------------------ Fig 7A
    # Only the top of the sheet is a time course; panel B onwards is a
    # checkerboard. Block label sits in column B, data in A/B/C.
    df = pd.read_excel(path, sheet_name="Figure 7", header=None)
    label = ""
    for i, r in df.iterrows():
        if i > 45:
            break
        lab = _txt(r[1])
        if lab and not _txt(r[0]) and np.isnan(_num(lab)):
            label = lab
            continue
        t = _num(r[0])
        if np.isnan(t) or not label:
            continue
        _emit(rows, "Figure 7", label, t, r[1], r[2], "", "",
              ("Drug Free log10(CFU/mL) [first count column]",
               "Drug Free log10(CFU/mL) [second count column]"))

    # ------------------------------------------ Supplementary figure S2
    # Four small grids, "Day 1" to "Day 4". Rows are labelled "Drug Free",
    # "8 mg/L", "16 mg/L" ... and columns "No treatment" / "Thiourea Treated".
    # Two things here are NOT resolvable from the deposit and are left blank:
    #   - what "Day N" is in hours. It could be the day of a passage series or
    #     an elapsed time; nothing says. time_h stays blank and the day is kept
    #     in arm.
    #   - whether "8 mg/L" is the concentration the culture saw or the
    #     concentration in the agar the sample was plated on. concentration
    #     stays blank and the label is kept verbatim.
    df = pd.read_excel(path, sheet_name="Supplementary figure S2", header=None)
    grids = [(2, 0), (2, 6), (9, 0), (9, 6)]
    for r0, c0 in grids:
        day = _txt(df.iat[r0, c0]) or _txt(df.iat[r0, c0 + 1])
        heads = [_txt(df.iat[r0 + 1, c0 + 1]), _txt(df.iat[r0 + 1, c0 + 2])]
        for i in range(r0 + 2, min(r0 + 7, df.shape[0])):
            row_label = _txt(df.iat[i, c0])
            if not row_label:
                continue
            for j, head in enumerate(heads):
                v = _num(df.iat[i, c0 + 1 + j])
                if np.isnan(v):
                    continue
                rows.append({
                    "source_file": XLSX, "sheet": "Supplementary figure S2",
                    "arm": day + " | " + row_label + " | " + head,
                    "cfu_per_ml": v,
                    "floor_basis": FLOOR_BASIS,
                    "readout": "CFU",
                    "notes": ("thiourea experiment. time_h is BLANK on purpose: "
                              "the deposit labels these blocks only 'Day 1' to "
                              "'Day 4' and never says what that is in hours, or "
                              "whether the days are successive timepoints or "
                              "separate passages. concentration is blank for the "
                              "same reason: '" + row_label + "' is not tied to "
                              "the culture or to the plate by anything in the "
                              "file. Both labels are kept verbatim in arm"),
                })

    if not rows:
        return empty()
    return finish(pd.DataFrame(rows), "MOLECULAR2026")
