---
name: publication-publisher
description: Publish documents with proper formatting, Zenodo DOI registration, and social media cross-posting. Use when the agent is publishing a research document, paper, or report.
tools: exec, fill_prompt_template
---
# Publication Publisher

## When to Use
- Publishing research papers or reports
- Registering Zenodo DOIs
- Cross-posting to social media
- Applying publication formatting standards

## Workflow
1. Apply formatting standards (Visible Author Block, curly quotes)
2. Register Zenodo DOI (if applicable)
3. Copy to GitHub Releases
4. Trigger PDF generation (if applicable)
5. Trigger social media cross-posting

## Visible Author Block (MANDATORY)
Every release document MUST include at the top:
```
**Author:** [Full Name] | **Date:** [YYYY-MM-DD] | **License:** CC BY 4.0
```
This block MUST be present in visible content — not hidden in metadata.

## Curly Quotes Standard
All publication documents use curly/smart quotes:
- Opening: `“` (")  |  Closing: `”` (")
- Single: `‘` (')  |  Single closing: `’` (')
Code blocks and inline code are exempt.

## Zenodo DOI Registration
```bash
# Via Zenodo REST API (preferred)
python -c "
import requests, json
# Create deposit
resp = requests.post(
    'https://zenodo.org/api/deposit/depositions',
    params={'access_token': ZENODO_TOKEN},
    json={'metadata': {'title': '...', 'upload_type': 'publication', ...}},
    headers={'Content-Type': 'application/json'}
)
deposition_id = resp.json()['id']

# Upload file
with open('paper.pdf', 'rb') as f:
    requests.put(
        f'https://zenodo.org/api/deposit/depositions/{deposition_id}/files/paper.pdf',
        params={'access_token': ZENODO_TOKEN},
        data=f
    )

# Publish
requests.post(
    f'https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish',
    params={'access_token': ZENODO_TOKEN}
)
"
```

### Sandbox vs Production
- Sandbox: `https://sandbox.zenodo.org/api/` (requires separate token)
- Production: `https://zenodo.org/api/`
- If sandbox token unavailable: document as [SANDBOX-SKIPPED], proceed to production

### Failure: sandbox.zenodo.org 403
Zenodo sandbox requires a separate token from production. If 403:
1. Document as [SANDBOX-SKIPPED]
2. Proceed directly to production deposit
3. Do NOT retry loop against 403

## Social Media Cross-Posting
```python
fill_prompt_template("SOCIAL-ORCHESTRATOR", {
    "platforms": "twitter, linkedin, mastodon",
    "content": "[Title] + link to publication",
    "schedule": "now"
})
```

## Pre-Publication Checklist
- [ ] Visible Author Block present
- [ ] Curly quotes applied (scan for straight quotes outside code blocks)
- [ ] All file references verified (Test-Path)
- [ ] Git log confirms all changes committed
- [ ] REVIEWER subagent passed fabrication audit
- [ ] PDF generated (if document project)
- [ ] Copied to GitHub Releases
- [ ] Zenodo DOI registered (if applicable)
- [ ] Social cross-post triggered (if applicable)
