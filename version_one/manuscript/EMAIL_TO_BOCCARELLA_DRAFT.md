# Draft email to the authors

**To:** giorgio.boccarella@kuleuven.be; piet.vandenberg@kuleuven.be
**Subject:** Reproducing the simulations in msag180 — a few parameter questions

## What we are actually asking for, and why

Four things, in descending order of how much we need them.

**1. Why resistance fails to establish twenty times more often in our
low-persistence arm.** This is the only item that blocks anything. Their high
arm reproduces almost exactly, so the setup is right in general. But in the low
arm 12% of our populations never evolve at all, against 0.6% of theirs, in three
independent batches spanning 108 populations. We have ruled out the Hill
coefficient, seeding and the tau-leaping step. We cannot find it in the deposit,
and they can answer it in one line if they know.

Note this is a quantity their Figure 3 filters out and never reports, so they may
never have looked at it.

**2. Confirmation of `min_bR` = 2.** We are already confident, since three of
their four scripts hardcode it and all their recorded output carries it. But it
is their model, and describing it wrongly in print would be worse than asking.

**3. Confirmation of σ = 0.7.** Their Table 1 prints 0.07. Code and output both
say 0.7. Same reasoning: we need to describe their model correctly.

**4. What *b* = 1.7 in Table 1 denotes.** Genuinely ambiguous. It is not the
birth rate any lineage in the simulation uses.

Nothing here needs their permission or blocks writing. Items 2 to 4 protect us
from misdescribing their work; item 1 might resolve a real puzzle.

## Notes before sending

**Tone.** Reports one unexplained result and asks three factual questions. No
criticism, no interpretation of what the discrepancies mean, no mention of
publication. This is now a friendly message: the substance of their conclusion
holds up in our hands.

**Disclosure.** Decide whether to say this is preparatory work for a possible
paper. Not saying so is normal for a first factual query. If the exchange
continues, say it. Easier to say early than to have it inferred.

**The tau-leaping step has been tested and ruled out.** A finer step (0.02
against the default 0.1) moves both quantities further from theirs, not closer.

---

Dear Dr Boccarella and Dr van den Berg,

I have been working with the simulation code and data you deposited alongside
your recent paper in *Molecular Biology and Evolution* (msag180,
doi:10.1093/molbev/msag180). Thank you for releasing it so completely — the
parameter columns embedded in the result files in particular have been very
useful.

I can reproduce your high-persistence arm closely, but not your low-persistence
arm, and I would be grateful for your help on that and on three smaller points.

**1. The low-persistence arm.** Running your deposited
`magnitude_of_evolution_simulations.py` unmodified at 12.5 µg/mL, with
`min_bR` = 2, `kappaS` = 2, `dilution_factor` = 1, σ = 0.7, µ = 10⁻⁶, and the
remaining Table 1 values:

| arm, α as you simulate it | quantity | mine | yours |
|---|---|---|---|
| high, α = 0.8 | median final MIC among evolved, n = 20 | 9.20 | 9.25 |
| high | populations never evolving | 0 of 20 | 13 of 500 (2.6%) |
| low, α = 5×10⁻⁵ | median final MIC among evolved, n = 95 | 17.61 | 18.67 |
| low | **populations never evolving** | **13 of 108 (12.0%)** | **3 of 500 (0.6%)** |

The high arm is consistent with yours (two-sample Kolmogorov–Smirnov p = 0.84).

For the low arm, the firm difference is the bottom row: how often resistance
never establishes at all. Across 108 populations in three independent batches I
get 12.0% (95% CI 6.6–19.7%), against your 0.6%, and every individual batch of
mine falls in the 7.5–16.7% range. These are not extinctions; the daily series
runs to day 12 in all of them, with the wild type still dominant.

I should be careful about the median. Pooled it differs from yours (17.61 against
18.67, p = 0.01), but my own three batches differ from one another about as much
(16.25, 17.84, 19.55), so I would not press that point.

Both comparisons apply the `final_MIC > 2` filter your `Fig_3_a-b.R` uses at line
70, so they are on the basis your figure plots.

Ruled out so far: the Hill coefficient (2 and 3 tried; 3 is worse); random
seeding, since `RUN_tau_leaping` calls `np.random.seed()` with no argument at
line 66 and reseeds from system entropy regardless of the caller; and the
tau-leaping step, since `tau_max` = 0.02 against the default 0.1 moves both
quantities further from yours rather than closer.

Is there something about the published configuration I have missed — a different
version of the script, a particular Python or NumPy version, or a step not
visible in the deposit? I am on Python 3.14 with NumPy 2.5, calling
`run_simulation_with_mic` directly.

**2. `min_bR`.** `magnitude_of_evolution_simulations.py` sets
`min_bR_values = [bS]`, that is 1.7. Your other three simulation scripts all set
`min_bR_values = [2]`, and every row of the recorded output in `Fig_2_b` and
`Fig_6` carries `min_bR = 2`. Since 1.7 gives me no resistance evolution at all
in the high-persistence arm, against your published median of 9.21, I have
assumed 2 is correct and that the `[bS]` in that one file is a leftover. Could
you confirm?

**3. σ.** Table 1 gives σ = 0.07 for the log-normal distribution of mutational
effects, while `main()` and the recorded output both give 0.7. I have used 0.7.
If Table 1 is a typographical error it may be worth a correction, since σ governs
the spread of mutational effect sizes.

**4. The birth rate.** Table 1 gives a single birth rate *b* = 1.7, but in the
code each lineage's birth rate comes from `mic_to_br(mic, min_bR)`, which
interpolates from 2.0 at MIC 1 down to `min_bR` at MIC 32. The wild type at MIC 2
therefore replicates at 1.99 when `min_bR` = 1.7, and at 2.0 when `min_bR` = 2 —
in neither case at 1.7. Is *b* in Table 1 meant to be the wild-type birth rate,
or the floor of that interpolation?

I would be glad to send my run scripts and outputs if that would help.

With thanks and best wishes,

Vahhab Piranfar
ORCID 0000-0003-3653-5739
vahab.p@gmail.com

---

## Evidence behind each number

| Claim | Source |
|---|---|
| high arm 9.20 vs 9.25, KS p = 0.84 | `results/tables/exp05_replicates.csv`, scenario `authors`; `data/raw/boccarella2026/sim_final_mic_Fig3.csv` |
| low arm 17.61 vs 18.67, KS p = 0.010 | pooled `exp06_reproduction.csv` + `exp05_replicates.csv` + `exp07_tau_test.csv`, n = 95 evolved |
| never-evolved 13 of 108 vs 3 of 500 | same three files; binomial p = 1.6×10⁻¹³ |
| my batches vary among themselves | medians 16.25, 17.84, 19.55; Kruskal-Wallis p = 0.045 |
| tau-leaping step ruled out | `results/tables/exp07_tau_test.csv`, 20 replicates per step size |
| `min_bR` 1.7 in one script, 2 in three others | `Simulations_code/*.py`, `main()` in each |
| `min_bR` = 2 in all recorded output | `data/raw/boccarella2026/sim_params_Fig2b.csv` |
| b = 1.7 is not any lineage's birth rate | `mic_to_br`, lines 34-39 |
| `psimaxS` computed but unused | line 65 defines it; the loop uses `psimaxR` at line 154 |
| internal reseed | line 66 |
| Fig-3 filter | `Fig_3/Fig_3_a-b.R` line 70 |
