# Generative AI disclosure — draft for the author's decision

**This is not something I can write for you and have you sign.** It is a
declaration about your own conduct, ASM's policy on it is restrictive, and the
honest description of how this manuscript was produced sits close to the edge of
what that policy permits. Read the tension below before choosing wording.

---

## What ASM requires

Two ASM pages impose different obligations and neither supersedes the other, so
both must be satisfied:

- **Cover letter.** "Use of AI tools must be disclosed at submission in the cover
  letter", and authors may be asked for the tool's name and version, its purpose,
  the prompts, and the input.
  (https://journals.asm.org/generative-ai)
- **Materials and Methods.** The role of AI tools must be explained there, with
  further detail in Acknowledgments if needed.
  (https://journals.asm.org/authorship)

ASM prescribes **no template sentence**. That was checked directly: the
Generative AI page carries no wording to copy.

## The substantive limits

1. Wholly AI-generated content is **not allowed**.
2. AI may **only** be used to improve the language, accessibility or quality of
   **human-generated** text.
3. AI must **not** be used for images, cover art, videos or schematics.
4. AI tools **cannot be authors**.
5. The author remains responsible for accuracy and for avoiding AI-introduced
   plagiarism.

## Where this manuscript sits against limit 2 — read this part

Limit 2 is the one that matters. On any honest account, generative AI was used
here for more than polishing prose you had already written. Across this project
it was used to:

- write and revise the analysis code in `src/`, including the experiment scripts,
  the two audit scripts and the eight checker modules;
- draft and revise substantial passages of the manuscript text, and to restructure
  it in response to two rounds of peer review;
- compile and verify the reference list;
- design and run the adversarial checks that found several of the defects the
  revisions corrected.

Calling that "improving the language of human-generated text" would not be true.
Three positions are available and **the choice is yours**:

**(a) Disclose it fully and let the editor rule.** The most defensible course.
State plainly what the tool did, state that you directed the work, verified every
number against the deposited data and the regenerating pipeline, and take
responsibility for the content. The reproducibility apparatus is an unusually
strong argument here: every quantity in the paper is regenerated from public
deposits by committed code, and two audit stages check the text against it. That
is a stronger accuracy guarantee than most manuscripts can offer, AI or not.

**(b) Ask AAC before submitting.** ASM's policy does not address a paper whose
analysis pipeline was AI-assisted end to end. The editorial office (aac@asmusa.org)
can say whether that is within policy. This costs a few days and removes the risk
of the question arriving as a rejection instead.

**(c) Reduce the AI contribution before submitting**, so the disclosure describes
something narrower. This means rewriting in your own words and re-deriving the
code yourself, and it is a large amount of work.

I recommend **(a) with (b) first** — ask, then disclose what you are told to
disclose. What I would not do is submit a disclosure that describes only language
editing, because that is not what happened, and a reviewer who reads the commit
history of the repository the Methods point them to will see it.

---

## Draft statement for Materials and Methods, on option (a)

> **Use of generative artificial intelligence.** Anthropic's Claude (Opus 5) was
> used throughout this work, under the author's direction: to write and revise the
> analysis code in the accompanying repository, to draft and revise manuscript
> text, to compile the reference list, and to construct the static checks
> described under Reproducibility. It was not used to generate any figure, image
> or schematic; every figure is plotted by the deposited code from the deposited
> data. No AI tool is an author. The author directed the analysis, verified every
> reported quantity against the source deposits and the regenerating pipeline, and
> takes full responsibility for the content, including its accuracy and
> originality.

## Draft sentence for the cover letter, on option (a)

> In accordance with ASM's policy on generative AI, we disclose that Anthropic's
> Claude (Opus 5) was used under the author's direction to write and revise the
> analysis code, to draft and revise manuscript text, and to construct the
> manuscript's static consistency checks. It was not used to generate figures or
> images. The author verified every reported quantity against the source deposits
> and the regenerating pipeline and takes full responsibility for the content. We
> are glad to supply further detail, including tool version and usage, on request.

---

## Before you use either draft

- Confirm the tool name and version you want on record.
- Decide between (a), (b) and (c) above.
- If you take (b), record what AAC tells you and put that wording in instead.
- The placeholder in Materials and Methods currently points here. Replace it with
  the statement you choose; the manuscript should not go out with a pointer to
  this file.
