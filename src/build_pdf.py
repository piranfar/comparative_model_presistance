"""Render manuscript/PAPER_COMPLETE.md to a self-contained reading PDF.

No LaTeX and no pandoc: the assembled Markdown is converted to a single HTML
file with every figure inlined as a data URI, and Chrome's headless printer is
asked for the PDF. The point is a clean read-through copy, not a typeset
submission — the journal will impose its own template.
"""
from __future__ import annotations

import base64
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "manuscript" / "PAPER_COMPLETE.md"
BUILD = ROOT / "build"
HTML_OUT = BUILD / "PAPER_COMPLETE.html"
PDF_OUT = BUILD / "PAPER_COMPLETE.pdf"

CHROME_CANDIDATES = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
)

CSS = """
@page { size: A4; margin: 22mm 20mm 20mm 20mm; }
@page { @bottom-center { content: counter(page); } }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Charter", "Georgia", "Cambria", serif;
  font-size: 10.5pt; line-height: 1.52; color: #14181d;
  margin: 0; hyphens: auto; text-align: justify;
}

/* ---- title block ---------------------------------------------------- */
.titleblock { border-bottom: 1.5px solid #14181d; padding-bottom: 14px; margin-bottom: 22px; }
.titleblock h1 {
  font-size: 19pt; line-height: 1.24; margin: 0 0 10px 0;
  font-weight: 600; text-align: left; letter-spacing: -0.1px;
}
.meta { font-size: 9pt; color: #4a545f; line-height: 1.7; text-align: left; }
.meta .status {
  display: inline-block; margin-top: 6px; padding: 2px 8px;
  border: 1px solid #c2c9d1; border-radius: 3px; background: #f4f6f8;
  font-family: "Segoe UI", system-ui, sans-serif; font-size: 8pt; color: #45505c;
}

/* ---- headings ------------------------------------------------------- */
h2, h3, h4 {
  font-family: "Segoe UI Semibold", "Helvetica Neue", system-ui, sans-serif;
  text-align: left; break-after: avoid-page; page-break-after: avoid;
  color: #0d1116;
}
h2 {
  font-size: 13pt; margin: 26px 0 10px; padding-bottom: 4px;
  border-bottom: 0.75px solid #ccd3da; letter-spacing: 0.2px;
}
h3 { font-size: 11pt; margin: 19px 0 7px; }
h4 { font-size: 10pt; margin: 15px 0 5px; font-style: italic; font-weight: 600; }

p { margin: 0 0 9px; orphans: 3; widows: 3; }

/* ---- tables --------------------------------------------------------- */
table {
  border-collapse: collapse; width: 100%; margin: 4px 0 18px;
  font-family: "Segoe UI", system-ui, sans-serif; font-size: 8.2pt;
  break-inside: avoid-page; page-break-inside: avoid; text-align: left;
}
thead th {
  border-top: 1px solid #14181d; border-bottom: 0.75px solid #14181d;
  padding: 5px 7px; font-weight: 600; vertical-align: bottom; background: #fafbfc;
}
tbody td { border-bottom: 0.4px solid #dde2e7; padding: 4px 7px; vertical-align: top; }
tbody tr:last-child td { border-bottom: 1px solid #14181d; }

/* a caption is the bold paragraph immediately before its table */
p > strong:first-child { font-family: "Segoe UI", system-ui, sans-serif; }
p.caption {
  font-family: "Segoe UI", system-ui, sans-serif; font-size: 8.6pt;
  line-height: 1.45; color: #2b333c; margin: 20px 0 0;
  break-after: avoid-page; page-break-after: avoid; text-align: left;
}

/* ---- figures -------------------------------------------------------- */
img {
  display: block; max-width: 100%; height: auto; margin: 16px auto 6px;
  break-inside: avoid-page; page-break-inside: avoid;
}
.figure { break-inside: avoid-page; page-break-inside: avoid; margin-bottom: 22px; }

/* ---- misc ----------------------------------------------------------- */
hr { border: none; border-top: 0.5px solid #dde2e7; margin: 24px 0; }
code { font-family: "Consolas", monospace; font-size: 9pt; background: #f4f6f8; padding: 0 3px; }
em { font-style: italic; }
sup { font-size: 0.72em; vertical-align: super; line-height: 0; }
a { color: inherit; text-decoration: none; }
ul, ol { margin: 0 0 9px; padding-left: 22px; }
li { margin-bottom: 4px; }
blockquote {
  margin: 10px 0; padding-left: 12px; border-left: 2px solid #ccd3da; color: #45505c;
}
h2#abstract + p { font-size: 10.5pt; }

.display {
  margin: 9px 0 11px; padding-left: 26px; text-align: left;
  break-inside: avoid-page; page-break-inside: avoid;
}
pre {
  margin: 10px 0 12px; padding-left: 26px; text-align: left;
  break-inside: avoid-page; page-break-inside: avoid;
}
pre code {
  background: none; padding: 0; font-family: "Consolas", monospace; font-size: 9.2pt;
}
"""


