---
name: template-catalog
description: Template discovery and parameter documentation. Use when the agent needs to find the right template for a task or check template parameters.
version: "1.0"
---

# TEMPLATE CATALOG SKILL — v1.1

> **On-demand skill.** Load via `skill_view('template-catalog')` to discover available templates.
> Source: `prompts.json` + `templates/` directory

---

## Available Templates (20 total)

### Core Project Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `PROJECT-INITIATION` | New project setup | `project_name`, `description`, `domain`, `moscow_analysis` |
| `PROJECT-CHARTER` | Project charter document | `project_name`, `scope`, `success_criteria`, `constraints` |
| `DEFINITION-OF-DONE` | Quality gates | `project_name`, `deliverable_type`, `acceptance_criteria` |
| `HANDOFF` | Agent-to-agent handoff | `type`, `scope`, `success_criteria`, `research_trail`, `return_protocol` |
| `DISCOVERY-PROTOCOL` | **Unified ecosystem discovery** | `scope`, `topic`, `project_name` |
| `BLING-USABILITY-AUDIT` | BLING UI usability audit | `project_name`, `url`, `screenshots` |

### Publication Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `ZENODO-PUBLISH` | Zenodo upload | `title`, `authors`, `description`, `keywords`, `file_path` |
| `PDF-BUILDER-TEMPLATE` | PDF generation | `source`, `output`, `template_style`, `include_toc` |
| `SOCIAL-ORCHESTRATOR-TEMPLATE` | Social media posts | `publication_title`, `url`, `abstract`, `channels` |

### Operations Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `CLOUDFLARE-DEPLOYMENT` | Cloudflare deploy | `action`, `project_name`, `branch`, `domain` |
| `CLOUDFLARE-AUDIT-EXPORT` | Session audit export | `agent`, `session_date`, `summary`, `decisions`, `files_changed` |
| `CLOSEOUT-CHECKLIST` | Session close-out | `project_name`, `session_type` |
| `KAIZEN-AUDIT` | Kaizen improvement report | `health_score`, `total_findings`, `auto_applied_count` |
| `KAIZEN-AUTONOMOUS-UPDATE` | Autonomous system-wide update | `trigger_type`, `components`, `auto_apply` |
| `EMAIL-AGENT-TEMPLATE` | Email composition | `to`, `subject`, `body`, `cc`, `bcc`, `attachments` |

### Research Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `RESEARCH-LAUNCH` | Research pipeline launch | `topic`, `scope`, `output_type`, `priority` |
| `RESEARCH-PROTOCOL` | Research methodology protocol | `topic`, `methodology`, `sources` |
| `PHYSICS-STYLE` | Physics/technical writing style enforcement (18-rule checklist) | (none — self-contained) |

---



## Tools Required

This skill is designed for use with QNFO agent tools. When loaded by a DEFAULT.md agent, the full tool suite (read, write, edit, exec, process, brave_web_search, YoBrowser, subagent_orchestrator) is available.

## QNFO Custom Skill Note

This is a QNFO custom skill deployed via `tools/deploy.py`. It is NOT accessible via `skill_view()` (which only indexes DeepChat's built-in registry). Load it with:

```
read('G:\My Drive\prompts\skills\template-catalog\SKILL.md')
```



## 2.5.1 Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (`qnfo/tools/`). Local copies at `G:\My Drive\prompts\tools\` are convenience copies only — R2 is the single source of truth.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:----------------------|:--------|
| `deploy.py` | `qnfo/tools/deploy.py` | `G:\My Drive\prompts\tools\deploy.py` | Deploys template files to DeepChat runtime |

### Script Recovery Protocol
If a script is missing from local disk:
1. Pull canonical from R2: `npx wrangler r2 object get qnfo/tools --remote --file=<local_path>`
2. Verify integrity: `Test-Path <local_path>`
3. If R2 copy also missing: flag `[SKILL-GAP: script <name>.py missing from R2, cannot bootstrap]`
4. Do NOT attempt to use this skill if its canonical scripts cannot be recovered.


## How to Use Templates

```python
# Get template parameters
get_prompt_template_parameters(templateName="HANDOFF")

# Fill a template
fill_prompt_template("HANDOFF", {
    type: "Program->Project",
    scope: "Research quantum error correction...",
    success_criteria: "Peer-review-ready paper...",
    ...
})

# List all templates
list_all_prompt_template_names()
```

---

## Template Discovery

For full parameter documentation of any template:
```python
get_prompt_template_parameters(templateName="<name>")
```

All templates stored in: `G:\My Drive\prompts\templates\`
Template registry: `G:\My Drive\prompts\prompts.json`

---

## Common Patterns

### Session Lifecycle
```
(Start) → DISCOVERY-PROTOCOL → RESEARCH-LAUNCH → ... → CLOSEOUT-CHECKLIST → CLOUDFLARE-AUDIT-EXPORT
```

### Autonomous Update
```
KAIZEN-AUDIT → KAIZEN-AUTONOMOUS-UPDATE → deploy → commit → discovery-update
```

### New Project
```
PROJECT-INITIATION → PROJECT-CHARTER → DEFINITION-OF-DONE → README → HANDOFF
```

### Publication
```
PDF-BUILDER-TEMPLATE → ZENODO-PUBLISH → CLOUDFLARE-DEPLOYMENT → SOCIAL-ORCHESTRATOR-TEMPLATE
```

### Session Lifecycle
```
(Start) → RESEARCH-LAUNCH → ... → CLOSEOUT-CHECKLIST → CLOUDFLARE-AUDIT-EXPORT
```

---

*template-catalog skill v1.0 — Load on-demand via skill_view() for template discovery*

---

*template-catalog v1.0 — QNFO custom skill. Load via read('G:\\My Drive\\prompts\\skills\\template-catalog\\SKILL.md'). Not accessible via skill_view().*
