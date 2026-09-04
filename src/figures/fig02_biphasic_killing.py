"""
Figure 2. Biphasic killing: the printed equation against its two corrections.

Run:  python -m src.figures.fig02_biphasic_killing

This is the figure that decides the paper. Panels A and B put the printed Eq. 4
next to the two candidate replacements on the same axes and the same Table 1
parameters, so the discontinuity is visible rather than argued. Panel C zooms on
the transition. Panel D shows why the transition time cannot be a free
parameter: it is fixed by the other three, and the values asserted in Results
3.3 do not sit on that curve.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..models import corrected as fix
from ..models import paper_equations as eq
from ..models.parameters import LOD_CFU_ML, SPECIES, T_MAX_H
from . import style as st

ROOT = st.ROOT


def build():
    st.apply()
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(7.4, 6.2))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.92])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1], sharey=ax_a)
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    t = np.linspace(0.0, T_MAX_H, 4801)
    rows = []

    for ax, (short, sp) in zip((ax_a, ax_b), SPECIES.items()):
        printed = eq.persistence_as_printed(t, sp.N0, sp.k_fast, sp.k_slow,
                                            sp.f_dormant_point, sp.t_c_asserted)
        cont = fix.persistence_continuous(t, sp.N0, sp.k_fast, sp.k_slow,
                                          sp.t_c_asserted)
        biexp = fix.biexponential(t, sp.N0, sp.k_fast, sp.k_slow,
                                  sp.f_dormant_point)

        ax.plot(t, np.log10(np.maximum(printed, 1e-300)), color=st.CRITICAL,
                ls=(0, (5, 2)), lw=2.0, label="Eq. 4 as printed")
        ax.plot(t, np.log10(np.maximum(cont, 1e-300)), color=st.BLUE, lw=1.9,
                label="continuous piecewise")
        ax.plot(t, np.log10(np.maximum(biexp, 1e-300)), color=st.AQUA, lw=1.9,
                label="biexponential")

        left, right, fold, log10fold = eq.transition_jump(
            sp.N0, sp.k_fast, sp.f_dormant_point, sp.t_c_asserted)
        ax.annotate("", xy=(sp.t_c_asserted, np.log10(right)),
                    xytext=(sp.t_c_asserted, np.log10(left)),
                    arrowprops=dict(arrowstyle="-|>", color=st.CRITICAL,
                                    lw=1.4, shrinkA=0, shrinkB=0))
        ax.text(sp.t_c_asserted + 6, (np.log10(right) + np.log10(left)) / 2,
                f"+{log10fold:.2f} log$_{{10}}$\npopulation rises\nat $t_c$",
                fontsize=7.0, color=st.CRITICAL, fontweight="semibold",
                va="center")
        ax.axvline(sp.t_c_asserted, color=st.INK_MUTED, lw=0.8,
                   ls=(0, (1, 3)))
        ax.text(sp.t_c_asserted + 3, 1.15, f"$t_c$ = {sp.t_c_asserted:g} h",
                fontsize=6.8, color=st.INK_MUTED, ha="left")

        ax.set_xlim(0, T_MAX_H)
        ax.set_ylim(-4, 6.9)
        ax.set_xticks([0, 48, 96, 144, 192, 240])
        ax.set_xlabel("time on antibiotic (h)")
        ax.set_title(st.SPECIES_LABEL[short])
        st.lod_band(ax, np.log10(LOD_CFU_ML))

        rows.append({
            "species": short, "t_c_h": sp.t_c_asserted,
            "jump_log10": log10fold, "jump_fold": fold,
            "log10_N240_printed": float(np.log10(max(printed[-1], 1e-300))),
            "log10_N240_continuous": float(np.log10(max(cont[-1], 1e-300))),
            "log10_N240_biexponential": float(np.log10(max(biexp[-1], 1e-300))),
        })

    ax_a.set_ylabel("log$_{10}$ CFU/mL")
    ax_a.legend(loc="lower left", fontsize=7.0)

    # ---------------------------------------------------- C: zoom on t_c ----
    sp = SPECIES["Mtb"]
    tz = np.linspace(sp.t_c_asserted - 25, sp.t_c_asserted + 25, 2001)
    pz = eq.persistence_as_printed(tz, sp.N0, sp.k_fast, sp.k_slow,
                                   sp.f_dormant_point, sp.t_c_asserted)
    cz = fix.persistence_continuous(tz, sp.N0, sp.k_fast, sp.k_slow,
                                    sp.t_c_asserted)
    bz = fix.biexponential(tz, sp.N0, sp.k_fast, sp.k_slow, sp.f_dormant_point)
    ax_c.plot(tz, np.log10(pz), color=st.CRITICAL, ls=(0, (5, 2)), lw=2.0)
    ax_c.plot(tz, np.log10(cz), color=st.BLUE, lw=1.9)
    ax_c.plot(tz, np.log10(bz), color=st.AQUA, lw=1.9)
    st.direct_labels_decollided(ax_c, [
        (tz[-1], float(np.log10(pz[-1])), "as printed", st.CRITICAL),
        (tz[-1], float(np.log10(cz[-1])), "continuous", st.BLUE),
        (tz[-1], float(np.log10(bz[-1])), "biexponential", st.AQUA),
    ])
    ax_c.axvline(sp.t_c_asserted, color=st.INK_MUTED, lw=0.8, ls=(0, (1, 3)))
    ax_c.set_xlim(tz[0], tz[-1] + 14)
    ax_c.set_xlabel("time on antibiotic (h)")
    ax_c.set_ylabel("log$_{10}$ CFU/mL")
    ax_c.set_title("M. tuberculosis, transition region")
    st.note(ax_c, "At $t_c$ the printed second branch evaluates to exactly "
                  "$N_0$ for any amount of phase-1 killing.", y=-0.30)

    # ------------------------------------ D: t_c is fixed by the other three -
    f_grid = np.logspace(-4.5, -0.9, 400)
    for short, sp2 in SPECIES.items():
        tc_curve = np.log((1 - f_grid) / f_grid) / (sp2.k_fast - sp2.k_slow)
        color = st.SPECIES_COLOR[short]
        ax_d.plot(f_grid * 100, tc_curve, color=color, lw=1.9,
                  label=f"{st.SPECIES_LABEL[short]}: "
                        f"$k_{{fast}}$={sp2.k_fast:g}, $k_{{slow}}$={sp2.k_slow:g}")
        implied = eq.implied_t_c(sp2.k_fast, sp2.k_slow, sp2.f_dormant_point)
        ax_d.plot([sp2.f_dormant_point * 100], [implied], "o", color=color,
                  ms=6.5, mec=st.SURFACE, mew=1.2, zorder=5)
        ax_d.plot([sp2.f_dormant_point * 100], [sp2.t_c_asserted], "X",
                  color=st.CRITICAL, ms=8.5, mec=st.SURFACE, mew=1.2, zorder=6)
        ax_d.annotate("", xy=(sp2.f_dormant_point * 100, sp2.t_c_asserted),
                      xytext=(sp2.f_dormant_point * 100, implied),
                      arrowprops=dict(arrowstyle="-|>", color=st.CRITICAL,
                                      lw=1.2, shrinkA=2, shrinkB=2))
        # push the two labels apart in whichever direction keeps them clear
        up = 1 if sp2.t_c_asserted >= implied else -1
        ax_d.text(sp2.f_dormant_point * 100 * 1.3,
                  sp2.t_c_asserted + up * 4.5,
                  f"asserted {sp2.t_c_asserted:g} h",
                  fontsize=6.8, color=st.CRITICAL,
                  va="bottom" if up > 0 else "top", fontweight="semibold")
        ax_d.text(sp2.f_dormant_point * 100 * 1.3, implied - up * 4.5,
                  f"implied {implied:.1f} h", fontsize=6.8, color=color,
                  va="top" if up > 0 else "bottom")
        rows.append({"species": short, "t_c_asserted_h": sp2.t_c_asserted,
                     "t_c_implied_h": implied,
                     "f_dormant_pct": sp2.f_dormant_point * 100})

    ax_d.set_xscale("log")
    ax_d.set_xlabel("dormant fraction f (% of inoculum)")
    ax_d.set_ylabel("transition time $t_c$ (h)")
    ax_d.set_title("$t_c$ is determined, not free")
    ax_d.set_ylim(0, 130)
    ax_d.legend(loc="upper right", fontsize=6.6)
    st.note(ax_d, "$t_c = \\ln((1-f)/f)\\,/\\,(k_{fast}-k_{slow})$. Crosses "
                  "mark the values asserted in Results 3.3; neither lies on "
                  "its own curve.", y=-0.30)

    for ax, letter in zip((ax_a, ax_b, ax_c, ax_d), "ABCD"):
        st.panel_tag(ax, letter)

    fig.suptitle("Biphasic killing: the printed equation and its two "
                 "corrections, all on Table 1 parameters",
                 fontsize=10.5, fontweight="semibold", x=0.005, ha="left")
    fig.set_constrained_layout_pads(hspace=0.10, wspace=0.06)

    df = pd.DataFrame(rows)
    (ROOT / "results" / "tables").mkdir(parents=True, exist_ok=True)
    df.to_csv(ROOT / "results" / "tables" / "fig02_values.csv", index=False)
    return fig, df


def main() -> int:
    fig, df = build()
    paths = st.save(fig, "fig02_biphasic_killing")
    print(df.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
