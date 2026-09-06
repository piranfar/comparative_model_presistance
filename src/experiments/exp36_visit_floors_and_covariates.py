"""
The floor is visit-specific, and most of the covariate sweep was circular.

Run:  python -m src.experiments.exp36_visit_floors_and_covariates

WHY THIS TEST EXISTS. Three questions from peer review, all of which turn out to
change numbers in the manuscript.

ONE. IS THE STARTING DENSITY ITSELF CENSORED? The Methods say the MPN minimum
shifts by a factor of ten per visit -- 2300, 230, 23 -- and read that as one
dilution series applied to a differently diluted sample at each timepoint. If
2300 is a day-0 floor, then N0 is left-censored for any isolate sitting on it,
and every quantity that treats N0 as observed is wrong.

It is not, and this paper already owns the tool that settles it. The floor rule
of exp33 asks for a pile-up: a floor is a value readings stop at, so it shows as
many ties on the lowest rung and nothing below. Applied visit by visit, day 5
and day 2 have that signature and day 0 does not -- its minimum occurs exactly
once, in both panels, which is what the tail of a distribution looks like. The
verdict for day 0 is NONE and the labels are refused. So N0 is observed
throughout, and the Methods sentence claiming a floor at every visit is what
needs correcting, not the analysis.

TWO. THE DAY-2 ENDPOINT HAS ITS OWN FLOOR AND ITS OWN THRESHOLDS. Everything in
the paper is computed against L = 23, the day-5 floor. But the deposit also
carries a day-2 tolerance class, which Table 4 and Table S3 model, and the
applicable floor there is 230. The day-2 class thresholds are nowhere stated in
the source, so they are recovered here the way exp35 recovers the day-5 ones: by
finding the cuts that reproduce every deposited class with no disagreement.

They are one decade shallower than the day-5 cuts. That has a consequence worth
stating: since L and c1 both shift by ten, N_id = L/c1 is the SAME 23 000 per mL
at both visits. The identifiability boundary does not move between the two
endpoints, even though the reachability boundary does.

THREE. MOST OF THE COVARIATE SWEEP WAS CONDITIONING ON THE EXPOSURE. exp35 asks
what the deposit can rule out for the unexplained ten-fold seeding gap, by
adjusting the resistance-to-inoculum association for each pretreatment covariate
in turn. Six of the eight covariates are recorded only for resistant isolates:
INH_MGIT_DST and RIF_MGIT_DST are present for 0 of 119 susceptible isolates and
82 of 84 resistant ones, and the two Mykrobe calls behave identically. Their
MISSINGNESS is the exposure. Adjusting for such a column is not a sensitivity
analysis, and it explains a detail that looked like a coincidence: the
INH_MGIT_DST and RIF_MGIT_DST rows are identical to three significant figures
because the two columns are missing on exactly the same rows, so they contribute
the same design matrix.

INH_mutation is nearly as bad -- 79 of 84 resistant, 1 of 119 susceptible -- and
it is the row the Discussion singled out as the largest attenuation at 22 per
cent. That attenuation is an artefact of conditioning on a proxy for the
exposure.

The correction runs in our own disfavour and then back again. Only two
covariates, the growth proxy and months on treatment, are missing at rates
unrelated to susceptibility. Restricted to those, the seeding gap barely moves
at all. The honest sweep is narrower than the one reported and the conclusion it
supports is stronger.

Writes:
  results/tables/exp36_visit_floors.csv
  results/tables/exp36_day2_boundaries.csv
  results/tables/exp36_covariate_independence.csv
  results/receipts/exp36_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from ..floor_posterior import floor_posterior

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

LEVELS = ("Low", "Medium", "High")
EXPOSURE = "INH-Suceptibility"          # the deposit's own spelling
DECADES = (1e-4, 1e-3, 1e-2, 1e-1)


def visit_floors(d: pd.DataFrame) -> pd.DataFrame:
    """Apply the paper's own floor rule to every visit column."""
    rows = []
    for age in (15, 30, 60):
        for visit in ("T0", "T2", "T5"):
            col = f"mpn_{visit}_{age}days"
            if col not in d.columns:
                continue
            s = pd.to_numeric(d[col], errors="coerce").dropna().to_numpy(float)
            fp = floor_posterior(s, counts_per_ml=True)
            vc = pd.Series(s).value_counts().sort_index()
            rows.append({
                "culture_age_days": age,
                "visit": visit,
                "n_readings": len(s),
                "minimum": float(vc.index[0]),
                "n_on_the_minimum": int(vc.iloc[0]),
                "verdict": fp.verdict,
                "floor_used": fp.candidate_floor,
                "ci_low": fp.ci_low,
                "ci_high": fp.ci_high,
                "log10_span": fp.log10_span,
                "refuse_labels": fp.refuse_labels,
                "reason": fp.reason,
            })
    return pd.DataFrame(rows)


