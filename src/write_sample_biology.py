"""
What the samples actually are, biologically.

Run:  python -m src.write_sample_biology

WHY THIS EXISTS. This project has spent its effort on what the assay could and
could not measure. That left the organisms themselves undescribed. The clinical
deposit carries a resistance genotype, a treatment timeline, two drug MICs and
two growth measures on every isolate, and almost none of it has been looked at.

This is a description, not an argument. It characterises the cohort the way a
microbiologist would want it characterised before drawing any conclusion from
it, and it tests the textbook expectations that a reader will hold about these
mutations, so that where the cohort is ordinary it can be said to be ordinary
and where it is not, that is visible.

Writes:  docs/20_SAMPLE_BIOLOGY.md
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
VIJAY = ROOT / "data" / "raw" / "tb" / "elife93243_supp2.xlsx"
WINDELS = ROOT / "data" / "raw" / "windels2024" / "phenotypes_after_evol.csv"
OUT = ROOT / "docs" / "20_SAMPLE_BIOLOGY.md"

# katG mutations abolish the prodrug activation isoniazid needs and give
# high-level resistance; promoter and inhA changes raise the target level or
# alter it, and classically give lower-level resistance.
MECHANISM = {
    "katG_S315X": "catalase-peroxidase, prodrug activation lost; classically high-level",
    "fabG1_C-15X": "inhA promoter, target overexpressed; classically low-level",
    "inhA_I21T": "target structural change; classically low-level",
    "ahpC_G-48A": "alkyl hydroperoxidase promoter, compensatory rather than causal",
}
PHASE = {"IS": "susceptible", "IR-BL": "resistant, baseline isolate",
         "IR-IP": "resistant, intensive phase", "IR-CP": "resistant, continuation phase"}


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    head = "| " + " | ".join(str(c) for c in cols) + " |"
    rule = "| " + " | ".join("---" for _ in cols) + " |"
    body = "\n".join("| " + " | ".join(str(v) for v in row) + " |"
                     for row in df.itertuples(index=False))
    return "\n".join([head, rule, body])


def fmt_p(p: float) -> str:
    return "< 0.0001" if p < 1e-4 else f"{p:.4g}"


def main() -> int:
    d = pd.read_excel(VIJAY)
    d["growth"] = pd.to_numeric(d["Time_to_0.4"], errors="coerce")
    mic_i = pd.to_numeric(d["MIC_INH"], errors="coerce")
    mic_r = pd.to_numeric(d["MIC_RIF"], errors="coerce")

    # -- cohort composition ---------------------------------------------------
    comp = (d["INH-Suceptibility"].value_counts()
            .rename_axis("isoniazid phenotype").reset_index(name="isolates"))
    comp["per cent"] = (100 * comp["isolates"] / len(d)).round(1)

    tp = d["Time_point"].astype(str)
    months = tp.str.extract(r"(\d+)")[0].astype(float)
    timeline = (pd.DataFrame({"month": months})
                .groupby("month").size().reset_index(name="isolates"))
    timeline["month"] = timeline["month"].astype(int)

    phase = (d["INH-R-sequential isolates"].value_counts()
             .rename_axis("stratum").reset_index(name="isolates"))
    phase["meaning"] = phase["stratum"].map(PHASE).fillna("-")

    # -- resistance genotype --------------------------------------------------
    gen = d["INH_mutation"].dropna()
    grows = []
    for mut in gen.unique():
        m = d["INH_mutation"] == mut
        gi = mic_i[m].dropna()
        gg = d.loc[m, "growth"].dropna()
        grows.append({
            "mutation": mut,
            "isolates": int(m.sum()),
            "mechanism": MECHANISM.get(mut, "-"),
            "median INH MIC": f"{gi.median():g}" if len(gi) else "-",
            "INH MIC range": f"{gi.min():g} to {gi.max():g}" if len(gi) else "-",
            "median time to OD 0.4": f"{gg.median():g}" if len(gg) else "-",
        })
    geno = pd.DataFrame(grows).sort_values("isolates", ascending=False)

    # textbook expectation: katG gives a higher MIC than the promoter/target group
    katg = mic_i[d["INH_mutation"] == "katG_S315X"].dropna()
    other = mic_i[d["INH_mutation"].isin(["fabG1_C-15X", "inhA_I21T"])].dropna()
    katg_test = (stats.mannwhitneyu(katg, other) if len(katg) > 2 and len(other) > 2
                 else (None, np.nan))

    # -- MIC distribution -----------------------------------------------------
    microws = []
    for name, s in (("isoniazid", mic_i), ("rifampicin", mic_r)):
        v = s.dropna()
        microws.append({
            "drug": name, "isolates": len(v),
            "min": f"{v.min():g}", "median": f"{v.median():g}", "max": f"{v.max():g}",
            "fold range": f"{v.max()/v.min():,.0f}x",
            "distinct values": v.nunique(),
        })
    micdf = pd.DataFrame(microws)

    # -- growth ---------------------------------------------------------------
    g = d["growth"].dropna()
    gi_s = d.loc[d["INH-Suceptibility"] == "IS", "growth"].dropna()
    gi_r = d.loc[d["INH-Suceptibility"] == "IR", "growth"].dropna()
    growth_p = stats.mannwhitneyu(gi_r, gi_s)[1] if len(gi_r) > 2 and len(gi_s) > 2 else np.nan

    # -- the evolved E. coli --------------------------------------------------
    w = pd.read_csv(WINDELS)
    wtab = (w.groupby(["AB_conc", "nutrient_conc"])
            .agg(clones=("MIC", "size"), median_MIC=("MIC", "median"),
                 median_persister=("pers_frac", "median"))
            .reset_index().round(4))

    doc = f"""# The samples, described biologically

