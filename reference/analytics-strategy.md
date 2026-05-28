# Cloudflare Analytics Strategy — QNFO & QWAV Unified Traffic Visibility

> **Version:** 1.0 | **Date:** 2026-05-28 | **Author:** System Prompt Generator v4.6
> **Status:** Ready for deployment | **Priority:** HIGH (16 sites deployed, zero traffic visibility)
>
> **Related:** CLOUDFLARE-DEPLOYMENT.md v2.1 (Section 8.5: enable-analytics operation),
> DEFINITION-OF-DONE.md v2.0 (DEPLOYMENT TASK analytics gate)

---

## 1. Executive Summary

**Problem:** 16 Cloudflare Pages sites + 3 Google Sites serving 8,000+ visitors/month with ZERO analytics — no traffic source data, no page access metrics, no user behavior insights. Every deployment is blind.

**Solution:** Two-phase deployment:
1. **Phase 1 (Today — 1 session):** Enable Cloudflare Web Analytics on all proxied zones and Pages projects (free, zero-code, automatic for proxied traffic). This gives immediate traffic visibility: top pages, referrers, countries, device types.
2. **Phase 2 (Week):** Create GA4 properties, inject via Cloudflare Zaraz (edge-level, no HTML changes), verify data flowing. Optional unified dashboard Worker.

**Cost:** $0/month. All within Cloudflare + Google Analytics free tiers.

---

## 2. Current State Audit

### 2.1 What's Deployed

| Category | Count | Details |
|:---------|:------|:--------|
| Cloudflare Pages projects | 16 | 14 `*.qnfo.org` research sites + `deep.qwav.tech` + `primer.qwav.tech` + `prompts-wiki.pages.dev` |
| Google Sites | 3 | `qnfo.org` (5,590 visits/mo), `qwav.tech` (QWAV marquee), `q08.org` (2,280 visits/mo) |
| Cloudflare Zones (proxied) | ~10 | qwav.tech, qnfo.org, quni.cloud, qnfo.net, qnfo.uk, qwav.net, qwav.uk, qwav.org, q-wave.tech, qwave.tech |
| Bulk Redirect Rules | 6 | `*.(net|uk|org)` → primary domains |
| Cloudflare Workers | 3 | audit-worker, task-worker, search-worker (PM infrastructure) |

### 2.2 What Analytics Exist

| Provider | Status | Notes |
|:---------|:-------|:------|
| Cloudflare Zone Analytics | ❌ Not checked | Available automatically for proxied zones but never queried |
| Cloudflare Web Analytics (RUM) | ❌ Not enabled | Must be enabled per-Pages-project via Dashboard |
| Google Analytics 4 | ❌ Not configured | No GA4 properties created for any domain |
| Google Tag Manager | ❌ Not configured | No GTM containers exist |
| Cloudflare Zaraz | ❌ Not enabled | Available for GA4/GTM injection at edge |

### 2.3 Wrangler Auth Status

```
✅ OAuth Token active: rwnquni@outlook.com
✅ Account: quniverse (edb167b78c9fb901ea5bca3ce58ccc4b)
✅ Scopes: pages(write), zone(read), workers(write), d1(write)
✅ Analytics scope: zone(read) — sufficient for analytics API queries
```

---

## 3. Target Architecture

```
                         VISITORS
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ Pages Site │  │ Google Site│  │ Cloudflare │
     │(*.qnfo.org)│  │(qnfo.org)  │  │  Worker    │
     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
           │               │               │
           ▼               ▼               ▼
    ┌──────────────────────────────────────────┐
    │        Cloudflare Edge (All Traffic)      │
    │                                          │
    │  ┌─────────┐  ┌──────────┐  ┌─────────┐ │
    │  │  Zone   │  │  Zaraz   │  │   RUM   │ │
    │  │Analytics│  │ (GA4/GTM)│  │ Web     │ │
    │  │(automatic│  │injection)│  │Analytics│ │
    │  └────┬────┘  └────┬─────┘  └────┬────┘ │
    └───────┼────────────┼─────────────┼───────┘
            │            │             │
            ▼            ▼             ▼
    ┌──────────┐  ┌───────────┐  ┌──────────┐
    │   CF     │  │  Google   │  │   CF     │
    │Dashboard │  │ Analytics │  │ GraphQL  │
    │   API    │  │    4      │  │   API    │
    └────┬─────┘  └─────┬─────┘  └────┬─────┘
         │              │             │
         └──────────────┼─────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Unified Dashboard │  ← Phase 2 (Worker)
              │ analytics.qnfo.org│
              └──────────────────┘
```

