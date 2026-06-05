---
template: HTML-PUBLICATION-PAGE
version: "1.0"
date: 2026-06-05
parameters:
  - name: title
    type: string
    required: true
    description: "Publication title (used in <title> and <h1>)"
  - name: author
    type: string
    required: true
    description: "Author name(s) with affiliation"
  - name: date
    type: string
    required: true
    description: "Publication date (YYYY-MM-DD)"
  - name: doi
    type: string
    required: false
    default: ""
    description: "Zenodo DOI (e.g., 10.5281/zenodo.XXXXXXXX)"
  - name: description
    type: string
    required: true
    description: "Meta description (for SEO, social cards)"
  - name: license
    type: string
    required: false
    default: "QNFO Unified License Agreement (QNFO-ULA)"
    description: "License identifier"
  - name: stylesheet_path
    type: string
    required: false
    default: "stylesheets/papers.css"
    description: "Path to CSS stylesheet (relative to page)"
  - name: extra_macros
    type: string
    required: false
    default: ""
    description: "Additional MathJax macro definitions (JSON) for publication-specific commands"
  - name: canonical_md_path
    type: string
    required: true
    description: "Path to canonical Markdown source file (for reproducibility)"
  - name: ga4_measurement_id
    type: string
    required: false
    default: ""
    description: "Google Analytics 4 Measurement ID (G-XXXXXXXXXX)"
---

# HTML PUBLICATION PAGE — v1.0

> **TEMPLATE PURPOSE:** Generate a self-contained HTML publication page from canonical Markdown source. ALL content derives from the Markdown — HTML is a presentation layer, not a content source. MathJax is embedded with correct config-before-script ordering.

---

## GENERATION PROTOCOL

### Step 1: Verify Canonical Markdown Exists

```powershell
Test-Path "{{canonical_md_path}}"
```
If missing → `[BLOCKED: canonical Markdown source not found]`. Do NOT proceed.

### Step 2: Convert Markdown to HTML Body

Use Python (via script file — NEVER inline Python through PowerShell per Rule 13):

```python
import markdown
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert Markdown to HTML
# Use extensions for: code highlighting, tables, footnotes, math (pass-through for MathJax)
extensions = [
    'markdown.extensions.fenced_code',
    'markdown.extensions.tables',
    'markdown.extensions.footnotes',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
    'markdown.extensions.smarty',  # Smart quotes, em dashes
]

html_body = markdown.markdown(md_content, extensions=extensions)

# Write body to temp file for assembly
with open('_body.html', 'w', encoding='utf-8') as f:
    f.write(html_body)

print(f'[OK] Converted {len(md_content)} chars Markdown → {len(html_body)} chars HTML')
```

### Step 3: Assemble Full HTML Page

Write a Python script that assembles the final HTML by wrapping the body with the template below:

