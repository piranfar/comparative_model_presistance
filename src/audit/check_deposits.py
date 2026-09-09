"""Checker 5 -- when a sentence sends the reader to a table, is the thing it
promises actually in that table?

Run:  python -m src.audit.check_deposits

THE GAP THIS CLOSES.  ``src/audit/check_consistency.py`` already resolves every
cross-reference, but its table test is existence only::

    for tok in re.findall(r"S?\\d+", m.group(1)):
        if tok not in ms.tables:            # <- the whole test

A citation therefore passes as long as the table has a caption somewhere.  It
passed "It does appear as a descriptive row in Tables 9, 14 and S2" for two
rounds of review, because Tables 9, 14 and S2 all exist -- while the held-out
deposit has a row in exactly one of the three.  A reader who checked the
sentence was sent to two tables with nothing in them.  This module tests the
other half of a citation: not that the number resolves, but that the table it
resolves to contains what the sentence says it contains.

WHAT IT CHECKS.

(a) DEPOSIT IN TABLE.  Five deposits carry this paper.  Every sentence that
    claims one of them has a row in a list of tables, or is the subject of one,
    is checked against the tables themselves.  The name-to-table map is built by
    splitting ``manuscript/tables.md`` at each ``**Table N.**`` caption and
    scanning the legend and the grid of each block separately, because the
    deposits are written several ways -- "Dubey 2026", "Dubey hollow fibre
    (held out)", "Dubey, hollow fibre", "Dubey et al. 2026" -- and a map keyed
    on one spelling would miss the rest.  Only the surname or consortium name
    is hard-coded; the descriptive aliases ("hollow fibre", "six-laboratory",
    "clinical isolates") are harvested from the cells that carry an anchor, so
    the map learns the table's own vocabulary rather than the author's.  A
    claimed row in a table with no trace of the deposit at all is HIGH: the two
    statements cannot both be true.  A claimed *row* traced only to the legend
    is MEDIUM, with the distinction stated -- a legend that mentions a deposit
    is not a row a reader can find.  A claim that a table is a deposit's own,
    on the other hand, is exactly what a legend should carry, so a legend trace
    settles it.

    The subject of the claim may be an anaphor ("It does appear
    descriptively..."), which is how the defective sentence was written, so
    when the sentence names no deposit itself the enclosing paragraph is read
    for one, and the claim is dropped rather than guessed at if the paragraph
    names none or names several.

    Two disciplines keep this rule from failing the pipeline on correct prose.
    First, the subject has to BE the deposit, not a quantity drawn from it:
    "the Kaur concentration slopes are listed in Table 13" is a true sentence
    about a table that never writes "Kaur", so a claim whose subject carries a
    head noun of its own beyond the deposit's name is handed to rule (b)
    instead of being failed here.  Second, the descriptive aliases are trusted
    to identify a deposit inside a TABLE, where a wrong match only suppresses
    a finding, but not inside a SENTENCE unless the alias is a compound rather
    than a plain word: "laboratories" is harvested from the roster row, and in
    a paper about a six-laboratory ring trial it is ordinary vocabulary, not a
    name.  Negated and counterfactual predicates ("is not reported in Table
    14", "would have had a row of its own in Table 14") are not claims that a
    table holds anything, and are skipped; the count of them is on the receipt.

(b) ANY SUBJECT IN A CITED TABLE, generalised.  "<X> is reported in Table N"
    is the same promise with an arbitrary subject.  A distinctive token of X is
    required to occur somewhere in the cited table.  This is graded MEDIUM and
    never HIGH, because the subject of a general claim is open vocabulary: a
    table can legitimately report a thing under another word, and only the
    closed deposit vocabulary of (a) makes absence conclusive.  Where no
    distinctive token can be identified at all the claim is reported LOW rather
    than guessed at.

    The same promise is also made with the table in subject position -- "Table
    15 records what each conclusion is worth" -- which the claim patterns
    cannot see, and which the Table 7 legend now uses for the very pointer that
    replaced the defective one.  That shape is checked identically and at the
    same MEDIUM, except that an object carrying no distinctive word is passed
    over in silence: it is usually a pronoun standing in for the clause before
    ("Table S4 prints none"), and a finding on that would be noise.

(c) MULTI-PANEL FIGURE REFERENCES.  ``check_consistency`` already tests a
    single trailing panel letter (``Fig. 2D``) against the letters its legend
    defines, and that half is deliberately not repeated here.  What its pattern
    cannot see is a panel range or list -- ``Fig. 2A-D``, ``Fig. 2A and C``,
    ``panels A and C of Figure 2`` -- where every letter after the first
    escapes the test.  Only those forms are checked, at the same MEDIUM the
    existing panel finding uses.

DELIBERATELY NOT FLAGGED.  A cited table that does not exist at all (that is
``check_consistency``'s dangling-table-reference, and repeating it here would
double-report the same defect).  A table cited without a claim about its
contents -- the parenthetical "(Table 9)" that ends most sentences in this
paper promises nothing and is not tested.  A deposit named in a table under a
description that never co-occurs with its name anywhere in tables.md: the alias
harvest cannot learn such a name, so a claim about it would be reported
wrongly; the map is printed as a low finding on every run so that the exemption
is visible rather than silent.  A claim spread over two sentences ("It does
appear descriptively.  The rows are in Tables 9, 14 and S2.") is not seen: the
claim and its subject are read within one sentence, and the second sentence
names neither a deposit nor an anaphor this module will follow.  A negative
statement is not checked in either direction -- neither "is not reported in
Table 14" when the deposit is absent (correct, and skipped) nor when it is
present (a defect this module does not detect).
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------
# text utilities
# --------------------------------------------------------------------------

_SUPERSCRIPTS = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-",
}


def _normalise(s: str) -> str:
    """Fold the typographic characters the manuscript uses into ASCII."""
    out = []
    for ch in s:
        if ch in _SUPERSCRIPTS:
            out.append(_SUPERSCRIPTS[ch])
        elif ch in "‐‑‒–—−":
            out.append("-")
        elif ch in "‘’":
            out.append("'")
        elif ch in "“”":
            out.append('"')
        elif ch == "×":
            out.append("x")
        elif ch == "·":
            out.append(".")
        else:
            out.append(ch)
    return unicodedata.normalize("NFKC", "".join(out))


def _plain(s: str) -> str:
    """Strip markdown emphasis so phrases match across **bold** and *italic*."""
    return re.sub(r"[*_`]", "", s)


def _flat(s: str) -> str:
    return _plain(_normalise(s))


def _tokens(s: str) -> list[str]:
    """Lowercase word tokens, keeping internal hyphens ('six-laboratory')."""
    return re.findall(r"[a-z][a-z-]*", _flat(s).lower())


def _paragraphs(text: str) -> list[tuple[int, str]]:
    """Split into blocks, returning (1-based start line, block text)."""
    lines = text.split("\n")
    blocks: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 1
    for i, line in enumerate(lines, start=1):
        if line.strip() == "":
            if buf:
                blocks.append((start, "\n".join(buf)))
                buf = []
        else:
            if not buf:
                start = i
            buf.append(line)
    if buf:
        blocks.append((start, "\n".join(buf)))
    return blocks


def _sentence_span(text: str, pos: int) -> tuple[int, int]:
    a = text.rfind(". ", 0, pos)
    a = 0 if a < 0 else a + 2
    b = text.find(". ", pos)
    b = len(text) if b < 0 else b + 1
    return a, b


def _tidy(s: str, width: int = 200) -> str:
    return re.sub(r"\s+", " ", s).strip()[:width]


_STOP = {
    "the", "a", "an", "of", "in", "on", "at", "to", "is", "are", "was", "were",
    "and", "or", "but", "that", "this", "those", "these", "it", "its", "with",
    "for", "from", "by", "as", "be", "been", "not", "no", "than", "then",
    "which", "what", "when", "where", "into", "onto", "over", "under", "out",
    "up", "down", "so", "if", "each", "every", "any", "all", "one", "two",
    "more", "most", "less", "least", "also", "still", "own", "per", "cent",
    "there", "here", "does", "do", "did", "has", "have", "had", "them", "they",
    "we", "our", "us", "you", "he", "she", "his", "her", "their", "both",
    "other", "another", "same", "such", "only", "even", "much", "many",
    "between", "within", "without", "against", "across", "after", "before",
    "while", "how", "why", "who", "whom", "whose", "can", "could", "may",
    "might", "must", "should", "would", "will", "shall", "whether", "about",
    "above", "below", "again", "rather", "instead", "here", "itself",
}

# Words that describe a table's furniture or the paper's own machinery, and so
# cannot identify a deposit or a subject.  A deposit alias made of these alone
# would match every table in the manuscript.
_GENERIC = {
    "deposit", "deposits", "dataset", "datasets", "file", "files", "data",
    "table", "tables", "row", "rows", "column", "columns", "legend", "value",
    "values", "used", "using", "point", "mass", "span", "refuse", "refused",
    "none", "true", "false", "yes", "derived", "inferred", "flagged", "held",
    "plated", "volume", "volumes", "reading", "readings", "count", "counts",
    "culture", "cultures", "fraction", "density", "densities", "floor",
    "floors", "assay", "study", "paper", "section", "figure", "panel",
    "analysed", "analysis", "reported", "quoted", "stated", "measured",
    "median", "mean", "level", "levels", "variant", "variants", "model",
    "models", "test", "tests", "result", "results", "number", "numbers",
    "scenario", "quantity", "quantities", "verdict", "units", "unit",
}

# The head nouns a deposit itself is called by, and the adjectives this paper
# hangs on one.  A subject built only from these plus the deposit's own name is
# a claim ABOUT the deposit; anything else in it makes the claim about some
# quantity drawn from the deposit, which is a different promise (see
# ``_is_identity_subject``).
_DEPOSIT_HEAD = {
    "deposit", "deposits", "dataset", "datasets", "data", "file", "files",
    "study", "studies", "series", "record", "records", "source", "sources",
    "collection", "repository", "deposition", "entry", "arm", "arms",
}
_DEPOSIT_QUALIFIER = {
    "held-out", "held", "holdout", "primary", "secondary", "fifth", "further",
    "remaining", "published", "deposited", "original", "validation",
    "external", "independent", "present", "five", "own",
}


# --------------------------------------------------------------------------
# the tables, split at their captions
# --------------------------------------------------------------------------

_CAPTION_RE = re.compile(r"^\*\*Table\s+(S?\d+)[.:]")
_CAPTION_FLAT_RE = re.compile(r"^Table\s+(S?\d+)[.:]")
_GRID_RE = re.compile(r"^\s*\|")
_RULE_ROW = re.compile(r"^:?-{2,}:?$")


class Tables:
    """Every ``**Table N.**`` block, its legend and its grid, kept apart.

    Built from ``manuscript/tables.md`` -- the generated file that IS the
    tables -- and falling back to the assembled paper for any table that file
    does not hold.  Legend and body are kept separate because the two carry
    different promises: a legend says what a table is about, a body row is
    something a reader can point at.
    """

    def __init__(self, tables_md: str, paper: str = ""):
        self.blocks: dict[str, dict] = {}
        for src in (tables_md, paper):
            if src:
                self._scan(src)

    def _scan(self, text: str) -> None:
        lines = _normalise(text).split("\n")
        starts = [i for i, ln in enumerate(lines) if _CAPTION_RE.match(ln)]
        for k, i in enumerate(starts):
            num = _CAPTION_RE.match(lines[i]).group(1)
            if num in self.blocks:
                continue                     # first source seen wins
            end = starts[k + 1] if k + 1 < len(starts) else len(lines)
            legend: list[str] = []
            rows: list[str] = []
            in_legend = True
            for ln in lines[i:end]:
                if _GRID_RE.match(ln):
                    in_legend = False
                    cells = [_plain(c).strip()
                             for c in ln.strip().strip("|").split("|")]
                    if all(_RULE_ROW.fullmatch(c) for c in cells if c):
                        continue
                    rows.append(" | ".join(cells))
                elif in_legend:
                    legend.append(_plain(ln))
                else:
                    break                    # the block ends at its grid
            self.blocks[num] = {
                "legend": " ".join(legend).strip(),
                "rows": rows,
                "body": " ".join(rows),
            }

    def __contains__(self, num: str) -> bool:
        return num in self.blocks

    def get(self, num: str) -> dict | None:
        return self.blocks.get(num)


# --------------------------------------------------------------------------
# (a) which table holds which deposit
# --------------------------------------------------------------------------

# The five deposits, keyed by the one thing that cannot be paraphrased: the
# author's surname, or the consortium's name.  Everything else about how a
# table writes them is learned from the tables.
_ANCHORS: dict[str, str] = {
    "Vijay (clinical isolates)": r"vijay",
    "van Wijk / ERA4TB (six laboratories)": r"era4tb|van\s+wijk",
    "Windels (evolved clones)": r"windels",
    "Kaur (apramycin grid)": r"kaur",
    "Dubey (hollow fibre, held out)": r"dubey",
}


def _alias_words(segment: str) -> list[str]:
    """The words of one label segment that could identify a deposit."""
    return [w for w in _tokens(segment)
            if len(w) >= 4 and w not in _STOP and w not in _GENERIC]


def _strong_alias(alias: tuple[str, ...]) -> bool:
    """Is this alias distinctive enough to name a deposit in a SENTENCE?

    A phrase of two or more words is; so is a single constructed term, one
    carrying a hyphen or a digit ("six-laboratory").  A single plain word is
    not, however long: "laboratories", "planktonic" and "intracellular" are all
    harvested from rows that carry an anchor, and all three are ordinary
    vocabulary in a paper about laboratories and growth states.
    """
    if len(alias) >= 2:
        return True
    return bool(alias) and bool(re.search(r"[-0-9]", alias[0]))


def _candidate_aliases(cell: str, anchor: re.Pattern) -> list[tuple[str, ...]]:
    """Alias word-sets learned from one cell that already carries an anchor.

    Parenthesised text is dropped: in these labels it holds units and
    qualifiers ("(CFU per mL)", "(held out)"), which say nothing about which
    deposit is meant.  A single word only becomes an alias on its own when it
    is long enough to be a term rather than a common noun -- "laboratories"
    and "planktonic" earn it, "clinical" and "isolates" do not, and have to
    travel in pairs.
    """
    s = anchor.sub(" ", re.sub(r"\([^)]*\)", " ", cell))
    out: list[tuple[str, ...]] = []
    for seg in re.split(r"[,;:/|]|--", s):
        words = sorted(set(_alias_words(seg)))
        if len(words) >= 2:
            out.append(tuple(words))
        elif len(words) == 1 and len(words[0]) >= 9:
            out.append((words[0],))
    return out


class Deposits:
    """A name-to-table map, learned from the tables rather than declared."""

    def __init__(self, tables: Tables):
        self.tables = tables
        self.anchors = {k: re.compile(v, re.I) for k, v in _ANCHORS.items()}
        self.aliases: dict[str, set[tuple[str, ...]]] = {k: set()
                                                         for k in _ANCHORS}
        self.spellings: dict[str, set[str]] = {k: set() for k in _ANCHORS}
        self._harvest()
        self._drop_ambiguous()
        self.trace: dict[str, dict[str, str]] = {}      # deposit -> num -> how
        self._map()

    # -- learn the aliases ------------------------------------------------
    def _harvest(self) -> None:
        """Aliases are learned from the label CELLS that carry a deposit name.

        Legends are prose about a deposit, not a name for it, so they are read
        for the anchor but never mined for aliases: "Kaur is NA because its
        three day-zero readings are technical replicates" would otherwise
        enter the map as a name.
        """
        for _num, blk in self.tables.blocks.items():
            for dep, anchor in self.anchors.items():
                for row in blk["rows"]:
                    if not anchor.search(row):
                        continue
                    for cell in row.split("|"):
                        if not anchor.search(cell):
                            continue
                        self.spellings[dep].add(_tidy(cell, 60))
                        for al in _candidate_aliases(cell, anchor):
                            self.aliases[dep].add(al)

    def _drop_ambiguous(self) -> None:
        """An alias two deposits both answer to identifies neither."""
        owners: dict[tuple[str, ...], set[str]] = {}
        for dep, als in self.aliases.items():
            for al in als:
                owners.setdefault(al, set()).add(dep)
        for al, deps in owners.items():
            if len(deps) > 1:
                for dep in deps:
                    self.aliases[dep].discard(al)

    # -- apply them -------------------------------------------------------
    def _hit(self, dep: str, text: str, strong_only: bool = False) -> str | None:
        """Does this stretch of text name the deposit, and how.

        ``strong_only`` is the prose setting.  Inside a table a loose alias is
        safe: a match that should not have happened only records the deposit as
        present and so SUPPRESSES a finding.  Inside a sentence the same loose
        alias invents a claim and fails the build, so there only a compound
        alias -- two words, or a hyphenated or numbered term -- is allowed to
        stand in for the name.  "laboratories" is harvested from the roster and
        is a plain noun of this paper's subject matter; "six-laboratory" is a
        term, and is kept.
        """
        if self.anchors[dep].search(text):
            return "by name"
        toks = set(_tokens(text))
        for al in self.aliases[dep]:
            if strong_only and not _strong_alias(al):
                continue
            if all(w in toks for w in al):
                return "as '" + " ".join(al) + "'"
        return None

    def _map(self) -> None:
        for dep in self.anchors:
            per: dict[str, str] = {}
            for num, blk in self.tables.blocks.items():
                body = next((h for h in (self._hit(dep, r) for r in blk["rows"])
                             if h), None)
                legend = self._hit(dep, blk["legend"])
                if body:
                    per[num] = "body " + body
                elif legend:
                    per[num] = "legend only " + legend
            self.trace[dep] = per

    # -- lookups ----------------------------------------------------------
    def named_in(self, text: str, anchors_only: bool = False) -> list[str]:
        """Which deposits a stretch of prose names.

        Prose is read with the strong aliases only -- see ``_hit``.
        """
        out = []
        for dep in self.anchors:
            if self.anchors[dep].search(text):
                out.append(dep)
            elif not anchors_only and self._hit(dep, text, strong_only=True):
                out.append(dep)
        return out

    def naming_words(self, dep: str) -> set[str]:
        """Every word that, in prose, could be part of this deposit's name."""
        out = set(self.anchors[dep].pattern.replace(r"\s+", " ").split("|"))
        words = {w for token in out for w in re.findall(r"[a-z]+", token)}
        for al in self.aliases[dep]:
            words.update(al)
        return words

    def in_body(self, dep: str, num: str) -> bool:
        return self.trace[dep].get(num, "").startswith("body")

    def anywhere(self, dep: str, num: str) -> bool:
        return num in self.trace[dep]


