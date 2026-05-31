# Prompts — System Prompt Library v5.5

> **G:\My Drive\prompts\** — git-tracked prompt engineering workspace.
> **Generator:** META-PROMPT-DEEPSEEK.md v4.5 (the factory that produces system prompts).

---

## FOR THE HUMAN: What You Need to Know

**You manage a 3-agent LLM system.** This directory contains everything they need.

### What you actually paste into DeepChat
| DeepChat Field | Paste this file |
|:---------------|:----------------|
| **Projects agent → System Prompt** | Entire contents of `DEFAULT.md` |
| **QWAV agent → System Prompt** | Entire contents of `QWAV-DEFAULT.md` |
| **Prompts agent → System Prompt** | Entire contents of `META-PROMPT-DEEPSEEK.md` |
| **Each Subagent → Description** | Short block from `agents/subagents/EXPLORER-SUBAGENT.md` (etc.) |
| **Agent names, tools, slot IDs** | See `ARCHITECTURE.md` §1 for the exact values |

### Reference files (read, don't paste)
| File | Purpose |
|:-----|:--------|
| `ARCHITECTURE.md` (v1.4) | System design, agent taxonomy, slot IDs, sandboxing model |
| `agents/PROJECTS-AGENT.md` | Detailed Projects agent execution spec (LLM reads this, you don't need to) |
| `agents/PROMPTS-AGENT.md` | Detailed Prompts agent execution spec |
| `agents/QWAV-AGENT.md` | Detailed QWAV agent execution spec |
| `agents/subagents/*.md` | Subagent descriptions (paste the short block) + execution specs (LLM reference) |

### Ongoing (occasional)
- Type **"SYSTEM HEALTH CHECK"** in any agent chat to run `tools/system_audit.py`
- Check `ARCHITECTURE.md` for how the system is designed
- Check GitHub Discussions (#32+) for Architecture Decision Records

### Everything Else
**You never need to open, edit, or worry about any other file in this directory.** If an agent creates files you didn't ask for, tell it to explain or delete them.

---

## Architecture (3 Agents)

| Agent | System Prompt | Write Boundary |
|:------|:-------------|:---------------|
| **Projects** | DEFAULT.md | `G:\My Drive\projects\<name>\` |
| **QWAV** | QWAV-DEFAULT.md | `G:\My Drive\QWAV\` |
| **Prompts** | META-PROMPT-DEEPSEEK.md v4.5 | `G:\My Drive\prompts\` |

**Design principle:** Agent = filesystem write boundary. Email, social media, image generation are templates consumed within the Projects/QWAV agents — not separate agents.

## Prompt Templates (call via `fill_prompt_template`)

### Active Templates (18 total — in `templates/`)
| Template Name | Purpose |
|:--------------|:--------|
| EMAIL-AGENT TEMPLATE v1.2 | Draft emails from project outputs |
| SOCIAL-ORCHESTRATOR TEMPLATE v1.0 | Generate social media posts |
| Research Planning — Step 1 of 4 | Scholar pipeline: planning |
| Research Writing — Step 2 of 4 | Scholar pipeline: drafting |
| Research Review — Step 3 of 4 | Scholar pipeline: review |
| Research Publication — Step 4 of 4 | Scholar pipeline: publication |
| ADR-TEMPLATE | Architecture Decision Record |
| CHANGELOG-TEMPLATE | Changelog entry |
| CONTRIBUTING-TEMPLATE | Contributing guide |
| DEFINITION-OF-DONE-TEMPLATE | Definition of Done checklist |
| HANDOFF-TEMPLATE | Session handoff document |
| PRODUCT-BACKLOG-TEMPLATE | Product backlog |
| PROJECT-CHARTER-TEMPLATE | Project charter |
| README-TEMPLATE | README generator |
| RETROSPECTIVE-TEMPLATE | Project retrospective |
| RISK-REGISTER-TEMPLATE | Risk register |
| SPRINT-BACKLOG-TEMPLATE | Sprint backlog |
| image-gen-banner-prompt | Generate banner images |

## Subagents (3 self-clones)

| Slot | Role | Use |
|:-----|:-----|:----|
| `self` (auto-clone) | EXPLORER — Divergent thinking | Brainstorming, alternatives, edge cases |
| `slot-mp80dr5g-oh9g` | IMPLEMENTER — Convergent execution | Drafting, structured output |
| `slot-mp80e4mj-5s1l` | REVIEWER — Critical evaluation | Blind validation, gap analysis |

## Directory Structure

```
prompts\
├── README.md                     ← YOU ARE HERE (human reference)
├── ARCHITECTURE.md               ← System taxonomy + agent config (LLM + human reference)
├── CHANGELOG.md                  ← DEPRECATED — use GitHub Releases + Discussions
│
├── META-PROMPT-DEEPSEEK.md       ← THE FACTORY: generates all system prompts
├── DEFAULT.md                    ← System prompt for Projects agent
├── QWAV-DEFAULT.md               ← System prompt for QWAV agent
│
├── tools\                         ← Utility scripts (system_audit.py)
│
├── .github\                       ← GitHub-native infrastructure
│   ├── workflows\                 ← CI/CD (pdf-release, zenodo-publish, etc.)
│   └── ISSUE_TEMPLATE\            ← Issue templates (project-state, handoff, task, bug, audit)
│
├── agents\                        ← Agent & subagent execution specs (LLM reference)
│   ├── PROJECTS-AGENT.md
│   ├── QWAV-AGENT.md
│   ├── PROMPTS-AGENT.md
│   └── subagents\
│       ├── EXPLORER-SUBAGENT.md
│       ├── IMPLEMENTER-SUBAGENT.md
│       └── REVIEWER-SUBAGENT.md
│
├── templates\                     ← Prompt templates
├── email\                         ← Email agent workflow
├── scholar\                       ← Scholar pipeline (4 stages)
├── pdf\                           ← PDF builder workflow
├── prompts.json                   ← Auto-generated template cache
└── audit-reports\                 ← DEPRECATED — use GitHub Issues (label: audit)
```

## File Ownership

| Audience | Files |
|:---------|:------|
| **HUMAN** (you) | `README.md`, `ARCHITECTURE.md` |
| **HUMAN — paste into DeepChat** | `DEFAULT.md`, `QWAV-DEFAULT.md`, `META-PROMPT-DEEPSEEK.md`, subagent descriptions from `agents/subagents/` |
| **HUMAN — reference only** | `ARCHITECTURE.md` (system design, agent taxonomy, slot IDs) |
| **LLM** (agents) | Everything else |

**If you're ever confused about a file:** ask any agent "Why does this file exist? Is it for me or for you?"
