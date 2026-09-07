# Supplemental material

**Score only the kill the assay can see: starting density and the floor bound every MDK**

Vahhab Piranfar

---

## Supplementary text

### Text S1. A turbidity standard fixes what goes in, not what the plate can resolve

A time-kill inoculum is not chosen freely: a suspension is matched to 0.5
McFarland and diluted, and NCCLS M26-A (approved guideline, 1999; the body is now
CLSI, which has archived the document) puts the target near 5 × 10⁵ CFU/mL [[R31]]. If the
protocol fixes the starting density, the preceding sections describe a variable
that does not vary.

Two properties of the standard make this answerable with counts. A McFarland
figure is a turbidity, matched optically [[R32]], and counts live cells, dead cells,
debris and a clump as one particle [[R32]]; converting it to CFU/mL assumes a cell size,
shape and dispersal that *M. tuberculosis* does not oblige, and tuberculosis
protocols work from a range of dilutions and target inocula [[R33]]. And the standard
fixes what goes in, while what is needed here is what the plate counts, separated
from it by a dilution, a transfer and whatever aggregation occurs on the way.

In the six-laboratory exercise, the untreated arm at day zero on the 100 µL
plating gives realised densities of 3.67, 4.61, 4.65 and 6.00 log10 CFU/mL for
institutes B, C, D and F. Institute E deposits no untreated day-zero reading at
any volume, its series beginning at day one, and institute A's three readings at
that plating are flagged above the quantification limit rather than counted. Three
of the four sit below the M26-A target, by 11-, 12- and 107-fold; the fourth sits
two-fold above it. Every
figure in this section is on that one basis — untreated, day zero, 100 µL — which
is not the basis of Table S7 and is not expected to match it.

Reported as headroom at a fixed plating volume the spread is Δ*h* = 2.33 log10, a
216-fold difference in measurable capacity under one written protocol (Table S12),
and that figure needs its roster stated because it is small. It is a
maximum-minus-minimum over those same four laboratories — B at *h* = 2.67, C at
3.61, D at 3.65 and F at 5.00, each exactly one log10 below the density above it,
since *L* = 10 CFU/mL at this plating. Institute A's other platings put it near
*h* = 2.4, so including it would widen the spread rather than narrow it. A range over four
draws is a fragile statistic: its cluster-bootstrap 95 per cent interval runs from
0.05 to 2.33 log10, the upper limit being the observed range by construction.

