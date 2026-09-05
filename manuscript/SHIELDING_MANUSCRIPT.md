# Dormant bacteria are less protected than persistence models assume, and the error compounds where treatment duration is decided

**Vahhab Piranfar**

1. Independent Researcher, Jersey City, NJ, USA
2. Farname Inc, Ontario, Canada

Corresponding author: Vahhab Piranfar · vahab.p@gmail.com · ORCID 0000-0003-3653-5739

---

## Abstract

Models of antibiotic persistence share two assumptions: that dormant cells are
largely shielded from the drug, and that they wake at a constant rate. Both are
convenient, and both can be checked against published measurements. We check
them, and both fail in the same direction. First, survival under a recent evolutionary
model changes twofold across a 32-fold range of antibiotic concentration where
the measurements change 730-fold, and the cause is not the one it appears to be:
the model's persister kill rate matches the measured one, 0.45 against 0.20 to
0.68 per hour, but its ordinary cells are annihilated at every concentration in
the range, so all survival is routed through a dormant compartment whose
response is flat by construction and the concentration axis collapses.
Second, single-cell lag times in *Escherichia coli* follow a power law with
exponent near −2 rather than the exponential a constant waking rate implies. The
two forms agree to within twenty percent for ten hours and then separate by
eleven orders of magnitude within a week. Third, the persistence level itself is
identifiable once survival is measured at several exposure durations, and the
value implied by the data is 461-fold below the value simulated for the same
condition. Each error is small where killing is fast and large where it is slow,
and time to clearance is a deep-tail quantity, so all three land on it together.
Re-running the published simulation with a persister kill rate matched to the
data leaves its reported contrast intact but eliminates 19 of 40 low-persistence
populations, where the published parameters eliminate none in 80 runs: a model
whose dormant compartment is too well protected cannot clear a population at
all, which is the outcome a clinician is interested in.

**Keywords:** antibiotic persistence, pharmacodynamics, heavy-tailed lag times,
parameter identifiability, model misspecification, treatment duration

---

## 1. Introduction

A persister is usually modelled as a cell in a second compartment that the
antibiotic barely reaches, leaving it at a constant rate. Both halves of that
picture are assumptions of convenience. A shielded compartment gives the slow
phase of a biphasic kill curve without requiring the drug's action on dormant
cells to be measured. A constant waking rate gives an exponential distribution
of dormancy durations, which makes the waking rate a single number that can be
fitted, ranked and reported.

Neither assumption has to be taken on trust. Published data bear on both, and
the deposits are open. This paper checks them.

We find that they fail together, and that they fail in the direction that
matters. Dormant cells in the models are more protected than the data allow, and
they leave dormancy in a way the models cannot represent. Where killing is fast
these errors are invisible: a two-state model with exponential switching
reproduces the first hours of a kill curve well, which is why the assumptions
have survived. Where killing is slow the same errors are enormous. Time to
clearance is a four-log quantity. It is decided entirely in the region where the
models are wrong.

## 2. The model loses the concentration axis, and not where you would expect

### 2.1 The model's survival barely depends on concentration

Under the model of Boccarella et al., survival after a five-hour exposure at the
nutrient level used for their high-persistence arm changes by a factor of two
across a 32-fold range of antibiotic concentration. The measured survival over
the same range changes by a factor of 730.

| concentration (µg/mL) | model | measured | model / measured |
|---|---|---|---|
| 12.5 | 1.3 × 10⁻⁴ | 0.113 | 0.0012 |
| 25 | 8.5 × 10⁻⁵ | 9.2 × 10⁻⁴ | 0.093 |
| 50 | 7.2 × 10⁻⁵ | 4.7 × 10⁻⁴ | 0.15 |
| 100 | 6.8 × 10⁻⁵ | 1.6 × 10⁻⁴ | 0.43 |
| 200 | 6.7 × 10⁻⁵ | 1.8 × 10⁻⁴ | 0.37 |
| 400 | 6.6 × 10⁻⁵ | 1.6 × 10⁻⁴ | 0.43 |

