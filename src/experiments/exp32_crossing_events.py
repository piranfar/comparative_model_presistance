"""
The event is a crossing, not an ending, and most of the crossings are crossed back.

Run:  python -m src.experiments.exp32_crossing_events

WHY THIS TEST EXISTS. Section 3.4 of this manuscript builds a time-to-event
analysis on the ERA4TB ring trial: per flask, the first visit at which the
culture reads below the assay boundary, with flasks that never do so
right-censored at their last visit. exp17 fits it, exp24 audits the flags around
it, and the prose then reads that event as the moment the culture ended. It is
not that moment, and the deposit says so plainly: most of the series that fall
below the boundary read above it again at a later visit. What is being modelled
is a FIRST OBSERVED CROSSING BELOW THE ASSAY BOUNDARY, and nothing stronger.
Every quantity in this script is named accordingly.

The distinction is not pedantic. A first crossing has three properties that an
ending does not:

  1. It is REVERSIBLE, so a survival model that treats it as absorbing is
     describing an event that the same series undoes a few days later.
  2. Its TIME IS NOT OBSERVED. The visit schedule is 0, 1, 2, 3, 7, 10, 14, 21
     days, so a crossing recorded on day 7 happened somewhere in the four days
     since day 3. Treating it as if it happened on day 7 is a decision, and it
     is the one exp17 makes.
  3. It is a property of the PLATING as much as of the culture. Each flask is
     plated in four formats with different boundaries at the same visit, so the
     same flask crosses at four different times, or in some formats not at all.

This script measures all three.

TWO THINGS THE PROJECT'S OWN FIGURE OF 74.8 PER CENT GETS WRONG, BOTH IN ITS
OWN FAVOUR. The figure comes from grouping by (Institute, Sample, Replicate,
Volume), sorting by Time, and counting a return whenever a later reading is not
flagged below: 83 of 111 series. Reproduced exactly here, and then corrected on
two counts.

First, a reading that carries neither a count nor a flag is not evidence that
the culture was above the boundary; it is evidence that nothing was recorded.
Requiring a real reading turns 83 returns into 72 under the same key.

Second, the key itself. 684 rows share a key under it, because the deposit
contains TWO ten-microlitre formats. Both corrections are applied below and both
are reported, because the honest number matters more than the large one. Under
the plating key with a real reading required, 84 of 140 series come back, 60.0
per cent. The claim survives the correction: it is smaller and it is sound.

THE DUPLICATE KEY, AND HOW IT IS RESOLVED. Grouping the deposit by
(Institute, Sample, Replicate, Volume) and sorting by Time is the grouping this
project has used, and it gives 270 series of which 111 ever fall below the
boundary. But 684 of those rows share a key: the deposit
contains TWO ten-microlitre formats, a single drop and four drops, recorded as
Condition 2 and Condition 1 at the same Volume. Merging them interleaves two
different platings into one series, and every visit where the four-drop plate
saw colonies and the single drop did not becomes an oscillation that no culture
performed.

The rule adopted here is to put the plating format in the series key rather than
the plated volume. Under (Institute, Sample, Replicate, Condition) all readings
have distinct keys, nothing is dropped, nothing is averaged, and the two
ten-microlitre formats stay separate. Both keyings are computed and reported
side by side, because the difference between them measures how much of the
oscillation this project has quoted is an artefact of the merge.

WHAT REPLACES THE ABSORBING-STATE MODEL. Three analyses, in increasing order of
what they assume:

  A. INTERVAL-CENSORED TIME TO FIRST CROSSING. The crossing lies between the
     last visit above the boundary and the first visit below it. Weibull and
     Turnbull non-parametric maximum likelihood are fitted on those intervals
     and compared with the naive fit that pins the event to the later endpoint.
     The naive fit is not merely imprecise: it takes the upper end of every
     interval, so it is biased late by construction.

     The two non-parametric curves must be read on one convention before they
     are subtracted, and the two lifelines fitters do not use the same one: the
     Kaplan-Meier returns the survival after the drop at t, the interval-
     censored fit returns the survival before it. Subtracting what each returns
     lags the NPMLE by one step and makes it look uniformly HIGHER than the
     naive curve, which is the opposite of the truth. _npmle_survival_at
     realigns them, and the check that fixes the convention is in its docstring:
     feed both fitters the same data with no interval censoring in it and they
     must agree exactly, which they only do after the realignment. Read
     correctly the interval-censored curve sits BELOW the naive one at every
     visit at which crossings are still being recorded. A probability quoted at
     a visit day is therefore NOT immune to the correction; it is immune only
     where the curve has stopped moving.

  B. A DISCRETE-TIME TWO-STATE TRANSITION ANALYSIS, plus an explicit trajectory
     classification. This is chosen over a continuous-time multistate model and
     over Andersen-Gill deliberately. Both of those want transition TIMES, and
     the deposit supplies none: every transition is interval-censored on a grid
     whose gaps run to seven days, and a series contributes at most eleven
     visits. A Markov intensity fitted to those data would be reporting the
     visit schedule. Counted transitions between consecutive observed visits are
     what the design can support, and they answer the question directly: a state
     that is left in one visit gap this often is not a state anything stays in.

  C. A COX MODEL, KEPT ONLY AS DESCRIPTION. Every row of its output is labelled
     descriptive. Its standard errors assume independent flasks in independent
     laboratories, which this design does not have, so the intervals reported
     here come from a cluster bootstrap over laboratories and, separately, over
     flasks. The model's own intervals are printed beside them only to show how
     much they understate.

A NOTE ON THE ADJUSTMENT FOR STARTING DENSITY. exp17 adds starting density to a
Cox model on laboratory and the laboratory coefficients move. That is reported
here too, and it is reported as what it is: a statement about the covariance of
laboratory and starting density in this design, in which exp24 found laboratory
explains most of the variance in starting density. Two predictors that nearly
determine one another will always trade coefficients when one is added. Nothing
in this design licenses reading that trade as starting density accounting for
the laboratory effect, and no sentence here does.

Data: ERA4TB standardised time-kill kinetics, figshare item 19766083.

Writes:
  results/tables/exp32_recrossing.csv
  results/tables/exp32_interval_censored.csv
  results/tables/exp32_transitions.csv
  results/tables/exp32_cox_descriptive.csv
  results/receipts/exp32_receipt.json
"""
from __future__ import annotations

import json
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

# The four plating formats. Condition, not Volume, is the identity of a plating:
# the two ten-microlitre entries are a single drop and four drops, and they are
# different platings of the same sample at the same visit.
PLATING = {0: "100 uL quadruplicate",
           1: "10 uL four drops",
           2: "10 uL single drop",
           3: "2.5 uL single drop"}
MOST_SENSITIVE = 0                      # boundary 1.0 log10 CFU/mL

