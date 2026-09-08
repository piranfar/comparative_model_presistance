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
4. **The corpus is being expanded from 29 to ~42 deposits.** In progress; readers
   are being written and reviewed as I write this.

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

## 4. Corpus expansion — in progress

Manifest 62 → 78 rows. 13 of 16 new deposits downloaded with provenance;
Rifapentine recovered after diagnosing the fetcher's dropped URL parameter.

Readers are being written and adversarially reviewed one per deposit, with one
rule above all others: **never invent a floor.** A reader that supplies a
plausible detection limit destroys the one number this corpus exists to count.

Two deposits have only a landing page and no file URL — `BARR2021_OSF` and
`TABOR2025_MINDTHEGAP`. They need their file URLs found by hand.

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
