"""
Model fitting, model comparison and identifiability, on synthetic data.

Run:  python -m src.experiments.exp02_fit_and_identifiability   (first)
      python -m src.figures.fig03_model_fitting

No experimental dataset is named in the manuscript and none exists in this
project, so the data shown here is SYNTHETIC, drawn from the state-structured
model with known ground truth and stamped as such on the figure itself.

What the panels establish is about the estimator and the model structure, which
is exactly what synthetic data can establish:
  fits       both models track the data closely and both reach high R-squared,
             so that statistic cannot distinguish them;
  residuals  the residual pattern and AICc can;
  profile    the transition time of the closed-form law is not identifiable at
             these designs: its profile is flat and the 95% interval runs to the
             edge of the searched range.

Three modules are emitted. The preprint carries all three rows as one figure.
The journal version needs model comparison and identifiability as separate
results with their own figure numbers, so the same drawing code emits those two
subsets as well. Splitting the figure rather than duplicating the plotting means
the three files cannot disagree with each other.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..models.parameters import LOD_CFU_ML
from . import style as st

ROOT = st.ROOT
NPZ = REPO / "data" / "processed" / "synthetic_fits.npz"
DIAG = ROOT / "results" / "tables" / "fit_diagnostics.csv"

PRINTED_NAME = "Eq. 4 as printed (4 rate parameters + N0)"
BIEXP_NAME = "biexponential (3 rate parameters + N0)"

PANELS = [("Mtb", "dense (14-point, 240 h)"),
          ("S. aureus", "dense (16-point, 48 h)")]

ROW_FITS, ROW_RESID, ROW_PROFILE = "fits", "residuals", "profile"
ALL_ROWS = (ROW_FITS, ROW_RESID, ROW_PROFILE)
HEIGHT = {ROW_FITS: 1.25, ROW_RESID: 0.60, ROW_PROFILE: 1.05}

TITLE = {
    ALL_ROWS: ("Model fitting: R-squared cannot separate the two models; "
               "residuals, AICc and profile likelihood can"),
    (ROW_FITS, ROW_RESID): ("Model comparison: a high R-squared is compatible "
                            "with both models; AICc and the residuals are not"),
    (ROW_PROFILE,): ("Practical identifiability: the closed-form transition "
                     "time is not determined by data of this density"),
}
FOOTNOTE = {
    ROW_PROFILE: ("Shaded band is the 95% likelihood interval. A band reaching "
                  "the edge of the searched\nrange means the data do not "
                  "determine that parameter."),
    ROW_RESID: ("R-squared, annotated above, exceeds 0.9 for both models while "
                "AICc separates them:\ngoodness of fit alone does not decide "
                "between candidate killing models."),
}


def _fits(ax, t, y, cens, tf, fit_p, fit_b, short, design, r2p, r2b, ap, ab):
    lod_log10 = np.log10(LOD_CFU_ML)
    ax.plot(tf, fit_p, color=st.CRITICAL, ls=(0, (5, 2)), lw=1.9,
            label="closed-form biphasic law")
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
            f"closed form:      $R^2$ {r2p:.3f}   AICc {ap:6.1f}\n"
            f"biexponential:   $R^2$ {r2b:.3f}   AICc {ab:6.1f}\n"
            f"$\\Delta$AICc = {ap - ab:.1f} in favour of biexponential",
            transform=ax.transAxes, ha="right", va="top", fontsize=6.4,
            color=st.INK_SECONDARY, linespacing=1.5)


def _residuals(axr, t, y, tf, fit_p, fit_b, zp, zb, col, xlim):
    pred_p = np.interp(t, tf, fit_p)
    pred_b = np.interp(t, tf, fit_b)
    axr.axhline(0, color=st.AXIS, lw=0.9)
    axr.plot(t, pred_p - y, "s", color=st.CRITICAL, ms=4.2,
             mec=st.SURFACE, mew=0.7, label="closed-form biphasic law")
    axr.plot(t, pred_b - y, "o", color=st.AQUA, ms=4.2, mec=st.SURFACE,
             mew=0.7, label="biexponential")
    axr.set_ylabel("residual\n(log$_{10}$)")
    axr.set_xlabel("time on antibiotic (h)", labelpad=1)
    lim = max(0.4, float(np.abs(np.concatenate(
        [pred_p - y, pred_b - y])).max()) * 1.35)
    axr.set_ylim(-lim, lim)
    if xlim is not None:
        axr.set_xlim(*xlim)
    axr.set_title(f"residuals   runs-test z: closed form {zp:+.2f}, "
                  f"biexponential {zb:+.2f}", fontsize=7.6)
    if col == 0:
        axr.legend(loc="lower right", fontsize=6.3, ncols=2,
                   columnspacing=0.8, handletextpad=0.3)


def _profile(axp, z, key):
    for model, pname, color, label in [
        (PRINTED_NAME, "t_c", st.CRITICAL, "$t_c$, closed-form law"),
        (BIEXP_NAME, "k_slow", st.AQUA, "$k_{slow}$, biexponential"),
    ]:
        g = z[f"prof_grid|{key}|{model}|{pname}"]
        s = z[f"prof_sse|{key}|{model}|{pname}"]
        th = float(z[f"prof_thresh|{key}|{model}|{pname}"][0])
        xnorm = (g - g.min()) / (g.max() - g.min())
        # The stored curve is the profiled negative log-likelihood. It is
        # plotted as 2*(profile - minimum), the likelihood-ratio statistic,
        # so the horizontal line is the chi-square(1) 95% quantile itself.
        axp.plot(xnorm, 2.0 * (s - s.min()), color=color, lw=1.9, label=label)
        axp.axhline(2.0 * (th - s.min()), color=color, lw=0.9, ls=(0, (2, 2)),
                    alpha=0.85)
        inside = xnorm[s <= th]
        if inside.size:
            axp.axvspan(inside.min(), inside.max(), color=color,
                        alpha=0.11, lw=0)
    axp.set_xlabel("parameter value, as a fraction of the searched range")
    axp.set_ylabel("$2(\\ell_{max}-\\ell)$")
    axp.set_title("profile likelihood", fontsize=8.8)
    axp.legend(loc="upper center", fontsize=6.5, ncols=1)
    axp.set_xlim(0, 1)
    axp.set_ylim(bottom=0.0)


def build(rows: tuple[str, ...] = ALL_ROWS):
    """Draw the requested panel rows. `rows` is a subset of ALL_ROWS, in order."""
    if not NPZ.exists():
        raise SystemExit(
            "run  python -m src.experiments.exp02_fit_and_identifiability  first")
    st.apply()
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams["figure.constrained_layout.use"] = False

    z = np.load(NPZ)
    diag = pd.read_csv(DIAG)

    rows = tuple(r for r in ALL_ROWS if r in rows)
    note = FOOTNOTE.get(rows[-1])

    # Margins in inches, not as fractions of the figure. A fraction tuned for
    # the three-row figure leaves no room for the title or the footnote when
    # only one row is drawn, and the panel tags collide with the title.
    top_in, bot_in = 0.62, 1.05 if note else 0.62
    fig_h = top_in + bot_in + 2.35 * sum(HEIGHT[r] for r in rows)
    fig = plt.figure(figsize=(7.4, fig_h))
    gs = fig.add_gridspec(len(rows), 2, height_ratios=[HEIGHT[r] for r in rows],
                          left=0.095, right=0.985,
                          top=1.0 - top_in / fig_h, bottom=bot_in / fig_h,
                          hspace=0.42, wspace=0.26)
    axes = {(r, c): fig.add_subplot(gs[i, c])
            for i, r in enumerate(rows) for c in range(2)}

    for col, (short, design) in enumerate(PANELS):
        key = f"{short}|{design}"
        t, y = z[f"t|{key}"], z[f"y|{key}"]
        cens = z[f"cens|{key}"].astype(bool)
        tf = z[f"tfine|{key}"]
        fit_p = z[f"fit|{key}|{PRINTED_NAME}"]
        fit_b = z[f"fit|{key}|{BIEXP_NAME}"]

        d = diag[(diag["species"] == short) & (diag["design"] == design)]
        get = lambda m, c: float(d[d["model"] == m][c].iloc[0])

        xlim = None
        if ROW_FITS in rows:
            ax = axes[(ROW_FITS, col)]
            _fits(ax, t, y, cens, tf, fit_p, fit_b, short, design,
                  get(PRINTED_NAME, "r_squared"), get(BIEXP_NAME, "r_squared"),
                  get(PRINTED_NAME, "aicc"), get(BIEXP_NAME, "aicc"))
            xlim = ax.get_xlim()
        if ROW_RESID in rows:
            _residuals(axes[(ROW_RESID, col)], t, y, tf, fit_p, fit_b,
                       get(PRINTED_NAME, "runs_test_z"),
                       get(BIEXP_NAME, "runs_test_z"), col, xlim)
        if ROW_PROFILE in rows:
            _profile(axes[(ROW_PROFILE, col)], z, key)

    letters = iter("ABCDEF")
    for r in rows:
        for c in range(2):
            st.panel_tag(axes[(r, c)], next(letters))

    fig.suptitle(TITLE.get(rows, TITLE[ALL_ROWS]), fontsize=10.2,
                 fontweight="semibold", x=0.006, ha="left",
                 y=1.0 - 0.16 / fig_h)
    if note:
        fig.text(0.006, (bot_in - 0.70) / fig_h, note, fontsize=6.8,
                 color=st.INK_MUTED, ha="left", va="top", linespacing=1.6)
    st.synthetic_stamp(fig)
    return fig, diag


def main() -> int:
    paths = []
    for stem, rows in [("fig03_model_fitting", ALL_ROWS),
                       ("bmb_fig04_identifiability", (ROW_PROFILE,)),
                       ("bmb_fig05_model_comparison", (ROW_FITS, ROW_RESID))]:
        fig, diag = build(rows)
        paths += st.save(fig, stem)
    print(diag[["species", "design", "model", "r_squared", "aicc",
                "t_c_fitted_h", "t_c_hit_bound"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3f}"))
    for p in paths:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
