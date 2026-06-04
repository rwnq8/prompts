---
name: pdf-builder
description: Build publication-quality PDFs from Markdown files with math rendering via matplotlib mathtext. Use when the agent needs to convert .md to .pdf for QNFO publications, papers, or reports. Handles inline math ($...$), display math ($$...$$), code blocks, and Unicode typography. Supports --no-math flag for Unicode fallback rendering.
version: "1.1"
---

# PDF BUILDER SKILL — v1.1

> **Bundled skill.** All scripts and references are self-contained in this skill directory.
> Deployed via `_deploy.py` to `%APPDATA%\DeepChat\skills\pdf-builder\`.

---

## Purpose

Convert Markdown (`.md`) or HTML (`.html`) files to publication-quality PDFs using
reportlab. Renders mathematical expressions using matplotlib's mathtext parser.

**Replaces:** `templates/PDF-BUILDER-TEMPLATE.md` (deprecated — v1.1, 2026-06-03).

---

## Quick Start

```bash
# Pull canonical from R2 if bundled copy is stale:
# npx wrangler r2 object get qnfo/tools/build_pdf.py --remote --file=_build_pdf.py

# Execute (use bundled copy):
python "G:\My Drive\prompts\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf

# With title override:
python "G:\My Drive\prompts\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf --title "My Paper" --author "Name" --date "2026-06-03"

# Skip math rendering (Unicode fallback):
python "G:\My Drive\prompts\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf --no-math
```

---

## Workflow

### Step 1: Verify Prerequisites

```bash
python -c "import reportlab, matplotlib; print('OK')"
# Expected: OK (no ImportError)
```

If missing: `pip install reportlab matplotlib markdown pymupdf`

### Step 2: Verify Input

```bash
Test-Path "<input>.md"
```

### Step 3: Build PDF

```bash
python "G:\My Drive\prompts\skills\pdf-builder\scripts\build_pdf.py" --input "<input>.md" --output "<output>.pdf"
```

### Step 4: Verify Rendering (MANDATORY)

```bash
python -c "
import fitz
doc = fitz.open('<output>.pdf')
text = ''.join(page.get_text() for page in doc)
if '\ufffd' in text:
    print('[BLOCKED] PDF contains Unicode replacement characters')
else:
    print('[OK] No replacement characters')
