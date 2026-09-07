"""SOEORG2026_2 -- a second download of Zenodo record 19889677, byte-identical
to SOEORG2026 in both files (data.csv sha256
e3c144eb86668bcad8cce1afd7d98703a7801154cfd4f8bf359f3f376230b5e6, model.txt
sha256 7f0a5acede2ce0d697a6e7e627ff877e2f14dcd639f9fb5a5f78dacf3bd936db).

SOEORG2026 is read as the copy of record; this returns nothing so the same
2,257 readings are not counted twice. The duplicate test is made on the bytes
at run time -- see src/ingest/_soeorg_dup.py.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingest._soeorg_dup import read_unless_duplicate


def read(d: Path) -> pd.DataFrame:
    return read_unless_duplicate(d)
