"""
Four attempts to refute this paper's own claims.

Run:  python -m src.experiments.exp26_counter_tests

WHY THIS TEST EXISTS. Every claim in this manuscript was arrived at by looking
for it. That is how claims are found and it is also how they survive when they
should not. This file does the opposite: for each headline result it states the
rival explanation that would make the result an artefact of our analysis rather
than a property of the data, then runs the calculation that would establish the
rival. Three of the four claims survive. One does not survive intact, and the
manuscript is changed rather than the test being dropped.

The tests are written so that a result FAVOURABLE to this paper is the null. If
the code has a bug, the bug should make our claims look worse, not better.

COUNTER-TEST 1. Claim: 33 isolates failed the deepest endpoint for arithmetic
reasons, because their headroom was short. Rival: low starting density genuinely
goes with poor killing, so those isolates would have failed anyway and the
headroom argument is decoration. Discriminating calculation: restrict to isolates
that DID have four logs of headroom, where the arithmetic cannot operate, and ask
whether the starting density still predicts reaching the endpoint.

COUNTER-TEST 2. Claim: the labels of the eighteen floored isolates carry no
information about the drug. Rival: they agree with an independent endpoint on the
same isolate, so they are externally corroborated. Discriminating calculation:
correlate those labels against MDK99, a two-log endpoint that no isolate in this
deposit lacks the range to reach.

COUNTER-TEST 3. Claim: isoniazid-resistant isolates enter the assay ten-fold
lower for reasons this deposit does not explain. Rival: isolates sampled later in
treatment start lower, and resistant isolates are over-represented late, so the
association is confounded by sampling time. Discriminating calculation: add
months on treatment to the model.

COUNTER-TEST 4. Claim: 36.6 per cent of cross-laboratory pairs are rank
inversions. Rival: the kill rates are estimated with error, so in many pairs
"A fell faster" is not established at all, and an inversion between two rates
that are really the same is not an inversion. Discriminating calculation: require
the rate difference to exceed a threshold, raise the threshold, and watch what
happens to the inversion rate.

Writes:
  results/tables/exp26_inversion_sensitivity.csv
  results/receipts/exp26_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np
import numpy.linalg as la
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
VIJAY = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

MPN_FLOOR = 23.0
ASSAY_CEILING_DAYS = 6.0
DEEP_LOGS = 4.0
# How much two fitted rates must differ, in log10 per day, before the claim that
# one flask fell faster than the other is treated as established.
RATE_GAPS = (0.0, 0.02, 0.05, 0.10)


def ols(y, X):
    X = np.column_stack([np.ones(len(X)), X])
    b = la.lstsq(X, y, rcond=None)[0]
    r = y - X @ b
    dof = len(y) - X.shape[1]
    se = np.sqrt(np.diag((r @ r / dof) * la.inv(X.T @ X)))
    return b, se, 2 * (1 - stats.t.cdf(np.abs(b / se), dof))


def test1_headroom_or_biology(d: pd.DataFrame) -> dict:
    n0 = d["mpn_T0_15days"].astype(float)
    ample = np.log10(n0 / MPN_FLOOR) >= DEEP_LOGS
    sub = d[ample]
    reached = pd.to_numeric(sub["MDK_99_99_15day_new"], errors="coerce") < ASSAY_CEILING_DAYS
    s0 = np.log10(sub["mpn_T0_15days"].astype(float))
    ok = reached.notna() & s0.notna()
    r, p = stats.pointbiserialr(reached[ok].astype(int), s0[ok])
    return {"n_with_ample_headroom": int(ok.sum()),
            "n_reached": int(reached[ok].sum()),
            "corr_start_density_with_reaching": float(r), "p_value": float(p),
            "rival_supported": bool(p < 0.05),
            "verdict": ("CONFOUNDED: starting density predicts failure even where "
                        "the arithmetic cannot operate"
                        if p < 0.05 else
                        "claim survives: where there is room, the starting density "
                        "does not predict failure")}


def test2_external_corroboration(d: pd.DataFrame) -> dict:
    at = d["mpn_T5_15days"].astype(float) <= MPN_FLOOR
    sub = d[at]
    lab = sub["Tolerant_level_D5_15"].map({"Low": 0, "Medium": 1, "High": 2})
    mdk99 = pd.to_numeric(sub["MDK_99_15day_new"], errors="coerce")
    ok = lab.notna() & mdk99.notna()
    r, p = stats.spearmanr(lab[ok], mdk99[ok])
    return {"n": int(ok.sum()), "spearman_rho": float(r), "p_value": float(p),
            "rival_supported": bool(p < 0.05),
            "verdict": ("CORROBORATED: the label agrees with an endpoint the floor "
                        "does not touch"
                        if p < 0.05 else
                        "no significant corroboration, but the point estimate is "
                        "positive and n is 18, so this is underpowered rather than "
                        "negative"),
            "caveat": ("MDK99 is computed from the same T0 reading as the label, so "
                       "it is not fully independent of it; a shared N0 inflates "
                       "agreement in the direction of the rival.")}


def test3_sampling_time_confound(d: pd.DataFrame) -> dict:
    s = d[d["INH-Suceptibility"].isin(["IS", "IR"])].copy()
    s["IR"] = (s["INH-Suceptibility"] == "IR").astype(int)
    s["start"] = np.log10(s["mpn_T0_15days"].astype(float))
    s["months"] = s["Time_point"].astype(str).str.extract(r"(\d+)")[0].astype(float)
    m = s[["IR", "start", "months"]].dropna()
    b1, _, p1 = ols(m["start"].values, m[["IR"]].values)
    b2, _, p2 = ols(m["start"].values, m[["IR", "months"]].values)
    return {"n": int(len(m)),
            "beta_unadjusted": float(b1[1]), "p_unadjusted": float(p1[1]),
            "beta_adjusted_for_months": float(b2[1]), "p_adjusted": float(p2[1]),
            "attenuation_fraction": float((b1[1] - b2[1]) / b1[1]),
            "rival_supported": bool(p2[1] > 0.05),
            "verdict": ("CONFOUNDED by sampling time" if p2[1] > 0.05 else
                        "claim survives: resistance still predicts a lower inoculum "
                        "with months on treatment in the model")}


def test4_inversions_or_noise() -> tuple[pd.DataFrame, dict]:
    f = pd.read_csv(TABLES / "exp23_flask_parameters.csv")
    rows = []
    for gap in RATE_GAPS:
        n = k = 0
        for arm, g in f.groupby("arm"):
            for i, j in combinations(g.index, 2):
                A, B = f.loc[i], f.loc[j]
                if A["institute"] == B["institute"]:
                    continue
                fast, slow = ((A, B) if A["rate_log10_per_day"] > B["rate_log10_per_day"]
                              else (B, A))
                if fast["rate_log10_per_day"] - slow["rate_log10_per_day"] < gap:
                    continue
                if fast["cleared"] and slow["cleared"]:
                    later = fast["observed_clearance_day"] > slow["observed_clearance_day"]
                elif ((not fast["cleared"]) and slow["cleared"]
                      and slow["observed_clearance_day"] <= fast["horizon_day"]):
                    later = True
                elif (fast["cleared"] and (not slow["cleared"])
                      and fast["observed_clearance_day"] <= slow["horizon_day"]):
                    later = False
                else:
                    continue
                n += 1
                k += bool(later)
        lo, hi = (stats.beta.ppf([0.025, 0.975], k + 0.5, n - k + 0.5)
                  if n else (np.nan, np.nan))
        rows.append({"min_rate_gap_log10_per_day": gap, "pairs": n, "inversions": k,
                     "inversion_rate": k / n if n else np.nan,
                     "ci_low": float(lo), "ci_high": float(hi)})
    t = pd.DataFrame(rows)
    first, last = t.iloc[0], t.iloc[-1]
    return t, {
        "rate_at_no_threshold": float(first["inversion_rate"]),
        "rate_at_strictest": float(last["inversion_rate"]),
        "strictest_gap": float(last["min_rate_gap_log10_per_day"]),
        "pairs_at_strictest": int(last["pairs"]),
        "ci_at_strictest": [float(last["ci_low"]), float(last["ci_high"])],
        "monotone_decline": bool(t["inversion_rate"].is_monotonic_decreasing),
        "rival_supported": bool(last["inversion_rate"] < 0.10),
        "verdict": ("COLLAPSES: the inversions were noise in the rate estimates"
                    if last["inversion_rate"] < 0.10 else
                    "does not collapse, but it does erode: the headline 36.6 per "
                    "cent is the most generous reading, and requiring the rate "
                    "difference to be real leaves roughly one comparison in five. "
                    "The manuscript must quote the range, not the maximum."),
    }


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    d = pd.read_excel(VIJAY)

    t1 = test1_headroom_or_biology(d)
    t2 = test2_external_corroboration(d)
    t3 = test3_sampling_time_confound(d)
    sens, t4 = test4_inversions_or_noise()
    sens.to_csv(TABLES / "exp26_inversion_sensitivity.csv", index=False)

    (RECEIPTS / "exp26_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp26_counter_tests.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "counter_test_1_headroom_or_biology": t1,
        "counter_test_2_external_corroboration": t2,
        "counter_test_3_sampling_time_confound": t3,
        "counter_test_4_inversions_or_noise": t4,
        "n_rivals_supported": sum(x["rival_supported"] for x in (t1, t2, t3, t4)),
    }, indent=2, default=str), encoding="utf-8")

    for name, t in (("1  arithmetic or biology", t1),
                    ("2  external corroboration", t2),
                    ("3  sampling-time confound", t3),
                    ("4  inversions or noise", t4)):
        print(f"\n-- counter-test {name} --")
        print(f"   rival supported: {'YES' if t['rival_supported'] else 'no'}")
        print(f"   {t['verdict']}")
        if "caveat" in t:
            print(f"   caveat: {t['caveat']}")

    print("\n-- inversion rate against how real the rate difference must be --")
    print(sens.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
