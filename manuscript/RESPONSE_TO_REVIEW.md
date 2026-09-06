# Response to peer review

Manuscript: "Score only the kill the assay can see" (Resource).

We thank the reviewer for a review that found real errors, two of which changed
what the paper claims. Every comment is answered below in the reviewer's own
numbering. Section and table numbers refer to the revised manuscript, in which
tables are renumbered into citation order; where a number has changed, the old
one is given in brackets.

Three comments cannot be closed on the material we hold, and are marked
**OUTSTANDING** with the reason rather than answered with a reconstruction.

---

## Critical comments

**C1 — three numbers reported as two different statistics.** Resolved from the
analysis output. `results/tables/exp17_cox.csv` records 0.138, 0.172 and 0.576 as
the p-values for institutes D, E and F in the model that adds starting density;
the hazard ratios in that model are 0.339, 0.364 and 0.619. The Results were
wrong and the table and figure legend were right.

Relabelling was not the correction, because Section 5 states four sentences
earlier that no p-value attaches to a term constant within cluster. Section 5 now
reports the hazard ratios and no p-values: 0.20, 0.21 and 0.20 on laboratory
alone, moving to 0.34, 0.36 and 0.62 with starting density added, with institute
C moving the other way from 3.0 to 5.3. Figure 2D is retained, and its legend now
states that the p-values are plotted because they are what moves, not because
they are valid, and that no between-laboratory test is available on six clusters.
The audit pins each hazard ratio and, separately, the p-value it was confused
with, so the two cannot merge again.

