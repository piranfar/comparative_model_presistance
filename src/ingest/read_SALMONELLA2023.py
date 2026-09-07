"""SALMONELLA2023 -- a second fetch of the same Zenodo record as NOREL2023.

Both directories hold the same twelve workbooks from Zenodo record 10277562
(concept DOI 10.5281/zenodo.10277561). This is not a resemblance: every one of
the twelve files is byte-identical across the two directories, and the two
PROVENANCE.json files list the same twelve sha256 digests --

    M13_Persisters-LB.xlsx   72d72227930e85fbd886a5fec2aa70fdb2d5be2c06f6c83a4fb11efadac7616f
    M14_Persisters-LB.xlsx   c0dbbd1c80639ed86ec4d4d939af9c02b5a986a09e429080ccb86fc74e89e7b7
    M18_persisters-LB.xlsx   7dcdc01e08ae8d3c9ae786ec8e5a5a7b048f4b94e419b7c228f324ee740cd8e1
    M19_persisters-LB.xlsx   b817ed5a0d580b573a4f1a703aa89416dcfbb2ead3fcddb4c94b34c5221ad2a9
    M20_persisters-LB.xlsx   bfba1bc3897dd65a399714508d1fbf6c68f64bbb20bfea74fc6ce68b10ffeaee
    M28_persisters-M63.xlsx  98a50f82b55de33c3af7abc96643242e7f384355b2ab219b1013a0b37b72b576
    M56_persisters-LB.xlsx   53e92163078eb952adf6c80ff1bc8a9b67da8f8cc849d800549d68d5332897eb
    M70_persisters-LB.xlsx   e81afd3cbb949f3446a2850cdd7a80662c0a84b8c7f8451d9eb2db720d210977
    M77_persisters-M63.xlsx  c8de67e344d3d584f8a154c66a131f684de9b53e87a1993e3eb28f148d83ee2a
    M7_persisters-LB.xlsx    0fd4c46b57fcb17fe0a79980a65e31a065a6583d725d3067ef2b704307d3290e
    M96_persisters-LB.xlsx   6675e85021782fe3618377ec243900b440d76923177d4bc464cea629afb493cf
    M97_persisters-LB.xlsx   9c059c743fd455e3011b775088f5ea36912344a504095c9a4e0deb83ef5b9ae2

Reading them twice would put every one of those readings into the corpus twice
and silently halve the apparent between-experiment variance, so this reader
returns nothing and read_NOREL2023.py carries the record. The verification below
runs on every build: if the two directories ever stop matching -- a corrected
file, a new version of the record fetched into one of them -- the reader raises
rather than staying quietly empty, because at that point the duplicate decision
would no longer be safe.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from src.ingest import empty

STUDY = "SALMONELLA2023"
TWIN = "NOREL2023"


def _digests(d: Path) -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(d.glob("*.xlsx"))}


def read(d: Path) -> pd.DataFrame:
    twin = d.parent / TWIN
    if not twin.is_dir():
        raise FileNotFoundError(
            f"{STUDY} is held to be a duplicate of {TWIN}, but {twin} is not "
            f"there to check that against; do not trust the empty frame")
    mine, theirs = _digests(d), _digests(twin)
    if mine != theirs:
        only_mine = sorted(set(mine) - set(theirs))
        differ = sorted(k for k in set(mine) & set(theirs) if mine[k] != theirs[k])
        raise ValueError(
            f"{STUDY} was skipped as a byte-identical duplicate of {TWIN}, but "
            f"the two directories no longer match (files only here: {only_mine}; "
            f"same name, different content: {differ}). Read it properly instead "
            f"of returning an empty frame.")
    return empty()
