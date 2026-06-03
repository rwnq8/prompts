---
name: publication-publisher
description: End-to-end publication workflow — formatting, PDF building, Zenodo upload, Cloudflare deployment, and social media orchestration. Use when publishing papers, reports, or other documents.
version: "1.3"
---

# PUBLICATION PUBLISHER SKILL — v1.3

> **On-demand skill.** Load via `skill_view('publication-publisher')` for publication workflows.
> Source: DEFAULT.md §11 + `ZENODO-PUBLISH.md` + `pdf-builder` skill

---

## Publication Pipeline

```
Draft Complete → Format (§11) → Build PDF → Zenodo Upload → Cloudflare Deploy → Social Posts
```

---



## Tools Required

This skill is designed for use with QNFO agent tools. When loaded by a DEFAULT.md agent, the full tool suite (read, write, edit, exec, process, brave_web_search, YoBrowser, subagent_orchestrator) is available.

## QNFO Custom Skill Note

This is a QNFO custom skill deployed via `_deploy.py` (pulled from R2: `qnfo/tools/deploy.py`). It is NOT accessible via `skill_view()` (which only indexes DeepChat's built-in registry). Load it with:

```
read('G:\My Drive\prompts\skills\publication-publisher\SKILL.md')
```



## Step 1: Format (§11 Standards)

### Visible Author Block (MANDATORY)
Every release document must start with:
```
**Author:** Rowan Quni-Gudzinas | **Date:** YYYY-MM-DD | **License:** CC BY 4.0
```

### Curly Quotes
All publication documents use curly/smart quotes (Unicode: \u201c \u201d \u2018 \u2019). Code blocks exempt.

### Pre-Publication Checklist
- [ ] Visible Author Block present
- [ ] Curly quotes applied
- [ ] REVIEWER subagent passed fabrication audit
- [ ] All file references verified (`Test-Path`)
- [ ] Git log confirms all changes committed
- [ ] PDF generated
- [ ] **PDF rendering verified — no `\ufffd` characters, em dashes/curly quotes render correctly**
- [ ] **Zenodo duplicate check passed — no existing record for this publication (or updating existing)**
- [ ] Cloudflare Pages deployed and URL verified

---

## Step 2: Build PDF

Use `skill_view('pdf-builder')` to load the skill, then follow its workflow:
1. Verify prerequisites: `python -c "import reportlab, matplotlib; print('OK')"`
2. Build: `python "G:\My Drive\prompts\skills\pdf-builder\scripts\build_pdf.py" --input "paper.md" --output "paper.pdf"`
3. Verify rendering (MANDATORY): See skill's Step 4 for the fitz verification script.

For math-free drafts, add `--no-math` for lighter/faster builds.

### PDF Rendering Verification (MANDATORY)
After building PDF, extract text and verify ALL Unicode characters render correctly:
```bash
python -c "
import fitz
doc = fitz.open('output.pdf')
text = ''.join(page.get_text() for page in doc)
# Check for replacement character (corrupted Unicode)
if '\ufffd' in text:
    print('[BLOCKED] PDF contains Unicode replacement characters! Fix font encoding.')
    print('First occurrence:', text[max(0,text.index('\ufffd')-20):text.index('\ufffd')+20])
else:
    print('[OK] No replacement characters found.')
# Check key typographic characters
for char, name in [('\u2014','em dash'), ('\u201c','left curly quote'), ('\u201d','right curly quote')]:
    count = text.count(char)
    print(f'[{chr(0x2713) if count>0 else chr(0x2717)}] {name}: {count} found')
"
```
If ANY character fails: PDF is NOT publication-ready. Fix font encoding in `build_pdf.py` BEFORE proceeding.

---

## Step 3: Zenodo Upload

**Zenodo Duplicate Prevention (MANDATORY — execute BEFORE creating any record):**

1. Check for existing Zenodo record by searching the Discovery Index for a prior DOI for this publication title:
```bash
python -c "import json; d=json.load(open('_discovery_index.json','r',encoding='utf-8')); pubs=[p for p in d.get('publications',[]) if '<publication_title>' in p.get('title','')]; print(json.dumps(pubs, indent=2))" (via script file)
```
2. If existing DOI found → use `--doi <existing_doi>` flag to create a NEW VERSION (not a duplicate record):
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/zenodo_publish.py --remote --file=_zenodo_publish.py
python _zenodo_publish.py --doi "<existing_doi>" --title "..." --author "..." --file "..."
# Discard: Remove-Item _zenodo_publish.py
```
3. If Zenodo API search needed: use `brave_web_search` for `site:zenodo.org "<publication_title>"` to find existing records.
4. Never create a new Zenodo record (`zenodo_publish.py` without `--doi`) for a publication that already has one. This creates DUPLICATE records.
5. If unsure whether a record exists: search first. Create only when search returns zero results.

After duplicate check passes, use `fill_prompt_template("ZENODO-PUBLISH", {...})` then:
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/zenodo_publish.py --remote --file=_zenodo_publish.py
python _zenodo_publish.py
# Discard: Remove-Item _zenodo_publish.py
```

---

## Step 4: Cloudflare Deploy

> **HARD RULE:** NEVER create a new Cloudflare Pages project for an existing publication resource. All QNFO publications deploy under the single `qwav` umbrella project via subdirectory routing (e.g., `/papers/<slug>/`). Creating additional Pages projects for the same resource clutters the dashboard, wastes quota, and creates maintenance burden.

### Pre-Deploy Checklist
- [ ] Verify the target deployment uses `--project-name qwav` (NEVER a new project)
- [ ] Verify the publication deploys to a subdirectory path: `/papers/<kebab-case-title>/`
- [ ] Verify no duplicate R2 artifact already exists at `qnfo/releases/<file>.pdf`

```bash
# Deploy to Cloudflare Pages
npx wrangler pages deploy <dir> --project-name qwav --branch main

# Upload PDF to R2
npx wrangler r2 object put qnfo/releases/<file>.pdf --file=<path>

# Generate SEO files
# Pull from R2: npx wrangler r2 object get qnfo/tools/generate-seo.py --remote --file=_generate-seo.py
python _generate-seo.py
# Discard: Remove-Item _generate-seo.py
```

---

## Step 5: Social Media Orchestration

Use `fill_prompt_template("SOCIAL-ORCHESTRATOR-TEMPLATE", {...})` to generate posts for all channels.
Post via Buffer API `create_post` tool with `schedulingType: "notification"` for manual approval.

**Channels:** Twitter/X, Bluesky, LinkedIn (Mastodon pending Buffer plan upgrade)

---

## Descriptive Filenames

Use descriptive publication filenames (DEFAULT.md §10):
```
QUANTUM-ERROR-CORRECTION-ULTRAMETRIC-v1.0.pdf
```
NOT: `paper.pdf`, `final.pdf`, `output.pdf`

---


## Embedded Scripts

> **SELF-CONTAINED:** This skill depends on the scripts listed below. Before executing any script, verify it exists at its canonical path. If missing, see the bootstrap note below for recovery.

| Script | R2 Canonical | Execution Cache | Purpose |
|:-------|:-------------|:----------------|:--------|
| `zenodo_publish.py` | `qnfo/tools/zenodo_publish.py` | `_zenodo_publish.py` (ephemeral) | Zenodo DOI registration via REST API |
| `generate-seo.py` | `qnfo/tools/generate-seo.py` | `_generate-seo.py` (ephemeral) | sitemap.xml, robots.txt, llms.txt generator |

> **Note:** `build_pdf.py` is now bundled in the `pdf-builder` skill (`skills/pdf-builder/scripts/build_pdf.py`). Use `skill_view('pdf-builder')` for PDF generation. R2 backup at `qnfo/tools/build_pdf.py`.

### Bootstrap Protocol

**Before using any script, verify it exists:**
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py
# Verify pull: Test-Path _<script>.py
```

**If script is MISSING:** Scripts are canonical on Cloudflare R2 (`qnfo/tools/`). Pull from R2: `npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py`.
1. Re-pull from R2: `npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py`
2. Check: are you on the correct branch? `git branch --show-current`
3. The canonical source for all tools is the `prompts` repo `tools/` directory.

**Last resort:** If all scripts are missing and unrecoverable from git, flag as `[BLOCKED: missing tools]`.
DO NOT attempt publication without these scripts.

### Dependencies
- `build_pdf.py`: requires `reportlab` and optionally `markdown` packages
- `zenodo_publish.py`: requires `%USERPROFILE%\.zenodo_token` (Zenodo API token with deposit:actions, deposit:write)
- `generate-seo.py`: standard library only, no external dependencies

### Cross-Reference
- `build_pdf.py` is now bundled in the `pdf-builder` skill (`skill_view('pdf-builder')`)
- These scripts are embedded in the `publication-publisher` skill as their primary documentation home

## Reference Files

- Publication standards: DEFAULT.md §11
- PDF builder: `skill_view('pdf-builder')` (bundled skill with `scripts/build_pdf.py`)
- Zenodo: `templates/ZENODO-PUBLISH.md`
- Social orchestrator: `templates/SOCIAL-ORCHESTRATOR-TEMPLATE.md`
- Cloudflare deploy: `templates/CLOUDFLARE-DEPLOYMENT.md`

---

*publication-publisher skill v1.3 — Load on-demand via skill_view()*

---

*publication-publisher v1.3 — QNFO custom skill. Load via read('G:\\My Drive\\prompts\\skills\\publication-publisher\\SKILL.md'). Not accessible via skill_view().*
