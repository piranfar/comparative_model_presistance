"""SHEE2026_SENOLYTIC -- Nat Commun 41467-026-72874-y source data: a senolytic
(DQF) with and without an antitubercular (ETH) in Mtb-infected mice, plus two in
vitro macrophage infection assays.

WHAT IS HERE.  Two workbooks, 46 sheets, of which seven carry viable counts.  A
sheet is read only where the deposit itself says the readout is CFU -- either the
word "CFU" appears on the sheet, or the sheet deposits its own raw plate counts.
On that test the CFU sheets are

    Fig. 5f        in vivo, Veh / DQF / ETH / DQF+ETH, three mouse groups
    Fig. 5g        the same design in a second organ, WITH raw plate counts
    Fig. 5b        in vivo, no arm labelled, Day 1 and Day 21 lung and spleen
    Fig. 1g        in vitro macrophage, raw counts, no drug
    S. Fig. 7a,b   in vivo log10 CFU, lung and spleen, Veh / DQF / Eth
    S. Fig. 7d-f   in vitro BMDM, Day 0 / Untreated / +DQF (10uM), raw counts
    S. Fig. 5a     in vitro BMDM, Day 0 / Day 1, untreated / TNF, raw counts

Fig. 2b, Fig. 2c, Fig. 3b and Fig. 3c are almost certainly organ CFU as well --
per-animal values of 1e4 to 1e8 at weeks 2/4/6 and days 10/20 -- but nothing on
those four sheets says so, they carry no raw counts, and Fig. 3d and Fig. 3e use
the same "Lung"/"Spleen" row labels for flow-cytometry percentages.  They are
left out rather than assumed.

THE FLOOR.  Neither workbook states a limit of detection, a plated volume or a
plating fraction, in any cell of any sheet.  floor_cfu_per_ml is therefore blank
on every row.  What the deposit does give is dilution labels and, on four sheets,
the raw colony counts behind the plotted values, and those two reconcile exactly:

    plotted CFU = colonies x 10^(dilution exponent + 1)

on Fig. 5g, S. Fig. 7d-f, S. Fig. 5a and Fig. 1g alike (exponent 3 is written on
the last three as "Dilution=-3").  The extra factor of ten is the deposit's own
arithmetic and is recorded in floor_basis, but the deposit never says where it
comes from -- no plated volume, no homogenate volume, no fraction -- so it fixes
no detection limit and none is filled.

THE BELOW-LIMIT ENCODING, which is why this deposit was flagged.  Sheet Fig. 5g,
the 2 wpi row of the B6.Sst1S block, contains the literal strings

    "0(=1)"    in the Veh column, in two cells

and sheet Fig. 5f, the Week 8 row of the B6.Sst1S block, contains

    "0 (1)"    in the DQF+ETH column, with the cell below it reading
               "No CFU detected in Neat dilution"

Fig. 5g's own raw block confirms the reading: 0 colonies at dil=Neat for animals
F1 and F4 at 2 wpi.  So the deposit writes a zero count as zero and states beside
it the value it is plotted at, and that value is ONE.  Those three cells are
carried through as cfu_per_ml = 0, censored = "yes" (the deposit's own claim
about them, not an inference from a floor this reader does not have), with the
literal cell text quoted in notes.

TIME.  The in vivo clock is time after INFECTION, not after first dose: Fig. 5g's
raw block labels its rows "2 wpi", "5 wpi", "8 wpi", and nothing in either
workbook says when dosing began.  time_h is hours after infection and every row
says so.  Where a sheet gives a bare number the unit is taken from evidence
inside the deposit and that evidence is written on the row.  Where the deposit
gives no timepoint at all -- the treated blocks of S. Fig. 7a,b, the "Untreated"
and "+DQF" blocks of S. Fig. 7d-f, the second row label of Fig. 1g -- time_h is
left blank rather than guessed.

IN VIVO COUNTS ARE PER ORGAN.  cfu_per_ml carries a per-organ burden on every in
vivo row.  No volume is stated and none is invented.

ARM.  Where a sheet crosses a mouse group or an organ with a treatment label, arm
joins the deposit's own two labels with " / " -- "B6.Sst1S / DQF+ETH", "Veh /
Lung" -- so both axes survive in one column.  Both halves are verbatim.

WHAT THE DEPOSIT NEVER SAYS.  It never spells out "DQF" or "ETH".  The only sheet
carrying full compound names is S. Fig. 6a, an in vitro MIC panel reporting
"Dasatinib MIC 90/Day6", "Quercetin MIC 90/Day6", "Fisetin MIC 90/Day6",
"Rifampicin MIC 90/Day6" and "Ethambutol MIC 90/Day6".  That is reported as what
the deposit contains; the abbreviations are left unexpanded and no dose is
assigned to them.  The organism is written "Mtb", and only on sheets Fig. 2g,
Fig. 2h and S. Fig. 5b; no strain appears anywhere in either workbook.

Licence: CC BY-NC-ND 4.0.  Values are read here, not redistributed from here.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty, finish

FIG = "Source data Fig1-7.xlsx"
SUP = "Source data Supp. Figs.xlsx"

ORGANISM = "Mtb"

FLOOR_BASIS = (
    "no floor: neither workbook states a limit of detection, a plated volume or "
    "a plating fraction in any cell of any of its 46 sheets. The only plating "
    "information deposited is the dilution labels (dil=Neat..dil=4 on Fig. 5g, "
    '"Dilution=-3" on Fig. 1g and S. Fig. 7d-f) together with the raw colony '
    "counts behind the plotted values, and those reconcile exactly as "
    "CFU = colonies x 10^(dilution exponent + 1); the deposit never says where "
    "that extra factor of ten comes from, so it fixes no detection limit and "
    "none is supplied here"
)

ABBREV_NOTE = (
    'the deposit never defines "DQF" or "ETH"; the only sheet in it that gives '
    "full compound names is S. Fig. 6a, an in vitro MIC panel reporting "
    '"Dasatinib MIC 90/Day6", "Quercetin MIC 90/Day6", "Fisetin MIC 90/Day6", '
    '"Rifampicin MIC 90/Day6" and "Ethambutol MIC 90/Day6"'
)
ORG_NOTE = (
    'the organism is written "Mtb" on sheets Fig. 2g, Fig. 2h and S. Fig. 5b of '
    "this deposit and nowhere on the CFU sheets themselves; no strain is named "
    "anywhere in either workbook"
)
INVIVO_NOTE = (
    "in vivo: cfu_per_ml holds a per-organ burden, not a density; the deposit "
    "states no volume and none is derived"
)
PI_NOTE = (
    "time_h is hours after INFECTION, not after first dose: Fig. 5g's raw-count "
    'block labels the same rows "2 wpi", "5 wpi", "8 wpi", and neither workbook '
    "says when dosing began"
)
CONV_NOTE = (
    "this sheet's plotted values equal colonies x 10^(dilution exponent + 1); "
    "the deposit states no plated volume, so the extra factor of ten is "
    "unexplained"
)
INVITRO_NOTE = (
    "in vitro macrophage infection; the group label names the mouse the "
    "macrophages came from, not a treatment"
)

# "0(=1)" on Fig. 5g, "0 (1)" on Fig. 5f: a zero count with the value it is
# plotted at written beside it.
ZERO_PLACEHOLDER = re.compile(r"^\s*0\s*\(\s*=?\s*1\s*\)\s*$")
DAY_RE = re.compile(r"^day\s*(-?[\d.]+)", re.I)
WEEK_RE = re.compile(r"^week\s*(-?[\d.]+)", re.I)
WPI_RE = re.compile(r"^(\d+)\s*wpi$", re.I)
DIL_RE = re.compile(r"^dil(?:ution)?\s*=\s*(neat|-?\d+)$", re.I)
F_RE = re.compile(r"^F\d+$", re.I)


def _s(v) -> str:
    """A cell as text, with the sheets' non-breaking spaces normalised."""
    if not isinstance(v, str):
        return ""
    return v.replace("\xa0", " ").strip()


