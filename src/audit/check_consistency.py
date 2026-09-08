"""Checker 4 -- does the manuscript agree with itself and with its own audit table?

Four families of check are run over the assembled manuscript
(``manuscript/PAPER_COMPLETE.md``):

(a) THE SELF-AUDIT TABLE.  One table recomputes every conclusion at the level its
    observations are actually independent and carries a ``Verdict`` column.  A
    conclusion marked ``NOT SUPPORTED`` must not still be *asserted* anywhere in
    the body, a table legend, a figure legend or a table's own body rows (each
    row is matched on its own, so numbers from unrelated rows cannot pool into
    a spurious match).  Matching is fuzzy -- on the
    distinctive numbers and content words of the conclusion string -- and is
    suppressed where the surrounding text reports the claim as withdrawn, as
    description without inference, or explicitly declines to attach a test to it.

(b) DENOMINATOR TRACEABILITY.  One table gives the flow account: every analysis
    set as a stage, an n and a count excluded.  Every ``n = ...``, every bare
    analysis-set denominator carrying a reported statistic, every explicit ``n``
    column of another table, and every stated exclusion count should trace to a
    value that account holds.  A stated exclusion is checked against exclusions
    rather than against any number anywhere: when the sentence names a panel,
    the count must be one that panel actually records, so an exclusion cannot
    be waved through by an unrelated stage that happens to carry the same
    integer.  The account's own chain is checked too -- a stage that removes k
    rows must have a sibling stage of the same panel holding exactly k more --
    because it is the standard everything else is measured against.  Five
    things are deliberately not flagged, because the flow account does not
    promise them: counts belonging to deposits it does not cover; one arm of a
    split whose arms sum to a traced total; a table column that decomposes a
    traced total; a subset defined by its own outcome ("the 140 series that
    cross") rather than by an exclusion; and a stacked set that is a small
    multiple of a stage named in the same row ("420 isolate-panel", two panels
    of the same 210 isolates).

(c) CROSS-REFERENCE RESOLUTION.  Every ``Table N``, ``Table SN``, ``Figure N``,
    ``Fig. NX``, ``Section N`` and ``Box N`` reference must resolve to something
    that exists.  Methods subsections are unnumbered, so ``Section N of the
    Methods`` cannot resolve; and a ``described in Section N`` pointer whose
    subject never occurs in the section it names is dangling too.

(d) SUPERSEDED PASSAGES.  A rewrite that leaves its predecessor in place says
    the same thing twice, and check (a) cannot see it: that check's universe is
    the conclusions the self-audit table lists as ``NOT SUPPORTED``, so a reading
    retracted in the prose alone lies outside it.  Two sentences of one block
    that share most of their content words are flagged instead, because that is
    what a paragraph looks like when the passage its rewrite replaced was never
    deleted.

Run standalone with::

    python -m src.audit.check_consistency
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------
# text utilities
# --------------------------------------------------------------------------

# The manuscript uses ordinary spaces as thousands separators ("2 775").
_THOU = "[   ]"
_NUM_RE = re.compile(r"\d{1,3}(?:" + _THOU + r"\d{3})+|\d+")
_NUM_PAT = r"\d{1,3}(?:" + _THOU + r"\d{3})+|\d+"

_SUPERSCRIPTS = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "⁻": "-",
}
_SUBSCRIPTS = {
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5",
}


def _normalise(s: str) -> str:
    """Fold the typographic characters the manuscript uses into ASCII."""
    out = []
    for ch in s:
        if ch in _SUPERSCRIPTS:
            out.append(_SUPERSCRIPTS[ch])
        elif ch in _SUBSCRIPTS:
            out.append(_SUBSCRIPTS[ch])
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


def _int(tok: str) -> int:
    return int(re.sub(r"[   ,]", "", tok))


def _plain(s: str) -> str:
    """Strip markdown emphasis so phrases match across **bold** and *italic*."""
    return re.sub(r"[*_`]", "", s)


def _tokens(s: str) -> list[str]:
    return re.findall(r"[a-z][a-z-]*", _plain(_normalise(s)).lower())


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


def _content_words(s: str) -> list[str]:
    return [t for t in _tokens(s) if t not in _STOP and len(t) > 2]


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


def _ctx(text: str, pos: int, width: int = 130) -> str:
    a = max(0, pos - 25)
    return re.sub(r"\s+", " ", text[a:a + width]).strip()


def _sentence(text: str, pos: int) -> str:
    a = text.rfind(". ", 0, pos)
    a = 0 if a < 0 else a + 2
    b = text.find(". ", pos)
    b = len(text) if b < 0 else b + 1
    return re.sub(r"\s+", " ", text[a:b])


# --------------------------------------------------------------------------
# manuscript structure
# --------------------------------------------------------------------------

_CAPTION_RE = re.compile(r"^\*\*(Table|Figure|Box)\s+(S?\d+)[.:]")
_TABLE_ROW_RE = re.compile(r"^\s*\|")


class Manuscript:
    """Everything the three checks need to know about the document's shape."""

    def __init__(self, text: str):
        self.text = text
        self.lines = text.split("\n")
        self.blocks = _paragraphs(text)

        self.tables: dict[str, dict] = {}      # "5" / "S1" -> caption + grid
        self.figures: dict[str, dict] = {}     # "1" -> legend + panels
        self.boxes: set[str] = set()
        self.results_sections: dict[int, tuple[int, int, str]] = {}
        self.methods_subsections: list[str] = []

        self._scan_captions()
        self._scan_sections()

    # -- captions ---------------------------------------------------------
    def _scan_captions(self) -> None:
        for lineno, block in self.blocks:
            m = _CAPTION_RE.match(block)
            if not m:
                continue
            kind, num = m.group(1), m.group(2)
            if kind == "Box":
                self.boxes.add(num)
                continue
            if kind == "Figure":
                self.figures[num] = {
                    "line": lineno,
                    "legend": block,
                    "panels": set(re.findall(r"\(\*\*([A-Z])\*\*\)", block)),
                }
                continue
            self.tables[num] = {
                "line": lineno,
                "caption": block,
                "grid": self._grid_after(lineno + block.count("\n")),
            }

    def _grid_after(self, lineno: int) -> list[list[str]]:
        """The pipe-delimited grid that follows the caption ending at `lineno`."""
        rows: list[list[str]] = []
        i = lineno                      # 0-based index of the next line
        n = len(self.lines)
        while i < n and self.lines[i].strip() == "":
            i += 1
        while i < n and _TABLE_ROW_RE.match(self.lines[i]):
            cells = [c.strip() for c in self.lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                rows.append(cells)
            i += 1
        return rows

    # -- headings ---------------------------------------------------------
    def _scan_sections(self) -> None:
        """Numbered '### N. Title' headings are the manuscript's Sections.

        They are collected wherever they appear rather than only under the
        Results heading: the assembled document occasionally interleaves other
        top-level headings, and only the Results sections are numbered anyway.
        """
        in_methods = False
        current: int | None = None
        start = 0
        for i, line in enumerate(self.lines, start=1):
            if line.startswith("## "):
                in_methods = line[3:].strip().lower().startswith("methods")
                continue
            if line.startswith("### "):
                title = line[4:].strip()
                m = re.match(r"(\d+)\.\s+(.*)", title)
                if m:
                    if current is not None:
                        self._close(current, start, i - 1)
                    current = int(m.group(1))
                    start = i
                elif in_methods:
                    self.methods_subsections.append(title)
        if current is not None:
            self._close(current, start, len(self.lines))

    def _close(self, num: int, a: int, b: int) -> None:
        self.results_sections[num] = (a, b, "\n".join(self.lines[a - 1:b]))

    # -- lookups ----------------------------------------------------------
    def table_by_header(self, *required: str):
        """First table whose header row carries all the given cell names."""
        want = [r.lower() for r in required]
        for num, tab in self.tables.items():
            if not tab["grid"]:
                continue
            header = [c.lower() for c in tab["grid"][0]]
            if all(any(w == h or w in h for h in header) for w in want):
                return num, tab
        return None, None


# --------------------------------------------------------------------------
# (a) the self-audit table
# --------------------------------------------------------------------------

# Text saying the claim is reported as withdrawn, as description, or without the
# inference the audit table struck out.
_WITHDRAWAL_MARKERS = (
    "not supported", "no longer", "withdrawn", "deleted",
    "removed from the text", "do not survive", "does not survive",
    "not recomputable", "without a p-value", "with no p-value", "no p-value",
    "quoted without", "descriptive", "description", "descriptively",
    "not a test", "rather than a test", "not a finding", "none is claimed",
    "no between-laboratory test", "not because they are valid", "not evidence",
    "is a description", "smallest attainable", "cannot produce a meaningful p",
    "not valid", "invalid", "with the same restraint",
    "reported for the same reason", "singular by construction",
    "does not fail loudly", "wrong instrument", "bounds the evidence",
    "recomputed at the level", "is refused", "are refused",
    "no p is quoted", "no p-value is quoted", "no p-value is attached",
)


def _claim_numbers(claim: str) -> list[str]:
    """Distinctive numeric fingerprints: decimals, exponentials, 3+ digit ints."""
    out: list[str] = []
    for m in re.finditer(r"\d+\.\d+e-?\d+|\d+e-?\d+|\d+\.\d+|\d{3,}",
                         _normalise(claim)):
        out.append(m.group(0))
    return out


def _number_in(tok: str, hay: str) -> bool:
    """Look for a number, allowing 1.2e-10 <-> 1.2 x 10-10 style rewrites."""
    if re.search(r"(?<![\d.])" + re.escape(tok) + r"(?!\d)", hay):
        return True
    m = re.fullmatch(r"(\d+(?:\.\d+)?)e(-?\d+)", tok)
    if m:
        alt = rf"{re.escape(m.group(1))}\s*(?:x|\*)\s*10\s*-?{abs(int(m.group(2)))}"
        if re.search(alt, hay):
            return True
    return False


def _check_self_audit(ms: Manuscript) -> list[dict]:
    num, tab = ms.table_by_header("verdict", "conclusion")
    if tab is None:
        num, tab = ms.table_by_header("verdict")
    if tab is None or not tab["grid"]:
        return [{
            "severity": "medium",
            "kind": "audit-table-missing",
            "where": "manuscript",
            "detail": "No table with a Verdict column was found, so the "
                      "self-audit could not be cross-checked against the text.",
        }]

    header = [c.lower() for c in tab["grid"][0]]
    i_concl = next((i for i, h in enumerate(header) if "conclusion" in h), 1)
    i_verdict = next(i for i, h in enumerate(header) if "verdict" in h)
    i_section = 0 if "section" in header[0] else None

    failed: list[tuple[str, str]] = []
    for row in tab["grid"][1:]:
        if len(row) <= max(i_concl, i_verdict):
            continue
        if row[i_verdict].strip().upper().replace("-", " ") == "NOT SUPPORTED":
            sect = row[i_section].strip() if i_section is not None else "?"
            failed.append((sect, row[i_concl].strip()))

    # Every place a claim could be re-asserted: prose blocks and legends, plus
    # the body rows of every other table.  A row is scanned as its own unit --
    # a whole grid would pool numbers from unrelated rows and match anything.
    targets: list[tuple[int, str]] = [
        (ln, b) for ln, b in ms.blocks
        if not _plain(_normalise(b)).lstrip().startswith("|")
    ]
    for tnum, t in ms.tables.items():
        if tnum == num or not t["grid"]:
            continue
        if any("stage" == h.lower() or "stage" in h.lower()
               for h in t["grid"][0]) and any(
                   "exclud" in h.lower() for h in t["grid"][0]):
            continue                        # the flow account, not a claim
        caption_low = _plain(_normalise(t["caption"])).lower()
        withdrawn_caption = any(mk in caption_low
                                for mk in _WITHDRAWAL_MARKERS)
        for row in t["grid"][1:]:
            if withdrawn_caption:
                continue
            targets.append((t["line"], "TABLEROW " + tnum + ": "
                            + " ".join(row)))

    findings: list[dict] = []
    for sect, claim in failed:
        nums = _claim_numbers(claim)
        words = set(_content_words(claim))
        if not words:
            continue
        for lineno, block in targets:
            btxt = _plain(_normalise(block))
            low = btxt.lower()
            # DISTINCT numbers. A value the withdrawn claim happens to state
            # twice -- "p = 0.015, 0.016, 0.015" -- used to score two hits
            # against a single occurrence in the block, so one coincidental
            # number was enough to fire. That is what it did on Section 9's
            # bootstrap intervals, whose "-0.015" has nothing to do with a Cox
            # p-value: one shared number, no shared word, reported as a
            # re-asserted conclusion.
            hits = {t for t in nums if _number_in(t, btxt)}
            shared = words & set(_content_words(block))
            cov = len(shared) / len(words)
            # Two numbers in common and NOTHING else is a collision, not a
            # restatement: a block that re-asserts a claim uses some of its
            # words. One shared content word is a low bar and it is enough to
            # tell the two cases apart.
            fires = ((len(hits) >= 2 and shared)
                     or (len(hits) >= 1 and cov >= 0.50)
                     or (cov >= 0.70 and len(shared) >= 3))
            if not fires:
                continue
            if any(mk in low for mk in _WITHDRAWAL_MARKERS):
                continue
            if btxt.startswith("TABLEROW "):
                btxt = btxt.split(":", 1)[1].strip()
                place = f"line {lineno} (a body row of Table " \
                        f"{block.split()[1].rstrip(':')})"
            else:
                place = f"line {lineno}"
            findings.append({
                "severity": "high",
                "kind": "not-supported-claim-still-asserted",
                "where": place,
                "detail": (
                    f"A conclusion Table {num} marks NOT SUPPORTED (its "
                    f"Section {sect} row) still reads as asserted here, with "
                    f"nothing marking it as withdrawn or as description only."),
                "expected": f"withdrawn, or reported as description: {claim[:130]}",
                "found": _ctx(btxt, 0, 170),
            })
    return findings


# --------------------------------------------------------------------------
# (b) denominator traceability
# --------------------------------------------------------------------------

# Units the flow account enumerates.  A denominator counted in any other unit is
# an object the flow account does not cover, and is out of scope rather than
# untraceable.  "cell" is deliberately absent: here it usually means a
# contingency-table cell ("the 0 of 33 cell").
_FLOW_UNITS = ("isolates?", "flasks?", "series", "readings?", "pairs?",
               "rows?", "calls?", "flags?")
_UNIT_RE = "(?:" + "|".join(_FLOW_UNITS) + ")"

_DENOM_RE = re.compile(
    r"\b(?:of|over|across|among|on|from|in|is|are|was|were)\s+"
    r"(?:the\s+|all\s+|its\s+|those\s+|these\s+)?"
    r"(" + _NUM_PAT + r")\s+"
    r"((?:[a-z][a-z-]*\s+){0,3}?" + _UNIT_RE + r")\b",
    re.I,
)
_NEQ_RE = re.compile(r"\bn\s*=\s*(" + _NUM_PAT + r")", re.I)

# Exclusion counts: the flow account's other column is a promise about these,
# so a count of rows removed should appear there too.
_EXCL_RE = re.compile(
    r"\b(?:taking|drops?|dropping|dropped|excludes?|excluding|removes?|"
    r"removing|affects?|omits?|omitting|discards?)\s+"
    r"(?:a\s+further\s+|the\s+|its\s+)?"
    r"(" + _NUM_PAT + r")\s+"
    r"((?:[a-z][a-z-]*\s+){0,3}?" + _UNIT_RE + r")\b",
    re.I,
)
_EXCL_COORD_RE = re.compile(
    r"\band\s+(\d+)\s+(?:from|in|for)\s+the\b")

# A bare count is a load-bearing denominator only when a statistic is computed
# on it in the same sentence.  Otherwise it is narrative arithmetic, and the
# flow account does not promise to derive it.
_STAT_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:per cent|%)|\bp\s*[=<>]|\b95 per cent\b|\bCI\b|"
    r"\bodds ratio\b|\bAUC\b|\barea under the curve\b", re.I)

