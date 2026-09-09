---
title: "The detection floor bounds tolerance endpoints in Mycobacterium tuberculosis"
short_title: "The detection floor bounds tolerance endpoints in M. tuberculosis"
article_type: "Research Article"
keywords:
  - time-kill assay
  - limit of quantification
  - minimum duration for killing
  - antibiotic tolerance
  - colony counting
  - censored data
  - Mycobacterium tuberculosis
---

# The detection floor bounds tolerance endpoints in *Mycobacterium tuberculosis*

**Author:** Vahhab Piranfar¹

¹Independent Researcher, New York, NY, USA

ORCID: [0000-0003-3653-5739](https://orcid.org/0000-0003-3653-5739)

**Correspondence:** Vahhab Piranfar, vahab.p@gmail.com

**Figures:** 3 | **Tables:** 3 | **Boxes:** 1 | **Supplemental figures:** 2 | **Supplemental tables:** 22

---

## Abstract

A culture that grows nothing after antibiotics has never proved sterility, so
tolerance is scored by how far the count fell: the minimum duration for killing.
That endpoint is a fraction of the starting count, so the inoculum should cancel.
It does in the definition, and fails once killing reaches the assay's floor.
Five deposits are reanalysed; one experiment tests this.

Two boundaries follow from the definitions. For a floor *L*, a *q*-log endpoint
is visible only above *L*·10^*q*; above
*L*/*c*₁, with *c*₁ the lowest class threshold, a floor-level reading fits only
the lowest class. Reaching the floor is the drug's doing; the label it permits is
not.

Of 217 *Mycobacterium tuberculosis* isolates classified for rifampicin tolerance,
33 began too close to the floor to show the 99.99 per cent reduction used, and
all 33 are recorded as failing. Of eighteen read at the floor, twelve admit one
class, six admit two. The label tracks growth state, not isoniazid resistance;
most of that runs through a ten-fold lower inoculum — the denominator it is cut
on.

Prospectively, *Escherichia coli* ATCC 25922 at the standard inoculum could
report 3.71–3.93 logs at 10 µL and 4.88–5.05 at 100 µL; at a cut of 10⁻³, six of
54 sample-times took two labels from one culture, the pipette alone deciding.
Letting the plated volume vary across the permitted range moves demonstrable
depth by 1.60 log10, as exact arithmetic.
A tolerance call reported without its starting density and assay floor cannot be
interpreted.

**Keywords:** time-kill assay; limit of quantification; minimum duration for
killing; antibiotic tolerance; colony counting; censored data;
*Mycobacterium tuberculosis*

## Introduction

Tuberculosis treatment runs for four to six months (1). Shortening it means
finding drugs that kill *Mycobacterium tuberculosis* faster, and that choice is
made in a flask: the compounds that could shorten a regimen are picked out of in
vitro killing experiments.

The experiment is simple. Grow the organism, add the drug, and at set times take
a sample, dilute it, spread it on a plate, and count the colonies. Each colony
stands for one bacterium that was alive when it was plated. The counts over time
are the killing curve.

Every clinical microbiologist already knows the trap in that last step. A culture
taken after antibiotics have started is not evidence of sterility. It is why
blood cultures are drawn before the first dose. A drug suppresses growth, injures
cells sublethally, carries over into the medium, and drives the population
beneath what the plate can see; the plate then reports absence, and absence is
not what happened. The rule is old, it is correct, and nobody disputes it.

The plate also has a hard floor, and the pipette sets it. The smallest positive
result is one colony, and what one colony means depends on how much you spread.
Plate 100 µL and one colony is 10 bacteria per mL. That is the floor. Anything
below it comes back as no growth, which is not the same as nothing there. Write
*L* for that floor and *N₀* for the starting density.

Tuberculosis makes the old rule expensive, because the phenotype invoked to
explain why treatment takes so long is itself defined by a duration. That
phenotype is tolerance: the capacity of a genetically susceptible population to
survive an exposure that should kill it. These bacteria are not resistant. The
drug still works on them. They just take a long time to die, and that time is the
measurement. A phenotype defined by a duration is defined by exactly the
observation the old rule warns about.

The field's response was not to ignore the warning but to engineer around it.
Rather than asking whether a culture went negative, the modern definition asks
how many logs the population fell: the minimum duration for killing, MDK, is the
time to a specified fractional reduction — 90, 99 or 99.99 per cent — and it is
proposed as the tolerance counterpart to the minimum inhibitory concentration
(2, 3). The choice of a *fraction* is the whole point. A ratio to the
starting population is scale-free: if the count falls in a straight line on a log
scale at rate *b*, the time to a *q*-log reduction is *q/b*, and the starting
density cancels. By construction, MDK cannot be contaminated by how much culture
went into the tube. That is the property it was built to have.

The property holds in the definition. It does not hold in the measurement, and
the gap between the two is what this paper is about. To show a four-log kill you
have to be able to see four logs down. A *q*-log reduction can be estimated only
if *q* logs are visible, and what is visible is bounded below by the floor. So an
isolate has

    headroom  h = log10(N₀ / L)

and no experiment can demonstrate a reduction deeper than *h*, however completely
the drug worked. Where *h* < *q* the endpoint is unreachable before the drug is
added. That is the first boundary, and we call it reachability.

It gets worse when the last count lands on the floor. The fraction written down
is then *L/N₀* — the floor divided by the starting density. It is not a
measurement of how many survived. The drug has dropped out of it, and what is
left is the pipette and the inoculum. The metric designed to be
inoculum-independent becomes a pure inoculum readout precisely at the depth where
tolerance is scored. That is the second boundary, and we call it
identifiability.

The two failures are different in kind, and this paper keeps them apart. Whether
an endpoint is reachable at all is settled by the assay geometry before the drug
is added, since *h* depends only on the starting culture and the floor. Whether a
reading that has reached the floor can be classified is settled by the geometry
too, but only once the drug has driven the population down to it: reaching the
floor takes a reduction of the isolate's entire headroom, and that is the drug's
doing.

The bound is already in the papers that defined the assays. Vijay and colleagues,
introducing the most-probable-number MDK for rifampicin — a count read off a
dilution series rather than off colonies on a plate — treated an MDK99.99 longer
than ten days as high tolerance beyond the **time** window of the assay, not as a
statement about the count floor (4). In the 217-isolate classification that
follows from that assay they report that MDK99.99 at 15 days of recovery could be
calculated for only 22 of 209 isolates and that the rest lay, in their words,
"beyond the assay limits" (5). The ERA4TB consortium requires below- and
above-quantification-limit flags together with the limit of quantification, and
notes that pharmacometric models can use those flags (6); the same
six-laboratory comparison then excluded both from its numerical analysis. Their
2025 protocol states the geometry of the pipette explicitly: a 2.5 µL drop has a
limit of detection above 2.6 log10 CFU/mL, and a lower limit requires a larger
plated volume (7). Independently, a 2025 pharmacokinetic-pharmacodynamic
analysis of hollow-fibre CFU series showed that censoring counts below 10 CFU —
recording them only as "below the floor", with the true value unknown — biases
regimen ranking (8), and a within-host tuberculosis tolerance study chose a
shallower MDK threshold specifically so that more isolates could enter the
analysis (9).

The closest statement of the bound is in the framework's own methods paper, and
we claim no priority over it. Brauner and colleagues, presenting a direct
measurement of tolerance that deliberately avoids time-kill curves, scale the
inoculum to the endpoint being measured: a hundred bacteria per well to determine
MDK99, a thousand for MDK99.9, and so on (3). That is the reachability
inequality of this paper, with the floor idealised at one cell per well and a
grew-or-did-not-grow readout in place of a count. What has not been done is to
carry the rule back into plate-count time-kill, where the floor is not one cell
but a concentration fixed by the plated volume — 10 to 400 CFU/mL across the
deposits reanalysed here — and must therefore be measured sample by sample rather
than assumed; nor to ask what the published record looks like where the rule was
not applied.

The requirement is older still, and it is quantitative. NCCLS M26-A ties the
plated volume to the endpoint: after the defined 99.9 per cent killing, at least
ten colonies must remain to be counted. It separately requires the smallest
accurately detectable count to be established by serial dilution of a known
inoculum (10). What has happened since is that the endpoint moved and the rule
did not travel with it. The persistence field's own consensus guideline makes the
time-kill assay the starting point for identifying persistence and catalogues at
length what can go wrong with it — resistant mutants, heteroresistance, drug
degradation, adhesion to the vessel, washing and recovery conditions, delayed
colony appearance, culture density, inoculum history — and raises neither the
limit of detection, nor the plated volume, nor how deep a reduction the assay can
report (11).

None of these converts a floor-level reading into the classification rule it
becomes. When the last count sits at *L*, the recorded fraction is *L*/*N*₀, and
the low, medium or high label is then a cut on starting density. That is the gap
this paper fills. Two further failures have to be kept distinct from it. A
duration ceiling — the assay stopped looking — is not a count floor, which is the
plate being unable to see. And recording a below-limit flag is not the same as
scoring a duration from the points so recorded.

This is testable rather than arguable, because one published deposit assigns the
tolerance phenotype itself. Vijay and colleagues (5, 12) scored 217 clinical
*Mycobacterium tuberculosis* isolates as having low, medium or high tolerance to
rifampicin, and deposited alongside each call the starting most probable number,
the growth rate, the isoniazid susceptibility and the killing readings the call
was built from. The classification, the inputs to it, and the assay geometry that
bounds it are all in the same file.

This study asks how deep a log-reduction tolerance endpoint can be measured at
all, and whether real isolates have been assigned tolerance phenotypes from
outside that range. Two boundaries on the starting density follow from the
definitions — one deciding whether an endpoint is reachable, the other whether a
floor-level reading identifies a class — and both are computed from quantities a
time-kill protocol already records. Neither asks a laboratory to measure anything
new.

We then test the hypothesis that a deep log-reduction endpoint is
inoculum-dependent through what can be observed, even though it is
inoculum-independent in its definition, using the classification and the assay
geometry of 217 clinical isolates. We then ask what the resulting phenotype
tracks: drug susceptibility, or the physiological state of the culture. Two
further deposits establish that the same arithmetic governs killing experiments
where inoculum is controlled by protocol rather than by clinical accident: a
six-laboratory consortium exercise distributing one strain under one written
protocol (6, 13), and a concentration-by-time grid in the same organism
(14, 15). From the first we also ask whether a faster-killing flask reliably
crosses the floor sooner. From the second, whether a late endpoint can erase a
dose difference that an early one resolves. A fourth deposit (16, 17), held
out until every boundary was fixed, tests whether the boundaries locate the same
depth in an experiment they were not built from. Finally we ask whether the
concentration and duration axes are separate in these files, which is the premise
the framework defining them rests on. All five deposits are published and openly
licensed, and none was generated for this study (Table 1). The two boundaries are
then tested forward rather than backward, in a prospective experiment built to
break them, with every prediction written down before a plate was counted.

If the hypothesis holds, a tolerance call reported without its starting density
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
*L*. And the recorded fraction is then *L*/*N*₀, a monotone decreasing function
of *N*₀, so its rank correlation with *N*₀ is
−1 whatever the numbers are, including random ones. Both follow from the
definition of a censored reading, and neither is evidence about a drug.

What is testable is what happens when one sample is plated at two volumes under a
fixed class threshold. If both readings sit at their own floors the labels are
*L*₁/*N*₀ and *L*₂/*N*₀, and they differ only when those two fractions fall on
opposite sides of the cut — which is again arithmetic. The empirical quantity is
how often a real experiment lands in that window. It could be none of the time.


---

## Results



### 1. The plate's floor sets how far down killing can be seen

The most probable number (MPN) readings can only take the discrete values of an
MPN table (18, 19) — a fixed ladder of rungs, not a continuous scale. The
day-5 column does not taper towards zero. It stops. Eighteen isolates sit at
exactly 23 per mL in the 15-day panel and six in the 60-day panel, and nothing in
the file lies below that (Fig. 1A). That is a floor, not a tail, and it is
treated as one throughout.

The deposit never states its limit of quantification (12), so the floor has to
be inferred, and the inference is quantified rather than asserted. A posterior
over the MPN rungs at or below the lowest observed value — a probability spread
across which rung is the real floor — places 95 per cent support on 9.2 to 23 per
mL, a span of 0.40 log10. That is narrow enough that the class labels of
Section 3 are computed rather than refused (Table S1). Where a deposit gives no
such evidence, the labels are refused instead of reported.

The deposit carries a second classification, scored at day 2, and it sits on a
different floor. The day-2 column bottoms out at 230 per mL with eighteen
readings resting there, so *L* = 230 there. The day-2 class thresholds are not
stated in the source either, and they are recovered the same way as the day-5
ones: cuts at 10⁻² and 10⁻¹ reproduce all 203 usable day-2 classes with no
disagreement, one decade shallower than at day 5. Floor and lowest threshold both
shift by a factor of ten, so the identifiability boundary does not move:
*N*_id = 230/10⁻² = 23 000 per mL, the same value as at day 5. The reachability
boundary does move, by a decade, and the consequence is large. Against the day-2
floor, 121 of 203 isolates have too little room for a four-log reduction; against
the day-5 floor, 31 of those 203 isolates do. Eighteen day-2 readings rest on
their floor, eleven with a single compatible class and seven with more than one.
At 60 days no pair of decade cuts reproduces the day-2 classes (109 of 197), so
that rule is not a decade threshold on the recorded fraction, and no day-2
accounting is offered for it.

Each isolate therefore carries a fixed budget of killing the assay can see. At 15
days of prior culture the starting densities span 3.36 to 7.79 log10, so headroom
— the distance from the starting density down to the floor — spans 2.00 to 6.42
log10 (Fig. 1B, Table 2). Both spans are the same 4.42 log10, and the fold
figures quoted throughout are ten raised to the unrounded difference rather than
to the displayed one. Against that budget the three deposited endpoints behave
very differently. Every isolate has the room for a 90 or a 99 per cent reduction:
0 of 217 fall short in both cases. **Thirty-three of 217 isolates — 15.2 per
cent — lack the headroom for the 99.99 per cent endpoint**, which is to say that
a four-log reduction was unobservable for them before rifampicin was added. Two
of those 33 carry a fourth label that the deposit writes literally as "MDR",
conventionally multidrug-resistant. It is unordered with respect to the other
three, so no ordered analysis can place it (Table S2); over the 203 isolates with
an ordered label the same count is the 31 quoted above.

All 33 are recorded as not having reached the endpoint — they sit at the **assay
ceiling**. That is a census of the affected isolates rather than an estimate, and
it is the load-bearing observation. The ceiling is a different censoring
mechanism from the floor and should not be read as its mirror. The floor censors
the count: anything below *L* is not reported as a count. The ceiling censors
time: the killing assay runs six days, so an isolate that has not reached its
endpoint by then is recorded at the last day rather than at the day it would have
reached. One sets how deep the assay can see, the other how long it looks.
Among the 184 isolates that did have four logs of headroom, 162 are also at the
ceiling, 88.0 per cent.

No p-value is attached to that contrast, and the reason is worth saying out loud
rather than hiding in a caveat. An isolate with less than four logs of headroom
cannot record a four-log reduction. The 0 of 33 cell is fixed by arithmetic, not
by biology, so the null of independence between ceiling status and headroom is
false before any data are seen. A test of an impossible null still returns a
number, and that number means nothing. The census is the finding: every isolate
that could not reach the endpoint is recorded as not having reached it, and 88.0
per cent of those that could are recorded the same way. The deepest endpoint is
therefore the only one at risk, and it is the one the tolerance classification is
built on.

### 2. The same floor reading was given different tolerance labels

The deposited tolerance level is a cut-off on the recorded surviving fraction,
with no overlap between classes. The thresholds themselves are not deposited.
They are recovered here, and the data pin them only to the gaps between classes:
at day 5 and 15 days of prior culture, low tolerance covers fractions below 10⁻³,
medium covers 10⁻³ to 10⁻², and high exceeds 10⁻². Those cuts reproduce every
usable class in the file, 203 of 203 (Table S3). Usable means the 203 of 217
isolates whose label is one of the three ordered classes; the other 14 carry the
fourth, unordered category, the "MDR" label above, that no ordered analysis can
place (Table S2). So what follows is an argument about the fraction the assay
recorded, not about an independent clinical judgement.

Eighteen isolates ended at the floor. They share one reported floor-level
observation, but their true final counts are unknown below the floor, so the
assay cannot tell their surviving burdens apart down there. That is not the same
as saying they were killed to the same degree, and the difference matters. Their
starting densities span 265-fold, from 23 000 to 6.1 × 10⁶ per mL, so the same
terminal reading implies a different range of compatible reductions in each. An
isolate that began at 23 000 has demonstrated at least a 3.00-log reduction; one
that began at 6.1 × 10⁶ at least 5.42 logs. In either case the true reduction may
be anything from that bound down to complete kill. What the deposit records
instead is a single number per isolate, *L*/*N₀*, and those recorded fractions
span 265-fold, from 3.8 × 10⁻⁶ to 1.0 × 10⁻³ — exactly the span of the starting
densities (Fig. 1C), because that is what the ratio is. They are upper bounds on
survival, not measurements of it.

The labels those eighteen received differ. Six isolates that began at 23 000 per
mL received a fraction of 10⁻³ and were classified **medium** tolerance; twelve
that began at 230 000 or above received 10⁻⁴ or less and were classified **low**.
A single cut on the starting density alone reproduces all eighteen (Table 3).
That is a statement about the classification step and not about the killing: once
a reading is censored at the floor, the starting density fixes which label the
published rule is able to return.

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

The larger effect is at the deeper endpoint, and it falls unevenly on the groups
a study would compare. The 99.99 per cent endpoint is unreachable for 22 of 84
isoniazid-resistant isolates, 26.2 per cent, against 9 of 119 susceptible ones,
7.6 per cent (Fisher exact p = 0.00056 (20)); the remaining two of the 33 are
MDR and fall outside that contrast. Their median headroom differs by a full log,
4 against 5. A comparison of tolerance between those groups is therefore in part
a comparison of how well each group could be measured, which is the disposition
the previous section quantifies.

### 3. The affected isolates are named before the drug is added

Sections 1 and 2 counted isolates. The two boundaries derived in the Methods
do more than that. Given
only the floor, the class thresholds and each isolate's starting density, they
say in advance which isolates are affected, before any day-5 reading is used.

For this assay *N*_reach = 23 × 10⁴ = 230 000 per mL and *N*_id = 23/10⁻³ =
23 000 per mL. Applied to the 15-day panel, the first predicts 33 isolates unable
to reach the 99.99 per cent endpoint. The second predicts that of the eighteen
isolates whose reading rests on the floor, twelve have only the lowest class
compatible with that reading and six have more than one. Those are the three
counts Sections 1 and 2 report.

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

How finely the agreement resolves also has to be stated. Among the eighteen the
starting density takes only five values — 23 000 for six isolates, then 230 000
for eight, and 610 000, 2.3 × 10⁶ and 6.1 × 10⁶ for one, one and two — and **no
isolate lies strictly between *N*_id and *N*_reach**. Any cut placed anywhere in
that decade reproduces the same twelve-six split, so the split locates the
boundary only to within an order of magnitude and is not by itself a sharp test
of where it sits.

What is sharp is the boundary case, and it is the part of this section that
discriminates. Six isolates sit at exactly 23 000 per mL, which is *N*_id itself.
For them *L*/*N₀* equals *c*₁ exactly, the interval [0, *L*/*N₀*] touches the
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

