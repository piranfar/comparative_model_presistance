"""
Run every dataset reader and assemble the corpus as one row per reading.

Run:  python -m src.build_corpus_long

Each reader lives in src/ingest/read_<STUDY_ID>.py and returns the schema in
src/ingest/__init__.py. This finds them, runs each against its own directory
under data/corpus/, validates what comes back, and concatenates.

A reader that raises is reported and skipped rather than stopping the build:
forty datasets should not be held hostage by one whose supplementary workbook
changed shape. What is NOT tolerated is a reader that returns rows failing the
schema -- a silently malformed frame would propagate into every model fitted on
it, so those abort.

Writes:
  data/processed/corpus_long.csv     one row per reading
  results/tables/corpus_coverage.csv what each dataset contributed, and what it
                                     could not supply
"""
from __future__ import annotations

import importlib
import pkgutil
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

from src.ingest import COLUMNS, SCHEMA, finish

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus"
OUT = ROOT / "data" / "processed" / "corpus_long.csv"
COVER = ROOT / "results" / "tables" / "corpus_coverage.csv"


def find_dir(study_id: str) -> Path | None:
    for base in ("open", "restricted"):
        d = CORPUS / base / study_id
        if d.is_dir():
            return d
    return None


def validate(df: pd.DataFrame, study_id: str) -> None:
    extra = [c for c in df.columns if c not in COLUMNS]
    if extra:
        raise ValueError(f"{study_id}: columns not in the schema: {extra}")
    for c, (t, _) in SCHEMA.items():
        if t == "float" and not pd.api.types.is_numeric_dtype(df[c]):
            raise ValueError(f"{study_id}: {c} should be numeric")
    bad = df.time_h.notna() & (df.time_h < 0)
    if bad.any():
        raise ValueError(f"{study_id}: {bad.sum()} rows with negative time")


def main() -> int:
    import src.ingest as pkg
    readers = sorted(m.name for m in pkgutil.iter_modules(pkg.__path__)
                     if m.name.startswith("read_"))
    if not readers:
        print("no readers yet under src/ingest/; nothing to assemble")
        return 0

    frames, cover, failed = [], [], []
    for mod_name in readers:
        study_id = mod_name[len("read_"):]
        d = find_dir(study_id)
        if d is None:
            failed.append((study_id, "no directory under data/corpus/"))
            continue
        try:
            mod = importlib.import_module(f"src.ingest.{mod_name}")
            df = finish(mod.read(d), study_id)
            validate(df, study_id)
        except Exception as exc:
            failed.append((study_id, f"{type(exc).__name__}: {exc}"))
            traceback.print_exc(limit=1)
            continue
        # Two ways a floor can be present, and they are different findings.
        # STATED means the depositor named a limit as a number and therefore
        # thought about it. DERIVED means nobody named one, but the plated
        # volume survives in the file and the floor follows by arithmetic --
        # the information is there by accident rather than by intent. Counting
        # them together, as an earlier version of this table did, turns "two
        # deposits report their detection limit" into "five do".
        stated = df.floor_basis.str.contains(
            r"stated in the sheet|LOD column|limit of detection\b.*\d",
            case=False, regex=True, na=False) & df.floor_cfu_per_ml.notna()
        derived = df.floor_cfu_per_ml.notna() & ~stated
        frames.append(df)
        cover.append({
            "floor_regime": ("stated by the source" if stated.any()
                             else "derived from a stated plated volume"
                             if derived.any() else "none"),
            "floor_stated_rows": int(stated.sum()),
            "floor_derived_rows": int(derived.sum()),
            "study_id": study_id,
            "rows": len(df),
            "series": df.groupby(["arm", "replicate"], dropna=False).ngroups,
            "timepoints": df.time_h.nunique(dropna=True),
            "has_time_zero": bool((df.time_h == 0).any()),
            "with_a_count": int(df.cfu_per_ml.notna().sum()),
            "with_a_floor": int(df.floor_cfu_per_ml.notna().sum()),
            "censored_rows": int((df.censored == "yes").sum()),
            "floor_unknown_rows": int((df.censored == "unknown").sum()),
            "organisms": "; ".join(sorted(set(df.organism) - {""}))[:60],
            "drugs": "; ".join(sorted(set(df.drug) - {""}))[:60],
        })

    if not frames:
        print(f"every reader failed ({len(failed)})")
        for s, why in failed:
            print(f"   {s:22} {why}")
        return 1

    long = pd.concat(frames, ignore_index=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    COVER.parent.mkdir(parents=True, exist_ok=True)
    long.to_csv(OUT, index=False)
    cv = pd.DataFrame(cover).sort_values("rows", ascending=False)
    cv.to_csv(COVER, index=False)

    print(f"{len(long):,} readings from {len(frames)} datasets -> "
          f"{OUT.relative_to(ROOT)}")
    print(cv[["study_id", "rows", "series", "timepoints", "with_a_count",
              "with_a_floor"]].to_string(index=False))

    n_stated = int((cv.floor_stated_rows > 0).sum())
    n_derived = int((cv.floor_derived_rows > 0).sum())
    print(f"\n   deposits that STATE a detection limit as a number : "
          f"{n_stated} of {len(cv)}  ({int(cv.floor_stated_rows.sum()):,} readings)")
    print(f"   deposits where it is DERIVABLE from a stated volume: "
          f"{n_derived} of {len(cv)}  ({int(cv.floor_derived_rows.sum()):,} readings)")
    print(f"   readings whose censoring cannot be decided from the file: "
          f"{int(cv.floor_unknown_rows.sum()):,} of {len(long):,} "
          f"({100*cv.floor_unknown_rows.sum()/len(long):.1f}%)")
    print("\n   whether that last number means anything depends on the papers, "
          "not the files:\n   a deposit whose article states the limit in its "
          "methods is a different case\n   from one where nobody recorded it at "
          "all. exp39 settles that.")
    if failed:
        print(f"\n   {len(failed)} reader(s) failed:")
        for s, why in failed:
            print(f"      {s:22} {why[:88]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
