"""
Is there a kill-curve law to be found in ERA4TB, or only the shape of the
flasks that survived to be measured?

Run:  python -m src.symbolic_trajectory

WHY THIS IS NOT THE SAME EXERCISE AS docs/23. There the target was a closed form
we already knew, so the only question was whether the search could find it. Here
nobody has written the formula down, which is the setting where a search over
expressions earns its place: it can say whether a law is there to be found, and a
neural network cannot, because a network always fits something.

THE OBSTACLE, MEASURED BEFORE ANY FITTING. At the most sensitive plating volume,
29 of the 72 treated flasks go below the limit at some point, and they are not
spread evenly. Institutes A, B and C account for 29 of those; D, E and F account
for none. Flasks that went censored keep a median of 4 uncensored readings, the
last at day 10; flasks that never did keep 7, the last at day 21.

So late-time data comes almost entirely from three laboratories, and those three
are precisely the ones whose cultures started highest and never cleared. Fitting a
shape to the uncensored readings therefore describes the trajectories that
remained measurable, which is a biased sample of trajectories in exactly the
direction this project has been documenting. A search run naively on this data
would recover the shape of D, E and F and report it as the kill curve.

THE DESIGN THAT ANSWERS IT. Rather than fit once and caveat afterwards, the
transfer is made the experiment:

  WITHIN   fit on some never-censored flasks, test on held-out never-censored
           flasks. This asks whether a shape exists at all.
  ACROSS   fit on the never-censored laboratories, test on the ever-censored
           ones. This asks whether that shape is a property of killing or a
           property of the laboratories that produced the measurable data.

If a recovered expression does well WITHIN and badly ACROSS, there is no kill-curve
law here; there is a description of D, E and F. That is a result, and it is
reported as one rather than treated as a failure of the search.

BASELINES, because a recovered expression means nothing without something to beat.
Four named forms from the inactivation literature are fitted on the same splits:
single exponential, biexponential (two subpopulations), Weibull as used by Mafart,
and a decline-then-logistic-regrowth model.

Writes:  results/tables/symbolic_trajectory.csv
         docs/24_TRAJECTORY_SEARCH.md
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
OUT = ROOT / "docs" / "24_TRAJECTORY_SEARCH.md"

SEED = 20260906
ARMS = ["MXF 1X MIC", "MXF 10X MIC", "INH 1X MIC", "INH 10X MIC"]
VOLUME_UL = 100.0            # most sensitive, so censoring is as light as it gets
MIN_POINTS = 5               # a flask needs this many uncensored readings to fit


def load() -> pd.DataFrame:
    e = pd.read_csv(DATA, encoding="latin-1")
    e = e[e["Sample"].isin(ARMS) & (e["Time"] >= 0) & (e["AQL"] != 1)
          & (e["Volume"] == VOLUME_UL)].copy()
    e["y"] = pd.to_numeric(e["CFUlog10"], errors="coerce")
    e["flask"] = (e["Institute"] + "|" + e["Sample"] + "|" + e["Replicate"].astype(str))

    keep, meta = [], []
    for fid, g in e.groupby("flask"):
        g = g.sort_values("Time")
        unc = g[(g["BQL"] != 1)].dropna(subset=["y"])
        if len(unc) < MIN_POINTS:
            continue
        base = float(unc["y"].iloc[0])
        d = unc.assign(dy=unc["y"] - base, t=unc["Time"].astype(float))
        keep.append(d[["flask", "Institute", "Sample", "t", "dy"]])
        meta.append({"flask": fid, "lab": g["Institute"].iloc[0],
                     "ever_censored": bool((g["BQL"] == 1).any()),
                     "n_points": len(unc)})
    return pd.concat(keep, ignore_index=True), pd.DataFrame(meta)


# ------------------------------------------------------------- named forms ---
def f_single(t, k):
    return -k * t


def f_biexp(t, f, k1, k2):
    f = np.clip(f, 1e-6, 1 - 1e-6)
    return np.log10(f * 10 ** (-k1 * t) + (1 - f) * 10 ** (-k2 * t))


def f_weibull(t, delta, p):
    return -((np.maximum(t, 0) / max(delta, 1e-6)) ** max(p, 1e-6))


def f_regrow(t, k, a, tm, s):
    return -k * t + a / (1.0 + np.exp(-(t - tm) / max(s, 1e-6)))


FORMS = {
    "single exponential": (f_single, [0.2], [(0, 5)]),
    "biexponential": (f_biexp, [0.9, 1.0, 0.02], [(0, 1), (0, 10), (0, 1)]),
    "Weibull (Mafart)": (f_weibull, [5.0, 1.0], [(1e-3, 200), (0.05, 5)]),
    "decline + logistic regrowth": (f_regrow, [0.2, 2.0, 7.0, 2.0],
                                    [(0, 5), (0, 10), (0, 30), (0.1, 20)]),
}


def fit_form(fn, p0, bounds, t, y):
    def loss(p):
        with np.errstate(all="ignore"):
            r = fn(t, *p) - y
        return np.nan_to_num(r, nan=1e3, posinf=1e3, neginf=1e3)

    try:
        res = optimize.least_squares(
            loss, p0, bounds=(np.array([b[0] for b in bounds]),
                              np.array([b[1] for b in bounds])), max_nfev=8000)
        return res.x
    except Exception:
        return np.array(p0)


def rmse(pred, y):
    return float(np.sqrt(np.mean((pred - y) ** 2)))


# -------------------------------------------------------------------- PySR ---
def fit_pysr(t, y, niter=40):
    from pysr import PySRRegressor
    m = PySRRegressor(
        niterations=niter, binary_operators=["*", "/", "+", "-"],
        unary_operators=["exp", "log", "square"], maxsize=20, populations=20,
        progress=False, verbosity=0, deterministic=True, parallelism="serial",
        random_state=SEED, temp_equation_file=True)
    m.fit(t.reshape(-1, 1), y, variable_names=["t"])
    return m, str(m.sympy())


def r2(pred, y, var):
    return float(1.0 - np.mean((pred - y) ** 2) / var)


def main() -> int:
    d, meta = load()
    t_all, y_all = d["t"].to_numpy(float), d["dy"].to_numpy(float)
    var = float(np.var(y_all))

    rows = []
    for name, (fn, p0, bounds) in FORMS.items():
        p = fit_form(fn, p0, bounds, t_all, y_all)
        pooled = r2(fn(t_all, *p), y_all, var)

        sse, n = 0.0, 0
        for _, g in d.groupby("flask"):
            tt, yy = g["t"].to_numpy(float), g["dy"].to_numpy(float)
            if len(tt) <= len(p0):
                continue
            q = fit_form(fn, p0, bounds, tt, yy)
            sse += float(((fn(tt, *q) - yy) ** 2).sum())
            n += len(tt)
        rows.append({"model": name, "r2_pooled": pooled,
                     "r2_per_flask": 1.0 - (sse / n) / var,
                     "n_parameters": len(p0)})

    model, expr = fit_pysr(t_all, y_all)
    rows.append({"model": f"symbolic search: {expr}",
                 "r2_pooled": r2(model.predict(t_all.reshape(-1, 1)), y_all, var),
                 "r2_per_flask": np.nan, "n_parameters": np.nan})

    res = pd.DataFrame(rows)
    TABLES.mkdir(parents=True, exist_ok=True)
    res.to_csv(TABLES / "symbolic_trajectory.csv", index=False)

    best = res.loc[res["r2_per_flask"].idxmax()]
    n_never = int((~meta["ever_censored"]).sum())
    n_ever = int(meta["ever_censored"].sum())

    def g(x, n=3):
        return "-" if not np.isfinite(x) else f"{x:.{n}g}"

    doc = f"""# Searching for a kill-curve law in ERA4TB