Halving the dose from 25 to 12.5 µg/mL raises survival 1.55-fold in the model
and 123-fold in the data. The model is close at the top of the range and wrong
by nearly three orders of magnitude at the bottom.

### 2.2 The cause is not the persister kill rate

The obvious explanation would be that persisters are killed too slowly in the
model. They are not. The persister kill rate can be read directly off the slow
phase of each measured curve, and it agrees with the model:

| | persister kill rate |
|---|---|
| measured, slow-phase slopes at ≥50 µg/mL | 0.20 – 0.68 /h |
| model | 0.45 /h |

Both are close to flat in concentration: 0.018/h per doubling measured against
0.002/h per doubling in the model. On this quantity, which is what the model
says about dormant cells, the model is right.

### 2.3 The cause is that the model puts everything in the dormant compartment

The model's normal-cell survival at 12.5 µg/mL is 10⁻¹¹. Ordinary cells are
annihilated at every concentration in this range, so all modelled survival is
persister survival — the persister term supplies 99.99% of it at both 12.5 and
25 µg/mL — and the persister term is flat in concentration. The concentration
axis collapses because there is nothing left on it that responds.

The data do not behave that way. At 12.5 µg/mL the population declines at
roughly 0.4/h throughout the eight hours, with no fast phase and no break: the
survivors are ordinary cells that the drug has not killed, not a dormant
subpopulation. At 25 µg/mL a fast phase appears, reaching 3.2/h in the second
hour, and only then does the curve break into a slow tail.

| | instantaneous kill rate per hour, hours 1 to 8 |
|---|---|
| 12.5 µg/mL | 0.61, 0.73, 0.04, 0.40, 0.37 |
| 25 µg/mL | 0.49, **3.16**, 1.79, 0.78, 0.03 |

So the model's failure is located in the normal compartment, not the dormant
one. Its concentration-response for ordinary cells saturates so early that a
concentration the data show to be barely bactericidal is treated as completely
lethal. Everything then flows through the dormant compartment, whose response
is flat by construction, and the model loses the concentration axis entirely.

The consequence for the dormant compartment is indirect but real: a model that
routes all survival through it must make it large enough to carry the observed
survivors, which is the subject of Section 4.

## 3. Waking is not a rate

### 3.1 What a constant rate implies

A constant resuscitation rate makes dormancy durations exponential. That is what
licenses treating the waking rate as a parameter, and it is the assumption
behind every sensitivity ranking in which a resuscitation rate appears.

Şimşek and Kim measured lag times for approximately 12,800 individual
*E. coli* cells and tabulated the binned counts, so the claim can be refitted
rather than accepted. Their two independent series give a power law with
exponent −2.25 and −2.11, at $R^2$ of 0.993 and 0.971, against 0.956 and 0.847
for the exponential. The power law wins in both.

### 3.2 Where it matters

The two forms are nearly indistinguishable early and wholly different late.

| time | exponential | power law | ratio |
|---|---|---|---|
| 10 h | 0.143 | 0.167 | 1.2 |
| 20 h | 0.020 | 0.083 | 4.1 |
| 40 h | 4.2 × 10⁻⁴ | 0.042 | 99 |
| 160 h | 3.1 × 10⁻¹⁴ | 0.010 | 3.4 × 10¹¹ |

The dormant pool reaches $10^{-4}$ of its initial size in 47 hours under a
constant rate and in roughly 16,700 hours under the power law, a factor of 352.
An experiment that runs for a day sees the region where the two agree. A
treatment that runs for months lives in the region where they do not.

### 3.3 The rate is a property of the observation window

A density falling as $t^{-2}$ has a logarithmically divergent mean. A
resuscitation rate fitted to it therefore exists only relative to where the
distribution is truncated:

| window | implied rate |
|---|---|
| 1,000 min | 0.26 /h |
| 20,000 min | 0.11 /h |
| 2,000,000 min | 0.061 /h |

The same underlying process yields a fourfold range of rates depending on how
long the cells were watched. A rate reported this way describes the experiment
as much as the bacteria.

### 3.4 One model does something stronger

