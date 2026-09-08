---
title: "The detection floor bounds what a time-kill assay can report: minimum duration for killing and log-reduction endpoints in five published deposits and a prospective test"
short_title: "The detection floor bounds time-kill endpoints"
article_type: "Research Article"
keywords:
  - time-kill assay
  - limit of quantification
  - minimum duration for killing
  - antibiotic tolerance
  - colony counting
  - censored data
  - inoculum effect
---

# The detection floor bounds what a time-kill assay can report: minimum duration for killing and log-reduction endpoints in five published deposits and a prospective test

**Author:** Vahhab Piranfar¹

¹[department, institution, city, country — to be inserted]

ORCID: [0000-0003-3653-5739](https://orcid.org/0000-0003-3653-5739)

**Correspondence:** Vahhab Piranfar, vahab.p@gmail.com

**Figures:** 4 | **Tables:** 3 | **Boxes:** 1 | **Supplemental tables:** 22

---

## Abstract

A negative culture after antibiotics has never meant sterility, so tolerance is
scored by how far the population fell: the minimum duration for killing. That
endpoint is a fraction of the starting count, so the inoculum should cancel. It
does in the definition, and fails once killing reaches the assay's floor. Five
published time-kill deposits are reanalysed, and one experiment tests it
prospectively.

Two boundaries follow from the definitions. For a floor *L*, the smallest
reportable positive count, a *q*-log endpoint is observable only above
*L*·10^*q*; above *L*/*c*₁, with *c*₁ the lowest class threshold, a censored
reading is compatible only with the lowest class. Reaching the floor is the
drug's doing; the label it then permits is not.

Of 217 *Mycobacterium tuberculosis* isolates classified for rifampicin
tolerance, 33 lack the range for the 99.99 per cent endpoint used, and all 33
are recorded as failing. Of eighteen read at the floor, twelve admit one class
and six admit two. The label tracks growth state; isoniazid resistance does not,
and most of it travels through a ten-fold lower inoculum, the denominator the
label is cut on.

Under one written protocol, six laboratories differed by 4.40 log10 in
demonstrable kill depth. Prospectively, *Escherichia coli* ATCC 25922 at the
standard inoculum could report 3.71–3.93 logs at 10 µL and 4.88–5.05 at 100 µL;
at a cut of 10⁻³, nine of 54 sample-times took two different labels from one
culture. A tolerance call reported without its starting density and assay
floor cannot be interpreted.

**Keywords:** time-kill assay; limit of quantification; minimum duration for
killing; antibiotic tolerance; colony counting; censored data; inoculum effect

## Introduction

Every clinical microbiologist is taught that a culture taken after antibiotics
have started is not evidence of sterility. It is why blood cultures are drawn
before the first dose. A drug suppresses growth, injures cells sublethally,
carries over into the medium, and drives the population beneath what the plate
can see; the plate then reports absence, and absence is not what happened. The
rule is old, it is correct, and nobody disputes it.

Tuberculosis makes the rule expensive. Regimens run for four to six months (1), the
compounds that could shorten them must be selected from in vitro killing
experiments, and the phenotype invoked to explain why treatment takes so long —
tolerance, the capacity of a genetically susceptible population to survive
exposure that should kill it — is defined by how long killing takes. A phenotype
defined by a duration is a phenotype defined by exactly the observation the old
rule warns about.

The field's response was not to ignore the warning but to engineer around it.
Rather than asking whether a culture went negative, the modern definition asks
how many logs the population fell: the minimum duration for killing, MDK, is the
time to a specified fractional reduction — 90, 99 or 99.99 per cent — and it is
proposed as the tolerance counterpart to the minimum inhibitory concentration
(2, 3). The choice of a *fraction* is the
whole point. A ratio to the starting population is scale-free: on a log-linear
decline at rate *b*, the time to a *q*-log reduction is *q/b*, and the starting
density cancels. By construction, MDK cannot be contaminated by how much culture
went into the tube. That is the property it was built to have.

We report that the property holds only in the estimand, not in the measurement,
and that the difference is consequential. A *q*-log reduction can be estimated
only if *q* logs are visible, and what is visible is bounded below by the assay's
floor. Writing *L* for that floor and *N₀* for the starting density, an isolate
has

    headroom  h = log10(N₀ / L)

and no experiment can demonstrate a reduction deeper than *h*, however completely
the drug worked. Where *h* < *q* the endpoint is unreachable before the drug is
added. Worse, when the final reading sits *at* the floor, the recorded fraction
is not a measurement at all but the ratio *L/N₀* — the most starting-density-
dependent quantity available. The metric designed to be inoculum-independent
becomes a pure inoculum readout precisely at the depth where tolerance is scored.

The two failures are different in kind, and this paper keeps them apart. Whether
an endpoint is reachable at all is settled by the assay geometry before the drug
is added, since *h* depends only on the starting culture and the floor. Whether a
reading that has reached the floor can be classified is settled by the geometry
too, but only once the drug has driven the population down to it: reaching the
floor takes a reduction of the isolate's entire headroom, and that is the drug's
doing.

The bound is already in the papers that defined the assays. Vijay and colleagues,
introducing the most-probable-number MDK for rifampicin, treated an MDK99.99
longer than ten days as high tolerance beyond the **time** window of the assay,
not as a statement about the count floor (4). In the 217-isolate
classification that follows from that assay they report that MDK99.99 at 15 days
of recovery could be calculated for only 22 of 209 isolates and that the rest lay,
in their words, "beyond the assay limits" (5). The ERA4TB consortium requires below- and
above-quantification-limit flags together with the limit of quantification, and
notes that pharmacometric models can use those flags (6); the same
six-laboratory comparison then excluded both from its numerical analysis. Their
2025 protocol states the geometry of the pipette explicitly: a 2.5 µL drop has a
limit of detection above 2.6 log10 CFU/mL, and a lower limit requires a larger
plated volume (7). Independently, a 2025 pharmacokinetic-pharmacodynamic
analysis of hollow-fibre CFU series showed that censoring counts below 10 CFU
biases regimen ranking (8), and a within-host tuberculosis tolerance study
chose a shallower MDK threshold specifically so that more isolates could enter
the analysis (9).

The closest statement of the bound is in the framework's own methods paper, and
we claim no priority over it. Brauner and colleagues, presenting a direct
measurement of tolerance that deliberately avoids time-kill curves, scale the
inoculum to the endpoint being measured: a hundred bacteria per well to determine
MDK99, a thousand for MDK99.9, and so on (3). That is the reachability
inequality of this paper, with the floor idealised at one cell per well and a
presence-or-absence readout in place of a count. What has not been done is to
carry the rule back into plate-count time-kill, where the floor is not one cell
but a concentration fixed by the plated volume — 10 to 400 CFU/mL across the
deposits reanalysed here — and must therefore be measured per sample rather than
assumed; nor to ask what the published record looks like where the rule was not
applied.

The requirement is older still, and it is quantitative. NCCLS M26-A ties the
plated volume to the endpoint, requiring that after the defined 99.9 per cent
killing at least ten colonies remain to be counted, and separately requires the
smallest accurately detectable count to be established by serial dilution of a
known inoculum (10). What has happened since is that the endpoint moved and the
rule did not travel with it. The persistence field's own consensus guideline
makes the time-kill assay the starting point for identifying persistence and
catalogues at length what can go wrong with it — resistant mutants,
heteroresistance, drug degradation, adhesion to the vessel, washing and recovery
conditions, delayed colony appearance, culture density, inoculum history — and
raises neither the limit of detection, nor the plated volume, nor how deep a
reduction the assay can report (11).

None of these converts a floor-level reading into the classification rule it
becomes: when the last count sits at *L*, the recorded fraction is *L*/*N*₀, and
the low, medium or high label is then a cut on starting density. That is the gap
this paper fills. Two further failures have to be kept distinct from it. A
duration ceiling — the assay stopped looking — is not a count floor, which is the
plate being unable to see; and recording a below-limit flag is not the same as
scoring a duration from the points so recorded.

This is testable rather than arguable, because one published deposit assigns the
tolerance phenotype itself. Vijay and colleagues (5, 12) scored 217 clinical
*Mycobacterium tuberculosis* isolates as having low, medium or high tolerance to
rifampicin, and deposited alongside each call the starting most probable number,
the growth rate, the isoniazid susceptibility and the killing readings the call
was built from. The classification, the inputs to it, and the assay geometry that
bounds it are all in the same file.

The aim of this study is to characterise the range over which a log-reduction
tolerance endpoint is measurable at all, and to establish whether real isolates
have been assigned tolerance phenotypes from outside it. Two boundaries on the
starting density follow from the definitions — one deciding whether an endpoint
is reachable, the other whether a floor-level reading identifies a class — and
both are computed from quantities a time-kill protocol already records, so
neither asks a laboratory to measure anything new. We then test the hypothesis
that a deep log-reduction endpoint is inoculum-dependent through its
observability even though it is inoculum-independent in its definition, using the
classification and the assay geometry of 217 clinical isolates; we then ask what
the resulting phenotype tracks — drug susceptibility, or the physiological state
of the culture. Two
further deposits establish that the same arithmetic governs killing experiments
where inoculum is controlled by protocol rather than by clinical accident: a
six-laboratory consortium exercise distributing one strain under one written
protocol (6, 13), and a concentration-by-time grid in the same organism (14, 15). From the first
we also ask whether a faster-killing flask reliably crosses the floor sooner, and
from the second whether a late endpoint can erase a dose difference that an early
one resolves. A fourth deposit (16, 17), held out until every boundary was fixed, tests
whether the boundaries locate the same depth in an experiment they were not built
from. Finally we ask whether the concentration and duration axes are separate in
these files, which is the premise the framework defining them rests on. All five
deposits are published and openly licensed, and none was generated for this study
(Table 1). The two boundaries are then tested forward rather than backward, in a
prospective experiment built to break them, with every prediction written down
before a plate was counted. If the hypothesis holds, a tolerance call reported without its starting density
and its assay floor cannot be interpreted, and the phenotypes assigned in its
name are, in part, a record of how the assay was set up.

---

**Box 1. Four numbers that score an MDK.** *N₀* is the starting density. *L* is
the smallest positive count the method can report — one colony in a plated volume
*v* µL is *L* = 1 000/*v* per mL, and an MPN series uses the lowest table rung (18, 19).
Headroom is *h* = log10(*N₀*/*L*). A *q*-log endpoint is legal only if *h* ≥ *q*,
which is the same as seeding at or above *L* · 10^*q*. If the last reading sits
at *L*, the recorded fraction is *L*/*N₀*: an upper bound, not a measurement.

| Culture | *N₀* (per mL) | *L* (per mL) | Headroom | Legal endpoints | If the last reading is at *L* |
| --- | ---: | ---: | ---: | --- | --- |
| Thin clinical MPN | 23 000 | 23 | 3.00 | 90%, 99%, 99.9%; not 99.99% | Fraction 10⁻³. Low and medium both compatible: the rule cannot choose. |
| Adequate clinical MPN | 230 000 | 23 | 4.00 | all four, including 99.99% | Fraction 10⁻⁴. Only low is compatible. |
| 100 µL plate | 10⁵ | 10 | 4.00 | through 99.99%; not a 5-log call | Fraction 10⁻⁴. A 5-log MDK needs *N₀* ≥ 10⁶. |
| 10 µL drop, same *N₀* | 10⁵ | 100 | 3.00 | through 99.9%; not 99.99% | Fraction 10⁻³. The pipette, not the isolate, removed one log. |

The first two rows are the two starting densities that recur in the clinical
deposit analysed below, and Section 2 reports what became of the isolates that
began at each. The last two are why a written protocol does not standardise
measurable depth: the plated volume sets *L*. To make both a four-log endpoint
and a low class identifiable against *L* = 23 per mL, seed above
*L* · max(10⁴, 1/*c*₁) = 230 000 per mL, or choose a shallower endpoint.

Two of the claims this arithmetic supports are not testable and should not be
read as though they were. If the last reading sits at the floor, the recorded
reduction cannot exceed *h*, because a deeper one would require a count below
*L*. And the recorded fraction is then *L*/*N*₀, so its correlation with *N*₀ is
−1 whatever the numbers are, including random ones. Both follow from the
definition of a censored reading, and neither is evidence about a drug.

