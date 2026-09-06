"""
Figure 2. Where the inoculum is set by protocol, the two summaries still diverge.

Run:  python -m src.figures.fig2_rate_vs_duration

This figure used to be the spine of the paper. It is now the demonstration
that the arithmetic of Section 2.5 is not a property of clinical sampling: here
one strain from one stock went to six laboratories under one written protocol,
and the inoculum still decided which of them could produce a duration at all.

Panel A shows that every laboratory produces a kill rate. Panel B shows that half
of them produce no clearance time on the same flasks. Panel C shows what decides
which half. Panel D shows what happens when the starting density enters a Cox
model - three laboratories stop being distinguishable and one does not, which is
reported rather than absorbed.

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
    """Survival of the 'not yet cleared' state. No library, so it is auditable."""
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


def build():
    st.apply()
    import matplotlib.pyplot as plt

    rates = pd.read_csv(T / "exp17_kill_rates.csv")
    surv = pd.read_csv(T / "exp17_survival.csv")
    base = pd.read_csv(T / "exp17_baseline.csv").set_index("Institute")
    cox = pd.read_csv(T / "exp17_cox.csv")

    r = (rates[rates["arm"] == ARM]
         .dropna(subset=["kill_rate_tobit"])
         .set_index("institute").sort_index())
    treated = surv[surv["arm"] != "untreated"]
    cleared = treated.groupby("institute")["event"].max().astype(bool)

    # identity: a laboratory that ever cleared vs one that never did. Two
    # categories, so two categorical slots, and both carry a text label as well.
    col = {inst: (st.BLUE if cleared.get(inst, False) else st.ORANGE)
           for inst in r.index}

    fig = plt.figure(figsize=(7.4, 6.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.95])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

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
                  "censored (Tobit) fit. Blue: laboratory ever cleared a flask.\n"
                  "Orange: never cleared, in any arm.", y=-0.30)

    # ---- B: half of them yield no duration -------------------------------
    flat = []
    ends = []
    for inst, g in treated.groupby("institute"):
        xs, ys = kaplan_meier(g["time_days"], g["event"])
        ax_b.step(xs, ys, where="post", color=col[inst], lw=1.9,
                  alpha=0.95 if cleared.get(inst, False) else 0.75)
        if ys[-1] >= 0.999:
            flat.append((inst, xs[-1]))          # never descends: identical line
        else:
            ends.append((xs[-1], ys[-1], inst, col[inst]))
    # The laboratories that never cleared trace the same horizontal line, so one
    # label names all of them rather than three labels overprinting each other.
    if flat:
        ax_b.annotate(", ".join(i for i, _ in sorted(flat)),
                      xy=(max(x for _, x in flat), 1.0), xytext=(5, 0),
                      textcoords="offset points", fontsize=7.6,
                      fontweight="semibold", color=st.ORANGE, va="center")
    st.direct_labels_decollided(ax_b, ends, min_gap_frac=0.075)
    ax_b.set_ylim(-0.03, 1.05)
    ax_b.set_xlabel("days of exposure")
    ax_b.set_ylabel("fraction of flasks still detectable")
    ax_b.set_title("A duration is undefined in three", loc="left")
    st.panel_tag(ax_b, "B")
    st.note(ax_b, "Kaplan-Meier over all treated flasks. Three curves never\n"
                  "descend: those laboratories recorded no flask below the\n"
                  "limit in any arm, so no clearance time exists for them.",
            y=-0.30)

    # ---- C: what decides which half --------------------------------------
    xs = base.loc[r.index, "start_log10_cfu_ml"].to_numpy()
    ys = r["kill_rate_tobit"].to_numpy()
    ax_c.scatter(xs, ys, s=64, zorder=3, color=[col[i] for i in r.index],
                 edgecolor=st.SURFACE, lw=1.1)
    for inst, x0, y0 in zip(r.index, xs, ys):
        ax_c.annotate(inst, xy=(x0, y0), xytext=(0, 9),
                      textcoords="offset points", ha="center", fontsize=7.6,
                      fontweight="semibold", color=col[inst])
    cut = 0.5 * (sorted(xs)[2] + sorted(xs)[3])
    ax_c.axvline(cut, color=st.INK_MUTED, lw=0.9, ls=(0, (4, 3)))
    lo, hi = ax_c.get_ylim()
    ax_c.set_ylim(lo - 0.06 * (hi - lo), hi + 0.06 * (hi - lo))
    lo2, hi2 = ax_c.get_ylim()
    ax_c.text(cut - 0.08, lo2, "cleared ", ha="right", va="bottom", fontsize=7.2,
              color=st.BLUE, fontweight="semibold")
    ax_c.text(cut + 0.08, lo2, " never cleared", ha="left", va="bottom",
              fontsize=7.2, color=st.ORANGE, fontweight="semibold")
    ax_c.set_xlabel("starting density (log$_{10}$ CFU/mL)")
    ax_c.set_ylabel("kill rate (log$_{10}$ CFU/mL per day)")
    ax_c.set_title("The inoculum splits them; the rate does not", loc="left")
    st.panel_tag(ax_c, "C")
    st.note(ax_c, "The three lowest starting densities are exactly the three\n"
                  "laboratories that cleared. F kills faster than four of the\n"
                  "other five and never clears.", y=-0.30)

    # ---- D: the laboratory stops explaining ------------------------------
    before = cox[cox["model"] == "institute only"].set_index("term")["p_value"]
    after = cox[cox["model"] == "institute + starting density"].set_index("term")["p_value"]
    terms = [t for t in before.index if str(t).startswith("institute_")
             and t in after.index]
    labs = [t.replace("institute_", "") for t in terms]
    yb = np.arange(len(terms))
    for i, t_ in enumerate(terms):
        c = st.BLUE if after[t_] >= 0.05 <= 1 and before[t_] < 0.05 else st.INK_MUTED
        c = st.BLUE if (before[t_] < 0.05 and after[t_] >= 0.05) else st.ORANGE if after[t_] < 0.05 else st.INK_MUTED
        ax_d.annotate("", xy=(after[t_], i), xytext=(before[t_], i),
                      arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6,
                                      shrinkA=2, shrinkB=2))
        ax_d.scatter([before[t_]], [i], s=26, color=st.INK_MUTED, zorder=3)
        ax_d.scatter([after[t_]], [i], s=44, color=c, zorder=4,
                     edgecolor=st.SURFACE, lw=0.9)
    ax_d.axvline(0.05, color=st.CRITICAL, lw=1.0, ls=(0, (4, 3)))
    ax_d.text(0.05, -0.85, " p = 0.05", color=st.CRITICAL,
              fontsize=7.0, va="center", ha="left")
    ax_d.set_ylim(len(terms) - 0.4, -1.2)
    ax_d.set_xscale("log")
    ax_d.set_yticks(yb, labs)
    ax_d.set_xlabel("p-value for the laboratory term (Cox model)")
    ax_d.set_ylabel("laboratory")
    ax_d.set_title("Adjusting for the inoculum absorbs three of four", loc="left")
    ax_d.grid(axis="y", visible=False)
    st.panel_tag(ax_d, "D")
    st.note(ax_d, "Grey: laboratory alone. Arrow head: after adding starting\n"
                  "density. Blue crosses from significant to not. Orange (C)\n"
                  "stays significant and also has the fastest rate.", y=-0.30)

    return st.save(fig, "fig2_rate_vs_duration")


if __name__ == "__main__":
    for p in build():
        print(p)
