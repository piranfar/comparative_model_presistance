"""
Every number in this paper is computed as though its rows were independent. They
are not. This is the audit that says which conclusions survive that.

Run:  python -m src.experiments.exp31_clustering_audit

WHY THIS TEST EXISTS. Both primary deposits are clustered, and neither analysis
in this repository has said so out loud in the arithmetic. The clinical file
contains 43 follow-up isolates from patients who also contributed a baseline, so
some of its 217 rows are repeated measurements on the same person. The
six-laboratory file is nested four levels deep -- a reading is one of up to four
platings of one flask at one visit, the flask is one of three in a treatment arm,
the arm is one of five in a laboratory, and there are six laboratories -- and
almost every between-laboratory statement in the manuscript is computed on
flasks or on readings as if each were a fresh draw. When the unit of analysis is
smaller than the unit of independence, a confidence interval is too narrow and a
p-value is too small, and both are wrong in the direction that flatters the
author. So this script recomputes them at the level at which the data are
actually exchangeable, and prints the corrected number beside the published one.

WHAT CANNOT BE DONE, AND IS NOT FAKED. The clinical deposit has no patient
identifier. Archive and Sample-ID are unique per row; Time_point and the
sequential-isolate column together prove that repeats exist but do not say which
baseline belongs to which follow-up, and no other column in the file has the
multiplicity a patient key would have (this script checks all 48). A
mixed-effects model with a patient random effect is therefore not available and
is not invented. What is available is the exact sensitivity analysis: drop every
isolate that could be a repeat and rerun. Time_point == '0M' leaves 174 isolates
that are one-per-patient by construction, and every load-bearing count is
recomputed on them.

THE 15-DAY AND 60-DAY PANELS ARE ONE SET OF ISOLATES, NOT TWO. They are columns
on the same row. Comparing them with a two-sample test -- a Fisher exact on
33/217 against 7/210, a Mann-Whitney on the two headroom distributions -- treats
210 isolates as 420 and discards the pairing that makes the comparison sharp.
McNemar and Wilcoxon signed-rank are used instead, and the unpaired versions are
printed beside them so the difference is visible.

SIX CLUSTERS IS TOO FEW FOR AN ASYMPTOTIC CLUSTER-ROBUST STANDARD ERROR, and
this is not a stylistic preference. The cluster-robust meat matrix is a sum of
one outer product per cluster, so with six laboratories it has rank at most six,
and after centring at most five. The Cox model in Section 5 carries five
institute dummies plus starting density: six parameters against a matrix of rank
five. There is no valid Wald test for the institute terms at all. That is a fact
about the design, not about the software, and the rank bound is arithmetic
rather than something this script measures; what it measures is the consequence,
which is a robust p-value one-and-twenty orders of magnitude smaller than the
one it was meant to correct. Permutation and cluster bootstrap are used instead, and where the
design admits neither, the script says so rather than reporting a number.

THE RESULT THAT MATTERS. Starting density separates flasks that ever cleared
from those that never did with an area under the curve of 0.974 and a
Mann-Whitney p of 1.2e-10 across 67 treated flasks. But three laboratories
cleared flasks and three did not, and the three lowest starting densities are
exactly the three that cleared. The comparison is a three-against-three
comparison of laboratories wearing 67 flasks as a disguise. Its exact
laboratory-level p is 0.10 two-sided -- and 0.10 is the smallest two-sided value
a 3-against-3 design can return, so the deposit could not have produced a
significant result at this level however clean the separation.

Nor is there a within-laboratory version to fall back on. Shuffling clearance
among the flasks of each laboratory, the association still looks strong, but that
shuffle leaves the treatment arm free, and the day 0 to 1 window used to measure
the starting density is not arm-neutral: the arms treated at ten times MIC have
already lost most of their population inside that window and they are the arms
that clear, so the arm that never clears also reads highest. Hold the arm fixed
as well and only two of 24 laboratory-arm cells still contain both outcomes -- six distinct
arrangements, a smallest attainable p of 0.17. The direction and the size of the
effect survive as a description. The p-value does not survive at all.

DEPENDENCIES. This script audits published tables, so where a quantity comes
from a censored maximum-likelihood fit it reads that fit from the table the
experiment wrote rather than refitting it, and the naive figure it prints
alongside is therefore literally the published one. It needs exp17, exp23 and
exp24 to have run.

Writes:
  results/tables/exp31_clustering_structure.csv
  results/tables/exp31_recomputed_inference.csv
  results/tables/exp31_baseline_only_sensitivity.csv
  results/receipts/exp31_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from itertools import combinations, permutations
from math import comb
from pathlib import Path

import numpy as np
import numpy.linalg as la
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
TB = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
ERA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

MPN_FLOOR = 23.0                 # per mL, inferred; see exp22
DEPTH_LOGS = 4.0                 # the 99.99 per cent endpoint
CLASS_CUTS = (1e-3, 1e-2)        # deposited thresholds on the surviving fraction
LEVEL = {"Low": 0, "Medium": 1, "High": 2}       # "MDR" is a fourth label
BASELINE_TIMEPOINT = "0M"

MOST_SENSITIVE_UL = 100.0
CLEARANCE_LIMIT = 1.0            # log10 CFU/mL at 100 uL plated
GROUPS = {0: "untreated", 1: "MXF 1x MIC", 2: "MXF 10x MIC",
          3: "INH 1x MIC", 4: "INH 10x MIC"}

N_BOOT = 4000
N_BOOT_PAIRS = 600               # the pairwise statistic is O(n^2) per draw
N_PERM = 20000
SEED = 20260906


# ==========================================================================
# small shared machinery
# ==========================================================================

def ols(y: np.ndarray, X: np.ndarray):
    """Least squares with t-tests. Returns (coefficients, standard errors, p)."""
    X = np.column_stack([np.ones(len(X)), X])
    b = la.lstsq(X, y, rcond=None)[0]
    r = y - X @ b
    dof = len(y) - X.shape[1]
    se = np.sqrt(np.diag((r @ r / dof) * la.inv(X.T @ X)))
    return b, se, 2 * (1 - stats.t.cdf(np.abs(b / se), dof))


def benjamini_hochberg(p: np.ndarray, q: float = 0.05) -> np.ndarray:
    order = np.argsort(p)
    crit = q * (np.arange(1, len(p) + 1)) / len(p)
    passed = p[order] <= crit
    keep = np.zeros(len(p), dtype=bool)
    if passed.any():
        keep[order[: np.max(np.flatnonzero(passed)) + 1]] = True
    return keep


def mcnemar_exact(a: np.ndarray, b: np.ndarray) -> dict:
    """Exact McNemar for two binary readings on the SAME units.

    Only the discordant pairs carry information about a change, which is exactly
    the point: an unpaired test spends the concordant pairs as though they were
    evidence.
    """
    a = np.asarray(a, bool)
    b = np.asarray(b, bool)
    n01 = int((a & ~b).sum())
    n10 = int((~a & b).sum())
    disc = n01 + n10
    p = float(stats.binomtest(n01, disc, 0.5).pvalue) if disc else 1.0
    return {"n_pairs": int(len(a)), "n_both": int((a & b).sum()),
            "n_only_first": n01, "n_only_second": n10, "n_neither": int((~a & ~b).sum()),
            "n_discordant": disc, "p_value": p}


def auc_from_ranks(x_pos: np.ndarray, x_neg: np.ndarray) -> float:
    """Probability that a positive scores below a negative (ties at 0.5).

    Written to match exp17: clearance is associated with a LOW starting density,
    so the discriminating direction is downward and the AUC is 1 - U/(n+ n-).
    """
    if len(x_pos) == 0 or len(x_neg) == 0:
        return np.nan
    u = stats.mannwhitneyu(x_pos, x_neg).statistic
    return float(1 - u / (len(x_pos) * len(x_neg)))


def pfmt(p: float, n_draws: int) -> str:
    """A Monte Carlo p of zero is a bound, not a zero. Print it as one."""
    return f"< {1.0/n_draws:.0e}" if p <= 0 else f"{p:.3g}"


def percentile_ci(v: np.ndarray, lo: float = 2.5, hi: float = 97.5):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if v.size < 20:
        return (np.nan, np.nan)
    return (float(np.percentile(v, lo)), float(np.percentile(v, hi)))


def cluster_jackknife(values_by_cluster, stat) -> dict:
    """Delete-one-cluster jackknife. With G clusters the interval uses t(G-1)."""
    keys = list(values_by_cluster)
    g = len(keys)
    full = stat(keys)
    reps = np.array([stat([k for k in keys if k != drop]) for drop in keys], float)
    reps = reps[np.isfinite(reps)]
    if len(reps) < 3:
        return {"estimate": full, "se": np.nan, "ci_low": np.nan, "ci_high": np.nan,
                "n_clusters": g}
    mean = reps.mean()
    se = np.sqrt((len(reps) - 1) / len(reps) * ((reps - mean) ** 2).sum())
    t = stats.t.ppf(0.975, len(reps) - 1)
    return {"estimate": float(full), "se": float(se),
            "ci_low": float(full - t * se), "ci_high": float(full + t * se),
            "n_clusters": g}


# ==========================================================================
# 1. the clinical deposit: what the repeated structure is, and what it is not
# ==========================================================================

def clinical_load() -> pd.DataFrame:
    d = pd.read_excel(TB)
    # remember what the deposit actually contains, before the derived columns
    # below are added, so the patient-key search searches the deposit
    d.attrs["deposited_columns"] = list(d.columns)
    d["growth"] = pd.to_numeric(d["Time_to_0.4"], errors="coerce")
    d["resistant"] = d["INH-Suceptibility"].isin(["IR"]).astype(int)
    d["baseline"] = d["Time_point"].astype(str) == BASELINE_TIMEPOINT
    for age in (15, 60):
        n0 = pd.to_numeric(d[f"mpn_T0_{age}days"], errors="coerce")
        n5 = pd.to_numeric(d[f"mpn_T5_{age}days"], errors="coerce")
        d[f"start_{age}"] = np.log10(n0)
        d[f"headroom_{age}"] = np.log10(n0 / MPN_FLOOR)
        d[f"at_floor_{age}"] = n5 <= MPN_FLOOR
        d[f"short_{age}"] = d[f"headroom_{age}"] < DEPTH_LOGS
        d[f"level_{age}"] = d[f"Tolerant_level_D5_{age}"].map(LEVEL)
    return d


def hunt_for_a_patient_key(d: pd.DataFrame) -> pd.DataFrame:
    """Is there any column that could be the missing patient identifier?

    43 rows are follow-ups from patients who also gave a baseline, so a patient
    key would show roughly 174 distinct values with about 43 of them appearing
    twice. Every column is checked against that signature. Reporting the search
    matters as much as its result: the linkage is absent, not overlooked.
    """
    rows = []
    n_follow = int((~d["baseline"]).sum())
    for col in d.attrs.get("deposited_columns", list(d.columns)):
        s = d[col]
        vc = s.value_counts(dropna=True)
        rows.append({
            "column": col,
            "n_non_null": int(s.notna().sum()),
            "n_distinct": int(vc.size),
            "n_values_appearing_twice": int((vc == 2).sum()),
            "max_multiplicity": int(vc.max()) if vc.size else 0,
            "matches_patient_key_signature": bool(
                vc.size >= len(d) - n_follow - 5 and vc.size < len(d)
                and (vc == 2).sum() >= n_follow - 5),
        })
    return pd.DataFrame(rows).sort_values("n_distinct", ascending=False)


def clinical_structure(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    seq = d["INH-R-sequential isolates"]
    n = len(d)
    n_base = int(d["baseline"].sum())
    n_follow = n - n_base
    n_cp = int((seq == "IR-CP").sum())
    n_ip = int((seq == "IR-IP").sum())
    rows = [
        {"deposit": "Vijay clinical", "level": 1, "unit": "isolate (row)",
         "n_units": n, "n_parents": n_base, "mean_per_parent": n / n_base,
         "note": "Archive and Sample-ID are both unique per row, so neither is "
                 "the parent key"},
        {"deposit": "Vijay clinical", "level": 2, "unit": "patient (NOT RECOVERABLE)",
         "n_units": n_base, "n_parents": np.nan, "mean_per_parent": np.nan,
         "note": f"at least {n_base} patients; {n_follow} follow-up isolates come "
                 f"from patients already represented, but the deposit does not "
                 f"say which, so up to {2 * n_follow} rows sit in clusters of two"},
    ]
    summ = {
        "n_isolates": n,
        "n_baseline_isolates": n_base,
        "n_follow_up_isolates": n_follow,
        "n_continuation_phase_IR_CP": n_cp,
        "n_intensive_phase_IR_IP": n_ip,
        "n_follow_up_without_sequential_label": n_follow - n_cp - n_ip,
        "time_point_counts": {str(k): int(v) for k, v in
                              d["Time_point"].value_counts().items()},
        "sequential_label_counts": {str(k): int(v) for k, v in
                                    seq.value_counts(dropna=False).items()},
        "n_rows_potentially_non_independent": 2 * n_follow,
        "pct_rows_potentially_non_independent": 100 * 2 * n_follow / n,
        "min_distinct_patients": n_base,
        "max_mean_cluster_size": n / n_base,
        "worst_case_design_effect": n / n_base,
        "worst_case_se_inflation": float(np.sqrt(n / n_base)),
        "linkage_recoverable": False,
    }
    return pd.DataFrame(rows), summ


# ==========================================================================
# 2. baseline-only sensitivity for every load-bearing clinical count
# ==========================================================================

def _class_of(fraction: float) -> str:
    lo, hi = CLASS_CUTS
    return "Low" if fraction < lo else ("Medium" if fraction <= hi else "High")


def observability(d: pd.DataFrame, age: int = 15) -> pd.Series:
    """exp25's three classes, recomputed so it can be restricted to baselines."""
    n0 = pd.to_numeric(d[f"mpn_T0_{age}days"], errors="coerce")
    n5 = pd.to_numeric(d[f"mpn_T5_{age}days"], errors="coerce")
    lab = d[f"Tolerant_level_D5_{age}"]
    usable = n0.notna() & n5.notna() & lab.isin(LEVEL)
    at_floor = n5 <= MPN_FLOOR
    low_end = np.array([_class_of(0.0)] * len(d))
    high_end = np.array([_class_of(MPN_FLOOR / v) if v > 0 else None for v in n0])
    forced = at_floor & (low_end == high_end)
    k = np.where(~at_floor, "determinable",
                 np.where(forced, "forced by inoculum", "undecidable"))
    return pd.Series(np.where(usable, k, None), index=d.index)


