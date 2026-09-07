"""PRETOMANID -- Figure 3 source data, nutrient-starved non-replicating M. tuberculosis.

Four workbooks, one per figure panel (3B, 3C, 3D, 3E), each with a single sheet
called "Figure 3". Every sheet has the same shape: a caption paragraph in the
first cell, a header row whose first entry is "Day", drug-arm labels spread
across merged cells with three unlabelled columns of replicates under each, and
one data row per sampling day.

This deposit is unusual and valuable: it states its own detection limit in the
sheet -- "L.O.D: limit of detection. 20 CFU/mL" -- and writes censored readings
as the literal string "0 (below L.O.D)".  Both are captured.  The floor is
PARSED out of the sheet text, not hard-coded, so a changed deposit is noticed.

The four panels overlap heavily: 3B is a strict subset of 3E, and the left half
of 3C repeats 3B while its right half repeats 3D.  Every file is still read, but
each row that repeats a reading already taken from an earlier file is flagged in
notes, so a downstream user can de-duplicate without having to rediscover this.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

SHEET = "Figure 3"

# The deposit's own words for a below-floor reading.
BLOD = re.compile(r"below\s*L\.?O\.?D", re.I)
# "L.O.D: limit of detection. 20 CFU/mL"
FLOOR_RE = re.compile(r"limit of detection[.:]?\s*([\d.]+)\s*CFU\s*/\s*mL", re.I)
# "Final drug concentrations of Q203 and pretomanid used were 100 nM and 1.2 uM respectively."
LIST_RE = re.compile(
    r"concentrations?\s+of\s+(?P<names>.+?)\s+used\s+were\s+(?P<vals>.+?)\s+respectively",
    re.I | re.S)
# "Pretomanid was used at a final concentration of 1.2 uM."
ONE_RE = re.compile(
    r"(?P<name>[A-Za-z0-9\-]+)\s+was used at a final concentration of\s+"
    r"(?P<val>[\d.]+)\s*(?P<unit>[a-zA-Zµμ]+M)", re.I)

# The sheets abbreviate; expand only what the caption itself spells out.
ALIAS = {"pmd": "pretomanid", "pretomanid": "pretomanid",
         "q203": "Q203", "nd-011992": "ND-011992"}


def _u(s: str) -> str:
    return s.replace("µ", "u").replace("μ", "u").strip()


def _caption_concentrations(text: str) -> dict:
    """Drug -> (value, unit) exactly as this sheet's caption states it."""
    out = {}
    m = LIST_RE.search(text)
    if m:
        names = re.split(r",\s*|\s+and\s+", m.group("names").strip())
        vals = re.split(r",\s*|\s+and\s+", m.group("vals").strip())
        if len(names) == len(vals):
            for n, v in zip(names, vals):
                vm = re.match(r"([\d.]+)\s*([a-zA-Zµμ]+M)", _u(v))
                key = ALIAS.get(n.strip().lower())
                if vm and key:
                    out[key] = (float(vm.group(1)), _u(vm.group(2)))
    for m in ONE_RE.finditer(text):
        key = ALIAS.get(m.group("name").strip().lower())
        if key:
            out[key] = (float(m.group("val")), _u(m.group("unit")))
    return out


def _drug_of(arm: str) -> str:
    """The arm label rewritten with the caption's own drug names. '' = control."""
    a = arm.strip()
    if a.lower().startswith("dmso"):
        return ""                      # vehicle control, no drug
    named = []
    for p in a.split("+"):
        p = re.sub(r"\s*\(.*?\)\s*", "", p).strip()   # drop "(100nM)"
        named.append(ALIAS.get(p.lower(), p))
    return " + ".join(x for x in named if x)


