---
template: HANDOFF
version: "1.2"
---

# Handoff: {{type}}

> **⚠️ CLOUDFLARE-NATIVE v3.15:** Handoffs are tracked as R2 objects (`qnfo/audit/handoffs/`) and registered in the Discovery Index. After filling this template, upload to R2: `npx wrangler r2 object put qnfo/audit/handoffs/<filename>.md --file=<local> --remote`. Handoffs are also referenced from project state files at `qnfo/audit/state/<project>.json`.

> **⚠️ STALENESS WARNING (v1.2):** This handoff is a static snapshot. Tasks listed may have been completed since this document was authored. **All handoffs older than 24 hours carry this warning automatically.** Incoming agents MUST verify every task against live Cloudflare infrastructure (R2 object counts, Vectorize index metadata, D1 row counts, Worker deployments) before execution. See DEFAULT.md §3.2 step 1.6 (Infrastructure State Verification Gate). **Trust live infrastructure over handoff documents.**

**Type:** [Program→Project | Project→Task | Session→Session | Project→Project Dependency]
**R2 Handoff:** `qnfo/audit/handoffs/<filename>.md`
**Date:** [YYYY-MM-DD HH:MM UTC] — **Expires:** [YYYY-MM-DD HH:MM UTC] (24h from creation)
**Issuing Authority:** [Who is delegating]
**Accepting Authority:** [Who is receiving]
**Handoff Age at Read:** [Computed by incoming agent — if >24h, ALL tasks require re-verification]

## ⚠️ SEPARATION OF CONCERNS (CPL L42)

**The agent that writes this handoff spec MUST NOT be the same agent instance that builds the deliverable and declares it complete.** The issuing authority provides the spec. The accepting authority builds from the spec. The issuing authority reviews against the spec + test results. Self-certification without independent verification produces untested output.

**For spinoff repos:** Commit 1 = this handoff spec (from issuing authority). Commits 2+ = implementation (from accepting authority). Never: commit 1 = "Initial commit... Ready for deploy" containing a pre-built deliverable.

## Scope

### Included
[List what IS part of this handoff]

### Excluded
[List what is explicitly NOT part of this handoff]

## Success Criteria

| # | Criterion | How Measured |
|:--|:----------|:-------------|
| 1 | [Measurable outcome] | [Verification method] |

## Constraints

| Constraint | Value |
|:-----------|:------|
| [e.g., Budget: human attention hours] | [Value] |
| [e.g., Deadline] | [Value or "None"] |

## Dependencies

| Dependency | Status | Blocking? |
|:-----------|:-------|:----------|
| [Other project/task/resource] | [Ready/Blocked/Complete] | [Yes/No] |

## Acceptance Gate

Before this handoff is considered complete:

- [ ] **SPEC-VS-DELIVERABLE VERIFICATION (CPL L46):** Accepting authority re-reads original handoff spec. Each Success Criterion above is verified against the actual deliverable. Gaps are documented. No "DEPLOYED" or "COMPLETE" status until this audit passes.
- [ ] **TEST PLAN EXECUTED:** Test file(s) exist, were actually run, output committed, pass/fail accounting honest
- [ ] [Issuing authority sign-off]

## Task Provenance (MANDATORY — v1.2 anti-duplication)

**Every executable task listed in this handoff MUST carry a `verified_against` field** documenting what infrastructure was checked to determine this task is still pending. This prevents the #1 churn pattern: agents re-executing completed work because a stale handoff claimed it was needed.

### Provenance Labels

| Label | Meaning | Agent Action |
|:------|:--------|:-------------|
| `[VERIFIED: <timestamp> — <source>]` | Task confirmed pending via live infrastructure check | Execute |
| `[STALE-SOURCE: needs verification]` | Task from static document, not verified against live state | **BLOCK — verify first** |
| `[ALREADY-COMPLETE: <evidence>]` | Live infrastructure shows work already done | **SKIP** |
| `[UNVERIFIABLE: <reason>]` | Cannot verify against live infrastructure | Flag for manual confirmation |

### Required Format for Every Task

```
- [ ] TASK: <description> `[VERIFIED: 2026-06-02T10:00Z — R2: 73 obsidian papers already in qnfo/papers/]`
- [ ] TASK: <description> `[STALE-SOURCE: needs verification — listed in CONSOLIDATION-MASTER.md from 2026-06-01]`
```

**Tasks without a `verified_against` label are automatically `[STALE-SOURCE]` and MUST be verified against live infrastructure before execution. See DEFAULT.md §3.2 step 1.6 and `qnfo/pipeline-status.json` for verification sources.**

## Escalation

If blocked, contact: [Who/How]

## Session→Session Handoff (if applicable)

- Last session ended: [YYYY-MM-DD HH:MM]
- Current git branch: [branch name]
- Last commit: [hash] — [message]
- Files modified this session: [list]
- Open issues: [list]
- Next step for incoming agent: [clear instruction]

---
*Generated from HANDOFF-TEMPLATE.md v1.2 — includes staleness warnings and mandatory task provenance.*
