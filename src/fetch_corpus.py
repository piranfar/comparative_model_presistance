"""
Fetch every dataset in the corpus manifest, whatever its licence.

Run:  python -m src.fetch_corpus            # download what is missing
      python -m src.fetch_corpus --dry-run  # show what would happen
      python -m src.fetch_corpus --report   # what is held, and what may be shipped

EVERYTHING IS FETCHED. A restricted licence is not a reason to leave a dataset
out of the analysis: reading published numbers and drawing conclusions from them
is ordinary scholarship, and in most jurisdictions measurements are facts rather
than protected expression. So every row with a URL is downloaded and every
downloaded dataset is available to the pipeline. Nothing here gates the science.

WHAT IS GATED IS GIT, AND ONLY GIT. Files land in one of two directories:

  data/corpus/open/<study_id>/        CC BY or CC0 -- tracked, shipped, cited
  data/corpus/restricted/<study_id>/  everything else -- on disk, used by the
                                      pipeline, ignored by git

The split exists because of an asymmetry that is easy to miss. Taking a file off
a disk is instant. Taking it out of a public git history is not: it survives in
every clone, every fork and every cache, and removing it means rewriting history
and force-pushing over everyone who has the old copy. So "we will sort the
licences out later" stays true for the restricted directory and stops being true
the moment those bytes are committed.

MOVING THEM IN. When a permission arrives, record it in
data/manifests/permissions.csv, set the row's licence_class to USE_OK_REDIST_OK
in the manifest, and re-run: the file moves to open/ and becomes shippable. To
move everything in at once regardless -- an author's call, not this script's --
set SHIP_EVERYTHING below to True and re-run. One line, and the .gitignore rule
is written to match.

EVERY DOWNLOAD IS RECORDED. Each directory gets a PROVENANCE.json with the URL,
the retrieval time, the SHA-256 of every file and the licence as recorded. That
is what makes a later licence question answerable instead of archaeological.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifests" / "corpus.csv"
CORPUS = ROOT / "data" / "corpus"
OPEN_DIR = CORPUS / "open"
REST_DIR = CORPUS / "restricted"

# The author's switch. False keeps restricted bytes out of git while still
# fetching and using them. True puts everything under data/corpus/open/, which
# is tracked -- do that only with the permissions in hand, or deliberately.
SHIP_EVERYTHING = False

UA = ("Mozilla/5.0 (research corpus builder; contact vahab.p@gmail.com) "
      "python-urllib")
TIMEOUT = 60


def shippable(licence_class: str) -> bool:
    return SHIP_EVERYTHING or licence_class.strip() == "USE_OK_REDIST_OK"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            OSError, ValueError) as exc:
        return False, f"{type(exc).__name__}: {exc}"
    if not data:
        return False, "empty response"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return True, f"{len(data):,} bytes"


def provenance(d: Path, row: dict, results: list[tuple[str, str]]) -> None:
    files = [p for p in sorted(d.iterdir()) if p.name != "PROVENANCE.json"]
    (d / "PROVENANCE.json").write_text(json.dumps({
        "study_id": row.get("study_id", ""),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "record_url": row.get("record_url") or row.get("url", ""),
        "doi_or_accession": row.get("doi_or_accession") or row.get("doi", ""),
        "article": row.get("article", ""),
        "licence": row.get("licence", ""),
        "licence_class": row.get("licence_class", ""),
        "redistributable": row.get("redistributable", ""),
        "shipped_in_repository": shippable(row.get("licence_class", "")),
        "files": [{"name": p.name, "bytes": p.stat().st_size,
                   "sha256": sha256(p)} for p in files],
        "download_log": [{"url": u, "result": r} for u, r in results],
        "note": ("Third-party data, not generated here and not relicensed here. "
                 "Attribute to the depositor under the licence recorded above."),
    }, indent=2), encoding="utf-8")


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    report_only = "--report" in argv
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}; run src/build_corpus_manifest.py")
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig")))

    if report_only:
        held = {"open": [], "restricted": []}
        for base, key in ((OPEN_DIR, "open"), (REST_DIR, "restricted")):
            if base.exists():
                held[key] = [p.name for p in sorted(base.iterdir()) if p.is_dir()]
        print(f"corpus on disk: {len(held['open'])} open, "
              f"{len(held['restricted'])} restricted")
        for k in ("open", "restricted"):
            for n in held[k]:
                print(f"   {k:11} {n}")
        print(f"\nSHIP_EVERYTHING = {SHIP_EVERYTHING}")
        print("   restricted datasets are used by the pipeline and ignored by git"
              if not SHIP_EVERYTHING else
              "   EVERYTHING is being placed in the tracked directory")
        return 0

    got = skipped = failed = 0
    for row in rows:
        sid = (row.get("study_id") or "").strip()
        url = (row.get("record_url") or row.get("url") or "").strip()
        cls = (row.get("licence_class") or "").strip()
        if not sid:
            continue
        base = OPEN_DIR if shippable(cls) else REST_DIR
        d = base / sid
        if not url:
            skipped += 1
            print(f"   -- {sid:20} no URL recorded; needs one before it can be "
                  f"fetched ({row.get('acquisition') or 'source unknown'})")
            continue
        if d.exists() and any(p.name != "PROVENANCE.json" for p in d.iterdir()):
            skipped += 1
            print(f"   ok {sid:20} already held in {base.name}/")
            continue
        if dry:
            print(f"   would fetch {sid:20} -> {base.name}/  {url[:60]}")
            continue
        name = url.rstrip("/").split("/")[-1] or "download"
        okd, msg = download(url, d / name)
        if okd:
            got += 1
            provenance(d, row, [(url, msg)])
            print(f"   got {sid:20} -> {base.name}/{name}  ({msg})")
        else:
            failed += 1
            print(f"   !! {sid:20} {msg}")

    print(f"\n{got} fetched, {skipped} already held or without a URL, {failed} failed")
    n_open = len([p for p in OPEN_DIR.iterdir() if p.is_dir()]) if OPEN_DIR.exists() else 0
    n_rest = len([p for p in REST_DIR.iterdir() if p.is_dir()]) if REST_DIR.exists() else 0
    print(f"   data/corpus/open/       {n_open} datasets, tracked and shippable")
    print(f"   data/corpus/restricted/ {n_rest} datasets, used by the pipeline, "
          f"not in git")
    if n_rest and not SHIP_EVERYTHING:
        print("   to ship those too, set SHIP_EVERYTHING = True and re-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
