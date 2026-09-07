"""Kollerova 2024 -- eleven CSVs on Escherichia coli MG1655 under recurrent
and constant ampicillin exposure, with a README.txt that documents every file.
Two of the eleven hold readings; the other nine do not, and this reader says so
rather than inventing a way to use them.

WHAT IS READ.

  R_long_data_Alex_and_Sara_CFU_counts.csv -- 384 colony counts, and the best
  documented file in this whole batch. The README defines every column, and
  the file supplies what almost no deposit does: N_of_colonies, the
  Dilution_factor each count was made at, and Vol_plated_mL. So

      * colonies, dilution and plated_volume_ul all go in as given
        (Vol_plated_mL is 0.005 throughout, i.e. 5 uL);
      * cfu_per_ml is the deposit's own CFU_mL column, which this reader
        checked equals colonies * dilution / volume exactly on all 383 rows
        where colonies is recorded;
      * A FLOOR IS RECOVERABLE. Not stated -- the deposit never uses the words
        detection limit -- but fixed, because one colony on a plate at that
        row's own dilution and volume is the smallest non-zero density the
        reported plating scheme can produce: 1 * Dilution_factor / 0.005 mL.
        floor_basis says precisely that on every row, so anyone counting
        "deposits that state a floor" can exclude these if they mean stated
        rather than fixed. It is worth seeing what the arithmetic gives: the
        t=0 samples plated at a 10,000-fold dilution have a floor of 2e6
        CFU/mL, which is above where several of the later readings sit.
      * 22 rows report zero colonies. They come through as cfu_per_ml = 0,
        no log10, and censored = yes against the row's own floor.
      * One row (Time 0, Conc 2, replicate 7) has CFU_mL = 0 but blank
        N_of_colonies and blank Dilution_factor. Its floor cannot be computed,
        so that row alone carries a blank floor and censored = unknown.

  Kopie_von_Uli_ampi-killing-curve.csv -- 73 timepoints x 72 wells of OD600 at
  constant ampicillin, every 20 minutes for 24 h. Returned as readout OD600.
  The OD is NOT converted to anything: an optical density is not a count, and
  no floor of any kind is asserted for these rows. The plate map comes from the
  README, which states it explicitly -- well A1..H9, the digit gives the
  concentration (1=128, 2=64, 3=32, 4=16, 5=8, 6=4, 7=2, 8=0 ug/mL, 9 =
  negative control with no bacteria added) and the letter gives the replicate.
  Column 9 wells are medium blanks, so their organism is left blank.

WHAT IS NOT READ, AND WHY.

  COMPLETE_DATA_1_2_EXP_06.csv   2,598 single cells x 1,056 columns of cell
                                 size, growth rate and division events from a
                                 mother-machine microfluidic device, at 4 min
                                 steps. Per-cell microscopy, not a population
                                 density; there is no reading here that
                                 belongs in a CFU corpus.
  Oikos_longdata-div.csv         per-cell division events, same device. Also
                                 contains an AB1157 subset the README says was
                                 excluded from the analysis.
  Oikos_MG1655-deathrates.csv    a life table (dx, lx, qx, sx, moving average)
                                 computed from the single-cell data.
  CON2/4/16/24/32/64/128         seven files of time versus death rate at one
    deathrate_07.csv             ampicillin concentration each -- two columns,
                                 "Time" and "death rate". Death rate is a
                                 fitted quantity derived from the survival
                                 data, not a measurement of density, so
                                 nothing is returned from them. (CON24 is in
                                 the directory and documented in the README,
                                 but is absent from the file list in
                                 PROVENANCE.json.)
  README.txt, PROVENANCE.json    documentation.

TIME. The CFU file gives TimeMin, "the time during the experiment the sampling
was done" -- 60, 150, 330, 420, 1080 and 1170 minutes -- converted to hours
here. Its Time column is the sampling number, not a clock, and is kept in
notes. Ampicillin in that experiment was applied recurrently, so hours are
hours since the start of the experiment and not since a single exposure. The
OD file gives an elapsed HH:MM:SS clock from 00:00:00 to 24:00:00.

UNITS. The README writes ampicillin concentrations as "?g/ml" -- the micro sign
is mojibake in the depositor's own file -- read here as ug/mL.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty

CFU_FILE = "R_long_data_Alex_and_Sara_CFU_counts.csv"
OD_FILE = "Kopie_von_Uli_ampi-killing-curve.csv"

ORGANISM = "Escherichia coli"
STRAIN = "MG1655"
ORG_NOTE = "organism and strain from README.txt, which names E. coli MG1655"
UG = "ug/mL"
UNIT_NOTE = ("README writes concentrations as '?g/ml' -- the micro sign is "
             "mojibake in the depositor's file -- read as ug/mL")

# README: "Column labels containing a 1 were exposed to concentrations of
# 128 ?g/ml Ampicillin ... a 8 ... 0 ?g/ml ... a 9 were Negative Control, i.e.,
# no bacteria added to medium."
OD_PLATE = {1: 128.0, 2: 64.0, 3: 32.0, 4: 16.0, 5: 8.0, 6: 4.0, 7: 2.0,
            8: 0.0}


def _note(*bits: str) -> str:
    return "; ".join(b for b in bits if b)


def _hours(clock: str) -> float:
    """'HH:MM:SS' elapsed -- 24:00:00 is a real value here, so no time-of-day
    parser can be used."""
    parts = str(clock).strip().split(":")
    if len(parts) != 3:
        return np.nan
    try:
        h, m, s = (float(p) for p in parts)
    except ValueError:
        return np.nan
    return h + m / 60.0 + s / 3600.0


def _read_cfu(d: Path) -> list[dict]:
    p = d / CFU_FILE
    if not p.exists():
        return []
    df = pd.read_csv(p, sep=";", decimal=",")

    rows = []
    for _, r in df.iterrows():
        colonies = r["N_of_colonies"]
        dil = r["Dilution_factor"]
        vol_ml = r["Vol_plated_mL"]
        conc = float(r["Conc"])

        have_plating = not (pd.isna(dil) or pd.isna(vol_ml)) and vol_ml > 0
        floor = float(dil) / float(vol_ml) if have_plating else np.nan
        if have_plating:
            basis = (f"one colony at this row's own stated dilution "
                     f"({dil:g}) and plated volume ({vol_ml:g} mL) = "
                     f"{floor:g} CFU/mL. The deposit reports dilution and "
                     "plated volume per sample but never names a limit of "
                     "detection: this is the smallest non-zero density its "
                     "reported plating scheme can produce, not a figure the "
                     "depositor states")
        else:
            basis = ("dilution factor is blank for this row, so no floor can "
                     "be computed even though every other row supplies one")

        note = [
            ORG_NOTE, UNIT_NOTE,
            f"README: sampling number Time={r['Time']:g}, TimeMin="
            f"{r['TimeMin']:g} min converted to hours",
            "ampicillin applied recurrently, so the clock runs from the start "
            "of the experiment, not from a single exposure",
            f"96-well plate column {r['Column']:g} (concentration), row "
            f"{r['Replicates_Row']:g} (replicate)",
        ]
        if not pd.isna(colonies) and colonies == 0:
            note.append("zero colonies counted")
        if pd.isna(colonies):
            note.append("N_of_colonies and Dilution_factor are blank in the "
                        "deposit although CFU_mL is given as 0")

        rows.append({
            "source_file": CFU_FILE, "sheet": "",
            "organism": ORGANISM, "strain": STRAIN,
            "drug": "" if conc == 0 else "Ampicillin",
            "concentration": np.nan if conc == 0 else conc,
            "conc_unit": "" if conc == 0 else UG,
            "arm": ("no antibiotic (0 ug/mL)" if conc == 0
                    else f"ampicillin {conc:g} ug/mL, recurrent exposure"),
            "replicate": f"row{int(r['Replicates_Row'])}",
            "tech_replicate": "",
            "time_h": float(r["TimeMin"]) / 60.0,
            "colonies": float(colonies) if not pd.isna(colonies) else np.nan,
            "dilution": float(dil) if not pd.isna(dil) else np.nan,
            "plated_volume_ul": (float(vol_ml) * 1000.0
                                 if not pd.isna(vol_ml) else np.nan),
            "cfu_per_ml": float(r["CFU_mL"]) if not pd.isna(r["CFU_mL"])
            else np.nan,
            "floor_cfu_per_ml": floor,
            "floor_basis": basis,
            "readout": "CFU",
            "notes": _note(*note),
        })
    return rows


def _read_od(d: Path) -> list[dict]:
    p = d / OD_FILE
    if not p.exists():
        return []
    df = pd.read_csv(p, encoding="utf-8-sig")
    wells = [c for c in df.columns if c not in ("Time", "Temp")]

    rows = []
    for _, r in df.iterrows():
        t = _hours(r["Time"])
        for w in wells:
            letter, digit = w[0], int(w[1:])
            blank = digit not in OD_PLATE          # README: digit 9, no cells
            conc = OD_PLATE.get(digit, np.nan)
            rows.append({
                "source_file": OD_FILE, "sheet": "",
                "organism": "" if blank else ORGANISM,
                "strain": "" if blank else STRAIN,
                "drug": "" if blank or conc == 0 else "Ampicillin",
                "concentration": np.nan if blank or conc == 0 else conc,
                "conc_unit": "" if blank or conc == 0 else UG,
                "arm": ("negative control, no bacteria added to medium"
                        if blank else
                        "no antibiotic (0 ug/mL), constant exposure"
                        if conc == 0 else
                        f"ampicillin {conc:g} ug/mL, constant exposure"),
                "replicate": f"well{w}",
                "tech_replicate": "",
                "time_h": t,
                "cfu_per_ml": np.nan,
                "floor_cfu_per_ml": np.nan,
                "floor_basis": ("optical density, not a colony count -- no CFU "
                                "floor applies, and the deposit states no OD "
                                "blank threshold either"),
                "readout": "OD600",
                "notes": _note(
                    f"OD600 = {r[w]}",
                    "the schema has no numeric column for a non-count "
                    "readout, so the value is carried here; it is NOT "
                    "converted to a cell density and no count column is used",
                    "" if blank else ORG_NOTE,
                    "README: constant antibiotic levels, read every 20 min "
                    "for 24 h; elapsed clock HH:MM:SS converted to hours",
                    f"well {w}: README maps the digit to the concentration "
                    f"and the letter {letter} to the replicate",
                    "README: no bacteria added to this well" if blank else "",
                    "" if blank else UNIT_NOTE,
                    "the deposit does not say whether the negative-control "
                    "wells received antibiotic" if blank else ""),
            })
    return rows


def read(d: Path) -> pd.DataFrame:
    rows = _read_cfu(d) + _read_od(d)
    if not rows:
        return empty()
    return pd.DataFrame(rows)
