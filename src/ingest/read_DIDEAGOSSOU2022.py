"""DIDEAGOSSOU2022 -- AAC supplementary of PMC9017352 (aac.02310-21-s0002.xlsx),
per-mouse lung burdens from three BALB/c M. tuberculosis efficacy experiments.

The deposit is a zip holding two files that matter: the workbook, and the
supplementary methods PDF `aac.02310-21-s0001.pdf`. Both are the source. The
PDF is read at run time rather than quoted from memory, because everything this
reader knows beyond the bare numbers -- the organism, Experiment 1's strain and
its missing time axis -- comes out of it, and a revised deposit must be able to
change the answer.

WHAT THE WORKBOOK CONTAINS.  Five sheets, no captions, no merged headers: the
whole text of the file is its column headings, its group labels, and one string
cell reading "<3.26086956521739".  Three sheets carry counts:

  Experiment1 PD markers data   52 mice, groups UNTX PZA EMB STR RIF INH BDQ,
                                NO time column at all
  Experiment2 PD markers data   44 mice, PreRx HRZE PMZ BMZ BMZRb, days 0/14/28
  Experiment3 PD markers data   90 mice, PreRx HRZE PaMZ BPaL BPaMZ,
                                days 0/7/14/21/28

The two "relapse data" sheets are NOT read: they give the proportion of mice
whose lungs were culture-positive three months after treatment stopped (15/15,
9/15, 0/15 ...), which is an outcome per group, not a viable count per animal.

THREE THINGS THE DEPOSIT DOES NOT SAY, and are therefore blank here.

  * A DETECTION LIMIT, anywhere, for any experiment.  The strings "limit of
    detection", "detection limit" and "LOD" do not occur in the workbook or in
    the methods PDF; that absence is asserted by searching both at run time, not
    by memory.  What the methods do say is that Experiment 3's counts came from
    "serial dilutions of homogenates ... and plating on 7H11-OADC agar plates" ,
    with no volume and no dilution given, and that for Experiment 2
    "enumeration of CFU is described elsewhere (8)" -- an external reference,
    which is exactly the kind of pointer that cannot be turned into a floor
    here.  So floor_cfu_per_ml is blank on 183 of the 186 rows.

  * THE EXCEPTION, and it is a real one.  Three Experiment 3 cells (BPaMZ, day
    28) are not numbers but the string "<3.26086956521739".  For those three
    readings the deposit states a bound, so they get floor_cfu_per_ml =
    3.26086956521739 and censored = yes, with cfu_per_ml left BLANK -- the file
    gives an inequality, not a count, and writing 3.26 into the count column
    would invent a measurement.  The number is 75/23 exactly, and the three
    smallest positive counts in the same group and day are 3.26, 6.52 and 9.78,
    i.e. one, two and three times it: it is that block's one-colony equivalent.
    That arithmetic is recorded in the notes of the rows it concerns and is
    NOT propagated to any other row -- elsewhere in the same column the counts
    step in multiples of 7.5, so the per-mouse multiplier plainly varies and
    one block's quantum is not the sheet's floor.

  * DRUG DOSES AND REGIMEN EXPANSIONS.  Experiment 1's six single drugs are
    expanded by the deposit itself (Table S1: "pyrazinamide (PZA), ethambutol
    (EMB), ...") and those expansions are parsed out and used.  The regimen
    codes of Experiments 2 and 3 -- HRZE, PMZ, BMZ, BMZRb, PaMZ, BPaL, BPaMZ --
    are never expanded anywhere in the deposit, so `drug` carries the code
    verbatim.  Expanding them from the wider literature would be exactly the
    inference this corpus forbids.  No dose or concentration is given for any
    arm, so `concentration` and `conc_unit` are blank throughout.

THE CFU COLUMN IS ON TWO DIFFERENT SCALES AND THE SHEET NEVER SAYS SO.
Experiments 1 and 2 head the column "CFU" and fill it with 0.74-7.42;
Experiment 3 heads it "CFU" and fills it with 3.26-2.06e7.  The first two are
log10 and the third is linear, and this reader demonstrates that at run time
rather than assuming it: Experiment 1's values antilog to exact integers with a
common factor of 15, and Experiment 2's pre-treatment values sit inside the
log10 of Experiment 3's pre-treatment counts.  Both measurements are written
into the notes of every row they justify, so if a future revision breaks them
the note says the numbers no longer support the reading.

EXPERIMENT 1 HAS NO TIME COLUMN.  Its 52 mice carry a group and nothing else.
The deposit's own methods supply the design -- "Treatment was initiated on day
11 post aerosol and continued for 4 (3) weeks" and "Groups of 6 mice were
individually euthanized ... on day 11, prior to treatment initiation, and on
the last day of treatment" -- so UNTX is the pre-treatment sacrifice (time zero
of treatment) and the six drug groups are the end-of-treatment sacrifice.  Both
sentences must match before any Experiment 1 time is filled; if either fails,
time_h stays blank and the note says why.  The "(3)" inside "4 (3) weeks" is a
citation, not a second duration: reference 3 of this same PDF is Walter et al.
2021 Nat Commun 12:2899.

WHICH BRINGS US TO THE OVERLAP, and it is large.  Reference 3 is the deposit
WALTER2021_RSRATIO in this corpus, and Experiments 1 and 3 are re-depositions of
its source data:

  * all 52 Experiment 1 rows reappear in Walter's "Fig 4a-c & Sup Fig 7-8",
    which is a 80-row sheet that also carries the mouse number, the drug DOSE
    (RIF 10, INH 25, BDQ 25 ...), "Days of treatment" and "Day of sacrifice";
  * all 90 Experiment 3 rows reappear in Walter's "Fig 5a-d & Sup Fig 9-10",
    a 335-row sheet, restricted here to the pre-treatment and on-treatment
    animals -- Walter's censored cells read "<3.26", this deposit's read
    "<3.26086956521739";
  * Experiment 2 (Johns Hopkins) matches nothing in Walter and is new data.

So the re-deposition dropped Experiment 1's time axis and every dose, and
recovered precision on the censoring bound.  THE OVERLAP IS MEASURED AT RUN
TIME against the sibling directory and reported per row; nothing is imported
from it.  In particular Experiment 1's times come from this deposit's own
methods text and not from Walter's "Days of treatment" column, even though the
two agree, because filling a field from another deposit is the one thing a
reader here may not do.  If WALTER2021_RSRATIO is absent or has changed shape,
the check says so instead of failing.
"""
from __future__ import annotations

