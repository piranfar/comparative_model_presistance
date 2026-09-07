"""Checker 5 -- censuses, precision, scope, and the audit's own count.

Run:  python -m src.audit.check_census

WHY THIS EXISTS.  The four checkers already in this directory ask whether a
number is traceable, whether it carries one label, whether it agrees with its
own stated inputs, and whether the paper contradicts its own self-audit.  None
of them can see the four failures below, and peer review found all four:

(1) A CENSUS THAT DOES NOT ADD UP.  Results Section 4 said "Six of the nine
    pretreatment covariates ... cannot adjust" and then named five of them; six
    plus the two it called usable is eight, not nine, and Table S4 has nine rows
    in three categories, so two covariates sat in no category at all.  Every
    number in that sentence was individually traceable.  What was wrong was the
    partition.

(2) ONE QUANTITY AT THREE PRECISIONS.  The share of resistant isolates that
    cannot reach the deepest endpoint was "26.2 per cent" in Section 2,
    "26 per cent" in Section 4 and "a quarter" in the Discussion.  No value
    audit can object: each is a correct rounding of the same figure.  A reader
    comparing sections cannot tell whether they are one quantity or three.

(3) A QUALIFIER THAT DID NOT TRAVEL.  Section 5 establishes that the split
    between laboratories that record crossings and laboratories that do not "is
    a property of the plating, not of the laboratories", and qualifies the claim
    "at the 100 uL plating".  The Figure 2 legend and the Table 15 rows carrying
    the same claim stated it unqualified, which is the reading the section
    exists to refute.

(4) THE AUDIT'S OWN COUNT.  The Methods promise that "a separate audit script
    recomputes N of the quantities quoted in the text".  N has now drifted three
    times, because it is a hand-typed count of something a script decides.

WHAT EACH RULE GRADES, AND WHY.

  census-parts-do-not-partition            HIGH
                  "N of the M things", where M is the data-row count of the
                  table the sentence sits in or names, and the parts the text
                  goes on to name ("five of them", "the other two", "only two
                  covariates") cannot be read as partitioning it.  A census says
                  N of M have a property and M - N do not, so a chain that
                  enumerates the M must have a sub-collection making N.  Five,
                  two and two do sum to nine -- but nothing in them makes six,
                  which is exactly how the live defect read.
                  Two further conditions before this is called a contradiction
                  rather than an unfinished list: the parts must carry a
                  complement marker, and they must already account for at least
                  N.  Without the second, "seven of the nine fail; SOME of them
                  are recorded only for resistant isolates, and the other two
                  are the MICs" was graded HIGH, and there is nothing false in
                  it -- a hedge in place of a count is not a contradiction.

  census-not-resolved                      LOW
                  The same census, answerable to the same table, where the
                  parser cannot find the parts, finds parts that stop short of
                  N, or cannot tell whether the enumeration is finished.  It
                  says what it resolved and what it did not, and asks for an
                  eye.  A partial check that admits it is worth more than a rule
                  that guesses.

  named-items-miscounted                   HIGH
                  "Five are recorded almost exclusively for resistant isolates:
                  the two susceptibility calls, the two Mykrobe calls and the
                  mutation identity" claims five and names five.  Claim six and
                  it is a contradiction with its own list.
                  TWO readings satisfy the claim and only both failing is a
                  defect: the count can be of the things the items contain
                  (2 + 2 + 1 = 5) or of the items themselves, which is what
                  "three kinds of column are recorded ...: the two
                  susceptibility calls, the two Mykrobe calls and the mutation
                  identity" says.  Grading only the first made ordinary English
                  a pipeline failure.
                  Only counted where EVERY item in the list opens with a
                  determiner or a count, which is the shape a clean enumeration
                  has; where at least half do it is reported as
                  named-items-not-resolved at LOW, and where fewer than half do
                  the colon is introducing an explanation rather than a list and
                  nothing is reported at all.

  enumerated-partition-total               HIGH
                  "20 survive unchanged, 6 survive with materially wider
                  uncertainty, 5 do not survive, and 1 is withdrawn" is a
                  partition of a table whose rows can be counted.  Three or more
                  NOUNLESS clauses each opening with a number, in a table legend
                  or in a block naming exactly one table, must sum to that
                  table's data rows.  The table is right there, so the two
                  cannot both stand.
                  Nounless is what makes it a partition of the TABLE.  "4
                  deposits derive a floor from a plated volume, 2 infer one from
                  a pile-up, 3 evidence none at all" is a legend sentence about
                  deposits, and weighing it against the legend's own row count
                  produced a HIGH on prose with nothing wrong in it.  A clause
                  that names its own noun is enumerating that noun.

  quantity-at-two-precisions               MEDIUM
                  Two mentions of the same quantity where the coarser value is
                  a correct rounding of the finer one, including a difference
                  of trailing zeros alone.  Both can be right, so this is not a
                  contradiction and does not fail the run -- but only one of
                  them should be in the paper.

  quantity-at-two-values                   MEDIUM, and not higher
                  The same, where the two values are NOT roundings of one
                  another, are within eight per cent of each other, are both
                  percentages, and the identity evidence is strong -- a shared
                  companion figure AND five shared content words.  26.2 against
                  27.4 for the same share cannot both be right.
                  It grades MEDIUM because the identity is a LEXICAL judgement
                  and it can be wrong in the direction that matters.  Measured
                  on this manuscript: a fabricated but perfectly legitimate "36
                  per cent of the pairs invert in the untreated arm" placed in
                  the Table 11 legend matched the real 36.6 per cent overall
                  inversion rate on 13 shared words at 0.76 containment with a
                  shared companion figure -- STRONGER evidence than the genuine
                  26.2-against-27.4 drift it is meant to catch, which matches on
                  5 shared words at 0.38.  No threshold over these features
                  separates a drifted copy from a neighbouring share of the same
                  set, so this cannot be allowed to stop a pipeline.

  qualifier-not-propagated                 MEDIUM
                  As the brief for this rule requires, and for a reason: a
                  legend may legitimately compress, and Table 15 records each
                  claim "as it was originally stated", so an absent qualifier
                  there is a judgement call rather than an error.

  audit-count-drift, -disagreement         HIGH
                  src/audit_claims.py is RUN and its own count is read off.  The
                  Methods sentence, its prose source and the README copy are
                  checked against it and against each other.  One of the parties
                  is a machine, so they cannot both be right.  If the script
                  cannot be run the count is taken statically instead, and then
                  it is a lower bound and everything drops to LOW: a checker
                  that stops a pipeline because pandas was missing is the
                  definition of crying wolf.

  audit-count-missing-from-paper           MEDIUM
                  The prose source states the size of the value audit and the
                  assembled paper states no such number.  PAPER_COMPLETE.md is
                  generated from RATE_VS_DURATION.md, so a sentence present in
                  one and absent from the other means the assembled paper is
                  behind its source -- the same staleness that produced the live
                  defect, one step further along.  Without it, rewording the
                  sentence out of the pattern would have dropped the Methods
                  silently out of the coverage receipt, which would then have
                  read as a clean result.

WHAT IS DELIBERATELY NOT ATTEMPTED, AND WHY.

  * A CENSUS WITH NOTHING TO CHECK IT AGAINST.  "Five of six laboratories record
    net growth" is a census, but no table's rows equal six laboratories and no
    part of it is enumerated, so there is nothing to check.  Twenty-three of the
    manuscript's censuses are in that position and the summary says so.  An
    earlier version of this rule ran the partition arithmetic on them too and
    every finding it produced was cross-talk: "the remaining two of the 33" sits
    four words from a census of 84 and was read as that census's complement.
    The arithmetic is now gated on a table, and the ungated ones are counted,
    not reported.

  * PROSE FRACTION WORDS AS ARITHMETIC.  "a quarter", "a third", "about half"
    are recognised, but reported only when a numeric statement of the SAME claim
    -- five shared content words, in a different region -- is found, and only at
    LOW.  They cannot be checked by rounding: 26.2 per cent is not any rounding
    of 25, so the only numeric test available is a loose ratio band, and a band
    wide enough to catch "a quarter" against 26.2 also catches every unrelated
    figure between 20 and 30 per cent.  The rule therefore leans entirely on the
    lexical match and abstains when there is not one.  It stays LOW because it
    can attach a vague word to the wrong claim; it is here because the live
    example was exactly this and nothing else in the audit could have seen it.

  * MAPPING PROSE CATEGORY WORDS ONTO A TABLE'S CATEGORY COLUMN.  Table S4's
    legend says "Five are recorded almost exclusively for resistant isolates"
    while the table's verdict column holds four PROXY rows: the mutation
    identity is grouped with the five in prose and scored PARTIAL in the table,
    and both are right.  A checker that tallied verdict values against the
    numbers in a legend would report that, and would be wrong.  Only the ROW
    COUNT of a table is used here, never its category labels.

  * 33 OF 217 AGAINST 31 OF 203.  These are the same isolates on two
    denominators -- all isolates, and those carrying an ordered tolerance label
    -- and Section 1 says so explicitly.  The precision rule cannot flag them,
    because it fires only where the coarser value is a correct ROUNDING of the
    finer one, and 33 is not a rounding of 31.  Two integers that differ are a
    job for check_consistency's denominator account, not for a precision rule.

  * PRECISION VARIANTS OUTSIDE PERCENTAGES, FOLD CHANGES AND LOG10 DEPTHS.
    Every integer below a hundred occurs somewhere in this manuscript for some
    unrelated reason, so a bare number is never treated as a coarse rendering of
    another one.  A quantity has to carry a unit before it is compared at all,
    and the contradiction branch is narrowed further to percentages: a log10
    depth and a fold change have too many near-neighbours in this paper for the
    identity test to be safe at HIGH.

  * TREATED AGAINST UNTREATED AS A SCOPE QUALIFIER.  Those two words appear
    incidentally in nearly every sentence about the six-laboratory deposit, so
    as a scope test they fire on prose that has not widened anything.  The
    qualifier families kept are the plating volume, the culture-age panel, the
    reading day and the adjustment state.

WHERE THIS CHECKER STOPS.  Measured by mutating a copy of the assembled paper
and re-running, so these are demonstrated gaps rather than suspected ones:

  * THE CENSUS ARITHMETIC REACHES TWO SENTENCES.  Twenty-five sentences in this
    manuscript have the shape "N of the M things"; two of them have a table
    whose data rows equal M, and only those two are checked.  The gate is
    deliberate -- see the cross-talk note below -- but it means a broken census
    over a set with no table ("four of the six laboratories record a crossing;
    three do so in every arm and the other two do not") passes in silence.  The
    summary reports the number it could not check, so the reach is visible
    rather than implied.

  * THE CENSUS NOUN LIST IS CLOSED.  "Six of the nine confounders" is not read
    as a census at all, because "confounders" is not in CENSUS_NOUNS.  Any new
    collective noun has to be added by hand.

  * A DELETION LARGE ENOUGH TO REMOVE A QUALIFIER CAN BREAK THE MATCH THAT
    WOULD FIND IT.  The scope rule pairs a Results sentence with the legend
    repeating it by shared words.  The qualifier's own vocabulary is stripped
    out of that fingerprint, precisely so that deleting it does not delete the
    evidence -- but a real deletion takes neighbouring words with it.  Measured:
    strip "at day 5 after 15 days of prior culture" from Table 4's legend and
    the pair falls from 8 shared words at 0.50 containment to 6 at 0.43, under
    the gate, and the rule goes quiet.  Loosening the gate to 0.40 recovers that
    case and adds a false one on the manuscript as it stands (Table 15's row 29,
    on starting-density spread between panels, matched against a Results
    sentence about crossings at the most sensitive plating), so the gate stays
    where it is and this class is only partly covered.

  * THE SCOPE RULE ONLY LOOKS FORWARD FROM THE RESULTS.  A qualifier that a
    legend or a self-audit row carries and the Results do not is never
    examined; nor is a Discussion or Methods sentence repeating a Results claim.

  * A COUNT SPELT "one hundred and thirty-nine" IS NOT PARSED.  The audit-count
    pattern reads digits and simple number words, not compound hundreds.  Such a
    sentence is not silently ignored -- it falls to audit-count-missing-from-
    paper at MEDIUM -- but it is not read as a drift.

  * THE FRACTION-WORD RULE ABSTAINS ON A FOUR-WORD MATCH.  It needs five shared
    content words at half containment and reports nothing below that, which is
    why "about half of the series that cross return above the floor" against the
    60 per cent that states the same thing fires only when the two sentences are
    worded alike.  It is a LOW receipt, not a guarantee.

Conventions learned from the Methods and deliberately not flagged: 90, 99, 99.9,
99.99, 99.999 and 99.9999 per cent are endpoint definitions; 95 per cent is a
confidence level, 5 per cent a false discovery rate, 100 per cent a saturated
cell and 50 per cent a median; 0.5 McFarland, 0.4 optical density and the
plated volumes 100, 10 and 2.5 microlitres are protocol constants.
"""
from __future__ import annotations

