# Growth regime determines which parameters govern antibiotic killing in a state-structured pharmacodynamic model

**Vahhab Piranfar**

1. Independent Researcher, Jersey City, NJ, USA
2. Farname Inc, Ontario, Canada

Corresponding author: Vahhab Piranfar · vahab.p@gmail.com · ORCID 0000-0003-3653-5739

---

## Abstract

Resistance, tolerance and persistence are three different ways a bacterial
population survives an antibiotic, and clinicians treat them differently. The
single-exponential representation used to model them does not: writing all three
as $N(t) = N_0 e^{-kt}$ with a different value of $k$ makes them one object under
three names, and leaves no measurement able to separate them. We build a two-compartment
pharmacodynamic model in which replicating and dormant subpopulations each carry
their own sigmoid concentration–response, and show that the three strategies then
occupy separate directions in a space of quantities a laboratory already
measures: resistance moves the minimum inhibitory concentration sixteen-fold and
leaves the minimum duration for killing untouched, tolerance multiplies that
duration fourfold at an unchanged concentration, and persistence lifts the deep
killing endpoint 3.6-fold while moving the shallow one by 2.5%. Biphasic killing
emerges from the compartment structure rather than being imposed by a breakpoint.
Variance-based global sensitivity analysis then shows that which parameter
governs killing is not a property of the drug but of the growth regime: for a
slow grower the resuscitation rate of dormant cells carries 78% of the
first-order variance in time to detection limit, while for a fast grower its
total-order index falls to $2 \times 10^{-5}$ and interactions account for
roughly 70% of the variance. We give the sampling designs under which each
parameter can and cannot be estimated.

**Keywords:** antibiotic tolerance, bacterial persistence, pharmacodynamics,
minimum duration for killing, practical identifiability, global sensitivity
analysis

---

## 1. Introduction

A patient with a staphylococcal bacteraemia is treated for two weeks. A patient
with drug-susceptible tuberculosis is treated for six months. Neither duration
follows from the minimum inhibitory concentration of the organism, because both
organisms are susceptible. The difference is in how the surviving population
behaves under an antibiotic it cannot resist, and that behaviour has three
distinct forms which the field has agreed to name and define separately
(Brauner et al. 2016; Balaban et al. 2019).

Resistance raises the concentration required to inhibit growth. Tolerance leaves
that concentration where it is and extends the time required to kill. Persistence
leaves both bulk quantities alone and expresses itself only in a subpopulation
that survives far longer than the rest (Lewis 2007; Levin and Rozen 2006). The
operational definitions are quantitative and, in principle, measurable: a shift
in the minimum inhibitory concentration, a shift in the minimum duration for
killing at a fixed concentration, and a change in the shape of the deep tail of
the killing curve.

Single-exponential representations cannot carry these distinctions. When
resistance, tolerance and persistence are each written as $N(t) = N_0 e^{-kt}$
with a different rate constant, they differ in a number and in nothing else. This is not
an approximation that loses precision; it is a representation that cannot express
the thing it names. Two of these strategies are defined by *when* killing happens
rather than by *how fast*, and a single exponential has no time structure to
carry that information. No fitting procedure recovers a distinction the model
does not contain, and no amount of data repairs it.

The obstacle is therefore structural, not numerical. Separating the three
strategies requires a model with at least two subpopulations of differing drug
susceptibility, and one that expresses drug concentration explicitly, since two of
the three definitions are statements about concentration. A two-compartment
system with a sigmoid concentration–response satisfies both requirements; no
single exponential satisfies either. That much is a modelling choice, and what
makes it worth making is what follows from it.

First, the three strategies become separable by measurement. Given the
compartment structure, each leaves a distinct signature across the minimum
inhibitory concentration and the shallow and deep killing endpoints, so an
isolate can be placed in that space from assays laboratories already run. This
converts a classification that is currently argued from mechanism into three
numbers that can be reported and compared.

