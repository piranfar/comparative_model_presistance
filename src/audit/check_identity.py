"""
Is the same number called the same thing everywhere, in the same unit?

Run:  python -m src.audit.check_identity
      python -m src.audit.check_identity --debug      every classified literal
      python -m src.audit.check_identity --selftest   plant the old errors

Two families of check, both reading the assembled manuscript rather than the
results tables, because the failures they catch live in prose, table legends,
figure legends, Box 1 and the Abstract, where the value audit never looks.

STATISTIC IDENTITY
------------------
Every distinctive numeric literal is collected with the words around it and
given the statistical label that window implies: p-value, hazard ratio, odds
ratio, confidence-interval bound, correlation, proportion, count, log10
quantity, rate, days, fold change.  A literal carrying two mutually exclusive
labels is a candidate.  The historical failure this is built for: 0.138, 0.172
and 0.576 were hazard ratios in the Results and p-values in a table and a
figure legend.

The hard part is silence.  Three significant figures is not by itself rare in a
manuscript with seven hundred numbers in it.  In this text 0.138 really is
institute B's imputation kill rate in Table 8 *and* a p-value in Table 15;
0.0590 is a concentration slope in Table 13 *and* a linear-model p in Table S2;
2.95 is a starting density in log10 *and* a percentile in days.  A numeral
shared by two unrelated quantities is a coincidence, not an error, so a
conflict is reported only with evidence that the two sites are talking about
the same quantity:

  * a shared tuple -- two or more further distinctive literals written beside
    it at both sites.  "0.138, 0.172, 0.576" appearing in both places is this,
    and it is what the historical failure looked like; or
  * a shared rare subject -- both windows name the same uncommon things (the
    same drug, predictor, endpoint or estimator), rarity measured by document
    frequency so that "laboratory", "density" and "isolate" cannot carry it.

Tuple evidence is reported high, subject evidence low, and every finding says
which of the two it rests on.

UNIT CONSISTENCY
----------------
The clinical deposit is a most-probable-number series: its floor and its
densities are MPN per mL and must never be printed as CFU/mL.  The
six-laboratory and hollow-fibre deposits are colony counts: their floors -- 10,
100 and 400 CFU/mL, one colony in 100, 10 and 2.5 uL -- must never be printed
as MPN.  Headroom h is log10(N0/L), a ratio of two densities, and carries no
concentration unit at all.

Conventions taken from the Methods first, so that they are not reported as
errors:
  * h is dimensionless by design and is quoted in log10 units;
  * "assay ceiling" (a limit on how long the assay looks) and "assay floor" (a
    limit on how deep it sees) are different mechanisms on purpose;
  * a value may legitimately appear at different precisions in the Abstract and
    in a table, so literals are grouped by value, not by spelling;
  * fold figures are ten raised to the unrounded log10 difference, so a fold
    and its log10 are different numbers and are never compared as one;
  * 23, 230 and 2300 are the visit-specific MPN rungs of one deposit, and the
    same numerals elsewhere are counts, depths and percentages, so a unit rule
    fires only where the sentence is actually about a floor.
"""
from __future__ import annotations

import bisect
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------
# number extraction
# --------------------------------------------------------------------------

_SUP = {"\u2070": "0", "\u00b9": "1", "\u00b2": "2", "\u00b3": "3",
        "\u2074": "4", "\u2075": "5", "\u2076": "6", "\u2077": "7",
        "\u2078": "8", "\u2079": "9", "\u207b": "-", "\u207a": "+"}
_SUPCH = "".join(_SUP)


def _desup(s: str) -> str:
    return "".join(_SUP.get(c, c) for c in s)


_SCI = re.compile(
    r"(?<![\d.])(\d+(?:\.\d+)?)\s*[\u00d7x*]\s*10\s*"
    r"([" + _SUPCH + r"]+|\^-?\d+|-?\d+)")

# A leading sign is taken only where it cannot be a range dash: after a space,
# a bracket, a pipe or an equals sign, never after a digit.  "1.30-4.12" is a
# confidence interval; "| -0.206 |" is a negative correlation.
_GROUPED = r"\d{1,3}(?:[ ,]\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?"
_PLAIN = re.compile(
    r"(?:(?<=^)|(?<=[\s(\[|=]))([-+\u2212]?)(" + _GROUPED + r")"
    r"|(?<![\d.\w])()(" + _GROUPED + r")")
_YEARISH = re.compile(r"(19|20)\d{2}")


def _sigfigs(digits: str) -> int:
    """Significant figures in a literal as written.

    Trailing zeros on a bare integer are not counted -- 230 000 is two figures,
    not six -- so a rounded density is never treated as distinctive.  Trailing
    zeros after a decimal point are counted, since 3.00 was written that way on
    purpose.
    """
    s = digits.replace(",", "").replace(" ", "")
    if "." in s:
        return len(s.replace(".", "").lstrip("0"))
    d = s.lstrip("0").rstrip("0")
    return len(d)


def _numbers(line: str):
    """Yield (start, end, literal, value, sigfigs) for one line."""
    out, taken = [], []
    for m in _SCI.finditer(line):
        mant, exp = m.group(1), _desup(m.group(2)).replace("^", "")
        try:
            val = float(mant) * 10.0 ** int(exp)
        except ValueError:
            continue
        out.append((m.start(), m.end(), m.group(0), val, _sigfigs(mant)))
        taken.append((m.start(), m.end()))
    for m in _PLAIN.finditer(line):
        if any(a <= m.start() < b for a, b in taken):
            continue
        sign = (m.group(1) or m.group(3) or "").replace("\u2212", "-")
        digits = m.group(2) or m.group(4)
        lit = sign + digits
        try:
            val = float(lit.replace(",", "").replace(" ", ""))
        except ValueError:
            continue
        out.append((m.start(), m.end(), lit, val, _sigfigs(digits)))
    return sorted(out)