import ast
import contextlib
import io
import itertools
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# text utilities
# --------------------------------------------------------------------------

_SUPERSCRIPTS = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5",
                 "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-"}
_SUBSCRIPTS = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5"}


def _normalise(s: str) -> str:
    """Fold the typography the manuscript uses into ASCII."""
    out = []
    for ch in s:
        if ch in _SUPERSCRIPTS:
            out.append(_SUPERSCRIPTS[ch])
        elif ch in _SUBSCRIPTS:
            out.append(_SUBSCRIPTS[ch])
        elif ch in "‐‑‒–—−":
            out.append("-")
        elif ch in "’‘":
            out.append("'")
        elif ch in "“”":
            out.append('"')
        elif ch in "    ":
            out.append(" ")
        else:
            out.append(ch)
    return "".join(out)


def _plain(s: str) -> str:
    """Strip the markdown emphasis that splits a phrase in the middle."""
    return re.sub(r"[*_`]+", "", s)


NUMWORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100,
}
_TENS = ("twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty",
         "ninety")
_UNITS = ("one", "two", "three", "four", "five", "six", "seven", "eight",
          "nine")

# "thirty-three", "twenty two", "one hundred and forty"
_COMPOUND = r"(?:%s)(?:[- ](?:%s))?" % ("|".join(_TENS), "|".join(_UNITS))
_WORD_NUM = r"(?:%s|%s)" % (_COMPOUND, "|".join(sorted(NUMWORDS, key=len,
                                                       reverse=True)))
_DIGIT_NUM = r"\d{1,3}(?:[, ]\d{3})*"
NUM_PAT = r"(?:%s|%s)" % (_DIGIT_NUM, _WORD_NUM)


def numeral(token: str):
    """'thirty-three' -> 33, '2 775' -> 2775, '17' -> 17, else None."""
    t = token.strip().lower().replace(",", "")
    if re.fullmatch(r"\d[\d ]*", t):
        return int(t.replace(" ", ""))
    parts = re.split(r"[- ]+", t)
    if len(parts) == 2 and parts[0] in _TENS and parts[1] in _UNITS:
        return NUMWORDS[parts[0]] + NUMWORDS[parts[1]]
    if len(parts) == 1 and parts[0] in NUMWORDS:
        return NUMWORDS[parts[0]]
    return None


STOP = set("""a an and are as at be been being below but by can could did do does
each for from had has have here how in into is it its may might must no not of
on only or other our out over per rather same second so some than that the their
then there these they this those to under up was were what when where which
while who will with would above after again all also always any because before
both cannot even ever every few first give given how just least less like made
make many more most much never new now off once one two three four five six
seven eight nine ten own part per same say see still such take than them
therefore though through together too very well what whether why within without
cent""".split())


