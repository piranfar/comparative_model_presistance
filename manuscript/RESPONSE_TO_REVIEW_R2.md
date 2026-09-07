# Response to peer review — round two

Manuscript: "Score only the kill the assay can see" (Resource).

We thank the reviewer for a second reading that found eleven real defects. None
required re-analysis. Each was a stale token, a qualifier that did not travel, a
census that did not reconcile, or a passage left in place when its replacement
was inserted — and one of them, C1, had the manuscript restating a claim we had
withdrawn in round one. Every comment is answered below in the reviewer's own
numbering. Section, table and figure numbers refer to the revised manuscript; the
numbering is unchanged from the round-one revision.

Two comments cannot be closed on the material we hold and are marked
**OUTSTANDING** with the reason, exactly as in the round-one letter. Two more are
answered in part and marked **PARTIALLY OUTSTANDING**.

## The cumulative state after two rounds

Round one raised 35 comments (C1–C5, M1–M15, m1–m15) and this round did not
reopen most of them. C2 (the two meanings of *H*), C5 (whether *N*₀ is itself
left-censored), M2 (content outside its section), M4 (two mislabelled columns),
M11 (procedures with no stated implementation), m1 (the duplicated keyword list),
m2 (the sparse sensitivity grid), m6 (the Discussion's opening), m7 (the
unattributed six-laboratory deposit), m9 (two headings), m10 (the 30-day panel)
and m14 (the six exact zeros in the Windels deposit) all stand as answered; each
was checked again here rather than assumed, and the fixes are intact.

Four round-one comments were revisited because this round found their execution
incomplete rather than their answer wrong. Round-one M13 asked us to make the
boundary case load-bearing and to concede that the isolate-by-isolate agreement
is an identity; the replacement paragraph was inserted and its predecessor was
not deleted, which is round-two C1. Round-one M1 renumbered the tables into
citation order but left the layout order unfixed, which is round-two m2.
Round-one M6 fixed the 26.2 / 7.6 per cent contrast in Section 2 and not in the
two places downstream of it, which is round-two m1. Round-one m3 renamed the four
figure sources and left a fifth script claiming a figure number it no longer has,
which is round-two m9. These are failures of follow-through on our side, not new
findings.

