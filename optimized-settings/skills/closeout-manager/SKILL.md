---
name: closeout-manager
description: Execute project close-out procedures: archive, PDF generation, GitHub Release creation, and state update. Use when the agent is completing a project or session.
tools: exec, fill_prompt_template
---
# Closeout Manager

## When to Use
- Project work is complete
- Session is ending
- Agent needs to archive, release, and transition

## Workflow
1. Complete all pending commits (verify with git log)
2. Run Mandatory Close-Out Checklist
3. Archive project to Archive directory
4. Generate PDF (if document project)
5. Create GitHub Release
6. Update project-state Issue
7. Auto-continue to next project

## Mandatory Close-Out Checklist
- [ ] All code committed: README.md reflects final documentation
- [ ] All tests pass: Python self-tests return success
- [ ] Git log verified: `git log -1 --oneline` confirms last commit
- [ ] Publication-ready docs copied to GitHub Releases
- [ ] Auto-archive to: `G:\My Drive\Archive\projects\YYYY\MM\<name>\`
- [ ] Auto-PDF: `gh workflow run pdf-release.yml --repo qnfo/<name>`
- [ ] GitHub Release: `gh release create vX.Y.Z --repo qnfo/<name> --title "..." --notes "..."`
- [ ] Project-state Issue updated with final status + archive location

## Archive Path Convention
```
G:\My Drive\Archive\projects\YYYY\MM\<project-name>\
```
Example: `G:\My Drive\Archive\projects\2026\05\game-of-life\`

## PDF Generation
```bash
# For document projects with pdf-release workflow
gh workflow run pdf-release.yml --repo qnfo/<name>

# Manual (if no workflow)
fill_prompt_template("PDF-BUILDER-TEMPLATE", {...})
```

## GitHub Release
```bash
gh release create v1.0.1 --repo qnfo/<name> \
  --title "Release v1.0.1" \
  --notes "$(cat CHANGELOG.md)"
gh release upload v1.0.1 ./output/paper.pdf --repo qnfo/<name>
```

## Project State Update
```bash
gh issue comment <num> --repo qnfo/<name> --body "
## Project Complete
| Field | Value |
|:------|:------|
| Status | CLOSED |
| Archive | G:\\My Drive\\Archive\\projects\\YYYY\\MM\\<name>\\ |
| Release | https://github.com/qnfo/<name>/releases/tag/vX.Y.Z |
| PDF | Attached to Release |
"
```

## Social Media Trigger
If publication occurred:
```python
fill_prompt_template("SOCIAL-ORCHESTRATOR", {
    "platforms": "twitter, linkedin",
    "content": "New publication: [Title] | [DOI/URL]",
    "schedule": "now"
})
```

## Post-Close-Out Auto-Continue
1. Check GitHub Issues (label: project-state) for next active project
2. Prioritize: P0 > P1 > P2 > unfiled
3. If no projects: report "All projects closed out. Nothing pending."
4. If found: navigate to directory and begin session startup
