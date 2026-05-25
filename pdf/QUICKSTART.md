# Markdown → PDF Builder — Quickstart & Install Guide

> **v3.0** | Convert any Markdown file to a professional A4 PDF with one command. Three CSS presets. MathJax 3 LaTeX. Edge/Chrome headless.

---

## What This Is

A fully automated Markdown → HTML → PDF pipeline that runs entirely within DeepChat. Replaces manual PDF export with a script that:

1. Parses YAML frontmatter (title, authors, ORCID, DOI, abstract, date)
2. Renders Markdown → HTML (code highlighting, tables, lists, math)
3. Renders LaTeX via MathJax 3 CDN (unless `--no-math`)
4. Prints to A4 PDF via Edge/Chrome headless (preserves rendered JavaScript)

**No external dependency. No manual export step. Works from any project directory.**

---

## Prerequisites

| Requirement | Check | Install |
|:------------|:------|:--------|
| Python 3.8+ | `python --version` | [python.org](https://www.python.org) |
| `markdown` library | `pip show markdown` | `pip install markdown` |
| Edge or Chrome | Installed by default on Windows 10/11 | — |

---

## Quick Install (30 seconds)

### Option A: Skill Install (Recommended — works from DEFAULT agent)

```powershell
# Already installed at:
C:\Users\LENOVO\.deepchat\skills\markdown-pdf\
```

The DEFAULT agent activates this skill automatically when you say "convert paper.md to PDF" or "build PDF from markdown".

### Option B: Manual Install (for custom setups)

```powershell
# 1. Create skill directory
New-Item -Path "$env:USERPROFILE\.deepchat\skills\markdown-pdf" -ItemType Directory -Force

# 2. Copy files from canonical location
Copy-Item "G:\My Drive\prompts\pdf\build_pdf.py" "$env:USERPROFILE\.deepchat\skills\markdown-pdf\"
Copy-Item "G:\My Drive\prompts\pdf\css\*" "$env:USERPROFILE\.deepchat\skills\markdown-pdf\css\" -Recurse
Copy-Item "G:\My Drive\prompts\pdf\SKILL.md" "$env:USERPROFILE\.deepchat\skills\markdown-pdf\"
```

### Option C: Standalone (no skill — use exec directly)

The script is self-contained at:
```
G:\My Drive\prompts\pdf\build_pdf.py
```

Just run it directly — no installation needed.

---

## First Use (30 seconds)

Create a minimal test file and build it:

```bash
# Create test markdown
Write-Output @"
---
title: "Hello, PDF"
authors: "Your Name"
date: "2026-05-23"
abstract: "My first Markdown->PDF build."
---

## Section One

This is a test of the automatic PDF builder.

- It handles **bold** and *italic* text
- It renders inline math: $E = mc^2$
- It renders display math:
$$
\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}
$$

\`\`\`python
print("Hello, world!")
\`\`\`

| Col A | Col B |
|:------|:------|
| 1     | 2     |
"@ | Out-File -Encoding UTF8 test.md

# Build it! (academic style — default)
python "G:\My Drive\prompts\pdf\build_pdf.py" --input test.md

# Result: test.pdf (~191 KB) in the same directory
```

---

## CSS Presets — Choose Your Style

Three built-in styles, no CSS knowledge needed. Use `--style <name>`.

| Preset | Font | Code Style | Size | Best For |
|:-------|:-----|:-----------|:-----|:---------|
| `academic` | Inter (Google Fonts) | Color-coded pink/blue, light bg | 6.5 KB | Research papers, formal docs |
| `modern` | System font stack | Dark bg #1e293b, pastel highlights | 6.3 KB | Reports, presentations |
| `minimal` | Georgia (serif) | Plain Courier, no color | 4.4 KB | Preprints, arXiv, plain text |

### Academic (default)
```bash
python build_pdf.py --input paper.md --style academic
```
- Inter font from Google Fonts CDN
- Black 3px title underline
- Author block with left black border, gray background
- Color-coded code (pink strings, blue numbers, purple functions)
- A4 print margins with page numbers

### Modern
```bash
python build_pdf.py --input paper.md --style modern
```
- System font stack (no external font dependency)
- Blue accent (#2563eb) on title and author block
- Dark code blocks (#1e293b) with pastel syntax colors
- Card-style author block with gradient background
- Cleaner borders, more whitespace

### Minimal
```bash
python build_pdf.py --input paper.md --style minimal
```
- Georgia serif, centered title
- Plain code blocks (Courier, no color)
- No external font dependencies
- 32% smaller HTML than academic
- Best for plain-text preprints

### Custom CSS
```bash
python build_pdf.py --input paper.md --css my-style.css
```
Full control — `--css` always overrides `--style`. Any valid CSS works.

---

## Integration — Three Ways to Use

### 1. From DEFAULT Agent (via Skill — automatic)

```
User: "Convert research-paper.md to PDF, academic style"

DEFAULT agent (reads markdown-pdf skill):
  1. Identifies trigger: "convert ... to PDF"
  2. Composes: python "G:\My Drive\prompts\pdf\build_pdf.py" --input "research-paper.md" --style academic
  3. Executes with background:true
  4. Verifies: Test-Path research-paper.pdf -> reports 191 KB
  5. (Optional) Post-processes with pdf skill: merge, watermark, metadata
```

### 2. From Subagent (via Template)

```
Parent agent:
  fill_prompt_template("PDF-BUILDER-TEMPLATE", {
    markdownPath: "...",
    outputPdfPath: "...",
    style: "modern"
  })
  -> Subagent validates inputs, produces command
  -> Parent executes command
```

### 3. Direct CLI (from any terminal)

```bash
python "G:\My Drive\prompts\pdf\build_pdf.py" --input paper.md --style modern
```

---

## All CLI Flags

| Flag | Required | Default | Description |
|:-----|:---------|:--------|:------------|
| `--input`, `-i` | **Yes** | — | Input Markdown file (.md) |
| `--output`, `-o` | No | same name + `.pdf` | Output PDF path |
| `--style` | No | `academic` | CSS preset: `academic`, `modern`, `minimal` |
| `--css` | No | — | Custom CSS file (overrides `--style`) |
| `--title` | No | from frontmatter | Override title |
| `--no-math` | No | `False` | Skip MathJax/LaTeX |
| `--html-only` | No | `False` | Stop after HTML (preview) |
| `--working-dir` | No | output dir | Intermediate HTML location |

---

## YAML Frontmatter Reference

All fields are optional. Missing fields are simply omitted from the author block.

```yaml
---
title: "My Paper Title"           # Override with --title flag
authors: "Rowan Quni"             # Displayed as "Author:" line
orcid: "0000-0002-4317-5604"      # Linked to orcid.org
doi: "10.5281/zenodo.123456"      # Linked to doi.org (Zenodo DOIs)
date: "2026-05-23"                # Defaults to today if omitted
abstract: "Paper abstract here."  # Displayed below author block
---
```

---

## Post-Processing with the `pdf` Skill

The existing `pdf` skill handles everything AFTER conversion:

| Task | pdf Skill Command |
|:-----|:------------------|
| Merge chapters | `PdfWriter` → `.add_page()` for each chapter PDF |
| Add watermark | Load watermark PDF → `.merge_page()` on each page |
| Extract text | `pdfplumber` → `page.extract_text()` |
| Extract tables | `pdfplumber` → `page.extract_tables()` → DataFrame |
| Split pages | One `PdfWriter` per page |
| Extract metadata | `PdfReader` → `.metadata.title`, `.metadata.author` |
| Password protect | `writer.encrypt("userpass", "ownerpass")` |

Typical full pipeline:

```bash
# Step 1: Convert each chapter to PDF
python build_pdf.py --input ch1.md --style academic
python build_pdf.py --input ch2.md --style academic
python build_pdf.py --input ch3.md --style academic

# Step 2: Merge with pdf skill
python -c "
from pypdf import PdfReader, PdfWriter
w = PdfWriter()
for f in ['ch1.pdf','ch2.pdf','ch3.pdf']:
    for p in PdfReader(f).pages: w.add_page(p)
w.write('book.pdf')
w.encrypt('', 'ownerpass')
"
```

---

## Exit Codes

| Code | Meaning | Recovery |
|:-----|:--------|:---------|
| 0 | Success | — |
| 1 | Input file not found | Check `--input` path |
| 2 | CSS file not found | Check `--css` path |
| 3 | `markdown` library missing | `pip install markdown` |
| 4 | HTML build failed | Check Markdown syntax, frontmatter |
| 5 | No browser found | Install Edge or Chrome |
| 6 | PDF step empty output | Check browser version, file permissions |
| 7 | PDF conversion timeout | File too large? Increase timeout |
| 8 | PDF conversion error | Check browser path, disk space |

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| `markdown` import error | Library not installed | `pip install markdown` |
| "No browser found" | Edge/Chrome not at standard path | Install browser OR set custom path in `find_browser()` |
| PDF has no page numbers | Not yet rendered by browser | Wait — headless takes 5-15s for MathJax |
| Chinese/Unicode missing | Font doesn't support CJK | Use `--css custom-with-cjk.css` that loads Noto Sans |
| MathJax renders as raw LaTeX | CDN unreachable or `--no-math` flag | Check internet; remove `--no-math` |
| Output file is 0 bytes | Browser crashed or timed out | Re-run; check `--working-dir` for HTML debug |
| Frontmatter not parsed | Not at start of file, or malformed | Must start with `---` on line 1 |

---

## File Structure

```
prompts/pdf/                          # Canonical source (git-tracked)
├── build_pdf.py          16,509 B    CLI pipeline (v3.0)
├── README.md              4,524 B    Full documentation
├── QUICKSTART.md             —       This guide
└── css/
    ├── academic.css        4,914 B   Inter font, A4, print-ready
    ├── modern.css          4,645 B   System fonts, dark code
    └── minimal.css         2,815 B   Georgia serif, plain text

skills/markdown-pdf/                  # Installed skill (DEFAULT agent)
├── SKILL.md                2,837 B   Trigger conditions + workflow
├── build_pdf.py           16,509 B   Same pipeline script
├── README.md                  —      Quickstart (duplicate)
└── css/                              Same CSS presets
    ├── academic.css
    ├── modern.css
    └── minimal.css
```

---

## Examples Gallery

```bash
# Basic: convert paper to PDF with default academic style
python build_pdf.py --input paper.md

# Named output + modern style
python build_pdf.py --input paper.md --output release/paper-v2.pdf --style modern

# Minimal style + no math (fastest build)
python build_pdf.py --input paper.md --style minimal --no-math

# Custom CSS + title override
python build_pdf.py --input paper.md --css arxiv-style.css --title "My Preprint"

# HTML preview only (debug CSS)
python build_pdf.py --input paper.md --html-only --style modern

# Build with custom working directory
python build_pdf.py --input paper.md --working-dir tmp/
```

---

## See Also

- **`pdf` skill** — Post-processing: merge, split, watermark, extract text/tables
- **`PDF-BUILDER-TEMPLATE`** — Subagent template (#29 in prompts.json) for validated command generation
- **`EMAIL-AGENT-TEMPLATE`** — Same pattern, but for email drafting
- **Archived origin**: `G:\My Drive\Archive\projects\2026\05\markdown-pdf-builder\` (v2.0 proof-of-concept)

---

*markdown-pdf v3.0 — built 2026-05-23. System audit: ALL PASS.*