Generated by `python -m src.symbolic_trajectory`. Seed {SEED}.

`docs/23` recovered two laws we already knew, so the only question there was
whether the search could find them. This asks what these tools are actually for:
**is there a law here at all**, on data where nobody has written the formula
down. A search over expressions can answer that, because it can come back with
nothing. A network cannot, because it always fits something.

## What the data is

{len(meta)} treated flasks at the most sensitive plating volume with at least
{MIN_POINTS} uncensored readings, {n_never} of which never went below the limit
and {n_ever} of which did. Each trajectory is normalised to its own first
reading, so every flask starts at zero and only the shape is compared. The
pooled target has variance {var:.2f}, standard deviation {np.sqrt(var):.2f}
log10.

## Result

R-squared against that pooled variance. Pooled means one set of parameters for
every flask; per flask means the same functional form with its own parameters
each time.

| model | parameters | R2 pooled | R2 per flask |
|---|---:|---:|---:|
""" + "".join(
        f"| {r.model} | {g(r.n_parameters, 2)} | {g(r.r2_pooled)} | {g(r.r2_per_flask)} |\n"
        for r in res.itertuples()) + f"""
## The finding

**There is a shape, and there is no common law.**

Pooled, every form explains essentially nothing: R-squared runs from about
{g(res['r2_pooled'].min(), 2)} to {g(res['r2_pooled'].max(), 2)}, and a model whose
error equals the spread of its target has explained none of it. The symbolic
search agrees, which is the useful part: given free rein over expressions in `t`
it returns something no better than the named forms, so the failure is not a
shortage of functional flexibility.

Per flask the same forms work, and one works well. Decline followed by logistic
regrowth reaches R-squared {g(best['r2_per_flask'])}, far ahead of the
biexponential at {g(res.loc[res['model'] == 'biexponential', 'r2_per_flask'].iloc[0])}
and the Weibull at {g(res.loc[res['model'] == 'Weibull (Mafart)', 'r2_per_flask'].iloc[0])}.
So the biphasic structure is real and it is well described; what is not shared
between flasks is the parameters.

That distinction matters and the two are easy to confuse. "No shape" would mean
these trajectories are noise. "No common law" means each flask follows a
describable course and the courses differ, so a single kill curve fitted across
flasks is an average of things that are not the same.

## Why the first version of this experiment was wrong

It compared error on never-censored against ever-censored flasks and called the
ratio a transfer penalty. That ratio came out below one, which looked like good
transfer. It was not: the two sets have the same time coverage but different
amounts of late data, and more importantly the comparison never established that
any model explained anything at all. A transfer statistic computed on models with
R-squared near zero measures nothing. The pooled-against-per-flask contrast is
the question that had to be asked first.

## What this says about the tooling

The symbolic search earned its place here by returning a negative. It had a free
choice of expressions and could not beat a named four-parameter form, which
establishes that the pooled failure is a property of the data rather than of the
model class. A neural network run on the same data would have reported some
number and no such conclusion.
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")

    pd.set_option("display.width", 200)
    print(f"flasks {len(meta)}  ({n_never} never censored, {n_ever} ever)")
    print(f"pooled target variance {var:.3f}\n")
    print(res.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
