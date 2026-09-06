"""
How often does the faster-killed flask disappear later, and why?

Run:  python -m src.experiments.exp23_inversion_decomposition

WHY THIS TEST EXISTS. Until now this project has shown that the ordering of
laboratories by kill rate and the ordering by clearance do not correspond. That
is a statement about two rankings. It is not a measurement of how often the
rankings actually invert, nor of what fraction of the spread in clearance times
is bought by the rate and what fraction by the distance the population had to
fall. Both are computable, and without them Section 3.5 would rest on a
qualitative comparison between two rankings.

THE ARITHMETIC. Over an interval in which the decline is close to log-linear,

    y(t) = log10 N(t) = a - b t,        b > 0

with a = log10 N0 and b the decline rate in log10 per day. Writing l for the
log10 detection limit and D = a - l for the distance the population starts above
it, the time at which the trajectory crosses the limit is

    T = D / b

so a clearance time is a ratio of two things a rate is not: how fast the
population fell, and how far it had to fall. For two flasks,

    log(T_A / T_B) = log(D_A / D_B) - log(b_A / b_B)

which is exact on this model and splits the difference in clearance time into a
distance term and a rate term. An INVERSION is a pair in which A fell faster yet
crossed later, and on this model that happens exactly when

    D_A / D_B  >  b_A / b_B

The point of the decomposition is that both terms are measurable, so the
question "is the clearance time reporting the drug or the inoculum" stops being
rhetorical.

TWO LIMITS OF THIS MODEL, STATED BEFORE THE RESULTS RATHER THAN AFTER.
A single slope is not a full description of a biphasic trajectory, so b here is
the average decline over the window fitted, not a claim that killing is
first-order. And a flask that never crossed does not have a T; it has T > H,
where H is its last visit. Those pairs are used only when the censoring settles
the comparison on its own, which it does whenever the other flask crossed before
H. Pairs the censoring cannot settle are counted and excluded, not imputed.

Writes:
  results/tables/exp23_flask_parameters.csv
  results/tables/exp23_inversions.csv
  results/receipts/exp23_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

# The limit of quantification is a property of the plated volume: the deposit
# reports counts per mL, and one colony in a plated volume v uL is 1000/v per mL.
# The most sensitive volume, 100 uL, therefore reaches 1.0 log10 CFU/mL, and that
# is the line a flask has to cross to be recorded as cleared.
CLEARANCE_LIMIT = 1.0
FIT_WINDOW = 14          # days; the interval over which a single slope is defensible
TREATED = ["MXF 1X MIC", "MXF 10X MIC", "INH 1X MIC", "INH 10X MIC"]


def load() -> pd.DataFrame:
    d = pd.read_csv(DATA, encoding="latin-1")
    d = d[d["Sample"].isin(TREATED)].copy()
    d = d[(d["Time"] >= 0) & (d["AQL"] != 1)]          # drop pre-dose and over-range
    d["loq"] = np.log10(1000.0 / d["Volume"])
    d["censored"] = d["BQL"] == 1
    d["y"] = pd.to_numeric(d["CFUlog10"], errors="coerce")
    d.loc[d["censored"], "y"] = np.nan
    return d.dropna(subset=["y", "loq"], how="all")


def tobit_slope(t, y, cens, loq):
    """Fit y = a - b t by censored maximum likelihood (Beal's M3).

    An observed reading contributes the Gaussian density; a reading below its
    own limit contributes the probability that it fell there.
    """
    obs = ~cens
    if obs.sum() < 3 or len(np.unique(t[obs])) < 2:
        return None
    a0, b0 = np.polyfit(t[obs], y[obs], 1)[::-1]
    b0 = max(-b0, 1e-3)

    def nll(p):
        a, b, ls = p
        s = np.exp(ls)
        mu = a - b * t
        out = 0.0
        if obs.any():
            out -= np.sum(stats.norm.logpdf(y[obs], mu[obs], s))
        if cens.any():
            out -= np.sum(stats.norm.logcdf((loq[cens] - mu[cens]) / s))
        return out

    r = optimize.minimize(nll, [a0, b0, np.log(0.5)], method="Nelder-Mead",
                          options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-6})
    if not r.success:
        return None
    a, b, ls = r.x
    return {"start_log10": a, "rate_log10_per_day": b, "sigma": np.exp(ls)}


def flask_table(d: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (inst, samp, rep), g in d.groupby(["Institute", "Sample", "Replicate"]):
        w = g[g["Time"] <= FIT_WINDOW]
        t = w["Time"].to_numpy(float)
        y = w["y"].to_numpy(float)
        cens = w["censored"].to_numpy(bool)
        loq = w["loq"].to_numpy(float)
        y = np.where(np.isnan(y), loq, y)          # value unused where censored

        # The same admission rule Section 2.3 applies elsewhere in this project:
        # a cell is fitted only when it retains at least six quantified readings
        # at three distinct times. Below that the slope is set by the censoring
        # pattern rather than by the counts, and a flask whose fitted start sits
        # three logs under its neighbours is reporting the fit, not the culture.
        if (~cens).sum() < 6 or len(np.unique(t[~cens])) < 3:
            continue
        fit = tobit_slope(t, y, cens, loq)
        if fit is None or fit["rate_log10_per_day"] <= 0:
            continue

        # Observed crossing of the clearance limit, at the most sensitive volume.
        sens = g[np.isclose(g["loq"], CLEARANCE_LIMIT)]
        crossed = sens[sens["censored"]]
        t_obs = float(crossed["Time"].min()) if len(crossed) else np.nan
        horizon = float(sens["Time"].max()) if len(sens) else float(g["Time"].max())

        # The distance is taken from the MEASURED starting density, not from the
        # fitted intercept. Killing here is biphasic, so a single line through
        # the whole window extrapolates back to an intercept well below the
        # culture the flask actually started from, and that intercept would put
        # a false distance into every ratio below. This is the same definition
        # of starting density Section 2.3 uses: uncensored readings at the most
        # sensitive volume on days 0 and 1.
        early = g[(g["Time"] <= 1) & (~g["censored"]) &
                  np.isclose(g["loq"], CLEARANCE_LIMIT)]["y"]
        if early.empty:
            early = g[(g["Time"] <= 1) & (~g["censored"])]["y"]
        if early.empty:
            continue
        start_measured = float(early.mean())
        D = start_measured - CLEARANCE_LIMIT
        if D <= 0:
            continue
        rows.append({
            "institute": inst, "arm": samp, "replicate": int(rep),
            "start_measured_log10": start_measured,
            "fitted_intercept_log10": fit["start_log10"],
            "rate_log10_per_day": fit["rate_log10_per_day"],
            "distance_to_limit_log10": D,
            "predicted_clearance_day": D / fit["rate_log10_per_day"],
            "observed_clearance_day": t_obs,
            "cleared": bool(np.isfinite(t_obs)),
            "horizon_day": horizon,
        })
    return pd.DataFrame(rows)


def inversions(f: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Count pairs where the faster-killed flask crossed later.

    Comparisons are made within a treatment arm, so the two flasks met the same
    drug at the same multiple of the MIC and differ only in laboratory and
    replicate. A censored flask is used only when the censoring settles the
    comparison by itself.
    """
    rows, undecidable = [], 0
    for arm, g in f.groupby("arm"):
        for i, j in combinations(g.index, 2):
            A, B = f.loc[i], f.loc[j]
            if A["institute"] == B["institute"]:
                continue
            fast, slow = (A, B) if A["rate_log10_per_day"] > B["rate_log10_per_day"] else (B, A)
            if fast["cleared"] and slow["cleared"]:
                later = fast["observed_clearance_day"] > slow["observed_clearance_day"]
            elif (not fast["cleared"]) and slow["cleared"] and slow["observed_clearance_day"] <= fast["horizon_day"]:
                later = True          # the faster flask had not crossed by then
            elif fast["cleared"] and (not slow["cleared"]) and fast["observed_clearance_day"] <= slow["horizon_day"]:
                later = False
            else:
                undecidable += 1
                continue
            rows.append({
                "arm": arm,
                "faster_institute": fast["institute"], "slower_institute": slow["institute"],
                "rate_ratio": fast["rate_log10_per_day"] / slow["rate_log10_per_day"],
                "distance_ratio": fast["distance_to_limit_log10"] / slow["distance_to_limit_log10"],
                "inversion": bool(later),
            })
    out = pd.DataFrame(rows)
    if out.empty:
        return out, {"n_comparable_pairs": 0, "undecidable_pairs": undecidable}
    n, k = len(out), int(out["inversion"].sum())
    lo, hi = stats.beta.ppf([0.025, 0.975], k + 0.5, n - k + 0.5)   # Jeffreys interval
    pred = out["distance_ratio"] > out["rate_ratio"]
    summ = {
        "n_comparable_pairs": n, "undecidable_pairs": undecidable,
        "n_inversions": k, "inversion_rate": k / n,
        "inversion_rate_95CI": [float(lo), float(hi)],
        "model_predicts_inversion_correctly": float((pred == out["inversion"]).mean()),
    }
    return out, summ


def decompose(f: pd.DataFrame) -> dict:
    """Split the spread in clearance time into a distance term and a rate term.

    On log(T) = log(D) - log(b) the variance decomposition is exact:
        Var(log T) = Var(log D) + Var(log b) - 2 Cov(log D, log b)
    """
    out = {}
    for arm, g in f.groupby("arm"):
        if len(g) < 4:
            continue
        g = g[g["rate_log10_per_day"] > 0.01]     # log(b) is unstable as b -> 0
        if len(g) < 4:
            continue
        lD, lb = np.log(g["distance_to_limit_log10"]), np.log(g["rate_log10_per_day"])
        vD, vb = np.var(lD, ddof=1), np.var(lb, ddof=1)
        cov = np.cov(lD, lb, ddof=1)[0, 1]
        vT = vD + vb - 2 * cov
        out[arm] = {
            "n_flasks": int(len(g)),
            "var_log_predicted_time": float(vT),
            "var_log_distance": float(vD),
            "var_log_rate": float(vb),
            "cov": float(cov),
            "share_distance": float(vD / (vD + vb)),
            "share_rate": float(vb / (vD + vb)),
            "distance_fold_spread": float(np.exp(lD.max() - lD.min())),
            "rate_fold_spread": float(np.exp(lb.max() - lb.min())),
        }
    return out


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    f = flask_table(load())
    f.to_csv(TABLES / "exp23_flask_parameters.csv", index=False)
    inv, summ = inversions(f)
    inv.to_csv(TABLES / "exp23_inversions.csv", index=False)
    dec = decompose(f)

    (RECEIPTS / "exp23_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp23_inversion_decomposition.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "van Wijk et al. 2023, figshare 19766083",
        "clearance_limit_log10": CLEARANCE_LIMIT,
        "fit_window_days": FIT_WINDOW,
        "n_flasks_fitted": int(len(f)),
        "inversions": summ,
        "variance_decomposition": dec,
    }, indent=2, default=str), encoding="utf-8")

    pd.set_option("display.width", 220)
    print(f"-- {len(f)} treated flasks fitted, {int(f['cleared'].sum())} of them crossed "
          f"the {CLEARANCE_LIMIT:.1f} log10 limit --\n")
    print(f.groupby(["arm", "institute"])[
        ["start_measured_log10", "rate_log10_per_day", "distance_to_limit_log10",
         "observed_clearance_day"]].mean().to_string(float_format=lambda v: f"{v:,.3f}"))

    print("\n-- how often did the faster-killed flask disappear later? --")
    if summ["n_comparable_pairs"]:
        print(f"   comparable pairs (same arm, different laboratories): {summ['n_comparable_pairs']}")
        print(f"   pairs the censoring could not settle, excluded      : {summ['undecidable_pairs']}")
        print(f"   inversions                                          : {summ['n_inversions']} "
              f"({100*summ['inversion_rate']:.1f}%, 95% CI "
              f"{100*summ['inversion_rate_95CI'][0]:.1f}-{100*summ['inversion_rate_95CI'][1]:.1f}%)")
        print(f"   predicted by D_A/D_B > b_A/b_B                       : "
              f"{100*summ['model_predicts_inversion_correctly']:.1f}% of pairs called correctly")

    print("\n-- what buys the spread in clearance time? --")
    for arm, v in dec.items():
        print(f"   {arm:14s} n={v['n_flasks']:2d}  distance {100*v['share_distance']:4.1f}%  "
              f"rate {100*v['share_rate']:4.1f}%   "
              f"(spread: distance {v['distance_fold_spread']:.2f}x, rate {v['rate_fold_spread']:.2f}x)")

    print("\n   The shares are of Var(log D) + Var(log b), so they say how much of the")
    print("   variation available to move a clearance time sits in each term. They are")
    print("   not a causal decomposition, and the covariance is reported separately")
    print("   because the two terms are not independent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
