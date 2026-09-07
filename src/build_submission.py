"""
Split the paper into the two files a journal actually wants.

Run:  python -m src.build_submission

WHY THIS EXISTS. The manuscript is one document of about 30,000 words with 15
numbered tables. No journal takes that as a research article. What every journal
does take is a short main text plus a supplemental file, and the split is not a
matter of deleting: a section that moves out of the main text takes its tables,
its figures and its cross-references with it, and everything that stays behind
has to be renumbered to close the gaps.

That renumbering is where this project has made its mistakes. Moving one table
to the supplement left a bare "16" in a list, a stale count in the front matter
and a legend pointing at the wrong table -- three errors from one edit, all
found by the checkers rather than by reading. So the split is done here, by a
program, from one routing table that a human can read in thirty seconds.

WHAT IS NOT TOUCHED. manuscript/PAPER_COMPLETE.md stays the complete document
and stays the thing the audit pipeline verifies. Every claim in this paper is
checked against the assembled long form, and it would be a poor trade to shorten
the paper by removing the text the checkers read. The submission files are a
DERIVED VIEW: this script reads the same prose and emits a main text and a
supplement, and if the two ever disagree it is because this script is wrong, not
because two documents drifted.

Writes:
  manuscript/SUBMISSION_MAIN.md
  manuscript/SUBMISSION_SUPPLEMENT.md
  manuscript/submission_routing.csv   what moved where, for the cover letter
"""
from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSE = ROOT / "manuscript" / "RATE_VS_DURATION.md"
TABLES = ROOT / "manuscript" / "tables.md"
ABSTRACT = ROOT / "manuscript" / "abstract.md"
MAIN_OUT = ROOT / "manuscript" / "SUBMISSION_MAIN.md"
SUPP_OUT = ROOT / "manuscript" / "SUBMISSION_SUPPLEMENT.md"
ROUTING_OUT = ROOT / "manuscript" / "submission_routing.csv"

# --------------------------------------------------------------------------
# THE ROUTING TABLE. This is the whole editorial decision, in one place.
#
# A Results section stays in the main text if the paper's claim is unsupported
# without it. Everything else is evidence a referee may want and a reader may
# not: it goes to the supplement, where it is still published, still citable and
# still checked, but does not spend a word of the main text's budget.
#
# The rule applied here: keep what establishes the two boundaries, what shows
# them changing a published conclusion, and the one prospective test. Move the
# corroborations, the secondary deposits and every methodological defence.
# --------------------------------------------------------------------------
MAIN = "main"
SUPP = "supplement"

RESULTS_ROUTE = {
    1:  (MAIN, "the boundary itself; without it there is no paper"),
    2:  (MAIN, "the boundary changing a published label -- the core claim"),
    3:  (MAIN, "the affected isolates are identified before treatment; short "
               "and load-bearing"),
    4:  (MAIN, "what the phenotype tracks instead, and the mediation the "
               "referee attacked; longest section, cut hard rather than moved"),
    5:  (MAIN, "six laboratories, one protocol -- the generality argument"),
    6:  (SUPP, "corroboration: the turbidity standard fixes the inoculum, not "
               "the resolvable depth. Supports Section 5, does not extend it"),
    7:  (SUPP, "the inversion decomposition; a consequence of the boundary "
               "rather than evidence for it"),
    8:  (MAIN, "the only prospective data in the paper"),
    9:  (MAIN, "the shortest and most concrete demonstration of the cost"),
    10: (SUPP, "resistance and tolerance as separate axes; this is the prior "
               "literature's claim, not this paper's finding"),
    11: (MAIN, "one culture, two plated volumes, two labels -- the boundary "
               "made experimental"),
}

# Methods: the main text keeps a condensed account, written by hand in
# manuscript/methods_condensed.md; the full account moves wholesale. Anything
# not named here defaults to the supplement, so a new Methods subsection is
# moved unless someone deliberately keeps it.
METHODS_KEEP_IN_MAIN = {
    "Ethics",
    "Use of generative artificial intelligence",
    "Data availability",
}

