# What happened while you slept — 8 September 2026

Written for you to read first thing. Everything below is committed; nothing is
pushed. The manuscript is green throughout: **152 of 152 claim checks agree, 0
high findings.**

---

## The short version

Four things worth your attention, in order of how much they change the paper.

1. **A study that already does what we ask, in a paper that never says so.** The
   best single illustration the project has found, and it is a positive one.
2. **The plate calls 18 mouse lungs sterile; a culture finds thousands in them.**
   Our clinical argument, observed in someone else's published data.
3. **The systematic sweep: 151 candidates assessed, 25 usable, 126 rejected with
   reasons.** This is what licences a defensible claim about coverage.
4. **The corpus went from 29 deposits to 40, and from 64,015 readings to
   68,812.** 17 of them now support the boundaries across 2,210 series in seven
   species, with zero violations. The best addition is human sputum from a
   tuberculosis trial — and it arrived with a mislabelled citation that would
   have put the wrong decade in the reference list.

---

## 1. The exemplar — Rifapentine (Lai et al. 2023)

The deposited workbook states its lower limit of detection **once per CFU sheet,
separately for each agar type, and separately for individual mice where they
differ**:

> "The lower limit of detection for each sample on each agar type was 0.78 log10
> CFU/lung."
> "The lower limit of detection for each sample on TCH agar was 0.54 log10
> CFU/lung."
> "Culture volume was 500 µL per agar plate."

That is better practice than anything else in the corpus — more than this
manuscript asks for.

**The article states none of it.** A full-text search of all 73,249 characters
returns zero occurrences of "limit of detection", "lower limit of detection",
"LLOD" and "0.78".

So the number is not missing from the science. It is missing from the paper.
Nobody was careless. The information does not travel from the supplementary
spreadsheet to the article, and a reader who never opens the workbook cannot know
the endpoint was bounded.

This reframes the whole recommendation from a complaint into a request for one
sentence, behind which somebody has already done the work. It is now the closing
argument of *What should change*.

### And its complement — Tabor et al. 2025

The deposited `Modeling data.csv` has 272 rows and 23 columns, one of them named
**`CFU_LOD`**. It is declared numeric. **Zero of 272 rows carry a value.** No
detection limit appears in any of the eight R analysis scripts deposited beside
it either.

The field for the detection limit was designed, declared, and never filled.

I verified this by opening the file rather than taking it from a report.

### A third instance, verified but not used in the text

Walter et al. 2021 write the censoring constant `2.176091259` — which is
log10(150) — three times into the "Fig 4a–c & Sup Fig 7-8" sheet of their Source
Data, and state the corresponding floor only in a supplementary figure legend.
The article body does not carry it.

Three cases, one pattern. Together they say the diagnosis is not carelessness:
the floor is measured, sometimes recorded better than anyone asks for, and it
falls out of the record between the bench and the reader — off the end of a
spreadsheet, or into a column nobody completed.

## 2. Below the floor is not nothing — Evangelopoulos et al. 2022

Three parallel enumerations of the **same** murine lungs: colony count, molecular
bacterial load, and most probable number.

In three arms, **18 lungs, the colony count reads zero in every animal** while
the most probable number on that same tissue runs from **1,450 to 18,700 per
lung**.

The distinction that makes this evidence rather than a curiosity: a molecular
load counts nucleic acid, and nucleic acid outlives its owner, so a sceptic can
attribute it to dead organisms. An MPN is a culture. Growth requires an organism
that is alive and culturable.

`exp43` recomputes all three figures from the deposit; they are pinned.

## 3. The systematic sweep

Six territories, twelve agents, 1,040 tool calls, search date 8 September 2026.
Full record with verbatim search strings in
`docs/TB_DEPOSIT_SWEEP_2026-09-08.md`.

- **151 candidates assessed**
- **25 qualifying**, collapsing to 21 distinct deposits once fingerprinted on
  DOI, figshare id, Zenodo record and PMC id — five were already ours under a
  different author's name
- **126 rejected with a stated reason**, and the reasons matter: Dryad DOIs that
  404 while the article cites them, steering-committee gates at TB-APEX and
  TB-PACTS, treated arms that are baseline plus a single endpoint, deposits that
  tabulate only medians

### On the claim you wanted

"We analysed all published TB data" is not available — one missed deposit
destroys it, and this sweep found 151 candidates where a casual search finds a
dozen. What **is** available, and is stronger because it is checkable:

> A systematic search of [sources] on 8 September 2026, with the strategy
> reported in the supplement, assessed 151 candidate deposits. N carried a
> measured starting density and a detection floor with a value and were
> analysed; M were excluded for the reasons recorded.

That cannot be refuted by finding a deposit the search missed. It can only be
extended.

## 4. Corpus expansion — done

