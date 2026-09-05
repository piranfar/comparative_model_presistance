# 11 — Relapse Claim Check (adversarial)

**Claim under test:** *"Mtb persister resuscitation rate determines the probability and timing of relapse after treatment stops (distinct from time-to-clearance during treatment); because relapse from a small surviving population is stochastic, it requires a branching-process treatment that deterministic PD models cannot provide."*

---

## VERDICT (blunt)

1. **The claim as stated is dead.** Both halves are already published, separately and together.
2. **"Deterministic PD models cannot predict relapse" is factually false.** Magombedze/Pasipanodya/Gumbo 2021 predict relapse in 1,924 REMoxTB patients at 92% sensitivity / 89% specificity from a deterministic two-compartment ODE with **no resuscitation term at all**. Wallis 2016 does it with no bacteria in the model whatsoever.
3. **The stochastic machinery is done.** Blath–Hermann–Slowik 2021 (J Math Biol) is a two-type active/dormant branching process with switching in a fluctuating environment, extinction probability included. Lohmar & Meerson 2011 (PRE) did WKB extinction with normal/persister switching. Applying either to Mtb is an application, not a contribution.
4. **The resuscitation→relapse causal link is accepted knowledge, not an open question.** Rpf-dependent Mtb is enriched during chemotherapy (Mukamolova 2009), and eliminating culture-filtrate-dependent Mtb prevents relapse in the Cornell mouse. The proposer's own supporting citation (Russell-Goldman 2008) is a 2008 paper making exactly this point.
5. **The relapse-probability-from-mouse-CFU problem is an operational industry standard.** Berg/Clary et al. (AAC 2022, AAC 2025, Gates Foundation + Simulations Plus + TB-APEX) fit Bernoulli relapse outcomes to a sigmoid in treatment duration and report T95. No mechanism, no persisters, and it is the tool actually used for regimen selection.
6. **What survives (thin):** nobody has published a *mechanistic* stochastic model in which an explicitly parameterised **resuscitation rate** sets the post-treatment extinction probability, calibrated to Mtb. That is a gap of assembly, not of ideas — and there is no data to identify the resuscitation rate, which is the killing objection (§6).

---

## 1. Is relapse probability from persister dynamics already modelled?

Yes, at least four independent ways, none of which needed the proposer's mechanism.

| Approach | Work | What it computes | Resuscitation term? |
|---|---|---|---|
| Deterministic ODE + time-to-extinction | Magombedze, Pasipanodya & Gumbo 2021 | Per-patient relapse vs cure vs failure, 1,924 patients | **No** |
| Pure meta-regression, no bacteria | Wallis 2016 / Wallis et al. 2013, 2015 | Trial-level relapse rate from month-2 culture + duration | **No** |
| Deterministic translational PK/PD | Lyons 2017, *Clin Transl Sci* | Probability of relapse at 1 year for 4-month regimens | **No** |
| Mixed-effects logistic on mouse relapse | Berg et al. AAC 2022; Clary et al. AAC 2025 | Relapse probability vs duration, T95, per regimen | **No** |

Magombedze is the one to read. Their model is two logistic subpopulations, fast (`B_F`) and semi-dormant/non-replicating (`B_S`), each with its own growth rate and its own drug kill slope (γ_F, γ_S). **There is no interconversion term between the two compartments** — no dormancy entry rate, no resuscitation rate. Relapse is attributed entirely to γ_S, the slow-phase kill slope, which CART ranked as the #1 predictor (variable importance 100%), ahead of baseline burden (91.7%); γ_F was **not ranked at all**. They rename γ_S "the sterilizing activity rate". Time-to-extinction is a deterministic threshold crossing (≤10^0 CFU/mL), and Monte Carlo is used only to sweep parameters, not to compute an extinction probability.

So the field's best-performing relapse predictor attributes relapse to **how fast persisters are killed**, not to **how fast they wake up**. The proposer must explain why a resuscitation rate adds anything on top of a variable that already delivers 92%/89%.

Wallis is worse for the claim: logit(recurrence) ~ log(duration) + logit(month-2 culture positivity), fit to 7,793 patients / 58 regimens from 1973–1997, then *prospectively* correct on REMox, RIFAQUIN and OFLOTUB (predicted 10.4–19.4% relapse, observed 12.5–17.8%; r = 0.86 on the validation). A model containing zero bacterial biology predicted the outcomes of three phase III trials.

Also relevant: a stochastic CTMC TB model with fast–slow progression and relapse uses a multitype Galton–Watson branching process for extinction probability (Electron Res Arch 2023) — but that is population-level epidemiology, not within-host persisters.