What is testable is what happens when one sample is plated at two volumes under a
fixed class threshold. If both readings sit at their own floors the labels are
*L*₁/*N*₀ and *L*₂/*N*₀, and they differ only when those two fractions fall on
opposite sides of the cut — which is again arithmetic. The empirical quantity is
how often a real experiment lands in that window. It could be none of the time.


---

## Results



### 1. Observable kill is bounded by the assay floor

The most probable number readings take the discrete values of an MPN table (18, 19), and
the day-5 column does not taper towards zero but stops. Eighteen isolates sit at
exactly 23 per mL in the 15-day panel and six in the 60-day panel, with no value
anywhere in the file below it (Fig. 1A). That is the behaviour of a floor rather
than of a tail, and it is treated as one throughout.

The deposit states no limit of quantification (12), so that value is inferred and the
inference is quantified rather than asserted. A discrete posterior over the
most-probable-number rungs at or below the observed minimum places 95 per cent
support on 9.2 to 23 per mL, a span of 0.40 log10 — narrow enough that the class
labels of Section 3 are computed rather than refused (Table S1). Where a deposit
gives no such evidence, those labels are refused instead of reported.

The deposit carries a second classification, scored at day 2, and it sits on a
different floor. The day-2 column bottoms out at 230 per mL with eighteen
readings on it, so *L* = 230 there, and the day-2 class thresholds — which the
source does not state — are recovered the same way as the day-5 ones: the cuts
10⁻² and 10⁻¹ reproduce all 203 usable day-2 classes with no disagreement, one
decade shallower than at day 5. Both the floor and the lowest threshold shift by
a factor of ten, so the identifiability boundary is unmoved: *N*_id = 230/10⁻² =
23 000 per mL, the same value as at day 5. The reachability boundary does move,
by a decade, and the consequence is large: 121 of 203 isolates lack the headroom
for a four-log reduction against the day-2 floor, where 31 of those 203 isolates
lack it against the day-5 floor. Eighteen day-2 readings rest on their floor,
eleven with a single
compatible class and seven with more than one. At 60 days no pair of decade cuts
reproduces the day-2 classes (109 of 197), so that rule is not a decade threshold
on the recorded fraction and no day-2 accounting is offered for it.

The consequence is that each isolate carries a fixed budget of observable
killing. At 15 days of prior culture the starting densities span 3.36 to 7.79
log10, so headroom spans 2.00 to 6.42 log10 (Fig. 1B, Table 2); both spans are
the same 4.42 log10, and the fold figures quoted throughout are ten raised to the
unrounded difference rather than to the displayed one. Against that budget the
three deposited endpoints behave very differently. No isolate lacks the headroom
for a 90 or a 99 per cent reduction: 0 of 217 in both cases. **Thirty-three of
217 isolates — 15.2 per cent — lack the headroom for the 99.99 per cent
endpoint**, which is to say that a four-log reduction was unobservable for them
before rifampicin was added. Two of those 33 carry a fourth label that
the deposit writes literally as "MDR", conventionally multidrug-resistant, and
that is unordered with respect to the other three, so no ordered analysis can
place it (Table S2); the same count over the 203 isolates with an ordered label
is therefore the 31 quoted above.

All 33 are recorded as not having reached it — at the **assay ceiling**,
which is a census of the affected isolates rather than an estimate, and it is the load-bearing observation. The ceiling is a
different censoring mechanism from the floor and should not be read as its
mirror. The floor censors the measurement scale: a count below *L*
is not reported as a count. The ceiling censors time: the killing assay runs six
days, so an isolate that has not reached its endpoint by then is recorded at the
last day rather than at the day it would have reached. One is a limit on how deep
the assay can see, the other on how long it looks. Among the 184 isolates that
did have four logs of headroom, 162 are also at the ceiling, 88.0 per cent.

No p-value is attached to that contrast, and the reason is worth stating rather
than hiding in a caveat. An isolate short of four logs of headroom cannot record
a four-log reduction: the 0 of 33 cell is fixed by arithmetic, not by biology, so
the null of independence between ceiling status and headroom is false before any
data are seen. A test of an impossible null returns a number, and that number
means nothing. The census is the finding: every isolate that could not reach the
endpoint is recorded as not having reached it, and 88.0 per cent of those that
could are recorded the same way. The deepest endpoint is therefore the only one at risk, and it is the
one the tolerance classification is built on.

### 2. Identical floor observations received different tolerance labels

The deposited tolerance level is a threshold on the recorded surviving fraction,
with no overlap between classes. The thresholds themselves are not deposited;
they are recovered here, and the data pin them only to the gaps between classes:
at day 5 and 15 days of prior culture, low tolerance covers fractions below
10⁻³, medium covers 10⁻³ to 10⁻², and high exceeds 10⁻². Applying those cuts reproduces every usable class in the file,
203 of 203 (Table S3) — usable meaning the 203 of 217 isolates whose label is
one of the three ordered classes, the other 14 carrying a fourth, unordered
category, the "MDR" label above, that no ordered analysis can place (Table S2) — so what follows is an argument about the fraction the
assay recorded and not about an independent clinical judgement.

Eighteen isolates ended at the floor. They share one reported floor-level
observation, but their true final counts are unknown below the assay floor, so
the assay cannot distinguish their final viable burdens within the censored
region. That is not the same as saying they were killed to the same degree, and
the difference matters. Their starting densities span 265-fold, from 23 000 to
6.1 × 10⁶ per mL, so the same terminal reading implies a different range of
compatible fractional reductions in each: an isolate that began at 23 000 has
demonstrated at least a 3.00-log reduction, one that began at 6.1 × 10⁶ at least
5.42 logs, and in either case the true reduction may be anything from that bound
down to complete kill. What the deposit records instead is a single number per
isolate, *L*/*N₀*, and those recorded fractions span 265-fold, from 3.8 × 10⁻⁶ to
1.0 × 10⁻³ — exactly the span of the starting densities (Fig. 1C), because that
is what the ratio is. They are upper bounds on survival, not measurements of
it.

The tolerance labels assigned to them differ. Six isolates that began at 23 000
per mL received a fraction of 10⁻³ and were classified **medium** tolerance;
twelve that began at 230 000 or above received 10⁻⁴ or less and were classified
**low**. Predicting the label from the starting density alone, with a single cut,
reproduces all eighteen (Table 3). That is a statement about the classification
step and not about the killing: conditional on a reading censored at the floor,
the starting density fixes which label the published rule is able to return.

The question this raises is not whether those labels are wrong but which labels
the published rule could have returned once the reading came back at the floor. A
censored reading places the true count somewhere between zero and *L*. Sweeping
the true count across that range and applying the deposited thresholds gives the
set of classes compatible with the observation. For the twelve isolates that
began at 230 000 per mL or above, every count the assay admits yields a fraction
below 10⁻³, so **low** is the only class compatible with a floor-level reading.
For the six that began at 23 000, the compatible set spans the low–medium
threshold and the rule cannot choose between two classes.

Three questions have to be kept apart here, and the rest of this paper keeps them
apart. Whether a culture reaches the floor at all is a question about the drug:
rifampicin has to reduce the population by that isolate's entire headroom for it
to happen, and the starting density does not by itself decide it. Which label the
rule assigns once the reading is censored is a question about arithmetic: there
the starting density determines the compatible set, and for twelve of these
eighteen that set has one member. How far the population actually fell is a
question the assay leaves open, since the true count lies anywhere below *L*. The
first is biology, the second is bookkeeping, and the third is unmeasured.
Conflating them is the error this paper is about.