**C2 — headroom defined twice with incompatible meanings for *H*.** Corrected
throughout. Lowercase *h* is the log-scale headroom everywhere — Introduction,
Box 1, all ten Results sections, every table legend and every figure legend — and
uppercase *H* now appears only in the Methods, where the ratio *N*₀/*L* is
defined. Both are defined once, at first use. The reviewer's related point is
also taken: *h* is a log ratio of two per-mL quantities and no longer carries the
unit "log10 CFU/mL".

**C3 — references, declarations and the AI-use statement. OUTSTANDING.** The
reference list, author names, affiliations, ORCIDs, corresponding author,
funding, competing interests, author contributions, the archived commit
identifier and an AI-use declaration are all still to be supplied. They depend on
a target journal, whose style and policy determine the reference format and the
wording of the declaration, and on author information the analysis repository
does not hold. We agree the citation check cannot be performed until this is
done. The deposit identifiers in Table 1 are unchanged and are verifiable now.

**C4 — the self-audit table disagreed with the text.** Corrected on both sides.
Of the five conclusions marked NOT SUPPORTED, three are now absent from the
manuscript entirely: the panel interaction p, the flask-level Mann–Whitney p
behind the area under the curve, and the log-rank across laboratories. For the
other two a weaker statement is retained and is marked as such where it appears —
the Cox coefficient trade is reported as hazard ratios with no p-value, and
institute C as the laboratory whose crossings its starting density does not
account for rather than as a tested contrast. The legend of Table 15 [12] now
states exactly that, so the verdict column and the text no longer disagree.

The Methods claim is corrected too. It no longer asserts that the manuscript
cannot drift from the analysis; it states that every table is generated and the
manuscript assembled from that generated material, that the audit recomputes 138
quantities, and that this coverage is not exhaustive. New static checks now read
the table legends, the figure legends, Box 1 and the Abstract, which the audit
previously never parsed.

**C5 — is the starting density itself left-censored?** No, and the reviewer's
inference from our own Methods sentence was reasonable: we had offered the
ten-fold shift in the per-visit minimum as evidence of a floor at every visit,
which it is not.

Applying this paper's own floor rule visit by visit, a floor shows as a pile-up
on the lowest rung with nothing below. Day 5 has that signature in every panel
and day 2 has it at 15 days, but day 0 does not: its minimum of 2 300 per mL
occurs **exactly once** in each panel, with the next value at 6 100. That is the
tail of a distribution, and the verdict for day 0 is that no floor is evidenced.
*N*₀ is therefore observed throughout, no model needs a censored specification,
and the headroom range and Δ*h* are values rather than bounds.

We confirmed from the data, as requested, that the headline count of 33 isolates
short of four logs is unaffected. The corrected Methods sentence now states which
visits carry the pile-up and which do not (new experiment `exp36`).

---

## Major comments

**M1 — tables out of citation order; supplementary block inside the Results.**
Done. The supplementary block was a trailing section of the generated table file
and rode along with whichever numbered table came last, which is how it landed
inside a Results section; the assembler now separates it and places it after the
figure legends. Table 3a is promoted to its own number. All 16 main and 7
supplementary tables are renumbered into citation order by a script that computes
the map from the assembled document, so it cannot drift from the text. Every
table is cited, every citation resolves, and no table is cited before it is
numbered.

**M2 — content outside its section.** Done in all three places. Box 1 keeps its
four arithmetic rows and gives back what it borrowed: the finding about the six
medium and twelve low isolates moves to Section 2, replaced by a forward pointer,
and the recommendation not to densify an inoculum moves to the Discussion, where
it now also says why. The Box stays before the Results, because this is a
Resource and the reader should be able to run the calculation before meeting a
result. The Introduction's aim paragraph now names the inversion analysis, the
dose-difference erasure, the held-out validation and the axis-independence
question, in the order the Results take them. The covariate sweep moves to
Results Section 4; the Discussion keeps only the reading of it.

**M3 — terms used before or without definition, and interchangeably.** Done.
"Ceiling" is now defined at its first use in the Results, alongside the floor and
saying explicitly that the two are different censoring mechanisms — one on the
measurement scale, one on time. *L* has one short form, the **assay floor**, used
everywhere including the self-audit table; "assay boundary" is gone entirely,
which also frees "boundary" for the two derived boundaries, and the Methods state
the convention once. The clinical floor prints as MPN per mL. FLAGGED is defined
in the legend that uses it. The Kaur row is reconciled: a deposit whose verdict is
that no floor is evidenced no longer prints a floor value.

**M4 — two column labels do not describe their contents.** Done. "Depth" is now
"Reading day" with values "day 5" and "day 2", in both tables. The predictor is
renamed "time to OD 0.4", and both the legend and a new Methods sentence state
that it is a time and therefore runs inversely to growth rate, so an odds ratio
above one means slower growth. The wavelength is not recoverable: the deposit
records the quantity as `Time_to_0.4` and names no wavelength, and the Methods now
say so rather than supplying one.

**M5 — the baseline stratum reported at five sizes.** Done. Every analysis set is
now derived in one place, as successive exclusions with a reason and a count on
each line (Table 5, from new experiment `exp37`). The baseline stratum is 174
rows, of which 6 carry the unordered MDR label and 1 lacks the growth proxy,
leaving 167 at 15 days and 161 at 60. The legend of Table 7 [4] no longer states a
single figure; the analysis-specific n is in the row.

**M6 — statistics without the information needed to check them.** Done. The
comparison now reads "22 of 84 isoniazid-resistant isolates, 26.2 per cent,
against 9 of 119 susceptible ones, 7.6 per cent", and states that the remaining
two of the 33 are MDR and outside that contrast — which is what made the
percentages irrecoverable from the totals. It is reported at one precision
throughout. The correction family is named at both locations: it is the 24
comparisons the file supports, and Table 14 [8]'s critical values are ranked
against 24. The baseline near-miss against a family of six is now presented as
the alternative reading it is, not as the reading. The resolvable correlation is
0.14 to 0.25 across all 24 tests and 0.14 to 0.18 across the six the table lists,
and the text now says which.

**M7 — the starting-density column is not on a common time base.** Done, and the
reviewer's arithmetic was right on every point. Table 8 [5] gains a reading-day
column, and its legend states that the figure pools day-0 and day-1 readings
across arms at the 100 µL plating, that institute A deposits no day-zero reading
at all, and that among treated flasks only C and D do. The day-base caveat moves
from the Limitations to Section 5, where the column is first used.

Section 6 now uses one basis throughout — untreated, day zero, 100 µL — and says
so. That resolves institute C: its apparent 0.45 log10 discrepancy was a
comparison of the section against itself on two different bases. The
treated-versus-untreated agreement is restricted to C and D at the point it is
made, those being the only two laboratories that can support it. Institute F's
inversion has a plain explanation: its untreated culture grows from 6.00 to 6.72
log10 over the same twenty-four hours, so its treated day-one readings
legitimately exceed its untreated day-zero one.

**M8 — the concentration range differs by a factor of four.** Done. Section 9 now
states that the deposit carries 1, 4, 8, 32 and 128 µg/mL, that the 1 µg/mL arm
shows net growth and is excluded from the dose comparison, and that the compared
range is therefore 4 to 128 µg/mL: 32-fold, five doublings. The Figure 3B legend
names the two arms compared. Table 1 records that the amikacin arm is not
analysed.

**M9 — the day-2 endpoint has no observability accounting of its own.** Done, and
it produced a result worth having. The day-2 floor is 230 per mL, and the day-2
class thresholds, which the source does not state, are recovered the same way as
the day-5 ones: the cuts 10⁻² and 10⁻¹ reproduce all 203 usable day-2 classes with
no disagreement, one decade shallower.

Because *L* and *c*₁ both shift by ten, the identifiability boundary does not
move: *N*_id = 23 000 per mL at both visits. The reachability boundary does move,
and the consequence is large — 121 of 203 isolates lack four logs of headroom
against the day-2 floor where 31 do against the day-5 floor. Eighteen day-2
readings rest on their own floor, eleven with a single compatible class and seven
with more than one. At 60 days no decade cuts reproduce the day-2 classes (109 of
197), so that rule is not a decade threshold and no day-2 accounting is offered
for it.

**M10 — analysis sets shrink without the reduction being stated.** Done. Table 5
reconciles every denominator the manuscript uses, per deposit, as successive
exclusions. "Usable" is defined at its first use in Results Section 2. The
promised comparison of dropped against retained rows is now reported (Table S1):
the MDR exclusion differs in susceptibility by construction, and the only
difference not by construction is in the 60-day panel, where the 20 dropped rows
sit higher in starting density.

**M11 — procedures with no stated implementation.** Done. A Methods paragraph now
describes the replicate-level bootstrap: the resampling unit is the replicate
count at each end of the interval, 20 000 draws, percentile intervals. A second
paragraph separates what comes from a package from what does not: the Brant test,
the partial-proportional-odds fit with a per-cut coefficient mask, the
product-of-coefficients mediation with bootstrap intervals and the
residual-correlation sensitivity are implemented in the released code, are named
by file, and the released likelihood is validated against the proportional-odds
fit it nests. Both dangling cross-references are repaired by naming the Methods
subsection rather than numbering it.

**M12 — Table S4 [S6] adjusts the exposure for itself.** Confirmed, and the
problem is larger than the reviewer could see from the manuscript. The exposure is
`INH-Suceptibility == "IR"`. Six of the nine pretreatment covariates are recorded
almost exclusively for resistant isolates: the two susceptibility calls and the
two Mykrobe calls for 82 of 84 resistant isolates and for **none** of the 119
susceptible ones, and the mutation identity for 79 and one. Their missingness is
the exposure, so conditioning on them conditions on resistance. That also explains
the identical rows the reviewer noticed: `INH_MGIT_DST` and `RIF_MGIT_DST` are
missing on exactly the same rows and contribute the same design matrix.

The 22 per cent attenuation we had highlighted came from the mutation identity and
was an artefact of the same circularity. Only two covariates — the growth proxy
and months on treatment — are recorded at rates unrelated to susceptibility, and
adjusting for either leaves the coefficient at −0.81 or −0.82 against an
unadjusted −0.85. The claim is restated over those two: the seeding gap moves by
at most five per cent under any adjustment the deposit can legitimately support,
which is a stronger result than the one we published.

**M13 — the identifiability boundary is confirmed only to an order of magnitude.**
Accepted, and reported. Among the eighteen censored isolates the starting density
takes five values — 23 000 for six, 230 000 for eight, and 610 000, 2.3 × 10⁶ and
6.1 × 10⁶ for one, one and two — and no isolate lies strictly between *N*_id and
*N*_reach. Any cut in that decade reproduces the same twelve-six split, and
Section 3 now says so.

The boundary case is kept and is made the load-bearing argument, as the reviewer
suggested: six isolates sit exactly on *N*_id, where *L*/*N*₀ equals *c*₁ and the
strict inequality fails, and those six are precisely the six the deposit records
as medium. A rule with the inequality reversed would have been wrong six times out
of six. Section 3 also now states that the isolate-by-isolate agreement is an
identity given the class rule rather than an independent test, and names what
could have failed and did not: that the three classes separate cleanly on the
recorded fraction at all, in 203 of 203 calls.