# --------------------------------------------------------------------------
# claims: "<subject> <claim phrase> Table(s) N, M"
# --------------------------------------------------------------------------

_TABLE_LIST_RE = re.compile(
    r"\bTables?\s+(S?\d+(?:\s*(?:,|and|,\s*and|&)\s*S?\d+)*)")

# The claim is a row in the table: a reader should be able to point at a line.
_ROW_LEAD_RE = re.compile(
    r"(?:"
    r"(?:a|an|one|its\s+own)?\s*(?:descriptive|separate|single|further)?\s*"
    r"rows?(?:\s+of\s+its\s+own)?(?:\s+apiece)?\s+(?:in|of)"
    r"|appears?(?:\s+[a-z]+){0,3}?\s+in"
    r"|(?:is|are|was|were)\s+(?:[a-z]+\s+){0,2}?"
    r"(?:reported|shown|listed|given|tabulated|recorded|summari[sz]ed|"
    r"printed|plotted|quoted|described|tested|set\s+out)\s+in"
    r")\s*$", re.I)

# The claim is that the whole table belongs to the subject.  Every branch is
# inside the group the end-anchor applies to, so the phrase has to be the thing
# the table reference follows and cannot be matched loose in the sentence.
_SUBJECT_LEAD_RE = re.compile(
    r"(?:"
    r"(?:a|an|one|its\s+own)\s+(?:whole\s+|entire\s+)?table"
    r"(?:\s+(?:of\s+its\s+own|to\s+itself|all\s+of\s+its\s+own))?\s+in"
    r"|the\s+subject\s+of"
    r"|given\s+over\s+(?:entirely\s+)?to"
    r")\s*$", re.I)