# Discussion subsections are merged into a running Discussion in the main text;
# none moves, because a Discussion split across two files cannot be read.
#
# TABLES. A table is a main table only if it is named here. Everything else is
# supplementary even where the main text cites it -- and the main text should go
# on citing it, because a supplemental table nobody cites is a supplemental
# table nobody reads, and most journals will not accept one.
#
# Three is close to the ceiling once four figures are counted. The three kept
# are the ones a reader cannot follow the argument without: what was reanalysed,
# what each endpoint costs in headroom, and the isolates whose identical
# floor-level readings carry different labels. Every other table answers a
# question a referee will ask rather than a question the argument raises.
KEEP_AS_MAIN_TABLE = {"1", "3", "6"}
# --------------------------------------------------------------------------

# A paragraph carrying this marker leaves the article and lands in the
# supplement, under a heading naming the section it came from. Shortening a
# manuscript by deleting is irreversible and loses the answer to the referee who
# asks the question the deleted paragraph answered; marking moves it somewhere
# it is still published, still numbered and still cited. The marker sits at the
# end of the paragraph so it never interrupts a sentence being read in the
# source file.
SUPP_MARK = re.compile(r"\s*<!--\s*supp\s*-->\s*$", re.M)
COUNTS = re.compile(r"^\*\*Figures:\*\*.*$", re.M)
HEAD3 = re.compile(r"^### (.*)$", re.M)
HEAD2 = re.compile(r"^## (.*)$", re.M)
TABLE_REF = re.compile(r"\bTable (S?\d+)\b")
FIG_REF = re.compile(r"\b(?:Fig\.|Figure) (S?\d+)\b")
SECTION_REF = re.compile(r"\bSection (\d+)\b")


@dataclass
class Section:
    """One `### ` subsection of the prose, with where it is going."""
    parent: str                 # the `## ` heading it sits under
    number: int | None          # the leading integer of a numbered Results head
    title: str                  # heading text with any leading number stripped
    body: str
    dest: str = MAIN
    why: str = ""
    new_label: str = ""         # "3" in the main text, "S2" in the supplement
    deferred: list[str] = field(default_factory=list)   # marked paragraphs

    @property
    def words(self) -> int:
        return len(self.body.split())

    # A paragraph that opens by pointing backwards cannot follow a paragraph
    # that has just been removed. This is the one failure mode paragraph-level
    # deferral creates that section-level routing does not, and it is invisible
    # in a diff: the article still reads as English, it just refers to something
    # that is no longer there. The first version of the Section 4 cut left
    # "Restricted to it, the two surviving associations part company" with no
    # antecedent, because the paragraph defining the stratum had gone.
    # Deliberately narrow: a BARE pronoun or demonstrative, one with no noun of
    # its own. "These 217 isolates" and "That last objection" carry their
    # antecedent with them and survive a deletion above; "Restricted to it" and
    # "They do not" do not. A wider pattern was tried first and fired on three
    # paragraphs, two of which were fine -- and a check that cries wolf twice
    # for every catch is a check that gets ignored on the day it is right.
    _VERB = (r"(?:is|are|was|were|does|do|did|has|have|had|will|would|can|"
             r"could|holds?|fails?|follows?|sits?|shows?|leaves?|gives?|"
             r"remains?|stands?)")
    ANAPHORA = re.compile(
        r"^\s*(?:"
        r"Restricted to (?:it|that|them|those)\b"
        r"|(?:It|They|Both|Either|Neither|Such|This|That|These|Those)\s+"
        + _VERB + r"\b"
        r"|The (?:other|second|remaining) (?:two|three|four|one)\b"
        r")", re.I)

    def defer_marked(self, problems: list[str]) -> None:
        """Pull the marked paragraphs out of the body and hold them aside.

        Only meaningful for a section that stays in the article; a section that
        moves wholesale takes its marked paragraphs with it, and splitting them
        out again would scatter one argument across two places in one file.
        """
        if self.dest != MAIN:
            return
        keep, moved, prev_deferred = [], [], False
        for para in re.split(r"\n{2,}", self.body.strip()):
            if SUPP_MARK.search(para):
                moved.append(SUPP_MARK.sub("", para).rstrip())
                prev_deferred = True
                continue
            if prev_deferred and self.ANAPHORA.match(para):
                problems.append(
                    f"{self.parent} / {self.title[:40]}: a deferred paragraph is "
                    f"followed by one that points back at it -- "
                    f"“{' '.join(para.split()[:7])}...” has lost its "
                    f"antecedent")
            prev_deferred = False
            keep.append(para)
        self.body = "\n\n".join(keep) + "\n"
        self.deferred = moved


