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

  days 0 to 3    slope +0.059 log10/day per doubling, 95% CI [+0.030, +0.088],
                 p = 0.013. Concentration matters, and the interval is the only
                 one where the confidence interval excludes zero.
  days 3 to 7    slope +0.033, CI [-0.052, +0.118], p = 0.24.
  days 7 to 14   slope -0.025, CI [-0.060, +0.010], p = 0.09.

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

STEP TWO: DOES A SECOND DRUG ADD WHAT IT IS WORTH ALONE?

The same deposit carries a mouse experiment with apramycin alone, the standard
four-drug regimen alone, and both together, which is the arithmetic of
combination therapy in one sheet. On a log scale independent effects add, which
is Bliss independence, so the test is whether the combination reaches the sum.

  apramycin alone       1.30 log10 reduction
  HREZ alone            2.26
  sum, if independent   3.56
  observed together     3.15

The combination is worth having: it beats HREZ alone by 0.89 log10 (Welch
p = 0.027). But it recovers less than the sum of its parts by 0.41 log10, so the
second agent contributes about two thirds of what it achieves on its own. That
is the same shape as the finding above. Intensity, whether bought with
concentration or with a second drug, returns less than proportionally, and the
excess is spent early.

THE ARITHMETIC IS WEAKER THAN IT LOOKS, and the script says so. The control arm
has n = 2. Every reduction quoted above is measured against those two mice, and
their spread is 0.32 log10. The pre-treatment and post-treatment controls differ
by +0.37 log10, so the infection was still expanding while the drugs were given,
which means these are not sterilisation figures. With four and five animals per
arm the design could resolve about 1.9 log10 at conventional power, and the
sub-additivity being discussed is 0.41. It is reported as a direction, not as an
established interaction.

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
    rows = []
    for a, b in zip(cols[:-1], cols[1:]):
        rate = (g[a] - g[b]) / (b - a)
        lr = stats.linregress(np.log2(rate.index.to_numpy(float)), rate.to_numpy())
        tcrit = stats.t.ppf(0.975, len(rate) - 2)
        rows.append({
            "interval": f"days {int(a)}-{int(b)}",
            "n_concentrations": int(len(rate)),
            "slope_per_doubling": lr.slope,
            "ci_low": lr.slope - tcrit * lr.stderr,
            "ci_high": lr.slope + tcrit * lr.stderr,
            "p_value": lr.pvalue,
            "rate_at_lowest": float(rate.iloc[0]),
            "rate_at_highest": float(rate.iloc[-1]),
            "fold_across_range": float(rate.iloc[-1] / rate.iloc[0]),
            "concentration_matters": bool(lr.pvalue < 0.05),
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
        observed = red[combo]
        print(f"\n   Bliss independence: independent effects add on a log scale.")
        for m in mono:
            print(f"      {m:<20}{red[m]:>6.2f}")
        print(f"      {'sum if independent':<20}{expected:>6.2f}")
        print(f"      {'observed together':<20}{observed:>6.2f}")
        print(f"      {'shortfall':<20}{observed-expected:>+6.2f} log10")

        best_mono = max(mono, key=lambda m: red[m])
        t = stats.ttest_ind(v[combo], v[best_mono], equal_var=False)
        gain = red[combo] - red[best_mono]
        n1, n2 = len(v[combo]), len(v[best_mono])
        detectable = 2.8 * np.sqrt(1 / n1 + 1 / n2)
        print(f"\n   against the better single arm ({best_mono}): {gain:+.2f} log10, "
              f"Welch p = {t.pvalue:.3f}")
        # Two ways of saying the same shortfall, because both get quoted and
        # they have different denominators. The pair reaches 89 per cent of the
        # sum of the two solo effects; equivalently, the agent that is added
        # delivers 68 per cent of what it delivers by itself.
        added = next(m for m in mono if m != best_mono)
        print(f"   the combination is worth having, but recovers "
              f"{100*observed/expected:.0f}% of the sum of its parts;")
        print(f"   equivalently, adding {added} to {best_mono} buys {gain:.2f} log10 "
              f"where {added} alone")
        print(f"   buys {red[added]:.2f}, so it delivers {100*gain/red[added]:.0f}% of its "
              "solo effect inside the combination.")
        print(f"\n   With n={n1} and n={n2} the design resolves about {detectable:.1f} log10 "
              f"at conventional power,")
        print(f"   and the sub-additivity in question is {abs(observed-expected):.2f}. It is a "
              "direction, not an established interaction.")

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
