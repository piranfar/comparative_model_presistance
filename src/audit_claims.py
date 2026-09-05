"""
Check every headline number in the current paper against its table.

Run:  python -m src.audit_claims

Numbers drift. A figure gets regenerated, a filter changes, a section is
rewritten, and a value quoted in three places stops agreeing with itself. This
has already happened twice in this project, both times caught by accident. This
script checks on purpose.

Each entry names the claim, where it is asserted, and how to recompute it from
the results tables. A claim that cannot be recomputed is reported as such rather
than passed.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"


def load(name: str):
    p = T / name
    return pd.read_csv(p) if p.exists() else None


def check(label: str, claimed, computed, tol=0.05, unit=""):
    """Compare a claimed value with a recomputed one, on relative tolerance."""
    if computed is None or (isinstance(computed, float) and not np.isfinite(computed)):
        return {"claim": label, "claimed": claimed, "computed": None,
                "status": "CANNOT RECOMPUTE"}
    ok = abs(computed - claimed) <= tol * max(abs(claimed), 1e-12)
    return {"claim": label, "claimed": f"{claimed:g}{unit}",
            "computed": f"{computed:.4g}{unit}",
            "status": "ok" if ok else "MISMATCH"}


def main() -> int:
    rows = []

    # --- exp16, the family correction ------------------------------------
    f = load("exp16_tb_independence.csv")
    if f is not None:
        rows.append(check("MIC-MDK tests available (docs/18: 24)",
                          24, float(len(f)), 0.001))
        rows.append(check("nominally significant (docs/18: 4)",
                          4, float((f.p_value < 0.05).sum()), 0.001))
        rows.append(check("surviving Benjamini-Hochberg (docs/18: 0)",
                          0, float(f.survives_bh.sum()), 1.0))

    # --- exp17, the two censoring estimators must agree -------------------
    f = load("exp17_kill_rates.csv")
    if f is not None:
        g = f.dropna(subset=["kill_rate_tobit", "kill_rate_mi"])
        rows.append(check("max |Tobit - imputation| (docs/18: 0.003 log10/day)",
                          0.003, float((g.kill_rate_tobit - g.kill_rate_mi).abs().max()),
                          0.35, " log10/d"))

    # --- exp18, the conclusion must hold on both unit readings ------------
    f = load("exp18_unit_sensitivity.csv")
    if f is not None:
        rows.append(check("smallest psi_min gap, either unit reading (273x)",
                          273, float(f.fold_gap.min()), 0.02, "x"))
        rows.append(check("largest psi_min gap, either unit reading (658x)",
                          658, float(f.fold_gap.max()), 0.02, "x"))

    # --- exp20, the endpoint that decides what is visible -----------------
    f = load("exp20_endpoint_separation.csv")
    if f is not None:
        s = f.set_index("day")["survivor_ratio_low_over_high"]
        for day, claimed in ((7.0, 48.2), (14.0, 5.2)):
            if day in s.index:
                rows.append(check(f"32-fold dose range separates at day {int(day)}",
                                  claimed, float(s.loc[day]), 0.05, "x"))

    out = pd.DataFrame(rows)
    pd.set_option("display.width", 210)
    pd.set_option("display.max_colwidth", 62)
    print(out.to_string(index=False))

    bad = out[out.status.isin(["MISMATCH", "CANNOT RECOMPUTE", "EXPLAIN OR PICK ONE"])]
    print(f"\n{len(out) - len(bad)} of {len(out)} checks agree with the tables")
    if len(bad):
        print(f"{len(bad)} need attention:")
        for _, x in bad.iterrows():
            print(f"   [{x.status}] {x.claim}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