Second, biphasic killing stops being an assumption. Closed-form biphasic laws
impose a breakpoint at an explicit transition time and fit that time as a free
parameter. In a state-structured model the biphasic shape is a consequence of the
compartments, the curvature maximum is a derived observable rather than an input,
and time to the detection limit is finite and computable rather than asserted.

Third, and least expected, the identity of the parameter that governs killing is
not fixed. It depends on the growth regime of the organism. For a slow grower the
rate at which dormant cells resume replication dominates the variance in time to
the detection limit; for a fast grower the same rate falls four orders of
magnitude in importance and most of the variance is carried by interactions
rather than by any parameter alone. A regimen-shortening
strategy built for one organism therefore has no structural reason to transfer to
the other, and this is a prediction of the model rather than an observation about
either species.

This is a modelling and analysis paper. It contains no experimental data, its
parameter values are illustrative and chosen to reproduce documented qualitative
behaviour, and its species-level statements are therefore qualitative. It
establishes which quantities must be measured, which of them a given experimental
design can determine, and what a model must contain before those measurements can
be interpreted at all.

## 2. A state-structured pharmacodynamic model

### 2.1 The model

Let $S(t)$ be the density of replicating cells and $P(t)$ the density of dormant
cells, both in colony-forming units per millilitre, under a constant drug
concentration $C$ expressed in multiples of a reference minimum inhibitory
concentration. Cells replicate logistically, switch between the two states, and
are killed at a rate set by a sigmoid concentration–response:

$$\frac{dS}{dt} = rS\left(1 - \frac{S+P}{K}\right) - k_{S\to P}S + k_{P\to S}P - E_S(C)\,S$$

$$\frac{dP}{dt} = k_{S\to P}S - k_{P\to S}P - E_P(C)\,P$$

with Hill kill functions

$$E_S(C) = \frac{E_{\max,S}\,C^{H}}{EC_{50}^{H} + C^{H}}, \qquad
E_P(C) = \frac{E_{\max,P}\,C^{H}}{(\rho\, EC_{50})^{H} + C^{H}}$$

where $r$ is the replication rate, $K$ the carrying capacity, $k_{S\to P}$ and
$k_{P\to S}$ the switching rates into and out of dormancy, $E_{\max,S}$ and
$E_{\max,P}$ the maximum kill rates of the two compartments, $EC_{50}$ the
concentration giving half-maximal kill of replicating cells, $H$ the Hill
coefficient, and $\rho$ the ratio of the dormant compartment's $EC_{50}$ to that
of the replicating compartment. The kill functions follow Regoes et al. (2004);
the two-compartment structure is standard (Nielsen and Friberg 2013).

### 2.2 The three strategies as parameter changes

Each strategy is imposed as a change to one mechanism, holding the others fixed,
so that the resulting signatures are consequences rather than constructions.

**Resistance** multiplies $EC_{50}$ by a fold change. The concentration required
for half-maximal kill rises; the maximum achievable kill rate does not change.

**Tolerance** divides $r$, $E_{\max,S}$ and $E_{\max,P}$ by the same factor. This
is the point at which an implementation can go quietly wrong. Slowing metabolism
slows both growth and killing, and dividing the kill rates alone shifts the
minimum inhibitory concentration by $\text{fold}^{1/H}$, which is partial
resistance rather than tolerance. Dividing all three together leaves the minimum
inhibitory concentration exactly invariant, which is what the operational
definition requires.

**Persistence** raises $k_{S\to P}$, enlarging the dormant subpopulation without
altering any rate constant of either compartment.

### 2.3 The state of the inoculum

The dormant fraction of the inoculum is not a free choice. In a population held
at carrying capacity, where replication has stopped, switching balances at
$f = k_{S\to P}/(k_{S\to P} + k_{P\to S})$. A time-kill experiment does not start
there: it starts from an exponentially growing culture, where replication keeps
refilling the replicating compartment faster than switching drains it.

Taking $S$ and $P$ to grow exponentially at a common rate $\lambda$ gives
$P/S = k_{S\to P}/(\lambda + k_{P\to S})$, so the dormant fraction of a growing
population is

