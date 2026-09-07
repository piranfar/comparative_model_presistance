"""
Shared figure style: one place that decides how every figure looks.

Colour assignment follows the validated three-slot categorical palette, which
clears the all-pairs colour-vision-deficiency and normal-vision separation gates
in light mode. The aqua slot sits below 3:1 contrast against the chart surface,
so every series carries a direct label as well as a legend entry and identity is
never conveyed by colour alone.

Conventions used throughout:
  * species identity is a colour, fixed for the whole figure set;
  * a curve drawn from the paper's printed equation is dashed and annotated;
  * a curve drawn from a corrected equation is solid;
  * y axes are log10 CFU/mL, because time-kill data is homoscedastic in log
    space and a linear count axis hides everything below the first log;
  * limits of detection are drawn as a labelled horizontal band, never omitted;
  * no figure uses two y scales.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIGDIR = ROOT / "results" / "figures"

# AAC accepts 300-600 dpi and names 600 as the ceiling.
SUBMISSION_DPI = 600

# ------------------------------------------------------------------ tokens ---
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

# categorical slots 1-3 of the validated palette
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"

# status colours, reserved: used only to mark a defect, never as a series
CRITICAL = "#d03b3b"
WARNING = "#fab219"

SPECIES_COLOR = {"Mtb": BLUE, "S. aureus": ORANGE}
SPECIES_LABEL = {"Mtb": "M. tuberculosis", "S. aureus": "S. aureus"}

COMPARTMENT_COLOR = {"S": BLUE, "P": AQUA, "total": INK}

STRATEGY_COLOR = {"resistance": BLUE, "tolerance": ORANGE, "persistence": AQUA}


def apply() -> None:
    """Install the rcParams. Call once at the top of every figure script."""
    mpl.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "savefig.dpi": 300,
        "figure.dpi": 110,
        "font.family": "sans-serif",
        # AAC requires Arial, Helvetica or Times New Roman in figures, so Arial
        # leads and the others are only fallbacks for machines without it.
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8.5,
        "axes.titlesize": 9.5,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.labelsize": 8.5,
        "axes.labelcolor": INK_SECONDARY,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "axes.grid.axis": "both",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "grid.alpha": 1.0,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.frameon": False,
        "legend.fontsize": 7.5,
        "legend.handlelength": 1.8,
        "lines.linewidth": 1.9,
        "lines.markersize": 5.5,
        "lines.solid_capstyle": "round",
        "text.color": INK,
        "figure.constrained_layout.use": True,
    })


def panel_tag(ax, letter: str) -> None:
    """Panel letter in the top-left corner, outside the data area."""
    ax.text(-0.085, 1.06, letter, transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="bottom", ha="left", color=INK)


def lod_band(ax, lod_log10: float, label: str = "limit of detection",
             xpos: float = 0.985) -> None:
    """Draw the limit of detection as a labelled band, not a bare line."""
    lo, hi = ax.get_ylim()
    ax.axhspan(lo, lod_log10, color=INK_MUTED, alpha=0.10, lw=0, zorder=0)
    ax.axhline(lod_log10, color=INK_MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.text(xpos, lod_log10, f" {label} ", transform=ax.get_yaxis_transform(),
            ha="right", va="bottom", fontsize=6.8, color=INK_MUTED)
    ax.set_ylim(lo, hi)


def direct_label(ax, x, y, text, color, dx=4, dy=0, ha="left", va="center",
                 weight="semibold", fontsize=7.6):
    """Label a series at its end, so identity does not rest on colour alone."""
    return ax.annotate(text, xy=(x, y), xytext=(dx, dy),
                       textcoords="offset points", ha=ha, va=va,
                       fontsize=fontsize, fontweight=weight, color=color,
                       zorder=6)


def direct_labels_decollided(ax, items, min_gap_frac: float = 0.055):
    """Place several end-of-series labels without letting them overlap.

    `items` is a sequence of (x, y, text, color). Labels are sorted by y and
    pushed apart vertically by at least `min_gap_frac` of the axis height, so a
    figure never ships with two identity labels on top of each other.
    """
    lo, hi = ax.get_ylim()
    span = hi - lo
    gap = min_gap_frac * span
    order = sorted(items, key=lambda it: it[1])
    placed = []
    for x, y, text, color in order:
        y_new = y
        if placed and y_new - placed[-1] < gap:
            y_new = placed[-1] + gap
        placed.append(y_new)
        if abs(y_new - y) > 1e-12:
            ax.plot([x, x], [y, y_new], color=color, lw=0.7, alpha=0.55,
                    zorder=5, clip_on=False)
        direct_label(ax, x, y_new, text, color)
    return placed


def note(ax, text: str, y: float = -0.28, fontsize: float = 6.9) -> None:
    """A short caption note under a panel, for provenance or a caveat."""
    ax.text(0.0, y, text, transform=ax.transAxes, fontsize=fontsize,
            color=INK_MUTED, va="top", ha="left", wrap=True)


def synthetic_stamp(fig, text: str = "SYNTHETIC DATA - no experimental "
                                     "dataset exists in this project") -> None:
    """An unmissable stamp for any figure built on synthetic data."""
    fig.text(0.995, 0.005, text, ha="right", va="bottom", fontsize=7.0,
             color=CRITICAL, fontweight="bold")


def save(fig, stem: str) -> list[Path]:
    """PNG to read, PDF to typeset, TIFF to submit. Returns the paths.

    AAC takes PDF at initial submission but requires TIFF or EPS at revision, at
    300-600 dpi, in bitmap, grayscale or RGB. Matplotlib writes RGBA, which is not
    on that list, so the TIFF is flattened onto the surface colour and converted
    to RGB rather than handed over with an alpha channel. Writing it now means the
    revision package needs no second pass over the figures.
    """
    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = []
    for ext in ("png", "pdf"):
        path = FIGDIR / f"{stem}.{ext}"
        fig.savefig(path, bbox_inches="tight")
        out.append(path)

    w, h = fig.get_size_inches()
    if w > 7.0 or h > 9.0:
        print(f"   ! {stem} is {w:.1f} x {h:.1f} in; AAC recommends 7 x 9 or less")

    tif = FIGDIR / f"{stem}.tif"
    try:
        from PIL import Image
        png = FIGDIR / f"{stem}.png"
        im = Image.open(png)
        if im.mode in ("RGBA", "LA", "P"):
            flat = Image.new("RGB", im.size, SURFACE)
            im = im.convert("RGBA")
            flat.paste(im, mask=im.split()[-1])
            im = flat
        else:
            im = im.convert("RGB")
        im.save(tif, format="TIFF", compression="tiff_lzw",
                dpi=(SUBMISSION_DPI, SUBMISSION_DPI))
        out.append(tif)
    except ImportError:
        print(f"   ! Pillow not installed; {tif.name} not written")
    plt.close(fig)
    return out