# Deposits the flow account does not cover.
_OUT_OF_SCOPE = re.compile(
    r"kaur|windels|dubey|apramycin|amikacin|hollow[- ]fibre|evolved clone|"
    r"e\.\s*coli|escherichia|mcfarland", re.I)

# "the 140 series that cross", "the 32 flasks that fell below" -- a subset
# defined by its own outcome, not by an exclusion a flow account could list.
_RELCLAUSE_RE = re.compile(r"\s+(?:that|which|whose|who)\s")

# A count set against an "A of B <unit>" proportion but given no base of its
# own: "121 of 203 isolates lack the headroom ... where 31 do".  _DENOM_RE
# captures the DENOMINATOR -- the number after the preposition, with a unit
# noun behind it -- so a numerator written bare produces no candidate at all
# and is never tested against anything.  Existence in the flow account is no
# defence here: 31 is a real count on the 203 base, but nothing in the
# sentence says so, and the reader cannot tell 203 from 217.
_BARE_COUNT_RE = re.compile(
    r"\b(?:where|while|whereas|against|versus|compared with|but|and)\s+"
    r"(" + _NUM_PAT + r")\s+"
    r"(?:do|does|did|are|is|was|were|lacks?|falls?|sits?|rests?|reach(?:es)?)\b"
    r"(?!\s+(?:of|out of)\b)",
    re.I,
)


