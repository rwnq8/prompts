# DEEPCHAT HOOKS REFERENCE — Configuration Guide

> **Date:** 2026-06-05 | **Version:** 1.0

## Overview

DeepChat supports lifecycle hooks — custom commands that fire on 8 lifecycle events. This enables automated auditing, execution tracking, failure detection, and session cleanup.

## Events

| Event | Fires When |
|:------|:----------|
| Session Start | New conversation created |
| User Prompt Submit | User sends a message |
| Pre Tool Use | Tool is about to be invoked |
| Post Tool Use | Tool completed successfully |
| Tool Use Failure | Tool returned an error |
| Permission Request | DeepChat asks for permission |
| Stop | Agent stopped mid-generation |
| Session End | Conversation closed |

## Setup

### 1. Hook Scripts Location

All scripts are in `G:\My Drive\prompts\hooks\`:
- `deepchat_hooks.py` — Unified dispatcher (handles ALL events)
- `on_session_start.py` — SessionStart only
- `on_post_tool.py` — PostToolUse only  
- `on_tool_failure.py` — ToolUseFailure only
- `on_session_end.py` — SessionEnd only

### 2. Configure in DeepChat UI

Settings → Hooks → New Hook:

| Field | Value |
|:------|:------|
| Name | QNFO Session Tracker |
| Command | `python "G:\My Drive\prompts\hooks\deepchat_hooks.py" {{event}} {{conversationId}}` |
| Events | ✅ ALL 8 events |

### 3. Test

Click **Test** to verify. Check `G:\My Drive\prompts\audit\hooks\` for output.

## Stdin JSON

Every event writes JSON to stdin:
```json
{
  "event": "PostToolUse",
  "time": "2026-06-05T10:00:00.000Z",
  "session": {"conversationId": "abc123", "workdir": "G:\\..."},
  "tool": {"name": "exec", "callId": "xyz789"}
}
```

## Environment Variables

| Variable | Events |
|:---------|:-------|
| `DEEPCHAT_HOOK_EVENT` | All |
| `DEEPCHAT_CONVERSATION_ID` | All |
| `DEEPCHAT_TOOL_NAME` | Pre/Post/Failure |
| `DEEPCHAT_TOOL_CALL_ID` | Pre/Post/Failure |

## Audit Output

Session data is logged to `audit\hooks\<conversationId>\`:
- `_session_meta.json` — tool_count, execution_ratio, severity
- `*_PostToolUse.json` — Per-tool invocation logs
- `*_SessionEnd.json` — Computed statistics
- `_failure_tracker.json` — Cross-session anti-loop detector

## PLATFORM-GAPS Status

| Gap | Before | After |
|:----|:-------|:------|
| Response Interception | CRITICAL | PARTIAL (track, can't block) |
| Scheduled Polling | HIGH | RESOLVED |
| Per-Session Audit | MEDIUM | RESOLVED |

---

*HOOKS-REFERENCE.md v1.0*