def content_words(s: str) -> set:
    """Distinctive words of a sentence: the fingerprint a claim carries."""
    flat = _plain(_normalise(s)).lower()
    return {w for w in re.findall(r"[a-z][a-z-]{3,}", flat) if w not in STOP}


# --------------------------------------------------------------------------
# regions: where in the manuscript a sentence sits
# --------------------------------------------------------------------------

# Table 15 is the self-audit table; its rows are claims, not data, and are
# treated as a region of their own.
SELF_AUDIT_TABLE = "15"

_TABLE_HEAD = re.compile(r"\*\*Table\s+(S?\d+)\.\*\*")
_FIGURE_HEAD = re.compile(r"\*\*Figure\s+(\d+)\.")


class Manuscript:
    """The assembled paper, cut into blocks that know where they sit.

    A block is a paragraph, a legend with its own table body, or one row of the
    self-audit table.  Every block carries the region it belongs to, so a claim
    can be compared with the same claim in a different region -- which is the
    whole point of the scope rule.
    """

    def __init__(self, text: str):
        self.text = text
        self.lines = text.split("\n")
        self.blocks = []            # (line, region, label, body_text)
        self.table_rows = {}        # table number -> [row strings]
        self.table_legend = {}      # table number -> legend text
        self._segment()

    # -- segmentation ------------------------------------------------------
    def _segment(self):
        lines = self.lines
        section = "front matter"
        subsection = ""
        current = None              # open prose paragraph
        n = len(lines)

        def flush():
            nonlocal current
            if current:
                self.blocks.append(current)
            current = None

        i = 0
        while i < n:
            raw = lines[i]
            s = raw.strip()

            if s.startswith("#"):
                flush()
                title = s.lstrip("#").strip()
                h = title.lower()
                # A level-2 heading names the part of the paper; a deeper one
                # names the numbered Results section or Discussion subsection,
                # which is where a finding has to be actionable.
                if s.startswith("## ") or s.startswith("# "):
                    subsection = ""
                    section = ("abstract" if h.startswith("abstract") else
                               "results" if h.startswith("results") else
                               "discussion" if h.startswith("discussion") else
                               "methods" if h.startswith("methods") else
                               "conclusion" if h.startswith("conclusion") else
                               "figure legends" if "figure legend" in h else
                               "supplementary" if "supplementary" in h else
                               "other")
                else:
                    subsection = title
                i += 1
                continue

            if not s or s.startswith("!["):
                flush()
                i += 1
                continue

            m = _TABLE_HEAD.match(s)
            if m:
                flush()
                num = m.group(1)
                body = [s]
                j = i + 1
                while j < n and lines[j].strip() and \
                        not lines[j].lstrip().startswith("|"):
                    body.append(lines[j].strip())
                    j += 1
                # tables.md puts a blank line between a legend and its body
                k = j
                while k < n and not lines[k].strip():
                    k += 1
                rows = []
                if k < n and lines[k].lstrip().startswith("|"):
                    j = k
                    while j < n and lines[j].lstrip().startswith("|"):
                        rows.append(lines[j].strip())
                        j += 1
                legend_text = " ".join(body)
                self.table_legend[num] = legend_text
                self.table_rows[num] = rows
                self.blocks.append((i + 1, "table legend", "Table %s legend" % num,
                                    legend_text))
                if num == SELF_AUDIT_TABLE:
                    for k, row in enumerate(rows):
                        if set(row.replace("|", "").strip()) <= set("- :"):
                            continue
                        self.blocks.append(
                            (i + 1 + len(body) + k, "self-audit row",
                             "Table %s row %d" % (num, k + 1), row))
                i = j
                continue

            m = _FIGURE_HEAD.match(s)
            if m:
                flush()
                num = m.group(1)
                body = [s]
                j = i + 1
                while j < n:
                    t = lines[j].strip()
                    if (not t or _FIGURE_HEAD.match(t) or _TABLE_HEAD.match(t)
                            or t.startswith("![") or t.startswith("#")
                            or t.startswith("---")):
                        break
                    body.append(t)
                    j += 1
                self.blocks.append((i + 1, "figure legend",
                                    "Figure %s legend" % num, " ".join(body)))
                i = j
                continue

            if s.startswith("|"):
                flush()
                i += 1
                continue

            if current is None:
                where = ("%s, %s" % (section, subsection[:60]) if subsection
                         else section)
                current = [i + 1, section, where, s]
            else:
                current[3] = current[3] + " " + s
            i += 1

        flush()
        self.blocks = [tuple(b) for b in self.blocks]

    # -- derived views -----------------------------------------------------
    def sentences(self):
        """(line, region, label, sentence) over every prose-bearing block."""
        out = []
        for line, region, label, body in self.blocks:
            if region == "self-audit row":
                out.append((line, region, label, body))
                continue
            flat = re.sub(r"\s+", " ", body).strip()
            for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(*—\"'])", flat):
                s = s.strip()
                if s:
                    out.append((line, region, label, s))
        return out

    def data_rows(self, number: str) -> int:
        """Data rows of a table: its body less header and separator."""
        rows = self.table_rows.get(number)
        if not rows:
            return -1
        body = [r for r in rows
                if not set(r.replace("|", "").strip()) <= set("- :")]
        return max(0, len(body) - 1)          # the first row is the header


# --------------------------------------------------------------------------
# RULE 1 -- category census
# --------------------------------------------------------------------------

# Nouns that name a countable set the paper censuses.  A closed list, because
# "5 of 6 laboratories" is a census and "3 of 4 logs" is not: the second is a
# depth, and its "of" is not partitive.
CENSUS_NOUNS = {
    "covariates", "analyses", "exclusions", "laboratories", "isolates",
    "tests", "deposits", "series", "flasks", "pairs", "calls", "classes",
    "readings", "flags", "cultures", "columns", "conclusions", "failures",
    "terms", "platings", "arms", "panels", "cells", "sets", "thresholds",
    "boundaries", "curves", "institutes", "rows", "clones", "strata",
    "predictors", "members", "questions", "verdicts", "labels", "volumes",
    "endpoints", "stages", "checkers", "figures", "tables", "sections",
}

# Units of measurement, never a census even in the "N of M" shape.
CENSUS_SKIP_NOUNS = {"logs", "days", "hours", "decades", "orders", "times",
                     "fold", "per", "cent", "log10"}

CENSUS_RE = re.compile(
    r"\b(?P<n>" + NUM_PAT + r")\s+of\s+(?:the\s+)?(?P<m>" + NUM_PAT + r")\s+"
    r"(?P<tail>(?:[A-Za-z][\w'-]*[\s,]+){0,3}[A-Za-z][\w'-]*)", re.I)


def _census_noun(tail: str):
    """The set a census counts: the first word of the tail that names one.

    "the nine pretreatment covariates the file carries" has to yield
    "pretreatment covariates" and not "pretreatment", and not "covariates the
    file".  Walk the tail and stop at the first countable noun.
    """
    words = re.findall(r"[A-Za-z][\w'-]*", tail)
    for i, w in enumerate(words):
        low = w.lower()
        if low in CENSUS_SKIP_NOUNS:
            return None
        if low in CENSUS_NOUNS:
            return " ".join(words[: i + 1])
    return None

TABLE_REF = re.compile(r"\bTable\s+(S?\d+)\b")

# A part of a census, marked as such by the text.  These are the only shapes
# accepted: each one names its own count and ties it to the census by an
# anaphor, by the census noun, or by an explicit complement word.
PART_PATTERNS = [
    ("complement", re.compile(
        r"\b(?:the\s+)?(?:other|remaining|rest|last)\s+(?P<k>" + NUM_PAT + r")\b",
        re.I)),
    ("complement", re.compile(
        r"\bOnly\s+(?P<k>" + NUM_PAT + r")\s+(?P<noun>[A-Za-z][\w'-]*)\b")),
    ("anaphoric", re.compile(
        r"\b(?P<k>" + NUM_PAT + r")\s+of\s+(?:them|these|those)\b", re.I)),
    ("named", re.compile(
        r"(?:^|(?<=[.;:]\s))(?P<k>" + NUM_PAT + r")\s+(?:are|were)\b", re.I)),
]

