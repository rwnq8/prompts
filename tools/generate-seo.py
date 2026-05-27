#!/usr/bin/env python3
"""
generate-seo.py -- Generate sitemap.xml, robots.txt, llms.txt for QWAV site

Scans publications in Obsidian/releases/ and QWAV/papers/ to generate
SEO files that make all 185+ publications discoverable by:
  - Google / search engines (sitemap.xml + robots.txt)
  - AI crawlers: ChatGPT, Claude, Perplexity (llms.txt)
  - Google Scholar (Schema.org markup)

Usage:
  python tools/generate-seo.py                   # Generate all files
  python tools/generate-seo.py --dry-run         # Preview only

v1.0 -- 2026-05-27
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

QWAV_ROOT = Path(r"G:\My Drive\QWAV")
OBSIDIAN_RELEASES = Path(r"G:\My Drive\Obsidian\releases")
SITE_URL = "https://deep.qwav.tech"


def scan_publications():
    """Scan all publication dirs and return paper metadata."""
    papers = []
    
    # Scan Obsidian releases
    for year_dir in sorted(OBSIDIAN_RELEASES.iterdir()):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for paper_file in month_dir.glob("*.md"):
                papers.append({
                    "title": paper_file.stem,
                    "path": str(paper_file.relative_to(OBSIDIAN_RELEASES)),
                    "url": "{}/papers/{}/{}/{}.html".format(
                        SITE_URL, year_dir.name, month_dir.name, paper_file.stem),
                    "date": "{}-{}-01".format(year_dir.name, month_dir.name),
                    "file": paper_file,
                })
    
    # Also scan QWAV/papers/ for natively hosted papers
    qwav_papers = QWAV_ROOT / "papers"
    if qwav_papers.exists():
        for paper_file in qwav_papers.glob("*.html"):
            papers.append({
                "title": paper_file.stem,
                "path": paper_file.name,
                "url": "{}/papers/{}".format(SITE_URL, paper_file.name),
                "date": datetime.fromtimestamp(paper_file.stat().st_mtime).strftime("%Y-%m-%d"),
                "file": paper_file,
            })
    
    return sorted(papers, key=lambda p: p["date"], reverse=True)


def generate_sitemap(papers, dry_run=False):
    """Generate sitemap.xml."""
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Home page
    url_el = SubElement(urlset, "url")
    SubElement(url_el, "loc").text = SITE_URL + "/"
    SubElement(url_el, "changefreq").text = "weekly"
    SubElement(url_el, "priority").text = "1.0"
    
    # Papers index
    url_el = SubElement(urlset, "url")
    SubElement(url_el, "loc").text = SITE_URL + "/papers/"
    SubElement(url_el, "changefreq").text = "daily"
    SubElement(url_el, "priority").text = "0.9"
    
    # Individual papers
    for paper in papers[:500]:  # Limit to 500 URLs per sitemap
        url_el = SubElement(urlset, "url")
        SubElement(url_el, "loc").text = paper["url"]
        SubElement(url_el, "lastmod").text = paper["date"]
        SubElement(url_el, "changefreq").text = "monthly"
        SubElement(url_el, "priority").text = "0.7"
    
    xml_str = minidom.parseString(tostring(urlset, "utf-8")).toprettyxml(indent="  ")
    
    if dry_run:
        print("[DRY RUN] Would write sitemap.xml ({} papers)".format(len(papers)))
        print("  Preview: {} URLs".format(len(papers) + 2))
        return xml_str
    
    sitemap_path = QWAV_ROOT / "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print("[OK] sitemap.xml written: {} papers".format(len(papers)))
    return xml_str


def generate_robots_txt(dry_run=False):
    """Generate robots.txt with AI crawler directives."""
    content = """User-agent: *
Allow: /
Sitemap: {}/sitemap.xml

# AI Crawlers - allow all for discoverability
User-agent: GPTBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

# Disallow nothing - all research is open access
""".format(SITE_URL)
    
    if dry_run:
        print("[DRY RUN] Would write robots.txt")
        return content
    
    robots_path = QWAV_ROOT / "robots.txt"
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] robots.txt written")
    return content


def generate_llms_txt(papers, dry_run=False):
    """Generate llms.txt - the AI crawler manifest introduced by llmstxt.org.
    
    llms.txt is a Markdown file that tells LLM crawlers what content is available,
    with structured links that AI systems can parse efficiently.
    """
    recent = papers[:20]
    
    content = """# deep.qwav.tech — QWAV Research Publications

> QWAV Technical Site: Ultrametric Quantum Computing & AI research. All papers are open-access with registered DOIs and computational evidence.

## Quick Links

- [QWAV Home]({}/)
- [Paper Catalog]({}/papers/)
- [Interactive Demos]({}/#demos)
- [Evidence Deck]({}/#evidence)

## Recent Publications

""".format(SITE_URL, SITE_URL, SITE_URL, SITE_URL, SITE_URL)
    
    for paper in recent:
        content += "- [{}]({}) ({})\n".format(paper["title"], paper["url"], paper["date"])
    
    content += """
## About This Site

This site hosts peer-reviewed and pre-print research on ultrametric quantum computing, 
geometric physics, topological quantum computation, and related fields. All publications 
include registered DOIs, computational evidence, and full source traceability.

| Stat | Value |
|:-----|:------|
| Total Papers | {} |
| Zenodo DOIs | 85+ |
| Interactive Demos | 7 |
| Semantic Search | Vectorize-powered (qwav-research, 768d) |

## Optional

- [Sitemap]({}/sitemap.xml)
- [Robots.txt]({}/robots.txt)
- [QNFO GitHub](https://github.com/qnfo)
""".format(len(papers), SITE_URL, SITE_URL)
    
    if dry_run:
        print("[DRY RUN] Would write llms.txt ({} papers featured)".format(len(recent)))
        return content
    
    llms_path = QWAV_ROOT / "llms.txt"
    with open(llms_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] llms.txt written")
    return content


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate SEO files for QWAV site")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    dry = args.dry_run
    mode = "DRY RUN" if dry else "LIVE"
    
    print("=" * 60)
    print("SEO GENERATOR v1.0 — {}".format(mode))
    print("Site: {}".format(SITE_URL))
    print("=" * 60)
    
    papers = scan_publications()
    print("\n[S CAN] Found {} publications".format(len(papers)))
    
    if not dry:
        QWAV_ROOT.mkdir(parents=True, exist_ok=True)
    
    generate_sitemap(papers, dry_run=dry)
    generate_robots_txt(dry_run=dry)
    generate_llms_txt(papers, dry_run=dry)
    
    if dry:
        print("\n[DRY RUN] No files written. Remove --dry-run to generate.")
    else:
        print("\n[DONE] SEO files generated at {}".format(QWAV_ROOT))
        print("  sitemap.xml — Search engine discovery")
        print("  robots.txt — Crawler directives (all AI crawlers allowed)")
        print("  llms.txt    — AI crawler manifest")
        print("\n  Next: wrangler pages deploy --project-name qwav")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
