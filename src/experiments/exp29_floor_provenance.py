"""
What is L, actually? A per-deposit audit of where the floor came from and what to call it.

Run:  python -m src.experiments.exp29_floor_provenance

WHY THIS TEST EXISTS. This paper is about a number, L, that almost nobody
reports. Having spent the paper insisting that the number be reported, we cannot
be loose about what it is. The draft currently calls the same quantity a "limit
of quantification", a "limit of detection", a "detection limit", a
"quantification limit" and an "assay floor", sometimes in adjacent sentences.
Those are not synonyms. A limit of quantification is a validated property of an
assay: the lowest concentration at which the method returns a value with stated
precision and bias. A limit of detection is the lowest concentration
distinguishable from blank. Neither is what any of these deposits gives us.

What they give us, at best, is the smallest positive count the reporting
arithmetic can return: one colony in the volume plated, or the lowest rung of an
MPN table. That number is real and it is load-bearing, but it is an OPERATIONAL
ASSAY FLOOR, not a validated LOQ, and calling it one imports a claim about
precision that no source in this paper has made. This experiment establishes,
per deposit and from the files themselves, which of the two we actually have.

WHAT IT DOES.

  1. Scans each deposit for the strings a source would use if it stated a limit.
     This is the part that has to be mechanical: an assertion that "the source
     states no limit" is worth nothing unless the search that failed to find one
     is recorded. The source's own bytes and this project's provenance records
     are scanned SEPARATELY and never merged, because our own note that a limit
     is absent is not evidence about what the source said, and an early version
     of this scan reported a limit "found" in the clinical deposit that was in
     fact our own line about a different paper in data/raw/SOURCES.json.

  2. Labels how the value in use was obtained. STATED by the source; DERIVED
     from a recorded plated volume by the identity L = 1000/V for counts per mL;
     INFERRED from a pile-up on the observed minimum; FLAGGED, meaning the
     deposit marks readings as below a limit whose value it never gives; or
     NONE, where no floor is evidenced at all.

  3. Assigns the term the evidence supports. Only a value the source validated
     earns "limit of quantification". Everything else here is an operational
     assay floor or a minimum reportable positive count.

  4. Records how replicate plates were treated and whether volumes were pooled.
     For the six-laboratory deposit this is not a formality. Each flask-visit is
     plated at up to four volumes -- 100 uL quadruplicate, 10 uL as four drops,
     10 uL as a single drop, 2.5 uL as a single drop -- and the reported count
     per mL sits on the 1000/V lattice of the volume in its own row. So one
     flask-visit carries readings against THREE different floors, 10, 100 and 400
     CFU/mL, a spread of 1.6 log10. The analysis judges every reading against the
     floor its own volume implies and never pools them, and the sweep below says
     what pooling would cost.

  5. Sweeps the alternatives. For the clinical deposit the floor is inferred, so
     the load-bearing counts are recomputed at every value a three-tube MPN table
     returns at or below 23. For the six-laboratory deposit the per-volume floors
     are compared against four pooled alternatives.

  6. Reproduces what docs/21_FLOOR_INFERENCE.md records for the three deposits it
     covers, and says where this goes further, so the two cannot drift apart
     unnoticed.

WHAT IT FOUND, IN ONE LINE EACH. Not one of the five deposits states a limit of
quantification with a value. The six-laboratory deposit names the concept -- its
BQL column is literally "below quantification limit" -- but defines it as an
operator's judgement of countability ("uncountable culture/too few or no
colonies") and never gives a number, so even there the number is ours, derived
from the volume the deposit does record. The clinical floor of 23 MPN/mL and the
Dubey floor of 10 CFU/mL survive their sweeps; the Kaur deposit supports no floor
at all and the Windels deposit reports surviving fractions with the below-limit
readings written as exact zeros, which fixes no value whatever.

TWO THINGS THIS TURNED UP THAT THE PAPER SHOULD FIX. First, the terminology: on
the evidence collected here, "limit of quantification" is the wrong term for
every value the paper uses, and "operational assay floor" or "minimum reportable
positive count" is the right one. Second, a denominator: the same 498 below-limit
flags are 17.9 per cent of the 2,775 rows in the six-laboratory file and 19.3 per
cent of the 2,580-row analysis set, and the Methods currently pair the second
figure with the first denominator.

Writes:
  results/tables/exp29_floor_provenance.csv
  results/tables/exp29_floor_sensitivity.csv
  results/receipts/exp29_receipt.json
"""
from __future__ import annotations

import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw"
TABLES = ROOT / "results" / "tables"
RECEIPTS = ROOT / "results" / "receipts"

VIJAY = DATA / "tb" / "elife93243_supp2.xlsx"
ERA4TB = DATA / "tb" / "era4tb_timekill.csv"
ERA4TB_README = DATA / "tb" / "era4tb_readme.txt"
WINDELS_DIR = DATA / "windels2024"
WINDELS = WINDELS_DIR / "timekill.csv"
KAUR = DATA / "apramycin_mtb" / "Raw Data.xlsx"
KAUR_PROV = DATA / "apramycin_mtb" / "PROVENANCE.json"
DUBEY = DATA / "dubey2026" / "source_data.xlsx"
DUBEY_PROV = DATA / "dubey2026" / "PROVENANCE.json"
SOURCES = DATA / "SOURCES.json"

# Values a standard three-tube most-probable-number table returns at or below the
# observed minimum of the clinical deposit. Taken from src/infer_floor.py so the
# two modules sweep the same ladder.
MPN_TABLE_AT_OR_BELOW_23 = (3.0, 3.6, 7.2, 7.4, 9.2, 11.0, 14.0, 15.0, 20.0,
                            21.0, 23.0)
MPN_FLOOR = 23.0
DEPTH_LOGS = 4.0                     # the 99.99 per cent endpoint
CLASS_CUTS = (1e-3, 1e-2)            # Low < 1e-3 <= Medium <= 1e-2 < High
CLASS_ORDER = ("Low", "Medium", "High")
DUBEY_PLACEHOLDER = 1.0              # a 100 uL plate cannot return 1 per mL

# What a source would have to write for us to say it stated a limit. Deliberately
# generous: a false positive here costs one line of reading, a false negative
# costs the paper a wrong claim about a source.
LIMIT_PATTERNS = (
    r"limit of quantification", r"limit of quantitation", r"limit of detection",
    r"quantification limit", r"quantitation limit", r"detection limit",
    r"\bLLOQ\b", r"\bLOQ\b", r"\bLOD\b", r"\bBQL\b", r"\bAQL\b",
    r"below (the )?limit", r"above (the )?limit", r"lower limit",
    r"assay floor", r"countable", r"quantifiable",
)
_LIMIT_RE = re.compile("|".join(LIMIT_PATTERNS), re.IGNORECASE)
# Naming a limit is not stating one. A stated limit is a number carrying a
# concentration unit, so the test near a match is for a quantity, not a digit:
# "[0: countable culture, 1: uncountable culture]" contains digits and states
# nothing. The window is deliberately narrow so a number elsewhere in a long
# provenance paragraph cannot be read as the limit.
_VALUE_RE = re.compile(
    r"\d[\d.,]*\s*(?:[x*]\s*10\s*\^?\s*-?\d+)?\s*"
    r"(?:CFU|cfu|MPN|colony|colonies|log\s*10|log10)?\s*"
    r"(?:/|per\s+)\s*(?:mL|ml|millilitre|milliliter)",
    re.IGNORECASE)
_VALUE_WINDOW = 80


# --------------------------------------------------------------- text scan ---
def _strings_from_xlsx(path: Path) -> list[str]:
    """Every literal string in a workbook, headers and cell text alike.

    Numbers live in the sheet XML and strings in sharedStrings; a stated limit
    would be prose, so sharedStrings is the right place to look. Reading the
    archive directly rather than through pandas means a limit written into a
    stray cell on an unread sheet is still found.
    """
    with zipfile.ZipFile(path) as z:
        if "xl/sharedStrings.xml" not in z.namelist():
            return []
        xml = z.read("xl/sharedStrings.xml").decode("utf-8", errors="ignore")
    return [re.sub(r"<[^>]+>", "", m) for m in
            re.findall(r"<si>(.*?)</si>", xml, flags=re.S)]


def _strings_from_text(path: Path) -> list[str]:
    raw = path.read_bytes().decode("latin-1")
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def _strings_from_csv(path: Path) -> list[str]:
    """Header row plus every non-numeric cell. A limit written into a CSV would
    be in a column name or a comment field, not in the numeric body."""
    raw = path.read_bytes().decode("latin-1")
    out = []
    for i, line in enumerate(raw.splitlines()):
        if i == 0:
            out.append(line.strip())
            out += [c.strip() for c in line.split(",") if c.strip()]
        else:
            out += [c.strip() for c in line.split(",")
                    if c.strip() and not re.fullmatch(r"-?[\d.eE+-]+", c.strip())]
    return sorted(set(out))


