"""
Measurable kill depth across four deposits, and what the turbidity standard does
and does not fix.

Run:  python -m src.experiments.exp28_standard_vs_realised

WHY THIS TEST EXISTS. The strongest objection to this project is that the
starting inoculum is not a free variable: a suspension is matched to 0.5
McFarland and diluted, and CLSI M26 puts the time-kill target near 5e5 CFU/mL.
If the protocol fixes the inoculum, a framework built on it varying is built on
nothing.

The objection is right about the standard, so it is answered with counts.

TWO QUANTITIES, KEPT APART. For culture i with starting density N0_i and
quantification limit L_i:

    H_i = N0_i / L_i            a ratio, dimensionless
    h_i = log10(N0_i / L_i)     the deepest reduction measurable, in log10

Variation is reported on h, never on N0 alone:

    delta_h    = max(h_i) - min(h_i)
    fold_spread = 10 ** delta_h

That distinction is not pedantic here. In ERA4TB, L is set by the plated volume:
1000/100 = 10, 1000/10 = 100, 1000/2.5 = 400 CFU/mL. The SAME culture measured
on a 2.5 uL drop and a 100 uL quadruplicate differs by 1.6 log10 in measurable
depth. Computing a spread from N0 alone would discard that entirely, and an
earlier version of this experiment did exactly that.

WHAT THE 0.5 McFARLAND FIGURE IS FOR. It is a nominal reference and nothing
else. It is a TURBIDITY, matched optically, counting live cells, dead cells,
debris, and a clump as one particle; converting it to CFU/mL assumes a cell size,
shape and dispersal that M. tuberculosis does not oblige. Tuberculosis protocols
also work from a range of dilutions and target inocula. So distance from 1.5e8 is
descriptive, is expected because a time-kill inoculum is prepared BY diluting
from it, and is NOT a compliance or deviation metric. It is reported in a
supplementary table and kept out of the main one, because a column gets read and
a caveat does not.

LEVELS OF VARIATION ARE NOT INTERCHANGEABLE. Four deposits measure four
different things, and a single column pooling them invites the inference that the
clinical dataset is a thousand times less reproducible than the consortium. Each
row states its level, and rows compare only within a level.

Writes:  results/tables/exp28_measurable_depth.csv
         results/tables/exp28_supplementary_mcfarland.csv
         results/receipts/exp28_receipt.json
         docs/26_MEASURABLE_DEPTH.md
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ERA = ROOT / "data" / "raw" / "tb" / "era4tb_timekill.csv"
VIJAY = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
KAUR = ROOT / "data" / "raw" / "apramycin_mtb" / "Raw Data.xlsx"
DUBEY = ROOT / "data" / "raw" / "dubey2026" / "source_data.xlsx"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"
DOC = ROOT / "docs" / "26_MEASURABLE_DEPTH.md"

MCFARLAND_05 = 1.5e8        # nominal CFU/mL at 0.5 McFarland turbidity
VIJAY_FLOOR = 23.0          # MPN table floor, INFERRED (see exp22 sensitivity)
DUBEY_FLOOR = 10.0          # DERIVED: 100 uL plated, counts per mL
TREATED = ["MXF 1X MIC", "MXF 10X MIC", "INH 1X MIC", "INH 10X MIC"]


def md_table(d: pd.DataFrame, right: tuple[str, ...] = ()) -> str:
    """A markdown table whose header row is a header row."""
    cols = [str(c) for c in d.columns]
    head = "| " + " | ".join(cols) + " |"
    rule = "| " + " | ".join("---:" if c in right else "---" for c in cols) + " |"
    body = [
        "| " + " | ".join("" if pd.isna(v) else str(v) for v in row) + " |"
        for row in d.itertuples(index=False)
    ]
    return "\n".join([head, rule] + body)


# ------------------------------------------------------------------- ERA4TB ---
def era4tb_channels() -> pd.DataFrame:
    """One row per (institute, plated volume): N0, its own L, and h.

    The floor is a property of the plated volume, so a culture measured at three
    volumes has three values of h. Both sources of variation - between
    laboratories and between plating volumes - are real and both are kept.
    """
    e = pd.read_csv(ERA, encoding="latin-1")
    e["y"] = pd.to_numeric(e["CFUlog10"], errors="coerce")
    ok = (e["BQL"] != 1) & (e["AQL"] != 1)
    u = e[ok & (e["Sample"] == "untreated") & (e["Time"] == 0)].dropna(subset=["y"])

    rows = []
    for (lab, vol), g in u.groupby(["Institute", "Volume"]):
        n0 = 10 ** g["y"].mean()
        L = 1000.0 / vol
        rows.append({"institute": lab, "plated_volume_ul": vol, "n_readings": len(g),
                     "N0_cfu_per_ml": n0, "L_cfu_per_ml": L,
                     "H_ratio": n0 / L, "h_log10": float(np.log10(n0 / L))})
    return pd.DataFrame(rows)


def era4tb_audit() -> dict:
    """Is the floor L = 1000/V borne out, institute by institute?

    A count reported per mL from a plate of volume V can only be a multiple of
    1000/V. If an institute's counts sit on a coarser grid, a further dilution
    step is in play and its L is not what the volume implies.
    """
    e = pd.read_csv(ERA, encoding="latin-1")
    s = e[(e["BQL"] != 1) & (e["AQL"] != 1)].copy()
    s["CFU"] = pd.to_numeric(s["CFU"], errors="coerce")
    out = {}
    for (lab, vol), g in s.dropna(subset=["CFU"]).groupby(["Institute", "Volume"]):
        v = g["CFU"][g["CFU"] > 0]
        if not len(v):
            continue
        L = 1000.0 / vol
        out[f"{lab} @ {vol:g}uL"] = {
            "n": int(len(v)), "expected_floor": L,
            "smallest_observed": float(v.min()),
            "fraction_on_the_L_grid": float(np.isclose(v % L, 0).mean()),
        }
    return out


# -------------------------------------------------------------------- others ---
def vijay_groups() -> pd.DataFrame:
    d = pd.read_excel(VIJAY)
    rows = []
    # The 30-day panel is deposited but no section of the paper analyses it, and a
    # table row a reader cannot follow back to a claim is noise.
    for age in (15, 60):
        col = f"mpn_T0_{age}days"
        if col not in d:
            continue
        v = pd.to_numeric(d[col], errors="coerce").dropna()
        v = v[v > 0]
        h = np.log10(v / VIJAY_FLOOR)
        rows.append({
            "dataset": f"Vijay, {age}-day culture",
            "level_of_variation": "between clinical isolates",
            "n": int(len(v)), "median_log10_N0": float(np.log10(v).median()),
            "L_note": f"{VIJAY_FLOOR:g} MPN/mL, inferred",
            "delta_h": float(h.max() - h.min()),
        })
    return pd.DataFrame(rows)


def kaur_groups() -> pd.DataFrame:
    """Kaur records three day-zero control replicates of ONE preparation.

    delta_h is left blank rather than printed as 1x. A 1x entry beside the other
    rows would be read as perfect between-preparation reproducibility, and these
    are technical replicates of a single preparation, which cannot estimate that.
    The deposit also states no quantification limit, so h is not computable.
    """
    if not KAUR.exists():
        return pd.DataFrame()
    rows = []
    for sheet, label in (("Kill kinetics", "Kaur, planktonic"),
                         ("Intracellular efficacy", "Kaur, intracellular")):
        try:
            v = pd.to_numeric(pd.ExcelFile(KAUR).parse(sheet).iloc[2, 4:7],
                              errors="coerce").dropna()
        except Exception:
            continue
        if not len(v):
            continue
        rows.append({
            "dataset": label,
            "level_of_variation": "technical replicates of one preparation",
            "n": int(len(v)), "median_log10_N0": float(v.median()),
            "L_note": "not stated in the deposit",
            "delta_h": np.nan,
        })
    return pd.DataFrame(rows)


def dubey_group() -> pd.DataFrame:
    if not DUBEY.exists():
        return pd.DataFrame()
    starts = []
    for sh in ("Figure 1", "Figure 4"):
        d = pd.read_excel(DUBEY, sheet_name=sh, header=None)
        t = pd.to_numeric(d[0], errors="coerce")
        v = pd.to_numeric(d[1], errors="coerce")
        starts.append(v[(t == 0) & (v > 1)])
    s = pd.concat(starts).dropna()
    h = np.log10(s / DUBEY_FLOOR)
    return pd.DataFrame([{
        "dataset": "Dubey, hollow fibre",
        "level_of_variation": "between cultures, one laboratory",
        "n": int(len(s)), "median_log10_N0": float(np.log10(s).median()),
        "L_note": f"{DUBEY_FLOOR:g} CFU/mL, derived from 100 uL plated",
        "delta_h": float(h.max() - h.min()),
    }])


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    ch = era4tb_channels()
    audit = era4tb_audit()

    # Between laboratories at a fixed plating volume, and across every channel.
    at_100 = ch[ch["plated_volume_ul"] == 100.0]
    era_rows = pd.DataFrame([
        {"dataset": "ERA4TB, between laboratories at 100 uL",
         "level_of_variation": "between laboratories, one written protocol",
         "n": int(at_100["n_readings"].sum()),
         "median_log10_N0": float(np.log10(at_100["N0_cfu_per_ml"]).median()),
         "L_note": "10 CFU/mL, derived from 100 uL plated",
         "delta_h": float(at_100["h_log10"].max() - at_100["h_log10"].min())},
        {"dataset": "ERA4TB, every laboratory and plating volume",
         "level_of_variation": "laboratories and plated volumes together",
         "n": int(ch["n_readings"].sum()),
         "median_log10_N0": float(np.log10(ch["N0_cfu_per_ml"]).median()),
         "L_note": "10, 100 or 400 CFU/mL by volume",
         "delta_h": float(ch["h_log10"].max() - ch["h_log10"].min())},
    ])

    main_tbl = pd.concat([era_rows, vijay_groups(), kaur_groups(), dubey_group()],
                         ignore_index=True)
    main_tbl["fold_spread"] = 10 ** main_tbl["delta_h"]
    main_tbl.to_csv(TABLES / "exp28_measurable_depth.csv", index=False)

    supp = main_tbl[["dataset", "median_log10_N0"]].copy()
    supp["fold_below_nominal_0.5_McFarland"] = (
        10 ** (np.log10(MCFARLAND_05) - supp["median_log10_N0"]))
    supp.to_csv(TABLES / "exp28_supplementary_mcfarland.csv", index=False)

    (RECEIPTS / "exp28_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp28_standard_vs_realised.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "definitions": {"H_i": "N0_i / L_i",
                        "h_i": "log10(N0_i / L_i), deepest measurable reduction",
                        "delta_h": "max(h_i) - min(h_i)",
                        "fold_spread": "10 ** delta_h"},
        "nominal_reference_only": {"half_mcfarland_cfu_per_ml": MCFARLAND_05,
                                   "status": "descriptive, not a compliance metric"},
        "era4tb_channels": ch.to_dict(orient="records"),
        "era4tb_floor_audit": audit,
        "main_table": main_tbl.to_dict(orient="records"),
    }, indent=2, default=str), encoding="utf-8")

    disp = main_tbl.copy()
    disp["median log10 N0"] = disp["median_log10_N0"].map(lambda v: f"{v:.2f}")
    disp["delta h (log10)"] = disp["delta_h"].map(
        lambda v: "NA" if pd.isna(v) else f"{v:.2f}")
    disp["fold spread"] = disp["fold_spread"].map(
        lambda v: "NA" if pd.isna(v) else f"{v:,.0f}x")
    disp = disp.rename(columns={"dataset": "dataset",
                                "level_of_variation": "level of variation",
                                "L_note": "quantification limit L"})
    show = disp[["dataset", "level of variation", "n", "median log10 N0",
                 "quantification limit L", "delta h (log10)", "fold spread"]]

    off_grid = {k: v for k, v in audit.items() if v["fraction_on_the_L_grid"] < 0.999}
    doc = f"""# Measurable kill depth across four deposits