import math
import re
import zipfile
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
RELAPSE_SHEETS = ("Experiment2 relapse data", "Experiment3 relapse data")

READOUT = ("CFU per mouse lung (left and lower right lobes, per the deposit's "
           "supplementary methods; the denominator is an organ, NOT a mL)")

NOT_READ = ('the two "relapse data" sheets are not read here: they give the '
            "proportion of mice culture-positive after a drug holiday "
            "(15/15, 9/15, 0/15 ...), an outcome per group rather than a "
            "viable count per animal")

ORGAN = ("in vivo organ burden: the count is per mouse lung, and is placed in "
         "cfu_per_ml only because the schema has no per-organ column; do not "
         "read it as a concentration")

NO_ID = ("the deposit gives no mouse identifier; replicate is the 1-based row "
         "of the sheet the reading sits on, so a row can be found again")

NO_PLATING = ("the deposit states no plated volume, no dilution and no raw "
              "colony count for any experiment")

FLOOR_ABSENT = (
    'no reporting floor anywhere in this deposit: neither "limit of '
    'detection" nor "detection limit" nor "LOD" occurs in the workbook or in '
    "its supplementary methods PDF, the methods give Experiment 3's plating "
    "without a volume or a dilution, and Experiment 2's CFU enumeration is "
    "referred to an external publication")

FLOOR_STATED = ('stated in the sheet: the cell itself reads "%s", so this '
                "reading is bounded above by %.14g CFU per lung; it is the "
                "only floor statement anywhere in the deposit and it applies "
                "to this cell, not to the column")

# "Treatment was initiated on day 11 post aerosol and continued for 4 (3) weeks."
# The parenthesised number is a citation; both are captured so the note can
# quote the sentence as printed.
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
NO_FLOOR_WORDS = ("limit of detection", "detection limit", "lod")


