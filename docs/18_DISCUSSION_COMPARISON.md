# Discussion: what others did, what we did, and why ours holds

Our results are locked. This file is the comparison table the Discussion is
written from. Sections 0 to 0c were added when the paper's spine moved from the
divergence of two summaries to the failure of the log-reduction metric; sections
1 to 7 predate that move and still stand, with section 1 now supporting Section
3.4 rather than the whole argument. Every row follows one shape: **what they did, what we did, what
differs, and why our choice is defensible.** Nothing here restates a prior
finding as ours, and every citation below was verified against the live record
rather than recalled.

The rule applied throughout: where a prior study reached a different answer, the
difference is traced to a specific methodological choice, and that choice is
named. Disagreement without a named cause is not a defence.

---

## 0. The rule this paper does not claim to have discovered

**Clinical microbiology, uncited because it is universal.** A culture taken after
antibiotics have started is not evidence of sterility. It is why blood cultures
are drawn before the first dose, and it is taught to every trainee.

**What we do.** We concede it in the first sentence of the Introduction rather
than rediscovering it in the Results. The paper is not about negative cultures.

**What differs.** Nothing. This is the premise, and stating it as ours would be
the fastest way to lose a referee.

**Why this matters to the framing.** An earlier draft of this paper argued that a
clearance time depends on the starting inoculum and a kill rate does not. That is
the old rule with survival analysis on top. The current paper begins where that
draft ended: given that everyone knows a threshold crossing is unreliable, what
did the field build to replace it, and does the replacement work?

---

## 0b. MDK as the engineered answer, and where it fails

**Brauner A, Fridman O, Gefen O, Balaban NQ.** *Nat Rev Microbiol*
2016;14(5):320-30. doi:10.1038/nrmicro.2016.34. And **Brauner A, Shoresh N,
Fridman O, Balaban NQ.** *Biophys J* 2017;112(12):2664-71.
doi:10.1016/j.bpj.2017.05.014.

**What they did.** Defined the minimum duration for killing as the tolerance
counterpart to the MIC: the time to a specified fractional reduction, 90, 99 or
99.99 per cent. The fraction is the design decision. A ratio to the starting
population is scale-free, so on a log-linear decline the starting density cancels
and the metric cannot be contaminated by how much culture went into the tube.
They also warn, in the 2016 paper, that poor quantification of tolerance "may
lead to the misclassification of tolerant strains".

**What we do.** Accept the design entirely and test whether the property it was
built to have survives the measurement. It does not, for a reason that is
arithmetic rather than statistical: a q-log reduction is observable only where q
logs of dynamic range exist above the assay floor, and when the final reading
rests on the floor the recorded fraction reduces to L/N0 - the most
inoculum-dependent quantity available.

**What differs.** They analyse the estimand; we analyse the observability of the
estimand. These are not in conflict. MDK is scale-free where the assay can
resolve it and is a reading of the starting density where it cannot.

**Why ours is acceptable.** The failure is bounded and specific, which is what
makes it a fixable defect rather than an attack on the framework. In the deposit
examined, no isolate lacks the range for the 90 or the 99 per cent endpoint:
0 of 217 in both cases. It is the 99.99 per cent endpoint - the deepest, and the
one the clinical classification uses - that 33 of 217 could not have reached
under any drug effect. Alexandersen et al. 2025, working at MDK99, report no
highly tolerant isolates, which is consistent with a shallow endpoint being safe.
We are extending their framework at its deep end, not disputing it.

---

## 0c. The deposit that made this testable

**Vijay S, Bao NLH, Vinh DN, Nhat LTH, Thu DDA, Quang NL, et al.** *eLife*
2024;12:RP93243. doi:10.7554/eLife.93243. Open access, CC BY 4.0.

**What they did.** Assayed 217 clinical *M. tuberculosis* isolates under
rifampicin, scored each as low, medium or high tolerance, and reported
associations between tolerance, resistance status and treatment history. Crucially
for us, they deposited the classification, the MPN readings it was computed from,
the starting densities, a growth-rate proxy and the resistance genotype in one
file.

**What we do.** Use their own classification as the object of study. We show the
labels are a clean threshold on the recorded surviving fraction with no class
overlap; that 18 isolates ended at the identical MPN floor and were nonetheless
assigned survival values spanning exactly the 265-fold span of their starting
densities; and that a single cut on starting density reproduces all 18 labels.

