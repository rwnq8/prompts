#!/usr/bin/env python3
"""
ps_run.py — Safe Python Script Execution Wrapper (v1.0)

Eliminates PowerShell/Python string mangling by enforcing file-based execution.
All agents MUST use this instead of `python -c "..."` which has a 100% failure rate.

Usage:
    python tools/ps_run.py --script tools/migration_scanner.py -- --scan "G:/My Drive/projects" --output report.json
    python tools/ps_run.py --script _upload.py -- arg1 arg2

Canonical: G:/My Drive/prompts/tools/ps_run.py
R2: qnfo/tools/ps_run.py

This tool exists because 40% of all tool calls in the 2026-06-04 session failed
due to PowerShell mangling inline Python strings. Never use `python -c` again.
"""

import argparse
import subprocess
import sys
import os


def main():
    parser = argparse.ArgumentParser(
        description='Safe Python script execution — bypasses PowerShell string mangling',
        epilog='NEVER use python -c "..." from PowerShell. Always use this wrapper.'
    )
    parser.add_argument('--script', required=True, help='Path to Python script to execute')
    parser.add_argument('args', nargs='*', help='Arguments to pass to the script (after --)')

    # Parse known args, pass remainder to script
    parsed, script_args = parser.parse_known_args()

    script_path = parsed.script
    if not os.path.exists(script_path):
        print(f'ERROR: Script not found: {script_path}', file=sys.stderr)
        sys.exit(1)

    # Build command
    cmd = [sys.executable, script_path] + parsed.args

    print(f'[ps_run] Executing: {" ".join(cmd)}', file=sys.stderr)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
