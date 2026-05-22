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

### P2 (Medium Priority)

| # | Item | Description | Effort | Status |
|:--|:-----|:-----------|:-------|:-------|
| P5 | **Update system_audit.py Part A3 — exclude known .git contamination** | Two projects (ultrametric-game-of-life, polysynthetic-communication) have .git dirs in projects tree — by design for GitHub Pages deployment. Audit should exclude these known repos. | 0.25h | [ ] |
| P6 | **Add template invocation audit to system_audit.py** | Beyond Part F's text-search (is template name present), add a check that calls fill_prompt_template for each template and verifies non-empty output | 0.5h | [ ] |
| P7 | **Retrofit archived projects with template-conformant docs** | Per CPL L21: audit recently archived projects and retrofit template-conformant documentation (CHARTER.md, DEFINITION-OF-DONE.md, RISK-REGISTER.md) where valuable | 2h | [ ] |

### P3 (Nice-to-Have)

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
| **No app-level testing** | Only `test_tree.py` exists (12 tree construction cases). Zero tests for JS functionality, UI interaction, error handling, edge cases | App could be broken in browser without detection |
| **LEARNINGS.md empty** | File says "Lessons will be added as the project executes." — never populated | No kaizen captured for future projects |
| **P2/P3 backlog skipped** | 6 P2 items (live index display, pre-loaded data, export, depth chart, animation, multi-prime) and 6 P3 items (mobile, accessibility, tutorial, URL sharing, data pre-load, publication link) all unaddressed | App lacks features that make it usable by target audience |
| **No UI/UX review** | No reader testing on the deployed app experience | Usability issues undetected |
| **No deployment verification** | No documented check that live URL works after push | Could deploy broken assets |
| **No DEFINITION-OF-DONE for web apps** | DoD template has CODE/DOC/PUBLICATION/ANALYSIS — no WEB APP category | No standard for when a web app is "done" |

### P1 (High Priority — Next Sprint)

| # | Item | Description | Project | Effort |
|:--|:-----|:-----------|:--------|:-------|
| W1 | **Game of Life: Complete P2 backlog items** | Ultrametricity index live display, pre-loaded comparison data, export/import JSON, depth vs LER interactive chart, propagation animation, multi-prime comparison (p=2,3,5) | ultrametric-game-of-life | 4h |
| W2 | **Game of Life: Testing & hardening** | Functional test plan for all JS modules (virtual-qubit-engine, dual-viz, showdown-main), error state handling (empty config, broken JSON, missing DOM elements), cross-browser screenshots, console error audit | ultrametric-game-of-life | 3h |
| W3 | **Game of Life: Populate LEARNINGS.md** | Capture all issues found during W2 testing, CPL promotion candidates, design decisions made during hardening | ultrametric-game-of-life | 0.5h |
| W4 | **Polysynthetic: Interactive Semantic Graph Explorer** | Web app demo: visualize morphemic trees as ultrametric trees. Interactive: user clicks morpheme nodes, sees ultrametric distance metrics, cross-linguistic comparison. P2 item from BACKLOG: "Visual diagrams: morphemic tree vs. ultrametric tree isomorphism" | polysynthetic-communication | 6h |
| W5 | **Polysynthetic: Cross-Linguistic Comparison Table (interactive)** | Web app: filterable, sortable comparison of isolating vs. agglutinative vs. polysynthetic chunking strategies with live examples. P2 item from BACKLOG | polysynthetic-communication | 3h |

### P2 (Medium Priority)

| # | Item | Description | Project | Effort |
|:--|:-----|:-----------|:--------|:-------|
| W6 | **Game of Life: P3 backlog completion** | Mobile touch support, color-blind accessible palette, tutorial/guided tour overlay, share state via URL hash, pre-loaded data scatter plot, publication link | ultrametric-game-of-life | 3h |
| W7 | **Polysynthetic: Semantic Graph Search Prototype** | Web app: cross-linguistic semantic graph search concept demo. P2 item from BACKLOG: "Prototype query: cross-linguistic semantic graph search concept" | polysynthetic-communication | 4h |
| W8 | **QWAV Simulation Code: Web Demo** | P28 repo has GitHub Pages config. Build an interactive web demo for the open-source simulation code showcasing ultrametric computational geometry | QWAV (P28) | 4h |

