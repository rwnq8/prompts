# Optimized DeepChat Settings Architecture

## Layer Model

```
LAYER 0: DeepChat Platform (Agent Loop, ToolPresenter, subagent_orchestrator)
LAYER 1: default_system_prompt (app-settings.json, ~17K → ideal ~10K)
LAYER 2: Agent System Prompts (DEFAULT.md, META-PROMPT-DEEPSEEK.md, QWAV-DEFAULT.md)
LAYER 3: Skills (on-demand, 7 files, loaded via skill_view)
LAYER 4: Custom Prompt Templates (10 files, invoked via fill_prompt_template)
LAYER 5: Subagent Prompts (EXPLORER, IMPLEMENTER, REVIEWER)
LAYER 6: Agent Configs (PROJECTS, PROMPTS, QWAV)
LAYER 7: MCP Tools (Brave Search, Buffer, LinkedIn)
LAYER 8: ACP Agents (claude-acp, codex-acp, kimi — currently disabled)
LAYER 9: Wiki (rwnq8/prompts/wiki — documentation, never in agent context)
```

## What Changed

### DEFAULT.md: 177K → 24K (-86.5%)
- KEPT: Rules 1-6,12-14, git protocol, delegation, write-then-verify, anti-phantom
- ADDED: Skill triggers (one-liners: "To send email → skill_view('email-composer')")
- REMOVED: Email COM (~25K), template docs (~53K), GitHub workflow (~20K),
  publication pipeline (~20K), Cloudflare (~15K), close-out (~10K), git failures (~4K)

### New Skills (7 files, ~30K total)
| Skill | Replaces | When Loaded |
|:------|:---------|:------------|
| email-composer | DEFAULT.md §E (25K) | Sending email |
| cloudflare-deployer | Inline docs (15K) | Deploying to Cloudflare |
| publication-publisher | DEFAULT.md §11-12 (20K) | Publishing documents |
| github-manager | DEFAULT.md §0.6.8 (20K) | Managing GitHub projects |
| closeout-manager | DEFAULT.md §12.2 (10K) | Closing out projects |
| git-hygiene | DEFAULT.md §9.7 (4K) | Git failure recovery |
| template-catalog | DEFAULT.md §0.6.4 (53K) | Finding templates |

## Installation

1. Copy skills/ to %APPDATA%\DeepChat\skills\ (or your skillsPath)
2. Replace system prompts in DeepChat Settings → Agents → [Name] → System Prompt
3. Agent configs and subagent files replace agents/ in prompts directory
4. Templates replace templates/ in prompts directory
5. Restart DeepChat to load new skills

## Skill Invocation

Agents use skill_view('skill-name') to load a skill on demand.
Skills unload after use — freeing context for the main task.

## Source

Generated from rwnq8/prompts — the system prompt engineering workspace.