def _sources_entry(key: str) -> list[str]:
    """This project's SOURCES.json entry for one deposit, and only that one.

    Scanning the whole file matches other papers' notes. An early version did
    exactly that and reported a limit of detection "found" for the clinical
    deposit that was our own sentence about Drusano 2018.
    """
    rec = json.loads(SOURCES.read_text(encoding="utf-8"))
    for s in rec.get("sources", []):
        if s.get("key") == key:
            return [f"{k}: {v}" for k, v in s.items()]
    return [f"NO ENTRY for key '{key}' in data/raw/SOURCES.json"]


def _scan_strings(strings: list[str], where: str) -> list[dict]:
    hits = []
    for s in strings:
        for m in _LIMIT_RE.finditer(s):
            lo = max(0, m.start() - _VALUE_WINDOW)
            hi = min(len(s), m.end() + _VALUE_WINDOW)
            hits.append({
                "where": where,
                "term": m.group(0),
                "text": s[:300],
                "states_a_value": bool(_VALUE_RE.search(s[lo:hi])),
            })
            break                      # one hit per string is enough to read it
    return hits


def scan_for_limit_terms(deposit_files: list[Path],
                         project_records: list[Path] | None = None,
                         sources_key: str | None = None) -> dict:
    """Search a deposit's own bytes for a stated limit, and record the search.

    Two searches, kept apart. The first covers only what the depositors wrote:
    the data file and any readme they supplied. The second covers what this
    project wrote about the deposit. Only the first can answer "does the source
    state a limit", and merging them is how a project note becomes, three steps
    later, a claim about a source.

    A match is further split by whether a concentration value appears beside it.
    Naming the concept is not stating a limit, and the ERA4TB deposit is exactly
    that case: its column definitions say "below quantification limit" and never
    give a number.
    """
    scanned, hits = 0, []
    for p in deposit_files:
        if not p.exists():
            hits.append({"where": "deposit", "term": "FILE ABSENT",
                         "text": str(p), "states_a_value": False})
            continue
        if p.suffix.lower() in (".xlsx", ".xls"):
            strings = _strings_from_xlsx(p)
        elif p.suffix.lower() == ".csv":
            strings = _strings_from_csv(p)
        else:
            strings = _strings_from_text(p)
        scanned += len(strings)
        hits += _scan_strings(strings, f"deposit: {p.relative_to(ROOT)}")

    proj_scanned, proj_hits = 0, []
    for p in (project_records or []):
        if not p.exists():
            continue
        strings = _strings_from_text(p)
        proj_scanned += len(strings)
        proj_hits += _scan_strings(strings, f"project record: {p.relative_to(ROOT)}")
    if sources_key is not None:
        strings = _sources_entry(sources_key)
        proj_scanned += len(strings)
        proj_hits += _scan_strings(
            strings, f"project record: data/raw/SOURCES.json[{sources_key}]")

    return {
        "deposit_strings_scanned": scanned,
        "deposit_matches": len(hits),
        "deposit_matches_stating_a_value": sum(h["states_a_value"] for h in hits),
        "deposit_hits": hits,
        "project_record_strings_scanned": proj_scanned,
        "project_record_matches": len(proj_hits),
        "project_record_hits": proj_hits,
    }


# ------------------------------------------------------- clinical (Vijay) ---
def _class_of(fraction: float) -> str:
    lo, hi = CLASS_CUTS
    return "Low" if fraction < lo else ("Medium" if fraction <= hi else "High")


def vijay_evidence() -> dict:
    """The four facts that stand behind an INFERRED floor of 23 MPN/mL."""
    d = pd.read_excel(VIJAY)
    cols = [c for c in d.columns if c.startswith("mpn_") and "log" not in c]
    allv = pd.concat([pd.to_numeric(d[c], errors="coerce") for c in cols]).dropna()
    per_visit = {c: float(pd.to_numeric(d[c], errors="coerce").min()) for c in cols}
    lo = float(allv.min())
    return {
        "n_readings": int(len(allv)),
        "minimum_per_ml": lo,
        "n_exactly_at_minimum": int((allv == lo).sum()),
        "n_below_minimum": int((allv < lo).sum()),
        "minimum_by_column": per_visit,
        "minimum_is_an_mpn_table_value": bool(
            any(abs(lo - x) < 1e-9 for x in MPN_TABLE_AT_OR_BELOW_23)),
        "mpn_rungs_below_the_minimum_that_never_appear": [
            x for x in MPN_TABLE_AT_OR_BELOW_23 if x < lo],
        "plated_volume_recorded": False,
    }


def sweep_clinical() -> tuple[pd.DataFrame, dict]:
    """Recompute every load-bearing count at every MPN rung at or below 23.

    Two quantities move with L and both are load-bearing. The first is headroom:
    an isolate with fewer than four logs between its starting density and the
    floor cannot show a 99.99 per cent reduction, so its deepest endpoint is
    unreachable however the drug behaves. The second is observability: a day-5
    reading resting on the floor bounds the surviving fraction at L/N0 rather
    than measuring it, and where only one tolerance class is reachable across the
    range 0 to L the label was fixed by the inoculum before the drug went in.

    Lowering the assumed floor moves these in OPPOSITE directions, which is why
    the sweep is worth running rather than asserting. A lower floor buys headroom,
    so fewer isolates are short of four logs. But a lower floor also means no
    reading sits on it -- 23 is the smallest value in the file -- so every call
    becomes nominally determinable. The second effect is not a reassurance. It is
    the arithmetic consequence of assuming a floor the data give no sign of, and
    the last two columns say how much it costs to assume it: at a floor of 3.0 the
    ten MPN rungs between 3.0 and 23 are all empty while 23 itself carries 33
    readings out of 1,932.

    THE LADDER STOPS AT 23 AND THE REASON IS NOT COSMETIC, so it is worth stating
    rather than leaving the range to imply a robustness it does not have. A floor
    above 23 is excluded outright: 33 readings sit exactly on 23 and a floor above
    them would put readings below the floor, which is impossible. That is a proof,
    not a preference, and it is why only the downward direction is swept. But it
    also means the stability of these counts across the ladder -- 28 to 33 short
    of four logs -- is stability in the only direction the deposit permits, and a
    reader should not carry it over to the direction it does not. For scale, were
    the floor of the day-5 column instead the 230 that the day-2 column bottoms
    out at, the count short of four logs would go from 33 to 133 and the
    undecidable calls from 6 to 52. Nothing in the deposit supports that reading
    -- the per-visit minima step by a factor of ten because the dilutions do --
    but the asymmetry is the honest description of the sensitivity.
    """
    d = pd.read_excel(VIJAY)
    mpn_cols = [c for c in d.columns if c.startswith("mpn_") and "log" not in c]
    allv = pd.concat([pd.to_numeric(d[c], errors="coerce")
                      for c in mpn_cols]).dropna()
    rows = []
    for L in MPN_TABLE_AT_OR_BELOW_23:
        rec = {"assumed_floor_per_ml": L, "assumed_floor_log10": float(np.log10(L))}
        for age in (15, 60):
            n0 = pd.to_numeric(d[f"mpn_T0_{age}days"], errors="coerce")
            n5 = pd.to_numeric(d[f"mpn_T5_{age}days"], errors="coerce")
            lab = d[f"Tolerant_level_D5_{age}"]
            head = np.log10(n0 / L)
            usable = n0.notna() & n5.notna() & lab.isin(CLASS_ORDER)

            at_floor = (n5 <= L) & usable
            low_end = np.array([_class_of(0.0)] * len(n0))
            high_end = np.array([_class_of(L / v) if v and v > 0 else None
                                 for v in n0])
            forced = at_floor & (low_end == high_end)
            undecidable = at_floor & ~forced

            rec[f"n_short_of_4_logs_{age}d"] = int((head < DEPTH_LOGS).sum())
            rec[f"pct_short_of_4_logs_{age}d"] = float(
                100 * (head < DEPTH_LOGS).sum() / int(n0.notna().sum()))
            rec[f"n_calls_{age}d"] = int(usable.sum())
            rec[f"n_at_floor_{age}d"] = int(at_floor.sum())
            rec[f"n_determinable_{age}d"] = int((usable & ~at_floor).sum())
            rec[f"n_forced_by_inoculum_{age}d"] = int(forced.sum())
            rec[f"n_undecidable_{age}d"] = int(undecidable.sum())
            # The forced/undecidable split turns on where L/N0 falls relative to
            # the deposited class cut of 1e-3, and some isolates land exactly on
            # it: 23/23000 is 1e-3 to the last bit, and under the deposit's own
            # rule -- Low below 1e-3, Medium at it and above -- an upper bound of
            # exactly 1e-3 spans two classes and the call is filed undecidable.
            # It is undecidable only at a single point, so the count is recorded
            # here rather than left for a reader to discover that the 12/6 split
            # rests on an exact tie.
            ub = np.where(n0 > 0, L / n0, np.nan)
            rec[f"n_at_floor_whose_bound_sits_exactly_on_a_class_cut_{age}d"] = int(
                (at_floor & np.isin(ub, CLASS_CUTS)).sum())

        # Baseline-only stratum: the 174 rows with no earlier isolate from the
        # same patient. Repeated isolates exist in this deposit but their patient
        # linkage is not recoverable from it, so this is the only clean stratum.
        base = d[d["Time_point"] == "0M"]
        n0b = pd.to_numeric(base["mpn_T0_15days"], errors="coerce")
        rec["n_short_of_4_logs_15d_baseline_only"] = int(
            (np.log10(n0b / L) < DEPTH_LOGS).sum())
        rec["n_baseline_only"] = int(n0b.notna().sum())

        # What it costs to assume this floor: rungs the MPN table offers between
        # the candidate and the observed minimum, and how many readings use them.
        gap = [x for x in MPN_TABLE_AT_OR_BELOW_23 if L <= x < MPN_FLOOR]
        rec["n_mpn_rungs_between_this_floor_and_23"] = len(gap)
        rec["n_readings_on_those_rungs"] = int(allv.isin(gap).sum())
        rows.append(rec)

    t = pd.DataFrame(rows)
    at23 = t[t["assumed_floor_per_ml"] == MPN_FLOOR].iloc[0]
    at30 = t[t["assumed_floor_per_ml"] == 3.0].iloc[0]

    # The one number that says how asymmetric this sweep is. The ladder cannot go
    # above 23 because readings sit on 23, but a reader is owed the size of the
    # effect in the direction the ladder cannot go. The day-2 column bottoms out
    # at 230, ten times higher, so 230 is the natural upward counterfactual even
    # though nothing in the deposit supports applying it to the day-5 column.
    n0 = pd.to_numeric(d["mpn_T0_15days"], errors="coerce")
    n5 = pd.to_numeric(d["mpn_T5_15days"], errors="coerce")
    lab = d["Tolerant_level_D5_15"]
    usable = n0.notna() & n5.notna() & lab.isin(CLASS_ORDER)
    up = float(pd.to_numeric(d["mpn_T2_15days"], errors="coerce").min())
    at_up = (n5 <= up) & usable
    forced_up = at_up & np.array([bool(v and v > 0 and _class_of(up / v) == "Low")
                                  for v in n0])
    upward = {
        "assumed_floor_per_ml": up,
        "why_this_value": "the day-2 column's own minimum, a factor of ten above "
                          "the day-5 minimum the analysis uses",
        "excluded_because": f"{int((allv == MPN_FLOOR).sum())} readings sit "
                            f"exactly on {MPN_FLOOR:g}; a floor above them would "
                            "put readings below the floor",
        "n_short_of_4_logs_15d": int((np.log10(n0 / up) < DEPTH_LOGS).sum()),
        "n_undecidable_15d": int((at_up & ~forced_up).sum()),
    }

    summ = {
        "upward_counterfactual_not_in_the_ladder": upward,
        "n_short_of_4_logs_15d_range": [int(t["n_short_of_4_logs_15d"].min()),
                                        int(t["n_short_of_4_logs_15d"].max())],
        "n_short_of_4_logs_15d_at_23": int(at23["n_short_of_4_logs_15d"]),
        "n_short_of_4_logs_15d_at_3": int(at30["n_short_of_4_logs_15d"]),
        "n_undecidable_15d_at_23": int(at23["n_undecidable_15d"]),
        "n_forced_by_inoculum_15d_at_23": int(at23["n_forced_by_inoculum_15d"]),
        "n_calls_15d": int(at23["n_calls_15d"]),
        "mpn_rungs_from_3_up_to_but_excluding_23":
            int(at30["n_mpn_rungs_between_this_floor_and_23"]),
        "readings_on_those_rungs": int(at30["n_readings_on_those_rungs"]),
        "readings_exactly_on_23": int((allv == MPN_FLOOR).sum()),
        "n_readings_total": int(len(allv)),
    }
    return t, summ


