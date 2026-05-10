"""Fix 6 gaps found in blind validation test of DEFAULT.md git protocols."""
import os

os.chdir(r'G:\My Drive\prompts')
with open('DEFAULT.md', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ============================================================
# GAP 1+6: Fix Section 8 GIT BRANCH VIOLATION
# - Check stash list before stashing
# - Skip stash if worktree is clean
# - Use identifiable stash messages
# - Don't stash pop if nothing was stashed
# ============================================================
old_branch_violation = """### GIT BRANCH VIOLATION
If you discover you are on `main`/`master` or a non-`feature/` branch:
1. **Do not proceed with file operations.**
2. Stash any in-progress work: `git stash --include-untracked`
3. Create feature branch: `git checkout -b feature/<descriptive-name>`
4. Restore work: `git stash pop`
5. Verify: `git branch --show-current`
6. Resume work ONLY after confirming feature branch."""

new_branch_violation = """### GIT BRANCH VIOLATION
If you discover you are on `main`/`master` or a non-`feature/` branch:
1. **Do not proceed with file operations.**
2. **Check stash stack and worktree:**
   - `git stash list` \u2192 Note how many stash entries exist (baseline count).
   - `git status --short` \u2192 Is the worktree dirty?
   - **If worktree is CLEAN:** skip to step 4. Do NOT stash \u2014 there is nothing to save, and `git stash pop` will restore the wrong entry.
   - **If worktree is DIRTY:** `git stash push -m "pre-branch-switch-<feature-name>" --include-untracked`
3. **Verify stash was created:** `git stash list` \u2192 Count should be baseline+1. If not, the stash failed \u2014 investigate before proceeding.
4. Create feature branch: `git checkout -b feature/<descriptive-name>`
5. Restore work (ONLY if you stashed in step 2):
   - `git stash list` \u2192 Identify your stash entry by its message.
   - `git stash pop` \u2192 If this triggers merge conflicts from a wrong stash entry, see Section 9.7 (Stash Pop Contamination).
   - **If you did NOT stash** (worktree was clean): skip this step.
6. Verify: `git branch --show-current`
7. Resume work ONLY after confirming feature branch."""

if old_branch_violation in content:
    content = content.replace(old_branch_violation, new_branch_violation)
    changes += 1
    print('[OK] GAP 1+6: Section 8 GIT BRANCH VIOLATION fixed')
else:
    print('[FAIL] GAP 1+6: old text not found')
    idx = content.find('### GIT BRANCH VIOLATION')
    if idx >= 0:
        print(f'  Found at {idx}: {repr(content[idx:idx+200])}')

# ============================================================
# GAP 2: Fix Section 9.7 merge conflict resolution HOW-TO
# ============================================================
old_merge_conflict = """| **Merge conflict** | Git reports CONFLICT during merge/rebase | 1. Open conflicted file. 2. Resolve conflict markers. 3. `git add <file>`. 4. `git commit`. |"""

new_merge_conflict = """| **Merge conflict** | Git reports CONFLICT during merge/rebase | 1. Open each conflicted file. 2. Remove `<<<<<<<`, `=======`, `>>>>>>>` markers \u2014 choose which version to keep (current branch = between `<<<<<<<` and `=======`, incoming = between `=======` and `>>>>>>>`). 3. `git add <file>` to mark as resolved. 4. `git commit`. |"""

if old_merge_conflict in content:
    content = content.replace(old_merge_conflict, new_merge_conflict)
    changes += 1
    print('[OK] GAP 2: Merge conflict resolution improved')
else:
    print('[FAIL] GAP 2: old merge conflict text not found')

# ============================================================
# GAP 3: Add "Stash Pop Contamination" to Section 9.7 failure scenarios
# ============================================================
old_dirty_worktree = """| **Dirty worktree on branch switch** | `git status --short` shows changes when trying to switch | 1. `git stash --include-untracked`. 2. Switch/create branch. 3. `git stash pop`. |"""

new_dirty_worktree = """| **Dirty worktree on branch switch** | `git status --short` shows changes when trying to switch | 1. `git stash list` (baseline). 2. `git stash push -m \"pre-switch\" --include-untracked`. 3. `git stash list` (verify +1). 4. Switch/create branch. 5. `git stash pop` (verify message matches). |"""

if old_dirty_worktree in content:
    content = content.replace(old_dirty_worktree, new_dirty_worktree)
    changes += 1
    print('[OK] GAP 3: Dirty worktree procedure updated with stash list checks')
else:
    print('[FAIL] GAP 3: old dirty worktree text not found')

# Add Stash Pop Contamination as a new row in Section 9.7
old_detached_head = """| **Detached HEAD** | `git branch --show-current` returns nothing or error | `git checkout -b feature/recovery` to attach to new branch. |"""

new_stash_row = """| **Detached HEAD** | `git branch --show-current` returns nothing or error | `git checkout -b feature/recovery` to attach to new branch. |
| **Stash pop restores wrong work** | `git stash pop` triggers merge conflicts from a pre-existing stash entry (not your own) | 1. `git merge --abort` (or `git reset --merge`). 2. `git stash list` to identify the offending entry. 3. `git stash drop stash@{N}` to remove it. 4. Verify worktree clean with `git status --short`. 5. Resume work. **Prevention:** Always check `git stash list` before/after `git stash push`; only `git stash pop` if the count increased by exactly 1. |"""

if old_detached_head in content:
    content = content.replace(old_detached_head, new_stash_row)
    changes += 1
    print('[OK] GAP 3: Stash Pop Contamination scenario added')
else:
    print('[FAIL] GAP 3: old Detached HEAD text not found')

# ============================================================
# GAP 5: Add multi-file commit format to Section 9.6
# ============================================================
old_commit_format = """- **ACTION:** CREATE (new file), EDIT (modified existing), DELETE (removed file)
- **FILE:** Path relative to repo root
- **RATIONALE:** Why this change was made (one sentence)"""

new_commit_format = """- **ACTION:** CREATE (new file), EDIT (modified existing), DELETE (removed file)
- **FILE:** Path relative to repo root. For multi-file commits, use FILES: and comma-separate paths.
- **RATIONALE:** Why this change was made (one sentence)

**Single-file format:**
```
ACTION:[CREATE|EDIT|DELETE] FILE: <relative-path> RATIONALE:<brief-reason>
```

**Multi-file format (use only when files are logically inseparable):**
```
ACTION:[CREATE|EDIT|DELETE] FILES: <path1>, <path2>, <path3> RATIONALE:<brief-reason>
```"""

if old_commit_format in content:
    content = content.replace(old_commit_format, new_commit_format)
    changes += 1
    print('[OK] GAP 5: Multi-file commit format added')
else:
    print('[FAIL] GAP 5: old commit format text not found')

# ============================================================
# GAP 4: Add stash list guidance to Section 9.5 transition procedure
# ============================================================
old_transition = """- **Transition procedure for non-`feature/` branch:** `git stash` \u2192 `git checkout -b feature/<name>` \u2192 `git stash pop`"""

new_transition = """- **Transition procedure for non-`feature/` branch:**
  1. `git stash list` \u2192 Record baseline count.
  2. **If worktree is dirty:** `git stash push -m \"migrate-to-feature-<name>\" --include-untracked`
  3. **If worktree is clean:** skip stash (nothing to save).
  4. `git checkout -b feature/<name>`
  5. **If you stashed:** `git stash list` \u2192 verify count increased by 1, then `git stash pop`.
  6. **If you did NOT stash:** proceed directly."""

if old_transition in content:
    content = content.replace(old_transition, new_transition)
    changes += 1
    print('[OK] GAP 4: Section 9.5 transition procedure updated')
else:
    print('[FAIL] GAP 4: old transition text not found')

# Write
with open('DEFAULT.md', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n[DONE] Applied {changes}/6 gap fixes. File size: {len(content)} chars')