# --------------------------------------------------------------------------
# document structure
# --------------------------------------------------------------------------

class Occurrence:
    __slots__ = ("line", "off", "literal", "value", "sig", "section", "site",
                 "before", "after", "wide", "header", "rowlabel", "label",
                 "gap")

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"<{self.literal} {self.label} {self.site} L{self.line}>"


_TABLE_LEGEND = re.compile(r"^\*\*Table\s+(S?\d+)\.\*\*")
_FIG_LEGEND = re.compile(r"^\*\*Figure\s+(\d+)\.")
_SEP_ROW = re.compile(r"^\|[\s:\-|]+\|\s*$")


def _cells(row: str):
    """Split a markdown row into (cell_text, offset_in_line) pairs."""
    out, i = [], row.find("|")
    if i < 0:
        return out
    pos = i + 1
    while True:
        j = row.find("|", pos)
        if j < 0:
            break
        out.append((row[pos:j], pos))
        pos = j + 1
    return out


def parse(text: str) -> list[Occurrence]:
    """Walk the manuscript and return every numeric occurrence with context."""
    lines = text.split("\n")
    starts, pos = [], 0
    for ln in lines:
        starts.append(pos)
        pos += len(ln) + 1

    occ: list[Occurrence] = []
    section = "front matter"
    in_box = False
    legend_line, table_name, legend_text = -99, None, None
    fig_legend = None
    headers: list[str] = []
    pending_header: list[str] | None = None

    for i, ln in enumerate(lines):
        if ln.startswith("#"):
            section = ln.lstrip("#").strip()[:70]
            in_box, headers, table_name, legend_text = False, [], None, None
            fig_legend = None
        if ln.startswith("**Box 1."):
            in_box = True
        m = _TABLE_LEGEND.match(ln)
        if m:
            table_name, legend_text, legend_line, headers = (
                "Table " + m.group(1), ln, i, [])
            in_box = False
        m = _FIG_LEGEND.match(ln)
        if m:
            fig_legend = "Figure " + m.group(1)

        is_row = ln.lstrip().startswith("|")
        if is_row and _SEP_ROW.match(ln.strip()):
            if pending_header is not None:
                headers, pending_header = pending_header, None
            continue
        if is_row:
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if _SEP_ROW.match(nxt.strip()):
                pending_header = [c.strip().strip("*") for c, _ in _cells(ln)]
                continue

        if is_row:
            site = f"{table_name or 'table'} body"
        elif i == legend_line:
            site = f"{table_name} legend"
        elif in_box:
            site = "Box 1"
        elif fig_legend:
            site = f"{fig_legend} legend"
        elif section.lower().startswith("abstract"):
            site = "Abstract"
        else:
            site = "prose"

        if is_row:
            row_cells = _cells(ln)
            rowlabel = row_cells[0][0].strip() if row_cells else ""
            caption = (legend_text or "")[:500]
            for ci, (cell, coff) in enumerate(row_cells):
                head = headers[ci] if ci < len(headers) else ""
                for a, b, lit, val, sig in _numbers(cell):
                    occ.append(Occurrence(
                        line=i + 1, off=starts[i] + coff + a,
                        literal=lit, value=val, sig=sig,
                        section=section, site=site,
                        before=cell[max(0, a - 40):a], after=cell[b:b + 24],
                        wide=f"{caption} {head} {rowlabel} {cell}",
                        header=head, rowlabel=rowlabel, label=None, gap=None))
            continue

        prev = lines[i - 1] if i > 0 else ""
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        for a, b, lit, val, sig in _numbers(ln):
            occ.append(Occurrence(
                line=i + 1, off=starts[i] + a, literal=lit, value=val, sig=sig,
                section=section, site=site,
                before=(prev + " " + ln[:a])[-140:],
                after=(ln[b:] + " " + nxt)[:110],
                wide=prev + " " + ln + " " + nxt,
                header="", rowlabel="", label=None, gap=None))
    occ.sort(key=lambda o: o.off)
    return occ


# --------------------------------------------------------------------------
# statistical labelling
# --------------------------------------------------------------------------
# "before" is the text immediately preceding the literal, "after" the text
# immediately following.  Case matters for OR and HR, so those two are matched
# case-sensitively; everything else is not.

_HR_BEFORE = re.compile(r"(hazard ratios?\b[a-z ,]{0,32}?(of|is|are|=|,)?\s*"
                        r"|\bHR\s*=?\s*)$")
_OR_BEFORE = re.compile(r"(odds ratios?\b[a-z ,]{0,32}?(of|is|are|=|,)?\s*"
                        r"|\bOR\s*=?\s*|relative risk ratios?,?\s*)$")
# "resistant isolates have 2.32 times the odds of a higher tolerance class" is
# this manuscript's own way of writing an odds ratio, and the unit sits after
# the value rather than before it.  Without this the literal falls through to
# the confidence-interval fallback and is labelled a CI bound.
_TIMES_AFTER = re.compile(r"^\s*times the (odds|hazard|risk)\b", re.I)

_RHO_BEFORE = re.compile(r"(\u03c1\s*(=|of)?\s*|\brho\s*(of|=)?\s*"
                         r"|correlations? (of|=)\s*"
                         r"|(spearman|pearson)[a-z ]{0,14})$", re.I)
_AUC_BEFORE = re.compile(r"(area under the curve of\s*|\bAUC\s*(of)?\s*)$",
                         re.I)
_P_BEFORE = re.compile(
    r"(?:^|[^a-zA-Z])[pP]\s*(?:=|<|>|\u2264|\u2265|\s+is|\s+of)\s*$")
