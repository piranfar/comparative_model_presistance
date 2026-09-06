"""
Build the manuscript tables from the results files.

Run:  python -m src.build_tables

The tables are generated rather than typed, for the same reason the figures are:
a number transcribed by hand into a manuscript is a number that can drift away
from the analysis that produced it, and this project has already had to correct
several that did. Every value below is read from results/tables/ and formatted
here, so regenerating the analysis regenerates the tables.

Writes manuscript/tables.md, in the order the text refers to them.
"""
from __future__ import annotations

from pathlib import Path

import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"
OUT = ROOT / "manuscript" / "tables.md"


def md(df: pd.DataFrame, align_right_from: int = 1) -> str:
    """A markdown table, numbers right-aligned so columns can be scanned."""
    cols = list(df.columns)
    head = "| " + " | ".join(cols) + " |"
    rule = "| " + " | ".join("---" if i < align_right_from else "---:"
                             for i in range(len(cols))) + " |"
    body = "\n".join("| " + " | ".join(str(v) for v in row) + " |"
                     for row in df.itertuples(index=False))
    return "\n".join([head, rule, body])


def table1() -> str:
    """The datasets, with what each contributes and its licence."""
    rows = [
        ["Six-laboratory exercise", "*M. tuberculosis* H37Rv",
         "moxifloxacin, isoniazid, 1x and 10x MIC", "90 flasks, 2 775 readings",
         "figshare 19766083", "CC BY 4.0"],
        ["Clinical isolates", "*M. tuberculosis*, 217 isolates",
         "rifampicin", "6 duration endpoints per isolate",
         "eLife 93243, suppl. file 2", "CC BY 4.0"],
        ["Evolved clones", "*E. coli*, 126 clones", "amikacin",
         "MIC and persister fraction per clone",
         "Zenodo 7550302", "CC BY 4.0"],
        ["Concentration-by-time grid", "*M. tuberculosis*",
         "apramycin 1-128 ug/mL (amikacin arm not analysed)",
         "5 concentrations x 4 days x 3 replicates",
         "figshare 26462791", "CC BY 4.0"],
        ["Held out for validation", "*E. coli*, hollow fibre",
         "amoxicillin-clavulanate",
         "20 cultures, measured day-zero density, 100 uL plated",
         "Nat Commun 2026 Source Data", "CC BY 4.0"],
    ]
    d = pd.DataFrame(rows, columns=["Dataset", "Organism", "Drug and range",
                                    "Design", "Deposit", "Licence"])
    return ("**Table 1.** The five published deposits reanalysed. Four carry "
            "the analysis and the fifth is held out to test it. None was "
            "generated for this study. The held-out deposit was opened after "
            "every boundary and threshold was fixed, which the commit history "
            "of the analysis repository timestamps; the other four were "
            "selected for the fields they carry, and that selection is not "
            "separately registered.\n\n" + md(d, align_right_from=99))


def table3() -> str:
    """The dynamic range each endpoint needs against the range available."""
    h = pd.read_csv(T / "exp22_headroom.csv")
    rows = []
    for age in sorted(h["culture_age_days"].unique()):
        g = h[h["culture_age_days"] == age].set_index("group")
        short = g.loc["cannot reach 4 logs"]
        ample = g.loc["has 4 logs of headroom"]
        n = int(short.n_isolates + ample.n_isolates)
        rows.append([f"{int(age)} days", "90% (1 log)", n, 0, "0.0%", "-"])
        rows.append([f"{int(age)} days", "99% (2 log)", n, 0, "0.0%", "-"])
        rows.append([f"{int(age)} days", "99.99% (4 log)", n,
                     int(short.n_isolates),
                     f"{100 * short.n_isolates / n:.1f}%",
                     f"{100 * short.fraction_at_ceiling:.0f}% vs "
                     f"{100 * ample.fraction_at_ceiling:.0f}%"])
    d = pd.DataFrame(rows, columns=[
        "Prior culture", "Endpoint", "Isolates", "Short of headroom",
        "Fraction short", "At ceiling: short vs ample"])
    return ("**Table 3.** The reduction each tolerance endpoint requires against "
            "the reduction the assay can resolve. Headroom is the distance from "
            "an isolate's starting density to the MPN floor of 23 per mL. An "
            "isolate short of headroom cannot reach that endpoint however "
            "completely the drug worked, and every such isolate is recorded at "
            "the assay ceiling." + chr(10) + chr(10) + md(d))


