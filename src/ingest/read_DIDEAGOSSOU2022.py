"""DIDEAGOSSOU2022 -- AAC supplementary of PMC9017352 (aac.02310-21-s0002.xlsx),
per-mouse lung burdens from three BALB/c M. tuberculosis efficacy experiments.

The deposit is a zip holding two files that matter: the workbook, and the
supplementary methods PDF `aac.02310-21-s0001.pdf`. Both are the source. The PDF
is parsed at run time rather than quoted from memory, because everything this
reader knows beyond the bare numbers -- the organism, Experiment 1's strain, and
Experiment 1's missing time axis -- comes out of it, and a revised deposit must
be able to change the answer.

WHAT THE WORKBOOK CONTAINS. Five sheets, no captions, no merged headers: the
entire text of the file is its column headings, its group labels, and one string
cell reading "<3.26086956521739". Three sheets carry counts:

  Experiment1 PD markers data   52 mice, groups UNTX PZA EMB STR RIF INH BDQ,
                                and NO time column at all
  Experiment2 PD markers data   44 mice, PreRx HRZE PMZ BMZ BMZRb, days 0/14/28
  Experiment3 PD markers data   90 mice, PreRx HRZE PaMZ BPaL BPaMZ,
                                days 0/7/14/21/28

The two "relapse data" sheets are NOT read: they give the proportion of mice
whose lungs were culture-positive after a drug holiday (15/15, 9/15, 0/15 ...),
an outcome per group rather than a viable count per animal.

THREE THINGS THE DEPOSIT DOES NOT SAY, and which are therefore blank here.

  * A DETECTION LIMIT, anywhere, for any experiment. The strings "limit of
    detection", "detection limit" and "LOD" occur in neither the workbook nor
    the methods PDF; that absence is established by searching both at run time,
    not from memory. What the methods do say is that Experiment 3's counts came
    from "serial dilutions of homogenates ... and plating on 7H11-OADC agar
    plates", with no volume and no dilution given, and that for Experiment 2
    "enumeration of CFU is described elsewhere (8)" -- an external reference,
    exactly the kind of pointer that cannot be turned into a floor here. So
    floor_cfu_per_ml is blank on 183 of the 186 rows.

  * THE EXCEPTION, and it is a real one. Three Experiment 3 cells (BPaMZ, day
    28) are not numbers but the string "<3.26086956521739". For those three
    readings the deposit states a bound, so they get floor_cfu_per_ml =
    3.26086956521739 and censored = yes, with cfu_per_ml left BLANK -- the file
    gives an inequality, not a count, and writing 3.26 into the count column
    would invent a measurement. The number is 75/23 to every digit the sheet
    prints (not exactly: 75/23 runs on 3.2608695652173913...), and the three
    positive counts in the same group and day are 3.26, 6.52 and 9.78, i.e.
    one, two and three times it: it is that block's one-colony equivalent, and
    those three rows say so in their notes without receiving a floor. It is NOT
    propagated further. Some counts elsewhere on the sheet are also consistent
    with a multiple of it and some are not -- the reader counts both at run time
    and puts the tally in the note -- but that is a weak test, because the sheet
    prints counts to three significant figures, and it cannot show that one
    block's quantum is the whole sheet's. Counts stepping in exact multiples of
    7.5 elsewhere in the same column say the per-mouse multiplier varies. So the
    bound stays where the deposit put it: on three cells.

  * DRUG DOSES AND REGIMEN EXPANSIONS. Experiment 1's six single drugs are
    expanded by the deposit itself (Table S1: "pyrazinamide (PZA), ethambutol
    (EMB), ..."), and those expansions are parsed out and used. The regimen
    codes of Experiments 2 and 3 -- HRZE, PMZ, BMZ, BMZRb, PaMZ, BPaL, BPaMZ --
    are never expanded anywhere in the deposit, so `drug` carries the code
    verbatim. Expanding them from the wider literature would be exactly the
    inference this corpus forbids. No dose or concentration is given for any
    arm, so `concentration` and `conc_unit` are blank throughout.

THE CFU COLUMN IS ON TWO DIFFERENT SCALES AND THE SHEET NEVER SAYS SO.
Experiments 1 and 2 head the column "CFU" and fill it with 0.74-7.42;
Experiment 3 heads it "CFU" and fills it with 3.26-2.06e7. The first two are
log10 and the third is linear, and this reader demonstrates that at run time
rather than assuming it: Experiment 1's values antilog to whole numbers sharing
a common factor of 15, and Experiment 2's pre-treatment values fall inside the
log10 of Experiment 3's pre-treatment counts. Both measurements are written into
the notes of every row they justify, so if a future revision breaks them the
note stops supporting the reading.

EXPERIMENT 1 HAS NO TIME COLUMN. Its 52 mice carry a group label and nothing
else. The deposit's own methods supply the design -- "Treatment was initiated on
day 11 post aerosol and continued for 4 (3) weeks" and "Groups of 6 mice were
individually euthanized ... on day 11, prior to treatment initiation, and on the
last day of treatment" -- so UNTX is the pre-treatment sacrifice (time zero of
treatment) and the six drug groups are the end-of-treatment sacrifice. Both
sentences must match, and agree on the day, before any Experiment 1 time is
filled; if either fails, time_h stays blank and the note says why. The "(3)"
inside "4 (3) weeks" is a citation, not a second duration: reference 3 of that
same PDF is Walter et al. 2021 Nat Commun 12:2899.

WHICH BRINGS US TO THE OVERLAP, and it is large. Reference 3 is the deposit
WALTER2021_RSRATIO in this corpus, and Experiments 1 and 3 are re-depositions of
its source data:

  * all 52 Experiment 1 rows reappear in Walter's "Fig 4a-c & Sup Fig 7-8", an
    80-row sheet that also carries the mouse number, the drug DOSE (RIF 10, INH
    25, BDQ 25 ...), "Days of treatment" and "Day of sacrifice";
  * all 90 Experiment 3 rows reappear in Walter's "Fig 5a-d & Sup Fig 9-10", a
    335-row sheet, restricted here to the pre-treatment and on-treatment
    animals -- Walter's censored cells read "<3.26", this deposit's read
    "<3.26086956521739";
  * Experiment 2 (Johns Hopkins) matches nothing in Walter and is new data.

So the re-deposition dropped Experiment 1's time axis and every dose, and gained
precision on the censoring bound. THE OVERLAP IS MEASURED AT RUN TIME against
the sibling directory and reported per row; nothing is imported from it. In
particular Experiment 1's times come from this deposit's own methods text and
not from Walter's "Days of treatment" column, even though the two agree, because
filling a field from another deposit is the one thing a reader here may not do.
If WALTER2021_RSRATIO is absent or has changed shape, the check says so on every
row instead of failing.
"""
from __future__ import annotations

