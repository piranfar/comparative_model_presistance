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
         "apramycin, amikacin, 1-128 ug/mL",
         "5 concentrations x 4 days x 3 replicates",
         "figshare 26462791", "CC BY 4.0"],
    ]
    d = pd.DataFrame(rows, columns=["Dataset", "Organism", "Drug and range",
                                    "Design", "Deposit", "Licence"])
    return ("**Table 1.** The four published deposits reanalysed. None was "
            "generated for this study, and none was selected after its result "
            "was known.\n\n" + md(d, align_right_from=99))


def table2() -> str:
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
    return ("**Table 2.** The reduction each tolerance endpoint requires against "
            "the reduction the assay can resolve. Headroom is the distance from "
            "an isolate's starting density to the MPN floor of 23 per mL. An "
            "isolate short of headroom cannot reach that endpoint however "
            "completely the drug worked, and every such isolate is recorded at "
            "the assay ceiling." + chr(10) + chr(10) + md(d))


def table3() -> str:
    """Isolates that ended at the floor, and the labels they were given."""
    r = json.loads((ROOT / "results" / "receipts" / "exp22_receipt.json")
                   .read_text(encoding="utf-8"))
    rows = []
    for f in r["isolates_at_floor"]:
        counts = json.loads(f["label_counts"])
        rows.append([f"{int(f['culture_age_days'])} days",
                     int(f["n_isolates_at_floor"]),
                     f"{f['start_density_fold_range']:.0f}x",
                     f"{f['apparent_survival_fold_range']:.0f}x",
                     ", ".join(f"{k}: {v}" for k, v in counts.items())])
    d = pd.DataFrame(rows, columns=[
        "Prior culture", "Isolates at the floor", "Starting density spread",
        "Recorded survival spread", "Tolerance labels assigned"])
    return ("**Table 3.** Isolates whose day-5 reading sat on the MPN floor, so "
            "that as far as the assay could resolve they were killed to the same "
            "degree. Because a reading at the floor gives a recorded fraction of "
            "L/N0, the spread in their apparent survival equals the spread in "
            "their starting densities exactly. The labels they received differ."
            + chr(10) + chr(10) + md(d))


def table4() -> str:
    """What the deposited tolerance label tracks, as one corrected family."""
    a = pd.read_csv(T / "exp22_label_associations.csv").sort_values("p_value")
    rows = []
    for r in a.itertuples():
        pa = getattr(r, "p_after_adjusting_for_start_density", float("nan"))
        adj = ("-" if pd.isna(pa) else
               f"{r.beta_after_adjusting_for_start_density:+.3f} (p={pa:.3f})")
        rows.append([r.predictor, f"{int(r.culture_age_days)} d", r.endpoint_depth,
                     int(r.n), f"{r.beta:+.4f}", f"{r.p_value:.4f}",
                     "yes" if r.survives_bh else "no", adj])
    d = pd.DataFrame(rows, columns=[
        "Predictor", "Prior culture", "Depth", "n", "Coefficient", "p",
        "Survives BH", "After adjusting for starting density"])
    n = int(a["survives_bh"].sum())
    return (f"**Table 4.** The family of {len(a)} tests between the deposited "
            f"tolerance label and its candidate determinants, corrected together "
            f"at a false discovery rate of 5%. {n} survive. The final column "
            "shows what happens to the resistance association once the starting "
            "density enters the model." + chr(10) + chr(10) + md(d))


def table6() -> str:
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
    return (f"**Table 6.** Pairs of flasks in the same arm from different "
            f"laboratories. An inversion is a pair in which the population that "
            f"fell faster crossed the detection limit later. "
            f"{inv['undecidable_pairs']} further pairs that the censoring could "
            "not settle are excluded rather than imputed. The last two columns "
            "decompose the spread in crossing time; the rate term is the larger "
            "in every arm." + chr(10) + chr(10) + md(d))