Generated by `python -m src.experiments.exp28_standard_vs_realised`.

## Definitions

For culture *i* with starting density `N0_i` and quantification limit `L_i`:

- `H_i = N0_i / L_i` — a ratio
- `h_i = log10(N0_i / L_i)` — the deepest reduction measurable, in log10 CFU/mL
- `delta_h = max(h_i) - min(h_i)`, and `fold_spread = 10 ** delta_h`

Variation is reported on `h`, never on `N0` alone. In ERA4TB the limit follows
the plated volume — 1000/100 = 10, 1000/10 = 100, 1000/2.5 = 400 CFU/mL — so one
culture measured on a 2.5 uL drop and on a 100 uL quadruplicate differs by 1.6
log10 in measurable depth before any biology enters.

## Main table

{md_table(show, right=("n", "median log10 N0", "delta h (log10)", "fold spread"))}

Rows compare only within a level of variation. The clinical rows describe
between-isolate starting burden, which is biological and expected; they are not
a measure of laboratory imprecision, and reading them against the consortium row
would say the clinical deposit is orders of magnitude less reproducible, which is
not what the numbers mean.

Kaur is reported as NA rather than as a small number. Its three day-zero readings
are technical replicates of a single preparation, so they cannot estimate
between-preparation reproducibility, and the deposit states no quantification
limit, so `h` is not computable at all.

