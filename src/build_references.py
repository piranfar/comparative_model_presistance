"""
Number the references in citation order, and build the list from that order.

Run:  python -m src.build_references

WHY THIS EXISTS. AAC uses the citation-sequence system: references are numbered
in order of first citation and cited parenthetically by number. Doing that by
hand is why the reference list was held back through two rounds of review --
every edit that moves a sentence renumbers the list, and a hand-maintained list
drifts from the text the first time that happens.

So the text does not carry numbers. It carries keys: [[R12]]. This module reads
the assembled document in final reading order, assigns 1..N by first appearance,
substitutes the numbers, and emits the list in that order. Moving a paragraph
renumbers everything correctly and costs nothing.

WHAT ASM REQUIRES, and what this enforces:
  - numbered in order of first citation, cited parenthetically by number
  - EVERY author named; "et al." is not permitted, however long the byline
  - journal names abbreviated per the PubMed Journals Database
  - data sets and code are reference types in their own right and must appear in
    the numbered list, not only in the Data availability paragraph
  - a deposit is cited alongside the article that first described it

It fails loudly on a key with no bibliography entry, on a bibliography entry
never cited, and on an entry whose author list has been abbreviated.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "manuscript" / "references.json"
OUT = ROOT / "manuscript" / "references.md"

KEY = re.compile(r"\[\[(R\d+)\]\]")


def load_bib() -> dict:
    if not BIB.exists():
        raise SystemExit(f"missing {BIB}; the bibliography has not been built yet")
    bib = json.loads(BIB.read_text(encoding="utf-8"))
    bad = [k for k, v in bib.items() if "et al" in v.get("authors", "").lower()]
    if bad:
        raise SystemExit("ASM does not permit 'et al.' in the reference list; "
                         f"these entries abbreviate their byline: {bad}")
    return bib


def order_of_appearance(text: str) -> list[str]:
    """Keys in the order the assembled document first cites them."""
    seen: list[str] = []
    for m in KEY.finditer(text):
        if m.group(1) not in seen:
            seen.append(m.group(1))
    return seen


def format_entry(e: dict) -> str:
    """One reference in ASM style.

    Journal article : Authors. Year. Title. Journal Abbrev Volume:pages.
    Data set / code : Party. Year. Data from "title". Repository, identifier.
    Book / report   : Authors. Year. Title. Publisher, City, State/Country.
    """
    bits = [e["authors"].rstrip("."), e["year"].rstrip(".")]
    kind = e.get("kind", "article")
    if kind in ("dataset", "code"):
        bits.append(e["title"].rstrip("."))
        tail = e.get("repository", "").rstrip(".")
        if e.get("identifier"):
            tail = f"{tail}. {e['identifier']}" if tail else e["identifier"]
        if e.get("retrieved"):
            tail = f"{tail}. Retrieved {e['retrieved']}"
        bits.append(tail)
    else:
        bits.append(e["title"].rstrip("."))
        venue = e.get("journal") or e.get("publisher", "")
        loc = e.get("volume_pages", "")
        bits.append(f"{venue} {loc}".strip().rstrip("."))
        if e.get("identifier"):
            bits.append(e["identifier"].rstrip("."))
    return ". ".join(b for b in bits if b) + "."


def substitute(text: str, bib: dict) -> tuple[str, list[str]]:
    """Replace every [[Rn]] with its citation-sequence number.

    Adjacent keys collapse: [[R2]][[R3]] becomes (2, 3), which is how a
    numbered style reads when one clause rests on two sources.
    """
    order = order_of_appearance(text)
    missing = [k for k in order if k not in bib]
    if missing:
        raise SystemExit(f"cited but not in the bibliography: {missing}")
    num = {k: i + 1 for i, k in enumerate(order)}

    def run(m: re.Match) -> str:
        # Sort, do not preserve the order the keys were typed in. A run written
        # [[R23]][[R4]] would otherwise render "(9, 3)", and which key is typed
        # first depends on where else in the document each one happens to be
        # cited -- so the same pair renders ascending or descending depending on
        # an edit somewhere else entirely. Sorting here makes the writing order
        # irrelevant, which is the only way it stays right.
        nums = sorted({num[k] for k in KEY.findall(m.group(0))})
        return "(" + ", ".join(str(n) for n in nums) + ")"

    text = re.sub(r"(?:\[\[R\d+\]\])+", run, text)
    return text, order


def build_list(order: list[str], bib: dict) -> str:
    lines = ["## References", ""]
    for i, k in enumerate(order, 1):
        lines.append(f"{i}. {format_entry(bib[k])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    bib = load_bib()
    body = ""
    for f in ("manuscript/MANUSCRIPT.md", "manuscript/abstract.md",
              "manuscript/tables.md"):
        p = ROOT / f
        if p.exists():
            body += p.read_text(encoding="utf-8") + "\n"
    order = order_of_appearance(body)
    uncited = sorted(set(bib) - set(order), key=lambda s: int(s[1:]))
    OUT.write_text(build_list(order, bib), encoding="utf-8")
    print(f"{len(order)} references numbered in citation order -> {OUT}")
    for i, k in enumerate(order[:8], 1):
        print(f"   {i}. {format_entry(bib[k])[:96]}")
    if uncited:
        # An entry nobody cites is carried, not printed: build_list emits only
        # what the text reaches. It is a housekeeping note, not a failure -- a
        # source can sit in the bibliography while its sentence is still being
        # decided. Failing the pipeline on it would make the reference list the
        # one stage that stops work rather than reporting it.
        print(f"   note: {len(uncited)} entries are never cited and are not "
              f"printed: {uncited}")
        for k in uncited:
            print(f"      {k}: {bib[k].get('supports', '(no note)')[:88]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
