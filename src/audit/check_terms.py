"""Checker 5 -- is every term used in the sense the Methods declare, and is every
abbreviation expanded before it is used?

Run:  python -m src.audit.check_terms
      python -m src.audit.check_terms --debug      every term occurrence, classified
      python -m src.audit.check_terms --selftest   plant the errors this module catches

WHY THIS EXISTS.  The value audit recomputes numbers and the other checkers
under src/audit compare numbers with each other.  None of them reads a
*word*.  But this paper's argument is carried by a vocabulary it had to
invent and then keep, and two rounds of review found the vocabulary
slipping: the assay floor called a boundary, the boundary called a limit,
a first observed crossing called clearance, and one abbreviation carrying
two meanings.  Each of those is a definitional defect that leaves every
number in the manuscript correct.

THE RULE, AS THE MANUSCRIPT STATES IT.  The Methods subsection *Two kinds of
limit, kept apart* declares:

    "Those two names are the precise ones and are used where *L* is defined or
    its provenance discussed.  In running text *L* is the **assay floor**, and
    that is the only short form used, so that "boundary" is left free for the
    two derived boundaries of the next subsection and never denotes a value.
    The event a time-to-event analysis records is correspondingly a first
    observed crossing below the assay floor."

This module enforces exactly that sentence, and reports if the manuscript stops
making the promise, because a checker enforcing a rule the paper no longer states
is worse than no checker.

WHAT IT CHECKS
--------------

BOUNDARY.  "Boundary" belongs to the two quantities derived under *Dynamic range,
and the two boundaries it sets* -- *N*_reach and *N*_id -- and to nothing else.
The allow-list is built from the manuscript rather than guessed, and it is
GRADED, because the strength of a marker decides what can override it:

  * the two derived boundaries named anywhere in the window (identifiability,
    reachability, *N*_reach, *N*_id, the subsection cited by title) settle the
    question and nothing overrides them.  That is deliberate: the pair is the
    paper's central contribution and must keep the word;
  * the quantified spellings the occurrence is itself part of -- "two
    boundaries", "both boundaries", "neither boundary", "every boundary", "the
    boundary case" -- clear it, but only where the phrase covers that
    occurrence, so a plural two lines above no longer clears a singular below;
  * "thresholds", "derived" and "definitions alone" are company a derived
    boundary keeps and nothing more.  They clear an otherwise unclassified
    occurrence and are overridden by floor-denoting grammar, because one common
    word inside a 420-character window is not a reason to disbelieve a sentence
    that says a count fell below the boundary.

The high tier asks for two things at once, and asking for only one was the
mistake worth fixing.  N_reach and N_id are values too; isolates and starting
densities legitimately sit above and below them, and the manuscript's own
"Above that boundary the lowest class is the only one compatible with a censored
reading" is correct prose.  What cannot be said of a derived boundary is that a
COUNT is below it.  So high needs the grammar of a value on the measurement
scale -- below, above, at, crossing, and the passive and relative forms of the
same -- together with a measurement noun in the position that grammar puts the
subject.  Grammar without the noun is medium.

A few spellings can never be the derived boundaries whatever surrounds them --
"assay boundary", "floor boundary", "the boundary *L*", "*L*, the boundary",
"boundary of quantification", "detection boundary", "below-boundary" -- and
those are reported high even inside an allow-listed span, unless they sit inside
quotation marks, which is how a rule gets stated.

LIMIT.  The same treatment for "limit", with the exemptions the authors have
decided to keep.  Censoring notation outranks everything, because "the
probability that it fell below its own limit" IS the Tobit likelihood: the
Estimation subsection is exempt whole, and the exemption is held a second time
by the notation beside the word (Tobit, Phi, truncated at, Beal, Rubin), so that
renaming the heading cannot by itself fail the pipeline.  The named assay terms
("limit of quantification", "limit of detection"), the ends of an interval
("upper limit"), a constraint rather than a value ("a limit on how deep the
assay can see"), the deposit's hyphenated flag columns, and the manuscript's own
licence to report what a source states or fails to state, all clear the
occurrence -- but only where the phrase covers it.  A "limit of quantification"
elsewhere in the paragraph no longer launders "three of the four readings sit
below the limit".

EVENT NAMES.  The manuscript renamed the endpoint that a time-to-event analysis
records: it is a first observed crossing below the assay floor, not clearance
and not sterilisation, because most series that cross read above the floor
again.  Both old names are still in the text, in the sentences that disown them,
so the rule needs a disavowal test -- and the test asks what the negation
actually negates.  "is not clearance", "are not clearances", "is not read as
clearance, sterilisation or the end of a culture" all disown the name, because
nothing stands between the negation and the name but the copula, a naming verb
or the other names of the same family.  "on data it was not built from, the
depth at which a sterilisation claim ..." negates a different verb, and a rule
that asked only whether some negation stood in the ninety characters before the
word was silenced by any of them.  Naming the event in the sentence after the
one that defines it -- "We call it clearance throughout" -- is caught too.

ABBREVIATIONS.  Every abbreviation is expanded before it is used, and the title,
the Abstract and the main text count as separate regions, because a reader of
the Abstract alone gets no expansion from the Introduction.  Every character of
the file belongs to one of the three, front matter and author block included.

And no abbreviation denotes two things: the defect this was written for is
"MDK", the minimum duration for killing, once used for "MDR", the deposited
label's fourth, unordered category.  Confusable pairs are found rather than
listed -- two abbreviations of the same length differing in one letter -- and an
occurrence is reported where its surroundings carry the other abbreviation's
REPEATED company, none of its own, and no word of its own expansion.  Repetition
matters on both sides: a word standing once beside an abbreviation that occurs
nine times is not evidence the abbreviation was meant, while a word the other
one keeps beside it twice and this one never does is.  An occurrence with the
other abbreviation written beside it is not judged at all, since there the
surrounding words are shared on purpose -- but that is now decided occurrence by
occurrence, because as a test on the pair it meant one sentence naming both
switched the rule off for the whole manuscript.

Exemptions to the expansion rule are taken from what actually occurs, each judged
on its own: standard units and assay terms (CFU, MPN, MIC, LOD, LOQ), standard
statistics (CI, IQR), drug and deposit codes that appear only as arm labels or
column names beside a legend that names them in full (INH, MXF, RIF, IS, IR, BQL,
AQL), the names of standards bodies, which are their acronyms (NCCLS, CLSI),
licence tags (CC, BY), and table fillers (NA).  All-caps status codes -- NOT
SUPPORTED, DERIVED, INFERRED, FLAGGED, PROXY, NONE -- are not abbreviations at
all, and are recognised by the manuscript using the same word in lower case
elsewhere; a token the paper writes out in full is an abbreviation whatever its
casing elsewhere, or one stray lower-case spelling would switch the token off.

WHERE THIS IS BLIND, so nobody reads more guarantee into it than it gives
------------------------------------------------------------------------

  * A floor-denoting sentence written inside the Dynamic-range subsection, or in
    the same paragraph as "identifiability", "reachability", *N*_reach or *N*_id,
    is masked.  Appending "Counts that fall below the boundary are not reported"
    to each of the manuscript's 174 prose paragraphs in turn is reported high in
    166 of them; the eight silent ones are that subsection and three paragraphs
    that name the derived boundaries.  The same probe for "limit" is high in 157,
    the seventeen silent ones being the two Methods subsections that keep the
    word.  The six unconditional spellings punch through the mask; nothing else
    does.
  * "Boundary is 23 per mL" is judged only where the number carries a plating
    unit.  N_reach and N_id are numeric too, and this module does not know which
    value is the floor.
  * The confusable-pair rule needs both members to occur at least twice, needs
    three repeated collocates with two of them uncommon, and does not judge an
    occurrence with its sibling written beside it.  Substituting MDK for MDR is
    caught in the Table 5 rows, in the Methods, in the Discussion and in the
    sentence that defines the label; it is missed in the Table S1 row, where a
    genuine MDR stands two lines away, and in the Box 1 heading, where the
    evidence is one shared word.  On this manuscript it judges exactly one pair,
    MDK/MDR: OD/OR is skipped occurrence by occurrence where the two stand
    together, and every other pair is a single occurrence or not confusable.
  * Nothing here reads a number.  A term used correctly of the wrong quantity is
    invisible to it.
"""
from __future__ import annotations

import bisect
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------
# the two sentences of the Methods this module enforces
# --------------------------------------------------------------------------