**What differs.** They report an association between isoniazid resistance and
tolerance. We find that association loses two thirds of its coefficient once the
starting density enters the model, with an interval that then spans zero, and
that the mechanism is visible in their own file: resistant isolates enter the
assay ten-fold lower and 26 per cent of them lack the headroom the deepest
endpoint needs, against 8 per cent of susceptible isolates.

**Why ours is acceptable, and how it must be phrased.** This analysis exists only
because they deposited the classification alongside its inputs, which most
studies do not, and the paper says so. We do not dispute a single measurement. We
add a covariate they did not have reason to consider and report what it does. The
correct verb is *attenuates*, not *eliminates*: 0.259 to 0.089, a 66 per cent
reduction, CI +0.086 to +0.431 becoming -0.108 to +0.285.

**The one thing we must not claim.** That resistant isolates seed lower because
resistance carries a fitness cost. We checked: they do not grow significantly
more slowly here (p = 0.24), and 85 of them carry katG S315X, the allele that
predominates clinically precisely because it is close to fitness-neutral. Why
they seed lower is unexplained and is stated as such.

---

## 1. ERA4TB, the six-laboratory exercise

**van Wijk RC, Lucía A, Sudhakar PK, Sonnenkalb L, Gaudin C, Hoffmann E,
Dremierre B, Aguilar-Ayala DA, et al.** *iScience* 2023;26(5):106411.
PMID 37091238, PMC10119593, doi:10.1016/j.isci.2023.106411. Open access.

**What they did.** Ran the standardised time-kill exercise and reported it. Their
abstract states: *"Baseline bacterial burden per laboratory ranged from 3.29 to
5.97 log10 CFU/mL"* and *"Baseline bacterial burden varied between laboratories
but variability was limited in net drug effect, confirming 2.5 µL equally robust
as 100 µL plating."*

**What we did.** Built a duration endpoint on the same flasks and compared it
against a rate estimated on those same flasks.

**What differs, precisely.**

| | van Wijk et al. | this work |
|---|---|---|
| readings outside the quantification limits | excluded from numerical analysis | retained and treated as censored at the limit of their own plating volume |
| estimator | net drug effect | Tobit (Beal M3), multiple imputation with Rubin pooling, and survival analysis, cross-validated against each other |
| duration endpoint | none constructed | time to first undetectable culture, per flask |
| laboratories unable to produce the endpoint | not addressed | three of six, in every arm |

**Why ours is acceptable.** Their exclusion is a defensible reporting choice and
we do not criticise it; it simply forecloses the question we ask. Because
censoring is a property of the plated volume here — 1.0, 2.0, 2.0 and 2.6 log10
CFU/mL for 100, 10, 10 and 2.5 µL — dropping flagged readings removes the
deepest killing, and removes more of it at the laboratories that killed most.
Retaining them as censored is the standard treatment for below-limit data in
antibacterial pharmacodynamics and is what lets a rate be estimated where they
report none. Our Tobit and imputation estimates never differ by more than 0.002
log10/day, so nothing turns on which censoring model is used.

**What must be conceded in the text, in our own words before a referee's.** The
inoculum spread is theirs. We reproduce their 3.29–5.97 exactly from the raw
file. The 3.58 log10 figure our script computes is a different quantity,
restricted to the most sensitive plating, and is not a correction of theirs.
Their observation that burden varies while net effect varies less is also
theirs, and it points the same way as ours.

**What is ours.** That their reproducible net effect and their unreproducible
clearance pattern point in opposite directions, and that three laboratories
cannot produce a duration endpoint at all.

---

## 2. MIC and the minimum duration for killing

**Vijay S, Bao NLH, Vinh DN, Nhat LTH, Thu DDA, Quang NL, Trieu LPT, et al.**
*eLife* 2024;12:RP93243. PMID 39250422, PMC11383526, doi:10.7554/eLife.93243.

**What they did.** Generated the 217-isolate collection and reported a negative
association between MIC and the minimum duration for killing.

**What we did.** Tested every MIC-versus-duration comparison the deposited file
supports — six duration endpoints at 15 and 60 days, crossed with four strata,
24 tests — and corrected for the family.

**What differs, precisely.** Four tests reach p < 0.05 where 1.2 are expected by
chance. **Under Benjamini–Hochberg, none survives.**

**Why ours is acceptable, and this is the strongest defence in the paper.** The
four nominal hits share three features that a family-wise correction exists to
catch. They are concentrated in the deepest endpoint, MDK99.99, which is also
the most heavily censored at 90% of isolates sitting at the assay ceiling. They
are negative — a higher MIC going with a *shorter* duration — which is not the
direction a shared mechanism predicts and is hard to interpret mechanistically.
And they are not independent of each other: the 15-day and 60-day columns are
measured on overlapping isolates, so the four hits are not four pieces of
evidence.

