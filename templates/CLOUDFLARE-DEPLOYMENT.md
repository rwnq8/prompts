---
template: CLOUDFLARE-DEPLOYMENT
version: "2.1"
parameters:
  - name: action
    type: string
    required: true
    description: "Operation: deploy-pages, upload-r2, deploy-worker, migrate-pages-from-github, sandbox-build, audit, configure, domain-add, enable-analytics"
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
    description: "Custom domain for Cloudflare Pages (e.g., primer.qwav.tech)"
  - name: branch
    type: string
    required: false
    default: "master"
    description: "Git branch to deploy from (QWAV convention: master, not main)"
  - name: build_command
    type: string
    required: false
    description: "Build command (omit for static HTML sites — no build step needed)"
  - name: output_dir
    type: string
    required: false
    default: "."
    description: "Output directory for built site ('.' for root-deployed static sites)"
  - name: r2_bucket
    type: string
    required: false
    description: "R2 bucket name for storage operations"
  - name: file_pattern
    type: string
    required: false
    description: "Glob pattern for file uploads"
  - name: cf_account_id
    type: string
    required: false
    default: "edb167b78c9fb901ea5bca3ce58ccc4b"
    description: "Cloudflare Account ID (quniverse)"
  - name: cf_zone_id
    type: string
    required: false
    default: "331e4363fd05e8e4fc123ea7d2775411"
    description: "Cloudflare Zone ID for qwav.tech"
  - name: ga4_measurement_id
    type: string
    required: false
    description: "Google Analytics 4 Measurement ID (G-XXXXXXXXXX) for GA4/GTM injection"
  - name: analytics_provider
    type: string
    required: false
    default: "cloudflare"
    description: "Analytics provider: cloudflare (Web Analytics), ga4 (Google Analytics 4), both (dual tracking)"
  - name: site_type
    type: string
    required: false
    default: "pages"
    description: "Site hosting type: pages (Cloudflare Pages), google-site (Google Sites), worker (Cloudflare Worker), proxied (zone-level only)"
---

# CLOUDFLARE DEPLOYMENT — {{action}} for {{project_name}}

> **⚠️ PLATFORM AWARENESS:** Cloudflare-native deployment for QWAV public-facing assets.
> Cloudflare already hosts QWAV domains (qwav.tech, quni.cloud) via DNS.
> **⚠️ DUAL-PLATFORM MODEL:** GitHub = git + Issues. Cloudflare = hosting + storage + compute.
> **⚠️ COST GATE:** Check free tier thresholds before any operation (Pages: unlimited bandwidth, R2: 10GB, Workers: 100k/day).
> **⚠️ VERSION NOTICE:** Template v2.1 updated 2026-05-28. Key changes: v2.0 added domain management via API (wrangler 4.95.0 lacks `set-domain`), OAuth+YoBrowser auth path verified, branch default changed to `master` (QWAV convention), static sites omit build flags. v2.1 adds `enable-analytics` operation (Cloudflare Web Analytics + GA4/GTM injection), analytics parameters, and post-deployment analytics verification.

---

## 0. PREREQUISITES

### 0.1 Authentication

Three auth methods, ranked by reliability for agent execution:

| Method | Agent-Compatible | Persistence | Notes |
|:-------|:----------------:|:-----------|:------|
| **API Token (PERSISTENT FILE)** | Yes Fully | Yes Persisted to `C:\Users\LENOVO\.cloudflare\api-token` | **PRIMARY METHOD -- FULL account access.** Load at session start. zone:write, DNS:edit, redirects, Pages, Workers, R2. |
| **OAuth Token** (`wrangler login`) | Yes With YoBrowser | Yes Persisted to `%APPDATA%\xdg.config\.wrangler\config\default.toml` | **LIMITED SCOPES (zone:read only).** CANNOT do DNS writes or redirect management. Useful for wrangler CLI only. |
| **Global API Key** (`CLOUDFLARE_API_KEY`+`CLOUDFLARE_EMAIL`) | Yes Fully | No Per-session env vars | Use for headless/non-browser agents |

