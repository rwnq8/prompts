---
template: KAIZEN-AUTONOMOUS-UPDATE
version: 1.1
---

# KAIZEN-AUTONOMOUS-UPDATE TEMPLATE v1.1

> **Purpose:** Autonomous system-wide Kaizen update protocol — triggers Kaizen engine, applies improvements across ALL components, deploys, and commits.
> **Cadence:** On-demand (user command "UPDATE ALL FROM KAIZEN") or auto-triggered when Kaizen engine finds 5+ unapplied improvements.
> **Output:** Comprehensive update report + git commit + deploy + R2 audit trail

---

## EXECUTION PROTOCOL

### Phase 0: Pre-Flight & Discovery

```bash
# 0.0 Git branch check — NEVER work on main
git branch --show-current
# If on main: git checkout -b feature/kaizen-autonomous-update

# 0.1 Pull Discovery Index
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json

# 0.2 Run Kaizen Engine audit
python "G:\My Drive\tools\kaizen_engine.py" --audit

# 0.3 Run system consistency audit
python tools/system_consistency_audit.py

# 0.4 Run Comprehensive Python System Audit (MANDATORY)
python _kaizen_system_audit.py
```

The Phase 0.4 comprehensive audit checks ALL of:
- **Version consistency** across all prompts, agents, subagents, skills, templates
- **Required section presence** in every system prompt (Rules 1-6, 12-14, Research Integrity, Web Research Protocol, File Lifecycle, Publication Language Gate, Git Protocol, Cloudflare-Native, Discovery Index Step 0, Kaizen)
- **Cross-reference integrity** — QWAV-DEFAULT.md section completeness (must be fully self-contained), agent config references to system prompts
- **Skill completeness** — version header, tool documentation, read-based loading patterns, trigger conditions
- **Template staleness** — referenced vs. unreferenced templates, duplicate detection
- **Guardrail completeness** — all essential guardrails present in all prompts
- **Kaizen engine health** — conversation search capability, R2 integration

### Phase 1: System Prompt Updates

| Prompt | Audit Checks | Update Priority |
|:-------|:-------------|:----------------|
| **DEFAULT.md** | Rule completeness, Web Research Protocol, File Lifecycle, Publication Language Gate, Git Protocol, Cloudflare-Native, Discovery Index Step 0, Kaizen §9.5 | CRITICAL |
| **META-PROMPT-DEEPSEEK.md** | Template requirements, skill references, subagent slot IDs, wiki references (→ R2), version self-consistency | HIGH |
| **QWAV-DEFAULT.md** | Self-containment verification (all rules embedded directly), domain-specific rules, cross-reference integrity, Research Integrity presence | CRITICAL |

**Update rules (HARD):**
- Version bump: MINOR for new content/sections, PATCH for fixes/typos
- Always append to VERSION HISTORY table at bottom of prompt
- Never remove content without documenting rationale
- Filesystem verify after every write: `Test-Path <file>` + `Get-Content <file> -First 5`
- Git verify after every commit: `git log -1 --oneline`
- **One prompt at a time**: Update prompts → verify self-containment → commit (each prompt is self-contained, order-independent)

### Phase 2: Template Audit & Cleanup

```bash
# Use the comprehensive audit to identify stale templates
python _kaizen_system_audit.py
# Review Section 3 (Template Audit) for STALE? tags
```

