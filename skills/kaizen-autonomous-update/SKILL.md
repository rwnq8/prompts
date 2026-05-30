# SKILL: kaizen-autonomous-update (v1.0)

> **QNFO Custom Skill** — Load via `read('G:\\My Drive\\prompts\\skills\\kaizen-autonomous-update\\SKILL.md')`
> **Template:** `fill_prompt_template("KAIZEN-AUTONOMOUS-UPDATE", {...})`

---

## Purpose

Autonomous system-wide Kaizen continuous improvement protocol. Executes comprehensive audit of ALL DeepChat settings — prompts, templates, skills, agents, subagents — applies improvements, deploys changes, and commits with full audit trail.

## When to Use

| Trigger | Example |
|:--------|:--------|
| User issues Kaizen update command | "UPDATE ALL FROM KAIZEN", "UPDATE ALL DEEPCHAT SETTINGS FROM KAIZEN" |
| Kaizen engine finds 5+ unapplied improvements | Auto-triggered threshold |
| System consistency audit finds 3+ drift items | Proactive maintenance |
| After major architecture changes | Ensures all components stay synchronized |

## Tools Required

| Tool | Purpose |
|:-----|:--------|
| `read`, `write`, `edit` | File operations on prompts, templates, skills, agents |
| `exec`, `process` | Run audit scripts, git, wrangler, deploy |
| `fill_prompt_template` | Fill the KAIZEN-AUTONOMOUS-UPDATE template |
| `brave_web_search` | Web research for current best practices (when needed) |
| `git` (via exec) | Branch management, commits |
| `wrangler` (via exec) | R2 Discovery Index and audit trail operations |

## Protocol (7 Phases)

Fill the `KAIZEN-AUTONOMOUS-UPDATE` template using `fill_prompt_template`. The template contains the complete 7-phase execution protocol:

| Phase | Description | Key Output |
|:------|:-----------|:-----------|
| **0. Pre-Flight** | Discovery Index pull, Kaizen audit, comprehensive Python audit | Gap report |
| **1. System Prompts** | Update DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT-DEEPSEEK.md | Version bumps |
| **2. Templates** | Audit staleness, merge duplicates, deprecate unused | Clean template set |
| **3. Skills** | Version headers, tool docs, read-based loading patterns | Versioned skills |
| **4. Agent Configs** | Tool lists, subagent slots, system prompt references | Updated configs |
| **5. Subagent Prompts** | Research Integrity, DoD criteria, anti-patterns | Updated subagents |
| **6. Deploy & Commit** | Dry-run, deploy, git commit with verification | Deployed + committed |
| **7. R2 Upload** | Kaizen report to R2, Discovery Index update, cleanup | Audit trail |

## Comprehensive Audit Script

The Phase 0 comprehensive audit (`_kaizen_system_audit.py`) checks:

1. **Version consistency** — every prompt, template, skill, agent has a version
2. **Required section presence** — Rules 1-6, 12-14, Research Integrity, Web Research Protocol, File Lifecycle, Publication Language Gate, Git Protocol, Cloudflare-Native, Discovery Index Step 0, Kaizen §9.5
3. **Cross-reference integrity** — QWAV→DEFAULT section refs, agent→system prompt refs
4. **Skill completeness** — version, tools, read-based loading, trigger conditions
5. **Template staleness** — every template must be referenced somewhere
6. **Guardrail completeness** — all essential guardrails present
7. **Kaizen engine health** — conversation search, R2 integration

## Related Skills

| Skill | When to Use |
|:------|:-----------|
| `git-hygiene` | If git operations fail during update |
| `closeout-manager` | After update completes, for session close-out |
| `template-catalog` | To verify template entries after cleanup |
| `cloudflare-deployer` | If R2/wrangler operations fail |
| `publication-publisher` | If the update report needs formal publication |

## Safety Rules

1. **NEVER work on main branch** — always `feature/kaizen-autonomous-update`
2. **Read before write** — never edit a file from memory
3. **One component at a time** — update → verify → commit before next
4. **Never delete PERMANENT files** — only EPHEMERAL files
5. **Version ALL changes** — every edit = version bump + VERSION HISTORY
6. **Filesystem verify after every write** — `Test-Path` + `Get-Content -First 5`
7. **Git verify after every commit** — `git log -1 --oneline`
8. **Anti-Phantom Rule 14** — never claim an action without tool evidence

## QNFO Custom Skill Note

This is a QNFO custom skill deployed via `tools/deploy.py`. It is NOT accessible via `skill_view()` (which only indexes DeepChat's built-in registry). Load it with:

```
read('G:\\My Drive\\prompts\\skills\\kaizen-autonomous-update\\SKILL.md')
```

---

*kaizen-autonomous-update v1.0 — Autonomous system-wide Kaizen improvement protocol. 7-phase execution. Template-driven.*

---

*kaizen-autonomous-update v1.0 — QNFO custom skill. Load via read('G:\\My Drive\\prompts\\skills\\kaizen-autonomous-update\\SKILL.md'). Not accessible via skill_view().*
