"""
Retrieve the external sources this repository is not entitled to redistribute.

Run:  python -m src.fetch_external_data          # report what is missing
      python -m src.fetch_external_data --fetch  # download the openly hosted ones

WHY THIS EXISTS. Reproducibility and copyright pull in opposite directions here.
Every number this project reports should be traceable to the file it came from,
which argues for keeping those files. But several of the sources are free to read
and not free to redistribute: one is CC BY-NC-ND, one sits in an institutional
repository under a Dutch copyright exception that names the author rather than
any third party, and several are free in PubMed Central without an open-access
licence at all. Copying those into a public repository would breach the
publisher's terms even though the analysis itself is entirely legitimate.

The resolution is to keep the openly licensed bytes and record the rest by URL.
data/raw/SOURCES.json holds the registry with the licence for each. This script
reads it, reports what is present, and fetches what can be fetched.

WHAT IT WILL NOT DO. It will not defeat a paywall. Sources marked paywalled are
listed with what they are for and how to request them, and nothing more; two of
them are interlibrary loan requests and two are emails to authors, all set out in
docs/16_EXTERNAL_NEEDS_AUDIT.md. Fetching is limited to material the publisher
serves openly.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "raw" / "SOURCES.json"
CACHE = ROOT / "data" / "raw" / "_fetched"

UA = {"User-Agent": "antibiotic-resistance-model/1.0 (academic reuse; contact via repository)"}


def load() -> dict:
    if not REGISTRY.exists():
        raise SystemExit(f"missing {REGISTRY}")
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def fetch_one(key: str, url: str) -> tuple[bool, str]:
    CACHE.mkdir(parents=True, exist_ok=True)
    suffix = Path(url.split("?")[0]).suffix
    out = CACHE / f"{key}{suffix or '.html'}"
    if out.exists() and out.stat().st_size > 0:
        return True, f"already present, {out.stat().st_size:,} bytes"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        out.write_bytes(data)
        return True, f"fetched {len(data):,} bytes -> {out.relative_to(ROOT)}"
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        return False, f"could not fetch: {type(exc).__name__} {exc}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fetch", action="store_true",
                    help="download the openly hosted sources into data/raw/_fetched/")
    args = ap.parse_args()

    reg = load()
    held, external, blocked = [], [], []
    for s in reg["sources"]:
        if s.get("redistributable"):
            held.append(s)
        elif s.get("url") or s.get("data_url"):
            external.append(s)
        else:
            blocked.append(s)

    print(f"-- {len(held)} sources are openly licensed and kept in this repository --")
    for s in held:
        loc = ROOT / s["in_repo"]
        mark = "present" if loc.exists() else "MISSING"
        print(f"   {s['key']:<20} {s['licence']:<14} {mark:>8}  {s['in_repo']}")

    print(f"\n-- {len(external)} are free to read but not to redistribute --")
    for s in external:
        print(f"   {s['key']:<20} {s['licence']}")
        print(f"      {s.get('url') or s.get('data_url')}")
        if args.fetch:
            ok, msg = fetch_one(s["key"], s.get("data_url") or s["url"])
            print(f"      {'ok  ' if ok else 'fail'} {msg}")

    print(f"\n-- {len(blocked)} are paywalled and need a person, not a script --")
    for s in blocked:
        print(f"   {s['key']:<20} doi:{s.get('doi')}  PMID {s.get('pmid')}")
        note = (s.get("note") or "").strip()
        if note:
            print(f"      {note[:200]}")
    print("\n   Requests for these are set out in docs/16_EXTERNAL_NEEDS_AUDIT.md.")

    if not args.fetch:
        print("\nRun with --fetch to download the second group into data/raw/_fetched/,")
        print("which is untracked. Nothing in that group may be committed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
