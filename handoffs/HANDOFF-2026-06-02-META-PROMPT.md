---
template: HANDOFF
version: "1.2"
---

# Handoff: META-PROMPT → Projects Agent + QWAV Agent

> **⚠️ STALENESS WARNING (v1.2):** This handoff is a static snapshot. Tasks listed may have been completed since this document was authored. **All handoffs older than 24 hours carry this warning automatically.** Incoming agents MUST verify every task against live Cloudflare infrastructure (R2 object counts, Vectorize index metadata, D1 row counts, Worker deployments) before execution. See DEFAULT.md §3.2 step 1.6 (Infrastructure State Verification Gate). **Trust live infrastructure over handoff documents.**

**Type:** Program→Project + Program→Program
**R2 Handoff:** `qnfo/audit/handoffs/HANDOFF-2026-06-02-META-PROMPT.md`
**Date:** 2026-06-02 11:50 UTC — **Expires:** 2026-06-03 11:50 UTC
**Issuing Authority:** META-PROMPT v5.8
**Accepting Authority:** Projects Agent (DEFAULT v3.18) + QWAV Agent (v3.17)
**Handoff Age at Read:** [Computed by incoming agent — if >24h, ALL tasks require re-verification]

---

## Scope

### Included
- Portfolio API Worker architecture implementation (H1-H3)
- Subagent regeneration from META-PROMPT v5.8 (H4)
- Skills Embedded Scripts gap closure (H5)
- Template YAML frontmatter gap closure (H6)
- Cloudflare resource recovery (H7)
- Discovery Index update (H8)
- D1+DO architecture decision logging (Q1-Q3)

### Excluded
- System prompt protocol changes (completed this session)
- Deploy pipeline fixes (completed this session)
- System audit (completed this session)

---

## Success Criteria

| # | Criterion | How Measured |
|:--|:----------|:-------------|
| 1 | Portfolio API Worker deployed with D1 state tables | `GET /v1/health` returns `d1_connected: true, do_connected: true` |
| 2 | Read-only agent IAM tokens provisioned | `wrangler whoami` shows `read` scope only |
| 3 | Request-time duplicate prevention working | `POST /v1/pipelines` with duplicate name returns `409 Conflict` |
| 4 | Subagents regenerated from META-PROMPT v5.8 | EXPLORER/IMPLEMENTER/REVIEWER version headers show v1.4 |
| 5 | 6 skills have Embedded Scripts sections | `_system_audit.py` shows 0 warnings for skill:Embedded |
| 6 | 8 templates have YAML frontmatter | `_system_audit.py` shows 0 warnings for template:frontmatter |
| 7 | qwav-scan D1 status documented | Decision logged with recover/archive/destroy determination |
| 8 | Discovery Index updated with current state | Index shows `last_audit: 2026-06-02` for all active projects |

---

## Constraints

| Constraint | Value |
|:-----------|:------|
| Architecture | Cloudflare-native ONLY (D1 + DO + Workers + Queues + R2 for blobs) |
| IAM model | Agents: read-only tokens. Worker: admin token (never exposed). Capability-based temporary writes. |
| Template persistence | `agent.db.custom_prompts` table (NOT JSON files — DeepChat overwrites them) |
| Prompt versions | DEFAULT v3.18, QWAV v3.17, META-PROMPT v5.8 |

---

## Dependencies

| Dependency | Status | Blocking? |
|:-----------|:-------|:----------|
| Cloudflare account access (quniverse) | Ready | No |
| wrangler v4.95+ | Ready | No |
| portfolio-api Worker (to be created) | Not started | Yes for H2-H3 |
| agent.db schema knowledge | Known | No |

---

## Task List — Projects Agent (H1-H8)

### PRIORITY 0 (BLOCKING)

- [ ] **H1: Portfolio API Worker** `[VERIFIED: 2026-06-02T11:50Z — DESIGN COMPLETE, needs implementation]`
  - Deploy `portfolio-api.q08.workers.dev` Worker
  - D1 database `portfolio-state` with schema: `resources`, `pipeline_runs`, `sessions`, `decisions`, `audit_log`, `index_checksums`, `handoffs`
  - Durable Object `StateRegistry` for per-resource global locking with version tracking
  - Queues for pipeline task deduplication
  - API endpoints: `POST /v1/resources`, `GET /v1/resources/:id`, `POST /v1/pipelines`, `PATCH /v1/pipelines/:id`, `POST /v1/lock/acquire`, `POST /v1/lock/release`, `GET /v1/portfolio`, `GET /v1/health`

- [ ] **H2: IAM Read-Only Agent Tokens** `[VERIFIED: 2026-06-02T11:50Z — DESIGN COMPLETE, needs Cloudflare dashboard action]`
  - Create read-only Cloudflare API tokens for agent use
  - Store admin token as Worker secret (never exposed to agents)
  - Implement capability-based temporary write grants: `POST /v1/capabilities/request`

### PRIORITY 1

- [ ] **H3: Request-Time Prevention** `[VERIFIED: 2026-06-02T11:50Z — Depends on H1 completion]`
  - Worker API validates every operation before execution
  - `UNIQUE(pipeline_name, status)` constraint prevents duplicate pipeline completions
  - DO lock versioning rejects stale writes (`version` mismatch → 409 Stale)
  - No reconciliation window — all checks at request time