| Check | Action |
|:------|:-------|
| Duplicate templates (different names, same content) | Merge into canonical name, update ALL references, delete duplicate |
| Stale templates (unreferenced in any system prompt, skill, or agent config) | Mark with `[DEPRECATED vX.Y]` prefix in file, move to `templates/_archived/` |
| Missing templates (referenced but don't exist) | Create minimal stub OR remove reference from source |
| Template catalog mismatch | Update `skills/template-catalog/SKILL.md` count and entries |
| Unversioned templates | Add semantic version header to each template |

**Staleness detection method:** The comprehensive audit checks every template against:
- `fill_prompt_template("KAIZEN-AUTONOMOUS-UPDATE")` references in all system prompts
- Direct `templates/NAME.md` references in skill files
- `template-catalog` skill entries
- If NONE of these reference it → STALE

### Phase 3: Skill Updates

For each QNFO custom skill in `skills/`:

| Check | Fix |
|:------|:----|
| **Version header present?** | Add `# SKILL: <name> (vX.Y)` header with semantic version |
| **Tool documentation?** | Add "## Tools Required" section listing tools used |
| **Read-based loading?** | Add note: "QNFO custom skills use `read()` with filesystem path, not `skill_view()`" |
| **Trigger conditions clear?** | Add explicit "Use when:" or "Trigger:" section |
| **Cross-references valid?** | Fix any references to non-existent templates, tools, or paths |
| **GitHub wiki references?** | Replace with R2 `qnfo/` paths or local filesystem paths |

**Skill update checklist:**
- [ ] `bling-usability-audit/SKILL.md` — version, tools, read-based loading
- [ ] `closeout-manager/SKILL.md` — version, tools, read-based loading
- [ ] `cloudflare-deployer/SKILL.md` — version, tools, read-based loading
- [ ] `email-composer/SKILL.md` — version, tools, read-based loading
- [ ] `git-hygiene/SKILL.md` — version, tools, read-based loading
- [ ] `github-manager/SKILL.md` — version, tools, read-based loading
- [ ] `publication-publisher/SKILL.md` — version, tools, read-based loading
- [ ] `template-catalog/SKILL.md` — version, tools, read-based loading
- [ ] `kaizen-autonomous-update/SKILL.md` — create new skill

### Phase 4: Agent Config Updates

| Agent Config | Audit Checks | Common Gaps |
|:-------------|:-------------|:------------|
| PROMPTS-AGENT.md | System prompt reference, tool list, subagent slot IDs, Kaizen section | Missing `brave_web_search` in tool list, outdated slot IDs |
| PROJECTS-AGENT.md | System prompt reference, tool list, subagent delegation rules, Kaizen section | Missing Cloudflare-Native PM tools, outdated gh CLI refs |
| QWAV-AGENT.md | System prompt reference, domain-specific tools, anti-patterns | Buffer API refs, cross-contamination warnings |
| SUBAGENT-REFERENCE.md | Slot IDs, tool reliability stats, anti-patterns per subagent | Outdated slot IDs, missing subagent |

### Phase 5: Subagent Prompt Updates

Subagent prompts are embedded in DeepChat's `subagent_orchestrator` tool description AND maintained as canonical files:

| Subagent | Canonical File | Update Trigger |
|:---------|:---------------|:---------------|
| EXPLORER | `agents/subagents/EXPLORER-SUBAGENT.md` | Anti-patterns, Research Integrity §0 update, web search tool list |
| IMPLEMENTER | `agents/subagents/IMPLEMENTER-SUBAGENT.md` | Fabrication patterns, DoD criteria changes |
| REVIEWER | `agents/subagents/REVIEWER-SUBAGENT.md` | Review type additions, severity criteria changes |

**Note:** The canonical `.md` files are the SOURCE. After editing, run `G:\My Drive\tools\deploy.py` to sync to DeepChat runtime.

### Phase 6: Deploy & Commit

```bash
# 6.1 Dry-run deploy to preview changes
python "G:\My Drive\tools\deploy.py" --dry-run

# 6.2 Deploy all changes
python "G:\My Drive\tools\deploy.py"

# 6.3 Verify deployment (check all canonical paths synced)
python "G:\My Drive\tools\deploy.py" --dry-run
# Should show "All files up to date"

# 6.4 Git add ALL changed files
git add -A
git status

# 6.5 Git commit
git commit -m "ACTION:EDIT FILE: multiple RATIONALE:Kaizen autonomous update - {{summary}}"

# 6.6 Verify commit
git log -1 --oneline
```

### Phase 7: Kaizen Report & R2 Upload

```bash
# 7.1 Run Kaizen engine with --apply to record improvements
python "G:\My Drive\tools\kaizen_engine.py" --audit --apply

# 7.2 Upload Kaizen report to R2 audit trail
npx wrangler r2 object put qnfo/audit/kaizen/kaizen_update_{{date}}_{{time}}.md --file=audit/kaizen/kaizen_report_*.md --remote

# 7.3 Update Discovery Index with update entry
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json
# Update the "last_kaizen_update" field and add entry
npx wrangler r2 object put qnfo/discovery/index.json --file=_updated_index.json --remote

# 7.4 Clean up ephemeral files
Remove-Item _audit_filesystem.py, _kaizen_system_audit.py, _discovery_index.json, _updated_index.json -ErrorAction Stop
```

---

## UPDATE REPORT FORMAT

```markdown
# KAIZEN AUTONOMOUS UPDATE REPORT — {{date}} {{time}}

## Summary
- Components Updated: {{count}}
- Improvements Applied: {{count}}
- Version Bumps: {{list}}
- Deployment: {{status}}
- Git Commit: {{hash}}
- R2 Audit Trail: {{path}}

## Changes Applied

### System Prompts
| Prompt | Old Version | New Version | Changes |
|:-------|:-----------|:-----------|:--------|

### Templates
| Template | Action | Rationale |
|:---------|:-------|:----------|

### Skills
| Skill | Action | Rationale |
|:------|:-------|:----------|

### Agent Configs
| Agent | Action | Rationale |
|:------|:-------|:----------|

### Subagent Prompts
| Subagent | Action | Rationale |
|:---------|:-------|:----------|

## Remaining Gaps
| Gap | Severity | Recommended Action |
|:----|:---------|:-------------------|

## Verification
- [ ] All files filesystem-verified (Test-Path + Get-Content -First 5)
- [ ] All commits git-verified (git log -1 --oneline)
- [ ] Deployment verified (deploy.py --dry-run shows "All files up to date")
- [ ] Discovery Index updated on R2
- [ ] Kaizen report uploaded to R2 `qnfo/audit/kaizen/`
- [ ] Ephemeral files cleaned up
- [ ] Comprehensive audit re-run: 0 gaps
```

---

## TRIGGER CONDITIONS

| Trigger | Activation |
|:--------|:-----------|
| **User command** | "UPDATE ALL FROM KAIZEN" / "UPDATE ALL DEEPCHAT SETTINGS FROM KAIZEN" / "RUN KAIZEN AUTONOMOUS UPDATE" |
| **Kaizen threshold** | 5+ unapplied improvements in Kaizen engine report |
| **System drift** | `tools/system_consistency_audit.py` reports 3+ consistency failures |
| **Weekly** | Monday auto-trigger (if Kaizen engine has pending improvements) |

---

## SAFETY GATES

1. **Read-before-write:** Always read current file content before editing — never edit from memory
2. **Dry-run first:** Preview all changes with `G:\My Drive\tools\deploy.py --dry-run` before live deploy
3. **One-component-at-a-time:** Update → filesystem verify → git commit → next component
4. **Never delete PERMANENT files:** Only EPHEMERAL files may be removed (see File Lifecycle §6)
5. **Version all changes:** Every prompt/template/skill edit = version bump + VERSION HISTORY entry
6. **Filesystem verify:** After every write: `Test-Path <file>` + `Get-Content <file> -First 5`
7. **Git verify:** After every commit: `git log -1 --oneline`
8. **Anti-Phantom:** Never claim an action without tool evidence (Rule 14)
9. **Cross-reference audit:** After all updates, re-run comprehensive audit to verify 0 gaps

---

## REFERENCED SKILLS

This template works with:
- `template-catalog` — to verify template entries
- `git-hygiene` — for recovery from git failures during update
- `closeout-manager` — for session close-out after update
- `cloudflare-deployer` — for R2 upload verification

---

*KAIZEN-AUTONOMOUS-UPDATE v1.1 — Autonomous system-wide improvement protocol. Comprehensive audit + targeted fixes + deploy + R2 audit trail.*