_P_WORD = re.compile(r"(p-values?|critical values?|two-sided p|exact p"
                     r"|nominal p|attained p|smallest[a-z ]{0,24}\bp\b)"
                     r"\s*(is|of|=|<|would be)?\s*$", re.I)

_FOLD_AFTER = re.compile(r"^\s*(-|\u2011)?fold|^\s*x(\b|[^a-z0-9])"
                         r"|^\s*\u00d7\b")
_PCT_AFTER = re.compile(r"^\s*(%|per cent)")
_DAY_AFTER = re.compile(r"^\s*days?\b")
_RATE_AFTER = re.compile(r"^\s*log\s?10\s*(CFU\s*/\s*mL\s*)?(per day|/\s*day)",
                         re.I)
_LOG_AFTER = re.compile(r"^\s*log\s?10\b|^\s*logs?\b")
_CONC_AFTER = re.compile(r"^\s*(CFU\s*(/|\s+per\s+)\s*mL|MPN\s*(/|\s+per\s+)"
                         r"\s*mL|per mL|\u00b5g\s*/\s*mL|ug\s*/\s*mL)", re.I)
_COUNT_AFTER = re.compile(
    r"^\s*(of\s+\d|isolates|readings|flasks|pairs|series|cultures|clones|"
    r"comparisons|tests|flags|calls|rows|counts|visits|laboratories|"
    r"resamples|draws|patients|samples)\b", re.I)
_COUNT_BEFORE = re.compile(r"\bn\s*=\s*$")
_OF_BEFORE = re.compile(r"\b(of|in)\s+$")
_CI_WORDS = re.compile(r"95 per cent (CI|interval|confidence)|95% CI"
                       r"|confidence interval|bootstrap[a-z ]{0,18}interval"
                       r"|profile interval|percentile interval", re.I)

# Header cues for table cells, tried before the prose cues.  "P(above to
# below)" is a transition probability and deliberately not a p-value.
_HEAD_RULES = [
    ("probability", re.compile(r"^p\s*\(.*(above|below|cross)", re.I)),
    ("p_value", re.compile(r"(^|\s)p$|^p\s*\(|p-value|critical value", re.I)),
    ("hazard_ratio", re.compile(r"hazard", re.I)),
    ("odds_ratio", re.compile(r"odds ratio", re.I)),
    ("correlation", re.compile(r"\brho\b|\u03c1|correlation", re.I)),
    ("rate", re.compile(r"rate.*log10|log10.*day|slope per", re.I)),
    ("fold", re.compile(r"fold", re.I)),
    ("ci_bound", re.compile(r"\bCI\b|interval", re.I)),
    ("days", re.compile(r"^days?\b|\(days\)", re.I)),
    ("log10", re.compile(r"log10|delta h", re.I)),
    ("percent", re.compile(r"%|per cent|percentage|fraction", re.I)),
    ("count", re.compile(r"^n$|^isolates$|^cultures$|^comparable pairs$"
                         r"|^inversions$|^dropped$|^retained$", re.I)),
]

_EFFECT_IN_LEGEND = (("odds_ratio", r"odds ratio"),
                     ("hazard_ratio", r"hazard ratio"),
                     ("correlation", r"\brho\b|\u03c1"))

_EFFECT = {"hazard_ratio", "odds_ratio", "correlation"}
_EXCLUSIVE: set[frozenset] = set()
for _a in _EFFECT | {"fold", "rate", "count", "days", "concentration",
                     "log10", "percent", "auc"}:
    _EXCLUSIVE.add(frozenset({"p_value", _a}))
for _a in _EFFECT:
    for _b in _EFFECT | {"rate", "concentration", "count", "days"}:
        if _a != _b:
            _EXCLUSIVE.add(frozenset({_a, _b}))


def classify(o: Occurrence) -> str | None:
    b, a = o.before, o.after
    if o.header:
        for lab, rx in _HEAD_RULES:
            if rx.search(o.header.strip()):
                return lab
    if _HR_BEFORE.search(b):
        return "hazard_ratio"
    if _OR_BEFORE.search(b):
        return "odds_ratio"
    m = _TIMES_AFTER.match(a)
    if m:
        return "odds_ratio" if m.group(1).lower() == "odds" else "hazard_ratio"
    if _RHO_BEFORE.search(b):
        return "correlation"
    if _AUC_BEFORE.search(b):
        return "auc"
    if _P_WORD.search(b) or _P_BEFORE.search(b):
        return "p_value"
    if _CONC_AFTER.match(a):
        return "concentration"
    if _RATE_AFTER.match(a):
        return "rate"
    if _FOLD_AFTER.match(a):
        return "fold"
    if _PCT_AFTER.match(a):
        return "percent"
    if _DAY_AFTER.match(a):
        return "days"
    if _LOG_AFTER.match(a):
        return "log10"
    if _COUNT_AFTER.match(a) or _COUNT_BEFORE.search(b):
        return "count"
    if _OF_BEFORE.search(b) and "." not in o.literal and abs(o.value) >= 20:
        return "count"
    # A table cell that is a point estimate with a parenthetical -- "2.11
    # (p=0.031, no)" -- takes the one effect measure its legend names, and
    # only where the legend names exactly one.
    if o.header and not o.before.strip() and a.lstrip().startswith("("):
        named = [lab for lab, rx in _EFFECT_IN_LEGEND
                 if re.search(rx, o.wide, re.I)]
        if len(named) == 1:
            return named[0]
    if _CI_WORDS.search(o.wide):
        return "ci_bound"
    return None


