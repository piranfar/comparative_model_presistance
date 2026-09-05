# Growth regime determines which parameters govern antibiotic killing in a state-structured pharmacodynamic model

**Vahhab Piranfar**

1. Independent Researcher, Jersey City, NJ, USA
2. Farname Inc, Ontario, Canada

Corresponding author: Vahhab Piranfar · vahab.p@gmail.com · ORCID 0000-0003-3653-5739

---

## Abstract

Resistance, tolerance and persistence differ in their concentration and killing-time signatures. Representing all three solely by changes in a single exponential decay rate cannot preserve those distinctions. We analyse a two-compartment pharmacodynamic model with replicating and dormant populations and state-specific sigmoid concentration–responses. All data are synthetic, and two illustrative parameter sets represent slow- and fast-growth regimes. The prescribed phenotype changes produce distinct signatures across the minimum inhibitory concentration and shallow and deep killing endpoints, while biphasic killing emerges without a fitted breakpoint. Variance-based sensitivity analysis of time to the limit of detection (time to LOD) gives sharply different rankings in the two regimes. In the slow-growth set, the resuscitation rate has a first-order Sobol index of 0.780; in the fast-growth set, its total-order index is small but nonzero, at $2.3 \times 10^{-5}$. Interactions collectively account for approximately 69.5% of the fast-growth variance, without identifying the contribution of any specific parameter pair. Profile likelihood indicates that the fitted transition time of the closed-form comparator is not practically identifiable in the four synthetic sampling designs examined. High coefficients of determination coexist with a discontinuity in that comparator and therefore do not establish model adequacy. The results connect model structure, endpoint sensitivity and practical identifiability: a parameter's importance depends on the regime and exposure convention, and a close fit does not establish that its mechanistic interpretation is determined by the data.

**Keywords:** antibiotic tolerance, bacterial persistence, pharmacodynamics,
minimum duration for killing, practical identifiability, global sensitivity
analysis

---

## 1. Introduction

The minimum inhibitory concentration describes growth inhibition, not the full time course of bacterial killing. Populations with similar susceptibility can differ in how rapidly they decline and in the survivors remaining after the initial decline. Resistance, tolerance and persistence distinguish these features of antibiotic response (Brauner et al. 2016; Balaban et al. 2019).

Resistance raises the concentration required to inhibit growth. Tolerance leaves
that concentration where it is and extends the time required to kill. Persistence
describes prolonged survival in a subpopulation and is expressed most clearly in
the slow tail of the killing curve (Lewis 2007; Levin and Rozen 2006). The
operational definitions are quantitative and, in principle, measurable: a shift
in the minimum inhibitory concentration, a shift in the minimum duration for
killing at a fixed concentration, and a change in the shape of the deep tail of
the killing curve.

A single exponential, $N(t)=N_0e^{-kt}$, assigns the entire population one constant decay rate. Changing that rate changes killing duration, but cannot represent a distinct slow tail or a concentration shift when concentration is absent from the formulation. The objection concerns this restricted representation, not every model containing an exponential term. No fitting procedure recovers a distinction the model does not contain.

A state-structured model makes those distinctions expressible. Here, two compartments represent populations with different drug responses, and explicit concentration–response functions separate concentration dependence from temporal population dynamics. This is one way to represent heterogeneous killing; it does not establish that two discrete biological states are uniquely required.

The analysis addresses three connected questions. First, do the prescribed phenotype changes leave distinct signatures across concentration and killing endpoints? Second, which parameters account for variation in time to LOD in the two illustrative growth regimes? Third, which fitted quantities are determined by the synthetic observations, and which model defects remain compatible with a high $R^2$?

The distinction between the last two questions matters. Sensitivity describes how an outcome varies over a specified input distribution. Identifiability describes what observations determine about a fitted parameter. A parameter can dominate an outcome without being separately estimable. The results below concern these mathematical properties in synthetic examples, rather than species-specific treatment durations.

## 2. A state-structured pharmacodynamic model

### 2.1 The model

Let $S(t)$ be the density of replicating cells and $P(t)$ the density of dormant
cells, both in colony-forming units per millilitre, under a constant drug
concentration $C$ expressed in multiples of a reference minimum inhibitory
concentration. Cells replicate logistically, switch between the two states, and
are killed at a rate set by a sigmoid concentration–response:

