# Claim Novelty Check — Resuscitation Rate as Dominant Determinant of Treatment Duration

**Date:** 2026-09-04 · **Status:** adversarial pre-writing novelty assessment

---

## VERDICT (blunt)

1. **NOT novel as stated — partially published, and the published half is the conceptual half.** "Bacilli dormant much of the time but occasionally metabolising" as the determinant of sterilising activity is Dickinson & Mitchison 1981; "the exit rate limits the rate of killing" is already stated of Balaban's 2004 model.
2. **Single closest paper: Patra & Klumpp, PLoS ONE 2013 (PMID 23675428, OA).** Their small-switching-rate result gives the terminal decay rate under stress as `λ_eff ≈ λ_p − b` — persister kill rate **plus** resuscitation rate. That is the claim's entire algebra, published, thirteen years ago; they simply never apply it to treatment duration.
3. **The clause "dominating the direct kill rate of persisters" is empirically contradicted**, not merely unpublished — Magombedze/Gumbo (Commun Biol 2021, 1,924 REMoxTB patients) rank the slow-phase kill slope γs first at 100% importance for therapy duration. **Drop this clause.**
4. **A published negative result exists against the mechanism:** Martinecz et al. (PLoS Comput Biol 2023) fitted switching-based persistence to human rifampicin EBA data and rejected it for heteroresistance. Experimentally, ΔrpfAB mice (Russell-Goldman 2008) show blocking resuscitation delays *relapse* but leaves *clearance under identical treatment unchanged*.
5. **Genuinely open:** (a) no variance-based/Sobol GSA of any persister or dormancy PD model on time-to-sterilisation exists anywhere; (b) the slow-grower/fast-grower organism dependence is unpublished; (c) no model proposes accelerating resuscitation and computes a duration effect.
6. **Caution — self prior-art:** the author's own bioRxiv preprint (10.1101/2025.02.12.637810) already occupies the Mtb-vs-*S. aureus* slot and attributes the difference to the **kill rate**. The new claim contradicts it and must say so explicitly.

---

## 1. The three closest published papers

