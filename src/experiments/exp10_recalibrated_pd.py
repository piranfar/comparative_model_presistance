"""
Re-run the published simulation with a persister kill response calibrated to
the survival data, and see what survives.

Run:  python -m src.experiments.exp10_recalibrated_pd [n_rep]

WHAT exp09 ESTABLISHED. The ratio of survival at two antibiotic concentrations
is a prediction of the model with effectively no free parameters: the persister
death rate cancels exactly and the persistence level to within 3e-6 in log
units. The model predicts that doubling the concentration from 12.5 to 25 ug/mL
reduces survival 1.55-fold. The deposited data show 75- to 200-fold.

The gap cannot be closed by tuning. With psi_max_PR = 0.05 and the floor on
psi_min_PR set by MIN_VALUE = -0.5, the persister kill rate cannot exceed
0.55/h, so no two concentrations can differ by more than 2.75 in log survival.
Both observations exceed that ceiling. Raising the Hill coefficient makes it
worse rather than better, because at six to twelve times the MIC the response is
already saturated and a steeper curve saturates sooner.

Matching the data needs psi_min_PR near -2.9/h at the wild-type MIC, which is
MIN_VALUE = -3.58: persisters killed roughly six times faster at maximum than
the published floor allows.

WHAT THIS SCRIPT ASKS. Their conclusion is that a high persistence level leads
to a lower final MIC than a low persistence level, a contrast they report as
about 1.7-fold. Does that conclusion survive a persister kill response that
matches the survival data?

It could go either way, and that is why it is worth running. Killing persisters
harder removes the reservoir that carries populations between doses, which could
suppress evolution in both arms and compress the contrast; or it could hurt the
high-persistence arm more, since that arm has more of its population in the
compartment whose kill rate just increased, and widen it.

The simulation is Boccarella et al.'s, run unmodified
(doi:10.6084/m9.figshare.31389142, CC BY 4.0). Only `min_value`, a parameter
their own driver exposes, is changed.

Writes:
  results/tables/exp10_recalibrated_replicates.csv
  results/tables/exp10_recalibrated_contrast.csv
  results/receipts/exp10_receipt.json
"""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ..models import boccarella as bc
from ..models.boccarella_runner import default_params, run_one

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

C_UGML = 12.5
SEED_BASE = 7710000

# psi_min_PR at the wild-type MIC that reproduces the observed concentration
# ratio, and the MIN_VALUE that delivers it through their `mic_mapping`.
PSI_MIN_PR_CALIBRATED = -2.900
MIN_VALUE_CALIBRATED = -3.5824
MIN_VALUE_PUBLISHED = -0.5

ARMS = {"high": bc.ALPHA_HIGH, "low": bc.ALPHA_LOW}
SCENARIOS = {"published": MIN_VALUE_PUBLISHED,
             "calibrated": MIN_VALUE_CALIBRATED}


def predicted_log_ratio(min_value: float) -> float:
    """ln[S(12.5)/S(25)] under a given MIN_VALUE, for the record."""
    psimin = bc.mic_mapping(bc.MIC_WT, min_value=min_value)
    a = lambda c: bc._regoes_reduction(c / bc.MIC_WT, bc.PSI_MAX_PR,
                                       psimin, bc.KAPPA)
    return float((a(25.0) - a(12.5)) * bc.TAU_TREAT)