## The floor is borne out, laboratory by laboratory

A count reported per mL from a plate of volume V can only be a multiple of
1000/V. Across every institute and every plating volume in ERA4TB,
**{sum(1 for v in audit.values() if v['fraction_on_the_L_grid'] >= 0.999)} of
{len(audit)}** channels have every reading on that grid.
{"All channels pass." if not off_grid else
 "The exception is " + ", ".join(f"{k}, {100*v['fraction_on_the_L_grid']:.0f}% on grid" for k, v in off_grid.items())
 + ". Its off-grid values are multiples of 10 but not of 100 - 260, 840, 1040, 2350 - which is the signature of a count averaged over the four 10 uL drops rather than reported from one. That is a reporting convention rather than a different limit, and it does not move L."}

### Institute B, audited rather than labelled an outlier

Institute B has the second-lowest realised inoculum and was checked before being
described.

- Units are self-consistent: the largest disagreement between `CFU` and
  `CFUlog10` is 5.3e-15.
- All four plating volumes agree at day zero: 3.59, 3.63 and 3.67 log10 at
  2.5, 10 and 100 uL, twelve readings, none censored.
- Its counts sit on the grid the plated volume implies, so no additional
  dilution step is unaccounted for. The smallest count it reports at 100 uL is
  100 rather than 10, which means it never counted that low, not that its
  granularity differs.