### 4. The label tracks how fast an isolate grows, and its link to resistance cannot be separated from the inoculum

We asked what the deposited tolerance label goes with. There are two candidate
predictors, and each is tested at two culture ages and at two endpoint depths,
which is eight tests in all. Eight tests on one question will throw up a false
positive on their own, so we correct them together as one family. Two survive
(Table S4).

The label tracks the **growth rate** of the isolate. Slower growth goes with a
higher tolerance class, and it survives adjustment for starting density
(OR 1.096 per day of time to OD 0.4, 95 per cent CI 1.032 to 1.164, p = 0.0030,
n = 202; unadjusted OR 1.126, 1.062 to 1.193). The label also tracks **isoniazid
resistance** — until the starting density enters the model. On its own, a
resistant isolate has 2.32 times the odds of a higher tolerance class (95 per
cent CI 1.30 to 4.12, p = 0.0042). Adjusted for starting density the odds ratio
falls to 1.31 (0.67 to 2.57, p = 0.42), and the interval no longer excludes one.
We call that attenuation, not elimination. Starting density is the strongest
term in the file: every ten-fold rise in the starting most probable number halves
the odds of a higher tolerance class (OR 0.480, 0.340 to 0.677,
p = 2.9 × 10⁻⁵).

Why the adjustment does that is measurable. Isoniazid-resistant isolates go into
this assay at 5.36 log10 against 6.36 for susceptible isolates, ten-fold thinner
(Mann–Whitney p = 9.1 × 10⁻¹⁴) (21), and 26.2 per cent of them lack the
headroom for the deepest endpoint against 7.6 per cent of susceptible isolates
(Section 2). They are one log short of observable killing before the experiment
begins.

