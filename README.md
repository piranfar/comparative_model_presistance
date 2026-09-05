# Antibiotic tolerance endpoints measure the starting inoculum, not the kill rate

A reanalysis of four published deposits, asking what happens to the two ways
antibiotic killing is summarised — as a rate, and as a duration — when the same
protocol is run in six different laboratories.

The finding is an asymmetry. Every laboratory produces a kill rate. Half of them
produce no clearance time at all, on the same flasks, and which half is decided
by where their cultures started rather than by how fast the drug killed.

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

Fourteen stages, about forty seconds. Each writes a table and a receipt
recording the software versions it actually ran under, then the last stage
recomputes every quantity the manuscript quotes from the table it came from and
reports any that disagree.

```bash
python -m src.audit_claims
```

That check exists because numbers drift. Several in this project did, and were
caught by it rather than by rereading.

## What each stage does

| stage | question |
|---|---|
| exp16 | Do MIC and the minimum duration for killing move together in 217 clinical isolates? |
| exp17 | Six laboratories, one protocol: does a rate travel where a duration does not? |
| exp18 | Do published pharmacodynamic constants transfer to a slow grower? |
| exp19 | What does a nominal concentration actually deliver once the evolved MIC is known? |
| exp20 | What does the choice of endpoint do to a 32-fold dose range? |
| exp21 | Is the concentration slope the same early and late? |

`results/README.md` maps every output to the script that writes it and the
script or manuscript section that uses it.

## Data

Four openly licensed deposits, none generated for this study and none chosen
after its result was known. `data/raw/SOURCES.json` records every external
source with its licence and whether its bytes may be redistributed; several are
free to read but not to redistribute, and are registered by URL only.
`src/fetch_external_data.py` retrieves what publishers serve openly.

## Licence

Code under the terms in `LICENSE`. Every reanalysed deposit is CC BY 4.0 or CC0
and is cited in the manuscript and in `data/raw/SOURCES.json`.
