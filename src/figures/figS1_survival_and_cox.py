"""
Figure S1. The descriptive survival picture behind Figure 2.

Run:  python -m src.figures.figS1_survival_and_cox

These two panels were Figure 2B and Figure 2D. They are here because each had to
disclaim itself in its own legend: every flask in a laboratory shares a starting
culture, so what looks like sixty-seven flasks is six clusters, and for a
three-against-three split of six clusters the smallest attainable two-sided
p-value is 0.10. No between-laboratory test is available and none is claimed.
What the panels do show is descriptive and worth keeping -- three laboratories
produce no crossing time at all, and adjusting for the starting density moves
five of the six laboratory terms toward p = 1 -- so they are reported in the
supplement rather than deleted or promoted.

Colour, the cleared/never-cleared split and the four tables come from
`fig2_rate_vs_duration.load`, so a laboratory is the same colour in both figures.

Reads:
  results/tables/exp17_survival.csv
  results/tables/exp17_cox.csv
  (via fig2_rate_vs_duration.load, which also reads the rate and baseline tables)
"""
from __future__ import annotations

import numpy as np

from . import style as st
from .fig2_rate_vs_duration import ARM, kaplan_meier, load


def build():
    st.apply()
    import matplotlib.pyplot as plt

    r, treated, base, cox, cleared, col = load()

    fig = plt.figure(figsize=(7.0, 3.3))
    gs = fig.add_gridspec(1, 2)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    # ---- A: half of them yield no duration -------------------------------
    flat = []
    ends = []
    for inst, g in treated.groupby("institute"):
        xs, ys = kaplan_meier(g["time_days"], g["event"])
        ax_a.step(xs, ys, where="post", color=col[inst], lw=1.9,
                  alpha=0.95 if cleared.get(inst, False) else 0.75)
        if ys[-1] >= 0.999:
            flat.append((inst, xs[-1]))          # never descends: identical line
        else:
            ends.append((xs[-1], ys[-1], inst, col[inst]))
    # The laboratories that never cleared trace the same horizontal line, so one
    # label names all of them rather than three labels overprinting each other.
    if flat:
        ax_a.annotate(", ".join(i for i, _ in sorted(flat)),
                      xy=(max(x for _, x in flat), 1.0), xytext=(5, 0),
                      textcoords="offset points", fontsize=7.6,
                      fontweight="semibold", color=st.ORANGE, va="center")
    st.direct_labels_decollided(ax_a, ends, min_gap_frac=0.075)
    ax_a.set_ylim(-0.03, 1.05)
    ax_a.set_xlabel("days of exposure")
    ax_a.set_ylabel("fraction of flasks still detectable")
    ax_a.set_title("A duration is undefined in three", loc="left")
    st.panel_tag(ax_a, "A")
    st.note(ax_a, "Kaplan-Meier, all treated flasks, 100 uL plating. Three\n"
                  "curves never descend: those laboratories recorded no flask\n"
                  "below the floor in any arm, so no crossing time exists.",
            y=-0.30)

    # ---- B: the laboratory stops explaining ------------------------------
    before = cox[cox["model"] == "institute only"].set_index("term")["p_value"]
    after = cox[cox["model"] == "institute + starting density"].set_index("term")["p_value"]
    terms = [t for t in before.index if str(t).startswith("institute_")
             and t in after.index]
    labs = [t.replace("institute_", "") for t in terms]
    yb = np.arange(len(terms))
    for i, t_ in enumerate(terms):
        c = (st.BLUE if (before[t_] < 0.05 and after[t_] >= 0.05)
             else st.ORANGE if after[t_] < 0.05 else st.INK_MUTED)
        ax_b.annotate("", xy=(after[t_], i), xytext=(before[t_], i),
                      arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6,
                                      shrinkA=2, shrinkB=2))
        ax_b.scatter([before[t_]], [i], s=26, color=st.INK_MUTED, zorder=3)
        ax_b.scatter([after[t_]], [i], s=44, color=c, zorder=4,
                     edgecolor=st.SURFACE, lw=0.9)
    ax_b.axvline(0.05, color=st.CRITICAL, lw=1.0, ls=(0, (4, 3)))
    ax_b.text(0.05, -0.85, " p = 0.05", color=st.CRITICAL,
              fontsize=7.0, va="center", ha="left")
    ax_b.set_ylim(len(terms) - 0.4, -1.2)
    ax_b.set_xscale("log")
    ax_b.set_yticks(yb, labs)
    ax_b.set_xlabel("p-value for the laboratory term (Cox model)")
    ax_b.set_ylabel("laboratory")
    ax_b.set_title("Adjusting for the inoculum absorbs three of four", loc="left")
    ax_b.grid(axis="y", visible=False)
    st.panel_tag(ax_b, "B")
    st.note(ax_b, "Grey: laboratory alone. Arrow head: after adding starting\n"
                  "density. Blue crosses from significant to not. Orange (C)\n"
                  "stays significant and also has the fastest rate.", y=-0.30)

    return st.save(fig, "figS1_survival_and_cox")


if __name__ == "__main__":
    for p in build():
        print(p)
