"""YANG2024_PHAGE -- figshare file 44617477, the source data behind one figure
panel of a mycobacteriophage study.

WHAT THE DEPOSIT IS. The file is named 44617477.csv but it is not a CSV: it is a
GraphPad Prism project (PrismXMLVersion 5.00, written by Prism 8.3.0.538), whose
first 2.7 kB are the readable data table and whose remaining 16 kB are the
graphs and layouts as one zlib-compressed base64 blob. There is exactly one
table, Prism ID Table0, titled "Data 1", TableType XY, YFormat "replicates" with
Replicates=3:

    row titles   Day 0, Day 3, Day 6, Day 9   (the XColumn itself is empty)
    Y columns    Ctrl, D29, Chah, DS6A        (3 replicate subcolumns each)

4 timepoints x 4 arms x 3 replicates = 48 readings, and all 48 are present.

WHAT THE DEPOSIT SAYS, and is therefore recorded.

  * The unit and the system, but only inside the compressed graph block. The
    graph title there is "CFU of liquid culture" and the Y-axis title is
    "CFU/ml culture". This reader inflates that block and reads both strings out
    rather than assuming them; the exact strings recovered are quoted in notes
    on every row. The data table on its own carries no unit at all.

  * The arm labels, verbatim: Ctrl, D29, Chah, DS6A. "Ctrl" is the deposit's own
    control label, so its rows carry no drug. The other three go into `drug` as
    the file writes them.

  * Day 0 is the start of exposure and is time_h = 0. Days are converted at 24 h
    from the row titles.

WHAT THE DEPOSIT DOES NOT SAY, and is therefore left blank.

  * NO ORGANISM AND NO STRAIN. Nothing in the XML or in the strings of the
    compressed block names a species, a strain, a medium or a temperature. The
    study_id and the repository's manifest identify this as M. tuberculosis and
    identify D29, Chah and DS6A as mycobacteriophages, but the deposited file
    does not, so organism and strain stay blank and `drug` carries the bare
    column titles.

  * NO CONCENTRATION AND NO MOI. There is no dose anywhere in the file.

  * NO FLOOR, and this is the point worth being careful about. The file states
    no limit of detection, no plated volume, no dilution and no colony count --
    only densities. This reader searches for all of those, in both the XML text
    and the inflated graph strings, and records in floor_basis what it searched
    for and did not find. The repository's own sweep note derives 100 CFU/mL for
    this study from a 10 uL spot volume stated in the ARTICLE's Methods; that
    text is not in this deposit, this reader has not read it, and the number is
    deliberately not recorded here.

TWO THINGS A LATER READER NEEDS TO KNOW, both checked in code rather than
asserted from memory.

  * The Day 0 row is one measurement copied across the arm columns. All four
    arms carry the identical triple 101250 / 168750 / 168750, so the twelve
    t=0 rows are three readings repeated four times, not twelve independent
    ones. Any hierarchical model that treats them as twelve will understate the
    variance at baseline. The reader compares the arms at every timepoint and
    flags any timepoint where they coincide exactly.

  * DS6A at Day 9 has two replicates written as a literal 0 while the third
    reads 285000. A 0 is not a count; with no stated floor it is impossible to
    tell from this deposit whether it means no colonies were seen at the lowest
    dilution plated or something else, so it is kept as 0, left uncensored, and
    flagged in notes.
"""
from __future__ import annotations

import base64
import re
import zlib
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
import pandas as pd

from src.ingest import empty, finish

NS = "{http://graphpad.com/prism/Prism.htm}"

# Row titles are "Day 0" ... "Day 9". Accept the other units Prism users write,
# so a differently-labelled table is converted rather than silently dropped.
TIME_UNIT_H = {
    "min": 1.0 / 60, "mins": 1.0 / 60, "minute": 1.0 / 60, "minutes": 1.0 / 60,
    "h": 1.0, "hr": 1.0, "hrs": 1.0, "hour": 1.0, "hours": 1.0,
    "d": 24.0, "day": 24.0, "days": 24.0,
    "wk": 168.0, "week": 168.0, "weeks": 168.0,
}
TIME_RE = re.compile(r"^\s*(?P<u1>[A-Za-z.]+)?\s*(?P<v>-?\d+(?:\.\d+)?)\s*"
                     r"(?P<u2>[A-Za-z.]+)?\s*$")

