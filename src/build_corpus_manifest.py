"""
The corpus manifest: every candidate dataset, whatever its licence.

Run:  python -m src.build_corpus_manifest

WHY EVERYTHING GOES IN. A dataset we may not redistribute is still a dataset we
may analyse, and the ones we cannot use at all are worth recording so that nobody
searches for them twice. Leaving restricted material out of the manifest does not
make the corpus cleaner; it makes it look complete when it is not, and it hides
the one number a survey of reporting practice would want -- how much of this
literature is reachable at all.

So the manifest carries every candidate, and a separate column says what may be
done with each. That column, not the presence of a row, is what governs the
public repository.

THE DISTINCTION THE LICENCE COLUMN ENCODES. Analysing published numbers and
publishing conclusions is ordinary scholarship, and in most jurisdictions the
measurements are facts rather than protected expression. What licences restrict
is REDISTRIBUTION -- putting somebody's bytes, or a tidied derivative of them,
into a public repository. Those are different acts and the manifest keeps them
apart:

  USE_OK_REDIST_OK      CC BY or CC0. Analyse and redistribute, with attribution.
  USE_OK_REDIST_NO      NC into a CC BY repository, or ND at all. Analyse freely;
                        keep the bytes out and record the fetch route. Ask for a
                        one-off permission if the dataset is worth it.
  USE_OK_FACTS_ONLY     No licence, or paywalled. The numbers may still be
                        extractable as facts; the document is not ours to carry.
  ASK_FIRST             Licence unclear, or the deposit has conditions we have
                        not read. Nothing goes in until somebody looks.
  BLOCKED               A term we cannot satisfy, or a refusal on record.

WHAT THIS SCRIPT DOES. It reads the existing manifest, adds the columns the
corpus needs, classifies each row's licence, and writes a permissions tracker
seeded with every row that needs a letter. It does not invent a dataset and it
does not change a licence: an UNKNOWN licence stays UNKNOWN and lands in
ASK_FIRST, which is the honest place for it.

Writes:
  data/manifests/corpus.csv
  data/manifests/permissions.csv   (created once, then appended to by hand)
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifests" / "datasets.csv"
CORPUS = ROOT / "data" / "manifests" / "corpus.csv"
PERMS = ROOT / "data" / "manifests" / "permissions.csv"

EXTRA = [
    "repository", "record_url", "licence", "licence_class", "redistributable",
    "has_time_series", "has_starting_density", "has_floor_or_volume",
    "headroom_computable", "n_series", "acquisition", "permission_status",
    "notes",
]

PERM_COLS = [
    "study_id", "contact_name", "contact_email", "letter", "sent_date",
    "reply_date", "outcome", "scope_granted", "evidence_file", "notes",
]


def classify(licence: str) -> tuple[str, str]:
    """(licence_class, redistributable) from the licence string.

    Deliberately conservative: anything not recognised as an open licence lands
    in ASK_FIRST rather than being waved through. A false 'yes' here puts
    somebody else's bytes in a public repository.
    """
    l = (licence or "").strip().upper()
    if not l or l in {"UNKNOWN", "NOT_STATED", "UNVERIFIED", "NONE STATED", "?"}:
        return "ASK_FIRST", "no"
    if "CC0" in l or "PUBLIC DOMAIN" in l:
        return "USE_OK_REDIST_OK", "yes"
    if re.search(r"CC[ -]?BY", l) and not re.search(r"\bNC\b|\bND\b", l):
        return "USE_OK_REDIST_OK", "yes"
    if re.search(r"\bND\b", l):
        # NoDerivatives blocks the tidied copy, which is the thing we would ship
        return "USE_OK_REDIST_NO", "no"
    if re.search(r"\bNC\b", l):
        return "USE_OK_REDIST_NO", "no"
    if any(k in l for k in ("PAYWALL", "SUBSCRIPTION", "ALL RIGHTS RESERVED",
                            "NO OPEN", "FREE TO READ", "TAVERNE", "25FA")):
        return "USE_OK_FACTS_ONLY", "no"
    return "ASK_FIRST", "no"


def headroom_flag(n0: str, lod: str) -> str:
    def known(x):
        return bool(x) and str(x).strip().upper() not in {
            "", "UNKNOWN", "NOT_STATED", "UNVERIFIED", "NA", "NONE"}
    if known(n0) and known(lod):
        return "yes"
    if known(n0) and not known(lod):
        return "no: floor not reported"
    if not known(n0) and known(lod):
        return "no: starting density not reported"
    return "no: neither reported"


def main() -> int:
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}")
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig")))
    cols = list(rows[0].keys()) if rows else []
    out_cols = cols + [c for c in EXTRA if c not in cols]

    # MERGE, do not overwrite. datasets.csv is the hand-curated seed; corpus.csv
    # also accumulates datasets found by search and entered directly, and those
    # have no row upstream to regenerate them from. An earlier version of this
    # script rebuilt corpus.csv from the seed alone and silently destroyed
    # fifty-two of them on its next run.
    carried = 0
    if CORPUS.exists():
        seed_ids = {r.get("study_id", "") for r in rows}
        for r in csv.DictReader(CORPUS.open(encoding="utf-8-sig")):
            if r.get("study_id") and r["study_id"] not in seed_ids:
                rows.append(r)
                carried += 1
        for c in out_cols:
            for r in rows:
                r.setdefault(c, "")

    # The licences are already recorded, in a different file. data/raw/SOURCES.json
    # carries a licence and a redistributable flag per source key; the manifest
    # carries study_ids like DRUSANO2018 against keys like drusano2018. Matching
    # them is worth doing rather than sending letters asking for what we already
    # know -- and it is the only place several of these licences exist.
    known: dict[str, str] = {}
    src = ROOT / "data" / "raw" / "SOURCES.json"
    if src.exists():
        import json
        for s in json.loads(src.read_text(encoding="utf-8")).get("sources", []):
            key = re.sub(r"[^a-z0-9]", "", (s.get("key") or "").lower())
            lic = s.get("licence") or s.get("license") or ""
            if key and lic:
                known[key] = lic

    matched = 0
    needs_letter = []
    for r in rows:
        sid = re.sub(r"[^a-z0-9]", "", (r.get("study_id") or "").lower())
        from_sources = known.get(sid, "")
        if from_sources:
            matched += 1
        r.setdefault("licence", from_sources or r.get("data_availability") or "")
        if from_sources:
            r["licence"] = from_sources
        cls, redist = classify(r.get("licence", ""))
        r["licence_class"] = cls
        r["redistributable"] = redist
        r["headroom_computable"] = headroom_flag(r.get("inoculum_cfu_ml", ""),
                                                 r.get("LOD_cfu_ml", ""))
        r.setdefault("acquisition", r.get("data_source", ""))
        r.setdefault("permission_status", "not requested")
        for c in EXTRA:
            r.setdefault(c, "")
        # A letter is worth sending when the data is not machine-readable, or
        # when we hold bytes we may not redistribute.
        digitised = "digitis" in (r.get("data_source") or "").lower() or \
                    "digitiz" in (r.get("data_source") or "").lower()
        if digitised or cls in {"USE_OK_REDIST_NO", "ASK_FIRST"}:
            needs_letter.append((r["study_id"],
                                 "A" if digitised else "B",
                                 cls, r.get("licence", "")))

    with CORPUS.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=out_cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in out_cols})

    if not PERMS.exists():
        with PERMS.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=PERM_COLS)
            w.writeheader()
            for sid, letter, cls, lic in needs_letter:
                w.writerow({"study_id": sid, "letter": letter,
                            "outcome": "not sent",
                            "notes": f"{cls}; licence as recorded: {lic or 'none'}"})
        made = f"created with {len(needs_letter)} rows"
    else:
        made = "left alone (already exists; append by hand)"

    print(f"wrote {CORPUS.relative_to(ROOT)}  ({len(rows)} datasets)")
    print(f"   licences recovered from SOURCES.json: {matched}")
    print(f"   carried forward from the existing corpus: {carried}")
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["licence_class"]] = counts.get(r["licence_class"], 0) + 1
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"   {k:22} {v}")
    hk = sum(1 for r in rows if r["headroom_computable"] == "yes")
    print(f"\n   headroom computable from what is reported: {hk} of {len(rows)}")
    print(f"   {PERMS.relative_to(ROOT)}: {made}")
    print(f"   letters worth sending: "
          f"{sum(1 for x in needs_letter if x[1] == 'A')} asking for data (A), "
          f"{sum(1 for x in needs_letter if x[1] == 'B')} asking to redistribute (B)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