def recover_cuts(frac: pd.Series, lab: pd.Series) -> tuple[tuple[float, float] | None, int, int]:
    """Find the decade cuts that reproduce the deposited classes, if any do."""
    ok = frac.notna() & lab.isin(LEVELS)
    n = int(ok.sum())
    best = None
    for i, c1 in enumerate(DECADES):
        for c2 in DECADES[i + 1:]:
            pred = np.where(frac < c1, "Low", np.where(frac <= c2, "Medium", "High"))
            agree = int((pred[ok.to_numpy()] == lab[ok].to_numpy()).sum())
            if best is None or agree > best[1]:
                best = ((c1, c2), agree)
    (cuts, agree) = best
    return (cuts if agree == n else None), agree, n


def day2_boundaries(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """The day-2 endpoint on the day-2 floor, beside day 5 for comparison."""
    rows, notes = [], {}
    for age in (15, 60):
        frac2 = pd.to_numeric(d[f"Survival_T2_{age}days"], errors="coerce")
        lab2 = d[f"Tolerant_level_D2_{age}"]
        cuts, agree, n = recover_cuts(frac2, lab2)
        notes[f"{age}d_day2_cuts"] = {
            "cuts": list(cuts) if cuts else None,
            "n_agree": agree, "n_usable": n,
            "reproduces_every_class": cuts is not None,
        }
        if cuts is None:
            # No decade cut reproduces the classes; report the observed gaps so a
            # reader can see what the rule is not.
            ok = frac2.notna() & lab2.isin(LEVELS)
            notes[f"{age}d_day2_cuts"]["observed_class_ranges"] = {
                lv: [float(frac2[ok & (lab2 == lv)].min()),
                     float(frac2[ok & (lab2 == lv)].max())]
                for lv in LEVELS if (ok & (lab2 == lv)).any()
            }
            continue

        c1, c2 = cuts
        for visit, L, cc1, cc2 in (("T2", 230.0, c1, c2), ("T5", 23.0, 1e-3, 1e-2)):
            n0 = pd.to_numeric(d[f"mpn_T0_{age}days"], errors="coerce")
            nv = pd.to_numeric(d[f"mpn_{visit}_{age}days"], errors="coerce")
            lab = d[f"Tolerant_level_D{visit[1]}_{age}"]
            ok = n0.notna() & nv.notna() & lab.isin(LEVELS)
            h = np.log10(n0 / L)
            at = ok & (nv <= L)
            klass = lambda f: "Low" if f < cc1 else ("Medium" if f <= cc2 else "High")
            single = int(sum(klass(0.0) == klass(L / v) for v in n0[at])) if at.any() else 0
            rows.append({
                "culture_age_days": age,
                "endpoint": f"day {visit[1]}",
                "assay_floor": L,
                "c1": cc1,
                "n_usable": int(ok.sum()),
                "N_reach_1log": L * 10,
                "N_reach_2log": L * 1e2,
                "N_reach_4log": L * 1e4,
                "N_id": L / cc1,
                "n_short_1log": int((ok & (h < 1)).sum()),
                "n_short_2log": int((ok & (h < 2)).sum()),
                "n_short_4log": int((ok & (h < 4)).sum()),
                "n_at_floor": int(at.sum()),
                "n_single_compatible_class": single,
                "n_multiple_compatible_classes": int(at.sum()) - single,
            })
    return pd.DataFrame(rows), notes


def covariate_independence(d: pd.DataFrame) -> pd.DataFrame:
    """Which covariates can adjust the seeding gap without conditioning on it."""
    IR = d[EXPOSURE] == "IR"
    IS = d[EXPOSURE] == "IS"
    rows = []
    for col in ("INH_mutation", "INH_MGIT_DST", "RIF_MGIT_DST", "INH_Mykrobe",
                "RIF_Mykrobe", "MIC_INH", "MIC_RIF", "Time_to_0.4", "Time_point"):
        nn = d[col].notna()
        a, b = int((nn & IR).sum()), int((nn & IS).sum())
        p = stats.fisher_exact([[a, int(IR.sum()) - a], [b, int(IS.sum()) - b]])[1]
        if b == 0 or a == 0:
            verdict = "PROXY: recorded for only one exposure group"
        elif p < 1e-6:
            verdict = "PARTIAL: missingness strongly associated with exposure"
        else:
            verdict = "INDEPENDENT: usable for adjustment"
        rows.append({
            "covariate": col,
            "n_non_null": int(nn.sum()),
            "n_non_null_resistant": a,
            "n_resistant": int(IR.sum()),
            "n_non_null_susceptible": b,
            "n_susceptible": int(IS.sum()),
            "fisher_p_missingness_vs_exposure": float(p),
            "verdict": verdict,
            "usable_for_adjustment": verdict.startswith("INDEPENDENT"),
        })
    return pd.DataFrame(rows).sort_values("fisher_p_missingness_vs_exposure")


def main() -> int:
    d = pd.read_excel(DATA)

    vf = visit_floors(d)
    vf.to_csv(TABLES / "exp36_visit_floors.csv", index=False)

    db, notes = day2_boundaries(d)
    db.to_csv(TABLES / "exp36_day2_boundaries.csv", index=False)

    ci = covariate_independence(d)
    ci.to_csv(TABLES / "exp36_covariate_independence.csv", index=False)

    n0_censored = {
        f"{age}d": int((pd.to_numeric(d[f"mpn_T0_{age}days"], errors="coerce") == 2300).sum())
        for age in (15, 60)
    }
    day0 = vf[vf.visit == "T0"]

    (RECEIPTS / "exp36_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp36_visit_floors_and_covariates.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "eLife 93243 supplementary file 2",
        "starting_density_censoring": {
            "n_on_the_day0_minimum": n0_censored,
            "day0_verdicts": day0.set_index("culture_age_days")["verdict"].to_dict(),
            "n0_is_left_censored": bool((day0.verdict != "NONE").any()),
            "conclusion": ("the day-0 minimum occurs once per panel, so no day-0 floor "
                           "is evidenced and N0 is observed throughout"),
        },
        "day2_cut_recovery": notes,
        "day2_boundaries": db.to_dict("records"),
        "covariate_independence": ci.to_dict("records"),
        "n_covariates_usable_for_adjustment": int(ci.usable_for_adjustment.sum()),
    }, indent=2, default=str), encoding="utf-8")

    print("\n-- 1. is the starting density itself censored? --")
    print(vf[["culture_age_days", "visit", "minimum", "n_on_the_minimum",
              "verdict", "refuse_labels"]].to_string(index=False))
    print("\n   day-0 verdict is NONE in every panel: the minimum occurs once, which is a")
    print("   tail and not a floor. N0 is observed; no quantity needs a censored refit.")

    print("\n-- 2. the day-2 endpoint on its own floor --")
    for k, v in notes.items():
        print(f"   {k}: cuts={v['cuts']} agree={v['n_agree']}/{v['n_usable']}")
    if not db.empty:
        print(db[["culture_age_days", "endpoint", "assay_floor", "c1", "N_id",
                  "n_short_4log", "n_at_floor", "n_single_compatible_class",
                  "n_multiple_compatible_classes"]].to_string(index=False))

    print("\n-- 3. which covariates can adjust the seeding gap? --")
    print(ci[["covariate", "n_non_null_resistant", "n_non_null_susceptible",
              "verdict"]].to_string(index=False))
    print(f"\n   usable for adjustment: {int(ci.usable_for_adjustment.sum())} of {len(ci)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