# An enumerated partition: three or more clauses, each opening with a number.
ENUM_SPLIT = re.compile(r",\s+(?:and\s+)?|\s+and\s+")
# A partition is split on its commas and on sentence boundaries, but NOT on a
# bare "and": the Discussion writes "five do not survive and have been removed
# from the text", and splitting there loses the clause that follows it and
# turns a partition that adds up into one that does not.  The enumeration that
# opens Table 15's legend follows a full stop and starts with a digit, which no
# sentence splitter divides, so the run has to be found without one.
RUN_SPLIT = re.compile(r",\s+(?:and\s+)?|(?<=[.;:])\s+")


def _table_in_scope(sentence, region, label, ms):
    """Which table a census or an enumeration is answerable to, if any.

    Distinct tables, not distinct mentions: a Results paragraph that names
    Table 14 three times is still about one table, and an earlier build read
    that as "more than one table named" and stopped looking.
    """
    if region == "table legend":
        m = re.match(r"Table (S?\d+) legend", label)
        if m:
            return m.group(1)
    refs = set(TABLE_REF.findall(sentence))
    return refs.pop() if len(refs) == 1 else None


def _collect_parts(scope: str, noun: str):
    """Ordered part counts the text marks as parts of a census."""
    parts, seen = [], set()
    head = noun.split()[-1].lower()
    singular = head[:-1] if head.endswith("s") else head
    for kind, pat in PART_PATTERNS:
        for m in pat.finditer(scope):
            k = numeral(m.group("k"))
            if k is None or k <= 0 or k > 5000:
                continue
            if m.start() in seen:
                continue
            if kind == "complement" and "noun" in (pat.groupindex or {}):
                got = (m.groupdict().get("noun") or "").lower()
                if got and got not in (head, singular):
                    continue
            seen.add(m.start())
            parts.append((m.start(), k, kind))
    parts.sort()
    return parts


def _subset_sums(counts):
    """Every total a sub-collection of the parts can make."""
    sums = {0}
    for c in counts:
        sums |= {s + c for s in sums}
    return sums


def _census_readings(n, m, counts):
    """Every admissible reading of a parts chain.  True if any one holds.

    A census says N of M have some property and M - N do not, so a chain that
    enumerates the whole M must have a sub-collection making N.  "Parts sum to
    M" on its own is NOT accepted: five, two and two do sum to nine, but no
    combination of them makes six, which is exactly how the live defect read.
    """
    if not counts:
        return False
    total = sum(counts)
    return (
        (total == m and n in _subset_sums(counts))   # parts partition M, N in it
        or total == n                                # parts partition N
        or n + total == m                            # parts are N's complement
    )


def check_censuses(ms: Manuscript) -> list[dict]:
    """"N of the M things" against the parts the text goes on to name.

    Only a census the manuscript itself makes answerable is reported: one whose
    M equals the data-row count of the table it sits in or names.  A census with
    nothing to check it against -- "five of six laboratories record net growth"
    -- is counted in the summary and otherwise left alone, because reporting
    every one of those is how a checker gets switched off.
    """
    findings = []
    resolved = gated_total = ungated = 0

    for idx, (line, region, label, body) in enumerate(ms.blocks):
        if region == "self-audit row":
            continue
        flat = _plain(_normalise(body))
        for cm in CENSUS_RE.finditer(flat):
            n, m = numeral(cm.group("n")), numeral(cm.group("m"))
            noun = _census_noun(cm.group("tail"))
            if noun is None:
                continue
            if n is None or m is None or n < 2 or m <= n or m > 5000:
                continue

            table = _table_in_scope(flat, region, label, ms)
            rows = ms.data_rows(table) if table else -1

            # ONLY a census answerable to a table is arithmetic-checked.  Over
            # a manuscript this dense the complement markers cross-talk between
            # neighbouring censuses -- "the remaining two of the 33" sits four
            # words from a census of 84 -- and every ungated finding this rule
            # produced during development was that cross-talk rather than a
            # defect.  The uncheckable ones are counted in the summary instead.
            if rows != m:
                ungated += 1
                continue
            gated_total += 1

            # A census answerable to a table may run its partition over the two
            # paragraphs that follow it: the live example ran over three
            # consecutive paragraphs of Section 4.
            scope = flat[cm.end():]
            for nxt in ms.blocks[idx + 1: idx + 3]:
                if nxt[1] != region:
                    break
                scope += " " + _plain(_normalise(nxt[3]))

            parts = _collect_parts(scope, noun)
            counts = [k for _, k, _ in parts]
            anchored = any(kind == "complement" for _, _, kind in parts)
            where = "%s (line %d): \"%s\"" % (
                label, line,
                " ".join((cm.group("n") + " of " + cm.group("m") + " "
                          + noun).split()))

            if _census_readings(n, m, counts):
                resolved += 1
                continue

            # A chain whose parts do not even reach N is an INCOMPLETE
            # enumeration, not a contradiction: "seven of the nine fail, and
            # some of them are recorded only for resistant isolates; the other
            # two are the MICs" names parts of 2 and says nothing false.  Only
            # a chain that has already accounted for at least N can be held to
            # the arithmetic, and it was firing HIGH on the other case, which
            # is the wolf-crying this audit is not allowed to do.
            if counts and anchored and sum(counts) >= n:
                findings.append({
                    "severity": "high",
                    "kind": "census-parts-do-not-partition",
                    "where": where,
                    "detail": (
                        "the text says %d of the %d %s and then names parts of "
                        "%s; no reading of those parts partitions the census -- "
                        "they do not sum to %d, they do not sum to %d, and %d "
                        "plus them is not %d%s"
                        % (n, m, noun, ", ".join(str(c) for c in counts),
                           n, m, n, m,
                           " (Table %s has %d data rows, so the %d is the whole "
                           "set)" % (table, rows, m))),
                    "expected": "parts of the %d %s that account for all %d"
                                % (m, noun, m),
                    "found": "parts of %s" % ", ".join(str(c) for c in counts),
                })
                continue

            findings.append({
                "severity": "low",
                "kind": "census-not-resolved",
                "where": where,
                "detail": (
                    "resolved: the census claims %d of %d %s, and Table %s has "
                    "%d data rows, so the %d is the whole set. Not resolved: "
                    "%s, so this rule cannot confirm that %d %s are named or "
                    "that the categories partition the %d. Read it by eye"
                    % (n, m, noun, table, rows, m,
                       "the text names no counted part of the census in the "
                       "block it sits in or the two after it"
                       if not counts else
                       "the parts found (%s) reach only %d, short of the %d "
                       "the census claims, so the enumeration is unfinished "
                       "rather than wrong"
                       % (", ".join(str(c) for c in counts), sum(counts), n)
                       if sum(counts) < n else
                       "the parts found (%s) carry no complement marker, so "
                       "the parser cannot tell whether the enumeration is "
                       "finished" % ", ".join(str(c) for c in counts),
                       n, noun, m)),
                "expected": "%d parts accounted for" % m,
                "found": "%d part(s) named: %s"
                         % (len(counts),
                            ", ".join(str(c) for c in counts) or "none"),
            })

    findings.append({
        "severity": "low", "kind": "census-summary",
        "where": "whole manuscript",
        "detail": ("%d censuses of the form 'N of the M <things>' were checked "
                   "against the parts the text names and partition cleanly; "
                   "%d are answerable to a table whose rows equal M and are the "
                   "only ones the arithmetic runs on; %d have no such table and "
                   "are counted here rather than checked"
                   % (resolved, gated_total, ungated)),
        "expected": "every checkable census partitioned",
        "found": "%d resolved, %d gated on a table, %d not checkable"
                 % (resolved, gated_total, ungated),
    })
    return findings