$$\frac{dS}{dt} = rS\left(1 - \frac{S+P}{K}\right) - k_{S\to P}S + k_{P\to S}P - E_S(C)\,S$$

$$\frac{dP}{dt} = k_{S\to P}S - k_{P\to S}P - E_P(C)\,P$$

with Hill kill functions

$$E_S(C) = \frac{E_{\max,S}\,C^{H}}{EC_{50}^{H} + C^{H}}, \qquad
E_P(C) = \frac{E_{\max,P}\,C^{H}}{(\rho\, EC_{50})^{H} + C^{H}}$$

where $r$ is the replication rate, $K$ the carrying capacity, $k_{S\to P}$ and
$k_{P\to S}$ the switching rates into and out of dormancy, $E_{\max,S}$ and
$E_{\max,P}$ the maximum kill rates of the two compartments, $EC_{50}$ the
concentration giving half-maximal kill of replicating cells, $H$ the Hill
coefficient, and $\rho$ the ratio of the dormant compartment's $EC_{50}$ to that
of the replicating compartment. The kill functions follow Regoes et al. (2004);
the two-compartment structure is standard (Nielsen and Friberg 2013).

### 2.2 The three strategies as parameter changes

Each phenotype is represented by a prescribed parameter change. The endpoint
signatures are computed from those choices.

**Resistance** multiplies $EC_{50}$ by a fold change. The concentration required
for half-maximal kill rises; the maximum achievable kill rate does not change.

**Tolerance** divides $r$, $E_{\max,S}$ and $E_{\max,P}$ by the same factor, representing a joint reduction in replication and killing. In the reported comparison, the resulting MIC is unchanged to the displayed precision. Because the switching rates are not scaled with these rates, this construction does not impose a uniform rescaling of the entire trajectory.

**Persistence** raises $k_{S\to P}$, enlarging the dormant subpopulation while leaving the replication and kill-rate parameters unchanged.

### 2.3 The state of the inoculum

The dormant fraction used here is determined by the assumed initial growth state. In a population held
at carrying capacity, where replication has stopped, switching balances at
$f = k_{S\to P}/(k_{S\to P} + k_{P\to S})$. The simulations here start from a growing population, where replication keeps
refilling the replicating compartment faster than switching drains it.

Taking $S$ and $P$ to grow exponentially at a common rate $\lambda$ gives
$P/S = k_{S\to P}/(\lambda + k_{P\to S})$, giving the following initialisation for the dormant fraction

$$f = \frac{k_{S\to P}}{\lambda + k_{P\to S} + k_{S\to P}}, \qquad
\lambda^2 + \lambda\left(k_{S\to P} + k_{P\to S} - r_{\text{eff}}\right)
- r_{\text{eff}}\,k_{P\to S} = 0$$

with $r_{\text{eff}} = r(1 - N_0/K)$, evaluated at the initial density rather than held fixed throughout the subsequent logistic trajectory. At $r_{\text{eff}} = 0$ this returns
$\lambda = 0$ and collapses to the stationary-phase expression, as it must. While
the population grows it is smaller: fourfold for the slow grower of Section 2.5
and sixfold for the fast one. Initialising at the stationary-phase value and then
integrating an exponentially growing population overstates the dormant pool of
the inoculum by that factor. The trajectory inherits the error, but does not
preserve it: once killing begins the compartment ratio evolves under the drug, so
the discrepancy is a function of time rather than a constant offset.

### 2.4 Endpoints

Four quantities are computed from each solution, chosen because each is
measurable and because the operational definitions are stated in terms of them.

- **MIC** (minimum inhibitory concentration), defined here as the lowest concentration at which the net growth rate of the bulk
  population is non-positive, obtained by root-finding on the initial net growth
  rate of the inoculum in the state it actually starts from.
- **MDK$_{99}$** and **MDK$_{99.99}$** (minimum durations for killing), the times to two- and four-log$_{10}$
  reduction: the shallow and deep killing endpoints.
- **Time to LOD**, the time at which the population first falls below an assay
  limit of detection (LOD), taken as $10^2$ CFU/mL.

The MIC definition is an initial net-growth threshold within the model; equivalence to an assay MIC is not established here. Time to LOD is a detection endpoint, not time to sterilisation. Falling below
a detection limit is not sterility: true sterilisation is an extinction event at
small copy number, which a deterministic model cannot represent.

