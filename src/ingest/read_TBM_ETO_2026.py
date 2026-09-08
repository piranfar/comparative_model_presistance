"""TBM_ETO_2026 -- AAC supplemental source data for "Ethionamide versus
Ethambutol-Containing First-Line Regimens for TB Meningitis" (PMC13336335).

WHAT IS IN THE DEPOSIT.  The retrieved package holds two files that matter:
aac.00190-26-s0001.xlsx (the figure source data) and aac.00190-26-s0002.docx
(the supplementary methods, figure legends and Table S1).  The workbook alone is
nearly mute -- its entire text is sixteen shared strings: the title, the organ
names and the regimen abbreviations -- so every piece of metadata this reader
carries is parsed out of the .docx, and nothing is parsed out of the main
article, which is not in the deposit.

  * Organism and strain come from the methods sentence "inoculated
    intracranially with titrated frozen stocks of M. tuberculosis H37Rv".
  * The unit comes from the Figure S1 legend: "Brain (A) and lung (B) bacterial
    burden (log10 CFU/g)".  So the sheet values are log10, the counts are per
    GRAM of tissue, and the organ each sheet belongs to is stated there too.
  * The regimen letters are expanded with the legend's own glossary, "HRZ (H,
    isoniazid; R, rifampin; Z, pyrazinamide), HRZE (E, ethambutol added), or
    HRZEt (Et, ethionamide added)".
  * The mouse doses come from Table S1.  They are per drug and there are three
    or four drugs per arm, so nothing goes in `concentration`; the arm's doses
    go in notes and the regimen label goes in `arm`.  Table S1 also gives a
    dexamethasone dose that no regimen letter accounts for and that the deposit
    never assigns to an arm; that is said in notes and put nowhere else.

THERE IS NO FLOOR, AND THAT IS THE POINT.  Nothing in either file names a limit
of detection, a plated volume, a dilution or a raw colony count -- the words
"detection", "limit", "LOD", "plate", "dilution", "homogenate" and "colony" do
not occur anywhere in the deposit.  That is CHECKED at read time, over every
text node of the workbook package (cells, comments, defined names) and over the
methods document, rather than asserted: if any of those words ever appears,
floor_basis says so loudly instead of repeating a denial that has gone stale.
The values arrive already reduced to log10 CFU per gram, so no floor can be
recovered by arithmetic either, and per-gram normalisation would in any case
give every animal a different one.  So floor_cfu_per_ml stays blank.

  Nineteen lung readings, all at week 6, are written as exactly 0.  On the
  log10 scale the deposit uses, 0 means 1 CFU/g, and that is what this reader
  records -- 10**0 -- because writing 0 into cfu_per_ml would change the
  deposited number rather than transcribe it.  Whether those animals yielded a
  single colony per gram or no colonies at all is not recoverable: the deposit
  plots them at the bottom of a log axis and says nothing more.  Every such row
  says so in notes.  This is precisely the ambiguity the corpus exists to count,
  so it is left standing rather than resolved by assumption.

WHAT THE SHEETS CONTAIN, and what is left out.

  Figure S1A (brain) and Figure S1B (lung) are the whole time course: week 0,
  2 and 6, with an untreated arm.  Figures 1B and 1C are the same numbers with
  the untreated arm and week 0 removed -- verified value by value at read time,
  in order -- so the readings are emitted once, from the S1 sheets, and each row
  records where else it is printed.  If a block ever stops matching, the rows of
  that block say so instead of the mismatch passing silently.

  Within Figure S1A and S1B the six week-0 values are printed four times, once
  under each arm heading, so that every plotted curve has a starting point.
  They are one set of six pre-treatment animals and are emitted once, under the
  arm "week 0 baseline"; the repetition is recorded in notes.

  Figures 2A and 2B are tissue and plasma drug concentrations, Figure S2 is
  serum GFAP in ug/mL and Figure S3 is percent area of Iba1 staining.  None is a
  viable count, and none is read.

UNVERIFIED, and every row says so in notes.  (1) The deposit never expands the
"W" of W2/W6.  The row labels 0/2/6 are read as WEEKS because Figures 1B/1C
label the very same columns W2 and W6 and the study counts its own treatment in
weeks -- "after two weeks of treatment" (Figure S2 legend), "treated for two
weeks" (Figure S3 legend).  That is an inference from the deposit's own words,
not a statement in it, and it sets every time_h by a factor of 168.  (2) The
deposit never says how long after infection treatment began, so the "0" row is
read as time zero of TREATMENT.  It is not the inoculum: the week-0 brain and
lung burdens differ by two logs, as an established intracranial infection would.
(3) Nor does the deposit say whether the same column position in the brain and
lung sheets is the same mouse; the animal counts match in every arm and week,
which is suggestive and nothing more.
"""
from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty

