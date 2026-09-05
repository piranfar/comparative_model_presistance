"""
Reproduction check: does the vendored simulation reproduce the authors' own
published final-MIC distribution?

Run:  python -m src.experiments.exp06_reproduce_check [n_low] [n_high]

Nothing downstream is trustworthy until this passes. exp05 compares outcomes
between persistence levels; that comparison only means something if the baseline
reproduces what the authors published at their own persistence levels.

The check matters because the authors' deposited driver does not reproduce their
deposited results. Their `main()` sets min_bR to 1.7, while every row of their
recorded output carries min_bR = 2. That parameter controls whether resistance
carries a fitness cost, so the two settings give materially different evolution.
This script runs the corrected setting and tests it against their published
distribution with a two-sample Kolmogorov-Smirnov test, which is a legitimate
use of that test here because both samples are genuinely random draws.
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
from scipy.stats import ks_2samp

from ..models import boccarella as bc
from ..models.boccarella_runner import default_params, run_one

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent          # data/ is shared with the current paper
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"
THEIRS = REPO / "data" / "raw" / "boccarella2026" / "sim_final_mic_Fig3.csv"
C_UGML = 12.5
SEED_BASE = 771000


def main() -> int:
    n_low = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    n_high = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    theirs = pd.read_csv(THEIRS)
    theirs = theirs[theirs.concentration == C_UGML]

    jobs, meta, sid = [], [], 0
    for arm, alpha, n in (("high", bc.ALPHA_HIGH, n_high),
                          ("low", bc.ALPHA_LOW, n_low)):
        for k in range(n):
            jobs.append((default_params(alpha, c=C_UGML, sim_id=sid),
                         SEED_BASE + sid))
            meta.append({"arm": arm, "alpha": alpha, "simulation_id": sid})
            sid += 1
    by_id = {m["simulation_id"]: m for m in meta}

    print(f"reproduction check: {n_high} high + {n_low} low replicates at "
          f"{C_UGML} ug/mL, min_bR = 2.0 (from their recorded output)\n")
    t0 = time.perf_counter()
    rows = []
    with mp.Pool(max(1, min(14, (mp.cpu_count() or 4) - 2))) as pool:
        for i, res in enumerate(pool.imap_unordered(run_one, jobs, chunksize=1)):
            rows.append({**by_id[res["simulation_id"]],
                         "final_mic": res["most_common_mic"],
                         "extinct": res["extinct"]})
            if (i + 1) % 5 == 0 or i + 1 == len(jobs):
                print(f"   {i+1:>3d}/{len(jobs)}  "
                      f"{(time.perf_counter()-t0)/60:.1f} min")
    mine = pd.DataFrame(rows)
    mine.to_csv(TABLES / "exp06_reproduction.csv", index=False)

    out = []
    for arm in ("high", "low"):
        m = mine[(mine.arm == arm) & (~mine.extinct)]["final_mic"].to_numpy()
        t = theirs[theirs.persistence_level == arm]["final_MIC"].to_numpy()
        ks = ks_2samp(m, t)
        out.append({
            "arm": arm, "n_mine": m.size, "n_theirs": t.size,
            "median_mine": float(np.median(m)), "median_theirs": float(np.median(t)),
            "q25_mine": float(np.percentile(m, 25)),
            "q25_theirs": float(np.percentile(t, 25)),
            "q75_mine": float(np.percentile(m, 75)),
            "q75_theirs": float(np.percentile(t, 75)),
            "ks_statistic": float(ks.statistic), "ks_p": float(ks.pvalue),
            "consistent_at_0.05": bool(ks.pvalue > 0.05),
        })
    res = pd.DataFrame(out)
    res.to_csv(TABLES / "exp06_reproduction_check.csv", index=False)

    ok = bool(res["consistent_at_0.05"].all())
    (RECEIPTS / "exp06_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp06_reproduce_check.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "min_bR_used": 2.0,
        "min_bR_in_their_main": 1.7,
        "reproduces_published_distribution": ok,
        "runtime_minutes": round((time.perf_counter() - t0) / 60, 1),
    }, indent=2), encoding="utf-8")

    print("\n-- my runs against their published simulation output --")
    print(res.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print(f"\nreproduction {'PASSES' if ok else 'FAILS'} at the 5% level")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