# "Table 12 is entirely its own" -- the table comes first in this shape.
_SUBJECT_TRAIL_RE = re.compile(
    r"^\s*(?:,)?\s*is\s+(?:entirely\s+|wholly\s+)?(?:its|his|her|their)\s+own",
    re.I)

_ANAPHOR_RE = re.compile(
    r"^\s*(?:it|this|that|these|those|they)\b"
    r"|^\s*(?:the|this|that)\s+(?:[a-z]+[- ]){0,2}deposit\b", re.I)

_CLAUSE_SPLIT_RE = re.compile(r"[;:]|\s-\s|\s--\s")

# A predicate that denies the table holds the thing, or supposes it rather than
# asserting it.  Neither is a claim about what is in the table, and failing a
# build on one is how an audit gets switched off.
_NOT_A_CLAIM_RE = re.compile(
    r"\b(?:not|no|never|neither|nor|cannot|none|nothing|without|"
    r"would|could|might|hypothetical|counterfactual)\b|n't\b", re.I)


class Claim:
    __slots__ = ("kind", "tables", "subject", "sentence", "lineno", "block",
                 "phrase", "anaphoric")

    def __init__(self, kind, tables, subject, sentence, lineno, block, phrase,
                 anaphoric=False):
        self.kind = kind                # "row" | "subject"
        self.tables = tables
        self.subject = subject
        self.sentence = sentence
        self.lineno = lineno
        self.block = block
        self.phrase = phrase
        # True when the subject is a pronoun, or is left implicit by the shape
        # of the sentence ("Table 12 is entirely its own"), so that it has to
        # be recovered from the paragraph rather than read off the clause.
        self.anaphoric = anaphoric


