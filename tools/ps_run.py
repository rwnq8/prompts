#!/usr/bin/env python3
"""
ps_run.py — Safe Python Script Execution Bridge for PowerShell (v1.0)

Solves the PowerShell-Python quoting boundary problem that makes `python -c "..."`
unreliable. PowerShell intercepts <, >, $, {, }, (), |, backticks and nested quotes
BEFORE Python receives them.

Usage (from PowerShell):
    python ps_run.py script.py arg1 arg2          # Run a script with args
    python ps_run.py -c "print('hello')"          # Inline code (careful — use -c for trivial)
    python ps_run.py --stdin < script.py          # Read script from stdin

This tool is the ONLY safe way to call Python from PowerShell when the code contains
special characters common in Python (f-strings, comparisons, dict literals, etc.).
"""

import sys
import os
import subprocess
import tempfile

def run_file(script_path, args):
    """Execute a Python script file with given arguments."""
    if not os.path.exists(script_path):
        print(f"[ERROR] Script not found: {script_path}")
        sys.exit(1)
    
    cmd = [sys.executable, script_path] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    sys.exit(result.returncode)

def run_inline(code):
    """Execute inline Python code safely."""
    # Write to temp file to avoid PowerShell quoting issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_path = f.name
    
    try:
        result = subprocess.run([sys.executable, temp_path], capture_output=True, text=True)
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        sys.exit(result.returncode)
    finally:
        os.unlink(temp_path)

def run_stdin():
    """Execute Python code from stdin."""
    code = sys.stdin.read()
    if code.strip():
        run_inline(code)
    else:
        print("[ERROR] No code provided on stdin")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python ps_run.py <script.py> [args...]")
        print("       python ps_run.py -c '<code>'")
        print("       python ps_run.py --stdin < script.py")
        sys.exit(1)
    
    if sys.argv[1] == '-c' and len(sys.argv) > 2:
        run_inline(sys.argv[2])
    elif sys.argv[1] == '--stdin':
        run_stdin()
    else:
        run_file(sys.argv[1], sys.argv[2:])

if __name__ == "__main__":
    main()