import math
import re
import zipfile
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty

BOOK = "_unpacked/PMC9017352_supplementary/aac.02310-21-s0002.xlsx"
ZIP = "PMC9017352_supplementary.zip"
METHODS_PDF = "aac.02310-21-s0001.pdf"
TWIN = "WALTER2021_RSRATIO"

COUNT_SHEETS = ("Experiment1 PD markers data",
                "Experiment2 PD markers data",
                "Experiment3 PD markers data")

READOUT = ("CFU per mouse lung (left and lower right lobes, per the deposit's "
           "supplementary methods; the denominator is an organ, NOT a mL)")

ORGAN = ("in vivo organ burden: the count is per mouse lung and sits in "
         "cfu_per_ml only because the schema has no per-organ column -- it is "
         "not a concentration, and no volume was invented to make it one")

NO_ID = ("the deposit gives no mouse identifier and each mouse is sacrificed "
         "once, so no animal is followed over time; replicate is the "
         "experiment and the 1-based data row of its sheet, which locates the "
         "reading in the file and keeps the three experiments apart")

NO_PLATING = ("the deposit states no plated volume, no dilution and no raw "
              "colony count for any of its experiments")

FLOOR_ABSENT = (
    'no reporting floor anywhere in this deposit: neither "limit of '
    'detection" nor "detection limit" nor "LOD" occurs in the workbook or in '
    "its supplementary methods, the methods give Experiment 3's plating with "
    "no volume and no dilution, and Experiment 2's CFU enumeration is referred "
    "to an external publication")

FLOOR_STATED = ('stated in the sheet: the cell itself reads "%s", which bounds '
                "this reading above in CFU per lung; it is the only floor "
                "statement anywhere in the deposit, and it bounds this cell, "
                "not the column")

