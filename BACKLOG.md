# BACKLOG — Prompts Directory (System Prompt Engineering)

> **Purpose:** Prioritized queue of future work for the Prompts agent and cross-cutting system improvements.
> **Last Updated:** 2026-05-22

---

## 🟡 META — Prompt Engineering & Agent Config (Prompts Workspace)

### P0 (Must Do — Current Sprint)

*None — Template Integration Sprint (S0-S7) complete. All 14 PM templates wired.*

### P1 (High Priority — Next Sprint)

| # | Item | Description | Effort | Depends On | Status |
|:--|:-----|:-----------|:-------|:-----------|:-------|
| P1 | **Merge feature/template-integration-audit to main** | Run §9.9 testing before merge: system_audit.py (all parts), Test-Path all 21 templates, verify DEFAULT.md/QWAV-DEFAULT.md cross-references, git log integrity | 0.5h | S0-S7 complete | [ ] |
| P2 | **Add WEB APP DoD section to DEFINITION-OF-DONE-TEMPLATE** | New task type: WEB APP — functionality verification, cross-browser testing, error/edge case handling, mobile responsiveness, accessibility baseline, performance check, asset loading verification | 0.5h | P1 | [ ] |
| P3 | **Create WEB-APP-RELEASE-CHECKLIST template** | Pre-deployment gate: all P0+P1 items complete, LEARNINGS.md populated, reader testing on deployed app, screenshot verification, live URL interaction test, 404 check | 0.5h | P2 | [ ] |
| P4 | **Wire web app templates into agent workflows** | Add WEB APP DoD to DEFAULT.md §0.7, wire WEB-APP-RELEASE-CHECKLIST into DEFAULT.md §12 close-out, update ARCHITECTURE.md Layer 5, update system_audit.py Part F | 0.5h | P2, P3 | [ ] |

### P2 — Universal QA/QC Process Overhaul (Medium Priority)

> **Context:** The Ultrametric Game of Life release exposed a systemic QA/QC gap: `test_plan.py` (12,522 chars, 7 comprehensive test suites) was written to disk but never executed, never mentioned in SPRINT.md, and never verified. The agent claimed "all 22 tasks complete" because test files *existed* — not because tests *passed*. Same pattern could affect any deliverable type.

| # | Item | Description | Effort | Status |
|:--|:-----|:-----------|:-------|:-------|
| **P10** | **Create universal QA/QC Testing Protocol template** | One template covering all deliverable types: DOCUMENT (reader testing per §11.5, minimum 2 rounds, severity classification), CODE (functional tests + edge cases executed and verified), WEB APP (UI/UX, cross-browser, error handling, accessibility, deployment verification), ANALYSIS (quantitative re-execution, reproducibility). Each type has: test plan requirement, execution evidence requirement, pass/fail gate, and iteration loop (test → fix → retest until clean). | 1h | [ ] |
| **P11** | **Wire QA/QC gates into DEFAULT.md phase workflow** | P0: TEST PLAN template created (mandatory). P2: Test suite executed before declaring file "done" (not just "file exists"). P3: Full QA/QC gate — all tests for deliverable type re-executed, evidence captured. P4: Pre-publication gate extended beyond documents to all deliverable types. WHAT'S NEXT? PROCEED: Step 2.5 added — "Verify test evidence exists for all completed tasks. If test files exist but were never executed, mark task as [~] in-progress and re-execute tests." | 1h | [ ] |
| **P12** | **Add test evidence requirement to SPRINT task format** | SPRINT.md task completion verification must distinguish "wrote test file" from "executed test suite." New format: `Test-Path test_file.py + re-executed: [N] passed, [0] failed`. Phase workflow must gate on evidence, not file existence. | 0.5h | [ ] |
| **P13** | **Update DEFINITION-OF-DONE-TEMPLATE with test execution gates** | Add 3 new task types: CODE TEST (test suite executed with zero failures, edge cases covered, output verified, results saved), WEB APP (functionality, cross-browser, error handling, accessibility, deployment verified, LEARNINGS.md populated), ANALYSIS TEST (quantitative claims re-executed, reproducibility confirmed, limits checked). DOCUMENT task: add reader testing requirement (not just for publications). | 0.5h | [ ] |
| **P14** | **Add testing gate to WHAT'S NEXT? PROCEED** | After Step 2 (Identify Next Task), insert Step 2.5: "Audit completed tasks for test evidence. For any task where a test file exists but was never executed, re-execute the test suite BEFORE proceeding. If tests fail, surface failures to user instead of marking task complete." Prevents the test_plan.py ghost pattern. | 0.5h | [ ] |
| **P15** | **Create TEST-EVIDENCE-TEMPLATE** | Standardized test evidence document: test file path, re-execution command, output captured, pass/fail count, date executed, agent that executed it. Appended to project directory as test evidence. | 0.25h | [ ] |

