"""
Checker 5 -- is a passage in this section a leftover copy of another one?

Run:  python -m src.audit.check_duplication

WHY THIS EXISTS. Results Section 3 was rewritten to concede that the agreement
between the algebra and the deposit is an identity rather than a passed test. The
rewrite was inserted and the passage it replaced was never deleted, so the section
restated the retracted reading and closed on it. Two rounds of review and two
audit scripts read past it, because nothing in the section was arithmetically
wrong: the defect was that one sentence stood twice, in two incompatible versions.

WHAT IT CHECKS.

  RULE 1  duplicated-passage. Two passages of one section sharing more than
          fifteen consecutive words, where the two copies continue the same way.
          MEDIUM. A repeat is a defect, but it is not by itself a contradiction:
          two copies of one sentence can both be right, and only a reader can say
          which of them to cut.

  RULE 2  superseded-passage. The same shared span, where one copy ASSERTS what
          the other DENIES: a polarity word (not / never / no / nor / cannot /
          rather than / instead) present on one side and absent on the other,
          AND the two remainders otherwise the same statement -- one of them
          empty, or both a word or two long, or equal once the negations are
          removed. Then only one of them can be current. HIGH, and it fails the
          run. It applies within a section and, at the cross-section length,
          between two sections.

  RULE 2' divergent-duplicate. The same shared span where the two copies differ
          in a QUANTITY rather than in a negation, or in a negation that does not
          meet rule 2's gate; and, separately, two sentences of one section that
          are word-for-word identical but for a single token, when that token is
          a quantity. MEDIUM. This is the stale-count case -- and it is also
          exactly what an enumeration looks like ("in the 15-day panel ... in the
          60-day panel ...", "institute D ... institute E ..."), which is
          ordinary scientific prose. The checker cannot tell the two apart, so it
          reports and does not fail. See WHY RULE 2 IS NARROW below.

  RULE 3  numberless-reassertion. A sentence of the prose, of a table or figure
          legend, or of Box 1, asserting a conclusion the paper's own self-audit
          table (Table 15, "Conclusion as originally stated" against its verdict
          column) marks NOT SUPPORTED or WITHDRAWN, while carrying none of that
          conclusion's numbers. MEDIUM: the match is on words alone, with no
          numeric anchor to make it certain, and a rule that cannot be certain
          should not fail a build.

  RULE 1', reused-passage. More than thirty consecutive words shared by two
          DIFFERENT sections. LOW.

WHY RULE 2 IS NARROW, AND WHY A NUMBER IS NOT ENOUGH FOR HIGH. An earlier draft
graded ANY difference in the two copies' surroundings -- a number or a negation --
as high. Four constructions of ordinary, true, correctly written prose defeat it,
each verified against this manuscript by mutation:

    "In institute D the mean starting density is 4.69 log10, and <25 identical
     words>."  /  "In institute E the mean starting density is 4.95 log10, and
     <the same 25 words>."

    "The 2011 edition of the standard defines <29 identical words>."  /  "The 2019
     edition of the standard defines <the same 29 words>."

    "In the 15-day panel <30 identical words>."  /  "In the 60-day panel <the same
     30 words>."

    "Institutes D, E and F record no crossing at <25 identical words>."  /
    "Institutes A, B and C record a crossing at <the same 25 words>."

All four are parallel constructions over two arms, two panels, two editions or
two groups; all four were graded HIGH, and a high finding fails the pipeline. A
repeated span whose surroundings differ in a quantity is indistinguishable from
an enumeration, so the quantity case is reported at MEDIUM. The fourth shows that
a bare polarity difference is not enough either, which is why high additionally
requires the two remainders to be the same statement (see rule 2 above): in the
fourth case they name different institutes, so it is refused. Years and edition
numbers are dropped from the quantity comparison for the same reason a
cross-reference is: they are pointers, not quantities.

NORMALISATION, AND WHY STOPWORDS ARE KEPT. Text is folded to ASCII (superscripts,
subscripts, dashes, quotes, the multiplication sign), markdown emphasis is deleted
in place rather than spaced -- so *N*_id and N_id give one token -- the result is
lowercased, and words are the maximal runs of [a-z0-9]. Stopwords are NOT dropped,
and the fifteen counts every word including them. Dropping them would be wrong
here. This manuscript names the same few quantities on every page -- starting
density, assay floor, recorded fraction, compatible class, headroom -- so two
paragraphs arguing different things still share a long skeleton of content words,
and a stopword-free rule would fire on ordinary writing. Function words are what a
rewrite changes and what an undeleted copy keeps: requiring the connectives to
match as well means a hit is a hit on the sentence as it was actually written,
which is the thing being looked for. Nothing is stemmed either, for the same
reason: "isolate" and "isolates" are allowed to differ.

SCOPE: PROSE. Table bodies repeat cell values by design and table legends share
boilerplate, so neither is prose. What counts as prose is the complement of what
src/audit/check_coverage.py's segment() calls a region -- table legends with the
grids they label, figure legends, Box 1 -- with every pipe row, heading, image,
the YAML front matter, the horizontal rules and the two placeholder sections
(References, Declarations) removed as well. Each region is walked to its end with
segment()'s own rules, so the two agree by construction and not by coincidence.
The Abstract is the one region kept, because it is prose.

SCOPE: ONE SECTION. A section runs from one heading to the next, at the finest
level the document has, so Results 3 and Limitations are separate. This is not
fastidiousness, it is the calibration itself. Run without it, the same fifteen-word
rule returns five spans on the CURRENT, clean manuscript, each shared between a
Results section and the Discussion or the Methods, the longest twenty words, and
every one of them a legitimate restatement of a result where the paper discusses
it. Inside a section there is no such licence: the current manuscript shares no
span of even eight words within any section, so the fifteen is not a threshold
tuned to sit just above the noise, it is far above it. Hence the cross-section
variant (rule 1') runs at thirty words -- half again the longest legitimate
restatement -- and reports LOW.

WHAT THIS DOES NOT DUPLICATE. src/audit/check_consistency.py carries two
neighbouring rules, and this module is written to sit beside them, not on them:

  * its (d), superseded-passage-left-in-place, compares two SENTENCES OF ONE
    PARAGRAPH on a bag of content words and fires at 70 per cent Jaccard. It
    cannot see a repeat that crosses a paragraph break, and it cannot see a long
    verbatim span inside two sentences whose remaining vocabulary differs enough
    to hold the Jaccard below 0.70. Rules 1 and 2 work on consecutive word order
    across the whole section instead, and report the shared span verbatim rather
    than two whole sentences.

  * its (a), not-supported-claim-still-asserted, wants a numeric anchor: it fires
    on two of the conclusion's numbers found in the block, or on one number plus
    half its content words, or -- its one numberless path -- on seventy per cent
    of them. Seventy per cent of a conclusion string is a near-quotation, so a
    reassertion in the author's own words, which is what Section 3's residue was,
    passes it untouched. It also collects only rows whose verdict reads exactly
    NOT SUPPORTED, so the WITHDRAWN row of Table 15 is outside its universe
    altogether. Rule 3 closes exactly those two gaps and stays out of the rest: on
    a NOT SUPPORTED row it drops any candidate that check_consistency would
    ACTUALLY report -- its three disjuncts are recomputed here, and so is its own
    withdrawal-marker veto, because a block that veto silences is a block it never
    reports and therefore never covers; on a WITHDRAWN row no guard applies,
    because there is nothing to defer to.

  Deferring on the thresholds alone was wrong and left a hole that has now been
  closed. Where a block carries a withdrawal marker anywhere in it -- the Figure 2
  legend carries four -- check_consistency skips the whole block, so a reassertion
  planted in it was reported by neither checker. Rule 3 therefore reads the marker
  in a window of the candidate sentence and its two neighbours rather than the
  whole block, and it reads legends and Box 1 as well as running prose, which is
  where a struck-out claim most easily survives a rewrite.

CONVENTIONS DELIBERATELY NOT FLAGGED. A repeat inside a table body, a legend or
Box 1; a span shared by two sections and shorter than thirty words, which is how a
paper restates its own results where it discusses them; a cross-reference or a
year, which are pointers and not quantities, so two copies citing Table 4 and
Table 5, or the 2011 and the 2019 edition of one standard, are not called a
numeric contradiction; and any passage that reports the claim, in the sentence
before or after it, as withdrawn, as description, or without the inference the
audit table struck out.

WHAT THIS STILL CANNOT SEE, said plainly, because a checker that implies more
than it does is worse than none.

  * A leftover copy that was REWORDED. Every span rule here is verbatim: it finds
    two copies that share sixteen consecutive words. A rewrite that says the same
    thing in its own words shares no such run and is invisible, and that is the
    commoner shape of the defect. The one reworded case that is caught is a
    single-token substitution over a whole sentence (rule 2').

  * A superseded copy across a section boundary shorter than thirty words. Between
    two sections the bar is thirty, because at fifteen five legitimate
    restatements in this manuscript reach it; a twenty-word leftover in the
    Discussion is below the floor and is not reported at any severity.

  * A repeat inside a table body, and a repeat between a legend and the prose.
    Rules 1, 1', 2 and 2' read running prose only.

  * Whether two copies are about the same thing. That is the whole difficulty, and
    rule 2's gate is a proxy for it, not a decision procedure.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

try:                                     # imported as src.audit.check_duplication
    from src.audit.check_coverage import segment
except ImportError:                      # run as a plain file
    from check_coverage import segment


# --------------------------------------------------------------------------
# thresholds
# --------------------------------------------------------------------------

MIN_SPAN = 16          # "more than fifteen consecutive words"
MIN_CROSS_SPAN = 30    # between two sections; see the docstring for the fit
CONTEXT = 40           # words of context printed either side of a span
_CLAUSE = 15           # the longest trailing qualification rule 2's gate accepts

# rule 3
MIN_DISTINCTIVE = 4    # a conclusion identified by fewer words is not identified
MIN_COVERAGE = 0.55    # of the conclusion's distinctive words


# --------------------------------------------------------------------------
# folding and words
# --------------------------------------------------------------------------

_FOLD = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "⁻": "-",
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5",
    "×": "x", "·": ".",
    "−": "-", "–": "-", "—": "-", "‐": "-", "‑": "-",
    "‘": "'", "’": "'", "“": '"', "”": '"',
    " ": " ", " ": " ", " ": " ",
}

_EMPHASIS = re.compile(r"[*_`]")
_WORD = re.compile(r"[a-z0-9]+")

# a number as the manuscript writes it, the space thousands separator included
_NUMBER = re.compile(r"(?<![\w.])\d{1,3}(?:[ ,]\d{3})+(?:\.\d+)?"
                     r"|(?<![\w.])\d+(?:\.\d+)?(?:e-?\d+)?")

# A year is a pointer too: a citation year, or the edition of a standard. Two
# copies of a passage that cite different sources differ in where they point,
# not in what they claim.
_YEARISH = re.compile(r"(?:1[89]|20)\d\d$")

# A pointer is not a quantity: two copies of a passage that cite Table 4 and
# Table 5 differ in their cross-reference, not in what they claim, and rule 2
# must not call that a contradiction.
_CROSSREF = re.compile(r"\b(?:Tables?|Figs?\.?|Figures?|Sections?|Boxes?|Box|"
                       r"[Pp]anels?)\s+S?\d+[A-Z]?", re.I)

_POLARITY = (
    ("not", re.compile(r"\bnot\b")),
    ("never", re.compile(r"\bnever\b")),
    ("no", re.compile(r"\bno\b")),
    ("nor", re.compile(r"\bnor\b")),
    ("cannot", re.compile(r"\bcan\s?not\b")),
    ("rather than", re.compile(r"\brather than\b")),
    ("instead", re.compile(r"\binstead\b")),
)

# the same words as tokens, for deciding whether two remainders are the same
# statement once their negations are taken out
_POLARITY_TOKENS = {"not", "never", "no", "nor", "cannot", "rather", "than",
                    "instead"}


def fold(s: str) -> str:
    """Fold the typography the manuscript uses down to ASCII."""
    return unicodedata.normalize("NFKC", "".join(_FOLD.get(c, c) for c in s))


def flatten(s: str) -> str:
    """Folded, with markdown emphasis removed IN PLACE so *N*_id == N_id."""
    return _EMPHASIS.sub("", fold(s))


# --------------------------------------------------------------------------
# what counts as prose
# --------------------------------------------------------------------------

_HEADING = re.compile(r"(#{1,6})\s+(.*)")
_PLACEHOLDER_SECTIONS = ("references", "declarations")


def nonprose_lines(text: str) -> set[int]:
    """0-based indices of the lines check_coverage.segment() claims as a region.

    The Abstract is deliberately not claimed: it is prose. Every other region is
    walked to its end with the rules segment() itself uses.
    """
    lines = text.split("\n")
    n = len(lines)
    bad: set[int] = set()
    for r in segment(text):
        i = r["line"] - 1
        if r["region"] == "abstract" or not 0 <= i < n:
            continue
        if r["region"] == "table legend":
            j = i
            while j < n and lines[j].strip():            # the legend paragraph
                bad.add(j)
                j += 1
            while j < n and not lines[j].strip():
                j += 1
            while j < n and lines[j].lstrip().startswith("|"):
                bad.add(j)                              # the grid it labels
                j += 1
        elif r["region"] == "figure legend":
            bad.add(i)
            j = i + 1
            while j < n:
                s = lines[j]
                if (re.match(r"\*\*Figure\s+\d+\.", s) or s.startswith("![")
                        or s.startswith("---") or s.startswith("#")):
                    break
                bad.add(j)
                j += 1
        elif r["region"] == "box":
            j = i
            while j < n:
                s = lines[j]
                if j > i and (s.startswith("---") or s.startswith("## ")):
                    break
                bad.add(j)
                j += 1
    return bad


def prose_map(text: str) -> dict[int, str]:
    """1-based line number -> line, for every line of running prose."""
    lines = text.split("\n")
    bad = nonprose_lines(text)

    if lines and lines[0].strip() == "---":              # YAML front matter
        for k, ln in enumerate(lines):
            bad.add(k)
            if k and ln.strip() == "---":
                break

    out: dict[int, str] = {}
    skipping = False
    for k, ln in enumerate(lines):
        m = _HEADING.match(ln)
        if m:
            skipping = m.group(2).strip().lower() in _PLACEHOLDER_SECTIONS
            continue
        s = ln.strip()
        if k in bad or skipping or not s:
            continue
        if s.startswith("|") or s.startswith("!["):
            continue
        if len(s) >= 3 and set(s) <= set("-"):           # a horizontal rule
            continue
        out[k + 1] = ln
    return out


class Section:
    """One heading's prose, as a word sequence with the source behind it."""

    __slots__ = ("title", "line", "flat", "words", "starts", "ends", "lines",
                 "para", "breaks")

    def __init__(self, title: str, line: int, body: list[tuple[int, str]]):
        self.title = title
        self.line = line
        pieces: list[str] = []
        self.lines, self.starts, self.ends, self.words, self.para = [], [], [], [], []
        pos = 0
        block = 0
        previous = None
        for lineno, raw in body:
            # prose_map drops blank lines, so a gap in the line numbers is
            # exactly where a paragraph ended
            if previous is not None and lineno != previous + 1:
                block += 1
            previous = lineno
            flat = flatten(raw)
            low = flat.lower()
            for m in _WORD.finditer(low):
                self.words.append(m.group(0))
                self.starts.append(pos + m.start())
                self.ends.append(pos + m.end())
                self.lines.append(lineno)
                self.para.append(block)
            pieces.append(flat)
            pos += len(flat) + 1
        self.flat = "\n".join(pieces)
        self.breaks = self._sentence_breaks()

    def _sentence_breaks(self) -> list[bool]:
        """True where a full stop follows word i, so a span can round out."""
        out = []
        for i in range(len(self.words)):
            tail = self.flat[self.ends[i]:self.ends[i] + 4]
            out.append(bool(re.match(r"[)\]\"']*[.!?](?:\s|$)", tail)))
        return out

    def raw(self, i: int, j: int) -> str:
        """The source text carrying words i .. j-1, whitespace collapsed."""
        if i >= j:
            return ""
        return re.sub(r"\s+", " ",
                      self.flat[self.starts[i]:self.ends[j - 1]]).strip()

    def widen(self, i: int, j: int, w: int = 0) -> tuple[int, int]:
        """Words i..j-1 widened by w, rounded out to sentence boundaries and
        CLAMPED TO THE PARAGRAPH.

        The clamp is not tidiness. Sentence rounding walks back until it finds a
        full stop, and a paragraph whose last line ends in a colon, a display
        expression or a bolded run-in has no full stop to stop it, so a span
        beginning a paragraph swept the whole of the previous paragraph's closing
        sentence into what rule 2 compares. A duplicated paragraph then differed
        from itself in a number forty words away and was graded high. Verified:
        with a mutated copy inserted one line short of the paragraph break, the
        checker reported "the numbers before the span differ (none against 0.10)"
        at HIGH for two byte-identical copies of one paragraph.
        """
        p0, _ = self.block(i)
        _, p1 = self.block(min(j, len(self.words)) - 1)
        a = max(p0, i - w)
        b = min(p1, j + w)
        while a > p0 and not self.breaks[a - 1]:
            a -= 1
        while b < p1 and not self.breaks[b - 1]:
            b += 1
        return a, b

    def block(self, i: int) -> tuple[int, int]:
        """The paragraph holding word i, as a word range."""
        p = self.para[i]
        a = i
        while a > 0 and self.para[a - 1] == p:
            a -= 1
        b = i + 1
        while b < len(self.words) and self.para[b] == p:
            b += 1
        return a, b