def _flow_values(tab: dict) -> set[int]:
    grid = tab["grid"]
    header = [c.lower() for c in grid[0]]
    i_n = next((i for i, h in enumerate(header) if h == "n"), None)
    if i_n is None:
        i_n = next(i for i, h in enumerate(header) if h.startswith("n"))
    i_ex = next((i for i, h in enumerate(header) if "exclud" in h), None)
    vals: set[int] = set()
    for row in grid[1:]:
        if len(row) <= i_n:
            continue
        m = _NUM_RE.fullmatch(row[i_n].strip())
        if m:
            vals.add(_int(m.group(0)))
        if i_ex is not None and len(row) > i_ex:
            m2 = re.fullmatch(r"-?\s*(\d[\d   ,]*)", row[i_ex].strip())
            if m2:
                vals.add(_int(m2.group(1)))
    return vals


def _flow_rows(tab: dict) -> list[tuple[str, str, int, int | None]]:
    """(deposit, panel, n, excluded) for every stage row of the flow account."""
    grid = tab["grid"]
    header = [c.lower() for c in grid[0]]
    i_n = next((i for i, h in enumerate(header) if h == "n"), None)
    if i_n is None:
        i_n = next(i for i, h in enumerate(header) if h.startswith("n"))
    i_ex = next((i for i, h in enumerate(header) if "exclud" in h), None)
    i_dep = 0
    i_pan = 1 if len(header) > 1 else 0
    out = []
    for row in grid[1:]:
        if len(row) <= i_n:
            continue
        m = _NUM_RE.fullmatch(row[i_n].strip())
        if not m:
            continue
        ex = None
        if i_ex is not None and len(row) > i_ex:
            m2 = re.fullmatch(r"-?\s*(\d[\d   ,]*)", row[i_ex].strip())
            if m2:
                ex = _int(m2.group(1))
        out.append((row[i_dep].strip(), row[i_pan].strip(),
                    _int(m.group(0)), ex))
    return out