# What a stated floor would look like if this deposit ever grew one.
FLOOR_RE = re.compile(
    r"(?:limit of detection|detection limit|\bL\.?O\.?D\.?\b|\bLLOQ\b)"
    r"[^0-9]{0,24}?(\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*(?:CFU|cfu)\s*/\s*m[lL]")
# A plated volume, which with a dilution would fix a floor by arithmetic.
VOLUME_RE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:u|µ|μ)[lL]\b")
DILUTION_RE = re.compile(r"\bdilut", re.I)

UNIT_RE = re.compile(r"CFU\s*/\s*m[lL]", re.I)

CONTROL_RE = re.compile(r"^(ctrl|control|untreated|no phage|none)\b", re.I)

FLOOR_SEARCHED = (
    'searched the table XML and the inflated graph strings for "limit of '
    'detection", "detection limit", "LOD", "LLOQ", a microlitre volume and the '
    'word "dilution"')


def _text_of(el) -> str:
    return "" if el is None or el.text is None else el.text.strip()


def _graph_strings(raw: str) -> list[str]:
    """The readable strings inside the file's compressed graph block.

    Prism stores graphs, axis titles and layouts as zlib-compressed base64 in
    <Template>. The axis titles are the only place this deposit names its unit,
    so the block is inflated and its printable runs returned. A block that will
    not inflate yields nothing rather than raising -- the data table is still
    readable without it, and the caller says in notes that it found no titles.
    """
    m = re.search(r"<Template[^>]*>(.*?)</Template>", raw, re.S)
    if not m:
        return []
    try:
        blob = zlib.decompress(base64.b64decode(re.sub(r"\s", "", m.group(1))))
    except (ValueError, zlib.error):
        return []
    out = []
    for run in re.findall(rb"[\x20-\x7e]{4,}", blob):
        s = run.decode("ascii").strip().rstrip("-").strip()
        if s:
            out.append(s)
    return out


def _time_h(label: str) -> float | None:
    """Hours from a Prism row title such as 'Day 3'. None if it is not a time."""
    m = TIME_RE.match(label)
    if not m:
        return None
    unit = (m.group("u1") or m.group("u2") or "").strip(". ").lower()
    if unit not in TIME_UNIT_H:
        return None
    return float(m.group("v")) * TIME_UNIT_H[unit]


def _values(sub) -> list[float | None]:
    """One subcolumn's <d> cells; None for an empty or non-numeric cell."""
    out = []
    for d in sub.findall(f"{NS}d"):
        txt = _text_of(d)
        if not txt:
            out.append(None)
            continue
        try:
            out.append(float(txt))
        except ValueError:
            out.append(None)
    return out


def _prism_files(d: Path) -> list[Path]:
    files = []
    for p in sorted(d.iterdir()):
        if not p.is_file() or p.name == "PROVENANCE.json":
            continue
        head = p.read_text(encoding="utf-8", errors="replace")[:4000]
        if "GraphPadPrismFile" in head:
            files.append(p)
    return files