def _num(v):
    """A cell as a number, or None. The two zero placeholders count as zero."""
    if isinstance(v, str):
        return 0.0 if ZERO_PLACEHOLDER.match(v.replace("\xa0", " ")) else None
    if isinstance(v, (int, float, np.number)) and pd.notna(v):
        return float(v)
    return None


def _label_hours(label: str, bare_unit: str = "") -> float:
    """Hours from a row or band label. bare_unit says what a bare number means."""
    m = DAY_RE.match(label)
    if m:
        return float(m.group(1)) * 24.0
    m = WEEK_RE.match(label)
    if m:
        return float(m.group(1)) * 168.0
    try:
        n = float(label)
    except ValueError:
        return float("nan")
    if bare_unit == "day":
        return n * 24.0
    if bare_unit == "week":
        return n * 168.0
    return float("nan")


def _spans(raw: pd.DataFrame, row: int, first_col: int = 1, stop_col=None):
    """(label, start, stop) for each labelled column band in a header row."""
    hi = raw.shape[1] if stop_col is None else stop_col
    hits = [(c, _s(raw.iat[row, c])) for c in range(first_col, hi)
            if _s(raw.iat[row, c])]
    return [(lab, c, hits[k + 1][0] if k + 1 < len(hits) else hi)
            for k, (c, lab) in enumerate(hits)]