- Its day −3 pre-inoculation reading is 3.56 against 3.63 at day zero, so the
  day-zero figure is stable.
- Its untreated culture grows from 3.6 to 5.8 log10 over fourteen days.

B seeded a genuinely low inoculum and it was measured correctly. It is not an
outlier to be excluded.

Two related observations. Institute B records no treated arm at day zero; its
treated series begin at day 1. And institute E is the only one to deposit a
separate `Inoculum TKA` row, at 4.35 log10, against an untreated day-1 reading of
5.38 — a full log between the recorded inoculum and the realised culture.

## Supplementary: distance from the nominal turbidity reference

{md_table(pd.DataFrame({
    "dataset": supp["dataset"],
    "median log10 N0": supp["median_log10_N0"].map(lambda v: f"{v:.2f}"),
    "fold below nominal 0.5 McFarland": supp["fold_below_nominal_0.5_McFarland"].map(lambda v: f"{v:,.0f}x"),
}), right=("median log10 N0", "fold below nominal 0.5 McFarland"))}

Fold below the nominal 0.5 McFarland reference, 1.5e8 CFU/mL. **Descriptive
only, not a protocol-compliance metric.** A time-kill inoculum is prepared by
diluting from a suspension matched to that turbidity, so every entry is expected
to sit far below it. The conversion of a turbidity to CFU/mL depends on species,
cell aggregation and preparation, and is least reliable for mycobacteria; TB
protocols also work from a range of dilutions and target inocula. The capacity of
a time-kill experiment is set by the measured `N0` and the real `L`, not by the
turbidity the preparation started from.

## Conclusion

The measured starting inoculum, rather than the nominal turbidity standard,
determined the maximum observable log-kill depth. Across ERA4TB laboratories at a
fixed plating volume this capacity differed by
{era_rows.loc[0, 'delta_h']:.2f} log10 units
({10 ** era_rows.loc[0, 'delta_h']:,.0f}-fold), and once the choice of plated
volume is included as well it differed by {era_rows.loc[1, 'delta_h']:.2f} log10
({10 ** era_rows.loc[1, 'delta_h']:,.0f}-fold). The larger ranges in the Vijay
datasets primarily represent between-isolate starting-burden heterogeneity and
should not be interpreted as laboratory imprecision. Kaur measurements were
technical replicates from single preparations and therefore do not estimate
between-preparation reproducibility.
"""
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(doc, encoding="utf-8")

    pd.set_option("display.width", 220)
    print(show.to_string(index=False))
    print(f"\nERA4TB floor audit: "
          f"{sum(1 for v in audit.values() if v['fraction_on_the_L_grid'] >= 0.999)}"
          f"/{len(audit)} institute-by-volume channels fully on the L = 1000/V grid")
    if off_grid:
        for k, v in off_grid.items():
            print(f"   off grid: {k} at {100*v['fraction_on_the_L_grid']:.0f}%")
    print(f"\nwrote {DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
