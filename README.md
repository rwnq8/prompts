# Prompts \u2014 System Prompt Library

System prompts that govern LLM agents. **G:\\My Drive\\prompts\\** is the active git-tracked workspace.

---

## Active System Prompts

| File | Agent | Use |
|:-----|:------|:----|
| **DEFAULT.md** v1.7+ | Projects | THE ONE \u2014 all research, writing, coding, project work. Hard isolation, 7-file docs, cross-project learning, semi-autonomous sprint progression (WHAT\u2019S NEXT? PROCEED / RESUME), Phase 0.1.6 project git init, email capabilities, Sections 11-12 publication & close-out standards. |
| META-PROMPT-DEEPSEEK.md v4.1 | Prompts | Create, review, and improve system prompts. |
| EMAIL-AGENT-v1.0.md | Email | Lightweight email agent for quick inbox sessions. |
| image-gen-banner-prompt.md | Image Gen | Generate banner images. |

## Active Prompt Templates (registered in DeepChat Settings \u2192 Prompts)

| Template Name | Purpose |
|:--------------|:--------|
| Research Planning Agent \u2014 Step 1 of 4: Setup | Scholar pipeline: research planning |
| Research Writing Agent \u2014 Step 2 of 4: Draft | Scholar pipeline: draft writing |
| Research Review Agent \u2014 Step 3 of 4: Quality Check | Scholar pipeline: review |
| Research Publication Agent \u2014 Step 4 of 4: Final Assembly | Scholar pipeline: publication |
| WHAT\u2019S NEXT? PROCEED | Autonomous sprint task selection |
| SOCIAL-ORCHESTRATOR TEMPLATE v1.0 | Generate social media content from publications |

## Reference & Infrastructure

| File | Content |
|:-----|:--------|
| SUBAGENT_DESCRIPTIONS.md v4.2 | Agent/subagent setup values for DeepChat Settings |
| CROSS-PROJECT-LEARNINGS.md | 7 cross-project lessons (L1-L7) |
| SOCIAL-ORCHESTRATOR-TEMPLATE.md | Social media template source (auto-registered) |
| SOCIAL-ORCHESTRATOR-v4.0.md | **DEPRECATED** \u2014 replaced by template |
| scholar/ | 4-stage research pipeline system prompts |
| email/ | Email scripts + Outlook MCP server |
| .gitattributes | Git line-ending config |

---

## DeepChat Setup (2 minutes)

```
Settings \u2192 Agents:
  Projects   \u2190 paste DEFAULT.md
  Prompts    \u2190 paste META-PROMPT-DEEPSEEK.md
  Email      \u2190 paste EMAIL-AGENT-v1.0.md
  Image Gen  \u2190 paste image-gen-banner-prompt.md

  All agents: enable read, write, edit, exec, process,
  deepchat_question, skill_list, skill_view, skill_manage

Settings \u2192 Subagents \u2192 SELF-CLONE slot:
  Paste slot description from SUBAGENT_DESCRIPTIONS.md

Settings \u2192 Prompts (templates auto-register from files in prompts/):
  Verify all 6 templates are present
```

**That\u2019s it.** Use the Projects agent for everything \u2014 including WHAT\u2019S NEXT? PROCEED / RESUME for autonomous sprint progression. Switch to Prompts/Email/Image Gen only for those specific tasks. Social media content is generated via the SOCIAL-ORCHESTRATOR TEMPLATE (called automatically during project close-out or manually via fill_prompt_template).
