"""STEPANYAN2015 -- Dryad/Zenodo deposit, seven files, of which two carry
time-resolved viable counts.  The other five are read and rejected, with the
reason for each below.

READ.

'Fig S2 killing curve.xlsx', Sheet1 -- the only file in the deposit that is a
kill curve in the ordinary sense: columns TIME, REPLICATE, LOG10CFU, three
replicates at 1, 2, 3, 4, 5, 12 and 24.  Nothing else is on the sheet: no
strain, no drug, no unit for TIME, and no volume basis for LOG10CFU.  Time is
read as hours and the count as CFU/mL, and both of those readings are flagged
on every row, because neither is written down.  There is no t=0.

'Fig 4 raw data.txt' -- 327 rows, tab separated: time, strain, perslevel,
its two confidence limits, replicate, popsz, type.  The structure is a paired
design: `type` = Normal rows sit at 0, 24, 48, 72 and 96 and `type` =
Persister rows at 5, 29, 53, 77 and 101, i.e. five hours later, so each
Persister row is the surviving population of the Normal row above it after a
five-hour exposure.  Both are ingested as readings with `arm` set to the
file's own word.  `popsz` is recorded as cfu_per_ml -- the file gives no unit,
and this too is flagged on every row.  `perslevel` is NOT ingested: it is a
single constant per strain, repeated down every time point and replicate, so
it is a summary of the experiment and not a reading in it.  The drug is never
named in this file, so `drug` is blank on every row, including the Persister
rows that plainly had one.

NOT READ, and why:

  'Fig S1 raw data.txt' (120 rows) gives Nrcells and Percent per Time,
    Replicate, Treated and Type.  Its treated cultures hold ~7-9.7e9 Nrcells
    at every time point, while Fig 4's five-hour survivors for the same
    strains are ~1e4 -- so Nrcells cannot be a viable count, and the deposit
    supplies no legend saying what it is.  Ingesting it as a density would be
    a guess of exactly the kind this corpus exists to avoid.
  'Fig 1 raw data.txt' is the same shape without even Nrcells: a Percent
    whose denominator is nowhere stated.
  'Fig 2 raw data.xlsx' is a per-strain table of mean persistence levels and
    MICs, with no time axis.  Worth knowing rather than using: its last column
    is headed "MICofloxacin (ug/ml)", which is the only place any drug is
    named in the whole deposit.  Neither the kill curve nor 'Fig 4 raw data'
    says what drug IT used, so `drug` stays blank on all 348 rows; carrying
    ofloxacin across from a different file's MIC table would be exactly the
    guess this corpus exists to avoid.  Its first sheet also gives each
    strain's geographical origin and clinical/environmental type, and cites
    Pirnay et al. 2002 -- but it never writes a species, so `organism` stays
    blank too.
  'Fig 3 and S5 Gompertz growth curve fits.csv' and the matching summary are
    fitted parameters -- lag, R0, Log10Nmax, AIC -- not observations.

BOTH INGESTED FILES CARRY `unit_inferred=cfu_per_ml` AT THE FRONT OF EVERY
ROW'S NOTES.  Neither writes a volume basis -- one column is headed only
"LOG10CFU" and the other only "popsz" -- so all 348 rows can be found and
dropped with one grep by anyone who would rather not carry the inference.

NO FLOOR ANYWHERE.  Not one of the seven files states a plated volume, a
dilution or a limit of detection.  Fig 4's popsz descends to 1.07, below any
plausible single-colony resolution, which is worth knowing precisely because
the deposit gives nothing to interpret it against.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingest import empty

UNPACKED = "_unpacked"
KILL = "Fig S2 killing curve.xlsx"
FIG4 = "Fig 4 raw data.txt"


def _find(d: Path, name: str) -> Path | None:
    hits = sorted(d.rglob(name))
    return hits[0] if hits else None


def read(d: Path) -> pd.DataFrame:
    rows = []

    kill = _find(d, KILL)
    if kill is not None:
        g = pd.read_excel(kill, "Sheet1", header=0)
        g.columns = [str(c).strip().upper() for c in g.columns]
        for _, r in g.iterrows():
            if pd.isna(r.get("LOG10CFU")) or pd.isna(r.get("TIME")):
                continue
            rows.append({
                "source_file": kill.name, "sheet": "Sheet1",
                "organism": "", "strain": "", "drug": "", "arm": "",
                "replicate": str(int(r["REPLICATE"])),
                "time_h": float(r["TIME"]),
                "cfu_per_ml": 10.0 ** float(r["LOG10CFU"]),
                "readout": "CFU",
                "notes": ("unit_inferred=cfu_per_ml; "
                          "sheet holds only TIME / REPLICATE / LOG10CFU: the "
                          "time unit is not written down (values 1,2,3,4,5,"
                          "12,24, read as hours) and LOG10CFU carries no "
                          "volume basis (read as per mL); the sheet names "
                          "neither strain nor drug, so both are blank; no "
                          "t=0 reading exists"),
            })

    f4 = _find(d, FIG4)
    if f4 is not None:
        g = pd.read_csv(f4, sep="\t")
        for _, r in g.iterrows():
            if pd.isna(r["popsz"]):
                continue
            kind = str(r["type"]).strip()
            rows.append({
                "source_file": f4.name, "sheet": "",
                "organism": "", "strain": str(r["strain"]).strip(),
                "drug": "", "arm": kind,
                "replicate": str(int(r["replicate"])),
                "time_h": float(r["time"]),
                "cfu_per_ml": float(r["popsz"]),
                "readout": "CFU",
                "notes": ("unit_inferred=cfu_per_ml; "
                          "column 'popsz' recorded as CFU/mL: the file states "
                          "no unit for it and no volume basis; the time "
                          "column is likewise unlabelled (0,5,24,29,48,53,72,"
                          "77,96,101 -- read as hours), with Persister rows "
                          "sitting exactly five hours after the Normal row "
                          "of the same strain and replicate -- this is NOT a "
                          "kill curve read down one axis: `time` is age of "
                          "the culture and the Persister row is that same "
                          "culture after a five-hour exposure, so the two "
                          "arms must be kept apart; the drug is "
                          "never named in this file; the column 'perslevel' "
                          "is a per-strain constant, not a per-reading "
                          "quantity, and is deliberately not ingested"),
            })

    if not rows:
        return empty()
    return pd.DataFrame(rows)