### P3 (Nice-to-Have)

| # | Item | Description | Project | Effort |
|:--|:-----|:-----------|:--------|:-------|
| W9 | **Game of Life: CI/CD for GitHub Pages** | GitHub Actions workflow: lint JS, run test suite, deploy to Pages on merge to main. Prevents deploying broken code | ultrametric-game-of-life | 1h |
| W10 | **Polysynthetic: Phylogenetic Tree Cross-Reference** | Interactive D3 visualization overlaying linguistic phylogeny with ultrametric tree structure. P3 item from BACKLOG | polysynthetic-communication | 4h |

---

## 🔴 PROCEDURE IMPROVEMENTS — Web App Release Quality Gates

### Root Cause Analysis: Why Was Game of Life Released Half-Baked?

1. **No WEB APP category in DEFINITION-OF-DONE-TEMPLATE** — The DoD template has CODE, DOCUMENT, PUBLICATION, and ANALYSIS sections. Web apps don't fit any of these. The agent had no standard for when a web app was "done."

2. **No pre-deployment checklist** — The §12 close-out procedure is designed for research papers, not interactive web apps. No gate required: "does the live URL work?"

3. **No post-deployment verification** — After pushing to GitHub Pages, no protocol required visiting the live URL and testing.

4. **Empty LEARNINGS.md** — The kaizen engine was never engaged. Issues were never captured, so they can't be prevented in future projects.

5. **P2/P3 items treated as optional** — The agent treated "P2 = could have later" as "P2 = don't need to do." No gate required backlog triage before release.

### Required Additions (tracked as P2-P4 in META backlog above)

| # | Addition | Where | Prevents |
|:--|:---------|:------|:---------|
| **DoD: WEB APP** | New section in DEFINITION-OF-DONE-TEMPLATE | `templates/DEFINITION-OF-DONE-TEMPLATE.md` | Apps deployed without functional verification |
| **Release Checklist** | New WEB-APP-RELEASE-CHECKLIST template | `templates/WEB-APP-RELEASE-CHECKLIST.md` | Skipping pre-deployment gates |
| **Wiring** | Wire into DEFAULT.md close-out and QWAV initiation | `DEFAULT.md`, `QWAV-DEFAULT.md` | Templates exist but unused (same pattern we just fixed) |

### Proposed WEB APP Definition of Done

```
## WEB APP TASK

- [ ] All interactive features verified by human-in-the-loop (click every button, test every input)
- [ ] Error states handled: empty config, broken JSON, missing DOM elements show user-facing messages (not console errors)
- [ ] Cross-browser screenshots: Chrome + Firefox (minimum)
- [ ] Console audit: zero unexpected errors on page load and during interaction
- [ ] Mobile responsiveness check OR explicit "desktop-only" declaration in UI
- [ ] Accessibility baseline: color contrast ratios pass, keyboard-navigable, alt text on key visuals
- [ ] All assets load from live URL (zero 404s on JS/CSS/images)
- [ ] `<title>`, `<meta description>`, and Open Graph tags present
- [ ] `.nojekyll` file present (GitHub Pages requirement)
- [ ] LEARNINGS.md updated with any issues found during testing
- [ ] BACKLOG.md: all P1 items triaged (complete, migrate, or explicitly defer with rationale)
```

---

## Legend

| Domain | Color | Scope |
|:-------|:------|:------|
| 🟡 META | Yellow | Prompt engineering, templates, agent config (Prompts workspace) |
| 🟣 SPINOFF | Purple | Delegated to Projects agent — web app demos, POCs |
| 🔴 PROCEDURE | Red | Cross-cutting quality improvements |

---

*Generated from PRODUCT-BACKLOG-TEMPLATE.md v1.0*
