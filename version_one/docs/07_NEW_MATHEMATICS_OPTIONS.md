# 07 — New Mathematics Options: Novelty Reconnaissance

**Date:** 2026-09-03
**Scope:** Five candidate directions for genuinely new mathematics building on a two-compartment (replicating / dormant persister) PD model with Hill concentration–response.
**Method:** PubMed (via NCBI E-utilities), Consensus (Semantic Scholar / Scopus / PubMed / arXiv), and targeted web/publisher retrieval. Literature searched through September 2026.

---

## VERDICT SUMMARY (blunt, 6 lines)

1. **D1 (stochastic extinction with switching): PARTIALLY OPEN.** The extinction mathematics exists (Lohmar–Meerson, Blath, Gunnarsson), and the antibiotic extinction mathematics exists (Coates), but *nobody has joined switching + Hill PD + a real PK profile* to get a probability of sterilisation.
2. **D2 (persistence → resistance evolution): PARTIALLY OPEN, BUT CROWDED AND CLOSING FAST.** Boccarella et al. (MBE, Aug 2026) already did most of it. Only *regimen optimisation under realistic PK* survives. Two established groups (Regoes/Igler at ETH, Uecker) are working this lane right now. **Highest scoop risk of the five.**
3. **D3 (non-Markovian / dormancy depth): PARTIALLY OPEN BUT A TRAP.** The mathematics is 20+ years old in food microbiology, an age-structured antibiotic PDE already exists (De Leenheer 2009), and the binding constraint is parameter identifiability — which Cogan just published on. Needs wet-lab data you do not have.
4. **D4 (persister model → PTA/CFR for a sterilisation endpoint): GENUINELY OPEN.** Nielsen–Friberg built the mechanistic resting-compartment model but computed no PTA; the PTA literature computes stasis/1-log/2-log with deterministic models that *structurally cannot* express a sterilisation probability. Nobody has bridged them.
5. **D5 (optimal control against a switching population): LARGELY SOLVED.** Cogan's group has owned this since 2006 and published again in 2026. Only the stochastic objective (minimise P(relapse), not deterministic biomass) is unclaimed.
6. **RECOMMENDATION: D4, executed as a fusion of D4 + D1.** It is the only direction where you hold a structural advantage (an existing ceftazidime–avibactam Monte Carlo PTA/CFR pipeline), the novelty is real, the data is public, and the two relevant communities (pharmacometrics; branching processes) do not read each other.

---

## D1. Stochastic extinction / probability of sterilisation with phenotype switching

### Verdict: **PARTIALLY OPEN**

### What has been done

The field splits into three streams that have never been joined.

**Stream A — stochastic extinction under antibiotics, no switching.** Coates et al. (eLife 2018) is the landmark. They characterised bacterial clearance as a stochastic extinction event, showed experimentally that bactericidal antibiotics induce population fluctuations, and demonstrated non-zero extinction probability at concentrations previously deemed inefficacious. Their model is a **single-type Markovian birth–death process**. There is no persister compartment, no phenotype switching, and no pharmacokinetics — the drug concentration is constant.

**Stream B — extinction with phenotype switching, no antibiotic pharmacodynamics.** Lohmar & Meerson (Phys Rev E 2011) is the closest mathematical relative to what you would build. They treat exactly the two-population "normals / persisters" system with stochastic switching, apply a WKB approximation to the master equation, and compute the extinction risk and the *optimal path to extinction* under both favourable and adverse conditions. This is genuinely the right machinery. But the "stress" is an abstract parameter — there is no Hill concentration–response, no MIC, no drug, and no time-varying environment driven by a PK profile.

Blath, Hermann & Slowik (J Math Biol 2021) formalise a **2-type branching process** with active/dormant switching embedded in a randomly fluctuating environment, comparing strategies via maximal Lyapunov exponents. Rigorous and directly on-structure, but the object of study is evolutionary fitness of dormancy strategies, not extinction probability under a treatment schedule. Garet, Marchand & Schinazi (arXiv 2011/2012) give two stochastic persistence models with periodic "mass killing" of non-persisters — closer in spirit, but the killing is an idealised instantaneous event, not a pharmacodynamic function.

**Stream C — multi-type branching with switching, but in oncology.** Gunnarsson, De, Leder & Foo (J Theor Biol 2020) build a multi-type branching process with phenotypic switching, derive extinction probabilities by conditioning on the first event and solving the resulting nonlinear system, and use it to reason about drug sequencing. The mathematics you would need is essentially *already written down here* — for cancer, without pharmacokinetics.