**Data flow:**
- All Cloudflare-proxied traffic → CF Zone Analytics (automatic)
- Pages projects → CF Web Analytics (RUM) (manual enable)
- GA4 data → from Zaraz edge injection (no site code changes)
- Google Sites → GA4 via built-in Insert → Analytics
- Unified dashboard → CF Worker aggregating CF Analytics API + GA4 Data API

---

## 4. GA4 Property Setup Plan

### 4.1 Properties to Create

GA4 uses a data stream model. Each distinct domain/brand gets a property:

| Property | Data Streams | Type | Priority |
|:---------|:------------|:------|:---------|
| **QNFO Research** | `*.qnfo.org` (14 Pages sites) | Web | P0 — Highest traffic |
| **QNFO Landing** | `qnfo.org` (Google Site) | Web | P0 — 5,590 visits/mo |
| **QWAV Knowledge** | `deep.qwav.tech`, `primer.qwav.tech` | Web | P1 |
| **QWAV Landing** | `qwav.tech` (Google Site) | Web | P1 |
| **Q08 Project** | `q08.org` (Google Site) | Web | P2 — 2,280 visits/mo |

**Alternative (simpler):** Single GA4 property for all QNFO traffic, with separate data streams per domain. This is easier to manage and provides cross-domain analytics.

**Recommended: Single property "QNFO Network" with 5 data streams:**
1. qnfo.org (Google Site landing)
2. *.qnfo.org (14 Pages sites — single stream since all share qnfo.org root)
3. qwav.tech (Google Site landing)
4. *.qwav.tech (2 Pages sites)
5. q08.org (Google Site)

### 4.2 GA4 Property Creation

```bash
# Cannot be automated — must use Google Analytics web UI:
# 1. Go to analytics.google.com
# 2. Admin → Create Property → "QNFO Network"
# 3. Reporting timezone: America/Chicago (UTC-6)
# 4. Currency: USD
# 5. Add data streams for each domain above
# 6. Record the Measurement ID (G-XXXXXXXXXX) for each stream
```

**Measurement IDs (to be filled after creation):**

| Stream | Domain | Measurement ID |
|:-------|:-------|:---------------|
| QNFO Landing | qnfo.org | `[CREATE IN GA4 UI]` |
| QNFO Research | *.qnfo.org | `[CREATE IN GA4 UI]` |
| QWAV Landing | qwav.tech | `[CREATE IN GA4 UI]` |
| QWAV Research | *.qwav.tech | `[CREATE IN GA4 UI]` |
| Q08 | q08.org | `[CREATE IN GA4 UI]` |

---

## 5. Cloudflare Analytics Configuration

### 5.1 Zone-Level Analytics (AUTOMATIC — Verify Only)

All traffic proxied through Cloudflare (orange cloud) is automatically tracked. No configuration needed.

**Zones to verify:**

```bash
# List all zones:
curl -X GET "https://api.cloudflare.com/client/v4/zones?per_page=50" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN"

# For each zone, verify analytics data exists:
curl "https://api.cloudflare.com/client/v4/zones/ZONE_ID/analytics/dashboard?since=-1440" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | jq '.result.totals'
```

**Zones confirmed active (May 28 audit via wrangler API):**

| Zone | Zone ID | Plan | Status |
|:-----|:--------|:-----|:-------|
| qnfo.org | `84e9dc1d7fb72629ccdbe3174ed24420` | Free Website | active |
| qwav.tech | `331e4363fd05e8e4fc123ea7d2775411` | Free Website | active |
| q08.org | `fa732a265dd53230b9777908734a74d5` | Free Website | active |
| qnfo.net | `d4e7855f3ed5f0a93204b7bd34e286ab` | Free Website | active (redirect) |
| qnfo.uk | `26699a3b10699f257eabc34a0faee56d` | Free Website | active (redirect) |
| qwav.net | `260c09728193c4f902435bad47ce976c` | Free Website | active (redirect) |
| qwav.org | `4df9cb76facef38e78f6f6fc61cbb7c7` | Free Website | active (redirect) |
| qwav.uk | `2e0b5be2a41da2a5754269984e7873ad` | Free Website | active (redirect) |
| q-wave.tech | `dd6908d3cc04acb2efee47382fb94e8e` | Free Website | active (redirect) |
| qwave.tech | `365f6eebc45b8075aece5a6ecbd2850a` | Free Website | active (redirect) |