### 2.5 Parameter values

Two illustrative parameter sets stand for a slow grower and a fast grower.
Values are chosen to reproduce documented qualitative behaviour — replication
rates differing by more than an order of magnitude, dormant subpopulations of
order $10^{-3}$ to $10^{-4}$, and a dormant compartment far harder to kill than a
replicating one — and are not fitted to any dataset. They are inputs to a
structural argument, not estimates. Table 1 gives every value, the quantities
derived from them, and the settings under which the synthetic observations are
generated, so that the analyses can be reproduced without reading the code.
**Table 1** Parameter values of the two illustrative sets. Values are chosen to reproduce documented qualitative behaviour and are not fitted to any dataset. The two labels denote a slow-growth and a fast-growth parameterisation; they are not claims about the named organisms.

| Symbol | Meaning | Unit | M. tuberculosis | S. aureus |
|---|---|---|---|---|
| $r$ | Replication rate of the replicating compartment | h⁻¹ | $0.03$ | $0.5$ |
| $K$ | Carrying capacity | CFU/mL | $10^{9}$ | $10^{9}$ |
| $E_{\max,S}$ | Maximum kill rate, replicating compartment | h⁻¹ | $0.25$ | $1.2$ |
| $E_{\max,P}$ | Maximum kill rate, dormant compartment | h⁻¹ | $0.004$ | $0.05$ |
| $EC_{50}$ | Half-maximal kill concentration, replicating | reference MIC | $1$ | $1$ |
| $H$ | Hill coefficient | — | $1.5$ | $1.5$ |
| $k_{S\to P}$ | Switching rate into dormancy | h⁻¹ | $1.01 \times 10^{-4}$ | $10^{-4}$ |
| $k_{P\to S}$ | Resuscitation rate out of dormancy | h⁻¹ | $0.01$ | $0.1$ |
| $\rho$ | EC50 of the dormant compartment, relative | — | $3$ | $3$ |

Quantities derived from these values by the same functions the simulations call:

| Derived quantity | M. tuberculosis | S. aureus |
|---|---|---|
| MIC (reference MIC units) | 0.2647 | 0.7981 |
| Dormant fraction of the inoculum at $N_0=10^6$ | 0.00253 | 0.000167 |
| Dormant fraction at carrying capacity | 0.01 | 0.000999 |

Inoculum $N_0 = 10^6$ CFU/mL and limit of detection 100 CFU/mL throughout.

**Phenotype constructions.** The signature comparison of Section 3.2 starts from the slow-growth set with the dormant fraction lowered to $k_{S\to P} = 5.0025 \times 10^{-6}$ h⁻¹ so that the baseline is not already persistent, and applies one change at a time: resistance multiplies $EC_{50}$ by 16, tolerance divides $r$, $E_{\max,S}$ and $E_{\max,P}$ by 4, and persistence multiplies $k_{S\to P}$ by 10. Duration endpoints are evaluated at 8 times each variant's own MIC.

**Synthetic observations.** Time-kill data for the fitting analyses are generated from the state-structured model of Section 2.1 at four times each set's own MIC, with additive Gaussian noise on $\log_{10}$ CFU/mL of standard deviation 0.25 for a single plate, three replicates per time point, and observations below the limit of detection recorded as censored. The generator is seeded, so the datasets are reproducible. Sampling schedules:

| Set | Design | Times (h) |
|---|---|---|
| Mtb | sparse (8-point, 240 h) | 0, 24, 48, 72, 96, 144, 192, 240 |
| Mtb | dense (14-point, 240 h) | 0, 6, 12, 24, 36, 48, 72, 96, 120, 144, 168, 192, 216, 240 |
| S. aureus | sparse (8-point, 48 h) | 0, 2, 4, 8, 12, 24, 36, 48 |
| S. aureus | dense (16-point, 48 h) | 0, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 30, 36, 42, 48 |

### 2.6 Exposure