# A literal listed with another inherits its label: "hazard ratios of 0.138,
# 0.172 and 0.576" labels all three, and "p = 0.015, 0.016, 0.015, which
# adjustment ... moves to 0.138, 0.172, 0.576" carries the label across the
# connective too.  "against" and "versus" are deliberately NOT separators --
# the manuscript uses them to contrast two different statistics ("p = 0.0003)
# against 0.951 for clearing low").
_SEPS = r"[\s,;()\[\]\-\u2013\u2212]*"
_SEP_GAP = re.compile(r"^" + _SEPS + r"(and|or|to|through)?" + _SEPS + r"$",
                      re.I)
_MOVE_GAP = re.compile(
    r"^[\s,;]*(which|and|then)?[\s,]*([a-z ]{0,40})?"
    r"(moves?|falls?|rises?|shifts?|goes?|becomes?|drops?)"
    r"[\s,]*(those|them|it|these)?[\s,]*(to|from)[\s,]*$", re.I)


def _joined(text: str, a: Occurrence, b: Occurrence) -> str | None:
    """The separator between two adjacent literals, or None when there is more
    than a separator between them."""
    if abs(b.line - a.line) > 2:
        return None
    gap = text[a.off + len(a.literal):b.off]
    if len(gap) > 60:
        return None
    flat = " ".join(gap.split())
    if _SEP_GAP.match(flat) or _MOVE_GAP.match(flat):
        return flat
    return None


def inherit(text: str, occ: list[Occurrence]) -> None:
    """Propagate a label along a list, forwards and backwards, since the unit
    may sit at either end: "hazard ratios of A, B and C" but "A to B log10"."""
    for _ in range(3):
        moved = False
        for k in range(1, len(occ)):
            cur, prv = occ[k], occ[k - 1]
            if cur.label is None and prv.label not in (None, "ci_bound",
                                                       "count"):
                # "(OR 0.480, 0.340 to 0.677, p = ...)" -- the comma after an
                # effect estimate introduces its interval, not a second
                # estimate, so an effect label must not run on into the left
                # member of an "A to B" pair.  Without this, every lower
                # confidence bound in the paper is labelled an odds ratio,
                # and 0.340 collides with the hazard ratio 0.34.
                if prv.label in _EFFECT and k + 1 < len(occ):
                    nxt_gap = _joined(text, cur, occ[k + 1])
                    if nxt_gap is not None and nxt_gap.lower() == "to":
                        continue
                flat = _joined(text, prv, cur)
                if flat is not None:
                    cur.label, cur.gap, moved = prv.label, flat, True
        for k in range(len(occ) - 2, -1, -1):
            cur, nxt = occ[k], occ[k + 1]
            if cur.label is None and nxt.label not in (None, "ci_bound",
                                                       "count", "p_value"):
                flat = _joined(text, cur, nxt)
                if flat is not None:
                    cur.label, cur.gap, moved = nxt.label, flat, True
        if not moved:
            break


# --------------------------------------------------------------------------
# evidence that two occurrences are about the same quantity
# --------------------------------------------------------------------------

_STOP = set("""the and that with from this those there their them then than
into over under about which what when where while were was are is be been being
for not but its has have had can could would should will shall may might must
one two three four five six seven eight nine ten same each every any all both
other another such only also more most less least very much many few here does
did done per cent value values number numbers table figure section paper
deposit deposits reported report reports quoted given taken used using rather
because since after before between within against across through
""".split())
_WORD = re.compile(r"[a-z][a-z\-]{3,}")


def _doc_freq(text: str) -> Counter:
    """How many paragraphs each word appears in.  Crude, but enough to tell
    'moxifloxacin' from 'laboratory'."""
    df: Counter = Counter()
    for para in re.split(r"\n\s*\n", text):
        for w in set(_WORD.findall(para.lower())):
            df[w] += 1
    return df


def _peers(occ: list[Occurrence], offs: list[int], o: Occurrence,
           span: int = 130) -> set[float]:
    """Distinctive literals written beside this one, across line wraps."""
    lo = bisect.bisect_left(offs, o.off - span)
    hi = bisect.bisect_right(offs, o.off + span)
    return {round(q.value, 10) for q in occ[lo:hi]
            if q is not o and q.sig >= 3 and abs(q.value) < 100000
            and not (_YEARISH.fullmatch(q.literal) and q.value > 1900)}


def _usable(o: Occurrence, min_sig: int) -> bool:
    if o.sig < min_sig or o.label is None:
        return False
    if _YEARISH.fullmatch(o.literal) and o.value > 1900:
        return False
    if abs(o.value) >= 100000:            # accessions, N_reach, McFarland
        return False
    if o.value > 900 and re.search(
            r"figshare|zenodo|eLife|10\.5281|Source Data|CC BY", o.wide, re.I):
        return False
    return True


