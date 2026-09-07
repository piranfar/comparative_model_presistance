"""
Are the numbers OUTSIDE table bodies checked at all?

Run:  python -m src.audit.check_coverage

src/audit_claims.py recomputes a pinned list of headline values from the
results tables. It reads nothing else. Every number the manuscript states in a
table legend, a figure legend, Box 1 or the Abstract is therefore unaudited --
which is exactly where a wrong number is hardest to see, because a legend sits
next to the table that contradicts it and the eye reads the table.

This module extracts every numeric claim from those four regions and asks a
deliberately blunt question of each one: does this value occur anywhere in the
generated material -- a results CSV, a receipt, or a table body? A value that
occurs nowhere was typed by hand and has never been checked against anything.

Two sharper checks ride along, because the blunt question cannot see them:

  * a legend number that is absent from its OWN table body while that body
    states a different total for the same thing (a legend that once said
    "the 174 baseline isolates" over a body that said 167);
  * a stated percentage that does not equal the count and denominator stated
    beside it, and Box 1 headroom against log10(N0/L);
  * a sentence that contradicts itself -- an "all N" restating neither of the
    two counts in front of it, or "Of T subjects, A ... and B ..." where A and
    B do not make T. These need no index, which matters, because the index is
    nearly powerless on small counts: every integer below 100 occurs somewhere
    in the results, so an existence test can never catch a real number quoted
    for the wrong quantity;
  * the coverage itself, against the inventory the paper's own front matter
    declares and the table blocks tables.md holds -- a sweep that scans three
    figure legends where the paper has four has failed at its own job, and
    would otherwise report that silently as a smaller total.

Conventions learned from the Methods, and deliberately NOT flagged: h is
dimensionless; a bare power of ten is a threshold or an endpoint definition,
not a measurement; 90 / 99 / 99.9 / 99.99 per cent are the endpoint constants;
95 per cent is a confidence level and 5 per cent a false discovery rate;
deposit identifiers, years, plated volumes and cross-references are not
data-derived. Numbers legitimately appear at different precision in an Abstract
than in a table, so a claim counts as traceable when it is a correct rounding
of a generated value.
"""
from __future__ import annotations

import bisect
import math
import re
from pathlib import Path

# --------------------------------------------------------------------------
# number scanning
# --------------------------------------------------------------------------

SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3",
       "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7",
       "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+"}

SUPCHARS = "".join(SUP)
_THIN = "   "

# order matters: the longest constructs first
TOKEN = re.compile(
    r"(?P<sci_sup>(?P<sci_m>\d+(?:\.\d+)?)\s*(?:×|x|\*)\s*10\s*"
    r"(?P<sci_e>[" + SUPCHARS + r"]+))"
    r"|(?P<sci_car>(?P<car_m>\d+(?:\.\d+)?)\s*(?:×|x|\*)\s*10\s*\^\s*"
    r"\{?(?P<car_e>[-−+]?\d+)\}?)"
    r"|(?P<pow_sup>10\s*(?P<pow_e>[" + SUPCHARS + r"]+))"
    r"|(?P<pow_car>10\s*\^\s*\{?(?P<pow_ce>[-−+]?\d+)\}?)"
    r"|(?P<enot>\d+(?:\.\d+)?[eE][-+]?\d+)"
    r"|(?P<grouped>\d{1,3}(?:[," + _THIN + r" ]\d{3})+(?:\.\d+)?)"
    r"|(?P<plain>\d+(?:\.\d+)?)"
)

KINDS = ("sci_sup", "sci_car", "pow_sup", "pow_car", "enot", "grouped", "plain")

CROSSREF = re.compile(
    r"(?:Tables?|Figs?\.?|Figures?|Sections?|Boxes?|Box|panels?|Panels?|"
    r"Supplementary\s+Tables?)\s+S?$")
DEPOSIT = re.compile(r"(figshare|zenodo|elife|nat\s+commun|doi|pmid|accession|"
                     r"biorxiv|medrxiv)", re.I)
# A culture-collection number is a name, not a quantity: "ATCC 25922" is the
# strain, and asking which results table 25922 came from is the wrong question.
# Anchored to the end of the preceding text on purpose. The deposit pattern
# above is allowed to match anywhere in the last 40 characters, which is right
# for "figshare 19766083" but wrong here -- searching that far back would also
# exempt the 3.93 in "in ATCC 25922 the depth was 3.93", and that number is a
# result and has to be traced like any other.
STRAIN = re.compile(r"\b(?:ATCC|NCTC|DSM|CIP|NCIMB|CCUG)\s*$", re.I)
VERSIONW = re.compile(r"(?:version|python|pandas|numpy|scipy|lifelines|"
                      r"statsmodels|\bv)\s*$", re.I)

ENDPOINT_CONSTANTS = {90.0, 99.0, 99.9, 99.99}


def _sup_to_int(s: str) -> int:
    return int("".join(SUP.get(c, c) for c in s))