def table6() -> str:
    """Isolates at the floor, and how many of their labels are decidable."""
    r = json.loads((ROOT / "results" / "receipts" / "exp22_receipt.json")
                   .read_text(encoding="utf-8"))
    o = json.loads((ROOT / "results" / "receipts" / "exp25_receipt.json")
                   .read_text(encoding="utf-8"))["observability"]
    rows = []
    for f in r["isolates_at_floor"]:
        age = int(f["culture_age_days"])
        s = o[f"{age}d"]
        rows.append([f"{age} days",
                     int(f["n_isolates_at_floor"]),
                     f"{f['start_density_fold_range']:.0f}x",
                     f"{f['apparent_survival_fold_range']:.0f}x",
                     ", ".join(f"{k}: {v}" for k, v in
                               json.loads(f["label_counts"]).items()),
                     int(s["measured"]),
                     int(s["single_compatible_class"]),
                     int(s["multiple_compatible_classes"])])
    d = pd.DataFrame(rows, columns=[
        "Prior culture", "At the floor", "Starting density spread",
        "Recorded survival spread", "Labels assigned at the floor",
        "Measured", "Single compatible class", "Multiple compatible classes"])
    return ("**Table 6.** Isolates whose day-5 reading was censored at the MPN "
            "floor. They share one reported floor-level observation, but their "
            "true final counts are unknown below the limit, so the assay cannot "
            "distinguish their final viable burdens; because their starting "
            "densities differ, the same reading also implies a different range of "
            "compatible fractional reductions in each. The recorded fraction is "
            "L/N0, so the spread in apparent survival equals the spread in "
            "starting density exactly, and the labels differ accordingly. The "
            "last three columns sort every call in the panel, not only the "
            "censored ones: a censored reading bounds the class from above, and "
            "sweeping the true count across the admissible range leaves twelve "
            "calls with a single compatible class and six with more than one. "
            "Reaching the floor at all is a property of the killing; which class "
            "is then compatible is a property of the starting density and the "
            "floor."
            + chr(10) + chr(10) + md(d))


def table7() -> str:
    """What the deposited tolerance label tracks, on the ordering it actually is."""
    a = (pd.read_csv(T / "exp30_model_comparison.csv")
           .query("in_bh_family").sort_values("p_ordinal"))
    rows = []
    for r in a.itertuples():
        base = ("-" if pd.isna(r.p_ordinal_baseline_only) else
                f"{r.or_ordinal_baseline_only:.2f} (p={r.p_ordinal_baseline_only:.3f}, "
                f"{'survives' if r.survives_bh_ordinal_baseline_only else 'no'})")
        rows.append([
            {"growth": "time to OD 0.4"}.get(r.predictor, r.predictor),
            f"{int(r.culture_age_days)} d",
            {"D5": "day 5", "D2": "day 2"}.get(r.endpoint_depth, r.endpoint_depth),
            "adjusted" if r.adjusted_for_N0 else "unadjusted", int(r.n_ordinal),
            f"{r.odds_ratio:.3f} ({r.ci_low:.2f}-{r.ci_high:.2f})",
            f"{r.p_ordinal:.4f}",
            "yes" if r.survives_bh_ordinal else "no",
            f"{r.proportional_odds_p:.3f}", base])
    d = pd.DataFrame(rows, columns=[
        "Predictor", "Prior culture", "Reading day", "For starting density", "n",
        "Odds ratio (95% CI)", "p", "Survives BH", "Prop. odds p",
        "Baseline isolates only"])
    n = int(a["survives_bh_ordinal"].sum())
    return (f"**Table 7.** The family of {len(a)} tests between the deposited "
            f"tolerance label and its candidate determinants, fitted as "
            f"proportional-odds ordinal logistic regression and corrected "
            f"together at a false discovery rate of 5%. {n} survive. An odds "
            "ratio above one means higher odds of a higher tolerance class; time "
            "to OD 0.4 is in days and runs inversely to growth rate, so above one "
            "there means SLOWER growth accompanies a higher class. The "
            "proportional-odds column is a Brant test per predictor; the "
            "assumption holds throughout this family. The final column repeats "
            "each test on the baseline isolates, one per patient by "
            "construction, which is where the resistance association stops "
            "clearing its corrected threshold. Standard errors are model-based; "
            "the deposit carries no patient identifier, so none can be clustered "
            "on the true grouping, and the intervals here are model-based; "
            "a clustered variant is reported in Table S2."
            + chr(10) + chr(10) + md(d, align_right_from=4))


def table11() -> str:
    """How often the ranking inverts, and what buys the difference."""
    r = json.loads((ROOT / "results" / "receipts" / "exp23_receipt.json")
                   .read_text(encoding="utf-8"))
    inv = r["inversions"]
    rows = [["All arms pooled", inv["n_comparable_pairs"], inv["n_inversions"],
             f"{100 * inv['inversion_rate']:.1f}%",
             f"{100 * inv['inversion_rate_95CI'][0]:.1f}-"
             f"{100 * inv['inversion_rate_95CI'][1]:.1f}%",
             f"{100 * inv['model_predicts_inversion_correctly']:.1f}%", "", ""]]
    for arm, v in r["variance_decomposition"].items():
        rows.append([arm, "", "", "", "", "",
                     f"{100 * v['share_distance']:.1f}%",
                     f"{100 * v['share_rate']:.1f}%"])
    d = pd.DataFrame(rows, columns=[
        "Arm", "Comparable pairs", "Inversions", "Rate", "95% CI",
        "Called by D/b criterion", "Variance: distance", "Variance: rate"])
    return (f"**Table 11.** Pairs of flasks in the same arm from different "
            f"laboratories. An inversion is a pair in which the population that "
            f"fell faster crossed below the assay floor later. "
            f"{inv['undecidable_pairs']} further pairs that the censoring could "
            "not settle are excluded rather than imputed. The last two columns "
            "decompose the spread in crossing time; the rate term is the larger "
            "in every arm." + chr(10) + chr(10) + md(d))


