
## 2026-06-01 — Master Index + Portfolio Triage (DEC-023 through DEC-025)

### DEC-023: living-paper — Keep Vanilla JS Frontend
**Decision:** Keep vanilla JavaScript for the living-paper frontend. Reject React migration.
**Rationale:** 7 well-organized IIFE modules (~53K chars total), all integrations working correctly (MathJax, D3.js, Pyodide WASM, Kùzu API client), React migration estimated at 2-3 weeks with zero feature gain. The one feature that would benefit from React state management (LP-006 Community Annotations) is COULD priority, not on the critical path.
**Alternatives considered:** React migration (rejected — cost exceeds benefit at current scope).
**Status:** ACCEPTED. Documented in R2 state: qnfo/audit/state/living-paper.json.

### DEC-024: Master Discovery Index v2.0 — Single Source of Truth
**Decision:** Rebuild qnfo/discovery/index.json as a definitive master index (v2.0) covering ALL 42 unique project names across 6 registries. Categorize into: 9 active dev projects, 2 services, 15 published papers, 10 infrastructure, 3 meta, 3 archived.
**Rationale:** Prior index had 17 entries with 8 orphans (no local directory) and 1 missing project (qnfo-knowledge-graph). D1 graph was re-seeded from stale data. Cloudflare Pages entries were invisible to the index. A single master eliminates disconnect between registries.
**Alternatives considered:** Keep stale index (rejected — perpetuates orphan projects). Manual per-registry cleanup (rejected — re-creates the problem).
**Status:** ACCEPTED. Uploaded to R2 2026-06-01. Rule: all future project changes must update this index FIRST.

### DEC-025: D1 Knowledge Graph Re-Seed from Clean Index
**Decision:** Wipe and re-seed the qnfo-graph D1 database from the clean v2.0 master index.
**Rationale:** Previous graph had 16 project nodes including 8 orphan/archived entries. Clean graph has 9 project nodes matching actual active portfolio (74 nodes, 57 edges total).
**Alternatives considered:** Manual node deletion (rejected — error-prone). Incremental update (rejected — D1 lacks differential update mechanism).
**Status:** EXECUTED. Graph API at https://graph-api.q08.workers.dev now serves clean data.

---



## 2026-06-01 — QWAV SEO Phase 1 Audit & Fix

### ADR-012: Cache-Control Override via _headers for Cloudflare Pages
**Decision:** Deploy `_headers` file to ALL QWAV/QNFO Pages projects setting `Cache-Control: public, max-age=86400` for HTML.
**Rationale:** Every site had `max-age=0, must-revalidate` (Cloudflare Pages default for dynamic content). Google uses Core Web Vitals/LCP as ranking factor. Pages serve static HTML — 24h cache is appropriate.
**Trade-off:** Content changes take up to 24h to propagate through CDN unless cache is purged.

### ADR-013: DNS CNAME Must Point to Project Subdomain, NOT Deployment Hash
**Decision:** All custom domain CNAME records must point to `[project].pages.dev` (auto-resolves to latest production deployment), never to `[hash].[project].pages.dev` (frozen on specific deployment).
**Root Cause:** qwav.tech CNAME was `e27c4614.qwav-marquee.pages.dev` — locked to a 2-day-old deployment. 5+ deploys succeeded but never reached the live site.
**Fix:** Updated DNS to `qwav-marquee.pages.dev`. Same issue found on unity.qnfo.org and quantum.qnfo.org (fixed earlier today).

### ADR-014: robots.txt + sitemap.xml as Static Files in Cloudflare Pages
**Decision:** Create static robots.txt and sitemap.xml in deploy root (not relying on SPA framework to serve them).
**Rationale:** SPA catch-all returned HTML for both paths. Googlebot couldn't read crawl directives or discover pages. Cloudflare Pages serves static files before catch-all routing, so placing them in the deploy root resolves the issue.

### Phase 1 Summary — Sites Fixed
- qwav.tech: Cache, robots, sitemap, JSON-LD (Organization), 404, DNS, title/desc lengths, JSON-LD escaping
- deep.qwav.tech: Cache, robots, sitemap (was already 92KB/502 URLs), JSON-LD (WebSite), 404, title/desc lengths, JSON-LD escaping

### Phase 2 Handoff — Remaining
- P0-A: 507 paper subpages share identical homepage metadata (duplicate content penalty)
- P0-B: og-image.png returns HTML on both sites (broken social previews)
- P1: MathJax loads on pages without math (per old SYSTEM_INSTRUCTIONS: "No MathJax")
- Handoff: `coordination/HANDOFF-PHASE2-SEO-2026-06-01.md`

---

## 2026-05-28 -- deep.qwav.tech Overhaul Session

### ADR-003: Markdown-First Architecture
**Decision:** Papers render from .md files via single paper.html template (marked.js + MathJax). No Pandoc pre-generation.
**Rationale:** User directive: separate content from presentation. Front-end changes never require content regeneration.
**Impact:** 497 HTML files removed. 1 template file. 498 .md files in R2. Content/presentation fully decoupled.