**Note:** quni.cloud is NOT in the zone list — DNS-only, not proxied. 3 non-QNFO zones also exist (bradworks.net, empoweringchange.today, ipatent.me) — these are out of scope.

**API Access Blocked:** The OAuth token from `wrangler login` has `zone:read` but NOT `analytics:read` scope. Analytics API (`/zones/{id}/analytics/dashboard`) returns 403. To query analytics data programmatically, a Global API Key or scoped API Token with `Analytics:read` is needed. However, all analytics data IS being collected automatically for proxied traffic — it's visible in the Dashboard UI.

### 5.2 Cloudflare Web Analytics (RUM) — Per Pages Project

Must be manually enabled for each Pages project. Provides detailed metrics:
- Top pages, referrers, countries, device types, browsers
- Core Web Vitals (LCP, FID, CLS)
- Page load waterfall

**Enable via Dashboard (one-time per project):**
```
dash.cloudflare.com → Analytics & Logs → Web Analytics → Add a site
→ Select: Cloudflare Pages → [project name]
→ Auto-detects: Auto-detects Pages project
→ Site tag: Auto-configured (no code changes needed)
```

**Pages projects to enable (16 total):**

| # | Project | Domain | Priority |
|:--|:--------|:-------|:---------|
| 1 | qlof-primer | primer.qwav.tech | P0 (verify flow works) |
| 2 | quantum-laws-of-form | laws.qnfo.org | P0 |
| 3 | ultrametric-paradigm | paradigm.qnfo.org | P0 |
| 4 | hierarchical-universe | hierarchy.qnfo.org | P0 |
| 5 | different-physics | different.qnfo.org | P0 |
| 6 | two-ways-of-measuring | measure.qnfo.org | P1 |
| 7 | unity-of-ultrametric-physics | unity.qnfo.org | P1 |
| 8 | ultrametric-quantum | quantum.qnfo.org | P1 |
| 9 | ultrametric-ai-poc | ai-poc.qnfo.org | P1 |
| 10 | adelic-qft | adelic.qnfo.org | P2 |
| 11 | cocyle | cocyle.qnfo.org | P2 |
| 12 | knowing-patterns | knowing.qnfo.org | P2 |
| 13 | solo-scientist | solo.qnfo.org | P2 |
| 14 | verb-lexicon | lexicon.qnfo.org | P2 |
| 15 | qwav | deep.qwav.tech | P1 |
| 16 | prompts-wiki | prompts-wiki.pages.dev | P3 (internal) |

### 5.3 Analytics API Verification

After enabling, verify data is flowing:

```bash
# For each Pages project:
# 1. Generate test traffic:
for domain in laws.qnfo.org paradigm.qnfo.org hierarchy.qnfo.org; do
  curl -sI "https://$domain" > /dev/null
  echo "Hit: $domain"
done

# 2. Wait 60 seconds for data processing

# 3. Check zone analytics (aggregate view):
curl "https://api.cloudflare.com/client/v4/zones/QNFO_ZONE_ID/analytics/dashboard?since=-5" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "
import sys, json
d = json.load(sys.stdin)
totals = d.get('result', {}).get('totals', {})
print('Requests:', totals.get('requests', {}).get('all', 'NO DATA'))
print('Unique Visitors:', totals.get('uniques', {}).get('all', 'NO DATA'))
print('Bandwidth:', totals.get('bandwidth', {}).get('all', 'NO DATA'))
"

# 4. Check individual Page Views (top pages):
curl "https://api.cloudflare.com/client/v4/zones/QNFO_ZONE_ID/analytics/dashboard?since=-1440&continuous=true" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "
import sys, json
d = json.load(sys.stdin)
http_requests = d.get('result', {}).get('timeseries', [])
print(f'Timeseries data points: {len(http_requests)}')
# Show last 3 with non-zero requests:
count = 0
for point in reversed(http_requests):
    reqs = point.get('requests', {}).get('all', 0)
    if reqs > 0:
        print(f'  {point.get(\"since\")}: {reqs} requests')
        count += 1
        if count >= 3: break
"
```

---