```bash
# METHOD 1: API Token from persistent file (PREFERRED -- FULL account access):
$env:CLOUDFLARE_API_TOKEN = (Get-Content "C:\Users\LENOVO\.cloudflare\api-token" -Raw).Trim()
# Token has zone:write, DNS:edit, redirect rules, Pages, Workers, R2, D1, Vectorize
# Use for ALL direct API calls (curl, Python) to Cloudflare REST API
# The wrangler OAuth token has zone:read ONLY -- never use for DNS/redirect operations

# METHOD 2: OAuth (PERSISTENT -- do this ONCE):
wrangler login
# -> Opens browser. Authenticate via Cloudflare Dashboard.
# -> Token stored permanently. Verify with "wrangler whoami".
# -> LIMITED TO zone:read -- DNS writes and redirects WILL FAIL.

# METHOD 3: Global API Key (per-session):
$env:CLOUDFLARE_API_KEY = "<global-api-key>"
$env:CLOUDFLARE_EMAIL = "<cloudflare-account-email>"
# NOTE: Both env vars required. API Key alone is insufficient.

# Verify auth:
wrangler --version          # Must be v3.0+ (PoC tested: v4.95.0)
wrangler whoami             # Must show authenticated account + scopes
wrangler pages project list # Active Pages projects
```

### 0.2 Install Wrangler (if not present)

```bash
npm install -g wrangler      # Global install (~35 packages)
wrangler --version           # Confirm
```

---

## 1. OPERATION: deploy-pages

Deploy a static site to Cloudflare Pages. **For static HTML sites (no framework, no build step), the deployment is a simple file upload.**

### 1.1 First-Time Setup

```bash
# Clone the repo (if not already local):
git clone https://github.com/{{repo}}.git C:\Temp\{{project_name}}-deploy

# Create Pages project:
wrangler pages project create {{project_name}} --production-branch {{branch}}
# → Available at https://{{project_name}}.pages.dev after first deploy
```

### 1.2 Deploy Static Files

```bash
# STATIC HTML (no build step — just upload):
wrangler pages deploy C:\Temp\{{project_name}}-deploy --project-name {{project_name}} --branch {{branch}}

# WITH BUILD STEP:
wrangler pages deploy --project-name {{project_name}} --branch {{branch}} \
  --build-command "{{build_command}}" --build-output-directory {{output_dir}}
```

### 1.3 Verify Deployment

```bash
wrangler pages deployment list --project-name {{project_name}}
curl.exe -sI https://{{project_name}}.pages.dev | Select-String "HTTP"
# MUST return: HTTP/1.1 200 OK
```

### 1.4 Custom Domain — See Section 7

**⚠️ WRANGLER 4.95.0 GAP:** `wrangler pages project set-domain` does NOT exist. Use the Cloudflare API directly (Section 7).

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

Migrate an existing GitHub Pages site to Cloudflare Pages with zero downtime. **The original GitHub Pages site is NOT touched — this is a parallel deployment.**

### 4.1 Audit & Deploy

```bash
# 1. Audit current GitHub Pages (optional — GitHub Pages stays live):
gh api /repos/{{repo}}/pages --jq '{status, cname, branch: .source.branch, path: .source.path}'

# 2. Clone and deploy:
git clone https://github.com/{{repo}}.git C:\Temp\{{project_name}}-deploy
wrangler pages project create {{project_name}} --production-branch {{branch}}
wrangler pages deploy C:\Temp\{{project_name}}-deploy --project-name {{project_name}} --branch {{branch}}

# 3. Test on pages.dev:
curl.exe -sI https://{{project_name}}.pages.dev
```

### 4.2 Add Custom Domain

See **Section 7** (domain management). For migration, add the SAME custom domain that GitHub Pages uses — this requires removing the domain from GitHub Pages first (not covered here; see Section 7.4 for the full migration sequence).

### 4.3 Verification Checklist (Before Disabling GitHub Pages)

| Check | Command | Expected |
|:------|:--------|:---------|
| Pages.dev URL | `curl -sI https://{{project_name}}.pages.dev` | HTTP 200 |
| Custom domain | `curl -sI https://{{domain}}` | HTTP 200 |
| GitHub Pages still live | `curl -sI https://{{repo_owner}}.github.io/{{project_name}}/` | HTTP 200 |
| Content match | Spot-check both URLs | Identical |
| HTTPS | Browser check | 🔒 Lock icon |