def _check_flow_arithmetic(tnum: str, rows) -> list[dict]:
    """Each recorded exclusion must join two stages of the same panel.

    The flow account is the standard every other denominator is measured
    against, so its own chain is checked rather than taken on faith: a stage
    that removes k rows must have a sibling stage, in the same deposit and the
    same panel, holding exactly k more.
    """
    findings = []
    for dep, pan, n, ex in rows:
        if not ex:
            continue
        siblings = {v for d, p, v, _ in rows if d == dep and p == pan}
        if n + ex in siblings:
            continue
        findings.append({
            "severity": "high",
            "kind": "flow-table-arithmetic",
            "where": f"Table {tnum}",
            "detail": (
                f"A stage of the flow account for the {dep} {pan} panel "
                f"reports n = {n} after excluding {ex}, but no stage of that "
                f"panel holds {n + ex}, so the exclusion joins nothing."),
            "expected": f"a stage of that panel with n = {n + ex}",
            "found": f"n = {n}, excluded {ex}",
        })
    return findings


def _unit_key(unit: str) -> str:
    """Normalise a unit phrase to a singular head noun, for display."""
    if unit == "n =" or unit.startswith("n column of Table"):
        return unit
    u = re.sub(r"\([^)]*\)", " ", unit.lower())
    u = u.split(" of ")[0]
    u = re.sub(r"[^a-z\- ]", " ", u).strip()
    words = [w for w in u.split() if w]
    head = words[-1] if words else unit.strip().lower()
    if head == "series":
        return head
    if head.endswith("ies"):
        head = head[:-3] + "y"
    elif head.endswith("s") and not head.endswith("ss"):
        head = head[:-1]
    return head or "count"


