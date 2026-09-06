"""Checker 3 of the manuscript audit: does every derived quantity follow from
its own stated inputs?

Every check here is self-contained.  It needs nothing but the assembled
manuscript, because the inputs and the result are both printed in it:

  (a) percentages quoted beside their own numerator and denominator -- as
      "22 of 84 ... 26.2 per cent", as "Of its 498 flags, 83, or 16.7 per
      cent", as "... in 48 (75%)", as "191 pairs ... 70 pairs - 36.6 per
      cent", as a percentage change across a stated fall, and as a table
      column whose numerator and denominator are two other columns;
  (b) fold-changes quoted beside the log10 difference or the two endpoints
      they were computed from, in prose and in table columns, including folds
      quoted against a stated reference concentration;
  (c) Benjamini-Hochberg critical values against 0.05 * rank / family, the
      survives-correction flags those thresholds imply, the step-up decision
      where a table prints a whole family, the survivor count in a legend, and
      the number of nominal hits a family expects by chance;
  (d) ranges quoted beside their own span, spans quoted beside the roster they
      were taken over, headroom quoted beside N0 and L, a log reduction
      written as a percentage, an equation written out in the text, and the
      subtraction in a table that walks a set down through its exclusions;
  (e) interval estimates, which must bracket the point estimate they belong
      to, in prose and in tables.

STATS records how many derived quantities each rule actually recomputed, so
that a clean run can be told apart from a run in which nothing was checked.

Two conventions of the manuscript are respected throughout, because ignoring
either of them manufactures false positives:

  * Methods, "Fold-change figures such as 216-fold and 265-fold are ten raised
    to the unrounded log10 difference before display rounding".  So a fold is
    never compared against 10 ** (displayed difference); every displayed number
    is read as the interval its own precision implies, and a finding is raised
    only when the interval the inputs allow cannot reach the interval the
    printed result allows.  4.42 log10 printed beside a 3.36-to-7.79 range is
    consistent, because 7.79 - 3.36 is 4.43 +- 0.01 and both come from the same
    unrounded 4.4236.

  * h is dimensionless by design, so a "span" printed in log10 units beside a
    range printed in CFU/mL is checked as a log ratio, not as a difference.

Run standalone:

    python -m src.audit.check_arithmetic
"""

from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path

# how many derived quantities each rule actually recomputed, so that a clean
# run can be told apart from a run in which nothing was checked
STATS: Counter = Counter()


def _tally(key: str, n: int = 1) -> None:
    STATS[key] += n

# --------------------------------------------------------------------------
# text preparation
# --------------------------------------------------------------------------

_SUPERSCRIPTS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"
_SUP_MAP = str.maketrans(_SUPERSCRIPTS, "0123456789-+")

# same-length substitutions, so character offsets survive them
_SAME_LENGTH = {
    "−": "-",   # minus sign
    "–": "-",   # en dash
    " ": " ",   # no-break space
    " ": " ",   # narrow no-break space
    " ": " ",   # thin space
    "*": " ",        # markdown emphasis
    "·": "*",   # middle dot, used for multiplication
    "×": "x",   # multiplication sign
}


def _prepare(text: str) -> tuple[str, list[int]]:
    """Return (working text, line number per working character).

    Superscript runs become ``^123`` so that ``6.1 x 10^6`` can be parsed by an
    ordinary number regex; that changes lengths, so the line number of every
    working character is recorded alongside.
    """
    out: list[str] = []
    lines: list[int] = []
    line = 1
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in _SUPERSCRIPTS:
            j = i
            while j < n and text[j] in _SUPERSCRIPTS:
                j += 1
            run = text[i:j].translate(_SUP_MAP)
            for c in "^" + run:
                out.append(c)
                lines.append(line)
            i = j
            continue
        if ch == "\n":
            out.append("\n")
            lines.append(line)
            line += 1
            i += 1
            continue
        out.append(_SAME_LENGTH.get(ch, ch))
        lines.append(line)
        i += 1
    return "".join(out), lines


# --------------------------------------------------------------------------
# numbers
# --------------------------------------------------------------------------

_MANT = r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)(?:\.\d+)?"
_NUMBER = (
    r"(?:"
    r"[+-]?" + _MANT + r"\s*[x*]\s*10\^[+-]?\d+"      # 6.1 x 10^6
    r"|[+-]?" + _MANT + r"[eE][+-]?\d+"                # 1.5e8
    r"|10\^[+-]?\d+"                                   # 10^-3
    r"|[+-]?" + _MANT +                                # 23 000, 4.42, 216
    r")"
)
_NUMBER_RE = re.compile(_NUMBER)


class Q:
    """A number as the manuscript prints it: a value and the interval its own
    display precision allows."""

    __slots__ = ("value", "half", "text")

    def __init__(self, value: float, half: float, text: str = ""):
        self.value = value
        self.half = half
        self.text = text

    @property
    def lo(self) -> float:
        return self.value - self.half

    @property
    def hi(self) -> float:
        return self.value + self.half

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Q({self.text or self.value}={self.value:g}+-{self.half:g})"


def parse_q(s: str, exact: bool = False) -> Q | None:
    """Parse one printed number into a value and its display half-width."""
    t = s.strip().replace(",", "")
    t = re.sub(r"(?<=\d) (?=\d)", "", t)          # 23 000 -> 23000
    m = re.fullmatch(r"([+-]?[\d.]*)\s*[x*]\s*10\^([+-]?\d+)", t)
    if m:
        mant_txt = m.group(1)
        exp = int(m.group(2))
        mant = float(mant_txt)
        half = 0.0 if exact else _half_of(mant_txt)
        return Q(mant * 10.0 ** exp, half * 10.0 ** exp, s.strip())
    m = re.fullmatch(r"10\^([+-]?\d+)", t)
    if m:
        return Q(10.0 ** int(m.group(1)), 0.0, s.strip())
    m = re.fullmatch(r"([+-]?[\d.]+)[eE]([+-]?\d+)", t)
    if m:
        mant = float(m.group(1))
        exp = int(m.group(2))
        half = 0.0 if exact else _half_of(m.group(1))
        return Q(mant * 10.0 ** exp, half * 10.0 ** exp, s.strip())
    if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", t):
        return Q(float(t), 0.0 if exact else _half_of(t), s.strip())
    return None


def _half_of(mant: str) -> float:
    if "." in mant:
        return 0.5 * 10.0 ** (-len(mant.split(".", 1)[1]))
    return 0.5


def _overlap(a_lo: float, a_hi: float, b_lo: float, b_hi: float,
             slack: float = 0.0) -> bool:
    eps = 1e-12 * max(1.0, abs(a_lo), abs(a_hi), abs(b_lo), abs(b_hi))
    return a_hi >= b_lo - slack - eps and a_lo <= b_hi + slack + eps


def _gap(a_lo: float, a_hi: float, b_lo: float, b_hi: float) -> float:
    if a_hi < b_lo:
        return b_lo - a_hi
    if b_hi < a_lo:
        return a_lo - b_hi
    return 0.0


def _fmt(x: float) -> str:
    if x == 0:
        return "0"
    if abs(x) >= 1e5 or abs(x) < 1e-3:
        return f"{x:.4g}"
    return f"{x:.6g}"


# interval arithmetic on Q, done by evaluating at the corners

def _iv_div(a: Q, b: Q) -> tuple[float, float] | None:
    corners = []
    for x in (a.lo, a.hi):
        for y in (b.lo, b.hi):
            if y == 0:
                return None
            corners.append(x / y)
    return min(corners), max(corners)


def _iv_sub(a: Q, b: Q) -> tuple[float, float]:
    return a.lo - b.hi, a.hi - b.lo


def _iv_pow10(a: Q) -> tuple[float, float]:
    return 10.0 ** a.lo, 10.0 ** a.hi


def _iv_log10(lo: float, hi: float) -> tuple[float, float] | None:
    if lo <= 0 or hi <= 0:
        return None
    return math.log10(lo), math.log10(hi)


# --------------------------------------------------------------------------
# word numerals
# --------------------------------------------------------------------------

_ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
_TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}
_ORDINALS = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6,
    "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
}


def word_number(word: str) -> int | None:
    w = word.strip().lower().replace("–", "-")
    if w in ("hundred", "a hundred", "one hundred"):
        return 100
    if w in _ONES:
        return _ONES[w]
    if w in _TENS:
        return _TENS[w]
    if "-" in w:
        a, _, b = w.partition("-")
        if a in _TENS and b in _ONES:
            return _TENS[a] + _ONES[b]
    if re.fullmatch(r"\d+", w):
        return int(w)
    return None


# --------------------------------------------------------------------------
# document model
# --------------------------------------------------------------------------

class Table:
    def __init__(self, label: str, legend: str, headers: list[str],
                 rows: list[list[str]], row_lines: list[int], line: int):
        self.label = label
        self.legend = legend
        self.headers = headers
        self.rows = rows
        self.row_lines = row_lines
        self.line = line

    def col(self, i: int) -> list[str]:
        return [r[i] if i < len(r) else "" for r in self.rows]

    def header_index(self, *needles: str) -> int | None:
        for i, h in enumerate(self.headers):
            low = h.lower()
            if any(nd in low for nd in needles):
                return i
        return None