The stronger version of the same argument does not depend on that roster at all.
Including the choice of plated volume widens the spread to Δ*h* = 4.40 log10, and
1.6 log10 of that is exact arithmetic on *L* = 1000/*V* — it carries no sampling
uncertainty whatever. The pipette moves the measurable depth by more than the
laboratories differ.

The obvious counter-explanation is early killing: if the drug had already acted
by the day-zero reading, a spread in those readings would be kill rather than
inoculum. Only institutes C and D deposit a day-zero reading in both arms, and there
treated and untreated agree to 0.06 and 0.13 log10 respectively, so for those two
the spread is the inoculum and not early kill. The other four cannot be checked
this way. Institute F shows why the check matters and why it is not decisive: its
treated day-one readings average 6.62 log10, above its untreated day-zero reading
of 6.00, because the untreated culture itself grows to 6.72 over the same
twenty-four hours. A day-one reading is not a day-zero reading in either
direction. A second deposit [[R36]][[R8]] gives the same result
against its own stated figure rather than against a standard: its Methods specify
10⁵ CFU/mL and its file measures 7 × 10⁵ to 2.8 × 10⁶, a median of 1.215 × 10⁶ and
so 12.15-fold above nominal — computed from the unrounded median, which Table S12
displays rounded to 6.08 log10.

Distance from the McFarland reference is descriptive and is reported as such
(Table S13). Sitting far below it is the intended state, since the inoculum is
prepared by diluting from it, and the figure is not a measure of protocol
compliance. What determines the maximum observable log-kill depth is the measured
starting density and the real assay floor, not the turbidity the
preparation began from.

### Text S2. The population that fell faster often crossed the floor later

Across 191 pairs of flasks in the same treatment arm from different laboratories,
with 45 further pairs that the censoring could not settle and which are excluded
rather than imputed, **70 pairs — 36.6 per cent — are inversions**: the flask in which the population fell faster crossed
below the assay floor later (Table S14). Restricting to pairs whose rates differ by more
than 0.10 log10 per day, so that the faster flask is unambiguously faster, leaves
21.3 per cent of 94 pairs. The criterion *D_A*/*D_B* > *b_A*/*b_B* calls
83.8 per cent of all 191 pairs correctly, but that figure is carried by the easy
majority: 63.4 per cent of pairs are not inversions, and the criterion gets 97.5
per cent of those right against 60.0 per cent of the inversions themselves. The
decomposition therefore identifies the mechanism — a pair inverts when the
distance ratio exceeds the rate ratio — without predicting which pairs invert
much better than three times in five. The residual is what a single averaged
slope through a biphasic trajectory cannot capture, which the Methods state as a
known limitation of *b*.

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
per cent at ten times moxifloxacin, 31.4 per cent at ten times isoniazid and
19.6 per cent at one times isoniazid; the rate term carries the remainder. **The
rate contributes more of the spread than the distance does in each of the three
arms that can be decomposed.** The fourth treated arm, moxifloxacin at one times
the inhibitory concentration, is not among them: five of six laboratories record
net growth there, and only one flask in the arm returns a positive fitted rate,
so there is no spread in the rate to divide (Table S14). A crossing time is
therefore not predominantly an inoculum measurement. It is a mixture, in which
the inoculum is a large minority contribution — large enough to reverse the
ranking in more than a third of comparisons, and not large enough to justify
treating the endpoint as an inoculum readout in general.

### Text S3. Inhibitory concentration and killing duration remain separate axes

That the two axes are separate is the premise of the framework that defines them
(Brauner et al. 2016) [[R2]], and the deposits bound rather than assert it. The
217-isolate file supports 24 comparisons between the concentration axis and the
duration axis, and those 24 are the correction family throughout: the
Benjamini–Hochberg critical values in Table S15 are ranked against 24, not against
the size of any one stratum. Four reach nominal significance where 1.2 are
expected by chance and none survives correction (Fig. 4, Table S15). The four are
negative, so a higher inhibitory concentration accompanies a *shorter* duration,
which is not the direction a shared mechanism predicts, and they concentrate in
the deepest endpoint — the one Section 1 shows is compromised. Across all 24 tests the design
resolves correlations of 0.14 to 0.25 depending on stratum; the six strongest,
which Table S15 lists, span 0.14 to 0.18.

This null is narrower than it looks and we report it as such. Restricted to the
baseline isolates, where every isolate is from a different patient, the deepest
15-day endpoint gives ρ = −0.21 with p = 0.0086. Against the family of 24 its
critical value is 0.0021 and it is nowhere near; treated as a pre-specified
family of six baseline tests in its own right the threshold would be 0.0083 and
it would miss by three and a half per cent. The family of 24 is the one this
paper corrects against, so the honest reading is the first; the second is
recorded only because the direction is the same negative one.
The axes are not shown to be independent here; they are shown not to be
positively coupled, which is what the deposits can support.

The same question in 126 evolved clones sharing an ancestor [[R38]][[R6]] gives ρ = +0.043
(p = 0.63) against a resolvable ρ of 0.175, and independence holds within every
nutrient stratum separately. Stratifying is not optional there: the nominal
concentration is not a fixed exposure across those strata, since at 25 µg/mL the
same figure spans 0.55 to 9.47 times the inhibitory concentration each population
evolved to and straddles it (Table S16).

---

## Supplementary methods

### Datasets

Five published deposits are analysed (Table 1). Four carry the analysis and the fifth is held out to test it. None was generated for this
study and all are openly licensed. The held-out deposit was opened only after
every boundary and threshold was fixed, which the commit history of the analysis
repository timestamps; the other four were chosen for the fields they carry, and
that choice is not separately registered.

**Clinical isolates with a deposited tolerance classification.** 217 *M.
tuberculosis* isolates assayed under rifampicin, each carrying a minimum
inhibitory concentration, minimum durations for 90, 99 and 99.99 per cent killing
at 15 and 60 days of prior culture, most probable number readings at days 0, 2
and 5, a growth-rate proxy, isoniazid susceptibility with the resistance mutation
where present, months on treatment, and the authors' own tolerance level for each
isolate (Vijay et al. 2024; eLife 93243 supplementary file 2) [[R5]]. The killing assay
runs for six days, so an isolate not reaching its target within that window is
recorded at the ceiling. Of the 217 rows, 43 are follow-up isolates from patients
already represented, so a baseline-only stratum is analysed separately.

**The six-laboratory exercise.** *M. tuberculosis* H37Rv from one stock,
distributed with one written protocol to six laboratories blinded and labelled A
to F (van Wijk et al. 2023; figshare 19766083, CC BY 4.0) [[R23]][[R4]]. Moxifloxacin and
isoniazid at one and ten times the minimum inhibitory concentration, an untreated
control, three flasks per arm, sampled to day 21 or 28. Each sample was plated at
four volumes: 100 µL in quadruplicate, 10 µL as four drops, 10 µL as a single
drop, and 2.5 µL as a single drop. In the deposited file the colony count is
already expressed per millilitre, confirmed by the smallest count recorded at
each volume being exactly 1000 divided by that volume, which is one colony per
millilitre. The minimum reportable positive count is therefore a property of the
plated volume — one colony in that volume — and equals 1.0, 2.0, 2.0 and
2.6 log10 CFU/mL respectively, so four platings give three distinct floors
spanning 1.6 log10 within a single flask-visit [[R34]]. The identity is exact for 1 055
of the 1 068 readings at 10 µL; the thirteen exceptions all come from one
laboratory and do not lie on the lattice its recorded volume implies. The file
holds 2 775 readings, of which 17.9 per cent are flagged below the floor and 24
above it; the analysis set, after dropping above-limit flags, unusable values and
pre-treatment visits, is 2 580 readings, of which 19.3 per cent are flagged.

**Evolved clones.** 126 *Escherichia coli* clones from a parallel evolution
experiment under amikacin, each carrying an endpoint minimum inhibitory
concentration and a persister fraction measured on the same clone, labelled by
the antibiotic concentration and nutrient level its population evolved under
(Windels et al. 2024; Zenodo 10.5281/zenodo.7550302, CC BY 4.0) [[R38]][[R6]]. Six of its
595 surviving fractions are written as exact zeros, marking a below-limit reading
without naming a limit; they fix no floor, so this deposit is one of the two for
which observability labels are refused.

**A deposit held out for validation.** Amoxicillin-clavulanate against
*Escherichia coli* in a hollow-fibre infection model, with 100 µL plated and
counts per mL so the assay floor is derived rather than inferred,
measured day-zero densities for every culture rather than a nominal inoculum, and
below-limit readings retained as a placeholder (Dubey et al. 2026; article Source
Data, CC BY 4.0) [[R36]][[R8]]. It was located by a search of five general repositories, the
tuberculosis consortia, the persistence literature, food microbiology and the
hollow-fibre field, and was the only deposit found carrying all three fields the
boundaries require. No boundary, threshold or modelling choice in this
paper was informed by it: it was opened after all of them were fixed, and
Section 6 is the only place it tests anything. What cannot be documented is the
search itself. The repositories were searched interactively and no query log,
access date or screening count was kept, so this paper reports the outcome of
that search — one deposit carrying a measured per-culture starting density, a
recorded plated volume and per-culture time-course counts together — without
being able to evidence its extent. The claim that no deposit was selected after
its result was known rests on the commit history of this repository rather than
on a registration, and readers should weigh it accordingly. It does appear
descriptively — a row of its own in Tables 2, 5, 9, 15, S5 and S7, and a table of
its own in Table S9 — which is reporting rather than fitting.

**Concentration-by-time grid.** Apramycin and amikacin against *M. tuberculosis*
at 128, 32, 8, 4 and 1 µg/mL, triplicate log10 CFU at days 0, 3, 7 and 14, with a
concurrent drug-free control at every visit (Kaur et al. 2024; figshare 26462791,
CC BY 4.0) [[R37]][[R7]]. The amikacin arms are not analysed here. Within apramycin the 1 µg/mL
arm shows net growth rather than killing and is excluded from the dose
comparison, leaving 4 to 128 µg/mL as the range compared (Section 7).

### Two kinds of limit, kept apart

No deposit analysed here reports a validated limit of quantification with a
value. The six-laboratory file names the concept in the definitions of its BQL
and AQL columns but defines it as whether the plate was countable, which is an
operator's judgement rather than a validated limit. Throughout this paper *L* is
therefore an **operational assay floor**: where a plated volume is recorded it is
the **minimum reportable positive count**, one colony in that volume, and where
none is recorded it is inferred from the deposit and is labelled as inferred. The
term limit of quantification is used only in reporting what a source states.

Those two names are the precise ones and are used where *L* is defined or its
provenance discussed. In running text *L* is the **assay floor**, and that is the
only short form used, so that "boundary" is left free for the two derived
boundaries of the next subsection and never denotes a value. The event a
time-to-event analysis records is correspondingly a first observed crossing below
the assay floor.
What *L* is in each deposit, how it was arrived at, and how replicate plates and
plated volumes were treated is tabulated deposit by deposit (Table S17).

Two distinct censoring problems arise and are handled separately, because
conflating them is the error this paper is about.

A **count below the assay floor** is left-censored: the population is somewhere
below a known value. In the six-laboratory deposit that value is a property of
the plated volume, as above. In the clinical deposit the readings are most
probable numbers taking the discrete values of an MPN table [[R9]][[R10]], and the day-5 column
bottoms out at 23 per mL with a visible pile-up there; that value is treated as
the floor, and the first Results section reports the evidence for it.

That deposit states no limit of quantification, so the floor is inferred rather
than read off, and the inference is bounded rather than asserted. Three things
support it: 23 per mL is the smallest value anywhere in the file, nothing lies
below it in 1 932 readings, and the minimum shifts by exactly a factor of ten per
visit — 2 300, 230, 23 — in all three culture ages, which is the signature of one
dilution series applied to a differently diluted sample at each timepoint.

The floor is therefore visit-specific, and it does not follow that every visit
has one. A floor is a value readings stop at, so it shows as a pile-up on the
lowest rung with nothing below; the ten-fold shift alone only shows the dilution
changing. Applying the rule of the next subsection visit by visit, the day-5
column has that signature in every panel and the day-2 column has it at 15 days,
but the day-0 column does not: its minimum of 2 300 per mL occurs exactly once in
each panel, with the next value at 6 100, which is the tail of a distribution
rather than a floor. The verdict for day 0 is that no floor is evidenced. The
starting density is therefore an observed value throughout, and no quantity in
this paper that conditions on *N₀* needs a censored specification. Since
none of that is proof, the load-bearing count is recomputed at every value a
three-tube MPN table returns below 23. The number of isolates lacking four logs
of headroom is 33 at a floor of 23 and does not fall below 28 at a floor of 3.0,
the lowest such table returns. The conclusion holds across the whole range, so it
is not an artefact of where we place the floor, and the same sweep is run for
every deposit that carries a floor (Table S18).

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
that never fell below the floor contributes the information that its crossing
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
observability labels are **refused** rather than reported (Table S1). Surviving
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
causal mediation effect through log10 *N₀* and an average direct effect [[R16]][[R17]], with
bootstrap percentile intervals from 5 000 resamples, repeated on the baseline
stratum and on two binary collapses of the outcome.

There is a sharper objection than untestable ignorability, and it has to be met
with a number rather than a concession. For an isolate whose day-5 reading sits
at the floor the recorded fraction is *L*/*N*₀ exactly, so the class is a
function of the starting density and the decomposition recovers arithmetic. That
holds for the eighteen isolates that ended at the floor and for no others: in
the remaining 185 the numerator was measured and can move independently of
*N*₀. Refitting on those 185 alone, the mediated path does not weaken but
strengthens, to +0.227 classes (0.118 to 0.348), while the direct path collapses
to +0.008 (−0.197 to 0.208) and the proportion mediated rises from 0.65 to 0.96.
Removing exactly the isolates for which the criticism is true leaves the effect
larger, so it is not an artefact of them.

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

### What each analysis was fitted to

A dozen different denominators appear in this paper and each is correct for its
own analysis, so every one of them is derived in a single place (Table S2). The
reductions are few and they are named: the MDR tolerance label is a fourth,
unordered category and is dropped wherever an ordered outcome is fitted, taking
14 rows from each panel; six 60-day labels are absent before that, so the 60-day
panel loses 20 in all; the growth proxy is missing for one isolate; and five of the 72 treated flasks
in the six-laboratory deposit carry no usable starting density, which is why a
comparison over 72 flasks is reported on 67. Of the 30 laboratory-by-arm cells,
29 retain enough quantified readings to fit a rate.