def _check_denominators(ms: Manuscript) -> list[dict]:
    num, tab = ms.table_by_header("stage", "exclud")
    if tab is None:
        return [{
            "severity": "medium",
            "kind": "flow-table-missing",
            "where": "manuscript",
            "detail": "No analysis-flow table (a Stage / n / Excluded account) "
                      "was found, so denominators could not be traced.",
        }]
    traced = _flow_values(tab)
    rows = _flow_rows(tab)
    flow_lines = set(range(tab["line"], tab["line"] + len(tab["grid"]) + 4))

    # exclusion counts the flow account actually records, by panel label, and
    # the cumulative reductions a panel's stages imply
    excl_by_panel: dict[str, set[int]] = {}
    n_by_panel: dict[str, set[int]] = {}
    for _dep, pan, n, ex in rows:
        n_by_panel.setdefault(pan, set()).add(n)
        if ex:
            excl_by_panel.setdefault(pan, set()).add(ex)
    all_excl = {e for s in excl_by_panel.values() for e in s}
    cumulative = {a - b for s in n_by_panel.values() for a in s for b in s
                  if a > b}
    panels = [p for p in n_by_panel if re.search(r"[a-z0-9]", p, re.I)
              and p != "-"]

    def _panel_after(text: str, pos: int) -> str | None:
        """The flow account's panel label named just after an exclusion arm."""
        window = text[pos:pos + 60].lower()
        for p in panels:
            if p.lower() in window:
                return p
        return None

    findings_pre = _check_flow_arithmetic(num, rows)

    # value, unit, line, context, panel (panel only for exclusion arms)
    cands: list[tuple[int, str, int, str, str | None]] = []

    # -- prose, table legends and figure legends --------------------------
    for lineno, block in ms.blocks:
        if lineno in flow_lines:
            continue
        btxt = _plain(_normalise(block))
        if btxt.lstrip().startswith("|"):
            continue                    # grids are handled column-wise below
        para_ints = {_int(m.group(0)) for m in _NUM_RE.finditer(btxt)}
        for m in _NEQ_RE.finditer(btxt):
            v = _int(m.group(1))
            if v in traced or _OUT_OF_SCOPE.search(_sentence(btxt, m.start())):
                continue
            cands.append((v, "n =", lineno, _ctx(btxt, m.start()), None))
        for m in _EXCL_RE.finditer(btxt):
            sent = _sentence(btxt, m.start())
            if _OUT_OF_SCOPE.search(sent):
                continue
            unit = re.sub(r"\s+", " ", m.group(2).strip().lower())
            arms = [(_int(m.group(1)), m.start(), m.end(), False)]
            # "taking 14 rows from the 15-day panel and 20 from the 60-day":
            # the second arm is the same exclusion cause applied to the other
            # panel, so it must be a single recorded exclusion of that panel
            for c in _EXCL_COORD_RE.finditer(btxt, m.end(), m.end() + 120):
                arms.append((_int(c.group(1)), c.start(), c.end(), True))
            for v, pos, end, coordinated in arms:
                pan = _panel_after(btxt, pos)
                if pan is not None:
                    # the sentence names the panel, so the count is checked
                    # against that panel's own exclusions rather than against
                    # any number anywhere in the account
                    if v in excl_by_panel.get(pan, set()):
                        continue
                    if not coordinated and v in cumulative:
                        continue    # a cumulative reduction, not one stage
                    cands.append((v, "excluded " + unit, lineno,
                                  _ctx(btxt, pos), pan))
                    continue
                if v in all_excl or v in cumulative or v in traced:
                    continue
                cands.append((v, "excluded " + unit, lineno,
                              _ctx(btxt, pos), None))
        for m in _DENOM_RE.finditer(btxt):
            v = _int(m.group(1))
            if v in traced:
                continue
            sent = _sentence(btxt, m.start())
            if _OUT_OF_SCOPE.search(sent) or not _STAT_RE.search(sent):
                continue
            if any(v + o in traced for o in para_ints if o != v):
                continue            # one arm of a split that sums to a traced n
            if _RELCLAUSE_RE.match(btxt[m.end():m.end() + 24]):
                continue            # an outcome-defined subset, not an
                                    # exclusion the flow account could list
            unit = re.sub(r"\s+", " ", m.group(2).strip().lower())
            cands.append((v, unit, lineno, _ctx(btxt, m.start()), None))
        # a numerator quoted with no base of its own, in a sentence that has
        # already shown the reader an "A of B <unit>" pair.  This one cannot
        # go through `cands`: the collapse there is keyed on whether the value
        # is a traced flow number, and the defect is the missing denominator,
        # not the value.
        for m in _BARE_COUNT_RE.finditer(btxt):
            sent = _sentence(btxt, m.start())
            if _OUT_OF_SCOPE.search(sent) or not _DENOM_RE.search(sent):
                continue
            findings_pre.append({
                "severity": "medium",
                "kind": "count-without-a-stated-denominator",
                "where": f"line {lineno}",
                "detail": (
                    f"The count {m.group(1)} is set against a stated "
                    f"'A of B' proportion in the same sentence but is given "
                    f"no denominator of its own, so which set it counts is "
                    f"left to the reader to guess."),
                "expected": f"'{m.group(1)} of <denominator> <unit>'",
                "found": _ctx(btxt, m.start()),
            })

    # -- explicit n columns of every table --------------------------------
    for tnum, t in ms.tables.items():
        if tnum == num or not t["grid"]:
            continue
        header = [c.lower() for c in t["grid"][0]]
        try:
            i_n = header.index("n")
        except ValueError:
            continue
        body: list[tuple[list[str], int]] = []
        totals: list[tuple[list[str], int]] = []
        for row in t["grid"][1:]:
            if len(row) <= i_n or not _NUM_RE.fullmatch(row[i_n].strip()):
                continue
            label = " ".join(row[:i_n]).lower()
            target = totals if re.search(r"\ball\b|total|pooled", label) else body
            target.append((row, _int(row[i_n].strip())))
        # a column whose parts sum to a traced total decomposes that total
        if body and sum(v for _, v in body) in traced:
            continue
        for row, v in body + totals:
            if v in traced or _OUT_OF_SCOPE.search(" ".join(row)):
                continue
            cands.append((v, f"n column of Table {tnum}", t["line"],
                          f"Table {tnum}: " + " | ".join(row)[:150], None))

    # -- the audit table's 'units treated as independent' column ----------
    anum, atab = ms.table_by_header("verdict", "units treated as independent")
    if atab is not None:
        header = [c.lower() for c in atab["grid"][0]]
        i_u = next(i for i, h in enumerate(header)
                   if "units treated as independent" in h)
        for row in atab["grid"][1:]:
            if len(row) <= i_u:
                continue
            cell = _normalise(row[i_u].strip())
            m = re.match(r"(" + _NUM_PAT + r")(?:\s*\+\s*(\d+))?\s+(.*)", cell)
            if not m:
                continue
            rest = _normalise(" ".join(row))
            for part in [m.group(1)] + ([m.group(2)] if m.group(2) else []):
                v = _int(part)
                if v in traced or v < 10:
                    continue
                # a stacked set -- "420 isolate-panel", two panels of the same
                # 210 isolates -- is traced when its factor is a stage and is
                # named in the same row, the way "217 + 210" already is
                if any(v == k * t
                       for t in traced if t > 1
                       for k in (2, 3, 4)
                       if v == k * t and _number_in(str(t), rest)):
                    continue
                cands.append((v, m.group(3).strip().lower(), atab["line"],
                              f"Table {anum}, units column: '{cell}'", None))

    # -- collapse to one finding per value --------------------------------
    seen: dict[int, dict] = {}
    for v, unit, lineno, ctx, pan in cands:
        rec = seen.setdefault(
            v, {"lines": [], "ctx": [], "units": [], "sources": [],
                "raw_units": [], "panel": None})
        rec["raw_units"].append(unit)
        if pan and not rec["panel"]:
            rec["panel"] = pan
        rec["lines"].append(lineno)
        rec["ctx"].append(ctx)
        key = _unit_key(unit)
        bucket = "units" if not (key == "n =" or key.startswith("n column"))             else "sources"
        if key not in rec[bucket]:
            rec[bucket].append(key)

    findings: list[dict] = list(findings_pre)
    for v, rec in sorted(seen.items()):
        lines = sorted(set(rec["lines"]))
        unit = "/".join(rec["units"] or rec["sources"] or ["count"])
        is_excl = all(u.startswith("excluded ") for u in rec["raw_units"])
        if is_excl:
            pan = rec["panel"] or "that panel"
            detail = (
                f"An exclusion of {v} is attributed to a named cause in the "
                f"{pan} panel, but Table {num} records no such exclusion "
                f"there; its exclusions for that panel are "
                f"{sorted(excl_by_panel.get(rec['panel'], all_excl))}.")
            expected = f"an exclusion of {v} in the {pan} panel of Table {num}"
        else:
            detail = (
                f"A count of {v} ({unit}) is quoted, but no stage of the "
                f"analysis-flow table (Table {num}) has that n or that "
                f"exclusion count, so the flow account cannot say which set "
                f"it is.")
            expected = f"an n of {v} among the stages of Table {num}"
        findings.append({
            "severity": "medium",
            "kind": ("exclusion-not-in-flow-table" if is_excl
                     else "denominator-not-in-flow-table"),
            "where": "line " + ", ".join(str(x) for x in lines[:4]),
            "detail": detail,
            "expected": expected,
            "found": " || ".join(dict.fromkeys(rec["ctx"]))[:280],
        })
    return findings


