"""
How much of the drug's effect survives nutrient limitation, for ordinary cells
and for dormant ones.

Run:  python -m src.experiments.exp14_nutrient_dependent_pd

WHY. Section 2 of the shielding manuscript found that the model of Boccarella et
al. loses the concentration axis: its survival moves twofold across a 32-fold
concentration range where the measurements move 730-fold. exp13 located the
cause in the ordinary-cell compartment rather than the dormant one, since the
model's persister kill rate already matches the measured one.

This script asks what the ordinary-cell kill rate actually is, and finds that
the variable it depends on is not concentration but nutrient availability. The
drug in this dataset is amikacin, an aminoglycoside, whose uptake requires the
proton-motive force and therefore active metabolism, so a strong dependence on
nutrient level is the expected physiology rather than a surprise.

WHAT IS MEASURED, and what is not. Two rates are read off each curve:

  - the ordinary-cell kill rate, as the largest instantaneous rate of decline
    over the observed time points, which is the fast phase where one exists;
  - the persister kill rate, as the slope of the slow phase, from exp13.

Neither is a fitted pharmacodynamic parameter. Fitting the three-parameter
Regoes form to six concentrations per nutrient level was attempted and abandoned:
the optimiser puts zMIC and psi_min on their bounds, which is over-parameterisation
rather than estimation. The rates below are read from the data directly and carry
no functional form.

WHAT IT FINDS. Ordinary-cell killing falls roughly nineteenfold between rich
medium and starvation, from 10.4/h to 0.56/h. Persister killing barely moves,
0.15 to 0.81/h across the same range. The ratio between them, which is the
selective advantage of being dormant, therefore collapses from 27-fold at
intermediate nutrient levels to 3.6-fold under starvation: when the drug cannot
kill ordinary cells, there is little left for dormancy to protect against.

The model under test uses a single ordinary-cell kill rate for every condition,
7.06/h at 12.5 ug/mL. The measured value at that concentration runs from 0.41/h
to 9.55/h depending on how well fed the population is.

Data: Windels et al. 2024, ISME J 18(1):wrae070, deposited at
doi:10.5281/zenodo.7550302 under CC BY 4.0.

Writes:
  results/tables/exp14_kill_rates_by_nutrient.csv
  results/receipts/exp14_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ..models import boccarella as bc

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent          # data/ is shared with the current paper
DATA = REPO / "data" / "raw" / "windels2024" / "timekill.csv"
SLOW = ROOT / "results" / "tables" / "exp13_slow_phase_fits.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

REFERENCE_C = 12.5      # the concentration the model is compared at


def instantaneous_rates(series: pd.Series) -> np.ndarray:
    """Kill rate between consecutive time points, per hour."""
    s = np.log(series.dropna())
    if len(s) < 2:
        return np.array([])
    return -np.diff(s.values) / np.diff(s.index.values.astype(float))


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)

    d = pd.read_csv(DATA)
    d = d[d["surv_frac"] > 0]
    slow = pd.read_csv(SLOW)

    rows = []
    for nut, g in d.groupby("nutrient_conc"):
        piv = (g.groupby(["AB_conc", "time"])["surv_frac"]
               .apply(lambda v: float(np.exp(np.log(v).mean()))).unstack())
        fast, at_ref = [], np.nan
        for c in piv.index:
            r = instantaneous_rates(piv.loc[c])
            if r.size:
                fast.append(float(np.nanmax(r)))
                if float(c) == REFERENCE_C:
                    at_ref = float(np.nanmax(r))
        sl = slow[(slow["nutrient_conc"] == nut) & (slow["AB_conc"] >= 50)]
        if not fast or sl.empty:
            continue
        nf = float(np.median(fast))
        ns = float(sl["persister_kill_rate_per_h"].median())
        rows.append({
            "nutrient_conc": nut,
            "n_concentrations": len(fast),
            "normal_kill_median_per_h": nf,
            "normal_kill_min_per_h": float(np.min(fast)),
            "normal_kill_max_per_h": float(np.max(fast)),
            "normal_kill_at_12.5_per_h": at_ref,
            "persister_kill_median_per_h": ns,
            "normal_over_persister": nf / ns if ns else np.nan,
        })
    out = pd.DataFrame(rows).sort_values("nutrient_conc")
    out.to_csv(TABLES / "exp14_kill_rates_by_nutrient.csv", index=False)

    psimin = bc.mic_mapping(bc.MIC_WT)
    model_normal = bc._regoes_reduction(REFERENCE_C / bc.MIC_WT, bc.B_S,
                                        bc.PSI_MIN_S, bc.KAPPA)
    model_pers = bc._regoes_reduction(REFERENCE_C / bc.MIC_WT, bc.PSI_MAX_PR,
                                      psimin, bc.KAPPA)

    span_normal = out["normal_kill_median_per_h"].max() / out["normal_kill_median_per_h"].min()
    span_pers = out["persister_kill_median_per_h"].max() / out["persister_kill_median_per_h"].min()

    (RECEIPTS / "exp14_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp14_nutrient_dependent_pd.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_doi": "10.5281/zenodo.7550302",
        "antibiotic": "amikacin",
        "reference_concentration_ug_ml": REFERENCE_C,
        "model_normal_kill_per_h": float(model_normal),
        "model_persister_kill_per_h": float(model_pers),
        "measured_normal_kill_span_fold": float(span_normal),
        "measured_persister_kill_span_fold": float(span_pers),
        "advantage_of_dormancy_max_fold": float(out["normal_over_persister"].max()),
        "advantage_of_dormancy_min_fold": float(out["normal_over_persister"].min()),
        "note": "rates read directly from the curves; no pharmacodynamic form fitted",
    }, indent=2), encoding="utf-8")

    pd.set_option("display.width", 200)
    print("-- kill rates by nutrient level, read from the curves --")
    print(out[["nutrient_conc", "n_concentrations", "normal_kill_median_per_h",
               "normal_kill_at_12.5_per_h", "persister_kill_median_per_h",
               "normal_over_persister"]].to_string(
        index=False, float_format=lambda v: f"{v:,.2f}"))

    print(f"\nordinary-cell killing spans {span_normal:.0f}-fold across nutrient levels")
    print(f"persister killing spans {span_pers:.1f}-fold across the same range")
    print(f"the advantage of dormancy runs from "
          f"{out['normal_over_persister'].min():.1f}x to "
          f"{out['normal_over_persister'].max():.1f}x")
    print(f"\nthe model uses one value for every condition: "
          f"{model_normal:.2f}/h ordinary, {model_pers:.2f}/h dormant, "
          f"at {REFERENCE_C:g} ug/mL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