def _asserted(lead: str, start: int, phrase: str) -> bool:
    """Does the clause carrying this claim actually assert it?

    The window is the matched phrase plus the four words immediately before it,
    because a negation or a modal can sit on either side of the join: "is NOT
    reported in Table 14" puts it inside the phrase, "WOULD have had a row of
    its own in Table 14" puts it just before.  Four words is deliberately tight.
    A wider window swallows negations that belong to an earlier clause and do
    not govern the claim at all -- "the deposit, for which no patient
    identifier exists, has a row of its own in Table 14" is an assertion, and
    suppressing it would hide the defect it may carry.
    """
    before = _tokens(lead[:start])[-4:]
    window = " ".join(before) + " " + phrase
    return not _NOT_A_CLAIM_RE.search(window)


def _subject_of(sentence: str, upto: int) -> str:
    """The noun phrase a claim is made about: the last clause before it.

    A clause that carries a table reference of its own is skipped: in "a row of
    its own in Tables 2, 5 ... and a table of its own in Table 12" the second
    claim's subject is not the first claim, it is what both are about.
    """
    pre = sentence[:upto].rstrip()
    parts = [p.strip() for p in _CLAUSE_SPLIT_RE.split(pre) if p.strip()]
    for part in reversed(parts):
        if _tokens(part) and not _TABLE_LIST_RE.search(part):
            return part
    return parts[0] if parts else pre.strip()


