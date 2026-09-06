"""Extract Kaur 2024 apramycin figshare deposit into the common tidy schema.

Layout was inspected cell-by-cell before writing this.
Rules honoured: no invented numbers; no guessed limit of quantification;
per-replicate values only, never the depositors' Avg column.
"""
import re
import numpy as np
import pandas as pd

SRC = r"E:/Research/Modeling of Antibiotic Resistance/data/raw/apramycin_mtb/Raw Data.xlsx"
OUT = r"E:/Research/Modeling of Antibiotic Resistance/data/processed/tidy_kaur.csv"

DATASET = "kaur2024_apramycin"
ORGANISM = "M. tuberculosis"
REPCOLS = {1: 4, 2: 5, 3: 6}          # Replicate-1/2/3 -> column index
NO_LOQ = ("no limit of quantification stated anywhere in the deposit; "
          "limit_log10 left NaN, not guessed")

rows = []


def rounded_flag(v):
    """Flag cells that are hand-typed 2-dp entries rather than computed log10."""
    if abs(v - round(v, 2)) < 1e-12:
        return "; cell is a 2-dp rounded entry, not a computed log10"
    return ""


def add(state, drug, dose_value, dose_unit, dose_xmic, unit_group,
        n0, time_days, y, note):
    rows.append(dict(
        dataset=DATASET, organism=ORGANISM, state=state, state_numeric=np.nan,
        drug=drug, dose_value=dose_value, dose_unit=dose_unit, dose_xmic=dose_xmic,
        unit_group=unit_group, n0_log10=n0, time_days=time_days, y_log10=y,
        censored=False, limit_log10=np.nan, notes=note))


# ---------------------------------------------------------------- time-course
def parse_timecourse(sheet, state, tag, day0_row, first_data_row, base_note):
    df = pd.read_excel(SRC, sheet_name=sheet, header=None)

    assert "Day 0 cell control" in str(df.iat[day0_row, 2])
    day0 = {r: float(df.iat[day0_row, c]) for r, c in REPCOLS.items()}

    # the day-0 untreated baseline is a real measurement: emit it as t=0 of the
    # untreated control series
    for r, v in day0.items():
        add(state, "none", np.nan, "", np.nan,
            tag + "_none_untreated_r" + str(r), v, 0.0, v,
            base_note + "; untreated cell control at t=0; this single day-0 row "
            "is the only baseline in the sheet and is shared by every arm"
            + rounded_flag(v))

    day = np.nan
    drug = None
    for i in range(first_data_row, df.shape[0]):
        lab_day, lab_drug, lab_conc = df.iat[i, 1], df.iat[i, 2], df.iat[i, 3]
        if pd.notna(lab_day):
            m = re.search(r"Day\s*(\d+)", str(lab_day))
            if m:
                day = float(m.group(1))
        dose_unit, dose_value = "ug/mL", np.nan
        if pd.notna(lab_drug):
            s = str(lab_drug).strip()
            if s.lower().startswith("rif"):
                drug = "rifampicin"
                m = re.search(r"@\s*([\d.]+)", s)   # dose lives inside the label
                dose_value = float(m.group(1))
            elif s.lower().startswith("cell control"):
                drug = "none"
            else:
                drug = s.lower()
        if drug is None or all(pd.isna(df.iat[i, c]) for c in REPCOLS.values()):
            continue
        if drug == "none":
            dose_value, dose_unit = np.nan, ""
            arm = "untreated"
        else:
            if pd.isna(dose_value):
                dose_value = float(lab_conc) if pd.notna(lab_conc) else np.nan
            if pd.isna(dose_value):
                raise ValueError(sheet + " row " + str(i) + ": no concentration")
            arm = "{:g}ugmL".format(dose_value)

        for r, c in REPCOLS.items():
            v = df.iat[i, c]
            if pd.isna(v):
                continue
            v = float(v)
            note = base_note + rounded_flag(v)
            if drug == "none":
                note += "; untreated cell control"
            add(state, drug, dose_value, dose_unit, np.nan,
                tag + "_" + drug + "_" + arm + "_r" + str(r),
                day0[r], day, v, note)


KK_NOTE = ("planktonic time-kill, days 0/3/7/14; dose in ug/mL as reported, MIC not "
           "given in the workbook so dose_xmic is NaN; n0_log10 is the replicate-index-"
           "matched Day 0 cell control, the single untreated baseline the sheet provides "
           "(replicate correspondence between that row and the treated arms is assumed by "
           "column index, it is not stated by the deposit); " + NO_LOQ)

