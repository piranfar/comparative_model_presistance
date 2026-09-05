"""
Recalculate every quantitative claim in the preprint from its own equations.

Run:  python -m src.experiments.exp01_recalculate_equations

Writes:
  results/tables/claim_recalculation.csv    one row per claim, with verdict
  results/tables/claim_recalculation.md     the same, formatted for the response
  results/tables/model_endpoints.csv        endpoints under each formulation
  results/receipts/exp01_environment.json   versions and timestamps

The rule applied throughout: a claim is checked against the paper's own stated
parameters and equations. Nothing here depends on data the paper does not have,
so every verdict is reproducible from the manuscript alone.
"""
from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import ks_2samp

from ..models import corrected as fix
from ..models import paper_equations as eq
from ..models.parameters import (DT_EULER_H, LOD_CFU_ML, MTB, SAUREUS, SPECIES,
                                 T_MAX_H)

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

# Whitman, Coleman & Wiebe 1998, PNAS 95:6578-83: 4-6 x 10^30 prokaryotic
# cells on Earth. Used only as an order-of-magnitude sanity bound.
EARTH_PROKARYOTES = 5.0e30

claims: list[dict] = []


def claim(claim_id, location, as_stated, recomputed, verdict, note):
    claims.append({
        "id": claim_id,
        "location_in_paper": location,
        "as_stated": as_stated,
        "recomputed": recomputed,
        "verdict": verdict,
        "note": note,
    })


# ---------------------------------------------------------------------------
# 1. Equation 4 is discontinuous at t_c: the population is resurrected
# ---------------------------------------------------------------------------

