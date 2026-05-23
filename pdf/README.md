# PDF Builder -- Markdown-to-PDF Pipeline

> **Location:** `G:\My Drive\prompts\pdf\` | **Status:** Active | **Version:** 3.0

Automated Markdown -> HTML -> PDF pipeline using Edge/Chrome headless mode. Accepts any Markdown file (with optional YAML frontmatter), embeds professional academic CSS, renders LaTeX math via MathJax 3 CDN, and produces a print-ready A4 PDF.

Reusable from any DeepChat agent thread via a single CLI command.

---

## Prerequisites

| Requirement | Check | Install |
|:------------|:------|:--------|
| Python 3.8+ | `python --version` | [python.org](https://www.python.org/) |
| `markdown` library | `pip show markdown` | `pip install markdown` |
| Edge or Chrome | Installed by default on Windows | [microsoft.com/edge](https://www.microsoft.com/edge) |

---

## Usage

```bash
# Basic: convert paper.md to paper.pdf in the same directory
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md

# Custom output path
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md --output out/release.pdf

# Custom CSS (overrides embedded academic stylesheet)
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md --css custom.css

# HTML only (no PDF -- preview or debug)
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md --html-only

# No MathJax (faster, no JavaScript rendering)
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md --no-math

# Override title from frontmatter
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md --title "My Title"

# Specify working directory for intermediate HTML
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md --working-dir tmp/
```

---

## Pipeline Steps

1. **Parse frontmatter** -- Extract YAML metadata (title, author, ORCID, DOI, abstract, date)
2. **Markdown to HTML** -- Convert body via `markdown` library (extra, codehilite, tables, fenced_code extensions)
3. **Embed CSS** -- Academic stylesheet with A4 page layout, Inter font, print media queries, code highlighting
4. **MathJax CDN** -- Inline LaTeX rendering via MathJax 3 (tex-chtml)
5. **Headless browser** -- Edge/Chrome renders JavaScript/MathJax and prints to PDF

---

## YAML Frontmatter

The script extracts these fields from `---` delimited YAML at the top of the markdown file:

```yaml
---
title: "Paper Title"
authors: "Author Name"
orcid: "0000-0002-4317-5604"
doi: "10.5281/zenodo.123456"
date: "2026-05-23"
abstract: "Brief summary of the paper content."
---
```

All fields are optional. Missing fields are omitted from the author block.

---

## Exit Codes

| Code | Meaning |
|:-----|:--------|
| 0 | Success |
| 1 | Input file not found |
| 2 | CSS file not found |
| 3 | `markdown` library not installed |
| 4 | HTML build failed |
| 5 | No browser found (PDF step skipped) |
| 6 | PDF step returned no output |
| 7 | PDF conversion timed out (30s) |
| 8 | PDF conversion error |

---

## Files

| File | Purpose |
|:-----|:--------|
| `build_pdf.py` | Main pipeline script (CLI entry point) |
| `README.md` | This documentation |

---

## Integration

This script is integrated into the prompts template system via `PDF-BUILDER-TEMPLATE`. Parent agents invoke the template through `fill_prompt_template` to get a validated, ready-to-execute command. See `G:\My Drive\prompts\templates\PDF-BUILDER-TEMPLATE.md`.