# "Five are recorded almost exclusively for resistant isolates: the two
# susceptibility calls, the two Mykrobe calls and the mutation identity."
NAMED_HEAD = re.compile(
    r"(?:^|(?<=[.;]\s))(?:(?:the|these|those|its|their|all)\s+)?"
    r"(?P<n>" + NUM_PAT + r")\s+"
    r"(?:[A-Za-z][\w'-]*[\s,]+){0,12}?(?:are|were|is)\b[^:;.]{0,90}"
    r":\s*(?P<list>[^.;]+)", re.I)
# The optional determiner matters.  An earlier build anchored the count to the
# first token of a sentence, so it saw "Five are recorded ...: a, b and c" and
# was blind to "The five covariates recorded ... are: a, b and c" -- the same
# claim, the same list, the same defect, one article apart.  A rule that
# catches only the wording it was written against is an existence check.
DETERMINER = re.compile(
    r"^(?:the|a|an|its|their|each|every|both|" + _WORD_NUM + r")\b", re.I)
# a leading count inside a named item: "the two Mykrobe calls" is two things,
# "a six-laboratory consortium exercise" is one.
ITEM_COUNT = re.compile(
    r"^(?:(?:the|a|an|its|their|both)\s+)?(?P<k>" + NUM_PAT +
    r")\s+(?:[a-z][\w'-]*\s+){0,2}[a-z][\w'-]*s\b", re.I)


def check_named_items(ms: Manuscript) -> list[dict]:
    """"Five ...: a, b and c" -- are five things actually named?

    The live defect was exactly this: a sentence claimed six covariates could
    not adjust and then listed two susceptibility calls, two Mykrobe calls and
    one mutation identity, which is five.  The list is only counted when EVERY
    item in it opens with a determiner or a number, because that is the shape a
    clean enumeration has; a list whose items trail into qualifying clauses is
    reported as unresolved rather than counted wrongly, and one where fewer
    than half the fragments are determiner-led is not a list at all -- the
    colon is introducing an explanation -- so nothing is said about it.

    A claim is satisfied by EITHER reading of its count: the items themselves,
    or the things the items contain.  "Three kinds of column are recorded
    almost exclusively for resistant isolates: the two susceptibility calls,
    the two Mykrobe calls and the mutation identity" names three items holding
    five columns and both numbers are right.  Counting only the second reading
    graded that sentence HIGH and would have stopped the pipeline over correct
    English.
    """
    findings = []
    for line, region, label, body in ms.blocks:
        flat = _plain(_normalise(body))
        for m in NAMED_HEAD.finditer(flat):
            n = numeral(m.group("n"))
            if n is None or n < 2 or n > 30:
                continue
            items = [x.strip() for x in ENUM_SPLIT.split(m.group("list"))
                     if x.strip()]
            if len(items) < 2:
                continue
            quote = " ".join(m.group(0).split())[:110]
            led = sum(1 for i in items if DETERMINER.match(i))
            # Fewer than half the fragments determiner-led means the colon
            # introduces an explanation, not an enumeration -- "The five that
            # fail are all between-laboratory p-values computed on flasks:
            # every flask in a laboratory shares a starting culture, so ..."
            # There is no list there to count, and saying so at LOW is noise
            # rather than a partial result.
            if led * 2 < len(items):
                continue
            if led < len(items):
                findings.append({
                    "severity": "low", "kind": "named-items-not-resolved",
                    "where": "%s (line %d): \"%s\"" % (label, line, quote),
                    "detail": (
                        "resolved: the sentence says %d and then names a list. "
                        "Not resolved: %d of its %d items do not open with a "
                        "determiner or a count (%s), so the list runs into "
                        "qualifying clauses and cannot be counted mechanically. "
                        "Count it by eye"
                        % (n, sum(1 for i in items if not DETERMINER.match(i)),
                           len(items),
                           "; ".join(i[:34] for i in items
                                     if not DETERMINER.match(i))[:120])),
                    "expected": "%d items named" % n,
                    "found": "a list of %d fragments" % len(items),
                })
                continue
            total = 0
            for i in items:
                im = ITEM_COUNT.match(i)
                k = numeral(im.group("k")) if im else None
                total += k if k and k > 0 else 1
            # TWO readings, and the claim only has to satisfy one of them.
            # The count can be of the things the items enumerate -- five
            # columns in "the two susceptibility calls, the two Mykrobe calls
            # and the mutation identity" -- or of the items themselves, which
            # is what "three kinds of column are recorded ...: the two
            # susceptibility calls, the two Mykrobe calls and the mutation
            # identity" means.  Both are ordinary English and both are right.
            # Grading only the first reading made the second a HIGH, and a
            # HIGH stops the pipeline over a sentence with nothing wrong in it.
            if total == n or len(items) == n:
                continue
            findings.append({
                "severity": "high", "kind": "named-items-miscounted",
                "where": "%s (line %d): \"%s\"" % (label, line, quote),
                "detail": ("the sentence claims %d and then names %d item(s) "
                           "counting %d things, so it is neither a count of the "
                           "items nor of what they contain: %s"
                           % (n, len(items), total,
                              "; ".join("%s" % i[:40] for i in items))),
                "expected": "%d items, or items totalling %d" % (n, n),
                "found": "%d items totalling %d" % (len(items), total),
            })
    return findings


# A clause that names its own noun is enumerating THAT noun, not the rows of
# the table it happens to sit beside.  "4 deposits derive a floor from a plated
# volume, 2 infer one from a pile-up, 3 evidence none at all" is a legend
# sentence about deposits; it has no business being weighed against the
# legend's own row count, and an earlier build failed the pipeline on exactly
# that shape.  A partition of a table's rows is written nounlessly -- "20
# survive unchanged" -- because the noun is the table.  After a count above
# one, a following word ending in "s" is a plural noun, since an English verb
# agreeing with a plural subject does not take one; after a count of one the
# verb does, so the copulas are allowed back in.
_CLAUSE_HEAD = re.compile(r"^(?P<num>" + NUM_PAT + r")\s+(?P<w>[a-z][\w'-]*)", re.I)
_SINGULAR_VERBS = {"is", "was", "has", "does", "remains", "stays", "stands",
                   "survives", "fails", "holds", "goes", "runs", "needs",
                   "carries", "moves", "sits", "gives"}


def _numbered_runs(block: str):
    """Maximal runs of three or more NOUNLESS clauses that open with a number.

    "20 survive unchanged, 6 survive with materially wider uncertainty, 5 do
    not survive, and 1 is withdrawn" is such a run.  Working on runs rather
    than on whole sentences matters, because that sentence follows a full stop
    and a digit, which no sentence splitter divides.
    """
    frags = [f.strip() for f in RUN_SPLIT.split(block)]
    run, out = [], []
    for f in frags:
        m = _CLAUSE_HEAD.match(f)
        v = numeral(m.group("num")) if m else None
        if v is not None and v > 1:
            w = m.group("w").lower()
            if w.endswith("s") and w not in _SINGULAR_VERBS:
                v = None                    # the clause counts its own noun
        if v is None or v <= 0:
            if len(run) >= 3:
                out.append(list(run))
            run = []
            continue
        run.append((v, f))
    if len(run) >= 3:
        out.append(list(run))
    return out