# Two significant figures, not three.  Three sounds safer and is not: this
# manuscript writes its hazard ratios as 0.20, 0.21, 0.34, 0.36 and 0.62 and
# several of its p-values as 0.0030 and 0.0042, all of which are two figures,
# so at three the only hazard ratio in the whole paper that is even looked at
# is 5.27.  The gate, not the threshold, is what keeps this quiet: at two
# figures the gated output on all three manuscript sources is still empty.
def statistic_identity(text: str, min_sig: int = 2,
                       debug: bool = False) -> list[dict]:
    occ = parse(text)
    for o in occ:
        o.label = classify(o)
    inherit(text, occ)

    df = _doc_freq(text)
    offs = [o.off for o in occ]
    live = [o for o in occ if _usable(o, min_sig)]

    groups: dict[float, list[Occurrence]] = defaultdict(list)
    for o in live:
        groups[round(o.value, 10)].append(o)

    findings = []
    for val, os_ in sorted(groups.items()):
        labels = {o.label for o in os_}
        for pair in sorted(p for p in _EXCLUSIVE if p <= labels):
            la, lb = sorted(pair)
            # Two *effect measures* on one value need no corroboration.  The
            # evidence gate exists because a bare numeral is shared by
            # unrelated quantities all over this manuscript -- but that is a
            # p-value problem: p-values, counts and percentages are dense
            # enough for coincidence, while hazard ratios, odds ratios and
            # correlations are not.  Ungated, the effect-versus-effect space
            # on PAPER_COMPLETE.md, tables.md and RATE_VS_DURATION.md is
            # empty, so requiring corroboration here buys no silence and
            # costs the commonest failure: prose restating a table's estimate
            # under the wrong name, with none of the table's other numbers
            # beside it to corroborate the match.
            effect_pair = pair <= _EFFECT
            best = None
            for x in [o for o in os_ if o.label == la]:
                for y in [o for o in os_ if o.label == lb]:
                    if x.line == y.line:
                        continue
                    if effect_pair:
                        best = (x, y, "both are effect measures, which this "
                                "manuscript does not reuse across quantities",
                                "high")
                        break
                    shared = _peers(occ, offs, x) & _peers(occ, offs, y)
                    if len(shared) >= 2:
                        best = (x, y, "the same neighbours ("
                                + ", ".join(f"{v:g}" for v in
                                            sorted(shared)[:4])
                                + ") are written beside it at both sites",
                                "high")
                        break
                    sx = set(_WORD.findall(x.wide.lower())) - _STOP
                    sy = set(_WORD.findall(y.wide.lower())) - _STOP
                    rare = sorted(w for w in (sx & sy) if df[w] <= 6)
                    if len(rare) >= 3 and best is None:
                        best = (x, y, "both windows name "
                                + ", ".join(rare[:4]), "low")
                if best and best[3] == "high":
                    break
            if best is None:
                continue
            x, y, why, sev = best
            findings.append({
                "severity": sev,
                "kind": "statistic-identity",
                "where": f"{x.site}, line {x.line} vs {y.site}, line {y.line}",
                "detail": (f"{x.literal} is used as a {la.replace('_', ' ')} "
                           f"at line {x.line} and as a "
                           f"{lb.replace('_', ' ')} at line {y.line}; {why}"),
                "expected": f"one statistical label for {x.literal}",
                "found": f"{la} at line {x.line}, {lb} at line {y.line}",
            })
    if debug:
        for o in occ:
            if o.sig >= min_sig:
                print(f"L{o.line:>5} {o.literal:>12} "
                      f"{str(o.label):<13} {o.site:<20} "
                      f"{('<-' + o.gap) if o.gap else '':<10}"
                      f" ...{o.before[-32:]!r} -> {o.after[:22]!r}")
    return findings


# --------------------------------------------------------------------------
# unit consistency
# --------------------------------------------------------------------------

_MPN_FLOORS = {23.0, 230.0, 2300.0}
_CFU_FLOORS = {10.0, 100.0, 400.0}

_CFU_UNIT = re.compile(r"CFU\s*(/|\s+per\s+)\s*mL", re.I)
_MPN_UNIT = re.compile(r"MPN\s*(/|\s+per\s+)\s*mL", re.I)

_FLOOR_CUE = re.compile(
    r"assay floor|\bfloor\b|\bL\s*=|\*L\*|lowest[a-z ]{0,18}rung"
    r"|minimum reportable|limit of quantification|quantification limit"
    r"|below-limit|bottoms out|pile-?up|smallest[a-z ]{0,22}count", re.I)
_CLIN_CUE = re.compile(r"vijay|clinical isolate|most probable number|\bMPN\b"
                       r"|day-5 column|day-2 column|rifampicin", re.I)
_PLATE_CUE = re.compile(r"ERA4TB|six-laborator|van Wijk|Dubey|hollow.fibre"
                        r"|hollow.fiber|plated volume|\bplating\b|\bplated\b"
                        r"|colony|\bCFU\b|\u00b5L|\buL\b", re.I)

# h, Delta h or "headroom" followed by a value and then something unit-shaped
_H_VALUE = re.compile(
    r"(?:\bheadroom\b|\*h\*|\u0394\s*\*?h\*?|\bdelta\s+h\b"
    r"|(?<![A-Za-z])h(?![A-Za-z]))"
    r"[^0-9\n]{0,18}?(\d+(?:\.\d+)?)\s*[-\u2011]?\s*"
    r"([A-Za-z\u00b5/][A-Za-z\u00b5/ ]{0,12})")
_H_LEGAL = re.compile(r"^(log\s?10|logs?|units?|and|to|at|for|in|of|or"
                      r"|per cent|days?|is|was|the|a|by|with|between)\b", re.I)


def _flag(sev, kind, where, detail, expected="", found=""):
    return {"severity": sev, "kind": kind, "where": where, "detail": detail,
            "expected": expected, "found": found}


# A ratio whose denominator is an MPN and whose numerator is stated in CFU/mL
# is a unit conversion, not a ratio.  Only fires where the *legend* names one
# CFU/mL reference shared by every row, so a table that carries each deposit's
# own floor in its own row (Table 9) cannot trip it.
_LEGEND_CFU_REF = re.compile(
    r"\d[\d.,]*\s*(?:e-?\d+|[x×]\s*10[\s\d⁰-⁹^-]*)?\s*"
    r"CFU\s*(?:/|\s+per\s+)\s*mL", re.I)
_LEGEND_RATIO = re.compile(r"\bfold\b|\bratio\b|\btimes\b|multiples? of", re.I)
_MPN_ROW = re.compile(r"vijay|clinical isolate|most probable number", re.I)