For the trajectory and sensitivity analyses, concentration is set to four times the minimum inhibitory concentration *of the
parameter set being simulated*, recomputed for every draw. The alternative, a
single absolute concentration applied to every parameter set, compares organisms
of different susceptibility at different multiples of their own MIC: for the two
sets used here, a common absolute concentration of four reference-MIC units is
15.1 times the MIC of the slow grower and 5.0 times that of the fast one, and any
between-organism contrast then carries that difference inside it. Normalising to
each set's own MIC also closes the route by which $EC_{50}$ acts on the outcome
through exposure, so the two conventions ask different questions; the two exposure conventions are included in the saved sensitivity outputs. The phenotype comparison in Section 3.2 uses eight times each variant's own MIC for its duration endpoints.

### 2.7 Sensitivity, estimation and identifiability

First- and total-order Sobol indices were computed with the Saltelli estimator
over $\pm50\%$ log-uniform ranges on seven parameters, from 4,096 base samples,
giving 36,864 model evaluations per parameter set, with 2,000-sample bootstrap
intervals on every index. Smaller designs return negative first-order estimates
for parameters carrying no variance, which is a statement about Monte Carlo error
rather than about the model, and the bootstrap intervals are reported so that a
reader can tell the two apart.

Fitting was performed on synthetic data with known ground truth, since no
experimental dataset is used in this work. On the observation scale, left-censored values contribute the Gaussian cumulative probability below the detection threshold to the log-likelihood (Beal 2001), with $\sigma$ estimated alongside the parameters;
assigning such points a zero residual gives a workable objective but not a
likelihood, and information criteria built on it do not have their usual meaning.
Model comparison used the corrected Akaike information criterion (AICc) and Bayesian information criterion (BIC) from that likelihood, and parameter
identifiability was assessed by profile likelihood, re-optimising all other
parameters and $\sigma$ at each fixed value and taking the interval where
$2(\ell_{\max}-\ell)$ stays below the $\chi^2_1$ 95% quantile.

### 2.8 Use of a large language model

OpenAI Codex was used to revise the manuscript's argument and organisation, draft and revise the Discussion and Conclusion, check consistency of terminology and claims, and prepare draft figure captions and declarations. This use extended beyond language editing. During this revision, the tool consulted selected published sources and inspected existing project tables and limited code excerpts; it did not rerun the simulations or independently validate the figures or all quantitative results.

[Author to complete before submission: identify any additional LLM use in model development, coding or analysis, including the tool and version where known, and describe the human review and verification actually performed. Final human approval and numerical verification are not asserted in this draft.]

## 3. Results

### 3.1 State structure generates biphasic killing

Biphasic killing does not have to be put into a model by hand. Under a constant
exposure of four times MIC, both parameter sets produce a killing curve with a
sharp initial decline and a slow tail, and the curvature maximum separating the
two phases appears at 61.5 h for the slow grower and 18.5 h for the fast one
(Figure 1). Neither number was supplied. Both are derived observables,
consequences of the rate at which the replicating compartment is depleted
relative to the rate at which the dormant compartment is refilled and killed.

The closed-form comparator instead includes a fitted transition time $t_c$. Its breakpoint and the curvature maximum of a smooth trajectory are different definitions of a transition. Sections 3.4 and 3.5 assess the practical identifiability and fit of this particular comparator; they do not establish a defect shared by all closed-form biphasic models.

The reported time to LOD is 347 h for the slow-growth set and 19 h for the fast-growth set. The corresponding values with dormant killing set to zero are 370 h and 20 h, changes of approximately 7% and 5%. In these examples, direct dormant killing contributes to the endpoint but is not required for the population to cross the detection threshold. The compartment trajectories attribute most dormant-pool depletion to exit into the replicating compartment, where killing is faster. This interpretation concerns the reported trajectories and does not by itself establish a general sensitivity ranking.

### 3.2 Resistance, tolerance and persistence produce distinct phenotypic signatures

Imposing each strategy on the same parameter set, one mechanism at a time,
produces distinct endpoint signatures in the synthetic comparison (Table 2, Figure 2).

**Table 2** Phenotypic signatures at eight times each variant's own MIC. MIC values are ratios to the baseline; baseline MDK values are in hours and variant MDK values are fold changes relative to that baseline. Ratios are rounded to the displayed precision.

| | MIC | MDK$_{99}$ | MDK$_{99.99}$ |
|---|---|---|---|
| wild type | 1.00× | 29.1 h | 67.6 h |
| resistant | **16.0×** | 1.00× | 1.00× |
| tolerant | 1.00× | **4.00×** | 3.67× |
| persistent | 1.00× | 1.02× | **3.65×** |

