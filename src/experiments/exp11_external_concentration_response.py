"""
The persister concentration-response against independent published data.

Run:  python -m src.experiments.exp11_external_concentration_response

exp09 found that the model of Boccarella et al. predicts a 1.55-fold drop in
survival when the antibiotic concentration doubles, against 75- to 200-fold in
the data their own persistence contrast is drawn from. That test rested on one
dataset and one pair of concentrations, and one of its two comparisons had two
populations in a cell.

This script asks the same question of datasets collected independently of that
model, spanning two genera and three antibiotics. They were not chosen to make a
point: they are what a search for published survival data returned.

The quantity compared is the steepness of the concentration-response: how far
log survival falls per doubling of concentration. It is the quantity that
cancels the persistence level and the persister death rate, which is why exp09
could use it without knowing either.

THE CEILING. With psi_max_PR = 0.05/h and the floor on psi_min_PR set by
MIN_VALUE = -0.5, the persister kill rate cannot exceed 0.55/h. Over a 5 h
exposure no two concentrations can differ by more than 2.75 in log survival, at
any parameter values and any Hill coefficient. Raising the Hill coefficient
lowers the achievable slope rather than raising it, because above the MIC the
response is already saturated.

DATA, all published and obtained from their public deposits:
  1. Recurrent-exposure CFU counts, E. coli MG1655, ampicillin at eight
     concentrations from 0 to 128 ug/mL, eight replicates, three 90-minute
     pulses. Kollerova S, Jouvet L, Smelkova J, Zunk-Parras S, Rodriguez-Rojas
     A, Steiner UK (2024) mSystems 9(7):e00256-24, doi:10.1128/msystems.00256-24,
     PMID 38920373, PMC11264686. Deposit: Dryad doi:10.5061/dryad.rr4xgxdbj
     (CC0 1.0), file `R long data Alex and Sara CFU counts.csv`.
     THE AUTHORS' OWN FINDING, which this script must not restate as its own:
     "for the cell culture experiments, we find the higher the antibiotic
     concentration the stronger the reduction in CFUs". They also report the
     opposite at the single-cell level in the same paper: "We also find no
     graded survival response to different levels of antibiotics at the
     single-cell level ... although at the cell-culture level we observed graded
     responses in CFUs." What is new here is the size of the slope per doubling
     and its comparison with the model ceiling, not the direction.
  2. Vogwill et al., J Evol Biol: survival of eight Pseudomonas species under
     ciprofloxacin and rifampicin at three relative doses, 48 observations per
     antibiotic and dose.

Two further datasets in the same folder vary exposure duration rather than
concentration and so do not enter this test: Stewart and Rozen time-kill curves
for ECOR strains, and the Stepanyan et al. 2015 killing curve for a wild-type
and a high-persistence strain. They bear on the other axis and are left to a
separate analysis.

DATASET 2's DOSE AXIS, RESOLVED. Its dose column is labelled "relative dose"
with levels 1, 2 and 3, and an earlier version of this script could not tell
whether those were concentrations or ordered categories. They are neither read
literally: the Methods state the assay was run "at the MIC, 2x and 4x MIC for
the strain with highest MIC for that antibiotic", so the three levels are 1x,
2x and 4x, not 1, 2 and 3. The same paragraph gives the exposure as four hours
("Four hours was found to representative to the level of persistence").

Both corrections matter and both cut against the earlier result. Regressing on
log2 of 1, 2, 3 instead of 1, 2, 4 compresses the top of the concentration range
and inflates the fitted slope per doubling by 2/log2(3) = 1.26-fold. Filling the
missing exposure with the model's own 5 h rather than the experiment's 4 h
raised the model's ceiling by a quarter, which was generous to the model but
still wrong. The ciprofloxacin slope reported here is therefore smaller than the
one this script produced before the paper's Methods were read.

Writes:
  results/tables/exp11_slopes.csv
  results/tables/exp11_ecoli_dose_response.csv
  results/receipts/exp11_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from ..models import boccarella as bc

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "external_survival"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

PULSES = [(60, 150, "pulse 1"), (330, 420, "pulse 2"), (1080, 1170, "pulse 3")]
EXPOSURE_MIN = 90.0          # each pulse in dataset 1, from the sampling times
AMP_MIC_REGION = 8.0         # concentrations at or above this are used for the slope

# Vogwill et al.: "relative dose" 1, 2 and 3 are 1x, 2x and 4x the MIC of the
# least susceptible strain, and each exposure lasted four hours. Both read from
# the paper's Methods (PMC5021160), not inferred.
VOGWILL_DOSE_MULTIPLE = {1: 1.0, 2: 2.0, 3: 4.0}
VOGWILL_EXPOSURE_H = 4.0


def model_ceiling() -> dict:
    """The steepest response the published functional form can produce."""
    cap_rate = bc.PSI_MAX_PR - bc.MIN_VALUE
    psimin = bc.mic_mapping(bc.MIC_WT)

    def a(c):
        return bc._regoes_reduction(c / bc.MIC_WT, bc.PSI_MAX_PR, psimin, bc.KAPPA)

    return {
        "max_persister_kill_rate_per_h": float(cap_rate),
        "max_log_ratio_over_5h": float(cap_rate * bc.TAU_TREAT),
        "slope_at_published_values_per_doubling":
            float((a(25.0) - a(12.5)) * bc.TAU_TREAT),
    }


def ecoli_dose_response() -> pd.DataFrame:
    """Per-pulse survival at each concentration, dataset 1."""
    d = pd.read_csv(RAW / "R_long_data_Alex_and_Sara_CFU_counts.csv",
                    sep=";", decimal=",")
    key = ["Conc", "Replicates_Row"]
    rows = []
    for t0, t1, name in PULSES:
        before = d[d.TimeMin == t0].set_index(key)["CFU_mL"]
        after = d[d.TimeMin == t1].set_index(key)["CFU_mL"]
        for k in before.index:
            if k not in after.index or before[k] <= 0:
                continue
            censored = after[k] <= 0
            rows.append({
                "conc": float(k[0]), "replicate": int(k[1]), "pulse": name,
                "cfu_before": float(before[k]), "cfu_after": float(after[k]),
                "censored": bool(censored),
                "ln_survival": float(np.log(after[k] / before[k]))
                if not censored else np.nan,
            })
    return pd.DataFrame(rows)


def series_quality(conc, ln_surv) -> dict:
    """Whether a dose-response series is fit to be quoted at all.

    A slope per doubling is only meaningful if survival actually falls with
    concentration. Three checks are applied and reported rather than assumed:
    Spearman rank correlation, which should approach -1 for a clean series; the
    coefficient of determination of the log-linear fit; and leave-one-out, which
    catches a slope carried by a single concentration.

    This gate exists because the third exposure pulse of dataset 1 fails all
    three. Its slope has an R-squared of 0.15 and a p-value of 0.61, so it is not
    distinguishable from no dose response, and dropping one of its four
    concentrations moves the slope from -0.83 to -0.30. A number of that
    stability should not appear beside the two pulses that behave.
    """
    conc = np.asarray(conc, dtype=float)
    ln_surv = np.asarray(ln_surv, dtype=float)
    ok = np.isfinite(ln_surv) & (conc > 0)
    c, y = conc[ok], ln_surv[ok]
    if c.size < 3:
        return {"usable": False, "reason": "fewer than three concentrations"}

    lr = stats.linregress(np.log2(c), y)
    rho = stats.spearmanr(c, y).statistic
    slopes = []
    for j in range(c.size):
        m = np.ones(c.size, dtype=bool)
        m[j] = False
        if m.sum() >= 3:
            slopes.append(stats.linregress(np.log2(c[m]), y[m]).slope)
    swing = float(np.max(np.abs(np.asarray(slopes) - lr.slope))) if slopes else np.nan

    usable = bool(lr.pvalue < 0.05 and rho < 0 and swing < 0.5 * abs(lr.slope))
    reasons = []
    if lr.pvalue >= 0.05:
        reasons.append(f"slope not distinguishable from zero (p={lr.pvalue:.2f})")
    if rho >= 0:
        reasons.append(f"survival does not fall with concentration (rho={rho:+.2f})")
    if not (swing < 0.5 * abs(lr.slope)):
        reasons.append(f"one concentration moves the slope by {swing:.2f}")
    return {"usable": usable, "r_squared": float(lr.rvalue ** 2),
            "p_value": float(lr.pvalue), "spearman_rho": float(rho),
            "monotone": bool(pd.Series(y, index=c).sort_index().is_monotonic_decreasing),
            "max_leave_one_out_swing": swing,
            "reason": "; ".join(reasons)}



def slope_per_doubling(conc, ln_surv) -> float:
    """Regression of ln survival on log2 concentration."""
    conc = np.asarray(conc, dtype=float)
    ln_surv = np.asarray(ln_surv, dtype=float)
    ok = np.isfinite(ln_surv) & (conc > 0)
    if ok.sum() < 3:
        return float("nan")
    return float(np.polyfit(np.log2(conc[ok]), ln_surv[ok], 1)[0])


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)

    ceiling = model_ceiling()
    rows = []

    ec = ecoli_dose_response()
    ec.to_csv(TABLES / "exp11_ecoli_dose_response.csv", index=False)
    n_censored = int(ec["censored"].sum())

    for pulse, g in ec[~ec["censored"]].groupby("pulse"):
        m = g.groupby("conc")["ln_survival"].mean()
        above = m[m.index >= AMP_MIC_REGION]
        rows.append({
            "dataset": "E. coli MG1655, recurrent ampicillin",
            "organism": "E. coli", "antibiotic": "ampicillin",
            "stratum": pulse,
            "n_levels": int(len(above)),
            "n_obs": int((g["conc"] >= AMP_MIC_REGION).sum()),
            "slope_ln_per_doubling": slope_per_doubling(above.index, above.values),
            **{f"quality_{k}": v for k, v in
               series_quality(above.index, above.values).items()},
            "exposure_h": EXPOSURE_MIN / 60.0,
            "dose_axis": "ug/mL, measured",
        })

    vg = pd.read_excel(RAW / "Vogwill+JEB+persistence+resistance.xlsx",
                       sheet_name="Survival scores")
    names = {"Cip": "ciprofloxacin", "Rif": "rifampicin"}
    for ab, g in vg.groupby("Antibiotic"):
        m = g.groupby("Relative dose")["Log survival"].mean() * np.log(10)
        # The three levels are 1x, 2x and 4x MIC, not 1, 2 and 3. See the
        # docstring: taking the labels literally shortens the log2 axis and
        # inflates the slope.
        conc = np.array([VOGWILL_DOSE_MULTIPLE[int(d)] for d in m.index], float)
        rows.append({
            "dataset": "Vogwill et al., 8 Pseudomonas species",
            "organism": "Pseudomonas spp.",
            "antibiotic": names.get(ab, ab),
            "stratum": "pooled over species",
            "n_levels": int(len(m)),
            "n_obs": int(len(g)),
            "slope_ln_per_doubling": slope_per_doubling(conc, m.values),
            "exposure_h": VOGWILL_EXPOSURE_H,
            "dose_axis": "multiples of MIC: 1x, 2x, 4x, from the paper's Methods",
        })

    obs = pd.DataFrame(rows)
    obs["model_slope_per_doubling"] = ceiling["slope_at_published_values_per_doubling"]
    obs["steeper_than_model_by"] = (obs["slope_ln_per_doubling"].abs()
                                    / abs(ceiling["slope_at_published_values_per_doubling"]))
    # The ceiling is a rate limit, so it has to be matched to each experiment's
    # own exposure duration before it means anything. Where the duration is not
    # recorded the 5 h of the published protocol is used, which is the most
    # generous assumption available to the model.
    hours = obs["exposure_h"].fillna(bc.TAU_TREAT)
    obs["model_ceiling_at_this_exposure"] = ceiling["max_persister_kill_rate_per_h"] * hours
    obs["exceeds_model_ceiling"] = (obs["slope_ln_per_doubling"].abs()
                                    > obs["model_ceiling_at_this_exposure"])
    obs.to_csv(TABLES / "exp11_slopes.csv", index=False)

    (RECEIPTS / "exp11_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp11_external_concentration_response.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model_ceiling": ceiling,
        "datasets": sorted(obs["dataset"].unique().tolist()),
        "n_strata": int(len(obs)),
        "n_steeper_than_model": int((obs["steeper_than_model_by"] > 1).sum()),
        "n_exceeding_ceiling": int(obs["exceeds_model_ceiling"].sum()),
        "median_steepness_ratio": float(obs["steeper_than_model_by"].median()),
        "ecoli_censored_observations": n_censored,
    }, indent=2), encoding="utf-8")

    pd.set_option("display.width", 220)
    print("-- what the published functional form can produce --")
    for k, v in ceiling.items():
        print(f"   {k:<46} {v:8.4f}")

    print("\n-- what independent data show --")
    if "quality_usable" in obs.columns:
        q = obs.dropna(subset=["quality_usable"])
        print()
        print("-- is each dose-response series fit to be quoted at all? --")
        print(q[["stratum", "quality_r_squared", "quality_p_value",
                 "quality_spearman_rho", "quality_max_leave_one_out_swing",
                 "quality_usable", "quality_reason"]].to_string(
            index=False, float_format=lambda v: f"{v:,.3f}"))
        bad = q[~q["quality_usable"].astype(bool)]
        for _, b in bad.iterrows():
            print()
            print(f"{b['stratum']} FAILS the gate: {b['quality_reason']}.")
        if len(bad):
            print("   Its slope is reported below for completeness and must not be quoted")
            print("   alongside the series that pass. The headline comparison rests on the")
            print("   series that do.")

    print()
    print("-- what independent data show --")
    print(obs[["organism", "antibiotic", "stratum", "n_obs", "exposure_h",
               "slope_ln_per_doubling", "model_slope_per_doubling",
               "steeper_than_model_by", "model_ceiling_at_this_exposure",
               "exceeds_model_ceiling"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3f}"))
    print(f"\n{n_censored} of {len(ec)} E. coli pulse-replicate pairs fell below "
          "detection and are excluded from the slopes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