IC_NOTE = ("intracellular (macrophage) killing, days 0/3/7; dose in ug/mL as reported, MIC "
           "not given so dose_xmic is NaN; n0_log10 is the replicate-index-matched Day 0 "
           "cell control (correspondence assumed by column index, not stated); apramycin and "
           "amikacin were tested over different concentration ladders, so this sheet is not a "
           "dose-matched drug comparison; " + NO_LOQ)

parse_timecourse("Kill kinetics", "planktonic", "kaur_kk", 3, 5, KK_NOTE)
parse_timecourse("Intracellular efficacy", "intracellular", "kaur_ic", 3, 5, IC_NOTE)


# ------------------------------------------------------------------- biofilm
def parse_biofilm(sheet, tag, header_row, early_row, base_note):
    df = pd.read_excel(SRC, sheet_name=sheet, header=None)
    assert str(df.iat[header_row, 1]).strip() == "SN"
    assert str(df.iat[header_row, 3]).strip().startswith("Conc")
    assert str(df.iat[early_row, 2]).strip() == "Early"
    early = {r: float(df.iat[early_row, c]) for r, c in REPCOLS.items()}

    drug = None
    for i in range(header_row + 1, df.shape[0]):
        lab_drug, lab_conc = df.iat[i, 2], df.iat[i, 3]
        if pd.notna(lab_drug):
            drug = str(lab_drug).strip()
        if all(pd.isna(df.iat[i, c]) for c in REPCOLS.values()):
            continue
        if drug in ("Early", "Late"):
            dose_value = dose_xmic = np.nan
            dose_unit = ""
            arm = "control_" + drug.lower()
            dname = "none"
            extra = "; untreated " + drug.lower() + " control"
            if drug == "Early":
                extra += ("; this is the pre-treatment baseline the depositors' "
                          "log10-drop column is anchored on (verified arithmetically)")
            else:
                extra += "; untreated end-of-experiment control"
        else:
            m = re.fullmatch(r"(\d+(?:\.\d+)?)X", str(lab_conc).strip(), flags=re.I)
            if not m:
                raise ValueError(sheet + " row " + str(i) + ": unparsable conc "
                                 + repr(lab_conc))
            dose_value = dose_xmic = float(m.group(1))
            dose_unit = "xMIC"
            arm = "{:g}xMIC".format(dose_value)
            dname = drug.lower()
            extra = ("; dose reported as a multiple of MIC; the MIC in ug/mL is not in "
                     "the workbook, so this dose cannot be converted to ug/mL")
        for r, c in REPCOLS.items():
            v = df.iat[i, c]
            if pd.isna(v):
                continue
            v = float(v)
            add("biofilm", dname, dose_value, dose_unit, dose_xmic,
                tag + "_" + dname + "_" + arm + "_r" + str(r),
                early[r], np.nan, v, base_note + extra + rounded_flag(v))


BIO_NOTE = ("biofilm, single-endpoint assay: the workbook gives NO sampling time, so "
            "time_days is NaN rather than guessed; n0_log10 is the replicate-index-matched "
            "untreated Early control (correspondence assumed by column index, not stated); "
            + NO_LOQ)

parse_biofilm("Biofilm 1", "kaur_bio1", 2, 27,
              "experiment 'Biofilm 1'; " + BIO_NOTE)
parse_biofilm("Biofilm 2", "kaur_bio2", 4, 29,
              "experiment 'Biofilm 2', a separate biofilm run from 'Biofilm 1' "
              "(different Early control); " + BIO_NOTE)

# The 'In-vivo' sheet is deliberately NOT written here: it is CFU per lung per
# animal, not CFU/mL, with no time axis and no per-mL denominator. Putting it in
# a column documented as log10 CFU/mL would be a unit error.

cols = ["dataset", "organism", "state", "state_numeric", "drug", "dose_value",
        "dose_unit", "dose_xmic", "unit_group", "n0_log10", "time_days",
        "y_log10", "censored", "limit_log10", "notes"]
out = pd.DataFrame(rows)[cols]
out.to_csv(OUT, index=False, encoding="utf-8")
print("wrote", OUT, out.shape)