**M14 — the repository search is undocumented. PARTIALLY OUTSTANDING.** No query
log, access date or screening count was kept. Rather than reconstruct one, the
Methods now state that the search cannot be evidenced and report only its outcome:
one deposit carrying a measured per-culture starting density, a recorded plated
volume and per-culture time-course counts together. The related pre-specification
claim is reduced to what can be documented — the held-out deposit was opened after
every boundary and threshold was fixed, which the commit history timestamps, while
the other four were chosen for the fields they carry and that choice is not
separately registered. Table 1's caption carries the same correction.

**M15 — the Abstract's design and the title's scope. PARTIALLY OUTSTANDING.** The
title's overclaim is accepted. Three candidates are offered rather than one, each
expanding or removing the abbreviation, naming the object and the constraint, and
naming the design:

1. *Score only the kill the assay can see: the floor and the starting density
   bound a log-reduction tolerance endpoint*
2. *What a minimum duration for killing can measure: assay floor, starting
   density, and the limits of log-reduction tolerance endpoints in five published
   time-kill deposits*
3. *A tolerance endpoint is only as deep as the assay: reanalysis of five
   published time-kill deposits*

The Abstract restructure is outstanding pending a target journal, since the
required structure, word limit and whether an explicit objective sentence is
wanted all follow from it. The reviewer's substantive point — that the Abstract
never states this is a secondary reanalysis of published deposits with no new data
— will be addressed in that pass.

