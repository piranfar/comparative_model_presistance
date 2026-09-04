"""
Figure 6. Resistance, tolerance and persistence as three distinct signatures.

Run:  python -m src.figures.fig06_mic_mdk_plane

The preprint states that resistance, tolerance and persistence are three
different survival strategies, then writes all three as one first-order
exponential with a different constant, so nothing in its mathematics tells them
apart. This figure supplies the missing distinction, using the operational
definitions of Brauner, Fridman, Gefen and Balaban (2016), Nat Rev Microbiol
14:320-30, applied to the two-compartment model.

Each mechanism is introduced one at a time into one parameter set:

  resistance   EC50 x16              raises the concentration needed to stop
                                     growth; killing above MIC is unaffected
  tolerance    metabolism /4         replication and both kill rates slowed
                                     together, which leaves the MIC exactly
                                     invariant and multiplies MDK
  persistence  dormancy entry x10    bulk population unaffected; the tail of
                                     the kill curve is not

The result is three orthogonal directions in measurement space:

  variant      MIC fold   MDK99    MDK99.99
  wild type       1.0      29 h      152 h
  resistant      16.0      29 h      152 h     MIC moves, MDK does not
  tolerant        1.0     117 h      257 h     MDK moves, MIC does not
  persistent      1.0      32 h      352 h     only the deep endpoint moves

An isolate can be placed on panels C and D from two standard laboratory
measurements, which is what makes the distinction operational rather than
verbal.
"""
from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd

from ..models.corrected import mdk
from ..models.mechanistic import MTB_PD, mic, net_growth_rate, total_curve
from ..models.parameters import LOD_CFU_ML
from . import style as st

ROOT = st.ROOT
N0 = 1.0e6
EXPOSURE_MULTIPLE = 8.0          # multiples of MIC at which MDK is measured

RESISTANCE_FOLD = 16.0
TOLERANCE_FOLD = 4.0
PERSISTENCE_FOLD = 10.0

# Base parameter set for this figure: the M. tuberculosis set of mechanistic.py
# with a 0.05% dormant fraction, low enough that a ten-fold increase in dormancy
# still leaves MDK99 untouched. That is the regime in which persistence and
# tolerance are distinguishable, and showing it is the point of panel D.
BASE = replace(MTB_PD, k_SP=5.0025e-6)

VARIANT_COLOR = {"wild type": st.INK_SECONDARY, "resistant": st.BLUE,
                 "tolerant": st.ORANGE, "persistent": st.AQUA}
VARIANT_MARKER = {"wild type": "o", "resistant": "s", "tolerant": "^",
                  "persistent": "D"}


def variants() -> dict:
    return {
        "wild type": BASE,
        "resistant": BASE.with_resistance(RESISTANCE_FOLD),
        "tolerant": BASE.with_tolerance(TOLERANCE_FOLD),
        "persistent": BASE.with_persistence(PERSISTENCE_FOLD),
    }


def measure() -> pd.DataFrame:
    """MIC, and MDK measured at a fixed multiple of each strain's own MIC.

    Measuring MDK at the strain's own MIC multiple is what isolates the three
    mechanisms: it removes the trivial consequence that a resistant strain is
    not killed by a dose chosen for a susceptible one, leaving only the question
    of how fast each strain dies once adequately exposed.
    """
    mic_wt = mic(BASE)
    rows = []
    for name, q in variants().items():
        mq = mic(q)
        own = total_curve(q, EXPOSURE_MULTIPLE * mq, N0=N0)
        fixed = total_curve(q, EXPOSURE_MULTIPLE * mic_wt, N0=N0)
        rows.append({
            "variant": name,
            "MIC_fold_vs_wild_type": mq / mic_wt,
            "MDK99_h_at_own_MIC": mdk(own, N0, 99.0),
            "MDK99.99_h_at_own_MIC": mdk(own, N0, 99.99),
            "MDK99_h_at_wild_type_dose": mdk(fixed, N0, 99.0),
            "MDK99.99_h_at_wild_type_dose": mdk(fixed, N0, 99.99),
            "r": q.r, "Emax_S": q.Emax_S, "EC50": q.EC50,
            "dormant_fraction": q.persister_fraction_growing(N0),
        })
    return pd.DataFrame(rows)