_RULE_BOUNDARY = (
    'In running text *L* is the **assay floor**, and that is the only short '
    'form used, so that "boundary" is left free for the two derived boundaries '
    'of the next subsection and never denotes a value.'
)
_RULE_EVENT = (
    'The event a time-to-event analysis records is correspondingly a first '
    'observed crossing below the assay floor.'
)

# Headings whose whole body is exempt, and why.
_H_LIMIT = "Two kinds of limit, kept apart"
_H_RANGE = "Dynamic range, and the two boundaries it sets"
_H_ESTIM = "Estimation"


# --------------------------------------------------------------------------
# text utilities
# --------------------------------------------------------------------------

_WRAP_RE = re.compile(r"[\n\r\t]")


def _flat(text: str) -> str:
    """Emphasis markers replaced by spaces, so offsets and line numbers hold.

    "*L*" becomes " L ", "**assay floor**" becomes "  assay floor  ", and a
    phrase can be matched without writing every asterisk into every pattern.
    """
    return text.translate(str.maketrans({"*": " ", "`": " "}))


def _squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _starts(text: str) -> list[int]:
    out, pos = [], 0
    for ln in text.split("\n"):
        out.append(pos)
        pos += len(ln) + 1
    return out


def _lineno(starts: list[int], off: int) -> int:
    return bisect.bisect_right(starts, off)


def _quoted_spans(text: str) -> list[tuple[int, int]]:
    """Spans inside quotation marks, straight or curly, single or double.

    A rule can only be stated by quoting the word it governs, so a term inside
    quotation marks is being mentioned rather than used.
    """
    spans: list[tuple[int, int]] = []
    for pat in (r'"([^"\n]{1,400})"', r"'([^'\n]{1,400})'",
                r"“([^”\n]{1,400})”",
                r"‘([^’\n]{1,400})’"):
        for m in re.finditer(pat, text):
            spans.append((m.start(1), m.end(1)))
    return spans


def _in_spans(off: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= off < b for a, b in spans)


class Paper:
    """The assembled manuscript, with the structure the term rules need."""

    def __init__(self, text: str):
        self.text = text
        self.flat = _flat(text)
        self.low = self.flat.lower()
        # The manuscript is hard-wrapped at about 80 columns, so a two-word
        # marker ("two derived boundaries", "neither boundary") fails whenever
        # the wrap falls between its words.  Newlines and tabs become spaces --
        # a one-for-one substitution, so every offset still holds -- and the
        # windows below are matched against this copy instead.
        self.wtext = _WRAP_RE.sub(" ", self.low)
        self.starts = _starts(text)
        self.quoted = _quoted_spans(text)
        self.squashed = _squash(text)
        self._phrase_counts: dict[str, int] = {}

        self.headings: list[tuple[int, int, str]] = []   # (off, level, title)
        for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.M):
            self.headings.append((m.start(), len(m.group(1)), m.group(2)))
        self._hoffs = [h[0] for h in self.headings]

        # Paragraph blocks, for the sentence/paragraph tiers of the event rule.
        self.blocks: list[tuple[int, int]] = []
        pos = 0
        for chunk in re.split(r"\n\s*\n", text):
            self.blocks.append((pos, pos + len(chunk)))
            pos += len(chunk) + 2

    def heading_at(self, off: int) -> str:
        i = bisect.bisect_right(self._hoffs, off) - 1
        return self.headings[i][2] if i >= 0 else "front matter"

    def where(self, off: int) -> str:
        return f"line {_lineno(self.starts, off)} ({self.heading_at(off)[:60]})"

    def span_of(self, title: str) -> tuple[int, int] | None:
        """The body of a named subsection: its heading through the next one."""
        for i, (off, level, text) in enumerate(self.headings):
            if _squash(text).lower() == _squash(title).lower():
                end = len(self.text)
                for off2, level2, _ in self.headings[i + 1:]:
                    if level2 <= level:
                        end = off2
                        break
                return (off, end)
        return None

    def is_term(self, phrase: str, abbr: str, off: int) -> bool:
        """Is this run of words a term of the paper, or a coincidence of initials?

        Two tests, either sufficient: the abbreviation is written within 500
        characters of this occurrence, which is a gloss; or the phrase itself
        appears three times or more in the manuscript, which is a term used in
        full.
        """
        key = _squash(phrase).lower()
        near = re.compile(r"(?<![A-Za-z0-9])" + re.escape(abbr) +
                          r"(?![A-Za-z0-9])")
        if near.search(self.text[max(0, off - 500):off + len(phrase) + 500]):
            return True
        if key not in self._phrase_counts:
            # Tolerant of the manuscript's own spelling variants: a plural, a
            # hyphen or an en dash where another occurrence has a space.
            body = r"[\s\-‐-―]+".join(
                re.escape(w[:-1] if w.endswith("s") and len(w) > 3 else w) + "s?"
                for w in _WORD_RE.findall(key))
            self._phrase_counts[key] = len(re.findall(body, self.low))
        return self._phrase_counts[key] >= 3

    def block_at(self, off: int) -> tuple[int, int]:
        for a, b in self.blocks:
            if a <= off < b:
                return (a, b)
        return (off, off)

    def sentence_at(self, off: int) -> tuple[int, int]:
        """The sentence around an offset, inside its own paragraph or table row."""
        a, b = self.block_at(off)
        if self.text[a:b].lstrip().startswith("|"):        # a table: one row
            a = self.flat.rfind("\n", a, off) + 1
            nb = self.flat.find("\n", off, b)
            return (a, nb if nb >= 0 else b)
        left = max((self.flat.rfind(p, a, off) for p in (". ", ".\n", "; ", ": ")),
                   default=-1)
        a2 = left + 2 if left >= 0 else a
        right = min((p for p in (self.flat.find(". ", off, b),
                                 self.flat.find(".\n", off, b))
                     if p >= 0), default=-1)
        b2 = right + 1 if right >= 0 else b
        return (max(a, a2), min(b, b2))


def _window(low: str, off: int, back: int, fwd: int) -> str:
    return low[max(0, off - back):off + fwd]


