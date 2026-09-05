# 05 — Novelty Landscape: What Is Already Published

Literature/novelty reconnaissance for a modelling paper on antibiotic persistence.
Searches run: PubMed (E-utilities), Consensus (Semantic Scholar/Scopus/PubMed/arXiv), bioRxiv, general web.
Date of search: 2026-09-03.

**Grading convention used throughout:** EXACT MATCH / CLOSE / ADJACENT / NOT RELEVANT.
Negative findings are reported plainly. Where I could not find something, I say so.

---

## BLUNT 5-LINE SUMMARY

1. **Q1 (discontinuous biphasic equation): GAP EXISTS — but it is a *narrow* gap.** I could not find a single published paper, in antimicrobial PD, persister modelling, food-microbiology inactivation, or disinfection kinetics, that uses the specific *discontinuous* two-branch form. Every standard "additive tail" model (Geeraerd, Cerf, Albert-Mafart) is a single continuous expression. **This is an idiosyncratic error, not a widespread practice — a standalone technical comment is NOT warranted.**
2. **Q2 (identifiability of biphasic/two-subpopulation kill models): GAP EXISTS (largely).** The nearest prior art is Galvanin et al. 2013 (J Pharmacokinet Pharmacodyn), which does practical identifiability + MBDoE on antibacterial two-subpopulation *resistance* models. No one has published structural/practical identifiability for a *persister/dormancy* biphasic time-kill model under realistic sparse CFU sampling with a detection floor.
3. **Q3 (optimal experimental design for time-kill curves): ALREADY DONE — but only in grey literature.** Kristoffersson, Hooker, Karlsson & Friberg (PAGE 2011, Abstract 2243) did exactly this: PopED optimal design on the Nielsen two-subpopulation (growing + resting/persister) model, optimising sampling times and concentrations, cutting 9 unique sampling points to 5 (7 with autocorrelation). **It was never published as a journal paper** — it exists only as a PAGE abstract and a chapter of Kristoffersson's 2016 Uppsala thesis. A pure "optimal design for time-kill" paper is therefore *not* novel in substance, though the peer-reviewed niche is technically vacant.
4. **Q4 (resuscitation rate governs time to sterilisation): PARTIALLY DONE — split the claim.** As a *mechanism* it is already published and must not be claimed as new: Patra & Klumpp 2013 derives analytically that the wake-up rate `b` sits inside the expression for the fast→slow switch time, and the whole Cogan pulse-dosing corpus runs on it. As a *quantitative global-sensitivity result on time-to-sterilisation*, **nothing exists** — I found no Sobol/Morris/eFAST/PRCC analysis of any persister PD model reporting the dominant parameter for eradication time.
5. **Overall:** the defensible contribution is **Q2 — practical identifiability of persister time-kill parameters under realistic sampling and CFU censoring** — with Q3's design consequences as its second half. Q1 belongs inside that paper as a methods paragraph, not as its own technical comment. **Warning: Q3 alone is not novel** (Kristoffersson 2011); it must be positioned as "identifiability first, design as the remedy," and it must cite the PAGE abstract explicitly or a Uppsala-adjacent reviewer will flag the omission.

---

# Q1. Is the specific discontinuous biphasic killing equation used elsewhere?

## The equation in question

```
N(t) = N0 * exp(-k_fast * t)                          for t <  t_c
N(t) = N_d + (N0 - N_d) * exp(-k_slow * (t - t_c))    for t >= t_c
```

**The flaw.** At `t = t_c⁻` the value is `N0*exp(-k_fast*t_c)`. At `t = t_c⁺` the value is `N_d + (N0 - N_d) = N0`.
So the population **jumps discontinuously back up to the full inoculum `N0`** at the breakpoint — it recovers everything the fast phase just killed. The jump magnitude is `N0*(1 - exp(-k_fast*t_c))`, i.e. essentially the entire fast-phase kill. This is not a small numerical artefact; it is a structural error that makes the second branch independent of `k_fast` entirely.

## VERDICT: **GAP EXISTS — the form is not in the published literature.**

I searched antimicrobial pharmacodynamics, persister modelling, time-kill curve fitting, food-microbiology inactivation ("tail" models), and water-disinfection kinetics. **I could not find any published paper using this discontinuous form.** Every closely-related published model is continuous. The details:

### 1a. The food-microbiology "tail" models are ALL single continuous expressions

This directly answers the question posed in the brief. Verified against the predictive-microbiology review (Pérez-Rodríguez / "A Focus on the Death Kinetics in Predictive Microbiology", PMC5224560) and the GInaFiT model guide:

| Model | Equation (as published) | Piecewise? | Continuous? |
|---|---|---|---|
| **Geeraerd shoulder+tail** | `N(t) = (N0 − Nres)·e^(−kmax·t)·[e^(kmax·SL) / (1 + (e^(kmax·SL) − 1)·e^(−kmax·t))] + Nres` | **No** — one expression, all t | Yes (=N0 at t=0) |
| **Geeraerd log-linear + tail** (SL=0) | `N(t) = (N0 − Nres)·e^(−kmax·t) + Nres` | **No** | Yes |
| **Cerf biphasic** | `y = y0 + log[f·e^(−kmax1·t) + (1 − f)·e^(−kmax2·t)]` | **No** — sum of exponentials, both phases run simultaneously | Yes |
| **Mafart/Weibull** | `log N = log N0 − (t/δ)^p` | **No** | Yes |
| **Albert–Mafart Weibull + tail** | `log N = log[(N0 − Nres)·10^(−(t/δ)^p) + Nres]` | **No** | Yes |

**Key point for the paper:** the Geeraerd log-linear+tail form `(N0 − Nres)·e^(−kt) + Nres` is the *legitimate* additive-residual model. It looks superficially like the second branch of the flawed equation, but there is no breakpoint and no time shift, so it starts at exactly `N0`. The flawed equation is what you get if you take this and bolt a shifted breakpoint onto it without renormalising the constant.

### 1b. The correctly-formulated antibiotic-persistence counterpart exists (and is recent)

