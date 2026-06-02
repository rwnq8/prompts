---
name: cloudflare-deployer
description: Cloudflare platform deployment operations — Pages, R2, Workers, Vectorize, DNS, redirects, and Sandboxes. Use when the agent needs to deploy, manage, or troubleshoot Cloudflare infrastructure.
version: "1.1"
---

# CLOUDFLARE DEPLOYER SKILL — v1.1

> **On-demand skill.** Load via `skill_view('cloudflare-deployer')` for all Cloudflare operations.
> Source: `templates/CLOUDFLARE-DEPLOYMENT.md` v2.1 + QWAV-DEFAULT.md §0.6.5-0.6.7

---

## ⚠️ WRANGLER v4.95+ COMPATIBILITY

**`r2 object list` was REMOVED in wrangler v4.95+.** Only `get`, `put`, `delete` are available.
The `--remote` flag is deprecated (remote is default in v4+). For directory enumeration, deploy a list-objects Worker or use per-object `get` operations.

---



## Tools Required

This skill is designed for use with QNFO agent tools. When loaded by a DEFAULT.md agent, the full tool suite (read, write, edit, exec, process, brave_web_search, YoBrowser, subagent_orchestrator) is available.

## QNFO Custom Skill Note

This is a QNFO custom skill deployed via `_deploy.py` (R2: `qnfo/tools/deploy.py`). It is NOT accessible via `skill_view()` (which only indexes DeepChat's built-in registry). Load it with:

```
read('G:\My Drive\prompts\skills\cloudflare-deployer\SKILL.md')
```



## Authentication

**⚠️ MANDATORY:** Load the API token from the persistent file BEFORE any Cloudflare operations. The `wrangler` OAuth token has zone:read only — CANNOT do DNS writes or redirect management.

```bash
# MANDATORY — Load FULL-ACCESS API token:
$env:CLOUDFLARE_API_TOKEN = (Get-Content "C:\Users\LENOVO\.cloudflare\api-token" -Raw).Trim()

# Verify
npx wrangler whoami
```

**Token scopes (API token):** zone:write, DNS:edit, redirect rules, Pages, Workers, R2, D1, Vectorize — FULL account access.
**OAuth scopes (wrangler):** zone:read only — DNS reads work, DNS WRITES and redirects FAIL.

For direct API calls (DNS, redirects, zone management), use the API token with Bearer auth:
```bash
curl -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" https://api.cloudflare.com/client/v4/...
```

**Account:** quniverse (edb167b78c9fb901ea5bca3ce58ccc4b)
**Email:** rwnquni@outlook.com

---

## Cloudflare Pages

```bash
# List all Pages projects
npx wrangler pages project list

# Deploy
npx wrangler pages deploy <dir> --project-name <name> --branch main

# Custom domain
npx wrangler pages project set-domain <name> <domain>

# Deployment history
npx wrangler pages deployment list --project-name <name>

# Rollback
npx wrangler pages deployment rollback --project-name <name>
```

**Active Projects:** qwav (deep.qwav.tech), prompts-wiki, qnfo-archive (archive.qnfo.org),
quantum-laws-of-form (laws.qnfo.org), qlof-primer (primer.qwav.tech), +11 more.

---

## Cloudflare R2 (Object Storage)

```bash
# Get an object (v4.95+ compatible)
npx wrangler r2 object get qnfo/audit/state/<project>.json

# Put an object
npx wrangler r2 object put qnfo/audit/state/<project>.json --file=<local-file>

# Delete an object
npx wrangler r2 object delete qnfo/audit/state/<project>.json

# NOTE: r2 object list does NOT exist in v4.95+
# Use per-object get operations instead
```

**Primary bucket:** `qnfo`
**R2 paths:** `qnfo/audit/state/`, `qnfo/audit/backlog/`, `qnfo/audit/decisions/`,
`qnfo/releases/`, `qnfo/deployments/`

---

## Cloudflare Workers

```bash
# Deploy a worker
npx wrangler deploy --name <worker-name>

# Deployment history
npx wrangler deployments list
```

---

## Cloudflare Sandboxes

```bash
# Create
npx wrangler sandbox create <name> --image ubuntu-22.04

# Execute
npx wrangler sandbox exec <name> -- "<command>"

# List
npx wrangler sandbox list

# Stop (cost: $0 when paused)
npx wrangler sandbox stop <name>
```

---

## Vectorize (Semantic Search)

For paper vectorization, use:
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/vectorize-papers.py --remote --file=_vectorize-papers.py
python _vectorize-papers.py
# Discard: Remove-Item _vectorize-papers.py
```

---

## Cost Gate

| Resource | Free Tier | Overage |
|:---------|:----------|:--------|
| Pages builds | 500/month | Builds queue |
| Pages bandwidth | Unlimited | N/A |
| Workers requests | 100k/day | $0.30/M |
| R2 storage | 10 GB | $0.015/GB/mo |
| R2 egress | **Free** | N/A |
| Sandboxes | Free quota | $0.002/min |

---

## Common Patterns

### Deploy a Publication
```bash
# 1. Build PDF
# Pull from R2: npx wrangler r2 object get qnfo/tools/build_pdf.py --remote --file=_build_pdf.py
python _build_pdf.py
# Discard: Remove-Item _build_pdf.py --input <file>

# 2. Deploy to Pages
npx wrangler pages deploy <dir> --project-name qwav --branch main

# 3. Upload PDF to R2
npx wrangler r2 object put qnfo/releases/<file>.pdf --file=<path>

# 4. Generate SEO
# Pull from R2: npx wrangler r2 object get qnfo/tools/generate-seo.py --remote --file=_generate-seo.py
python _generate-seo.py
# Discard: Remove-Item _generate-seo.py
```

### Check Infrastructure Health
```bash
npx wrangler whoami
npx wrangler pages project list
npx wrangler r2 object get qnfo/audit/state/qwav.json
```

---

## Reference Files

- Full deployment template: `templates/CLOUDFLARE-DEPLOYMENT.md`
- Cloudflare audit: `G:\My Drive\QWAV\SESSION-HANDOFF-2026-05-28.md`
- SEO generator: `_generate-seo.py` (R2: `qnfo/tools/generate-seo.py`)
- Vectorize: `_vectorize-papers.py` (R2: `qnfo/tools/vectorize-papers.py`)

---


## Embedded Scripts

> **SELF-CONTAINED:** This skill depends on the scripts listed below. Before executing any script, verify it exists at its canonical path.

| Script | R2 Canonical | Execution Cache | Purpose |
|:-------|:-------------|:----------------|:--------|
| `vectorize-papers.py` | `qnfo/tools/\vectorize-papers.py` | Index papers in Cloudflare Vectorize for semantic search |
| `build_pdf.py` | `qnfo/tools/\build_pdf.py` | Markdown/HTML -> PDF (shared with publication-publisher) |

### Bootstrap Protocol

Before using any script, verify it exists:
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py
# Verify: Test-Path _<script>.py
```

**If script is MISSING:** Scripts are version-controlled in the prompts repo.
1. `git log --oneline -- G:/My Drive/tools/<script>.py`
2. The canonical source for all tools is R2 (`qnfo/tools/`). Pull from R2: `npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py`.

**Shared scripts:** `build_pdf.py` is primarily maintained in the `publication-publisher` skill.
If missing, check that skill's Embedded Scripts section for recovery guidance.

### Dependencies
- `vectorize-papers.py`: requires Cloudflare API token (`%USERPROFILE%\.cloudflare\api-token`) and Workers AI access
- `build_pdf.py`: requires `reportlab` and optionally `markdown` packages


*cloudflare-deployer skill v1.1 — Load on-demand via skill_view(). Compatible with wrangler v4.95+*

---

*cloudflare-deployer v1.1 — QNFO custom skill. Load via read('G:\\My Drive\\prompts\\skills\\cloudflare-deployer\\SKILL.md'). Not accessible via skill_view().*