TREATED = ("MXF 1X MIC", "MXF 10X MIC", "INH 1X MIC", "INH 10X MIC")
# Where the survival curves are read off. Every visit the whole schedule shares,
# not a subset of it: days 14 and 21 sit in the flat tail of the 100 uL curve,
# where no further crossing is recorded and any two estimators must agree, so a
# grid made only of those days cannot detect a disagreement even if there is one.
VISIT_GRID = (1.0, 2.0, 3.0, 7.0, 10.0, 14.0, 21.0)
N_BOOT = 400
SEED = 20250906


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def load() -> pd.DataFrame:
    """Every reading, labelled above / below / not observed.

    The boundary is a property of the plating: the smallest count recorded in
    each format is exactly 1000/Volume CFU per mL, so that is the boundary used,
    per reading, as elsewhere in this project.

    Three states, not two. A reading flagged BQL is below the boundary. A
    reading carrying a count, or one flagged above the upper limit, is above it.
    A reading with neither a count nor a flag was not observed at all, and is
    skipped rather than counted as either.
    """
    d = pd.read_csv(DATA, encoding="latin-1")
    d = d[(d["Time"] >= 0) & (d["Sample"] != "Inoculum TKA")].copy()
    d["plating"] = d["Condition"].map(PLATING)
    d["boundary_log10"] = np.log10(1000.0 / d["Volume"])
    d["state"] = np.where(
        d["BQL"] == 1, "below",
        np.where(d["CFU"].notna() | (d["AQL"] == 1), "above", "not observed"))
    return d


def key_audit(d: pd.DataFrame) -> dict:
    """How bad is the duplicate key, and does the plating format resolve it?"""
    vol_key = ["Institute", "Sample", "Replicate", "Volume", "Time"]
    con_key = ["Institute", "Sample", "Replicate", "Condition", "Time"]
    v = d.groupby(vol_key).size()
    c = d.groupby(con_key).size()
    clash = d.merge(v[v > 1].rename("n").reset_index(), on=vol_key)
    return {
        "rows": int(len(d)),
        "volume_keys_with_more_than_one_row": int((v > 1).sum()),
        "rows_sharing_a_volume_key": int(len(clash)),
        "volumes_involved": sorted(clash["Volume"].unique().tolist()),
        "platings_involved": sorted(clash["plating"].unique().tolist()),
        "condition_keys_with_more_than_one_row": int((c > 1).sum()),
        "series_under_volume_key": int(
            d.groupby(["Institute", "Sample", "Replicate", "Volume"]).ngroups),
        "series_under_condition_key": int(
            d.groupby(["Institute", "Sample", "Replicate", "Condition"]).ngroups),
    }


# --------------------------------------------------------------------------
# per-series crossing and return
# --------------------------------------------------------------------------

def _one_series(g: pd.DataFrame) -> dict:
    g = g.sort_values("Time", kind="stable")
    obs = g[g["state"] != "not observed"]
    t = obs["Time"].to_numpy(float)
    s = obs["state"].to_numpy()
    below = s == "below"

    # The looser rule this project has used elsewhere: a series has come back if
    # any LATER reading is simply not flagged below, whether or not it carries a
    # count. Readings with neither a count nor a flag qualify under it, so it
    # counts more returns than the rule used here, which needs a real reading.
    sa = g["state"].to_numpy()
    lb = sa == "below"
    loose = bool(lb.any() and (sa[int(np.argmax(lb)) + 1:] != "below").any())

    # "Starting density" is the mean of the quantified readings at day 0 or day
    # 1 in this series' own plating. It is worth knowing which of the two it
    # came from, because the deposit does not carry a day-zero reading for every
    # laboratory: where day zero is missing the value is a day-ONE reading, taken
    # after twenty-four hours of drug. The provenance is recorded per series so
    # that the covariate cannot be read as an inoculum without checking.
    quant = g[(g["state"] == "above") & g["CFUlog10"].notna()]
    early = quant[quant["Time"] <= 1]
    start = float(early["CFUlog10"].mean()) if len(early) else np.nan

    down = int(((s[:-1] == "above") & (s[1:] == "below")).sum()) if len(s) > 1 else 0
    up = int(((s[:-1] == "below") & (s[1:] == "above")).sum()) if len(s) > 1 else 0

    rec = {
        "n_rows": int(len(g)),
        "n_visits_observed": int(len(obs)),
        "n_visits_not_observed": int((g["state"] == "not observed").sum()),
        "last_visit_day": float(t[-1]) if len(t) else np.nan,
        "start_log10": start,
        "start_uses_day_zero": bool((early["Time"] == 0).any()),
        "start_n_early_readings": int(len(early)),
        "day_zero_log10": (float(early.loc[early["Time"] == 0, "CFUlog10"].mean())
                           if (early["Time"] == 0).any() else np.nan),
        "day_one_log10": (float(early.loc[early["Time"] == 1, "CFUlog10"].mean())
                          if (early["Time"] == 1).any() else np.nan),
        "ever_crossed_below": bool(below.any()),
        # A series can read below at its FIRST observed visit, in which case no
        # above-to-below step was ever seen: the culture was never watched above
        # its own boundary in this plating. It is still counted as having crossed
        # -- it is below, and the crossing must have happened before the first
        # look -- but the crossing itself is an inference from a single reading,
        # not something observed, and the count is carried so it can be excluded.
        "first_observed_visit_below": bool(below.any() and below[0]),
        "n_crossings_below": down,
        "n_returns_above": up,
        "oscillates_more_than_once": bool(up >= 2),
        "terminal_state": str(s[-1]) if len(s) else "not observed",
        "returned_under_loose_rule": loose,
    }
    if not below.any():
        rec.update({"first_crossing_day": np.nan,
                    "last_day_above_before_crossing": np.nan,
                    "returned_above": False, "day_of_first_return": np.nan,
                    "days_below_before_return": np.nan,
                    "longest_run_below_days": np.nan})
        return rec

    i = int(np.argmax(below))
    rec["first_crossing_day"] = float(t[i])
    rec["last_day_above_before_crossing"] = float(t[i - 1]) if i > 0 else np.nan
    back = np.flatnonzero(s[i + 1:] == "above")
    if back.size:
        j = i + 1 + int(back[0])
        rec.update({"returned_above": True,
                    "day_of_first_return": float(t[j]),
                    "days_below_before_return": float(t[j] - t[i])})
    else:
        rec.update({"returned_above": False, "day_of_first_return": np.nan,
                    "days_below_before_return": np.nan})

    # The longest unbroken stretch of visits reading below, in days.
    longest, run_start = 0.0, None
    for a in range(len(s)):
        if s[a] == "below":
            if run_start is None:
                run_start = t[a]
            longest = max(longest, t[a] - run_start)
        else:
            run_start = None
    rec["longest_run_below_days"] = float(longest)
    return rec


def series_table(d: pd.DataFrame, by_volume: bool = False) -> pd.DataFrame:
    """One row per series. A series is one flask followed in one plating format.

    With by_volume the two ten-microlitre formats are merged, which is the
    keying this project has used and which this script exists partly to correct.
    """
    unit = "Volume" if by_volume else "Condition"
    rows = []
    for (inst, arm, rep, u), g in d.groupby(["Institute", "Sample", "Replicate", unit]):
        rec = {"institute": inst, "arm": arm, "replicate": int(rep)}
        if by_volume:
            rec["plating"] = "volume key, formats merged"
            rec["plated_volume_ul"] = float(u)
        else:
            rec["plating"] = PLATING[int(u)]
            rec["plated_volume_ul"] = float(g["Volume"].iloc[0])
        rec["boundary_log10"] = float(g["boundary_log10"].iloc[0])
        rec.update(_one_series(g))
        rows.append(rec)
    return pd.DataFrame(rows)


