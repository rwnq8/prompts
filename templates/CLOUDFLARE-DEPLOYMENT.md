---
template: CLOUDFLARE-DEPLOYMENT
version: "1.0"
parameters:
  - name: action
    type: string
    required: true
    description: "Operation to perform: deploy-pages, upload-r2, deploy-worker, migrate-pages-from-github, sandbox-build, audit, configure"
  - name: project_name
    type: string
    required: true
    description: "Project identifier matching GitHub repo name"
  - name: repo
    type: string
    required: false
    description: "Full GitHub repo path (e.g., rwnq8/quantum-laws-of-form)"
  - name: domain
    type: string
    required: false
    description: "Custom domain for Cloudflare Pages"
  - name: branch
    type: string
    required: false
    default: "main"
    description: "Git branch to deploy from"
  - name: build_command
    type: string
    required: false
    description: "Build command for Cloudflare Pages"
  - name: output_dir
    type: string
    required: false
    default: "/"
    description: "Output directory for built site"
  - name: r2_bucket
    type: string
    required: false
    description: "R2 bucket name for storage operations"
  - name: file_pattern
    type: string
    required: false
    description: "Glob pattern for file uploads"
---

# CLOUDFLARE DEPLOYMENT — {{action}} for {{project_name}}

> **⚠️ PLATFORM AWARENESS:** Cloudflare-native deployment for QWAV public-facing assets.
> Cloudflare already hosts QWAV domains (qwav.tech, quni.cloud) via DNS.
> **⚠️ DUAL-PLATFORM MODEL:** GitHub = git + Issues. Cloudflare = hosting + storage + compute.
> **⚠️ COST GATE:** Check free tier thresholds before any operation (Pages: 500 builds/mo, R2: 10GB, Workers: 100k/day).

---

## 0. PREREQUISITES

**⚠️ AGENT AUTH CRITICAL:** The `wrangler login` OAuth flow is **incompatible with autonomous agent execution** — it requires manual browser credential entry. Use `CLOUDFLARE_API_TOKEN` environment variable instead for non-interactive auth.

```bash
# Agent-compatible auth (PREFERRED):
set CLOUDFLARE_API_TOKEN=<global-api-key>
# OR: set CLOUDFLARE_API_TOKEN=<api-token-with-scopes>

# Verify:
wrangler --version          # Must be v3.0+
wrangler whoami             # Must show authenticated account
wrangler pages project list # Active Pages projects

# Interactive auth (HUMAN ONLY — do NOT use in agent execution):
# wrangler login            # Opens browser — requires manual credential entry
```

---

## 1. OPERATION: deploy-pages

Deploy a static site from GitHub to Cloudflare Pages.

```bash
# First-time setup:
wrangler pages project create {{project_name}} --production-branch {{branch}}

# Deploy:
wrangler pages deploy --project-name {{project_name}} --branch {{branch}} \
  --build-command "{{build_command}}" --build-output-directory {{output_dir}}

# Custom domain:
wrangler pages project set-domain {{project_name}} {{domain}}

# Verify:
wrangler pages deployment list --project-name {{project_name}}
curl -sI https://{{domain}} | head -5
```

---

## 2. OPERATION: upload-r2

Upload files to R2 (zero egress fees).

```bash
# Create bucket:
wrangler r2 bucket create {{r2_bucket}}

# Upload:
wrangler r2 object put {{r2_bucket}}/path/file.pdf --file ./local/file.pdf

# List:
wrangler r2 object list {{r2_bucket}}
```

---

## 3. OPERATION: deploy-worker

Deploy edge compute via Workers.

```bash
wrangler init {{project_name}}-worker
wrangler deploy --name {{project_name}}-worker
```

---

## 4. OPERATION: migrate-pages-from-github

Migrate an existing GitHub Pages site with zero downtime.

```bash
# 1. Audit current Pages:
gh api /repos/{{repo}}/pages --jq '{status, cname, branch: .source.branch, path: .source.path}'

# 2. Create Cloudflare Pages project:
wrangler pages project create {{project_name}} --production-branch {{branch}}
wrangler pages deploy --project-name {{project_name}} --branch {{branch}} --build-output-directory {{output_dir}}

# 3. Test on pages.dev:
curl -sI https://{{project_name}}.pages.dev

# 4. Add custom domain:
wrangler pages project set-domain {{project_name}} {{domain}}

# 5. Verify DNS:
dig +short {{domain}}

# 6. Disable GitHub Pages after 24h verification:
gh api /repos/{{repo}}/pages -X DELETE
```

---

## 5. OPERATION: sandbox-build

Run heavy builds in Cloudflare Sandboxes ($0.002/min).

```bash
wrangler sandbox create {{project_name}}-build --image ubuntu-22.04
wrangler sandbox exec {{project_name}}-build -- "git clone https://github.com/{{repo}}.git && cd {{project_name}} && make pdf"
wrangler sandbox stop {{project_name}}-build
```

---

## 6. OPERATION: audit

Compare GitHub vs Cloudflare usage.

```bash
# Cloudflare:
wrangler pages project list
wrangler r2 bucket list

# GitHub:
gh api /orgs/QNFO/settings/billing/usage --jq '.usageItems[] | select(.product=="actions") | "\(.repositoryName): \(.quantity) min"'
gh api /users/rwnq8/settings/billing/usage --jq '.usageItems[] | select(.product=="actions") | "\(.repositoryName): \(.quantity) min"'
gh repo list rwnq8 --limit 50 --json name,hasPagesEnabled --jq '.[] | select(.hasPagesEnabled==true) | .name'
```

---

## 7. ERROR HANDLING

| Scenario | Response |
|:---------|:---------|
| `wrangler` not installed | `[BLOCKED: npm install -g wrangler]` |
| Not authenticated | `wrangler login` |
| Build fails | Check logs, retry 3x |
| Rate limit (429) | Wait 60s, retry 3x |
| Domain conflict | Remove from other project, retry |

All commands retry 3x with exponential backoff (1s, 4s, 16s).

---

## 8. POST-OPERATION CHECKLIST

- [ ] Deployment URL verified (curl 200)
- [ ] Custom domain resolves (dig)
- [ ] HTTPS enforced
- [ ] GitHub Issue updated with deployment evidence
- [ ] Cost recorded (if Sandbox used)

---

*Cloudflare Deployment Template v1.0 — QWAV prompts ecosystem. Dual-platform: GitHub for git + Cloudflare for hosting.*