- [ ] **H4: Subagent Regeneration** `[VERIFIED: 2026-06-02T11:50Z — agents/subagents/EXPLORER-SUBAGENT.md etc.]`
  - Regenerate EXPLORER-SUBAGENT.md from META-PROMPT v5.8
  - Regenerate IMPLEMENTER-SUBAGENT.md from META-PROMPT v5.8
  - Regenerate REVIEWER-SUBAGENT.md from META-PROMPT v5.8
  - Update version: v1.3 → v1.4, generation tag: v5.4 → v5.8

- [ ] **H7: Cloudflare Resource Recovery** `[VERIFIED: 2026-06-02T11:50Z — Discovery Index infrastructure warnings]`
  - qwav-scan D1: 193 papers, marked "Recover data before deleting"
  - consistency-engine: was destroyed, needs decision (rebuild? archive?)
  - Document both decisions in DECISION-LOG.md

- [ ] **H8: Discovery Index Update** `[VERIFIED: 2026-06-02T11:50Z — _discovery_index.json]`
  - Fix living-paper DNS status (currently "propagating" → "resolved")
  - Add missing PROJECT-CHARTER entries for 5 projects
  - Sync pipeline_status with current R2/Vectorize/D1 state
  - Upload to R2: `npx wrangler r2 object put qnfo/discovery/index.json`

### PRIORITY 2

- [ ] **H5: Skills Embedded Scripts** `[STALE-SOURCE: needs verification — listed in _system_audit.py warnings]`
  - bling-usability-audit, closeout-manager, git-hygiene, github-manager, kaizen-autonomous-update, template-catalog
  - Add `## Embedded Scripts` section to each SKILL.md per DEFAULT.md §6.1

- [ ] **H6: Template Frontmatter** `[STALE-SOURCE: needs verification — listed in _system_audit.py warnings]`
  - DISCOVERY-PROTOCOL, EMAIL-AGENT, KAIZEN-AUDIT, KAIZEN-AUTONOMOUS-UPDATE, PDF-BUILDER, PDF-BUILDER-TEMPLATE, RESEARCH-PROTOCOL, SOCIAL-ORCHESTRATOR-TEMPLATE
  - Add YAML frontmatter with `template:` and `version:` fields

---

## Task List — QWAV Agent (Q1-Q3)

- [ ] **Q1: DEC-027 — D1+DO Portfolio Architecture** `[VERIFIED: 2026-06-02T11:50Z — Design documented in META-PROMPT session]`
  - Log architectural decision to migrate portfolio state from R2 blobs to D1 + Durable Objects
  - Justification: R2 has no schema validation, no transactions, no concurrency control, no duplicate prevention

- [ ] **Q2: DEC-028 — Read-Only Agent Token IAM Policy** `[VERIFIED: 2026-06-02T11:50Z — Design documented]`
  - Log architectural decision for read-only agent tokens + Worker-held admin token
  - Justification: Prevents agents from bypassing the Worker API for destructive operations

- [ ] **Q3: Verify qwav-scan Recovery Status** `[VERIFIED: 2026-06-02T11:50Z — D1 database exists, 193 papers]`
  - Query `wrangler d1 execute qwav-scan --remote --command "SELECT COUNT(*) FROM papers"`
  - Log decision: recover or archive? If recover, create pipeline for data extraction

---

## Acceptance Gate

Before this handoff is considered complete:

- [ ] **SPEC-VS-DELIVERABLE VERIFICATION (CPL L46):** Accepting authority re-reads original handoff spec. Each Success Criterion above is verified against the actual deliverable. Gaps are documented. No "DEPLOYED" or "COMPLETE" status until this audit passes.
- [ ] **TEST PLAN EXECUTED:** Test file(s) exist, were actually run, output committed, pass/fail accounting honest
- [ ] META-PROMPT sign-off: Verified against Portfolio Awareness Protocol (§4.7)

## Task Provenance (MANDATORY — v1.2 anti-duplication)

Every executable task above carries a `verified_against` label. Tasks were verified against:
- Discovery Index (`_discovery_index.json`)
- System audit report (`_system_audit.py` output)
- Live Cloudflare state (R2, Vectorize, D1)
- Git log (`git log --oneline -15`)

## Escalation

If blocked, contact: META-PROMPT agent session or review DEFAULT.md §3.2 step 1.6-1.8

---

## Session→Session Handoff

- Last session ended: 2026-06-02 11:50 UTC
- Current git branch: main
- Last commit: 02ca597 — deploy.py template persistence fix
- Files modified this session: DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT-DEEPSEEK.md, HANDOFF.md, tools/deploy.py, app-settings.json, prompts.json, _discovery_index.json, tools/build_pdf.py, tools/zenodo_publish.py, templates/PDF-BUILDER-TEMPLATE.md, skills/publication-publisher/SKILL.md, skills/email-composer/SKILL.md, skills/template-catalog/SKILL.md, templates/DEFINITION-OF-DONE.md, templates/KAIZEN-AUTONOMOUS-UPDATE.md
- Open issues: Templates require DeepChat restart to load from agent.db
- Next steps: Deploy H1-H3 (Portfolio API Worker), regenerate subagents (H4), close skill/template gaps (H5-H6)

---
*Generated from HANDOFF-TEMPLATE.md v1.2 — includes staleness warnings and mandatory task provenance.*
