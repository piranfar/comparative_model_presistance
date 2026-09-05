# Reproducing Boccarella et al. (2026)

**Target:** Boccarella G, Ruelens P, Berríos-Caro E, Van den Bergh B, Cool L, Michiels J,
van den Berg P. "Bacterial Persistence Modulates the Speed, Magnitude, and Onset of
Antibiotic Resistance Evolution." *Mol Biol Evol* 2026;43(8):msag180.
[10.1093/molbev/msag180](https://doi.org/10.1093/molbev/msag180). PMID 42483960.

**Deposit:** [10.6084/m9.figshare.31389142](https://doi.org/10.6084/m9.figshare.31389142),
CC BY 4.0. Downloaded 2026-09-03. Raw reads: SRA `PRJNA498891`.

**Status (2026-09-04): both arms reproduce** on the quantity their published figure
actually shows. One narrow residual remains, in a quantity their figure conditions away.
Four gaps found between what is published and what was run. `min_bR` = 2 is now confirmed
by three independent deposited scripts.

---

## 1. Why reproduce before anything else

The scientific question is whether their conclusion depends on a persistence level that
their own data cannot identify (see [`exp04`](../src/experiments/exp04_boccarella_alpha.py)).
Answering it means running their simulation at a different persistence level and comparing.
That comparison is meaningless unless the baseline reproduces what they published, so the
reproduction check gates everything downstream.

Their code is vendored **unmodified** at
[`external/boccarella2026/`](../external/boccarella2026/) and verified byte-identical to
the copy inside their `Data_and_scripts.zip`. Two accommodations, both in
[`src/models/boccarella_runner.py`](../src/models/boccarella_runner.py) and nowhere else:
`mpi4py` is stubbed, since their cluster driver imports it but the simulation function
does not use it; and a seed is set per replicate, which turns out to have no effect for
the reason given in G3 below.

## 2. Four gaps between the published record and the executed code

None of these is evidence of misconduct. Together they mean that **running the deposited
code as deposited does not reproduce the deposited results.**

### G1 · `min_bR`: the driver and the output disagree — this one is decisive

| Source | Value |
|---|---|
| `magnitude_of_evolution_simulations.py` `main()` | `min_bR_values = [bS]`, and `bS = 1.7` |
| `many_treaments_simualtions.py` `main()` | `min_bR_values = [2]` |
| `mutant_frequency_simulations.py` `main()` | `min_bR_values = [2]` |
| `population_size_simulations.py` `main()` | `min_bR_values = [2]` |
| Every row of their deposited `Fig_2_b` and `Fig_6` output | `min_bR = 2` |

**Three of their four deposited simulation scripts hardcode 2.** Only the one that
generates Figures 2 and 3 uses `bS`. Together with the recorded output this makes 2 the
intended value beyond reasonable doubt, and the `[bS]` an artefact in that one file.

`mic_to_br` interpolates the birth rate from 2.0 at MIC 1 down to `min_bR` at MIC 32, so
this parameter decides whether resistance carries a fitness cost. At 1.7 it does; at 2.0
it does not, because the interpolation becomes constant.

The consequence is not subtle. Running their `main()` value at 12.5 µg/mL:

| Arm | Their published median final MIC | With `min_bR` = 1.7 | With `min_bR` = 2.0 |
|---|---|---|---|
| high persistence | 9.21 | **2.00** (100% of runs never evolve) | **8.17** (KS p = 0.43, consistent) |
| low persistence | 18.63 | 11.65 | 15.38 (KS p = 5×10⁻⁵, still low) |

At 1.7 the high-persistence arm shows no resistance evolution at all, in every replicate.
`min_bR = 2.0` is therefore the value the published runs used, and it is recorded only in
the data, never in the manuscript or the driver.

### G2 · `sigma`: the manuscript and the code disagree

| Source | Value |
|---|---|
| Manuscript Table 1 | σ = 0.07 |
| Their `main()` | `sigma_values = [0.7]` |
| Their deposited output | `sigma = 0.7` |

Code and output agree, so 0.7 is what ran and Table 1 is wrong by a factor of ten. This
matters because σ is the spread of the log-normal distribution of mutational effects on
MIC, which is the quantity their small-effect versus large-effect argument rests on.

### G3 · The simulation reseeds itself, so no run is reproducible

Line 66 of `RUN_tau_leaping`, inside the function, is:

```python
np.random.seed()
```

with no argument. It reseeds from OS entropy at the start of every run and discards any
seed the caller sets. **No execution of their simulation can be reproduced, by
construction**, and no external seeding changes that without editing their file.

This also corrects an earlier diagnosis in this document's history. A difference between
two of my batches was attributed to correlated consecutive seeds; the seeds never reached
the generator, and the difference was sampling variation.

### G4 · Three parameters are absent from the paper but fixed in the code

**Corrected 2026-09-04.** An earlier version of this document claimed the Hill coefficient
was "recorded nowhere". That was wrong. The manuscript's Table 1 gives *h* = 2 explicitly,
and their `main()` sets it to 2. The trap is only that the function signature defaults to
3, so anyone calling `RUN_tau_leaping` directly without setting `kappaS` silently gets the
wrong value.

The dilution factor and the tau-leaping step are genuinely absent from both the manuscript
and the supplementary information, which was read in full. But both are fixed in the
deposited code: `main()` sets `dilution_factor = 1`, and `tau_max` is never overridden from
its default of 0.1.

**So there is no unrecoverable parameter.** Every value used by the published runs can be
determined from the deposit, provided the reader takes `min_bR` from the recorded output
rather than from the driver. This makes the residual in §3 harder to explain, not easier.

## 3. Reproduction status

Run: [`src/experiments/exp06_reproduce_check.py`](../src/experiments/exp06_reproduce_check.py).
Compares final-MIC distributions against their 500 deposited simulations per arm at
12.5 µg/mL, by two-sample Kolmogorov–Smirnov. The test is legitimate here, unlike its use
in the preprint this project began with, because both samples are genuine random draws.

**Their Figure 3 script filters the data.** `Fig_3/Fig_3_a-b.R` line 70:

```r
# Keep only those that ended up with MIC > 2
data_density <- data_filtered %>% filter(final_MIC > 2)
```

The published density plot therefore shows final MIC *conditional on resistance having
evolved*. Comparing on the same basis:

| Arm | comparison | n mine | median mine | median theirs | KS p | verdict |
|---|---|---|---|---|---|---|
| high | all populations | 16 | 10.59 | 9.21 | 0.092 | consistent |
| high | `final_MIC > 2`, their filter | 16 | 10.59 | 9.26 | 0.099 | **consistent** |
| low | all populations | 48 | 16.99 | 18.63 | 0.002 | not consistent |
| low | `final_MIC > 2`, their filter | 40 | 17.84 | 18.67 | 0.299 | **consistent** |

**On the quantity their figure plots, both arms reproduce.** The earlier failure came from
comparing my unfiltered output against a sheet whose published rendering is filtered.

The one residual left is the rate at which resistance fails to establish at all, which
their figure removes and does not report:

| arm | populations ending at MIC 2 | mine | theirs |
|---|---|---|---|
| high persistence | never evolved | 0 of 16 (0%) | 13 of 500 (2.6%) |
| low persistence | never evolved | 8 of 48 (**16.7%**) | 3 of 500 (**0.6%**) |

For the low arm this is 8 of 48 against 3 of 500, with non-overlapping binomial intervals,
so it is systematic and not sampling noise. These runs are not extinctions: the daily
series is complete for all of them, so the population survived twelve days with the wild
type still dominant. Note the direction reverses in the high arm, where my runs evolve
slightly more readily than theirs.

Ruled out as the cause of the rate difference:
- **Hill coefficient.** Tested at 2 and 3. At 3 the non-evolving fraction rises to 18.8%
  and the median falls, so 3 is worse, and 2 is what Table 1 and their driver both give.
- **Correlated seeds.** Impossible, per G3: the seeds never reach the generator.
- **Extinction bookkeeping.** Their Fig-5 sweep records zero extinctions at the nearest
  available regimen, and none of my non-evolving runs terminated early.

This residual is present **with every parameter set to its determined value**: Table 1
throughout, `min_bR` = 2 from their recorded output, `dilution_factor` = 1 and
`tau_max` = 0.1 from their driver. There is no remaining free parameter to blame.

## 4. What this already establishes, independent of the persistence question

A reader who downloads their deposit and runs it as given will not reproduce their
figures. They will find no resistance evolution at all in the high-persistence arm. The
correct parameter is recoverable, but only by reading the parameter columns embedded in
the result files, and one parameter is not recoverable at all.

This is worth reporting on its own terms and it does not depend on how the low-arm
question resolves.

## 5. Standing rule for this line of work

No statement about their conclusions goes into any manuscript until the residual is
either explained or disclosed with its size. As things stand the honest report is that
the high-persistence arm reproduces, the low-persistence arm reproduces above MIC 10, and
a systematic excess of non-evolving populations remains unexplained.

**The deposit has been exhausted.** The manuscript, the supplementary information, the
deposited code and the parameter columns of the deposited output have all been read. Every
parameter is determined, and the residual survives anyway. The remaining possibilities are
a difference in software environment, an undeposited variant of the script, or something
in their pipeline not visible in what was released.

The next step is to write to the corresponding authors, stating the residual precisely and
asking them to confirm `min_bR` and `sigma`, which are the two places where their own
sources disagree with each other. That is a normal request and is answerable briefly.
