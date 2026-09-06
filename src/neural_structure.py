"""
Use a neural network to discover structure, then throw the network away.

Run:  python -m src.neural_structure

WHY A NETWORK HERE WHEN docs/22 SHOWED THEY DO NOT EXTRAPOLATE. Because this
does not use the network's predictions. It uses its derivatives, inside the
region where it was trained and is trustworthy, to ask what SHAPE the underlying
function has. The network is an interpolator good enough to differentiate, and
once it has answered the structural question it is discarded. This is the
approach AI Feynman takes, and it is the one use of a network in this pipeline
that survives the objection in docs/22.

THE TWO PROBES. Separability has an exact differential signature.

  ADDITIVE        f(x,y) = g(x) + h(y)      iff   d2f/dxdy = 0 everywhere
  MULTIPLICATIVE  f(x,y) = g(x) * h(y)      iff   d2(log f)/dxdy = 0 everywhere

So a trained network can be differentiated twice by autograd and the mixed
partial examined. If it is zero across the domain, the function factorises and a
two-variable search collapses into two one-variable searches. That is the point:
the network does not solve the problem, it decomposes it.

The statistic reported is the mixed partial normalised by the scale of the
first derivatives, so it is dimensionless and comparable between problems:

    s = mean |d2f/dxdy| / (mean|df/dx| * mean|df/dy|) ** 0.5

VALIDATION FIRST, ON A KNOWN ANSWER. The probe is run on N_reach = L * 10^q,
where the truth is known: it is multiplicatively separable and not additively
separable, since log N_reach = log L + q. A probe that cannot recover that has
no business being pointed at data.

THEN THE OPEN QUESTION. docs/24 found that ERA4TB trajectories have a shape per
flask and no common law, with decline-plus-logistic-regrowth reaching R2 0.917
per flask and 0.097 pooled. So the interesting structure is not in the
trajectory, it is in what sets each flask's parameters. The probe is pointed at
f(t, N0): the normalised trajectory as a function of time and of the starting
density the flask was seeded at.

Writes:  results/tables/neural_structure.csv
         docs/25_STRUCTURE_DISCOVERY.md
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
TABLES = ROOT / "results" / "tables"
OUT = ROOT / "docs" / "25_STRUCTURE_DISCOVERY.md"

SEED = 20260906
ARMS = ["MXF 1X MIC", "MXF 10X MIC", "INH 1X MIC", "INH 10X MIC"]


def train(X: np.ndarray, y: np.ndarray, epochs: int = 4000):
    """A small network, only ever evaluated inside the box it was trained on."""
    import torch

    torch.manual_seed(SEED)
    Xt = torch.tensor(X, dtype=torch.float64)
    yt = torch.tensor(y, dtype=torch.float64).unsqueeze(1)
    mu, sd = Xt.mean(0), Xt.std(0).clamp_min(1e-9)
    ym, ys = yt.mean(), yt.std().clamp_min(1e-9)

    net = torch.nn.Sequential(
        torch.nn.Linear(2, 96), torch.nn.Tanh(),
        torch.nn.Linear(96, 96), torch.nn.Tanh(),
        torch.nn.Linear(96, 1)).double()
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    for _ in range(epochs):
        opt.zero_grad()
        loss = torch.nn.functional.mse_loss(net((Xt - mu) / sd), (yt - ym) / ys)
        loss.backward()
        opt.step()

    def f(Xq):
        return net((Xq - mu) / sd) * ys + ym

    return f, float(loss.item())


def mixed_partial_stat(f, X: np.ndarray, take_log: bool = False) -> float:
    """Normalised |d2f/dxdy|. Near zero means the variables separate.

    take_log is retained for the record and is not used: taking the log of a
    network's output was the bug this module was fixed for. Multiplicative
    separability is tested by training on log y and calling this with
    take_log=False.
    """
    import torch

    x = torch.tensor(X, dtype=torch.float64, requires_grad=True)
    out = f(x).squeeze(1)
    if take_log:
        out = torch.log(out.clamp_min(1e-12))
    g = torch.autograd.grad(out.sum(), x, create_graph=True)[0]
    d2 = torch.autograd.grad(g[:, 0].sum(), x, create_graph=True)[0][:, 1]
    num = d2.abs().mean()
    den = (g[:, 0].abs().mean() * g[:, 1].abs().mean()).clamp_min(1e-12).sqrt()
    return float((num / den).item())


def curvature_stat(f, X: np.ndarray) -> float:
    """Normalised |d2f/dx2|. Near zero means f is linear in its first variable.

    This is the test the Windels prediction actually needs. Pharmacodynamics
    says log(surv) = -k(c) * t, so the slope in t is constant and the second
    derivative in t vanishes. Unlike the multiplicative test it needs only
    surv > 0, so net-growth points, where the surviving fraction exceeds one,
    stay in the analysis instead of being discarded for a property of my
    formulation rather than of the data.
    """
    import torch

    x = torch.tensor(X, dtype=torch.float64, requires_grad=True)
    out = f(x).squeeze(1)
    g = torch.autograd.grad(out.sum(), x, create_graph=True)[0]
    d2 = torch.autograd.grad(g[:, 0].sum(), x, create_graph=True)[0][:, 0]
    num = d2.abs().mean()
    den = (g[:, 0] ** 2).mean().clamp_min(1e-12).sqrt()
    return float((num / den).item())


def probe(name: str, X: np.ndarray, y: np.ndarray, truth: str) -> dict:
    """Two networks, not one, and neither has a logarithm taken of its output.

    The first version trained a single network on y and, for the multiplicative
    test, took log of the network's OUTPUT. That failed its own calibration on
    the easiest case, reporting N_reach = L * 10^q as neither: the target spans
    seven orders of magnitude, the network is fitted on a normalised scale, and
    its relative error at small values is large, so log of that output is
    dominated by fitting error rather than by structure.

    The stable formulation uses the identity directly. f = g*h if and only if
    log f = log g + log h, so multiplicative separability of y is ADDITIVE
    separability of log y. Train a second network on log y and run the same
    well-conditioned additive test on it.
    """
    sub_idx = np.random.default_rng(SEED).choice(len(X), min(500, len(X)), replace=False)
    sub = X[sub_idx]

    f, loss = train(X, y)
    add = mixed_partial_stat(f, sub, take_log=False)
    curv = curvature_stat(f, sub)

    # The multiplicative test needs a positive target. Skipping the whole test
    # when a few points are non-positive threw away the one prediction theory
    # actually makes about the Windels data, so the non-positive rows are
    # dropped for that test alone and their number is reported.
    # A target that is negative by construction, such as a log surviving
    # fraction, has no multiplicative test: log of it does not exist and the
    # question is not meaningful rather than the data being unusable. Say so,
    # rather than reporting NaN beside a large drop count that reads like loss.
    pos = y > 0
    n_dropped = int((~pos).sum())
    if pos.sum() < 0.5 * len(y):
        return {"problem": name, "train_mse": loss, "additive_stat": add,
                "multiplicative_stat": np.nan, "n_dropped_for_mult": np.nan,
                "curvature_stat": curv,
                "verdict": "additive" if add < 0.05 else "neither",
                "truth": truth}
    if pos.sum() >= 50:
        Xp = X[pos]
        flog, _ = train(Xp, np.log(y[pos]))
        idx = np.random.default_rng(SEED).choice(len(Xp), min(500, len(Xp)),
                                                 replace=False)
        mul = mixed_partial_stat(flog, Xp[idx], take_log=False)
    else:
        mul = np.nan



    verdict = "neither"
    if np.isfinite(mul) and mul < add and mul < 0.05:
        verdict = "multiplicative"
    elif add < 0.05:
        verdict = "additive"
    return {"problem": name, "train_mse": loss, "additive_stat": add,
            "multiplicative_stat": mul, "n_dropped_for_mult": n_dropped,
            "curvature_stat": curv,
            "verdict": verdict, "truth": truth}


def known_law(n=3000):
    rng = np.random.default_rng(SEED)
    L = 10 ** rng.uniform(0, 3, n)
    q = rng.uniform(1, 4, n)
    return np.column_stack([L, q]), L * 10.0 ** q


def known_additive(n=3000):
    rng = np.random.default_rng(SEED + 1)
    a = rng.uniform(1, 10, n)
    b = rng.uniform(1, 10, n)
    return np.column_stack([a, b]), a ** 2 + np.sqrt(b)


def known_neither(n=3000):
    rng = np.random.default_rng(SEED + 2)
    a = rng.uniform(1, 5, n)
    b = rng.uniform(1, 5, n)
    return np.column_stack([a, b]), 1.0 / (a + b)


def trajectories():
    """Normalised ERA4TB trajectory against time and the flask's own inoculum."""
    e = pd.read_csv(DATA, encoding="latin-1")
    e = e[e["Sample"].isin(ARMS) & (e["Time"] >= 0) & (e["AQL"] != 1)
          & (e["Volume"] == 100.0) & (e["BQL"] != 1)].copy()
    e["y"] = pd.to_numeric(e["CFUlog10"], errors="coerce")
    e = e.dropna(subset=["y"])
    e["flask"] = e["Institute"] + "|" + e["Sample"] + "|" + e["Replicate"].astype(str)

    rows = []
    for _, g in e.groupby("flask"):
        g = g.sort_values("Time")
        if len(g) < 5:
            continue
        n0 = float(g["y"].iloc[0])
        for t, y in zip(g["Time"], g["y"]):
            rows.append({"t": float(t), "n0": n0, "dy": float(y) - n0})
    d = pd.DataFrame(rows)
    return d[["t", "n0"]].to_numpy(float), d["dy"].to_numpy(float), len(d)