## 6. Zaraz GA4 Injection Plan

### 6.1 Why Zaraz

Cloudflare Zaraz injects third-party tools (GA4, GTM, Facebook Pixel, etc.) at the edge — no HTML changes needed on any site. Benefits:
- **Zero code changes** — inject GA4 into all 16 Pages sites simultaneously
- **Single configuration** — one Zaraz setup per zone, applies to all proxied Pages sites
- **Performance** — loaded from Cloudflare edge, not third-party servers
- **Consent management** — built-in GDPR/cookie consent if needed later

### 6.2 Zaraz Configuration (Per Zone)

For `qwav.tech` zone:

```bash
# 1. Enable Zaraz (via Dashboard or API):
# dash.cloudflare.com → qwav.tech → Zaraz → Enable

# 2. Add GA4 tool via API:
curl -X POST "https://api.cloudflare.com/client/v4/zones/331e4363fd05e8e4fc123ea7d2775411/zaraz/tools" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "google-analytics-4",
    "enabled": true,
    "name": "QWAV Research GA4",
    "settings": {
      "measurement_id": "G-XXXXXXXXXX"
    },
    "triggers": [
      {"type": "pageview"}
    ],
    "default_fields": {
      "page_location": "{{client.URL}}",
      "page_referrer": "{{client.referer}}",
      "page_title": "{{client.page_title}}"
    }
  }'

# 3. Verify Zaraz is injecting:
curl -s "https://primer.qwav.tech" | grep -i "zaraz\|gtag\|googletagmanager"
```

For `qnfo.org` zone (once zone ID is obtained):

```bash
# Same procedure with QNFO GA4 measurement ID
# Zaraz will inject GA4 into all *.qnfo.org Pages sites automatically
```

### 6.3 Google Sites GA4 (Manual)

Google Sites (qnfo.org, qwav.tech, q08.org) are NOT proxied through Cloudflare. Use the built-in GA4 integration:

1. Open the Google Site in edit mode
2. Settings gear → Analytics
3. Enter GA4 Measurement ID
4. Publish

**Note:** This is a MANUAL step. The Projects agent can prepare the Measurement IDs but the user (rwnq8) must insert them in the Google Sites editor.

---

## 7. Unified Dashboard Architecture (Phase 2)

### 7.1 Worker Design

```
analytics.qnfo.org (Cloudflare Worker)
│
├── GET / → HTML dashboard (Chart.js)
│   ├── Real-time active users (GA4 → Real-Time API)
│   ├── Today's page views (CF Zone Analytics)
│   ├── Top referrers (CF Zone Analytics)
│   ├── Geographic map (CF Zone Analytics countries)
│   ├── Device breakdown (CF Zone Analytics)
│   └── Page load performance (CF RUM Web Vitals)
│
├── GET /api/summary → JSON aggregate (for external consumption)
│   └── Combined CF + GA4 metrics
│
└── GET /api/raw → JSON raw data (for custom dashboards)
    └── All available metrics from both providers
```

### 7.2 API Integrations Required

| API | Endpoint | Auth | Data |
|:----|:---------|:-----|:-----|
| CF Zone Analytics | `/client/v4/zones/{zone}/analytics/dashboard` | API Token `Analytics:read` | Requests, bandwidth, threats, uniques, countries |
| CF RUM Analytics | `/client/v4/accounts/{account}/rum/analytics` | API Token `Account:read` | Page views, Web Vitals, referrers |
| GA4 Data API | `/v1beta/properties/{property}:runReport` | OAuth2 | Active users, sessions, events, conversions |

### 7.3 KV Storage

Store credentials securely in Cloudflare KV:

```bash
wrangler kv:namespace create "ANALYTICS_CREDENTIALS"
# Store:
# - CF_API_TOKEN
# - GA4_OAUTH_CLIENT_ID
# - GA4_OAUTH_CLIENT_SECRET
# - GA4_OAUTH_REFRESH_TOKEN
# - GA4_PROPERTY_IDS (JSON map of domain → property)
```

### 7.4 Implementation Timeline