def build():
    st.apply()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams["figure.constrained_layout.use"] = False

    df = measure()
    mic_wt = mic(BASE)
    wt = df[df["variant"] == "wild type"].iloc[0]

    fig = plt.figure(figsize=(7.4, 6.6))
    gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, top=0.905,
                          bottom=0.185, hspace=0.42, wspace=0.28)
    ax_a, ax_b = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
    ax_c, ax_d = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])

    # ------------------------------------------ A: concentration-response ---
    conc = np.logspace(-2, 3, 500)
    for name, q in variants().items():
        net = np.array([net_growth_rate(q, c * mic_wt, N0=N0) for c in conc])
        ax_a.plot(conc, net, color=VARIANT_COLOR[name], lw=1.9, label=name)
        m = mic(q) / mic_wt
        ax_a.plot([m], [0.0], VARIANT_MARKER[name], color=VARIANT_COLOR[name],
                  ms=6.0, mec=st.SURFACE, mew=1.1, zorder=6)
    ax_a.axhline(0, color=st.AXIS, lw=1.0)
    ax_a.set_xscale("log")
    ax_a.set_xlabel("concentration (x wild-type MIC)")
    ax_a.set_ylabel("net growth rate (1/h)")
    ax_a.set_title("A  concentration-response; markers are each MIC",
                   fontsize=8.6)
    ax_a.legend(loc="lower left", fontsize=6.5)
    ax_a.annotate("resistance moves\nthe MIC 16-fold",
                  xy=(RESISTANCE_FOLD, 0.0), xytext=(14, -50),
                  textcoords="offset points", ha="left", fontsize=6.5,
                  color=st.BLUE, fontweight="semibold",
                  arrowprops=dict(arrowstyle="-|>", color=st.BLUE, lw=0.9))
    ax_a.annotate("tolerance does not:\nboth sides scale together",
                  xy=(1.0, 0.0), xytext=(-10, -48),
                  textcoords="offset points", ha="right", fontsize=6.5,
                  color=st.ORANGE, fontweight="semibold",
                  arrowprops=dict(arrowstyle="-|>", color=st.ORANGE, lw=0.9))

    # ------------------------------------- B: time-kill at one fixed dose ---
    t = np.linspace(0.0, 500.0, 2001)
    for name, q in variants().items():
        y = np.log10(np.maximum(
            total_curve(q, EXPOSURE_MULTIPLE * mic_wt, N0=N0)(t), 1e-300))
        ax_b.plot(t, y, color=VARIANT_COLOR[name], lw=1.9, label=name)
    ax_b.set_xlim(0, 500)
    ax_b.set_ylim(np.log10(LOD_CFU_ML) - 1.4, 9.3)
    st.lod_band(ax_b, np.log10(LOD_CFU_ML))
    ax_b.set_xlabel("time on antibiotic (h)")
    ax_b.set_ylabel("log$_{10}$ CFU/mL")
    ax_b.set_title(f"B  one fixed dose, {EXPOSURE_MULTIPLE:g}x wild-type MIC",
                   fontsize=8.6)
    ax_b.legend(loc="center right", fontsize=6.5)

    # ------------------------------------------------- C: (MIC, MDK99) ------
    for _, row in df.iterrows():
        name = row["variant"]
        ax_c.plot([row["MIC_fold_vs_wild_type"]], [row["MDK99_h_at_own_MIC"]],
                  VARIANT_MARKER[name], color=VARIANT_COLOR[name], ms=9.5,
                  mec=st.SURFACE, mew=1.3, zorder=6)
        dy = {"wild type": -20, "persistent": 13, "tolerant": 13,
              "resistant": 13}[name]
        ax_c.annotate(name,
                      xy=(row["MIC_fold_vs_wild_type"],
                          row["MDK99_h_at_own_MIC"]),
                      xytext=(0, dy), textcoords="offset points",
                      fontsize=6.9, color=VARIANT_COLOR[name],
                      fontweight="semibold", ha="center")
    ax_c.annotate("", xy=(RESISTANCE_FOLD * 0.72, wt["MDK99_h_at_own_MIC"]),
                  xytext=(1.35, wt["MDK99_h_at_own_MIC"]),
                  arrowprops=dict(arrowstyle="-|>", color=st.BLUE, lw=1.3,
                                  alpha=0.65))
    ax_c.annotate("", xy=(1.0, wt["MDK99_h_at_own_MIC"] * 3.2),
                  xytext=(1.0, wt["MDK99_h_at_own_MIC"] * 1.25),
                  arrowprops=dict(arrowstyle="-|>", color=st.ORANGE, lw=1.3,
                                  alpha=0.65))
    ax_c.text(2.0, wt["MDK99_h_at_own_MIC"] * 0.80, "resistance",
              fontsize=6.7, color=st.BLUE, fontweight="semibold")
    ax_c.text(1.12, wt["MDK99_h_at_own_MIC"] * 2.1, "tolerance",
              fontsize=6.7, color=st.ORANGE, fontweight="semibold")
    ax_c.set_xscale("log")
    ax_c.set_yscale("log")
    ax_c.set_xlim(0.55, 45)
    ax_c.set_ylim(18, 260)
    ax_c.set_xlabel("MIC (fold change vs wild type)")
    ax_c.set_ylabel("MDK$_{99}$ (h)")
    ax_c.set_title("C  resistance and tolerance separate here", fontsize=8.6)

    # ------------------------------------- D: (MDK99, MDK99.99) -------------
    # wild type and resistant land on exactly the same point here, which is
    # the finding: once adequately exposed, a resistant strain dies at the
    # wild-type rate. The resistant marker is drawn as a ring around it.
    for _, row in df.iterrows():
        name = row["variant"]
        x, y = row["MDK99_h_at_own_MIC"], row["MDK99.99_h_at_own_MIC"]
        if name == "resistant":
            ax_d.plot([x], [y], "o", mfc="none", color=VARIANT_COLOR[name],
                      ms=16.0, mew=1.6, zorder=5)
            continue
        ax_d.plot([x], [y], VARIANT_MARKER[name], color=VARIANT_COLOR[name],
                  ms=9.5, mec=st.SURFACE, mew=1.3, zorder=6)
        off = {"wild type": (0, -20), "persistent": (0, 16),
               "tolerant": (0, 16)}[name]
        ax_d.annotate(name, xy=(x, y), xytext=off,
                      textcoords="offset points", fontsize=6.9,
                      color=VARIANT_COLOR[name], fontweight="semibold",
                      ha="center")
    wtx = wt["MDK99_h_at_own_MIC"]
    wty = wt["MDK99.99_h_at_own_MIC"]
    ax_d.annotate("resistant sits exactly on wild type:\n"
                  "adequately exposed it dies at the same rate",
                  xy=(wtx, wty), xytext=(0.97, 0.10),
                  textcoords=ax_d.transAxes,
                  fontsize=6.4, color=st.BLUE, fontweight="semibold",
                  ha="right", va="bottom",
                  arrowprops=dict(arrowstyle="-|>", color=st.BLUE, lw=0.9))
    lo, hi = 22, 400
    ax_d.plot([lo, hi], [lo * wt["MDK99.99_h_at_own_MIC"] / wt["MDK99_h_at_own_MIC"],
                         hi * wt["MDK99.99_h_at_own_MIC"] / wt["MDK99_h_at_own_MIC"]],
              color=st.INK_MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax_d.text(0.97, 0.72, "both endpoints scale together\n(pure tolerance)",
              transform=ax_d.transAxes, fontsize=6.4, color=st.INK_MUTED,
              ha="right", va="top")
    pers = df[df["variant"] == "persistent"].iloc[0]
    ax_d.annotate("persistence lifts the\ndeep endpoint only",
                  xy=(pers["MDK99_h_at_own_MIC"],
                      pers["MDK99.99_h_at_own_MIC"]),
                  xytext=(30, 26), textcoords="offset points", fontsize=6.5,
                  color=st.AQUA, fontweight="semibold", ha="left",
                  arrowprops=dict(arrowstyle="-|>", color=st.AQUA, lw=0.9))
    ax_d.set_xscale("log")
    ax_d.set_yscale("log")
    ax_d.set_xlim(lo, hi)
    ax_d.set_ylim(112, 900)
    ax_d.set_xticks([30, 50, 100, 200, 400])
    ax_d.set_xticklabels(['30', '50', '100', '200', '400'])
    ax_d.set_yticks([150, 250, 400, 700])
    ax_d.set_yticklabels(['150', '250', '400', '700'])
    ax_d.minorticks_off()
    ax_d.set_xlabel("MDK$_{99}$ (h), the bulk population")
    ax_d.set_ylabel("MDK$_{99.99}$ (h), the tail")
    ax_d.set_title("D  tolerance and persistence separate here", fontsize=8.6)

    fig.suptitle("Three strategies, three signatures: what the printed "
                 "equations cannot separate and this model can",
                 fontsize=10.2, fontweight="semibold", x=0.006, ha="left",
                 y=0.982)
    fig.text(0.006, 0.125,
             "One parameter set, one mechanism changed at a time: resistance "
             f"= EC50 x{RESISTANCE_FOLD:g}; tolerance = replication and both "
             f"kill rates /{TOLERANCE_FOLD:g} together, which is what leaves "
             "the MIC exactly invariant;\n"
             f"persistence = dormancy entry x{PERSISTENCE_FOLD:g}. In C and D "
             f"each strain is exposed to {EXPOSURE_MULTIPLE:g}x its own MIC, "
             "removing the trivial effect that a resistant strain survives a "
             "dose chosen for a susceptible one.",
             fontsize=6.8, color=st.INK_MUTED, ha="left", va="top",
             linespacing=1.6)
    fig.text(0.006, 0.018, "ILLUSTRATIVE PARAMETERS - not fitted to data",
             ha="left", va="bottom", fontsize=7.0, color=st.CRITICAL,
             fontweight="bold")

    (ROOT / "results" / "tables").mkdir(parents=True, exist_ok=True)
    df.to_csv(ROOT / "results" / "tables" / "fig06_mic_mdk.csv", index=False)
    return fig, df


def main() -> int:
    fig, df = build()
    paths = st.save(fig, "fig06_mic_mdk_plane")
    print(df[["variant", "MIC_fold_vs_wild_type", "MDK99_h_at_own_MIC",
              "MDK99.99_h_at_own_MIC", "MDK99_h_at_wild_type_dose",
              "dormant_fraction"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3g}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