**29 deposits and 64,015 readings this morning; 40 deposits and 68,812 readings
now.** Ten new readers written, each adversarially reviewed against its own
source file by a second agent.

The boundary sweep on the expanded corpus: **17 published deposits support the
boundaries, across 2,210 series, with 0 violations of the consistency
condition**, in seven species — *Acinetobacter baumannii*, *Escherichia coli*,
*Mycobacterium abscessus*, *M. tuberculosis*, *Pseudomonas aeruginosa* and
*Streptococcus pneumoniae*. Section 8 is updated to match.

### The most valuable addition, and a citation it nearly got wrong

`JINDANI1980_SGUL` — human sputum from a tuberculosis early-bactericidal-activity
trial. 112 patients, 989 readings across 8 timepoints, 977 with a floor. Median
headroom 4.23 logs: **43 of 112 patient series cannot demonstrate four logs and
83 cannot demonstrate five.** That is the clinical analogue of the deposit this
paper is built on.

The floor is recovered rather than assumed: `cfu == (Ct1+Ct2) × K × 10^Diln`
holds with a single K = 2.4 in 976 of 977 populated readings, so one colony at
that reading's own dilution is K × 10^Diln CFU/mL. Per-reading, derived from
inside the file, nothing taken from a paper.

**The deposit is mislabelled and I nearly cited the wrong decade.** figshare
27862029 carries the 2003 EBA paper's title and a description of "100 patients
treated with 22 regimens". The file inside is `Jindani 1980.xlsx`, the sheet is
"Jindani 1980", and it holds 112 patients and 24 regimens — including PAS and
thiacetazone, which belong to the 1980 study and not to the 2003 one. Renamed to
follow the contents, with the mismatch documented in the reader, the manifest and
the corpus directory. Cite it by DOI, `10.24376/rd.sgul.27862029.v1`, and do not
attach it to either paper without checking.

### The same animals, deposited twice

`build_corpus_long` now detects it. Two pairs survive a check that only counts
values distinctive enough that they could not collide by chance:

- **Dide-Agossou 2022 and Walter 2021** share 46 distinctive readings, 54% of one.
  Same group, same mice, two papers.
- **Rivani 2022 and Soeorg 2026** share 20, 28% of one — and this one is a
  finding. Soeorg's deposit is a NONMEM dataset built from time-kill curves its
  author extracted from published papers, and Rivani is evidently one of them.
  The corpus holds the same *Acinetobacter* measurements twice: once as a primary
  deposit, once as digitised input to somebody's model.

Nothing is deleted. Which copy is canonical is a judgement about the papers, and
the check exists so it gets made deliberately.

## 4b. What is still outstanding in the expansion

Manifest 62 → 78 rows. All 16 new deposits are now on disk with provenance.
Three needed hand-work: Rifapentine after diagnosing a dropped URL parameter,
and Barr and Tabor after finding their file URLs behind landing pages.

Every reader was written under one rule above all others: **never invent a
floor.** A reader that supplies a plausible detection limit destroys the one
number this corpus exists to count. Each was then reviewed by a second agent
whose brief was to attack that specifically.

One deposit still has no reader: `SHEE2026_SENOLYTIC`, which was still being
written when I stopped. Its interest is a contradiction worth confirming — the
Fig. 1 legend states a limit of detection of 10 CFU while the deposited sheets
appear to encode below-detection values as 1.

---

## Decisions waiting for you

| | |
|---|---|
| **Affiliation** | Still a placeholder in the manuscript. A submission with `[department, institution, city, country — to be inserted]` reads as unfinished before page two. |
| **Three preferred reviewers** | Elsevier asks at submission. None named. |
| **AI disclosure** | `manuscript/AI_DISCLOSURE.md` lays out three options honestly. Your call, and it must be made before submitting. |
| **Figure 2, panels B and D** | Both survival panels, both disclaimed in their own legend as descriptive rather than valid. Moving them to a supplementary figure would shorten the article and remove two panels that invite the objection the last review raised. |
| **VAN2026 files** | Permission granted verbally; the Zenodo files are still restricted. The depositors must open the record to your account or send the files. Permission is not access. |
| **Permission in writing** | 51 manifest rows record a verbal grant. A data availability statement resting on a phone call is not checkable — which is awkward in a paper about claims that cannot be checked. An email naming the deposit and DOI is enough. |

## Where the title stands

> The detection floor bounds what a time-kill assay can report: minimum duration
> for killing and log-reduction endpoints in five published deposits and a
> prospective test

You asked to put TB at the centre. The paper already is — sections 1–7 and 9 are
all *M. tuberculosis*, some 6,600 of 8,200 Results words — and Section 8 now says
so out loud. Three TB-centred title options are in the conversation; none is
applied, because the count in the version I first proposed was wrong and you
caught it. All five deposits are reanalysed and all five yield results; three
are TB.
