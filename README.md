# Prompts — System Prompt Library

System prompts that govern LLM agents. **G:\My Drive\prompts\** is the active git-tracked workspace.

---

## Active Prompts

| File | Agent | Use |
|:-----|:------|:----|
| **DEFAULT.md** v1.6 | Projects | THE ONE — all research, writing, coding, project work. Hard isolation, 7-file docs, cross-project learning, semi-autonomous sprint progression (WHAT'S NEXT? PROCEED / RESUME). |
| AUTONOMOUS-PROGRESSION-AGENT.md v1.0 | Autopilot | Ad-hoc autonomous task execution via WHAT'S NEXT? PROCEED / RESUME. Reads SPRINT.md, executes next task, updates docs, commits. |
| META-PROMPT-DEEPSEEK.md v4.1 | Prompts | Create and improve system prompts. |
| SOCIAL-ORCHESTRATOR-v4.0.md | Social | Manage Buffer social media posts. |
| image-gen-banner-prompt.md | Image Gen | Generate banner images. |

## Reference

| File | Content |
|:-----|:--------|
| SUBAGENT_DESCRIPTIONS.md v4.1 | Agent/subagent setup values for DeepChat Settings |
| .gitattributes | Git line-ending config |

---

## DeepChat Setup (30 seconds)

```
Settings → Agents:
  Projects  ← paste DEFAULT.md
  Autopilot ← paste AUTONOMOUS-PROGRESSION-AGENT.md
  Prompts   ← paste META-PROMPT-DEEPSEEK.md
  Social    ← paste SOCIAL-ORCHESTRATOR-v4.0.md
  Image Gen ← paste image-gen-banner-prompt.md

  All agents: enable read, write, edit, exec, process,
  deepchat_question, skill_list, skill_view, skill_manage

Settings → Subagents → SELF-CLONE slot:
  Paste slot description from SUBAGENT_DESCRIPTIONS.md
```

**That's it.** Use the Projects agent for everything. Switch to Autopilot for autonomous WHAT'S NEXT? PROCEED task execution. Use Prompts/Social/Image Gen only for those specific tasks.
