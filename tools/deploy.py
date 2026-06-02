#!/usr/bin/env python3
"""
deploy.py -- Sync canonical skills and configs to the DeepChat runtime.

Only deploys skills (.md files in skills/) and config files (mcp-settings.json,
acp_agents.json, model-config.json). These are separate files that DeepChat reads
at runtime and CAN be safely synced.

System prompts (DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT-DEEPSEEK.md) and
templates (templates/*.md) are NOT deployed -- they must be imported through
DeepChat's UI. The prompts.json file in the repo root is the import file
for both system prompts and templates.

Usage:
  python tools/deploy.py              # Deploy skills + configs
  python tools/deploy.py --dry-run    # Show what would change
  python tools/deploy.py --skills-only  # Deploy only skills
  python tools/deploy.py --config-only  # Deploy only config files

v2.0 -- 2026-06-02: Removed system prompt and template sync (DeepChat UI only).
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path

# --- Paths ------------------------------------------------------------
CANONICAL_ROOT = Path(__file__).resolve().parent.parent  # prompts/
APPDATA = Path(os.environ.get("APPDATA", ""))
if not APPDATA.exists():
    APPDATA = Path(os.path.expandvars(r"%APPDATA%"))
DEEPCHAT_DIR = APPDATA / "DeepChat"
DEEPCHAT_SKILLS = DEEPCHAT_DIR / "skills"

# Only configs we can safely deploy (separate files, not DeepChat-managed state)
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

def read_file(path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

# =====================================================================
# SKILL DEPLOYMENT (works -- separate .md files, not settings)
# =====================================================================

def deploy_skills(dry_run=False):
    """Sync canonical skills/ to DeepChat skills/ directory."""
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
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        canonical = read_file(skill_md)
        if canonical is None:
            continue

        deployed_dir = DEEPCHAT_SKILLS / skill_name
        deployed_md = deployed_dir / "SKILL.md"

        if deployed_md.exists():
            deployed = read_file(deployed_md)
            if deployed and hash_content(canonical) == hash_content(deployed):
                results[skill_name] = "UNCHANGED"
                continue
            if dry_run:
                results[skill_name] = "WOULD_UPDATE"
                continue

        if dry_run:
            results[skill_name] = "WOULD_INSTALL"
            continue

        write_file(deployed_md, canonical)
        results[skill_name] = "UPDATED" if deployed_md.exists() else "INSTALLED"

    return results

# =====================================================================
# CONFIG DEPLOYMENT (works -- separate JSON files)
# =====================================================================

def deploy_configs(dry_run=False):
    """Sync canonical config files to DeepChat config directory."""
    results = {}
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
        description="Deploy canonical skills and configs to DeepChat runtime"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skills-only", action="store_true")
    parser.add_argument("--config-only", action="store_true")
    args = parser.parse_args()

    run_all = not (args.skills_only or args.config_only)
    dry = args.dry_run

    print("=" * 60)
    print("DEPLOY -- Canonical -> DeepChat Runtime (v2.0)")
    print(f"Source: {CANONICAL_ROOT}")
    print(f"Mode: {'DRY RUN' if dry else 'LIVE'}")
    print("=" * 60)

    if run_all or args.skills_only:
        print("\n--- Skills ---")
        results = deploy_skills(dry_run=dry)
        for skill in sorted(results.keys()):
            flag = "->" if any(w in results[skill] for w in ("UPDATE", "INSTALL")) else "  "
            print(f"  {flag} {skill}: {results[skill]}")

    if run_all or args.config_only:
        print("\n--- Configs ---")
        results = deploy_configs(dry_run=dry)
        for cfg in sorted(results.keys()):
            flag = "->" if "UPDATE" in results[cfg] else "  "
            print(f"  {flag} {cfg}: {results[cfg]}")

    if dry:
        print("\n[DRY RUN] Remove --dry-run to apply changes.")
    else:
        print("\n[DONE] Skills and configs deployed.")
        print("Note: System prompts and templates must be imported via DeepChat UI.")


if __name__ == "__main__":
    main()