The series counts in the six-laboratory deposit differ for the same reason. Each
of the 90 flasks is plated four ways, giving 360 series of which 288 are treated;
the descriptive Cox drops a further 27, 26 for carrying no quantified reading at
day 0 or day 1 in their own plating and one for reading below its floor at day
zero, leaving 261.

Whether these exclusions are plausibly ignorable is tested rather than asserted:
dropped rows are compared with retained rows on starting density and
susceptibility (Table S19). The MDR exclusion differs in susceptibility by
construction. The only difference not by construction is in the 60-day panel,
where the 20 dropped rows sit higher in starting density.

### Dynamic range, and the two boundaries it sets

For a culture starting at *N₀* against an assay floor *L*, two quantities
are used and are kept apart, because they are not interchangeable:

  *H* = *N₀*/*L*, a ratio;
  *h* = log10(*N₀*/*L*), the **headroom**, in log10 units.

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

A **Tobit model** fits log10 CFU/mL linearly in time by maximum likelihood [[R47]]. An
observed reading contributes the usual Gaussian density; a censored reading
contributes log Φ((limit − µ)/σ), the probability that it fell below its own
limit. This is Beal's M3 (Beal 2001) written for this assay [[R46]]. Intervals come from
the profile likelihood.

**Multiple imputation** draws each censored reading from the fitted normal
truncated at its own limit, refits by ordinary least squares, and pools 50 fits
by Rubin's rules [[R48]]. It makes a different assumption from the Tobit model about what
happened below the limit, so agreement between them shows the answer is not
driven by either.

The growth proxy is the deposit's time to an optical density of 0.4, in days;
the deposit records no wavelength, so none is given here. Because it is a time,
it runs inversely to growth rate: a larger value is a slower-growing isolate.

**The tolerance label** is modelled as an ordered categorical outcome by
proportional-odds ordinal logistic regression [[R12]], with starting density as a
prespecified covariate and every association reported unadjusted and adjusted for
it. The MDR category of the deposited label is a fourth, unordered category and
is excluded; all 14 rows carrying it fall outside the susceptible-versus-resistant
contrast in any case, so the ordinal and linear models are fitted to identical
rows. Proportional odds is tested by a Brant test per predictor [[R13]] and by a
likelihood-ratio test against a generalised ordered logit [[R15]] with the coefficient
released; where it fails, the released partial-proportional-odds fit is reported
and checked against a multinomial fit that assumes no ordering. Rows are dropped
only for a missing outcome, predictor or starting density, and the dropped rows
are compared with the retained ones on starting density and susceptibility.
Because the deposit carries no patient identifier, the repeated-isolate structure
is handled by a baseline-only stratum rather than by a random effect, and the
linear models of the earlier analysis are retained as a sensitivity comparison
(Table S20).

**Time-to-event analysis** treats the **first observed crossing below the assay
floor** as the event, with series never falling below their own floor
right-censored at their last visit. The event is named that way throughout and is
not read as clearance, sterilisation or the end of a culture: of the series that
cross, 60 per cent read above the floor again at a later visit.

The crossing time is interval-censored, not observed: it lies between the last
visit above the floor and the first visit below it, and the visit schedule is
coarse. Interval-censored fits [[R29]] are therefore reported alongside the naive
treatment that pins the event to the visit at which the blank plate was noticed.
Kaplan–Meier [[R24]] and Cox proportional hazards [[R25]] are retained as **descriptive**
summaries of first crossing only; their intervals are replaced by cluster
bootstraps over laboratories and over flasks [[R27]], because those 261 series come from
72 flasks in 6 laboratories and the partial likelihood treats them as independent.
No p-value is quoted for a term that is constant within laboratory, since six
clusters cannot support one. Proportionality is tested on Schoenfeld residuals [[R49]][[R50]].

A cell is fitted only when it retains at least six quantified readings at three
distinct times; below that the slope is determined by the censoring pattern
rather than by the counts.

**The replicate-level bootstrap** [[R26]] behind the interval slopes resamples the three
replicate counts with replacement at both ends of each interval, refits the
concentration slope on each draw, and takes percentile intervals from 20 000
draws. The resampling unit is the replicate count, not the interval, so a draw
can repeat a replicate at one end and not the other. An interval on a
proportion — an inversion rate, or a share of flasks — is the Jeffreys
interval [[R30]], which is the equal-tailed posterior under the Jeffreys prior
and does not collapse to zero width when the count is 0 or n, as the normal
approximation does at the sample sizes here.

**What is standard and what is not.** The Tobit fit, Kaplan–Meier, Cox and the
interval-censored fits come from the packages named below. Four procedures do
not: the Brant test of proportional odds, the partial-proportional-odds fit with
a per-cut coefficient mask, the product-of-coefficients mediation with bootstrap
percentile intervals, and the residual-correlation sensitivity for sequential
ignorability. Those are implemented in the released analysis code rather than
taken from a package — in `exp30_ordinal_tolerance.py` and `exp34_mediation.py` —
and the partial-proportional-odds likelihood is validated against the
proportional-odds fit it nests, agreeing to 1.0 × 10⁻¹⁰ in log-likelihood when
nothing is released. The multinomial check uses statsmodels.

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
run, and the family is corrected by the Benjamini–Hochberg procedure [[R14]] at a false
discovery rate of 5 per cent. For each test we report the correlation the sample
size could have resolved at 95 per cent confidence, so that a null is bounded
rather than asserted.

### Reproducibility

Every number in this paper is regenerated by a script that writes a machine-
readable receipt of what it computed, and a separate audit script recomputes 142
of the quantities quoted in the text from the tables they came from and reports
any that disagree. That audit is not exhaustive: it pins the load-bearing counts,
every headline interval and every figure a conclusion rests on, and it does not
pin every cell of every table.

A second audit reads what the first cannot. The value audit parses table bodies
only, so it never sees a table legend, a figure legend, Box 1 or the Abstract —
and it has no way to notice that a number called a hazard ratio in one place is
called a p-value in another, which is a mistake this manuscript made and a
reviewer caught. The second audit checks that every number in those four regions,
conventions such as the endpoint constants and the confidence level aside,
occurs in a results file, a receipt or a table body; that no numeric literal
carries two incompatible statistical labels and that no most-probable number is
printed as a colony count; that percentages, fold-changes, corrected thresholds,
spans and interval bounds follow from their own stated inputs; and that no
conclusion the self-audit marks unsupported is still asserted anywhere, that
every sample size traces to a line in the flow account, that every
cross-reference resolves, and that no block of prose states the same thing
twice, which is what a paragraph looks like when the passage its rewrite
replaced was never deleted. It fails the pipeline
on the findings it grades as contradictions and reports anything weaker without
failing; an untraceable number in a figure legend, in Box 1 or in the Abstract
is weaker, and so is a legend count its own table contradicts where the results
carry that value elsewhere. Every table is
generated from the results files and the manuscript is assembled from that
generated material, never edited downstream of it, so a table cannot drift from
the analysis behind it.

What the second audit does not cover is worth stating, because a guarantee whose
edges are unstated will be read as covering everything. It is an existence check
before it is a semantic one: a number that is correct somewhere in the corpus but
attached to the wrong quantity passes unless some other rule reaches it. Figure
legends, Box 1 and the Abstract have no staleness net comparable to the one that
diffs each spliced table against the block that generated it, so a stale number
there is caught only if it exists nowhere else. An error introduced into a legend
inside the table-generating code is invisible to a check that compares the paper
against that code's own output. And the self-audit table is the premise of the
withdrawn-claim check rather than its subject: the check sees only the
conclusions that table lists, so a reading retracted in the prose alone lies
outside it, and a verdict silently changed from unsupported to supported would
not be detected.

Analyses used Python 3.14 with numpy 2.5.0 [[R41]], scipy 1.18.0 [[R42]],
pandas 3.0.3 [[R43]], statsmodels 0.15.0 [[R44]] and lifelines 0.30.3
[[R45]].

---


## Supplementary tables

