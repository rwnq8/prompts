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
| **Agent names, tools, slot IDs** | Reference `AGENT-CONFIG.md` for the exact values |

### Reference files (read, don't paste)
| File | Purpose |
|:-----|:--------|
| `AGENT-CONFIG.md` | Configuration reference — agent names, tools, slot IDs, write boundaries |
| `agents/PROJECTS-AGENT.md` | Detailed Projects agent execution spec (LLM reads this, you don't need to) |
| `agents/PROMPTS-AGENT.md` | Detailed Prompts agent execution spec |
| `agents/QWAV-AGENT.md` | Detailed QWAV agent execution spec |
| `agents/subagents/*.md` | Subagent descriptions (paste the short block) + execution specs (LLM reference) |

### Ongoing (occasional)
- Type **"SYSTEM HEALTH CHECK"** in any agent chat to run `system_audit.py`
- Check `CHANGELOG.md` to see what changed
- Check `ARCHITECTURE.md` for how the system is designed

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

### Active Templates (17 total — across templates/, email/, scholar/)
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
| SPRINT-BACKLOG-TEMPLATE | Sprint backlog |
| image-gen-banner-prompt | Generate banner images |

## Subagents (3 self-clones)

| Slot | Role | Use |
|:-----|:-----|:----|
| `slot-mp80a5ry-e7hn` | EXPLORER — Divergent thinking | Brainstorming, alternatives, edge cases |
| `slot-mp80ay3u-yzqo` | IMPLEMENTER — Convergent execution | Drafting, structured output |
| `slot-mp80b6bl-iix2` | REVIEWER — Critical evaluation | Blind validation, gap analysis |

## Directory Structure

```
prompts\
├── README.md                     ← YOU ARE HERE (human reference)
├── AGENT-CONFIG.md               ← Configuration reference (agent names, tools, slot IDs)
├── ARCHITECTURE.md               ← System taxonomy (LLM reference)
├── CHANGELOG.md                  ← Change history
│
├── META-PROMPT-DEEPSEEK.md       ← THE FACTORY: generates all system prompts
├── DEFAULT.md                    ← System prompt for Projects agent
├── QWAV-DEFAULT.md               ← System prompt for QWAV agent
├── system_audit.py               ← Health check (type "SYSTEM HEALTH CHECK")
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
├── templates\                    ← Prompt templates (consumed by fill_prompt_template) — 12 files
│   ├── SOCIAL-ORCHESTRATOR-TEMPLATE.md
│   ├── image-gen-banner-prompt.md
│   ├── ADR-TEMPLATE.md
│   ├── CHANGELOG-TEMPLATE.md
│   ├── CONTRIBUTING-TEMPLATE.md
│   ├── DEFINITION-OF-DONE-TEMPLATE.md
│   ├── HANDOFF-TEMPLATE.md
│   ├── PRODUCT-BACKLOG-TEMPLATE.md
│   ├── PROJECT-CHARTER-TEMPLATE.md
│   ├── README-TEMPLATE.md
│   ├── RETROSPECTIVE-TEMPLATE.md
│   └── SPRINT-BACKLOG-TEMPLATE.md
│
├── email\                        ← Email automation module (Outlook COM)
│   ├── EMAIL-AGENT-TEMPLATE.md
│   ├── EMAIL-CAPABILITIES.md
│   ├── email_*.py (7 scripts)
│   └── outlook_mcp_server\
│
├── scholar\                      ← Research pipeline (4 stages)
│   ├── STAGE-1-SETUP.md
│   ├── STAGE-2-DRAFT.md
│   ├── STAGE-3-REVIEW.md
│   └── STAGE-4-PUBLISH.md
│
└── audit-reports\                ← Generated health reports (auto)
```

## File Ownership

| Audience | Files |
|:---------|:------|
| **HUMAN** (you) | `README.md`, `CHANGELOG.md` |
| **HUMAN — paste into DeepChat** | `DEFAULT.md`, `QWAV-DEFAULT.md`, `META-PROMPT-DEEPSEEK.md`, subagent descriptions from `agents/subagents/` |
| **HUMAN — reference only** | `AGENT-CONFIG.md` (agent names, tools, slot IDs), `ARCHITECTURE.md` (system design) |
| **LLM** (agents) | Everything else |

**If you're ever confused about a file:** ask any agent "Why does this file exist? Is it for me or for you?"
