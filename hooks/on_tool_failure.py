#!/usr/bin/env python3
"""on_tool_failure.py — ToolUseFailure hook (standalone or called by dispatcher)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deepchat_hooks import load_stdin_payload, get_env_info, on_tool_failure
payload = load_stdin_payload()
env = get_env_info()
on_tool_failure(payload, env)