**Wait 24 hours** after Cloudflare deployment before disabling GitHub Pages. This allows DNS propagation, SSL provisioning, and cache warming.

```bash
# 6. Disable GitHub Pages only after 24h verification:
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
gh api /orgs/QNFO/settings/billing/usage --jq '.usageItems[] | select(.product=="actions")'
```

---

## 7. OPERATION: domain-add — Custom Domain Management

**⚠️ CRITICAL:** `wrangler pages project set-domain` does NOT exist in wrangler 4.95.0. Use the Cloudflare REST API for all domain operations. This section is the **verified procedure from the qlof-primer PoC (2026-05-27).**

### 7.1 API Constants

```
Cloudflare Account ID: {{cf_account_id}}          # edb167b78c9fb901ea5bca3ce58ccc4b
Zone ID (qwav.tech):  {{cf_zone_id}}              # 331e4363fd05e8e4fc123ea7d2775411
API Base:             https://api.cloudflare.com/client/v4
Auth Header (Global Key):  X-Auth-Email + X-Auth-Key
Auth Header (API Token):   Authorization: Bearer <token>
```

### 7.2 Add Custom Domain to Pages Project

```python
# Python script: add_domain.py
import urllib.request, json

ACCOUNT_ID = "{{cf_account_id}}"
PROJECT = "{{project_name}}"
API_KEY = "<global-api-key>"        # or use API Token
EMAIL = "<cloudflare-email>"        # required for Global Key

url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT}/domains"
data = json.dumps({"name": "{{domain}}"}).encode()

req = urllib.request.Request(url, data=data, method="POST")
req.add_header("X-Auth-Email", EMAIL)
req.add_header("X-Auth-Key", API_KEY)
req.add_header("Content-Type", "application/json")

resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read())
print(f"Status: {result['result']['status']}")  # → "initializing"
```

### 7.3 The CNAME-Record Dance (WHEN VERIFICATION FAILS)

**Problem:** Adding a domain BEFORE the CNAME DNS record exists causes verification failure ("CNAME record not set"). Cloudflare does NOT auto-create the CNAME even when the zone is in the same account.

**Solution:** Create the CNAME first, then add the domain.

```python
# Step 1: Create CNAME record in DNS
import urllib.request, json

ZONE_ID = "{{cf_zone_id}}"
data = json.dumps({
    "type": "CNAME",
    "name": "{{domain}}",                      # e.g., primer.qwav.tech
    "content": "{{project_name}}.pages.dev",    # e.g., qlof-primer.pages.dev
    "proxied": True,                            # Orange cloud — REQUIRED for SSL
    "ttl": 1                                    # Auto TTL
}).encode()

url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
req = urllib.request.Request(url, data=data, method="POST")
req.add_header("X-Auth-Email", EMAIL)
req.add_header("X-Auth-Key", API_KEY)
req.add_header("Content-Type", "application/json")

resp = urllib.request.urlopen(req, timeout=15)
print(json.loads(resp.read()))

# Step 2: NOW add the domain to Pages (verification will succeed)
# → Run the script from Section 7.2 AFTER the CNAME exists
```

### 7.4 Fix a Failed Verification (Delete + Re-Add)

If you added the domain BEFORE the CNAME existed and verification shows "CNAME record not set":

```python
# 1. Delete the domain
DOMAIN_NAME = "{{domain}}"
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT}/domains/{DOMAIN_NAME}"
req = urllib.request.Request(url, method="DELETE")
req.add_header("X-Auth-Email", EMAIL)
req.add_header("X-Auth-Key", API_KEY)
urllib.request.urlopen(req, timeout=15)

# 2. Re-add (verification will pass now that CNAME exists)
# → Run Section 7.2 script again
```

### 7.5 Verify Domain Status

```python
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT}/domains"
req = urllib.request.Request(url)
req.add_header("X-Auth-Email", EMAIL)
req.add_header("X-Auth-Key", API_KEY)
resp = urllib.request.urlopen(req, timeout=15)
result = json.loads(resp.read())

for d in result["result"]:
    print(f"Domain: {d['name']}")
    print(f"  Status: {d['status']}")                        # active = live
    print(f"  Validation: {d['validation_data']['status']}")  # active = SSL ready
    print(f"  Verification: {d['verification_data'].get('status', 'N/A')}")
```