XLSX = "s0001.xlsx"
DOCX = "s0002.docx"

# sheet holding the full time course -> the figure that reprints part of it
SUPP_TO_MAIN = {"Figure S1A": "Figure 1B", "Figure S1B": "Figure 1C"}

HOURS_PER_WEEK = 168.0

# Every sheet in the deposit. The first four hold the counts (S1A/S1B read,
# 1B/1C their reprints); the last four are drug concentrations, serum GFAP and
# Iba1 staining -- no viable counts, checked against the legends, none read.
KNOWN_SHEETS = {"Figure S1A", "Figure S1B", "Figure 1B", "Figure 1C",
                "Figure 2A", "Figure 2B", "Figure S2", "Figure S3"}

ARM_ROW = 2        # row carrying the arm labels in Figure S1A / S1B
FIRST_DATA_ROW = 3  # first row carrying a week and its values

DOSE_UNIT_RE = re.compile(r"^\d[\d.–—-]*\s*mg/kg", re.I)


# --------------------------------------------------------------------------
# getting at the two files, unpacked or still zipped

def _bytes(d: Path, suffix: str) -> tuple[bytes, str] | None:
    """The named file and its path relative to the dataset dir."""
    hits = sorted(p for p in d.rglob("*" + suffix) if p.is_file())
    if hits:
        return hits[0].read_bytes(), hits[0].relative_to(d).as_posix()
    for z in sorted(d.glob("*.zip")):
        with zipfile.ZipFile(z) as zf:
            inner = [n for n in zf.namelist() if n.endswith(suffix)]
            if inner:
                return zf.read(inner[0]), f"{z.name}::{inner[0]}"
    return None


def _docx_text(blob: bytes) -> str:
    """Paragraph text of a .docx, one paragraph per line.

    EndNote stores its citation payload as base64 inside the run text; those
    runs are stripped so they cannot be mistaken for prose.
    """
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    txt = re.sub(r"</w:p>", "\n", xml)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = (txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
              .replace("&quot;", '"').replace("&apos;", "'"))
    txt = re.sub(r"[A-Za-z0-9+/=]{60,}", " ", txt)
    return "\n".join(ln.strip() for ln in txt.split("\n") if ln.strip())


# --------------------------------------------------------------------------
# everything the reader knows, parsed out of the supplementary methods