We also test two things their analysis did not separate. The file contains 43
follow-up isolates from patients already represented, so we report a
baseline-only stratum rather than pooling 217 rows as independent. And we report
the correlation each stratum could have detected, so a null is bounded rather
than merely asserted: at n = 193 the design resolves ρ ≈ 0.14.

**Framing for the text.** Not "they are wrong". The honest sentence is that a
negative association is visible in individual comparisons and does not survive
correction for the comparisons available, and that the deepest endpoint where it
concentrates is 90% censored.

---

## 3. Combination therapy in the mouse arm

**Kaur P, Ramya VK, Naveenkumar CN, Bharathkumar K, Singh M, Hobbie SN,
Shandil RK, Narayanan S.** 2024, doi:10.3389/fitd.2024.1413211. Verified via
Crossref; not indexed in PubMed.

**What they did.** Deposited the workbook we analyse and reported the apramycin
plus HREZ combination as additive.

**What we did.** Withdrew a contrary claim rather than defend it. Our earlier
sub-additivity finding depended on measuring reductions against a two-mouse
post-treatment control; against the five-mouse pre-treatment control the same
arithmetic gives additivity, agreeing with them.

**Why this belongs in the Discussion at all.** It is a worked example of the
paper's own thesis applied to the paper. A 0.41 log10 "interaction" that
reverses on a choice of denominator between two control arms differing by 0.37
log10 is exactly the kind of quantity this manuscript argues should not be
transferred between studies. We report it as a demonstration, with the
withdrawal stated, not as a result.

---

## 4. Observation window and the visible dose range

**Firsov AA, Vostrov SN, Shevchenko AA, Cornaglia G.** *Antimicrob Agents
Chemother* 1997;41(6):1281. PMID 9174184, PMC163900.
**Jindani A, Doré CJ, Mitchison DA.** *Am J Respir Crit Care Med* 2003.
PMID 12519740, doi:10.1164/rccm.200210-1125OC.
**Srivastava S, Modongo C, Siyambalapitiyage Dona CW, Pasipanodya JG,
Deshpande D, Gumbo T.** *Antimicrob Agents Chemother* 2016. PMID 27458215,
PMC5038304, doi:10.1128/AAC.00961-16.

**What they did.** Firsov established that killing and regrowth parameters
depend on the observation interval. Jindani established the tuberculosis version
in 100 patients, with regression coefficients fitted per window, on the axis of
drug identity and regimen composition. Srivastava fitted E_max per sampling day
in *M. tuberculosis* under amikacin and treated the day-dependence as a design
nuisance to be optimised away.

**What we did.** Measured the concentration slope separately per interval on a
replicate-level bootstrap, and reported that the early-versus-late contrast is
firm while the early-versus-middle contrast is not.

**What differs, and this must be conceded plainly.** The general claim that a
late endpoint carries less dose information is **not new**, and the Discussion
must say so with these three citations. Srivastava in particular reaches a
different conclusion about day 14 in the same organism and drug class.

**Why our narrower version still stands.** Ours is not "the endpoint matters",
which is established. Ours is the specific arithmetic: across a 32-fold
concentration range the survivor separation is 6.9-fold at day 3, 48.2-fold at
day 7 and 5.2-fold at day 14, so a 14-day readout would call this drug
dose-insensitive. And we do not claim the late slope's sign, because the top arm
sits at 65 CFU/mL against an unstated quantification limit and censoring would
manufacture exactly that sign.

---

## 5. Which published E_max values may be used as a rate

**Musuka S, Srivastava S, Siyambalapitiyage Dona CW, Meek C, Leff R,
Pasipanodya J, Gumbo T.** *Antimicrob Agents Chemother* 2013. PMID 24041886,
PMC3837896, doi:10.1128/AAC.00829-13.

**What they did.** Report E_max values as cumulative log10 CFU reductions over a
fixed 7-day or 21-day window, alongside Hill coefficients fitted to the same
endpoints.

**What we did.** Excluded every such value from the parameter comparison, and
used only rates fitted inside a differential equation for N.