class Doc:
    def __init__(self, text: str):
        self.raw = text
        self.work, self.line_of = _prepare(text)
        self.tables = self._parse_tables()
        self.sections = self._parse_sections()

    # -- locations ---------------------------------------------------------
    def line_at(self, pos: int) -> int:
        if 0 <= pos < len(self.line_of):
            return self.line_of[pos]
        return 0

    def section_at(self, pos: int) -> str:
        title = "front matter"
        for start, name in self.sections:
            if start <= pos:
                title = name
            else:
                break
        return title

    def where(self, pos: int) -> str:
        return f"{self.section_at(pos)} (line {self.line_at(pos)})"

    def _parse_sections(self) -> list[tuple[int, str]]:
        out = []
        for m in re.finditer(r"^#{1,4}\s+(.+)$", self.work, re.M):
            out.append((m.start(), m.group(1).strip()))
        return out

    # -- tables ------------------------------------------------------------
    def _parse_tables(self) -> list[Table]:
        lines = self.work.split("\n")
        # character offset of the start of every line
        offsets = []
        pos = 0
        for ln in lines:
            offsets.append(pos)
            pos += len(ln) + 1

        tables: list[Table] = []
        i = 0
        while i < len(lines):
            if lines[i].lstrip().startswith("|"):
                j = i
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    j += 1
                block = lines[i:j]
                if len(block) >= 3 and re.fullmatch(r"[|\s:-]+", block[1]):
                    headers = _split_row(block[0])
                    rows, row_lines = [], []
                    for k, ln in enumerate(block[2:], start=i + 2):
                        cells = _split_row(ln)
                        if any(c.strip() for c in cells):
                            rows.append(cells)
                            row_lines.append(self.line_at(offsets[k]))
                    label, legend = self._legend_for(lines, i)
                    tables.append(Table(label, legend, headers, rows,
                                        row_lines, self.line_at(offsets[i])))
                i = j
                continue
            i += 1
        return tables

    @staticmethod
    def _legend_for(lines: list[str], start: int) -> tuple[str, str]:
        """The nearest caption paragraph above a table block."""
        k = start - 1
        blanks = 0
        while k >= 0 and blanks < 3:
            ln = lines[k].strip()
            if not ln:
                blanks += 1
                k -= 1
                continue
            m = re.match(r"^\s{0,3}(Table|Box)\s+([A-Za-z0-9.]+?)\.?\s{2}", ln + "  ")
            if re.match(r"^\s{0,3}(Table|Box)\s+[A-Za-z0-9]+\.", ln):
                m2 = re.match(r"^\s{0,3}(Table|Box)\s+([A-Za-z0-9]+)\.", ln)
                label = f"{m2.group(1)} {m2.group(2)}"
                return label, ln
            k -= 1
        return "", ""


def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


# --------------------------------------------------------------------------
# cell helpers
# --------------------------------------------------------------------------

_MISSING = {"", "-", "--", "—", "na", "n/a", "none", "point mass", "true",
            "false", "yes", "no"}


def cell_scalar(cell: str) -> Q | None:
    t = cell.strip()
    if t.lower() in _MISSING:
        return None
    t = t.rstrip("%")
    if t.endswith(("x", "X")) and re.fullmatch(r"[\d., ]+[xX]", t):
        t = t[:-1]
    t = t.strip()
    if not re.fullmatch(r"[+-]?[\d., ]*\d(?:\s*\^?)?", t):
        # allow the 10^k form
        if not re.fullmatch(r"(?:[+-]?[\d.]+\s*[x*]\s*)?10\^[+-]?\d+", t):
            return None
    return parse_q(t)


_INTERVAL_RE = re.compile(
    r"^\[?\s*(?P<lo>[+-]?[\d., ]*\d)\s*(?:to|,|-)\s*(?P<hi>[+-]?[\d., ]*\d)\s*\]?%?$"
)


def cell_interval(cell: str) -> tuple[Q, Q] | None:
    t = cell.strip()
    if t.lower() in _MISSING or "/" in t:
        return None
    t = t.replace("%", "")
    m = _INTERVAL_RE.match(t)
    if not m:
        return None
    lo = parse_q(m.group("lo"))
    hi = parse_q(m.group("hi"))
    if lo is None or hi is None:
        return None
    if lo.value > hi.value:
        return None
    return lo, hi


# --------------------------------------------------------------------------
# finding helper
# --------------------------------------------------------------------------

def finding(severity, kind, where, detail, expected=None, found=None) -> dict:
    d = {"severity": severity, "kind": kind, "where": where, "detail": detail}
    if expected is not None:
        d["expected"] = expected
    if found is not None:
        d["found"] = found
    return d


def _grade(printed: Q, lo: float, hi: float) -> str | None:
    """None if the printed number is reachable from its inputs; otherwise a
    severity.  A miss no larger than one unit in the printed last digit is
    treated as display rounding and is not reported."""
    if _overlap(lo, hi, printed.lo, printed.hi):
        return None
    gap = _gap(lo, hi, printed.lo, printed.hi)
    tolerated = 2.0 * printed.half if printed.half else 0.0
    if gap <= tolerated:
        return None
    scale = max(abs(printed.value), 1e-12)
    return "high" if gap / scale > 0.05 else "medium"


# --------------------------------------------------------------------------
# (a) percentages
# --------------------------------------------------------------------------

_INT = r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)"
_PCT = r"(?P<pct>\d+(?:\.\d+)?)\s*(?:per cent|%)"

# "22 of 84 ... isolates, 26.2 per cent"
_A1 = re.compile(
    r"(?P<num>" + _INT + r"|[A-Za-z]+(?:-[a-z]+)?)\s+of\s+(?:the\s+|its\s+)?"
    r"(?P<den>" + _INT + r")\b"
)
# "Of the 360 series, only 56, or 15.6 per cent"
_A2 = re.compile(
    r"\b(?:[Oo]f|[Aa]mong)\s+(?:the\s+|its\s+|those\s+)?(?P<den>" + _INT + r")\s+"
    r"(?P<mid>[^.;:]{0,90}?),\s*(?:only\s+)?(?P<num>" + _INT + r")\b"
    r"(?P<mid2>[^.;:]{0,45}?),\s*(?:or\s+)?" + _PCT
)
# "of 64 treated series ... not a decline in 48 (75%)"
_A3 = re.compile(
    r"\bof\s+(?P<den>" + _INT + r")\s+(?P<mid>[^.;:|]{0,80}?)\b"
    r"(?P<num>" + _INT + r")\s*\(\s*(?P<pct>\d+(?:\.\d+)?)\s*%\s*\)"
)
# "Across 191 pairs ... 70 pairs - 36.6 per cent - are inversions":
# numerator and denominator carry the same noun
_A4 = re.compile(
    r"\b(?P<den>\d{2,})\s+(?P<noun>[a-z]{3,})\b(?P<mid>[^.;:|]{0,170}?)\b"
    r"(?P<num>\d+)\s+(?P=noun)\b(?P<mid2>[^.;:|]{0,24}?)" + _PCT
)
_PCT_RE = re.compile(_PCT)

# percentages that are endpoint names or conventional levels, never derived
_ENDPOINT_PCTS = {90.0, 99.0, 99.9, 99.99, 99.999, 99.9999, 95.0, 5.0}
_PCT_CONTEXT_STOP = re.compile(
    r"^\s*(?:endpoint|reduction|killing|kill|confidence|interval|CI|support|"
    r"false discovery|McFarland|of the variance|of the isolates)",
    re.I,
)


_HARD_STOP = re.compile(r"[.]\s+(?=[A-Z(])|\n\n")
_ANY_STOP = re.compile(r"[.;:]\s+|\n\n")


def _sentence_start(work: str, pos: int, back: int,
                    rx: "re.Pattern[str]" = _ANY_STOP) -> int:
    """Index just after the last sentence boundary before ``pos``.

    The caller chooses the boundary set, because a clause that states a range
    and the clause that states its span are often separated by a semicolon.
    """
    lo = max(0, pos - back)
    best = lo
    for m in rx.finditer(work[lo:pos]):
        best = lo + m.end()
    return best


def _sentence_end(work: str, pos: int, forward: int = 400) -> int:
    """End of the sentence containing ``pos`` -- a full stop before a capital,
    never the decimal point inside 2.67."""
    m = _HARD_STOP.search(work, pos, pos + forward)
    return m.start() if m else min(len(work), pos + forward)


def _sentence_window(work: str, start: int, span: int = 110) -> str:
    w = work[start:start + span]
    cut = re.search(r"(?<=[.;])\s+(?=[A-Z\s])|\n\n", w)
    if cut:
        w = w[:cut.start()]
    return w