Five round-one comments were left **OUTSTANDING** in that letter and remain so,
for the same reasons: C3 (references, declarations and the AI-use statement,
which is this round's C2), M15's title and Abstract structure (this round's M9),
m4 (the table and figure count against a journal limit), m8 (the ethics
determination, this round's m6) and m15 (tense). Round-one M14 remains partially
outstanding: the repository search still cannot be evidenced, and the Methods
still say so.

## The numeric consistency table

The review's eleven-row numeric consistency table is not in the material we hold,
and we cannot answer it row by row. Read against the numbered comments as far as
we can reconstruct it, every row appears to correspond to one of them —
principally M2, M5, m1 and m8, which are the four comments about a quantity whose
base, precision or partition did not reconcile. **The authors should check that
table against this response before submission**, and any row it contains that is
not answered here should be treated as unanswered rather than as covered.

---

## Critical comments

**C1 — the superseded passage at the end of Results Section 3.** Confirmed, and
this is the one that mattered. The round-one revision rewrote Section 3 to
concede that the agreement between the algebra and the deposit is an identity
given the class rule rather than a passed test. The replacement paragraph was
spliced in; the passage it replaced was never removed. The section therefore made
the boundary-case argument twice and closed on the sentence "A relationship fitted
to the data would not fail in the right places as well as succeeding in the right
places" — which is the reading we had retracted four paragraphs earlier.

Deleted. Section 3 now ends the boundary-case paragraph at "…given a floor, a set
of thresholds and a starting density, the affected isolates can be named before
any reading is taken", and the section closes on the paragraph that was always
meant to close it: "The empirical findings are therefore consequences of the
definitions rather than properties of this deposit, and the claim is a prediction
that any dataset reporting a starting density, a floor and a threshold
classification can be checked against."

The Discussion carried the same overclaim in one sentence and is corrected with
it. *What fails, and where* now reads: "In the clinical deposit that agreement is
exact isolate by isolate, though for the twelve with a single compatible class it
is an identity given the class rule rather than an independent test. What could
have gone the other way is the boundary, where six isolates sit at *N*_id itself,
the strict inequality leaves them undecidable, and the deposit records all six as
medium rather than low."

Why neither audit caught it: the withdrawn-claim check matched numeric literals,
and this reassertion carried no numbers. A new checker,
`src/audit/check_duplication.py`, now reads for a repeated span inside one section
and for a struck-out conclusion reasserted without its numbers, and
`src/audit/check_consistency.py` gained a fourth family of check for the same
failure.

**C2 — references, declarations, ethics and the generative-AI statement.
PARTIALLY OUTSTANDING.** The reference list has been compiled and verified and is
in the repository as `manuscript/REFERENCES_DRAFT.md`. It carries 50 entries, each
checked against a primary record — PubMed, Crossref, Project Euclid, the figshare
and Zenodo APIs, or the issuing body's own catalogue — with the manuscript
sentence each supports quoted verbatim and a support check on each. Nothing in it
was reconstructed from memory. Eleven items (U1–U11) are listed with the exact
field that is missing and where to obtain it, rather than filled in by inference.

The compilation also found substantive gaps the manuscript had, which that file
records: the most-probable-number table on which the entire floor inference for
the primary deposit rests is uncited, and the deposit's MPN scheme is unstated;
Turnbull 1976, the Tobit model itself, Rubin's rules and the Grambsch–Therneau
test are all used and uncited; and Brauner et al. 2017 is in *Biophysical
Journal*, not *Nature Reviews Microbiology*.

The list is **not inserted into the manuscript**, and that is deliberate. Whether
the style is numeric or author–date decides whether the R-numbering means
anything, and hard-coding markers now would guarantee a second renumbering. The
Methods still say the list is held back until the text stops moving.

Everything else in this comment is outstanding for the reasons given in round one.
Author names, affiliations, ORCIDs, the corresponding author, funding, competing
interests, CRediT contributions, the archived commit identifier and the
generative-AI declaration all depend on author information the analysis repository
does not hold, and on a journal whose policy fixes the required wording. The
Declarations block still reads "[to be inserted]" at each of those points, and the
manuscript carries no AI-use statement of any kind. The deposit identifiers in
Table 1 are unchanged and are verifiable now.

---

## Major comments

**M1 — "MDK" written where the manuscript means "MDR".** Corrected. Methods,
*Estimation*: "The MDR category of the deposited label is a fourth, unordered
category and is excluded; all 14 rows carrying it fall outside the
susceptible-versus-resistant contrast in any case, so the ordinal and linear
models are fitted to identical rows." The abbreviation is also now expanded at its
first use in Results Section 1, which it was not before: the deposit "writes
literally as 'MDR', conventionally multidrug-resistant".

**M2 — the covariate census did not partition.** Corrected, and the arithmetic
was wrong in three places rather than one: the Results said six of nine and then
named five, Table S4's legend said six of nine, and the analysis script's own
docstring said six of eight. The correct census is seven of nine unusable,
failing in two distinct ways, and Results Section 4 now says so: "Seven of the
nine pretreatment covariates the file carries cannot adjust this association, and
they fail in two different ways." Five are recorded almost exclusively for
resistant isolates — the two susceptibility calls, the two Mykrobe calls and the
mutation identity — so their missingness is the exposure. The other two are the
isoniazid and rifampicin MICs, recorded for all 119 susceptible isolates and 67
of 84 resistant ones: their missingness sits inside the exposed group rather than
across the contrast, and the isoniazid MIC separates the two groups with no
overlap, so it is the exposure on a graded scale. The remaining two, the growth
proxy and months on treatment, are the two that can be used. Five plus two plus
two is nine.

Table S4's nine rows now carry a three-valued verdict column whose rule the legend
states — "PROXY means the covariate is recorded for no isolate in one of the two
exposure groups, so its missingness is the exposure; PARTIAL means both groups
record it but the missingness is still tied to the exposure (Fisher exact
p < 10⁻⁶); INDEPENDENT means it is not" — so the census can be checked against the
table it describes rather than taken on trust.

**M3 — "a descriptive row in Tables 9, 14 and S2" does not resolve.** Confirmed;
the sentence was false as printed. The list was correct at an earlier commit and
was never renumbered when the tables were: old Table 9 is still 9, but old Table
14 is now Table 2 and old Table S2 is now Table S5. Methods, *A deposit held out
for validation*, now reads: "It does appear descriptively — a row of its own in
Tables 2, 5, 9, 16, S5 and S7, and a table of its own in Table 12 — which is
reporting rather than fitting." Each of those seven was verified against the table
bodies. The one further appearance is Table 1, the deposit inventory that this same
subsection expands in prose.

Why the audit missed it: the cross-reference check tested that a cited table
number *exists*, never that the table contains what the sentence says it contains,
so all three numbers passed. A new checker, `src/audit/check_deposits.py`, now
tests the other half of a citation.

**M4 — the Methods declare a terminology rule and then break it.** Corrected
throughout. The rule stands where it was: "In running text *L* is the **assay
floor**, and that is the only short form used, so that 'boundary' is left free for
the two derived boundaries of the next subsection and never denotes a value."
"Boundary" used of the assay floor is now gone from the manuscript body
(37 occurrences of "boundary" or "boundaries" in the prose source before, 25
after) and from the generated tables (5 before, 1 after, that one being the
held-out deposit's pre-specification in Table 1). Every
surviving occurrence denotes *N*_reach, *N*_id, the pair, or the boundary case
between them. Table 8's column header is now "Flasks ever crossing the floor
(treated arms)", Table 16's legend is "What the assay floor *L* is in each deposit
analysed", and Tables 6 and 10's legends are corrected the same way. A new
checker, `src/audit/check_terms.py`, enforces that Methods sentence and reports if
the manuscript ever stops making the promise, on the ground that a checker
enforcing a rule the paper no longer states is worse than no checker.

**M5 — the "31" in Results Section 1 is quoted on a denominator the reader cannot
see.** Corrected in both places. The 121 and the 31 are both on 203, and only the
121 said so. Section 1 now reads: "121 of 203 isolates lack the headroom for a
four-log reduction against the day-2 floor, where 31 of those 203 isolates lack it
against the day-5 floor." The reader also needed to be told why the headline count
is 33 and this one is 31, so the paragraph reporting the 33 now says: "Two of those
33 carry a fourth label that the deposit writes literally as 'MDR', conventionally
multidrug-resistant, and that is unordered with respect to the other three, so no
ordered analysis can place it (Table 5); the same count over the 203 isolates with
an ordered label is therefore the 31 quoted above." The 31 is now pinned by the
value audit as well.

Why the audit missed it: the flow-account check matched a sample size on the number
alone, and 31 is a real count on the 203 base, so a bare "31" passed. The check now
also flags a numerator set against a stated "A of B" proportion but given no base of
its own.

**M6 — the audit claim is scoped in the Methods and unbounded in Data and code
availability.** Corrected. The Methods paragraph already said the coverage is not
exhaustive; the availability statement still said the audit "recomputes each one".
It now reads: "…two audit stages check it: one recomputes the pinned quantities —
the load-bearing counts, every headline interval and every figure a conclusion
rests on — from the tables they came from; the other reads the table legends, the
figure legends, Box 1 and the Abstract that the first does not. Both report
anything that disagrees, and neither pins every cell of every table, as the
Reproducibility subsection states." The same paragraph now says "both audit
scripts" rather than "the audit script", which is what the repository contains.

**M7 — the "at the 100 µL plating" qualifier did not reach the Figure 2 legend or
Table 15.** Done for Figure 2; deliberately not done for Table 15, and the reason
is stated rather than left implicit.

Figure 2's legend now carries it in both panels that need it: "(**B**)
Kaplan–Meier curves for time to the first observed crossing below the assay floor
at the 100 µL plating. Three curves never descend: those laboratories recorded no
flask below the floor in any arm at that plating…", and "(**C**) … The three
lowest starting densities are exactly the three laboratories that recorded
crossings at the 100 µL plating." The figure's own panel notes, which are
generated separately from the legend and so had to be corrected separately, carry
it in panels A, B and C, and the Limitations sentence that quotes the
three-against-three split now reads "Three laboratories recorded crossings at the
100 µL plating and three did not".

Table 15 is unchanged, because its rows quote each conclusion as we originally
published it, before the qualifier existed — which is what makes the verdict
column mean anything. What was wrong there was the column heading saying only "as
stated"; that is comment m3, and it is fixed. The static checker grades an absent
qualifier in that table as a reportable judgement call rather than a
contradiction, for the same reason.

**M8 — the MXF 1× MIC arm is missing from Table 11's variance decomposition
without comment.** Corrected in the legend and in the text. Table 11's legend now
reads: "The last two columns decompose the spread in crossing time; the rate term
is the larger in each of the three arms that can be decomposed. Moxifloxacin at
one times MIC is not among them: the decomposition is taken on log *D* and log
*b*, five of six laboratories record net growth in that arm, and only one flask in
it returns a positive fitted rate, so there is no spread in the rate to divide."
Results Section 7 makes the same correction to the claim it draws from that table:
the bolded sentence now reads "The rate contributes more of the spread than the
distance does in each of the three arms that can be decomposed" rather than "in
every arm", and the sentence after it names the fourth arm and why it is absent.

**M9 — the title's unexpanded "MDK" and universal "every MDK", and the Abstract.
PARTIALLY OUTSTANDING.**

The Abstract is done. It now states the design in its first paragraph — "Five
published time-kill deposits are reanalysed as deposited; no experiment was
performed for this paper" — which was the reviewer's substantive point in round
one and again here, and it is back to 300 words exactly, from 307. The held-out
deposit is named as held out in the closing paragraph ("In a hollow-fibre
experiment held out from this work…") rather than described as one the framework
never saw.

The title is **OUTSTANDING**, and it is an authors' decision we should not take by
default. The round-one letter offered three candidates; none was adopted, so the
title still reads "…starting density and the floor bound every MDK" and the short
title still reads "Headroom bounds every MDK". The terminology checker reports
this as the single remaining medium finding in the manuscript, on the ground that
the title, the Abstract and the body are read separately and each has to carry
its own first use.

The reviewer's second point is the one the round-one candidates did not meet:
that the title asserts a universal the Discussion spends a paragraph walking
back, since what fails universally is not every tolerance call but the
interpretability of a deep log-reduction call reported without *N*₀ and *L*.
Three candidates are therefore offered afresh, each dropping or expanding the
abbreviation, each claiming only what that paragraph concedes, and each naming
the design:

1. *Score only the kill the assay can see: the detection floor bounds any deep
   log-reduction endpoint, in five published time-kill deposits*
   — short title: *The floor bounds deep-kill endpoints*.
   Keeps the working register of the present title unchanged and narrows only
   what follows the colon. The design rides in the tail rather than in a true
   subtitle.
2. *A deep log-reduction endpoint cannot be read without its starting density and
   its detection floor: a reanalysis of five published time-kill deposits*
   — short title: *Deep-kill endpoints need N*₀ *and the floor*.
   States the Discussion's concession almost in its own words and names the
   secondary design explicitly. It gives up the imperative.
3. *Headroom, not tolerance: what five published time-kill deposits can and
   cannot say about the minimum duration for killing*
   — short title: *What time-kill deposits can say about MDK*.
   Expands the abbreviation in full, and "can and cannot say" is the Resource
   claim rather than a universal about every call. The Abstract's structure and word limit also remain
outstanding pending a target journal, as in round one.

---

## Minor comments

**m1 — the headroom contrast quoted at three precisions.** Corrected. It is 26.2
per cent everywhere: Results Section 2 ("22 of 84 isoniazid-resistant isolates,
26.2 per cent, against 9 of 119 susceptible ones"), Results Section 4 ("26.2 per
cent of them lack the headroom for the deepest endpoint against 7.6 per cent of
susceptible isolates (Section 2)") and the Discussion ("resistant isolates enter
the assay ten-fold lower and 26.2 per cent of them lack the headroom the endpoint
requires"). "26 per cent" and "a quarter" are gone, and Section 4's sentence now
points back to where the numerators are.

**m2 — Table 5's body is laid out before Table 4's.** Corrected, and by
construction rather than by hand. Two rules had drifted apart: tables are numbered
on first citation anywhere, while the assembler spliced each one after its first
citation inside the Results, and Table 5's Results citation precedes Table 4's.
Splice positions are now clamped to be non-decreasing in table number, so body
order matches numbering by construction. That also fixed a second inversion the
comment did not name — Table 10 was laid out before Table 9 — and the assembled
document now runs 1 to 16, then S1 to S7, in order.

**m3 — Table 15's column heading "Conclusion as stated".** Corrected to
"Conclusion as originally stated". The rows quote each conclusion in its
pre-revision wording, which is what makes the verdict column meaningful; the old
heading invited the reader to look for them in the current text and find several
of them gone.

**m4 — Table 15's row on the ceiling contrast marked WEAKENED.** Corrected. The
verdict is now WITHDRAWN, the "Method used instead" cell reads "none: the null is
arithmetically impossible", and the row's own note records why: "an isolate short
of four logs of headroom cannot record a four-log reduction, so the 0 of 33 cell
is fixed by arithmetic and the null of independence is false before any data are
seen; Section 1 reports the census and no test." The legend's tally follows — "20
survive unchanged, 6 survive with materially wider uncertainty, 5 do not survive,
and 1 is withdrawn because its null is false before any data are seen" — as do the
two sentences in the Discussion and the Limitations that quote it, and the value
audit, which now pins four verdict counts instead of three.

**m5 — the amikacin note reached Table 1 but not the Methods.** Corrected.
Methods, *Datasets*, *Concentration-by-time grid*: "The amikacin arms are not
analysed here. Within apramycin the 1 µg/mL arm shows net growth rather than
killing and is excluded from the dose comparison, leaving 4 to 128 µg/mL as the
range compared (Section 9)." That also brings the round-one M8 exclusion into the
Methods, where it belonged.

**m6 — the ethics statement records no institutional determination.
OUTSTANDING.** Unchanged from round one and for the same reason. The statement
still reads only: "This study reanalysed publicly available, de-identified
datasets. No new patient samples were collected and no new experimental data were
generated." A determination from the authors' institution — most likely that the
work is not human-subjects research and requires no review — and the journal's
required wording for secondary analyses of open data are both needed, and neither
can be supplied from the analysis repository.

**m7 — Table 7's legend claims the proportional-odds assumption "holds throughout
this family".** Corrected. It now reads "the assumption holds for every predictor
in this family", followed by the exception the old wording concealed: "Starting
density enters the adjusted fits as a covariate rather than as a member of the
family, and it is where proportional odds fails, at 60 days at the deepest
endpoint; that failure and the released fit are reported in Section 4." The claim
and its exception are now in the same legend.

**m8 — the three flask counts in Section 5 on three unnamed bases.** Corrected,
and there were four rather than three once we traced them. Each now names its
base: "at the 100 µL quadruplicate plating, the most sensitive of the four, and
there 29 of 72 treated flasks ever fall below the floor"; "Counting a crossing on
**any** of the four platings gives 48 of the same 72 treated flasks, and every
laboratory records at least one — D six of its twelve, E one, F ten"; "the 32
flasks that fell below the floor at the most sensitive plating — the 29 treated
flasks above and three untreated ones"; and "counted by flask, 53 of the 90
contain a crossing series — the 48 treated flasks above and five untreated ones".
A reader can now get from any one of the four to the other three.

**m9 — the figure source file names.** Corrected. Round one renamed the four
figure scripts to match their figure numbers; a fifth,
`src/figures/fig13_parameter_transfer.py`, still opened "Figure S1. Published
pharmacodynamic constants transfer only when they are rates." It has not been a
figure of this paper since the rate-constant comparison left it — the assembler
neither embeds it nor lists it as supplementary, and the front matter declares
four figures and no supplementary figures. Its docstring now says exactly that,
the pipeline stage that runs it is labelled "aside … (not a figure of this paper)"
rather than "fig S1", and `results/README.md` lists the four current figures under
this paper and this one under Unassigned.

---

## Where this revision went beyond the review

Briefly, since the editor has the review.

- The M3 cross-reference fix produced a list the reviewer did not supply and that
  neither of our own two passes reached: the first proposed a seven-table list
  that quietly broadened an authorial selection, the second a three-table list
  that was too narrow. The committed list was verified table by table against the
  table bodies and against the deposit map the new checker builds.
- Four static checkers were added — `check_terms`, `check_census`,
  `check_duplication`, `check_deposits` — and each was broken by an adversarial
  pass on correct prose before it was kept. Each module's docstring records the
  constructions that defeated an earlier version of the rule and how the rule was
  narrowed, and `check_terms` ships a `--selftest` that plants every defect it
  claims to catch.
- Those checkers immediately found three defects the review had not: Table 7's
  legend sent readers to Table S2 for a clustered variant that is not there (Table
  S2 is the ordinal-versus-linear comparison; the clustered treatment is that
  table's own baseline-isolate column and the verdicts in Table 15); MDR, OD and
  BH were used and never written out; and Figure 1C and the Table 6 legend named
  no culture-age panel, though the 60-day panel has six isolates at the floor of
  its own and that legend already uses "six" for something else.
- The descriptive Cox's 261 series had no line in the flow account, so a reader
  could not get from 288 to 261. Table 5 now carries both intermediate steps and
  the chain runs 360 → 288 → 262 → 261, read from the analysis receipt rather than
  recomputed alongside it.
- NCCLS, not CLSI, issued M26-A in 1999; the body was renamed in 2005. Section 6
  now attributes it correctly, and the sentence comparing realised densities
  against the target names M26-A rather than CLSI.
- The Dubey inoculum was quoted as 1.22 × 10⁶ and 12.2-fold, which is neither
  median the pipeline computes: the counts give 1,215,000 and the log10s
  1,214,743, both a rounding tie at three significant figures, which is how 12.2
  arose. The text now reads 1.215 × 10⁶ and 12.15-fold in both places, and the
  count median is pinned by the audit so the two cannot part again.
- Three smaller fixes in the same families as m1 and M2: "88 per cent" against
  "88.0 per cent" for one quantity within Section 1, "a third" against "more than
  a third" for the inversion rate between Section 7 and the Discussion, and the
  analysis script's own docstring census, which said six of eight.

The pipeline now runs 32 stages, the value audit 142 checks, and the manuscript
audit reports 0 high and 0 medium findings apart from the unexpanded MDK in the
title, which is the title decision itself (M9).

---

## What the authors must still supply

| Comment | What is needed | From whom |
|---|---|---|
| C2 | Author names, affiliations, ORCIDs, corresponding author, funding, competing interests, CRediT contributions, archived commit identifier, generative-AI declaration | The authors |
| C2 | The reference style, and the eleven fields listed as U1–U11 in `manuscript/REFERENCES_DRAFT.md` | The journal, then the authors |
| M9 | The title, from the three candidates offered under M9 above or another; the Abstract's structure and word limit | The authors, then the journal |
| m6 | An institutional ethics determination, and the journal's wording for secondary analyses of open data | The authors' institution |
| Round-one m4 | Which tables and figures move to supplementary | The journal's limit |
| Round-one m15 | The tense convention | The journal |
| Round-one M14 | Nothing further: the search cannot be evidenced, and the Methods say so | — |