def check_enumerated_partitions(ms: Manuscript) -> list[dict]:
    """A run of numbered clauses is a partition of the table it names."""
    findings = []
    for line, region, label, body in ms.blocks:
        if region == "self-audit row":
            continue
        flat = _plain(_normalise(body))
        table = _table_in_scope(flat, region, label, ms)
        if not table:
            continue
        rows = ms.data_rows(table)
        if rows <= 0:
            continue
        for run in _numbered_runs(flat):
            counts = [v for v, _ in run]
            if sum(counts) == rows:
                continue
            # Only a partition of the WHOLE table is checkable here.  A run of
            # clauses enumerating something smaller -- or something bigger than
            # the table, which is then not the table's rows at all -- is left
            # alone rather than guessed at.
            if max(counts) >= rows or not rows * 0.5 <= sum(counts) <= rows * 1.5:
                continue
            findings.append({
                "severity": "high", "kind": "enumerated-partition-total",
                "where": "%s (line %d): \"%s\""
                         % (label, line, "; ".join(f for _, f in run)[:120]),
                "detail": ("the clauses enumerate %s, which make %d, over a "
                           "Table %s that has %d data rows"
                           % (" + ".join(str(c) for c in counts), sum(counts),
                              table, rows)),
                "expected": "%d" % rows,
                "found": "%d" % sum(counts),
            })
    return findings


# --------------------------------------------------------------------------
# RULE 2 -- one quantity, two precisions
# --------------------------------------------------------------------------

PCT_RE = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)\s*(?:%|per\s+cent)")
FOLD_RE = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)[- ]?(?:fold|x\b)", re.I)
LOG_RE = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)\s*log10\b", re.I)

# Values that are definitions, levels or protocol constants, not measurements.
PCT_CONVENTIONS = {90.0, 99.0, 99.9, 99.99, 99.999, 99.9999, 95.0, 5.0, 100.0,
                   50.0, 0.0}
FOLD_CONVENTIONS = {10.0, 32.0, 2.0}
LOG_CONVENTIONS = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0}

FRACTION_WORDS = {
    "a quarter": 25.0, "one quarter": 25.0, "a third": 100.0 / 3,
    "one third": 100.0 / 3, "a half": 50.0, "one half": 50.0,
    "two thirds": 200.0 / 3, "two-thirds": 200.0 / 3,
    "three quarters": 75.0, "three-quarters": 75.0,
    "a fifth": 20.0, "a tenth": 10.0,
    # The hedged halves.  The docstring said "about half" was recognised and
    # it was not: the table held "a half" and "one half", neither of which any
    # of this manuscript's registers would ever write.  A bare "half" is NOT
    # here -- "half of one log10" and "half the flasks" are not shares.
    "about half": 50.0, "around half": 50.0, "roughly half": 50.0,
    "nearly half": 50.0, "almost half": 50.0, "more than half": 50.0,
    "over half": 50.0, "just under half": 50.0,
}
# Longest first: "more than half" has to win over "half", and Python's
# alternation takes the first branch that matches, not the longest.
FRACTION_RE = re.compile(
    r"\b(" + "|".join(sorted(FRACTION_WORDS, key=len, reverse=True)) + r")\b",
    re.I)


class Quantity:
    __slots__ = ("value", "raw", "dec", "unit", "line", "region", "label",
                 "sentence", "words", "numbers")

    def __init__(self, value, raw, dec, unit, line, region, label, sentence):
        self.value = value
        self.raw = raw
        self.dec = dec
        self.unit = unit
        self.line = line
        self.region = region
        self.label = label
        self.sentence = sentence
        self.words = content_words(sentence)
        # "log10", "MDK99", "10X MIC" and "OD 0.4" are names, not companion
        # figures; a companion has to be a quantity in its own right.
        stripped = re.sub(r"\b(?:log10|MDK\d+(?:\.\d+)?|OD)\b|10[X×x]\b",
                          " ", _normalise(sentence))
        self.numbers = set(re.findall(r"(?<![\d.])\d+(?:\.\d+)?",
                                      stripped)) - {raw}


def _quantities(ms: Manuscript):
    """Every percentage, fold change and log10 depth outside a data row."""
    out = []
    for line, region, label, sent in ms.sentences():
        flat = _plain(_normalise(sent))
        for pat, unit, conv in ((PCT_RE, "per cent", PCT_CONVENTIONS),
                                (FOLD_RE, "fold", FOLD_CONVENTIONS),
                                (LOG_RE, "log10", LOG_CONVENTIONS)):
            for m in pat.finditer(flat):
                raw = m.group(1)
                v = float(raw)
                if v in conv:
                    continue
                dec = len(raw.split(".")[1]) if "." in raw else 0
                out.append(Quantity(v, raw, dec, unit, line, region, label,
                                    flat))
    return out


def _same_quantity(a: Quantity, b: Quantity):
    """(strength, why) that two mentions are the same quantity, or None.

    Two independent signals are accepted, and one of them is required: a
    companion number shared by both sentences -- 26.2 per cent travels with
    7.6 per cent wherever it goes -- or a substantial overlap of distinctive
    content words.  A number alone is never enough.  "strong" needs both, and
    is what the contradiction branch demands before it fails a run.
    """
    companions = a.numbers & b.numbers
    shared = a.words & b.words
    small = min(len(a.words), len(b.words)) or 1
    if len(companions) >= 1 and len(shared) >= 5:
        return ("strong",
                "both sentences carry %s as a companion figure and share %s"
                % (", ".join(sorted(companions)[:3]),
                   ", ".join(sorted(shared)[:5])))
    if len(companions) >= 1 and len(shared) >= 3:
        return ("weak",
                "both sentences carry %s as a companion figure and share %s"
                % (", ".join(sorted(companions)[:3]),
                   ", ".join(sorted(shared)[:5])))
    if len(shared) >= 6 and len(shared) / small >= 0.55:
        return ("weak",
                "the two sentences share %s" % ", ".join(sorted(shared)[:6]))
    return None


def check_precision(ms: Manuscript) -> list[dict]:
    """One quantity quoted at two precisions, or at two incompatible values."""
    findings = []
    quants = _quantities(ms)
    seen = set()
    for a, b in itertools.combinations(quants, 2):
        if a.unit != b.unit:
            continue
        if a.line == b.line and a.sentence == b.sentence:
            continue
        # Equal values at unequal precision -- 26.2 against 26.20 -- are the
        # same defect as 26.2 against 26, and float equality hid them.
        if a.value == b.value and a.dec == b.dec:
            continue
        fine, coarse = (a, b) if a.dec > b.dec else (b, a)
        rounds_to = (fine.dec > coarse.dec
                     and round(fine.value, coarse.dec) == coarse.value)
        if not rounds_to:
            # An incompatible pair is only interesting when the two mentions
            # are plainly the same quantity AND close enough that one is a
            # drifted copy of the other rather than a different figure.
            # Restricted to percentages: a log10 depth and a fold change carry
            # far too many near-neighbours for the identity test to be safe.
            if coarse.unit != "per cent":
                continue
            if abs(fine.value - coarse.value) > max(0.5, 0.08 * fine.value):
                continue
        evidence = _same_quantity(a, b)
        if not evidence:
            continue
        strength, why = evidence
        if not rounds_to and strength != "strong":
            continue
        key = (round(fine.value, 6), round(coarse.value, 6),
               min(a.line, b.line), max(a.line, b.line))
        if key in seen:
            continue
        seen.add(key)
        if rounds_to:
            findings.append({
                "severity": "medium", "kind": "quantity-at-two-precisions",
                "where": "%s (line %d) and %s (line %d)"
                         % (coarse.label, coarse.line, fine.label, fine.line),
                "detail": ("the same quantity is quoted as %s %s and as %s %s; "
                           "%s. Both can be right, which is why this does not "
                           "fail the run, but only one of them should be in the "
                           "paper"
                           % (coarse.raw, coarse.unit, fine.raw, fine.unit, why)),
                "expected": "%s %s in both places" % (fine.raw, fine.unit),
                "found": "%s %s and %s %s" % (coarse.raw, coarse.unit,
                                              fine.raw, fine.unit),
            })
        else:
            findings.append({
                "severity": "medium", "kind": "quantity-at-two-values",
                "where": "%s (line %d) and %s (line %d)"
                         % (coarse.label, coarse.line, fine.label, fine.line),
                "detail": ("%s %s and %s %s look like one quantity written "
                           "twice, and %s is not a rounding of %s, so if they "
                           "are one quantity one of them has drifted; %s. "
                           "Reported and not failed: the evidence that they "
                           "are the same quantity is lexical, and two "
                           "different shares of the same set are described in "
                           "the same words"
                           % (coarse.raw, coarse.unit, fine.raw, fine.unit,
                              coarse.raw, fine.raw, why)),
                "expected": "one value, or two quantities named apart",
                "found": "%s and %s" % (coarse.raw, fine.raw),
            })
    findings += _check_fraction_words(ms, quants)
    return findings


