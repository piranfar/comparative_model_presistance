# AAC submission checklist

Every row is sourced from an ASM or AAC page; where a requirement could not be
established, the row says so rather than guessing. AAC runs a **two-stage**
regime: initial submission is format-neutral, and most formatting is enforced
only at revision. Rows are marked accordingly.

---

## Done

| Item | What was required | State |
|---|---|---|
| Article type | AAC has **no "Resource" type**. Research Article is the only type admitting an unsolicited, full-length, abstract-bearing primary report. | Front matter now reads `Research Article`. |
| Abstract | ≤250 words, unstructured, no abbreviations, no references, must end with a summary statement, must stand alone. | Exactly 250 words. Unstructured. Its cross-reference to Box 1 was removed. Ends on the summary statement. |
| IMPORTANCE statement | **Not required at AAC** (unlike several sibling ASM journals). Checked negative on the AAC article-types page and against published AAC articles. | None written. Correct. |
| Section order | AAC's element list: Title / Abstract / Introduction / Results / Discussion / Materials and Methods / Acknowledgments. | Restructured. "Methods" renamed "Materials and Methods"; the standalone Conclusion is now the closing subsection of the Discussion, since AAC's list has no Conclusion section. |
| Ethics placement | The statement **must physically live in Materials and Methods**. | Moved there from the old Declarations block. |
| Data availability | A paragraph led by "Data availability" at the **end of Materials and Methods**, giving data description, repositories, and DOIs or accession numbers. | Written, at the end of Materials and Methods. |
| Acknowledgments | Funding, competing interests and contributor roles go **inside Acknowledgments, unheaded**. There is no separate published Conflict of Interest heading. | Standalone Declarations block deleted; the three statements now run as unheaded paragraphs under Acknowledgments. |
| Funding | Explicit statement required; a blank form field is read as "no support received". | "No specific grant from any funding agency…" |
| Competing interests | Required. | "The author declares no competing interests." |
| Figure fonts | Arial, Helvetica or Times New Roman. | The plotting style led with Segoe UI; Arial now leads. |
| Figure dimensions | 7 × 9 inches or less, submitted at intended publication size. | Figure 1 was 11.4 in wide — over a full page. Reflowed to 7.0 × 3.3 with wrapped panel titles (they collided at the narrower width; checked visually). The other three narrowed 7.4 → 7.0. |
| Figure format | TIFF or EPS at revision, 300–600 dpi, RGB — **not RGBA**, which is what matplotlib writes. | The build now emits `.tif` at 600 dpi, flattened to RGB, alongside the PNG and PDF. |
| Figure vocabulary | — | Not an AAC rule, but found while checking: Figure 2 still said "cleared", "never cleared" and "no clearance time exists" in three panels, the vocabulary the manuscript renamed two rounds ago. The words were baked into the image, so no checker that reads the manuscript could see them. Fixed, and a new audit rule now reads the figure scripts' visible strings. |

## Needs you before submission

| Item | What is required | Why I could not do it |
|---|---|---|
| **Affiliation, ORCID, email** | Corresponding author's ORCID is **required** at submission; contributing authors' are optional. | Yours to supply. Three placeholders remain in the front matter. |
| **Generative AI disclosure** | Required in the **cover letter**, and separately in **Materials and Methods**. ASM prescribes no template. | See `AI_DISCLOSURE.md`. This is a declaration about your own conduct and ASM's limits are restrictive; read that file before choosing wording. Placeholders currently point at it — they must not go out. |
| **Ethics determination** | A statement of IRB approval, or of waiver **with the reason**, or of adherence to the Declaration of Helsinki, in Materials and Methods. | **ASM publishes no route for secondary analysis of already-public de-identified data.** Searched exhaustively: the Human Subjects policy offers only approval or waiver. This needs a written non-human-subjects determination from your institution, or a ruling from the AAC editorial office (aac@asmusa.org). |
| **Repository URL** | Source code deposition is **mandatory**, with installation and run documentation and a test dataset with control parameter settings. GitHub is named as acceptable. The repository licence must be no more restrictive than CC BY. | The repository is not yet public. Its URL and the submitted commit identifier are placeholders in the Data availability paragraph, and the code entry in the reference list has an empty identifier. |
| **Three preferred reviewers** | Name, email and institution for **at least three** are required on the form. Preferred editors are required too. | Yours to choose. |
| **Primary manuscripts as supplemental-not-for-publication** | Reusing published datasets requires four affirmations, one of which is uploading copies of the primary manuscripts. | The five papers are named in the cover letter; the PDFs must be uploaded at submission. |
| **Title** | AAC gives no title character limit; the **running title is capped at 54 characters**. | Three candidates are in `RESPONSE_TO_REVIEW_R2.md` under M9. The current title's unexpanded "MDK" is the audit's one remaining medium finding. |

## Flagged — unresolved upstream, decide before submitting

| Item | The problem |
|---|---|
| **Box 1** | AAC's Research Article element list has **no "Box"**. Three routes exist — make it a table, make it an appendix (AAC permits appendixes), or leave it to production — and **no ASM page chooses between them**. Making it Table 1 would renumber sixteen hardcoded tables and every citation, which is the cascade that has caused defects in this manuscript before, so I left it alone. Ask the editorial office. |
| **Two significant figures** | ASM: reporting data to more than two significant figures must be **justified by statistical analysis**. This manuscript quotes many three-figure values (26.2 per cent, 4.40 log10, 12.15-fold). Most are defensible — they are exact counts or interval bounds — but a reviewer may ask, and the Methods do not currently make the argument. |
| **Scope** | AAC's scope admits assay-method validation but refers some assay and quality-control papers to the *Journal of Clinical Microbiology*, and excludes new methods not applied to antimicrobial action. The cover letter makes the scope case deliberately. **This matters more than politeness:** a scope rejection can be transferred to another ASM journal, but a rejection on scientific grounds closes every ASM journal. |
| **Page charges** | AAC is Subscribe-to-Open with no APC, but charges **$125–221 per page**, with supplemental material a flat $214–380. The manuscript is long and carries 16 main tables. Moving tables to supplemental is the cheapest lever on the bill, and ASM would rather large data went to a repository than to supplemental files at all. |
| **Licence** | CC BY vs Exclusive Licence to Publish is decided by whether the Sustainability Target is met **or your institution subscribes** — not by a fee. Worth checking your institution's status before committing. |

## Not applicable, checked

- **Keywords** are collected on the submission form, not in the manuscript. The seven in the front matter are for the form.
- **Word limit**: AAC publishes **no total word count** for Research Articles.
- **Display-item cap**: none for Research Articles. The 16 tables are permitted; the pressure on them is cost and readability, not compliance.
- **Preprints**: AAC accepts them and takes direct submission from bioRxiv and medRxiv. Disclose at submission if posted.
