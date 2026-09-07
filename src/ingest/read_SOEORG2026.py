"""Soeorg 2026 -- Zenodo 19889677: a NONMEM dataset (data.csv) plus the control
stream (model.txt) for a meropenem + colistin/polymyxin B PK/PD model of
Acinetobacter baumannii, built from time-kill curves the depositor extracted
from published papers.

WHAT THE DEPOSIT ACTUALLY SAYS, and how this reader uses it.

  * model.txt $PROBLEM names the organism: "Meropenem and colistin/polymyxin B
    against Acinetobacter baumannii". Nothing anywhere names a strain, so
    `strain` stays blank even though each ID plainly is one.

  * Only CMT=4 carries bacteria (model.txt: COMP=(BTOT)). Every EVID=0 row in
    the file is CMT=4, so the drug compartments (CMT=1 meropenem, CMT=3
    colistin) contribute no observations at all -- they appear only as EVID=1
    dosing and EVID=3 reset records, which are dropped.

  * DV on CMT=4 is log10 of the bacterial compartment: $ERROR sets
    IPRED = LOG10(A(4)) and Y = IPRED + EPS(1), and A(4) starts at 10**INOC.
    So cfu_per_ml = 10**DV.  The deposit never writes the unit down; "CFU/mL"
    is this reader's label for a density the deposit leaves unlabelled, and the
    note on every row says so.

  * THE FLOOR IS STATED, which is rare enough to spell out. Column LOD carries
    10, 20, 100 or 400 (constant within an ID), and $ERROR uses it as the
    censoring limit for the M3 method: LOQ = LOG10(LOD), compared against the
    same LOG10(A(4)) that DV is compared against. So LOD is on the same linear
    density scale as 10**DV and is a genuine, source-stated reporting floor --
    not one this reader supplied. Column BLOD is the depositor's own
    below-limit flag; every BLOD=1 row has DV exactly log10(LOD).

  * The starting density is stated as a nominal target, not measured: INOC_TH
    is log10 of the intended inoculum (4-8), and $PK sets A_0(4) = 10**INOC
    with INOC = THETA(1)*INOC_TH, THETA(1) = 1 FIX. The measured t=0 reading is
    the DV at TIME=0. Both are kept -- the reading in cfu_per_ml, the nominal
    target in notes.

WHAT IS LEFT UNRESOLVED.

  * Concentration UNIT. CSET_MERO and CSET_COL are the static concentrations
    (model.txt: Cmero = CmeroCOMP*(1-SRC_MERO) + CSET_MERO*SRC_MERO), and they
    live on the same scale as MIC_meropenem / MIC_colpmb, because EC50_MER =
    THETA(8)*MIC_meropenem. Nothing in the deposit names that scale, so
    conc_unit is blank.

  * Dynamic-regimen arms. Where SRC_MERO or SRC_COL is 0 the drug is dosed
    through AMT/RATE/ADDL/II and its concentration varies over the curve; there
    is no single number to put in `concentration`, so it is left blank and the
    arm is labelled "dynamic".

  * Combination arms carry two concentrations and the schema has one column, so
    `concentration` is blank there too and both values go in `arm`.

  * TIME has no stated unit. It is read as hours: values run 0-24, the dosing
    intervals II are 8 and 12, and the model's KG = 0.329 and KE are per-hour
    rate constants. That reasoning is recorded in notes rather than hidden.

  * Which of the depositor's source papers each ID came from is not in the
    file. ID and OCC are carried through verbatim in `replicate` so the
    clustering survives, but no ID can be attributed to a paper here.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty

TIME_NOTE = ("TIME read as hours: the deposit does not label the unit, but "
             "values run 0-24, dosing II is 8 and 12, and model.txt's KG and "
             "KE are per-hour rate constants")
SCALE_NOTE = ("DV is log10 of the bacterial compartment ($ERROR: "
              "IPRED=LOG10(A(4))); the deposit never names the density unit, "
              "CFU/mL is this reader's label")


def _fmt(x: float) -> str:
    """A concentration as the file writes it, without trailing zeros."""
    return f"{x:g}"


def read(d: Path) -> pd.DataFrame:
    src = d / "data.csv"
    if not src.exists():
        return empty()

    raw = pd.read_csv(src, na_values=["."])

    # EVID=0 is an observation; EVID=1 is a dose and EVID=3 a reset record.
    obs = raw[(raw.EVID == 0) & (raw.MDV == 0)].copy()
    # Every observation in this file is the bacterial compartment, but assert
    # it rather than assume it: a future revision could add drug assays.
    obs = obs[obs.CMT == 4].copy()
    if obs.empty:
        return empty()

    organism = ""
    model = d / "model.txt"
    if model.exists():
        head = model.read_text(errors="replace")
        if "Acinetobacter baumannii" in head:
            organism = "Acinetobacter baumannii"

    rows = []
    for r in obs.itertuples(index=False):
        mero_on = bool(r.MEROPENEM)
        col_on = bool(r.COLPMB)
        # COLPMB is the union of the COLISTIN and POLYMYXINB flags; they are
        # never both set, so the polymyxin can always be named.
        pmx = "colistin" if r.COLISTIN else ("polymyxin B" if r.POLYMYXINB
                                             else "")

        mero_static = bool(r.SRC_MERO)
        col_static = bool(r.SRC_COL)

        parts, drug, conc = [], "", np.nan
        if mero_on:
            if mero_static:
                parts.append(f"meropenem {_fmt(r.CSET_MERO)}")
            else:
                parts.append("meropenem (dynamic)")
        if col_on:
            name = pmx or "colistin/polymyxin B"
            if col_static:
                parts.append(f"{name} {_fmt(r.CSET_COL)}")
            else:
                parts.append(f"{name} (dynamic)")

        if not mero_on and not col_on:
            arm = "growth control"
        else:
            arm = " + ".join(parts)

        if mero_on and not col_on:
            drug = "meropenem"
            if mero_static:
                conc = float(r.CSET_MERO)
        elif col_on and not mero_on:
            drug = pmx or "colistin/polymyxin B"
            if col_static:
                conc = float(r.CSET_COL)
        elif mero_on and col_on:
            drug = f"meropenem + {pmx}" if pmx else "meropenem + colistin/polymyxin B"
            # two concentrations, one column: neither goes in, both are in arm.

        note = [
            TIME_NOTE, SCALE_NOTE,
            f"NONMEM ID={r.ID} OCC={r.OCC}",
            f"nominal inoculum INOC_TH = 1e{r.INOC_TH} (model A_0(4)=10**INOC), "
            "a target not a measurement",
            f"MIC_meropenem={_fmt(r.MIC_meropenem)} "
            f"MIC_colpmb={_fmt(r.MIC_colpmb)} (unit not stated)",
            "concentration unit not stated by the deposit",
        ]
        if (mero_on and not mero_static) or (col_on and not col_static):
            note.append("dynamic regimen: drug dosed via AMT/RATE/ADDL/II, "
                        "concentration varies over the curve")
        if mero_on and col_on:
            note.append("combination arm: two concentrations, so the single "
                        "concentration column is left blank")
        if r.anyacqbl:
            note.append("anyacqbl=1 in the deposit (acquired beta-lactamase "
                        "covariate); the deposit does not define it further")
        floor = float(r.LOD)
        if r.BLOD == 1:
            note.append("depositor flagged this reading BLOD=1")
        elif r.DV <= np.log10(floor):
            note.append("depositor's BLOD flag is 0 although DV is at or below "
                        "log10(LOD); flag and value disagree in the source")

        rows.append({
            "source_file": "data.csv",
            "sheet": "",
            "organism": organism,
            "strain": "",
            "drug": drug,
            "concentration": conc,
            "conc_unit": "",
            "arm": arm,
            "replicate": f"ID{int(r.ID)}_OCC{int(r.OCC)}",
            "tech_replicate": "",
            "time_h": float(r.TIME),
            "cfu_per_ml": float(10.0 ** r.DV),
            "floor_cfu_per_ml": floor,
            "floor_basis": ("LOD column of the deposited NONMEM dataset; "
                            "model.txt $ERROR uses LOQ=LOG10(LOD) as the M3 "
                            "censoring limit on the same log10 bacterial "
                            "density DV reports"),
            "readout": "CFU",
            "notes": "; ".join(note),
        })

    return pd.DataFrame(rows)