$$f = \frac{k_{S\to P}}{\lambda + k_{P\to S} + k_{S\to P}}, \qquad
\lambda^2 + \lambda\left(k_{S\to P} + k_{P\to S} - r_{\text{eff}}\right)
- r_{\text{eff}}\,k_{P\to S} = 0$$

with $r_{\text{eff}} = r(1 - N_0/K)$. At $r_{\text{eff}} = 0$ this returns
$\lambda = 0$ and collapses to the stationary-phase expression, as it must. While
the population grows it is smaller: fourfold for the slow grower of Section 2.5
and sixfold for the fast one. Initialising at the stationary-phase value and then
integrating an exponentially growing population overstates the dormant pool of
the inoculum by that factor. The trajectory inherits the error, but does not
preserve it: once killing begins the compartment ratio evolves under the drug, so
the discrepancy is a function of time rather than a constant offset.

### 2.4 Endpoints

Four quantities are computed from each solution, chosen because each is
measurable and because the operational definitions are stated in terms of them.

- **MIC**, the lowest concentration at which the net growth rate of the bulk
  population is non-positive, obtained by root-finding on the initial net growth
  rate of the inoculum in the state it actually starts from.
- **MDK$_{99}$** and **MDK$_{99.99}$**, the times to two- and four-log$_{10}$
  reduction: the shallow and deep killing endpoints.
- **Time to LOD**, the time at which the population first falls below an assay
  limit of detection, taken as $10^2$ CFU/mL.

This is time to the limit of detection, not time to sterilisation. Falling below
a detection limit is not sterility: true sterilisation is an extinction event at
small copy number, which a deterministic model cannot represent.

### 2.5 Parameter values

Two illustrative parameter sets stand for a slow grower and a fast grower.
Values are chosen to reproduce documented qualitative behaviour — replication
rates differing by more than an order of magnitude, dormant subpopulations of
order $10^{-3}$ to $10^{-4}$, and a dormant compartment far harder to kill than a
replicating one — and are not fitted to any dataset. They are inputs to a
structural argument, not estimates.

### 2.6 Exposure

Concentration is set to four times the minimum inhibitory concentration *of the
parameter set being simulated*, recomputed for every draw. The alternative, a
single absolute concentration applied to every parameter set, compares organisms
of different susceptibility at different multiples of their own MIC: for the two
sets used here, a common absolute concentration of four reference-MIC units is
15.1 times the MIC of the slow grower and 5.0 times that of the fast one, and any
between-organism contrast then carries that difference inside it. Normalising to
each set's own MIC also closes the route by which $EC_{50}$ acts on the outcome
through exposure, so the two conventions ask different questions; results under
both are reported in the supplementary tables.

### 2.7 Sensitivity, estimation and identifiability

First- and total-order Sobol indices were computed with the Saltelli estimator
over $\pm50\%$ log-uniform ranges on seven parameters, from 4,096 base samples,
giving 36,864 model evaluations per organism, with 2,000-sample bootstrap
intervals on every index. Smaller designs return negative first-order estimates
for parameters carrying no variance, which is a statement about Monte Carlo error
rather than about the model, and the bootstrap intervals are reported so that a
reader can tell the two apart.

Fitting was performed on synthetic data with known ground truth, since no
experimental dataset is used in this work. Observations below the limit of
detection contribute $\log\Phi\!\left((\mathrm{LOD}-\mu)/\sigma\right)$ to the
log-likelihood (Beal 2001), with $\sigma$ estimated alongside the parameters;
assigning such points a zero residual gives a workable objective but not a
likelihood, and information criteria built on it do not have their usual meaning.
Model comparison used AICc and BIC from that likelihood, and parameter
identifiability was assessed by profile likelihood, re-optimising all other
parameters and $\sigma$ at each fixed value and taking the interval where
$2(\ell_{\max}-\ell)$ stays below the $\chi^2_1$ 95% quantile.

## 3. Results

### 3.1 State structure generates biphasic killing