def _key(label: str) -> str:
    """A label reduced to a comparison key: the sheets vary case and spacing
    between their processed and raw blocks ("ETH" against "Eth", "DQF+ ETH"
    against "DQF+Eth"). Only the lookup uses this; every emitted value stays
    verbatim."""
    return re.sub(r"\s+", "", label).lower()


def _label0(raw: pd.DataFrame, i: int) -> str:
    """The row label in column 0. Several sheets write it as a bare number."""
    t = _s(raw.iat[i, 0])
    if t:
        return t
    n = _num(raw.iat[i, 0])
    return "" if n is None else "%g" % n


def _row_labels(raw: pd.DataFrame, i: int):
    return [(c, _s(raw.iat[i, c])) for c in range(raw.shape[1])
            if _s(raw.iat[i, c])]


def _has_number(raw: pd.DataFrame, i: int, first_col: int = 1) -> bool:
    return any(_num(raw.iat[i, c]) is not None
               for c in range(first_col, raw.shape[1]))


def _base(**kw) -> dict:
    row = {"organism": ORGANISM, "strain": "", "drug": "",
           "concentration": np.nan, "conc_unit": "", "arm": "",
           "replicate": "", "tech_replicate": "", "time_h": np.nan,
           "colonies": np.nan, "dilution": np.nan,
           "plated_volume_ul": np.nan, "cfu_per_ml": np.nan,
           "censored": "", "floor_cfu_per_ml": np.nan,
           "floor_basis": FLOOR_BASIS, "readout": "CFU", "notes": ""}
    row.update(kw)
    return row


def _join(parts) -> str:
    return "; ".join(p for p in parts if p)


def _drug_of(arm_label: str):
    """(drug, concentration, unit) from an arm label, in the sheet's own words."""
    a = arm_label.strip()
    if a.lower() in ("", "veh", "vehicle", "untreated", "ut", "day 0"):
        return "", np.nan, ""
    m = re.match(r"^\+?\s*(TNF)\s*\(\s*([\d.]+)\s*(ng/ml)\s*\)$", a, re.I)
    if m:
        return m.group(1), float(m.group(2)), m.group(3)
    m = re.match(r"^\+?\s*(DQF)\s*\(\s*([\d.]+)\s*[uµμ]M\s*\)$", a, re.I)
    if m:
        return m.group(1), float(m.group(2)), "uM"
    # the sheets write "DQF+ETH" and "DQF+ ETH" for the same arm; the arm label
    # stays verbatim, only the drug token is whitespace-collapsed
    return re.sub(r"\s*\+\s*", "+", a), np.nan, ""


# ---------------------------------------------------------------------------
# Fig. 5g's raw plate counts, the lookup the plotted values are matched against
# ---------------------------------------------------------------------------
def _fig5g_raw(raw: pd.DataFrame, start: int) -> dict:
    """(group, hours, arm, replicate index) -> [(dilution exponent, colonies)]."""
    runs, cur = [], []
    for i in range(start, len(raw)):
        if F_RE.match(_s(raw.iat[i, 0])):
            cur.append(i)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)

    lookup: dict = {}
    for run in runs:
        dil_row = None
        for i in range(run[0] - 1, start - 1, -1):
            if sum(bool(DIL_RE.match(t)) for _, t in _row_labels(raw, i)) >= 2:
                dil_row = i
                break
        if dil_row is None:
            continue
        group = _s(raw.iat[dil_row, 0])

        wpi_row = None
        for i in range(dil_row - 1, start - 1, -1):
            if any(WPI_RE.match(t) for _, t in _row_labels(raw, i)):
                wpi_row = i
                break
        wpi = _spans(raw, wpi_row) if wpi_row is not None else []

        def is_arm_row(i):
            labs = [t for _, t in _row_labels(raw, i)]
            if len(labs) < 2:
                return False
            return not any(DIL_RE.match(t) or WPI_RE.match(t) or F_RE.match(t)
                           for t in labs)

        arm_row = None
        if wpi_row is not None:
            for i in range(wpi_row + 1, dil_row):
                if is_arm_row(i):
                    arm_row = i
                    break
        if arm_row is None:
            for i in range(run[-1] + 1, min(run[-1] + 5, len(raw))):
                if is_arm_row(i):
                    arm_row = i
                    break
        arms = _spans(raw, arm_row) if arm_row is not None else []

        def band(spans, col, default=""):
            for lab, a, b in spans:
                if a <= col < b:
                    return lab
            return default

        for k, i in enumerate(run, start=1):
            for c in range(1, raw.shape[1]):
                n = _num(raw.iat[i, c])
                dm = DIL_RE.match(_s(raw.iat[dil_row, c]))
                if n is None or dm is None:
                    continue
                d = dm.group(1).lower()
                exp = 0 if d == "neat" else abs(int(d))
                m = WPI_RE.match(band(wpi, c))
                hours = float(m.group(1)) * 168.0 if m else float("nan")
                key = (_key(group), hours, _key(band(arms, c)), k)
                lookup.setdefault(key, []).append((exp, n))
    return lookup