### P3 — Cross-Cutting Improvements (Medium Priority)

| # | Item | Description | Effort | Status |
|:--|:-----|:-----------|:-------|:-------|
| P5 | **Update system_audit.py Part A3 — exclude known .git contamination** | Two projects (ultrametric-game-of-life, polysynthetic-communication) have .git dirs in projects tree — by design for GitHub Pages deployment. Audit should exclude these known repos. | 0.25h | [ ] |
| P6 | **Add template invocation audit to system_audit.py** | Beyond Part F's text-search (is template name present), add a check that calls fill_prompt_template for each template and verifies non-empty output | 0.5h | [ ] |
| P7 | **Retrofit archived projects with template-conformant docs** | Per CPL L21: audit recently archived projects and retrofit template-conformant documentation (CHARTER.md, DEFINITION-OF-DONE.md, RISK-REGISTER.md) where valuable | 2h | [ ] |

### P4 — Nice-to-Have

| # | Item | Description | Effort | Status |
|:--|:-----|:-----------|:-------|:-------|
| P8 | **Template parameter discovery** | Some PM templates return empty parameters from get_prompt_template_parameters. Consider whether formal parameters (project name, date) would improve utility vs inline placeholders | 0.5h | [ ] |
| P9 | **CPL risk audit for RISK-REGISTER-TEMPLATE** | Verify pre-populated CPL risks (L7, L3/L6, L18/L40, L14, L39, L19) are current and complete against all 40 CPL lessons | 0.5h | [ ] |

---

## 🟣 SPINOFF — Web App Demos & POCs for GitHub Pages

### CRITICAL CONTEXT — Ultrametric Game of Life Post-Mortem

The **Virtual Qubit Showdown** (`qnfo.github.io/ultrametric-game-of-life`) was deployed to GitHub Pages with all 22 SPRINT tasks marked complete, but the release was **half-baked**:

| Gap | Evidence | Impact |
|:----|:---------|:-------|
| **No app-level testing** | Only `test_tree.py` exists (12 construction cases). `test_plan.py` (12,522 chars, 7 test suites) was written to disk but NEVER EXECUTED — not tracked in SPRINT, not mentioned in CHANGELOG, no output captured. | Comprehensive test suite is a ghost file |
| **No test execution verification** | Agent distinguished "wrote test file" from "executed test suite" — the system has no mechanism to enforce the difference | Pattern could repeat in any project |
| **LEARNINGS.md empty** | File says "Lessons will be added as the project executes." — never populated | No kaizen captured |
| **P2/P3 backlog skipped** | 6 P2 items + 6 P3 items all unaddressed | App lacks features needed by target audience |
| **No UI/UX review** | No reader testing on deployed app experience | Usability issues undetected |
| **No deployment verification** | No documented check that live URL works after push | Could deploy broken assets |
| **No DEFINITION-OF-DONE for web apps** | DoD template has CODE/DOC/PUBLICATION/ANALYSIS — no WEB APP category | No standard for when a web app is "done" |

### P1 (High Priority — Next Sprint)

| # | Item | Description | Project | Effort |
|:--|:-----|:-----------|:--------|:-------|
| W1 | **Game of Life: Execute test_plan.py + fix failures** | Run the comprehensive 7-test suite. Address any failures. Save output as test evidence. This is the single highest-impact fix — the test suite already exists but was never run. | ultrametric-game-of-life | 1h |
| W2 | **Game of Life: Complete P2 backlog items** | Ultrametricity index live display, pre-loaded comparison data, export/import JSON, depth vs LER interactive chart, propagation animation, multi-prime comparison (p=2,3,5) | ultrametric-game-of-life | 4h |
| W3 | **Game of Life: UI/UX testing & hardening** | Cross-browser screenshots (Chrome + Firefox), console error audit, error state handling (empty config, broken JSON, missing DOM), populate LEARNINGS.md | ultrametric-game-of-life | 2h |
| W4 | **Polysynthetic: Interactive Semantic Graph Explorer** | Web app: visualize morphemic trees as ultrametric trees. Click nodes → ultrametric distance metrics, cross-linguistic comparison. P2 backlog item. | polysynthetic-communication | 6h |
| W5 | **Polysynthetic: Cross-Linguistic Comparison Table (interactive)** | Web app: filterable, sortable comparison of isolating vs. agglutinative vs. polysynthetic chunking strategies with live examples. P2 backlog item. | polysynthetic-communication | 3h |

