"""
Figure S1. Published pharmacodynamic constants transfer only when they are rates.

Run:  python -m src.figures.fig13_parameter_transfer

Panel A places the constants in routine use beside every admissible
mycobacterial measurement on one logarithmic axis, because the distance is the
finding and a linear axis would hide it. Panel B shows that the ratio which
alone sets the shape of the concentration-response curve is not a constant to be
looked up: it moves with drug, with physiological state and with the observation
window, inside a single laboratory. Panel C shows the consequence for the
exposure schedule, which fails before the parameters do.

Reads:
  results/tables/exp18_parameter_gaps.csv
  results/tables/exp18_shape_ratio.csv
  results/tables/exp18_cycle_balance.csv
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

    gaps = pd.read_csv(T / "exp18_parameter_gaps.csv")
    ratio = pd.read_csv(T / "exp18_shape_ratio.csv")
    cycle = pd.read_csv(T / "exp18_cycle_balance.csv")

    fig = plt.figure(figsize=(7.4, 6.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 0.9])
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    # ---- A: assumed against measured, on one log axis --------------------
    for i, (const, sub) in enumerate(gaps.groupby("constant")):
        sub = sub.sort_values("published_value", key=lambda s: s.abs())
        yy = np.arange(len(sub)) + (0 if const == "psi_max" else len(gaps) - len(sub))
        vals = sub["published_value"].abs().to_numpy()
        model = abs(float(sub["model_value"].iloc[0]))
        c = st.BLUE if const == "psi_max" else st.ORANGE
        ax_a.scatter(vals, yy, s=44, color=c, zorder=3,
                     edgecolor=st.SURFACE, lw=0.9)
        ax_a.hlines(yy, vals, model, color=c, lw=1.1, alpha=0.35, zorder=2)
        ax_a.scatter([model] * len(yy), yy, s=52, marker="D",
                     color=st.CRITICAL, zorder=4, edgecolor=st.SURFACE, lw=0.9)
        for y0, r in zip(yy, sub.itertuples()):
            ax_a.annotate(f"{r.state}  ({r.fold_gap:,.0f}x)",
                          xy=(abs(r.published_value), y0), xytext=(-9, 0),
                          textcoords="offset points", ha="right", va="center",
                          fontsize=6.6, color=st.INK_SECONDARY)
    ax_a.set_xscale("log")
    ax_a.set_yticks([])
    ax_a.set_xlim(2.5e-4, 22.0)
    ax_a.set_xlabel("rate, natural log per hour (absolute value)")
    ax_a.set_title("Assumed constants against every admissible mycobacterial "
                   "measurement", loc="left")
    ax_a.grid(axis="y", visible=False)
    ax_a.scatter([], [], s=52, marker="D", color=st.CRITICAL,
                 label="value assumed by the model")
    ax_a.scatter([], [], s=44, color=st.BLUE, label=r"measured $\psi_{max}$")
    ax_a.scatter([], [], s=44, color=st.ORANGE, label=r"measured $\psi_{min}$")
    ax_a.legend(loc="lower left", ncols=3, bbox_to_anchor=(0.0, -0.015))
    st.panel_tag(ax_a, "A")
    st.note(ax_a, "Only rates fitted inside a differential equation are shown. Every "
                  "maximum effect reported as a\ncumulative log reduction over a fixed "
                  "window is excluded, because its plateau is set by the\ninoculum "
                  "running out rather than by the drug saturating.", y=-0.20)

    # ---- B: the shape ratio is not a constant ----------------------------
    intra = ratio[ratio["state"].str.startswith("intracellular")].sort_values("ratio")
    yb = np.arange(len(intra))
    src_col = {"PMID 28356552": st.BLUE, "figshare 26462791": st.AQUA}
    cols = [src_col.get(s, st.INK_MUTED) for s in intra["source"]]
    ax_b.barh(yb, intra["ratio"], color=cols, height=0.62, zorder=3)
    model_ratio = 6.06
    ax_b.axvline(model_ratio, color=st.CRITICAL, lw=1.3, ls=(0, (5, 2)), zorder=4)
    ax_b.text(model_ratio, len(intra) - 0.4, " assumed 6.06", color=st.CRITICAL,
              fontsize=7.0, va="top", ha="left", fontweight="semibold")
    ax_b.axvline(1.0, color=st.INK_MUTED, lw=0.9, ls=(0, (2, 3)))
    ax_b.text(1.0, -0.75, "drug outruns growth ->", color=st.INK_MUTED,
              fontsize=6.6, va="center", ha="left")
    ax_b.set_yticks(yb, [f"{r.drug}, {r.state.split(',')[-1].strip()}"
                         for r in intra.itertuples()], fontsize=6.6)
    ax_b.set_xlabel(r"$-\psi_{min}/\psi_{max}$")
    ax_b.set_title("The shape ratio is not a constant", loc="left")
    ax_b.grid(axis="y", visible=False)
    st.panel_tag(ax_b, "B")
    st.note(ax_b, "Intracellular measurements only. Blue and green are two\n"
                  "independent laboratories. Within the second alone the ratio\n"
                  "runs 0.65 to 4.10 and halves between windows.", y=-0.34)

    # ---- C: the exposure schedule fails first ----------------------------
    cy = cycle.copy()
    cy["is_model"] = cy["parameters"].str.contains("model")
    cy = cy.sort_values("net_per_cycle")
    yc = np.arange(len(cy))
    cols = [st.CRITICAL if m else (st.ORANGE if not clears else st.BLUE)
            for m, clears in zip(cy["is_model"], cy["population_clears"])]
    ax_c.barh(yc, np.log10(cy["net_per_cycle"]), color=cols, height=0.62, zorder=3)
    ax_c.axvline(0.0, color=st.INK, lw=1.1, zorder=4)
    ax_c.text(0.02, len(cy) - 0.4, " population grows ->", color=st.ORANGE,
              fontsize=6.8, va="top", ha="left", fontweight="semibold")
    ax_c.set_yticks(yc, [p.replace(", intracellular", ", intra")
                         .replace(" (provisional)", "")
                         for p in cy["parameters"]], fontsize=6.4)
    ax_c.set_xlabel("log$_{10}$ net change per 24 h cycle")
    ax_c.set_title("At infinite drug, the cycle still fails", loc="left")
    ax_c.grid(axis="y", visible=False)
    st.panel_tag(ax_c, "C")
    n_fail = int((~cycle["population_clears"]).sum())
    st.note(ax_c, f"A 5 h pulse then 19 h regrowth. {n_fail} of the seven published\n"
                  "parameter sets leave the population growing at unlimited\n"
                  "drug. Six of those come from one publication.", y=-0.34)

    return st.save(fig, "fig13_parameter_transfer")


if __name__ == "__main__":
    for p in build():
        print(p)