# --------------------------------------------- six laboratories (ERA4TB) ---
def era4tb_load() -> pd.DataFrame:
    d = pd.read_csv(ERA4TB, encoding="latin-1")
    d["y"] = pd.to_numeric(d["CFUlog10"], errors="coerce")
    d["cfu"] = pd.to_numeric(d["CFU"], errors="coerce")
    d["floor_own_volume"] = 1000.0 / d["Volume"]
    d["loq_own_volume"] = np.log10(d["floor_own_volume"])
    return d


def era4tb_evidence(d: pd.DataFrame) -> dict:
    """Is 1000/V really the floor, and did the depositors pool the replicates?

    The second question answers itself from the lattice, but only if the test is
    stated so that it could fail. A 100 uL plate read in quadruplicate, if the
    four plates were pooled, would report counts per mL in steps of 1000/400 =
    2.5. Saying that every quadruplicate reading is a multiple of 10 does NOT on
    its own exclude that: every multiple of 10 is also a multiple of 2.5, so the
    readings sit on the pooled lattice as well as the single-plate one and the
    observation is consistent with both. What excludes pooling is the pooled
    lattice's other three rungs. Under pooling the reported value is 2.5 times the
    colonies counted across four plates, which lands on a multiple of 10 only when
    that total is divisible by four, so three readings in four should sit at a
    x2.5, x5.0 or x7.5 rung, and none of the 533 does.

    That test has force only where the reported precision could have expressed
    such a rung, which is why the small readings carry the argument and the large
    ones do not: a count of 2 300 000 is a multiple of 10 whatever the arithmetic
    behind it, because the deposit reports two or three significant figures. The
    informative subset is the 91 readings below 1 000 and above all the 24 below
    100, which take the values 10, 20, 30, 40, 50, 70, 80 and 90 and never 25, 45
    or 75; the smallest reading in the whole 100 uL set is exactly 10 and not the
    2.5 that four pooled plates would allow. So the deposited number is a
    single-plate count scaled by its own volume and the replicate plates were not
    pooled into it -- on the evidence of two dozen readings, not of 533.

    The same test at 10 uL in four drops finds 13 readings, all from one
    laboratory, that miss the 1000/10 lattice, so the arithmetic is not uniform
    across the six laboratories and the derivation is exact for 535 of 548 rather
    than for all of them. That is worth saying out loud rather than rounding to
    "the floor is derived".
    """
    out = {"n_rows": int(len(d))}
    q = d[d["cfu"].notna() & (d["cfu"] > 0) & d["Volume"].notna()]
    out["n_quantified_counts"] = int(len(q))
    out["n_counts_below_their_own_volume_floor"] = int(
        (q["cfu"] < q["floor_own_volume"] - 1e-9).sum())
    out["n_counts_exactly_on_their_own_volume_floor"] = int(
        np.isclose(q["cfu"], q["floor_own_volume"]).sum())

    lattice = []
    for (vol, cond), s in d.groupby(["Volume", "Condition"]):
        cf = s["cfu"].dropna()
        cf = cf[cf > 0]
        if not len(cf):
            continue
        step = 1000.0 / vol
        on = np.isclose(cf / step, np.round(cf / step))
        lattice.append({
            "plated_volume_ul": float(vol),
            "plating_format": str(s["Comments"].dropna().iloc[0])
            .replace("\xb5", "u").encode("ascii", "replace").decode(),
            "n_counts": int(len(cf)),
            "implied_floor_per_ml": float(step),
            "smallest_count_per_ml": float(cf.min()),
            "smallest_equals_implied_floor": bool(np.isclose(cf.min(), step)),
            "fraction_on_the_1000_over_V_lattice": float(on.mean()),
            "n_off_lattice": int((~on).sum()),
            "off_lattice_institutes": sorted(
                s.loc[cf.index[~on], "Institute"].unique().tolist()),
        })
    out["by_volume_and_format"] = lattice

    # The pooling test, with the half that can fail it. Multiples of 10 are a
    # subset of multiples of 2.5, so counting them settles nothing on its own;
    # what settles it is that the pooled lattice's other three rungs are empty,
    # and that the emptiness is visible in the readings small enough for such a
    # rung to have been written down at all.
    cf100 = d.loc[(d["Volume"] == 100.0) & d["cfu"].notna() & (d["cfu"] > 0),
                  "cfu"]
    on25 = np.abs(cf100 / 2.5 - np.round(cf100 / 2.5)) < 1e-9
    on10 = np.abs(cf100 / 10.0 - np.round(cf100 / 10.0)) < 1e-9
    out["pooling_test_100ul"] = {
        "n_readings": int(len(cf100)),
        "n_on_the_pooled_2_5_lattice": int(on25.sum()),
        "n_on_the_single_plate_10_lattice": int(on10.sum()),
        "n_on_2_5_but_off_10": int((on25 & ~on10).sum()),
        "n_readings_below_1000": int((cf100 < 1000).sum()),
        "n_readings_below_100": int((cf100 < 100).sum()),
        "distinct_values_below_100": sorted(
            float(x) for x in cf100[cf100 < 100].unique()),
        "smallest_reading": float(cf100.min()),
        "n_at_a_pooled_only_rung_below_10": int(
            cf100.isin([2.5, 5.0, 7.5]).sum()),
        "note": "Every multiple of 10 is a multiple of 2.5, so the count on the "
                "10 lattice cannot by itself exclude pooling. The discriminating "
                "count is n_on_2_5_but_off_10, which under pooling should be "
                "about three readings in four and is 0. The test has force only "
                "where the reported precision could have expressed a x2.5, x5.0 "
                "or x7.5 rung, so the argument rests on the readings below 1 000 "
                "and above all on those below 100, not on all 533.",
    }

    # How many distinct floors does one flask-visit carry?
    fv = d.groupby(["Institute", "Sample", "Replicate", "Time"])
    spread = fv["floor_own_volume"].agg(["nunique", "min", "max", "size"])
    out["n_flask_visits"] = int(len(spread))
    out["platings_per_flask_visit_median"] = float(spread["size"].median())
    out["distinct_floors_per_flask_visit"] = {
        int(k): int(v) for k, v in spread["nunique"].value_counts().sort_index().items()}
    ok = spread["min"] > 0
    out["max_floor_spread_within_a_flask_visit_log10"] = float(
        np.log10(spread.loc[ok, "max"] / spread.loc[ok, "min"]).max())

    # Duplicate (Institute, Sample, Replicate, Volume, Time) keys are real and
    # are not an error: 10 uL is plated twice at the same visit, once as four
    # drops and once as a single drop. Keying on Condition as well separates them.
    k4 = d.groupby(["Institute", "Sample", "Replicate", "Volume", "Time"]).size()
    k5 = d.groupby(["Institute", "Sample", "Replicate", "Volume", "Condition",
                    "Time"]).size()
    out["n_keys_without_condition"] = int(len(k4))
    out["n_keys_with_more_than_one_row_without_condition"] = int((k4 > 1).sum())
    out["n_keys_with_condition"] = int(len(k5))
    out["n_keys_with_more_than_one_row_with_condition"] = int((k5 > 1).sum())

    # Three rows carry a Volume that its own Comments field contradicts, and one
    # carries no Volume at all. They are the pre-timepoint inoculum readings from
    # one laboratory. They are recorded rather than quietly dropped, because a
    # floor DERIVED from a recorded volume is only as good as the volume field,
    # and here the volume field is wrong four times in 2,775 rows.
    odd = d[(d["Volume"].isna()) |
            ((d["Volume"] == 50.0) & d["Comments"].astype(str).str.contains("100"))]
    out["rows_whose_volume_field_is_unusable"] = {
        "n": int(len(odd)),
        "detail": [{"institute": r.Institute, "sample": r.Sample,
                    "time": float(r.Time), "volume_ul": None if pd.isna(r.Volume)
                    else float(r.Volume),
                    "comments": str(r.Comments).replace("\xb5", "u")}
                   for r in odd.itertuples()],
        "note": "Comments say 100 uL quad while Volume says 50 (or is blank); all "
                "are Time = -3 pre-timepoint readings from one laboratory and none "
                "enters a killing series.",
    }

    # A flag rate needs its denominator attached. The whole file is 2,775 rows;
    # exp17's analysis set is the 2,580 that survive dropping the above-limit
    # flags, the rows with no usable value and the pre-treatment visits. The same
    # 498 flags give 17.9 per cent of the first and 19.3 per cent of the second,
    # and the Methods currently pair the second figure with the first denominator.
    an = d[(d["AQL"] == 0)]
    y = np.where(an["BQL"] == 1, an["loq_own_volume"], an["y"])
    an = an[pd.notna(y) & (an["Time"] >= 0)]
    out["flag_rate_denominators"] = {
        "all_rows_in_file": int(len(d)),
        "pct_flagged_below_over_all_rows": float(100 * (d["BQL"] == 1).mean()),
        "rows_in_the_exp17_analysis_set": int(len(an)),
        "pct_flagged_below_over_analysis_set": float(100 * (an["BQL"] == 1).mean()),
        "n_flags": int((d["BQL"] == 1).sum()),
    }

    out["n_bql_flags"] = int((d["BQL"] == 1).sum())
    out["n_aql_flags"] = int((d["AQL"] == 1).sum())
    out["n_bql_flags_that_retain_a_count"] = int(
        ((d["BQL"] == 1) & d["cfu"].notna()).sum())
    out["n_rows_with_no_count_and_no_flag"] = int(
        (d["cfu"].isna() & (d["BQL"] != 1) & (d["AQL"] != 1)).sum())
    return out