class Claim:
    __slots__ = ("value", "raw", "dec", "region", "label", "line", "context",
                 "is_pct")

    def __init__(self, value, raw, dec, region, label, line, context, is_pct):
        self.value = value
        self.raw = raw
        self.dec = dec
        self.region = region
        self.label = label
        self.line = line
        self.context = context
        self.is_pct = is_pct

    def __repr__(self):
        return "Claim(%r=%r in %s)" % (self.raw, self.value, self.label)


def _decimals(raw: str) -> int:
    """Significant decimals as DISPLAYED, which sets the rounding tolerance."""
    m = re.search(r"\.(\d+)", raw)
    return len(m.group(1)) if m else 0


def scan_numbers(s: str):
    """Yield (value, raw, decimals, start, end) for every number in `s`."""
    for m in TOKEN.finditer(s):
        raw = m.group(0)
        try:
            if m.group("sci_sup"):
                v = float(m.group("sci_m")) * 10.0 ** _sup_to_int(m.group("sci_e"))
                dec = 12
            elif m.group("sci_car"):
                v = float(m.group("car_m")) * 10.0 ** int(
                    m.group("car_e").replace("−", "-"))
                dec = 12
            elif m.group("pow_sup"):
                v = 10.0 ** _sup_to_int(m.group("pow_e"))
                dec = 12
            elif m.group("pow_car"):
                v = 10.0 ** int(m.group("pow_ce").replace("−", "-"))
                dec = 12
            elif m.group("enot"):
                v = float(raw)
                dec = 12
            elif m.group("grouped"):
                v = float(re.sub(r"[,\s   ]", "", raw))
                dec = _decimals(raw)
            else:
                v = float(raw)
                dec = _decimals(raw)
        except (ValueError, OverflowError):
            continue
        if not math.isfinite(v):
            continue
        yield v, raw, dec, m.start(), m.end()


# --------------------------------------------------------------------------
# what a manuscript region is allowed to say without it being a data claim
# --------------------------------------------------------------------------

# "90, 99 or 99.99 per cent" -- the constant may sit anywhere in the list
PCT_LIST = re.compile(
    r"\s*(?:(?:,|or|and)\s+(?:an?\s+)?\d+(?:\.\d+)?\s*)*(?:%|per\s+cent)")


def _is_convention(v, raw, before, after, kind):
    """True when this number is not a data-derived quantity."""
    # bare powers of ten: class thresholds and endpoint definitions
    if kind in ("pow_sup", "pow_car"):
        return True
    # part of an identifier, not a number: log10, N0, H37Rv, MDK99, ERA4TB
    if before and before[-1].isalpha():
        return True
    # the base of a symbolic power: L * 10^q
    if after.startswith("^"):
        return True
    # cross-references
    if CROSSREF.search(before):
        return True
    # years
    if "." not in raw and re.fullmatch(r"\d{4}", raw.strip()) and 1900 <= v <= 2100:
        return True
    # deposit identifiers and accession numbers
    if DEPOSIT.search(before[-40:]):
        return True
    # a culture-collection number immediately after its collection's name
    if STRAIN.search(before):
        return True
    # software versions
    if re.fullmatch(r"\d+\.\d+\.\d+", raw) or VERSIONW.search(before):
        return True
    # the endpoint constants, alone or in a list
    pct_next = re.match(r"\s*(?:%|per\s+cent)", after)
    if v in ENDPOINT_CONSTANTS and PCT_LIST.match(after):
        return True
    # confidence level
    if v == 95 and pct_next and re.search(
            r"confidence|support|interval|profile|credible|\bCI\b|bootstrap",
            after[:70], re.I):
        return True
    # false discovery rate
    if v == 5 and pct_next and re.search(r"false\s+discovery\s+rate",
                                         before[-70:], re.I):
        return True
    # endpoint depth in "q-log" / "1 log" / "four-log": definitional.
    # A DISPLAYED decimal ("3.00 logs") is a computed headroom, not a depth.
    if ("." not in raw and re.match(r"\s*-?\s*log", after, re.I)
            and v in (1, 2, 3, 4, 5, 6)):
        return True
    return False


# --------------------------------------------------------------------------
# spelled-out counts: "Eighteen isolates", "Thirty-three of 217"
# --------------------------------------------------------------------------

ONES = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
        "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
        "seventy": 70, "eighty": 80, "ninety": 90}

WORDNUM_SRC = (r"(?:(?:" + "|".join(TENS) + r")(?:[-\s](?:"
               + "|".join(k for k in ONES if ONES[k] < 10) + r"))?"
               r"|" + "|".join(sorted(ONES, key=len, reverse=True)) + r")")
WORDNUM = re.compile(r"\b" + WORDNUM_SRC + r"\b", re.I)


