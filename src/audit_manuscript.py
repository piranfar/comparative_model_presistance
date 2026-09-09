"""
Audit the manuscript itself, not only the values the tables report.

Run:  python -m src.audit_manuscript

WHY THIS EXISTS. src/audit_claims.py recomputes every pinned number from the
results tables and passes. Peer review nevertheless found around twenty numeric
and definitional discrepancies it could not have caught, because it only checks
values it has been told about and only inside table BODIES. It never reads the
prose, the table legends, the figure legends, Box 1 or the Abstract, and it has
no way to notice that a number labelled a hazard ratio in one place is called a
p-value in another.

The Methods promise that "a separate audit script recomputes the quantities
quoted in the text from the tables they came from and reports any that
disagree". This is the part of that promise the value audit cannot keep.

WHAT IT CHECKS. Each module under src/audit/ exposes check(text, ctx) and
returns findings. Between them they cover the classes the review's own
consistency table was built from:

  coverage      numbers in table legends, figure legends, Box 1 and the Abstract
                that appear nowhere in the generated material -- and, worse, a
                legend number that contradicts the body of its own table
  identity      one number carrying two incompatible statistical labels, and
                units: an MPN floor printed as CFU, a dimensionless headroom
                given a concentration unit
  arithmetic    percentages against their own stated numerator and denominator,
                fold-changes against their own log difference, Benjamini-Hochberg
                thresholds against their own family size and rank, ranges against
                their stated span, intervals against the estimates they bracket
  consistency   claims the paper's own self-audit marks unsupported that are
                still asserted somewhere, sample sizes with no line in the flow
                account, cross-references that resolve to nothing, and a block
                of prose that says the same thing twice, which is what a
                paragraph looks like when the passage its rewrite replaced was
                never deleted

WHAT A FINDING MEANS. A high finding is a contradiction: two places in the
manuscript that cannot both be right. Those fail the run. Medium and low are
reported and do not, because some are legitimate conventions this script cannot
know about, and an audit that cries wolf gets switched off.

Writes results/receipts/manuscript_audit.json.
"""
from __future__ import annotations

import importlib
import json
import pkgutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "manuscript" / "PAPER_COMPLETE.md"
PROSE = ROOT / "manuscript" / "MANUSCRIPT.md"
TABLES = ROOT / "manuscript" / "tables.md"
ABSTRACT = ROOT / "manuscript" / "abstract.md"
RECEIPTS = ROOT / "results" / "receipts"

ORDER = {"high": 0, "medium": 1, "low": 2}


def load_checkers() -> list:
    """Every src/audit/check_*.py that exposes check(text, ctx)."""
    import src.audit as pkg

    out = []
    for mod in pkgutil.iter_modules(pkg.__path__):
        if not mod.name.startswith("check_"):
            continue
        m = importlib.import_module(f"src.audit.{mod.name}")
        if callable(getattr(m, "check", None)):
            out.append((mod.name, m))
        else:
            print(f"   ! {mod.name} has no check(); skipped")
    return sorted(out)


def main() -> int:
    if not PAPER.exists():
        print(f"missing {PAPER}; run src/assemble_paper.py first")
        return 1

    text = PAPER.read_text(encoding="utf-8")
    ctx = {
        "root": ROOT,
        "paper": text,
        "prose": PROSE.read_text(encoding="utf-8") if PROSE.exists() else "",
        "tables": TABLES.read_text(encoding="utf-8") if TABLES.exists() else "",
        "abstract": ABSTRACT.read_text(encoding="utf-8") if ABSTRACT.exists() else "",
    }

    checkers = load_checkers()
    if not checkers:
        print("no checkers found under src/audit/")
        return 1

    all_findings: list[dict] = []
    per_checker: dict[str, int] = {}
    for name, mod in checkers:
        try:
            found = list(mod.check(text, ctx) or [])
        except Exception as exc:                      # a broken checker is a finding
            found = [{"severity": "high", "kind": "checker-error", "where": name,
                      "detail": f"{type(exc).__name__}: {exc}"}]
        for f in found:
            f.setdefault("severity", "low")
            f["checker"] = name
        per_checker[name] = len(found)
        all_findings.extend(found)

    all_findings.sort(key=lambda f: (ORDER.get(f["severity"], 3), f["checker"]))
    counts = {s: sum(1 for f in all_findings if f["severity"] == s)
              for s in ("high", "medium", "low")}

    print(f"\n-- manuscript audit: {len(checkers)} checkers over "
          f"{len(text.split()):,} words --")
    for name, n in sorted(per_checker.items()):
        print(f"   {name:22} {n:3d} finding{'' if n == 1 else 's'}")

    if all_findings:
        print()
        for f in all_findings:
            head = f"[{f['severity']:6}] {f.get('kind', '?')}  @ {f.get('where', '?')}"
            print(f"   {head}")
            print(f"            {f.get('detail', '')}")
            if f.get("expected") is not None or f.get("found") is not None:
                print(f"            expected {f.get('expected')!r}, "
                      f"found {f.get('found')!r}")

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    (RECEIPTS / "manuscript_audit.json").write_text(json.dumps({
        "script": "src/audit_manuscript.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "checkers": [n for n, _ in checkers],
        "n_words_audited": len(text.split()),
        "counts": counts,
        "findings": all_findings,
    }, indent=2, default=str), encoding="utf-8")

    print(f"\n   {counts['high']} high, {counts['medium']} medium, "
          f"{counts['low']} low")
    if counts["high"]:
        print("   a high finding is a contradiction between two places in the "
              "manuscript; both cannot be right")
        return 1
    print("   no contradictions found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
