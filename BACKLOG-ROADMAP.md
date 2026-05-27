# QNFO/QWAV — Complete Backlog, Roadmap & Unfinished Work

> **Generated:** 2026-05-27 by System Prompt Generator v4.6
> **Audience:** Next agent session — read this on startup for full context
> **Status:** ACTIVE — all items below are pending

---

## SESSION COMPLETED (2026-05-27) — What Got Built

| # | Deliverable | Status |
|:--|:------------|:------|
| 1 | Cloudflare audit trail infrastructure (R2 `qnfo/audit/`) | ✅ Deployed |
| 2 | github-sync cron Worker (daily, 06:00 UTC) | ✅ Deployed |
| 3 | cloudflare-deployer skill v2.0 (10 failure modes, all ops) | ✅ Committed |
| 4 | closeout-manager skill v2.0 (R2 audit trail export) | ✅ Committed |
| 5 | REBUILD-FROM-SCRATCH.md (crash recovery, 11.9 KB) | ✅ Committed |
| 6 | CLOUDFLARE-AUDIT-EXPORT template (session closeout format) | ✅ Registered* |
| 7 | DEFAULT.md S10 closeout (mandatory R2 export) | ✅ Committed |
| 8 | Decision log (13 decisions, R2 + GitHub) | ✅ Populated |
| 9 | prompts repo pushed (feature/agent-subagent-refactoring) | ✅ Pushed |
| 10 | github-sync-worker repo pushed (master) | ✅ Pushed |

*\*Needs DeepChat restart to activate (F11)*

---

## IMMEDIATE — Next Session Must Do

### 1. Merge prompts branch to main
```bash
cd "G:\My Drive\prompts"
git checkout main
git merge feature/agent-subagent-refactoring
git push origin main
git branch -d feature/agent-subagent-refactoring
```
3 commits to merge: `2c411f9`, `9192bf1`, `6d0f24a`

### 2. Restart DeepChat (F11)
Template `CLOUDFLARE-AUDIT-EXPORT` is registered in `prompts.json` but the runtime hasn't reloaded. After restart, `list_all_prompt_template_names()` will include it.

### 3. Verify template activation
```
fill_prompt_template("CLOUDFLARE-AUDIT-EXPORT", {test params})
```
If "Template not found" persists, rebuild prompts.json again.

### 4. Push worker project
Worker repo `rwnq8/github-sync-worker` has commit `fe2364c` — verify pushed to origin.

---

## PHASE 2 — High Priority, Ready to Execute

### P2.1: rwnq8 Pages Migration (9 sites)
**Issue:** QNFO/QWAV#74
**Source:** CLOUDFLARE-CLOSEOUT-2026-05-27.md
**Context:** Phase 1 migrated 4 QWAV Pages sites. Phase 2 covers 9 rwnq8 GitHub Pages sites.
**Template:** `CLOUDFLARE-DEPLOYMENT` v2.0
**Skill:** `skill_view('cloudflare-deployer')` v2.0
**Procedure:**
```bash
# For each rwnq8 repo with a Pages site:
# 1. Clone repo
# 2. wrangler pages project create <name> --production-branch main
# 3. wrangler pages deploy
# 4. Map custom domain (CNAME FIRST, then API)
```
**Cost:** $0.00 (free tier — unlimited Pages bandwidth)

### P2.2: Google Site Fixes (3 sites)
**Source:** CLOUDFLARE-CLOSEOUT-2026-05-27.md §5
**Sites:** qwav.tech, qnfo.org, q08.org
**Context:** Google Sites contain broken `qnfo.github.io/*` links. Replace with Cloudflare Pages URLs.
**Replacements:**
| Broken Link | Replacement |
|:-----------|:------------|
| `qnfo.github.io/QWAV/` | `https://deep.qwav.tech` |
| `qnfo.github.io/QWAV/papers` | `https://deep.qwav.tech/papers` |
| `quniverse.cloud` | REMOVE |
| `qni.co` | REMOVE |
**New links to add:** `deep.qwav.tech`, `primer.qwav.tech`, `archive.qnfo.org`
**Tool:** Google Sites → AI Studio App Builder (or manual editing)