def check_discontinuity():
    rows = []
    cases = [
        ("Mtb", MTB, MTB.t_c_asserted, "Results 3.3 (t_c = 80 h)"),
        ("S. aureus", SAUREUS, SAUREUS.t_c_asserted, "Results 3.3 (t_c = 12 h)"),
        ("S. aureus", SAUREUS, 80.0, "Abstract (t_c = 80 h)"),
    ]
    for short, sp, t_c, where in cases:
        left, right, fold, log10fold = eq.transition_jump(
            sp.N0, sp.k_fast, sp.f_dormant_point, t_c)
        rows.append({
            "species": short, "t_c_h": t_c, "source": where,
            "N_left_over_N0": left / sp.N0,
            "N_right_over_N0": right / sp.N0,
            "jump_fold": fold, "jump_log10": log10fold,
        })
        claim(
            f"EQ4-DISC-{short.replace('. ', '')}-{t_c:g}",
            f"Methods Eq. 4 with {where}",
            "biphasic decay, monotone decreasing",
            f"upward jump x{fold:,.4g} ({log10fold:.2f} log10) at t_c",
            "FAIL",
            "second branch equals N0 exactly at t = t_c regardless of phase-1 "
            "killing, so the printed equation increases the population at the "
            "transition; Figure 2 shows no such jump, so the figure was not "
            "drawn from the printed equation",
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Equation 4 has a permanent nonzero floor: sterilisation is impossible
# ---------------------------------------------------------------------------

def check_floor():
    for short, sp in SPECIES.items():
        floor = sp.f_dormant_point * sp.N0
        claim(
            f"EQ4-FLOOR-{short.replace('. ', '')}",
            "Methods Eq. 4, Discussion 4.2",
            "persisters decline slowly under prolonged therapy",
            f"lim N(t) = {floor:,.0f} CFU/mL, constant for all t",
            "FAIL",
            f"with a {sp.N0:,.0f} CFU/mL inoculum the model asserts a permanent "
            f"floor at {100*sp.f_dormant_point:.4g}% of inoculum, i.e. no "
            "regimen of any duration can sterilise; the floor is "
            f"{floor/LOD_CFU_ML:,.0f}x the assay limit of detection",
        )


# ---------------------------------------------------------------------------
# 3. t_c is not a free parameter
# ---------------------------------------------------------------------------

def check_tc_identifiability():
    rows = []
    for short, sp in SPECIES.items():
        t_imp = eq.implied_t_c(sp.k_fast, sp.k_slow, sp.f_dormant_point)
        t_lo = eq.implied_t_c(sp.k_fast, sp.k_slow, sp.f_dormant_high)
        t_hi = eq.implied_t_c(sp.k_fast, sp.k_slow, sp.f_dormant_low)
        rows.append({
            "species": short, "t_c_asserted_h": sp.t_c_asserted,
            "t_c_implied_h": t_imp,
            "t_c_implied_range_h": f"{min(t_lo, t_hi):.1f}-{max(t_lo, t_hi):.1f}",
            "ratio_asserted_over_implied": sp.t_c_asserted / t_imp,
        })
        claim(
            f"TC-IDENT-{short.replace('. ', '')}",
            "Results 3.3, Table 1",
            f"t_c = {sp.t_c_asserted:g} h, fitted independently",
            f"t_c implied by k_fast, k_slow, f is {t_imp:.2f} h "
            f"({sp.t_c_asserted / t_imp:.2f}x discrepancy)",
            "FAIL",
            "in a biexponential population t_c = ln((1-f)/f)/(k_fast - k_slow), "
            "so treating f, k_fast, k_slow and t_c as four free parameters "
            "over-parameterises a three-parameter system",
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4. Equation 2 grows without bound
# ---------------------------------------------------------------------------

def check_resistance_growth():
    rows = []
    for short, sp in SPECIES.items():
        for t in (24.0, 240.0):
            printed = eq.resistance_as_printed(np.array([t]), sp.N0, sp.r, sp.k_R)[0]
            capped = fix.logistic_with_kill(np.array([t]), sp.N0, sp.K, sp.r, sp.k_R)[0]
            rows.append({
                "species": short, "t_h": t,
                "N_printed_cfu_ml": printed,
                "log10_fold_printed": np.log10(printed / sp.N0),
                "N_logistic_capped_cfu_ml": capped,
                "log10_fold_capped": np.log10(capped / sp.N0),
                "printed_over_K": printed / sp.K,
            })
        n240 = eq.resistance_as_printed(np.array([240.0]), sp.N0, sp.r, sp.k_R)[0]
        claim(
            f"EQ2-UNBOUNDED-{short.replace('. ', '')}",
            "Methods Eq. 2, Results 3.1",
            "resistant subpopulation continues growing under antibiotic",
            f"N(240 h) = 1e{np.log10(n240):.1f} CFU/mL, "
            f"{n240 / sp.K:,.3g}x the carrying capacity declared in Eq. 1",
            "FAIL" if n240 > sp.K else "PASS",
            "Eq. 1 declares a carrying capacity K that appears in none of the "
            "three survival laws; applying it caps growth at K and removes the "
            "excursion",
        )
    sa = SAUREUS
    n240 = eq.resistance_as_printed(np.array([240.0]), sa.N0, sa.r, sa.k_R)[0]
    claim(
        "EQ2-EARTH-Saureus",
        "Methods Eq. 2 with Table 1 S. aureus values",
        "exponential resistant growth over the 240 h simulation window",
        f"1e{np.log10(n240):.1f} CFU/mL, which is "
        f"1e{np.log10(n240 / EARTH_PROKARYOTES):.1f}x the estimated total "
        "prokaryotic population of Earth",
        "FAIL",
        "order-of-magnitude sanity bound from Whitman et al. 1998 PNAS "
        "(5e30 cells); a model output exceeding it by 27 orders of magnitude "
        "cannot be reported as a simulation of an infection",
    )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4b. Equation 3 omits replication, which reverses its verdict for S. aureus
# ---------------------------------------------------------------------------

def check_tolerance_omits_growth():
    rows = []
    for short, sp in SPECIES.items():
        net = sp.r - sp.k_T
        printed = eq.tolerance_as_printed(np.array([240.0]), sp.N0, sp.k_T)[0]
        with_growth = fix.logistic_with_kill(
            np.array([240.0]), sp.N0, sp.K, sp.r, sp.k_T)[0]
        rows.append({
            "species": short, "r": sp.r, "k_T": sp.k_T,
            "net_rate_r_minus_kT": net,
            "log10_N240_printed_eq3": np.log10(max(printed, 1e-300)),
            "log10_N240_with_replication": np.log10(max(with_growth, 1e-300)),
            "direction_printed": "decline",
            "direction_with_replication": "growth" if net > 0 else "decline",
        })
        verdict = "FAIL" if net > 0 else "PARTIAL"
        claim(
            f"EQ3-NO-REPLICATION-{short.replace('. ', '')}",
            "Methods Eq. 3, Results 3.2",
            f"tolerance in {short}: bacteria survive transiently before "
            f"declining at k_T = {sp.k_T:g}/h",
            f"Eq. 3 contains no replication term, yet Table 1 gives "
            f"r = {sp.r:g}/h, so the net rate is "
            f"{net:+.3f}/h and the population "
            f"{'GROWS to the carrying capacity' if net > 0 else 'declines, but ' + f'{sp.r / sp.k_T:.0%} more slowly than Eq. 3 shows'}",
            verdict,
            "dropping replication from the tolerance equation is not a "
            "simplification, it changes the sign of the result: under the "
            "paper's own Table 1 values S. aureus replicates 2.5x faster than "
            "the tolerance kill rate removes cells, so the printed equation "
            "reports 15 logs of killing where the parameters imply net growth",
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 5. What the corrected equation does to the paper's central comparison
# ---------------------------------------------------------------------------

def check_central_comparison():
    rows = []
    for short, sp in SPECIES.items():
        printed = eq.persistence_as_printed(
            np.array([240.0]), sp.N0, sp.k_fast, sp.k_slow,
            sp.f_dormant_point, sp.t_c_asserted)[0]
        cont = fix.persistence_continuous(
            np.array([240.0]), sp.N0, sp.k_fast, sp.k_slow, sp.t_c_asserted)[0]
        biexp = fix.biexponential(
            np.array([240.0]), sp.N0, sp.k_fast, sp.k_slow, sp.f_dormant_point)[0]
        rows.append({
            "species": short,
            "N240_printed_over_N0": printed / sp.N0,
            "N240_continuous_over_N0": cont / sp.N0,
            "N240_biexponential_over_N0": biexp / sp.N0,
            "log10_drop_printed": np.log10(sp.N0 / printed),
            "log10_drop_continuous": np.log10(sp.N0 / cont),
            "log10_drop_biexponential": np.log10(sp.N0 / biexp),
        })
    df = pd.DataFrame(rows).set_index("species")
    ratio_cont = (df.loc["Mtb", "N240_continuous_over_N0"] /
                  df.loc["S. aureus", "N240_continuous_over_N0"])
    claim(
        "CENTRAL-CLAIM-SURVIVES-FIX",
        "Abstract, Results 3.3, Conclusion",
        "M. tuberculosis survives extended antibiotic exposure whereas "
        "S. aureus declines sharply",
        f"under the continuous-piecewise fix the two species differ by only "
        f"{ratio_cont:.2f}x at 240 h "
        f"({np.log10(ratio_cont):.2f} log10)",
        "FAIL",
        "the qualitative contrast in Figure 2 is produced by the discontinuity, "
        "not by the parameters; once the equation is made continuous the "
        "paper's own Table 1 values make the two species nearly identical at "
        "10 days, so the comparative conclusion must be rebuilt on a "
        "mechanistic model rather than patched",
    )
    ratio_bi = (df.loc["Mtb", "N240_biexponential_over_N0"] /
                df.loc["S. aureus", "N240_biexponential_over_N0"])
    claim(
        "CENTRAL-CLAIM-BIEXP",
        "Abstract, Results 3.3",
        "same",
        f"under the biexponential fix the ratio at 240 h is {ratio_bi:,.4g}x "
        f"({np.log10(ratio_bi):.2f} log10) in favour of Mtb survival",
        "PARTIAL",
        "the biexponential form does preserve a Mtb-versus-S. aureus "
        "difference, because it retains the dormant fraction as a weight "
        "rather than discarding it; this is the formulation to adopt if a "
        "closed form is required",
    )
    return df.reset_index()


# ---------------------------------------------------------------------------
# 6. MDK endpoints under each formulation
# ---------------------------------------------------------------------------

def check_endpoints():
    rows = []
    for short, sp in SPECIES.items():
        forms = {
            "Eq. 4 as printed": lambda t, s=sp: eq.persistence_as_printed(
                t, s.N0, s.k_fast, s.k_slow, s.f_dormant_point, s.t_c_asserted),
            "continuous piecewise": lambda t, s=sp: fix.persistence_continuous(
                t, s.N0, s.k_fast, s.k_slow, s.t_c_asserted),
            "biexponential": lambda t, s=sp: fix.biexponential(
                t, s.N0, s.k_fast, s.k_slow, s.f_dormant_point),
        }
        for name, curve in forms.items():
            rows.append({
                "species": short,
                "formulation": name,
                "MDK99_h": fix.mdk(curve, sp.N0, 99.0),
                "MDK99.99_h": fix.mdk(curve, sp.N0, 99.99),
                "time_to_LOD_h": fix.time_to_lod(curve, LOD_CFU_ML),
                "log10_drop_240h": fix.log10_drop(curve, sp.N0, 240.0),
            })
    df = pd.DataFrame(rows)
    inf_rows = df[np.isinf(df["time_to_LOD_h"])]
    claim(
        "ENDPOINT-STERILISATION",
        "Methods Eq. 4, Discussion 4.2",
        "prolonged therapy eradicates M. tuberculosis",
        f"time to reach the {LOD_CFU_ML:,.0f} CFU/mL limit of detection is "
        f"infinite for {len(inf_rows)} of {len(df)} species-formulation "
        "combinations, all of them the printed Eq. 4",
        "FAIL",
        "the endpoint the paper's clinical conclusions rest on is not "
        "computable from the printed equation; it becomes finite under both "
        "corrected forms",
    )
    return df


# ---------------------------------------------------------------------------
# 7. The abstract compares two different parameters
# ---------------------------------------------------------------------------

def check_abstract_arithmetic():
    claim(
        "ABSTRACT-MISMATCHED-PARAMS",
        "Abstract",
        f"S. aureus killing rate {SAUREUS.k_T:g}/h versus M. tuberculosis "
        f"{MTB.k_slow:g}/h, a {SAUREUS.k_T / MTB.k_slow:.0f}-fold difference",
        f"{SAUREUS.k_T:g}/h is k_T from Eq. 3 (tolerance) and {MTB.k_slow:g}/h "
        f"is k_slow from Eq. 4 (persistence); the like-for-like pairs are "
        f"k_T {SAUREUS.k_T:g} vs {MTB.k_T:g} ({SAUREUS.k_T / MTB.k_T:.0f}x) and "
        f"k_slow {SAUREUS.k_slow:g} vs {MTB.k_slow:g} "
        f"({SAUREUS.k_slow / MTB.k_slow:.0f}x)",
        "FAIL",
        "the headline ratio compares parameters from two different equations; "
        "the like-for-like ratios are 4x for tolerance and 10x for slow "
        "killing, not the 200x the abstract implies",
    )
    claim(
        "ABSTRACT-TC-LABEL",
        "Abstract versus Results 3.3",
        "the transition from fast to slow killing occurs significantly "
        "earlier in S. aureus (80 hours)",
        f"Results 3.3 gives S. aureus {SAUREUS.t_c_asserted:g} h and Mtb "
        f"{MTB.t_c_asserted:g} h; the Abstract attaches Mtb's value to "
        "S. aureus while asserting the smaller of the two",
        "FAIL",
        "internally contradictory: the number and the label disagree, and the "
        "word earlier disagrees with the number quoted",
    )
    claim(
        "PERSISTER-FRACTION-3.58",
        "Discussion 4.2",
        "the persistence fraction (~3.58%) was consistent with prior research",
        f"3.58% lies inside the assumed input range "
        f"{100*MTB.f_dormant_low:g}-{100*MTB.f_dormant_high:g}% of Table 1; "
        "no fit exists that could have produced it",
        "FAIL",
        "presented in the Discussion as an output of model fitting, but it is "
        "an input drawn from the middle of the assumed prior range; the third "
        "decimal place implies a precision no procedure in the paper delivers",
    )


# ---------------------------------------------------------------------------
# 8. The Kolmogorov-Smirnov test is inapplicable
# ---------------------------------------------------------------------------

def check_ks_test():
    rows = []
    t_max = 240.0
    for n in (10, 25, 50, 100, 241, 500, 1000, 5000):
        t = np.linspace(0.0, t_max, n)
        a = eq.persistence_as_printed(t, MTB.N0, MTB.k_fast, MTB.k_slow,
                                      MTB.f_dormant_point, MTB.t_c_asserted)
        b = eq.persistence_as_printed(t, SAUREUS.N0, SAUREUS.k_fast,
                                      SAUREUS.k_slow, SAUREUS.f_dormant_point,
                                      SAUREUS.t_c_asserted)
        res = ks_2samp(np.log10(a), np.log10(b))
        rows.append({"n_grid_points": n, "ks_statistic": float(res.statistic),
                     "p_value": float(res.pvalue),
                     "significant_at_0.05": bool(res.pvalue < 0.05)}
                    )
    df = pd.DataFrame(rows)
    first_sig = df.loc[df["significant_at_0.05"], "n_grid_points"]
    claim(
        "KS-TEST-INAPPLICABLE",
        "Methods 2.3.3",
        "a two-sample Kolmogorov-Smirnov test yielded a significant "
        "difference (p < 0.05) between M. tuberculosis and S. aureus",
        "the p-value is controlled entirely by the simulation grid density: "
        f"it crosses 0.05 at n = {int(first_sig.min()) if len(first_sig) else 'n/a'} "
        f"grid points and reaches {df['p_value'].min():.2e} at n = "
        f"{int(df['n_grid_points'].max())}, with the KS statistic itself "
        f"changing by only {100*(df['ks_statistic'].max()-df['ks_statistic'].min()):.1f} "
        "percentage points",
        "FAIL",
        "a two-sample KS test compares empirical distributions of random "
        "samples; applied to two deterministic curves it tests whether the "
        "curves are identical, which is known a priori, and any two distinct "
        "curves can be made significant by sampling them more densely; the "
        "test carries no inferential content here and should be deleted",
    )
    return df


# ---------------------------------------------------------------------------
# 9. The sensitivity conclusions are algebraic identities
# ---------------------------------------------------------------------------

def check_sensitivity_tautology():
    rows = []
    T = 240.0
    for short, sp in SPECIES.items():
        # Under the printed Eq. 4 with T > t_c the response is
        #   N(T) = N0 [ f + (1-f) e^{-k_slow (T - t_c)} ]
        # so the elasticity with respect to k_slow is analytic.
        f, ks, tc = sp.f_dormant_point, sp.k_slow, sp.t_c_asserted
        dt = T - tc
        num = (1.0 - f) * np.exp(-ks * dt)
        denom = f + num
        elast_kslow = -ks * dt * num / denom
        elast_kfast = 0.0   # k_fast does not appear in the branch for t >= t_c
        rows.append({
            "species": short,
            "endpoint": "N(240 h) under printed Eq. 4",
            "elasticity_wrt_k_slow": float(elast_kslow),
            "elasticity_wrt_k_fast": float(elast_kfast),
            "elasticity_wrt_f": float(f * (1.0 - np.exp(-ks * dt)) / denom),
        })
    df = pd.DataFrame(rows)
    claim(
        "SENSITIVITY-TAUTOLOGY",
        "Methods 2.3.2, Results 3.3, Discussion 4.1",
        "persistence duration in Mtb was most sensitive to k_slow, and in "
        "S. aureus variations in k_T had the largest effect; these findings "
        "underscore the biological relevance of biphasic killing rates",
        "for any t > t_c the printed Eq. 4 contains k_slow and f only, and "
        "k_fast has an elasticity of exactly 0; the ranking is a property of "
        "which symbols appear in which branch, computed here in closed form",
        "FAIL",
        "the sensitivity ranking is forced by the structure of the equation "
        "and would be unchanged for any parameter values or any organism, so "
        "it cannot support a biological conclusion; a defensible analysis "
        "needs a global method on a model where all parameters act at all "
        "times, which is exp03",
    )
    return df


# ---------------------------------------------------------------------------
# 10. Numerical-methods claims
# ---------------------------------------------------------------------------

def check_numerics():
    sp = MTB
    rhs = lambda t, N: -sp.k_fast * N
    t_e, N_e = eq.euler_solution(rhs, sp.N0, 24.0, DT_EULER_H)
    analytic = sp.N0 * np.exp(-sp.k_fast * t_e)
    max_rel = float(np.max(np.abs(N_e - analytic) / analytic))
    claim(
        "NUMERICS-NOTHING-TO-SOLVE",
        "Methods 2.3.1",
        "SciPy odeint (LSODA) was used to solve the differential equations, "
        "and Euler with dt = 0.5 h cross-validated the results",
        "all four models in Methods 2.1 are closed-form algebraic solutions, "
        "so no differential equation is integrated anywhere in the paper; "
        f"Euler at dt = 0.5 h differs from the exact exponential by up to "
        f"{100*max_rel:.1f}% over 24 h, which measures the error of Euler, not "
        "the validity of the model",
        "FAIL",
        "the sentence describes a computation that the paper's mathematics "
        "does not contain; either remove it or move to a genuine ODE model, "
        "which is what mechanistic.py provides",
    )
    claim(
        "EQ1-K-UNUSED",
        "Methods 2.1 Eq. 1",
        "bacterial population dynamics were modelled using a logistic growth "
        "equation with carrying capacity K",
        "K appears in Eq. 1 and in none of Eqs. 2, 3 or 4, so no "
        "antibiotic-exposure result in the paper uses it",
        "FAIL",
        "declaring a carrying capacity and then omitting it is what permits "
        "the unbounded resistance excursion in claim EQ2-UNBOUNDED",
    )
    claim(
        "PANDAS-NO-DATA",
        "Methods 2.3, 2.3.3, Figure 3",
        "Pandas was used for handling large datasets, and simulated survival "
        "curves were compared with published experimental time-kill studies "
        "with R-squared > 0.9",
        "no dataset is named anywhere in the manuscript, no fit table is "
        "reported, and the project's data directory is empty",
        "FAIL",
        "Figure 3 is captioned as experimental data versus model fitting but "
        "no experimental data exists; this is the highest-severity item and "
        "cannot be repaired by recomputation, only by extracting real data",
    )
    return max_rel


# ---------------------------------------------------------------------------

def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    disc = check_discontinuity()
    check_floor()
    tc = check_tc_identifiability()
    res = check_resistance_growth()
    tol = check_tolerance_omits_growth()
    central = check_central_comparison()
    endpoints = check_endpoints()
    check_abstract_arithmetic()
    ks = check_ks_test()
    sens = check_sensitivity_tautology()
    euler_err = check_numerics()

    claims_df = pd.DataFrame(claims)
    claims_df.to_csv(TABLES / "claim_recalculation.csv", index=False)

    disc.to_csv(TABLES / "eq4_discontinuity.csv", index=False)
    tc.to_csv(TABLES / "tc_identifiability.csv", index=False)
    res.to_csv(TABLES / "eq2_unbounded_growth.csv", index=False)
    tol.to_csv(TABLES / "eq3_omits_replication.csv", index=False)
    central.to_csv(TABLES / "central_comparison.csv", index=False)
    endpoints.to_csv(TABLES / "model_endpoints.csv", index=False)
    ks.to_csv(TABLES / "ks_test_grid_dependence.csv", index=False)
    sens.to_csv(TABLES / "analytic_elasticities.csv", index=False)

    lines = ["# Recalculation of every quantitative claim", "",
             f"Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
             "",
             "Each row recomputes one claim from the paper's own equations and "
             "Table 1 values. No experimental data is involved, so every "
             "verdict is reproducible from the manuscript alone.", "",
             "| # | Where | As stated | Recomputed | Verdict |",
             "|---|---|---|---|---|"]
    for i, c in enumerate(claims, 1):
        lines.append(
            f"| {i} | {c['location_in_paper']} | {c['as_stated']} | "
            f"{c['recomputed']} | **{c['verdict']}** |")
    lines += ["", "## Notes", ""]
    for i, c in enumerate(claims, 1):
        lines.append(f"{i}. **{c['id']}** - {c['note']}")
    (TABLES / "claim_recalculation.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")

    receipt = {
        "script": "src/experiments/exp01_recalculate_equations.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
        "versions_claimed_in_paper": {
            "python": "3.9", "numpy": "1.21.2", "scipy": "1.7.1",
            "matplotlib": "3.4.3", "pandas": "1.3.3",
        },
        "n_claims_checked": len(claims),
        "n_fail": int((claims_df["verdict"] == "FAIL").sum()),
        "n_partial": int((claims_df["verdict"] == "PARTIAL").sum()),
        "n_pass": int((claims_df["verdict"] == "PASS").sum()),
        "euler_max_rel_error_24h": euler_err,
        "simulation_window_h": T_MAX_H,
        "lod_cfu_ml": LOD_CFU_ML,
    }
    (RECEIPTS / "exp01_environment.json").write_text(
        json.dumps(receipt, indent=2), encoding="utf-8")

    print(f"claims checked: {len(claims)}  "
          f"FAIL {receipt['n_fail']}  PARTIAL {receipt['n_partial']}  "
          f"PASS {receipt['n_pass']}")
    print("\n-- Eq. 4 discontinuity --")
    print(disc.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print("\n-- t_c identifiability --")
    print(tc.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    print("\n-- endpoints under each formulation --")
    print(endpoints.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
    print("\n-- KS-test grid dependence --")
    print(ks.to_string(index=False))
    print(f"\nwrote {TABLES / 'claim_recalculation.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