class Meta:
    def __init__(self, text: str, rel: str):
        self.rel = rel
        self.text = text
        flat = " ".join(text.split())

        self.organism = ("Mycobacterium tuberculosis"
                         if re.search(r"M\.\s*tuberculosis", flat) else "")
        sm = re.search(r"M\.\s*tuberculosis\s+([A-Za-z0-9]+)", flat)
        self.strain = sm.group(1) if sm else ""

        hm = re.search(r"(Female|Male)\s+([A-Za-z0-9/]+)\s+mice,\s*([^,]+)\s+old",
                       flat, re.I)
        self.host = (f"{hm.group(1).lower()} {hm.group(2)} mice, {hm.group(3)} old"
                     if hm else "")
        self.route = ("inoculated intracranially" if "intracranially" in flat
                      else "")

        # Figure S1 legend: the organs, the unit, and the regimen glossary
        cap = re.search(r"Figure S1\..*?(?=Figure S2\.)", flat, re.S)
        self.s1_caption = cap.group(0).strip() if cap else ""

        om = re.search(r"(\w+)\s*\(A\)\s*and\s*(\w+)\s*\(B\)", self.s1_caption)
        self.organ_of = ({"Figure S1A": om.group(1).capitalize(),
                          "Figure S1B": om.group(2).capitalize()}
                         if om else {})

        um = re.search(r"burden\s*\(\s*log\s*10\s*(CFU\s*/\s*g)\s*\)",
                       self.s1_caption, re.I)
        self.unit = re.sub(r"\s+", "", um.group(1)) if um else ""
        self.unit_quote = um.group(0) if um else ""

        # "HRZ (H, isoniazid; R, rifampin; Z, pyrazinamide)" and friends
        self.letters: dict[str, str] = {}
        for grp in re.findall(r"\(([^()]*)\)", self.s1_caption):
            for k, v in re.findall(
                    r"(?<![A-Za-z0-9])([A-Z][a-z]?),\s*([a-z][a-z]+)", grp):
                self.letters[k] = v

        self.doses = self._table_s1(text)

    @staticmethod
    def _table_s1(text: str) -> dict[str, str]:
        """Drug -> mouse dose, from Table S1's cells."""
        lines = text.split("\n")
        try:
            start = next(i for i, ln in enumerate(lines)
                         if ln.lower().startswith("table s1"))
        except StopIteration:
            return {}
        out, pending = {}, None
        for ln in lines[start + 1:]:
            if ln.upper().startswith("REFERENCES"):
                break
            if re.fullmatch(r"[A-Za-z][A-Za-z\- ]+", ln) and len(ln) < 30:
                low = ln.strip().lower()
                pending = None if low in ("drug", "mouse dose", "human dose") \
                    else low
            elif pending and DOSE_UNIT_RE.match(ln):
                out.setdefault(pending, ln.strip())
                pending = None
        return out

    def split_arm(self, arm: str) -> str:
        """'HRZEt' -> the drug names the legend gives those letters."""
        parts, i = [], 0
        while i < len(arm):
            two = arm[i:i + 2]
            if two in self.letters:
                parts.append(self.letters[two])
                i += 2
                continue
            one = arm[i]
            if one in self.letters:
                parts.append(self.letters[one])
            else:                       # a letter the legend never explains
                parts.append(one)
            i += 1
        return " + ".join(parts)

    def dose_note(self, arm: str) -> str:
        named = [p for p in self.split_arm(arm).split(" + ")]
        have = [f"{n} {self.doses[n]}" for n in named if n in self.doses]
        if not have:
            return "the deposit states no dose for this arm"
        miss = [n for n in named if n not in self.doses]
        s = ("Table S1 of the supplementary methods states the mouse doses: "
             + ", ".join(have))
        if miss:
            s += f"; no dose is stated for {', '.join(miss)}"
        # Table S1 also doses dexamethasone, which no regimen letter accounts
        # for and which the deposit never assigns to an arm. Saying so is the
        # honest move: these animals may have had a steroid alongside the
        # regimen, and `drug` must not pretend to know either way.
        extra = self.unassigned_doses()
        return s + ("; " + extra if extra else "")

    def unassigned_doses(self) -> str:
        """Drugs Table S1 doses that no regimen letter in the legend explains."""
        extra = sorted(set(self.doses) - set(self.letters.values()))
        if not extra:
            return ""
        return ("Table S1 also states a mouse dose for %s, which no regimen "
                "letter accounts for; the deposit never says which arms "
                "received %s, so it is left out of `drug`"
                % (", ".join("%s %s" % (n, self.doses[n]) for n in extra),
                   "them" if len(extra) > 1 else "it"))


# --------------------------------------------------------------------------
# the sheets

