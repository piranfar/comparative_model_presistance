"""Zenodo 7147832 -- "Manuscript persistence in S. pneumoniae_raw data.xlsx",
ten sheets of growth curves, time-kill curves and single-timepoint survival
assays for Streptococcus pneumoniae.

The same workbook was downloaded twice into this corpus, as GEERTS2022 and as
MICHIELS2022 (identical sha256, identical Zenodo record). This module holds the
parsing; read_MICHIELS2022.py returns nothing so the readings are not counted
twice.

WHAT THE WORKBOOK SAYS.

  * Counts are already CFU/mL -- every count column is headed
    "Concentration (CFU/mL)" -- so they go straight into cfu_per_ml. There are
    no raw colonies, no dilution and no plated volume anywhere in the file.

  * NO DETECTION FLOOR IS STATED. Searching every cell of all ten sheets for
    "detect", "LOD", "LOQ", "limit", "plated", "volume" or "inoculum" returns
    nothing at all. So floor_cfu_per_ml is blank on every row and every
    reading's censoring is unknown. That absence is the point, and this reader
    will not paper over it -- note in particular that a hundred-odd readings
    across the workbook are exactly 1 CFU/mL, which cannot be a real per-mL
    count off a plate and is far more likely a placeholder for "nothing grew";
    without a stated floor there is no way to tell, so those rows keep the
    value 1 and carry a note saying exactly that.

  * Antibiotic concentrations are headed "(?g/mL)" -- the micro sign is stored
    as U+FFFD inside the depositor's own file, encoding damage that is in the
    deposit and not introduced here. Read as ug/mL, which the workbook
    corroborates internally: its MIC sheet gives D39 amoxicillin MIC 0.0071,
    and the kill-curve sheets label 0.7 as "100X MIC".

  * The organism is named only by the file name ("persistence in S.
    pneumoniae") and the Zenodo record title, never in a cell. It is recorded
    as the source writes it, "S. pneumoniae", with that provenance in notes.

SHEET BY SHEET.

  Growth curves media          SKIPPED -- all 381 of its rows appear verbatim
                               in "Growth curves - cat - chol" as the Control
                               strategy. Checked row by row at run time, and
                               if the two ever stop matching this reader falls
                               back to reading both.
  Growth curves - cat - chol   924 rows, 867 read. Growth only, no
                               antibiotic. Strategy is a mix of media
                               additives, knockouts and anaerobic incubation,
                               so it goes in `arm`, not in `strain` -- the
                               workbook never names the parent strain on this
                               sheet.
  Validation of long-living    372 rows, 364 read. Growth, strain named per
    model                      row (TIGR4, R6, ATCC49619 and the numbered
                               isolates 85 and 88). Clock is "Time of growth
                               (h)", not treatment.
  Dose-dependent kill curve    120 rows, 119 read, all at one timepoint: the
    - D39                      column is headed "Concentration after 5 hours
                               (CFU/mL)", so time_h = 5. The sheet name gives
                               the strain.
  Time-kill curves D39         480 rows, 472 read, "Time of treatment (h)".
  Heritability assay -         585 rows, of which 248 are read. Every one of
    kill curve                 the 320 readings labelled "Original culture" is
                               a verbatim re-listing of "Time-kill curves
                               D39": curve by curve, each matches a time-kill
                               row on time, growth phase, antibiotic and CFU
                               value, and the time-kill sheet is the superset
                               (it also has the untreated controls and three
                               more exponential repeats). Those are dropped as
                               duplicates and the Clone 1 readings kept. The
                               test runs at run time on whole curves -- a
                               curve goes only if it has at least three
                               readings and every one of them is still
                               unclaimed in the time-kill sheet -- so nothing
                               is discarded on the strength of a coincidence
                               in one or two values.
  Heritability assay -         156 rows, 139 with a value, of which 83 are
    survival                   read. One reading per (strain, growth phase,
                               antibiotic, repeat) at 6 h diluted-stationary
                               or 18 h exponential, strain = Original culture
                               / Clone 1-5. It is NOT curve-shaped, so the
                               per-curve test used on the kill-curve sheet can
                               never fire here; the block tested is (strain,
                               growth phase). All 36 "Original culture"
                               readings are the corresponding time-kill
                               readings verbatim, and all 20 "Clone 1"
                               readings are the corresponding heritability
                               kill-curve readings verbatim -- 56 in total,
                               dropped. Clones 2-5 appear on no other sheet
                               and are kept in full; their blocks match the
                               pool at best 5 of 12, which is what
                               coincidence on small counts (10, 20, 30, 33)
                               looks like, and is why the test demands that
                               EVERY reading in a block match before any of
                               it is dropped.
  Screening clinical isolates  wide: "pre treatment (CFU/mL)" and "post 8h
                               treatment (CFU/mL)". Unpivoted to t=0 and t=8.
                               See the shared-inoculum note below.
  MIC                          MICs only, no time course. Nothing returned.
  qPCR                         fold-change in expression. Nothing returned.

THE SHARED INOCULUM ON THE SCREENING SHEET. For the ten clinical isolates the
same pre-treatment count is repeated on the negative-control, amoxicillin and
vancomycin rows of a given repeat -- one reading written three times. For D39
and TIGR4 the three pre-treatment counts differ, so those are three readings.
This reader emits each distinct pre-treatment value once per (isolate, growth
phase, repeat): where the value belongs to a single arm it becomes that arm's
t=0, and where it is shared the arm label says so and lists the arms sharing
it. Nothing is counted twice and nothing is dropped.

MISSING VALUES. The workbook writes "/" where it has no value; those readings
are dropped. "/" is also how it writes "no antibiotic" in the AB and X MIC
columns, which is read as a control rather than as a missing value.

REPLICATE KEYS. The workbook restarts its Repeat numbering in every sheet and,
on several sheets, in every strain, so a bare "R1" is not a curve. `replicate`
is therefore written as <sheet code>-<strain>-R<n>, which makes (arm,
replicate) a unique series within this study -- without it the D39 time-kill
curves and the Clone 1 heritability curves collide on identical labels.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import empty

XLSX = "Manuscript_persistence_in_S._pneumoniae_raw_data.xlsx"

ORGANISM = "S. pneumoniae"
ORG_NOTE = ("organism from the deposited file name and Zenodo record title; "
            "no cell in the workbook names it")
NO_FLOOR = ("the workbook states no detection limit, no plated volume and no "
            "dilution anywhere in its ten sheets")
UG = "ug/mL"
UNIT_NOTE = ("concentration unit written '?g/mL' in the deposit -- the micro "
             "sign is stored as U+FFFD in the depositor's file; read as ug/mL, "
             "which the workbook's own MIC sheet corroborates")
ONE_NOTE = ("value is exactly 1 CFU/mL; with no stated floor there is no way "
            "to tell a real count from a placeholder for zero")


def _txt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    return str(v).strip()


def _num(v) -> float:
    s = _txt(v)
    if s in ("", "/", "nan"):
        return np.nan
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return np.nan


def _load(path: Path, sheet: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet, header=0)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _col(df: pd.DataFrame, *needles: str) -> str:
    """The one column whose name contains all of the needles.

    An exact match wins outright, so asking for "AB" does not also catch
    "Concentration of AB (?g/mL)".
    """
    exact = [c for c in df.columns
             if len(needles) == 1 and c.lower() == needles[0].lower()]
    if len(exact) == 1:
        return exact[0]
    hits = [c for c in df.columns
            if all(n.lower() in c.lower() for n in needles)]
    if len(hits) != 1:
        raise KeyError(f"{needles} matched {hits} in {list(df.columns)}")
    return hits[0]


def _row(**kw) -> dict:
    base = {
        "source_file": XLSX, "sheet": "", "organism": ORGANISM, "strain": "",
        "drug": "", "concentration": np.nan, "conc_unit": "", "arm": "",
        "replicate": "", "tech_replicate": "", "time_h": np.nan,
        "cfu_per_ml": np.nan, "floor_cfu_per_ml": np.nan,
        "floor_basis": NO_FLOOR, "readout": "CFU", "notes": "",
    }
    base.update(kw)
    return base


def _note(*bits: str) -> str:
    return "; ".join(b for b in bits if b)


def _one(cfu: float) -> str:
    return ONE_NOTE if cfu == 1 else ""


def _rep(code: str, repeat, strain: str = "") -> str:
    """A replicate key unique within the study: the workbook restarts Repeat
    in every sheet and, on some sheets, in every strain."""
    bits = [code] + ([strain] if strain else []) + [f"R{_txt(repeat)}"]
    return "-".join(bits)


# A curve has to be at least this many readings before it can be dismissed as
# a re-listing of another sheet. Below it, a "match" is just two numbers that
# happen to agree, which is not evidence of anything.
MIN_CURVE_FOR_DUP = 3

# The survival sheet has no curves at all: it lists ONE reading per (strain,
# growth phase, antibiotic, repeat), so a per-curve test can never fire there
# and its re-listings would be counted a second time. The comparable block on
# that sheet is (strain, growth phase) -- 8 to 24 readings across the four
# antibiotics and every repeat -- and it has to be at least this large before
# an all-match is treated as evidence.
MIN_BLOCK_FOR_DUP = 6


def _curve_keys(df: pd.DataFrame, t: str, cfu: str, phase: str,
                ab: str) -> list[tuple]:
    """Readings as comparable keys. Rows with no value are left out entirely
    -- a NaN cannot be matched against another NaN, and those rows are not
    emitted either, so nothing is lost by ignoring them here."""
    keys = zip(df[t].map(_num), df[phase].map(_txt), df[ab].map(_txt),
               df[cfu].map(_num))
    return [k for k in keys if not (isinstance(k[3], float) and np.isnan(k[3]))]


def _growth_sheets(path: Path) -> list[tuple[str, pd.DataFrame, bool]]:
    """(sheet, frame, media_was_absorbed) -- de-duplicating the two growth
    sheets only if the smaller really is contained in the larger."""
    media = _load(path, "Growth curves media")
    cc = _load(path, "Growth curves - cat - chol")
    strat = _col(cc, "Strategy")
    cc[strat] = cc[strat].map(_txt)
    ctrl = cc[cc[strat] == "Control"].drop(columns=[strat]).reset_index(drop=True)
    subset = (len(media) == len(ctrl)
              and set(media.astype(str).apply(tuple, axis=1))
              <= set(ctrl.astype(str).apply(tuple, axis=1)))
    out = [("Growth curves - cat - chol", cc, subset)]
    if not subset:
        media["Strategy"] = "Control"
        out.append(("Growth curves media", media, False))
    return out


def read(d: Path) -> pd.DataFrame:
    path = d / XLSX
    if not path.exists():
        return empty()

    rows: list[dict] = []

    # ---- Growth curves --------------------------------------------------
    for sheet, df, absorbed in _growth_sheets(path):
        t, cfu = _col(df, "Time point"), _col(df, "CFU/mL")
        med, strat = _col(df, "Medium"), _col(df, "Strategy")
        dedup = ("'Growth curves media' skipped: its 381 rows are this sheet's "
                 "Control rows verbatim") if absorbed else ""
        for _, r in df.iterrows():
            v = _num(r[cfu])
            if np.isnan(v):
                continue
            strategy, medium = _txt(r[strat]), _txt(r[med])
            rows.append(_row(
                sheet=sheet,
                arm=f"{strategy} in {medium}",
                replicate=_rep("GC", r["Repeat"]),
                time_h=_num(r[t]), cfu_per_ml=v,
                notes=_note(
                    ORG_NOTE, "growth curve, no antibiotic",
                    f"medium {medium}; the Strategy column reads '{strategy}' "
                    "-- the workbook mixes media additives, knockouts and "
                    "incubation conditions in that one column and never names "
                    "the parent strain on this sheet",
                    "source header: Time point (hours)", dedup, _one(v)),
            ))

    # ---- Validation of long-living model --------------------------------
    sheet = "Validation of long-living model"
    df = _load(path, sheet)
    t, cfu = _col(df, "Time of growth"), _col(df, "CFU/mL")
    st = _col(df, "Strain")
    for _, r in df.iterrows():
        v = _num(r[cfu])
        if np.isnan(v):
            continue
        rows.append(_row(
            sheet=sheet, strain=_txt(r[st]),
            arm="long-living model, no antibiotic",
            replicate=_rep("VAL", r["Repeat"], _txt(r[st])),
            time_h=_num(r[t]), cfu_per_ml=v,
            notes=_note(ORG_NOTE,
                        "source header: Time of growth (h) -- the clock is "
                        "time in culture, not time of treatment", _one(v)),
        ))

    # ---- Dose-dependent kill curve - D39 --------------------------------
    sheet = "Dose-dependent kill curve - D39"
    df = _load(path, sheet)
    cfu = _col(df, "Concentration after 5 hours")
    ab, xmic = _col(df, "AB"), _col(df, "X MIC")
    conc, phase_c = _col(df, "Concentration of AB"), _col(df, "Growth phase")
    for _, r in df.iterrows():
        v = _num(r[cfu])
        if np.isnan(v):
            continue
        drug, phase, xm = _txt(r[ab]), _txt(r[phase_c]), _txt(r[xmic])
        is_ctrl = drug.lower() == "control"
        rows.append(_row(
            sheet=sheet, strain="D39",
            drug="" if is_ctrl else drug,
            concentration=np.nan if is_ctrl else _num(r[conc]),
            conc_unit="" if is_ctrl else UG,
            arm=(f"{phase}, control" if is_ctrl
                 else f"{phase}, {drug} {xm}x MIC"),
            replicate=_rep("DD", r["Repeat"], "D39"),
            time_h=5.0, cfu_per_ml=v,
            notes=_note(ORG_NOTE, "strain D39 from the sheet name",
                        "single timepoint; source header 'Concentration after "
                        "5 hours (CFU/mL)', taken as 5 h",
                        "" if is_ctrl else f"stated as {xm}x MIC",
                        "" if is_ctrl else UNIT_NOTE, _one(v)),
        ))

    # ---- Time-kill curves D39 -------------------------------------------
    sheet = "Time-kill curves D39"
    df = _load(path, sheet)
    t, cfu = _col(df, "Time of treatment"), _col(df, "CFU/mL")
    conc, phase_c = _col(df, "100X MIC"), _col(df, "Growth phase")
    # Pool of readings this sheet holds, for the heritability duplicate test.
    pool = Counter(_curve_keys(df, t, cfu, phase_c, "AB"))
    for _, r in df.iterrows():
        v = _num(r[cfu])
        if np.isnan(v):
            continue
        drug, phase = _txt(r["AB"]), _txt(r[phase_c])
        is_ctrl = drug in ("", "/")
        rows.append(_row(
            sheet=sheet, strain="D39",
            drug="" if is_ctrl else drug,
            concentration=np.nan if is_ctrl else _num(r[conc]),
            conc_unit="" if is_ctrl else UG,
            arm=f"{phase}, control" if is_ctrl else f"{phase}, {drug} 100x MIC",
            replicate=_rep("TK", r["Repeat"], "D39"),
            time_h=_num(r[t]), cfu_per_ml=v,
            notes=_note(ORG_NOTE, "strain D39 from the sheet name",
                        "source header: Time of treatment (h)",
                        "" if is_ctrl else
                        "column headed 'Concentration of 100X MIC'",
                        "" if is_ctrl else UNIT_NOTE, _one(v)),
        ))

    # ---- Heritability assay, both sheets --------------------------------
    # Both sheets re-list readings that another sheet already holds, and each
    # needs its own test because they are shaped differently.
    #
    #   kill curve  is curve-shaped: (strain, phase, AB, Repeat) is 4-7
    #               readings over time. A curve is dropped only if EVERY one
    #               of its readings is still unclaimed in `tk_pool`, the
    #               readings of "Time-kill curves D39"; the pool is consumed
    #               as it matches, so two distinct curves cannot both be
    #               explained by one.
    #
    #   survival    is NOT curve-shaped: it lists a single reading per
    #               (strain, phase, AB, Repeat), so a per-curve test can never
    #               fire on it and its re-listings would go straight into the
    #               corpus a second time. Its comparable block is (strain,
    #               growth phase) -- 8 to 24 readings -- and it is tested
    #               against everything ACTUALLY EMITTED from the two kill-curve
    #               sheets, because a survival reading is a third listing of a
    #               time-kill reading, not a second.
    #
    # The all-match requirement, not the size guard, is what separates the two
    # cases: the four blocks that are re-listings match 8/8, 12/12, 24/24 and
    # 12/12, while the strongest of the eight blocks that are NOT re-listings
    # manages 5 of 12. Those blocks are the clones that appear on no other
    # sheet, and they are kept in full.
    tk_all = Counter(pool)          # pristine copy, before the HKC test eats it

    # -- kill curve --------------------------------------------------------
    sheet = "Heritability assay - kill curve"
    df = _load(path, sheet)
    t, cfu = _col(df, "Time of treatment"), _col(df, "CFU/mL")
    st, conc = _col(df, "Strain"), _col(df, "100X MIC")
    phase_c = _col(df, "Growth phase")
    df = df.copy()
    df[st] = df[st].map(_txt)

    drop_curves = set()
    for key, grp in df.groupby([st, phase_c, "AB", "Repeat"], sort=True):
        need = Counter(_curve_keys(grp, t, cfu, phase_c, "AB"))
        if sum(need.values()) >= MIN_CURVE_FOR_DUP and \
                all(pool[k] >= n for k, n in need.items()):
            pool -= need
            drop_curves.add(key)

    hkc_kept: Counter = Counter()
    for key, grp in df.groupby([st, phase_c, "AB", "Repeat"], sort=True):
        if key in drop_curves:
            continue
        for _, r in grp.iterrows():
            v = _num(r[cfu])
            if np.isnan(v):
                continue
            drug, phase = _txt(r["AB"]), _txt(r[phase_c])
            hkc_kept[(_num(r[t]), phase, drug, v)] += 1
            rows.append(_row(
                sheet=sheet, strain=_txt(r[st]), drug=drug,
                concentration=_num(r[conc]), conc_unit=UG,
                arm=f"{phase}, {drug} 100x MIC",
                replicate=_rep("HKC", r["Repeat"], _txt(r[st])),
                time_h=_num(r[t]), cfu_per_ml=v,
                notes=_note(ORG_NOTE,
                            "Strain column reads 'Original culture' or "
                            "'Clone n'; the workbook does not say which "
                            "background the clones came from",
                            "source header: Time of treatment (h)",
                            (f"{len(drop_curves)} curve(s) on this sheet "
                             "dropped as a verbatim re-listing of "
                             "'Time-kill curves D39'")
                            if drop_curves else "",
                            UNIT_NOTE, _one(v)),
            ))

    # -- survival ----------------------------------------------------------
    sheet = "Heritability assay - survival"
    df = _load(path, sheet)
    t, cfu = _col(df, "Time of treatment"), _col(df, "CFU/mL")
    st, conc = _col(df, "Strain"), _col(df, "100X MIC")
    phase_c = _col(df, "Growth phase")
    df = df.copy()
    df[st] = df[st].map(_txt)

    surv_pool = tk_all + hkc_kept
    drop_blocks, dropped_from = set(), set()
    for key, grp in df.groupby([st, phase_c], sort=True):
        need = Counter(_curve_keys(grp, t, cfu, phase_c, "AB"))
        if sum(need.values()) >= MIN_BLOCK_FOR_DUP and \
                all(surv_pool[k] >= n for k, n in need.items()):
            surv_pool -= need
            drop_blocks.add(key)
            dropped_from.add(key[0])

    drop_note = ("this sheet's " + " and ".join(sorted(dropped_from))
                 + " readings are dropped: every one of them is a verbatim "
                 "re-listing of a reading already emitted from 'Time-kill "
                 "curves D39' or 'Heritability assay - kill curve', which "
                 "carry the whole curve rather than this sheet's single "
                 "timepoint") if drop_blocks else ""

    for key, grp in df.groupby([st, phase_c], sort=True):
        if key in drop_blocks:
            continue
        for _, r in grp.iterrows():
            v = _num(r[cfu])
            if np.isnan(v):
                continue
            drug, phase = _txt(r["AB"]), _txt(r[phase_c])
            rows.append(_row(
                sheet=sheet, strain=_txt(r[st]), drug=drug,
                concentration=_num(r[conc]), conc_unit=UG,
                arm=f"{phase}, {drug} 100x MIC",
                replicate=_rep("HSV", r["Repeat"], _txt(r[st])),
                time_h=_num(r[t]), cfu_per_ml=v,
                notes=_note(ORG_NOTE,
                            "Strain column reads 'Original culture' or "
                            "'Clone n'; the workbook does not say which "
                            "background the clones came from",
                            "source header: Time of treatment (h)",
                            "single timepoint, not a curve: this sheet gives "
                            "one reading per strain, phase, antibiotic and "
                            "repeat",
                            drop_note, UNIT_NOTE, _one(v)),
            ))

    # ---- Screening clinical isolates ------------------------------------
    sheet = "Screening clinical isolates"
    df = _load(path, sheet)
    pre, post = _col(df, "pre treatment"), _col(df, "post 8h")
    stam, conc = _col(df, "Stam"), _col(df, "100X MIC")
    sero, phase_c = _col(df, "Serotype"), _col(df, "Growth phase")
    for c in (stam, phase_c, "AB", sero):
        df[c] = df[c].map(_txt)

    def arm_of(drug: str, phase: str) -> tuple[str, str]:
        if drug.lower() in ("negative control", "control", "", "/"):
            return "", f"{phase}, negative control"
        return drug, f"{phase}, {drug} 100x MIC"

    for (isolate, phase, rep), grp in df.groupby(
            [stam, phase_c, "Repeat"], sort=False):
        serotype = grp[sero].iloc[0]
        sero_note = (f"serotype {serotype}" if serotype not in ("", "/")
                     else "serotype not given")
        for _, r in grp.iterrows():
            v = _num(r[post])
            if np.isnan(v):
                continue
            drug, arm = arm_of(r["AB"], phase)
            rows.append(_row(
                sheet=sheet, strain=isolate, drug=drug,
                concentration=np.nan if not drug else _num(r[conc]),
                conc_unit="" if not drug else UG,
                arm=arm, replicate=_rep("SCR", rep, isolate),
                time_h=8.0, cfu_per_ml=v,
                notes=_note(ORG_NOTE, sero_note,
                            "source header: post 8h treatment (CFU/mL)",
                            "" if not drug else UNIT_NOTE, _one(v)),
            ))
        # One row per DISTINCT pre-treatment value in the group: for the
        # clinical isolates a single inoculum count is written on all three
        # antibiotic rows, while for D39 and TIGR4 the three differ.
        for val, sub in grp.groupby(grp[pre].map(_num), dropna=True):
            arms = sorted({arm_of(a, phase)[1] for a in sub["AB"].tolist()})
            shared = len(arms) > 1
            rows.append(_row(
                sheet=sheet, strain=isolate,
                arm=(f"{phase}, pre-treatment inoculum shared by "
                     f"{len(arms)} arms") if shared else arms[0],
                replicate=_rep("SCR", rep, isolate), time_h=0.0,
                cfu_per_ml=float(val),
                notes=_note(ORG_NOTE, sero_note,
                            "source header: pre treatment (CFU/mL)",
                            ("one inoculum count written on several antibiotic "
                             "rows of this repeat; emitted once here, not once "
                             "per arm; the arms sharing it are "
                             + " / ".join(arms)) if shared else
                            "each arm of this repeat carries its own "
                            "pre-treatment count",
                            _one(float(val))),
            ))

    return pd.DataFrame(rows)
