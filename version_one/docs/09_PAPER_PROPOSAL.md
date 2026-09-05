# Paper proposal: what this work adds up to

**Date:** 2026-09-04
**Status:** proposal. Nothing here is committed to. Section 5 lists what is still missing.

---

## 1. The thesis

One sentence:

> **In persistence pharmacodynamics the parameters that get reported are not
> identifiable, and the quantity that is identifiable is not reported. Conclusions
> often survive anyway, because what determines the outcome is not the parameter
> value but the regime it sits in, and the regime is identifiable.**

That third clause is what makes this a contribution rather than a complaint. A
paper that only says "your parameters are unidentifiable" is a nuisance. A paper
that says "they are unidentifiable, here is why your conclusion is nonetheless
safe, and here is what you should report instead" is useful to the field and
defensible in review.

## 2. The three legs, and the evidence already in hand

### Leg 1 — the reported parameters are not identifiable

| Evidence | Status | Where |
|---|---|---|
| Survival depends on the dormant fraction α and the persister kill rate only through their **product**, so survival data determines one number and models use two | done, analytic + numerical | `exp04`, fig08 |
| Demonstrated on a real published dataset: freeing the persister death rate moves α over an 18-fold range with log-likelihood change < 10⁻¹³ | done | `exp04`, fig08C |
| A single time-kill curve, the design most published studies use, identifies **0 of 7** parameters of the standard two-compartment model | done | scratchpad `identifiability_probe.py` |
| Robust across parameter space: the persister kill rate is unidentifiable in 93% of Mtb draws and 98% of *S. aureus* draws over ±50% | done, 100 draws | scratchpad `design_probe.py` |
| The best public *M. tuberculosis* time-kill dataset (ERA4TB, 6 labs, 2,120 points) identifies **1 of 7**, because it has two concentrations | done | scratchpad |
| The transition time of the closed-form biphasic law is unidentifiable in 4 of 4 realistic designs and lands on the optimiser bound in 3 | done | `exp02`, fig03 |

### Leg 2 — this usually does not invalidate the conclusion

| Evidence | Status | Where |
|---|---|---|
| Raising the dormant fraction 19-fold in a 2026 *Mol Biol Evol* paper, to the value its own survival data implies, changes its result not at all (Mann-Whitney p = 0.45); the contrast widens from 1.77× to 1.92× | done, 120 simulations of their unmodified code | `exp05`, fig09 |
| The parameters that cannot be measured are largely the ones that do not drive the outcome | **point estimate only** | `exp03` + scratchpad |
| Mechanism: both values sit in the same regime, and the identified combination determines the regime | argued, not yet formalised | — |

### Leg 3 — but the reported numbers are wrong, and here is what to report

| Evidence | Status | Where |
|---|---|---|
| R² above 0.9 for both a correct and a structurally broken model on the same data, while AICc differs by up to 84 | done | `exp02`, fig07C |
| The closed-form biphasic law raises the population 2.6 to 3.5 log₁₀ at its transition and can never sterilise | done | `exp01`, fig02 |
| Resistance, tolerance and persistence written as one exponential are formally indistinguishable; they separate onto orthogonal axes only in a structured model | done | fig06 |
| Concentration diversity, not replication or sampling density, is the binding constraint on identifiability | done | scratchpad |
| Global sensitivity on a structured model names a determinant the closed form cannot express (resuscitation rate, first-order Sobol 0.87) | done | `exp03`, fig04 |

## 3. Two case studies, and why both are needed

**Case A, the closed-form biphasic law.** Our own preprint's Equation 4, and the
same form wherever it appears. Shows the failure in its starkest form: the
reported transition time is where the optimiser stopped.

**Case B, Boccarella et al. 2026** (*Mol Biol Evol* 43:msag180,
doi:10.1093/molbev/msag180). Shows the failure on a current, well-executed,
fully deposited paper, and then shows the conclusion surviving. Without Case B
the paper reads as an attack on a flawed preprint. With it, the point is general.

Case B is only usable because they deposited code and data under CC BY 4.0. That
should be said in the paper, prominently and without irony. Their openness is
what makes the analysis possible, and a reader should come away wanting to
deposit like they did, not fearing it.

## 4. How to do it, in order

**Phase 1, formalise what is in the scratchpad.** The identifiability and design
probes are currently throwaway scripts. They become `exp07` (Fisher information
across designs), `exp08` (robustness across parameter space) and `exp09`
(importance against measurability). Roughly two days.

**Phase 2, close the two gaps in Leg 2.** The importance-versus-measurability
pairing exists only at a single parameter point; Sobol must be run across the
parameter space the way the Fisher analysis already is. And the regime argument
needs to be made analytically: define the regime boundary, show both values fall
on the same side, show where the boundary is. This is the intellectual core and
is currently the weakest part.

**Phase 3, resolve or disclose the Boccarella residual.** 12% of our
low-persistence populations never evolve against 0.6% of theirs. Either their
reply explains it, or it is reported as an unexplained difference with its size.
Not a blocker either way, but it must not be quietly dropped.

**Phase 4, the constructive section.** What design identifies what, and what to
report when a parameter is not identifiable: the identified combination, the
regime, and sensitivity bands rather than point estimates.

**Phase 5, write.** Target *Journal of Pharmacokinetics and Pharmacodynamics* or
*CPT: Pharmacometrics & Systems Pharmacology*. *PLOS Computational Biology* is
the alternative if the framing leans more biological than pharmacometric.

## 5. What is missing, and the risks

**Missing work:**
- Sobol across parameter space, not one point (Phase 2).
- The regime boundary made analytic rather than asserted.
- The Boccarella residual.
- A structural identifiability proof for the product form, so Leg 1 rests on a
  theorem and not only on numerics.

**Positioning risks, all real:**
- **Cogan et al. 2026** (*J R Soc Interface*, doi:10.1098/rsif.2025.0938) applied
  uncertainty, sensitivity and identifiability to bacterial persistence four
  months ago. Different question, adjacent territory. Must be cited prominently
  and the difference stated plainly: they order the methods, we ask what
  published designs support.
- **Kristoffersson, Hooker, Karlsson and Friberg, PAGE 2011 abstract 2243** did
  optimal design on essentially this model. Never published in a journal, so the
  niche is open, but the idea is not new and those authors are likely referees.
- The structural identifiability of a sum of two exponentials is classical. The
  novelty must sit in **practical** identifiability under sparse sampling and
  censoring, never in the structural result.

**Relational risk:** Case B uses a paper whose authors we have just written to.
Sequence matters. Wait for their reply before drafting Case B, and send them the
preprint before submission. Neither is required; both are right.

## 6. What this is not

Not a paper about our preprint being wrong. That is a bioRxiv v2 and a corrections
log, both already written, and it should go up independently.

Not a critique of Boccarella et al. Their conclusion survives our test, and the
paper should say so in its abstract.