### 7.6 Full Status Lifecycle

| Status | What It Means | Wait Time |
|:-------|:-------------|:----------|
| `initializing` | Domain just added, DNS/SSL provisioning starting | ~5 seconds |
| `pending` | Waiting for DNS verification / SSL provisioning | 10-60 seconds |
| `active` | ✅ Live — domain resolves with HTTPS | N/A |

### 7.7 Troubleshooting

| Symptom | Likely Cause | Fix |
|:--------|:------------|:----|
| HTTP 522 | Domain in Pages but CNAME missing or un-proxied | Verify CNAME exists and `proxied: true` |
| "CNAME record not set" | CNAME created after domain added | Delete + re-add domain (Section 7.4) |
| HTTP 530 | SSL not provisioned yet | Wait 60s, check validation_data.status |
| Domain not resolving | DNS propagation | `nslookup {{domain}} 1.1.1.1` |

---

## 8. OPERATION: configure

Configure Cloudflare Pages project settings via API.

```bash
# View project settings:
wrangler pages project list --json

# Set production branch:
# (Use API — no wrangler command for post-creation branch changes)
```

---

## 8.5 OPERATION: enable-analytics

Enable traffic analytics and user tracking on deployed sites. Supports Cloudflare Web Analytics (native, free, no code changes for Pages), Google Analytics 4 injection (via Cloudflare Zaraz or manual HTML), and dual tracking.

### 8.5.1 Choose Analytics Strategy

| Site Type | Cloudflare Web Analytics | GA4/GTM | Recommended | Method |
|:----------|:------------------------:|:-------:|:-----------|:-------|
| **Cloudflare Pages** (`*.pages.dev`, `*.qnfo.org`, `*.qwav.tech`) | ✅ Native, zero-code | ✅ Via Zaraz or manual `<script>` injection | **Both** — CF for real-time, GA4 for deeper user journeys | Enable CF Analytics in Dashboard; inject GA4 via Zaraz |
| **Google Sites** (`qnfo.org`, `qwav.tech`, `q08.org`) | ❌ Not proxied by CF | ✅ Built-in support | **GA4 only** | Insert → Analytics in Google Sites editor |
| **Proxied DNS-only** (domains routing through CF to external origins) | ✅ Zone-level analytics | ✅ Manual injection | **CF Analytics** (automatic) | Enable at zone level in Dashboard |
| **Cloudflare Workers** | ❌ No built-in pages analytics | ✅ Manual via `fetch` to GA4 endpoint | **GA4** (server-side) | Worker code adds GA4 Measurement Protocol calls |

### 8.5.2 Enable Cloudflare Web Analytics (Pages Sites)

For each Cloudflare Pages project, enable Web Analytics:

```bash
# METHOD 1: Via Cloudflare Dashboard (recommended for initial setup)
# Navigate: dash.cloudflare.com → Analytics & Logs → Web Analytics → Add a site
# Select: Pages project → {{project_name}}
# Note: Analytics data begins flowing within 60 seconds.

# METHOD 2: Via API (for programmatic enablement)
# Get Pages project deployment info:
curl -X GET "https://api.cloudflare.com/client/v4/accounts/{{cf_account_id}}/pages/projects/{{project_name}}" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json"

# Enable Web Analytics on existing Pages project:
# NOTE: Web Analytics must be enabled via Dashboard for the initial site tag.
# After site tag is created, use the RUM site tag for SPA/manual injection.
```

**Automatic analytics for proxied zones:** If the domain (e.g., `laws.qnfo.org`) is proxied through Cloudflare (orange cloud), zone-level analytics are automatically collected. No action needed. Verify:

```bash
# Check if domain is proxied:
curl -sI "https://{{domain}}" | findstr "cf-ray"
# → If cf-ray header present, traffic is proxied and analytics are collecting.

# View zone analytics data:
curl "https://api.cloudflare.com/client/v4/zones/{{cf_zone_id}}/analytics/dashboard?since=-1440" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json"
```