**Table S1.** What is actually known about the assay floor in each deposit, and the rule that follows from it. A floor derived from a recorded plated volume is a point mass: one colony in that volume, no inference required. A floor inferred from a pile-up on a most-probable-number rung carries a posterior over the rungs at or below the observed minimum, and the 95 per cent support is quoted. Where no floor is evidenced at all, or where the support spans more than one log10, the observability labels of Section 3 are refused rather than reported -- a label is only as good as the floor it is computed against.

| Deposit | Verdict | Floor used | 95% support | Span (log10) | Refuse observability labels |
| --- | --- | ---: | ---: | ---: | ---: |
| Vijay 2024, clinical isolates (MPN per mL) | INFERRED | 23 | [9.2, 23.0] | 0.398 | no |
| ERA4TB, 100 uL plated (CFU per mL) | DERIVED | 10 | point mass | 0.000 | no |
| ERA4TB, 10 uL plated (CFU per mL) | DERIVED | 100 | point mass | 0.000 | no |
| ERA4TB, 2.5 uL plated (CFU per mL) | DERIVED | 400 | point mass | 0.000 | no |
| Kaur 2024, apramycin grid (log10 CFU per mL) | NONE | - | - | - | yes |
| Windels 2024, evolved clones (surviving fraction) | NONE | - | - | - | yes |
| Dubey 2026, hollow fibre (CFU per mL) | DERIVED | 10 | point mass | 0.000 | no |

**Table S2.** Every analysis set in this paper, and the exclusion that produced it. The manuscript quotes a dozen different denominators, each correct for its own analysis; this is where a reader checks which is which. The MDR tolerance label is a fourth, unordered category and is dropped wherever an ordered outcome is fitted; the growth proxy is missing for one isolate; and five treated flasks in the six-laboratory deposit carry no usable starting density, which is why a comparison over 72 flasks is reported on 67. Whether these exclusions are plausibly ignorable is tested in Table S19. The last rows of each block cover sets counted in units other than isolates or flasks -- pairs, flags, cells, readings -- because a reader meeting one of those figures in the text needs somewhere to look it up too.

| Deposit | Panel | Stratum | Stage | n | Excluded here |
| --- | --- | --- | --- | ---: | ---: |
| Vijay clinical | 15-day | all isolates | rows in the deposit | 217 | - |
| Vijay clinical | 15-day | all isolates | tolerance label present | 217 | - |
| Vijay clinical | 15-day | all isolates | label is Low, Medium or High (drops 'MDR') | 203 | -14 |
| Vijay clinical | 15-day | all isolates | starting and day-5 readings present | 203 | - |
| Vijay clinical | 15-day | all isolates | susceptibility is IS or IR | 203 | - |
| Vijay clinical | 15-day | all isolates | growth proxy present (association family) | 202 | -1 |
| Vijay clinical | 15-day | baseline only (0M) | rows in the deposit | 174 | - |
| Vijay clinical | 15-day | baseline only (0M) | tolerance label present | 174 | - |
| Vijay clinical | 15-day | baseline only (0M) | label is Low, Medium or High (drops 'MDR') | 168 | -6 |
| Vijay clinical | 15-day | baseline only (0M) | starting and day-5 readings present | 168 | - |
| Vijay clinical | 15-day | baseline only (0M) | susceptibility is IS or IR | 168 | - |
| Vijay clinical | 15-day | baseline only (0M) | growth proxy present (association family) | 167 | -1 |
| Vijay clinical | 60-day | all isolates | rows in the deposit | 217 | - |
| Vijay clinical | 60-day | all isolates | tolerance label present | 211 | -6 |
| Vijay clinical | 60-day | all isolates | label is Low, Medium or High (drops 'MDR') | 197 | -14 |
| Vijay clinical | 60-day | all isolates | starting and day-5 readings present | 197 | - |
| Vijay clinical | 60-day | all isolates | susceptibility is IS or IR | 197 | - |
| Vijay clinical | 60-day | all isolates | growth proxy present (association family) | 196 | -1 |
| Vijay clinical | 60-day | baseline only (0M) | rows in the deposit | 174 | - |
| Vijay clinical | 60-day | baseline only (0M) | tolerance label present | 168 | -6 |
| Vijay clinical | 60-day | baseline only (0M) | label is Low, Medium or High (drops 'MDR') | 162 | -6 |
| Vijay clinical | 60-day | baseline only (0M) | starting and day-5 readings present | 162 | - |
| Vijay clinical | 60-day | baseline only (0M) | susceptibility is IS or IR | 162 | - |
| Vijay clinical | 60-day | baseline only (0M) | growth proxy present (association family) | 161 | -1 |
| Vijay clinical | 15-day | other sets quoted | isolates with a starting density | 217 | - |
| Vijay clinical | 60-day | other sets quoted | isolates with a starting density | 210 | -7 |
| Vijay clinical | 15-day | concentration-duration family | all isolates with an inhibitory concentration | 193 | - |
| Vijay clinical | 60-day | concentration-duration family | all isolates with an inhibitory concentration | 187 | - |
| Vijay clinical | 15-day | concentration-duration family | INH-susceptible with one | 119 | - |
| Vijay clinical | 60-day | concentration-duration family | INH-susceptible with one | 117 | - |
| Vijay clinical | 15-day | concentration-duration family | baseline only with one | 162 | - |
| Vijay clinical | 60-day | concentration-duration family | baseline only with one | 156 | - |
| ERA4TB six-laboratory | - | - | readings in the file | 2775 | - |
| ERA4TB six-laboratory | - | - | excluding inoculum controls | 2751 | -24 |
| ERA4TB six-laboratory | - | - | flasks (institute x arm x replicate) | 90 | - |
| ERA4TB six-laboratory | - | - | treated flasks | 72 | -18 |
| ERA4TB six-laboratory | - | - | treated flasks with a usable starting density | 67 | -5 |
| ERA4TB six-laboratory | - | - | laboratory-by-arm cells | 30 | - |
| ERA4TB six-laboratory | - | - | cells with a fitted kill rate | 29 | -1 |
| ERA4TB six-laboratory | - | - | series under the plating key (flasks x 4 platings) | 360 | - |
| ERA4TB six-laboratory | - | - | treated series | 288 | -72 |
| ERA4TB six-laboratory | - | - | cross-laboratory pairs in the same arm | 191 | - |
| ERA4TB six-laboratory | - | derived units | treated series with a quantified day-0 or day-1 reading in their own plating | 262 | -26 |
| ERA4TB six-laboratory | - | derived units | of those, not already below their own floor at day zero (the descriptive Cox set) | 261 | -1 |
| ERA4TB six-laboratory | - | derived units | cross-laboratory pairs, strict rate separation | 94 | - |
| ERA4TB six-laboratory | - | derived units | flasks contributing those pairs | 42 | - |
| ERA4TB six-laboratory | - | derived units | laboratory-by-arm-by-volume cells with a measured start | 56 | - |
| ERA4TB six-laboratory | - | derived units | treated series with three or more quantified readings at 100 uL | 64 | - |
| ERA4TB six-laboratory | - | derived units | flask units in the variance decomposition (all arms plus inoculum) | 85 | - |
| ERA4TB six-laboratory | - | derived units | untreated day-zero readings at 100 uL (4 laboratories x 3 flasks) | 12 | - |
| ERA4TB six-laboratory | - | derived units | below-limit flags in the analysis set | 498 | - |
| ERA4TB six-laboratory | - | derived units | readings in the kill-rate analysis set | 2580 | -171 |
| Dubey hollow fibre (held out) | - | - | cultures with a measured day-zero density | 20 | - |

**Table S3.** The deposited tolerance class at day 5 after 15 days of prior culture is a threshold on the recorded surviving fraction, with no overlap between classes: low below 10⁻³, medium from 10⁻³ to 10⁻² inclusive, high above 10⁻². Applying those cuts reproduces every usable class in the file. This matters because the argument that follows is about the fraction the assay recorded, not about an independent clinical judgement.

| Recorded class | n | Min fraction | Max fraction | Predicted from cuts | Disagreements |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low | 33 | 3.8 × 10⁻⁶ | 4.7 × 10⁻⁴ | Low | 0 |
| Medium | 124 | 1.0 × 10⁻³ | 1.0 × 10⁻² | Medium | 0 |
| High | 46 | 2.7 × 10⁻² | 1.0 × 10¹ | High | 0 |
| All usable | 203 | - | - | - | 0 |

