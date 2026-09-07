"""SOU -- data.csv only, and it is byte-identical to the data.csv of
SOEORG2026 and SOEORG2026_2: all three are downloads of Zenodo record
19889677 (each PROVENANCE.json records the same sha256,
e3c144eb86668bcad8cce1afd7d98703a7801154cfd4f8bf359f3f376230b5e6).

SOU is in fact the thinnest of the three -- it lacks model.txt, the NONMEM
control stream that is the only place in the deposit naming the organism and
defining LOD as the censoring limit. SOEORG2026 has both files and is read as
the superset; this returns nothing so the 2,257 readings are not counted three
times. See src/ingest/_soeorg_dup.py: the check is on the bytes at run time, so
if the copies ever diverge this reader parses its own copy instead.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingest._soeorg_dup import read_unless_duplicate


def read(d: Path) -> pd.DataFrame:
    return read_unless_duplicate(d)
