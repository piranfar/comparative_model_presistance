"""
The boundary framework applied to a deposit it has never seen.

Run:  python -m src.experiments.exp27_out_of_sample_boundaries

WHY THIS EXISTS. docs/19 derives two boundaries and checks them against the
deposit they were built on, which is the weakest kind of check. An overnight
search of five repositories, the TB consortia, the food-microbiology literature
and the hollow-fibre field turned up one deposit that closes the gap, and this
applies the framework to it cold.

WHAT MAKES THIS DEPOSIT DIFFERENT. Of the four already in hand, only ERA4TB
records a plated volume, so only ERA4TB has a floor that is derived rather than
inferred, and none of the four records a per-culture measured starting density or
a culture volume. Dubey et al. 2026 has all three:

  - the Methods state 100 uL plated, so L = 1000/100 = 10 CFU/mL
  - the file carries MEASURED t=0 counts per culture, not a nominal inoculum
  - the paper states the cartridge volumes, so an absolute burden is computable

The floor is corroborated inside the file rather than taken on trust. A 100 uL
plate reporting per mL can only return multiples of 10, and every genuine count
in the deposit is one: 229 of 229, with the smallest exactly 10. That is the
signature of the plating protocol showing up in the data, and it is checked here
rather than asserted.

THE ONE JUDGEMENT CALL, STATED PLAINLY. The drug-treated columns contain entries
of exactly 1, which cannot be a count from a 100 uL plate since the smallest such
count is 10. They are the deposit's below-limit placeholder. They are treated as
censored at L and never as measurements of one cell per mL.

A SECOND, WHICH COSTS A FULL ORDER OF MAGNITUDE IF MISSED. The Methods give a
nominal inoculum of 1e5 CFU/mL. The measured t=0 counts are 7e5 to 2.8e6. Using
the nominal figure would put a whole log into every boundary, so N0 is taken from
the file and never from the Methods.

Writes:  results/tables/exp27_out_of_sample.csv
         results/receipts/exp27_receipt.json
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

# Dubey V, Darlow C, Gerada A, et al. Nat Commun 2026;17(1). PMC13408132, CC BY 4.0.
# Source Data file, sheets "Figure 1" and "Figure 4".
SOURCE = ROOT / "data" / "raw" / "dubey2026" / "source_data.xlsx"
PLATED_UL = 100.0
FLOOR = 1000.0 / PLATED_UL          # 10 CFU/mL, derived from the plating protocol
BELOW_LIMIT_PLACEHOLDER = 1.0
DEPTHS = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)


# In both sheets column 0 is time and column 1 is the DRUG-FREE arm; the
# drug-treated arm sits in the last column. The starting density of a culture is
# the drug-free count at t = 0, and only that. Taking t = 0 from every column
# swept in one drug-arm reading of 10, which is the floor itself, and produced a
# culture with zero headroom that does not exist.
DRUG_FREE_COL = 1


def load_counts() -> tuple[pd.Series, pd.Series]:
    """Every genuine count, and the measured t=0 density of every culture.

    A note on the deposit rather than on our handling: in both sheets the
    drug-treated arm reads at or below the limit already at t = 0, while its
    paired drug-free control reads about 1e6. So the treated t = 0 sample was
    taken after exposure rather than before it. That does not affect the
    boundaries, which need the inoculum and the floor, but it does mean the
    treated column cannot be used to establish a starting density.
    """
    counts, starts = [], []
    for sheet in ("Figure 1", "Figure 4"):
        d = pd.read_excel(SOURCE, sheet_name=sheet, header=None)
        t = pd.to_numeric(d[0], errors="coerce")
        for c in d.columns[1:]:                      # column 0 is time
            v = pd.to_numeric(d[c], errors="coerce")
            counts.append(v[v > 0])
        free = pd.to_numeric(d[DRUG_FREE_COL], errors="coerce")
        starts.append(free[(t == 0) & (free > BELOW_LIMIT_PLACEHOLDER)])
    return pd.concat(counts).dropna(), pd.concat(starts).dropna()


def corroborate_floor(counts: pd.Series) -> dict:
    """Does the data itself show the granularity the plating protocol implies?"""
    genuine = counts[counts > BELOW_LIMIT_PLACEHOLDER]
    on_grid = np.isclose(genuine % FLOOR, 0)
    return {
        "plated_volume_ul": PLATED_UL,
        "derived_floor_per_ml": FLOOR,
        "n_genuine_counts": int(len(genuine)),
        "n_on_the_grid": int(on_grid.sum()),
        "fraction_on_the_grid": float(on_grid.mean()),
        "smallest_genuine_count": float(genuine.min()),
        "n_below_limit_placeholders": int((counts == BELOW_LIMIT_PLACEHOLDER).sum()),
        "corroborated": bool(on_grid.all() and np.isclose(genuine.min(), FLOOR)),
    }


def boundaries(starts: pd.Series) -> pd.DataFrame:
    rows = []
    head = np.log10(starts / FLOOR)
    for q in DEPTHS:
        short = int((head < q).sum())
        rows.append({
            "endpoint_logs": q,
            "endpoint_pct": 100 * (1 - 10 ** -q),
            "N_reach_per_ml": FLOOR * 10 ** q,
            "n_cultures": int(len(starts)),
            "n_unreachable": short,
            "pct_unreachable": 100 * short / len(starts),
        })
    return pd.DataFrame(rows)


def main() -> int:
    if not SOURCE.exists():
        print(f"source not present at {SOURCE.relative_to(ROOT)}")
        print("Download the Source Data file of Nat Commun 2026;17(1), "
              "PMC13408132 (CC BY 4.0), and place it there.")
        return 1

    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    counts, starts = load_counts()
    floor = corroborate_floor(counts)
    b = boundaries(starts)
    b.to_csv(TABLES / "exp27_out_of_sample.csv", index=False)

    head = np.log10(starts / FLOOR)
    (RECEIPTS / "exp27_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp27_out_of_sample_boundaries.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_source": "Dubey et al. 2026, Nat Commun 17(1), PMC13408132, CC BY 4.0",
        "floor": floor,
        "n_cultures_with_measured_start": int(len(starts)),
        "start_density_range": [float(starts.min()), float(starts.max())],
        "headroom_range_log10": [float(head.min()), float(head.max())],
        "boundaries": b.to_dict(orient="records"),
    }, indent=2, default=str), encoding="utf-8")

    print("-- is the derived floor corroborated by the data itself? --")
    print(f"   plated volume stated in the Methods : {PLATED_UL:g} uL")
    print(f"   floor that implies                  : {FLOOR:g} CFU/mL")
    print(f"   genuine counts on that grid         : {floor['n_on_the_grid']}"
          f"/{floor['n_genuine_counts']} "
          f"({100*floor['fraction_on_the_grid']:.1f}%)")
    print(f"   smallest genuine count              : {floor['smallest_genuine_count']:g}")
    print(f"   below-limit placeholders            : {floor['n_below_limit_placeholders']}")
    print(f"   verdict                             : "
          f"{'DERIVED and corroborated' if floor['corroborated'] else 'NOT corroborated'}")

    print(f"\n-- {len(starts)} cultures with a measured starting density --")
    print(f"   range {starts.min():,.0f} to {starts.max():,.0f} CFU/mL")
    print(f"   headroom {head.min():.2f} to {head.max():.2f} log10")

    print("\n-- what each endpoint could have demonstrated, out of sample --")
    print(b.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))

    worst = b[b["n_unreachable"] > 0]
    if len(worst):
        first = worst.iloc[0]
        print(f"\n   The shallowest endpoint any culture cannot reach is "
              f"{first['endpoint_logs']:.0f} logs, unreachable for "
              f"{int(first['n_unreachable'])} of {int(first['n_cultures'])}.")
    else:
        print("\n   Every endpoint tested is reachable for every culture here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
