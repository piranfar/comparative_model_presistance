"""
Table 1 of the preprint, machine-readable, with the OCR column offset resolved.

The published Table 1 has its label column offset by one row relative to its
value columns.  Reading the values in printed order and re-attaching the labels
gives the mapping below, which is the only assignment consistent with the
Abstract, Results 3.3 and Discussion 4.1/4.2:

    row 1  0.03  / 0.5    -> growth rate r
    row 2  0.002 / 0.01   -> resistance killing rate k_R
    row 3  0.05  / 0.2    -> tolerance killing rate k_T
    row 4  0.1   / 0.5    -> fast killing rate k_fast
    row 5  0.001 / 0.01   -> slow killing rate k_slow
    row 6  1-5%  / 0.01-0.1% -> dormant fraction f

PROVENANCE.  Every value below is class (b): adopted from the literature
without a traceable extraction.  None is a class (a) measurement tied to a
named dataset, figure panel and digitisation record.  `provenance` records this
explicitly so no downstream script can present these as fitted quantities.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass(frozen=True)
class SpeciesParams:
    """Parameters for one species, exactly as printed in Table 1."""

    name: str
    short: str
    r: float                 # intrinsic growth rate, 1/h
    k_R: float               # "resistance killing rate", 1/h
    k_T: float               # "tolerance killing rate", 1/h
    k_fast: float            # fast-phase killing rate, 1/h
    k_slow: float            # slow-phase killing rate, 1/h
    f_dormant_low: float     # dormant fraction, lower bound (dimensionless)
    f_dormant_high: float    # dormant fraction, upper bound (dimensionless)
    f_dormant_point: float   # value used in the paper's figures/Discussion
    t_c_asserted: float      # transition time asserted in Results 3.3, h
    N0: float = 1.0e6        # inoculum, CFU/mL (Methods do not state one)
    K: float = 1.0e9         # carrying capacity, CFU/mL (Eq. 1 only)
    doubling_time_h: float = 0.0
    provenance: str = "class (b): literature-adopted, not extracted"

    def as_dict(self) -> dict:
        return asdict(self)


MTB = SpeciesParams(
    name="Mycobacterium tuberculosis",
    short="Mtb",
    r=0.03,
    k_R=0.002,
    k_T=0.05,
    k_fast=0.1,
    k_slow=0.001,
    f_dormant_low=0.01,
    f_dormant_high=0.05,
    f_dormant_point=0.0358,   # the "~3.58%" of Discussion 4.2
    t_c_asserted=80.0,
    doubling_time_h=23.1,
)

SAUREUS = SpeciesParams(
    name="Staphylococcus aureus",
    short="S. aureus",
    r=0.5,
    k_R=0.01,
    k_T=0.2,
    k_fast=0.5,
    k_slow=0.01,
    f_dormant_low=0.0001,
    f_dormant_high=0.001,
    f_dormant_point=0.0005,
    t_c_asserted=12.0,
    doubling_time_h=1.39,
)

SPECIES = {"Mtb": MTB, "S. aureus": SAUREUS}

# Simulation grid declared in Methods 2.3.1: 240 h, dt = 1 h.
T_MAX_H = 240.0
DT_H = 1.0
DT_EULER_H = 0.5

# Limit of detection.  Not stated in the paper; 1e2 CFU/mL is the value used by
# the hollow-fibre studies in data/manifests/datasets.csv (TSUJI2012).
LOD_CFU_ML = 1.0e2