def check_percentages(doc: Doc) -> list[dict]:
    out: list[dict] = []
    work = doc.work
    seen: set[tuple[int, int, int]] = set()

    for m in _A1.finditer(work):
        num_txt = m.group("num")
        den = parse_q(m.group("den"), exact=True)
        num = parse_q(num_txt, exact=True)
        if num is None:
            wn = word_number(num_txt)
            if wn is None:
                continue
            num = Q(float(wn), 0.0, num_txt)
        if den is None or den.value == 0 or num.value > den.value:
            continue
        window = _sentence_window(work, m.end())
        pm = _PCT_RE.search(window)
        if not pm:
            continue
        printed = parse_q(pm.group("pct"))
        if printed is None:
            continue
        tail = window[pm.end():]
        if printed.value in _ENDPOINT_PCTS and _PCT_CONTEXT_STOP.match(tail):
            continue
        expected = 100.0 * num.value / den.value
        _tally('percentage (prose, N of M)')
        sev = _grade(printed, expected, expected)
        if sev and printed.value in _ENDPOINT_PCTS:
            continue          # a conventional level standing next to a count
        if sev:
            key = (m.start(), m.end() + pm.start(), 1)
            if key in seen:
                continue
            seen.add(key)
            out.append(finding(
                sev, "percentage",
                doc.where(m.start()),
                f"{int(num.value)} of {int(den.value)} is "
                f"{expected:.4g} per cent, not the {printed.text} per cent printed "
                f"beside it.",
                expected=f"{expected:.4g}%", found=f"{printed.text}%"))

    for m in _A2.finditer(work):
        den = parse_q(m.group("den"), exact=True)
        num = parse_q(m.group("num"), exact=True)
        printed = parse_q(m.group("pct"))
        if not (den and num and printed) or den.value == 0:
            continue
        if num.value > den.value or printed.value > 100:
            continue
        expected = 100.0 * num.value / den.value
        _tally('percentage (prose, of-M-then-N)')
        sev = _grade(printed, expected, expected)
        if sev:
            key = (m.start(), m.end(), 2)
            if key in seen:
                continue
            seen.add(key)
            out.append(finding(
                sev, "percentage",
                doc.where(m.start()),
                f"{int(num.value)} of {int(den.value)} is {expected:.4g} per cent, "
                f"not the {printed.text} per cent printed beside it.",
                expected=f"{expected:.4g}%", found=f"{printed.text}%"))

    for rx, label in ((_A3, "prose, of-M-then-N-in-brackets"),
                      (_A4, "prose, same noun")):
        for m in rx.finditer(work):
            den = parse_q(m.group("den"), exact=True)
            num = parse_q(m.group("num"), exact=True)
            printed = parse_q(m.group("pct"))
            if not (den and num and printed) or den.value == 0:
                continue
            if num.value > den.value or printed.value > 100:
                continue
            if printed.value in _ENDPOINT_PCTS:
                continue
            expected = 100.0 * num.value / den.value
            _tally(f"percentage ({label})")
            sev = _grade(printed, expected, expected)
            if not sev:
                continue
            key = (m.start(), m.end(), 3)
            if key in seen:
                continue
            seen.add(key)
            out.append(finding(
                sev, "percentage", doc.where(m.start()),
                f"{int(num.value)} of {int(den.value)} is {expected:.4g} per "
                f"cent, not the {printed.text} per cent printed beside it.",
                expected=f"{expected:.4g}%", found=f"{printed.text}%"))

    out += _check_percentage_change(doc)
    return out


_PCT_CHANGE = re.compile(
    r"falls?\s+from\s+(?P<a>[\d.]+)\s+to\s+(?P<b>[\d.]+)"
    r"(?P<mid>[^.;]{0,60}?),\s*(?:a|an)\s+(?P<pct>\d+(?:\.\d+)?)\s*(?:per cent|%)\s*"
    r"(?P<what>shortening|reduction|fall|drop|decrease|decline)"
)


def _check_percentage_change(doc: Doc) -> list[dict]:
    out = []
    for m in _PCT_CHANGE.finditer(doc.work):
        a = parse_q(m.group("a"))
        b = parse_q(m.group("b"))
        printed = parse_q(m.group("pct"))
        if not (a and b and printed) or a.value == 0:
            continue
        _tally('percentage change (prose)')
        lo = 100.0 * (a.lo - b.hi) / a.hi
        hi = 100.0 * (a.hi - b.lo) / a.lo
        sev = _grade(printed, lo, hi)
        if sev:
            out.append(finding(
                sev, "percentage-change", doc.where(m.start()),
                f"a fall from {a.text} to {b.text} is "
                f"{100.0 * (a.value - b.value) / a.value:.4g} per cent, not the "
                f"{printed.text} per cent printed.",
                expected=f"{100.0 * (a.value - b.value) / a.value:.4g}%",
                found=f"{printed.text}%"))
    return out


# --------------------------------------------------------------------------
# (a)/(b) table columns: percentages, folds, spans, headroom
# --------------------------------------------------------------------------