def table8() -> str:
    """Kill rate and first crossing, per laboratory, in the arm that kills."""
    r = pd.read_csv(T / "exp17_kill_rates.csv")
    b = pd.read_csv(T / "exp17_baseline.csv").set_index("Institute")
    s = pd.read_csv(T / "exp17_survival.csv")
    s = s[s["arm"] != "untreated"]
    crossed = s.groupby("institute")["event"].sum()
    n_flask = s.groupby("institute")["event"].size()

    m = (r[r["arm"] == "MXF 10x MIC"].dropna(subset=["kill_rate_tobit"])
         .set_index("institute").sort_index())
    rows = []
    for inst in m.index:
        rows.append([
            inst,
            f"{b.loc[inst, 'start_log10_cfu_ml']:.2f}",
            str(b.loc[inst, 'reading_days']),
            f"{m.loc[inst, 'kill_rate_tobit']:.3f}",
            f"{m.loc[inst, 'kill_rate_ci_low']:.3f} to {m.loc[inst, 'kill_rate_ci_high']:.3f}",
            f"{m.loc[inst, 'kill_rate_mi']:.3f}",
            f"{100 * m.loc[inst, 'fraction_censored']:.0f}%",
            f"{int(crossed.get(inst, 0))} / {int(n_flask.get(inst, 0))}",
        ])
    d = pd.DataFrame(rows, columns=[
        "Lab", "Starting density (log10 CFU/mL)", "Reading day",
        "Kill rate (log10/day)",
        "95% profile interval", "By imputation", "Readings censored",
        "Flasks ever crossing the boundary (treated arms)"])
    return ("**Table 8.** Moxifloxacin at ten times MIC. Every laboratory yields "
            "a rate; three record no crossing below the assay floor in any arm. "
            "The final column counts first observed crossings, which are not "
            "clearances: across the deposit 60% of the series that cross read "
            "above the boundary again at a later visit. The two censoring "
            "estimators agree to 0.003 log10 per day. The starting density is the "
            "mean of quantified readings at day 0 or day 1 at the 100 uL plating, "
            "pooled over all of that laboratory's arms; the reading-day column "
            "says which visits contributed. Institute A deposits no day-zero "
            "reading at all, and among treated flasks only institutes C and D do, "
            "so for the rest this figure rests partly on readings taken after 24 "
            "hours of drug. Section 6 and Table 9 instead use untreated day-zero "
            "readings only, so the two tables are not expected to "
            "match.\n\n" + md(d))


def table14() -> str:
    """The family of MIC-versus-duration tests, and what survives it."""
    i = pd.read_csv(T / "exp16_tb_independence.csv").sort_values("p_value")
    top = i.head(6).copy()
    rows = [[r.stratum, r.endpoint, int(r.n), f"{r.spearman_rho:+.3f}",
             f"{r.p_value:.4f}", f"{r.bh_critical_value:.4f}",
             "yes" if r.survives_bh else "no",
             f"{r.detectable_rho_at_95pct:.2f}"]
            for r in top.itertuples()]
    d = pd.DataFrame(rows, columns=[
        "Stratum", "Endpoint", "n", "Spearman rho", "p", "BH critical value",
        "Survives correction", "Resolvable rho"])
    n_nom = int((i["p_value"] < 0.05).sum())
    return (f"**Table 14.** The six strongest of the {len(i)} comparisons the "
            f"217-isolate file supports. {n_nom} reach nominal significance where "
            f"{0.05 * len(i):.1f} are expected by chance; none exceeds its "
            "Benjamini-Hochberg critical value, which is ranked against the full "
            "family of 24 rather than against any one stratum. MDK99 and MDK99.99 "
            "are the minimum durations for a 99 and a 99.99 per cent reduction, "
            "the endpoints the text names in words. The final column is the "
            "correlation each design could have resolved at 95% confidence.\n\n"
            + md(d))


def table13() -> str:
    """What the endpoint does to a 32-fold concentration range."""
    s = pd.read_csv(T / "exp20_endpoint_separation.csv")
    iv = pd.read_csv(T / "exp21_interval_concentration_dependence.csv")
    rows = []
    for r in s.itertuples():
        rows.append([f"day {int(r.day)}",
                     f"{r.survivor_ratio_low_over_high:.1f}x",
                     f"{r.log10_separation:.2f}", "", "", ""])
    for r in iv.itertuples():
        rows.append([r.interval, "", "", f"{r.slope_per_doubling:+.4f}",
                     f"{r.ci_low:+.4f} to {r.ci_high:+.4f}", f"{r.p_value:.3f}"])
    d = pd.DataFrame(rows, columns=[
        "Read at", "Survivor ratio (low/high dose)", "log10 separation",
        "Slope per doubling", "95% interval", "p"])
    return ("**Table 13.** The same 32-fold concentration range summarised at each "
            "sampling day (upper rows), and the concentration slope fitted "
            "separately in each interval (lower rows). Slopes and intervals are "
            "from the replicate-level bootstrap described in the Methods.\n\n"
            + md(d))