### P2.3: Expand github-sync Worker REPOS List
**Current:** Only `rwnq8/prompts` (confirmed: 33 issues)
**Verified repos with issues:**
- `rwnq8/prompts` — 33 issues ✅
- `rwnq8/quantum-laws-of-form` — exists, needs issue count check
- (QNFO repos blocked by org flagging — skip for now)
**Action:** Edit `src/entry.py` REPOS list → redeploy:
```bash
cd "G:\My Drive\projects\github-sync-worker"
# Edit REPOS in src/entry.py
wrangler deploy
Invoke-RestMethod -Uri "https://github-sync.q08.workers.dev" -Method Get
wrangler r2 object get qnfo/audit/github/latest/<repo>-issues.json --remote
```

### P2.4: R2 Bucket Inventory (0pus, mail)
**Source:** CLOUDFLARE-CLOSEOUT-2026-05-27.md §8
**Context:** Buckets `0pus` and `mail` created 2024-06-05, never inventoried.
**Action:**
```bash
wrangler r2 object get 0pus/ --remote   # (if listing supported)
# Or use Cloudflare REST API to list bucket contents
# Document what's in each bucket
```

### P2.5: Email Routing Verification
**Source:** HANDOFF-2026-05-27.md
**Context:** Email routing configured for `papers@qnfo.org`, `collab@qnfo.org`. Never tested.
**Action:**
```bash
# Check email routing config via Cloudflare REST API
# Send test emails to verify routing works
```

---

## PHASE 3 — Needs Design, Medium Priority

### P3.1: Vectorize Population
**Index:** `qwav-research` (768d, cosine, empty)
**Goal:** Semantic search across all QWAV research documents
**Design:**
1. Write embedding Worker — reads R2 audit files → Workers AI `@cf/baai/bge-base-en-v1.5` → insert into Vectorize
2. Chunk documents by section, store with metadata (source, date, category)
3. Cron: daily re-index of changed files
**Skill:** `cloudflare-deployer` v2.0 §3 (Vectorize operations)
**Cost:** $0.00 (30M queries/month free)

### P3.2: ask-qwav Search Endpoint
**Worker:** `ask-qwav.q08.workers.dev` (deployed, AI + Vectorize bindings, no logic)
**Goal:** Agents query one endpoint at session start for full context
**Endpoints to add:**
- `POST /search` — `{"query": "what's the state of X?"}` → top-K relevant chunks
- `GET /context` — returns latest decisions, open issues, recent conversations, infra state
**Design reference:** cloudflare-deployer skill §3.4 (Vectorize + Workers AI pattern)

### P3.3: Infrastructure Snapshot Cron Worker
**Goal:** Automated daily Cloudflare state capture → R2
**Design:**
1. New Worker: `infra-snapshot` — cron daily
2. Queries Cloudflare REST API for: Pages projects, Workers, R2 buckets, DNS zones, Vectorize indexes
3. Writes snapshot to `audit/infrastructure/YYYY-MM-DD-snapshot.json`
4. Compares with previous snapshot, logs changes

### P3.4: Email Workers
**Source:** HANDOFF-2026-05-27.md, CLOUDFLARE-CLOSEOUT-2026-05-27.md
**Context:** `emailqueue` exists (0 producers/consumers since 2024). Email routing configured but not tested.
**Actions:**
1. Configure Email Workers in Cloudflare Dashboard (or via REST API if available)
2. Route `papers@qnfo.org` → Worker → auto-acknowledge, categorize, store
3. Route `collab@qnfo.org` → Worker → notify, archive

### P3.5: Domain WHOIS Monitoring
**Source:** HANDOFF-2026-05-27.md
**Context:** 14 domains. No expiry monitoring. Prevent another qwav.tech 240h outage.
**Design:**
1. New Worker: `domain-monitor` — cron weekly
2. Query WHOIS for all 14 domains
3. Alert if any domain expires within 30 days
4. Export status to R2