So for twelve of the eighteen the recorded label carries no information beyond
the fact that the reading was censored, and for six it is not determinate at all.
None of the eighteen is a measurement of the surviving fraction.

Sorting every call in the panel this way separates the labels the assay measured
from the labels the censoring rule fixed (Table 3). At 15 days of prior culture,
185 of 203 calls rest on a reading above the floor and are measured; for 12 the
reading is censored and only one class is compatible with it; for 6 the reading
is censored and more than one class is compatible. At 60 days the counts are 191,
6 and none, because the cultures are denser and few readings reach the floor.

The larger effect is at the deeper endpoint and it falls unevenly on the groups a
study would compare. The 99.99 per cent endpoint is unreachable for 22 of 84
isoniazid-resistant isolates, 26.2 per cent, against 9 of 119 susceptible ones,
7.6 per cent (Fisher exact p = 0.00056 (20)); the remaining two of the 33 fall outside
that contrast, being MDR. Their median headroom differs by a full log, 4 against
5.
A comparison of tolerance between those groups is therefore in part a comparison
of how well each group could be measured, which is the disposition the previous
section quantifies.

### 3. The affected isolates are named before the drug is added

Sections 1 and 2 counted isolates. The two boundaries derived in the Methods,
under *Dynamic range, and the two boundaries it sets*, do more than that: given only the floor, the class thresholds and each isolate's
starting density, they say in advance which isolates are affected, before any
day-5 reading is used.

For this assay *N*_reach = 23 × 10⁴ = 230 000 per mL and *N*_id = 23/10⁻³ =
23 000 per mL. Applied to the 15-day panel, the first predicts 33 isolates unable
to reach the 99.99 per cent endpoint, and the second predicts that of the
eighteen isolates whose reading rests on the floor, twelve have only the lowest
class compatible with that reading and six have more than one. Those are the
three counts Sections 1 and 2 report.

Neither boundary predicts which isolates reach the floor; that depends on what
rifampicin does. Both predict what a reading at the floor can be made to mean
once it happens, and there the agreement with the deposit is exact isolate by
isolate: the set the algebra says has a single compatible class and the set the
deposit records in the lowest class are the same set.

That agreement is an identity rather than a passed test, and saying so is the
honest way to report it. Once the label is a cut on the recorded fraction
(Table S3) and every floor reading has a numerator of exactly *L*, the class of a
floored isolate is a function of *N₀* alone, so the algebra cannot disagree with
the deposit. What could have failed, and did not, is the premise: that the three
classes separate cleanly on the recorded fraction at all, in 203 of 203 calls.

The resolution of the agreement also has to be stated. Among the eighteen the
starting density takes only five values — 23 000 for six isolates, then 230 000
for eight, and 610 000, 2.3 × 10⁶ and 6.1 × 10⁶ for one, one and two — and **no
isolate lies strictly between *N*_id and *N*_reach**. Any cut placed anywhere in
that decade reproduces the same twelve-six split, so the split locates the
boundary only to within an order of magnitude and is not by itself a sharp test
of where it sits.

What is sharp is the boundary case, and it is the part of this section that
discriminates. Six isolates sit at exactly 23 000 per mL, which is *N*_id itself,
so for them *L*/*N₀* equals *c*₁ exactly, the interval [0, *L*/*N₀*] touches the
threshold from below and spans two classes, and the strict inequality fails.
Those six are precisely the six the deposit records as medium rather than low. A
rule written with the inequality the other way would have called all six low and
been wrong six times out of six. That is a test the arithmetic could have failed
and did not, and it is what licenses using the boundary in advance: given a
floor, a set of thresholds and a starting density, the affected isolates can be
named before any reading is taken.

The empirical findings are therefore consequences of the definitions rather than
properties of this deposit, and the claim is a prediction that any dataset
reporting a starting density, a floor and a threshold classification can be
checked against.

### 4. The classification tracks growth; the resistance association is not separable from the inoculum

Eight association tests are available between the deposited label and its
candidate determinants — two predictors, at two culture ages and two endpoint
depths — and they are corrected as one family. Two survive (Table S4).

The label tracks the **growth rate** of the isolate: slower growth accompanies a
higher tolerance class, and the association survives adjustment for starting
density (OR 1.096 per day of time to OD 0.4, 95 per cent CI 1.032 to 1.164,
p = 0.0030, n = 202; unadjusted OR 1.126, 1.062 to 1.193). It also tracks
**isoniazid resistance**, until the starting density enters the model.
Unadjusted, resistant isolates have 2.32 times the odds of a higher tolerance
class (95 per cent CI 1.30 to 4.12, p = 0.0042); adjusted for starting density
the odds ratio falls to 1.31 (0.67 to 2.57, p = 0.42) and the interval no longer
excludes one. We describe this as attenuation rather than elimination. Starting
density is the strongest term in the file: each ten-fold increase in the starting
most probable number halves the odds of a higher tolerance class (OR 0.480, 0.340
to 0.677, p = 2.9 × 10⁻⁵).

The mechanism of that attenuation is measurable. Isoniazid-resistant isolates
enter this assay at 5.36 log10 against 6.36 for susceptible isolates, ten-fold
lower (Mann–Whitney p = 9.1 × 10⁻¹⁴) (21), and 26.2 per cent of them lack the
headroom for the deepest endpoint against 7.6 per cent of susceptible isolates
(Section 2). They are one log poorer in observable killing before the experiment
begins.

A percentage attenuation is a descriptive ratio, not an estimand, so the path is
also estimated directly. Decomposing the total effect of resistance on the
tolerance class into a path through log10 starting density and a direct path
gives, on the 203 isolates with a usable class rather than the 202 the
association family retains, a mediated effect of +0.166 classes (bootstrap
95 per cent CI +0.067 to
+0.279) against a direct effect of +0.091 (−0.116 to +0.287), so about 65 per
cent of the association travels through the inoculum and the direct path covers
zero. Restricting to baseline isolates leaves the mediated path intact (+0.159,
+0.053 to +0.295), and binary collapses of the outcome agree (Table S5). Two things bound that estimate, and neither is a formality. It rests on
sequential ignorability, which no observational file can establish: a residual
correlation between the mediator and outcome errors of about −0.24 would nullify
the point estimate, and one ordinary measured covariate already moves it about
forty per cent of that way. More fundamentally, the mediator here is the
denominator of the ratio the outcome is cut on. The tolerance class is a
threshold on *N*₅/*N₀*, so a decomposition that routes resistance through *N₀* is
in part recovering the censoring arithmetic this paper is about rather than a
biological pathway from resistance to tolerance. That is not a reason to discard
the estimate — it is the quantity a reader wants, because it says how much of the
association is carried by the label's own denominator — but it is a reason not to
read it as a mechanism. Only a design that fixes the inoculum separates the
two.

That last objection can be tested rather than merely conceded, because it is
true of a subset one can name. The recorded fraction is *L*/*N₀* exactly for the
eighteen isolates whose day-5 reading sits at the floor, and for no others: in
the remaining 185 the numerator was measured and is free to move independently
of *N₀*. Refitting on those 185 alone, the mediated path does not weaken but
strengthens, to +0.227 classes (+0.118 to +0.348), while the direct path
collapses to +0.008 (−0.197 to +0.208) and the proportion mediated rises from
0.65 to 0.96. Deleting exactly the isolates for which the criticism holds leaves
the effect larger, so it is not an artefact of them. What it remains is an
association in observational data, and the caution above about mechanism is
unaffected.

These 217 isolates are not 217 independent patients, and the deposit carries no
patient key with which to say so in a standard error. What it does carry is the
exact substitute: a baseline-only stratum in which every isolate comes from a
different patient by construction (Time_point = 0M, n = 167 at 15 days).

Restricted to that stratum, the two surviving associations part company. Growth holds and
still survives correction (OR 1.116, 1.040 to 1.198, p = 0.0024). Resistance does
not: OR 2.11 (1.07 to 4.16, p = 0.031), which is second in the family of eight
and so is tested against a Benjamini–Hochberg critical value of 0.0125. The
resistance association therefore depends on isolates that are not independent of
one another, and it is already the association that starting density explains
away. We report it as the weaker of the two on both counts.

The two surviving associations sit in the 15-day panel, which is where the
mechanism places them. By 60 days the cultures are 38-fold denser, the spread of
starting densities has more than halved, from an interquartile range of 1.00 to
0.42 log10, and the fraction of isolates short of headroom falls from 15.2 to 3.3
per cent. The confound is a property of a thin assay and it thins out when the
assay is not. Those two panels are columns on the same spreadsheet rows — 210
isolates appear in both — so every comparison between them is within-isolate and
is made that way. Pairing sharpens rather than softens the result: 26 isolates
lose their headroom shortfall between panels and none acquires one (exact McNemar
p = 3.0 × 10⁻⁸ against an unpaired p of 2 × 10⁻⁵) (22), eleven leave the floor and none
joins it (p = 9.8 × 10⁻⁴), and every isolate whose headroom changes gains
(Wilcoxon signed-rank p = 1.3 × 10⁻³³) (23). The interquartile range of starting
density falls by 0.58 log10.

It does not vanish, and the ordinal treatment is what shows where it goes.
Proportional odds holds throughout the 15-day panel but fails at 60 days for
starting density at the deepest endpoint (Brant p = 0.0031; likelihood-ratio test
against a released fit p = 0.0062). Releasing that coefficient puts the whole
effect at the upper cut: the odds ratio for clearing medium is 0.493 (0.336
to 0.724, p = 0.0003) against 0.951 for clearing low (0.647 to 1.396, p = 0.80).
A multinomial fit that assumes no ordering at all agrees (high against low,
relative risk ratio 0.59, p = 0.028; medium against low, 1.22, p = 0.39). In the
denser panel the starting density no longer decides who is called low; it still
decides who can be called high. A single averaged slope, ordinal or linear, would
have reported that as a null.

### 5. One written protocol does not produce one measurable depth