def _match_raw(cands, value):
    """The one deposited plate count that reproduces this plotted value."""
    hits = [(e, n) for e, n in cands
            if abs(n * 10.0 ** (e + 1) - value) <= max(0.5, abs(value) * 1e-9)]
    if len(hits) == 1:
        return hits[0][1], 10.0 ** hits[0][0], ""
    if not cands:
        return np.nan, np.nan, "no raw plate count is deposited for this reading"
    shown = ", ".join("%g colonies at dil=%s" % (n, "Neat" if e == 0 else e)
                      for e, n in cands)
    if not hits:
        return np.nan, np.nan, (
            "FINDING: the raw counts deposited for this animal and arm (%s) do "
            "not reproduce the plotted value %g under this sheet's own "
            "conversion CFU = colonies x 10^(dilution exponent + 1); colonies "
            "and dilution are left blank rather than forced" % (shown, value))
    return np.nan, np.nan, (
        "more than one deposited plate count reproduces the plotted value (%s); "
        "colonies and dilution are left blank" % shown)


def _lookup_raw(lookup, group, hours, arm_lab, k, value):
    """Find the deposited plate count behind one plotted value.

    Tried in order: the arm's own label; the unlabelled column the raw block
    uses at its earlier timepoint; and a label the raw block writes differently
    from the processed block ("Vehicle" where the processed block says "Veh").
    A candidate is accepted only when its arithmetic reproduces the plotted
    value exactly, so a wrong pairing cannot slip through as a number.

    Returns (colonies, dilution, why_not, how) -- at most one of the last two
    is non-empty.
    """
    gk, ak = _key(group), _key(arm_lab)
    exact = lookup.get((gk, hours, ak, k), [])
    blank = lookup.get((gk, hours, "", k), [])
    tried = [(exact, "")]
    if blank:
        tried.append((blank, "the raw-count block labels no arm at this "
                             "timepoint; its single unlabelled column is the "
                             "only candidate and it reproduces the plotted "
                             "value exactly"))
    near = [(a, v) for (g, h, a, kk), v in lookup.items()
            if g == gk and h == hours and kk == k and a not in ("", ak)
            and min(len(a), len(ak)) >= 3
            and ("+" in a) == ("+" in ak)   # never pair a single arm with a
            and (a.startswith(ak) or ak.startswith(a))]   # combination arm
    if len(near) == 1:
        tried.append((near[0][1],
                      'the raw-count block writes this arm "%s" where the '
                      'plotted block writes it "%s"; the pairing is accepted '
                      "only because its arithmetic reproduces the plotted "
                      "value exactly" % (near[0][0], arm_lab)))

    for cands, how in tried:
        col, dil, _why = _match_raw(cands, value)
        if np.isfinite(col):
            return col, dil, "", how
    pool = next((c for c, _ in reversed(tried) if c), [])
    col, dil, why = _match_raw(pool, value)
    return col, dil, why, ""


# ---------------------------------------------------------------------------
# Fig. 5f and Fig. 5g -- the treatment experiment
# ---------------------------------------------------------------------------
def _is_group_header(raw: pd.DataFrame, i: int) -> bool:
    """Text in column 0, two or more further labels, and no numbers at all."""
    if not _s(raw.iat[i, 0]):
        return False
    labs = _row_labels(raw, i)
    return len(labs) >= 3 and not _has_number(raw, i, 0)