### #1 — Patra P, Klumpp S. "Population dynamics of bacterial persistence." PLoS ONE 2013;8(5):e62814.
- **PMID** 23675428 · **PMCID** PMC3652822 · **DOI** [10.1371/journal.pone.0062814](https://doi.org/10.1371/journal.pone.0062814)
- **OA:** Yes, full CC-BY. Full text read.
- **What it actually establishes.** Two-state linear ODE model (normal ↔ persister) with switching rates `a` (normal→persister) and `b` (persister→normal, i.e. the resuscitation rate). Under a small-switching-rate approximation the population ratio maps to a logistic equation and closed forms follow. The load-bearing result for this claim: the **steady-state decay rate of the total population under stress is `λ_eff^s ≈ λ_p^s − b`** — so the asymptotic (sterilising) kill slope is the persister death rate **plus** the resuscitation rate. Their own gloss: the presence of persisters "leads to a significant reduction in the steady state death rate of the total population under stress conditions." They also derive the biphasic transition time `t_c` and the regrowth delay, and give expressions for inverting killing/regrowth curves to recover `a` and `b`.
- **What it explicitly leaves open.** No time-to-sterilisation or treatment-duration quantity anywhere. No sensitivity analysis of any kind. No Hill/pharmacodynamic kill function — death rates are constants, not drug-concentration-dependent. No M. tuberculosis: their Table 1 of empirical switching rates lists only *E. coli* and *S. aureus*. No slow-grower/fast-grower contrast. Their stated conclusion about survival attributes it to the **persister fraction formed beforehand**, not to `b`.
- **Does it foreclose the claim?** **It forecloses the mathematics, not the claim.** Anyone competent reading Eq. (12–13) can see in one line that when `λ_p → 0` (persisters effectively unkilled, the slow-grower regime) the sterilisation rate collapses to `b` alone and time-to-sterilisation `≈ ln(N₀)/b`. That is the manuscript's central result, already derivable from a 2013 paper. The manuscript cannot present the mechanism as a discovery; it can present the *sensitivity ranking*, the *organism-dependent scaling*, and the *clinical framing* as new. **This is the paper a referee will cite to say "this is a corollary of a known result."**

### #2 — Magombedze G, Pasipanodya JG, Gumbo T. "Bacterial load slopes represent biomarkers of tuberculosis therapy success, failure, and relapse." Commun Biol 2021;4:664.
- **PMID** 34079045 · **PMCID** PMC8172544 · **DOI** [10.1038/s42003-021-02184-0](https://doi.org/10.1038/s42003-021-02184-0)
- **OA:** Yes, full. Companion: Magombedze et al., J Antimicrob Chemother 2020 (**PMID** 31713607, PMC6966096, [DOI 10.1093/jac/dkz460](https://doi.org/10.1093/jac/dkz460)); framework origin: Clin Infect Dis 2018 (**PMID** 30496464, [DOI 10.1093/cid/ciy623](https://doi.org/10.1093/cid/ciy623)).
- **What it actually establishes.** Two-subpopulation (fast-replicating `Cf`, non-replicating persister `Cs`) logistic model with four parameters — growth rates `rf`, `rs` and drug kill slopes `γf`, `γs` — fitted to serial sputum from **1,924 REMoxTB patients**, deriving a time-to-extinction that maps to required therapy duration. Verbatim: *"increasing or reducing the [γs] (i.e., speed of kill of slow-replicating bacteria) changes the time-to-extinction and therefore the required minimum duration of therapy"* — six months extends to eight when γs falls 0.148→0.131, and shortens to two months if γs rises to 0.286. CART variable importance: **γs ranked first at 100%**, initial burden second at 91.7%, γf not ranked. JAC 2020 states it flatly: *"Given that sterilization is slower than the bactericidal effect, the former is the rate-limiting process for shortening of treatment duration."*
- **What it explicitly leaves open.** **The model contains no phenotype-switching, resuscitation, or wake-up term at all** — the two subpopulations are uncoupled. The word "resuscitation" does not appear. So the resuscitation rate's absence from their ranking is a null result by construction, not evidence. Sensitivity work is LHS + Monte Carlo + CART; **no PRCC, Sobol, Morris or eFAST**.
- **Does it foreclose the claim?** **It forecloses the second clause outright.** "Dominating the direct kill rate of persisters" is falsified in the only large clinical dataset where a persister kill rate has been estimated against outcome. The first clause survives only because their model structurally cannot test it. Any manuscript asserting resuscitation beats persister kill rate must confront this paper head-on with clinical data, not illustrative parameters.

### #3 — Martinecz A, Boeree MJ, Diacon AH, et al. "High rifampicin peak plasma concentrations accelerate the slow phase of bacterial decline in tuberculosis patients: Evidence for heteroresistance." PLoS Comput Biol 2023;19(4):e1011000.
- **PMID** 37053266 · **PMCID** PMC10128972 · **DOI** [10.1371/journal.pcbi.1011000](https://doi.org/10.1371/journal.pcbi.1011000)
- **OA:** Yes, full CC-BY.
- **What it actually establishes.** Sets up precisely the dichotomy this claim inhabits — **persistence (switching between susceptible and non-susceptible states) vs heteroresistance (a distribution of susceptibilities)** — parameterises both against human rifampicin EBA trial data, and rejects persistence. Their argument: *"In persistence, the slow phase is driven by bacteria exiting a non-susceptible state which is commonly assumed to be independent of antibiotic concentrations. Therefore, higher antibiotic concentrations would not accelerate the slow phase."* The data show the slow phase **does** accelerate with rifampicin Cmax; they conclude the results are *"only compatible with the definitions of heteroresistance and not persistence."*
- **What it explicitly leaves open.** They used *in vitro* maximal replication rates and concede this is *"unlikely to be same as in vivo"* and *"would have introduced unknowns when it came to using the model of persistence"* — their persistence arm is the more weakly parameterised of the two. Analysis covers only EBA days 1–14, not the six-month duration horizon. They fall back to a weaker claim: *"the slowdown in elimination is caused by heterogeneous bacterial elimination rates."*
- **Does it foreclose the claim?** **It is the closest thing to a killer.** Not a "comes close" — a published negative result against the exact mechanism, in TB, in patients, by the group that owns the rival model. It does not formally foreclose (their test was of concentration-*in*dependence of the exit rate, a specific assumption the manuscript could relax), but a referee who knows this paper will demand the manuscript answer it before anything else.

---

## 2. Is the claim already published?

**PARTIALLY.** Split precisely:

| Component of the claim | Status |
|---|---|
| Dormant bacilli that intermittently resume metabolism set sterilising-drug requirements and therapy length | **Published (qualitatively), 1981.** Dickinson & Mitchison, PMID 6784622 — verbatim conclusion: bacilli *"dormant much of the time but occasionally metabolising for short periods."* Not a rate parameter, not a model. |
| The persister→normal exit rate rate-limits the slow phase of killing | **Published.** Implicit in Balaban et al. Science 2004 (PMID 15308767); stated explicitly by Abel zur Wiesch et al. 2015 as *"the rate of switching limits the rate of bacterial killing such that higher antibiotic doses do not produce additional killing."* |
| Terminal sterilisation slope = persister kill rate + resuscitation rate (the algebra) | **Published.** Patra & Klumpp 2013, Eq. (12–13). |
| Resuscitation rate **dominates** drug potency and replication rate for time-to-sterilisation, quantified | **NOT published.** No paper ranks it. |
| Resuscitation rate dominates **the persister kill rate** | **NOT published — and contradicted** by Magombedze 2021 / JAC 2020, and disfavoured by Martinecz 2023. |
| Sobol / variance-based GSA of any persister or dormancy PD model on time-to-sterilisation | **NOT published.** Searched extensively; nothing found. Prior GSA in this space is local (Carvalho 2018, ±20% OAT) or PRCC/CART on other outcomes. **This is a real methodological gap.** |
| Organism dependence: dominant in slow growers, negligible in fast growers | **NOT published.** See §4. |
| Scaling with the ratio of dormancy timescale to regrowth window | **NOT published** as an explicit scaling law. |

---

## 3. Rival explanations a referee will raise

Ordered by how much damage each does. **The single most dangerous is #1.**

| # | Rival explanation | Key citation(s) | OA | Force |
|---|---|---|---|---|
| **1** | **Drug–target binding kinetics + ~2% variance in target-molecule number is sufficient** to produce multiphasic kill, lag, post-antibiotic effect and inoculum effect — with **no persister subpopulation and no switching at all**. Reanalyses TB rifampicin trial data and reproduces weeks-long slow decline. | Abel zur Wiesch P et al., *Sci Transl Med* 2015;7:287ra73. PMID 25972005, [10.1126/scitranslmed.aaa8760](https://doi.org/10.1126/scitranslmed.aaa8760) | PMC4554720 | **Maximal — the parsimony objection.** |
| **1b** | Treatment length derived directly from a heterogeneity distribution + elimination-rate function, **with no switching/wake-up rate anywhere**. Competes for the exact quantity claimed. | Martinecz A & Abel zur Wiesch P, *Pathog Dis* 2018;76:fty065. PMID 30107522, [10.1093/femspd/fty065](https://doi.org/10.1093/femspd/fty065) | PMC6134427 | Very high |
| **1c** | Heteroresistance via multi-step reaction kinetics delays clearance "even with long antibiotic exposure". | Martinecz A et al., *IJMS* 2019;20:3965. PMID 31443146, [10.3390/ijms20163965](https://doi.org/10.3390/ijms20163965) | Yes | Moderate |
| **2** | **Slow-phase kill rate (sterilising activity) is itself the rate-limiting process** for treatment shortening — the clinical-data answer. | Magombedze et al., *Commun Biol* 2021 (PMID 34079045); *JAC* 2020 (PMID 31713607) | Yes | Very high |
| **3** | **Lesion pharmacokinetics** — drugs fail to penetrate caseum/granuloma; sterilising activity tracks lesion distribution, not bacterial physiology. | Prideaux B et al., *Nat Med* 2015;21:1223 (PMID 26343800, [10.1038/nm.3937](https://doi.org/10.1038/nm.3937)); Dartois V, *Nat Rev Microbiol* 2014;12:159 (PMID 24487820); Kjellsson MC et al., *AAC* 2012;56:446 (PMID 21986820) | All PMC | High — the TB field's default |
| **3b** | **Caseum microenvironment**, not non-replication per se, confers extreme tolerance; "non-replicating" is not one state with one exit rate. | Sarathy JP et al., *AAC* 2018;62:e02266-17. PMID 29203492 | PMC5786764 | High |
| **3c** | Multi-scale granuloma model: sterilisation times emerge from **spatial drug gradients + subpopulation PD**, no resumption rate. Competes on the manuscript's own terrain. | Pienaar E et al., *PLoS Comput Biol* 2017;13:e1005650. PMID 28817561 | Yes | High |
| **4** | **Persister fraction / formation rate** (not exit rate) is the clinically selected trait — `hip` mutants selected in patients; biphasic killing set by subpopulation size. | Balaban NQ et al., *Science* 2004;305:1622 (PMID 15308767, **not OA**); Lewis K, *Annu Rev Microbiol* 2010;64:357 (PMID 20528688, not OA); Balaban et al., *Nat Rev Microbiol* 2019;17:441 (PMID 30980069, PMC7136161) | mixed | High |
| **5** | **Growth-rate heterogeneity amplified by host immunity**; nongrowing-but-metabolically-active forms are host-driven and heterogeneous, not characterised by one exit rate. | Manina G et al., *Cell Host Microbe* 2015;17:32 (PMID 25543231, not OA); Manina G et al., *EMBO J* 2019;38:e101876 (PMID 31583725, PMC6856624) | mixed | High, double-edged |
| **6** | **Efflux-mediated tolerance in *replicating* bacteria** — the tolerant reservoir need not be dormant at all, so its resuscitation rate cannot govern. | Adams KN et al., *Cell* 2011;145:39. PMID 21376383, [10.1016/j.cell.2011.02.022](https://doi.org/10.1016/j.cell.2011.02.022) | PMC3117281 | **Very high for framing** |
| **7** | **Immune-mediated, lesion-level sterilisation** — individual granulomas sterilise independently; heterogeneity in killing, not dormancy exit, produces the long tail. | Lin PL et al., *Nat Med* 2014;20:75 (PMID 24336248, PMC3947310); Ankomah P & Levin BR, *PNAS* 2014;111:8331 (PMID 24843148) | Yes | High |
| **8** | **Stochastic extinction from burden** — a null model. Clearance is a first-passage event; times are heterogeneous purely from birth–death noise. | Coates J et al., *eLife* 2018;7:e32976 (PMID 29508699); Lipsitch M & Levin BR, *AAC* 1997;41:363 (PMID 9021193, PMC163715) | Yes | Moderate–high **as the baseline the GSA must beat** |
| **9** | Mitchison's four "special populations" — the classical framing the claim must be positioned against. | Mitchison DA, *Tubercle* 1985;66:219 (PMID 3931319, not OA) | No | Contextual |

---

## 4. Has anyone shown the organism dependence (slow vs fast growers)?

**No — with one important caveat that is self-inflicted.**

- **No published paper** demonstrates that resuscitation-rate importance is high for slow growers and negligible for fast growers. Patra & Klumpp tabulate switching rates for *E. coli* and *S. aureus* only and draw no contrast; Magombedze/Gumbo are Mtb-only; Carvalho 2018 is *Klebsiella*/generic biofilm; Himeoka & Mitarai are *E. coli*-generic.
- **CAVEAT — self-prior-art.** The bioRxiv preprint *"Comparative Modeling of Antibiotic Resistance, Tolerance, and Persistence in Mycobacterium tuberculosis and Staphylococcus aureus"* ([10.1101/2025.02.12.637810](https://doi.org/10.1101/2025.02.12.637810), posted 14 Feb 2025) is **authored by Vahhab Piranfar** — i.e. this project's own author. It already occupies the Mtb-vs-*S. aureus* comparative modelling slot, uses logistic growth + biphasic killing, and **attributes the difference to the kill rate** (Mtb 0.001/h vs *S. aureus* 0.2/h), concluding *"these findings highlight the necessity of prolonged therapy for tuberculosis."* It contains no resuscitation parameter and no GSA. This must be cited, and the new manuscript must explicitly explain why it now advances a *different* explanation for the same phenomenon, or referees and readers will read it as a contradiction of the author's own preprint.
- **Verdict on the title question:** the organism-dependence result, if properly demonstrated with fitted (not illustrative) parameters for at least two organisms, is the **most novel component of the whole claim** and is what would justify "Bacterial" over "in M. tuberculosis". With illustrative parameters only, it would not survive review.

---

## 5. Experimental support or contradiction

**Headline: no study — experimental or modelling — directly manipulates the resuscitation rate and measures time to clearance or required treatment duration.** Every candidate either manipulates resuscitation and measures something else (reactivation/relapse), or measures clearance and manipulates something else (drug potency). The claim is therefore **untested**, not merely unpublished.

### 5a. The discriminating experiment — and it goes the wrong way

**Russell-Goldman E, Chan J, Tufariello JD. Infect Immun 2008;76:4269.** PMID 18591237 · [10.1128/IAI.01735-07](https://doi.org/10.1128/IAI.01735-07) · OA (PMC2519441).
Modified Cornell model, NOS2−/− mice, INH+PZA for 3 months, then withdrawal. At the end of the **identical** drug course, lung counts were *"very low (<50)"* and **similar between ΔrpfAB and wild-type Erdman**; spleen and liver sterile in both. The mutant phenotype appeared only *after* withdrawal — median survival 237 d (ΔrpfAB) vs 143 d (WT).
→ **Crippling resuscitation delayed relapse but did not accelerate clearance and did not change the treatment needed.** This is the closest available test of the claim and it separates *relapse timing* from *clearance timing*, finding an effect only on the former. **The manuscript must cite this and explain whether its model predicts this dissociation.** (Caveat: not designed as a duration titration; both arms hit the same detection floor.) Same phenotype class from a different gene: Khan & Nandicoori, AAC 2021;65:e02095-20, PMID 33468473 — ΔpknG "drastically attenuated resuscitation after antibiotic treatment", again reported as reduced reactivation only.

### 5b. Rpf genetics — manipulates resuscitation, silent on clearance

| Study | Result | Verdict |
|---|---|---|
| Tufariello et al., Infect Immun 2004;72:515 (PMID 14688133, OA) | All five single rpf KOs grow normally in vitro and in mice | **Silent** — no drug treatment |
| Downing et al., Infect Immun 2005;73:3038 (PMID 15845511, OA) | Triple mutants cannot resuscitate spontaneously; singles = WT | **Silent**; Rpf loss is heavily buffered |
| Tufariello et al., Infect Immun 2006;74:2985 (PMID 16622237, OA) | ΔrpfB: delayed **reactivation**, prolonged survival | **Weak support** (reactivation ≠ clearance) |
| Kana et al., Mol Microbiol 2008;67:672 (PMID 18186793, OA) | Quintuple ΔrpfA–E viable; resuscitation abolished | **Silent**; rpfA–E collectively dispensable for growth |
| Biketov et al., BMC Infect Dis 2007;7:146 (PMID 18086300, OA) | Defective regrowth after immunosuppression | **Weak support** (reactivation only) |

**Note:** the genetics is entirely loss-of-function. **No study has over-expressed Rpf or added exogenous Rpf to test whether *faster* resuscitation shortens anything.** And Rpf machinery is five-fold redundant — a poor therapeutic lever.

### 5c. "Wake and kill" — real log-kill enhancement, but the mechanism is probably not waking

- **Allison, Brynildsen & Collins, Nature 2011;473:216** (PMID 21562562, PMC3145328). The canonical paper — and the authors state explicitly that potentiation **"does not rely on growth resumption"**; it works via PMF-driven aminoglycoside uptake. **Contradicts the mechanism as stated**; silent on duration.
- Barraud et al., PLoS One 2013;8:e84220 (PMID 24349568, OA) — mannitol+tobramycin, ~1,000-fold sensitisation, blocked by PMF inhibitor. PMF, not awakening.
- Koeva et al., AAC 2017;61:e00987-17 (PMID 28923873, OA) — fumarate+tobramycin, up to 6 logs. Fixed-timepoint kill.
- Marques/Davies et al., AEM 2014;80:6976 (PMID 25192989, OA) — cis-2-decenoic acid reverts persisters to a susceptible state **without increase in cell number**. **Supports the mechanism**, silent on duration.
- Roy et al., PLoS Pathog 2021;17:e1010144 (PMID 34890435, PMC8716142) — minocycline/eravacycline accumulate during dormancy (low efflux) and kill **on wake-up**. Cleanest mechanistic support for a resuscitation-coupled killing window, but the leverage is drug accumulation, not faster awakening.

**None of these measures time to eradication.** All measure log-kill at a fixed time, and the mechanistic weight of evidence is PMF/drug-uptake rather than resuscitation kinetics.

### 5d. The competing causal lever has the better duration data — CONTRADICTS

The Hu/Coates Cornell series are the only studies that measure **time to organ sterility** and **relapse** while tracking Rpf-dependent persisters — and in every one, duration was shortened by **raising the kill rate of the dormant compartment**, with resuscitation used purely as a detection assay:

- Hu et al., Front Microbiol 2015;6:641 (PMID 26157437, OA) — high-dose rifampicin: sterility at **8 wk vs 14 wk**; relapse 0% vs 87.5%.
- Liu et al., JAC 2018;73:724 (PMID 29244108) — rifampicin ≥30 mg/kg: sterility 8–11 wk; relapse fully prevented vs 86%.
- Hu et al., JAC 2019;74:1627 (PMID 30789209) — bedaquiline: clearance 8 vs 14 wk, zero relapse.
- Liu et al., AAC 2018;62:e00190-18 (PMID 29661869, OA) — moxifloxacin clears CFU faster but **fails to remove CF-dependent persisters at all**.

### 5e. Rpf-dependent DCTB in patients — mixed, and one direct contradiction

- **Supports (correlational):** Mukamolova et al., AJRCCM 2010;181:174 (PMID 19875686, OA) — 80–99.99% of viable bacilli in pre-treatment sputum are Rpf-dependent, and that fraction rises during chemotherapy. Turapov et al., AAC 2016;60:2476 (PMID 26883695, OA) — supernatant-dependent Mtb is *more* drug-tolerant.
- **Supports weakly:** Peters et al., Front Cell Infect Microbiol 2023;12:1064148 (PMID 36710965, OA) — 74% (46/62) had residual DCTB at treatment completion and both recurrences were in that group; but with a 74% base rate and n=2 events this is near-useless as a positive predictor.
- **Weakens:** Chengalroyen et al., AJRCCM 2016;194:1532 (PMID 27387272, OA) — a substantial **Rpf-independent** DCTB population exists, so Rpf-mediated resuscitation is not the sole gate.
- **CONTRADICTS:** Almeida Júnior et al., Tuberculosis 2020;124:101945 (PMID 32692652) — 17 patients through 6-month therapy: **no bacillary recovery after 2 months, with or without culture-filtrate supplementation.** Directly opposes a picture in which a slowly-resuscitating reservoir persists detectably through months 2–6 and governs duration.

### 5f. Is the dormant compartment even well-posed?

- Orman & Brynildsen, AAC 2013;57:3230 (PMID 23629720, OA) — **>99% of "dormant" cells are not persisters**, and rapidly growing cells can become persisters.
- Conlon et al., Nat Microbiol 2016;1:16051 (PMID 27572649, OA) and Zalis et al., mBio 2019;10:e01930-19 (PMID 31530676, OA) — persistence tracks **ATP level** / stochastic TCA expression.
→ If persisters are a continuum of energy states rather than a discrete dormant compartment, **the resuscitation rate is not a well-defined parameter** — an attack on the model structure, not just the ranking.

---

## 6. Citation table

| # | Citation | PMID | DOI | OA | Role |
|---|---|---|---|---|---|
| 1 | Patra & Klumpp, PLoS ONE 2013;8:e62814 | 23675428 | 10.1371/journal.pone.0062814 | Yes (PMC3652822) | **Closest paper** — contains the algebra |
| 2 | Magombedze et al., Commun Biol 2021;4:664 | 34079045 | 10.1038/s42003-021-02184-0 | Yes (PMC8172544) | **Contradicts clause 2** |
| 3 | Magombedze et al., JAC 2020;75:224 | 31713607 | 10.1093/jac/dkz460 | Yes (PMC6966096) | Sterilisation is rate-limiting for duration |
| 4 | Magombedze et al., Clin Infect Dis 2018 | 30496464 | 10.1093/cid/ciy623 | Partial (PMC6260172) | Time-to-extinction framework origin |
| 5 | Martinecz et al., PLoS Comput Biol 2023;19:e1011000 | 37053266 | 10.1371/journal.pcbi.1011000 | Yes (PMC10128972) | **Published negative result vs mechanism** |
| 6 | Abel zur Wiesch et al., Sci Transl Med 2015;7:287ra73 | 25972005 | 10.1126/scitranslmed.aaa8760 | Yes (PMC4554720) | **Most dangerous rival** |
| 7 | Martinecz & Abel zur Wiesch, Pathog Dis 2018;76:fty065 | 30107522 | 10.1093/femspd/fty065 | Yes (PMC6134427) | Treatment length without switching |
| 8 | Dickinson & Mitchison, Am Rev Respir Dis 1981;123:367 | 6784622 | 10.1164/arrd.1981.123.4.367 | No | **Qualitative priority, 1981** |
| 9 | Mitchison, Tubercle 1985;66:219 | 3931319 | 10.1016/0041-3879(85)90040-6 | No | Special populations hypothesis |
| 10 | Balaban et al., Science 2004;305:1622 | 15308767 | 10.1126/science.1099390 | No | Switching model; exit rate limits killing |
| 11 | Carvalho G et al., npj Biofilms Microbiomes 2018;4:6 | 29560270 | 10.1038/s41522-018-0049-2 | Yes (PMC5854711) | Wake-up rate × treatment duration, IBM |
| 12 | Carvalho G et al., Microb Biotechnol 2017;10:1616 | 28730700 | 10.1111/1751-7915.12739 | Yes | Switching rates vs substrate/antibiotic |
| 13 | Himeoka & Mitarai, PLoS Comput Biol 2021;17:e1008655 | 33571191 | 10.1371/journal.pcbi.1008655 | Yes (PMC7904209) | Optimal wake-up time (fitness, not duration) |
| 14 | Lohmar & Meerson, Phys Rev E 2011;84:051901 | — | 10.1103/PhysRevE.84.051901 | arXiv:1107.5192 | Extinction risk under phenotype switching |
| 15 | Cogan NG, J Theor Biol 2006;238:694 | 16125727 | 10.1016/j.jtbi.2005.06.017 | No | Dose/withdrawal timing vs persisters |
| 16 | De Leenheer & Cogan, J Math Biol 2009;59:563 | 19083238 | 10.1007/s00285-008-0243-6 | No | Speed of wipe-out vs dosing duration |
| 17 | Cogan NG et al., FEMS Microbiol Lett 2016;363:fnw264 | 27915255 | 10.1093/femsle/fnw264 | No | **Wake-and-kill timing, theory + experiment** |
| 18 | Clewe O et al., JAC 2016;71:964 | 26702921 | 10.1093/jac/dkv416 | Yes (PMC4790616) | MTP model — has k_NS/k_SF transfer rates |
| 19 | Svensson & Simonsson, CPT PSP 2016;5:264 | 27299939 | 10.1002/psp4.12079 | Yes (PMC4873565) | MTP in patients |
| 20 | Fang X & Allison KR, Mol Syst Biol 2023;19:e11320 | 36866643 | 10.15252/msb.202211320 | Yes (PMC10090945) | Resuscitation is exponential, not stochastic |
| 21 | Pu Y et al., Mol Cell 2019;73:143 | 30472191 | 10.1016/j.molcel.2018.10.022 | No | Dormancy depth sets resuscitation lag |
| 22 | Fridman O et al., Nature 2014;513:418 | 25043002 | 10.1038/nature13469 | No | Lag time evolves to match exposure duration |
| 23 | Prideaux B et al., Nat Med 2015;21:1223 | 26343800 | 10.1038/nm.3937 | Yes (PMC4598290) | Lesion PK rival |
| 24 | Sarathy JP et al., AAC 2018;62:e02266-17 | 29203492 | 10.1128/AAC.02266-17 | Yes (PMC5786764) | Caseum tolerance rival |
| 25 | Pienaar E et al., PLoS Comput Biol 2017;13:e1005650 | 28817561 | 10.1371/journal.pcbi.1005650 | Yes | Multi-scale granuloma rival |
| 26 | Adams KN et al., Cell 2011;145:39 | 21376383 | 10.1016/j.cell.2011.02.022 | Yes (PMC3117281) | Efflux tolerance in replicating cells |
| 27 | Lin PL et al., Nat Med 2014;20:75 | 24336248 | 10.1038/nm.3412 | Yes (PMC3947310) | Lesion-level immune sterilisation |
| 28 | Coates J et al., eLife 2018;7:e32976 | 29508699 | 10.7554/eLife.32976 | Yes | Stochastic extinction null model |
| 29 | Lipsitch & Levin, AAC 1997;41:363 | 9021193 | 10.1128/AAC.41.2.363 | Yes (PMC163715) | Foundational within-host framework |
| 30 | Piranfar V, bioRxiv 2025 | — | 10.1101/2025.02.12.637810 | Preprint | **Self prior-art, Mtb vs S. aureus** |
| 31 | Russell-Goldman E et al., Infect Immun 2008;76:4269 | 18591237 | 10.1128/IAI.01735-07 | Yes (PMC2519441) | **Discriminating experiment — clearance unchanged** |
| 32 | Kana BD et al., Mol Microbiol 2008;67:672 | 18186793 | 10.1111/j.1365-2958.2007.06078.x | Yes (PMC2229633) | Quintuple ΔrpfA–E; resuscitation abolished |
| 33 | Tufariello JD et al., Infect Immun 2006;74:2985 | 16622237 | 10.1128/IAI.74.5.2985-2995.2006 | Yes (PMC1459759) | ΔrpfB delays reactivation |
| 34 | Downing KJ et al., Infect Immun 2005;73:3038 | 15845511 | 10.1128/IAI.73.5.3038-3043.2005 | Yes (PMC1087353) | Triple rpf mutants cannot resuscitate |
| 35 | Allison KR et al., Nature 2011;473:216 | 21562562 | 10.1038/nature10069 | Yes (PMC3145328) | Wake-and-kill; **"does not rely on growth resumption"** |
| 36 | Marques CNH et al., AEM 2014;80:6976 | 25192989 | 10.1128/AEM.01576-14 | Yes (PMC4249009) | cis-DA reverts persisters without regrowth |
| 37 | Roy S et al., PLoS Pathog 2021;17:e1010144 | 34890435 | 10.1371/journal.ppat.1010144 | Yes (PMC8716142) | Kill-on-wake-up via low efflux |
| 38 | Hu Y et al., Front Microbiol 2015;6:641 | 26157437 | 10.3389/fmicb.2015.00641 | Yes (PMC4477163) | **Duration shortened by raising kill rate** |
| 39 | Liu Y et al., JAC 2018;73:724 | 29244108 | 10.1093/jac/dkx467 | No | High-dose RIF: sterility 8–11 wk, no relapse |
| 40 | Mukamolova GV et al., AJRCCM 2010;181:174 | 19875686 | 10.1164/rccm.200905-0661OC | Yes (PMC2809243) | Rpf-dependent DCTB dominant in sputum |
| 41 | Chengalroyen MD et al., AJRCCM 2016;194:1532 | 27387272 | 10.1164/rccm.201604-0769OC | Yes (PMC5215032) | Rpf-**in**dependent DCTB exists |
| 42 | Almeida Júnior PS et al., Tuberculosis 2020;124:101945 | 32692652 | 10.1016/j.tube.2020.101945 | No | **Contradicts persistent DCTB reservoir** |
| 43 | Orman MA & Brynildsen MP, AAC 2013;57:3230 | 23629720 | 10.1128/AAC.00243-13 | Yes (PMC3697331) | >99% of dormant cells are not persisters |
| 44 | Conlon BP et al., Nat Microbiol 2016;1:16051 | 27572649 | 10.1038/nmicrobiol.2016.51 | Yes (PMC4932909) | Persistence tracks ATP, not a discrete state |
| 45 | Cogan NG et al., AAC 2012;56:4816 | 22751538 | 10.1128/AAC.00675-12 | Yes (PMC3421875) | Optimal control: cycling gives fastest killing |
| 46 | Martinecz A et al., IJMS 2019;20:3965 | 31443146 | 10.3390/ijms20163965 | Yes | Heteroresistance kinetics delay clearance |
| 47 | Adams KN et al., J Infect Dis 2014;210:456 | 24532601 | 10.1093/infdis/jiu095 | Yes (PMC4110457) | Efflux tolerance extended to newer drugs |
| 48 | Dartois VA & Rubin EJ, Nat Rev Microbiol 2022;20:685 | 35478222 | 10.1038/s41579-022-00731-y | Yes | Individualised duration by disease severity |

---

## 7. What to do before writing

1. **Delete "dominating the direct kill rate of persisters."** It is falsified in the only large clinical dataset (Magombedze 2021) and is the easiest thing for a referee to kill. Reframe as *rivals or exceeds* only if you can show it with fitted parameters.
2. **Cite Dickinson & Mitchison 1981 pre-emptively** and position the work as the quantitative formalisation of their hypothesis, not as a new one.
3. **Answer Martinecz 2023 head-on.** Their test was of concentration-*independence* of the exit rate; if your model relaxes that, say so. Their own hedges (in vitro replication rates, EBA days 1–14 only) are the footholds.
4. **Answer Russell-Goldman 2008.** Does your model predict the dissociation between delayed relapse and unchanged clearance? If not, that is a structural problem.
5. **Beat the null models.** Show the resuscitation signal survives against (a) target-binding heterogeneity (Abel zur Wiesch 2015), (b) stochastic extinction from burden (Coates 2018), (c) lesion PK (Prideaux 2015).
6. **Fit the parameters.** With illustrative parameters, the Sobol indices (0.87/0.90) are a statement about the chosen ranges, not about biology. The organism-dependence result — the only genuinely novel component — will not survive review otherwise.
7. **Disclose and reconcile the self prior-art preprint.**
8. **Lead with the methodological gap**, which is real and defensible: no variance-based GSA of a persister/dormancy PD model on time-to-sterilisation exists.
