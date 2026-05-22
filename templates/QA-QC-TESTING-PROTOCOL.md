---
template: QA-QC-TESTING-PROTOCOL
version: "1.0"
---

# QA/QC Testing Protocol — [PROJECT NAME]

> **Purpose:** Universal quality control framework for ALL deliverable types. Test files existing on disk is NOT the same as tests being executed. This protocol defines what "tested" means for each deliverable type and how to prove it.

## Core Principle: Execution Evidence Over File Existence

```
WRONG: "test_plan.py exists → tests pass"        ← Game of Life failure pattern
RIGHT: "test_plan.py re-executed → 7/7 pass → output saved as evidence"
```

Every test claim must be backed by RE-EXECUTION — not file presence, not memory, not assumption.

---

## Deliverable Type Testing Matrix

### 1. DOCUMENT

| Gate | Requirement | Evidence |
|:-----|:-----------|:---------|
| **Reader Test** | Minimum 2 rounds blind review (CPL L27). Round 1 catches surface; Round 2 catches structure. Use REVIEWER subagent or fresh LLM session. | Reader feedback document + CHANGELOG entry documenting fixes applied |
| **Publication Language** | §11.7 scan — zero internal project language hits | Python scan output |
| **Math Format** | §6 scan — zero bare Unicode math | Python scan output |
| **Quote Type** | Curly quotes throughout (Python scan) | Python scan output |
| **Severity Gate** | All [BLOCKING] and [MAJOR] issues resolved before proceeding | Documented in CHANGELOG |

**Iteration loop:** Test → reader feedback → fix → retest. Repeat until zero [BLOCKING]/[MAJOR] issues.

### 2. CODE

| Gate | Requirement | Evidence |
|:-----|:-----------|:---------|
| **Pre-Execution Scan** | Rule 12: zero non-ASCII in code files | Python scan output |
| **Functional Tests** | All test files executed, all assertions pass | Re-execution output captured as file |
| **Edge Cases** | Empty input, boundary values, error conditions tested | Documented in test output |
| **No `python -c`** | Rule 13: all Python executed from script files | Verify no inline Python in git log |
| **Regression Check** | Re-run ALL test files after any code change | Both old and new test output match or improve |

**Iteration loop:** Test → failure → fix → retest ALL tests. Must return to zero failures before marking complete.

### 3. WEB APP

| Gate | Requirement | Evidence |
|:-----|:-----------|:---------|
| **Functionality** | Every interactive element tested end-to-end | Screenshots of each mode |
| **Error Handling** | Invalid input, missing DOM, CDN failure — all show user-facing messages | Console screenshots (zero unexpected errors) |
| **Cross-Browser** | Chrome + Firefox (minimum) | Screenshots from both browsers |
| **Accessibility** | WCAG AA contrast, keyboard-navigable, alt text | Audit tool output or manual checklist |
| **Asset Loading** | Zero 404s on all JS/CSS/images from live URL | Network tab screenshot |
| **Deployment** | Live URL visited in incognito — all features work | Screenshot of live URL |
| **Test Suite** | All JS tests executed (not just Python algorithm tests) | Test output saved |

**Iteration loop:** Deploy to staging → test all gates → fix → redeploy → retest. Only push to production after all gates pass.

**Pre-deployment gate:** Use `fill_prompt_template("WEB-APP-RELEASE-CHECKLIST")` for the full 9-section checklist.

### 4. ANALYSIS

| Gate | Requirement | Evidence |
|:-----|:-----------|:---------|
| **Quantitative Verification** | All claims re-executed, output matches | Re-execution log with timestamps |
| **Reproducibility** | Same input → same output (seed-controlled where applicable) | Two independent runs compared |
| **Limit Checks** | Boundary conditions, asymptotic behavior verified | Documented in output |
| **Source Traceability** | Every claim traced to [CODE-EXECUTED] or [EXTERNAL-SOURCE] | Audit trail in document |

**Iteration loop:** Re-execute analysis → compare with claimed results → flag discrepancies → fix.

---

## Phase Gate Integration

| Phase | Testing Gate | Action |
|:------|:-------------|:-------|
| **P0 Initiation** | TEST PLAN created | Determine deliverable type, write/identify test files, document test criteria in SPRINT.md |
| **P1 Planning** | TEST CRITERIA defined per task | Each SPRINT task includes: test file path, expected pass criteria, evidence format |
| **P2 Execution** | TEST SUITE EXECUTED | Before marking any file as "done": re-execute tests, capture output, verify zero failures |
| **P3 Review** | FULL QA/QC GATE | All tests for deliverable type re-executed. Evidence captured. Reader testing (2 rounds) for documents. |
| **P4 Publication** | PRE-RELEASE GATE | All P0-P3 gates satisfied. Test evidence audited. Web app: release checklist complete. |
| **P5 Close-Out** | TEST EVIDENCE AUDIT | Verify all test evidence files exist and show zero failures. Document in final audit. |

---

## Test Evidence Standard

Every test execution must produce a test evidence document containing:

```
# Test Evidence — [Test Suite Name]
**Date executed:** [YYYY-MM-DD HH:MM]
**Executed by:** [Agent]
**Test file:** [path]
**Re-execution command:** [exact command used]
**Result:** [N] passed, [M] failed, [K] skipped
**Output captured:** [path to output file or inline]
```

Use `fill_prompt_template("TEST-EVIDENCE-TEMPLATE")` to generate the evidence document.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| "test_plan.py exists → tests pass" | File existence ≠ execution (Game of Life failure) | Re-execute test_plan.py, capture output |
| "I remember the tests passing" | Memory is not evidence (CPL L17) | Re-execute and capture output |
| "The DoD says file executes without errors" | "Executes" ≠ "all assertions pass" | Require test suite output showing zero failures |
| Skipping test evidence because "it's just a small change" | Small changes cause regressions | Always re-execute full test suite |

---

*Generated from QA-QC-TESTING-PROTOCOL.md v1.0*