# The complaint is that the MPN rows are not marked as such.  A legend that
# says so itself has answered it, and the rule must then stand down -- a
# checker that keeps firing after the text has been fixed in exactly the way
# it asked for is a checker its authors will switch off.
_LEGEND_MPN_DISCLOSED = re.compile(
    r"most probable number|most-probable-number|\bMPN\b", re.I)


def _cross_unit_ratio(lines: list[str], tag: str) -> list[dict]:
    out, legend, name, hits, start = [], None, None, [], 0
    for i, ln in enumerate(lines + [""]):
        m = _TABLE_LEGEND.match(ln)
        end_of_table = m or ln.startswith("#") or (legend and not ln.strip()
                                                   and hits)
        if end_of_table and hits:
            out.append(_flag(
                "low", "unit-mpn-over-cfu-reference",
                f"{tag}{name} legend, line {start + 1}",
                f"{name} divides every row by one reference stated in CFU/mL, "
                f"but {len(hits)} row(s) are the most-probable-number deposit, "
                "so those ratios convert MPN into CFU without saying so",
                "the MPN rows marked as such, or the reference given per "
                "deposit", "; ".join(h[:78] for h in hits)))
            hits = []
        if m:
            legend, name, start = ln, "Table " + m.group(1), i
            continue
        if not legend or not ln.lstrip().startswith("|"):
            continue
        if _SEP_ROW.match(ln.strip()):
            continue
        if not (_LEGEND_CFU_REF.search(legend) and _LEGEND_RATIO.search(legend)):
            continue
        if _LEGEND_MPN_DISCLOSED.search(legend):
            continue
        if _MPN_ROW.search(ln) and _numbers(ln):
            hits.append(ln.strip())
    return out


# A deposit's *densities* wear its unit too, not only its floor.  The floor
# rules above key on the six floor values, so "the clinical isolates enter at
# 5.36 log10 CFU/mL" -- an MPN deposit wearing a colony-count unit on a number
# that is not a floor -- passed straight through them.  This rule works per
# sentence, and only where a numeral is actually attached to the unit: the
# Table S5 legend says "divided by a reference stated in CFU/mL" while naming
# the clinical rows, and that is disclosure, not a density.
# "clinical *Mycobacterium tuberculosis* isolates" is the Abstract's way of
# saying clinical isolates, and a cue that misses it makes the Abstract look
# like a plated section, which would be a false positive waiting to happen the
# first time someone writes a correct MPN figure there.
_DENS_CLIN = re.compile(r"vijay|clinical[^.\n]{0,40}?isolates?"
                        r"|most probable number|most-probable-number"
                        r"|\bMPN\b", re.I)
_DENS_PLATE = re.compile(r"ERA4TB|six-laborator|van Wijk|Dubey|hollow.fibre"
                         r"|hollow.fiber|plated volume|plating|plated|colony"
                         r"|colonies|institute", re.I)
_BRIDGE = re.compile(r"^[\s,]*(log\s?10|logs?|×|x)?[\s,]*$", re.I)


def _attached(sentence: str, unit_start: int) -> str | None:
    """The literal that this unit belongs to, or None when the unit is being
    named rather than used ("a reference stated in CFU/mL")."""
    for a, b, lit, _v, _s in _numbers(sentence):
        if b <= unit_start and _BRIDGE.match(sentence[b:unit_start]):
            return lit
    return None


def _blocks(lines: list[str]):
    """Contiguous runs of prose, rejoined, with the line each one starts at.

    The manuscript is hard-wrapped, so a sentence about the clinical deposit
    routinely names it on one line and gives its density on the next.  Working
    line by line would look at half a sentence and see no deposit at all.
    """
    buf, start = [], 0
    for i, ln in enumerate(lines + [""]):
        if not ln.strip() or ln.lstrip().startswith("|") or ln.startswith("#"):
            if buf:
                yield start, " ".join(buf)
            buf = []
        else:
            if not buf:
                start = i
            buf.append(ln.strip())


def _section_deposit(lines: list[str]) -> list[str | None]:
    """Per line: 'clin', 'plate' or None for the deposit its section is about.

    A sentence often names no deposit at all -- "Isoniazid-resistant isolates
    enter this assay at 5.36 log10" is the clinical panel, and says so only by
    the section it sits in.  The section is used only where it is unambiguous:
    it names one deposit and never the other.  Where a section discusses both,
    as Section 6 and the Abstract do, it yields no cue and the rule stays out.
    """
    bounds = [i for i, l in enumerate(lines) if l.startswith("#")]
    out: list[str | None] = [None] * len(lines)
    for a, b in zip([0] + bounds, bounds + [len(lines)]):
        body = "\n".join(lines[a:b])
        bare = _MPN_UNIT.sub(" ", _CFU_UNIT.sub(" ", body))
        cl, pl = bool(_DENS_CLIN.search(bare)), bool(_DENS_PLATE.search(bare))
        if cl == pl:
            continue
        for k in range(a, min(b, len(lines))):
            out[k] = "clin" if cl else "plate"
    return out


def _density_units(lines: list[str], tag: str) -> list[dict]:
    out = []
    sect = _section_deposit(lines)
    for i, block in _blocks(lines):
        for sent in re.split(r"(?<=[.;])\s+", block):
            # The cue search must not see the unit it is judging: "6.00 log10
            # MPN/mL" contains the token MPN, which would otherwise make every
            # mis-united plated density look like a clinical sentence.
            bare = _MPN_UNIT.sub(" ", _CFU_UNIT.sub(" ", sent))
            clin, plate = _DENS_CLIN.search(bare), _DENS_PLATE.search(bare)
            if not clin and not plate:
                s = sect[i] if i < len(sect) else None
                clin, plate = (s == "clin") or None, (s == "plate") or None
            for rx, want, other, kind, why in (
                (_CFU_UNIT, clin, plate, "unit-mpn-as-cfu",
                 "the clinical deposit reports most probable numbers, not "
                 "colony-forming units"),
                (_MPN_UNIT, plate, clin, "unit-cfu-as-mpn",
                 "the plated deposits report colony counts; only the clinical "
                 "deposit reports most probable numbers"),
            ):
                m = rx.search(sent)
                if not m or not want or other:
                    continue
                lit = _attached(sent, m.start())
                if lit is None:
                    continue
                out.append(_flag(
                    "high", kind, f"{tag}paragraph at line {i + 1}",
                    f"a density of {lit} is printed as {m.group(0)} in a "
                    f"sentence about the "
                    f"{'clinical' if want is clin else 'plated'}"
                    f" deposit; {why}", f"{lit} in the other unit",
                    sent.strip()[:150]))
    return out