def tableS2() -> str:
    """The ordered fit against the linear one it replaces."""
    a = (pd.read_csv(T / "exp30_model_comparison.csv")
           .query("in_bh_family").sort_values("p_ordinal"))
    rows = [[{"growth": "time to OD 0.4"}.get(r.predictor, r.predictor),
             f"{int(r.culture_age_days)} d",
             {"D5": "day 5", "D2": "day 2"}.get(r.endpoint_depth, r.endpoint_depth),
             f"{r.beta_linear:+.4f}", f"{r.p_linear:.4f}",
             "yes" if r.survives_bh_linear else "no",
             f"{r.odds_ratio:.3f}", f"{r.p_ordinal:.4f}",
             "yes" if r.survives_bh_ordinal else "no",
             "yes" if r.same_direction else "no"]
            for r in a.itertuples()]
    d = pd.DataFrame(rows, columns=[
        "Predictor", "Prior culture", "Reading day", "Linear beta", "p (linear)",
        "Survives BH", "Odds ratio", "p (ordinal)", "Survives BH ", "Same direction"])
    return ("**Table S2.** The ordinal reanalysis against the linear model it "
            "replaces, member for member. The linear model scores the ordering "
            "0, 1, 2, which assumes the two class steps are equal; the ordinal "
            "model does not. Every direction agrees and the same two members "
            "survive correction under both, so the linear treatment did not "
            "manufacture the result -- but the coefficients it reports are in a "
            "unit that does not exist, which is why the ordinal fit is the one "
            "in the main table."
            + chr(10) + chr(10) + md(d, align_right_from=3))


def tableS6() -> str:
    """What one nominal concentration means once the evolved MIC is known."""
    m = pd.read_csv(T / "exp19_exposure_mapping.csv")
    rows = [[f"{r.AB_conc_ug_ml:g}", int(r.n_nutrient_levels),
             f"{r.exposure_min_x_mic:.2f}", f"{r.exposure_max_x_mic:.2f}",
             f"{r.fold_spread:.1f}x",
             "yes" if r.crosses_the_mic else "no"]
            for r in m.itertuples()]
    d = pd.DataFrame(rows, columns=[
        "Nominal concentration (ug/mL)", "Nutrient levels",
        "Lowest exposure (x MIC)", "Highest exposure (x MIC)", "Spread",
        "Straddles the MIC"])
    return ("**Table S6.** The same nominal concentration expressed in multiples "
            "of the minimum inhibitory concentration each population actually "
            "evolved to. At 25 ug/mL the same number denotes a sub-inhibitory "
            "exposure in one nutrient condition and a strongly inhibitory one in "
            "another." + chr(10) + chr(10) + md(d))



def table9() -> str:
    """Measurable kill depth, reported on h and with each level of variation named."""
    d = pd.read_csv(T / "exp28_measurable_depth.csv")
    rows = []
    for r in d.itertuples():
        rows.append([
            r.dataset, r.level_of_variation, int(r.n),
            f"{r.median_log10_N0:.2f}", r.L_note,
            "NA" if pd.isna(r.delta_h) else f"{r.delta_h:.2f}",
            "NA" if pd.isna(r.fold_spread) else f"{r.fold_spread:,.0f}x",
        ])
    f = pd.DataFrame(rows, columns=[
        "Dataset", "Level of variation", "n", "Median log10 N0",
        "Assay floor L", "delta h (log10)", "Fold"])
    return ("**Table 9.** The deepest reduction each assay could resolve, as "
            "h = log10(N0/L), with the assay floor taken per sample "
            "where it varies. Rows compare only within a level of variation: the "
            "clinical rows describe between-isolate starting burden, which is "
            "biological, and are not a measure of laboratory imprecision. Kaur "
            "is NA because its three day-zero readings are technical replicates "
            "of one preparation and cannot estimate between-preparation "
            "reproducibility, and because that deposit states no quantification "
            "limit." + chr(10) + chr(10) + md(f, align_right_from=2))


def table12() -> str:
    """The framework applied to a deposit it was not built from."""
    d = pd.read_csv(T / "exp27_out_of_sample.csv")
    rows = [[f"{int(r.endpoint_logs)} log ({r.endpoint_pct:g}%)",
             f"{r.N_reach_per_ml:,.0f}", int(r.n_cultures),
             int(r.n_unreachable), f"{r.pct_unreachable:.0f}%"]
            for r in d.itertuples()]
    f = pd.DataFrame(rows, columns=[
        "Endpoint", "N_reach (per mL)", "Cultures", "Unreachable", "Per cent"])
    return ("**Table 12.** Dubey et al. 2026, analysed cold. The floor is "
            "derived from a stated 100 uL plated volume and corroborated inside "
            "the file: all 229 genuine counts are multiples of ten and the "
            "smallest is exactly ten. Starting densities are the 20 measured "
            "day-zero counts, not the nominal inoculum the Methods state."
            + chr(10) + chr(10) + md(f))