doc.close()
"
```

If verification fails: PDF is NOT publication-ready. See `references/math-rendering.md` for
troubleshooting.

### Step 5: Clean Up (if using R2-pulled ephemeral copy)

```bash
Remove-Item _build_pdf.py -ErrorAction SilentlyContinue
```

---

## Math Rendering

### Supported Delimiters

| Delimiter | Type | Example |
|:----------|:-----|:--------|
| `$...$` | Inline math | `$E = mc^2$` |
| `$$...$$` | Display math (single-line) | `$$\hat{H}\psi = E\psi$$` |
| `$$` (block) | Display math (multi-line) | `$$\n...\n$$` |

### --no-math Mode

Converts LaTeX to Unicode approximations instead of rendering images:
- `$\alpha$` → α, `$\hbar$` → ℏ, `$\int$` → ∫, `$\infty$` → ∞
- Use for drafts or when matplotlib is unavailable
- See `references/math-rendering.md` for the full conversion table

### Limitations — READ BEFORE USING

**This skill is designed for SIMPLE markdown documents.** For documents with complex
math or tables, use the HTML-to-PDF alternative (see §Alternative below).

#### Math: Mathtext is NOT Full LaTeX

matplotlib's mathtext parser supports a SUBSET of LaTeX math. These specific commands
are KNOWN to fail and will produce `[MATH RENDER ERROR]` in output:

| Unsupported Command | Failure Mode | Workaround |
|:--------------------|:-------------|:-----------|
| `\bmod` | Not recognized by mathtext | Use `\ \mathrm{mod}\ ` (spaces required) |
| `\operatorname{...}` | Not recognized by mathtext | Use `\mathrm{...}` |
| `\\text{...}` (double backslash) | Causes parse error | Use `\text{...}` (single backslash) |
| `\begin{align}...\end{align}` | Not recognized | Use separate `$$...$$` blocks |
| `\begin{cases}...\end{cases}` | Not recognized | Use `\left\{ \begin{array}...` |
| `\bm{...}` | Not recognized | Use `\mathbf{...}` |
| `\mathcal{...}` | Limited support | Test before deploying |
| `\tag{...}` / `\label{...}` / `\ref{...}` | Not recognized | Add equation numbers manually |

**Pre-flight check:** Before building a PDF, scan the source file for unsupported
commands:
```bash
rg -n '\\\\bmod|\\\\\\\\text|\\\\operatorname|\\\\begin\{align|\\\\begin\{cases|\\\\bm\{|\\\\tag\{|\\\\label\{|\\\\ref\{' input.md
```
Any hits = this document is NOT suitable for pdf-builder. Use HTML-to-PDF instead.

#### Tables: NOT SUPPORTED

**Markdown tables are NOT rendered.** The pdf-builder has no table parser —
pipe-delimited markdown tables appear as raw text in the output. This is a
FUNDAMENTAL limitation of the reportlab pipeline, not a bug.

For documents containing ANY tables → use HTML-to-PDF alternative.

#### Other Limitations

- **No cross-references**: Equation numbering and `\ref{}` not supported.
- **Font**: Uses matplotlib's default math font (not Calibri or DejaVu).
- **Very long expressions** (>200 chars): May break across lines incorrectly.

---

## Script

### Bundled Script

`scripts/build_pdf.py` — v1.1 (2026-06-03)

The script is bundled in this skill's `scripts/` directory and is the primary
execution path. It is also backed up to R2 at `qnfo/tools/build_pdf.py`.

### Dependencies

| Package | Version | Purpose |
|:--------|:--------|:--------|
| `reportlab` | ≥4.0 | PDF generation |
| `matplotlib` | ≥3.5 | Math rendering (mathtext) |
| `markdown` | ≥3.0 | Markdown→HTML parsing (optional, fallback available) |
| `pymupdf` (fitz) | ≥1.20 | PDF text extraction for verification |

### Arguments

| Flag | Required | Description |
|:-----|:---------|:------------|
| `--input`, `-i` | Yes | Input file (.md or .html) |
| `--output`, `-o` | Yes | Output PDF file path |
| `--title`, `-t` | No | Publication title (auto-detected from first H1) |
| `--author`, `-a` | No | Author name |
| `--date`, `-d` | No | Publication date (YYYY-MM-DD, defaults to today) |
| `--no-math` | No | Skip math rendering, use Unicode approximations |
| `--check-unicode` | No | Scan input for `\uXXXX` escapes (no PDF build) |
| `--fix-unicode` | No | Auto-correct `\uXXXX` escapes in place |

---

## Reference Files

| File | Purpose |
|:-----|:--------|
| `references/math-rendering.md` | Math rendering limitations, LaTeX→Unicode table, troubleshooting |
| `scripts/build_pdf.py` | The bundled PDF builder script (v1.1) |

---

## Alternative: HTML-to-PDF for Complex Documents

**When pdf-builder cannot handle your document** (tables, complex LaTeX, `\bmod`,
`\operatorname`, etc.), build the PDF from the HTML render instead. Modern browsers
render MathJax + HTML tables perfectly — capture that.

### Decision Flow

```
Does document contain tables? ──YES──→ Use HTML-to-PDF
Does document use \bmod, \operatorname, \\text? ──YES──→ Use HTML-to-PDF
Does document use \begin{align}, \begin{cases}? ──YES──→ Use HTML-to-PDF
Otherwise ──→ pdf-builder is suitable
```

### Method A: CDP Page.printToPDF (Live URL)

If the document is already deployed (Cloudflare Pages, any web server):

```bash
# 1. Load the page in YoBrowser
load_url("https://example.pages.dev/spec/")
# Wait for MathJax to finish rendering (3-5 seconds)

# 2. Print to PDF
cdp_send(method="Page.printToPDF", params={
    "printBackground": True,
    "preferCSSPageSize": True,
    "marginTop": 0.5,
    "marginBottom": 0.5,
    "marginLeft": 0.5,
    "marginRight": 0.5
})
# Save the returned base64 data → output.pdf

# 3. Verify the PDF
python -c "
import fitz
doc = fitz.open('output.pdf')
text = ''.join(page.get_text() for page in doc)
has_tables = '|' not in text  # Tables rendered as text, not pipes
print(f'Pages: {len(doc)}, Chars: {len(text)}, Tables rendered: {has_tables}')
doc.close()
"
```

### Method B: CDP Page.printToPDF (Local File)

For local HTML files that aren't deployed yet:

```bash
# 1. Start a temporary HTTP server (PowerShell, background)
$server = Start-Process python -ArgumentList '-m','http.server','8765' -PassThru -WorkingDirectory 'pages/spec/'

# 2. Load the local page
load_url("http://localhost:8765/index.html")

# 3. Print to PDF (same as Method A)
cdp_send(method="Page.printToPDF", params={...})

# 4. Clean up
Stop-Process $server.Id
Remove-Item _output.pdf  # if ephemeral
```

### Verification Gate (Same for Both Methods)

```bash
python -c "
import fitz, sys
doc = fitz.open(sys.argv[1])
text = ''.join(page.get_text() for page in doc)
issues = []
if '\ufffd' in text:
    issues.append('Unicode replacement characters')
if '|' in text and '|---' in text:
    issues.append('Raw markdown table pipes in output')
if 'MATH RENDER ERROR' in text:
    issues.append('Math rendering errors')
if '\\bmod' in text or '\\text' in text:
    issues.append('Raw LaTeX commands in output')
if issues:
    print('[BLOCKED]', '; '.join(issues))
else:
    print('[OK] PDF verified — no rendering issues')
doc.close()
" output.pdf
```

---

## Cross-References

- Used by: `publication-publisher` skill (Step 2: Build PDF)
- Related: `cloudflare-deployer` skill (post-PDF deployment)
- Deprecates: `templates/PDF-BUILDER-TEMPLATE.md`

---

*pdf-builder v1.1 — Bundled skill with math rendering + HTML-to-PDF fallback for complex documents. Replaces PDF-BUILDER-TEMPLATE.*
