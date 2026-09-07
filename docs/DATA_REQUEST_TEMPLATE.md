# Writing to depositors and authors

Two different letters, because two different things are being asked for. Sending
the wrong one wastes the contact — most people answer once.

**Letter A** asks for the underlying data, and is the one worth sending. It goes
to authors whose paper reports kill curves but deposits nothing, or deposits only
a figure. What comes back is usually far better than anything digitised from a
plot: the actual counts, often with the plated volume and the detection limit
that the paper omitted.

**Letter B** asks only for permission to redistribute bytes we already have, and
is needed only where the licence blocks redistribution — NC into a CC BY
repository, or ND at all. It is a smaller ask and gets a faster yes.

A note on what you do NOT need to ask for. Analysing published numbers and
publishing conclusions from them is ordinary scholarship; in most jurisdictions
the measurements themselves are facts and are not what copyright protects. Ask
for data because it is better data and because it is courteous, and ask for
redistribution rights because a public repository needs them. Do not ask for
permission to do the analysis, which invites a "no" to a question nobody needed
to answer.

---

## Letter A — asking for the underlying data

> Subject: Request for the underlying time-kill counts from <SHORT CITATION>
>
> Dear Dr <NAME>,
>
> I am reanalysing published antibiotic time-kill data to ask a measurement
> question: whether the assay in each study could, in principle, have resolved
> the log-reduction endpoint the study reports. The answer turns on two numbers —
> the starting density and the smallest count the method can report — and it
> turns out that most papers report the first and not the second.
>
> Your <YEAR> paper in <JOURNAL> (<DOI>) is one of the studies I would like to
> include. Figure <N> shows the killing over time, and I can digitise it, but
> digitised points lose exactly what I need: the individual replicate counts, the
> volume plated, and how readings at or below the limit were recorded.
>
> Would you be willing to share the underlying counts? Anything machine-readable
> would be ideal — one row per plate or per reading, with the time, the replicate,
> the colonies counted and the volume plated. If those are only in a lab notebook
> or an old spreadsheet, that is fine; I would rather have the awkward original
> than a tidy summary.
>
> Two things I can offer in return. I will send you the analysis of your data
> before anything is submitted, so you can correct any misreading of your
> methods. And if it is useful to you, I will send back the tidied version in the
> common format the whole corpus uses.
>
> The work is a methodological reanalysis. There is no commercial interest in it,
> and I will cite your paper and your deposit however you prefer. If you would
> rather the data were not included, please just say so and I will leave it out.
>
> With thanks for considering it,
>
> Vahhab Piranfar
> ORCID 0000-0003-3653-5739
> <affiliation>

### Before you send it

- Read the paper's data-availability statement first. Asking for something they
  already deposited reads as carelessness and costs you the reply.
- Name the actual figure or table you want. A generic request gets a generic
  refusal.
- Write to the corresponding author, and copy the first author if they have since
  moved — the first author usually still has the files.
- One follow-up after three weeks, then stop.

---

## Letter B — asking only for redistribution rights

> Subject: Permission to redistribute the <DATASET> data under CC BY
>
> Dear Dr <NAME>,
>
> Your dataset <NAME / DOI> is deposited under <LICENCE>. I am including it in a
> reanalysis of published time-kill data, which the licence permits, and I have
> no commercial interest in the work.
>
> My difficulty is only with redistribution. The analysis repository that
> accompanies the manuscript is public and carries a CC BY licence for its own
> material, so that anyone can reproduce every number in the paper. A
> <NonCommercial / NoDerivatives> term cannot be carried into that repository,
> and I do not want to relicense your work or to quietly leave it out.
>
> Two ways forward, and either suits me:
>
> 1. You give written permission for this specific reuse — that I may include the
>    data, and a tidied form of it, in the public repository accompanying this
>    manuscript, with attribution to you and a note of the original licence. This
>    is a one-off permission and changes nothing about your deposit.
>
> 2. I keep your data out of the repository entirely and record only its
>    provenance and how to obtain it, so the analysis remains reproducible for
>    anyone who fetches it themselves. This is what I do by default, and it costs
>    a reader one extra download.
>
> If (1) is acceptable, a single line by email is enough. If I hear nothing, I
> will assume (2) and proceed on that basis.
>
> With thanks,
>
> Vahhab Piranfar
> ORCID 0000-0003-3653-5739

### Why (2) is offered

Because it is true, and because offering someone an easy way to say no is what
gets a considered yes. It also means no reply is not a blocker: the default is
already lawful and the corpus is not held up waiting.

---

## What to record when a reply arrives

Every answer goes in `data/manifests/permissions.csv`, including the refusals and
the silences. Three reasons: an unrecorded permission is worth nothing when a
journal asks for evidence of it two years later; a refusal has to be visible so
nobody re-requests it; and the response rate is itself worth reporting in the
paper if the corpus ever becomes a survey of reporting practice.

Keep the email itself. A line in a CSV is a note, not evidence.
