"""
Can a search over algebraic expressions recover the boundary laws from data?

Run:  python -m src.symbolic_boundaries

WHY THIS AND NOT ANOTHER NETWORK. docs/22 showed that fitting a surface through
the training box does not give the law: both neural networks were wrong by about
three orders of magnitude outside the box and neither signalled it. The diagnosis
there was that offering the right representation as input features does not
impose it. Symbolic regression tests the other half of that claim, because it
does not fit a surface at all. It searches the space of algebraic expressions
built from a chosen set of operators and returns the expression itself, so the
output is a formula that can be read and checked rather than a set of weights.

If the diagnosis in docs/22 is right, this should recover the laws exactly and
extrapolate for the same reason the linear-in-log model did: a recovered
expression IS the law rather than an approximation to it over a region.

THE TEST IS DELIBERATELY HARDER THAN IT NEEDS TO BE. The target is given on the
RAW scale, not in logs:

    N_reach = L * 10^q                    (spans 10 to 10^12 over the box)
    N_id    = L / c1

The linear model in docs/22 was handed the log transform that makes the problem
trivial. Here the search must find the structure itself, from operators that
include but do not privilege the right ones. A search that only recovers the law
when handed log inputs has not recovered much.

TWO TARGETS, because they exercise different structure. N_reach needs an
exponential in one variable multiplied by the other. N_id is a plain quotient.
If the search finds the quotient and misses the exponential, that is worth
knowing and is reported rather than averaged away.

HONEST FAILURE MODES, checked for and reported:
  - an expression that fits the box and is not the law, which shows up as
    exact-looking in-box error and large out-of-box error, exactly as in docs/22
  - an expression algebraically equivalent to the law but written differently,
    which sympy is used to detect so it is not scored as a miss
  - the search finding nothing, which is a result about the operator set

Writes:  results/tables/symbolic_boundaries.csv
         docs/23_SYMBOLIC_RECOVERY.md
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
OUT = ROOT / "docs" / "23_SYMBOLIC_RECOVERY.md"

SEED = 20260906
TRAIN_L = (1.0, 1000.0)
TRAIN_Q = (1.0, 4.0)
TEST_L = (1000.0, 100000.0)
TEST_Q = (4.0, 8.0)
TRAIN_C1 = (1e-4, 1e-1)
TEST_C1 = (1e-6, 1e-4)
N_TRAIN, N_TEST = 2000, 1000


def draw_reach(n, lr, qr, rng):
    L = 10 ** rng.uniform(np.log10(lr[0]), np.log10(lr[1]), n)
    q = rng.uniform(*qr, n)
    return np.column_stack([L, q]), L * 10.0 ** q


def draw_id(n, lr, cr, rng):
    L = 10 ** rng.uniform(np.log10(lr[0]), np.log10(lr[1]), n)
    c1 = 10 ** rng.uniform(np.log10(cr[0]), np.log10(cr[1]), n)
    return np.column_stack([L, c1]), L / c1


def rel_err(pred, truth) -> float:
    """Relative error, because the targets span twelve orders of magnitude."""
    return float(np.median(np.abs(pred - truth) / np.abs(truth)))


def equivalent(expr_str: str, target: str, names: list[str]) -> bool:
    """Is the recovered expression algebraically the target, however written?

    Two traps, both hit on the first run of this module.

    The first is ordering: PySR returned `10.0**q*L` for a target written
    `L*10**q`. Those are the same expression with the factors swapped.

    The second is what defeated the original check. PySR emits float literals,
    so the recovered expression contains `10.0**q` while the target contains
    `10**q`. sympy treats 10.0 as a Float and 10 as an Integer and will not
    reduce their difference to exact zero, so `simplify(got - want) == 0` is
    False for two expressions that are identical. That mislabelled a full
    recovery as a miss.

    The fix is to rationalise the floats before comparing, and to fall back on
    a high-precision numerical identity over random points, which catches any
    equivalence sympy cannot see symbolically.
    """
    import sympy as sp
    syms = {n: sp.Symbol(n, positive=True) for n in names}
    try:
        got = sp.nsimplify(sp.sympify(expr_str, locals=syms), rational=True)
        want = sp.nsimplify(sp.sympify(target, locals=syms), rational=True)
        if sp.simplify(got - want) == 0:
            return True
    except Exception:
        pass
    # Numerical identity, to 30 digits, at points spread over the input range.
    try:
        got = sp.sympify(expr_str, locals=syms)
        want = sp.sympify(target, locals=syms)
        rng = np.random.default_rng(SEED)
        for _ in range(24):
            sub = {syms[n]: sp.Float(rng.uniform(0.5, 5.0), 30) for n in names}
            a = sp.N(got.subs(sub), 30)
            b = sp.N(want.subs(sub), 30)
            if abs(a - b) > abs(b) * sp.Float("1e-25"):
                return False
        return True
    except Exception:
        return False


def run(name, Xtr, ytr, Xin, yin, Xout, yout, var_names, target, ops):
    from pysr import PySRRegressor

    model = PySRRegressor(
        niterations=60,
        binary_operators=ops["binary"],
        unary_operators=ops["unary"],
        maxsize=18,
        populations=24,
        progress=False,
        verbosity=0,
        deterministic=True,
        parallelism="serial",
        random_state=SEED,
        temp_equation_file=True,
    )
    model.fit(Xtr, ytr, variable_names=var_names)
    best = str(model.sympy())
    return {
        "target": name,
        "recovered_expression": best,
        "true_law": target,
        "algebraically_equal": equivalent(best, target, var_names),
        "median_rel_err_in_box": rel_err(model.predict(Xin), yin),
        "median_rel_err_out_of_box": rel_err(model.predict(Xout), yout),
    }


def main() -> int:
    rng = np.random.default_rng(SEED)
    rows = []

    # -- N_reach = L * 10^q, on the raw scale ---------------------------------
    Xtr, ytr = draw_reach(N_TRAIN, TRAIN_L, TRAIN_Q, rng)
    Xin, yin = draw_reach(N_TEST, TRAIN_L, TRAIN_Q, rng)
    Xout, yout = draw_reach(N_TEST, TEST_L, TEST_Q, rng)
    rows.append(run("N_reach", Xtr, ytr, Xin, yin, Xout, yout,
                    ["L", "q"], "L*10**q",
                    {"binary": ["*", "/", "+", "-", "^"], "unary": ["exp", "log"]}))

    # -- N_id = L / c1 --------------------------------------------------------
    Xtr, ytr = draw_id(N_TRAIN, TRAIN_L, TRAIN_C1, rng)
    Xin, yin = draw_id(N_TEST, TRAIN_L, TRAIN_C1, rng)
    Xout, yout = draw_id(N_TEST, TEST_L, TEST_C1, rng)
    rows.append(run("N_id", Xtr, ytr, Xin, yin, Xout, yout,
                    ["L", "c1"], "L/c1",
                    {"binary": ["*", "/", "+", "-"], "unary": ["exp", "log"]}))

    res = pd.DataFrame(rows)
    TABLES.mkdir(parents=True, exist_ok=True)
    res.to_csv(TABLES / "symbolic_boundaries.csv", index=False)

    def g(x, n=3):
        return f"{x:.{n}g}"

    doc = f"""# Recovering the boundary laws by symbolic regression