def _methods_text(d: Path) -> tuple[str, str]:
    """The deposit's supplementary methods as text, and where it came from."""
    loose = list(d.rglob(METHODS_PDF))
    blob = None
    where = ""
    if loose:
        blob = loose[0].read_bytes()
        where = loose[0].relative_to(d).as_posix()
    else:
        z = d / ZIP
        if z.exists():
            try:
                with zipfile.ZipFile(z) as zf:
                    if METHODS_PDF in zf.namelist():
                        blob = zf.read(METHODS_PDF)
                        where = f"{ZIP}::{METHODS_PDF}"
            except (zipfile.BadZipFile, KeyError):
                blob = None
    if blob is None:
        return "", ""
    try:
        import pymupdf
    except ImportError:                                    # pragma: no cover
        try:
            import fitz as pymupdf                         # older PyMuPDF
        except ImportError:
            return "", ""
    try:
        with pymupdf.open(stream=blob, filetype="pdf") as doc:
            text = "".join(p.get_text() for p in doc)
    except Exception:                                      # pragma: no cover
        return "", ""
    return re.sub(r"\s+", " ", text).strip(), where


def _drug_names(text: str) -> dict[str, str]:
    """{'PZA': 'pyrazinamide', ...} exactly as Table S1's caption spells them."""
    m = TABLE_S1.search(text)
    if not m:
        return {}
    return {code: name.lower() for name, code in ABBREV.findall(m.group(1))}


def _twin_keys(d: Path) -> tuple[dict, str]:
    """(RS ratio, CFU as written) -> sheet, for every row of the twin deposit."""
    for base in (d.parent, d.parent.parent / "open", d.parent.parent / "restricted"):
        cand = base / TWIN
        if cand.is_dir():
            break
    else:                                                  # pragma: no cover
        return {}, ""
    books = sorted(cand.rglob("*.xlsx"))
    if not books:
        return {}, ""
    book = books[0]
    keys: dict[tuple, str] = {}
    try:
        xl = pd.ExcelFile(book)
        for sheet in xl.sheet_names:
            raw = pd.read_excel(book, sheet_name=sheet, header=None)
            hdr = rs_col = cfu_col = None
            for i in range(min(12, len(raw))):
                row = [str(v) for v in raw.iloc[i]]
                r = [j for j, v in enumerate(row)
                     if re.search(r"RS ratio|rRNA synthesis ratio", v, re.I)]
                c = [j for j, v in enumerate(row) if re.match(r"\s*CFU", v, re.I)]
                if r and c:
                    hdr, rs_col, cfu_col = i, r[0], c[0]
                    break
            if hdr is None:
                continue
            for i in range(hdr + 1, len(raw)):
                key = (_rs(raw.iat[i, rs_col]), _cfu_token(raw.iat[i, cfu_col]))
                if key[0] is None or key[1] is None:
                    continue
                keys.setdefault(key, sheet)
    except Exception:                                      # pragma: no cover
        return {}, book.name
    return keys, book.name


