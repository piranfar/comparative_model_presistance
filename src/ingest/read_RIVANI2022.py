"""RIVANI2022 -- Dryad/Zenodo deposit: colony counts and turbidity for four
Acinetobacter baumannii resistotypes under two meropenem-based combinations.

Three files.  README_TurbidityandColonyCountdata.txt is the only source of
metadata in the deposit and everything asserted here comes from it verbatim:
the organism, the four resistotype labels, the two drug pairs, the four
concentration steps, and -- decisively -- that "Turbidity data and colony count
were the means of six replications".  Both data files are semicolon-delimited
with a comma decimal mark and a wide layout: Isolate, Hour, then one column per
treatment arm.

THE ONE PLACE THE README IS READ RATHER THAN QUOTED.  It names the two
combinations as "meropenem and ampicillin-sulbactam" and "meropenem and
amikacin"; the column headers are "MEM+SAM" and "MEM+AK".  The deposit never
writes MEM = meropenem, but it offers exactly two combinations and exactly two
prefixes, so the pairing is fixed within the deposit.  The raw header is kept
in `arm` either way, so nothing is lost if that reading is ever disputed.

WHAT IS NOT HERE.  No plated volume, no dilution, no limit of detection: the
floor is blank.  No concentration can be put in the numeric column either,
because every arm is a PAIR of drugs at a pair of multiples ("0,5+0,5 MIC"),
which is not one number; the whole label is kept in `arm` instead.

A WARNING CARRIED ON EVERY COUNT ROW.  The value 5.78 log CFU/mL is the entry
at t=0 for all 36 arms and recurs unchanged at later times, and the growth
control is exactly 6.78 at every time from 1 h to 24 h.  The deposit nowhere
says whether those repeats are measurements or values carried forward, so they
are ingested as deposited and flagged, not filtered.

THE TWIN DEPOSIT.  RIVANI2022_2 is the figshare copy of this same experiment.
This deposit is the corpus's copy of record -- it has the README and the
growth-control counts -- and the figshare reader suppresses everything the two
share, so the 476 shared readings are counted once.  See
src/ingest/_rivani_dup.py.  The one cell where the two disagree is found at
run time by comparing the files and is flagged in `notes` on the row it
affects; the value printed in THIS deposit is what is kept.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingest import empty
from src.ingest._rivani_dup import FIGSHARE, annotate_discrepancies

# Expansions the README itself gives; the raw header is kept in `arm`.
DRUGS = {
    "MEM+SAM": "meropenem + ampicillin-sulbactam",
    "MEM+AK": "meropenem + amikacin",
}
ORGANISM = "Acinetobacter baumannii"  # README, first line of paragraph 2

INOCULUM_CONSTANT = 5.78
CONTROL_CONSTANT = 6.78


def _grid(path: Path) -> pd.DataFrame:
    """Read one of the two semicolon/comma-decimal wide files."""
    df = pd.read_csv(path, sep=";", dtype=str)
    df["Isolate"] = df["Isolate"].ffill().str.strip()
    return df


def _drug_for(header: str) -> str:
    for key, name in DRUGS.items():
        if header.startswith(key):
            return name
    return ""  # growth control


def _parse(d: Path) -> pd.DataFrame:
    rows = []

    counts = d / "Colony_Count_Data.csv"
    turb = d / "Turbidity_Data.csv"

    if counts.exists():
        g = _grid(counts)
        arms = [c for c in g.columns if c not in ("Isolate", "Hour")]
        for _, r in g.iterrows():
            for a in arms:
                raw = (r[a] or "").strip()
                if not raw:
                    continue
                val = float(raw.replace(",", "."))
                note = ("value is log CFU/mL as deposited and is the mean of "
                        "six replications (README); ")
                if val == INOCULUM_CONSTANT:
                    note += ("equals 5.78, the value entered at t=0 for every "
                             "arm -- the deposit does not say whether repeats "
                             "of it are measurements or carried forward; ")
                if val == CONTROL_CONSTANT and a == "Growth Control":
                    note += ("equals 6.78, the growth control's value at every "
                             "time from 1 h on; ")
                rows.append({
                    "source_file": counts.name, "sheet": "",
                    "organism": ORGANISM, "strain": r["Isolate"],
                    "drug": _drug_for(a), "arm": a,
                    "replicate": "", "time_h": float(r["Hour"]),
                    "cfu_per_ml": 10.0 ** val, "readout": "CFU",
                    "notes": note + "source time unit: hours (column 'Hour')",
                })

    if turb.exists():
        g = _grid(turb)
        arms = [c for c in g.columns if c not in ("Isolate", "Hour")]
        for _, r in g.iterrows():
            for a in arms:
                raw = (r[a] or "").strip()
                if not raw:
                    continue
                rows.append({
                    "source_file": turb.name, "sheet": "",
                    "organism": ORGANISM, "strain": r["Isolate"],
                    "drug": _drug_for(a), "arm": a,
                    "replicate": "", "time_h": float(r["Hour"]),
                    "readout": "McFarland turbidity",
                    "notes": ("value_as_deposited=" + raw.replace(",", ".") +
                              " McFarland units (README); mean of six "
                              "replications; NOT a count, so deliberately "
                              "left out of cfu_per_ml (the schema has no "
                              "column for a non-count value); source time "
                              "unit: hours"),
                })

    if not rows:
        return empty()
    return pd.DataFrame(rows)


def read(d: Path) -> pd.DataFrame:
    mine = _parse(d)
    twin = d.parent / FIGSHARE
    if len(mine) and twin.is_dir():
        from src.ingest.read_RIVANI2022_2 import _parse as twin_parse
        theirs = twin_parse(twin)
        if len(theirs):
            mine = annotate_discrepancies(mine, theirs, FIGSHARE)
    return mine
