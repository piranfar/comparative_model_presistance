"""WALLER2023 -- figshare file 39444559.xlsx, the figure Source Data workbook
for Waller, Cheung, Cook and McNeil, Nat Commun 2023;14:1517 (PMC10024696).

Eleven sheets, one per figure or supplementary figure, each holding several
panel-lettered blocks stacked vertically with a blank row between them.  A block
is introduced by its panel letter in a cell of its own ("A", "E", "A/B/C/D"),
then a header row whose first cell is "Time (days)" (or "Day", or "Time
(Days)"), then a row of "Rep 1"/"Rep 2" labels, then one row per sampling day.
Column labels sit above each pair of replicate columns.

WHAT IS READ.  Every block whose row index is a time.  There are twenty-six of
them and they are found by looking for the header, not by hard-coded addresses:

    Figure 4      E F G H J K L        counts, 5-6 days each, WT vs mutants
    Figure 6      A/B/C/D              counts, 9 days, ten labelled drug arms
    Figure 6      E F G H              counts, 6 days, WT vs INH-1
    Supplementary 4  A B               counts, 9 days, four labelled drug arms
    Supplementary 5  E F G H           counts, 4-6 days, WT vs mutants
    Figure 3      E F G H              NOT counts (see below)
    Supplementary 5  A B C D           NOT counts (see below)

This is a good deal more than the repository's own sweep note found, which
reported the Figure 6 sheet only.  Figure 4 alone carries seven count blocks.

WHAT IS NOT READ, and why.  Figure 1 (a drug-by-mutant matrix of log2 fold MIC
changes), Figures 2, 3A-D and Supplementary 1 and 3 (per cent growth against
concentration), Figure 5 (per cent growth at 1x/3x/9x MIC), Figure 4 A-D and
Supplementary 2 (colony counts against CONCENTRATION, with a single "Day 0" row
for the inoculum and no second timepoint, so there is no time axis to put them
on), and Figure 4 I and Figure 6 I and J (frequency of resistance, one number
per replicate, no time).

TWO BLOCK TYPES, TOLD APART BY THEIR NUMBERS, NOT BY THEIR PANEL LETTER.  The
count blocks run from 200 to 2e7.  Figure 3 E-H and Supplementary 5 A-D run from
0.005 to 1.28 and are plainly not colony counts.  The reader classifies a block
as a non-count block when every value in it is below 100, keeps the value in
notes, and leaves cfu_per_ml BLANK -- an unlabelled small number is never
converted into a density.  (The article's Methods say OD600 was measured on the
same days; that sentence is outside this deposit and the sheets never write
"OD", so `readout` says only that the quantity is not a count and is unlabelled.)

THE FLOOR IS NOT IN THIS DEPOSIT, and that is the finding.  The workbook writes
no limit, no plated volume, no dilution factor and no raw colony count anywhere
in its eleven sheets; the reader searches every cell of every sheet for all four
and reports in floor_basis what it searched for and did not find.  So
floor_cfu_per_ml is blank on every row.

  What the workbook does show, and what belongs to src.infer_floor rather than
  here, is that 200 is the smallest number in the file, that it recurs exactly
  many times, that nothing lies below it, and that it is sustained for weeks in
  single replicates while the paired replicate regrows.

  The repository's sweep derives 200 CFU/mL from the ARTICLE's Methods, and that
  derivation was checked here against the article rather than taken on trust.
  The "Killing kinetics" section says the samples were "diluted and spotted as
  described above for MBC", and the MBC section says "5 uL of each dilution was
  spotted onto 7H11 supplemented with OADC, leucine and pantothenate acid" after
  "a 3-point, 10-fold dilution curve in 7H9 with pantothenic acid and leucine".
  One colony in a 5 uL spot of the undiluted sample is 200 per mL, which is
  exactly the minimum the workbook shows.  That text is outside this deposit, so
  the number is quoted in floor_basis and deliberately NOT written into
  floor_cfu_per_ml -- the same line read_YANG2024_PHAGE takes.

WHAT ELSE THE WORKBOOK DOES NOT SAY, all left blank rather than imported.

  * THE ORGANISM.  The word tuberculosis does not appear in the file.  The
    manifest and the article name M. tuberculosis mc2 6206; neither is
    transcribed, per the schema's rule.

  * THE DRUG, for twenty of the twenty-six time blocks.  Only Figure 6 A/B/C/D
    and Supplementary 4 A and B label their columns with a condition ("DMSO",
    "Q203 0.3x MIC", "INH 9x MIC", "PA824 0.3x MIC + INH 9x MIC", ...).  Every
    other time block labels its columns with a STRAIN and identifies its
    condition only by the panel letter, which points into a figure legend that
    is not in the deposit.  Those rows therefore carry a blank `drug`, and their
    notes say in as many words that blank means NOT STATED and not untreated.
    The article's Figure 6 legend does name a drug per panel; it is outside the
    deposit and is not transcribed.

  * WHETHER "Rep 1" AND "Rep 2" ARE BIOLOGICAL OR TECHNICAL.  The workbook does
    not say, so they go into `replicate` verbatim and tech_replicate stays blank.
    `replicate` is prefixed with the sheet and panel because the same labels
    ("WT", "Rep 1") recur in every block of every sheet and the blocks are
    different experiments; without the prefix a downstream group-by would fuse
    twenty-six experiments into a handful of series.

  * THE UNIT of the counts.  The sheets never write "CFU" or "per mL".  The
    numbers are carried into cfu_per_ml, which is the only numeric column the
    schema has for a density, and `readout` says the unit is not stated.

TWO THINGS WORTH KNOWING BEFORE MODELLING THESE CURVES.

  * A CEILING.  20000000 recurs as a saturating maximum, and in Figure 6 F and
    Supplementary 5 F the maximum is 10000000 instead.  Readings sitting on it
    are at an upper reporting limit, not measured densities.  The schema has no
    ceiling column, so every row that sits on its block's saturating maximum
    says so in notes and the count is reported by the reader.

  * BELOW-LIMIT READINGS ARE WRITTEN AS THE FLOOR VALUE ITSELF, 200, not as a
    zero, a blank or a "<" string.  A run of 200s is therefore indistinguishable
    in the file from a genuine measurement of 200, and rows on the minimum say
    so in notes.

NO NEGATIVE TIMES anywhere: every block's day index starts at 0.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty

XLSX = "39444559.xlsx"

# A block's row index is a time when its header cell says so.
TIME_HDR = re.compile(r"^\s*(?:time\s*\(\s*days?\s*\)|days?)\s*$", re.I)
# A panel row is a single cell holding "A", "E" or "A/B/C/D".
PANEL_RE = re.compile(r"^[A-Z](?:\s*/\s*[A-Z])*$")
REP_RE = re.compile(r"^\s*rep\b", re.I)
# "Q203 0.3x MIC", "INH 9x", "INH9x MIC", "I9x MIC", "PA824 0.3x MIC"
ARM_TOKEN = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9\-]*?)\s*([0-9]*\.?[0-9]+)\s*[xX]\s*(?:MIC)?\s*$")
CONTROL_RE = re.compile(r"^\s*(dmso|untreated|no drug|vehicle)\s*$", re.I)

# Below this, a block's numbers cannot be colony densities; see the docstring.
COUNT_THRESHOLD = 100.0

# What a floor would have to look like if this workbook stated one.
SEARCH = {
    "a detection or quantification limit":
        re.compile(r"limit of (?:detection|quantification)|detection limit|"
                   r"\bLOD\b|\bLLOQ\b|\bLOQ\b", re.I),
    "a plated or spotted volume":
        re.compile(r"\b\d+(?:\.\d+)?\s*(?:[uµμ]\s*[lL]\b|mL\b|ml\b)", re.I),
    "a dilution factor": re.compile(r"dilut", re.I),
    "a raw colony count": re.compile(r"colon", re.I),
}

FLOOR_QUOTE = (
    "The repository's sweep derives 200 CFU/mL for this study from the "
    "ARTICLE's Methods (PMC10024696), and the derivation was checked against "
    'the article rather than taken on trust: its "Killing kinetics" section '
    'says samples were "diluted and spotted as described above for MBC", and '
    'its MBC section says "5 uL of each dilution was spotted onto 7H11 '
    'supplemented with OADC, leucine and pantothenate acid" following "a '
    '3-point, 10-fold dilution curve in 7H9 with pantothenic acid and '
    'leucine". One colony in a 5 uL spot of the undiluted sample is 200 per '
    "mL, which is exactly the smallest number this workbook contains. That "
    "text is outside this deposit, so the number is quoted here and "
    "deliberately not written into floor_cfu_per_ml.")

NO_DRUG_NOTE = (
    "the workbook names no drug for this block: its columns are labelled with "
    "a strain and its condition is identified only by the panel letter, which "
    "points into a figure legend that is not in this deposit -- a blank drug "
    "here means NOT STATED, not untreated")

NO_UNIT_NOTE = ("the workbook never writes CFU or per mL; the number is "
                "carried in cfu_per_ml because that is the only numeric "
                "column the schema has, and its unit is not stated")

REP_NOTE = ("the workbook does not say whether Rep 1 and Rep 2 are biological "
            "or technical replicates, so they are carried verbatim and "
            "tech_replicate is left blank")

ORG_NOTE = ("the workbook names no organism anywhere in its eleven sheets, so "
            "organism is blank")


def _txt(v) -> str:
    return str(v).strip() if isinstance(v, str) else ""


def _num(v):
    if isinstance(v, (int, float, np.number)) and not pd.isna(v):
        return float(v)
    return None


def _search_all_sheets(book: dict[str, pd.DataFrame]) -> dict[str, str]:
    """What a floor would need, and whether any sheet says it.

    Checked in code so that floor_basis reports a search that actually ran,
    rather than an absence asserted from having glanced at one sheet.
    """
    found = {}
    for name, pat in SEARCH.items():
        hits = []
        for sheet, raw in book.items():
            for v in raw.values.ravel():
                if isinstance(v, str) and pat.search(v):
                    hits.append(f"{sheet}: {v.strip()[:60]}")
        if hits:
            found[name] = "; ".join(sorted(set(hits))[:3])
    return found


def _floor_basis(found: dict[str, str]) -> str:
    if found:
        got = "; ".join(f"{k} -> {v}" for k, v in found.items())
        return ("not recorded: the workbook does contain text matching " + got +
                ", which this reader did not expect and has not interpreted "
                "into a number. " + FLOOR_QUOTE)
    return (
        "not stated by this deposit. The reader searched every cell of all "
        "eleven sheets for " + ", ".join(SEARCH) + ", and found none of them: "
        "the workbook is bare numbers under panel letters. What it does show "
        "-- that 200 is its smallest value, recurs exactly, is never "
        "undercut, and is sustained for weeks in single replicates while the "
        "paired replicate regrows -- is evidence for src.infer_floor to "
        "weigh, not a floor the source states. " + FLOOR_QUOTE)


def _panel_above(raw: pd.DataFrame, hdr: int) -> str:
    """The panel letter introducing the block whose header row is `hdr`."""
    for i in range(hdr - 1, max(-1, hdr - 4), -1):
        cells = [_txt(v) for v in raw.iloc[i] if _txt(v)]
        if len(cells) == 1 and PANEL_RE.match(cells[0]):
            return cells[0]
    return ""


def _is_rep_row(raw: pd.DataFrame, i: int) -> bool:
    if i >= len(raw):
        return False
    return any(REP_RE.match(_txt(v)) for v in raw.iloc[i])


def _expand(name: str, siblings: set[str]) -> tuple[str, str]:
    """Expand a truncated drug name only against this header row's own labels.

    Figure 6 writes one arm "Q203 0.3x MIC + I9x MIC" while the three arms
    beside it write "... + INH9x MIC" and "... + INH 9x MIC".  "I" is expanded
    to "INH" only because "INH" is present in the SAME header row and is the
    only label there that "I" prefixes; the expansion is reported in notes so a
    reader who disagrees can undo it.
    """
    cands = {s for s in siblings
             if s.upper() != name.upper() and s.upper().startswith(name.upper())}
    if len(cands) == 1:
        full = cands.pop()
        return full, (f'the workbook writes this drug "{name}"; it is read as '
                      f'"{full}" because "{full}" appears in the same header '
                      f'row and is the only label there that "{name}" begins')
    return name, ""


def _condition(label: str, siblings: set[str]):
    """(drug, concentration, unit, note) for a column label, or None.

    None means the label is not a condition at all -- it is a strain name.
    """
    if CONTROL_RE.match(label):
        return "", np.nan, "", ""
    parts = [p.strip() for p in label.split("+") if p.strip()]
    hits = [ARM_TOKEN.match(p) for p in parts]
    if not parts or not all(hits):
        return None
    names, vals, notes = [], [], []
    for m in hits:
        nm, note = _expand(m.group(1), siblings)
        if note:
            notes.append(note)
        names.append(nm)
        vals.append(float(m.group(2)))
    if len(names) == 1:
        return names[0], vals[0], "xMIC", "; ".join(notes)
    notes.append("combination arm: the schema has one concentration column and "
                 "this arm has %d, so concentration is left blank and the "
                 "workbook's own label is kept in arm" % len(names))
    return " + ".join(names), np.nan, "", "; ".join(notes)


def _drug_names(labels: list[str]) -> set[str]:
    """Every bare drug name appearing in one header row, for _expand."""
    out = set()
    for lab in labels:
        for p in lab.split("+"):
            m = ARM_TOKEN.match(p.strip())
            if m:
                out.add(m.group(1))
    return out


def _shape(raw: pd.DataFrame, hdr: int):
    """(panel, rep_row, body rows, labels, values) for the block at `hdr`.

    None when the header does not introduce a usable block.
    """
    ncol = raw.shape[1]
    panel = _panel_above(raw, hdr)
    rep_row = hdr + 1 if _is_rep_row(raw, hdr + 1) else None

    body = []
    for r in range((rep_row if rep_row is not None else hdr) + 1, len(raw)):
        day = _num(raw.iat[r, 0])
        if day is None:
            break
        body.append((r, day))
    labels = [(c, _txt(raw.iat[hdr, c])) for c in range(1, ncol)
              if _txt(raw.iat[hdr, c])]
    if not body or not labels:
        return None
    every = [v for c in range(1, ncol) for v in
             [_num(raw.iat[r, c]) for r, _ in body] if v is not None]
    if not every:
        return None
    return panel, rep_row, body, labels, every


def _read_block(raw, sheet, hdr, floor_basis, workbook_min):
    ncol = raw.shape[1]
    shape = _shape(raw, hdr)
    if shape is None:
        return []
    panel, rep_row, body, labels, every = shape
    bounds = [c for c, _ in labels] + [ncol]
    siblings = _drug_names([lab for _, lab in labels])

    # Is this a block of counts, or of some much smaller unlabelled quantity?
    is_count = max(every) >= COUNT_THRESHOLD
    ceiling = max(every) if is_count else None
    floor_val = workbook_min if is_count else None

    rows = []
    for k, (lcol, label) in enumerate(labels):
        span = range(lcol, bounds[k + 1])
        cols = [c for c in span
                if any(_num(raw.iat[r, c]) is not None for r, _ in body)]
        declared = [c for c in span
                    if rep_row is not None and REP_RE.match(_txt(raw.iat[rep_row, c]))]
        blank_reps = [_txt(raw.iat[rep_row, c]) for c in declared if c not in cols]

        cond = _condition(label, siblings)
        if cond is None:
            drug, conc, unit, cnote = "", np.nan, "", NO_DRUG_NOTE
            strain, arm = label, label
        else:
            drug, conc, unit, cnote = cond
            strain, arm = "", label
            if not drug:
                cnote = ("the workbook labels this arm %r; it is a control "
                         "column and carries no drug" % label)

        for c in cols:
            rep = _txt(raw.iat[rep_row, c]) if rep_row is not None else ""
            rep = rep or f"col{c}"
            for r, day in body:
                v = _num(raw.iat[r, c])
                if v is None:
                    continue
                note = [cnote] if cnote else []
                if is_count:
                    if v >= ceiling:
                        note.append("this reading sits on the block's "
                                    "saturating maximum of %g, an upper "
                                    "reporting limit rather than a measured "
                                    "density; the schema has no ceiling "
                                    "column" % ceiling)
                    if v <= floor_val:
                        note.append("this reading sits on the smallest value "
                                    "anywhere in the workbook, %g; the file "
                                    "writes a below-limit reading as that "
                                    "value itself, not as a zero, a blank or "
                                    "a '<' string, so it cannot be told apart "
                                    "from a genuine measurement of %g"
                                    % (floor_val, floor_val))
                    note.append(NO_UNIT_NOTE)
                else:
                    note.append("value = %g. The schema has no column for a "
                                "non-count reading, so the value is kept here "
                                "and cfu_per_ml is left blank; the workbook "
                                "gives these numbers no unit and they are far "
                                "too small to be densities, so nothing is "
                                "converted" % v)
                if blank_reps:
                    note.append("the workbook declares %s for this arm but "
                                "leaves that column empty at every timepoint"
                                % " and ".join(repr(x) for x in blank_reps))
                note += [REP_NOTE, ORG_NOTE,
                         "source time in days, converted to hours"]
                rows.append({
                    "source_file": XLSX,
                    "sheet": sheet if not panel else f"{sheet} / {panel}",
                    "organism": "",
                    "strain": strain,
                    "drug": drug,
                    "concentration": conc,
                    "conc_unit": unit,
                    "arm": arm,
                    "replicate": f"{sheet}|{panel or '?'}|{rep}",
                    "tech_replicate": "",
                    "time_h": day * 24.0,
                    "colonies": np.nan,
                    "dilution": np.nan,
                    "plated_volume_ul": np.nan,
                    "cfu_per_ml": v if is_count else np.nan,
                    "floor_cfu_per_ml": np.nan,
                    "floor_basis": floor_basis if is_count else
                    ("not applicable: this block is not a colony count. Its "
                     "values run below %g and the workbook gives them no "
                     "unit, so no floor applies and none is recorded."
                     % COUNT_THRESHOLD),
                    "readout": ("count, unit not stated by the deposit"
                                if is_count else
                                "not a count, unit not stated by the deposit"),
                    "notes": "; ".join(note),
                })
    return rows


def read(d: Path) -> pd.DataFrame:
    src = d / XLSX
    if not src.exists():
        return empty()

    xl = pd.ExcelFile(src)
    book = {s: pd.read_excel(src, sheet_name=s, header=None)
            for s in xl.sheet_names}
    basis = _floor_basis(_search_all_sheets(book))

    # Every block whose row index is a time, found by its header rather than
    # by address.
    blocks = [(sheet, i) for sheet, raw in book.items() for i in range(len(raw))
              if TIME_HDR.match(_txt(raw.iat[i, 0]))]

    # The smallest count anywhere in the workbook, over the count blocks only,
    # taken in a first pass so that a row can say whether it sits on it.
    seen = []
    for sheet, i in blocks:
        shape = _shape(book[sheet], i)
        if shape and max(shape[4]) >= COUNT_THRESHOLD:
            seen += [v for v in shape[4] if v > 0]
    workbook_min = min(seen) if seen else np.nan

    rows = []
    for sheet, i in blocks:
        rows += _read_block(book[sheet], sheet, i, basis, workbook_min)
    if not rows:
        return empty()
    return pd.DataFrame(rows)
