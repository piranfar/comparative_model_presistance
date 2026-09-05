"""
Where does the persistence level start to matter?

Run:  python -m src.experiments.exp08_persistence_threshold [n_rep]

THE CLAIM UNDER TEST. Outcomes are insensitive to the persister fraction over
orders of magnitude, because the survivors of each dose fully regrow before the
next one arrives, erasing the difference in bottleneck size. The persistence
level should only begin to matter once the bottleneck is small enough that the
population cannot recover within the regrowth window, or small enough that
stochastic loss bites.

If that is right, a sweep of alpha across five orders of magnitude gives a flat
response with a break at one end, and the location of the break is set by the
regrowth window and the growth rate rather than by anything about persistence.
If instead the response varies smoothly with alpha, the claim is wrong and the
idea should be dropped.

WHY IT MATTERS. Every model of antibiotic persistence carries a persister
fraction, published values span orders of magnitude, and models with very
different values reach similar conclusions. Nobody has said why. A threshold
would explain it, would say for which organisms and regimens persistence is
worth measuring at all, and would explain as a by-product why the parameter is
hard to estimate: a quantity with no effect over most of its range leaves no
signature in data.

The simulation is Boccarella et al.'s, run unmodified
(doi:10.6084/m9.figshare.31389142, CC BY 4.0), so the sweep is a property of a
published model rather than of one we wrote to suit ourselves.

Writes:
  results/tables/exp08_alpha_sweep.csv       one row per simulated population
  results/tables/exp08_threshold.csv         summary by alpha
  results/receipts/exp08_receipt.json
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

from ..models.boccarella_runner import default_params, run_one

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

C_UGML = 12.5
SEED_BASE = 5510000

# Five orders of magnitude, log-spaced, plus the two values Boccarella et al.
# simulate so the sweep contains their own points.
ALPHAS = sorted({1e-5, 5e-5, 1e-4, 9.576e-4, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 0.8})

# The expected bottleneck after one pulse, for context: alpha * N0 * survival.
N0 = 2e8


def main() -> int:
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    for d in (TABLES, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)

    jobs, meta, sid = [], [], 0
    for rep in range(n_rep):              # replicate-major so partials are balanced
        for a in ALPHAS:
            jobs.append((default_params(a, c=C_UGML, sim_id=sid),
                         SEED_BASE + sid))
            meta.append({"alpha": a, "replicate": rep, "simulation_id": sid})
            sid += 1
    by_id = {m["simulation_id"]: m for m in meta}

    print(f"alpha sweep: {len(ALPHAS)} levels x {n_rep} replicates = {len(jobs)} "
          f"populations at {C_UGML} ug/mL")
    print(f"alphas: {', '.join(f'{a:g}' for a in ALPHAS)}\n")

    out = TABLES / "exp08_alpha_sweep.csv"
    rows, t0 = [], time.perf_counter()
    n_workers = max(1, min(14, (mp.cpu_count() or 4) - 2))
    with mp.Pool(n_workers) as pool:
        for i, res in enumerate(pool.imap_unordered(run_one, jobs, chunksize=1)):
            m = by_id[res["simulation_id"]]
            rows.append({**m, "final_mic": res["most_common_mic"],
                         "extinct": res["extinct"]})
            if (i + 1) % 10 == 0 or i + 1 == len(jobs):
                pd.DataFrame(rows).to_csv(out, index=False)
                el = time.perf_counter() - t0
                print(f"   {i+1:>4d}/{len(jobs)}  {el/60:5.1f} min, "
                      f"~{(len(jobs)-i-1)/((i+1)/el)/60:5.1f} min left")

    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)

    alive = df[~df["extinct"]]
    summ = (alive.groupby("alpha")
            .agg(n=("final_mic", "size"),
                 median_all=("final_mic", "median"),
                 median_evolved=("final_mic",
                                 lambda v: float(np.median(v[v > 2.001]))
                                 if (v > 2.001).any() else np.nan),
                 frac_never_evolved=("final_mic",
                                     lambda v: float((v <= 2.001).mean())),
                 q25=("final_mic", lambda v: float(np.percentile(v, 25))),
                 q75=("final_mic", lambda v: float(np.percentile(v, 75))))
            .reset_index())
    # expected survivors of one pulse, the quantity the threshold should track
    from ..models import boccarella as bc
    surv = bc.persister_survival_factor(C_UGML)
    summ["expected_survivors_per_pulse"] = summ["alpha"] * N0 * surv
    summ["doublings_to_refill"] = np.log2(N0 / summ["expected_survivors_per_pulse"])
    summ["hours_to_refill_at_r1"] = summ["doublings_to_refill"] * np.log(2) / 1.0
    summ["fits_in_19h_regrowth"] = summ["hours_to_refill_at_r1"] < 19.0
    summ.to_csv(TABLES / "exp08_threshold.csv", index=False)

    (RECEIPTS / "exp08_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp08_persistence_threshold.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "simulation_code": "external/boccarella2026/"
                           "magnitude_of_evolution_simulations.py, unmodified",
        "code_source_doi": "10.6084/m9.figshare.31389142",
        "licence": "CC BY 4.0",
        "concentration_ug_ml": C_UGML,
        "alphas": ALPHAS,
        "replicates_per_alpha": n_rep,
        "persister_survival_per_pulse": surv,
        "runtime_minutes": round((time.perf_counter() - t0) / 60, 1),
    }, indent=2), encoding="utf-8")

    print("\n-- outcome against persistence level --")
    print(summ[["alpha", "n", "median_evolved", "frac_never_evolved",
                "expected_survivors_per_pulse", "hours_to_refill_at_r1",
                "fits_in_19h_regrowth"]].to_string(
        index=False, float_format=lambda v: f"{v:,.4g}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
