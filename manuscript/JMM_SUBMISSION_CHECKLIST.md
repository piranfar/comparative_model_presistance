# Journal of Microbiological Methods — submission checklist

Target chosen after a verified search for a journal that charges the author
nothing. Every cost row below was read on the publisher's or the journal's own
page; where something could not be read, the row says so rather than guessing.

Submission site: **https://submit.elsevier.com/MIMET** — the address the
journal's own Guide for Authors gives. An Editorial Manager page for this title
carries a "Site under development, do not use for live manuscript submission"
banner; that is the old platform being retired, not a journal in trouble.

---

## Why this journal

| Question | Answer | Evidence |
|---|---|---|
| Cost to the author | **Nothing**, on the subscription route. | The journal's own Guide for Authors contains the string "page charge" zero times and "submission fee" zero times. The only charge named in it is the optional gold-OA APC of USD 3,230. Its "Color artwork" section offers free online colour and does not offer or price colour in print. Elsevier's own publishing-options page: authors in hybrid journals "can publish under the subscription model at no cost". Elsevier's own APC price list, priced 27 Aug 2026, lists ISSN 0167-7012 as "Hybrid Open Access". |
| Indexed | **MEDLINE, currently indexed.** | NLM Catalog record fetched directly: MedlineTA "J Microbiol Methods", IndexingStatus "Currently-indexed", plus PubMed and Index Medicus. |
| Alive | 290 PubMed items dated 2026 against 231 in 2025, with articles dated the week of this search. |
| Word limit | **None.** "We do not impose a word limit, however we do strongly recommend to authors to be as succinct as possible." | The journal's own guide. This is the only free candidate found with no length pressure at all. |
| Abstract | 250 words, 1–7 keywords. | The journal's own guide. |
| Supplementary | Explicitly encouraged: "We encourage the use of supplementary materials such as applications, images and sound clips to enhance research." | The journal's own guide. |

**Runner-up, if this fails.** *FEMS Microbiology Letters* (OUP, for FEMS). Free
by deliberate policy — FEMS kept exactly one subscription journal so that authors
without APC funds could publish — with colour free and supplementary free.
Research Article limit 6,500 words with 8 display items, which the manuscript
would meet. Weaker only on scope: a broad letters journal where a paper resting
largely on reanalysis is an unusual submission.

---

## The one real risk, and what was done about it

JMM's aims ask for methodologies that are "novel, state-of-the-art, and
significantly improved", and Research Articles "must contribute new knowledge".
**A paper framed as a critique of five other groups' deposits could be desk
rejected on that wording alone.** It is not framed that way:

- The title claims what the paper establishes — the floor bounds what the assay
  can **report** — rather than an indictment of anyone's data.
- The aims paragraph now opens on the contribution: two boundaries on the
  starting density, derived from the definitions, computed from quantities a
  time-kill protocol already records.
- The prospective *E. coli* experiment is named in the aims, in the Abstract and
  in the cover letter. It is the thing an editor can hold that is not a
  reanalysis.
- Box 1 is the deliverable: three numbers an investigator enters before seeding,
  which say which endpoints the experiment will be able to report.

The journal demonstrably prints this shape of paper — a killing assay whose
endpoint does not mean what users assume; *M. tuberculosis* viable-count
quantification against its floor; a susceptibility-testing methodology critique.

---

## Done

| Item | Requirement | State |
|---|---|---|
| Article type | Research Article. | Front matter reads `Research Article`. |
| Title | No stated limit. | Retitled: names the finding and the design, expands "MDK", and drops the universal "every MDK" that the Discussion spent a paragraph walking back. 168 characters. |
| Abstract | 250 words, 1–7 keywords. | Exactly 250 words. Seven keywords, retargeted to the journal's own vocabulary. |
| Main text length | No limit, succinctness encouraged. | 12,000 words with 3 tables and 4 figures. Legal, and shorter than it was. |
| Supplementary file | Encouraged; **can only be added or replaced at revision**, so it must be complete at first submission. | One file: three supplementary analyses, the full Materials and Methods, one supplementary figure and 22 supplementary tables. Built by `src/build_submission.py` from the same prose as the article, so the two cannot drift. |
| Every supplementary item cited | Files "must be cited in the text". | Enforced by the builder, which fails the build if an item is uncited. |
| Reference style | Numbered, citation order. | Generated per file from its own citation order: 27 in the article, 38 in the supplement. |
| Data availability | Required. | Paragraph at the end of Materials and Methods. |
| Publication route | Subscription, not open access — this is what makes it free. | Requested explicitly in the cover letter. **Confirm it again on the submission form; the OA question is asked there and a wrong click costs USD 3,230.** |
| Affiliation | Department, institution, city, country. | **Independent Researcher, New York, NY, USA.** In the manuscript front matter and in the cover letter signature. |
| Generative AI disclosure | Required where generative AI assisted the writing. | Written, and it says what happened: Claude (Opus 5) edited and revised the text and wrote the analysis and plotting code; no figure or image was AI-generated; no AI tool is an author; the author verified every quantity against the deposits and the pipeline and takes responsibility. In Materials and Methods, repeated in the cover letter. |
| Ethics determination | Required, or a statement that none was needed. | Stated: an independent researcher has no institutional review board with jurisdiction, none was approached, and none is required for secondary analysis of de-identified data already public under open licences. The prospective experiment used a reference strain and no human or animal material. |
| Figure 2, panels B and D | Editorial call. | **Moved to Figure S1.** The Kaplan–Meier panel and the Cox p-value panel each disclaimed itself in its own legend, and a panel that has to do that does not belong in a main figure. Figure 2 is now two panels; `src/figures/figS1_survival_and_cox.py` imports the loader from `fig2_rate_vs_duration`, so the two cannot disagree about which laboratory is which colour. Checking the moved panel against its own table turned up an error the legend had carried through two review rounds — it said "five of the six terms move toward p = 1" where the model has five laboratory terms and four of them move. Corrected, and now pinned in `audit_claims`. |

---

## Outstanding — author decisions

| Item | What is needed |
|---|---|
| **Print colour** | The guide prices no print colour and offers free online colour. If the proof stage offers print colour, decline it. |
| **Repository URL** | The code deposit is cited as a reference; its public URL is not yet fixed. |