def wordnum_value(s):
    parts = re.split(r"[-\s]+", s.strip().lower())
    total = 0
    for p in parts:
        if p in TENS:
            total += TENS[p]
        elif p in ONES:
            total += ONES[p]
        else:
            return None
    return float(total) if total else None


def word_claims(text, region, label, line0, minimum=3.0):
    """Counts written as words. `one` and `two` are almost always determiners
    in this prose, so the floor is three."""
    out = []
    for m in WORDNUM.finditer(text):
        v = wordnum_value(m.group(0))
        if v is None or v < minimum:
            continue
        before = text[max(0, m.start() - 70):m.start()]
        if before and before[-1].isalpha():
            continue
        line = line0 + text.count("\n", 0, m.start())
        ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 55):m.end() + 55]).strip()
        out.append(Claim(v, m.group(0), 0, region, label, line, ctx, False))
    return out


def region_claims(text, region, label, line0, stats=None):
    """Numeric claims in one region. `stats`, if given, receives the count of
    tokens skipped as conventions, so the summary can say what is NOT checked."""
    out = []
    skipped = 0
    for m in TOKEN.finditer(text):
        kind = next((k for k in KINDS if m.group(k)), "plain")
        raw = m.group(0)
        before = text[max(0, m.start() - 70):m.start()]
        after = text[m.end():m.end() + 70]
        vals = list(scan_numbers(raw))
        if not vals:
            continue
        v, _, dec, _, _ = vals[0]
        if _is_convention(v, raw, before, after, kind):
            skipped += 1
            continue
        line = line0 + text.count("\n", 0, m.start())
        ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 55):m.end() + 55]).strip()
        is_pct = bool(re.match(r"\s*(?:%|per\s+cent)", after))
        out.append(Claim(v, raw, dec, region, label, line, ctx, is_pct))
    out += word_claims(text, region, label, line0)
    out.sort(key=lambda c: (c.line, c.raw))
    if stats is not None:
        stats["skipped"] = stats.get("skipped", 0) + skipped
    return out


# --------------------------------------------------------------------------
# segmentation of PAPER_COMPLETE.md
# --------------------------------------------------------------------------

def _table_body_after(lines, i):
    """Rows of the pipe table that follows line i; [] if there is none."""
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j >= len(lines) or not lines[j].lstrip().startswith("|"):
        return []
    body = []
    while j < len(lines) and lines[j].lstrip().startswith("|"):
        body.append(lines[j])
        j += 1
    return body


def segment(text):
    """Table legends (with their bodies), figure legends, Box 1, Abstract."""
    lines = text.split("\n")
    regions = []

    for i, ln in enumerate(lines):
        m = re.match(r"\*\*Table\s+(S?\d+)\.\*\*\s*(.*)", ln)
        if not m:
            continue
        legend = [m.group(2)]
        j = i + 1
        while j < len(lines) and lines[j].strip() \
                and not lines[j].lstrip().startswith("|"):
            legend.append(lines[j])
            j += 1
        body = _table_body_after(lines, j - 1)
        regions.append({
            "region": "table legend",
            "label": "Table %s legend" % m.group(1),
            "line": i + 1,
            "text": "\n".join(legend),
            "body": "\n".join(body),
        })

    for i, ln in enumerate(lines):
        m = re.match(r"\*\*Figure\s+(\d+)\.", ln)
        if not m:
            continue
        block = [ln]
        j = i + 1
        while j < len(lines):
            s = lines[j]
            if re.match(r"\*\*Figure\s+\d+\.", s) or s.startswith("![") \
                    or s.startswith("---") or s.startswith("#"):
                break
            block.append(s)
            j += 1
        regions.append({
            "region": "figure legend",
            "label": "Figure %s legend" % m.group(1),
            "line": i + 1,
            "text": "\n".join(block),
            "body": "",
        })

    for i, ln in enumerate(lines):
        m = re.match(r"\*\*Box\s+(\d+)\.", ln)
        if not m:
            continue
        block, body = [], []
        j = i
        while j < len(lines):
            s = lines[j]
            if j > i and (s.startswith("---") or s.startswith("## ")):
                break
            (body if s.lstrip().startswith("|") else block).append(s)
            j += 1
        regions.append({
            "region": "box",
            "label": "Box %s" % m.group(1),
            "line": i + 1,
            "text": "\n".join(block),
            "body": "\n".join(body),
        })

    for i, ln in enumerate(lines):
        if ln.strip().lower() in ("## abstract", "# abstract"):
            block = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                block.append(lines[j])
                j += 1
            regions.append({
                "region": "abstract", "label": "Abstract", "line": i + 1,
                "text": "\n".join(block), "body": "",
            })
            break

    return regions


# --------------------------------------------------------------------------
# the index of generated values
# --------------------------------------------------------------------------

def _values_of(s):
    return [v for v, _, _, _, _ in scan_numbers(s)]