**Why ours is acceptable, stated as a rule rather than a complaint.** A
cumulative reduction has no time in its denominator and cannot be divided to
yield a maximum kill rate. Its plateau is reached when the inoculum is exhausted,
not when the drug effect saturates, so a Hill exponent fitted alongside it
measures assay geometry — inoculum size, window length, detection limit — rather
than the drug. This is why rifampicin's Hill coefficient appears as 0.49 in one
study and 1.90 in another: they are exponents on different independent variables
fitted to different dependent variables, and their difference carries no
pharmacodynamic information.

**Outstanding before this can be asserted at full strength.** The claim that in
four excluded studies the fitted E_max exceeds the entire starting inoculum is
currently documented for one. Either extract the other three, or state the rule
with the one worked example we can show.

---

## 6. Condition dependence of pharmacodynamic parameters

**Kok M, Hankemeier T, van Hasselt JGC.** *Microbiol Spectr* 2024.
PMID 39656019, PMC11705865, doi:10.1128/spectrum.01409-24. **Does not
foreclose.**

**What they did.** Showed nutrient conditions affect antimicrobial
pharmacodynamics in *Pseudomonas aeruginosa*: one laboratory, one strain, a
15-hour window, with the Hill coefficient carried in the model but not allowed
to vary systematically by condition.

**What we did.** Treated the Hill coefficient and the ψ_min/ψ_max ratio as the
objects of study rather than as carried parameters, across two organisms and two
laboratories, and reported that the ratio is drug-, condition- and
window-dependent.

**Why ours is acceptable.** Their design cannot answer whether the *shape*
parameter moves, because it was not allowed to. That is the gap, and it is a
real one rather than a difference of opinion.

---

## 7. Biofilm tolerance is a metabolic-state effect

**Walters MC 3rd, Roe F, Bugnicourt A, Franklin MJ, Stewart PS.** *Antimicrob
Agents Chemother* 2003;47(1):317-323. PMID 12499208,
doi:10.1128/AAC.47.1.317-323.2003. Verified from the article text.

**What they did.** *P. aeruginosa* colony biofilms over 100 h with fresh
antibiotic every 24 h lost only 0.49 ± 0.18 log10 to tobramycin and 1.42 ± 0.03
to ciprofloxacin. Both drugs penetrated, and they report no acceleration of
killing once they had. Oxygen reached 50–90 µm, and that zone coincided with
where an inducible reporter was expressed.

**Why this is our strongest external support, not a competitor.** It reaches the
same explanation from an independent system, laboratory and readout: tolerance
tracks metabolic state, not drug access. It is cited in support, and the
Discussion should say so explicitly rather than burying it in a list.

---

## Concessions to make in our own words

Chosen by us, so they are not chosen by a referee.

1. The between-laboratory inoculum spread is van Wijk's finding, not ours, and
   their conclusion that net effect varies less than burden anticipates part of
   ours.
2. That a late endpoint carries less dose information is established by Firsov
   1997, Jindani 2003 and Srivastava 2016. Only the arithmetic on this
   concentration range is ours, and Srivastava reaches a different conclusion
   about day 14.
3. Independence of resistance and tolerance is the premise of the
   Brauner–Balaban framework, not an open question. Our contribution is a bound
   on how large an association could have hidden, and the demonstration that the
   nominal associations in this file do not survive correction.
4. The combination sub-additivity is withdrawn and the source's additive result
   is accepted.
5. Six of seven failing parameter sets in the exposure-cycle analysis come from
   a single publication and share two growth-rate denominators. It is one
   parameter set applied to six drug-state pairs, not six independent failures.
6. Whether ψ_min = −6.0 was adopted on a log10 axis is unresolved and needs the
   original authors. The conclusion holds under both readings, 273–286 fold or
   628–658 fold, so it is stated as an open question about the source rather
   than a threat to the argument.
7. The variance decomposition does not support the strong reading of our own
   argument. Across the six-laboratory arms the rate term carries 61 to 80 per
   cent of the spread in crossing time and the distance term 20 to 39 per cent.
   A clearance time is a mixture in which the inoculum is a large minority, not
   a measurement of the inoculum. We state this in the Results, not only in the
   limitations, because it bounds the claim rather than qualifying it.
8. Both surviving label associations sit in the 15-day panel. For growth the
   difference between panels is itself supported (interaction p = 0.0072); for
   resistance it is not (p = 0.088). And because the same isolates appear in both
   panels the comparison is not independent, so it bounds the evidence rather
   than establishing it. The mechanism predicts the pattern - by 60 days the
   cultures are 38-fold denser and only 3 per cent of isolates are short of
   headroom - but a prediction confirmed in one panel of two is reported as that.