**Adjacent.** Czuppon et al. (PLoS Comput Biol 2023) derive analytical survival probabilities for a resistant subpopulation within a stochastic within-host model across density-regulation scenarios and drug modes of action, but has no persisters. Nyhoegen & Uecker (Evol Appl 2024) compute eradication probability under stochastic pharmacodynamics for drug combinations — again no persisters.

### The specific remaining gap

**Nobody has taken a persister-switching multi-type branching process, driven the type-specific kill rates through a Hill function of a clinically realistic time-varying concentration C(t) from a population PK model, and derived either the probability of sterilisation or the distribution of time to extinction.** The required machinery — extinction probabilities for a *time-inhomogeneous* multitype branching process via the backward Kolmogorov ODE system for the probability generating function — is standard, but the composition with a dosing-interval-periodic PK forcing has not been done. The technically interesting sub-question is whether the extinction probability under a periodic PK profile can be characterised via a Floquet/monodromy argument on the pgf system rather than by brute-force simulation.

### Key citations

| Work | Contribution | What it lacks |
|---|---|---|
| Coates et al. 2018, eLife 7:e32976. PMID 29508699, DOI [10.7554/eLife.32976](https://doi.org/10.7554/eLife.32976) | Stochastic clearance of bacteria under antibiotics; Markovian birth–death; experimental validation | No switching, no PK |
| Lohmar & Meerson 2011, Phys Rev E 84:051901. DOI [10.1103/PhysRevE.84.051901](https://doi.org/10.1103/PhysRevE.84.051901) | Normals/persisters switching; WKB on master equation; extinction risk and optimal path | No PD, no PK, abstract stress |
| Blath, Hermann & Slowik 2021, J Math Biol 83:17. PMID 34279717, DOI [10.1007/s00285-021-01639-6](https://doi.org/10.1007/s00285-021-01639-6) | 2-type branching process, active/dormant, random environment, Lyapunov fitness | Fitness not extinction-under-treatment; no drug |
| Gunnarsson, De, Leder & Foo 2020, J Theor Biol 490:110162. DOI [10.1016/j.jtbi.2020.110162](https://doi.org/10.1016/j.jtbi.2020.110162) | Multi-type branching + phenotypic switching; extinction probabilities; drug sequencing | Cancer, not bacteria; no PK |

---

## D2. Coupling persistence to the EVOLUTION of resistance

### Verdict: **PARTIALLY OPEN — but substantially more occupied than expected, and closing fast**

This was flagged as the priority direction. The honest report is that it is the *most* crowded of the five, and that a paper published in August 2026 has already taken the central result.

### What has been done

**The experimental foundation is settled.** Levin-Reisman et al. (Science 2017) showed tolerance precedes resistance in all replicates and supplied a population-genetics model explaining how tolerance boosts the fixation chances of resistance mutations. Liu et al. (Science 2020) extended this to drug combinations, tracking clinical MRSA strains evolving in patients and showing tolerance mutations emerging first, then resistance, *despite* combination treatment. Windels et al. (ISME J 2024) combined high-throughput experimental evolution with a mathematical model of intermittent exposure, and showed the interaction is dose-dependent: at high doses resistance evolution is facilitated by preceding or concurrent persistence mutants; at low doses resistance emerges independently of persistence.

**The modelling is well advanced.** Witzany, Regoes & Igler (Proc R Soc B 2022) built a stochastic population model containing persistence, genetic resistance *and* hypermutation simultaneously, and asked which drives treatment failure. Their answer is sharp and directly relevant to you: persistence causes "hidden" treatment failure at low cell numbers when concentrations suppress resistant growth, persisters regrow after discontinuation and enable resistance evolution *in the absence of drug*, and hypermutation facilitates resistance during treatment but rarely causes failure. Witzany, Rolff, Regoes & Igler (Microbiology 2023) then wrote what is effectively the programme statement for D2: an explicit methodological paper on coupling PKPD models with population-genetics models to find regimens minimising resistance evolution under dynamic selection pressure, including adaptive phenotypes.

**And then the central result was published.** Boccarella et al. (Mol Biol Evol, August 2026) develop an analytical model deriving resistance emergence probabilities by integration, plus a Gillespie-variant stochastic simulation with lineage tracking, explicitly coupling persistence to mutational resistance. They find a trade-off: high persistence gives slow, predictable resistance via common small-effect mutations; low persistence gives faster but less predictable emergence of rare large-effect mutations with higher extinction risk. Persistence facilitates resistance more in small populations than large.

### The specific remaining gap

Read the Boccarella limitations carefully, because they define precisely what is left:

- They **assume fixed persistence levels** — persistence does not itself evolve.
- They assume **the simplest possible drug kinetics** (drug present or absent), explicitly mimicking *in vitro* conditions rather than a realistic pharmacokinetic profile. They name this as a limitation.
- They **do not optimise dosing regimens** — they sweep treatment severity and frequency and report trade-offs, but pose no optimisation problem.
- No genotype-specific epistasis; persister physiology abstracted away.

So the surviving open question is: **given a persister-switching population with mutational resistance, and a clinically admissible regimen space constrained by a real population PK model, find the schedule minimising P(resistance emerges by end of treatment) subject to P(sterilisation) ≥ target.** That is a constrained stochastic optimal-control problem on a multi-type branching process with time-inhomogeneous rates, and it has not been posed, let alone solved.

**But be honest about the risk.** The ETH group (Regoes, Igler — now Manchester) published the framework paper telling everyone to do exactly this, and Boccarella's group is one step away. Uecker's group is adjacent via the combination-therapy eradication-probability work. A small group without a wet lab entering this lane is entering it *behind* two established groups who have the data and have declared intent. Feasibility of the modelling is fine; the risk is publication timing, not tractability.

### Key citations

| Work | Contribution | What it lacks |
|---|---|---|
| Levin-Reisman et al. 2017, Science 355:826–830. PMID 28183996, DOI [10.1126/science.aaj2191](https://doi.org/10.1126/science.aaj2191) | Tolerance precedes and facilitates resistance; population-genetics model | In vitro; no PK; no regimen optimisation |
| Witzany, Regoes & Igler 2022, Proc R Soc B 289:20221300. PMID 36350213, DOI [10.1098/rspb.2022.1300](https://doi.org/10.1098/rspb.2022.1300) | Stochastic model with persistence + resistance + hypermutation; "hidden" failure; relapse routes | No PK profile; no optimisation |
| Witzany, Rolff, Regoes & Igler 2023, Microbiology 169:001368. PMID 37522891, DOI [10.1099/mic.0.001368](https://doi.org/10.1099/mic.0.001368) | Explicit framework for coupling PKPD + population genetics to minimise resistance | Framework proposal, not executed |
| Boccarella et al. 2026, Mol Biol Evol 43(8):msag180. DOI [10.1093/molbev/msag180](https://doi.org/10.1093/molbev/msag180) | Analytic + Gillespie; persistence modulates speed/magnitude/onset of resistance evolution | **Explicitly** no realistic PK; no dosing optimisation; fixed persistence |
| Liu et al. 2020, Science 367:200–204. PMID 31919223, DOI [10.1126/science.aay3041](https://doi.org/10.1126/science.aay3041) | Tolerance promotes resistance *under combinations*; clinical strains | Experimental; model is minimal |
| Windels et al. 2024, ISME J 18:wrae070. DOI [10.1093/ismejo/wrae070](https://doi.org/10.1093/ismejo/wrae070) | Dose- and nutrient-dependence of the persistence→resistance route | In vitro; no PK |

---

## D3. Non-Markovian / structured dormancy (dormancy depth as a continuum)

### Verdict: **PARTIALLY OPEN — but the mathematics largely already exists elsewhere, and this is a trap for a group without wet-lab data**

### What has been done

**The biology has moved decisively toward "depth is real".** Şimşek & Kim (PNAS 2019) is the key quantitative result: normal cells rejuvenate with an **exponential** lag-time distribution (single rate constant), while persisters show a **power-law tail**, which they show arises from a wide distribution of the rate constant itself. They then build a model on this biphasic lag-time distribution and reproduce persistence population dynamics with no ad hoc parameters. Kaplan et al. (Nature 2021) show universal ageing dynamics in regrowth after acute stress, predictable from a random-network model that ignores molecular detail, with slow and heterogeneous recovery. Rotem et al. (Sci Adv 2026, Balaban group) then split growth arrest into two archetypes — *regulated* (protected dormancy) versus *disrupted* (dysregulated, impaired membrane homeostasis) — which resolves conflicting persister characterisations and implies at least a two-mode, not a continuum, structure.

**Crucially, an age-structured antibiotic PDE already exists.** De Leenheer, Dockery, Gedeon & Pilyugin (J Math Biol 2009) study an **age-structured chemostat model** in which senescence is the hypothesised mechanism generating persisters, and prove global stabilisation at a coexistence steady state, persisting under antibiotic below a threshold, with washout globally attracting above it. This is a genuine age-structured PDE with an antibiotic — direct prior art that would have to be cited and superseded.

**And the non-exponential lag mathematics is decades old in food microbiology.** As suspected. Baranyi and colleagues developed stochastic lag-phase models transforming an assumed individual-cell lag distribution into a population growth function via an integral formula; Métris and others systematically fitted normal, lognormal, Gumbel, gamma, Weibull and exponential distributions to individual-cell lag data, with gamma and lognormal generally winning; and inactivation data have been transformed to cumulative individual-cell inactivation-time distributions and fitted the same way. A predictive-microbiology reviewer will know this literature and will ask what is new.

### The specific remaining gap

The unclaimed piece is a model in which a **dormancy-depth coordinate x indexes both the resuscitation hazard r(x) and the drug kill rate k(x, C)**, so that antibiotic exposure *moves cells along the depth axis* rather than merely between two boxes — an advection–reaction structure on depth, fitted to time-kill data and used to predict regimen outcomes. That specific coupling has not been written.

**But be honest about why this is a trap.** Distinguishing a depth-continuum model from a two-compartment model, or from a distributed-delay model with a gamma kernel, requires exactly the kind of single-cell resuscitation-time data that Şimşek/Kim and Balaban generate in their own labs and that you cannot generate. Worse, Cogan, Nooranidoost, Peltier & Romero (J R Soc Interface 2026) just published on precisely this hazard — sensitivity analysis, parameter identifiability and uncertainty quantification for bacterial persistence models, showing that workflow order changes which parameters are even identifiable. A richer model with more parameters fitted to the same population-level CFU data is very likely to be *non-identifiable*, and that is a referee's first question.

### Key citations

| Work | Contribution | What it lacks |
|---|---|---|
| Şimşek & Kim 2019, PNAS 116:17635–17640. PMID 31427535, DOI [10.1073/pnas.1903836116](https://doi.org/10.1073/pnas.1903836116) | Power-law lag-time tail for persisters vs exponential for normals; model built on it | No PK; no depth coordinate; no regimen design |
| De Leenheer, Dockery, Gedeon & Pilyugin 2009, J Math Biol 61:475–499. PMID 19908044, DOI [10.1007/s00285-009-0302-7](https://doi.org/10.1007/s00285-009-0302-7) | Age-structured chemostat PDE, senescence as persister mechanism, antibiotic threshold | Age not dormancy depth; no PK; no depth-dependent kill |
| Kaplan et al. 2021, Nature 600:290–294. PMID 34789881, DOI [10.1038/s41586-021-04114-w](https://doi.org/10.1038/s41586-021-04114-w) | Universal ageing dynamics; heterogeneous recovery predicts persistence | Descriptive; no treatment design |
| Rotem et al. 2026, Sci Adv 12:eadt6577. PMID 41481724, DOI [10.1126/sciadv.adt6577](https://doi.org/10.1126/sciadv.adt6577) | Regulated vs disrupted growth-arrest archetypes; tailored treatments | Argues for two modes, complicating a pure continuum |
| Cogan et al. 2026, J R Soc Interface 23(238). PMID 42126461, DOI [10.1098/rsif.2025.0938](https://doi.org/10.1098/rsif.2025.0938) | Identifiability/SA/UQ workflow for persistence models | **Warning shot**: identifiability is the binding constraint |

---

## D4. Linking the persister model to standard PK/PD target attainment (PTA / CFR)

### Verdict: **GENUINELY OPEN**

This is the clearest gap of the five, and the reason is structural rather than accidental: the two relevant literatures use incompatible model classes and do not cite each other.

### What has been done

**The mechanistic side built the model but never computed PTA.** Nielsen, Cars & Friberg (AAC 2011) is the canonical semi-mechanistic antibacterial PKPD model, and — importantly for you — it *already contains your structure*: a proliferating drug-sensitive compartment S and a **non-growing, drug-insensitive resting compartment R**, with a transfer rate between them. They use it to predict which PK/PD index best correlates with effect for different drugs, arguing explicitly that static indices are summary endpoints that discard the time course. But their endpoints are bacterial count at 24 h, time-to-kill thresholds (T99, T99.9, T99.99) and area under the bacterial count curve. **They compute no PTA and no CFR.** They also state the model does not predict resistance development.

**The PTA side computes PTA but with deterministic models and non-sterilisation endpoints.** The semi-mechanistic-PKPD-plus-Monte-Carlo papers — e.g. Mohd Sazlly Lim et al. on fosfomycin/sulbactam (AAC 2021) and meropenem/sulbactam (Eur J Clin Microbiol Infect Dis 2021) against carbapenem-resistant *A. baumannii* — do exactly the right pipeline shape: fit a semi-mechanistic PK/PD model to time-kill data, then Monte Carlo simulate to get PTA. But their targets are **stasis, 1-log kill and 2-log kill at 24 h**. Not sterilisation. And because the underlying model is a deterministic ODE, it *structurally cannot* express a probability of sterilisation: a deterministic model's bacterial count decays toward zero asymptotically and never reaches it, so "probability of extinction" is not a quantity the model possesses. The best it can do is threshold an arbitrary CFU cut-off.

Toutain et al. (CPT Pharmacometrics Syst Pharmacol 2023) have separately criticised how PTA is computed, showing bias in standard implementations — useful methodological ammunition, and evidence the community is receptive to PTA methodology papers.

### The specific remaining gap

**Nobody has replaced the static PK/PD index with a mechanistic persister model *and* adopted a stochastic extinction criterion, so as to compute PTA and CFR for a true sterilisation endpoint.** Doing so requires exactly the D1 machinery: the endpoint "probability that the population hits zero before end of therapy" only exists in a stochastic model. This reframes the PTA question from "what fraction of simulated patients achieve fT>MIC ≥ 50%?" to "what fraction of simulated patients achieve P(sterilisation) ≥ 0.9?", which is a different and clinically more meaningful object, and it makes the persister compartment *matter* — because it is the persisters that set the tail of the extinction-time distribution and hence the relapse rate.

The composition is novel, publishable in a pharmacometrics or AAC-tier venue, and neither community is positioned to do it: pharmacometricians do not use branching processes, and the branching-process community does not know what a cumulative fraction of response is.

### Key citations

| Work | Contribution | What it lacks |
|---|---|---|
| Nielsen, Cars & Friberg 2011, AAC 55:4619–4630. PMID 21807983, DOI [10.1128/AAC.00182-11](https://doi.org/10.1128/AAC.00182-11) | Semi-mechanistic PKPD with growing S + **resting, drug-insensitive R** compartments; predicts PK/PD indices | **No PTA, no CFR**; endpoints are 24 h count / time-to-kill / AUBC; deterministic |
| Mohd Sazlly Lim et al. 2021, AAC 65:e02472-20. PMID 33685901, DOI [10.1128/AAC.02472-20](https://doi.org/10.1128/AAC.02472-20) | Semi-mechanistic PK/PD + Monte Carlo → PTA for a combination | Endpoints stasis / 1-log / 2-log, **not sterilisation**; deterministic model cannot yield an extinction probability |
| Mohd Sazlly Lim et al. 2021, Eur J Clin Microbiol Infect Dis 40:1943–1952. PMID 33884516, DOI [10.1007/s10096-021-04252-z](https://doi.org/10.1007/s10096-021-04252-z) | Same pipeline, meropenem/sulbactam; PTA for 2-log kill | Same limitation |
| Toutain et al. 2023, CPT Pharmacometrics Syst Pharmacol 12:1069. DOI [10.1002/psp4.12929](https://doi.org/10.1002/psp4.12929) | Demonstrates bias in standard PTA computation | Methodological critique only; no mechanistic model |
| Coates et al. 2018, eLife 7:e32976. PMID 29508699, DOI [10.7554/eLife.32976](https://doi.org/10.7554/eLife.32976) | Supplies the stochastic-extinction endpoint concept | Constant concentration; no PK, no PTA, no switching |

---

## D5. Optimal control / regimen scheduling against a switching population

### Verdict: **LARGELY SOLVED — only the stochastic objective remains**

### What has been done

Cogan's corpus is deep, sustained and closely matched to the question. It should be treated as an occupied field.

- **De Leenheer & Cogan (J Math Biol 2009)** give, for a general chemostat model with susceptible + persister subpopulations, a *condition for failure* of a periodic dosing protocol — and show failure is **global**, i.e. the mixed population persists above a level independent of initial composition. They also give a sufficient condition for success near washout, and — critically — show the dependence of killing speed on antibiotic administration duration is **non-monotone**, so continuous administration is not optimal and genuinely periodic protocols can win.
- **Cogan, Brown, Darres & Petty (AAC 2012)** pose it as a formal optimal-control problem: minimise bacteria while managing total antibiotic load, with environment-dependent switching rates between tolerant and susceptible populations. Result: constant dosing is not optimal; **cycling application and withdrawal kills fastest**. They deliberately produce experimentally testable predictions.
- **Cogan, Rath, Kommerein, Stumpp & Stiesch (FEMS Microbiol Lett 2016)** then *experimentally confirm* the predicted timing with *S. aureus* biofilms and ofloxacin. Theory-to-experiment loop closed.
- **Acar & Cogan (Math Biosci 2019)** extend to **two control variables** — antibiotic *and nutrient* — and solve the optimal dose–withdrawal timing under constant, dynamic and piecewise-constant nutrient, via a Poincaré map.
- **Cogan et al. (J R Soc Interface 2026)** are still active, now on identifiability and uncertainty quantification for these same persistence models.

Outside Cogan: **Katriel (Bull Math Biol 2024)** derives *analytic* optimal schedules — minimise AUC subject to eradication — showing the optimal concentration profile is constant over a finite duration, and that a practical bolus-plus-continuous-infusion schedule comes close. This work **does include pharmacokinetics** but has **no persister compartment**. Birnir et al. (Commun Nonlinear Sci Numer Simul 2025) derive finite-time biofilm extinction with bang-bang and Kalman-filter-based optimal control. Ali et al. (PLoS ONE 2022) solve optimal dosing with resistant strains via HGT and explicitly state in their conclusion that adding persisters is their intended follow-up — i.e. another group has publicly declared this exact next step.

### The specific remaining gap

Every result above optimises a **deterministic** objective — biomass, time to reach a threshold, AUC subject to deterministic eradication. **Nobody has optimised a stochastic objective: minimise P(relapse), or maximise P(extinction before end of therapy), over a regimen space constrained by realistic PK.** That is genuinely unclaimed, and it is the same object D4 needs. But note it is a modest increment on a 20-year-old corpus by an author who is still publishing in the area and whose collaborators have announced the persister extension.

### Key citations

| Work | Contribution | What it lacks |
|---|---|---|
| De Leenheer & Cogan 2009, J Math Biol 59:563–579. PMID 19083238, DOI [10.1007/s00285-008-0243-6](https://doi.org/10.1007/s00285-008-0243-6) | Global failure condition for periodic dosing; non-monotone dependence on dosing duration | Deterministic; chemostat; no clinical PK |
| Cogan, Brown, Darres & Petty 2012, AAC 56:4816–4826. PMID 22751538, DOI [10.1128/AAC.00675-12](https://doi.org/10.1128/AAC.00675-12) | Formal optimal control, persister/susceptible; cycling beats constant dosing | Deterministic objective; no PK model; no relapse probability |
| Cogan et al. 2016, FEMS Microbiol Lett 363:fnw264. PMID 27915255, DOI [10.1093/femsle/fnw264](https://doi.org/10.1093/femsle/fnw264) | Experimental confirmation of predicted optimal timing | — (closes the loop, raising the bar) |
| Acar & Cogan 2019, Math Biosci 313:12–32. PMID 31047899, DOI [10.1016/j.mbs.2019.04.007](https://doi.org/10.1016/j.mbs.2019.04.007) | Two-control (antibiotic + nutrient) optimal dose–withdrawal timing; Poincaré map | Deterministic; batch culture |
| Katriel 2024, Bull Math Biol 86:5. DOI [10.1007/s11538-023-01230-8](https://doi.org/10.1007/s11538-023-01230-8) | Analytic optimal schedule minimising AUC subject to eradication, **with PK** | **No persisters**; deterministic eradication |

---

## MASTER CITATION TABLE

| # | Citation | PMID | DOI | Direction |
|---|---|---|---|---|
| 1 | Coates JL et al. Antibiotic-induced population fluctuations and stochastic clearance of bacteria. eLife 2018;7:e32976 | 29508699 | 10.7554/eLife.32976 | D1, D4 |
| 2 | Lohmar I, Meerson B. Switching between phenotypes and population extinction. Phys Rev E 2011;84:051901 | — | 10.1103/PhysRevE.84.051901 | D1 |
| 3 | Blath J, Hermann F, Slowik M. A branching process model for dormancy and seed banks in randomly fluctuating environments. J Math Biol 2021;83:17 | 34279717 | 10.1007/s00285-021-01639-6 | D1, D3 |
| 4 | Gunnarsson EB, De S, Leder K, Foo J. Understanding the role of phenotypic switching in cancer drug resistance. J Theor Biol 2020;490:110162 | — | 10.1016/j.jtbi.2020.110162 | D1 |
| 5 | Garet O, Marchand R, Schinazi RB. Bacterial persistence: a winning strategy? arXiv:1109.5132 | — | 10.48550/arXiv.1109.5132 | D1 |
| 6 | Czuppon P et al. A stochastic analysis of the interplay between antibiotic dose, mode of action, and bacterial competition. PLoS Comput Biol 2023 | — | 10.1371/journal.pcbi.1011364 | D1, D2 |
| 7 | Nyhoegen C, Uecker H. The many dimensions of combination therapy. Evol Appl 2024 | — | 10.1111/eva.13764 | D1, D2 |
| 8 | Levin-Reisman I et al. Antibiotic tolerance facilitates the evolution of resistance. Science 2017;355:826–830 | 28183996 | 10.1126/science.aaj2191 | D2 |
| 9 | Witzany C, Regoes RR, Igler C. Assessing the relative importance of bacterial resistance, persistence and hyper-mutation for antibiotic treatment failure. Proc R Soc B 2022;289:20221300 | 36350213 | 10.1098/rspb.2022.1300 | D2 |
| 10 | Witzany C, Rolff J, Regoes RR, Igler C. The PKPD modelling framework as a tool to predict drug resistance evolution. Microbiology 2023;169:001368 | 37522891 | 10.1099/mic.0.001368 | D2 |
| 11 | Boccarella G et al. Bacterial persistence modulates the speed, magnitude, and onset of antibiotic resistance evolution. Mol Biol Evol 2026;43:msag180 | — | 10.1093/molbev/msag180 | D2 |
| 12 | Liu J et al. Effect of tolerance on the evolution of antibiotic resistance under drug combinations. Science 2020;367:200–204 | 31919223 | 10.1126/science.aay3041 | D2 |
| 13 | Windels EM et al. Antibiotic dose and nutrient availability differentially drive the evolution of antibiotic resistance and persistence. ISME J 2024;18:wrae070 | — | 10.1093/ismejo/wrae070 | D2 |
| 14 | Şimşek E, Kim M. Power-law tail in lag time distribution underlies bacterial persistence. PNAS 2019;116:17635–17640 | 31427535 | 10.1073/pnas.1903836116 | D3 |
| 15 | De Leenheer P, Dockery J, Gedeon T, Pilyugin SS. Senescence and antibiotic resistance in an age-structured population model. J Math Biol 2009;61:475–499 | 19908044 | 10.1007/s00285-009-0302-7 | D3 |
| 16 | Kaplan Y et al. Observation of universal ageing dynamics in antibiotic persistence. Nature 2021;600:290–294 | 34789881 | 10.1038/s41586-021-04114-w | D3 |
| 17 | Rotem A et al. Differentiation between regulated and disrupted growth arrests... Sci Adv 2026;12:eadt6577 | 41481724 | 10.1126/sciadv.adt6577 | D3 |
| 18 | Cogan NG, Nooranidoost M, Peltier M, Romero S. Order matters: sensitivity analysis, parameter identifiability and uncertainty quantification. J R Soc Interface 2026;23(238) | 42126461 | 10.1098/rsif.2025.0938 | D3, D5 |
| 19 | Nielsen EI, Cars O, Friberg LE. PK/PD indices of antibiotics predicted by a semimechanistic PKPD model. AAC 2011;55:4619–4630 | 21807983 | 10.1128/AAC.00182-11 | D4 |
| 20 | Mohd Sazlly Lim S et al. Semi-mechanistic PK/PD modelling of fosfomycin and sulbactam. AAC 2021;65:e02472-20 | 33685901 | 10.1128/AAC.02472-20 | D4 |
| 21 | Mohd Sazlly Lim S et al. Semi-mechanistic PK/PD modelling of meropenem and sulbactam. Eur J Clin Microbiol Infect Dis 2021;40:1943–1952 | 33884516 | 10.1007/s10096-021-04252-z | D4 |
| 22 | Toutain PL et al. Biased computation of probability of target attainment for antimicrobial drugs. CPT Pharmacometrics Syst Pharmacol 2023;12:1069 | — | 10.1002/psp4.12929 | D4 |
| 23 | De Leenheer P, Cogan NG. Failure of antibiotic treatment in microbial populations. J Math Biol 2009;59:563–579 | 19083238 | 10.1007/s00285-008-0243-6 | D5 |
| 24 | Cogan NG, Brown J, Darres K, Petty K. Optimal control strategies for disinfection of bacterial populations with persister and susceptible dynamics. AAC 2012;56:4816–4826 | 22751538 | 10.1128/AAC.00675-12 | D5 |
| 25 | Cogan NG et al. Theoretical and experimental evidence for eliminating persister bacteria by manipulating killing timing. FEMS Microbiol Lett 2016;363:fnw264 | 27915255 | 10.1093/femsle/fnw264 | D5 |
| 26 | Acar N, Cogan NG. Enhanced disinfection of bacterial populations by nutrient and antibiotic challenge timing. Math Biosci 2019;313:12–32 | 31047899 | 10.1016/j.mbs.2019.04.007 | D5 |
| 27 | Katriel G. Optimizing antimicrobial treatment schedules: some fundamental analytical results. Bull Math Biol 2024;86:5 | — | 10.1007/s11538-023-01230-8 | D5 |
| 28 | Ankomah P, Levin BR. Exploring the collaboration between antibiotics and the immune response... PNAS 2014;111:8331–8338 | 24843148 | 10.1073/pnas.1400352111 | D1, D2 |
| 29 | Ankomah P, Johnson PJT, Levin BR. The pharmaco-, population and evolutionary dynamics of multi-drug therapy. PLoS Pathog 2013;9:e1003300 | 23593006 | 10.1371/journal.ppat.1003300 | D2, D4 |
| 30 | Ali A et al. Pharmacokinetics determine persister formation in *Escherichia coli*. JAC-AMR 2026;8:dlag145 | — | 10.1093/jacamr/dlag145 | D1, D5 |

*Source note: records retrieved from PubMed (NCBI) and Consensus (Semantic Scholar / Scopus / arXiv). Items without a PMID were not indexed in PubMed at time of search; DOIs verified against publisher pages where accessible. Two DOIs (#6, #7, #13) were resolved from Consensus/publisher metadata rather than a PubMed record and should be re-verified before submission.*

---

## RANKED RECOMMENDATION

### 1st — **D4, executed as a fusion of D4 and D1.** *Recommended.*

**The project.** Replace the static PK/PD index in a standard PTA/CFR pipeline with a two-type (replicating / persister) *stochastic* model whose type-specific kill rates are Hill functions of a time-varying concentration drawn from a published population PK model. Compute, per simulated patient, the probability of sterilisation via the backward Kolmogorov system for the multitype pgf under periodic forcing. Then report PTA and CFR against a **sterilisation** target rather than stasis or 1-log kill, using EUCAST MIC distributions, and show where the sterilisation-based breakpoint diverges from the index-based one.

**Why it wins on all four criteria:**

- *(a) Mathematical novelty* — real but bounded. The novel object is the extinction probability of a time-inhomogeneous two-type branching process under periodic PK forcing, and its use as a clinical target. The Floquet/monodromy characterisation of that pgf system is a genuine mathematical contribution, and it makes the persister compartment do real work (it sets the tail of the extinction-time distribution, hence relapse).
- *(b) Clinical relevance* — the highest of the five, and the most legible. PTA/CFR is the language EUCAST, CLSI and every dose-selection dossier already speak. "Your 1-log-kill target is not a cure target, and here is what changes when you use one" is a sentence a clinical pharmacologist will act on. It also directly addresses relapse, which is the clinical failure mode persisters actually cause.
- *(c) Feasibility for a small group with public data and no wet lab* — excellent, and decisively better than the alternatives. You already have the Monte Carlo PTA/CFR pipeline built for ceftazidime–avibactam. Population PK models are published; EUCAST MIC distributions are free; time-kill data with biphasic killing are extractable from the literature. Nothing here needs a bench.
- *(d) Scoop / collision risk* — the lowest of the five, for a structural reason. The gap persists because it sits in the seam between two communities that do not overlap: pharmacometricians (Friberg, Nielsen, Landersdorfer, Bulitta) build deterministic ODE models and do not use branching processes; the stochastic-extinction community (Meerson, Blath, Foo/Leder, Uecker) does not know or care what a cumulative fraction of response is. Nobody has declared intent here, unlike D2 and D5 where competitors have publicly announced the next step.

**Principal risk.** A referee will ask whether the sterilisation probability is identifiable from population-level CFU data. Pre-empt this: fix the switching parameters from published single-cell lag-time data (Şimşek & Kim supplies the distributional form), and present the result as a sensitivity band over those parameters rather than a point estimate. Frame the contribution as *"here is how the target changes"*, not *"here is the true persister rate"*.

### 2nd — **D1 as the standalone methods companion.**

If D4 is the applied paper, D1 is its methods half and can be split out into a mathematical-biology venue. Lower clinical pull, but clean, defensible and it strengthens D4. Do not do D1 *instead of* D4 — alone it competes directly with Lohmar–Meerson and Gunnarsson et al. on their own terms, and the PK coupling is the only thing that makes it new.

### 3rd — **D2.** *Do not lead with this.*

Highest intellectual appeal and the direction you care most about, but the honest assessment is that Boccarella et al. (August 2026) took the central result, Witzany et al. (2023) published the roadmap, and the surviving gap — regimen optimisation under realistic PK — is the obvious next paper for two established groups who have the data and have said so. A small group without a wet lab entering here is entering behind. If you want this direction, the defensible entry is *through* D4: once you have a stochastic sterilisation-probability machinery with real PK, adding a resistance type and asking for the Pareto front between P(sterilisation) and P(resistance) is a natural second paper — and you would arrive with a tool the competitors do not have, rather than competing on their ground.

### 4th — **D5.**

Cogan has owned this since 2006, closed the theory-experiment loop in 2016, and published again in 2026. Katriel (2024) took the analytic-optimal-schedule-with-PK result. Ali et al. (2022) publicly announced persisters as their follow-up. The remaining stochastic-objective increment is real but modest, and it is subsumed by D4 anyway.

### 5th — **D3.** *Avoid.*

The mathematics substantially pre-exists in food microbiology and in De Leenheer et al. (2009); the biology is moving toward two archetypes rather than a clean continuum (Rotem 2026); and the binding constraint is parameter identifiability from population-level data, which Cogan just published a paper about. Without single-cell resuscitation data you cannot distinguish your model from a simpler one, and that is the first question you will be asked.
