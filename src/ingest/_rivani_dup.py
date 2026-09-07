"""Shared duplicate handling for the two deposits of one Acinetobacter
baumannii combination time-kill.

RIVANI2022 is the Dryad/Zenodo deposit (10.5061/dryad.rxwdbrvc3); RIVANI2022_2
is the figshare "REV" copy (10.6084/m9.figshare.20024270.v3), whose own
PROVENANCE.json already records that "a CC0 twin sits on Dryad at
10.5061/dryad.rxwdbrvc3".  They are not two experiments.  Compared cell by
cell at run time:

  * all 224 of the figshare deposit's colony-count readings share a key with
    the Dryad deposit's, and 223 of them are numerically identical.  One is
    not: MDR A / MDR 1, MEM + AK 2 MIC + 2 MIC, 2 h, printed 2.75 in the Dryad
    file and 2.95 in the figshare file.
  * all 252 of the Dryad deposit's turbidity readings appear unchanged in the
    figshare file, which adds a 48 h column the Dryad file does not have.
  * the Dryad deposit additionally has 28 growth-control colony counts that
    the figshare deposit does not, and the only README of the two.

So neither is a strict superset, but the overlap is 476 readings.  The Dryad
deposit is taken as the copy of record because it carries the README (the only
statement of organism, units and replicate count anywhere in either deposit)
and the growth-control counts; the figshare reader emits only what its twin
does not contain, so the shared 476 are counted once.

THE TEST IS MADE ON THE VALUES AT RUN TIME, NOT ASSERTED FROM THIS COMMENT.
If the two ever stop agreeing -- if either deposit is revised, or the wrong
directory is passed -- the figshare reader falls back to emitting everything
it has, so a divergence shows up as rows rather than as silence.

MATCHING THE LABELS.  The two deposits name the same things differently:
isolates are "ATCC 19606 / MDR 1 / MDR 2 / XDR" in one and "ATCC / MDR A /
MDR B / XDR" in the other, and arms are "MEM+SAM 0,5+0,5 MIC" against
"MEM + SAM 1/2 MIC + 1/2 MIC".  Arms are matched by flattening the text (case,
spaces, the half sign, the comma decimal mark and the word MIC all removed),
which makes the two spellings identical.  Isolates are matched by ORDER OF
FIRST APPEARANCE in each file rather than by asserting that "MDR 1" is the
same isolate as "MDR A": that equivalence is nowhere written down in either
deposit, and position is what the files actually give.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

DRYAD = "RIVANI2022"
FIGSHARE = "RIVANI2022_2"

# below this fraction of agreeing shared cells the two are no longer the same
# experiment, and nothing is suppressed
AGREEMENT_FLOOR = 0.90

_VALUE_RE = re.compile(r"value_as_deposited=(\S+)")


def _canon_arm(arm: str) -> str:
    """'MEM+SAM 0,5+0,5 MIC' and 'MEM + SAM 1/2 MIC + 1/2 MIC' -> one string."""
    s = str(arm).upper().replace("½", "0.5").replace(",", ".")
    return s.replace("MIC", "").replace(" ", "")


def _isolate_rank(labels) -> dict[str, int]:
    """label -> index of first appearance, so the deposits' different isolate
    names line up by position instead of by an equivalence neither states."""
    rank: dict[str, int] = {}
    for x in labels:
        x = str(x).strip()
        if x not in rank:
            rank[x] = len(rank)
    return rank


def _printed_value(row):
    """What the source printed, as a float where it is one.

    Counts come back as log10, which is what both files actually print;
    turbidity comes back from the value_as_deposited token in notes, because
    the schema has no column for a non-count value.
    """
    if row.readout == "CFU" and pd.notna(row.cfu_per_ml):
        return round(float(np.log10(row.cfu_per_ml)), 6)
    m = _VALUE_RE.search(str(row.notes))
    if not m:
        return None
    try:
        return round(float(m.group(1)), 6)
    except ValueError:
        return m.group(1)  # e.g. the file that prints '0..03'


def keyed(df: pd.DataFrame) -> tuple[list[tuple], dict[tuple, object]]:
    """Per-row keys, and the key -> printed-value map they build."""
    rank = _isolate_rank(df.strain)
    keys = [(rank[str(r.strain).strip()], _canon_arm(r.arm), float(r.time_h),
             r.readout) for r in df.itertuples()]
    values = {k: _printed_value(r) for k, r in zip(keys, df.itertuples())}
    return keys, values


def compare(mine: pd.DataFrame, theirs: pd.DataFrame):
    """-> (my keys, their value map, shared keys, agreeing fraction, diffs)."""
    my_keys, my_vals = keyed(mine)
    _, their_vals = keyed(theirs)
    shared = set(my_vals) & set(their_vals)
    comparable = [k for k in shared
                  if isinstance(my_vals[k], float)
                  and isinstance(their_vals[k], float)]
    agree = sum(1 for k in comparable if my_vals[k] == their_vals[k])
    frac = agree / len(comparable) if comparable else 0.0
    diffs = {k: (my_vals[k], their_vals[k]) for k in shared
             if my_vals[k] != their_vals[k]}
    return my_keys, their_vals, shared, frac, diffs


def annotate_discrepancies(mine: pd.DataFrame, theirs: pd.DataFrame,
                           twin_id: str) -> pd.DataFrame:
    """Flag, on my own rows, every cell the twin deposit prints differently.

    The value is never replaced -- this reader reports the file it was given.
    """
    my_keys, their_vals, _, _, diffs = compare(mine, theirs)
    if not diffs:
        return mine
    out = mine.copy()
    notes = list(out["notes"])
    for i, k in enumerate(my_keys):
        if k in diffs:
            mine_v, their_v = diffs[k]
            notes[i] = (str(notes[i]) + "; DEPOSIT DISAGREEMENT: the twin "
                        f"deposit {twin_id} prints {their_v} where this file "
                        f"prints {mine_v} for the same isolate, arm and time. "
                        "Both are transcriptions of one reading; this reader "
                        "keeps the value in the file it was given")
    out["notes"] = notes
    return out