def _contradicted_flags(d: pd.DataFrame, pooled_floor: float | None) -> dict:
    """How many below-limit flags does the deposit itself contradict?

    A flag is contradicted when another plating of the SAME flask at the SAME
    visit, whose own limit is at least as sensitive, returns a quantified count
    above the flagged reading's limit. Passing a pooled floor replaces every
    per-volume limit with one number, which is exactly the counterfactual this
    function exists to price: under pooling every plating is "at least as
    sensitive" as every other, and the threshold the contradiction is judged
    against stops depending on which plate produced the flag.
    """
    if pooled_floor is None:
        loq = d["loq_own_volume"]
    else:
        loq = pd.Series(np.log10(pooled_floor), index=d.index)
    w = d.assign(_loq=loq)
    n_checked = n_comparator = n_contra = 0
    for _, g in w.groupby(["Institute", "Sample", "Replicate", "Time"]):
        flagged = g[g["BQL"] == 1]
        if flagged.empty or len(g) < 2:
            continue
        quant = g[(g["BQL"] != 1) & (g["AQL"] != 1)].dropna(subset=["y"])
        for _, r in flagged.iterrows():
            better = quant[quant["_loq"] <= r["_loq"] + 1e-12]
            n_checked += 1
            if len(better):
                n_comparator += 1
                if better["y"].max() > r["_loq"]:
                    n_contra += 1
    # Two different denominators, and the difference matters. n_flags_checkable
    # is every flag that sits in a flask-visit with more than one plating, which
    # is all 498 of them; it is the denominator the Methods use. But most of
    # those visits hold no quantified companion at an at-least-as-sensitive
    # limit, so most flags cannot be contradicted by construction. Judged only
    # against the flags that actually have a comparator, the contradiction rate
    # is far higher, and reporting the first number without the second would let
    # a reader take 16.7 per cent as the rate at which the deposit's own flags
    # are wrong when it is the rate at which they are demonstrably wrong.
    return {"n_flags_checkable": n_checked,
            "n_flags_with_a_comparator": n_comparator,
            "n_contradicted": n_contra}


