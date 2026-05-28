---
name: template-catalog
description: Template discovery and parameter documentation. Use when the agent needs to find the right template for a task or check template parameters.
version: "1.0"
---

# TEMPLATE CATALOG SKILL — v1.0

> **On-demand skill.** Load via `skill_view('template-catalog')` to discover available templates.
> Source: `prompts.json` + `templates/` directory

---

## Available Templates (12 total)

### Core Project Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `PROJECT-INITIATION` | New project setup | `project_name`, `description`, `domain`, `moscow_analysis` |
| `PROJECT-CHARTER` | Project charter document | `project_name`, `scope`, `success_criteria`, `constraints` |
| `DEFINITION-OF-DONE` | Quality gates | `project_name`, `deliverable_type`, `acceptance_criteria` |
| `HANDOFF` | Agent-to-agent handoff | `type`, `scope`, `success_criteria`, `research_trail`, `return_protocol` |
| `README` | Project README | `project_name`, `description`, `repo_url`, `architecture` |

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
| `EMAIL-AGENT-TEMPLATE` | Email composition | `to`, `subject`, `body`, `cc`, `bcc`, `attachments` |

### Research Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `RESEARCH-LAUNCH` | Research pipeline launch | `topic`, `scope`, `output_type`, `priority` |

---

## How to Use Templates

```python
# Get template parameters
fill_prompt_template("get_prompt_template_parameters", {templateName: "HANDOFF"})

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