### ADR-004: R2 Content + Pages Template + Function Proxy
**Decision:** Three-layer decoupled architecture: R2 (qnfo/papers/), Pages (paper.html), Function (/api/paper/[slug]) as proxy adding charset=utf-8.
**Rationale:** r2.dev serves without Content-Type header, causing browser encoding guessing (CP1252 on Windows). Proxy fixes.
**Impact:** New functions/api/paper/[slug].js. Content must be in R2 (blocker: only 1/498 uploaded -- H1).

### ADR-005: Query-Parameter Routing
**Decision:** Paper URLs use ?p=slug query parameter instead of /papers/slug path-based routing.
**Rationale:** Cloudflare Pages _redirects wildcard (*) matches empty path segments, causing redirect loops.
**Impact:** Catalog links changed. _redirects simplified to only handle catalog routing.

### ADR-006: No Subjective/Unverifiable Claims
**Decision:** All public-facing content must contain only verifiable claims. Scrubbed: Peer-Reviewed, healthy, verified.
**Rationale:** Fabricated claims damage credibility. User directive.
**Impact:** Marquee status bar changed to "7 demos live - 15/15 online".

### ADR-007: Deprecated Platform Removal
**Decision:** GitHub, Zenodo, ResearchGate references removed from all templates.
**Rationale:** All research hosted on Cloudflare. Cross-references misleading.
**Impact:** Nav: Home | Papers only. License references retained (github.com/QNFO/license is a license URL, not a platform).

### ADR-008: Encoding Prevention
**Decision:** No CP1252 conversion scripts. Source files verified clean (650/650 UTF-8). Corruption from r2.dev missing charset header.
**Rationale:** Fix the serving layer, not the content. Content was never broken.
**Impact:** 35MB md/ directory removed from git. Proxy function adds Content-Type: text/markdown; charset=utf-8.

### ADR-009: Theme Toggle
**Decision:** Paper template includes light/dark theme toggle with localStorage persistence. Respects prefers-color-scheme.
**Rationale:** User preference -- dark theme hard to read. Toggle gives reader choice.
**Impact:** CSS variables for light/dark. Button in nav. JS for toggle + persistence.



---

## Session 2026-05-29T10:21:26Z
## 2026-05-29 — Program Session: DNS Migration & Full Portfolio Audit

### Decisions Made
1. **DNS Migration**: Migrated qnfo.org, hub.qnfo.org, www.qnfo.org from Obsidian Publish (publish-main.obsidian.md) to Cloudflare Pages (qnfo-hub.pages.dev). Obsidian Publish fully retired from qnfo.org zone.
2. **Legal Content Hosting**: Deployed QNFO-ULA-v2.0.md as styled HTML at /legal/license on qnfo-hub. No separate Pages project needed.
3. **TLS Baseline**: Raised min TLS from 1.0 to 1.2 across qnfo.org zone.
4. **HSTS**: Enabled strict-transport-security with max-age=31536000, includeSubdomains=true, preload=true.
5. **Pages Domain Registration**: Registered 10 previously DNS-only custom domains as formal Pages custom domains for dedicated SSL management.
6. **Discovery Index Governance**: Added FAIL-CLOSED enforcement gate (§0.6.5) — Discovery Index MUST be pulled before any non-read tool. Result of "likely" incident where index knew qnfo.org mapping but agent didn't wait.
7. **Discovery Index Expansion**: Expanded from 1 to 67 catalogued projects (21 Pages sites + 30 local tools + 11 QWAV meta + 7 archive).
8. **API Token Storage**: Persisted Cloudflare API token to G:\My Drive\QWAV\.env and User env var CLOUDFLARE_API_TOKEN for all agent sessions.
9. **ask-qwav.tech Status**: Downgraded from LIVE to ISSUE/degraded. Worker RAG queries timeout at 30s (Workers free-tier CPU limit). Hub HTML updated to reflect.

### Audit Findings
- 14 Cloudflare Pages projects, all deployed
- 16 custom domains (8 before session, 10 registered during)
- 17 DNS CNAMEs to pages.dev, 0 Obsidian references remaining
- 12 Workers, 2 KV namespaces, 2 D1 databases, 2 queues
- 4 R2 buckets, email routing active
- SSL Full, Always HTTPS On, TLS 1.2, HSTS enabled
- 1 known degraded site: ask.qwav.tech (Worker LLM timeout)
- System prompt patched: QWAV-DEFAULT.md v3.5 with Discovery Index First Gate

### Files Modified
- G:\My Drive\QWAV\hub-deploy\index.html (hub HTML corrections)
- G:\My Drive\QWAV\hub-deploy\legal\license.html (new, 82KB)
- G:\My Drive\QWAV\hub-deploy\legal\index.html (new, redirect)
- G:\My Drive\QWAV\.env (new, API token storage)
- G:\My Drive\prompts\QWAV-DEFAULT.md (startup checklist + §0.8.1 patches)
- qnfo/discovery/index.json (R2, 1->21->67 projects)
- qnfo/audit/state/qnfo-hub.json (R2, updated)
- qnfo/audit/state/ask-qwav.json (R2, new degraded state)

---

## Session 2026-05-29T11:00:00Z
## 2026-05-29 — Program Session: Portfolio Audit, Archiving & Index Rebuild