def _claims(text: str) -> tuple[list[Claim], int]:
    """Every sentence that promises a named thing is inside a named table.

    Returns the claims and the number of table references that matched a claim
    shape but were denied or supposed rather than asserted, which the receipt
    reports so that the skip is visible rather than silent.
    """
    out: list[Claim] = []
    skipped = 0
    for lineno, block in _paragraphs(text):
        btxt = _flat(block)
        if btxt.lstrip().startswith("|"):
            continue                     # a grid, not a sentence
        for m in _TABLE_LIST_RE.finditer(btxt):
            a, b = _sentence_span(btxt, m.start())
            sentence = btxt[a:b]
            at = m.start() - a
            lead = sentence[:at]
            trail = sentence[at + len(m.group(0)):]
            if _CAPTION_FLAT_RE.match(btxt.lstrip()) and m.start() < 10:
                continue                 # the caption that defines the table
            nums = re.findall(r"S?\d+", m.group(1))
            if _SUBJECT_LEAD_RE.search(lead) or _SUBJECT_TRAIL_RE.match(trail):
                kind, cut = "subject", _SUBJECT_LEAD_RE.search(lead)
            elif _ROW_LEAD_RE.search(lead):
                kind, cut = "row", _ROW_LEAD_RE.search(lead)
            else:
                continue
            start = cut.start() if cut else len(lead)
            phrase = _tidy(lead[start:] + m.group(0), 80)
            if not _asserted(lead, start, phrase + " " + trail[:40]):
                skipped += 1
                continue
            subject = _subject_of(sentence, start)
            # "Table 12 is entirely its own" carries its referent in the
            # sentence before it, so there is no subject to read off this one;
            # without this the whole trailing branch could only ever fall
            # through to the unverifiable-claim rule.
            anaphoric = bool(_ANAPHOR_RE.match(sentence)) or not _tokens(subject)
            out.append(Claim(kind, nums, subject, sentence, lineno, block,
                             phrase, anaphoric))
    return out, skipped


# --------------------------------------------------------------------------
# where a finding is actionable
# --------------------------------------------------------------------------

def _where(claim: Claim, prose: str) -> str:
    """Point at the file an editor would open, not only the assembled paper."""
    head = _flat(claim.block).lstrip()
    m = _CAPTION_FLAT_RE.match(head)
    if m:
        return (f"Table {m.group(1)} legend (PAPER_COMPLETE.md line "
                f"{claim.lineno}; legends are generated by src/build_tables.py)")
    line = _prose_line(claim.sentence, prose)
    if line:
        return (f"line {claim.lineno} (MANUSCRIPT.md line {line})")
    return f"line {claim.lineno}"


def _prose_line(sentence: str, prose: str) -> int | None:
    """The line of the prose source the sentence was written on."""
    if not prose:
        return None
    words = _tokens(sentence)
    if len(words) < 4:
        return None
    # anything but letters may sit between the words: the prose wraps its
    # lines, and an em dash or a bracket can fall between any two of them
    needle = r"[^A-Za-z]+".join(re.escape(w) for w in words[:6])
    hay = _flat(prose)
    m = re.search(needle, hay, re.I)
    if not m:
        return None
    return hay.count("\n", 0, m.start()) + 1


# --------------------------------------------------------------------------
# rule (a): a deposit claimed into a table that does not carry it
# --------------------------------------------------------------------------

