"""
Re-run Boccarella et al.'s own simulation with the persistence level their own
survival data implies, and ask whether their evolutionary conclusion survives.

Run:  python -m src.experiments.exp04_boccarella_alpha        (first)
      python -m src.experiments.exp05_boccarella_recalibrated [n_replicates]

Their headline result is a contrast: low-persistence populations evolve higher
final resistance than high-persistence populations. That contrast is produced by
simulating two chosen persistence levels, alpha = 0.8 and alpha = 5e-5.

exp04 estimated alpha from their own supplementary survival data. The
low-persistence arm implies alpha near 1e-3, roughly nineteen times the
simulated value. The high-persistence arm implies a value the model cannot
reach at all: the observed survival exceeds the model's ceiling, so alpha is
pinned at 1.

This script runs their deposited simulation, unmodified, at both the simulated
and the implied persistence levels, and compares the resulting distributions of
final MIC. The question is not whether their model is correctly implemented, it
is theirs and is executed verbatim. The question is whether the conclusion is a
property of the data or of the two numbers that were chosen.

Because alpha is not identifiable from survival data (exp04, panel C), the
implied values are not presented as estimates of a true persistence level. They
are the values consistent with the observed survival under the authors' own
pharmacodynamic assumptions. That is the strongest statement the data supports.

Writes, incrementally so partial runs are usable:
  results/tables/exp05_replicates.csv     one row per simulated population
  results/tables/exp05_summary.csv        the contrast, by scenario
  results/receipts/exp05_receipt.json
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
ALPHA_TABLE = TABLES / "exp04_alpha_estimates.csv"

C_UGML = 12.5          # the concentration with the largest experimental n
SEED_BASE = 20260903


def calibrated_alphas() -> dict:
    """Persistence levels implied by the authors' own day-2 survival data."""
    est = pd.read_csv(ALPHA_TABLE)
    est = est[(est.AB_conc == C_UGML) & (est.time_day == 2)]
    out = {}
    for arm, nut in (("high", 0.25), ("low", 0.80)):
        row = est[est.nutrient_conc == nut].iloc[0]
        out[arm] = {"alpha": float(row["alpha_hat"]),
                    "pinned": bool(row["alpha_hits_upper_bound"]),
                    "ci": (float(row["alpha_ci_low"]), float(row["alpha_ci_high"])),
                    "observed_survival": float(row["geo_mean_survival"])}
    return out


def build_jobs(n_low: int, n_high: int):
    """Interleave scenarios so partial results stay balanced and usable.

    Runtime is strongly asymmetric: a high-persistence replicate takes four to
    ten times as long as a low-persistence one, because more of the population
    survives each pulse and more lineages accumulate. Running the scenarios
    block by block would spend the first hours entirely on the slowest and least
    informative arm, so jobs are emitted round-robin and the high arm is given
    fewer replicates.
    """
    cal = calibrated_alphas()
    scenarios = [
        ("authors", "high", bc.ALPHA_HIGH, n_high),
        ("authors", "low", bc.ALPHA_LOW, n_low),
        ("implied", "high", cal["high"]["alpha"], n_high),
        ("implied", "low", cal["low"]["alpha"], n_low),
    ]
    per_scen = []
    for scen, arm, alpha, n in scenarios:
        per_scen.append([(scen, arm, alpha, k) for k in range(n)])

    jobs, meta = [], []
    sid = 0
    for k in range(max(len(s) for s in per_scen)):
        for lst in per_scen:
            if k >= len(lst):
                continue
            scen, arm, alpha, rep = lst[k]
            jobs.append((default_params(alpha, c=C_UGML, sim_id=sid),
                         SEED_BASE + sid))
            meta.append({"scenario": scen, "arm": arm, "alpha": alpha,
                         "replicate": rep, "simulation_id": sid})
            sid += 1
    return jobs, meta, cal, [(s, a, al) for s, a, al, _ in scenarios]