If the effect is a property of assay geometry rather than of clinical sampling,
it should appear where one protocol, one strain and one stock are distributed
deliberately. Van Wijk and colleagues (2023) ran exactly that exercise, sending a
single stock of H37Rv to six blinded laboratories under one written protocol (6, 13). It
does.

At ten times the minimum inhibitory concentration of moxifloxacin all six
laboratories return a positive kill rate spanning 5.2-fold, from 0.090 to 0.464
log10 CFU/mL per day, and across all 30 laboratory-by-arm cells the Tobit and
imputation estimates never differ by more than 0.003 log10 per day (Fig. 2A,
Table S6). The duration endpoint behaves differently on the same flasks. The
event it records is not clearance and not sterilisation but a **first observed
crossing below the assay floor**, and the distinction is not pedantic: most
series that cross later read above the floor again, including all five
untreated series that cross. The frame has to be stated,
because the endpoint depends on it. The time-to-event analysis runs at the 100 µL
quadruplicate plating, the most sensitive of the four, and there 29 of 72 treated
flasks ever fall below the floor: institutes B and C record crossings in every
arm, institute A in three of its four, and institutes D, E and F in none
(Fig. 2B), so for half the laboratories the first-crossing time is right-censored
throughout.

That split is a property of the plating, not of the laboratories. Counting a
crossing on **any** of the four platings gives 48 of the same 72 treated
flasks, and every laboratory records at least one — D six of its twelve, E one,
F ten. The two facts are the same
fact seen at two sensitivities, and they are exactly what this paper is about: a
duration endpoint is defined against a floor, and the floor is a choice. The
analysis keeps the single most sensitive plating so that the endpoint is
consistently defined, and reports here what a different choice would have
shown.

The two orderings do not correspond. Ranked by starting density, the three lowest
laboratories are exactly the three that recorded crossings and the three highest
exactly the three that did not, without exception; ranked by kill rate there is
no such correspondence (Fig. 2C). Institute F, with the highest starting density
at 6.53 log10, kills faster than four of the other five at 0.223 log10 per day
and records no crossing. Institute E returns the slowest rate of all at 0.090 and
also records none.

Starting density separates flasks that ever crossed from those that never did
with an area under the curve of 0.974. That figure is a description and it is quoted
without a p-value, deliberately. The comparison looks like 67 flasks but it is
three laboratories against three, and the between-laboratory evidence in this
deposit is six clusters throughout; the Limitations set out what that permits and
what it forbids. In short: the exact laboratory-level test returns 0.10, which is
the smallest value the design can return, and there is no within-laboratory
fallback once the treatment arm is held fixed.

The Cox fits are reported for the same reason and with the same restraint. On
laboratory alone, institutes D, E and F carry hazard ratios of 0.20, 0.21 and
0.20; adding starting density moves those to 0.34, 0.36 and 0.62, and concordance
rises from 0.896 to 0.930 (Fig. 2D). Institute C moves the other way, from 3.0 to
5.3, and it is also the fastest killer, which is the behaviour expected of a
laboratory that genuinely kills faster. No p-value is attached to any of these
terms, and the panel that displays them is a display of that movement rather than
a test of it. The tested covariate
is constant within cluster, and with six laboratories and six parameters the
cluster-robust covariance is singular by construction; fitting it anyway does not
fail loudly but returns a smaller p than the one it was meant to correct. A
coefficient that moves on adjustment is a statement about how far starting
density and laboratory identity overlap in this design, not evidence that one
explains the other.

Killing here is not sustained, and this is stronger than a caveat about
individual flasks. Of the 64 treated series carrying at least three quantified
readings at the most sensitive plating volume, the final step is not a decline in
48, and 44 end more than one log10 above their own lowest reading, with a median
rebound of 2.17 log10 and a largest of 5.54. Seventeen of the 32 flasks that fell
below the floor at the most sensitive plating — the 29 treated flasks above and
three untreated ones — were detectable again at a later visit, 14 of them in
treated arms. Across all four platings, 84 of the 140 series
that cross return above the floor, 60 per cent, and the return is quick: a
median of four days, with 45 per cent back within three. Those 360 series come
from 90 flasks, four platings each, so they are not 360 independent observations;
counted by flask, 53 of the 90 contain a crossing series — the 48
treated flasks above and five untreated ones — and 42 of those contain a
returning one. A crossing below the
assay floor in this deposit is therefore usually a transient rather than an
endpoint, which is a further reason it summarises less than the trajectory that
produced it. Killing itself is real and dose-dependent:
at one times the inhibitory concentration five of six laboratories record net
growth under moxifloxacin, between −0.047 and −0.214 log10 per day, and at ten
times all six record net decline.

Two consequences follow, and they matter for anyone who reads a duration off
such an experiment. The first is that the state below the floor is not
absorbing. Of 2 232 visit-to-visit transitions, 144 go from above to below and 95
go from below to above, so a series sitting below the floor leaves it at the
next visit with probability 0.22. The gradient runs with drug pressure — that
probability is 1.00 in untreated series, 0.37 to 0.92 at one times MIC and 0.07
to 0.18 at ten times — which says the event is at least partly a property of the
plate rather than of the drug. Of the 360 series, only 56, or 15.6 per cent, show
the shape a survival model assumes: one crossing that holds (Table S7). Two hundred and
twenty never cross at all, 65 cross and return, and 19 oscillate more than once.

The second is that the crossing time is never observed. It lies between the last
visit above the floor and the first visit below it, and the naive treatment
pins it to the later end, which biases every duration late by construction rather
than merely imprecisely. Fitted as interval-censored data (24) at the most sensitive
plating, the tenth percentile of the first crossing falls from 2.95 to 1.82 days
and the twenty-fifth from 11.24 to 9.64; across the treated arms at all four
platings the twenty-fifth percentile falls from 5.77 to 3.67 days, a 36 per cent
shortening. The non-parametric interval-censored curve sits below the naive
Kaplan–Meier at every visit at which crossings are still being recorded — by
0.081 at day 3 and 0.031 at day 7 — and the two coincide only from day 14, where
both are flat. A duration read off the naive curve is therefore too long, and by
about a day at the depths that matter.

What the adjustment establishes is descriptive and is worth stating as such: a
continuous measure of where the cultures began accounts for the laboratory term
at least as well as the laboratory label does, and one institute resists even
that. What can be tested, because flasks are exchangeable across laboratories
under the null, is how much of each quantity the laboratory owns. It owns 87.0
per cent of the variance in starting density (permutation p < 0.0002) and 33.0
per cent of the within-arm kill rate (p = 0.0048). It owns the duration endpoint
outright, since three laboratories produce none at all.

### 6. The same boundaries hold in an experiment the framework never saw

Every section so far tests the framework on the deposits it was built from, and
all of them are *Mycobacterium tuberculosis*. A search of five general
repositories, the tuberculosis consortia, the persistence literature, food
microbiology and the hollow-fibre field returned one deposit that carried all
three fields the boundaries require and could be analysed cold.

That was true of the search described. It is no longer true of the analysis
repository, which now holds 29 ingested deposits, of which 13 permit the
boundaries to be computed once the floor is established on the same tiers this
paper uses for its own — stated by the depositor, derived from a recorded plated
volume, or inferred from a pile-up on a plate-plausible value. Across those the
condition the boundaries imply, that no series may present as a measurement a
reduction deeper than its own floor allows, holds in 1 822 of 1 822 series in
five species. Those deposits are described in the data release rather than here,
because none was held out: the point of this section is a deposit opened after
every boundary and threshold was fixed, and only one qualifies on that ground.

Dubey and colleagues (2026) report amoxicillin-clavulanate against *Escherichia
coli* in a hollow-fibre system (16, 17). Their Methods state 100 µL plated with counts per
mL, so *L* = 10 CFU/mL is derived rather than inferred, and the derivation is
corroborated inside the file: a 100 µL plate reporting per mL can return only
multiples of ten, and all 229 genuine counts in the deposit are multiples of ten
with the smallest exactly ten. Sixty-nine further entries read as one, which no
100 µL plate can produce, and are the deposit's below-limit placeholder.

Across the 20 cultures with a measured day-zero density, headroom runs 4.85 to
5.45 log10. Endpoints at 1, 2, 3 and 4 logs are reachable for every culture; a
5-log endpoint is unreachable for 5 of 20; a 6-log endpoint is unreachable for
all 20 (Table S8). The framework therefore locates, on data it was not built
from, the depth at which a sterilisation claim in this experiment stops being
demonstrable.

Two features of that deposit are worth recording because they are the failure
modes this framework is meant to catch. Its Methods give a nominal inoculum of
10⁵ CFU/mL while the file measures a median of 1.215 × 10⁶, so taking *N₀* from the
Methods rather than from the data would have placed a full order of magnitude
into every boundary. And its treated arm reads at or below the floor already at
day zero while the paired control reads about 10⁶, so that sample was drawn after
exposure rather than before it.

### 7. A late endpoint can erase a 32-fold dose difference

The deposit carries apramycin at 1, 4, 8, 32 and 128 µg/mL (14, 15). The 1 µg/mL arm
shows net growth rather than killing and is excluded from the dose comparison, so
the range compared is 4 to 128 µg/mL: 32-fold, five doublings. Across it,
survivors separate 6.9-fold at day 3, 48.2-fold at day 7 and 5.2-fold at day 14 (Fig. 3,
Table S9). An experiment read at 14 days would report this drug as insensitive to
a 32-fold change in dose. Fitted per interval on a bootstrap resampling all three
replicates at both ends of every interval, the concentration slope is +0.059
log10 per day per doubling over days 0 to 3 (95 per cent interval +0.030 to
+0.088, p = 0.013), +0.033 over days 3 to 7 (−0.052 to +0.118, p = 0.24) and
−0.025 over days 7 to 14 (−0.060 to +0.010, p = 0.091); the early-versus-late
contrast is firm (+0.084, +0.037 to +0.128) and the early-versus-middle contrast
is not (p = 0.43).