Resistance shifts the MIC sixteen-fold while leaving both duration endpoints unchanged at matched multiples of each variant's MIC. Tolerance increases MDK$_{99}$ fourfold and MDK$_{99.99}$ 3.67-fold, with MIC unchanged to the displayed precision. Persistence has its largest effect on the deep endpoint: MDK$_{99.99}$ rises 3.65-fold, while MDK$_{99}$ changes by approximately 2.5%.

These are distinct phenotypic signatures, not independent axes. The persistence example changes the shallow endpoint as well as the deep one, and the tolerance example does not scale both durations identically. The deep endpoint carries the strongest contrast between the baseline and persistence examples. This separation demonstrates the descriptive capacity of the model under the prescribed changes; it is not a validated classifier of clinical isolates.

### 3.3 Growth regime determines the sensitivity landscape

The sensitivity ranking differs sharply between the two illustrative growth regimes (Figure 3).

For the slow-growth set, the resuscitation rate $k_{P\to S}$ accounts for 78.0% of the output variance through its first-order contribution, with a 95% bootstrap interval of 0.640 to 0.916 and a total-order index of 0.799 (0.769 to 0.830). No other parameter reaches a first-order index of 0.08. Interactions collectively account for 2.3% of the variance. Resuscitation dominates this decomposition; the remaining parameters still contribute.

For the fast-growth set, the same parameter has a small but nonzero total-order index of $2.3 \times 10^{-5}$, with a bootstrap interval of $(1.9\text{–}2.7) \times 10^{-5}$. Its first-order interval spans zero. The maximum replicating-cell kill rate and replication rate have total-order indices of 0.819 (0.706 to 0.935) and 0.821 (0.713 to 0.942), respectively, compared with first-order indices of 0.169 and 0.136. Both participate strongly in interactions. The indices do not isolate their pairwise interaction: total-order contributions include every interaction involving the parameter and cannot be added as disjoint variance shares.

Interactions collectively account for 69.5% of the fast-growth variance, as estimated by one minus the sum of the first-order indices. A one-at-a-time analysis does not recover this variance decomposition. The result supports joint parameter analysis, but does not assign 69.5% to a specific pair or quantify the effect of a particular intervention.

The trajectories in Section 3.1 provide a mechanistic interpretation of the slow-growth ranking. In the fast-growth example, resuscitation contributes very little to variation in time to LOD over the tested range. That endpoint-specific result does not mean the parameter has no effect on the underlying trajectory.

Both sets use four times their own MIC, matching relative susceptibility-adjusted exposure. This does not match absolute concentration or every state-specific drug effect. The contrast is established for the stated input distributions and parameter sets; robustness to alternative ranges or distributions was not tested. Section 4.1 considers how this model-level result relates to existing biological interpretations.

### 3.4 Which parameters can the data identify?

A model that fits is not the same as a model whose parameters are determined, and
the transition time of the closed-form biphasic law is a clear case of the
difference.

Fitting that law to synthetic time-kill data at four sampling designs — sparse
and dense, for both organisms — gives close fits in every case. Profile
likelihood on the same fits shows that $t_c$ is not practically identifiable in
any of them. The 95% likelihood interval reaches the edge of the searched range
in four of four designs, including the two dense ones, and the point estimate
lies on the optimiser bound in three (Figure 4). The open intervals provide the direct evidence for the practical identifiability conclusion.

A separate issue concerns the meaning assigned to a transition time. For a biexponential mixture with initial slow-population fraction
$f$ and rates $k_{\text{fast}}$ and $k_{\text{slow}}$, the equal-contribution crossover time is

$$t_c = \frac{\ln[(1-f)/f]}{k_{\text{fast}} - k_{\text{slow}}}$$

This crossover is derived from the mixture parameters. It is not automatically the breakpoint of a piecewise model or the curvature maximum of the state-structured trajectory. A derived quantity can retain interpretive value, and a phenomenological breakpoint can be a useful descriptor. Neither status establishes whether it can be estimated accurately.

