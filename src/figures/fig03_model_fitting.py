"""
Figure 3. Model fitting, uncertainty and identifiability.

Run:  python -m src.experiments.exp02_fit_and_identifiability   (first)
      python -m src.figures.fig03_model_fitting

This replaces the original Figure 3, captioned "Experimental data vs. model
fitting". No experimental dataset is named in the manuscript and none exists in
this project, so the data shown here is SYNTHETIC, drawn from the mechanistic
model with known ground truth and stamped as such on the figure itself.

What the panels establish is about the estimator and the model structure, which
is exactly what synthetic data can establish:
  A, B  both models track the data closely and both reach high R-squared, so
        the statistic the paper reports cannot distinguish them;
  C, D  the residuals and AICc can;
  E, F  the transition time of the printed equation is not identifiable: its
        profile is flat and the 95% interval runs to the edge of the searched
        range, so the fitted t_c is set by the bound rather than by the data.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..models.parameters import LOD_CFU_ML
from . import style as st

ROOT = st.ROOT
NPZ = ROOT / "data" / "processed" / "synthetic_fits.npz"
DIAG = ROOT / "results" / "tables" / "fit_diagnostics.csv"

PRINTED_NAME = "Eq. 4 as printed (4 rate parameters + N0)"
BIEXP_NAME = "biexponential (3 rate parameters + N0)"

PANELS = [("Mtb", "dense (14-point, 240 h)"),
          ("S. aureus", "dense (16-point, 48 h)")]


def build():
    if not NPZ.exists():
        raise SystemExit(
            "run  python -m src.experiments.exp02_fit_and_identifiability  first")
    st.apply()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams["figure.constrained_layout.use"] = False

    z = np.load(NPZ)
    diag = pd.read_csv(DIAG)

    fig = plt.figure(figsize=(7.4, 7.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.25, 0.60, 1.05],
                          left=0.095, right=0.985, top=0.905, bottom=0.115,
                          hspace=0.42, wspace=0.26)
    axes = {(r, c): fig.add_subplot(gs[r, c]) for r in range(3) for c in range(2)}
    lod_log10 = np.log10(LOD_CFU_ML)

    for col, (short, design) in enumerate(PANELS):
        key = f"{short}|{design}"
        t, y = z[f"t|{key}"], z[f"y|{key}"]
        cens = z[f"cens|{key}"].astype(bool)
        tf = z[f"tfine|{key}"]
        fit_p = z[f"fit|{key}|{PRINTED_NAME}"]
        fit_b = z[f"fit|{key}|{BIEXP_NAME}"]

        d = diag[(diag["species"] == short) & (diag["design"] == design)]
        get = lambda m, c: float(d[d["model"] == m][c].iloc[0])
        r2p, r2b = get(PRINTED_NAME, "r_squared"), get(BIEXP_NAME, "r_squared")
        ap, ab = get(PRINTED_NAME, "aicc"), get(BIEXP_NAME, "aicc")

        # ------------------------------------------------------ fits -------
        ax = axes[(0, col)]
        ax.plot(tf, fit_p, color=st.CRITICAL, ls=(0, (5, 2)), lw=1.9,
                label="Eq. 4 as printed")
        ax.plot(tf, fit_b, color=st.AQUA, lw=1.9, label="biexponential")
        ax.plot(t[~cens], y[~cens], "o", color=st.INK, ms=4.8, mec=st.SURFACE,
                mew=0.9, zorder=5, label="synthetic observation")
        if cens.any():
            ax.plot(t[cens], y[cens], "v", color=st.SURFACE, ms=5.8,
                    mec=st.INK, mew=1.1, zorder=5, label="below LOD")
        ax.set_ylim(lod_log10 - 1.3, 7.0)
        st.lod_band(ax, lod_log10)
        ax.set_title(f"{st.SPECIES_LABEL[short]}, {design}", fontsize=8.8)
        ax.set_ylabel("log$_{10}$ CFU/mL")
        ax.set_xlabel("time on antibiotic (h)", labelpad=1)
        ax.legend(loc="lower left", fontsize=6.4, ncols=2,
                  columnspacing=0.9, handletextpad=0.4)
        ax.text(0.975, 0.955,
                f"as printed:      $R^2$ {r2p:.3f}   AICc {ap:6.1f}\n"
                f"biexponential:  $R^2$ {r2b:.3f}   AICc {ab:6.1f}\n"
                f"$\\Delta$AICc = {ap - ab:.1f} in favour of biexponential",
                transform=ax.transAxes, ha="right", va="top", fontsize=6.4,
                color=st.INK_SECONDARY, linespacing=1.5)

        # -------------------------------------------------- residuals ------
        axr = axes[(1, col)]
        pred_p = np.interp(t, tf, fit_p)
        pred_b = np.interp(t, tf, fit_b)
        axr.axhline(0, color=st.AXIS, lw=0.9)
        axr.plot(t, pred_p - y, "s", color=st.CRITICAL, ms=4.2,
                 mec=st.SURFACE, mew=0.7, label="Eq. 4 as printed")
        axr.plot(t, pred_b - y, "o", color=st.AQUA, ms=4.2, mec=st.SURFACE,
                 mew=0.7, label="biexponential")
        axr.set_ylabel("residual\n(log$_{10}$)")
        axr.set_xlabel("time on antibiotic (h)", labelpad=1)
        lim = max(0.4, float(np.abs(np.concatenate(
            [pred_p - y, pred_b - y])).max()) * 1.35)
        axr.set_ylim(-lim, lim)
        axr.set_xlim(*ax.get_xlim())
        zp = get(PRINTED_NAME, "runs_test_z")
        zb = get(BIEXP_NAME, "runs_test_z")
        axr.set_title(f"residuals   runs-test z: printed {zp:+.2f}, "
                      f"biexponential {zb:+.2f}", fontsize=7.6)
        if col == 0:
            axr.legend(loc="lower right", fontsize=6.3, ncols=2,
                       columnspacing=0.8, handletextpad=0.3)

        # ------------------------------------------ profile likelihood ------
        axp = axes[(2, col)]
        for model, pname, color, label in [
            (PRINTED_NAME, "t_c", st.CRITICAL, "$t_c$, Eq. 4 as printed"),
            (BIEXP_NAME, "k_slow", st.AQUA, "$k_{slow}$, biexponential"),
        ]:
            g = z[f"prof_grid|{key}|{model}|{pname}"]
            s = z[f"prof_sse|{key}|{model}|{pname}"]
            th = float(z[f"prof_thresh|{key}|{model}|{pname}"][0])
            xnorm = (g - g.min()) / (g.max() - g.min())
            axp.plot(xnorm, s / s.min(), color=color, lw=1.9, label=label)
            axp.axhline(th / s.min(), color=color, lw=0.9, ls=(0, (2, 2)),
                        alpha=0.85)
            inside = xnorm[s <= th]
            if inside.size:
                axp.axvspan(inside.min(), inside.max(), color=color,
                            alpha=0.11, lw=0)
        axp.set_xlabel("parameter value, as a fraction of the searched range")
        axp.set_ylabel("SSE / SSE$_{min}$")
        axp.set_title("profile likelihood", fontsize=8.8)
        axp.legend(loc="upper center", fontsize=6.5, ncols=1)
        axp.set_xlim(0, 1)
        axp.set_ylim(0.98, None)

    for (rc, letter) in zip([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
                            "ABCDEF"):
        st.panel_tag(axes[rc], letter)

    fig.suptitle("Model fitting: R-squared cannot separate the two models; "
                 "residuals, AICc and profile likelihood can",
                 fontsize=10.2, fontweight="semibold", x=0.006, ha="left",
                 y=0.982)
    fig.text(0.006, 0.070,
             "Shaded band in E and F is the 95% likelihood interval. A band "
             "that reaches the edge of the searched range means the\n"
             "parameter is not determined by the data: the printed equation's "
             "$t_c$ is unidentifiable in all four designs tested, and its\n"
             "fitted value sits on the optimiser bound in three of them.",
             fontsize=6.8, color=st.INK_MUTED, ha="left", va="top",
             linespacing=1.6)
    st.synthetic_stamp(fig)
    return fig, diag


def main() -> int:
    fig, diag = build()
    paths = st.save(fig, "fig03_model_fitting")
    print(diag[["species", "design", "model", "r_squared", "aicc",
                "t_c_fitted_h", "t_c_hit_bound"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3f}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
