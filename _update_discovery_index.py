#!/usr/bin/env python3
"""Update Discovery Index with prompts R2 migration paths."""
import json, subprocess
from pathlib import Path
from datetime import datetime

# Pull current index
subprocess.run("npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json",
               shell=True, capture_output=True, timeout=30)

DI_PATH = Path("_discovery_index.json")
if not DI_PATH.exists() or DI_PATH.stat().st_size < 10:
    print("ERROR: Could not pull Discovery Index")
    exit(1)

di = json.loads(DI_PATH.read_text(encoding="utf-8"))

# Update prompts section
di["prompts_r2_migration"] = {
    "status": "complete",
    "migrated_at": datetime.now().isoformat(),
    "canonical_prefix": "qnfo/prompts",
    "description": "All prompt-defining files now canonical on R2. Local G:\\My Drive\\prompts\\ is the import surface (DeepChat bridge) — files are pulled from R2 when needed.",
    "files": {
        "core_prompts": [
            "DEFAULT.md", "QWAV-DEFAULT.md", "META-PROMPT-DEEPSEEK.md"
        ],
        "prompts_json": ["prompts.json", "prompts_bare.json"],
        "skills": "14 skills with SKILL.md + scripts + references",
        "templates": "21 templates",
        "agents": "3 agent configs",
        "tools": ["_deploy.py", "_system_audit.py", "_bootstrap_from_r2.py"],
        "architecture": "Architecture documentation",
        "config": "DeepChat config files"
    },
    "bootstrap_script": "qnfo/prompts/_bootstrap_from_r2.py",
    "deploy_script": "qnfo/prompts/_deploy.py"
}

# Update skills section
if "skills" in di:
    di["skills"]["r2_prefix"] = "qnfo/prompts/skills"
    di["skills"]["canonical_location"] = "R2 qnfo/prompts/skills/"

# Update templates section
if "templates" in di:
    di["templates"]["r2_prefix"] = "qnfo/prompts/templates"
    di["templates"]["canonical_location"] = "R2 qnfo/prompts/templates/"

# Update metadata
di["_metadata"]["last_prompts_migration"] = datetime.now().isoformat()
di["last_updated"] = datetime.now().isoformat()
di["updated_by"] = "META-PROMPT v6.5 — prompts-r2-migration"

# Write updated index
updated_path = Path("_discovery_index_updated.json")
updated_path.write_text(json.dumps(di, indent=2), encoding="utf-8")

# Backup old index
subprocess.run(
    f'npx wrangler r2 object put "qnfo/discovery/index-backup-{datetime.now().strftime("%Y%m%dT%H%M%S")}.json" --file "_discovery_index.json" --remote',
    shell=True, capture_output=True, timeout=30)

# Upload updated index
subprocess.run(
    'npx wrangler r2 object put "qnfo/discovery/index.json" --file "_discovery_index_updated.json" --remote',
    shell=True, capture_output=True, timeout=30)

# Verify
subprocess.run("npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index_verify.json",
               shell=True, capture_output=True, timeout=30)

verify = Path("_discovery_index_verify.json")
if verify.exists():
    vdi = json.loads(verify.read_text(encoding="utf-8"))
    if "prompts_r2_migration" in vdi:
        print("VERIFIED: Discovery Index updated with prompts_r2_migration section")
    else:
        print("WARNING: Verification failed - prompts_r2_migration not found")
else:
    print("WARNING: Verification file not pulled")

print("Discovery Index update complete.")