def _is_identity_subject(subject: str, dep: str, deps: Deposits) -> bool:
    """Is the subject the deposit itself, rather than something drawn from it?

    "The Dubey deposit" and "the held-out hollow fibre deposit" are the deposit.
    "The Kaur concentration slopes" and "the apramycin grid concentrations" are
    quantities that come out of one, and a table can report them without ever
    writing the depositor's name -- Table 13 is exactly that table.  Only the
    first kind may reach a high finding; the second is handed to the general
    subject rule, where absence of a word is evidence and not proof.

    The test is applied to the comma-delimited piece that actually carries the
    name, so that a leading subordinate clause ("Although no deposit was
    selected on its result, the Dubey deposit has a row in ...") does not make
    a plain claim look like a derived one -- while a name stranded in an
    earlier piece ("In the hollow fibre deposit, the plating volumes are
    tabulated in ...") still reads as the derived claim it is.
    """
    naming = deps.naming_words(dep)

    def _clean(s: str) -> bool:
        return not [w for w in _tokens(s)
                    if w not in _STOP and w not in naming
                    and w not in _DEPOSIT_HEAD and w not in _DEPOSIT_QUALIFIER]

    pieces = [p for p in subject.split(",") if p.strip()]
    carrying = [p for p in pieces if deps._hit(dep, p, strong_only=True)]
    if carrying:
        return _clean(carrying[-1])
    return _clean(subject)


def _resolve_deposit(claim: Claim, deps: Deposits) -> tuple[str | None, str]:
    """Which deposit a claim is about, and how that was decided."""
    named = deps.named_in(claim.subject)
    if len(named) == 1:
        if not _is_identity_subject(claim.subject, named[0], deps):
            return None, "subject is a quantity, not the deposit"
        return named[0], "named in the claim"
    if len(named) > 1:
        return None, "several deposits named"
    if claim.anaphoric:
        in_block = deps.named_in(_flat(claim.block), anchors_only=True)
        if len(in_block) == 1:
            return in_block[0], "the deposit its paragraph names"
        return None, "anaphor with %d deposits in the paragraph" % len(in_block)
    return None, "no deposit named"


def _check_deposit_claims(claims, deps: Deposits, prose: str) -> tuple:
    findings: list[dict] = []
    handled: set[int] = set()
    for i, claim in enumerate(claims):
        dep, _how = _resolve_deposit(claim, deps)
        if dep is None:
            continue
        handled.add(i)
        known = "; ".join(sorted(deps.spellings[dep])[:4]) or "none"
        for num in claim.tables:
            if num not in deps.tables:
                continue            # check_consistency reports the dangling ref
            if claim.kind == "subject":
                if deps.anywhere(dep, num):
                    continue
                findings.append({
                    "severity": "high",
                    "kind": "deposit-not-in-cited-table",
                    "where": _where(claim, prose),
                    "detail": (
                        f"The sentence says Table {num} is the {dep} deposit's "
                        f"own, but neither the legend nor any row of Table "
                        f"{num} names that deposit, under any spelling the "
                        f"tables use elsewhere."),
                    "expected": (f"the {dep} deposit named in Table {num}; "
                                 f"the tables write it as: {known}"),
                    "found": _tidy(claim.phrase, 120),
                })
                continue
            if deps.in_body(dep, num):
                continue
            if deps.anywhere(dep, num):
                findings.append({
                    "severity": "medium",
                    "kind": "deposit-in-legend-not-in-a-row",
                    "where": _where(claim, prose),
                    "detail": (
                        f"The sentence sends the reader to a row of the {dep} "
                        f"deposit in Table {num}, but that deposit appears only "
                        f"in the table's legend; no body row carries it, so "
                        f"there is no line to point at."),
                    "expected": f"a body row of Table {num} naming {dep}",
                    "found": deps.trace[dep][num],
                })
                continue
            others = sorted(d.split(" (")[0] for d in deps.anchors
                            if deps.anywhere(d, num))
            tail = (f"Table {num} does carry {', '.join(others)}"
                    if others else
                    f"Table {num} names no deposit at all")
            findings.append({
                "severity": "high",
                "kind": "deposit-not-in-cited-table",
                "where": _where(claim, prose),
                "detail": (
                    f"The sentence says the {dep} deposit has a row in Table "
                    f"{num}. It has none: no row and no legend of that table "
                    f"names it, under any spelling the tables use elsewhere. "
                    f"{tail}."),
                "expected": (f"a row of Table {num} naming {dep}; the tables "
                             f"write it as: {known}"),
                "found": _tidy(claim.phrase, 120),
            })
    return findings, handled


# --------------------------------------------------------------------------
# rule (b): any subject claimed into a table that does not mention it
# --------------------------------------------------------------------------

def _distinctive(subject: str) -> list[str]:
    """Tokens of the subject that could be looked for in a table."""
    return [w for w in dict.fromkeys(_tokens(subject))
            if len(w) >= 5 and w not in _STOP and w not in _GENERIC]


def _token_in(tok: str, toks: set[str]) -> bool:
    """Match on a six-character stem, so plurals and inflections agree."""
    if tok in toks:
        return True
    stem = tok[:6]
    if len(tok) >= 6:
        return any(t.startswith(stem) for t in toks)
    return any(t == tok or t[:-1] == tok for t in toks)


def _check_subject_claims(claims, handled, tables: Tables,
                          prose: str) -> list[dict]:
    findings: list[dict] = []
    for i, claim in enumerate(claims):
        if i in handled:
            continue
        keys = _distinctive(claim.subject)
        live = [n for n in claim.tables if tables.get(n) is not None]
        if not live:
            continue                # check_consistency reports the dangling ref
        if not keys:
            findings.append({
                "severity": "low",
                "kind": "unverifiable-table-claim",
                "where": _where(claim, prose),
                "detail": (
                    f"'{_tidy(claim.subject, 60)}' is said to be in Table "
                    f"{', '.join(live)}, but the claim carries no distinctive "
                    f"word to look for, so whether the table holds it was not "
                    f"decided either way."),
                "expected": "a checkable subject for the Table "
                            f"{', '.join(live)} claim",
                "found": _tidy(claim.sentence, 160),
            })
            continue
        for num in live:
            blk = tables.get(num)
            toks = set(_tokens(blk["legend"] + " " + blk["body"]))
            if any(_token_in(k, toks) for k in keys):
                continue
            findings.append({
                "severity": "medium",
                "kind": "claim-absent-from-cited-table",
                "where": _where(claim, prose),
                "detail": (
                    f"The sentence sends the reader to Table {num} for "
                    f"'{_tidy(claim.subject, 60)}', but no word of that "
                    f"subject ({', '.join(keys)}) occurs anywhere in Table "
                    f"{num} -- neither in its legend nor in any row. Either "
                    f"the pointer is to the wrong table or the table does not "
                    f"report what the sentence promises."),
                "expected": f"'{keys[0]}' somewhere in Table {num}",
                "found": _tidy(claim.sentence, 200),
            })
    return findings


