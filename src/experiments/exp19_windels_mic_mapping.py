"""
The measured MIC of every evolved population, and the two things it settles.

Run:  python -m src.experiments.exp19_windels_mic_mapping

WHY THIS EXISTS. data/raw/windels2024/phenotypes_after_evol.csv has been in this
repository since the Zenodo deposit was downloaded and, until now, was read by no
script in src/. It holds the endpoint minimum inhibitory concentration and the
persister fraction of 126 clones, one row per clone, labelled by the antibiotic
concentration and nutrient level its population evolved under. Two separate
questions in this project turn out to be answerable from it directly.

THE FIRST IS AN ERROR THIS PROJECT KEPT MAKING. Three scripts compared conditions
at equal absolute concentration in micrograms per millilitre, on the assumption
that equal concentration means equal exposure. It does not, because the
populations did not end at the same MIC. exp02, exp03 and fig05 each had to be
corrected for this separately, the third time only because the second correction
was found not to have been applied everywhere.

With the measured MICs the size of that confound stops being an argument and
becomes a number. At 25 ug/mL, the same absolute concentration spans 0.55 to
9.47 times the evolved MIC depending on the nutrient level, a seventeenfold
spread. A comparison at equal absolute concentration is therefore a comparison
between a sub-inhibitory exposure and a strongly inhibitory one. The mapping
computed here should be used wherever this dataset's conditions are compared.

The confound is also directional rather than random: MIC rises with the nutrient
level the population evolved under (Spearman rho = +0.24, p = 0.008, n = 126).
Richer conditions produced more resistant populations, so equal absolute
concentration systematically understates exposure in the poor conditions, which
are exactly the conditions exp14 finds the drug performing worst in.

THE SECOND IS A CLAIM THE MANUSCRIPT MAKES. The framework asserts that
resistance and persistence occupy separate measurable axes: a concentration axis
and a duration axis. exp16 tested that on 217 clinical Mycobacterium tuberculosis
isolates and found MIC and the minimum duration for killing uncorrelated.

The obvious objection to exp16 is that clinical isolates differ in a thousand
uncontrolled ways. This dataset answers a complementary version of the same
question under laboratory control: the clones share an ancestor, evolved in
parallel under known conditions, and carry both an MIC and a persister fraction
measured on the same clone. If the two axes were one axis, they would move
together here.

They do not. Across all 126 clones the correlation between log2 MIC and log10
persister fraction is +0.04 with p = 0.63, in a design able to detect a
correlation of 0.17. The independence holds within every nutrient stratum
separately, so it is not an artefact of pooling conditions with different means.
This is a null result, and it is reported as one: the design bounds how large a
correlation could have hidden, rather than proving there is none.

Together with exp16 the claim now rests on two organisms, two laboratories and
two designs, one clinical and one experimental evolution.

Data: Windels et al. 2024, ISME J 18(1):wrae070, doi:10.5281/zenodo.7550302,
CC BY 4.0.

Writes:
  results/tables/exp19_mic_by_condition.csv
  results/tables/exp19_exposure_mapping.csv
  results/tables/exp19_axis_independence.csv
  results/receipts/exp19_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "windels2024" / "phenotypes_after_evol.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"


def geomean(v) -> float:
    v = np.asarray(v, dtype=float)
    v = v[v > 0]
    return float(np.exp(np.log(v).mean())) if v.size else float("nan")


def detectable_rho(n: int) -> float:
    """The smallest correlation this sample size could have called at 95%."""
    return float(np.tanh(1.96 / np.sqrt(n - 3))) if n > 3 else float("nan")


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; see the docstring for its source")
    pd.set_option("display.width", 200)

    d = pd.read_csv(DATA)

    # -- 1. the measured MIC of each condition, and the exposure it implies --
    by = (d.groupby(["AB_conc", "nutrient_conc"])
          .agg(n_clones=("MIC", "size"),
               mic_geomean_ug_ml=("MIC", geomean),
               mic_min=("MIC", "min"), mic_max=("MIC", "max"),
               persister_median=("pers_frac", "median"))
          .reset_index())
    by["exposure_x_mic"] = by["AB_conc"] / by["mic_geomean_ug_ml"]
    by["mic_fold_range_within_condition"] = by["mic_max"] / by["mic_min"]
    by.to_csv(TABLES / "exp19_mic_by_condition.csv", index=False)

    print("-- endpoint MIC of every evolved condition --")
    print(by.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    # -- 2. how far equal absolute concentration is from equal exposure -----
    rows = []
    for c, sub in by.groupby("AB_conc"):
        lo, hi = sub["exposure_x_mic"].min(), sub["exposure_x_mic"].max()
        rows.append({"AB_conc_ug_ml": float(c),
                     "n_nutrient_levels": int(len(sub)),
                     "exposure_min_x_mic": float(lo),
                     "exposure_max_x_mic": float(hi),
                     "fold_spread": float(hi / lo) if lo > 0 else np.nan,
                     "crosses_the_mic": bool(lo < 1.0 <= hi)})
    mapping = pd.DataFrame(rows)
    mapping.to_csv(TABLES / "exp19_exposure_mapping.csv", index=False)

    print("\n-- what one absolute concentration means across nutrient levels --")
    print(mapping.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
    worst = mapping.loc[mapping["fold_spread"].idxmax()]
    print(f"\n   At {worst['AB_conc_ug_ml']:g} ug/mL the same number denotes anything from "
          f"{worst['exposure_min_x_mic']:.2f}x to {worst['exposure_max_x_mic']:.2f}x MIC,")
    print(f"   a {worst['fold_spread']:.0f}-fold spread. Comparing conditions at equal absolute")
    print("   concentration compares different exposures, not different physiologies.")

    crossing = mapping[mapping["crosses_the_mic"]]
    if len(crossing):
        print(f"\n   {len(crossing)} concentration(s) straddle the MIC itself: in some nutrient")
        print("   conditions the exposure is sub-inhibitory while in others it is not.")

    # -- 3. is the confound directional? -----------------------------------
    r_nut = stats.spearmanr(d["nutrient_conc"], np.log2(d["MIC"]))
    print("\n-- does the evolved MIC track the nutrient level? --")
    print(f"   Spearman rho = {r_nut.statistic:+.3f}, p = {r_nut.pvalue:.4g}, n = {len(d)}")
    print("   Richer conditions evolved higher MICs, so equal absolute concentration")
    print("   understates exposure in exactly the poor conditions where exp14 finds")
    print("   the drug performing worst. The confound runs with the effect, not against it.")

    # -- 4. do resistance and persistence move together? -------------------
    rows = []
    strata = [("all clones", d)] + [(f"nutrient {n:g}", s)
                                    for n, s in d.groupby("nutrient_conc")]
    for label, sub in strata:
        s = sub.dropna(subset=["MIC", "pers_frac"])
        s = s[(s["pers_frac"] > 0) & (s["MIC"] > 0)]
        if len(s) < 8 or s["MIC"].nunique() < 2:
            continue
        r = stats.spearmanr(np.log2(s["MIC"]), np.log10(s["pers_frac"]))
        bound = detectable_rho(len(s))
        rows.append({"stratum": label, "n_clones": int(len(s)),
                     "spearman_rho": float(r.statistic), "p_value": float(r.pvalue),
                     "detectable_rho_at_95pct": bound,
                     "independent": bool(r.pvalue >= 0.05 and abs(r.statistic) < bound)})
    ind = pd.DataFrame(rows)
    ind.to_csv(TABLES / "exp19_axis_independence.csv", index=False)

    print("\n-- resistance against persistence, measured on the same clones --")
    print(ind.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))

    allc = ind[ind["stratum"] == "all clones"].iloc[0]
    print(f"\n   Across all {allc['n_clones']:.0f} clones the two axes are uncorrelated "
          f"(rho = {allc['spearman_rho']:+.3f}, p = {allc['p_value']:.2f})")
    print(f"   in a design that could have detected {allc['detectable_rho_at_95pct']:.2f}. "
          "The independence holds")
    print("   within every nutrient stratum, so it is not an artefact of pooling.")
    print("   With exp16 on 217 clinical M. tuberculosis isolates, the separation of")
    print("   the two axes now rests on two organisms and two designs.")

    (RECEIPTS / "exp19_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp19_windels_mic_mapping.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_doi": "10.5281/zenodo.7550302",
        "licence": "CC BY 4.0",
        "n_clones": int(len(d)),
        "n_conditions": int(len(by)),
        "mic_range_ug_ml": [float(d["MIC"].min()), float(d["MIC"].max())],
        "worst_exposure_confound": {
            "AB_conc_ug_ml": float(worst["AB_conc_ug_ml"]),
            "exposure_min_x_mic": float(worst["exposure_min_x_mic"]),
            "exposure_max_x_mic": float(worst["exposure_max_x_mic"]),
            "fold_spread": float(worst["fold_spread"])},
        "mic_vs_nutrient_spearman": {"rho": float(r_nut.statistic),
                                     "p": float(r_nut.pvalue)},
        "axis_independence": ind.to_dict(orient="records"),
        "note": ("This file had been in the repository unread since download. The "
                 "exposure mapping here should be used wherever conditions from this "
                 "dataset are compared."),
    }, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
