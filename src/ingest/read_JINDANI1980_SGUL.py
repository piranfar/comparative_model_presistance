"""JINDANI1980_SGUL -- serial sputum colony counts from an early bactericidal
activity trial, deposited by St George's, University of London (figshare item
27862029, file 50649807.xlsx, one sheet "Jindani 1980").

WHY THIS IS 1980 AND NOT 2003, WHICH THE DEPOSIT'S OWN TITLE SAYS. The figshare
record 27862029 is titled "Bactericidal and Sterilizing Activities of
Antituberculosis Drugs during the First 14 Days (EBA Study)" and its description
says "100 patients treated with 22 regimens" -- that is the 2003 paper. The file
inside is named "Jindani 1980.xlsx", its only sheet is "Jindani 1980", and it
holds 112 patients and 24 regimens. The regimen labels settle it: they include
PAS and T, para-aminosalicylic acid and thiacetazone, which belong to the 1980
study and not to the 2003 one. So the record's metadata describes a different
study from its contents, and this reader follows the contents. Cite the deposit
by its DOI, 10.24376/rd.sgul.27862029.v1, and do not attach it to either paper
without checking -- the mismatch is the depositor's, not ours, and it is worth
recording rather than silently resolving.

WHAT THE FILE IS. One row per patient, 112 patients, 49 columns. There is no
caption, no README, no legend and no text anywhere below the header row -- the
sheet ends at the last data row, which is why so much of what a reader would
like to state is left blank here. Columns:

    ID   reg
    Day-0 A Ct1  Ct2  Diln  cfu  Log cfu
    Day-0 B Ct1  Ct2  Diln  cfu  Log cfu
    Mn Log cfu
    Day-2  Ct1 Ct2 Diln Cfu Log cfu     ... and the same five for
    Day-4, Day-6, Day-8, Day-10, Day-12, Day-14

so nine blocks of five columns per patient. Ct1 and Ct2 are the two plate
counts of one specimen; Diln is an integer dilution index 1-6; cfu and Log cfu
are the sheet's own derived density and its base-10 log (Log cfu == log10(cfu)
in every populated cell, checked).

THE HYPHEN IN "Day-14" IS A SEPARATOR, NOT A MINUS SIGN. The blocks run
Day-0, Day-2 ... Day-14 left to right and the counts fall across them, so these
are days 0 to 14 of treatment, not negative days. Day 0 is the pre-treatment
baseline and is time_h = 0; there is no pre-infection reading in this deposit
and nothing has to be dropped. Days are multiplied by 24.

Day-0 A and Day-0 B are two separate pre-treatment sputum specimens from the
same patient, so each patient has TWO readings at time_h = 0. They are kept
apart in tech_replicate rather than averaged; column M "Mn Log cfu" is the
sheet's own mean of the two day-0 logs and is a summary, not a reading, so no
row is emitted for it.

THE FLOOR: DERIVED FROM THE WORKBOOK'S OWN CELL FORMULA, NOT STATED BY ANYONE.
Nobody in this deposit names a limit -- there is no LOD, no LOQ, no plated
volume, no column, no footnote, no README, no legend. What the workbook does
carry is live Excel formulas, and they give the conversion exactly. Every cfu
cell in every one of the nine blocks reads

    =AVERAGE(Ct1,Ct2)*48*10^(Diln-1)

and every Log cfu cell reads =LOG(cfu) -- verbatim, e.g. F2 is
"=AVERAGE(C2,D2)*48*10^(E2-1)" and AV2 is "=AVERAGE(AS2,AT2)*48*10^(AU2-1)".
976 of the 977 populated cfu cells carry it; exactly one does not, and that one
is the corrupt cell below. _formula() pulls the formula out of the file at read
time, so the sentence in floor_basis is a quotation of the deposit in hand and
cannot go stale; _constant() then re-derives the same constant from the values
alone, and the two must agree or the reader raises rather than write a floor.

Two consequences, and neither is an inference from outside the file.

  * Ct1 and Ct2 ARE TWO SEPARATE PLATES of one specimen, not two counts of one
    plate. The sheet AVERAGES them -- it does not sum them -- and the average
    lands on a half in 498 of the 977 populated readings, with six readings
    where one plate grew nothing and the other did (e.g. Ct1=1, Ct2=0 giving
    cfu=240 at Diln=2). Two counts of a single plate could not do that.

  * THE SMALLEST NON-ZERO DENSITY the sheet's own arithmetic can produce for a
    reading is therefore one colony on one of the two plates: mean 0.5, i.e.

        floor = 0.5 * 48 * 10**(Diln-1) = 24 * 10**(Diln-1) = 2.4 * 10**Diln

    That is what goes in floor_cfu_per_ml -- a per-reading floor, the same
    construction read_PIRANFAR2026 uses on a recorded plated volume, and one
    the file demonstrates rather than merely permits (cfu = 240 at Diln=2 and
    cfu = 48 at Diln=1 both occur). The lowest dilution used anywhere is
    Diln = 1, so the smallest floor in the deposit, and the number to quote as
    the study-level floor, is 24 CFU/mL. A reading taken at Diln = 5 has a
    floor of 240,000 CFU/mL and cannot resolve anything below it.

The floor is DERIVED and the corpus must count it as derived: the arithmetic is
the depositor's, but the reading of it as a floor is this reader's. No author
states a limit, and nothing was taken from the 2003 paper (not open access) or
from any protocol.

WHAT STILL CANNOT BE SEPARATED is the plated volume from any fixed dilution
folded into the constant 48. The file applies 48 * 10**(Diln-1) as one factor;
48 alone would be 1/48 mL = 20.8 uL plated, but a 20 uL plate with a further
1:0.96 step gives the same number and the deposit does not say which. So
plated_volume_ul stays blank on every row, and `dilution` carries the power of
ten the file's own formula applies -- 10**(Diln-1), NOT 10**Diln -- with the
caveat repeated in notes. (An earlier version of this reader wrote 10**Diln
here, which is a factor of ten larger than anything the workbook does.)

TWELVE READINGS HAVE NO DERIVABLE FLOOR, and they are exactly the ones where it
matters. When both plate counts are zero the sheet leaves Diln, cfu and Log cfu
empty, so the dilution that specimen was read at is not recorded and no floor
follows for it. Those rows carry cfu_per_ml = 0 and a BLANK floor, and their
`censored` is left for finish() to fill, which makes it "unknown". That is
deliberate and it is the point of the corpus: we know nothing grew, and we do
NOT know what density that non-detection excludes. Calling them censored = yes,
as an earlier version of this reader did, is literally true but hides twelve
readings from the one statistic the coverage table exists to report, and
finish()'s own docstring forbids it -- "never by guessing that a zero means the
floor". The fact that nothing grew is preserved in cfu_per_ml = 0 and in notes.
Nineteen further patient-timepoints are wholly empty -- no specimen -- and get
no row at all. 112 * 9 = 1008 = 977 + 12 + 19.

ONE CORRUPT CELL, left uncorrected. Patient 1747206132, Day-14: Ct1 = 25,
Ct2 = 29, Diln = 4, which give 1,296,000, but the sheet writes cfu = 3 and
Log cfu = 0.477. The workbook XML shows why: cell AV113 is the only cfu cell in
the file with NO formula in it -- someone overtyped =AVERAGE(AS113,AT113)*48*
10^(AU113-1) with a literal 3, and the neighbouring =LOG(AV113) faithfully
returned 0.477. It is the only reading in the workbook where the arithmetic
fails. The value is passed through exactly as written and flagged in notes; the
censored flag that then follows from it is an artefact of the corrupt cell, not
a measurement.

WHAT THE DEPOSIT DOES NOT SAY, and is therefore blank here.

  * THE ORGANISM AND THE STRAIN. The workbook names neither, anywhere. The
    corpus manifest records M. tuberculosis in human sputum for this study from
    outside the deposit; per the schema's rule that is not transcribed into the
    data, so organism and strain are blank.

  * WHAT THE REGIMEN LETTERS MEAN. The "reg" column gives bare codes -- SHRZM,
    HRM, R20, H150, T, PAS, M, Z, Nil -- and the deposit never expands them.
    They are carried verbatim into `arm` and into `drug`, untranslated. The one
    exception is "Nil", which is the file's own word for no treatment: those
    four patients get arm = "Nil" and drug = "" as the schema asks for an
    untreated arm.

  * THE DOSE UNIT. Six codes embed a number (H150, H300, H600, R5, R10, R20)
    and nothing says what the number is -- almost certainly a daily dose rather
    than a concentration, but the deposit does not say so and these are human
    sputum counts, not broth. `concentration` and `conc_unit` stay blank and
    the number stays where the file put it, inside the arm label.

  * THE UNIT ON "cfu". The header is a bare "cfu"/"Cfu". These are sputum
    densities, and CFU/mL is this reader's label for a quantity the deposit
    leaves unlabelled; every row's notes say so.

  * WHAT THE 48 IS MADE OF. See above: the plated volume and any fixed
    dilution folded into it cannot be separated, so neither is recorded.

ONE ROW PER SPECIMEN, NOT PER PLATE. Ct1 and Ct2 are two plates of one
specimen, and the schema's tech_replicate is for exactly that -- but the file
reports only the averaged density, never a per-plate one, so splitting the
reading in two would mean manufacturing two cfu values the deposit does not
contain. The reading the deposit reports is the specimen, so that is the row.
`colonies` is Ct1 + Ct2, the total colonies actually counted (which is what the
floor is one of), both raw numbers are kept in notes, and tech_replicate is
used for the two day-0 SPECIMENS, A and B, which are a different thing.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

from src.ingest import empty

SHEET = "Jindani 1980"
# "Day-0 A Ct1", "Day-2 Ct1"
CT1_RE = re.compile(r"^Day-(\d+)\s*([A-Z])?\s*Ct1$", re.I)
PREFIX_RE = re.compile(r"^day-\d+\s*[a-z]?\s*")
FOLLOW = ["ct2", "diln", "cfu", "log cfu"]
# The cfu column is live Excel formulas: =AVERAGE(Ct1,Ct2)*48*10^(Diln-1).
# That is the deposit's own arithmetic in the deposit's own words, and it is
# the whole basis of the floor, so it is read out of the file rather than
# assumed. Captures the multiplier and the exponent offset.
FORMULA_RE = re.compile(
    r"^=\s*AVERAGE\(\s*[A-Z]+\d+\s*,\s*[A-Z]+\d+\s*\)\s*\*\s*([0-9.]+)\s*\*"
    r"\s*10\^\(\s*[A-Z]+\d+\s*-\s*([0-9.]+)\s*\)\s*$")

UNIT_NOTE = ("the sheet's column is a bare \"cfu\" with no unit; these are "
             "sputum densities and CFU/mL is this reader's label, not the "
             "deposit's")
CODE_NOTE = ("the deposit never expands its regimen letter codes, so the code "
             "is carried verbatim into arm and drug and no drug name, dose or "
             "unit is inferred")
# Referenced on every row and lost in an edit, which the corpus build caught as
# a NameError rather than as a silent blank. It records the one thing the
# recovered constant K cannot tell us.
VOL_NOTE = ("the plated volume cannot be separated from the absolute dilution: "
            "the recovered constant K fixes only their ratio, so plated_volume_ul "
            "stays blank while the per-reading floor, which depends only on that "
            "ratio, does not")


def _norm(v) -> str:
    return re.sub(r"\s+", " ", str(v)).strip() if isinstance(v, str) else ""


def _blocks(raw: pd.DataFrame) -> list[tuple[str, int, float, str]]:
    """(label, first column, time_h, specimen) for each five-column block."""
    out = []
    for c in range(raw.shape[1]):
        m = CT1_RE.match(_norm(raw.iat[0, c]))
        if not m:
            continue
        # The two Day-0 blocks repeat the block name on the Ct2 header
        # ("Day-0 A Ct2"); the later blocks leave it as padded "Ct2".
        tail = [PREFIX_RE.sub("", _norm(raw.iat[0, c + k]).lower())
                for k in range(1, 5)]
        if tail != FOLLOW:
            raise ValueError(
                "%s: block at column %d is headed %r, not %r"
                % (SHEET, c, tail, FOLLOW))
        day = float(m.group(1))
        if day < 0:
            raise ValueError("%s: negative day in header %r"
                             % (SHEET, m.group(0)))
        spec = (m.group(2) or "").upper()
        label = "Day-%d%s" % (int(day), " " + spec if spec else "")
        out.append((label, c, day * 24.0, spec))
    if not out:
        raise ValueError("%s: no 'Day-<n> Ct1' blocks in the header row" % SHEET)
    return out


def _formula(src: Path, blocks) -> tuple[float, float, int, int] | None:
    """(multiplier, exponent offset, cells with the formula, cells without).

    Read off the cfu cells themselves, so what floor_basis says about the
    deposit's arithmetic is a quotation of the file in hand and cannot go
    stale. Returns None if the workbook has been re-saved values-only and the
    formulas are gone; the caller then falls back to _constant()'s fit, which
    gives the same floor but cannot say how the power of ten splits.
    """
    ws = load_workbook(src, data_only=False)[SHEET]
    seen, yes, no = set(), 0, 0
    for _, c, _, _ in blocks:
        for r in range(2, ws.max_row + 1):
            v = ws.cell(row=r, column=c + 4).value   # 0-based c+3 -> 1-based
            if v is None:
                continue
            if isinstance(v, str) and v.startswith("="):
                m = FORMULA_RE.match(v)
                if m is None:
                    raise ValueError(
                        "%s: cfu cell %s holds %r, which is not the "
                        "AVERAGE(Ct1,Ct2)*k*10^(Diln-n) the rest of the sheet "
                        "uses; the floor derivation must be re-checked before "
                        "any floor is written"
                        % (SHEET, ws.cell(row=r, column=c + 4).coordinate, v))
                seen.add((float(m.group(1)), float(m.group(2))))
                yes += 1
            else:
                no += 1
    if not yes:
        return None
    if len(seen) != 1:
        raise ValueError(
            "%s: the cfu cells use %d different conversions %r; the floor "
            "derivation must be re-checked before any floor is written"
            % (SHEET, len(seen), sorted(seen)))
    mult, off = seen.pop()
    return mult, off, yes, no


def _constant(raw: pd.DataFrame, blocks) -> tuple[float, int, int, int, int]:
    """The sheet's colonies-to-density constant K in cfu = (Ct1+Ct2)*K*10**Diln.

    Fitted from the numbers, not assumed: the modal ratio across every
    populated reading, then checked against all of them. Independent of
    _formula(), which reads the same constant out of the cell formulas; the
    two are cross-checked in read().

    Also counts the evidence that Ct1 and Ct2 are two SEPARATE plates rather
    than two counts of one plate, which is what fixes the floor at one colony
    on one plate (mean 0.5) instead of one colony on both (mean 1): readings
    whose two counts sum to an odd number, and readings where one plate grew
    nothing and the other did.
    """
    ratios, halves, splits = [], 0, 0
    for _, c, _, _ in blocks:
        for i in range(1, len(raw)):
            a, b, dl, cfu = (raw.iat[i, c], raw.iat[i, c + 1],
                             raw.iat[i, c + 2], raw.iat[i, c + 3])
            if any(pd.isna(v) for v in (a, b, dl, cfu)):
                continue
            a, b = float(a), float(b)
            s = a + b
            halves += int(s % 2 == 1)
            splits += int(min(a, b) == 0 and max(a, b) > 0)
            if s > 0:
                ratios.append(round(float(cfu) / (s * 10.0 ** float(dl)), 10))
    if not ratios:
        raise ValueError("%s: no populated readings to fit the constant" % SHEET)
    k, n = Counter(ratios).most_common(1)[0]
    if n < 0.95 * len(ratios):
        raise ValueError(
            "%s: cfu = (Ct1+Ct2)*K*10**Diln holds in only %d of %d readings; "
            "the deposit's arithmetic has changed and the floor derivation "
            "must be re-checked before any floor is written"
            % (SHEET, n, len(ratios)))
    return float(k), n, len(ratios), halves, splits


def read(d: Path) -> pd.DataFrame:
    src = next(iter(sorted(d.glob("*.xlsx"))), None)
    if src is None:
        return empty()
    raw = pd.read_excel(src, sheet_name=SHEET, header=None)

    blocks = _blocks(raw)
    k, agree, total, halves, splits = _constant(raw, blocks)
    form = _formula(src, blocks)
    if form is None:
        # Formulas gone (a values-only re-save). The floor still follows from
        # the numbers, but how the power of ten splits between dilution and
        # plated volume no longer does, so `dilution` is left blank.
        off = None
        quote = ("cfu = (Ct1+Ct2) x %g x 10^Diln, recovered from the sheet's "
                 "own numbers as the modal ratio and holding in %d of %d "
                 "populated readings (the workbook's cfu formulas are gone, "
                 "so this is a fit, not a quotation)" % (k, agree, total))
    else:
        mult, off, live, dead = form
        # One colony on one of the two plates is a mean of 0.5, so the
        # per-colony density is 0.5*mult*10**(Diln-off) = k*10**Diln.
        from_formula = 0.5 * mult * 10.0 ** (-off)
        if abs(from_formula - k) > 1e-9 * max(1.0, k):
            raise ValueError(
                "%s: the cfu formula gives %g per colony but the values give "
                "%g; the deposit's arithmetic has changed and the floor "
                "derivation must be re-checked before any floor is written"
                % (SHEET, from_formula, k))
        quote = ("the workbook's cfu column is live Excel and all %d of its "
                 "formula cells read =AVERAGE(Ct1,Ct2)*%g*10^(Diln-%g)%s, and "
                 "the same constant comes back independently from the numbers "
                 "in %d of %d populated readings"
                 % (live, mult, off,
                    "" if not dead else
                    ", the other %d holding a typed value instead" % dead,
                    agree, total))

    lowest = int(min(
        float(raw.iat[i, c + 2])
        for _, c, _, _ in blocks for i in range(1, len(raw))
        if pd.notna(raw.iat[i, c + 2])))
    study_floor = k * 10.0 ** lowest

    vol_note = (
        "no plated volume and no reporting limit appears anywhere in the "
        "deposit, so plated_volume_ul is blank; the file folds the volume into "
        "a single constant" +
        ("" if off is None else
         " (%g, which alone would be 1/%g mL plated but could equally be a "
         "smaller volume with a further fixed dilution step), and `dilution` "
         "carries only the power of ten the file's own formula applies, "
         "10**(Diln-%g)" % (mult, mult, off)) +
        ("; the workbook's formulas are gone, so `dilution` is blank too"
         if off is None else ""))

    # Ct1 and Ct2 are two SEPARATE plates, which is what puts the floor at one
    # colony on one plate rather than one on each. The file proves it: half the
    # averages land on a .5, and some readings have one plate blank.
    fit = ("%s. Ct1 and Ct2 are two separate plates, not two counts of one "
           "plate -- the sheet averages them, the average lands on a half in "
           "%d of the %d populated readings, and in %d of them one plate grew "
           "nothing while the other did" % (quote, halves, total, splits))
    # NOTE ON WORDING. build_corpus_long.py separates a STATED floor from a
    # DERIVED one by matching floor_basis against
    #   "stated in the sheet|LOD column|limit of detection\b.*\d"
    # so this text must not contain the phrase "limit of detection" -- saying
    # that the deposit HAS no detection limit would otherwise be counted as
    # the deposit having declared one, which is the exact miscount that table
    # exists to prevent. "detection limit" and "quantification limit" below
    # are deliberate. The floor here IS derived: the arithmetic is the
    # depositor's, but reading it as a floor is this reader's doing.
    basis_tmpl = (
        "DERIVED BY THIS READER, NOT STATED BY THE DEPOSIT. Nobody in the "
        "deposit names a floor: no detection limit, no quantification limit, "
        "no plated volume, no footnote, no README. The derivation is the "
        "deposit's own arithmetic -- " + fit + ". So the smallest non-zero "
        "density that arithmetic can produce for a reading taken at Diln=%d "
        "is one colony on one of the two plates, %s CFU/mL. The lowest "
        "dilution used anywhere in the sheet is Diln=%d, so the study-level "
        "floor is %s CFU/mL.")
    basis_zero = (
        "NO FLOOR FOR THIS READING. Both plate counts are 0 and the sheet "
        "leaves Diln, cfu and Log cfu blank, so the dilution this specimen was "
        "read at is not recorded and no floor follows from it. The deposit's "
        "arithmetic (" + fit + ") would give %s CFU/mL only if this reading "
        "had been taken at the lowest dilution the sheet uses anywhere "
        "(Diln=%d), and the deposit does not say that it was."
        % ("%g" % study_floor, lowest))

    rows = []
    for label, c, time_h, spec in blocks:
        for i in range(1, len(raw)):
            pid = raw.iat[i, 0]
            reg = _norm(raw.iat[i, 1])
            if pd.isna(pid) or not reg:
                continue
            a, b, dl, cfu, lg = (raw.iat[i, c + j] for j in range(5))
            if all(pd.isna(v) for v in (a, b, dl, cfu, lg)):
                continue                      # no specimen at this timepoint
            if pd.isna(a) or pd.isna(b):
                raise ValueError("%s row %d %s: one plate count missing; the "
                                 "deposit's shape has changed"
                                 % (SHEET, i, label))

            colonies = float(a) + float(b)
            note = ["%s: two plates of one specimen, Ct1=%g and Ct2=%g, which "
                    "the sheet AVERAGES (not sums) into one density; colonies "
                    "is their total" % (label, float(a), float(b))]

            if pd.isna(dl):
                if colonies != 0:
                    raise ValueError(
                        "%s row %d %s: Diln blank but colonies=%g; only "
                        "zero-count readings lack a dilution in this deposit"
                        % (SHEET, i, label, colonies))
                dilution, floor, basis = np.nan, np.nan, basis_zero
                # censored is LEFT BLANK for finish() to make "unknown".
                # Calling it "yes" would be true of the count and false of the
                # evidence: we know nothing grew, we do not know what density
                # that excludes, and finish()'s own rule is never to infer
                # censoring from a zero with no floor. The non-detection is
                # carried by cfu_per_ml = 0 and by the note below.
                value, cens = 0.0, ""
                note.append("nothing grew on either plate; the sheet leaves "
                            "Diln, cfu and Log cfu empty for this reading, so "
                            "cfu_per_ml is the 0 the plate counts state and "
                            "the floor it sits below is not recorded")
            else:
                dl = int(dl)
                # The power of ten the sheet's own formula applies is
                # 10**(Diln-off), not 10**Diln. Without the formulas the split
                # is unknown, so the column stays blank rather than guess.
                dilution = np.nan if off is None else 10.0 ** (dl - off)
                floor = k * 10.0 ** dl
                basis = basis_tmpl % (dl, "%g" % floor, lowest,
                                      "%g" % study_floor)
                value, cens = float(cfu), ""
                note.append("Diln=%d" % dl)
                expect = colonies * k * 10.0 ** dl
                if abs(value - expect) > 1e-6 * max(1.0, expect):
                    note.append(
                        "CORRUPT CELL, PASSED THROUGH UNCHANGED: the sheet "
                        "writes cfu=%g (Log cfu=%s) but its own Ct1, Ct2 and "
                        "Diln give %g. The cell has had its formula overtyped "
                        "with a literal value -- it is the only cfu cell in "
                        "the workbook with no formula in it -- and the "
                        "neighbouring =LOG() faithfully logged the wrong "
                        "number. Nothing is repaired here, and any censoring "
                        "flag on this row is an artefact of the bad cell, not "
                        "a measurement"
                        % (value,
                           "%g" % float(lg) if pd.notna(lg) else "blank",
                           expect))

            if spec:
                note.append("one of two pre-treatment sputum specimens (A and "
                            "B) from this patient, both at time_h = 0; the "
                            "sheet's 'Mn Log cfu' column averages them and is "
                            "not read as a reading")

            rows.append({
                "source_file": src.name,
                "sheet": SHEET,
                "organism": "",
                "strain": "",
                "drug": "" if reg.lower() == "nil" else reg,
                "concentration": np.nan,
                "conc_unit": "",
                "arm": reg,
                "replicate": "patient %s" % str(pid).strip(),
                "tech_replicate": ("specimen %s" % spec) if spec else "",
                "time_h": time_h,
                "colonies": colonies,
                "dilution": dilution,
                "plated_volume_ul": np.nan,
                "cfu_per_ml": value,
                "censored": cens,
                "floor_cfu_per_ml": floor,
                "floor_basis": basis,
                "readout": "CFU",
                "notes": "; ".join(note + [UNIT_NOTE, CODE_NOTE, vol_note]),
            })

    df = pd.DataFrame(rows)
    return df if not df.empty else empty()