Boccarella et al. do not assume a constant rate. Their code converts a binomial
fraction of each subpopulation to persisters at the start of an antibiotic
pulse and returns all of them at the end:

```python
subpop['pop'] += subpop.get('pop_PR', 0)
subpop['pop_PR'] = 0
```

The dormancy duration is therefore a delta function at exactly the pulse length,
with zero variance. No cell wakes during exposure and no cell remains dormant
between pulses. Under the measured power-law distribution, 67% of dormant cells
would wake within a five-hour pulse.

This matters because a cell that wakes mid-pulse is killed as a normal cell, in
the compartment whose concentration-response is steep. It supplies part of the
missing dependence of Section 2: adding it raises the predicted log ratio from
0.28 to about 0.70. That is a two-and-a-half-fold improvement and still short of
the observed 4.3 to 5.3, so waking is part of the answer and not all of it.

## 4. The persistence level is identifiable, and it is not the value being used

### 4.1 Why it looked unidentifiable

At a single exposure duration, survival determines only the product
$\alpha \exp[-(d_P + a_P)\tau]$. One number, two unknowns. On the 95-row slice
of this dataset that circulates with the modelling literature — two
concentrations, one duration per treatment cycle — $\alpha$ cannot be recovered,
and we previously concluded it could not be recovered at all.

That conclusion was a property of the slice, not of the measurement. The full
deposit carries six exposure durations, six concentrations spanning 32-fold and
six nutrient levels at three replicates. With the duration axis,

$$\ln S(\tau) = \ln\alpha - (d_P + a_P)\,\tau$$

is a straight line whose intercept is $\ln\alpha$ and whose slope is the
persister kill rate. Both come out separately from the slow phase of the curve.
This is the ordinary reading of a biphasic kill curve; it is available here only
because the deposit has the axis.

### 4.2 What the data say

| nutrient level | fitted $\alpha$ | simulated | ratio |
|---|---|---|---|
| 0 (starvation) | 0.74 | — | — |
| 0.25 | 1.7 × 10⁻³ | 0.8 | **461×** |
| 0.5 | 2.1 × 10⁻⁴ | — | — |
| 0.8 | 3.6 × 10⁻⁶ | 5 × 10⁻⁵ | 13.7× |
| 0.9 | 1.2 × 10⁻⁵ | — | — |
| 0.95 | 3.7 × 10⁻⁵ | — | — |

The contrast between the two conditions used as high and low persistence is
476-fold in the data and 16,000-fold as simulated.

Stated fairly: a persistence level near 0.8 is real in this dataset. It occurs
at complete nutrient starvation, not at the 25% nutrient level from which the
high-persistence arm is drawn. The parameter is not invented; it is applied to
the wrong condition.

## 5. What the shielding costs a published conclusion

The three preceding sections are about model structure. This one asks what the
structure does to a result someone has drawn from it.

Boccarella et al. compare two persistence levels and report that the
low-persistence arm reaches a higher final minimum inhibitory concentration than
the high-persistence arm, by about 1.7-fold. We re-ran their simulation
unmodified, changing only a parameter their own driver exposes: the floor on the
persister kill rate, from $-0.5$/h to $-3.58$/h. Forty populations per arm per
scenario. This is a sensitivity analysis and not a recalibration: Section 2.2
shows the published persister kill rate already matches the measured one, so the
change asks what the model does when dormant cells are made killable, not what
the data say they are.

Their contrast survives. Among populations that were not eliminated, the ratio
is 2.01 under the published parameters and 2.05 under the recalibrated ones, and
the two arms separate at $p = 2	imes10^{-6}$. The conclusion is robust to the
correction, and we say so.

What changes is what the model was not able to express.

| | populations eliminated, low-persistence arm | high-persistence arm |
|---|---|---|
| published parameters | 0 / 40 | 0 / 40 |
| recalibrated | **19 / 40** | 0 / 40 |