# --------------------------------------------------------------------------
# (c) cross-reference resolution
# --------------------------------------------------------------------------

_TABLE_REF_RE = re.compile(
    r"\bTables?\s+(S?\d+(?:\s*(?:,|and|,\s*and)\s*S?\d+)*)")
_FIG_REF_RE = re.compile(r"\b(?:Fig\.|Figure)\s*(\d+)([A-Z])?\b")
_BOX_REF_RE = re.compile(r"\bBox\s+(\d+)\b")
_SEC_REF_RE = re.compile(
    r"\bSections?\s+(\d+(?:\s*(?:,|and|,\s*and)\s*\d+)*)"
    r"(\s+of\s+the\s+(?:Methods|Discussion|Introduction|Results|Supplement\w*))?",
    re.I)
_METHODS_SEC_RE = re.compile(
    r"\b(?:the\s+)?Methods,?\s+[Ss]ection\s+(\d+)|\bMethods\s+§\s*(\d+)")
_DESCRIBED_IN_RE = re.compile(
    r"((?:[a-z][\w-]*\s+){1,6}?)"
    r"(?:described|defined|derived|given|set out|stated|specified|"
    r"introduced|explained)\s+in\s+Sections?\s+(\d+)")


def _check_crossrefs(ms: Manuscript) -> list[dict]:
    findings: list[dict] = []
    n_sections = max(ms.results_sections) if ms.results_sections else 0

    for lineno, block in ms.blocks:
        btxt = _plain(_normalise(block))
        head = btxt.lstrip()
        is_tab_caption = bool(re.match(r"Table\s+S?\d+[.:]", head))
        is_fig_caption = bool(re.match(r"Figure\s+\d+[.:]", head))
        is_box_caption = bool(re.match(r"Box\s+\d+[.:]", head))

        # ---- tables ----
        for m in _TABLE_REF_RE.finditer(btxt):
            if is_tab_caption and m.start() < 8:
                continue                       # the caption defining the table
            for tok in re.findall(r"S?\d+", m.group(1)):
                if tok not in ms.tables:
                    findings.append({
                        "severity": "high",
                        "kind": "dangling-table-reference",
                        "where": f"line {lineno}",
                        "detail": f"Reference to Table {tok}, which the "
                                  f"manuscript never defines.",
                        "expected": f"a caption '**Table {tok}.**'",
                        "found": _ctx(btxt, m.start()),
                    })

        # ---- figures ----
        if not head.startswith("!["):
            for m in _FIG_REF_RE.finditer(btxt):
                fnum, panel = m.group(1), m.group(2)
                if is_fig_caption and m.start() < 10:
                    continue
                if fnum not in ms.figures:
                    findings.append({
                        "severity": "high",
                        "kind": "dangling-figure-reference",
                        "where": f"line {lineno}",
                        "detail": f"Reference to Figure {fnum}, which has no "
                                  f"legend.",
                        "expected": f"a legend '**Figure {fnum}.'",
                        "found": _ctx(btxt, m.start()),
                    })
                elif (panel and ms.figures[fnum]["panels"]
                        and panel not in ms.figures[fnum]["panels"]):
                    have = ", ".join(sorted(ms.figures[fnum]["panels"]))
                    findings.append({
                        "severity": "medium",
                        "kind": "dangling-figure-panel",
                        "where": f"line {lineno}",
                        "detail": (f"Reference to panel {panel} of Figure "
                                   f"{fnum}, whose legend defines only {have}."),
                        "expected": f"panel {panel} in the Figure {fnum} legend",
                        "found": _ctx(btxt, m.start()),
                    })

        # ---- boxes ----
        for m in _BOX_REF_RE.finditer(btxt):
            if is_box_caption and m.start() < 6:
                continue
            if m.group(1) not in ms.boxes:
                findings.append({
                    "severity": "high",
                    "kind": "dangling-box-reference",
                    "where": f"line {lineno}",
                    "detail": f"Reference to Box {m.group(1)}, which does not "
                              f"exist.",
                    "expected": f"a caption '**Box {m.group(1)}.'",
                    "found": _ctx(btxt, m.start()),
                })

        # ---- sections ----
        for m in _SEC_REF_RE.finditer(btxt):
            nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
            qualifier = (m.group(2) or "").strip().lower()
            if qualifier.endswith("methods"):
                findings.append(_methods_section_finding(
                    ms, lineno, m.group(0).strip(), _ctx(btxt, m.start())))
                continue
            for v in nums:
                if v not in ms.results_sections:
                    findings.append({
                        "severity": "high",
                        "kind": "dangling-section-reference",
                        "where": f"line {lineno}",
                        "detail": (f"Reference to Section {v}; the manuscript's "
                                   f"numbered sections run 1 to {n_sections}."),
                        "expected": f"a numbered section {v}",
                        "found": _ctx(btxt, m.start()),
                    })

        for m in _METHODS_SEC_RE.finditer(btxt):
            findings.append(_methods_section_finding(
                ms, lineno, m.group(0).strip(), _ctx(btxt, m.start())))

        # ---- 'X described in Section N' where Section N never mentions X ----
        for m in _DESCRIBED_IN_RE.finditer(btxt):
            subject, snum = m.group(1), int(m.group(2))
            if snum not in ms.results_sections:
                continue                       # already reported above
            keys = _content_words(subject)
            if not keys:
                continue
            tgt = set(_content_words(ms.results_sections[snum][2]))
            if not any(k in tgt for k in keys):
                phrase = re.sub(r"\s+", " ", m.group(0).strip())
                findings.append({
                    "severity": "high",
                    "kind": "misdirected-section-reference",
                    "where": f"line {lineno}",
                    "detail": (
                        f"'{phrase}' points at Results Section {snum}, which "
                        f"never mentions {'/'.join(keys)}; the Methods "
                        f"subsections that do are unnumbered, so the pointer "
                        f"resolves to the wrong place."),
                    "expected": f"Section {snum} to describe "
                                f"'{subject.strip()}'",
                    "found": _ctx(btxt, m.start(), 170),
                })

    # de-duplicate identical findings raised twice by overlapping patterns
    out: list[dict] = []
    seen: set[tuple] = set()
    for f in findings:
        key = (f["kind"], f["where"], f.get("expected"), f.get("found"))
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out


