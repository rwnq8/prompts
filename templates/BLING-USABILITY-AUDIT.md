---
template: BLING-USABILITY-AUDIT
version: "1.1"
description: Structured usability audit for UI changes — combines functional BLIND testing with visual BLING (polish/aesthetics) review AND Discovery Momentum (graph visibility & traversability). Answers the four core questions: what's working, what's not, what needs fixing, what can be improved.
---

# BLING Usability Audit — [PROJECT/COMPONENT NAME]

> **BLING = BLIND Usability + Visual Polish.** Every UI change must pass both dimensions before being declared DONE.

---

## AUDIT DIMENSIONS

| Dimension | Focus | Key Question |
|:----------|:------|:-------------|
| **BLIND** | Functional usability | Can users accomplish their tasks without friction? |
| **BLING** | Visual polish & aesthetics | Does the UI look distinctive, polished, and high-quality? |

---

## THE 4 CORE QUESTIONS

For every UI element, screen, component, and interaction flow under review, answer ALL four:

### 1. WHAT'S WORKING? ✅

Identify what functions correctly and what visual elements are effective.

- [ ] Which interactions are smooth, intuitive, and error-free?
- [ ] Which visual elements are polished and visually effective?
- [ ] Which flows complete successfully without friction?
- [ ] Which design decisions are working well? (cite specific elements)

### 2. WHAT'S NOT WORKING? ❌

Identify broken functionality and visual defects.

- [ ] Which interactions fail, error, or produce unexpected results?
- [ ] Which visual elements are broken, missing, or incorrectly rendered?
- [ ] Which flows dead-end or cannot be completed?
- [ ] Which UI states cause confusion or errors?

### 3. WHAT NEEDS TO BE FIXED? 🔧

Prioritize blocking and major issues. These MUST be resolved.

- [ ] **BLOCKING:** Issues that prevent task completion or cause data loss
- [ ] **MAJOR:** Functional bugs, accessibility violations, broken responsive layouts
- [ ] **MINOR:** Visual defects — misalignment, clipping, wrong colors, typography issues

### 4. WHAT CAN BE IMPROVED/ENHANCED? ⬆️

Non-blocking opportunities for polish and refinement.

- [ ] Visual polish — animations, transitions, micro-interactions
- [ ] UX flow — reduce clicks, improve information hierarchy
- [ ] Performance — loading states, perceived speed
- [ ] Accessibility — go beyond baseline compliance
- [ ] Distinctiveness — make the UI memorable, not generic

---

## FUNCTIONAL UI TESTING CHECKLIST

### Core Interactions

- [ ] All buttons, links, and interactive elements respond to click/tap
- [ ] Forms submit correctly with valid data
- [ ] Form validation errors display clearly and helpfully
- [ ] Navigation (menus, tabs, breadcrumbs) works correctly
- [ ] Search/filter functionality returns expected results
- [ ] Data displays correctly (tables, lists, cards, charts)

### State Handling

- [ ] **Loading states:** Spinners, skeletons, or progress indicators appear
- [ ] **Empty states:** Helpful messages appear when no data exists
- [ ] **Error states:** Clear error messages with recovery actions
- [ ] **Edge cases:** Zero results, very long text, special characters
- [ ] **Timeout/network failure:** Graceful degradation, not white screen

### Responsive & Cross-Platform

- [ ] Desktop (1920px, 1440px, 1024px): Layout is correct
- [ ] Tablet (768px): Layout adapts appropriately
- [ ] Mobile (375px, 414px): All functions accessible
- [ ] Touch targets are minimum 44x44px on mobile

### Accessibility Baseline

- [ ] Keyboard navigation: Tab order is logical, focus indicators visible
- [ ] Screen reader: All interactive elements have accessible names
- [ ] Color contrast: Text meets WCAG AA (4.5:1 normal, 3:1 large)
- [ ] Form inputs have associated labels
- [ ] Images have alt text (or marked decorative)

---

## BLING — VISUAL POLISH AUDIT CHECKLIST

### Typography

- [ ] Font hierarchy is clear (headings > subheadings > body > captions)
- [ ] Line height is comfortable for reading (1.5-1.75 for body text)
- [ ] Font sizes are consistent across similar elements
- [ ] No more than 2-3 font families in use
- [ ] Web fonts load without layout shift (FOUT/FOIT handled)

### Color & Contrast

- [ ] Color palette is harmonious and consistent
- [ ] Primary, secondary, accent, neutral colors are clearly defined
- [ ] Text/background contrast passes WCAG AA
- [ ] Color is not the ONLY indicator of state (add icons/text)
- [ ] Dark mode: All elements visible, no hard-coded white backgrounds

### Layout & Spacing

