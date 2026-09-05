# A kill rate transfers between laboratories; a time to clearance does not

## 1. Introduction

Antibiotic killing is summarised in two currencies, and the field spends both as
though they were interchangeable. The first is a rate: how fast a population
falls while the drug is present, captured by the maximum kill rate and the
steepness of its concentration dependence (Regoes et al. 2004). The second is a
duration: how long the drug must be present before some threshold is crossed,
captured by the minimum duration for killing and by the time to a negative
culture. Rates populate pharmacodynamic models. Durations populate treatment
guidelines, trial endpoints, and the operational definition of tolerance itself
(Brauner et al. 2016; Balaban et al. 2019).

The two currencies are not equivalent, and the difference is not a matter of
units. A rate is estimated from the whole trajectory. A duration is estimated
from a single crossing of a fixed line. Everything that moves the line, or moves
the population's starting distance from it, enters a duration and leaves a rate
untouched. The starting density is the largest such quantity, and it is the one
a protocol is written to fix.

Whether protocols succeed in fixing it is an empirical question that has become
answerable. The ERA4TB consortium distributed one stock of *Mycobacterium
tuberculosis* H37Rv with one written protocol to six laboratories, had each run
the same time-kill exercise against moxifloxacin and isoniazid, and deposited
every colony count (van Wijk et al. 2023). Their own analysis reports that
baseline burden varied between laboratories while the net drug effect varied
less. That observation is the starting point of this paper rather than its
conclusion.

What has not been asked of that dataset is what its variation does to a duration
endpoint, and the reason is a methodological convention. Time-kill data are
censored: below some density the assay returns no count, and the limit depends
on how much culture was plated. The standard treatment is to exclude
below-limit readings from numerical analysis, which van Wijk et al. do
explicitly. For a rate this exclusion is a modest loss. For a duration it is
fatal, because a duration endpoint *is* the moment a culture crosses the
detection limit. Excluding the readings that define the endpoint removes the
endpoint. The question therefore cannot be asked without changing how the
censoring is handled.

Handling it properly turns out to be the whole analysis. Each ERA4TB sample was
plated at four volumes, so each carries four readings against four different
limits — 1.0, 2.0, 2.0 and 2.6 log10 CFU/mL for 100, 10, 10 and 2.5 µL. A blank
2.5 µL drop and a blank 100 µL quadruplicate are not the same event and do not
carry the same information. Judging every reading against the limit of its own
plating volume, and retaining it as censored rather than discarding it, makes
both currencies estimable on the same flasks: a rate by censored maximum
likelihood, a duration by survival analysis. That is what allows them to be
compared rather than assumed comparable.

We report that comparison here, and it is asymmetric. Under one protocol, one
strain and one stock, every laboratory produces a kill rate and half of them
produce no duration at all. The rates that survive span a few fold; the
durations are undefined in three of six laboratories, in every treatment arm.
Which laboratories can produce a duration is decided almost entirely by where
their cultures started. A duration endpoint measured across laboratories is
therefore, in substantial part, a measurement of their inocula.

We then ask how far this reaches beyond one exercise. Three further published
datasets are analysed with the same discipline: 217 clinical isolates carrying
both a minimum inhibitory concentration and a minimum duration for killing; 126
experimentally evolved clones carrying both a concentration endpoint and a
persistence endpoint; and a concentration-by-time grid on a slow grower in which
the same 32-fold dose range separates 48-fold at one week and 5-fold at two. The
pattern is consistent. Quantities defined by a rate travel between conditions
and laboratories. Quantities defined by a crossing do not, because they inherit
whatever the population brought with it.

Three things follow for practice, and they are the contribution.
A pharmacodynamic parameter taken from one study and used in another must be
checked for the axis it was fitted on: an E_max reported as a cumulative log10
reduction over a fixed window has no time in its denominator and is not a rate.
A comparison between regimens should be read at the window where the
concentration axis is still informative, which is early. And a duration endpoint
reported without its starting density is not interpretable, because the two are
not separable after the fact.

---

## 6. Discussion