def sections(text: str) -> list[Section]:
    """The document's prose, cut at every heading."""
    lines = text.split("\n")
    heads = [i for i, ln in enumerate(lines) if _HEADING.match(ln)]
    prose = prose_map(text)
    out = []
    for idx, i in enumerate(heads):
        end = heads[idx + 1] if idx + 1 < len(heads) else len(lines)
        body = [(k, prose[k]) for k in range(i + 2, end + 1) if k in prose]
        if not body:
            continue
        out.append(Section(flatten(_HEADING.match(lines[i]).group(2).strip()),
                           i + 1, body))
    return out


# --------------------------------------------------------------------------
# repeated word spans
# --------------------------------------------------------------------------

def repeated_spans(words: list[str], k: int) -> list[tuple[int, int, int]]:
    """Maximal non-overlapping repeats: (first start, second start, length)."""
    n = len(words)
    if n < 2 * k:
        return []
    first: dict[tuple[str, ...], int] = {}
    seeds: list[tuple[int, int]] = []
    for i in range(n - k + 1):
        key = tuple(words[i:i + k])
        j = first.get(key)
        if j is None:
            first[key] = i
        elif i - j >= k:                       # the two copies must not overlap
            seeds.append((j, i))

    out: set[tuple[int, int, int]] = set()
    for a, b in seeds:
        length = k
        while (b + length < n and words[a + length] == words[b + length]
               and a + length + 1 <= b):
            length += 1
        while (a > 0 and words[a - 1] == words[b - 1]
               and a + length <= b - 1):
            a -= 1
            b -= 1
            length += 1
        out.add((a, b, length))
    return sorted(out, key=lambda t: (-t[2], t[0]))


