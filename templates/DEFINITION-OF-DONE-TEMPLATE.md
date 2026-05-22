---
template: DEFINITION-OF-DONE
version: "1.0"
---

# Definition of Done — [PROJECT NAME]

A task is NOT complete until ALL applicable criteria are met. DoD is verified by the human orchestrator per the Force-Multiplier Protocol, not self-assessed by the agent.

## CODE TASK

- [ ] File passes pre-execution Unicode safety scan (Rule 12)
- [ ] File executes without errors on first run
- [ ] Output verified against expected results
- [ ] No `python -c` used (Rule 13: HARD BLOCK)
- [ ] File committed with format: `ACTION:[CREATE|EDIT] FILE: path RATIONALE:reason`
- [ ] `git log -1 --oneline` confirms commit exists

## DOCUMENT TASK

- [ ] Document passes Publication Language Gate (§11.7) — zero internal project language
- [ ] Curly quotes throughout body text (Python scan confirmation)
- [ ] YAML frontmatter present and valid
- [ ] File committed with format
- [ ] If replacing prior version: old version deleted per File Replacement Protocol (§10.5)

## PUBLICATION TASK

- [ ] Publication Language Gate (§11.7): zero internal language hits
- [ ] Standalone Publication Requirement (§11.8): zero project references
- [ ] Reader testing: 2 rounds minimum, no truncation gaps (§3.1)
- [ ] Curly quotes, YAML, author block per §11
- [ ] `[DOI-PENDING]` replaced with actual DOI
- [ ] Copy to `G:\My Drive\Obsidian\releases\YYYY\MM\` verified with Test-Path
- [ ] Human review (G4) completed
- [ ] File committed

## ANALYSIS TASK

- [ ] All quantitative claims verified via Python (re-executed, output matches)
- [ ] All citations traceable to source files or labeled `[UNVERIFIED-LLM]`
- [ ] Limit checks performed on derivations
- [ ] Web-retrieved claims verified per §0.8.6 Web Research Protocol
- [ ] Results saved in structured format (JSON/CSV)

## WEB APP TASK

- [ ] All interactive features verified working — click every button, test every input, confirm every mode
- [ ] Error states handled: empty config, broken JSON, missing DOM elements show user-facing messages (not console errors)
- [ ] Cross-browser screenshots captured: Chrome + Firefox (minimum)
- [ ] Console audit: zero unexpected errors on page load and during ALL interaction paths
- [ ] Mobile responsiveness check OR explicit "desktop-only" declaration visible in UI
- [ ] Accessibility baseline: color contrast ratios pass WCAG AA, keyboard-navigable, alt text on key visuals
- [ ] All assets load from live URL (zero 404s on JS/CSS/images — verify with browser network tab)
- [ ] `<title>`, `<meta description>`, and Open Graph tags present in `<head>`
- [ ] `.nojekyll` file present at root (GitHub Pages requirement)
- [ ] Test suite executed with zero failures — verified by re-execution, NOT by checking file existence
- [ ] LEARNINGS.md updated with any issues found during testing
- [ ] BACKLOG.md: all P1 items triaged (complete, migrate to next sprint, or explicitly defer with rationale)
- [ ] File committed with format: `ACTION:[CREATE|EDIT] FILE: path RATIONALE:reason`
- [ ] `git log -1 --oneline` confirms commit exists

---
*Generated from DEFINITION-OF-DONE-TEMPLATE.md v1.0*