# --------------------------------------------------------------------------
# rule (b), second shape: the table as the SUBJECT of the sentence
# --------------------------------------------------------------------------

# "Table 15 records what each conclusion is worth" makes the same promise as
# "what each conclusion is worth is recorded in Table 15", with the table in
# subject position, where the claim patterns above cannot see it.  This is not
# a rare form here: the Table 7 legend, whose pointer at Table S2 was the
# defect this module was written for, now carries its replacement in exactly
# this shape, and a rule blind to it would pass the same defect a second time.
_TABLE_SUBJECT_RE = re.compile(
    r"\bTables?\s+(S?\d+)\s+"
    r"((?:instead\s+|also\s+|only\s+|now\s+|then\s+|already\s+){0,2}"
    r"(?:records?|reports?|lists?|gives?|shows?|prints?|carries|carry|holds?|"
    r"contains?|tabulates?|counts?|collects?|separates?|sets\s+out|uses?)"
    r")\s+([^.;:]{0,110})", re.I)


def _check_table_subject_claims(text: str, tables: Tables,
                                prose: str) -> list[dict]:
    """"Table N <verb> <X>" -- is X anywhere in Table N?

    Graded like rule (b) and for the same reason: the object of such a sentence
    is open vocabulary, so a missing word is evidence and not proof.  An object
    with no distinctive word at all is passed over in silence rather than
    reported, because unlike the subject of a presence claim it is often a
    pronoun standing in for the previous clause ("Table S4 prints none"), and
    a finding on that is noise.
    """
    findings: list[dict] = []
    for lineno, block in _paragraphs(text):
        btxt = _flat(block)
        if btxt.lstrip().startswith("|"):
            continue
        head_caption = _CAPTION_FLAT_RE.match(btxt.lstrip())
        for m in _TABLE_SUBJECT_RE.finditer(btxt):
            if head_caption and m.start() < 10:
                continue                 # the caption naming its own table
            num, verb, obj = m.group(1), m.group(2), m.group(3)
            blk = tables.get(num)
            if blk is None:
                continue            # check_consistency reports the dangling ref
            before = " ".join(_tokens(btxt[:m.start()])[-4:])
            if _NOT_A_CLAIM_RE.search(before + " " + verb):
                continue            # denied or supposed, not asserted
            keys = _distinctive(obj)
            if not keys:
                continue
            toks = set(_tokens(blk["legend"] + " " + blk["body"]))
            if any(_token_in(k, toks) for k in keys):
                continue
            a, b = _sentence_span(btxt, m.start())
            claim = Claim("table-subject", [num], obj, btxt[a:b], lineno,
                          block, _tidy(m.group(0), 80))
            findings.append({
                "severity": "medium",
                "kind": "claim-absent-from-cited-table",
                "where": _where(claim, prose),
                "detail": (
                    f"The sentence says Table {num} {_tidy(verb, 20)} "
                    f"'{_tidy(obj, 60)}', but no word of that "
                    f"({', '.join(keys)}) occurs anywhere in Table {num} -- "
                    f"neither in its legend nor in any row. Either the pointer "
                    f"is to the wrong table or the table does not hold what "
                    f"the sentence says it holds."),
                "expected": f"'{keys[0]}' somewhere in Table {num}",
                "found": _tidy(claim.sentence, 200),
            })
    return findings


# --------------------------------------------------------------------------
# rule (c): panel ranges and lists, which the single-letter test cannot see
# --------------------------------------------------------------------------

_FIG_PANELS_RE = re.compile(
    r"\b(?:Fig\.|Figure)\s*(\d+)\s*"
    r"([A-Z](?:\s*(?:-|,|and|,\s*and|&|to)\s*[A-Z])+)\b")
_PANELS_OF_RE = re.compile(
    r"\bpanels\s+([A-Z](?:\s*(?:-|,|and|,\s*and|&|to)\s*[A-Z])*)\s+of\s+"
    r"(?:Fig\.|Figure)\s*(\d+)\b")
_PANEL_DEF_RE = re.compile(r"\(\*\*([A-Z])\*\*\)")
_FIG_CAPTION_RE = re.compile(r"^\*\*Figure\s+(\d+)[.:]")


def _expand(letters: str) -> list[str]:
    """'A-D' is four panels; 'A and C' is two."""
    parts = re.split(r"\s*(-|to)\s*", letters)
    out: list[str] = []
    if len(parts) == 3 and parts[1] in ("-", "to"):
        a, b = parts[0].strip(), parts[2].strip()
        if len(a) == 1 and len(b) == 1 and a <= b:
            return [chr(c) for c in range(ord(a), ord(b) + 1)]
    for ch in re.findall(r"[A-Z]", letters):
        if ch not in out:
            out.append(ch)
    return out