def _numbers(s: str) -> list[str]:
    """The quantities a passage states; cross-references and years removed."""
    s = _CROSSREF.sub(" ", s)
    out = [re.sub(r"[ ,]", "", m.group(0)) for m in _NUMBER.finditer(s)]
    return sorted(t for t in out if not _YEARISH.fullmatch(t))


def _polarity(s: str) -> set[str]:
    low = s.lower()
    return {name for name, rx in _POLARITY if rx.search(low)}


# The manuscript writes small counts as words -- "eighteen isolates", "twelve
# have only the lowest class" -- so a stale count is as likely to be a word as a
# digit, and rule 2' has to recognise both.
_NUMBER_WORDS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty",
    "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred",
    "thousand", "million", "half", "third", "quarter", "twice", "dozen",
    "none",
}
# Ordinals are deliberately absent. "The first panel shows <sixteen identical
# words>" beside "The second panel shows <the same words>" is a parallel, not a
# stale count, and a rule that reports it is noise a reader learns to skip.


def _is_quantity(w: str) -> bool:
    """A bare number, or a number written as a word."""
    return bool(re.fullmatch(r"\d[\d.]*", w)) or w in _NUMBER_WORDS


def _same_statement(ra: str, rb: str) -> bool:
    """Are these two remainders the same statement with a negation toggled?

    Yes if one of them is empty and the other is a trailing CLAUSE -- one copy
    stops where the other adds a qualification; or if both are a word or two --
    "does not" against "does too"; or if they are equal once the negations are
    removed. No if they are two substantive clauses that differ in more than the
    negation, which is what an enumeration over two arms or two groups looks
    like, and which must not fail a build.

    The clause length is fitted, not chosen. The genuine case -- the sentence a
    rewrite replaced, reinstated -- continues "and it is not independent evidence
    that the boundary is real", eleven words. The spurious case is a long
    cross-section paste that happens to stop at a paragraph break while the
    original runs on for twenty-five more words into an unrelated "not". Fifteen
    sits between them, and above it the finding falls to the paste's own grade.
    """
    wa = _WORD.findall(ra.lower())
    wb = _WORD.findall(rb.lower())
    if not wa or not wb:
        return max(len(wa), len(wb)) <= _CLAUSE
    if len(wa) <= 3 and len(wb) <= 3:
        return True
    return ([w for w in wa if w not in _POLARITY_TOKENS]
            == [w for w in wb if w not in _POLARITY_TOKENS])