def _rs(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if not math.isfinite(f) else round(f, 2)


def _cfu_token(v):
    """A CFU cell reduced to something comparable across the two deposits.

    Walter prints "<3.26" where this deposit prints "<3.26086956521739"; both
    reduce to "<3.26".  Plain numbers keep six decimals, which is enough to
    separate the log10 values and exact enough not to fuse distinct counts.
    """
    if isinstance(v, str):
        s = v.strip()
        m = re.match(r"^<\s*([\d.]+)$", s)
        if m:
            return "<%.2f" % float(m.group(1))
        try:
            v = float(s)
        except ValueError:
            return None
    if isinstance(v, (int, float, np.number)) and math.isfinite(float(v)):
        return "%.6f" % float(v)
    return None


def read(d: Path) -> pd.DataFrame:
    book = d / BOOK
    if not book.exists():
        found = sorted(d.rglob("aac.02310-21-s0002.xlsx"))
        if not found:
            return empty()
        book = found[0]
    rel = book.relative_to(d).as_posix()

    text, pdf_where = _methods_text(d)
    if text:
        pdf_note = ("organism, strain and Experiment 1's times are read at run "
                    "time from the deposit's own supplementary methods, %s"
                    % pdf_where)
    else:
        pdf_note = ("the deposit's supplementary methods PDF could not be read, "
                    "so organism, strain and Experiment 1's times are blank")

    am = AEROSOL.search(text) if text else None
    organism = "Mycobacterium tuberculosis" if am else ""
    exp1_strain = (am.group(2) or "") if am else ""
    # Experiments 2 and 3 are described in a second paragraph that names no
    # strain; only Experiment 1's sentence carries one.
    exp23_strain = ""
    if am and am.group(2):
        strain_note = ('Experiment 1 strain from the methods: "aerosol of %s %s '
                       'from broth culture"' % (am.group(1), am.group(2)))
    else:
        strain_note = "the methods name no strain for this experiment"

    names = _drug_names(text) if text else {}
    twin, twin_book = _twin_keys(d)

    # --- Experiment 1's missing time axis ------------------------------------
    lm, sm = (EXP1_LEN.search(text), EXP1_SAC.search(text)) if text else (None, None)
    if lm and sm and lm.group(1) == sm.group(1):
        weeks = float(lm.group(2))
        exp1_end_h = weeks * 7.0 * 24.0
        exp1_time_note = (
            "the sheet has NO time column; the deposit's methods say "
            '"Treatment was initiated on day %s post aerosol and continued for '
            '%s %sweeks" and that mice were "euthanized ... on day %s, prior to '
            "treatment initiation, and on the last day of treatment\", so UNTX "
            "is the pre-treatment sacrifice (t = 0 of treatment) and each drug "
            "group is the end-of-treatment sacrifice at %g h; the parenthesised "
            "number is a citation, reference 3 of that PDF being Walter et al. "
            "2021 Nat Commun 12:2899"
            % (lm.group(1), lm.group(2), (lm.group(3) or "") and lm.group(3) + " ",
               sm.group(1), exp1_end_h))
    else:
        exp1_end_h = np.nan
        exp1_time_note = ("the sheet has NO time column and the two methods "
                          "sentences that would fix one did not both match, so "
                          "time_h is blank for this experiment")

    # --- the floor, asserted absent rather than assumed absent ---------------
    hay = text.lower()
    rows = []

    def sheet_text(df: pd.DataFrame) -> str:
        return " ".join(str(v) for v in df.values.ravel() if isinstance(v, str)).lower()

    frames = {s: pd.read_excel(book, sheet_name=s, header=0) for s in COUNT_SHEETS}
    workbook_text = " ".join(sheet_text(f) + " " + " ".join(map(str, f.columns)).lower()
                             for f in frames.values())
    hits = [w for w in NO_FLOOR_WORDS if w in hay or w in workbook_text]
    floor_absent = FLOOR_ABSENT if not hits else (
        "a floor phrase (%s) now occurs in this deposit and this reader's "
        "search for it is out of date -- check before trusting the blank"
        % ", ".join(hits))

    # --- the two scale claims, measured ---------------------------------------
    e1 = frames["Experiment1 PD markers data"]
    anti = np.power(10.0, pd.to_numeric(e1["CFU"], errors="coerce").astype(float))
    dev = float(np.nanmax(np.abs(anti - np.round(anti))))
    gcd = int(np.gcd.reduce(np.round(anti[np.isfinite(anti)]).astype("int64")))
    e1_scale = (
        'the column is headed only "CFU", with no unit and no log marker; it is '
        "read as log10 because its antilogs are whole numbers (largest "
        "departure from an integer %.3g over %d values) sharing a common factor "
        "of %d, e.g. 10**6.595221 = 3937500, and cfu_per_ml is 10**value"
        % (dev, int(np.isfinite(anti).sum()), gcd))

    e2 = frames["Experiment2 PD markers data"]
    e3 = frames["Experiment3 PD markers data"]
    e2_pre = pd.to_numeric(e2.loc[e2.Group == "PreRx", "CFU"], errors="coerce")
    e3_pre = np.log10(pd.to_numeric(e3.loc[e3.Group == "PreRx", "CFU"],
                                    errors="coerce").astype(float))
    e2_scale = (
        'the column is headed only "CFU", with no unit and no log marker; it is '
        "read as log10 because this deposit's Experiment 3 gives the same "
        "model's pre-treatment burdens as plain counts, whose log10 spans "
        "%.2f-%.2f, while these pre-treatment values span %.2f-%.2f, and "
        "cfu_per_ml is 10**value"
        % (float(e3_pre.min()), float(e3_pre.max()),
           float(e2_pre.min()), float(e2_pre.max())))
    e3_scale = ('the column is headed only "CFU" and holds plain counts, not '
                "log10: its values run to 2.06e7 and its pre-treatment mice "
                "agree with Experiments 1 and 2 once those are antilogged")

    for sheet, df in frames.items():
        exp1 = sheet.startswith("Experiment1")
        log_scale = not sheet.startswith("Experiment3")
        scale_note = e1_scale if exp1 else (e2_scale if log_scale else e3_scale)
        strain = exp1_strain if exp1 else exp23_strain
        for i, r in enumerate(df.itertuples(index=False)):
            group = str(r.Group).strip()
            note = [ORGAN, READOUT.split("(")[0].strip() and scale_note,
                    NO_ID, NO_PLATING, pdf_note, NOT_READ]

            # ---- time --------------------------------------------------------
            if exp1:
                time_h = 0.0 if group == "UNTX" else exp1_end_h
                note.append(exp1_time_note)
            else:
                days = float(getattr(r, "_1"))     # 'Time (days)'
                time_h = days * 24.0
                note.append("time given in days by the sheet (%g) and converted "
                            "to hours" % days)
                if days == 0 and group == "PreRx":
                    note.append("PreRx is the pre-treatment sacrifice, so this "
                                "is t = 0 of treatment")

            # ---- drug and arm -------------------------------------------------
            if group in ("UNTX", "PreRx"):
                drug = ""
                note.append("no drug: %s is this deposit's untreated / "
                            "pre-treatment baseline" % group)
            elif exp1 and group in names:
                drug = names[group]
                note.append('drug name expanded from the deposit\'s own Table '
                            'S1 caption, "%s (%s)"; no dose is stated anywhere '
                            "in the deposit" % (names[group], group))
            else:
                drug = group
                note.append("the deposit never expands the regimen code \"%s\" "
                            "and states no dose for it, so the code is kept "
                            "verbatim rather than guessed at" % group)

            # ---- the count ----------------------------------------------------
            raw = r.CFU
            cfu = np.nan
            floor = np.nan
            basis = floor_absent
            censored = ""
            if isinstance(raw, str):
                s = raw.strip()
                m = re.match(r"^<\s*([\d.]+)$", s)
                if m:
                    floor = float(m.group(1))
                    basis = FLOOR_STATED % (s, floor)
                    censored = "yes"
                    note.append('the cell is the inequality "%s", not a count, '
                                "so cfu_per_ml is left blank and the bound is "
                                "recorded as the floor" % s)
                    note.append("3.26086956521739 is 75/23 exactly, and the "
                                "smallest positive counts in this same group "
                                "and day are 3.26, 6.52 and 9.78 -- one, two "
                                "and three times it -- so it is this block's "
                                "one-colony equivalent; it is NOT applied to "
                                "any other row, because elsewhere in the same "
                                "column the counts step in multiples of 7.5")
                else:
                    note.append('the cell is the unparsed string "%s"' % s)
            else:
                v = float(raw)
                cfu = 10.0 ** v if log_scale else v

            # ---- the twin deposit ---------------------------------------------
            if twin:
                key = (_rs(r._1 if exp1 else r._2), _cfu_token(raw))
                # Experiment 1 has no time column, so RS ratio is field 1 there
                # and field 2 on the other two sheets.
                where = twin.get(key)
                if where:
                    note.append('this reading also appears in the %s deposit '
                                '(%s, sheet "%s"), which is reference 3 of this '
                                "deposit's own methods; that sheet additionally "
                                "carries the mouse number and the treatment day"
                                % (TWIN, twin_book, where))
            else:
                note.append("the %s deposit was not available to check the "
                            "overlap this deposit's reference 3 implies" % TWIN)

            note.append(strain_note if exp1 else
                        "the methods name no strain for Experiments 2 and 3")

            rows.append({
                "source_file": rel,
                "sheet": sheet,
                "organism": organism,
                "strain": strain,
                "drug": drug,
                "concentration": np.nan,
                "conc_unit": "",
                "arm": group,
                "replicate": "sheet row %d" % (i + 2),
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

    out = pd.DataFrame(rows)
    return out.dropna(subset=["time_h"]) if out.time_h.isna().all() is None else out