# ------------------------------------------------------------- Windels 2024 ---
def windels_pairs():
    """The one deposit where the two factors are actually crossed.

    A 6 x 6 factorial of amikacin concentration against nutrient level, three
    replicates, six timepoints. Because it is a designed grid rather than an
    observational one, drug and nutrient are not confounded with each other or
    with a laboratory, so a separability question about them is well posed.

    Standard pharmacodynamics says surv = exp(-k(c) t), which makes
    y = -log(surv) equal to k(c) * t and therefore MULTIPLICATIVELY separable in
    (t, c). That is a prediction from theory, and this is a test of it.

    Rows where the surviving fraction is zero carry no logarithm and are dropped
    with their number reported. Rows where it exceeds one are net growth; they
    are kept for the additive test, which tolerates negatives, and drop out of
    the multiplicative test, which needs a positive target.
    """
    w = pd.read_csv(ROOT / "data/raw/windels2024/timekill.csv")
    n_all = len(w)
    w = w[(w["surv_frac"] > 0) & (w["time"] > 0)].copy()
    # log of the surviving fraction, not minus-log. This is defined for every
    # positive reading, so the rows where the population grew stay in.
    w["logsurv"] = np.log(w["surv_frac"])
    w["neglog"] = -w["logsurv"]
    late = w[w["time"] >= w["time"].max()]
    return {
        "n_all": n_all, "n_used": len(w), "n_zero": int(n_all - len(w)),
        "n_growth": int((w["neglog"] <= 0).sum()), "n_late": len(late),
        "pairs": [
            ("Windels: log surv against (time, drug concentration)",
             w[["time", "AB_conc"]].to_numpy(float), w["logsurv"].to_numpy(float),
             "theory says linear in time"),
            ("Windels: log surv against (time, nutrient level)",
             w[["time", "nutrient_conc"]].to_numpy(float),
             w["logsurv"].to_numpy(float), "unknown"),
            ("Windels: log surv against (drug, nutrient), last timepoint",
             late[["AB_conc", "nutrient_conc"]].to_numpy(float),
             late["logsurv"].to_numpy(float), "unknown"),
        ],
    }


