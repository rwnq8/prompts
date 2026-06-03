---
name: pdf-builder
description: Build publication-quality PDFs from Markdown files with math rendering via matplotlib mathtext. Use when the agent needs to convert .md to .pdf for QNFO publications, papers, or reports. Handles inline math ($...$), display math ($$...$$), code blocks, and Unicode typography. Supports --no-math flag for Unicode fallback rendering.
version: "1.0"
---

# PDF BUILDER SKILL — v1.0

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

### Limitations

- **Not full LaTeX**: mathtext supports a subset of LaTeX math. Complex environments
  (`\begin{align}`, `\begin{cases}`) may not render correctly.
- **No cross-references**: Equation numbering and `\ref{}` not supported.
- **Font**: Uses matplotlib's default math font (not Calibri or DejaVu).

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

## Cross-References

- Used by: `publication-publisher` skill (Step 2: Build PDF)
- Related: `cloudflare-deployer` skill (post-PDF deployment)
- Deprecates: `templates/PDF-BUILDER-TEMPLATE.md`

---

*pdf-builder v1.0 — Bundled skill with math rendering. Replaces PDF-BUILDER-TEMPLATE.*