**Alexandersen NR, Nielsen KL, Häussler S, Bjarnsholt T, Schønning K. (2025)** "Antibiotic tolerance and persistence in clinical isolates of *Escherichia coli* evaluated by high-resolution time-kill assays." *Microbiology Spectrum* 13(9):e0112425. **PMID 40772932**, DOI [10.1128/spectrum.01124-25](https://doi.org/10.1128/spectrum.01124-25).

Their model (reconstructed from the PMC full text, PMC12403604) is:

```
N = N0 * [ p * e^(-k1*(t - T0)) + (1 - p) * e^(-k2*(t - T0)) ]        for t >= T0
N = N0                                                                for t <  T0
```

where `T0` = duration of the initial bacteriostatic phase, `k1` = fast kill rate, `k2` = slow kill rate, `p` = fraction undergoing rapid killing.

**This is the single most important comparator for Q1.** It is:
- a **breakpoint model with a time shift `(t − T0)`** — structurally the closest published thing to your equation;
- but it is a **continuous mixture (Cerf form) shifted in time**, so at `t = T0` it evaluates to `N0·(p + 1 − p) = N0`, matching the plateau branch exactly. **No jump.**
- It reports parameter precision (mean CV: 0.16 for T0, 0.27 for k1, 0.28 for k2, <0.01 for p in β-lactams; 0.38/0.73/<0.01 for ciprofloxacin) — note the **k2 CV of 0.73 for ciprofloxacin**, which is itself informal evidence of the practical-identifiability problem in Q2.
- Sampling design: 0, 15, 30, 45, 60, 75, 90, 120, 180, 240, 360, 480 min (12 points), deliberately dense early.

Grade: **CLOSE** (same intent, correct formulation).

### 1c. The likely *origin* of the flawed form — a misapplied GraphPad Prism template

This is a useful diagnostic finding. GraphPad Prism ships a built-in equation, **"Plateau followed by one phase decay"**:

```
Y = IF( X < X0,  Y0,  Plateau + (Y0 - Plateau)*exp(-K*(X - X0)) )
```

This is *structurally identical* to the flawed equation — two branches, a breakpoint `X0`, an additive plateau term — **and it is continuous**, precisely because branch 1 is a *flat plateau at `Y0`*, so both branches give `Y0` at `X = X0`.

The flawed equation is what results if branch 1's flat plateau `Y0` is replaced by a decaying `N0·exp(−k_fast·t)` **while leaving `N0` as the constant in branch 2**. The discontinuity is exactly the deviation introduced by that substitution.

(Prism's actual biphasic tool, **"Two phase decay"**, is `Y = Plateau + SpanFast·exp(−Kfast·X) + SpanSlow·exp(−Kslow·X)` — a continuous sum, with Prism's own documentation stressing that *"the two phases are both happening at all time points"*, i.e. sequential-branch thinking is explicitly not what that model does.)

### 1d. Piecewise breakpoint models DO exist in environmental decay — but log-linear and continuous, and already criticised

**Brouwer AF, Eisenberg MC, Remais JV, Collender PA, Meza R, Eisenberg JNS. (2017)** "Modeling Biphasic Environmental Decay of Pathogens and Implications for Risk Analysis." *Environ Sci Technol* 51(4):2186–2196. **PMID 28112914**, DOI [10.1021/acs.est.6b04030](https://doi.org/10.1021/acs.est.6b04030).

- Their preferred model is the **continuous biexponential** `E(t) = a·c·e^(−at) + b·(1−c)·e^(−bt)`.
- They **explicitly contrast this with a "piecewise log-linear model" with a breakpoint `t*`** and argue the mechanistic biexponential "should be preferred to purely empirical models."
- Critically, the piecewise log-linear alternative is **two joined straight lines in log space — continuous by construction, and with no additive residual term.**

Grade: **ADJACENT.** It establishes that (i) breakpoint models are known in the wider inactivation literature, (ii) they are continuous, and (iii) a published critique of empirical breakpoint models already exists in a neighbouring field. Useful to cite; does not contain your equation.

### 1e. Systematic negative evidence

**Minichmayr IK, Aranzana-Climent V, Friberg LE. (2022)** "Pharmacokinetic/pharmacodynamic models for time courses of antibiotic effects." *Int J Antimicrob Agents* 60(3):106616. **PMID 35691605**, DOI [10.1016/j.ijantimicag.2022.106616](https://doi.org/10.1016/j.ijantimicag.2022.106616).

This is a **systematic review of 132 published antibacterial PKPD models (1963–2021)** with an interactive searchable table of every model's structural elements. The dominant paradigm throughout is **coupled ODE systems** (susceptible/resting/persister compartments with transfer rates), not closed-form piecewise algebraic fits. **No discontinuous closed-form biphasic model appears in this corpus.** This is the strongest single piece of negative evidence available: if the form were in common use, it would be in that table.

### Q1 bottom line

> **Is this a widely used form worth a technical comment? No.** It is an idiosyncratic error. The nearest published relatives are all continuous. I found no second user of this equation anywhere.
>
> **Recommendation:** do NOT write a standalone technical comment. Treat the discontinuity as a short *methods/limitations* observation inside the identifiability paper — "closed-form breakpoint parameterisations of biphasic kill are easy to mis-specify; here is the continuity constraint they must satisfy" — cite Alexandersen 2025 as the correct construction, the Geeraerd/Cerf family as the continuous standard, and Brouwer 2017 as the precedent for preferring mechanistic over empirical breakpoint models. That is a real and useful contribution; a whole paper about one preprint's algebra is not.
>
> **Note on provenance:** the 2025 bioRxiv preprint referred to in the brief is **Piranfar V. (2025)** "Comparative Modeling of Antibiotic Resistance, Tolerance, and Persistence in *Mycobacterium tuberculosis* and *Staphylococcus aureus*", bioRxiv, posted 14 Feb 2025, DOI [10.1101/2025.02.12.637810](https://doi.org/10.1101/2025.02.12.637810). Its parameters (`k_fast`, `k_slow`, `N_d`, `t_c`) match the equation in the brief exactly; transition times reported are ~12 h (*S. aureus*) and ~80 h (*M. tuberculosis*). The equations themselves are embedded as images in the preprint and could not be extracted verbatim by automated fetch — **confirm the exact rendered form against the source before publishing any claim about it.**

---

# Q2. Structural / practical identifiability for biphasic two-subpopulation kill models?

## VERDICT: **GAP EXISTS (largely) — with one important piece of near-prior-art.**

### 2a. The closest prior art — and it is close enough that you must cite and distinguish it

**Galvanin F, Ballan CC, Barolo M, Bezzo F. (2013)** "A general model-based design of experiments approach to achieve practical identifiability of pharmacokinetic and pharmacodynamic models." *J Pharmacokinet Pharmacodyn* 40(4):451–467. **PMID 23733369**, DOI [10.1007/s10928-013-9321-5](https://doi.org/10.1007/s10928-013-9321-5).

- Couples **numerical structural identifiability assessment** with **model-based design of experiments (MBDoE)** to achieve **practical identifiability**.
- **Both case studies are in vitro bacterial growth and killing models.** Per secondary sources, these are based on **Tam et al.** (bacterial killing with an adaptation function) and **Campion et al.** (two bacterial subpopulations capturing resistance).
- Grade: **CLOSE for methodology, ADJACENT for subject matter.**
- **Critical distinction to draw:** the two subpopulations there are a **resistance** construct (susceptible + resistant mutants, with a heritable adaptation/`C50k` drift), not a **persistence/dormancy** construct (phenotypic switching, reversible, non-heritable). The parameters at issue are `Emax`/`C50k`/adaptation rate — **not** persister fraction and transition time. Also: I could **not** obtain the full text (Springer paywall, ResearchGate 403), so the precise list of unidentifiable parameters is **unverified**. **Get this paper before writing.**

**Ballan CC, Galvanin F, Barolo M, Bezzo F. (2012)** "Parallel design of pharmacodynamic experiments for the identification of antimicrobial-resistant bacterial population models." *Computer Aided Chemical Engineering* 31:1125–1129. (Conference proceedings; no PMID. Record: research.unipd.it/handle/11577/2523615.)
- Explicitly states that complex PK-PD resistance models "are usually affected by identifiability issues typically related to their specific model structure and strong correlation among model parameters," and uses MBDoE with parallel experiments to fix it.
- Grade: **CLOSE** (methodologically), **ADJACENT** (resistance, not persistence). Low visibility venue — easy to overlook, so worth citing to show diligence.

### 2b. What I searched for and did NOT find

I ran PubMed queries combining `"structural identifiability"` / `"practical identifiability"` / `"profile likelihood"` with bacteria/antibiotic/antimicrobial/microbial. **Total corpus: 21 papers.** Of those, essentially **none** concern antibiotic time-kill or persister models. The corpus breaks down as:

- **Microbial community / Lotka-Volterra ecology:** Díaz-Seoane, Sellán & Villaverde 2023, *Bioengineering* 10(4):483, PMID 37106670; Remien, Eckwright & Ridenhour 2021, *R Soc Open Sci* 8(7):201378, PMID 34295510; Paredes-Vázquez, Balsa-Canto & Banga 2025, *PLoS Comput Biol* 21(12):e1013204, PMID 41325459.
- **Wastewater / bioreactor kinetics:** Zonta et al. 2012, *Water Res* 47(3):1369, PMID 23276428; Domingo-Félez et al. 2016, *Biotechnol Bioeng* 114(1):132, PMID 27477588; Ben Youssef & Zepeda 2023, PMID 36630048.
- **Metabolic flux:** Kappelmann, Wiechert & Noack 2015, *Biotechnol Bioeng* 113(3):661, PMID 26375179.
- **QMRA dose-response:** Schmidt, Emelko & Thompson 2019, *Risk Anal* 40(2):352, PMID 31441953 — a good general cautionary citation ("misleading models can still have great fit"), but on *E. coli* O157:H7 / norovirus dose-response, **not** kill kinetics.
- **Phage-bacteria:** Phan et al. 2026, *Bull Math Biol* 88(9), PMID 42622694 — uses profile likelihood on a gLV phage-resistance model. **ADJACENT.**
- **Methods:** Joubert, Stigter & Molenaar 2020, *Math Biosci* 323:108328, PMID 32171772 (re-parametrisation of unidentifiable models; one example is a generic microbial growth model).

> **I could not find any paper that asks whether `k_fast`, `k_slow`, the persister fraction `p`, and the transition time `t_c` are identifiable from a typical time-kill sampling design.** That is the gap.

### 2c. The theoretical result you will need to confront head-on

The classical identifiability result for a sum of two exponentials observed only in aggregate: **the rate constants are recoverable as an *unordered pair*, but the assignment of each rate to its subpopulation is not identifiable** (label-swapping non-identifiability). Combined with the amplitude/rate trade-off, this means:

- **Structural identifiability of the biphasic mixture is essentially a solved, classical problem** — you will not get a novel structural result from `p·e^(−k1·t) + (1−p)·e^(−k2·t)` alone. Claiming otherwise would be a re-tread and reviewers will catch it.
- **The genuinely novel territory is PRACTICAL identifiability under realistic experimental conditions:** sparse sampling, log-normal CFU counting noise, plating replication, and — most importantly — the **CFU detection floor / left-censoring**, which truncates exactly the slow phase from which `k_slow` and `p` must be estimated. Alexandersen 2025's ciprofloxacin CV of 0.73 on `k_slow` is empirical evidence this bites in practice.
- Adding the breakpoint `t_c` as a *free* parameter (rather than the fixed-plateau `T0` of Alexandersen) is where new structural results may actually be available, since a free breakpoint interacts with `k_fast` and `p` in a way the pure mixture does not.

### Q2 bottom line

> **GAP EXISTS.** An identifiability-focused paper on persister time-kill parameters would be novel, **provided** it (a) is framed around *practical* identifiability with censoring and realistic noise, not a structural re-derivation of the two-exponential result; (b) cites and clearly distinguishes Galvanin 2013 and Ballan 2012; (c) uses profile likelihood, which is the expected standard in this space.

---

# Q3. Optimal experimental design for time-kill curves?

## VERDICT: **ALREADY DONE — in grey literature only.**

### 3a. THE DECISIVE FINDING — this exact study exists, but was never published as a paper

**Kristoffersson A, Hooker A, Karlsson MO, Friberg LE. (2011)** "Optimal design of in vitro time kill curve experiments for the evaluation of antibiotic effects." *PAGE 20*, Abstract 2243. Department of Pharmaceutical Biosciences, Uppsala University. (page-meeting.org/?abstract=2243)

This is **exactly the study described in Q3**:
- Implements the **Nielsen 2007 semi-mechanistic PKPD model — which contains the growing + resting (persister) two-subpopulation structure** — in **PopED** optimal design software.
- Optimises **both** the sampling schedule (number and placement of time points) **and** the antibiotic concentrations.
- Original design: 9 unique sampling points at 9–10 concentrations, across five antibiotics.
- **Result: the optimal design reduces this to 5 unique sampling points — 7 once AR(1) residual autocorrelation is accounted for** (autocorrelation half-life estimated at 7.5 h for 24 h experiments, implemented in NONMEM 7). Efficiency 102% (autocorrelation-naive design evaluated against autocorrelated model) vs 120% (autocorrelation-aware).
- Conclusion: "increased power at decreased experimental cost by a reduction of sampling points", yielding a generalised design applicable across antibiotic classes.
- **No identifiability analysis is mentioned in the abstract.**

Grade: **EXACT MATCH for Q3.**

**Publication status — this is the crucial nuance.** I searched all 12 PubMed-indexed Kristoffersson AN papers and found **no journal version**. The work appears only as this PAGE abstract and as a chapter of Kristoffersson's 2016 Uppsala thesis (*Study Design and Dose Regimen Evaluation of Antibiotics based on Pharmacokinetic and Pharmacodynamic Modelling*, Acta Universitatis Upsaliensis; DiVA diva2:917780), where it is listed as a manuscript. So:
- The peer-reviewed journal niche is **technically vacant**;
- but the **idea, method, model and headline number are all already in the community's hands**, from the single most authoritative group in antibacterial pharmacometrics (Friberg/Karlsson/Hooker — also the authors of PopED and of the Nielsen model itself).
- **A paper claiming to be the first optimal design for time-kill sampling would be wrong, and these authors are highly likely to be reviewers.**

### 3b. Formal model-based DoE on antibacterial killing models — also already published

- **Galvanin et al. 2013**, PMID 23733369 (above). Formal MBDoE applied to in vitro bacterial growth/killing models, optimising experimental settings to secure practical identifiability. **This is the paper that most threatens a pure "optimal design for time-kill" claim.**
- **Ballan et al. 2012**, *Comput Aided Chem Eng* 31:1125–1129 (above). MBDoE designing *parallel simultaneous* experiments for antimicrobial-resistant bacterial population models.

### 3c. Formal optimal design for bacterial infection dynamics — published, but in vivo and tagged-strain

**Vlazaki M, Price DJ, Restif O. (2020)** "An experimental design tool to optimize inference precision in data-driven mathematical models of bacterial infections." *J R Soc Interface* 17(173):20200717. **PMID 33323052**, DOI [10.1098/rsif.2020.0717](https://doi.org/10.1098/rsif.2020.0717).
- Optimises exactly the three things your Q3 asks about: **number of biological replicates, sampling timepoint selection**, and number of tag copies. Establishes the link between the optimality criterion and CI width by simulation.
- **But:** in vivo isogenic-tagged-strain (WITS) infection models, host-to-host dynamics, likelihood-free inference. **No antibiotic, no persister subpopulation, no in vitro time-kill.**
- Grade: **ADJACENT but methodologically the closest template.** Cite it; it is the paper a reviewer will ask "how is yours different?" about.

### 3d. Heuristic (non-formal) design guidance for time-kill studies — published

**Sy SKB, Derendorf H. (2017)** "Experimental design and modelling approach to evaluate efficacy of β-lactam/β-lactamase inhibitor combinations." *Clin Microbiol Infect* 24(7):707–715. **PMID 28760708**, DOI [10.1016/j.cmi.2017.07.020](https://doi.org/10.1016/j.cmi.2017.07.020).
- Recommends an "agile matrix" of two-drug concentration combinations spanning 0.25–4× MIC, arguing it "can save substantial costs and resources, without sacrificing crucial information needed for model development."
- **This is design advice on the CONCENTRATION axis, arrived at heuristically — not Fisher-information-based, and it says nothing about sampling times.**
- Grade: **ADJACENT.**

### 3e. What I searched for and did NOT find

- PubMed `("optimal design" OR "design of experiments" OR "Fisher information") AND (J Pharmacokinet Pharmacodyn OR CPT:PSP) AND bacteria*` returned **only 4 hits**, of which the only relevant one is Galvanin 2013. (Kristoffersson, Friberg & Nyberg 2015, *J Pharmacokinet Pharmacodyn* 42(6):735, PMID 26452548, is inter-occasion variability in individual optimal design — colistin **PK**, not time-kill PD. NOT RELEVANT.)
- PubMed `("experimental design" OR "study design" OR "optimal")[Title] AND "time-kill"` returned **16 hits**, essentially **all of which are optimal *dosing regimen* studies, not optimal *sampling* studies** (e.g. Srivastava et al. 2016 AAC amikacin HFS-TB PMID 27458215; Kim et al. 2021 AAC three-drug TB PMID 34339275; Lim et al. 2014 vancomycin PMID 24428720).
- Hollow-fibre infection model literature (incl. the JAC systematic review of HFIM reporting) discusses sampling *practice* and AIC-based model selection, but **I found no Fisher-information or D-optimal sampling design for HFIM.**

> In the **peer-reviewed journal literature** I could not find a paper asking: how many CFU sampling times, placed where, at how many antibiotic concentrations, are needed to estimate persister-model parameters. **But the PAGE 2011 abstract in §3a answers precisely that question**, so the journal-literature gap is a documentation gap, not a knowledge gap.

### Q3 bottom line

> **ALREADY DONE (grey literature).** Kristoffersson et al. 2011 did this study, on a model that already contains the persister compartment, and got a concrete answer (5–7 sampling points). It never reached a journal.
>
> **Consequences for the paper:**
> - Do **not** pitch a standalone "optimal design for time-kill curves" paper. It is not novel in substance, and the people who did it are the field's referees.
> - **Do** cite Kristoffersson 2011 explicitly and prominently. Omitting it would look either uninformed or evasive.
> - The viable framing is **Q2-led**: *identifiability* is the contribution; the design recommendation is the remedy that follows from it. That is genuinely additive, because Kristoffersson's abstract explicitly contains **no identifiability analysis**, and because a design optimised for D-efficiency of the whole parameter vector is not the same as a design that rescues specifically the poorly-identified persister parameters under CFU censoring.
> - A second genuinely additive angle: Kristoffersson found **residual autocorrelation dominates the design** (half-life 7.5 h). Nobody has examined what autocorrelation plus a left-censored detection floor jointly do to persister-parameter identifiability.

---

# Q4. Is "resuscitation rate from dormancy governs time to sterilisation" already published?

## VERDICT: **PARTIALLY DONE — the mechanism is already published; the quantitative ranked result is not.**

Split the claim in two, because the two halves have opposite verdicts.

### 4a. As a qualitative mechanism: **ALREADY DONE. Do not claim this as a discovery.**

The fact that the persister→normal reversion (wake-up) rate `b` sets the slow phase of biphasic killing, and therefore the tail of eradication, is **analytically explicit** in the published literature:

**Patra P, Klumpp S. (2013)** "Population dynamics of bacterial persistence." *PLoS One* 8(5):e62814. **PMID 23675428**, DOI [10.1371/journal.pone.0062814](https://doi.org/10.1371/journal.pone.0062814).
- **This is the single closest published statement and the biggest threat to the claim.** In a Balaban-type two-state model they derive in closed form that the fast→slow switch time is `t = ln(N₀/P₀)/(μₙ − μₚ + b)` — the wake-up rate `b` appears directly in the expression governing the killing timescale, and `b` sets the asymptotic decay of the surviving population under antibiotic.
- Grade: **CLOSE.** Framed as "population dynamics of persistence"; no sensitivity analysis, no parameter ranking, no time-to-sterilisation framing.

**Balaban NQ, Merrin J, Chait R, Kowalik L, Leibler S. (2004)** "Bacterial persistence as a phenotypic switch." *Science* 305(5690):1622–1625. **PMID 15308767**, DOI [10.1126/science.1099390](https://doi.org/10.1126/science.1099390).
- In the originating model, persisters die only after waking, so **the slow-phase slope of the biphasic kill curve *is* the wake-up rate**. Balaban et al. use exactly this to *estimate* `b` from kill curves. The identity is baked into the model everyone has used since.
- Grade: **CLOSE.**

**The entire Cogan / De Leenheer pulse-dosing corpus operates on this premise.** Its central result — that cycling antibiotic on/off eradicates faster than continuous exposure — exists *because* persisters must wake to be killed:
- De Leenheer P, Cogan NG. (2009) *J Math Biol* 59(4):563–579. **PMID 19083238**, DOI [10.1007/s00285-008-0243-6](https://doi.org/10.1007/s00285-008-0243-6). Explicitly investigates "how the speed at which the bacteria are wiped out depends on the duration of administration of the antibiotic" — finds non-monotone dependence.
- Cogan NG. (2006) *J Theor Biol* 238(3):694–703. **PMID 16125727**, DOI [10.1016/j.jtbi.2005.06.017](https://doi.org/10.1016/j.jtbi.2005.06.017).
- Cogan NG, Brown J, Darres K, Petty K. (2012) *Antimicrob Agents Chemother* 56(9):4816–4826. **PMID 22751538**, DOI [10.1128/AAC.00675-12](https://doi.org/10.1128/AAC.00675-12). "Cycling between application and withdrawal of the antibiotic yields the fastest killing."
- Cogan NG, Rath H, Kommerein N, Stumpp SN, Stiesch M. (2016) *FEMS Microbiol Lett* 363(23). **PMID 27915255**, DOI [10.1093/femsle/fnw264](https://doi.org/10.1093/femsle/fnw264). Model-predicted timing validated experimentally on *S. aureus* biofilms.
- Review of the class: Cogan NG. (2013) *Math Biosci* 245(2):111–125. **PMID 23891584**, DOI [10.1016/j.mbs.2013.07.007](https://doi.org/10.1016/j.mbs.2013.07.007).

**Carvalho G, Balestrino D, Forestier C, Mathias JD. (2018)** "How do environment-dependent switching rates between susceptible and persister cells affect the dynamics of biofilms faced with antibiotics?" *npj Biofilms Microbiomes* 4:6. **PMID 29560270**, DOI [10.1038/s41522-018-0049-2](https://doi.org/10.1038/s41522-018-0049-2).
- States directly that "the decay of the persister population during antibiotic treatments was mainly due to the wake-up of persisters."
- Grade: **CLOSE** on mechanism; it is a three-strategy scenario comparison, not a sensitivity ranking, and the outcome variable is biofilm survival/recovery rather than time-to-sterilisation.

### 4b. As a quantitative, globally-ranked sensitivity result: **GAP EXISTS.**

> **NEGATIVE FINDING (important):** I could not find a single paper performing **Sobol, Morris, eFAST, or LHS/PRCC global sensitivity analysis on a persister / antibiotic-persistence pharmacodynamic model and reporting which parameter dominates time-to-sterilisation or eradication time.** A sweep of 61 PubMed hits for `(persister OR persistence OR dormant OR biofilm) AND (Sobol OR eFAST OR PRCC OR "Latin hypercube" OR "global sensitivity analysis")` returned only unrelated epidemiological, oncology and bioreactor models. Web search returned nothing either.

Nearest neighbours:
- **Marino S, Hogue IB, Ray CJ, Kirschner DE. (2008)** "A methodology for performing global uncertainty and sensitivity analysis in systems biology." *J Theor Biol* 254(1):178–196. **PMID 18572196**, DOI [10.1016/j.jtbi.2008.04.011](https://doi.org/10.1016/j.jtbi.2008.04.011). The canonical LHS/PRCC + eFAST methods paper — this is what you would cite for the method. Its TB granuloma-ABM descendants run LHS/PRCC on **granuloma outcome / bacterial load** and report the **intracellular bacterial growth rate** as the top correlate — *not* dormancy-exit rate, and *not* on time-to-sterilisation.
- Cogan's group does use Sobol', but on non-persister problems (e.g. Jarrett AM & Cogan NG 2019, *Math Med Biol* 36(2):157–177, **PMID 29767719** — *S. aureus* nasal carriage, output is carriage oscillation).

### 4c. The HIV "shock and kill" structural analogue — checked deliberately; does NOT pre-empt

This is the obvious structural analogue and a referee will raise it, so it was searched specifically. **It does not contain the claim in your form:**
- **Hill AL, Rosenbloom DIS, Fu F, Nowak MA, Siliciano RF. (2014)** *PNAS* 111(37):13475–13480. **PMID 25097264**, DOI [10.1073/pnas.1406663111](https://doi.org/10.1073/pnas.1406663111). Governing quantity is **reservoir size** (~2,000-fold reduction for 1 y), not activation rate.
- **Ke R, Conway JM, Margolis DM, Perelson AS. (2018)** *JCI Insight* 3(20):e123052. **PMID 30333308**, DOI [10.1172/jci.insight.123052](https://doi.org/10.1172/jci.insight.123052). The closest analogue: finds the **duration of antigen expression (the "period of vulnerability")** plus clearance rate govern latency-reversing-agent efficacy — i.e. *the window during which an awakened cell is killable*, not the awakening rate itself. **Cite this defensively.**

### 4d. Competing explanations you must distinguish

**Martinecz A, Abel zur Wiesch P. (2018)** "Estimating treatment prolongation for persistent infections." *Pathog Dis* 76(6):fty065. DOI [10.1093/femspd/fty065](https://doi.org/10.1093/femspd/fty065).
- Asks exactly your question — what prolongs treatment — but answers it with **heterogeneity in drug-target binding / efflux numbers**, not switching or wake-up rates. **An explicit competing explanation for the same phenomenon.** Cite and distinguish.

**Magombedze G, Pasipanodya JG, Gumbo T. (2021)** "Bacterial load slopes represent biomarkers of tuberculosis therapy success, failure, and relapse." *Commun Biol* 4:664. **PMID 34079045**, DOI [10.1038/s42003-021-02184-0](https://doi.org/10.1038/s42003-021-02184-0).
- Two-subpopulation TB model; treatment duration computed as **time-to-extinction of all subpopulations** — structurally the same output metric you want. But their driver is the **kill rate of the slow subpopulation (γs)**, not its awakening rate. **ADJACENT, and directly in tension with the claim.**

**Fang X, Brynildsen MP et al. (2023)** "Resuscitation dynamics reveal persister partitioning after antibiotic treatment." *Mol Syst Biol* 19:e11320. DOI [10.15252/msb.202211320](https://doi.org/10.15252/msb.202211320).
- Persisters resuscitate **exponentially, not stochastically** — challenges the constant-`b` assumption your model would rest on. **A modelling-assumption caveat you must address.**

**Şimşek E, Kim M. (2019)** *PNAS* 116(36):17635–17640. **PMID 31427535**, DOI [10.1073/pnas.1903836116](https://doi.org/10.1073/pnas.1903836116). Persister lag-time (awakening-time) distribution has a **power-law tail** — again undermines a single constant `b`. Supportive background for "awakening sets the tail", but the output is kill-curve shape, not eradication time.

**Jõers A, Kaldalu N, Tenson T. (2010)** *J Bacteriol* 192(13):3379–3384. **PMID 20435730**, DOI [10.1128/JB.00056-10](https://doi.org/10.1128/JB.00056-10). Experimental: death rate depends on how fast stationary-phase cells wake. Foundational empirical support.

### 4e. Checked and found NOT to make the claim

- **Singh G, Orman MA, Conrad JC, Nikolaou M. (2023)** "Systematic design of pulse dosing to eradicate persister bacteria." *PLoS Comput Biol* 19(1):e1010243. DOI [10.1371/journal.pcbi.1010243](https://doi.org/10.1371/journal.pcbi.1010243). Eradication criterion depends on the **ratio of on/off durations** and kill-rate ratios Rₙ, Rₚ — **not** explicitly on the reversion rate `b`.
- **Ankomah P, Levin BR. (2014)** *PNAS* 111(23):8331–8338. **PMID 24843148**. Outputs include time-to-clearance, but the drivers examined are dose, frequency and term — not dormancy exit.
- **Levin BR, Rozen DE. (2006)** *Nat Rev Microbiol* 4(7):556–562. **PMID 16778840**. Closest *verbal* statement in a high-profile venue ("could extend the duration of antibiotic treatment"), but about the *existence* of persisters, not the resuscitation rate as controlling parameter.
- **Rpf (resuscitation-promoting factor) + treatment-shortening model:** **not found.** No modelling paper linking Rpf activity to treatment duration was located.

### Q4 bottom line

> **PARTIALLY DONE.** Frame the contribution as **quantification and parameter ranking**, never as discovery of the mechanism. The sentence "resuscitation rate governs time to sterilisation" as a bare claim will be rejected as known — Patra & Klumpp 2013 derives it analytically. What is genuinely open is a **global (Sobol/eFAST) sensitivity analysis of a persister PD model with time-to-sterilisation as the output**, showing the resuscitation rate dominates and quantifying by how much relative to kill rates and persister fraction.
>
> Three things that must be handled or the paper will be attacked: (i) Magombedze 2021 says the *slow-phase kill rate* is the driver, not awakening; (ii) Martinecz & Abel zur Wiesch 2018 offers a rival mechanism (target binding heterogeneity); (iii) Fang 2023 and Şimşek & Kim 2019 both show resuscitation is **not** a single constant rate, so a constant-`b` model needs explicit defence.
>
> **Self-collision warning:** the Piranfar 2025 bioRxiv preprint already performs a ±10% one-at-a-time (OAT) sensitivity analysis and concludes `k_slow` dominates. A new GSA paper concluding the *resuscitation* rate dominates must explain the relationship to — or supersession of — that earlier OAT result.

---

# BACKGROUND MAP: standard mathematical model structures in the field

All verified in PubMed. This is the landscape a new contribution has to sit inside.

| # | Citation | Structure |
|---|---|---|
| 1 | **Balaban NQ, Merrin J, Chait R, Kowalik L, Leibler S (2004).** *Bacterial persistence as a phenotypic switch.* Science 305(5690):1622–5. PMID 15308767, DOI [10.1126/science.1099390](https://doi.org/10.1126/science.1099390) | The canonical two-state ODE: normal `n` ⇄ persister `p`, switching rates `a` (n→p) and `b` (p→n); each state has its own growth/death rate under drug. **Type I** (triggered, a≈0 in exponential phase) vs **Type II** (spontaneous, constitutive). Every persister model below descends from this. |
| 2 | **Regoes RR, Wiuff C, Zappala RM, Garner KN, Baquero F, Levin BR (2004).** *Pharmacodynamic functions: a multiparameter approach to the design of antibiotic treatment regimens.* AAC 48(10):3670–6. PMID 15388418, DOI [10.1128/AAC.48.10.3670-3676.2004](https://doi.org/10.1128/AAC.48.10.3670-3676.2004) | Not a persister model — the standard **PD function**: net growth ψ(a) as a Hill/Emax function with ψmax, ψmin, zMIC, κ. This is the kill term nearly everyone plugs into persister models. |
| 3 | **Nielsen EI, Viberg A, Löwdin E, Cars O, Karlsson MO, Sandström M (2007).** *Semimechanistic PK/PD model...from time-kill curve experiments.* AAC 51(1):128–36. PMID 17060524, DOI [10.1128/AAC.00604-06](https://doi.org/10.1128/AAC.00604-06) | Two subpopulations: **growing drug-susceptible** + **resting drug-insusceptible**, with transfer between them; drug acts as an Emax increase of the kill rate of the susceptible state only. The workhorse of the pharmacometrics community — and the model used in the Kristoffersson 2011 optimal-design work (Q3). |
| 4 | **Nielsen EI, Friberg LE (2013).** *Pharmacokinetic-pharmacodynamic modeling of antibacterial drugs.* Pharmacol Rev 65(3):1053–90. PMID 23803529, DOI [10.1124/pr.111.005769](https://doi.org/10.1124/pr.111.005769) | The review that catalogues and taxonomises the PKPD structures. **Note the exact title** — not "semi-mechanistic PKPD review"; fix any reference string that says otherwise. |
| 5 | **Lipsitch M, Levin BR (1997).** *The population dynamics of antimicrobial chemotherapy.* AAC 41(2):363–73. PMID 9021193, DOI [10.1128/AAC.41.2.363](https://doi.org/10.1128/AAC.41.2.363) | Sensitive + resistant subpopulations with mutation, host PK and dosing; the founding within-host antibiotic-resistance ODE framework. |
| 6 | **Lipsitch M, Levin BR (1998).** *Population dynamics of tuberculosis treatment...* Int J Tuberc Lung Dis 2(3):187–99. **PMID 9526190 — no DOI in PubMed; cite by PMID.** | TB version: adds a **"protected compartment"** where only one drug is active — the structural ancestor of "special populations" / dormant-subpopulation TB models. |
| 7 | **Cogan NG (2006)** J Theor Biol 238(3):694–703, PMID 16125727 — with **De Leenheer & Cogan (2009)** J Math Biol 59(4):563–79, PMID 19083238, and **Cogan et al. (2012)** AAC 56(9):4816–26, PMID 22751538. Class review: **Cogan (2013)** Math Biosci 245(2):111–25, PMID 23891584 | Susceptible ⇄ persister where the **switch is regulated by growth rate and antibiotic concentration**, in batch and chemostat, with periodic on/off dosing; analyses failure conditions and optimal dose/withdrawal timing. |
| 8 | **Levin BR, Udekwu KI (2010).** *Population dynamics of antibiotic treatment: a mathematical model and hypotheses for time-kill and continuous-culture experiments.* AAC 54(8):3414–26. PMID 20516272, DOI [10.1128/AAC.00381-10](https://doi.org/10.1128/AAC.00381-10) | Resource-limited (Monod) growth + Hill PD + phenotypic tolerance; **the reference model for interpreting time-kill and chemostat data.** Directly relevant to Q1–Q3. |
| 9 | **Ankomah P, Levin BR (2014).** *Exploring the collaboration between antibiotics and the immune response in the treatment of acute, self-limiting infections.* PNAS 111(23):8331–8. PMID 24843148, DOI [10.1073/pnas.1400352111](https://doi.org/10.1073/pnas.1400352111) | Couples PK + Regoes-type PD + innate/adaptive immune killing + resistance evolution; outputs time-to-clearance and P(resistance). |

**Supporting / conceptual (verified):**
- **Kussell E, Leibler S (2005).** *Science* 309(5743):2075–8. PMID 16123265, DOI [10.1126/science.1114383](https://doi.org/10.1126/science.1114383) — bet-hedging theory; optimal switching rates mirror environmental switching statistics.
- **Gefen O, Balaban NQ (2009).** *FEMS Microbiol Rev* 33(4):704–17. PMID 19207742, DOI [10.1111/j.1574-6976.2008.00156.x](https://doi.org/10.1111/j.1574-6976.2008.00156.x) — standard review of the mathematical description of persistence.
- **Marino S, Hogue IB, Ray CJ, Kirschner DE (2008).** *J Theor Biol* 254(1):178–96. PMID 18572196 — the LHS/PRCC + eFAST methodology to cite for any GSA.

**Corrections to the candidate list supplied in the brief:**
- **Katsube** — verified, but it is a *series* (Katsube et al. 2008 *J Pharm Sci* 97(4):1606–14, PMID 17705288; 97(9):4108–17, PMID 18314887; 2014, 103(4):1288–97, PMID 24523230), and **none of it is persister-specific** — concentration-dependent bactericidal PK/PD with no dormant compartment. **Do not list it among standard persistence structures.**
- **"Meredith / Bergstrom" and "Sharma"** — too underspecified to verify; **no standard persistence model-structure paper was found under either name. Do not cite.**
- **Wallis "special populations hypothesis"** — the concept is real, but **no PubMed-indexed Wallis RS paper under that phrase was found. Treat as unverified.**
- **Ankomah & Levin 2014** — the real title is about antibiotic/immune collaboration, not "immune system + antibiotic clearance"; correct the reference string.

---

# CITATION TABLE

| # | Citation | Identifier | Relevance | Grade |
|---|---|---|---|---|
| 1 | Alexandersen NR, Nielsen KL, Häussler S, Bjarnsholt T, Schønning K. (2025) Antibiotic tolerance and persistence in clinical isolates of *E. coli* evaluated by high-resolution time-kill assays. *Microbiol Spectr* 13(9):e0112425 | PMID 40772932 / [10.1128/spectrum.01124-25](https://doi.org/10.1128/spectrum.01124-25) | Q1 — correctly-formulated continuous breakpoint biphasic model; also gives parameter CVs relevant to Q2 | CLOSE |
| 2 | Minichmayr IK, Aranzana-Climent V, Friberg LE. (2022) PK/PD models for time courses of antibiotic effects. *Int J Antimicrob Agents* 60(3):106616 | PMID 35691605 / [10.1016/j.ijantimicag.2022.106616](https://doi.org/10.1016/j.ijantimicag.2022.106616) | Q1 — systematic review of 132 antibacterial PKPD models; strongest negative evidence | ADJACENT |
| 3 | Brouwer AF, Eisenberg MC, Remais JV, Collender PA, Meza R, Eisenberg JNS. (2017) Modeling Biphasic Environmental Decay of Pathogens. *Environ Sci Technol* 51(4):2186–2196 | PMID 28112914 / [10.1021/acs.est.6b04030](https://doi.org/10.1021/acs.est.6b04030) | Q1 — explicitly contrasts continuous biexponential vs piecewise log-linear breakpoint models, prefers the former | ADJACENT |
| 4 | Geeraerd AH, Herremans CH, Van Impe JF. (2000) / Geeraerd, Valdramidis & Van Impe (2005) GInaFiT — shoulder+tail inactivation model | see GInaFiT documentation; equation reproduced in PMC5224560 | Q1 — the canonical additive-residual "tail" model; single continuous expression | ADJACENT |
| 5 | Cerf O. (1977) biphasic inactivation model; Mafart et al. (2002) Weibull; Albert & Mafart (2005) Weibull+tail | equations reproduced in PMC5224560 | Q1 — all continuous; none piecewise | ADJACENT |
| 6 | GraphPad Prism Curve Fitting Guide — "Plateau followed by one phase decay" and "Two phase decay" | graphpad.com/guides/prism/latest/curve-fitting/ | Q1 — probable origin of the mis-specified form; both Prism equations are continuous | ADJACENT |
| 7 | Piranfar V. (2025) Comparative Modeling of Antibiotic Resistance, Tolerance, and Persistence in *M. tuberculosis* and *S. aureus*. bioRxiv, 14 Feb 2025 | [10.1101/2025.02.12.637810](https://doi.org/10.1101/2025.02.12.637810) | Q1 — the preprint in question (parameters k_fast, k_slow, N_d, t_c confirmed; equations embedded as images, form not machine-verified) | — |
| 8 | **Galvanin F, Ballan CC, Barolo M, Bezzo F. (2013)** A general model-based DoE approach to achieve practical identifiability of PK and PD models. *J Pharmacokinet Pharmacodyn* 40(4):451–467 | PMID 23733369 / [10.1007/s10928-013-9321-5](https://doi.org/10.1007/s10928-013-9321-5) | **Q2 AND Q3 — the decisive prior art.** MBDoE + practical identifiability, case studies = in vitro bacterial growth/killing models (resistance, not persistence). Full text not obtained | CLOSE |
| 9 | Ballan CC, Galvanin F, Barolo M, Bezzo F. (2012) Parallel design of pharmacodynamic experiments for identification of antimicrobial-resistant bacterial population models. *Comput Aided Chem Eng* 31:1125–1129 | research.unipd.it/handle/11577/2523615 | Q2/Q3 — MBDoE for antibacterial two-subpopulation models; explicitly cites parameter-correlation identifiability problems | CLOSE |
| 10 | Vlazaki M, Price DJ, Restif O. (2020) An experimental design tool to optimize inference precision in data-driven mathematical models of bacterial infections. *J R Soc Interface* 17(173):20200717 | PMID 33323052 / [10.1098/rsif.2020.0717](https://doi.org/10.1098/rsif.2020.0717) | Q3 — optimises replicates + sampling timepoints for bacterial infection models (in vivo, tagged strains, no antibiotic) | ADJACENT |
| 11 | Sy SKB, Derendorf H. (2017) Experimental design and modelling approach to evaluate efficacy of β-lactam/β-lactamase inhibitor combinations. *Clin Microbiol Infect* 24(7):707–715 | PMID 28760708 / [10.1016/j.cmi.2017.07.020](https://doi.org/10.1016/j.cmi.2017.07.020) | Q3 — heuristic concentration-matrix design for time-kill; not formal optimal design, silent on sampling times | ADJACENT |
| 12 | Schmidt PJ, Emelko MB, Thompson ME. (2019) Recognizing Structural Nonidentifiability: When Experiments Do Not Provide Information About Important Parameters and Misleading Models Can Still Have Great Fit. *Risk Anal* 40(2):352–369 | PMID 31441953 / [10.1111/risa.13386](https://doi.org/10.1111/risa.13386) | Q2 — general cautionary framing (microbial dose-response, not kill kinetics) | ADJACENT |
| 13 | Díaz-Seoane S, Sellán E, Villaverde AF. (2023) Structural Identifiability and Observability of Microbial Community Models. *Bioengineering* 10(4):483 | PMID 37106670 / [10.3390/bioengineering10040483](https://doi.org/10.3390/bioengineering10040483) | Q2 — shows what microbial identifiability work exists (communities, not kill curves) | NOT RELEVANT to persisters |
| 14 | Remien CH, Eckwright MJ, Ridenhour BJ. (2021) Structural identifiability of the generalized Lotka-Volterra model for microbiome studies. *R Soc Open Sci* 8(7):201378 | PMID 34295510 / [10.1098/rsos.201378](https://doi.org/10.1098/rsos.201378) | Q2 — same | NOT RELEVANT to persisters |
| 15 | Paredes-Vázquez A, Balsa-Canto E, Banga JR. (2025) Identification of dynamic models of microbial communities: A workflow addressing identifiability and modeling pitfalls. *PLoS Comput Biol* 21(12):e1013204 | PMID 41325459 / [10.1371/journal.pcbi.1013204](https://doi.org/10.1371/journal.pcbi.1013204) | Q2 — good workflow template (structural + practical + stability + predictive checks) to mirror | ADJACENT |
| 16 | Phan T, Shrestha A, Schow J, Miller CR, Peters TL, Van Leuven JT. (2026) Bacteriophage Density Influences the Rate of Resistance Evolution. *Bull Math Biol* 88(9) | PMID 42622694 / [10.1007/s11538-026-01704-5](https://doi.org/10.1007/s11538-026-01704-5) | Q2 — profile likelihood applied to a bacterial two-subpopulation model (phage resistance) | ADJACENT |
| 17 | Nielsen EI, Viberg A, Löwdin E, Cars O, Karlsson MO, Sandström M. (2007) Semimechanistic PK/PD Model for Assessment of Activity of Antibacterial Agents from Time-Kill Curve Experiments. *AAC* 51(1):128–136 | PMID 17060524 / [10.1128/aac.00604-06](https://doi.org/10.1128/aac.00604-06) | Q1/Q2 — the standard growing+resting two-subpopulation ODE model (see Q4 section model map) | — |
| 18 | Tam VH, Schilling AN, Nikolaou M. (2005) Modelling time–kill studies to discern the pharmacodynamics of meropenem. *J Antimicrob Chemother* 55(5):699–706 | PMID 15772138 / [10.1093/jac/dki086](https://doi.org/10.1093/jac/dki086) | Q2 — the model family used in Galvanin's case study; 8-parameter fit (growth − sigmoidal kill, with adaptation modelled as drift in C50k) | ADJACENT |
| 19 | Bhagunde P, Singh R, Ledesma KR, Chang K-T, Nikolaou M, Tam VH. (2011) Modelling biphasic killing of fluoroquinolones: guiding optimal dosing regimen design. *J Antimicrob Chemother* 66(5):1079–1086 | PMID 21393141 / [10.1093/jac/dkr054](https://doi.org/10.1093/jac/dkr054) | Q1 — "biphasic killing" handled via heterogeneous-population ODEs, NOT a piecewise closed form | ADJACENT |
| 20 | Kristoffersson AN, Friberg LE, Nyberg J. (2015) Inter occasion variability in individual optimal design. *J Pharmacokinet Pharmacodyn* 42(6):735–750 | PMID 26452548 / [10.1007/s10928-015-9449-6](https://doi.org/10.1007/s10928-015-9449-6) | Q3 — checked and excluded: colistin PK, not time-kill PD | NOT RELEVANT |
| **21** | **Kristoffersson A, Hooker A, Karlsson MO, Friberg LE. (2011) Optimal design of in vitro time kill curve experiments for the evaluation of antibiotic effects. PAGE 20, Abstract 2243** | page-meeting.org/?abstract=2243 (no PMID — **conference abstract + 2016 Uppsala thesis chapter only; never published as a journal paper**) | **Q3 — THE DECISIVE PRIOR ART.** PopED optimal design on the Nielsen 2007 growing+resting(persister) model; optimises sampling times AND concentrations; 9 unique sampling points reduced to 5 (7 with AR(1) autocorrelation); efficiency 102% vs 120% | **EXACT MATCH** |
| 22 | Patra P, Klumpp S. (2013) Population dynamics of bacterial persistence. *PLoS One* 8(5):e62814 | PMID 23675428 / [10.1371/journal.pone.0062814](https://doi.org/10.1371/journal.pone.0062814) | **Q4 — the decisive prior art.** Derives analytically that switch time = ln(N₀/P₀)/(μₙ−μₚ+b); wake-up rate b governs the killing timescale | CLOSE |
| 23 | Balaban NQ, Merrin J, Chait R, Kowalik L, Leibler S. (2004) Bacterial persistence as a phenotypic switch. *Science* 305(5690):1622–1625 | PMID 15308767 / [10.1126/science.1099390](https://doi.org/10.1126/science.1099390) | Q4 + model map — slow-phase slope of the biphasic kill curve *is* the wake-up rate | CLOSE |
| 24 | De Leenheer P, Cogan NG. (2009) Failure of antibiotic treatment in microbial populations. *J Math Biol* 59(4):563–579 | PMID 19083238 / [10.1007/s00285-008-0243-6](https://doi.org/10.1007/s00285-008-0243-6) | Q4 — studies how fast bacteria are wiped out as a function of dosing duration; non-monotone | CLOSE |
| 25 | Cogan NG, Brown J, Darres K, Petty K. (2012) Optimal control strategies for disinfection of bacterial populations with persister and susceptible dynamics. *AAC* 56(9):4816–4826 | PMID 22751538 / [10.1128/AAC.00675-12](https://doi.org/10.1128/AAC.00675-12) | Q4 — on/off cycling yields fastest killing; premised on persisters having to wake | CLOSE |
| 26 | Carvalho G, Balestrino D, Forestier C, Mathias JD. (2018) How do environment-dependent switching rates...affect the dynamics of biofilms faced with antibiotics? *npj Biofilms Microbiomes* 4:6 | PMID 29560270 / [10.1038/s41522-018-0049-2](https://doi.org/10.1038/s41522-018-0049-2) | Q4 — "decay of the persister population...mainly due to the wake-up of persisters" | CLOSE |
| 27 | Magombedze G, Pasipanodya JG, Gumbo T. (2021) Bacterial load slopes represent biomarkers of TB therapy success, failure, and relapse. *Commun Biol* 4:664 | PMID 34079045 / [10.1038/s42003-021-02184-0](https://doi.org/10.1038/s42003-021-02184-0) | Q4 — **in tension with the claim:** same time-to-extinction output, but attributes it to slow-subpopulation *kill rate* γs, not awakening | ADJACENT |
| 28 | Martinecz A, Abel zur Wiesch P. (2018) Estimating treatment prolongation for persistent infections. *Pathog Dis* 76(6):fty065 | [10.1093/femspd/fty065](https://doi.org/10.1093/femspd/fty065) | Q4 — **rival explanation:** attributes treatment prolongation to drug-target/efflux heterogeneity, not switching rates | ADJACENT |
| 29 | Fang X, Brynildsen MP et al. (2023) Resuscitation dynamics reveal persister partitioning after antibiotic treatment. *Mol Syst Biol* 19:e11320 | [10.15252/msb.202211320](https://doi.org/10.15252/msb.202211320) | Q4 — **assumption threat:** resuscitation is exponential, not stochastic; undermines constant-b | ADJACENT |
| 30 | Şimşek E, Kim M. (2019) Power-law tail in lag time distribution underlies bacterial persistence. *PNAS* 116(36):17635–17640 | PMID 31427535 / [10.1073/pnas.1903836116](https://doi.org/10.1073/pnas.1903836116) | Q4 — **assumption threat:** awakening-time distribution is power-law tailed, not single-rate | ADJACENT |
| 31 | Ke R, Conway JM, Margolis DM, Perelson AS. (2018) Determinants of the efficacy of HIV latency-reversing agents. *JCI Insight* 3(20):e123052 | PMID 30333308 / [10.1172/jci.insight.123052](https://doi.org/10.1172/jci.insight.123052) | Q4 — closest HIV shock-and-kill analogue; governing quantity is the "period of vulnerability", NOT activation rate. Cite defensively | ADJACENT |
| 32 | Marino S, Hogue IB, Ray CJ, Kirschner DE. (2008) A methodology for performing global uncertainty and sensitivity analysis in systems biology. *J Theor Biol* 254(1):178–196 | PMID 18572196 / [10.1016/j.jtbi.2008.04.011](https://doi.org/10.1016/j.jtbi.2008.04.011) | Q4 — the LHS/PRCC + eFAST method to cite; never applied to persister eradication time | ADJACENT (method) |
| 33 | Levin BR, Udekwu KI. (2010) Population dynamics of antibiotic treatment: a mathematical model and hypotheses for time-kill and continuous-culture experiments. *AAC* 54(8):3414–3426 | PMID 20516272 / [10.1128/AAC.00381-10](https://doi.org/10.1128/AAC.00381-10) | Model map — the reference model for interpreting time-kill data | — |

---

## METHODOLOGICAL CAVEATS

- **Consensus is capped at 3 results per query** on this account, so its coverage here is indicative rather than exhaustive. PubMed and web search carried the load.
- **Two full texts could not be retrieved:** Galvanin et al. 2013 (Springer paywall; ResearchGate 403) and the Piranfar 2025 preprint's equations (embedded as images). **Both should be read directly before the paper is written** — Galvanin because it is the closest prior art for Q2/Q3, and the preprint because the exact rendered equation matters for any claim about it.
- PubMed's query parser ANDs all free-text terms aggressively; long natural-language queries returned 1–2 hits spuriously. All substantive searches here used field tags and OR-groups.
- **Conference proceedings turned out to matter decisively.** A targeted check of page-meeting.org found Kristoffersson et al. 2011 (Abstract 2243), which changed the Q3 verdict from "gap" to "already done". **ACoP, ESCMID/ECCMID and ASM abstracts were NOT systematically searched** — given what PAGE yielded, they should be checked before any novelty claim is finalised, particularly for Q2 (identifiability) and Q4 (sensitivity analysis).
- Q4's global-sensitivity negative finding rests on PubMed + web search. **GSA results are frequently buried in supplementary material and not indexed in titles/abstracts**, so "no paper reports this" is better read as "no paper foregrounds this". The claim of novelty on Q4 is therefore somewhat softer than the search result alone suggests.
