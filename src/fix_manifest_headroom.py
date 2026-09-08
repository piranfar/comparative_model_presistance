"""
Recompute the manifest's headroom verdict from its own evidence columns.

Run:  python -m src.fix_manifest_headroom

WHY. data/manifests/corpus.csv carries three evidence columns filled in by
hand from the deposited files -- has_time_series, has_starting_density,
has_floor_or_volume -- and a fourth, headroom_computable, that is supposed to
summarise them. The summary had drifted badly: 58 of 62 rows read "no: neither
reported" while the evidence columns beside them said YES to all three in 18.

That is not a cosmetic problem. The verdict column is what a reader consults,
and it was hiding eight deposits that qualify, including one whose floor is
stated three times over inside its own deposited R script:

    censReg(logCFU ~ hours, data = MICs, left = log(50))
    censored$mean_CFU[censored$mean_CFU < 50] <- 50
    geom_hline(yintercept = 50) ... label = "Detection Limit"

The verdict is now derived rather than typed, so it cannot drift again. The
evidence columns stay hand-written, because reading a deposit is a human act;
only the conclusion drawn from them is mechanical.

Writes data/manifests/corpus.csv in place, and prints what changed.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifests" / "corpus.csv"

EVIDENCE = ["has_time_series", "has_starting_density", "has_floor_or_volume"]


def affirmative(x) -> bool | None:
    """Read a hand-written evidence cell as yes, no, or not established.

    The cells are prose -- "YES - verified by parsing the workbook", "NO - no
    plated volume, no LOD", "UNKNOWN - contents not inspected" -- so the first
    word carries the verdict and everything after it carries the reason. A cell
    that is blank or UNKNOWN is not a NO: nobody has looked, and recording that
    as a refusal would bury a deposit that may well qualify.
    """
    s = str(x).strip().upper()
    if not s or s in ("NAN", "(BLANK)"):
        return None
    if s.startswith(("YES", "UPGRADED")):
        return True
    if s.startswith(("NO", "NOT ")):
        return False
    if s.startswith(("UNKNOWN", "PARTIAL")):
        return None
    return None


def verdict(row) -> str:
    marks = {c: affirmative(row[c]) for c in EVIDENCE}
    if all(v is True for v in marks.values()):
        return "yes"
    missing = [c.replace("has_", "").replace("_", " ")
               for c, v in marks.items() if v is False]
    unknown = [c.replace("has_", "").replace("_", " ")
               for c, v in marks.items() if v is None]
    if missing:
        return "no: " + ", ".join(missing) + " not present"
    if unknown:
        return "not established: " + ", ".join(unknown) + " not inspected"
    return "not established"


def main() -> int:
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}")
    d = pd.read_csv(MANIFEST)
    before = d.headroom_computable.astype(str).copy()
    d["headroom_computable"] = d.apply(verdict, axis=1)
    after = d.headroom_computable.astype(str)

    changed = d[before != after]
    print(f"{len(d)} deposits; {len(changed)} verdicts changed\n")
    gained = d[(after == "yes") & (before != "yes")]
    if len(gained):
        print(f"   {len(gained)} deposits now read 'yes' that did not before:")
        for r in gained.itertuples():
            print(f"      {str(r.study_id):20} {str(r.species)[:44]}")
    print(f"\n   final tally:")
    for v, n in after.value_counts().items():
        print(f"      {n:>3}  {v[:70]}")

    d.to_csv(MANIFEST, index=False)
    print(f"\n   wrote {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