A percentage attenuation is a description, not a quantity a model estimates, so
we estimated the path directly. The total effect of resistance on the tolerance
class splits into two parts: the part that runs through log10 starting density
and the part that does not. On the 203 isolates with a usable class, rather than
the 202 the association family retains, the mediated part is +0.166 classes
(bootstrap 95 per cent CI +0.067 to +0.279) and the direct part +0.091 (−0.116 to
+0.287). About 65 per cent of the association therefore travels through the
inoculum, and the direct path covers zero. Restricting to baseline isolates
leaves the mediated path intact (+0.159, +0.053 to +0.295), and collapsing the
outcome to two levels agrees (Table S5).

Two things bound that estimate, and neither is a formality. It rests on
sequential ignorability — that nothing unmeasured drives both the starting
density and the class — which no observational file can establish. A residual
correlation of about −0.23 between the mediator and outcome errors would nullify
the point estimate, and one ordinary measured covariate already moves it about
forty per cent of that way. More fundamentally, the step in the middle is the
denominator of the ratio the outcome is cut on. The tolerance class is a
threshold on *N*₅/*N₀*, so a decomposition that routes resistance through *N₀* is
in part recovering the censoring arithmetic this paper is about rather than a
biological pathway from resistance to tolerance. That is not a reason to discard
the estimate — it is the quantity a reader wants, because it says how much of the
association is carried by the label's own denominator — but it is a reason not to
read it as a mechanism. Only a design that fixes the inoculum separates the two.

That last objection can be tested rather than merely conceded, because the
isolates it applies to can be named. The recorded fraction is *L*/*N₀* exactly
for the eighteen isolates whose day-5 reading sits on the floor, and for no
others: in the remaining 185 the numerator was counted and is free to move
independently of *N₀*. Refit on those 185 alone and the mediated path does not
weaken but strengthens, to +0.227 classes (+0.118 to +0.348), while the direct
path collapses to +0.008 (−0.197 to +0.208) and the proportion mediated rises
from 0.65 to 0.96. Deleting exactly the isolates the criticism is about leaves
the effect larger, so it is not an artefact of them. What it remains is an
association in observational data, and the caution above about mechanism is
unaffected.

These 217 isolates are not 217 independent patients, and the deposit carries no
patient key with which to say so in a standard error. What it does carry is the
exact substitute: a baseline-only stratum in which every isolate comes from a
different patient by construction (Time_point = 0M, n = 167 at 15 days).

In that stratum the two surviving associations part company. Growth holds and
still survives correction (OR 1.116, 1.040 to 1.198, p = 0.0024). Resistance does
not: OR 2.11 (1.07 to 4.16, p = 0.031). It ranks second in the family of eight,
so under Benjamini–Hochberg it must beat a critical value of 0.0125, and it does
not. The resistance association therefore leans on isolates that are not
independent of one another, and it is already the association that starting
density explains away. We report it as the weaker of the two on both counts.

The two surviving associations sit in the 15-day panel, which is where the
mechanism places them. By 60 days the cultures are 38-fold denser, the spread of
starting densities has more than halved, from an interquartile range of 1.00 to
0.42 log10, and the fraction of isolates short of headroom falls from 15.2 to 3.3
per cent. The confound is a property of a thin assay, and it thins out when the
assay is not thin. The two panels are columns on the same spreadsheet rows — 210
isolates appear in both — so every comparison between them is within-isolate and
is made that way. Pairing sharpens the result rather than softening it: 26
isolates lose their headroom shortfall between panels and none acquires one
(exact McNemar p = 3.0 × 10⁻⁸ against an unpaired p of 2 × 10⁻⁵) (22), eleven
leave the floor and none joins it (p = 9.8 × 10⁻⁴), and every isolate whose
headroom changes gains (Wilcoxon signed-rank p = 1.3 × 10⁻³³) (23). The
interquartile range of starting density falls by 0.58 log10.

It does not vanish, and the ordinal treatment is what shows where it goes. The
one-odds-ratio-for-both-cuts assumption holds throughout the 15-day panel but
fails at 60 days for starting density at the deepest endpoint (Brant p = 0.0031;
likelihood-ratio test against a released fit p = 0.0062). Let that coefficient
differ between the two cuts and the whole effect lands on the upper one: the odds
ratio for clearing medium is 0.493 (0.336 to 0.724, p = 0.0003) against 0.951 for
clearing low (0.647 to 1.396, p = 0.80). A multinomial fit, which assumes no
ordering at all, agrees (high against low, relative risk ratio 0.59, p = 0.028;
medium against low, 1.22, p = 0.39). In the denser panel the starting density no
longer decides who is called low. It still decides who can be called high. A
single averaged slope, ordinal or linear, would have reported that as a null.

### 5. One written protocol does not give every laboratory the same depth to look down

If the effect is a property of assay geometry rather than of clinical sampling,
it should appear where one protocol, one strain and one stock are handed out
deliberately. Van Wijk and colleagues (2023) ran exactly that exercise, sending a
single stock of H37Rv to six blinded laboratories under one written protocol
(6, 13). It does.

