# Journal version — outline

Forward-facing. No correction narrative, no "version 1", no withdrawal language.
That material stays in the bioRxiv revision note, where it belongs. This document
is the plan the journal manuscript is written from.

Section titles are the author's. Two of them fix real problems with the working
titles used earlier: "sensitivity landscape" covers both findings, where
"governing parameter" covered only the slow grower; and "distinct phenotypic
signatures" drops a mathematical claim the numbers do not support, since
persistence moves MDK99 by 2.5% rather than not at all.

## Structure

| § | Title | Content | Figure |
|---|---|---|---|
| 1 | Introduction | The three strategies and their clinical weight; Brauner's operational definitions; that models write all three as one exponential and thereby make them indistinguishable; what this work builds | — |
| 2 | A state-structured pharmacodynamic model | Replicating and dormant compartments, each with a sigmoid concentration–response; parameters and their provenance | — |
| 3.1 | **State structure generates biphasic killing** | No imposed breakpoint; time to LOD finite and computable | Fig 1 |
| 3.2 | **Resistance, tolerance, and persistence produce distinct phenotypic signatures** | MIC / MDK99 / MDK99.99 — the measurable signature of each strategy | Fig 2 |
| 3.3 | **Growth regime determines the sensitivity landscape** | Slow grower: resuscitation rate carries 78% of first-order variance, interactions 2.3%. Fast grower: resuscitation contributes zero, and 69.5% of the variance is interaction between kill rate and replication rate | Fig 3 |
| 3.4 | **Which parameters can the data identify?** | Profile likelihood under a censored likelihood; the transition time is unidentifiable in 4 of 4 sampling designs | Fig 4 |
| 3.5 | **Model selection needs more than R²** | R² > 0.9 for both a correct and a structurally broken model; AICc differs by 81.5 | Fig 5 |
| 4.1 | **Positioning the model within existing frameworks** | Patra & Klumpp 2013, Magombedze 2021, Martinecz 2023, Abel zur Wiesch 2015 answered directly | — |
| 4.2 | **What to measure** | Which sampling design identifies which parameter | — |
| 4.3 | **Scope and limitations** | Where the model applies, and where it does not: no experimental data, illustrative parameters | — |
| 5 | Conclusion | Assertive close: the strategies become three measurements a laboratory already has the assays to make | — |
| 6 | Methods | Equations, solver, Sobol design and convergence, profile likelihood, public code | — |

## Methods placement

Journal-dependent, so it is not decided here:

- **CPT: Pharmacometrics & Systems Pharmacology**, **Journal of Theoretical Biology** — standard IMRaD, Methods after the Introduction.
- **PLOS Computational Biology** — Methods last, as laid out above.

Written so the Methods section is self-contained and can be moved without
rewriting anything that refers to it.

## Section 4.1 is not optional

The present draft cites none of those four papers. Magombedze 2021 ranks the
slow-phase kill slope first at 100% importance for therapy duration in 1,924
REMoxTB patients, which is the strongest clinical evidence bearing on §3.3 and
points the other way. Patra & Klumpp 2013 already contains the algebra. A referee
will raise both. Raised first by the authors and answered, they position the
work; raised first by the referee, they end it.

The answer §3.3 can defend: the claim is a property of this model under
illustrative parameters, the two organisms are governed by different parameters,
and the clinical fits that rank kill rate first contain no resuscitation term at
all, so they cannot test it.

## Title

Chosen after §3.3 is final, not before. The working candidate rested on a
between-species comparison that was confounded by exposure until this revision;
it is now defensible, but the wording should follow the section titles above.