def _col_letter(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def _is_num(v) -> bool:
    return isinstance(v, (int, float, np.number)) and np.isfinite(v)


def _blocks(raw: pd.DataFrame) -> list[tuple[str, int, int]]:
    """(arm label, first column, one past last column) across the arm row."""
    lab = [(c, str(raw.iat[ARM_ROW, c]).replace("\xa0", " ").strip())
           for c in range(raw.shape[1])
           if isinstance(raw.iat[ARM_ROW, c], str)
           and str(raw.iat[ARM_ROW, c]).strip()]
    if not lab:
        raise ValueError("no arm labels in row %d" % ARM_ROW)
    bounds = [c for c, _ in lab] + [raw.shape[1]]
    return [(name, c0, bounds[k + 1]) for k, (c0, name) in enumerate(lab)]


def _weeks(raw: pd.DataFrame) -> list[tuple[int, float]]:
    out = []
    for r in range(FIRST_DATA_ROW, len(raw)):
        v = raw.iat[r, 0]
        if _is_num(v):
            out.append((r, float(v)))
    if not out:
        raise ValueError("no numeric week labels in column A")
    return out


def _cells(raw, row, c0, c1) -> list[tuple[int, float]]:
    return [(c, float(raw.iat[row, c])) for c in range(c0, c1)
            if _is_num(raw.iat[row, c])]


def _main_figure_columns(raw: pd.DataFrame) -> dict[tuple[str, float], list[float]]:
    """Figure 1B / 1C: a week band over an arm row over one column per arm."""
    week_row = next((r for r in range(len(raw))
                     if any(isinstance(raw.iat[r, c], str)
                            and re.fullmatch(r"W\d+", str(raw.iat[r, c]).strip())
                            for c in range(raw.shape[1]))), None)
    if week_row is None:
        return {}
    arm_row = week_row + 1
    bands = [(c, float(re.sub(r"\D", "", str(raw.iat[week_row, c]))))
             for c in range(raw.shape[1])
             if isinstance(raw.iat[week_row, c], str)
             and re.fullmatch(r"W\d+", str(raw.iat[week_row, c]).strip())]

    def week_of(col):
        wk = np.nan
        for c, w in bands:
            if c <= col:
                wk = w
        return wk

    out = {}
    for c in range(raw.shape[1]):
        lab = raw.iat[arm_row, c]
        if not (isinstance(lab, str) and lab.strip()):
            continue
        vals = [float(raw.iat[r, c]) for r in range(arm_row + 1, len(raw))
                if _is_num(raw.iat[r, c])]
        out[(lab.replace("\xa0", " ").strip(), week_of(c))] = vals
    return out


# Any word that would name a floor, a plated volume, a dilution or a raw count.
# The basis below CLAIMS none of them occurs in this deposit. That claim is the
# whole finding for this dataset, so it is checked against the files every time
# the reader runs rather than trusted from the day it was written: a re-deposit
# that added a methods line would otherwise slip past behind a stale denial.
FLOOR_WORDS = re.compile(
    r"detect\w*|limit\w*|L\.?O\.?D\b|plat(?:e|ed|ing)\b|dilut\w*|"
    r"colon(?:y|ies)|homogen\w*|CFU\s*/\s*m[lL]", re.I)

FLOOR_ABSENT = (
    "left blank: the deposit states no detection limit and no plated volume, "
    "and this reader verifies that rather than assuming it -- the words "
    "detection, limit, LOD, plate, dilution, colony and homogenate occur in "
    "neither file. Not in any of the %d distinct text values of the workbook "
    "package (its title, the organ names, the regimen and week labels, the "
    "numbers themselves, and no cell comments or defined names at all), and "
    "not in the supplementary methods (%s), which cover only the animal "
    "infection, the GFAP and Iba1 assays and the statistics. Values are "
    "deposited already reduced to log10 CFU/g, with no colony count, dilution "
    "or plated volume, so no floor follows by arithmetic either")

FLOOR_WORD_FOUND = (
    "left blank, but DO NOT TRUST THIS BLANK WITHOUT READING THE DEPOSIT: this "
    "reader found no stated limit, yet the deposit's text contains %s, which it "
    "did not contain when the reader was written. Someone must read those "
    "passages and decide whether a floor is now stated")


def _xml_text(blob: bytes) -> list[str]:
    """Every text node of an OOXML package: cells, comments, defined names.

    Markup is dropped rather than searched, so a tag or attribute name can never
    be mistaken for a word the depositor wrote.
    """
    out: list[str] = []
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for name in z.namelist():
            if not name.endswith(".xml"):
                continue
            body = z.read(name).decode("utf-8", "replace")
            out += [s.strip() for s in re.sub(r"<[^>]*>", "\n", body).split("\n")
                    if s.strip()]
    return out


def _floor_basis(xbytes: bytes, meta: "Meta") -> str:
    nodes = _xml_text(xbytes)
    hits = sorted({m.group(0).lower()
                   for m in FLOOR_WORDS.finditer("\n".join(nodes + [meta.text]))})
    if hits:
        return FLOOR_WORD_FOUND % ", ".join('"%s"' % h for h in hits)
    return FLOOR_ABSENT % (len(set(nodes)), meta.rel)

ZERO_NOTE = (
    "the sheet writes this reading as exactly 0 on its log10 scale, so the "
    "count transcribed here is 10**0 = 1 CFU/g; the deposit gives no detection "
    "limit and does not say whether this animal yielded one colony per gram or "
    "none, and this reader does not decide for it")


def read(d: Path) -> pd.DataFrame:
    got_x = _bytes(d, XLSX)
    got_d = _bytes(d, DOCX)
    if got_x is None:
        return empty()
    xbytes, xrel = got_x
    if got_d is None:
        raise ValueError("the supplementary methods (%s) are missing; every "
                         "unit, organism and dose this reader reports comes "
                         "from them" % DOCX)
    meta = Meta(_docx_text(got_d[0]), got_d[1])
    floor_basis = _floor_basis(xbytes, meta)
    if not meta.unit or not meta.organ_of:
        raise ValueError("the Figure S1 legend no longer states the organs and "
                         "the unit; refusing to assume them")

    book = pd.ExcelFile(io.BytesIO(xbytes))
    # The four sheets deliberately not read are named in the docstring; if the
    # deposit ever grows a sheet nobody has looked at, the reader must stop
    # rather than drop it silently -- an unread sheet of counts would be
    # missing readings that nothing in the corpus would show as missing.
    unexpected = [s for s in book.sheet_names if s not in KNOWN_SHEETS]
    if unexpected:
        raise ValueError("unexamined sheet(s) in %s: %s; the reader knows only "
                         "%s and will not decide on its own that a new sheet "
                         "holds no counts"
                         % (xrel, ", ".join(map(repr, unexpected)),
                            ", ".join(sorted(KNOWN_SHEETS))))
    shared = ("the supplementary methods (%s) supply the organism, strain, "
              "unit, regimen letters and doses; the workbook itself states "
              "none of them" % meta.rel)
    host = "; ".join(x for x in (meta.host, meta.route) if x)
    time_note = ("UNVERIFIED time unit: the sheet labels the rows 0, 2 and 6 "
                 "with no unit and the deposit never expands the \"W\" of the "
                 "W2/W6 headings that Figures 1B/1C put over the same columns. "
                 "They are read as WEEKS because the study counts its own "
                 "treatment in weeks -- \"after two weeks of treatment\" "
                 "(Figure S2 legend), \"treated for two weeks\" (Figure S3 "
                 "legend) -- and converted at 168 h per week; that is an "
                 "inference from the deposit's words, not a statement in it, "
                 "and it scales every time_h by 168. The deposit also never "
                 "says how long after infection treatment began, so the 0 row "
                 "is treatment time zero and not the inoculum")
    unit_note = ("the deposit reports %s, quoting the Figure S1 legend: \"%s\"; "
                 "cfu_per_ml therefore holds a count per GRAM of tissue, not "
                 "per mL, and no volume is invented to convert it"
                 % (meta.unit, meta.unit_quote))
    animal_note = ("in vivo terminal organ count: each mouse is read once, so "
                   "the columns of a block are different animals and a column "
                   "position does not link a week-2 reading to a week-6 one")
    pairing_note = ("the brain and lung sheets carry the same number of animals "
                    "in every arm and week; the same column position may be the "
                    "same mouse's other organ, but the deposit does not say so")

    rows: list[dict] = []
    for sheet, main in SUPP_TO_MAIN.items():
        if sheet not in book.sheet_names:
            raise ValueError("sheet %r is missing from %s" % (sheet, xrel))
        raw = book.parse(sheet, header=None)
        organ = meta.organ_of[sheet]
        blocks = _blocks(raw)
        weeks = _weeks(raw)

        # Figures 1B / 1C reprint the treated blocks; check them value by value
        reprint = (_main_figure_columns(book.parse(main, header=None))
                   if main in book.sheet_names else {})
        row_of_week = {w: r for r, w in weeks}
        agree: dict[tuple[str, float], bool] = {}
        for (arm, wk), vals in reprint.items():
            hit = [b for b in blocks if b[0] == arm]
            if not hit or wk not in row_of_week:
                agree[(arm, wk)] = False
                continue
            _, c0, c1 = hit[0]
            agree[(arm, wk)] = vals == [v for _, v
                                        in _cells(raw, row_of_week[wk], c0, c1)]

        for r, wk in weeks:
            per_arm = {arm: _cells(raw, r, c0, c1) for arm, c0, c1 in blocks}
            baseline = wk == 0 and len({tuple(v for _, v in cells)
                                        for cells in per_arm.values()
                                        if cells}) == 1
            emitted_baseline = False

            for arm, c0, c1 in blocks:
                cells = per_arm[arm]
                if not cells:
                    continue
                if baseline:
                    if emitted_baseline:
                        continue
                    emitted_baseline = True
                    label, drug = "week 0 baseline", ""
                else:
                    label = arm
                    drug = "" if arm.lower() == "untreated" \
                        else meta.split_arm(arm)

                for c, v in cells:
                    note = [unit_note, time_note, animal_note, pairing_note,
                            shared]
                    note.append("cell %s%d of sheet %r, log10 value %.8g"
                                % (_col_letter(c), r + 1, sheet, v))
                    if baseline:
                        note.append(
                            "the sheet prints these same six week-0 values "
                            "under all four arm headings (%s) so that each "
                            "plotted curve has a starting point; they are one "
                            "set of pre-treatment animals and are emitted once"
                            % ", ".join(a for a, _, _ in blocks))
                    elif wk == 0:
                        note.append("the week-0 columns of the four arm blocks "
                                    "are not identical in this sheet, so each "
                                    "block's week-0 readings are kept under its "
                                    "own arm label rather than merged")
                    if not baseline:
                        key = (arm, wk)
                        if key in agree and agree[key]:
                            note.append("this reading is also printed in sheet "
                                        "%r, whose %s W%g column is identical "
                                        "to this block value for value; it is "
                                        "emitted once, from %r"
                                        % (main, arm, wk, sheet))
                        elif key in agree:
                            note.append("sheet %r reprints a %s W%g column that "
                                        "does NOT match this block; the deposit "
                                        "disagrees with itself and neither "
                                        "version is preferred here"
                                        % (main, arm, wk))
                    if drug:
                        note.append(meta.dose_note(arm))
                    else:
                        note.append("no drug: this is an untreated reading"
                                    if not baseline else
                                    "no drug: the reading precedes treatment")
                    if host:
                        note.append(host)
                    if v == 0:
                        note.append(ZERO_NOTE)

                    rows.append({
                        "source_file": xrel,
                        "sheet": sheet,
                        "organism": meta.organism,
                        "strain": meta.strain,
                        "drug": drug,
                        "concentration": np.nan,
                        "conc_unit": "",
                        "arm": label,
                        "replicate": "%s_%s_W%g_c%02d" % (
                            organ.lower(), label.replace(" ", "-"), wk,
                            c - c0 + 1),
                        "tech_replicate": "",
                        "time_h": wk * HOURS_PER_WEEK,
                        "colonies": np.nan,
                        "dilution": np.nan,
                        "plated_volume_ul": np.nan,
                        "cfu_per_ml": float(10.0 ** v),
                        "floor_cfu_per_ml": np.nan,
                        "floor_basis": floor_basis,
                        "readout": "CFU per gram of %s tissue" % organ.lower(),
                        "notes": "; ".join(note),
                    })

    return pd.DataFrame(rows)