def _ctx(text: str, off: int, width: int = 130) -> str:
    a = max(0, off - width // 3)
    return _squash(text[a:a + width])


# --------------------------------------------------------------------------
# rule 0 -- is the rule still stated?
# --------------------------------------------------------------------------

def _check_rule_present(p: Paper) -> list[dict]:
    findings = []
    for quote, what in ((_RULE_BOUNDARY, "that *L* is the assay floor in running "
                                         "text and 'boundary' never denotes a value"),
                        (_RULE_EVENT, "that the time-to-event endpoint is a first "
                                      "observed crossing below the assay floor")):
        if _squash(quote) not in p.squashed:
            findings.append({
                "severity": "medium",
                "kind": "term-rule-not-stated",
                "where": f"Methods, {_H_LIMIT}",
                "detail": ("This checker enforces a rule the Methods no longer "
                           f"state -- {what} -- so either the sentence was "
                           "edited and the checker must follow it, or the "
                           "discipline it imposes has been dropped."),
                "expected": _squash(quote)[:150],
                "found": "not present in the assembled manuscript",
            })
    for title in (_H_LIMIT, _H_RANGE, _H_ESTIM):
        if p.span_of(title) is None:
            findings.append({
                "severity": "low",
                "kind": "term-anchor-missing",
                "where": "Methods",
                "detail": (f'The Methods subsection "{title}" was not found, so '
                           "the exemption its body carries could not be applied "
                           "and the terms inside it are judged as running text."),
                "expected": f"### {title}",
                "found": "no such heading",
            })
    return findings


# --------------------------------------------------------------------------
# rule 1 -- "boundary" must not denote the assay floor L
# --------------------------------------------------------------------------

_BOUNDARY_RE = re.compile(r"\bboundar(?:y|ies)\b", re.I)

# A boundary's legitimate senses come in three strengths, and the strength
# decides what can override it.  The lists were built by reading all 26
# occurrences in the manuscript, not by guessing; what is graded here is the
# evidence, because a marker that merely sits somewhere in the same paragraph is
# not the same thing as one the word is part of.

# STRENGTH 1 -- the two derived boundaries, named anywhere in the window.  They
# are the paper's central contribution and nothing overrides them.
_BOUNDARY_OK_CTX = (
    r"identifiabilit",
    r"reachabilit",
    r"\bn\s*_?\s*reach\b",
    r"\bn\s*_?\s*id\b",
    r"dynamic range, and the two boundaries it sets",
)

# STRENGTH 2 -- spellings the occurrence is itself part of.  A quantifier over
# the pair cannot denote one value, and "the boundary case" is the six isolates
# sitting exactly on N_id.  These must COVER the occurrence, so that "two
# boundaries" in one sentence no longer clears a different "boundary" two lines
# further on.
_BOUNDARY_OK_COVER = (
    r"\btwo (?:derived )?boundaries\b",
    r"\bboth boundaries\b",
    r"\bneither boundary\b",
    r"\b(?:every|each|any|no) boundary\b",
    r"\bthe boundaries (?:require|locate|it sets)\b",
    r"\bsame boundaries\b",
    r"\bboundary case\b",
)

# STRENGTH 3 -- company a derived boundary keeps, and nothing more.  A boundary
# is fixed together with the class thresholds it is built from, and follows from
# the definitions alone; so these clear an otherwise unclassified occurrence.
# But they are single common words inside a 420-character window, and they must
# not be able to launder a sentence that says a count fell below the boundary.
# Floor-denoting grammar overrides them.
_BOUNDARY_OK_WEAK = (
    r"\bthresholds?\b",
    r"\bderived\b",
    r"\bdefinitions alone\b",
)
_BOUNDARY_OK_CTX_RE = [re.compile(p, re.I) for p in _BOUNDARY_OK_CTX]
_BOUNDARY_OK_COVER_RE = [re.compile(p, re.I) for p in _BOUNDARY_OK_COVER]
_BOUNDARY_OK_WEAK_RE = [re.compile(p, re.I) for p in _BOUNDARY_OK_WEAK]

# Spellings that name a value directly.  L is never a boundary, so these cannot
# be the derived boundaries whatever else is in the sentence.
_BOUNDARY_NEVER = (
    (r"\bassay(?:'s)? boundar(?:y|ies)\b", "assay boundary"),
    (r"\bboundar(?:y|ies)[\s,]{0,3}\bl\b", "the boundary L"),
    (r"\bl\b[\s,]{0,3}the (?:assay )?boundar(?:y|ies)\b", "L, the boundary"),
    (r"\bboundar(?:y|ies) of (?:quantification|detection)\b",
     "boundary of quantification/detection"),
    (r"\b(?:quantification|detection) boundar(?:y|ies)\b",
     "quantification/detection boundary"),
    (r"\bbelow-boundary\b", "below-boundary"),
    (r"\b(?:assay )?floor boundar(?:y|ies)\b", "floor boundary"),
)
_BOUNDARY_NEVER_RE = [(re.compile(p, re.I), name) for p, name in _BOUNDARY_NEVER]

# What the floor censors and the two derived boundaries do not: a measurement.
# N_reach and N_id are values too, and isolates and starting densities sit above
# and below them all through Section 3, so "above that boundary" is on its own no
# evidence at all -- the manuscript's own sentence "Above that boundary the
# lowest class is the only one compatible with a censored reading" is correct
# prose about N_id, and an earlier version of this rule reported it high when it
# was moved out of its subsection.  What cannot be said of a derived boundary is
# that a COUNT is below it.  The high tier therefore asks for both: the grammar
# of a value on the measurement scale, and a measurement noun in the position
# that grammar puts the subject.
_SCALE_NOUN = re.compile(
    r"\b(?:counts?|readings?|colonies|colony|cfu|mpn|values?|flasks?|plates?|"
    r"series|replicates?|observations?|measurements?)\b", re.I)

# Grammar with the measurement before the word: "a count below the boundary".
_FLOOR_ADJACENT = (
    r"\b(?:below|above|beneath|under|at|past|across|onto|to)[\s,]+"
    r"(?:the|its|their|that|this|his)?\s*(?:assay\s+)?boundar(?:y|ies)\b",
    r"\bcross(?:es|ed|ing)?\s+(?:below\s+)?(?:the|its|their)?\s*boundar(?:y|ies)\b",
    r"\b(?:fell|falls|fall|fallen|drops?|dropped|sits?|sat|rests?|rested|"
    r"reach(?:es|ed)?|hits?|hit|lands?|reads?|read)\s+"
    r"(?:\w+\s+){0,2}(?:below|above|at|on|to)\s+"
    r"(?:the|its|their)?\s*boundar(?:y|ies)\b",
)
# Grammar with the measurement after it: "the boundary was crossed by two
# replicates", "the boundary at which a count stops being reported".
_FLOOR_ADJACENT_PASSIVE = (
    r"\bboundar(?:y|ies)\s+(?:\w+\s+){0,2}"
    r"(?:is|was|were|are|gets?|got|had been|has been|been)\s+"
    r"(?:then\s+)?(?:crossed|reached|passed|hit|met|breached)\b",
    r"\bboundar(?:y|ies)\s+(?:at|below|above|beneath|under)\s+which\b",
    r"\bcensor(?:ed|ing|s)?\s+(?:\w+\s+){0,3}(?:the|its|their)\s*boundar(?:y|ies)\b",
    r"\bboundar(?:y|ies)\s+(?:that|which)\b[^.]{0,45}?"
    r"\b(?:fall|falls|fell|fallen|drop|drops|dropped|sit|sits|sat|"
    r"read|reads|go|goes|went|land|lands)\s+"
    r"(?:below|beneath|under)\b",
)
# A value with a plating density beside it needs no noun: N_reach and N_id are
# numeric too, but they are not quoted in CFU or MPN per mL the way a reporting
# threshold is.
_FLOOR_ADJACENT_VALUE = (
    r"\bboundar(?:y|ies)\s+(?:is|was|of|=)\s*\d",
    r"\bboundar(?:y|ies)\b[^.]{0,40}\b(?:CFU|MPN)\s*(?:/|per)\s*mL",
)
_FLOOR_ADJACENT_RE = [re.compile(p, re.I) for p in _FLOOR_ADJACENT]
_FLOOR_ADJACENT_PASSIVE_RE = [re.compile(p, re.I) for p in _FLOOR_ADJACENT_PASSIVE]
_FLOOR_ADJACENT_VALUE_RE = [re.compile(p, re.I) for p in _FLOOR_ADJACENT_VALUE]


def _covers(rx, win: str, rel: int) -> bool:
    """Does a match of this pattern cover the occurrence under judgement?

    Without the test, one floor-denoting phrase would incriminate every other
    occurrence of the word in the same 420-character window, and one allow-
    listed phrase would clear them all.  Both are wrong: the reason a word is
    reported has to be the words around that word.
    """
    return any(mm.start() <= rel <= mm.end() for mm in rx.finditer(win))


def _term_findings(p: Paper, word_re, exempt_spans, ctx_res, cover_res, weak_res,
                   never_res, adjacent_res, passive_res, value_res,
                   kind: str, term: str, replacement: str,
                   debug: bool = False) -> list[dict]:
    """One pass of the term rule, shared by "boundary" and "limit".

    Order matters, and the order is an argument about evidence.  The never-list
    runs first, because those spellings name a value outright.  The senses the
    Methods reserve run next, strongest first.  Floor-denoting grammar -- a
    measurement said to be below, at or crossing the word -- outranks the weak
    company markers, because one common word somewhere in the same paragraph is
    not a reason to disbelieve a sentence that says a count fell below the
    boundary.  Anything left unclassified is medium.
    """
    findings: list[dict] = []
    back = 230
    for m in word_re.finditer(p.flat):
        off = m.start()
        win = _window(p.wtext, off, back, 190)
        rel = off - max(0, off - back)
        quoted = _in_spans(off, p.quoted)

        hit = None
        for rx, name in never_res:
            # The match has to cover this occurrence, not another one further
            # along the same window, or one violation would report twice and
            # the wrong occurrence would carry the line number.
            if _covers(rx, win, rel):
                hit = name
                break
        if hit and not quoted:
            findings.append({
                "severity": "high",
                "kind": kind + "-names-the-floor",
                "where": p.where(off),
                "detail": (f'"{hit}" names the assay floor {term}. The Methods '
                           f'reserve "{term}" for the two derived boundaries and '
                           f"require the running-text short form to be "
                           f"{replacement}, so this spelling and that rule "
                           f"cannot both stand."),
                "expected": replacement,
                "found": _ctx(p.text, off),
            })
            continue

        if any(a <= off < b for a, b in exempt_spans):
            if debug:
                print(f"    ok  {p.where(off):48} exempt span")
            continue
        if quoted:
            if debug:
                print(f"    ok  {p.where(off):48} quoted, being mentioned")
            continue
        if any(rx.search(win) for rx in ctx_res):
            if debug:
                print(f"    ok  {p.where(off):48} reserved sense named in window")
            continue
        if any(_covers(rx, win, rel) for rx in cover_res):
            if debug:
                print(f"    ok  {p.where(off):48} allow-listed spelling")
            continue

        before = win[max(0, rel - 90):rel]
        after = win[rel:rel + 90]
        adjacent = bool(
            (any(_covers(rx, win, rel) for rx in adjacent_res)
             and _SCALE_NOUN.search(before))
            or (any(_covers(rx, win, rel) for rx in passive_res)
                and _SCALE_NOUN.search(after))
            or any(_covers(rx, win, rel) for rx in value_res))
        if not adjacent and any(rx.search(win) for rx in weak_res):
            if debug:
                print(f"    ok  {p.where(off):48} weak company, not floor-denoting")
            continue

        findings.append({
            "severity": "high" if adjacent else "medium",
            "kind": kind + ("-denotes-the-floor" if adjacent
                            else "-outside-its-declared-sense"),
            "where": p.where(off),
            "detail": (
                (f'"{term}" is used here of a measurement said to be below, at '
                 f"or crossing it, which is the assay floor. The Methods say "
                 f'"{term}" is left free for the two derived boundaries and '
                 f"that in running text the floor is {replacement}; both "
                 f"cannot hold.")
                if adjacent else
                (f'"{term}" appears here in none of the senses the Methods '
                 f"reserve it for. Check that it is not standing in for "
                 f"{replacement}.")),
            "expected": replacement,
            "found": _ctx(p.text, off),
        })
    return findings


def _check_boundary(p: Paper, debug: bool = False) -> list[dict]:
    exempt = []
    span = p.span_of(_H_RANGE)
    if span:
        exempt.append(span)           # the subsection that derives them
    if debug:
        print("  -- boundary --")
    return _term_findings(p, _BOUNDARY_RE, exempt,
                          _BOUNDARY_OK_CTX_RE, _BOUNDARY_OK_COVER_RE,
                          _BOUNDARY_OK_WEAK_RE, _BOUNDARY_NEVER_RE,
                          _FLOOR_ADJACENT_RE, _FLOOR_ADJACENT_PASSIVE_RE,
                          _FLOOR_ADJACENT_VALUE_RE,
                          "boundary", "boundary", "the assay floor *L*", debug)


# --------------------------------------------------------------------------
# rule 2 -- "the limit" must not denote the assay floor L either
# --------------------------------------------------------------------------

_LIMIT_RE = re.compile(r"\blimits?\b", re.I)

# Censoring notation, wherever the Methods put it.  The Estimation subsection is
# exempt whole, below, but these markers hold the exemption to the notation
# itself, so that renaming the heading cannot turn a Tobit likelihood into a
# term violation.  They are the one limit sense that outranks floor-denoting
# grammar, because "the probability that it fell below its own limit" IS the
# likelihood, and rewriting it would be the error rather than the fix.
_LIMIT_OK_CTX = (
    r"tobit",
    r"truncated at",
    r"Φ",
    r"beal",
    r"rubin",
    r"two kinds of limit, kept apart",
)
# Named assay terms, interval ends, and the manuscript's own licence to use the
# word when reporting what a source states: the occurrence has to be part of
# them, not merely near them.
_LIMIT_OK_COVER = (
    r"limits? of (?:quantification|detection)",
    r"(?:quantification|detection) limits?",
    r"\b(?:upper|lower)\s+limits?\b",
    # a constraint on something, not a value: "a limit on how deep the assay
    # can see, the other on how long it looks"
    r"\blimits?\s+on\b",
    # the deposit's own flag columns, always hyphenated as a modifier
    r"\b(?:below|above)-limit\b",
    r"\b(?:state[sd]?|report(?:s|ed)?|nam(?:e|es|ed|ing)|quote[sd]?|"
    r"record(?:s|ed)?|declares?|gives?|carr(?:y|ies))\s+"
    r"(?:no|a|any|the|its|their)?\s*limits?\b",
)
# Nothing is weak company for "limit": every legitimate sense above is either a
# phrase the word belongs to or the censoring notation, so there is no third
# tier here.
_LIMIT_OK_WEAK = ()
_LIMIT_OK_CTX_RE = [re.compile(pat, re.I) for pat in _LIMIT_OK_CTX]
_LIMIT_OK_COVER_RE = [re.compile(pat, re.I) for pat in _LIMIT_OK_COVER]
_LIMIT_OK_WEAK_RE = [re.compile(pat, re.I) for pat in _LIMIT_OK_WEAK]

_LIMIT_NEVER = (
    (r"\bassay(?:'s)? limits?\b", "assay limit"),
    (r"\bthe limit[\s,]{0,3}\bl\b", "the limit L"),
    (r"\bl\b[\s,]{0,3}the (?:assay )?limit\b", "L, the limit"),
)
_LIMIT_NEVER_RE = [(re.compile(p, re.I), name) for p, name in _LIMIT_NEVER]

_LIMIT_ADJACENT = (
    r"\b(?:below|above|beneath|under|at|past|across|to)[\s,]+"
    r"(?:the|its|their|that|this)?\s*(?:assay\s+)?limits?\b",
    r"\bcross(?:es|ed|ing)?\s+(?:below\s+)?(?:the|its|their)?\s*limits?\b",
    r"\b(?:fell|falls|fall|fallen|drops?|dropped|sits?|sat|rests?|rested|"
    r"reach(?:es|ed)?|hits?|hit|reads?|read)\s+"
    r"(?:\w+\s+){0,2}(?:below|above|at|to)\s+(?:the|its|their)?\s*limits?\b",
)
_LIMIT_ADJACENT_PASSIVE = (
    r"\bthe limits?\s+(?:\w+\s+){0,2}"
    r"(?:is|was|were|are|gets?|got|had been|has been|been)\s+"
    r"(?:then\s+)?(?:crossed|reached|passed|hit|met|breached)\b",
    r"\bthe limits?\s+(?:at|below|above|beneath|under)\s+which\b",
    r"\bcensor(?:ed|ing|s)?\s+(?:\w+\s+){0,3}(?:the|its|their)\s*limits?\b",
    r"\bthe limits?\s+(?:that|which)\b[^.]{0,45}?"
    r"\b(?:fall|falls|fell|fallen|drop|drops|dropped|sit|sits|sat|"
    r"read|reads|go|goes|went|land|lands)\s+"
    r"(?:below|beneath|under)\b",
)
_LIMIT_ADJACENT_VALUE = (
    r"\bthe limits?\s+(?:is|was|of|=)\s*\d",
)
_LIMIT_ADJACENT_RE = [re.compile(p, re.I) for p in _LIMIT_ADJACENT]
_LIMIT_ADJACENT_PASSIVE_RE = [re.compile(p, re.I) for p in _LIMIT_ADJACENT_PASSIVE]
_LIMIT_ADJACENT_VALUE_RE = [re.compile(p, re.I) for p in _LIMIT_ADJACENT_VALUE]


def _check_limit(p: Paper, debug: bool = False) -> list[dict]:
    exempt = []
    # DELIBERATE EXEMPTION 1.  The subsection that defines the terms.  "Limit"
    # is the word being disambiguated there and it cannot be disambiguated
    # without being written.
    span = p.span_of(_H_LIMIT)
    if span:
        exempt.append(span)
    # DELIBERATE EXEMPTION 2.  Tobit and censoring notation in Estimation:
    # "log Phi((limit - mu)/sigma)", "truncated at its own limit", "what
    # happened below the limit".  That is how the likelihood is written.
    span = p.span_of(_H_ESTIM)
    if span:
        exempt.append(span)
    if debug:
        print("  -- limit --")
    return _term_findings(p, _LIMIT_RE, exempt,
                          _LIMIT_OK_CTX_RE, _LIMIT_OK_COVER_RE,
                          _LIMIT_OK_WEAK_RE, _LIMIT_NEVER_RE,
                          _LIMIT_ADJACENT_RE, _LIMIT_ADJACENT_PASSIVE_RE,
                          _LIMIT_ADJACENT_VALUE_RE,
                          "limit", "limit", "the assay floor *L*", debug)


# --------------------------------------------------------------------------
# rule 3 -- clearance and sterilisation are not the name of a first crossing
# --------------------------------------------------------------------------

_OLD_NAMES = re.compile(
    r"\b(?:clearance|clearances|sterilisations?|sterilizations?|"
    r"sterilised|sterilized|steriliz(?:ing|ation)|bacterial clearance)\b", re.I)

# What a sentence about the renamed event looks like.
_EVENT_CUE = re.compile(
    r"\bfirst (?:observed )?crossing|crossing below|crosses below|cross below"
    r"|below (?:its |their |the )?(?:own )?(?:assay )?floor"
    r"|time-to-event|time to event|crossing times?|first crossings?"
    r"|\bthe event\b|survival likelihood|right-censored at", re.I)

# The manuscript disowns both names twice, and must keep being able to.  But a
# negation is only a disavowal of THIS word when this word is what it negates.
# "is not clearance", "are not clearances", "is not read as clearance,
# sterilisation or the end of a culture" all disown the name.  "on data it was
# not built from, the depth at which a sterilisation claim ..." negates a
# different verb entirely, and an earlier version of this rule, which asked only
# whether a negation stood anywhere in the ninety characters before the word,
# was silenced by any of them -- so "The schedule is not dense, so clearance is
# scored at the first crossing below the floor" went unreported.
_NEG_CUE = re.compile(
    r"\b(?:not|never|no|neither|nor)\b|\b(?:rather than|instead of|"
    r"as opposed to)\b", re.I)
# What may stand between the negation and the name without breaking the link:
# the copula and the naming verbs, articles, coordination, and the other names
# of the same family, because the manuscript disowns them as a list.
_LINK_WORDS = {
    "read", "as", "a", "an", "the", "of", "is", "are", "be", "been", "being",
    "and", "or", "nor", "called", "call", "named", "name", "term", "termed",
    "labelled", "labeled", "simply", "merely", "really", "quite", "exactly",
    "just", "longer", "it", "this", "that", "them", "either", "any", "true",
    "clearance", "clearances", "sterilisation", "sterilisations",
    "sterilization", "sterilizations", "sterilised", "sterilized", "bacterial",
}
_LINK_RE = re.compile(r"[A-Za-z]+")

# Naming a thing is not the same as mentioning it.  "We call it clearance" in a
# paragraph about the crossing event renames the endpoint even though the
# crossing is described in the sentence before.
_NAMING_VERB = re.compile(
    r"\b(?:call(?:s|ed|ing)?|nam(?:e|es|ed|ing)|term(?:s|ed)?|"
    r"label(?:s|led|ed)?|known as|referred to as|refer(?:s|red)? to .{0,20}as|"
    r"record(?:s|ed)? as|report(?:s|ed)? as|treats? .{0,20}as|scored? as|"
    r"is the event|as the event)\b[^.]{0,30}$", re.I)


def _disowned(text: str, sa: int, off: int) -> bool:
    """Is the name at `off` the thing a nearby negation is denying?"""
    for m in _NEG_CUE.finditer(text[max(sa, off - 60):off]):
        between = text[max(sa, off - 60):off][m.end():]
        if len(between) > 30:
            continue
        if all(w.lower() in _LINK_WORDS for w in _LINK_RE.findall(between)):
            return True
    return False


def _check_event_names(p: Paper, debug: bool = False) -> list[dict]:
    findings: list[dict] = []
    for m in _OLD_NAMES.finditer(p.flat):
        off = m.start()
        sa, sb = p.sentence_at(off)
        sent = p.flat[sa:sb]
        disowned = _disowned(p.flat, sa, off)
        if debug:
            print(f"    {p.where(off):48} cue="
                  f"{bool(_EVENT_CUE.search(sent))} disowned={bool(disowned)}")
        if disowned:
            continue                       # "is not clearance and not sterilisation"
        if _EVENT_CUE.search(sent):
            findings.append({
                "severity": "high",
                "kind": "renamed-event-called-clearance",
                "where": p.where(off),
                "detail": (
                    f'"{m.group(0)}" names the endpoint in a sentence about the '
                    "crossing event. The Methods record a first observed "
                    "crossing below the assay floor and say so because 60 per "
                    "cent of the series that cross read above the floor again; "
                    "the two readings cannot both be right."),
                "expected": "a first observed crossing below the assay floor",
                "found": _ctx(p.text, off, 170),
            })
            continue
        ba, bb = p.block_at(off)
        if not _EVENT_CUE.search(p.flat[ba:bb]):
            continue
        if _NAMING_VERB.search(p.flat[max(ba, off - 40):off]):
            findings.append({
                "severity": "high",
                "kind": "renamed-event-called-clearance",
                "where": p.where(off),
                "detail": (
                    f'"{m.group(0)}" is given as the NAME of the endpoint in a '
                    "paragraph about the first observed crossing below the "
                    "assay floor. The Methods record a first observed crossing "
                    "and say so because 60 per cent of the series that cross "
                    "read above the floor again; the two readings cannot both "
                    "be right."),
                "expected": "a first observed crossing below the assay floor",
                "found": _ctx(p.text, off, 170),
            })
            continue
        findings.append({
            "severity": "medium",
            "kind": "renamed-event-name-nearby",
            "where": p.where(off),
            "detail": (
                f'"{m.group(0)}" appears in a paragraph that is about the '
                "first observed crossing below the assay floor, though not "
                "in the same sentence. Check that it is describing a claim "
                "about depth and not naming the event."),
            "expected": "a first observed crossing below the assay floor",
            "found": _ctx(p.text, off, 170),
        })
    return findings


# --------------------------------------------------------------------------
# rule 4 -- abbreviations
# --------------------------------------------------------------------------

_ABBR_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z]{2,6})(?![A-Za-z0-9])")
_WORD_RE = re.compile(r"[A-Za-z]+")