def unit_consistency(text: str, label: str = "") -> list[dict]:
    findings = []
    lines = text.split("\n")
    tag = (label + " ") if label else ""

    for i, ln in enumerate(lines):
        window = " ".join(lines[max(0, i - 1): i + 2])

        for a, b, lit, val, sig in _numbers(ln):
            tail = ln[b:b + 30].lstrip()
            if val in _MPN_FLOORS and _CFU_UNIT.match(tail):
                if _FLOOR_CUE.search(window) and _CLIN_CUE.search(window) \
                        and not _PLATE_CUE.search(ln):
                    findings.append(_flag(
                        "high", "unit-mpn-as-cfu", f"{tag}line {i + 1}",
                        "the clinical deposit is a most-probable-number "
                        f"series, but its floor {lit} is printed as CFU/mL",
                        f"{lit} MPN/mL", ln[max(0, a - 30):b + 30].strip()))
            if val in _CFU_FLOORS and _MPN_UNIT.match(tail):
                if _PLATE_CUE.search(window) or _FLOOR_CUE.search(window):
                    findings.append(_flag(
                        "high", "unit-cfu-as-mpn", f"{tag}line {i + 1}",
                        f"a colony-count floor of {lit} is printed as MPN; "
                        "only the clinical deposit reports most probable "
                        "numbers", f"{lit} CFU/mL",
                        ln[max(0, a - 30):b + 30].strip()))

        m = re.search(r"\b(23|230|2300)\b\s*(colonies|colony|CFU)\b", ln, re.I)
        if m and _CLIN_CUE.search(window):
            findings.append(_flag(
                "high", "unit-mpn-as-cfu", f"{tag}line {i + 1}",
                f"the clinical floor of {m.group(1)} is an MPN table rung, "
                "not a colony count", f"{m.group(1)} MPN/mL", m.group(0)))

        for m in _H_VALUE.finditer(ln):
            unit = m.group(2).strip()
            if not unit or _H_LEGAL.match(unit):
                continue
            if re.match(r"CFU|MPN|per mL|/\s*mL|\u00b5g|ug/", unit, re.I):
                findings.append(_flag(
                    "high", "unit-headroom-concentration",
                    f"{tag}line {i + 1}",
                    "headroom is log10(N0/L), a dimensionless log ratio, but "
                    f"is printed with the concentration unit '{unit}'",
                    f"{m.group(1)} log10", m.group(0).strip()))
            elif re.match(r"fold\b", unit, re.I):
                # The Methods keep H = N0/L and h = log10(N0/L) apart on
                # purpose, and quote the fold as 10^h, not as h.
                findings.append(_flag(
                    "medium", "unit-headroom-as-fold", f"{tag}line {i + 1}",
                    "headroom is in log10 units; a fold difference is 10 "
                    "raised to it, not the value of h itself",
                    f"{m.group(1)} log10, or 10^h as a fold",
                    m.group(0).strip()))

    findings += _cross_unit_ratio(lines, tag)
    findings += _density_units(lines, tag)

    # whole table rows: a deposit's row must wear that deposit's unit
    for i, ln in enumerate(lines):
        if not ln.lstrip().startswith("|"):
            continue
        low = ln.lower()
        clinical = re.search(r"vijay|clinical isolate|thin clinical"
                             r"|adequate clinical", low)
        plated = re.search(r"era4tb|dubey|hollow|kaur|six-laborator"
                           r"|\bplate\b|\bdrop\b", low)
        if clinical and _CFU_UNIT.search(ln) and not _MPN_UNIT.search(ln):
            findings.append(_flag(
                "high", "unit-mpn-as-cfu", f"{tag}table row, line {i + 1}",
                "a clinical-deposit row carries CFU/mL; that deposit reports "
                "most probable numbers", "MPN per mL", ln.strip()[:130]))
        if plated and not clinical and _MPN_UNIT.search(ln):
            findings.append(_flag(
                "high", "unit-cfu-as-mpn", f"{tag}table row, line {i + 1}",
                "a colony-count deposit row carries MPN; only the clinical "
                "deposit reports most probable numbers", "CFU per mL",
                ln.strip()[:130]))
    return findings


# --------------------------------------------------------------------------

def _orphan_blocks(tables_md: str, assembled: str) -> str:
    """Table blocks in tables.md that never reached the assembled paper.

    Today there are none, and the whole of tables.md is checked by way of the
    assembled text.  If a table is ever cut from the manuscript but left in the
    generator's output, its units still get looked at, and once, not twice.
    """
    out, keep = [], False
    for ln in tables_md.split("\n"):
        m = _TABLE_LEGEND.match(ln)
        if m:
            keep = ln[:90] not in assembled
        elif ln.startswith("#"):
            keep = False
        if keep:
            out.append(ln)
    return "\n".join(out)