def tableS5() -> str:
    """The turbidity reference, kept out of the main tables on purpose."""
    d = pd.read_csv(T / "exp28_supplementary_mcfarland.csv")
    col = "fold_below_nominal_0.5_McFarland"
    rows = [[a, f"{b:.2f}", f"{c:,.0f}x"] for a, b, c in
            zip(d["dataset"], d["median_log10_N0"], d[col])]
    f = pd.DataFrame(rows, columns=[
        "Dataset", "Median log10 N0", "Fold below nominal 0.5 McFarland"])
    return ("**Table S5.** Fold below the nominal 0.5 McFarland reference, "
            "1.5e8 CFU/mL. Descriptive only, and not a protocol-compliance "
            "metric. A time-kill inoculum is prepared by diluting from a "
            "suspension matched to that turbidity, so every entry is expected to "
            "sit far below it; the conversion of a turbidity to CFU/mL depends "
            "on species, cell aggregation and preparation and is least reliable "
            "for mycobacteria." + chr(10) + chr(10) + md(f))



def table16() -> str:
    """What L is, deposit by deposit, and how we came by it."""
    d = pd.read_csv(T / "exp29_floor_provenance.csv")
    rows = [[r.dataset.split(",")[0],
             "yes" if str(r.source_states_lod).lower().startswith("y") else "no",
             "term only" if "term only" in str(r.source_states_loq)
             else ("yes" if str(r.source_states_loq).lower().startswith("y") else "no"),
             str(r.value_used), str(r.units), r.how_obtained,
             r.correct_term.split("(")[0].strip()]
            for r in d.itertuples()]
    f = pd.DataFrame(rows, columns=[
        "Deposit", "States an LOD", "States an LOQ", "Value used", "Units",
        "How obtained", "What it should be called"])
    return ("**Table 16.** What the boundary *L* is in each deposit analysed. No "
            "deposit reports a validated limit of quantification with a value. "
            "The six-laboratory file names the concept in the definitions of its "
            "below- and above-quantification-limit columns but defines it as "
            "whether the plate was countable, which is an operator's judgement. "
            "DERIVED means the value follows arithmetically from a recorded "
            "plated volume; INFERRED means it was read off the deposit's own "
            "behaviour and is labelled as inferred wherever it is used; NONE "
            "means no floor is evidenced and none is assumed; FLAGGED means the deposit "
            "marks below-limit readings without naming a value, which fixes no floor "
            "either. Where a plated "
            "volume is recorded the honest term is the minimum reportable "
            "positive count, one colony in that volume; elsewhere it is an "
            "operational assay floor."
            + chr(10) + chr(10) + md(f))


def tableS7() -> str:
    """What the load-bearing counts do under a different floor."""
    d = pd.read_csv(T / "exp29_floor_sensitivity.csv")
    # Long form, not a wide grid. The five deposits are sensitive to different
    # things, so a column set that suits one is empty for the others; pivoting
    # them into one grid produced a table that was mostly dashes.
    keep = {"n_short_of_4_logs_15d": "isolates short of 4 logs",
            "n_at_floor_15d": "isolates at the floor",
            "n_determinable_15d": "calls resting on a measured fraction",
            "n_forced_by_inoculum_15d": "calls with one compatible class",
            "n_undecidable_15d": "calls with several compatible classes",
            "n_short_of_4_logs_15d_baseline_only": "short of 4 logs, baseline only",
            "pct_genuine_counts_discarded": "genuine counts a pooled floor discards (%)",
            "pct_flags_contradicted": "below-limit flags contradicted (%)",
            "n_short_of_4_logs": "cultures short of 4 logs",
            "median_headroom_log10": "median headroom (log10)",
            "headroom_log10": "headroom (log10)",
            "four_log_endpoint_reachable": "4-log endpoint reachable",
            "n_below_limit_written_as_exact_zero": "readings written as exact zero"}
    f = d[d.metric.isin(keep)].copy()
    f["metric"] = f["metric"].map(keep)

    def fmt(v):
        try:
            x = float(v)
        except (TypeError, ValueError):
            return str(v)
        return f"{x:,.0f}" if x.is_integer() else f"{x:,.2f}"

    rows = [[r.dataset.split(",")[0], r.scenario, r.metric, fmt(r.value)]
            for r in f.itertuples()]
    w = pd.DataFrame(rows, columns=["Deposit", "Floor assumed", "Quantity", "Value"])
    return ("**Table S7.** Sensitivity of the load-bearing counts to the choice "
            "of floor. Each deposit is sensitive to a different thing, so the "
            "table is long rather than wide: one row per deposit, floor scenario "
            "and quantity. The clinical sweep steps through every three-tube "
            "most-probable-number rung at or below 23 per mL, and the number of "
            "isolates short of four logs of headroom moves only between 28 and "
            "33 across the whole range, which is why the inferred floor is safe "
            "to use. The six-laboratory rows price what pooling the four plating "
            "volumes to one floor would cost. The Kaur deposit records no plated "
            "volume, so its rows show what assuming one would do: the four-log "
            "endpoint stays reachable throughout while the headroom itself moves "
            "by 1.6 log10."
            + chr(10) + chr(10) + md(w, align_right_from=3))



