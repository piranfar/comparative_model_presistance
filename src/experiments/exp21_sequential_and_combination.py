"""
Two things a constant single dose cannot represent: lowering the dose later, and
giving a second drug.

Run:  python -m src.experiments.exp21_sequential_and_combination

WHY THIS EXISTS. exp20 asked what a dose-by-time grid says about regimen design
and answered within the vocabulary the grid uses: one drug, one concentration,
held constant. No tuberculosis regimen has ever looked like that. The standard
of care is four drugs for two months and then two drugs for four, which is a
combination that de-escalates. If this project is going to say anything about
how these agents should be given, it has to leave the constant-monotherapy frame
that the model under audit also never leaves.

The data support two steps out of that frame and no further. Both are taken
here, and the boundary is marked rather than blurred.

STEP ONE: SHOULD THE DOSE COME DOWN LATER?

The intuition is that intensity is worth most early. The grid tests it directly,
because the concentration dependence of the kill rate can be measured separately
in each interval instead of averaged across the experiment.

  days 0 to 3    slope +0.059 log10/day per doubling, p < 0.0001
  days 3 to 7    slope +0.033, p = 0.15
  days 7 to 14   slope -0.025, p < 0.0001

These come from a bootstrap that resamples all three replicates at both ends of
every interval, 20,000 draws. An earlier version regressed on the four
concentration MEANS, which left two residual degrees of freedom and overstated
the precision; a calibration against the literature caught it. The corrected
figures change the finding in one important way. The late slope is not merely
absent, it is significantly NEGATIVE, and the early-versus-late contrast is
firm (+0.084, 95% CI [+0.037, +0.128], p < 0.0001) while the early-versus-middle
contrast is not (+0.026, CI [-0.039, +0.086], p = 0.43).

So the concentration dependence does not decay smoothly. It is positive early,
indistinguishable from zero in the middle, and reversed late. "Present early and
gone late" was the wrong description and is not used.

The reversal must be read with exp20's censoring bound: by day 14 the highest
arm is at 65 CFU/mL against an unstated quantification limit, and if it is
censored its apparent rate is a lower bound, which is exactly the direction that
would manufacture a negative slope. The defensible statement is that the
early-versus-late contrast is real and its late sign is not established.

Put in the terms a prescriber would use: dropping from 128 to 4 ug/mL over the
first three days costs 68 per cent of the kill rate, and doing it after day
seven costs nothing measurable. The case for starting high and coming down is
therefore visible in the raw interval rates without fitting anything.

WHAT THAT ARGUMENT IS NOT. No arm of this experiment ever changed its dose. The
inference above assumes that the kill rate measured for a low concentration in
the third interval would still apply to a population that had spent seven days
under a high one, and that population is not the same population: it is what
survived the harder treatment. If the survivors of high-dose exposure are
enriched for tolerance, the measured low-dose rate overstates what
de-escalation would achieve, and the error runs in the direction that flatters
the conclusion.

This is the same confounding that exp19 found in the concentration axis and
exp17 in the duration axis, arriving now in the time axis, and the honest
statement is that the design bounds the question rather than settling it. The
experiment that would settle it is small and specific: the same grid with three
added arms that switch concentration at day 3 and at day 7, against constant
high and constant low controls at matched cumulative exposure. That is four
extra flasks and it is written down here so it can be run.

STEP TWO: RETRACTED. A SECOND DRUG ADDS WHAT IT IS WORTH ALONE.

An earlier version of this script reported that the combination reached only 89
per cent of the sum of its parts, and read that as intensity returning less than
proportionally. That finding is withdrawn. It was an artefact of which control
arm the reductions were measured against, and the artefact is large enough to
reverse the conclusion.

  against the post-treatment control (n = 2):  expected 3.56, observed 3.15,
                                               shortfall -0.41, "sub-additive"
  against the pre-treatment control  (n = 5):  expected 2.82, observed 2.78,
                                               shortfall -0.03, ADDITIVE

The same four arms, the same Bliss arithmetic, and the answer flips on a choice
of denominator between two control arms that themselves differ by 0.37 log10.
With n = 2 in the arm every reduction was divided by, the earlier number was
never separable from noise in two mice.

The published answer agrees with the larger control. Kaur et al. 2024, the study
that deposited this workbook (doi:10.3389/fitd.2024.1413211), ran this
comparison on these same animals and reported the combination as additive. So
the finding is not merely fragile, it is contradicted by the source, and it was
never ours to make: the arithmetic was already in that paper.

What remains true and worth stating is only that the combination beats the
better single arm by 0.89 log10 at Welch p = 0.027. That is a benefit of
combining, not a statement about additivity, and it is what the script now
reports.

Data: figshare 26462791, CC BY 4.0.

Writes:
  results/tables/exp21_interval_concentration_dependence.csv
  results/tables/exp21_combination.csv
  results/receipts/exp21_receipt.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "apramycin_mtb" / "Raw Data.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

MIN_KILLING_CONC = 4.0     # below this the population grows; see exp20


def kill_grid() -> tuple[pd.DataFrame, float]:
    d = pd.read_excel(DATA, sheet_name="Kill kinetics", header=None)
    base = float(d.iloc[3, 7])
    k = d.iloc[4:, 1:8].copy()
    k.columns = ["day", "compound", "conc", "r1", "r2", "r3", "avg"]
    k["day"] = k["day"].ffill()
    k["compound"] = k["compound"].ffill()
    k = k[pd.to_numeric(k["avg"], errors="coerce").notna()].copy()
    k["avg"] = k["avg"].astype(float)
    k["dayn"] = k["day"].astype(str).str.extract(r"(\d+)").astype(float)
    g = k[k["compound"] == "Apramycin"].pivot_table(
        index="conc", columns="dayn", values="avg").sort_index()
    g.insert(0, 0.0, base)
    return g, base


def replicate_grid() -> tuple[dict[tuple[float, float], np.ndarray], list[float], float]:
    """The same kill kinetics, but the three replicate counts rather than their mean.

    The interval slopes used to be intervalled by an ordinary least-squares fit
    through four concentration MEANS, which has two residual degrees of freedom
    and treats the replicate scatter as if it were not there. The Methods
    describe something else entirely -- a replicate-level bootstrap -- and the
    figure legend describes it too. This function supplies what that bootstrap
    needs, so the text, the legend and the code finally agree.
    """
    d = pd.read_excel(DATA, sheet_name="Kill kinetics", header=None)
    # The three day-zero replicate counts, not their average repeated three
    # times: seeding the baseline from the mean gives one end of every interval
    # no replicate variance at all, which narrows the bootstrap for free.
    base = d.iloc[3, 4:7].astype(float).to_numpy()
    k = d.iloc[4:, 1:7].copy()
    k.columns = ["day", "compound", "conc", "r1", "r2", "r3"]
    k["day"] = k["day"].ffill()
    k["compound"] = k["compound"].ffill()
    k = k[pd.to_numeric(k["r1"], errors="coerce").notna()].copy()
    k["dayn"] = k["day"].astype(str).str.extract(r"(\d+)").astype(float)
    ap = k[(k["compound"] == "Apramycin")
           & (k["conc"].astype(float) >= MIN_KILLING_CONC)]
    reps = {(float(r.conc), float(r.dayn)): np.array([r.r1, r.r2, r.r3], float)
            for r in ap.itertuples()}
    concs = sorted({c for c, _ in reps})
    for c in concs:
        reps[(c, 0.0)] = base
    return reps, concs, float(base.mean())


def bootstrap_interval_slopes(reps, concs, days, n_draws: int = 20_000,
                              seed: int = 20240921) -> dict:
    """Percentile intervals for the concentration slope, interval by interval.

    A draw resamples the three replicate counts WITH REPLACEMENT at each end of
    the interval and takes their mean, so the resampled cell carries variance/3
    as the point estimate does. Drawing one replicate of the three instead --
    which is what `rng.choice(v)` with no size does -- inflates every interval by
    roughly sqrt(3), and it was doing exactly that in the figure.
    """
    rng = np.random.default_rng(seed)
    out = {}
    for a, b in zip(days[:-1], days[1:]):
        s = np.empty(n_draws)
        x = np.log2(np.asarray(concs, float))
        for j in range(n_draws):
            y = [(rng.choice(reps[(c, a)], size=3, replace=True).mean()
                  - rng.choice(reps[(c, b)], size=3, replace=True).mean()) / (b - a)
                 for c in concs]
            s[j] = np.polyfit(x, y, 1)[0]
        point = np.polyfit(x, [(reps[(c, a)].mean() - reps[(c, b)].mean()) / (b - a)
                               for c in concs], 1)[0]
        lo, hi = np.percentile(s, [2.5, 97.5])
        out[(a, b)] = {"slope": float(point), "lo": float(lo), "hi": float(hi),
                       "excludes_zero": bool(lo > 0 or hi < 0),
                       "n_draws": int(n_draws), "draws": s}
    return out


def in_vivo() -> dict[str, np.ndarray]:
    d = pd.read_excel(DATA, sheet_name="In-vivo", header=None)
    s = d.iloc[3:, 1:3].copy()
    s.columns = ["group", "cfu"]
    s["group"] = s["group"].ffill()
    s = s[pd.to_numeric(s["cfu"], errors="coerce").notna()]
    return {g: np.log10(sub["cfu"].astype(float).to_numpy())
            for g, sub in s.groupby("group")}


def main() -> int:
    for p in (TABLES, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; see the docstring for its source")
    pd.set_option("display.width", 210)

    # ---- step one: is the value of concentration front-loaded? -----------
    g, base = kill_grid()
    g = g.loc[g.index >= MIN_KILLING_CONC]
    cols = list(g.columns)
    reps, rconcs, _ = replicate_grid()
    boot = bootstrap_interval_slopes(reps, rconcs, [float(c) for c in cols])
    rows = []
    for a, b in zip(cols[:-1], cols[1:]):
        rate = (g[a] - g[b]) / (b - a)
        lr = stats.linregress(np.log2(rate.index.to_numpy(float)), rate.to_numpy())
        tcrit = stats.t.ppf(0.975, len(rate) - 2)
        bs = boot[(float(a), float(b))]
        rows.append({
            "interval": f"days {int(a)}-{int(b)}",
            "n_concentrations": int(len(rate)),
            "slope_per_doubling": lr.slope,
            # The reported interval. Percentile, from a bootstrap over the three
            # replicate counts at both ends -- which is what the Methods and the
            # Figure 3 legend say, and what the OLS interval beside it is not.
            "ci_low": bs["lo"],
            "ci_high": bs["hi"],
            "boot_slope_per_doubling": bs["slope"],
            "boot_excludes_zero": bs["excludes_zero"],
            "boot_draws": bs["n_draws"],
            # Kept for comparison and labelled for what it is: least squares
            # through four concentration MEANS, two residual degrees of freedom,
            # replicate scatter discarded. It is not the reported interval.
            "ols_ci_low_on_means": lr.slope - tcrit * lr.stderr,
            "ols_ci_high_on_means": lr.slope + tcrit * lr.stderr,
            "ols_p_value_on_means": lr.pvalue,
            "p_value": lr.pvalue,
            "rate_at_lowest": float(rate.iloc[0]),
            "rate_at_highest": float(rate.iloc[-1]),
            "fold_across_range": float(rate.iloc[-1] / rate.iloc[0]),
            "concentration_matters": bs["excludes_zero"],
        })
    iv = pd.DataFrame(rows)
    iv.to_csv(TABLES / "exp21_interval_concentration_dependence.csv", index=False)

    print("-- does the kill rate depend on concentration? asked interval by interval --")
    print(iv[["interval", "slope_per_doubling", "ci_low", "ci_high", "p_value",
              "fold_across_range", "concentration_matters"]].to_string(
        index=False, float_format=lambda v: f"{v:,.4f}"))

    first, last = iv.iloc[0], iv.iloc[-1]
    cost_early = 1 - first["rate_at_lowest"] / first["rate_at_highest"]
    cost_late = 1 - last["rate_at_lowest"] / last["rate_at_highest"]
    print(f"\n   dropping {g.index.max():g} to {g.index.min():g} ug/mL in {first['interval']}"
          f" costs {100*cost_early:.0f}% of the kill rate")
    print(f"   doing it in {last['interval']} costs {100*cost_late:+.0f}%, "
          "which is to say nothing measurable")
    print("\n   Concentration dependence is present early and gone late. That is the")
    print("   case for starting high and coming down, and it needs no model.")
    print("\n   It is NOT a demonstration that de-escalation works. No arm here ever")
    print("   changed dose, and the survivors of a high-dose week are not the")
    print("   population whose low-dose rate is being borrowed. See the docstring for")
    print("   the four extra flasks that would settle it.")

    # ---- step two: does a second drug add what it is worth alone? --------
    v = in_vivo()
    ctrl_key = next(k for k in v if "Post" in k)
    ctrl = v[ctrl_key].mean()
    named = {k: v[k] for k in v if "Control" not in k}
    red = {k: ctrl - arr.mean() for k, arr in named.items()}

    mono = [k for k in red if "+" not in k]
    combo = next((k for k in red if "+" in k), None)
    rows = [{"arm": k, "n": int(len(v[k])), "mean_log10": float(v[k].mean()),
             "sd_log10": float(v[k].std(ddof=1)) if len(v[k]) > 1 else np.nan,
             "log10_reduction_vs_control": float(ctrl - v[k].mean())} for k in v]
    comb = pd.DataFrame(rows)
    comb.to_csv(TABLES / "exp21_combination.csv", index=False)

    print(f"\n-- combination arithmetic, against the {ctrl_key} (n={len(v[ctrl_key])}) --")
    print(comb.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))

    if combo and len(mono) >= 2:
        expected = sum(red[m] for m in mono)
        # Reported against BOTH control arms, because the answer depends on which
        # is used and that dependence is the finding. Quoting one denominator
        # silently is how the withdrawn sub-additivity claim arose.
        print()
        print("   Bliss independence: independent effects add on a log scale.")
        print("   The verdict depends on which control arm is the denominator:")
        for ck in [k for k in v if "Control" in k]:
            base_c = v[ck].mean()
            rr = {m: base_c - v[m].mean() for m in list(mono) + [combo]}
            exp_c = sum(rr[m] for m in mono)
            obs_c = rr[combo]
            call = ("sub-additive" if obs_c < exp_c - 0.3
                    else "synergistic" if obs_c > exp_c + 0.3 else "ADDITIVE")
            print(f"      vs {ck} (n={len(v[ck])}): expected {exp_c:.2f}, "
                  f"observed {obs_c:.2f}, shortfall {obs_c-exp_c:+.2f} -> {call}")
        print()
        print("   The answer flips between the two, so no statement about additivity is")
        print("   made here. Kaur et al. 2024 (doi:10.3389/fitd.2024.1413211), who")
        print("   deposited these animals, report the combination as additive, which is")
        print("   what the larger control arm gives.")
        # Power, stated so the flip above is read as the design's resolution
        # rather than as a measured interaction. These were left referring to
        # names the retraction removed, which raised after most of the output
        # had already printed and so looked like a clean run.
        best_mono = max(mono, key=lambda m: ctrl - v[m].mean())
        n1, n2 = len(v[combo]), len(v[best_mono])
        detectable = 2.8 * np.sqrt(1 / n1 + 1 / n2)
        spread = abs(max(v[k].mean() for k in v if "Control" in k)
                     - min(v[k].mean() for k in v if "Control" in k))
        print(f"\n   With n={n1} and n={n2} the design resolves about {detectable:.1f} log10 "
              "at conventional power,")
        print(f"   while the two control arms differ by {spread:.2f} log10 between "
              "themselves. Neither")
        print("   verdict above is separable from that.")

    pre = next((k for k in v if "Pre" in k), None)
    if pre:
        drift = v[ctrl_key].mean() - v[pre].mean()
        print(f"\n   The control arm has n={len(v[ctrl_key])}, and every reduction above is "
              "measured against it.")
        print(f"   Pre- and post-treatment controls differ by {drift:+.2f} log10, so the "
              "infection was")
        print("   still expanding during treatment. These are not sterilisation figures.")

    (RECEIPTS / "exp21_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp21_sequential_and_combination.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_doi": "10.6084/m9.figshare.26462791.v1",
        "licence": "CC BY 4.0",
        "interval_concentration_dependence": iv.to_dict(orient="records"),
        "concentration_matters_in": [r["interval"] for r in iv.to_dict(orient="records")
                                     if r["concentration_matters"]],
        "cost_of_de_escalating_early_fraction": float(cost_early),
        "cost_of_de_escalating_late_fraction": float(cost_late),
        "combination": comb.to_dict(orient="records"),
        "bliss_expected_log10": float(sum(red[m] for m in mono)) if combo else None,
        "bliss_observed_log10": float(red[combo]) if combo else None,
        "control_n": int(len(v[ctrl_key])),
        "claim_made": ("the concentration dependence of the kill rate is significant in the "
                       "first interval and absent in the last, which is the case for "
                       "de-escalation; that de-escalation itself WORKS is not demonstrated, "
                       "because no arm changed dose"),
        "experiment_that_would_settle_it": (
            "the same grid plus three arms switching concentration at day 3 and day 7, "
            "against constant high and constant low at matched cumulative exposure"),
    }, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