def _check_figure_panels(text: str, prose: str) -> list[dict]:
    findings: list[dict] = []
    defined: dict[str, set[str]] = {}
    blocks = _paragraphs(text)
    for _ln, block in blocks:
        m = _FIG_CAPTION_RE.match(block)
        if m:
            defined[m.group(1)] = set(_PANEL_DEF_RE.findall(block))
    for lineno, block in blocks:
        btxt = _flat(block)
        for m in _FIG_PANELS_RE.finditer(btxt):
            fnum, letters = m.group(1), m.group(2)
            findings += _panel_finding(fnum, _expand(letters), defined, lineno,
                                       btxt, m.start())
        for m in _PANELS_OF_RE.finditer(btxt):
            letters, fnum = m.group(1), m.group(2)
            findings += _panel_finding(fnum, _expand(letters), defined, lineno,
                                       btxt, m.start())
    return findings


def _panel_finding(fnum, letters, defined, lineno, btxt, pos) -> list[dict]:
    have = defined.get(fnum)
    if not have:
        return []                     # no legend, or a legend without panels
    missing = [p for p in letters if p not in have]
    if not missing:
        return []
    return [{
        "severity": "medium",
        "kind": "dangling-figure-panel-range",
        "where": f"line {lineno}",
        "detail": (
            f"A multi-panel reference to Figure {fnum} names panel"
            f"{'s' if len(missing) > 1 else ''} {', '.join(missing)}, which "
            f"its legend does not define; the legend defines "
            f"{', '.join(sorted(have))}. Only the first letter of such a "
            f"reference is tested elsewhere, so the rest pass unread."),
        "expected": f"panels {', '.join(sorted(have))} in the Figure {fnum} "
                    f"legend",
        "found": _tidy(btxt[max(0, pos - 25):pos + 105], 130),
    }]


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------

def _read(root: Path, rel: str) -> str:
    path = root / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""


def check(text: str, ctx: dict) -> list[dict]:
    """Return a list of findings.  Empty list means clean."""
    root = Path(ctx.get("root") or Path(__file__).resolve().parents[2])
    if not text or "**Table" not in text:
        text = _read(root, "manuscript/PAPER_COMPLETE.md")
    tables_md = ctx.get("tables")
    if tables_md is None:
        tables_md = _read(root, "manuscript/tables.md")
    prose = ctx.get("prose")
    if prose is None:
        prose = _read(root, "manuscript/MANUSCRIPT.md")

    tables = Tables(tables_md, text)
    deps = Deposits(tables)
    claims, skipped = _claims(text)

    findings, handled = _check_deposit_claims(claims, deps, prose)
    findings += _check_subject_claims(claims, handled, tables, prose)
    findings += _check_table_subject_claims(text, tables, prose)
    findings += _check_figure_panels(text, prose)

    # The map itself is reported, so that what the deposit rule believes is
    # auditable rather than implicit -- and so that a deposit the harvest never
    # learned to recognise shows up as an empty row instead of as silence.
    def _order(n: str) -> tuple[int, int]:
        return (1 if n.startswith("S") else 0, int(n.lstrip("S")))

    def _mark(dep: str, n: str) -> str:
        """A table number, starred where only a description matched.

        A trace that rests on an alias rather than on the depositor's name is
        the weakest link in the map: it is how Table 1, the roster, is read
        correctly, and it is also how an accidental pair of ordinary words can
        make a table look as though it names a deposit -- which SUPPRESSES a
        finding.  Starring them keeps that visible on the receipt.
        """
        return n if deps.trace[dep][n].endswith("by name") else n + "*"

    lines = []
    for dep in _ANCHORS:
        rows = [_mark(dep, n) for n in
                sorted((n for n in deps.trace[dep] if deps.in_body(dep, n)),
                       key=_order)]
        legs = [_mark(dep, n) for n in
                sorted((n for n in deps.trace[dep] if not deps.in_body(dep, n)),
                       key=_order)]
        lines.append(
            "%s: rows in %s; legend only in %s"
            % (dep.split(" (")[0],
               ", ".join(rows) or "no table",
               ", ".join(legs) or "no table"))
    findings.append({
        "severity": "low",
        "kind": "deposit-table-map",
        "where": "manuscript/tables.md",
        "detail": ("; ".join(lines)
                   + ". A starred table matched a description rather than the "
                     "depositor's name"),
        "expected": ("%d claims about a table's contents were checked; %d "
                     "denied or supposed rather than asserted, and skipped"
                     % (len(claims), skipped)),
        "found": "aliases learned: " + "; ".join(
            "%s = %s" % (dep.split(" (")[0],
                         " / ".join(sorted(" ".join(a)
                                           for a in deps.aliases[dep])) or "-")
            for dep in _ANCHORS),
    })

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 3), f["kind"]))
    return findings


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(__file__).resolve().parents[2]
    paper = Path(argv[0]) if argv else root / "manuscript" / "PAPER_COMPLETE.md"
    text = paper.read_text(encoding="utf-8")
    ctx = {"root": root,
           "tables": _read(root, "manuscript/tables.md"),
           "prose": _read(root, "manuscript/MANUSCRIPT.md")}
    findings = check(text, ctx)
    print(f"check_deposits on {paper}")
    hard = [f for f in findings if f["severity"] == "high"]
    print(f"  {len(findings)} finding(s), {len(hard)} high\n")
    for f in findings:
        print(f"[{f['severity'].upper():6}] {f['kind']}  ({f['where']})")
        print(f"         {f['detail']}")
        if "expected" in f:
            print(f"         expected: {f['expected']}")
        if "found" in f:
            print(f"         found:    {f['found']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
