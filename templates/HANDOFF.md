---
template: HANDOFF
version: "1.1"
---

# Handoff: {{type}}

**Type:** [Program→Project | Project→Task | Session→Session | Project→Project Dependency]
**Date:** [YYYY-MM-DD]
**Issuing Authority:** [Who is delegating]
**Accepting Authority:** [Who is receiving]

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
*Generated from HANDOFF-TEMPLATE.md v1.1*