RELAPSE = ('this deposit\'s two "relapse data" sheets are not read: they give '
           "the proportion of mice culture-positive after a drug holiday, an "
           "outcome per group rather than a viable count per animal")

# "Treatment was initiated on day 11 post aerosol and continued for 4 (3) weeks."
# The parenthesised number is a citation; it is captured so the note can quote
# the sentence exactly as the deposit prints it.
EXP1_LEN = re.compile(
    r"Treatment was initiated on day\s+(\d+)\s+post aerosol and continued "
    r"for\s+(\d+)\s*(\(\s*\d+\s*\))?\s*weeks", re.I)
# "Groups of 6 mice were individually euthanized by CO2 narcosis on day 11,
#  prior to treatment initiation, and on the last day of treatment"
EXP1_SAC = re.compile(
    r"euthanized[^.]{0,80}on day\s+(\d+),\s*prior to treatment initiation,\s*"
    r"and on the last day of treatment", re.I)
# "exposed to high-dose aerosol of M. tuberculosis Erdman from broth culture"
AEROSOL = re.compile(
    r"aerosol of\s+(M\.\s*tuberculosis)\s*([A-Z][A-Za-z0-9]*)?\s+from broth",
    re.I)
# Table S1's caption is the only place the deposit expands a drug abbreviation.
TABLE_S1 = re.compile(r"treated with\s+(.{0,320}?)\.\s*Pairwise", re.I | re.S)
ABBREV = re.compile(r"([A-Za-z][A-Za-z\-]{3,})\s*\(([A-Z][A-Z0-9]{1,4})\)")
FLOOR_WORDS = (r"limit\s+of\s+detection", r"detection\s+limit", r"\bLOD\b")
LT = re.compile(r"^<\s*([\d.]+)$")


def _sig3(c: float) -> float:
    """Half a unit in the third significant figure of a printed count."""
    return 0.5 * 10.0 ** (math.floor(math.log10(abs(c))) - 2) if c else 0.0


def _multiple_of(c: float, bound: float) -> int | None:
    """n if c is n*bound to the precision the sheet prints c at, else None."""
    if not (math.isfinite(c) and c > 0 and bound > 0):
        return None
    n = int(round(c / bound))
    if n >= 1 and abs(n * bound - c) <= _sig3(c):
        return n
    return None


def _quantum_note(bound: float, counts: pd.Series) -> str:
    """What this sheet's other counts say about a bound stated in one block.

    Computed, not asserted: the point of the sentence is that the bound is
    specific to the block that states it, and that has to be true of the file
    in front of the reader rather than of the file this was written against.
    """
    frac = Fraction(bound).limit_denominator(1000)
    off = [c for c in counts if _multiple_of(float(c), bound) is None]
    return ("%r is %d/%d to every digit the sheet prints, and across this "
            "sheet %d of the %d positive counts are NOT an integer "
            "multiple of it at the "
            "precision printed (%s among them), so it is the one-colony "
            "equivalent of the block that states it rather than a floor for "
            "the sheet, and it is applied to no other row"
            % (bound, frac.numerator, frac.denominator, len(off), len(counts),
               ", ".join("%g" % float(c) for c in off[:3])))


def _methods_text(d: Path) -> tuple[str, str]:
    """The deposit's supplementary methods as flat text, and where it came from."""
    blob, where = None, ""
    loose = sorted(d.rglob(METHODS_PDF))
    if loose:
        blob, where = loose[0].read_bytes(), loose[0].relative_to(d).as_posix()
    elif (d / ZIP).exists():
        try:
            with zipfile.ZipFile(d / ZIP) as zf:
                if METHODS_PDF in zf.namelist():
                    blob, where = zf.read(METHODS_PDF), f"{ZIP}::{METHODS_PDF}"
        except (zipfile.BadZipFile, OSError):
            blob = None
    if blob is None:
        return "", ""
    try:
        import pymupdf
    except ImportError:                                    # pragma: no cover
        try:
            import fitz as pymupdf                         # PyMuPDF < 1.24
        except ImportError:
            return "", ""
    try:
        with pymupdf.open(stream=blob, filetype="pdf") as doc:
            text = "".join(page.get_text() for page in doc)
    except Exception:                                      # pragma: no cover
        return "", ""
    return re.sub(r"\s+", " ", text).strip(), where