Biphasic killing does not have to be put into a model by hand. Under a constant
exposure of four times MIC, both parameter sets produce a killing curve with a
sharp initial decline and a slow tail, and the curvature maximum separating the
two phases appears at 61 h for the slow grower and 19 h for the fast one
(Figure 1A, 1B). Neither number was supplied. Both are derived observables,
consequences of the rate at which the replicating compartment is depleted
relative to the rate at which the dormant compartment is refilled and killed.

This is the substantive difference from a closed-form biphasic law, which
introduces a transition time $t_c$ as a fitted parameter and switches between two
exponentials at it. Such a law asserts the breakpoint that the state-structured
model derives, and Sections 3.4 and 3.5 show what that costs: at the sampling
designs tested there, $t_c$ cannot be estimated from the data, so a fitted value
records the optimiser's stopping point rather than a property of the organism.

Time to the limit of detection is finite and computable: 347 h for the slow
grower and 19 h for the fast one. It does not depend on the drug reaching the
dormant compartment at all. Setting the dormant kill rate to zero, so that
dormant cells are wholly refractory to the antibiotic, moves those times only to
370 h and 20 h, changes of 7% and 5%. The dormant pool in this model is not
cleared by being killed. It is cleared by waking into a compartment where killing
is fast, and the drug's action on dormant cells is close to irrelevant to how long
treatment takes.

The mechanism visible in the compartment trajectories is that the dormant pool
declines faster than its own kill rate alone would allow, because cells leaving
dormancy enter a compartment that is being killed rapidly. The effective
clearance rate of the dormant pool is approximately $k_{P\to S} + E_{\max,P}$
rather than $E_{\max,P}$, which is the algebraic root of the result in Section
3.3.

### 3.2 Resistance, tolerance and persistence produce distinct phenotypic signatures

Imposing each strategy on the same parameter set, one mechanism at a time,
produces three signatures that a laboratory can tell apart (Table 1, Figure 2).

| | MIC | MDK$_{99}$ | MDK$_{99.99}$ |
|---|---|---|---|
| wild type | 1.00× | 29.1 h | 67.6 h |
| resistant | **16.0×** | 1.00× | 1.00× |
| tolerant | 1.00× | **4.00×** | 3.67× |
| persistent | 1.00× | 1.02× | **3.65×** |

Resistance moves the concentration axis and nothing else. Tolerance moves both
duration endpoints together and leaves the concentration axis exactly where it
was, which is what dividing replication and both kill rates by a common factor
must do. Persistence moves the deep endpoint alone: MDK$_{99.99}$ rises
3.65-fold while MDK$_{99}$ changes by 2.5% and the MIC does not move at all.

The separation is clean rather than exact, and the 2.5% is the size of the
departure. A subpopulation large enough to dominate the tail is still small
enough that removing it barely changes the time to two-log killing — which is why
persistence is invisible to any assay reporting only MIC and a bulk kill rate,
and why the deep endpoint is the measurement that carries the information.

Three consequences follow for experimental design. Measuring MIC alone cannot
distinguish tolerance from persistence, since neither moves it. Measuring MIC and
MDK$_{99}$ separates resistance and tolerance but leaves persistence looking like
wild type. Only the addition of a deep endpoint, four logs rather than two,
resolves all three, and it requires the assay to have four logs of dynamic range
below the inoculum.

### 3.3 Growth regime determines the sensitivity landscape

The parameter that governs killing is not a fixed property of the model. It
changes with the growth regime of the organism, and it changes completely
(Figure 3).

For the slow grower, the resuscitation rate $k_{P\to S}$ carries 78.0% of the
first-order variance in time to the limit of detection, with a 95% bootstrap
interval of 0.640 to 0.916 and a total-order index of 0.799 (0.769 to 0.830). No
other parameter reaches a first-order index of 0.08, and interactions account for
2.3% of the variance. One parameter dominates, and the margin over the next is a
factor of ten rather than a rank ordering among comparable contributors.