def build_index(root, manuscript_text, tables_md=""):
    """Every number the analysis produced, plus every table body."""
    results, bodies = [], []

    tdir = root / "results" / "tables"
    if tdir.is_dir():
        for p in sorted(tdir.glob("*.csv")):
            results += _values_of(p.read_text(encoding="utf-8", errors="replace"))
    rdir = root / "results" / "receipts"
    if rdir.is_dir():
        # exp*.json only: an audit's own receipt is not generated evidence, and
        # indexing it would let this script vouch for its own output
        for p in sorted(rdir.glob("exp*.json")):
            results += _values_of(p.read_text(encoding="utf-8", errors="replace"))

    for src in (manuscript_text, tables_md):
        for ln in src.split("\n"):
            if ln.lstrip().startswith("|"):
                bodies += _values_of(ln)

    results = sorted(set(results))
    bodies = sorted(set(bodies))
    return {"results": results, "bodies": bodies,
            "all": sorted(set(results) | set(bodies))}


def _hit(sorted_vals, target, tol):
    if not sorted_vals:
        return False
    i = bisect.bisect_left(sorted_vals, target - tol)
    return i < len(sorted_vals) and sorted_vals[i] <= target + tol


def traceable(claim, sorted_vals):
    """A claim is traceable when it is a correct rounding of a generated value.

    A percentage is also matched against the same share stored as a fraction,
    and a fraction below one against the same share stored as a percentage,
    because the tables carry shares both ways. Nothing else is rescaled.
    """
    scales = [1.0]
    if claim.is_pct:
        scales.append(0.01)
    if 0.0 < claim.value < 1.0:
        scales.append(100.0)
    for scale in scales:
        v = claim.value * scale
        dec = claim.dec + (2 if scale == 0.01 else 0)
        tol = max(0.5 * 10.0 ** (-min(dec, 12)), abs(v) * 5e-4)
        if _hit(sorted_vals, v, tol):
            return True
    return False


# --------------------------------------------------------------------------
# sharper checks
# --------------------------------------------------------------------------

COUNT_NOUN = (r"(?:isolates?|flasks?|series|readings?|pairs?|laboratories|"
              r"clones?|cultures?|calls?|rows?|comparisons?|tests?|deposits?|"
              r"counts?|samples?|conclusions?|members?|cells?)")

N_OF_M = re.compile(
    r"(?<![\d.])(?P<n>\d{1,4}|" + WORDNUM_SRC + r")\s+of\s+(?:the\s+)?"
    r"(?P<d>\d{1,4}|" + WORDNUM_SRC + r")\b"
    r"(?P<mid>[^.;()]{0,40}?)"
    r"(?<![\d.])(?P<p>\d{1,3}(?:\.\d+)?)\s*(?:%|per\s+cent)", re.I)

# "below the 99.99 per cent endpoint" names a threshold, not a share of the
# ratio in front of it; so does "at 95 per cent confidence". Both are refused
# by what FOLLOWS the percentage, which is precise. A comparative between the
# ratio and the percentage means the percentage belongs to a second subject.
# Nothing else is refused, so "56 of 360 series IN THE POOLED SET, 15.6 per
# cent" is still an apposition and is still checked.
MID_STOP = re.compile(r"\b(?:than|compared|versus|vs\.?|against|whereas|"
                      r"while|but)\b", re.I)
PCT_IS_THRESHOLD = re.compile(
    r"\s*(?:endpoint|threshold|reduction|confidence|interval|level|support|"
    r"critical|significance|cut|kill|point)\b", re.I)


def _num(tok):
    try:
        return float(tok)
    except ValueError:
        return wordnum_value(tok)


def check_stated_percentages(regions):
    """`N of M ... P per cent` where P is not 100 N / M."""
    out = []
    for r in regions:
        for m in N_OF_M.finditer(r["text"]):
            n, d = _num(m.group("n")), _num(m.group("d"))
            if n is None or d is None:
                continue
            p = float(m.group("p"))
            if d == 0 or n > d:
                continue
            # "below the 99.99 per cent endpoint" is an endpoint name, not a
            # share of the ratio in front of it
            if (p in ENDPOINT_CONSTANTS
                    or MID_STOP.search(m.group("mid"))
                    or PCT_IS_THRESHOLD.match(r["text"][m.end():m.end() + 30])):
                continue
            got = 100.0 * n / d
            praw = m.group("p")
            dec = len(praw.split(".")[1]) if "." in praw else 0
            tol = max(0.5 * 10.0 ** -dec, 0.05)
            if abs(got - p) > tol:
                out.append({
                    "severity": "high", "kind": "percentage-vs-count",
                    "where": "%s (line %d)" % (r["label"], r["line"]),
                    "detail": ("\"%s\" states %g per cent, but %g of %g is "
                               "%.3g per cent."
                               % (" ".join(m.group(0).split()), p, n, d, got)),
                    "expected": "%.4g per cent" % got,
                    "found": "%g per cent" % p,
                })
    return out