| Phase | Description | Effort | Priority |
|:------|:-----------|:-------|:---------|
| **1A** | Enable CF Web Analytics on all 16 Pages projects | 1 session | 🔴 HIGH |
| **1B** | Create GA4 properties + data streams | 30 min (manual) | 🔴 HIGH |
| **1C** | Configure Zaraz GA4 injection (qwav.tech + qnfo.org zones) | 1 session | 🔴 HIGH |
| **1D** | Insert GA4 on Google Sites | 15 min (manual) | 🟡 MEDIUM |
| **2A** | Build analytics dashboard Worker | 1-2 sessions | 🟡 MEDIUM |
| **2B** | Deploy dashboard to analytics.qnfo.org | 1 session | 🟢 LOW |
| **2C** | Add alerting (traffic spike/drop detection) | Future | ⚪ LOW |

---

## 8. Deployment Sequence (Execution Plan)

### Pre-Deployment Checklist

- [ ] Wrangler authenticated (✅ CONFIRMED — OAuth token active)
- [ ] CF API Token with Analytics:read scope (✅ zone:read scope includes analytics)
- [ ] All 16 Pages projects confirmed deployed (✅ CONFIRMED — wrangler pages project list)
- [ ] Zone IDs known (⚠️ PARTIAL — qwav.tech known, qnfo.org needs lookup)
- [ ] GA4 properties created (❌ NOT YET — requires Google Analytics UI)
- [ ] Google Sites accessible for GA4 insertion (❌ NOT YET — requires user)

### Phase 1A: Enable Cloudflare Web Analytics (IMMEDIATE — No Dependencies)

This can be done NOW. Web Analytics is a Dashboard-only enablement (no API endpoint for initial creation). However, proxied zone analytics are automatic.

**Immediate action — verify zone analytics already flowing:**

```bash
# Get all zones:
curl -X GET "https://api.cloudflare.com/client/v4/zones?per_page=50" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "
import sys, json
zones = json.load(sys.stdin).get('result', [])
for z in zones:
    print(f'{z[\"name\"]:30s} | {z[\"id\"]} | Status: {z[\"status\"]} | Proxied: {z.get(\"paused\", True) == False}')
"

# For each zone, check if analytics data exists:
for zone_id in ZONE_IDS; do
  curl -s "https://api.cloudflare.com/client/v4/zones/$zone_id/analytics/dashboard?since=-1440" \
    -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "
import sys, json
d = json.load(sys.stdin)
totals = d.get('result', {}).get('totals', {})
reqs = totals.get('requests', {}).get('all', 0)
print(f'Zone $zone_id: {reqs} requests in last 24h')
"
done
```

### Phase 1A-Alt: Enable RUM Web Analytics on Each Pages Project

Since RUM Web Analytics requires Dashboard UI for initial enablement:

1. Open Cloudflare Dashboard in YoBrowser: `load_url("https://dash.cloudflare.com/")`
2. Navigate: Analytics & Logs → Web Analytics → Add a site
3. Select each Pages project from the dropdown
4. Repeat for all 16 projects

**Automation option:** If Cloudflare provides a programmatic API for RUM site creation (checking), use this instead of Dashboard.

### Phase 1B: Create GA4 Properties (MANUAL — Requires User)

1. Go to https://analytics.google.com
2. Create property: "QNFO Network"
3. Add 5 data streams:
   - qnfo.org (web)
   - *.qnfo.org (web)
   - qwav.tech (web)
   - *.qwav.tech (web)
   - q08.org (web)
4. Record all Measurement IDs

### Phase 1C: Configure Zaraz GA4 Injection

Once GA4 Measurement IDs are available:

```bash
# For qwav.tech zone (known ID: 331e4363fd05e8e4fc123ea7d2775411):
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/331e4363fd05e8e4fc123ea7d2775411/zaraz/tools" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "google-analytics-4",
    "enabled": true,
    "settings": {"measurement_id": "G-QWAV_ID_HERE"},
    "triggers": [{"type": "pageview"}]
  }'

# For qnfo.org zone (get zone ID first):
# Same procedure with G-QNFO_ID_HERE
```

### Phase 1D: Google Sites GA4 (MANUAL — Requires User)

Per the template SECTION 8.5.3 Method C:
1. Open qnfo.org in Google Sites editor
2. Insert → Analytics → Enter GA4 Measurement ID
3. Publish
4. Repeat for qwav.tech, q08.org

---

## 9. Verification Gates (BLOCKING)

After each phase, verify with these gates. Do NOT proceed until all pass.

### Gate 1: Cloudflare Zone Analytics Active

