# Antibiotic tolerance is assigned from the starting inoculum wherever killing reaches the assay floor

Every clinical microbiologist knows a culture taken after antibiotics have
started is not evidence of sterility. The field's answer was to stop asking
whether a culture went negative and to ask how far it fell — a fraction of the
starting population, so that the starting population could not matter.

This is a reanalysis of five published deposits showing that the fraction stops
being a fraction once the population reaches the assay floor, and becomes a
reading of the starting density instead.

In 217 clinical *M. tuberculosis* isolates carrying their authors' own tolerance
classification: no isolate lacks the range to demonstrate a 99% kill, 33 of 217
lack it for the 99.99% kill the classification uses, and all 33 are recorded as
having failed. Eighteen isolates ended at the same unmeasurable floor and a
single threshold on their starting density reproduces every tolerance label they
were given.

## Layout

```
manuscript/     the paper: PAPER_COMPLETE.md is the assembled document
docs/           working documents 12 to 18
src/            the analysis
results/        every table, figure and receipt it produces
data/           the deposits, shared with version one
version_one/    the first paper, complete and frozen
```

Two papers live here. This one is at the root; the earlier simulation study is
in `version_one/`, self-contained, with its own copy of the modules the two once
shared so that work here cannot retroactively alter what it reported. They share
`data/` and nothing else.

## Reproducing everything

```bash
pip install -r requirements.txt
python run_all.py
```

Thirty-four stages, about five minutes. Each writes a table and a receipt
recording the software versions it actually ran under, then two audit stages
close the run: the first recomputes 145 pinned quantities from the tables they
came from, and the second reads the table legends, the figure legends, Box 1
and the Abstract that the first never sees. Both report anything that
disagrees.

```bash
python -m src.audit_claims
```

That check exists because numbers drift. Several in this project did, and were
caught by it rather than by rereading.

## What each stage does

| stage | question |
|---|---|
| exp22 | What does a published tolerance classification actually track? |
| exp23 | How often does the faster-killed flask disappear later, and why? |
| exp17 | Six laboratories, one protocol: does a rate travel where a duration does not? |
| exp16 | Do MIC and the minimum duration for killing move together in 217 clinical isolates? |
| exp20 | What does the choice of endpoint do to a 32-fold dose range? |
| exp21 | Is the concentration slope the same early and late? |
| exp18 | Do published pharmacodynamic constants transfer to a slow grower? (supplementary) |
| exp19 | What does a nominal concentration actually deliver once the evolved MIC is known? (supplementary) |

`results/README.md` maps every output to the script that writes it and the
script or manuscript section that uses it.

## Data

Five openly licensed deposits, none generated for this study and none chosen
after its result was known. `data/raw/SOURCES.json` records every external
source with its licence and whether its bytes may be redistributed; several are
free to read but not to redistribute, and are registered by URL only.
`src/fetch_external_data.py` retrieves what publishers serve openly.

## Citing this work

If you use the code or the analyses, cite the manuscript; `CITATION.cff` carries
the machine-readable form. If you use any of the deposits, cite their depositors
rather than this repository — none of that data was generated here.

Vahhab Piranfar. *The detection floor bounds what a time-kill assay can report: minimum duration for killing and log-reduction endpoints in five published deposits and a prospective test* ORCID [0000-0003-3653-5739](https://orcid.org/0000-0003-3653-5739).

## Licence

Three kinds of material, licensed separately, with the full terms in `LICENSE`:

| what | where | licence |
|---|---|---|
| code | `src/`, `run_all.py`, `version_one/src/` | MIT |
| manuscripts, figures, tables, results | `manuscript/`, `docs/`, `results/` | CC BY 4.0 |
| third-party data | `data/` | each depositor's own licence |

CC BY 4.0 rather than a NonCommercial or NoDerivatives variant, deliberately: a
paper arguing that published tolerance calls should be recomputable against their
own assay floor cannot licence its own material in a way that stops anyone doing
it.

The five deposits reanalysed here are all CC BY 4.0 and are attributed to their
depositors in the manuscript and in `data/raw/SOURCES.json`. Third-party material
that may **not** be redistributed — CC BY-NC-ND, subscription, or carrying no
open licence — is excluded from this repository by `.gitignore`, with its
provenance and fetch route kept so the work stays reproducible by anyone who
obtains it from the original deposit. `SOURCES.json` marks each such entry
`"redistributable": false`.