The result here is narrower and direct: the tested synthetic designs do not determine the comparator's fitted $t_c$ within the searched range. No structural identifiability analysis was performed. The slow rate of the biexponential has closed profile intervals for the slow-growth set in both designs and open intervals in both fast-growth designs. Closure is necessary but not sufficient for a useful estimate: of the two closed intervals only the sparse slow-growth one is narrower than its own point estimate, which is the additional criterion recorded in the results table. This concerns the fitted slow rate, not separate identification of the state-structured model's resuscitation rate.

### 3.5 Model selection needs more than $R^2$

Across the four synthetic designs, both models have $R^2>0.9$ in three cases (Figure 5). The saved comparison table gives a maximum absolute difference of 0.104. The closed-form comparator nevertheless contains a second branch that returns to the inoculum at the transition, producing an upward discontinuity after first-phase decline. A high $R^2$ is compatible with that defect and is insufficient to diagnose or exclude it. The reported AICc difference reaches 132.6 across these fits.

$R^2$ summarises residual variation relative to the spread of the observations. It does not test continuity or establish a mechanistic interpretation. Information criteria compare penalised likelihoods, residual diagnostics assess patterns left unexplained, and profile likelihood evaluates parameter uncertainty. These are different questions. Their combined use is more informative than a high $R^2$ alone, without requiring every diagnostic to distinguish the models in every design.

## 4. Discussion

### 4.1 Growth regime and the interpretation of the slow phase

The main result is the change in the variance decomposition between the two illustrative regimes. Resuscitation dominates the slow-growth example and contributes very little to time to LOD in the fast-growth example. A biological role and a dominant sensitivity index are different claims. A process can be present in both regimes while accounting for substantially different amounts of outcome variation.

The two-state interpretation belongs to an established modelling tradition. Patra and Klumpp (2013) analysed population dynamics with reversible switching and different growth and survival properties. The present contribution is the comparison of endpoint sensitivity under the specified concentration–response model and input distributions, together with a separate assessment of practical identifiability. It is not the introduction of phenotypic switching as an explanation of biphasic killing. Earlier work by Dickinson and Mitchison (1981) also connected intermittent metabolic activity with the interpretation of sterilising drug activity.

Clinical slow-phase estimates address a related question at a different level. Magombedze et al. (2021) analysed serial sputum data from 1,924 REMoxTB participants and used estimated bacterial decline rates to predict treatment outcomes. Those empirical associations do not establish which microscopic process a decline rate represents. Conversely, the sensitivity ranking in the present synthetic model does not overturn those associations. A fitted aggregate rate can describe a population trajectory without separately resolving all the processes that contribute to it. Establishing such a decomposition would require its own identifiability evidence; Section 3.4 does not provide it for the resuscitation rate.

Biphasic shape alone also does not establish a switching mechanism. Martinecz et al. (2023) found that the concentration dependence of the slow phase in their rifampicin analysis supported the heteroresistance models they examined over their persistence models. That finding concerns those model formulations and data. It should not be restated as a universal incompatibility between persistence and concentration-dependent killing. The present model itself contains concentration-dependent responses in both compartments.

Abel Zur Wiesch et al. (2015) provided a further alternative by linking drug–target reaction kinetics to complex killing patterns without invoking phenotypic switching. The existence of that alternative does not prove that a switching parameter is unreal or that it equals a binding parameter. It establishes a problem of mechanistic discrimination: similar population-level patterns can have different model explanations. The present analysis compares consequences of an assumed state structure; it does not select that structure over all competing mechanisms.

### 4.2 Phenotypic signatures, sensitivity and identifiability

The concentration and duration endpoints retain information that a single decay rate discards. In the prescribed comparisons, the resistance signature is primarily a concentration shift, the tolerance signature is an extension of killing duration, and the persistence signature is strongest at the deep endpoint. Their overlap is part of the result. Calling them distinct signatures preserves the separation without claiming exact independence or unique biological classification.

That descriptive separation does not identify every underlying parameter. Several parameter combinations may yield similar endpoint values or trajectories. Likewise, a large Sobol index establishes importance under an input distribution, not recoverability from observations. The contrast between these two properties is central to interpreting the slow-growth example: resuscitation dominates its endpoint variance, but the reported fitting analysis profiles parameters of closed-form models, not the full state-structured system.