def _flask_id(t: pd.DataFrame) -> pd.Series:
    return t["institute"] + "|" + t["arm"] + "|" + t["replicate"].astype(str)


def recrossing_summary(t: pd.DataFrame) -> dict:
    cross = t[t["ever_crossed_below"]]
    ret = cross[cross["returned_above"]]
    dd = ret["days_below_before_return"].dropna()
    # The series is not the independent unit. Each flask is plated in several
    # formats and contributes a series in each, so the proportions below are
    # computed over correlated units. The flask counts are carried beside them
    # for the same reason the Cox model below gets a clustered interval: the
    # denominator is not 360 independent experiments.
    f_all, f_cross, f_ret = (_flask_id(t), _flask_id(cross), _flask_id(ret))
    return {
        "n_series": int(len(t)),
        "n_flasks": int(f_all.nunique()),
        "n_flasks_with_a_crossing_series": int(f_cross.nunique()),
        "n_flasks_with_a_returning_series": int(f_ret.nunique()),
        "n_first_observed_visit_already_below": int(
            t["first_observed_visit_below"].sum()),
        "n_ever_crossed_below": int(len(cross)),
        "n_returned_above": int(len(ret)),
        "n_returned_under_loose_rule": int(cross["returned_under_loose_rule"].sum()),
        "fraction_of_crossers_returning":
            float(len(ret) / len(cross)) if len(cross) else np.nan,
        "n_oscillating_more_than_once": int(t["oscillates_more_than_once"].sum()),
        "n_series_ending_below": int((t["terminal_state"] == "below").sum()),
        "days_below_before_return": {
            "min": float(dd.min()) if len(dd) else np.nan,
            "q25": float(dd.quantile(0.25)) if len(dd) else np.nan,
            "median": float(dd.median()) if len(dd) else np.nan,
            "q75": float(dd.quantile(0.75)) if len(dd) else np.nan,
            "max": float(dd.max()) if len(dd) else np.nan,
        },
        "n_returning_within_three_days": int((dd <= 3).sum()) if len(dd) else 0,
        "median_first_crossing_day":
            float(cross["first_crossing_day"].median()) if len(cross) else np.nan,
    }