### P3.6: Security Headers + Custom 404 Pages
**Source:** HANDOFF-2026-05-27.md
**Context:** `archive.qnfo.org` and `ask-qwav` need security headers. All Pages sites need custom 404.
**Action:** Low priority. Add HTTP headers via Cloudflare transform rules or Pages _headers file.

---

## BACKLOG — Needs Investigation

### B1: QNFO Full Issue List in Archive
**Blocked by:** QNFO org flagging (QNFO/QWAV#62 — 240h+ offline)
**Impact:** GitHub API returns empty for all qnfo/* repos
**Mitigation:** If QNFO org is un-flagged, run `gh issue list` for all qnfo repos and export to R2

### B2: qnfo-archive Pages Site — Complete PM Mirror
**Current:** 9 files, 4 issues archived
**Goal:** Full mirror of all QNFO project management (Issues, Projects, Wiki)
**Blocked by:** QNFO org flagging (can't access Issues via API)

### B3: Email Queue Configuration Audit
**Queue:** `emailqueue` — 0 producers, 0 consumers since 2024-06-05
**Action:** Check if queue is still needed. If email workers are implemented, connect them. Otherwise, document or delete.

### B4: Cross-Project Learnings Wiki Update
**Add:** F11 (system reload needed for templates), F12 (Unicode output crash), F13 (GitHub flagged org quirk), F8 (R2 get without --remote)
**Wiki:** https://github.com/rwnq8/prompts/wiki/Cross-Project-Learnings
**Current lessons:** L1-L40

### B5: System Audit Run
```bash
python "G:\My Drive\prompts\tools\system_audit.py"
```
Expected: 6 PASS, 1 WARN (CROSS-PROJECT-LEARNINGS.md on wiki), 0 FAIL

---

## ROADMAP — Strategic Direction

### R1: Complete Cloudflare Survivability Story
- All rwnq8 repos archived to R2 (currently 15 QNFO repos only)
- All Pages sites on Cloudflare (4 QWAV done, 9 rwnq8 pending)
- All DNS on Cloudflare (14 domains — done)
- R2 audit trail fully automated (foundation built)

### R2: Semantic Search Across All Research
- Vectorize populated with all papers, decisions, conversations
- ask-qwav Worker provides AI-powered Q&A over the entire corpus
- Agents get context with one query instead of reading 6 files

### R3: Fully Autonomous Agent Operations
- Every Cloudflare operation scripted (skills + templates done)
- Every session auto-exported to R2 (DEFAULT.md S10 done)
- Every decision tracked in decision log (infrastructure built)
- Every infrastructure change auto-snapshotted (worker pending)

### R4: Multi-Agent Cloudflare Coordination
- EXPLORER subagent: Cloudflare capability research
- IMPLEMENTER subagent: Worker code generation from specs
- REVIEWER subagent: Cloudflare deployment validation
- Parent agent: orchestrates, handles git + wrangler execution

---

## AGENT STARTUP INSTRUCTIONS

When starting a new session, the agent should:

1. **Read this document** — `G:\My Drive\prompts\BACKLOG-ROADMAP.md` (or from R2 if local is missing)
2. **Verify git state** — `git log -1 --oneline`, `git status`, check branch
3. **Check Cloudflare** — `wrangler whoami`, `wrangler deployments list`
4. **Query R2 audit trail** — `wrangler r2 object get qnfo/audit/conversations/2026-05-27-cloudflare-audit-trail.md --remote`
5. **Check open issues** — `gh issue list --repo rwnq8/prompts`
6. **Review priorities** — P2.1 (Pages migration) and P2.3 (expand worker) are highest impact
7. **Begin work** — Start with the highest-priority Phase 2 item

---

*BACKLOG-ROADMAP.md v1.0 — Everything pending. Give this to any agent. No knowledge required.*
