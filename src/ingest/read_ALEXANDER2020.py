"""ALEXANDER2020 -- Dryad/Zenodo deposit (206 files unpacked), of which ONE is
a time-resolved colony count: pop-dynamics/colony-counts.xlsx.  It is also,
unusually, a deposit that states its own plating geometry, so this is one of
the few datasets in the corpus where a detection floor can be written down
from what the source says rather than left blank.

THE FILE.  Two sheets, 'Plate Set A' and 'Plate Set B'.  Each is four plate
columns (col2, col5, col8, col11) at a streptomycin level given as a multiple
of MIC.R in row 1 -- Set A: 0x, 1/32x, 1/16x, 0x; Set B: 0x, 1/8x, 1/4x, 0x --
above a stack of timepoint blocks.  A block is a banner in column A giving the
sampling time to the minute, e.g. 3h 05.5min, then six rows, one per
biologically independent replicate culture.

THE FLOOR, AND EXACTLY HOW MUCH OF IT THE SOURCE STATES.  The sheet's own
explanatory notes say: "Each entry gives the total colony count sampled from a
single biological replicate; total is across 5 plates (5 x 4ul spots) unless
otherwise noted", and two columns are annotated in place as a "total of only
4 plates".  So the PLATED VOLUME -- 20 uL, or 16 uL in those two columns -- is
stated outright, and the floor in colonies is one colony over it.

Turning that into CFU/mL needs one thing the deposit does not write in a
sentence: that the sample went onto the plate undiluted.  What the deposit
does give is arithmetic.  README-other.txt defines popsize-ANOVA.csv as these
counts "scaled up" to "estimated population size in the culture", and that
file equals colonies x 50/nplates exactly -- verified here against all 330
values, matching group by group on (plate set, [Strep], categorical time).
50/nplates is colonies x 200 uL / plated volume, so the deposit fixes the
product (dilution x culture volume) = 200 uL and nothing finer.  The sheet
says the replicates are wells in a 96-well plate and README-other.txt calls
this study's 96-well cultures "standard 200ul cultures", which leaves
dilution = 1.  dilution is therefore recorded as 1 and finish() derives
cfu_per_ml = colonies x 1000 / plated_volume_ul; the floor is one colony over
the same volume, 50 CFU/mL on five plates and 62.5 on four.

CORROBORATION FROM ELSEWHERE IN THE SAME DEPOSIT.  The MIC workbooks are not
read here (no time axis), but their 'Colony counts (inoc culture)' sheets are
worth knowing about, because they show this lab writing its plating geometry
down in full and they confirm both numbers used above.
MIC-varyinocsize-stdvol.xlsx heads its columns "Vol per plate (ul): 20" and
"Dil fac: 5000000", and its own "Est. CFU/ml by dil series" reproduces
exactly as mean colonies x dilution x 1000 / 20 -- 25.5 x 5e6 x 50 =
6.375e9, the figure printed in the sheet.  That is finish()'s formula, from
the depositor's hand.  MIC-std-allSR.xlsx says the same thing as "Plated vol
(ml) 0.02".  Two things follow: 20 uL per count is this deposit's standard,
and when a dilution IS used this depositor writes the factor down.
colony-counts.xlsx writes none.

Anyone who doubts the 200 uL should note what does and does not move with it:
a different culture volume would rescale every density AND the floor by the
same factor, so which readings sit at or below the floor -- the thing this
corpus counts -- depends only on the plated volume, which the sheet states.

NO EXACT TIME ZERO.  The sheet says sampling times are "time post-
inoculation" and gives the first as 0h 07min (Set A) and 0h 17.5min (Set B),
which it then labels "0h" for its own categorical ANOVA.  The exact minute is
kept, so the earliest reading is 0.117 h and not 0: the deposit's own
approximation is recorded in notes rather than substituted for the number.

BLANK CELLS ARE READINGS TOO.  The sheet states "Where entries are blank at a
given timepoint, there were too many colonies to count."  Those are emitted as
rows with no count and censored = "no" -- they are known to be above the
floor, they are simply not quantified.  Dropping them would silently delete
the fastest-growing cultures from every drug-free arm.

WHAT IS NOT HERE.  The deposit never names the organism or the strain in any
file -- not in either README, not in the workbook -- so organism and strain are
blank.  'Strep' is expanded to streptomycin on the authority of
README-other.txt, which defines the popsize-ANOVA column as "streptomycin
concentration, scaled by MIC.R".

NOT READ, and why:
  ~200 plate-reader .txt files (OD595 and fluorescence per well) from the
    seeding and null-model experiments: they are scored as grown / not grown
    after three days, not as densities over time.
  platedata_*.txt, data.Strep_*.txt, growthdata.*_*.txt: replicate counts that
    showed growth, i.e. tallies of wells, not cell counts.
  MIC-*.xlsx: MIC readings, no time-kill.  Their 'Colony counts (inoc
    culture)' sheets do hold real colony counts with a stated plated volume
    and dilution factor, but they estimate the density of one overnight
    culture at a single time with no arm, so there is no reading in the
    schema's sense to make of them.  Flag them if the corpus ever wants
    plating geometry on its own.
  PoissonCFUtest.R: 3 x 48 raw 4 uL spot counts of one sample, with no time
    axis and no arm -- excellent plating-geometry data but not a reading in a
    time series, so left out rather than forced into this schema.
  competition24h-flowcyto.xlsx, staining7h-flowcyto.xlsx: flow-cytometry event
    counts at a single time.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from src.ingest import empty

WORKBOOK = "colony-counts.xlsx"
TIME_RE = re.compile(r"^\s*(\d+)\s*h\s*([\d.]+)\s*min", re.I)
SPOT_UL = 4.0
DEFAULT_PLATES = 5
DRUG = "streptomycin"
CONC_UNIT = "x MIC.R"

FLOOR_BASIS = (
    "one colony over the plated volume the sheet itself states: 'total is "
    "across 5 plates (5 x 4ul spots)' = 20 uL, or 16 uL in the two columns "
    "the sheet annotates in place as a 'total of only 4 plates'. The per-mL "
    "conversion additionally takes the sample as plated neat, which the "
    "deposit fixes only to (dilution x culture volume) = 200 uL "
    "(popsize-ANOVA.csv = colonies x 50/nplates, verified against all 330 "
    "values) together with README-other.txt calling this study's 96-well "
    "cultures 'standard 200ul cultures'. A different culture volume would "
    "rescale the densities and this floor by the same factor, leaving which "
    "readings are censored unchanged"
)


def _conc(label: str):
    """Turn a level label into a number: 1/32x -> 0.03125, 0x -> 0.0."""
    s = str(label).strip().rstrip("xX")
    if not s:
        return None
    try:
        if "/" in s:
            a, b = s.split("/")
            return float(a) / float(b)
        return float(s)
    except ValueError:
        return None


def read(d: Path) -> pd.DataFrame:
    hits = sorted(d.rglob(WORKBOOK))
    if not hits:
        return empty()
    path = hits[0]
    xl = pd.ExcelFile(path)

    rows = []
    for sheet in xl.sheet_names:
        g = xl.parse(sheet, header=None)
        plate_col = {c: str(g.iat[0, c]).strip() for c in range(1, g.shape[1])
                     if isinstance(g.iat[0, c], str)}
        conc_lbl = {c: str(g.iat[1, c]).strip() for c in range(1, g.shape[1])
                    if isinstance(g.iat[1, c], str)}
        cols = sorted(set(plate_col) & set(conc_lbl))
        if not cols:
            continue

        banners = []
        for r in range(len(g)):
            v = g.iat[r, 0]
            if isinstance(v, str) and TIME_RE.match(v):
                banners.append((r, v.strip()))

        for i, (r0, banner) in enumerate(banners):
            m = TIME_RE.match(banner)
            t = float(m.group(1)) + float(m.group(2)) / 60.0
            r1 = banners[i + 1][0] if i + 1 < len(banners) else len(g)

            plates = {c: DEFAULT_PLATES for c in cols}
            data_rows = []
            for r in range(r0 + 1, r1):
                cells = {c: g.iat[r, c] for c in cols}
                if any(isinstance(v, str) and v.strip() for v in cells.values()):
                    for c, v in cells.items():
                        if isinstance(v, str) and "4 plates" in v:
                            plates[c] = 4
                    continue
                if all(pd.isna(v) for v in cells.values()):
                    continue
                data_rows.append(cells)

            for k, cells in enumerate(data_rows, start=1):
                for c in cols:
                    v = cells[c]
                    vol = plates[c] * SPOT_UL
                    conc = _conc(conc_lbl[c])
                    common = {
                        "source_file": str(path.relative_to(d)).replace("\\", "/"),
                        "sheet": sheet, "organism": "", "strain": "",
                        "drug": "" if conc == 0 else DRUG,
                        "concentration": conc, "conc_unit": CONC_UNIT,
                        "arm": "[Strep] " + conc_lbl[c] + " (" + plate_col[c] + ")",
                        "replicate": sheet[-1] + "-" + plate_col[c] + "-" + str(k),
                        "time_h": t, "readout": "CFU",
                        "floor_cfu_per_ml": 1000.0 / vol,
                        "floor_basis": FLOOR_BASIS,
                    }
                    stem = ("sampling time as the sheet prints it: " + banner +
                            "; total across " + str(plates[c]) + " spots of "
                            "4 uL")
                    if pd.isna(v):
                        rows.append({**common, "censored": "no",
                                     "notes": stem + "; blank in the sheet, "
                                     "which its notes define as too many "
                                     "colonies to count -- a reading above "
                                     "the quantifiable range, kept with no "
                                     "value rather than dropped"})
                    else:
                        rows.append({**common, "colonies": float(v),
                                     "dilution": 1.0,
                                     "plated_volume_ul": vol,
                                     "notes": stem})
    if not rows:
        return empty()
    return pd.DataFrame(rows)
