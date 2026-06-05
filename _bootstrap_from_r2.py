#!/usr/bin/env python3
"""
BOOTSTRAP FROM R2 — Pull all prompt-defining files from R2 canonical.

This script is the MINIMAL bootstrap for agents that need the QNFO prompt system.
When local files don't exist (or are stale), run this to pull everything from R2.

Usage:
  python _bootstrap_from_r2.py              # Pull all prompt files
  python _bootstrap_from_r2.py --dry-run    # Show what would be pulled
  python _bootstrap_from_r2.py --skills-only  # Pull only skills
"""
import os, sys, subprocess, json, hashlib
from pathlib import Path

R2_PREFIX = "qnfo/prompts"
LOCAL_ROOT = Path(r"G:\My Drive\prompts")

# Files and directories to pull
BOOTSTRAP_MAP = {
    "core": [
        "DEFAULT.md", "QWAV-DEFAULT.md", "META-PROMPT-DEEPSEEK.md",
        "prompts.json", "prompts_bare.json",
        "_deploy.py", "_system_audit.py",
        "PLATFORM-GAPS.md",
    ],
    "config": ["config/mcp-settings.json", "config/acp_agents.json", "config/model-config.json"],
    "architecture": [],  # Populated at runtime
}

def r2_pull(r2_path, local_path, dry_run=False):
    """Pull a single file from R2."""
    if dry_run:
        print(f"  WOULD PULL: {r2_path} -> {local_path}")
        return True
    
    cmd = ["npx", "wrangler", "r2", "object", "get", r2_path,
           "--remote", "--file", str(local_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        # Verify file was actually pulled
        if local_path.exists() and local_path.stat().st_size > 0:
            return True
        else:
            print(f"  PULLED BUT EMPTY: {r2_path}")
            return False
    else:
        # Check if it's "key does not exist" (expected for some files)
        stderr = result.stderr.strip()
        if "key does not exist" in stderr.lower():
            print(f"  NOT ON R2: {r2_path}")
            return False
        print(f"  PULL FAILED: {r2_path} — {stderr[:100]}")
        return False

def main():
    dry_run = "--dry-run" in sys.argv
    skills_only = "--skills-only" in sys.argv
    
    print("=" * 60)
    print(f"BOOTSTRAP FROM R2 — {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"Source: {R2_PREFIX}/ on qnfo bucket")
    print(f"Target: {LOCAL_ROOT}")
    print("=" * 60)
    
    # Ensure target directory exists
    if not dry_run:
        LOCAL_ROOT.mkdir(parents=True, exist_ok=True)
    
    results = {"pulled": [], "failed": [], "skipped": []}
    
    if not skills_only:
        # --- Core files ---
        print("\n--- Core Prompts ---")
        for name in BOOTSTRAP_MAP["core"]:
            r2_path = f"{R2_PREFIX}/{name}"
            local_path = LOCAL_ROOT / name
            local_path.parent.mkdir(parents=True, exist_ok=True)
            if r2_pull(r2_path, local_path, dry_run):
                results["pulled"].append(name)
            else:
                results["failed"].append(name)
        
        # --- Architecture ---
        print("\n--- Architecture ---")
        # List what's on R2
        list_cmd = ["npx", "wrangler", "r2", "object", "list", "qnfo",
                    "--prefix", f"{R2_PREFIX}/architecture/", "--remote"]
        list_result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=30)
        # Parse output for file keys
        for line in list_result.stdout.split("\n"):
            if f"{R2_PREFIX}/architecture/" in line:
                # Simple extraction - the key should be in the output
                pass
        
        # Fallback: try known architecture files
        arch_files = ["architecture/system-taxonomy.md", "architecture/agent-roles.md"]
        for name in arch_files:
            r2_path = f"{R2_PREFIX}/{name}"
            local_path = LOCAL_ROOT / name
            local_path.parent.mkdir(parents=True, exist_ok=True)
            r2_pull(r2_path, local_path, dry_run)
    
    # --- Skills ---
    print("\n--- Skills ---")
    # List skills on R2
    list_cmd = ["npx", "wrangler", "r2", "object", "list", "qnfo",
                "--prefix", f"{R2_PREFIX}/skills/", "--remote"]
    list_result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=30)
    
    skill_files = set()
    for line in list_result.stdout.split("\n"):
        if f"{R2_PREFIX}/skills/" in line:
            # Extract relative path
            parts = line.split()
            for p in parts:
                if p.startswith(f"{R2_PREFIX}/skills/"):
                    rel = p[len(f"{R2_PREFIX}/"):]
                    skill_files.add(rel)
                    break
    
    print(f"  Skills files on R2: {len(skill_files)}")
    for rel in sorted(skill_files):
        r2_path = f"{R2_PREFIX}/{rel}"
        local_path = LOCAL_ROOT / rel
        local_path.parent.mkdir(parents=True, exist_ok=True)
        if r2_pull(r2_path, local_path, dry_run):
            results["pulled"].append(rel)
        else:
            results["failed"].append(rel)
    
    # --- Templates ---
    if not skills_only:
        print("\n--- Templates ---")
        list_cmd = ["npx", "wrangler", "r2", "object", "list", "qnfo",
                    "--prefix", f"{R2_PREFIX}/templates/", "--remote"]
        list_result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=30)
        
        tmpl_files = set()
        for line in list_result.stdout.split("\n"):
            if f"{R2_PREFIX}/templates/" in line:
                parts = line.split()
                for p in parts:
                    if p.startswith(f"{R2_PREFIX}/templates/"):
                        rel = p[len(f"{R2_PREFIX}/"):]
                        tmpl_files.add(rel)
                        break
        
        print(f"  Template files on R2: {len(tmpl_files)}")
        for rel in sorted(tmpl_files):
            r2_path = f"{R2_PREFIX}/{rel}"
            local_path = LOCAL_ROOT / rel
            local_path.parent.mkdir(parents=True, exist_ok=True)
            if r2_pull(r2_path, local_path, dry_run):
                results["pulled"].append(rel)
            else:
                results["failed"].append(rel)
    
    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"RESULTS ({'DRY RUN' if dry_run else 'LIVE'})")
    print(f"  Pulled: {len(results['pulled'])}")
    print(f"  Failed: {len(results['failed'])}")
    if results["failed"]:
        print("  Failures:")
        for f in results["failed"]:
            print(f"    - {f}")
    
    if not dry_run and results["pulled"]:
        print(f"\n  To deploy skills to DeepChat:")
        print(f"    python {LOCAL_ROOT / '_deploy.py'} --skills-only")
        print(f"  Then restart DeepChat.")

if __name__ == "__main__":
    main()