def _compare(ra_l: str, ra_r: str, rb_l: str, rb_r: str) -> tuple[list, bool]:
    """(reasons the two copies differ, whether one asserts what the other denies).

    Only the residue of the sentences the span partly occupies is compared, side
    by side, and only within the paragraph. A wider window drags in whatever
    happens to stand nearby and grades an innocuous back-to-back duplication as a
    contradiction.
    """
    why: list[str] = []
    asserts_and_denies = False
    for side, ra, rb in (("before", ra_l, rb_l), ("after", ra_r, rb_r)):
        na, nb = _numbers(ra), _numbers(rb)
        if na != nb:
            why.append("the quantities %s the span differ (%s against %s)"
                       % (side, ", ".join(na) or "none", ", ".join(nb) or "none"))
        pa, pb = _polarity(ra), _polarity(rb)
        if pa != pb:
            why.append("the polarity %s the span differs (%s against %s)"
                       % (side, ", ".join(sorted(pa)) or "none",
                          ", ".join(sorted(pb)) or "none"))
            if _same_statement(ra, rb):
                asserts_and_denies = True
    return why, asserts_and_denies


def _source_lines(prose: str, words: list[str], limit: int = 2) -> list[int]:
    """Where the span sits in the prose SOURCE, so the fix is actionable there."""
    if not prose or len(words) < 4:
        return []
    flat = flatten(prose).lower()
    needle = re.compile(r"\W+".join(re.escape(w) for w in words[:8]))
    out, pos = [], 0
    while len(out) < limit:
        m = needle.search(flat, pos)
        if m is None:
            break
        out.append(flat[:m.start()].count("\n") + 1)
        pos = m.end()
    return out


