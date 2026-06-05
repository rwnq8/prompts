#!/usr/bin/env python3
"""
deepchat_hooks.py — DeepChat Lifecycle Hook Dispatcher (v1.0)

DESIGNED FOR: DeepChat Hook configuration UI
  Command: python "G:\My Drive\prompts\hooks\deepchat_hooks.py" {{event}} {{conversationId}}
  Events: ALL 8 lifecycle events recommended
  Stdin: JSON payload from DeepChat

For each lifecycle event, this script:
  - Parses stdin JSON payload + environment variables
  - Routes to the appropriate handler
  - Logs JSON to audit/hooks/<conversationId>/
  - Maintains execution statistics for Kaizen engine
  - Detects anti-loop patterns (3x same tool+error → alert)

Events handled: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse,
                ToolUseFailure, PermissionRequest, Stop, SessionEnd
"""

import os, sys, json, time, hashlib
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────
HOOKS_AUDIT_DIR = Path(r"G:\My Drive\prompts\audit\hooks")
MAX_LOG_FILES = 100  # Per conversation
FAILURE_TRACKER_FILE = HOOKS_AUDIT_DIR / "_failure_tracker.json"

# ── Helpers ────────────────────────────────────────────────────────
def load_stdin_payload():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}

def get_env_info():
    return {
        "event": os.environ.get("DEEPCHAT_HOOK_EVENT", "unknown"),
        "time": os.environ.get("DEEPCHAT_HOOK_TIME", datetime.now(timezone.utc).isoformat()),
        "conversation_id": os.environ.get("DEEPCHAT_CONVERSATION_ID", "unknown"),
        "workdir": os.environ.get("DEEPCHAT_WORKDIR", ""),
        "agent_id": os.environ.get("DEEPCHAT_AGENT_ID", ""),
        "model_id": os.environ.get("DEEPCHAT_MODEL_ID", ""),
        "tool_name": os.environ.get("DEEPCHAT_TOOL_NAME", ""),
        "tool_call_id": os.environ.get("DEEPCHAT_TOOL_CALL_ID", ""),
        "is_test": os.environ.get("DEEPCHAT_HOOK_IS_TEST", "false") == "true",
    }

def get_session_dir(conversation_id):
    safe_id = conversation_id[:32] if len(conversation_id) > 32 else conversation_id
    session_dir = HOOKS_AUDIT_DIR / safe_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

def write_event_log(session_dir, event_name, data):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    log_file = session_dir / f"{timestamp}_{event_name}.json"
    existing = sorted(session_dir.glob("*.json"))
    while len(existing) >= MAX_LOG_FILES and existing:
        try:
            existing[0].unlink()
            existing.pop(0)
        except Exception:
            break
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    return log_file

