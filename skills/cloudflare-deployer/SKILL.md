---
name: cloudflare-deployer
description: Complete Cloudflare platform automation — Pages, Workers (cron + HTTP), R2, Vectorize, D1, Queues, DNS, Bulk Redirects, Secrets. Covers Python Worker quirks, REST API fallbacks, audit trail patterns, and full worker lifecycle. Use when the agent needs ANY Cloudflare operation.
tools: exec, fill_prompt_template, read, write
---

# Cloudflare Deployer v2.0 — Complete Platform Automation

## When to Use
- Deploying static sites to Cloudflare Pages
- Creating/deploying Workers (HTTP, cron-triggered, Python or JS)
- Managing R2 buckets & objects (storage, audit trail, backups)
- Managing Vectorize indexes (embeddings, semantic search)
- Setting secrets for Workers
- Managing DNS records (requires REST API)
- Creating Bulk Redirect rules (requires REST API)
- Any Cloudflare resource lifecycle

## Quick Start
```bash
wrangler --version    # Must be v3.0+ (current: v4.95.0)
wrangler whoami       # Verify OAuth token + scopes
```

## Agent Authentication

Three methods, ranked by agent reliability:

| Method | Setup | Persistence | Use Case |
|:-------|:------|:------------|:---------|
| **OAuth Token** (`wrangler login`) | One-time via YoBrowser | ✅ Permanent (`%APPDATA%\xdg.config\.wrangler\config\default.toml`) | Primary — do this ONCE |
| **Global API Key** (`CLOUDFLARE_API_KEY` + `CLOUDFLARE_EMAIL`) | Per-session env vars | ❌ | REST API operations wrangler can't do |
| **API Token** (`CLOUDFLARE_API_TOKEN`) | Per-session env vars | ❌ | Scoped CI/CD operations |

```bash
# Verify OAuth (must show 20+ scopes including workers:write, r2:write, ai:write)
wrangler whoami

# For REST API operations (DNS, redirects, some domain ops):
$env:CLOUDFLARE_API_KEY = "<global-api-key>"
$env:CLOUDFLARE_EMAIL = "<account-email>"
# NOTE: Both required. API Key alone is insufficient.
```

### Account Identifiers
```
Account ID: edb167b78c9fb901ea5bca3ce58ccc4b (quniverse)
Zone IDs vary by domain — query via REST API or wrangler.
```

---

## 1. WORKERS — Complete Lifecycle

### 1.1 Cron Worker Deployment (Proven Pattern)

**STEP 1: Write Worker Code** (Python)
```python
# src/entry.py
from js import Response, Object, fetch, console
import json

async def scheduled(event, env, ctx):
    """Called by cron trigger — do work here"""
    token = env.MY_SECRET
    bucket = env.MY_BUCKET
    # ... work ...
    pass

async def on_fetch(request, env):
    """HTTP trigger for manual testing"""
    await scheduled(None, env, None)
    return Response.new("OK", Object.fromEntries([
        ["headers", Object.fromEntries([["Content-Type", "text/plain"]])]
    ]))
```

**CRITICAL Python Worker Quirks** (discovered 2026-05-27):
| Quirk | Wrong | Right |
|:------|:------|:------|
| Fetch options | Python dict `{"headers": {...}}` | `Object.fromEntries([...])` for ALL nested objects |
| Response headers | Python dict in Response.new() | `Object.fromEntries([...])` |
| wrangler get/delete | Without `--remote` | Always use `--remote` for get/delete |
| Compatibility | Default `compatibility_date` only | Add `compatibility_flags = ["python_workers"]` |
| **compatibility_date** | `compatibility_date >= "2026-01-01"` — server introspection fails: `ModuleNotFoundError: No module named 'workers'` | **Always use `compatibility_date = "2025-08-01"` for Python Workers (wrangler 4.95.0)** |
| Vectorize binding | `[[vectorize_indexes]]` | `[[vectorize]]` (singular) |
| R2 from Worker | `bucket.put(key, value)` Python string | Python strings auto-convert to JS |

**STEP 2: Write wrangler.toml**
```toml
name = "my-worker"
main = "src/entry.py"
compatibility_date = "2025-08-01"
compatibility_flags = ["python_workers"]

[triggers]
crons = ["0 6 * * *"]         # Daily at 06:00 UTC
# crons = ["*/15 * * * *"]    # Every 15 minutes

[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "qnfo"

[[vectorize]]
binding = "VECTORIZE"
index_name = "qwav-research"

[ai]
binding = "AI"
```

**STEP 3: Set Secrets**
```bash
cd <worker-project-dir>
echo "<secret-value>" | wrangler secret put MY_SECRET
wrangler secret list                    # Verify
```

