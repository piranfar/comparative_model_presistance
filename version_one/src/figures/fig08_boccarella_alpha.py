"""
Figure 7. The persistence level in Boccarella et al. (2026), estimated from
their own survival data.

Run:  python -m src.experiments.exp04_boccarella_alpha   (first)
      python -m src.figures.fig08_boccarella_alpha

Data reused under CC BY 4.0 from doi:10.6084/m9.figshare.31389142, accompanying
Boccarella G et al., Mol Biol Evol 2026;43(8):msag180,
doi:10.1093/molbev/msag180.

Panel A. The survival model has a hard ceiling: even if every cell entered the
protected state, the modelled surviving fraction after one 5 h pulse cannot
exceed exp(psi_p * tau). In the high-persistence arm at 12.5 ug/mL the observed
survival lies above that ceiling, so no value of alpha reproduces the data.

Panel B. Where alpha can be estimated, it disagrees with the simulated values by
factors of 12 to 16, and it moves fifteen-fold with drug concentration within
the same experimental arm. In the model alpha is a property of the culture set
at pulse onset and does not depend on concentration.

Panel C. Freeing the persister death rate moves alpha over an eighteen-fold
range with no change in log-likelihood. Survival data determines the product
alpha * exp(psi_p * tau), not alpha.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..models import boccarella as bc
from . import style as st

ROOT = st.ROOT
T = ROOT / "results" / "tables"
NPZ = REPO / "data" / "processed" / "exp04_profile.npz"

ARM_COLOR = {"high persistence (25% MHB)": st.BLUE,
             "intermediate (50% MHB, unused in the paper)": st.AQUA,
             "low persistence (80% MHB)": st.ORANGE}
SHORT = {"high persistence (25% MHB)": "high persistence\n25% MHB",
         "intermediate (50% MHB, unused in the paper)": "intermediate\n50% MHB",
         "low persistence (80% MHB)": "low persistence\n80% MHB"}


def build():
    st.apply()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams["figure.constrained_layout.use"] = False

    raw = pd.read_csv(REPO / "data" / "raw" / "boccarella2026" / "survival_S1.csv")
    est = pd.read_csv(T / "exp04_alpha_estimates.csv")
    z = np.load(NPZ)

    fig = plt.figure(figsize=(7.4, 7.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.95], left=0.095,
                          right=0.985, top=0.895, bottom=0.205,
                          hspace=0.62, wspace=0.28)
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    # ------------------------------------------- A: data against the ceiling
    order = [(12.5, 0.25), (12.5, 0.50), (12.5, 0.80), (25.0, 0.25), (25.0, 0.80)]
    labels, xs = [], []
    for i, (c, nut) in enumerate(order):
        g = raw[(raw.AB_conc == c) & (raw.nutrient_conc == nut) & (raw.surv_frac > 0)]
        if g.empty:
            continue
        arm = [k for k in ARM_COLOR if str(nut) in k or
               (nut == 0.25 and "25%" in k) or (nut == 0.5 and "50%" in k) or
               (nut == 0.8 and "80%" in k)][0]
        color = ARM_COLOR[arm]
        jitter = (np.random.default_rng(i).random(len(g)) - 0.5) * 0.26
        ax_a.plot(i + jitter, g.surv_frac, "o", color=color, ms=4.2,
                  mec=st.SURFACE, mew=0.5, alpha=0.85, zorder=4)
        gm = float(np.exp(np.log(g.surv_frac).mean()))
        ax_a.plot([i - 0.28, i + 0.28], [gm, gm], color=st.INK, lw=2.0, zorder=5)
        labels.append(f"{SHORT[arm]}\n{c:g} $\\mu$g/mL")
        xs.append(i)

        ceiling = bc.persister_survival_factor(c)
        ax_a.plot([i - 0.36, i + 0.36], [ceiling] * 2, color=st.CRITICAL,
                  lw=1.8, ls=(0, (4, 2)), zorder=6)
        if nut == 0.25:
            sim = bc.survival(bc.ALPHA_HIGH, c)
        elif nut == 0.80:
            sim = bc.survival(bc.ALPHA_LOW, c)
        else:
            sim = None
        if sim is not None:
            ax_a.plot([i - 0.36, i + 0.36], [float(sim)] * 2, color=st.INK_MUTED,
                      lw=1.6, ls=(0, (1, 2)), zorder=6)

    ax_a.set_yscale("log")
    ax_a.set_xticks(xs)
    ax_a.set_xticklabels(labels, fontsize=6.8)
    ax_a.set_ylabel("surviving fraction after one 5 h pulse")
    ax_a.set_title("A  the observed survival exceeds what the model can produce "
                   "at any persistence level", fontsize=8.8)
    ax_a.set_ylim(2e-9, 6)
    ax_a.grid(axis="x", visible=False)

    from matplotlib.lines import Line2D
    ax_a.legend(handles=[
        Line2D([], [], color=st.CRITICAL, lw=1.8, ls=(0, (4, 2)),
               label="model ceiling: every cell a persister ($\\alpha$ = 1)"),
        Line2D([], [], color=st.INK_MUTED, lw=1.6, ls=(0, (1, 2)),
               label="model at the simulated $\\alpha$ (0.8 or 5$\\times$10$^{-5}$)"),
        Line2D([], [], color=st.INK, lw=2.0, label="observed geometric mean"),
        Line2D([], [], color=st.BLUE, marker="o", ls="none", ms=4.2,
               label="one evolving population"),
    ], loc="lower left", fontsize=6.5, ncols=2, columnspacing=1.0,
        borderpad=0.5)

    over = raw[(raw.AB_conc == 12.5) & (raw.nutrient_conc == 0.25)]
    gm = float(np.exp(np.log(over.surv_frac[over.surv_frac > 0]).mean()))
    ax_a.annotate(f"observed is {gm / bc.persister_survival_factor(12.5):.1f}$\\times$ "
                  "above the ceiling",
                  xy=(0.30, gm), xytext=(0.80, 3.0),
                  fontsize=6.8, color=st.CRITICAL, fontweight="semibold",
                  arrowprops=dict(arrowstyle="-|>", color=st.CRITICAL, lw=1.0))

    # ------------------------------------------------ B: alpha estimates ----
    e = est.dropna(subset=["alpha_simulated_by_authors"]).copy()
    e = e.sort_values(["nutrient_conc", "AB_conc", "time_day"]).reset_index(drop=True)
    xp = np.arange(len(e))
    for i, r in e.iterrows():
        color = ARM_COLOR[r["arm"]]
        lo = r["alpha_ci_low"] if r["alpha_ci_low"] == r["alpha_ci_low"] else r["alpha_hat"]
        hi = r["alpha_ci_high"] if r["alpha_ci_high"] == r["alpha_ci_high"] else r["alpha_hat"]
        ax_b.plot([i, i], [lo, hi], color=color, lw=1.6, alpha=0.75, zorder=3)
        marker = "^" if r["alpha_hits_upper_bound"] else "o"
        ax_b.plot([i], [r["alpha_hat"]], marker, color=color, ms=7,
                  mec=st.SURFACE, mew=1.1, zorder=5)
        ax_b.plot([i - 0.3, i + 0.3], [r["alpha_simulated_by_authors"]] * 2,
                  color=st.INK, lw=1.8, ls=(0, (3, 2)), zorder=4)
    ax_b.set_yscale("log")
    ax_b.set_xticks(xp)
    ax_b.set_xticklabels([f"{r['AB_conc']:g}\nd{int(r['time_day'])}"
                          for _, r in e.iterrows()], fontsize=6.6)
    ax_b.set_xlabel("concentration ($\\mu$g/mL) and day", labelpad=1)
    ax_b.set_ylabel("persistence level $\\alpha$")
    ax_b.set_title("B  estimated $\\alpha$ against the simulated value",
                   fontsize=8.8)
    ax_b.set_ylim(3e-6, 4)
    ax_b.grid(axis="x", visible=False)
    ax_b.legend(handles=[
        Line2D([], [], color=st.INK, lw=1.8, ls=(0, (3, 2)),
               label="value simulated by the authors"),
        Line2D([], [], color=st.BLUE, marker="^", ls="none", ms=7,
               label="estimate pinned at $\\alpha$ = 1"),
    ], loc="lower left", fontsize=6.3)

    # ------------------------------------------------- C: the ridge ---------
    for key in [k for k in z.files if k.startswith("alpha|")]:
        tag = key.split("|", 1)[1]
        c, nut, _t = tag.split("|")
        nut = float(nut)
        arm = ("high persistence (25% MHB)" if nut == 0.25 else
               "intermediate (50% MHB, unused in the paper)" if nut == 0.5 else
               "low persistence (80% MHB)")
        if nut == 0.25:
            continue                       # pinned at the bound; ridge truncated
        dp = z[f"dp|{tag}"]
        al = z[key]
        ax_c.plot(dp, al, color=ARM_COLOR[arm], lw=2.0,
                  label=f"{SHORT[arm].replace(chr(10), ' ')}, {float(c):g} $\\mu$g/mL")
    ax_c.axvline(bc.D_P, color=st.INK, lw=1.2, ls=(0, (3, 2)))
    ax_c.text(bc.D_P, ax_c.get_ylim()[1], " value assumed\n by the authors",
              fontsize=6.5, color=st.INK, va="top", ha="left")
    ax_c.set_yscale("log")
    ax_c.set_xlabel("persister death rate $d_P$ (1/h), freed", labelpad=1)
    ax_c.set_ylabel("maximum-likelihood $\\alpha$")
    ax_c.set_title("C  every point on these curves fits equally well",
                   fontsize=8.8)
    ax_c.legend(loc="lower right", fontsize=6.3)

    fig.suptitle("The persistence level of Boccarella et al. (2026), estimated "
                 "from their own survival data",
                 fontsize=10.2, fontweight="semibold", x=0.006, ha="left",
                 y=0.982)
    fig.text(0.006, 0.145,
             "Survival data reused under CC BY 4.0 from "
             "doi:10.6084/m9.figshare.31389142. Model re-implemented from the "
             "authors' deposited code.\n"
             "C: across the plotted range of $d_P$ the log-likelihood changes "
             "by less than 10$^{-13}$, because survival depends on $\\alpha$ "
             "and $d_P$ only through their product.\n"
             "The data therefore determines a curve in this plane, not a point, "
             "and $\\alpha$ is not identifiable from survival data alone.",
             fontsize=6.8, color=st.INK_MUTED, ha="left", va="top",
             linespacing=1.55)
    return fig, est


def main() -> int:
    fig, est = build()
    paths = st.save(fig, "fig08_boccarella_alpha")
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