def _read_fig5fg(path: Path, rel: str, sheet: str) -> list:
    raw = pd.read_excel(path, sheet_name=sheet, header=None)

    stop = len(raw)
    for i in range(len(raw)):
        if "raw data counts" in _s(raw.iat[i, 0]).lower():
            stop = i
            break
    lookup = _fig5g_raw(raw, stop) if stop < len(raw) else {}

    # the sheet's own annotation of the cell it writes as "0 (1)"
    zero_notes = {}
    for i in range(len(raw)):
        for c in range(raw.shape[1]):
            t = _s(raw.iat[i, c])
            if t.lower().startswith("no cfu detected"):
                zero_notes[(i - 1, c)] = t

    bare = "week" if sheet == "Fig. 5g" else "day"
    unit_evidence = (
        "this sheet labels its rows with bare numbers; they are read as weeks "
        "after infection because its own raw-count block labels the same rows "
        '"2 wpi", "5 wpi" and "8 wpi"' if sheet == "Fig. 5g" else
        "this block labels its rows with bare numbers; they are read as days "
        "because the row labelled 1 holds values identical to the \"Day 1\" "
        "rows of the other two blocks of this sheet, and because 28 and 56 are "
        "the 4 wpi and 8 wpi rows Fig. 5g gives for this same mouse group")

    rows, group, arms = [], "", []
    for i in range(stop):
        if _is_group_header(raw, i):
            group, arms = _s(raw.iat[i, 0]), _spans(raw, i)
            continue
        label = _label0(raw, i)
        if not label or not arms or not _has_number(raw, i):
            continue
        hours = _label_hours(label, bare)
        if not np.isfinite(hours):
            continue
        bare_label = not (DAY_RE.match(label) or WEEK_RE.match(label))
        for arm_lab, a, b in arms:
            k = 0
            for c in range(a, b):
                v = raw.iat[i, c]
                n = _num(v)
                if n is None:
                    continue
                k += 1
                drug, conc, unit = _drug_of(arm_lab)
                note = [ORG_NOTE, INVIVO_NOTE, PI_NOTE, ABBREV_NOTE,
                        "the sheet does not name the organ; Fig. 5f and Fig. 5g "
                        "are two different organs and neither says which",
                        'the sheet writes this timepoint as "%s"' % label]
                if bare_label:
                    note.append(unit_evidence)
                cens = ""
                colonies = dilution = np.nan
                if isinstance(v, str):
                    cens = "yes"
                    note.append(
                        'FINDING: the sheet writes this reading as the literal '
                        'cell "%s" -- a zero count with the value it is plotted '
                        "at written beside it, and that value is 1, not the 10 "
                        "of any stated detection limit (the deposit states "
                        "none)" % _s(v))
                    if (i, c) in zero_notes:
                        note.append('the cell below it reads "%s", which states '
                                    "the colonies (0) and the dilution (neat)"
                                    % zero_notes[(i, c)])
                        colonies, dilution = 0.0, 1.0
                if lookup:
                    col, dil, why, extra = _lookup_raw(
                        lookup, group, hours, arm_lab, k, n)
                    if extra:
                        note.append(extra)
                    if np.isfinite(col):
                        colonies, dilution = col, dil
                        note.append(
                            "colonies and dilution come from this sheet's own "
                            "raw-count block, matched to the plotted value by "
                            "its conversion CFU = colonies x 10^(dilution "
                            "exponent + 1)")
                        note.append(CONV_NOTE)
                    elif why:
                        note.append(why)
                rows.append(_base(
                    source_file=rel, sheet=sheet,
                    drug=drug, concentration=conc, conc_unit=unit,
                    arm="%s / %s" % (group, arm_lab) if group else arm_lab,
                    replicate=("F%d" % k) if lookup else str(k),
                    time_h=hours, colonies=colonies, dilution=dilution,
                    cfu_per_ml=n, censored=cens, notes=_join(note)))
    return rows


# ---------------------------------------------------------------------------
# Fig. 5b -- Day 1, and Day 21 lung and spleen; no treatment arm is labelled
# ---------------------------------------------------------------------------
def _read_fig5b(path: Path, rel: str) -> list:
    raw = pd.read_excel(path, sheet_name="Fig. 5b", header=None)
    rows = []
    for i in range(len(raw)):
        label = _s(raw.iat[i, 0])
        m = DAY_RE.match(label)
        if not m:
            continue
        hours = float(m.group(1)) * 24.0
        organ = re.sub(r"^day\s*[\d.]+\s*", "", label, flags=re.I).strip()
        k = 0
        for c in range(1, raw.shape[1]):
            n = _num(raw.iat[i, c])
            if n is None:
                continue
            k += 1
            rows.append(_base(
                source_file=rel, sheet="Fig. 5b", arm=organ,
                replicate=str(k), time_h=hours, cfu_per_ml=n,
                notes=_join([
                    ORG_NOTE, INVIVO_NOTE, PI_NOTE,
                    'the sheet\'s own row label is "%s"' % label,
                    "this sheet labels no treatment arm and no mouse group, so "
                    "arm carries only the organ its row label names",
                    'the sheet states its readout in the summary rows "mean '
                    'Lung CFU" and "mean Spleen CFU"',
                    "" if organ else "this row names no organ"])))
    return rows