# "the 174 baseline isolates", "all 33 isolates": a denominator the legend
# asserts for the table it labels. A partitive -- "six strongest OF the 24
# comparisons" -- says the table is a subset and is excluded.
# re.I, because the same assertion at the start of a sentence -- "The 174
# baseline isolates ..." -- is the same defect as "of the 174 baseline
# isolates" in the middle of one, and \d{1,4} because a single-digit
# denominator ("the 6 laboratories") is a denominator too.
DENOM = re.compile(
    r"(?<!\bof )(?<!\bof the )(?:the|all|every|these|those)\s+"
    r"(?P<n>\d{1,4})\s+(?:[a-z-]+\s+){0,2}" + COUNT_NOUN, re.I)

COUNT_COL = re.compile(
    r"^\**(?:n|no\.?|count|isolates?|flasks?|series|rows?|calls?|pairs?|"
    r"cultures?|clones?|comparisons?|tests?|readings?|samples?)\**$", re.I)
TOTAL_ROW = re.compile(r"\b(all|total|overall|every)\b", re.I)


def _body_totals(body):
    """Numbers the table body itself offers as a total of its subjects:
    the cells of any count column, and any row labelled all/total/overall."""
    rows = [ln for ln in body.split("\n") if ln.lstrip().startswith("|")]
    if len(rows) < 3:
        return []
    header = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    cols = [i for i, c in enumerate(header) if COUNT_COL.match(c)]
    out = []
    for ln in rows[2:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        for i in cols:
            if i < len(cells):
                out += _values_of(cells[i])
        if cells and TOTAL_ROW.search(cells[0]):
            for c in cells[1:]:
                out += _values_of(c)
    return sorted(set(out))


def check_legend_against_own_body(regions, idx):
    """A legend denominator its own table body contradicts.

    Only denominators are examined, and only against the counts the body
    itself presents as totals, because a legend legitimately quotes many
    numbers that the body it labels does not carry.
    """
    out = []
    for r in regions:
        if r["region"] != "table legend" or not r["body"]:
            continue
        body_vals = sorted(set(_values_of(r["body"])))
        totals = _body_totals(r["body"])
        if not body_vals or not totals:
            continue
        n_rows = max(0, len(r["body"].split("\n")) - 2)
        for m in DENOM.finditer(r["text"]):
            v = float(m.group("n"))
            if _hit(body_vals, v, max(0.5, abs(v) * 5e-4)) or v == n_rows:
                continue
            rivals = [b for b in totals
                      if b > 1 and 0.5 <= b / v <= 2.0 and abs(b - v) > 0.5]
            if not rivals:
                continue
            rival = min(rivals, key=lambda b: abs(b - v))
            sev = "high" if not _hit(idx["results"], v, max(0.5, v * 5e-4)) \
                else "medium"
            out.append({
                "severity": sev, "kind": "legend-vs-own-body",
                "where": "%s (line %d)" % (r["label"], r["line"]),
                "detail": ("the legend says \"%s\" but no such count appears "
                           "in the table it labels, which gives %g for the "
                           "same quantity."
                           % (" ".join(m.group(0).split()), rival)),
                "expected": "a count the body carries, nearest is %g" % rival,
                "found": "%g" % v,
            })
    return out


# --------------------------------------------------------------------------
# a region that contradicts itself
# --------------------------------------------------------------------------
#
# The traceability sweep above asks only whether a value exists SOMEWHERE in
# the generated material. That question is nearly powerless on small counts --
# every integer below 100 occurs somewhere in the results -- so a legend that
# quotes a real number for the wrong quantity sails through it. The two rules
# below do not ask where a number came from. They ask whether the sentence
# holding it is consistent with itself, which needs no index at all.

# a decimal point is not a full stop: "99.99 per cent endpoint, and all 33"
_SENT = r"(?:[^.]|\.(?=\d))"

# "Thirty-three of 217 ... and all 33 are recorded as failing": the "all N"
# restates one of the two counts in front of it. It must be one of them.
RESTATED = re.compile(
    r"(?<![\d.])(?P<n>\d{1,4}|" + WORDNUM_SRC + r")\s+of\s+(?:the\s+)?"
    r"(?P<d>\d{1,4})\b(?P<mid>" + _SENT + r"{0,180}?)"
    r"\ball\s+(?P<k>\d{1,4})\b(?!\s*(?:of\b|per\s+cent|%))", re.I)


def check_restated_counts(regions):
    """An "all N" that restates neither the numerator nor the denominator it
    was written to restate."""
    out = []
    for r in regions:
        for m in RESTATED.finditer(r["text"]):
            n, d, k = _num(m.group("n")), float(m.group("d")), float(m.group("k"))
            if n is None or k in (n, d):
                continue
            out.append({
                "severity": "high", "kind": "restated-count",
                "where": "%s (line %d)" % (r["label"], r["line"]),
                "detail": ("\"%s\" says all %g, but the counts it restates are "
                           "%g and %g."
                           % (" ".join(m.group(0).split()), k, n, d)),
                "expected": "all %g" % n, "found": "all %g" % k,
            })
    return out


# "Of eighteen isolates whose reading was censored, twelve admit one
# compatible class and six admit two": the parts must make the whole.
PARTITION = re.compile(
    r"(?:^|(?<=[.!?])\s|\n)Of\s+(?P<t>" + WORDNUM_SRC + r"|\d{1,4})\s+"
    r"(?P<noun>[a-z]{3,})\b(?P<mid>" + _SENT + r"{0,120}?),\s*"
    r"(?P<a>" + WORDNUM_SRC + r"|\d{1,4})\s+(?P<m2>" + _SENT + r"{0,80}?)"
    r"\band\s+(?P<b>" + WORDNUM_SRC + r"|\d{1,4})\b")


def check_partitions(regions):
    """"Of T subjects, A do this and B do that" where A + B is not T."""
    out = []
    for r in regions:
        for m in PARTITION.finditer(r["text"]):
            t, a, b = (_num(m.group(g)) for g in ("t", "a", "b"))
            if None in (t, a, b) or min(t, a, b) <= 0:
                continue
            if a >= t or b >= t:            # not a partition of t at all
                continue
            if abs((a + b) - t) < 1e-9:
                continue
            out.append({
                "severity": "high", "kind": "partition-total",
                "where": "%s (line %d)" % (r["label"], r["line"]),
                "detail": ("\"%s\" splits %g %s into %g and %g, which make %g."
                           % (" ".join(m.group(0).split()), t, m.group("noun"),
                              a, b, a + b)),
                "expected": "parts summing to %g" % t, "found": "%g" % (a + b),
            })
    return out


def _endpoint_depth(pct):
    """90 per cent -> 1 log, 99 -> 2, 99.9 -> 3, 99.99 -> 4."""
    if not 0 < pct < 100:
        return None
    return -math.log10(1.0 - pct / 100.0)


def check_box_arithmetic(regions):
    """Box 1 states the rules the whole paper rests on. Check the box against
    its own rules: h = log10(N0/L); a q-log endpoint is legal only where
    h >= q; a reading at L records the fraction L/N0."""
    out = []
    for r in regions:
        if r["region"] != "box" or not r["body"]:
            continue
        rows = [ln for ln in r["body"].split("\n") if ln.lstrip().startswith("|")]
        if len(rows) < 3:
            continue
        header = [c.strip().lower() for c in rows[0].strip().strip("|").split("|")]

        def col(pred):
            return next((i for i, c in enumerate(header) if pred(c)), None)

        i_n0 = col(lambda c: "n₀" in c or "n0" in c)
        i_l = col(lambda c: re.fullmatch(r"\**\*?l\*?\**(\s*\(.*\))?", c))
        i_h = col(lambda c: "headroom" in c)
        i_leg = col(lambda c: "legal" in c and "endpoint" in c)
        i_frac = col(lambda c: "last reading" in c)
        if None in (i_n0, i_l, i_h):
            continue

        for ln in rows[2:]:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if max(i_n0, i_l, i_h) >= len(cells):
                continue
            got = [_values_of(cells[i]) for i in (i_n0, i_l, i_h)]
            if not all(got):
                continue
            n0, L, h = got[0][0], got[1][0], got[2][0]
            if n0 <= 0 or L <= 0:
                continue
            where = "%s (line %d), row \"%s\"" % (r["label"], r["line"], cells[0])

            want = math.log10(n0 / L)
            if abs(want - h) > 0.005:
                out.append({
                    "severity": "high", "kind": "box-headroom-arithmetic",
                    "where": where,
                    "detail": ("Box 1 defines h = log10(N0/L); log10(%g/%g) is "
                               "%.3f, the row states %g." % (n0, L, want, h)),
                    "expected": "%.2f" % want, "found": "%g" % h,
                })

            # a q-log endpoint is legal only where h >= q
            if i_leg is not None and i_leg < len(cells):
                legal, refused = _split_legal(cells[i_leg])
                qs = [q for q in map(_endpoint_depth, legal) if q is not None]
                deepest = max(qs) if qs else None
                if deepest is not None and deepest > h + 1e-6:
                    out.append({
                        "severity": "high", "kind": "box-endpoint-rule",
                        "where": where,
                        "detail": ("the row allows a %.4g-log endpoint on "
                                   "headroom %g, but Box 1 makes a q-log "
                                   "endpoint legal only where h >= q."
                                   % (deepest, h)),
                        "expected": "no endpoint deeper than %g logs" % h,
                        "found": "%.4g logs" % deepest,
                    })
                rq = [q for q in map(_endpoint_depth, refused) if q is not None]
                shallowest = min(rq) if rq else None
                if shallowest is not None and shallowest <= h + 1e-6:
                    out.append({
                        "severity": "high", "kind": "box-endpoint-rule",
                        "where": where,
                        "detail": ("the row refuses a %.4g-log endpoint that "
                                   "headroom %g reaches." % (shallowest, h)),
                        "expected": "refuse only endpoints deeper than %g" % h,
                        "found": "%.4g logs refused" % shallowest,
                    })

            # a reading at L records the fraction L/N0
            if i_frac is not None and i_frac < len(cells):
                m = re.search(r"[Ff]raction\s+(\S+)", cells[i_frac])
                if m:
                    vs = _values_of(m.group(1))
                    if vs and 0 < vs[0] < 1:
                        want_f = L / n0
                        if abs(math.log10(vs[0]) - math.log10(want_f)) > 0.05:
                            out.append({
                                "severity": "high",
                                "kind": "box-recorded-fraction",
                                "where": where,
                                "detail": ("a reading at L records L/N0 = %.3g; "
                                           "the row states %.3g."
                                           % (want_f, vs[0])),
                                "expected": "%.3g" % want_f,
                                "found": "%.3g" % vs[0],
                            })
    return out


def _split_legal(cell):
    """Endpoints a Box 1 row allows, and endpoints it refuses."""
    legal, refused = [], []
    # split on the semicolon only: "99.9%" carries a decimal point
    for part in cell.split(";"):
        target = refused if re.search(r"\bnot\b", part, re.I) else legal
        target += [v for v, _, _, _, _ in scan_numbers(part)
                   if 0 < v < 100 and re.search(r"%|per\s+cent", part)]
        # "not a 5-log call": a depth written in logs
        for m in re.finditer(r"(\d+(?:\.\d+)?)\s*-?\s*log", part, re.I):
            q = float(m.group(1))
            target.append(100.0 * (1.0 - 10.0 ** -q))
    return legal, refused


# --------------------------------------------------------------------------
# is the coverage itself complete?
# --------------------------------------------------------------------------
#
# A coverage sweep that silently scans three figure legends where the paper
# has four has failed at its own job: the region it never saw is the one
# nobody checked. The paper states its own inventory in its front matter, and
# tables.md states which table blocks exist, so both are checkable.

INVENTORY = re.compile(
    r"\*\*Figures:\*\*\s*(?P<fig>\d+)\s*\|\s*\*\*Tables:\*\*\s*(?P<tab>\d+)"
    r"\s*\|\s*\*\*Boxes:\*\*\s*(?P<box>\d+)"
    r"(?:\s*\|\s*\*\*Supplementary\s+tables:\*\*\s*(?P<supp>\d+))?", re.I)


def check_inventory(text, regions, tables_md):
    """The regions actually segmented, against the inventory the paper
    declares and the table blocks tables.md holds."""
    out = []
    labels = [r["label"].split()[1] for r in regions
              if r["region"] == "table legend"]
    got = {
        "figure legends": sum(1 for r in regions if r["region"] == "figure legend"),
        "boxes": sum(1 for r in regions if r["region"] == "box"),
        "main tables": sum(1 for n in labels if not n.upper().startswith("S")),
        "supplementary tables": sum(1 for n in labels if n.upper().startswith("S")),
    }

    m = INVENTORY.search(text)
    if m:
        want = {"figure legends": int(m.group("fig")),
                "main tables": int(m.group("tab")),
                "boxes": int(m.group("box"))}
        if m.group("supp"):
            want["supplementary tables"] = int(m.group("supp"))
        for what, n in sorted(want.items()):
            # a document that carries no table block at all is not the
            # assembled paper -- RATE_VS_DURATION.md is the prose, and its
            # tables are spliced in only at assembly. Do not accuse it of
            # losing sixteen tables it never held.
            if not labels and "tables" in what:
                continue
            if got[what] != n:
                out.append({
                    "severity": "high", "kind": "coverage-incomplete",
                    "where": "front matter vs the assembled paper",
                    "detail": ("the paper declares %d %s but %d were found and "
                               "scanned, so %d region(s) went unread."
                               % (n, what, got[what], abs(n - got[what]))),
                    "expected": "%d %s" % (n, what),
                    "found": "%d" % got[what],
                })

    if tables_md.strip() and labels:
        gen = set(r["label"].split()[1] for r in segment(tables_md)
                  if r["region"] == "table legend")
        pap = set(labels)
        for num in sorted(gen - pap):
            out.append({
                "severity": "high", "kind": "coverage-incomplete",
                "where": "Table %s" % num,
                "detail": ("build_tables.py generated Table %s into tables.md "
                           "but the assembled paper carries no such table, so "
                           "nothing about it is checked." % num),
                "expected": "Table %s spliced into the paper" % num,
                "found": "absent",
            })
        for num in sorted(pap - gen):
            out.append({
                "severity": "high", "kind": "coverage-incomplete",
                "where": "Table %s" % num,
                "detail": ("the paper carries Table %s but tables.md does not, "
                           "so it was written by hand and no generated block "
                           "backs it." % num),
                "expected": "a generated block in tables.md",
                "found": "absent",
            })
    return out


def check_table_blocks_are_generated(text, tables_md):
    """The assembled paper splices tables.md verbatim. A table block that no
    longer matches the generated one means the paper is stale against the
    results it was built from."""
    if not tables_md.strip():
        return []

    def blocks(src):
        out = {}
        for r in segment(src):
            if r["region"] != "table legend":
                continue
            num = r["label"].split()[1]
            out[num] = (re.sub(r"\s+", " ", r["text"]).strip(),
                        [re.sub(r"\s+", " ", x).strip()
                         for x in r["body"].split("\n") if x.strip()])
        return out

    paper, gen = blocks(text), blocks(tables_md)
    out = []
    for num in sorted(set(paper) & set(gen)):
        pl, pb = paper[num]
        gl, gb = gen[num]
        for what, a, b in (("legend", pl, gl), ("body", pb, gb)):
            if a == b:
                continue
            av, bv = _values_of(str(a)), _values_of(str(b))
            diff = [x for x in bv if x not in av][:3]
            out.append({
                "severity": "high", "kind": "table-block-not-generated",
                "where": "Table %s %s" % (num, what),
                "detail": ("the %s in PAPER_COMPLETE.md is not the one "
                           "build_tables.py generated into tables.md%s"
                           % (what,
                              "; tables.md carries %s and the paper does not"
                              % ", ".join("%g" % d for d in diff)
                              if diff else " (wording only)")),
            })
    return out


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

def check(text: str, ctx: dict) -> list[dict]:
    """Return a list of findings. Empty list means clean."""
    root = Path(ctx.get("root") or Path(__file__).resolve().parents[2])
    tables_md = ctx.get("tables") or ""
    if not tables_md:
        p = root / "manuscript" / "tables.md"
        tables_md = p.read_text(encoding="utf-8") if p.exists() else ""

    regions = segment(text)
    idx = build_index(root, text, tables_md)

    findings = []
    findings += check_stated_percentages(regions)
    findings += check_restated_counts(regions)
    findings += check_partitions(regions)
    findings += check_legend_against_own_body(regions, idx)
    findings += check_box_arithmetic(regions)
    findings += check_table_blocks_are_generated(text, tables_md)
    findings += check_inventory(text, regions, tables_md)

    counts = {}
    for r in regions:
        own_body = sorted(set(_values_of(r["body"]))) if r["body"] else []
        c = counts.setdefault(r["region"],
                              {"claims": 0, "traceable": 0, "regions": 0,
                               "skipped": 0, "results": 0})
        c["regions"] += 1
        for cl in region_claims(r["text"], r["region"], r["label"], r["line"], c):
            c["claims"] += 1
            if traceable(cl, idx["all"]) or (own_body and traceable(cl, own_body)):
                c["traceable"] += 1
                if traceable(cl, idx["results"]):
                    c["results"] += 1
                continue
            findings.append({
                "severity": "high" if r["region"] == "table legend" else "medium",
                "kind": "untraceable-number",
                "where": "%s (line %d)" % (cl.label, cl.line),
                "detail": ("the value %s appears in no results table, no "
                           "receipt and no table body: \"...%s...\""
                           % (cl.raw, cl.context)),
                "found": cl.raw,
            })

    findings.append({
        "severity": "low", "kind": "coverage-summary", "where": "whole manuscript",
        "detail": "; ".join(
            "%s (%d): %d numeric claims, %d traceable, %d of those to a "
            "results table or receipt, %d tokens skipped as conventions"
            % (k, v["regions"], v["claims"], v["traceable"], v["results"],
               v["skipped"])
            for k, v in sorted(counts.items())) or "no regions found",
        "expected": "every region scanned",
        "found": "%d numeric claims outside table bodies"
                 % sum(v["claims"] for v in counts.values()),
    })
    return findings


def main() -> int:
    try:                                    # legends carry N₀, µL, 10⁻³
        import sys
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    root = Path(__file__).resolve().parents[2]
    text = (root / "manuscript" / "PAPER_COMPLETE.md").read_text(encoding="utf-8")
    def read(name):
        p = root / "manuscript" / name
        return p.read_text(encoding="utf-8") if p.exists() else ""

    ctx = {"root": root, "tables": read("tables.md"),
           "prose": read("RATE_VS_DURATION.md")}
    found = check(text, ctx)
    order = {"high": 0, "medium": 1, "low": 2}
    for f in sorted(found, key=lambda x: (order[x["severity"]], x["kind"])):
        print("[%-6s] %-26s %s" % (f["severity"].upper(), f["kind"], f["where"]))
        for line in f["detail"].split("; "):
            print("          %s" % line)
    n = sum(1 for f in found if f["kind"] != "coverage-summary")
    print("\n%d finding(s)" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