For the fast grower, the same parameter carries essentially none of the
variance. Its total-order index is $2.3 \times 10^{-5}$ (bootstrap interval
$1.9$–$2.7 \times 10^{-5}$), four orders of magnitude below the dominant
parameters, and its first-order estimate is indistinguishable from zero, its
bootstrap interval spanning zero. What governs the fast grower is the maximum kill rate together with the
replication rate — and together is the operative word, since their total-order
indices are 0.819 (0.706 to 0.935) and 0.821 (0.713 to 0.942) against first-order
indices of only 0.169 and 0.136. Interactions carry 69.5% of the variance, which
is the share of the answer that a one-at-a-time analysis cannot see at all.

The mechanism is the one visible in Section 3.1. A dormant cell is hard to kill;
a dormant cell that resumes replication is not. Where the dormant compartment is
the rate-limiting reservoir, the rate of leaving it sets how long treatment takes,
and increasing the kill rate of dormant cells does comparatively little because
those cells are being cleared mainly by waking. Where the population barely
occupies that compartment, the same rate has nothing to act on.

Two things follow. The first is a prediction about transferability: an
intervention that shortens treatment by accelerating resuscitation should work for
a slow grower and have little effect on a fast one, and an intervention that
raises the kill rate should behave in the opposite way. The second is methodological. A
one-at-a-time analysis run on the fast grower would report the two dominant
parameters and miss two-thirds of the variance, and it would do so without any
diagnostic indicating that it had.

The slow-grower result holds for this model under these illustrative
parameters; carrying it to *M. tuberculosis* requires fitting to time-kill data,
and Section 4.1 sets out why the clinical evidence bearing on the question cannot
currently settle it either way. The contrast between the two regimes rests on
less. Both organisms were simulated at four times their own MIC, so the
difference between them is not a difference in exposure, and it is large enough
that no plausible reweighting of the parameter ranges removes it.

### 3.4 Which parameters can the data identify?

A model that fits is not the same as a model whose parameters are determined, and
the transition time of the closed-form biphasic law is a clear case of the
difference.

Fitting that law to synthetic time-kill data at four sampling designs — sparse
and dense, for both organisms — gives close fits in every case. Profile
likelihood on the same fits shows that $t_c$ is not practically identifiable in
any of them. The 95% likelihood interval reaches the edge of the searched range
in four of four designs, including the two dense ones, and the point estimate
lies on the optimiser bound in three (Figure 4). The Jacobian condition number at
the optimum reaches $5\times10^{17}$ for the closed-form law against roughly
$5\times10^{2}$ for the biexponential, fifteen orders of magnitude, which
indicates a rank-deficient design matrix rather than a difficult optimisation.

There is an algebraic reason. In a two-subpopulation system with dormant fraction
$f$ and rates $k_{\text{fast}}$ and $k_{\text{slow}}$, the crossover time is

$$t_c = \frac{\ln[(1-f)/f]}{k_{\text{fast}} - k_{\text{slow}}}$$

so $t_c$ is determined by the other three. Treating it as a fourth free parameter
is redundant under the two-subpopulation reading that motivates the equation in
the first place; read instead as a purely phenomenological piecewise form, $t_c$
is genuinely free and there is no redundancy, but then it is not the biological
transition time it is reported as. The redundancy is worth stating because it
explains the profile likelihoods above, but it is the identifiability result that
carries the practical weight: at the designs tested, whichever reading is
intended, the data do not determine $t_c$.

The claim here is about practical identifiability at the sampling designs tested,
which span the range time-kill experiments use. It is not a structural result: no
structural identifiability analysis was performed, and a design with much denser
sampling around the transition might determine $t_c$. The slow rate of the
biexponential, by contrast, is identifiable for the slow grower in both designs,
with closed intervals, and is not identifiable for the fast grower, where killing
is complete before the slow phase is observed. Which parameters a study can
estimate is a property of the design as much as of the model.

### 3.5 Model selection needs more than $R^2$

