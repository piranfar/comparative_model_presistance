"""BENZBROMARONE2025 -- returns NOTHING, on purpose.

Data_Sheet_1 (sheets Fig.1 to Fig.5) contains what looks like a usable
time-kill: sheet Fig.3, panels A to C, six time points (0-12 h), four arms
(untreated, colistin 0.5 ug/mL, benzbromarone 64 ug/mL, and the combination),
three replicate columns per arm, in log10 CFU/mL.  It is not ingested, because
the numbers in this workbook cannot be measurements.  Five findings, each
reproducible from the file itself:

1. Fig.1, the checkerboard.  Every one of the 64 optical-density values in
   panel A ends in the decimal digit 5; every one of the 64 in panel B and
   every one of the 64 in panel C ends in 4.  Real plate reads do not share a
   terminal digit.

2. Fig.2, the growth curves.  Sixteen of the thirty cells of the colistin arm
   are bit-identical between panel A and panel C -- different strains,
   independent experiments -- including whole triplicates at 6, 8, 10, 12 and
   16 h, and including the misplaced decimal 0.0288, which appears in panel A
   where panel C has 0.288.  That is a copy, with a typo copied along with it.

3. Fig.3A-C, the time-kill.  237 non-zero log10 values share only 124 distinct
   six-digit fractional strings: "482135" occurs 19 times and "193458" 13
   times, across different strains, arms, replicates and time points.  Worse,
   76 of the 124 strings use six all-different digits, where 18.7 +/- 4.0 are
   expected if the digits were those of measured quantities (z = 14).  These
   are hand-invented digit strings being recycled.  For contrast, the same
   count on HAO2026's time-kill -- an ordinary log10 CFU deposit -- gives 120
   distinct strings out of 144 values and 15 all-distinct-digit strings, right
   where chance puts it.

4. Fig.4D.  The four treatment groups read 624/524/424/124, 503/403/403/103
   and 498/463/398/98: exact decrements of 100 across arms that are supposed
   to be independent.

5. Fig.3A and 3B report the combination arm as exactly 0 at 10 h and 12 h,
   i.e. censoring written as a zero, with no limit of detection anywhere in
   the workbook to interpret it against.

Any one of these might be argued about.  Together they establish that the
deposited values were not read off plates, and the point of this corpus is to
count real detection floors against real counts.  Ingesting these rows would
put fabricated log-densities into that count with no way for anyone
downstream to tell them apart, so the reader returns an empty frame.

To re-check finding 3 without re-reading this docstring:

    import collections, pandas as pd
    g = pd.read_excel(<the workbook>, "Fig.3", header=None)
    v = [float(g.iat[r, c]) for r0 in (2, 15, 28) for r in range(r0, r0 + 7)
         for c in range(1, 13) if pd.notna(g.iat[r, c])]
    print(collections.Counter(f"{x:.6f}".split(".")[1] for x in v if x > 0)
          .most_common(5))
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingest import empty


def read(d: Path) -> pd.DataFrame:
    """Deliberately empty -- see the module docstring."""
    return empty()