### 8.5.3 Inject Google Analytics 4 (GA4/GTM)

Two injection methods, ranked by simplicity:

#### Method A: Cloudflare Zaraz (Recommended — No Code Changes)

Zaraz is Cloudflare's built-in third-party tool loader. It injects GA4/GTM at the edge without modifying site HTML.

```bash
# 1. Enable Zaraz on the zone via Dashboard:
#    dash.cloudflare.com → {{cf_zone_id}} → Zaraz → Enable

# 2. Add Google Analytics 4 tool via Zaraz API:
curl -X POST "https://api.cloudflare.com/client/v4/zones/{{cf_zone_id}}/zaraz/tools" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "google-analytics-4",
    "enabled": true,
    "settings": {
      "measurement_id": "{{ga4_measurement_id}}"
    }
  }'

# 3. Verify Zaraz is injecting:
curl -s "https://{{domain}}" | findstr "zaraz"
# → Should show zaraz script reference in <head>
```

**⚠️ Zaraz Prerequisites:** The domain must be proxied through Cloudflare (orange cloud). Google Sites (`qnfo.org`, `qwav.tech`) are NOT proxied by Cloudflare — use Method B for those.

#### Method B: Manual HTML Injection (Pages Sites)

For Cloudflare Pages sites, add the GA4/GTM snippet directly to the HTML template:

```html
<!-- Google tag (gtag.js) — GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ga4_measurement_id}}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ga4_measurement_id}}');
</script>
```

Add this to every page's `<head>` in the Pages project, then redeploy:

```bash
# After adding GA4 snippet to HTML files:
wrangler pages deploy C:\Temp\{{project_name}}-deploy --project-name {{project_name}} --branch {{branch}}
```

#### Method C: Google Sites GA4 (for qnfo.org, qwav.tech, q08.org)

For Google Sites, GA4 is built-in:
1. Open the Google Site in edit mode
2. Click **Insert** → **Analytics** (or Settings gear → Analytics)
3. Enter the GA4 Measurement ID: `{{ga4_measurement_id}}`
4. Publish the site
5. Verify: Visit the site, then check GA4 Real-Time report for active users

### 8.5.4 Verification Checklist

After enabling analytics, verify ALL of the following:

```bash
# VERIFY CLOUDFLARE WEB ANALYTICS:
# 1. Check Pages project analytics status:
curl "https://api.cloudflare.com/client/v4/accounts/{{cf_account_id}}/pages/projects/{{project_name}}" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "import sys,json; d=json.load(sys.stdin); print('Analytics:', d.get('result',{}).get('analytics', 'NOT FOUND'))"

# 2. Visit the site to generate test traffic:
curl -sI "https://{{domain}}"

# 3. Wait 60 seconds, then check zone analytics:
curl "https://api.cloudflare.com/client/v4/zones/{{cf_zone_id}}/analytics/dashboard?since=-5" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "import sys,json; d=json.load(sys.stdin); print('Requests:', d.get('result',{}).get('totals',{}).get('requests',{}).get('all', 'NO DATA'))"

# VERIFY GOOGLE ANALYTICS 4:
# 4. Check GA4 snippet present in site HTML:
curl -s "https://{{domain}}" | findstr "googletagmanager\|gtag\|{{ga4_measurement_id}}"
# → Must show GA4 script or Zaraz reference

# 5. Check GA4 Real-Time report:
#    analytics.google.com → {{ga4_measurement_id}} → Reports → Real-Time
#    → Should show active users within 30 seconds of test visit
```

### 8.5.5 Analytics Endpoint Reference

Record these endpoints in audit trail for dashboard building:

| Endpoint | Purpose | Access |
|:---------|:--------|:-------|
| `https://api.cloudflare.com/client/v4/zones/{zone}/analytics/dashboard` | Zone-level analytics (requests, bandwidth, threats, unique visitors) | API Token with `Analytics:read` |
| `https://api.cloudflare.com/client/v4/accounts/{account}/rum/site_info` | Web Analytics RUM sites | API Token with `Account:read` |
| `https://api.cloudflare.com/client/v4/accounts/{account}/rum/analytics` | Web Analytics RUM data | API Token with `Account:read` |
| `https://analyticsdata.googleapis.com/v1beta/properties/{property}:runReport` | GA4 Data API | OAuth2 with `https://www.googleapis.com/auth/analytics.readonly` |
| `https://www.googleapis.com/analytics/v3/data/ga` | Universal Analytics API (legacy, if any UA properties exist) | OAuth2 |