The sign of the late slope is not claimed. By day 14 the highest arm sits at
65 CFU/mL and the deposit states no limit of quantification and records no plated
volume, so no floor can be derived for it. At any floor of 100 CFU/mL or above —
the value 10 µL plating would give, and an assumption rather than a derivation —
that arm is censored and its apparent rate is a lower bound. What holds without
any assumption about the floor is that the separation collapses.

### 8. One culture, two plated volumes, two tolerance labels

Every result above reads a deposit somebody else made for another purpose. This
one reads an experiment designed to try to break *N*_reach and *N*_id, with its
predictions written down before a plate was counted: *Escherichia coli* ATCC
25922, of the American Type Culture Collection — the reference strain the
standard names for quality control — against
ciprofloxacin at ten times its inhibitory concentration, seeded at three
densities and plated at two volumes, three flasks each, 216 plate readings.

The seeding is deliberately chosen so that the middle arm is the 5 × 10⁵ per mL
the standard specifies. Realised densities were 6.4 × 10⁴, 4.4 × 10⁵ and
3.8 × 10⁶ per mL. **At the standard inoculum plated at 10 µL, the deepest
reduction the three flasks could report ran from 3.71 to 3.93 logs — each arm's
own ceiling, not the drug's** — while those same three cultures plated at 100 µL
ran from 4.88 to 5.05 (Table S10). Every flask is paired with itself across the
two platings, so the gain is a property of the plating and not of the culture.

That much is arithmetic, as Box 1 says. So is the observation that two platings
of one sample carry different labels when both sit at their floors, since the
labels are then *L*₁/*N*₀ and *L*₂/*N*₀. **The quantity that could have come out
zero is how often a real experiment lands in the window where those two fractions
straddle the cut**, and it depends on where the cut is (Table S11). At a
threshold of one per cent the window is nearly shut. At one in a thousand,
which is where the clinical classification analysed above cuts its lowest class,
one sample-time in six receives two different labels from one culture. Nothing
about the biology differs between the two readings: there is one flask, one drug
and one moment, and the pipette decides.

---

## Discussion



### What fails, and where

That a negative culture under antibiotic exposure is not evidence of sterility is
established clinical microbiology and is not what this paper reports. What it
reports is that the quantitative metric introduced to replace that judgement
carries the same defect into a number, where it is harder to see.

The minimum duration for killing is scale-free by construction: a fractional
reduction divides out the starting density, and that is the property that makes
it the intended counterpart to the minimum inhibitory concentration. The property
holds in the estimand. It fails in the measurement, for a reason that is
arithmetic rather than statistical. A *q*-log reduction is observable only where
*q* logs are visible, and when the final reading rests on the floor the recorded
fraction reduces to *L*/*N₀* — a quantity determined entirely by the starting
culture. Fifteen per cent of the clinical isolates examined here could not have
demonstrated the deepest endpoint under any drug effect whatever, and all of them
are recorded as having failed to demonstrate it. Eighteen isolates that ended at
the same censored value carry tolerance labels that a single threshold on their
starting density reproduces exactly. Sweeping the true count across the range the
floor admits shows why: for twelve of them only one class is compatible with a
censored reading, so the published rule had no other label available, and for the
other six the compatible set spans a threshold, so the rule cannot choose.
Whether those cultures reached the floor is a question about rifampicin; which
label they received once they had is a question about arithmetic, and it is the
second that the starting density settles.

The title is scoped to the floor, and it is worth saying exactly how far it
reaches. In the 15-day panel, 12 of 203 usable calls have a single compatible
class and 6 have more than one; the other 185 rest on a measured fraction. The
kill rate still carries more of the variance in crossing time than the distance
does, in every multi-laboratory arm. What fails universally is not every
tolerance call but the *interpretability* of a deep log-reduction call reported
without *N₀* and *L*. What the inoculum settles is the subset of labels for which
killing has already reached the floor.

The failure is specific and it is bounded. Neither the 90 nor the 99 per cent
endpoint is compromised in this deposit: no isolate lacks headroom for either.
It is the 99.99 per cent endpoint that is unreachable for a substantial minority,
and it is the deep endpoint the clinical classification uses. That specificity is
what makes the problem fixable rather than fatal.

It is also a derivation rather than an observation, which is what allows it to be
tested elsewhere. Both boundaries follow from the definitions alone, they refer
to neither the drug nor the strain, and given a floor, a set of class thresholds
and a starting density they name the affected isolates in advance. In the
clinical deposit that agreement is exact isolate by isolate, though for the
twelve with a single compatible class it is an identity given the class rule
rather than an independent test. What could have gone the other way is the
boundary, where six isolates sit at *N*_id itself, the strict inequality leaves
them undecidable, and the deposit records all six as medium rather than low. In a deposit the framework was not built from it
locates the depth at which a sterilisation claim stops being demonstrable: five
of twenty cultures cannot show a five-log reduction, and none of the twenty can
show six.

Everything above is read backwards, out of files made for other purposes, and a
derivation that only ever explains the past is worth less than one that survives
being aimed at the future. So *N*_reach and *N*_id were used to design an
experiment against themselves, with the predictions recorded before a plate was
counted. At
the inoculum the standard specifies, the deepest reduction the three cultures
could report ran 3.71 to 3.93 logs at the 10 µL plating and 4.88 to 5.05 at
100 µL — the four-log endpoint unreportable at one plating and comfortable at the
other, in the same flask, on the same afternoon. That much is arithmetic and
could not have failed. What could have failed is whether a real experiment ever
lands in the window where the two platings straddle a class threshold, and at the
cut the clinical classification uses it does so for nine of 54 sample-times: one
culture, two labels, and nothing between them but the pipette. That is the
boundary behaving as a design constraint rather than as a post-hoc explanation,
and it is the reason the calculation in Box 1 belongs before an experiment rather
than after it.

What sits beneath the floor is the one thing a plate cannot report, and it has
been measured. Evangelopoulos and colleagues enumerated the same murine lungs
three ways — colony count, a molecular bacterial load from 16S rRNA, and a most
probable number — on the way to a different question (25). Under the deepest
regimens the colony count reads zero in every animal. In three arms, 18 lungs in
all, the plate declared every lung sterile while the most probable number on that
same tissue ran from 1 450 to 18 700 per lung. The molecular load can be
dismissed as nucleic acid outliving its owner; the most probable number cannot,
because it is a culture, and growth in a dilution series requires an organism
that is alive and culturable. Those lungs held thousands of viable bacilli that
the plate reporting them sterile could not see. This is the region a relapse
comes from, and in the mouse model used to decide which regimens enter clinical
trials it is the region a colony count is blind to.

A reader may object that this runs backwards. Falling below the limit of
detection is what a *susceptible* population does; how can it make an isolate
look more tolerant? The objection is a fair one, and it is answered by
separating two endpoints that the literature reports side by side.

A duration endpoint asks when a fixed depth was reached. An isolate short of the
headroom that depth requires cannot reach it under any drug effect whatever, so
what the file records is not a short duration but no duration: the isolate is
censored at the end of observation, which is the maximum of the scale and the
most tolerant value it can take. Of the 217 isolates, 33 lack the range for the
99.99 per cent endpoint the classification uses, and 33 of those 33 are recorded
at that ceiling, against 162 of the 184 with ample headroom (Fisher p = 0.030).
The isolates that could not demonstrate the endpoint are, without exception, the
ones recorded as having failed to reach it.

