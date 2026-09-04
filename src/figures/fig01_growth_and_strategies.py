"""
Figure 1. Growth and the three survival strategies, as printed and corrected.

Run:  python -m src.figures.fig01_growth_and_strategies

Replaces the original Figure 1, which showed the three survival laws on one set
of axes without a carrying capacity. Top row is the paper's equations exactly as
printed; bottom row is the same scenarios with the carrying capacity of Eq. 1
actually applied. The point of the pairing is visible in panel B: with Table 1's
S. aureus values the printed resistance equation reaches 10^51 CFU/mL by day 10,
which is 20 orders of magnitude beyond the total prokaryotic population of
Earth, purely because K is declared in Eq. 1 and then omitted from Eq. 2.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..models import corrected as fix
from ..models import paper_equations as eq
from ..models.parameters import LOD_CFU_ML, SPECIES, T_MAX_H
from . import style as st

ROOT = st.ROOT
EARTH_LOG10 = np.log10(5.0e30)   # Whitman et al. 1998 PNAS, order of magnitude


def build():
    st.apply()
    import matplotlib.pyplot as plt

    t = np.linspace(0.0, T_MAX_H, 2401)
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.9), sharex=True)
    rows = []

    for col, (short, sp) in enumerate(SPECIES.items()):
        color = st.SPECIES_COLOR[short]
        ax_top, ax_bot = axes[0, col], axes[1, col]

        # ---------------- top: exactly as printed -------------------------
        growth = eq.logistic_growth(t, sp.N0, sp.K, sp.r)
        resist = eq.resistance_as_printed(t, sp.N0, sp.r, sp.k_R)
        toler = eq.tolerance_as_printed(t, sp.N0, sp.k_T)
        persist = eq.persistence_as_printed(t, sp.N0, sp.k_fast, sp.k_slow,
                                            sp.f_dormant_point, sp.t_c_asserted)

        series = [
            ("no drug (Eq. 1, logistic)", growth, st.INK_MUTED, (0, (1, 2))),
            ("resistance (Eq. 2)", resist, st.STRATEGY_COLOR["resistance"], (0, (5, 2))),
            ("tolerance (Eq. 3)", toler, st.STRATEGY_COLOR["tolerance"], (0, (5, 2))),
            ("persistence (Eq. 4)", persist, st.STRATEGY_COLOR["persistence"], (0, (5, 2))),
        ]
        for label, y, c, dash in series:
            ax_top.plot(t, np.log10(np.maximum(y, 1e-300)), color=c, ls=dash,
                        lw=1.9, label=label)

        ax_top.axhline(np.log10(sp.K), color=st.AXIS, lw=1.0, ls="-")
        ax_top.text(0.985, np.log10(sp.K),
                    "carrying capacity K, in Eq. 1 only ",
                    transform=ax_top.get_yaxis_transform(), ha="right",
                    va="bottom", fontsize=6.4, color=st.INK_SECONDARY)

        top_max = np.log10(resist.max())
        if top_max > EARTH_LOG10:
            ax_top.axhline(EARTH_LOG10, color=st.CRITICAL, lw=1.0,
                           ls=(0, (2, 2)))
            ax_top.text(0.015, EARTH_LOG10, " all prokaryotes on Earth ",
                        transform=ax_top.get_yaxis_transform(), ha="left",
                        va="bottom", fontsize=6.4, color=st.CRITICAL,
                        fontweight="semibold")
        ax_top.set_ylim(-1, max(top_max * 1.08, np.log10(sp.K) + 1))
        ax_top.set_title(f"{st.SPECIES_LABEL[short]} - as printed")

        # ---------------- bottom: corrected -------------------------------
        resist_fix = fix.logistic_with_kill(t, sp.N0, sp.K, sp.r, sp.k_R)
        toler_fix = fix.logistic_with_kill(t, sp.N0, sp.K, sp.r, sp.k_T)
        persist_fix = fix.biexponential(t, sp.N0, sp.k_fast, sp.k_slow,
                                        sp.f_dormant_point)

        to_label = []
        for label, y, c in [
            ("no drug (logistic)", growth, st.INK_MUTED),
            ("resistance: growth to K", resist_fix,
             st.STRATEGY_COLOR["resistance"]),
            ("tolerance: net rate r - k_T", toler_fix,
             st.STRATEGY_COLOR["tolerance"]),
            ("persistence: biexponential", persist_fix,
             st.STRATEGY_COLOR["persistence"]),
        ]:
            ls = (0, (1, 2)) if "no drug" in label else "-"
            ax_bot.plot(t, np.log10(np.maximum(y, 1e-300)), color=c, ls=ls,
                        lw=1.9, label=label)
            if "no drug" not in label:
                to_label.append((t[-1], np.log10(max(y[-1], 1e-300)),
                                 label.split(":")[0], c))

        ax_bot.axhline(np.log10(sp.K), color=st.AXIS, lw=1.0)
        ax_bot.set_ylim(-1, np.log10(sp.K) + 0.6)
        st.direct_labels_decollided(ax_bot, to_label)
        st.lod_band(ax_bot, np.log10(LOD_CFU_ML))
        ax_bot.set_title(f"{st.SPECIES_LABEL[short]} - corrected")
        ax_bot.set_xlabel("time on antibiotic (h)")

        for ax in (ax_top, ax_bot):
            ax.set_xlim(0, T_MAX_H)
            ax.set_xticks([0, 48, 96, 144, 192, 240])
        if col == 0:
            ax_top.set_ylabel("log$_{10}$ CFU/mL")
            ax_bot.set_ylabel("log$_{10}$ CFU/mL")

        for name, y_pr, y_fx in [
            ("resistance", resist, resist_fix),
            ("tolerance", toler, toler_fix),
            ("persistence", persist, persist_fix),
        ]:
            rows.append({
                "species": short, "strategy": name,
                "log10_N_240h_as_printed": float(np.log10(max(y_pr[-1], 1e-300))),
                "log10_N_240h_corrected": float(np.log10(max(y_fx[-1], 1e-300))),
                "log10_K": float(np.log10(sp.K)),
                "exceeds_K_as_printed": bool(y_pr[-1] > sp.K),
            })

    axes[0, 0].legend(loc="lower left", ncols=1, fontsize=6.9)
    axes[1, 0].legend(loc="lower left", ncols=1, fontsize=6.9)
    for ax, letter in zip(axes.ravel(), "ABCD"):
        st.panel_tag(ax, letter)

    fig.suptitle("Growth and the three survival strategies: printed equations "
                 "(top) and corrected equations (bottom)",
                 fontsize=10.5, fontweight="semibold", x=0.005, ha="left")
    sa = SPECIES["S. aureus"]
    sa_240 = eq.resistance_as_printed(np.array([240.0]), sa.N0, sa.r, sa.k_R)[0]
    fig.text(0.005, -0.035,
             "Parameters are Table 1 of the preprint, unchanged.\n"
             "Panel B: the printed resistance equation has no "
             "carrying-capacity term, so S. aureus reaches "
             f"10$^{{{np.log10(sa_240):.0f}}}$ CFU/mL at 240 h.\n"
             "Panels C and D apply the K declared in Eq. 1 to every strategy "
             "and replace Eq. 4 with a biexponential.",
             fontsize=6.8, color=st.INK_MUTED, ha="left", va="top",
             linespacing=1.6)

    df = pd.DataFrame(rows)
    (ROOT / "results" / "tables").mkdir(parents=True, exist_ok=True)
    df.to_csv(ROOT / "results" / "tables" / "fig01_values.csv", index=False)
    return fig, df


def main() -> int:
    fig, df = build()
    paths = st.save(fig, "fig01_growth_and_strategies")
    print(df.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