At ten times the minimum inhibitory concentration of moxifloxacin all six
laboratories return a positive kill rate, and the rates span 5.2-fold, from 0.090
to 0.464 log10 CFU/mL per day. Across all 30 laboratory-by-arm cells the Tobit
estimate — a fit that treats a below-floor reading as below the floor rather than
as a number — and the imputation estimate never differ by more than 0.006 log10
per day (Fig. 2A, Table S6). That agreement says the fit is not an artefact of the
arithmetic used to reach it. It does not say the sub-floor assumption is safe:
both estimators assume the same normal distribution below the floor, and nothing
in this deposit can check that assumption from the inside.

The duration endpoint behaves differently on the same flasks. What it records is
not clearance and not sterilisation. It is a **first observed crossing below the
assay floor**, and the distinction is not pedantic: most series that cross later
read above the floor again, including all five untreated series that cross. The
plating volume has to be stated too, because the endpoint depends on it. The
time-to-event analysis runs at the 100 µL quadruplicate plating, the most
sensitive of the four, and there 29 of 72 treated flasks ever fall below the
floor: institutes B and C record crossings in every arm, institute A in three of
its four, and institutes D, E and F in none (Fig. S1A). For half the laboratories
the first-crossing time is therefore right-censored throughout — the flask never
crossed, so all that is known is that the crossing, if it comes, comes after the
last visit.

That split is a property of the plating, not of the laboratories. Counting a
crossing on **any** of the four platings gives 48 of the same 72 treated flasks,
and every laboratory records at least one — D six of its twelve, E one, F ten.
The two counts are the same fact seen at two sensitivities, and they are exactly
what this paper is about: a duration endpoint is defined against a floor, and the
floor is a choice. The analysis keeps the single most sensitive plating so that
the endpoint means the same thing everywhere, and reports here what the other
choice would have shown.

The two orderings do not correspond. Rank the laboratories by starting density
and the three lowest are exactly the three that recorded crossings, the three
highest exactly the three that did not, without exception. Rank them by kill rate
and there is no such correspondence (Fig. 2B). Institute F has the highest
starting density at 6.53 log10 among the treated flasks of this arm, kills
faster than four of the other five at 0.223
log10 per day, and records no crossing. Institute E returns the slowest rate of
all at 0.090 and also records none.

Starting density separates the flasks that ever crossed from those that never did
with an area under the curve of 0.974. That figure is a description, and it is
quoted without a p-value on purpose. The comparison looks like 67 flasks, but it
is three laboratories against three, and the between-laboratory evidence in this
deposit is six clusters throughout; the Limitations set out what that permits and
what it forbids. In short: the exact laboratory-level test returns 0.10, which is
the smallest value the design can return, and once the treatment arm is held
fixed there is no within-laboratory comparison left to fall back on.

The Cox fits are reported for the same reason and with the same restraint. On
laboratory alone, institutes D, E and F carry hazard ratios of 0.20, 0.21 and
0.20. Add starting density and those move to 0.34, 0.36 and 0.62, and concordance
rises from 0.896 to 0.930 (Fig. S1B). Institute C moves the other way, from 3.0
to 5.3, and it is also the fastest killer, which is how a laboratory that
genuinely kills faster ought to behave. No p-value is attached to any of these
terms, and the panel that displays them displays that movement rather than
testing it. The reason is mechanical. The tested covariate is constant within
cluster, and with six laboratories and six parameters the cluster-robust
covariance is singular by construction; fitting it anyway does not fail loudly
but returns a smaller p than the one it was meant to correct. A coefficient that
moves on adjustment says how far starting density and laboratory identity overlap
in this design. It is not evidence that one explains the other.

Killing here is not sustained, and this is stronger than a caveat about
individual flasks. Take the 64 treated series carrying at least three quantified
readings at the most sensitive plating volume. In 48 of them the final step is
not a decline, and 44 end more than one log10 above their own lowest reading,
with a median rebound of 2.17 log10 and a largest of 5.54. Seventeen of the 32
flasks that fell below the floor at the most sensitive plating — the 29 treated
flasks above and three untreated ones — were detectable again at a later visit,
14 of them in treated arms.

Across all four platings, 84 of the 140 series that cross return above the floor,
60 per cent, and the return is quick: a median of four days, with 45 per cent
back within three. Those 360 series come from 90 flasks, four platings each, so
they are not 360 independent observations; counted by flask, 53 of the 90 contain
a crossing series — the 48 treated flasks above and five untreated ones — and 42
of those contain a returning one. A crossing below the assay floor in this
deposit is therefore usually a transient rather than an endpoint, which is a
further reason it summarises less than the trajectory that produced it. Killing
itself is real and dose-dependent: at one times the inhibitory concentration five
of six laboratories record net growth under moxifloxacin, between −0.047 and
−0.214 log10 per day, and at ten times all six record net decline.

Two consequences follow, and they matter for anyone who reads a duration off such
an experiment. The first is that the state below the floor is not absorbing: a
series that drops below it does not stay there. Of 2 232 visit-to-visit
transitions, 144 go from above to below and 95 go from below to above, so a
series sitting below the floor leaves it at the next visit with probability 0.22.
The gradient runs with drug pressure — that probability is 1.00 in untreated
series, 0.37 to 0.92 at one times MIC and 0.07 to 0.18 at ten times — which says
the event is at least partly a property of the plate rather than of the drug. Of
the 360 series, only 56, or 15.6 per cent, show the shape a survival model
assumes: one crossing that holds (Table S7). Two hundred and twenty never cross
at all, 65 cross and return, and 19 oscillate more than once.

The second is that the crossing time is never observed. It lies between the last
visit above the floor and the first visit below it, and the naive treatment pins
it to the later end, which biases every duration late by construction rather than
merely imprecisely. Fitted as interval-censored data — the crossing recorded as
lying somewhere inside a window rather than at a point (24) — at the most
sensitive plating, the tenth percentile of the first crossing falls from 2.95 to
1.82 days and the twenty-fifth from 11.24 to 9.64; across the treated arms at all
four platings the twenty-fifth percentile falls from 5.77 to 3.67 days, a 36 per
cent shortening. The non-parametric estimate behaves differently, and the
difference is instructive. Fitted on the half-open interval the data actually
give — the crossing happened after the last visit that read above the floor, and
at or before the first that read below — the Turnbull curve agrees with the naive
Kaplan–Meier at every visit, to floating-point precision. That is not a
coincidence: the crossing intervals are the visit gaps themselves, so between
visits there is nothing left for a non-parametric estimator to identify, and the
naive pinning costs nothing at the visits. What the pinning costs is everything
between them, which is where the parametric fit puts the shortening above. A
duration read off the naive curve is therefore too long, and by about a day at
the depths that matter.

What the adjustment establishes is descriptive and is worth stating as such: a
continuous measure of where the cultures began accounts for the laboratory term
at least as well as the laboratory label does, and one institute resists even
that. What can be tested, because flasks are exchangeable across laboratories
under the null, is how much of each quantity the laboratory owns. It owns 87.0
per cent of the variance in starting density (permutation p < 0.0002) and 36.8
per cent of the within-arm kill rate (p = 0.0018). It owns the duration endpoint
outright, since three laboratories produce none at all.

### 6. The same boundaries hold in an experiment the framework never saw

Every section so far tests the framework on the deposits it was built from, and
all of them are *Mycobacterium tuberculosis*. A search of five general
repositories, the tuberculosis consortia, the persistence literature, food
microbiology and the hollow-fibre field returned one deposit that carried all
three fields the boundaries require and could be analysed cold.

That was true of the search as described. It is no longer true of the analysis
repository, which now holds 40 ingested deposits. Of those, 17 permit the
boundaries to be computed once the floor is established on the same tiers this
paper uses for its own: stated by the depositor, derived from a recorded plated
volume, or inferred from a pile-up of counts on a plate-plausible value. Across
those, the condition the boundaries imply — that no series may present as a
measurement a reduction deeper than its own floor allows — holds in 2 210 of
2 210 series in seven species. Those deposits are described in the data release
rather than here, because none was held out. The point of this section is a
deposit opened after every boundary and threshold was fixed, and only one
qualifies on that ground.

Dubey and colleagues (2026) report amoxicillin-clavulanate against *Escherichia
coli* in a hollow-fibre system (16, 17). Their Methods state 100 µL plated
with counts per mL, so *L* = 10 CFU/mL is derived rather than inferred, and the
file corroborates the derivation: a 100 µL plate reporting per mL can return only
multiples of ten, and all 229 genuine counts in the deposit are multiples of ten,
the smallest exactly ten. Sixty-nine further entries read as one, which no 100 µL
plate can produce; they are the deposit's placeholder for below the floor.

Across the 20 cultures with a measured day-zero density, headroom runs from 4.85
to 5.45 log10. Endpoints at 1, 2, 3 and 4 logs are reachable for every culture. A
5-log endpoint is unreachable for 5 of 20. A 6-log endpoint is unreachable for all
20 (Table S8). On data it was not built from, the framework therefore locates the
depth at which a sterilisation claim in this experiment stops being demonstrable.

