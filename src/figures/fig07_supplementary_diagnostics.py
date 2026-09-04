"""
Figure S1. Three statistical claims in Methods 2.3, checked.

Run:  python -m src.experiments.exp01_recalculate_equations   (first)
      python -m src.experiments.exp02_fit_and_identifiability (first)
      python -m src.figures.fig07_supplementary_diagnostics

Panel A. Methods 2.3.3 reports a two-sample Kolmogorov-Smirnov test giving
p < 0.05 between the two species. A two-sample KS test compares the empirical
distributions of two random samples. Applied to two deterministic curves it
tests whether the curves are identical, which is known before the test is run,
and the p-value is then a function of how densely the curves were sampled. The
panel shows the p-value falling by more than 170 orders of magnitude as the
simulation grid is refined, while the KS statistic itself barely moves. The test
carries no inferential content here and should be removed.

Panel B. Methods 2.3.1 states that Euler integration with a 0.5 h step
cross-validated the solver results. Every model in Methods 2.1 is a closed-form
algebraic solution, so there is no differential equation to integrate. What the
comparison measures is the truncation error of Euler, shown here: it is a
property of the numerical scheme, not evidence about the model.

Panel C. Methods 2.3.3 reports R-squared > 0.9 as confirmation of fit quality.
Across the four fitting designs of exp02 the printed equation and its
replacement both clear 0.9 in three of four cases while differing by up to 84
AICc units. R-squared cannot rank these models; information criteria can.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..models import paper_equations as eq
from ..models.parameters import DT_EULER_H, MTB
from . import style as st

ROOT = st.ROOT
T = ROOT / "results" / "tables"


def build():
    st.apply()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams["figure.constrained_layout.use"] = False

    ks = pd.read_csv(T / "ks_test_grid_dependence.csv")
    comp = pd.read_csv(T / "r2_vs_aicc_discrimination.csv")

    fig = plt.figure(figsize=(7.4, 2.9))
    gs = fig.add_gridspec(1, 3, left=0.075, right=0.985, top=0.825,
                          bottom=0.235, wspace=0.36)
    ax_a, ax_b, ax_c = (fig.add_subplot(gs[0, i]) for i in range(3))

    # ------------------------------------------------------- A: KS test -----
    ax_a.plot(ks["n_grid_points"], ks["p_value"].clip(lower=1e-200),
              color=st.CRITICAL, lw=2.0, marker="o", ms=4.5,
              label="p-value")
    ax_a.axhline(0.05, color=st.INK_MUTED, lw=1.0, ls=(0, (4, 3)))
    ax_a.text(ks["n_grid_points"].min(), 0.05, " p = 0.05 ", fontsize=6.6,
              color=st.INK_MUTED, va="bottom")
    ax_a.set_xscale("log")
    ax_a.set_yscale("log")
    ax_a.set_ylim(1e-200, 5)
    ax_a.set_xlabel("simulation grid points over 240 h")
    ax_a.set_ylabel("KS two-sample p-value")
    ax_a.set_title("A  the p-value tracks the grid,\n     not the biology",
                   fontsize=8.4)
    stat_range = ks["ks_statistic"].max() - ks["ks_statistic"].min()
    ax_a.text(0.96, 0.06,
              f"KS statistic varies by only\n{stat_range:.3f} over this range",
              transform=ax_a.transAxes, ha="right", va="bottom", fontsize=6.5,
              color=st.INK_SECONDARY)

    # -------------------------------------------------- B: Euler error ------
    rhs = lambda t, N: -MTB.k_fast * N
    for dt, color, label in ((1.0, st.ORANGE, "dt = 1 h"),
                             (DT_EULER_H, st.BLUE, "dt = 0.5 h"),
                             (0.1, st.AQUA, "dt = 0.1 h")):
        t_e, N_e = eq.euler_solution(rhs, MTB.N0, 48.0, dt)
        exact = MTB.N0 * np.exp(-MTB.k_fast * t_e)
        ax_b.plot(t_e, 100.0 * (N_e - exact) / exact, color=color, lw=1.9,
                  label=label)
        st.direct_label(ax_b, t_e[-1], 100.0 * (N_e[-1] - exact[-1]) / exact[-1],
                        label, color, dx=-4, ha="right")
    ax_b.axhline(0, color=st.AXIS, lw=1.0)
    ax_b.set_xlabel("time (h)")
    ax_b.set_ylabel("Euler error vs exact solution (%)")
    ax_b.set_title("B  what the stated cross-validation\n     actually measures",
                   fontsize=8.4)
    ax_b.legend(loc="lower left", fontsize=6.5)

    # ----------------------------------------------- C: R2 versus AICc ------
    lbl = [f"{r.species}\n{r.design.split('(')[0].strip()}"
           for r in comp.itertuples()]
    x = np.arange(len(comp))
    ax_c.bar(x - 0.19, comp["r2_printed"], width=0.36, color=st.CRITICAL,
             label="Eq. 4 as printed")
    ax_c.bar(x + 0.19, comp["r2_biexponential"], width=0.36, color=st.AQUA,
             label="biexponential")
    ax_c.axhline(0.9, color=st.INK, lw=1.1, ls=(0, (4, 3)))
    ax_c.text(len(comp) - 0.45, 0.905, "the reported threshold, $R^2$ > 0.9",
              fontsize=6.4, color=st.INK, ha="right", va="bottom")
    for xi, row in zip(x, comp.itertuples()):
        ax_c.text(xi, 1.005,
                  f"$\\Delta$AICc {row.delta_aicc_printed_minus_biexp:.0f}",
                  ha="center", va="bottom", fontsize=6.3,
                  color=st.INK_SECONDARY, fontweight="semibold")
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(lbl, fontsize=6.3)
    ax_c.set_ylim(0.8, 1.07)
    ax_c.set_ylabel("$R^2$")
    ax_c.set_title("C  both models clear the reported\n     threshold; AICc "
                   "does not tie", fontsize=8.4)
    ax_c.legend(loc="lower left", fontsize=6.4, ncols=2, columnspacing=0.8,
                frameon=True, framealpha=0.93, edgecolor="none",
                facecolor=st.SURFACE)
    ax_c.grid(axis="x", visible=False)

    fig.suptitle("Supplementary: three statistical claims in Methods 2.3, "
                 "checked", fontsize=10.2, fontweight="semibold", x=0.006,
                 ha="left", y=0.985)
    fig.text(0.006, 0.105,
             "C uses the synthetic fits of exp02; the AICc gap above each pair "
             "is the printed equation minus the biexponential, so a positive "
             "number favours the replacement.",
             fontsize=6.8, color=st.INK_MUTED, ha="left", va="top")
    return fig, ks, comp


def main() -> int:
    fig, ks, comp = build()
    paths = st.save(fig, "fig07_supplementary_diagnostics")
    print(ks.to_string(index=False))
    print()
    print(comp[["species", "design", "r2_printed", "r2_biexponential",
                "delta_aicc_printed_minus_biexp",
                "both_r2_above_0.9"]].to_string(
        index=False, float_format=lambda v: f"{v:,.4g}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
