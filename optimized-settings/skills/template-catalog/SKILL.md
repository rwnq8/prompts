---
name: template-catalog
description: Catalog of all available fill_prompt_template templates with descriptions, parameters, and use cases. Use when the agent needs to find the right template for a task.
tools: fill_prompt_template, list_all_prompt_template_names
---
# Template Catalog

## How to Use
1. Call `list_all_prompt_template_names` to get available templates
2. Call `get_prompt_template_parameters("template-name")` for required params
3. Call `fill_prompt_template("template-name", {args})` to invoke

## Template Reference

### EMAIL-AGENT-TEMPLATE (7.5 KB)
Compose and send emails via Outlook COM automation.
- Parameters: `to`, `subject`, `body`, `cc` (optional), `bcc` (optional), `attachments` (optional), `send_mode` (draft|send)
- Use when: Sending any email

### CLOUDFLARE-DEPLOYMENT (15.2 KB)
Deploy to Cloudflare Pages, R2, Workers, or Sandboxes.
- Parameters: `project_name`, `resource_type` (pages|r2|workers|sandbox), `branch`, `command`
- Use when: Deploying to Cloudflare

### ZENODO-PUBLISH (4.3 KB)
Register DOI and publish to Zenodo.
- Parameters: `title`, `authors`, `description`, `file_path`, `upload_type`, `sandbox` (true|false)
- Use when: Publishing research with DOI

### SOCIAL-ORCHESTRATOR-TEMPLATE (7.4 KB)
Cross-post to social media platforms via Buffer API.
- Parameters: `platforms` (comma-separated), `content`, `schedule` (now|custom), `media_urls` (optional)
- Use when: Publishing to social media

### DEFINITION-OF-DONE (6.6 KB)
Checklist for task completion verification.
- Parameters: `task_description`, `acceptance_criteria`, `evidence_required` (true|false)
- Use when: Verifying task completion

### HANDOFF (2.8 KB)
Multi-agent handoff with state transfer.
- Parameters: `target_agent`, `project_state`, `next_tasks`, `blockers`
- Use when: Handing off work between agents

### PROJECT-CHARTER (2.1 KB)
Project charter with scope, timeline, and deliverables.
- Parameters: `project_name`, `scope`, `timeline`, `deliverables`
- Use when: Initiating a new project

### PROJECT-INITIATION (6.3 KB)
Full project initialization workflow with GitHub integration.
- Parameters: `project_name`, `description`, `repo_org` (default: qnfo)
- Use when: Creating a new project from scratch

### CLOSEOUT-CHECKLIST (7.9 KB)
Comprehensive project closeout with archive, PDF, and release.
- Parameters: `project_name`, `archive` (true|false), `pdf` (true|false), `release` (true|false)
- Use when: Closing out a project

### PDF-BUILDER-TEMPLATE (7.4 KB)
Convert markdown to PDF with formatting.
- Parameters: `input_file`, `output_file`, `template` (default|academic|report)
- Use when: Generating PDF from markdown

## Template Size Reference
| Template | Size | Load Cost |
|:---------|:-----|:----------|
| CLOUDFLARE-DEPLOYMENT | 15.2 KB | Heavy — use skill instead |
| CLOSEOUT-CHECKLIST | 7.9 KB | Medium |
| PDF-BUILDER-TEMPLATE | 7.4 KB | Medium |
| SOCIAL-ORCHESTRATOR-TEMPLATE | 7.4 KB | Medium |
| EMAIL-AGENT-TEMPLATE | 7.5 KB | Medium |
| DEFINITION-OF-DONE | 6.6 KB | Medium |
| PROJECT-INITIATION | 6.3 KB | Medium |
| ZENODO-PUBLISH | 4.3 KB | Light |
| HANDOFF | 2.8 KB | Light |
| PROJECT-CHARTER | 2.1 KB | Light |

## Best Practice
For complex workflows, use a SKILL (skill_view) instead of repeatedly invoking templates. Skills carry the workflow logic; templates just provide the output format.
