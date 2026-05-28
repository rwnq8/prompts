# Handoff: Cloudflare Analytics Enablement → Projects Agent

**Type:** Session→Session (System Prompt Generator → Projects Agent)
**GitHub Issue:** [rwnq8/prompts#37](https://github.com/rwnq8/prompts/issues/37)
**Date:** 2026-05-28
**Issuing Authority:** System Prompt Generator v4.6
**Accepting Authority:** Projects Agent (DEFAULT / QWAV)

## ⚠️ SEPARATION OF CONCERNS

The System Prompt Generator designed the analytics strategy, updated deployment templates, and verified infrastructure. The Projects Agent builds the actual analytics deployment from these specs. Self-certification without independent verification produces untested output.

## Scope

### Included
- Enable Cloudflare Web Analytics on all 16 Pages projects
- Configure Cloudflare Zaraz for GA4 injection across qwav.tech and qnfo.org zones
- Insert GA4 Measurement IDs in 3 Google Sites (user-assisted)
- Build analytics dashboard Worker at analytics.qnfo.org (Phase 2)
- Generate test traffic from 2+ geographic locations for verification

### Excluded
- Creating GA4 properties in Google Analytics UI (user must do this)
- Modifying site HTML (Zaraz handles GA4 injection at edge)
- DNS changes (all zones already configured)
- Pages projects creation (all 16 already deployed)

## Success Criteria

| # | Criterion | How Measured |
|:--|:----------|:-------------|
| 1 | All 16 Pages projects have CF Web Analytics enabled | Dashboard shows non-zero traffic per project |
| 2 | Zone analytics API returns non-zero requests | GraphQL query across all 10 zones |
| 3 | Zaraz GA4 injection verified | `curl -s domain | findstr "gtag\|zaraz"` shows GA4 snippet |
| 4 | Google Sites GA4 inserted and verified | GA4 Real-Time shows test visit within 60s |
| 5 | Test traffic from 2+ locations visible | Analytics show >=2 distinct countries |
| 6 | cf-ray header confirmed on all proxied sites | `curl -sI domain | findstr "cf-ray"` |

## Infrastructure Verified (Do Not Rebuild)

```
10 Cloudflare Zones ── All active, proxied, Free Website plan
   qnfo.org:         84e9dc1d7fb72629ccdbe3174ed24420
   qwav.tech:        331e4363fd05e8e4fc123ea7d2775411
   q08.org:          fa732a265dd53230b9777908734a74d5
   qnfo.net:         d4e7855f3ed5f0a93204b7bd34e286ab
   qnfo.uk:          26699a3b10699f257eabc34a0faee56d
   qwav.net:         260c09728193c4f902435bad47ce976c
   qwav.org:         4df9cb76facef38e78f6f6fc61cbb7c7
   qwav.uk:          2e0b5be2a41da2a5754269984e7873ad
   q-wave.tech:      dd6908d3cc04acb2efee47382fb94e8e
   qwave.tech:       365f6eebc45b8075aece5a6ecbd2850a

16 Pages Projects ── All HTTP 200, cf-ray present
   14 *.qnfo.org research sites + primer.qwav.tech + deep.qwav.tech + prompts-wiki

Account: quniverse (edb167b78c9fb901ea5bca3ce58ccc4b)
Auth: OAuth token active (wrangler login), GraphQL API works
```

## Dependencies

| Dependency | Status | Blocking? |
|:-----------|:-------|:----------|
| GA4 Measurement IDs | ❌ NOT YET — user must create at analytics.google.com | Yes (blocks Phases 1C, 1D, 2) |
| Wrangler OAuth auth | ✅ Active, token verified | No |
| Analysts:read API token | ⚠️ OAuth token works for GraphQL but not REST | Partial (GraphQL sufficient for dashboard) |
| Google Sites edit access | ❌ Requires user login | Yes (blocks Phase 1D Google Sites GA4) |
| Cloudflare Dashboard access | ✅ YoBrowser can navigate | No |

## Constraints

| Constraint | Value |
|:-----------|:------|
| Cost | $0/month (all free tier) |
| Pages sites affected | 16 |
| Google Sites affected | 3 |
| Zones to configure Zaraz | 2 (qwav.tech + qnfo.org) |
| Effort estimate | 3 sessions (1A: 1 session, 1C: 1 session, 2A: 1 session) |

## Acceptance Gate

- [ ] **SPEC-VS-DELIVERABLE VERIFICATION:** Re-read this handoff spec. Each Success Criterion verified against actual deployment.
- [ ] **TEST PLAN EXECUTED:** Test traffic generated from >=2 locations, analytics data visible in both CF Dashboard and GA4 Real-Time.
- [ ] **DASHBOARD LIVE:** analytics.qnfo.org returns HTML dashboard with Chart.js visualizations.
- [ ] **ALL 16 PAGES SITES VERIFIED:** Every site has CF Web Analytics enabled, cf-ray present, analytics data flowing.

## Escalation

If blocked by GA4 IDs, contact user (rwnq8) to create GA4 property.
If blocked by API auth, request scoped API Token with `Analytics:read`.

## Session→Session Handoff

- **Last session ended:** 2026-05-28 ~10:00 UTC
- **Current git branch:** feature/audit-remediation-2026-05-28
- **Last analytics commits:**
  - `b029158` — Updated strategy doc with zone IDs
  - `d883654` — Strategy document created
  - `bce6b81` — Template updates (CLOUDFLARE-DEPLOYMENT v2.1, DEFINITION-OF-DONE)
- **Files modified this session:** reference/analytics-strategy.md, templates/CLOUDFLARE-DEPLOYMENT.md, templates/DEFINITION-OF-DONE.md
- **Open issues:** rwnq8/prompts#37 (META: Analytics deployment)
- **Next step:** Fill `CLOUDFLARE-DEPLOYMENT` template with action=enable-analytics once GA4 IDs exist. Proceed to Phase 1A (CF Web Analytics via Dashboard).

## Quick Start

```bash
# 1. Check if GA4 IDs are posted:
gh issue view 37 --repo rwnq8/prompts

# 2. Read full strategy:
read "G:\My Drive\prompts\reference\analytics-strategy.md"

# 3. Verify current infrastructure:
wrangler whoami
wrangler pages project list

# 4. Fill deployment template (requires GA4 ID):
fill_prompt_template("CLOUDFLARE-DEPLOYMENT", {
  "action": "enable-analytics",
  "analytics_provider": "both",
  "ga4_measurement_id": "G-XXXXXXXXXX",
  "site_type": "pages",
  "cf_zone_id": "331e4363fd05e8e4fc123ea7d2775411"
})

# 5. Phase 1A: Enable CF Web Analytics via Dashboard (YoBrowser)
#    load_url("https://dash.cloudflare.com/edb167b78c9fb901ea5bca3ce58ccc4b/analytics")
#    Navigate: Web Analytics → Add site → Select Pages project → Enable
```

---

*Handoff generated from HANDOFF-TEMPLATE.md v1.1 by System Prompt Generator v4.6*
*GitHub Issue: rwnq8/prompts#37*
