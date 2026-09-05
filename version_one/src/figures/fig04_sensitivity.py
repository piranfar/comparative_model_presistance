"""
Figure 4. Sensitivity analysis: what the paper's method can and cannot see.

Run:  python -m src.experiments.exp03_sensitivity     (first)
      python -m src.figures.fig04_sensitivity

Panel A reproduces the paper's own one-at-a-time analysis on the printed
equation. It shows why the reported ranking is not a result: for any time past
t_c the printed persistence branch contains only k_slow and f, so k_fast and k_T
have identically zero effect on the 240 h endpoint and the ranking is fixed by
which symbols appear in which branch.

Panels B to E run the same question on the mechanistic model, where every
parameter acts at every time. The answer changes, and it is not the answer the
paper gives: the strongest single determinant of time to LOD in the
slow grower is the rate at which dormant cells wake up, not the rate at which
dormant cells are killed. Panel E shows why one-at-a-time analysis is the wrong
instrument for the fast grower, where most of the outcome variance comes from
parameters acting jointly.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import style as st

ROOT = st.ROOT
T = ROOT / "results" / "tables"

PRETTY = {"r": "r  replication", "Emax_S": "$E_{max,S}$  kill of replicating",
          "Emax_P": "$E_{max,P}$  kill of dormant",
          "EC50": "$EC_{50}$  potency", "H": "H  Hill slope",
          "k_SP": "$k_{S\\rightarrow P}$  entry to dormancy",
          "k_PS": "$k_{P\\rightarrow S}$  waking from dormancy",
          "k_fast": "$k_{fast}$", "k_slow": "$k_{slow}$",
          "f_dormant": "f  dormant fraction", "t_c": "$t_c$", "k_T": "$k_T$"}


def _tornado(ax, sub, title, xlabel):
    """Horizontal paired bars, ordered by the larger of the two excursions."""
    piv = sub.pivot_table(index="parameter", columns="perturbation",
                          values="pct_change")
    piv = piv.reindex(piv.abs().max(axis=1).sort_values().index)
    ypos = np.arange(len(piv))
    ax.barh(ypos - 0.19, piv["-10%"], height=0.36, color=st.BLUE,
            label="parameter -10%")
    ax.barh(ypos + 0.19, piv["+10%"], height=0.36, color=st.ORANGE,
            label="parameter +10%")
    ax.axvline(0, color=st.AXIS, lw=1.0)
    ax.set_yticks(ypos)
    ax.set_yticklabels([PRETTY.get(i, i) for i in piv.index], fontsize=7.0)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontsize=8.8)
    ax.grid(axis="y", visible=False)
    # mark the parameters with exactly zero influence
    for i, name in enumerate(piv.index):
        if np.allclose(piv.loc[name].values, 0.0, atol=1e-12):
            ax.text(0.0, i, "  no effect, by construction", va="center",
                    ha="left", fontsize=6.4, color=st.CRITICAL,
                    fontweight="semibold")
    return piv


def build():
    st.apply()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams["figure.constrained_layout.use"] = False

    oat_p = pd.read_csv(T / "sensitivity_oat_printed.csv")
    oat_m = pd.read_csv(T / "sensitivity_oat_mechanistic.csv")
    sob = pd.read_csv(T / "sensitivity_sobol.csv")
    inter = pd.read_csv(T / "sensitivity_interaction_fraction.csv")

    fig = plt.figure(figsize=(7.4, 7.2))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.0, 0.85],
                          left=0.19, right=0.985, top=0.905, bottom=0.085,
                          hspace=0.55, wspace=0.78)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c1 = fig.add_subplot(gs[1, 0])
    ax_c2 = fig.add_subplot(gs[1, 1])
    ax_d = fig.add_subplot(gs[2, :])

    # ---------------------------------------- A: paper's OAT, printed model -
    sub = oat_p[(oat_p["species"] == "Mtb") &
                (oat_p["endpoint"] == "log10_drop_240h_persistence")]
    _tornado(ax_a, sub, "A  method as published: OAT on the printed Eq. 4\n"
                        "     M. tuberculosis, log$_{10}$ drop at 240 h",
             "change in endpoint (%)")

    # ------------------------------------- B: same OAT, mechanistic model ---
    sub = oat_m[(oat_m["species"] == "Mtb") &
                (oat_m["endpoint"] == "time_to_LOD_h")]
    _tornado(ax_b, sub, "B  the same OAT on the mechanistic model\n"
                        "     M. tuberculosis, time to LOD",
             "change in endpoint (%)")
    ax_b.legend(loc="lower right", fontsize=6.4)

    # ------------------------------------------------- C: Sobol indices -----
    for ax, short, letter in ((ax_c1, "Mtb", "C"), (ax_c2, "S. aureus", "D")):
        s = sob[(sob["species"] == short) &
                (sob["endpoint"] == "time_to_LOD_h")].copy()
        s = s.sort_values("ST_total")
        ypos = np.arange(len(s))
        ax.barh(ypos - 0.19, s["S1_first_order"], height=0.36, color=st.BLUE,
                label="first order $S_1$ (acting alone)")
        ax.barh(ypos + 0.19, s["ST_total"], height=0.36, color=st.AQUA,
                label="total $S_T$ (including interactions)")
        ax.set_yticks(ypos)
        ax.set_yticklabels([PRETTY.get(i, i) for i in s["parameter"]],
                           fontsize=7.0)
        ax.set_xlabel("Sobol index")
        ax.set_xlim(-0.05, 1.0)
        ax.axvline(0, color=st.AXIS, lw=1.0)
        ax.grid(axis="y", visible=False)
        ax.set_title(f"{letter}  {st.SPECIES_LABEL[short]}, "
                     f"time to LOD", fontsize=8.8)
        if short == "Mtb":
            ax.legend(loc="lower right", fontsize=6.3)
            top = s.iloc[-1]
            ax.annotate(f"{100*top['ST_total']:.0f}% of the variance in how "
                        f"long\ntime to LOD takes",
                        xy=(top["ST_total"], len(s) - 1),
                        xytext=(-6, -34), textcoords="offset points",
                        ha="right", fontsize=6.5, color=st.INK_SECONDARY,
                        arrowprops=dict(arrowstyle="-|>", color=st.INK_MUTED,
                                        lw=0.9))

    # -------------------------------------------- D: interaction fraction ---
    piv = inter.pivot_table(index="endpoint", columns="species",
                            values="fraction_variance_from_interactions")
    labels = {"log10_drop_240h": "log$_{10}$ drop at 240 h",
              "MDK99_h": "MDK$_{99}$", "time_to_LOD_h": "time to LOD"}
    xpos = np.arange(len(piv))
    for i, short in enumerate(("Mtb", "S. aureus")):
        ax_d.bar(xpos + (i - 0.5) * 0.34, piv[short], width=0.32,
                 color=st.SPECIES_COLOR[short], label=st.SPECIES_LABEL[short])
        for x, v in zip(xpos + (i - 0.5) * 0.34, piv[short]):
            ax_d.text(x, v + 0.02, f"{100*v:.0f}%", ha="center", va="bottom",
                      fontsize=6.8, color=st.INK_SECONDARY,
                      fontweight="semibold")
    ax_d.set_xticks(xpos)
    ax_d.set_xticklabels([labels.get(i, i) for i in piv.index], fontsize=7.6)
    ax_d.set_ylabel("fraction of outcome variance\nfrom parameter interactions")
    ax_d.set_ylim(0, 1.12)
    ax_d.set_title("E  what one-at-a-time analysis cannot see", fontsize=8.8)
    ax_d.legend(loc="upper left", fontsize=7.0, ncols=2)
    ax_d.grid(axis="x", visible=False)

    fig.suptitle("Sensitivity analysis: the published ranking is an identity "
                 "of the equation, not a property of the bacteria",
                 fontsize=10.2, fontweight="semibold", x=0.006, ha="left",
                 y=0.982)
    # Read the design off the receipt rather than restating it, so the caption
    # cannot fall out of step with the run as it did once already.
    import json
    rec = json.loads((ROOT / "results" / "receipts" / "exp03_receipt.json")
                     .read_text(encoding="utf-8"))
    n_base = rec["sobol_base_samples"]
    n_eval = rec["sobol_model_evaluations_per_species"]
    fig.text(0.006, 0.052,
             "A and B vary one parameter at a time by +/-10%. C and D use "
             f"{n_eval:,} model evaluations per parameter set\n"
             f"(Saltelli estimator, {n_base:,} base samples, parameters "
             "log-uniform over +/-50%, exposure at four times each set's own "
             "MIC).\n"
             "Where the bars in E are tall, no one-at-a-time analysis can be "
             "trusted, however carefully it is run.",
             fontsize=6.8, color=st.INK_MUTED, ha="left", va="top",
             linespacing=1.6)
    return fig, sob, inter


def main() -> int:
    fig, sob, inter = build()
    paths = st.save(fig, "fig04_sensitivity")
    print(sob[sob["endpoint"] == "time_to_LOD_h"][
        ["species", "parameter", "S1_first_order", "ST_total"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3f}"))
    print()
    print(inter.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
