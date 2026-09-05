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
     pulses.
  2. Vogwill et al., J Evol Biol: survival of eight Pseudomonas species under
     ciprofloxacin and rifampicin at three relative doses, 48 observations per
     antibiotic and dose.

Two further datasets in the same folder vary exposure duration rather than
concentration and so do not enter this test: Stewart and Rozen time-kill curves
for ECOR strains, and the Stepanyan et al. 2015 killing curve for a wild-type
and a high-persistence strain. They bear on the other axis and are left to a
separate analysis.

A CAVEAT ON DATASET 2. Its dose column is labelled "relative dose" with levels
1, 2 and 3. If those are multiples of the MIC then treating them as a
concentration axis is right. If they are ordered categories, the slope per
doubling is not defined and only the direction and rough magnitude survive.
Both readings are reported; the conclusion does not depend on which is correct,
because dataset 1 has real concentrations.

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

from ..models import boccarella as bc

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "external_survival"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

PULSES = [(60, 150, "pulse 1"), (330, 420, "pulse 2"), (1080, 1170, "pulse 3")]
EXPOSURE_MIN = 90.0          # each pulse in dataset 1, from the sampling times
AMP_MIC_REGION = 8.0         # concentrations at or above this are used for the slope


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
            "exposure_h": EXPOSURE_MIN / 60.0,
            "dose_axis": "ug/mL, measured",
        })

    vg = pd.read_excel(RAW / "Vogwill+JEB+persistence+resistance.xlsx",
                       sheet_name="Survival scores")
    names = {"Cip": "ciprofloxacin", "Rif": "rifampicin"}
    for ab, g in vg.groupby("Antibiotic"):
        m = g.groupby("Relative dose")["Log survival"].mean() * np.log(10)
        rows.append({
            "dataset": "Vogwill et al., 8 Pseudomonas species",
            "organism": "Pseudomonas spp.",
            "antibiotic": names.get(ab, ab),
            "stratum": "pooled over species",
            "n_levels": int(len(m)),
            "n_obs": int(len(g)),
            "slope_ln_per_doubling": slope_per_doubling(m.index, m.values),
            "exposure_h": float("nan"),
            "dose_axis": "relative dose levels 1-3, units unconfirmed",
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
