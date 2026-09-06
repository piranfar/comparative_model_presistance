"""
Assemble the complete paper into one document.

Run:  python -m src.assemble_paper

The paper lives in pieces on purpose: prose in one file, tables generated from
the results by src/build_tables.py, figures rendered from the results by the
scripts in src/figures/. That keeps every number tied to the analysis that
produced it, but it means there is no single thing to read. This script builds
that single thing.

Tables are spliced in at the point they are first cited, so the reader meets
each one where the text needs it rather than in an appendix. Figures are
embedded by relative path, which renders in any markdown viewer and survives the
conversion to Word.

What is deliberately still missing is listed at the end of the assembled file
rather than left for the reader to discover: the reference list, which is held
back until the text stops moving, and the author declarations.

Writes:
  manuscript/PAPER_COMPLETE.md
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODY = ROOT / "manuscript" / "RATE_VS_DURATION.md"
TABLES = ROOT / "manuscript" / "tables.md"
ABSTRACT = ROOT / "manuscript" / "abstract.md"
FIGDIR = ROOT / "results" / "figures"
OUT = ROOT / "manuscript" / "PAPER_COMPLETE.md"

FIGURES = {
    1: "fig14_dynamic_range",
    2: "fig10_rate_vs_duration",
    3: "fig11_endpoint_collapse",
    4: "fig12_independence",
    # fig13_parameter_transfer belongs to the published-rate-constant comparison,
    # which is no longer part of this paper. The figure stays in results/ as a
    # record of the work; it is neither embedded nor listed as supplementary.
}


def split_tables(text: str) -> dict[int, str]:
    """Split tables.md into {number: markdown block}."""
    out = {}
    parts = re.split(r"(?=\*\*Table \d+\.)", text)
    for part in parts:
        m = re.match(r"\*\*Table (\d+)\.", part.strip())
        if m:
            out[int(m.group(1))] = part.strip()
    return out


def first_citation_positions(body: str, n_tables: int) -> dict[int, int]:
    """Where to place each table: after the paragraph that first uses it.

    A table named in Methods before its data is discussed is a forward
    reference, not the place a reader wants the table. Table 4 is named in the
    admissibility rule in Section 2.3 and again in Section 3.6 where its values
    are reported; the second is where it belongs. So a citation at or after the
    Results heading wins, and a citation anywhere is the fallback for a table
    the Results never name.
    """
    results_at = body.find("## 3. Results")
    pos = {}
    for n in range(1, n_tables + 1):
        hits = list(re.finditer(rf"Table {n}\b", body))
        if not hits:
            continue
        in_results = [m for m in hits if results_at >= 0 and m.start() > results_at]
        m = in_results[0] if in_results else hits[0]
        end = body.find("\n\n", m.end())
        pos[n] = end if end > 0 else len(body)
    return pos


def main() -> int:
    if not BODY.exists():
        raise SystemExit(f"missing {BODY}")
    body = BODY.read_text(encoding="utf-8")
    tables = split_tables(TABLES.read_text(encoding="utf-8")) if TABLES.exists() else {}

    # The body opens with YAML front matter for the submission version, so the
    # head is three things rather than one: the front matter block, the H1
    # title, and the author block under it. The abstract belongs after all of
    # them. Splitting on the first newline put it after a bare "---".
    front = ""
    if body.startswith("---\n"):
        end = body.index("\n---\n", 4) + len("\n---\n")
        front, body = body[:end].rstrip(), body[end:].lstrip("\n")
    head, rest = body.split("\n\n---\n\n", 1)
    title = (front + "\n\n" + head).strip() if front else head.strip()

    # ---- abstract, if one has been written -------------------------------
    abstract = ABSTRACT.read_text(encoding="utf-8").strip() if ABSTRACT.exists() else ""

    # ---- splice each table in after the paragraph that first cites it ----
    positions = first_citation_positions(rest, max(tables) if tables else 0)
    # Splice by descending POSITION, not descending table number. Table 4 sits
    # earlier in the text than Table 2, so inserting in numeric order shifts
    # every position after the one just used and the later tables land adrift.
    for n, at in sorted(positions.items(), key=lambda kv: kv[1], reverse=True):
        if n not in tables:
            continue
        block = "\n\n" + tables[n] + "\n"
        rest = rest[:at] + block + rest[at:]

    # ---- embed each figure just before its caption ------------------------
    def embed(m):
        n = int(m.group(1))
        stem = FIGURES.get(n)
        if not stem or not (FIGDIR / f"{stem}.png").exists():
            return m.group(0)
        rel = f"../results/figures/{stem}.png"
        return f"![Figure {n}]({rel})\n\n{m.group(0)}"

    rest = re.sub(r"\*\*Figure (\d)\. ", lambda m: embed(m), rest)

    missing = []
    if not abstract:
        missing.append("the abstract")
    if "## References" not in rest:
        missing.append("the reference list, deliberately held back until the "
                       "text stops moving")
    if "Declarations" not in rest and "Statements" not in rest:
        missing.append("the author declarations: funding, competing interests, "
                       "author contributions, and the archived commit for the "
                       "submitted version")

    parts = [title, ""]
    if abstract:
        parts += [abstract, ""]
    parts += [rest.rstrip(), ""]
    if missing:
        parts += ["---", "",
                  "## Still to be added",
                  "",
                  "Listed here rather than left to be discovered:", ""]
        parts += [f"{i}. {m.capitalize()}." for i, m in enumerate(missing, 1)]
        parts += [""]

    OUT.write_text("\n".join(parts), encoding="utf-8")

    text = OUT.read_text(encoding="utf-8")
    n_words = len(text.split())
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"   {n_words:,} words")
    print(f"   abstract: {'yes' if abstract else 'NOT WRITTEN'}")
    print(f"   tables spliced in at first citation: "
          f"{sorted(n for n in positions if n in tables)}")
    print(f"   figures embedded: "
          f"{[n for n in FIGURES if (FIGDIR / (FIGURES[n] + '.png')).exists()]}")
    for m in missing:
        print(f"   STILL MISSING: {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
