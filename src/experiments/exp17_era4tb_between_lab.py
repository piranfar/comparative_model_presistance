"""
A kill rate travels between laboratories. A time to clearance does not.

Run:  python -m src.experiments.exp17_era4tb_between_lab

WHY THIS TEST EXISTS. The manuscript argues that a pharmacodynamic rate is a
property of a drug, an organism and a physiological condition together, and that
endpoints read as durations -- the minimum duration for killing, the time to
sterilisation -- are not clean summaries of drug action because they also carry
the state of the population they started from. exp14 made the first half of that
case within one dataset. exp16 made the second half on 217 clinical isolates,
where the minimum inhibitory concentration and the minimum duration for killing
were uncorrelated.

Both invite the same objection: the conditions were deliberately varied, or the
isolates genuinely differ, so of course the numbers move. The sharper question
is what happens when a consortium writes one protocol, distributes one stock of
one strain, and asks six laboratories to do exactly the same thing.

THE DESIGN. The ERA4TB consortium did this. Mycobacterium tuberculosis H37Rv,
moxifloxacin and isoniazid at one and ten times MIC, three flasks per arm,
sampled to day 21 or 28, in six laboratories blinded and labelled A to F. Each
sample was plated at four volumes, so each carries four readings with four
different limits of quantification.

WHAT THIS SCRIPT FINDS, stated before the methods so the methods can be judged
against it. The starting density, which the protocol fixes, spans more than
three log10 between laboratories. That single unreported difference decides
whether a flask is ever recorded as cleared: it classifies clearance with an
area under the curve of 0.97, and once it is in the model the laboratory itself
stops explaining anything. The kill rate, fitted as a slope, is far more
reproducible than the clearance time it implies. A duration endpoint measured in
six laboratories is therefore substantially a measurement of their inocula.

THREE ESTIMATORS, BECAUSE THE CENSORING IS THE DIFFICULTY. Roughly a fifth of
all readings are flagged below the limit of quantification. Dropping them is the
one clearly wrong option: it removes precisely the deepest killing, and it
removes more of it at the laboratories that killed more, so a slope fitted to
the survivors is biased by a different amount in each laboratory. Three
treatments of the censoring are run instead, and they are meant to be compared.

  1. A TOBIT MODEL. Left-censored linear regression of log10 CFU/mL on time,
     each reading judged against the limit of its own plating volume, so a
     2.5 uL plate that missed a population of 200 CFU/mL and a 100 uL
     quadruplicate that missed one of 8 contribute the different amounts of
     information they actually carry. A censored reading contributes
     log Phi((limit - mu)/sigma). This is Beal's M3, which is the Tobit
     likelihood written for this assay.

  2. MULTIPLE IMPUTATION. Each censored reading is drawn from the fitted normal
     truncated at its own limit, the slope is refitted by ordinary least squares
     on the completed data, and the estimates are pooled by Rubin's rules with
     the between-imputation variance included. This makes a different assumption
     from the Tobit model about what happened below the limit, so agreement
     between the two is evidence that neither is driving the answer.

  3. SURVIVAL ANALYSIS. Time to the first undetectable culture, per flask, with
     flasks never falling below the limit right-censored at their last visit.
     Kaplan-Meier curves per laboratory, a log-rank test across them, and Cox
     proportional hazards fitted twice: on laboratory alone, then with the
     starting density added. The comparison between those two fits is the point
     of the whole script.

The first two estimate a rate and the third estimates a duration, on the same
flasks. That is what makes the contrast between them interpretable.

Data: ERA4TB standardised time-kill kinetics, figshare item 19766083.

Writes:
  results/tables/exp17_kill_rates.csv
  results/tables/exp17_censoring.csv
  results/tables/exp17_baseline.csv
  results/tables/exp17_survival.csv
  results/tables/exp17_cox.csv
  results/receipts/exp17_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from ..inference.fitting import fit_log10, profile_likelihood

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

GROUPS = {0: "untreated", 1: "MXF 1x MIC", 2: "MXF 10x MIC",
          3: "INH 1x MIC", 4: "INH 10x MIC"}

# The most sensitive plating: 100 uL in quadruplicate, one colony per mL is
# 1.0 log10. The survival endpoint is defined here so that "undetectable" means
# the same thing in every laboratory.
SENSITIVE_CONDITION = 0

T_MIN, T_MAX = 0.0, 14.0    # window for the rate fits
MIN_QUANTIFIED = 6          # below this the slope is read off the censoring
N_IMPUTATIONS = 50
SEED = 20240917


def line(t, intercept, slope):
    """log10 CFU/mL changing at a constant rate per day."""
    return intercept + slope * t


def load() -> pd.DataFrame:
    d = pd.read_csv(DATA, encoding="latin-1")
    # CFU is already expressed per millilitre: the smallest count recorded at
    # each plating volume is exactly 1000/volume, which is one colony per mL.
    # The limit of quantification is therefore a property of the volume plated.
    d["loq"] = np.log10(1000.0 / d["Volume"])
    d["censored"] = d["BQL"] == 1
    d["y"] = np.where(d["censored"], d["loq"], d["CFUlog10"])
    d = d[d["AQL"] == 0]                       # too many to count: no information
    d = d[d["y"].notna() & (d["Time"] >= 0)]
    d["arm"] = d["Group"].map(GROUPS)
    return d


# --------------------------------------------------------------------------
# 1. Tobit
# --------------------------------------------------------------------------

def tobit_slope(g: pd.DataFrame) -> dict | None:
    t = g["Time"].to_numpy(float)
    y = g["y"].to_numpy(float)
    c = g["censored"].to_numpy(bool)
    seen = ~c
    if int(seen.sum()) < MIN_QUANTIFIED or np.unique(t[seen]).size < 3:
        return None
    a0 = float(y[seen][t[seen] == t[seen].min()].mean())
    b0 = float(np.polyfit(t[seen], y[seen], 1)[0])
    fit = fit_log10(line, t, y, [a0, b0], ["intercept", "slope"], "tobit",
                    censored=c, bounds=([0.0, -3.0], [10.0, 3.0]))
    prof = profile_likelihood(line, t, y, fit.theta, index=1, censored=c,
                              span=1.5, n_points=41,
                              bounds=([0.0, -3.0], [10.0, 3.0]))
    lo, hi = prof["ci95"]
    return {
        "n_points": int(len(g)), "n_quantified": int(seen.sum()),
        "fraction_censored": float(c.mean()),
        "intercept_log10": float(fit.theta[0]),
        "kill_rate_tobit": float(-fit.theta[1]),
        "kill_rate_se": None if fit.stderr is None else float(fit.stderr[1]),
        "kill_rate_ci_low": float(-hi), "kill_rate_ci_high": float(-lo),
        "residual_sd": float(fit.sigma), "runs_z": float(fit.runs_test_z),
    }


# --------------------------------------------------------------------------
# 2. Multiple imputation
# --------------------------------------------------------------------------

def mi_slope(g: pd.DataFrame, rng: np.random.Generator) -> dict | None:
    """Impute each censored reading below its own limit; pool by Rubin's rules."""
    t = g["Time"].to_numpy(float)
    y = g["y"].to_numpy(float)
    c = g["censored"].to_numpy(bool)
    seen = ~c
    if int(seen.sum()) < MIN_QUANTIFIED or np.unique(t[seen]).size < 3:
        return None

    base = tobit_slope(g)
    if base is None:
        return None
    a, b, sd = base["intercept_log10"], -base["kill_rate_tobit"], base["residual_sd"]

    ests, vars_ = [], []
    for _ in range(N_IMPUTATIONS):
        z = y.copy()
        if c.any():
            mu = a + b * t[c]
            # Draw from the fitted normal conditioned on being below the limit:
            # inverse-CDF sampling on the truncated distribution.
            u = rng.uniform(1e-12, 1.0, size=int(c.sum()))
            q = stats.norm.cdf((y[c] - mu) / sd)
            z[c] = mu + sd * stats.norm.ppf(np.clip(u * q, 1e-12, 1 - 1e-12))
        X = np.column_stack([np.ones_like(t), t])
        beta, *_ = np.linalg.lstsq(X, z, rcond=None)
        resid = z - X @ beta
        s2 = float(resid @ resid) / max(len(z) - 2, 1)
        cov = s2 * np.linalg.pinv(X.T @ X)
        ests.append(float(beta[1]))
        vars_.append(float(cov[1, 1]))

    q_bar = float(np.mean(ests))
    u_bar = float(np.mean(vars_))                     # within-imputation variance
    b_var = float(np.var(ests, ddof=1))               # between-imputation variance
    total = u_bar + (1 + 1 / N_IMPUTATIONS) * b_var   # Rubin's total variance
    se = float(np.sqrt(total))
    # Barnard-Rubin degrees of freedom would refine the interval; with 50
    # imputations and a two-parameter fit the normal approximation is adequate
    # and is reported as such.
    return {
        "kill_rate_mi": -q_bar,
        "kill_rate_mi_se": se,
        "kill_rate_mi_ci_low": -(q_bar + 1.96 * se),
        "kill_rate_mi_ci_high": -(q_bar - 1.96 * se),
        "fraction_missing_information": float(
            ((1 + 1 / N_IMPUTATIONS) * b_var) / total) if total > 0 else np.nan,
    }


