---
title: "Score only the kill the assay can see: starting density and the floor bound every MDK"
short_title: "Headroom bounds every MDK"
article_type: "Resource"
status: "Draft. Text not final; reference list deliberately not yet compiled."
keywords:
  - antibiotic tolerance
  - minimum duration for killing
  - Mycobacterium tuberculosis
  - assay floor
  - censored data
  - time-kill kinetics
  - inoculum effect
---

# Score only the kill the assay can see: starting density and the floor bound every MDK

**Authors:** [to be inserted]

**Correspondence:** [to be inserted]

**Figures:** 4 | **Tables:** 15 | **Boxes:** 1 | **Supplementary tables:** 6

## Abstract

A negative culture after antibiotics have started has never meant sterility. The
field's answer was to ask not whether the culture went blank but how far the
population fell: the minimum duration for killing, the time to a 90, 99 or 99.99
per cent reduction, is the accepted tolerance marker. The endpoint is a fraction
of the starting count, so the inoculum should cancel. It does in the definition,
and fails once killing reaches the lowest count the assay can report.

Two boundaries follow from the definitions alone. For an operational assay floor
*L*, the smallest reportable positive count, a *q*-log endpoint is observable
only above *L*·10^*q*; and above *L*/*c*₁, where *c*₁ is the lowest class
threshold, only the lowest class is compatible with a censored reading.
Reaching the floor is the drug's doing; the label it then permits is not.

In 217 clinical *Mycobacterium tuberculosis* isolates classified for rifampicin
tolerance, no isolate lacks the range for a 90 or 99 per cent
endpoint; 33 lack it for the 99.99 per cent endpoint the classification uses,
and all 33 are recorded as failing. Of eighteen isolates whose reading was
censored, twelve admit one compatible class and six admit two. The label tracks
growth state, which survives adjustment for starting density, and isoniazid
resistance, which does not: most of it travels through a ten-fold lower
inoculum (mediated effect +0.166 classes, +0.067 to +0.279;
the direct effect spans zero).

Under one written protocol, six laboratories differed by 4.40 log10 in the
deepest kill they could demonstrate once plated volume is counted. In a
hollow-fibre experiment the framework never saw, five of twenty cultures cannot
show five logs. A tolerance call reported without *N₀* and *L* cannot be
interpreted; Box 1 is the calculation, and it needs no new apparatus.

**Keywords:** antibiotic tolerance; minimum duration for killing; *Mycobacterium
tuberculosis*; assay floor; headroom; censored data; ordinal regression;
time-kill kinetics; inoculum effect

## Introduction

Every clinical microbiologist is taught that a culture taken after antibiotics
have started is not evidence of sterility. It is why blood cultures are drawn
before the first dose. A drug suppresses growth, injures cells sublethally,
carries over into the medium, and drives the population beneath what the plate
can see; the plate then reports absence, and absence is not what happened. The
rule is old, it is correct, and nobody disputes it.

Tuberculosis makes the rule expensive. Regimens run for four to six months, the
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
(Brauner et al. 2016; Brauner et al. 2017). The choice of a *fraction* is the
whole point. A ratio to the starting population is scale-free: on a log-linear
decline at rate *b*, the time to a *q*-log reduction is *q/b*, and the starting
density cancels. By construction, MDK cannot be contaminated by how much culture
went into the tube. That is the property it was built to have.

We report that the property holds only in the estimand, not in the measurement,
and that the difference is consequential. A *q*-log reduction can be estimated
only if *q* logs are visible, and what is visible is bounded below by the assay's
floor. Writing *L* for that floor and *N₀* for the starting density, an isolate
has

    headroom  H = log10(N₀ / L)

and no experiment can demonstrate a reduction deeper than *H*, however completely
the drug worked. Where *H < q* the endpoint is unreachable before the drug is
added. Worse, when the final reading sits *at* the floor, the recorded fraction
is not a measurement at all but the ratio *L/N₀* — the most starting-density-
dependent quantity available. The metric designed to be inoculum-independent
becomes a pure inoculum readout precisely at the depth where tolerance is scored.

The two failures are different in kind, and this paper keeps them apart. Whether
an endpoint is reachable at all is settled by the assay geometry before the drug
is added, since *H* depends only on the starting culture and the floor. Whether a
reading that has reached the floor can be classified is settled by the geometry
too, but only once the drug has driven the population down to it: reaching the
floor takes a reduction of the isolate's entire headroom, and that is the drug's
doing.

This is testable rather than arguable, because one published deposit assigns the
tolerance phenotype itself. Vijay and colleagues (2024) scored 217 clinical
*Mycobacterium tuberculosis* isolates as having low, medium or high tolerance to
rifampicin, and deposited alongside each call the starting most probable number,
the growth rate, the isoniazid susceptibility and the killing readings the call
was built from. The classification, the inputs to it, and the assay geometry that
bounds it are all in the same file.

The aim of this study is to determine what a log-reduction tolerance
classification measures when the assay floor is within reach of the endpoint, and
to establish whether real isolates have been assigned tolerance phenotypes on
that basis. We test the hypothesis that a deep log-reduction endpoint is
inoculum-dependent through its observability even though it is
inoculum-independent in its definition, using the classification and the assay
geometry of 217 clinical isolates; we then ask what the resulting phenotype
tracks — drug susceptibility, or the physiological state of the culture. Two
further deposits establish that the same arithmetic governs killing experiments
where inoculum is controlled by protocol rather than by clinical accident: a
six-laboratory consortium exercise distributing one strain under one written
protocol, and a concentration-by-time grid in the same organism. If the
hypothesis holds, a tolerance call reported without its starting density and its
assay floor cannot be interpreted, and the phenotypes assigned in its
name are, in part, a record of how the assay was set up.

---

**Box 1. Four numbers that score an MDK.** *N₀* is the starting density. *L* is
the smallest positive count the method can report — one colony in a plated volume
*v* µL is *L* = 1 000/*v* per mL, and an MPN series uses the lowest table rung.
Headroom is *h* = log10(*N₀*/*L*). A *q*-log endpoint is legal only if *h* ≥ *q*,
which is the same as seeding at or above *L* · 10^*q*. If the last reading sits
at *L*, the recorded fraction is *L*/*N₀*: an upper bound, not a measurement. Do
not densify the inoculum solely to buy headroom; a shallower legal endpoint is
the honest alternative, and growth state still belongs on the report.

| Culture | *N₀* (per mL) | *L* (per mL) | Headroom | Legal endpoints | If the last reading is at *L* |
| --- | ---: | ---: | ---: | --- | --- |
| Thin clinical MPN | 23 000 | 23 | 3.00 | 90%, 99%, 99.9%; not 99.99% | Fraction 10⁻³. Low and medium both compatible: the rule cannot choose. |
| Adequate clinical MPN | 230 000 | 23 | 4.00 | all four, including 99.99% | Fraction 10⁻⁴. Only low is compatible. |
| 100 µL plate | 10⁵ | 10 | 4.00 | through 99.99%; not a 5-log call | Fraction 10⁻⁴. A 5-log MDK needs *N₀* ≥ 10⁶. |
| 10 µL drop, same *N₀* | 10⁵ | 100 | 3.00 | through 99.9%; not 99.99% | Fraction 10⁻³. The pipette, not the isolate, removed one log. |

The first two rows are the six medium against twelve low isolates that ended on
the same MPN floor in the clinical file. The last two are why a written protocol
does not standardise measurable depth: the plated volume sets *L*. To make both a
four-log endpoint and a low class identifiable against *L* = 23 per mL, seed
above *L* · max(10⁴, 1/*c*₁) = 230 000 per mL, or choose a shallower endpoint.

---

## Results

### 1. Observable kill is bounded by the assay floor

The most probable number readings take the discrete values of an MPN table, and
the day-5 column does not taper towards zero but stops. Eighteen isolates sit at
exactly 23 per mL in the 15-day panel and six in the 60-day panel, with no value
anywhere in the file below it (Fig. 1A). That is the behaviour of a floor rather
than of a tail, and it is treated as one throughout.

The deposit states no limit of quantification, so that value is inferred and the
inference is quantified rather than asserted. A discrete posterior over the
most-probable-number rungs at or below the observed minimum places 95 per cent
support on 9.2 to 23 per mL, a span of 0.40 log10 — narrow enough that the class
labels of Section 3 are computed rather than refused (Table 14). Where a deposit
gives no such evidence, those labels are refused instead of reported.

**Table 14.** What is actually known about the assay floor in each deposit, and the rule that follows from it. A floor derived from a recorded plated volume is a point mass: one colony in that volume, no inference required. A floor inferred from a pile-up on a most-probable-number rung carries a posterior over the rungs at or below the observed minimum, and the 95 per cent support is quoted. Where no floor is evidenced at all, or where the support spans more than one log10, the observability labels of Section 3 are refused rather than reported -- a label is only as good as the floor it is computed against.

| Deposit | Verdict | Floor used | 95% support | Span (log10) | Refuse observability labels |
| --- | --- | ---: | ---: | ---: | ---: |
| Vijay 2024, clinical isolates (MPN per mL) | INFERRED | 23 | [9.2, 23.0] | 0.398 | no |
| ERA4TB, 100 uL plated (CFU per mL) | DERIVED | 10 | point mass | 0.000 | no |
| ERA4TB, 10 uL plated (CFU per mL) | DERIVED | 100 | point mass | 0.000 | no |
| ERA4TB, 2.5 uL plated (CFU per mL) | DERIVED | 400 | point mass | 0.000 | no |
| Kaur 2024, apramycin grid (log10 CFU per mL) | NONE | 40 | - | - | yes |
| Windels 2024, evolved clones (surviving fraction) | NONE | - | - | - | yes |
| Dubey 2026, hollow fibre (CFU per mL) | DERIVED | 10 | point mass | 0.000 | no |

---

## Supplementary tables

Held here so the Results stay on one line of reasoning. Table S1 supports Section 10 and Table S2 supports Section 6.

**Table S1.** The same nominal concentration expressed in multiples of the minimum inhibitory concentration each population actually evolved to. At 25 ug/mL the same number denotes a sub-inhibitory exposure in one nutrient condition and a strongly inhibitory one in another.

| Nominal concentration (ug/mL) | Nutrient levels | Lowest exposure (x MIC) | Highest exposure (x MIC) | Spread | Straddles the MIC |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12.5 | 3 | 1.49 | 4.74 | 3.2x | no |
| 25 | 3 | 0.55 | 9.47 | 17.1x | yes |
| 50 | 2 | 5.08 | 10.95 | 2.2x | no |
| 100 | 1 | 9.72 | 9.72 | 1.0x | no |

**Table S2.** Fold below the nominal 0.5 McFarland reference, 1.5e8 CFU/mL. Descriptive only, and not a protocol-compliance metric. A time-kill inoculum is prepared by diluting from a suspension matched to that turbidity, so every entry is expected to sit far below it; the conversion of a turbidity to CFU/mL depends on species, cell aggregation and preparation and is least reliable for mycobacteria.

| Dataset | Median log10 N0 | Fold below nominal 0.5 McFarland |
| --- | ---: | ---: |
| ERA4TB, between laboratories at 100 uL | 4.63 | 3,525x |
| ERA4TB, every laboratory and plating volume | 4.29 | 7,751x |
| Vijay, 15-day culture | 5.79 | 246x |
| Vijay, 30-day culture | 7.36 | 7x |
| Vijay, 60-day culture | 7.36 | 7x |
| Kaur, planktonic | 7.03 | 14x |
| Kaur, intracellular | 5.94 | 170x |
| Dubey, hollow fibre | 6.08 | 123x |

**Table S3.** The ordinal reanalysis against the linear model it replaces, member for member. The linear model scores the ordering 0, 1, 2, which assumes the two class steps are equal; the ordinal model does not. Every direction agrees and the same two members survive correction under both, so the linear treatment did not manufacture the result -- but the coefficients it reports are in a unit that does not exist, which is why the ordinal fit is the one in the main table.

| Predictor | Prior culture | Depth | Linear beta | p (linear) | Survives BH | Odds ratio | p (ordinal) | Survives BH  | Same direction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| growth | 15 d | D5 | +0.0266 | 0.0025 | yes | 1.096 | 0.0030 | yes | yes |
| resistance | 15 d | D5 | +0.2589 | 0.0035 | yes | 2.317 | 0.0042 | yes | yes |
| growth | 60 d | D2 | -0.0195 | 0.0590 | no | 0.933 | 0.0470 | no | yes |
| growth | 15 d | D2 | +0.0116 | 0.0812 | no | 1.068 | 0.0618 | no | yes |
| resistance | 15 d | D2 | +0.0515 | 0.4446 | no | 1.295 | 0.4529 | no | yes |
| growth | 60 d | D5 | -0.0041 | 0.6999 | no | 0.976 | 0.4605 | no | yes |
| resistance | 60 d | D2 | -0.0551 | 0.5486 | no | 0.836 | 0.5400 | no | yes |
| resistance | 60 d | D5 | +0.0389 | 0.6797 | no | 1.111 | 0.7150 | no | yes |

**Table S4.** Sensitivity of the load-bearing counts to the choice of floor, per deposit, showing only the counts a conclusion rests on. The clinical sweep steps through every three-tube most-probable-number rung at or below 23 per mL: the number of isolates short of four logs of headroom moves only between 28 and 33 across the whole range, which is why the inferred floor is safe to use. The six-laboratory rows compare judging each reading against the floor its own plated volume implies with pooling all four volumes to one floor, and price what pooling would cost. The Kaur deposit records no plated volume, so its row shows what assuming one would do: the four-log endpoint stays reachable throughout while h itself moves by 1.6 log10.

| Deposit | Floor assumed | % counts a pooled floor discards | % flags contradicted | 4-log reachable | at the floor | h | measured | median h | one class | several classes | short of 4 logs | short, baseline only | written as exact zero |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dubey 2026, hollow fibre | 10 uL plated | - | - | - | - | - | - | 4.08 | - | - | 5 | - | - |
| Dubey 2026, hollow fibre | 100 uL plated, as the deposit's staging record gives | - | - | - | - | - | - | 5.08 | - | - | 0 | - | - |
| Dubey 2026, hollow fibre | 50 uL plated | - | - | - | - | - | - | 4.78 | - | - | 0 | - | - |
| Dubey 2026, hollow fibre | the below-limit placeholder taken literally | - | - | - | - | - | - | 6.08 | - | - | 0 | - | - |
| ERA4TB, six laboratories | per-volume (as analysed) | 0 | 16.67 | - | - | - | - | - | - | - | - | - | - |
| ERA4TB, six laboratories | pooled at the geometric mean of the per-volume floors | 1.04 | 38.96 | - | - | - | - | - | - | - | - | - | - |
| ERA4TB, six laboratories | pooled at the least sensitive volume, 2.5 uL | 5.94 | 15.26 | - | - | - | - | - | - | - | - | - | - |
| ERA4TB, six laboratories | pooled at the modal volume, 10 uL | 1.13 | 28.71 | - | - | - | - | - | - | - | - | - | - |
| ERA4TB, six laboratories | pooled at the most sensitive volume, 100 uL | 0 | 43.17 | - | - | - | - | - | - | - | - | - | - |
| Kaur 2024, apramycin grid | 10 uL plated, if it had been stated | - | - | True | - | 5.03 | - | - | - | - | - | - | - |
| Kaur 2024, apramycin grid | 100 uL plated, if it had been stated | - | - | True | - | 6.03 | - | - | - | - | - | - | - |
| Kaur 2024, apramycin grid | 2.5 uL plated, if it had been stated | - | - | True | - | 4.43 | - | - | - | - | - | - | - |
| Kaur 2024, apramycin grid | the observed minimum, which occurs once | - | - | True | - | 5.43 | - | - | - | - | - | - | - |
| Vijay 2024, clinical isolates | floor = 11 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 14 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 15 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 20 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 21 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 23 MPN/mL | - | - | - | 18 | - | 185 | - | 12 | 6 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 3 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 28 | 17 | - |
| Vijay 2024, clinical isolates | floor = 3.6 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 28 | 17 | - |
| Vijay 2024, clinical isolates | floor = 7.2 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 7.4 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Vijay 2024, clinical isolates | floor = 9.2 MPN/mL | - | - | - | 0 | - | 203 | - | 0 | 0 | 33 | 21 | - |
| Windels 2024, evolved clones | no floor is recoverable | - | - | - | - | - | - | - | - | - | - | - | 6 |

**Table S5.** Decomposition of the isoniazid-resistance association with the tolerance class into a path through log10 starting density and a direct path, by the product of coefficients with bootstrap percentile intervals. The mediated path excludes zero in every specification and the direct path covers zero in every one. This replaces the percentage attenuation the earlier analysis quoted, which is a descriptive ratio rather than an estimand. Sequential ignorability is assumed and is not testable here; the sensitivity analysis in the Methods reports the residual correlation that would nullify the estimate.

| Outcome and stratum | n | Total effect c (95% CI) | Direct effect c' (95% CI) | Mediated effect (95% CI) | Proportion mediated |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linear 0/1/2, all IS/IR | 203 | +0.256 (+0.087, +0.425) | +0.091 (-0.116, +0.287) | +0.166 (+0.067, +0.279) | 65% |
| Linear 0/1/2, baseline isolates | 168 | +0.226 (+0.038, +0.409) | +0.067 (-0.157, +0.294) | +0.159 (+0.053, +0.295) | 70% |
| High versus rest | 203 | +0.121 | +0.013 | +0.108 (+0.037, +0.189) | 89% |
| Not-low versus low | 203 | +0.135 | +0.077 | +0.058 (+0.003, +0.121) | 43% |

**Table S6.** Isoniazid-resistant isolates enter this assay ten-fold lower than susceptible ones, and we do not know why. This is what the deposit can rule out: the association between resistance and starting density, adjusted in turn for every usable pretreatment covariate the file carries. None removes it. The file records no referring site and no processing batch, so those cannot be tested at all, and the gap is reported as real, large and unexplained rather than attributed to a mechanism the data cannot support.

| Adjusted for | Kind | n | Resistance coefficient | p | Attenuation |
| --- | --- | ---: | ---: | ---: | ---: |
| INH_mutation | categorical(k=4) | 203 | -0.662 | 0.0462 | 22% |
| MIC_INH | numeric | 186 | -0.963 | 3.07e-07 | -13% |
| Time_to_0.4 | numeric | 202 | -0.807 | 1.23e-14 | 5% |
| Time_point | categorical(k=8) | 203 | -0.818 | 2.89e-10 | 4% |
| MIC_RIF | numeric | 186 | -0.853 | 2.41e-13 | -0% |
| RIF_MGIT_DST | categorical(k=2) | 203 | -0.851 | 2.58e-14 | -0% |
| INH_MGIT_DST | categorical(k=2) | 203 | -0.851 | 2.58e-14 | -0% |
| (none) | unadjusted | 203 | -0.850 | 2.01e-14 | 0% |


The consequence is that each isolate carries a fixed budget of observable
killing. At 15 days of prior culture the starting densities span 3.36 to 7.79
log10, so headroom spans 2.00 to 6.42 log10 (Fig. 1B, Table 2). Against that budget the
three deposited endpoints behave very differently. No isolate lacks the headroom
for a 90 or a 99 per cent reduction: 0 of 217 in both cases. **Thirty-three of
217 isolates — 15.2 per cent — lack the headroom for the 99.99 per cent
endpoint**, which is to say that a four-log reduction was unobservable for them
before rifampicin was added.

**Table 2.** The reduction each tolerance endpoint requires against the reduction the assay can resolve. Headroom is the distance from an isolate's starting density to the MPN floor of 23 per mL. An isolate short of headroom cannot reach that endpoint however completely the drug worked, and every such isolate is recorded at the assay ceiling.

| Prior culture | Endpoint | Isolates | Short of headroom | Fraction short | At ceiling: short vs ample |
| --- | ---: | ---: | ---: | ---: | ---: |
| 15 days | 90% (1 log) | 217 | 0 | 0.0% | - |
| 15 days | 99% (2 log) | 217 | 0 | 0.0% | - |
| 15 days | 99.99% (4 log) | 217 | 33 | 15.2% | 100% vs 88% |
| 60 days | 90% (1 log) | 210 | 0 | 0.0% | - |
| 60 days | 99% (2 log) | 210 | 0 | 0.0% | - |
| 60 days | 99.99% (4 log) | 210 | 7 | 3.3% | 100% vs 95% |


All 33 are recorded as not having reached it. That is a census of the affected
isolates rather than an estimate, and it is the load-bearing observation. Among
the 184 isolates that did have four logs of headroom, 162 are also at the
ceiling, 88.0 per cent; the contrast between 100 and 88 per cent is small enough
that its nominal Fisher p of 0.030 does not survive restriction to the baseline
isolates (p = 0.14), and nothing here rests on it. The deepest endpoint is therefore the only one at risk, and it is the
one the tolerance classification is built on.

### 2. Identical floor observations received different tolerance phenotypes

The deposited tolerance level is a threshold on the recorded surviving fraction,
with no overlap between classes: at day 5 and 15 days of prior culture, low
tolerance covers fractions below 10⁻³, medium covers 10⁻³ to 10⁻², and high
exceeds 10⁻². Applying those cuts reproduces every usable class in the file,
203 of 203 (Table 3a), so what follows is an argument about the fraction the
assay recorded and not about an independent clinical judgement.

Eighteen isolates ended at the floor. They share one reported floor-level
observation, but their true final counts are unknown below the assay limit, so
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

**Table 3.** Isolates whose day-5 reading was censored at the MPN floor. They share one reported floor-level observation, but their true final counts are unknown below the limit, so the assay cannot distinguish their final viable burdens; because their starting densities differ, the same reading also implies a different range of compatible fractional reductions in each. The recorded fraction is L/N0, so the spread in apparent survival equals the spread in starting density exactly, and the labels differ accordingly. The last three columns sort every call in the panel, not only the censored ones: a censored reading bounds the class from above, and sweeping the true count across the admissible range leaves twelve calls with a single compatible class and six with more than one. Reaching the floor at all is a property of the killing; which class is then compatible is a property of the starting density and the floor.

| Prior culture | At the floor | Starting density spread | Recorded survival spread | Labels assigned at the floor | Measured | Single compatible class | Multiple compatible classes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 15 days | 18 | 265x | 265x | Low: 12, Medium: 6 | 185 | 12 | 6 |
| 60 days | 6 | 100x | 100x | Low: 6 | 191 | 6 | 0 |

**Table 3a.** The deposited tolerance class at day 5 after 15 days of prior culture is a threshold on the recorded surviving fraction, with no overlap between classes: low below 10⁻³, medium from 10⁻³ to 10⁻² inclusive, high above 10⁻². Applying those cuts reproduces every usable class in the file. This matters because the argument that follows is about the fraction the assay recorded, not about an independent clinical judgement.

| Recorded class | n | Min fraction | Max fraction | Predicted from cuts | Disagreements |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low | 33 | 3.8 × 10⁻⁶ | 4.7 × 10⁻⁴ | Low | 0 |
| Medium | 124 | 1.0 × 10⁻³ | 1.0 × 10⁻² | Medium | 0 |
| High | 46 | 2.7 × 10⁻² | 1.0 × 10¹ | High | 0 |
| All usable | 203 | - | - | - | 0 |


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
study would compare. The 99.99 per cent endpoint is unreachable for 26.2 per cent
of isoniazid-resistant isolates against 7.6 per cent of susceptible ones (Fisher
exact p = 0.00056), and their median headroom differs by a full log, 4 against 5.
A comparison of tolerance between those groups is therefore in part a comparison
of how well each group could be measured, which is the disposition the previous
section quantifies.

### 3. The affected isolates are named before the drug is added

Sections 1 and 2 counted isolates. The two boundaries of Section 2 of the Methods
do more than that: given only the floor, the class thresholds and each isolate's
starting density, they say in advance which isolates are affected, before any
day-5 reading is used.

For this assay *N*_reach = 23 × 10⁴ = 230 000 per mL and *N*_id = 23/10⁻³ =
23 000 per mL. Applied to the 15-day panel, the first predicts 33 isolates unable
to reach the 99.99 per cent endpoint, and the second predicts that of the
eighteen isolates whose reading rests on the floor, twelve have only the lowest
class compatible with that reading and six have more than one. Those are the
three counts Sections 1 and 2 report.

Neither boundary predicts which isolates reach the floor; that depends on what
rifampicin does. Both predict what a reading at the floor can be made to mean once
it happens, and there the prediction is exact isolate by isolate rather than
merely in aggregate: the set the algebra says has a single compatible class and
the set the deposit records in the lowest class are the same set. The boundary case decides it. Six isolates sit at exactly 23 000 per
mL, which is *N*_id itself, so for them *L*/*N₀* = *c*₁ exactly, the interval
[0, *L*/*N₀*] touches the threshold and spans two classes, and the strict
inequality fails. Those six are precisely the ones with more than one compatible
class. A relationship
fitted to the data would not fail in the right places as well as succeeding in
the right places.

The empirical findings are therefore consequences of the definitions rather than
properties of this deposit, and the claim is a prediction that any dataset
reporting a starting density, a floor and a threshold classification can be
checked against.

### 4. The classification tracks growth; the resistance association is carried by inoculum

Eight association tests are available between the deposited label and its
candidate determinants — two predictors, at two culture ages and two endpoint
depths — and they are corrected as one family. Two survive (Table 4).

**Table 4.** The family of 8 tests between the deposited tolerance label and its candidate determinants, fitted as proportional-odds ordinal logistic regression and corrected together at a false discovery rate of 5%. 2 survive. An odds ratio above one means higher odds of a higher tolerance class. The proportional-odds column is a Brant test per predictor; the assumption holds throughout this family. The final column repeats each test on the 174 baseline isolates, one per patient by construction, which is where the resistance association stops clearing its corrected threshold. Standard errors are model-based; the deposit carries no patient identifier, so none can be clustered on the true grouping.

| Predictor | Prior culture | Depth | For starting density | n | Odds ratio (95% CI) | p | Survives BH | Prop. odds p | Baseline isolates only |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| growth | 15 d | D5 | adjusted | 202 | 1.096 (1.03-1.16) | 0.0030 | yes | 0.152 | 1.12 (p=0.002, survives) |
| resistance | 15 d | D5 | unadjusted | 202 | 2.317 (1.30-4.12) | 0.0042 | yes | 0.417 | 2.11 (p=0.031, no) |
| growth | 60 d | D2 | adjusted | 196 | 0.933 (0.87-1.00) | 0.0470 | no | 0.688 | 0.92 (p=0.032, no) |
| growth | 15 d | D2 | adjusted | 202 | 1.068 (1.00-1.14) | 0.0618 | no | 0.243 | 1.07 (p=0.108, no) |
| resistance | 15 d | D2 | unadjusted | 202 | 1.295 (0.66-2.54) | 0.4529 | no | 0.479 | 1.07 (p=0.876, no) |
| growth | 60 d | D5 | adjusted | 196 | 0.976 (0.91-1.04) | 0.4605 | no | 0.875 | 0.99 (p=0.703, no) |
| resistance | 60 d | D2 | unadjusted | 196 | 0.836 (0.47-1.48) | 0.5400 | no | 0.075 | 1.11 (p=0.774, no) |
| resistance | 60 d | D5 | unadjusted | 196 | 1.111 (0.63-1.95) | 0.7150 | no | 0.067 | 1.61 (p=0.186, no) |


The label is an ordered categorical outcome, low below medium below high, and it
is modelled as one: a linear coefficient on a 0, 1, 2 score would assert that the
step from low to medium equals the step from medium to high, and nothing
establishes that. Associations are therefore reported as odds ratios from
proportional-odds ordinal logistic regression, with the proportional-odds
assumption tested rather than assumed (Methods; Table 4).

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
lower (Mann–Whitney p = 9.1 × 10⁻¹⁴), and 26 per cent of them lack the headroom
for the deepest endpoint against 8 per cent of susceptible isolates. They are
one log poorer in observable killing before the experiment begins.

A percentage attenuation is a descriptive ratio, not an estimand, so the path is
also estimated directly. Decomposing the total effect of resistance on the
tolerance class into a path through log10 starting density and a direct path
gives a mediated effect of +0.166 classes (bootstrap 95 per cent CI +0.067 to
+0.279) against a direct effect of +0.091 (−0.116 to +0.287), so about 65 per
cent of the association travels through the inoculum and the direct path covers
zero. Restricting to baseline isolates leaves the mediated path intact (+0.159,
+0.053 to +0.295), and binary collapses of the outcome agree (Table S5). This
rests on sequential ignorability, which no observational file can establish: a
residual correlation between the mediator and outcome errors of about −0.24
would nullify the point estimate. Only a design that fixes the inoculum settles
it.

These 217 isolates are not 217 independent observations. Forty-three are
follow-up isolates drawn during treatment from patients who also contributed a
baseline isolate, so up to 86 rows sit in clusters of two, but the deposit
carries no patient identifier: Archive and Sample-ID are unique per row and no
column among the 48 has the multiplicity a patient key would need. The pairing is
not recoverable, so no standard error can be clustered on the true grouping, and
we do not pretend otherwise. What is available is the exact substitute, a
baseline-only stratum in which every isolate is from a different patient by
construction (Time_point = 0M, n = 167 at 15 days).

Restricted to it, the two surviving associations part company. Growth holds and
still survives correction (OR 1.116, 1.040 to 1.198, p = 0.0024). Resistance does
not: OR 2.11 (1.07 to 4.16, p = 0.031), which is second in the family of eight
and so is tested against a Benjamini–Hochberg critical value of 0.0125. The
resistance association therefore depends on isolates that are not independent of
one another, and it is already the association that starting density explains
away. We report it as the weaker of the two on both counts.

Why they seed lower is not established here, and the obvious explanation fails:
resistant isolates do not grow significantly more slowly in this deposit (median
time to OD 0.4 of 19 against 17, p = 0.24), and 85 of them carry *katG* S315X,
the mutation that predominates clinically precisely because it is close to
fitness-neutral. The association between resistance and a low starting inoculum
is real, large and unexplained, and we record it as such.

Both surviving associations sit in the 15-day panel, which is where the
mechanism places them. By 60 days the cultures are 38-fold denser, the spread of
starting densities has more than halved, from an interquartile range of 1.00 to
0.42 log10, and the fraction of isolates short of headroom falls from 15.2 to 3.3
per cent. The confound is a property of a thin assay and it thins out when the
assay is not. Those two panels are columns on the same spreadsheet rows — 210
isolates appear in both — so every comparison between them is within-isolate and
is made that way. Pairing sharpens rather than softens the result: 26 isolates
lose their headroom shortfall between panels and none acquires one (exact McNemar
p = 3.0 × 10⁻⁸ against an unpaired p of 2 × 10⁻⁵), eleven leave the floor and none
joins it (p = 9.8 × 10⁻⁴), and every isolate whose headroom changes gains
(Wilcoxon signed-rank p = 1.3 × 10⁻³³). The interquartile range of starting
density falls by 0.58 log10.

It does not vanish, and the ordinal treatment is what shows where it goes.
Proportional odds holds throughout the 15-day panel but fails at 60 days for
starting density at the deepest endpoint (Brant p = 0.0031; likelihood-ratio test
against a released fit p = 0.0062). Releasing that coefficient puts the whole
effect at the upper boundary: the odds ratio for clearing medium is 0.493 (0.336
to 0.724, p = 0.0003) against 0.951 for clearing low (0.647 to 1.396, p = 0.80).
A multinomial fit that assumes no ordering at all agrees (high against low,
relative risk ratio 0.59, p = 0.028; medium against low, 1.22, p = 0.39). In the
denser panel the starting density no longer decides who is called low; it still
decides who can be called high. A single averaged slope, ordinal or linear, would
have reported that as a null.

### 5. One written protocol does not produce one measurable depth

If the effect is a property of assay geometry rather than of clinical sampling,
it should appear where one protocol, one strain and one stock are distributed
deliberately. It does.

At ten times the minimum inhibitory concentration of moxifloxacin all six
laboratories return a positive kill rate spanning 5.2-fold, from 0.090 to 0.464
log10 CFU/mL per day, and across all 30 laboratory-by-arm cells the Tobit and
imputation estimates never differ by more than 0.003 log10 per day (Fig. 2A,
Table 5). The duration endpoint behaves differently on the same flasks. The
event it records is not clearance and not sterilisation but a **first observed
crossing below the assay boundary**, and the distinction is not pedantic: most
series that cross later read above the boundary again, including all five
untreated series that cross. Of 72 treated flasks, 29 ever fell below their own
floor; institutes A, B and C recorded crossings in every arm and institutes D, E
and F recorded none in any arm (Fig. 2B). For half the laboratories the time to
first crossing is right-censored throughout.

**Table 5.** Moxifloxacin at ten times MIC. Every laboratory yields a rate; three record no crossing below the assay boundary in any arm. The final column counts first observed crossings, which are not clearances: across the deposit 60% of the series that cross read above the boundary again at a later visit. The two censoring estimators agree to 0.003 log10 per day.

| Lab | Starting density (log10 CFU/mL) | Kill rate (log10/day) | 95% profile interval | By imputation | Readings censored | Flasks ever crossing the boundary (all arms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 2.95 | 0.119 | 0.092 to 0.155 | 0.119 | 51% | 9 / 12 |
| B | 3.16 | 0.139 | 0.097 to 0.191 | 0.138 | 58% | 10 / 12 |
| C | 4.02 | 0.464 | 0.430 to 0.499 | 0.464 | 44% | 10 / 12 |
| D | 4.69 | 0.104 | 0.081 to 0.128 | 0.105 | 3% | 0 / 12 |
| E | 4.95 | 0.090 | 0.077 to 0.104 | 0.090 | 1% | 0 / 12 |
| F | 6.53 | 0.223 | 0.206 to 0.240 | 0.223 | 0% | 0 / 12 |


The two orderings do not correspond. Ranked by starting density, the three lowest
laboratories are exactly the three that recorded crossings and the three highest
exactly the three that did not, without exception; ranked by kill rate there is
no such correspondence (Fig. 2C). Institute F, with the highest starting density
at 6.53 log10, kills faster than four of the other five at 0.223 log10 per day
and records no crossing. Institute E returns the slowest rate of all at 0.090 and
also records none.

Starting density separates flasks that ever crossed from those that never did
with an area under the curve of 0.974. That figure is a description and it is
quoted without a p-value, deliberately. The comparison looks like 67 flasks but
it is three laboratories against three: every flask in a laboratory shares its
starting culture, and the three lowest starting densities are exactly the three
laboratories that recorded crossings. Tested at the level at which the
observations are actually independent, the exact two-sided p is 0.10 — and 0.10
is the smallest value a three-against-three split of six clusters can return, so
no arrangement of this deposit could have reached significance. Nor is there a
within-laboratory fallback: holding laboratory and treatment arm both fixed,
only 2 of 24 cells contain both outcomes, and the smallest attainable p is 0.17.

The Cox fits are reported for the same reason and with the same restraint. On
laboratory alone, institutes D, E and F carry hazard ratios of 0.20; adding
starting density moves those to 0.138, 0.172 and 0.576, and concordance rises
from 0.896 to 0.930 (Fig. 2D). Institute C does not dissolve, and it is also the
fastest killer, which is the behaviour expected of a laboratory that genuinely
kills faster. No p-value is attached to any of these terms. The tested covariate
is constant within cluster, and with six laboratories and six parameters the
cluster-robust covariance is singular by construction; fitting it anyway does not
fail loudly but returns a smaller p than the one it was meant to correct. A
coefficient that moves on adjustment is a statement about how far starting
density and laboratory identity overlap in this design, not evidence that one
explains the other.

Where an interval is quoted from that fit it is a cluster bootstrap and not the
model's own. For the starting-density coefficient the laboratory-clustered
interval is −1.11 to −0.51, half again as wide as the model's −0.91 to −0.48 and
two and a half times the flask-clustered −0.81 to −0.56; quoting the model's
interval is not conservative, it is wrong in an unpredictable direction. For the
laboratory contrasts the laboratory bootstrap is the wrong instrument, since it
keeps each laboratory's flasks together and the contrast barely moves, so the
flask-clustered interval is quoted there instead. The crossings behind each
laboratory's coefficient are also worth stating plainly: 43 of 48 series in
institute C against 1 of 48 in institute E.

Killing here is not sustained, and this is stronger than a caveat about
individual flasks. Of the 64 treated series carrying at least three quantified
readings at the most sensitive plating volume, the final step is not a decline in
48, and 44 end more than one log10 above their own lowest reading, with a median
rebound of 2.17 log10 and a largest of 5.54. Seventeen of the 32 flasks that fell
below the boundary at the most sensitive plating were detectable again at a later
visit, 14 of them in treated arms. Across all four platings, 84 of the 140 series
that cross return above the boundary, 60 per cent, and the return is quick: a
median of four days, with 45 per cent back within three. Those 360 series come
from 90 flasks, four platings each, so they are not 360 independent observations;
counted by flask, 53 contain a crossing series and 42 of those contain a
returning one. A crossing below the
assay boundary in this deposit is therefore usually a transient rather than an
endpoint, which is a further reason it summarises less than the trajectory that
produced it. Killing itself is real and dose-dependent:
at one times the inhibitory concentration five of six laboratories record net
growth under moxifloxacin, between −0.047 and −0.214 log10 per day, and at ten
times all six record net decline.

Two consequences follow, and they matter for anyone who reads a duration off
such an experiment. The first is that the state below the boundary is not
absorbing. Of 2 232 visit-to-visit transitions, 144 go from above to below and 95
go from below to above, so a series sitting below the boundary leaves it at the
next visit with probability 0.22. The gradient runs with drug pressure — that
probability is 1.00 in untreated series, 0.37 to 0.92 at one times MIC and 0.07
to 0.18 at ten times — which says the event is at least partly a property of the
plate rather than of the drug. Of the 360 series, only 56, or 15.6 per cent, show
the shape a survival model assumes: one crossing that holds (Table 13). Two hundred and
twenty never cross at all, 65 cross and return, and 19 oscillate more than once.

**Table 13.** What follows a first observed crossing below the assay boundary. The state below the boundary is not absorbing: a series sitting below it reads above again at the next visit with probability 0.22 overall, and that probability rises as drug pressure falls, which is what a plating artefact does. Only 56 of 360 series, 15.6 per cent, show the shape a survival model assumes -- one crossing that holds. The 360 series are four platings of each of 90 flasks and are not independent; the flask-level counts are 53 flasks with a crossing series and 42 with a returning one.

| Series | n | Visit pairs | P(above to below) | P(below to above) | Never below | One crossing, holds | One crossing, returns | Crosses repeatedly | Shape the model assumes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all series | 360 | 2232 | 0.080 | 0.222 | 220 | 56 | 65 | 19 | 16% |
| INH 10X MIC | 72 | 441 | 0.137 | 0.065 | 34 | 27 | 6 | 5 | 38% |
| INH 1X MIC | 72 | 440 | 0.150 | 0.373 | 30 | 2 | 33 | 7 | 3% |
| MXF 10X MIC | 72 | 433 | 0.141 | 0.175 | 30 | 26 | 9 | 7 | 36% |
| MXF 1X MIC | 72 | 441 | 0.023 | 0.923 | 59 | 1 | 12 | 0 | 1% |
| untreated | 72 | 477 | 0.011 | 1.000 | 67 | 0 | 5 | 0 | 0% |


The second is that the crossing time is never observed. It lies between the last
visit above the boundary and the first visit below it, and the naive treatment
pins it to the later end, which biases every duration late by construction rather
than merely imprecisely. Fitted as interval-censored data at the most sensitive
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

### 6. A turbidity standard fixes what goes in, not what the plate can resolve

A time-kill inoculum is not chosen freely: a suspension is matched to 0.5
McFarland and diluted, and CLSI M26 puts the target near 5 × 10⁵ CFU/mL. If the
protocol fixes the starting density, the preceding sections describe a variable
that does not vary.

Two properties of the standard make this answerable with counts. A McFarland
figure is a turbidity, matched optically, and counts live cells, dead cells,
debris and a clump as one particle; converting it to CFU/mL assumes a cell size,
shape and dispersal that *M. tuberculosis* does not oblige, and tuberculosis
protocols work from a range of dilutions and target inocula. And the standard
fixes what goes in, while what is needed here is what the plate counts, separated
from it by a dilution, a transfer and whatever aggregation occurs on the way.

In the six-laboratory exercise, the untreated arm at day zero gives realised
densities of 3.29, 3.63, 4.16, 4.70 and 5.97 log10 CFU/mL for institutes A, B, C,
D and F; institute E deposits no untreated day-zero reading at any volume, its
series beginning at day one. Three of the five sit between eleven and a
hundred-fold below the CLSI target.

Reported as headroom at a fixed plating volume the spread is Δ*h* = 2.33 log10, a
216-fold difference in measurable capacity under one written protocol (Table 9),
and that figure needs its roster stated because it is small. It is a
maximum-minus-minimum over the **four** laboratories that deposit a countable
untreated day-zero reading at 100 µL — B at *h* = 2.67, C at 3.61, D at 3.65 and
F at 5.00. Institute A's three readings there are flagged above the quantification
limit rather than absent, and its other platings put it near *h* = 2.4, so
including it would widen the spread rather than narrow it. A range over four
draws is a fragile statistic: its cluster-bootstrap 95 per cent interval runs from
0.05 to 2.33 log10, the upper limit being the observed range by construction.

**Table 9.** The deepest reduction each assay could resolve, as h = log10(N0/L), with the assay floor taken per sample where it varies. Rows compare only within a level of variation: the clinical rows describe between-isolate starting burden, which is biological, and are not a measure of laboratory imprecision. Kaur is NA because its three day-zero readings are technical replicates of one preparation and cannot estimate between-preparation reproducibility, and because that deposit states no quantification limit.

| Dataset | Level of variation | n | Median log10 N0 | Assay floor L | delta h (log10) | Fold |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| ERA4TB, between laboratories at 100 uL | between laboratories, one written protocol | 12 | 4.63 | 10 CFU/mL, derived from 100 uL plated | 2.33 | 216x |
| ERA4TB, every laboratory and plating volume | laboratories and plated volumes together | 56 | 4.29 | 10, 100 or 400 CFU/mL by volume | 4.40 | 25,123x |
| Vijay, 15-day culture | between clinical isolates | 217 | 5.79 | 23 CFU/mL, inferred | 4.42 | 26,522x |
| Vijay, 30-day culture | between clinical isolates | 217 | 7.36 | 23 CFU/mL, inferred | 5.43 | 269,565x |
| Vijay, 60-day culture | between clinical isolates | 210 | 7.36 | 23 CFU/mL, inferred | 5.43 | 269,565x |
| Kaur, planktonic | technical replicates of one preparation | 3 | 7.03 | not stated in the deposit | NA | NA |
| Kaur, intracellular | technical replicates of one preparation | 3 | 5.94 | not stated in the deposit | NA | NA |
| Dubey, hollow fibre | between cultures, one laboratory | 20 | 6.08 | 10 CFU/mL, derived from 100 uL plated | 0.60 | 4x |


The stronger version of the same argument does not depend on that roster at all.
Including the choice of plated volume widens the spread to Δ*h* = 4.40 log10, and
1.6 log10 of that is exact arithmetic on *L* = 1000/*V* — it carries no sampling
uncertainty whatever. The pipette moves the measurable depth by more than the
laboratories differ.

The obvious counter-explanation is early killing: if the drug had already acted
by the day-zero reading, a spread in those readings would be kill rather than
inoculum. Where both arms have a day-zero reading, treated and untreated agree to
0.13 log10, so the spread is the inoculum. A second deposit gives the same result
against its own stated figure rather than against a standard: its Methods specify
10⁵ CFU/mL and its file measures 7 × 10⁵ to 2.8 × 10⁶, a median 12.2-fold above
nominal.

Distance from the McFarland reference is descriptive and is reported as such
(Table S2). Sitting far below it is the intended state, since the inoculum is
prepared by diluting from it, and the figure is not a measure of protocol
compliance. What determines the maximum observable log-kill depth is the measured
starting density and the real assay floor, not the turbidity the
preparation began from.

### 7. Faster killing often crosses the floor later

Across 191 pairs of flasks in the same treatment arm from different laboratories,
with 45 further pairs that the censoring could not settle and which are excluded
rather than imputed, **70 pairs — 36.6 per cent — are inversions**: the flask in which the population fell faster crossed
below the assay floor later (Table 6). Restricting to pairs whose rates differ by more
than 0.10 log10 per day, so that the faster flask is unambiguously faster, leaves
21.3 per cent of 94 pairs. The criterion *D_A*/*D_B* > *b_A*/*b_B* calls
83.8 per cent of pairs correctly, so the inversions are accounted for by the
arithmetic of the crossing-time decomposition in the Methods rather than by
anything else.

**Table 6.** Pairs of flasks in the same arm from different laboratories. An inversion is a pair in which the population that fell faster crossed below the assay floor later. 45 further pairs that the censoring could not settle are excluded rather than imputed. The last two columns decompose the spread in crossing time; the rate term is the larger in every arm.

| Arm | Comparable pairs | Inversions | Rate | 95% CI | Called by D/b criterion | Variance: distance | Variance: rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All arms pooled | 191 | 70 | 36.6% | 30.1-43.6% | 83.8% |  |  |
| INH 10X MIC |  |  |  |  |  | 31.4% | 68.6% |
| INH 1X MIC |  |  |  |  |  | 19.6% | 80.4% |
| MXF 10X MIC |  |  |  |  |  | 39.4% | 60.6% |


The effect holds when the faster flask is required to be unambiguously faster.
Raising the minimum separation between the two fitted rates removes pairs whose
rates barely differ: at 0.02 log10 per day the inversion rate is 34.5 per cent,
at 0.05 it is 30.4 per cent, and at 0.10 — a difference no reader would dispute —
it is 21.3 per cent of 94 pairs.

Those point estimates are firm; their precision is not, and the difference
matters. Pairs are not independent observations: 191 pairs are built from 42
flasks in six laboratories, and an interval that treats them as independent
Bernoulli trials reports a precision the design does not have. Resampling whole
flasks within laboratory puts the 36.6 per cent between 24.7 and 50.5 per cent;
resampling whole laboratories, which is the level at which the comparison is
actually made, puts it between 3.0 and 72.4 per cent. Under the strictest rate
separation the corresponding intervals are 7.6 to 42.7 per cent and 0 to 82.4 per
cent. The claim the deposit supports is therefore that inversions are common and
are explained by the decomposition, not that they occur at any particular rate.

The variance decomposition sets the size of the effect and bounds the claim. Of
the variation available to move a crossing time, the distance term carries 39.4
per cent at ten times moxifloxacin, 31.4 per cent at ten times isoniazid and 19.6
per cent at one times isoniazid; the rate term carries the remainder. **The rate
contributes more of the spread than the distance does in every arm.** A crossing
time is therefore not predominantly an inoculum measurement. It is a mixture, in
which the inoculum is a large minority contribution — large enough to reverse the
ranking in more than a third of comparisons, and not large enough to justify
treating the endpoint as an inoculum readout in general.


### 8. The same boundaries hold in an experiment the framework never saw

Every section so far tests the framework on the deposits it was built from. A
search of five general repositories, the tuberculosis consortia, the persistence
literature, food microbiology and the hollow-fibre field returned one deposit
carrying all three fields the boundaries require, and it was analysed cold.

Dubey and colleagues (2026) report amoxicillin-clavulanate against *Escherichia
coli* in a hollow-fibre system. Their Methods state 100 µL plated with counts per
mL, so *L* = 10 CFU/mL is derived rather than inferred, and the derivation is
corroborated inside the file: a 100 µL plate reporting per mL can return only
multiples of ten, and all 229 genuine counts in the deposit are multiples of ten
with the smallest exactly ten. Sixty-nine further entries read as one, which no
100 µL plate can produce, and are the deposit's below-limit placeholder.

Across the 20 cultures with a measured day-zero density, headroom runs 4.85 to
5.45 log10. Endpoints at 1, 2, 3 and 4 logs are reachable for every culture; a
5-log endpoint is unreachable for 5 of 20; a 6-log endpoint is unreachable for
all 20 (Table 10). The framework therefore locates, on data it was not built
from, the depth at which a sterilisation claim in this experiment stops being
demonstrable.

**Table 10.** Dubey et al. 2026, analysed cold. The floor is derived from a stated 100 uL plated volume and corroborated inside the file: all 229 genuine counts are multiples of ten and the smallest is exactly ten. Starting densities are the 20 measured day-zero counts, not the nominal inoculum the Methods state.

| Endpoint | N_reach (per mL) | Cultures | Unreachable | Per cent |
| --- | ---: | ---: | ---: | ---: |
| 1 log (90%) | 100 | 20 | 0 | 0% |
| 2 log (99%) | 1,000 | 20 | 0 | 0% |
| 3 log (99.9%) | 10,000 | 20 | 0 | 0% |
| 4 log (99.99%) | 100,000 | 20 | 0 | 0% |
| 5 log (99.999%) | 1,000,000 | 20 | 5 | 25% |
| 6 log (99.9999%) | 10,000,000 | 20 | 20 | 100% |


Two features of that deposit are worth recording because they are the failure
modes this framework is meant to catch. Its Methods give a nominal inoculum of
10⁵ CFU/mL while the file measures a median of 1.2 × 10⁶, so taking *N₀* from the
Methods rather than from the data would have placed a full order of magnitude
into every boundary. And its treated arm reads at or below the limit already at
day zero while the paired control reads about 10⁶, so that sample was drawn after
exposure rather than before it.

### 9. A late endpoint can erase a 32-fold dose difference

In the concentration-by-time grid, survivors across a 32-fold range of apramycin
separate 6.9-fold at day 3, 48.2-fold at day 7 and 5.2-fold at day 14 (Fig. 3,
Table 7). An experiment read at 14 days would report this drug as insensitive to
a 32-fold change in dose. Fitted per interval on a bootstrap resampling all three
replicates at both ends of every interval, the concentration slope is +0.059
log10 per day per doubling over days 0 to 3 (95 per cent interval +0.030 to
+0.088, p = 0.013), +0.033 over days 3 to 7 (−0.052 to +0.118, p = 0.24) and
−0.025 over days 7 to 14 (−0.060 to +0.010, p = 0.091); the early-versus-late
contrast is firm (+0.084, +0.037 to +0.128) and the early-versus-middle contrast
is not (p = 0.43).

**Table 7.** The same 32-fold concentration range summarised at each sampling day (upper rows), and the concentration slope fitted separately in each interval (lower rows). Slopes and intervals are from the replicate-level bootstrap described in Section 2.

| Read at | Survivor ratio (low/high dose) | log10 separation | Slope per doubling | 95% interval | p |
| --- | ---: | ---: | ---: | ---: | ---: |
| day 3 | 6.9x | 0.84 |  |  |  |
| day 7 | 48.2x | 1.68 |  |  |  |
| day 14 | 5.2x | 0.71 |  |  |  |
| days 0-3 |  |  | +0.0590 | +0.0302 to +0.0878 | 0.013 |
| days 3-7 |  |  | +0.0330 | -0.0517 to +0.1176 | 0.236 |
| days 7-14 |  |  | -0.0251 | -0.0602 to +0.0099 | 0.091 |


The sign of the late slope is not claimed. By day 14 the highest arm sits at
65 CFU/mL and the deposit states no limit of quantification and records no plated
volume, so no floor can be derived for it. At any floor of 100 CFU/mL or above —
the value 10 µL plating would give, and an assumption rather than a derivation —
that arm is censored and its apparent rate is a lower bound. What holds without
any assumption about the floor is that the separation collapses.

### 10. Inhibitory concentration and killing duration remain separate axes

That the two axes are separate is the premise of the framework that defines them
(Brauner et al. 2016), and the deposits bound rather than assert it. The
217-isolate file supports 24 comparisons between the concentration axis and the
duration axis. Four reach nominal significance where 1.2 are expected by chance
and none survives Benjamini–Hochberg correction (Fig. 4, Table 8). The four are
negative, so a higher inhibitory concentration accompanies a *shorter* duration,
which is not the direction a shared mechanism predicts, and they concentrate in
the deepest endpoint — the one Section 1 shows is compromised. The design
resolves correlations of 0.14 to 0.25 depending on stratum.

**Table 8.** The six strongest of the 24 comparisons the 217-isolate file supports. 4 reach nominal significance where 1.2 are expected by chance; none exceeds its Benjamini-Hochberg critical value. The final column is the correlation each design could have resolved at 95% confidence.

| Stratum | Endpoint | n | Spearman rho | p | BH critical value | Survives correction | Resolvable rho |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline only | MDK99.99 (15d) | 162 | -0.206 | 0.0086 | 0.0021 | no | 0.15 |
| INH-susceptible | MDK99.99 (15d) | 119 | -0.218 | 0.0171 | 0.0042 | no | 0.18 |
| INH-susceptible | MDK99 (60d) | 117 | -0.198 | 0.0324 | 0.0063 | no | 0.18 |
| all isolates | MDK99.99 (60d) | 187 | -0.153 | 0.0361 | 0.0083 | no | 0.14 |
| INH-susceptible | MDK99.99 (60d) | 117 | -0.179 | 0.0540 | 0.0104 | no | 0.18 |
| baseline only | MDK99.99 (60d) | 156 | -0.149 | 0.0628 | 0.0125 | no | 0.16 |


This null is narrower than it looks and we report it as such. Restricted to the
baseline isolates, where every isolate is from a different patient, the deepest
15-day endpoint gives ρ = −0.21 with p = 0.0086 against a corrected threshold of
0.0083 — it misses by three and a half per cent, in the same negative direction.
The axes are not shown to be independent here; they are shown not to be
positively coupled, which is what the deposits can support.

The same question in 126 evolved clones sharing an ancestor gives ρ = +0.043
(p = 0.63) against a resolvable ρ of 0.175, and independence holds within every
nutrient stratum separately. Stratifying is not optional there: the nominal
concentration is not a fixed exposure across those strata, since at 25 µg/mL the
same figure spans 0.55 to 9.47 times the inhibitory concentration each population
evolved to and straddles it (Table S1).

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
clinical deposit that prediction is exact isolate by isolate, including at the
boundary, where six isolates sit at *N*_id itself and are the six the strict
inequality leaves undecidable. In a deposit the framework was not built from it
locates the depth at which a sterilisation claim stops being demonstrable: five
of twenty cultures cannot show a five-log reduction, and none of the twenty can
show six.

The same arithmetic answers the objection that the starting density is fixed by
protocol. It is fixed as a turbidity, and a turbidity is not a viable count. Under
one written protocol the realised densities differed enough to change the deepest
demonstrable kill by 2.33 log10 between laboratories, and by 4.40 once the choice
of plated volume is included, since that choice sets the floor. A standard that
fixes what enters the flask does not thereby fix what the assay can resolve.

### What the tolerance phenotype tracks instead

Removing the assay's contribution leaves something rather than nothing, and what
remains is biologically coherent. Growth state predicts the tolerance class and
survives adjustment for starting density, which is the expected direction:
isoniazid requires KatG activation and active cell-wall synthesis, rifampicin
requires transcription, and a population that is not dividing presents less of
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
in the same file: resistant isolates enter the assay ten-fold lower and a quarter
of them lack the headroom the endpoint requires. We do not know why they seed
lower.
The natural explanation — that resistance carries a fitness cost — is not
supported here, since these isolates do not grow measurably more slowly and most
carry the near-neutral *katG* S315X allele. That gap is a finding in its own
right and belongs in the next study rather than in a speculative sentence in this
one. What the deposit can rule out, it does: adjusting the
resistance–inoculum association in turn for every usable pretreatment covariate
the file carries — sampling time, growth, both inhibitory concentrations, the
resistance mutation and both susceptibility calls — leaves the coefficient
between −0.66 and −0.96, the largest attenuation being 22 per cent for the
mutation identity (Table S6). The file records no referring site and no
processing batch, so those cannot be tested at all.


### How large the effect is

Where the inoculum is set deliberately rather than by clinical accident, the same
arithmetic operates and can be measured rather than inferred. In more than a
third of cross-laboratory comparisons the flask in which the population fell
faster crossed below the assay floor later, and the simple distance-over-rate
criterion accounts for six in seven of those inversions. Resampling whole
laboratories rather than pairs leaves that rate poorly determined — 3.0 to 72.4
per cent — so it is the mechanism and not the rate that the deposit establishes.

The variance decomposition sets the size of the effect. The rate term carries more of the
spread in crossing time than the distance term in every arm examined. A
crossing time is not mostly a measurement of the inoculum. It is a mixture in
which the inoculum is a large minority — enough to reverse the ranking of two
populations in a third of comparisons, which is the number that matters to anyone
choosing between two compounds, and not enough to license the claim that the
endpoint measures the starting culture.

### Relation to the analyses these deposits were made for

Our reading and van Wijk's agree where they overlap. They report the inoculum
spread themselves and conclude that baseline burden varied between laboratories
while net drug effect varied less; that conclusion anticipates part of ours and
belongs to them. The separation is that they excluded readings outside the
quantification limits from numerical analysis, which is a defensible reporting
decision that forecloses the question asked here, because it removes the
observations from which a duration is built.

Vijay and colleagues report associations between tolerance, resistance status and
treatment history in the same isolates. We do not dispute the measurements; the
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

Every conclusion this paper draws from the two primary deposits has been
recomputed at the level its observations are actually independent, and the result
is tabulated rather than summarised (Table 12): twenty survive unchanged, seven
survive with materially wider uncertainty, and five do not survive and have been
removed from the text.

**Table 12.** Every conclusion this paper draws from the two primary deposits, against uncertainty recomputed at the level the observations are actually independent. 20 survive unchanged, 7 survive with materially wider uncertainty, and 5 do not survive and have been removed from the text. The five that fail are all between-laboratory p-values computed on flasks: every flask in a laboratory shares a starting culture, so a comparison that looks like 67 flasks is six laboratories, and for a three-against-three split of six clusters the smallest attainable two-sided p is 0.10. They are deleted rather than corrected, because there is nothing to correct them to.

| Section | Conclusion as stated | Units treated as independent | Independent clusters | Method used instead | Verdict |
| --- | --- | --- | ---: | ---: | ---: |
| 4 | the difference between panels in the growth association is itself supported (interaction p = 0.0072) | unknown isolate-panel | 210 isolates | not recomputable | NOT SUPPORTED |
| 5 | starting density separates flasks that ever cleared from those that never did (AUC 0.974, p = 1.2e-10) | 67 flask | 6 | exact laboratory-level test (3 cleared vs 3 did not); cluster bootstrap over laboratories; permutation of clearance within laboratory, and within laboratory AND treatment arm | NOT SUPPORTED |
| 5 | in a Cox model, institutes D, E and F carry p = 0.015, 0.016, 0.015, which adjustment for starting density moves to 0.138, 0.172, 0.576 | 67 flask | 6 | cluster-robust sandwich on six clusters | NOT SUPPORTED |
| 5 | the log-rank test separates the six laboratories on time to clearance | 67 flask | 6 | none available: the grouping variable is the cluster | NOT SUPPORTED |
| 5 | institute C remains distinguishable after adjustment (HR 5.27, p < 0.001) | 67 flask | 1 | none available | NOT SUPPORTED |
| 1 | all 33 short isolates are at the ceiling; 88.0% of the rest are (Fisher p = 0.030) | 217 isolate | 174 patients min | baseline-only Fisher exact | WEAKENED |
| 5 | at ten times MIC of moxifloxacin the kill rate spans 5.2-fold between laboratories (0.090 to 0.464) | 6 laboratory-arm cell | 6 | cluster bootstrap over whole laboratories | WEAKENED |
| 5 | at one times MIC five of six laboratories record net growth | 6 laboratory-arm cell | 6 | Jeffreys interval on six clusters | WEAKENED |
| 5 / 7 | the laboratory effect lands on the duration endpoint and not on the rate; the rate is 'far more reproducible' | 42 flask | 6 | permutation of the laboratory label across flasks, within arm for the rate | WEAKENED |
| 6 | the deepest demonstrable kill differs by 2.33 log10 between laboratories at one plating volume | 12 day-zero reading | 4 | cluster bootstrap over whole laboratories | WEAKENED |
| 7 | 36.6% of 191 cross-laboratory pairs are inversions (95% CI 30.1-43.6) | 191 pair of flasks | 6 | cluster bootstrap over whole laboratories; also over flasks within laboratory; also delete-one-laboratory jackknife | WEAKENED |
| 7 | under the strictest rate separation the inversion rate is 21.3% of 94 pairs (95% CI 13.9-30.3) | 94 pair of flasks | 6 | cluster bootstrap over whole laboratories | WEAKENED |
| 1 | 33 of 217 isolates (15.2%) lack the headroom for a 4-log endpoint | 217 isolate | 174 patients min | baseline-only recount | SUPPORTED |
| 1 / 2 | 18 isolates rest on the floor at 15 days and 6 at 60 | 217 + 210 isolate-panel | 210 isolates | exact McNemar on the paired binary | SUPPORTED |
| 10 | no MIC-MDK association survives Benjamini-Hochberg | 6 tests isolate | 174 patients min | baseline-only family of six | SUPPORTED |
| 2 | 18 isolates at the floor; their survival span IS their inoculum span | 217 isolate | 174 patients min | baseline-only recount | SUPPORTED |
| 2 | 185 determinable, 12 forced by the inoculum, 6 undecidable | 203 isolate | 174 patients min | baseline-only reclassification | SUPPORTED |
| 2 | at 60 days the observability counts are 191, 6 and none, 'because the cultures are denser and few readings reach the floor' | 203 + 197 isolate-panel | 197 isolates | exact McNemar on the paired binary | SUPPORTED |
| 2 / 4 | the deep endpoint is unreachable for 26.2% of resistant against 7.6% of susceptible isolates | 217 isolate | 174 patients min | baseline-only Fisher exact | SUPPORTED |
| 4 | resistant isolates enter the assay ten-fold lower | 217 isolate | 174 patients min | baseline-only Mann-Whitney | SUPPORTED |
| 4 | the resistance-tolerance association attenuates by 66% and its interval then spans zero | 202 isolate | 174 patients min | baseline-only refit | SUPPORTED |
| 4 | growth state predicts the tolerance class and survives adjustment (beta = +0.027, p = 0.0025) | 202 isolate | 174 patients min | baseline-only refit | SUPPORTED |
| 4 | resistant isolates do not grow measurably more slowly (p = 0.24) | 217 isolate | 174 patients min | baseline-only Mann-Whitney | SUPPORTED |
| 4 | the confound thins between panels: 15.2% short of headroom at 15 days against 3.3% at 60 | 217 + 210 isolate-panel | 210 isolates | exact McNemar on the paired binary | SUPPORTED |
| 4 | the 60-day cultures are denser, so headroom is larger there | 420 treated as independent isolate-panel | 210 isolates | Wilcoxon signed-rank on the within-isolate change | SUPPORTED |
| 4 | the spread of starting densities more than halves between panels (IQR 1.00 to 0.42 log10) | 420 isolate-panel | 210 isolates | paired bootstrap resampling whole isolates | SUPPORTED |
| 5 | of 64 treated series the final step is not a decline in 48 (75%) | 64 series (one per treated flask) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| 5 | 44 of 64 series end more than one log10 above their own nadir | 64 series (one per treated flask) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| 5 / Limitations | 87.0% of the variance in flask starting density lies between laboratories | 85 flask | 6 | permutation of the laboratory label across flasks | SUPPORTED |
| 6 | including the choice of plated volume widens the spread in measurable depth to 4.40 log10 | up to 4 volumes x 5 laboratories laboratory-by-volume channel | 6 | no resampling required for the volume term | SUPPORTED |
| 7 | the criterion D_A/D_B > b_A/b_B calls 83.8% of pairs correctly | 191 pair of flasks | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| Methods | 83 of 498 below-limit flags (16.7%) are contradicted by another plating of the same sample at the same visit | 498 flag (one reading) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |


The between-laboratory evidence is six clusters. Every flask in a laboratory
shares a starting culture, so the effective sample size for any comparison
*between* laboratories is six and not the 67 to 85 flasks the tables list. Six is
too few for asymptotic cluster-robust standard errors, and fitting them anyway
does not fail loudly: on these data the sandwich returns a smaller p for every
institute term than the model-based p it was meant to correct. Where a comparison
is between laboratories we therefore quote the exact laboratory-level test or a
cluster bootstrap and, where the design cannot produce a meaningful p at all, no
p. Three laboratories recorded crossings and three did not, and for that split
the smallest attainable two-sided p is 0.10. Quantities for which flasks *are*
exchangeable across laboratories — the variance shares, and the inversion rate
under a flask bootstrap — keep an exact permutation test and are the strongest
between-laboratory evidence the deposit holds.

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

## Conclusion


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

## Methods

### Datasets

Five published deposits are analysed (Table 1). Four carry the analysis and the fifth is held out to test it. None was generated for this
study, all are openly licensed, and no dataset was selected after its result was
known.

**Table 1.** The five published deposits reanalysed. Four carry the analysis and the fifth is held out to test it. None was generated for this study, and none was selected after its result was known.

| Dataset | Organism | Drug and range | Design | Deposit | Licence |
| --- | --- | --- | --- | --- | --- |
| Six-laboratory exercise | *M. tuberculosis* H37Rv | moxifloxacin, isoniazid, 1x and 10x MIC | 90 flasks, 2 775 readings | figshare 19766083 | CC BY 4.0 |
| Clinical isolates | *M. tuberculosis*, 217 isolates | rifampicin | 6 duration endpoints per isolate | eLife 93243, suppl. file 2 | CC BY 4.0 |
| Evolved clones | *E. coli*, 126 clones | amikacin | MIC and persister fraction per clone | Zenodo 7550302 | CC BY 4.0 |
| Concentration-by-time grid | *M. tuberculosis* | apramycin, amikacin, 1-128 ug/mL | 5 concentrations x 4 days x 3 replicates | figshare 26462791 | CC BY 4.0 |
| Held out for validation | *E. coli*, hollow fibre | amoxicillin-clavulanate | 20 cultures, measured day-zero density, 100 uL plated | Nat Commun 2026 Source Data | CC BY 4.0 |


**Clinical isolates with a deposited tolerance classification.** 217 *M.
tuberculosis* isolates assayed under rifampicin, each carrying a minimum
inhibitory concentration, minimum durations for 90, 99 and 99.99 per cent killing
at 15 and 60 days of prior culture, most probable number readings at days 0, 2
and 5, a growth-rate proxy, isoniazid susceptibility with the resistance mutation
where present, months on treatment, and the authors' own tolerance level for each
isolate (Vijay et al. 2024; eLife 93243 supplementary file 2). The killing assay
runs for six days, so an isolate not reaching its target within that window is
recorded at the ceiling. Of the 217 rows, 43 are follow-up isolates from patients
already represented, so a baseline-only stratum is analysed separately.

**The six-laboratory exercise.** *M. tuberculosis* H37Rv from one stock,
distributed with one written protocol to six laboratories blinded and labelled A
to F (van Wijk et al. 2023; figshare 19766083, CC BY 4.0). Moxifloxacin and
isoniazid at one and ten times the minimum inhibitory concentration, an untreated
control, three flasks per arm, sampled to day 21 or 28. Each sample was plated at
four volumes: 100 µL in quadruplicate, 10 µL as four drops, 10 µL as a single
drop, and 2.5 µL as a single drop. In the deposited file the colony count is
already expressed per millilitre, confirmed by the smallest count recorded at
each volume being exactly 1000 divided by that volume, which is one colony per
millilitre. The minimum reportable positive count is therefore a property of the
plated volume — one colony in that volume — and equals 1.0, 2.0, 2.0 and
2.6 log10 CFU/mL respectively, so four platings give three distinct floors
spanning 1.6 log10 within a single flask-visit. The identity is exact for 1 055
of the 1 068 readings at 10 µL; the thirteen exceptions all come from one
laboratory and do not lie on the lattice its recorded volume implies. The file
holds 2 775 readings, of which 17.9 per cent are flagged below the floor and 24
above it; the analysis set, after dropping above-limit flags, unusable values and
pre-treatment visits, is 2 580 readings, of which 19.3 per cent are flagged.

**Evolved clones.** 126 *Escherichia coli* clones from a parallel evolution
experiment under amikacin, each carrying an endpoint minimum inhibitory
concentration and a persister fraction measured on the same clone, labelled by
the antibiotic concentration and nutrient level its population evolved under
(Windels et al. 2024; Zenodo 10.5281/zenodo.7550302, CC BY 4.0).

**A deposit held out for validation.** Amoxicillin-clavulanate against
*Escherichia coli* in a hollow-fibre infection model, with 100 µL plated and
counts per mL so the assay floor is derived rather than inferred,
measured day-zero densities for every culture rather than a nominal inoculum, and
below-limit readings retained as a placeholder (Dubey et al. 2026; article Source
Data, CC BY 4.0). It was located by a search of five general repositories, the
tuberculosis consortia, the persistence literature, food microbiology and the
hollow-fibre field, and was the only deposit found carrying all three fields the
boundaries require. It contributes to no analysis except Section 8, where the
framework is applied to it cold.

**Concentration-by-time grid.** Apramycin and amikacin against *M. tuberculosis*
at 128, 32, 8, 4 and 1 µg/mL, triplicate log10 CFU at days 0, 3, 7 and 14, with a
concurrent drug-free control at every visit (Kaur et al. 2024; figshare 26462791,
CC BY 4.0).

### Two kinds of limit, kept apart

No deposit analysed here reports a validated limit of quantification with a
value. The six-laboratory file names the concept in the definitions of its BQL
and AQL columns but defines it as whether the plate was countable, which is an
operator's judgement rather than a validated limit. Throughout this paper *L* is
therefore an **operational assay floor**: where a plated volume is recorded it is
the **minimum reportable positive count**, one colony in that volume, and where
none is recorded it is inferred from the deposit and is labelled as inferred. The
term limit of quantification is used only in reporting what a source states.
What *L* is in each deposit, how it was arrived at, and how replicate plates and
plated volumes were treated is tabulated deposit by deposit (Table 11).

**Table 11.** What the boundary *L* is in each deposit analysed. No deposit reports a validated limit of quantification with a value. The six-laboratory file names the concept in the definitions of its below- and above-quantification-limit columns but defines it as whether the plate was countable, which is an operator's judgement. DERIVED means the value follows arithmetically from a recorded plated volume; INFERRED means it was read off the deposit's own behaviour and is labelled as inferred wherever it is used; NONE means no floor is evidenced and none is assumed. Where a plated volume is recorded the honest term is the minimum reportable positive count, one colony in that volume; elsewhere it is an operational assay floor.

| Deposit | States an LOD | States an LOQ | Value used | Units | How obtained | What it should be called |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Vijay 2024 | no | no | 23 | MPN per mL | INFERRED | operational assay floor |
| ERA4TB 2023 | no | term only | 10, 100 and 400, per plated volume | CFU per mL | DERIVED | minimum reportable positive count |
| Windels 2024 | no | no | none; no value is recoverable | surviving fraction, dimensionless | FLAGGED | no floor is established; a below-limit reading is written as exact zero and fixes no value |
| Kaur 2024 | no | no | none; no floor is used | log10 CFU per mL | NONE | no floor is evidenced; the smallest reading is the smallest reading |
| Dubey 2026 | no | no | 10 | CFU per mL | DERIVED | minimum reportable positive count |


Two distinct censoring problems arise and are handled separately, because
conflating them is the error this paper is about.

A **count below the assay floor** is left-censored: the population is somewhere
below a known value. In the six-laboratory deposit that value is a property of
the plated volume, as above. In the clinical deposit the readings are most
probable numbers taking the discrete values of an MPN table, and the day-5 column
bottoms out at 23 per mL with a visible pile-up there; that value is treated as
the floor, and the first Results section reports the evidence for it.

That deposit states no limit of quantification, so the floor is inferred rather
than read off, and the inference is bounded rather than asserted. Three things
support it: 23 per mL is the smallest value anywhere in the file, nothing lies
below it in 1 932 readings, and the minimum shifts by exactly a factor of ten per
visit — 2 300, 230, 23 — in all three culture ages, which is the signature of one
dilution series applied to a differently diluted sample at each timepoint. Since
none of that is proof, the load-bearing count is recomputed at every value a
three-tube MPN table returns below 23. The number of isolates lacking four logs
of headroom is 33 at a floor of 23 and does not fall below 28 at a floor of 3.0,
the lowest such table returns. The conclusion holds across the whole range, so it
is not an artefact of where we place the floor, and the same sweep is run for
every deposit that carries a floor (Table S4).

The six-laboratory deposit also carries the evidence for judging each reading
against its own volume rather than pooling. Each sample is plated at four
volumes at the same visit, so a below-limit flag can be checked against the other
platings of the same flask. Of its 498 flags, 83, or 16.7 per cent, are
contradicted: another plating of the same sample at the same visit, with a limit
at least as sensitive, returns a quantified count above the flagged reading's
limit. Those flags record a drop that missed rather than a culture that fell.
Pooling the four volumes to a single limit would treat them as evidence about the
population; judging each against the floor its own volume implies does not, and
that is the reason the analysis is built the way it is. The cost of pooling can
be priced. Pooling at the least sensitive volume would discard 126 genuine
quantified counts, 5.9 per cent of them, and pooling changes the contradicted-flag
rate itself: 16.7 per cent judged per volume, against 43.2 per cent pooled at
10 CFU/mL and 15.3 per cent pooled at 400. The audit's own answer depends on the
choice, which is the strongest reason to make it explicitly.

A **crossing time not observed within the study** is right-censored: the event
has not happened yet, which is not the same as the event having no time. A flask
that never fell below the limit contributes the information that its crossing
time exceeds its last visit, and enters the survival likelihood as such. It is
never recorded as missing.

### Floor posterior, refusal, and what is not learned

The algebra of headroom and observability is closed form once *L* is known. What
requires inference is *L* itself, and the two cases are not alike. A
volume-derived floor — one colony in *V* µL is 1000/*V* per mL, and the observed
minimum equals that value — is a point mass, with nothing to infer. A floor
inferred from a pile-up on a most-probable-number rung carries a discrete
posterior over the rungs at or below the observed minimum; the interval quoted is
the 95 per cent highest-posterior-density support.

That distinction is turned into a rule rather than a caveat. Where the verdict is
that no floor is evidenced, or where the support spans more than one log10, the
observability labels are **refused** rather than reported (Table 14). Surviving
fractions written as exact zeros with no named *L* fall in that refused class, as
does a deposit whose minimum occurs once in a continuous tail. The clinical
deposit passes the rule with a support of 0.40 log10; two of the five deposits
fail it and are labelled accordingly. This paper fits nothing to predict an MDK:
once *L* is in hand the rest is derived.

### Causal mediation of the resistance association

The attenuation of the resistance coefficient once starting density enters the
model is reported in the Results as a descriptive ratio, which is what it is.
Separately, a linear product-of-coefficients mediation decomposes the total
effect of isoniazid resistance on the day-5 tolerance class into an average
causal mediation effect through log10 *N₀* and an average direct effect, with
bootstrap percentile intervals from 5 000 resamples, repeated on the baseline
stratum and on two binary collapses of the outcome.

Sequential ignorability is assumed and is not testable here, so the estimate is
accompanied by the sensitivity that matters: the residual correlation between
mediator and outcome errors at which the point estimate crosses zero, which is
about −0.24. The outcome is an ordinal class scored linearly, as in the
association family; the binary collapses are reported because they do not depend
on that scoring. No claim is made that unmeasured confounding is absent. The
estimate replaces the attenuation percentage as the quantity cited for the
pathway (Table S5).

Fold-change figures such as 216-fold and 265-fold are ten raised to the unrounded
log10 difference before display rounding, so that Δ*h* = 2.3349… is reported as
216-fold rather than as 10^2.33.

### Dynamic range, and the two boundaries it sets

For a culture starting at *N₀* against an assay floor *L*, two quantities
are used and are kept apart, because they are not interchangeable:

  *H* = *N₀*/*L*, a ratio;
  *h* = log10(*N₀*/*L*), the **headroom**, in log10 CFU/mL.

The headroom is the deepest reduction the assay can resolve. It is fixed by the
dilution scheme and the starting culture before any drug acts, and variation
between cultures is reported on *h* rather than on *N₀*, as Δ*h* = max(*h*) −
min(*h*) with the corresponding fold difference 10^Δ*h*. That distinction is not
notational here. Where *L* is set by the plated volume, one culture read on a
2.5 µL drop and on a 100 µL quadruplicate differs by 1.6 log10 in headroom, and a
figure computed from *N₀* alone would discard it.

Two boundaries follow from the definitions alone.

**Reachability.** The smallest value the assay reports as a measurement is *L*,
so the largest reduction expressible as a measured value is *h*. A *q*-log
endpoint is therefore observable if and only if

  *N₀* ≥ *N*_reach = *L* · 10^*q*.

**Identifiability.** A censored reading places the true count in [0, *L*], so the
recorded surviving fraction is at most *L*/*N₀* — an upper bound, not a
measurement. Given class thresholds 0 < *c*₁ < *c*₂ …, the class is determined by
the data only if the whole interval [0, *L*/*N₀*] lies inside one class. Since
that interval contains zero, the only candidate is the lowest class, so the class
is determined if and only if

  *N₀* > *N*_id = *L*/*c*₁.

Above that boundary the lowest class is the only one compatible with a censored
reading, whatever the true count was, so the class the rule assigns is fixed by
*N₀* rather than by the surviving population. The boundary says nothing about
whether a culture reaches the floor, which depends on the drug; it says what the
classification can mean once one has. Both
boundaries are properties of the method and involve neither the drug nor the
strain, and their ratio is *N*_reach/*N*_id = *c*₁ · 10^*q*.

Seeding a culture above *L* · max(10^*q*, 1/*c*₁) makes both failure modes
impossible, which is a design criterion computable before an experiment rather
than a diagnosis after it.

### Estimation

A **Tobit model** fits log10 CFU/mL linearly in time by maximum likelihood. An
observed reading contributes the usual Gaussian density; a censored reading
contributes log Φ((limit − µ)/σ), the probability that it fell below its own
limit. This is Beal's M3 (Beal 2001) written for this assay. Intervals come from
the profile likelihood.

**Multiple imputation** draws each censored reading from the fitted normal
truncated at its own limit, refits by ordinary least squares, and pools 50 fits
by Rubin's rules. It makes a different assumption from the Tobit model about what
happened below the limit, so agreement between them shows the answer is not
driven by either.

**The tolerance label** is modelled as an ordered categorical outcome by
proportional-odds ordinal logistic regression, with starting density as a
prespecified covariate and every association reported unadjusted and adjusted for
it. The MDK category of the deposited label is a fourth, unordered category and
is excluded; all 14 rows carrying it fall outside the susceptible-versus-resistant
contrast in any case, so the ordinal and linear models are fitted to identical
rows. Proportional odds is tested by a Brant test per predictor and by a
likelihood-ratio test against a generalised ordered logit with the coefficient
released; where it fails, the released partial-proportional-odds fit is reported
and checked against a multinomial fit that assumes no ordering. Rows are dropped
only for a missing outcome, predictor or starting density, and the dropped rows
are compared with the retained ones on starting density and susceptibility.
Because the deposit carries no patient identifier, the repeated-isolate structure
is handled by a baseline-only stratum rather than by a random effect, and the
linear models of the earlier analysis are retained as a sensitivity comparison
(Table S3).

**Time-to-event analysis** treats the **first observed crossing below the assay
boundary** as the event, with series never falling below their own floor
right-censored at their last visit. The event is named that way throughout and is
not read as clearance, sterilisation or the end of a culture: of the series that
cross, 60 per cent read above the boundary again at a later visit.

The crossing time is interval-censored, not observed: it lies between the last
visit above the boundary and the first visit below it, and the visit schedule is
coarse. Interval-censored fits are therefore reported alongside the naive
treatment that pins the event to the visit at which the blank plate was noticed.
Kaplan–Meier and Cox proportional hazards are retained as **descriptive**
summaries of first crossing only; their intervals are replaced by cluster
bootstraps over laboratories and over flasks, because 261 series come from 72
flasks in 6 laboratories and the partial likelihood treats them as independent.
No p-value is quoted for a term that is constant within laboratory, since six
clusters cannot support one. Proportionality is tested on Schoenfeld residuals.

A cell is fitted only when it retains at least six quantified readings at three
distinct times; below that the slope is determined by the censoring pattern
rather than by the counts.

### The decomposition of a crossing time

Over an interval in which the decline is close to log-linear, log10 *N*(*t*) =
*a* − *bt*, and with *ℓ* the log10 assay floor and *D* = *a* − *ℓ* the
distance the population starts above it, the crossing time is *T* = *D*/*b*. For
two flasks,

    log(T_A / T_B) = log(D_A / D_B) − log(b_A / b_B)

which is exact on this model and splits a difference in crossing time into a
distance term and a rate term. An **inversion** is a pair in which A fell faster
yet crossed later, which occurs exactly when *D_A*/*D_B* > *b_A*/*b_B*. A single
slope is not a full description of a biphasic trajectory, so *b* is the average
decline over the window fitted, and the variance shares reported below are shares
of that averaged slope; averaging across decline and regrowth moves the rate term
up rather than down, so the distance share is a lower bound; *D* is taken from the measured day 0 to 1 density
rather than from the fitted intercept, because a single line through a biphasic
curve extrapolates back to an intercept well below the culture the flask started
from.

### Multiplicity

Where a question admits more than one test, every test the deposit supports is
run, and the family is corrected by the Benjamini–Hochberg procedure at a false
discovery rate of 5 per cent. For each test we report the correlation the sample
size could have resolved at 95 per cent confidence, so that a null is bounded
rather than asserted.

### Reproducibility

Every number in this paper is regenerated by a script that writes a receipt
recording the software versions it ran under, and a separate audit script
recomputes each quantity quoted in the text from the table it came from and
reports any that disagree. Every table is generated from the results files and
the manuscript is assembled from that generated material, never edited
downstream of it, so a table cannot drift from the analysis behind it. Analyses
used Python 3.14 with numpy 2.5.0, scipy 1.18.0, pandas 3.0.3, statsmodels
0.15.0 and lifelines 0.30.3.

---

## Data and code availability

Every dataset analysed here is already public under an open licence, and each is
identified by its deposit in Table 1. Nothing in this study required new patient
samples or new experimental data.

The analysis code, the audit script, the headroom tool described above and the
machine-readable receipts recording the software versions each stage ran under
will be released in a public repository on publication. Every number quoted in this manuscript is regenerated
from the deposits by that code, and a separate audit stage recomputes each one
from the table it came from and reports any that disagree.

---

## Declarations

**Ethics.** This study reanalysed publicly available, de-identified datasets. No
new patient samples were collected and no new experimental data were generated.

**Funding:** [to be inserted]

**Competing interests:** [to be inserted]

**Author contributions:** [to be inserted]

**Archived version:** [commit identifier of the submitted version, to be inserted]

---

## References

[Deliberately not yet compiled. The reference list is held back until the text
stops moving, so that citations are not renumbered repeatedly. Sources are named
in full in the text and in the deposit table.]

---

## Figure legends

![Figure 1](../results/figures/fig14_dynamic_range.png)

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
eighteen isolates whose day-5 reading was censored at the floor. Their true final
counts are unknown below *L*, so the assay cannot distinguish their final viable
burdens; what is plotted is the recorded fraction *L*/*N₀*, which is what a
censored reading computes, so the 265-fold span in apparent survival is exactly
the 265-fold span in starting density. The dotted lines are the deposited
classification thresholds. Which side of the low/medium cut an isolate falls on
is settled by where it began, not by what the reading measured — though reaching
the floor at all required rifampicin to cover that isolate's whole headroom, at
least 3.00 logs for the shallowest and 5.42 for the deepest. For the twelve below
the cut, no count the assay admits leaves any class but **low** compatible; for
the six above it the compatible range straddles the cut and two classes
remain.

![Figure 2](../results/figures/fig10_rate_vs_duration.png)

**Figure 2. Where the inoculum is set by protocol, the two summaries still
diverge.** Six laboratories, one written protocol, one stock of *M. tuberculosis*
H37Rv, moxifloxacin at ten times the minimum inhibitory concentration.
(**A**) The kill rate by censored maximum likelihood with 95 per cent
profile-likelihood intervals; every laboratory yields one, spanning 5.2-fold.
(**B**) Kaplan–Meier curves for time to the first observed crossing below the
assay boundary. Three
curves never descend: those laboratories recorded no flask below the limit in any
arm, so their first-crossing times are right-censored throughout. (**C**) The two
summaries against each other. The three lowest starting densities are exactly the
three laboratories that recorded crossings; the kill rate produces no such
separation.
(**D**) The p-value attached to each laboratory in a Cox model before (grey) and
after (arrow head) starting density is added. Blue: crosses from significant to
not. Orange: institute C remains distinguishable, and it also returns the fastest
rate.

![Figure 3](../results/figures/fig11_endpoint_collapse.png)

**Figure 3. A late endpoint cannot resolve a 32-fold concentration range.**
Apramycin against *M. tuberculosis*, five concentrations, triplicate counts.
(**A**) The trajectories, with an assumed floor of 100 CFU/mL — the value 10 µL
plating would give — drawn as a band; this deposit records no plated volume, so
the band is an assumption and is drawn to show what the assumption costs; by day 14 the highest arm lies within it, so its apparent rate
over the final interval is a lower bound. (**B**) The ratio of survivors between
the lowest and highest concentration at each sampling day, rising to 48.2-fold at
day 7 and collapsing to 5.2-fold at day 14. (**C**) The concentration slope fitted
separately in each interval from a replicate-level bootstrap, 20 000 draws.

![Figure 4](../results/figures/fig12_independence.png)

**Figure 4. Resistance and tolerance occupy separate axes, in two designs.**
(**A**) All 24 comparisons between the concentration axis and the duration axis
that the 217-isolate file supports, each against the Benjamini–Hochberg critical
value it would have to beat. Amber marks the four reaching nominal significance;
none survives. (**B**) The censoring behind them: the fraction of isolates at the
assay ceiling rises with endpoint depth, and the nominal hits concentrate where
censoring is heaviest. (**C**) The same question in 126 evolved *E. coli* clones,
by nutrient stratum.