# ---------------------------------------------------------------------------
# S. Fig. 7a,b -- log10 CFU; only the first band of the header row is a time
# ---------------------------------------------------------------------------
def _read_sfig7ab(path: Path, rel: str) -> list:
    sheet = "S. Fig. 7a,b"
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    bands = _spans(raw, 0)
    rows = []
    for i in range(1, len(raw)):
        organ = _s(raw.iat[i, 0])
        if not organ or not _has_number(raw, i):
            continue
        for lab, a, b in bands:
            hours = _label_hours(lab)
            timed = bool(np.isfinite(hours))
            drug, conc, unit = ("", np.nan, "") if timed else _drug_of(lab)
            k = 0
            for c in range(a, b):
                n = _num(raw.iat[i, c])
                if n is None:
                    continue
                k += 1
                note = [ORG_NOTE, INVIVO_NOTE, ABBREV_NOTE,
                        'the sheet states its readout in cell A1: "log10 CFU"; '
                        "cfu_per_ml is 10 ** the deposited value",
                        'the reading is from the sheet\'s "%s" row' % organ]
                if timed:
                    note += [PI_NOTE,
                             'this band is labelled "%s" and carries no '
                             "treatment label" % lab]
                else:
                    note.append(
                        "the sheet gives no timepoint for this band: only the "
                        'first band of its header row ("Week 2") is a time, the '
                        "rest are treatment labels, so time_h is left blank")
                rows.append(_base(
                    source_file=rel, sheet=sheet,
                    drug=drug, concentration=conc, conc_unit=unit,
                    arm="%s / %s" % (lab, organ), replicate=str(k),
                    time_h=hours, cfu_per_ml=float(10.0 ** n),
                    notes=_join(note)))
    return rows


# ---------------------------------------------------------------------------
# S. Fig. 7d-f -- in vitro, a processed grid over a raw-count grid of the same
# shape and the same column positions
# ---------------------------------------------------------------------------
def _read_sfig7df(path: Path, rel: str) -> list:
    sheet = "S. Fig. 7d-f"
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    split = next(i for i in range(len(raw))
                 if "raw data counts" in _s(raw.iat[i, 0]).lower())

    bands = []
    for i in range(split):
        if not _has_number(raw, i, 0) and len(_row_labels(raw, i)) >= 2:
            bands = _spans(raw, i)
            break

    def data_rows(lo, hi):
        out, group = [], ""
        for i in range(lo, hi):
            lab = _s(raw.iat[i, 0])
            if lab and not _has_number(raw, i, 0):
                group = lab
            if _has_number(raw, i):
                out.append((i, lab or group))
        return out

    raw_by_group = {g: i for i, g in data_rows(split, len(raw))}
    rows = []
    for i, group in data_rows(0, split):
        ri = raw_by_group.get(group)
        for lab, a, b in bands:
            hours = _label_hours(lab)
            drug, conc, unit = _drug_of(lab)
            k = 0
            for c in range(a, b):
                n = _num(raw.iat[i, c])
                if n is None:
                    continue
                k += 1
                colonies = dilution = np.nan
                note = [ORG_NOTE, ABBREV_NOTE, INVITRO_NOTE,
                        'the sheet writes this condition as "%s"' % lab]
                rv = _num(raw.iat[ri, c]) if ri is not None else None
                if rv is not None and abs(rv * 1e4 - n) < 0.5:
                    colonies, dilution = rv, 1000.0
                    note.append('dilution from this sheet\'s "dilution=-3"; '
                                + CONV_NOTE)
                elif rv is not None:
                    note.append(
                        "FINDING: the raw count in the same column (%g) does "
                        "not give the plotted %g under this sheet's conversion "
                        "(colonies x 1e4); colonies and dilution left blank"
                        % (rv, n))
                if np.isfinite(hours):
                    note.append('the sheet labels this band "%s"' % lab)
                else:
                    note.append(
                        "the sheet gives no day for this band -- only the first "
                        'band is a date ("Day 0") -- so time_h is left blank')
                rows.append(_base(
                    source_file=rel, sheet=sheet,
                    drug=drug, concentration=conc, conc_unit=unit,
                    arm="%s / %s" % (group, lab), replicate=str(k),
                    time_h=hours, colonies=colonies, dilution=dilution,
                    cfu_per_ml=n, notes=_join(note)))
    return rows