A class endpoint asks how far the population fell by a fixed time, and there the
direction is not merely preserved but inverted by the arithmetic. Once the final
reading sits on the floor the recorded fraction is *L*/*N₀*, and with *L* fixed a
*lower* starting density yields a *larger* recorded fraction — which is a higher
tolerance class, not a lower one. Eighteen isolates ended at the same floor value
at day 5. Their starting densities span 265-fold; their recorded apparent
survival spans 265-fold. The two agree to every digit because they are the same
quantity, and the labels split accordingly, twelve low and six medium.

Neither mechanism asks anyone to mistake a sterile culture for a surviving one.
In the first the assay returns no endpoint; in the second it returns the floor
divided by the inoculum. What is read as biology is, in both cases, a property of
the measurement.

The same arithmetic answers the objection that the starting density is fixed by
protocol. It is fixed as a turbidity, and a turbidity is not a viable count. Under
one written protocol the realised densities differed enough to change the deepest
demonstrable kill by 2.33 log10 between laboratories, and by 4.40 once the choice
of plated volume is included, since that choice sets the floor.

The standard is not silent on that choice, and this is the paper's sharpest
finding rather than an awkwardness for it. M26-A's section 1.3.2.5 is headed
*Volume Transferred*, and it ties the volume to the endpoint by a quantification
rule: the volume must be such that after the defined 99.9 per cent killing, at
least ten colonies remain to be counted (10). It permits 10 to 100 µL, and gives a
reason at each end — carryover above, Poisson sampling error below. Section 3.1
goes further and requires that the smallest accurately detectable count be
determined by serial dilution of a known inoculum. A guideline written in 1999
therefore already required both of the numbers this paper asks for: a floor
established by measurement, and a plated volume chosen against the endpoint.

Applied to its own endpoint the rule bites. Ten colonies after a 99.9 per cent
kill of 5 × 10⁵ per mL needs at least 20 µL streaked; a 10 µL streak yields five
and fails the rule. The requirement was there, it was quantitative, and the
deposits reanalysed here do not meet it — not because their authors disregarded a
standard, but because the endpoint moved. M26-A sets 99.9 per cent throughout and
nowhere contemplates a four-log call; the deeper endpoints came later, and the
volume rule did not travel with them.

### What the tolerance phenotype tracks instead

Removing the assay's contribution leaves something rather than nothing, and what
remains is biologically coherent. Growth state predicts the tolerance class and
survives adjustment for starting density, which is the expected direction:
isoniazid requires KatG activation and active cell-wall synthesis (26), rifampicin
requires transcription (27), and a population that is not dividing presents less of
what these drugs act on. Physiological state, not drug susceptibility, is the
axis the classification is reading.

The isoniazid-resistance association behaves differently and instructively, and
it is the weaker of the two on two separate counts. Unadjusted, resistant
isolates carry 2.32 times the odds of a higher tolerance class; adjusted for
starting density the odds ratio is 1.31 and the interval spans one. It also does
not clear its corrected threshold once the analysis is restricted to the baseline
isolates, which are one per patient by construction — the only correction for
repeated isolates this deposit permits, since it carries no patient identifier.
The growth association survives both. The mechanism of the attenuation is visible
in the same file: resistant isolates enter the assay ten-fold lower and 26.2
per cent of them lack the headroom the endpoint requires. We do not know why they
seed lower.
The natural explanation — that resistance carries a fitness cost — is not
supported here, since these isolates do not grow measurably more slowly and most
carry the near-neutral *katG* S315X allele (28, 29). That gap is a finding in its own
right and belongs in the next study rather than in a speculative sentence in this
one. Nor is it explained away by anything else the file records: of its nine
pretreatment covariates only two can legitimately be adjusted for, and neither
moves the association by more than five per cent (Section 4). The two larger
movements in that table both come from columns that record the exposure rather
than a confounder: the mutation identity, which is missing for all but one
susceptible isolate, and the isoniazid MIC, which separates the two groups
completely and enlarges the seeding gap by 13 per cent instead of shrinking it.

### How large the effect is

Where the inoculum is set deliberately rather than by clinical accident, the same
arithmetic operates and can be measured rather than inferred. In more than a
third of cross-laboratory comparisons the flask in which the population fell
faster crossed below the assay floor later, and the distance-over-rate criterion
accounts for three in five of them. Resampling whole
laboratories rather than pairs leaves that rate poorly determined — 3.0 to 72.4
per cent — so it is the mechanism and not the rate that the deposit establishes.

The variance decomposition sets the size of the effect. The rate term carries more of the
spread in crossing time than the distance term in every arm examined. A
crossing time is not mostly a measurement of the inoculum. It is a mixture in
which the inoculum is a large minority — enough to reverse the ranking of two
populations in more than a third of comparisons, which is the number that
matters to anyone
choosing between two compounds, and not enough to license the claim that the
endpoint measures the starting culture.

### Relation to the analyses these deposits were made for

Our reading and van Wijk's agree where they overlap. They report the inoculum
spread themselves and conclude that baseline burden varied between laboratories
while net drug effect varied less (6); that conclusion anticipates part of ours and
belongs to them. The separation is that they excluded readings outside the
quantification limits from numerical analysis, which is a defensible reporting
decision that forecloses the question asked here, because it removes the
observations from which a duration is built.

Vijay and colleagues report associations between tolerance, resistance status and
treatment history in the same isolates (5). We do not dispute the measurements; the
deposit is unusually complete, and it is only because they deposited the
classification, its inputs and the assay geometry together that this analysis was
possible at all. What we add is that the deepest of their endpoints has a
dynamic-range constraint that varies systematically with the isolate groups being
compared, and that the resistance association survives neither the inclusion of
starting density nor restriction to one isolate per patient. The growth
association survives both, so the finding is not that their classification is
empty but that one of its two associations is carried by the assay geometry and
by isolates that are not independent.

### Limitations

Four features of these deposits bound what the analysis can establish, and each
points at the design that would settle it.

The first limitation is one this paper has already acted on rather than merely
declared. Every conclusion drawn from the two primary deposits was recomputed at
the level its observations are actually independent, and the outcome is
tabulated rather than summarised (Table S12): twenty survive unchanged, six
survive with materially wider uncertainty, five do not survive and **have already
been removed from the text above**, and one is withdrawn because its null is
false before any data are seen. The five and the one are not claims this paper
makes; they are claims it tested and dropped, and the ledger is here so a reader
can check that the dropping was done rather than promised.

The between-laboratory evidence is six clusters. Every flask in a laboratory
shares a starting culture, so the effective sample size for any comparison
*between* laboratories is six and not the 67 to 85 flasks the tables list. Six is
too few for asymptotic cluster-robust standard errors, and fitting them anyway
does not fail loudly: on these data the sandwich returns a smaller p for every
institute term than the model-based p it was meant to correct. Where a comparison
is between laboratories we therefore quote the exact laboratory-level test or a
cluster bootstrap and, where the design cannot produce a meaningful p at all, no
p. Three laboratories recorded crossings at the 100 µL plating and three did
not, and for that split the smallest attainable two-sided p is 0.10. Quantities
for which flasks *are* exchangeable across laboratories — the variance shares,
and the inversion rate under a flask bootstrap — keep an exact permutation test
and are the strongest between-laboratory evidence the deposit holds.

The starting density is not measured on a common time base. Only institutes C and
D deposit day-zero readings for treated flasks; A, B, E and F deposit day one, by
which point the ten-times-MIC arms have already lost between 0.7 and 2.4 log10.
For four of six laboratories the exposure is therefore a partly post-kill
reading. Re-running the whole comparison on a day-one exposure for every
laboratory leaves the ordering, the area under the curve and the laboratory-level
p unchanged, so the conclusion is robust to it, but the heterogeneity is real and
is reported rather than smoothed over.

Starting density is not independent of laboratory in the six-laboratory exercise:
87.0 per cent of the variance in flask-level starting density lies between
laboratories rather than within them, the laboratory means spanning 3.62 log10
against a median within-laboratory standard deviation of 0.43. Adding starting
density to a model that already contains laboratory is therefore closer to
replacing a label with a number carrying much the same information than to
separating two covariates. Separating them requires a design that fixes the
inoculum across laboratories.

The same isolates appear in the 15-day and 60-day panels of the clinical deposit,
so the comparison between panels is not independent and bounds the evidence for a
difference rather than establishing it.

Starting density could be a mediator rather than a confounder of the resistance
association: if resistance slows growth and slow growth causes genuine tolerance,
adjusting for the density that slow growth produces would remove real signal. The
asymmetry favours the confounding reading, since growth survives adjustment and
resistance does not, but a design that fixes the inoculum would settle it.

### What should change

**Report the starting density and the assay floor with every tolerance
measurement.** Together they give the headroom, and without the
headroom a log-reduction endpoint cannot be interpreted. Neither costs anything
to record. Four of the deposits examined in the course of this project state no
limit anywhere.

**Choose the endpoint depth against the headroom actually available**, and note
that the required inoculum is computable before the experiment rather than
diagnosable after it: seeding above *L* · max(10^*q*, 1/*c*₁) makes both failure
modes impossible, which for this assay is 230 000 per mL. A 99 per cent endpoint
was reachable for every isolate in this deposit and a 99.99 per cent endpoint for
85 per cent of them. Where the deep endpoint is wanted, the
starting culture must be concentrated or the assay floor lowered until the budget
covers it; where it cannot be, the shallower endpoint is the honest one. This is
a design decision that is currently not being made.

**Model an ordered label as ordered.** A tolerance class is low, medium or high,
and scoring that 0, 1, 2 to fit a line asserts a distance between classes that no
one has established. Proportional-odds regression costs nothing to run, reports
in odds ratios, and — where the proportionality it assumes fails, as it does here
at 60 days — says so rather than averaging two different effects into one null.

**Do not densify the inoculum merely to buy headroom.** Seeding higher makes a
deep endpoint legal, and it also changes the experiment: a denser culture is a
different physiological state, and this paper's own finding is that physiological
state is what the tolerance label tracks. Where the headroom will not carry the
endpoint, the shallower endpoint is the honest choice, and the growth state
belongs on the report either way.

**Treat an endpoint at the floor as a bound, not a value.** A recorded fraction of
*L*/*N₀* is an upper limit on survival, not an estimate of it. Analysed as a
measurement it manufactures differences between isolates whose final viable
burdens the assay could not distinguish, and it hides the converse point: because
the compatible range of fractional reductions depends on where each culture
started, the same censored reading represents a different demonstrated kill at
every starting density.

None of this requires new apparatus or a statistician, and to make that concrete
the four checks are released as a small command-line tool alongside the analysis
code. Given a starting density and either an assay floor or a plated volume, it
returns the headroom, states which of the 90, 99, 99.9 and 99.99 per cent
endpoints that headroom can support, and reports the recorded fraction a
floor-level reading would produce, labelled as the bound it is. Where a culture
volume is known it also returns the viable burden a blank reading is consistent
with; where it is not, it declines to compute it rather than assuming one. The
tool exits non-zero when a requested endpoint is unreachable, so it can be run
before an experiment rather than after it.

**Report physiological state as a required field.** It is what the classification
is reading, and it is currently the least documented variable in the assay.

**Fix the inoculum, or adjust for it, before comparing tolerance across groups.**
The comparison that motivated this work — resistant against susceptible isolates
— is confounded by a ten-fold difference in starting density whose cause is
unknown. Until that is understood, group comparisons of tolerance in clinical
isolates should carry the starting density as a covariate.

---

### Conclusion