def sweep_era4tb(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Per-volume floors against the pooled alternatives, and what pooling costs.

    The deposit plates one flask-visit at up to four volumes, so a pooled floor
    is not a simplification of the truth but a contradiction of it: a count of 40
    CFU/mL from a 100 uL plate is a genuine quantified reading and the same
    number is unreachable from a 2.5 uL drop. Pooling has to pick one, and each
    choice breaks something specific.

      pooled at the most sensitive volume (10 CFU/mL) treats the 2.5 uL drops as
      forty times better than they are, so their below-limit flags are judged
      against a threshold no 2.5 uL plate could ever have met;

      pooled at the least sensitive volume (400 CFU/mL) throws away every genuine
      count between 10 and 400 CFU/mL, which is where the killing curves spend
      their tails.

    Both are reported as counts, not adjectives.
    """
    q = d[d["cfu"].notna() & (d["cfu"] > 0)]
    schemes = [
        ("per-volume (as analysed)", None),
        ("pooled at the most sensitive volume, 100 uL", 10.0),
        ("pooled at the modal volume, 10 uL", 100.0),
        ("pooled at the least sensitive volume, 2.5 uL", 400.0),
        ("pooled at the geometric mean of the per-volume floors",
         float(10.0 ** np.log10(1000.0 / d["Volume"].dropna()).mean())),
    ]
    rows = []
    for name, L in schemes:
        if L is None:
            lost = int((q["cfu"] < q["floor_own_volume"] - 1e-9).sum())
            on = int(np.isclose(q["cfu"], q["floor_own_volume"]).sum())
            floor_txt = "10, 100 or 400 by volume"
            fl = np.nan
        else:
            lost = int((q["cfu"] < L - 1e-9).sum())
            on = int(np.isclose(q["cfu"], L).sum())
            floor_txt = f"{L:g}"
            fl = float(np.log10(L))
        flags = _contradicted_flags(d, L)
        rows.append({
            "scheme": name,
            "floor_per_ml": floor_txt,
            "floor_log10": fl,
            "n_quantified_counts": int(len(q)),
            "n_genuine_counts_this_floor_would_discard": lost,
            "pct_genuine_counts_discarded": 100.0 * lost / len(q),
            "n_counts_sitting_exactly_on_the_floor": on,
            "n_below_limit_flags": int((d["BQL"] == 1).sum()),
            "n_flags_checkable": flags["n_flags_checkable"],
            "n_flags_with_a_comparator": flags["n_flags_with_a_comparator"],
            "n_flags_contradicted": flags["n_contradicted"],
            "pct_flags_contradicted": 100.0 * flags["n_contradicted"] /
                                      max(1, int((d["BQL"] == 1).sum())),
            "pct_of_flags_with_a_comparator_contradicted":
                100.0 * flags["n_contradicted"] /
                max(1, flags["n_flags_with_a_comparator"]),
        })
    t = pd.DataFrame(rows)
    base = t.iloc[0]
    worst = t["n_genuine_counts_this_floor_would_discard"].max()
    summ = {
        "n_quantified_counts": int(base["n_quantified_counts"]),
        "per_volume_flags_contradicted": int(base["n_flags_contradicted"]),
        "per_volume_pct_flags_contradicted": float(base["pct_flags_contradicted"]),
        "per_volume_flags_with_a_comparator": int(
            base["n_flags_with_a_comparator"]),
        "per_volume_pct_of_comparable_flags_contradicted": float(
            base["pct_of_flags_with_a_comparator_contradicted"]),
        "flags_with_a_comparator_by_scheme": dict(
            zip(t["scheme"], t["n_flags_with_a_comparator"].astype(int))),
        "max_genuine_counts_a_pooled_floor_would_discard": int(worst),
        "pct_at_the_least_sensitive_pooled_floor": float(
            t.loc[t["floor_per_ml"] == "400", "pct_genuine_counts_discarded"].iloc[0]),
        "flags_contradicted_by_scheme": dict(
            zip(t["scheme"], t["n_flags_contradicted"].astype(int))),
    }
    return t, summ


# ------------------------------------------------ the three smaller sets ---
def kaur_evidence() -> dict:
    """A deposit that supports no floor, reported as such.

    The minimum appears once. Under a floor, readings pile up on it; under a
    continuous tail, the minimum is just the smallest draw. One occurrence is
    what the second looks like, so no floor is evidenced and none is used. An
    earlier version of the floor module searched a list of plausible pipettes for
    one whose 1000/V matched this minimum, found 25 uL, and reported the floor as
    DERIVED. That is a coincidence dressed as a derivation and it is recorded
    here as the negative it is.
    """
    k = pd.ExcelFile(KAUR).parse("Kill kinetics")
    num = k.iloc[:, 4:7].apply(pd.to_numeric, errors="coerce").to_numpy(float).ravel()
    num = num[np.isfinite(num)]
    v = 10.0 ** num
    lo = float(v.min())
    # The three day-zero control replicates, the same cell exp28 reads for
    # Table 9, so the two experiments cannot disagree about this deposit's N0.
    n0 = pd.to_numeric(k.iloc[2, 4:7], errors="coerce").dropna()
    return {
        "n_readings": int(len(v)),
        "minimum_per_ml": lo,
        "minimum_log10": float(np.log10(lo)),
        "n_exactly_at_minimum": int((v == lo).sum()),
        "plated_volume_recorded": False,
        "n_day_zero_replicates": int(len(n0)),
        "median_log10_n0_planktonic": float(n0.median()),
    }


def windels_evidence() -> dict:
    """Surviving fractions, so no absolute count and no floor to state.

    The deposit reports survival relative to t = 0 and writes a below-limit
    reading as exactly 0. A zero fixes no value: it says the count was under
    something the deposit never names. The only quantity recoverable is the
    lowest non-zero fraction in the file, which is an upper bound on the limit
    and not the limit.
    """
    w = pd.read_csv(WINDELS)
    f = pd.to_numeric(w["surv_frac"], errors="coerce")
    zeros = f == 0
    nz = f[(f > 0)]
    return {
        "n_readings": int(f.notna().sum()),
        "n_below_limit_written_as_exact_zero": int(zeros.sum()),
        "pct_below_limit": float(100 * zeros.mean()),
        "lowest_non_zero_surviving_fraction": float(nz.min()),
        "lowest_non_zero_log10": float(np.log10(nz.min())),
        "n_grid_cells": int(w.groupby(["AB_conc", "nutrient_conc", "repl"]).ngroups),
        "n_grid_cells_with_a_zero": int(
            w.assign(z=zeros).groupby(["AB_conc", "nutrient_conc", "repl"])["z"]
            .any().sum()),
        "absolute_counts_present": False,
    }


def dubey_evidence() -> tuple[dict, pd.DataFrame]:
    """A floor derived from a recorded plated volume, checked inside the file.

    The 100 uL comes from this project's own provenance record for the deposit,
    data/raw/dubey2026/PROVENANCE.json, written when the deposit was staged. The
    published Methods are not in this repository and are NOT what was scanned
    here, so this experiment can say the volume is recorded and where, but not,
    on its own evidence, that the article's Methods state it. Keeping that
    distinction is the whole point of separating the source's bytes from ours,
    and it applies to the volume exactly as it applies to a limit.

    With 100 uL plated and counts reported per mL, L = 1000/100 = 10 CFU/mL.
    That is a derivation, not an inference, and the file corroborates it from the
    inside, which is the part that does not depend on anyone's Methods: a 100 uL
    plate reporting per mL can only return multiples of 10, every genuine count
    is one, and the smallest is exactly 10. The corroboration is carried by the
    small readings -- 20 of the 229 counts fall below 100 and take the values 10
    to 80 in steps of 10 -- since a value in the millions is a multiple of 10
    whatever the plating was. The entries of exactly 1 in the drug-treated
    columns are the below-limit placeholder, not counts, since a 100 uL plate
    cannot return 1 per mL, and the deposit's column headers say log10 while the
    columns hold linear counts.
    """
    counts, starts = [], []
    for sheet in ("Figure 1", "Figure 4"):
        s = pd.read_excel(DUBEY, sheet_name=sheet, header=None)
        t = pd.to_numeric(s[0], errors="coerce")
        for c in s.columns[1:]:
            v = pd.to_numeric(s[c], errors="coerce")
            counts.append(v[v > DUBEY_PLACEHOLDER])
        free = pd.to_numeric(s[1], errors="coerce")
        starts.append(free[(t == 0) & (free > DUBEY_PLACEHOLDER)])
    c = pd.concat(counts).dropna()
    n0 = pd.concat(starts).dropna()
    mult = np.isclose(c / 10.0, np.round(c / 10.0))
    ev = {
        "n_genuine_counts": int(len(c)),
        "n_multiples_of_10": int(mult.sum()),
        "smallest_genuine_count": float(c.min()),
        "n_genuine_counts_below_100": int((c < 100).sum()),
        "distinct_genuine_counts_below_100": sorted(
            float(x) for x in c[c < 100].unique()),
        "plated_volume_ul": 100.0,
        "plated_volume_source": "data/raw/dubey2026/PROVENANCE.json, this "
                                "project's own staging record; the published "
                                "Methods are not in this repository and were "
                                "not scanned by this experiment",
        "derived_floor_per_ml": 10.0,
        "n_cultures_with_a_measured_t0": int(len(n0)),
        "median_log10_n0": float(np.log10(n0).median()),
    }
    rows = []
    for L, why in ((1.0, "the below-limit placeholder taken literally"),
                   (10.0, "100 uL plated, as the deposit's staging record gives"),
                   (20.0, "50 uL plated"),
                   (100.0, "10 uL plated")):
        h = np.log10(n0 / L)
        rows.append({"assumed_floor_per_ml": L, "corresponds_to": why,
                     "n_cultures": int(len(n0)),
                     "median_headroom_log10": float(h.median()),
                     "n_short_of_4_logs": int((h < DEPTH_LOGS).sum())})
    return ev, pd.DataFrame(rows)


def sweep_kaur(ev: dict) -> pd.DataFrame:
    """What a floor would have to be assumed to be, and how much it would move.

    The deposit states nothing, so this is not a sensitivity analysis around a
    value we hold. It is the demonstration that the deposit cannot support one.
    Across the range a plating protocol could plausibly imply, the deepest
    resolvable reduction swings by 1.6 log10. A four-log endpoint stays reachable
    at every candidate, so a claim of that form would survive; the depth h would
    be undetermined to within a factor of forty, and h is the quantity the paper
    tabulates. That is why the Kaur row of Table 9 is NA rather than a number
    with a caveat.
    """
    n0 = ev["median_log10_n0_planktonic"]
    rows = []
    for L, why in ((10.0, "100 uL plated, if it had been stated"),
                   (40.0, "the observed minimum, which occurs once"),
                   (100.0, "10 uL plated, if it had been stated"),
                   (400.0, "2.5 uL plated, if it had been stated")):
        rows.append({"assumed_floor_per_ml": L, "corresponds_to": why,
                     "median_log10_n0": n0,
                     "headroom_log10": n0 - float(np.log10(L)),
                     "four_log_endpoint_reachable": bool(
                         n0 - float(np.log10(L)) >= DEPTH_LOGS)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- assembly ---
def provenance_table(scans: dict, vij: dict, era: dict, kaur: dict,
                     win: dict, dub: dict) -> pd.DataFrame:
    era_min = {r["plated_volume_ul"]: r["smallest_count_per_ml"]
               for r in era["by_volume_and_format"]}
    rows = [
        {
            "dataset": "Vijay 2024, 217 clinical M. tuberculosis isolates",
            "source_states_lod": "no",
            "source_states_loq": "no",
            "value_used": f"{vij['minimum_per_ml']:g}",
            "units": "MPN per mL",
            "how_obtained": "INFERRED",
            "correct_term": "operational assay floor "
                            "(lowest most-probable-number rung the assay returns)",
            "replicate_handling": "one MPN series per isolate per visit; the "
                                  "deposit reports a single number per cell and "
                                  "no replicate structure is recoverable",
            "volumes_pooled": "not applicable; no plated volume is recorded "
                              "anywhere in the file",
            "evidence": (
                f"{scans['vijay']['deposit_matches']} matches for any limit term in "
                f"{scans['vijay']['deposit_strings_scanned']} strings in the workbook; "
                f"{vij['minimum_per_ml']:g} is the smallest of "
                f"{vij['n_readings']:,} readings, {vij['n_exactly_at_minimum']} sit "
                f"exactly on it and {vij['n_below_minimum']} lie below it; the "
                "per-visit minima are "
                + ", ".join(f"{k.split('_')[1]}={v:g}" for k, v in
                            list(vij["minimum_by_column"].items())[:3])
                + " for the 15-day panel, a factor of ten per visit; "
                f"{len(vij['mpn_rungs_below_the_minimum_that_never_appear'])} "
                "three-tube MPN rungs below it never appear"),
        },
        {
            "dataset": "ERA4TB 2023, six-laboratory ring trial",
            "source_states_lod": "no",
            "source_states_loq": "term only, no value: the BQL and AQL columns "
                                 "are named 'below/above quantification limit' "
                                 "and defined as countability of the plate",
            "value_used": "10, 100 and 400, per plated volume",
            "units": "CFU per mL",
            "how_obtained": "DERIVED",
            "correct_term": "minimum reportable positive count "
                            "(one colony in the volume plated)",
            "replicate_handling": (
                "the deposited count per mL is a single-plate count scaled by "
                "its own volume, so the four plates were not pooled into the "
                "reported number. Pooling would put the value on a 2.5 CFU/mL "
                "lattice, three rungs of which are not multiples of 10; "
                f"{era['pooling_test_100ul']['n_on_2_5_but_off_10']} of "
                f"{era['pooling_test_100ul']['n_readings']} quadruplicate 100 uL "
                "readings sit on one of those three rungs, where pooling would "
                "put about three in four. The evidence is carried by the "
                f"{era['pooling_test_100ul']['n_readings_below_100']} readings "
                "below 100, which take only multiples of 10 and bottom out at "
                f"{era['pooling_test_100ul']['smallest_reading']:g} rather than "
                "the 2.5 four pooled plates would allow; above 1,000 the "
                "deposit's two or three significant figures make every value a "
                "multiple of 10 whatever the arithmetic behind it"),
            "volumes_pooled": "no: each reading is judged against the floor its "
                              "own volume implies",
            "evidence": (
                f"{scans['era4tb']['deposit_matches']} matches for a limit term across "
                f"{scans['era4tb']['deposit_strings_scanned']} strings in the file and "
                "its readme, none carrying a value; smallest count at each volume "
                f"is exactly 1000/V ("
                + ", ".join(f"{v:g} uL -> {m:g}" for v, m in
                            sorted(era_min.items()) if v in (2.5, 10.0, 100.0))
                + f"); {era['n_counts_below_their_own_volume_floor']} of "
                f"{era['n_quantified_counts']} counts lie below their own floor and "
                f"{era['n_counts_exactly_on_their_own_volume_floor']} sit on it; a "
                "flask-visit carries up to "
                f"{max(era['distinct_floors_per_flask_visit'])} distinct floors "
                f"spanning {era['max_floor_spread_within_a_flask_visit_log10']:.1f} "
                "log10; the 1000/V derivation is exact for "
                + str(sum(r["n_counts"] - r["n_off_lattice"]
                          for r in era["by_volume_and_format"]
                          if r["plated_volume_ul"] == 10.0))
                + " of "
                + str(sum(r["n_counts"] for r in era["by_volume_and_format"]
                          if r["plated_volume_ul"] == 10.0))
                + " readings at 10 uL, the exceptions all from one laboratory"),
        },
        {
            "dataset": "Windels 2024, 126 evolved E. coli clones",
            "source_states_lod": "no",
            "source_states_loq": "no",
            "value_used": "none; no value is recoverable",
            "units": "surviving fraction, dimensionless",
            "how_obtained": "FLAGGED",
            "correct_term": "no floor is established; a below-limit reading is "
                            "written as exact zero and fixes no value",
            "replicate_handling": "three biological replicates per grid cell, "
                                  "reported separately and never pooled here",
            "volumes_pooled": "not applicable; the deposit reports relative "
                              "survival, not counts",
            "evidence": (
                f"{scans['windels']['deposit_matches']} matches for a limit term "
                f"in {scans['windels']['deposit_strings_scanned']} strings across "
                "the four deposited CSVs, which carry column names and numbers and "
                "no free text at all; "
                f"{win['n_below_limit_written_as_exact_zero']} of "
                f"{win['n_readings']} readings are exactly zero "
                f"({win['pct_below_limit']:.1f} per cent), affecting "
                f"{win['n_grid_cells_with_a_zero']} of {win['n_grid_cells']} "
                "grid cells; the lowest non-zero fraction is "
                f"{win['lowest_non_zero_surviving_fraction']:.3g}, an upper bound "
                "on the limit and not the limit"),
        },
        {
            "dataset": "Kaur 2024, apramycin concentration-by-time grid",
            "source_states_lod": "no",
            "source_states_loq": "no",
            "value_used": "none; no floor is used",
            "units": "log10 CFU per mL",
            "how_obtained": "NONE",
            "correct_term": "no floor is evidenced; the smallest reading is the "
                            "smallest reading",
            "replicate_handling": "three technical replicates of one preparation "
                                  "per cell, reported separately; they cannot "
                                  "estimate between-preparation reproducibility",
            "volumes_pooled": "not applicable; no plated volume is recorded",
            "evidence": (
                f"{scans['kaur']['deposit_matches']} matches for a limit term in "
                f"{scans['kaur']['deposit_strings_scanned']} strings in the "
                "workbook; this project's own provenance record for the deposit "
                "says separately that no limit of detection is given anywhere in "
                "it, which is not evidence about the source but does agree with "
                "the scan; the minimum "
                f"{kaur['minimum_per_ml']:g} per mL occurs "
                f"{kaur['n_exactly_at_minimum']} time in {kaur['n_readings']} "
                "readings, which is what a continuous tail looks like"),
        },
        {
            "dataset": "Dubey 2026, hollow-fibre E. coli (held out)",
            "source_states_lod": "no",
            "source_states_loq": "no. The plated volume from which L follows "
                                 "arithmetically is recorded in this project's "
                                 "staging record for the deposit, not found by "
                                 "the scan of the deposited file; the published "
                                 "Methods were not scanned here",
            "value_used": f"{dub['derived_floor_per_ml']:g}",
            "units": "CFU per mL",
            "how_obtained": "DERIVED",
            "correct_term": "minimum reportable positive count "
                            "(one colony in 100 uL)",
            "replicate_handling": "counts reported per culture; the below-limit "
                                  "placeholder is treated as censored at L and "
                                  "never as a count of one per mL",
            "volumes_pooled": "not applicable; one plated volume throughout",
            "evidence": (
                f"{scans['dubey']['deposit_matches']} matches for a limit term in "
                f"{scans['dubey']['deposit_strings_scanned']} strings in the "
                "source-data workbook; 100 uL plated with counts per mL comes "
                "from this project's staging record for the deposit and not from "
                "the deposited file, and the file agrees from the inside: "
                f"{dub['n_multiples_of_10']} of {dub['n_genuine_counts']} genuine "
                f"counts are multiples of 10 and the smallest is exactly "
                f"{dub['smallest_genuine_count']:g}. The corroboration rests on "
                f"the {dub['n_genuine_counts_below_100']} counts below 100, which "
                "run 10 to 80 in steps of ten; a count in the millions is a "
                "multiple of 10 whatever the plating was"),
        },
    ]
    return pd.DataFrame(rows)


# ------------------------------------------------- reconcile with docs/21 ---
# What docs/21_FLOOR_INFERENCE.md, generated by src.infer_floor, records for the
# three deposits it covers. Held here as numbers rather than prose so that if
# either module drifts the disagreement shows up in this experiment's output
# instead of in a referee's report.
DOC21 = {
    "Vijay clinical": {"verdict": "INFERRED", "n_readings": 1932,
                       "minimum": 23.0, "ties": 33, "below": 0},
    "ERA4TB 100 uL": {"verdict": "DERIVED", "n_readings": 533,
                      "minimum": 10.0, "ties": 4, "below": 0},
    "ERA4TB 10 uL": {"verdict": "DERIVED", "n_readings": 1068,
                     "minimum": 100.0, "ties": 31, "below": 0},
    "ERA4TB 2.5 uL": {"verdict": "DERIVED", "n_readings": 517,
                      "minimum": 400.0, "ties": 21, "below": 0},
    "Kaur apramycin": {"verdict": "NONE", "n_readings": 102,
                       "minimum": 40.0, "ties": 1, "below": 0},
}


def reconcile_with_doc21(vij: dict, d: pd.DataFrame, kaur: dict) -> list[dict]:
    """Recompute what docs/21 reports and say plainly where this differs.

    The brief for this experiment was to reconcile rather than contradict
    silently. There is one place where it goes further than docs/21 and it is
    worth stating: docs/21 labels the ERA4TB floors DERIVED without qualification,
    on the true observation that the smallest count at each volume is exactly
    1000/V. That test looks only at the minimum. Testing the whole lattice rather
    than its lowest rung finds 13 readings at 10 uL, all from one laboratory,
    that are not multiples of 1000/10 at all. The verdict does not change -- the
    floor is still derived from a recorded volume -- but it holds for 1,055 of
    1,068 readings at that volume rather than for all of them, and that is a
    refinement of docs/21, not a contradiction of it.
    """
    rows = []

    def add(name, n, mn, ties, below, verdict, note=""):
        want = DOC21[name]
        rows.append({
            "deposit": name, "docs21_verdict": want["verdict"],
            "exp29_verdict": verdict,
            "n_readings_docs21": want["n_readings"], "n_readings_exp29": n,
            "minimum_docs21": want["minimum"], "minimum_exp29": mn,
            "ties_docs21": want["ties"], "ties_exp29": ties,
            "below_docs21": want["below"], "below_exp29": below,
            "agrees": bool(want["verdict"] == verdict and
                           want["n_readings"] == n and
                           abs(want["minimum"] - mn) < 1e-9 and
                           want["ties"] == ties and want["below"] == below),
            "note": note,
        })

    add("Vijay clinical", vij["n_readings"], vij["minimum_per_ml"],
        vij["n_exactly_at_minimum"], vij["n_below_minimum"], "INFERRED")

    for vol, label in ((100.0, "ERA4TB 100 uL"), (10.0, "ERA4TB 10 uL"),
                       (2.5, "ERA4TB 2.5 uL")):
        s = d[(d["Volume"] == vol) & (d["BQL"] != 1) & (d["AQL"] != 1)]
        y = s["cfu"].dropna()
        step = 1000.0 / vol
        off = int((~np.isclose(y / step, np.round(y / step))).sum())
        add(label, int(len(y)), float(y.min()), int((y == y.min()).sum()),
            int((y < y.min()).sum()), "DERIVED",
            note=("derivation exact at the minimum and across the lattice"
                  if off == 0 else
                  f"exact at the minimum, but {off} readings are off the 1000/V "
                  "lattice; DERIVED holds for the rest"))

    k = pd.ExcelFile(KAUR).parse("Kill kinetics")
    num = k.iloc[:, 4:7].apply(pd.to_numeric, errors="coerce").to_numpy(float).ravel()
    v = 10.0 ** num[np.isfinite(num)]
    add("Kaur apramycin", int(len(v)), kaur["minimum_per_ml"],
        int((v == v.min()).sum()), int((v < v.min()).sum()), "NONE")
    return rows


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    scans = {
        # No SOURCES.json key exists for the clinical or the hollow-fibre
        # deposit; the lookup says so rather than silently scanning nothing.
        "vijay": scan_for_limit_terms([VIJAY], sources_key="vijay2024"),
        "era4tb": scan_for_limit_terms([ERA4TB, ERA4TB_README],
                                       sources_key="era4tb"),
        "windels": scan_for_limit_terms(sorted(WINDELS_DIR.glob("*.csv")),
                                        sources_key="windels2024"),
        "kaur": scan_for_limit_terms([KAUR], [KAUR_PROV],
                                     sources_key="apramycin_mtb"),
        "dubey": scan_for_limit_terms([DUBEY], [DUBEY_PROV],
                                      sources_key="dubey2026"),
    }

    vij = vijay_evidence()
    d = era4tb_load()
    era = era4tb_evidence(d)
    kaur = kaur_evidence()
    win = windels_evidence()
    dub, dub_sweep = dubey_evidence()

    recon = reconcile_with_doc21(vij, d, kaur)
    prov = provenance_table(scans, vij, era, kaur, win, dub)
    prov.to_csv(TABLES / "exp29_floor_provenance.csv", index=False)

    clin, clin_summ = sweep_clinical()
    era_sweep, era_summ = sweep_era4tb(d)
    kaur_sweep = sweep_kaur(kaur)

    # One tidy sensitivity table across the deposits, because the sweeps do not
    # share a set of columns and a wide table would be mostly empty.
    tidy = []
    for _, r in clin.iterrows():
        for k, v in r.items():
            if k in ("assumed_floor_per_ml", "assumed_floor_log10"):
                continue
            tidy.append({"dataset": "Vijay 2024, clinical isolates",
                         "scenario": f"floor = {r['assumed_floor_per_ml']:g} MPN/mL",
                         "floor_per_ml": r["assumed_floor_per_ml"],
                         "metric": k, "value": v})
    for _, r in era_sweep.iterrows():
        for k in ("n_genuine_counts_this_floor_would_discard",
                  "pct_genuine_counts_discarded",
                  "n_counts_sitting_exactly_on_the_floor",
                  "n_flags_checkable", "n_flags_with_a_comparator",
                  "n_flags_contradicted", "pct_flags_contradicted",
                  "pct_of_flags_with_a_comparator_contradicted"):
            tidy.append({"dataset": "ERA4TB, six laboratories",
                         "scenario": r["scheme"],
                         "floor_per_ml": r["floor_per_ml"],
                         "metric": k, "value": r[k]})
    for _, r in dub_sweep.iterrows():
        for k in ("median_headroom_log10", "n_short_of_4_logs", "n_cultures"):
            tidy.append({"dataset": "Dubey 2026, hollow fibre",
                         "scenario": r["corresponds_to"],
                         "floor_per_ml": r["assumed_floor_per_ml"],
                         "metric": k, "value": r[k]})
    for _, r in kaur_sweep.iterrows():
        for k in ("headroom_log10", "four_log_endpoint_reachable"):
            tidy.append({"dataset": "Kaur 2024, apramycin grid",
                         "scenario": r["corresponds_to"],
                         "floor_per_ml": r["assumed_floor_per_ml"],
                         "metric": k, "value": r[k]})
    tidy.append({"dataset": "Windels 2024, evolved clones",
                 "scenario": "no floor is recoverable",
                 "floor_per_ml": np.nan,
                 "metric": "n_below_limit_written_as_exact_zero",
                 "value": win["n_below_limit_written_as_exact_zero"]})
    tidy.append({"dataset": "Windels 2024, evolved clones",
                 "scenario": "upper bound only",
                 "floor_per_ml": np.nan,
                 "metric": "lowest_non_zero_surviving_fraction",
                 "value": win["lowest_non_zero_surviving_fraction"]})
    sens = pd.DataFrame(tidy)
    sens.to_csv(TABLES / "exp29_floor_sensitivity.csv", index=False)

    (RECEIPTS / "exp29_receipt.json").write_text(json.dumps({
        "script": "src/experiments/exp29_floor_provenance.py",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_sources": [
            "eLife 93243 supplementary file 2 (Vijay et al. 2024)",
            "figshare 19766083 (ERA4TB / van Wijk et al. 2023)",
            "Zenodo 7550302 (Windels et al. 2024)",
            "figshare 26462791 (Kaur et al. 2024)",
            "Nat Commun source data (Dubey et al. 2026)",
        ],
        "limit_term_scans": scans,
        "vijay_floor_evidence": vij,
        "era4tb_floor_evidence": era,
        "kaur_floor_evidence": kaur,
        "windels_floor_evidence": win,
        "dubey_floor_evidence": dub,
        "clinical_sweep": clin_summ,
        "era4tb_pooling_sweep": era_summ,
        "n_datasets_stating_a_loq_with_a_value": 0,
        "reconciles_with": "docs/21_FLOOR_INFERENCE.md",
        "reconciliation": recon,
    }, indent=2, default=str), encoding="utf-8")

    # ------------------------------------------------------------- report ---
    print("\n== 1. Does any source state a limit, with a value? ==")
    print("   (the deposit's own bytes only; this project's notes are counted "
          "separately)")
    for k, s in scans.items():
        print(f"   {k:9s} {s['deposit_matches']:2d} matches in "
              f"{s['deposit_strings_scanned']:5d} deposited strings, "
              f"{s['deposit_matches_stating_a_value']} of them beside a value  "
              f"[project notes: {s['project_record_matches']} matches in "
              f"{s['project_record_strings_scanned']} strings]")
        for m in s["deposit_hits"][:3]:
            print(f"             ! {m['text'][:92]}")
    print("   No deposit states a limit of quantification with a value. The ERA4TB")
    print("   readme names the concept in its BQL and AQL column definitions and")
    print("   defines it as whether the plate was countable, which is an operator")
    print("   judgement, not a validated limit.")

    print("\n== 2. What L is, per deposit ==")
    print(prov[["dataset", "value_used", "units", "how_obtained",
                "correct_term"]].to_string(index=False, max_colwidth=52))

    print("\n== 3. The six-laboratory deposit plates one flask-visit at several "
          "volumes ==")
    for r in era["by_volume_and_format"]:
        print(f"   {r['plated_volume_ul']:6.1f} uL  {r['plating_format']:<20s} "
              f"n={r['n_counts']:4d}  floor={r['implied_floor_per_ml']:6.1f}  "
              f"smallest={r['smallest_count_per_ml']:8.1f}  "
              f"on lattice {100 * r['fraction_on_the_1000_over_V_lattice']:5.1f}%"
              + (f"  ({r['n_off_lattice']} off, institutes "
                 f"{r['off_lattice_institutes']})" if r["n_off_lattice"] else ""))
    print(f"   distinct floors within one flask-visit: "
          f"{era['distinct_floors_per_flask_visit']} "
          f"(count of visits by number of distinct floors)")
    print(f"   widest floor spread inside one flask-visit: "
          f"{era['max_floor_spread_within_a_flask_visit_log10']:.2f} log10")
    print(f"   duplicate (Institute, Sample, Replicate, Volume, Time) keys: "
          f"{era['n_keys_with_more_than_one_row_without_condition']} of "
          f"{era['n_keys_without_condition']}; adding Condition leaves "
          f"{era['n_keys_with_more_than_one_row_with_condition']} of "
          f"{era['n_keys_with_condition']}. The duplication is 10 uL plated twice "
          "at one visit,")
    print("   as four drops and as a single drop, and is not an error.")
    print(f"   below-limit flags retain no count: "
          f"{era['n_bql_flags_that_retain_a_count']} of {era['n_bql_flags']} "
          "flagged rows carry a number, so the deposit deletes rather than "
          "censors.")
    ru = era["rows_whose_volume_field_is_unusable"]
    print(f"   rows whose Volume field its own Comments contradict: {ru['n']} "
          f"(the 50 uL line above). {ru['note']}")
    fr = era["flag_rate_denominators"]
    print(f"   flag rate needs its denominator: the same {fr['n_flags']} flags are "
          f"{fr['pct_flagged_below_over_all_rows']:.1f}% of the "
          f"{fr['all_rows_in_file']:,} rows in the file and "
          f"{fr['pct_flagged_below_over_analysis_set']:.1f}% of the "
          f"{fr['rows_in_the_exp17_analysis_set']:,}-row analysis set.")

    print("\n== 4. What pooling the volumes would cost ==")
    print(era_sweep.to_string(index=False, max_colwidth=44,
                              float_format=lambda v: f"{v:,.3g}"))
    print(f"   Two denominators for the flag audit. All "
          f"{era_summ['per_volume_flags_contradicted']} contradictions are found "
          f"among the {era_summ['per_volume_flags_with_a_comparator']} flags that "
          "have a companion plating at an")
    print(f"   at-least-as-sensitive limit, not among all "
          f"{int(era_sweep['n_below_limit_flags'].iloc[0])}: the rest sit in "
          "flask-visits with nothing to check them against and cannot be")
    print(f"   contradicted by construction. So the rate is "
          f"{era_summ['per_volume_pct_flags_contradicted']:.1f} per cent of every "
          f"flag and {era_summ['per_volume_pct_of_comparable_flags_contradicted']:.1f} "
          "per cent of the flags the deposit itself can be asked about.")
    pt = era["pooling_test_100ul"]
    print(f"   Were the four 100 uL plates pooled, the count would sit on a 2.5 "
          f"CFU/mL lattice; {pt['n_on_2_5_but_off_10']} of {pt['n_readings']} "
          "readings sit on one of its three")
    print(f"   non-multiple-of-ten rungs, where pooling would put about three in "
          f"four. The test bites on the {pt['n_readings_below_100']} readings "
          "below 100")
    print(f"   ({', '.join(f'{v:g}' for v in pt['distinct_values_below_100'])}) "
          f"and on the smallest reading, {pt['smallest_reading']:g} and not the "
          "2.5 pooling would allow;")
    print(f"   above 1,000 ({pt['n_readings'] - pt['n_readings_below_1000']} "
          "readings) two or three significant figures make every value a multiple "
          "of ten regardless.")

    print("\n== 5. The clinical floor swept over every MPN rung at or below 23 ==")
    show = ["assumed_floor_per_ml", "n_short_of_4_logs_15d",
            "n_short_of_4_logs_15d_baseline_only", "n_at_floor_15d",
            "n_determinable_15d", "n_forced_by_inoculum_15d", "n_undecidable_15d",
            "n_readings_on_those_rungs"]
    print(clin[show].to_string(index=False))
    print(f"   isolates short of four logs of headroom: "
          f"{clin_summ['n_short_of_4_logs_15d_range'][0]} to "
          f"{clin_summ['n_short_of_4_logs_15d_range'][1]} across the whole ladder, "
          f"{clin_summ['n_short_of_4_logs_15d_at_23']} at 23.")
    print("   The observability split collapses below 23 for an arithmetic reason,")
    print("   not a reassuring one: 23 is the smallest value in the file, so at any")
    print("   lower assumed floor nothing sits on it and every call is nominally")
    print("   determinable. The price of assuming one is that the "
          f"{clin_summ['mpn_rungs_from_3_up_to_but_excluding_23']} MPN rungs from")
    print(f"   3.0 up to 23 hold {clin_summ['readings_on_those_rungs']} readings "
          f"between them, while 23 itself holds "
          f"{clin_summ['readings_exactly_on_23']} of "
          f"{clin_summ['n_readings_total']:,}.")
    up = clin_summ["upward_counterfactual_not_in_the_ladder"]
    print(f"   The ladder stops at 23 because {up['excluded_because']}, so the "
          "28-to-33 stability above is")
    print("   stability in the only direction the deposit permits and should not "
          "be carried over to the other.")
    print(f"   For scale: at a floor of {up['assumed_floor_per_ml']:g} "
          f"({up['why_this_value']}) the count short of four logs")
    print(f"   would be {up['n_short_of_4_logs_15d']} rather than "
          f"{clin_summ['n_short_of_4_logs_15d_at_23']}, and the undecidable calls "
          f"{up['n_undecidable_15d']} rather than "
          f"{clin_summ['n_undecidable_15d_at_23']}.")
    tie = int(clin.loc[clin["assumed_floor_per_ml"] == MPN_FLOOR,
                       "n_at_floor_whose_bound_sits_exactly_on_a_class_cut_15d"]
              .iloc[0])
    print(f"   Of the {clin_summ['n_undecidable_15d_at_23']} undecidable calls at "
          f"23, {tie} are undecidable only because L/N0 lands exactly on the "
          "1e-3 class cut,")
    print("   where the deposit's own rule (Low below it, Medium at it) puts the "
          "two classes on either side of a single point.")

    print("\n== 6. The two deposits that cannot carry a floor ==")
    print(kaur_sweep.to_string(index=False, float_format=lambda v: f"{v:,.3g}"))
    swing = float(kaur_sweep["headroom_log10"].max() -
                  kaur_sweep["headroom_log10"].min())
    print(f"   Kaur: the deepest resolvable reduction swings {swing:.2f} log10 "
          "across the range a plating protocol could")
    print("   plausibly imply. A four-log endpoint stays reachable throughout, so "
          "that particular")
    print("   conclusion would survive; the depth h itself would not, and h is what "
          "Table 9 reports.")
    print("   The deposit states no floor, so none is used and the Kaur row of "
          "Table 9 stays NA.")
    print(f"   Windels: {win['n_below_limit_written_as_exact_zero']} readings are "
          f"exact zeros; the lowest non-zero fraction is "
          f"{win['lowest_non_zero_surviving_fraction']:.3g}, an upper bound and not "
          "a limit.")

    print("\n== 7. The held-out deposit, where the floor is derived and checked ==")
    print(dub_sweep.to_string(index=False, float_format=lambda v: f"{v:,.3g}"))
    print(f"   {dub['n_multiples_of_10']} of {dub['n_genuine_counts']} genuine "
          f"counts are multiples of 10 and the smallest is "
          f"{dub['smallest_genuine_count']:g}, so the plating protocol shows up in "
          "the data.")

    print("\n== 8. Reconciliation with docs/21_FLOOR_INFERENCE.md ==")
    r = pd.DataFrame(recon)
    print(r[["deposit", "docs21_verdict", "exp29_verdict", "n_readings_exp29",
             "minimum_exp29", "ties_exp29", "below_exp29", "agrees"]]
          .to_string(index=False))
    for row in recon:
        if row["note"]:
            print(f"   {row['deposit']}: {row['note']}")
    n_dis = sum(not x["agrees"] for x in recon)
    print(f"   {len(recon) - n_dis} of {len(recon)} deposits reproduce docs/21 "
          "exactly; this experiment adds the Windels and Dubey deposits, which")
    print("   docs/21 does not cover, and the terminology column, which it does "
          "not attempt.")

    print("\n   Wrote results/tables/exp29_floor_provenance.csv, "
          "results/tables/exp29_floor_sensitivity.csv, "
          "results/receipts/exp29_receipt.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
