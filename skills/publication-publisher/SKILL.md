---
name: publication-publisher
description: End-to-end publication workflow — formatting, PDF building, Zenodo upload, Cloudflare deployment, and social media orchestration. Use when publishing papers, reports, or other documents.
version: "1.0"
---

# PUBLICATION PUBLISHER SKILL — v1.0

> **On-demand skill.** Load via `skill_view('publication-publisher')` for publication workflows.
> Source: DEFAULT.md §11 + `ZENODO-PUBLISH.md` + `PDF-BUILDER-TEMPLATE.md`

---

## Publication Pipeline

```
Draft Complete → Format (§11) → Build PDF → Zenodo Upload → Cloudflare Deploy → Social Posts
```

---

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
- [ ] PDF generated and verified

---

## Step 2: Build PDF

Use `fill_prompt_template("PDF-BUILDER-TEMPLATE", {source, output, ...})` to generate PDF configuration, then:
```bash
python "G:\My Drive\prompts\tools\build_pdf.py"
```

---

## Step 3: Zenodo Upload

Use `fill_prompt_template("ZENODO-PUBLISH", {...})` then:
```bash
python "G:\My Drive\prompts\tools\zenodo_publish.py"
```

---

## Step 4: Cloudflare Deploy

```bash
# Deploy to Cloudflare Pages
npx wrangler pages deploy <dir> --project-name qwav --branch main

# Upload PDF to R2
npx wrangler r2 object put qnfo/releases/<file>.pdf --file=<path>

# Generate SEO files
python "G:\My Drive\prompts\tools\generate-seo.py"
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

## Reference Files

- Publication standards: DEFAULT.md §11
- PDF builder: `templates/PDF-BUILDER-TEMPLATE.md`
- Zenodo: `templates/ZENODO-PUBLISH.md`
- Social orchestrator: `templates/SOCIAL-ORCHESTRATOR-TEMPLATE.md`
- Cloudflare deploy: `templates/CLOUDFLARE-DEPLOYMENT.md`

---

*publication-publisher skill v1.0 — Load on-demand via skill_view()*