# ---------------------------------------------------------------------------
# S. Fig. 5a -- in vitro; the processed blocks carry no arm label, so the arm is
# recovered from the raw-count grid by arithmetic, or left blank
# ---------------------------------------------------------------------------
def _read_sfig5a(path: Path, rel: str) -> list:
    sheet = "S. Fig. 5a"
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    split = next(i for i in range(len(raw))
                 if _s(raw.iat[i, 0]).lower().startswith("raw data"))

    groups = _spans(raw, 0)                    # WT B6 / B6.Sst1S / WT B6 Old
    day_row = next(i for i in range(split + 1, len(raw))
                   if any(DAY_RE.match(t) for _, t in _row_labels(raw, i)))
    arm_row = next(i for i in range(day_row + 1, len(raw))
                   if len(_row_labels(raw, i)) >= 2)
    days = _spans(raw, day_row, first_col=0)
    arms = _spans(raw, arm_row, first_col=0)
    raw_rows = [i for i in range(arm_row + 1, len(raw))
                if _s(raw.iat[i, 0]) and _has_number(raw, i)]

    def raw_cell(gi, hours, arm_lab, k):
        """The raw count for the k-th replicate of one cell of the raw grid."""
        if gi >= len(raw_rows):
            return None
        ri = raw_rows[gi]
        for lab, a, b in arms:
            if lab != arm_lab:
                continue
            for dlab, da, db in days:
                if _label_hours(dlab) != hours or not (da <= a < db):
                    continue
                cols = [c for c in range(a, b) if _num(raw.iat[ri, c]) is not None]
                if k <= len(cols):
                    return _num(raw.iat[ri, cols[k - 1]])
        return None

    # processed rows: a bare 0 or 1 in column 0, in two runs of contiguous rows
    runs, cur, prev = [], [], None
    for i in range(split):
        if _num(raw.iat[i, 0]) is None or not _has_number(raw, i):
            continue
        if prev is not None and i != prev + 1:
            runs.append(cur)
            cur = []
        cur.append(i)
        prev = i
    if cur:
        runs.append(cur)

    def cells(i):
        """(group index, group label, replicate, hours, value) for one row."""
        hours = _num(raw.iat[i, 0]) * 24.0
        for gi, (g, a, b) in enumerate(groups):
            k = 0
            for c in range(a, b):
                n = _num(raw.iat[i, c])
                if n is None:
                    continue
                k += 1
                yield gi, g, k, hours, n

    rows = []
    for run in runs:
        # which arm is this unlabelled block? decided by arithmetic, not position
        votes = {}
        for lab, _, _ in arms:
            ok = tot = 0
            for i in run:
                for gi, _g, k, hours, n in cells(i):
                    rv = raw_cell(gi, hours, lab, k)
                    if rv is None:
                        continue
                    tot += 1
                    ok += abs(rv * 1e5 - n) < 0.5
            votes[lab] = (ok, tot)
        best = max(votes, key=lambda L: votes[L][0])
        matched = votes[best][1] > 0 and votes[best][0] == votes[best][1]
        arm_lab = best if matched else ""
        drug, conc, unit = _drug_of(arm_lab) if matched else ("", np.nan, "")

        for i in run:
            for gi, g, k, hours, n in cells(i):
                rv = raw_cell(gi, hours, best, k) if matched else None
                colonies = rv if rv is not None and abs(rv * 1e5 - n) < 0.5 \
                    else np.nan
                note = [ORG_NOTE, INVITRO_NOTE,
                        "the processed block carries no day unit; it is read as "
                        "days because this sheet's own raw-count grid labels the "
                        'same two columns "Day 0" and "Day 1"']
                if matched:
                    note.append(
                        'the processed block carries no arm label; "%s" is '
                        "taken from the sheet's raw-count grid, every one of "
                        "whose counts times 1e5 equals the plotted value in "
                        "this block" % best)
                else:
                    note.append(
                        "the processed block carries no arm label and its "
                        "values do not match either arm of the raw-count grid, "
                        "so arm is left blank")
                note.append(
                    "the conversion on this sheet is plotted value = colonies x "
                    "1e5; no dilution and no plated volume are stated anywhere "
                    "on it, so dilution stays blank and the factor is "
                    "unexplained")
                if drug:
                    note.append(
                        "TNF is a cytokine, not an antimicrobial; it is in the "
                        "drug column because it is this arm's stated exposure")
                rows.append(_base(
                    source_file=rel, sheet=sheet,
                    drug=drug, concentration=conc, conc_unit=unit,
                    arm="%s / %s" % (g, arm_lab) if arm_lab else g,
                    replicate=str(k), time_h=hours,
                    colonies=colonies, cfu_per_ml=n, notes=_join(note)))
    return rows


