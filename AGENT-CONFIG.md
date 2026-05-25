# AGENT-CONFIG.md — DeepChat Agent Configuration

> **Version:** v5.3 | **Last Updated:** 2026-05-25 (reconstructed from live tool definitions)
> **Purpose:** Authoritative reference for agent identity, slot IDs, write sandboxes, and tool configurations. This file was reconstructed after the original v5.2 was lost.

---

## 1. AGENT INSTANCES — DeepChat Settings → Agents

| Agent Name | System Prompt | Write Sandbox | Purpose |
|:-----------|:-------------|:--------------|:--------|
| **Projects** | `DEFAULT.md` (149K) | `G:\My Drive\projects\<name>\` | Project Executor — autonomous research, writing, coding |
| **Prompts** | `META-PROMPT-DEEPSEEK.md` (35K) | `G:\My Drive\prompts\` | System prompt engineering — create, edit, audit prompts |
| **QWAV** | `QWAV-DEFAULT.md` (18K) + `DEFAULT.md` | `G:\My Drive\QWAV\` | Program/Portfolio Manager — coordinates across projects, manages GitHub Issues/Projects |

---

## 2. SUBAGENT SLOT IDs — Live Configuration

> **Source:** Extracted from `subagent_orchestrator` tool definition (live system), verified 2026-05-25.

| Role | Slot ID | Input | Tool Reliability |
|:-----|:--------|:------|:-----------------|
| **EXPLORER** — Divergent Thinking | `self` | Inline text only | ~35% file I/O |
| **IMPLEMENTER** — Convergent Execution | `slot-mp80dr5g-oh9g` | Inline text only | ~35% file I/O |
| **REVIEWER** — Critical Evaluation | `slot-mp80e4mj-5s1l` | Inline text only | ~35% file I/O |

**CRITICAL:** The Prompts agent does NOT have `subagent_orchestrator` access. It works alone.

---

## 3. WRITE SANDBOXES — 1:1 Agent-to-Directory Mapping

| Agent | Write Sandbox | MOVE Destinations | Read Scope |
|:------|:-------------|:------------------|:-----------|
| Projects | `G:\My Drive\projects\<name>\` | `Archive\projects\YYYY\MM\`, GitHub Releases | ALL directories |
| Prompts | `G:\My Drive\prompts\` | `Archive\prompts\` | ALL directories |
| QWAV | `G:\My Drive\QWAV\` | `Archive\QWAV\`, GitHub Releases | ALL directories |

---

## 4. TOOL AVAILABILITY MATRIX

| Tool | Projects | QWAV | Prompts |
|:-----|:--------|:-----|:--------|
| `read`, `write`, `edit` | ✅ | ✅ | ✅ |
| `exec`, `process` | ✅ | ✅ | ✅ |
| `subagent_orchestrator` | ✅ | ✅ | ❌ |
| `fill_prompt_template` | ✅ | ✅ | ✅ |
| `deepchat_question` | ✅ | ✅ | ✅ |
| `skill_list/view/manage` | ✅ | ✅ | ✅ |
| `search_conversations` | ✅ | ✅ | ✅ |
| `get_browser_status`, `load_url`, `cdp_send` (YoBrowser) | ✅ | ✅ | ✅ |
| `brave_web_search`, `brave_local_search` | ✅ | ✅ | ✅ |
| Buffer API (social media) | ✅ | ✅ | ✅ |
| Email (Outlook COM) | ✅ | ✅ | ❌ |
| `list_all_prompt_template_names` | ✅ | ✅ | ✅ |
| `get_prompt_template_parameters` | ✅ | ✅ | ✅ |

---

## 5. SYSTEM PROMPT INHERITANCE

```
DEFAULT.md (149K) ─── Projects agent (full prompt)
                   └── QWAV agent (DEFAULT.md + QWAV-DEFAULT.md appended)
                        QWAV-DEFAULT.md (18K) is a PROGRAM DELTA only
                        — it does NOT duplicate DEFAULT.md content

META-PROMPT-DEEPSEEK.md (35K) ─── Prompts agent (standalone)
```

---

## 6. AGENT DESCRIPTION FILES (Reference)

| File | Audience | Purpose |
|:-----|:---------|:--------|
| `agents/PROJECTS-AGENT.md` | Projects agent | Identity, tools, triggers, anti-patterns, chaining patterns |
| `agents/QWAV-AGENT.md` | QWAV agent | Identity, sandbox, domain guidance, anti-patterns |
| `agents/PROMPTS-AGENT.md` | Prompts agent | Identity, scope boundary, task type detection |
| `agents/subagents/EXPLORER-SUBAGENT.md` | All agents | Divergent thinking — brainstorming, alternatives |
| `agents/subagents/IMPLEMENTER-SUBAGENT.md` | All agents | Convergent execution — drafting, structured output |
| `agents/subagents/REVIEWER-SUBAGENT.md` | All agents | Critical evaluation — validation, reader testing |

---

*AGENT-CONFIG.md v5.3 — Reconstructed 2026-05-25 from live subagent_orchestrator tool definition, ARCHITECTURE.md, DEFAULT.md, and agent description files.*