```python
import sys
from datetime import datetime

title = sys.argv[1]
author = sys.argv[2]
date = sys.argv[3]
doi = sys.argv[4] if len(sys.argv) > 4 else ''
description = sys.argv[5] if len(sys.argv) > 5 else ''
license_name = sys.argv[6] if len(sys.argv) > 6 else 'QNFO Unified License Agreement (QNFO-ULA)'
stylesheet = sys.argv[7] if len(sys.argv) > 7 else 'stylesheets/papers.css'
extra_macros_json = sys.argv[8] if len(sys.argv) > 8 else '{}'
ga4_id = sys.argv[9] if len(sys.argv) > 9 else ''

with open('_body.html', 'r', encoding='utf-8') as f:
    body_html = f.read()

# Build the full HTML page
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{author}">
<meta name="citation_title" content="{title}">
<meta name="citation_author" content="{author}">
<meta name="citation_date" content="{date}">
<meta name="citation_doi" content="{doi}">
<meta name="generator" content="QNFO Publication Pipeline — generated from canonical Markdown">
<link rel="stylesheet" href="{stylesheet}">
'''

# GA4 (only if measurement ID provided)
if ga4_id:
    html += f'''
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga4_id}');
</script>
'''

html += '''
<!-- ===== MATHJAX CONFIG (MUST come BEFORE script — CRITICAL) ===== -->
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true,
    processEnvironments: true,
    macros: {
'''

# QNFO Standard Macros (from canonical MATHJAX-CONFIG)
import json
standard_macros = {
    "ket": ["{|{#1}\\rangle}", 1],
    "bra": ["{\\langle{#1}|}", 1],
    "braket": ["{\\langle{#1}|{#2}\\rangle}", 2],
    "bmod": ["{\\ \\mathrm{mod}\\ }"],
    "Z": "{\\mathbb{Z}}",
    "Q": "{\\mathbb{Q}}",
    "C": "{\\mathbb{C}}",
    "R": "{\\mathbb{R}}",
    "F": "{\\mathbb{F}}",
    "N": "{\\mathbb{N}}",
    "Ocal": "{\\mathcal{O}}",
    "Scal": "{\\mathcal{S}}",
    "Ncal": "{\\mathcal{N}}",
    "Ccal": "{\\mathcal{C}}",
    "Hcal": "{\\mathcal{H}}",
    "Ucal": "{\\mathcal{U}}",
    "llbracket": "{\\llbracket}",
    "rrbracket": "{\\rrbracket}",
    "square": "{\\square}",
    "ge": "{\\geq}",
    "le": "{\\leq}",
    "sim": "{\\sim}",
    "otimes": "{\\otimes}",
    "oplus": "{\\oplus}",
    "Succ": "{\\succ}",
    "Chi": "{\\chi}",
    "mu": "{\\mu}",
    "la": "{\\lambda}", "LA": "{\\Lambda}",
    "al": "{\\alpha}", "be": "{\\beta}",
    "ga": "{\\gamma}", "GA": "{\\Gamma}",
    "de": "{\\delta}", "DE": "{\\Delta}",
    "ep": "{\\varepsilon}", "om": "{\\omega}",
    "OM": "{\\Omega}", "si": "{\\sigma}",
    "SI": "{\\Sigma}", "th": "{\\theta}",
    "TH": "{\\Theta}", "ph": "{\\phi}",
    "PH": "{\\Phi}", "ps": "{\\psi}",
    "PS": "{\\Psi}", "rh": "{\\rho}",
    "et": "{\\eta}", "xi": "{\\xi}",
    "XI": "{\\Xi}", "ze": "{\\zeta}",
    "pi": "{\\pi}", "PI": "{\\Pi}",
    "ta": "{\\tau}", "ka": "{\\kappa}",
    "io": "{\\iota}", "up": "{\\upsilon}",
    "UP": "{\\Upsilon}", "nu": "{\\nu}",
}

# Merge publication-specific macros
extra = json.loads(extra_macros_json) if extra_macros_json else {}
all_macros = {**standard_macros, **extra}

for key, value in all_macros.items():
    if isinstance(value, list):
        html += f'      "{key}": {json.dumps(value)},\n'
    else:
        html += f'      "{key}": "{value}",\n'

html += '''    }
  },
  options: {
    ignoreHtmlClass: 'no-mathjax',
    processHtmlClass: 'mathjax',
  },
  chtml: {
    displayAlign: 'left',
    displayIndent: '0',
  }
};
</script>
<!-- MathJax script loads AFTER config — DO NOT REORDER -->
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>

<header class="publication-header">
  <div class="publication-badge">QNFO/QWAV Research Publication</div>
  <h1>'''

html += title

html += '''</h1>
  <div class="publication-meta">
    <span>'''

html += author

html += '''</span>
    <span>'''

html += date

if doi:
    html += f'''</span>
    <span class="doi-badge">
      <a href="https://doi.org/{doi}">{doi}</a>
    </span>'''

html += f'''
    <span>{license_name}</span>
  </div>
</header>

<article class="article-body">
'''

html += body_html

html += '''
</article>

<footer class="publication-footer">
  <p>Generated from canonical Markdown source. Published under QNFO Unified License Agreement (QNFO-ULA).</p>
  <p>Hosted on Cloudflare Pages. Permanent archive: Zenodo.</p>
</footer>

</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'[OK] Assembled index.html ({len(html)} chars)')
```

Save to `_assemble_html.py`, execute, then verify:
```powershell
python _assemble_html.py "{{title}}" "{{author}}" "{{date}}" "{{doi}}" "{{description}}" "{{license}}" "{{stylesheet_path}}" '{{extra_macros}}' "{{ga4_measurement_id}}"
Test-Path index.html
Remove-Item _assemble_html.py, _body.html
```

### Step 4: Verify MathJax Config Order (MANDATORY)

```python
import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
config_pos = html.find('window.MathJax')
script_pos = html.find('MathJax-script')
if config_pos == -1:
    print('[BLOCKED] No MathJax config found in index.html!')
    sys.exit(1)
if script_pos == -1:
    print('[BLOCKED] No MathJax script found in index.html!')
    sys.exit(1)
if config_pos > script_pos:
    print('[BLOCKED] MathJax config AFTER script! Render will FAIL.')
    print(f'  Config at pos {config_pos}, Script at pos {script_pos}')
    print('  Swap the order: config MUST come before script tag.')
    sys.exit(1)
print(f'[OK] MathJax config before script: config@{config_pos}, script@{script_pos}')
```

**GATE:** If config is AFTER script → `[BLOCKED: MathJax order]`. Fix before deploying.

### Step 5: Verify Content Fidelity

```python
import markdown
with open("{{canonical_md_path}}", 'r', encoding='utf-8') as f:
    md = f.read()
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Verify all math delimiters preserved
md_dollars = md.count('$')
html_dollars = html.count('$')
print(f'Markdown $ count: {md_dollars}')
print(f'HTML $ count: {html_dollars}')
if html_dollars < md_dollars * 0.8:
    print('[WARN] Math content may have been lost during conversion!')
```

---

## OUTPUT STRUCTURE

```
project/
├── paper.md              ← CANONICAL Markdown source
├── index.html            ← Generated HTML page (from template)
├── stylesheets/
│   └── papers.css        ← Publication stylesheet
├── paper.pdf             ← Generated PDF (from pdf-builder)
└── ARTIFACT-MANIFEST.json ← All artifacts catalogued
```

**HARD RULE:** `index.html` is ALWAYS generated from `paper.md`. Never edit HTML directly. The Markdown is the single source of truth. If the HTML needs fixing, fix the Markdown and regenerate.

---

## DEPLOYMENT

After generation and verification, deploy via Cloudflare Pages:

```bash
wrangler pages deploy . --project-name {{project_name}} --branch {{branch}}
```

Post-deploy: verify MathJax renders correctly on the live URL using the verification protocol from MATHJAX-CONFIG.md.

---

*HTML-PUBLICATION-PAGE v1.0 — Generate HTML publication pages from canonical Markdown with correct MathJax ordering. Config before script. Always.*
