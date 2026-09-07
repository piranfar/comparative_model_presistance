"""Shared duplicate check for the three copies of Zenodo record 19889677.

SOU, SOEORG2026 and SOEORG2026_2 are three downloads of one Zenodo record.
data.csv is byte-identical in all three (sha256
e3c144eb86668bcad8cce1afd7d98703a7801154cfd4f8bf359f3f376230b5e6, which is also
what each directory's own PROVENANCE.json records), and model.txt is identical
in the two directories that have it. SOEORG2026 is the superset -- it carries
both files -- so it is the copy that yields rows and the other two return
nothing, rather than the same 2,257 readings being counted three times.

The check is made at run time on the bytes, not asserted from this comment: if
a copy ever stops matching, its reader falls back to parsing it in full so the
divergence shows up as rows rather than as silence.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from src.ingest import empty

PRIMARY = "SOEORG2026"


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def read_unless_duplicate(d: Path) -> pd.DataFrame:
    """Empty if this directory's data.csv matches the primary copy's."""
    mine = d / "data.csv"
    theirs = d.parent / PRIMARY / "data.csv"
    if mine.exists() and theirs.exists() and _sha256(mine) == _sha256(theirs):
        return empty()

    # Not (or no longer) a duplicate -- parse it rather than lose it.
    from src.ingest.read_SOEORG2026 import read as read_primary
    return read_primary(d)