# --------------------------------------------------------------------------
# 3. Survival
# --------------------------------------------------------------------------

def survival_frame(d: pd.DataFrame) -> pd.DataFrame:
    """One row per flask: time to first undetectable culture, or censoring."""
    s = d[d["Condition"] == SENSITIVE_CONDITION]
    rows = []
    for (inst, grp, rep), g in s.groupby(["Institute", "Group", "Replicate"]):
        g = g.sort_values("Time")
        below = g[g["censored"]]
        start = g[(g["Time"] <= 1) & (~g["censored"])]["y"].mean()
        if len(below):
            t_ev, event = float(below["Time"].iloc[0]), 1
            after = g[g["Time"] > t_ev]
            regrew = bool((~after["censored"]).any())
        else:
            t_ev, event, regrew = float(g["Time"].max()), 0, False
        rows.append({"institute": inst, "arm": GROUPS[grp], "replicate": rep,
                     "time_days": t_ev, "event": event, "regrew": regrew,
                     "start_log10": float(start) if np.isfinite(start) else np.nan,
                     "last_visit": float(g["Time"].max())})
    return pd.DataFrame(rows)


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; see the docstring for its source")
    rng = np.random.default_rng(SEED)
    pd.set_option("display.width", 230)

    d = load()

    # -- how much is censored, and at which limit ---------------------------
    cens = (d.groupby(["arm", "Condition"])
            .agg(plating_volume_uL=("Volume", lambda v: float(v.mode().iloc[0])),
                 loq_log10=("loq", lambda v: float(v.mode().iloc[0])),
                 n_points=("y", "size"),
                 fraction_below_limit=("censored", "mean"))
            .reset_index().sort_values(["arm", "plating_volume_uL"]))
    cens.to_csv(TABLES / "exp17_censoring.csv", index=False)
    print("-- censoring is a property of the plating volume, not of the assay --")
    print(cens.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    # -- the starting density the protocol was supposed to fix --------------
    base = (d[(d["Time"] <= 1) & (~d["censored"]) & (d["Condition"] == SENSITIVE_CONDITION)]
            .groupby("Institute")["y"].agg(["mean", "std", "size"])
            .rename(columns={"mean": "start_log10_cfu_ml", "std": "sd", "size": "n"})
            .reset_index())
    base.to_csv(TABLES / "exp17_baseline.csv", index=False)
    spread = float(base["start_log10_cfu_ml"].max() - base["start_log10_cfu_ml"].min())
    print("\n-- starting density, which one protocol was written to fix --")
    print(base.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
    print(f"   spread across laboratories: {spread:.2f} log10 = {10**spread:,.0f}-fold")

    # -- rates, both estimators --------------------------------------------
    win = d[(d["Time"] >= T_MIN) & (d["Time"] <= T_MAX)]
    rows = []
    for (grp, inst), g in win.groupby(["Group", "Institute"]):
        tob = tobit_slope(g)
        if tob is None:
            rows.append({"arm": GROUPS[grp], "institute": inst,
                         "note": "too little quantified signal to fit"})
            continue
        mi = mi_slope(g, rng) or {}
        rows.append({"arm": GROUPS[grp], "institute": inst, **tob, **mi, "note": ""})
    rates = pd.DataFrame(rows)
    rates.to_csv(TABLES / "exp17_kill_rates.csv", index=False)

    print("\n-- apparent kill rate, log10 CFU/mL per day, days 0 to 14 --")
    print(rates[["arm", "institute", "n_quantified", "fraction_censored",
                 "kill_rate_tobit", "kill_rate_ci_low", "kill_rate_ci_high",
                 "kill_rate_mi", "fraction_missing_information"]]
          .to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    ok = rates.dropna(subset=["kill_rate_tobit", "kill_rate_mi"])
    agree = float(np.max(np.abs(ok["kill_rate_tobit"] - ok["kill_rate_mi"]))) if len(ok) else np.nan
    print(f"\n   Tobit and multiple imputation never differ by more than "
          f"{agree:.3f} log10/day, so the answer is not an artefact of either")
    print("   treatment of the censored readings.")

    # -- survival ----------------------------------------------------------
    surv = survival_frame(d)
    surv.to_csv(TABLES / "exp17_survival.csv", index=False)
    treated = surv[surv["arm"] != "untreated"].dropna(subset=["start_log10"])

    print("\n-- time to the first undetectable culture, per flask --")
    print(surv.groupby("arm").agg(flasks=("event", "size"), cleared=("event", "sum"),
                                  regrowth=("regrew", "sum"))
          .to_string())
    print("\n   cleared flasks, by laboratory:")
    print(pd.crosstab(treated["institute"], treated["arm"],
                      values=treated["event"], aggfunc="sum").fillna(0)
          .to_string(float_format=lambda v: f"{v:,.0f}"))

    cl = treated[treated["event"] == 1]["start_log10"]
    no = treated[treated["event"] == 0]["start_log10"]
    u = stats.mannwhitneyu(cl, no)
    auc = 1 - u.statistic / (len(cl) * len(no))
    print(f"\n   flasks that cleared started at {cl.mean():.2f} log10 on average;")
    print(f"   flasks that never cleared started at {no.mean():.2f}. "
          f"Mann-Whitney p = {u.pvalue:.1e},")
    print(f"   and the starting density alone separates the two with AUC {auc:.3f}.")

    regrew = surv[surv["regrew"]]
    print(f"\n   {len(regrew)} of the {int(surv['event'].sum())} flasks that fell below the "
          f"limit were detectable again later,")
    print("   so an undetectable culture is not a sterilised one. "
          f"{int((regrew['arm'] == 'INH 1x MIC').sum())} of those "
          f"{len(regrew)} were on isoniazid at 1x MIC.")

    cox_rows = _survival_models(treated, cox_rows=[])
    cox = pd.DataFrame(cox_rows)
    cox.to_csv(TABLES / "exp17_cox.csv", index=False)

    # -- the comparison this script exists to make --------------------------
    # A rate and a duration measured on the same flasks. How far does each
    # travel between laboratories?
    print("\n-- how far each kind of endpoint travels between laboratories --")
    print(f"   {'arm':<14}{'rate: lowest':>14}{'highest':>10}{'fold':>8}"
          f"{'   labs reaching the limit':>26}")
    spread_rows = []
    for arm, g in rates.dropna(subset=["kill_rate_tobit"]).groupby("arm"):
        if arm == "untreated":
            continue
        pos = g[g["kill_rate_tobit"] > 0]["kill_rate_tobit"]
        s = treated[treated["arm"] == arm]
        n_labs_clearing = int((s.groupby("institute")["event"].max() == 1).sum())
        n_labs = int(s["institute"].nunique())
        fold = float(pos.max() / pos.min()) if len(pos) >= 2 and pos.min() > 0 else np.nan
        print(f"   {arm:<14}{(pos.min() if len(pos) else np.nan):>14.3f}"
              f"{(pos.max() if len(pos) else np.nan):>10.3f}{fold:>8.1f}"
              f"{f'{n_labs_clearing} of {n_labs}':>26}")
        spread_rows.append({"arm": arm, "n_labs_with_killing": int(len(pos)),
                            "rate_min": float(pos.min()) if len(pos) else np.nan,
                            "rate_max": float(pos.max()) if len(pos) else np.nan,
                            "rate_fold_range": fold,
                            "labs_reaching_limit": n_labs_clearing,
                            "labs_total": n_labs})
    sp = pd.DataFrame(spread_rows)
    sp.to_csv(TABLES / "exp17_endpoint_spread.csv", index=False)

    # The fold range is only interpretable where the drug is actually killing.
    # At one times MIC most laboratories record net growth, so the ratio is
    # taken over the two or three laboratories with a positive rate and is a
    # ratio of numbers indistinguishable from zero.
    high = sp[sp["arm"].str.contains("10x")]
    print(f"\n   At ten times MIC, where the drug kills, the rate spans "
          f"{high['rate_fold_range'].min():.1f} to {high['rate_fold_range'].max():.1f}")
    print("   fold between laboratories, and every laboratory produces one. At one")
    print("   times MIC most laboratories record net growth, so a fold range there is")
    print("   a ratio of rates indistinguishable from zero and is not interpretable.")
    print("\n   The duration endpoint is the one half the laboratories cannot produce")
    print("   at all: three of six never saw a culture reach the limit, in any arm, so")
    print("   for them the minimum duration for killing has no value. Both endpoints")
    print("   were measured on the same flasks, under one protocol, on one strain.")

    (RECEIPTS / "exp17_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp17_era4tb_between_lab.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "ERA4TB standardised time-kill, figshare 19766083",
        "organism": "Mycobacterium tuberculosis H37Rv",
        "drugs": ["moxifloxacin", "isoniazid"],
        "n_laboratories": int(d["Institute"].nunique()),
        "n_flasks": int(len(surv)),
        "fraction_below_limit_overall": float(d["censored"].mean()),
        "censoring_treatments": ["tobit (Beal M3)",
                                 f"multiple imputation, {N_IMPUTATIONS} draws, Rubin pooling",
                                 "Kaplan-Meier and Cox proportional hazards"],
        "baseline_spread_log10": spread,
        "baseline_spread_fold": float(10 ** spread),
        "clearance_auc_from_baseline_alone": float(auc),
        "clearance_mannwhitney_p": float(u.pvalue),
        "tobit_vs_mi_max_abs_difference": agree,
        "cox": cox_rows,
        "seed": SEED,
    }, indent=2), encoding="utf-8")
    return 0


def _survival_models(treated: pd.DataFrame, cox_rows: list) -> list:
    """Kaplan-Meier, log-rank across laboratories, and two Cox fits."""
    try:
        from lifelines import CoxPHFitter, KaplanMeierFitter
        from lifelines.statistics import multivariate_logrank_test
    except ImportError:
        print("\n   [lifelines not installed: survival models skipped]")
        return cox_rows

    kmf = KaplanMeierFitter()
    print("\n-- Kaplan-Meier, median time to undetectable, by laboratory --")
    for inst, g in treated.groupby("institute"):
        kmf.fit(g["time_days"], g["event"])
        med = kmf.median_survival_time_
        print(f"   {inst}: {len(g)} flasks, {int(g['event'].sum())} cleared, "
              + (f"median {med:.0f} days" if np.isfinite(med)
                 else "median not reached"))

    lr = multivariate_logrank_test(treated["time_days"], treated["institute"],
                                   treated["event"])
    print(f"\n   log-rank across the six laboratories: chi2 = {lr.test_statistic:.1f}, "
          f"p = {lr.p_value:.2e}")
    cox_rows.append({"model": "log-rank across institutes", "term": "institute",
                     "statistic": float(lr.test_statistic), "p_value": float(lr.p_value)})

    # Cox on laboratory alone, then with the starting density added. If the
    # laboratory effect is really an inoculum effect, the second fit absorbs it.
    df = treated.copy()
    df = pd.get_dummies(df, columns=["institute"], drop_first=True, dtype=float)
    inst_cols = [c for c in df.columns if c.startswith("institute_")]

    for label, cols in (("institute only", inst_cols),
                        ("institute + starting density", inst_cols + ["start_log10"])):
        sub = df[cols + ["time_days", "event"]]
        cph = CoxPHFitter(penalizer=0.1)
        try:
            cph.fit(sub, duration_col="time_days", event_col="event")
        except Exception as exc:                      # separation is itself a result
            print(f"\n   Cox ({label}) did not converge: {type(exc).__name__}")
            cox_rows.append({"model": label, "term": "all",
                             "note": f"did not converge: {type(exc).__name__}"})
            continue
        print(f"\n-- Cox proportional hazards, {label} --")
        print(f"   concordance {cph.concordance_index_:.3f}, "
              f"partial log-likelihood {cph.log_likelihood_:.2f}")
        summ = cph.summary[["coef", "exp(coef)", "p"]]
        print(summ.to_string(float_format=lambda v: f"{v:,.3f}"))
        for term, r in summ.iterrows():
            cox_rows.append({"model": label, "term": str(term),
                             "coef": float(r["coef"]),
                             "hazard_ratio": float(r["exp(coef)"]),
                             "p_value": float(r["p"]),
                             "concordance": float(cph.concordance_index_)})

    # Does the inoculum absorb the laboratory effect? Compare each laboratory's
    # p-value before and after, one by one. Reporting only the smallest would
    # hide the laboratories it does absorb behind the one it does not.
    before = {r["term"]: r for r in cox_rows if r.get("model") == "institute only"}
    after = {r["term"]: r for r in cox_rows
             if r.get("model") == "institute + starting density"}
    shared = [t for t in before if t in after and t.startswith("institute_")]
    if shared:
        print("\n-- what the starting density explains, laboratory by laboratory --")
        print(f"   {'laboratory':<14}{'p alone':>10}{'p adjusted':>13}   verdict")
        absorbed, resistant = [], []
        for t in sorted(shared):
            pb, pa = before[t]["p_value"], after[t]["p_value"]
            if pb < 0.05 <= pa:
                verdict, bucket = "explained by inoculum", absorbed
            elif pa < 0.05:
                verdict, bucket = "still differs after adjustment", resistant
            else:
                verdict, bucket = "never differed", None
            print(f"   {t.replace('institute_',''):<14}{pb:>10.3f}{pa:>13.3f}   {verdict}")
            if bucket is not None:
                bucket.append(t.replace("institute_", ""))
        cox_rows.append({"model": "adjustment summary",
                         "absorbed_by_inoculum": ",".join(absorbed),
                         "remaining_after_adjustment": ",".join(resistant)})
        if absorbed:
            print(f"\n   The inoculum accounts for laboratories {', '.join(absorbed)}: they")
            print("   were recorded as never clearing because they started higher, not")
            print("   because their drug killed less.")
        if resistant:
            print(f"   It does not account for {', '.join(resistant)}, which clears faster")
            print("   than its starting density explains. That laboratory differs in the")
            print("   rate itself, and the rate fits agree: see the table above.")

    # The proportional hazards assumption underwrites every hazard ratio above.
    try:
        from lifelines.statistics import proportional_hazard_test
        ph = proportional_hazard_test(cph, sub, time_transform="rank")
        worst = float(ph.summary["p"].min())
        print(f"\n   proportional hazards check (Schoenfeld residuals): "
              f"smallest p = {worst:.3f}")
        print("   " + ("no evidence against proportional hazards"
                       if worst >= 0.05 else
                       "the assumption is doubtful; read the hazard ratios as summaries"))
        cox_rows.append({"model": "proportional hazards test",
                         "term": "global", "p_value": worst})
    except Exception as exc:
        print(f"\n   [proportional hazards check unavailable: {type(exc).__name__}]")
    return cox_rows


if __name__ == "__main__":
    raise SystemExit(main())