**STEP 4: Deploy**
```bash
wrangler deploy                         # Deploys worker + cron triggers
# Output: https://<name>.q08.workers.dev
#         schedule: 0 6 * * *
```

**STEP 5: Verify**
```bash
wrangler whoami                         # Auth check
wrangler deployments list               # Confirm deployed
Invoke-RestMethod https://<name>.q08.workers.dev  # Trigger manually
wrangler tail <name>                    # Live logs (timeout after ~30s)
```

### 1.2 Worker Deletion
```bash
wrangler delete <name>
```

### 1.3 Worker Bindings Reference

| Binding Type | wrangler.toml Syntax | Access in Python Worker |
|:-------------|:---------------------|:------------------------|
| R2 Bucket | `[[r2_buckets]]` → `binding = "X"`, `bucket_name = "y"` | `env.X.put(key, value)` / `env.X.get(key)` |
| Vectorize | `[[vectorize]]` → `binding = "X"`, `index_name = "y"` | `env.X.query(vector)` / `env.X.insert(vectors)` |
| AI | `[ai]` → `binding = "X"` | `env.X.run(model, input)` |
| D1 Database | `[[d1_databases]]` → `binding = "X"`, `database_name = "y"` | `env.X.prepare(sql).run()` |
| Queue | `[[queues]]` → `binding = "X"`, `queue_name = "y"` | `env.X.send(message)` |
| Secret | Via `wrangler secret put` | `env.SECRET_NAME` (bare string) |
| Service (other Worker) | `[[services]]` → `binding = "X"`, `service = "y"` | `env.X.fetch(request)` |

---

## 2. R2 — Object Storage Operations

### 2.1 Bucket Management
```bash
wrangler r2 bucket list                      # All buckets
wrangler r2 bucket create <name>             # New bucket
wrangler r2 bucket delete <name>             # Delete (must be empty)
```

### 2.2 Object Operations (ALWAYS use --remote for get/delete)
```bash
# Upload
wrangler r2 object put <bucket>/path/to/file.md --file=./local/file.md
wrangler r2 object put qnfo/audit/data.json --remote --file=./data.json

# Download
wrangler r2 object get qnfo/audit/data.json --remote --file=./local-copy.json

# Delete
wrangler r2 object delete qnfo/audit/old-file.md --remote

# NOTE: `wrangler r2 object` has NO list subcommand.
# To list objects, use `wrangler r2 bucket` or the REST API.
```

### 2.3 R2 Audit Trail Pattern
```
qnfo/audit/
├── README.md                    ← Bucket documentation
├── conversations/               ← Agent session exports (.md)
├── github/                      ← GitHub Issues/Projects exports
│   ├── YYYY-MM-DD/              ← Dated snapshots
│   └── latest/                  ← Overwritten daily
├── decisions/                   ← DECISION-LOG.md
├── infrastructure/              ← State snapshots (.json)
└── wiki/                        ← GitHub Wiki mirror
```

### 2.4 Local vs. Remote Mode (CRITICAL)
| Operation | Without `--remote` | With `--remote` |
|:----------|:-------------------|:----------------|
| `object put` | ✅ Uploads (local mode, still works) | ✅ Uploads (explicit) |
| `object get` | ❌ Returns "key does not exist" (false negative) | ✅ Downloads correctly |
| `object delete` | ❌ Fails silently | ✅ Deletes correctly |

**Rule:** Always use `--remote` for `get` and `delete`. `put` works without it but using `--remote` is safer.

---

## 3. VECTORIZE — Semantic Search Indexes

### 3.1 Index Management
```bash
wrangler vectorize list                                      # All indexes
wrangler vectorize create <name> --dimensions=768 --metric=cosine
wrangler vectorize delete <name>
wrangler vectorize info <name>                               # Details + status
```

### 3.2 Vector Operations
```bash
# Insert vectors (from file)
wrangler vectorize insert <name> --file=./vectors.ndjson

# Upsert (insert or update)
wrangler vectorize upsert <name> --file=./vectors.ndjson

# Query (vector search)
wrangler vectorize query <name> --vector="[0.1, 0.2, ...]" --top-k=10

# Query with metadata filter
wrangler vectorize query <name> --vector="[...]" --filter='{"category": "decisions"}'

# List vectors
wrangler vectorize list-vectors <name>

# Get specific vectors
wrangler vectorize get-vectors <name> --ids=id1,id2,id3

# Delete vectors
wrangler vectorize delete-vectors <name> --ids=id1,id2
```

