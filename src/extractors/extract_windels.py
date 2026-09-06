"""
Extract the Windels et al. 2024 E. coli amikacin deposit into the common tidy
schema.

Source:  data/raw/windels2024/timekill.csv     (595 rows, the nutrient x dose grid)
         data/raw/windels2024/phenotypes_after_evol.csv  (read for the MIC audit only)
Target:  data/processed/tidy_windels.csv

WHAT THIS DEPOSIT IS. Four bare CSV files, no README, no metadata, no column
dictionary. Every unit below therefore comes from OUTSIDE the deposit and is
labelled as such in the notes column of every row.

  Windels EM, Cool L, Persy E, Swinnen J, Matthay P, Van den Bergh B,
  Wenseleers T, Michiels J. "Antibiotic dose and nutrient availability
  differentially drive the evolution of antibiotic resistance and persistence."
  ISME J 2024;18(1):wrae070. doi:10.1093/ismejo/wrae070, PMID 38691440,
  PMC11102087. Data doi:10.5281/zenodo.7550302, CC BY 4.0.

THE ONE THING THAT MATTERS MOST. surv_frac is a SURVIVING FRACTION. Every
unit_group that has a t=0 row has surv_frac == 1.0 there, exactly, in all 101
such rows. The starting density has been divided out of the file. There are no
CFU counts, no plating volumes, no dilution factors and no optical densities
anywhere in any of the four files. An absolute n0 is therefore NOT RECOVERABLE
FROM THIS DEPOSIT and n0_log10 is NaN on every row. y_log10 is
log10(surviving fraction), a RELATIVE quantity, and it is not comparable with
the absolute log10 CFU/mL that tidy_era4tb.csv and tidy_vijay.csv carry in the
same column.

CENSORING. Six rows report surv_frac exactly 0.0 (nutrient 0.9, 400 ug/mL,
replicates 2 and 3, at t = 3, 5 and 8). Those are below detection: censored,
not zero and not missing. They are kept with y_log10 = NaN and censored = True.
The limit that applies to them is NOT in the deposit -- the limit in
surviving-fraction units is (CFU/mL detection floor) / N0 and neither number
exists in any file -- so limit_log10 is NaN and the notes record the lowest
non-zero surviving fraction observed anywhere in the file (7.04e-09, log10
-8.152) as an empirical UPPER BOUND on the limit, explicitly not as the limit.

UNITS, all from the paper and not from the deposit:
  * drug          amikacin. The deposit never names a drug.
  * AB_conc       ug/mL. The deposit never gives a unit. Recorded in this
                  repository at docs/16 as read from two Windels figure
                  legends, and consistent with the MIC column of
                  phenotypes_after_evol.csv, which is the standard doubling
                  series 0.5-64 on the same scale.
  * nutrient_conc DIMENSIONLESS AND UNRESOLVED. Values 0, 0.25, 0.5, 0.8, 0.9,
                  0.95. Nothing in the deposit says what they are a fraction
                  of. Carried through unchanged as state_numeric and left
                  uninterpreted.
  * time          integer 0,1,2,3,5,8, no unit in the deposit. Read as HOURS,
                  from the source paper's 8 h time-kill assay and from this
                  repository exp13/exp14, which compute per-hour kill rates
                  from this column. time_days = hours / 24.
  * dose_xmic     AB_conc / 2.0. The ANCESTRAL MIC of 2 ug/mL is not in the
                  deposit; it is the wild-type MIC recorded at
                  src/models/boccarella.py MIC_WT and in docs/16. The evolved
                  MICs in phenotypes_after_evol.csv are deliberately NOT used
                  here: they belong to populations from the evolution
                  experiment, which covers only 3 of the 6 nutrient levels and
                  4 of the 6 concentrations in this time-kill grid, and they
                  are endpoint phenotypes rather than the phenotype of the
                  culture that was killed in this assay.

NOT EXTRACTED, and why. evol_dynamics.csv is 942 rows of per-CYCLE survival
for 203 evolving populations over up to 16 daily cycles. Its `time` is a cycle
index, not time within a kill curve, and each row is an independent
single-cycle survival measurement, not a point on a decaying trajectory.
Writing it into time_days/y_log10 would produce something that looks like a
kill curve and is not one. It is reported in the extraction record instead.

Run:  python -m src.extractors.extract_windels
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "windels2024" / "timekill.csv"
MICS = ROOT / "data" / "raw" / "windels2024" / "phenotypes_after_evol.csv"
OUT = ROOT / "data" / "processed" / "tidy_windels.csv"

SCHEMA = [
    "dataset", "organism", "state", "state_numeric", "drug",
    "dose_value", "dose_unit", "dose_xmic", "unit_group", "n0_log10",
    "time_days", "y_log10", "censored", "limit_log10", "notes",
]

ANCESTRAL_MIC_UG_ML = 2.0     # NOT from the deposit; see the docstring
HOURS_PER_DAY = 24.0

PROVENANCE = (
    "deposit names no drug and no units; amikacin, ug/mL and ancestral "
    "MIC 2 ug/mL are from Windels 2024 ISME J wrae070, not from these files; "
    "nutrient_conc is dimensionless and unresolved; time read as hours"
)
RELATIVE = (
    "y_log10 = log10(surviving fraction) RELATIVE to t=0, NOT absolute "
    "log10 CFU/mL; surv_frac == 1.0 at t=0 by construction; no absolute "
    "density exists anywhere in this deposit so n0_log10 is absent"
)


def main() -> None:
    raw = pd.read_csv(RAW)
    n_raw = len(raw)

    required = {"AB_conc", "nutrient_conc", "time", "repl", "surv_frac"}
    absent = required - set(raw.columns)
    if absent:
        raise ValueError(f"timekill.csv is missing columns: {absent}")
    if raw[sorted(required)].isna().any().any():
        raise ValueError("unexpected NaN in timekill.csv; inspect before extracting")

    # --- the claim the whole extraction rests on, verified not assumed -------
    t0 = raw.loc[raw["time"] == 0, "surv_frac"]
    if not (t0 == 1.0).all():
        raise ValueError(
            "surv_frac at t=0 is not identically 1.0; the file may not be "
            "normalised to its own start and the docstring must be revised"
        )

    below = raw["surv_frac"] <= 0.0
    if (raw["surv_frac"] < 0.0).any():
        raise ValueError("negative surviving fraction in the deposit")
    n_censored = int(below.sum())

    lowest_detected = float(raw.loc[~below, "surv_frac"].min())
    bound_log10 = float(np.log10(lowest_detected))

    out = pd.DataFrame({
        "dataset": "windels2024",
        "organism": "E. coli",
        "state": ["nutrient_" + f"{v:g}" for v in raw["nutrient_conc"]],
        "state_numeric": raw["nutrient_conc"].astype(float),
        "drug": "amikacin",
        "dose_value": raw["AB_conc"].astype(float),
        "dose_unit": "ug/mL",
        "dose_xmic": raw["AB_conc"].astype(float) / ANCESTRAL_MIC_UG_ML,
        "unit_group": [
            f"windels_nut{n:g}_ab{c:g}_r{r:d}"
            for n, c, r in zip(raw["nutrient_conc"], raw["AB_conc"], raw["repl"])
        ],
        "n0_log10": np.nan,
        "time_days": raw["time"].astype(float) / HOURS_PER_DAY,
        "y_log10": np.where(
            below, np.nan, np.log10(raw["surv_frac"].where(~below, 1.0))),
        "censored": below.to_numpy(),
        "limit_log10": np.nan,
    })

    # --- notes: one row, one honest sentence per flag that applies ----------
    notes = []
    for frac, cens, hrs in zip(raw["surv_frac"], below, raw["time"]):
        parts = [f"t={hrs:g}h", RELATIVE, PROVENANCE]
        if cens:
            parts.append(
                "surv_frac reported as exactly 0 = below detection, CENSORED; "
                "no limit of quantification appears anywhere in this deposit, "
                "so limit_log10 is absent; lowest non-zero surviving fraction "
                f"in this file is {lowest_detected:.3g} (log10 {bound_log10:.3f}), "
                "an empirical upper bound on the limit and NOT the limit"
            )
        elif frac > 1.0:
            parts.append(
                f"surv_frac {frac:g} exceeds 1 (net growth or assay noise); "
                "y_log10 is positive, as reported"
            )
        notes.append("; ".join(parts))
    out["notes"] = notes

    out = out[SCHEMA]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)

    # --- extraction record, printed not written ----------------------------
    print(f"read   {RAW}  rows={n_raw}")
    print(f"wrote  {OUT}  rows={len(out)}")
    print(f"unit_groups (nutrient x dose x repl) : {out['unit_group'].nunique()}")
    print(f"censored (surv_frac == 0)            : {n_censored}")
    print(f"n0_log10 non-null                    : {int(out['n0_log10'].notna().sum())}")
    print(f"limit_log10 non-null                 : {int(out['limit_log10'].notna().sum())}")
    print(f"lowest detected surviving fraction   : {lowest_detected:.3g} "
          f"(log10 {bound_log10:.3f})")

    mic = pd.read_csv(MICS)
    cells_tk = set(zip(raw["nutrient_conc"], raw["AB_conc"]))
    cells_mic = set(zip(mic["nutrient_conc"], mic["AB_conc"]))
    print(f"time-kill grid cells                 : {len(cells_tk)}")
    print(f"of those with an evolved MIC measured: {len(cells_tk & cells_mic)}")
    print("dose_xmic is therefore anchored on the ancestral MIC, not the "
          "evolved MICs, which do not cover this grid.")


if __name__ == "__main__":
    main()
