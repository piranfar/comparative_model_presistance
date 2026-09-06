"""
Figure 1. A log-reduction endpoint is bounded by the assay floor, and the bound
decides the phenotype.

Run:  python -m src.figures.fig1_dynamic_range

This is the figure the rebuilt paper rests on, and it is drawn so the argument is
visible rather than asserted.

Panel A is the floor itself. The most probable number readings do not taper
towards zero; they stop at 23 per mL with a pile-up on it. If that were a tail
there would be values below it, and there are none anywhere in the file.

Panel B is the budget. Each isolate's headroom - the distance from its starting
density down to that floor - is plotted against the depth each tolerance endpoint
asks for. The 90 and 99 per cent endpoints sit under every isolate. The 99.99 per
cent endpoint does not, and the isolates it sits above could not have reached it
whatever rifampicin did to them.

Panel C is the consequence, and it is the panel to look at. Eighteen isolates
ended at the floor, so as far as the assay could resolve they were killed
identically. Their recorded surviving fractions lie exactly on the curve
L / N0, because that is what a reading at the floor computes. The classification
thresholds cut that curve, and the isolates fall on either side of the cut
according to where they started. Nothing about the drug enters.

Reads:
  data/raw/tb/elife93243_supp2.xlsx
  results/receipts/exp22_receipt.json
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import style as st

ROOT = st.ROOT
DATA = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
FLOOR = 23.0
AGE = 15                      # the panel where the classification is made
DEPTHS = {"90% (1 log)": 1.0, "99% (2 log)": 2.0, "99.99% (4 log)": 4.0}
# The deposited classification thresholds, recovered in exp22 by showing the
# classes do not overlap on the recorded surviving fraction.
LABEL_CUTS = {"low / medium": 1e-3, "medium / high": 1e-2}


def main() -> int:
    import matplotlib.pyplot as plt

    st.apply()
    d = pd.read_excel(DATA)
    n0 = d[f"mpn_T0_{AGE}days"].astype(float)
    n5 = d[f"mpn_T5_{AGE}days"].astype(float)
    head = np.log10(n0 / FLOOR)

    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.5))

    # -- A: the floor is a floor, not a tail ---------------------------------
    ax = axes[0]
    vc = n5.value_counts().sort_index()
    x = np.log10(vc.index.to_numpy(float))
    ax.bar(x, vc.to_numpy(), width=0.28, color=st.BLUE, edgecolor=st.SURFACE,
           linewidth=0.6)
    ax.axvline(np.log10(FLOOR), color=st.CRITICAL, lw=1.6, zorder=0)
    ax.annotate(f"floor\n{FLOOR:g} per mL", xy=(np.log10(FLOOR), vc.max() * 0.86),
                xytext=(np.log10(FLOOR) + 0.55, vc.max() * 0.86),
                color=st.CRITICAL, fontsize=8, va="center",
                arrowprops=dict(arrowstyle="->", color=st.CRITICAL, lw=1.0))
    ax.text(np.log10(FLOOR) + 0.55, vc.max() * 0.55,
            "nothing below it,\nanywhere in the file",
            fontsize=7.5, color=st.INK_SECONDARY, va="center")
    ax.set_xlabel("day-5 most probable number (log10 per mL)")
    ax.set_ylabel("isolates")
    ax.set_title("The readings stop; they do not taper", fontsize=9, loc="left")
    st.panel_tag(ax, "A")

    # -- B: the budget each isolate has --------------------------------------
    ax = axes[1]
    order = np.argsort(head.to_numpy())
    y = np.sort(head.dropna().to_numpy())
    ax.plot(np.arange(len(y)), y, lw=1.8, color=st.INK, zorder=3)
    for name, q in DEPTHS.items():
        short = int((head < q).sum())
        col = st.CRITICAL if short else st.INK_MUTED
        ax.axhline(q, color=col, lw=1.2, ls="--", zorder=1)
        ax.text(len(y) * 0.985, q + 0.10,
                f"{name}: {short} of {head.notna().sum()} short",
                fontsize=7.5, color=col, ha="right")
    below = y < 4.0
    ax.fill_between(np.arange(len(y)), y, 4.0, where=below, color=st.CRITICAL,
                    alpha=0.13, zorder=2)
    ax.set_xlabel("isolates, ranked by headroom")
    ax.set_ylabel("headroom (log10 above the floor)")
    ax.set_title("What each isolate could ever demonstrate", fontsize=9, loc="left")
    st.panel_tag(ax, "B")

    # -- C: the eighteen isolates that ended at the floor --------------------
    ax = axes[2]
    at = n5 <= FLOOR
    sub = d[at].copy()
    s0 = np.log10(sub[f"mpn_T0_{AGE}days"].astype(float))
    surv = sub[f"Survival_T5_{AGE}days"].astype(float)
    lab = sub[f"Tolerant_level_D5_{AGE}"]

    grid = np.linspace(s0.min() - 0.35, s0.max() + 0.35, 200)
    ax.plot(grid, np.log10(FLOOR / 10 ** grid), color=st.INK_MUTED, lw=1.3,
            ls="-", zorder=1)
    ax.text(grid[-1], np.log10(FLOOR / 10 ** grid[-1]) - 0.30,
            r"recorded fraction $= L/N_0$", fontsize=7.5, color=st.INK_SECONDARY,
            ha="right")

    for name, cut in LABEL_CUTS.items():
        ax.axhline(np.log10(cut), color=st.WARNING, lw=1.1, ls=":", zorder=0)
        ax.text(grid[0], np.log10(cut) + 0.09, name, fontsize=7,
                color=st.INK_SECONDARY, ha="left")

    for name, colour, marker in (("Low", st.BLUE, "o"), ("Medium", st.ORANGE, "s")):
        m = (lab == name).to_numpy()
        if not m.any():
            continue
        ax.scatter(s0[m], np.log10(surv[m]), s=46, color=colour, marker=marker,
                   edgecolor=st.SURFACE, linewidth=0.8, zorder=4,
                   label=f"{name} tolerance  (n={int(m.sum())})")
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    ax.set_xlabel("starting density (log10 per mL)")
    ax.set_ylabel("recorded surviving fraction (log10)")
    ax.set_title("Same endpoint, different phenotype", fontsize=9, loc="left")
    st.panel_tag(ax, "C")

    fig.tight_layout()
    paths = st.save(fig, "fig1_dynamic_range")

    n_short = int((head < 4).sum())
    print(f"-- figure 1 --")
    print(f"   isolates                              {int(head.notna().sum())}")
    print(f"   short of headroom for the 4-log endpoint  {n_short}")
    print(f"   isolates ending at the floor              {int(at.sum())}")
    print(f"   their starting densities span             "
          f"{10 ** (s0.max() - s0.min()):.0f}-fold")
    print(f"   their recorded survival spans             "
          f"{surv.max() / surv.min():.0f}-fold")
    for p in paths:
        print(f"   wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