def clinical_panel(d: pd.DataFrame, age: int = 15) -> dict:
    """Every load-bearing clinical quantity, on whatever subset is handed in."""
    out = {"n_rows": int(len(d))}

    mdk = pd.to_numeric(d[f"MDK_99_99_{age}day_new"], errors="coerce")
    head = d[f"headroom_{age}"]
    ok = mdk.notna() & head.notna()
    out["n_with_headroom_and_endpoint"] = int(ok.sum())
    out["n_short_of_4_logs"] = int((ok & (head < DEPTH_LOGS)).sum())
    out["pct_short_of_4_logs"] = 100 * out["n_short_of_4_logs"] / max(int(ok.sum()), 1)

    ceiling = mdk[ok].max() if ok.any() else np.nan
    short_m = ok & (head < DEPTH_LOGS)
    long_m = ok & (head >= DEPTH_LOGS)
    a_at, b_at = int((mdk[short_m] == ceiling).sum()), int((mdk[long_m] == ceiling).sum())
    out["fraction_at_ceiling_short"] = a_at / max(int(short_m.sum()), 1)
    out["fraction_at_ceiling_ample"] = b_at / max(int(long_m.sum()), 1)
    out["ceiling_fisher_p"] = float(stats.fisher_exact(
        [[a_at, int(short_m.sum()) - a_at], [b_at, int(long_m.sum()) - b_at]])[1])

    at = d[f"at_floor_{age}"].fillna(False)
    sub = d[at]
    out["n_at_floor"] = int(at.sum())
    if len(sub):
        n0 = pd.to_numeric(sub[f"mpn_T0_{age}days"], errors="coerce")
        sv = pd.to_numeric(sub[f"Survival_T5_{age}days"], errors="coerce")
        out["at_floor_start_fold_range"] = float(n0.max() / n0.min())
        out["at_floor_survival_fold_range"] = float(sv.max() / sv.min())
        out["at_floor_label_counts"] = {str(k): int(v) for k, v in
                                        sub[f"Tolerant_level_D5_{age}"]
                                        .value_counts().items()}

    obs = observability(d, age)
    used = obs.notna()
    out["n_calls"] = int(used.sum())
    for k in ("determinable", "forced by inoculum", "undecidable"):
        out[k.replace(" ", "_")] = int((obs == k).sum())

    # the deep endpoint by susceptibility group
    reach = head >= DEPTH_LOGS
    g = d["INH-Suceptibility"]
    ir, is_ = (g == "IR") & head.notna(), (g == "IS") & head.notna()
    out["n_IR"], out["n_IS"] = int(ir.sum()), int(is_.sum())
    out["pct_unreachable_IR"] = 100 * float((~reach[ir]).mean()) if ir.any() else np.nan
    out["pct_unreachable_IS"] = 100 * float((~reach[is_]).mean()) if is_.any() else np.nan
    if ir.any() and is_.any():
        out["unreachable_fisher_p"] = float(stats.fisher_exact(
            [[int((~reach[ir]).sum()), int(reach[ir].sum())],
             [int((~reach[is_]).sum()), int(reach[is_].sum())]])[1])

    s_ir = d.loc[ir, f"start_{age}"].dropna()
    s_is = d.loc[is_, f"start_{age}"].dropna()
    if len(s_ir) and len(s_is):
        out["start_median_IR"] = float(s_ir.median())
        out["start_median_IS"] = float(s_is.median())
        out["start_fold_lower_in_IR"] = float(10 ** (s_is.median() - s_ir.median()))
        out["start_mannwhitney_p"] = float(stats.mannwhitneyu(s_ir, s_is).pvalue)
        gr_ir = d.loc[ir, "growth"].dropna()
        gr_is = d.loc[is_, "growth"].dropna()
        if len(gr_ir) and len(gr_is):
            out["growth_median_IR"] = float(gr_ir.median())
            out["growth_median_IS"] = float(gr_is.median())
            out["growth_mannwhitney_p"] = float(stats.mannwhitneyu(gr_ir, gr_is).pvalue)

    # the association family, D5 at this culture age
    m = pd.DataFrame({
        "lab": d[f"level_{age}"], "resistant": d["resistant"],
        "start": d[f"start_{age}"], "growth": d["growth"],
    })[d["INH-Suceptibility"].isin(["IS", "IR"])].dropna()
    if len(m) >= 30:
        b1, se1, p1 = ols(m["lab"].values, m[["resistant"]].values)
        b2, se2, p2 = ols(m["lab"].values, m[["resistant", "start"]].values)
        b3, se3, p3 = ols(m["lab"].values, m[["growth", "start"]].values)
        out["n_association"] = int(len(m))
        out["resistance_beta"] = float(b1[1])
        out["resistance_ci"] = [float(b1[1] - 1.96 * se1[1]), float(b1[1] + 1.96 * se1[1])]
        out["resistance_p"] = float(p1[1])
        out["resistance_beta_adjusted"] = float(b2[1])
        out["resistance_ci_adjusted"] = [float(b2[1] - 1.96 * se2[1]),
                                         float(b2[1] + 1.96 * se2[1])]
        out["resistance_p_adjusted"] = float(p2[1])
        out["resistance_attenuation"] = float((b1[1] - b2[1]) / b1[1])
        out["growth_beta_adjusted"] = float(b3[1])
        out["growth_p_adjusted"] = float(p3[1])
    return out


def mic_mdk_family(d: pd.DataFrame) -> dict:
    """exp16's question, restricted to one-per-patient rows.

    Six endpoints against the rifampicin MIC. exp16 runs them in three strata as
    one family of 24; here the family is the six tests the baseline stratum
    supports, which is the strictest reading of both the multiplicity and the
    independence problem at once.
    """
    ends = ["MDK_90_15day_new", "MDK_99_15day_new", "MDK_99_99_15day_new",
            "MDK_90_60day_new", "MDK_99_60day_new", "MDK_99_99_60day_new"]
    rows = []
    for col in ends:
        sub = d.dropna(subset=["MIC_RIF", col])
        if len(sub) < 20 or sub[col].nunique() < 3:
            continue
        r = stats.spearmanr(np.log2(sub["MIC_RIF"].astype(float)),
                            sub[col].astype(float))
        rows.append({"endpoint": col, "n": int(len(sub)),
                     "rho": float(r.statistic), "p": float(r.pvalue)})
    t = pd.DataFrame(rows)
    if t.empty:
        return {"n_tests": 0}
    t["survives_bh"] = benjamini_hochberg(t["p"].to_numpy())
    return {"n_tests": int(len(t)),
            "n_nominal": int((t["p"] < 0.05).sum()),
            "n_surviving_bh": int(t["survives_bh"].sum()),
            "smallest_p": float(t["p"].min()),
            "all_negative": bool((t.loc[t["p"] < 0.05, "rho"] < 0).all())}


# ==========================================================================
# 3. the two panels are the same isolates: paired versus unpaired
# ==========================================================================

def paired_panels(d: pd.DataFrame, rng: np.random.Generator) -> dict:
    both = d[d["start_15"].notna() & d["start_60"].notna()].copy()
    out = {"n_isolates_in_both_panels": int(len(both)),
           "n_only_15d": int((d["start_15"].notna() & d["start_60"].isna()).sum()),
           "n_only_60d": int((d["start_15"].isna() & d["start_60"].notna()).sum()),
           "pairing_key": "same spreadsheet row; Archive and Sample-ID identical "
                          "for the 15-day and 60-day columns by construction"}

    # -- short of 4 logs of headroom -----------------------------------------
    s15_all = d["short_15"][d["headroom_15"].notna()]
    s60_all = d["short_60"][d["headroom_60"].notna()]
    out["unpaired_short"] = {
        "n_15d": int(s15_all.sum()), "N_15d": int(len(s15_all)),
        "n_60d": int(s60_all.sum()), "N_60d": int(len(s60_all)),
        "fisher_p": float(stats.fisher_exact(
            [[int(s15_all.sum()), len(s15_all) - int(s15_all.sum())],
             [int(s60_all.sum()), len(s60_all) - int(s60_all.sum())]])[1])}
    out["paired_short"] = mcnemar_exact(both["short_15"].to_numpy(bool),
                                        both["short_60"].to_numpy(bool))

    # -- reading at the floor -------------------------------------------------
    f15 = d["at_floor_15"][d[f"mpn_T5_15days"].notna()]
    f60 = d["at_floor_60"][d[f"mpn_T5_60days"].notna()]
    out["unpaired_at_floor"] = {
        "n_15d": int(f15.sum()), "N_15d": int(len(f15)),
        "n_60d": int(f60.sum()), "N_60d": int(len(f60)),
        "fisher_p": float(stats.fisher_exact(
            [[int(f15.sum()), len(f15) - int(f15.sum())],
             [int(f60.sum()), len(f60) - int(f60.sum())]])[1])}
    out["paired_at_floor"] = mcnemar_exact(both["at_floor_15"].fillna(False).to_numpy(bool),
                                           both["at_floor_60"].fillna(False).to_numpy(bool))

    # -- determinable or not --------------------------------------------------
    o15, o60 = observability(d, 15), observability(d, 60)
    m = o15.notna() & o60.notna()
    out["paired_not_determinable"] = mcnemar_exact(
        (o15[m] != "determinable").to_numpy(bool),
        (o60[m] != "determinable").to_numpy(bool))
    out["paired_not_determinable"]["n_not_determinable_15d"] = int((o15[m] != "determinable").sum())
    out["paired_not_determinable"]["n_not_determinable_60d"] = int((o60[m] != "determinable").sum())

    # -- headroom and starting density, continuous ---------------------------
    for name in ("headroom", "start"):
        a = both[f"{name}_15"].to_numpy(float)
        b = both[f"{name}_60"].to_numpy(float)
        out[f"unpaired_{name}"] = {
            "median_15d": float(np.median(a)), "median_60d": float(np.median(b)),
            "mannwhitney_p": float(stats.mannwhitneyu(a, b).pvalue)}
        w = stats.wilcoxon(a, b)
        out[f"paired_{name}"] = {
            "median_within_isolate_change": float(np.median(b - a)),
            "n_pairs": int(len(a)),
            "n_increased": int((b > a).sum()), "n_decreased": int((b < a).sum()),
            "wilcoxon_p": float(w.pvalue), "wilcoxon_statistic": float(w.statistic)}

    # -- the spread of starting density, which Section 4 compares -------------
    a = both["start_15"].to_numpy(float)
    b = both["start_60"].to_numpy(float)
    def iqr(v):
        return float(np.percentile(v, 75) - np.percentile(v, 25))
    obs = iqr(b) - iqr(a)
    draws = np.array([iqr(b[i]) - iqr(a[i]) for i in
                      (rng.integers(0, len(a), size=(N_BOOT, len(a))))])
    out["iqr_start"] = {
        "iqr_15d": iqr(a), "iqr_60d": iqr(b), "difference": obs,
        "paired_bootstrap_ci": list(percentile_ci(draws)),
        "note": "isolates resampled as whole units so both panels move together"}
    return out


# ==========================================================================
# 4. the six-laboratory deposit: the nesting, counted
# ==========================================================================

def era_load() -> pd.DataFrame:
    d = pd.read_csv(ERA, encoding="latin-1")
    d["loq"] = np.log10(1000.0 / d["Volume"])
    d["censored"] = d["BQL"] == 1
    d["y_raw"] = pd.to_numeric(d["CFUlog10"], errors="coerce")
    d["y"] = np.where(d["censored"], d["loq"], d["y_raw"])
    d["arm"] = d["Group"].map(GROUPS)
    return d


