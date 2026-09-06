"""
Bayesian / discrete-posterior floor inference with a refusal rule (Exp33).

Run:  python -m src.experiments.exp33_floor_posterior

Validates src.floor_posterior on the five deposits audited in Exp29:
  DERIVED (ERA4TB volumes, Dubey) -> near-degenerate intervals
  INFERRED (Vijay) -> posterior concentrated on 23
  NONE (Windels, Kaur) -> refuse_labels True

Writes:
  results/tables/exp33_floor_posterior.csv
  results/receipts/exp33_receipt.json
  docs/29_FLOOR_POSTERIOR.md
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from src.floor_posterior import MAX_LOG10_SPAN_FOR_LABELS, floor_posterior
from src.infer_floor import load_deposits

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"
DOC = ROOT / "docs" / "29_FLOOR_POSTERIOR.md"


def load_all() -> dict[str, dict]:
    deps = load_deposits()

    # Windels: surviving fractions; zeros are below-limit placeholders, not a floor.
    w = pd.read_csv(DATA / "windels2024" / "timekill.csv")
    vals = pd.to_numeric(w["surv_frac"], errors="coerce").dropna().to_numpy(float)
    deps["Windels 2024, evolved clones (surviving fraction)"] = {
        "values": vals, "counts_per_ml": False, "recorded_volume_ul": None,
        "below_limit_as_zero": True,
        "stated_limit": "no plated volume; below-limit written as zero",
        "expect_verdict": "NONE", "expect_refuse": True,
    }

    # Dubey: genuine counts on Figures 1 and 4, DERIVED from 100 uL (Exp29).
    counts = []
    for sheet in ("Figure 1", "Figure 4"):
        df = pd.read_excel(DATA / "dubey2026" / "source_data.xlsx",
                           sheet_name=sheet, header=None)
        for col in df.columns[1:]:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            s = s[s > 1.0]  # drop below-limit placeholder of 1
            counts.append(s.to_numpy(float))
    dubey_vals = np.concatenate(counts) if counts else np.array([])
    deps["Dubey 2026, hollow fibre (CFU per mL)"] = {
        "values": dubey_vals, "counts_per_ml": True, "recorded_volume_ul": 100.0,
        "stated_limit": "100 uL plated; L = 10 derived",
        "expect_verdict": "DERIVED", "expect_refuse": False,
        "expect_point": 10.0,
    }

    # Expectations for deposits from infer_floor.load_deposits
    deps["Vijay 2024, clinical isolates (MPN per mL)"].update(
        expect_verdict="INFERRED", expect_refuse=False, expect_point=23.0)
    for vol in (100.0, 10.0, 2.5):
        key = f"ERA4TB, {vol:g} uL plated (CFU per mL)"
        if key in deps:
            deps[key].update(expect_verdict="DERIVED", expect_refuse=False,
                             expect_point=1000.0 / vol)
    deps["Kaur 2024, apramycin grid (log10 CFU per mL)"].update(
        expect_verdict="NONE", expect_refuse=True)
    return deps


def main() -> int:
    deps = load_all()
    rows = []
    checks = []
    for name, spec in deps.items():
        r = floor_posterior(
            spec["values"],
            counts_per_ml=spec.get("counts_per_ml", True),
            recorded_volume_ul=spec.get("recorded_volume_ul"),
            below_limit_as_zero=bool(spec.get("below_limit_as_zero", False)),
        )
        expect_v = spec.get("expect_verdict")
        expect_refuse = spec.get("expect_refuse")
        expect_point = spec.get("expect_point")
        ok_verdict = (expect_v is None) or (r.verdict == expect_v)
        ok_refuse = (expect_refuse is None) or (r.refuse_labels is expect_refuse)
        ok_point = True
        if expect_point is not None and r.candidate_floor is not None:
            ok_point = abs(r.candidate_floor - expect_point) < 1e-6
        passed = bool(ok_verdict and ok_refuse and ok_point)
        checks.append({"deposit": name, "passed": passed,
                       "expect_verdict": expect_v, "got_verdict": r.verdict,
                       "expect_refuse": expect_refuse, "got_refuse": r.refuse_labels})
        rows.append({
            "deposit": name,
            "verdict": r.verdict,
            "candidate_floor": r.candidate_floor,
            "ci_low": r.ci_low,
            "ci_high": r.ci_high,
            "log10_span": r.log10_span,
            "refuse_labels": r.refuse_labels,
            "reason": r.reason,
            "validation_passed": passed,
        })
        print(f"  {name[:52]:<52} {r.verdict:<9} "
              f"refuse={r.refuse_labels} span={r.log10_span}  "
              f"{'PASS' if passed else 'FAIL'}")

    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    tab = pd.DataFrame(rows)
    tab.to_csv(TABLES / "exp33_floor_posterior.csv", index=False)

    n_pass = int(sum(c["passed"] for c in checks))
    receipt = {
        "script": "src/experiments/exp33_floor_posterior.py",
        "utc": datetime.now(timezone.utc).isoformat(),
        "max_log10_span_for_labels": MAX_LOG10_SPAN_FOR_LABELS,
        "n_deposits": len(checks),
        "n_passed": n_pass,
        "all_passed": n_pass == len(checks),
        "checks": checks,
        "rows": rows,
    }
    (RECEIPTS / "exp33_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str), encoding="utf-8")

    lines = [
        "# Floor posterior with a refusal rule",
        "",
        "Generated by `python -m src.experiments.exp33_floor_posterior`.",
        "",
        "Unconstrained networks learn the training box of a closed-form boundary",
        "(`docs/22`). The division of labour is therefore: learn *L* under",
        "uncertainty; derive everything downstream. This module adds an interval",
        f"and a refusal when the 95% support spans more than "
        f"{MAX_LOG10_SPAN_FOR_LABELS:g} log10, or when the verdict is WEAK/NONE.",
        "",
        "## Method",
        "",
        "- **DERIVED** (plated volume recorded, minimum equals 1000/*V*): point mass.",
        "- **INFERRED** on an MPN ladder: discrete posterior over table rungs at or",
        "  below the observed minimum, weighted by pile-up and empty lower rungs;",
        "  95% highest-posterior-density support is the interval.",
        "- **WEAK / NONE**: refuse observability labels.",
        "",
        "## Validation on five deposits",
        "",
        "| Deposit | Verdict | Floor | 95% support | log10 span | Refuse | Pass |",
        "|---|---|---:|---|---:|---|---|",
    ]
    for r in rows:
        span = "" if r["log10_span"] is None else f"{r['log10_span']:.3g}"
        ci = ("—" if r["ci_low"] is None
              else f"[{r['ci_low']:g}, {r['ci_high']:g}]")
        floor = "—" if r["candidate_floor"] is None else f"{r['candidate_floor']:g}"
        lines.append(
            f"| {r['deposit']} | {r['verdict']} | {floor} | {ci} | {span} | "
            f"{r['refuse_labels']} | {r['validation_passed']} |"
        )
    lines += [
        "",
        f"**{n_pass} of {len(checks)} validation checks passed.**",
        "",
        "## How callers must use the refusal",
        "",
        "If `refuse_labels` is true, do not emit forced / undecidable observability",
        "classes. Report that the assay floor is underspecified. Headroom arithmetic",
        "may still be shown as a sensitivity over a stated range of *L*, but not as",
        "a point classification.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {DOC.relative_to(ROOT)}  ({n_pass}/{len(checks)} passed)")
    return 0 if n_pass == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
