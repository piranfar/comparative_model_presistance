"""
Figure 5. The mechanistic replacement, and what it produces that Eq. 4 cannot.

Run:  python -m src.figures.fig05_mechanistic_model

Two compartments, replicating and dormant, with a Hill concentration-response on
each:

    dS/dt = r S (1 - (S+P)/K) - kill_S(C) S - k_SP S + k_PS P
    dP/dt =                   - kill_P(C) P + k_SP S - k_PS P

Panels A and B show that biphasic killing emerges from the structure rather than
being imposed by a breakpoint: there is no t_c anywhere in the model, no
discontinuity, and the population reaches the limit of detection in finite time.
Panel C shows what the printed model has no way to express, that killing depends
on concentration. Panel D reports the result that the sensitivity analysis
identified: for the slow grower, time to sterilisation is governed by how fast
dormant cells wake up, because a dormant cell that resumes replication becomes
killable. That is a statement about a drug target, and it is the kind of
statement the printed equation is structurally incapable of making.

Parameters are illustrative, not fitted, and the figure says so. Fitting them to
the hollow-fibre datasets listed in data/manifests/datasets.csv is the next step
and requires no change to the model code.
"""
from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd

from ..models.corrected import hill_kill, log10_drop, mdk, time_to_lod
from ..models.mechanistic import (PD_SPECIES, apparent_transition_time, mic,
                                  net_growth_rate, simulate, total_curve)
from ..models.parameters import LOD_CFU_ML
from . import style as st

ROOT = st.ROOT
C_XMIC = 4.0
N0 = 1.0e6