def era_structure(d: pd.DataFrame) -> pd.DataFrame:
    """The nesting, level by level, with the fan-out at each step.

    (Institute, Sample, Replicate, Condition, Time) is the unique reading key --
    NOT (..., Volume, Time), because 10 uL is plated two ways, as four drops and
    as a single drop, and those are different readings with the same volume.
    696 keys collide if volume is used, and none if the plating format is.
    """
    key_vol = d.groupby(["Institute", "Sample", "Replicate", "Volume", "Time"]).size()
    key_cond = d.groupby(["Institute", "Sample", "Replicate", "Condition", "Time"]).size()
    treated = d[~d["Sample"].isin(["untreated", "Inoculum TKA"])]
    rows = [
        {"deposit": "ERA4TB six-laboratory", "level": 1, "unit": "reading (one plating)",
         "n_units": int(len(d)), "n_parents": int(d.groupby(
             ["Institute", "Sample", "Replicate", "Time"]).ngroups),
         "mean_per_parent": len(d) / d.groupby(
             ["Institute", "Sample", "Replicate", "Time"]).ngroups,
         "note": f"unique on institute+sample+replicate+plating format+time "
                 f"({(key_cond > 1).sum()} collisions); using volume instead "
                 f"collides {(key_vol > 1).sum()} times"},
        {"deposit": "ERA4TB six-laboratory", "level": 2, "unit": "flask-visit",
         "n_units": int(d.groupby(["Institute", "Sample", "Replicate", "Time"]).ngroups),
         "n_parents": int(d.groupby(["Institute", "Sample", "Replicate"]).ngroups),
         "mean_per_parent": d.groupby(["Institute", "Sample", "Replicate", "Time"]).ngroups
                            / d.groupby(["Institute", "Sample", "Replicate"]).ngroups,
         "note": "up to four platings of one culture at one time point"},
        {"deposit": "ERA4TB six-laboratory", "level": 3, "unit": "flask (replicate)",
         "n_units": int(d.groupby(["Institute", "Sample", "Replicate"]).ngroups),
         "n_parents": int(d.groupby(["Institute", "Sample"]).ngroups),
         "mean_per_parent": d.groupby(["Institute", "Sample", "Replicate"]).ngroups
                            / d.groupby(["Institute", "Sample"]).ngroups,
         "note": f"{int(treated.groupby(['Institute','Sample','Replicate']).ngroups)} "
                 f"of them in treated arms"},
        {"deposit": "ERA4TB six-laboratory", "level": 4, "unit": "treatment arm in a laboratory",
         "n_units": int(d.groupby(["Institute", "Sample"]).ngroups),
         "n_parents": int(d["Institute"].nunique()),
         "mean_per_parent": d.groupby(["Institute", "Sample"]).ngroups
                            / d["Institute"].nunique(),
         "note": "five arms per laboratory; institute E also deposits an inoculum check"},
        {"deposit": "ERA4TB six-laboratory", "level": 5, "unit": "laboratory",
         "n_units": int(d["Institute"].nunique()), "n_parents": 1,
         "mean_per_parent": float(d["Institute"].nunique()),
         "note": "THE ONLY LEVEL AT WHICH BETWEEN-LABORATORY CLAIMS REPLICATE. "
                 "Six clusters, one written protocol, one stock."},
    ]
    return pd.DataFrame(rows)


def survival_frame(d: pd.DataFrame) -> pd.DataFrame:
    """exp17's flask table: time to the first undetectable culture at 100 uL."""
    s = d[(d["Condition"] == 0) & d["y"].notna() & (d["Time"] >= 0) & (d["AQL"] == 0)]
    rows = []
    for (inst, grp, rep), g in s.groupby(["Institute", "Group", "Replicate"]):
        g = g.sort_values("Time")
        below = g[g["censored"]]
        start = g[(g["Time"] <= 1) & (~g["censored"])]["y"].mean()
        if len(below):
            t_ev, event = float(below["Time"].iloc[0]), 1
        else:
            t_ev, event = float(g["Time"].max()), 0
        rows.append({"institute": inst, "arm": GROUPS.get(grp), "replicate": int(rep),
                     "time_days": t_ev, "event": event,
                     "start_log10": float(start) if np.isfinite(start) else np.nan})
    return pd.DataFrame(rows)


# ==========================================================================
# 5. the recomputations that respect the nesting
# ==========================================================================

def clearance_vs_density(surv: pd.DataFrame, rng: np.random.Generator) -> dict:
    """Section 5's headline association, at four levels of analysis.

    NAIVE: 67 treated flasks as 67 independent draws.
    CLUSTER BOOTSTRAP: whole laboratories resampled; and, separately, whole
      flasks resampled within laboratory, which holds the six laboratories fixed
      and therefore measures flask noise only, not between-laboratory evidence.
    WITHIN-LABORATORY PERMUTATION: clearance shuffled among the flasks of each
      laboratory. This leaves the laboratory structure intact and asks what the
      starting density explains that the laboratory identity does not.
    WITHIN LABORATORY AND ARM: the same shuffle, restricted further so that
      flasks are only ever exchanged with flasks that met the same drug at the
      same multiple of the MIC. This is the level at which the flasks are
      genuinely exchangeable, because whether a flask clears depends first on
      what was put in it. It is also the test that matters, because the day 0 to
      1 "starting density" is not arm-neutral: at one times MIC the population
      grows over that window, so the arm that never clears also reads highest.
    LABORATORY-LEVEL EXACT TEST: six laboratories, three that cleared and three
      that did not. This is the comparison the flasks are standing in for.
    """
    t = surv[(surv["arm"] != "untreated") & surv["arm"].notna()].dropna(subset=["start_log10"])
    pos = t[t["event"] == 1]["start_log10"].to_numpy(float)
    neg = t[t["event"] == 0]["start_log10"].to_numpy(float)
    naive_auc = auc_from_ranks(pos, neg)
    naive_p = float(stats.mannwhitneyu(pos, neg).pvalue)

    labs = sorted(t["institute"].unique())
    # cluster bootstrap over whole laboratories
    boot = []
    for _ in range(N_BOOT):
        draw = rng.choice(labs, size=len(labs), replace=True)
        b = pd.concat([t[t["institute"] == L] for L in draw], ignore_index=True)
        a = auc_from_ranks(b[b["event"] == 1]["start_log10"].to_numpy(float),
                           b[b["event"] == 0]["start_log10"].to_numpy(float))
        if np.isfinite(a):
            boot.append(a)
    boot = np.array(boot)

    # cluster bootstrap over whole flasks WITHIN laboratory
    bootf = []
    for _ in range(N_BOOT):
        parts = []
        for L in labs:
            g = t[t["institute"] == L]
            parts.append(g.iloc[rng.integers(0, len(g), size=len(g))])
        b = pd.concat(parts, ignore_index=True)
        a = auc_from_ranks(b[b["event"] == 1]["start_log10"].to_numpy(float),
                           b[b["event"] == 0]["start_log10"].to_numpy(float))
        if np.isfinite(a):
            bootf.append(a)
    bootf = np.array(bootf)

    # restricted permutation of the clearance label, at two levels
    ev = t["event"].to_numpy(int)
    x = t["start_log10"].to_numpy(float)
    strata = {"laboratory": t["institute"].astype(str).to_numpy(),
              "laboratory and arm": (t["institute"].astype(str) + "|"
                                     + t["arm"].astype(str)).to_numpy()}
    perm_out = {}
    for name, key in strata.items():
        idx = [np.flatnonzero(key == g) for g in np.unique(key)]
        informative = [ix for ix in idx if 0 < ev[ix].sum() < len(ix)]
        arrangements = 1
        for ix in informative:
            arrangements *= comb(len(ix), int(ev[ix].sum()))
        null = np.empty(N_PERM)
        for i in range(N_PERM):
            e = ev.copy()
            for ix in informative:
                e[ix] = rng.permutation(e[ix])
            null[i] = auc_from_ranks(x[e == 1], x[e == 0])
        null = null[np.isfinite(null)]
        perm_out[name] = {
            "p_value": float((null >= naive_auc - 1e-12).mean()),
            "null_mean_auc": float(null.mean()),
            "null_95th_percentile": float(np.percentile(null, 95)),
            "n_strata": len(idx),
            "n_strata_with_both_outcomes": len(informative),
            "n_distinct_arrangements": int(arrangements),
            "smallest_attainable_p": 1.0 / arrangements if arrangements else np.nan,
        }

    # laboratory-level exact test: mean starting density, cleared labs vs not
    lab = (t.groupby("institute")
             .agg(mean_start=("start_log10", "mean"),
                  n_flasks=("event", "size"),
                  n_cleared=("event", "sum")).reset_index())
    lab["any_cleared"] = lab["n_cleared"] > 0
    lab["fraction_cleared"] = lab["n_cleared"] / lab["n_flasks"]
    a = lab.loc[lab["any_cleared"], "mean_start"].to_numpy(float)
    b = lab.loc[~lab["any_cleared"], "mean_start"].to_numpy(float)
    mw = stats.mannwhitneyu(a, b, alternative="two-sided", method="exact")
    mw1 = stats.mannwhitneyu(a, b, alternative="less", method="exact")
    # the smallest two-sided p a split this size can ever return
    floor_p = 2.0 / comb(len(lab), len(a))

    # exact permutation of the laboratory-level rank correlation, all 6! orders
    ms = lab["mean_start"].to_numpy(float)
    fc = lab["fraction_cleared"].to_numpy(float)
    obs_rho = float(stats.spearmanr(ms, fc).statistic)
    rhos = np.array([stats.spearmanr(np.array(p), fc).statistic
                     for p in permutations(ms)])
    p_exact_rho = float((np.abs(rhos) >= abs(obs_rho) - 1e-12).mean())

    return {
        "n_treated_flasks": int(len(t)), "n_cleared": int(len(pos)),
        "n_never_cleared": int(len(neg)), "n_laboratories": len(labs),
        "naive_auc": naive_auc, "naive_mannwhitney_p": naive_p,
        "cluster_bootstrap_labs_auc_ci": list(percentile_ci(boot)),
        "cluster_bootstrap_labs_n_usable": int(len(boot)),
        "cluster_bootstrap_flasks_within_lab_auc_ci": list(percentile_ci(bootf)),
        "cluster_bootstrap_flasks_note":
            "holds the six laboratories fixed, so it measures flask noise and "
            "carries no between-laboratory information",
        "restricted_permutation": perm_out,
        "within_laboratory_permutation_p": perm_out["laboratory"]["p_value"],
        "within_laboratory_and_arm_permutation_p":
            perm_out["laboratory and arm"]["p_value"],
        "laboratory_level_exact_p_two_sided": float(mw.pvalue),
        "laboratory_level_exact_p_one_sided": float(mw1.pvalue),
        "smallest_two_sided_p_this_design_can_return": float(floor_p),
        "laboratory_level_spearman_rho": obs_rho,
        "laboratory_level_spearman_exact_p": p_exact_rho,
        "laboratory_table": lab.to_dict(orient="records"),
    }


def variance_share_permutation(values: np.ndarray, groups: np.ndarray,
                               rng: np.random.Generator,
                               strata: np.ndarray | None = None) -> dict:
    """One-way between-group variance share, with a flask-level permutation.

    Under the null that the laboratory label carries nothing, flasks ARE
    exchangeable across laboratories, so permuting the label is exact up to Monte
    Carlo error. This is the one between-laboratory question in the deposit that
    six clusters can answer, because the replication that matters here is between
    flasks, not between laboratories.

    Pass `strata` to hold something else fixed -- for a kill rate the treatment
    arm, since a flask on ten times MIC and a flask on one times MIC are not
    exchangeable whatever laboratory they came from. Values are then centred
    within stratum and the label is permuted within stratum.
    """
    v = np.asarray(values, float)
    if strata is not None:
        v = v.copy()
        for s in np.unique(strata):
            m = strata == s
            v[m] = v[m] - v[m].mean()

    def share(g):
        grand = v.mean()
        ss_t = float(((v - grand) ** 2).sum())
        ss_b = float(sum(len(v[g == k]) * (v[g == k].mean() - grand) ** 2
                         for k in np.unique(g)))
        return ss_b / ss_t if ss_t else np.nan

    obs = share(groups)
    n_draw = N_PERM // 4
    if strata is None:
        null = np.array([share(rng.permutation(groups)) for _ in range(n_draw)])
    else:
        idx = [np.flatnonzero(strata == s) for s in np.unique(strata)]
        null = np.empty(n_draw)
        for i in range(n_draw):
            g = groups.copy()
            for ix in idx:
                g[ix] = rng.permutation(g[ix])
            null[i] = share(g)
    n_g = len(np.unique(groups))
    return {"n_units": int(len(v)), "n_groups": int(n_g),
            "stratified_by": None if strata is None else "treatment arm",
            "n_permutation_draws": int(n_draw),
            "smallest_p_these_draws_can_return": 1.0 / n_draw,
            "observed_share": float(obs),
            "expected_share_under_null": float((n_g - 1) / (len(v) - 1)),
            "permutation_p": float((null >= obs).mean()),
            "null_share_mean": float(np.mean(null)),
            "null_share_95th_percentile": float(np.percentile(null, 95))}


