"""RIVANI2022_2 -- the figshare "REV" copy of the Dryad colony-count deposit,
and ALMOST ENTIRELY A DUPLICATE OF IT.

The two deposits are one experiment.  This directory's own PROVENANCE.json
records that "a CC0 twin sits on Dryad at 10.5061/dryad.rxwdbrvc3", which is
the record RIVANI2022 was downloaded from, and a cell-by-cell comparison made
at run time confirms it: 224 of 224 colony-count readings and 252 of 252
turbidity readings here share a key with the Dryad deposit's, and 475 of those
476 are numerically identical.  So this reader emits ONLY what its twin does
not contain -- the 36 turbidity readings at 48 h, a column the Dryad file
stops short of -- and the 476 shared readings are counted once, in RIVANI2022.
The Dryad deposit is the copy of record because it carries the only README of
the two (the sole statement of organism, units and replicate count) and 28
growth-control colony counts this deposit does not have.

The test is on the values, at run time, not asserted here: if the two ever
stop agreeing, or the twin directory is absent, this reader emits everything
it has instead, so a divergence appears as rows rather than as silence.  The
matching is described in src/ingest/_rivani_dup.py.

THE ONE DISAGREEMENT BETWEEN THE DEPOSITS.  MDR A (this deposit) / MDR 1 (the
twin), MEM + AK 2 MIC + 2 MIC, 2 h: printed 2.95 here and 2.75 there.  Nothing
in either deposit says which is right, so neither is corrected; the flag is
raised at run time on the RIVANI2022 row that carries the reading.

WHAT THIS DEPOSIT DOES NOT SAY.  Unlike its Dryad twin it ships no README, so
it never names the organism, never expands MEM / SAM / AK, and never says how
many replicates a value is a mean of.  Organism is therefore BLANK here and
the drug column keeps the file's own abbreviation.  There is no plated volume,
dilution or limit of detection anywhere in either file, so the floor is blank.
This deposit also has no growth-control colony counts (the growth control
appears only in its turbidity file).

THE LAYOUT, for anyone who has to re-read the fallback path.  Both files are
cp437-encoded (their only non-ASCII byte, 0xAB, is the DOS half sign) and
semicolon-delimited.  The colony-count file is stacked three-row blocks --

    MEM + SAM ; 1/2 MIC + 1/2 MIC ; Colony count (log 10) ; <7 values>
              ;                   ; Colony count change   ; <7 differences>
              ;                   ; d CFU/ml              ; d Log 10 = 4.25

-- of which only the first row is a reading; the other two are arithmetic on
it and are never ingested.  The seven columns are the times 0, 1, 2, 4, 6, 8
and 24, named in the file's own second header row as "Post incubation
measurement time (hour)".  Two further flags carried in `notes`: 5.78 is the
entry at t=0 for every one of the 32 arms and recurs unchanged at later times,
with nothing saying whether the repeats are measurements or carried forward;
and one turbidity cell is printed "0..03", which is not a number, so that
reading is emitted with no value rather than repaired.
"""
from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from src.ingest import empty
from src.ingest._rivani_dup import AGREEMENT_FLOOR, DRYAD, compare

COUNT_LABEL = "colony count (log 10)"
INOCULUM_CONSTANT = 5.78


def _rows(path: Path) -> list[list[str]]:
    with path.open(encoding="cp437", newline="") as fh:
        return [[c.strip() for c in r] for r in csv.reader(fh, delimiter=";")]


def _num(cell: str):
    try:
        return float(cell.replace(",", "."))
    except ValueError:
        return None


