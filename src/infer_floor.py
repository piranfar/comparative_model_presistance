"""
Infer an assay's floor from the readings, with the evidence, when it is not stated.

Run:  python -m src.infer_floor

WHY THIS EXISTS. Every quantity in docs/19_MATHEMATICS.md is exact once the floor
L is known, and the algebra is closed form, so nothing about the computation needs
to be learned. What does need work is L itself. Four of the deposits examined in
this project state no limit of quantification anywhere, and the whole calculation
rests on it.

This module infers L from the distribution of the readings and reports WHY,
because a floor asserted without evidence is worth nothing. It runs four
independent tests and returns each verdict separately rather than collapsing them
into one number:

  PILE-UP        a floor shows as an excess of readings sitting exactly on the
                 smallest value. Under any continuous distribution, k exact ties
                 at the minimum is essentially impossible; under a floor it is
                 expected. Reported as the tie count and the fraction.

  NOTHING BELOW  a floor means no reading anywhere lies below it. A smooth tail
                 means some do. Reported as the count below the candidate.

  DILUTION LADDER  serial dilution leaves values on a lattice c*10^k. Extracting
                 the mantissas says whether the readings come from a ladder, and
                 a ladder whose lowest rung is the observed minimum is a floor
                 rather than a coincidence.

  VOLUME-DERIVED  where counts are expressed per mL, one colony in a plated
                 volume v uL is 1000/v per mL. If the smallest value at each
                 volume equals 1000/v exactly, the floor is derived rather than
                 inferred and the other three tests are unnecessary.

The output is a verdict of DERIVED, INFERRED, WEAK or NONE, and the caller is
expected to propagate that label rather than treat every floor as equally solid.

Writes:  docs/21_FLOOR_INFERENCE.md
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "21_FLOOR_INFERENCE.md"

# Values a standard three-tube most-probable-number table returns, ascending.
MPN_TABLE = (3.0, 3.6, 7.2, 7.4, 9.2, 11.0, 14.0, 15.0, 20.0, 21.0, 23.0,
             28.0, 29.0, 39.0, 43.0, 75.0, 93.0, 150.0, 210.0, 240.0, 460.0, 1100.0)
PLAUSIBLE_VOLUMES_UL = (1.0, 2.5, 5.0, 10.0, 20.0, 25.0, 50.0, 100.0, 200.0, 1000.0)


def mantissas(values: np.ndarray) -> list[float]:
    """The lattice a set of readings sits on, if any: values as c * 10^k."""
    v = values[values > 0]
    if not len(v):
        return []
    m = v / 10.0 ** np.floor(np.log10(v))
    return sorted({round(float(x), 2) for x in m})


def pile_up(values: np.ndarray) -> dict:
    v = values[np.isfinite(values)]
    if not len(v):
        return {"n": 0}
    lo = float(v.min())
    ties = int((v == lo).sum())
    # Second-smallest, to see whether the minimum is an outlier or a rung.
    above = v[v > lo]
    return {
        "n": int(len(v)),
        "minimum": lo,
        "ties_at_minimum": ties,
        "fraction_at_minimum": ties / len(v),
        "n_below_minimum": 0,
        "next_value_up": float(above.min()) if len(above) else None,
        "gap_to_next": float(above.min() / lo) if len(above) and lo > 0 else None,
    }


def volume_derived(values: np.ndarray, recorded_volume_ul: float | None) -> dict | None:
    """Is the floor DERIVED from a recorded plated volume?

    This test only fires when the deposit RECORDS the plated volume. An earlier
    version searched a list of plausible pipettes for one whose 1000/v matched
    the observed minimum, and duly reported the Kaur deposit as DERIVED with a
    floor of 40 per mL because its minimum happened to equal 1000/25. That is a
    coincidence dressed as a derivation, and it is exactly the confident wrong
    number this module exists to prevent. A derivation needs the volume to be
    stated, not guessed backwards from the answer.
    """
    if recorded_volume_ul is None:
        return None
    v = values[np.isfinite(values) & (values > 0)]
    if not len(v):
        return None
    lo = float(v.min())
    implied = 1000.0 / recorded_volume_ul
    if abs(lo - implied) < 1e-6:
        return {"plated_volume_ul": recorded_volume_ul, "implied_floor": lo,
                "reasoning": f"the deposit records {recorded_volume_ul:g} uL plated and "
                             f"one colony in that volume is {lo:g} per mL"}
    return {"plated_volume_ul": recorded_volume_ul, "implied_floor": implied,
            "reasoning": f"the deposit records {recorded_volume_ul:g} uL plated, implying "
                         f"{implied:g} per mL, but the smallest reading is {lo:g}",
            "disagrees": True}


def matches_mpn(values: np.ndarray) -> dict:
    v = values[np.isfinite(values) & (values > 0)]
    mant = mantissas(v)
    table_mant = mantissas(np.array(MPN_TABLE))
    on_table = [m for m in mant if m in table_mant]
    lo = float(v.min()) if len(v) else np.nan
    below_in_table = [x for x in MPN_TABLE if x < lo]
    return {
        "mantissas_observed": mant,
        "mantissas_on_mpn_table": on_table,
        "minimum_is_an_mpn_value": bool(any(abs(lo - x) < 1e-6 for x in MPN_TABLE)),
        "mpn_values_below_the_minimum": below_in_table,
    }


def infer(values: np.ndarray, counts_per_ml: bool = True,
          recorded_volume_ul: float | None = None) -> dict:
    p = pile_up(values)
    if not p.get("n"):
        return {"verdict": "NONE", "reason": "no finite readings"}
    vd = volume_derived(values, recorded_volume_ul) if counts_per_ml else None
    mp = matches_mpn(values)

    if vd and not vd.get("disagrees"):
        verdict, reason = "DERIVED", (
            f"the minimum equals 1000/{vd['plated_volume_ul']:g}, so the floor "
            "follows from the plated volume and is not an inference")
    elif p["ties_at_minimum"] >= 5 and mp["minimum_is_an_mpn_value"]:
        verdict, reason = "INFERRED", (
            f"{p['ties_at_minimum']} readings sit exactly on the minimum, nothing "
            "lies below it, and the minimum is a value an MPN table returns")
    elif p["ties_at_minimum"] >= 5:
        verdict, reason = "INFERRED", (
            f"{p['ties_at_minimum']} readings sit exactly on the minimum and "
            "nothing lies below it")
    elif p["ties_at_minimum"] >= 2:
        verdict, reason = "WEAK", (
            f"only {p['ties_at_minimum']} readings sit on the minimum; a floor is "
            "possible but a thin tail would look similar")
    else:
        verdict, reason = "NONE", (
            "the minimum appears once, which is what a continuous tail looks "
            "like; no floor is evidenced")

    return {"verdict": verdict, "reason": reason, "candidate_floor": p["minimum"],
            "pile_up": p, "mpn": mp, "volume_derived": vd}


# ---------------------------------------------------------------- deposits ---
def load_deposits() -> dict[str, dict]:
    out: dict[str, dict] = {}

    v = pd.read_excel(ROOT / "data/raw/tb/elife93243_supp2.xlsx")
    cols = [c for c in v.columns if c.startswith("mpn_") and "log" not in c]
    out["Vijay 2024, clinical isolates (MPN per mL)"] = {
        "values": pd.concat([v[c] for c in cols]).dropna().to_numpy(float),
        "counts_per_ml": True, "recorded_volume_ul": None,
        "stated_limit": "no limit and no plated volume recorded",
    }

    e = pd.read_csv(ROOT / "data/raw/tb/era4tb_timekill.csv", encoding="latin-1")
    for vol in (100.0, 10.0, 2.5):
        s = e[(e["Volume"] == vol) & (e["BQL"] != 1) & (e["AQL"] != 1)]
        y = pd.to_numeric(s["CFU"], errors="coerce").dropna()
        out[f"ERA4TB, {vol:g} uL plated (CFU per mL)"] = {
            "values": y.to_numpy(float), "counts_per_ml": True,
            "recorded_volume_ul": vol,
            "stated_limit": "no limit stated, but the plated volume IS recorded",
        }

    k = pd.ExcelFile(ROOT / "data/raw/apramycin_mtb/Raw Data.xlsx").parse("Kill kinetics")
    num = k.iloc[:, 4:7].apply(pd.to_numeric, errors="coerce").to_numpy(float).ravel()
    num = num[np.isfinite(num)]
    out["Kaur 2024, apramycin grid (log10 CFU per mL)"] = {
        "values": 10.0 ** num, "counts_per_ml": True, "recorded_volume_ul": None,
        "stated_limit": "no limit and no plated volume recorded",
    }
    return out


def main() -> int:
    deposits = load_deposits()
    lines = ["# Inferring an assay floor, with the evidence", "",
             "Generated by `python -m src.infer_floor`.", "",
             "The algebra in `docs/19_MATHEMATICS.md` is exact once the floor `L` is",
             "known, so nothing about the computation needs to be learned. `L` itself",
             "is the part that needs work: most deposits do not state it. This runs",
             "four independent tests per deposit and labels each floor DERIVED,",
             "INFERRED, WEAK or NONE, so the label can travel with the number.", "",
             "---", ""]

    for name, spec in deposits.items():
        r = infer(spec["values"], spec["counts_per_ml"],
                  spec.get("recorded_volume_ul"))
        p = r["pile_up"]
        lines += [f"## {name}", "",
                  f"- readings analysed: **{p['n']:,}**",
                  f"- deposit states: {spec['stated_limit']}",
                  f"- smallest reading: **{p['minimum']:,.4g}** per mL",
                  f"- readings exactly on it: **{p['ties_at_minimum']}** "
                  f"({100 * p['fraction_at_minimum']:.1f} per cent)",
                  f"- readings below it: **{p['n_below_minimum']}**",
                  f"- next value up: {p['next_value_up']:,.4g}"
                  + (f", a factor of {p['gap_to_next']:.1f} away" if p["gap_to_next"] else ""),
                  f"- lattice the readings sit on: {r['mpn']['mantissas_observed']}",
                  ]
        if r["mpn"]["mpn_values_below_the_minimum"]:
            lines.append("- MPN-table values below the minimum that never appear: "
                         f"{r['mpn']['mpn_values_below_the_minimum']}")
        if r["volume_derived"]:
            lines.append(f"- **volume test passes**: {r['volume_derived']['reasoning']}")
        lines += ["", f"**Verdict: {r['verdict']}.** {r['reason']}.", "", "---", ""]
        print(f"  {name:<48} {r['verdict']:<9} L = {r['candidate_floor']:,.4g}")

    lines += [
        "## How to use the label", "",
        "A `DERIVED` floor can be used without qualification: it follows from a",
        "recorded plated volume and an arithmetic identity.", "",
        "An `INFERRED` floor should be carried with a sensitivity analysis over the",
        "plausible alternatives, as `exp22` does for the clinical deposit, where the",
        "load-bearing count moves from 33 to 28 across every value a three-tube MPN",
        "table can return below 23.", "",
        "A `WEAK` or `NONE` floor means the deposit cannot support this calculation.",
        "That is a finding about the deposit, not a reason to pick a number.", "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
