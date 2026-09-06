"""
Assay geometry: floor inference, headroom, and observability in one CLI.

Run:  python -m src.assay_geometry --help
      python -m src.assay_geometry vignette clinical
      python -m src.assay_geometry vignette dubey
      python -m src.assay_geometry headroom --n0 2.3e4 --floor 23
      python -m src.assay_geometry floor --deposit vijay
      python -m src.assay_geometry observe --n0 1e4 --n-final 23 --floor 23 --label Medium

WHY THIS EXISTS. The paper's software contribution is not a neural net that
predicts MDK. It is the closed-form geometry around an inferred floor L:
headroom H = log10(N0/L), reachability of a q-log endpoint, and whether a
floor-level tolerance label was forced by the inoculum or still undecidable.
src/headroom.py, src/floor_posterior.py and the Exp25 observability rules each
answer one piece. This module is the product surface: one entry point, JSON or
human report, and two vignettes that must reproduce the manuscript counts.

VIGNETTE CONTRACTS (regression targets, not illustrations).
  clinical  -> 33 isolates short of 4-log headroom; 12 forced; 6 undecidable
  dubey     -> 5 of 20 cultures short of 5 logs; 20 of 20 short of 6 logs
               (equivalently: 5 unreachable at 5 logs, 20 at 6 logs among
               cultures with a measured t=0)

Refusal: if floor_posterior.refuse_labels is true, observability classes are
not emitted.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .floor_posterior import FloorPosterior, floor_posterior
from .headroom import (
    ENDPOINT_LOGS,
    headroom,
    hidden_burden,
    limit_from_plated_volume,
    reachable,
    recorded_fraction_at_floor,
    report as headroom_report,
)
from .infer_floor import load_deposits

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"

CLASS_CUTS = (1e-3, 1e-2)
CLASS_ORDER = {"Low": 0, "Medium": 1, "High": 2}
MPN_FLOOR = 23.0
DEEP_ENDPOINT_LOGS = 4.0
DUBEY_PLACEHOLDER = 1.0
DUBEY_FLOOR = 10.0


def _class_of(fraction: float) -> str:
    lo, hi = CLASS_CUTS
    return "Low" if fraction < lo else ("Medium" if fraction <= hi else "High")


@dataclass
class ObservabilityCall:
    observability: str
    recorded_class: str | None
    headroom_log10: float
    day5_at_floor: bool
    deep_endpoint_reachable: bool
    refuse: bool
    reason: str


def observe_one(n0: float, n_final: float, floor: float,
                recorded_class: str | None = None,
                refuse: bool = False) -> ObservabilityCall:
    """Classify one isolate; refuse if the floor posterior says so."""
    if refuse or not (n0 > 0 and floor > 0):
        return ObservabilityCall(
            observability="refused", recorded_class=recorded_class,
            headroom_log10=float("nan"), day5_at_floor=False,
            deep_endpoint_reachable=False, refuse=True,
            reason="floor underspecified; observability labels not emitted",
        )
    h = math.log10(n0 / floor)
    at_floor = n_final <= floor + 1e-9
    if not at_floor:
        klass = "determinable"
        reason = "day-5 reading above the floor"
    else:
        low = _class_of(0.0)
        high = _class_of(floor / n0)
        if low == high:
            klass = "forced by inoculum"
            reason = "only one class reachable under the floor bound"
        else:
            klass = "undecidable"
            reason = f"classes reachable under the bound: {low} to {high}"
    return ObservabilityCall(
        observability=klass, recorded_class=recorded_class,
        headroom_log10=h, day5_at_floor=at_floor,
        deep_endpoint_reachable=h >= DEEP_ENDPOINT_LOGS,
        refuse=False, reason=reason,
    )


def geometry_report(n0: float, floor: float,
                    culture_volume_ml: float | None = None,
                    floor_post: FloorPosterior | None = None) -> dict:
    """Headroom block plus optional floor-posterior refusal flag."""
    limit = math.log10(floor)
    h = headroom(n0, limit)
    out = {
        "n0": n0,
        "floor": floor,
        "headroom_log10": h,
        "recorded_fraction_at_floor": recorded_fraction_at_floor(n0, limit),
        "endpoints": {
            name: {"needs_logs": q, "reachable": reachable(n0, limit, q)}
            for name, q in ENDPOINT_LOGS.items()
        },
        "refuse_observability_labels": bool(
            floor_post.refuse_labels if floor_post else False),
        "floor_posterior": floor_post.to_dict() if floor_post else None,
        "human": headroom_report(n0, limit, culture_volume_ml),
    }
    if culture_volume_ml:
        out["hidden_burden_cells"] = hidden_burden(limit, culture_volume_ml)
    return out


# ---------------------------------------------------------------- vignettes ---
def vignette_clinical() -> dict:
    """Reproduce manuscript 33 / 12 / 6 on Vijay clinical isolates."""
    path = DATA / "tb" / "elife93243_supp2.xlsx"
    d = pd.read_excel(path)
    cols = [c for c in d.columns if c.startswith("mpn_") and "log" not in c]
    vals = pd.concat([d[c] for c in cols]).dropna().to_numpy(float)
    post = floor_posterior(vals, counts_per_ml=True, recorded_volume_ul=None)
    floor = float(post.candidate_floor) if post.candidate_floor else MPN_FLOOR

    n0 = pd.to_numeric(d["mpn_T0_15days"], errors="coerce")
    n5 = pd.to_numeric(d["mpn_T5_15days"], errors="coerce")
    lab = d["Tolerant_level_D5_15"]
    # Headroom census uses every isolate with a measured N0 (manuscript: 33/217).
    short = int(((np.log10(n0 / floor) < DEEP_ENDPOINT_LOGS) & n0.notna()).sum())
    n_with_n0 = int(n0.notna().sum())

    calls = []
    if not post.refuse_labels:
        usable = n0.notna() & n5.notna() & lab.isin(CLASS_ORDER)
        for i in d.index[usable]:
            calls.append(observe_one(
                float(n0.loc[i]), float(n5.loc[i]), floor,
                recorded_class=str(lab.loc[i]), refuse=False))
    n_forced = sum(1 for c in calls if c.observability == "forced by inoculum")
    n_undec = sum(1 for c in calls if c.observability == "undecidable")
    n_det = sum(1 for c in calls if c.observability == "determinable")

    expected = {"short_of_4log": 33, "forced": 12, "undecidable": 6}
    got = {"short_of_4log": short, "forced": n_forced, "undecidable": n_undec}
    passed = got == expected

    return {
        "vignette": "clinical",
        "deposit": "eLife 93243 supplementary file 2",
        "floor_posterior": post.to_dict(),
        "floor_used": floor,
        "n_isolates_with_n0": n_with_n0,
        "n_observability_calls": len(calls),
        "short_of_4log_headroom": short,
        "forced_by_inoculum": n_forced,
        "undecidable": n_undec,
        "determinable": n_det,
        "expected": expected,
        "got": got,
        "passed": passed,
        "human": (
            f"Clinical vignette (Vijay / eLife 93243)\n"
            f"  floor posterior: {post.verdict} L={floor:g} "
            f"refuse={post.refuse_labels}\n"
            f"  short of 4-log headroom: {short} of {n_with_n0} "
            f"(expect {expected['short_of_4log']})\n"
            f"  observability: {n_forced} forced, {n_undec} undecidable, "
            f"{n_det} determinable "
            f"(expect {expected['forced']}/{expected['undecidable']})\n"
            f"  {'PASS' if passed else 'FAIL'}"
        ),
    }


def vignette_dubey() -> dict:
    """Reproduce manuscript 5/20: unreachable at 5 logs / 6 logs."""
    source = DATA / "dubey2026" / "source_data.xlsx"
    counts, starts = [], []
    for sheet in ("Figure 1", "Figure 4"):
        s = pd.read_excel(source, sheet_name=sheet, header=None)
        t = pd.to_numeric(s[0], errors="coerce")
        for c in s.columns[1:]:
            v = pd.to_numeric(s[c], errors="coerce")
            counts.append(v[v > DUBEY_PLACEHOLDER])
        free = pd.to_numeric(s[1], errors="coerce")
        starts.append(free[(t == 0) & (free > DUBEY_PLACEHOLDER)])
    all_counts = pd.concat(counts).dropna().to_numpy(float)
    n0 = pd.concat(starts).dropna().to_numpy(float)

    post = floor_posterior(all_counts, counts_per_ml=True,
                           recorded_volume_ul=100.0)
    floor = float(post.candidate_floor) if post.candidate_floor else DUBEY_FLOOR
    h = np.log10(n0 / floor)
    n5 = int((h < 5.0).sum())
    n6 = int((h < 6.0).sum())
    n_cult = int(len(n0))

    expected = {"unreachable_5log": 5, "unreachable_6log": 20, "n_cultures": 20}
    got = {"unreachable_5log": n5, "unreachable_6log": n6, "n_cultures": n_cult}
    # Contract: 5 of 20 short of 5 logs; all 20 short of 6 logs.
    passed = (n5 == 5 and n6 == 20 and n_cult == 20
              and post.verdict == "DERIVED" and not post.refuse_labels)

    return {
        "vignette": "dubey",
        "deposit": "Dubey et al. 2026 Nat Commun source data",
        "floor_posterior": post.to_dict(),
        "floor_used": floor,
        "n_cultures_with_measured_t0": n_cult,
        "unreachable_at_5log": n5,
        "unreachable_at_6log": n6,
        "expected": expected,
        "got": got,
        "passed": passed,
        "human": (
            f"Dubey vignette (hollow fibre)\n"
            f"  floor posterior: {post.verdict} L={floor:g} "
            f"refuse={post.refuse_labels}\n"
            f"  cultures with measured t=0: {n_cult}\n"
            f"  unreachable at 5 logs: {n5} of {n_cult} (expect 5)\n"
            f"  unreachable at 6 logs: {n6} of {n_cult} (expect 20)\n"
            f"  {'PASS' if passed else 'FAIL'}"
        ),
    }


def deposit_floor(name: str) -> dict:
    """Named deposit floor posterior for CLI users."""
    key = {
        "vijay": "Vijay 2024, clinical isolates (MPN per mL)",
        "era4tb100": "ERA4TB, 100 uL plated (CFU per mL)",
        "era4tb10": "ERA4TB, 10 uL plated (CFU per mL)",
        "era4tb2.5": "ERA4TB, 2.5 uL plated (CFU per mL)",
        "kaur": "Kaur 2024, apramycin grid (log10 CFU per mL)",
    }.get(name.lower())
    if key is None:
        raise SystemExit(f"unknown deposit {name!r}; "
                         f"choose vijay|era4tb100|era4tb10|era4tb2.5|kaur")
    deps = load_deposits()
    spec = deps[key]
    post = floor_posterior(spec["values"], spec.get("counts_per_ml", True),
                           spec.get("recorded_volume_ul"))
    return {"deposit": key, "floor_posterior": post.to_dict(),
            "stated_limit": spec.get("stated_limit"),
            "human": (f"{key}\n  verdict={post.verdict}  L={post.candidate_floor}\n"
                      f"  95% support=[{post.ci_low}, {post.ci_high}]  "
                      f"span={post.log10_span}\n"
                      f"  refuse_labels={post.refuse_labels}\n  {post.reason}")}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m src.assay_geometry",
        description="Floor inference, headroom, and observability for MDK assays.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_h = sub.add_parser("headroom", help="reachable endpoints for one culture")
    p_h.add_argument("--n0", type=float, required=True)
    g = p_h.add_mutually_exclusive_group(required=True)
    g.add_argument("--floor", type=float)
    g.add_argument("--plated-volume", type=float, metavar="UL")
    p_h.add_argument("--culture-volume-ml", type=float, default=None)
    p_h.add_argument("--json", action="store_true")

    p_o = sub.add_parser("observe", help="observability class for one isolate")
    p_o.add_argument("--n0", type=float, required=True)
    p_o.add_argument("--n-final", type=float, required=True)
    p_o.add_argument("--floor", type=float, required=True)
    p_o.add_argument("--label", type=str, default=None)
    p_o.add_argument("--refuse", action="store_true")
    p_o.add_argument("--json", action="store_true")

    p_f = sub.add_parser("floor", help="floor posterior for a named deposit")
    p_f.add_argument("--deposit", required=True,
                     choices=["vijay", "era4tb100", "era4tb10", "era4tb2.5", "kaur"])
    p_f.add_argument("--json", action="store_true")

    p_v = sub.add_parser("vignette", help="reproduce manuscript count contracts")
    p_v.add_argument("name", choices=["clinical", "dubey", "all"])
    p_v.add_argument("--json", action="store_true")

    a = ap.parse_args(argv)

    if a.cmd == "headroom":
        floor = (a.floor if a.floor is not None
                 else 10.0 ** limit_from_plated_volume(a.plated_volume))
        out = geometry_report(a.n0, floor, a.culture_volume_ml)
        if a.json:
            print(json.dumps({k: v for k, v in out.items() if k != "human"},
                             indent=2))
        else:
            print(out["human"])
        return 0

    if a.cmd == "observe":
        call = observe_one(a.n0, a.n_final, a.floor, a.label, refuse=a.refuse)
        if a.json:
            print(json.dumps(asdict(call), indent=2))
        else:
            print(f"observability: {call.observability}\n"
                  f"headroom:      {call.headroom_log10:.3g} log10\n"
                  f"at floor:      {call.day5_at_floor}\n"
                  f"deep reachable:{call.deep_endpoint_reachable}\n"
                  f"reason:        {call.reason}")
        return 0

    if a.cmd == "floor":
        out = deposit_floor(a.deposit)
        if a.json:
            print(json.dumps({k: v for k, v in out.items() if k != "human"},
                             indent=2, default=str))
        else:
            print(out["human"])
        return 0 if not out["floor_posterior"]["refuse_labels"] else 0

    if a.cmd == "vignette":
        names = (["clinical", "dubey"] if a.name == "all" else [a.name])
        results = []
        ok = True
        for name in names:
            r = vignette_clinical() if name == "clinical" else vignette_dubey()
            results.append(r)
            ok = ok and bool(r["passed"])
            if a.json:
                continue
            print(r["human"])
            print()
        if a.json:
            print(json.dumps(results if len(results) > 1 else results[0],
                             indent=2, default=str))
        return 0 if ok else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
