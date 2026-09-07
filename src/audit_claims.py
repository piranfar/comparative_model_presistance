"""
Check every headline number in the current paper against its table.

Run:  python -m src.audit_claims

Numbers drift. A figure gets regenerated, a filter changes, a section is
rewritten, and a value quoted in three places stops agreeing with itself. This
has already happened twice in this project, both times caught by accident. This
script checks on purpose.

Each entry names the claim, where it is asserted, and how to recompute it from
the results tables. A claim that cannot be recomputed is reported as such rather
than passed.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"


def load(name: str):
    p = T / name
    return pd.read_csv(p) if p.exists() else None


def receipt(name: str):
    """Read a receipt, or None if the stage has not been run."""
    p = ROOT / "results" / "receipts" / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def check(label: str, claimed, computed, tol=0.05, unit=""):
    """Compare a claimed value with a recomputed one, on relative tolerance."""
    if computed is None or (isinstance(computed, float) and not np.isfinite(computed)):
        return {"claim": label, "claimed": claimed, "computed": None,
                "status": "CANNOT RECOMPUTE"}
    ok = abs(computed - claimed) <= tol * max(abs(claimed), 1e-12)
    return {"claim": label, "claimed": f"{claimed:g}{unit}",
            "computed": f"{computed:.4g}{unit}",
            "status": "ok" if ok else "MISMATCH"}


def main() -> int:
    rows = []

    # --- exp24, the three properties a design review found we had missed --
    # Two of these constrain our own argument rather than support it, which is
    # why they are pinned: a number that limits a claim must not be free to
    # drift in the direction we would prefer.
    r = receipt("exp24_receipt.json")
    if r is not None:
        tr = r["trajectory_shape"]
        rows.append(check("treated series measured for shape (4: 64)",
                          64, float(tr["n_treated_series"]), 0.001))
        rows.append(check("final step not a decline (4: 48)",
                          48, float(tr["n_terminal_step_not_a_decline"]), 0.001))
        rows.append(check("rebound over 1 log10 from nadir (4: 44)",
                          44, float(tr["n_rebound_over_1_log"]), 0.001))
        rows.append(check("median rebound (4: 2.17 log10)",
                          2.17, float(tr["median_rebound_log10"]), 0.02))
        fc = r["flag_consistency"]
        rows.append(check("BQL flags contradicted (methods: 83)",
                          83, float(fc["n_contradicted"]), 0.001))
        rows.append(check("share of flags contradicted (methods: 16.7%)",
                          0.167, float(fc["fraction_of_all_flags_contradicted"]), 0.02))
        co = r["starting_density_vs_laboratory"]
        # The number that most limits Section 4's Cox result.
        rows.append(check("starting density variance that is laboratory (4: 87.0%)",
                          0.870, float(co["variance_explained_by_laboratory"]), 0.01))

    # --- exp25, how much of the classification survives its measurement ---
    # The "six, not eighteen" numbers. These SHRINK this paper's claim and are
    # pinned for that reason: an earlier draft said eighteen labels were in
    # doubt, and the direction of the bound says six are.
    r = receipt("exp25_receipt.json")
    if r is not None:
        o = r["observability"]["15d"]
        rows.append(check("tolerance calls classified, 15d (2: 203)",
                          203, float(o["n_calls"]), 0.001))
        rows.append(check("calls resting on a measured fraction (2: 185)",
                          185, float(o["measured"]), 0.001))
        rows.append(check("censored calls with one compatible class (2: 12)",
                          12, float(o["single_compatible_class"]), 0.001))
        rows.append(check("censored calls with several compatible (2: 6)",
                          6, float(o["multiple_compatible_classes"]), 0.001))
        g = {x["group"]: x for x in r["by_susceptibility_group"]["15d"]}
        if "IR" in g and "IS" in g:
            rows.append(check("deep endpoint unreachable, resistant (2: 26.2%)",
                              26.2, float(g["IR"]["pct_deep_endpoint_unreachable"]), 0.02))
            rows.append(check("deep endpoint unreachable, susceptible (2: 7.6%)",
                              7.56, float(g["IS"]["pct_deep_endpoint_unreachable"]), 0.02))

    # --- exp22, the floor is inferred, so bound what rests on it ----------
    f = load("exp22_floor_sensitivity.csv")
    if f is not None:
        rows.append(check("short of 4 logs at the lowest plausible floor (methods: 28)",
                          28, float(f["n_short_of_4_logs"].min()), 0.001))
        rows.append(check("short of 4 logs at the inferred floor (methods: 33)",
                          33, float(f["n_short_of_4_logs"].max()), 0.001))

    # --- exp29, what L is and what a different L would cost ---------------
    r = receipt("exp29_receipt.json")
    if r is not None:
        rows.append(check("deposits stating an LOQ with a value (Methods: 0)",
                          0, float(r["n_datasets_stating_a_loq_with_a_value"]), 1.0))

    # --- exp30, the label refitted as an ordered outcome -------------------
    f = load("exp30_model_comparison.csv")
    if f is not None:
        fam = f[f.in_bh_family]
        rows.append(check("ordinal family members (4: 8)",
                          8, float(len(fam)), 0.001))
        rows.append(check("ordinal members surviving BH (4: 2)",
                          2, float(fam.survives_bh_ordinal.sum()), 0.001))
        rows.append(check("linear members surviving BH, same family (S3: 2)",
                          2, float(fam.survives_bh_linear.sum()), 0.001))
        rows.append(check("every member agrees in direction (S3: 8 of 8)",
                          8, float(fam.same_direction.sum()), 0.001))
        g = fam.set_index(["predictor", "culture_age_days", "endpoint_depth"])
        rows.append(check("resistance odds ratio, 15 d D5 (4: 2.32)",
                          2.317, float(g.loc[("resistance", 15, "D5"), "odds_ratio"]), 0.01))
        rows.append(check("growth odds ratio, 15 d D5 adjusted (4: 1.096)",
                          1.096, float(g.loc[("growth", 15, "D5"), "odds_ratio"]), 0.01))
        rows.append(check("baseline-only resistance loses BH (4: 0 = no)",
                          0, float(g.loc[("resistance", 15, "D5"),
                                         "survives_bh_ordinal_baseline_only"]), 1.0))
        rows.append(check("baseline-only growth keeps BH (4: 1 = yes)",
                          1, float(g.loc[("growth", 15, "D5"),
                                         "survives_bh_ordinal_baseline_only"]), 0.001))

    # --- exp31, what survives once the clustering is respected -------------
    r = receipt("exp31_receipt.json")
    if r is not None:
        c = r["clinical_clustering"]
        rows.append(check("baseline isolates, one per patient (4: 174)",
                          174, float(c["n_baseline_isolates"]), 0.001))
        rows.append(check("follow-up isolates from repeat patients (4: 43)",
                          43, float(c["n_follow_up_isolates"]), 0.001))
        rows.append(check("rows in clusters of two (4: 86)",
                          86, float(c["n_rows_potentially_non_independent"]), 0.001))

        p = r["paired_panels"]
        rows.append(check("isolates in both panels (4: 210)",
                          210, float(p["n_isolates_in_both_panels"]), 0.001))
        rows.append(check("lose the headroom shortfall between panels (4: 26)",
                          26, float(p["paired_short"]["n_only_first"]), 0.001))
        rows.append(check("gain one (4: 0)",
                          0, float(p["paired_short"]["n_only_second"]), 1.0))
        rows.append(check("paired McNemar on the shortfall (4: 3.0e-8)",
                          2.98e-8, float(p["paired_short"]["p_value"]), 0.02))
        rows.append(check("leave the floor between panels (4: 11)",
                          11, float(p["paired_at_floor"]["n_only_first"]), 0.001))

        e = r["era4tb_clearance_vs_density"]
        rows.append(check("laboratory-level exact p (5: 0.10)",
                          0.10, float(e["laboratory_level_exact_p_two_sided"]), 0.01))
        rows.append(check("smallest p this design can return (5: 0.10)",
                          0.10, float(e["smallest_two_sided_p_this_design_can_return"]), 0.01))
        rows.append(check("laboratory and arm both fixed, floor p (5: 0.167)",
                          0.1667, float(e["restricted_permutation"]["laboratory and arm"]
                                        ["smallest_attainable_p"]), 0.01))

        rows.append(check("between-laboratory share of starting density (5: 87.0%)",
                          0.870, float(r["era4tb_starting_density_variance"]
                                       ["observed_share"]), 0.01))
        rows.append(check("between-laboratory share of within-arm kill rate (5: 33.0%)",
                          0.330, float(r["era4tb_kill_rate_variance"]["observed_share"]), 0.01))

        h = r["era4tb_headroom_spread_100ul"]
        rows.append(check("laboratories behind delta h at 100 uL (6: 4)",
                          4, float(h["n_laboratories"]), 0.001))
        rows.append(check("delta h at 100 uL (6: 2.33)",
                          2.335, float(h["observed_range"]), 0.01))

        v = r["verdicts"]
        rows.append(check("conclusions that survive clustering (12: 20)",
                          20, float(v["SUPPORTED"]), 0.001))
        rows.append(check("conclusions weakened by clustering (12: 6)",
                          6, float(v["WEAKENED"]), 0.001))
        rows.append(check("conclusions withdrawn as meaningless (12: 1)",
                          1, float(v.get("WITHDRAWN", 0)), 0.001))
        rows.append(check("conclusions that do not survive (12: 5)",
                          5, float(v["NOT SUPPORTED"]), 0.001))

        b = r["clinical_baseline_only_15d"]
        rows.append(check("baseline-only short of 4-log headroom (4: 21)",
                          21, float(b["n_short_of_4_logs"]), 0.001))
        rows.append(check("baseline-only ceiling Fisher p (1: 0.137)",
                          0.137, float(b["ceiling_fisher_p"]), 0.02))

    # --- exp32, the crossing event and what follows it ---------------------
    r = receipt("exp32_receipt.json")
    if r is not None:
        k = r["recrossing_plating_key"]
        rows.append(check("series under the plating key (5: 360)",
                          360, float(k["n_series"]), 0.001))
        rows.append(check("flasks behind them (5: 90)", 90, float(k["n_flasks"]), 0.001))
        rows.append(check("series that ever cross (5: 140)",
                          140, float(k["n_ever_crossed_below"]), 0.001))
        rows.append(check("of those, series that return above (5: 84)",
                          84, float(k["n_returned_above"]), 0.001))
        rows.append(check("fraction of crossers returning (5: 60.0%)",
                          0.600, float(k["fraction_of_crossers_returning"]), 0.01))
        rows.append(check("median days below before returning (5: 4)",
                          4.0, float(k["days_below_before_return"]["median"]), 0.01))
        rows.append(check("returning within three days (5: 38)",
                          38, float(k["n_returning_within_three_days"]), 0.001))
        rows.append(check("volume key collides, plating key does not (5: 0)",
                          0, float(r["duplicate_key_resolution"]
                                   ["condition_keys_with_more_than_one_row"]), 1.0))

    f = load("exp32_transitions.csv")
    if f is not None:
        o = f[f.stratum_kind == "overall"].iloc[0]
        rows.append(check("visit-to-visit transitions (13: 2232)",
                          2232, float(o.n_visit_pairs), 0.001))
        rows.append(check("above to below (13: 144)", 144, float(o.above_to_below), 0.001))
        rows.append(check("below to above (13: 95)", 95, float(o.below_to_above), 0.001))
        rows.append(check("P(leaving the below state) (13: 0.222)",
                          0.222, float(o.p_below_to_above), 0.01))
        rows.append(check("series with one crossing that holds (13: 56)",
                          56, float(o.n_one_crossing_no_return), 0.001))

    f = load("exp32_interval_censored.csv")
    if f is not None:
        g = f.set_index("stratum")
        a = "all arms, 100 uL quadruplicate"
        rows.append(check("interval-censored t10, 100 uL (5: 1.82 d)",
                          1.819, float(g.loc[a, "weibull_interval_t10_days"]), 0.01))
        rows.append(check("naive t10, same stratum (5: 2.95 d)",
                          2.953, float(g.loc[a, "weibull_naive_t10_days"]), 0.01))
        rows.append(check("interval-censored t25, 100 uL (5: 9.64 d)",
                          9.637, float(g.loc[a, "weibull_interval_t25_days"]), 0.01))
        # the correction has a sign: the interval curve sits BELOW the naive one
        rows.append(check("Turnbull minus naive KM at day 3 (5: -0.081)",
                          -0.0814, float(g.loc[a, "turnbull_minus_km_day3"]), 0.02))
        t = "treated arms, all four platings"
        rows.append(check("treated arms, interval t25 (5: 3.67 d)",
                          3.670, float(g.loc[t, "weibull_interval_t25_days"]), 0.01))
        rows.append(check("treated arms, naive t25 (5: 5.77 d)",
                          5.765, float(g.loc[t, "weibull_naive_t25_days"]), 0.01))

    # --- exp33, what is known about the floor ------------------------------
    f = load("exp33_floor_posterior.csv")
    if f is not None:
        v = f.set_index("deposit")
        row = [i for i in v.index if i.startswith("Vijay")][0]
        rows.append(check("clinical floor posterior, lower support (1: 9.2)",
                          9.2, float(v.loc[row, "ci_low"]), 0.02))
        rows.append(check("clinical floor posterior, span log10 (1: 0.398)",
                          0.398, float(v.loc[row, "log10_span"]), 0.01))
        rows.append(check("deposits whose labels are refused (14: 2)",
                          2, float(f["refuse_labels"].sum()), 0.001))

    # --- exp34, the path through the inoculum ------------------------------
    f = load("exp34_mediation.csv")
    if f is not None:
        g = f.set_index("stratum")
        rows.append(check("mediated effect, all IS/IR (4: +0.166)",
                          0.1655, float(g.loc["all_IS_IR", "acme"]), 0.02))
        rows.append(check("its lower bootstrap bound excludes zero (4: +0.067)",
                          0.0670, float(g.loc["all_IS_IR", "acme_ci_low"]), 0.05))
        rows.append(check("direct effect covers zero, lower bound (4: -0.116)",
                          -0.1159, float(g.loc["all_IS_IR", "ade_ci_low"]), 0.05))
        rows.append(check("proportion mediated (4: 65%)",
                          0.65, float(g.loc["all_IS_IR", "prop_mediated"]), 0.02))
        rows.append(check("mediated effect, baseline only (4: +0.159)",
                          0.1586, float(g.loc["baseline_0M", "acme"]), 0.02))

    # --- exp35, what the deposit cannot rule out ---------------------------
    r = receipt("exp35_receipt.json")
    if r is not None:
        d = r["fraction_determinism"]
        rows.append(check("cuts reproduce every usable class (3a: 203)",
                          203, float(d["n_agree"]), 0.001))
        rows.append(check("disagreements between cuts and labels (3a: 0)",
                          0, float(d["n_disagree"]), 1.0))
        rows.append(check("residual correlation nullifying the path (Methods: -0.24)",
                          -0.237, float(r["mediation_sensitivity"]["rho_nullifies_point_acme"]), 0.05))

    # --- the two figures an adversarial review corrected --------------------
    f = load("exp23_inversions.csv")
    if f is not None:
        pred = f.distance_ratio > f.rate_ratio
        obs = f.inversion.astype(bool)
        rows.append(check("D/b criterion, all pairs (7: 83.8%)",
                          0.838, float((pred == obs).mean()), 0.01))
        rows.append(check("D/b criterion, inversions only (7: 60.0%)",
                          0.600, float((pred == obs)[obs].mean()), 0.01))
        rows.append(check("pairs that are not inversions (7: 63.4%)",
                          0.634, float((~obs).mean()), 0.01))

    f = load("exp32_recrossing.csv")
    if f is not None:
        tr = f[f.arm != "untreated"]
        flask = tr.groupby(["institute", "arm", "replicate"])["ever_crossed_below"].any()
        rows.append(check("treated flasks crossing on any plating (5: 48)",
                          48, float(flask.sum()), 0.001))
        rows.append(check("treated flasks in the deposit (5: 72)",
                          72, float(len(flask)), 0.001))

    # --- exp36, the visit-specific floor and the covariate screen ----------
    r = receipt("exp36_receipt.json")
    if r is not None:
        c = r["starting_density_censoring"]
        rows.append(check("day-0 readings on the minimum, 15 d (Methods: 1)",
                          1, float(c["n_on_the_day0_minimum"]["15d"]), 0.001))
        rows.append(check("N0 is left-censored (Methods: 0 = no)",
                          0, 1.0 if c["n0_is_left_censored"] else 0.0, 1.0))
        rows.append(check("covariates that may adjust the seeding gap (S6: 2)",
                          2, float(r["n_covariates_usable_for_adjustment"]), 0.001))
        d2 = r["day2_cut_recovery"]["15d_day2_cuts"]
        rows.append(check("day-2 cuts reproduce every class, 15 d (1: 203)",
                          203, float(d2["n_agree"]), 0.001))

    f = load("exp36_day2_boundaries.csv")
    if f is not None:
        g = f[f.culture_age_days == 15].set_index("endpoint")
        rows.append(check("day-2 assay floor (1: 230)",
                          230, float(g.loc["day 2", "assay_floor"]), 0.001))
        rows.append(check("N_id at day 2 equals N_id at day 5 (1: 23000)",
                          23000, float(g.loc["day 2", "N_id"]), 0.001))
        rows.append(check("short of 4 logs against the day-2 floor (1: 121)",
                          121, float(g.loc["day 2", "n_short_4log"]), 0.001))
        rows.append(check("short of 4 logs against the day-5 floor (1: 31)",
                          31, float(g.loc["day 5", "n_short_4log"]), 0.001))
        rows.append(check("day-2 readings at their floor (1: 18)",
                          18, float(g.loc["day 2", "n_at_floor"]), 0.001))
        rows.append(check("of those, one compatible class (1: 11)",
                          11, float(g.loc["day 2", "n_single_compatible_class"]), 0.001))

    # --- the Cox terms, pinned as hazard ratios so they cannot become p-values
    f = load("exp17_cox.csv")
    if f is not None:
        adj = f[f.model == "institute + starting density"].set_index("term")
        alone = f[f.model == "institute only"].set_index("term")
        for inst, before, after in (("D", 0.202, 0.339), ("E", 0.205, 0.364),
                                    ("F", 0.202, 0.619), ("C", 3.015, 5.267)):
            rows.append(check(f"institute {inst} hazard ratio, laboratory alone (5)",
                              before, float(alone.loc[f"institute_{inst}", "hazard_ratio"]), 0.02))
            rows.append(check(f"institute {inst} hazard ratio, adjusted (5)",
                              after, float(adj.loc[f"institute_{inst}", "hazard_ratio"]), 0.02))
        # the numbers Section 5 once printed as hazard ratios are these p-values
        rows.append(check("institute D adjusted p, NOT a hazard ratio (12: 0.138)",
                          0.138, float(adj.loc["institute_D", "p_value"]), 0.02))
        rows.append(check("institute F adjusted p, NOT a hazard ratio (12: 0.576)",
                          0.576, float(adj.loc["institute_F", "p_value"]), 0.02))

    # --- exp27, the out-of-sample test ------------------------------------
    f = load("exp27_out_of_sample.csv")
    if f is not None:
        g = f.set_index("endpoint_logs")
        rows.append(check("cultures in the held-out deposit (8: 20)",
                          20, float(g.loc[5.0, "n_cultures"]), 0.001))
        rows.append(check("5-log endpoint unreachable there (8: 5)",
                          5, float(g.loc[5.0, "n_unreachable"]), 0.001))
        rows.append(check("6-log endpoint unreachable there (8: 20)",
                          20, float(g.loc[6.0, "n_unreachable"]), 0.001))
        rows.append(check("4-log endpoint unreachable there (8: 0)",
                          0, float(g.loc[4.0, "n_unreachable"]), 1.0))

    # --- exp28, measurable depth against the standard ----------------------
    f = load("exp28_measurable_depth.csv")
    if f is not None:
        d = f.set_index("dataset")
        rows.append(check("delta h between laboratories at 100 uL (6: 2.33)",
                          2.33, float(d.loc["ERA4TB, between laboratories at 100 uL",
                                            "delta_h"]), 0.01))
        rows.append(check("delta h including plated volume (6: 4.40)",
                          4.40, float(d.loc["ERA4TB, every laboratory and plating volume",
                                            "delta_h"]), 0.01))
        # Kaur must stay NA: a number here would read as reproducibility.
        kaur_na = bool(f[f.dataset.str.startswith("Kaur")]["delta_h"].isna().all())
        rows.append(check("Kaur delta h reported as NA, not a number", 1,
                          1.0 if kaur_na else 0.0, 0.001))
        # Sections 6 and 8 quote the Dubey inoculum as a count, and the count
        # and log medians differ in the fourth figure. Pin the one the text
        # quotes, at the precision the text quotes it, or the two drift apart
        # again the way 1.22 x 10^6 did.
        rows.append(check("Dubey median day-zero count (6, 8: 1.215e6)",
                          1.215e6, float(d.loc["Dubey, hollow fibre",
                                               "median_N0"]), 0.0005,
                          unit=" per mL"))
        rows.append(check("Dubey inoculum above nominal (6: 12.15-fold)",
                          12.15, float(d.loc["Dubey, hollow fibre",
                                             "median_N0"]) / 1e5, 0.0005,
                          unit="x"))

    # --- exp26, the counter-tests -----------------------------------------
    # The strictest inversion rate is pinned because it is the number that
    # replaced our headline. 36.6 per cent was the most generous reading.
    r = receipt("exp26_receipt.json")
    if r is not None:
        t4 = r["counter_test_4_inversions_or_noise"]
        rows.append(check("inversion rate, no rate-gap requirement (5: 36.6%)",
                          0.366, float(t4["rate_at_no_threshold"]), 0.01))
        rows.append(check("inversion rate, gap > 0.10 log10/day (5: 21.3%)",
                          0.213, float(t4["rate_at_strictest"]), 0.02))
        rows.append(check("rivals supported across the four counter-tests (0)",
                          0, float(r["n_rivals_supported"]), 1.0))

    # --- exp21, the per-interval p-values --------------------------------
    # Added after a manuscript revision caught three of these wrong in the body
    # text. They had been carried over from an earlier draft and never
    # rechecked against the regenerated table, and no audit line covered them.
    f = load("exp21_interval_concentration_dependence.csv")
    if f is not None:
        g = f.set_index("interval")
        for iv, claimed in (("days 0-3", 0.013), ("days 3-7", 0.24),
                            ("days 7-14", 0.091)):
            if iv in g.index:
                rows.append(check(f"concentration slope p, {iv} (9)",
                                  claimed, float(g.loc[iv, "p_value"]), 0.05))

    # --- exp17, the Cox adjustment: p-values, not hazard ratios -----------
    # A revision of this manuscript relabelled these three p-values as hazard
    # ratios. Both quantities exist in the same table, so the audit now pins
    # both and names which is which.
    f = load("exp17_cox.csv")
    if f is not None:
        adj = f[f.model == "institute + starting density"].set_index("term")
        for term, claimed_p, claimed_hr in (("institute_D", 0.138, 0.339),
                                            ("institute_E", 0.172, 0.364),
                                            ("institute_F", 0.576, 0.619)):
            if term in adj.index:
                rows.append(check(f"{term} adjusted P-VALUE (5)",
                                  claimed_p, float(adj.loc[term, "p_value"]), 0.02))
                rows.append(check(f"{term} adjusted HAZARD RATIO (not the p)",
                                  claimed_hr, float(adj.loc[term, "hazard_ratio"]), 0.02))

    # --- exp17, growth at one times MIC ----------------------------------
    # The claim is net GROWTH in five of six laboratories, which is stronger
    # than "little or no killing" and is what the numbers say.
    f = load("exp17_kill_rates.csv")
    if f is not None:
        one = f[f.arm == "MXF 1x MIC"].dropna(subset=["kill_rate_tobit"])
        rows.append(check("laboratories with net growth at 1x MIC (5: 5)",
                          5, float((one.kill_rate_tobit < 0).sum()), 0.001))

    # --- exp22, the spine: dynamic range and the floored isolates --------
    # These are the numbers Sections 3.1 and 3.2 rest on. They are arithmetic
    # rather than statistical, so a drift here is a coding error, not noise.
    f = load("exp22_headroom.csv")
    if f is not None:
        g = f[f.culture_age_days == 15].set_index("group")
        rows.append(check("isolates short of 4-log headroom at 15 days (1: 33)",
                          33, float(g.loc["cannot reach 4 logs", "n_isolates"]), 0.001))
        rows.append(check("of those, recorded at the ceiling (1: 100%)",
                          1.0, float(g.loc["cannot reach 4 logs", "fraction_at_ceiling"]),
                          0.001))
        rows.append(check("with ample headroom, at the ceiling (1: 88.0%)",
                          0.880, float(g.loc["has 4 logs of headroom", "fraction_at_ceiling"]),
                          0.01))

    r = receipt("exp22_receipt.json")
    if r is not None:
        at = next(x for x in r["isolates_at_floor"] if x["culture_age_days"] == 15)
        rows.append(check("isolates ending at the MPN floor (2: 18)",
                          18, float(at["n_isolates_at_floor"]), 0.001))
        # The claim that makes the paper: the spread in recorded survival is not
        # merely similar to the spread in starting density, it IS it.
        rows.append(check("their survival spread equals their inoculum spread (2)",
                          float(at["start_density_fold_range"]),
                          float(at["apparent_survival_fold_range"]), 0.001, "x"))
        gap = r["starting_density_by_resistance"]["15d"]
        rows.append(check("resistant isolates start lower (4: 10.0-fold)",
                          10.0, float(gap["fold_lower_in_resistant"]), 0.05, "x"))

    f = load("exp22_label_associations.csv")
    if f is not None:
        rows.append(check("label tests in the family (4: 8)",
                          8, float(len(f)), 0.001))
        rows.append(check("surviving Benjamini-Hochberg (4: 2)",
                          2, float(f.survives_bh.sum()), 0.001))
        res = f[(f.predictor == "resistance") & (f.culture_age_days == 15)
                & (f.endpoint_depth == "D5")]
        if len(res) == 1:
            b0 = float(res.beta.iloc[0])
            b1 = float(res.beta_after_adjusting_for_start_density.iloc[0])
            rows.append(check("attenuation of the resistance coefficient (4: 66%)",
                              0.66, (b0 - b1) / b0, 0.03))

    # --- exp23, the inversion rate ---------------------------------------
    r = receipt("exp23_receipt.json")
    if r is not None:
        inv = r["inversions"]
        rows.append(check("inversion rate (7: 36.6%)",
                          0.366, float(inv["inversion_rate"]), 0.01))
        rows.append(check("comparable pairs (7: 191)",
                          191, float(inv["n_comparable_pairs"]), 0.001))
        # The share that argues AGAINST the strong reading. It is audited for
        # exactly that reason: a number that limits our own claim must not drift
        # quietly in the direction we would prefer.
        mxf = r["variance_decomposition"].get("MXF 10X MIC")
        if mxf:
            rows.append(check("distance share, MXF 10x (7: 39.4%)",
                              0.394, float(mxf["share_distance"]), 0.02))

    # --- exp16, the family correction ------------------------------------
    f = load("exp16_tb_independence.csv")
    if f is not None:
        rows.append(check("MIC-MDK tests available (docs/18: 24)",
                          24, float(len(f)), 0.001))
        rows.append(check("nominally significant (docs/18: 4)",
                          4, float((f.p_value < 0.05).sum()), 0.001))
        rows.append(check("surviving Benjamini-Hochberg (docs/18: 0)",
                          0, float(f.survives_bh.sum()), 1.0))

    # --- exp17, the two censoring estimators must agree -------------------
    f = load("exp17_kill_rates.csv")
    if f is not None:
        g = f.dropna(subset=["kill_rate_tobit", "kill_rate_mi"])
        rows.append(check("max |Tobit - imputation| (docs/18: 0.003 log10/day)",
                          0.003, float((g.kill_rate_tobit - g.kill_rate_mi).abs().max()),
                          0.35, " log10/d"))

    # --- exp18, the conclusion must hold on both unit readings ------------
    f = load("exp18_unit_sensitivity.csv")
    if f is not None:
        rows.append(check("smallest psi_min gap, either unit reading (docs/18: 273x)",
                          273, float(f.fold_gap.min()), 0.02, "x"))
        rows.append(check("largest psi_min gap, either unit reading (docs/18: 658x)",
                          658, float(f.fold_gap.max()), 0.02, "x"))

    # --- exp20, the endpoint that decides what is visible -----------------
    f = load("exp20_endpoint_separation.csv")
    if f is not None:
        s = f.set_index("day")["survivor_ratio_low_over_high"]
        for day, claimed in ((7.0, 48.2), (14.0, 5.2)):
            if day in s.index:
                rows.append(check(f"32-fold dose range separates at day {int(day)}",
                                  claimed, float(s.loc[day]), 0.05, "x"))

    out = pd.DataFrame(rows)
    pd.set_option("display.width", 210)
    pd.set_option("display.max_colwidth", 62)
    print(out.to_string(index=False))

    bad = out[out.status.isin(["MISMATCH", "CANNOT RECOMPUTE", "EXPLAIN OR PICK ONE"])]
    print(f"\n{len(out) - len(bad)} of {len(out)} checks agree with the tables")
    if len(bad):
        print(f"{len(bad)} need attention:")
        for _, x in bad.iterrows():
            print(f"   [{x.status}] {x.claim}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