A negative culture under antibiotic exposure has never been evidence of
sterility, and the field knows it. The remedy adopted was to stop asking whether
the culture went negative and to start asking how far it fell, expressed as a
fraction of where it began so that the starting culture could not matter. We find
that the fraction stops being a fraction once the population reaches the floor.
What the deposit records from that point is *L*/*N₀*, which moves with the
starting density and not with the surviving population — in this deposit, for
fifteen per cent of isolates at the depth the classification uses, and for the
eighteen isolates whose recorded label a single threshold on their inoculum
reproduces exactly, because for twelve of them no count below the floor would
have changed which class the rule could return.

The consequence is not that tolerance is an artefact. It is that a tolerance call
made without its headroom cannot be told apart from an inoculum measurement, and
that the phenotype which does survive the correction is physiological state
rather than drug susceptibility. Reporting the starting density and the assay
floor, matching endpoint depth to the range actually available,
and treating a reading at the floor as a bound would make a tolerance
classification mean the same thing in one laboratory as in the next. Until then,
some of what the field calls tolerance cannot be separated from a record of how
much culture went into the tube.

---

## Materials and Methods

*The condensed account. The full account, with every estimator and every sensitivity analysis, is Supplementary Methods in the supplemental file.*

### Ethics

This study reanalysed publicly available, de-identified datasets deposited by
other groups. No new patient samples were collected, no new experimental data
were generated, and no individual is identifiable from any material presented
here. [An institutional determination that ethics approval was not required for
secondary analysis of these deposits is to be inserted, naming the body that made
it.]

### Use of generative artificial intelligence

[To be confirmed by the author before submission. See AI_DISCLOSURE.md in the
submission package for the draft statement and what ASM requires it to cover.]

### Data availability

Every dataset analysed here was already public under an open licence when this
work began, and none was generated for it. Each deposit is identified in Table 1
and cited in the reference list alongside the article that first described it:
the clinical isolate panel of Vijay and colleagues, the six-laboratory time-kill
exercise of van Wijk and colleagues, the evolved-clone deposit of Windels and
colleagues, the apramycin grid of Kaur and colleagues, and the hollow-fibre
Source Data of Dubey and colleagues, which was held out of every fitting step.

The analysis code, both audit scripts, the headroom tool described above and the
machine-readable receipts recording the software versions each stage ran under
are deposited in a public repository (30), with the documentation needed to install
and run them and a test dataset with the control parameter settings used here.
Code created to generate the results and to interpret the data is included. The
repository is dual-licensed, MIT for the code and CC BY 4.0 for the manuscript,
figures and results, which is no more restrictive than CC BY; the deposits keep
their depositors' own licences and are not relicensed here. It is at
https://github.com/piranfar/comparative_model_presistance. [The commit
identifier of the submitted version is to be inserted at submission.]

Every number quoted in this manuscript is regenerated from the deposits by that
code, and two audit stages check it: one recomputes the pinned quantities — the
load-bearing counts, every headline interval and every figure a conclusion rests
on — from the tables they came from; the other reads the table legends, the
figure legends, Box 1 and the Abstract that the first does not. Both report
anything that disagrees, and neither pins every cell of every table, as the
Reproducibility subsection states.

---

## Acknowledgments

This research received no specific grant from any funding agency in the public,
commercial or not-for-profit sectors.

The author declares no competing interests.

Vahhab Piranfar is the sole author and is responsible for conceptualisation,
methodology, software, formal analysis, investigation, data curation, writing of
the original draft, review and editing, and visualisation.

---

## Figure legends

**Figure 1. A log-reduction endpoint is bounded by the assay floor, and the bound
decides the phenotype.** 217 clinical *M. tuberculosis* isolates under
rifampicin, from the deposit that carries the tolerance classification.
(**A**) The distribution of day-5 most probable numbers. It stops at 23 per mL
with a pile-up on it rather than tapering, and no value anywhere in the file lies
below; that is the behaviour of a floor. (**B**) Headroom, the distance from each
isolate's starting density down to that floor, ranked across isolates, against
the depth each tolerance endpoint requires. No isolate is short of the 90 or 99
per cent endpoint. Thirty-three of 217 fall in the shaded band below the 99.99
per cent endpoint, and all 33 are recorded as failing to reach it. (**C**) The
eighteen isolates of the 15-day panel whose day-5 reading was censored at the
floor. Their true final
counts are unknown below *L*, so the assay cannot distinguish their final viable
burdens; what is plotted is the recorded fraction *L*/*N₀*, which is what a
censored reading computes, so the 265-fold span in apparent survival is exactly
the 265-fold span in starting density. The dotted lines are the deposited
classification thresholds. Which side of the low/medium cut an isolate falls on
is settled by where it began, not by what the reading measured — though reaching
the floor at all required rifampicin to cover that isolate's whole headroom, at
least 3.00 logs for the shallowest and 5.42 for the deepest. For the twelve below
the cut, no count the assay admits leaves any class but **low** compatible; for
the six that sit exactly on it the compatible range straddles the cut and two
classes remain.

**Figure 2. Where the inoculum is set by protocol, the two summaries still
diverge.** Six laboratories, one written protocol, one stock of *M. tuberculosis*
H37Rv, moxifloxacin at ten times the minimum inhibitory concentration.
(**A**) The kill rate by censored maximum likelihood with 95 per cent
profile-likelihood intervals; every laboratory yields one, spanning 5.2-fold.
(**B**) Kaplan–Meier curves for time to the first observed crossing below the
assay floor at the 100 µL plating. Three curves never descend: those
laboratories recorded no flask below the floor in any arm at that plating, so
their first-crossing times are right-censored throughout. (**C**) The two
summaries against each other. The three lowest starting densities are exactly
the three laboratories that recorded crossings at the 100 µL plating; the kill
rate produces no such separation.
(**D**) The model-based p-value attached to each laboratory in a descriptive Cox
model before (grey) and after (arrow head) starting density is added. The panel
shows how far the two predictors overlap: five of the six terms move toward
p = 1 on adjustment and institute C moves away from it. Those p-values are
plotted because they are what moves, not because they are valid: the laboratory
label is constant within its own cluster and there are six clusters, so no
between-laboratory test is available and none is claimed. Blue marks a term
crossing the conventional threshold, which is a description of the movement and
not a finding.

**Figure 3. A late endpoint cannot resolve a 32-fold concentration range.**
Apramycin against *M. tuberculosis*, five concentrations, triplicate counts.
(**A**) The trajectories, with an assumed floor of 100 CFU/mL — the value 10 µL
plating would give — drawn as a band; this deposit records no plated volume, so
the band is an assumption and is drawn to show what the assumption costs; by day 14 the highest arm lies within it, so its apparent rate
over the final interval is a lower bound. (**B**) The ratio of survivors between
the lowest and highest of the four compared concentrations, 4 and 128 µg/mL, at
each sampling day, rising to 48.2-fold at
day 7 and collapsing to 5.2-fold at day 14. (**C**) The concentration slope fitted
separately in each interval from a replicate-level bootstrap, 20 000 draws.

**Figure 4. Resistance and tolerance occupy separate axes, in two designs.**
(**A**) All 24 comparisons between the concentration axis and the duration axis
that the 217-isolate file supports, each against the Benjamini–Hochberg critical
value it would have to beat. Amber marks the four reaching nominal significance;
none survives. (**B**) The censoring behind them: the fraction of isolates at the
assay ceiling rises with endpoint depth, and the nominal hits concentrate where
censoring is heaviest. (**C**) The same question in 126 evolved *E. coli* clones,
by nutrient stratum.


## Supplemental material

The supplemental file carries the full Materials and Methods, the analyses named above as supplementary text, and 22 supplemental tables. Table S13, Table S14, Table S15, Table S16, Table S17, Table S18, Table S19, Table S20, Table S21 and Table S22 support analyses reported there rather than in this article, and are listed so that every supplemental item is named in the manuscript.


## Tables

**Table 1.** The five published deposits reanalysed. Four carry the analysis and the fifth is held out to test it. None was generated for this study. The held-out deposit was opened after every boundary and threshold was fixed, which the commit history of the analysis repository timestamps; the other four were selected for the fields they carry, and that selection is not separately registered.

| Dataset | Organism | Drug and range | Design | Deposit | Licence |
| --- | --- | --- | --- | --- | --- |
| Six-laboratory exercise | *M. tuberculosis* H37Rv | moxifloxacin, isoniazid, 1x and 10x MIC | 90 flasks, 2 775 readings | figshare 19766083 | CC BY 4.0 |
| Clinical isolates | *M. tuberculosis*, 217 isolates | rifampicin | 6 duration endpoints per isolate | eLife 93243, suppl. file 2 | CC BY 4.0 |
| Evolved clones | *E. coli*, 126 clones | amikacin | MIC and persister fraction per clone | Zenodo 7550302 | CC BY 4.0 |
| Concentration-by-time grid | *M. tuberculosis* | apramycin 1-128 ug/mL (amikacin arm not analysed) | 5 concentrations x 4 days x 3 replicates | figshare 26462791 | CC BY 4.0 |
| Held out for validation | *E. coli*, hollow fibre | amoxicillin-clavulanate | 20 cultures, measured day-zero density, 100 uL plated | Nat Commun 2026 Source Data | CC BY 4.0 |

**Table 2.** The reduction each tolerance endpoint requires against the reduction the assay can resolve. Headroom is the distance from an isolate's starting density to the MPN floor of 23 per mL. An isolate short of headroom cannot reach that endpoint however completely the drug worked, and every such isolate is recorded at the assay ceiling.

| Prior culture | Endpoint | Isolates | Short of headroom | Fraction short | At ceiling: short vs ample |
| --- | ---: | ---: | ---: | ---: | ---: |
| 15 days | 90% (1 log) | 217 | 0 | 0.0% | - |
| 15 days | 99% (2 log) | 217 | 0 | 0.0% | - |
| 15 days | 99.99% (4 log) | 217 | 33 | 15.2% | 100% vs 88% |
| 60 days | 90% (1 log) | 210 | 0 | 0.0% | - |
| 60 days | 99% (2 log) | 210 | 0 | 0.0% | - |
| 60 days | 99.99% (4 log) | 210 | 7 | 3.3% | 100% vs 95% |

**Table 3.** Isolates whose day-5 reading was censored at the MPN floor. They share one reported floor-level observation, but their true final counts are unknown below the floor, so the assay cannot distinguish their final viable burdens; because their starting densities differ, the same reading also implies a different range of compatible fractional reductions in each. The recorded fraction is L/N0, so the spread in apparent survival equals the spread in starting density exactly, and the labels differ accordingly. The last three columns sort every call in the 15-day panel, not only the censored ones: a censored reading bounds the class from above, and sweeping the true count across the admissible range leaves twelve calls with a single compatible class and six with more than one. Reaching the floor at all is a property of the killing; which class is then compatible is a property of the starting density and the floor.