def _read_one(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    root = ET.fromstring(raw)
    graph = _graph_strings(raw)

    # --- the unit, taken from the file's own graph titles or not at all -------
    axis = [s for s in graph if UNIT_RE.search(s)]
    system = [s for s in graph if re.search(r"culture|broth|lung|spleen|"
                                            r"macrophage", s, re.I)]
    if axis:
        unit_note = ("the data table carries no unit; the unit is taken from "
                     "the file's own compressed graph block, where a title "
                     'reads "%s"' % axis[0])
    else:
        unit_note = ("neither the data table nor the file's graph block names "
                     "a unit for these values; they are recorded as CFU/mL on "
                     "the reading that the table is a viable-count time course")
    if system:
        unit_note += ('; the same block titles the graph "%s"' % system[0])

    # --- the floor, or the explicit absence of one ---------------------------
    hay = raw[:raw.find("<Template")] + " " + " ".join(graph)
    fm = FLOOR_RE.search(hay)
    vm = VOLUME_RE.search(hay)
    if fm:
        floor = float(fm.group(1))
        basis = 'stated in the deposit: "%s"' % fm.group(0)
    else:
        floor = np.nan
        basis = ("not stated: this deposit is a single GraphPad Prism file "
                 "that reports densities only -- no colony count, no dilution, "
                 "no plated volume and no limit of detection anywhere in it. "
                 + FLOOR_SEARCHED + ". ")
        if vm:
            basis += ('a volume-like string "%s" is present, but no dilution '
                      "accompanies it, so no floor follows by arithmetic and "
                      "none is recorded. " % vm.group(0))
        basis += ("The repository's sweep note derives 100 CFU/mL for this "
                  "study from a 10 uL spot volume stated in the ARTICLE's "
                  "Methods; that text is outside this deposit, this reader has "
                  "not read it, and the number is deliberately not recorded "
                  "here")

    no_meta = ("the deposit names no organism, strain, medium, agent class, "
               "concentration or MOI anywhere in the file, so all of those are "
               "left blank; the arm labels are the Prism column titles verbatim")

    rows = []
    for table in root.findall(f"{NS}Table"):
        sheet = _text_of(table.find(f"{NS}Title")) or table.get("ID", "")
        reps_declared = table.get("Replicates", "")

        rt = table.find(f"{NS}RowTitlesColumn")
        labels = []
        if rt is not None:
            sub = rt.find(f"{NS}Subcolumn")
            if sub is not None:
                labels = [_text_of(d) for d in sub.findall(f"{NS}d")]
        times = [_time_h(x) for x in labels]
        if not any(t is not None for t in times):
            raise ValueError("%s / %s: no time can be read from the row titles "
                             "%r" % (path.name, sheet, labels[:6]))

        cols = table.findall(f"{NS}YColumn")
        if not cols:
            raise ValueError("%s / %s: no Y columns" % (path.name, sheet))

        # Every arm's readings at each timepoint, to test below whether the
        # arms are carrying one shared measurement rather than four.
        by_time: dict[int, list[tuple[str, tuple]]] = {}
        block = []
        for col in cols:
            arm = _text_of(col.find(f"{NS}Title"))
            subs = [_values(s) for s in col.findall(f"{NS}Subcolumn")]
            for i, (label, t) in enumerate(zip(labels, times)):
                if t is None:
                    continue
                vals = tuple(s[i] if i < len(s) else None for s in subs)
                by_time.setdefault(i, []).append((arm, vals))
                for rep, v in enumerate(vals, start=1):
                    if v is None:
                        continue
                    block.append({"i": i, "arm": arm, "rep": rep,
                                  "label": label, "t": t, "v": v})

        shared = set()
        for i, entries in by_time.items():
            seen = {vals for _, vals in entries}
            if len(entries) > 1 and len(seen) == 1 and any(
                    x is not None for x in entries[0][1]):
                shared.add(i)

        for r in block:
            note = [
                "Prism table %r, column %r, replicate subcolumn %d" % (
                    sheet, r["arm"], r["rep"]),
                'row title "%s" converted to hours' % r["label"],
                unit_note,
                no_meta,
            ]
            if reps_declared:
                note.append("the table declares YFormat=%r Replicates=%s but "
                            "never says whether the subcolumns are biological "
                            "or technical, so they are numbered 1-%s and "
                            "tech_replicate is left blank" % (
                                table.get("YFormat", ""), reps_declared,
                                reps_declared))
            if r["i"] in shared:
                note.append("every arm in this table carries the identical "
                            "values at this timepoint, so these rows are one "
                            "measurement repeated across the arm columns, not "
                            "one reading per arm -- at Day 0 that is the shared "
                            "inoculum")
            if r["v"] == 0:
                note.append("the file writes this reading as a literal 0; the "
                            "deposit states no floor, so a 0 here cannot be "
                            "read as either a true absence or a below-limit "
                            "placeholder, and it is kept as 0 and left "
                            "uncensored")
            rows.append({
                "source_file": path.name,
                "sheet": sheet,
                "organism": "",
                "strain": "",
                "drug": "" if CONTROL_RE.match(r["arm"]) else r["arm"],
                "concentration": np.nan,
                "conc_unit": "",
                "arm": r["arm"],
                "replicate": str(r["rep"]),
                "tech_replicate": "",
                "time_h": r["t"],
                "cfu_per_ml": float(r["v"]),
                "floor_cfu_per_ml": floor,
                "floor_basis": basis,
                "readout": "CFU",
                "notes": "; ".join(note),
            })
    return rows


def read(d: Path) -> pd.DataFrame:
    rows = []
    for p in _prism_files(d):
        rows.extend(_read_one(p))
    if not rows:
        return empty()
    # Negative times would be a pre-exposure reading, which is not time zero of
    # treatment; this deposit has none, and any that appeared would be dropped
    # here rather than folded into the curve.
    df = pd.DataFrame(rows)
    df = df[df.time_h >= 0].copy()
    return finish(df, "YANG2024_PHAGE")