Two features of that deposit are worth recording because they are the failure
modes this framework is meant to catch. Its Methods give a nominal inoculum of
10⁵ CFU/mL while the file measures a median of 1.215 × 10⁶, so taking *N₀* from
the Methods rather than from the data would have placed a full order of magnitude
into every boundary. And its treated arm reads at or below the floor already at
day zero while the paired control reads about 10⁶, so that sample was drawn after
exposure rather than before it.

### 7. Read the plate late enough and a 32-fold dose difference disappears

The deposit tests apramycin at 1, 4, 8, 32 and 128 µg/mL (14, 15). The 1 µg/mL
flasks grow rather than die, so that arm is left out of the dose comparison. What
remains is 4 to 128 µg/mL: 32-fold, five doublings. Across that range the
survivor counts spread out 6.9-fold at day 3, 48.2-fold at day 7 and 5.2-fold at
day 14 (Fig. 3, Table S9). The spread opens, then closes again. An experiment
read at 14 days would report this drug as insensitive to a 32-fold change in
dose. Each interval is fitted on its own, resampling all three replicate counts
with replacement at both ends of every interval, 20 000 draws. Over days 0 to 3,
each doubling of the dose adds +0.059 log10 per day to the kill rate (95 per cent
percentile interval +0.033 to +0.083). Over days 3 to 7 it adds +0.033 (+0.008 to
+0.059). Over days 7 to 14 it adds −0.025 (−0.035 to −0.015). Early against late
is a firm difference (+0.084, +0.055 to +0.111). Early against middle is not
(+0.026, −0.011 to +0.062). So concentration dependence is positive early, still
positive but smaller in the middle, and reversed late — and the reversal, not
just the shrinkage, is what a 14-day readout would be measuring.

We do not claim the late slope is truly negative. By day 14 the highest arm is
down to 65 CFU/mL, and the deposit states no limit of quantification and no
plated volume, so its floor cannot be worked out. Put the floor at 100 CFU/mL or
above — the value 10 µL plating would give, an assumption and not a derivation —
and that arm has already dropped below what its plate can count. Its readings are
then censored: recorded only as "below the floor", true value unknown. The rate
read off them is a lower bound. What holds whatever the floor turns out to be is
that the separation collapses.

### 8. One culture, two plated volumes, two tolerance labels

Every result above reads data somebody else generated for another purpose. This
one reads an experiment built to try to break the two boundaries *N*_reach and
*N*_id — the starting densities that decide whether an endpoint is reachable and
a label means anything — with its predictions written down before a plate was
counted. *Escherichia coli* ATCC 25922, of the American Type Culture
Collection — the reference strain the standard names for quality control —
against ciprofloxacin at ten times the concentration that stops it growing. Three
seeding densities, two plated volumes, three flasks each, 216 plate readings.

The middle arm was seeded on purpose at the 5 × 10⁵ per mL the standard
specifies. The densities actually reached were 6.4 × 10⁴, 4.4 × 10⁵ and
3.8 × 10⁶ per mL. **At the standard inoculum plated at 10 µL, the deepest
reduction the three flasks could report ran from 3.71 to 3.93 logs — each arm's
own ceiling, not the drug's** — while those same three cultures plated at 100 µL
ran from 4.88 to 5.05 (Table S10). Every flask is paired with itself across the
two platings, so the comparison is within a culture rather than between
cultures.

The gain the pipette buys is exactly one log, because the floor at the pooled
100 µL plating is one tenth of the floor at the pooled 10 µL plating. The nine
paired gains are not exactly one log: they run 0.87 to 1.19 (Table S10). The
difference is not the drug and not the flask. It is that each plating measures
its own starting density from the same culture, and the two measurements
disagree — 425,000 against 565,000 per mL in one flask, 255,000 against 375,000
in another. That disagreement is this paper's own argument turned on its own
experiment: *N*₀ is not a constant a protocol supplies, it is a measurement with
error, and the headroom computed from it inherits that error. Reported per
flask, the gain never falls below 0.87 log10, so the four-log endpoint moves
from unreportable to reportable in every one of the three cultures at the
standard inoculum.

That much is arithmetic, as Box 1 says. So is the next step. When both platings
of one sample rest on their own floors, the two fractions written down are
*L*₁/*N*₀ and *L*₂/*N*₀ — two different floors over one starting density — so
they can fall either side of a class threshold and give one culture two labels.
**The quantity that could have come out zero is how often a real experiment lands
in the window where those two fractions straddle the cut**, and it depends on
where the cut is (Table S11). Put the cut at one per cent and the window is
nearly shut. Put it at one in a thousand, which is where the clinical
classification analysed above cuts its lowest class, and six of 54 sample-times
receive two different labels from one culture — one in nine.

That figure is computed with a single starting density per flask, and it has to
be, because the sentence above says *L*₁/*N*₀ and *L*₂/*N*₀ — one denominator.
The experiment can also be read the way a laboratory would actually run it, with
each plating series carrying the starting density it measured for itself, and
then the count is nine of 54 rather than six. The three extra are not the pipette.
They are the two platings disagreeing about how much culture went in: across the
nine flasks those two estimates differ by 0.74- to 1.53-fold, median 1.12. Both
numbers belong in the record. Six is what the plated volume does on its own, and
it is the claim this section makes; nine is what a laboratory would see, because
in a real experiment the starting density is measured too, and it is measured
with error.

---

## Discussion



### What fails, and where

Every clinical microbiologist knows that a negative culture taken under
antibiotic exposure is not proof of sterility. That is not what this paper
reports. What it reports is that the number brought in to replace that judgement
carries the same defect — and once it is a number, it is harder to see.

The minimum duration for killing was built to be scale-free. It reports a
fraction, and a fraction divides out the starting density. That is the property
meant to make it the time-side counterpart of the minimum inhibitory
concentration.

The property holds in the definition. It fails in the measurement, for a reason
that is arithmetic, not statistical. A *q*-log reduction can only be seen where
*q* logs are visible below where you started. When the last count rests on the
plate's floor, the fraction written down collapses to *L*/*N₀* — the floor
divided by the starting culture. The drug has dropped out of it.

Fifteen per cent of the clinical isolates examined here could not have shown the
deepest endpoint whatever the drug did to them, and every one of them is
recorded as having failed to show it. Eighteen isolates ended at the same
censored value — recorded only as below the floor, true value unknown — and
their tolerance labels are reproduced exactly by a single threshold on their
starting density. To see why, sweep the true count across the range the floor
allows. For twelve of them only one class fits a censored reading, so the
published rule had no other label to give. For the other six the compatible
range straddles a threshold, so the rule cannot choose at all. Whether those
cultures reached the floor is a question about rifampicin. Which label they
received once they were there is a question about arithmetic, and the starting
density settles it.

It is worth saying how far this reaches. The claim is scoped to the floor and no
further. In the 15-day panel, 12 of 203 usable calls have a single compatible
class and 6 have more than one; the other 185 rest on a fraction that was
actually measured. The kill rate still carries more of the variance in crossing
time than the distance does, in every multi-laboratory arm. So what fails
everywhere is not every tolerance call. It is the *interpretability* of a deep
log-reduction call reported without *N₀* and *L*. What the inoculum settles is
the subset of labels for which killing had already reached the floor.

The failure is specific and it is bounded. In this deposit neither the 90 nor
the 99 per cent endpoint is compromised: every isolate has the room to show
both. It is the 99.99 per cent endpoint that a substantial minority cannot
reach, and that is the deep endpoint the clinical classification uses. Being
that specific is what makes the problem fixable rather than fatal.

This is a derivation rather than an observation, which is what lets anyone test
it on their own plates. Both boundaries follow from the definitions alone, and
neither refers to the drug or the strain. Give them a floor, a set of class
thresholds and a starting density, and they name the affected isolates in
advance. In the clinical deposit they name them exactly, isolate by isolate —
though for the twelve with a single compatible class that agreement is forced by
the class rule rather than an independent test. What could have gone the other
way is the boundary itself: six isolates sit at *N*_id exactly, the strict
inequality leaves them undecidable, and the deposit records all six as medium
rather than low. In a deposit the framework was not built from, the same
arithmetic locates the depth at which a sterilisation claim stops being
demonstrable: five of twenty cultures cannot show a five-log reduction, and none
of the twenty can show six.

Everything above is read backwards, out of files made for other purposes, and a
derivation that only explains the past is worth less than one that survives
being aimed at the future. So *N*_reach and *N*_id were used to design an
experiment against themselves, with the predictions written down before a plate
was counted. At the inoculum the standard specifies, the deepest reduction the
three cultures could report ran 3.71 to 3.93 logs at the 10 µL plating and 4.88
to 5.05 at 100 µL. The four-log endpoint was unreportable at one plating and
comfortable at the other — same flask, same afternoon. That much is arithmetic
and could not have failed. What could have failed is whether a real experiment
ever lands in the window where the two platings fall on opposite sides of a
class threshold, and at the cut the clinical classification uses it does so for
six of 54 sample-times with the starting density held to one value per flask, and
for nine when each plating carries its own — one culture, two labels, and nothing
between them but the pipette and the error in measuring what went in. That is reachability working as a design constraint rather than as
an explanation after the fact, and it is why the calculation in Box 1 belongs
before an experiment rather than after it.