# Exemptions, each judged against what actually occurs in this manuscript.
_ABBR_STANDARD = {
    # units and assay terms that no journal in this field expands
    "CFU": "colony-forming units, the standard unit",
    "MPN": "most probable number, expanded in the Introduction as well",
    "MIC": "minimum inhibitory concentration, standard",
    "LOD": "limit of detection, a standard assay term and Table 16's subject",
    "LOQ": "limit of quantification, named in full in the prose above Table 16",
    # standard statistics
    "CI": "confidence interval; the manuscript writes '95 per cent CI' throughout",
    "IQR": "interquartile range; the range is named in full at the same result",
    # drug and deposit codes, used only as arm labels or column names in tables
    # whose legends name the drug in full
    "INH": "isoniazid, an arm label in Tables 6, 10 and S4",
    "MXF": "moxifloxacin, an arm label in Tables 6 and 10",
    "RIF": "rifampicin, a field name in Table S4",
    "MGIT": "the deposit's own drug-susceptibility field name, Table S4",
    "DST": "the deposit's own drug-susceptibility field name, Table S4",
    "IS": "the deposit's isoniazid-susceptible code, Table 5",
    "IR": "the deposit's isoniazid-resistant code, Table 5",
    "BQL": "the six-laboratory file's own column name; Table 16's legend "
           "expands it as the below-quantification-limit column",
    "AQL": "the six-laboratory file's own column name; Table 16's legend "
           "expands it as the above-quantification-limit column",
    # names of bodies, which are their acronyms
    "NCCLS": "the standards body's name",
    "CLSI": "the standards body's name",
    # licence tags and table fillers
    "CC": "Creative Commons licence tag",
    "BY": "Creative Commons licence tag",
    "NA": "not applicable, a table filler",
}
# "OR" is an English word in lower case and an odds ratio in upper case.  The
# lower-case test below would exempt it, and it should not: the manuscript uses
# it as a statistic and expands it.
_ABBR_ALWAYS = {"OR"}