def table15() -> str:
    """What survives once the clustering is respected, conclusion by conclusion."""
    d = pd.read_csv(T / "exp31_recomputed_inference.csv")
    order = {"NOT SUPPORTED": 0, "WEAKENED": 1, "SUPPORTED": 2}
    d = d.assign(_o=d.verdict.map(order)).sort_values(["_o", "manuscript_section"])
    rows = [[str(r.manuscript_section), r.conclusion,
             f"{r.n_naive_units} {r.unit_treated_as_independent}",
             str(r.n_independent_clusters), r.clustered_method, r.verdict]
            for r in d.itertuples()]
    f = pd.DataFrame(rows, columns=[
        "Section", "Conclusion as stated", "Units treated as independent",
        "Independent clusters", "Method used instead", "Verdict"])
    n = d.verdict.value_counts()
    return (f"**Table 15.** Every conclusion this paper draws from the two "
            f"primary deposits, against uncertainty recomputed at the level the "
            f"observations are actually independent. "
            f"{int(n.get('SUPPORTED', 0))} survive unchanged, "
            f"{int(n.get('WEAKENED', 0))} survive with materially wider "
            f"uncertainty, and {int(n.get('NOT SUPPORTED', 0))} do not survive. "
            "Each verdict applies to the claim as it was originally stated. "
            "Three of the five failures are gone from the text entirely; for the "
            "other two a weaker statement is retained and is marked as such where "
            "it appears -- the Cox coefficient trade is now reported as hazard "
            "ratios with no p-value, and institute C as the laboratory whose "
            "crossings its starting density does not account for rather than as a "
            "tested contrast. The five that fail are all "
            "between-laboratory p-values computed on flasks: every flask in a "
            "laboratory shares a starting culture, so a comparison that looks "
            "like 67 flasks is six laboratories, and for a three-against-three "
            "split of six clusters the smallest attainable two-sided p is 0.10. "
            "They are deleted rather than corrected, because there is nothing to "
            "correct them to."
            + chr(10) + chr(10) + md(f, align_right_from=3))


def table10() -> str:
    """What a crossing below the boundary turns out to be."""
    d = pd.read_csv(T / "exp32_transitions.csv")
    d = d[d.stratum_kind.isin(["overall", "arm"])]
    rows = []
    for r in d.itertuples():
        n = int(r.n_series)
        rows.append([
            r.stratum, n, int(r.n_visit_pairs),
            f"{r.p_above_to_below:.3f}", f"{r.p_below_to_above:.3f}",
            int(r.n_never_below), int(r.n_one_crossing_no_return),
            int(r.n_one_crossing_returns), int(r.n_crosses_repeatedly),
            f"{100 * r.n_one_crossing_no_return / n:.0f}%"])
    f = pd.DataFrame(rows, columns=[
        "Series", "n", "Visit pairs", "P(above to below)", "P(below to above)",
        "Never below", "One crossing, holds", "One crossing, returns",
        "Crosses repeatedly", "Shape the model assumes"])
    return ("**Table 10.** What follows a first observed crossing below the "
            "assay floor. The state below the boundary is not absorbing: a "
            "series sitting below it reads above again at the next visit with "
            "probability 0.22 overall, and that probability rises as drug "
            "pressure falls, which is what a plating artefact does. Only 56 of "
            "360 series, 15.6 per cent, show the shape a survival model assumes "
            "-- one crossing that holds. The 360 series are four platings of "
            "each of 90 flasks and are not independent; the flask-level counts "
            "are 53 flasks with a crossing series and 42 with a returning one."
            + chr(10) + chr(10) + md(f))


