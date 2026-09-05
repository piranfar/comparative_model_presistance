"""
Test the persister concentration-response against the survival data, without
needing the persistence level at all.

Run:  python -m src.experiments.exp09_concentration_response

WHY THIS TEST EXISTS. exp04 showed that the persistence level alpha is not
identifiable from survival data: survival contains alpha and the persister death
rate only through the product alpha * exp(-(d_P + a_PR(c)) * tau) at a fixed
exposure duration tau, so the data determines a curve in that plane and not a
point. That is a limit on what survival data can supply, and it is not an
objection to any published work, because the persistence level was never claimed
to be estimated from it.

But the same algebra supplies a test that survives the degeneracy. Take the
ratio of survival at two antibiotic concentrations:

    S(c1) / S(c2) = exp( (a_PR(c2) - a_PR(c1)) * tau )

Alpha very nearly cancels, and the persister death rate cancels exactly. What
remains is the concentration-response of persister killing alone, which the model
specifies analytically. Cancellation of alpha is not perfect because survival
also carries a small contribution from the normal compartment, but across the
persistence levels of interest the predicted ratio moves by under 3e-6 in log
units, against a discrepancy of about 4.9. The ratio is therefore a prediction
with effectively no free parameters, and the deposited survival data contains
both concentrations needed to check it.

Nobody appears to have run it. The model, the data and the two concentrations
have been in the same paper and the same deposit since publication.

WHAT IT FINDS. The model predicts that doubling the antibiotic concentration
from 12.5 to 25 ug/mL reduces survival 1.55-fold. The data show 75- to 200-fold.
The persister concentration-response in the model is one to two orders of
magnitude too shallow against the data used to motivate it.

Model and data: Boccarella et al. 2026, Mol Biol Evol 43:msag180,
doi:10.1093/molbev/msag180; simulation code and survival data deposited at
doi:10.6084/m9.figshare.31389142 under CC BY 4.0 and reused here under that
licence. The survival measurements originate with Windels et al. 2024,
ISME J 18(1):wrae070, doi:10.1093/ismejo/wrae070.

Writes:
  results/tables/exp09_concentration_ratio.csv
  results/tables/exp09_alpha_invariance.csv
  results/receipts/exp09_receipt.json
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
REPO = ROOT.parent          # data/ is shared with the current paper
DATA = REPO / "data" / "raw" / "boccarella2026" / "survival_S1.csv"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

C_LOW, C_HIGH = 12.5, 25.0

# The two levels the authors simulate, plus the value exp04 found their own
# survival data to imply. The prediction below must be identical for all three;
# that identity is the point of the test.
ALPHAS = (0.8, 5e-5, 9.576e-4)


def alpha_invariance() -> pd.DataFrame:
    """The predicted ratio, computed at several persistence levels."""
    rows = []
    for a in ALPHAS:
        s_lo, s_hi = bc.survival(a, C_LOW), bc.survival(a, C_HIGH)
        rows.append({
            "alpha": a,
            "model_survival_at_12.5": s_lo,
            "model_survival_at_25": s_hi,
            "log_ratio": float(np.log(s_lo / s_hi)),
            "fold_ratio": float(s_lo / s_hi),
        })
    return pd.DataFrame(rows)


def observed_ratios(df: pd.DataFrame, predicted: float) -> pd.DataFrame:
    """Observed log survival ratio between the two concentrations.

    Compared within a nutrient level and treatment cycle, so the contrast is
    between concentrations and not between conditions. The populations are not
    paired, so this is a two-sample comparison on log survival.
    """
    rows = []
    for (nut, cycle), g in df.groupby(["nutrient_conc", "time"]):
        lo = g[g["AB_conc"] == C_LOW]["surv_frac"].values
        hi = g[g["AB_conc"] == C_HIGH]["surv_frac"].values
        if not len(lo) or not len(hi):
            continue
        l_lo, l_hi = np.log(lo), np.log(hi)
        diff = float(l_lo.mean() - l_hi.mean())
        enough = len(lo) > 1 and len(hi) > 1
        se = float(np.sqrt(l_lo.var(ddof=1) / len(lo) + l_hi.var(ddof=1) / len(hi))) \
            if enough else np.nan
        rows.append({
            "nutrient_conc": nut,
            "cycle": cycle,
            "n_at_12.5": len(lo),
            "n_at_25": len(hi),
            "geo_mean_survival_12.5": float(np.exp(l_lo.mean())),
            "geo_mean_survival_25": float(np.exp(l_hi.mean())),
            "observed_log_ratio": diff,
            "ci95_half_width": 1.96 * se if enough else np.nan,
            "model_log_ratio": predicted,
            "discrepancy_log": diff - predicted,
            "model_understates_by_fold": float(np.exp(diff - predicted)),
            "mannwhitney_p": float(stats.mannwhitneyu(lo, hi).pvalue) if enough else np.nan,
            "ci_excludes_model": bool(enough and abs(diff - predicted) > 1.96 * se),
        })
    return pd.DataFrame(rows)


def main() -> int:
    for d in (TABLES, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)

    inv = alpha_invariance()
    predicted = float(inv["log_ratio"].mean())
    # Alpha cancels from the ratio only in the limit where survival is entirely
    # persister-driven. The normal compartment contributes a little, so the
    # cancellation is very good rather than exact, and the residual has to be
    # small against the discrepancy the test is measuring, not merely small.
    spread = float(inv["log_ratio"].max() - inv["log_ratio"].min())
    if spread > 0.05:
        raise SystemExit(
            f"the predicted ratio moves by {spread:.3g} across the persistence "
            "levels tested, which is not negligible; the test is void")

    df = pd.read_csv(DATA)
    df = df[df["surv_frac"] > 0].copy()
    obs = observed_ratios(df, predicted)

    inv.to_csv(TABLES / "exp09_alpha_invariance.csv", index=False)
    obs.to_csv(TABLES / "exp09_concentration_ratio.csv", index=False)

    (RECEIPTS / "exp09_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp09_concentration_response.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source_doi": "10.6084/m9.figshare.31389142",
        "data_origin_doi": "10.1093/ismejo/wrae070",
        "model_source_doi": "10.1093/molbev/msag180",
        "licence": "CC BY 4.0",
        "tau_hours": bc.TAU_TREAT,
        "concentrations_ug_ml": [C_LOW, C_HIGH],
        "alphas_checked": list(ALPHAS),
        "predicted_log_ratio": predicted,
        "predicted_log_ratio_spread_across_alphas": spread,
        "predicted_fold_ratio": float(np.exp(predicted)),
        "n_comparisons": int(len(obs)),
        "n_excluding_model": int(obs["ci_excludes_model"].sum()),
        "max_understatement_fold": float(obs["model_understates_by_fold"].max()),
    }, indent=2), encoding="utf-8")

    pd.set_option("display.width", 200)
    print("-- the prediction barely depends on the persistence level --")
    print(inv.to_string(index=False, float_format=lambda v: f"{v:,.6g}"))
    print(f"\nmodel: doubling the concentration reduces survival "
          f"{np.exp(predicted):.2f}-fold\n")

    print("-- against the data --")
    print(obs[["nutrient_conc", "cycle", "n_at_12.5", "n_at_25",
               "observed_log_ratio", "ci95_half_width", "model_log_ratio",
               "model_understates_by_fold", "mannwhitney_p",
               "ci_excludes_model"]].to_string(
        index=False, float_format=lambda v: f"{v:,.3f}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
