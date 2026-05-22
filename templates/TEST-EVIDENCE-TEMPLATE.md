---
template: TEST-EVIDENCE
version: "1.0"
---

# Test Evidence — [Test Suite Name]

**Project:** [PROJECT NAME]
**Date executed:** [YYYY-MM-DD HH:MM]
**Executed by:** [Agent]
**Phase gate:** [P2 Execution | P3 Review | P4 Publication | P5 Close-Out]

## Test File

**Path:** `[relative path to test file]`
**Language:** [Python | JavaScript | Other]
**Re-execution command:** `[exact command used to re-execute]`

## Results

**Passed:** [N]
**Failed:** [M]
**Skipped:** [K]
**Total:** [N+M+K]

**PASS/FAIL:** [PASS (zero failures) | FAIL ([M] failures)]

## Output Captured

```
[Paste full test output here, or reference output file path]
```

## Failed Tests (if any)

| Test Name | Expected | Actual | Error Message |
|:----------|:---------|:-------|:--------------|
| [name] | [expected] | [actual] | [error] |

## Root Cause Analysis (if failures exist)

[Why did these tests fail? What changed?]

## Fixes Applied

| Test | Fix | Re-executed? |
|:-----|:----|:-------------|
| [name] | [what was changed] | [Yes — now passes | No — deferred with rationale] |

## Iteration Count

**Rounds of test → fix → retest:** [N]
**Current state:** [All passing | [M] failures remain — deferred with rationale]

---

## Audit Trail

| Check | Status |
|:------|:-------|
| Test file exists on disk (Test-Path) | [✓] |
| Re-executed in this session | [✓] |
| Output captured and saved | [✓] |
| Zero failures OR failures documented with rationale | [✓] |
| Evidence file committed | [✓] |

---

*Generated from TEST-EVIDENCE-TEMPLATE.md v1.0. File as `test-evidence-[date]-[suite-name].md` in project directory.*
