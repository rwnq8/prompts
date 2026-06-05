---
template: DEEP-DIVE-DISCOVERY
version: "1.0"
date: 2026-06-03
---

# DEEP-DIVE DISCOVERY PROTOCOL — [PROJECT/PHASE]

> **MANDATORY:** Execute this protocol at session start AND after every major phase/task completion. The agent automatically discovers ALL ecosystem records without user prompting. No stone unturned.

---

## STEP 0: ECOSYSTEM INVENTORY

### 0.1 Pull Discovery Index (ALWAYS FIRST)

```bash
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json
```

### 0.2 Cross-Reference ALL Records

| Record | R2 Path | Query |
|:-------|:--------|:------|
| **Open Handoffs** | `qnfo/audit/handoffs/` | ALL — scan for related scope, dependencies |
| **Processed Handoffs** | `qnfo/audit/handoffs/` | Recent (last 7 days) — may contain context |
| **Decision Log** | `qnfo/audit/decisions/DECISION-LOG.md` | ALL decisions affecting target resources |
| **Pipeline Status** | `qnfo/pipeline-status.json` | Check for completed pipelines (avoid re-execution) |
| **Project States** | `qnfo/audit/state/*.json` | ALL active projects — cross-project dependencies |
| **Project Backlogs** | `qnfo/audit/backlog/*.json` | ALL — check for tasks touching same resources |
| **Cloudflare D1** | `qnfo-graph`, `qnfo-audit` | Row counts, table schemas, task statuses |
| **R2 Assets** | `qnfo/releases/YYYY/MM/`, `qnfo/deployments/` | Related publications, deployments |

### 0.3 Infrastructure State Verification (ANTI-DUPLICATION)

For EVERY pipeline/upload/deploy/data task:
1. Query live Cloudflare state (D1 row counts, R2 objects, Worker deployments, Pages projects)
2. Compare task claim against live state
3. If already complete → SKIP with `[ALREADY-COMPLETE: <evidence>]`
4. TRUST LIVE INFRASTRUCTURE OVER HANDOFFS

---

## STEP 1: GAP ANALYSIS

After discovery, document:

- [ ] **What's missing?** — Resources referenced but not found, sections empty in Discovery Index
- [ ] **What's stale?** — Handoffs >24h old, index entries not matching live state
- [ ] **What's conflicting?** — Multiple handoffs touching same resources, overlapping backlogs
- [ ] **What's dependent?** — Other projects that must complete before this one
- [ ] **What's blocked?** — Missing credentials, destroyed resources, unknown state

---

## STEP 2: CROSS-PROJECT IMPACT ASSESSMENT

For EVERY proposed change:

- [ ] **Upstream dependencies:** What must exist before this can proceed?
- [ ] **Downstream impacts:** What will break or need updating after this change?
- [ ] **Shared resources:** Is anyone else using this D1 table / R2 path / Worker?
- [ ] **Index impacts:** Will this require Discovery Index updates? (Almost always YES)

---

## STEP 3: EXECUTION WITH LIVE VERIFICATION

After EVERY phase/task completion:

- [ ] **Re-pull Discovery Index** — detect changes by other agents
- [ ] **Re-check handoff statuses** — any new or updated handoffs?
- [ ] **Verify against live infrastructure** — confirm your changes actually deployed
- [ ] **Log cross-project impacts** — update R2 state with dependency notes
- [ ] **Update Discovery Index** — register new resources, update statuses

---

## OUTPUT FORMAT

```
# DEEP-DIVE DISCOVERY REPORT — [YYYY-MM-DD] [PROJECT/PHASE]

## Ecosystem Inventory
| Record | Checked | Findings |
|:-------|:------:|:---------|
| Discovery Index | [x] | ... |
| Open Handoffs (N) | [x] | ... |
| Decision Log | [x] | ... |
| Pipeline Status | [x] | ... |
| Project States (N active) | [x] | ... |
| D1 Tables | [x] | ... |

## Gap Analysis
- Missing: ...
- Stale: ...
- Conflicting: ...
- Dependent: ...
- Blocked: ...

## Cross-Project Impact
- Upstream: ...
- Downstream: ...
- Shared resources: ...

## Infrastructure Verification
| Resource | Live State | Matches Claim? |
|:---------|:-----------|:--------------:|
...
```

---

*DEEP-DIVE-DISCOVERY Template v1.0 — Mandatory ecosystem discovery protocol. Execute at session start and after every phase.*
