"""
Assemble everything the journal receives into one folder, correctly named.

Run:  python -m src.build_submission_package

WHY. The submission has lived as eight files scattered through manuscript/ under
names that describe how they were built rather than what they are:
MANUSCRIPT.md is the manuscript of a paper that is no longer about rates
versus durations, SUBMISSION_MAIN.md and SUBMISSION_SUPPLEMENT.md are what gets
uploaded, PAPER_COMPLETE.md is a reading aid, and nothing says which is which to
anyone who did not build them. Uploading the wrong one is a real risk and the
names invite it.

This copies the finished artefacts into submission/ under names a stranger can
read, numbered in the order the journal asks for them, with the figures at
submission resolution in their own folder. Nothing here is authored: every file
is a copy of something the pipeline generated, so the folder can be deleted and
rebuilt at any time and never drifts.

Writes: submission/
"""
from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "manuscript"
FIG = ROOT / "results" / "figures"
OUT = ROOT / "submission"

# source -> name in the package. The numbers are the order a submission form
# asks for them, so the folder reads as the checklist it is.
DOCS = [
    (M / "COVER_LETTER.md", "01_cover_letter.md"),
    (M / "SUBMISSION_MAIN.md", "02_manuscript.md"),
    (M / "SUBMISSION_SUPPLEMENT.md", "03_supplementary_material.md"),
    (M / "PREFERRED_REVIEWERS.md", "04_preferred_reviewers.md"),
    (M / "REVIEW_COPY.pdf", "reading_copy.pdf"),
    (M / "REVIEW_COPY.html", "reading_copy.html"),
]

# Figure number -> the script's output stem. Article figures first, then
# supplemental, each named for what it shows rather than for the script.
FIGURES = [
    ("figure_1_headroom_bounds_the_endpoint", "fig1_dynamic_range"),
    ("figure_2_one_protocol_six_laboratories", "fig2_rate_vs_duration"),
    ("figure_3_a_late_endpoint_hides_the_dose", "fig3_endpoint_collapse"),
    ("figure_S1_survival_behind_figure_2", "figS1_survival_and_cox"),
    ("figure_S2_resistance_and_tolerance_axes", "fig4_independence"),
]
FIG_EXT = ("png", "pdf", "tif")

README = """# Submission package

Built by `python -m src.build_submission_package` on {today}. Every file here is
a copy of something the pipeline generated; nothing in this folder is edited by
hand. Delete it and rebuild it rather than correcting a file inside it.

## What to upload

| File | What it is |
|---|---|
| `01_cover_letter.md` | Cover letter. **Fill in the date and the preprint line before sending.** |
| `02_manuscript.md` | The article. This is the file to upload as the manuscript. |
| `03_supplementary_material.md` | The supplemental file, uploaded separately. The journal takes it only at first submission. |
| `04_preferred_reviewers.md` | Three names with affiliations and verified emails, for the submission form. Not uploaded as a file. |
| `figures/` | Every figure at 600 dpi, as PNG, PDF and TIFF. |

## Not for upload

| File | What it is |
|---|---|
| `reading_copy.pdf` | Article and supplement in one document, figures placed at their legends, blocks numbered for marking up. For reading and for sending to colleagues. |
| `reading_copy.html` | The same, in a browser. |

## Figures

{figure_table}

## State of the manuscript at this build

{state}

## Still to do before this can be sent

These are the items no build can close.

1. **Methods for the prospective experiment.** Strain source, medium, MIC value
   and the method used to determine it, incubation, the washing and recovery
   step, and the number of independent runs. The plate readings are in
   `results/tables/exp38_experiment_readings.csv`; the protocol behind them is
   not written down anywhere.
2. **The repository name.** The code is at a URL that misspells "persistence",
   and that URL is the permanent pointer in the data availability statement.
3. **An archived DOI** for the code and for the prospective experiment's raw
   readings, plus the commit identifier the manuscript leaves as a placeholder.
4. **The date and the preprint line** in the cover letter.
"""


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "figures").mkdir(parents=True)

    missing, copied = [], []
    for src, name in DOCS:
        if not src.exists():
            missing.append(src.name)
            continue
        shutil.copy2(src, OUT / name)
        copied.append(name)

    fig_rows = []
    for name, stem in FIGURES:
        got = []
        for ext in FIG_EXT:
            p = FIG / f"{stem}.{ext}"
            if p.exists():
                shutil.copy2(p, OUT / "figures" / f"{name}.{ext}")
                got.append(ext.upper())
        if got:
            fig_rows.append(f"| `{name}` | {', '.join(got)} | from `{stem}` |")
        else:
            missing.append(f"{stem} (no image found)")

    # The audit's own last word, read rather than remembered.
    state_lines = []
    audit = ROOT / "results" / "receipts" / "manuscript_audit.json"
    if audit.exists():
        import json
        a = json.loads(audit.read_text(encoding="utf-8"))
        counts = a.get("counts") or a.get("summary") or {}
        if counts:
            state_lines.append(f"- Manuscript audit: {counts}")
    main_md = M / "SUBMISSION_MAIN.md"
    supp_md = M / "SUBMISSION_SUPPLEMENT.md"
    for label, p in (("Article", main_md), ("Supplement", supp_md)):
        if p.exists():
            state_lines.append(
                f"- {label}: {len(p.read_text(encoding='utf-8').split()):,} words")
    state = "\n".join(state_lines) or "- (no build state found)"

    (OUT / "README.md").write_text(
        README.format(today=date.today().isoformat(),
                      figure_table="\n".join(
                          ["| File | Formats | Built from |", "|---|---|---|"]
                          + fig_rows),
                      state=state),
        encoding="utf-8")

    print(f"wrote {OUT.relative_to(ROOT)}/")
    for n in copied:
        print(f"   {n}")
    print(f"   figures/  {len(fig_rows)} figures x {len(FIG_EXT)} formats")
    if missing:
        print(f"   ! MISSING: {missing}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
