"""
Figure 4. Resistance and tolerance are separate axes, in two designs.

Run:  python -m src.figures.fig4_independence

Panel A is the whole family of twenty-four comparisons the 217-isolate file
supports, each against the Benjamini-Hochberg critical value it has to beat. It
is drawn this way so that the four nominally significant results are visible
together with the twenty that are not, which is the only honest way to show a
family. Panel B shows why the deepest endpoint should be read with care: it is
almost entirely censored. Panel C repeats the question in evolved clones, where
the design bound is drawn alongside the estimate so a null is bounded rather
than asserted.

Reads:
  results/tables/exp16_tb_independence.csv
  results/tables/exp16_tb_censoring.csv
  results/tables/exp19_axis_independence.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import style as st

ROOT = st.ROOT
T = ROOT / "results" / "tables"


def build():
    st.apply()
    import matplotlib.pyplot as plt

    ind = pd.read_csv(T / "exp16_tb_independence.csv").sort_values("p_value")
    cen = pd.read_csv(T / "exp16_tb_censoring.csv")
    clones = pd.read_csv(T / "exp19_axis_independence.csv")

    fig = plt.figure(figsize=(7.0, 6.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 0.85])
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    # ---- A: the whole family against its correction ----------------------
    y = np.arange(len(ind))
    nominal = ind["p_value"].to_numpy() < 0.05
    cols = np.where(nominal, st.WARNING, st.INK_MUTED)
    ax_a.scatter(ind["p_value"], y, s=34, color=cols, zorder=3,
                 edgecolor=st.SURFACE, lw=0.8)
    ax_a.plot(ind["bh_critical_value"], y, color=st.CRITICAL, lw=1.6,
              ls=(0, (5, 2)), zorder=2)
    ax_a.axvline(0.05, color=st.INK_MUTED, lw=0.9, ls=(0, (2, 3)))
    ax_a.set_xscale("log")
    labels = [f"{r.stratum}, {r.endpoint}" for r in ind.itertuples()]
    ax_a.set_yticks(y, labels, fontsize=6.4)
    ax_a.set_xlabel("p-value")
    ax_a.set_title("All 24 comparisons the file supports, against the "
                   "correction each must beat", loc="left")
    ax_a.invert_yaxis()
    ax_a.grid(axis="y", visible=False)
    ax_a.annotate("Benjamini-Hochberg\ncritical value",
                  xy=(float(ind["bh_critical_value"].iloc[len(ind) // 2]),
                      len(ind) // 2),
                  xytext=(-14, 0), textcoords="offset points", ha="right",
                  va="center", fontsize=7.0, color=st.CRITICAL,
                  fontweight="semibold")
    ax_a.text(0.05, len(ind) - 0.2, " nominal 0.05", fontsize=7.0,
              color=st.INK_MUTED, va="bottom", ha="left")
    st.panel_tag(ax_a, "A")
    n_nom = int(nominal.sum())
    st.note(ax_a, f"Amber: the {n_nom} results reaching nominal significance, where "
                  f"{0.05*len(ind):.1f} are expected by chance.\n"
                  "Every one of them lies to the right of the critical value it "
                  "would have to beat,\nso none survives. All four are negative, "
                  "the direction a shared mechanism does not predict.",
            y=-0.18)

    # ---- B: the deepest endpoint is almost entirely censored -------------
    order = cen.sort_values("fraction_censored")
    yb = np.arange(len(order))
    bar_col = [st.CRITICAL if f > 0.5 else st.BLUE
               for f in order["fraction_censored"]]
    ax_b.barh(yb, order["fraction_censored"], color=bar_col, height=0.62, zorder=3)
    for i, f in enumerate(order["fraction_censored"]):
        ax_b.text(f, i, f" {100*f:.0f}%", va="center", ha="left", fontsize=7.4,
                  fontweight="semibold", color=st.INK)
    ax_b.set_yticks(yb, order["endpoint"], fontsize=7.0)
    ax_b.set_xlim(0, 1.16)
    ax_b.set_xlabel("fraction of isolates at the assay ceiling")
    ax_b.set_title("The deepest endpoint is mostly censored", loc="left")
    ax_b.grid(axis="y", visible=False)
    st.panel_tag(ax_b, "B")
    st.note(ax_b, "Red where more than half the isolates never reached the\n"
                  "target within the six-day assay. The four nominal results\n"
                  "in panel A concentrate here.", y=-0.32)

    # ---- C: the same question in evolved clones --------------------------
    yc = np.arange(len(clones))
    ax_c.barh(yc, clones["detectable_rho_at_95pct"], height=0.62,
              color=st.GRID, zorder=2)
    ax_c.barh(yc, -clones["detectable_rho_at_95pct"], height=0.62,
              color=st.GRID, zorder=2)
    ax_c.scatter(clones["spearman_rho"], yc, s=52, color=st.BLUE, zorder=4,
                 edgecolor=st.SURFACE, lw=1.0)
    ax_c.axvline(0.0, color=st.INK_MUTED, lw=0.9)
    ax_c.set_yticks(yc, [f"{r.stratum} (n={r.n_clones})" for r in clones.itertuples()],
                    fontsize=7.0)
    ax_c.set_xlabel("Spearman rho, MIC against persister fraction")
    ax_c.set_title("126 evolved clones, one ancestor", loc="left")
    ax_c.invert_yaxis()
    ax_c.grid(axis="y", visible=False)
    st.panel_tag(ax_c, "C")
    st.note(ax_c, "Grey band: the correlation each stratum could have resolved\n"
                  "at 95% confidence. Every estimate falls inside its own band,\n"
                  "so the null is bounded rather than asserted.", y=-0.32)

    return st.save(fig, "fig4_independence")


if __name__ == "__main__":
    for p in build():
        print(p)
