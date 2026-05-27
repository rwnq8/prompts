---
name: git-hygiene
description: Git failure recovery, branch management, and advanced scenarios. Use when the agent encounters git errors, branch issues, or needs to recover from git problems.
tools: exec
---
# Git Hygiene

## When to Use
- Git operation fails (commit rejected, merge conflict, detached HEAD)
- Branch was renamed by parallel process (CPL L19)
- Need to recover lost commits
- Dirty worktree preventing operations
- Accidentally committed to main/master

## Core Rules (Always Applied)
1. NEVER commit to main/master — feature branches only
2. Pre-work: `git branch --show-current` → must be `feature/<name>`
3. Post-work: `git log -1 --oneline` after every commit
4. Write-then-verify: filesystem verification before staging
5. Never use `-ErrorAction SilentlyContinue`

## Failure Scenario Quick Reference

### F1: On main/master
```bash
git checkout -b feature/<kebab-case-description>
```

### F2: Dirty worktree (uncommitted changes)
```bash
git stash push -m "WIP: <description>"
# ... do work ...
git stash pop
```

### F3: Commit not executed (phantom claim)
```bash
# Verify what's staged
git diff --cached --name-status
# If nothing staged: git add <files>, then git commit
```

### F4: Detached HEAD
```bash
git checkout -b feature/<recovery-branch>
```

### F5: Merge conflict
```bash
git status  # See conflicted files
# Resolve conflicts in editor
git add <resolved-files>
git commit -m "ACTION:MERGE FILE: <files> RATIONALE:Resolve conflicts"
```

### F6: Wrong branch (committed to wrong feature branch)
```bash
git log -1 --oneline  # Note commit hash
git checkout <correct-branch>
git cherry-pick <hash>
git checkout <wrong-branch>
git reset --hard HEAD~1
```

### F7: Forgot to commit
```bash
git status  # See what changed
git add <files>
git commit -m "ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE:<reason>"
```

### F8: Accidental `git add .` (staged too many files)
```bash
git reset HEAD <unwanted-file>  # Unstage specific files
# Or: git reset HEAD  (unstage all, then selectively re-add)
```

### F9: Orphan feature branch never merged
```bash
# If work is complete:
git checkout main
git merge feature/<name>
git branch -d feature/<name>

# If work is abandoned:
git branch -D feature/<name>  # Force delete with documented rationale
```

### F10: Branch renamed by parallel process (CPL L19)
```bash
# Symptom: git branch --show-current shows different name
#        but git log shows same commits
# Action: Update recorded branch name, continue — do NOT create another branch
git branch --show-current  # Note new name
git log -1 --oneline       # Verify commits match
# Continue work on renamed branch
```

### F11: git log verification fails (CPL L13)
```bash
# Expected: git log -1 --oneline shows the commit you just made
# If not: check git status, re-stage, re-commit
```

### F12: Write-then-verify failure (CPL L15)
```bash
# After every file write or edit:
Test-Path <file>           # Must return True
Get-Content <file> -First 5 # Must show expected content
# If either fails: re-write file, re-verify
```

## Branch Naming Convention
```
feature/<kebab-case-description>
```
- Lowercase, hyphens, concise
- Examples: `feature/git-hygiene-enforcement`, `feature/add-email-skill`
- Anti-patterns: `fix`, `test`, `update`, `my-branch`, `temp`

## Commit Format
```
ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE:<reason>
```
Example: `ACTION:CREATE FILE: skills/email-composer/SKILL.md RATIONALE:Extract email COM from DEFAULT.md into on-demand skill`

## Ultimate Rule
**If you say you committed, the commit MUST exist.**
Verify with `git log -1 --oneline` before claiming any git operation.