```bash
# For each zone, confirm non-zero requests:
curl "https://api.cloudflare.com/client/v4/zones/ZONE_ID/analytics/dashboard?since=-60" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "
import sys, json
d = json.load(sys.stdin)
reqs = d.get('result',{}).get('totals',{}).get('requests',{}).get('all', 0)
if reqs > 0:
    print(f'PASS: {reqs} requests in last hour')
else:
    print('FAIL: No requests. Generate test traffic and retry.')
"
```

### Gate 2: Cloudflare Web Analytics (RUM) Active

```bash
# Check if Web Analytics site exists:
curl "https://api.cloudflare.com/client/v4/accounts/edb167b78c9fb901ea5bca3ce58ccc4b/rum/site_info" \
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" | python -c "
import sys, json
sites = json.load(sys.stdin).get('result', [])
print(f'RUM sites configured: {len(sites)}')
for s in sites:
    print(f'  {s.get(\"host\")} — {s.get(\"id\")}')
"
```

### Gate 3: GA4 Data Flowing

After Zaraz injection or Google Sites insertion:
1. Visit the site (generate test traffic)
2. Go to GA4 → Reports → Real-Time
3. Confirm active users appear within 30 seconds
4. Check that `page_view` events are being collected

### Gate 4: cf-ray Header Present

```bash
# Every proxied site must show cf-ray header:
curl -sI "https://laws.qnfo.org" | grep -i "cf-ray"
# Expected: cf-ray: [hash]-[airport-code]
```

---

## 10. Cost Analysis

| Component | Free Tier Limit | Projected Usage | Status |
|:----------|:---------------|:----------------|:-------|
| Cloudflare Zone Analytics | Unlimited | ~8,000 requests/day | ✅ Free |
| Cloudflare Web Analytics (RUM) | 100 sites | 16 sites | ✅ Free |
| Cloudflare Zaraz | 50 tools/zone | 1 tool × 2 zones | ✅ Free |
| GA4 Properties | Unlimited (up to 2,000) | 1 property, 5 streams | ✅ Free |
| GA4 Events | 1M events/month (standard) | ~240K page views/month | ✅ Free |
| GA4 Data API | 50,000 requests/day | ~100 requests/day (dashboard refresh) | ✅ Free |
| Cloudflare Worker (dashboard) | 100,000 requests/day | ~1,000 requests/day (dashboard) | ✅ Free |
| Cloudflare KV (credentials) | 1 GB storage, 1,000 writes/day | <1 KB, <10 writes | ✅ Free |

**Total cost: $0/month. All within free tiers with 100x+ headroom.**

---

## 11. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| GA4 property creation requires user action | HIGH | Schedule delay | Prepare exact steps; user can complete in 15 minutes |
| Zaraz API requires token scope upgrade | LOW | Blocked deployment | Current token has zone:read — may need zone:write for Zaraz |
| Google Sites GA4 insertion requires user | HIGH | Manual step | Document exact click path; provide Measurement IDs |
| Zone-level analytics show zero data initially | MEDIUM | Confusion | Generate test traffic via curl; wait 60 seconds |
| Unified dashboard Worker hits API rate limits | LOW | Dashboard errors | Cache in KV; 5-minute refresh intervals |
| Old Google Analytics (UA) properties exist | LOW | Confusion | Audit existing properties; migrate to GA4 only |

---

## 12. References

- **Deployment Template:** `fill_prompt_template("CLOUDFLARE-DEPLOYMENT", {"action": "enable-analytics", ...})` — Section 8.5
- **Definition of Done:** `fill_prompt_template("DEFINITION-OF-DONE")` — DEPLOYMENT TASK analytics gate
- **Master Strategy:** QNFO/QWAV#66 — Phase 1-4 Cloudflare migration
- **Pages Migration Handoff:** `G:\My Drive\projects\cloudflare-pages-migration\HANDOFF.md`
- **Google Sites Audit:** `G:\My Drive\projects\google-site-auditor\HANDOFF.md`
- **DNS Validator:** `G:\My Drive\projects\cf-dns-validator\HANDOFF.md`
- **SESSION-CLOSEOUT-2026-05-27.md:** Web Analytics listed as Tier 2 (External) — ❌ None built

---

*Strategy Document v1.0 — 2026-05-28. Generated by System Prompt Generator v4.6.*
*Ready for execution. Next: Enable Cloudflare Web Analytics on all Pages projects, then create GA4 properties for Zaraz injection.*