def _column_kind(header: str, cells: list[str]) -> str | None:
    h = header.lower()
    body = [c for c in cells if c.strip() and c.strip().lower() not in _MISSING]
    pct_like = sum(1 for c in body if c.strip().rstrip(")").endswith("%"))
    fold_like = sum(1 for c in body if re.fullmatch(r"[\d., ]+[xX]", c.strip()))
    if "fold" in h or (body and fold_like >= max(2, len(body) // 2)):
        return "fold"
    if ("per cent" in h or "%" in h or "fraction" in h or "proportion" in h
            or (body and pct_like >= max(2, len(body) // 2))):
        return "percentage"
    if h.strip() in ("h", "median h", "headroom") or "headroom" in h:
        return "headroom"
    if "span" in h or h.strip() == "spread":
        return "span"
    return None


def _reference_in_legend(legend: str) -> Q | None:
    m = re.search(r"reference,\s*(" + _NUMBER + r")", legend)
    if m:
        return parse_q(m.group(1))
    return None


def _formulas(kind: str, ref: Q | None):
    """Yield (name, arity, fn) where fn maps Q values to an interval."""
    if kind == "percentage":
        yield ("100 * {a} / {b}", 2,
               lambda a, b: (lambda r: None if r is None else
                             (100 * r[0], 100 * r[1]))(_iv_div(a, b)))
    elif kind == "fold":
        yield ("{a} / {b}", 2, _iv_div)
        yield ("10 ^ {a}", 1, lambda a: _iv_pow10(a))
        yield ("10 ^ ({a} - {b})", 2,
               lambda a, b: _iv_pow10(Q((a.value - b.value),
                                        (a.half + b.half))))
        if ref is not None:
            yield (f"{_fmt(ref.value)} / 10 ^ {{a}}", 1,
                   lambda a: (ref.lo / 10.0 ** a.hi, ref.hi / 10.0 ** a.lo))
    elif kind == "span":
        yield ("{a} - {b}", 2, _iv_sub)
        yield ("log10({a} / {b})", 2,
               lambda a, b: (lambda r: None if r is None else _iv_log10(*r))(
                   _iv_div(a, b)))
    elif kind == "headroom":
        yield ("log10({a} / {b})", 2,
               lambda a, b: (lambda r: None if r is None else _iv_log10(*r))(
                   _iv_div(a, b)))


def check_table_columns(doc: Doc) -> list[dict]:
    out: list[dict] = []
    for tbl in doc.tables:
        if not tbl.rows or len(tbl.headers) < 2:
            continue
        # scalar values per row, per column
        scal: list[list[Q | None]] = []
        for row in tbl.rows:
            scal.append([cell_scalar(row[i]) if i < len(row) else None
                         for i in range(len(tbl.headers))])
        # bracketed intervals contribute two pseudo-columns
        extra: dict[int, tuple[list[Q | None], list[Q | None]]] = {}
        for ci in range(len(tbl.headers)):
            los, his = [], []
            got = 0
            for row in tbl.rows:
                iv = cell_interval(row[ci]) if ci < len(row) else None
                if iv:
                    got += 1
                    los.append(iv[0])
                    his.append(iv[1])
                else:
                    los.append(None)
                    his.append(None)
            if got >= 2:
                extra[ci] = (los, his)

        ref = _reference_in_legend(tbl.legend)
        for ci, header in enumerate(tbl.headers):
            kind = _column_kind(header, tbl.col(ci))
            if kind is None:
                continue
            target = [s[ci] for s in scal]
            if sum(1 for t in target if t is not None) < 2:
                continue
            # candidate source columns
            sources: list[tuple[str, list[Q | None]]] = []
            for cj in range(len(tbl.headers)):
                if cj == ci:
                    continue
                col = [s[cj] for s in scal]
                if any(v is not None for v in col):
                    sources.append((tbl.headers[cj] or f"col{cj}", col))
                if cj in extra:
                    sources.append((tbl.headers[cj] + " lo", extra[cj][0]))
                    sources.append((tbl.headers[cj] + " hi", extra[cj][1]))

            best = None
            for name, arity, fn in _formulas(kind, ref):
                combos = []
                if arity == 1:
                    combos = [(s,) for s in sources]
                else:
                    combos = [(a, b) for a in sources for b in sources
                              if a[0] != b[0]]
                for combo in combos:
                    hits, misses = 0, []
                    for ri in range(len(tbl.rows)):
                        t = target[ri]
                        args = [c[1][ri] for c in combo]
                        if t is None or any(a is None for a in args):
                            continue
                        try:
                            res = fn(*args)
                        except (ValueError, ZeroDivisionError, OverflowError):
                            res = None
                        if res is None:
                            continue
                        if _grade(t, res[0], res[1]) is None:
                            hits += 1
                        else:
                            misses.append((ri, res))
                    defined = hits + len(misses)
                    if hits >= 2 and defined and hits >= 0.6 * defined:
                        cand = (hits, -len(misses), name, combo, misses)
                        if best is None or cand[:2] > best[:2]:
                            best = cand
            if best is None:
                continue
            hits, _, name, combo, misses = best
            _tally(f'{kind} column (tables)', hits + len(misses))
            for ri, res in misses:
                t = target[ri]
                args = [c[1][ri] for c in combo]
                expr = name.format(a=args[0].text,
                                   b=args[1].text if len(args) > 1 else "")
                lbl = tbl.rows[ri][0] if tbl.rows[ri] else f"row {ri + 1}"
                out.append(finding(
                    "high" if kind in ("percentage", "fold") else "medium",
                    f"table-{kind}",
                    f"{tbl.label or 'table'}, row '{lbl}' "
                    f"(line {tbl.row_lines[ri]})",
                    f"column '{header}' prints {t.text} but {expr} "
                    f"(the formula every other row in the column obeys) gives "
                    f"{_fmt(res[0])} to {_fmt(res[1])}.",
                    expected=f"{_fmt(res[0])}..{_fmt(res[1])}", found=t.text))
    return out


def check_legend_tallies(doc: Doc) -> list[dict]:
    """A legend that counts its own verdicts -- '20 survive unchanged, 7
    survive with materially wider uncertainty, and 5 do not survive' -- is
    counting a column printed directly beneath it."""
    out: list[dict] = []
    for tbl in doc.tables:
        n_rows = len(tbl.rows)
        if n_rows < 4 or not tbl.legend:
            continue
        cats = None
        for ci in range(len(tbl.headers)):
            vals = [r[ci].strip() for r in tbl.rows if ci < len(r)]
            if len(vals) != n_rows or any(not v for v in vals):
                continue
            if any(cell_scalar(v) is not None for v in vals):
                continue
            distinct = set(vals)
            if 2 <= len(distinct) <= 6:
                cats = sorted(
                    (vals.count(v) for v in distinct), reverse=True)
                col = tbl.headers[ci]
                break
        if cats is None:
            continue
        for sent in re.split(r"(?<=[.])\s+", tbl.legend):
            ints = [int(x) for x in re.findall(r"(?<![\d.])(\d+)(?![\d.])",
                                               sent)]
            if len(ints) < 2:
                continue
            # A sentence is a tally of the column beneath it if its integers
            # sum to the row count -- or if it has one integer per category
            # and lands near the row count.  The second case matters: the
            # natural way to miscount a tally is to change one of its parts,
            # which breaks the sum, and a rule that insisted on the sum would
            # be blind to exactly the error it exists to find.
            slack = max(2.0, 0.25 * n_rows)
            if not (sum(ints) == n_rows
                    or (len(ints) == len(cats)
                        and all(0 <= i <= n_rows for i in ints)
                        and abs(sum(ints) - n_rows) <= slack)):
                continue
            _tally("legend tally against its own column (tables)")
            if sorted(ints, reverse=True) == cats:
                continue
            total = (f" (they total {sum(ints)} against {n_rows} rows)"
                     if sum(ints) != n_rows else "")
            out.append(finding(
                "medium", "legend-tally",
                f"{tbl.label or 'table'} legend (line {tbl.line})",
                f"the legend counts {', '.join(str(i) for i in ints)}, but the "
                f"'{col}' column of the {n_rows} rows below it divides as "
                f"{', '.join(str(c) for c in cats)}{total}.",
                expected=", ".join(str(c) for c in cats),
                found=", ".join(str(i) for i in ints)))
            break
    return out


def check_partition_sums(doc: Doc) -> list[dict]:
    """A table that splits its own n into mutually exclusive states -- Table
    10's 'never below', 'one crossing, holds', 'one crossing, returns' and
    'crosses repeatedly' -- prints the parts and the whole, so the addition is
    checkable.  A run is only trusted as a partition once it adds up on at
    least four fifths of the rows that define it, which is what tells a real
    breakdown apart from three columns that happen to sum on one row."""
    out: list[dict] = []
    for tbl in doc.tables:
        if len(tbl.rows) < 3 or len(tbl.headers) < 4:
            continue
        ncols = len(tbl.headers)
        cols: list[list[Q | None]] = []
        for ci in range(ncols):
            col: list[Q | None] = []
            for row in tbl.rows:
                raw = row[ci] if ci < len(row) else ""
                q = cell_scalar(raw)
                if (q is None or "%" in raw or q.value < 0
                        or q.value != int(q.value)):
                    col.append(None)
                else:
                    col.append(q)
            cols.append(col)

        best = None
        for ti in range(ncols):
            if sum(1 for v in cols[ti] if v is not None) < 3:
                continue
            for a in range(ncols):
                for b in range(a + 3, ncols + 1):     # runs of three or more
                    if a <= ti < b:
                        continue
                    parts = list(range(a, b))
                    hits, misses = 0, []
                    for ri in range(len(tbl.rows)):
                        t = cols[ti][ri]
                        vals = [cols[cj][ri] for cj in parts]
                        if t is None or any(v is None for v in vals):
                            continue
                        s = sum(v.value for v in vals)
                        if abs(s - t.value) < 1e-9:
                            hits += 1
                        else:
                            misses.append((ri, s, t))
                    defined = hits + len(misses)
                    if defined < 3 or hits < 2 or hits < 0.8 * defined:
                        continue
                    cand = (hits, -len(misses), ti, parts, misses)
                    if best is None or cand[:2] > best[:2]:
                        best = cand
        if best is None:
            continue
        hits, _, ti, parts, misses = best
        _tally("partition adds to its own total (tables)", hits + len(misses))
        names = " + ".join(tbl.headers[cj] or f"col{cj}" for cj in parts)
        for ri, s, t in misses:
            lbl = tbl.rows[ri][0] if tbl.rows[ri] else f"row {ri + 1}"
            out.append(finding(
                "high", "partition-sum",
                f"{tbl.label or 'table'}, row '{lbl}' "
                f"(line {tbl.row_lines[ri]})",
                f"'{names}' comes to {s:g}, but '{tbl.headers[ti]}' on the "
                f"same row is {t.text}; every other row of the table adds up.",
                expected=t.text, found=f"{s:g}"))
    return out


def check_exclusion_arithmetic(doc: Doc) -> list[dict]:
    """A table that walks an analysis set down through its exclusions prints
    both the surviving n and the number removed, so the subtraction is
    checkable row against row."""
    out: list[dict] = []
    for tbl in doc.tables:
        xi = tbl.header_index("excluded")
        if xi is None:
            continue
        ni = None
        for i, h in enumerate(tbl.headers):
            if h.strip().lower() in ("n", "count", "rows"):
                ni = i
        if ni is None:
            continue
        # a stage is subtracted from some earlier stage of the same deposit,
        # not necessarily from the line directly above it
        checks, bad = [], []
        earlier: list[tuple[str, float]] = []
        for ri, row in enumerate(tbl.rows):
            n = cell_scalar(row[ni]) if ni < len(row) else None
            block = row[0].strip() if row else ""
            drop_txt = row[xi].strip() if xi < len(row) else ""
            m = re.fullmatch(r"-\s*(\d+)", drop_txt)
            if n is not None and m:
                dropped = int(m.group(1))
                checks.append(ri)
                want = n.value + dropped
                if not any(b == block and abs(v - want) < 1e-9
                           for b, v in earlier):
                    bad.append((ri, n.value, dropped, want))
            if n is not None:
                earlier.append((block, n.value))
        if len(checks) < 2 or len(bad) > 0.4 * len(checks):
            continue
        _tally("exclusion subtraction (tables)", len(checks))
        for ri, n, dropped, want in bad:
            lbl = " / ".join(x for x in tbl.rows[ri][:4] if x and x != "-")
            out.append(finding(
                "medium", "exclusion-arithmetic",
                f"{tbl.label or 'table'}, row '{lbl}' "
                f"(line {tbl.row_lines[ri]})",
                f"n = {n:g} after dropping {dropped} implies a stage of "
                f"{want:g} to drop them from, and no earlier row of this "
                f"deposit carries that n.",
                expected=f"an earlier stage of n = {want:g}",
                found=f"n = {n:g}, -{dropped}"))
    return out


# --------------------------------------------------------------------------
# (b) fold-changes in prose
# --------------------------------------------------------------------------

_FOLD_RANGE = re.compile(
    r"(?P<fold>[\d.,]+)-fold(?P<mid>[^.;]{0,60}?)"
    r"(?:,\s*from|\(|\s+from)\s*(?P<a>" + _NUMBER + r")\s+to\s+(?P<b>" + _NUMBER + r")"
)
_FOLD_LOG = re.compile(
    r"(?P<d>\d+\.\d+)\s*log10\b(?P<mid>[^.;]{0,50}?),?\s*(?:a|an)\s+"
    r"(?P<fold>[\d.,]+)-fold"
)
_FOLD_TWO_VALUES = re.compile(
    r"at\s+(?P<a>\d+\.\d+)\s+log10\s+against\s+(?P<b>\d+\.\d+)\b"
    r"(?P<mid>[^.;]{0,40}?),\s*(?P<word>[a-z]+(?:-[a-z]+)?)-fold"
)


def check_folds(doc: Doc) -> list[dict]:
    out: list[dict] = []
    work = doc.work

    for m in _FOLD_RANGE.finditer(work):
        fold = parse_q(m.group("fold"))
        a = parse_q(m.group("a"))
        b = parse_q(m.group("b"))
        if not (fold and a and b) or a.value <= 0 or b.value <= 0:
            continue
        hi_q, lo_q = (b, a) if b.value >= a.value else (a, b)
        r = _iv_div(hi_q, lo_q)
        if r is None:
            continue
        _tally('fold beside its range (prose)')
        sev = _grade(fold, r[0], r[1])
        if sev:
            out.append(finding(
                sev, "fold-from-range", doc.where(m.start()),
                f"{hi_q.text} over {lo_q.text} is "
                f"{hi_q.value / lo_q.value:.4g}-fold, not the {fold.text}-fold "
                f"printed with the range.",
                expected=f"{_fmt(r[0])}..{_fmt(r[1])}x", found=f"{fold.text}x"))

    for m in _FOLD_LOG.finditer(work):
        d = parse_q(m.group("d"))
        fold = parse_q(m.group("fold"))
        if not (d and fold):
            continue
        lo, hi = _iv_pow10(d)
        _tally('fold beside a log10 difference (prose)')
        sev = _grade(fold, lo, hi)
        if sev:
            out.append(finding(
                sev, "fold-from-log", doc.where(m.start()),
                f"10 ^ {d.text} log10 is {10 ** d.value:.4g}-fold, which the "
                f"printed {fold.text}-fold cannot be a rounding of.",
                expected=f"{_fmt(lo)}..{_fmt(hi)}x", found=f"{fold.text}x"))

    for m in _FOLD_TWO_VALUES.finditer(work):
        a = parse_q(m.group("a"))
        b = parse_q(m.group("b"))
        w = word_number(m.group("word"))
        if not (a and b) or w is None:
            continue
        diff = Q(abs(b.value - a.value), a.half + b.half)
        lo, hi = _iv_pow10(diff)
        printed = Q(float(w), 0.5 if w >= 10 else 0.0, m.group("word"))
        _tally('fold between two stated log10 values (prose)')
        sev = _grade(printed, lo, hi)
        if sev:
            out.append(finding(
                sev, "fold-from-log", doc.where(m.start()),
                f"{b.text} against {a.text} log10 is "
                f"{10 ** abs(b.value - a.value):.4g}-fold, not "
                f"{m.group('word')}-fold.",
                expected=f"{_fmt(lo)}..{_fmt(hi)}x",
                found=f"{m.group('word')}-fold"))

    out += _check_fold_bucket_count(doc)
    return out


_BUCKET = re.compile(
    r"(?P<count>[A-Za-z]+|\d+)\s+of\s+the\s+(?P<total>[A-Za-z]+|\d+)\s+"
    r"sit\s+between\s+(?P<lo>[A-Za-z\d.]+)\s+and\s+(?:a\s+|an\s+)?"
    r"(?P<hi>[A-Za-z\d.]+)-fold\s+(?P<dir>below|above)\s+the\s+"
    r"(?P<what>[^.]{0,40}?target)"
)
_DENSITY_LIST = re.compile(
    r"densit(?:y|ies)\s+of\s+(?P<list>(?:" + _NUMBER + r"(?:,\s*|\s+and\s+))+"
    + _NUMBER + r")\s+log10"
)
_TARGET_VALUE = re.compile(r"target\s+near\s+(" + _NUMBER + r")")


def _check_fold_bucket_count(doc: Doc) -> list[dict]:
    """'Two of the four sit between twenty and a hundred-fold below the target'
    -- the densities and the target are both printed, so the count is derived."""
    out = []
    work = doc.work
    for m in _BUCKET.finditer(work):
        count = word_number(m.group("count"))
        total = word_number(m.group("total"))
        lo = word_number(m.group("lo"))
        hi = word_number(m.group("hi"))
        if None in (count, total, lo, hi):
            continue
        back = work[max(0, m.start() - 1200):m.start()]
        dm = None
        for dm in _DENSITY_LIST.finditer(back):
            pass
        tm = None
        for tm in _TARGET_VALUE.finditer(back):
            pass
        if dm is None or tm is None:
            continue
        target = parse_q(tm.group(1))
        vals = [parse_q(x) for x in _NUMBER_RE.findall(dm.group("list"))]
        vals = [v for v in vals if v is not None]
        if target is None or len(vals) != total:
            continue
        _tally('count of values inside a stated fold band (prose)')
        sure, possible = 0, 0
        ratios = []
        for v in vals:
            r_lo = target.lo / 10.0 ** v.hi
            r_hi = target.hi / 10.0 ** v.lo
            ratios.append(target.value / 10.0 ** v.value)
            if m.group("dir") == "above":
                r_lo, r_hi = 1.0 / r_hi, 1.0 / r_lo
            if r_lo >= lo and r_hi <= hi:
                sure += 1
            if _overlap(r_lo, r_hi, lo, hi):
                possible += 1
        if not (sure <= count <= possible):
            out.append(finding(
                "high", "fold-bucket-count", doc.where(m.start()),
                f"the {total} printed densities are "
                f"{', '.join(f'{r:.3g}' for r in ratios)}-fold "
                f"{m.group('dir')} the stated target of {target.text}, so "
                f"{sure} of them (at most {possible}) sit between {lo} and {hi}"
                f"-fold {m.group('dir')} it, not {count}.",
                expected=f"{sure} of {total}",
                found=f"{m.group('count')} of {m.group('total')}"))
    out += _check_fold_against_target(doc)
    return out


_AGAINST_TARGET = re.compile(
    r"(?P<count>[A-Za-z]+|\d+)\s+of\s+the\s+(?P<total>[A-Za-z]+|\d+)\s+sits?\s+"
    r"(?P<dir>below|above)\s+(?:the\s+)?(?P<what>[^.,;]{0,40}?target)\s*,?\s*"
    r"(?:by|at)\s+(?P<folds>[\d.,\s-]*?(?:and\s+)?[\d.]+)\s*-\s*fold"
)
_OTHER_ONE = re.compile(
    r"the\s+(?:fourth|third|second|other|remaining|last)\s+sits?\s+"
    r"(?P<f>[A-Za-z\d.]+)-fold\s+(?P<dir>above|below)\s+it")


def _ratio_interval(target: Q, density: Q, direction: str) -> tuple[float, float]:
    """How far a printed log10 density sits below (or above) a printed target."""
    lo = target.lo / 10.0 ** density.hi
    hi = target.hi / 10.0 ** density.lo
    if direction == "above":
        lo, hi = 1.0 / hi, 1.0 / lo
    return lo, hi


def _target_and_densities(work: str, pos: int):
    back = work[max(0, pos - 1400):pos]
    dm = tm = None
    for dm in _DENSITY_LIST.finditer(back):
        pass
    for tm in _TARGET_VALUE.finditer(back):
        pass
    if dm is None or tm is None:
        return None, []
    target = parse_q(tm.group(1))
    vals = [parse_q(x) for x in _NUMBER_RE.findall(dm.group("list"))]
    return target, [v for v in vals if v is not None]


def _check_fold_against_target(doc: Doc) -> list[dict]:
    """'Three of the four sit below the CLSI target, by 11-, 12- and 107-fold'
    -- each quoted fold is the printed target over a printed density."""
    out = []
    work = doc.work
    for m in _AGAINST_TARGET.finditer(work):
        count = word_number(m.group("count"))
        total = word_number(m.group("total"))
        target, vals = _target_and_densities(work, m.start())
        if count is None or total is None or target is None:
            continue
        if len(vals) != total:
            continue
        quoted = [parse_q(x) for x in re.findall(r"[\d.]+", m.group("folds"))]
        quoted = [x for x in quoted if x is not None]
        if not quoted:
            continue
        _tally("fold against a stated target (prose)", len(quoted))
        ivs = [_ratio_interval(target, v, m.group("dir")) for v in vals]
        on_this_side = [i for i, iv in enumerate(ivs) if iv[1] >= 1.0]
        unused = list(on_this_side)
        unmatched = []
        for qf in quoted:
            hit = None
            for i in unused:
                if _overlap(*ivs[i], qf.lo, qf.hi):
                    hit = i
                    break
            if hit is None:
                unmatched.append(qf)
            else:
                unused.remove(hit)
        shown = ", ".join(f"{target.value / 10.0 ** v.value:.3g}" for v in vals)
        if unmatched:
            out.append(finding(
                "high", "fold-against-target", doc.where(m.start()),
                f"{', '.join(x.text for x in unmatched)}-fold is not the "
                f"printed target {target.text} over any of the printed "
                f"densities, which give {shown}-fold.",
                expected=shown, found=m.group("folds")))
        if len(quoted) != count or count != len(on_this_side):
            out.append(finding(
                "high", "fold-against-target", doc.where(m.start()),
                f"{len(on_this_side)} of the {total} printed densities sit "
                f"{m.group('dir')} the stated target ({shown}-fold), and "
                f"{len(quoted)} fold figures are quoted, against the "
                f"'{m.group('count')} of the {m.group('total')}' claimed.",
                expected=f"{len(on_this_side)} of {total}",
                found=f"{m.group('count')} of {m.group('total')}"))

    for m in _OTHER_ONE.finditer(work):
        f = parse_q(m.group("f"))
        if f is None:
            w = word_number(m.group("f"))
            if w is None:
                continue
            f = Q(float(w), 0.0, m.group("f"))
        target, vals = _target_and_densities(work, m.start())
        if target is None or not vals:
            continue
        _tally("fold against a stated target (prose)")
        ivs = [_ratio_interval(target, v, m.group("dir")) for v in vals]
        if any(_overlap(*iv, f.lo, f.hi) for iv in ivs):
            continue
        out.append(finding(
            "high", "fold-against-target", doc.where(m.start()),
            f"{f.text}-fold {m.group('dir')} the printed target {target.text} "
            f"matches none of the printed densities, which sit "
            f"{', '.join(f'{iv[0]:.3g}' for iv in ivs)}-fold "
            f"{m.group('dir')} it.",
            expected="one of the printed densities", found=f"{f.text}-fold"))
    return out


# --------------------------------------------------------------------------
# (c) Benjamini-Hochberg critical values
# --------------------------------------------------------------------------

_FAMILY = re.compile(
    r"family of (?:the )?(?P<n>\d+|[a-z]+)|"
    r"(?:ranked )?against (?:the full family of )?(?P<n2>\d+)\b|"
    r"the (?P<n3>\d+) comparisons"
)


def _family_size(textblock: str) -> int | None:
    for m in _FAMILY.finditer(textblock):
        for g in ("n", "n2", "n3"):
            if m.group(g):
                v = word_number(m.group(g))
                if v and v > 1:
                    return v
    return None


def _last_family_size(textblock: str) -> int | None:
    """The family size stated closest before the quantity being checked."""
    got = None
    for m in _FAMILY.finditer(textblock):
        for g in ("n", "n2", "n3"):
            if m.group(g):
                v = word_number(m.group(g))
                if v and v > 1:
                    got = v
    return got


_PROSE_CRIT = re.compile(
    r"(?:critical value|corrected threshold|threshold)\s+"
    r"(?:of|is|was|would be)\s+(?P<v>\d*\.\d+)")


def _fdr(doc: Doc) -> float:
    m = re.search(r"false discovery rate of (\d+(?:\.\d+)?)\s*(?:per cent|%)",
                  doc.work)
    if m:
        return float(m.group(1)) / 100.0
    return 0.05


def check_bh(doc: Doc) -> list[dict]:
    out: list[dict] = []
    q = _fdr(doc)

    # --- tables carrying a printed critical value ------------------------
    for tbl in doc.tables:
        ci = tbl.header_index("bh critical", "critical value")
        if ci is None:
            continue
        pi = tbl.header_index("| p |")
        if pi is None:
            for i, h in enumerate(tbl.headers):
                if h.strip().lower() == "p":
                    pi = i
                    break
        m = _family_size(tbl.legend)
        if pi is None or m is None:
            continue
        rows = []
        for ri, row in enumerate(tbl.rows):
            p = cell_scalar(row[pi]) if pi < len(row) else None
            c = cell_scalar(row[ci]) if ci < len(row) else None
            if p is not None and c is not None:
                rows.append((p.value, ri, p, c))
        rows.sort()
        for rank, (_, ri, p, c) in enumerate(rows, start=1):
            expected = q * rank / m
            _tally('BH critical value (tables)')
            sev = _grade(c, expected, expected)
            lbl = " / ".join(x for x in tbl.rows[ri][:2] if x)
            if sev:
                out.append(finding(
                    sev, "bh-critical-value",
                    f"{tbl.label or 'table'}, row '{lbl}' "
                    f"(line {tbl.row_lines[ri]})",
                    f"rank {rank} in a family of {m} at a false discovery rate "
                    f"of {q:g} has critical value {expected:.5g}, not the "
                    f"{c.text} printed.",
                    expected=f"{expected:.5g}", found=c.text))
            # the survival flag must agree with its own printed threshold
            si = tbl.header_index("survives")
            if si is not None and si < len(tbl.rows[ri]):
                flag = tbl.rows[ri][si].strip().lower()
                if flag in ("yes", "no"):
                    _tally('BH decision against a printed threshold (tables)')
                    should = "yes" if p.value <= c.value else "no"
                    if flag != should:
                        out.append(finding(
                            "high", "bh-decision",
                            f"{tbl.label or 'table'}, row '{lbl}' "
                            f"(line {tbl.row_lines[ri]})",
                            f"p = {p.text} against its printed critical value "
                            f"{c.text} implies '{should}', but the table says "
                            f"'{flag}'.",
                            expected=should, found=flag))

    # --- prose: 'second in the family of eight ... 0.0125' ----------------
    for m in _PROSE_CRIT.finditer(doc.work):
        v = parse_q(m.group("v"))
        back = doc.work[max(0, m.start() - 320):m.start()]
        fam = _last_family_size(back)
        if v is None or fam is None:
            continue
        _tally("BH critical value (prose)")
        rank = None
        for om in re.finditer(r"(" + "|".join(_ORDINALS) + r") in the family",
                              back):
            rank = _ORDINALS[om.group(1)]
        if rank is not None:
            expected = q * rank / fam
            if _grade(v, expected, expected) is None:
                continue
            out.append(finding(
                "high", "bh-critical-value", doc.where(m.start()),
                f"rank {rank} in a family of {fam} at a false discovery rate "
                f"of {q:g} has critical value {expected:.5g}, not the {v.text} "
                f"quoted.", expected=f"{expected:.5g}", found=v.text))
            continue
        if any(_grade(v, q * k / fam, q * k / fam) is None
               for k in range(1, fam + 1)):
            continue
        out.append(finding(
            "high", "bh-critical-value", doc.where(m.start()),
            f"a threshold of {v.text} is not {q:g} * rank / {fam} for any rank "
            f"in the family of {fam} it is quoted against.",
            expected=f"{q:g}*k/{fam}", found=v.text))

    # --- prose: 'N reach nominal significance where X are expected' -------
    for m in re.finditer(
            r"where\s+(?P<exp>\d+(?:\.\d+)?)\s+(?:are|is)\s+expected by chance",
            doc.work):
        printed = parse_q(m.group("exp"))
        block = doc.work[max(0, m.start() - 400):m.start()]
        fam = _family_size(block)
        if printed is None or fam is None:
            continue
        expected = 0.05 * fam
        _tally('hits expected by chance (prose)')
        sev = _grade(printed, expected, expected)
        if sev:
            out.append(finding(
                sev, "expected-by-chance", doc.where(m.start()),
                f"a family of {fam} at a nominal 0.05 expects "
                f"{expected:.4g} hits by chance, not {printed.text}.",
                expected=f"{expected:.4g}", found=printed.text))

    out += _check_bh_step_up(doc, q)
    return out


def _check_bh_step_up(doc: Doc, q: float) -> list[dict]:
    """Where a table prints the whole family and a survives-correction column,
    recompute the Benjamini-Hochberg decisions."""
    out = []
    for tbl in doc.tables:
        if tbl.header_index("bh critical", "critical value") is not None:
            continue      # already checked row by row against its own threshold
        p_cols = [i for i, h in enumerate(tbl.headers)
                  if h.strip().lower() == "p" or h.strip().lower().startswith("p (")]
        s_cols = [i for i, h in enumerate(tbl.headers)
                  if "survives" in h.lower()]
        if not p_cols or not s_cols or len(p_cols) != len(s_cols):
            continue
        fam = _family_size(tbl.legend) or len(tbl.rows)
        if fam != len(tbl.rows):
            continue      # the table is not the whole family; cannot step up
        for pi, si in zip(p_cols, s_cols):
            vals = []
            for ri, row in enumerate(tbl.rows):
                p = cell_scalar(row[pi]) if pi < len(row) else None
                flag = row[si].strip().lower() if si < len(row) else ""
                if p is None or flag not in ("yes", "no"):
                    break
                vals.append((p.value, ri, flag, p))
            if len(vals) != len(tbl.rows):
                continue
            order = sorted(vals)
            kmax = 0
            for rank, (pv, _, _, _) in enumerate(order, start=1):
                if pv <= q * rank / fam:
                    kmax = rank
            rejected = {order[i][1] for i in range(kmax)}
            _tally('BH step-up decision (tables)', len(vals))
            for pv, ri, flag, p in vals:
                should = "yes" if ri in rejected else "no"
                if flag != should:
                    lbl = " / ".join(x for x in tbl.rows[ri][:2] if x)
                    out.append(finding(
                        "high", "bh-decision",
                        f"{tbl.label or 'table'}, row '{lbl}' "
                        f"(line {tbl.row_lines[ri]})",
                        f"Benjamini-Hochberg at {q:g} over the printed family "
                        f"of {fam} rejects {kmax} test(s); p = {p.text} should "
                        f"read '{should}', not '{flag}'.",
                        expected=should, found=flag))
            # the legend's own count of survivors
            lm = re.search(r"(\d+|[a-z]+) survives?\b", tbl.legend)
            if lm:
                stated = word_number(lm.group(1))
                got = sum(1 for _, _, f, _ in vals if f == "yes")
                _tally('survivor count in a legend (tables)')
                if stated is not None and stated != got:
                    out.append(finding(
                        "medium", "survivor-count",
                        f"{tbl.label or 'table'} legend (line {tbl.line})",
                        f"the legend says {stated} survive, but the table marks "
                        f"{got} rows as surviving.",
                        expected=str(got), found=str(stated)))
    return out


# --------------------------------------------------------------------------
# (d) ranges and spans
# --------------------------------------------------------------------------

_SPAN_CLAIM = re.compile(
    r"(?:both\s+spans?\s+are\s+the\s+same|spans?\s+(?:are|is)\s+the\s+same|"
    r"a\s+span\s+of)\s+(?P<span>[\d.]+)\s*log10"
)
_RANGE = re.compile(r"(?P<a>" + _NUMBER + r")\s+to\s+(?P<b>" + _NUMBER + r")")


def check_spans(doc: Doc) -> list[dict]:
    out: list[dict] = []
    work = doc.work
    for m in _SPAN_CLAIM.finditer(work):
        span = parse_q(m.group("span"))
        if span is None:
            continue
        start = _sentence_start(work, m.start(), 400, _HARD_STOP)
        sent = work[start:m.end() + 120]
        cut = re.search(r"(?<=[.])\s+(?=[A-Z])", sent[m.end() - start:])
        if cut:
            sent = sent[:m.end() - start + cut.start()]
        all_of = "both" in m.group(0) or "the same" in m.group(0)
        ranges = []
        for rm in _RANGE.finditer(sent):
            a = parse_q(rm.group("a"))
            b = parse_q(rm.group("b"))
            if a and b and b.value > a.value:
                ranges.append((a, b, rm.group(0)))
        if not ranges:
            continue
        results = []
        _tally('range against its stated span (prose)', len(ranges))
        for a, b, txt in ranges:
            ok = False
            diff = _iv_sub(b, a)
            if _grade(span, diff[0], diff[1]) is None:
                ok = True
            r = _iv_div(b, a)
            if not ok and r is not None and r[0] > 0:
                lg = _iv_log10(*r)
                if lg and _grade(span, lg[0], lg[1]) is None:
                    ok = True
            results.append((ok, a, b, txt, diff))
        if all_of:
            bad = [r for r in results if not r[0]]
        else:
            bad = [] if any(r[0] for r in results) else results[:1]
        for _, a, b, txt, diff in bad:
            out.append(finding(
                "medium", "span", doc.where(m.start()),
                f"the range '{txt}' spans {b.value - a.value:.4g} "
                f"(or {math.log10(b.value / a.value):.4g} in log10 if the range "
                f"is a ratio), which cannot round to the {span.text} log10 span "
                f"stated with it.",
                expected=f"{_fmt(diff[0])}..{_fmt(diff[1])}", found=span.text))

    out += _check_max_minus_min(doc)
    return out


_MAXMIN = re.compile(r"maximum-minus-minimum")
_LABELLED_VALUE = re.compile(r"\b([A-Z])\s+at\s+(?:h\s*=\s*)?(\d+\.\d+)")
_DELTA_H = re.compile(r"(?:Δ|delta)\s*h\s*=\s*(\d+\.\d+)\s*log10")


def _check_max_minus_min(doc: Doc) -> list[dict]:
    """'Delta h = 2.33 log10 ... a maximum-minus-minimum over B at h = 2.67,
    C at 3.61, D at 3.65 and F at 5.00' -- the roster is printed, so the range
    it produces is derived."""
    out = []
    work = doc.work
    for m in _MAXMIN.finditer(work):
        sent_start = _sentence_start(work, m.start(), 300, _HARD_STOP)
        sent_end = _sentence_end(work, m.end(), 400)
        sent = work[sent_start:sent_end]
        vals = [parse_q(v) for _, v in _LABELLED_VALUE.findall(sent)]
        vals = [v for v in vals if v is not None]
        if len(vals) < 3:
            continue
        back = work[max(0, sent_start - 500):sent_start]
        dm = None
        for dm in _DELTA_H.finditer(back):
            pass
        if dm is None:
            continue
        stated = parse_q(dm.group(1))
        if stated is None:
            continue
        hi = max(vals, key=lambda v: v.value)
        lo = min(vals, key=lambda v: v.value)
        d = _iv_sub(hi, lo)
        _tally('max minus min over a printed roster (prose)')
        sev = _grade(stated, d[0], d[1])
        if sev:
            out.append(finding(
                sev, "max-minus-min", doc.where(m.start()),
                f"the roster runs {lo.text} to {hi.text}, a range of "
                f"{hi.value - lo.value:.4g}, against the {stated.text} log10 "
                f"stated for it.",
                expected=f"{_fmt(d[0])}..{_fmt(d[1])}", found=stated.text))
    return out


# --------------------------------------------------------------------------
# (d) log-reduction endpoints written as percentages
# --------------------------------------------------------------------------

_LOG_PCT = re.compile(
    r"(?P<q1>\d+)\s*log\s*\(\s*(?P<p1>\d+(?:\.\d+)?)\s*%\s*\)"
    r"|(?P<p2>\d+(?:\.\d+)?)\s*%\s*\(\s*(?P<q2>\d+)\s*log\s*\)"
)


def check_endpoint_depths(doc: Doc) -> list[dict]:
    out = []
    for m in _LOG_PCT.finditer(doc.work):
        if m.group("q1"):
            q_logs, pct_txt = int(m.group("q1")), m.group("p1")
        else:
            q_logs, pct_txt = int(m.group("q2")), m.group("p2")
        printed = parse_q(pct_txt)
        if printed is None:
            continue
        expected = 100.0 * (1.0 - 10.0 ** (-q_logs))
        _tally('log reduction written as a percentage')
        # this is an identity, not a measurement: 99.99 per cent is four logs
        # and 99.999 is five, and neither is a rounding of the other
        if abs(printed.value - expected) > 1e-9 * expected:
            out.append(finding(
                "high", "endpoint-depth", doc.where(m.start()),
                f"a {q_logs}-log reduction is {expected:.6g} per cent, not the "
                f"{pct_txt} per cent printed with it.",
                expected=f"{expected:.6g}%", found=f"{pct_txt}%"))
    return out


# --------------------------------------------------------------------------
# (d) equations written out in the text
# --------------------------------------------------------------------------

_EQ_MUL = re.compile(
    r"(?P<a>" + _NUMBER + r")\s*[x*]\s*10\^(?P<k>[+-]?\d+)\s*=\s*"
    r"(?P<b>" + _NUMBER + r")")
_EQ_DIV = re.compile(
    r"(?P<a>" + _NUMBER + r")\s*/\s*10\^(?P<k>[+-]?\d+)\s*=\s*"
    r"(?P<b>" + _NUMBER + r")")


def check_stated_equations(doc: Doc) -> list[dict]:
    out = []
    for rx, op in ((_EQ_MUL, "*"), (_EQ_DIV, "/")):
        for m in rx.finditer(doc.work):
            a = parse_q(m.group("a"))
            b = parse_q(m.group("b"))
            if not (a and b):
                continue
            k = int(m.group("k"))
            factor = 10.0 ** k
            _tally('equation written out in the text')
            lo, hi = (a.lo * factor, a.hi * factor) if op == "*" \
                else (a.lo / factor, a.hi / factor)
            sev = _grade(b, min(lo, hi), max(lo, hi))
            if sev:
                out.append(finding(
                    sev, "stated-equation", doc.where(m.start()),
                    f"the equation printed as '{m.group(0)}' does not hold: the "
                    f"left-hand side is {(a.value * factor) if op == '*' else (a.value / factor):.6g}.",
                    expected=_fmt((a.value * factor) if op == "*"
                                  else (a.value / factor)),
                    found=b.text))
    return out


# --------------------------------------------------------------------------
# (e) intervals must bracket their point estimate
# --------------------------------------------------------------------------

_MARKER = (r"(?:odds ratio|OR|hazard ratio|HR|relative risk ratio|"
           r"rho|ρ|AUC|concordance)")
_EST_1 = re.compile(
    _MARKER + r"\b[^0-9(\n]{0,32}?(?P<pt>[+-]?\d+(?:\.\d+)?)\s*"
    r"(?:,|\()\s*(?:[a-z ]{0,28}?(?:CI|interval)\s+)?"
    r"(?P<lo>[+-]?\d+(?:\.\d+)?)\s+to\s+(?P<hi>[+-]?\d+(?:\.\d+)?)")
_EST_2 = re.compile(
    r"(?P<pt>[+-]?\d+(?:\.\d+)?)\s*\(\s*(?P<lo>[+-]?\d+(?:\.\d+)?)\s+to\s+"
    r"(?P<hi>[+-]?\d+(?:\.\d+)?)\s*[,)]")
_EST_3 = re.compile(
    r"\(\s*(?P<pt>[+-]?\d+(?:\.\d+)?)\s*,\s*(?P<lo>[+-]?\d+(?:\.\d+)?)\s+to\s+"
    r"(?P<hi>[+-]?\d+(?:\.\d+)?)\s*\)")
_EST_4 = re.compile(
    r"\(\s*(?:[a-z-]+[\s\n]+){0,3}95 per cent (?:CI|interval)\s+"
    r"(?P<lo>[+-]?\d+(?:\.\d+)?)\s+to\s+(?P<hi>[+-]?\d+(?:\.\d+)?)")
# "OR 1.096 per day of time to OD 0.4, 95 per cent CI 1.032 to 1.164": the
# estimate is pinned by its own marker, and the interval is introduced by an
# explicit cue, so the prose between them may carry numbers of its own.
_EST_5 = re.compile(
    _MARKER + r"\b[^0-9(\n]{0,32}?(?P<pt>[+-]?\d+(?:\.\d+)?)"
    r"(?P<gap>[^\n]{0,70}?),\s*(?:[a-z-]+\s+){0,2}95 per cent (?:CI|interval)\s+"
    r"(?P<lo>[+-]?\d+(?:\.\d+)?)\s+to\s+(?P<hi>[+-]?\d+(?:\.\d+)?)")

_NOT_A_POINT = re.compile(
    r"\b(?:day|days|Table|Section|Fig|Figure|panel|rank|volume|"
    r"institutes?|visit|visits|month|months|percentile)\b", re.I)


def _decimals(text: str) -> int:
    t = text.strip()
    return len(t.split(".", 1)[1]) if "." in t else 0


def _point_before(work: str, pos: int, back: int = 130, max_skips: int = 4,
                  want_decimals: int = 0) -> Q | None:
    """The point estimate an interval ending at ``pos`` belongs to.

    Walking backwards and taking the first number is not enough: the clause
    that introduces an estimate often names a day range or a scale first --
    "+0.059 log10 per day per doubling over days 0 to 3 (95 per cent interval
    ...)" -- so a candidate is refused, and the walk continues, when it is
    glued to letters (the 10 of log10), when it is an index rather than a
    measurement, or when it is the 95 of "95 per cent".

    A candidate printed to fewer decimals than the interval it would have to
    sit inside is refused the same way, because an estimate and its interval
    are printed at one precision: "a mediated effect of +0.166 classes on the
    203 usable rows (95 per cent CI +0.067 to +0.279)" passes over 203 and
    nominates +0.166.  The walk never crosses a sentence boundary and never
    passes more than ``max_skips`` refusals, because a number from the wrong
    clause is worse than no check at all.
    """
    lo_bound = max(0, pos - back)
    before = work[lo_bound:pos]
    stop = 0
    for sm in _HARD_STOP.finditer(before):
        stop = sm.end()
    before = before[stop:]
    skips = 0
    for m in reversed(list(_NUMBER_RE.finditer(before))):
        prev_ch = before[m.start() - 1] if m.start() > 0 else " "
        nxt = before[m.end():m.end() + 9]
        bad = (
            prev_ch.isalnum() or prev_ch in "._^"
            or re.match(r"^[A-Za-z]", nxt)
            or re.match(r"^\s*per cent", nxt)
            or _NOT_A_POINT.search(before[max(0, m.start() - 30):m.start()])
        )
        if bad:
            skips += 1
            if skips > max_skips:
                return None
            continue
        if want_decimals and _decimals(m.group(0)) < min(want_decimals, 1):
            # a whole number where the interval carries decimals is a count
            # in the same clause ("on the 203 usable rows"), not the estimate
            skips += 1
            if skips > max_skips:
                return None
            continue
        return parse_q(m.group(0))
    return None


def check_intervals(doc: Doc) -> list[dict]:
    out: list[dict] = []
    work = doc.work
    seen = set()

    def record(pt: Q, lo: Q, hi: Q, pos: int, how: str):
        if (pos, pt.text) in seen:
            return
        _tally('interval brackets its estimate (prose)')
        if lo.value > hi.value:
            return
        if lo.lo - 1e-12 <= pt.value <= hi.hi + 1e-12:
            return
        seen.add((pos, pt.text))
        out.append(finding(
            "high", "interval-brackets", doc.where(pos),
            f"the interval {lo.text} to {hi.text} does not contain the point "
            f"estimate {pt.text} it is quoted for ({how}).",
            expected=f"{lo.text} <= {pt.text} <= {hi.text}",
            found=f"{pt.text} ({lo.text} to {hi.text})"))

    for rx, how in ((_EST_1, "prose, marker-led"),
                    (_EST_5, "prose, marker-led across a clause"),
                    (_EST_2, "prose, point then interval"),
                    (_EST_3, "prose, point inside the bracket")):
        for m in rx.finditer(work):
            pt = parse_q(m.group("pt"))
            lo = parse_q(m.group("lo"))
            hi = parse_q(m.group("hi"))
            if not (pt and lo and hi):
                continue
            if rx is _EST_2:
                before = work[max(0, m.start() - 30):m.start("pt")]
                if _NOT_A_POINT.search(before):
                    # the number against the bracket is a day or a rank, not
                    # an estimate; the estimate is further back in the clause
                    pt2 = _point_before(
                        work, m.start("pt"), 70, 3,
                        max(_decimals(m.group("lo")), _decimals(m.group("hi"))))
                    if pt2 is None:
                        continue
                    record(pt2, lo, hi, m.start(), how + ", index skipped")
                    continue
            record(pt, lo, hi, m.start(), how)

    for m in _EST_4.finditer(work):
        lo = parse_q(m.group("lo"))
        hi = parse_q(m.group("hi"))
        if not (lo and hi):
            continue
        pt = _point_before(
            work, m.start(), 130, 4,
            max(_decimals(m.group("lo")), _decimals(m.group("hi"))))
        if pt is None:
            continue
        record(pt, lo, hi, m.start(), "prose, CI in parentheses")

    out += _check_table_intervals(doc)
    return out


_CELL_EST = re.compile(
    r"^(?P<pt>[+-]?[\d.]+)\s*%?\s*\(\s*(?P<lo>[+-]?[\d.]+)\s*(?:to|,|-)\s*"
    r"(?P<hi>[+-]?[\d.]+)\s*\)\s*%?$")
# a cell that states its estimate in words before bracketing the interval:
# "36.6% of 191 cross-laboratory pairs are inversions (95% CI 30.1-43.6)"
_CELL_CI = re.compile(
    r"\(\s*(?:[a-z-]+\s+){0,3}95\s*(?:%|per cent)\s*(?:CI|interval)\s+"
    r"(?P<lo>[+-]?\d+(?:\.\d+)?)\s*(?:to|-|,)\s*(?P<hi>[+-]?\d+(?:\.\d+)?)")


def _check_table_intervals(doc: Doc) -> list[dict]:
    out = []
    for tbl in doc.tables:
        for ri, row in enumerate(tbl.rows):
            for ci, cell in enumerate(row):
                cm = _CELL_CI.search(cell)
                if cm:
                    lo = parse_q(cm.group("lo"))
                    hi = parse_q(cm.group("hi"))
                    pt = _point_before(
                        cell, cm.start(), 200, 4,
                        max(_decimals(cm.group("lo")),
                            _decimals(cm.group("hi"))))
                    if pt and lo and hi and lo.value <= hi.value:
                        _tally('interval brackets its estimate (table cell)')
                        if not (lo.lo - 1e-12 <= pt.value <= hi.hi + 1e-12):
                            out.append(finding(
                                "high", "interval-brackets",
                                f"{tbl.label or 'table'}, row "
                                f"'{row[0]}' (line {tbl.row_lines[ri]})",
                                f"column '{tbl.headers[ci]}' quotes an "
                                f"interval of {lo.text} to {hi.text} for a "
                                f"stated {pt.text}, which it does not "
                                f"contain.",
                                expected=f"{lo.text} <= {pt.text} <= {hi.text}",
                                found=cell.strip()[:90]))
                m = _CELL_EST.match(cell.strip())
                if m:
                    pt = parse_q(m.group("pt"))
                    lo = parse_q(m.group("lo"))
                    hi = parse_q(m.group("hi"))
                    if pt and lo and hi and lo.value <= hi.value:
                        _tally('interval brackets its estimate (table cell)')
                        if not (lo.lo - 1e-12 <= pt.value <= hi.hi + 1e-12):
                            out.append(finding(
                                "high", "interval-brackets",
                                f"{tbl.label or 'table'}, row "
                                f"'{row[0]}' (line {tbl.row_lines[ri]})",
                                f"column '{tbl.headers[ci]}' prints "
                                f"{cell.strip()}: the interval does not contain "
                                f"its own point estimate.",
                                expected=f"{lo.text} <= {pt.text} <= {hi.text}",
                                found=cell.strip()))
        # an interval column beside the estimate column it belongs to
        for ci, header in enumerate(tbl.headers):
            h = header.lower()
            if not any(k in h for k in ("interval", "ci", "support", "95%")):
                continue
            prev = None
            for cj in range(ci - 1, -1, -1):
                if any(cell_scalar(r[cj]) is not None
                       for r in tbl.rows if cj < len(r)):
                    prev = cj
                    break
            if prev is None:
                continue
            for ri, row in enumerate(tbl.rows):
                if ci >= len(row) or prev >= len(row):
                    continue
                iv = cell_interval(row[ci])
                pt = cell_scalar(row[prev])
                if not iv or pt is None:
                    continue
                _tally('interval brackets its estimate (adjacent columns)')
                lo, hi = iv
                if not (lo.lo - 1e-12 <= pt.value <= hi.hi + 1e-12):
                    out.append(finding(
                        "high", "interval-brackets",
                        f"{tbl.label or 'table'}, row '{row[0]}' "
                        f"(line {tbl.row_lines[ri]})",
                        f"'{tbl.headers[ci]}' is {row[ci]} but "
                        f"'{tbl.headers[prev]}' is {row[prev]}, which the "
                        f"interval does not contain.",
                        expected=f"{lo.text} <= {pt.text} <= {hi.text}",
                        found=f"{row[prev]} ({row[ci]})"))
    return out


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

_ORDER = {"high": 0, "medium": 1, "low": 2}


def check(text: str, ctx: dict) -> list[dict]:
    """Return a list of findings.  Empty list means clean."""
    STATS.clear()
    doc = Doc(text)
    findings: list[dict] = []
    findings += check_percentages(doc)
    findings += check_table_columns(doc)
    findings += check_partition_sums(doc)
    findings += check_exclusion_arithmetic(doc)
    findings += check_legend_tallies(doc)
    findings += check_folds(doc)
    findings += check_bh(doc)
    findings += check_spans(doc)
    findings += check_endpoint_depths(doc)
    findings += check_stated_equations(doc)
    findings += check_intervals(doc)

    # de-duplicate identical findings raised by two rules
    uniq, seen = [], set()
    for f in findings:
        key = (f["kind"], f["where"], f["detail"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(f)
    uniq.sort(key=lambda f: (_ORDER.get(f["severity"], 3), f["where"]))
    return uniq


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(argv[0]) if argv else Path(__file__).resolve().parents[2]
    paper = root / "manuscript" / "PAPER_COMPLETE.md"
    text = paper.read_text(encoding="utf-8")
    ctx = {
        "root": root,
        "tables": (root / "manuscript" / "tables.md").read_text(encoding="utf-8"),
        "prose": (root / "manuscript" / "RATE_VS_DURATION.md").read_text(
            encoding="utf-8"),
    }
    findings = check(text, ctx)
    print(f"check_arithmetic: {len(findings)} finding(s) in {paper}")
    print(f"  recomputed {sum(STATS.values())} derived quantities:")
    for key, n in sorted(STATS.items()):
        print(f"    {n:4d}  {key}")
    for f in findings:
        print()
        print(f"  [{f['severity']}] {f['kind']} -- {f['where']}")
        print(f"      {f['detail']}")
        if "expected" in f:
            print(f"      expected: {f['expected']}   found: {f['found']}")
    return 1 if any(f["severity"] == "high" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
