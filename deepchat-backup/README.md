# DeepChat Settings Backup

**Backup Date:** 2026-05-08
**Purpose:** Disaster recovery — restore DeepChat configuration after data loss, corruption, or application failure.

## Contents

### `appdata-settings/` — Core Configuration Files
Copied from `C:\Users\LENOVO\AppData\Roaming\deepchat\`

| File | Description | Size |
|------|-------------|------|
| `app-settings.json` | Main application settings (theme, language, font, sound, etc.) | 42.7 KB |
| `system_prompts.json` | System prompt definitions for all agents | 75.1 KB |
| `custom_prompts.json` | User-defined custom prompts | 171.4 KB |
| `custom_prompts.json.bak` | Custom prompts backup | 171.4 KB |
| `mcp-settings.json` | MCP server configurations | 4.3 KB |
| `model-config.json` | Model provider settings | 2.1 KB |
| `acp_agents.json` | ACP agent configurations | 425 B |
| `knowledge-configs.json` | Knowledge base settings | 27 B |
| `Preferences` | Electron preferences | 168 B |
| `Local State` | Application local state | 434 B |
| `settings-window-state.json` | Settings window position | 141 B |
| `window-state.json` | Main window position | 140 B |
| `lockfile` | Instance lock file | 0 B |

### `skills/` — Installed Skills (14 skills)
Copied from `C:\Users\LENOVO\.deepchat\skills\`

Includes: algorithmic-art, code-review, deepchat-settings, doc-coauthoring, docx, frontend-design, git-commit, infographic-syntax-creator, mcp-builder, pdf, pptx, skill-creator, web-artifacts-builder, xlsx

### `templates/` — Prompt Template Registry
- `template-inventory.json` — All 9 registered prompt templates with metadata

## Restoration Guide

1. Close DeepChat completely
2. Copy files from `appdata-settings/` back to `C:\Users\LENOVO\AppData\Roaming\deepchat\`
3. Copy `skills/` contents back to `C:\Users\LENOVO\.deepchat\skills\`
4. Restart DeepChat

## Pre-Restore Checklist
- [ ] DeepChat is fully closed (check Task Manager)
- [ ] Existing config backed up (rename old directory as additional safety)
- [ ] File permissions allow write to AppData\Roaming
