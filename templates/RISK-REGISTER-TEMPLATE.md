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
| L7 | Python -c string corruption on Windows | High | Medium | Rule 13: HARD BLOCK |
| L3/L6 | Unicode cp1252 console crash | High | Low | Rule 12: Pre-execution scan |
| L18/L40 | Write tool silent failure | Medium | High | §0.6.1: Verify after every write |
| L14 | -ErrorAction SilentlyContinue masking | Medium | High | §0.6.3: Forbidden in verification |
| L39 | Subagent output truncation | High | Medium | §3.1: Parent completes |
| L19 | Branch renamed by parallel process | Low | Medium | §9.0.1: Check before every commit |

## Resolved Risks

| ID | Description | Resolution Date | Resolution |
|:---|:------------|:----------------|:-----------|
| [R#] | [Risk] | [YYYY-MM-DD] | [How resolved] |

---
*Generated from RISK-REGISTER-TEMPLATE.md v1.0*