The transition-time result makes the distinction concrete. A close fit coexists with an open profile interval in all four tested designs. The fitted point is therefore insufficient to support a precise transition-time claim in those designs. Its failure to be determined is not a verdict against derived quantities or phenomenological parameters. It is a statement about the information supplied by these observations to this model.

### 4.3 Exposure conventions and interaction effects

Exposure normalisation is part of the question being asked. A fixed absolute concentration compares responses to the same external concentration. A fixed multiple of each parameter set's MIC compares responses after adjusting for the model's susceptibility threshold. Neither convention is universally correct. They condition the analysis differently, including the route through which concentration–response parameters affect the outcome.

This distinction also limits interpretation of the word “regime.” The two examples are parameter sets that differ in more than a species label or a single replication rate. Their contrasting sensitivity rankings do not isolate replication rate as the sole cause of the contrast. In this paper, growth regime denotes the full illustrative parameterisation and its associated population dynamics.

The large fast-growth interaction share makes a further point. First-order indices alone understate the involvement of parameters whose effects depend strongly on other inputs. Total-order indices capture that involvement, but overlapping contributions cannot be read as separate percentages of the total variance. The reported 69.5% is an aggregate interaction share. It neither identifies one dominant pair nor supplies the direction of a parameter effect. These distinctions retain the force of the result without converting a variance analysis into an intervention analysis.

### 4.4 Model adequacy and scope

The comparator's discontinuity is a specific mathematical defect. Its coexistence with high $R^2$ demonstrates why goodness of fit is insufficient as a model adequacy criterion. AICc and BIC add a complexity penalty, but selecting a better-fitting candidate within a set does not establish biological truth. Profile likelihood adds a different test: whether the fitted quantities are constrained. Continuity, likelihood fit and parameter uncertainty deserve separate assessment because one does not stand in for the others.

The study uses synthetic data and illustrative parameters at constant exposure. Its endpoint is time to LOD, which depends on the detection threshold and is distinct from extinction, cure or relapse. The model contains neither stochastic extinction nor host processes, and no result here estimates clinical treatment duration. Time-varying exposure would change the analysis; its effect on the sensitivity ranking has not been established.

The Sobol results are conditional on the specified ranges, distributions and exposure convention. Bootstrap intervals describe sampling uncertainty in the indices under that setup; they do not quantify uncertainty about the biological appropriateness of the setup. Two compartments provide a compact representation of heterogeneity, but the analysis does not test whether discrete states, a continuum of states or an alternative pharmacodynamic mechanism best describes any particular organism.

## 5. Conclusion

The state-structured model preserves distinct concentration and killing-time signatures and generates biphasic trajectories without a fitted breakpoint. Under the specified input distributions, the two illustrative growth regimes have sharply different sensitivity rankings: resuscitation dominates the slow-growth example, whereas its contribution to fast-growth time to LOD is small but nonzero and interactions collectively dominate the variance.

The fitting results establish a separate conclusion. A close fit does not ensure that a transition time is practically identifiable, and high $R^2$ does not establish model adequacy. Model structure determines which distinctions can be expressed; the endpoint and input distribution determine the sensitivity ranking; the observations determine which fitted quantities can be estimated. These results define the contribution of the model without turning synthetic parameter sets into findings about particular pathogens.

## Statements and Declarations

**Funding:** [Author to provide the funding source and grant details, or confirm that no funding supported this work.]

**Competing interests:** [Author to declare relevant financial and non-financial interests, including any relevant relationship with Farname Inc. No absence-of-interest statement has been assumed.]

**Author contributions:** [Author to confirm contributions to conceptualisation, methodology, software, analysis, and manuscript preparation.]

**Data and code availability:** The study uses synthetic data and computational model outputs. [Insert the persistent location and version of the code, synthetic data and outputs used for the final manuscript; public deposition has not been confirmed.]

**Ethics approval and consent to participate:** Not applicable to the synthetic modelling study described here; no human participants or animal experiments are reported.

**Consent for publication:** Not applicable; the study reports no individual participant data.

## Figure captions

Figure files are in `submission/bmb/figures/` as `Fig1.pdf` to `Fig5.pdf`, generated by `python -m src.bmb_package`, which also checks each file for superseded wording and for embedded raster content before copying it. Panel letters are as drawn on the figures.