def _where(sec: Section, a: int, b: int, prose: str, words: list[str]) -> str:
    src = _source_lines(prose, words)
    tail = ("; MANUSCRIPT.md line%s %s"
            % ("" if len(src) == 1 else "s",
               " and ".join(str(s) for s in src))) if src else ""
    return ("section \"%s\" (line %d), lines %d and %d%s"
            % (sec.title[:60], sec.line, sec.lines[a], sec.lines[b], tail))


def check_within_section(secs: list[Section], prose: str) -> list[dict]:
    """Rules 1, 2 and 2': a span repeated inside one section."""
    findings = []
    for sec in secs:
        for a, b, length in repeated_spans(sec.words, MIN_SPAN):
            verbatim = sec.raw(a, a + length)
            # each copy's own sentences, minus the shared span: what the two
            # copies do NOT have in common, on each side, and nothing else
            sa0, sa1 = sec.widen(a, a + length)
            sb0, sb1 = sec.widen(b, b + length)
            why, denies = _compare(sec.raw(sa0, a), sec.raw(a + length, sa1),
                                   sec.raw(sb0, b), sec.raw(b + length, sb1))

            where = _where(sec, a, b, prose, sec.words[a:a + length])
            ca0, ca1 = sec.widen(a, a + length, CONTEXT)
            cb0, cb1 = sec.widen(b, b + length, CONTEXT)
            both = "%s  ||  %s" % (sec.raw(ca0, ca1)[:260],
                                   sec.raw(cb0, cb1)[:260])

            if denies:
                findings.append({
                    "severity": "high",
                    "kind": "superseded-passage",
                    "where": where,
                    "detail": ("%d consecutive words repeat inside one section "
                               "and one copy asserts what the other denies -- %s "
                               "-- so they are two versions of one statement and "
                               "only one of them is current: \"%s\""
                               % (length, "; ".join(why), verbatim)),
                    "expected": "one version of the passage, the revised one",
                    "found": both,
                })
            elif why:
                findings.append({
                    "severity": "medium",
                    "kind": "divergent-duplicate",
                    "where": where,
                    "detail": ("%d consecutive words repeat inside one section "
                               "and the two copies continue differently -- %s. "
                               "Either one copy is a stale version of the other "
                               "or the two are a parallel over two arms, panels "
                               "or sources; the checker cannot tell which: \"%s\""
                               % (length, "; ".join(why), verbatim)),
                    "expected": "one version of the passage, or a parallel that "
                                "does not repeat sixteen words verbatim",
                    "found": both,
                })
            else:
                findings.append({
                    "severity": "medium",
                    "kind": "duplicated-passage",
                    "where": where,
                    "detail": ("%d consecutive words repeat inside one section, "
                               "which is what a section looks like when the "
                               "passage a rewrite replaced was never deleted: "
                               "\"%s\"" % (length, verbatim)),
                    "expected": "the passage stated once",
                    "found": both,
                })
    return findings


def check_renumbered(secs: list[Section], prose: str) -> list[dict]:
    """Rule 2': two sentences of one section identical but for one token.

    The span rules cannot see this. If the stale word sits in the MIDDLE of a
    repeated sentence it cuts the shared run in two, and two runs of a dozen
    words each are under the sixteen; the more the two copies contradict each
    other the less likely a verbatim-span rule is to notice. Verified on a copy:
    one sentence of twenty-seven words reinserted with "twelve" changed to
    "eleven" at word thirteen produced no finding at all before this rule.
    """
    findings = []
    for sec in secs:
        by_length: dict[int, list[tuple[int, int]]] = {}
        for _, i, j in _prose_sentences([sec]):
            if j - i >= MIN_SPAN:
                by_length.setdefault(j - i, []).append((i, j))
        for group in by_length.values():
            for x in range(len(group)):
                for y in range(x + 1, len(group)):
                    i1, j1 = group[x]
                    i2, j2 = group[y]
                    diff = [k for k in range(j1 - i1)
                            if sec.words[i1 + k] != sec.words[i2 + k]]
                    if len(diff) != 1:
                        continue
                    u = sec.words[i1 + diff[0]]
                    v = sec.words[i2 + diff[0]]
                    if not (_is_quantity(u) and _is_quantity(v)):
                        continue
                    src = _source_lines(prose, sec.words[i1:j1], limit=2)
                    tail = ("; MANUSCRIPT.md line%s %s"
                            % ("" if len(src) == 1 else "s",
                               " and ".join(str(s) for s in src))) if src else ""
                    findings.append({
                        "severity": "medium",
                        "kind": "divergent-duplicate",
                        "where": ("section \"%s\" (line %d), lines %d and %d%s"
                                  % (sec.title[:60], sec.line,
                                     sec.lines[i1], sec.lines[i2], tail)),
                        "detail": ("two sentences of one section are identical "
                                   "word for word except for one quantity, \"%s\" "
                                   "against \"%s\". Either one is a stale copy of "
                                   "the other or they are a parallel over two "
                                   "arms or panels: \"%s\""
                                   % (u, v, sec.raw(i1, j1))),
                        "expected": "one of the two, or a parallel that does not "
                                    "restate the whole sentence",
                        "found": "%s  ||  %s" % (sec.raw(i1, j1)[:260],
                                                 sec.raw(i2, j2)[:260]),
                    })
    return findings


