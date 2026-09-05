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
them, and both fail in the same direction. First, the concentration-response of
persister killing in a recent evolutionary model is five- to thirteen-fold
shallower than survival data from three genera and four antibiotics, and its
functional form carries a ceiling that no parameter value can pass: the
persister kill rate is bounded at 0.55 per hour, so no two concentrations can
differ by more than 2.75 in log survival, while the observations reach 5.3.
Second, single-cell lag times in *Escherichia coli* follow a power law with
exponent near −2 rather than the exponential a constant waking rate implies. The
two forms agree to within twenty percent for ten hours and then separate by
eleven orders of magnitude within a week. Third, the persistence level itself is
identifiable once survival is measured at several exposure durations, and the
value implied by the data is 461-fold below the value simulated for the same
condition. Each error is small where killing is fast and large where it is slow.
Time to clearance is a deep-tail quantity, so all three land on it together.

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

## 2. The concentration-response of persister killing is too shallow, and it is capped

### 2.1 A test that needs neither unknown

Persister survival under a pharmacodynamic model of the standard form is

$$S(c,\tau) = \alpha \exp\!\big[-(d_P + a_P(c))\,\tau\big] + (1-\alpha)\,S_{\text{normal}}(c,\tau)$$

with $\alpha$ the persistence level, $d_P$ a drug-independent death rate and
$a_P(c)$ the drug-dependent kill rate. Neither $\alpha$ nor $d_P$ is easy to
measure. But the ratio of survival at two concentrations removes them both:

$$\ln\frac{S(c_1,\tau)}{S(c_2,\tau)} = \big[a_P(c_2) - a_P(c_1)\big]\,\tau$$

$d_P$ cancels exactly and $\alpha$ cancels to within $3\times10^{-6}$ in log
units across the range of interest, the residual coming only from the normal
compartment's small contribution. What remains is the concentration-response of
persister killing alone, which the model specifies analytically. It is a
prediction with effectively no free parameters, and it can be checked against
any dataset that reports survival at two concentrations.

### 2.2 The prediction fails by two orders of magnitude

Applied to the model of Boccarella et al. and to the survival data its own
persistence contrast is drawn from, the prediction is that doubling the
concentration from 12.5 to 25 µg/mL reduces survival 1.55-fold. The data show
203-fold at one nutrient level and 75-fold at another. Both confidence intervals
exclude the prediction, at $p=0.025$ and $p=0.002$.

| | ln ratio | fold |
|---|---|---|
| model prediction | 0.440 | 1.55 |
| observed, 25% nutrient | 5.31 ± 0.47 | 203 |
| observed, 80% nutrient | 4.32 ± 0.73 | 75 |

### 2.3 The gap cannot be closed by tuning

The functional form has a ceiling. With a maximum persister growth rate of
0.05/h and a floor on the minimum net growth rate of −0.5/h, the persister kill
rate cannot exceed 0.55/h. Over a five-hour exposure no two concentrations can
differ by more than 2.75 in log survival, at any parameter values. Both
observations exceed that.

Raising the Hill coefficient makes matters worse rather than better. Above the
minimum inhibitory concentration the response is already saturated, so a steeper
curve saturates sooner: the achievable log ratio falls from 0.33 at $\kappa=2$
to 0.05 at $\kappa=4$ and to zero by $\kappa=12$. Varying the assumed MIC does
not rescue it either; the best achievable value over all MIC and all $\kappa$
tested is 0.33, an order of magnitude short.

The same is not true of the normal compartment. Its floor is −6/h rather than
−0.5/h, and at an assumed MIC between 4 and 16 µg/mL the identical functional
form produces log ratios of 7 to 12.5 — more than the observations require. The
problem is therefore specific and locatable. It is not the Regoes form, which is
adequate. It is that survival is routed almost entirely through a compartment
whose kill rate is capped by a constant, and that constant is too small.

### 2.4 Independent data agree

Four published datasets, obtained from their public deposits and spanning two
genera and three antibiotics, give the same answer. Every stratum is steeper
than the model, and three exceed the ceiling once it is matched to each
experiment's own exposure duration.

| organism | antibiotic | ln per doubling | vs model |
|---|---|---|---|
| *E. coli*, ampicillin, pulse 1 | ampicillin | −1.43 | 5.1× |
| *E. coli*, ampicillin, pulse 2 | ampicillin | −0.79 | 2.8× |
| *E. coli*, ampicillin, pulse 3 | ampicillin | −0.83 | 3.0× |
| *Pseudomonas*, 8 species | ciprofloxacin | −3.72 | 13.4× |
| *Pseudomonas*, 8 species | rifampicin | −1.27 | 4.6× |
| model | | −0.28 | — |

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

## 5. Discussion

### 5.1 The three failures are one failure

Each result says that dormant cells are less isolated from the drug than the
models represent. The concentration-response is too shallow because survival
runs through a compartment whose kill rate is capped. The lag distribution is
heavy-tailed because cells leave dormancy continuously rather than at a fixed
rate or a fixed time. The persistence level is overstated because a shielded
compartment must be made large to reproduce an observed slow phase that is
really produced by cells waking into the drug and dying there.

A model in which dormancy is a graded, concentration-permeable state with a
heavy-tailed exit time would produce all three observations from one mechanism.
We have not built it, and we do not claim that it would.

### 5.2 What is safe and what is not

None of this overturns a published conclusion by itself. A sensitivity ranking
computed on a two-state model with exponential switching remains true of that
model. What these results do is bound the conditions under which such rankings
transfer to bacteria.

The bound is sharp and it has a location. Quantities decided in the first ten
hours are safe: that is where the assumptions were tested and where they hold.
Quantities decided four logs down are not, and treatment duration is one of
them.

### 5.3 Limitations

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

## 6. Methods

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