### 3.3 Metadata Indexes (Enable Filtering)
```bash
wrangler vectorize create-metadata-index <name> --property-name=category
wrangler vectorize list-metadata-index <name>
wrangler vectorize delete-metadata-index <name> --property-name=category
```

### 3.4 Vectorize + Workers AI Embedding Pattern
```python
# In Worker code: generate embedding → insert into Vectorize
async def on_fetch(request, env):
    # Generate embedding via Workers AI
    result = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
        "text": "What is quantum computing?"
    })
    embedding = result["data"][0]  # 768-dimensional vector

    # Insert into Vectorize
    await env.VECTORIZE.upsert([{
        "id": "doc-001",
        "values": embedding,
        "metadata": {"source": "paper-0.1.md", "category": "research"}
    }])

    # Query
    results = await env.VECTORIZE.query(embedding, {
        "topK": 5,
        "filter": {"category": "research"}
    })
```

---

## 4. PAGES — Static Site Deployment

### 4.1 CNAME FIRST RULE (CRITICAL — 6 documented failures)
**Create CNAME DNS record BEFORE adding domain to Pages.**
Adding domain before CNAME → verification failure → HTTP 522.

```bash
# STEP 1: Create CNAME via Cloudflare REST API
# STEP 2: THEN add domain to Pages via REST API
# STEP 3: Wait 30-60s for verification

# Deploy static files
wrangler pages deploy --project-name <name> --branch main

# Create Pages project (first time)
wrangler pages project create <name> --production-branch main
```

### 4.2 Domain Management (REST API — wrangler removed set-domain in v4.95)
```python
# Python script: _pages_domain.py
import requests
ACCOUNT_ID = "edb167b78c9fb901ea5bca3ce58ccc4b"

# 1. Add custom domain to Pages project
resp = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/<name>/domains",
    headers={"Authorization": f"Bearer {API_TOKEN}"},
    json={"name": "subdomain.example.com"}
)
# 2. Wait for verification (poll status)
```

---

## 5. SECRETS MANAGEMENT

```bash
wrangler secret put <key>        # Set/update (prompts for value or piped)
wrangler secret delete <key>     # Remove
wrangler secret list             # List all secrets (shows names only)
wrangler secret bulk <file>      # Upload multiple from JSON file
```

**Setting secrets non-interactively:**
```bash
echo "<secret-value>" | wrangler secret put GITHUB_TOKEN
```

---

## 6. DNS MANAGEMENT (REST API)

wrangler does NOT manage DNS. Use Cloudflare REST API:

```python
# _manage_dns.py
import requests, os

ZONE_ID = "<zone-id>"  # Get from Cloudflare Dashboard or API
API_TOKEN = os.environ["CLOUDFLARE_API_TOKEN"]

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# List records
resp = requests.get(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
    headers=headers
)

# Create CNAME
resp = requests.post(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
    headers=headers,
    json={
        "type": "CNAME",
        "name": "sub.example.com",
        "content": "target.pages.dev",
        "proxied": True,
        "ttl": 1  # Auto TTL
    }
)

# Create A record
resp = requests.post(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
    headers=headers,
    json={
        "type": "A",
        "name": "example.com",
        "content": "192.0.2.1",
        "proxied": True,
        "ttl": 1
    }
)
```

---

## 7. BULK REDIRECTS (REST API)

```python
# _create_redirects.py
import requests

ACCOUNT_ID = "edb167b78c9fb901ea5bca3ce58ccc4b"
headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}

# 1. Create redirect list
resp = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/rules/lists",
    headers=headers,
    json={
        "name": "my-redirects",
        "kind": "redirect",
        "description": "Domain redirects"
    }
)
list_id = resp.json()["result"]["id"]

# 2. Add items
resp = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/rules/lists/{list_id}/items",
    headers=headers,
    json=[{
        "redirect": {
            "source_url": "old.example.com/",
            "target_url": "new.example.com/",
            "status_code": 301,
            "include_subdomains": True
        }
    }]
)

# 3. Create Bulk Redirect Rule referencing the list
resp = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/rulesets",
    headers=headers,
    json={
        "name": "default",
        "kind": "zone",
        "phase": "http_request_redirect",
        "rules": [{
            "expression": "true",
            "action": "redirect",
            "action_parameters": {"from_list": {"name": "my-redirects", "key": "redirect"}}
        }]
    }
)
```

---

## 8. COST GATE (Free Tier — QWAV/QNFO)

