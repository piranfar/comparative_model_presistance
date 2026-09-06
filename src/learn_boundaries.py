"""
Learn the identifiability boundaries from data, and measure what was learned.

Run:  python -m src.learn_boundaries

WHY LEARN SOMETHING WE CAN ALREADY DERIVE. Because the derivation gives exact
labels, and exact labels are rare. Most machine learning is graded against noisy
targets, so a model that is 95 per cent right cannot be distinguished from a
target that is 5 per cent wrong. Here the target is a theorem:

    N_reach = L * 10^q        N_id = L / c1

so every prediction can be scored against truth to machine precision, and the
question stops being "how accurate is the model" and becomes the sharper one:
DID IT LEARN THE LAW, OR DID IT LEARN THE TRAINING BOX?

That distinction is the point of this module and it is what the extrapolation
test below measures. A model that interpolates well and extrapolates badly has
memorised a region. A model that recovers the exponent has recovered the law.

THREE LEARNERS, chosen so the comparison is informative rather than a horse race.

  LINEAR IN LOG SPACE. Taking logs makes both laws linear:
      log10 N_reach = log10 L + q          log10 N_id = log10 L - log10 c1
  so ordinary least squares on (log10 L, q) must recover coefficients of exactly
  1 and 1. This is the control: if the representation is right, the problem is
  trivial, and that is itself the lesson.

  NEURAL NETWORK ON RAW INPUTS. A small MLP given (L, q) with no log transform.
  It has ample capacity to fit the training box and no structural reason to
  extrapolate. This is what "just train a model on it" looks like.

  NEURAL NETWORK ON LOG INPUTS. The same network given (log10 L, q). The only
  change is the representation.

WHAT IS REPORTED. In-box error, out-of-box error, and for the linear model the
recovered coefficients against their true values. Read the ABSOLUTE out-of-box
error, not the ratio: the ratio flatters whichever learner interpolated worst,
and in this experiment it ranks the two networks in the wrong order for exactly
that reason.

Writes:  results/tables/learn_boundaries.csv
         docs/22_LEARNING_THE_BOUNDARIES.md
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
OUT = ROOT / "docs" / "22_LEARNING_THE_BOUNDARIES.md"

SEED = 20260906
# Training box: floors and depths a real assay plausibly uses.
TRAIN_L = (1.0, 1000.0)      # per mL
TRAIN_Q = (1.0, 4.0)         # log10 reduction
# Extrapolation box: deliberately outside, in both variables.
TEST_L = (1000.0, 100000.0)
TEST_Q = (4.0, 8.0)
N_TRAIN, N_TEST = 4000, 2000


def sample(n: int, lrange: tuple[float, float], qrange: tuple[float, float],
           rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Draw (L, q) log-uniformly in L and uniformly in q, and label exactly."""
    L = 10 ** rng.uniform(np.log10(lrange[0]), np.log10(lrange[1]), n)
    q = rng.uniform(*qrange, n)
    X = np.column_stack([L, q])
    y = np.log10(L) + q                      # log10 of N_reach, the exact target
    return X, y


def fit_linear_log(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, callable]:
    """OLS on (log10 L, q). The true coefficients are exactly (1, 1) and 0."""
    A = np.column_stack([np.ones(len(X)), np.log10(X[:, 0]), X[:, 1]])
    beta = np.linalg.lstsq(A, y, rcond=None)[0]

    def predict(Xn: np.ndarray) -> np.ndarray:
        An = np.column_stack([np.ones(len(Xn)), np.log10(Xn[:, 0]), Xn[:, 1]])
        return An @ beta

    return beta, predict


