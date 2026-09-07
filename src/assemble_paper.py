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
    1: "fig1_dynamic_range",
    2: "fig2_rate_vs_duration",
    3: "fig3_endpoint_collapse",
    4: "fig4_independence",
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
    # The supplementary block is a trailing section of tables.md. It has to be
    # separated before splitting, or it rides along with whichever numbered table
    # happens to come last and is spliced into the middle of a Results section.
    tables_md = TABLES.read_text(encoding="utf-8") if TABLES.exists() else ""
    supplementary = ""
    marker = "\n## Supplementary tables"
    if marker in tables_md:
        i = tables_md.index(marker)
        tables_md, supplementary = tables_md[:i], tables_md[i:].strip()
    tables = split_tables(tables_md)

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
    # The numbering and the placement were computed by different rules, and it
    # showed: tables are numbered on first citation ANYWHERE, while the splice
    # above prefers a citation inside the Results. Table 5's first Results
    # citation precedes Table 4's, so Table 5's body was laid out first and a
    # reader following the text met them in reverse order. Forcing the splice
    # positions to be non-decreasing in table number makes the body order match
    # the numbering by construction. A table can then sit a paragraph or two
    # after the sentence that first cites it, which is ordinary; sitting BEFORE
    # it is not.
    running = -1
    for n in sorted(positions):
        running = positions[n] = max(positions[n], running)

    # Splice by descending POSITION, not descending table number. Table 4 sits
    # earlier in the text than Table 2, so inserting in numeric order shifts
    # every position after the one just used and the later tables land adrift.
    # Ties are now common, since clamping creates them; within a tie the higher
    # number goes in first so the lower one ends up above it.
    for n, at in sorted(positions.items(),
                        key=lambda kv: (kv[1], kv[0]), reverse=True):
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
    # AAC carries funding, competing interests and contributor roles inside
    # Acknowledgments, unheaded, rather than under a Declarations heading of
    # their own -- so that is the section to check for.
    if "## Acknowledgments" not in rest:
        missing.append("the Acknowledgments section, which is where AAC carries "
                       "funding, competing interests and contributor roles")
    for phrase, what in (("no specific grant", "the funding statement"),
                         ("competing interests", "the competing-interests statement")):
        if phrase not in rest:
            missing.append(what)

    parts = [title, ""]
    if abstract:
        parts += [abstract, ""]
    parts += [rest.rstrip(), ""]
    if supplementary:
        parts += ["---", "", supplementary, ""]
    if missing:
        parts += ["---", "",
                  "## Still to be added",
                  "",
                  "Listed here rather than left to be discovered:", ""]
        parts += [f"{i}. {m.capitalize()}." for i, m in enumerate(missing, 1)]
        parts += [""]

    text = "\n".join(parts)

    # ---- citation-sequence numbering, done last --------------------------
    # AAC numbers references in order of first citation. The sources carry keys
    # ([[R12]]), never numbers, so that moving a paragraph cannot leave a stale
    # number behind. The numbering therefore has to happen HERE, on the finished
    # document: the tables are spliced in above, and a table legend that cites a
    # source changes the order. Doing it in the source files would number them in
    # the order the files happen to be read.
    n_refs = 0
    try:
        from src.build_references import load_bib, substitute, build_list
        bib = load_bib()
        text, order = substitute(text, bib)
        n_refs = len(order)
        refs = build_list(order, bib)
        if "## References" in text:
            head, _, tail = text.partition("## References")
            nxt = tail.find("\n## ")
            text = head + refs.rstrip() + "\n" + (tail[nxt:] if nxt >= 0 else "")
        else:
            text += "\n" + refs
    except SystemExit as exc:
        print(f"   ! references not numbered: {exc}")
    except ImportError:
        print("   ! src/build_references.py not importable; keys left in place")

    OUT.write_text(text, encoding="utf-8")

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
