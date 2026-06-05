# SETUP.md — QNFO DeepChat Configuration Master Guide

> **Date:** 2026-06-05 | **Version:** 1.0 | **Total setup time:** ~10 minutes

---

## 0. Prerequisites

- [ ] DeepChat installed and running
- [ ] Python 3.12+ at `C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\python.exe`
- [ ] Cloudflare API token at `C:\Users\LENOVO\.cloudflare\api-token`
- [ ] Git working directory: `G:\My Drive\prompts\` (current branch: `main`)

---

## 1. System Prompts (v3.26 / v6.5)

**One-time setup.** Import into DeepChat UI:

1. DeepChat Settings → **Prompts** → Import
2. Select `prompts.json` from `G:\My Drive\prompts\`
3. Verify: **DEFAULT-DEEPSEEK v3.26**, **QWAV v3.26**, **META-PROMPT v6.5**

---

## 2. Skills Deployment

```powershell
# Pull and run deploy (skills only — configs are DeepChat-managed)
npx wrangler r2 object get qnfo/tools/deploy.py --remote --file=_deploy.py
python _deploy.py --dry-run  # Preview
python _deploy.py            # Deploy
Remove-Item _deploy.py
```

---

## 3. DeepChat Hooks (NEW — v1.0)

> **See `SETUP-HOOKS.md` for detailed UI configuration.**

**Quick setup:**

| Step | Action |
|:-----|:-------|
| 1 | Open DeepChat Settings → **Hooks** |
| 2 | Click **New Hook** |
| 3 | Name: `QNFO Session Tracker` |
| 4 | Command: `python "G:\My Drive\prompts\hooks\deepchat_hooks.py" {{event}} {{conversationId}}` |
| 5 | Check ALL 8 events |
| 6 | Click **Test**, verify output |
| 7 | Click **Save** |

**What the hooks do:**
- **SessionStart**: Initialize audit trail, track tool_count
- **PostToolUse**: Log every tool invocation (ground-truth counter)
- **ToolUseFailure**: Detect 3x same failure → [HOOK-ALERT]
- **SessionEnd**: Compute execution_ratio, severity, run cleanup

---

## 4. Windows Scheduled Tasks (NEW — v1.0)

> **Run ONCE as Administrator:**

```powershell
powershell -ExecutionPolicy Bypass -File "G:\My Drive\prompts\scheduled\setup_scheduled_tasks.ps1"
```

Creates 3 tasks:

| Task | Schedule | Purpose |
|:-----|:---------|:--------|
| **QNFO Daily Execution Audit** | Daily 6:00 AM | Analyzes conversation exports for plan:execution ratios |
| **QNFO Weekly Orphan Cleanup** | Sunday 3:00 AM | Cleans `_*` ephemeral files and `__pycache__` dirs |
| **QNFO Daily Kaizen Audit** | Daily 6:30 AM | Pulls kaizen_engine.py from R2, runs audit |

View tasks: `taskschd.msc` or `Get-ScheduledTask -TaskName "QNFO*"`

---

## 5. Pin Execution Guard Skill

> **Manual UI action required:**

1. DeepChat Settings → **Skills**
2. Find **execution-guard**
3. Click **Pin** (📌)
4. Verify: shows as "Pinned" with Priority 0 badge
5. **Pin kaizen-autonomous-update** as well

---

## 6. Verification Checklist

After completing all steps:

- [ ] **System prompts:** DEFAULT v3.26, QWAV v3.26, META-PROMPT v6.5 loaded
- [ ] **Skills:** `execution-guard` appears in pinned skills
- [ ] **Hooks:** Test button produces `[HOOK] Session started: ...` output
- [ ] **Scheduled tasks:** `Get-ScheduledTask -TaskName "QNFO*"` shows 3 tasks
- [ ] **Audit dirs exist:** `G:\My Drive\prompts\audit\hooks\` and `G:\My Drive\prompts\audit\scheduled\`
- [ ] **Tools on R2:** `fast_r2_upload.py`, `r2_list.py`, `ps_run.py`, `execution_audit.py`, `kaizen_engine.py`
- [ ] **Restart DeepChat** and start a **new conversation**

---

## 7. Post-Setup: First Session

1. Start a new conversation with DEFAULT v3.26
2. The `execution-guard` skill auto-loads (Priority 0)
3. SessionStart hook fires → creates `audit/hooks/<convId>/_session_meta.json`
4. Do some work (write, execute, commit)
5. Close conversation normally
6. Check `_session_meta.json` for `tool_count`, `execution_ratio`, `severity`

---

## Quick Reference

| Resource | Path |
|:---------|:-----|
| System prompts | `G:\My Drive\prompts\DEFAULT.md`, `QWAV-DEFAULT.md`, `META-PROMPT-DEEPSEEK.md` |
| Hook dispatcher | `G:\My Drive\prompts\hooks\deepchat_hooks.py` |
| Scheduled tasks | `G:\My Drive\prompts\scheduled\` |
| Hook audit logs | `G:\My Drive\prompts\audit\hooks\<convId>\` |
| Kaizen reports | `G:\My Drive\prompts\audit\kaizen\` |
| Execution audits | `G:\My Drive\prompts\audit\scheduled\` |
| Platform gaps | `G:\My Drive\prompts\PLATFORM-GAPS.md` |

---

*SETUP.md v1.0 — Complete DeepChat configuration in ~10 minutes*
