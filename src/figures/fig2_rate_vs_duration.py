"""
Figure 2. Where the inoculum is set by protocol, the two summaries still diverge.

Run:  python -m src.figures.fig2_rate_vs_duration

This figure used to be the spine of the paper. It is now the demonstration
that the arithmetic of Section 2.5 is not a property of clinical sampling: here
one strain from one stock went to six laboratories under one written protocol,
and the inoculum still decided which of them could produce a duration at all.

Panel A shows that every laboratory produces a kill rate. Panel B shows what
decides which of them can produce a crossing time at all.

The two survival panels that used to sit here -- the Kaplan-Meier curves and the
movement of the Cox p-values -- are now Figure S1. Both carried a disclaimer in
their own legend saying the between-laboratory comparison they display is not
valid, because the laboratory label is constant within its own cluster and there
are six clusters. A panel that has to disclaim itself belongs in the supplement,
where a reader who wants the descriptive picture can have it without the main
figure appearing to make a test it cannot make. `load` and `kaplan_meier` are
shared with that module so the two figures cannot drift apart.

Reads:
  results/tables/exp17_kill_rates.csv
  results/tables/exp17_survival.csv
  results/tables/exp17_baseline.csv
  results/tables/exp17_cox.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import style as st

ROOT = st.ROOT
T = ROOT / "results" / "tables"
ARM = "MXF 10x MIC"


def kaplan_meier(times, events):
    """Survival of the 'not yet crossed' state. No library, so it is auditable."""
    t = np.asarray(times, float)
    e = np.asarray(events, int)
    order = np.argsort(t)
    t, e = t[order], e[order]
    uniq = np.unique(t[e == 1])
    s, at_risk = 1.0, len(t)
    xs, ys = [0.0], [1.0]
    for u in uniq:
        n_risk = int((t >= u).sum())
        d = int(((t == u) & (e == 1)).sum())
        if n_risk > 0:
            s *= 1.0 - d / n_risk
        xs.extend([u, u])
        ys.extend([ys[-1], s])
    xs.append(float(t.max()))
    ys.append(ys[-1])
    return np.asarray(xs), np.asarray(ys)


def load():
    """The four tables and the colour assignment, shared with Figure S1.

    Identity is a laboratory that ever cleared versus one that never did. Two
    categories, so two categorical slots, and both carry a text label as well.
    Figure S1 imports this rather than recomputing it: the same laboratory must
    be the same colour in both figures or the reader is misled by the split.
    """
    rates = pd.read_csv(T / "exp17_kill_rates.csv")
    surv = pd.read_csv(T / "exp17_survival.csv")
    base = pd.read_csv(T / "exp17_baseline.csv").set_index("Institute")
    cox = pd.read_csv(T / "exp17_cox.csv")

    r = (rates[rates["arm"] == ARM]
         .dropna(subset=["kill_rate_tobit"])
         .set_index("institute").sort_index())
    treated = surv[surv["arm"] != "untreated"]
    cleared = treated.groupby("institute")["event"].max().astype(bool)
    col = {inst: (st.BLUE if cleared.get(inst, False) else st.ORANGE)
           for inst in r.index}
    return r, treated, base, cox, cleared, col


def build():
    st.apply()
    import matplotlib.pyplot as plt

    r, treated, base, cox, cleared, col = load()

    fig = plt.figure(figsize=(7.0, 3.3))
    gs = fig.add_gridspec(1, 2)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    # ---- A: every laboratory yields a rate -------------------------------
    y = np.arange(len(r))
    ax_a.hlines(y, r["kill_rate_ci_low"], r["kill_rate_ci_high"],
                color=[col[i] for i in r.index], lw=2.4, alpha=0.45)
    ax_a.scatter(r["kill_rate_tobit"], y, s=42, zorder=3,
                 color=[col[i] for i in r.index], edgecolor=st.SURFACE, lw=1.0)
    ax_a.axvline(0.0, color=st.INK_MUTED, lw=0.9, ls=(0, (4, 3)))
    ax_a.set_yticks(y, list(r.index))
    ax_a.set_xlabel("kill rate (log$_{10}$ CFU/mL per day)")
    ax_a.set_ylabel("laboratory")
    ax_a.set_title("A rate is estimable in all six", loc="left")
    ax_a.invert_yaxis()
    ax_a.grid(axis="y", visible=False)
    st.panel_tag(ax_a, "A")
    st.note(ax_a, f"{ARM}. Bars are 95% profile-likelihood intervals from the\n"
                  "censored (Tobit) fit. Blue: laboratory with a flask ever below\n"
                  "the floor at the 100 uL plating; orange: never, in any arm.", y=-0.30)

    # ---- B: what decides which half --------------------------------------
    xs = base.loc[r.index, "start_log10_cfu_ml"].to_numpy()
    ys = r["kill_rate_tobit"].to_numpy()
    ax_b.scatter(xs, ys, s=64, zorder=3, color=[col[i] for i in r.index],
                 edgecolor=st.SURFACE, lw=1.1)
    for inst, x0, y0 in zip(r.index, xs, ys):
        ax_b.annotate(inst, xy=(x0, y0), xytext=(0, 9),
                      textcoords="offset points", ha="center", fontsize=7.6,
                      fontweight="semibold", color=col[inst])
    cut = 0.5 * (sorted(xs)[2] + sorted(xs)[3])
    ax_b.axvline(cut, color=st.INK_MUTED, lw=0.9, ls=(0, (4, 3)))
    lo, hi = ax_b.get_ylim()
    ax_b.set_ylim(lo - 0.06 * (hi - lo), hi + 0.06 * (hi - lo))
    lo2, hi2 = ax_b.get_ylim()
    ax_b.text(cut - 0.08, lo2, "crossed ", ha="right", va="bottom", fontsize=7.2,
              color=st.BLUE, fontweight="semibold")
    ax_b.text(cut + 0.08, lo2, " never crossed", ha="left", va="bottom",
              fontsize=7.2, color=st.ORANGE, fontweight="semibold")
    ax_b.set_xlabel("starting density (log$_{10}$ CFU/mL)")
    ax_b.set_ylabel("kill rate (log$_{10}$ CFU/mL per day)")
    ax_b.set_title("The inoculum splits them; the rate does not", loc="left")
    st.panel_tag(ax_b, "B")
    st.note(ax_b, "The three lowest starting densities are exactly the three\n"
                  "laboratories that crossed at the 100 uL plating. F kills\n"
                  "faster than four of the other five and never crosses.", y=-0.30)

    return st.save(fig, "fig2_rate_vs_duration")


if __name__ == "__main__":
    for p in build():
        print(p)