def recrossing_by(t: pd.DataFrame, col: str) -> pd.DataFrame:
    rows = []
    for k, g in t.groupby(col):
        c = g[g["ever_crossed_below"]]
        r = c[c["returned_above"]]
        rows.append({
            "stratum_kind": col, "stratum": str(k), "n_series": int(len(g)),
            "n_crossed": int(len(c)), "n_returned": int(len(r)),
            "fraction_of_crossers_returning":
                float(len(r) / len(c)) if len(c) else np.nan,
            "n_oscillating_more_than_once": int(g["oscillates_more_than_once"].sum()),
            "median_first_crossing_day":
                float(c["first_crossing_day"].median()) if len(c) else np.nan,
            "median_days_below_before_return":
                float(r["days_below_before_return"].median()) if len(r) else np.nan,
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# A. interval-censored time to the first crossing
# --------------------------------------------------------------------------

def event_frame(t: pd.DataFrame) -> pd.DataFrame:
    """Bounds on the time of the first crossing, one row per series.

    Crossed: the crossing happened after the last visit that read above the
    boundary and no later than the first visit that read below it. Never
    crossed: right censored at the last observed visit, upper bound infinite.
    A series whose first observed visit already reads below has lower bound
    zero, the start of the experiment.
    """
    e = t.copy()
    e["lower"] = np.where(e["ever_crossed_below"],
                          e["last_day_above_before_crossing"].fillna(0.0),
                          e["last_visit_day"])
    e["upper"] = np.where(e["ever_crossed_below"], e["first_crossing_day"], np.inf)
    e["event"] = e["ever_crossed_below"].astype(int)
    # The naive endpoint this project has used: the event is pinned to the visit
    # at which it was noticed, which is always the LATER end of the interval.
    e["naive_time"] = np.where(e["event"] == 1, e["upper"], e["lower"])
    return e


def _weibull_interval(lower, upper):
    from lifelines import WeibullFitter
    w = WeibullFitter()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        w.fit_interval_censoring(np.asarray(lower, float), np.asarray(upper, float))
    return w


def _weibull_naive(time, event):
    from lifelines import WeibullFitter
    w = WeibullFitter()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        w.fit(np.asarray(time, float), np.asarray(event, int))
    return w


def _npmle_survival_at(tb, t: float) -> tuple[float, bool]:
    """Turnbull survival at t, on the SAME convention as Kaplan-Meier.

    The two lifelines estimators are indexed differently and comparing what
    each returns compares two different quantities. KaplanMeierFitter.predict
    returns S(t), the survival AFTER the drop at t. The interval-censored fit
    indexes its output by the right endpoints of the NPMLE support intervals
    and each row holds the survival that stood BEFORE the drop at that row, so
    predict returns S(t-). On a decreasing curve that lag makes the NPMLE look
    uniformly higher than the Kaplan-Meier, by roughly the size of one step.

    Checked against a case whose answer is known independently. Give both
    fitters the SAME data with no interval censoring in it at all: exact events
    at days 1, 1, 2, 2 and six observations censored at day 10. The two must
    then agree exactly. Kaplan-Meier gives S(1) = 0.8 and S(2) = 0.6. The NPMLE
    rows read 1.0 at 1, 0.8 at 2 and 0.6 at 10 -- every value one row late.
    Reading the row at the first index STRICTLY GREATER than t recovers 0.8 and
    0.6 and makes the two comparable. That is what this function does.

    The NPMLE is a bracket wherever the data do not identify it. The upper
    estimate is returned and the second element of the pair records whether the
    bracket had closed at that point, so an unidentified reading cannot be
    quoted as though it were a number.
    """
    sf = tb.survival_function_
    idx = sf.index
    later = idx[idx > t]
    r = idx[-1] if len(later) == 0 else later[0]
    hi = float(sf.loc[r, "NPMLE_estimate_upper"])
    lo = float(sf.loc[r, "NPMLE_estimate_lower"])
    return hi, bool(np.isclose(hi, lo))


def interval_vs_naive(e: pd.DataFrame, label: str) -> dict:
    """Fit both treatments of the same crossings and put them side by side.

    One series in the deposit already reads below its boundary at the day-zero
    visit, so its crossing is bounded only by the interval (0, 0]: it happened
    before the experiment's first look. No clock can express that, and it is
    dropped from the time-to-event fits rather than being moved to a day it was
    not observed on. The count of such series is carried in the output.
    """
    from lifelines import KaplanMeierFitter
    n_all = int(len(e))
    zero = e[(e["event"] == 1) & (e["upper"] <= 0)]
    e = e.drop(zero.index)
    n, k = int(len(e)), int(e["event"].sum())
    if k < 3:
        return {"stratum": label, "n_series": n, "n_crossed": k,
                "n_series_before_exclusions": n_all,
                "n_excluded_already_below_at_day_zero": int(len(zero)),
                "n_crossed_never_observed_above_first": int(
                    e.loc[e["event"] == 1, "first_observed_visit_below"].sum()),
                "note": "fewer than three crossings; not fitted"}

    # THE INTERVAL IS HALF-OPEN, AND LIFELINES READS IT AS CLOSED.
    # `lower` is the last visit at which the culture was counted ABOVE its own
    # floor. The crossing therefore happened strictly after that visit: the
    # interval is (lower, upper], not [lower, upper]. lifelines' Turnbull builds
    # its support from closed intervals, so passing the raw pair lets probability
    # mass land ON a day the series was observed above the floor -- and because
    # every series shares the visit grid, one series' `lower` is another's
    # `upper`, so those days are exactly where the mass goes. Nudging the lower
    # bound by one floating-point step excludes it without inventing a gap: the
    # Turnbull support intervals become the visit gaps themselves, and every
    # crossing's mass is uniquely assigned.
    #
    # It matters only for the NPMLE, which places atoms. The Weibull fits use
    # S(lower) - S(upper) and a one-ULP shift is invisible to them; they take the
    # same arrays so the two fits are answering the same question.
    lower_open = np.nextafter(np.asarray(e["lower"], float),
                              np.asarray(e["upper"], float))
    upper = np.asarray(e["upper"], float)

    wi = _weibull_interval(lower_open, upper)
    wn = _weibull_naive(e["naive_time"], e["event"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        km = KaplanMeierFitter().fit(e["naive_time"], e["event"])
        tb = KaplanMeierFitter().fit_interval_censoring(lower_open, upper)

    width = e.loc[e["event"] == 1, "upper"] - e.loc[e["event"] == 1, "lower"]
    last = float(e["last_visit_day"].max())
    row = {"stratum": label, "n_series": n, "n_crossed": k, "note": "",
           "n_series_before_exclusions": n_all,
           "n_excluded_already_below_at_day_zero": int(len(zero)),
           # Of the crossings fitted, these were below at the series' first
           # observed visit: no above-to-below step was seen, and the interval
           # (0, first visit] is an assumption that the crossing happened in the
           # unwatched window before the experiment was first read. Both fits
           # carry them, so the comparison between them is like for like, but
           # they are a real share of the early mass and are counted here.
           "n_crossed_never_observed_above_first": int(
               e.loc[e["event"] == 1, "first_observed_visit_below"].sum()),
           "last_visit_day": last,
           "weibull_interval_scale_days": float(wi.lambda_),
           "weibull_interval_shape": float(wi.rho_),
           "weibull_naive_scale_days": float(wn.lambda_),
           "weibull_naive_shape": float(wn.rho_),
           "median_interval_width_days": float(width.median()),
           "max_interval_width_days": float(width.max())}
    for p in (10, 25, 50):
        ti = float(wi.percentile(1 - p / 100))
        tn = float(wn.percentile(1 - p / 100))
        row[f"weibull_interval_t{p}_days"] = ti
        row[f"weibull_naive_t{p}_days"] = tn
        row[f"shift_t{p}_days"] = ti - tn
        # Most series never cross, so the upper quantiles sit past the end of
        # the experiment. A quantile there is a property of the Weibull tail,
        # not of anything anybody watched, and is flagged as such.
        row[f"t{p}_beyond_last_visit"] = bool(max(ti, tn) > last)
    for v in VISIT_GRID:
        d = int(v)
        row[f"weibull_interval_not_yet_crossed_day{d}"] = float(wi.predict(v))
        row[f"weibull_naive_not_yet_crossed_day{d}"] = float(wn.predict(v))
        tb_v, tb_identified = _npmle_survival_at(tb, v)
        row[f"turnbull_not_yet_crossed_day{d}"] = tb_v
        row[f"turnbull_point_identified_day{d}"] = tb_identified
        row[f"km_naive_not_yet_crossed_day{d}"] = float(km.predict(v))
        row[f"turnbull_minus_km_day{d}"] = (row[f"turnbull_not_yet_crossed_day{d}"]
                                            - row[f"km_naive_not_yet_crossed_day{d}"])
    return row


# --------------------------------------------------------------------------
# B. discrete-time two-state transitions and trajectory classes
# --------------------------------------------------------------------------

def classify(t: pd.DataFrame) -> pd.Series:
    """The shape of a series, in the only vocabulary the visits support."""
    def f(r):
        if not r["ever_crossed_below"]:
            return "never below the boundary"
        if r["n_returns_above"] == 0:
            return "one crossing, no return"
        if r["n_returns_above"] == 1 and r["n_crossings_below"] <= 1:
            return "one crossing, returns above"
        return "crosses repeatedly"
    return t.apply(f, axis=1)


def transition_counts(d: pd.DataFrame) -> pd.DataFrame:
    """Transitions between CONSECUTIVE OBSERVED visits, per series.

    This is the multistate model this design supports: two states, discrete time
    on the visit grid the protocol actually used, transitions counted rather
    than intensities estimated. Where a visit was not observed the pair spans
    the gap; the number of unobserved visits per series is carried alongside so
    the reader can see how often that happens.
    """
    rows = []
    for (inst, arm, rep, cond), g in d.groupby(
            ["Institute", "Sample", "Replicate", "Condition"]):
        obs = g[g["state"] != "not observed"].sort_values("Time", kind="stable")
        s = obs["state"].to_numpy()
        if len(s) < 2:
            continue
        pre, post = s[:-1], s[1:]
        rows.append({
            "institute": inst, "arm": arm, "replicate": int(rep),
            "plating": PLATING[int(cond)],
            "n_pairs": int(len(pre)),
            "n_visits_not_observed": int((g["state"] == "not observed").sum()),
            "above_to_above": int(((pre == "above") & (post == "above")).sum()),
            "above_to_below": int(((pre == "above") & (post == "below")).sum()),
            "below_to_below": int(((pre == "below") & (post == "below")).sum()),
            "below_to_above": int(((pre == "below") & (post == "above")).sum()),
        })
    return pd.DataFrame(rows)


def transitions_by(pairs: pd.DataFrame, traj: pd.DataFrame,
                   col: str | None) -> pd.DataFrame:
    rows = []
    groups = ([("all series", pairs, traj)] if col is None
              else [(str(k), pairs[pairs[col] == k], traj[traj[col] == k])
                    for k in sorted(pairs[col].unique())])
    for name, p, t in groups:
        aa = int(p["above_to_above"].sum()); ab = int(p["above_to_below"].sum())
        bb = int(p["below_to_below"].sum()); ba = int(p["below_to_above"].sum())
        cls = t["trajectory_class"].value_counts()
        rows.append({
            "stratum_kind": col or "overall", "stratum": name,
            "n_series": int(len(t)), "n_visit_pairs": int(p["n_pairs"].sum()),
            "n_visits_not_observed": int(p["n_visits_not_observed"].sum()),
            "above_to_above": aa, "above_to_below": ab,
            "below_to_below": bb, "below_to_above": ba,
            "p_above_to_below": ab / (aa + ab) if (aa + ab) else np.nan,
            "p_below_to_above": ba / (bb + ba) if (bb + ba) else np.nan,
            "n_never_below": int(cls.get("never below the boundary", 0)),
            "n_one_crossing_no_return": int(cls.get("one crossing, no return", 0)),
            "n_one_crossing_returns": int(cls.get("one crossing, returns above", 0)),
            "n_crosses_repeatedly": int(cls.get("crosses repeatedly", 0)),
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# C. Cox, descriptive only, with clustered intervals
# --------------------------------------------------------------------------

def _cox_fit(df: pd.DataFrame, cols: list[str]) -> dict | None:
    from lifelines import CoxPHFitter
    sub = df[cols + ["naive_time", "event"]].dropna()
    if sub["event"].sum() < 3 or sub["naive_time"].nunique() < 2:
        return None
    cph = CoxPHFitter(penalizer=0.1)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cph.fit(sub, duration_col="naive_time", event_col="event")
    except Exception:
        return None
    return {"coefs": cph.params_.to_dict(),
            "se": cph.standard_errors_.to_dict(),
            "p": cph.summary["p"].to_dict(),
            "concordance": float(cph.concordance_index_)}


def cluster_bootstrap(df: pd.DataFrame, cols: list[str], cluster: str,
                      rng: np.random.Generator, n_boot: int,
                      require: object | None = None) -> dict:
    """Resample whole clusters with replacement and refit.

    Two details that matter with six laboratories. A laboratory absent from a
    resample contributes no coefficient for its own indicator, so that
    indicator's interval is taken over the replicates in which it appears, and
    the count of those replicates is carried beside it. And every laboratory
    coefficient is a contrast against a reference laboratory, so a resample that
    omits the reference is not estimating the same quantity at all: with no
    intercept and the remaining indicators summing to one, the coefficients are
    identified only up to a constant and the penalty, not the data, decides it.
    Those resamples are discarded and counted rather than pooled.
    """
    units = df[cluster].unique()
    draws: dict[str, list[float]] = {c: [] for c in cols}
    ok, dropped = 0, 0
    for _ in range(n_boot):
        pick = rng.choice(units, size=len(units), replace=True)
        if require is not None and require not in set(pick.tolist()):
            dropped += 1
            continue
        rep = pd.concat([df[df[cluster] == u] for u in pick], ignore_index=True)
        keep = [c for c in cols if rep[c].nunique() > 1]
        fit = _cox_fit(rep, keep)
        if fit is None:
            continue
        ok += 1
        for c in keep:
            if c in fit["coefs"]:
                draws[c].append(fit["coefs"][c])
    out = {"cluster": cluster, "n_clusters": int(len(units)),
           "n_replicates_attempted": int(n_boot), "n_replicates_fitted": int(ok),
           "n_replicates_discarded_missing_reference": int(dropped),
           "reference_required": None if require is None else str(require),
           "terms": {}}
    for c, v in draws.items():
        a = np.asarray(v, float)
        out["terms"][c] = {
            "n_replicates_with_term": int(a.size),
            "ci_low": float(np.percentile(a, 2.5)) if a.size >= 20 else np.nan,
            "ci_high": float(np.percentile(a, 97.5)) if a.size >= 20 else np.nan,
            "bootstrap_sd": float(a.std(ddof=1)) if a.size >= 3 else np.nan,
        }
    return out


def cox_descriptive(e: pd.DataFrame, rng: np.random.Generator
                    ) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """First observed crossing, described. Not a model of anything ending.

    Fitted over all four platings of every treated flask rather than over the
    most sensitive plating alone. Two reasons. The plating format is a covariate
    of the crossing, not a nuisance: the same flask crosses on different days,
    or not at all, depending on which plate is read. And at one plating there is
    exactly one series per flask, so a bootstrap clustered on flasks would
    reduce to an ordinary case resample and could not show what the clustering
    costs. Here 288 series come from 72 flasks in 6 laboratories, the partial
    likelihood treats all 288 as independent, and the two cluster bootstraps
    show what that assumption is worth.

    AND IT IS FITTED ON THE NAIVE TIMES. The duration is naive_time, the visit
    at which the crossing was noticed, which section A of this script has just
    shown is the late end of an interval every time. There is no interval-
    censored Cox here: the point of this fit is to describe the endpoint the
    manuscript already reports, on the clock the manuscript already uses, and
    to show what its intervals are worth. It is not an improved estimate of the
    crossing time, and no coefficient from it should be read as one. Every row
    carries the duration definition in a column so the fit cannot be quoted
    without it.
    """
    df = e[e["arm"].isin(TREATED)].copy()
    n_treated = int(len(df))
    # A series with no quantified reading at day 0 or day 1 IN ITS OWN PLATING
    # has no starting density to adjust for and is dropped. That is not a
    # neutral loss: the platings and laboratories that lose series are the ones
    # whose early readings were already at or below their own boundary.
    n_no_start = int(df["start_log10"].isna().sum())
    df = df.dropna(subset=["start_log10"])
    n_zero_time = int((df["naive_time"] <= 0).sum())
    df = df[df["naive_time"] > 0]        # a crossing seen at day zero has no duration
    n_dropped = n_treated - int(len(df))
    # The two exclusions are separate and are counted separately. Reporting the
    # total under the first reason would misattribute the one series that was
    # already below its own boundary at the day-zero visit.
    start_uses_day_zero = (
        df.groupby("institute")["start_uses_day_zero"].agg(["size", "sum"])
        .rename(columns={"size": "series", "sum": "with_a_day_zero_reading"}))
    both_days = df.dropna(subset=["day_zero_log10", "day_one_log10"])
    day_zero_minus_day_one = (
        float((both_days["day_zero_log10"] - both_days["day_one_log10"]).mean())
        if len(both_days) else np.nan)
    df["lab"] = df["institute"]
    df["flask"] = (df["institute"] + "|" + df["arm"] + "|"
                   + df["replicate"].astype(str))
    df["plating_format"] = df["plating"]
    reference_lab = sorted(df["lab"].unique())[0]     # what drop_first drops
    df = pd.get_dummies(df, columns=["institute", "plating_format"],
                        drop_first=True, dtype=float)
    inst = sorted(c for c in df.columns if c.startswith("institute_"))
    plate = sorted(c for c in df.columns if c.startswith("plating_format_"))

    rows, boots = [], {}
    for label, cols in (
            ("descriptive Cox: laboratory + plating format", inst + plate),
            ("descriptive Cox: laboratory + plating format + starting density",
             inst + plate + ["start_log10"])):
        fit = _cox_fit(df, cols)
        if fit is None:
            rows.append({"model": label, "analysis_role": "descriptive only",
                         "term": "all",
                         "note": "did not fit; recorded as a null result"})
            continue
        bl = cluster_bootstrap(df, cols, "lab", rng, N_BOOT,
                               require=reference_lab)
        bf = cluster_bootstrap(df, cols, "flask", rng, N_BOOT)
        boots[label] = {"by_laboratory": bl, "by_flask": bf}
        for term, coef in fit["coefs"].items():
            se = fit["se"][term]
            rows.append({
                "model": label, "analysis_role": "descriptive only",
                "duration_variable": ("naive pinned time: the visit at which the "
                                      "crossing was noticed, the late end of the "
                                      "interval"),
                "term": term, "coef": float(coef),
                "hazard_ratio_of_first_crossing": float(np.exp(coef)),
                "naive_model_ci_low": float(coef - 1.96 * se),
                "naive_model_ci_high": float(coef + 1.96 * se),
                "naive_model_p": float(fit["p"][term]),
                "lab_cluster_boot_ci_low":
                    bl["terms"].get(term, {}).get("ci_low", np.nan),
                "lab_cluster_boot_ci_high":
                    bl["terms"].get(term, {}).get("ci_high", np.nan),
                "lab_cluster_boot_replicates":
                    bl["terms"].get(term, {}).get("n_replicates_with_term", 0),
                "flask_cluster_boot_ci_low":
                    bf["terms"].get(term, {}).get("ci_low", np.nan),
                "flask_cluster_boot_ci_high":
                    bf["terms"].get(term, {}).get("ci_high", np.nan),
                "flask_cluster_boot_replicates":
                    bf["terms"].get(term, {}).get("n_replicates_with_term", 0),
                "concordance": fit["concordance"],
                "n_series": int(len(df)),
                "n_treated_series_before_exclusions": n_treated,
                "n_series_dropped_total": n_dropped,
                "n_series_dropped_no_early_quantified_reading": n_no_start,
                "n_series_dropped_already_below_at_day_zero": n_zero_time,
                "n_series_start_from_a_day_zero_reading":
                    int(df["start_uses_day_zero"].sum()),
                "n_flasks": int(df["flask"].nunique()),
                "n_laboratories": int(df["lab"].nunique()),
                "note": "",
            })
    return (pd.DataFrame(rows), boots, df[["lab", "flask", "event", "naive_time"]],
            {"by_laboratory": start_uses_day_zero,
             "n_with_both_days": int(len(both_days)),
             "mean_day_zero_minus_day_one_log10": day_zero_minus_day_one})


# --------------------------------------------------------------------------

def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; see the docstring for its source")
    rng = np.random.default_rng(SEED)
    pd.set_option("display.width", 230)

    d = load()
    keys = key_audit(d)

    print("-- the duplicate key, and the rule used to resolve it --")
    print(f"   readings, day 0 onwards, inoculum controls excluded : {keys['rows']}")
    print("   (Institute, Sample, Replicate, Volume, Time)")
    print(f"     keys carrying more than one reading               : "
          f"{keys['volume_keys_with_more_than_one_row']} "
          f"({keys['rows_sharing_a_volume_key']} readings)")
    print(f"     volumes involved                                  : "
          f"{keys['volumes_involved']}")
    print(f"     platings involved                                 : "
          f"{keys['platings_involved']}")
    print("   (Institute, Sample, Replicate, Condition, Time)")
    print(f"     keys carrying more than one reading               : "
          f"{keys['condition_keys_with_more_than_one_row']}")
    print(f"   series: {keys['series_under_volume_key']} under the volume key, "
          f"{keys['series_under_condition_key']} under the plating key")
    print("   RULE: the plating format is part of the series key. Nothing is dropped,")
    print("   nothing is averaged, and the two ten-microlitre formats stay apart.")

    # -- crossing and return -----------------------------------------------
    t = series_table(d, by_volume=False)
    t["trajectory_class"] = classify(t)
    t.to_csv(TABLES / "exp32_recrossing.csv", index=False)

    merged = series_table(d, by_volume=True)
    s_ok = recrossing_summary(t)
    s_merged = recrossing_summary(merged)

    print("\n-- how often does a series read above the boundary again? --")
    print(f"   {'':<36}{'plating key':>13}{'volume key':>13}")
    for lab, a, b in (
            ("series", s_ok["n_series"], s_merged["n_series"]),
            ("ever crossed below", s_ok["n_ever_crossed_below"],
             s_merged["n_ever_crossed_below"]),
            ("read above again afterwards", s_ok["n_returned_above"],
             s_merged["n_returned_above"]),
            ("   same, counting unrecorded visits",
             s_ok["n_returned_under_loose_rule"],
             s_merged["n_returned_under_loose_rule"]),
            ("crossed back more than once", s_ok["n_oscillating_more_than_once"],
             s_merged["n_oscillating_more_than_once"]),
            ("last observed visit still below", s_ok["n_series_ending_below"],
             s_merged["n_series_ending_below"])):
        print(f"   {lab:<36}{a:>13}{b:>13}")
    print(f"   {'proportion of crossers returning':<36}"
          f"{s_ok['fraction_of_crossers_returning']:>12.1%}"
          f"{s_merged['fraction_of_crossers_returning']:>13.1%}")
    print("   The volume key merges two platings into one series and manufactures")
    print("   oscillation. The looser rule counts a visit with no reading at all as a")
    print("   return. Together they are where the 83 of 111, 74.8 per cent, that this")
    print("   project has quoted comes from; the honest figure under the plating key")
    print(f"   with a real reading required is {s_ok['n_returned_above']} of "
          f"{s_ok['n_ever_crossed_below']}, "
          f"{100 * s_ok['fraction_of_crossers_returning']:.1f} per cent. The")
    print("   claim survives the correction: it is smaller and it is sound.")

    dd = s_ok["days_below_before_return"]
    print("\n   days spent below the boundary before reading above it again:")
    print(f"     min {dd['min']:.0f}, lower quartile {dd['q25']:.0f}, "
          f"median {dd['median']:.0f}, upper quartile {dd['q75']:.0f}, "
          f"max {dd['max']:.0f}")
    print(f"     {s_ok['n_returning_within_three_days']} of "
          f"{s_ok['n_returned_above']} were back above within three days, which is")
    print("     one visit gap in the early part of the schedule.")
    print(f"   median day of the first crossing: "
          f"{s_ok['median_first_crossing_day']:.0f}")

    print("\n   TWO THINGS THAT PROPORTION IS NOT.")
    print(f"   It is not over independent units. The {s_ok['n_series']} series come from "
          f"{s_ok['n_flasks']} flasks, each")
    print("   plated in four formats; the crossers are "
          f"{s_ok['n_flasks_with_a_crossing_series']} distinct flasks and the returners")
    print(f"   {s_ok['n_flasks_with_a_returning_series']}. No interval is quoted on "
          f"the proportion for that reason, and")
    print("   it should be read as a description of readings, not of experiments.")
    print(f"   And {s_ok['n_first_observed_visit_already_below']} of the "
          f"{s_ok['n_ever_crossed_below']} crossers read below at their FIRST observed")
    print("   visit, so no above-to-below step was ever seen in that plating: the")
    print("   crossing is inferred from one reading, not watched. They are kept, because")
    print("   they are below, but a reader who wants only watched crossings should")
    print(f"   subtract them.")

    by = pd.concat([recrossing_by(t, c) for c in ("arm", "institute", "plating")],
                   ignore_index=True)
    print("\n-- crossing and return by arm, laboratory and plating format --")
    print(by.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))

    # -- A. interval censoring ---------------------------------------------
    e = event_frame(t)
    sens = e[e["plating"] == PLATING[MOST_SENSITIVE]]
    ic_rows = [interval_vs_naive(sens, "all arms, 100 uL quadruplicate")]
    for arm in TREATED + ("untreated",):
        ic_rows.append(interval_vs_naive(sens[sens["arm"] == arm],
                                         f"{arm}, 100 uL quadruplicate"))
    ic_rows.append(interval_vs_naive(e[e["arm"].isin(TREATED)],
                                     "treated arms, all four platings"))
    ic = pd.DataFrame(ic_rows)
    ic.to_csv(TABLES / "exp32_interval_censored.csv", index=False)

    head = ic.iloc[0]
    print("\n-- time to the first observed crossing: interval-censored vs naive --")
    print("   The naive analysis pins the crossing to the visit at which it was")
    print("   noticed. That is the LATE end of the interval every time, so the naive")
    print("   estimate is biased late by construction, not merely imprecise.")
    print(f"   flasks {int(head['n_series'])}, crossings {int(head['n_crossed'])}; "
          f"median interval width {head['median_interval_width_days']:.0f} days "
          f"(largest {head['max_interval_width_days']:.0f})")
    print(f"   {'Weibull quantile of crossing time':<34}{'interval':>10}"
          f"{'naive':>10}{'shift':>9}")
    for p in (10, 25, 50):
        flag = "  extrapolated past the last visit" \
            if head[f"t{p}_beyond_last_visit"] else ""
        print(f"   {f'{p}% of flasks crossed by day':<34}"
              f"{head[f'weibull_interval_t{p}_days']:>10.2f}"
              f"{head[f'weibull_naive_t{p}_days']:>10.2f}"
              f"{head[f'shift_t{p}_days']:>9.2f}{flag}")
    print(f"   {'not yet crossed at':<34}{'Turnbull':>10}{'naive KM':>10}{'shift':>9}")
    for v in VISIT_GRID:
        n = int(v)
        print(f"   {f'  day {n}':<34}"
              f"{head[f'turnbull_not_yet_crossed_day{n}']:>10.3f}"
              f"{head[f'km_naive_not_yet_crossed_day{n}']:>10.3f}"
              f"{head[f'turnbull_minus_km_day{n}']:>9.3f}")
    shifts = {int(v): head[f"turnbull_minus_km_day{int(v)}"] for v in VISIT_GRID}
    worst_day = min(shifts, key=lambda k: shifts[k])
    print("   Both curves are read on the same convention. lifelines indexes the")
    print("   interval-censored fit by the right endpoints of its support intervals")
    print("   and each row holds the survival BEFORE the drop at that row, while the")
    print("   Kaplan-Meier returns the survival AFTER it; compared as returned, the")
    print("   two are one step apart and the NPMLE looks uniformly higher for no")
    print("   reason but the indexing. Realigned, the interval-censored curve sits")
    print(f"   BELOW the naive one at every visit at which crossings are still being")
    print(f"   recorded, furthest at day {worst_day} by "
          f"{abs(shifts[worst_day]):.3f}. The two coincide only from")
    print("   day 14 on, where no further crossing is recorded and both curves are")
    print("   flat. So a survival probability quoted AT A VISIT is not safe from the")
    print("   correction either: wherever the curve is still moving the naive")
    print("   estimate overstates how many flasks are still above the boundary.")

    # -- B. transitions ----------------------------------------------------
    pairs = transition_counts(d)
    tr = pd.concat(
        [transitions_by(pairs, t, None)]
        + [transitions_by(pairs, t, c) for c in ("arm", "institute", "plating")],
        ignore_index=True)
    tr.to_csv(TABLES / "exp32_transitions.csv", index=False)

    o = tr.iloc[0]
    print("\n-- the two-state transition count, on the visits the protocol used --")
    print("   Chosen over a continuous-time multistate model and over Andersen-Gill")
    print("   because no transition time is observed: every transition is interval-")
    print("   censored on a grid whose gaps reach seven days. Counted transitions")
    print("   are what this design supports.")
    print(f"   visit-to-visit pairs               : {int(o['n_visit_pairs'])}")
    print(f"   above -> below                     : {int(o['above_to_below']):>5}"
          f"   P = {o['p_above_to_below']:.3f} of pairs starting above")
    print(f"   below -> above                     : {int(o['below_to_above']):>5}"
          f"   P = {o['p_below_to_above']:.3f} of pairs starting below")
    print(f"   below -> below                     : {int(o['below_to_below']):>5}")
    print("   A state left this readily in one visit gap is not an absorbing state.")
    print("\n   trajectory classes over all series:")
    for c, n in (("never below the boundary", o["n_never_below"]),
                 ("one crossing, no return", o["n_one_crossing_no_return"]),
                 ("one crossing, returns above", o["n_one_crossing_returns"]),
                 ("crosses repeatedly", o["n_crosses_repeatedly"])):
        print(f"     {c:<32}{int(n):>5}  ({100 * n / o['n_series']:.1f}%)")
    n_pre = int(t.loc[t["first_observed_visit_below"] & (t["n_crossings_below"] == 0)
                      & (t["n_returns_above"] == 0)].shape[0])
    print(f"   Read the second class with care: {n_pre} of those "
          f"{int(o['n_one_crossing_no_return'])} series were already below at")
    print("   their first observed visit and never recorded an above-to-below step at")
    print("   all, so the class is an upper bound on the shape the survival model")
    print("   assumes, not a count of series seen to make the move.")

    print("\n   by arm:")
    print(tr[tr["stratum_kind"] == "arm"][
        ["stratum", "n_series", "above_to_below", "below_to_above",
         "p_below_to_above", "n_never_below", "n_one_crossing_no_return",
         "n_one_crossing_returns", "n_crosses_repeatedly"]]
        .to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    # -- C. Cox, descriptive ------------------------------------------------
    cox, boots, cox_events, start_prov = cox_descriptive(e, rng)
    cox.to_csv(TABLES / "exp32_cox_descriptive.csv", index=False)
    width_summary: dict = {}

    print("\n-- descriptive Cox on the first observed crossing, all four platings of")
    print("   every treated flask. A description of when a laboratory first records a")
    print("   blank plate. It is not a model of a state anything stays in.")
    if "coef" in cox.columns:
        print(f"   {int(cox['n_series'].iloc[0])} series from "
              f"{int(cox['n_flasks'].iloc[0])} flasks in "
              f"{int(cox['n_laboratories'].iloc[0])} laboratories; the partial")
        print("   likelihood treats all of them as independent.")
        print(f"   {int(cox['n_series_dropped_total'].iloc[0])} of "
              f"{int(cox['n_treated_series_before_exclusions'].iloc[0])} treated series "
              f"are dropped, for two")
        print(f"   separate reasons: "
              f"{int(cox['n_series_dropped_no_early_quantified_reading'].iloc[0])} carry no "
              f"quantified reading at day 0 or 1 in their")
        print(f"   own plating format, and "
              f"{int(cox['n_series_dropped_already_below_at_day_zero'].iloc[0])} was already "
              f"below its own boundary at the")
        print("   day-zero visit and so has no duration to model. The first is itself a")
        print("   censoring: those are the platings that started at or below their own")
        print("   boundary, and it falls unevenly across laboratories.")
        print("   The duration is the NAIVE pinned time, the visit at which the crossing")
        print("   was noticed. Section A above showed that is the late end of an interval")
        print("   every time. This fit describes the endpoint the manuscript already")
        print("   reports on the clock it already uses; it is not a better estimate of")
        print("   when anything crossed, and no coefficient here should be read as one.")
        show = cox[["model", "term", "coef", "naive_model_ci_low",
                    "naive_model_ci_high", "lab_cluster_boot_ci_low",
                    "lab_cluster_boot_ci_high", "flask_cluster_boot_ci_low",
                    "flask_cluster_boot_ci_high"]]
        print(show.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
        w = cox.dropna(subset=["lab_cluster_boot_ci_low",
                               "flask_cluster_boot_ci_low"]).copy()
        w["is_lab_term"] = w["term"].str.startswith("institute_")
        w["naive_w"] = w["naive_model_ci_high"] - w["naive_model_ci_low"]
        w["flask_w"] = w["flask_cluster_boot_ci_high"] - w["flask_cluster_boot_ci_low"]
        w["lab_w"] = w["lab_cluster_boot_ci_high"] - w["lab_cluster_boot_ci_low"]
        print("\n   median width of the interval on a coefficient:")
        print(f"   {'terms':<28}{'model SE':>10}{'flask boot':>12}{'lab boot':>10}")
        for name, sub in (("laboratory contrasts", w[w["is_lab_term"]]),
                          ("plating and density", w[~w["is_lab_term"]]),
                          ("starting density alone", w[w["term"] == "start_log10"])):
            if len(sub):
                width_summary[name] = {
                    "median_width_model_standard_errors": float(sub["naive_w"].median()),
                    "median_width_flask_cluster_bootstrap": float(sub["flask_w"].median()),
                    "median_width_laboratory_cluster_bootstrap": float(sub["lab_w"].median()),
                }
        for name, sub in (("laboratory contrasts", w[w["is_lab_term"]]),
                          ("plating and density", w[~w["is_lab_term"]])):
            if len(sub):
                print(f"   {name:<28}{sub['naive_w'].median():>10.2f}"
                      f"{sub['flask_w'].median():>12.2f}{sub['lab_w'].median():>10.2f}")
        sd = w[w["term"] == "start_log10"]
        if len(sd):
            print(f"   {'starting density alone':<28}{sd['naive_w'].median():>10.2f}"
                  f"{sd['flask_w'].median():>12.2f}{sd['lab_w'].median():>10.2f}")
        print("   The two bootstraps answer different questions and the split above is")
        print("   not an accident. Resampling laboratories keeps each laboratory's own")
        print("   flasks intact, so a coefficient that IS one laboratory's contrast")
        print("   hardly moves under it; that bootstrap is the wrong instrument for")
        print("   those terms and the flask bootstrap, which is close to the model's")
        print("   own width, is the one to read. For a covariate that is not a")
        print("   laboratory label the position reverses, and starting density is the")
        print("   coefficient the argument of Section 3.4 rests on:")
        if len(sd):
            print(f"   the laboratory-clustered interval on it is "
                  f"{sd['lab_w'].median() / sd['naive_w'].median():.1f} times the model's own")
            print(f"   and {sd['lab_w'].median() / sd['flask_w'].median():.1f} times the "
                  f"flask-clustered one. It is the interval to quote.")
        ev = (cox_events.groupby("lab")["event"].agg(["size", "sum"])
              .rename(columns={"size": "series", "sum": "crossings"}))
        print("\n   crossings behind each laboratory's coefficient:")
        print("   " + ev.to_string().replace("\n", "\n   "))
        print("   Laboratory E carries a coefficient on very few crossings, and the")
        print("   penalised fit is what keeps it finite. That is a limit of the data,")
        print("   not a property of the laboratory.")

    print("\n   what the covariate called starting density is actually made of:")
    print("   " + start_prov["by_laboratory"].to_string().replace("\n", "\n   "))
    print("   It is the mean of the quantified readings at day 0 or day 1 in the")
    print("   series' own plating, and the deposit does not carry a day-zero reading")
    print("   for every laboratory. Where day zero is absent the value is a day-ONE")
    print("   reading, taken after twenty-four hours of drug. That is not a small")
    print(f"   difference: over the {start_prov['n_with_both_days']} series that have "
          f"both, the day-zero reading is")
    print(f"   {start_prov['mean_day_zero_minus_day_one_log10']:.2f} log10 above the "
          f"day-one one on average. So for most of these")
    print("   series the covariate is not an inoculum, and its definition is not the")
    print("   same in every laboratory -- which is a laboratory-level offset sitting")
    print("   inside the very covariate whose trade with the laboratory term is being")
    print("   discussed. It should be called the early recorded density, not the")
    print("   inoculum, and the trade below read with that in mind.")

    print("\n   Adding starting density moves the laboratory coefficients. exp24 found")
    print("   laboratory explains most of the variance in starting density in this")
    print("   design, so the two predictors nearly determine one another and a")
    print("   coefficient trade between them is arithmetic. It is a statement about")
    print("   the covariance of the two predictors here. It is not evidence that")
    print("   starting density accounts for the laboratory effect.")

    (RECEIPTS / "exp32_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp32_crossing_events.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "ERA4TB standardised time-kill, figshare 19766083",
        "event_definition": ("first observed crossing below the assay boundary; "
                             "the boundary is 1000/plated volume CFU per mL"),
        "duplicate_key_resolution": {
            "problem": ("Volume does not identify a plating: 10 uL appears both "
                        "as a single drop and as four drops"),
            "rule": "the plating format (Condition) is part of the series key",
            **keys,
        },
        "recrossing_plating_key": s_ok,
        "recrossing_volume_key_for_comparison": s_merged,
        "recrossing_by_stratum": by.to_dict(orient="records"),
        "interval_vs_naive": ic.to_dict(orient="records"),
        "transitions": tr.to_dict(orient="records"),
        "cox_descriptive_only": cox.to_dict(orient="records"),
        "cox_cluster_bootstrap": boots,
        "cox_interval_widths": width_summary,
        "cox_crossings_per_laboratory": (
            cox_events.groupby("lab")["event"].agg(["size", "sum"])
            .rename(columns={"size": "series", "sum": "crossings"})
            .to_dict(orient="index")),
        "n_bootstrap_replicates": N_BOOT,
        "seed": SEED,
    }, indent=2, default=str), encoding="utf-8")

    unt = by[(by["stratum_kind"] == "arm") & (by["stratum"] == "untreated")]
    print("\n-- what survives --")
    print(f"   {s_ok['n_ever_crossed_below']} of {s_ok['n_series']} series cross below "
          f"the boundary; {s_ok['n_returned_above']} of those read above it")
    print(f"   again, {s_ok['n_oscillating_more_than_once']} of them more than once. "
          f"In the untreated arm "
          f"{int(unt['n_crossed'].iloc[0])} series cross and")
    print(f"   {int(unt['n_returned'].iloc[0])} of them return, which is the cleanest "
          f"demonstration available that this")
    print("   event is at least partly a property of the plate rather than of the drug.")
    print("   STILL SAYABLE. That the first crossing depends on the starting density,")
    print("   with the laboratory-clustered interval above and not the model's own.")
    print("   That laboratories differ in whether they produce the endpoint at all.")
    print("   That the endpoint depends on the plating format, which is a choice.")
    print("   NO LONGER SAYABLE. That the event is the end of the culture; that a")
    print("   series below the boundary stays there; that the time at which it was")
    print("   noticed is the time it happened; and any minimum-duration figure read")
    print("   off a curve fitted to those pinned times without the interval above.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