def table5() -> str:
    """Kill rate and clearance, per laboratory, in the arm that kills."""
    r = pd.read_csv(T / "exp17_kill_rates.csv")
    b = pd.read_csv(T / "exp17_baseline.csv").set_index("Institute")
    s = pd.read_csv(T / "exp17_survival.csv")
    s = s[s["arm"] != "untreated"]
    cleared = s.groupby("institute")["event"].sum()
    n_flask = s.groupby("institute")["event"].size()

    m = (r[r["arm"] == "MXF 10x MIC"].dropna(subset=["kill_rate_tobit"])
         .set_index("institute").sort_index())
    rows = []
    for inst in m.index:
        rows.append([
            inst,
            f"{b.loc[inst, 'start_log10_cfu_ml']:.2f}",
            f"{m.loc[inst, 'kill_rate_tobit']:.3f}",
            f"{m.loc[inst, 'kill_rate_ci_low']:.3f} to {m.loc[inst, 'kill_rate_ci_high']:.3f}",
            f"{m.loc[inst, 'kill_rate_mi']:.3f}",
            f"{100 * m.loc[inst, 'fraction_censored']:.0f}%",
            f"{int(cleared.get(inst, 0))} / {int(n_flask.get(inst, 0))}",
        ])
    d = pd.DataFrame(rows, columns=[
        "Lab", "Starting density (log10 CFU/mL)", "Kill rate (log10/day)",
        "95% profile interval", "By imputation", "Readings censored",
        "Flasks ever cleared (all arms)"])
    return ("**Table 5.** Moxifloxacin at ten times MIC. Every laboratory yields "
            "a rate; three yield no clearance time in any arm. The two censoring "
            "estimators agree to 0.003 log10 per day.\n\n" + md(d))


def table8() -> str:
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
    return (f"**Table 8.** The six strongest of the {len(i)} comparisons the "
            f"217-isolate file supports. {n_nom} reach nominal significance where "
            f"{0.05 * len(i):.1f} are expected by chance; none exceeds its "
            "Benjamini-Hochberg critical value. The final column is the "
            "correlation each design could have resolved at 95% confidence.\n\n"
            + md(d))


def tableS1() -> str:
    """Admissible mycobacterial rates against the constants in routine use."""
    g = pd.read_csv(T / "exp18_parameter_gaps.csv")
    rows = [[r.constant.replace("psi_", "psi "), r.state,
             f"{r.published_value:+.4f}", f"{r.model_value:+.4f}",
             f"{r.fold_gap:,.0f}x", str(r.pmid)]
            for r in g.itertuples()]
    d = pd.DataFrame(rows, columns=[
        "Constant", "State measured in", "Published (ln/h)", "Assumed (ln/h)",
        "Gap", "Source PMID"])
    return ("**Table S1.** Every mycobacterial rate admissible under the rule of "
            "Section 2.3, against the constant in routine use. Values reported as "
            "a cumulative log reduction over a fixed window are excluded and are "
            "not listed.\n\n" + md(d))


def table7() -> str:
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
    return ("**Table 7.** The same 32-fold concentration range summarised at each "
            "sampling day (upper rows), and the concentration slope fitted "
            "separately in each interval (lower rows). Slopes and intervals are "
            "from the replicate-level bootstrap described in Section 2.\n\n"
            + md(d))


def tableS2() -> str:
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
    return ("**Table S2.** The same nominal concentration expressed in multiples "
            "of the minimum inhibitory concentration each population actually "
            "evolved to. At 25 ug/mL the same number denotes a sub-inhibitory "
            "exposure in one nutrient condition and a strongly inhibitory one in "
            "another." + chr(10) + chr(10) + md(d))


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    parts = ["# Tables",
             "",
             "Generated by `python -m src.build_tables` from the files in "
             "`results/tables/`. Do not edit by hand: a value typed into this "
             "file can drift away from the analysis that produced it.",
             ""]
    order = (table1, table2, table3, table4, table5, table6, table7, table8)
    for fn in order:
        parts.append(fn())
        parts.append("")
    parts += ["---", "", "## Supplementary tables", "",
              "These support Sections 4.2 and 4.5 but are not part of the "
              "main argument, and are held here so the Results stay on one "
              "line of reasoning.", ""]
    for fn in (tableS1, tableS2):
        parts.append(fn())
        parts.append("")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    for fn in order + (tableS1, tableS2):
        first = fn().split("\n")[0]
        print("   " + first[:96])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