What sits beneath the floor is the one thing a plate cannot report, and it has
been measured. Evangelopoulos and colleagues counted the same mouse lungs three
ways — colony count, a molecular bacterial load from 16S rRNA, and a most
probable number — on their way to a different question (25). Under the
deepest regimens the colony count reads zero in every animal. In three arms, 18
lungs in all, the plate declared every lung sterile while the most probable
number on that same tissue ran from 1 450 to 18 700 per lung. The molecular load
can be dismissed as nucleic acid outliving its owner. The most probable number
cannot, because it is a culture, and growth in a dilution series requires an
organism that is alive and culturable. Those lungs held thousands of viable
bacilli, and the plate that reported them sterile could not see them. This is
the region a relapse comes from, and in the mouse model used to decide which
regimens enter clinical trials it is the region a colony count is blind to.

That is also where the counts feeding regimen selection are taken. A model
published as a preprint while this paper was in preparation predicts relapse in
the murine model from lung CFU at 28 days together with a ribosomal RNA
synthesis ratio, across nine datasets, 58 regimens and 2 239 relapse
observations, reaching an area under the curve of 0.90 on external validation
(26). Its own reported finding is that CFU alone performs about as well as
CFU with the RS ratio, once the sterilising contribution of the individual drugs
is accounted for. That is what a censored covariate looks like from the outside:
where the best regimens drive the count onto the floor the count stops
separating them, and a term standing for drug identity takes over the
discrimination the count can no longer supply. Version 1 of that preprint
reports no detection limit and no plated fraction, and we do not read this as a
lapse peculiar to it — the field's own consensus guideline raises neither. It is
precisely why *N*_reach and *N*_id are worth writing down. A relapse model
resting on a 28-day count needs that count treated as left-censored — read as
below the floor rather than as a number — and *h* says when the question arises
instead of leaving it to be noticed.

A reader may object that this runs backwards. Dropping below the limit of
detection is what a *susceptible* population does; how can it make an isolate
look more tolerant? The objection is a fair one, and it is answered by
separating two endpoints that the literature reports side by side.

A duration endpoint asks when a fixed depth was reached. An isolate without the
room that depth requires cannot reach it under any drug effect whatever, so what
the file records is not a short duration but no duration at all: the isolate is
censored at the end of observation, which is the top of the scale and therefore
the most tolerant value it can take. Of the 217 isolates, 33 lack the range for
the 99.99 per cent endpoint the classification uses, and 33 of those 33 are
recorded at that ceiling, against 162 of the 184 with ample room.
The isolates that could not demonstrate the endpoint are,
without exception, the ones recorded as having failed to reach it.