| Prior culture | At the floor | Starting density spread | Recorded survival spread | Labels assigned at the floor | Measured | Single compatible class | Multiple compatible classes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 15 days | 18 | 265x | 265x | Low: 12, Medium: 6 | 185 | 12 | 6 |
| 60 days | 6 | 100x | 100x | Low: 6 | 191 | 6 | 0 |


## References

1. World Health Organization. 2022. WHO consolidated guidelines on tuberculosis. Module 4: treatment — drug-susceptible tuberculosis treatment. World Health Organization, Geneva, Switzerland. https://iris.who.int/handle/10665/353829.

2. Brauner A, Fridman O, Gefen O, Balaban NQ. 2016. Distinguishing between resistance, tolerance and persistence to antibiotic treatment. Nat Rev Microbiol 14:320-330. https://doi.org/10.1038/nrmicro.2016.34.

3. Brauner A, Shoresh N, Fridman O, Balaban NQ. 2017. An experimental framework for quantifying bacterial tolerance. Biophys J 112:2664-2671. https://doi.org/10.1016/j.bpj.2017.05.014.

4. Vijay S, Vinh DN, Hai HT, Ha VTN, Dung VTM, Dinh TD, Nhung HN, Tram TTB, Aldridge BB, Hanh NT, Thu DDA, Phu NH, Thwaites GE, Thuong NTT. 2021. Ribosomal protein S1 is required for growth and antibiotic tolerance in Mycobacterium tuberculosis. Antimicrob Agents Chemother 65:e00429-21.

5. Vijay S, Bao NLH, Vinh DN, Nhat LTH, Thu DDA, Quang NL, Trieu LPT, Nhung HN, Ha VTN, Thai PVK, Ha DTM, Lan NH, Caws M, Thwaites GE, Javid B, Thuong NT. 2024. Rifampicin tolerance and growth fitness among isoniazid-resistant clinical *Mycobacterium tuberculosis* isolates from a longitudinal study. Elife 13:RP93243. https://doi.org/10.7554/eLife.93243.

6. van Wijk RC, Lucía A, Sudhakar PK, Sonnenkalb L, Gaudin C, Hoffmann E, Dremierre B, Aguilar-Ayala DA, Dal Molin M, Rybniker J, de Giorgi S, Cioetto-Mazzabò L, Segafreddo G, Manganelli R, Degiacomi G, Recchia D, Pasca MR, Simonsson USH, Ramón-García S. 2023. Implementing best practices on data generation and reporting of *Mycobacterium tuberculosis* in vitro assays within the ERA4TB consortium. iScience 26:106411. https://doi.org/10.1016/j.isci.2023.106411.

7. Rabodoarivelo MS, Hoffmann E, Gaudin C, Aguilar-Ayala DA, Galizia J, Sonnenkalb L, Dal Molin M, Cioetto-Mazzabò L, Degiacomi G, Recchia D, Rybniker J, Manganelli R, Pasca MR, Ramón-García S, Lucía A. 2025. Protocol to quantify bacterial burden in time-kill assays using colony-forming units and most probable number readouts for *Mycobacterium tuberculosis*. STAR Protoc 6:103643. https://doi.org/10.1016/j.xpro.2025.103643.

8. 2025. Handling of bacterial counts below the limit of quantification in pharmacokinetic-pharmacodynamic analysis biases regimen ranking. CPT Pharmacometrics Syst Pharmacol. https://doi.org/10.1002/psp4.70140.

9. 2025. Within-host antibiotic tolerance in Mycobacterium tuberculosis. bioRxiv. https://doi.org/10.1101/2025.07.29.667394.

10. National Committee for Clinical Laboratory Standards. 1999. Methods for determining bactericidal activity of antimicrobial agents; approved guideline. NCCLS document M26-A. National Committee for Clinical Laboratory Standards, Wayne, PA. ISBN 1-56238-384-1.

11. Balaban NQ, Helaine S, Lewis K, Ackermann M, Aldridge B, Andersson DI, Brynildsen MP, Bumann D, Camilli A, Collins JJ, Dehio C, Fortune S, Ghigo J-M, Hardt W-D, Harms A, Heinemann M, Hung DT, Jenal U, Levin BR, Michiels J, Storz G, Tan M-W, Tenson T, Van Melderen L, Zinkernagel A. 2019. Definitions and guidelines for research on antibiotic persistence. Nat Rev Microbiol 17:441-448. https://doi.org/10.1038/s41579-019-0196-3.

12. Vijay S, Bao NLH, Vinh DN, Nhat LTH, Thu DDA, Quang NL, Trieu LPT, Nhung HN, Ha VTN, Thai PVK, Ha DTM, Lan NH, Caws M, Thwaites GE, Javid B, Thuong NT. 2024. Supplementary file 2 to "Rifampicin tolerance and growth fitness among isoniazid-resistant clinical *Mycobacterium tuberculosis* isolates from a longitudinal study" (elife-93243-supp2-v1.xlsx). eLife. https://doi.org/10.7554/eLife.93243.

13. van Wijk RC, Lucía Quintana A, Ramón-García S. 2023. *Mycobacterium tuberculosis* time kill assay data of the standardized protocol within the ERA4TB consortium. figshare. https://doi.org/10.6084/m9.figshare.19766083.v1.

14. Kaur P. 2024. Apramycin kills replicating and non-replicating *Mycobacterium tuberculosis* — raw data. figshare. https://doi.org/10.6084/m9.figshare.26462791.v1.

15. Kaur P, Ramya VK, Naveenkumar CN, Bharathkumar K, Singh M, Hobbie SN, Shandil RK, Narayanan S. 2024. Apramycin kills replicating and non-replicating *Mycobacterium tuberculosis*. Front Trop Dis 5:1413211. https://doi.org/10.3389/fitd.2024.1413211.

16. Dubey V, Darlow C, Gerada A, Unsworth J, Sheth E, Reza N, Farrington N, Haldenby S, Warren D, Liu X, Howard A, Hope W. 2026. Source Data to "Molecular pharmacodynamics of amoxicillin-clavulanic acid for urinary tract infections caused by *Escherichia coli*" (41467_2026_74323_MOESM4_ESM.xlsx). Nature Communications. https://doi.org/10.1038/s41467-026-74323-2.

17. Dubey V, Darlow C, Gerada A, Unsworth J, Sheth E, Reza N, Farrington N, Haldenby S, Warren D, Liu X, Howard A, Hope W. 2026. Molecular pharmacodynamics of amoxicillin-clavulanic acid for urinary tract infections caused by *Escherichia coli*. Nat Commun 17:7504. https://doi.org/10.1038/s41467-026-74323-2.

18. Cochran WG. 1950. Estimation of bacterial densities by means of the "most probable number". Biometrics 6:105. https://doi.org/10.2307/3001491.

19. Blodgett R. 2023. BAM appendix 2: most probable number from serial dilutions. Bacteriological analytical manual. US Food and Drug Administration, Silver Spring, MD. https://www.fda.gov/food/laboratory-methods-food/bam-appendix-2-most-probable-number-serial-dilutions.

20. Fisher RA. 1922. On the interpretation of χ² from contingency tables, and the calculation of P. J R Stat Soc 85:87-94. https://doi.org/10.2307/2340521.

21. Mann HB, Whitney DR. 1947. On a test of whether one of two random variables is stochastically larger than the other. Ann Math Stat 18:50-60. https://doi.org/10.1214/aoms/1177730491.

22. McNemar Q. 1947. Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika 12:153-157. https://doi.org/10.1007/BF02295996.

23. Wilcoxon F. 1945. Individual comparisons by ranking methods. Biom Bull 1:80. https://doi.org/10.2307/3001968.

24. Turnbull BW. 1976. The empirical distribution function with arbitrarily grouped, censored and truncated data. J R Stat Soc Series B Stat Methodol 38:290-295. https://doi.org/10.1111/j.2517-6161.1976.tb01597.x.

25. Evangelopoulos D, Prosser G, Rodgers A, Dagg B, Khatri B, Bhagwat A, Gonzalo X, Kolyva A, Bertozzi G, Silva-Pereira TT, Gibbons N, Bhatt A, Sabharwal N, Perdigao J, Portugal I, Rodrigues C, Duarte R, Gomes M, Cirillo DM, McHugh TD. 2022. Data from: Comparative evaluation of viable count, molecular bacterial load and most probable number for the enumeration of Mycobacterium tuberculosis in murine tissue. University College London Research Data Repository. https://doi.org/10.5522/04/19175153.v2. Retrieved 2026-09-07.

26. Vilchèze C, Jacobs WR Jr. 2007. The mechanism of isoniazid killing: clarity through the scope of genetics. Annu Rev Microbiol 61:35-50. https://doi.org/10.1146/annurev.micro.61.111606.122346.

27. Campbell EA, Korzheva N, Mustaev A, Murakami K, Nair S, Goldfarb A, Darst SA. 2001. Structural mechanism for rifampicin inhibition of bacterial RNA polymerase. Cell 104:901-912. https://doi.org/10.1016/S0092-8674(01)00286-0.

28. Pym AS, Saint-Joanis B, Cole ST. 2002. Effect of *katG* mutations on the virulence of *Mycobacterium tuberculosis* and the implication for transmission in humans. Infect Immun 70:4955-4960. https://doi.org/10.1128/IAI.70.9.4955-4960.2002.

29. van Soolingen D, de Haas PEW, van Doorn HR, Kuijper E, Rinder H, Borgdorff MW. 2000. Mutations at amino acid position 315 of the *katG* gene are associated with high-level resistance to isoniazid, other drug resistance, and successful transmission of *Mycobacterium tuberculosis* in the Netherlands. J Infect Dis 182:1788-1790. https://doi.org/10.1086/317598.

30. Piranfar V. 2026. Analysis code, audit scripts and headroom tool for "The detection floor bounds what a time-kill assay can report: minimum duration for killing and log-reduction endpoints in five published deposits and a prospective test".
