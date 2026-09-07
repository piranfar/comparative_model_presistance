"""
The common shape every dataset in the corpus is read into.

One row per READING. Not per curve, not per condition, per reading -- because
the questions this corpus exists to answer are about individual observations:
whether a count sits at the assay floor, whether the culture had the range to
show the reduction its paper reports, how much of the spread between flasks is
the flask and how much is the laboratory. A row per curve cannot answer any of
those, and a hierarchical model needs the levels intact.

WRITING A READER. Put it in src/ingest/read_<STUDY_ID>.py, expose

    def read(d: Path) -> pd.DataFrame

where d is that dataset's directory under data/corpus/, and return a frame with
the columns below. Use blank for anything the source does not say. Every reader
is run by src/build_corpus_long.py, which validates the frame against this
schema and refuses a column it does not recognise.

THE RULE THAT MATTERS MOST. Never fill a field by inference from another paper,
a protocol, or what is usual. If a deposit does not state its plated volume, the
floor is blank and stays blank -- that absence is the corpus's most important
measurement, because the manuscript's whole argument is that it is usually
missing. A reader that quietly supplies a plausible detection limit destroys the
one number this corpus was built to count.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# name -> (dtype, what it means)
SCHEMA: dict[str, tuple[str, str]] = {
    "study_id":        ("str",   "the manifest's study_id"),
    "source_file":     ("str",   "file the row came from, relative to the dataset dir"),
    "sheet":           ("str",   "sheet or table within that file, blank if none"),
    "organism":        ("str",   "as the source states it"),
    "strain":          ("str",   "as the source states it"),
    "drug":            ("str",   "blank for an untreated or growth-control row"),
    "concentration":   ("float", "numeric value as given"),
    "conc_unit":       ("str",   "mg/L, ug/mL, xMIC -- whatever the source used"),
    "arm":             ("str",   "the source's own label for the condition"),
    "replicate":       ("str",   "flask, biological replicate or experiment id"),
    "tech_replicate":  ("str",   "plate within a sample, blank if not distinguished"),
    "time_h":          ("float", "hours since exposure began; 0 is the inoculum"),
    "colonies":        ("float", "raw colonies counted, if the source gives them"),
    "dilution":        ("float", "dilution factor the count was made at, 1 = neat"),
    "plated_volume_ul": ("float", "volume plated, if stated"),
    "cfu_per_ml":      ("float", "count per mL, as given or as derived from the above"),
    "log10_cfu_per_ml": ("float", "log10 of the above; blank where the count is zero"),
    "censored":        ("str",   "yes / no / unknown -- at or below the reporting floor"),
    "floor_cfu_per_ml": ("float", "the floor, ONLY if the source states or fixes it"),
    "floor_basis":     ("str",   "how the floor was obtained, or why it is blank"),
    "readout":         ("str",   "CFU, MPN, luminescence, OD -- what was measured"),
    "notes":           ("str",   "anything a later reader needs to know"),
}

COLUMNS = list(SCHEMA)


def empty() -> pd.DataFrame:
    """An empty frame with the right columns and dtypes."""
    return pd.DataFrame({c: pd.Series(dtype="float64" if t == "float" else "object")
                         for c, (t, _) in SCHEMA.items()})


def finish(df: pd.DataFrame, study_id: str) -> pd.DataFrame:
    """Fill in what can be derived, and nothing that cannot.

    Derives cfu_per_ml from colonies, dilution and plated volume where all three
    are present, and log10 from cfu_per_ml. Marks a reading censored only when a
    floor is actually known -- never by guessing that a zero means the floor,
    because a zero with no stated floor is precisely the ambiguity this corpus
    is meant to quantify.
    """
    for c in COLUMNS:
        if c not in df.columns:
            df[c] = np.nan if SCHEMA[c][0] == "float" else ""
    df = df[COLUMNS].copy()
    df["study_id"] = study_id
    for c, (t, _) in SCHEMA.items():
        df[c] = pd.to_numeric(df[c], errors="coerce") if t == "float" \
            else df[c].fillna("").astype(str)

    derivable = df.cfu_per_ml.isna() & df.colonies.notna() & \
        df.dilution.notna() & df.plated_volume_ul.notna()
    df.loc[derivable, "cfu_per_ml"] = (
        df.colonies * df.dilution * 1000.0 / df.plated_volume_ul)[derivable]

    pos = df.cfu_per_ml.notna() & (df.cfu_per_ml > 0)
    df.loc[pos, "log10_cfu_per_ml"] = np.log10(df.cfu_per_ml[pos])

    known = df.floor_cfu_per_ml.notna() & df.cfu_per_ml.notna()
    df.loc[known & (df.cfu_per_ml <= df.floor_cfu_per_ml), "censored"] = "yes"
    df.loc[known & (df.cfu_per_ml > df.floor_cfu_per_ml), "censored"] = "no"
    df.loc[~known & (df.censored == ""), "censored"] = "unknown"
    df.loc[df.floor_cfu_per_ml.isna() & (df.floor_basis == ""), "floor_basis"] = \
        "not stated by the source"
    return df.reset_index(drop=True)