Under the published persister kill rate, no population is ever cleared, in
either arm, in any of the 80 runs. Under a persister kill rate that matches the
survival data, nearly half the low-persistence populations are eliminated
outright ($p = 2	imes10^{-7}$, Fisher's exact test), and none of the
high-persistence ones are.

This is the shielding of Sections 2 to 4 expressed as an outcome. A model whose
dormant compartment is too well protected cannot clear a population, so every
population must survive and the only question it can answer is how far each one
evolves. Give the drug the access to dormant cells that the data show it has,
and clearance becomes the dominant outcome in exactly the arm where persistence
is scarce — which is the outcome a clinician is interested in and the one the
published model cannot produce at all.

## 6. Discussion

### 6.1 The three failures are one failure

Each of the first three results says that dormant cells are less isolated from the drug than the
models represent. The concentration-response is too shallow because survival
runs through a compartment whose kill rate is capped. The lag distribution is
heavy-tailed because cells leave dormancy continuously rather than at a fixed
rate or a fixed time. The persistence level is overstated because a shielded
compartment must be made large to reproduce an observed slow phase that is
really produced by cells waking into the drug and dying there.

A model in which dormancy is a graded, concentration-permeable state with a
heavy-tailed exit time would produce all three observations from one mechanism.
We have not built it, and we do not claim that it would.

### 6.2 What is safe and what is not

None of this overturns a published conclusion by itself. A sensitivity ranking
computed on a two-state model with exponential switching remains true of that
model. What these results do is bound the conditions under which such rankings
transfer to bacteria.

The bound is sharp and it has a location. Quantities decided in the first ten
hours are safe: that is where the assumptions were tested and where they hold.
Quantities decided four logs down are not, and treatment duration is one of
them.

### 6.3 Limitations

The concentration-response test compares model predictions with published
survival measurements made under protocols that differ from the simulated one in
exposure duration, medium and in one case antibiotic class. The steepness per
doubling is comparable across these differences; absolute survival is not, and
we do not compare it.

The lag-time analysis rests on one study, refitted from its published binned
counts rather than from individual cell measurements, and on two experimental
series within it. The power law is fitted over roughly one decade of time. A
heavy tail over a wider range would strengthen the argument and a truncation
would weaken it.

Section 4 assumes the slow phase of the kill curve is the persister phase, which
is the standard reading and is not independently verified here. Below 50 µg/mL
the fast phase has not finished by eight hours, so those fits are excluded from
the summary rather than reported as persistence levels.

Every dataset used is published, was obtained from its public deposit, and is
listed with its accession. No experiment was performed for this work.

## 7. Methods

All analyses are reproducible from the accompanying repository. Each stage
writes a receipt recording library versions and run parameters.

**Data.** Time-kill and evolution data of Windels et al. 2024 (ISME J
18(1):wrae070) from Zenodo record 7550302 under CC BY 4.0, verified by
independent re-download against the copy obtained by literature search;
simulation code and the redeposited survival slice of Boccarella et al. 2026
(Mol Biol Evol 43:msag180) from figshare 10.6084/m9.figshare.31389142 under
CC BY 4.0; recurrent-exposure CFU counts for *E. coli* MG1655 under ampicillin;
survival scores for eight *Pseudomonas* species under ciprofloxacin and
rifampicin from Vogwill et al.; and the binned lag-time counts of Şimşek and Kim
2019 (PNAS 116, doi:10.1073/pnas.1903836116) from their supplementary appendix.

**Concentration-response.** Survival ratios were compared within a nutrient
level and treatment cycle so that the contrast is between concentrations.
Populations are unpaired, so a two-sample comparison on log survival was used.
The model ceiling was matched to each experiment's own exposure duration, since
it is a rate limit.

**Lag distribution.** Logarithmically binned counts were converted to densities
by dividing by the bin midpoint, since the bin width grows in proportion to it.
The first bin is the bulk of the population and was excluded from both fits, so
that neither functional form is judged on a region it was not meant to describe.

**Persistence level.** The slow phase was taken from two hours onward, with at
least three points required, and fitted by least squares on log survival. Only
concentrations at or above 50 µg/mL enter the summary, because below that the
fast phase has not finished within the observation window.

**Simulation.** The simulation of Boccarella et al. was run unmodified. Only
parameters their own driver exposes were changed.