def _drug_names(text: str) -> dict[str, str]:
    """{'PZA': 'pyrazinamide', ...} exactly as Table S1's caption spells them."""
    m = TABLE_S1.search(text)
    return {code: name.lower() for name, code in ABBREV.findall(m.group(1))} \
        if m else {}


def _rs(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return round(f, 2) if math.isfinite(f) else None


def _cfu_token(v):
    """A CFU cell reduced to something comparable across the two deposits.

    Walter prints "<3.26" where this deposit prints "<3.26086956521739"; both
    reduce to "<3.26". Plain numbers keep six decimals, which separates the
    log10 values without fusing distinct counts.
    """
    if isinstance(v, str):
        s = v.strip()
        m = LT.match(s)
        if m:
            return "<%.2f" % float(m.group(1))
        try:
            v = float(s)
        except ValueError:
            return None
    if isinstance(v, (int, float, np.number)) and math.isfinite(float(v)):
        return "%.6f" % float(v)
    return None


def _twin_keys(d: Path) -> tuple[dict, str]:
    """(RS ratio, CFU as written) -> sheet name, for every row of the twin."""
    cand = None
    for base in (d.parent, d.parent.parent / "open", d.parent.parent / "restricted"):
        if (base / TWIN).is_dir():
            cand = base / TWIN
            break
    if cand is None:
        return {}, ""
    books = sorted(cand.rglob("*.xlsx"))
    if not books:
        return {}, ""
    book = books[0]
    keys: dict[tuple, str] = {}
    try:
        for sheet in pd.ExcelFile(book).sheet_names:
            raw = pd.read_excel(book, sheet_name=sheet, header=None)
            hdr = rs_col = cfu_col = None
            for i in range(min(12, len(raw))):
                cells = [str(v) for v in raw.iloc[i]]
                r = [j for j, v in enumerate(cells)
                     if re.search(r"RS ratio|rRNA synthesis ratio", v, re.I)]
                c = [j for j, v in enumerate(cells)
                     if re.match(r"\s*CFU", v, re.I)]
                if r and c:
                    hdr, rs_col, cfu_col = i, r[0], c[0]
                    break
            if hdr is None:
                continue
            for i in range(hdr + 1, len(raw)):
                key = (_rs(raw.iat[i, rs_col]), _cfu_token(raw.iat[i, cfu_col]))
                if key[0] is not None and key[1] is not None:
                    keys.setdefault(key, sheet)
    except Exception:                                      # pragma: no cover
        return {}, book.name
    return keys, book.name


def read(d: Path) -> pd.DataFrame:
    book = d / BOOK
    if not book.exists():
        found = sorted(d.rglob("aac.02310-21-s0002.xlsx"))
        if not found:
            return empty()
        book = found[0]
    rel = book.relative_to(d).as_posix()
    frames = {s: pd.read_excel(book, sheet_name=s, header=0) for s in COUNT_SHEETS}

    # ---- the deposit's own methods -----------------------------------------
    text, where = _methods_text(d)
    pdf_note = (
        "organism, strain and Experiment 1's times are parsed at run time from "
        "the deposit's own supplementary methods, %s" % where) if text else (
        "the deposit's supplementary methods PDF could not be read, so "
        "organism, strain and Experiment 1's times are blank")

    am = AEROSOL.search(text) if text else None
    organism = "Mycobacterium tuberculosis" if am else ""
    exp1_strain = (am.group(2) or "") if am else ""
    exp1_strain_note = (
        'strain from the methods: "aerosol of %s %s from broth culture"'
        % (am.group(1), am.group(2))) if (am and am.group(2)) else \
        "the methods name no strain for this experiment"
    exp23_strain_note = ("the methods describe Experiments 2 and 3 as "
                         '"aerosol of M. tuberculosis" with no strain, so '
                         "strain is blank")

    names = _drug_names(text) if text else {}

    # ---- Experiment 1's missing time axis -----------------------------------
    lm = EXP1_LEN.search(text) if text else None
    sm = EXP1_SAC.search(text) if text else None
    if lm and sm and lm.group(1) == sm.group(1):
        exp1_end_h = float(lm.group(2)) * 7.0 * 24.0
        exp1_time_note = (
            "the sheet has NO time column; this time comes from the deposit's "
            'own methods, "Treatment was initiated on day %s post aerosol and '
            'continued for %s %sweeks" together with mice "euthanized ... on '
            "day %s, prior to treatment initiation, and on the last day of "
            'treatment", so UNTX is the pre-treatment sacrifice at t = 0 of '
            "treatment and every drug group is the end-of-treatment sacrifice "
            "at %g h; the parenthesised number is a citation, reference 3 of "
            "that PDF being Walter et al. 2021 Nat Commun 12:2899"
            % (lm.group(1), lm.group(2),
               (lm.group(3) + " ") if lm.group(3) else "",
               sm.group(1), exp1_end_h))
    else:
        exp1_end_h = np.nan
        exp1_time_note = ("the sheet has NO time column and the two methods "
                          "sentences that would fix one did not both match, so "
                          "time_h is blank for this experiment")

    # ---- the absent floor, established rather than assumed -------------------
    # Every sheet, not only the three that carry counts: the sentence this
    # search produces says the phrase occurs nowhere in the WORKBOOK, and the
    # two relapse sheets are part of the workbook. header=None keeps the column
    # headings in the cells, so they are searched too.
    whole = pd.read_excel(book, sheet_name=None, header=None)
    hay = text.lower() + " " + " ".join(
        " ".join(str(v) for v in f.values.ravel() if isinstance(v, str)).lower()
        for f in whole.values())
    hits = [w for w in FLOOR_WORDS if re.search(w, hay, re.I)]
    floor_absent = FLOOR_ABSENT if not hits else (
        "a floor phrase (%s) now occurs somewhere in this deposit and this "
        "reader's search for it is out of date -- check the source before "
        "trusting a blank floor" % ", ".join(hits))

    # ---- the two scale claims, measured -------------------------------------
    e1 = pd.to_numeric(frames[COUNT_SHEETS[0]]["CFU"], errors="coerce").astype(float)
    anti = np.power(10.0, e1)
    fin = np.isfinite(anti)
    dev = float(np.max(np.abs(anti[fin] - np.round(anti[fin]))))
    gcd = int(np.gcd.reduce(np.round(anti[fin]).astype("int64")))
    e1_scale = (
        'the column is headed only "CFU", with no unit and no log marker; it is '
        "read as log10 because its antilogs are whole numbers (largest "
        "departure from an integer %.3g across %d values) sharing a common "
        "factor of %d, e.g. 10**6.595221 = 3937500, so cfu_per_ml is 10**value"
        % (dev, int(fin.sum()), gcd))

    f2, f3 = frames[COUNT_SHEETS[1]], frames[COUNT_SHEETS[2]]
    e2_pre = pd.to_numeric(f2.loc[f2.Group == "PreRx", "CFU"], errors="coerce")
    e3_pre = np.log10(pd.to_numeric(f3.loc[f3.Group == "PreRx", "CFU"],
                                    errors="coerce").astype(float))
    e2_scale = (
        'the column is headed only "CFU", with no unit and no log marker; it is '
        "read as log10 because Experiment 3 of this same deposit gives the same "
        "model's pre-treatment burdens as plain counts, whose log10 spans "
        "%.2f-%.2f, while these pre-treatment values span %.2f-%.2f, so "
        "cfu_per_ml is 10**value"
        % (float(e3_pre.min()), float(e3_pre.max()),
           float(e2_pre.min()), float(e2_pre.max())))
    e3_scale = ('the column is headed only "CFU" and holds plain counts, not '
                "log10: its values run to 2.06e7, and its pre-treatment mice "
                "agree with Experiments 1 and 2 once those are antilogged")

    twin, twin_book = _twin_keys(d)

    rows = []
    for sheet, df in frames.items():
        exp1 = sheet.startswith("Experiment1")
        log_scale = not sheet.startswith("Experiment3")
        scale_note = e1_scale if exp1 else (e2_scale if log_scale else e3_scale)

        # A bound stated by a "<" cell belongs to the group and day that state
        # it. Both are collected so the neighbouring counts can be told about
        # it WITHOUT the bound being written into their floor.
        block, counts = {}, []
        for j in range(len(df)):
            v = df.iloc[j]["CFU"]
            if isinstance(v, str):
                m = LT.match(v.strip())
                if m and not log_scale:
                    key = (str(df.iloc[j]["Group"]).strip(),
                           float(df.iloc[j]["Time (days)"]))
                    block[key] = float(m.group(1))
            elif not log_scale and float(v) > 0:
                counts.append(float(v))

        for i in range(len(df)):
            row = df.iloc[i]
            group = str(row["Group"]).strip()
            note = [ORGAN, scale_note, NO_ID, NO_PLATING, pdf_note, RELAPSE]

            # -- time ---------------------------------------------------------
            if exp1:
                # UNTX is time zero of TREATMENT only because the methods say
                # the untreated mice were taken on the day treatment began. If
                # that sentence did not parse, a bare group label fixes no time
                # at all and a 0 here would be exactly the quiet fill this
                # corpus exists to count -- and it would contradict the note
                # this row already carries. Blank for every arm, then.
                time_h = ((0.0 if group == "UNTX" else exp1_end_h)
                          if np.isfinite(exp1_end_h) else np.nan)
                note.append(exp1_time_note)
            else:
                days = float(row["Time (days)"])
                time_h = days * 24.0
                note.append("time given by the sheet in days (%g) and converted "
                            "to hours" % days)
                if group == "PreRx":
                    note.append("PreRx is the pre-treatment sacrifice, so this "
                                "is t = 0 of treatment")

            # -- drug and arm --------------------------------------------------
            if group in ("UNTX", "PreRx"):
                drug = ""
                note.append("no drug: %s is this deposit's untreated / "
                            "pre-treatment baseline" % group)
            elif exp1 and group in names:
                drug = names[group]
                note.append('drug name expanded from the deposit\'s own Table S1 '
                            'caption, "%s (%s)"; no dose is stated anywhere in '
                            "the deposit" % (names[group], group))
            else:
                drug = group
                note.append('the deposit never expands the regimen code "%s" '
                            "and states no dose for it, so the code is kept "
                            "verbatim rather than guessed at" % group)

            # -- the count -----------------------------------------------------
            raw = row["CFU"]
            cfu, floor, censored, basis = np.nan, np.nan, "", floor_absent
            if isinstance(raw, str):
                s = raw.strip()
                m = LT.match(s)
                if m:
                    floor = float(m.group(1))
                    basis = FLOOR_STATED % s
                    censored = "yes"
                    note.append('the cell is the inequality "%s", not a count, '
                                "so cfu_per_ml is left blank and the bound is "
                                "recorded as the floor" % s)
                    note.append(_quantum_note(floor, counts))
                else:
                    note.append('the cell holds the unparsed string "%s"' % s)
            else:
                v = float(raw)
                cfu = 10.0 ** v if log_scale else v
                bound = block.get((group, time_h / 24.0)) if not log_scale else None
                n = _multiple_of(v, bound) if bound else None
                if n:
                    note.append('this count is %d x %r, the bound stated by '
                                'the "<" cells of this same group and day, so '
                                "it is %d %s on that block's plating; the "
                                "deposit states no floor for THIS cell, and "
                                "none has been supplied for it"
                                % (n, bound, n, "colony" if n == 1
                                   else "colonies"))

            # -- the twin deposit ----------------------------------------------
            if twin:
                key = (_rs(row["RS ratio"]), _cfu_token(raw))
                seen = twin.get(key)
                if seen:
                    note.append("this reading also appears in the %s deposit "
                                '(%s, sheet "%s"), which is reference 3 of this '
                                "deposit's own methods; that sheet additionally "
                                "carries the mouse number and the treatment day"
                                % (TWIN, twin_book, seen))
                else:
                    note.append("this reading was not found in the %s deposit"
                                % TWIN)
            else:
                note.append("the %s deposit was not available to check the "
                            "overlap this deposit's reference 3 implies" % TWIN)

            note.append(exp1_strain_note if exp1 else exp23_strain_note)

            rows.append({
                "source_file": rel,
                "sheet": sheet,
                "organism": organism,
                "strain": exp1_strain if exp1 else "",
                "drug": drug,
                "concentration": np.nan,
                "conc_unit": "",
                "arm": group,
                "replicate": "%s row %d" % (sheet.split(" ")[0], i + 2),
                "tech_replicate": "",
                "time_h": time_h,
                "colonies": np.nan,
                "dilution": np.nan,
                "plated_volume_ul": np.nan,
                "cfu_per_ml": cfu,
                "censored": censored,
                "floor_cfu_per_ml": floor,
                "floor_basis": basis,
                "readout": READOUT,
                "notes": "; ".join(x for x in note if x),
            })

    return pd.DataFrame(rows)