def main() -> int:
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    for d in (TABLES, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)

    jobs, meta, sid = [], [], 0
    for rep in range(n_rep):                 # replicate-major, so partials stay balanced
        for scen, min_value in SCENARIOS.items():
            for arm, alpha in ARMS.items():
                p = default_params(alpha, c=C_UGML, sim_id=sid)
                p["min_value"] = min_value
                jobs.append((p, SEED_BASE + sid))
                meta.append({"scenario": scen, "arm": arm, "alpha": alpha,
                             "min_value": min_value, "replicate": rep,
                             "simulation_id": sid})
                sid += 1
    by_id = {m["simulation_id"]: m for m in meta}

    for scen, mv in SCENARIOS.items():
        print(f"{scen:<12} min_value={mv:<9.4f} "
              f"predicted ln[S(12.5)/S(25)] = {predicted_log_ratio(mv):.3f}")
    print(f"\nobserved in the deposited data: 4.32 and 5.31")
    print(f"{len(jobs)} runs: {len(SCENARIOS)} scenarios x {len(ARMS)} arms "
          f"x {n_rep} replicates at {C_UGML} ug/mL\n")

    out = TABLES / "exp10_recalibrated_replicates.csv"
    rows, t0 = [], time.perf_counter()
    n_workers = max(1, min(14, (mp.cpu_count() or 4) - 2))
    with mp.Pool(n_workers) as pool:
        for i, res in enumerate(pool.imap_unordered(run_one, jobs, chunksize=1)):
            rows.append({**by_id[res["simulation_id"]],
                         "final_mic": res["most_common_mic"],
                         "extinct": res["extinct"]})
            if (i + 1) % 10 == 0 or i + 1 == len(jobs):
                pd.DataFrame(rows).to_csv(out, index=False)
                el = time.perf_counter() - t0
                print(f"   {i+1:>4d}/{len(jobs)}  {el/60:5.1f} min, "
                      f"~{(len(jobs)-i-1)/((i+1)/el)/60:5.1f} min left")

    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)
    alive = df[~df["extinct"]]

    con = []
    for scen in SCENARIOS:
        s = alive[alive["scenario"] == scen]
        med = {a: float(s[s["arm"] == a]["final_mic"].median()) for a in ARMS}
        ev = {}
        for a in ARMS:
            v = s[s["arm"] == a]["final_mic"]
            ev[a] = float(np.median(v[v > 2.001])) if (v > 2.001).any() else np.nan
        con.append({
            "scenario": scen,
            "min_value": SCENARIOS[scen],
            "predicted_log_ratio": predicted_log_ratio(SCENARIOS[scen]),
            "n_low": int((s["arm"] == "low").sum()),
            "n_high": int((s["arm"] == "high").sum()),
            "median_low": med["low"], "median_high": med["high"],
            "ratio_low_over_high": med["low"] / med["high"] if med["high"] else np.nan,
            "median_low_evolved": ev["low"], "median_high_evolved": ev["high"],
            "ratio_evolved": ev["low"] / ev["high"] if ev["high"] else np.nan,
            "frac_never_evolved_low": float(
                (s[s["arm"] == "low"]["final_mic"] <= 2.001).mean()),
            "frac_never_evolved_high": float(
                (s[s["arm"] == "high"]["final_mic"] <= 2.001).mean()),
            "extinction_fraction": float(
                df[df["scenario"] == scen]["extinct"].mean()),
        })
    contrast = pd.DataFrame(con)
    contrast.to_csv(TABLES / "exp10_recalibrated_contrast.csv", index=False)

    from scipy import stats
    tests = {}
    for scen in SCENARIOS:
        s = alive[alive["scenario"] == scen]
        lo = s[s["arm"] == "low"]["final_mic"]
        hi = s[s["arm"] == "high"]["final_mic"]
        tests[scen] = float(stats.mannwhitneyu(lo, hi).pvalue)

    (RECEIPTS / "exp10_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp10_recalibrated_pd.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "simulation_code": "external/boccarella2026/"
                           "magnitude_of_evolution_simulations.py, unmodified",
        "code_source_doi": "10.6084/m9.figshare.31389142",
        "licence": "CC BY 4.0",
        "concentration_ug_ml": C_UGML,
        "scenarios": SCENARIOS,
        "psi_min_pr_calibrated": PSI_MIN_PR_CALIBRATED,
        "replicates_per_cell": n_rep,
        "arm_separation_p": tests,
        "runtime_minutes": round((time.perf_counter() - t0) / 60, 1),
    }, indent=2), encoding="utf-8")

    print("\n-- does the contrast survive the recalibration? --")
    print(contrast[["scenario", "min_value", "predicted_log_ratio",
                    "median_low", "median_high", "ratio_low_over_high",
                    "frac_never_evolved_low", "frac_never_evolved_high",
                    "extinction_fraction"]].to_string(
        index=False, float_format=lambda v: f"{v:,.4g}"))
    print("\nlow vs high arm, Mann-Whitney p:")
    for scen, p in tests.items():
        print(f"   {scen:<12} p = {p:.4g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
