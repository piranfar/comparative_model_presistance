# Submission package

Built by `python -m src.build_submission_package` on 2026-09-09. Every file here is
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

| File | Formats | Built from |
|---|---|---|
| `figure_1_headroom_bounds_the_endpoint` | PNG, PDF, TIF | from `fig1_dynamic_range` |
| `figure_2_one_protocol_six_laboratories` | PNG, PDF, TIF | from `fig2_rate_vs_duration` |
| `figure_3_a_late_endpoint_hides_the_dose` | PNG, PDF, TIF | from `fig3_endpoint_collapse` |
| `figure_S1_survival_behind_figure_2` | PNG, PDF, TIF | from `figS1_survival_and_cox` |
| `figure_S2_resistance_and_tolerance_axes` | PNG, PDF, TIF | from `fig4_independence` |

## State of the manuscript at this build

- Manuscript audit: {'high': 0, 'medium': 1, 'low': 9}
- Article: 15,685 words
- Supplement: 20,440 words

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
