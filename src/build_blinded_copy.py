"""
Write the whole paper with everything that identifies it replaced by a label.

Run:  python -m src.build_blinded_copy

Reads manuscript/PAPER_COMPLETE.md and writes manuscript/BLINDED_COPY.md, plus
manuscript/BLINDED_COPY_KEY.md, which is the decoder and MUST NOT be sent
anywhere the blinded copy is going.

THE RULE THAT SHAPES ALL OF THIS. A blinded copy is worth nothing if the
argument does not survive it. Masking every drug name to one token would collapse
"tolerance to drug A" and "resistance to drug B" into the same string and destroy
the paper's central distinction, so each entity gets its OWN label: DRUG-A,
DRUG-B, STRAIN-1, GENE-1. The reader loses the identity and keeps the logic.

WHAT IS MASKED
  organism    every word built on the two stems, the binomial in any form, and
              the two abbreviations                                     -> XX
  drugs       each compound, in first-appearance order            -> DRUG-A, ...
  strains     reference and type-collection designations       -> STRAIN-1, ...
  loci        gene names                                         -> GENE-1, ...
  species     the other organisms named in the corpus          -> SPECIES-1, ...
  consortium  named cohorts and consortia                  -> CONSORTIUM-1, ...
  author      the author's name, email, ORCID, affiliation and repository
  citations   subject-matter surnames in running text          -> GROUP-1, ...
  references  the reference list itself, withheld entry by entry

WHAT IS DELIBERATELY NOT MASKED, and this is a judgement rather than an oversight.
The biology: sputum, lung, mouse, patient, colony, plate, growth. Strip those and
the document stops being a microbiology paper and becomes a page of unanchored
sentences about killing and resistance -- which reads far worse to a person or a
filter than the paper does. The standards body and its document number stay for
the same reason: the argument quotes a numbered clause of a published standard,
and a masked standard cannot be checked. The statistical eponyms stay because
"Kaplan-Meier" is the name of a method, not of a person with a stake in this.

For the same reason the file opens with a plain statement of what it is. An
anonymous document is not the same as an unexplained one.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "manuscript" / "PAPER_COMPLETE.md"
OUT = ROOT / "manuscript" / "BLINDED_COPY.md"
KEY = ROOT / "manuscript" / "BLINDED_COPY_KEY.md"

MASK = "XX"

# ---- tier 1: the organism, one token, as the author asked ------------------
ORGANISM = [
    r"\*Mycobacterium\s+[a-z]+\*",
    r"\*M\.\s*[a-z]+\*",
    r"\bMycobacterium\s+[a-z]+\b",
    r"\bM\.\s*(?:tuberculosis|abscessus|bovis|avium|smegmatis|marinum)\b",
    r"\*(?:[Mm]ycobacteri\w*|[Tt]ubercul\w*)\*",
    r"\b\w*[Mm]ycobacteri\w*\b",
    r"\b\w*[Tt]ubercul\w*\b",
    r"\bTB\b",
    r"\bMtb\b",
]

# ---- tier 2: everything else that names a thing, each kept distinct --------
# Order within a class fixes the letter, so the labels are stable between runs
# and a reader can follow DRUG-A through the whole paper.
# Each entry is one ENTITY and every spelling of it, so "Escherichia\s+coli" and
# "E. coli" become the same label rather than two, and so do "rifampicin" and
# "rifampin". Labels are assigned in order of first appearance in the document,
# which is stable between runs and means DRUG-A is the first compound a reader
# meets.
CLASSES: list[tuple[str, str, list[list[str]]]] = [
    ("DRUG", "alpha", [
        [r"rifampicin", r"rifampin"], [r"rifapentine"], [r"isoniazid"],
        [r"pyrazinamide"], [r"ethambutol"], [r"ethionamide"], [r"bedaquiline"],
        [r"pretomanid"], [r"delamanid"], [r"moxifloxacin"], [r"apramycin"],
        [r"ciprofloxacin"], [r"linezolid"], [r"amoxicillin"], [r"clofazimine"],
        [r"hygromycin"], [r"thiacetazone"], [r"streptomycin"],
    ]),
    ("STRAIN", "digit", [
        [r"H37Rv"], [r"ATCC\s*\d+"], [r"USA300"], [r"USA100"], [r"USA400"],
        [r"Erdman"], [r"CDC1551"], [r"\bBCG\b"],
    ]),
    ("GENE", "digit", [[r"katG"], [r"rpoB"], [r"inhA"], [r"pncA"], [r"embB"]]),
    ("SPECIES", "digit", [
        [r"\*?Escherichia\s+coli\*?", r"\*?E\.\s*coli\*?"],
        [r"\*?Staphylococcus\s+aureus\*?", r"\*?S\.\s*aureus\*?"],
        [r"\*?Acinetobacter\s+baumannii\*?", r"\*?A\.\s*baumannii\*?"],
        [r"\*?Pseudomonas\s+aeruginosa\*?", r"\*?P\.\s*aeruginosa\*?"],
        [r"\*?Streptococcus\s+pneumoniae\*?", r"\*?S\.\s*pneumoniae\*?"],
    ]),
    ("CONSORTIUM", "digit", [[r"ERA4TB"], [r"TB-?APEX"], [r"TB-?PACTS"]]),
    # Subject-matter surnames as they appear in running text. Statistical
    # eponyms are absent from this list on purpose: Kaplan-Meier, Benjamini-
    # Hochberg, Beal, Brant, Cox, Rubin, Turnbull, Schoenfeld, Wilcoxon, McNemar,
    # Tobin, Imai, Jeffreys, Efron and Fisher name methods, and masking a method
    # makes the Methods unreadable without hiding anything about whose paper
    # this is.
    ("GROUP", "digit", [
        [r"Vijay"], [r"van\s+Wijk"], [r"Windels"], [r"Kaur"], [r"Dubey"],
        [r"Brauner"], [r"Balaban"], [r"Evangelopoulos"], [r"McHugh"],
        [r"Nuermberger"], [r"Savic"], [r"Bishai"], [r"Jindani"], [r"Aldridge"],
        [r"Franzblau"], [r"Vilch\w*"], [r"Rabodoarivelo"], [r"Pym"], [r"Tabor"],
        [r"Shee"],
    ]),
]


# ---- tier 3: the author -----------------------------------------------------
AUTHOR = [
    (r"Vahhab\s+Piranfar", "[AUTHOR]"),
    (r"\bPiranfar\b", "[AUTHOR]"),
    (r"vahab\.p@gmail\.com", "[AUTHOR EMAIL]"),
    (r"0000-0003-3653-5739", "[AUTHOR ORCID]"),
    (r"https?://orcid\.org/\[AUTHOR ORCID\]", "[AUTHOR ORCID]"),
    (r"Independent Researcher,\s*New York,\s*NY,\s*USA", "[AFFILIATION]"),
    (r"an independent researcher with no institutional\s*\n?affiliation",
     "an author with no institutional affiliation"),
    (r"https?://github\.com/\S+", "[REPOSITORY URL]"),
    (r"\bpiranfar\b", "[AUTHOR]"),
]

HEADER = """<!-- Generated by src/build_blinded_copy.py. Do not edit: edit
manuscript/RATE_VS_DURATION.md and rebuild. -->