def pair_counts(f: pd.DataFrame, min_gap: float = 0.0) -> dict:
    """exp23's inversion count, on whatever flask table is handed in.

    Pairs are admitted only when the two flasks come from different ORIGINAL
    laboratories, so that a bootstrap draw holding the same laboratory twice does
    not manufacture spurious between-laboratory comparisons out of one.
    """
    origin = f["origin"] if "origin" in f.columns else f["institute"]
    slot = f["slot"] if "slot" in f.columns else f["institute"]
    n = k = correct = 0
    for arm, g in f.groupby("arm"):
        idx = list(g.index)
        for i, j in combinations(idx, 2):
            if origin[i] == origin[j] or slot[i] == slot[j]:
                continue
            A, B = f.loc[i], f.loc[j]
            fast, slow = ((A, B) if A["rate_log10_per_day"] > B["rate_log10_per_day"]
                          else (B, A))
            if fast["rate_log10_per_day"] - slow["rate_log10_per_day"] < min_gap:
                continue
            if fast["cleared"] and slow["cleared"]:
                later = fast["observed_clearance_day"] > slow["observed_clearance_day"]
            elif ((not fast["cleared"]) and slow["cleared"]
                  and slow["observed_clearance_day"] <= fast["horizon_day"]):
                later = True
            elif (fast["cleared"] and (not slow["cleared"])
                  and fast["observed_clearance_day"] <= slow["horizon_day"]):
                later = False
            else:
                continue
            n += 1
            k += bool(later)
            pred = (fast["distance_to_limit_log10"] / slow["distance_to_limit_log10"]
                    > fast["rate_log10_per_day"] / slow["rate_log10_per_day"])
            correct += bool(pred == bool(later))
    return {"n_pairs": n, "n_inversions": k,
            "rate": k / n if n else np.nan,
            "correct_call_rate": correct / n if n else np.nan}


def inversion_uncertainty(f: pd.DataFrame, rng: np.random.Generator,
                          min_gap: float = 0.0) -> dict:
    f = f.copy()
    f["origin"] = f["institute"]
    f["slot"] = f["institute"]
    naive = pair_counts(f, min_gap)
    n, k = naive["n_pairs"], naive["n_inversions"]
    lo, hi = stats.beta.ppf([0.025, 0.975], k + 0.5, n - k + 0.5)

    labs = sorted(f["institute"].unique())

    def resample_labs():
        draw = rng.choice(labs, size=len(labs), replace=True)
        parts = []
        for s, L in enumerate(draw):
            g = f[f["institute"] == L].copy()
            g["slot"] = s
            g["origin"] = L
            parts.append(g)
        return pd.concat(parts, ignore_index=True)

    def resample_flasks():
        parts = []
        for L in labs:
            g = f[f["institute"] == L]
            h = g.iloc[rng.integers(0, len(g), size=len(g))].copy()
            h["slot"] = L
            h["origin"] = L
            parts.append(h)
        return pd.concat(parts, ignore_index=True)

    bl_res = [pair_counts(resample_labs(), min_gap) for _ in range(N_BOOT_PAIRS)]
    bl = np.array([r["rate"] for r in bl_res])
    cl = np.array([r["correct_call_rate"] for r in bl_res])
    bf = np.array([pair_counts(resample_flasks(), min_gap)["rate"]
                   for _ in range(N_BOOT_PAIRS)])

    def stat(keys):
        g = f[f["institute"].isin(keys)]
        return pair_counts(g, min_gap)["rate"]
    jk = cluster_jackknife({L: L for L in labs}, stat)

    return {
        "min_rate_gap": min_gap,
        "naive_n_pairs": n, "naive_n_inversions": k, "naive_rate": naive["rate"],
        "naive_jeffreys_ci": [float(lo), float(hi)],
        "naive_correct_call_rate": naive["correct_call_rate"],
        "cluster_bootstrap_labs_ci": list(percentile_ci(bl)),
        "cluster_bootstrap_labs_median_pairs_per_draw":
            float(np.median([r["n_pairs"] for r in bl_res])),
        "cluster_bootstrap_flasks_within_lab_ci": list(percentile_ci(bf)),
        "leave_one_laboratory_out_ci": [jk["ci_low"], jk["ci_high"]],
        "leave_one_laboratory_out_se": jk["se"],
        "leave_one_laboratory_out_note":
            "a delete-one-cluster jackknife on a pairwise statistic with six "
            "clusters; where the interval runs outside [0, 1] that is the result, "
            "not a bug -- the normal approximation has nothing to stand on",
        "cluster_bootstrap_correct_call_ci": list(percentile_ci(cl)),
        "n_bootstrap_draws": N_BOOT_PAIRS,
        "n_clusters": len(labs),
    }


def proportion_cluster_ci(flags: pd.Series, labs: pd.Series,
                          rng: np.random.Generator) -> dict:
    """A proportion over units nested in six laboratories, both ways."""
    x = flags.to_numpy(bool)
    g = labs.to_numpy()
    p = float(x.mean())
    n = len(x)
    lo, hi = stats.beta.ppf([0.025, 0.975], x.sum() + 0.5, n - x.sum() + 0.5)
    keys = sorted(pd.unique(g))
    boot = []
    for _ in range(N_BOOT):
        draw = rng.choice(keys, size=len(keys), replace=True)
        v = np.concatenate([x[g == L] for L in draw])
        boot.append(v.mean())
    return {"n": n, "n_laboratories": len(keys), "proportion": p,
            "naive_jeffreys_ci": [float(lo), float(hi)],
            "cluster_bootstrap_labs_ci": list(percentile_ci(np.array(boot)))}


def lab_level_spread_ci(values: np.ndarray, rng: np.random.Generator) -> dict:
    """A max-minus-min over laboratories: what six clusters can say about a range.

    A range is the worst statistic to bootstrap, because a resample with
    replacement can only ever lose extremes, so the interval is pulled downward.
    It is reported anyway, with the between-laboratory standard deviation beside
    it as the dispersion measure that does not have that defect.
    """
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    draws = rng.integers(0, len(v), size=(N_BOOT, len(v)))
    rng_stat = np.array([v[i].max() - v[i].min() for i in draws])
    sd_stat = np.array([v[i].std(ddof=1) for i in draws])
    return {"n_laboratories": int(len(v)),
            "observed_range": float(v.max() - v.min()),
            "cluster_bootstrap_range_ci": list(percentile_ci(rng_stat)),
            "observed_between_lab_sd": float(v.std(ddof=1)),
            "cluster_bootstrap_sd_ci": list(percentile_ci(sd_stat))}


def cox_cluster_diagnosis(surv: pd.DataFrame) -> dict:
    """Why Section 5's Cox p-values have no cluster-robust version.

    The cluster-robust ("sandwich") variance sums one outer product per cluster,
    so its rank is at most the number of clusters, and at most G-1 once the
    scores are centred. Section 5 fits five institute dummies plus starting
    density: six parameters against a meat matrix of rank at most five. The
    robust covariance is singular by construction. Nor is there a permutation
    fallback, because each laboratory appears exactly once, so permuting the
    laboratory label permutes whole laboratories onto themselves and the
    statistic never moves. The honest report is that the design does not support
    a between-laboratory p-value.

    Two halves, and they are different kinds of evidence. The rank bound is
    arithmetic and is reported as such: G outer products, G - 1 of them free
    once the scores are centred, against six parameters. The fit below carries a
    ridge penalty, so its scores do not centre exactly and the sandwich need not
    be numerically singular -- which is the point. The estimator does not fail
    loudly when the clusters run out. It returns a standard error that has
    collapsed, and that collapse is what this function measures.
    """
    t = surv[(surv["arm"] != "untreated") & surv["arm"].notna()].dropna(subset=["start_log10"])
    labs = sorted(t["institute"].unique())
    n_par = (len(labs) - 1) + 1
    out = {"n_clusters": len(labs), "n_parameters": n_par,
           "max_rank_of_cluster_robust_meat": len(labs) - 1,
           "cluster_robust_wald_available": bool(len(labs) - 1 >= n_par),
           "institute_constant_within_cluster": True,
           "n_flasks": int(len(t))}
    try:
        from lifelines import CoxPHFitter
        df = pd.get_dummies(t[["institute", "start_log10", "time_days", "event"]],
                            columns=["institute"], drop_first=True, dtype=float)
        cph = CoxPHFitter(penalizer=0.1)
        cph.fit(df, duration_col="time_days", event_col="event",
                cluster_col=None)
        out["naive_institute_p"] = {c: float(cph.summary.loc[c, "p"])
                                    for c in cph.summary.index if c.startswith("institute_")}
        df2 = df.copy()
        df2["cluster"] = t["institute"].to_numpy()
        try:
            cph2 = CoxPHFitter(penalizer=0.1)
            cph2.fit(df2, duration_col="time_days", event_col="event",
                     cluster_col="cluster")
            out["cluster_robust_institute_p"] = {
                c: float(cph2.summary.loc[c, "p"]) for c in cph2.summary.index
                if c.startswith("institute_")}
            out["cluster_robust_fit"] = "converged, but see max_rank: the reported " \
                                        "standard errors are not trustworthy with six clusters"
        except Exception as exc:
            out["cluster_robust_fit"] = f"failed: {type(exc).__name__}: {exc}"
    except ImportError:
        out["cluster_robust_fit"] = "lifelines not installed"
    return out


def _worst_robust(cox: dict) -> str:
    """The smallest cluster-robust p the singular sandwich produces.

    Quoted because it is absurd, and the absurdity is the evidence: a variance
    estimator with fewer clusters than parameters does not fail loudly, it
    returns a standard error that has collapsed, and the p-value that follows is
    smaller than the one it was meant to correct.
    """
    d = cox.get("cluster_robust_institute_p")
    if not d:
        return "no fit"
    term = min(d, key=d.get)
    return (f"a smallest robust p of {d[term]:.1e} for "
            f"{term.replace('institute_', 'institute ')}")


# ==========================================================================
# main
# ==========================================================================