Across the same four designs, $R^2$ exceeds 0.9 for both the closed-form
biphasic law and the biexponential in three of the four, with a maximum
difference between the two models of 0.098 (Figure 5). The first of these is the
law whose second branch returns to the inoculum at the transition, raising the
modelled population by up to three log$_{10}$ at that point. A high $R^2$ neither
reveals that defect nor rules it out: the value is compatible with both models,
so it cannot be used to decide between them. Over the same fits the corrected
Akaike information criterion differs by up to 81.5.

The reason $R^2$ behaves this way on time-kill data is not subtle. The total sum
of squares is dominated by the spread of the data across orders of magnitude, so
almost any decreasing function fitted to a monotone decaying curve reproduces most
of it. It is not evidence that
a persistence model is correct, and it cannot choose between candidate killing
models. Information criteria, residual runs tests and profile
likelihood each separate the two models cleanly on the same data.

## 4. Discussion

### 4.1 Positioning the model within existing frameworks

The result of Section 3.3 sits in a literature that has approached the same
question from three directions, and it agrees with none of them completely.

**The algebra is not new.** Patra and Klumpp (2013) analysed a two-state
persistence model and showed that under stress the terminal decay rate approaches
the sum of the persister kill rate and the switching rate out of dormancy. When
the persister kill rate is small, that sum collapses to the switching rate alone,
which is the mechanism of Section 3.3 written down thirteen years ago. They did
not apply it to treatment duration, did not include a concentration-dependent
kill function, and performed no sensitivity analysis, so the quantitative
ranking, the organism dependence and the identifiability consequences are not in
their paper. But the mechanism is, and it should be read as their result rather
than ours. What we add is the demonstration that this term dominates the outcome
variance for one growth regime and is negligible for the other, which is a
statement about relative magnitude that their analysis does not make.

**The strongest clinical evidence points the other way, and cannot settle the
question.** Magombedze et al. (2021) fitted a two-subpopulation model to serial
sputum from 1,924 patients in the REMoxTB trial and ranked the kill rate of the
slow-replicating subpopulation first, at 100% variable importance, as the
determinant of time to extinction and therefore of required therapy duration.
That is a far stronger evidential base than anything in this paper, and it is
data rather than simulation.

It also cannot test the claim made here. Their two subpopulations are uncoupled:
the model contains no switching term, no resuscitation rate, and the word does
not appear. A parameter absent from a model cannot be ranked by an analysis of
that model, so the absence of resuscitation from their ranking is a property of
the model structure and not evidence about the biology. The two results are
compatible in the following sense: if the true system contains a resuscitation
term, fitting a model without one will load its effect onto whichever parameter
is structurally closest, and in their model that is the slow-phase kill rate.
Section 3.1 gives the reason to expect exactly that, since the effective
clearance rate of the dormant pool is approximately $k_{P\to S} + E_{\max,P}$ and
a model containing only the second will absorb the first into it.

We do not claim this is what happened. We claim that their design cannot
distinguish the two, and that distinguishing them requires fitting a model with a
switching term to data with enough resolution in the slow phase to identify it —
which Section 3.4 shows is a demanding requirement rather than a routine one.

**A competing explanation of the slow phase is better supported than persistence
in at least one dataset.** Martinecz et al. (2023) set up the same dichotomy
directly, parameterised both persistence and heteroresistance against rifampicin
early bactericidal activity data, and rejected persistence: the slow phase
accelerated with peak drug concentration, which switching-based persistence does
not predict because exit from the non-susceptible state is concentration
independent. Their persistence arm used in vitro replication rates that they
concede are unlikely to match the in vivo values, and their window is fourteen
days rather than the six-month duration horizon, but the argument is sound and
the prediction it tests is one our model also makes. A model of the kind
developed here should be confronted with that observation before its slow-phase
behaviour is believed.

**The qualitative claim is old.** That the subpopulation governing sterilising
activity consists of bacilli dormant much of the time but occasionally
metabolising for short periods is the stated conclusion of Dickinson and
Mitchison (1981), from experiments on why rifampicin sterilises better than
isoniazid. The idea that waking is what exposes these cells to the drug is
theirs. What Section 3.3 adds is the rate parameter and its rank against the
alternatives, not the mechanism.