---

## Minor comments

**m1 — two keyword lists.** Done. One list of seven terms, identical in the front
matter and after the Abstract.

**m2 — Table S7 [S4] packs five sensitivity analyses into one sparse grid.** Done,
by restructuring rather than splitting. The five deposits are sensitive to
different quantities, so the table is now long rather than wide — one row per
deposit, floor scenario and quantity — and contains no empty cells at all. Five
separate small tables would have added four table numbers for the same content.

**m3 — figure source files do not match figure numbers.** Done. Renamed to
`fig1_dynamic_range`, `fig2_rate_vs_duration`, `fig3_endpoint_collapse` and
`fig4_independence`, with every reference updated.

**m4 — table and figure count against the journal's limit. OUTSTANDING.** The
manuscript carries 16 main tables, 7 supplementary, 4 figures and 1 box. Which of
these must move to supplementary depends on the journal's limit, and we will make
that reduction once a journal is chosen.

**m5 — the six-cluster argument is developed twice.** Done. It is stated once, in
the Limitations, and Section 5 now gives the conclusion in two sentences and
refers to it.

**m6 — the Discussion opens by repeating Results numbers.** Considered and not
changed. The Discussion's first two paragraphs already state the finding in prose
before any number appears — that the metric introduced to replace a clinical
judgement carries the same defect into a number, and that a fraction whose
numerator has been censored is no longer a fraction. The numbers follow that
statement rather than substituting for it. We are content to revisit this if the
reviewer still finds the balance wrong.

**m7 — the six-laboratory deposit is unattributed in the Results.** Done.
Attributed to van Wijk and colleagues at its first use in Section 5.

**m8 — the ethics statement records no institutional determination. OUTSTANDING.**
This requires a determination from the authors' institution and the journal's
required wording for secondary analyses of open data, neither of which we can
supply from the analysis repository.

**m9 — two headings do not match the manuscript's own terminology.** Done. Section
7 is now "The population that fell faster often crossed the floor later", and
Section 2 is "Identical floor observations received different tolerance labels".

**m10 — the 30-day panel returns identical values and is never discussed.** Done.
We confirm the two panels are not duplicates — the medians coincide because both
sit on the same most-probable-number rung — and since no section analyses the
30-day panel its rows are removed from both tables.

**m11 — MDK99 notation is never expanded.** Done, in the legend of Table 14 [8].

**m12 — CLSI M26 lacks an edition and date. OUTSTANDING.** This will be supplied
with the reference list (C3). The reviewer's substantive point, that M26 is a
general bacterial standard applied to a mycobacterial protocol, is already
conceded in Section 6 and will be cited alongside the mycobacteria-specific
guidance.

**m13 — Table 8 [5]'s final column header says "all arms".** Done. The header
reads "treated arms", which the denominator of 12 per laboratory reflects.

**m14 — six exact zeros in the Windels deposit are never mentioned.** Done. Stated
where that deposit is introduced in the Methods, with the consequence: they mark a
below-limit reading without naming a limit, fix no floor, and are why observability
labels are refused for that deposit.

