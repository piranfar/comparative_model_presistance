# Version one

Everything belonging to the first paper, kept together and frozen.

This directory is a snapshot, not a working copy. It holds its own copy of the
three modules it shares with the later work — `boccarella.py`, `fitting.py` and
`style.py` — so that changes made for the current paper cannot retroactively
alter what version one reported. That duplication is deliberate. A published
result should be reproducible from the code as it stood when the result was
published, not from whatever the shared library has become since.

## What is here

| | |
|---|---|
| `manuscript/` | the bioRxiv preprint, the *Bulletin of Mathematical Biology* version, the shielding manuscript, the editorial review and the corrections log |
| `submission/` | what was actually submitted: the bioRxiv v2 package and the BMB package |
| `docs/` | working documents 01 to 11: the audit and rebuild plan, the study design, reference verification, the novelty landscape, the reproduction of Boccarella et al. |
| `src/` | experiments 01 to 15, figures 01 to 09, and the model, inference and packaging code they use |
| `results/` | 47 tables, 22 figure files and 14 receipts produced by that code |
| `run_all.py` | the pipeline that regenerates all of it |

## Running it

From this directory:

```bash
python run_all.py
```

Two paths differ from the later work and are worth knowing before anything is
moved again. Outputs resolve relative to this directory, so a run writes into
`version_one/results/` and cannot overwrite the current paper's results. Inputs
do not: `data/` stays at the repository root and is shared, because it is 749 MB
and both papers read the same deposits. Scripts that read data therefore resolve
it through `REPO = ROOT.parent` rather than `ROOT`.

## Checking the numbers

```bash
python -m src.audit_claims
```

This recomputes every quantity quoted in the version-one manuscripts from the
table it came from. Twelve of thirteen checks agree. The one that does not is
deliberate and is labelled as such: exp14 and exp15 report the nutrient effect on
different bases, 19-fold from empirical medians and 41-fold from a fitted linear
trend extrapolated to nutrient 0.9, and the manuscript quotes the first. The
check exists to keep that disagreement visible rather than to be silenced.

## What version one claimed, and what happened to it

The first paper is a simulation study: a state-structured pharmacodynamic model,
its sensitivity and its identifiability, examined on synthetic data. The current
paper is not a revision of it. It is an empirical reanalysis of five published
deposits, and it lives at the repository root.

Several claims made here were later corrected, and the corrections are recorded
rather than quietly applied. `manuscript/CORRECTIONS_LOG.md` holds them. The
substantive ones: the reference numbering in the submitted bioRxiv v2 was wrong,
four figures sat under the wrong legends, and the exposure convention was
absolute rather than per-MIC in three places. The current paper's Section 3.4
quantifies what that last error costs, which is why it appears there rather than
being buried here.