_FUNCTION_WORDS = {"of", "the", "a", "an", "for", "and", "in", "on", "to",
                   "per", "under", "by", "with", "at", "from"}


def _regions(p: Paper) -> list[tuple[str, list[tuple[int, int]]]]:
    """Title, Abstract and main text, which a reader may meet separately."""
    title: list[tuple[int, int]] = []
    for m in re.finditer(r"^(?:short_)?title:\s*.+$", p.text, re.M):
        title.append((m.start(), m.end()))
    for off, level, _ in p.headings:
        if level == 1:
            end = p.flat.find("\n", off)
            title.append((off, end if end >= 0 else len(p.text)))
            break

    abstract: list[tuple[int, int]] = []
    span = p.span_of("Abstract")
    if span:
        abstract.append(span)

    # Everything that is neither title nor Abstract is main text, gaps
    # included.  Taking the main region to start where the Abstract ends left
    # the YAML keywords, the author block and the figure counts inside no
    # region at all, so an abbreviation written there was never judged.
    used = sorted(title + abstract)
    main: list[tuple[int, int]] = []
    cur = 0
    for a, b in used:
        if a > cur:
            main.append((cur, a))
        cur = max(cur, b)
    if cur < len(p.text):
        main.append((cur, len(p.text)))
    main = [(a, b) for a, b in main if b > a]
    return [("the title", title), ("the Abstract", abstract),
            ("the main text", main)] if used or main else []


def _region_text(p: Paper, spans: list[tuple[int, int]]) -> list[tuple[int, str]]:
    return [(a, p.flat[a:b]) for a, b in spans]