def check_across_sections(secs: list[Section], prose: str) -> list[dict]:
    """Rules 1' and 2: a long span shared by two different sections."""
    words: list[str] = []
    owner: list[tuple[int, int]] = []
    for s_i, sec in enumerate(secs):
        if words:
            # A sentinel no word can equal, unique to this boundary, so that no
            # repeat can straddle two sections. Without it a span that ran off
            # the end of its section indexed past that section's last word and
            # raised IndexError, which src/audit_manuscript.py turns into a HIGH
            # checker-error and a failed run. Verified: pasting one section's
            # closing paragraph and the next section's opening paragraph, back to
            # back, into the Limitations crashed the checker.
            words.append("\x00%d" % s_i)
            owner.append((-1, -1))
        for w_i in range(len(sec.words)):
            words.append(sec.words[w_i])
            owner.append((s_i, w_i))

    findings = []
    for a, b, length in repeated_spans(words, MIN_CROSS_SPAN):
        sa, wa = owner[a]
        sb, wb = owner[b]
        if sa < 0 or sb < 0 or sa == sb:
            continue                       # rule 1's business, reported there
        A, B = secs[sa], secs[sb]
        verbatim = A.raw(wa, wa + length)
        src = _source_lines(prose, words[a:a + length])
        where = ("sections \"%s\" (line %d) and \"%s\" (line %d)%s"
                 % (A.title[:45], A.lines[wa], B.title[:45], B.lines[wb],
                    ("; MANUSCRIPT.md line %d" % src[0]) if src else ""))

        wa0, wa1 = A.widen(wa, wa + length)
        wb0, wb1 = B.widen(wb, wb + length)
        why, denies = _compare(A.raw(wa0, wa), A.raw(wa + length, wa1),
                               B.raw(wb0, wb), B.raw(wb + length, wb1))
        if denies:
            findings.append({
                "severity": "high",
                "kind": "superseded-passage",
                "where": where,
                "detail": ("%d consecutive words appear in both sections and one "
                           "copy asserts what the other denies -- %s -- so they "
                           "are two versions of one statement and only one of "
                           "them is current: \"%s\"" % (length, "; ".join(why),
                                                        verbatim)),
                "expected": "one version of the passage, the revised one",
                "found": "%s  ||  %s" % (A.raw(wa0, wa1)[:260],
                                         B.raw(wb0, wb1)[:260]),
            })
            continue
        findings.append({
            "severity": "low",
            "kind": "reused-passage",
            "where": where,
            "detail": ("%d consecutive words appear in both sections. A result "
                       "restated where it is discussed is normal and the longest "
                       "such restatement in this manuscript is twenty words; a "
                       "span this long is a paste%s: \"%s\""
                       % (length,
                          (", and " + "; ".join(why)) if why else "", verbatim)),
            "expected": "a restatement in the section's own words",
            "found": verbatim[:260],
        })
    return findings


# --------------------------------------------------------------------------
# rule 3: the self-audit table's failures, reasserted without their numbers
# --------------------------------------------------------------------------

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
    "might", "must", "should", "would", "will", "shall",
}

# Text saying the claim is being reported rather than made. Held in step with
# check_consistency's list, which was tuned on this manuscript, so that a
# paragraph that satisfies one checker's restraint satisfies the other's.
_WITHDRAWAL_MARKERS = (
    "not supported", "no longer", "withdrawn", "is withdrawn", "deleted",
    "as originally", "originally stated", "removed from the text",
    "do not survive", "does not survive", "not recomputable",
    "without a p-value", "with no p-value", "no p-value", "quoted without",
    "descriptive", "description", "descriptively", "not a test",
    "rather than a test", "not a finding", "none is claimed", "not evidence",
    "no between-laboratory test", "is a description", "smallest attainable",
    "not valid", "invalid", "with the same restraint", "cannot support",
    "recomputed at the level", "is refused", "are refused",
    "no p is quoted", "no p-value is quoted", "no p-value is attached",
    "does not hold", "cannot be tested", "is not available", "we do not claim",
    "not because they are valid", "bounds the evidence",
)

_FAILED_VERDICTS = {"NOT SUPPORTED", "WITHDRAWN"}

# check_consistency's own numeric fingerprint, reproduced here so the two rules
# can be held apart rather than guessed apart.
_FINGERPRINT = re.compile(r"\d+\.\d+e-?\d+|\d+e-?\d+|\d+\.\d+|\d{3,}")


def _content(s: str) -> list[str]:
    return [w for w in _WORD.findall(flatten(s).lower())
            if w not in _STOP and len(w) > 2 and not w.isdigit()]