**Table S4.** The family of 8 tests between the deposited tolerance label and its candidate determinants, fitted as proportional-odds ordinal logistic regression and corrected together by the Benjamini-Hochberg procedure at a false discovery rate of 5%; the "survives BH" column is that correction. 2 survive. An odds ratio above one means higher odds of a higher tolerance class; time to an optical density (OD) of 0.4 is in days and runs inversely to growth rate, so above one there means SLOWER growth accompanies a higher class. The proportional-odds column is a Brant test per predictor; the assumption holds for every predictor in this family. Starting density enters the adjusted fits as a covariate rather than as a member of the family, and it is where proportional odds fails, at 60 days at the deepest endpoint; that failure and the released fit are reported in Section 4. The final column repeats each test on the baseline isolates, one per patient by construction, which is where the resistance association stops clearing its corrected threshold. The deposit carries no patient identifier, so no standard error here can be clustered on the true grouping and every interval in this table is model-based; the baseline-isolate column is the sensitivity analysis that stands in for clustering, and Table S11 records what each conclusion is worth once it is applied.

| Predictor | Prior culture | Reading day | For starting density | n | Odds ratio (95% CI) | p | Survives BH | Prop. odds p | Baseline isolates only |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| time to OD 0.4 | 15 d | day 5 | adjusted | 202 | 1.096 (1.03-1.16) | 0.0030 | yes | 0.152 | 1.12 (p=0.002, survives) |
| resistance | 15 d | day 5 | unadjusted | 202 | 2.317 (1.30-4.12) | 0.0042 | yes | 0.417 | 2.11 (p=0.031, no) |
| time to OD 0.4 | 60 d | day 2 | adjusted | 196 | 0.933 (0.87-1.00) | 0.0470 | no | 0.688 | 0.92 (p=0.032, no) |
| time to OD 0.4 | 15 d | day 2 | adjusted | 202 | 1.068 (1.00-1.14) | 0.0618 | no | 0.243 | 1.07 (p=0.108, no) |
| resistance | 15 d | day 2 | unadjusted | 202 | 1.295 (0.66-2.54) | 0.4529 | no | 0.479 | 1.07 (p=0.876, no) |
| time to OD 0.4 | 60 d | day 5 | adjusted | 196 | 0.976 (0.91-1.04) | 0.4605 | no | 0.875 | 0.99 (p=0.703, no) |
| resistance | 60 d | day 2 | unadjusted | 196 | 0.836 (0.47-1.48) | 0.5400 | no | 0.075 | 1.11 (p=0.774, no) |
| resistance | 60 d | day 5 | unadjusted | 196 | 1.111 (0.63-1.95) | 0.7150 | no | 0.067 | 1.61 (p=0.186, no) |

**Table S5.** Decomposition of the isoniazid-resistance association with the tolerance class into a path through log10 starting density and a direct path, by the product of coefficients with bootstrap percentile intervals. The mediated path excludes zero in every specification and the direct path covers zero in every one. This replaces the percentage attenuation the earlier analysis quoted, which is a descriptive ratio rather than an estimand. Sequential ignorability is assumed and is not testable here; the sensitivity analysis in the Methods reports the residual correlation that would nullify the estimate.

| Outcome and stratum | n | Total effect c (95% CI) | Direct effect c' (95% CI) | Mediated effect (95% CI) | Proportion mediated |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linear 0/1/2, all IS/IR | 203 | +0.256 (+0.087, +0.425) | +0.091 (-0.116, +0.287) | +0.166 (+0.067, +0.279) | 65% |
| Linear 0/1/2, baseline isolates | 168 | +0.226 (+0.038, +0.409) | +0.067 (-0.157, +0.294) | +0.159 (+0.053, +0.295) | 70% |
| High versus rest | 203 | +0.121 | +0.013 | +0.108 (+0.037, +0.189) | 89% |
| Not-low versus low | 203 | +0.135 | +0.077 | +0.058 (+0.003, +0.121) | 43% |

**Table S6.** Isoniazid-resistant isolates enter this assay ten-fold lower than susceptible ones, and we do not know why. This is what the deposit can and cannot rule out. The verdict column is decided on the two recorded-rate columns beside it: PROXY means the covariate is recorded for no isolate in one of the two exposure groups, so its missingness is the exposure; PARTIAL means both groups record it but the missingness is still tied to the exposure (Fisher exact p < 10⁻⁶); INDEPENDENT means it is not. Seven of the nine covariates are therefore unusable, and they fail in two ways. Five are recorded almost exclusively for resistant isolates: the two susceptibility calls, the two Mykrobe calls and the mutation identity. The susceptibility calls are missing on identical rows, which is why they return identical coefficients, and the Mykrobe calls carry a single value wherever they are recorded in this stratum, so no model can be fitted for them and no coefficient is printed. The other two are the drug MICs, recorded for every susceptible isolate and 67 of 84 resistant ones; the isoniazid MIC separates the two groups completely, so adjusting for it conditions on a graded reading of the exposure. A negative attenuation is an amplification: the adjusted coefficient sits further from zero than the unadjusted one, which is what the isoniazid MIC does at 13 per cent. A coefficient is printed wherever one exists so the circularity is visible, but none of these seven bounds anything. Only 2 covariates are recorded at rates unrelated to susceptibility, and adjusting for either leaves the coefficient within five per cent of its unadjusted value. The file records no referring site and no processing batch, so those cannot be tested at all.

| Covariate | Recorded, resistant | Recorded, susceptible | Can it adjust? | Resistance coefficient | Attenuation |
| --- | ---: | ---: | ---: | ---: | ---: |
| INH_MGIT_DST | 82/84 | 0/119 | PROXY | -0.851 | -0% |
| RIF_MGIT_DST | 82/84 | 0/119 | PROXY | -0.851 | -0% |
| INH_mutation | 79/84 | 1/119 | PARTIAL | -0.662 | 22% |
| INH_Mykrobe | 76/84 | 0/119 | PROXY | - | - |
| RIF_Mykrobe | 76/84 | 0/119 | PROXY | - | - |
| MIC_INH | 67/84 | 119/119 | PARTIAL | -0.963 | -13% |
| MIC_RIF | 67/84 | 119/119 | PARTIAL | -0.853 | -0% |
| Time_to_0.4 | 83/84 | 119/119 | INDEPENDENT | -0.807 | 5% |
| Time_point | 84/84 | 119/119 | INDEPENDENT | -0.818 | 4% |

**Table S7.** Moxifloxacin at ten times MIC. Every laboratory yields a rate; three record no crossing below the assay floor in any arm at the 100 uL plating. The final column counts first observed crossings, which are not clearances: across the deposit 60% of the series that cross read above the floor again at a later visit. The two censoring estimators agree to 0.003 log10 per day. The starting density is the mean of quantified readings at day 0 or day 1 at the 100 uL plating, pooled over all of that laboratory's arms; the reading-day column says which visits contributed. Institute A deposits no day-zero reading at all, and among treated flasks only institutes C and D do, so for the rest this figure rests partly on readings taken after 24 hours of drug. Text S1 and Table S12 instead use untreated day-zero readings only, so the two tables are not expected to match.