def _methods_section_finding(ms: Manuscript, lineno: int, phrase: str,
                             ctx: str) -> dict:
    return {
        "severity": "high",
        "kind": "dangling-section-reference",
        "where": f"line {lineno}",
        "detail": (
            f"'{phrase}' cannot resolve: the Methods subsections are "
            f"unnumbered ({len(ms.methods_subsections)} of them, each titled "
            f"rather than numbered)."),
        "expected": "a numbered Methods subsection, or a reference by title",
        "found": ctx,
    }


# --------------------------------------------------------------------------
# (d) superseded passages left in place
# --------------------------------------------------------------------------

def _sentences(block: str) -> list[str]:
    flat = re.sub(r"\s+", " ", _plain(_normalise(block)))
    return [s.strip() for s in re.split(r"(?<=[.!?]) +", flat) if s.strip()]


def _check_superseded(ms: Manuscript) -> list[dict]:
    """A rewrite that leaves its predecessor in place repeats itself.

    The withdrawn-claim check above can only see conclusions the self-audit
    table lists as NOT SUPPORTED.  A reading retracted in the prose alone --
    'that agreement is an identity rather than a passed test' -- is outside
    its universe, and the sentence that reasserts the retracted reading may
    carry no number for the numeric fingerprint to catch.  What a leftover
    passage does carry is a near-duplicate of the text that replaced it, so
    look for that instead.
    """
    findings: list[dict] = []
    for lineno, block in ms.blocks:
        if _plain(_normalise(block)).lstrip().startswith("|"):
            continue
        if _CAPTION_RE.match(block):
            continue
        sents = _sentences(block)
        bags = [set(_content_words(s)) for s in sents]
        for i, bag_i in enumerate(bags):
            if len(bag_i) < 6:
                continue
            for j in range(i + 1, len(bags)):
                bag_j = bags[j]
                if len(bag_j) < 6:
                    continue
                overlap = len(bag_i & bag_j) / len(bag_i | bag_j)
                if overlap < 0.70:
                    continue
                findings.append({
                    "severity": "high",
                    "kind": "superseded-passage-left-in-place",
                    "where": f"line {lineno}",
                    "detail": (
                        "Two sentences in one block say the same thing, which "
                        "is what a paragraph looks like when the passage its "
                        "rewrite replaced was never deleted.  Check whether "
                        "the later one reasserts a reading the earlier one "
                        "retracts."),
                    "expected": "one statement of the claim, in its revised form",
                    "found": f"{sents[i][:150]} || {sents[j][:150]}",
                })
    return findings


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
    findings = (_check_self_audit(ms)
                + _check_denominators(ms)
                + _check_crossrefs(ms)
                + _check_superseded(ms))
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 3), f["kind"]))
    return findings


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(__file__).resolve().parents[2]
    paper = Path(argv[0]) if argv else root / "manuscript" / "PAPER_COMPLETE.md"
    text = paper.read_text(encoding="utf-8")
    ctx = {"root": root}
    for key, rel in (("tables", "manuscript/tables.md"),
                     ("prose", "manuscript/RATE_VS_DURATION.md")):
        path = root / rel
        ctx[key] = path.read_text(encoding="utf-8") if path.exists() else ""
    findings = check(text, ctx)
    print(f"check_consistency on {paper}")
    if not findings:
        print("  clean (0 findings)")
        return 0
    print(f"  {len(findings)} finding(s)\n")
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