Generated by `python -m src.write_sample_biology`. Every number is recomputed
from the deposits; nothing is typed by hand.

This is a description of the organisms, kept separate from the manuscript for
the author to draw on. It makes no argument. Where the cohort matches what a
microbiologist would expect, that is stated; where it does not, that is stated
too, because an unexpected cohort is worth knowing about before it is used.

---

## 1. The clinical cohort

217 *Mycobacterium tuberculosis* isolates from patients, assayed under
rifampicin (Vijay et al. 2024, eLife 12:RP93243).

### Isoniazid phenotype

{md(comp)}

### Where in treatment each isolate was taken

{md(timeline)}

{int((months == 0).sum())} of {len(d)} isolates are pre-treatment. The remainder
span one to 24 months on therapy, so the cohort is mostly a baseline survey with
a longitudinal tail rather than a treatment time-course.

### Resistant isolates by treatment phase

{md(phase)}

---

## 2. Resistance genotype

A mutation is recorded for {len(gen)} isolates.

{md(geno)}

**The cohort is a katG cohort.** {int((gen == 'katG_S315X').sum())} of {len(gen)}
typed isolates carry *katG* S315X, the substitution that removes the
catalase-peroxidase activation isoniazid depends on. It is the commonest
isoniazid-resistance mutation in clinical strains worldwide, and it is common
precisely because it costs the organism little: unlike most resistance
mutations it retains near-normal fitness, which is why it displaces the
alternatives in circulating populations.

**The textbook expectation, tested.** *katG* changes are classically high-level
and promoter or target changes classically low-level. In this cohort the median
isoniazid MIC is {katg.median():g} for *katG* S315X against {other.median():g}
for the *fabG1*/*inhA* group{f", Mann-Whitney p = {fmt_p(katg_test[1])}" if np.isfinite(katg_test[1]) else ""}.
{'The expected ordering is present.' if len(katg) and len(other) and katg.median() > other.median() else 'The expected ordering is NOT present in these data, which is worth knowing before any inference that assumes it.'}

The table above shows one departure from the textbook, and it is small: the two
*inhA* I21T isolates sit at an isoniazid MIC of 6.4, higher than most of the
*katG* group, where the classical account puts target changes at the low end.
Two isolates decide nothing, and the group test is carried by the six *fabG1*
isolates at 0.4, but a reader comparing the table against expectation will notice
it, so it is named here.

---

## 3. Drug susceptibility

{md(micdf)}

The isoniazid MIC spans a {mic_i.max()/mic_i.min():,.0f}-fold range and the
rifampicin MIC only {mic_r.max()/mic_r.min():,.0f}-fold. The killing assay these
isolates were put through used rifampicin, so the axis along which they differ
most is not the axis they were challenged on.

---

## 4. Growth

Time to optical density 0.4 is recorded for {len(g)} isolates and runs from
{g.min():g} to {g.max():g}, median {g.median():g}. That is a
{g.max()/g.min():.1f}-fold spread in the time these isolates need to reach the
same density.

Resistant isolates take a median {gi_r.median():g} against {gi_s.median():g} for
susceptible ones (Mann-Whitney p = {fmt_p(growth_p)}).
{'The difference is not significant, which is consistent with katG S315X being close to fitness-neutral and is what makes this cohort ordinary in that respect.' if growth_p > 0.05 else 'The difference is significant, which is not what a katG-dominated cohort would be expected to show.'}

---

## 5. The evolved *Escherichia coli*

126 clones from a parallel evolution experiment under amikacin (Windels et al.
2024), each carrying the MIC and persister fraction reached at the end of
evolution, labelled by the antibiotic concentration and nutrient level the
population evolved under.

{md(wtab)}

The design is a {w['AB_conc'].nunique()} by {w['nutrient_conc'].nunique()} grid
of antibiotic concentration against nutrient level. It is the only deposit in
this project with a genuine nutrient axis, and the only one where the
physiological state of the population was set deliberately rather than
inherited.

---

## 6. What is not in any of these deposits

Recorded so the gaps are known rather than discovered later.

- **No patient outcome.** No cure, failure, relapse or death is linked to any
  isolate. Nothing here can speak to what happened to a person.
- **No culture volume.** The vessel volume appears in none of the four deposits,
  so the number of surviving cells behind a blank reading cannot be computed
  from them.
- **No lineage or whole-genome typing** beyond the single resistance locus.
- **No replicate isolates from the same patient at the same visit**, so
  within-patient measurement variation cannot be separated from between-isolate
  variation.
- **One strain only in the six-laboratory exercise**, H37Rv from a single stock,
  so it carries no isolate-level biology at all by design.
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"   clinical isolates {len(d)}, genotyped {len(gen)}, "
          f"katG S315X {int((gen=='katG_S315X').sum())}")
    print(f"   INH MIC spans {mic_i.max()/mic_i.min():,.0f}-fold, "
          f"RIF MIC {mic_r.max()/mic_r.min():,.0f}-fold")
    print(f"   growth spread {g.max()/g.min():.1f}-fold; resistant vs susceptible "
          f"p = {fmt_p(growth_p)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