def strip_front_matter(text: str) -> tuple[dict, str]:
    """Pull the YAML block off the top without a YAML dependency."""
    meta: dict[str, str] = {}
    if not text.startswith("---"):
        return meta, text
    end = text.index("\n---", 3)
    for line in text[3:end].splitlines():
        m = re.match(r"^(\w+):\s*\"?(.*?)\"?$", line.strip())
        if m and m.group(2):
            meta[m.group(1)] = m.group(2)
    return meta, text[end + 4:].lstrip("\n")


def inline_images(html: str) -> tuple[str, int]:
    """Replace every <img src> with a base64 data URI so the file stands alone."""
    n = 0

    def sub(m: re.Match) -> str:
        nonlocal n
        src = m.group(1)
        path = (ROOT / "manuscript" / src).resolve()
        if not path.exists():
            print(f"   ! missing figure: {src}", file=sys.stderr)
            return m.group(0)
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        n += 1
        return f'src="data:image/png;base64,{data}"'

    return re.sub(r'src="([^"]+)"', sub, html), n


def display_lines(text: str) -> tuple[str, int]:
    """Set the indented definition lines as displayed equations.

    Markdown folds a two-space indent back into the preceding paragraph, which
    runs the boundary definitions together mid-sentence. They are indented in
    the source because they are displayed, so honour that.
    """
    out, n = [], 0
    for line in text.split("\n"):
        m = re.match(r"^ {2,3}(?=\S)", line)
        if m:
            out.append(f'<div class="display" markdown="1">{line.strip()}</div>')
            n += 1
        else:
            out.append(line)
    return "\n".join(out), n


def superscripts(text: str) -> str:
    """10^*q* and 10^Δ*h* are exponents; render them as such."""
    text = re.sub(r"\^(Δ?)\*([^*\n]+)\*", r"<sup>\1*\2*</sup>", text)
    assert "^" not in text, "an exponent was not converted"
    return text


def mark_captions(html: str) -> str:
    """Tag caption paragraphs so they stay with their table or figure."""
    return re.sub(
        r"<p>(<strong>(?:Table|Figure) [^<]*</strong>)",
        r'<p class="caption">\1',
        html,
    )


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    return shutil.which("chrome") or shutil.which("msedge")


def main() -> int:
    if not SRC.exists():
        print(f"missing {SRC}; run src/assemble_paper.py first", file=sys.stderr)
        return 1
    BUILD.mkdir(exist_ok=True)

    meta, body = strip_front_matter(SRC.read_text(encoding="utf-8"))
    body, n_disp = display_lines(body)
    body = superscripts(body)

    # The H1 and the byline block become a designed title block instead.
    lines = body.split("\n")
    start = next(i for i, L in enumerate(lines) if L.startswith("## Abstract"))
    head, body = lines[:start], "\n".join(lines[start:])
    title = next((L[2:].strip() for L in head if L.startswith("# ")), meta.get("title", ""))
    meta_lines = [L.strip() for L in head if L.startswith("**")]

    inner = markdown.markdown(
        body, extensions=["tables", "attr_list", "sane_lists", "md_in_html"]
    )
    inner = mark_captions(inner)
    inner, n_img = inline_images(inner)

    meta_html = "<br>".join(
        markdown.markdown(L).removeprefix("<p>").removesuffix("</p>") for L in meta_lines
    )
    status = meta.get("status", "")
    status_html = f'<div class="status">{status}</div>' if status else ""

    page = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title><style>{CSS}</style></head><body>"
        f'<div class="titleblock"><h1>{title}</h1>'
        f'<div class="meta">{meta_html}{status_html}</div></div>'
        f"{inner}</body></html>"
    )
    HTML_OUT.write_text(page, encoding="utf-8")
    print(f"wrote {HTML_OUT.relative_to(ROOT)}  "
          f"({n_img} figures inlined, {n_disp} displayed equations)")

    chrome = find_chrome()
    if chrome is None:
        print("no Chrome or Edge found; HTML written, PDF skipped", file=sys.stderr)
        return 1
    if PDF_OUT.exists():
        PDF_OUT.unlink()
    cmd = [
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=20000",
        f"--print-to-pdf={PDF_OUT}", HTML_OUT.as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not PDF_OUT.exists():
        print(r.stderr[-2000:], file=sys.stderr)
        return 1
    print(f"wrote {PDF_OUT.relative_to(ROOT)}  ({PDF_OUT.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
