---
template: DEFINITION-OF-DONE
version: "2.0"
---

# Definition of Done — [PROJECT NAME]

A task is NOT complete until ALL applicable criteria are met. DoD is verified by the human orchestrator per the Force-Multiplier Protocol, not self-assessed by the agent.

## ⚠️ UNIVERSAL GATES — Apply to ALL Task Types (NON-NEGOTIABLE)

These gates apply regardless of task type. No exemption. Every `[x]` must reference evidence committed to the repository.

- [ ] **TEST PLAN EXECUTED** — Minimum: (a) test file(s) exist and are committed, (b) tests were actually executed (re-run to verify — NOT "I remember running them"), (c) output/log is committed to repo, (d) pass/fail accounting is honest (document what failed, don't hide it). "Tested manually" without a committed test file/script = NOT DONE. "Verified live URL" is a smoke test, not a test plan.
- [ ] **FILESYSTEM VERIFICATION** — Every file claimed as created/modified/deleted passes `Test-Path` verification (or absence verification for deletes). Tool success messages are NOT verification (CPL L15, L18).
- [ ] **GIT VERIFICATION** — Every commit claimed passes `git log -1 --oneline` confirmation. Never claim a commit from memory (CPL L13).
- [ ] **PLAN-EXECUTE-AUDIT CYCLE COMPLETE** — Every planned item was actually executed and audited before declaring DONE. "Planned but not executed" items are NOT DONE. Planning language ("let me fix X", "I will do Y") without corresponding write/exec/git tool invocation does not count as execution. If you cannot produce `Test-Path` or `git log` evidence for a claimed action, it was NOT executed.

- [ ] **NO CHECKBOX THEATER** — If you mark `[x]` but didn't execute the verification, you are falsifying the DoD. Leave `[ ]` and document the gap honestly. Every `[x]` must trace to evidence on disk.

⚠️ **ANTI-PATTERN (CPL L41/L45):** Marking all checkboxes `[x]` with "ALL criteria met. Project is DONE" when no test files exist and no tests were executed. This is checkbox theater. If evidence doesn't exist on disk, the checkbox stays empty.

---

## CODE TASK

- [ ] File passes pre-execution Unicode safety scan (Rule 12)
- [ ] File executes without errors on first run
- [ ] Output verified against expected results
- [ ] No `python -c` used (Rule 13: HARD BLOCK)
- [ ] File committed with format: `ACTION:[CREATE|EDIT] FILE: path RATIONALE:reason`
- [ ] `git log -1 --oneline` confirms commit exists
- [ ] UNIVERSAL GATES above satisfied (test plan executed, filesystem verified, git verified)

## CODE TEST TASK

- [ ] ALL test files for this module executed — verified by re-execution (NOT by checking file existence)
- [ ] Test suite output: {{count}} passed, [0] failed, {{k}} skipped
- [ ] Edge cases covered: empty input, boundary values, error conditions
- [ ] Test evidence saved to project directory as `_test_evidence.md`
- [ ] If any tests failed: root cause documented, fix applied, re-executed to zero failures
- [ ] Regression check: re-ran ALL related test files after fix — no new failures
- [ ] UNIVERSAL GATES above satisfied

## DOCUMENT TASK

- [ ] Document passes Publication Language Gate (§11.7) — zero internal project language
- [ ] Curly quotes throughout body text (Python scan confirmation)
- [ ] YAML frontmatter present and valid
- [ ] Reader testing: minimum 1 round (2 rounds for publication documents per §11.5)
- [ ] All {{blocking_count}} and {{major_count}} reader testing issues resolved
- [ ] File committed with format
- [ ] If replacing prior version: old version deleted per File Replacement Protocol (§10.5)
- [ ] UNIVERSAL GATES above satisfied

## PUBLICATION TASK

- [ ] Publication Language Gate (§11.7): zero internal language hits
- [ ] Standalone Publication Requirement (§11.8): zero project references
- [ ] Reader testing: 2 rounds minimum, no truncation gaps (§3.1)
- [ ] Curly quotes, YAML, author block per §11
- [ ] `[DOI-PENDING]` replaced with actual DOI
- [ ] PDF generated and uploaded to GitHub Release as asset (DEFAULT.md Persistent Preference 12)
- [ ] Release created via `gh release create` with both Markdown source and PDF attached
- [ ] PDF presence verified with `gh release view --json assets`
- [ ] Copy to `GitHub Releases (via gh release create)\YYYY\MM\` verified with Test-Path
- [ ] Human review (G4) completed
- [ ] File committed
- [ ] UNIVERSAL GATES above satisfied

## ANALYSIS TASK

- [ ] All quantitative claims verified via Python (re-executed, output matches)
- [ ] All citations traceable to source files or labeled `[UNVERIFIED-LLM]`
- [ ] Limit checks performed on derivations
- [ ] Web-retrieved claims verified per §0.8.6 Web Research Protocol
- [ ] Results saved in structured format (JSON/CSV)
- [ ] UNIVERSAL GATES above satisfied

## ANALYSIS TEST TASK

- [ ] ALL analysis scripts re-executed — verified output matches claimed results
- [ ] Reproducibility confirmed: same input → same output (seed-controlled)
- [ ] Limit/boundary checks performed and documented
- [ ] Test evidence saved to project directory as `_test_evidence.md`
- [ ] Discrepancies between claimed and re-executed results documented with rationale
- [ ] UNIVERSAL GATES above satisfied

## WEB APP TASK

- [ ] All interactive features verified working — click every button, test every input, confirm every mode
- [ ] Error states handled: empty config, broken JSON, missing DOM elements show user-facing messages (not console errors)
- [ ] Cross-browser screenshots captured: Chrome + Firefox (minimum)
- [ ] Console audit: zero unexpected errors on page load and during ALL interaction paths
- [ ] Mobile responsiveness check OR explicit "desktop-only" declaration visible in UI
- [ ] Accessibility baseline: color contrast ratios pass WCAG AA, keyboard-navigable, alt text on key visuals
- [ ] **Analytics verified active:** For deployed sites, confirm analytics data is flowing — either Cloudflare zone analytics returning non-zero requests OR GA4 Real-Time showing test visit. No analytics confirmation = site is live but blind.
- [ ] All assets load from live URL (zero 404s on JS/CSS/images — verify with browser network tab)
- [ ] `<title>`, `<meta description>`, and Open Graph tags present in `<head>`
- [ ] `.nojekyll` file present at root (GitHub Pages requirement)
- [ ] Test suite executed with zero failures — verified by re-execution, NOT by checking file existence
- [ ] GitHub Wiki updated with any issues found during testing (`OWNER/REPO.wiki.git`)
- [ ] All P1 GitHub Issues triaged (close completed, migrate to next sprint, or explicitly defer with rationale in Issue comment)
- [ ] File committed with format: `ACTION:[CREATE|EDIT] FILE: path RATIONALE:reason`
- [ ] `git log -1 --oneline` confirms commit exists
- [ ] UNIVERSAL GATES above satisfied

---
*Generated from DEFINITION-OF-DONE-TEMPLATE.md v2.0*

## DEPLOYMENT TASK (Cloudflare Pages / Workers / R2)

- [ ] Site returns HTTP 200 with valid HTML on production URL
- [ ] HTTPS enforced (HTTP → HTTPS redirect working)
- [ ] Custom domain verified active (not pending/initializing)
- [ ] **Analytics gate (BLOCKING):** At least one analytics provider confirmed active:
  - [ ] Cloudflare zone analytics: non-zero requests in dashboard API response, OR
  - [ ] Cloudflare Web Analytics: RUM site tag returns 200, OR
  - [ ] GA4: Real-Time report shows test visit within 60 seconds, OR
  - [ ] Google Sites Analytics: measurement ID confirmed inserted in site settings
  - [ ] If NO analytics provider confirmed: `[BLOCKED: analytics-not-verified]`
- [ ] `cf-ray` header confirmed present (proxied traffic flowing)
- [ ] DNS CNAME record verified with `dig` or `curl -sI`
- [ ] Deployment evidence posted to GitHub Issue (deployment URL, analytics status, verification output)
- [ ] Original source (GitHub Pages / prior host) still functional (dual-running until cutover)
- [ ] Free tier thresholds checked: no cost risk from deployment
- [ ] Test visit from at least 2 geographic locations (generate traffic via browser + curl)
- [ ] UNIVERSAL GATES above satisfied