A class endpoint asks how far the population fell by a fixed time, and there the
arithmetic does not merely preserve the direction — it inverts it. Once the
final reading sits on the floor the recorded fraction is *L*/*N₀*, and with *L*
fixed a *lower* starting density yields a *larger* recorded fraction. A larger
surviving fraction is a higher tolerance class, not a lower one. Eighteen
isolates ended at the same floor value at day 5. Their starting densities span
265-fold; their recorded apparent survival spans 265-fold. The two agree to
every digit because they are the same quantity, and the labels split
accordingly, twelve low and six medium.

Neither route asks anyone to mistake a sterile culture for a surviving one. In
the first the assay returns no endpoint. In the second it returns the floor
divided by the inoculum. What is read as biology is, in both cases, a property
of the measurement.

The same arithmetic answers the objection that the starting density is fixed by
protocol. It is fixed as a turbidity, and a turbidity is not a viable count.
Under one written protocol the densities actually achieved differed enough to
move the deepest demonstrable kill by 2.33 log10 between laboratories, and by
4.40 once the choice of plated volume is included. Those are two unlike
quantities and the paper keeps them apart: 1.6 log10 of the 4.40 is exact
arithmetic on *L* = 1000/*v* and carries no sampling uncertainty at all, while
the density part is a range over the four laboratories that deposit an untreated
day-zero reading at the 100 µL plating, and its cluster bootstrap runs 0.05 to
2.33 log10. The exact part is the stronger half. The choice of plated volume is
what
sets the floor.

The standard is not silent on that choice, and this is the paper's sharpest
finding rather than an awkwardness for it. M26-A's own section 1.3.2.5 is headed
*Volume Transferred*, and it ties the volume to the endpoint with a counting
rule: plate a volume such that, after the defined 99.9 per cent killing, at
least ten colonies remain to be counted (10). It permits 10 to 100 µL, and
gives a reason at each end — carryover above, Poisson sampling error below.
Section 3.1 goes further and requires that the smallest accurately detectable
count be established by serial dilution of a known inoculum. A guideline written
in 1999 therefore already required both of the numbers this paper asks for: a
floor established by measurement, and a plated volume chosen against the
endpoint.

Applied to its own endpoint the rule bites. Ten colonies after a 99.9 per cent
kill of 5 × 10⁵ per mL needs at least 20 µL streaked; a 10 µL streak yields five
and fails the rule. The requirement was there, it was quantitative, and the
deposits reanalysed here do not meet it — not because their authors disregarded
a standard, but because the endpoint moved out from under it. M26-A sets 99.9
per cent throughout and nowhere contemplates a four-log call; the deeper
endpoints came later, and the volume rule did not travel with them.

### What the tolerance phenotype tracks instead

Take the assay's contribution out and something is left, not nothing, and what
is left makes biological sense. Growth state predicts the tolerance class, and
it still predicts it after adjustment for starting density, which is the
expected direction: isoniazid needs KatG to activate it and needs active
cell-wall synthesis (27), rifampicin needs transcription (28), and a
population that is not dividing offers less of what these drugs act on. The axis
the classification is reading is physiological state, not drug susceptibility.

The isoniazid-resistance association behaves differently, and instructively. It
is the weaker of the two on two separate counts. Unadjusted, resistant isolates
carry 2.32 times the odds of a higher tolerance class. Adjusted for starting
density the odds ratio is 1.31 and the interval spans one. It also does not
clear its corrected threshold once the analysis is restricted to the baseline
isolates, which are one per patient by construction — the only correction for
repeated isolates this deposit permits, since it carries no patient identifier.
The growth association survives both.

Why the association weakens is visible in the same file: resistant isolates
enter the assay ten-fold lower and 26.2 per cent of them lack the room the
endpoint requires. We do not know why they seed lower. The natural explanation —
that resistance carries a fitness cost — is not supported here, since these
isolates do not grow measurably more slowly and most carry the near-neutral
*katG* S315X allele (29, 30). That gap is a finding in its own right and
belongs in the next study rather than in a speculative sentence in this one. Nor
is it explained away by anything else the file records: of its nine pretreatment
covariates only two can legitimately be adjusted for, and neither moves the
association by more than five per cent (Section 4). The two larger movements in
that table both come from columns that record the exposure rather than a
confounder: the mutation identity, which is missing for all but one susceptible
isolate, and the isoniazid MIC, which separates the two groups completely and
enlarges the seeding gap by 13 per cent instead of shrinking it.

### How large the effect is

Where the inoculum is set deliberately rather than by clinical accident, the
same arithmetic operates and can be measured rather than inferred. In more than
a third of cross-laboratory comparisons the flask in which the population fell
faster was the one that crossed below the assay floor later, and the
distance-over-rate criterion accounts for three in five of them. Resampling
whole laboratories rather than pairs leaves that rate poorly determined — 3.0 to
72.4 per cent — so what the deposit establishes is the mechanism and not the
rate.

The variance decomposition sets the size of the effect, and it will not carry
more than that. At the flask level the rate term takes the larger share in every
arm examined, but the flasks are three to a laboratory and the ordering does not
survive being asked at the laboratory level, so this paper does not assert it.
What the decomposition does establish is that the two terms are of comparable
size. A crossing time is not mostly a measurement of the inoculum, and it is not
mostly a measurement of the drug either. It is a mixture in which the inoculum is
a large minority — enough to reverse the ranking of two populations in more than
a third of comparisons, which is the number that matters to anyone choosing
between two compounds, and not enough to license the claim that the endpoint
measures the starting culture.

### Where we agree with the original authors, and where we differ

We agree with van Wijk and colleagues wherever the two analyses overlap. They
noticed the spread in starting densities themselves. They report that the burden
at the start varied between laboratories while the net effect of the drug varied
less (6); that conclusion is theirs, and it anticipates part of ours. Where
we part company is in what they did with readings that fell outside the
quantification limits: they left them out of the numbers. That is a defensible
way to report an assay. It also closes off the question this paper asks, because
those are exactly the readings a duration is built from.

Vijay and colleagues report that tolerance goes with resistance status and with
treatment history in the same isolates (5). We do not dispute a single
measurement. Their deposit is unusually complete, and this analysis was only
possible because they posted the classification, the readings behind it and the
assay geometry together. What we add is this. Their deepest endpoint asks for the
largest fall, so it is the one shortest of room to fall in, and how much room
there is differs systematically between the very groups being compared. The link
to resistance then survives neither putting starting density into the model nor
cutting the data down to one isolate per patient. The link to growth survives
both. So the finding is not that their classification is empty. It is that one of
its two associations is carried by the geometry of the assay and by isolates that
are not independent of each other.

### Limitations

Four things about these deposits bound what the analysis can establish. Each of
them points at the experiment that would settle the question.

The first limitation is one this paper has already acted on rather than merely
declared. Flasks from one laboratory share a starting culture; repeat isolates
come from a patient already counted.
Every conclusion drawn from the two primary deposits was recomputed at the level
where the observations really are independent, and the outcome is listed one line
at a time rather than summarised (Table S12): twenty survive unchanged, six
survive with much wider uncertainty, five do not survive and **have already been
removed from the text above**, and one is withdrawn because the "no difference"
it was tested against was already false before any data were seen. The five and
the one are not claims this paper makes; they are claims it tested and dropped,
and the ledger is printed so a reader can check that the dropping was done rather
than promised.

The evidence between laboratories rests on six laboratories, not on hundreds of
flasks. Every flask in a laboratory was seeded from the same starting culture, so
for this purpose those flasks are copies of one another. The effective sample
size for any comparison *between* laboratories is six, not the 67 to 85 flasks
the tables list. Six is too few for the standard correction — a cluster-robust
standard error — and the correction does not fail loudly when you fit it anyway.
On these data it returns a *smaller* p for every institute term than the
model-based p it was meant to correct. So where a comparison is between
laboratories we quote the exact laboratory-level test or a bootstrap that
resamples whole laboratories, and where the design cannot produce a meaningful p
at all, we give no p. Three laboratories recorded crossings at the 100 µL plating
and three did not; with the six split three and three, the smallest two-sided p
the arithmetic can return is 0.10, whatever the biology. Some quantities do let
flasks be pooled across laboratories — the variance shares, and the inversion
rate under a flask bootstrap. Those keep an exact permutation test, and they are
the strongest between-laboratory evidence the deposit holds.

The laboratories did not all count their starting density on the same day. Only
institutes C and D deposit a day-zero reading for the treated flasks. A, B, E and
F deposit day one, and by day one the ten-times-MIC arms have already lost
between 0.7 and 2.4 log10. For four of the six laboratories, then, the number we
are calling the exposure has some killing baked into it. We re-ran the whole
comparison on a day-one exposure for every laboratory. The ordering, the area
under the curve and the laboratory-level p all stayed the same, so the conclusion
is robust to it. The mismatch is real all the same, and we report it rather than
smooth it over.

In the six-laboratory exercise, starting density and laboratory are close to the
same variable. 87.0 per cent of the variance in flask-level starting density lies
between laboratories rather than within them. Taken over every flask that
deposits an early density, treated and untreated arms together, the laboratory
means span 3.62
log10, against a median within-laboratory standard deviation of 0.43. Adding
starting density to a model that already knows which laboratory a flask came from
is therefore not separating two covariates. It is closer to swapping a label for
a number carrying much the same information. Telling the two apart needs a design
that fixes the inoculum across laboratories.

The 15-day and 60-day panels of the clinical deposit contain the same isolates.
The comparison between panels is therefore not independent, and it bounds the
evidence for a difference rather than establishing it.

Starting density could sit on the causal path rather than beside it. Suppose
resistance slows growth, and slow growth causes genuine tolerance. Then the thin
inoculum is a consequence of the slow growth, and adjusting for it would remove
real signal rather than a confounder. The asymmetry favours the confounding
reading, since growth survives adjustment and resistance does not, but a design
that fixes the inoculum would settle it.

### What should change

**Report the starting density and the assay floor with every tolerance
measurement.** The two together say how far down the experiment could look, and
without that a log-reduction endpoint cannot be interpreted. Neither costs
anything to record: one is the count that went into the flask, the other is what
a single colony on the plate is worth. Four of the deposits examined in the
course of this project state no limit anywhere.

This is not an aspiration. One study already does it. A murine preventive-therapy
experiment writes its lower limit of detection into the deposited workbook once
on every sheet, separately for each agar type, and separately for individual mice
where the lower limit differed between them: 0.78 log10 CFU per lung on plain and
hygromycin agar, 0.54 on thiophenecarboxylic acid hydrazide agar, with the plated
volume stated beside it (31). That is better practice than anything else in
this corpus. The article reporting the experiment states none of it — a full-text
search returns no occurrence of "limit of detection" or of either value. So the
number is not missing from the science. It is missing from the paper, and a
reader who never opens the supplementary spreadsheet cannot know an endpoint was
bounded. What we are asking for is one sentence in a methods section, and
somebody has already done all the work that sits behind it.

The mirror image is a deposit whose modelling table carries a column named
`CFU_LOD`, and that column is empty in all 272 rows (32). Somebody designed
the field, declared it numeric, and never filled it in; nor does a detection
limit appear in any of the eight analysis scripts deposited beside it. Put the
two cases together and the diagnosis is not carelessness. The assay floor *L* is
measured. Sometimes it is written down to a standard higher than anyone asks for.
It then falls out of the record between the bench and the reader — off the end of
a spreadsheet, or into a column nobody completed.

**Choose the depth of the endpoint to fit the headroom actually available.** The
inoculum this needs can be worked out before the experiment rather than diagnosed
after it. Seeding above *L* · max(10^*q*, 1/*c*₁) makes both failure modes
impossible — the endpoint that was never reachable, and the last count that lands
on the floor. For this assay that is 230 000 per mL. A 99 per cent endpoint was
reachable for every isolate in this deposit, and a 99.99 per cent endpoint for 85
per cent of them. Where the deep endpoint is wanted, concentrate the starting
culture or lower the assay floor until the budget covers it. Where neither is
possible, the shallower endpoint is the honest one. This is a design decision
that is currently not being made.

**Model an ordered label as ordered.** A tolerance class is low, medium or high.
Scoring that 0, 1, 2 and fitting a line asserts that the step from low to medium
is the same size as the step from medium to high, and no one has established
that. Proportional-odds regression — a fit built for ranked categories — costs
nothing to run and reports in odds ratios. Where the proportionality it assumes
fails, as it does here at 60 days, it says so rather than averaging two different
effects into one null.

**Do not densify the inoculum merely to buy headroom.** Seeding higher makes a
deep endpoint legal, and it also changes the experiment: a denser culture is a
different physiological state, and this paper's own finding is that physiological
state is what the tolerance label tracks. Where the headroom will not carry the
endpoint, the shallower endpoint is the honest choice, and the growth state
belongs on the report either way.

**Treat an endpoint at the floor as a bound, not a value.** A recorded fraction of
*L*/*N₀* is an upper limit on survival, not an estimate of it. Analysed as a
measurement it manufactures differences between isolates whose final viable
burdens the assay could not tell apart. It also hides the converse point: the
range of true reductions a floor reading is compatible with depends on where that
culture started, so the same censored reading stands for a different demonstrated
kill at every starting density.

None of this requires new apparatus or a statistician, and to make that concrete
the four checks are released as a small command-line tool alongside the analysis
code. Give it a starting density and either an assay floor or a plated volume. It
returns the headroom, states which of the 90, 99, 99.9 and 99.99 per cent
endpoints that headroom can support, and reports the recorded fraction a
floor-level reading would produce, labelled as the bound it is. Where a culture
volume is known it also returns the viable burden a blank reading is consistent
with; where it is not, it declines to compute one rather than assuming a volume.
The tool exits with a failure code when a requested endpoint is unreachable, so
it can be run before an experiment rather than after it.

**Report physiological state as a required field.** It is what the classification
is reading, and it is currently the least documented variable in the assay.

**Fix the inoculum, or adjust for it, before comparing tolerance across groups.**
The comparison that motivated this work — resistant against susceptible isolates
— is confounded by a ten-fold difference in starting density, and nobody knows
why that difference is there. Until it is understood, group comparisons of
tolerance in clinical isolates should carry the starting density as a covariate.

---

### Conclusion