def _expansion_offsets(p: "Paper", chunks: list[tuple[int, str]],
                       abbr: str, spans: list | None = None) -> list[int]:
    """Offsets of every phrase whose word initials spell the abbreviation.

    Function words may be skipped, so "minimum duration for killing" expands
    MDK and "area under the curve" expands AUC; the first and last word of the
    phrase must both be used, so a run of prose cannot drift into a match.

    Initials alone are far too cheap -- two letters will hit some pair of
    adjacent words on almost any page -- so a candidate counts as an expansion
    only where the manuscript treats it as a term: either the abbreviation is
    written beside it somewhere, which is what expanding at first use looks
    like, or the phrase is used in full three times or more, which is a term
    the reader has met whether or not it was ever glossed.
    """
    target = abbr.lower()
    out: list[int] = []
    for base, chunk in chunks:
        words = [(m.start(), m.group(0)) for m in _WORD_RE.finditer(chunk)]
        for i in range(len(words)):
            for k in range(len(target), min(len(target) + 3, len(words) - i) + 1):
                win = words[i:i + k]
                if len(win) < len(target):
                    continue
                span_txt = chunk[win[0][0]:win[-1][0] + len(win[-1][1])]
                if "|" in span_txt or "\n" in span_txt or len(span_txt) > 90:
                    continue
                if any(w.isupper() and len(w) > 1 for _, w in win):
                    continue
                used: list[int] = []
                j = 0
                for wi, (_, w) in enumerate(win):
                    if j < len(target) and w[0].lower() == target[j]:
                        used.append(wi)
                        j += 1
                    elif w.lower() not in _FUNCTION_WORDS:
                        j = -1
                        break
                if j != len(target) or len(used) != len(target):
                    continue
                if used[0] != 0 or used[-1] != len(win) - 1:
                    continue
                if any(len(win[wi][1]) < 3 for wi in used):
                    continue
                if not any(len(win[wi][1]) >= 5 for wi in used):
                    continue      # "over days" is not an expansion of OD
                off = base + win[0][0]
                if not p.is_term(span_txt, abbr, off):
                    continue
                out.append(off)
                if spans is not None:
                    spans.append((off, off + len(span_txt)))
    return out


def _expansion_spans(p: "Paper", abbr: str) -> list[tuple[int, int]]:
    """The (start, end) of every expansion of this abbreviation in the paper.

    The first-use rule needs only the starts; the confusable-pair rule needs
    the words of the phrase itself, and reading them off a fixed window pulled
    in half the surrounding sentence.
    """
    cache = p.__dict__.setdefault("_exp_spans", {})
    if abbr not in cache:
        spans: list[tuple[int, int]] = []
        _expansion_offsets(p, [(0, p.flat)], abbr, spans)
        cache[abbr] = spans
    return cache[abbr]


def _gloss_offsets(p: "Paper", chunks: list[tuple[int, str]],
                   abbr: str) -> list[int]:
    """Offsets of a gloss written beside the abbreviation itself.

    Some abbreviations are cut from inside a word rather than from initials:
    the deposit's label is glossed as "conventionally multidrug-resistant", and
    the D of MDR is the fourth letter of "multidrug".  A looser reading is
    allowed for that -- the first and last letters begin the first and last
    word, the rest appear in order anywhere between -- but only within 200
    characters of the abbreviation, which is the only place a gloss can be.
    """
    target = abbr.lower()
    tok = re.compile(r"(?<![A-Za-z0-9])" + re.escape(abbr) + r"(?![A-Za-z0-9])")
    out: list[int] = []
    for base, chunk in chunks:
        for m in tok.finditer(chunk):
            a = max(0, m.start() - 200)
            win = chunk[a:m.end() + 200]
            words = [(mm.start(), mm.group(0).lower())
                     for mm in _WORD_RE.finditer(win)]
            for i in range(len(words)):
                for k in range(1, len(target) + 1):
                    grp = words[i:i + k]
                    if len(grp) < k:
                        break
                    if grp[0][1][0] != target[0] or grp[-1][1][0] != target[-1]:
                        continue
                    if grp[0][1] == target:
                        continue                      # the abbreviation itself
                    span = win[grp[0][0]:grp[-1][0] + len(grp[-1][1])]
                    if "|" in span or chr(10) in span or len(span) > 60:
                        continue
                    if sum(len(w) for _, w in grp) < 8:
                        continue
                    j = 0
                    for ch in span.lower():
                        if ch.isalpha() and j < len(target) and ch == target[j]:
                            j += 1
                    if j == len(target):
                        out.append(base + a + grp[0][0])
    return out


def _abbr_occurrences(p: Paper) -> list[tuple[int, str]]:
    """Every all-caps token that is behaving like an abbreviation."""
    out = []
    for m in _ABBR_RE.finditer(p.text):
        tok, off = m.group(1), m.start(1)
        before = p.text[off - 1] if off else " "
        after = p.text[m.end(1)] if m.end(1) < len(p.text) else " "
        if before == "_" or after == "_":
            continue          # a deposit field name, quoted verbatim: INH_MGIT_DST
        if before == "-" and off >= 2 and p.text[off - 2].islower():
            continue          # part of a compound identifier: Sample-ID
        out.append((off, tok))
    return out


def _expansion_words(p: Paper, tok: str) -> set[str]:
    """Every word of every phrase the paper uses to expand this abbreviation.

    These are the abbreviation's own definition, and they clear an occurrence
    however rarely they occur: a sentence that writes "an MDK is a duration"
    is using MDK for what MDK means, whatever else stands beside it.
    """
    cache = p.__dict__.setdefault("_exp_words", {})
    if tok in cache:
        return cache[tok]
    out: set[str] = set()
    for a, b in _expansion_spans(p, tok):
        out |= {w for w in _WORD_RE.findall(p.low[a:b]) if len(w) >= 4}
    for o in _gloss_offsets(p, [(0, p.flat)], tok):
        out |= {w for w in _WORD_RE.findall(p.low[o:o + 40]) if len(w) >= 4}
    cache[tok] = out
    return out


def _is_status_word(p: Paper, tok: str) -> bool:
    """An all-caps rendering of a word the manuscript also uses in lower case.

    NOT SUPPORTED, DERIVED, INFERRED, FLAGGED, PROXY, NONE and SLOWER are
    verdict and status codes in the tables, not abbreviations.  A token the
    paper actually writes out in full is an abbreviation whatever its casing
    elsewhere, or one stray lower-case spelling would switch the token off.
    """
    if tok in _ABBR_ALWAYS:
        return False
    n = len(re.findall(r"(?<![A-Za-z0-9])" + tok.lower() + r"(?![A-Za-z0-9])",
                       p.text))
    if n < 2:
        return False
    return not _expansion_spans(p, tok)


def _check_abbreviations(p: Paper, debug: bool = False) -> list[dict]:
    findings: list[dict] = []
    occ = _abbr_occurrences(p)
    real: dict[str, list[int]] = defaultdict(list)
    for off, tok in occ:
        if tok in _ABBR_STANDARD or _is_status_word(p, tok):
            continue
        real[tok].append(off)

    # (a) expanded before it is used, region by region
    for label, spans in _regions(p):
        chunks = _region_text(p, spans)
        for tok, offs in sorted(real.items()):
            here = sorted(o for o in offs
                          if any(a <= o < b for a, b in spans))
            if not here:
                continue
            first = here[0]
            exps = (_expansion_offsets(p, chunks, tok)
                    + _gloss_offsets(p, chunks, tok))
            if debug:
                print(f"    {tok:6} in {label:14} first at "
                      f"line {_lineno(p.starts, first)}, "
                      f"{len(exps)} expansion(s)")
            if any(e <= first + 200 for e in exps):
                continue
            findings.append({
                "severity": "medium",
                "kind": "abbreviation-not-expanded",
                "where": p.where(first),
                "detail": (
                    f'"{tok}" is used in {label} with no expansion of it '
                    f"anywhere in {label}"
                    + (", though it is expanded later in the paper"
                       if (_expansion_offsets(p, [(0, p.flat)], tok)
                           or _gloss_offsets(p, [(0, p.flat)], tok))
                       else "")
                    + ". The title, the Abstract and the main text are read "
                      "separately, so each has to carry its own first use."),
                "expected": f"the term written out at the first use of {tok}",
                "found": _ctx(p.text, first),
            })

    # (b) one abbreviation, two meanings.  Confusable pairs are discovered:
    # same length, one letter apart.  The pairing runs over the abbreviations
    # the expansion rule judges and not over the exempt list: the only
    # Hamming-one pairs it would add are OR/IR and CI/CC, two statistics
    # against two deposit and licence codes, where the risk of a false high
    # buys nothing a reader would ever confuse.
    toks = [t for t, offs in real.items() if len(offs) >= 2]
    for i, a in enumerate(sorted(toks)):
        for b in sorted(toks)[i + 1:]:
            if len(a) != len(b):
                continue
            if sum(1 for x, y in zip(a, b) if x != y) != 1:
                continue
            findings += _confusion(p, a, real[a], b, real[b], debug)
            findings += _confusion(p, b, real[b], a, real[a], debug)
    return findings


