#!/usr/bin/env python3
"""
render-papers.py -- Convert ALL publications to HTML and generate catalog page

Scans Obsidian/releases/ for all .md papers, converts to HTML pages,
updates the papers/index.html catalog, and prepares for Cloudflare Pages deployment.

Usage:
  python tools/render-papers.py              # Render all papers to QWAV/papers/
  python tools/render-papers.py --dry-run    # Preview only

v1.0 — 2026-05-27
"""

import os, sys, re, json, hashlib
from pathlib import Path
from datetime import datetime

QWAV_ROOT = Path(r"G:\My Drive\QWAV")
OBSIDIAN_RELEASES = Path(r"G:\My Drive\Obsidian\releases")
PAPERS_DIR = QWAV_ROOT / "papers"
SITE_URL = "https://deep.qwav.tech"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | QWAV</title>
<meta name="description" content="{title} — QWAV Research Publication">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<!-- Schema.org / JSON-LD for Google Scholar -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "headline": "{js_title}",
  "datePublished": "{date}",
  "url": "{url}",
  "isAccessibleForFree": true,
  "publisher": {{
    "@type": "Organization",
    "name": "QWAV / QNFO"
  }}
}}
</script>
<style>
  body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; line-height: 1.6; color: #1a1a2e; background: #f8f9fa; }}
  a {{ color: #6366f1; }}
  pre {{ background: #1e1e2e; color: #cdd6f4; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
  code {{ background: #e8e8f0; padding: 0.2em 0.4em; border-radius: 4px; }}
  pre code {{ background: none; padding: 0; }}
  .meta {{ color: #6c757d; font-size: 0.9em; margin-bottom: 2rem; }}
  .nav {{ margin-bottom: 2rem; }}
  .nav a {{ margin-right: 1rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #dee2e6; padding: 0.5rem; text-align: left; }}
  th {{ background: #e9ecef; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #0d1117; color: #c9d1d9; }}
    a {{ color: #58a6ff; }}
    pre {{ background: #161b22; }}
    code {{ background: #21262d; }}
    pre code {{ background: none; }}
    th {{ background: #21262d; }}
    th, td {{ border-color: #30363d; }}
  }}
</style>
<script>
MathJax = {{
  tex: {{ inlineMath: [['$', '$'], ['\\(', '\\)']] }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
</head>
<body>
<div class="nav">
  <a href="{site_url}/">Home</a>
  <a href="{site_url}/papers/">All Papers</a>
</div>
<article>
<h1>{title}</h1>
<div class="meta">Published: {date} | <a href="{url}">Permalink</a></div>
{body}
</article>
</body>
</html>"""


def md_to_html(text):
    """Basic markdown-to-HTML converter. Handles: headers, code blocks, lists, links, bold, italic."""
    lines = text.split('\n')
    result = []
    in_code_block = False
    code_lang = ''
    in_list = False
    list_type = None
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                result.append('</code></pre>')
                in_code_block = False
            else:
                code_lang = line[3:].strip()
                result.append('<pre><code class="language-{}">'.format(code_lang or 'plaintext'))
                in_code_block = True
            continue
        
        if in_code_block:
            result.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            continue
        
        # Close list if we hit a non-list line
        if in_list and not line.startswith(('- ', '* ', '+ ', '1. ')):
            result.append('</{}>'.format(list_type))
            in_list = False
            list_type = None
        
        # Headers
        if line.startswith('#### '):
            result.append('<h4>{}</h4>'.format(line[5:]))
            continue
        if line.startswith('### '):
            result.append('<h3>{}</h3>'.format(line[4:]))
            continue
        if line.startswith('## '):
            result.append('<h2>{}</h2>'.format(line[3:]))
            continue
        if line.startswith('# '):
            continue  # Skip title (already in h1)
        
        # Horizontal rule
        if line.strip() == '---' or line.strip() == '***':
            result.append('<hr>')
            continue
        
        # Unordered lists
        if line.startswith(('- ', '* ', '+ ')):
            if not in_list or list_type != 'ul':
                if in_list:
                    result.append('</{}>'.format(list_type))
                result.append('<ul>')
                in_list = True
                list_type = 'ul'
            item = line[2:]
            result.append('<li>{}</li>'.format(_inline_format(item)))
            continue
        
        # Ordered lists
        if re.match(r'^\d+\. ', line):
            if not in_list or list_type != 'ol':
                if in_list:
                    result.append('</{}>'.format(list_type))
                result.append('<ol>')
                in_list = True
                list_type = 'ol'
            item = re.sub(r'^\d+\. ', '', line)
            result.append('<li>{}</li>'.format(_inline_format(item)))
            continue
        
        # Tables
        if '|' in line and line.strip().startswith('|'):
            if '---' in line and line.replace('-', '').replace('|', '').strip() == '':
                continue  # Table separator
            cells = [c.strip() for c in line.strip('|').split('|')]
            tag = 'th' if not result or not result[-1].startswith('<t') else 'td'
            row = '<tr>' + ''.join('<{}>{}</{}>'.format(tag, _inline_format(c), tag) for c in cells) + '</tr>'
            if tag == 'th' and (not result or not result[-1].startswith('<table')):
                result.append('<table>')
            result.append(row)
            continue
        
        # Close table if we were in one
        if result and result[-1].startswith('<t'):
            result.append('</table>')
        
        # Empty lines
        if not line.strip():
            result.append('<br>')
            continue
        
        # Regular paragraph
        result.append('<p>{}</p>'.format(_inline_format(line)))
    
    # Cleanup any unclosed tags
    if in_code_block:
        result.append('</code></pre>')
    if in_list:
        result.append('</{}>'.format(list_type))
    
    return '\n'.join(result)


def _inline_format(text):
    """Format inline elements: links, bold, italic, inline code, math."""
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Math: $...$ → LaTeX spans (client-side rendering via KaTeX or MathJax)
    text = re.sub(r'\$\$([^$]+)\$\$', r'<div class="math display">$$\1$$</div>', text)
    text = re.sub(r'\$([^$]+)\$', r'<span class="math inline">$\1$</span>', text)
    return text


def render_paper(md_path, dry_run=False):
    """Convert a single markdown paper to HTML."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from first # heading
    title = md_path.stem
    for line in content.split('\n')[:5]:
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            break
    
    # Extract date from path
    path_parts = md_path.relative_to(OBSIDIAN_RELEASES).parts
    date = datetime.now().strftime('%Y-%m-%d')
    if len(path_parts) >= 2:
        date = '{}-{}-01'.format(path_parts[0], path_parts[1])
    
    # Generate URL-safe slug
    slug = title[:60].replace(' ', '-').replace('/', '-').lower()
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = hashlib.md5(title.encode()).hexdigest()[:8]  # fallback: unique hash
    
    url = '{}/papers/{}.html'.format(SITE_URL, slug)
    
    # Convert markdown to HTML
    body_html = md_to_html(content)
    
    # Escape title for JSON-LD
    js_title = title.replace('"', '\\"').replace('\n', ' ')
    
    html = HTML_TEMPLATE.format(
        title=title,
        js_title=js_title,
        date=date,
        url=url,
        site_url=SITE_URL,
        body=body_html
    )
    
    if dry_run:
        return slug, len(html)
    
    # Write to QWAV/papers/
    html_path = PAPERS_DIR / '{}.html'.format(slug)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return slug, len(html)


def build_catalog(papers_meta, dry_run=False):
    """Build the papers/index.html catalog page listing all papers."""
    paper_rows = []
    for p in papers_meta:
        size_kb = p['size'] // 1024
        paper_rows.append(
            '<tr><td><a href="{slug}.html">{title}</a></td>'
            '<td>{size_kb:,} KB</td><td>{date}</td></tr>'.format(
                slug=p['slug'], title=p['title'], size_kb=size_kb, date=p['date']
            )
        )
    
    catalog_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QWAV Publications Catalog</title>
<meta name="description" content="Complete QWAV research publication catalog — {total} papers">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{site_url}/papers/">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 0 auto; padding: 2rem; line-height: 1.6; color: #1a1a2e; background: #f8f9fa; }}
  a {{ color: #6366f1; }}
  input[type="search"] {{ padding: 0.5rem 1rem; border: 2px solid #6366f1; border-radius: 8px; width: 100%; max-width: 400px; font-size: 1rem; margin-bottom: 1rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #dee2e6; padding: 0.5rem; text-align: left; }}
  th {{ background: #e9ecef; cursor: pointer; }}
  tr:hover {{ background: #e8e8f0; }}
  .search {{ margin-bottom: 1.5rem; }}
  .nav {{ margin-bottom: 2rem; }}
  .nav a {{ margin-right: 1rem; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #0d1117; color: #c9d1d9; }}
    a {{ color: #58a6ff; }}
    tr:hover {{ background: #1a2332; }}
    th {{ background: #21262d; }}
    th, td {{ border-color: #30363d; }}
    input[type="search"] {{ background: #0d1117; color: #c9d1d9; border-color: #30363d; }}
  }}
</style>
<script>
MathJax = {{
  tex: {{ inlineMath: [['$', '$'], ['\\(', '\\)']] }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
</head>
<body>
<div class="nav">
  <a href="{site_url}/">Home</a>
  <a href="{site_url}/papers/">Papers</a>
  <a href="https://github.com/qnfo">GitHub</a>
</div>
<h1>QWAV Publications Catalog</h1>
<p>{total} papers — all open access with registered DOIs. Click any title to read.</p>
<div class="search">
  <input type="search" id="search" placeholder="Search {total} papers..." oninput="filterPapers()">
</div>
<table id="papersTable">
<thead>
<tr><th onclick="sortTable(0)">Title</th><th onclick="sortTable(1)">Size</th><th onclick="sortTable(2)">Date</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
<script>
function filterPapers() {{
  const q = document.getElementById('search').value.toLowerCase();
  const rows = document.querySelectorAll('#papersTable tbody tr');
  rows.forEach(r => {{
    r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}
function sortTable(col) {{
  const tbody = document.querySelector('#papersTable tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  rows.sort((a, b) => a.cells[col].textContent.localeCompare(b.cells[col].textContent));
  rows.forEach(r => tbody.appendChild(r));
}}
</script>
</body>
</html>""".format(total=len(paper_rows), site_url=SITE_URL, rows='\n'.join(paper_rows))
    
    if dry_run:
        return len(catalog_html)
    
    catalog_path = PAPERS_DIR / 'index.html'
    with open(catalog_path, 'w', encoding='utf-8') as f:
        f.write(catalog_html)
    
    return len(catalog_html)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Render all publications to HTML")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Limit to N papers (0=all)")
    args = parser.parse_args()
    
    dry = args.dry_run
    limit = args.limit
    mode = "DRY RUN" if dry else "LIVE"
    
    print("=" * 60)
    print("PAPER RENDERER v1.0 — {}".format(mode))
    print("Source: {}".format(OBSIDIAN_RELEASES))
    print("Target: {}".format(PAPERS_DIR))
    print("=" * 60)
    
    if not dry:
        PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Scan all papers
    papers = []
    for year_dir in sorted(OBSIDIAN_RELEASES.iterdir()):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for md_file in month_dir.glob("*.md"):
                papers.append((
                    md_file,
                    md_file.stat().st_size,
                    '{}-{}-01'.format(year_dir.name, month_dir.name)
                ))
    
    papers.sort(key=lambda x: x[2], reverse=True)  # Newest first
    
    if limit > 0:
        papers = papers[:limit]
    
    print("\n[SCAN] Found {} papers".format(len(papers)))
    
    # Render each paper
    papers_meta = []
    rendered = 0
    for i, (md_path, size, date) in enumerate(papers):
        title = md_path.stem
        slug, html_size = render_paper(md_path, dry_run=dry)
        papers_meta.append({'slug': slug, 'title': title, 'size': size, 'date': date})
        rendered += 1
        if (i + 1) % 50 == 0:
            print("[{} / {}] Rendered...".format(i + 1, len(papers)))
    
    print("\n[RENDERED] {}/{} papers to HTML".format(rendered, len(papers)))
    
    # Build catalog
    catalog_size = build_catalog(papers_meta, dry_run=dry)
    print("[CATALOG] papers/index.html: {:,} chars / {} papers listed".format(
        catalog_size, len(papers_meta)))
    
    if dry:
        print("\n[DRY RUN] No files written. Remove --dry-run to render.")
    else:
        print("\n[DONE] All papers rendered to {}".format(PAPERS_DIR))
        print("  Deploy: wrangler pages deploy --project-name qwav")
    return 0

if __name__ == "__main__":
    sys.exit(main())
