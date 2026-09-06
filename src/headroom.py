"""
Headroom: is the tolerance endpoint you are about to measure reachable at all?

Run:  python -m src.headroom --help
      python -m src.headroom --n0 2.3e4 --floor 23
      python -m src.headroom --n0 1e6 --plated-volume 100 --endpoint 99.99

WHY THIS EXISTS. The paper recommends four things: report the starting density
and the limit of quantification, match the endpoint depth to the dynamic range
actually available, treat a reading at the floor as a bound rather than a value,
and record the physiological state. Recommendations that arrive without a tool
are exhortations. This is the tool, and it is deliberately small enough to read
in one sitting and to reimplement in any language.

THE ONE IDEA. A tolerance endpoint asks for a q-log reduction. An assay can
resolve a reduction only as deep as the distance from where the culture started
down to the lowest density the assay reports. That distance is the HEADROOM,

    H = log10(N0 / L)

and it is fixed by the dilution scheme and the starting culture before any drug
acts. If H < q the endpoint is unreachable: the culture will be recorded as
having failed to reach it whatever the drug did, and that record is arithmetic
rather than biology. If the final reading rests on the floor, the recorded
surviving fraction is exactly L/N0, which is an upper bound on survival and not
a measurement of it.

Two limits are commonly available and it matters which is used. When the assay is
a plate and counts are expressed per millilitre, one colony in a plated volume v
microlitres is 1000/v per millilitre, so the limit follows from the pipette. When
the assay is a most probable number, the limit is the smallest value the MPN
table returns for the dilution series used.

WHAT THIS DOES NOT DO. It says nothing about whether a reachable endpoint was
reached, and nothing about the biology of an isolate. It answers one question:
could this experiment, as configured, have demonstrated this endpoint at all.
"""
from __future__ import annotations

import argparse
import math

# The tolerance endpoints in common use, as the log10 reduction each demands.
ENDPOINT_LOGS = {"90": 1.0, "99": 2.0, "99.9": 3.0, "99.99": 4.0}


def limit_from_plated_volume(volume_ul: float) -> float:
    """The log10 limit implied by plating `volume_ul` when counts are per mL.

    One colony in v microlitres is 1000/v per millilitre. This is the limit the
    pipette chose, not one the experimenter set, and it moves by a full log
    between a 100 microlitre quadruplicate and a 10 microlitre drop.
    """
    if volume_ul <= 0:
        raise ValueError("plated volume must be positive")
    return math.log10(1000.0 / volume_ul)


def headroom(n0: float, limit_log10: float) -> float:
    """log10 distance from the starting density down to the assay floor."""
    if n0 <= 0:
        raise ValueError("starting density must be positive")
    return math.log10(n0) - limit_log10


def reachable(n0: float, limit_log10: float, endpoint_logs: float) -> bool:
    """Could this experiment demonstrate this reduction, if every cell died?"""
    return headroom(n0, limit_log10) >= endpoint_logs


def recorded_fraction_at_floor(n0: float, limit_log10: float) -> float:
    """What a reading resting on the floor computes: L / N0.

    Returned so it can be reported as the bound it is. Two cultures killed to the
    same unmeasurable value get different numbers here purely because they
    started in different places.
    """
    return (10.0 ** limit_log10) / n0


def hidden_burden(limit_log10: float, culture_volume_ml: float) -> float:
    """Viable cells that may remain in the vessel when the assay reads blank.

    A limit is a concentration; a flask holds a volume. The number of survivors
    the blank plate is consistent with is the product, and it is not zero. This
    is the arithmetic behind the clinical rule that a negative culture taken
    under antibiotic is not evidence of sterility.

    Requires a culture volume, which most published deposits do not state. If
    you do not know it, you do not know this number: do not guess it.
    """
    if culture_volume_ml <= 0:
        raise ValueError("culture volume must be positive")
    return (10.0 ** limit_log10) * culture_volume_ml


def report(n0: float, limit_log10: float, culture_volume_ml: float | None = None) -> str:
    h = headroom(n0, limit_log10)
    lines = [
        f"starting density      {n0:,.4g} per mL   ({math.log10(n0):.2f} log10)",
        f"assay floor           {10 ** limit_log10:,.4g} per mL   ({limit_log10:.2f} log10)",
        f"headroom              {h:.2f} log10",
        "",
        "endpoint      needs   reachable?",
    ]
    for name, q in ENDPOINT_LOGS.items():
        ok = h >= q
        note = "" if ok else "   <-- unreachable whatever the drug does"
        lines.append(f"  {name + '%':<10} {q:.0f} log   {'yes' if ok else 'NO '}{note}")
    lines += [
        "",
        f"if the final reading rests on the floor, the recorded surviving",
        f"fraction is {recorded_fraction_at_floor(n0, limit_log10):.3g}, which is an UPPER BOUND on survival,",
        "not a measurement of it.",
    ]
    if culture_volume_ml:
        lines += [
            "",
            f"in a {culture_volume_ml:g} mL culture, a blank assay is consistent with up to",
            f"{hidden_burden(limit_log10, culture_volume_ml):,.0f} viable cells still present.",
        ]
    else:
        lines += [
            "",
            "culture volume not given, so the surviving burden behind a blank",
            "reading is not computed. Most deposits do not state it; if yours",
            "does, pass --culture-volume-ml and do not guess.",
        ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Is the tolerance endpoint you are about to measure reachable?")
    ap.add_argument("--n0", type=float, required=True,
                    help="starting density, per mL (e.g. 2.3e4)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--floor", type=float,
                   help="assay floor, per mL (e.g. 23 for an MPN series)")
    g.add_argument("--plated-volume", type=float, metavar="UL",
                   help="plated volume in uL, for a plate assay reporting per mL")
    ap.add_argument("--culture-volume-ml", type=float, default=None,
                    help="vessel volume, for the surviving burden behind a blank reading")
    ap.add_argument("--endpoint", choices=sorted(ENDPOINT_LOGS), default=None,
                    help="check one endpoint and exit non-zero if it is unreachable")
    a = ap.parse_args(argv)

    limit = (limit_from_plated_volume(a.plated_volume) if a.plated_volume
             else math.log10(a.floor))
    print(report(a.n0, limit, a.culture_volume_ml))

    if a.endpoint:
        q = ENDPOINT_LOGS[a.endpoint]
        if not reachable(a.n0, limit, q):
            print(f"\nFAIL: a {a.endpoint}% endpoint needs {q:.0f} logs and this "
                  f"assay has {headroom(a.n0, limit):.2f}.")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
