"""
One self-contained file to read the whole submission in.

Run:  python -m src.build_review_copy

WHY. The submission is two files and four separate figure images, which is the
right shape to upload and the wrong shape to read. Reviewing it means opening
the article, hunting for a supplementary table it cites, and opening a PNG in
another window to see what a legend is describing. Anything read that way gets
reviewed badly.

This builds one HTML document instead: the article, its figures placed at their
legends, then the supplement, with every table rendered and every line numbered
so a comment can name where it is. It opens in a browser and prints to PDF, and
nothing is fetched over the network -- the figures are embedded as data URIs, so
the file works from a memory stick with no internet and no missing images.

It is a READING copy and says so at the top. What gets submitted is the two
markdown files; this one exists to be marked up.

Writes manuscript/REVIEW_COPY.html
"""
from __future__ import annotations

import base64
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "manuscript" / "SUBMISSION_MAIN.md"
SUPP = ROOT / "manuscript" / "SUBMISSION_SUPPLEMENT.md"
FIGDIR = ROOT / "results" / "figures"
OUT = ROOT / "manuscript" / "REVIEW_COPY.html"

# Which image belongs to which figure number in the article. Taken from
# src/assemble_paper.py, which is the module that decides it.
FIGURES = {
    1: "fig1_dynamic_range",
    2: "fig2_rate_vs_duration",
    3: "fig3_endpoint_collapse",
    4: "fig4_independence",
}

# Supplemental figures, placed in the supplement half of the reading copy by the
# same routine. Keyed by the label as it appears in the legend, so "S1" builds
# the pattern "Figure S1." without a second regex.
SUPP_FIGURES = {
    "S1": "figS1_survival_and_cox",
}

CSS = """
:root { --ink:#1a1a1a; --dim:#666; --rule:#d8d8d8; --mark:#fffbe6; --bg:#fff; }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
       font:15px/1.65 Georgia,'Iowan Old Style',serif; }
.wrap { max-width: 46rem; margin: 0 auto; padding: 2rem 1.25rem 6rem; }
.banner { background:var(--mark); border:1px solid #e6d98a; border-radius:6px;
          padding:.9rem 1.1rem; margin-bottom:2rem;
          font:13px/1.55 ui-sans-serif,system-ui,sans-serif; color:#5a4c00; }
.banner b { display:block; margin-bottom:.3rem; font-size:14px; }
h1 { font-size:1.6rem; line-height:1.3; margin:2rem 0 .4rem; }
h2 { font-size:1.25rem; margin:2.6rem 0 .6rem; padding-top:.7rem;
     border-top:1px solid var(--rule); }
h3 { font-size:1.05rem; margin:1.8rem 0 .5rem; }
p { margin:0 0 1rem; }
code { font:13px ui-monospace,Menlo,Consolas,monospace; background:#f4f4f4;
       padding:.1em .35em; border-radius:3px; }
figure { margin:1.6rem 0; }
figure img { width:100%; height:auto; border:1px solid var(--rule);
             border-radius:4px; }
.tablewrap { overflow-x:auto; margin:0 0 1.4rem; }
table { border-collapse:collapse; width:100%;
        font:12.5px/1.45 ui-sans-serif,system-ui,sans-serif; }
th,td { border-bottom:1px solid var(--rule); padding:.42rem .55rem;
        text-align:left; vertical-align:top; }
th { border-bottom:1.5px solid #aaa; font-weight:600; white-space:nowrap; }
tr:hover td { background:#fafafa; }
.ln { color:#bbb; font:11px ui-monospace,monospace; user-select:none;
      float:left; margin-left:-3.2rem; width:2.6rem; text-align:right;
      padding-top:.28rem; }
.part { margin:4rem 0 0; padding:.8rem 0; border-top:3px double #999;
        border-bottom:3px double #999; text-align:center;
        font:600 13px ui-sans-serif,system-ui,sans-serif; letter-spacing:.08em;
        text-transform:uppercase; color:var(--dim); }
hr { border:0; border-top:1px solid var(--rule); margin:2rem 0; }
@media print {
  .banner { break-inside:avoid; }
  h2,h3 { break-after:avoid; }
  figure,table { break-inside:avoid; }
  .ln { display:none; }
  .wrap { max-width:none; padding:0; }
}
@media (max-width: 820px) { .ln { display:none; } }
"""


def md_to_html(text: str) -> str:
    """Markdown to HTML, with the extensions this manuscript actually uses."""
    try:
        import markdown
    except ImportError:
        raise SystemExit("this needs the markdown package: pip install markdown")
    return markdown.markdown(
        text, extensions=["tables", "attr_list", "sane_lists"],
        output_format="html5")