def split_sections(prose: str) -> tuple[str, list[Section], dict[str, str]]:
    """Split the prose into front matter, `### ` sections, and `## ` preambles.

    A `## ` section may carry text of its own before its first `### ` -- the
    Introduction is entirely such text, and Results opens with Box 1. That text
    is kept per parent heading rather than folded into the first subsection,
    because Box 1 is not part of Section 1 and must not travel with it.
    """
    parts = HEAD2.split(prose)
    front = parts[0]
    preambles: dict[str, str] = {}
    sections: list[Section] = []
    for i in range(1, len(parts), 2):
        parent, body = parts[i].strip(), parts[i + 1]
        sub = HEAD3.split(body)
        preambles[parent] = sub[0]
        for j in range(1, len(sub), 2):
            head, text = sub[j].strip(), sub[j + 1]
            m = re.match(r"^(\d+)\.\s+(.*)$", head)
            num = int(m.group(1)) if m else None
            title = m.group(2) if m else head
            sections.append(Section(parent, num, title, text.rstrip() + "\n"))
    return front, sections, preambles


def route(sections: list[Section]) -> None:
    """Apply the routing table. Mutates in place; every section gets a reason."""
    for s in sections:
        if s.parent == "Results":
            dest, why = RESULTS_ROUTE.get(
                s.number, (SUPP, "not in the routing table, so moved by default"))
            s.dest, s.why = dest, why
        elif s.parent == "Materials and Methods":
            if s.title in METHODS_KEEP_IN_MAIN:
                s.dest, s.why = MAIN, "a declaration the journal requires in the article"
            else:
                s.dest, s.why = SUPP, "detailed methods move wholesale"
        else:
            s.dest, s.why = MAIN, "part of the argument, not the evidence"


def assign_labels(sections: list[Section]) -> dict[int, str]:
    """Number the surviving Results sections, and the moved ones as Text S-n.

    Returns the map from OLD Results number to its new label, which is what the
    cross-reference rewriter needs.
    """
    remap: dict[int, str] = {}
    n_main = n_supp = 0
    for s in sections:
        if s.parent != "Results" or s.number is None:
            continue
        if s.dest == MAIN:
            n_main += 1
            s.new_label = str(n_main)
        else:
            n_supp += 1
            s.new_label = f"S{n_supp}"
        remap[s.number] = s.new_label
    return remap


def rewrite_section_refs(text: str, remap: dict[int, str], where: str,
                         problems: list[str]) -> str:
    """Rewrite `Section N` to its new number, or to `Text S-n` if it moved.

    A cross-reference to a section that is now in the supplement must not stay a
    bare number: "Section 6" in the main text would point at a section the
    reader cannot see. It becomes "Text S2" and reads as the pointer it is.
    """
    def sub(m: re.Match) -> str:
        old = int(m.group(1))
        new = remap.get(old)
        if new is None:
            problems.append(f"{where}: 'Section {old}' has no section {old}")
            return m.group(0)
        return f"Text S{new[1:]}" if new.startswith("S") else f"Section {new}"
    return SECTION_REF.sub(sub, text)


