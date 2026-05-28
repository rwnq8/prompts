#!/usr/bin/env python3
"""
render-papers.py -- Convert Obsidian papers to HTML via Pandoc

Uses Pandoc (standard markdown→HTML converter) for ALL formatting:
  - Tables, fenced code, footnotes, blockquotes, nested lists
  - Math: $...$ inline and $$...$$ display (Pandoc normalizes to \(\) and \[\])
  - YAML frontmatter extracted separately in Python

Pandoc handles the hard stuff. This script handles:
  - Frontmatter extraction
  - HTML template wrapping (JSON-LD, MathJax, nav, QNFO license)
  - Catalog generation

Usage:
  python tools/render-papers.py
  python tools/render-papers.py --dry-run
"""

import os
import sys
import json
import hashlib
import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime, timezone

# --- Paths ------------------------------------------------------------------
OBSIDIAN_RELEASES = Path(r"G:\My Drive\Obsidian\releases")
QWAV_PAPERS = Path(r"G:\My Drive\QWAV\papers")
PROMPTS_ROOT = Path(r"G:\My Drive\prompts")
SITE_URL = "https://deep.qwav.tech"

# --- HTML Template ----------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ | QWAV</title>
<meta name="description" content="__DESCRIPTION__">
<meta name="robots" content="index, follow">
<link rel="canonical" href="__CANONICAL_URL__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESCRIPTION__">
<meta property="og:type" content="article">
<meta property="og:url" content="__CANONICAL_URL__">
<meta name="twitter:card" content="summary">
<!-- Schema.org JSON-LD -->
<script type="application/ld+json">
__JSONLD__
</script>
<!-- MathJax v3 — renders LaTeX math from Pandoc output -->
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
  :root {{
    --bg: #0d1117; --fg: #c9d1d9; --link: #58a6ff;
    --border: #30363d; --code-bg: #161b22;
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg); color: var(--fg);
    max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem 4rem;
    line-height: 1.7; font-size: 16px;
  }}
  .nav {{
    display: flex; gap: 1.5rem; padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border); margin-bottom: 2rem;
    font-size: 0.95rem;
  }}
  .nav a {{ color: var(--link); text-decoration: none; }}
  .nav a:hover {{ text-decoration: underline; }}
  h1, h2, h3, h4, h5, h6 {{
    color: #f0f6fc; margin-top: 2rem; margin-bottom: 0.75rem;
    line-height: 1.3; font-weight: 600;
  }}
  h1 {{ font-size: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
  h2 {{ font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }}
  h3 {{ font-size: 1.25rem; }}
  a {{ color: var(--link); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  code {{
    background: var(--code-bg); padding: 0.2em 0.4em;
    border-radius: 3px; font-size: 0.9em; font-family: 'Consolas', 'Monaco', monospace;
  }}
  pre {{
    background: var(--code-bg); padding: 1rem; border-radius: 6px;
    overflow-x: auto; border: 1px solid var(--border);
    font-size: 0.9em; line-height: 1.5;
  }}
  pre code {{ background: none; padding: 0; }}
  table {{
    border-collapse: collapse; width: 100%; margin: 1.5rem 0;
  }}
  th, td {{
    border: 1px solid var(--border); padding: 0.5rem 0.75rem;
    text-align: left;
  }}
  th {{ background: var(--code-bg); font-weight: 600; }}
  blockquote {{
    border-left: 3px solid var(--link); margin: 1rem 0;
    padding: 0.5rem 1rem; color: #8b949e; background: var(--code-bg);
    border-radius: 0 6px 6px 0;
  }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
  img {{ max-width: 100%; border-radius: 6px; }}
  /* MathJax display math centering */
  .math.display {{ display: block; text-align: center; margin: 1.5rem 0; overflow-x: auto; }}
  .math.inline {{ display: inline; }}
  /* License footer */
  .license-notice {{
    margin-top: 3rem; padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    font-size: 0.85rem; color: #8b949e;
  }}
  .license-notice a {{ color: #8b949e; }}
  /* Responsive */
  @media (max-width: 600px) {{
    body {{ padding: 1rem; font-size: 15px; }}
    h1 {{ font-size: 1.5rem; }}
    pre {{ font-size: 0.8em; }}
  }}
</style>
</head>
<body>
<div class="nav">
  <a href="__SITE_URL__/">Home</a>
  <a href="__SITE_URL__/papers/">All Papers</a>
  <a href="https://github.com/qnfo">GitHub</a>
</div>
<article>
__PANDOC_BODY__
</article>
<footer class="license-notice">
  <p>This work is licensed under the
    <a href="https://github.com/QNFO/license" rel="license">QNFO Content License Agreement v1.1</a>
    by Rowan Brad Quni-Gudzinas (ORCID:
    <a href="https://orcid.org/0009-0002-4317-5604">0009-0002-4317-5604</a>).
    <strong>Non-commercial use only.</strong> Attribution required. Patent prior art citation required (§4.2).
  </p>
</footer>
</body>
</html>"""

CATALOG_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QWAV Publications Catalog</title>
<meta name="description" content="QWAV Research Publications — __COUNT__ papers on ultrametric quantum computing, geometric physics, and AI">
<meta name="robots" content="index, follow">
<link rel="canonical" href="__SITE_URL__/papers/">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
  :root {{
    --bg: #0d1117; --fg: #c9d1d9; --link: #58a6ff;
    --border: #30363d; --code-bg: #161b22;
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg); color: var(--fg);
    max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem 4rem;
    line-height: 1.7;
  }}
  .nav {{
    display: flex; gap: 1.5rem; padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border); margin-bottom: 2rem;
  }}
  .nav a {{ color: var(--link); text-decoration: none; }}
  h1 {{ color: #f0f6fc; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
  input[type="search"] {{
    width: 100%; padding: 0.75rem 1rem; font-size: 1rem;
    background: #0d1117; color: #c9d1d9;
    border: 1px solid #30363d; border-radius: 6px;
    margin: 1.5rem 0;
  }}
  input[type="search"]:focus {{ outline: none; border-color: #58a6ff; }}
  .paper-card {{
    border: 1px solid var(--border); border-radius: 8px;
    padding: 1.25rem; margin-bottom: 1rem;
    transition: border-color 0.15s;
  }}
  .paper-card:hover {{ border-color: #58a6ff; }}
  .paper-title {{ font-size: 1.15rem; margin: 0 0 0.5rem; }}
  .paper-title a {{ color: var(--link); font-weight: 600; }}
  .paper-meta {{ font-size: 0.85rem; color: #8b949e; }}
  .paper-topics {{ margin-top: 0.5rem; }}
  .paper-topic {{
    display: inline-block; background: var(--code-bg);
    color: #8b949e; padding: 0.15em 0.5em; border-radius: 3px;
    font-size: 0.8rem; margin: 0.15rem;
  }}
  .no-results {{ text-align: center; color: #8b949e; padding: 2rem; display: none; }}
</style>
</head>
<body>
<div class="nav">
  <a href="__SITE_URL__/">Home</a>
  <a href="__SITE_URL__/papers/">Papers</a>
  <a href="https://github.com/qnfo">GitHub</a>
</div>
<h1>QWAV Publications Catalog</h1>
<p>__COUNT__ papers. Click to read. Search to filter by title or topic.</p>
<input type="search" id="search" placeholder="Search papers..." oninput="filterPapers()">
<p class="no-results" id="no-results">No papers match your search.</p>
<div id="paper-list">
__PAPER_CARDS__
</div>
<script>
function filterPapers() {{
  const q = document.getElementById('search').value.toLowerCase();
  const cards = document.querySelectorAll('.paper-card');
  let visible = 0;
  cards.forEach(card => {{
    const text = card.textContent.toLowerCase();
    const match = !q || text.includes(q);
    card.style.display = match ? '' : 'none';
    if (match) visible++;
  }});
  document.getElementById('no-results').style.display = visible ? 'none' : 'block';
}}
</script>
</body>
</html>"""

PAPER_CARD = """<div class="paper-card">
  <p class="paper-title"><a href="__SITE_URL__/papers/__SLUG__">__TITLE__</a></p>
  <p class="paper-meta">__DATE__</p>
  <p class="paper-topics">__TOPICS__</p>
</div>"""


# =========================================================================
# HELPERS
# =========================================================================

def extract_frontmatter(text):
    """Extract YAML frontmatter and body from markdown text."""
    fm = {}
    body = text
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split('\n'):
                line = line.strip()
                if ':' in line:
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip()
            body = parts[2].strip()
    return fm, body


def pandoc_convert(body_text):
    """Convert markdown body to HTML5 via Pandoc."""
    result = subprocess.run(
        ['pandoc', '-f', 'markdown-yaml_metadata_block', '-t', 'html5', '--mathjax'],
        input=body_text,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    if result.returncode != 0:
        print(f"  [WARN] Pandoc error: {result.stderr[:200]}")
    return result.stdout


def extract_title(body_text):
    """Extract first h1 heading from markdown body."""
    m = re.search(r'^#\s+(.+)$', body_text, re.MULTILINE)
    return m.group(1).strip() if m else None


def extract_description(html_body, max_len=160):
    """Extract description from first paragraph of HTML body."""
    # Strip HTML tags for plain text
    text = re.sub(r'<[^>]+>', '', html_body)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_len:
        text = text[:max_len-3] + '...'
    return text


def extract_keywords(body_text):
    """Extract keywords from markdown body if present."""
    m = re.search(r'\*\*Keywords?:?\*\*\s*(.+?)(?:\n|$)', body_text, re.IGNORECASE)
    if m:
        return [k.strip() for k in m.group(1).split(',')]
    return []


def make_slug(title):
    """Generate a URL-friendly slug from paper title.
    
    Uses title keywords for SEO and human readability.
    Handles duplicates by appending a short hash suffix.
    """
    import re as _re
    
    # Convert to lowercase, replace non-alphanumeric with hyphens
    slug = title.lower().strip()
    slug = _re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    
    # Trim to max 80 chars (URLs shouldn't be too long)
    if len(slug) > 80:
        slug = slug[:80].rstrip('-')
    
    return slug


# Track used slugs across the render run to handle duplicates
_SLUGS_USED = set()

def unique_slug(title):
    """Generate a unique slug, appending hash suffix only if needed."""
    base = make_slug(title)
    if base not in _SLUGS_USED:
        _SLUGS_USED.add(base)
        return base
    # Duplicate detected — append short hash
    import hashlib as _hl
    suffix = _hl.sha256(title.encode()).hexdigest()[:4]
    unique = f'{base}-{suffix}'
    _SLUGS_USED.add(unique)
    return unique


def make_jsonld(title, slug, date_str, keywords, abstract):
    """Generate Schema.org JSON-LD."""
    ld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": title,
        "url": f"{SITE_URL}/papers/{slug}",
        "license": "https://github.com/QNFO/license",
        "copyrightHolder": {
            "@type": "Person",
            "name": "Rowan Brad Quni-Gudzinas",
            "identifier": "https://orcid.org/0009-0002-4317-5604"
        },
        "usageInfo": "Non-commercial use only. Attribution required. Patent prior art citation required per QNFO Content License Agreement v1.1.",
        "isAccessibleForFree": True
    }
    if date_str:
        ld["datePublished"] = date_str
    if keywords:
        ld["keywords"] = keywords
    if abstract:
        ld["abstract"] = abstract[:500]
    return json.dumps(ld, indent=2)


# =========================================================================
# RENDER
# =========================================================================

def render_paper(md_path, dry_run=False):
    """Convert a single .md paper to .html."""
    with open(md_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    # 1. Extract frontmatter
    fm, body = extract_frontmatter(raw)

    # 2. Extract metadata
    title = extract_title(body)
    if not title:
        title = os.path.basename(md_path).replace('.md', '').strip()
        print(f"  [WARN] No h1 found in {os.path.basename(md_path)}, using filename")

    # Date extraction
    date_str = fm.get('modified', fm.get('date', ''))
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    keywords = extract_keywords(body)
    slug = unique_slug(title)

    # 3. Pandoc conversion
    html_body = pandoc_convert(body)
    description = extract_description(html_body)
    jsonld = make_jsonld(title, slug, date_str, keywords, description)

    if dry_run:
        print(f"  [DRY] {title[:80]} → {slug}")
        return slug, title, date_str, keywords, 0

    # 4. Template assembly (use replace, not format, to avoid { } conflicts)
    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', title)
    html = html.replace('__DESCRIPTION__', description)
    html = html.replace('__CANONICAL_URL__', f'{SITE_URL}/papers/{slug}')
    html = html.replace('__SITE_URL__', SITE_URL)
    html = html.replace('__JSONLD__', jsonld)
    html = html.replace('__PANDOC_BODY__', html_body)

    # 5. Write
    out_path = QWAV_PAPERS / f'{slug}.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return slug, title, date_str, keywords, len(html)


def parse_date(date_str):
    """Parse date string to tuple for sorting. Handles ISO 8601 with/without time."""
    if not date_str:
        return (0, 0, 0)
    import re as _re
    m = _re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', date_str.strip())
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return (0, 0, 0)


def rebuild_catalog(papers, dry_run=False):
    """Regenerate the papers/index.html catalog."""
    cards = []
    for slug, title, date_str, keywords, _ in sorted(papers, key=lambda x: parse_date(x[2]), reverse=True):
        topics_html = ''.join(
            f'<span class="paper-topic">{k}</span>' for k in (keywords or [])[:8]
        )
        card = PAPER_CARD
        card = card.replace('__SITE_URL__', SITE_URL)
        card = card.replace('__SLUG__', slug)
        card = card.replace('__TITLE__', title)
        card = card.replace('__DATE__', date_str or '')
        card = card.replace('__TOPICS__', topics_html)
        cards.append(card)

    html = CATALOG_TEMPLATE
    html = html.replace('__SITE_URL__', SITE_URL)
    html = html.replace('__COUNT__', str(len(papers)))
    html = html.replace('__PAPER_CARDS__', '\n'.join(cards))

    if dry_run:
        return 0

    out_path = QWAV_PAPERS / 'index.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return len(html)


# =========================================================================
# MAIN
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Render Obsidian papers to HTML via Pandoc"
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview without writing')
    args = parser.parse_args()

    # Discover all .md files
    md_files = []
    for root, dirs, files in os.walk(OBSIDIAN_RELEASES):
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    md_files.sort()
    total = len(md_files)
    print(f"[SCAN] Found {total} papers")

    if total == 0:
        print("[ERR] No .md files found in Obsidian releases")
        return 1

    # Render all papers
    papers = []
    rendered = 0
    for i, md_path in enumerate(md_files):
        try:
            result = render_paper(md_path, dry_run=args.dry_run)
            papers.append(result)
            rendered += 1
        except Exception as e:
            print(f"  [ERR] {os.path.basename(md_path)}: {e}")

        if (i + 1) % 50 == 0:
            print(f"[{i+1}/{total}] Rendered...")

    print(f"\n[RENDERED] {rendered}/{total} papers to HTML")

    # Rebuild catalog
    if not args.dry_run and rendered > 0:
        cat_size = rebuild_catalog(papers)
        print(f"[CATALOG] papers/index.html: {cat_size:,} chars / {rendered} papers listed")

    print(f"\n[DONE] All papers rendered to {QWAV_PAPERS}")
    print(f"  Deploy: wrangler pages deploy --project-name qwav")

    return 0


if __name__ == '__main__':
    sys.exit(main())
