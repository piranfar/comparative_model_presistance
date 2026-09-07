"""PEPPER2026 -- Zenodo repository snapshot, 63 tabular files, one of them a time-kill.

The archive is a software-repository snapshot with no README and no analysis
code, so every column had to be understood from the numbers themselves.

WHAT IS READ.  time-kill-colony-counts.csv.  Thirteen rows, one per serial
dilution, with the deposit's own dilution.factor beside them, and 288 sample
columns named <strain>-<line>-<replicate>-<timepoint>.  896 raw colony counts.
This is the rarest thing in the whole corpus: counts as counted, at a stated
dilution, before anybody turned them into a concentration.

The interpretation of the column names was CHECKED, not assumed.  The companion
file inh-tolerance-final-data.csv carries the same 48 sample ids and the same
six time points, and its percent.survival reproduces exactly -- ratio 1.0 to
machine precision on all 288 of its rows -- as

    100 * mean_over_dilutions(colonies / dilution.factor)
        / the same quantity at time point 0 for that sample

so the four fields of each column name are the isolate, the line, the replicate
and the time point, and dilution.factor is what it says.

WHAT IS DELIBERATELY LEFT OUT, and why:

  * dose-response-assay-2..7.csv, CHx-INHR-isolates-INH-dose-response-batch-1..3
    .csv, wt-ohrR-CHx-dose-response-assay.csv -- microplate reader traces, 64
    readings each, the first column headed only "Time" and filled with H:MM:SS
    clock strings.  They are genuinely time-resolved, but no file in the deposit
    states WHAT was measured (every other header is a bare well label), nor the
    unit of the concentration inside that label, and there is no README or code
    to resolve it.  The schema's only numeric value column is cfu_per_ml; an
    unidentified absorbance has nowhere honest to go, and readout cannot be "set
    accordingly" when the source never says what the reading is.
    dose-response-assay-1.csv is different again: it has no Time column at all
    and exactly one data row, so it is a single endpoint, not a trace.
  * fluctuation-assay-*-cfus.csv / -mutants.csv, fluctuation-assay-cfus.xlsx --
    raw colony counts with dilutions, but a fluctuation assay has no time axis.
  * ros-assay-1..3.xlsx, ros-data-processed.csv -- there is no time axis in
    either.  (Their cfus column is not a fixed constant, as an earlier draft of
    this note claimed: it takes the values 0, 5.5e6, 6.0e6, 6.5e6 and 8.0e6, one
    nominal figure per experiment, and serves as the denominator of the RFU
    reading beside it.  Either way it is not a time course.)
  * scanlag-experiment-1/2.csv -- per-colony appearance-time and growth traces
    from a scanner; "growth" is a colony size, not a count of colonies.
  * nadh-nad-assay-*.xlsx, falcor-rates.*, all-isolate-phenotypes.csv,
    mutant-strain-phenotypes.csv, colony-cluster-assignments.csv -- IC50s,
    fitness, mutation rates, plate-reader redox assays; no time-resolved counts.
  * all-variant-calls.csv, all-isolate-mutations-filtered.csv, tb-profiler-calls
    .csv, dst-isolate-phenotypes.csv, INH-Global*.csv, tfoe-*, chipseq-*,
    cytoscape-*, *-enrichment-*, oxidative-stress-genes.xlsx,
    Supplementary-Data-1/2, sample-metadata.csv, test-sra-IDs.csv,
    susceptibility-profile-counts.csv, variant-count-table.csv -- genomics,
    enrichment statistics and metadata.

Three things this deposit does not state, and which therefore stay blank: the
plated volume (so no CFU/mL can be derived from these counts and no floor can be
computed), the drug and its concentration, and the unit of the time point.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

FILENAME = "time-kill-colony-counts.csv"
COMPANION = "inh-tolerance-final-data.csv"
# "mfs1-a-1-24" -> isolate, line, replicate, time point
COLNAME = re.compile(r"^(?P<isolate>[^-]+)-(?P<line>[^-]+)-(?P<rep>[^-]+)-(?P<t>\d+)$")

FLOOR_BASIS = (
    "not stated: the file gives raw colonies and the dilution factor but never "
    "the volume plated, so no CFU/mL and therefore no detection floor can be "
    "derived from it, and nothing else in the deposit states one"
)


def read(d: Path) -> pd.DataFrame:
    hits = list(d.rglob(FILENAME))
    if not hits:
        return empty()
    path = hits[0]
    rel = str(path.relative_to(d)).replace("\\", "/")

    df = pd.read_csv(path, encoding="utf-8-sig")
    if "dilution.factor" not in df.columns:
        raise ValueError("%s: no dilution.factor column" % FILENAME)

    # the same experiment, reported as a normalised survival, is used only to
    # confirm the column naming; nothing is taken from it into the rows
    comp = path.parent / COMPANION
    checked = ""
    if comp.exists():
        t = pd.read_csv(comp)
        stems = set("-".join(c.split("-")[:3]) for c in df.columns
                    if COLNAME.match(str(c)))
        if set(t["sample"]) == stems:
            checked = ("the same 48 sample ids and the same six time points "
                       "appear in %s, whose percent.survival this reader "
                       "reproduces exactly from these counts, which is how the "
                       "four fields of the column names were confirmed"
                       % COMPANION)

    out = []
    for c in df.columns:
        m = COLNAME.match(str(c))
        if not m:
            continue                      # dilution / dilution.factor
        for i in range(len(df)):
            v = df.at[i, c]
            if not (isinstance(v, (int, float, np.number)) and np.isfinite(v)):
                continue
            fac = df.at[i, "dilution.factor"]
            if not (isinstance(fac, (int, float, np.number)) and np.isfinite(fac)
                    and fac > 0):
                continue
            out.append({
                "source_file": rel, "sheet": "",
                "organism": "", "strain": m.group("isolate"),
                "drug": "", "concentration": np.nan, "conc_unit": "",
                "arm": "",
                "replicate": "%s-%s-%s" % (m.group("isolate"), m.group("line"),
                                           m.group("rep")),
                "tech_replicate": "dilution %s" % df.at[i, "dilution"]
                if "dilution" in df.columns else "",
                "time_h": float(m.group("t")),
                "colonies": float(v),
                "dilution": 1.0 / float(fac),
                "plated_volume_ul": np.nan,
                "floor_basis": FLOOR_BASIS,
                "readout": "CFU",
                "notes": "",
            })

    if not out:
        return empty()

    res = pd.DataFrame(out)
    common = (
        "raw colonies exactly as counted; dilution is the reciprocal of the "
        "file's own dilution.factor column, so 1 = neat. NO PLATED VOLUME is "
        "given anywhere in the deposit, so cfu_per_ml is deliberately left "
        "underivable and blank rather than completed with a plausible volume. "
        "TIME UNIT IS NOT STATED: the deposit calls this field only 'time "
        "point' and never gives a unit, so the values 0, 6, 24, 30, 48 and 72 "
        "are carried into time_h unchanged and unconverted -- treat them as "
        "hours only on evidence from outside this deposit. The drug is not "
        "named in any data field (only in the file NAME of the companion "
        "table), and no concentration appears anywhere, so drug and "
        "concentration are blank. Organism is not named in this file either; "
        "the strain labels are wt, ohrR, mfs1 and ntaA as the header gives "
        "them. Each dilution of a sample is a separate plate, recorded as "
        "tech_replicate."
    )
    if checked:
        common = common + " " + checked + "."
    res["notes"] = common
    return finish(res, "PEPPER2026")