A plate that grows nothing under antibiotic has never been evidence that the
flask was sterile, and the field knows it. The remedy adopted was to stop asking
whether the culture went negative and to start asking how far it fell, expressed
as a fraction of where it began so that the starting culture could not matter. We
find that the fraction stops being a fraction once the population reaches the
floor. What the deposit records from that point is *L*/*N₀*, which moves with the
starting density and not with the surviving population — in this deposit, for
fifteen per cent of isolates at the depth the classification uses, and for the
eighteen isolates whose recorded label a single threshold on their inoculum
reproduces exactly, because for twelve of them no count below the floor would
have changed which class the rule could return.

The consequence is not that tolerance is an artefact. It is that a tolerance call
made without its headroom cannot be told apart from an inoculum measurement, and
that the phenotype which does survive the correction is physiological state
rather than drug susceptibility. Report the starting density and the assay floor.
Match the depth of the endpoint to the range actually available. Treat a reading
at the floor as a bound. Do those three things and a tolerance classification
would mean the same in one laboratory as in the next. Until then, some of what
the field calls tolerance cannot be separated from a record of how much culture
went into the tube.

---

## Materials and Methods

*The condensed account. The full account, with every estimator and every sensitivity analysis, is Supplementary Methods in the supplemental file.*

### Ethics

This study reanalysed publicly available, de-identified datasets deposited by
other groups. No new patient samples were collected, no new experimental data
were generated, and no individual is identifiable from any material presented
here. The author is an independent researcher with no institutional
affiliation, so no institutional review board holds jurisdiction over the work;
none was approached, and none is required for secondary analysis of de-identified
data already in the public domain under open licences.

### Use of generative artificial intelligence

Anthropic's Claude (Opus 5) was used under the author's direction to edit and
revise the manuscript text, and to write and revise the analysis and plotting code
in the accompanying repository, which draws every figure in this article from the
deposited data. No figure, image or schematic was generated by an artificial
intelligence tool; each is plotted by that code from values that regenerate from
the public deposits. No artificial intelligence tool is an author. The author
directed the analysis, verified every reported quantity against the source
deposits and the regenerating pipeline, and takes full responsibility for the
content of this article, including its accuracy and its originality.

### Data availability

Every dataset analysed here was already public under an open licence when this
work began, and none was generated for it. Each deposit is identified in Table 1
and cited in the reference list alongside the article that first described it:
the clinical isolate panel of Vijay and colleagues (5, 12), the
six-laboratory time-kill exercise of van Wijk and colleagues (6, 13), the
evolved-clone deposit of Windels and colleagues (33, 34), the apramycin grid
of Kaur and colleagues (14, 15), and the hollow-fibre Source Data of Dubey
and colleagues (16, 17), which was held out of every fitting step.

The analysis code, both audit scripts, the headroom tool described above and the
machine-readable receipts recording the software versions each stage ran under
are deposited in a public repository (35), with the documentation needed to install
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
(**B**) The two summaries against each other. The three lowest starting densities
are exactly the three laboratories that recorded crossings at the 100 µL plating;
the kill rate produces no such separation. The Kaplan–Meier curves for the
crossing times themselves, and the movement of the laboratory terms in the
descriptive Cox model, are Figure S1: both are descriptive, neither carries a
between-laboratory test, and the supplement is where they belong.

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


## Supplemental material

The supplemental file carries the full Materials and Methods, the analyses named above as supplementary text, and 22 supplemental tables. Table S13, Table S14, Table S15, Table S16, Table S17, Table S18, Table S19, Table S20, Table S21 and Table S22 support analyses reported there rather than in this article, and are listed so that every supplemental item is named in the manuscript.


## Tables

**Table 1.** The five published deposits reanalysed. Four carry the analysis and the fifth is held out to test it. None was generated for this study. The held-out deposit was opened after every boundary and threshold was fixed, which the commit history of the analysis repository timestamps; the other four were selected for the fields they carry, and that selection is not separately registered.

| Dataset | Organism | Drug and range | Design | Deposit | Licence |
| --- | --- | --- | --- | --- | --- |
| Six-laboratory exercise | *M. tuberculosis* H37Rv | moxifloxacin, isoniazid, 1x and 10x MIC | 90 flasks, 2 775 readings | figshare 19766083 | CC BY 4.0 |
| Clinical isolates | *M. tuberculosis*, 217 isolates | rifampicin | 6 duration endpoints per isolate | eLife 93243, suppl. file 2 | CC BY 4.0 |
| Evolved clones | *E. coli*, 126 clones | amikacin | MIC and persister fraction per clone | Zenodo 7550302 (34) | CC BY 4.0 |
| Concentration-by-time grid | *M. tuberculosis* | apramycin 1-128 ug/mL (amikacin arm not analysed) | 5 concentrations x 4 days x 3 replicates | figshare 26462791 | CC BY 4.0 |
| Held out for validation | *E. coli*, hollow fibre | amoxicillin-clavulanate | 20 cultures, measured day-zero density, 100 uL plated | Nat Commun 2026 Source Data | CC BY 4.0 |

**Table 2.** The reduction each tolerance endpoint requires against the reduction the assay can resolve, in the 15-day and the 60-day prior-culture panel alike. Headroom is the distance from an isolate's starting density down to the day-5 MPN floor of 23 per mL. An isolate short of headroom cannot reach that endpoint however completely the drug worked, and every such isolate is recorded at the assay ceiling.

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

8. Yamada WM, Schumitzky A, Kryshchenko A, Otalvaro J, Kim S, Louie A, Drusano GL, Neely MN. 2026. Analyzing pharmacodynamic count data that rapidly decrease to zero. CPT Pharmacometrics Syst Pharmacol 15(1). https://doi.org/10.1002/psp4.70140.

9. March VFA, Mchedlishvili K, Goig GA, Maghradze N, Avaliani T, Aspindzelashvili R, Avaliani Z, Kipiani M, Tukvadze N, Jugheli L, Bouaouina S, Doetsch A, Kalkan S, Reinhardt M, Gagneux S, Borrell S. 2025. Within-host evolution of drug tolerance in *Mycobacterium tuberculosis*. bioRxiv 2025.07.29.667394; preprint, not peer reviewed. https://doi.org/10.1101/2025.07.29.667394.

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

26. van Wijk RC, Solans BP, Chaba L, Sordello S, Upton AM, Nuermberger EL, Robertson GT, Walter ND, Savic RM. 2026. Predicting tuberculosis relapse based on 28-day CFU, RS ratio, and/or drug contribution for novel regimens in the relapsing mouse model. bioRxiv 2026.07.27.740024, version 1, posted 30 July 2026; preprint, not peer reviewed. https://doi.org/10.64898/2026.07.27.740024.

27. Vilchèze C, Jacobs WR Jr. 2007. The mechanism of isoniazid killing: clarity through the scope of genetics. Annu Rev Microbiol 61:35-50. https://doi.org/10.1146/annurev.micro.61.111606.122346.

28. Campbell EA, Korzheva N, Mustaev A, Murakami K, Nair S, Goldfarb A, Darst SA. 2001. Structural mechanism for rifampicin inhibition of bacterial RNA polymerase. Cell 104:901-912. https://doi.org/10.1016/S0092-8674(01)00286-0.

29. Pym AS, Saint-Joanis B, Cole ST. 2002. Effect of *katG* mutations on the virulence of *Mycobacterium tuberculosis* and the implication for transmission in humans. Infect Immun 70:4955-4960. https://doi.org/10.1128/IAI.70.9.4955-4960.2002.

30. van Soolingen D, de Haas PEW, van Doorn HR, Kuijper E, Rinder H, Borgdorff MW. 2000. Mutations at amino acid position 315 of the *katG* gene are associated with high-level resistance to isoniazid, other drug resistance, and successful transmission of *Mycobacterium tuberculosis* in the Netherlands. J Infect Dis 182:1788-1790. https://doi.org/10.1086/317598.

31. Lai RPJ, Ammerman NC, Tasneen R, Almeida DV, Converse PJ, Nuermberger EL. 2023. Using dynamic oral dosing of rifapentine and rifabutin to simulate exposure profiles of long-acting formulations in a mouse model of tuberculosis preventive therapy. Antimicrob Agents Chemother 67:e00481-23. https://doi.org/10.1128/aac.00481-23.

32. Tabor ST, Friesen AD, Reichlen MJ, Dide-Agossou C, McGrath M, Peterson R, Ganusov VV, Robertson GT, Voskuil MI, Walter ND. 2025. Mind the gap: understanding discordance between culture- and a non-culture-based measure of bacterial burden in murine tuberculosis treatment models. bioRxiv posted 18 December 2025; preprint, not peer reviewed. https://github.com/SamuelTaborCU/Mtb-16S-rRNA-vs-CFU.

33. Windels EM, Cool L, Persy E, Swinnen J, Matthay P, Van den Bergh B, Wenseleers T, Michiels J. 2024. Data supporting "Antibiotic dose and nutrient availability differentially drive the evolution of antibiotic resistance and persistence". Zenodo. https://doi.org/10.5281/zenodo.7550302.

34. Windels EM, Cool L, Persy E, Swinnen J, Matthay P, Van den Bergh B, Wenseleers T, Michiels J. 2024. Antibiotic dose and nutrient availability differentially drive the evolution of antibiotic resistance and persistence. ISME J 18:wrae070. https://doi.org/10.1093/ismejo/wrae070.

35. Piranfar V. 2026. Analysis code, audit scripts and headroom tool for "The detection floor bounds tolerance endpoints in Mycobacterium tuberculosis".