# ── Event Handlers ─────────────────────────────────────────────────
def on_session_start(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    data = {
        "hook_version": "1.0", "event": "SessionStart",
        "conversation_id": conv_id, "timestamp": env["time"],
        "agent_id": env["agent_id"], "model_id": env["model_id"],
        "workdir": env["workdir"], "is_test": env["is_test"],
        "session_started": datetime.now(timezone.utc).isoformat(),
    }
    write_event_log(session_dir, "SessionStart", data)
    meta_file = session_dir / "_session_meta.json"
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump({"started": data["timestamp"], "conversation_id": conv_id,
                   "agent_id": env["agent_id"], "model_id": env["model_id"],
                   "tool_count": 0, "failure_count": 0, "status": "active"}, f, indent=2)
    print(f"[HOOK] Session started: {conv_id[:8]}...")

def on_user_prompt_submit(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    data = {"event": "UserPromptSubmit", "conversation_id": conv_id,
            "timestamp": env["time"], "message_id": os.environ.get("DEEPCHAT_MESSAGE_ID", "")}
    write_event_log(session_dir, "UserPromptSubmit", data)

def on_pre_tool_use(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    data = {"event": "PreToolUse", "conversation_id": conv_id,
            "timestamp": env["time"], "tool_name": env["tool_name"],
            "tool_call_id": env["tool_call_id"], "payload": payload.get("tool", {})}
    write_event_log(session_dir, "PreToolUse", data)

def on_post_tool_use(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    data = {"event": "PostToolUse", "conversation_id": conv_id,
            "timestamp": env["time"], "tool_name": env["tool_name"],
            "tool_call_id": env["tool_call_id"], "payload": payload.get("tool", {})}
    write_event_log(session_dir, "PostToolUse", data)
    meta_file = session_dir / "_session_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
            meta["tool_count"] = meta.get("tool_count", 0) + 1
            meta["last_tool"] = env["tool_name"]
            meta["last_activity"] = env["time"]
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
        except Exception:
            pass

def on_tool_failure(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    error_msg = str(payload.get("error", payload.get("tool", {}).get("error", "unknown")))[:200]
    data = {"event": "ToolUseFailure", "conversation_id": conv_id,
            "timestamp": env["time"], "tool_name": env["tool_name"],
            "tool_call_id": env["tool_call_id"], "payload": payload.get("tool", {}),
            "error": error_msg}
    write_event_log(session_dir, "ToolUseFailure", data)
    meta_file = session_dir / "_session_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
            meta["failure_count"] = meta.get("failure_count", 0) + 1
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
        except Exception:
            pass
    track_failure(env["tool_name"], error_msg, conv_id)

def on_permission_request(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    data = {"event": "PermissionRequest", "conversation_id": conv_id,
            "timestamp": env["time"], "payload": payload.get("permission", {})}
    write_event_log(session_dir, "PermissionRequest", data)

def on_stop(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    data = {"event": "Stop", "conversation_id": conv_id, "timestamp": env["time"]}
    write_event_log(session_dir, "Stop", data)

def on_session_end(payload, env):
    conv_id = env["conversation_id"]
    session_dir = get_session_dir(conv_id)
    data = {"event": "SessionEnd", "conversation_id": conv_id,
            "timestamp": env["time"], "session_ended": datetime.now(timezone.utc).isoformat()}
    write_event_log(session_dir, "SessionEnd", data)
    meta_file = session_dir / "_session_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
            meta["ended"] = data["session_ended"]
            meta["status"] = "closed"
            event_counts = {}
            for f_path in session_dir.glob("*.json"):
                if f_path.name.startswith("_"):
                    continue
                try:
                    with open(f_path, 'r') as f:
                        evt = json.load(f)
                    event_counts[evt.get("event", "unknown")] = event_counts.get(evt.get("event", "unknown"), 0) + 1
                except Exception:
                    pass
            meta["event_counts"] = event_counts
            tools = event_counts.get("PostToolUse", 0)
            prompts = event_counts.get("UserPromptSubmit", 0)
            meta["execution_ratio"] = round(tools / max(prompts, 1), 3)
            meta["severity"] = "CRITICAL" if meta["execution_ratio"] < 0.3 else ("WARN" if meta["execution_ratio"] < 0.5 else "OK")
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
        except Exception:
            pass
    cleanup_old_audits()
    print(f"[HOOK] Session ended: {conv_id[:8]}...")

# ── Failure Tracker ────────────────────────────────────────────────
def track_failure(tool_name, error_msg, conv_id):
    try:
        tracker = {}
        if FAILURE_TRACKER_FILE.exists():
            with open(FAILURE_TRACKER_FILE, 'r') as f:
                tracker = json.load(f)
        sig_input = f"{tool_name}|{error_msg[:100]}|{conv_id}"
        sig = hashlib.md5(sig_input.encode()).hexdigest()[:12]
        if sig not in tracker:
            tracker[sig] = {"count": 0, "first_seen": datetime.now(timezone.utc).isoformat()}
        tracker[sig]["count"] += 1
        tracker[sig]["last_seen"] = datetime.now(timezone.utc).isoformat()
        tracker[sig]["tool"] = tool_name
        tracker[sig]["error"] = error_msg[:200]
        if tracker[sig]["count"] >= 3:
            print(f"[HOOK-ALERT] Anti-loop: {tool_name} failed {tracker[sig]['count']}x — escalate!")
        with open(FAILURE_TRACKER_FILE, 'w') as f:
            json.dump(tracker, f, indent=2)
    except Exception:
        pass

def cleanup_old_audits():
    try:
        dirs = sorted(HOOKS_AUDIT_DIR.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
        for old_dir in dirs[20:]:
            if old_dir.name.startswith("_"):
                continue
            for f in old_dir.glob("*"):
                try:
                    f.unlink()
                except Exception:
                    pass
            try:
                old_dir.rmdir()
            except Exception:
                pass
    except Exception:
        pass

# ── Main Dispatcher ────────────────────────────────────────────────
HANDLERS = {
    "SessionStart": on_session_start, "UserPromptSubmit": on_user_prompt_submit,
    "PreToolUse": on_pre_tool_use, "PostToolUse": on_post_tool_use,
    "ToolUseFailure": on_tool_failure, "PermissionRequest": on_permission_request,
    "Stop": on_stop, "SessionEnd": on_session_end,
}

def main():
    event_name = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DEEPCHAT_HOOK_EVENT", "")
    if not event_name:
        print("[HOOK-ERROR] No event specified", file=sys.stderr)
        sys.exit(1)
    payload = load_stdin_payload()
    env = get_env_info()
    handler = HANDLERS.get(event_name)
    if handler:
        try:
            handler(payload, env)
        except Exception as e:
            print(f"[HOOK-ERROR] Handler for {event_name} failed: {e}", file=sys.stderr)
    else:
        print(f"[HOOK-WARN] No handler for: {event_name}", file=sys.stderr)
        conv_id = env.get("conversation_id", "unknown")
        data = {"event": event_name, "timestamp": env["time"], "raw_payload": payload}
        write_event_log(get_session_dir(conv_id), event_name, data)

if __name__ == "__main__":
    main()