### 8.5.6 Unified Dashboard Architecture (Future)

For combining Cloudflare + GA4 data into a single dashboard:

```
                    ┌──────────────────────────────┐
                    │   Cloudflare Worker Dashboard │
                    │   (analytics.qnfo.org)         │
                    └──────────┬───────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
    ┌─────────────────┐ ┌───────────┐ ┌─────────────────┐
    │ CF GraphQL API   │ │ GA4 Data  │ │ CF Zone         │
    │ (RUM analytics)  │ │ API       │ │ Dashboard API   │
    └─────────────────┘ └───────────┘ └─────────────────┘

Worker aggregates:
- Traffic by source (referrer, country, device)
- Top pages accessed
- Real-time active users (from GA4)
- Bot vs. human traffic (from CF)
- Page load performance (Web Vitals from CF RUM)
```

**Implementation (P2 — after analytics data is flowing):**
1. Create Worker: `analytics-dashboard` @ analytics.qnfo.org
2. Worker fetches from CF Analytics API + GA4 Data API
3. Renders HTML dashboard with Chart.js visualizations
4. Requires: CF API Token (`Analytics:read`), GA4 OAuth2 credentials stored in KV

---

## 9. FREE TIER THRESHOLDS

| Resource | Limit | Static HTML Impact |
|:---------|:------|:-------------------|
| Pages bandwidth | Unlimited | ✅ No concern |
| Pages builds | 500/month | ✅ Static deploys = uploads, not builds (0 build count) |
| Workers | 100k requests/day | N/A for static sites |
| R2 storage | 10 GB | ✅ ~84 KB per site × 9 sites = negligible |

---

## 10. POINTS OF FAILURE (PoC-Verified)

| # | Failure | Root Cause | Resolution |
|:--|:--------|:----------|:-----------|
| 1 | `wrangler pages project set-domain` not found | Removed in wrangler 4.95.0 | Use Cloudflare API (Section 7) |
| 2 | Domain verification fails: "CNAME record not set" | Cloudflare doesn't auto-create DNS CNAME | Create CNAME BEFORE adding domain (Section 7.3) |
| 3 | HTTP 522 after adding domain | CNAME missing but domain in Pages | Delete + re-add domain after CNAME exists (Section 7.4) |
| 4 | `wrangler login` with YoBrowser | Login page requires Cloudflare credentials | User must enter credentials in YoBrowser; OAuth persists afterwards |
| 5 | Inline Python corrupted by PowerShell | PowerShell intercepts quotes/special chars | Write Python to temp file first, then execute (Rule 13) |
| 6 | Wrangler requires both `CLOUDFLARE_API_KEY` + `CLOUDFLARE_EMAIL` | Global API Key auth needs email | Always set both env vars together |

---

## 11. PHASE 2 BATCH MIGRATION (9 Sites)

For migrating all QWAV research sites from GitHub Pages to Cloudflare Pages:

```bash
# Pseudocode for batch migration:
# For each repo in (qlof-primer, quantum-laws-of-form, ultrametric-paradigm, ...):
#   1. git clone → temp dir
#   2. wrangler pages project create $repo --production-branch master
#   3. wrangler pages deploy $temp_dir --project-name $repo --branch master
#   4. Add custom domain via API (Section 7)
#   5. Verify: curl pages.dev + custom domain → HTTP 200
#   6. Log results to QNFO/QWAV#63

# Estimated time per site: ~10 minutes (static HTML, no build)
# Total for 9 sites: ~90 minutes
# Free tier: No cost (unlimited bandwidth, 0 builds)
```

---

*Template v2.1 — Updated 2026-05-28 after analytics integration. v2.0: qlof-primer PoC deployment.*
*Reference: QNFO/QWAV#63 (migration investigation), QNFO/QWAV#62 (QNFO flagging incident)*
