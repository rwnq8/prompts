---
template: WEB-APP-RELEASE-CHECKLIST
version: "1.0"
---

# WEB APP RELEASE CHECKLIST — [PROJECT NAME]

**App URL:** [GitHub Pages URL]
**Date:** [YYYY-MM-DD]
**Release Version:** [vX.Y]

> **GATE:** This checklist MUST be completed before pushing to GitHub Pages. Items marked `[!]` indicate a blocker that prevents deployment.

## Pre-Deployment Verification

### 1. FUNCTIONALITY — All Features Working
- [ ] Every interactive element tested: buttons, inputs, dropdowns, sliders, mode selectors
- [ ] All 3 modes (or equivalent) function end-to-end: manual interaction, single trial, experiment run
- [ ] Data loading verified — embedded JSON, CDN dependencies, external resources
- [ ] State transitions work: start → interact → complete → reset → start again

### 2. ERROR HANDLING — Nothing Crashes
- [ ] Empty/invalid input shows user-facing message (not console error)
- [ ] Missing DOM elements handled gracefully (no `Cannot read property of null`)
- [ ] JSON parse failures caught with fallback
- [ ] CDN resource failure shows visible error indicator

### 3. CROSS-BROWSER — Screenshots Captured
- [ ] Chrome: screenshot captured — all features working
- [ ] Firefox: screenshot captured — all features working
- [ ] Console in BOTH browsers: zero unexpected errors
- [ ] Screenshots saved to project directory as release evidence

### 4. RESPONSIVENESS & ACCESSIBILITY
- [ ] App functions on viewport widths 1024px+ OR desktop-only declared in UI
- [ ] Color contrast ratios pass WCAG AA (use browser contrast checker)
- [ ] All interactive elements keyboard-navigable (Tab, Enter, Escape)
- [ ] Key visuals have alt text or are labeled as decorative

### 5. DEPLOYMENT ASSETS — Nothing Broken
- [ ] All CSS files load (check network tab — zero 404s)
- [ ] All JS files load (check network tab — zero 404s)
- [ ] CDN dependencies resolve (D3.js, fonts if any)
- [ ] `<title>` tag present and descriptive
- [ ] `<meta name="description">` tag present and accurate
- [ ] Open Graph tags present (`og:title`, `og:description`, `og:image` if applicable)
- [ ] `.nojekyll` file exists at repo root

### 6. TEST EXECUTION
- [ ] Test suite re-executed immediately before deployment
- [ ] Results: `{{count}} passed, [0] failed, {{m}} skipped`
- [ ] Test output saved to project directory as evidence
- [ ] Any pre-existing failures documented with rationale

### 7. DOCUMENTATION — Everything Up to Date
- [ ] LEARNINGS.md updated with issues found during testing
- [ ] BACKLOG.md: all P1 items triaged
- [ ] CHANGELOG.md entry added for this release
- [ ] PROJECT STATE.md updated with release version

## Deployment

### 8. PUSH & VERIFY
- [ ] Code pushed to GitHub (`git push origin main`)
- [ ] GitHub Pages build succeeded (check Actions tab or Pages settings)
- [ ] Live URL visited in incognito/private window
- [ ] All features tested on live URL (not localhost)
- [ ] Screenshot of live URL captured as deployment evidence

## Post-Deployment

### 9. USER COMMUNICATION
- [ ] Release announced via appropriate channel (social media, README update, CHANGELOG)
- [ ] Known limitations documented in README or release notes

## Sign-Off
- [ ] All pre-deployment items [x] — zero blockers
- [ ] Live URL verified working
- [ ] Deployment evidence saved

---
*Generated from WEB-APP-RELEASE-CHECKLIST.md v1.0. File as `RELEASE-CHECKLIST-[version].md` in project directory.*