**Fig. 1** State-structured population trajectories for the illustrative slow- and fast-growth parameter sets at four times their own MIC. Biphasic decline emerges from the compartment dynamics. The reported transition is a curvature-based observable, and time to LOD denotes crossing the detection threshold rather than population extinction

**Fig. 2** Distinct phenotypic signatures in the prescribed synthetic comparisons. Concentration and shallow and deep killing endpoints distinguish the baseline, resistance, tolerance and persistence examples. Duration endpoints in Table 2 are evaluated at eight times each variant's own MIC; the persistence example also changes the shallow endpoint slightly

**Fig. 3** First- and total-order Sobol indices for time to LOD in the two illustrative parameter sets under MIC-normalised exposure. The reported design uses 4,096 base samples, with bootstrap intervals. The interaction fraction is the aggregate share estimated from one minus the sum of first-order indices and is not a pair-specific contribution

**Fig. 4** Practical identifiability in the synthetic fitting comparisons. Profile likelihood assesses the fitted transition time of the closed-form comparator and the slow rate of the biexponential across four sampling designs. Open intervals indicate that the searched range does not bound the corresponding likelihood interval; this is not a structural identifiability analysis

**Fig. 5** Model comparison across the four synthetic sampling designs. High $R^2$ values coexist with the closed-form comparator's discontinuity. AICc assesses penalised likelihood fit and provides information beyond $R^2$; neither statistic establishes a unique biological mechanism

## References

Abel Zur Wiesch P, Abel S, Gkotzis S, Ocampo P, Engelstädter J, Hinkley T et al (2015) Classic reaction kinetics can explain complex patterns of antibiotic action. Sci Transl Med 7:287ra73. https://doi.org/10.1126/scitranslmed.aaa8760

Balaban NQ, Helaine S, Lewis K, Ackermann M, Aldridge B, Andersson DI et al (2019) Definitions and guidelines for research on antibiotic persistence. Nat Rev Microbiol 17:441-448. https://doi.org/10.1038/s41579-019-0196-3

Beal SL (2001) Ways to fit a PK model with some data below the quantification limit. J Pharmacokinet Pharmacodyn 28:481-504. https://doi.org/10.1023/a:1012299115260

Brauner A, Fridman O, Gefen O, Balaban NQ (2016) Distinguishing between resistance, tolerance and persistence to antibiotic treatment. Nat Rev Microbiol 14:320-330. https://doi.org/10.1038/nrmicro.2016.34

Dickinson JM, Mitchison DA (1981) Experimental models to explain the high sterilizing activity of rifampin in the chemotherapy of tuberculosis. Am Rev Respir Dis 123:367-371. https://doi.org/10.1164/arrd.1981.123.4.367

Levin BR, Rozen DE (2006) Non-inherited antibiotic resistance. Nat Rev Microbiol 4:556-562. https://doi.org/10.1038/nrmicro1445

Lewis K (2007) Persister cells, dormancy and infectious disease. Nat Rev Microbiol 5:48-56. https://doi.org/10.1038/nrmicro1557

Magombedze G, Pasipanodya JG, Gumbo T (2021) Bacterial load slopes represent biomarkers of tuberculosis therapy success, failure, and relapse. Commun Biol 4:664. https://doi.org/10.1038/s42003-021-02184-0

Martinecz A, Boeree MJ, Diacon AH, Dawson R, Hemez C, Aarnoutse RE, Abel Zur Wiesch P (2023) High rifampicin peak plasma concentrations accelerate the slow phase of bacterial decline in tuberculosis patients: evidence for heteroresistance. PLoS Comput Biol 19:e1011000. https://doi.org/10.1371/journal.pcbi.1011000

Nielsen EI, Friberg LE (2013) Pharmacokinetic-pharmacodynamic modeling of antibacterial drugs. Pharmacol Rev 65:1053-1090. https://doi.org/10.1124/pr.111.005769

Patra P, Klumpp S (2013) Population dynamics of bacterial persistence. PLoS One 8:e62814. https://doi.org/10.1371/journal.pone.0062814

Regoes RR, Wiuff C, Zappala RM, Garner KN, Baquero F, Levin BR (2004) Pharmacodynamic functions: a multiparameter approach to the design of antibiotic treatment regimens. Antimicrob Agents Chemother 48:3670-3676. https://doi.org/10.1128/AAC.48.10.3670-3676.2004