def _parse_sheet(path: Path, rel: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=SHEET, header=None)
    flat = [str(v) for v in raw.values.ravel() if isinstance(v, str)]
    text = " ".join(flat)

    caption = next((s for s in flat if s.strip().lower().startswith("figure")), "")
    conc = _caption_concentrations(caption)

    fm = FLOOR_RE.search(text)
    floor = float(fm.group(1)) if fm else np.nan
    floor_note = next((s for s in flat if FLOOR_RE.search(s)), "")
    basis = ('stated in the sheet: "%s"' % floor_note.strip() if fm else
             "the sheet states no detection limit")

    organism = "Mycobacterium tuberculosis" if re.search(
        r"M\.?\s*tuberculosis", caption, re.I) else ""
    sm = re.search(r"M\.?\s*tuberculosis\s+(H37Rv\S*)", caption, re.I)
    caption_strain = sm.group(1).rstrip(".,") if sm else ""

    # header row: the one whose first labelled cell is "Day"
    hdr = day_col = None
    for i in range(len(raw)):
        hit = [j for j, v in enumerate(raw.iloc[i]) if str(v).strip() == "Day"]
        if hit:
            hdr, day_col = i, hit[0]
            break
    if hdr is None:
        raise ValueError("%s: no 'Day' header row" % rel)

    # data rows: everything below the header whose Day cell is a number
    body = []
    for i in range(hdr + 1, len(raw)):
        try:
            day = float(raw.iat[i, day_col])
        except (TypeError, ValueError):
            continue
        if np.isfinite(day):
            body.append((i, day))
    if not body:
        raise ValueError("%s: no numeric Day rows" % rel)
    rows_idx = [i for i, _ in body]

    def is_value(v):
        if isinstance(v, str):
            return bool(BLOD.search(v))
        return isinstance(v, (int, float, np.number)) and np.isfinite(v)

    val_cols = [c for c in range(day_col + 1, raw.shape[1])
                if any(is_value(raw.iat[i, c]) for i in rows_idx)]
    if not val_cols:
        raise ValueError("%s: no value columns" % rel)

    # arm labels sit in the header row, one per block of replicate columns
    labels = [(c, str(raw.iat[hdr, c]).strip())
              for c in range(day_col + 1, raw.shape[1])
              if isinstance(raw.iat[hdr, c], str) and str(raw.iat[hdr, c]).strip()]
    if not labels:
        raise ValueError("%s: no arm labels in the header row" % rel)

    # an optional strain band one row above the header (panel 3C uses it)
    band = []
    if hdr > 0:
        band = [(c, str(raw.iat[hdr - 1, c]).strip())
                for c in range(day_col + 1, raw.shape[1])
                if isinstance(raw.iat[hdr - 1, c], str)
                and str(raw.iat[hdr - 1, c]).strip()]

    def band_of(col):
        lab = ""
        for c, v in band:
            if c <= col:
                lab = v
        return lab

    bounds = [c for c, _ in labels] + [raw.shape[1]]
    out = []
    for k, (lcol, label) in enumerate(labels):
        cols = [c for c in val_cols if lcol <= c < bounds[k + 1]]
        drug = _drug_of(label)
        single = [x for x in drug.split(" + ") if x]
        if len(single) == 1 and single[0] in conc:
            cval, cunit = conc[single[0]]
        else:
            cval, cunit = np.nan, ""
        strain = band_of(lcol) or caption_strain
        # this block's own first-timepoint readings identify which physical
        # experiment it belongs to; the panels reuse arm names across
        # experiments, so the signature keeps the overlap check honest
        i0 = body[0][0]
        sig = tuple(str(raw.iat[i0, c]) for c in cols)
        for i, day in body:
            for rep, c in enumerate(cols, start=1):
                v = raw.iat[i, c]
                note = ""
                if isinstance(v, str) and BLOD.search(v):
                    cfu, cens = 0.0, "yes"
                    note = 'the sheet reports this reading as "%s"' % v.strip()
                elif is_value(v):
                    cfu, cens = float(v), ""
                else:
                    continue
                out.append({
                    "source_file": rel, "sheet": SHEET,
                    "organism": organism, "strain": strain,
                    "drug": drug, "concentration": cval, "conc_unit": cunit,
                    "arm": label, "replicate": str(rep),
                    "time_h": day * 24.0,
                    "cfu_per_ml": cfu,
                    "censored": cens,
                    "floor_cfu_per_ml": floor, "floor_basis": basis,
                    "readout": "CFU",
                    "_key": (sig, drug, rep, day, cfu, cens),
                    "notes": note,
                })
    df = pd.DataFrame(out)
    df["_caption"] = caption.strip()
    return df


def read(d: Path) -> pd.DataFrame:
    # 3B, 3C, 3D sort before 3E, so the flag points at the file first seen
    files = sorted(d.glob("CFU_Nutrient_starvation_*.xlsx"), key=lambda p: p.name)
    if not files:
        return empty()

    df = pd.concat([_parse_sheet(p, p.name) for p in files], ignore_index=True)

    # flag readings that repeat one already taken from an earlier file
    seen = {}
    dup = []
    for key, src in zip(df["_key"], df["source_file"]):
        if key in seen and seen[key] != src:
            dup.append("this reading also appears in %s; the panels of this "
                       "deposit overlap" % seen[key])
        else:
            seen.setdefault(key, src)
            dup.append("")

    common = ("day converted to hours (source in days); the sheet does not say "
              "whether the three columns under each arm are biological or "
              "technical replicates, so they are numbered 1-3; plated volume is "
              "not stated anywhere in the deposit")
    df["notes"] = ["; ".join(x for x in (n, dp, cap, common) if x)
                   for n, dp, cap in zip(df["notes"], dup, df["_caption"])]

    # Panel 3D's caption says H37Rv, but its DMSO and PMD columns are the same
    # numbers as the H37Rv-delta-cydAB block of panel 3C.  The caption and the
    # data disagree, so the strain is left blank rather than guessed.
    is3d = df.source_file.str.contains("3D")
    df.loc[is3d, "strain"] = ""
    df.loc[is3d, "notes"] = df.loc[is3d, "notes"] + (
        "; strain left blank on purpose: this panel's caption says "
        '"M.tuberculosis H37Rv" but its DMSO and PMD columns are numerically '
        "identical to the H37Rv-delta-cydAB block of panel 3C, so the caption "
        "and the data disagree and neither is assumed")

    return finish(df.drop(columns=["_key", "_caption"]), "PRETOMANID")
