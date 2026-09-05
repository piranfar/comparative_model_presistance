"""
Convert the reference list and its in-text citations to Springer author-date.

Run:  python -m src.reference_style

Bulletin of Mathematical Biology wants name-and-year citations in the text and
an alphabetised reference list, where this manuscript carries Vancouver-style
numbered citations. The conversion is mechanical but has to be exact: a
mis-ordered list silently repoints citations, which is the same failure the
document build already produced once through Word's shared list counter.

The reference data is written out here rather than parsed out of the Markdown.
Parsing free-text references is where this kind of script goes wrong, and there
are only twenty-one of them.

Writes `manuscript/REVISED_MANUSCRIPT_authordate.md`. The numbered version is
left untouched, because bioRxiv has it and the two now diverge.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "manuscript" / "REVISED_MANUSCRIPT.md"
OUT = ROOT / "manuscript" / "REVISED_MANUSCRIPT_authordate.md"

# number in the current list -> (citation key, authors, year, rest, doi)
# `cite` is what appears in the text; `sort` is the alphabetisation key.
REFS = {
    1: dict(cite="Lewis 2007", sort=("Lewis", 2007),
            authors="Lewis K", year=2007,
            rest="Persister cells, dormancy and infectious disease. Nat Rev Microbiol 5:48-56",
            doi="10.1038/nrmicro1557"),
    2: dict(cite="Zhang and Yew 2009", sort=("Zhang", 2009),
            authors="Zhang Y, Yew WW", year=2009,
            rest="Mechanisms of drug resistance in Mycobacterium tuberculosis. Int J Tuberc Lung Dis 13:1320-1330",
            doi=None),
    3: dict(cite="Balaban et al. 2019", sort=("Balaban", 2019),
            authors="Balaban NQ, Helaine S, Lewis K, Ackermann M, Aldridge B, Andersson DI et al",
            year=2019,
            rest="Definitions and guidelines for research on antibiotic persistence. Nat Rev Microbiol 17:441-448",
            doi="10.1038/s41579-019-0196-3"),
    4: dict(cite="Brauner et al. 2016", sort=("Brauner", 2016),
            authors="Brauner A, Fridman O, Gefen O, Balaban NQ", year=2016,
            rest="Distinguishing between resistance, tolerance and persistence to antibiotic treatment. Nat Rev Microbiol 14:320-330",
            doi="10.1038/nrmicro.2016.34"),
    5: dict(cite="World Health Organization 2021", sort=("World Health Organization", 2021),
            authors="World Health Organization", year=2021,
            rest="Global tuberculosis report 2021. World Health Organization, Geneva. ISBN 978-92-4-003702-1",
            doi=None),
    6: dict(cite="Levin and Rozen 2006", sort=("Levin", 2006),
            authors="Levin BR, Rozen DE", year=2006,
            rest="Non-inherited antibiotic resistance. Nat Rev Microbiol 4:556-562",
            doi="10.1038/nrmicro1445"),
    7: dict(cite="Dhar and McKinney 2010", sort=("Dhar", 2010),
            authors="Dhar N, McKinney JD", year=2010,
            rest="Mycobacterium tuberculosis persistence mutants identified by screening in isoniazid-treated mice. Proc Natl Acad Sci USA 107:12275-12280",
            doi="10.1073/pnas.1003219107"),
    8: dict(cite="Gengenbacher and Kaufmann 2012", sort=("Gengenbacher", 2012),
            authors="Gengenbacher M, Kaufmann SHE", year=2012,
            rest="Mycobacterium tuberculosis: success through dormancy. FEMS Microbiol Rev 36:514-532",
            doi="10.1111/j.1574-6976.2012.00331.x"),
    9: dict(cite="Wakamoto et al. 2013", sort=("Wakamoto", 2013),
            authors="Wakamoto Y, Dhar N, Chait R, Schneider K, Signorino-Gelo F, Leibler S, McKinney JD",
            year=2013,
            rest="Dynamic persistence of antibiotic-stressed mycobacteria. Science 339:91-95",
            doi="10.1126/science.1229858"),
    10: dict(cite="Aldridge et al. 2012", sort=("Aldridge", 2012),
             authors="Aldridge BB, Fernandez-Suarez M, Heller D, Ambravaneswaran V, Sundaresan V, Fortune SM",
             year=2012,
             rest="Asymmetry and aging of mycobacterial cells lead to variable growth and antibiotic susceptibility. Science 335:100-104",
             doi="10.1126/science.1216166"),
    11: dict(cite="Conlon et al. 2016", sort=("Conlon", 2016),
             authors="Conlon BP, Rowe SE, Gandt AB, Nuxoll AS, Donegan NP, Zalis EA et al",
             year=2016,
             rest="Persister formation in Staphylococcus aureus is associated with ATP depletion. Nat Microbiol 1:16051",
             doi="10.1038/nmicrobiol.2016.51"),
    12: dict(cite="Wilmaerts et al. 2019", sort=("Wilmaerts", 2019),
             authors="Wilmaerts D, Windels EM, Verstraeten N, Michiels J", year=2019,
             rest="General mechanisms leading to persister formation and awakening. Trends Genet 35:401-411",
             doi="10.1016/j.tig.2019.03.007"),
    13: dict(cite="Regoes et al. 2004", sort=("Regoes", 2004),
             authors="Regoes RR, Wiuff C, Zappala RM, Garner KN, Baquero F, Levin BR",
             year=2004,
             rest="Pharmacodynamic functions: a multiparameter approach to the design of antibiotic treatment regimens. Antimicrob Agents Chemother 48:3670-3676",
             doi="10.1128/AAC.48.10.3670-3676.2004"),
    14: dict(cite="Nielsen and Friberg 2013", sort=("Nielsen", 2013),
             authors="Nielsen EI, Friberg LE", year=2013,
             rest="Pharmacokinetic-pharmacodynamic modeling of antibacterial drugs. Pharmacol Rev 65:1053-1090",
             doi="10.1124/pr.111.005769"),
    15: dict(cite="Whitman et al. 1998", sort=("Whitman", 1998),
             authors="Whitman WB, Coleman DC, Wiebe WJ", year=1998,
             rest="Prokaryotes: the unseen majority. Proc Natl Acad Sci USA 95:6578-6583",
             doi="10.1073/pnas.95.12.6578"),
    16: dict(cite="Pu et al. 2019", sort=("Pu", 2019),
             authors="Pu Y, Li Y, Jin X, Tian T, Ma Q, Zhao Z et al", year=2019,
             rest="ATP-dependent dynamic protein aggregation regulates bacterial dormancy depth critical for antibiotic tolerance. Mol Cell 73:143-156",
             doi="10.1016/j.molcel.2018.10.022"),
    17: dict(cite="Tsuji et al. 2012", sort=("Tsuji", 2012),
             authors="Tsuji BT, Brown T, Parasrampuria R, Brazeau DA, Forrest A, Kelchlin PA et al",
             year=2012,
             rest="Front-loaded linezolid regimens result in increased killing and suppression of the accessory gene regulator system of Staphylococcus aureus. Antimicrob Agents Chemother 56:3712-3719",
             doi="10.1128/AAC.05453-11"),
    18: dict(cite="Drusano et al. 2018", sort=("Drusano", 2018),
             authors="Drusano GL, Myrick J, Maynard M, Nole J, Duncanson B, Brown D et al",
             year=2018,
             rest="Linezolid kills acid-phase and non-replicative-persister-phase Mycobacterium tuberculosis in a hollow-fiber infection model. Antimicrob Agents Chemother 62:e00221-18",
             doi="10.1128/AAC.00221-18"),
    19: dict(cite="Pasipanodya et al. 2015", sort=("Pasipanodya", 2015),
             authors="Pasipanodya JG, Nuermberger E, Romero K, Hanna D, Gumbo T", year=2015,
             rest="Systematic analysis of hollow fiber model of tuberculosis experiments. Clin Infect Dis 61(Suppl 1):S10-S17",
             doi="10.1093/cid/civ425"),
    20: dict(cite="Gumbo et al. 2004", sort=("Gumbo", 2004),
             authors="Gumbo T, Louie A, Deziel MR, Parsons LM, Salfinger M, Drusano GL",
             year=2004,
             rest="Selection of a moxifloxacin dose that suppresses drug resistance in Mycobacterium tuberculosis, by use of an in vitro pharmacodynamic infection model and mathematical modeling. J Infect Dis 190:1642-1651",
             doi="10.1086/424849"),
    # Added for the journal version's Discussion and Methods. Every entry below
    # was verified against its PubMed record rather than recalled: the PMID
    # first used for Abel Zur Wiesch et al. turned out to belong to a paper on
    # prokaryotic flotillins, and the claim originally attributed to that paper
    # was not the one it makes.
    22: dict(cite="Beal 2001", sort=("Beal", 2001),
             authors="Beal SL", year=2001,
             rest="Ways to fit a PK model with some data below the quantification limit. J Pharmacokinet Pharmacodyn 28:481-504",
             doi="10.1023/a:1012299115260"),
    23: dict(cite="Patra and Klumpp 2013", sort=("Patra", 2013),
             authors="Patra P, Klumpp S", year=2013,
             rest="Population dynamics of bacterial persistence. PLoS One 8:e62814",
             doi="10.1371/journal.pone.0062814"),
    24: dict(cite="Magombedze et al. 2021", sort=("Magombedze", 2021),
             authors="Magombedze G, Pasipanodya JG, Gumbo T", year=2021,
             rest="Bacterial load slopes represent biomarkers of tuberculosis therapy success, failure, and relapse. Commun Biol 4:664",
             doi="10.1038/s42003-021-02184-0"),
    25: dict(cite="Martinecz et al. 2023", sort=("Martinecz", 2023),
             authors="Martinecz A, Boeree MJ, Diacon AH, Dawson R, Hemez C, Aarnoutse RE, Abel Zur Wiesch P",
             year=2023,
             rest="High rifampicin peak plasma concentrations accelerate the slow phase of bacterial decline in tuberculosis patients: evidence for heteroresistance. PLoS Comput Biol 19:e1011000",
             doi="10.1371/journal.pcbi.1011000"),
    26: dict(cite="Abel Zur Wiesch et al. 2015", sort=("Abel Zur Wiesch", 2015),
             authors="Abel Zur Wiesch P, Abel S, Gkotzis S, Ocampo P, Engelstädter J, Hinkley T et al",
             year=2015,
             rest="Classic reaction kinetics can explain complex patterns of antibiotic action. Sci Transl Med 7:287ra73",
             doi="10.1126/scitranslmed.aaa8760"),
    27: dict(cite="Dickinson and Mitchison 1981", sort=("Dickinson", 1981),
             authors="Dickinson JM, Mitchison DA", year=1981,
             rest="Experimental models to explain the high sterilizing activity of rifampin in the chemotherapy of tuberculosis. Am Rev Respir Dis 123:367-371",
             doi="10.1164/arrd.1981.123.4.367"),
    21: dict(cite="Conlon et al. 2013", sort=("Conlon", 2013),
             authors="Conlon BP, Nakayasu ES, Fischer LE, LoSasso G, Kim W, Lewis K et al",
             year=2013,
             rest="Activated ClpP kills persisters and eradicates a chronic biofilm infection. Nature 503:365-370",
             doi="10.1038/nature12790"),
}


def entry(r: dict) -> str:
    line = f"{r['authors']} ({r['year']}) {r['rest']}."
    if r["doi"]:
        line += f" https://doi.org/{r['doi']}"
    return line


def citation(numbers: list[int]) -> str:
    """Render one bracketed group as a name-and-year citation."""
    keys = sorted((REFS[n] for n in numbers), key=lambda r: r["sort"])
    return "(" + "; ".join(k["cite"] for k in keys) + ")"


def cited_in(text: str) -> list[dict]:
    """The entries actually cited in `text`, alphabetised.

    Springer is explicit that the list "should only include works that are cited
    in the text", and the two manuscripts drawn from this project cite different
    subsets. Citations are matched with whitespace collapsed, because a citation
    broken across a line break is still a citation, and in both the parenthetical
    and the narrative form.
    """
    flat = re.sub(r"\s+", " ", re.sub(r"\((\d{4})\)", r"\1", text))
    return sorted((r for r in REFS.values() if r["cite"] in flat),
                  key=lambda r: r["sort"])


def convert(text: str) -> str:
    def repl(m):
        nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
        if not nums or any(n not in REFS for n in nums):
            return m.group(0)
        return citation(nums)

    # Only bracketed groups that are entirely digits, commas and spaces.
    text = re.sub(r"\[([\d,\s]+)\]", repl, text)

    head, tail = text.split("## References", 1)
    body = tail.split("\n\n", 1)[1] if "\n\n" in tail else ""
    body = "\n".join(l for l in body.split("\n") if not re.match(r"^\d+\.\s", l))

    ordered = sorted(REFS.values(), key=lambda r: r["sort"])
    listing = "\n\n".join(entry(r) for r in ordered)
    preamble = (
        "All entries were verified in September 2026 against their PubMed record, "
        "except the World Health Organization report, which is not indexed in "
        "PubMed and was verified against the publisher record. Digital object "
        "identifiers are given where one exists; one entry (Zhang and Yew 2009) "
        "has none.")
    return f"{head}## References\n\n{preamble}\n\n{listing}\n{body}"


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    out = convert(text)
    OUT.write_text(out, encoding="utf-8")

    left = re.findall(r"\[[\d,\s]+\]", out)
    print(f"wrote {OUT.name}")
    print(f"  references: {len(REFS)}, alphabetised, "
          f"{sum(1 for r in REFS.values() if r['doi'])} with a DOI")
    print(f"  unconverted numeric citations remaining: {len(left)}")
    if left:
        print("   ", left[:5])
    return 0 if not left else 1


if __name__ == "__main__":
    raise SystemExit(main())