# Words too common in this manuscript to be anyone's distinctive company.
_CONF_STOP = _FUNCTION_WORDS | {
    "is", "are", "was", "were", "be", "been", "being", "it", "its", "that",
    "this", "these", "those", "as", "or", "not", "no", "but", "which", "each",
    "every", "one", "two", "all", "any", "has", "have", "had", "than", "then",
    "so", "if", "when", "where", "there", "their", "they", "we", "our", "can",
    "cannot", "only", "also", "both", "same",
}


def _company(p: Paper, off: int) -> set[str]:
    return {w for w in _WORD_RE.findall(_window(p.low, off, 130, 130))
            if len(w) >= 4 and w not in _CONF_STOP}


def _side_by_side(p: Paper, off: int, other: str) -> bool:
    """Is the other abbreviation written beside this one?

    Where the two stand together the surrounding words are shared on purpose
    and discriminate nothing, so that occurrence is not judged.  This used to
    be a test on the pair as a whole, which meant one sentence naming both --
    "the MDR label and the MDK endpoint" -- switched the rule off for the whole
    manuscript.
    """
    return re.search(r"(?<![A-Za-z0-9])" + re.escape(other) +
                     r"(?![A-Za-z0-9])",
                     _window(p.text, off, 220, 220)) is not None


def _confusion(p: Paper, tok: str, offs: list[int], other: str,
               other_offs: list[int], debug: bool = False) -> list[dict]:
    """Report an occurrence written in the other abbreviation's company.

    Company means REPEATED company: a word in two or more of the other
    abbreviation's windows and in none of this one's.  A word appearing once
    beside this abbreviation is not evidence that this abbreviation was meant
    -- with nine occurrences that vocabulary is most of a page -- but a word
    the other one keeps beside it twice, which this one never does, is.  The
    abbreviation's own expansion always exculpates, however rarely it occurs:
    "an MDK is a duration" uses MDK for what MDK means.
    """
    doc = p.__dict__.setdefault("_doc_freq", Counter(_WORD_RE.findall(p.low)))
    theirs: Counter = Counter()
    for o in other_offs:
        theirs.update(_company(p, o))
    theirs_rep = {w for w, n in theirs.items() if n >= 2}
    theirs_any = set(theirs)
    gloss = {w for w in _expansion_words(p, tok) if w not in _CONF_STOP}
    drop = {tok.lower(), other.lower()}
    findings = []
    for off in offs:
        if _side_by_side(p, off, other):
            if debug:
                print(f"    {tok} at line {_lineno(p.starts, off)}: "
                      f"{other} beside it, not judged")
            continue
        # The occurrence under suspicion is left out of its own profile.  Left
        # in, a substituted abbreviation would supply the very company that is
        # meant to clear it, and no substitution could ever be detected.
        mine: Counter = Counter()
        for o in offs:
            if o != off:
                mine.update(_company(p, o))
        mine_rep = {w for w, n in mine.items() if n >= 2}
        # A word this abbreviation repeats but the other one also uses says
        # nothing either way, so it does not exculpate.
        own_marks = (mine_rep - theirs_any) - drop
        sib_marks = (theirs_rep - mine_rep - gloss) - drop
        win = _company(p, off) - drop
        here = sorted(win & sib_marks)
        mine_here = sorted(win & own_marks)
        gloss_here = sorted(win & gloss)
        rare = [w for w in here if doc[w] <= 20]
        if debug and here:
            print(f"    {tok} at line {_lineno(p.starts, off)}: "
                  f"{len(here)} {other}-only, {len(mine_here)} {tok}-only, "
                  f"{len(gloss_here)} of its expansion, {len(rare)} rare")
        # A word of its own expansion settles it: the abbreviation is being
        # used for what it means.  Its ordinary company only has to be
        # outweighed -- one shared word against nine of the other's, five of
        # them rare, is not a reason to say nothing.
        if (gloss_here or len(here) < 3 or len(rare) < 2
                or len(here) < 3 * len(mine_here) + 2):
            continue
        findings.append({
            "severity": "high",
            "kind": "abbreviation-two-meanings",
            "where": p.where(off),
            "detail": (
                f'"{tok}" is written here in the company "{other}" keeps '
                f"({', '.join(rare[:4])}), in none of its own, and with no "
                f"word of its own expansion beside it, so one of the two "
                f"abbreviations is standing in for the other. An abbreviation "
                f"cannot denote two things."),
            "expected": other,
            "found": _ctx(p.text, off, 170),
        })
    return findings


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------

def check(text: str, ctx: dict) -> list[dict]:
    """Return a list of findings.  Empty list means clean."""
    if not text:
        root = Path(ctx.get("root", "."))
        text = (root / "manuscript" / "PAPER_COMPLETE.md").read_text(
            encoding="utf-8")
    p = Paper(text)
    findings = (_check_rule_present(p)
                + _check_boundary(p)
                + _check_limit(p)
                + _check_event_names(p)
                + _check_abbreviations(p))
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 3), f["kind"],
                                 f["where"]))
    return findings


# --------------------------------------------------------------------------
# self-test: plant the errors this module exists to catch
# --------------------------------------------------------------------------

