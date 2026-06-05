#!/usr/bin/env python3
"""
execution_audit.py — Post-Hoc Execution Fidelity Analyzer (v1.0)

Analyzes exported DeepChat conversation files to compute plan:execution ratios.
Detects sessions where agents produced text instead of invoking tools.

Usage:
    python execution_audit.py <conversation_export.md>
    python execution_audit.py --dir <exports_directory>
    python execution_audit.py --latest  # Analyze most recent export

Output:
    - EXECUTION RATIO: tool invocations / total responses
    - PLANNING SPIRAL COUNT: sequences of 3+ text-only responses
    - BANNED WORD COUNT: "done"/"complete"/"finished" without evidence
    - CONTINUATION TAG COMPLIANCE: % of responses with [AUTO-CONTINUE]/[ALL TASKS EXECUTED]/[BLOCKED]
    - SEVERITY: PASS / WARN / FAIL

Signals for Kaizen engine:
    - ratio < 0.4: HIGH severity — planning spiral
    - ratio < 0.6: MEDIUM severity — borderline
    - banned words > 5 in session: LOW/MEDIUM severity
"""

import re
import os
import sys
import json
import argparse
from datetime import datetime

# ── Analysis Patterns ─────────────────────────────────────────────
TOOL_INVOCATION_PATTERN = re.compile(
    r'<invoke name="[^"]+">|## (execute|write|edit|exec|process|subagent|deploy|git\b)',
    re.IGNORECASE
)

USER_MESSAGE_PATTERN = re.compile(r'## \S+ (?:用户|User)\b')
ASSISTANT_MESSAGE_PATTERN = re.compile(r'## \S+ (?:助手|Assistant)\b|### \S+ (?:思考|Thinking)')

BANNED_WORDS = [
    r'\b(done)\b(?!.*\[EXECUTED\])',
    r'\b(complete[d]?)\b(?!.*\[EXECUTED\])', 
    r'\b(finished)\b(?!.*\[EXECUTED\])',
    r'\b(successfully)\b',
    r"I'll\s+\w+",
    r"Let me\s+\w+",
]

CONTINUATION_TAG_PATTERN = re.compile(
    r'\[AUTO-CONTINUE|\[ALL TASKS EXECUTED|\[BLOCKED:'
)

EXECUTE_DEMAND_PATTERN = re.compile(
    r'\b(EXECUTE|RESUME|PROCEED|HANDOFF|CONTINUE)\b',
    re.IGNORECASE
)


def analyze_conversation(filepath):
    """Analyze a single conversation export file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find user and assistant turns
    user_turns = []
    assistant_turns = []
    
    # Split by common export formats
    sections = re.split(r'(## 👤 用户|## 🤖 助手|## 👤 User|## 🤖 Assistant)', content)[1:]
    
    current_role = None
    for i in range(0, len(sections), 2):
        role_label = sections[i]
        text = sections[i+1] if i+1 < len(sections) else ''
        if '用户' in role_label or 'User' in role_label:
            user_turns.append(text)
        else:
            assistant_turns.append(text)
    
    total_responses = len(assistant_turns)
    total_user = len(user_turns)
    
    # Count tool invocations
    tool_invocations = 0
    tool_responses = 0
    for text in assistant_turns:
        tools = len(TOOL_INVOCATION_PATTERN.findall(text))
        tool_invocations += tools
        if tools > 0:
            tool_responses += 1
    
    # Count banned words
    banned_count = 0
    for text in assistant_turns:
        for pattern in BANNED_WORDS:
            banned_count += len(re.findall(pattern, text, re.IGNORECASE))
    
    # Count continuation tags
    tag_count = len(CONTINUATION_TAG_PATTERN.findall(content))
    
    # Detect planning spirals (3+ consecutive text-only responses)
    planning_spirals = 0
    consecutive_text_only = 0
    for text in assistant_turns:
        has_tools = bool(TOOL_INVOCATION_PATTERN.search(text))
        if not has_tools:
            consecutive_text_only += 1
            if consecutive_text_only == 3:
                planning_spirals += 1
        else:
            consecutive_text_only = 0
    
    # Count user EXECUTE demands
    execute_demands = 0
    for text in user_turns:
        execute_demands += len(EXECUTE_DEMAND_PATTERN.findall(text[:300]))
    
    # Calculate metrics
    tool_ratio = tool_responses / total_responses if total_responses > 0 else 0
    tag_compliance = tag_count / total_responses if total_responses > 0 else 0
    
    # Determine severity
    if tool_ratio < 0.3:
        severity = "CRITICAL"
    elif tool_ratio < 0.5:
        severity = "HIGH"
    elif tool_ratio < 0.7:
        severity = "MEDIUM"
    else:
        severity = "OK"
    
    return {
        "file": os.path.basename(filepath),
        "total_user_messages": total_user,
        "total_assistant_responses": total_responses,
        "tool_invocations": tool_invocations,
        "tool_responses": tool_responses,
        "text_only_responses": total_responses - tool_responses,
        "execution_ratio": round(tool_ratio, 3),
        "planning_spirals": planning_spirals,
        "banned_words": banned_count,
        "continuation_tag_compliance": round(tag_compliance, 3),
        "user_execute_demands": execute_demands,
        "severity": severity,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze DeepChat exports for execution fidelity")
    parser.add_argument("file", nargs="?", help="Conversation export .md file")
    parser.add_argument("--dir", help="Directory of export files")
    parser.add_argument("--latest", action="store_true", help="Analyze most recent export")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    files = []
    if args.file:
        files = [args.file]
    elif args.dir:
        files = [os.path.join(args.dir, f) for f in os.listdir(args.dir) 
                 if f.endswith('.md') and 'export' in f.lower()]
    elif args.latest:
        downloads = os.path.expanduser(r"~\Downloads")
        candidates = [os.path.join(downloads, f) for f in os.listdir(downloads) 
                      if f.startswith('export_deepchat') and f.endswith('.md')]
        if candidates:
            files = [max(candidates, key=os.path.getmtime)]
    
    if not files:
        print("[ERROR] No export files found. Specify --file, --dir, or --latest")
        sys.exit(1)
    
    results = []
    for f in files:
        if os.path.exists(f):
            try:
                result = analyze_conversation(f)
                results.append(result)
            except Exception as e:
                print(f"[ERROR] Failed to analyze {f}: {e}")
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"\n{'='*60}")
            print(f"EXECUTION AUDIT: {r['file']}")
            print(f"{'='*60}")
            print(f"  User messages:         {r['total_user_messages']}")
            print(f"  Assistant responses:   {r['total_assistant_responses']}")
            print(f"  Tool invocations:      {r['tool_invocations']}")
            print(f"  Text-only responses:   {r['text_only_responses']}")
            print(f"  EXECUTION RATIO:       {r['execution_ratio']:.1%}  [{r['severity']}]")
            print(f"  Planning spirals:      {r['planning_spirals']}")
            print(f"  Banned words:          {r['banned_words']}")
            print(f"  User EXECUTE demands:  {r['user_execute_demands']}")
            print(f"  Tag compliance:        {r['continuation_tag_compliance']:.1%}")
            
            if r['severity'] in ('CRITICAL', 'HIGH'):
                print(f"\n  ⚠️  {r['severity']}: {r['text_only_responses']} text-only responses with {r['tool_invocations']} tool invocations.")
                print(f"  {r['user_execute_demands']} EXECUTE demands were met with {r['text_only_responses']}/{r['total_assistant_responses']} text-only responses.")
            
            print()

if __name__ == "__main__":
    main()