def main() -> int:
    n_low = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    n_high = int(sys.argv[2]) if len(sys.argv) > 2 else max(12, n_low // 3)
    for d in (TABLES, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)
    if not ALPHA_TABLE.exists():
        raise SystemExit("run exp04_boccarella_alpha first")

    jobs, meta, cal, scenarios = build_jobs(n_low, n_high)
    print(f"{len(jobs)} replicates over {len(scenarios)} scenarios at "
          f"{C_UGML} ug/mL: {n_low} per low-persistence arm, {n_high} per "
          f"high-persistence arm (those run 4-10x slower)")
    for scen, arm, a in scenarios:
        note = ""
        if scen == "implied" and arm == "high" and cal["high"]["pinned"]:
            note = (f"  (pinned at 1; observed survival "
                    f"{cal['high']['observed_survival']:.3g} exceeds the model "
                    f"ceiling {bc.persister_survival_factor(C_UGML):.3g})")
        print(f"   {scen:>9s} / {arm:<5s} alpha = {a:.4g}{note}")

    out_path = TABLES / "exp05_replicates.csv"
    meta_by_id = {m['simulation_id']: m for m in meta}
    rows, t0 = [], time.perf_counter()
    n_workers = max(1, min(14, (mp.cpu_count() or 4) - 2))
    print(f"\nrunning on {n_workers} workers, writing incrementally to "
          f"{out_path.name}\n")

    with mp.Pool(n_workers) as pool:
        for i, res in enumerate(pool.imap_unordered(run_one, jobs, chunksize=1)):
            m = meta_by_id[res["simulation_id"]]
            rows.append({**m,
                         "final_mic": res["most_common_mic"],
                         "average_mic_day_12": res.get("average_mic_day_12"),
                         "extinct": res["extinct"],
                         "seed": res["seed"]})
            if (i + 1) % 5 == 0 or i + 1 == len(jobs):
                pd.DataFrame(rows).to_csv(out_path, index=False)
                el = time.perf_counter() - t0
                rate = (i + 1) / el
                print(f"   {i+1:>4d}/{len(jobs)}  {el/60:5.1f} min elapsed, "
                      f"~{(len(jobs)-i-1)/rate/60:5.1f} min left")

    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)

    # ------------------------------------------------------------ summary --
    # Two bases, because the authors' Fig_3_a-b.R line 70 filters to
    # `final_MIC > 2` before plotting. Their published contrast is therefore
    # conditional on resistance having evolved. Reporting only the unfiltered
    # basis would compare against a quantity their figure never shows;
    # reporting only the filtered basis would hide a real difference in how
    # often resistance establishes at all. Both are given.
    alive = df[~df["extinct"]]
    evolved = alive[alive["final_mic"] > 2.001]

    def block(frame, tag):
        g = (frame.groupby(["scenario", "arm"])
             .agg(**{f"n_{tag}": ("final_mic", "size"),
                     f"median_{tag}": ("final_mic", "median"),
                     f"q25_{tag}": ("final_mic",
                                    lambda v: float(np.percentile(v, 25))),
                     f"q75_{tag}": ("final_mic",
                                    lambda v: float(np.percentile(v, 75)))})
             .reset_index())
        return g

    summ = block(alive, "all").merge(block(evolved, "evolved"),
                                     on=["scenario", "arm"], how="outer")
    extra = (alive.groupby(["scenario", "arm"])
             .agg(alpha=("alpha", "first"),
                  frac_never_evolved=("final_mic",
                                      lambda v: float((v <= 2.001).mean())))
             .reset_index())
    ext = (df.groupby(["scenario", "arm"])["extinct"].mean()
             .rename("extinction_fraction").reset_index())
    summ = summ.merge(extra, on=["scenario", "arm"]).merge(
        ext, on=["scenario", "arm"])
    summ.to_csv(TABLES / "exp05_summary.csv", index=False)

    contrasts = []
    for scen in ("authors", "implied"):
        s = summ[summ.scenario == scen].set_index("arm")
        if not {"high", "low"} <= set(s.index):
            continue
        row = {"scenario": scen}
        for tag, label in (("all", "all_populations"),
                           ("evolved", "evolved_only")):
            lo = float(s.loc["low", f"median_{tag}"])
            hi = float(s.loc["high", f"median_{tag}"])
            row[f"median_low_{label}"] = lo
            row[f"median_high_{label}"] = hi
            row[f"ratio_low_over_high_{label}"] = lo / hi
            row[f"log2_gap_{label}"] = float(np.log2(lo / hi))
        row["frac_never_evolved_low"] = float(s.loc["low", "frac_never_evolved"])
        row["frac_never_evolved_high"] = float(s.loc["high", "frac_never_evolved"])
        contrasts.append(row)
    con = pd.DataFrame(contrasts)
    con.to_csv(TABLES / "exp05_contrast.csv", index=False)

    (RECEIPTS / "exp05_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp05_boccarella_recalibrated.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "simulation_code": "external/boccarella2026/"
                           "magnitude_of_evolution_simulations.py, unmodified",
        "code_source_doi": "10.6084/m9.figshare.31389142",
        "paper_doi": "10.1093/molbev/msag180",
        "licence": "CC BY 4.0",
        "concentration_ug_ml": C_UGML,
        "replicates_low_arm": n_low,
        "replicates_high_arm": n_high,
        "alphas": {f"{s}/{a}": v for s, a, v in scenarios},
        "high_arm_alpha_pinned_at_1": cal["high"]["pinned"],
        "runtime_minutes": round((time.perf_counter() - t0) / 60, 1),
    }, indent=2), encoding="utf-8")

    print("\n-- final MIC by scenario (surviving populations) --")
    print(summ.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print("\n-- the contrast their conclusion rests on --")
    print(con.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