_PLANTS = [
    # ---- the floor called a boundary -------------------------------------
    ("the floor called a boundary, in floor-denoting context",
     "In the six-laboratory deposit that value is a property of\nthe plated volume",
     "In the six-laboratory deposit a reading below the boundary is a property "
     "of\nthe plated volume", "high"),
    ("the same defect in a paragraph that also says 'thresholds'",
     "named before any reading is taken.",
     "named before any reading is taken. Counts that fall below the boundary "
     "are not reported as counts.", "high"),
    ("the same defect written in the passive",
     "What holds without\nany assumption about the floor is that the separation "
     "collapses.",
     "What holds without\nany assumption about the floor is that the separation "
     "collapses. The boundary was crossed by two of the three replicates at "
     "day 14.", "high"),
    ("the same defect in a table legend",
     "FLAGGED means the deposit marks below-limit readings without naming a value",
     "FLAGGED means the deposit marks readings below the boundary without "
     "naming a value", "high"),
    ("the floor renamed the assay boundary",
     "Throughout this paper *L* is\ntherefore an **operational assay floor**",
     "Throughout this paper *L* is\ntherefore an **assay boundary**", "high"),
    ("the floor written as the boundary L",
     "The floor censors the measurement scale: a count below *L*",
     "The boundary *L* censors the measurement scale: a count below *L*", "high"),
    ("the floor called the quantification boundary",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. No "
     "quantification boundary is stated for that arm.", "high"),
    ("the word used in none of the senses the Methods reserve",
     "The deposit carries apramycin at 1, 4, 8, 32 and 128 \u00b5g/mL.",
     "The deposit carries apramycin at 1, 4, 8, 32 and 128 \u00b5g/mL. A boundary "
     "of this kind is what the deposit reports.", "medium"),

    ("the floor called a boundary in a table BODY cell",
     "| Vijay 2024 | no | no | 23 | MPN per mL | INFERRED | operational assay "
     "floor |",
     "| Vijay 2024 | no | no | 23 | MPN per mL | INFERRED | the boundary below "
     "which counts are not reported |", "high"),
    ("the same defect with the preposition stranded",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. That "
     "is the boundary that counts fall below.", "high"),

    # ---- the floor called a limit ----------------------------------------
    ("readings described as below the limit, outside Estimation",
     "and there 29 of 72 treated\nflasks ever fall below the floor",
     "and there 29 of 72 treated\nflasks ever fall below the limit", "high"),
    ("the same defect in a paragraph that also says 'quantification limit'",
     "Institute A's other platings put it near\n*h* = 2.4, so including it "
     "would widen the spread rather than narrow it.",
     "Institute A's other platings put it near\n*h* = 2.4, so including it "
     "would widen the spread rather than narrow it. Three of the four readings "
     "sit below the limit at that plating.", "high"),
    ("the floor renamed the assay limit",
     "carrying all three fields the boundaries require, and it was analysed cold.",
     "carrying all three fields the boundaries require, and its assay limit was "
     "analysed cold.", "high"),
    ("the word used of a value outside every reserved sense",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. The "
     "limit is a property of the deposit rather than of the drug.", "medium"),

    ("the floor called a limit in a table BODY cell",
     "| Dubey 2026 | no | no | 10 | CFU per mL | DERIVED | minimum reportable "
     "positive count |",
     "| Dubey 2026 | no | no | 10 | CFU per mL | DERIVED | the assay limit |",
     "high"),

    # ---- the renamed event -----------------------------------------------
    ("the first crossing called clearance",
     "The\nevent it records is not clearance and not sterilisation but a "
     "**first observed\ncrossing below the assay floor**",
     "The\nevent it records is clearance, a **first observed\ncrossing below "
     "the assay floor**", "high"),
    ("the first crossing called sterilisation in the Methods",
     "**Time-to-event analysis** treats the **first observed crossing below the "
     "assay\nfloor** as the event",
     "**Time-to-event analysis** treats **sterilisation** as the event", "high"),
    ("clearance named as the event with an unrelated negation in the sentence",
     "The time-to-event analysis runs at the 100 \u00b5L\nquadruplicate plating,",
     "The schedule is not dense, so the clearance time is measured at the 100 "
     "\u00b5L\nquadruplicate plating,", "high"),
    ("the event defined in one sentence and renamed in the next",
     "The time-to-event analysis runs at the 100 \u00b5L\nquadruplicate plating,",
     "The event is a first observed crossing below the assay floor. We call it "
     "clearance throughout. The time-to-event analysis runs at the 100 "
     "\u00b5L\nquadruplicate plating,", "high"),
    ("an old event name loose in the paragraph that defines the event",
     "cross, 60 per cent read above the floor again at a later visit.",
     "cross, 60 per cent read above the floor again at a later visit. "
     "Clearance is tabulated per laboratory in Table 8.", "medium"),

    # ---- abbreviations ----------------------------------------------------
    ("an abbreviation used in the Abstract with no expansion there",
     "adjustment for starting density, and isoniazid resistance, which does "
     "not.",
     "adjustment for starting density, and isoniazid resistance, which does "
     "not. The PDA of each isolate is reported.", "medium"),
    ("an abbreviation used in the front matter, outside title and Abstract",
     "**Authors:** [to be inserted]",
     "**Authors:** [to be inserted] (PDA consortium)", "medium"),
    ("an abbreviation first met in a table legend",
     "**Table 13.** The same 32-fold concentration range",
     "**Table 13.** Rows are grouped by RGM status. The same 32-fold "
     "concentration range", "medium"),
    ("MDK written for the deposited MDR label category, in a table row",
     "| Vijay clinical | 15-day | all isolates | label is Low, Medium or High "
     "(drops 'MDR') | 203 | -14 |",
     "| Vijay clinical | 15-day | all isolates | label is Low, Medium or High "
     "(drops 'MDK') | 203 | -14 |", "high"),
    ("the same substitution in the Methods prose",
     "the MDR tolerance label is a fourth,",
     "the MDK tolerance label is a fourth,", "high"),
    ("the same substitution in the sentence that defines the label",
     'the deposit writes literally as "MDR", conventionally multidrug-resistant',
     'the deposit writes literally as "MDK", conventionally multidrug-resistant',
     "high"),

    ("the same substitution where one word of its own company also stands by",
     'category, the "MDR" label above, that no ordered analysis can place',
     'category, the "MDK" label above, that no ordered analysis can place',
     "high"),

    # ---- the guards on the rules themselves -------------------------------
    ("the subsection whose body carries an exemption renamed away",
     "### Estimation",
     "### Fitting the models", "low"),
    ("the Methods no longer state the rule this module enforces",
     'so that "boundary" is left free for the two derived',
     'so that the word is left free for the two derived', "medium"),

    # ---- negative plants: correct text that must NOT be reported -----------
    ("NEGATIVE: a paragraph re-wrapped and nothing else",
     "Neither boundary predicts which isolates reach the floor",
     "Neither\nboundary predicts which isolates reach the floor", "silent"),
    ("NEGATIVE: 'the boundaries require' re-wrapped",
     "carrying all three fields the boundaries require",
     "carrying all three fields the\nboundaries require", "silent"),
    ("NEGATIVE: the assay floor named as a limit inside quotation marks",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. The "
     'Methods reject "assay limit" as a name for it.', "silent"),
    ("NEGATIVE: a reachability boundary discussed with 'below' grammar",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. An "
     "isolate below *N*_reach cannot show a four-log reduction at all.",
     "silent"),
    ("NEGATIVE: a sterilisation claim, which is a claim about depth",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. The "
     "framework locates the depth at which a sterilisation claim stops being "
     "demonstrable.", "silent"),
    ("NEGATIVE: the endpoint disowned again, at a new site",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. A "
     "first observed crossing below the floor is not clearance.", "silent"),
    ("NEGATIVE: both abbreviations named in one sentence",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. The "
     "MDR label and the MDK endpoint are different things.", "silent"),
    ("NEGATIVE: a derived boundary in the same relative-clause grammar",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. Every "
     "isolate below *N*_reach is unable to reach a four-log endpoint.",
     "silent"),
    ("NEGATIVE: an abbreviation expanded where it is first used",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings.",
     "the range compared is 4 to 128 \u00b5g/mL: 32-fold, five doublings. The "
     "area under the curve (AUC) is reported for each arm.", "silent"),
]


def selftest(text: str, ctx: dict) -> int:
    """Plant each error this module exists to catch and check it is caught.

    Positive plants must produce a finding at the severity claimed.  Negative
    plants are correct manuscript text -- a re-wrapped paragraph, a legitimate
    sense of a governed word -- and must produce nothing: a checker that fires
    on those gets switched off, and then it guards nothing at all.
    """
    def sig(f):
        return (f["kind"], f["found"])

    missed = 0
    base = check(text, ctx)
    seen = {sig(f) for f in base}
    print(f"baseline on the real manuscript: {len(base)} finding(s), "
          f"{sum(1 for f in base if f['severity'] == 'high')} high\n")
    for name, old, new, want in _PLANTS:
        if old not in text:
            print(f"  SKIP  {name}: anchor text no longer in the manuscript")
            missed += 1
            continue
        got = check(text.replace(old, new, 1), ctx)
        fresh = [f for f in got if sig(f) not in seen]
        lost = seen - {sig(f) for f in got}
        if want == "silent":
            ok = not fresh
        else:
            ok = any(f["severity"] == want for f in fresh)
        print(f"  {'ok  ' if ok else 'MISS'}  {name}: "
              f"want {want}, {len(fresh)} new finding(s)")
        for f in fresh[:3]:
            print(f"            [{f['severity']}] {f['kind']} @ {f['where']}")
        if lost:
            print(f"            ! {len(lost)} baseline finding(s) disappeared")
            ok = False
        if not ok:
            missed += 1
    return missed


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(__file__).resolve().parents[2]
    flags = [a for a in argv if a.startswith("--")]
    rest = [a for a in argv if not a.startswith("--")]
    paper = Path(rest[0]) if rest else root / "manuscript" / "PAPER_COMPLETE.md"
    text = paper.read_text(encoding="utf-8")
    ctx = {"root": root}
    for key, rel in (("tables", "manuscript/tables.md"),
                     ("prose", "manuscript/RATE_VS_DURATION.md"),
                     ("abstract", "manuscript/abstract.md")):
        path = root / rel
        ctx[key] = path.read_text(encoding="utf-8") if path.exists() else ""

    if "--debug" in flags:
        p = Paper(text)
        _check_boundary(p, debug=True)
        _check_limit(p, debug=True)
        print("  -- event names --")
        _check_event_names(p, debug=True)
        print("  -- abbreviations --")
        _check_abbreviations(p, debug=True)
        return 0
    if "--selftest" in flags:
        missed = selftest(text, ctx)
        print("\nself-test:", "every plant caught" if not missed
              else f"{missed} plant(s) missed")
        return 1 if missed else 0

    findings = check(text, ctx)
    print(f"check_terms on {paper}")
    if not findings:
        print("  clean (0 findings)")
        return 0
    print(f"  {len(findings)} finding(s)\n")
    for f in findings:
        print(f"[{f['severity'].upper():6}] {f['kind']}  ({f['where']})")
        print(f"         {f['detail']}")
        if f.get("expected"):
            print(f"         expected: {f['expected']}")
        if f.get("found"):
            print(f"         found:    {f['found']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