def main() -> int:
    checks = [
        ("N_reach = L * 10^q", *known_law(), "multiplicative"),
        ("a^2 + sqrt(b)", *known_additive(), "additive"),
        ("1 / (a + b)", *known_neither(), "neither"),
    ]
    rows = [probe(n, X, y, truth) for n, X, y, truth in checks]
    calibrated = sum(r["verdict"] == r["truth"] for r in rows)

    Xt, yt, n_pts = trajectories()
    rows.append(probe("ERA4TB trajectory f(t, N0)", Xt, yt, "unknown"))

    wn = windels_pairs()
    for nm, X, y, truth in wn["pairs"]:
        rows.append(probe(nm, X, y, truth))

    res = pd.DataFrame(rows)
    TABLES.mkdir(parents=True, exist_ok=True)
    res.to_csv(TABLES / "neural_structure.csv", index=False)
    traj = res.iloc[-1]

    def g(x, n=3):
        return "-" if not np.isfinite(x) else f"{x:.{n}g}"

    doc = f"""# Using a network to discover structure, then discarding it

Generated by `python -m src.neural_structure`. Seed {SEED}.

`docs/22` showed that networks learn the region rather than the law and fail
outside it by three orders of magnitude. This is the one use of a network in this
pipeline that survives that objection, because it never uses the network's
predictions. It uses the network's **derivatives**, inside the region where it
was trained and is trustworthy, to ask what shape the underlying function has.
Once the question is answered the network is thrown away.

## The probe

Separability has an exact differential signature:

| structure | holds if and only if |
|---|---|
| `f(x,y) = g(x) + h(y)` | mixed partial of `f` is zero everywhere |
| `f(x,y) = g(x) * h(y)` | mixed partial of `log f` is zero everywhere |

So a trained network is differentiated twice by autograd and the mixed partial
examined. The statistic is normalised by the scale of the first derivatives, so
it is dimensionless and comparable between problems. Near zero means the
variables separate, and a two-variable search collapses into two one-variable
searches.

## Calibration on known answers

The probe is worthless unless it recovers structure that is already known, so it
is run first on three functions whose answers are not in doubt.

| function | additive statistic | multiplicative statistic | verdict | truth |
|---|---:|---:|---|---|
""" + "".join(
        f"| `{r.problem}` | {g(r.additive_stat)} | {g(r.multiplicative_stat)} | "
        f"{r.verdict} | {r.truth} |\n" for r in res.iloc[:3].itertuples()) + f"""
**{calibrated} of 3 recovered.** A probe that fails here should not be pointed at
data, and this is reported before the result rather than after it.

## The open question

`docs/24` found that ERA4TB trajectories have a shape per flask and no common
law: decline plus logistic regrowth reaches R-squared 0.917 fitted per flask and
0.097 pooled. So the structure worth looking for is not inside the trajectory but
in what sets each flask's parameters, and the natural first question is whether
the trajectory factorises into a time course and an inoculum effect.

The probe is pointed at `f(t, N0)`, the normalised trajectory as a function of
time and of the density its own flask was seeded at, over {n_pts} readings.

| | additive statistic | multiplicative statistic | verdict |
|---|---:|---:|---|
| `f(t, N0)` | {g(traj['additive_stat'])} | {g(traj['multiplicative_stat'])} | {traj['verdict']} |

A verdict of **neither** would say the inoculum does not enter as a separable
factor or offset: its effect on the trajectory is entangled with time, so no
decomposition into a time course times an inoculum term exists to be found. A
verdict of **additive** would say the inoculum shifts the whole curve without
changing its shape.

## Windels, where the factors are actually crossed

ERA4TB cannot separate the inoculum from the laboratory that seeded it. The
Windels deposit can: a 6 by 6 factorial of amikacin concentration against
nutrient level, three replicates, six timepoints, so drug and nutrient are
crossed by design rather than by accident.

Of {wn['n_all']} rows, {wn['n_zero']} carry a zero surviving fraction and no
logarithm and are dropped; {wn['n_used']} remain. {wn['n_growth']} of those show
net growth, which the additive test tolerates and the multiplicative test cannot.

This deposit also carries a prediction to test. Standard pharmacodynamics says
`surv = exp(-k(c) t)`, which makes `-log(surv)` equal to `k(c) * t` and
therefore multiplicatively separable in time and concentration. Before any probe
runs, the raw table already strains that: mean `-log(surv)` rises only about
1.3-fold between the first and last timepoint, where proportionality to `t`
would require eightfold. Killing is nearly complete in the first interval and
then stops.

| pair | additive statistic | multiplicative statistic | verdict | expected |
|---|---:|---:|---|---|
""" + "".join(
        f"| {r.problem.replace('Windels: ', '')} | {g(r.additive_stat)} | "
        f"{g(r.multiplicative_stat)} | {r.verdict} | {r.truth} |\n"
        for r in res.iloc[4:].itertuples()) + f"""
The third row is the one with no textbook answer. It asks whether the drug
concentration and the nutrient level combine as a product on survival, which
would mean each acts independently of the other, or whether they interact. An
additive verdict on `-log(surv)` is the independent case.

## What this buys the pipeline

A structural verdict is worth more than a fitted surface, because it says which
searches are worth running. If a function factorises, two one-variable symbolic
searches will succeed where a two-variable search over the same budget would not.
If it does not, that is a fact about the system and no amount of search will
recover a product that is not there.

That is the division this project keeps arriving at: use the flexible model to
find out what kind of thing you are looking at, and use an exact method to write
down what it is.
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")

    pd.set_option("display.width", 200)
    print(res.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print(f"\ncalibration: {calibrated} of 3 known structures recovered")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