**A parsimonious alternative dispenses with switching altogether.** Abel Zur
Wiesch et al. (2015) showed that chemical binding kinetics alone reproduce
persister-like biphasic killing, post-antibiotic growth suppression and
density-dependent effects, without any phenotypic switching term. If that account
is sufficient, the resuscitation rate of Section 3.3 is not a real quantity but a
lumped stand-in for binding and unbinding at the target. Our model cannot
adjudicate this, because it assumes the two-state structure rather than deriving
it. The distinguishing prediction is available, however: a binding-kinetics
account ties the slow phase to drug concentration, whereas concentration-
independent switching does not, and that is precisely the comparison Martinecz et
al. made.

Taken together: the mechanism is established, its dominance is not, the one large
clinical dataset that bears on it cannot test it, and at least one careful study
disfavours the persistence explanation of the slow phase in tuberculosis. The
contribution of Section 3.3 is therefore the organism dependence and the
quantification, offered as a hypothesis that specifies its own test, and not as a
settled account of what governs treatment duration.

### 4.2 What to measure

The analysis implies a short experimental programme, and the requirements are
stringent enough to be worth stating plainly.

*To classify an isolate*, three quantities are needed: the MIC, MDK$_{99}$, and
MDK$_{99.99}$. The first two are routine. The third is not, and Section 3.2
explains why it is indispensable — persistence moves only the deep endpoint, so
an assay reporting MIC and a bulk kill rate returns wild-type values for a
persistent isolate. The requirement is four log$_{10}$ of dynamic range below the
inoculum, with sampling that continues into the tail rather than stopping when
the count approaches the detection limit.

*To estimate a resuscitation rate*, the design must resolve the slow phase.
Section 3.4 shows that the slow rate is identifiable for a slow grower in both
designs tested and not identifiable for a fast grower, where killing completes
before the slow phase is expressed. For a fast-growing organism the parameter is
not estimable from a standard time-kill curve at all, and a reported value should
be treated accordingly.

*To compare organisms*, exposure must be matched to each organism's own MIC.
Section 2.6 gives the size of the error otherwise: the same absolute
concentration was 15.1 times the MIC of one parameter set and 5.0 times that of
the other, and a contrast computed that way carries the exposure difference
inside it.

*To choose between models*, report an information criterion and a residual
diagnostic. Section 3.5 shows $R^2$ above 0.9 for two models whose AICc differs by
81.5, so a reported $R^2$ conveys almost nothing about which model is right.

### 4.3 Scope and limitations

**The model applies to a constant concentration.** Every result here is computed
at fixed exposure. Extending to a pharmacokinetic profile requires replacing $C$
with $C(t)$, which the structure accommodates without modification, but the
sensitivity ranking is not guaranteed to survive that change: a fluctuating
concentration gives dormant cells windows in which to resume replication at low
drug levels, which should raise rather than lower the importance of the
resuscitation rate, but this is an expectation and not a result.

**There is no experimental data.** Parameter values are illustrative, chosen to
reproduce documented qualitative behaviour, and the species labels are a
convenience for discussing a slow and a fast growth regime rather than claims
about *M. tuberculosis* and *S. aureus*. No quantitative statement about either
organism should be drawn from them.

**The model is deterministic.** At the copy numbers that matter for genuine
sterilisation, extinction is a stochastic event, and a deterministic model cannot
give an extinction probability or a relapse risk. This is why the endpoint here is
time to the limit of detection and not time to sterilisation, and it is a limit on
the question the model can be asked rather than on the accuracy of its answer.

**Two compartments is a modelling choice.** Real populations are distributed in
dormancy depth rather than divided into two states, and a graded model would
replace the switching rates with a distribution. Two compartments is the smallest
structure that separates the three strategies, which is what this paper needs; it
is not a claim that bacteria have two states.

**The Sobol ranges are wide and uniform in the logarithm.** A $\pm50\%$
log-uniform range on every parameter treats them as equally uncertain, which they
are not. Narrowing the range on well-characterised parameters would raise the
apparent importance of the poorly-characterised ones, so the ranking should be
read as conditional on that choice.