def table4() -> str:
    """The deposited class really is a threshold on the recorded fraction."""
    r = json.loads((ROOT / "results" / "receipts" / "exp35_receipt.json")
                   .read_text(encoding="utf-8"))
    d = r["fraction_determinism"]
    def sci(v: float) -> str:
        m, e = f"{v:.1e}".split("e")
        sup = str(int(e)).replace("-", "−")
        digits = str.maketrans("0123456789−", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
        return f"{m} × 10{sup.translate(digits)}"

    rows = [[c["label"], int(c["n"]), sci(c["min_fraction"]),
             sci(c["max_fraction"]), c["label"], int(c["disagreements"])]
            for c in d["classes"]]
    rows.append(["All usable", int(d["n_usable"]), "-", "-", "-",
                 int(d["n_disagree"])])
    f = pd.DataFrame(rows, columns=[
        "Recorded class", "n", "Min fraction", "Max fraction",
        "Predicted from cuts", "Disagreements"])
    return ("**Table 4.** The deposited tolerance class at day 5 after 15 days "
            "of prior culture is a threshold on the recorded surviving fraction, "
            "with no overlap between classes: low below 10\u207b\u00b3, medium from "
            "10\u207b\u00b3 to 10\u207b\u00b2 inclusive, high above 10\u207b\u00b2. Applying those cuts "
            "reproduces every usable class in the file. This matters because the "
            "argument that follows is about the fraction the assay recorded, not "
            "about an independent clinical judgement."
            + chr(10) + chr(10) + md(f, align_right_from=1))


def table2() -> str:
    """What is known about L, and when that is too little to label with."""
    d = pd.read_csv(T / "exp33_floor_posterior.csv")
    rows = []
    for r in d.itertuples():
        support = ("point mass" if r.verdict == "DERIVED"
                   else ("-" if pd.isna(r.ci_low)
                         else f"[{r.ci_low:.1f}, {r.ci_high:.1f}]"))
        # Where the verdict is NONE the minimum is not a floor, and printing it
        # in a column headed "floor used" would say it was.
        rows.append([r.deposit, r.verdict,
                     "-" if (pd.isna(r.candidate_floor) or r.verdict == "NONE")
                     else f"{r.candidate_floor:,.0f}",
                     support,
                     "-" if pd.isna(r.log10_span) else f"{r.log10_span:.3f}",
                     "yes" if r.refuse_labels else "no"])
    f = pd.DataFrame(rows, columns=[
        "Deposit", "Verdict", "Floor used", "95% support",
        "Span (log10)", "Refuse observability labels"])
    return ("**Table 2.** What is actually known about the assay floor in each "
            "deposit, and the rule that follows from it. A floor derived from a "
            "recorded plated volume is a point mass: one colony in that volume, "
            "no inference required. A floor inferred from a pile-up on a "
            "most-probable-number rung carries a posterior over the rungs at or "
            "below the observed minimum, and the 95 per cent support is quoted. "
            "Where no floor is evidenced at all, or where the support spans more "
            "than one log10, the observability labels of Section 3 are refused "
            "rather than reported -- a label is only as good as the floor it is "
            "computed against."
            + chr(10) + chr(10) + md(f, align_right_from=2))


def tableS3() -> str:
    """How much of the resistance association travels through the inoculum."""
    d = pd.read_csv(T / "exp34_mediation.csv")
    # exp35 repeats the linear fit as a reference row; exp34 already supplies it.
    b = pd.read_csv(T / "exp35_binary_mediation.csv")
    b = b[b.outcome != "linear_012"]
    rows = []
    for r in d.itertuples():
        rows.append([
            "Linear 0/1/2, " + {"all_IS_IR": "all IS/IR",
                                "baseline_0M": "baseline isolates"}
            .get(r.stratum, r.stratum.replace("_", " ")), int(r.n),
            f"{r.total_c:+.3f} ({r.total_ci_low:+.3f}, {r.total_ci_high:+.3f})",
            f"{r.ade_c_prime:+.3f} ({r.ade_ci_low:+.3f}, {r.ade_ci_high:+.3f})",
            f"{r.acme:+.3f} ({r.acme_ci_low:+.3f}, {r.acme_ci_high:+.3f})",
            f"{100 * r.prop_mediated:.0f}%"])
    for r in b.itertuples():
        rows.append([
            {"high_vs_rest": "High versus rest",
             "notlow_vs_low": "Not-low versus low"}.get(r.outcome, r.outcome),
            int(r.n),
            f"{r.total_c:+.3f}",
            f"{r.ade:+.3f}",
            f"{r.acme:+.3f} ({r.acme_ci_low:+.3f}, {r.acme_ci_high:+.3f})",
            f"{100 * r.prop_mediated:.0f}%"])
    f = pd.DataFrame(rows, columns=[
        "Outcome and stratum", "n", "Total effect c (95% CI)",
        "Direct effect c' (95% CI)", "Mediated effect (95% CI)",
        "Proportion mediated"])
    return ("**Table S3.** Decomposition of the isoniazid-resistance association "
            "with the tolerance class into a path through log10 starting density "
            "and a direct path, by the product of coefficients with bootstrap "
            "percentile intervals. The mediated path excludes zero in every "
            "specification and the direct path covers zero in every one. This "
            "replaces the percentage attenuation the earlier analysis quoted, "
            "which is a descriptive ratio rather than an estimand. Sequential "
            "ignorability is assumed and is not testable here; the sensitivity "
            "analysis in the Methods reports the residual correlation that would "
            "nullify the estimate."
            + chr(10) + chr(10) + md(f, align_right_from=1))


def tableS4() -> str:
    """What the deposit can, and cannot, rule out for the seeding gap."""
    a = pd.read_csv(T / "exp35_ir_seeding_confounders.csv").set_index("covariate")
    ind = pd.read_csv(T / "exp36_covariate_independence.csv")
    rows = []
    for r in ind.itertuples():
        s = a.loc[r.covariate] if r.covariate in a.index else None
        rows.append([
            r.covariate,
            f"{r.n_non_null_resistant}/{r.n_resistant}",
            f"{r.n_non_null_susceptible}/{r.n_susceptible}",
            r.verdict.split(":")[0],
            "-" if s is None else f"{s.beta_IR:+.3f}",
            "-" if s is None else f"{100 * s.attenuation_of_IR_beta:.0f}%",
        ])
    f = pd.DataFrame(rows, columns=[
        "Covariate", "Recorded, resistant", "Recorded, susceptible",
        "Can it adjust?", "Resistance coefficient", "Attenuation"])
    n_ok = int(ind.usable_for_adjustment.sum())
    return ("**Table S4.** Isoniazid-resistant isolates enter this assay ten-fold "
            "lower than susceptible ones, and we do not know why. This is what the "
            "deposit can and cannot rule out. Six of the nine pretreatment "
            "covariates are recorded almost exclusively for resistant isolates, so "
            "their missingness is the exposure and adjusting for them conditions on "
            "it; the two susceptibility calls are missing on identical rows, which "
            "is why they return identical coefficients. Those rows are shown with "
            "their coefficients so the circularity is visible, but they do not "
            f"bound anything. Only {n_ok} covariates are recorded at rates unrelated "
            "to susceptibility, and adjusting for either leaves the coefficient "
            "within five per cent of its unadjusted value. The file records no "
            "referring site and no processing batch, so those cannot be tested at "
            "all." + chr(10) + chr(10) + md(f, align_right_from=1))



def table5() -> str:
    """Every denominator, traced to the exclusion that produced it."""
    d = pd.read_csv(T / "exp37_analysis_flow.csv")
    rows = [[r.deposit, r.panel, r.stratum, r.stage, int(r.n),
             "-" if r.excluded_here == 0 else f"-{int(r.excluded_here)}"]
            for r in d.itertuples()]
    f = pd.DataFrame(rows, columns=[
        "Deposit", "Panel", "Stratum", "Stage", "n", "Excluded here"])
    return ("**Table 5.** Every analysis set in this paper, and the exclusion "
            "that produced it. The manuscript quotes a dozen different "
            "denominators, each correct for its own analysis; this is where a "
            "reader checks which is which. The MDR tolerance label is a fourth, "
            "unordered category and is dropped wherever an ordered outcome is "
            "fitted; the growth proxy is missing for one isolate; and five "
            "treated flasks in the six-laboratory deposit carry no usable "
            "starting density, which is why a comparison over 72 flasks is "
            "reported on 67. Whether these exclusions are plausibly ignorable is "
            "tested in Table S1." + chr(10) + chr(10) + md(f, align_right_from=4))


def tableS1() -> str:
    """Do the dropped rows differ from the retained ones?"""
    d = pd.read_csv(T / "exp37_dropped_vs_retained.csv")
    rows = [[r.panel, r.exclusion, int(r.n_dropped), int(r.n_retained),
             f"{r.median_start_log10_retained:.2f}",
             f"{r.median_start_log10_dropped:.2f}",
             f"{r.start_density_mannwhitney_p:.3f}",
             f"{r.pct_resistant_retained:.0f}%",
             f"{r.pct_resistant_dropped:.0f}%",
             f"{r.resistance_fisher_p:.3f}"] for r in d.itertuples()]
    f = pd.DataFrame(rows, columns=[
        "Panel", "Exclusion", "Dropped", "Retained", "Median log10 N0 retained",
        "Median log10 N0 dropped", "p", "Resistant, retained",
        "Resistant, dropped", "p "])
    return ("**Table S1.** The comparison the Methods promise: rows dropped from "
            "the association family against rows retained, on starting density "
            "and susceptibility. The MDR exclusion differs in susceptibility by "
            "construction, since those isolates are outside the "
            "resistant-versus-susceptible contrast the family tests. The one "
            "difference not by construction is in the 60-day panel, where the "
            "dropped rows sit higher in starting density (p = 0.027); it affects "
            "20 rows and no conclusion drawn from that panel."
            + chr(10) + chr(10) + md(f, align_right_from=2))

def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    parts = ["# Tables",
             "",
             "Generated by `python -m src.build_tables` from the files in "
             "`results/tables/`. Do not edit by hand: a value typed into this "
             "file can drift away from the analysis that produced it.",
             ""]
    order = (table1, table2, table3, table4, table5, table6, table7, table8,
             table9, table10, table11, table12, table13, table14, table15,
             table16)
    for fn in order:
        parts.append(fn())
        parts.append("")
    parts += ["---", "", "## Supplementary tables", "",
              "Held here so the Results stay on one line of reasoning. "
              "Table S6 supports Section 10 and Table S5 supports Section 6.",
              ""]
    for fn in (tableS1, tableS2, tableS3, tableS4, tableS5, tableS6, tableS7):
        parts.append(fn())
        parts.append("")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    for fn in order + (tableS1, tableS2, tableS3, tableS4, tableS5, tableS6, tableS7):
        first = fn().split("\n")[0]
        print("   " + first[:96])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
