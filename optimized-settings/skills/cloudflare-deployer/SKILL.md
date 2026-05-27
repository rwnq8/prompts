---
name: cloudflare-deployer
description: Deploy static sites, upload files to R2, run Workers, and manage Cloudflare Sandboxes. Use when the agent needs to deploy or manage Cloudflare resources.
tools: exec, fill_prompt_template
---
# Cloudflare Deployer

## When to Use
- Deploying static sites to Cloudflare Pages
- Uploading files to R2 buckets (zero egress fees)
- Deploying Workers (edge compute)
- Running Sandboxes (full Linux VMs, replaces GitHub Actions)
- Any Cloudflare resource management

## Quick Start
```bash
# Verify environment
wrangler --version    # Must be v3.0+ (current: v4.95.0)
wrangler whoami       # Must show authenticated account
```

## Workflow
1. Run startup checklist (version check + auth)
2. Identify resource type: Pages, R2, Workers, or Sandboxes
3. Execute deployment commands (see Reference)
4. Post deployment evidence to GitHub Issue
5. Verify deployment with HTTP status check

## CNAME FIRST RULE (CRITICAL)
**Create CNAME DNS record BEFORE adding domain to Pages.**
Adding domain before CNAME → verification failure → HTTP 522.
Six documented failures in deployment reference.

## Reference Commands

### Pages (Static Sites)
```bash
wrangler pages deploy --project-name <name> --branch main
wrangler pages project list
wrangler pages deployment list --project-name <name>
```

### R2 (Object Storage — Zero Egress)
```bash
wrangler r2 object put <bucket>/path --file ./local/file.pdf
wrangler r2 object list <bucket>
wrangler r2 bucket list
```

### Workers (Edge Compute)
```bash
wrangler deploy --name <worker-name>
wrangler deployments list
wrangler tail <worker-name>  # Live logs
```

### Sandboxes (Full Linux VMs)
```bash
wrangler sandbox exec <name> -- "<command>"
wrangler sandbox list
wrangler sandbox create <name>
```

### Auth
```bash
# Prefer API token (autonomous agent compatible)
$env:CLOUDFLARE_API_TOKEN = "<token>"

# OAuth login (NOT compatible with autonomous agents)
wrangler login  # Requires browser — avoid in agent mode
```

## Cost Gate (Free Tier)
| Resource | Free Tier | Overage |
|:---------|:----------|:--------|
| Pages builds | 500/month | Builds queue |
| Pages bandwidth | Unlimited | N/A |
| Workers requests | 100k/day | $0.30/million |
| R2 storage | 10 GB | $0.015/GB/month |
| R2 egress | **Free** | N/A |
| Sandboxes | Free quota | $0.002/min |

## Failure Scenarios
| Failure | Cause | Recovery |
|:--------|:------|:---------|
| wrangler not found | Not installed | `npm install -g wrangler` |
| Auth failed | No API token | Set CLOUDFLARE_API_TOKEN |
| CNAME not created | Domain added before CNAME | Remove domain, create CNAME, re-add |
| Build failed | Code error | Check build logs: `wrangler pages deployment tail` |
| Rate limited | Too many requests | Wait 60s, retry once |

## Deployment Evidence Template
```markdown
## Cloudflare Deploy
| Field | Value |
|:------|:------|
| URL | https://... |
| Status | HTTP 200 |
| Cost | $0.00 (free tier) |
```
Post to parent GitHub Issue via `gh issue comment`.
