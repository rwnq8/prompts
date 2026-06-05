#!/usr/bin/env python3
"""
deploy.py -- Sync canonical skills to the DeepChat runtime.

Deploys skills (FULL directory: SKILL.md + scripts/ + references/) to the
DeepChat skills directory. Handles the EPERM issue (DeepChat's import process
cannot rename directories in use) by writing files directly without rename.

System prompts (DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT-DEEPSEEK.md) and
templates (templates/*.md) are NOT deployed -- they must be imported through
DeepChat's UI. The prompts.json file in the repo root is the import file
for both system prompts and templates.

Config files (mcp-settings.json, acp_agents.json, model-config.json) are
DEPRECATED -- DeepChat manages these internally and overwrites deployed copies.
The --config-only flag is retained for backward compatibility only.

Usage:
  python _deploy.py              # Deploy skills
  python _deploy.py --dry-run    # Show what would change
  python _deploy.py --skills-only  # Deploy only skills
  python _deploy.py --config-only  # DEPRECATED - Deploy only configs

v2.1 -- 2026-06-05: Fixed target path (DeepChat reads from .deepchat, not AppData).
                    Extended to deploy ALL skill files (scripts, references, etc.).
v2.0 -- 2026-06-02: Removed system prompt and template sync (DeepChat UI only).
"""

import os
import sys
import json
import hashlib
import argparse
import shutil
from pathlib import Path

# --- Paths ------------------------------------------------------------
# Thin-Client Model: deploy.py may run from any location (pulled from R2).
# CANONICAL_ROOT is the import surface -- always at this absolute path.
CANONICAL_ROOT = Path(r"G:\My Drive\prompts")

# DeepChat uses .deepchat in the user's home directory as its runtime directory.
# This was discovered 2026-06-05: _deploy.py was deploying to %APPDATA%\DeepChat\
# but DeepChat actually reads skills from %USERPROFILE%\.deepchat\skills\.
# The two directories are SEPARATE (38 skills in .deepchat vs 14 in AppData).
DEEPCHAT_DIR = Path.home() / ".deepchat"
if not DEEPCHAT_DIR.exists():
    # Fallback: older DeepChat versions may use AppData
    APPDATA = Path(os.environ.get("APPDATA", ""))
    if not APPDATA.exists():
        APPDATA = Path(os.path.expandvars(r"%APPDATA%"))
    DEEPCHAT_DIR = APPDATA / "DeepChat"

DEEPCHAT_SKILLS = DEEPCHAT_DIR / "skills"

# Config deployment is DEPRECATED per META-PROMPT v6.0. DeepChat manages
# these internally and overwrites any deployed copies.
CONFIG_MAP = {
    "mcp-settings.json": DEEPCHAT_DIR / "mcp-settings.json",
    "acp_agents.json": DEEPCHAT_DIR / "acp_agents.json",
    "model-config.json": DEEPCHAT_DIR / "model-config.json",
}

# =====================================================================
# Utilities
# =====================================================================