| Lab | Starting density (log10 CFU/mL) | Reading day | Kill rate (log10/day) | 95% profile interval | By imputation | Readings censored | Flasks ever crossing the floor (treated arms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 2.95 | day 1 | 0.119 | 0.092 to 0.155 | 0.119 | 51% | 9 / 12 |
| B | 3.16 | day 0, day 1 | 0.139 | 0.097 to 0.191 | 0.138 | 58% | 10 / 12 |
| C | 4.02 | day 0, day 1 | 0.464 | 0.430 to 0.499 | 0.464 | 44% | 10 / 12 |
| D | 4.69 | day 0, day 1 | 0.104 | 0.081 to 0.128 | 0.105 | 3% | 0 / 12 |
| E | 4.95 | day 0, day 1 | 0.090 | 0.077 to 0.104 | 0.090 | 1% | 0 / 12 |
| F | 6.53 | day 0, day 1 | 0.223 | 0.206 to 0.240 | 0.223 | 0% | 0 / 12 |

**Table S8.** What follows a first observed crossing below the assay floor. The state below the floor is not absorbing: a series sitting below it reads above again at the next visit with probability 0.22 overall, and that probability rises as drug pressure falls, which is what a plating artefact does. Only 56 of 360 series, 15.6 per cent, show the shape a survival model assumes -- one crossing that holds. The 360 series are four platings of each of 90 flasks and are not independent; the flask-level counts are 53 flasks with a crossing series and 42 with a returning one.

| Series | n | Visit pairs | P(above to below) | P(below to above) | Never below | One crossing, holds | One crossing, returns | Crosses repeatedly | Shape the model assumes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all series | 360 | 2232 | 0.080 | 0.222 | 220 | 56 | 65 | 19 | 16% |
| INH 10X MIC | 72 | 441 | 0.137 | 0.065 | 34 | 27 | 6 | 5 | 38% |
| INH 1X MIC | 72 | 440 | 0.150 | 0.373 | 30 | 2 | 33 | 7 | 3% |
| MXF 10X MIC | 72 | 433 | 0.141 | 0.175 | 30 | 26 | 9 | 7 | 36% |
| MXF 1X MIC | 72 | 441 | 0.023 | 0.923 | 59 | 1 | 12 | 0 | 1% |
| untreated | 72 | 477 | 0.011 | 1.000 | 67 | 0 | 5 | 0 | 0% |

**Table S9.** Dubey et al. 2026, analysed cold. The floor is derived from a stated 100 uL plated volume and corroborated inside the file: all 229 genuine counts are multiples of ten and the smallest is exactly ten. Starting densities are the 20 measured day-zero counts, not the nominal inoculum the Methods state.

| Endpoint | N_reach (per mL) | Cultures | Unreachable | Per cent |
| --- | ---: | ---: | ---: | ---: |
| 1 log (90%) | 100 | 20 | 0 | 0% |
| 2 log (99%) | 1,000 | 20 | 0 | 0% |
| 3 log (99.9%) | 10,000 | 20 | 0 | 0% |
| 4 log (99.99%) | 100,000 | 20 | 0 | 0% |
| 5 log (99.999%) | 1,000,000 | 20 | 5 | 25% |
| 6 log (99.9999%) | 10,000,000 | 20 | 20 | 100% |

**Table S10.** The same 32-fold concentration range summarised at each sampling day (upper rows), and the concentration slope fitted separately in each interval (lower rows). Slopes and intervals are from the replicate-level bootstrap described in the Methods.

| Read at | Survivor ratio (low/high dose) | log10 separation | Slope per doubling | 95% interval | p |
| --- | ---: | ---: | ---: | ---: | ---: |
| day 3 | 6.9x | 0.84 |  |  |  |
| day 7 | 48.2x | 1.68 |  |  |  |
| day 14 | 5.2x | 0.71 |  |  |  |
| days 0-3 |  |  | +0.0590 | +0.0302 to +0.0878 | 0.013 |
| days 3-7 |  |  | +0.0330 | -0.0517 to +0.1176 | 0.236 |
| days 7-14 |  |  | -0.0251 | -0.0602 to +0.0099 | 0.091 |

**Table S11.** Every conclusion this paper draws from the two primary deposits, against uncertainty recomputed at the level the observations are actually independent. 20 survive unchanged, 6 survive with materially wider uncertainty, 5 do not survive, and 1 is withdrawn because its null is false before any data are seen. Each verdict applies to the claim as it was originally stated. Three of the five failures are gone from the text entirely; for the other two a weaker statement is retained and is marked as such where it appears -- the Cox coefficient trade is now reported as hazard ratios with no p-value, and institute C as the laboratory whose crossings its starting density does not account for rather than as a tested contrast. The five that fail are all between-laboratory p-values computed on flasks: every flask in a laboratory shares a starting culture, so a comparison that looks like 67 flasks is six laboratories, and for a three-against-three split of six clusters the smallest attainable two-sided p is 0.10. They are deleted rather than corrected, because there is nothing to correct them to.

| Section | Conclusion as originally stated | Units treated as independent | Independent clusters | Method used instead | Verdict |
| --- | --- | --- | ---: | ---: | ---: |
| 4 | the difference between panels in the growth association is itself supported (interaction p = 0.0072) | unknown isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | not recomputable | NOT SUPPORTED |
| 5 | starting density separates flasks that ever crossed below the assay floor from those that never did (AUC 0.974, p = 1.2e-10) | 67 flask | 6 | exact laboratory-level test (3 crossed vs 3 did not); cluster bootstrap over laboratories; permutation of crossing within laboratory, and within laboratory AND treatment arm | NOT SUPPORTED |
| 5 | in a Cox model, institutes D, E and F carry p = 0.015, 0.016, 0.015, which adjustment for starting density moves to 0.138, 0.172, 0.576 | 67 flask | 6 | cluster-robust sandwich on six clusters | NOT SUPPORTED |
| 5 | the log-rank test separates the six laboratories on time to first crossing | 67 flask | 6 | none available: the grouping variable is the cluster | NOT SUPPORTED |
| 5 | institute C remains distinguishable after adjustment (HR 5.27, p < 0.001) | 67 flask | 1 | none available | NOT SUPPORTED |
| 1 | all 33 short isolates are at the ceiling; 88.0% of the rest are (Fisher p = 0.030) | 217 isolate | 174 patients min | none: the null is arithmetically impossible | WITHDRAWN |
| 5 | at ten times MIC of moxifloxacin the kill rate spans 5.2-fold between laboratories (0.090 to 0.464) | 6 laboratory-arm cell | 6 | cluster bootstrap over whole laboratories | WEAKENED |
| 5 | at one times MIC five of six laboratories record net growth | 6 laboratory-arm cell | 6 | Jeffreys interval on six clusters | WEAKENED |
| 5 / 7 | the laboratory effect lands on the duration endpoint and not on the rate; the rate is 'far more reproducible' | 42 flask | 6 | permutation of the laboratory label across flasks, within arm for the rate | WEAKENED |
| 6 | the deepest demonstrable kill differs by 2.33 log10 between laboratories at one plating volume | 12 day-zero reading | 4 | cluster bootstrap over whole laboratories | WEAKENED |
| 7 | 36.6% of 191 cross-laboratory pairs are inversions (95% CI 30.1-43.6) | 191 pair of flasks | 6 | cluster bootstrap over whole laboratories; also over flasks within laboratory; also delete-one-laboratory jackknife | WEAKENED |
| 7 | under the strictest rate separation the inversion rate is 21.3% of 94 pairs (95% CI 13.9-30.3) | 94 pair of flasks | 6 | cluster bootstrap over whole laboratories | WEAKENED |
| 1 | 33 of 217 isolates (15.2%) lack the headroom for a 4-log endpoint | 217 isolate | 174 patients min | baseline-only recount | SUPPORTED |
| 1 / 2 | 18 isolates rest on the floor at 15 days and 6 at 60 | 217 + 210 isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | exact McNemar on the paired binary | SUPPORTED |
| 10 | no MIC-MDK association survives Benjamini-Hochberg | 6 tests isolate | 174 patients min | baseline-only family of six | SUPPORTED |
| 2 | 18 isolates at the floor; their survival span IS their inoculum span | 217 isolate | 174 patients min | baseline-only recount | SUPPORTED |
| 2 | 185 determinable, 12 forced by the inoculum, 6 undecidable | 203 isolate | 174 patients min | baseline-only reclassification | SUPPORTED |
| 2 | at 60 days the observability counts are 191, 6 and none, 'because the cultures are denser and few readings reach the floor' | 203 + 197 isolate-panel (each of 210 isolates counted once per panel) | 197 isolates | exact McNemar on the paired binary | SUPPORTED |
| 2 / 4 | the deep endpoint is unreachable for 26.2% of resistant against 7.6% of susceptible isolates | 217 isolate | 174 patients min | baseline-only Fisher exact | SUPPORTED |
| 4 | resistant isolates enter the assay ten-fold lower | 217 isolate | 174 patients min | baseline-only Mann-Whitney | SUPPORTED |
| 4 | the resistance-tolerance association attenuates once starting density enters the model, and its interval then spans zero | 202 isolate | 174 patients min | baseline-only refit | SUPPORTED |
| 4 | growth state predicts the tolerance class and survives adjustment (beta = +0.027, p = 0.0025) | 202 isolate | 174 patients min | baseline-only refit | SUPPORTED |
| 4 | resistant isolates do not grow measurably more slowly (p = 0.24) | 217 isolate | 174 patients min | baseline-only Mann-Whitney | SUPPORTED |
| 4 | the confound thins between panels: 15.2% short of headroom at 15 days against 3.3% at 60 | 217 + 210 isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | exact McNemar on the paired binary | SUPPORTED |
| 4 | the 60-day cultures are denser, so headroom is larger there | 420 treated as independent isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | Wilcoxon signed-rank on the within-isolate change | SUPPORTED |
| 4 | the spread of starting densities more than halves between panels (IQR 1.00 to 0.42 log10) | 420 isolate-panel (each of 210 isolates counted once per panel) | 210 isolates | paired bootstrap resampling whole isolates | SUPPORTED |
| 5 | of 64 treated series the final step is not a decline in 48 (75%) | 64 series (one per treated flask) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| 5 | 44 of 64 series end more than one log10 above their own nadir | 64 series (one per treated flask) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| 5 / Limitations | 87.0% of the variance in flask starting density lies between laboratories | 85 flask | 6 | permutation of the laboratory label across flasks | SUPPORTED |
| 6 | including the choice of plated volume widens the spread in measurable depth to 4.40 log10 | up to 4 volumes x 5 laboratories laboratory-by-volume channel | 6 | no resampling required for the volume term | SUPPORTED |
| 7 | the criterion D_A/D_B > b_A/b_B calls 83.8% of pairs correctly | 191 pair of flasks | 6 | cluster bootstrap over whole laboratories | SUPPORTED |
| Methods | 83 of 498 below-limit flags (16.7%) are contradicted by another plating of the same sample at the same visit | 498 flag (one reading) | 6 | cluster bootstrap over whole laboratories | SUPPORTED |

**Table S12.** The deepest reduction each assay could resolve, as h = log10(N0/L), with the assay floor taken per sample where it varies. Rows compare only within a level of variation: the clinical rows describe between-isolate starting burden, which is biological, and are not a measure of laboratory imprecision. Kaur is NA because its three day-zero readings are technical replicates of one preparation and cannot estimate between-preparation reproducibility, and because that deposit states no quantification limit.

| Dataset | Level of variation | n | Median log10 N0 | Assay floor L | delta h (log10) | Fold |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| ERA4TB, between laboratories at 100 uL | between laboratories, one written protocol | 12 | 4.63 | 10 CFU/mL, derived from 100 uL plated | 2.33 | 216x |
| ERA4TB, every laboratory and plating volume | laboratories and plated volumes together | 56 | 4.29 | 10, 100 or 400 CFU/mL by volume | 4.40 | 25,123x |
| Vijay, 15-day culture | between clinical isolates | 217 | 5.79 | 23 MPN/mL, inferred | 4.42 | 26,522x |
| Vijay, 60-day culture | between clinical isolates | 210 | 7.36 | 23 MPN/mL, inferred | 5.43 | 269,565x |
| Kaur, planktonic | technical replicates of one preparation | 3 | 7.03 | not stated in the deposit | NA | NA |
| Kaur, intracellular | technical replicates of one preparation | 3 | 5.94 | not stated in the deposit | NA | NA |
| Dubey, hollow fibre | between cultures, one laboratory | 20 | 6.08 | 10 CFU/mL, derived from 100 uL plated | 0.60 | 4x |

**Table S13.** Fold below the nominal 0.5 McFarland reference, 1.5e8 CFU/mL. Descriptive only, and not a protocol-compliance metric. A time-kill inoculum is prepared by diluting from a suspension matched to that turbidity, so every entry is expected to sit far below it; the conversion of a turbidity to CFU/mL depends on species, cell aggregation and preparation and is least reliable for mycobacteria. The clinical rows are most probable numbers divided by a reference stated in CFU/mL, so those two ratios cross units and are the least meaningful in the table.

| Dataset | Median log10 N0 | Fold below nominal 0.5 McFarland |
| --- | ---: | ---: |
| ERA4TB, between laboratories at 100 uL | 4.63 | 3,525x |
| ERA4TB, every laboratory and plating volume | 4.29 | 7,751x |
| Vijay, 15-day culture | 5.79 | 246x |
| Vijay, 60-day culture | 7.36 | 7x |
| Kaur, planktonic | 7.03 | 14x |
| Kaur, intracellular | 5.94 | 170x |
| Dubey, hollow fibre | 6.08 | 123x |

**Table S14.** Pairs of flasks in the same arm from different laboratories. An inversion is a pair in which the population that fell faster crossed below the assay floor later. 45 further pairs that the censoring could not settle are excluded rather than imputed. The last two columns decompose the spread in crossing time; the rate term is the larger in each of the three arms that can be decomposed. Moxifloxacin at one times MIC is not among them: the decomposition is taken on log *D* and log *b*, five of six laboratories record net growth in that arm, and only one flask in it returns a positive fitted rate, so there is no spread in the rate to divide.

| Arm | Comparable pairs | Inversions | Rate | 95% CI | Called by D/b criterion | Variance: distance | Variance: rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All arms pooled | 191 | 70 | 36.6% | 30.1-43.6% | 83.8% |  |  |
| INH 10X MIC |  |  |  |  |  | 31.4% | 68.6% |
| INH 1X MIC |  |  |  |  |  | 19.6% | 80.4% |
| MXF 10X MIC |  |  |  |  |  | 39.4% | 60.6% |

**Table S15.** The six strongest of the 24 comparisons the 217-isolate file supports. 4 reach nominal significance where 1.2 are expected by chance; none exceeds its Benjamini-Hochberg critical value, which is ranked against the full family of 24 rather than against any one stratum. MDK99 and MDK99.99 are the minimum durations for a 99 and a 99.99 per cent reduction, the endpoints the text names in words. The final column is the correlation each design could have resolved at 95% confidence.

| Stratum | Endpoint | n | Spearman rho | p | BH critical value | Survives correction | Resolvable rho |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline only | MDK99.99 (15d) | 162 | -0.206 | 0.0086 | 0.0021 | no | 0.15 |
| INH-susceptible | MDK99.99 (15d) | 119 | -0.218 | 0.0171 | 0.0042 | no | 0.18 |
| INH-susceptible | MDK99 (60d) | 117 | -0.198 | 0.0324 | 0.0063 | no | 0.18 |
| all isolates | MDK99.99 (60d) | 187 | -0.153 | 0.0361 | 0.0083 | no | 0.14 |
| INH-susceptible | MDK99.99 (60d) | 117 | -0.179 | 0.0540 | 0.0104 | no | 0.18 |
| baseline only | MDK99.99 (60d) | 156 | -0.149 | 0.0628 | 0.0125 | no | 0.16 |

**Table S16.** The same nominal concentration expressed in multiples of the minimum inhibitory concentration each population actually evolved to. At 25 ug/mL the same number denotes a sub-inhibitory exposure in one nutrient condition and a strongly inhibitory one in another.

| Nominal concentration (ug/mL) | Nutrient levels | Lowest exposure (x MIC) | Highest exposure (x MIC) | Spread | Straddles the MIC |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12.5 | 3 | 1.49 | 4.74 | 3.2x | no |
| 25 | 3 | 0.55 | 9.47 | 17.1x | yes |
| 50 | 2 | 5.08 | 10.95 | 2.2x | no |
| 100 | 1 | 9.72 | 9.72 | 1.0x | no |

**Table S17.** What the assay floor *L* is in each deposit analysed. No deposit reports a validated limit of quantification with a value. The six-laboratory file names the concept in the definitions of its below- and above-quantification-limit columns but defines it as whether the plate was countable, which is an operator's judgement. DERIVED means the value follows arithmetically from a recorded plated volume; INFERRED means it was read off the deposit's own behaviour and is labelled as inferred wherever it is used; NONE means no floor is evidenced and none is assumed; FLAGGED means the deposit marks below-limit readings without naming a value, which fixes no floor either. Where a plated volume is recorded the honest term is the minimum reportable positive count, one colony in that volume; elsewhere it is an operational assay floor.

| Deposit | States an LOD | States an LOQ | Value used | Units | How obtained | What it should be called |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Vijay 2024 | no | no | 23 | MPN per mL | INFERRED | operational assay floor |
| ERA4TB 2023 | no | term only | 10, 100 and 400, per plated volume | CFU per mL | DERIVED | minimum reportable positive count |
| Windels 2024 | no | no | none; no value is recoverable | surviving fraction, dimensionless | FLAGGED | no floor is established; a below-limit reading is written as exact zero and fixes no value |
| Kaur 2024 | no | no | none; no floor is used | log10 CFU per mL | NONE | no floor is evidenced; the smallest reading is the smallest reading |
| Dubey 2026 | no | no | 10 | CFU per mL | DERIVED | minimum reportable positive count |

---

## Supplementary tables

Held here so the Results stay on one line of reasoning. Table S16 supports Text S3 and Table S13 supports Text S1.

**Table S18.** Sensitivity of the load-bearing counts to the choice of floor. Each deposit is sensitive to a different thing, so the table is long rather than wide: one row per deposit, floor scenario and quantity. The clinical sweep steps through every three-tube most-probable-number rung at or below 23 per mL, and the number of isolates short of four logs of headroom moves only between 28 and 33 across the whole range, which is why the inferred floor is safe to use. The six-laboratory rows price what pooling the four plating volumes to one floor would cost. The Kaur deposit records no plated volume, so its rows show what assuming one would do: the four-log endpoint stays reachable throughout while the headroom itself moves by 1.6 log10.

| Deposit | Floor assumed | Quantity | Value |
| --- | --- | --- | ---: |
| Vijay 2024 | floor = 3 MPN/mL | isolates short of 4 logs | 28 |
| Vijay 2024 | floor = 3 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 3 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 3 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 3 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 3 MPN/mL | short of 4 logs, baseline only | 17 |
| Vijay 2024 | floor = 3.6 MPN/mL | isolates short of 4 logs | 28 |
| Vijay 2024 | floor = 3.6 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 3.6 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 3.6 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 3.6 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 3.6 MPN/mL | short of 4 logs, baseline only | 17 |
| Vijay 2024 | floor = 7.2 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 7.2 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 7.2 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 7.2 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 7.2 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 7.2 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 7.4 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 7.4 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 7.4 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 7.4 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 7.4 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 7.4 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 9.2 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 9.2 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 9.2 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 9.2 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 9.2 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 9.2 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 11 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 11 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 11 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 11 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 11 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 11 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 14 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 14 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 14 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 14 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 14 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 14 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 15 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 15 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 15 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 15 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 15 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 15 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 20 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 20 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 20 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 20 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 20 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 20 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 21 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 21 MPN/mL | isolates at the floor | 0 |
| Vijay 2024 | floor = 21 MPN/mL | calls resting on a measured fraction | 203 |
| Vijay 2024 | floor = 21 MPN/mL | calls with one compatible class | 0 |
| Vijay 2024 | floor = 21 MPN/mL | calls with several compatible classes | 0 |
| Vijay 2024 | floor = 21 MPN/mL | short of 4 logs, baseline only | 21 |
| Vijay 2024 | floor = 23 MPN/mL | isolates short of 4 logs | 33 |
| Vijay 2024 | floor = 23 MPN/mL | isolates at the floor | 18 |
| Vijay 2024 | floor = 23 MPN/mL | calls resting on a measured fraction | 185 |
| Vijay 2024 | floor = 23 MPN/mL | calls with one compatible class | 12 |
| Vijay 2024 | floor = 23 MPN/mL | calls with several compatible classes | 6 |
| Vijay 2024 | floor = 23 MPN/mL | short of 4 logs, baseline only | 21 |
| ERA4TB | per-volume (as analysed) | genuine counts a pooled floor discards (%) | 0 |
| ERA4TB | per-volume (as analysed) | below-limit flags contradicted (%) | 16.67 |
| ERA4TB | pooled at the most sensitive volume, 100 uL | genuine counts a pooled floor discards (%) | 0 |
| ERA4TB | pooled at the most sensitive volume, 100 uL | below-limit flags contradicted (%) | 43.17 |
| ERA4TB | pooled at the modal volume, 10 uL | genuine counts a pooled floor discards (%) | 1.13 |
| ERA4TB | pooled at the modal volume, 10 uL | below-limit flags contradicted (%) | 28.71 |
| ERA4TB | pooled at the least sensitive volume, 2.5 uL | genuine counts a pooled floor discards (%) | 5.94 |
| ERA4TB | pooled at the least sensitive volume, 2.5 uL | below-limit flags contradicted (%) | 15.26 |
| ERA4TB | pooled at the geometric mean of the per-volume floors | genuine counts a pooled floor discards (%) | 1.04 |
| ERA4TB | pooled at the geometric mean of the per-volume floors | below-limit flags contradicted (%) | 38.96 |
| Dubey 2026 | the below-limit placeholder taken literally | median headroom (log10) | 6.08 |
| Dubey 2026 | the below-limit placeholder taken literally | cultures short of 4 logs | 0 |
| Dubey 2026 | 100 uL plated, as the deposit's staging record gives | median headroom (log10) | 5.08 |
| Dubey 2026 | 100 uL plated, as the deposit's staging record gives | cultures short of 4 logs | 0 |
| Dubey 2026 | 50 uL plated | median headroom (log10) | 4.78 |
| Dubey 2026 | 50 uL plated | cultures short of 4 logs | 0 |
| Dubey 2026 | 10 uL plated | median headroom (log10) | 4.08 |
| Dubey 2026 | 10 uL plated | cultures short of 4 logs | 5 |
| Kaur 2024 | 100 uL plated, if it had been stated | headroom (log10) | 6.03 |
| Kaur 2024 | 100 uL plated, if it had been stated | 4-log endpoint reachable | True |
| Kaur 2024 | the observed minimum, which occurs once | headroom (log10) | 5.43 |
| Kaur 2024 | the observed minimum, which occurs once | 4-log endpoint reachable | True |
| Kaur 2024 | 10 uL plated, if it had been stated | headroom (log10) | 5.03 |
| Kaur 2024 | 10 uL plated, if it had been stated | 4-log endpoint reachable | True |
| Kaur 2024 | 2.5 uL plated, if it had been stated | headroom (log10) | 4.43 |
| Kaur 2024 | 2.5 uL plated, if it had been stated | 4-log endpoint reachable | True |
| Windels 2024 | no floor is recoverable | readings written as exact zero | 6 |

**Table S19.** The comparison the Methods promise: rows dropped from the association family against rows retained, on starting density and susceptibility. The MDR exclusion differs in susceptibility by construction, since those isolates are outside the resistant-versus-susceptible contrast the family tests. The one difference not by construction is in the 60-day panel, where the dropped rows sit higher in starting density (p = 0.027); it affects 20 rows and no conclusion drawn from that panel.

| Panel | Exclusion | Dropped | Retained | Median log10 N0 retained | Median log10 N0 dropped | p | Resistant, retained | Resistant, dropped | p  |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 15-day | label missing or 'MDR' | 14 | 202 | 5.79 | 5.36 | 0.198 | 41% | 0% | 0.001 |
| 15-day | growth proxy missing | 1 | 202 | 5.79 | 6.79 | 0.149 | 41% | 100% | 0.414 |
| 60-day | label missing or 'MDR' | 20 | 196 | 7.36 | 7.79 | 0.027 | 40% | 20% | 0.093 |
| 60-day | growth proxy missing | 1 | 196 | 7.36 | 7.36 | 0.749 | 40% | 100% | 0.406 |

**Table S20.** The ordinal reanalysis against the linear model it replaces, member for member. The linear model scores the ordering 0, 1, 2, which assumes the two class steps are equal; the ordinal model does not. Every direction agrees and the same two members survive correction under both, so the linear treatment did not manufacture the result -- but the coefficients it reports are in a unit that does not exist, which is why the ordinal fit is the one in the main table.

| Predictor | Prior culture | Reading day | Linear beta | p (linear) | Survives BH | Odds ratio | p (ordinal) | Survives BH  | Same direction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| time to OD 0.4 | 15 d | day 5 | +0.0266 | 0.0025 | yes | 1.096 | 0.0030 | yes | yes |
| resistance | 15 d | day 5 | +0.2589 | 0.0035 | yes | 2.317 | 0.0042 | yes | yes |
| time to OD 0.4 | 60 d | day 2 | -0.0195 | 0.0590 | no | 0.933 | 0.0470 | no | yes |
| time to OD 0.4 | 15 d | day 2 | +0.0116 | 0.0812 | no | 1.068 | 0.0618 | no | yes |
| resistance | 15 d | day 2 | +0.0515 | 0.4446 | no | 1.295 | 0.4529 | no | yes |
| time to OD 0.4 | 60 d | day 5 | -0.0041 | 0.6999 | no | 0.976 | 0.4605 | no | yes |
| resistance | 60 d | day 2 | -0.0551 | 0.5486 | no | 0.836 | 0.5400 | no | yes |
| resistance | 60 d | day 5 | +0.0389 | 0.6797 | no | 1.111 | 0.7150 | no | yes |