def build():
    st.apply()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams["figure.constrained_layout.use"] = False

    fig = plt.figure(figsize=(7.4, 6.4))
    gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, top=0.900,
                          bottom=0.175, hspace=0.44, wspace=0.24)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    rows = []
    lod_log10 = np.log10(LOD_CFU_ML)

    # -------------------------------------------- A, B: emergent biphasic ---
    for ax, short in ((ax_a, "Mtb"), (ax_b, "S. aureus")):
        p = PD_SPECIES[short]
        t_end = 600.0 if short == "Mtb" else 60.0
        t = np.linspace(0.0, t_end, 3001)
        out = simulate(p, C_XMIC, t, N0=N0)

        ax.plot(t, np.log10(np.maximum(out["S"], 1e-300)),
                color=st.COMPARTMENT_COLOR["S"], lw=1.7,
                label="replicating S")
        ax.plot(t, np.log10(np.maximum(out["P"], 1e-300)),
                color=st.COMPARTMENT_COLOR["P"], lw=1.7, label="dormant P")
        ax.plot(t, np.log10(np.maximum(out["total"], 1e-300)),
                color=st.COMPARTMENT_COLOR["total"], lw=2.3,
                label="total, what a CFU assay measures")

        curve = total_curve(p, C_XMIC, N0=N0)
        t_lod = time_to_lod(curve, LOD_CFU_ML)
        knee = apparent_transition_time(p, C_XMIC)
        ax.axvline(knee, color=st.INK_MUTED, lw=0.9, ls=(0, (1, 3)))
        ax.text(knee, 6.55, f" knee at {knee:.0f} h\n emerges, not imposed",
                fontsize=6.5, color=st.INK_SECONDARY, ha="left", va="top")
        ax.plot([t_lod], [lod_log10], "o", color=st.CRITICAL, ms=6.5,
                mec=st.SURFACE, mew=1.2, zorder=6, clip_on=False)
        ax.annotate(f"sterilised at {t_lod:.0f} h", xy=(t_lod, lod_log10),
                    xytext=(-8, 26) if short == "Mtb" else (10, 30),
                    textcoords="offset points", fontsize=6.6,
                    color=st.CRITICAL, fontweight="semibold",
                    ha="right" if short == "Mtb" else "left",
                    arrowprops=dict(arrowstyle="-|>", color=st.CRITICAL,
                                    lw=0.9, shrinkA=1, shrinkB=3))

        ax.set_xlim(0, t_end)
        ax.set_ylim(lod_log10 - 1.6, 6.9)
        st.lod_band(ax, lod_log10)
        ax.set_xlabel("time on antibiotic (h)", labelpad=1)
        ax.set_ylabel("log$_{10}$ CFU/mL")
        letter = "A" if short == "Mtb" else "B"
        ax.set_title(f"{letter}  {st.SPECIES_LABEL[short]} at "
                     f"{C_XMIC:g}x MIC", fontsize=8.8)
        ax.legend(loc="lower left", fontsize=6.5)

        rows.append({
            "species": short, "C_xMIC": C_XMIC,
            "knee_h": knee, "time_to_LOD_h": t_lod,
            "MDK99_h": mdk(curve, N0, 99.0),
            "MDK99.99_h": mdk(curve, N0, 99.99),
            "log10_drop_24h": log10_drop(curve, N0, 24.0),
            "persister_fraction_eq": p.persister_fraction_eq,
            "MIC_relative": mic(p),
        })

    # ------------------------------------------ C: concentration-response ---
    conc = np.logspace(-2, 2, 400)
    for short in ("Mtb", "S. aureus"):
        p = PD_SPECIES[short]
        net = np.array([net_growth_rate(p, c, N0=N0) for c in conc])
        color = st.SPECIES_COLOR[short]
        ax_c.plot(conc, net, color=color, lw=2.0,
                  label=st.SPECIES_LABEL[short])
        m = mic(p)
        ax_c.plot([m], [0.0], "o", color=color, ms=6.0, mec=st.SURFACE,
                  mew=1.2, zorder=6)
        ax_c.annotate(f"MIC = {m:.2f}", xy=(m, 0.0),
                      xytext=(0, -20 if short == "Mtb" else 14),
                      textcoords="offset points", ha="center", fontsize=6.6,
                      color=color, fontweight="semibold")
    ax_c.axhline(0, color=st.AXIS, lw=1.0)
    ax_c.set_xscale("log")
    ax_c.set_xlabel("drug concentration (multiples of reference MIC)")
    ax_c.set_ylabel("net population growth rate (1/h)")
    ax_c.set_title("C  concentration enters the model explicitly",
                   fontsize=8.8)
    ax_c.legend(loc="lower left", fontsize=7.0)


    # ------------------------------ D: waking rate governs sterilisation ----
    mults = np.logspace(-1, 1, 25)
    for short in ("Mtb", "S. aureus"):
        p = PD_SPECIES[short]
        color = st.SPECIES_COLOR[short]
        times = []
        for m in mults:
            q = replace(p, k_PS=p.k_PS * m)
            times.append(time_to_lod(total_curve(q, C_XMIC, N0=N0),
                                     LOD_CFU_ML, t_max=4000.0, n=8001,
                                     t_cap=2.0e5))
        times = np.array(times)
        ax_d.plot(mults, times, color=color, lw=2.0, marker="o", ms=3.6,
                  label=st.SPECIES_LABEL[short])
        base = time_to_lod(total_curve(p, C_XMIC, N0=N0), LOD_CFU_ML)
        ax_d.plot([1.0], [base], "o", color=color, ms=7.0, mec=st.SURFACE,
                  mew=1.4, zorder=6)
        for m, tv in zip(mults, times):
            rows.append({"species": short, "k_PS_multiplier": float(m),
                         "time_to_LOD_h": float(tv)})
        st.direct_label(ax_d, mults[-1], times[-1],
                        st.SPECIES_LABEL[short], color, dx=-4, ha="right",
                        dy=10)

    ax_d.set_xscale("log")
    ax_d.set_yscale("log")
    ax_d.axvline(1.0, color=st.INK_MUTED, lw=0.9, ls=(0, (1, 3)))
    ax_d.text(1.0, ax_d.get_ylim()[1], " baseline", fontsize=6.6,
              color=st.INK_MUTED, va="top", ha="left")
    ax_d.set_xlabel("waking rate $k_{P\\rightarrow S}$ (multiple of baseline)")
    ax_d.set_ylabel("time to sterilisation (h)")
    ax_d.set_title("D  waking dormant cells shortens therapy", fontsize=8.8)
    ax_d.legend(loc="upper right", fontsize=7.0)


    fig.suptitle("The mechanistic replacement: biphasic killing emerges and "
                 "sterilisation is finite",
                 fontsize=10.2, fontweight="semibold", x=0.006, ha="left",
                 y=0.984)
    fig.text(0.006, 0.115,
             "C: the printed Eqs. 2-4 contain no concentration term at all, so "
             "they cannot express an MIC, a dose or a regimen.\n"
             "D: a dormant cell that resumes replication becomes killable, so "
             "the resuscitation rate rather than the dormant kill rate sets "
             "treatment duration for the slow grower.",
             fontsize=6.8, color=st.INK_MUTED, ha="left", va="top",
             linespacing=1.6)
    fig.text(0.006, 0.018, "ILLUSTRATIVE PARAMETERS - not fitted to data",
             ha="left", va="bottom", fontsize=7.0, color=st.CRITICAL,
             fontweight="bold")

    df = pd.DataFrame(rows)
    (ROOT / "results" / "tables").mkdir(parents=True, exist_ok=True)
    df.to_csv(ROOT / "results" / "tables" / "fig05_mechanistic.csv",
              index=False)
    return fig, df


def main() -> int:
    fig, df = build()
    paths = st.save(fig, "fig05_mechanistic_model")
    summary = df[df["k_PS_multiplier"].isna()] if "k_PS_multiplier" in df \
        else df
    print(summary.dropna(axis=1, how="all").to_string(
        index=False, float_format=lambda v: f"{v:,.3g}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
