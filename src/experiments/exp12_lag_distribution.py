"""
Is the resuscitation rate a rate? Test the constant-switching assumption against
single-cell lag time data.

Run:  python -m src.experiments.exp12_lag_distribution

WHY THIS MATTERS TO US, NOT ONLY TO OTHERS. Our own state-structured model
carries a constant resuscitation rate k_{P->S}. A constant rate means dormancy
durations are exponentially distributed, and it is that assumption which makes
"the resuscitation rate" a single number that a sensitivity analysis can rank.
Section 3.3 of the journal manuscript reports that this parameter carries 78% of
the first-order variance in time to the limit of detection. That result is
conditional on the exponential assumption, and until now we had not tested it.

Simsek and Kim (2019, PNAS 116:17635-17640, doi:10.1073/pnas.1903836116) measured
lag times for about 12,800 individual Escherichia coli cells and report that the
distribution has a power-law tail with exponent near -2, not an exponential one.
Their supplementary appendix tabulates the counts, so the claim can be checked
rather than taken on trust, and the consequence for a constant-rate model can be
computed.

WHAT THIS SCRIPT DOES.

  A. Refits their logarithmically binned counts to a power law and to an
     exponential, the latter being what a constant switching rate implies.

  B. Computes what the difference does to the quantity our paper reports. Time
     to the limit of detection is a deep-tail quantity, four logs below the
     inoculum, and the deep tail is exactly where the two forms part company.

  C. Shows that under a power law with exponent -2 the mean lag diverges
     logarithmically, so a resuscitation RATE exists only relative to where the
     distribution is truncated.

WHAT IT FINDS. The power law fits their tail better in both replicate series
(R-squared 0.99 and 0.97, against 0.96 and 0.85). The two forms agree to within
20% for the first ten hours, which is why the assumption survives ordinary
time-kill experiments, and then diverge: a hundredfold by forty hours and eleven
orders of magnitude by a week. The dormant pool reaches 1e-4 of its initial size
in 47 h under a constant rate and in about 16,700 h under the power law.

Data are transcribed from the supplementary appendix of Simsek and Kim 2019,
Fig. 2b, which reports logarithmically binned lag times for two independent
experiments.

Writes:
  results/tables/exp12_lag_fits.csv
  results/tables/exp12_tail_divergence.csv
  results/receipts/exp12_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

# Simsek and Kim 2019 PNAS, supplementary appendix, "Data presented in Fig. 2b".
# Logarithmically binned lag times, two independent experiments. Under
# logarithmic binning the bin width grows in proportion to t, so the density is
# the count divided by t.
LAG_DATA = {
    "experiment 2 (n=1,422)": {
        "t_min": [70, 140, 280, 560, 1120, 2240],
        "count": [1372, 36, 7, 5, 4, 1],
    },
    "experiment 3 (n=10,263)": {
        "t_min": [140, 209, 313, 468, 700, 1047, 1565],
        "count": [10093, 66, 39, 32, 18, 10, 5],
    },
}

POWER_LAW_ONSET_MIN = 100.0     # where they report the power law begins
TAIL_TARGET = 1e-4              # fraction of the dormant pool, a deep-tail depth


def _r2(y, yhat) -> float:
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def fit_tail(t, count):
    """Fit the tail to a power law and to an exponential.

    The first bin is the bulk of the population resuming growth promptly, not
    the tail, and is excluded from both fits so that neither form is judged on
    a region the other was never meant to describe.
    """
    t = np.asarray(t, dtype=float)
    density = np.asarray(count, dtype=float) / t
    t_tail, f_tail = t[1:], density[1:]
    ln_f = np.log(f_tail)

    a_pow, b_pow = np.polyfit(np.log(t_tail), ln_f, 1)
    r2_pow = _r2(ln_f, a_pow * np.log(t_tail) + b_pow)

    a_exp, b_exp = np.polyfit(t_tail, ln_f, 1)
    r2_exp = _r2(ln_f, a_exp * t_tail + b_exp)

    return {
        "n_tail_bins": int(len(t_tail)),
        "power_law_exponent": float(a_pow),
        "power_law_r2": float(r2_pow),
        "exponential_rate_per_min": float(-a_exp),
        "exponential_mean_lag_min": float(-1.0 / a_exp) if a_exp < 0 else np.nan,
        "exponential_r2": float(r2_exp),
        "better_fit": "power law" if r2_pow > r2_exp else "exponential",
    }


def tail_divergence(rate_per_min: float, onset: float) -> pd.DataFrame:
    """Dormant fraction still dormant at t, under each form."""
    rows = []
    for t in (60, 120, 300, 600, 1200, 2400, 4800, 9600, 20000):
        exp_s = float(np.exp(-rate_per_min * t))
        pow_s = float((max(t, onset) / onset) ** -1.0)
        rows.append({
            "t_min": t, "t_h": t / 60.0,
            "still_dormant_exponential": exp_s,
            "still_dormant_power_law": pow_s,
            "ratio_power_over_exponential": pow_s / exp_s if exp_s > 0 else np.inf,
        })
    return pd.DataFrame(rows)


def implied_rate_by_truncation(onset: float) -> pd.DataFrame:
    """A t^-2 density has a logarithmically divergent mean.

    The mean over [onset, cut] grows as onset*ln(cut/onset), so an experiment
    that follows cells for longer reports a lower resuscitation rate from the
    same underlying process. A rate fitted this way describes the observation
    window as much as the biology.
    """
    rows = []
    for cut in (1000, 2000, 20000, 200000, 2_000_000):
        mean_lag = onset * np.log(cut / onset)
        rows.append({
            "truncation_min": cut,
            "mean_lag_min": float(mean_lag),
            "implied_rate_per_h": float(60.0 / mean_lag),
        })
    return pd.DataFrame(rows)


def main() -> int:
    for d in (TABLES, RECEIPTS):
        d.mkdir(parents=True, exist_ok=True)

    fits = []
    for name, d in LAG_DATA.items():
        fits.append({"series": name, **fit_tail(d["t_min"], d["count"])})
    fits = pd.DataFrame(fits)
    fits.to_csv(TABLES / "exp12_lag_fits.csv", index=False)

    rate = float(fits["exponential_rate_per_min"].max())   # fastest, most favourable
    div = tail_divergence(rate, POWER_LAW_ONSET_MIN)
    trunc = implied_rate_by_truncation(POWER_LAW_ONSET_MIN)
    div.to_csv(TABLES / "exp12_tail_divergence.csv", index=False)

    t_exp_h = -np.log(TAIL_TARGET) / rate / 60.0
    t_pow_h = POWER_LAW_ONSET_MIN * (1.0 / TAIL_TARGET) / 60.0

    (RECEIPTS / "exp12_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp12_lag_distribution.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source_doi": "10.1073/pnas.1903836116",
        "data_location": "supplementary appendix, Fig. 2b tables",
        "power_law_exponents": fits["power_law_exponent"].tolist(),
        "power_law_r2": fits["power_law_r2"].tolist(),
        "exponential_r2": fits["exponential_r2"].tolist(),
        "power_law_wins_in": int((fits["better_fit"] == "power law").sum()),
        "n_series": int(len(fits)),
        "exponential_rate_used_per_min": rate,
        "hours_to_1e-4_exponential": float(t_exp_h),
        "hours_to_1e-4_power_law": float(t_pow_h),
        "fold_difference_at_1e-4": float(t_pow_h / t_exp_h),
    }, indent=2), encoding="utf-8")

    pd.set_option("display.width", 200)
    print("-- does a constant switching rate describe the lag tail? --")
    print(fits[["series", "n_tail_bins", "power_law_exponent", "power_law_r2",
                "exponential_mean_lag_min", "exponential_r2",
                "better_fit"]].to_string(index=False,
                                         float_format=lambda v: f"{v:,.4g}"))

    print("\n-- where the two forms part company --")
    print(div.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))

    print(f"\ntime for the dormant pool to fall to {TAIL_TARGET:g} of its initial size:")
    print(f"   constant rate: {t_exp_h:8.1f} h")
    print(f"   power law:     {t_pow_h:8.0f} h     ({t_pow_h/t_exp_h:,.0f}x longer)")

    print("\n-- a t^-2 mean diverges, so the rate depends on the window --")
    print(trunc.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
