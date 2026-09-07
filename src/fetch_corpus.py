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

NOTHING IS COMMITTED. The whole of data/corpus/ is ignored by git, whatever the
licence. What the repository carries instead is the manifest -- every dataset
with its URL, DOI and licence -- and this script, which rebuilds the corpus on
any machine from those links. The links are the deliverable; the bytes belong to
their depositors.

That decision removes a whole class of problem rather than managing it. No
licence question can turn into a publication question, no deposit's size can make
the repository painful to clone, and the awkward asymmetry disappears: taking a
file off a disk is instant, while taking it out of a public git history means
rewriting history and force-pushing over everyone who has the old copy.

The two directories remain, because the distinction is still worth seeing at a
glance:

  data/corpus/open/<study_id>/        CC BY or CC0 -- free to redistribute if we
                                      ever choose to
  data/corpus/restricted/<study_id>/  everything else -- analysed on the same
                                      terms, redistributed by nobody

EVERY DOWNLOAD IS RECORDED. Each directory gets a PROVENANCE.json with the URL,
the retrieval time, the SHA-256 of every file and the licence as recorded. That
is what makes a later licence question answerable instead of archaeological.
"""
from __future__ import annotations

import csv
import re
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

# None of the corpus is committed, so this is no longer about GitHub's 100 MB
# file limit -- it is about disk and about relevance. The largest things in these
# deposits are raw imaging and plate-reader dumps measured in gigabytes, and none
# of it is a count series. Anything above the cap is left unfetched with its URL
# recorded in the provenance, so a deliberate `--all` run or a manual download
# can still take it.
MAX_FILE_MB = 500

# A deposit is usually a whole paper's data, and most of it is not ours. One
# record here is a 197 MB snapshot of a software repository; another carries 96 MB
# of microscopy and membrane-potential imaging beside the 0.4 MB of time-kill
# curves that is the only part this project reads. Fetching by name keeps the
# corpus to what the analysis uses, which is also what makes it reviewable.
WANTED = re.compile(
    r"time.?kill|kill.?curve|killing|cfu|colony|colonies|viable|count|"
    r"survival|persist|toleran|mic|growth|od600|plate|raw.?data|source.?data|"
    r"supplement|dataset|data_s|\.csv$|\.tsv$", re.I)
UNWANTED = re.compile(
    r"microscop|image|imaging|movie|video|micrograph|tiff|\.czi|\.nd2|"
    r"flow.?cytom|facs|sequenc|fastq|genome|\.bam|\.sam|\.vcf|"
    r"membrane_potential|biosensor|renv\.lock|\.git", re.I)


def shippable(licence_class: str) -> bool:
    return SHIP_EVERYTHING or licence_class.strip() == "USE_OK_REDIST_OK"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def resolve(field: str) -> tuple[list[tuple[str, str]], str]:
    """Turn a manifest URL field into (filename, url) pairs to download.

    The field is prose as often as it is a link -- agents wrote things like
    "https://zenodo.org/records/123 (article: https://pmc...)" and
    "https://pmc.../PMC123/ ; file at https://static-content.springer.com/...".
    A record page is not a dataset: fetching zenodo.org/records/123 returns a
    web page. So each repository is resolved through its API to the actual
    files, and any explicit file URL written in the field is preferred over the
    landing page, because whoever wrote it had already found the file.

    Returns (files, note). An empty list with a note is the honest outcome when
    a repository cannot be resolved -- Dryad currently answers its download
    endpoint with a bot interstitial, so those are recorded, not faked.
    """
    urls = re.findall(r"https?://[^\s,;)\]]+", field or "")
    if not urls:
        return [], "no URL in the manifest row"

    # An explicit file URL beats a landing page.
    direct = [u for u in urls
              if re.search(r"\.(csv|tsv|xlsx?|zip|txt|json|dat)(\?|$)", u, re.I)
              or "static-content.springer.com" in u
              or "ndownloader.figshare.com" in u
              or "/api/access/datafile/" in u]
    if direct:
        return [(u.rstrip("/").split("/")[-1].split("?")[0] or "download", u)
                for u in direct[:6]], "explicit file URL from the manifest"

    for u in urls:
        try:
            if "zenodo.org" in u and (m := re.search(r"/records?/(\d+)", u)):
                rec = _json(f"https://zenodo.org/api/records/{m.group(1)}")
                fs = [(f.get("key") or "file", f["links"]["self"])
                      for f in rec.get("files", []) if f.get("links")]
                if fs:
                    return fs[:12], "Zenodo API"
            if "figshare.com" in u and (m := re.search(r"/(\d{6,})", u)):
                rec = _json(f"https://api.figshare.com/v2/articles/{m.group(1)}")
                fs = [(f["name"], f["download_url"]) for f in rec.get("files", [])]
                if fs:
                    return fs[:12], "figshare API"
            if "dataverse.no" in u and (m := re.search(r"doi:([^\s&]+)", u)):
                rec = _json("https://dataverse.no/api/datasets/:persistentId/"
                            f"?persistentId=doi:{m.group(1)}")
                fs = [(f["dataFile"]["filename"],
                       "https://dataverse.no/api/access/datafile/"
                       f"{f['dataFile']['id']}")
                      for f in rec["data"]["latestVersion"]["files"]]
                if fs:
                    return fs[:12], "DataverseNO API"
            if "datadryad.org" in u:
                return [], ("Dryad answers its download endpoint with a bot "
                            "interstitial; fetch by hand from the record page")
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError,
                ValueError, TimeoutError, OSError) as exc:
            return [], f"resolver failed: {type(exc).__name__}: {exc}"

    return [], ("only a landing page in the manifest; no file URL and no API "
                "route for this host")


def choose(files: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], list[str]]:
    """Keep the files the analysis reads; report what was left and why.

    A deposit with one file is taken whole -- there is nothing to choose between,
    and guessing from a single name risks discarding the only data there is.
    """
    if len(files) <= 1:
        return files, []
    keep, dropped = [], []
    for name, url in files:
        if UNWANTED.search(name):
            dropped.append(f"{name} (not a count series)")
        elif WANTED.search(name):
            keep.append((name, url))
        else:
            dropped.append(f"{name} (name matches nothing the analysis reads)")
    # If the filter rejected everything, it is the filter that is wrong, not the
    # deposit; take it all rather than silently returning an empty dataset.
    return (keep, dropped) if keep else (files, [])


def download(url: str, dest: Path) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            size = r.headers.get("Content-Length")
            if size and int(size) > MAX_FILE_MB * 1_000_000:
                return False, (f"{int(size)/1e6:.0f} MB exceeds the {MAX_FILE_MB} MB "
                               f"cap; not fetched, URL recorded")
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
        print("\n   the whole corpus is local: data/corpus/ is gitignored, and "
              "the manifest\n   is what travels. Any clone rebuilds this from "
              "the links in it.")
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
        files, note = resolve(url)
        if not files:
            skipped += 1
            print(f"   -- {sid:20} {note}")
            continue
        if dry:
            print(f"   would fetch {sid:20} {len(files)} file(s) via {note} "
                  f"-> {base.name}/")
            continue
        files, dropped = choose(files)
        for msg in dropped:
            print(f"      skipped {msg}")
        log, okc = [], 0
        for name, furl in files:
            name = re.sub(r"[^\w.\-]+", "_", name)[:120] or "download"
            okd, msg = download(furl, d / name)
            log.append((furl, msg))
            okc += okd
            if not okd:
                print(f"      ! {name}: {msg}")
        if okc:
            got += 1
            provenance(d, row, log)
            print(f"   got {sid:20} {okc}/{len(files)} file(s) via {note} "
                  f"-> {base.name}/")
        else:
            failed += 1
            print(f"   !! {sid:20} every file failed ({note})")

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