### 6.1 What the six-laboratory exercise shows

The finding is a divergence between two summaries of the same flasks. At ten
times the minimum inhibitory concentration of moxifloxacin, all six laboratories
return a positive kill rate by censored maximum likelihood, and the estimates
span a few fold. Over the same flasks, three laboratories never recorded a
single culture below the detection limit in any arm, so for them the time to
clearance does not exist as a number. The two orderings do not
correspond. Ranked by starting density, the three lowest laboratories are exactly
the three that ever cleared and the three highest are exactly the three that never
did, without exception. Ranked by kill rate there is no such correspondence: the
laboratory with the highest starting density kills faster than four of the other
five and never clears, while the laboratory with the slowest rate of all and one
that clears readily sit on opposite sides of the outcome. Clearance is ordered by
where the cultures began; it is not ordered by how fast the drug killed them.

The mechanism is not subtle once the endpoints are separated. Starting density
classifies which flasks ever became undetectable with an area under the curve of
0.97. In proportional-hazards models fitted on laboratory alone, three
laboratories differ significantly from the reference; adding starting density as
a covariate removes that difference for all three. One laboratory remains
distinguishable after adjustment, and it is distinguishable in its rate as well,
which is the behaviour expected of a laboratory that genuinely kills faster
rather than one that merely started lower.

Two estimators are reported because the censoring is the difficulty rather than
an aside. A Tobit model and multiple imputation from the truncated distribution
make different assumptions about what happened below the limit and never differ
by more than 0.003 log10 per day. The conclusion is therefore a property of the
data and not of the estimator.

The clinical reading is direct. Time to culture conversion is the endpoint on
which tuberculosis regimens are compared, and it is a duration. These data show
what a duration does when the starting burden is not fixed, in the most
favourable circumstances imaginable: one strain, one stock, one written
protocol, and laboratories that agreed in advance to follow it.

### 6.2 Relation to the analysis by van Wijk and colleagues

Our reading and theirs agree where they overlap and separate on one
methodological choice, which we state rather than leave to inference.

They report the inoculum spread themselves, and we reproduce their figure
exactly from the deposited file. They also conclude that baseline burden varied
between laboratories while net drug effect varied less. That conclusion
anticipates the first half of ours and belongs to them.

The separation is that they excluded every reading outside the quantification
limits from numerical analysis. That is a defensible reporting decision and we do
not criticise it; it simply forecloses the question asked here, because it
removes the observations from which a duration endpoint is constructed. Keeping
those readings as censored is what makes both currencies estimable on the same
flasks. What is new here is therefore not that burden varies, but that their
reproducible net effect and their unreproducible clearance pattern point in
opposite directions, and that half the laboratories cannot produce the second
quantity at all.

### 6.3 Resistance and tolerance as separate axes

That the minimum inhibitory concentration and the minimum duration for killing
are separate axes is the premise of the framework that defines them, not a
discovery (Brauner et al. 2016). The contribution here is a bound rather than a
claim of independence.

In 217 clinical isolates the deposited file supports twenty-four comparisons
between the two axes: six duration endpoints at two culture ages, crossed with
four strata. Four reach nominal significance where 1.2 are expected by chance,
and none survives control of the false discovery rate. The four also point in the
direction a shared mechanism does not predict, a higher inhibitory concentration
accompanying a *shorter* duration, and they concentrate in the deepest endpoint,
where ninety per cent of isolates sit at the assay ceiling after fifteen days of
prior culture and ninety-five per cent after sixty. We report the
correlation each stratum could have resolved, so the null is bounded rather than
asserted.

The same question in 126 experimentally evolved clones, which share an ancestor
and evolved in parallel under known conditions, returns the same answer within
every stratum. Two designs, two organisms, one clinical and one experimental,
and in each the axes carry separate information within the resolution available.

### 6.4 The window in which concentration is informative

That a late endpoint carries less information about dose than an early one is
established. Firsov et al. (1997) reported the dependence of killing and regrowth
parameters on the observation interval; Jindani et al. (2003) established the
tuberculosis version in patients with coefficients fitted per window; and
Srivastava et al. (2016) fitted maximum effect per sampling day in this organism
and drug class, reaching a different conclusion about the second week than the
one our data suggest.

