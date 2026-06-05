# SETUP-HOOKS.md — DeepChat Hooks Configuration Guide

> **Date:** 2026-06-05 | **Version:** 1.0

## Pre-Flight Check

Verify hook scripts exist:
```powershell
Get-ChildItem "G:\My Drive\prompts\hooks\deepchat_hooks.py"
```
If missing, pull from R2 first. Scripts are committed to git in `hooks/`.

---

## Step 1: Open DeepChat Settings → Hooks

1. Click the ⚙️ Settings icon (bottom-left)
2. Navigate to **Hooks** section
3. Click **New Hook**

---

## Step 2: Configure the Hook

Copy-paste these values EXACTLY:

| Field | Value |
|:------|:------|
| **Name** | `QNFO Session Tracker` |
| **Command** | `python "G:\My Drive\prompts\hooks\deepchat_hooks.py" {{event}} {{conversationId}}` |
| **Enabled** | ✅ ON |

**Check ALL 8 events:**
- ☑ Session Start
- ☑ User Prompt Submit
- ☑ Pre Tool Use
- ☑ Post Tool Use
- ☑ Tool Use Failure
- ☑ Permission Request
- ☑ Stop
- ☑ Session End

---

## Step 3: Test

1. Click the **Test** button (▶)
2. Verify output shows: `[HOOK] Session started: ...`
3. Check audit directory exists:
   ```powershell
   Get-ChildItem "G:\My Drive\prompts\audit\hooks"
   ```

---

## Step 4: Verify After Next Session

After your next conversation:
1. Open `G:\My Drive\prompts\audit\hooks\<conversationId>\_session_meta.json`
2. Verify `tool_count`, `execution_ratio`, and `severity` are populated

---

## Troubleshooting

| Problem | Fix |
|:--------|:----|
| Hook doesn't fire | Check "Enabled" toggle is ON |
| `python not found` | Use full path: `C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\python.exe` |
| Permission error | Ensure `G:\My Drive\prompts\audit\hooks\` exists and is writable |
| No SessionEnd data | Close conversation normally (don't force-quit) |

---

## What Each Event Does

| Event | Action |
|:------|:-------|
| **Session Start** | Creates `_session_meta.json` with `tool_count=0`, logs agent/model |
| **User Prompt Submit** | Logs user message for prompt:tool ratio |
| **Pre Tool Use** | Logs pending tool invocation |
| **Post Tool Use** | Increments `tool_count`, logs tool name + call ID |
| **Tool Use Failure** | Tracks errors, detects 3x same pattern → `[HOOK-ALERT]` |
| **Permission Request** | Logs permission requests |
| **Stop** | Logs mid-generation stop |
| **Session End** | Computes `execution_ratio`, `severity` (OK/WARN/CRITICAL), runs cleanup |

---

*SETUP-HOOKS.md v1.0 — Copy-paste ready. Configure once, runs forever.*
