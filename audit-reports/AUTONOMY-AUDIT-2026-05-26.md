# Autonomy & Tooling Audit — 2026-05-26

**Source:** Conversation log: `export_deepchat_2026-05-26_07-59-13.md` (82 messages, beginners-guide-blueprint project)
**Scope:** Projects Agent + DEFAULT.md system prompt audit
**Status:** IN PROGRESS

---

## FINDING 1 [CRITICAL]: Semi-Autonomous Progression Mode Causes Excessive Pausing

### Evidence
The completion report template in DEFAULT.md includes:
```
SAY "RESUME" TO CONTINUE with the next task.
```

This caused the agent to PAUSE after EVERY task and wait for user to type "RESUME":
- Line 4707: "SAY 'RESUME' TO CONTINUE with next steps"
- Line 5257: "SAY 'RESUME' TO CONTINUE to Chapter 1"
- Line 6190: "SAY 'RESUME' TO CONTINUE to the next task"
- Line 10486: "SAY 'RESUME' TO CONTINUE"
- Line 10809: "SAY 'RESUME' TO CONTINUE to Part II"
- Line 10944: "SAY 'RESUME' TO CONTINUE to Part III"
- Line 11012: "SAY 'RESUME' TO CONTINUE to Part IV"
- Line 11154: "SAY 'RESUME' TO CONTINUE to Part V"
- Line 13620: "SAY 'RESUME' or 'FIX' to apply..."

**9 explicit pauses in one session.** The agent also says "I need your direction" (line 1211).

### Root Cause
DEFAULT.md Section 13 (Semi-Autonomous Progression Mode) is designed to PAUSE after every task as a safety mechanism. The RESUME trigger was intended as an acceleration layer but became a bottleneck.

### Fix
- RESUME becomes the DEFAULT behavior — agent auto-continues through tasks
- RESUME command only needed after interruptions or user-initiated pauses
- Remove "I need your direction" pattern — agent self-directs

---

## FINDING 2 [CRITICAL]: GitHub Repos Default to rwnq8 Instead of qnfo

### Evidence
Line 16456: "Actually, I'll create a repo under `rwnq8` since that's the authenticated user, and the QNFO org might have..."

User feedback (line 16616): "ALSO, WHY ARE THESE REPOS BEING CREATED IN RWNQ8 WHEN QNFO SHOULD BE DEFAULT FOR ALL NEW REPOS?"

### Root Cause
- DEFAULT.md does not document `gh repo create`
- No persistent preference for default GitHub organization
- Agent defaults to `gh auth status` output

### Fix
- Add `GH_OWNER=qnfo` as persistent preference
- Document `gh repo create --org qnfo` with explicit examples

---

## FINDING 3 [HIGH]: Lack of In-Scope Autonomy

### Evidence
Line 1211: "I need your direction. The source materials are rich — 22 textbook chapters..."

Agent frequently stops to ask for direction rather than self-directing through workflow.

### Root Cause
- Phase 0 (due diligence) too lengthy, creates analysis paralysis
- Startup sequence requires reading 4+ documents before any work
- "Confirm Before Execution" in autonomous mode creates unnecessary checkpoint

### Fix
- Streamline Phase 0 — essential checks only
- Remove "Confirm Before Execution" from autonomous mode
- Agent executes immediately after identifying next task

---

## FINDING 4 [HIGH]: Archiving Is Manual

### Evidence
Close-out procedure is a manual 7-item checklist. No auto-archive trigger.

### Fix
- Auto-archive completed projects as part of P5 Close-Out
- When GitHub Release is created, automatically MOVE project to Archive

---

## FINDING 5 [MEDIUM]: PDF Not Auto-Generated for Releases

### Evidence
`pdf-release.yml` only triggers on tag push or `workflow_dispatch`. No `release` event trigger.

### Fix
- Add `release: published` trigger to pdf-release.yml
- Document auto-PDF generation in release protocol

---

## FINDING 6 [MEDIUM]: Tool/Capability Understanding Gaps

### Evidence
Agent didn't know it could use `gh repo create` autonomously.

### Fix
- Add comprehensive `gh` CLI reference to DEFAULT.md
- Document all available `gh` commands with examples

---

## FINDING 7 [LOW]: PowerShell gh stderr Confusion

### Evidence
Agent treated successful `gh` commands as errors due to PowerShell exit code confusion.

### Fix
- Document PowerShell `gh` stderr quirk
- Instruct agent to check actual output content, not just exit codes

---

## REFACTOR PLAN

### Files to Modify:
1. **DEFAULT.md** — Sections: §0 (GH_OWNER), §0.6.8 (gh repo create), §13 (auto-continue), Close-out (auto-archive)
2. **PROJECTS-AGENT.md** — §8 (streamline startup), §9 (auto-archive), §2 (autonomy mandate), §3 (gh CLI)
3. **pdf-release.yml** — Add `release: published` trigger

### Target Outcomes:
- Agent auto-continues through tasks without pausing for RESUME
- New repos default to `qnfo` organization
- Agent self-directs without "I need your direction"
- Archiving happens automatically on close-out
- PDFs auto-generated when releases are published
- Agent fully understands gh CLI capabilities