def _check_fraction_words(ms: Manuscript, quants) -> list[dict]:
    """"a quarter" where the same claim is stated as a percentage elsewhere.

    Reported LOW and never higher.  There is no arithmetic here: 26.2 per cent
    is not a rounding of 25, so the only link is the lexical one, and a lexical
    link can attach a vague word to the wrong claim.  What the rule can say
    honestly is that a claim is made in words in one place and in figures in
    another, which is a thing an author wants to know about.
    """
    findings = []
    pcts = [q for q in quants if q.unit == "per cent"]
    for line, region, label, sent in ms.sentences():
        flat = _plain(_normalise(sent))
        m = FRACTION_RE.search(flat)
        if not m:
            continue
        approx = FRACTION_WORDS[m.group(1).lower()]
        words = content_words(flat)
        for q in pcts:
            if q.line == line:
                continue
            shared = words & q.words
            small = min(len(words), len(q.words)) or 1
            if len(shared) < 5 or len(shared) / small < 0.5:
                continue
            if not 0.6 * approx <= q.value <= 1.6 * approx:
                continue
            findings.append({
                "severity": "low", "kind": "quantity-in-words-and-figures",
                "where": "%s (line %d) and %s (line %d)"
                         % (label, line, q.label, q.line),
                "detail": ("\"%s\" states in words what %s per cent states in "
                           "figures; the two sentences share %s. Check they are "
                           "the same quantity -- this rule matches on wording, "
                           "not on arithmetic, because %s is not a rounding of "
                           "%g" % (m.group(1), q.raw,
                                   ", ".join(sorted(shared)[:5]), q.raw, approx)),
                "expected": "the figure, or the word, in both places",
                "found": "\"%s\" against %s per cent" % (m.group(1), q.raw),
            })
    return findings


# --------------------------------------------------------------------------
# RULE 3 -- does a qualifier travel with its claim
# --------------------------------------------------------------------------

# Families of qualifier, each a set of mutually exclusive scope choices this
# manuscript insists on distinguishing.  A claim that carries one of them in
# the Results and none of them in the legend that repeats it has been widened
# in the retelling.
QUALIFIERS = {
    "plating volume": [
        r"100\s*[uµμ]L", r"10\s*[uµμ]L",
        r"2\.5\s*[uµμ]L", r"most sensitive plating",
        r"most sensitive plating volume",
        r"(?:all|any of the|the) four platings", r"plating volume",
        r"least sensitive volume", r"quadruplicate plating",
    ],
    "culture age panel": [r"15[- ]days?", r"60[- ]days?", r"15d\b", r"60d\b"],
    "reading day": [r"\bday[- ](?:2|5|zero|0|one|1)\b"],
    "adjustment": [r"\bunadjusted\b", r"\badjusted\b", r"baseline[- ]only",
                   r"baseline isolates"],
}
# Deliberately NOT a family: treated against untreated.  The words appear
# incidentally in nearly every sentence about the six-laboratory deposit, so as
# a scope test they fire on prose that has not widened anything.

CLAIM_REGIONS = ("results", "figure legend", "table legend", "self-audit row")

_QUALIFIER_PATS = [re.compile(p, re.I)
                   for pats in QUALIFIERS.values() for p in pats]


def _families(s: str) -> set:
    flat = _plain(_normalise(s))
    return {fam for fam, pats in QUALIFIERS.items()
            if any(re.search(p, flat, re.I) for p in pats)}


def _claim_words(s: str) -> set:
    """The fingerprint of a claim, with the qualifier vocabulary removed.

    This rule pairs a Results sentence with the legend that repeats it by
    shared words, and then asks whether the qualifier travelled.  If the
    qualifier's own words are left in the fingerprint, deleting the qualifier
    also deletes the evidence that the two sentences are the same claim, and
    the pair drops below the matching threshold instead of being reported --
    the rule goes quiet on precisely the edit it exists to catch.  Measured on
    Table 4's legend: with the qualifier words in, the pair matched at 9 shared
    words and 0.53 containment; strip "at day 5 after 15 days of prior culture"
    from the legend and it fell to 6 and 0.43, under the gate.
    """
    flat = _plain(_normalise(s))
    for p in _QUALIFIER_PATS:
        flat = p.sub(" ", flat)
    return content_words(flat)


def check_scope(ms: Manuscript) -> list[dict]:
    """A Results qualifier that the legend repeating the claim does not carry."""
    # The context a legend really has is its whole block, not the one sentence:
    # a figure legend that says "at the 100 uL plating" in panel B scopes panel
    # C too, and a self-audit row is read together with its table's legend.
    block_families = {}
    for line, region, label, body in ms.blocks:
        block_families[(line, label)] = _families(body)
    audit_legend = _families(ms.table_legend.get(SELF_AUDIT_TABLE, ""))

    claims = []
    for line, region, label, sent in ms.sentences():
        if region not in CLAIM_REGIONS:
            continue
        if len(sent) < 45:
            continue
        claims.append((line, region, label, sent, _claim_words(sent)))

    findings, compared, matched = [], 0, 0
    for a, b in itertools.combinations(claims, 2):
        if a[1] == b[1]:
            continue
        if "results" not in (a[1], b[1]):
            continue
        src, dst = (a, b) if a[1] == "results" else (b, a)
        shared = src[4] & dst[4]
        small = min(len(src[4]), len(dst[4])) or 1
        if len(shared) < 5 or len(shared) / small < 0.50:
            continue
        compared += 1
        src_fams = _families(src[3])
        dst_ctx = set(block_families.get((dst[0], dst[2]), set()))
        if dst[1] == "self-audit row":
            dst_ctx |= audit_legend
        missing = src_fams - dst_ctx
        if not missing:
            matched += 1
            continue
        findings.append({
            "severity": "medium", "kind": "qualifier-not-propagated",
            "where": "%s (line %d), against %s (line %d)"
                     % (dst[2], dst[0], src[2], src[0]),
            "detail": ("the Results state this claim within a stated %s and the "
                       "%s repeating it names no %s at all; the two share %s"
                       % (" and ".join(sorted(missing)),
                          dst[1], " or ".join(sorted(missing)),
                          ", ".join(sorted(shared)[:6]))),
            "expected": "the %s carried over"
                        % " and ".join(sorted(missing)),
            "found": "\"%s\"" % dst[3][:150],
        })
    findings.append({
        "severity": "low", "kind": "scope-summary", "where": "whole manuscript",
        "detail": ("%d claims are stated in the Results and repeated in a "
                   "legend or in the self-audit table; %d carry every "
                   "qualifier family the Results attach to them"
                   % (compared, matched)),
        "expected": "every repeated claim as narrowly scoped as its original",
        "found": "%d of %d" % (matched, compared),
    })
    return findings


# --------------------------------------------------------------------------
# RULE 4 -- the audit's own count
# --------------------------------------------------------------------------

AUDIT_COUNT_RE = re.compile(
    r"(?:audit\s+script\s+)?recomputes\s+(?P<n>" + NUM_PAT + r")\s+"
    r"(?:of\s+the\s+)?(?:pinned\s+)?"
    r"(?:quantities|numbers|values|counts|figures|checks)", re.I)
# Deliberately loose about the noun and about digits against words.  The
# earlier pattern accepted only "recomputes N of the quantities" and
# "recomputes N pinned quantities"; rewriting the sentence as "recomputes 139
# of the numbers quoted in the text" made the drift invisible AND dropped the
# Methods silently out of the coverage receipt, which is the worse of the two
# failures -- the summary would have gone on saying the count was checked.