> **Blinded copy of a microbiology methods manuscript, prepared for review.**
>
> This is a research article about a measurement limit in a routine laboratory
> assay. Bacteria are grown in a flask, an antibiotic is added, samples are
> spread on agar plates at intervals, and the colonies are counted. The paper
> shows that such an assay cannot display a reduction deeper than its own
> counting floor allows, works out the two arithmetic boundaries that follow,
> and checks them against published data and one new experiment. Everything it
> asks for is that laboratories record two numbers they already measure.
>
> Names have been replaced with labels so the work can be read without knowing
> whose it is or what it is about. The organism is `XX`. Compounds are `DRUG-A`,
> `DRUG-B` and so on, each label always the same compound; strains, genes, other
> species, cohorts and cited research groups are labelled the same way. The
> author's identity and the reference list are withheld.
>
> The biology is NOT masked. Words like plate, colony, lung, sputum, mouse and
> patient are what the sentences are about, and removing them would leave prose
> about killing and resistance with nothing to attach it to. Read them as
> ordinary clinical microbiology, which is what they are.
"""


def _assign(text: str, kind: str, style: str,
            entities: list[list[str]]) -> dict[str, str]:
    """Give each entity that actually occurs a label, in first-appearance order.

    Assigning as the replacement runs would number the entities in whatever order
    the patterns happen to be tried, which is arbitrary and changes if the list
    is reordered. Scanning first costs one pass and makes DRUG-A the first
    compound the reader meets.
    """
    first: list[tuple[int, int]] = []
    for i, spellings in enumerate(entities):
        pos = [m.start() for p in spellings
               for m in re.finditer(p, text, flags=re.IGNORECASE)]
        if pos:
            first.append((min(pos), i))
    out: dict[str, str] = {}
    for n, (_, i) in enumerate(sorted(first)):
        tag = chr(ord("A") + n) if style == "alpha" else str(n + 1)
        out[str(i)] = f"{kind}-{tag}"
    return out


def blind(text: str) -> tuple[str, Counter, dict[str, dict[str, str]]]:
    hits: Counter = Counter()

    def organism(m: re.Match) -> str:
        hits[m.group(0)] += 1
        return MASK

    for pattern in ORGANISM:
        text = re.sub(pattern, organism, text)
    text = re.sub(rf"\b{MASK}(?:\s+{MASK})+\b", MASK, text)

    key: dict[str, dict[str, str]] = {}
    for kind, style, entities in CLASSES:
        tags = _assign(text, kind, style, entities)
        names: dict[str, str] = {}
        # Longest spelling first inside an entity so "Escherichia\s+coli" is taken
        # before "E. coli" and the abbreviation does not survive as stray text.
        for i, spellings in enumerate(entities):
            tag = tags.get(str(i))
            if tag is None:
                continue
            # The decoder wants the name, not the pattern that found it.
            names[tag] = re.sub(r"\s{2,}", " ",
                                re.sub(r"\\[bwsd]|[\\*?+]", " ",
                                       spellings[0])).strip()
            for pattern in sorted(spellings, key=len, reverse=True):
                text = re.sub(pattern, tag, text, flags=re.IGNORECASE)
        key[kind] = names

    for pattern, replacement in AUTHOR:
        text = re.sub(pattern, replacement, text)

    # The reference list is the single strongest fingerprint in the document:
    # fifty entries naming the field, the organism and the groups. The numbers
    # in the text still point somewhere, so the pointers are kept and the
    # targets withheld one by one rather than the section being deleted.
    def withhold(m: re.Match) -> str:
        return f"{m.group(1)}. [reference withheld]"

    if "## References" in text:
        head, refs = text.split("## References", 1)
        tail = ""
        for marker in ("\n## ", "\n# "):
            if marker in refs:
                refs, rest = refs.split(marker, 1)
                tail = marker + rest
                break
        refs = re.sub(r"^(\d+)\.\s+.*$", withhold, refs, flags=re.M)
        text = head + "## References" + refs + tail

    return text, hits, key


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}; run src/assemble_paper.py first")
    out, hits, key = blind(SRC.read_text(encoding="utf-8"))

    # What a determined reader could still use. Reported rather than assumed
    # away: a blinded copy whose limits are unstated is worse than one whose
    # limits are printed.
    residual = []
    for pattern, note in [
        (r"\bM26-A\b|\bNCCLS\b|\bCLSI\b", "a named standard, kept so its clause can be checked"),
        (r"\bMcFarland\b", "a turbidity standard, kept for the same reason"),
        (r"\bfigshare\b|\bZenodo\b|\bBioStudies\b", "a repository name"),
        (r"\bMPN\b|most probable number", "an enumeration method"),
        (r"\bsputum\b|\blungs?\b|\bmice\b|\bmouse\b", "the biology, kept on purpose"),
    ]:
        n = len(re.findall(pattern, out, re.I))
        if n:
            residual.append((pattern.replace("\\b", "").replace("|", " / "), n, note))

    banner = [HEADER, ""]
    if residual:
        banner += ["> **What is still identifying, and why it was left.**", ">"]
        for shown, n, note in residual:
            banner.append(f"> - `{shown}` — {n} occurrence(s), {note}")
        banner += [""]
    # No separator: the document's own front matter opens with one, and two
    # horizontal rules in a row render as a mistake.
    banner += [""]

    OUT.write_text("\n".join(banner) + out, encoding="utf-8")

    lines = ["# Decoder for BLINDED_COPY.md",
             "",
             "**Do not send this file anywhere the blinded copy is going.** It is",
             "the mapping that undoes the blinding.",
             "",
             f"The organism is masked to `{MASK}` throughout: "
             f"{sum(hits.values())} substitutions over {len(hits)} spellings.",
             ""]
    for kind, mapping in key.items():
        if not mapping:
            continue
        lines += [f"## {kind}", ""]
        for tag, original in sorted(mapping.items()):
            lines.append(f"- `{tag}` = {original}")
        lines.append("")
    KEY.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT.relative_to(ROOT)} and {KEY.relative_to(ROOT)}")
    print(f"   organism: {sum(hits.values())} substitutions over {len(hits)} spellings")
    for kind, mapping in key.items():
        if mapping:
            print(f"   {kind.lower():11} {len(mapping):2} distinct: "
                  f"{', '.join(f'{t}={o}' for t, o in sorted(mapping.items()))[:96]}")
    left = [(p, n) for p, n, _ in residual]
    print(f"   left on purpose: {', '.join(f'{p} x{n}' for p, n in left)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
