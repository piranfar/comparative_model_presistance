"""
CT-BP: how long after the plate goes blank is the culture actually sterile?

Run:  python -m src.experiments.exp24_clearance_prediction [--quick]

WHY THIS TEST EXISTS. Every clinical microbiologist knows that a negative
culture taken under antibiotic is not proof of sterility. Nobody has written
down how long that gap is, or - more to the point - how often it is not a gap at
all but a permanent shortfall. This script builds the smallest model that can
say something defensible about both endpoints at once and, crucially, keep them
apart:

    T_LOD  the time at which a plate of a stated geometry reads blank. Observable,
           and here modelled as what it physically is: the plate received zero
           colonies, a Poisson event at rate 10**mu * v/1000, not a deterministic
           crossing of a threshold.
    T_ext  the time at which the expected number of survivors in the WHOLE culture
           falls below one. Not observable anywhere in this corpus, and this
           script is written to make that impossible to forget.

THE DECOMPOSITION THE WHOLE THING RESTS ON. On a terminal-linear trajectory,

    Delta = T_ext - T_LOD = H / b_tail,      H = L + log10(V_mL)

H is the HIDDEN BURDEN in log10 cells: how many living cells are still in the
flask at the instant the plate goes blank. It is exact arithmetic - assay
geometry plus vessel volume, no biology, no fitting, no extrapolation. Only the
denominator b_tail, the terminal decline rate, is inferred. A reader can see
which half of the answer is bookkeeping and which half is inference, and the
bookkeeping half is a number nobody has published.

WHY THE SLOPE IS SIGN FREE, WHICH IS THE DESIGN DECISION THAT MATTERS. In the
ERA4TB treated 100 uL series the terminal decline rate is NON-POSITIVE in most
flasks: the population is rising when observation stops. A model class that
requires a negative terminal rate - any Emax/Regoes form, any dying-persister
compartment - has to route three-quarters of the treated corpus through an
exception branch. Here b is an ordinary fitted value with no positivity
constraint and no log link, growth included, and

    P(T_ext = infinity) = P(b_tail <= 0)

is the FIRST number in every table rather than a footnote. Delta then has
infinite mean and undefined variance, so it is reported as conditional quantiles
only, and never as a mean.

WHAT THIS SCRIPT REFUSES TO DO. It does not claim T_ext was measured. Nothing in
this corpus was ever observed within two logs of extinction - the deepest
uncensored absolute reading anywhere is 1.000 log10 CFU/mL, against the -1.0
needed for one cell in 10 mL - and no deposit contains a single reading below
its own limit, so the sub-limit trajectory is unfalsifiable here by
construction. No deposit records a culture volume either, so V is a declared
scenario grid, never a datum. Every T_ext number is a consequence of stated
assumptions, printed beside its extrapolation depth and bracketed by three
terminal-behaviour variants that are never averaged.

WRITES
  results/tables/ctbp_hidden_burden.csv          exact, fit-free, written first
  results/tables/ctbp_gap_by_condition.csv       the main table
  results/tables/ctbp_tlod_calibration.csv       the validated endpoint
  results/tables/ctbp_two_timescale.csv          early vs terminal rate
  results/tables/ctbp_tipping_points.csv         the falsifiable inversion
  results/tables/ctbp_variance_components.csv    priors for future work
  results/tables/ctbp_identifiability_boundary.csv  the pre-fit gate
  results/tables/ctbp_validation_summary.csv     V1..V7
  results/receipts/exp24_receipt.json
  data/manifests/ctbp_external_assumptions.json  (written if absent; V is null)
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import optimize, stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.models.ct_bp import (  # noqa: E402
    GH_NODES,
    GH_WEIGHTS,
    LN10,
    gap,
    hidden_burden,
    limit_log10_from_volume,
    p_blank,
    required_b_tail_log10_per_day,
    sterility_offset_days,
    volume_from_limit_log10,
)

PROC = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"
MANIFESTS = ROOT / "data" / "manifests"
MANIFEST_PATH = MANIFESTS / "ctbp_external_assumptions.json"

SEED = 20260905
MAXSEG = 4

# ---------------------------------------------------------------------------
# Deposit-specific knots. The observation grids span three orders of magnitude
# in time and cannot share a basis, so nothing here is shared across deposits
# except the hyper-variances.
KNOTS = {
    "era4tb": np.array([0.0, 2.0, 7.0, 14.0, 21.0]),
    "kaur_planktonic": np.array([0.0, 3.0, 7.0, 14.0]),
    "kaur_intracellular": np.array([0.0, 3.0, 7.0]),
    "vijay": np.array([0.0, 2.0, 5.0]),
    "windels": np.array([0.0, 1.0 / 24.0, 3.0 / 24.0, 8.0 / 24.0]),
}
DEPOSIT_OF_BLOCK = {
    "era4tb": "era4tb",
    "kaur_planktonic": "kaur",
    "kaur_intracellular": "kaur",
    "vijay": "vijay",
    "windels": "windels",
}
DEPOSITS = ["era4tb", "kaur", "vijay", "windels"]

# The Windels assay is 8 hours long; every other deposit runs for days or weeks.
# A prior on log10 per day that is weakly informative for a 21-day mycobacterial
# time-kill is roughly 300 prior standard deviations away from an aminoglycoside
# killing 6 logs in an hour. Rather than silently fight the data, the prior scale
# is declared per deposit. 24 is exactly "the same prior, per hour".
RATE_PRIOR_SCALE = {"era4tb": 1.0, "kaur": 1.0, "vijay": 1.0, "windels": 24.0}

# Named exclusions, per the build contract. These are excluded BY NAME and
# counted; nothing is imputed to keep them.
ERA4TB_NO_N0 = [
    "era4tb_A_MXF10x_r1",
    "era4tb_A_untreated_r3",
    "era4tb_B_INH10x_r1",
    "era4tb_B_INH1x_r2",
    "era4tb_B_INH1x_r3",
    "era4tb_B_MXF1x_r2",
    "era4tb_E_untreated_r2",
    "era4tb_E_untreated_r3",
]

V_GRID_ML = [1.0, 10.0, 100.0, 1000.0]
VOL_GRID_UL = [100.0, 10.0, 2.5]
GAP_TARGETS_DAYS = [7, 14, 30, 60, 90]
DEEPEST_UNCENSORED_ABSOLUTE_LOG10 = 1.000  # ERA4TB 100 uL quad; the corpus floor

# V1 pre-registered failure criterion, fixed here before any fitting.
V1_COVERAGE_BAND = (0.80, 0.97)
V1_BLANK_RATE_FOLD = 1.5


# ===========================================================================
# 0. MANIFEST OF DECLARED EXTERNAL ASSUMPTIONS
# ===========================================================================
def ensure_manifest() -> dict:
    """The culture volume is in no deposit. This file says so, in writing.

    There is deliberately no default V anywhere in this code. Every V that
    appears in a table comes from the scenario grid below and is labelled as a
    scenario, not as a datum.
    """
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    man = {
        "purpose": "Declared external assumptions for CT-BP. Anything null here is "
                   "genuinely absent from the deposit and must not be filled in.",
        "culture_volume_mL": {
            "era4tb": None,
            "kaur": None,
            "vijay": None,
            "windels": None,
        },
        "culture_volume_provenance": {
            "era4tb": "ABSENT - the deposit's Volume column is PLATED volume only",
            "kaur": "ABSENT - the workbook records no vessel volume",
            "vijay": "ABSENT - MPN is reported per mL; no vessel volume anywhere",
            "windels": "ABSENT - no absolute density at all, let alone a volume",
        },
        "scenario_grid_V_mL": V_GRID_ML,
        "scenario_grid_provenance": "SCENARIO ONLY. These are hypothetical vessel "
                                    "volumes used to print Delta as a surface. They "
                                    "are not measurements and no deposit supports any "
                                    "of them.",
        "kaur_sensitivity_floor_log10_cfu_per_mL": 1.60,
        "kaur_sensitivity_floor_provenance": (
            "NOT A DATUM AND NOT FROM THE PAPER'S METHODS. This value is an "
            "INFERENCE from the deposit itself: of the 24 rows below 3 log10, 15 "
            "back-transform to exact multiples of 10 CFU/mL with a minimum of "
            "exactly 40, the pattern of plate counts times 10, i.e. 100 uL plated. "
            "It is used ONLY in the V5 sensitivity arm and never in the primary "
            "fit. The methods text was not available to this run."
        ),
        "windels_sensitivity_bound_log10_surv_frac": -8.152,
        "windels_sensitivity_bound_provenance": (
            "An UPPER BOUND on the limit, not the limit: the lowest non-zero "
            "surviving fraction anywhere in timekill.csv is 7.04e-09. The true "
            "floor lies at or below it. Used only in the V5 sensitivity arm."
        ),
        "windels_time_unit": "hours (external to the deposit; from the source paper "
                             "and this repo's exp13/exp14)",
        "windels_drug": "amikacin (external to the deposit; no drug column exists)",
        "windels_ancestral_MIC_ug_per_mL": 2.0,
    }
    MANIFEST_PATH.write_text(json.dumps(man, indent=2), encoding="utf-8")
    return man


# ===========================================================================
# 1. BUILD DESIGN
# ===========================================================================
class BuildLog(dict):
    def add(self, key, value):
        self[key] = value


def _era4tb(log: BuildLog) -> pd.DataFrame:
    d = pd.read_csv(PROC / "tidy_era4tb.csv")
    log.add("era4tb_rows_in_tidy_file", int(len(d)))
    d["plated_volume_uL"] = d["notes"].str.extract(r"plated_volume_uL=([\d.]+)")[0].astype(float)
    # Assertion: the recorded volume and the recorded limit must agree exactly.
    ok = d["plated_volume_uL"].notna() & d["limit_log10"].notna()
    resid = np.abs(limit_log10_from_volume(d.loc[ok, "plated_volume_uL"]) - d.loc[ok, "limit_log10"])
    assert float(resid.max()) < 1e-9, "plated volume and limit_log10 disagree"
    back = np.asarray(volume_from_limit_log10(d.loc[ok, "limit_log10"]))
    assert np.all(np.min(np.abs(back[:, None] - np.array([100.0, 50.0, 10.0, 2.5])), axis=1) < 1e-9)

    d["lab"] = d["unit_group"].str.split("_").str[1]
    d["arm"] = d["unit_group"].str.split("_").str[2]
    d["bql_contradicted"] = d["notes"].str.contains("bql_contradicted_by", na=False)
    n0src = d["notes"].str.extract(r"n0_source_days=([\d,]+)")[0]
    d["post_drug_baseline"] = (n0src == "1") & (d["arm"] != "untreated")
    d["untreated_censored"] = d["censored"] & (d["arm"] == "untreated")

    log.add("era4tb_bql_flags_total", int(d["censored"].sum()))
    log.add("era4tb_bql_flags_contradicted", int((d["censored"] & d["bql_contradicted"]).sum()))
    log.add("era4tb_censored_rows_in_untreated_flasks", int(d["untreated_censored"].sum()))
    log.add("era4tb_no_value_reported_not_censored",
            int(d["notes"].str.contains("no_value_reported_not_censored", na=False).sum()))
    log.add("era4tb_unit_groups_with_n0_from_day1_only", int(
        d.loc[n0src == "1", "unit_group"].nunique()))
    log.add("era4tb_post_drug_baseline_flasks", int(
        d.loc[d["post_drug_baseline"], "unit_group"].nunique()))
    log.add("era4tb_post_drug_baseline_definition",
            "n0_source_days == 1 AND the arm is treated. A day-1 reading in an "
            "UNDRUGGED flask is a genuine density, not one day of killing, so the "
            "untreated day-1-only flasks are counted separately above rather than "
            "labelled post-drug.")

    n_pre = int((d["time_days"] < 0).sum())
    n_50uL = int((d["plated_volume_uL"] == 50.0).sum())
    n_novol = int(d["plated_volume_uL"].isna().sum())
    d = d[(d["time_days"] >= 0) & (d["plated_volume_uL"].isin([100.0, 10.0, 2.5]))]
    log.add("era4tb_excluded_pre_inoculation_rows", n_pre)
    log.add("era4tb_excluded_50uL_rows_volume_disagrees_with_comment", n_50uL)
    log.add("era4tb_excluded_rows_with_no_plating_volume", n_novol)

    d = d[d["y_log10"].notna() | d["censored"]]
    excl_inoc = sorted(d.loc[d["arm"] == "inoculumTKA", "unit_group"].unique())
    d = d[d["arm"] != "inoculumTKA"]
    log.add("era4tb_excluded_inoculumTKA_series_single_visit_after_day0", excl_inoc)
    present = set(d["unit_group"])
    d = d[~d["unit_group"].isin(ERA4TB_NO_N0)]
    log.add("era4tb_excluded_unit_groups_no_usable_n0",
            sorted([u for u in ERA4TB_NO_N0 if u in present]))

    d["block"] = "era4tb"
    d["deposit"] = "era4tb"
    d["state_label"] = "standard"
    d["scale_tag"] = "absolute_cfu_per_ml"
    d["sample_visit"] = d["unit_group"] + "@" + d["time_days"].astype(str)
    log.add("era4tb_rows_used", int(len(d)))
    log.add("era4tb_series_used", int(d["unit_group"].nunique()))
    return d


def _kaur(log: BuildLog, add_baseline_anchor: bool = True) -> pd.DataFrame:
    d = pd.read_csv(PROC / "tidy_kaur.csv")
    log.add("kaur_rows_in_tidy_file", int(len(d)))
    n_bio = int((d["state"] == "biofilm").sum())
    d = d[d["state"] != "biofilm"].copy()
    log.add("kaur_excluded_biofilm_rows_no_time_axis", n_bio)
    assert d["censored"].sum() == 0 and d["limit_log10"].isna().all(), \
        "Kaur must carry no censoring and no limit; none is stated in the deposit"

    rows = [d]
    if add_baseline_anchor:
        # The deposit gives ONE day-0 baseline per sheet, shared by every arm, and
        # the extractor assigned it to arms by replicate column index. Without it a
        # treated series has no t=0 anchor at all. It is added here as an explicit,
        # flagged t=0 observation and the receipt counts it; V5 refits without it.
        anchors = []
        for ug, g in d[d["drug"] != "none"].groupby("unit_group"):
            r = g.iloc[0].copy()
            if 0.0 in set(g["time_days"]):
                continue
            r["time_days"] = 0.0
            r["y_log10"] = r["n0_log10"]
            r["notes"] = "kaur_baseline_anchor_row_added_by_exp24; " + str(r["notes"])
            anchors.append(r)
        if anchors:
            rows.append(pd.DataFrame(anchors))
        log.add("kaur_baseline_anchor_rows_added", int(len(anchors)))
    d = pd.concat(rows, ignore_index=True)
    d["block"] = np.where(d["state"] == "planktonic", "kaur_planktonic", "kaur_intracellular")
    d["deposit"] = "kaur"
    d["state_label"] = d["state"]
    d["scale_tag"] = "absolute_cfu_per_ml"
    d["plated_volume_uL"] = np.nan
    d["sample_visit"] = ""
    log.add("kaur_rows_used", int(len(d)))
    log.add("kaur_series_used", int(d["unit_group"].nunique()))
    return d


def _vijay(log: BuildLog) -> pd.DataFrame:
    d = pd.read_csv(PROC / "tidy_vijay.csv")
    log.add("vijay_rows_in_tidy_file", int(len(d)))
    log.add("vijay_readings_absent_and_not_emitted_by_extractor", 21)
    rungs = np.sort(d["mpn_raw"].dropna().unique())
    grungs = np.log10(rungs)
    log.add("vijay_distinct_mpn_rungs", int(len(rungs)))
    floor = float(grungs[0])
    assert abs(floor - np.log10(23.0)) < 1e-12
    mids = (grungs[:-1] + grungs[1:]) / 2.0
    # The outer edges are +/- 30 log10, not +/- inf. That is not a modelling
    # choice - 30 log10 is unreachable by any culture - it is because the
    # derivative of an interval whose edge is literally infinite is 0 * inf,
    # which is NaN, and the sampler refuses to start.
    lo = np.concatenate([[-30.0], mids])
    hi = np.concatenate([mids, [30.0]])
    idx = np.searchsorted(grungs, np.log10(d["mpn_raw"].values))
    d["bin_lo"] = lo[idx]
    d["bin_hi"] = hi[idx]
    # The floor rung is LEFT-censored at log10(23) exactly.
    d.loc[d["censored"], "bin_lo"] = -30.0
    d.loc[d["censored"], "bin_hi"] = floor
    d["block"] = "vijay"
    d["deposit"] = "vijay"
    d["state_label"] = d["state"]
    d["scale_tag"] = "absolute_mpn_per_ml"
    d["plated_volume_uL"] = np.nan
    d["sample_visit"] = ""
    log.add("vijay_floor_readings_left_censored_at_log10_23", int(d["censored"].sum()))
    log.add("vijay_rows_used", int(len(d)))
    log.add("vijay_series_used", int(d["unit_group"].nunique()))
    return d


def _windels(log: BuildLog, censor_zeros: bool = False) -> pd.DataFrame:
    d = pd.read_csv(PROC / "tidy_windels.csv")
    log.add("windels_rows_in_tidy_file", int(len(d)))
    n_zero = int(d["censored"].sum())
    if censor_zeros:
        d["bin_hi"] = np.where(d["censored"], -8.152, np.nan)
        log.add("windels_zero_surv_frac_rows_censored_at_declared_bound", n_zero)
    else:
        d = d[~d["censored"]].copy()
        log.add("windels_zero_surv_frac_rows_excluded_no_derivable_limit", n_zero)
    # A series with a single time point carries no kill information at all.
    n_per = d.groupby("unit_group")["time_days"].nunique()
    drop = sorted(n_per[n_per < 2].index)
    d = d[~d["unit_group"].isin(drop)]
    log.add("windels_excluded_series_single_timepoint", drop)
    d["block"] = "windels"
    d["deposit"] = "windels"
    d["state_label"] = "nutrient_" + d["state_numeric"].astype(str)
    d["scale_tag"] = "relative_fraction"
    d["plated_volume_uL"] = np.nan
    d["sample_visit"] = ""
    log.add("windels_rows_used", int(len(d)))
    log.add("windels_series_used", int(d["unit_group"].nunique()))
    return d


DESIGN_COLUMNS = [
    "e_int", "e_untreated", "e_mxf", "e_logdose_c", "e_n0_c", "e_n0_is_postdrug",
    "k_int", "k_intracellular", "k_untreated", "k_amikacin", "k_rifampicin", "k_logdose_c",
    "v_int", "v_age_c", "v_n0_c",
    "w_int", "w_state_c", "w_logdose_c", "w_state_x_logdose",
]


def build_design(add_kaur_anchor=True, windels_censor_zeros=False, kaur_floor=None,
                 bql_arm="censored", drop_labs=(), drop_volumes=(), drop_windels_cells=(),
                 drop_vijay_states=(), vijay_left_censor_only=False, deposits=None):
    """Assemble every plating reading as its own row, with hard assertions.

    Nothing is collapsed to a per-visit mean, nothing is imputed, and absence is
    never conflated with censoring.
    """
    log = BuildLog()
    parts = [_era4tb(log), _kaur(log, add_kaur_anchor), _vijay(log),
             _windels(log, windels_censor_zeros)]
    d = pd.concat(parts, ignore_index=True)

    # --- BQL sensitivity arms -------------------------------------------------
    era = d["deposit"] == "era4tb"
    if bql_arm == "censored":
        pass
    elif bql_arm == "reclassified":
        m = era & d["censored"] & d["bql_contradicted"].fillna(False)
        d.loc[m, "censored"] = False           # now missing, not censored
        d.loc[m, "y_log10"] = np.nan
        log.add("bql_arm_reclassified_rows", int(m.sum()))
    elif bql_arm == "dropped":
        m = era & d["censored"]
        d = d[~m]
        log.add("bql_arm_dropped_rows", int(m.sum()))
        era = d["deposit"] == "era4tb"
    else:
        raise ValueError(bql_arm)

    # --- Kaur declared-external floor sensitivity ----------------------------
    if kaur_floor is not None:
        m = (d["deposit"] == "kaur") & (d["y_log10"] <= kaur_floor)
        d.loc[m, "censored"] = True
        d.loc[m, "limit_log10"] = kaur_floor
        d.loc[m, "y_log10"] = np.nan
        log.add("kaur_rows_censored_at_declared_external_floor", int(m.sum()))

    # --- Vijay censoring-mechanism sensitivity ------------------------------
    if vijay_left_censor_only:
        m = (d["deposit"] == "vijay") & (~d["censored"])
        d.loc[m, "bin_lo"] = np.nan   # point likelihood instead of interval
        d.loc[m, "bin_hi"] = np.nan
        log.add("vijay_treated_as_point_plus_left_censoring", int(m.sum()))

    # --- holdout splits ------------------------------------------------------
    if drop_labs:
        d = d[~((d["deposit"] == "era4tb") & (d["lab"].isin(drop_labs)))]
    if drop_volumes:
        d = d[~((d["deposit"] == "era4tb") & (d["plated_volume_uL"].isin(drop_volumes)))]
    if drop_windels_cells:
        key = list(zip(d["state_numeric"].fillna(-1), d["dose_value"].fillna(-1)))
        keep = [not (dep == "windels" and k in drop_windels_cells)
                for dep, k in zip(d["deposit"], key)]
        d = d[np.array(keep)]
    if drop_vijay_states:
        d = d[~((d["deposit"] == "vijay") & (d["state_label"].isin(drop_vijay_states)))]
    if deposits is not None:
        d = d[d["deposit"].isin(list(deposits))]
        log.add("deposits_in_this_fit", list(deposits))

    d = d[d["y_log10"].notna() | d["censored"] | d["bin_lo"].notna()].copy()
    d = d.reset_index(drop=True)

    # --- HARD ASSERTIONS -----------------------------------------------------
    assert not ((d["censored"]) & (d["y_log10"].notna())).any(), \
        "a row is both censored and quantitative"
    assert d.loc[d["scale_tag"] == "relative_fraction", "n0_log10"].isna().all(), \
        "a relative-fraction row carries an n0"
    assert not d["unit_group"].isin(ERA4TB_NO_N0).any(), "an excluded unit_group survived"

    # --- series table --------------------------------------------------------
    ser = (d.groupby("unit_group")
             .agg(block=("block", "first"), deposit=("deposit", "first"),
                  drug=("drug", "first"), dose_value=("dose_value", "first"),
                  dose_unit=("dose_unit", "first"), state_label=("state_label", "first"),
                  state_numeric=("state_numeric", "first"), n0_log10=("n0_log10", "first"),
                  scale_tag=("scale_tag", "first"),
                  lab=("lab", "first") if "lab" in d else ("block", "first"),
                  arm=("arm", "first") if "arm" in d else ("block", "first"),
                  post_drug_baseline=("post_drug_baseline", "max")
                  if "post_drug_baseline" in d else ("block", "first"),
                  isolate_index=("isolate_index", "first")
                  if "isolate_index" in d else ("block", "first"),
                  t_first=("time_days", "min"), t_last=("time_days", "max"),
                  n_rows=("time_days", "size"), n_visits=("time_days", "nunique"))
             .reset_index())
    ser["post_drug_baseline"] = ser["post_drug_baseline"].fillna(False).astype(bool) \
        if ser["post_drug_baseline"].dtype != object else False
    ser["nseg_full"] = ser["block"].map(lambda b: len(KNOTS[b]) - 1)
    ser["sidx"] = np.arange(len(ser))
    sidx = dict(zip(ser["unit_group"], ser["sidx"]))
    d["sidx"] = d["unit_group"].map(sidx).astype(int)

    # --- design matrix, deposit-specific coding, never a shared numeric axis --
    X = pd.DataFrame(0.0, index=ser.index, columns=DESIGN_COLUMNS)
    is_e = ser["deposit"] == "era4tb"
    X.loc[is_e, "e_int"] = 1.0
    X.loc[is_e & (ser["drug"] == "none"), "e_untreated"] = 1.0
    X.loc[is_e & (ser["drug"] == "moxifloxacin"), "e_mxf"] = 1.0
    ld = np.where(is_e & (ser["dose_value"] > 0),
                  np.log10(ser["dose_value"].where(ser["dose_value"] > 0, 1.0)), 0.0)
    tr = (is_e & (ser["dose_value"] > 0)).values
    if tr.any():
        X.loc[tr, "e_logdose_c"] = ld[tr] - ld[tr].mean()
    genuine_n0 = (is_e & ~ser["post_drug_baseline"].astype(bool)).values
    n0 = ser["n0_log10"].values
    if genuine_n0.any():
        X.loc[genuine_n0, "e_n0_c"] = n0[genuine_n0] - np.nanmean(n0[genuine_n0])
    X.loc[is_e.values & ser["post_drug_baseline"].astype(bool).values, "e_n0_is_postdrug"] = 1.0

    is_k = ser["deposit"] == "kaur"
    X.loc[is_k, "k_int"] = 1.0
    X.loc[is_k & (ser["state_label"] == "intracellular"), "k_intracellular"] = 1.0
    X.loc[is_k & (ser["drug"] == "none"), "k_untreated"] = 1.0
    X.loc[is_k & (ser["drug"] == "amikacin"), "k_amikacin"] = 1.0
    X.loc[is_k & (ser["drug"] == "rifampicin"), "k_rifampicin"] = 1.0
    kd = (is_k & (ser["dose_value"] > 0)).values
    lk = np.zeros(len(ser))
    if kd.any():
        lk[kd] = np.log10(ser["dose_value"].values[kd])
        X.loc[kd, "k_logdose_c"] = lk[kd] - lk[kd].mean()

    is_v = ser["deposit"] == "vijay"
    if is_v.any():
        X.loc[is_v, "v_int"] = 1.0
        X.loc[is_v, "v_age_c"] = (ser.loc[is_v, "state_numeric"] - 35.0) / 30.0
        X.loc[is_v, "v_n0_c"] = (ser.loc[is_v, "n0_log10"]
                                 - ser.loc[is_v, "n0_log10"].mean())

    is_w = ser["deposit"] == "windels"
    if is_w.any():
        X.loc[is_w, "w_int"] = 1.0
        sc = ser.loc[is_w, "state_numeric"] - ser.loc[is_w, "state_numeric"].mean()
        lw = np.log10(ser.loc[is_w, "dose_value"])
        lwc = lw - lw.mean()
        X.loc[is_w, "w_state_c"] = sc
        X.loc[is_w, "w_logdose_c"] = lwc
        X.loc[is_w, "w_state_x_logdose"] = sc * lwc

    # --- per-row segment-elapsed design -------------------------------------
    W = np.zeros((len(d), MAXSEG))
    for b, k in KNOTS.items():
        m = (d["block"] == b).values
        if not m.any():
            continue
        lo, hi = k[:-1], k[1:].copy()
        hi[-1] = np.inf
        t = d.loc[m, "time_days"].values[:, None]
        W[np.ix_(m, np.arange(len(lo)))] = np.clip(t - lo, 0.0, hi - lo)

    # --- truncate each series at its last INFORMATIVE segment ---------------
    # Lab B stops at day 14 and lab F at day 15, so the deposit-level segment
    # [14, 21] contains no reading at all for most of ERA4TB. A rate fitted
    # there would be the random-walk prior wearing the name b_tail, and the
    # entire T_ext claim rests on that one scalar. Each series' terminal segment
    # is therefore the last one that actually contains an observation; segments
    # beyond it carry no parameter and the extrapolation starts from the last
    # knot the data reached.
    last_seg = np.zeros(len(ser), dtype=int)
    for r in range(len(d)):
        i = int(d["sidx"].iloc[r])
        nz = np.nonzero(W[r] > 0)[0]
        if nz.size:
            last_seg[i] = max(last_seg[i], int(nz[-1]))
    ser["nseg"] = np.minimum(last_seg + 1, ser["nseg_full"].values)
    ser["last_knot_day"] = [KNOTS[b][n] for b, n in zip(ser["block"], ser["nseg"])]
    log.add("series_with_terminal_segment_truncated",
            int((ser["nseg"] < ser["nseg_full"]).sum()))
    log.add("terminal_segment_truncation_by_block",
            {b: int((g["nseg"] < g["nseg_full"]).sum())
             for b, g in ser.groupby("block")})
    # zero out design weight in segments a series does not reach
    for r in range(len(d)):
        i = int(d["sidx"].iloc[r])
        W[r, int(ser["nseg"].iloc[i]):] = 0.0

    # --- index maps ----------------------------------------------------------
    labs = sorted(ser.loc[is_e, "lab"].dropna().unique())
    lab_idx = np.array([labs.index(l) if isinstance(l, str) and l in labs else -1
                        for l in ser["lab"]], dtype=int)
    isos = sorted(pd.to_numeric(ser.loc[is_v, "isolate_index"], errors="coerce").dropna().unique())
    iso_map = {v: i for i, v in enumerate(isos)}
    iso_idx = np.array([iso_map.get(v, -1) for v in
                        pd.to_numeric(ser["isolate_index"], errors="coerce")], dtype=int)

    dep_idx = np.array([DEPOSITS.index(x) for x in ser["deposit"]], dtype=int)
    visits = sorted(d.loc[d["deposit"] == "era4tb", "sample_visit"].unique())
    vmap = {v: i for i, v in enumerate(visits)}
    visit_idx = np.array([vmap.get(v, -1) for v in d["sample_visit"]], dtype=int)

    log.add("n_series", int(len(ser)))
    log.add("n_rows", int(len(d)))
    log.add("n_era4tb_sample_visits", int(len(visits)))
    log.add("n_labs", len(labs))
    log.add("n_vijay_isolates", len(isos))
    log.add("LN10", LN10)
    log.add("rate_units_everywhere", "log10 per day")

    return dict(rows=d, ser=ser, X=X.values.astype(float), Xcols=DESIGN_COLUMNS, W=W,
                dep_idx=dep_idx, lab_idx=lab_idx, iso_idx=iso_idx, labs=labs,
                visit_idx=visit_idx, n_visits=len(visits), visit_keys=visits,
                log=log,
                nseg=ser["nseg"].values.astype(int))


# ===========================================================================
# 2. THE NUMPYRO MODEL
# ===========================================================================
def _setup_numpyro(n_chains):
    import numpyro
    numpyro.set_host_device_count(n_chains)
    numpyro.enable_x64()
    return numpyro


def make_model_inputs(D):
    d, ser = D["rows"], D["ser"]
    dep = d["deposit"].values
    cen = d["censored"].fillna(False).values.astype(bool)

    e = dep == "era4tb"
    e_obs = e & ~cen
    e_cen = e & cen
    k_obs = (dep == "kaur") & ~cen
    k_cen = (dep == "kaur") & cen
    w_obs = (dep == "windels") & ~cen
    w_cen = (dep == "windels") & cen
    v = dep == "vijay"
    v_interval = v & d["bin_lo"].notna().values & np.isfinite(d["bin_lo"].fillna(-np.inf).values)
    v_left = v & d["censored"].fillna(False).values
    v_point = v & ~d["bin_lo"].notna().values & ~d["censored"].fillna(False).values

    out = dict(
        sidx=d["sidx"].values.astype(int),
        W=D["W"], X=D["X"], dep_idx=D["dep_idx"], lab_idx=D["lab_idx"],
        iso_idx=D["iso_idx"], visit_idx=D["visit_idx"], n_visits=D["n_visits"],
        nseg=D["nseg"], n_series=len(ser), n_labs=len(D["labs"]),
        n_iso=int(D["iso_idx"].max() + 1) if (D["iso_idx"] >= 0).any() else 0,
        is_windels_series=(ser["deposit"] == "windels").values,
        y=d["y_log10"].values.astype(float),
        vol=d["plated_volume_uL"].values.astype(float),
        lim=d["limit_log10"].values.astype(float),
        bin_lo=d["bin_lo"].fillna(-np.inf).values.astype(float) if "bin_lo" in d else None,
        bin_hi=d["bin_hi"].fillna(np.inf).values.astype(float) if "bin_hi" in d else None,
        m_e_obs=e_obs, m_e_cen=e_cen, m_k_obs=k_obs, m_k_cen=k_cen,
        m_w_obs=w_obs, m_w_cen=w_cen,
        m_v_int=v_interval & ~v_left, m_v_left=v_left, m_v_point=v_point,
    )
    return out


def ctbp_model(I):
    import jax.numpy as jnp
    import numpyro
    import numpyro.distributions as dist
    from jax.scipy.special import log_ndtr

    S, P = I["n_series"], I["X"].shape[1]
    dep_scale = jnp.array([RATE_PRIOR_SCALE[x] for x in DEPOSITS])[I["dep_idx"]]

    # column-wise prior scale: Windels columns get the per-hour scale
    col_scale = np.ones(P)
    col_sd = np.full(P, 0.5)
    for j, c in enumerate(DESIGN_COLUMNS):
        if c.startswith("w_"):
            col_scale[j] = RATE_PRIOR_SCALE["windels"]
        if c.endswith("_int"):
            col_sd[j] = 1.0
        if "_n0_" in c:
            col_sd[j] = 0.2          # explicitly weak; n0 is a designed variable nowhere
    beta = jnp.asarray(numpyro.sample(
        "beta", dist.Normal(0.0, jnp.array(col_sd * col_scale)[:, None]
                            * jnp.ones((P, MAXSEG)))))

    tau = jnp.asarray(numpyro.sample("tau_d", dist.HalfNormal(0.5 * jnp.array(
        [RATE_PRIOR_SCALE[x] for x in DEPOSITS]))))
    sigma_lab = numpyro.sample("sigma_lab", dist.HalfNormal(0.5))
    sigma_iso = numpyro.sample("sigma_iso", dist.HalfNormal(0.5))
    # ONE hyper-variance saying how much a rate moves, with a deposit-specific
    # scale. Sharing a single number across deposits whose timescales differ
    # 72-fold would not be pooling, it would be arithmetic on incommensurable
    # units; sharing the hyper-parameter is.
    sigma_rate_hyper = numpyro.sample("sigma_rate_hyper", dist.HalfNormal(0.5))
    sigma_series_d = jnp.asarray(numpyro.sample(
        "sigma_series_d", dist.HalfNormal(0.5).expand([len(DEPOSITS)]))) * sigma_rate_hyper         * jnp.array([RATE_PRIOR_SCALE[x] for x in DEPOSITS])
    sigma_series = numpyro.deterministic("sigma_series", sigma_series_d)

    u_lab = jnp.asarray(numpyro.sample(
        "u_lab", dist.Normal(0, 1).expand([max(I["n_labs"], 1)]))) * sigma_lab
    u_iso = jnp.asarray(numpyro.sample(
        "u_iso", dist.Normal(0, 1).expand([max(I["n_iso"], 1)]))) * sigma_iso
    w_ser = jnp.asarray(numpyro.sample(
        "w_series", dist.Normal(0, 1).expand([S]))) * sigma_series_d[I["dep_idx"]]

    # These index arrays stay NUMPY on purpose. Under init_to_value a sampled
    # site can come back as a plain numpy array, and numpy_array[jax_tracer]
    # tries to convert the tracer. Numpy indices work for both.
    lab_ok = I["lab_idx"] >= 0
    iso_ok = I["iso_idx"] >= 0
    li = np.clip(I["lab_idx"], 0, None)
    ii = np.clip(I["iso_idx"], 0, None)

    xb = jnp.asarray(I["X"]) @ beta                                    # (S, MAXSEG)
    base = xb[:, 0] + jnp.where(lab_ok, u_lab[li], 0.0) + jnp.where(iso_ok, u_iso[ii], 0.0) + w_ser
    z = jnp.asarray(numpyro.sample("z_rw", dist.Normal(0, 1).expand([S, MAXSEG - 1])))
    steps = jnp.cumsum(jnp.concatenate([jnp.zeros((S, 1)), z], axis=1), axis=1)
    b = base[:, None] + (xb - xb[:, :1]) + tau[I["dep_idx"]][:, None] * steps
    segmask = jnp.asarray((np.arange(MAXSEG)[None, :] < I["nseg"][:, None]).astype(float))
    b = numpyro.deterministic("b", b * segmask)

    # intercepts: flat for Windels (structurally invariant to its unknown N0)
    alpha = jnp.asarray(numpyro.sample("alpha_d", dist.Normal(6.0, 2.0).expand([len(DEPOSITS)])))
    sigma_a = jnp.asarray(numpyro.sample("sigma_a", dist.HalfNormal(2.0).expand([len(DEPOSITS)])))
    sigma_lab_a = numpyro.sample("sigma_lab_a", dist.HalfNormal(2.0))
    u_lab_a = jnp.asarray(numpyro.sample(
        "u_lab_a", dist.Normal(0, 1).expand([max(I["n_labs"], 1)]))) * sigma_lab_a
    za = jnp.asarray(numpyro.sample("z_a", dist.Normal(0, 1).expand([S])))
    a = alpha[I["dep_idx"]] + jnp.where(lab_ok, u_lab_a[li], 0.0) + sigma_a[I["dep_idx"]] * za
    # The flat intercept is sampled ONLY for the Windels series. Expanding it to
    # every series would leave one improper, perfectly flat coordinate per
    # non-Windels series: a posterior with no curvature at all in ~800
    # directions, which NUTS answers by running every trajectory to the maximum
    # tree depth. That is a correctness bug, not a tuning problem.
    w_idx = np.nonzero(I["is_windels_series"])[0]
    if w_idx.size:
        a_flat = jnp.asarray(numpyro.sample(
            "a_windels",
            dist.ImproperUniform(dist.constraints.real, (), ()).expand([len(w_idx)])))
        a = a.at[w_idx].set(a_flat)
    a = numpyro.deterministic("a", a)

    si = I["sidx"]
    mu = a[si] - jnp.sum(jnp.asarray(I["W"]) * b[si], axis=1)

    # InverseGamma, not HalfNormal, on the observation scales. A HalfNormal puts
    # its maximum density at zero, and the Vijay likelihood is an INTERVAL: the
    # maximum-likelihood sigma there is exactly zero, at which point the interval
    # term becomes a step function with unbounded curvature and the sampler
    # collapses. InverseGamma(3, 0.5) has median ~0.19, negligible mass at zero
    # and a heavy right tail, so it regularises without asserting a value.
    sigma_plate = numpyro.sample("sigma_plate", dist.InverseGamma(3.0, 0.5))
    sigma_proc = jnp.asarray(numpyro.sample(
        "sigma_proc_d", dist.InverseGamma(3.0, 0.5).expand([len(DEPOSITS)])))
    pi_e = numpyro.sample("pi_era4tb", dist.Beta(1.0, 4.0))

    # ERA4TB nests plate noise inside process noise: four platings of ONE sample
    # at ONE visit share a visit-level latent density, which is what identifies
    # sigma_plate directly rather than charging it to the biology.
    eta = jnp.asarray(numpyro.sample(
        "eta_visit", dist.Normal(0, 1).expand([max(I["n_visits"], 1)])))
    vi = np.clip(I["visit_idx"], 0, None)
    mu_e = mu + jnp.where(I["visit_idx"] >= 0, eta[vi] * sigma_proc[0], 0.0)

    y = jnp.asarray(np.nan_to_num(I["y"], nan=0.0))
    vol = jnp.asarray(np.nan_to_num(I["vol"], nan=100.0))

    def obs_normal(mask, mu_, sd, name):
        if int(mask.sum()) == 0:
            return
        idx = np.nonzero(mask)[0]
        numpyro.sample(name, dist.Normal(mu_[idx], sd), obs=y[idx])

    obs_normal(I["m_e_obs"], mu_e, sigma_plate, "y_era4tb")
    if I["m_e_obs"].sum():
        numpyro.factor("era4tb_notflagged", int(I["m_e_obs"].sum()) * jnp.log1p(-pi_e))
    if I["m_e_cen"].sum():
        idx = np.nonzero(I["m_e_cen"])[0]
        pb = _p_blank_jax(mu_e[idx], sigma_plate, vol[idx])
        numpyro.factor("era4tb_blank", jnp.sum(jnp.log(pi_e + (1 - pi_e) * pb + 1e-300)))

    obs_normal(I["m_k_obs"], mu, sigma_proc[1], "y_kaur")
    if I["m_k_cen"].sum():
        idx = np.nonzero(I["m_k_cen"])[0]
        lim = jnp.asarray(np.nan_to_num(I["lim"], nan=0.0))[idx]
        numpyro.factor("kaur_left", jnp.sum(log_ndtr((lim - mu[idx]) / sigma_proc[1])))

    obs_normal(I["m_w_obs"], mu, sigma_proc[3], "y_windels")
    if I["m_w_cen"].sum():
        idx = np.nonzero(I["m_w_cen"])[0]
        numpyro.factor("windels_left",
                       jnp.sum(log_ndtr((-8.152 - mu[idx]) / sigma_proc[3])))

    if I["m_v_int"].sum():
        idx = np.nonzero(I["m_v_int"])[0]
        lo = jnp.asarray(I["bin_lo"])[idx]
        hi = jnp.asarray(I["bin_hi"])[idx]
        s = sigma_proc[2]
        lu = log_ndtr((hi - mu[idx]) / s)
        ll = log_ndtr((lo - mu[idx]) / s)
        # log(Phi(zu) - Phi(zl)). The clip is not cosmetic: a bin whose lower
        # edge sits far below mu sends log_ndtr to -inf, and the 0 * inf that
        # follows in the chain rule is exactly what makes the gradient NaN.
        dd = jnp.clip(ll - lu, -700.0, -1e-10)
        numpyro.factor("vijay_interval", jnp.sum(lu + jnp.log(-jnp.expm1(dd))))
    if I["m_v_point"].sum():
        obs_normal(I["m_v_point"], mu, sigma_proc[2], "y_vijay_point")
    if I["m_v_left"].sum():
        idx = np.nonzero(I["m_v_left"])[0]
        numpyro.factor("vijay_left", jnp.sum(
            log_ndtr((np.log10(23.0) - mu[idx]) / sigma_proc[2])))

    numpyro.deterministic("mu_all", mu)


def init_values(I):
    """An explicit, flat starting point.

    A random start puts a latent density of 0 log10 against readings at 7 log10
    and the left-censoring terms underflow before the sampler has moved once.
    Starting every rate at zero and every intercept near the deposit's own mean
    is not an assumption about the answer - b is free and sign-free from the
    first step - it is just a start that has finite gradient.
    """
    S, P = I["n_series"], I["X"].shape[1]
    return {
        "beta": np.zeros((P, MAXSEG)),
        "tau_d": np.array([0.1, 0.1, 0.1, 2.4]),
        "sigma_lab": 0.1, "sigma_iso": 0.1,
        "sigma_rate_hyper": 0.3, "sigma_series_d": np.array([0.3, 0.3, 0.3, 0.3]),
        "u_lab": np.zeros(max(I["n_labs"], 1)),
        "u_iso": np.zeros(max(I["n_iso"], 1)),
        "w_series": np.zeros(S),
        "z_rw": np.zeros((S, MAXSEG - 1)),
        "alpha_d": np.array([5.5, 6.5, 6.5, 0.0]),
        "sigma_a": np.array([1.0, 1.0, 1.0, 1.0]),
        "sigma_lab_a": 1.0,
        "u_lab_a": np.zeros(max(I["n_labs"], 1)),
        "z_a": np.zeros(S),
        "a_windels": np.zeros(int(I["is_windels_series"].sum())),
        "sigma_plate": 0.4,
        "sigma_proc_d": np.array([0.4, 0.3, 0.3, 0.5]),
        "pi_era4tb": 0.15,
        "eta_visit": np.zeros(max(I["n_visits"], 1)),
    }


def _p_blank_jax(mu, sd, vol):
    import jax.numpy as jnp
    x = mu[:, None] + np.sqrt(2.0) * sd * jnp.asarray(GH_NODES)
    lam = jnp.power(10.0, x) * vol[:, None] / 1000.0
    return jnp.sum(jnp.asarray(GH_WEIGHTS) * jnp.exp(-lam), axis=1)


def run_mcmc(I, seed, warmup, draws, chains, target_accept=0.9, tree_depth=12,
             progress=False):
    import jax
    import numpyro
    from functools import partial
    from numpyro.infer import MCMC, NUTS, init_to_value
    # I is closed over, never passed as a model argument: jax would otherwise
    # trace every index array in it and the numpy masks would stop being numpy.
    kernel = NUTS(partial(ctbp_model, I), target_accept_prob=target_accept,
                  max_tree_depth=tree_depth,
                  init_strategy=init_to_value(values=init_values(I)))
    mcmc = MCMC(kernel, num_warmup=warmup, num_samples=draws, num_chains=chains,
                chain_method="parallel" if chains > 1 else "sequential",
                progress_bar=progress)
    t0 = time.time()
    mcmc.run(jax.random.PRNGKey(seed))
    el = time.time() - t0
    return mcmc, el


def diagnostics(mcmc, keys=("beta", "tau_d", "sigma_lab", "sigma_iso", "sigma_series_d",
                            "sigma_plate", "sigma_proc_d", "pi_era4tb", "b")):
    from numpyro.diagnostics import summary
    s = summary(mcmc.get_samples(group_by_chain=True), prob=0.9)
    worst_r, min_ess = 1.0, np.inf
    per = {}
    for k in keys:
        if k not in s:
            continue
        r = float(np.nanmax(s[k]["r_hat"]))
        e = float(np.nanmin(s[k]["n_eff"]))
        per[k] = {"max_r_hat": r, "min_ess": e}
        worst_r = max(worst_r, r)
        min_ess = min(min_ess, e)
    extra = mcmc.get_extra_fields() if mcmc._states else {}
    return {"per_parameter": per, "max_r_hat": worst_r, "min_ess": float(min_ess),
            "gate_pass": bool(worst_r <= 1.01 and min_ess >= 400)}


# ===========================================================================
# 3. POSTERIOR -> DERIVED QUANTITIES
# ===========================================================================
def posterior_series(mcmc, D):
    """b_tail, mu at the last knot, and the early-phase rate, per series."""
    sm = mcmc.get_samples()
    b = np.asarray(sm["b"])                     # (draws, S, MAXSEG)
    a = np.asarray(sm["a"])                     # (draws, S)
    nseg = D["nseg"]
    idx = np.arange(b.shape[1])
    b_tail = b[:, idx, nseg - 1]
    b_first = b[:, idx, 0]
    knots = [KNOTS[bl] for bl in D["ser"]["block"]]
    last = D["ser"]["last_knot_day"].values.astype(float)
    # mu at the last knot the data reached = a - sum of b_m * segment length,
    # over the segments that series actually has.
    seglen = np.zeros((len(idx), MAXSEG))
    for i, k in enumerate(knots):
        n = int(nseg[i])
        seglen[i, :n] = np.diff(k)[:n]
    mu_last = a - np.einsum("dsm,sm->ds", b, seglen)
    return dict(b_tail=b_tail, b_first=b_first, a=a, mu_last=mu_last, last_knot=last,
                sigma_plate=np.asarray(sm["sigma_plate"]),
                sigma_proc=np.asarray(sm["sigma_proc_d"]),
                pi=np.asarray(sm["pi_era4tb"]), samples=sm)


def q(x, p):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    return float(np.quantile(x, p)) if x.size else np.nan


# ===========================================================================
# 4. TABLE 1: HIDDEN BURDEN - exact, fit-free, written before anything is fitted
# ===========================================================================
def write_hidden_burden():
    rows = []
    for v in VOL_GRID_UL:
        L = float(limit_log10_from_volume(v))
        for V in V_GRID_ML:
            H = float(hidden_burden(L, V))
            rows.append(dict(plated_volume_uL=v, limit_log10=round(L, 6), V_mL=V,
                             H_log10_cells=H, H_cells=10.0 ** H,
                             units="H is log10 cells in the whole culture at the "
                                   "instant the plate first reads blank",
                             V_source="SCENARIO - hypothetical vessel volume; no "
                                      "deposit in this corpus records one"))
    t = pd.DataFrame(rows)
    TABLES.mkdir(parents=True, exist_ok=True)
    t.to_csv(TABLES / "ctbp_hidden_burden.csv", index=False)
    return t


# ===========================================================================
# 5. IDENTIFIABILITY GATE (single-series estimator, the real ERA4TB grid)
# ===========================================================================
ERA4TB_VISITS = np.array([0.0, 1.0, 2.0, 3.0, 7.0, 10.0, 14.0, 21.0])
ERA4TB_PLATES = np.array([100.0, 10.0, 10.0, 2.5])


def _series_nll(params, t, vol, y, cen, knots, sigma, pi):
    a, b0, b1, b2, b3 = params
    b = np.array([b0, b1, b2, b3])[: len(knots) - 1]
    lo, hi = knots[:-1], knots[1:].copy()
    hi[-1] = np.inf
    W = np.clip(t[:, None] - lo, 0.0, hi - lo)
    mu = a - W @ b
    ll = 0.0
    if np.any(~cen):
        ll += np.sum(stats.norm.logpdf(y[~cen], mu[~cen], sigma))
    if np.any(cen):
        pb = p_blank(mu[cen], sigma, vol[cen])
        ll += np.sum(np.log(pi + (1 - pi) * pb + 1e-300))
    return -ll


def simulate_era4tb_series(rng, a0, b_true, sigma, pi, knots=KNOTS["era4tb"]):
    t = np.repeat(ERA4TB_VISITS, len(ERA4TB_PLATES))
    vol = np.tile(ERA4TB_PLATES, len(ERA4TB_VISITS))
    lo, hi = knots[:-1], knots[1:].copy()
    hi[-1] = np.inf
    W = np.clip(t[:, None] - lo, 0.0, hi - lo)
    mu = a0 - W @ b_true
    x = rng.normal(mu, sigma)
    lam = np.power(10.0, x) * vol / 1000.0
    cen = (rng.poisson(np.clip(lam, 0, 1e12)) == 0) | (rng.random(len(t)) < pi)
    y = np.where(cen, np.nan, x)
    return t, vol, y, cen


def identifiability_gate(n_rep=200, n_profile=20, seed=SEED, quick=False):
    """exp25, retargeted from Design 2's alpha onto b_tail, and used as a GATE.

    Simulates on the REAL ERA4TB visit grid with the REAL per-row limits and
    volumes. The censoring fraction is an OUTCOME, not an input, so it is
    controlled by moving the starting level and then reported as realised.

    The point estimate is computed on all n_rep replicates; the profile-
    likelihood interval, which costs 13 nested optimisations each, is computed
    on the first n_profile of them. That subsampling is declared here and
    recorded in the table.
    """
    rng = np.random.default_rng(seed)
    if quick:
        n_rep, n_profile = 40, 8
    sigma, pi = 0.45, 0.12
    rows = []
    for b_tail_true in [0.02, 0.05, 0.10, 0.20]:
        for a0 in [7.0, 6.0, 5.0, 4.0, 3.0, 2.0]:
            b_true = np.array([0.45, 0.20, 0.10, b_tail_true])
            est, cf, wid, cov = [], [], [], []
            for k in range(n_rep):
                t, vol, y, cen = simulate_era4tb_series(rng, a0, b_true, sigma, pi)
                cf.append(float(cen.mean()))
                if cen.sum() >= len(cen) - 2:
                    est.append(np.nan)
                    continue
                p0 = np.array([np.nanmax(y), 0.4, 0.2, 0.1, 0.05])
                r = optimize.minimize(_series_nll, p0,
                                      args=(t, vol, y, cen, KNOTS["era4tb"], sigma, pi),
                                      method="Nelder-Mead",
                                      options=dict(maxiter=4000, xatol=1e-4, fatol=1e-4))
                est.append(r.x[4])
                if k < n_profile:
                    lo_b, hi_b = _profile_interval(r, t, vol, y, cen, sigma, pi)
                    wid.append(hi_b - lo_b)
                    cov.append(float(lo_b <= b_tail_true <= hi_b))
            est = np.array(est, dtype=float)
            ok = np.isfinite(est)
            rows.append(dict(
                true_b_tail_log10_per_day=b_tail_true, true_a_log10=a0,
                sigma_log10=sigma, pi_misread=pi, n_rep=n_rep,
                n_rep_with_profile_interval=n_profile,
                mean_censored_fraction=float(np.mean(cf)),
                n_estimable=int(ok.sum()),
                bias_log10_per_day=float(np.mean(est[ok]) - b_tail_true) if ok.any() else np.nan,
                median_b_tail_log10_per_day=float(np.median(est[ok])) if ok.any() else np.nan,
                interval_width_90_log10_per_day=float(np.median(wid)) if wid else np.nan,
                coverage_90=float(np.mean(cov)) if cov else np.nan,
                units="all rates log10 per day"))
    return pd.DataFrame(rows)


def _profile_interval(fit, t, vol, y, cen, sigma, pi, max_half_width=3.0,
                      n_bisect=9):
    """Profile-likelihood 90% interval on b_tail, found by bisection.

    A grid is not good enough here: the whole point of the gate is to measure
    how WIDE the interval gets as censoring rises, and a grid can only report
    multiples of its own spacing. The interval is opened outward from the MLE
    until the profile deviance crosses 0.5 * chi2(0.90, 1), then bisected. An
    endpoint that never crosses inside max_half_width is returned at the bound
    and the interval is, correctly, uninformative.
    """
    bhat = float(fit.x[4])
    warm = np.array(fit.x[:4], dtype=float)

    def prof(b):
        def f(pp):
            return _series_nll(np.array([pp[0], pp[1], pp[2], pp[3], b]), t, vol, y,
                               cen, KNOTS["era4tb"], sigma, pi)
        r = optimize.minimize(f, warm, method="Powell",
                              options=dict(maxiter=800, xtol=1e-3, ftol=1e-4))
        return float(r.fun)

    fmin = prof(bhat)
    thr = fmin + 0.5 * stats.chi2.ppf(0.90, 1)

    def find_edge(direction):
        step = max(0.02, 0.25 * abs(bhat))
        lo, hi = bhat, bhat
        while abs(hi - bhat) < max_half_width:
            hi = bhat + direction * step
            if prof(hi) > thr:
                break
            lo = hi
            step *= 2.0
        else:
            return bhat + direction * max_half_width
        for _ in range(n_bisect):
            mid = 0.5 * (lo + hi)
            if prof(mid) > thr:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    return float(find_edge(-1.0)), float(find_edge(+1.0))


def gate_boundary(tab, max_width=0.20):
    """The deliverable: the largest censoring fraction at which b_tail is
    estimable to a stated 90% interval width."""
    ok = tab[(tab["interval_width_90_log10_per_day"] <= max_width)]
    if not len(ok):
        return dict(max_censored_fraction_for_width=None, stated_width=max_width)
    return dict(max_censored_fraction_for_width=float(ok["mean_censored_fraction"].max()),
                stated_width=max_width,
                worst_bias_inside_boundary=float(ok["bias_log10_per_day"].abs().max()),
                min_coverage_inside_boundary=float(ok["coverage_90"].min()))


# ===========================================================================
# 6. PRIOR PREDICTIVE
# ===========================================================================
def prior_predictive(I, seed=SEED, n=400):
    import jax
    import numpyro
    from numpyro.infer import Predictive
    # The Windels intercept is an improper flat prior - it has no prior to draw
    # from, which is the point. Fix it at zero for the prior predictive; nothing
    # in this check involves an intercept.
    from functools import partial
    model = numpyro.handlers.substitute(
        partial(ctbp_model, I),
        {"a_windels": np.zeros(int(I["is_windels_series"].sum()))})
    pred = Predictive(model, num_samples=n)
    s = pred(jax.random.PRNGKey(seed + 7))
    b = np.asarray(s["b"])
    nseg = I["nseg"]
    bt = b[:, np.arange(b.shape[1]), nseg - 1]
    era = I["dep_idx"] == 0
    bte = bt[:, era].ravel()
    return dict(
        prior_b_tail_median_era4tb_log10_per_day=float(np.median(bte)),
        prior_P_b_tail_positive_era4tb=float(np.mean(bte > 0)),
        prior_symmetric_about_zero=bool(abs(np.mean(bte > 0) - 0.5) < 0.05),
        prior_admits_sterilisation=bool(np.mean(bte > 0.05) > 0.2),
        prior_admits_unbounded_regrowth=bool(np.mean(bte < -0.05) > 0.2),
        prior_b_tail_q05=float(np.quantile(bte, 0.05)),
        prior_b_tail_q95=float(np.quantile(bte, 0.95)),
        units="log10 per day")


# ===========================================================================
# 7. VALIDATION
# ===========================================================================
def v1_plate_holdout(seed, mcmc_kw, log_extra):
    """THE GATE. Fit on 2.5 and 10 uL only; predict the held-out 100 uL readings.

    Same biological samples, same visits, read 1.6 log10 deeper, with 663 real
    readings waiting on the other side. This is the only miniature of the
    sub-limit extrapolation available anywhere in the corpus.
    """
    Dtr = build_design(drop_volumes=(100.0,), deposits=("era4tb",))
    Itr = make_model_inputs(Dtr)
    mcmc, el = run_mcmc(Itr, seed + 11, **mcmc_kw)

    Dall = build_design(deposits=("era4tb",))
    Iall = make_model_inputs(Dall)
    rows = Dall["rows"]
    held = ((rows["deposit"] == "era4tb") & (rows["plated_volume_uL"] == 100.0)).values
    # map held-out rows onto the SERIES fitted in the training design
    tr_ser = {u: i for i, u in enumerate(Dtr["ser"]["unit_group"])}
    keep = held & rows["unit_group"].map(lambda u: u in tr_ser).values
    sm = mcmc.get_samples()
    b = np.asarray(sm["b"])
    a = np.asarray(sm["a"])
    si = np.array([tr_ser[u] for u in rows.loc[keep, "unit_group"]])
    W = Iall["W"][keep]
    mu_curve = a[:, si] - np.einsum("rm,drm->dr", W, b[:, si, :])
    sp = np.asarray(sm["sigma_plate"])[:, None]
    proc = np.asarray(sm["sigma_proc_d"])[:, 0][:, None]
    pi = np.asarray(sm["pi_era4tb"])[:, None]
    eta = np.asarray(sm["eta_visit"])

    # A held-out 100 uL plate is a NEW PLATE OF AN ALREADY-OBSERVED SAMPLE: the
    # 2.5 and 10 uL plates of that same flask at that same visit were in the
    # training set, so the visit-level latent density is estimated and the only
    # remaining noise is plating noise. That is the conditioning under which the
    # blank-plate layer has genuinely zero free parameters for the deeper limit.
    # The stricter trajectory-only prediction, which throws the visit effect away
    # and pays sigma_process as well, is scored alongside it.
    vmap = {k: i for i, k in enumerate(Dtr["visit_keys"])}
    vi = np.array([vmap.get(k, -1) for k in rows.loc[keep, "sample_visit"]])
    known = vi >= 0
    mu = mu_curve.copy()
    mu[:, known] = mu_curve[:, known] + eta[:, np.clip(vi[known], 0, None)] * proc
    sd_cond = np.where(known[None, :], sp, np.sqrt(sp ** 2 + proc ** 2))
    sd_tot = np.sqrt(sp ** 2 + proc ** 2) * np.ones((1, mu.shape[1]))

    cen = rows.loc[keep, "censored"].fillna(False).values
    y = rows.loc[keep, "y_log10"].values
    unc = ~cen
    rng = np.random.default_rng(seed)

    def score(mu_, sd_):
        yp = mu_ + rng.normal(0, 1, mu_.shape) * sd_
        lo = np.quantile(yp, 0.05, axis=0)
        hi = np.quantile(yp, 0.95, axis=0)
        cov = float(np.mean((y[unc] >= lo[unc]) & (y[unc] <= hi[unc]))) if unc.any() else np.nan
        nd = mu_.shape[0]
        thin = slice(0, nd, max(1, nd // 200))
        vol = np.full(mu_.shape[1], 100.0)
        pb = np.array([p_blank(mu_[i], sd_[min(i, sd_.shape[0] - 1)], vol)
                       for i in range(*thin.indices(nd))])
        pf = pi[thin][: pb.shape[0]]
        pfl = (pf + (1 - pf) * pb).mean(axis=0)
        return cov, pfl

    cover, pflag = score(mu, sd_cond)
    cover_traj, pflag_traj = score(mu_curve, sd_tot)

    pred_rate = float(pflag.mean())
    obs_rate = float(cen.mean())
    fold = pred_rate / obs_rate if obs_rate > 0 else np.inf
    deep = unc & (y >= 1.0) & (y < 2.0)
    mm = mu.mean(axis=0)
    bias_deep = float(np.mean(mm[deep] - y[deep])) if deep.any() else np.nan
    rmse = float(np.sqrt(np.mean((mm[unc] - y[unc]) ** 2)))
    mae = float(np.mean(np.abs(mm[unc] - y[unc])))
    brier = float(np.mean((pflag - cen.astype(float)) ** 2))

    passed = (V1_COVERAGE_BAND[0] <= cover <= V1_COVERAGE_BAND[1]) and \
             (1.0 / V1_BLANK_RATE_FOLD <= fold <= V1_BLANK_RATE_FOLD)
    detail = dict(n_held_out_rows=int(keep.sum()), n_uncensored=int(unc.sum()),
                  n_censored=int(cen.sum()),
                  n_rows_whose_visit_was_seen_at_another_volume=int(known.sum()),
                  coverage_90=cover,
                  coverage_90_trajectory_only=cover_traj,
                  predicted_blank_rate=pred_rate,
                  predicted_blank_rate_trajectory_only=float(pflag_traj.mean()),
                  observed_blank_rate=obs_rate,
                  fold_error_on_blank_rate=fold, rmse_log10=rmse, mae_log10=mae,
                  bias_in_1_to_2_log10_window=bias_deep,
                  n_in_1_to_2_window=int(deep.sum()),
                  brier_score=brier, fit_seconds=el, gate_pass=bool(passed),
                  rate_units="log10 CFU/mL for every quantity here")
    calib = pd.DataFrame(dict(
        unit_group=rows.loc[keep, "unit_group"].values,
        time_days=rows.loc[keep, "time_days"].values,
        plated_volume_uL=100.0, limit_log10=1.0,
        observed_blank=cen.astype(int), observed_y_log10=y,
        predicted_p_blank=pflag, mu_median=np.median(mu, axis=0),
        mu_q05=np.quantile(mu, 0.05, axis=0), mu_q95=np.quantile(mu, 0.95, axis=0),
        fold="V1-holdout"))
    log_extra["v1_training_rows"] = int(len(Dtr["rows"]))
    return detail, calib


def v2_leave_one_lab_out(seed, mcmc_kw, quick=False):
    Dall = build_design(deposits=("era4tb",))
    rows_all = Dall["rows"]
    labs = Dall["labs"][:2] if quick else Dall["labs"]
    out, calib = [], []
    for L in labs:
        Dtr = build_design(drop_labs=(L,), deposits=("era4tb",))
        Itr = make_model_inputs(Dtr)
        mcmc, el = run_mcmc(Itr, seed + 100 + labs.index(L), **mcmc_kw)
        sm = mcmc.get_samples()
        # the held-out lab's series were not fitted; predict from the deposit
        # regression plus the population lab distribution
        beta = np.asarray(sm["beta"])
        tau = np.asarray(sm["tau_d"])[:, 0]
        s_lab = np.asarray(sm["sigma_lab"])
        s_ser = np.asarray(sm["sigma_series"])[:, 0]   # ERA4TB column
        alpha = np.asarray(sm["alpha_d"])[:, 0]
        s_a = np.asarray(sm["sigma_a"])[:, 0]
        s_la = np.asarray(sm["sigma_lab_a"])
        sp = np.asarray(sm["sigma_plate"])
        proc = np.asarray(sm["sigma_proc_d"])[:, 0]
        pi = np.asarray(sm["pi_era4tb"])

        m = (rows_all["deposit"] == "era4tb") & (rows_all["lab"] == L)
        held = rows_all[m]
        if not len(held):
            continue
        sers = Dall["ser"].set_index("unit_group")
        ug = held["unit_group"].values
        uq = pd.unique(ug)
        Xh = pd.DataFrame(Dall["X"], columns=Dall["Xcols"])
        Xh.index = Dall["ser"]["unit_group"]
        rng = np.random.default_rng(seed + 3)
        nd = beta.shape[0]
        mu_pred = np.zeros((nd, len(held)))
        xrow = Xh.loc[ug].values
        xb = np.einsum("rp,dpm->drm", xrow, beta)
        ulab = rng.normal(0, 1, (nd, 1)) * s_lab[:, None]
        wser = rng.normal(0, 1, (nd, len(held))) * s_ser[:, None]
        z = rng.normal(0, 1, (nd, len(held), MAXSEG - 1)) * tau[:, None, None]
        steps = np.cumsum(np.concatenate([np.zeros((nd, len(held), 1)), z], axis=2), axis=2)
        bpred = (xb[:, :, 0] + ulab + wser)[:, :, None] + (xb - xb[:, :, :1]) + steps
        aa = alpha[:, None] + rng.normal(0, 1, (nd, 1)) * s_la[:, None] + \
            rng.normal(0, 1, (nd, len(held))) * s_a[:, None]
        W = Dall["W"][m.values]
        mu_pred = aa - np.einsum("rm,drm->dr", W, bpred)
        sd_tot = np.sqrt(sp ** 2 + proc ** 2)[:, None]
        y = held["y_log10"].values
        cen = held["censored"].fillna(False).values
        unc = ~cen
        yp = mu_pred + rng.normal(0, 1, mu_pred.shape) * sd_tot
        lo, hi = np.quantile(yp, 0.05, axis=0), np.quantile(yp, 0.95, axis=0)
        cover = float(np.mean((y[unc] >= lo[unc]) & (y[unc] <= hi[unc]))) if unc.any() else np.nan
        logsc = float(np.mean(stats.norm.logpdf(
            y[unc], mu_pred.mean(axis=0)[unc], np.sqrt(np.mean(sd_tot) ** 2 + mu_pred.var(axis=0)[unc])))) \
            if unc.any() else np.nan
        vol = held["plated_volume_uL"].values
        th = slice(0, nd, max(1, nd // 100))
        pb = np.array([p_blank(mu_pred[i], float(sd_tot[i, 0]), vol)
                       for i in range(*th.indices(nd))])
        pf = pi[th][: pb.shape[0], None]
        pflag = (pf + (1 - pf) * pb).mean(axis=0)
        ever = held.groupby("unit_group")["censored"].max()
        out.append(dict(fold=f"lab_{L}", n_series=int(len(uq)), n_rows=int(len(held)),
                        n_censored=int(cen.sum()), predicted_blank_rate=float(pflag.mean()),
                        observed_blank_rate=float(cen.mean()),
                        coverage_90=cover, mean_log_score=logsc,
                        rmse_log10=float(np.sqrt(np.mean((mu_pred.mean(0)[unc] - y[unc]) ** 2)))
                        if unc.any() else np.nan,
                        n_series_ever_censored=int(ever.sum()),
                        zero_event_fold=bool(ever.sum() == 0), fit_seconds=el))
        calib.append(pd.DataFrame(dict(
            unit_group=ug, time_days=held["time_days"].values,
            plated_volume_uL=vol, limit_log10=held["limit_log10"].values,
            observed_blank=cen.astype(int), observed_y_log10=y,
            predicted_p_blank=pflag, mu_median=np.median(mu_pred, axis=0),
            mu_q05=np.quantile(mu_pred, 0.05, axis=0),
            mu_q95=np.quantile(mu_pred, 0.95, axis=0), fold=f"V2-lab_{L}")))
    return pd.DataFrame(out), (pd.concat(calib, ignore_index=True) if calib else pd.DataFrame())


def v3_windels_cells(seed, quick=False):
    """Leave-one-cell-out on the Windels 6x6 grid, on a WINDELS-ONLY submodel.

    Refitting the full four-deposit model 34 times is not affordable; the
    state-by-dose interaction is a Windels-internal quantity and the deposit's
    betas are deposit-specific by construction, so a Windels-only refit is the
    same estimand. This substitution is declared, not silent.
    """
    w = pd.read_csv(PROC / "tidy_windels.csv")
    w = w[~w["censored"]]
    cells = sorted(set(zip(w["state_numeric"], w["dose_value"])))
    if quick:
        cells = cells[::6]
    rows = []
    for (s, dd) in cells:
        tr = w[~((w["state_numeric"] == s) & (w["dose_value"] == dd))]
        te = w[(w["state_numeric"] == s) & (w["dose_value"] == dd)]
        if not len(te):
            continue
        # OLS on the interaction surface for the per-segment rates, per series
        fit = _windels_surface_fit(tr)
        pred, obs = [], []
        for ug, g in te.groupby("unit_group"):
            g = g.sort_values("time_days")
            if 0.0 not in set(g["time_days"]):
                continue
            for _, r in g[g["time_days"] > 0].iterrows():
                pred.append(_windels_surface_predict(fit, s, dd, r["time_days"]))
                obs.append(r["y_log10"])
        if not pred:
            continue
        pred, obs = np.array(pred), np.array(obs)
        extrap = (s == 0.95) and (dd in (200.0, 400.0))
        rows.append(dict(nutrient=s, dose_ug_per_mL=dd, n_points=len(obs),
                         rmse_log10=float(np.sqrt(np.mean((pred - obs) ** 2))),
                         bias_log10=float(np.mean(pred - obs)),
                         is_extrapolation_not_holdout=bool(extrap)))
    return pd.DataFrame(rows)


def _windels_surface_fit(tr):
    """Segment rates as a linear surface in (nutrient, log10 dose) and their
    interaction, fitted by least squares on per-interval decline rates."""
    recs = []
    for ug, g in tr.groupby("unit_group"):
        g = g.sort_values("time_days")
        t = g["time_days"].values
        y = g["y_log10"].values
        for i in range(len(t) - 1):
            if t[i + 1] <= t[i]:
                continue
            recs.append(dict(seg=_seg_of(t[i], KNOTS["windels"]),
                             nut=g["state_numeric"].iloc[0],
                             ld=np.log10(g["dose_value"].iloc[0]),
                             rate=-(y[i + 1] - y[i]) / (t[i + 1] - t[i])))
    r = pd.DataFrame(recs)
    models = {}
    for seg, gg in r.groupby("seg"):
        A = np.column_stack([np.ones(len(gg)), gg["nut"], gg["ld"], gg["nut"] * gg["ld"]])
        coef, *_ = np.linalg.lstsq(A, gg["rate"].values, rcond=None)
        models[seg] = coef
    return models


def _seg_of(t, knots):
    return int(np.clip(np.searchsorted(knots, t, side="right") - 1, 0, len(knots) - 2))


def _windels_surface_predict(models, nut, dose, t):
    ld = np.log10(dose)
    knots = KNOTS["windels"]
    lo, hi = knots[:-1], knots[1:].copy()
    hi[-1] = np.inf
    w = np.clip(t - lo, 0.0, hi - lo)
    drop = 0.0
    for m in range(len(lo)):
        c = models.get(m)
        if c is None:
            continue
        drop += w[m] * (c[0] + c[1] * nut + c[2] * ld + c[3] * nut * ld)
    return -drop


def v4_vijay(seed, mcmc_kw):
    """Vijay as external calibration: fit on 15d + 30d, predict the 60d block."""
    Dtr = build_design(drop_vijay_states=("culture_age_60d",), deposits=("vijay",))
    Itr = make_model_inputs(Dtr)
    mcmc, el = run_mcmc(Itr, seed + 55, **mcmc_kw)
    sm = mcmc.get_samples()
    beta = np.asarray(sm["beta"])
    tau = np.asarray(sm["tau_d"])[:, 2]
    s_iso = np.asarray(sm["sigma_iso"])
    s_ser = np.asarray(sm["sigma_series"])[:, 2]   # Vijay column
    alpha = np.asarray(sm["alpha_d"])[:, 2]
    s_a = np.asarray(sm["sigma_a"])[:, 2]
    proc = np.asarray(sm["sigma_proc_d"])[:, 2]

    Dall = build_design(deposits=("vijay",))
    rows = Dall["rows"]
    m = ((rows["deposit"] == "vijay") & (rows["state_label"] == "culture_age_60d")).values
    held = rows[m]
    Xh = pd.DataFrame(Dall["X"], columns=Dall["Xcols"])
    Xh.index = Dall["ser"]["unit_group"]
    xrow = Xh.loc[held["unit_group"]].values
    nd = beta.shape[0]
    rng = np.random.default_rng(seed + 4)
    xb = np.einsum("rp,dpm->drm", xrow, beta)
    b0 = xb[:, :, 0] + rng.normal(0, 1, (nd, len(held))) *         np.sqrt(s_iso ** 2 + s_ser ** 2)[:, None]
    z = rng.normal(0, 1, (nd, len(held), MAXSEG - 1)) * tau[:, None, None]
    steps = np.cumsum(np.concatenate([np.zeros((nd, len(held), 1)), z], axis=2), axis=2)
    bpred = b0[:, :, None] + (xb - xb[:, :, :1]) + steps
    aa = alpha[:, None] + rng.normal(0, 1, (nd, len(held))) * s_a[:, None]
    W = Dall["W"][m]
    mu = aa - np.einsum("rm,drm->dr", W, bpred)

    # score the day-5 log drop per series, which is what this deposit resolves
    obs, pred = [], []
    for ug, g in held.groupby("unit_group"):
        g5 = g[g["time_days"] == 5.0]
        g0 = g[g["time_days"] == 0.0]
        if not len(g5) or not len(g0) or g5["censored"].iloc[0] or g0["censored"].iloc[0]:
            continue
        i5 = np.nonzero((held["unit_group"] == ug).values & (held["time_days"] == 5.0).values)[0][0]
        i0 = np.nonzero((held["unit_group"] == ug).values & (held["time_days"] == 0.0).values)[0][0]
        obs.append(g0["y_log10"].iloc[0] - g5["y_log10"].iloc[0])
        pred.append(mu[:, i0] - mu[:, i5])
    obs = np.array(obs)
    pred = np.array(pred).T                       # (draws, series)
    pit = np.array([np.mean(pred[:, j] <= obs[j]) for j in range(len(obs))])
    lo, hi = np.quantile(pred, 0.05, axis=0), np.quantile(pred, 0.95, axis=0)
    return dict(fold="vijay_60d_held_out", n_series_scored=int(len(obs)),
                observed_mean_day5_log10_drop=float(obs.mean()),
                predicted_mean_day5_log10_drop=float(pred.mean()),
                coverage_90=float(np.mean((obs >= lo) & (obs <= hi))),
                pit_ks_statistic=float(stats.kstest(pit, "uniform").statistic),
                pit_ks_pvalue=float(stats.kstest(pit, "uniform").pvalue),
                readout_distinct_y_values=29,
                note="the readout resolves ~1 log10; the model is neither credited "
                     "nor penalised for structure finer than the decade ladder",
                fit_seconds=el)


def v6_sbc(seed, mcmc_kw, n_sim=12, quick=False):
    """Simulation-based calibration of the ESTIMATOR, not of the assumption.

    Simulates on the real ERA4TB visit grid with the real per-row limits and
    volumes, at known b_tail, then refits with the same single-series estimator
    used for the gate. This validates the inference machinery given the model.
    It is NOT evidence that any sub-limit trajectory, or any T_ext, is correct.
    """
    rng = np.random.default_rng(seed + 9)
    if quick:
        n_sim = 3
    rec = []
    for _ in range(n_sim * 20):
        b_true = np.array([abs(rng.normal(0.4, 0.2)), rng.normal(0.15, 0.1),
                           rng.normal(0.08, 0.08), rng.normal(0.05, 0.12)])
        a0 = rng.uniform(3.5, 7.0)
        sigma, pi = 0.45, 0.12
        t, vol, y, cen = simulate_era4tb_series(rng, a0, b_true, sigma, pi)
        if np.all(cen) or (~cen).sum() < 6:
            continue
        p0 = np.array([np.nanmax(y), 0.4, 0.15, 0.08, 0.05])
        r = optimize.minimize(_series_nll, p0,
                              args=(t, vol, y, cen, KNOTS["era4tb"], sigma, pi),
                              method="Nelder-Mead", options=dict(maxiter=4000))
        lo, hi = _profile_interval(r, t, vol, y, cen, sigma, pi)
        H = hidden_burden(1.0, 10.0)
        rec.append(dict(true_b_tail=b_true[3], est_b_tail=r.x[4],
                        covered=float(lo <= b_true[3] <= hi),
                        true_inf=float(b_true[3] <= 0), est_inf=float(r.x[4] <= 0),
                        true_delta=float(gap(H, b_true[3])),
                        est_delta=float(gap(H, r.x[4]))))
        if len(rec) >= n_sim * 20:
            break
    r = pd.DataFrame(rec)
    fin = r[np.isfinite(r["true_delta"]) & np.isfinite(r["est_delta"])]
    return dict(n_simulations=int(len(r)),
                b_tail_bias_log10_per_day=float((r["est_b_tail"] - r["true_b_tail"]).mean()),
                b_tail_nominal_90_coverage=float(r["covered"].mean()),
                P_inf_agreement=float((r["true_inf"] == r["est_inf"]).mean()),
                delta_median_relative_error=float(np.median(
                    (fin["est_delta"] - fin["true_delta"]) / fin["true_delta"])) if len(fin) else np.nan,
                statement="validates the INFERENCE MACHINERY, not the assumption; "
                          "it is not evidence that any T_ext is correct")


def v6_sbc_hierarchical(mcmc, D, I, seed, mcmc_kw, n_sim=16, quick=False):
    """SBC on the ACTUAL estimator: simulate ERA4TB from the fitted model, on the
    real visit grid with the real per-row plating volumes, then refit the whole
    hierarchical model and check recovery of b_tail, of Delta and of
    P(b_tail <= 0).

    The blank plates are simulated the way the model says they arise - a Poisson
    draw at 10**mu * v/1000, plus the misread rate pi - so the censoring pattern
    is generated, not copied.

    THIS VALIDATES THE INFERENCE MACHINERY GIVEN THE MODEL. It is not evidence
    that any sub-limit trajectory is correct, and it is not evidence that any
    T_ext is correct. Those two things are different and conflating them is the
    easiest way to mislead a referee.
    """
    if quick:
        n_sim = 2
    sm = mcmc.get_samples()
    b_all = np.asarray(sm["b"])
    a_all = np.asarray(sm["a"])
    sp_all = np.asarray(sm["sigma_plate"])
    pr_all = np.asarray(sm["sigma_proc_d"])[:, 0]
    pi_all = np.asarray(sm["pi_era4tb"])
    nd = b_all.shape[0]
    rng = np.random.default_rng(seed + 31)
    rows = D["rows"]
    era = (rows["deposit"] == "era4tb").values
    W = I["W"][era]
    si = I["sidx"][era]
    vol = rows.loc[era, "plated_volume_uL"].values.astype(float)
    vis = I["visit_idx"][era]
    nseg = D["nseg"]

    recs = []
    for k in range(n_sim):
        j = int(rng.integers(0, nd))
        mu = a_all[j][si] - np.einsum("rm,rm->r", W, b_all[j][si, :])
        eta = rng.normal(0, pr_all[j], size=int(vis.max()) + 1)
        mu_v = mu + eta[np.clip(vis, 0, None)]
        x = rng.normal(mu_v, sp_all[j])
        lam = np.power(10.0, np.clip(x, -50, 20)) * vol / 1000.0
        blank = (rng.poisson(np.clip(lam, 0, 1e9)) == 0) | (rng.random(len(x)) < pi_all[j])
        sim = rows.copy()
        yy = sim["y_log10"].values.astype(float).copy()
        cc = np.zeros(len(sim), dtype=bool)
        yy[era] = np.where(blank, np.nan, x)
        cc[era] = blank
        sim["y_log10"] = yy
        sim["censored"] = np.where(era, cc, sim["censored"].fillna(False).values)
        Dsim = dict(D)
        Dsim["rows"] = sim
        Isim = make_model_inputs(Dsim)
        m2, _ = run_mcmc(Isim, seed + 400 + k, **mcmc_kw)
        ps2 = posterior_series(m2, Dsim)
        truth = b_all[j][np.arange(b_all.shape[1]), nseg - 1]
        est = ps2["b_tail"]
        eidx = np.nonzero((D["ser"]["deposit"] == "era4tb").values)[0]
        lo = np.quantile(est[:, eidx], 0.05, axis=0)
        hi = np.quantile(est[:, eidx], 0.95, axis=0)
        tt = truth[eidx]
        H = float(hidden_burden(1.0, 10.0))
        recs.append(dict(
            sim=k, n_series=len(eidx),
            b_tail_bias=float(np.median(est[:, eidx], axis=0).mean() - tt.mean()),
            b_tail_coverage_90=float(np.mean((tt >= lo) & (tt <= hi))),
            P_inf_true=float(np.mean(tt <= 0)),
            P_inf_est=float(np.mean(est[:, eidx] <= 0)),
            simulated_blank_fraction=float(blank.mean())))
    r = pd.DataFrame(recs)
    return dict(
        n_simulations=int(len(r)),
        mcmc=dict(mcmc_kw),
        b_tail_mean_bias_log10_per_day=float(r["b_tail_bias"].mean()),
        b_tail_nominal_90_coverage=float(r["b_tail_coverage_90"].mean()),
        P_inf_true_mean=float(r["P_inf_true"].mean()),
        P_inf_est_mean=float(r["P_inf_est"].mean()),
        simulated_blank_fraction_mean=float(r["simulated_blank_fraction"].mean()),
        per_simulation=r.to_dict("records"),
        statement="validates the INFERENCE MACHINERY given the model, not the "
                  "assumption; it is not evidence that any T_ext is correct")


def v7_negative_controls(mcmc, D, I):
    ps = posterior_series(mcmc, D)
    ser = D["ser"]
    rows = D["rows"]
    unt = ((ser["deposit"] == "era4tb") & (ser["drug"] == "none")).values
    bt = ps["b_tail"][:, unt]
    per = []
    for j, u in enumerate(ser.loc[unt, "unit_group"]):
        per.append(dict(unit_group=u, b_tail_median=float(np.median(bt[:, j])),
                        P_b_tail_le_0=float(np.mean(bt[:, j] <= 0))))
    a_ok = float(np.mean(np.median(bt, axis=0) < 0))
    # (b) the five censored readings in growing, undrugged flasks
    uc = rows[(rows["deposit"] == "era4tb") & rows["censored"].fillna(False)
              & (rows["arm"] == "untreated")]
    sm = mcmc.get_samples()
    b = np.asarray(sm["b"]); a = np.asarray(sm["a"])
    det = []
    for i in uc.index:
        si = int(rows.loc[i, "sidx"])
        mu = a[:, si] - I["W"][i] @ b[:, si, :].T
        det.append(dict(unit_group=rows.loc[i, "unit_group"],
                        time_days=float(rows.loc[i, "time_days"]),
                        plated_volume_uL=float(rows.loc[i, "plated_volume_uL"]),
                        mu_median_log10=float(np.median(mu)),
                        p_blank_at_mu=float(np.mean(p_blank(
                            np.median(mu) * np.ones(1), float(np.median(ps["sigma_plate"])),
                            np.array([rows.loc[i, "plated_volume_uL"]]))))))
    # (c) lab F day-1 MXF 1x
    labF = rows[(rows["deposit"] == "era4tb") & (rows["lab"] == "F")
                & (rows["arm"] == "MXF1x") & (rows["time_days"] == 1.0)]
    fdet = labF[["unit_group", "plated_volume_uL", "y_log10", "censored"]].to_dict("records")
    # (d) return-above-limit series
    era = rows[rows["deposit"] == "era4tb"]
    n_return = 0
    for (ug, v), g in era.groupby(["unit_group", "plated_volume_uL"]):
        g = g.sort_values("time_days")
        c = g["censored"].fillna(False).values
        if c.any() and (~c[np.argmax(c):]).any():
            n_return = n_return + 1
    return dict(
        n_untreated_series=int(unt.sum()),
        fraction_untreated_with_negative_median_b_tail=a_ok,
        mean_P_T_ext_infinite_untreated=float(np.mean(np.mean(bt <= 0, axis=0))),
        per_untreated_series=per,
        pi_era4tb_posterior_median=float(np.median(ps["pi"])),
        pi_era4tb_posterior_90=[q(ps["pi"], .05), q(ps["pi"], .95)],
        censored_readings_in_untreated_flasks=det,
        labF_day1_MXF1x_rows=fdet,
        n_flask_by_volume_series_returning_above_limit=int(n_return),
        note="a full censored likelihood absorbs the returning series; a "
             "first-passage survival endpoint would have fired early on all of them")


# ===========================================================================
# 8. MAIN REPORTING TABLES
# ===========================================================================
COND_COLS = ["deposit", "state_label", "drug", "dose_key", "dose_unit_key"]


def add_condition_cols(ser):
    ser = ser.copy()
    ser["dose_key"] = ser["dose_value"].fillna(-1.0).astype(float)
    ser["dose_unit_key"] = ser["dose_unit"].fillna("").astype(str)
    return ser


def n0_stratum(ser):
    out = []
    for dep, n0, pdb in zip(ser["deposit"], ser["n0_log10"],
                            ser["post_drug_baseline"].astype(bool)):
        if not np.isfinite(n0):
            out.append("absent")
        elif dep == "era4tb" and pdb:
            out.append("post_drug_day1_reading_not_an_inoculum")
        else:
            out.append("observed")
    return out


def build_gap_table(post_by_arm, D_by_arm, gate):
    rows = []
    W_window = {}
    for arm, ps in post_by_arm.items():
        D = D_by_arm[arm]
        ser = add_condition_cols(D["ser"])
        ser["n0_stratum"] = n0_stratum(ser)
        bt = ps["b_tail"]
        mul = ps["mu_last"]
        for cond, g in ser.groupby(COND_COLS, dropna=False):
            idx = g["sidx"].values
            btc = bt[:, idx].ravel()
            p_inf = float(np.mean(btc <= 0))
            cf = _censored_fraction(D, idx)
            identified = bool(cf <= (gate.get("max_censored_fraction_for_width") or 0.0))
            dep, state, drug, dose, dunit = cond
            last_k = float(g["last_knot_day"].max())
            window = float(g["t_last"].max() - g["t_first"].min())
            mulc = mul[:, idx].ravel()
            for vol in VOL_GRID_UL:
                L = float(limit_log10_from_volume(vol))
                for V in V_GRID_ML:
                    H = float(hidden_burden(L, V))
                    for variant in ("linear", "decelerating", "plateau"):
                        d = _delta_variant(variant, H, btc, window)
                        te0 = _t_ext(variant, mulc, btc, last_k, V, window)
                        off95 = sterility_offset_days(btc, 0.95)
                        off99 = sterility_offset_days(btc, 0.99)
                        rows.append(dict(
                            bql_arm=arm, deposit=dep, state_label=state, drug=drug,
                            dose_value=(np.nan if dose == -1 else dose), dose_unit=dunit,
                            n0_stratum="|".join(sorted(set(g["n0_stratum"]))),
                            plated_volume_uL=vol, limit_log10=L, V_mL=V,
                            P_T_ext_infinite=p_inf, n_series=int(len(idx)),
                            b_tail_median_log10_per_day=q(btc, .5),
                            b_tail_q05_log10_per_day=q(btc, .05),
                            b_tail_q95_log10_per_day=q(btc, .95),
                            b_tail_identified=identified, censored_fraction=cf,
                            H_log10_cells=H,
                            Delta_median_days=q(d, .5), Delta_q05_days=q(d, .05),
                            Delta_q95_days=q(d, .95),
                            Delta_units="days, conditional on b_tail>0, mean is undefined",
                            T_ext_0368_days=q(te0, .5),
                            T_ext_p95_days=q(te0 + off95, .5),
                            T_ext_p99_days=q(te0 + off99, .5),
                            extrapolation_depth_log10=float(
                                max(0.0, DEEPEST_UNCENSORED_ABSOLUTE_LOG10 - (-np.log10(V)))),
                            terminal_variant=variant,
                            rate_units="log10 per day",
                            V_source="SCENARIO - no deposit records a culture volume; "
                                     "T_ext is conditional on this declared value",
                            scale_tag=g["scale_tag"].iloc[0]))
    return pd.DataFrame(rows)


def _censored_fraction(D, idx):
    r = D["rows"]
    m = r["sidx"].isin(idx)
    if not m.any():
        return np.nan
    return float(r.loc[m, "censored"].fillna(False).mean())


def _delta_variant(variant, H, bt, window_days):
    if variant == "linear":
        return gap(H, bt)
    if variant == "plateau":
        return np.full(bt.shape, np.inf)
    # decelerating: b decays to zero with e-folding time = the observation window.
    # DECLARED BRACKET, NOT ESTIMATED. The corpus contains no information at all
    # about post-observation behaviour, so no fit could inform this.
    W = max(window_days, 1e-6)
    budget = bt * W
    out = np.full(bt.shape, np.inf)
    ok = (bt > 0) & (budget > H)
    out[ok] = -W * np.log(1.0 - H / budget[ok])
    return out


def _t_ext(variant, mu_last, bt, last_knot, V_mL, window):
    target = -np.log10(V_mL)
    need = mu_last - target
    if variant == "linear":
        out = np.full(bt.shape, np.inf)
        ok = bt > 0
        out[ok] = last_knot + np.maximum(need[ok] / bt[ok], 0.0)
        return out
    if variant == "plateau":
        return np.full(bt.shape, np.inf)
    W = max(window, 1e-6)
    budget = bt * W
    out = np.full(bt.shape, np.inf)
    ok = (bt > 0) & (budget > need) & (need > 0)
    out[ok] = last_knot - W * np.log(1.0 - need[ok] / budget[ok])
    out[(bt > 0) & (need <= 0)] = last_knot
    return out


def build_two_timescale(ps, D):
    ser = D["ser"]
    rows = []
    for i, r in ser.iterrows():
        j = int(r["sidx"])
        e = ps["b_first"][:, j]
        t = ps["b_tail"][:, j]
        rows.append(dict(
            deposit=r["deposit"], unit_group=r["unit_group"], state_label=r["state_label"],
            drug=r["drug"], dose_value=r["dose_value"], dose_unit=r["dose_unit"],
            early_rate_median_log10_per_day=q(e, .5),
            early_rate_q05_log10_per_day=q(e, .05), early_rate_q95_log10_per_day=q(e, .95),
            terminal_rate_median_log10_per_day=q(t, .5),
            terminal_rate_q05_log10_per_day=q(t, .05),
            terminal_rate_q95_log10_per_day=q(t, .95),
            early_rate_median_log10_per_hour=q(e, .5) / 24.0,
            terminal_rate_median_log10_per_hour=q(t, .5) / 24.0,
            ratio_early_over_terminal=(q(e, .5) / q(t, .5)) if q(t, .5) not in (0.0,) else np.nan,
            P_terminal_rate_le_0=float(np.mean(t <= 0)),
            rate_units="log10 per day unless the column name says per hour"))
    return pd.DataFrame(rows)


def empirical_two_timescale_summary():
    """The verified empirical facts the design rests on, recomputed from the data."""
    out = {}
    w = pd.read_csv(PROC / "tidy_windels.csv")
    w = w[~w["censored"]]
    early, late, nut, ld = [], [], [], []
    for ug, g in w.groupby("unit_group"):
        g = g.sort_values("time_days")
        t = g["time_days"].values * 24.0
        y = g["y_log10"].values
        if len(t) < 2:
            continue
        if t[0] == 0 and len(t) > 1:
            early.append(-(y[1] - y[0]) / (t[1] - t[0]))
        m = t >= 3.0
        if m.sum() >= 2:
            A = np.column_stack([np.ones(m.sum()), t[m]])
            c = np.linalg.lstsq(A, y[m], rcond=None)[0]
            late.append(-c[1])
            nut.append(g["state_numeric"].iloc[0])
            ld.append(np.log10(g["dose_value"].iloc[0]))
    early, late = np.array(early), np.array(late)
    out["windels_early_rate_log10_per_hour_min"] = float(early.min())
    out["windels_early_rate_log10_per_hour_max"] = float(early.max())
    out["windels_terminal_rate_log10_per_hour_p10"] = float(np.quantile(late, 0.1))
    out["windels_terminal_rate_log10_per_hour_p90"] = float(np.quantile(late, 0.9))
    out["windels_n_terminal_series"] = int(len(late))
    sr = stats.spearmanr(late, nut)
    out["windels_terminal_vs_nutrient_spearman"] = float(sr.statistic)
    out["windels_terminal_vs_nutrient_p"] = float(sr.pvalue)
    sd = stats.spearmanr(late, ld)
    out["windels_terminal_vs_log10dose_spearman"] = float(sd.statistic)
    out["windels_terminal_vs_log10dose_p"] = float(sd.pvalue)

    e = pd.read_csv(PROC / "tidy_era4tb.csv")
    e["vol"] = e["notes"].str.extract(r"plated_volume_uL=([\d.]+)")[0].astype(float)
    e["arm"] = e["unit_group"].str.split("_").str[2]
    e = e[(e["vol"] == 100.0) & (e["time_days"] >= 0) & (~e["censored"])
          & e["y_log10"].notna() & (e["arm"] != "untreated") & (e["arm"] != "inoculumTKA")]
    npos, tot, reb1, reb2, by_arm = 0, 0, 0, 0, {}
    for ug, g in e.groupby("unit_group"):
        g = g.sort_values("time_days")
        if len(g) < 3:
            continue
        t, y = g["time_days"].values, g["y_log10"].values
        A = np.column_stack([np.ones(2), t[-2:]])
        rate = -np.linalg.lstsq(A, y[-2:], rcond=None)[0][1]
        tot += 1
        arm = g["arm"].iloc[0]
        by_arm.setdefault(arm, [0, 0])
        by_arm[arm][1] += 1
        if rate <= 0:
            npos += 1
            by_arm[arm][0] += 1
        nadir = y.min()
        if y[-1] - nadir > 1:
            reb1 += 1
        if y[-1] - nadir > 2:
            reb2 += 1
    out["era4tb_treated_100uL_series_with_ge3_uncensored"] = tot
    out["era4tb_n_terminal_rate_non_positive"] = npos
    out["era4tb_P_terminal_rate_le_0_empirical"] = npos / tot if tot else np.nan
    out["era4tb_non_positive_by_arm"] = {k: f"{v[0]}/{v[1]}" for k, v in sorted(by_arm.items())}
    out["era4tb_n_rebound_gt_1_log10_from_nadir"] = reb1
    out["era4tb_n_rebound_gt_2_log10_from_nadir"] = reb2
    return out


def build_tipping_points_full(post_by_arm, D_by_arm, gap_tab):
    ps = post_by_arm["censored"]
    D = D_by_arm["censored"]
    ser = add_condition_cols(D["ser"])
    bt_by_cond = {c: ps["b_tail"][:, g["sidx"].values].ravel()
                  for c, g in ser.groupby(COND_COLS, dropna=False)}
    rows = []
    seen = set()
    base = gap_tab[(gap_tab["terminal_variant"] == "linear") & (gap_tab["bql_arm"] == "censored")]
    for _, r in base.iterrows():
        key = (r["deposit"], r["state_label"], r["drug"],
               -1 if not np.isfinite(r["dose_value"]) else r["dose_value"], r["dose_unit"])
        bt = bt_by_cond.get(key)
        if bt is None:
            continue
        for X in GAP_TARGETS_DAYS:
            need = float(required_b_tail_log10_per_day(r["H_log10_cells"], X))
            k = (key, r["V_mL"], r["plated_volume_uL"], X)
            if k in seen:
                continue
            seen.add(k)
            rows.append(dict(deposit=r["deposit"], state_label=r["state_label"],
                             drug=r["drug"], dose_value=r["dose_value"],
                             dose_unit=r["dose_unit"], V_mL=r["V_mL"],
                             plated_volume_uL=r["plated_volume_uL"],
                             H_log10_cells=r["H_log10_cells"], target_gap_days=X,
                             required_b_tail_log10_per_day=need,
                             P_b_tail_exceeds_required=float(np.mean(bt > need)),
                             rate_units="log10 per day"))
    return pd.DataFrame(rows)


def build_variance_components(mcmc):
    sm = mcmc.get_samples()
    rows = []

    def add(name, x, units, note):
        rows.append(dict(component=name, posterior_median=q(x, .5),
                         q05=q(x, .05), q95=q(x, .95), units=units, note=note))
    add("sigma_lab", np.asarray(sm["sigma_lab"]), "log10 per day",
        "between-laboratory spread in decline rate; 6 ERA4TB laboratories, one "
        "protocol, one strain")
    add("sigma_lab_a", np.asarray(sm["sigma_lab_a"]), "log10 CFU/mL",
        "between-laboratory spread in STARTING LEVEL, reported separately from the "
        "rate effect because the project's thesis is that the rate travels and the "
        "level does not")
    add("sigma_iso", np.asarray(sm["sigma_iso"]), "log10 per day",
        "between-isolate spread; 217 Vijay clinical isolates, identical protocol")
    for i, dd in enumerate(DEPOSITS):
        add(f"sigma_series_{dd}", np.asarray(sm["sigma_series"])[:, i], "log10 per day",
            "flask/series residual on the rate, this deposit")
    add("sigma_rate_hyper", np.asarray(sm["sigma_rate_hyper"]), "dimensionless",
        "the one shared hyper-variance: how much a rate moves, before the "
        "deposit-specific timescale is applied")
    add("sigma_plate", np.asarray(sm["sigma_plate"]), "log10 CFU/mL",
        "within-sample plating noise, identified directly from the four "
        "simultaneous ERA4TB platings of one sample at one visit")
    for i, d in enumerate(DEPOSITS):
        add(f"sigma_proc_{d}", np.asarray(sm["sigma_proc_d"])[:, i], "log10 units of that deposit's y",
            "process/visit-level noise")
        add(f"tau_{d}", np.asarray(sm["tau_d"])[:, i], "log10 per day",
            "random-walk step SD between adjacent segment rates; a declared "
            "SMOOTHING prior, not a mechanism")
    add("pi_era4tb", np.asarray(sm["pi_era4tb"]), "probability",
        "P(a below-limit flag means an unreadable plate rather than a culture "
        "below the limit), identified from the 125 self-contradicting flags")
    return pd.DataFrame(rows)


# ===========================================================================
# 9. MAIN
# ===========================================================================
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--smoke", action="store_true",
                    help="exercise every code path at useless MCMC settings")
    ap.add_argument("--warmup", type=int, default=1000)
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--val-warmup", type=int, default=1000)
    ap.add_argument("--val-draws", type=int, default=1000)
    ap.add_argument("--val-chains", type=int, default=4)
    args = ap.parse_args()
    if args.quick:
        args.warmup = args.draws = 150
        args.chains = 2
        args.val_warmup = args.val_draws = 100
        args.val_chains = 1
    if args.smoke:
        args.quick = True
        args.warmup = args.draws = 15
        args.chains = 1
        args.val_warmup = args.val_draws = 15
        args.val_chains = 1

    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    man = ensure_manifest()
    t_start = time.time()

    print("== 0. the exact, fit-free table, written before anything is fitted ==")
    hb = write_hidden_burden()
    print(hb[hb["V_mL"] == 10.0][["plated_volume_uL", "limit_log10", "V_mL",
                                  "H_log10_cells", "H_cells"]].to_string(index=False))

    print("\n== 1. build design ==")
    D = build_design()
    I = make_model_inputs(D)
    _setup_numpyro(max(args.chains, args.val_chains, 2))
    print(json.dumps({k: v for k, v in D["log"].items()
                      if not isinstance(v, list)}, indent=2, default=str))

    print("\n== 2. prior predictive (must admit sterilisation AND regrowth) ==")
    pp = prior_predictive(I)
    print(json.dumps(pp, indent=2))

    print("\n== 3. identifiability gate (exp25) ==")
    gate_tab = identifiability_gate(quick=args.quick)
    gate_tab.to_csv(TABLES / "ctbp_identifiability_boundary.csv", index=False)
    gate = gate_boundary(gate_tab)
    print(gate_tab.to_string(index=False))
    print("GATE:", json.dumps(gate, indent=2))

    print("\n== 4. main fit (all four deposits), BQL arm = censored ==")
    post, Darm, diag = {}, {}, {}
    Da = build_design(bql_arm="censored")
    Ia = make_model_inputs(Da)
    mcmc_main, el = run_mcmc(Ia, SEED, warmup=args.warmup, draws=args.draws,
                             chains=args.chains)
    post["censored"] = posterior_series(mcmc_main, Da)
    Darm["censored"] = Da
    D, I = Da, Ia
    diag["censored"] = diagnostics(mcmc_main)
    diag["censored"]["seconds"] = el
    print(f"   joint  {el:7.1f}s  max R-hat {diag['censored']['max_r_hat']:.3f} "
          f"min ESS {diag['censored']['min_ess']:.0f} gate={diag['censored']['gate_pass']}")

    # ---- coupling check -----------------------------------------------------
    # Every regression coefficient, random-walk step SD, process SD, intercept
    # mean and intercept SD in this model is deposit-specific. The ONLY thing the
    # four deposits share is sigma_rate_hyper. Every refit below is therefore
    # scoped to the deposit whose held-out data it predicts, which is what makes
    # nineteen refits affordable at all. That substitution is only legitimate if
    # the coupling really is negligible, so it is MEASURED here, not asserted.
    print("\n== 4b. coupling check: ERA4TB alone vs ERA4TB inside the joint fit ==")
    De = build_design(bql_arm="censored", deposits=("era4tb",))
    Ie = make_model_inputs(De)
    me, ele = run_mcmc(Ie, SEED, warmup=args.val_warmup, draws=args.val_draws,
                       chains=args.val_chains)
    pse = posterior_series(me, De)
    joint_era = post["censored"]["b_tail"][:, (Da["ser"]["deposit"] == "era4tb").values]
    coupling = dict(
        joint_era4tb_b_tail_median_log10_per_day=q(joint_era.ravel(), .5),
        era4tb_only_b_tail_median_log10_per_day=q(pse["b_tail"].ravel(), .5),
        joint_P_b_tail_le_0=float(np.mean(joint_era <= 0)),
        era4tb_only_P_b_tail_le_0=float(np.mean(pse["b_tail"] <= 0)),
        seconds=ele,
        note="if these differ materially the scoped refits below are not "
             "interchangeable with the joint fit and must be read as such")
    print(json.dumps(coupling, indent=2))

    # ---- BQL sensitivity arms, ERA4TB-scoped -------------------------------
    # The below-limit flag exists only in ERA4TB, so arms 2 and 3 change no other
    # deposit's data by a single row. They are refitted ERA4TB-only, and the
    # other three deposits appear in the gap table under the primary arm alone.
    print("\n== 4c. BQL sensitivity arms (ERA4TB-scoped refits) ==")
    for arm in ("reclassified", "dropped"):
        Db = build_design(bql_arm=arm, deposits=("era4tb",))
        Ib = make_model_inputs(Db)
        mb, elb = run_mcmc(Ib, SEED, warmup=args.val_warmup, draws=args.val_draws,
                           chains=args.val_chains)
        post[arm] = posterior_series(mb, Db)
        Darm[arm] = Db
        diag[arm] = diagnostics(mb)
        diag[arm]["seconds"] = elb
        diag[arm]["scope"] = "era4tb only"
        print(f"   {arm:14s} {elb:7.1f}s  max R-hat {diag[arm]['max_r_hat']:.3f} "
              f"min ESS {diag[arm]['min_ess']:.0f}")

    sm_main = mcmc_main.get_samples()
    sigma_plate_med = float(np.median(np.asarray(sm_main["sigma_plate"])))
    era_spread = _era4tb_within_visit_spread()
    sigma_check = dict(
        sigma_plate_posterior_median_log10=sigma_plate_med,
        observed_within_sample_visit_spread_median_log10=era_spread["median"],
        observed_within_sample_visit_spread_p90_log10=era_spread["p90"],
        n_multi_plating_visits=era_spread["n"],
        floor_stated_in_the_design=0.25,
        passes_floor=bool(sigma_plate_med >= 0.25),
        note="a fit returning an ERA4TB plating SD below about 0.25 log10 would be "
             "fitting noise: the four platings of ONE sample at ONE visit already "
             "disagree by this much")
    print("\n== 4d. ERA4TB plating-noise floor check ==")
    print(json.dumps(sigma_check, indent=2))

    print("\n== 5. V7 negative controls (reported first, as required) ==")
    v7 = v7_negative_controls(mcmc_main, D, I)
    print(f"   untreated ERA4TB series: {v7['n_untreated_series']}, "
          f"fraction with negative median b_tail (i.e. growing): "
          f"{v7['fraction_untreated_with_negative_median_b_tail']:.3f}")
    print(f"   mean P(T_ext = infinity) in untreated flasks: "
          f"{v7['mean_P_T_ext_infinite_untreated']:.3f}")
    print(f"   pi_era4tb posterior median: {v7['pi_era4tb_posterior_median']:.3f}")
    print(f"   flask x volume series returning above their limit: "
          f"{v7['n_flask_by_volume_series_returning_above_limit']}")

    val_kw = dict(warmup=args.val_warmup, draws=args.val_draws, chains=args.val_chains)
    print("\n== 6. V1 plate holdout - THE GATE ==")
    extra = {}
    v1, v1_calib = v1_plate_holdout(SEED, val_kw, extra)
    print(json.dumps(v1, indent=2))

    print("\n== 7. V2 leave-one-laboratory-out ==")
    v2, v2_calib = v2_leave_one_lab_out(SEED, val_kw, quick=args.smoke)
    print(v2.to_string(index=False))

    print("\n== 8. V3 leave-one-Windels-cell-out ==")
    v3 = v3_windels_cells(SEED, quick=args.quick)
    print(v3.describe().to_string())

    print("\n== 9. V4 Vijay external calibration ==")
    v4 = v4_vijay(SEED, val_kw)
    print(json.dumps(v4, indent=2))

    print("\n== 10. V5 censoring-mechanism sensitivity ==")
    v5 = {}
    # Each arm is refitted on the deposit whose data it actually changes, and
    # compared against that same deposit's primary fit, so it is like for like.
    arms = [("vijay_left_censor_only", "vijay",
             dict(vijay_left_censor_only=True, deposits=("vijay",))),
            ("windels_zeros_censored_at_bound", "windels",
             dict(windels_censor_zeros=True, deposits=("windels",))),
            ("kaur_declared_external_floor_1p60", "kaur",
             dict(kaur_floor=man["kaur_sensitivity_floor_log10_cfu_per_mL"],
                  deposits=("kaur",))),
            ("kaur_without_baseline_anchor", "kaur",
             dict(add_kaur_anchor=False, deposits=("kaur",)))]
    ref = {}
    for dep in ("vijay", "windels", "kaur"):
        mref = (Darm["censored"]["ser"]["deposit"] == dep).values
        ref[dep] = post["censored"]["b_tail"][:, mref].ravel()
    for name, dep, kw in arms:
        Ds = build_design(**kw)
        Is = make_model_inputs(Ds)
        ms, el = run_mcmc(Is, SEED + 21, **val_kw)
        pss = posterior_series(ms, Ds)
        bt = pss["b_tail"].ravel()
        v5[name] = dict(deposit=dep,
                        arm_b_tail_median_log10_per_day=q(bt, .5),
                        primary_b_tail_median_log10_per_day=q(ref[dep], .5),
                        arm_P_b_tail_le_0=float(np.mean(bt <= 0)),
                        primary_P_b_tail_le_0=float(np.mean(ref[dep] <= 0)),
                        seconds=el)
        print(f"   {name:40s} [{dep}] b_tail {q(bt,.5):+.4f} vs primary "
              f"{q(ref[dep],.5):+.4f}   P(inf) {np.mean(bt<=0):.3f} vs "
              f"{np.mean(ref[dep]<=0):.3f}")
    for arm in post:
        bt = post[arm]["b_tail"][:, (Darm[arm]["ser"]["deposit"] == "era4tb").values].ravel()
        v5[f"bql_{arm}"] = dict(deposit="era4tb",
                                arm_b_tail_median_log10_per_day=q(bt, .5),
                                primary_b_tail_median_log10_per_day=q(
                                    post["censored"]["b_tail"][
                                        :, (Darm["censored"]["ser"]["deposit"]
                                            == "era4tb").values].ravel(), .5),
                                arm_P_b_tail_le_0=float(np.mean(bt <= 0)))
        print(f"   bql_{arm:36s} b_tail {q(bt,.5):+.4f}  P(inf) {np.mean(bt<=0):.3f}")
    v5["V_mL_10fold_either_way"] = dict(
        note="Delta scales as H = L + log10(V), so a 10-fold change in V moves "
             "the gap by exactly 1/b_tail days at every condition. The full "
             "surface over V in {1, 10, 100, 1000} mL is already in "
             "ctbp_gap_by_condition.csv; this arm is exact arithmetic and needs "
             "no refit.")

    print("\n== 11. V6 simulation-based calibration of the estimator ==")
    sbc_kw = dict(warmup=max(300, args.val_warmup // 2),
                  draws=max(300, args.val_draws // 2), chains=2)
    v6h = v6_sbc_hierarchical(me, De, Ie, SEED, sbc_kw, quick=args.smoke)
    print("   hierarchical SBC (refits the whole ERA4TB model): "
          f"bias {v6h['b_tail_mean_bias_log10_per_day']:+.4f} log10/day, "
          f"90% coverage {v6h['b_tail_nominal_90_coverage']:.3f}, "
          f"P(inf) true {v6h['P_inf_true_mean']:.3f} vs est "
          f"{v6h['P_inf_est_mean']:.3f}")
    v6 = v6_sbc(SEED, val_kw, quick=args.smoke)
    v6["hierarchical"] = v6h
    print("   single-series estimator (the one the gate uses):")
    print(json.dumps({k: v for k, v in v6.items() if k != "hierarchical"}, indent=2))

    print("\n== 12. tables ==")
    gap_tab = build_gap_table(post, Darm, gate)
    gap_tab.to_csv(TABLES / "ctbp_gap_by_condition.csv", index=False)

    tt = build_two_timescale(post["censored"], Darm["censored"])
    emp = empirical_two_timescale_summary()
    for k, v in emp.items():
        tt[f"corpus_{k}"] = json.dumps(v) if isinstance(v, dict) else v
    tt.to_csv(TABLES / "ctbp_two_timescale.csv", index=False)

    # in-sample calibration rows for every ERA4TB plating, plus the holdout folds
    ins = _insample_calibration(mcmc_main, D, I)
    calib = pd.concat([ins, v1_calib, v2_calib], ignore_index=True)
    calib.to_csv(TABLES / "ctbp_tlod_calibration.csv", index=False)

    tp = build_tipping_points_full(post, Darm, gap_tab)
    tp.to_csv(TABLES / "ctbp_tipping_points.csv", index=False)

    vc = build_variance_components(mcmc_main)
    vc.to_csv(TABLES / "ctbp_variance_components.csv", index=False)

    vs = _validation_summary(v1, v2, v3, v4, v5, v6, v7, gate)
    vs.to_csv(TABLES / "ctbp_validation_summary.csv", index=False)

    headline = _headline(gap_tab, post, Darm, ins, v1, emp)
    print("\n== 13. headline ==")
    for k, v in headline.items():
        print(f"   {k}: {v}")

    receipt = dict(
        script="src/experiments/exp24_clearance_prediction.py",
        utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        wall_seconds=round(time.time() - t_start, 1),
        software=dict(python=platform.python_version(), numpy=np.__version__,
                      pandas=pd.__version__, scipy=scipy.__version__,
                      numpyro=__import__("numpyro").__version__,
                      jax=__import__("jax").__version__, platform=platform.platform()),
        seeds=dict(master=SEED, mcmc_main=SEED, v1=SEED + 11, v2=SEED + 100,
                   v4=SEED + 55, v5=SEED + 21, v6=SEED + 9, gate=SEED),
        mcmc=dict(warmup=args.warmup, draws=args.draws, chains=args.chains,
                  target_accept=0.9, max_tree_depth=12,
                  validation_warmup=args.val_warmup, validation_draws=args.val_draws,
                  validation_chains=args.val_chains,
                  note="validation and sensitivity refits use the same chain "
                       "length as the primary fit"),
        LN10=LN10,
        rate_axis_of_every_reported_field="log10 per day unless a column name ends "
                                          "in per_hour; no natural-log rate is emitted",
        declared_V_mL=man["culture_volume_mL"],
        V_provenance=man["culture_volume_provenance"],
        V_scenario_grid=V_GRID_ML,
        build_log={k: v for k, v in D["log"].items()},
        prior_predictive=pp,
        convergence=diag,
        era4tb_plating_noise_floor_check=sigma_check,
        coupling_check_joint_vs_era4tb_only=coupling,
        scoped_refit_declaration=(
            "Every validation and sensitivity refit is scoped to the deposit "
            "whose data it changes or predicts. That is legitimate because every "
            "regression coefficient, random-walk SD, process SD and intercept "
            "hyper-parameter in this model is deposit-specific; the only shared "
            "parameter is sigma_rate_hyper. The size of that coupling is measured "
            "in coupling_check_joint_vs_era4tb_only rather than assumed."),
        identifiability_gate=gate,
        V7_negative_controls=v7,
        V1_plate_holdout=v1,
        V2_leave_one_lab_out=v2.to_dict("records"),
        V3_windels_leave_one_cell_out=dict(
            n_cells=int(len(v3)),
            median_rmse_log10=float(v3["rmse_log10"].median()) if len(v3) else None,
            n_extrapolation_cells=int(v3["is_extrapolation_not_holdout"].sum()) if len(v3) else 0,
            substitution="Windels-only submodel; declared, see docstring of v3_windels_cells"),
        V4_vijay=v4,
        V5_sensitivity=v5,
        V6_sbc=v6,
        empirical_two_timescale=emp,
        headline=headline,
        tables_written=[str(p.relative_to(ROOT)).replace("\\", "/") for p in [
            TABLES / "ctbp_hidden_burden.csv", TABLES / "ctbp_gap_by_condition.csv",
            TABLES / "ctbp_tlod_calibration.csv", TABLES / "ctbp_two_timescale.csv",
            TABLES / "ctbp_tipping_points.csv", TABLES / "ctbp_variance_components.csv",
            TABLES / "ctbp_identifiability_boundary.csv",
            TABLES / "ctbp_validation_summary.csv"]],
        implementation_deviations=[
            "Windels rate priors carry a deposit-specific scale (x24). A single "
            "Normal(0, 0.5) log10-per-day prior is about 300 prior SDs from an "
            "aminoglycoside killing six logs in an hour; using it unchanged would "
            "have been the prior fighting the data, not weak information.",
            "sigma_series is per deposit, drawn from one shared hyper-variance "
            "(sigma_rate_hyper), rather than one number shared across four "
            "deposits whose timescales differ 72-fold.",
            "Observation-scale priors are InverseGamma(3, 0.5), not HalfNormal(0, "
            "0.5). Under the Vijay interval likelihood the maximum-likelihood "
            "sigma is exactly zero, at which the interval term becomes a step "
            "function with unbounded curvature; a HalfNormal, whose density peaks "
            "at zero, drove the sampler there and NUTS could not start.",
            "The laboratory effect on the INTERCEPT (u_lab_a, sigma_lab_a) is a "
            "separate parameter from the laboratory effect on the RATE (u_lab, "
            "sigma_lab). The brief wrote u_lab in both places; keeping them "
            "separate is what lets the rate-travels/level-does-not comparison be "
            "made at all.",
            "Each series' terminal segment is the last segment that CONTAINS an "
            "observation, not the deposit's last knot. Lab B stops at day 14 and "
            "lab F at day 15, so a b_tail fitted on the deposit-level [14, 21] "
            "segment would have been the random-walk prior wearing the name of the "
            "one number the whole T_ext claim rests on.",
            "Vijay interval edges are +/- 30 log10 rather than +/- infinity: the "
            "derivative of an infinite edge is 0 * inf and the sampler will not "
            "start. 30 log10 is unreachable by any culture.",
            "Every validation and sensitivity refit is scoped to the deposit whose "
            "data it changes or predicts; the size of the resulting approximation "
            "is measured in coupling_check_joint_vs_era4tb_only.",
            "V3 uses a Windels-only least-squares surface for the 34 leave-one-"
            "cell-out folds rather than 34 refits of the full hierarchical model.",
            "V4 is leave-one-culture-age-out WITHIN Vijay (fit 15 d + 30 d, predict "
            "60 d). A model fitted without Vijay has no Vijay coefficients at all, "
            "because every regression coefficient in this model is deposit-"
            "specific, so a pure external prediction of Vijay is not defined.",
            "Kaur treated arms get an explicit t=0 anchor row carrying the sheet's "
            "single day-0 control reading, flagged in the row's notes and counted "
            "in the build log. Without it a treated intracellular series has two "
            "readings and no baseline. V5 refits Kaur without it.",
            "Terminal variant (ii), decelerating, is a DECLARED bracket - the "
            "terminal rate decays to zero with an e-folding time equal to the "
            "series' own observation window - not a fitted alternative. No refit "
            "could inform it: the corpus contains no information whatsoever about "
            "behaviour after the last visit.",
            "Delivered as one script, src/experiments/exp24_clearance_prediction.py, "
            "rather than exp24 through exp28, following the instruction given. The "
            "table names are the ones the brief specified (ctbp_*.csv).",
            "src/audit_claims.py was NOT extended to recompute these numbers; that "
            "is outstanding work, not something this run did.",
        ],
        what_must_not_be_claimed=[
            "T_ext was measured, estimated from data, or validated. It was not and "
            "cannot be: no deposit contains a single reading below its own limit and "
            "the deepest uncensored absolute reading anywhere is 1.000 log10 CFU/mL.",
            "A single headline gap in days. Delta has infinite mean and undefined "
            "variance; only conditional quantiles are reported.",
            "Any T_ext without a declared V. No deposit records a culture volume.",
            "A starting-density effect on the rate. n0 is a designed variable nowhere.",
            "A concentration-response curve, EC50, Emax or Hill exponent.",
            "That the four physiological-state axes share a coordinate. They do not.",
            "That E[N] < 1 is sterility. Under a Poisson bridge it is 0.368.",
            "That V6 validates T_ext. It validates the estimator given the model.",
            "That the piecewise-linear random walk is a mechanism or a persister "
            "compartment. It is a declared smoothing prior.",
            "Anything about a patient. This is an in vitro flask at constant "
            "concentration."],
    )
    (RECEIPTS / "exp24_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str), encoding="utf-8")
    print(f"\nreceipt -> results/receipts/exp24_receipt.json  "
          f"({receipt['wall_seconds']}s)")
    return 0


def _era4tb_within_visit_spread():
    """max-minus-min log10 across the platings of one sample at one visit.

    This is measurement noise inside a single flask at a single visit, and it
    sets a floor on any residual variance a kill model can honestly achieve on
    this deposit.
    """
    d = pd.read_csv(PROC / "tidy_era4tb.csv")
    d = d[d["y_log10"].notna() & ~d["censored"] & (d["time_days"] >= 0)]
    g = d.groupby(["unit_group", "time_days"])["y_log10"]
    spread = (g.max() - g.min())[g.count() >= 2]
    return dict(median=float(spread.median()), p90=float(spread.quantile(0.9)),
                n=int(len(spread)))


def _insample_calibration(mcmc, D, I):
    rows = D["rows"]
    m = (rows["deposit"] == "era4tb").values
    sm = mcmc.get_samples()
    b = np.asarray(sm["b"]); a = np.asarray(sm["a"])
    si = I["sidx"][m]
    W = I["W"][m]
    mu = a[:, si] - np.einsum("rm,drm->dr", W, b[:, si, :])
    sp = np.asarray(sm["sigma_plate"])[:, None]
    proc = np.asarray(sm["sigma_proc_d"])[:, 0][:, None]
    # in sample the visit-level latent density is fitted, so the residual on a
    # plate is plating noise alone
    eta = np.asarray(sm["eta_visit"])
    vi = I["visit_idx"][m]
    mu = mu + np.where(vi[None, :] >= 0, eta[:, np.clip(vi, 0, None)] * proc, 0.0)
    sd = sp * np.ones((1, mu.shape[1]))
    pi = np.asarray(sm["pi_era4tb"])[:, None]
    nd = mu.shape[0]
    th = slice(0, nd, max(1, nd // 200))
    vol = rows.loc[m, "plated_volume_uL"].values
    pb = np.array([p_blank(mu[i], sd[i], vol) for i in range(*th.indices(nd))])
    pf = pi[th][: pb.shape[0]]
    pflag = (pf + (1 - pf) * pb).mean(axis=0)
    return pd.DataFrame(dict(
        unit_group=rows.loc[m, "unit_group"].values,
        time_days=rows.loc[m, "time_days"].values,
        plated_volume_uL=vol, limit_log10=rows.loc[m, "limit_log10"].values,
        observed_blank=rows.loc[m, "censored"].fillna(False).astype(int).values,
        observed_y_log10=rows.loc[m, "y_log10"].values,
        predicted_p_blank=pflag, mu_median=np.median(mu, axis=0),
        mu_q05=np.quantile(mu, 0.05, axis=0), mu_q95=np.quantile(mu, 0.95, axis=0),
        fold="in-sample"))


def _validation_summary(v1, v2, v3, v4, v5, v6, v7, gate):
    r = []
    r.append(dict(test="V7a", split="ERA4TB untreated series, in sample",
                  metric="fraction with negative median b_tail (net growth)",
                  value=v7["fraction_untreated_with_negative_median_b_tail"],
                  threshold="expect ~1.0", passed=bool(
                      v7["fraction_untreated_with_negative_median_b_tail"] >= 0.8)))
    r.append(dict(test="V7b", split="5 censored readings in growing undrugged flasks",
                  metric="pi_era4tb posterior median",
                  value=v7["pi_era4tb_posterior_median"], threshold="none pre-registered",
                  passed=""))
    r.append(dict(test="V7d", split="ERA4TB flask x volume series",
                  metric="n series returning above their limit after touching it",
                  value=v7["n_flask_by_volume_series_returning_above_limit"],
                  threshold="none; a censored likelihood absorbs them", passed=""))
    r.append(dict(test="V1a-traj", split="same, trajectory-only prediction",
                  metric="90% posterior predictive coverage, visit effect discarded",
                  value=v1["coverage_90_trajectory_only"],
                  threshold="reported, not gated", passed=""))
    r.append(dict(test="V1a", split="fit 2.5+10 uL, predict held-out 100 uL",
                  metric="90% posterior predictive coverage", value=v1["coverage_90"],
                  threshold=f"pre-registered [{V1_COVERAGE_BAND[0]}, {V1_COVERAGE_BAND[1]}]",
                  passed=bool(V1_COVERAGE_BAND[0] <= v1["coverage_90"] <= V1_COVERAGE_BAND[1])))
    r.append(dict(test="V1b", split="same",
                  metric="predicted/observed blank rate at the deeper limit",
                  value=v1["fold_error_on_blank_rate"],
                  threshold=f"pre-registered within {V1_BLANK_RATE_FOLD}-fold",
                  passed=bool(1 / V1_BLANK_RATE_FOLD <= v1["fold_error_on_blank_rate"]
                              <= V1_BLANK_RATE_FOLD)))
    r.append(dict(test="V1c", split="same",
                  metric="predictive bias in the 1.0-2.0 log10 window",
                  value=v1["bias_in_1_to_2_log10_window"], threshold="reported, not gated",
                  passed=""))
    r.append(dict(test="V1-GATE", split="V1a and V1b together", metric="gate decision",
                  value=("PASS - Delta may be reported as an estimate"
                         if v1["gate_pass"] else
                         "FAIL - Delta is reported as a BOUND only"),
                  threshold="pre-registered before fitting", passed=bool(v1["gate_pass"])))
    for _, row in v2.iterrows():
        r.append(dict(test=f"V2 {row['fold']}", split="leave-one-laboratory-out",
                      metric="90% coverage (blank-rate pred/obs in note)",
                      value=row["coverage_90"],
                      threshold=("zero-event fold" if row["zero_event_fold"] else "none"),
                      passed=""))
    if len(v3):
        r.append(dict(test="V3", split="leave-one-Windels-cell-out",
                      metric="median RMSE log10 across held-out cells",
                      value=float(v3["rmse_log10"].median()), threshold="none", passed=""))
        ex = v3[v3["is_extrapolation_not_holdout"]]
        if len(ex):
            r.append(dict(test="V3-extrap", split="nutrient 0.95 at 200/400 ug/mL",
                          metric="median RMSE log10 (EXTRAPOLATION, not holdout)",
                          value=float(ex["rmse_log10"].median()), threshold="none", passed=""))
    r.append(dict(test="V4", split="Vijay 60 d culture age held out",
                  metric="90% coverage of the day-5 log10 drop",
                  value=v4["coverage_90"], threshold="none", passed=""))
    r.append(dict(test="V4-PIT", split="same", metric="KS statistic of the PIT",
                  value=v4["pit_ks_statistic"], threshold="none", passed=""))
    for k, val in v5.items():
        if "arm_b_tail_median_log10_per_day" not in val:
            continue
        r.append(dict(test=f"V5 {k}",
                      split=f"censoring-mechanism sensitivity ({val.get('deposit')})",
                      metric="median b_tail under this arm (log10 per day)",
                      value=val["arm_b_tail_median_log10_per_day"],
                      threshold="none; the RANGE leads the result", passed=""))
        r.append(dict(test=f"V5 {k} P(inf)", split="same",
                      metric="P(b_tail <= 0) under this arm",
                      value=val["arm_P_b_tail_le_0"], threshold="none", passed=""))
    r.append(dict(test="V6", split="SBC, single-series estimator (the gate's)",
                  metric="nominal 90% coverage of b_tail",
                  value=v6["b_tail_nominal_90_coverage"], threshold="0.90 nominal",
                  passed=""))
    if "hierarchical" in v6:
        h = v6["hierarchical"]
        r.append(dict(test="V6-hier", split="SBC, full hierarchical refit of ERA4TB",
                      metric="nominal 90% coverage of b_tail",
                      value=h["b_tail_nominal_90_coverage"], threshold="0.90 nominal",
                      passed=""))
        r.append(dict(test="V6-hier P(inf)", split="same",
                      metric="simulated P(b_tail<=0) recovered / true",
                      value=(h["P_inf_est_mean"] / h["P_inf_true_mean"]
                             if h["P_inf_true_mean"] else np.nan),
                      threshold="1.0", passed=""))
    r.append(dict(test="V6-note", split="", metric="what V6 validates",
                  value=v6["statement"], threshold="", passed=""))
    r.append(dict(test="exp25-GATE", split="simulated ERA4TB grid",
                  metric="max censored fraction at which b_tail is estimable to "
                         f"{gate.get('stated_width')} log10/day",
                  value=gate.get("max_censored_fraction_for_width"),
                  threshold="annotates every row of the gap table", passed=""))
    return pd.DataFrame(r)


def _headline(gap_tab, post, Darm, ins, v1, emp):
    base = gap_tab[(gap_tab["terminal_variant"] == "linear")
                   & (gap_tab["bql_arm"] == "censored")
                   & (gap_tab["V_mL"] == 10.0) & (gap_tab["plated_volume_uL"] == 100.0)]
    era = base[base["deposit"] == "era4tb"]
    ps = post["censored"]
    D = Darm["censored"]
    is_era = (D["ser"]["deposit"] == "era4tb").values
    bt_era = ps["b_tail"][:, is_era].ravel()
    obs = ins["observed_blank"].values
    pred = ins["predicted_p_blank"].values
    out = dict(
        H_log10_cells_100uL_in_10mL=float(hidden_burden(1.0, 10.0)),
        H_cells_100uL_in_10mL=float(10 ** hidden_burden(1.0, 10.0)),
        H_log10_cells_2p5uL_in_10mL=float(hidden_burden(float(limit_log10_from_volume(2.5)), 10.0)),
        H_cells_2p5uL_in_10mL=float(10 ** hidden_burden(float(limit_log10_from_volume(2.5)), 10.0)),
        pipette_swing_log10=float(limit_log10_from_volume(2.5) - limit_log10_from_volume(100.0)),
        P_T_ext_infinite_era4tb_posterior=float(np.mean(bt_era <= 0)),
        P_T_ext_infinite_era4tb_empirical=emp["era4tb_P_terminal_rate_le_0_empirical"],
        era4tb_conditions_with_P_inf_above_half=int((era["P_T_ext_infinite"] > 0.5).sum()),
        era4tb_n_conditions=int(len(era)),
        in_sample_brier_score_T_LOD=float(np.mean((pred - obs) ** 2)),
        in_sample_blank_rate_pred=float(pred.mean()),
        in_sample_blank_rate_obs=float(obs.mean()),
        V1_out_of_sample_coverage_90=v1["coverage_90"],
        V1_out_of_sample_rmse_log10=v1["rmse_log10"],
        V1_out_of_sample_blank_rate_pred=v1["predicted_blank_rate"],
        V1_out_of_sample_blank_rate_obs=v1["observed_blank_rate"],
        V1_gate=("PASS" if v1["gate_pass"] else "FAIL - Delta reported as a BOUND"),
    )
    fin = era[np.isfinite(era["Delta_median_days"])]
    out["era4tb_Delta_median_days_range_conditional_on_b_tail_positive"] = (
        [float(fin["Delta_median_days"].min()), float(fin["Delta_median_days"].max())]
        if len(fin) else None)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
