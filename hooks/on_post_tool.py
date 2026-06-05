#!/usr/bin/env python3
"""on_post_tool.py — PostToolUse hook (standalone or called by dispatcher)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deepchat_hooks import load_stdin_payload, get_env_info, on_post_tool_use
payload = load_stdin_payload()
env = get_env_info()
on_post_tool_use(payload, env)
