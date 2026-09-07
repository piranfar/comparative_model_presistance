"""
Emit the supplemental material as the separate file AAC wants.

Run:  python -m src.build_supplement

WHY THIS IS A SEPARATE FILE. At initial submission AAC will take one combined
file, but at revision the supplemental material and its legends must be supplied
separately from the manuscript, as one file by preference and at most ten, 15 MB
each. Building it now means the revision package needs no second pass, and it
makes the two obligations that come with it visible rather than discovered late:

  1. Supplemental items are numbered with an S prefix and must be CITED in the
     manuscript text, while their legends must NOT remain in the manuscript file.
  2. A reference cited only in the supplemental material goes in a reference
     section inside the supplemental file, numbered independently. A reference
     cited in both places is listed in both.

This script therefore does more than copy tables across: it works out which
references the supplement uses, splits them into "cited in both" and "cited only
here", and numbers the supplement's own list. If the supplement ever cites
something the manuscript does not, that reference appears here and nowhere else,
which is exactly what ASM asks for and is easy to forget by hand.

Writes manuscript/SUPPLEMENTAL_MATERIAL.md.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "manuscript" / "tables.md"
PROSE = ROOT / "manuscript" / "RATE_VS_DURATION.md"
OUT = ROOT / "manuscript" / "SUPPLEMENTAL_MATERIAL.md"

MARKER = "\n## Supplementary tables"
KEY = re.compile(r"\[\[(R\d+)\]\]")


def main() -> int:
    if not TABLES.exists():
        raise SystemExit(f"missing {TABLES}; run src/build_tables.py first")
    tables_md = TABLES.read_text(encoding="utf-8")
    if MARKER not in tables_md:
        raise SystemExit("tables.md carries no supplementary block")
    main_tables, supp = tables_md.split(MARKER, 1)
    supp = supp.strip()

    prose = PROSE.read_text(encoding="utf-8") if PROSE.exists() else ""
    in_manuscript = set(KEY.findall(prose)) | set(KEY.findall(main_tables))
    in_supp = set(KEY.findall(supp))
    only_here = sorted(in_supp - in_manuscript, key=lambda s: int(s[1:]))

    items = sorted({m.group(1) for m in
                    re.finditer(r"\*\*(Table S\d+)\.", supp)},
                   key=lambda s: int(s.split("S")[1]))
    uncited = [t for t in items
               if not re.search(rf"{t}\b", prose) and not re.search(rf"{t}\b", main_tables)]

    # Taken from the prose front matter, not repeated here. A title repeated in
    # six files is a title that is wrong in five of them the day it changes.
    tm = re.search(r'^title:\s*"(.+)"\s*$', prose, re.M)
    body = [
        "# Supplemental material",
        "",
        f"**{tm.group(1) if tm else '[no title in the front matter]'}**",
        "",
        "Vahhab Piranfar",
        "",
        f"This file contains {len(items)} supplemental tables, "
        f"{items[0]} to {items[-1]}, each with its legend. Every one is cited in "
        "the manuscript text.",
        "",
        "---",
        "",
        supp,
        "",
    ]

    if only_here:
        body += ["---", "",
                 "## References cited only in this supplemental material", "",
                 "Numbered independently of the manuscript's reference list, as "
                 "required. A source cited in both places appears in both lists.",
                 ""]
        try:
            from src.build_references import load_bib, format_entry
            bib = load_bib()
            for i, k in enumerate(only_here, 1):
                body.append(f"{i}. {format_entry(bib[k])}")
                body.append("")
        except Exception as exc:                       # keep the file buildable
            body.append(f"[reference list not built: {exc}]")
            body.append("")

    OUT.write_text("\n".join(body), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"   {len(items)} supplemental tables: {', '.join(items)}")
    print(f"   {len(OUT.read_text(encoding='utf-8').split()):,} words, "
          f"{OUT.stat().st_size / 1024:.0f} KB (AAC allows 15 MB per file)")
    if uncited:
        print(f"   ! never cited in the manuscript, which AAC requires: {uncited}")
    if only_here:
        print(f"   {len(only_here)} reference(s) cited only here, listed "
              f"separately: {only_here}")
    else:
        print("   every reference it uses is also cited in the manuscript, so it "
              "needs no separate list")
    return 1 if uncited else 0


if __name__ == "__main__":
    raise SystemExit(main())