def strip_front_matter(text: str) -> str:
    """Drop the YAML block; its contents are shown in the banner instead."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            return text[end + 4:]
    return text


def embed_figures(html: str, figures=None) -> tuple[str, list]:
    """Put each figure above its own legend, as a data URI.

    Placing it above rather than below is deliberate: a legend read before the
    image it describes is read twice. Missing images are reported rather than
    silently skipped, because an absent figure in a review copy reads as a
    figure that does not exist.
    """
    missing = []
    for n, stem in (FIGURES if figures is None else figures).items():
        png = FIGDIR / f"{stem}.png"
        if not png.exists():
            missing.append(n)
            continue
        b64 = base64.b64encode(png.read_bytes()).decode("ascii")
        img = (f'<figure><img alt="Figure {n}" '
               f'src="data:image/png;base64,{b64}"></figure>')
        # The legend is a paragraph opening "<strong>Figure n." after markdown
        # has run. Anchor on that rather than on the raw text.
        pat = re.compile(rf"(<p><strong>(?:Fig\.|Figure) {n}\.)")
        html, k = pat.subn(img + r"\1", html, count=1)
        if not k:
            missing.append(n)
    return html, missing


def wrap_tables(html: str) -> str:
    """Let a wide table scroll inside itself rather than the page."""
    return (html.replace("<table>", '<div class="tablewrap"><table>')
                .replace("</table>", "</table></div>"))


def number_lines(html: str) -> str:
    """A number on every block, so a comment can say where it is."""
    out, n = [], 0
    for chunk in re.split(r"(<(?:p|h1|h2|h3|li)\b[^>]*>)", html):
        if re.match(r"<(?:p|h1|h2|h3|li)\b", chunk):
            n += 1
            out.append(chunk + f'<span class="ln">{n}</span>')
        else:
            out.append(chunk)
    return "".join(out)


def audit_line() -> str:
    """What the checkers say, run now rather than remembered."""
    try:
        r = subprocess.run([sys.executable, "-m", "src.audit_manuscript"],
                           cwd=ROOT, capture_output=True, text=True, timeout=300)
        tail = [x for x in r.stdout.splitlines() if "high," in x]
        return tail[-1].strip() if tail else "audit produced no summary line"
    except Exception as exc:                       # noqa: BLE001
        return f"audit not run ({type(exc).__name__})"


def main() -> int:
    for p in (MAIN, SUPP):
        if not p.exists():
            raise SystemExit(f"missing {p}; run src/build_submission.py first")

    main_md = strip_front_matter(MAIN.read_text(encoding="utf-8"))
    supp_md = SUPP.read_text(encoding="utf-8")

    m = re.search(r'^title:\s*"(.+)"\s*$',
                  MAIN.read_text(encoding="utf-8"), re.M)
    title = m.group(1) if m else "Manuscript"

    def words(md: str) -> int:
        md = re.split(r"^## References", md, maxsplit=1, flags=re.M)[0]
        return len(re.sub(r"^\|.*$", "", md, flags=re.M).split())

    body = md_to_html(main_md)
    body, missing = embed_figures(body)
    body = wrap_tables(number_lines(body))
    supp_html, supp_missing = embed_figures(md_to_html(supp_md), SUPP_FIGURES)
    missing = missing + supp_missing
    supp_html = wrap_tables(number_lines(supp_html))

    warn = ("" if not missing else
            f" <b>Figures {', '.join(str(x) for x in missing)} could not be "
            f"placed and are absent from this copy.</b>")

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Review copy — {title[:60]}</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="banner"><b>Reading copy for internal review — not the submission</b>
Built {date.today().isoformat()} from manuscript/SUBMISSION_MAIN.md and
manuscript/SUBMISSION_SUPPLEMENT.md, which are what would be uploaded. The
article and the supplemental file are printed here one after the other, with the
figures placed at their legends, so the whole thing can be read in one pass.
Numbers in the left margin are block numbers for marking up; they are not in the
submitted files and are hidden when printed.<br><br>
Article {words(main_md):,} words, {len(FIGURES)} figures,
{main_md.count(chr(10) + '**Table ')} tables &middot;
supplement {words(supp_md):,} words,
{supp_md.count(chr(10) + '**Table ')} tables,
{len(SUPP_FIGURES)} figure &middot;
target: <i>Journal of Microbiological Methods</i> &middot;
manuscript audit: {audit_line()}.{warn}</div>
<div class="part">Article</div>
{body}
<div class="part">Supplemental material</div>
{supp_html}
</div></body></html>"""

    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(html)/1e6:.1f} MB)")
    print(f"   article {words(main_md):,} words, supplement {words(supp_md):,}")
    if missing:
        print(f"   FIGURES NOT PLACED: {missing}")
        return 1
    print(f"   all {len(FIGURES)} article figures and "
          f"{len(SUPP_FIGURES)} supplemental figure embedded")
    pdf = to_pdf()
    print(f"   {pdf}")
    return 0


def to_pdf() -> str:
    """Print the HTML to PDF with whichever Chromium is installed.

    Neither pandoc nor weasyprint is available here, and installing a LaTeX
    toolchain to read a draft is a poor trade. Edge and Chrome both ship a
    headless printer that renders the same CSS the browser would, including the
    print rules above, so the PDF and the on-screen copy cannot disagree.
    Failure is reported, not raised: the HTML is the deliverable and the PDF is
    a convenience.
    """
    out = OUT.with_suffix(".pdf")
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    exe = next((c for c in candidates if c.exists()), None)
    if exe is None:
        return "no Chromium found; open the HTML and print to PDF yourself"
    try:
        subprocess.run(
            [str(exe), "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={out}", OUT.as_uri()],
            check=True, capture_output=True, timeout=180)
    except Exception as exc:                       # noqa: BLE001
        return f"PDF not produced ({type(exc).__name__}); the HTML is complete"
    if not out.exists():
        return "PDF not produced; the HTML is complete"
    return f"and {out.relative_to(ROOT)} ({out.stat().st_size/1e6:.1f} MB)"


if __name__ == "__main__":
    sys.exit(main())
