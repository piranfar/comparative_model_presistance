"""
Figure 3. The endpoint decides whether a 32-fold concentration range is visible.

Run:  python -m src.figures.fig11_endpoint_collapse

Panel A is the raw grid, so the reader sees the trajectories before any summary
of them. Panel B is the summary that matters: how far apart the top and bottom
of the concentration range are, read at each of the three sampling days. Panel C
fits the concentration slope separately in each interval, on a bootstrap over
replicates rather than on the four condition means, because two residual degrees
of freedom overstate precision.

The censoring bound is drawn on panel A rather than described, because the late
behaviour cannot be read without it.

Reads:
  results/tables/exp20_kill_grid.csv
  results/tables/exp20_endpoint_separation.csv
  results/tables/exp20_floor_sensitivity.csv
  data/raw/apramycin_mtb/Raw Data.xlsx  (replicates, for the bootstrap)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import style as st

ROOT = st.ROOT
T = ROOT / "results" / "tables"
XL = ROOT / "data" / "raw" / "apramycin_mtb" / "Raw Data.xlsx"
SEED = 20260905
N_BOOT = 20000


def replicate_grid():
    """Concentration x day x replicate, apramycin, from the deposited counts."""
    d = pd.read_excel(XL, sheet_name="Kill kinetics", header=None)
    base = d.iloc[3, 4:7].astype(float).to_numpy()
    k = d.iloc[4:, 1:7].copy()
    k.columns = ["day", "compound", "conc", "r1", "r2", "r3"]
    k["day"] = k["day"].ffill()
    k["compound"] = k["compound"].ffill()
    k = k[pd.to_numeric(k["r1"], errors="coerce").notna()].copy()
    k["dayn"] = k["day"].astype(str).str.extract(r"(\d+)").astype(float)
    ap = k[(k["compound"] == "Apramycin") & (k["conc"].astype(float) >= 4)]
    reps = {(float(r.conc), float(r.dayn)): np.array([r.r1, r.r2, r.r3], float)
            for r in ap.itertuples()}
    concs = sorted({c for c, _ in reps})
    for c in concs:
        reps[(c, 0.0)] = base
    return reps, concs


def bootstrap_slopes(reps, concs, days, rng):
    out = {}
    for a, b in zip(days[:-1], days[1:]):
        s = np.empty(N_BOOT)
        for j in range(N_BOOT):
            y = [(rng.choice(reps[(c, a)]) - rng.choice(reps[(c, b)])) / (b - a)
                 for c in concs]
            s[j] = np.polyfit(np.log2(concs), y, 1)[0]
        out[(a, b)] = s
    return out


def build():
    st.apply()
    import matplotlib.pyplot as plt

    grid = pd.read_csv(T / "exp20_kill_grid.csv").set_index("conc")
    sep = pd.read_csv(T / "exp20_endpoint_separation.csv")
    floor = pd.read_csv(T / "exp20_floor_sensitivity.csv")
    reps, concs = replicate_grid()
    rng = np.random.default_rng(SEED)
    days = [0.0, 3.0, 7.0, 14.0]
    draws = bootstrap_slopes(reps, concs, days, rng)

    fig = plt.figure(figsize=(7.4, 5.9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.9])
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    # ---- A: the trajectories ---------------------------------------------
    # concentration is an ordered magnitude, so one hue light to dark, not a
    # categorical set.
    import matplotlib.cm as cm
    order = sorted(grid.index)
    shades = plt.get_cmap("Blues")(np.linspace(0.42, 0.95, len(order)))
    daycols = [c for c in grid.columns if c.startswith("log10_day")]
    dvals = [float(c.replace("log10_day", "")) for c in daycols]
    ends = []
    for colr, c in zip(shades, order):
        ys = grid.loc[c, daycols].to_numpy(float)
        ax_a.plot(dvals, ys, marker="o", ms=4.5, color=colr, lw=1.9)
        ends.append((dvals[-1], ys[-1], f"{c:g} " + r"$\mu$g/mL", colr))
    st.direct_labels_decollided(ax_a, ends, min_gap_frac=0.085)
    lo_lim = float(floor.loc[floor["high_arm_censored"], "assumed_loq_log10"].min())
    st.lod_band(ax_a, lo_lim, "limit at 10 uL plating: the top arm is censored below this",
                xpos=0.62)
    ax_a.set_xlim(-0.6, 16.6)
    ax_a.set_xticks(dvals)
    ax_a.set_xlabel("days of exposure")
    ax_a.set_ylabel("log$_{10}$ CFU/mL")
    ax_a.set_title("Apramycin against M. tuberculosis, 32-fold concentration range",
                   loc="left")
    st.panel_tag(ax_a, "A")

    # ---- B: the separation, read at each day ------------------------------
    x = np.arange(len(sep))
    bars = ax_b.bar(x, sep["survivor_ratio_low_over_high"], width=0.58,
                    color=[st.INK_MUTED, st.BLUE, st.CRITICAL], zorder=3)
    for xi, v in zip(x, sep["survivor_ratio_low_over_high"]):
        ax_b.text(xi, v, f"{v:.1f}x", ha="center", va="bottom", fontsize=8.2,
                  fontweight="semibold", color=st.INK)
    ax_b.set_xticks(x, [f"day {int(d)}" for d in sep["day"]])
    ax_b.set_ylabel("survivor ratio, lowest / highest dose")
    ax_b.set_title("Read late, the dose range disappears", loc="left")
    ax_b.set_ylim(0, float(sep["survivor_ratio_low_over_high"].max()) * 1.22)
    ax_b.grid(axis="x", visible=False)
    st.panel_tag(ax_b, "B")
    st.note(ax_b, "The same 32-fold range of concentration, summarised at each\n"
                  "sampling day. A 14-day readout would call this drug\n"
                  "dose-insensitive.", y=-0.30)

    # ---- C: the slope, interval by interval -------------------------------
    labels, means, los, his = [], [], [], []
    for (a, b), s in draws.items():
        labels.append(f"days {int(a)}-{int(b)}")
        means.append(s.mean())
        lo, hi = np.percentile(s, [2.5, 97.5])
        los.append(lo)
        his.append(hi)
    y = np.arange(len(labels))
    cols = [st.BLUE if lo > 0 else st.CRITICAL if hi < 0 else st.INK_MUTED
            for lo, hi in zip(los, his)]
    ax_c.hlines(y, los, his, color=cols, lw=2.6, alpha=0.45)
    ax_c.scatter(means, y, s=46, color=cols, zorder=3, edgecolor=st.SURFACE, lw=1.0)
    ax_c.axvline(0.0, color=st.INK_MUTED, lw=0.9, ls=(0, (4, 3)))
    ax_c.set_yticks(y, labels)
    ax_c.set_xlabel("slope (log$_{10}$/day per doubling)")
    ax_c.set_title("Positive early, reversed late", loc="left")
    ax_c.invert_yaxis()
    ax_c.grid(axis="y", visible=False)
    st.panel_tag(ax_c, "C")
    st.note(ax_c, f"Bootstrap over all three replicates at both ends of every\n"
                  f"interval, {N_BOOT:,} draws. The late sign is not claimed: the\n"
                  "top arm may be censored (panel A).", y=-0.30)

    return st.save(fig, "fig11_endpoint_collapse")


if __name__ == "__main__":
    for p in build():
        print(p)
