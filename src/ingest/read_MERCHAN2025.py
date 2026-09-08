"""MERCHAN2025 -- Zenodo 17037904: Mycobacterium abscessus GD01 treated with
mycobacteriophages Muddy and 8UZL, cefoxitin and tigecycline, alone and in
combination, planktonically and as 96 h biofilms.

TEN FILES. Eight workbooks, a README and the manuscript PDF. What each holds,
and what this reader does with it:

  Biofilm_Muddyvs8UZL.xlsx      READ. Four sheets. "Biofilm CFU" and
                                "Planktonic CFU" are viable counts over time
                                (days 0/1/3/5 and 0/1/3/5/10) for four arms --
                                no-phage control, ferrous ammonium sulfate
                                control, Muddy, 8UZL -- three columns each.
  Planktonic_Muddyvs8UZL.xlsx   IGNORED AS A DUPLICATE, and the test is made at
                                run time, not asserted here: this file is BYTE
                                IDENTICAL to the one above (both sha256
                                8cac7266f73fc1f0...), so it carries the same
                                four sheets and contributes no new reading. The
                                README describes them as two different files.
                                If a revision ever makes them differ, the hash
                                check fails open and both are read.
  Biofilm_Muddyvs8UZL_FOX.xlsx  READ. One sheet, three timepoint blocks
  Biofilm_Muddyvs8UZL_TGC.xlsx  (24 h, day 3, day 5), nine arms x 3 replicates,
                                a "GD01 CFU" column and a phage "PFU 1" column
                                per block, an AUC column, and an inoculum block
                                at the foot.
  Planktonic_..._FOX.xlsx       READ. Same shape, five timepoint blocks
  Planktonic_..._TGC.xlsx       (24 h, 3, 5, 7, 10 days).
  Biofilm_7H9vsCAMH.xlsx        READ. Growth of GD01 in two media, 0-120 h,
  Planktonic_7H9vsCAMH.xlsx     three columns per medium. NO antimicrobial is
                                applied in either file: they are growth curves,
                                so `drug` is blank on all their rows. They are
                                kept because they are viable counts over time
                                from the same strain and assay, and because the
                                deposit states a detection limit for them.
  README.txt                    metadata only: organism, strain, the meaning of
                                FOX/TGC/Brep/Trep, the concentration unit, and
                                the file-to-figure map. Parsed, not transcribed.
  Mercha_n_Ruiz_2025.pdf        the manuscript, shipped INSIDE this deposit.
                                Parsed for one thing only: the limit of
                                detection its figure legends state.

WHAT IS DELIBERATELY NOT READ.

  * EVERY PFU NUMBER. The "Biofilm PFU" and "Planktonic PFU" sheets, and the
    "PFU"/"PFU 1" column of each timepoint block, are plaque counts -- phage,
    not bacteria. They do not belong in cfu_per_ml under any reading of the
    schema and none of them is emitted.
  * THE AUC COLUMNS ("AUC CFU", "AUC"). Derived summaries of the curves already
    read, not readings.
  * "Muddy titer" and "8UZL titer" in the inoculum block: phage stock titres.

THE FLOOR, and why it is on some rows and not others.

  This deposit does state a bacterial detection limit -- but only for two of
  its four figures, and this reader carries it no further than the deposit
  does. The shipped manuscript's Fig. 1 legend reads

      "LOD = limit of detection (2log10 CFU/mL for bacteria, 2log10 PFU/mL for
       phages)"

  and its Fig. S1 legend repeats the bacterial value. So 10**2 = 100 CFU/mL is
  a source-stated floor for the data behind those two figures: the phage-only
  workbook (Fig. 1) and the two media workbooks (Fig. S1). The legends of
  Fig. 2 (cefoxitin) and Fig. 3 (tigecycline) state NO detection limit, so the
  four combination workbooks get floor_cfu_per_ml blank. Assuming the same
  limit applies because it is the same laboratory and the same drip-dilution
  plate is exactly the inference the schema forbids; that the same deposit
  states a floor for half its figures and not the other half is a finding, and
  it is recorded as one rather than smoothed away.

  Which figure a workbook belongs to is READ OFF THE README at run time (its
  "Figure 1: / The file X.xlsx contains ..." sections), and which figure states
  a limit is READ OFF THE PDF at run time. Nothing here is hard-coded, so a
  revised deposit changes the answer instead of being silently overridden. One
  consequence worth naming: the README's "Figure 3" section names the two _FOX
  files a second time and never names the two _TGC files at all, so the
  tigecycline workbooks map to no figure. That does not change their floor --
  Fig. 3 states no limit either -- but it is why their floor_basis says the
  README does not map them.

  NO PLATED VOLUME IS STATED FOR THE BACTERIAL COUNTS. The manuscript says only
  that pellets were "plated using a drip dilution method on Middlebrook 7H10 +
  OADC plates" (ref. 14); no volume, no dilution and no colony count reaches
  any workbook, so no floor can be derived by arithmetic anywhere in this
  deposit. The PFU sheets do fix their own spot volume -- their PFU/mL is
  exactly mean(TRep) x 10**Dil / 0.003 mL throughout -- but that is the phage
  spot assay on a bacterial lawn, a different plate from the bacterial drip
  dilution, and it is NOT transferred to the CFU rows.

VALUES WRITTEN AS ZERO. The "Planktonic CFU" sheet of the Fig. 1 workbook
writes five readings as a literal 0 (Muddy and 8UZL arms, days 1-10). They are
kept as 0, not replaced: with the stated 100 CFU/mL floor finish() marks them
censored, but the file itself does not distinguish "no colonies on the plate"
from "below the limit", and neither does this reader. No placeholder value --
no 1, no 0.1, no floor substitution -- appears anywhere in this deposit.

REPLICATES. `replicate` is "<mode> <experiment>/<n>", because the same arm name
recurs across unrelated experiments here and a bare "1" would collapse them.
The three columns of the Fig. 1 and media sheets are unlabelled; the manuscript
says "three independent experiments with three technical replicates", so
whether one workbook cell is one plate or a mean of three is NOT stated, and
tech_replicate is left blank rather than guessed. The combination workbooks
label their rows "- 1/- 2/- 3", which is what `replicate` carries there.

SHARED ROWS BETWEEN THE FOX AND TGC WORKBOOKS. The Growth, Muddy and 8UZL arms
and the inoculum block are identical, cell for cell, between the cefoxitin and
tigecycline workbook of the same culture mode -- same values, same dates in the
block headers. They are one experiment reported in two figures, so each such
reading is emitted once, from the alphabetically first file, with a note naming
the file that repeats it. Divergent repeats would be emitted twice with a
divergence note instead; that comparison is made on the values at run time.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

README = "README.txt"
PDF = "Mercha_n_Ruiz_2025.pdf"

# "LOD = limit of detection (2log10 CFU/mL for bacteria, ..." and
# "LOD (limit of detection) = 2log10 CFU/mL MAB GD01"
LOD_RE = re.compile(
    r"limit of detection\D{0,15}?(\d+(?:\.\d+)?)\s*log\s*10\s*CFU\s*/\s*mL", re.I)
# a figure legend starts its own line: "Fig. 1 Differences ...", "Fig. S1. ..."
FIG_RE = re.compile(r"(?m)^Fig\.\s*(S?\d+)")
# the README's own section headings and file sentences
README_FIG_RE = re.compile(r"(?mi)^[ \t]*(Supplemental\s+Figure|Figure)\s+(\d+)\s*:")
README_FILE_RE = re.compile(r"The file\s+(\S+\.xlsx)", re.I)
# "GD01: Strain GD01, a rough clinical isolate of Mycobacterium abscessus"
ORG_RE = re.compile(
    r"[A-Z]\w+:\s*Strain\s+(?P<strain>\w+),\s*a\s+[^,.]*?isolate of\s+"
    r"(?P<organism>[A-Z][a-z]+\s+[a-z]+)")
# "All antibiotic concentrations are expressed as microgram per milliliter."
UNIT_RE = re.compile(
    r"All antibiotic concentrations are expressed as\s+([^.]+)\.", re.I)
# "FOX: The antibiotic cefoxitin"
GLOSS_RE = re.compile(r"(?m)^([A-Z0-9]+):\s*[Tt]he antibiotic\s+(\w+)")
# "phages were applied at a multiplicity of infection (MOI) of 1:10 (bacteria:phage)"
MOI_BIO_RE = re.compile(
    r"For biofilm assays[^.]*?\(MOI\)\s*of\s*([\d:.]+)\s*\(([^)]*)\)", re.I)
MOI_PLK_RE = re.compile(r"For planktonic cultures, the MOI was\s*([\d:.]+)", re.I)

# block header text -> hours: "24hr (11/02)", "Day 3 (13/02)", "10 days (21/02)"
HOURS_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hour|hours)\b", re.I)
DAYS_RE = re.compile(r"^\s*(?:day\s*)?(\d+(?:\.\d+)?)\s*(?:day|days)?\b", re.I)
# "Fox 64 + M - 2" -> arm "Fox 64 + M", replicate 2
ARM_REP_RE = re.compile(r"^(?P<arm>.+?)\s*-\s*(?P<rep>\d+)\s*$")
# "Fox 16", "Tgc 0.25"
ABX_RE = re.compile(r"^(?P<code>[A-Za-z]+)\s+(?P<val>\d+(?:\.\d+)?)$")

# The workbooks abbreviate the Muddy phage to "M" in the combination labels.
# "M" is not in the README's glossary; the expansion is forced by the parallel
# labels ("Fox 16 + M" beside "Fox 16 + 8UZL") and is flagged on every row it
# is used on rather than made silently.
PHAGE = {"m": "Muddy", "muddy": "Muddy", "8uzl": "8UZL"}
CONTROL_TOKENS = {"growth", "growth control", "no phage control",
                  "ferrous ammonium sulfate"}

READOUT = "CFU"
NO_VOLUME = ("no plated volume, dilution or colony count appears in any "
             "workbook of this deposit, so no floor can be derived by "
             "arithmetic")


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _flat(s: str) -> str:
    return " ".join(str(s).split())


def _num(v):
    """A finite number, or None. Strings are never coerced."""
    if isinstance(v, bool) or isinstance(v, str):
        return None
    if isinstance(v, (int, float, np.number)) and np.isfinite(v):
        return float(v)
    return None


def _hours(label: str):
    """Hours from a timepoint block header, or None."""
    t = _flat(label)
    m = HOURS_RE.match(t)
    if m:
        return float(m.group(1))
    m = DAYS_RE.match(t)
    if m:
        return float(m.group(1)) * 24.0
    return None


# --------------------------------------------------------------------------
# what the deposit says about itself


def _readme(d: Path) -> dict:
    """Organism, strain, concentration unit, drug names, file -> figure map."""
    out = {"organism": "", "strain": "", "unit_words": "", "abx": {},
           "figs": {}, "text": ""}
    p = d / README
    if not p.exists():
        return out
    text = p.read_text(encoding="utf-8", errors="replace")
    out["text"] = text

    m = ORG_RE.search(text)
    if m:
        out["organism"] = m.group("organism")
        out["strain"] = m.group("strain")

    m = UNIT_RE.search(text)
    if m:
        out["unit_words"] = _flat(m.group(1))

    out["abx"] = {code.upper(): name.lower()
                  for code, name in GLOSS_RE.findall(text)}

    # "Figure 1:" ... "The file X.xlsx contains ..." -> {X.xlsx: {"1", ...}}
    heads = list(README_FIG_RE.finditer(text))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        key = ("S" if h.group(1).lower().startswith("supplemental") else "") \
            + h.group(2)
        for fname in README_FILE_RE.findall(text[h.end():end]):
            out["figs"].setdefault(fname, set()).add(key)
    return out


def _sentence(chunk: str, m: re.Match) -> str:
    """The sentence around a match, trimmed before the next figure/table call."""
    start = chunk.rfind(".", 0, m.start()) + 1
    tail = chunk.find(".", m.end())
    end = tail + 1 if 0 <= tail - m.end() <= 60 else m.end()
    s = _flat(chunk[start:end])
    s = re.split(r"\b(?:Table|Fig)\b", s)[0]
    return s.strip().rstrip(",;")


def _pdf(d: Path) -> dict:
    """{'lods': {figure key: (cfu_per_ml, quoted sentence)}, 'moi': {...}}."""
    out = {"lods": {}, "moi": {}, "read": False}
    p = d / PDF
    if not p.exists():
        return out
    try:
        import pymupdf
        doc = pymupdf.open(p)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
    except Exception:
        return out
    out["read"] = True

    marks = list(FIG_RE.finditer(text))
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        chunk = " ".join(text[mk.end():end].split())
        m = LOD_RE.search(chunk)
        if m:
            out["lods"].setdefault(mk.group(1).upper(),
                                   (10.0 ** float(m.group(1)),
                                    _sentence(chunk, m)))

    flat = " ".join(text.split())
    m = MOI_BIO_RE.search(flat)
    if m:
        out["moi"]["biofilm"] = "%s (%s)" % (m.group(1), _flat(m.group(2)))
    m = MOI_PLK_RE.search(flat)
    if m:
        out["moi"]["planktonic"] = m.group(1)
    return out


def _floor_for(fname: str, meta: dict) -> tuple[float, str]:
    """The floor for one workbook, and the evidence for it or against it."""
    figs = sorted(meta["readme"]["figs"].get(fname, ()))
    lods = meta["pdf"]["lods"]
    if not meta["pdf"]["read"]:
        return np.nan, ("no workbook of this deposit states a detection limit, "
                        "and %s could not be read; %s" % (PDF, NO_VOLUME))
    hits = {f: lods[f] for f in figs if f in lods}
    values = {v for v, _ in hits.values()}
    if len(values) == 1:
        f = sorted(hits)[0]
        val, quote = hits[f]
        return val, ('limit of detection stated in %s, legend of Fig. %s: "%s"; '
                     "the README maps %s to that figure. No workbook cell "
                     "states it, and %s"
                     % (PDF, f, quote, fname, NO_VOLUME))
    if len(values) > 1:
        return np.nan, ("the shipped manuscript states different detection "
                        "limits for the figures the README maps this file to "
                        "(%s), so none is used" % ", ".join(sorted(hits)))
    if figs:
        return np.nan, (
            "no detection limit anywhere in this workbook, and the legend of "
            "Fig. %s in %s, which the README maps this file to, states none "
            "either; the Fig. %s legend of the same manuscript does state one "
            "for bacteria, but it is not carried across to a figure that does "
            "not claim it. %s"
            % ("/".join(figs), PDF, "/".join(sorted(lods)) or "-", NO_VOLUME))
    return np.nan, (
        "no detection limit anywhere in this workbook, and the README does not "
        "map it to any figure of %s, so no legend applies to it; the Fig. %s "
        "legend states one for bacteria but it is not carried across. %s"
        % (PDF, "/".join(sorted(lods)) or "-", NO_VOLUME))


# --------------------------------------------------------------------------
# the three sheet layouts


def _condition(label: str, meta: dict, mode: str) -> dict:
    """Split a condition label into drug, concentration and notes."""
    lab = _flat(label)
    if lab.lower() in CONTROL_TOKENS:
        note = []
        if lab.lower() == "ferrous ammonium sulfate":
            note.append("ferrous ammonium sulfate is the deposit's phage "
                        "inactivation control, not an antimicrobial; the "
                        "sheet states no concentration for it")
        return {"drug": "", "concentration": np.nan, "notes": note}

    drugs, conc, unit, note = [], np.nan, "", []
    for part in lab.split("+"):
        tok = _flat(part)
        low = tok.lower()
        if low in PHAGE:
            drugs.append(PHAGE[low])
            if low == "m":
                note.append('"M" in the arm label is read as the Muddy phage, '
                            "from the parallel Fox/Tgc + 8UZL labels; the "
                            "README's glossary does not define the initial")
            moi = meta["pdf"]["moi"].get(mode, "")
            if moi:
                note.append("the shipped manuscript states the %s multiplicity "
                            "of infection as %s; it is a ratio, not a "
                            "concentration, so it is not put in the "
                            "concentration column" % (mode, moi))
            continue
        m = ABX_RE.match(tok)
        if m:
            code = m.group("code").upper()
            name = meta["readme"]["abx"].get(code, "")
            if not name:
                note.append('the README does not define the antibiotic code '
                            '"%s"; the label is kept verbatim in arm' % code)
                name = m.group("code")
            drugs.append(name)
            if np.isnan(conc):
                conc = float(m.group("val"))
                unit = meta["unit"]
            else:                       # two antibiotics, one column
                conc, unit = np.nan, ""
                note.append("more than one antibiotic concentration in this "
                            "arm; the single concentration column is left "
                            "blank and both are in arm")
            continue
        drugs.append(tok)
        note.append('condition token "%s" is not one this reader recognises; '
                    "it is passed through as written" % tok)

    return {"drug": " + ".join(x for x in drugs if x),
            "concentration": conc, "conc_unit": unit, "notes": note}


def _fig1_sheet(raw: pd.DataFrame, rel: str, sheet: str, meta: dict,
                floor: tuple) -> list[dict]:
    """DAY down column 0, an arm label every third column across the header."""
    hdr = next((i for i in range(len(raw))
                if _flat(raw.iat[i, 0]).upper() == "DAY"), None)
    if hdr is None:
        raise ValueError("%s/%s: no DAY header row" % (rel, sheet))
    labels = [(c, _flat(raw.iat[hdr, c])) for c in range(1, raw.shape[1])
              if isinstance(raw.iat[hdr, c], str) and _flat(raw.iat[hdr, c])]
    if not labels:
        raise ValueError("%s/%s: no arm labels" % (rel, sheet))
    bounds = [c for c, _ in labels] + [raw.shape[1]]
    days = [(i, _num(raw.iat[i, 0])) for i in range(hdr + 1, len(raw))]
    days = [(i, v) for i, v in days if v is not None]

    mode = "biofilm" if sheet.lower().startswith("biofilm") else "planktonic"
    rows = []
    for k, (lcol, label) in enumerate(labels):
        cond = _condition(label, meta, mode)
        for rep, c in enumerate(range(lcol, bounds[k + 1]), start=1):
            for i, day in days:
                v = raw.iat[i, c]
                val = _num(v)
                note = list(cond["notes"])
                if val is None:
                    if not isinstance(v, str) or not _flat(v):
                        continue
                    note.append('the cell reads "%s", not a number' % _flat(v))
                rows.append({
                    "source_file": rel, "sheet": sheet,
                    "arm": label,
                    "drug": cond["drug"],
                    "concentration": cond["concentration"],
                    "conc_unit": cond.get("conc_unit", ""),
                    "replicate": "%s phage-only/%d" % (mode, rep),
                    "time_h": day * 24.0,
                    "cfu_per_ml": val,
                    "floor_cfu_per_ml": floor[0], "floor_basis": floor[1],
                    "_mode": mode,
                    "_notes": note + [
                        "day converted to hours; the sheet's column is DAY",
                        "%s culture" % mode,
                        "the three columns under each arm are unlabelled in "
                        "the sheet; they are numbered in column order",
                        "the DAY 0 row repeats one set of three counts under "
                        "every arm: it is the shared starting inoculum, not "
                        "an independent reading per arm"] if day == 0 else
                    note + [
                        "day converted to hours; the sheet's column is DAY",
                        "%s culture" % mode,
                        "the three columns under each arm are unlabelled in "
                        "the sheet; they are numbered in column order"],
                })
    return rows


def _media_sheet(raw: pd.DataFrame, rel: str, sheet: str, meta: dict,
                 floor: tuple) -> list[dict]:
    """Time (hours) down column 0, a medium name per column in the next row."""
    hdr = next((i for i in range(len(raw))
                if _flat(raw.iat[i, 0]).lower().startswith("time")), None)
    if hdr is None:
        raise ValueError("%s/%s: no Time header row" % (rel, sheet))
    media_row = hdr + 1
    labels = [(c, _flat(raw.iat[media_row, c])) for c in range(1, raw.shape[1])
              if isinstance(raw.iat[media_row, c], str)
              and _flat(raw.iat[media_row, c])]
    if not labels:
        raise ValueError("%s/%s: no medium labels" % (rel, sheet))
    times = [(i, _num(raw.iat[i, 0])) for i in range(media_row + 1, len(raw))]
    times = [(i, v) for i, v in times if v is not None]

    mode = "biofilm" if rel.lower().startswith("biofilm") else "planktonic"
    no_zero = [] if any(t == 0 for _, t in times) else [
        "this sheet has no time-zero row: its first reading is %g h, so the "
        "starting density of these cultures is not in the deposit"
        % min(t for _, t in times)]
    seen: dict[str, int] = {}
    rows = []
    for c, medium in labels:
        seen[medium] = seen.get(medium, 0) + 1
        rep = seen[medium]
        for i, t in times:
            val = _num(raw.iat[i, c])
            if val is None:
                continue
            rows.append({
                "source_file": rel, "sheet": sheet,
                "arm": medium, "drug": "", "concentration": np.nan,
                "conc_unit": "",
                "replicate": "%s media/%d" % (mode, rep),
                "time_h": t,
                "cfu_per_ml": val,
                "floor_cfu_per_ml": floor[0], "floor_basis": floor[1],
                "_mode": mode,
                "_notes": [
                    "growth curve with no antimicrobial: the arm is the "
                    "growth medium, so drug is blank",
                    "%s culture" % mode,
                    "the header row reads \"%s\" and the times are hours as "
                    "the sheet gives them" % _flat(raw.iat[hdr, 0]),
                    "the three columns per medium are unlabelled in the "
                    "sheet; they are numbered in column order"] + no_zero,
            })
    return rows


def _combo_sheet(raw: pd.DataFrame, rel: str, sheet: str, meta: dict,
                 floor: tuple) -> list[dict]:
    """Timepoint blocks across the sheet: label column, GD01 CFU, PFU."""
    hdr = next((i for i in range(len(raw))
                if any(_flat(v) == "GD01 CFU" for v in raw.iloc[i])), None)
    if hdr is None:
        raise ValueError("%s/%s: no 'GD01 CFU' header" % (rel, sheet))
    blocks = [c for c in range(raw.shape[1]) if _flat(raw.iat[hdr, c]) == "GD01 CFU"]

    mode = "biofilm" if sheet.lower().startswith("biofilm") else "planktonic"
    rows = []
    for cfu_col in blocks:
        lab_col = cfu_col - 1
        head = _flat(raw.iat[hdr - 1, lab_col]) if hdr else ""
        hours = _hours(head)
        if hours is None:
            raise ValueError("%s/%s: cannot read a time from block header %r"
                             % (rel, sheet, head))
        for i in range(hdr + 1, len(raw)):
            lab = raw.iat[i, lab_col]
            if not isinstance(lab, str) or not _flat(lab):
                continue
            m = ARM_REP_RE.match(_flat(lab))
            if not m:
                continue
            arm, rep = m.group("arm"), int(m.group("rep"))
            cond = _condition(arm, meta, mode)
            v = raw.iat[i, cfu_col]
            val = _num(v)
            note = list(cond["notes"])
            if val is None:
                if not isinstance(v, str) or not _flat(v):
                    continue
                note.append('the CFU cell reads "%s", not a number' % _flat(v))
            rows.append({
                "source_file": rel, "sheet": sheet,
                "arm": arm,
                "drug": cond["drug"],
                "concentration": cond["concentration"],
                "conc_unit": cond.get("conc_unit", ""),
                "replicate": "%s phage-antibiotic/%d" % (mode, rep),
                "time_h": hours,
                "cfu_per_ml": val,
                "floor_cfu_per_ml": floor[0], "floor_basis": floor[1],
                "_mode": mode,
                "_notes": note + [
                    "%s culture" % mode,
                    'timepoint block header "%s"; the parenthesised date is '
                    "the sampling date, not a time" % head,
                    "the block's PFU column is a phage count and is not read"],
            })

    # the inoculum block at the foot: the starting count, i.e. time zero
    anchor = None
    for i in range(len(raw)):
        for c in range(raw.shape[1]):
            if _flat(raw.iat[i, c]).lower() == "gd01 inoculum":
                anchor = (i, c)
                break
        if anchor:
            break
    if anchor:
        i0, c0 = anchor
        rep = 0
        for i in range(i0 + 1, len(raw)):
            cell = raw.iat[i, c0]
            if isinstance(cell, str):
                break                       # "Average" ends the block
            val = _num(cell)
            if val is None:
                break
            rep += 1
            rows.append({
                "source_file": rel, "sheet": sheet,
                "arm": _flat(raw.iat[i0, c0]),
                "drug": "", "concentration": np.nan, "conc_unit": "",
                "replicate": "%s phage-antibiotic/%d" % (mode, rep),
                "time_h": 0.0,
                "cfu_per_ml": val,
                "floor_cfu_per_ml": floor[0], "floor_basis": floor[1],
                "_mode": mode,
                "_notes": [
                    "%s culture" % mode,
                    "the starting bacterial count, from the sheet's "
                    "\"GD01 Inoculum\" block; the deposit records one set of "
                    "three for the whole experiment, not one per arm, so it "
                    "is not attributed to any treatment",
                    "time zero is the reading itself; the sheet gives it no "
                    "time label, and the treated blocks begin at 24 h",
                    "the \"Average\" row below it is a derived mean and is "
                    "not read; the \"Muddy titer\" and \"8UZL titer\" cells "
                    "beside it are phage counts and are not read"],
            })
    return rows


SHEET_READER = {"fig1": _fig1_sheet, "media": _media_sheet, "combo": _combo_sheet}


def _family(fname: str, sheets: list[str]) -> tuple[str, list[str]]:
    """Which layout a workbook uses, and which of its sheets to read."""
    cfu = [s for s in sheets if s.strip().upper().endswith("CFU")]
    if cfu:
        return "fig1", cfu
    if "7H9vsCAMH" in fname:
        return "media", list(sheets)
    return "combo", list(sheets)


# --------------------------------------------------------------------------


def read(d: Path) -> pd.DataFrame:
    books = sorted(d.glob("*.xlsx"), key=lambda p: p.name)
    if not books:
        return empty()

    meta = {"readme": _readme(d), "pdf": _pdf(d)}
    words = meta["readme"]["unit_words"]
    # the README names the unit in words; "ug/mL" is that unit written the way
    # the corpus writes units, and the README's own wording travels in notes.
    meta["unit"] = "ug/mL" if "microgram per milliliter" in words.lower() else ""

    # A workbook byte-identical to one already read carries no new reading.
    digests: dict[str, str] = {}
    skipped: dict[str, str] = {}
    rows: list[dict] = []
    for p in books:
        h = _sha256(p)
        if h in digests:
            skipped[p.name] = digests[h]
            continue
        digests[h] = p.name

        xl = pd.ExcelFile(p)
        family, sheets = _family(p.name, xl.sheet_names)
        floor = _floor_for(p.name, meta)
        for s in sheets:
            raw = pd.read_excel(p, sheet_name=s, header=None)
            rows.extend(SHEET_READER[family](raw, p.name, s, meta, floor))

    if not rows:
        return empty()
    df = pd.DataFrame(rows)

    # Each reading once. A key repeated across files with the same value is a
    # figure sharing an experiment's controls; a key repeated with a different
    # value is a disagreement, and both are kept so it shows up as rows.
    df["_key"] = list(zip(df.arm, df.replicate, df.time_h))
    keep = np.ones(len(df), dtype=bool)
    extra = [""] * len(df)
    for key, g in df.groupby("_key", sort=False):
        if len(g) == 1:
            continue
        vals = {("nan" if pd.isna(v) else v) for v in g.cfu_per_ml}
        idx = list(g.index)
        others = sorted(set(g.source_file) - {df.at[idx[0], "source_file"]})
        if len(vals) == 1 and others:
            for j in idx[1:]:
                keep[df.index.get_loc(j)] = False
            extra[df.index.get_loc(idx[0])] = (
                "this reading is repeated verbatim in %s, which reports the "
                "same experiment under another figure; it is emitted once"
                % ", ".join(others))
        elif len(vals) > 1:
            for j in idx:
                extra[df.index.get_loc(j)] = (
                    "the deposit gives different values for this same arm, "
                    "replicate and time in %s; both are kept"
                    % ", ".join(sorted(set(g.source_file))))

    df["_extra"] = extra
    df = df[keep].copy()

    common = [
        "organism, strain and the antibiotic names are the README's own words",
        "readings are CFU per mL as the workbook writes them; no colony count, "
        "dilution or plated volume is given anywhere in the deposit",
        "all PFU columns and sheets in this deposit are phage counts and are "
        "not read into this corpus",
    ]
    if meta["unit"]:
        common.append('the README states "All antibiotic concentrations are '
                      'expressed as %s"' % words)
    for name, twin in sorted(skipped.items()):
        common.append("%s is byte-identical to %s (same sha256) and was not "
                      "read a second time" % (name, twin))

    df["notes"] = ["; ".join(x for x in list(n) + [e] + common if x)
                   for n, e in zip(df["_notes"], df["_extra"])]
    df["organism"] = meta["readme"]["organism"]
    df["strain"] = meta["readme"]["strain"]
    df["readout"] = READOUT
    df["tech_replicate"] = ""
    df["censored"] = ""

    return finish(df.drop(columns=["_key", "_notes", "_extra", "_mode"]),
                  "MERCHAN2025")
