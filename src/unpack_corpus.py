"""
Unpack the corpus: open archives, name the nameless, list what is really there.

Run:  python -m src.unpack_corpus

WHY THIS IS ITS OWN STEP. A third of what came down is a zip -- Europe PMC hands
back every supplementary file of an article as one archive, and several deposits
ship one too. Three more files arrived with no extension at all, because figshare
serves them by numeric id and the download carried no filename. Until those are
opened and identified, a survey of the corpus is a survey of its packaging.

WHAT IT DOES. Extracts each archive into a _unpacked/ directory beside it,
skipping the members no analysis here reads -- the same name filter the fetcher
uses, because a supplementary zip is mostly figures and PDFs. Sniffs the magic
bytes of any extensionless file and renames it to what it actually is. Then
prints one line per dataset saying what tabular material it now holds.

IT DOES NOT INTERPRET ANYTHING. Deciding which column is a colony count is the
next step and a different kind of work; this one only makes the files legible.
"""
from __future__ import annotations

import pathlib
import zipfile

from src.fetch_corpus import UNWANTED, WANTED

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus"

MAGIC = [
    (b"PK\x03\x04", ".zip"),          # also xlsx/docx, disambiguated below
    (b"\xd0\xcf\x11\xe0", ".xls"),    # OLE2: legacy Excel or Word
    (b"%PDF", ".pdf"),
    (b"\x89PNG", ".png"),
    (b"\xff\xd8\xff", ".jpg"),
    (b"II*\x00", ".tif"),
    (b"MM\x00*", ".tif"),
]
TABULAR = {".csv", ".tsv", ".xlsx", ".xls", ".txt", ".dat", ".json"}


def sniff(p: pathlib.Path) -> str:
    head = p.read_bytes()[:8]
    for magic, ext in MAGIC:
        if head.startswith(magic):
            if ext == ".zip":
                # xlsx and docx are zips; look inside for the giveaway member
                try:
                    with zipfile.ZipFile(p) as z:
                        names = z.namelist()
                    if any(n.startswith("xl/") for n in names):
                        return ".xlsx"
                    if any(n.startswith("word/") for n in names):
                        return ".docx"
                except zipfile.BadZipFile:
                    return ".bin"
            return ext
    txt = head.decode("utf-8", "ignore")
    if txt and all(c.isprintable() or c in "\r\n\t" for c in txt):
        return ".csv"
    return ".bin"


def unpack(z: pathlib.Path) -> tuple[int, int]:
    out = z.parent / "_unpacked" / z.stem
    taken = skipped = 0
    try:
        with zipfile.ZipFile(z) as arc:
            for m in arc.infolist():
                if m.is_dir():
                    continue
                name = pathlib.PurePosixPath(m.filename).name
                if not name or name.startswith("."):
                    continue
                ext = pathlib.PurePosixPath(name).suffix.lower()
                if UNWANTED.search(m.filename) or (
                        ext not in TABULAR and not WANTED.search(name)):
                    skipped += 1
                    continue
                out.mkdir(parents=True, exist_ok=True)
                dest = out / name
                if not dest.exists():
                    dest.write_bytes(arc.read(m))
                taken += 1
    except zipfile.BadZipFile:
        return 0, 0
    return taken, skipped


def main() -> int:
    renamed = opened = 0
    print("naming the files that arrived without an extension:")
    for p in sorted(CORPUS.rglob("*")):
        if p.is_file() and not p.suffix and p.name != "PROVENANCE.json":
            ext = sniff(p)
            new = p.with_suffix(ext)
            if not new.exists():
                p.rename(new)
                renamed += 1
                print(f"   {p.parent.name}/{p.name} -> {new.name}")

    print("\nopening archives:")
    for z in sorted(CORPUS.rglob("*.zip")):
        if "_unpacked" in z.parts:
            continue
        took, skip = unpack(z)
        if took:
            opened += 1
            print(f"   {z.parent.name:22} {z.name[:38]:40} {took} kept, {skip} skipped")

    print("\nwhat each dataset now holds:")
    total = 0
    for base in ("open", "restricted"):
        for d in sorted((CORPUS / base).glob("*")):
            if not d.is_dir():
                continue
            tab = [f for f in d.rglob("*")
                   if f.is_file() and f.suffix.lower() in TABULAR
                   and f.name != "PROVENANCE.json"]
            if tab:
                total += 1
                kinds = ", ".join(sorted({f.suffix.lower() for f in tab}))
                print(f"   {d.name:22} {len(tab):3d} tabular file(s)  {kinds}")
            else:
                print(f"   {d.name:22}   -- nothing tabular found")
    print(f"\n{renamed} renamed, {opened} archives opened, "
          f"{total} datasets with tabular material")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