## 2. Does Magombedze et al. 2021 already do this? — Precisely

Read in full (PMC8172544). What they did:

- Converted MGIT time-to-positivity to CFU/mL for 1,924 REMoxTB patients.
- Fit a **2-ODE deterministic model** (fast + semi-dormant/NRP subpopulations, shared carrying capacity, separate γ kill slopes) by MCMC, 50,000 iterations.
- Estimated NRP fraction at 1–25% of the log-phase population, cross-checked against lipid-body counts in sputum (Garton, Sloan).
- CART on all clinical/radiological/model covariates → γ_S primary predictor, baseline burden second. HIV status, **cavitation**, and sex all scored <10% importance.
- K-means clustering of TTP trajectories → cure / slow-cure / relapse / failure clusters.
- Monte Carlo (10,000 trajectories) + Latin hypercube sensitivity only to resolve indeterminate γ_S bands and map γ_S → required duration.
- Derived rule: γ_S > 0.15 logCFU/mL/day → relapse-free cure; γ_S < 0.13 with B(0) > 5.6 logCFU/mL → relapse. Validation: **92% sensitivity, 89% specificity** separating relapse from failure at 6 months; 81%/89% at 4 months. Extended-EBA sensitivity 14%; month-2 conversion 33%.

**Answer to the three sub-questions:** (a) No resuscitation or switching term — confirmed by reading the model description; the compartments do not exchange. (b) Yes, they attribute relapse to the kill slope, explicitly renaming γ_S the "sterilizing activity rate". (c) Therefore yes — **they predict relapse without any resuscitation rate, and this damages the claim badly.** The proposer's mechanism is not necessary for the outcome the proposer wants to explain.

Two honest caveats the proposer may reach for, and why they are weak:
- Their "time-to-extinction" is a deterministic threshold, not P(extinction). True — but it works, so the burden is to show the stochastic version predicts *better*, on data the proposer does not have.
- They concede immunity can clear residual bacteria and that not all non-extinct patients relapse. That is an argument for a *host* term, not a resuscitation term.

## 3. Is the resuscitation→relapse link already established?

**Established, and old.** This is the single worst place for the proposer to claim novelty.

