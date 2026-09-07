"""BUCHHOLZ2026 -- Nature Communications Source Data, 26 sheets, one per figure panel.

10.1038/s41467-026-71178-5, file 41467_2026_71178_MOESM18_ESM.xlsx.

The workbook carries an "Overview" sheet that defines every column of every data
sheet in prose, so almost nothing here had to be guessed. The time-kill sheets
are tidy long format with one row per culture-timepoint and a cfu_ml (or cfu)
column that the Overview defines as "CFU/mL". Time is in hours ("timepoint
during main treatment in h") except Fig.5E, where the Overview says "Timepoint
in minutes after main treatment addition", and the Fig.3 optical-density block,
where it says "time in minutes after pre-treatment"; both are converted to hours
here.

These are hysteresis experiments: a pre-treatment antibiotic (ab1/conc1) is
followed by a main treatment (ab2/conc2), and the clock runs from the start of
the main treatment. `drug` is therefore the MAIN treatment; the pre-treatment is
carried in `arm` and `notes`. Some sheets add a third agent before the
pre-treatment (ab0: chloramphenicol, heat shock, CCCP, DMSO, ethanol); that also
goes in `arm`.

WHAT IS NOT READ, AND WHY
  Overview            prose legend, no data
  Fig.2B, Fig.4E      CombiANT fractional inhibitory concentrations, no time axis
  Fig.4F              transcriptome table
  Fig.5B, Fig.S10     Laurdan generalised polarisation
  Fig.S4              area-under-curve summaries of the Fig.3 screen, no time axis
  Fig.S9              relative growth rate on a CAR x GEN concentration grid
  Fig.S2A             VERIFIED DUPLICATE. The Overview says "same raw data as
                      Fig.1G; subset with pause = 0", and all 48 of its readings
                      match Fig.1G rows on (Rundate, Pause, Treatment, biorep,
                      Timepoint). Read from Fig.1G only, to avoid double-counting.
  Fig.4B              VERIFIED DUPLICATE. The Overview's own line for this sheet
                      reads "Subset of the time-kill data for Fig. 4 C panel 1",
                      and every one of its 48 rows is present verbatim in
                      Fig.4C_and_Fig.S8A panel 1 -- matched on all twelve shared
                      fields (time_h, ab1, conc1, xMIC1, ab2, conc2, xMIC2,
                      strain, biol.rep, cfu, survival, run), 48 of 48. Read from
                      Fig.4C_and_Fig.S8A only. Fig.4B carries 47 usable CFU
                      readings, none of them new.
  Fig.S5              DUPLICATE in kind: a 6 h CFU/OD correlation table whose
                      rows are labelled with the figure they came from (S1B and
                      so on), i.e. the same tubes already read from those sheets.
                      Its OD600 values are the only new content and they attach
                      to no timepoint other than 6 h.
  the AUC and summary blocks that sit to the right of the time-kill blocks on
                      Fig.1G, Fig.2A, Fig.4C, Fig.4D, Fig.5A, Fig.5C, Fig.5D and
                      Fig.S7 -- these are derived, not readings.

THE FLOOR. Nothing in this workbook states a plated volume, a dilution, a colony
count or a limit of detection. The Overview documents every column of every
sheet and no column is any of those. Fig.1B-D contains one cfu_ml value of
exactly 0 whose censoring therefore cannot be decided. floor_cfu_per_ml is blank
throughout, deliberately.

THE ORGANISM. The workbook names strains (PA14, cpxS / CpxS T163P, and numeric
Schulenburg-lab library IDs such as 1260, 787, 1268_I) but states a species in
exactly one place: the Overview line for Fig.3 and Fig.S4, "Negative hysteresis
screen across the species P. aeruginosa". organism is filled only for the Fig.3
rows that line describes, and left blank everywhere else.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

XLSX = "41467_2026_71178_MOESM18_ESM.xlsx"

FLOOR_BASIS = ("not stated: the workbook reports CFU/mL only -- no colony count, "
               "dilution, plated volume or limit of detection anywhere, including "
               "in the Overview sheet that documents every column")

# The Overview defines conc1/conc2 in mg/L for every time-kill sheet.
MGL = "mg/L"


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return np.nan
    return f


def _txt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    s = str(v).strip()
    return "" if s.lower() in {"nan", "nat"} else s


def _block(d: Path, sheet: str, header: int, c0: int, c1: int) -> pd.DataFrame:
    """One left-to-right block of a sheet, header on row `header` (0-based)."""
    df = pd.read_excel(d / XLSX, sheet_name=sheet, header=header)
    df = df.iloc[:, c0:c1].dropna(how="all")
    return df.reset_index(drop=True)


def _g(x) -> str:
    v = _num(x)
    return "" if np.isnan(v) else format(v, "g")


def _pre(ab1, conc1) -> str:
    a, c = _txt(ab1), _num(conc1)
    if not a or c == 0:
        return "no pre-treatment"
    return f"pre {a} {_g(conc1)} {MGL}" if not np.isnan(c) else f"pre {a}"


def _main(ab2, conc2) -> str:
    a, c = _txt(ab2), _num(conc2)
    if not a or c == 0:
        return "no main treatment"
    return f"main {a} {_g(conc2)} {MGL}" if not np.isnan(c) else f"main {a}"


def _hysteresis(df, sheet, cfu_col, time_col="time_h", strain_col="strain",
                rep_col="biol_rep", extra=None, time_scale=1.0):
    """The column set shared by the CAR->GEN style time-kill sheets."""
    rows = []
    for _, r in df.iterrows():
        t = _num(r[time_col]) * time_scale
        if np.isnan(t):
            continue
        conc2 = _num(r.get("conc2"))
        ab2 = _txt(r.get("ab2"))
        arm_extra, note_extra = extra(r) if extra else ("", "")
        drug = ab2 if (ab2 and conc2 != 0) else ""
        note = "pre-treatment: " + _pre(r.get("ab1"), r.get("conc1"))
        if not drug and ab2:
            note += ("; the source names ab2=" + ab2 + " with conc2=0, "
                     "i.e. no main treatment given")
        n = _num(r.get("n"))
        if not np.isnan(n):
            note += ("; the source's n=" + _g(n) + " is the number of technical "
                     "replicates behind this CFU/mL value, not their identities")
        if note_extra:
            note += "; " + note_extra
        rows.append({
            "source_file": XLSX, "sheet": sheet,
            "strain": _txt(r.get(strain_col)),
            "drug": drug,
            "concentration": conc2 if drug else np.nan,
            "conc_unit": MGL if drug else "",
            "arm": " | ".join(x for x in [_pre(r.get("ab1"), r.get("conc1")),
                                          _main(ab2, conc2), arm_extra] if x),
            "replicate": _txt(r.get(rep_col)),
            "time_h": t,
            "cfu_per_ml": _num(r[cfu_col]),
            "floor_basis": FLOOR_BASIS,
            "readout": "CFU",
            "notes": note,
        })
    return rows


def read(d: Path) -> pd.DataFrame:
    rows: list[dict] = []

    # ---- Fig.1B-D: CAR-GEN, GEN-GEN and GEN-CAR, varying pre-treatment conc.
    df = _block(d, "Fig.1B-D", 0, 0, 14)
    new = _hysteresis(
        df, "Fig.1B-D", "cfu_ml",
        extra=lambda r: ("set " + _txt(r["set"]) + " / id " + _txt(r["id"]),
                         "experiment date " + _txt(r["date"])
                         + ", tube " + _txt(r["tube"])))
    # the date is the only thing separating replicate 1 of one run from another
    for row, (_, r) in zip(new, df.iterrows()):
        row["replicate"] = _txt(r["date"]) + "/rep" + _txt(r["biol_rep"])
    rows += new

    # ---- Fig.1E: chloramphenicol added before the pre-treatment
    df = _block(d, "Fig.1E", 0, 0, 14)
    rows += _hysteresis(
        df, "Fig.1E", "cfu_ml",
        extra=lambda r: (_txt(r["treatment"]),
                         "ab0 " + _txt(r["ab0"]) + " at " + _g(r["conc0"])
                         + " mg/L (the Overview gives conc0 in mg/L); tube "
                         + _txt(r["tube"])))

    # ---- Fig.1F: varying pre-treatment DURATION
    df = _block(d, "Fig.1F", 0, 0, 12)
    rows += _hysteresis(
        df, "Fig.1F", "cfu_ml",
        extra=lambda r: ("pre-treatment for " + _g(r["t1_min"]) + " min",
                         "tube " + _txt(r["tube"])))

    # ---- Fig.1G: varying PAUSE between pre- and main treatment (cols A-H)
    df = _block(d, "Fig.1G", 1, 0, 8)
    for _, r in df.iterrows():
        t = _num(r["Timepoint"])
        if np.isnan(t):
            continue
        rows.append({
            "source_file": XLSX, "sheet": "Fig.1G",
            "arm": _txt(r["Treatment"]) + " | pause " + _g(r["Pause"]) + " min",
            "replicate": _txt(r["Rundate"]) + "/" + _txt(r["biorep"]),
            "time_h": t, "cfu_per_ml": _num(r["CFU_ml"]),
            "floor_basis": FLOOR_BASIS, "readout": "CFU",
            "notes": ("CAR->GEN hysteresis with a pause between pre- and main "
                      "treatment. The Overview labels the treatments only as "
                      "Hys / main / preonly / ndc and this sheet carries no drug "
                      "or concentration column, so drug and concentration are "
                      "left blank; the experiment line reads 'CAR-GEN time kill "
                      "with varying pauses between pre- & main treatment'"),
        })

    # ---- Fig.2A: clinical antibiotic panel at IC75 (cols A-J)
    df = _block(d, "Fig.2A", 1, 0, 10)
    for _, r in df.iterrows():
        t = _num(r["time"])
        if np.isnan(t):
            continue
        pre, main = _txt(r["pre"]), _txt(r["main"])
        rows.append({
            "source_file": XLSX, "sheet": "Fig.2A",
            "drug": "" if main == "ndc" else main,
            "arm": "pre " + pre + " -> main " + main + " (" + _txt(r["type"]) + ")",
            "replicate": "run" + _txt(r["runid"]),
            "tech_replicate": _txt(r["spot"]),
            "time_h": t, "cfu_per_ml": _num(r["cfu"]),
            "floor_basis": FLOOR_BASIS, "readout": "CFU",
            "notes": ("the Overview calls this column 'cfu -- Colony forming "
                      "units' with no unit; the values run 8.6e4 to 3.0e9, which "
                      "is a per-mL scale and not colonies on the spot named by "
                      "the 'spot' column, so they are recorded as CFU/mL. "
                      "Concentrations are not in the deposit: the Overview says "
                      "only that IC75 concentrations were used. 'ndc' is the "
                      "source's no-drug control. Observation, recorded but NOT "
                      "acted on: every value on this sheet is an integer "
                      "multiple of 1e6/7, which is the arithmetic of a 7 uL spot "
                      "at a 1000-fold dilution -- but the deposit states no "
                      "volume and no dilution, so neither is recorded. Run date "
                      + _txt(r["rundate"])[:10]),
        })

    # ---- Fig.3: exemplary optical-density curves of the hysteresis screen (I-X)
    df = _block(d, "Fig.3", 1, 8, 24)
    df.columns = ["panel", "strain", "preA", "preB", "main", "well", "row",
                  "column", "treat", "pre_drug", "pre_lvl", "pre_conc",
                  "main_lvl", "main_conc", "time", "od"]
    for _, r in df.iterrows():
        t = _num(r["time"])
        if np.isnan(t):
            continue
        main_conc = _num(r["main_conc"])
        main = _txt(r["main"])
        treated = bool(main) and main_conc not in (0.0,) and not np.isnan(main_conc)
        rows.append({
            "source_file": XLSX, "sheet": "Fig.3",
            "organism": "P. aeruginosa",
            "strain": _txt(r["strain"]),
            "drug": main if treated else "",
            "concentration": main_conc if treated else np.nan,
            "conc_unit": "ug/mL" if treated else "",
            "arm": ("pre " + _txt(r["pre_drug"]) + " " + _g(r["pre_conc"])
                    + " ug/mL -> main " + main + " " + _g(r["main_conc"])
                    + " ug/mL [" + _txt(r["treat"]) + "]"),
            "replicate": _txt(r["panel"]) + "/well " + _txt(r["well"]),
            "time_h": t / 60.0,
            "floor_basis": "not applicable: an optical-density sheet, not a count",
            "readout": "OD600",
            "notes": ("od600=" + format(_num(r["od"]), ".6g") + ". The schema has "
                      "no column for a non-count reading, so the value is kept "
                      "here and cfu_per_ml is left blank -- an OD is never "
                      "converted to a count. The Overview defines od as 'Optical "
                      "Density at 600nm', time as 'time in minutes after "
                      "pre-treatment' (converted to hours here) and "
                      "pre_conc/main_conc in ug/ml. Organism from the Overview "
                      "line for this sheet: 'Negative hysteresis screen across "
                      "the species P. aeruginosa'"),
        })

    # ---- Fig.4B is NOT read: the Overview calls it "Subset of the time-kill
    # data for Fig. 4 C panel 1", and all 48 of its rows were checked against
    # Fig.4C_and_Fig.S8A panel 1 and matched on every shared field. Reading it
    # would count 47 cultures twice.

    # ---- Fig.4C / Fig.4D: Cpx mutants and CpxS over-expression (cols A-N)
    for sheet in ("Fig.4C_and_Fig.S8A", "Fig.4D_and_Fig.S8B"):
        df = _block(d, sheet, 1, 0, 14)
        new = _hysteresis(
            df, sheet, "cfu", rep_col="biol.rep",
            extra=lambda r: ("xMIC1 " + _g(r["xMIC1"]) + " / xMIC2 "
                             + _g(r["xMIC2"]),
                             "panel " + _txt(r["panel"]) + ", run "
                             + _txt(r["run"]) + ", tube " + _txt(r["tube"])
                             + "; strain IDs are Schulenburg-lab library "
                             "numbers, '_I' meaning IPTG was added (Overview)"))
        for row, (_, r) in zip(new, df.iterrows()):
            row["replicate"] = _txt(r["run"]) + "/rep" + _txt(r["biol.rep"])
        rows += new

    # ---- Fig.5A: membrane stressors as the pre-treatment (cols A-G)
    df = _block(d, "Fig.5A", 1, 0, 7)
    for _, r in df.iterrows():
        t = _num(r["t"])
        if np.isnan(t):
            continue
        gen = _num(r["ab2"]) == 1
        rows.append({
            "source_file": XLSX, "sheet": "Fig.5A",
            "strain": _txt(r["strain"]),
            "drug": "Gentamicin" if gen else "",
            "arm": ("pre " + _txt(r["ab1"]) + " | main "
                    + ("Gentamicin" if gen else "none")),
            "replicate": _txt(r["biol.rep"]),
            "time_h": t, "cfu_per_ml": _num(r["cfu"]),
            "floor_basis": FLOOR_BASIS, "readout": "CFU",
            "notes": ("the Overview defines ab1 as the pre-treatment stressor and "
                      "ab2 as '1 = Gentamicin present, 0 = no main treatment'; "
                      "this sheet carries no concentration column, so "
                      "concentration is blank"),
        })

    # ---- Fig.5C / Fig.5D: heat shock and CCCP before the pre-treatment (A-O)
    for sheet, unit in (("Fig.5C", "degC (heat shock)"), ("Fig.5D", "uM")):
        df = _block(d, sheet, 1, 0, 15)
        rows += _hysteresis(
            df, sheet, "cfu_ml",
            extra=lambda r, u=unit: (
                _txt(r["treatment"]),
                "ab0 " + _txt(r["ab0"]) + " at " + _g(r["conc0"]) + " " + u
                + " (unit from the Overview); tube " + _txt(r["tube"])))

    # ---- Fig.5E: gentamicin uptake, with CFU/mL alongside the uptake assay
    df = _block(d, "Fig.5E", 0, 0, 14)
    for _, r in df.iterrows():
        t = _num(r["timepoint"])
        if np.isnan(t):
            continue
        rows.append({
            "source_file": XLSX, "sheet": "Fig.5E",
            "strain": _txt(r["Strain"]),
            "drug": "GEN",
            "arm": _txt(r["Treatment"]) + " (pre-treatment: " + _txt(r["treat"]) + ")",
            "replicate": _txt(r["Replicate"]),
            "time_h": t / 60.0, "cfu_per_ml": _num(r["CFU_ml"]),
            "floor_basis": FLOOR_BASIS, "readout": "CFU",
            "notes": ("gentamicin-uptake experiment; the Overview defines "
                      "timepoint as 'Timepoint in minutes after main treatment "
                      "addition' (converted to hours), Treatment as 'GEN = no "
                      "hysteresis control, HYS = hysteresis treatment CAR - GEN' "
                      "and treat as 'control = no pre treatment, CAR = "
                      "carbenicillin pre-treatment'. No concentration is given "
                      "on this sheet"),
        })

    # ---- Fig.S1: beta-lactam / gentamicin hysteresis panel
    df = _block(d, "Fig.S1", 0, 0, 12)
    rows += _hysteresis(
        df, "Fig.S1", "cfu_ml",
        extra=lambda r: ("panel " + _txt(r["panel"]), "tube " + _txt(r["tube"])))

    # ---- Fig.S2B: PBS wash between pre- and main treatment
    df = _block(d, "Fig.S2B", 0, 0, 13)
    rows += _hysteresis(
        df, "Fig.S2B", "cfu_ml",
        extra=lambda r: (_g(r["wash"]) + "x PBS wash", "tube " + _txt(r["tube"])))

    # ---- Fig.S7: mixtures of PA14 and CpxS T163P (cols A-M)
    df = _block(d, "Fig.S7", 1, 0, 13)
    rows += _hysteresis(
        df, "Fig.S7", "cfu_ml", strain_col="strain1",
        extra=lambda r: (
            _g(r["strain1_percent"]) + "% " + _txt(r["strain1"]) + " / "
            + _g(100 - _num(r["strain1_percent"])) + "% " + _txt(r["strain2"]),
            "co-culture of " + _txt(r["strain1"]) + " and " + _txt(r["strain2"])
            + "; the strain column here holds strain1 only, the mixture is "
            "given in arm"))

    if not rows:
        return empty()
    out = pd.DataFrame(rows)
    # 33 CFU cells are empty in the deposit, on the sheets this reader takes:
    # 23 on Fig.2A, 4 on Fig.1G, 4 on Fig.5A, 2 on Fig.4C_and_Fig.S8A. A blank
    # cell is not a reading, so those rows are dropped rather than carried as a
    # count of nothing -- and never as a zero, which would invent a measurement.
    blank = (out.readout == "CFU") & out.cfu_per_ml.isna()
    out = out[~blank]
    return finish(out, "BUCHHOLZ2026")