| Resource | Free Tier | Current Usage | Status |
|:---------|:----------|:--------------|:------|
| Pages bandwidth | Unlimited | — | ✅ |
| Pages builds | 500/month | ~10 | ✅ |
| Workers requests | 100k/day | <1k | ✅ |
| Workers CPU | 10ms/request | <5ms | ✅ |
| R2 storage | 10 GB | ~85 MB | ✅ |
| R2 Class A ops | 1M/month | <1k | ✅ |
| R2 Class B ops | 10M/month | <1k | ✅ |
| Vectorize queries | 30M/month | <100 | ✅ |
| Vectorize storage | 5M vectors | 0 | ✅ |
| Cron triggers | 3 free | 1 (github-sync) | ✅ |
| Queues | 1M operations/month | 0 | ✅ |

---

## 9. FAILURE CATALOG (PoC-Verified, 2026-05-27)

| # | Symptom | Root Cause | Resolution |
|:--|:--------|:----------|:-----------|
| F1 | `wrangler pages project set-domain` → Unknown arguments | Removed in wrangler 4.95.0 | Use REST API |
| F2 | Domain verification: "CNAME not set" | CNAME created after domain | CNAME FIRST, then domain |
| F3 | HTTP 522 after domain add | CNAME missing | Delete domain, create CNAME, re-add |
| F4 | `CLOUDFLARE_API_TOKEN` → Invalid | Global Key needs both API_KEY + EMAIL | Set both env vars |
| F5 | Inline Python corrupted by PowerShell | PowerShell intercepts quotes/brackets | Write to temp file, execute file |
| F6 | DNS records lost | Session artifact cleanup | Re-create via REST API |
| F7 | Python Worker: R2 writes fail silently | Python dicts in fetch/Response options | Use Object.fromEntries() |
| F8 | `wrangler r2 object get` → "key does not exist" | Default local mode | Use `--remote` flag |
| F9 | `wrangler r2 object` no list subcommand | Not implemented in CLI | Use REST API or bucket-level list |
| F10 | Python Worker: `python_workers` compatibility flag required | Missing in wrangler.toml | Add `compatibility_flags = ["python_workers"]` |
| **F11** | `list_all_prompt_template_names()` missing new templates | Runtime caches pre-rebuild list | Restart DeepChat (F5 reload) to pick up new prompts.json |
| **F12** | wrangler stdout crashes Python subprocess: `UnicodeEncodeError: cp1252` | wrangler uses Unicode box-drawing chars (U+2500-U+257F) | `encoding='utf-8', errors='replace'` or `text=False` + manual decode |
| **F13** | GitHub API returns HTTP 200 with `[]` for flagged orgs | QNFO org flagged — API silently returns empty | Worker handles gracefully. Cannot distinguish "no issues" from "org flagged." |
| **F14** | Worker deploy fails: `ModuleNotFoundError: No module named 'workers'` in introspection.py | `compatibility_date >= "2026-01-01"` triggers new `workers` SDK introspection on server-side that doesn't exist yet (wrangler 4.95.0) | **Permanent fix: use `compatibility_date = "2025-08-01"` for ALL Python Workers.** Same date as working github-sync. Also triggered by `[[vectorize_indexes]]` — use `[[vectorize]]` (singular). |

---

## 10. DEPLOYMENT EVIDENCE TEMPLATE

After every Cloudflare operation, post evidence to the relevant GitHub Issue:

```markdown
## Cloudflare Deploy
| Field | Value |
|:------|:------|
| Resource | Worker: github-sync |
| URL | https://github-sync.q08.workers.dev |
| Cron | 0 6 * * * (daily) |
| Bindings | QNFO (R2), GITHUB_TOKEN (secret) |
| Deploy time | 13.35 sec |
| Status | [HTTP 200 verified] or [wrangler tail verified] |
| Cost | $0.00/mo (free tier) |
```

---

## 11. AGENT PATTERNS — When to Use What

| Task | Pattern | Example |
|:-----|:--------|:--------|
| Deploy a Worker | Write code → wrangler.toml → secrets → `wrangler deploy` | github-sync |
| Upload to R2 | `wrangler r2 object put --remote --file=...` | Audit trail export |
| Semantic search | Worker → AI.run() → Vectorize.query() | ask-qwav |
| Add DNS record | Python script → REST API POST | Domain setup |
| Bulk redirect | Python script → REST API (lists + rulesets) | Domain mirrors |
| Tail Worker logs | `wrangler tail <name>` (timeout ~30s) | Debugging |
| Session closeout | Export conversation → R2 audit/conversations/ | DEFAULT.md §10 |

---

*Cloudflare Deployer v2.0 — Updated 2026-05-27 with Python Worker quirks, Vectorize patterns, REST API fallbacks, and full worker lifecycle. Six failing patterns documented from PoC.*
