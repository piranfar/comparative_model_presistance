"""
Assemble the Bulletin of Mathematical Biology figure set.

Run:  python -m src.bmb_package

The manuscript numbers its figures in citation order, which is not the order of
the modules that draw them, and two of the five come from one module that the
preprint keeps whole. Copying by hand is how a figure ends up under the wrong
legend, which has already happened once in this project, so the mapping lives
here and the check below fails loudly rather than shipping a wrong pairing.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "results" / "figures"
OUT = ROOT / "submission" / "bmb" / "figures"

# manuscript figure number -> (source stem, what the figure has to show)
FIGURES = {
    "1": ("fig05_mechanistic_model",
          "state-structured trajectories; biphasic decline emerges"),
    "2": ("fig06_mic_mdk_plane",
          "phenotypic signatures across MIC and the two duration endpoints"),
    "3": ("fig04_sensitivity",
          "Sobol indices for time to LOD in both parameter sets"),
    "4": ("bmb_fig04_identifiability",
          "profile likelihood; the closed-form transition time"),
    "5": ("bmb_fig05_model_comparison",
          "fits and residuals; R-squared against AICc"),
}

# Text that must not survive in any shipped figure, with the reason.
FORBIDDEN = {
    "steril": "the endpoint is time to LOD, not sterilisation",
    "4,608": "superseded Sobol design",
    "512 base": "superseded Sobol design",
    "0.873": "superseded first-order index",
    "orthogonal": "the signatures are distinct, not orthogonal",
}


def main() -> int:
    import pymupdf

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*"):
        old.unlink()

    problems = []
    for num, (stem, _) in FIGURES.items():
        src = FIG_DIR / f"{stem}.pdf"
        if not src.exists():
            problems.append(f"Figure {num}: {stem}.pdf has not been generated")
            continue
        page = pymupdf.open(src)[0]
        text = page.get_text().lower()
        for bad, why in FORBIDDEN.items():
            if bad.lower() in text:
                problems.append(f"Figure {num} ({stem}) still says {bad!r}: {why}")
        if page.get_images(full=True):
            problems.append(f"Figure {num} ({stem}) contains a raster image")
        for ext in (".pdf", ".png"):
            f = FIG_DIR / (stem + ext)
            if f.exists():
                shutil.copy2(f, OUT / f"Fig{num}{ext}")

    if problems:
        for p in problems:
            print("  FAIL:", p)
        raise SystemExit(f"{len(problems)} problem(s); nothing is ready to ship")

    print(f"wrote {OUT.relative_to(ROOT)}")
    for num, (stem, shows) in FIGURES.items():
        print(f"  Fig{num}.pdf  <-  {stem:<28} {shows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