### P2 (Medium Priority)

| # | Item | Description | Project | Effort |
|:--|:-----|:-----------|:--------|:-------|
| W6 | **Game of Life: P3 backlog completion** | Mobile touch support, color-blind accessible palette, tutorial/guided tour overlay, share state via URL hash, pre-loaded data scatter plot, publication link | ultrametric-game-of-life | 3h |
| W7 | **Polysynthetic: Semantic Graph Search Prototype** | Web app: cross-linguistic semantic graph search concept demo. P2 backlog item. | polysynthetic-communication | 4h |
| W8 | **QWAV Simulation Code: Web Demo** | P28 repo has GitHub Pages config. Build interactive web demo for open-source simulation code. | QWAV (P28) | 4h |

### P3 (Nice-to-Have)

| # | Item | Description | Project | Effort |
|:--|:-----|:-----------|:--------|:-------|
| W9 | **Game of Life: CI/CD for GitHub Pages** | GitHub Actions: lint JS, run test suite, deploy to Pages on merge to main. | ultrametric-game-of-life | 1h |
| W10 | **Polysynthetic: Phylogenetic Tree Cross-Reference** | Interactive D3 visualization overlaying linguistic phylogeny with ultrametric tree structure. P3 backlog item. | polysynthetic-communication | 4h |

---

## 🔴 CROSS-CUTTING — QA/QC Process That Failed & What Must Change

### The Test Evidence Gap — Universal Pattern

```
1. Agent writes test file to disk                    ← "task complete"
2. Test file sits unexecuted                         ← CPL L18: write ≠ verified
3. SPRINT.md tracks file existence, not execution    ← no differentiation
4. Phase gates don't check test execution            ← P3 only checks "reader testing"
5. WHAT'S NEXT? PROCEED marks task complete          ← never verifies tests passed
6. LEARNINGS.md stays empty                          ← no failures to learn from
7. Half-baked release                                ← inevitable
```

### Required Testing By Deliverable Type

| Deliverable Type | Testing Required | Current State | Gap |
|:-----------------|:-----------------|:--------------|:----|
| **DOCUMENT** | Reader testing: 2 rounds min, severity classification, fixes applied | §11.5 exists but gated to "Publication Documents" only | Extend to ALL documents (not just publications) |
| **CODE** | Functional tests + edge cases executed, results captured, regression-free | DoD has "file executes without errors on first run" — no test suite check | Add test suite execution gate: "All test files executed with zero failures — verified by re-execution" |
| **WEB APP** | UI/UX, cross-browser, error handling, accessibility, deployment verification, LEARNINGS.md populated | No DoD section exists | Add WEB APP DoD section (P2) |
| **ANALYSIS** | Quantitative claims re-executed, reproducibility confirmed, limits checked | DoD covers individual claim verification but not test suite execution | Add ANALYSIS TEST section requiring test suite re-execution |
| **PUBLICATION** | Reader testing (already covered) + all underlying deliverable testing complete | §11.5 is solid | Ensure upstream testing gates are satisfied before publication gate |

### Phase Gate Integration

| Phase | Current Testing Gate | What's Missing |
|:------|:---------------------|:---------------|
| **P0 Initiation** | 7 mandatory docs exist | No TEST PLAN requirement — should require a test plan for the deliverable type |
| **P1 Planning** | Detailed SPRINT with tasks | Tasks don't include test criteria — should require test criteria per task |
| **P2 Execution** | Versioned output files committed | No test execution gate — should verify test suite executed, evidence saved |
| **P3 Review** | Reader testing (documents only) | No code/web app testing — should be the universal QA/QC gate for all deliverable types |
| **P4 Publication** | Publication-ready document | No testing gate for code/web app releases — should require test evidence before any release |
| **P5 Close-Out** | Final checklist | No test evidence audit — should verify all test suites executed and passing |

---

## Legend

| Domain | Color | Scope |
|:-------|:------|:------|
| 🟡 META | Yellow | Prompt engineering, templates, agent config (Prompts workspace) |
| 🟣 SPINOFF | Purple | Delegated to Projects agent — web app demos, POCs |
| 🔴 CROSS-CUTTING | Red | Systemic QA/QC process improvements |

---

*Generated from PRODUCT-BACKLOG-TEMPLATE.md v1.0*