def fit_mlp(X: np.ndarray, y: np.ndarray, log_inputs: bool, seed: int):
    import torch

    torch.manual_seed(seed)

    def rep(Xn):
        return (np.column_stack([np.log10(Xn[:, 0]), Xn[:, 1]]) if log_inputs
                else Xn.astype(float))

    Xt = torch.tensor(rep(X), dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    mu, sd = Xt.mean(0), Xt.std(0).clamp_min(1e-8)
    Xn = (Xt - mu) / sd

    net = torch.nn.Sequential(
        torch.nn.Linear(2, 64), torch.nn.Tanh(),
        torch.nn.Linear(64, 64), torch.nn.Tanh(),
        torch.nn.Linear(64, 1))
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for _ in range(3000):
        opt.zero_grad()
        loss = torch.nn.functional.mse_loss(net(Xn), yt)
        loss.backward()
        opt.step()

    def predict(Xq: np.ndarray) -> np.ndarray:
        with torch.no_grad():
            q = (torch.tensor(rep(Xq), dtype=torch.float32) - mu) / sd
            return net(q).squeeze(1).numpy()

    return predict


def mae(pred, X, y) -> float:
    return float(np.abs(pred(X) - y).mean())


def main() -> int:
    rng = np.random.default_rng(SEED)
    Xtr, ytr = sample(N_TRAIN, TRAIN_L, TRAIN_Q, rng)
    Xin, yin = sample(N_TEST, TRAIN_L, TRAIN_Q, rng)      # held out, same box
    Xout, yout = sample(N_TEST, TEST_L, TEST_Q, rng)      # outside the box

    beta, lin = fit_linear_log(Xtr, ytr)
    mlp_raw = fit_mlp(Xtr, ytr, log_inputs=False, seed=SEED)
    mlp_log = fit_mlp(Xtr, ytr, log_inputs=True, seed=SEED)

    rows = []
    for name, pred in (("linear, log inputs", lin),
                       ("neural net, raw inputs", mlp_raw),
                       ("neural net, log inputs", mlp_log)):
        a, b = mae(pred, Xin, yin), mae(pred, Xout, yout)
        rows.append({"learner": name, "mae_in_box": a, "mae_out_of_box": b,
                     "degradation": b / a if a > 0 else np.inf})
    res = pd.DataFrame(rows)
    TABLES.mkdir(parents=True, exist_ok=True)
    res.to_csv(TABLES / "learn_boundaries.csv", index=False)

    # Does the linear model recover the law, digit for digit?
    truth = np.array([0.0, 1.0, 1.0])
    recovered = np.abs(beta - truth).max()

    def f(x, n=3):
        return f"{x:.{n}g}"

    doc = f"""# Learning the identifiability boundaries

Generated by `python -m src.learn_boundaries`. Seed {SEED}; every number is
reproducible.

The boundaries in `docs/19_MATHEMATICS.md` are closed form, so learning them is
not a way of computing them. It is a way of measuring what a learner extracts
from data whose labels are exact. Most machine learning is graded against noisy
targets; here the target is a theorem, so a model can be scored to machine
precision and the question sharpens from *how accurate* to **did it learn the
law or the training box**.

## Setup

Target: `log10 N_reach = log10 L + q`, exact, no noise.

| | floor L (per mL) | depth q (log10) | n |
|---|---|---|---:|
| training | {TRAIN_L[0]:g} to {TRAIN_L[1]:g} | {TRAIN_Q[0]:g} to {TRAIN_Q[1]:g} | {N_TRAIN:,} |
| held out, same box | {TRAIN_L[0]:g} to {TRAIN_L[1]:g} | {TRAIN_Q[0]:g} to {TRAIN_Q[1]:g} | {N_TEST:,} |
| outside the box | {TEST_L[0]:g} to {TEST_L[1]:g} | {TEST_Q[0]:g} to {TEST_Q[1]:g} | {N_TEST:,} |

The extrapolation box is outside in *both* variables: floors up to a hundred
times higher and depths up to twice as deep as anything seen in training.

## Result

| learner | MAE inside the box | MAE outside | degradation |
|---|---:|---:|---:|
""" + "".join(
        f"| {r.learner} | {f(r.mae_in_box)} | {f(r.mae_out_of_box)} | "
        f"{'∞' if not np.isfinite(r.degradation) else f(r.degradation)}x |\n"
        for r in res.itertuples()) + f"""
Errors are in log10 units, so 0.3 is a factor of two in the predicted inoculum.

## What the linear model recovered

Fitting `log10 N_reach = b0 + b1 * log10 L + b2 * q` gives

| coefficient | recovered | true | error |
|---|---:|---:|---:|
| intercept b0 | {beta[0]:+.6g} | 0 | {abs(beta[0]):.2g} |
| b1, on log10 L | {beta[1]:+.6g} | 1 | {abs(beta[1] - 1):.2g} |
| b2, on q | {beta[2]:+.6g} | 1 | {abs(beta[2] - 1):.2g} |

Largest coefficient error: **{recovered:.2g}**. The law is recovered to machine
precision, and it extrapolates exactly, because a linear model in the right
coordinates *is* the law rather than an approximation to it.

## The lesson, and it is not the one I expected

The obvious prediction was that giving the network log inputs would let it
extrapolate. It does not, and the numbers say so plainly.

Log inputs improve the fit *inside* the training box by a factor of
{f(res.loc[res.learner == 'neural net, raw inputs', 'mae_in_box'].iloc[0] / res.loc[res.learner == 'neural net, log inputs', 'mae_in_box'].iloc[0], 2)},
which is what a better representation should do. Outside the box both networks
fail at the same scale: absolute errors of
{f(res.loc[res.learner == 'neural net, raw inputs', 'mae_out_of_box'].iloc[0], 2)} and
{f(res.loc[res.learner == 'neural net, log inputs', 'mae_out_of_box'].iloc[0], 2)} log10 units,
which is a factor of roughly a thousand in the predicted inoculum. The
degradation *ratio* is worse for the log network only because its in-box fit was
better; the ratio flatters whichever model interpolated least well, which is why
the absolute error is the number to read.

The reason is structural rather than a matter of tuning. A network of tanh units
saturates. It can approximate a linear function across the region it was shown
and cannot continue that line beyond it, no matter which coordinates the inputs
arrive in. Offering the right representation as *features* does not impose it;
the model is still free to fit any smooth surface through the training box, and
it does.

**So the useful thing is not to learn the mapping in better coordinates. It is
to commit to the structure.** A linear model in log space does not approximate
`L * 10^q`, it *is* that law, which is why its coefficients come back as 1 and 1
to fifteen decimal places and its extrapolation error stays at machine
precision across floors a hundred times higher and depths twice as deep as
anything in training.

The practical consequence for a pipeline: a learner that regresses these
boundaries will be confidently wrong the first time it meets an assay outside
its training range, by about three orders of magnitude, **and nothing in its
output will signal that it has left the region it knows.** That silence is the
danger, not the error.

## How this fits the wider system

The floor `L` is the part that genuinely needs inference, and
`src/infer_floor.py` does it with evidence and a DERIVED / INFERRED / WEAK /
NONE label. Once `L` is in hand the boundaries are arithmetic. So the division of
labour is:

- **learned**: extracting `L`, `N_0`, `q` and the thresholds from heterogeneous
  deposits, and inferring `L` where it is not stated
- **derived**: everything downstream, because a learned approximation to
  `L * 10^q` can only be worse than the identity

The learning experiment above is what licenses that division rather than merely
asserting it. It shows the cost of learning the mapping, and it shows that the
cost is avoidable.
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")

    print(res.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print(f"\n  linear model coefficients: {beta.round(6)}  (true: 0, 1, 1)")
    print(f"  largest coefficient error: {recovered:.3g}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
