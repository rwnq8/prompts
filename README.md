# Prompts — System Prompt Library

System prompts that govern LLM agents. **G:\My Drive\prompts\** is the active git-tracked workspace.

---

## Active Prompts

| File | Agent | Use |
|:-----|:------|:----|
| **DEFAULT.md** v1.5 | Projects | THE ONE — all research, writing, coding, project work. Hard isolation, 7-file docs, cross-project learning. |
| META-PROMPT-DEEPSEEK.md v4.1 | Prompts | Create and improve system prompts. |
| SOCIAL-ORCHESTRATOR-v4.0.md | Social | Manage Buffer social media posts. |
| image-gen-banner-prompt.md | Image Gen | Generate banner images. |

## Deprecated (kept for reference)

| File | Superseded by |
|:-----|:--------------|
| PROJECT-ISOLATION-ENFORCER-v1.0.md | DEFAULT.md v1.5 (Section 0.6) |
| PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md | DEFAULT.md v1.5 (Section 0.7) |

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
  Prompts   ← paste META-PROMPT-DEEPSEEK.md
  Social    ← paste SOCIAL-ORCHESTRATOR-v4.0.md
  Image Gen ← paste image-gen-banner-prompt.md

  All agents: enable read, write, edit, exec, process,
  deepchat_question, skill_list, skill_view, skill_manage

Settings → Subagents → SELF-CLONE slot:
  Paste slot description from SUBAGENT_DESCRIPTIONS.md
```

**That's it.** Use the Projects agent for everything. Switch to Prompts/Social/Image Gen only for those specific tasks.