## 5. Conclusion

Written as single exponentials with different rate constants, resistance,
tolerance and persistence are one mathematical object under three names, and no
measurement can separate them. Given two compartments and a concentration
response, they become three different measurements: a shift in concentration, a
shift in duration, and a shift in the deep killing endpoint. Each is obtainable
from a time-kill assay and a dilution series that laboratories already run,
provided the assay reaches four log$_{10}$ below the inoculum.

That is the practical content of this work. It converts a classification argued
from mechanism into three numbers that can be reported and compared between
laboratories. And once they are reported, the question of which parameter limits a
regimen becomes answerable per organism and per drug rather than assumed. The
analysis here shows the answer is not the same for a fast grower and a slow one:
the parameter worth measuring, and the intervention worth developing, differ by
growth regime. Whether that difference holds for real pathogens is now an
experimental question with a specified design, which is the most useful thing a
model without data can produce.

## References

All entries were verified against their PubMed record in September 2026. Digital object identifiers are given where one exists.

Abel Zur Wiesch P, Abel S, Gkotzis S, Ocampo P, Engelstädter J, Hinkley T et al (2015) Classic reaction kinetics can explain complex patterns of antibiotic action. Sci Transl Med 7:287ra73. https://doi.org/10.1126/scitranslmed.aaa8760

Balaban NQ, Helaine S, Lewis K, Ackermann M, Aldridge B, Andersson DI et al (2019) Definitions and guidelines for research on antibiotic persistence. Nat Rev Microbiol 17:441-448. https://doi.org/10.1038/s41579-019-0196-3

Beal SL (2001) Ways to fit a PK model with some data below the quantification limit. J Pharmacokinet Pharmacodyn 28:481-504. https://doi.org/10.1023/a:1012299115260

Brauner A, Fridman O, Gefen O, Balaban NQ (2016) Distinguishing between resistance, tolerance and persistence to antibiotic treatment. Nat Rev Microbiol 14:320-330. https://doi.org/10.1038/nrmicro.2016.34

Dickinson JM, Mitchison DA (1981) Experimental models to explain the high sterilizing activity of rifampin in the chemotherapy of tuberculosis. Am Rev Respir Dis 123:367-371. https://doi.org/10.1164/arrd.1981.123.4.367

Levin BR, Rozen DE (2006) Non-inherited antibiotic resistance. Nat Rev Microbiol 4:556-562. https://doi.org/10.1038/nrmicro1445

Lewis K (2007) Persister cells, dormancy and infectious disease. Nat Rev Microbiol 5:48-56. https://doi.org/10.1038/nrmicro1557

Magombedze G, Pasipanodya JG, Gumbo T (2021) Bacterial load slopes represent biomarkers of tuberculosis therapy success, failure, and relapse. Commun Biol 4:664. https://doi.org/10.1038/s42003-021-02184-0

Martinecz A, Boeree MJ, Diacon AH, Dawson R, Hemez C, Aarnoutse RE, Abel Zur Wiesch P (2023) High rifampicin peak plasma concentrations accelerate the slow phase of bacterial decline in tuberculosis patients: evidence for heteroresistance. PLoS Comput Biol 19:e1011000. https://doi.org/10.1371/journal.pcbi.1011000

Nielsen EI, Friberg LE (2013) Pharmacokinetic-pharmacodynamic modeling of antibacterial drugs. Pharmacol Rev 65:1053-1090. https://doi.org/10.1124/pr.111.005769

Patra P, Klumpp S (2013) Population dynamics of bacterial persistence. PLoS One 8:e62814. https://doi.org/10.1371/journal.pone.0062814

Regoes RR, Wiuff C, Zappala RM, Garner KN, Baquero F, Levin BR (2004) Pharmacodynamic functions: a multiparameter approach to the design of antibiotic treatment regimens. Antimicrob Agents Chemother 48:3670-3676. https://doi.org/10.1128/AAC.48.10.3670-3676.2004