def _number_in(tok: str, hay: str) -> bool:
    """check_consistency's tolerance: 1.2e-10 also written 1.2 x 10-10."""
    if re.search(r"(?<![\d.])" + re.escape(tok) + r"(?!\d)", hay):
        return True
    m = re.fullmatch(r"(\d+(?:\.\d+)?)e(-?\d+)", tok)
    if m:
        alt = (re.escape(m.group(1)) + r"\s*(?:x|\*)\s*10\s*-?"
               + str(abs(int(m.group(2)))))
        return bool(re.search(alt, hay))
    return False


def _consistency_would_fire(claim: str, block: str) -> bool:
    """Would check_consistency's (a) actually REPORT this block?

    Reproduced rather than imported, because it is a threshold rule and the point
    of rule 3 is to describe exactly the space it leaves. Its withdrawal-marker
    veto is reproduced along with its thresholds: a block that veto silences is a
    block check_consistency never reports, so it is not a block rule 3 may defer
    to. Deferring on the thresholds alone left a hole -- the Figure 2 legend
    carries four markers, and a reassertion planted anywhere in it was reported by
    neither checker.
    """
    words = set(_content(claim))
    if not words:
        return False
    if any(mk in block.lower() for mk in _WITHDRAWAL_MARKERS):
        return False
    hits = [t for t in set(_FINGERPRINT.findall(flatten(claim)))
            if _number_in(t, block)]
    shared = words & set(_content(block))
    cov = len(shared) / len(words)
    return (len(hits) >= 2
            or (len(hits) >= 1 and cov >= 0.50)
            or (cov >= 0.70 and len(shared) >= 3))


