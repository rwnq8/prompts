---
name: github-manager
description: Manage GitHub repositories, issues, projects, releases, and PRs via gh CLI. Use when the agent needs to create repos, manage project boards, or interact with GitHub Issues/Projects.
tools: exec
---
# GitHub Manager

## When to Use
- Creating new repositories (under qnfo/ org)
- Managing GitHub Issues (create, label, close, comment)
- Managing GitHub Projects (Kanban boards)
- Creating GitHub Releases
- Managing Pull Requests
- Updating wiki pages

## Authentication
```bash
gh auth status  # Must show: repo, workflow, read:org, gist
# If not authenticated: gh auth login
```

## Quick Reference

### Repositories
```bash
# Create under qnfo/ org (NEVER personal account)
gh repo create qnfo/<name> --public --description "..."

# Clone
gh repo clone qnfo/<name>
```

### Issues
```bash
# Discover active work
gh issue list --repo qnfo/<name> --label "project-state" --state open
gh issue list --repo qnfo/<name> --label "handoff" --state open

# Create
gh issue create --repo qnfo/<name> --title "..." --body "..." --label "task,bug"

# Close
gh issue close --repo qnfo/<name> <num> --reason completed

# Edit labels
gh issue edit --repo qnfo/<name> <num> --add-label "in-progress"

# Comment
gh issue comment --repo qnfo/<name> <num> --body "STATUS: ACTIVE | PHASE: 2"
```

### Required Labels (Create on Repo Init)
```
project-state, handoff, task, bug, enhancement, blocked, documentation, research
```
```bash
gh label create "project-state" --repo qnfo/<name> --color "0E8A16"
gh label create "handoff" --repo qnfo/<name> --color "D93F0B"
```

### Projects (Kanban Boards)
```bash
gh project list --owner qnfo
gh project item-list <board-num> --owner qnfo
gh project item-create <board-num> --owner qnfo --title "..." --body "..."
```

### Releases
```bash
gh release create v1.0.0 --repo qnfo/<name> --title "Release v1.0.0" --notes "..."
gh release upload v1.0.0 ./file.pdf --repo qnfo/<name>
```

### Wiki
```bash
# Clone wiki repo
git clone https://github.com/rwnq8/prompts.wiki.git
# Edit pages, commit, push
```

### Pull Requests
```bash
gh pr create --repo qnfo/<name> --title "..." --body "..."
gh pr list --repo qnfo/<name>
gh pr merge <num> --repo qnfo/<name> --squash
```

## Project Initiation Protocol (New Projects)
1. Create repo: `gh repo create qnfo/<name> --public`
2. Create required labels (8 labels above)
3. Create project-state Issue
4. Create GitHub Project board
5. Register on QNFO Program Board
6. Clone and initialize with README.md

## Failure Scenarios
| Failure | Cause | Recovery |
|:--------|:------|:---------|
| gh not authenticated | No token | `gh auth login` |
| Repo already exists | Name collision | Use unique name or check existing |
| Label creation fails | Permission issue | Verify org membership |
| Issue rate-limited | Too many requests | Wait 60s, retry once |
| QNFO org flagged | Platform abuse detection | Document and escalate |

## Platform Failure Recovery Protocol
If GitHub is unavailable (rate limiting, outage, QNFO org flagging):
1. Continue work locally — do NOT block on GitHub
2. Local PM files serve as MANDATORY REDUNDANT BACKUP
3. Sync to GitHub when available
4. Priority: local filesystem first, GitHub second
