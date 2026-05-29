#!/usr/bin/env python3
import time
"""
deploy.py -- Canonical Source -> DeepChat Runtime Deployment Pipeline

Reads canonical files from prompts/ and deploys them to the
DeepChat runtime (agent.db, app-settings.json, skills directory, config files).

REDUNDANCY: Three-way protection against platform failure
  Layer 1: GitHub (git push) -- automatic on every commit
  Layer 2: Google Drive (local canonical) -- inherent, files live here
  Layer 3: Cloudflare R2 (sync) -- via cloudflare-deployer skill

Usage:
  python tools/deploy.py              # Deploy everything
  python tools/deploy.py --dry-run    # Show what would change
  python tools/deploy.py --skills-only  # Deploy only skills
  python tools/deploy.py --prompts-only # Deploy only system prompts
  python tools/deploy.py --config-only  # Deploy only config files
  python tools/deploy.py --kaizen     # Run Kaizen + deploy

v1.1 -- 2026-05-28 (Kaizen integration)
"""

import os
import sys
import json
import sqlite3
import hashlib
import argparse
from pathlib import Path

# --- Paths ------------------------------------------------------------
CANONICAL_ROOT = Path(os.path.expandvars(r"%USERPROFILE%")) / "My Drive" / "prompts"
# Resolve to absolute if the above doesn't exist (fallback for non-standard setups)
if not CANONICAL_ROOT.exists():
    CANONICAL_ROOT = Path(r"G:\My Drive\prompts")

APPDATA = Path(os.environ.get("APPDATA", ""))
if not APPDATA.exists():
    APPDATA = Path(os.path.expandvars(r"%APPDATA%"))

DEEPCHAT_DIR = APPDATA / "DeepChat"
DEEPCHAT_SKILLS = DEEPCHAT_DIR / "skills"
AGENT_DB = DEEPCHAT_DIR / "app_db" / "agent.db"
APP_SETTINGS = DEEPCHAT_DIR / "app-settings.json"
CUSTOM_PROMPTS = DEEPCHAT_DIR / "custom_prompts.json"

# --- Agent -> System Prompt Mapping -----------------------------------
AGENT_PROMPT_MAP = {
    "Projects": CANONICAL_ROOT / "DEFAULT.md",
    "Prompts": CANONICAL_ROOT / "META-PROMPT-DEEPSEEK.md",
    "QWAV": CANONICAL_ROOT / "QWAV-DEFAULT.md",
}

# --- Config File Mapping ----------------------------------------------
CONFIG_MAP = {
    "mcp-settings.json": DEEPCHAT_DIR / "mcp-settings.json",
    "acp_agents.json": DEEPCHAT_DIR / "acp_agents.json",
    "model-config.json": DEEPCHAT_DIR / "model-config.json",
}


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
# SYSTEM PROMPT DEPLOYMENT
# =====================================================================

def deploy_system_prompts(dry_run=False):
    """Deploy system prompts from canonical .md files to agent.db."""
    results = {}

    if not AGENT_DB.exists():
        results["error"] = "agent.db not found at {}".format(AGENT_DB)
        return results

    conn = sqlite3.connect(str(AGENT_DB))
    cur = conn.cursor()

    for agent_name, canonical_path in AGENT_PROMPT_MAP.items():
        canonical = read_file(canonical_path)
        if canonical is None:
            results[agent_name] = "CANONICAL_MISSING"
            continue

        cur.execute(
            "SELECT json_extract(config_json, '$.systemPrompt') FROM agents "
            "WHERE agent_type='deepchat' AND name=?",
            (agent_name,),
        )
        row = cur.fetchone()

        if row is None:
            results[agent_name] = "AGENT_NOT_FOUND"
            continue

        current_prompt = row[0] or ""
        current_hash = hash_content(current_prompt)
        canonical_hash = hash_content(canonical)

        if current_hash == canonical_hash:
            results[agent_name] = "UNCHANGED"
            continue

        if dry_run:
            results[agent_name] = "WOULD_UPDATE ({} -> {} chars)".format(
                len(current_prompt), len(canonical)
            )
            continue

        cur.execute(
            "SELECT config_json FROM agents WHERE agent_type='deepchat' AND name=?",
            (agent_name,),
        )
        config_row = cur.fetchone()
        if config_row:
            config = json.loads(config_row[0])
            config["systemPrompt"] = canonical
            cur.execute(
                "UPDATE agents SET config_json=? WHERE agent_type='deepchat' AND name=?",
                (json.dumps(config, ensure_ascii=False), agent_name),
            )
            results[agent_name] = "UPDATED ({} -> {} chars)".format(
                len(current_prompt), len(canonical)
            )

    if not dry_run and any(v.startswith("UPDATED") for v in results.values()):
        conn.commit()

    conn.close()
    return results