def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    for f in (TB, ERA):
        if not f.exists():
            raise SystemExit(f"missing {f}; see the docstring for its source")
    needed = {"flask": TABLES / "exp23_flask_parameters.csv",
              "traj": TABLES / "exp24_trajectory_shape.csv",
              "flags": TABLES / "exp24_flag_consistency.csv",
              "rates": TABLES / "exp17_kill_rates.csv"}
    for k, p in needed.items():
        if not p.exists():
            raise SystemExit(f"missing {p}; run exp17, exp23 and exp24 first")

    rng = np.random.default_rng(SEED)
    pd.set_option("display.width", 220)

    # ---------------------------------------------------------------- clinical
    d = clinical_load()
    struct_tb, cstruct = clinical_structure(d)
    keyhunt = hunt_for_a_patient_key(d)
    cstruct["columns_matching_a_patient_key_signature"] = \
        keyhunt.loc[keyhunt["matches_patient_key_signature"], "column"].tolist()

    full = clinical_panel(d, 15)
    base = clinical_panel(d[d["baseline"]], 15)
    fam_all = mic_mdk_family(d)
    fam_base = mic_mdk_family(d[d["baseline"]])
    paired = paired_panels(d, rng)

    # ---------------------------------------------------------------- ERA4TB
    e = era_load()
    struct_era = era_structure(e)
    surv = survival_frame(e)
    clearance = clearance_vs_density(surv, rng)
    cox = cox_cluster_diagnosis(surv)

    # starting density: how much of it is the laboratory, and is that testable
    s = e[(e["Volume"] == MOST_SENSITIVE_UL) & (~e["censored"]) & (e["AQL"] != 1)
          & (e["Time"] <= 1) & (e["Time"] >= 0)].dropna(subset=["y"])
    per_flask = (s.groupby(["Institute", "Sample", "Replicate"])["y"].mean().reset_index())
    dens = variance_share_permutation(per_flask["y"].to_numpy(float),
                                      per_flask["Institute"].to_numpy(), rng)

    dens_arm = variance_share_permutation(
        per_flask["y"].to_numpy(float), per_flask["Institute"].to_numpy(), rng,
        strata=per_flask["Sample"].to_numpy())

    flask = pd.read_csv(needed["flask"])
    rate_share = variance_share_permutation(
        np.log(flask["rate_log10_per_day"].to_numpy(float)),
        flask["institute"].to_numpy(), rng,
        strata=flask["arm"].to_numpy())

    inv_all = inversion_uncertainty(flask, rng, 0.0)
    inv_strict = inversion_uncertainty(flask, rng, 0.10)

    rates = pd.read_csv(needed["rates"])
    mxf10 = rates[rates["arm"] == "MXF 10x MIC"].dropna(subset=["kill_rate_tobit"])
    kill_spread = lab_level_spread_ci(np.log10(mxf10["kill_rate_tobit"].to_numpy(float)), rng)
    kill_spread["observed_fold_range"] = float(10 ** kill_spread["observed_range"])
    kill_spread["cluster_bootstrap_fold_range_ci"] = [
        float(10 ** v) for v in kill_spread["cluster_bootstrap_range_ci"]]
    mxf1 = rates[rates["arm"] == "MXF 1x MIC"].dropna(subset=["kill_rate_tobit"])
    n_growth = int((mxf1["kill_rate_tobit"] < 0).sum())
    growth_ci = stats.beta.ppf([0.025, 0.975], n_growth + 0.5, len(mxf1) - n_growth + 0.5)

    # headroom between laboratories at one plating volume (Section 6)
    u = e[(~e["censored"]) & (e["AQL"] != 1) & (e["Sample"] == "untreated")
          & (e["Time"] == 0)].dropna(subset=["y_raw"])
    h100 = (u[u["Volume"] == 100.0].groupby("Institute")["y_raw"].mean() - 1.0)
    dh = lab_level_spread_ci(h100.to_numpy(float), rng)
    # WHY the roster is four and not six, laboratory by laboratory. The two
    # absences are not the same kind of absence and the difference is worth a
    # sentence: one laboratory never deposits an untreated day-zero row at all,
    # while another deposits one at 100 uL and marks it above the quantification
    # limit, which is a measurable depth censored from above, not a missing
    # measurement. Derived here rather than asserted, because it is the count
    # Section 6 is cited against.
    d0 = e[(e["Sample"] == "untreated") & (e["Time"] == 0)]
    d0_100 = d0[d0["Volume"] == MOST_SENSITIVE_UL]
    h100_absent = sorted(set(e["Institute"].unique()) - set(d0["Institute"].unique()))
    h100_uncountable = sorted(
        set(d0_100.loc[d0_100["AQL"] == 1, "Institute"].unique()) - set(h100.index))
    dh["laboratories_used"] = sorted(h100.index)
    dh["laboratories_with_no_untreated_day_zero_row"] = h100_absent
    dh["laboratories_whose_day_zero_100ul_row_is_above_the_limit"] = h100_uncountable
    dh["n_day_zero_100ul_rows_above_the_limit"] = int((d0_100["AQL"] == 1).sum())

    traj = pd.read_csv(needed["traj"])
    term = proportion_cluster_ci(~traj["terminal_step_is_decline"], traj["institute"], rng)
    reb = proportion_cluster_ci(traj["rebounds"], traj["institute"], rng)
    flags = pd.read_csv(needed["flags"])
    flagp = proportion_cluster_ci(flags["contradicted"], flags["institute"], rng)

    # ------------------------------------------------------- structure table
    structure = pd.concat([struct_tb, struct_era], ignore_index=True)
    structure.to_csv(TABLES / "exp31_clustering_structure.csv", index=False)

    # -------------------------------------------------- baseline-only table
    def row(q, a, b, note=""):
        return {"quantity": q, "all_isolates": a, "baseline_only": b, "note": note}

    bl_rows = [
        row("isolates analysed", full["n_rows"], base["n_rows"],
            "Time_point == '0M'; the 43 follow-ups are the only rows that can "
            "repeat a patient"),
        row("short of 4-log headroom, n", full["n_short_of_4_logs"],
            base["n_short_of_4_logs"], "Section 1"),
        row("short of 4-log headroom, %", round(full["pct_short_of_4_logs"], 2),
            round(base["pct_short_of_4_logs"], 2), "Section 1"),
        row("of those, at the MDK ceiling", round(full["fraction_at_ceiling_short"], 4),
            round(base["fraction_at_ceiling_short"], 4), "Section 1"),
        row("with ample headroom, at the ceiling",
            round(full["fraction_at_ceiling_ample"], 4),
            round(base["fraction_at_ceiling_ample"], 4), "Section 1"),
        row("ceiling Fisher p", f"{full['ceiling_fisher_p']:.4g}",
            f"{base['ceiling_fisher_p']:.4g}",
            "the only clinical p-value in Section 1"),
        row("isolates at the assay floor", full["n_at_floor"], base["n_at_floor"],
            "Section 2"),
        row("their starting-density fold range",
            round(full.get("at_floor_start_fold_range", np.nan), 1),
            round(base.get("at_floor_start_fold_range", np.nan), 1), "Section 2"),
        row("their recorded-survival fold range",
            round(full.get("at_floor_survival_fold_range", np.nan), 1),
            round(base.get("at_floor_survival_fold_range", np.nan), 1),
            "identical to the line above by construction"),
        row("tolerance calls classified", full["n_calls"], base["n_calls"], "Section 2"),
        row("determinable", full["determinable"], base["determinable"], "Section 2"),
        row("forced by inoculum", full["forced_by_inoculum"], base["forced_by_inoculum"],
            "Section 2"),
        row("undecidable", full["undecidable"], base["undecidable"], "Section 2"),
        row("deep endpoint unreachable, resistant %",
            round(full["pct_unreachable_IR"], 2), round(base["pct_unreachable_IR"], 2),
            "Section 2"),
        row("deep endpoint unreachable, susceptible %",
            round(full["pct_unreachable_IS"], 2), round(base["pct_unreachable_IS"], 2),
            "Section 2"),
        row("unreachable Fisher p", f"{full['unreachable_fisher_p']:.4g}",
            f"{base['unreachable_fisher_p']:.4g}", "Section 2"),
        row("resistant start lower, fold", round(full["start_fold_lower_in_IR"], 2),
            round(base["start_fold_lower_in_IR"], 2), "Section 4"),
        row("that gap, Mann-Whitney p", f"{full['start_mannwhitney_p']:.3g}",
            f"{base['start_mannwhitney_p']:.3g}", "Section 4"),
        row("resistance coefficient, unadjusted", round(full["resistance_beta"], 4),
            round(base["resistance_beta"], 4), "Section 4"),
        row("resistance p, unadjusted", f"{full['resistance_p']:.4g}",
            f"{base['resistance_p']:.4g}", "Section 4"),
        row("resistance coefficient, adjusted",
            round(full["resistance_beta_adjusted"], 4),
            round(base["resistance_beta_adjusted"], 4), "Section 4"),
        row("resistance p, adjusted", f"{full['resistance_p_adjusted']:.4g}",
            f"{base['resistance_p_adjusted']:.4g}", "Section 4"),
        row("attenuation of the resistance coefficient",
            round(full["resistance_attenuation"], 4),
            round(base["resistance_attenuation"], 4), "Section 4"),
        row("growth coefficient, adjusted", round(full["growth_beta_adjusted"], 4),
            round(base["growth_beta_adjusted"], 4), "Section 4"),
        row("growth p, adjusted", f"{full['growth_p_adjusted']:.4g}",
            f"{base['growth_p_adjusted']:.4g}", "Section 4"),
        row("resistant grow more slowly, p", f"{full['growth_mannwhitney_p']:.3g}",
            f"{base['growth_mannwhitney_p']:.3g}", "Section 4, a null"),
        row("MIC-MDK tests surviving BH", fam_all["n_surviving_bh"],
            fam_base["n_surviving_bh"],
            f"Section 10; {fam_all['n_tests']} vs {fam_base['n_tests']} tests"),
    ]
    bl = pd.DataFrame(bl_rows)
    bl.to_csv(TABLES / "exp31_baseline_only_sensitivity.csv", index=False)

    # ------------------------------------------------- the deliverable table
    def V(x, n=3):
        return "n/a" if x is None or (isinstance(x, float) and not np.isfinite(x)) \
            else (f"{x:.{n}g}" if isinstance(x, float) else str(x))

    def ci(pair, n=3):
        return f"[{V(pair[0], n)}, {V(pair[1], n)}]"

    R = []

    def add(deposit, section, conclusion, unit, clustering, n_naive, n_clust,
            naive_est, naive_unc, method, cl_est, cl_unc, verdict, note):
        R.append({"deposit": deposit, "manuscript_section": section,
                  "conclusion": conclusion,
                  "unit_treated_as_independent": unit,
                  "actual_clustering": clustering,
                  "n_naive_units": n_naive, "n_independent_clusters": n_clust,
                  "naive_estimate": naive_est, "naive_uncertainty": naive_unc,
                  "clustered_method": method,
                  "clustered_estimate": cl_est, "clustered_uncertainty": cl_unc,
                  "verdict": verdict, "note": note})

    # --- clinical -----------------------------------------------------------
    add("Vijay clinical", "1",
        "33 of 217 isolates (15.2%) lack the headroom for a 4-log endpoint",
        "isolate", "up to 43 follow-ups repeat a patient", 217, "174 patients min",
        f"{full['n_short_of_4_logs']} ({full['pct_short_of_4_logs']:.1f}%)",
        "none (a count)", "baseline-only recount",
        f"{base['n_short_of_4_logs']} of {base['n_rows']} "
        f"({base['pct_short_of_4_logs']:.1f}%)", "none (a count)",
        "SUPPORTED", "a census of the deposit, not an estimate; the share barely moves")

    add("Vijay clinical", "1",
        "all 33 short isolates are at the ceiling; 88.0% of the rest are "
        "(Fisher p = 0.030)",
        "isolate", "up to 43 follow-ups repeat a patient", 217, "174 patients min",
        f"{full['fraction_at_ceiling_short']:.3f} vs {full['fraction_at_ceiling_ample']:.3f}",
        f"Fisher p = {full['ceiling_fisher_p']:.3f}",
        "baseline-only Fisher exact",
        f"{base['fraction_at_ceiling_short']:.3f} vs {base['fraction_at_ceiling_ample']:.3f}",
        f"Fisher p = {base['ceiling_fisher_p']:.3f}",
        "WEAKENED" if base["ceiling_fisher_p"] >= 0.05 else "SUPPORTED",
        "the contrast is 100% against 88%, which no test can make large; "
        "the count, not the p-value, is what Section 1 needs")

    add("Vijay clinical", "2",
        "18 isolates at the floor; their survival span IS their inoculum span",
        "isolate", "up to 43 follow-ups repeat a patient", 217, "174 patients min",
        f"{full['n_at_floor']} isolates, "
        f"{full.get('at_floor_start_fold_range', np.nan):.0f}-fold",
        "none (an identity)", "baseline-only recount",
        f"{base['n_at_floor']} isolates, "
        f"{base.get('at_floor_start_fold_range', np.nan):.0f}-fold",
        "none (an identity)", "SUPPORTED",
        "L/N0 is arithmetic; clustering cannot touch it")

    add("Vijay clinical", "2",
        "185 determinable, 12 forced by the inoculum, 6 undecidable",
        "isolate", "up to 43 follow-ups repeat a patient", 203, "174 patients min",
        f"{full['determinable']}/{full['forced_by_inoculum']}/{full['undecidable']}",
        "none (a count)", "baseline-only reclassification",
        f"{base['determinable']}/{base['forced_by_inoculum']}/{base['undecidable']}"
        f" of {base['n_calls']}", "none (a count)", "SUPPORTED",
        "the split is a deterministic function of N0 and L")

    add("Vijay clinical", "2 / 4",
        "the deep endpoint is unreachable for 26.2% of resistant against 7.6% of "
        "susceptible isolates",
        "isolate", "up to 43 follow-ups repeat a patient", 217, "174 patients min",
        f"{full['pct_unreachable_IR']:.1f}% vs {full['pct_unreachable_IS']:.1f}%",
        f"Fisher p = {full['unreachable_fisher_p']:.2g}",
        "baseline-only Fisher exact",
        f"{base['pct_unreachable_IR']:.1f}% vs {base['pct_unreachable_IS']:.1f}%",
        f"Fisher p = {base['unreachable_fisher_p']:.2g}",
        "SUPPORTED" if base["unreachable_fisher_p"] < 0.05 else "WEAKENED",
        "survives on one isolate per patient with room to spare")

    add("Vijay clinical", "4",
        "resistant isolates enter the assay ten-fold lower",
        "isolate", "up to 43 follow-ups repeat a patient", 217, "174 patients min",
        f"{full['start_fold_lower_in_IR']:.1f}-fold",
        f"Mann-Whitney p = {full['start_mannwhitney_p']:.2g}",
        "baseline-only Mann-Whitney",
        f"{base['start_fold_lower_in_IR']:.1f}-fold",
        f"p = {base['start_mannwhitney_p']:.2g}",
        "SUPPORTED" if base["start_mannwhitney_p"] < 1e-6 else "WEAKENED",
        "the largest effect in the clinical deposit and the least fragile")

    add("Vijay clinical", "4",
        "the resistance-tolerance association attenuates once starting density "
        "enters the model, and its interval "
        "then spans zero",
        "isolate", "up to 43 follow-ups repeat a patient",
        full.get("n_association"), "174 patients min",
        f"beta {full['resistance_beta']:.3f} -> {full['resistance_beta_adjusted']:.3f}",
        f"p {full['resistance_p']:.3g} -> {full['resistance_p_adjusted']:.3g}",
        "baseline-only refit",
        f"beta {base['resistance_beta']:.3f} -> {base['resistance_beta_adjusted']:.3f}",
        f"p {base['resistance_p']:.3g} -> {base['resistance_p_adjusted']:.3g}",
        "SUPPORTED" if (base["resistance_p"] < 0.05
                        and base["resistance_p_adjusted"] >= 0.05) else "WEAKENED",
        f"attenuation {100*base['resistance_attenuation']:.0f}% on baselines only")

    add("Vijay clinical", "4",
        "growth state predicts the tolerance class and survives adjustment "
        "(beta = +0.027, p = 0.0025)",
        "isolate", "up to 43 follow-ups repeat a patient",
        full.get("n_association"), "174 patients min",
        f"beta {full['growth_beta_adjusted']:.4f}",
        f"p = {full['growth_p_adjusted']:.3g}", "baseline-only refit",
        f"beta {base['growth_beta_adjusted']:.4f}",
        f"p = {base['growth_p_adjusted']:.3g}",
        "SUPPORTED" if base["growth_p_adjusted"] < 0.05 else "WEAKENED",
        "the surviving association of Section 4")

    add("Vijay clinical", "4",
        "resistant isolates do not grow measurably more slowly (p = 0.24)",
        "isolate", "up to 43 follow-ups repeat a patient", 217, "174 patients min",
        f"median {full['growth_median_IR']:.0f} vs {full['growth_median_IS']:.0f}",
        f"p = {full['growth_mannwhitney_p']:.2g}", "baseline-only Mann-Whitney",
        f"median {base['growth_median_IR']:.0f} vs {base['growth_median_IS']:.0f}",
        f"p = {base['growth_mannwhitney_p']:.2g}", "SUPPORTED",
        "a null that stays a null; the follow-ups were not carrying it")

    add("Vijay clinical", "10",
        "no MIC-MDK association survives Benjamini-Hochberg",
        "isolate", "up to 43 follow-ups repeat a patient",
        f"{fam_all['n_tests']} tests", "174 patients min",
        f"{fam_all['n_nominal']} nominal, {fam_all['n_surviving_bh']} survive",
        f"smallest p = {fam_all['smallest_p']:.3g}",
        "baseline-only family of six",
        f"{fam_base['n_nominal']} nominal, {fam_base['n_surviving_bh']} survive",
        f"smallest p = {fam_base['smallest_p']:.3g}",
        "SUPPORTED" if fam_base["n_surviving_bh"] == 0 else "NOT SUPPORTED",
        "exp16 already carried a baseline-only stratum; this confirms it as a "
        "family in its own right")

    # --- the two panels -----------------------------------------------------
    ps, pl = paired["unpaired_short"], paired["paired_short"]
    nd = paired["paired_not_determinable"]
    add("Vijay clinical", "4",
        "the confound thins between panels: 15.2% short of headroom at 15 days "
        "against 3.3% at 60",
        "isolate-panel (each of 210 isolates counted once per panel)", "the two panels are the SAME isolates",
        f"{ps['N_15d']} + {ps['N_60d']}",
        f"{paired['n_isolates_in_both_panels']} isolates",
        f"{ps['n_15d']}/{ps['N_15d']} vs {ps['n_60d']}/{ps['N_60d']}",
        f"unpaired Fisher p = {ps['fisher_p']:.3g}",
        "exact McNemar on the paired binary",
        f"{pl['n_only_first']} lost it, {pl['n_only_second']} gained it, "
        f"{pl['n_both']} short in both",
        f"McNemar p = {pl['p_value']:.3g}",
        "SUPPORTED",
        f"the paired test is the correct one and it is {'sharper' if pl['p_value'] < ps['fisher_p'] else 'no weaker'}: "
        f"{pl['n_only_first']} isolates lose their shortfall between panels and "
        f"{pl['n_only_second']} acquire one, so the change is within-isolate and "
        f"one-directional. The unpaired Fisher test was spending the concordant "
        f"isolates as though they were evidence.")

    pa, pb = paired["unpaired_at_floor"], paired["paired_at_floor"]
    add("Vijay clinical", "1 / 2",
        "18 isolates rest on the floor at 15 days and 6 at 60",
        "isolate-panel (each of 210 isolates counted once per panel)", "the two panels are the SAME isolates",
        f"{pa['N_15d']} + {pa['N_60d']}",
        f"{paired['n_isolates_in_both_panels']} isolates",
        f"{pa['n_15d']} vs {pa['n_60d']}",
        f"unpaired Fisher p = {pa['fisher_p']:.3g}",
        "exact McNemar on the paired binary",
        f"{pb['n_only_first']} vs {pb['n_only_second']} discordant",
        f"McNemar p = {pb['p_value']:.3g}",
        "SUPPORTED" if pb["p_value"] < 0.05 else "WEAKENED",
        "same direction; the paired test is the correct one and it agrees")

    add("Vijay clinical", "2",
        "at 60 days the observability counts are 191, 6 and none, 'because the "
        "cultures are denser and few readings reach the floor'",
        "isolate-panel (each of 210 isolates counted once per panel)", "the two panels are the SAME isolates",
        f"{full['n_calls']} + {nd['n_pairs']}", f"{nd['n_pairs']} isolates",
        f"{nd['n_not_determinable_15d']} not determinable at 15 d vs "
        f"{nd['n_not_determinable_60d']} at 60 d",
        "no test reported",
        "exact McNemar on the paired binary",
        f"{nd['n_only_first']} isolates lose determinability going the other "
        f"way, {nd['n_only_second']} gain it",
        f"McNemar p = {nd['p_value']:.3g}", "SUPPORTED",
        "the mechanism claim -- the confound is a property of a thin assay -- "
        "is a within-isolate claim and should be tested as one. It is, and it "
        "holds one-directionally.")

    ph, pw = paired["unpaired_headroom"], paired["paired_headroom"]
    add("Vijay clinical", "4",
        "the 60-day cultures are denser, so headroom is larger there",
        "isolate-panel (each of 210 isolates counted once per panel)", "the two panels are the SAME isolates",
        f"{2 * paired['n_isolates_in_both_panels']} treated as independent",
        f"{paired['n_isolates_in_both_panels']} isolates",
        f"median {ph['median_15d']:.2f} vs {ph['median_60d']:.2f} log10",
        f"unpaired Mann-Whitney p = {ph['mannwhitney_p']:.3g}",
        "Wilcoxon signed-rank on the within-isolate change",
        f"median gain {pw['median_within_isolate_change']:.2f} log10 "
        f"({pw['n_increased']} up, {pw['n_decreased']} down)",
        f"signed-rank p = {pw['wilcoxon_p']:.3g}", "SUPPORTED",
        f"the naive p was the smaller of the two, and it was not a p-value about "
        f"anything: it compared 210 isolates with the same 210 isolates. The "
        f"signed-rank test asks the question that was meant -- does an isolate "
        f"gain headroom between panels -- and answers it for "
        f"{pw['n_increased']} isolates against {pw['n_decreased']}.")

    iq = paired["iqr_start"]
    add("Vijay clinical", "4",
        "the spread of starting densities more than halves between panels "
        "(IQR 1.00 to 0.42 log10)",
        "isolate-panel (each of 210 isolates counted once per panel)", "the two panels are the SAME isolates",
        f"{2 * paired['n_isolates_in_both_panels']}",
        f"{paired['n_isolates_in_both_panels']} isolates",
        f"IQR {iq['iqr_15d']:.2f} -> {iq['iqr_60d']:.2f}",
        "none reported in the manuscript",
        "paired bootstrap resampling whole isolates",
        f"difference {iq['difference']:.2f} log10",
        f"95% CI {ci(iq['paired_bootstrap_ci'], 2)}",
        "SUPPORTED" if iq["paired_bootstrap_ci"][1] < 0 else "WEAKENED",
        "the manuscript quoted this with no uncertainty at all; it now has one")

    add("Vijay clinical", "4",
        "the difference between panels in the growth association is itself "
        "supported (interaction p = 0.0072)",
        "isolate-panel (each of 210 isolates counted once per panel)", "the two panels are the SAME isolates",
        "unknown", f"{paired['n_isolates_in_both_panels']} isolates",
        "interaction p = 0.0072", "as quoted",
        "not recomputable", "no generating code found in this repository",
        "n/a", "NOT SUPPORTED",
        "grep over src/ finds no script that computes an interaction between "
        "panels, and no audit line pins it. It is also a between-panel "
        "comparison on repeated measures, so whatever produced it must be a "
        "within-isolate contrast. Recompute it or cut it.")

    # --- ERA4TB -------------------------------------------------------------
    add("ERA4TB six-laboratory", "5",
        "starting density separates flasks that ever crossed below the assay "
        "floor from those that never did (AUC 0.974, p = 1.2e-10)",
        "flask", "flasks nested in six laboratories; the exposure is "
                 "87% a laboratory-level variable",
        clearance["n_treated_flasks"], clearance["n_laboratories"],
        f"AUC {clearance['naive_auc']:.3f}",
        f"Mann-Whitney p = {clearance['naive_mannwhitney_p']:.2g}",
        "exact laboratory-level test (3 crossed vs 3 did not); cluster bootstrap "
        "over laboratories; permutation of crossing within laboratory, and "
        "within laboratory AND treatment arm",
        f"AUC {clearance['naive_auc']:.3f}, cluster-bootstrap 95% CI "
        f"{ci(clearance['cluster_bootstrap_labs_auc_ci'])}",
        f"laboratory-level exact p = "
        f"{clearance['laboratory_level_exact_p_two_sided']:.2f} two-sided "
        f"(floor {clearance['smallest_two_sided_p_this_design_can_return']:.2f}); "
        f"permutation within laboratory p "
        f"{pfmt(clearance['within_laboratory_permutation_p'], N_PERM)}; within "
        f"laboratory AND arm p = "
        f"{clearance['within_laboratory_and_arm_permutation_p']:.2f} on only "
        f"{clearance['restricted_permutation']['laboratory and arm']['n_strata_with_both_outcomes']} "
        f"informative strata of "
        f"{clearance['restricted_permutation']['laboratory and arm']['n_strata']}",
        "NOT SUPPORTED",
        "the estimate is fine; the p-value is not. Three laboratories cleared "
        "and three did not, and 0.10 is the smallest two-sided p a three-"
        "against-three split can return, so no arrangement of this deposit "
        "could have reached 0.05 at the level where the comparison lives. "
        "Holding the laboratory fixed the association still looks strong, but "
        "that shuffle leaves the treatment arm free, and the day 0 to 1 window "
        "used to measure the starting density is not arm-neutral: the arms "
        "treated at ten times MIC have already lost most of their population "
        "inside that window and they are the arms that clear, so the arm that "
        "never clears also reads highest. "
        "Hold the arm fixed as well and only two of 24 laboratory-arm cells "
        "still contain both outcomes -- six distinct arrangements, a smallest "
        "attainable p of 0.17. There is essentially no within-laboratory "
        "evidence in the deposit either way. The perfect ordering of the six "
        "laboratories is real and should be reported as an ordering; 1.2e-10 "
        "is an artefact of counting 67 flasks as 67 laboratories.")

    add("ERA4TB six-laboratory", "5",
        "in a Cox model, institutes D, E and F carry p = 0.015, 0.016, 0.015, "
        "which adjustment for starting density moves to 0.138, 0.172, 0.576",
        "flask", "flasks nested in six laboratories; the covariate is CONSTANT "
                 "within cluster",
        cox["n_flasks"], cox["n_clusters"],
        "p = 0.015 / 0.016 / 0.015 -> 0.138 / 0.172 / 0.576",
        "model-based Wald",
        "cluster-robust sandwich on six clusters",
        "no valid estimate", f"the meat matrix has rank at most "
        f"{cox['max_rank_of_cluster_robust_meat']} against "
        f"{cox['n_parameters']} parameters, so the robust covariance is "
        f"singular; and each laboratory appears once, so no permutation of the "
        f"laboratory label exists either. Fitting it anyway returns "
        f"{_worst_robust(cox)}, which is the collapse the rank argument "
        f"predicts, not a stronger result",
        "NOT SUPPORTED",
        "the design admits no between-laboratory p-value at all. The comparison "
        "of the two fits remains a legitimate DESCRIPTION -- adding a number "
        "makes the labels redundant -- but it must be reported without "
        "p-values, and Section 5 currently reports six of them.")

    logrank = pd.read_csv(TABLES / "exp17_cox.csv")
    lr = logrank[logrank["model"] == "log-rank across institutes"]
    lr_p = float(lr["p_value"].iloc[0]) if len(lr) else np.nan
    add("ERA4TB six-laboratory", "5",
        "the log-rank test separates the six laboratories on time to first crossing",
        "flask", "flasks nested in six laboratories; the tested label IS the "
                 "cluster",
        cox["n_flasks"], cox["n_clusters"],
        f"chi2 across institutes", f"p = {lr_p:.2g}",
        "none available: the grouping variable is the cluster",
        "n/a",
        "a log-rank test asks whether flasks drawn from different groups have "
        "different event times, and assumes flasks within a group are "
        "independent. Here they are three flasks of one arm in one laboratory.",
        "NOT SUPPORTED",
        "the same defect as the Cox p-values, in the simplest possible test. "
        "That laboratories differ in clearance is visible without a test: three "
        "produce no event at all.")

    add("ERA4TB six-laboratory", "5",
        "institute C remains distinguishable after adjustment (HR 5.27, p < 0.001)",
        "flask", "one laboratory, three flasks per arm", cox["n_flasks"],
        1, "HR 5.27", "p < 0.001", "none available",
        "n/a", "a single cluster cannot be tested against the others without "
               "between-cluster replication",
        "NOT SUPPORTED",
        "C is one laboratory. That it is also the fastest killer is corroborating "
        "evidence and should be reported as that, not as a hazard ratio with a "
        "p-value.")

    add("ERA4TB six-laboratory", "5",
        "at ten times MIC of moxifloxacin the kill rate spans 5.2-fold between "
        "laboratories (0.090 to 0.464)",
        "laboratory-arm cell", "six laboratories", 6, 6,
        f"{kill_spread['observed_fold_range']:.1f}-fold",
        "none reported",
        "cluster bootstrap over whole laboratories",
        f"{kill_spread['observed_fold_range']:.1f}-fold",
        f"95% CI {ci(kill_spread['cluster_bootstrap_fold_range_ci'], 2)}-fold; "
        f"between-laboratory SD of log10 rate "
        f"{kill_spread['observed_between_lab_sd']:.3f} "
        f"(95% CI {ci(kill_spread['cluster_bootstrap_sd_ci'], 2)})",
        "WEAKENED",
        "a range over six draws. The point estimate is right and the "
        "qualitative claim -- every laboratory produces a rate, and they are "
        "within an order of magnitude -- holds, but the figure 5.2 should "
        "carry its interval.")

    add("ERA4TB six-laboratory", "5",
        "at one times MIC five of six laboratories record net growth",
        "laboratory-arm cell", "six laboratories", 6, 6,
        f"{n_growth} of {len(mxf1)}", "none reported",
        "Jeffreys interval on six clusters",
        f"{n_growth}/{len(mxf1)} = {n_growth/len(mxf1):.2f}",
        f"95% CI [{growth_ci[0]:.2f}, {growth_ci[1]:.2f}]",
        "WEAKENED",
        "true as reported, but 'five of six' is a proportion with an interval "
        "running from about a third to nearly all; the claim that survives is "
        "that the drug does not kill at 1x, not a rate for the field.")

    add("ERA4TB six-laboratory", "5 / Limitations",
        "87.0% of the variance in flask starting density lies between "
        "laboratories",
        "flask", "flasks nested in six laboratories", dens["n_units"],
        dens["n_groups"], f"{100*dens['observed_share']:.1f}%",
        "none reported",
        "permutation of the laboratory label across flasks",
        f"{100*dens['observed_share']:.1f}%",
        f"permutation p {pfmt(dens['permutation_p'], N_PERM // 4)}; the null share for this "
        f"design is {100*dens['expected_share_under_null']:.1f}% and its 95th "
        f"percentile {100*dens['null_share_95th_percentile']:.1f}%; holding the "
        f"treatment arm fixed as well it is "
        f"{100*dens_arm['observed_share']:.1f}% (p = "
        f"{pfmt(dens_arm['permutation_p'], N_PERM // 4)})",
        "SUPPORTED",
        "the one between-laboratory claim with a valid exact test behind it, "
        "because flasks are exchangeable across laboratories under the null. "
        "It is also the claim that most limits this paper, which is the right "
        "way round.")

    add("ERA4TB six-laboratory", "7",
        "36.6% of 191 cross-laboratory pairs are inversions (95% CI 30.1-43.6)",
        "pair of flasks", "each flask enters many pairs; flasks nested in six "
                          "laboratories",
        inv_all["naive_n_pairs"], inv_all["n_clusters"],
        f"{100*inv_all['naive_rate']:.1f}%",
        f"Jeffreys 95% CI [{100*inv_all['naive_jeffreys_ci'][0]:.1f}, "
        f"{100*inv_all['naive_jeffreys_ci'][1]:.1f}]%",
        "cluster bootstrap over whole laboratories; also over flasks within "
        "laboratory; also delete-one-laboratory jackknife",
        f"{100*inv_all['naive_rate']:.1f}%",
        f"laboratories {ci([100*v for v in inv_all['cluster_bootstrap_labs_ci']], 3)}%; "
        f"flasks-within-laboratory "
        f"{ci([100*v for v in inv_all['cluster_bootstrap_flasks_within_lab_ci']], 3)}%; "
        f"jackknife "
        f"{ci([100*v for v in inv_all['leave_one_laboratory_out_ci']], 3)}%",
        "WEAKENED",
        "the naive interval treats 191 pairs built from 42 flasks in six "
        "laboratories as 191 independent Bernoulli trials. The estimate holds "
        "and the interval roughly doubles.")

    add("ERA4TB six-laboratory", "7",
        "under the strictest rate separation the inversion rate is 21.3% of 94 "
        "pairs (95% CI 13.9-30.3)",
        "pair of flasks", "each flask enters many pairs; flasks nested in six "
                          "laboratories",
        inv_strict["naive_n_pairs"], inv_strict["n_clusters"],
        f"{100*inv_strict['naive_rate']:.1f}%",
        f"Jeffreys 95% CI [{100*inv_strict['naive_jeffreys_ci'][0]:.1f}, "
        f"{100*inv_strict['naive_jeffreys_ci'][1]:.1f}]%",
        "cluster bootstrap over whole laboratories",
        f"{100*inv_strict['naive_rate']:.1f}%",
        f"laboratories "
        f"{ci([100*v for v in inv_strict['cluster_bootstrap_labs_ci']], 3)}%; "
        f"flasks-within-laboratory "
        f"{ci([100*v for v in inv_strict['cluster_bootstrap_flasks_within_lab_ci']], 3)}%",
        "WEAKENED",
        "'one comparison in five inverts under the strictest criterion the data "
        "supports' becomes a much softer statement once the interval respects "
        "six laboratories.")

    add("ERA4TB six-laboratory", "7",
        "the criterion D_A/D_B > b_A/b_B calls 83.8% of pairs correctly",
        "pair of flasks", "each flask enters many pairs; six laboratories",
        inv_all["naive_n_pairs"], inv_all["n_clusters"],
        f"{100*inv_all['naive_correct_call_rate']:.1f}%", "none reported",
        "cluster bootstrap over whole laboratories",
        f"{100*inv_all['naive_correct_call_rate']:.1f}%",
        f"95% CI {ci([100*v for v in inv_all['cluster_bootstrap_correct_call_ci']], 3)}%",
        "SUPPORTED",
        "the interval stays far above the 50% a coin would give, which is the "
        "comparison the claim needs")

    add("ERA4TB six-laboratory", "5 / 7",
        "the laboratory effect lands on the duration endpoint and not on the "
        "rate; the rate is 'far more reproducible'",
        "flask", "flasks nested in six laboratories, within treatment arm",
        rate_share["n_units"], rate_share["n_groups"],
        f"rate spans {kill_spread['observed_fold_range']:.1f}-fold and every "
        f"laboratory yields one; three of six yield no duration at all",
        "no test reported",
        "permutation of the laboratory label across flasks, within arm for the "
        "rate",
        f"laboratory explains {100*dens['observed_share']:.1f}% of the starting "
        f"density and {100*rate_share['observed_share']:.1f}% of the log kill "
        f"rate within arm",
        f"density permutation p {pfmt(dens['permutation_p'], N_PERM // 4)}; "
        f"rate permutation p {pfmt(rate_share['permutation_p'], N_PERM // 4)} "
        f"against a null share of {100*rate_share['null_share_mean']:.1f}%",
        "WEAKENED",
        "the comparative claim survives -- the laboratory owns nearly three "
        "times as much of the inoculum as of the rate, and it owns the duration "
        "endpoint outright, since three laboratories produce none. But the "
        "laboratory effect on the RATE is real and detectable once the "
        "treatment arm is held fixed, so 'the rate travels' must mean it "
        "travels better, not that it is laboratory-independent. Both tests are "
        "exact under exchangeability of flasks, which is the one "
        "between-laboratory question six clusters can actually answer.")

    add("ERA4TB six-laboratory", "6",
        "the deepest demonstrable kill differs by 2.33 log10 between "
        "laboratories at one plating volume",
        "day-zero reading", "readings nested in the laboratories that deposit "
                            "an untreated day-zero arm at 100 uL",
        int(u[u["Volume"] == 100.0].shape[0]), int(len(h100)),
        f"delta h = {dh['observed_range']:.2f} log10 "
        f"({10**dh['observed_range']:,.0f}-fold)",
        "none reported",
        "cluster bootstrap over whole laboratories",
        f"delta h = {dh['observed_range']:.2f} log10",
        f"95% CI {ci(dh['cluster_bootstrap_range_ci'], 2)} log10 over "
        f"{len(h100)} laboratories; between-laboratory SD "
        f"{dh['observed_between_lab_sd']:.2f} "
        f"(95% CI {ci(dh['cluster_bootstrap_sd_ci'], 2)})",
        "WEAKENED",
        f"the figure rests on {len(h100)} laboratories "
        f"({', '.join(sorted(h100.index))}), not the five Section 6 lists by "
        f"name and not the six of the exercise. The two that drop out drop out "
        f"for different reasons and only one of them is a missing deposit: "
        f"{', '.join(h100_absent) or 'none'} deposits no untreated day-zero row "
        f"at any volume, while {', '.join(h100_uncountable) or 'none'} deposits "
        f"three at 100 uL that are flagged above the quantification limit and "
        f"carry no colony count, so its measurable depth at this volume is "
        f"censored from above rather than absent. A max-minus-min over "
        f"{len(h100)} draws with a bootstrap lower bound near zero. The claim "
        f"that measurable depth varies materially under one protocol survives "
        f"and is corroborated by the plated-volume term, which is a design "
        f"choice rather than a sample; the number 2.33 should carry its "
        f"interval and its laboratory count.")

    add("ERA4TB six-laboratory", "6",
        "including the choice of plated volume widens the spread in measurable "
        "depth to 4.40 log10",
        "laboratory-by-volume channel", "the plated volume is a design choice, "
                                        "not a sampled cluster",
        "up to 4 volumes x 5 laboratories", 6,
        "delta h = 4.40 log10", "none reported",
        "no resampling required for the volume term",
        "delta h = 4.40 log10",
        "1.6 log10 of it is the volume alone (2.5 uL single drop against 100 uL "
        "quadruplicate), which is exact arithmetic on L = 1000/V and carries no "
        "sampling uncertainty at all",
        "SUPPORTED",
        "the strongest form of the Section 6 argument, and the one that does "
        "not depend on six clusters: the pipette moves the measurable floor by a "
        "known amount whatever the laboratory does. Lead with this rather than "
        "with the between-laboratory range.")

    add("ERA4TB six-laboratory", "5",
        "of 64 treated series the final step is not a decline in 48 (75%)",
        "series (one per treated flask)", "series nested in six laboratories",
        term["n"], term["n_laboratories"], f"{100*term['proportion']:.1f}%",
        f"Jeffreys 95% CI {ci([100*v for v in term['naive_jeffreys_ci']], 3)}%",
        "cluster bootstrap over whole laboratories",
        f"{100*term['proportion']:.1f}%",
        f"95% CI {ci([100*v for v in term['cluster_bootstrap_labs_ci']], 3)}%",
        "SUPPORTED", "the interval widens but stays a clear majority")

    add("ERA4TB six-laboratory", "5",
        "44 of 64 series end more than one log10 above their own nadir",
        "series (one per treated flask)", "series nested in six laboratories",
        reb["n"], reb["n_laboratories"], f"{100*reb['proportion']:.1f}%",
        f"Jeffreys 95% CI {ci([100*v for v in reb['naive_jeffreys_ci']], 3)}%",
        "cluster bootstrap over whole laboratories",
        f"{100*reb['proportion']:.1f}%",
        f"95% CI {ci([100*v for v in reb['cluster_bootstrap_labs_ci']], 3)}%",
        "WEAKENED" if reb["cluster_bootstrap_labs_ci"][0] < 0.5 else "SUPPORTED",
        "'usually a transient rather than an endpoint' needs the lower bound to "
        "stay above one in two")

    add("ERA4TB six-laboratory", "Methods",
        "83 of 498 below-limit flags (16.7%) are contradicted by another "
        "plating of the same sample at the same visit",
        "flag (one reading)", "readings within flask-visits within flasks "
                              "within six laboratories",
        flagp["n"], flagp["n_laboratories"], f"{100*flagp['proportion']:.1f}%",
        f"Jeffreys 95% CI {ci([100*v for v in flagp['naive_jeffreys_ci']], 3)}%",
        "cluster bootstrap over whole laboratories",
        f"{100*flagp['proportion']:.1f}%",
        f"95% CI {ci([100*v for v in flagp['cluster_bootstrap_labs_ci']], 3)}%",
        "SUPPORTED",
        "the methodological point is that the number is not zero, and the "
        "clustered interval excludes zero comfortably")

    rec = pd.DataFrame(R)
    rec.to_csv(TABLES / "exp31_recomputed_inference.csv", index=False)

    # ---------------------------------------------------------------- receipt
    receipt = {
        "script": "src/experiments/exp31_clustering_audit.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_sources": ["eLife 93243 supplementary file 2",
                         "ERA4TB standardised time-kill, figshare 19766083"],
        "tables_audited": [str(p.relative_to(ROOT)).replace("\\", "/")
                           for p in needed.values()],
        "seed": SEED, "n_bootstrap": N_BOOT,
        "n_bootstrap_pairwise_statistics": N_BOOT_PAIRS,
        "n_permutations": N_PERM,
        "clinical_clustering": cstruct,
        "clinical_full_panel_15d": full,
        "clinical_baseline_only_15d": base,
        "clinical_mic_mdk_family": {"all_rows": fam_all, "baseline_only": fam_base},
        "paired_panels": paired,
        "era4tb_clearance_vs_density": clearance,
        "era4tb_cox_cluster_diagnosis": cox,
        "era4tb_starting_density_variance": dens,
        "era4tb_starting_density_variance_within_arm": dens_arm,
        "era4tb_kill_rate_variance": rate_share,
        "era4tb_headroom_100ul_by_laboratory": {k: float(v) for k, v in h100.items()},
        "era4tb_inversions": {"all_pairs": inv_all, "strictest_gap": inv_strict},
        "era4tb_kill_rate_spread": kill_spread,
        "era4tb_headroom_spread_100ul": dh,
        "era4tb_trajectory_terminal_step": term,
        "era4tb_trajectory_rebound": reb,
        "era4tb_flag_contradiction": flagp,
        "verdicts": rec["verdict"].value_counts().to_dict(),
    }
    (RECEIPTS / "exp31_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str), encoding="utf-8")

    # ---------------------------------------------------------------- report
    print("=" * 96)
    print("THE CLINICAL DEPOSIT: WHAT REPEATS, AND WHAT CANNOT BE RECOVERED")
    print("=" * 96)
    print(f"   isolates                                    : {cstruct['n_isolates']}")
    print(f"   baseline (Time_point == '0M')               : {cstruct['n_baseline_isolates']}")
    print(f"   follow-up isolates from treated patients    : {cstruct['n_follow_up_isolates']}"
          f"  ({cstruct['n_continuation_phase_IR_CP']} IR-CP, "
          f"{cstruct['n_intensive_phase_IR_IP']} IR-IP, "
          f"{cstruct['n_follow_up_without_sequential_label']} unlabelled)")
    print(f"   rows that could share a patient with another : "
          f"{cstruct['n_rows_potentially_non_independent']} "
          f"({cstruct['pct_rows_potentially_non_independent']:.1f}%)")
    print(f"   distinct patients                            : "
          f"at least {cstruct['min_distinct_patients']}, and no column says which")
    none_of = f"none of {len(keyhunt)} deposited columns"
    print(f"   columns with a patient-key multiplicity      : "
          f"{cstruct['columns_matching_a_patient_key_signature'] or none_of}")
    print(f"   worst-case design effect                     : "
          f"{cstruct['worst_case_design_effect']:.3f} "
          f"(standard errors up to {100*(cstruct['worst_case_se_inflation']-1):.1f}% too small)")
    print("   The linkage is not in the deposit. A random effect for patient is "
          "therefore not\n   available, and none is invented. The baseline-only "
          "stratum is the exact version\n   of the same sensitivity analysis.")

    print("\n" + "=" * 96)
    print("BASELINE ISOLATES ONLY: EVERY LOAD-BEARING CLINICAL NUMBER, RECOUNTED")
    print("=" * 96)
    print(bl.to_string(index=False))

    print("\n" + "=" * 96)
    print("THE 15-DAY AND 60-DAY PANELS ARE ONE SET OF ISOLATES")
    print("=" * 96)
    print(f"   isolates in both panels: {paired['n_isolates_in_both_panels']}"
          f"  (only 15 d: {paired['n_only_15d']}, only 60 d: {paired['n_only_60d']})")
    print(f"   short of headroom  : unpaired Fisher p = {ps['fisher_p']:.3g}"
          f"   ->  exact McNemar p = {pl['p_value']:.3g} "
          f"({pl['n_only_first']} vs {pl['n_only_second']} discordant)")
    print(f"   reading at floor   : unpaired Fisher p = {pa['fisher_p']:.3g}"
          f"   ->  exact McNemar p = {pb['p_value']:.3g} "
          f"({pb['n_only_first']} vs {pb['n_only_second']} discordant)")
    print(f"   not determinable   : {nd['n_not_determinable_15d']} at 15 d vs "
          f"{nd['n_not_determinable_60d']} at 60 d  ->  McNemar p = {nd['p_value']:.3g}")
    print(f"   headroom           : unpaired Mann-Whitney p = "
          f"{ph['mannwhitney_p']:.3g}  ->  Wilcoxon signed-rank p = "
          f"{pw['wilcoxon_p']:.3g}")
    print(f"   starting density IQR {iq['iqr_15d']:.2f} -> {iq['iqr_60d']:.2f} log10, "
          f"difference {iq['difference']:.2f} "
          f"(paired bootstrap 95% CI {ci(iq['paired_bootstrap_ci'], 2)})")
    print("   None of these conclusions changes direction. Two of the paired tests "
          "are the\n   sharper ones, because the change is within-isolate and "
          "almost one-directional;\n   the headroom comparison loses sixteen "
          "orders of magnitude of p-value and keeps\n   the finding. What "
          "changes is that the manuscript is currently quoting tests\n   that "
          "compared 210 isolates with the same 210 isolates.")

    print("\n" + "=" * 96)
    print("THE SIX-LABORATORY DEPOSIT: THE NESTING, COUNTED")
    print("=" * 96)
    print(struct_era[["level", "unit", "n_units", "n_parents", "mean_per_parent", "note"]]
          .to_string(index=False, float_format=lambda v: f"{v:,.2f}"))

    print("\n" + "=" * 96)
    print("WHAT TREATING READINGS AND FLASKS AS INDEPENDENT COSTS")
    print("=" * 96)
    print(f"   Section 5's headline: starting density separates cleared from "
          f"uncleared flasks.")
    print(f"     naive, {clearance['n_treated_flasks']} flasks as independent : "
          f"AUC {clearance['naive_auc']:.3f}, p = "
          f"{clearance['naive_mannwhitney_p']:.2g}")
    print(f"     cluster bootstrap over laboratories        : 95% CI "
          f"{ci(clearance['cluster_bootstrap_labs_auc_ci'])}")
    print(f"     cluster bootstrap over flasks within a lab : 95% CI "
          f"{ci(clearance['cluster_bootstrap_flasks_within_lab_auc_ci'])}"
          f"   (holds the six labs fixed: flask noise only)")
    for name, r in clearance["restricted_permutation"].items():
        print(f"     permutation within {name:<20}: p "
              f"{pfmt(r['p_value'], N_PERM)}"
              f"   ({r['n_strata_with_both_outcomes']} of {r['n_strata']} strata "
              f"informative, {r['n_distinct_arrangements']:,} arrangements, "
              f"smallest attainable p {r['smallest_attainable_p']:.2g})")
    print(f"     exact laboratory-level test (3 vs 3)       : p = "
          f"{clearance['laboratory_level_exact_p_two_sided']:.2f} two-sided, "
          f"{clearance['laboratory_level_exact_p_one_sided']:.3f} one-sided")
    print(f"     laboratory-level rank correlation          : rho = "
          f"{clearance['laboratory_level_spearman_rho']:.3f}, exact p = "
          f"{clearance['laboratory_level_spearman_exact_p']:.3f} over all 720 orders")
    print(f"     the smallest two-sided p this design can return is "
          f"{clearance['smallest_two_sided_p_this_design_can_return']:.2f}.")
    print("   Between laboratories, p = 1.2e-10 is not a small p-value that got "
          "smaller: it\n   is a p-value the design cannot produce, because three "
          "laboratories cleared and\n   three did not, and 0.10 is the floor for "
          "a three-against-three split. Within a\n   laboratory the association "
          "survives the shuffle -- but that shuffle leaves the\n   treatment arm "
          "free, and the day 0 to 1 window used to measure the starting\n   "
          "density is not arm-neutral: the arms treated at ten times MIC have "
          "already lost\n   most of their population inside it and they are the "
          "arms that clear, so the\n   arm that never clears also reads highest. Hold the arm fixed too "
          "and two of 24\n   laboratory-arm cells still contain both outcomes: "
          "six arrangements, and no\n   p below 0.17 is reachable. The deposit "
          "carries almost no within-laboratory\n   evidence either way. The "
          "perfect ordering of the six laboratories is real and\n   should be "
          "reported as an ordering. The p-value should not be reported at all.")

    print(f"\n   Cox on the same flasks: {cox['n_clusters']} clusters, "
          f"{cox['n_parameters']} parameters, cluster-robust meat of rank at "
          f"most {cox['max_rank_of_cluster_robust_meat']}.")
    print(f"     a cluster-robust Wald test is available: "
          f"{cox['cluster_robust_wald_available']}")
    print(f"     {cox.get('cluster_robust_fit', '')}")
    print(f"     fitting it anyway gives {_worst_robust(cox)} -- SMALLER than "
          f"the p-value it was\n     meant to correct, which is exactly how a "
          f"singular sandwich fails: quietly.")
    print("   Institute is constant within cluster, so there is no permutation "
          "of the\n   laboratory label either. Section 5's six institute "
          "p-values have no valid\n   clustered counterpart and should be "
          "reported as description.")

    print(f"\n   What the laboratory label explains, tested by permuting it "
          f"across flasks:")
    print(f"     starting density : {100*dens['observed_share']:.1f}% of "
          f"flask-level variance, p {pfmt(dens['permutation_p'], N_PERM//4)}   "
          f"(null share {100*dens['expected_share_under_null']:.1f}%)")
    print(f"     kill rate        : {100*rate_share['observed_share']:.1f}% "
          f"within arm, p {pfmt(rate_share['permutation_p'], N_PERM//4)}   "
          f"(null share {100*rate_share['null_share_mean']:.1f}%)")
    print("   These two are exact, because flasks ARE exchangeable across "
          "laboratories under\n   the null, and they are the sharpest form of "
          "Section 5's argument. But they do\n   not say the rate is "
          "laboratory-independent: the laboratory owns a third of the\n   rate "
          "too, and significantly. What survives is the comparison -- nearly "
          "three times\n   as much of the inoculum as of the rate, and the "
          "duration endpoint outright,\n   since three laboratories never "
          "produce one. The starting-density result is also\n   the finding "
          "that most constrains this paper's own Cox adjustment, which is the\n"
          "   right way round.")

    print(f"\n   Inversions, {inv_all['naive_n_pairs']} pairs from "
          f"{flask['institute'].nunique()} laboratories:")
    print(f"     naive Jeffreys 95% CI      : "
          f"{ci([100*v for v in inv_all['naive_jeffreys_ci']], 3)}%")
    print(f"     bootstrap over laboratories: "
          f"{ci([100*v for v in inv_all['cluster_bootstrap_labs_ci']], 3)}%")
    print(f"     bootstrap over flasks      : "
          f"{ci([100*v for v in inv_all['cluster_bootstrap_flasks_within_lab_ci']], 3)}%")
    print(f"     leave-one-laboratory-out   : "
          f"{ci([100*v for v in inv_all['leave_one_laboratory_out_ci']], 3)}%"
          f"   (runs outside [0, 100]: six clusters do not support a normal "
          f"approximation here)")
    print(f"     a laboratory bootstrap draw holds a median of "
          f"{inv_all['cluster_bootstrap_labs_median_pairs_per_draw']:.0f} of the "
          f"{inv_all['naive_n_pairs']} pairs, which is why the interval is wide")

    print("\n" + "=" * 96)
    print("EVERY CONCLUSION FROM THESE TWO DEPOSITS, WITH ITS VERDICT")
    print("=" * 96)
    show = rec[["deposit", "manuscript_section", "conclusion", "naive_uncertainty",
                "clustered_uncertainty", "verdict"]].copy()
    show["conclusion"] = show["conclusion"].str.slice(0, 64)
    show["naive_uncertainty"] = show["naive_uncertainty"].str.slice(0, 34)
    show["clustered_uncertainty"] = show["clustered_uncertainty"].str.slice(0, 46)
    print(show.to_string(index=False))
    print("\n   " + ", ".join(f"{k}: {v}" for k, v in
                              rec["verdict"].value_counts().items()))
    print("\n   Six clusters is the whole of the between-laboratory evidence. "
          "Nothing in this\n   deposit makes it more. Report the permutation and "
          "cluster-bootstrap figures,\n   and drop the p-values the design "
          "cannot support.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