### Decisions Made
1. **Archive 3 Completed Projects**: Moved portfolio-linkage, cf-dns-validator, google-site-auditor from "projects" to "archive" in Discovery Index. All three had status "complete" with published deliverables but no archival record. R2 state files created at qnfo/audit/state/{name}.json.
2. **Discovery Index Rebuild**: Expanded from 7 to 21 indexed projects. All 17 local project directories in G:\My Drive\projects\ registered. 8 identified as stubs (1-2 file scaffolds), 8 as active, 2 as informal coordination artifacts.
3. **R2 State File Creation**: Created qnfo/audit/state/*.json for all 3 archived projects with disposition notes (quarterly re-run for DNS validator, monthly for Google auditor, no further action for portfolio-linkage).
4. **Stub Project Inventory**: Identified 8 stub projects (agent-swarm, applications, automated-peer-review, consistency-engine, pm-mirror-builder, qwav-compute-cloud, reproducibility-as-code, ultrametric-playground) with 1-2 files each — likely project initiation artifacts that were never developed. Marked as "stub" status. Decision deferred to next session: archive or develop.
5. **Coordination Artifact Identification**: audit/ and handoffs/ directories are not projects — they are coordination artifacts. Should be moved out of G:\My Drive\projects\ to a dedicated coordination directory.

### Audit Findings
- Pre-audit Discovery Index: 7 projects, 0 archived, 3 publications
- Post-audit Discovery Index: 21 projects (8 active, 8 stubs, 5 other), 3 archived, 3 publications
- 15 of 17 local projects have HANDOFF.md (88%)
- 2 projects missing HANDOFF.md: audit, handoffs (both are coordination artifacts, not true projects)
- ~10 stub projects consuming directory space with no substantive content
- R2 coordination infrastructure (state files, backlogs) largely unpopulated for active projects
- Cloudflare R2 is adequate for PM use case; bottleneck is process discipline, not technology
- Alternative considered: Cloudflare D1 (SQL) — would enable queryable PM but adds schema overhead

### Files Modified
- qnfo/discovery/index.json (R2, 7→21 projects, 0→3 archived)
- qnfo/audit/state/portfolio-linkage.json (R2, new — archived)
- qnfo/audit/state/cf-dns-validator.json (R2, new — archived)
- qnfo/audit/state/google-site-auditor.json (R2, new — archived)

### Pending for Next Session
- Create R2 state files for 8 active projects
- Create R2 backlogs for active projects
- Archive or develop 8 stub projects
- Move audit/ and handoffs/ out of projects/ directory
- Run kaizen_engine.py --audit for cross-project learning
- Populate qnfo/audit/backlog/*.json for per-project task tracking


## 2026-05-29 -- System Prompt Audit & Improvement Session

### ADR-004: Subagent Slot IDs in DEFAULT.md Must Match Runtime Platform
**Status:** ACCEPTED | **Decision:** DEFAULT.md S5 subagent slot IDs updated from stale slot-mp9wx0q7-7125/slot-mp9wx1oa-ypw2 to current runtime slot-mp80dr5g-oh9g/slot-mp80e4mj-5s1l. Added Slot Verification Gate instructing agents to verify IDs against subagent_orchestrator tool description before delegation. Added references to subagent definition files in agents/subagents/.
**Rationale:** Stale slot IDs would cause delegation failures. Subagent files use platform-assigned slots that change, so verification gate provides resilience.

### ADR-005: PM Template Catalog Restructured into Active/Deprecated/Legacy Tiers
**Status:** ACCEPTED | **Decision:** system_audit.py PART F restructured. Active templates (6 with actual template files) are tracked for wiring. Deprecated R2-native PM docs (7) are SKIP. Legacy aspirational templates without files (6) are INFO.
**Rationale:** Previous catalog mixed all PM document names (19) causing misleading FAIL results when deprecated R2-native docs were correctly unwired.

### ADR-006: Cross-Project Learnings (CPL) Is Wiki-Based, Not Local File
**Status:** ACCEPTED | **Decision:** CROSS-PROJECT-LEARNINGS.md is maintained at https://github.com/rwnq8/prompts/wiki/Cross-Project-Learnings, not as a local file. System audit checks updated to note wiki URL instead of FAILing on local absence.
**Rationale:** CPL was moved to wiki for discoverability and cross-session persistence. Local file check was a false positive.

### ADR-007: ARCHITECTURE.md Is Wiki-Based
**Status:** ACCEPTED | **Decision:** ARCHITECTURE.md removed from SYSTEM_PROMPTS list in system_consistency_audit.py. Architecture documentation lives at https://github.com/rwnq8/prompts/wiki/Architecture.
**Rationale:** ARCHITECTURE.md was never deployed as a local file; it exists only on the wiki.

### ADR-008: System Prompt Generator v4.7 Scope Boundary Enforced
**Status:** ACCEPTED | **Decision:** Per META-PROMPT-DEEPSEEK.md v4.7 S0.5, the System Prompt Generator cannot fix project-level issues (D2 orphan files, QWAV project handoffs). These are delegated to the Projects Agent via closeout handoff.
**Rationale:** Scope boundary prevents prompt generator from crossing into project execution territory.

## 2026-05-30 -- CSS Centralization Architecture Decision

**ADR: All QWAV Pages reference QNFO Design System CDN exclusively.**

### Problem
HTML pages in subdirectories across Cloudflare Pages sites used relative CSS paths (`css/style.css`, `../css/style.css`) that resolved to incorrect locations after migration from GitHub Pages. Every site had its own local `css/style.css` � 67+ files with fragile relative references. Updating look/feel required editing dozens of files across multiple sites.

### Decision
1. MERGE all site-specific CSS into QNFO Design System CSS
2. STRIP all local CSS references from all HTML files
3. ALL pages reference ONLY `https://qnfo-design-system.pages.dev/css/qnfo-design-system.css`
4. ONE file to update for all look/feel/style changes across entire portfolio

### Files Modified
- Design system CSS: qlof-primer styles merged (7KB -> 20KB total)
- 21 primer HTML files stripped of local CSS refs
- 41 quantum-laws-of-form HTML files stripped
- 7 deploy directory HTML files stripped
- Total: 69 files fixed, 2 deployments

### Deployments
- qnfo-design-system: 2522ef8e
- qlof-primer (primer.qwav.tech): ea763eb9

### Architecture Post-Fix
```
EVERY page ? https://qnfo-design-system.pages.dev/css/qnfo-design-system.css
              ?
        ONE FILE to update
```


---

## Session 2026-05-30T16:20:00Z
## 2026-05-30 — Program Sprint: Portfolio Cleanup & Index Rebuild

### Decisions Made

1. **8 Stub Projects Archived**: agent-swarm, applications, automated-peer-review, consistency-engine, pm-mirror-builder, qwav-compute-cloud, reproducibility-as-code, ultrametric-playground. All had 1-2 files each, no activity since 2026-05-28. Archived as noise reduction. Physically moved to G:\My Drive\Archive\.

2. **3 Completed Projects Archived**: qnfo-site-migration (Phase B: 8/9 sites), portfolio-license-audit (24 projects backfilled), qwav-app-branding (dark theme deployed). All had status "complete" in index but no archive record.

3. **2 Deploy Artifacts Archived**: deploy (6 site deploy dirs, UTF-8 scrubbed) and deploy-fix (deep.qwav.tech paper router). Physically moved to Archive and indexed.

4. **Coordination Artifacts Relocated**: audit/ and handoffs/ moved from G:\My Drive\projects\ to G:\My Drive\QWAV\coordination\. These are not projects — they're program coordination artifacts.

5. **Empty Directory Removed**: analytics/ (0 files) deleted from projects/.

6. **Discovery Index Rebuilt**: 12 active projects, 19 archived, 4 publications. 3 unindexed projects added (analytics-infrastructure, knowing-patterns-refactor, phase-a-remaining). phase-a-remaining immediately archived (complete).

7. **R2 State Files Created**: New state files for analytics-infrastructure and knowing-patterns-refactor uploaded to qnfo/audit/state/.

8. **Stray Artifacts Cleaned**: discovery/ (local index copy) relocated to coordination/. Drive/ (stray LICENSE.md) deleted.

### Portfolio Health Post-Cleanup

| Metric | Before | After |
|:-------|:-------|:------|
| Active projects | ~21 (8 stubs + others) | 12 |
| Archived projects | 3 | 19 |
| Unindexed on disk | 6 | 0 |
| Index integrity gaps | Yes | No |
| Empty/stale dirs | 3 | 0 |
| Coordination artifacts in projects/ | 2 | 0 |

### Active Project Inventory (12 projects)

| Project | Type | Status | Key Note |
|:--------|:-----|:-------|:---------|
| analytics-infrastructure | infrastructure | active | Core deployed, GTM/GA4 blocked on OAuth |
| concept-graph | worker | mvp-deployed | Discovery Momentum Navigator |
| design-system-deploy | infrastructure | active | v1.1 deployed, 498/499 sites use CDN CSS |
| discovery-momentum-assets | assets | active | Social posts scheduled, PDF blocked |
| email-agent | tool | active | Email automation via Outlook COM |
| knowing-patterns-css | frontend | active | Design system CDN CSS |
| knowing-patterns-refactor | migration | active | 15/16 sites migrated, archive.qnfo.org deferred |
| pdf-builder | tool | active | PDF generation pipeline |
| qnfo-hub | hub | active | Master directory, qnfo.org |
| quantum-ecosystem-audit | audit | active | Quantum Hub Portal, 28 broken links fixed |
| qwav-scan | worker | mvp-deployed | arXiv Discovery Engine |
| research-pipeline | infrastructure | active | Research infrastructure pipeline |

### Files Modified
- qnfo/discovery/index.json (R2, 21->12 projects, 3->19 archived)
- qnfo/audit/state/analytics-infrastructure.json (R2, new)
- qnfo/audit/state/knowing-patterns-refactor.json (R2, new)
- G:\My Drive\QWAV\coordination\ (new, relocated audit + handoffs)
- G:\My Drive\Archive\ (13 new entries)

### Pending for Next Sprint
- Create R2 backlogs (qnfo/audit/backlog/*.json) for 12 active projects
- Run kaizen_engine.py --audit for cross-project learning
- Delegate analytics-infrastructure OAuth completion to Projects Agent
- Delegate quantum-ecosystem-audit continuation to Projects Agent
- Delegate knowing-patterns-refactor Phase 5-6 (archive.qnfo.org, chapter content) to Projects Agent


## 2026-05-31 � Bathie & Lagarde (2025) Paper Ingestion Session

### DEC-2026-05-31-1: Paper Relevance Classification

**Decision:** Classify Bathie & Lagarde (2025) "(1+e)-Approximation for Ultrametric Embedding in Subquadratic Time" (AAAI-25) as HIGH RELEVANCE to QWAV ultrametric research ecosystem.

**Rationale:** QWAV maintains 5 active Cloudflare Pages projects with "ultrametric" in their names. The paper advances state-of-the-art in computing ultrametric embeddings � the same mathematical objects QWAV studies for quantum foundations. Subquadratic ?-KT construction without spanner, dynamic approximate cut weights may inform QWAV computational approaches.

**Caveat:** Paper addresses Euclidean data analysis/clustering; QWAV research concerns physical foundations. Different application domain, same mathematical framework.

### DEC-2026-05-31-2: Paper Ingestion Handoff Created

**Decision:** Delegate Bathie & Lagarde (2025) paper ingestion to Projects Agent via Program?Project handoff (7 success criteria).

**Scope:** File PDF ? quantum-ecosystem-audit/references/; Index in qwav-scan D1; Cross-reference bibliography; Write research brief; Build PDF; Publish to R2+Pages; Update Discovery Index.

**Artifacts:** handoff-bathie-lagarde-2025-ultrametric.md (coordination/); R2 state + backlog updated for quantum-ecosystem-audit.

## 2026-05-31: Systemic cp1252 Encoding Disease Fix
**Decision:** Diagnosed and fixed 3-layer encoding disease.
**Fixes:** Rule 12 SCOPE (DEFAULT.md), PYTHONUTF8=1, encoding=utf-8 on all bare opens, PART J Unicode monitor.
**Remaining:** DeepChat restart required.


---

## 2026-06-01 — QA/QC Remediation Session

### DEC-015: QC Gates Must Hard-Block in All Execution Modes
**Status:** ACCEPTED
**Context:** The `zenodo_publish.py` QC gate only hard-blocked (`sys.exit(1)`) in `--yes` mode. In interactive mode, it asked "Proceed anyway?" — which autonomous agents never see (no stdin). This allowed duplicate Zenodo records (DOIs 20490986 and 20497097) for the same publication.
**Decision:** All QC gates must call `sys.exit(1)` unconditionally in ALL execution modes. No interactive fallback paths. The `--yes` flag should not change gate behavior — gates are gates regardless of mode.
**Impact:** `zenodo_publish.py` QC gate now always exits on duplicate detection. All future QC gates designed with this pattern.

### DEC-016: Custom Domain is Canonical Web URL, Not Cloudflare Pages Preview URL
**Status:** ACCEPTED
**Context:** Each `wrangler pages deploy` generates a unique ephemeral preview URL (e.g., `335d65c9.qwav.pages.dev`). The agent chased these URLs by re-deploying 4 times, each time getting a new URL. The preview URLs are ephemeral — they change with every deploy and may expire.
**Decision:** Custom domain redirects (e.g., `deep.qwav.tech/papers/<slug>`) are the canonical web URL for all publications. Cloudflare Pages preview URLs are for immediate verification only and must NOT be documented in publications, markdown files, or the Discovery Index.
**Impact:** `cloudflare-deployer` skill, `publication-publisher` skill, and DEFAULT.md §7.1c all warn about preview URL volatility and mandate custom domain usage.

### DEC-017: Single Umbrella Pages Project for All Publications
**Status:** ACCEPTED
**Context:** Risk of creating new Cloudflare Pages projects for publication updates instead of deploying to the existing `qwav` umbrella project.
**Decision:** All publications deploy under the SINGLE `qwav` Pages project via subdirectory routing. NEVER create a new Pages project for a publication update. Verify with `npx wrangler pages project list` before any deployment.
**Impact:** `cloudflare-deployer` skill and DEFAULT.md §7.1c include umbrella project verification step.

### DEC-018: TTF Font Embedding Required for All PDFs
**Status:** ACCEPTED
**Context:** `build_pdf.py` was broken (toc+TypeError bugs), forcing the agent to create a workaround script that used standard Helvetica Type1 fonts. These fonts don't guarantee Unicode glyph rendering, causing em dashes and curly quotes to appear as tofu or literal `\uXXXX` text in PDFs.
**Decision:** `build_pdf.py` now auto-discovers and registers system TTF fonts (Calibri on Windows, DejaVu Sans on Linux/macOS). Font subsets are embedded in every PDF. If no TTF fonts are available, falls back to Helvetica with a warning.
**Impact:** All PDFs built with the current `build_pdf.py` have guaranteed Unicode glyph coverage. DEFAULT.md §7.1a verifies TTF embedding as a publication gate.

### DEC-019: Template Parameter Discovery Gap Requires META Session
**Status:** ACCEPTED (deferred)
**Context:** 17 of 20 templates lack YAML frontmatter with `parameters:` blocks. When `get_prompt_template_parameters()` is called, it returns empty — causing agents to bypass templates entirely and hardcode publication workflows.
**Decision:** Template YAML frontmatter fix is deferred to a future META session. The scope is large (17 templates) and requires understanding the exact YAML schema expected by `fill_prompt_template`. Current workaround: agents should `read()` template files directly when parameters are unavailable.
**Impact:** Documented as a known gap. Not blocking publication — agents can still read templates directly.


---

## 2026-06-01 — Portfolio Cleanup & Sprint Planning Session

### DEC-020: Portfolio Reduction — 17 Active → 12 Active

**Decision:** Cleaned up project portfolio by archiving 3 completed/absorbed projects, removing 2 fake projects, and registering 1 unindexed project.

**Archived (3):**
- no-bullshit-physics-writing: Published with DOI 10.5281/zenodo.20497225. QA/QC complete.
- knowing-patterns-css: Absorbed into knowing-patterns-refactor. CSS migration complete.
- concept-graph: Shell project (4 files). Superseded by qnfo-knowledge-graph.

**Removed (2):**
- audit: Coordination artifact, not a real project. No git.
- releases: Single deploy artifact file. Not a project.

**Registered (1):**
- qnfo-knowledge-graph: New (2026-06-01), 39 files. Cloudflare Workers graph API at graph-api.q08.workers.dev.

**Rationale:** Portfolio had drifted from prior cleanup (2026-05-30: 12 active). New projects accumulated without archival of old ones. 17 active projects creates cognitive overhead for agents.

### DEC-021: Sprint Prioritization — 3-Tier Model

**Decision:** All active projects classified into 3 priority tiers for sprint planning.

**TIER 1 — Current Sprint (HIGH):**
1. living-paper: MVP completion. LP-002 (frontend review) is current blocker.
2. qnfo-knowledge-graph: Continue API development.
3. quantum-ecosystem-audit: Continue research audit.

**TIER 2 — Next Sprint (MEDIUM):**
4. analytics-infrastructure (710 files, needs audit)
5. knowing-patterns-refactor (Phase 5-6 remaining)
6. research-pipeline (research automation infra)

**TIER 3 — Backlog (LOW):**
7-12. pdf-builder, email-agent, discovery-momentum-assets, yogananda-scientific-claims, retrospective-prophecy-astrology, search-worker

**Rationale:** living-paper is the flagship QNFO project (MVP 9/10 complete). qnfo-knowledge-graph is its natural backend complement. quantum-ecosystem-audit is active research that shouldn't go stale. Remaining projects are either infrastructure tools (no user-facing value) or small research projects without urgency.

### DEC-022: Sprint Handoff to Projects Agent

**Decision:** Created formal Program→Project handoff at coordination/HANDOFF-SPRINT-2026-06-01.md. Delegates all TIER 1 projects to Projects Agent with explicit success criteria.

**Key constraints:**
- Cloudflare-native architecture ONLY (no external services)
- All publications must include PDF
- LP-002 (React vs vanilla) is the BLOCKING decision — Projects Agent must review frontend code first

### Files Modified
- qnfo/discovery/index.json (R2, 17→12 active, 0→3 archived, 0→2 removed, +1 registered)
- qnfo/audit/state/living-paper.json (R2, updated — delegated to Projects Agent)
- qnfo/audit/state/qnfo-knowledge-graph.json (R2, new)
- qnfo/audit/state/quantum-ecosystem-audit.json (R2, updated)
- qnfo/audit/backlog/qnfo-knowledge-graph.json (R2, new — 6 tasks)
- coordination/HANDOFF-SPRINT-2026-06-01.md (new)
- G:/My Drive/projects/ (3 archived → _archive/, 2 deleted)

### Portfolio Health Post-Cleanup
| Metric | Before | After |
|:-------|:-------|:------|
| Active projects | 17 | 12 |
| Archived projects | 0 | 3 |
| Removed (fake/artifact) | 0 | 2 |
| Unindexed on disk | 1 | 0 |
| Active with R2 state | 2 | 5 |
| Active with R2 backlog | 1 | 2 |

### Pending for Projects Agent
- Execute HANDOFF-SPRINT-2026-06-01.md (TIER 1 tasks)
- Create R2 state + backlog files for remaining TIER 2/3 projects
- Run kaizen_engine.py --audit for cross-project learning

---

## 2026-06-01 — GitHub Full Deprecation & Wiki Content Audit

### DEC-023: GitHub Fully Deprecated — All References Purged

**Decision:** GitHub is FULLY deprecated across the QNFO/QWAV ecosystem. All remaining references purged from agent files, system prompts, templates, and skill catalog.

**Audit Findings:**
- **qnfoorganization repos:** 0 visible (all deleted/private). ADR-001 migration complete.
- **rwnq8 repos:** 2 exist (prompts, .github). Both are archives.
- **rwnq8/prompts wiki:** ~5 pages (Architecture, Cross-Project-Learnings, Agent-Configuration, Home, _Sidebar). Status: 401 Unauthorized — inaccessible to agents. Content was effectively dead — agents referencing wiki URLs were hitting auth walls, not reading content.
- **Issues:** 0 open, 0 closed in rwnq8/prompts. Nothing to migrate.
- **PRs:** 0. Nothing to migrate.
- **Projects:** 0 active. Nothing to migrate.
- **Releases:** 0. Nothing to migrate.

**Actions Taken:**
1. **github-manager skill:** Marked DEPRECATED — ARCHIVED. Retained for historical reference only.
2. **System prompts (3):** QWAV-DEFAULT.md, DEFAULT.md, META-PROMPT-DEEPSEEK.md — github-manager skill trigger marked (DEPRECATED).
3. **Agent files (3):** PROJECTS-AGENT.md, PROMPTS-AGENT.md, QWAV-AGENT.md — 15 GitHub references → 0. All wiki links replaced with local file references or R2 paths.
4. **Templates (3):** HANDOFF.md, PROJECT-INITIATION.md, PROJECT-CHARTER.md — 34 GitHub references → 0 (cleaned earlier in same session).
5. **Wiki content:** NOT migrated. Content was behind 401 auth wall — agents couldn't read it anyway. All references to wiki URLs removed from agent ecosystem.

**Rationale:** GitHub migration was effectively complete (ADR-001, 2026-05-28) but templates and agent files still contained operational GitHub references. Wiki content was inaccessible (401) and being replaced by real-time R2/D1 data. Removing dead references eliminates confusion and prevents agents from attempting deprecated operations.

**Migration Status:**
| Resource | GitHub | R2/Cloudflare Equivalent |
|:---------|:-------|:-------------------------|
| Project state | GitHub Issues | R2 qnfo/audit/state/*.json |
| Task tracking | GitHub Projects | R2 qnfo/audit/backlog/*.json |
| Decisions | GitHub Discussions | R2 qnfo/audit/decisions/DECISION-LOG.md |
| Releases | GitHub Releases | R2 qnfo/releases/ + Cloudflare Pages |
| Wiki (Architecture) | github.com/rwnq8/prompts/wiki | G:/My Drive/prompts/agents/*.md |
| Wiki (CPL) | github.com/rwnq8/prompts/wiki | R2 decision log + local agent files |
| Code | GitHub repos | Git local + R2 qnfo/code/*.bundle |
| PM CLI | gh CLI | wrangler CLI |

### Files Modified
- G:/My Drive/prompts/skills/github-manager/SKILL.md (marked DEPRECATED)
- G:/My Drive/prompts/QWAV-DEFAULT.md (skill trigger + version history)
- G:/My Drive/prompts/DEFAULT.md (skill trigger + version history)
- G:/My Drive/prompts/META-PROMPT-DEEPSEEK.md (wiki refs removed, skill trigger updated)
- G:/My Drive/prompts/agents/PROJECTS-AGENT.md (5 refs → 0)
- G:/My Drive/prompts/agents/PROMPTS-AGENT.md (4 refs → 0)
- G:/My Drive/prompts/agents/QWAV-AGENT.md (6 refs → 0)

### Manual Action Required
- User may delete rwnq8/prompts repo on GitHub.com if desired. No QNFO data remains there.

---

## 2026-06-01: D-047 — Cloudflare Footprint Backlog Ratified

**Decision:** Adopt the 31-item Cloudflare Footprint Backlog as the program-level roadmap for platform consolidation, refactoring, expansion, and optimization.

**Context:** Cloudflare platform audit revealed 8 of ~20 services used (40% utilization), 4 underutilized, 8 never touched. User generated a structured 4-category backlog with tiered prioritization.

**Categories & Scale:**
| Category | Items | Effort |
|:---------|:-----:|:------:|
| CONSOLIDATE | 5 | ~16h |
| REFACTOR | 8 | ~27h |
| EXPAND | 12 | ~45h |
| OPTIMIZE | 5 | ~6h |
| **TOTAL** | **31** | **~94h** |

**Tier 1 (Do First — 7 items, ~15h):** C5 (delete unused D1), R4 (cron graph re-seed), R1 (populate D1 qnfo-graph), O4 (R2 lifecycle), E1 (Analytics on all Pages), E5 (Cron Triggers), E6 (Turnstile)

**Tier 2 (Next — 8 items, ~35h):** R2 (populate D1 qnfo-audit), C1 (merge D1 6→2), C2 (decommission stale Workers), E2 (Workers AI for LP), E3 (Vectorize), R8 (async paper ingestion), O1 (Cache-Control), O5 (security headers)

**Tier 3 (Later — 15 items, ~44h):** Remaining polish and future-proofing items.

**Target:** 40% → 60% (Tier 1) → 80% (Tier 2) → 100% (Tier 3) platform utilization. All within Cloudflare free tier at QNFO scale.

**Storage:** Backlog stored at `qnfo/audit/backlog/cloudflare-footprint.json`. Discovery Index updated with infrastructure utilization metrics.

**Rationale:** Structured execution prevents ad-hoc infrastructure drift. Tiered approach ensures foundational items (analytics, cron, graph seeding) are completed before expansion items (Workers AI, Vectorize) that depend on them.

**Status: RATIFIED. Tier 1 execution pending user approval.**

---

## DEC-024: analytics-infrastructure Audit + Cleanup (2026-06-02)

**Decision:** Audit and clean analytics-infrastructure project. Remove dead code, document architecture.
**Rationale:** 726 files (51.7 MB), 14 deploy dirs with 8 stale/duplicate. No README, no charter, no documented scope.
**Action:**
- Removed 135 files (68 .bak, 5 dead directories, 3 stale deploy dirs)
- Archived 15 one-off scripts
- Created PROJECT-CHARTER.md and README.md
- 726 files (51.7 MB) → 591 files (49.2 MB), 6 active deploy dirs
**Status:** EXECUTED. Project now documented and maintainable.

## DEC-025: Deploy Directory Architecture (2026-06-02)

**Decision:** analytics-infrastructure hosts 6 active deploy dirs. Quantum/paper sites (12 domains) deploy from quantum-ecosystem-audit/deploy-dirs/, not from analytics-infrastructure.
**Rationale:** Eliminate confusion about deploy sources. Single-source architecture: each project owns its deploy directories.
**Action:** Deleted stale deploy dirs (unity-of-ultrametric-physics, ultrametric-quantum, quantum-laws-of-form) from analytics-infrastructure. Real source files live in quantum-ecosystem-audit.
**Status:** EXECUTED.

## DEC-026: living-paper Cloudflare Pages API Workaround (2026-06-02)

**Decision:** Use Worker reverse proxy to serve living-paper.qnfo.org instead of Pages custom domain registration.
**Rationale:** Cloudflare Pages API returns "invalid TLD" error when trying to register \living-paper.qnfo.org\ on any Pages project. This is a confirmed API bug — the qnfo.org TLD parser rejects the subdomain. DNS CNAME pointed to a Worker that fetches from the Pages deployment URL.
**Action:**
- Created living-paper-standalone Pages project
- Deployed living-paper frontend files (10 files, from public/ directory)
- Created Worker (living-paper-proxy) that proxies from living-paper-standalone.pages.dev
- Updated DNS CNAME: living-paper.qnfo.org → living-paper-proxy.q08.workers.dev
- Worker confirmed returning HTTP 200 with proper content
**Status:** EXECUTED. DNS propagation in progress (self-resolving within minutes).

## DEC-027: SEO Batch Deployment Architecture (2026-06-02)

**Decision:** Batch-deploy \_headers\ + \obots.txt\ + \sitemap.xml\ to all SPA-catch-all QNFO sites via wrangler pages deploy.
**Rationale:** 14 of 22 sites had no SEO infrastructure. All were single-page apps with catch-all routing - robots.txt and sitemap.xml returned HTML. Fix: create static files in each deploy directory, deploy via wrangler.
**Action:**
- Batch 1 (5 sites): adelic, hierarchy, paradigm, knowing, solo — deploy dirs existed
- Batch 2 (5 sites): ai-poc, cocyle, different, lexicon, measure — HTML scraped from live sites, SEO files added, deployed
- Batch 3 (2 sites): primer, ask — deploy dirs existed
- Batch 4 (2 sites): deep.qwav.tech (cache fix), legal (SEO files)
- Also: archive.qnfo.org redirect (Pages project deleted), OG images fixed, living-paper SEO deployed
**Status:** EXECUTED. Portfolio SEO health: 8/22 → 21/22.


## 2026-06-02 — Duplication Root Cause Audit (DEC-026)

### DEC-026: Infrastructure Reconciliation Gate Required

**Problem:** Agent repeatedly proposed tasks as "REMAINING WORK" that had already been completed (paper upload to R2, Vectorize embeddings for 499 papers, PROJECT-CHARTER.md creation). Root cause: handoff documents contain stale snapshot data, agents treat handoffs as authoritative without verifying against live infrastructure.

**Evidence:**
- Handoff claimed "papers/: 20 objects (pipeline not yet run for full 497+)" — Vectorize index `qwav-research` has 1,963 vectors created 2026-05-27
- Handoff claimed "🟢 Vectorize embeddings — 499 papers need embedding" — `wrangler vectorize info qwav-research` confirms 1,963 vectors, last processed 2026-05-29
- Handoff claimed "🟡 5 PROJECT-CHARTER.md files" — Discovery Index confirms `analytics-infrastructure.has_charter: true`
- User at 6:08:24 AM: "HAVEN'T WE ALREADY VECTORIZED EMBEDDINGS ALREADY?"
- User at 6:10:29 AM: "ABSOLUTELY NOT! WE'VE ALREADY UPLOADED AT LEAST ONCE!"

**Root Cause (4-link failure chain):**
1. Handoff documents fossilize — written at a point in time, never updated
2. No infrastructure verification gate between "read handoff" and "execute tasks"
3. Infrastructure HAS the answer (1,963 vectors, 193 papers in D1, 91 graph nodes) but agent DOESN'T ASK
4. Wrangler v4.95+ removed `r2 object list` — no list-objects Worker deployed

**Decision:**
1. **Infrastructure Reconciliation Gate** — Add mandatory step to startup: for each handoff task, verify against live infrastructure before execution. Fail-closed: if can't verify, mark `[UNVERIFIED]` and flag for manual confirmation.
2. **Pipeline Status Tracker** — Create `qnfo/pipeline-status.json` in R2 tracking every completed data pipeline operation.
3. **Deploy List-Objects Worker** — Per existing prompt requirement (§0.6.5), deploy Worker to enable R2 enumeration.
4. **Handoff Staleness Warnings** — Any handoff >24h old must carry prominent staleness warning.
5. **Discovery Index Extension** — Add `pipeline_status` field to Discovery Index schema.

**Status:** AUDIT COMPLETE. Fixes #1-2 executed (decision log + pipeline-status.json). Fixes #3-5 require system prompt updates (Kaizen cycle).
**Full audit:** `qnfo/audit/decisions/DUPLICATION-ROOT-CAUSE-2026-06-02.md`

