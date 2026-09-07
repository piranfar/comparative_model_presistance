"""EDOO2026 -- alpibectir / ethionamide, Nature Communications Source Data.

The deposit is two workbooks.  Only ONE sheet in either of them is a time-kill:

    41467_2026_71460_MOESM6_ESM.xlsx, sheet "Fig 6"
        "log CFU/mL", two strain blocks (H37Rv and H37Rv dAdhD), eight arms per
        block, three unlabelled replicate columns per arm, days 0-21.

Everything else in the deposit was read and deliberately left out:

  * MOESM3_ESM.xls "Table1"          whole-proteome MS/MS fold changes
  * Fig 1A-E, 1F, 4, 5, Supp Figs 1-5, 7, 11, 12, Supp Table 3
                                     checkerboard endpoint assays (GFP
                                     fluorescence, luminescence, resazurin) with
                                     no time axis at all
  * Fig 3A, Supp Fig 5              SEAP reporter dose-response, no time axis
  * Fig 3B-C, Supp Fig 6            thermal shift, x axis is temperature in
                                     degrees C, not time
  * Table 1, Supp Table 4           resistant-colony counts from a single
                                     plating, no time axis
  * Fig 7, Supp Tables 7A/7B,
    Supp Fig 13, Supp Fig 14        mouse experiments reported as log CFU/LUNGS,
                                     as a delta log, or as survival counts.
                                     These are real counts but they are per
                                     organ, not per mL; the schema's only count
                                     column is cfu_per_ml, and writing a burden
                                     per pair of lungs into a per-mL column
                                     would corrupt every model fitted on it.

The Fig 6 sheet states no limit of detection.  Many killed-arm readings sit at
exactly log10 = 2.00, which is what a reporting floor looks like, but the
deposit never says so, so floor_cfu_per_ml stays blank and floor_basis says why.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

WORKBOOK = "41467_2026_71460_MOESM6_ESM.xlsx"
SHEET = "Fig 6"
SUBDIR = Path("_unpacked") / "PMC13234193_supplementary"

# "Eto 2.5 mg/L", "Alpibectir 0.003 mg/L", "INH 2.5 mg/L"
DOSE = re.compile(r"([A-Za-z][A-Za-z0-9\-]*)\s+([\d.]+)\s*(mg/L)")
NO_DRUG = re.compile(r"^(no drug|no treatment|untreated|control)$", re.I)

FLOOR_BASIS = (
    "not stated: the workbook gives no limit of detection anywhere. Many "
    "killed-arm readings sit at exactly log10 2.00 (100 CFU/mL), which is what "
    "a reporting floor looks like, but the deposit never says it is one, so no "
    "floor is recorded here"
)


def _blocks(raw: pd.DataFrame):
    """Yield (strain_label, header_row, day_col) for each 'Day' header row."""
    for i in range(len(raw)):
        hit = [j for j, v in enumerate(raw.iloc[i]) if str(v).strip() == "Day"]
        if not hit:
            continue
        day_col = hit[0]
        # the strain sits on the row immediately above, in the first data column
        strain = ""
        if i > 0:
            above = [str(v).strip() for v in raw.iloc[i - 1]
                     if isinstance(v, str) and str(v).strip()]
            if above:
                strain = above[0]
        yield strain, i, day_col


def read(d: Path) -> pd.DataFrame:
    path = d / SUBDIR / WORKBOOK
    if not path.exists():
        hits = list(d.rglob(WORKBOOK))
        if not hits:
            return empty()
        path = hits[0]
    rel = str(path.relative_to(d)).replace("\\", "/")

    raw = pd.read_excel(path, sheet_name=SHEET, header=None)

    unit_cell = next((str(v).strip() for v in raw.values.ravel()
                      if isinstance(v, str) and "CFU" in v), "")
    if "log" not in unit_cell.lower() or "/ml" not in unit_cell.lower():
        raise ValueError("%s: expected a 'log CFU/mL' banner, found %r"
                         % (SHEET, unit_cell))

    out = []
    for strain, hdr, day_col in _blocks(raw):
        # data rows for this block: numeric Day cells until the run breaks
        body = []
        for i in range(hdr + 1, len(raw)):
            try:
                day = float(raw.iat[i, day_col])
            except (TypeError, ValueError):
                break
            if not np.isfinite(day):
                break
            body.append((i, day))
        if not body:
            continue
        rows_idx = [i for i, _ in body]

        val_cols = [c for c in range(day_col + 1, raw.shape[1])
                    if any(isinstance(raw.iat[i, c], (int, float, np.number))
                           and np.isfinite(raw.iat[i, c]) for i in rows_idx)]
        labels = [(c, str(raw.iat[hdr, c]).strip())
                  for c in range(day_col + 1, raw.shape[1])
                  if isinstance(raw.iat[hdr, c], str) and str(raw.iat[hdr, c]).strip()]
        bounds = [c for c, _ in labels] + [raw.shape[1]]

        for k, (lcol, label) in enumerate(labels):
            cols = [c for c in val_cols if lcol <= c < bounds[k + 1]]
            doses = DOSE.findall(label)
            if NO_DRUG.match(label):
                drug, cval, cunit, dose_note = "", np.nan, "", ""
            elif len(doses) == 1:
                name, val, unit = doses[0]
                drug, cval, cunit, dose_note = name, float(val), unit, ""
            elif len(doses) > 1:
                drug = " + ".join(n for n, _, _ in doses)
                cval, cunit = np.nan, ""
                dose_note = ("a two-drug arm; the sheet's own label gives the "
                             'concentrations as "%s", which the single '
                             "concentration column cannot hold" % label)
            else:
                # a label this reader does not understand: skip it rather than
                # guess what condition it names
                continue

            for i, day in body:
                for rep, c in enumerate(cols, start=1):
                    v = raw.iat[i, c]
                    if not (isinstance(v, (int, float, np.number)) and np.isfinite(v)):
                        continue
                    out.append({
                        "source_file": rel, "sheet": SHEET,
                        "organism": "", "strain": strain,
                        "drug": drug, "concentration": cval, "conc_unit": cunit,
                        "arm": label, "replicate": str(rep),
                        "time_h": day * 24.0,
                        "cfu_per_ml": float(10.0 ** float(v)),
                        "floor_basis": FLOOR_BASIS,
                        "readout": "CFU",
                        "notes": dose_note,
                    })

    if not out:
        return empty()

    df = pd.DataFrame(out)
    common = (
        'the sheet reports log10 CFU/mL ("%s"); cfu_per_ml here is 10**value, '
        "not the log; day converted to hours (source in days); the three "
        "columns under each arm are unlabelled and the sheet does not say "
        "whether they are biological or technical replicates, so they are "
        "numbered 1-3; the day-0 readings are identical across every arm within "
        "a strain block, so one inoculum measurement is shared by all arms; "
        "organism left blank because this sheet names only the strain and never "
        "the species (the species appears only on the unrelated 'Supp Fig 14' "
        "sheet of the same workbook); no plated volume, dilution or colony "
        "count is given anywhere in the deposit" % unit_cell
    )
    df["notes"] = [("; ".join(x for x in (n, common) if x)) for n in df["notes"]]
    return finish(df, "EDOO2026")