def _parse(d: Path) -> pd.DataFrame:
    out = []

    counts = d / "Colony_Count_Data-REV.csv"
    if counts.exists():
        rows = _rows(counts)
        times = [float(t) for t in rows[1][3:] if t]
        isolate, drug = "", ""
        for r in rows[2:]:
            r = r + [""] * (3 + len(times) - len(r))
            if r[0] and not r[1] and not r[2]:
                isolate = r[0]
                drug = ""
                continue
            if r[2].lower() != COUNT_LABEL:
                continue
            if r[0]:
                drug = r[0]
            conc = r[1]
            for t, cell in zip(times, r[3:3 + len(times)]):
                v = _num(cell)
                if v is None:
                    continue
                note = ("value is log CFU/mL as printed; deposit ships no "
                        "README, so organism, replicate count and the "
                        "expansion of MEM/SAM/AK are not stated anywhere in "
                        "it; source time unit: hours; ")
                if v == INOCULUM_CONSTANT:
                    note += ("equals 5.78, the entry at t=0 for all 32 arms -- "
                             "the file does not say whether repeats of it are "
                             "measurements or carried forward; ")
                out.append({
                    "source_file": counts.name, "sheet": "",
                    "organism": "", "strain": isolate,
                    "drug": drug, "arm": f"{drug} {conc}".strip(),
                    "time_h": t, "cfu_per_ml": 10.0 ** v,
                    "readout": "CFU", "notes": note,
                })

    turb = d / "Turbidity_Data-REV.csv"
    if turb.exists():
        rows = _rows(turb)
        times = [float(t.split()[0]) for t in rows[1][3:] if t]
        isolate = ""
        drug = ""
        for r in rows[2:]:
            r = r + [""] * (3 + len(times) - len(r))
            if not any(r):
                continue
            if r[0]:
                isolate = r[0]
                drug = ""
            if r[1]:
                drug = r[1]
            conc = r[2]
            control = drug.lower().startswith("growth control")
            for t, cell in zip(times, r[3:3 + len(times)]):
                if not cell:
                    continue
                v = _num(cell)
                note = (f"value_as_deposited={cell} McFarland turbidity as "
                        "printed; not a count, so deliberately left out of "
                        "cfu_per_ml (the schema has no column for a non-count "
                        "value); source time unit: hours; organism not named "
                        "anywhere in the deposit; ")
                if v is None:
                    note += (f"the deposit prints {cell!r} in this cell, which "
                             "is not a number; the reading is kept with no "
                             "value rather than repaired; ")
                out.append({
                    "source_file": turb.name, "sheet": "",
                    "organism": "", "strain": isolate,
                    "drug": "" if control else drug,
                    "arm": (drug if control else f"{drug} {conc}").strip(),
                    "time_h": t, "readout": "McFarland turbidity",
                    "notes": note,
                })

    if not out:
        return empty()
    return pd.DataFrame(out)


def read(d: Path) -> pd.DataFrame:
    """Only the readings the Dryad twin does not already hold -- see above."""
    mine = _parse(d)
    twin = d.parent / DRYAD
    if not len(mine) or not twin.is_dir():
        return mine

    from src.ingest.read_RIVANI2022 import _parse as twin_parse
    theirs = twin_parse(twin)
    if not len(theirs):
        return mine

    my_keys, their_vals, shared, frac, diffs = compare(mine, theirs)
    if not shared or frac < AGREEMENT_FLOOR:
        # No longer the same experiment: emit everything, and say why.
        mine = mine.copy()
        mine["notes"] = mine["notes"].astype(str).str.rstrip("; ") + (
            f"; this deposit no longer agrees with {DRYAD} "
            f"({frac:.1%} of {len(shared)} shared cells match), so nothing is "
            "suppressed as duplicate -- the two need re-checking")
        return mine

    dup = [k in their_vals for k in my_keys]
    kept = mine.loc[[not x for x in dup]].copy()
    if not len(kept):
        return empty()
    kept["notes"] = kept["notes"].astype(str).str.rstrip("; ") + (
        f"; the other {sum(dup)} readings in this deposit duplicate {DRYAD} "
        f"({frac:.1%} of shared cells identical) and are emitted there, not "
        "here; this reading has no counterpart in that deposit")
    return kept.reset_index(drop=True)