Generated by `python -m src.symbolic_boundaries`. Seed {SEED}, PySR with a
serial deterministic backend, so the run reproduces.

`docs/22` found that neural networks fit the training box and failed outside it
by about three orders of magnitude, in any coordinates, and diagnosed the cause
as fitting a surface rather than committing to a structure. This tests the other
half of that diagnosis with a method that returns an expression instead of
weights.

## The test is harder than the one in docs/22

There the linear model was handed `log10 L` and `q`, which makes the law linear
and the problem trivial. Here the targets are given on the **raw** scale, so the
search has to find the structure itself:

- `N_reach = L * 10^q`, spanning about ten to a trillion across the box
- `N_id = L / c1`

Training used floors {TRAIN_L[0]:g} to {TRAIN_L[1]:g} per mL and depths
{TRAIN_Q[0]:g} to {TRAIN_Q[1]:g}; the extrapolation set used floors to
{TEST_L[1]:,g} and depths to {TEST_Q[1]:g}, outside in both variables. For
`N_id`, thresholds `c1` ran {TRAIN_C1[0]:g} to {TRAIN_C1[1]:g} in training and
{TEST_C1[0]:g} to {TEST_C1[1]:g} outside.

## Result

| target | true law | recovered | algebraically equal | median relative error, in box | out of box |
|---|---|---|---|---:|---:|
""" + "".join(
        f"| `{r.target}` | `{r.true_law}` | `{r.recovered_expression}` | "
        f"{'**yes**' if r.algebraically_equal else 'no'} | "
        f"{g(r.median_rel_err_in_box)} | {g(r.median_rel_err_out_of_box)} |\n"
        for r in res.itertuples()) + """
Relative rather than absolute error, because the targets span twelve orders of
magnitude and an absolute error would be meaningless across that range.

Equality is checked with sympy on the difference of the two expressions, so an
expression that is the law written differently is scored as a recovery and not
as a miss.

## Reading the result

The number that matters is the out-of-box error beside the in-box error. A
method that has found the law has essentially the same error in both, because a
recovered expression is not tied to the region it was fitted on. A method that
has found the region has a small in-box error and a large one outside, which is
the signature `docs/22` reported for both neural networks.

## Where this leaves the pipeline

The division of labour argued for in `docs/21` and `docs/22` was: learn the
extraction and the floor, derive everything downstream. Symbolic regression does
not change that conclusion, and it sharpens the reason for it. When a law exists
and the search recovers it, the right thing to ship is the law, not the search.
The value of running the search is that it says whether a law is there to be
found, which is exactly the question one cannot answer on a dataset where the
closed form is unknown, such as a biphasic kill curve.

That is the setting where this machinery earns its place: not on `L * 10^q`,
which is known, but on the parts of the problem where nobody has written the
formula down.
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")

    pd.set_option("display.width", 200)
    print(res.to_string(index=False))
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