- [ ] Consistent spacing scale (4px/8px base grid)
- [ ] No elements touching edges without intentional padding
- [ ] Related elements are grouped with proximity
- [ ] No orphaned or floating elements
- [ ] Content max-width is constrained for readability (~65ch for text)

### Animation & Motion

- [ ] Transitions are smooth (200-300ms duration)
- [ ] No jarring jumps or layout shifts during interaction
- [ ] Hover states provide clear visual feedback
- [ ] Loading animations are subtle, not distracting
- [ ] Respects `prefers-reduced-motion` media query

### Iconography & Imagery

- [ ] Icons are consistent in style (same weight, same library)
- [ ] Icons have clear, recognizable meanings
- [ ] Images are optimized (appropriate resolution, modern format)
- [ ] No pixelated or stretched images
- [ ] Placeholder/fallback states for images that fail to load

### Micro-Copy & Messaging

- [ ] Button labels are action-oriented and clear ("Save changes" not "Submit")
- [ ] Error messages explain what happened AND how to fix it
- [ ] Empty states are helpful, not just "No results"
- [ ] Tooltips provide useful context, not redundant information
- [ ] Confirmation messages confirm what just happened

### Brand Distinctiveness

- [ ] UI has a distinctive visual identity (not a generic template)
- [ ] Visual design is memorable and intentional
- [ ] Consistent use of brand colors, typography, and tone
- [ ] No uncanny-valley or "obviously AI-generated" feel
- [ ] Design feels crafted, not assembled from defaults

### Discovery Momentum — Graph Visibility & Traversability

Does the interface reveal the *shape* of knowledge and let users walk through it? Based on the 8 design principles from `research/discovery-momentum-knowledge-platforms.md`:

- [ ] **Every item is a node:** Are all linkable entities (pages, concepts, people, citations) addressable with unique IDs? Or are some invisible to the graph?
- [ ] **Links are bidirectional:** When A links to B, does B show a backlink to A? Are backlinks prominent in the UI?
- [ ] **Graph surfaced progressively:**
  - Level 1: Inline links and hover previews present?
  - Level 2: Sidebar with linked/unlinked references?
  - Level 3: Localized graph view (first-degree neighbors)?
  - Level 4: Global explorable graph with filtering and zoom?
- [ ] **Multiple link types:** Beyond the generic hyperlink, are there typed edges (cites, contradicts, extends, illustrates, is-example-of)?
- [ ] **Serendipity optimization:** Does the interface balance high-relevance adjacent nodes with some "long jumps" to different clusters? Is there a "random walk" or "explore" path?
- [ ] **Context preservation:** Does navigation preserve spatial continuity (zoom-in on canvas), temporal continuity (breadcrumbs), or a "stack" of open cards? Or does it break the frame with every click?
- [ ] **User-shaped graph:** Can users add links, create new nodes, group into collections, or draw connections? Or is the graph read-only?
- [ ] **Graph as first-class UI element:** Is the graph a live minimap, a "nearby" panel, or an interactive visualization? Or is the graph hidden behind a settings page?
- [ ] **Discovery momentum loop:** Does the interface generate a tight loop of: recognition of relevance -> low-cost navigation -> new context with fresh adjacent cues? Test: land with a question — does the interface surface 2+ adjacent nodes you want to click before finishing the current page?

---

## FINDINGS REGISTER

| # | Screen/Element | Status | Severity | Category | Finding |
|:-:|:--------------|:------:|:--------:|:--------:|:--------|
| 1 | | ✅❌🔧⬆️ | BLOCKING/MAJOR/MINOR/ENHANCEMENT | Functional/Visual/Accessibility/UX/Discovery | |

---

## AUDIT SUMMARY

- **Total findings:** {{total}}
- **BLOCKING:** {{blocking_count}} — must fix before release
- **MAJOR:** {{major_count}} — should fix before release
- **MINOR:** {{minor_count}} — fix when possible
- **ENHANCEMENT:** {{enhancement_count}} — polish opportunities

### Verdict

- [ ] **PASS** — All BLOCKING and MAJOR issues resolved. Ready for release.
- [ ] **CONDITIONAL PASS** — MAJOR issues remain but do not block release. Documented in known issues.
- [ ] **FAIL** — BLOCKING issues remain. NOT ready for release.

---

## AUDIT EVIDENCE

- **Screenshots captured:** {{screenshot_count}}
- **Test user paths exercised:** {{path_count}}
- **Browser/device matrix tested:** {{browser_list}}
- **Audit date:** {{audit_date}}
- **Auditor:** {{auditor}}

---

*BLING Usability Audit v1.1 — BLIND functional testing + BLING visual polish + Discovery Momentum (graph visibility & traversability). Every UI change must pass all three dimensions.*
