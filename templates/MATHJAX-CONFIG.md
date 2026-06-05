---
template: MATHJAX-CONFIG
version: "1.0"
date: 2026-06-05
parameters:
  - name: output_format
    type: string
    required: true
    description: "Target format: html (web page), pdf-latex (for PDF via LaTeX), pdf-mathtext (for PDF via matplotlib mathtext)"
  - name: extra_macros
    type: string
    required: false
    default: ""
    description: "Additional LaTeX macro definitions (JSON object format) specific to the publication"
---

# MATHJAX CANONICAL CONFIGURATION — v1.0

> **SINGLE SOURCE OF TRUTH:** This is the canonical MathJax configuration for ALL QNFO/QWAV publications. Every HTML page, every PDF build, every Zenodo publication MUST derive its math rendering configuration from this template. Do NOT create ad-hoc MathJax configs.

---

## CRITICAL: Script Loading Order (HTML)

**MANDATORY ORDER — Config BEFORE Script.** This is the #1 MathJax rendering failure mode. The `MathJax` configuration object MUST be defined before the MathJax script loads. When MathJax 3 loads via `async`, it checks for `window.MathJax` immediately. If the config script comes after, MathJax initializes with defaults (no macros, no custom inline/delimiter config) and math will NOT render correctly.

```html
<!-- CORRECT ORDER -->
<script>
window.MathJax = { /* config here */ };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<!-- WRONG ORDER (WILL NOT RENDER) -->
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
window.MathJax = { /* config here */ };  /* TOO LATE — MathJax already initialized */
</script>
```

---

## HTML Configuration (Web — tex-mml-chtml)

For Cloudflare Pages and any web deployment, embed this BEFORE the MathJax CDN script:

```html
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    macros: {
      /* === QNFO Standard Macros (ALWAYS INCLUDE) === */
      "ket": ["{|{#1}\\rangle}", 1],
      "bra": ["{\\langle{#1}|}", 1],
      "braket": ["{\\langle{#1}|{#2}\\rangle}", 2],
      "bmod": ["{\\ \\mathrm{mod}\\ }"],
      /* Blackboard bold */
      "Z": "{\\mathbb{Z}}",
      "Q": "{\\mathbb{Q}}",
      "C": "{\\mathbb{C}}",
      "R": "{\\mathbb{R}}",
      "F": "{\\mathbb{F}}",
      "N": "{\\mathbb{N}}",
      /* Calligraphic */
      "Ocal": "{\\mathcal{O}}",
      "Scal": "{\\mathcal{S}}",
      "Ncal": "{\\mathcal{N}}",
      "Ccal": "{\\mathcal{C}}",
      "Hcal": "{\\mathcal{H}}",
      "Ucal": "{\\mathcal{U}}",
      /* Operators */
      "llbracket": "{\\llbracket}",
      "rrbracket": "{\\rrbracket}",
      "square": "{\\square}",
      "ge": "{\\geq}",
      "le": "{\\leq}",
      "sim": "{\\sim}",
      "otimes": "{\\otimes}",
      "oplus": "{\\oplus}",
      "Succ": "{\\succ}",
      /* Greek shortcuts */
      "Chi": "{\\chi}",
      "mu": "{\\mu}",
      "la": "{\\lambda}",
      "LA": "{\\Lambda}",
      "al": "{\\alpha}",
      "be": "{\\beta}",
      "ga": "{\\gamma}",
      "GA": "{\\Gamma}",
      "de": "{\\delta}",
      "DE": "{\\Delta}",
      "ep": "{\\varepsilon}",
      "om": "{\\omega}",
      "OM": "{\\Omega}",
      "si": "{\\sigma}",
      "SI": "{\\Sigma}",
      "th": "{\\theta}",
      "TH": "{\\Theta}",
      "ph": "{\\phi}",
      "PH": "{\\Phi}",
      "ps": "{\\psi}",
      "PS": "{\\Psi}",
      "rh": "{\\rho}",
      "et": "{\\eta}",
      "xi": "{\\xi}",
      "XI": "{\\Xi}",
      "ze": "{\\zeta}",
      "pi": "{\\pi}",
      "PI": "{\\Pi}",
      "ta": "{\\tau}",
      "ka": "{\\kappa}",
      "io": "{\\iota}",
      "up": "{\\upsilon}",
      "UP": "{\\Upsilon}",
      "nu": "{\\nu}",
      /* === Publication-specific macros (add below) === */
      {{#extra_macros}}{{{extra_macros}}}{{/extra_macros}}
    }
  },
  options: {
    ignoreHtmlClass: 'no-mathjax',
    processHtmlClass: 'mathjax',
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
    renderActions: {
      find_script: [10, function (doc) {
        for (const node of document.querySelectorAll('script[type^="math/tex"]')) {
          const display = !!node.type.match(/; *mode=display/);
          const math = new doc.options.MathItem(node.textContent, doc.inputJax[0], display);
          const text = document.createTextNode('');
          node.parentNode.replaceChild(text, node);
          math.start = {node: text, delim: '', n: 0};
          math.end = {node: text, delim: '', n: 0};
          doc.math.push(math);
        }
      }, '']
    }
  },
  chtml: {
    scale: 1.0,
    minScale: 0.5,
    matchFontHeight: true,
    mtextInheritFont: true,
    merrorInheritFont: true,
    mathmlSpacing: false,
    skipAttributes: {},
    exFactor: 0.5,
    displayAlign: 'left',
    displayIndent: '0'
  },
  svg: {
    scale: 1.0,
    minScale: 0.5,
    matchFontHeight: true,
    mtextInheritFont: true,
    merrorInheritFont: true,
    mathmlSpacing: false,
    skipAttributes: {},
    exFactor: 0.5,
    displayAlign: 'left',
    displayIndent: '0'
  }
};
</script>
<!-- MathJax script loads AFTER config is set -->
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

---

## PDF Configuration (LaTeX — for PDF builds)

When building PDF from Markdown via `build_pdf.py` (pdf-builder skill), math is rendered via matplotlib mathtext or LaTeX. The PDF builder handles math automatically — the canonical Markdown source uses standard LaTeX math delimiters (`$...$`, `$$...$$`) that work in BOTH HTML (via MathJax) and PDF (via LaTeX).

**No separate PDF math configuration is needed** — the canonical Markdown is the single source. The same `$...$` and `$$...$$` delimiters work in both output formats.

For PDF builds that require LaTeX compilation (not mathtext), use the standard QNFO preamble:
```latex
\usepackage{amsmath, amssymb, amsthm}
\usepackage{mathrsfs}
\usepackage{braket}
```

---

## Markdown-to-HTML Conversion Protocol

ALL HTML publication pages MUST be generated from canonical Markdown. Never write HTML by hand for publication content. The Markdown is the single source of truth — HTML is a derived output format.

### Conversion Pipeline

```
canonical.md → (pandoc or Python markdown) → body.html → WRAP in HTML template with MathJax → deploy
```

### Minimum HTML Wrapper

Every publication HTML page must include:
1. `<!DOCTYPE html>` + `<meta charset="UTF-8">`
2. Citation metadata (`<meta name="citation_*">`)
3. MathJax config (BEFORE script, per above)
4. MathJax CDN script (AFTER config)
5. Responsive viewport meta
6. Publication stylesheet link

---

## Verification Protocol (MANDATORY for every deploy)

Before ANY Cloudflare Pages deploy of a publication page, verify MathJax setup:

### 1. Config-Before-Script Check
```bash
python -c "
import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# Find MathJax config and script positions
config_pos = html.find('window.MathJax')
script_pos = html.find('MathJax-script')
if config_pos == -1:
    print('[BLOCKED] No MathJax config found!')
    sys.exit(1)