**m15 — tense. OUTSTANDING pending the journal's convention.** The Results are in
the present tense and the Methods in the past, which the reviewer notes is
internally consistent and defensible for a reanalysis of a static file. We will
convert uniformly if the journal requires it.

---

## Numeric consistency table

Every row is resolved. Where two locations disagreed, the correct value was taken
from the analysis output rather than by choosing between the printed ones.

| # | Discrepancy | Resolution |
|---|---|---|
| 1 | Hazard ratios vs p-values (0.138, 0.172, 0.576) | p-values. Hazard ratios are 0.339, 0.364, 0.619. Section 5 corrected; both now pinned separately in the audit (C1) |
| 2 | *H* defined two ways | *h* is the log headroom, *H* the ratio; unit removed (C2) |
| 3 | Baseline stratum at five sizes | 174 rows, 167 at 15 days and 161 at 60 after two named exclusions; derived in Table 5 (M5) |
| 4 | 26.2% / 7.6% at three precisions, no numerators | 22 of 84 and 9 of 119; the other two of 33 are MDR. One precision throughout (M6) |
| 5 | 66% attenuation vs 67.9% implied | The percentage is removed. The path is reported as a mediated effect with an interval instead |
| 6 | Institute C headroom 3.61 vs 3.16 implied | Two bases in adjacent paragraphs. Section 6 now uses one throughout; C reconciles (M7) |
| 7 | Table 8 [5] densities vs Section 6 densities | Different bases, now stated. A reading-day column is added and the day-base caveat moved to Section 5 (M7) |
| 8 | 32-fold vs 128-fold apramycin range | 4 to 128 µg/mL, 32-fold, five doublings; the 1 µg/mL arm is excluded and now named (M8) |
| 9 | 261 vs 288 vs 360 series | 90 flasks × 4 platings = 360; 288 treated; 261 after 27 named drops. Derived in Table 5 |
| 10 | 67 vs 72 flasks | Five treated flasks carry no usable starting density. Derived in Table 5 |
| 11 | 42 vs 72 flasks | The 191 pairs are cross-laboratory pairs within arm, not flasks. Derived in Table 5 |
| 12 | 203 usable vs 202 in Table 7 [4] | One isolate lacks the growth proxy. "Usable" defined at first use; both derived in Table 5 |
| 13 | 30-day and 60-day rows identical | Confirmed not duplicates; the medians share a rung. The 30-day rows are removed as unanalysed (m10) |
| 14 | Kaur floor "none" vs "40" | A deposit with no evidenced floor no longer prints one (M3) |
| 15 | BH threshold 0.0021 vs 0.0083 | The family is 24 and is now named at both locations; the family-of-six reading is given as the alternative it is (M6) |
| 16 | Resolvable ρ 0.14–0.25 vs 0.14–0.18 | 0.14–0.25 across all 24 tests, 0.14–0.18 across the six tabulated. Both now stated (M6) |
| 17 | Dubey 12.2-fold vs 12.0 recomputed | 12.2 from the unrounded median of 1.22 × 10⁶, which displays as 6.08 log10. The convention is now stated |
| 18 | Headroom span 4.42 vs 4.43 | Both are the same unrounded 4.4236; the text now says so |
| 19 | Table 8 [5] header "all arms" | Corrected to "treated arms" (m13) |
| 20 | Two keyword lists | One list of seven (m1) |

---

## What changed in the analysis

Four new experiments were written to answer comments rather than to argue with
them, and all are in the released code:

- `exp36` applies the paper's own floor rule visit by visit (C5), recovers the
  day-2 class thresholds and computes the day-2 boundaries (M9), and screens every
  covariate for whether its missingness is the exposure (M12).
- `exp37` derives every analysis set as successive exclusions and compares dropped
  against retained rows (M5, M10).
- `exp33` and `exp34`, already present, supply the floor posterior and the
  mediation decomposition the responses to M3 and M12 rely on.

The audit script now runs 138 value checks, and four new static checkers read the
table legends, the figure legends, Box 1 and the Abstract, check that a number
labelled a hazard ratio in one place is not a p-value in another, recompute every
percentage, fold-change and corrected threshold from its own stated inputs, and
verify that no conclusion the self-audit marks unsupported still appears asserted.