def check(text: str, ctx: dict) -> list[dict]:
    """Return a list of findings.  Empty list means clean."""
    findings = statistic_identity(text)
    findings += unit_consistency(text)
    orphan = _orphan_blocks(ctx.get("tables") or "", text)
    if orphan.strip():
        findings += unit_consistency(orphan, label="tables.md (not assembled),")
    return findings


# --------------------------------------------------------------------------
# self-test: plant the errors this module exists to catch
# --------------------------------------------------------------------------

_PLANTS = [
    ("hazard ratios that a table calls p-values",
     "concordance\nrises from 0.896 to 0.930 (Fig. 2D).",
     "concordance\nrises from 0.896 to 0.930 (Fig. 2D). On laboratory alone "
     "institutes D, E and F\ncarry hazard ratios of 0.138, 0.172 and 0.576."),
    ("a figure legend calling correlations p-values",
     "Amber marks the four reaching nominal significance;\nnone survives.",
     "Amber marks the four reaching nominal significance;\nnone survives. "
     "The four carry p = -0.206, -0.218, -0.198\nand -0.153 against the "
     "critical value each would have to beat."),
    ("the clinical MPN floor printed as CFU/mL",
     "| Vijay 2024 | no | no | 23 | MPN per mL | INFERRED |",
     "| Vijay 2024 | no | no | 23 | CFU per mL | INFERRED |"),
    ("the clinical floor called a colony count in prose",
     "bottoms out at 23 per mL with a visible pile-up",
     "bottoms out at 23 CFU/mL with a visible pile-up"),
    ("a colony-count floor printed as MPN",
     "since *L* = 10 CFU/mL at this plating",
     "since *L* = 10 MPN/mL at this plating"),
    ("headroom given a concentration unit",
     "\u0394*h* = 2.33 log10, a\n216-fold difference",
     "\u0394*h* = 2.33 CFU/mL, a\n216-fold difference"),
    ("headroom quoted as a fold rather than in log10",
     "the spread is \u0394*h* = 2.33 log10, a",
     "the spread is \u0394*h* = 216-fold, a"),
    ("an odds ratio the Abstract calls a p-value",
     "resistance, which does not.",
     "resistance, which does not. Resistant isolates carry "
     "p = 2.317 (1.30 to 4.12)."),
    # The commonest real failure is barer than the historical one: prose
    # restating a table's estimate under the wrong name, with none of the
    # table's other numbers beside it to corroborate the match.
    ("prose restating an odds ratio as a hazard ratio, with no corroboration",
     "in odds ratios, and — where the proportionality it assumes fails",
     "in odds ratios (a hazard ratio of 0.480 for each ten-fold rise), and "
     "— where the proportionality it assumes fails"),
    ("the Abstract renaming the odds ratio behind 'times the odds'",
     "isoniazid\nresistance, which does not.",
     "isoniazid\nresistance, which does not (hazard ratio 2.32)."),
    ("a two-figure p-value renamed a hazard ratio in a table legend",
     "**Table 7.** The family of 8 tests",
     "**Table 7.** Growth carries a hazard ratio of 0.0030. "
     "The family of 8 tests"),
    ("a clinical density -- not a floor -- printed as CFU/mL",
     "enter this assay at 5.36 log10 against 6.36 for susceptible isolates",
     "enter this assay at 5.36 log10 CFU/mL against 6.36 for susceptible "
     "isolates"),
    ("a plated density -- not a floor -- printed as MPN/mL",
     "gives realised densities of 3.67, 4.61, 4.65 and 6.00 log10 CFU/mL",
     "gives realised densities of 3.67, 4.61, 4.65 and 6.00 log10 MPN/mL"),
]


def selftest(text: str, ctx: dict) -> int:
    """Plant each error this module exists to catch and check it is caught.

    Findings are compared on kind and evidence rather than on the whole dict,
    because planting text shifts the line numbers of everything below it.
    """
    def sig(f):
        return (f["kind"], f["found"])

    missed = 0
    base = check(text, ctx)
    seen = {sig(f) for f in base}
    print(f"baseline on the real manuscript: {len(base)} finding(s)\n")
    for name, old, new in _PLANTS:
        if old not in text:
            print(f"  SKIP  {name}: anchor text no longer in the manuscript")
            missed += 1
            continue
        got = check(text.replace(old, new, 1), ctx)
        fresh = [f for f in got if sig(f) not in seen]
        print(f"  {'ok  ' if fresh else 'MISS'}  {name}: "
              f"{len(fresh)} new finding(s)")
        for f in fresh[:3]:
            print(f"            [{f['severity']}] {f['kind']} {f['where']}")
        if not fresh:
            missed += 1
    return missed


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    root = Path(__file__).resolve().parents[2]
    man = root / "manuscript"
    text = (man / "PAPER_COMPLETE.md").read_text(encoding="utf-8")
    ctx = {
        "root": root,
        "tables": (man / "tables.md").read_text(encoding="utf-8"),
        "prose": (man / "RATE_VS_DURATION.md").read_text(encoding="utf-8"),
    }

    if "--debug" in sys.argv:
        statistic_identity(text, debug=True)
        return 0
    if "--selftest" in sys.argv:
        missed = selftest(text, ctx)
        print("\nself-test:", "every plant caught" if not missed
              else f"{missed} plant(s) missed")
        return 1 if missed else 0

    findings = check(text, ctx)
    if not findings:
        print("check_identity: clean (0 findings)")
        return 0
    rank = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: rank.get(f["severity"], 3))
    for f in findings:
        print(f"[{f['severity'].upper():<6}] {f['kind']}  {f['where']}")
        print(f"          {f['detail']}")
        if f.get("expected"):
            print(f"          expected: {f['expected']}")
        if f.get("found"):
            print(f"          found:    {f['found']}")
        print()
    print(f"check_identity: {len(findings)} finding(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
