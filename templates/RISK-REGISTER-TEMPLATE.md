---
template: RISK-REGISTER
version: "1.0"
---

# Risk Register — [PROJECT NAME]

**Last Reviewed:** [YYYY-MM-DD]
**Review Cadence:** Per sprint

## Active Risks

| ID | Description | Likelihood | Impact | Mitigation | Owner | Review Date | Status |
|:---|:------------|:-----------|:-------|:-----------|:------|:------------|:-------|
| R1 | [Risk] | [High/Med/Low] | [High/Med/Low] | [How we prevent/reduce] | [Human/Agent] | [YYYY-MM-DD] | [Active/Monitoring/Resolved] |

## Pre-Populated Known Risks (from CPL)

| CPL Ref | Risk | Default Likelihood | Default Impact | Default Mitigation |
|:--------|:-----|:-------------------|:---------------|:-------------------|
| L1 | Git repository contamination — .git dirs in projects tree | Low | High | system_audit.py Part A3 scans + excludes known deployment repos |
| L3/L6 | Unicode cp1252 console crash on Windows | High | Low | Rule 12: Pre-execution Unicode safety scan |
| L7 | Python -c string corruption on Windows (PowerShell) | High | Medium | Rule 13: HARD BLOCK — never inline Python through PowerShell |
| L13 | Agent claims "committed" without git log verification | Medium | High | §9.3 Post-Work Checklist: git log -1 after every commit |
| L14 | -ErrorAction SilentlyContinue masking critical failures | Medium | High | §0.6.3: Forbidden in verification — use Test-Path or try/catch |
| L15/L17 | Write-then-verify gap — tool success ≠ file exists; audit relies on memory not filesystem | Medium | High | §0.6.1: Test-Path + Get-Content after every write/edit |
| L16 | temperature: 0.0 insufficient for fabrication prevention | Medium | High | Structural guardrails: Due Diligence §0.8, Pre-Send Checklist §E.5.1, git log verification §9 |
| L18/L40 | Write tool silent failure after multiple calls | Medium | High | §0.6.1: Verify after every write; fall back to Python exec for batch ops |
| L19 | Git branch renamed by parallel process | Low | Medium | §9.0.1: Check branch name before every commit against session-start recorded name |
| L20 | Branch reuse across projects — cross-contamination | Low | High | §9.5: Never reuse branches — feature/kebab-case-unique per project |
| L21 | Backlog drift — 7 mandatory docs become stale when files deleted by parallel sessions | Low | Medium | §0.7 Startup Procedure: verify all 7 docs at session start; audit against deleted files |
| L38 | Null-byte placeholder math fix corrupts files | Low | High | Use ASCII-safe markers only; Python scan for null bytes before file writes |
| L39 | Subagent output truncation at ~32K tokens — content lost mid-generation | High | Medium | §3.1: Break long-form generation into sections; parent completes truncated output |

## Resolved Risks

| ID | Description | Resolution Date | Resolution |
|:---|:------------|:----------------|:-----------|
| [R#] | [Risk] | [YYYY-MM-DD] | [How resolved] |

---
*Generated from RISK-REGISTER-TEMPLATE.md v1.0*