- Mukamolova et al. 2009 (AJRCCM): in 20/25 pre-chemotherapy sputa, **80–99.99%** of viable Mtb were detectable only with Rpf stimulation, and the Rpf-dependent fraction **increases relative to CFU during chemotherapy** — described by the authors as phenotypic resistance relevant to chemotherapy.
- Downing/Kana/Mizrahi 2008 (Infect Immun, PMC2229633): Rpfs required for virulence and resuscitation from dormancy, dispensable in vitro.
- Russell-Goldman et al. 2008 (the proposer's own citation): ΔrpfAB has a reactivation defect **including from a drug-induced apparently sterile state in NOS2−/− mice upon cessation of antimycobacterial therapy**. That sentence is in the 2008 abstract. The proposer's "novel" hypothesis is the stated conclusion of an 18-year-old paper.
- Eradication of culture-filtrate-dependent Mtb prevents relapse in the Cornell mouse model.
- "Wake and kill" is an established named strategy; Rpf inhibitors are an active target class.
- Antia, Koella & Perrot 1996 (Proc R Soc B 263:257) already wrote the ODE with an explicit dormancy rate and **reactivation rate** for persistent mycobacterial infection. Thirty years ago.

So: not open. Accepted, mechanistically supported, and already the basis of a drug-discovery programme.

## 4. What actually causes TB relapse (ranked, with evidence)

A referee will ask why resuscitation rate should outrank any of these. It currently outranks none of them.

| Rank | Driver | Evidence | Strength |
|---|---|---|---|
| 1 | **Reinfection, not relapse at all** | Verver et al. 2005 (AJRCCM, PMID 15831840): post-treatment reinfection rate **exceeds** the rate of new TB; ~4–7× higher risk of a second episode. WGS now routinely splits relapse from reinfection (Bryant 2013, Lancet Respir Med). In high-burden settings a large share of "relapse" is a different strain. | Very strong |
| 2 | **Adherence / drug exposure** | Imperial et al. 2018 (Nat Med 24:1708): in 3,405 patients, adherence ≤90% a significant risk factor; Magombedze themselves note Imperial found non-adherence the strongest factor, HR 5.9. | Very strong |
| 3 | **Baseline bacterial burden & cavitation** | Imperial 2018: smear grade 3+ and cavitation define the "hard-to-treat" phenotype and gate 4-month eligibility. Magombedze's own model keeps B(0) as the #2 predictor. Cavitation + month-2 culture positivity is the classic Mitchison/Benator stratifier. | Strong |
| 4 | **Regimen sterilizing activity (kill slope)** | Magombedze 2021: γ_S, 92%/89%. Wallis: month-2 conversion + duration predicts phase III relapse. | Strong |
| 5 | **Lesion pathology / drug penetration** | Prideaux, Dartois et al. 2015 (Nat Med): MALDI-MSI shows lesion-structure- and drug-dependent penetration; rifampicin accumulates in caseum, pyrazinamide distributes differently; caseum harbours non-replicating persisters. This is a *spatial* explanation for persistence that competes directly with a switching-rate explanation. | Strong |
| 6 | **Host immunity** | Anti-TNF reactivation (Wallis hidden Markov model: infliximab 12.1× the monthly reactivation rate of etanercept); HIV status; Magombedze concede immunity clears residual bacteria in non-extinct patients. | Moderate–strong |
| 7 | **Persister/resuscitation dynamics** | Rpf/DCTB biology (§3) — mechanistically real, but never shown to be the *rate-limiting* determinant of relapse probability in humans, and absent from every model that successfully predicts relapse. | Weak as a *dominant* driver |

Note the killer detail: in Magombedze's own CART on 1,924 patients, **cavitation and HIV scored below 10% variable importance**, and the winning variable was a kill rate. There is no clinical dataset in which a resuscitation rate has ever been measured, let alone ranked.

## 5. Stochastic extinction under treatment with phenotype switching

| Work | What is done | Extension to TB relapse |
|---|---|---|
| **Lohmar & Meerson 2011**, *Phys Rev E* 84:051901, "Switching between phenotypes and population extinction" | WKB in real space; normals ↔ persisters with stochastic switching; extinction risk from intrinsic birth/death/switching noise plus extrinsic catastrophes. Exactly the proposer's mathematical object. | **Mechanical.** Substituting Mtb rate constants into an existing WKB result is a parameterisation exercise. |
| **Blath, Hermann & Slowik 2021**, *J Math Biol* 83:17 | Two-type branching process, active ↔ dormant switching, random environment alternating healthy/harsh (= off-drug/on-drug). Survival/extinction criteria. | **Mechanical.** The "harsh environment" is the drug course; "healthy" is post-treatment. The model is already the claim. |
| **Coates et al. 2018**, *eLife* 7:e32976 (PMID 29508699) | Experimental + probabilistic birth–death: shows antibiotic clearance is stochastic, extinction occurs with non-zero probability even at sub-MIC, and predicts/validates a strategy to raise extinction probability. Directly refutes "deterministic PD is sufficient" — but also **already made that argument**, in 2018, in E. coli. | **Mechanical for the physics; the novelty was spent in 2018.** |
| **Witzany, Regoes & Igler 2022**, *Proc R Soc B* 289:20221300 | Stochastic population model of persisters + resistance + hypermutation under PD kill. Explicitly: persisters cause "hidden" treatment failure at very low cell numbers, **regrow after treatment is discontinued**, and this constitutes *relapse*. Persister regrowth-after-stopping is the paper's stated mechanism. | **Substantively pre-empts the biological claim** in a general bacterial setting. |
| **Gunnarsson / Foo / Leder** | Branching-process machinery for phenotype-switching populations and extinction/escape probabilities exists in this line of work but is framed around resistance and cancer therapy rather than TB relapse. | The tooling is off-the-shelf. |
| **Clary et al. 2025**, *AAC* 70:e0110325 (PMID 41459930) | Stochastic simulation of TB relapse: Bernoulli relapse draws per virtual mouse, sigmoid P(relapse) in duration with study random effects and inoculum covariate, Bayesian MCMC re-estimation, T95 = time to 95% cure probability. | **This is what the field does instead.** Purely phenomenological, and it is what Gates/Simulations Plus use to pick regimens. A referee will ask what mechanism buys over this. |

Summary: **the physics is done, the general-bacteria biology is done, and the TB-specific engineering is done — just not all in the same paper.**

## 6. The hardest single objection

> **"Your resuscitation rate is not identifiable from any data you can obtain, and every model that already predicts relapse does so without it."**

Unpack it, because it is fatal in its current form:

- A branching process with dormancy has at minimum a growth rate, a death rate, a dormancy-entry rate and a resuscitation rate. Relapse probability depends on their **combination**. Post-treatment you observe one binary outcome per host, at one time. **One bit of data cannot identify four rates.** Structural non-identifiability, not a sample-size problem.
- Rpf-dependent/DCTB counts (Mukamolova) measure *how many* bacteria need resuscitation, not the *rate* at which they resuscitate in vivo. There is no assay that yields a per-cell in vivo resuscitation rate in a treated human or mouse.
- The proposer's only supporting datum actively undercuts them: ΔrpfAB had a reactivation defect **but lung counts identical to wild-type at the end of the drug course**. That is a single knockout genotype giving one qualitative contrast. It shows resuscitation matters for reactivation *timing*; it does not let you estimate a rate, and it does not show the rate is what varies between relapsing and non-relapsing patients.
- Meanwhile γ_S (Magombedze) and month-2 culture + duration (Wallis) are measured routinely, worldwide, at no extra cost, and already give 92%/89% and phase-III-accurate predictions.

The referee's closing line writes itself: *the proposal replaces an identifiable, measured, validated predictor with an unidentifiable, unmeasured one, and calls the substitution mechanistic insight.*

A secondary objection nearly as bad: **relapse timing is dominated by reinfection in exactly the high-burden settings where relapse is common** (Verver 2005). Any relapse-timing distribution the model predicts is confounded by exogenous reinfection unless the proposer restricts to WGS-confirmed same-strain recurrence — which collapses the sample size to a handful of events per trial.

---

## Citation table

| # | Citation | Access | Why it matters | Confidence it damages the claim |
|---|---|---|---|---|
| 1 | Magombedze G, Pasipanodya JG, Gumbo T. *Bacterial load slopes represent biomarkers of tuberculosis therapy success, failure, and relapse.* Commun Biol 2021;4:664. PMID 34079045. [DOI](https://doi.org/10.1038/s42003-021-02184-0) | **Open (PMC8172544), full text read** | Deterministic 2-ODE, **no resuscitation term**, predicts relapse at 92%/89% in 1,924 REMoxTB patients; relapse attributed to slow-phase kill slope γ_S | **Very high — the single most damaging paper** |
| 2 | Blath J, Hermann F, Slowik M. *A branching process model for dormancy and seed banks in randomly fluctuating environments.* J Math Biol 2021;83:17. [DOI](https://doi.org/10.1007/s00285-021-01639-6) | Open (link.springer.com) | Two-type active/dormant branching process with switching, harsh/healthy environment, extinction criteria — the claim's exact mathematical object, already published | **Very high** |
| 3 | Lohmar I, Meerson B. *Switching between phenotypes and population extinction.* Phys Rev E 2011;84:051901. [arXiv:1107.5192](https://arxiv.org/pdf/1107.5192) | Preprint open; journal paywalled | WKB extinction with normal↔persister switching under stress | High |
| 4 | Witzany C, Regoes RR, Igler C. *Assessing the relative importance of bacterial resistance, persistence and hyper-mutation for antibiotic treatment failure.* Proc Biol Sci 2022;289:20221300. PMID 36350213. [DOI](https://doi.org/10.1098/rspb.2022.1300) | **Open (PMC9653239)** | Stochastic model where persisters regrow after treatment stops = relapse; already frames persister-driven relapse | **High** |
| 5 | Coates J, Park BR, Le D, Şimşek E, Chaudhry W, Kim M. *Antibiotic-induced population fluctuations and stochastic clearance of bacteria.* eLife 2018;7:e32976. PMID 29508699. [DOI](https://doi.org/10.7554/eLife.32976) | **Open (PMC5847335)** | Establishes experimentally that clearance is stochastic and deterministic PD is insufficient — the proposer's framing argument, made in 2018 | High |
| 6 | Clary J, Roberts JK, Hanna D, Tagliavini A, Sordello S, Upton A, Hermann D, Berg A. *A stochastic simulation-based approach to inform the relapsing mouse model study design for non-clinical assessment of tuberculosis.* Antimicrob Agents Chemother 2025;70(2):e0110325. PMID 41459930. [DOI](https://doi.org/10.1128/aac.01103-25) | **Open (PMC12888889), full text read** | Field-standard stochastic TB relapse model: Bernoulli draws, sigmoid P(relapse) vs duration, T95. No mechanism needed | High |
| 7 | Wallis RS. *Mathematical Models of Tuberculosis Reactivation and Relapse.* Front Microbiol 2016;7:669. PMID 27242697. [DOI](https://doi.org/10.3389/fmicb.2016.00669) | **Open (PMC4869524), full text read** | Meta-regression with **no bacteria in the model** prospectively predicted REMox/RIFAQUIN/OFLOTUB relapse rates (r=0.86) | High |
| 8 | Mukamolova GV, Turapov O, Malkin J, Woltmann G, Barer MR. *Resuscitation-promoting factors reveal an occult population of tubercle bacilli in sputum.* Am J Respir Crit Care Med 2010;181:174–80. PMID 19875686. [DOI](https://doi.org/10.1164/rccm.200905-0661OC) | **Open (PMC2809243)** | 80–99.99% of viable Mtb Rpf-dependent; fraction rises during chemotherapy. Resuscitation-biology link long established | High (kills originality of §3) |
| 9 | Russell-Goldman E, Xu J, Wang X, Chan J, Tufariello JM. *A Mycobacterium tuberculosis Rpf double-knockout strain exhibits profound defects in reactivation…* Infect Immun 2008;76:4269–81. PMID 18591237. [DOI](https://doi.org/10.1128/IAI.01735-07) | **Open (PMC2519441)** | Proposer's own evidence — already states reactivation deficiency from a drug-induced sterile state on cessation of therapy (2008) | High (the claim is this paper's conclusion) |
| 10 | Imperial MZ, et al. *A patient-level pooled analysis of treatment-shortening regimens for drug-susceptible pulmonary tuberculosis.* Nat Med 2018;24:1708–15. PMID 30397355. [DOI](https://doi.org/10.1038/s41591-018-0224-2) | **Open (PMC6685538)** | Adherence ≤90%, smear 3+, HIV drive unfavourable outcomes in 3,405 patients — competing explanations that outrank persister dynamics | High |
| 11 | Verver S, et al. *Rate of reinfection tuberculosis after successful treatment is higher than rate of new tuberculosis.* Am J Respir Crit Care Med 2005;171:1430–5. PMID 15831840. | Paywalled abstract on PubMed | Much "relapse" is reinfection; confounds any relapse-timing prediction | High |
| 12 | Prideaux B, Dartois V, et al. *The association between sterilizing activity and drug distribution into tuberculosis lesions.* Nat Med 2015;21:1223–7. | Paywalled | Lesion-structure-dependent drug penetration as the competing explanation for persistence and relapse | Moderate–high |
| 13 | Lyons MA. *New Paradigm for Translational Modeling to Predict Long-term Tuberculosis Treatment Response.* Clin Transl Sci 2017. | **Open (PMC5593171)** | Deterministic mouse→human PK/PD predicting **probability of relapse** at 1 year for 4-month regimens | Moderate–high |
| 14 | Berg A, et al. *Model-Based Meta-Analysis of Relapsing Mouse Model Studies from the CPTR Initiative Database.* Antimicrob Agents Chemother 2022. [DOI](https://doi.org/10.1128/aac.01793-21) | Paywalled (journals.asm.org 403); [bioRxiv preprint open](https://www.biorxiv.org/content/10.1101/2021.09.13.460195v1.full) | Mixed-effects logistic relapse-probability model over 28 RMM studies; the parent of #6 | Moderate–high |
| 15 | Antia R, Koella JC, Perrot V. *Models of the within-host dynamics of persistent mycobacterial infections.* Proc R Soc Lond B 1996;263:257–63. PMID 8920248. [DOI](https://doi.org/10.1098/rspb.1996.0040) | Paywalled | ODE with explicit dormancy **and reactivation** rates for Mtb, 1996 | Moderate (kills "two-compartment with resuscitation" as novel) |
| 16 | Downing KJ, Kana BD, Mizrahi V, et al. *The Rpfs of M. tuberculosis are required for virulence and resuscitation from dormancy…* Infect Immun 2008. [PMC2229633](https://pmc.ncbi.nlm.nih.gov/articles/PMC2229633/) | Open | Rpf requirement for resuscitation established | Moderate |
| 17 | Chakraborty S, Ganusov VV. *A brief overview of mathematical modeling of the within-host dynamics of M. tuberculosis.* Front Appl Math Stat 2024;10:1355373. PMID 39906541. [DOI](https://doi.org/10.3389/fams.2024.1355373) | **Open (PMC11793202), full text read** | Field survey: confirms deterministic ODE and stochastic (Gillespie) within-host Mtb models both already exist, including dormancy compartments | Moderate (context) |

*Literature accessed via PubMed / PubMed Central, Consensus, and web search, 2026-09-04.*

---

## What the proposer could still do (not an endorsement)

Only one framing is not obviously foreclosed, and it is narrow:

> Given γ_S is already a 92%-sensitive relapse predictor, show that a stochastic extinction model **explains the residual misclassification** — specifically Magombedze's own admitted failure mode, that patients who do not reach modelled extinction nonetheless achieve relapse-free cure, and the 8-week-vs-4-month slope misclassification asymmetry.

That is a calibration/residual-analysis contribution to someone else's model, not a new theory of relapse. It still requires relapse data the proposer does not have, and it still cannot identify a resuscitation rate. **Recommendation: do not pursue the claim as written.**