def split_tables(tables_md: str) -> tuple[dict[str, str], list[str]]:
    """Split tables.md into {label: block} keyed by '7' or 'S3', in file order.

    Each block is trimmed at the first structural break after its own content.
    Splitting on the NEXT table alone makes the last table before a heading
    swallow that heading: the original Table 15 arrived carrying the whole
    "## Supplementary tables" heading and its preamble, so the built supplement
    had that heading twice, once in the middle of a table. A rule or a heading
    at the start of a line ends the block; a `|---|` row inside a table body
    does not, because it starts with a pipe.
    """
    blocks: dict[str, str] = {}
    order: list[str] = []
    for part in re.split(r"(?=^\*\*Table S?\d+\.)", tables_md, flags=re.M):
        m = re.match(r"\*\*Table (S?\d+)\.", part.strip())
        if not m:
            continue
        cut = re.search(r"^(?:-{3,}\s*|#{1,6} .*)$", part, re.M)
        blocks[m.group(1)] = part[:cut.start()].strip() if cut else part.strip()
        order.append(m.group(1))
    return blocks, order


def renumber_tables(main_text: str, supp_text: str,
                    blocks: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """Number the kept tables, then everything else, in citation order.

    Membership of the main text is the routing decision above; ORDER is taken
    from the text, because a table's number should rise as the reader meets it
    and no hand-maintained list survives a section moving. So the two are
    separated: KEEP_AS_MAIN_TABLE says which, the citations say in what order.

    Supplementary tables are numbered by where the main text first cites them,
    falling back to the supplement's own order and then to file order for any
    table nobody cites -- which the check below then reports rather than
    tolerating.
    """
    problems: list[str] = []
    main_hits = [m.group(1) for m in TABLE_REF.finditer(main_text)]
    supp_hits = [m.group(1) for m in TABLE_REF.finditer(supp_text)]

    remap: dict[str, str] = {}
    n = 0
    for lab in main_hits:
        if lab in remap or lab not in KEEP_AS_MAIN_TABLE or lab not in blocks:
            continue
        n += 1
        remap[lab] = str(n)
    for lab in sorted(KEEP_AS_MAIN_TABLE - set(remap)):
        problems.append(f"Table {lab} is kept as a main table but the main text "
                        f"never cites it")
    sn = 0
    for lab in main_hits + supp_hits + list(blocks):
        if lab in remap or lab not in blocks:
            continue
        sn += 1
        remap[lab] = f"S{sn}"

    for lab in set(main_hits + supp_hits) - set(blocks):
        problems.append(f"cited 'Table {lab}' but tables.md has no such table")
    return remap, problems


def apply_table_remap(text: str, remap: dict[str, str]) -> str:
    """Rewrite every `Table X` through the map, in one pass.

    One pass with a placeholder is not optional here. Rewriting 6->5 and then
    5->4 in sequence turns the original Table 6 into Table 4, which is the class
    of error that put a bare wrong number in a list the last time tables moved.
    """
    def sub(m: re.Match) -> str:
        new = remap.get(m.group(1))
        return m.group(0) if new is None else f"Table {new}"
    return TABLE_REF.sub(sub, text)


def check(main: str, supp: str, table_remap: dict[str, str],
          problems: list[str]) -> None:
    """The obligations a journal imposes, checked rather than remembered."""
    # 1. Every supplemental item must be cited in the manuscript text.
    for old, new in table_remap.items():
        if not new.startswith("S"):
            continue
        if not re.search(rf"Table {new}\b", main):
            problems.append(
                f"Table {new} is supplemental but the main text never cites it; "
                "journals require every supplemental item to be cited in the article")
    # 2. Nothing in the main text may point at a table that is not there.
    for m in TABLE_REF.finditer(main):
        lab = m.group(1)
        if lab.startswith("S"):
            continue
        if not re.search(rf"^\*\*Table {lab}\.", main, re.M):
            problems.append(f"main text cites Table {lab}, which is not in the main file")
    # 3. A supplement that cites a main table is fine; a main text that cites a
    #    section number that no longer exists is not, and is caught upstream.
    # 3b. A heading may appear once. Two "## Supplementary tables" headings is
    #     what a table block swallowing the heading after it looks like from
    #     the outside, and it is invisible unless counted.
    for doc, name in ((main, "article"), (supp, "supplement")):
        seen: dict[str, int] = {}
        for h in re.findall(r"^#{2,3} (.+)$", doc, re.M):
            seen[h.strip()] = seen.get(h.strip(), 0) + 1
        for h, n in seen.items():
            if n > 1:
                problems.append(f"the {name} carries the heading '{h}' {n} times")
    # 4. A display item in the article must not rest on an analysis that left
    #    it. Figure 2's panel D plots a descriptive Cox model; deferring the
    #    paragraph that reported that model put the panel in the article and
    #    its explanation in the supplement, which is not a thing a reader can
    #    follow. Detected by vocabulary rather than by semantics: if a named
    #    method appears in an article legend and nowhere in the article's own
    #    Results or Methods, the text that carried it has gone.
    METHODS_VOCAB = ("Cox", "Tobit", "Turnbull", "Kaplan", "Brant",
                     "proportional odds", "proportional-odds", "mediation",
                     "cluster bootstrap", "permutation", "Benjamini")
    LEGEND = re.compile(r"^\*\*(?:Fig\.|Figure|Table) \d+\..*?(?=\n\n|\Z)",
                        re.M | re.S)
    legends = "\n".join(m.group(0) for m in LEGEND.finditer(main))
    # Cut each legend out where it sits. Joining them into one string and
    # calling replace() removes nothing, because the joined string appears
    # nowhere in the document -- which is how the first version of this check
    # passed silently on the case it was written for.
    body_only = LEGEND.sub("", main)
    for term in METHODS_VOCAB:
        if re.search(rf"\b{re.escape(term)}", legends, re.I) and \
                not re.search(rf"\b{re.escape(term)}", body_only, re.I):
            problems.append(
                f"an article legend names '{term}' but no text in the article "
                f"does; the paragraph that explained it has moved to the "
                f"supplement, leaving the display item unsupported")
    # 5. Figures: the main text must not cite a figure it does not carry.
    for m in FIG_REF.finditer(main):
        lab = m.group(1)
        if lab.startswith("S"):
            continue
        if not re.search(rf"^\*\*(?:Fig\.|Figure) {lab}\.", main, re.M):
            problems.append(f"main text cites Fig. {lab} with no legend in the main file")


def main() -> int:
    if not PROSE.exists():
        raise SystemExit(f"missing {PROSE}")
    prose = PROSE.read_text(encoding="utf-8")
    tables_md = TABLES.read_text(encoding="utf-8") if TABLES.exists() else ""
    blocks, _ = split_tables(tables_md)

    front, sections, preambles = split_sections(prose)
    route(sections)
    remap_sec = assign_labels(sections)
    problems: list[str] = []
    for s in sections:
        s.defer_marked(problems)

    # ---- assemble the two bodies -------------------------------------
    def gather(dest: str, parent: str) -> list[Section]:
        return [s for s in sections if s.dest == dest and s.parent == parent]

    main_parts = [front.rstrip(), ""]
    main_parts += ["## Introduction", "", preambles.get("Introduction", "").strip(), ""]
    main_parts += ["## Results", "", preambles.get("Results", "").strip(), ""]
    for s in gather(MAIN, "Results"):
        main_parts += [f"### {s.new_label}. {s.title}", "", s.body.strip(), ""]
    main_parts += ["## Discussion", "", preambles.get("Discussion", "").strip(), ""]
    for s in gather(MAIN, "Discussion"):
        main_parts += [f"### {s.title}", "", s.body.strip(), ""]
    main_parts += ["## Materials and Methods", "",
                   "*The condensed account. The full account, with every "
                   "estimator and every sensitivity analysis, is Supplementary "
                   "Methods in the supplemental file.*", ""]
    for s in gather(MAIN, "Materials and Methods"):
        main_parts += [f"### {s.title}", "", s.body.strip(), ""]
    # "References" is skipped: the prose file carries an empty placeholder
    # heading, and the numbered list is generated below from this file's own
    # citation order. Emitting the placeholder too would put an empty References
    # section above the real one.
    for parent in ("Acknowledgments", "Figure legends"):
        if parent in preambles:
            main_parts += [f"## {parent}", "", preambles[parent].strip(), ""]

    # Read the title rather than repeating it. It was hard-coded in six files,
    # and retargeting the manuscript to a different journal changed it in one.
    m = re.search(r'^title:\s*"(.+)"\s*$', prose, re.M)
    title = m.group(1) if m else "[no title in the front matter]"
    supp_parts = ["# Supplemental material", "", f"**{title}**", "",
                  "Vahhab Piranfar", "", "---", ""]
    moved_results = gather(SUPP, "Results")
    deferred = [s for s in sections if s.deferred]
    if moved_results or deferred:
        supp_parts += ["## Supplementary text", ""]
        for s in moved_results:
            supp_parts += [f"### Text {s.new_label}. {s.title}", "",
                           s.body.strip(), ""]
        for s in deferred:
            where = (f"Section {s.new_label}" if s.parent == "Results"
                     and s.new_label else s.parent)
            supp_parts += [f"### Extended results for {where}: {s.title}", "",
                           "*Material held back from the article for length. It "
                           "is reported here rather than dropped, because each "
                           "paragraph answers a question a reader of that "
                           "section may reasonably ask.*", ""]
            supp_parts += ["\n\n".join(s.deferred), ""]
    supp_parts += ["## Supplementary methods", ""]
    for s in gather(SUPP, "Materials and Methods"):
        supp_parts += [f"### {s.title}", "", s.body.strip(), ""]

    main_text = "\n".join(main_parts)
    supp_text = "\n".join(supp_parts)

    # ---- rewrite the cross-references --------------------------------
    main_text = rewrite_section_refs(main_text, remap_sec, "main", problems)
    supp_text = rewrite_section_refs(supp_text, remap_sec, "supplement", problems)

    table_remap, tp = renumber_tables(main_text, supp_text, blocks)
    problems += tp
    main_text = apply_table_remap(main_text, table_remap)
    supp_text = apply_table_remap(supp_text, table_remap)

    # A supplemental table the article never names is one the journal will
    # query and the reader will never open. Where a table lost its citation
    # because the section that cited it moved, the main text says so here
    # rather than pretending the citation is still in the Results.
    supp_labels = sorted((v for v in table_remap.values() if v.startswith("S")),
                         key=lambda s: int(s[1:]))
    orphans = [s for s in supp_labels if not re.search(rf"Table {s}\b", main_text)]
    if orphans:
        named = ", ".join(f"Table {s}" for s in orphans[:-1])
        named = f"{named} and Table {orphans[-1]}" if len(orphans) > 1 \
            else f"Table {orphans[0]}"
        main_text += (
            "\n\n## Supplemental material\n\n"
            "The supplemental file carries the full Materials and Methods, the "
            f"analyses named above as supplementary text, and {len(supp_labels)} "
            f"supplemental tables. {named} support analyses reported there "
            "rather than in this article, and are listed so that every "
            "supplemental item is named in the manuscript.\n")

    # ---- place the table blocks --------------------------------------
    main_tabs, supp_tabs = [], []
    for old, new in sorted(table_remap.items(),
                           key=lambda kv: (kv[1].startswith("S"),
                                           int(kv[1].lstrip("S")))):
        block = apply_table_remap(blocks[old], table_remap)
        block = rewrite_section_refs(block, remap_sec, f"Table {new}", problems)
        (supp_tabs if new.startswith("S") else main_tabs).append(block)
    if main_tabs:
        main_text += "\n\n## Tables\n\n" + "\n\n".join(main_tabs) + "\n"
    if supp_tabs:
        supp_text += "\n\n## Supplementary tables\n\n" + "\n\n".join(supp_tabs) + "\n"

    # ---- the abstract, and an honest count of the display items -------
    # Both are things a reader meets before anything else and a journal checks
    # first. The prose file's own count describes the long document and is
    # simply wrong here: the article carries three tables, not fifteen.
    n_figs = len({s for s in FIG_REF.findall(main_text) if not s.startswith("S")})
    main_text = COUNTS.sub(
        f"**Figures:** {n_figs} | **Tables:** {len(main_tabs)} | "
        f"**Boxes:** 1 | **Supplemental tables:** {len(supp_tabs)}",
        main_text, count=1)
    if ABSTRACT.exists():
        abs_md = ABSTRACT.read_text(encoding="utf-8").strip()
        anchor = "\n## Introduction"
        if anchor in main_text:
            main_text = main_text.replace(anchor, "\n" + abs_md + "\n" + anchor, 1)
        else:
            problems.append("no Introduction heading to place the abstract before")

    # ---- number the references, separately for each file --------------
    # Each file is numbered in ITS OWN citation order, which is what a reader of
    # one of them needs and what ASM asks for: a reference cited only in the
    # supplemental material belongs to the supplement's list, and one cited in
    # both appears in both lists under whatever number each file gives it.
    try:
        from src.build_references import build_list, load_bib, substitute
        bib = load_bib()
        main_text, main_order = substitute(main_text, bib)
        supp_text, supp_order = substitute(supp_text, bib)
        main_text += "\n\n" + build_list(main_order, bib)
        if supp_order:
            supp_text += ("\n\n" + build_list(supp_order, bib)
                          .replace("## References",
                                   "## References cited in this supplemental "
                                   "material", 1))
    except SystemExit as exc:
        problems.append(f"references not numbered: {exc}")

    check(main_text, supp_text, table_remap, problems)

    MAIN_OUT.write_text(main_text, encoding="utf-8")
    SUPP_OUT.write_text(supp_text, encoding="utf-8")

    with ROUTING_OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["parent", "old_number", "title", "destination",
                    "new_label", "words", "why"])
        for s in sections:
            w.writerow([s.parent, s.number or "", s.title, s.dest,
                        s.new_label, s.words, s.why])

    # ---- report ------------------------------------------------------
    def wc(t: str) -> int:
        """The word count a journal's limit is actually about.

        Table bodies and the reference list are excluded because no journal
        counts them against a text limit, and including them here would make
        the number that decides how deep to cut the prose wrong by thousands.
        """
        t = re.split(r"^## References", t, maxsplit=1, flags=re.M)[0]
        return len(re.sub(r"^\|.*$", "", t, flags=re.M).split())

    print(f"main text   {wc(main_text):>7,} words, {len(main_tabs)} tables "
          f"-> {MAIN_OUT.relative_to(ROOT)}")
    print(f"supplement  {wc(supp_text):>7,} words, {len(supp_tabs)} tables "
          f"-> {SUPP_OUT.relative_to(ROOT)}")
    print()
    for s in sections:
        if s.parent not in ("Results", "Materials and Methods"):
            continue
        arrow = "stays" if s.dest == MAIN else "MOVES"
        lab = f"{s.number}." if s.number else " "
        held = sum(len(p.split()) for p in s.deferred)
        tail = f"  ({held}w held back)" if held else ""
        print(f"   {arrow}  {lab:>4} {s.title[:52]:52} {s.words:>5}w"
              f"  {s.new_label or '':3}{tail}")

    if problems:
        print(f"\n   {len(problems)} problem(s):")
        for p in problems:
            print(f"      {p}")
        return 1
    print("\n   no dangling cross-references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