def _audit_claims_count(root: Path):
    """How many checks src/audit_claims.py actually runs.

    Run it and read its own count.  That is the only figure that cannot drift
    away from the truth, because it is the truth.  If the run is not possible --
    a missing table, a missing dependency -- fall back to counting the
    check(...) calls statically, and say which was used.
    """
    sys.path.insert(0, str(root))
    try:
        import importlib
        mod = importlib.import_module("src.audit_claims")
        importlib.reload(mod)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod.main()
        m = re.search(r"(\d+)\s+of\s+(\d+)\s+checks\s+agree", buf.getvalue())
        if m:
            return int(m.group(2)), "run"
    except KeyboardInterrupt:
        raise
    except BaseException as exc:                # noqa: BLE001 -- report, not raise
        # BaseException, not Exception: the audit script ends with
        # `raise SystemExit(main())` under __main__, and a future edit that
        # moves an exit inside main() would otherwise kill the whole manuscript
        # audit from inside a checker.
        note = "%s: %s" % (type(exc).__name__, exc)
    else:
        note = "the script ran but printed no count"
    finally:
        with contextlib.suppress(ValueError):
            sys.path.remove(str(root))

    src = root / "src" / "audit_claims.py"
    if not src.exists():
        return None, note
    try:
        tree = ast.parse(src.read_text(encoding="utf-8"))
    except SyntaxError:
        return None, note
    n = sum(1 for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "append"
            and node.args
            and isinstance(node.args[0], ast.Call)
            and getattr(node.args[0].func, "id", "") == "check")
    return n, "counted statically (%s); loops and guards are NOT expanded, so " \
              "this is a lower bound" % note


def check_audit_count(text: str, ctx: dict) -> list[dict]:
    """The Methods' count of recomputed quantities, against the script."""
    root = Path(ctx.get("root") or Path(__file__).resolve().parents[2])
    actual, how = _audit_claims_count(root)

    stated = []
    per_source = {}
    for label, body in (("Methods (PAPER_COMPLETE.md)", text),
                        ("manuscript/RATE_VS_DURATION.md", ctx.get("prose") or ""),
                        ("README.md", _read(root / "README.md"))):
        hits = 0
        for m in AUDIT_COUNT_RE.finditer(_normalise(body)):
            n = numeral(m.group("n"))
            if n is None:
                continue
            hits += 1
            line = body[:m.start()].count("\n") + 1
            stated.append((label, line, n, " ".join(m.group(0).split())))
        per_source[label] = hits

    findings = []
    # The assembled paper is generated FROM the prose source.  If the prose
    # states the size of the value audit and the assembled paper does not, the
    # assembled paper is behind its source -- which is exactly the state this
    # repository was in when this rule was first run, except that then the line
    # was present with a stale number rather than absent.  Without this the
    # coverage receipt would quietly say "2 places state that number" and read
    # as a clean result.
    if per_source["manuscript/RATE_VS_DURATION.md"] and \
            not per_source["Methods (PAPER_COMPLETE.md)"]:
        findings.append({
            "severity": "medium", "kind": "audit-count-missing-from-paper",
            "where": "manuscript/PAPER_COMPLETE.md, Methods",
            "detail": ("manuscript/RATE_VS_DURATION.md states how many "
                       "quantities the value audit recomputes and the assembled "
                       "paper states no such number, so the assembled paper is "
                       "behind its own source; re-run python -m "
                       "src.assemble_paper rather than editing prose"),
            "expected": "the Methods sentence present in both",
            "found": "present in the prose source, absent from the paper",
        })
    if actual is None:
        findings.append({
            "severity": "low", "kind": "audit-count-unverifiable",
            "where": "src/audit_claims.py",
            "detail": ("the value audit could not be counted (%s), so the "
                       "%d place(s) that state its size are unchecked" % (how,
                                                                         len(stated))),
            "expected": "a count from src/audit_claims.py",
            "found": how,
        })
        return findings

    # A count obtained by RUNNING the script is the truth and a disagreement
    # with it fails the run.  A count read off the source statically is a lower
    # bound -- the loops and the "if the table exists" guards are not expanded
    # -- so it is reported and does not fail anything.  A checker that stops a
    # pipeline because pandas was missing is the definition of crying wolf.
    ran = how == "run"
    for label, line, n, quote in stated:
        if n == actual or (not ran and n >= actual):
            continue
        findings.append({
            "severity": "high" if ran else "low", "kind": "audit-count-drift",
            "where": "%s (line %d)" % (label, line),
            "detail": ("\"%s\" but src/audit_claims.py runs %d checks (%s). "
                       "This number is a hand-typed count of something a script "
                       "decides, and it has drifted before" % (quote, actual, how)),
            "expected": str(actual),
            "found": str(n),
        })

    values = {n for _, _, n, _ in stated}
    if len(values) > 1:
        findings.append({
            "severity": "high", "kind": "audit-count-disagreement",
            "where": "; ".join("%s line %d says %d" % (l, ln, n)
                               for l, ln, n, _ in stated),
            "detail": ("the manuscript, its prose source and the README do not "
                       "state the same number of recomputed quantities"),
            "expected": "one number in every copy",
            "found": ", ".join(str(v) for v in sorted(values)),
        })

    if not stated:
        findings.append({
            "severity": "low", "kind": "audit-count-not-stated",
            "where": "Methods, Reproducibility",
            "detail": ("no sentence of the form 'recomputes N of the quantities' "
                       "was found; src/audit_claims.py runs %d checks" % actual),
            "expected": "the Methods to state the size of the value audit",
            "found": "no statement",
        })
    else:
        findings.append({
            "severity": "low", "kind": "audit-count-summary",
            "where": "whole repository",
            "detail": ("src/audit_claims.py runs %d checks (%s); %d place(s) "
                       "state that number: %s"
                       % (actual, how, len(stated),
                          "; ".join("%s line %d = %d" % (l, ln, n)
                                    for l, ln, n, _ in stated))),
            "expected": str(actual),
            "found": ", ".join(str(n) for _, _, n, _ in stated),
        })
    return findings


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------

def check(text: str, ctx: dict) -> list[dict]:
    """Return a list of findings.  Empty list means clean."""
    if not text or "**Table" not in text:
        root = Path(ctx.get("root", "."))
        text = (root / "manuscript" / "PAPER_COMPLETE.md").read_text(
            encoding="utf-8")
    ms = Manuscript(text)
    findings = (check_censuses(ms)
                + check_named_items(ms)
                + check_enumerated_partitions(ms)
                + check_precision(ms)
                + check_scope(ms)
                + check_audit_count(text, ctx))
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 3), f["kind"]))
    return findings


def main(argv: list[str] | None = None) -> int:
    with contextlib.suppress(Exception):        # legends carry N0, uL, 10^-3
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(__file__).resolve().parents[2]
    paper = Path(argv[0]) if argv else root / "manuscript" / "PAPER_COMPLETE.md"
    ctx = {"root": root}
    for key, rel in (("tables", "manuscript/tables.md"),
                     ("prose", "manuscript/RATE_VS_DURATION.md"),
                     ("abstract", "manuscript/abstract.md")):
        ctx[key] = _read(root / rel)
    findings = check(paper.read_text(encoding="utf-8"), ctx)
    print("check_census on %s" % paper)
    if not findings:
        print("  clean (0 findings)")
        return 0
    print("  %d finding(s)\n" % len(findings))
    for f in findings:
        print("[%-6s] %s  (%s)" % (f["severity"].upper(), f["kind"], f["where"]))
        print("         %s" % f["detail"])
        if "expected" in f:
            print("         expected: %s" % f["expected"])
        if "found" in f:
            print("         found:    %s" % f["found"])
        print()
    n_high = sum(1 for f in findings if f["severity"] == "high")
    print("%d high" % n_high)
    return 0


if __name__ == "__main__":
    sys.exit(main())