# =====================================================================
# SKILL DEPLOYMENT
# =====================================================================

def deploy_skills(dry_run=False):
    """Deploy skills from canonical skills/ to DeepChat skills directory."""
    results = {}
    canonical_skills = CANONICAL_ROOT / "skills"

    if not canonical_skills.exists():
        results["error"] = "Canonical skills directory not found: {}".format(
            canonical_skills
        )
        return results

    for skill_dir in sorted(canonical_skills.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        canonical_skill = skill_dir / "SKILL.md"
        target_dir = DEEPCHAT_SKILLS / skill_name
        target_skill = target_dir / "SKILL.md"

        if not canonical_skill.exists():
            results[skill_name] = "CANONICAL_MISSING"
            continue

        canonical_content = read_file(canonical_skill)
        current_content = read_file(target_skill)

        if current_content and hash_content(canonical_content) == hash_content(
            current_content
        ):
            results[skill_name] = "UNCHANGED"
            continue

        if dry_run:
            status = "INSTALL" if current_content is None else "UPDATE"
            results[skill_name] = "WOULD_" + status
            continue

        write_file(target_skill, canonical_content)
        status = "INSTALLED" if current_content is None else "UPDATED"
        results[skill_name] = status

    return results


# =====================================================================
# CONFIG DEPLOYMENT
# =====================================================================

def deploy_configs(dry_run=False):
    """Deploy config files from canonical config/ to DeepChat directory."""
    results = {}
    canonical_config = CANONICAL_ROOT / "config"

    if not canonical_config.exists():
        results["error"] = "Canonical config directory not found: {}".format(
            canonical_config
        )
        return results

    for config_name, target_path in CONFIG_MAP.items():
        canonical_path = canonical_config / config_name

        if not canonical_path.exists():
            results[config_name] = "CANONICAL_MISSING"
            continue

        canonical_content = read_file(canonical_path)
        current_content = read_file(target_path)

        if current_content and hash_content(canonical_content) == hash_content(
            current_content
        ):
            results[config_name] = "UNCHANGED"
            continue

        if dry_run:
            status = "INSTALL" if current_content is None else "UPDATE"
            results[config_name] = "WOULD_" + status
            continue

        write_file(target_path, canonical_content)
        status = "INSTALLED" if current_content is None else "UPDATED"
        results[config_name] = status

    return results


# =====================================================================
# DEFAULT SYSTEM PROMPT (app-settings.json)
# =====================================================================

def deploy_default_system_prompt(dry_run=False):
    """Verify app-settings.json default_system_prompt status."""
    results = {}

    if not APP_SETTINGS.exists():
        results["error"] = "app-settings.json not found at {}".format(APP_SETTINGS)
        return results

    with open(APP_SETTINGS, "r", encoding="utf-8") as f:
        settings = json.load(f)

    dsp = settings.get("default_system_prompt", "")
    if not dsp:
        results["default_system_prompt"] = "MISSING"
    else:
        results["default_system_prompt"] = "PRESENT ({} chars)".format(len(dsp))

    return results


# =====================================================================
# MAIN
# =====================================================================

def deploy_templates(dry_run=False):
    """Sync canonical templates/ to custom_prompts.json.

    Canonical .md files in templates/ are the source of truth. This function:
    1. Reads all .md files from CANONICAL_ROOT/templates/
    2. Reads deployed custom_prompts.json
    3. Adds any missing canonical templates; updates content if drifted
    4. Does NOT remove deployed-only templates (they may be UI-created)
    """
    results = {}
    templates_dir = CANONICAL_ROOT / "templates"

    if not templates_dir.exists():
        results["error"] = "Canonical templates directory not found"
        return results

    # Read deployed custom_prompts.json
    if not CUSTOM_PROMPTS.exists():
        results["error"] = "custom_prompts.json not found"
        return results

    with open(CUSTOM_PROMPTS, "r", encoding="utf-8") as f:
        cp = json.load(f)

    prompts = cp.get("prompts", [])
    prompts_by_name = {p["name"]: p for p in prompts}

    # Scan canonical templates
    for md_file in sorted(templates_dir.glob("*.md")):
        template_name = md_file.stem  # filename without .md
        canonical_content = read_file(md_file)

        if canonical_content is None:
            continue

        if template_name in prompts_by_name:
            deployed_entry = prompts_by_name[template_name]
            deployed_content = deployed_entry.get("content", "")
            if hash_content(canonical_content) == hash_content(deployed_content):
                results[template_name] = "UNCHANGED"
                continue
            if dry_run:
                results[template_name] = "WOULD_UPDATE"
                continue
            deployed_entry["content"] = canonical_content
            deployed_entry["updatedAt"] = str(int(time.time() * 1000))
            results[template_name] = "UPDATED"
        else:
            if dry_run:
                results[template_name] = "WOULD_INSTALL"
                continue
            new_id = str(int(time.time() * 1000))
            new_entry = {
                "id": new_id,
                "name": template_name,
                "description": "",
                "content": canonical_content,
                "parameters": [],
                "files": [],
                "enabled": True,
                "source": "local",
                "createdAt": new_id,
                "updatedAt": new_id,
            }
            prompts.append(new_entry)
            results[template_name] = "INSTALLED"

    # Write back if not dry run
    if not dry_run:
        cp["prompts"] = prompts
        with open(CUSTOM_PROMPTS, "w", encoding="utf-8") as f:
            json.dump(cp, f, indent=2, ensure_ascii=False)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Deploy canonical prompts to DeepChat runtime"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without making changes",
    )
    parser.add_argument(
        "--prompts-only",
        action="store_true",
        help="Deploy only system prompts to agent.db",
    )
    parser.add_argument(
        "--skills-only", action="store_true", help="Deploy only skills"
    )
    parser.add_argument(
        "--config-only", action="store_true", help="Deploy only config files"
    )
    parser.add_argument(
        "--templates-only", action="store_true",
        help="Deploy only templates to custom_prompts.json"
    )
    parser.add_argument(
        "--kaizen", action="store_true",
        help="Run Kaizen Engine then deploy all changes (auto mode)"
    )
    args = parser.parse_args()

    # Kaizen auto mode: run improvement engine before deploying
    if args.kaizen:
        import subprocess as sp
        kaizen_path = CANONICAL_ROOT / "tools" / "kaizen_engine.py"
        if kaizen_path.exists():
            print("--- Running Kaizen Engine (auto mode) ---")
            result = sp.run(
                ["python", str(kaizen_path), "--auto"],
                capture_output=True, text=True, cwd=str(CANONICAL_ROOT)
            )
            print(result.stdout[-500:] if result.stdout else "No output")
            if result.returncode != 0:
                print(f"Kaizen warning (exit {result.returncode})")
        else:
            print(f"Kaizen engine not found at {kaizen_path}")

    run_all = not (args.prompts_only or args.skills_only or args.config_only or args.templates_only)
    dry = args.dry_run

    print("=" * 60)
    print("DEEPCHAT DEPLOYMENT PIPELINE v1.0")
    print("Canonical source: {}".format(CANONICAL_ROOT))
    print("Mode: {}".format("DRY RUN" if dry else "LIVE"))
    print("=" * 60)

    exit_code = 0

    if run_all or args.prompts_only:
        print("\n--- System Prompts (agent.db) ---")
        results = deploy_system_prompts(dry_run=dry)
        for agent in sorted(results.keys()):
            status = results[agent]
            flag = "->" if "UPDATE" in status else "  "
            print("  {} {}: {}".format(flag, agent, status))
            if status == "AGENT_NOT_FOUND" or status.startswith("error"):
                exit_code = 1

    if run_all or args.skills_only:
        print("\n--- Skills (DeepChat skills/) ---")
        results = deploy_skills(dry_run=dry)
        for skill in sorted(results.keys()):
            status = results[skill]
            flag = "->" if "UPDATE" in status or "INSTALL" in status else "  "
            print("  {} {}: {}".format(flag, skill, status))

    if run_all or args.config_only:
        print("\n--- Config Files ---")
        results = deploy_configs(dry_run=dry)
        for cfg in sorted(results.keys()):
            status = results[cfg]
            flag = "->" if "UPDATE" in status or "INSTALL" in status else "  "
            print("  {} {}: {}".format(flag, cfg, status))

    if run_all or args.templates_only:
        print("\n--- Templates (custom_prompts.json) ---")
        results = deploy_templates(dry_run=dry)
        for tmpl in sorted(results.keys()):
            status = results[tmpl]
            flag = "->" if "UPDATE" in status or "INSTALL" in status else "  "
            print("  {} {}: {}".format(flag, tmpl, status))

    if run_all:
        print("\n--- Default System Prompt (app-settings.json) ---")
        results = deploy_default_system_prompt(dry_run=dry)
        for key in sorted(results.keys()):
            print("    {}: {}".format(key, results[key]))

    if dry:
        print("\n[DRY RUN] No changes made. Remove --dry-run to deploy.")
    else:
        print("\n[OK] Deployment complete. Restart DeepChat to activate changes.")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
