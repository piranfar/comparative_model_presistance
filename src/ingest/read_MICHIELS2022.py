"""MICHIELS2022 -- the same file as GEERTS2022.

Both directories hold "Manuscript_persistence_in_S._pneumoniae_raw_data.xlsx"
downloaded from Zenodo record 7147832, byte-identical (sha256
56ef476b71abb121968e735de489f715f409c16584ce357ae55a54e65a51b273, recorded in
both PROVENANCE.json files). The two study_ids are one deposit fetched twice,
not two studies.

GEERTS2022 is read as the copy of record; this returns nothing so the same
2,554 readings are not counted twice. The test is on the bytes at run time, so
if the two ever diverge this reader parses its own copy in full rather than
silently returning an empty frame.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from src.ingest import empty
from src.ingest.read_GEERTS2022 import XLSX, read as read_geerts

PRIMARY = "GEERTS2022"


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(d: Path) -> pd.DataFrame:
    mine, theirs = d / XLSX, d.parent / PRIMARY / XLSX
    if mine.exists() and theirs.exists() and _sha256(mine) == _sha256(theirs):
        return empty()
    return read_geerts(d)
