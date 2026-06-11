# /// script
# dependencies = ["markdown"]
# ///
"""Render the project's markdown documents into a static site under site/.

Run: uv run build_site.py
"""
import pathlib
import re
import shutil

import markdown

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "site"

PAGES = [
    "NARRATIVES.md",
    "REPORT.md",
    "survey2/COMPARISON.md",
    "survey/question.md",
    "survey2/question.md",
    *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "survey" / "responses").glob("*.md")),
    *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "survey2" / "responses").glob("*.md")),
]

CSS = """
:root { --fg: #1a1a1a; --bg: #ffffff; --muted: #57606a; --accent: #0b5fa5;
        --card: #f6f8fa; --border: #d8dee4; }
@media (prefers-color-scheme: dark) {
  :root { --fg: #e6e6e6; --bg: #14161a; --muted: #9aa4af; --accent: #6cb6ff;
          --card: #1d2127; --border: #343a42; }
}
* { box-sizing: border-box; }
body { margin: 0; color: var(--fg); background: var(--bg);
       font: 17px/1.65 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 52rem; margin: 0 auto; padding: 1.5rem 1.2rem 4rem; }
nav.top { border-bottom: 1px solid var(--border); background: var(--card);
          font-size: 0.92rem; }
nav.top div { max-width: 52rem; margin: 0 auto; padding: 0.6rem 1.2rem;
              display: flex; gap: 1.2rem; flex-wrap: wrap; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3 { line-height: 1.25; margin-top: 2rem; }
h1 { font-size: 1.7rem; }
img { max-width: 100%; height: auto; border: 1px solid var(--border);
      border-radius: 8px; }
table { border-collapse: collapse; display: block; overflow-x: auto;
        font-size: 0.9rem; }
th, td { border: 1px solid var(--border); padding: 0.35rem 0.6rem; }
th { background: var(--card); }
code { background: var(--card); padding: 0.1rem 0.35rem; border-radius: 4px;
       font-size: 0.88em; }
pre { background: var(--card); padding: 0.9rem; border-radius: 8px;
      overflow-x: auto; }
pre code { padding: 0; background: none; }
blockquote { margin: 0; padding: 0.1rem 1rem; border-left: 3px solid var(--accent);
             color: var(--muted); }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
         gap: 1rem; margin: 1.5rem 0; }
.card { background: var(--card); border: 1px solid var(--border);
        border-radius: 10px; padding: 1rem 1.2rem; }
.card h3 { margin: 0 0 0.4rem; }
.card p { margin: 0; color: var(--muted); font-size: 0.92rem; }
footer { color: var(--muted); font-size: 0.85rem; margin-top: 3rem;
         border-top: 1px solid var(--border); padding-top: 1rem; }
"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{rel}style.css">
</head>
<body>
<nav class="top"><div>
<a href="{rel}index.html">Home</a>
<a href="{rel}NARRATIVES.html">Narratives</a>
<a href="{rel}REPORT.html">Report</a>
<a href="{rel}survey2/COMPARISON.html">Debiased survey</a>
<a href="https://github.com/m1el/ai-econ-sim">Source</a>
</div></nav>
<main>
{body}
<footer>Generated from an 11-model LLM survey and a calibrated simulation.
Models surveyed via OpenRouter; site built from markdown by build_site.py.</footer>
</main>
</body>
</html>
"""

INDEX_BODY = """
<h1>What happens to the median person under advanced AI?</h1>
<p>One person's attempt to plan their life: 10 frontier LLMs surveyed twice
(once with a framed prompt, once debiased), plus an 11th fresh-context model,
plus a small macroeconomic simulator calibrated so its statistics match the
panel's collective forecasts.</p>

<div class="cards">
<div class="card"><h3><a href="NARRATIVES.html">Four futures</a></h3>
<p>The main deliverable: four narratives with graphs and the observable
signposts that tell you which path you're on.</p></div>

<div class="card"><h3><a href="survey2/COMPARISON.html">The debiased survey</a></h3>
<p>11 models, neutral instrument, calibrated probability estimates — and a
measurement of how much prompt framing skewed the first survey.</p></div>

<div class="card"><h3><a href="REPORT.html">Full report (survey 1)</a></h3>
<p>The original synthesis: what the models think, key parameters, the four
most compelling causal stories, simulation v1.</p></div>

<div class="card"><h3><a href="https://github.com/m1el/ai-econ-sim">Simulator code</a></h3>
<p><code>model/simulate_v2.py</code> — task-based automation model with
political feedback, calibrated to the panel. <code>uv run</code> it.</p></div>
</div>

<h2>The single most useful picture</h2>
<p>The most likely path (~35%): the economy more than triples while the median
person's welfare crawls. Watch the gap between the gray and green lines.</p>
<p><a href="NARRATIVES.html"><img src="model/narrative_B_institutional_lag.png"
alt="Institutional lag scenario"></a></p>

<h2>Raw survey responses</h2>
<p>Survey 2 (neutral): {s2_links}</p>
<p>Survey 1 (framed): {s1_links}</p>
<p>Instruments: <a href="survey/question.html">survey 1</a> ·
<a href="survey2/question.html">survey 2</a></p>
"""


LIST_ITEM = re.compile(r"^\s*([-*+]|\d+\.)\s")


def ensure_blank_before_lists(text: str) -> str:
    """Python-Markdown needs a blank line before a list; GFM doesn't.

    Insert one when a list item directly follows a non-blank, non-list line
    (skipping fenced code blocks).
    """
    out, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if (not in_fence and LIST_ITEM.match(line) and out
                and out[-1].strip() and not LIST_ITEM.match(out[-1])):
            out.append("")
        out.append(line)
    return "\n".join(out)


def render(md_text: str, depth: int, title: str) -> str:
    md_text = ensure_blank_before_lists(md_text)
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])
    return TEMPLATE.format(title=title, body=body, rel="../" * depth)


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / "style.css").write_text(CSS)

    # images referenced by the pages
    (SITE / "model").mkdir()
    for png in (ROOT / "model").glob("*.png"):
        shutil.copy(png, SITE / "model" / png.name)

    for rel in PAGES:
        src = ROOT / rel
        text = src.read_text()
        # intra-site links: point .md references at the rendered .html
        text = re.sub(r"\(((?:[\w./-]+)?[\w-]+)\.md\)", r"(\1.html)", text)
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = m.group(1) if m else src.stem
        out = SITE / pathlib.Path(rel).with_suffix(".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        depth = len(pathlib.Path(rel).parents) - 1
        out.write_text(render(text, depth, title))
        print(f"  {rel} -> {out.relative_to(ROOT)}")

    def links(d):
        return " · ".join(
            f'<a href="{d}/responses/{p.stem}.html">{p.stem.split("_")[0]}</a>'
            for p in sorted((ROOT / d / "responses").glob("*.md")))

    index = TEMPLATE.format(
        title="AI economy scenarios",
        body=INDEX_BODY.format(s1_links=links("survey"), s2_links=links("survey2")),
        rel="")
    (SITE / "index.html").write_text(index)
    print(f"  index.html\nSite built in {SITE}")


if __name__ == "__main__":
    main()