if script_pos == -1:
    print('[BLOCKED] No MathJax script found!')
    sys.exit(1)
if config_pos > script_pos:
    print('[BLOCKED] MathJax config AFTER script! Script must come AFTER config.')
    print(f'  Config at position {config_pos}')
    print(f'  Script at position {script_pos}')
    sys.exit(1)
print('[OK] MathJax config correctly placed BEFORE script.')
print(f'  Config at position {config_pos}')
print(f'  Script at position {script_pos}')
print(f'  Gap: {script_pos - config_pos} chars')
" (via script file)
```

### 2. Post-Deploy Live Verification
```bash
python -c "
import urllib.request, sys
url = sys.argv[1]
html = urllib.request.urlopen(url).read().decode('utf-8')
config_pos = html.find('window.MathJax')
script_pos = html.find('MathJax-script')
if config_pos == -1 or script_pos == -1:
    print(f'[BLOCKED] MathJax config/script missing from deployed page: {url}')
    sys.exit(1)
if config_pos > script_pos:
    print(f'[BLOCKED] MathJax config AFTER script on deployed page: {url}')
    sys.exit(1)
print(f'[OK] MathJax correctly configured on {url}')
" (via script file)
```

### 3. Macro Cross-Reference
Verify all LaTeX commands used in the Markdown source have corresponding MathJax macros defined in the HTML config. Run:
```bash
python -c "
import re, json, sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
with open('paper.md', 'r', encoding='utf-8') as f:
    md = f.read()
# Extract macros from MathJax config
macro_match = re.search(r'macros:\s*({[^}]+(?:{[^}]*})*[^}]*})', html, re.DOTALL)
if not macro_match:
    print('[WARN] Could not extract MathJax macros from HTML')
    sys.exit(0)
# Extract \commands from markdown
cmds = set(re.findall(r'\\[a-zA-Z]+', md))
print(f'LaTeX commands in Markdown: {len(cmds)}')
# This is a best-effort check — full validation needs a proper parser
print('[INFO] Manual review: verify all \\commands in paper.md have MathJax macros')
" (via script file)
```

---

## Integration Notes

- **DEFAULT.md** agents: Reference this template for ALL publication HTML generation.
- **QWAV-DEFAULT.md** agents: Same — use this canonical config for all QWAV portfolio pages.
- **publication-publisher skill**: Step 4 (Cloudflare Deploy) MUST include MathJax verification before deploying.
- **cloudflare-deployer skill**: Post-deploy verification MUST check MathJax config ordering.
- **pdf-builder skill**: Math rendering via matplotlib mathtext or LaTeX — no MathJax needed for PDF. Standard `$...$` / `$$...$$` delimiters work in both.

---

*MATHJAX-CONFIG v1.0 — Canonical math rendering configuration for ALL QNFO/QWAV publications. Config before script. Always.*