What we add is the arithmetic on one concentration range in a slow grower.
Across a 32-fold range of apramycin, survivors separate 6.9-fold at day three,
48.2-fold at day seven and 5.2-fold at day fourteen. An experiment read at
fourteen days would report this drug as insensitive to a 32-fold change in dose.
The dose information is not absent from the system; it is absent from the
endpoint.

Fitted per interval on a replicate-level bootstrap, the concentration slope is
positive early, indistinguishable from zero in the middle window, and negative
late, with the early-versus-late contrast firm and the early-versus-middle
contrast not. We do not claim the late sign. By day fourteen the highest arm
sits at 65 CFU/mL against a limit the source does not state, and censoring of
that arm would produce a negative slope whether or not one exists.

### 6.5 Which published parameters may be transferred, and on what axis

A maximum effect reported as a cumulative log10 reduction over a fixed window
has no time in its denominator. It cannot be divided by the window to yield a
kill rate, because its plateau is set by the exhaustion of the inoculum rather
than by saturation of the drug effect. A Hill exponent fitted alongside such an
endpoint measures the geometry of the assay — the inoculum, the window length,
the detection limit — and changes when any of those change with nothing about
the drug changing.

This rule resolves an apparent conflict rather than adjudicating it. Rifampicin's
Hill coefficient is reported near 0.5 in one study and near 1.9 in another. They
are exponents on different independent variables fitted to different dependent
variables over different windows, and their difference carries no
pharmacodynamic information. Applying the rule to the mycobacterial literature
leaves few admissible values, and those that remain sit one to three orders of
magnitude away from the constants in routine use in models built on
fast-growing organisms.

### 6.6 Scope and what should be measured next

The limitations that matter here are not gaps in what was done but measurements
the field should now make, and each has a specific design.

**The starting density should be reported with every duration endpoint, and
adjusted for.** These data show it is not fixed by a protocol written to fix it,
and that it decides whether a duration exists. Reporting it costs nothing and
makes duration endpoints comparable between laboratories for the first time.

**Time-kill studies should record and publish their limit of quantification.**
Four of the studies examined here do not state one anywhere. Without it, a
censored observation cannot be distinguished from a measured one, and every
analysis downstream inherits the ambiguity. In this dataset the limit is a
property of the plated volume and is recoverable; in most it is not.

**A dose-switching arm belongs in the standard time-kill design.** The
concentration axis is informative early and not late, which invites a regimen
that begins high and steps down. No published grid tests it, because no arm ever
changes concentration. The experiment is small: the existing grid plus three
arms that switch at day three and day seven, against constant high and constant
low controls at matched cumulative exposure. Four flasks would settle whether
the early rate can be bought and the late cost avoided.

**Pharmacodynamic parameters should be published with the physiological state
they were measured in, as a required field.** The maximum kill rate and the
ratio that sets the shape of the concentration-response curve both move with
condition, drug and observation window. A parameter table that does not record
the state is not transferable, and the practice of transferring such values is
what places routine constants orders of magnitude from any measured
mycobacterial value.

**The falsification test for the central argument should be run.** de Steenwinkel
et al. (2010) report an aminoglycoside as equally effective irrespective of
metabolic state, which is the opposite of the condition dependence reported
here. That comparison crosses a concentration series with a metabolic contrast
in this organism and is the sharpest available test of whether the pattern
described in this paper generalises. It should be repeated with censoring
handled as censoring.

### 6.7 Conclusion

A kill rate and a time to clearance are not two views of the same quantity. One
is a property of the drug acting on a population in a state; the other is that
property convolved with where the population began and with where the assay
stops seeing it. Under a single protocol, a single strain and a single stock,
the first is estimable everywhere and the second is undefined in half the
laboratories that tried. Reporting the starting density, publishing the
quantification limit, and reading dose comparisons in the window where the
concentration axis still carries information would make duration endpoints mean
between studies what they are already assumed to mean.