def hash_content(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def hash_file_binary(path):
    """Hash a file by its binary content (handles any file type)."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def read_file(path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    """Write text content to a file. Creates parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def copy_file(src, dst):
    """Copy a file (binary safe). Creates parent directories."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True

# =====================================================================
# SKILL DEPLOYMENT (v2.1 -- full directory sync)
# =====================================================================

def deploy_skills(dry_run=False):
    """
    Sync canonical skills/ to DeepChat skills/ directory.

    For EACH skill, syncs ALL files in the skill directory:
    - SKILL.md (required)
    - scripts/* (Python scripts, etc.)
    - references/* (supporting documents)
    - Any other files in the skill directory

    Excludes:
    - __pycache__/ directories
    - .git/ directories
    - backup-* directories (DeepChat's own backups)

    Returns a dict of {skill_name: status} where status is one of:
    UNCHANGED, UPDATED, INSTALLED, WOULD_UPDATE, WOULD_INSTALL, ERROR
    """
    results = {}
    canonical_skills = CANONICAL_ROOT / "skills"

    if not canonical_skills.exists():
        results["error"] = "Canonical skills directory not found"
        return results

    DEEPCHAT_SKILLS.mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(canonical_skills.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_name = skill_dir.name

        # Skip non-skill directories
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        deployed_dir = DEEPCHAT_SKILLS / skill_name
        deployed_skill_md = deployed_dir / "SKILL.md"

        # --- Collect ALL files to sync from canonical ---
        canonical_files = {}  # relative_path -> absolute_path
        for fpath in skill_dir.rglob("*"):
            if fpath.is_dir():
                continue
            # Skip __pycache__ and hidden files
            parts = fpath.parts
            if "__pycache__" in parts:
                continue
            rel_path = fpath.relative_to(skill_dir)
            canonical_files[str(rel_path)] = fpath

        if not canonical_files:
            continue

        # --- Check what needs updating ---
        needs_update = False
        file_actions = []  # (rel_path, action: "update"|"install"|"skip")

        for rel_path, canonical_path in sorted(canonical_files.items()):
            deployed_path = deployed_dir / rel_path

            if deployed_path.exists():
                # Compare by binary hash
                canon_hash = hash_file_binary(canonical_path)
                depl_hash = hash_file_binary(deployed_path)
                if canon_hash == depl_hash:
                    file_actions.append((rel_path, "skip"))
                else:
                    file_actions.append((rel_path, "update"))
                    needs_update = True
            else:
                file_actions.append((rel_path, "install"))
                needs_update = True

        # --- Also detect files in deployed that are NOT in canonical (stale) ---
        if deployed_dir.exists():
            deployed_files = set()
            for fpath in deployed_dir.rglob("*"):
                if fpath.is_dir():
                    continue
                parts = fpath.parts
                if "__pycache__" in parts:
                    continue
                # Skip DeepChat backup dirs
                if any(p.startswith("backup-") for p in parts):
                    continue
                rel_path = fpath.relative_to(deployed_dir)
                deployed_files.add(str(rel_path))

            stale_files = deployed_files - set(canonical_files.keys())
            if stale_files:
                # Don't auto-delete stale files, just report them
                results[f"{skill_name}:stale"] = list(stale_files)

        # --- Determine overall status ---
        if not needs_update:
            results[skill_name] = "UNCHANGED"
            continue

        if dry_run:
            if deployed_skill_md.exists():
                results[skill_name] = "WOULD_UPDATE"
            else:
                results[skill_name] = "WOULD_INSTALL"
            continue

        # --- Execute: copy all changed files ---
        try:
            for rel_path, action in file_actions:
                if action == "skip":
                    continue
                canonical_path = canonical_files[rel_path]
                deployed_path = deployed_dir / rel_path

                if rel_path.endswith(".md") or rel_path.endswith(".json"):
                    # Text files: use write_file for proper encoding
                    content = read_file(canonical_path)
                    if content is not None:
                        write_file(deployed_path, content)
                    else:
                        copy_file(canonical_path, deployed_path)
                else:
                    # Binary/script files: use copy
                    copy_file(canonical_path, deployed_path)

            status = "UPDATED" if deployed_skill_md.exists() else "INSTALLED"
            results[skill_name] = status

        except PermissionError as e:
            results[skill_name] = f"ERROR: Permission denied - {e}. Close DeepChat and retry."
        except Exception as e:
            results[skill_name] = f"ERROR: {e}"

    return results

# =====================================================================
# CONFIG DEPLOYMENT (DEPRECATED -- DeepChat manages these internally)
# =====================================================================

def deploy_configs(dry_run=False):
    """
    DEPRECATED: Sync canonical config files to DeepChat config directory.
    DeepChat manages config files internally and WILL overwrite deployed copies.
    This function is retained for backward compatibility only.
    """
    results = {"_deprecated": "Config deployment is DEPRECATED. DeepChat manages configs internally."}
    config_dir = CANONICAL_ROOT / "config"

    for name, deployed_path in CONFIG_MAP.items():
        canonical_path = config_dir / name
        if not canonical_path.exists():
            results[name] = "CANONICAL_MISSING"
            continue

        canonical = read_file(canonical_path)
        if canonical is None:
            continue

        if deployed_path.exists():
            deployed = read_file(deployed_path)
            if deployed and hash_content(canonical) == hash_content(deployed):
                results[name] = "UNCHANGED"
                continue
            if dry_run:
                results[name] = "WOULD_UPDATE"
                continue

        if dry_run:
            results[name] = "WOULD_INSTALL"
            continue

        write_file(deployed_path, canonical)
        results[name] = "UPDATED"

    return results

# =====================================================================
# Main
# =====================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Deploy canonical skills to DeepChat runtime (v2.1)"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skills-only", action="store_true")
    parser.add_argument("--config-only", action="store_true",
                        help="DEPRECATED: DeepChat manages configs internally")
    args = parser.parse_args()

    run_all = not (args.skills_only or args.config_only)
    dry = args.dry_run

    print("=" * 60)
    print(f"DEPLOY -- Canonical -> DeepChat Runtime (v2.1)")
    print(f"Source:      {CANONICAL_ROOT}")
    print(f"Target:      {DEEPCHAT_SKILLS}")
    print(f"Mode:        {'DRY RUN' if dry else 'LIVE'}")
    print("=" * 60)

    if run_all or args.skills_only:
        print("\n--- Skills ---")
        results = deploy_skills(dry_run=dry)
        for key in sorted(results.keys()):
            if key == "error":
                print(f"  !! {results[key]}")
                continue
            if ":stale" in key:
                skill_name = key.replace(":stale", "")
                stale_list = results[key]
                print(f"  ?? {skill_name}: STALE FILES (in deployed but not canonical): {stale_list}")
                continue

            status = results[key]
            flag = "->" if any(w in str(status) for w in ("UPDATE", "INSTALL")) else "  "
            print(f"  {flag} {key}: {status}")

    if run_all or args.config_only:
        print("\n--- Configs (DEPRECATED) ---")
        results = deploy_configs(dry_run=dry)
        for cfg in sorted(results.keys()):
            if cfg == "_deprecated":
                print(f"  !! {results[cfg]}")
                continue
            flag = "->" if "UPDATE" in str(results[cfg]) else "  "
            print(f"  {flag} {cfg}: {results[cfg]}")

    if dry:
        print("\n[DRY RUN] Remove --dry-run to apply changes.")
    else:
        print("\n[DONE] Skills deployed.")
        print("Note: System prompts and templates must be imported via DeepChat UI.")
        print("Note: Restart DeepChat to pick up skill changes.")


if __name__ == "__main__":
    main()