def _audit_rows(text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """(table number, [(section, conclusion, verdict)]) for the failed rows."""
    for r in segment(text):
        if r["region"] != "table legend" or not r["body"]:
            continue
        rows = [[c.strip() for c in ln.strip().strip("|").split("|")]
                for ln in r["body"].split("\n") if ln.lstrip().startswith("|")]
        if len(rows) < 3:
            continue
        header = [c.lower() for c in rows[0]]
        i_c = next((i for i, h in enumerate(header) if "conclusion" in h), None)
        i_v = next((i for i, h in enumerate(header) if "verdict" in h), None)
        if i_c is None or i_v is None:
            continue
        i_s = 0 if "section" in header[0] else None
        failed = []
        for row in rows[2:]:
            if len(row) <= max(i_c, i_v):
                continue
            verdict = row[i_v].upper().replace("-", " ").strip()
            if verdict in _FAILED_VERDICTS:
                failed.append((row[i_s].strip() if i_s is not None else "?",
                               row[i_c].strip(), verdict))
        return r["label"].split()[1], failed
    return "", []


def _prose_sentences(secs: list[Section]):
    """(section, first word index, one past the last) for each prose sentence."""
    for sec in secs:
        start = 0
        for i, brk in enumerate(sec.breaks):
            if brk:
                if i + 1 - start >= 5:
                    yield sec, start, i + 1
                start = i + 1
        if len(sec.words) - start >= 5:
            yield sec, start, len(sec.words)


def _marker_window(sec: Section, i: int, j: int) -> str:
    """The candidate sentence and its two neighbours, inside its paragraph.

    Not the whole paragraph. A withdrawal marker anywhere in a paragraph silenced
    the rule, and "description", "descriptive" and "deleted" are ordinary words
    that a paragraph can carry for an unrelated reason four sentences away. The
    restraint the markers are there to recognise sits against the sentence it
    qualifies, so that is what is read.
    """
    b0, b1 = sec.block(i)
    starts = [k for k in range(b0, b1) if k == b0 or sec.breaks[k - 1]]
    idx = starts.index(i) if i in starts else 0
    lo = starts[max(0, idx - 1)]
    hi = starts[idx + 2] if idx + 2 < len(starts) else b1
    return sec.raw(lo, hi)


def _legend_sentences(text: str):
    """(label, line, sentence, window, whole region) for legends and Box 1.

    A struck-out conclusion survives a rewrite most easily where nobody rereads:
    the legend of the figure that plots it. Nothing in the span rules reads a
    legend, by design -- legends share boilerplate -- but a CLAIM in a legend is
    a claim.

    The window is the sentence and its two neighbours, for the same reason it is
    in prose, and here the reason is sharper: the Figure 2 legend alone carries
    "descriptive", "none is claimed", "not a finding" and "no between-laboratory
    test", so a legend-wide marker read silences the whole legend and a claim
    planted anywhere in it goes unreported by every checker in the stack.
    """
    for r in segment(text):
        if r["region"] not in ("table legend", "figure legend", "box"):
            continue
        whole = flatten(r["text"])
        parts = [re.sub(r"\s+", " ", s).strip()
                 for s in re.split(r"(?<=[.!?])\s+", whole)]
        for k, s in enumerate(parts):
            if len(_WORD.findall(s.lower())) >= 5:
                window = " ".join(parts[max(0, k - 1):k + 2])
                yield r["label"], r["line"], s, window, whole


def check_reassertions(text: str, secs: list[Section], prose: str) -> list[dict]:
    """Rule 3."""
    tnum, failed = _audit_rows(text)
    if not failed:
        return []

    sentences = list(_prose_sentences(secs))
    bags = [set(_content(sec.raw(i, j))) for sec, i, j in sentences]
    # A word the whole paper leans on cannot identify one conclusion, so rarity
    # is measured on the paper's own prose rather than assumed from a list.
    # KNOWN WEAKNESS, stated rather than hidden: a claim reasserted in several
    # places raises the frequency of its own vocabulary, and a word carried past
    # the cut stops being distinctive, so the rule loses sensitivity exactly
    # where the defect is worst. The cut is generous (a word in up to one
    # twenty-fifth of the paper's sentences still counts as distinctive) to blunt
    # that, but it does not remove it.
    freq: dict[str, int] = {}
    for bag in bags:
        for w in bag:
            freq[w] = freq.get(w, 0) + 1
    common = max(6, len(sentences) // 25)

    # candidates: (where, sentence, its bag, block read for the deferral, marker
    # window, the words the source-line hint would be looked up by). The hint is
    # looked up only for a candidate that is about to be reported -- searching
    # the prose source for all six hundred sentences cost six seconds.
    candidates: list[tuple[str, str, set, str, str, list[str]]] = []
    for (sec, i, j), bag in zip(sentences, bags):
        b0, b1 = sec.block(i)
        candidates.append((
            "section \"%s\", line %d" % (sec.title[:60], sec.lines[i]),
            sec.raw(i, j), bag, sec.raw(b0, b1), _marker_window(sec, i, j),
            sec.words[i:j]))
    for label, line, sentence, window, whole in _legend_sentences(text):
        candidates.append(("%s, line %d" % (label, line), sentence,
                           set(_content(sentence)), whole, window, []))

    findings = []
    for sect, claim, verdict in failed:
        marks = set(_FINGERPRINT.findall(flatten(claim)))
        distinctive = {w for w in set(_content(claim)) if freq.get(w, 0) <= common}
        if len(distinctive) < MIN_DISTINCTIVE:
            continue
        for where, sentence, bag, block, window, hint in candidates:
            shared = distinctive & bag
            if (len(shared) < MIN_DISTINCTIVE
                    or len(shared) / len(distinctive) < MIN_COVERAGE):
                continue
            if any(_number_in(t, sentence) for t in marks):
                continue                    # a numeric anchor: not rule 3's gap
            if any(mk in window.lower() for mk in _WITHDRAWAL_MARKERS):
                continue
            if verdict == "NOT SUPPORTED" and _consistency_would_fire(claim, block):
                continue                    # check_consistency reports this one
            src = _source_lines(prose, hint, limit=1) if hint else []
            findings.append({
                "severity": "medium",
                "kind": "numberless-reassertion",
                "where": (where + (("; MANUSCRIPT.md line %d" % src[0])
                                   if src else "")),
                "detail": ("this sentence carries %d of the %d distinctive words "
                           "of a conclusion Table %s marks %s (its Section %s "
                           "row) and none of that conclusion's numbers, so the "
                           "numeric audit cannot see it; check whether it "
                           "reasserts the retracted reading."
                           % (len(shared), len(distinctive), tnum, verdict, sect)),
                "expected": ("withdrawn, or reported as description: %s"
                             % claim[:130]),
                "found": sentence[:240],
            })
    return findings


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------

def check(text: str, ctx: dict) -> list[dict]:
    """Return a list of findings. Empty list means clean."""
    root = Path(ctx.get("root") or Path(__file__).resolve().parents[2])
    if not text:
        # Only when handed nothing. An earlier version also went to disk whenever
        # the text carried no "**Table", which meant a caller's text could be
        # silently replaced by the committed manuscript: a checker must audit
        # what it is given.
        p = root / "manuscript" / "PAPER_COMPLETE.md"
        if p.exists():
            text = p.read_text(encoding="utf-8")
    if not text:
        return []
    prose = ctx.get("prose") or ""
    if not prose:
        p = root / "manuscript" / "MANUSCRIPT.md"
        prose = p.read_text(encoding="utf-8") if p.exists() else ""

    secs = sections(text)
    # The single-token rule runs first because where both it and the span rule
    # see one defect its message is the sharper of the two: it names the pair of
    # words that differ rather than the numbers standing near the span.
    findings = (check_renumbered(secs, prose)
                + check_within_section(secs, prose)
                + check_across_sections(secs, prose)
                + check_reassertions(text, secs, prose))

    # One defect, one line. A sentence reinserted with one count left stale is
    # seen by the span rule and by the single-token rule, and they name the same
    # two lines of the same section; the audit should say so once.
    family = {"duplicated-passage", "divergent-duplicate", "superseded-passage",
              "reused-passage"}
    seen: set[tuple] = set()
    unique = []
    for f in findings:
        key = ((f["severity"], f["where"]) if f["kind"] in family
               else (f["severity"], f["kind"], f["where"]))
        if key not in seen:
            seen.add(key)
            unique.append(f)
    order = {"high": 0, "medium": 1, "low": 2}
    unique.sort(key=lambda f: (order.get(f["severity"], 3), f["kind"],
                               f["where"]))
    return unique


def main(argv: list[str] | None = None) -> int:
    try:                                   # the prose carries N0, uL, 10^-3
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(__file__).resolve().parents[2]
    paper = Path(argv[0]) if argv else root / "manuscript" / "PAPER_COMPLETE.md"
    text = paper.read_text(encoding="utf-8")

    def read(name):
        p = root / "manuscript" / name
        return p.read_text(encoding="utf-8") if p.exists() else ""

    found = check(text, {"root": root, "prose": read("MANUSCRIPT.md"),
                         "tables": read("tables.md")})
    print("check_duplication on %s" % paper)
    if not found:
        print("  clean (0 findings)")
        return 0
    print("  %d finding(s)\n" % len(found))
    for f in found:
        print("[%-6s] %-24s %s" % (f["severity"].upper(), f["kind"], f["where"]))
        print("         %s" % f["detail"])
        if "expected" in f:
            print("         expected: %s" % f["expected"])
        if "found" in f:
            print("         found:    %s" % f["found"])
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