# ---------------------------------------------------------------------------
# Fig. 1g -- in vitro; processed columns on the left, raw counts on the right
# ---------------------------------------------------------------------------
def _read_fig1g(path: Path, rel: str) -> list:
    sheet = "Fig. 1g"
    raw = pd.read_excel(path, sheet_name=sheet, header=None)

    side = {t.lower(): c for c, t in _row_labels(raw, 0)}
    p0 = next(c for t, c in side.items() if t.startswith("processed"))
    r0 = next(c for t, c in side.items() if t.startswith("raw"))

    hdr = next(i for i in range(1, len(raw))
               if len(_spans(raw, i, p0, r0)) >= 2 and not _has_number(raw, i, 0))
    proc = _spans(raw, hdr, p0, r0)
    rawb = _spans(raw, hdr, r0)

    dil = np.nan
    for i in range(len(raw)):
        for _, t in _row_labels(raw, i):
            m = DIL_RE.match(t)
            if m and m.group(1).lower() != "neat":
                dil = 10.0 ** abs(int(m.group(1)))

    rows, exp_note, setno, prev = [], "", 0, None
    for i in range(len(raw)):
        lab0 = _s(raw.iat[i, 0])
        if lab0.lower().startswith("independ"):
            exp_note, setno, prev = lab0, 0, None
            continue
        n0 = _num(raw.iat[i, 0])
        if n0 is None or not _has_number(raw, i):
            continue
        if prev is None or i != prev + 1:
            setno += 1
        prev = i
        hours = 0.0 if n0 == 0 else float("nan")
        for (glab, ga, gb), (_, ra, rb) in zip(proc, rawb):
            k = 0
            for off in range(gb - ga):
                n = _num(raw.iat[i, ga + off])
                if n is None:
                    continue
                k += 1
                colonies = dilution = np.nan
                note = [ORG_NOTE, INVITRO_NOTE,
                        'the sheet\'s own block heading is "%s"' % exp_note,
                        "this sheet stacks two unlabelled sets of rows under "
                        "each experiment heading and says nothing about what "
                        "distinguishes them; they are numbered in the replicate "
                        "column"]
                rv = _num(raw.iat[i, ra + off]) if ra + off < rb else None
                if rv is not None and abs(rv * 1e4 - n) < 0.5:
                    colonies, dilution = rv, dil
                    note.append('dilution from this sheet\'s "Dilution=-3"; '
                                + CONV_NOTE)
                else:
                    note.append(
                        "FINDING: the count in the matching column of this "
                        "sheet's raw-count block (%s) does not give the plotted "
                        "%g under the conversion the rest of the sheet obeys "
                        "(colonies x 1e4); colonies and dilution are left blank"
                        % ("none" if rv is None else "%g" % rv, n))
                if np.isfinite(hours):
                    note.append("the row is labelled 0, so it is the reading at "
                                "time zero whatever the sheet's unstated unit")
                else:
                    note.append(
                        "the row label is the bare number %g and no time unit "
                        "appears anywhere on this sheet, so time_h is left "
                        "blank rather than guessed at hours or days" % n0)
                rows.append(_base(
                    source_file=rel, sheet=sheet, arm=glab,
                    replicate="set %d rep %d" % (setno, k),
                    time_h=hours, colonies=colonies, dilution=dilution,
                    cfu_per_ml=n, notes=_join(note)))
    return rows


def read(d: Path) -> pd.DataFrame:
    fig = next(iter(sorted(d.rglob(FIG))), None)
    sup = next(iter(sorted(d.rglob(SUP))), None)
    if fig is None and sup is None:
        return empty()

    rows = []
    if fig is not None:
        rel = fig.relative_to(d).as_posix()
        rows += _read_fig5fg(fig, rel, "Fig. 5f")
        rows += _read_fig5fg(fig, rel, "Fig. 5g")
        rows += _read_fig5b(fig, rel)
        rows += _read_fig1g(fig, rel)
    if sup is not None:
        rel = sup.relative_to(d).as_posix()
        rows += _read_sfig7ab(sup, rel)
        rows += _read_sfig7df(sup, rel)
        rows += _read_sfig5a(sup, rel)

    if not rows:
        return empty()
    return finish(pd.DataFrame(rows), "SHEE2026_SENOLYTIC")
