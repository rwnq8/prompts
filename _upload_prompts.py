#!/usr/bin/env python3
"""Upload prompt-defining files to R2. Skip audit logs, hooks, and ephemeral files."""
import subprocess, json
from pathlib import Path
from datetime import datetime

ROOT = Path(r"G:\My Drive\prompts")
R2 = "qnfo/prompts"

# Only these directories contain prompt-defining files
PROMPT_DIRS = [
    "",           # root: DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT-DEEPSEEK.md, prompts.json, etc.
    "skills",     # 14 skills with SKILL.md + scripts/ + references/
    "templates",  # 21 templates
    "agents",     # 3 agent configs
    "config",     # deepchat configs
    "architecture",  # architecture docs
]

# Only these root-level files
ROOT_FILES = [
    "DEFAULT.md", "QWAV-DEFAULT.md", "META-PROMPT-DEEPSEEK.md",
    "prompts.json", "prompts_bare.json",
    "_deploy.py", "_system_audit.py",
    "PLATFORM-GAPS.md",
]

def collect_files():
    files = []
    # Root-level files
    for name in ROOT_FILES:
        fp = ROOT / name
        if fp.exists():
            rel = fp.relative_to(ROOT)
            files.append((fp, str(rel).replace("\\", "/")))
    
    # Skill directories
    skills_dir = ROOT / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir(): continue
            for f in skill_dir.rglob("*"):
                if f.is_file() and "__pycache__" not in f.parts:
                    rel = f.relative_to(ROOT)
                    files.append((f, str(rel).replace("\\", "/")))
    
    # Templates
    templates_dir = ROOT / "templates"
    if templates_dir.exists():
        for f in templates_dir.glob("*.md"):
            rel = f.relative_to(ROOT)
            files.append((f, str(rel).replace("\\", "/")))
    
    # Agents
    agents_dir = ROOT / "agents"
    if agents_dir.exists():
        for f in agents_dir.glob("*.md"):
            rel = f.relative_to(ROOT)
            files.append((f, str(rel).replace("\\", "/")))
    
    # Config
    config_dir = ROOT / "config"
    if config_dir.exists():
        for f in config_dir.glob("*"):
            if f.is_file():
                rel = f.relative_to(ROOT)
                files.append((f, str(rel).replace("\\", "/")))
    
    # Architecture
    arch_dir = ROOT / "architecture"
    if arch_dir.exists():
        for f in arch_dir.glob("*"):
            if f.is_file():
                rel = f.relative_to(ROOT)
                files.append((f, str(rel).replace("\\", "/")))
    
    return sorted(files, key=lambda x: x[1])

files = collect_files()
print(f"Prompt-defining files to upload: {len(files)}")
for _, rel in files:
    print(f"  {rel}")

print(f"\n--- UPLOADING ---")
ok, fail = 0, []
for i, (fp, rel) in enumerate(files):
    r2p = f"{R2}/{rel}"
    sz = fp.stat().st_size
    print(f"[{i+1}/{len(files)}] {rel} ({sz:,}B) ... ", end="", flush=True)
    r = subprocess.run(
        f'npx wrangler r2 object put "{r2p}" --file "{fp}" --remote',
        shell=True, capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        print("OK")
        ok += 1
    else:
        err = r.stderr.strip()[:120]
        print(f"FAIL: {err}")
        fail.append((rel, err))

print(f"\n--- RESULTS ---")
print(f"Uploaded: {ok}/{len(files)}")
if fail:
    print("FAILURES:")
    for f, e in fail: print(f"  {f}: {e}")

# Manifest
manifest = {"time": datetime.now().isoformat(), "total": len(files),
            "ok": ok, "failed": len(fail),
            "files": [rel for _, rel in files],
            "r2_prefix": R2}
mf = ROOT / "_MIGRATION_MANIFEST.json"
mf.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

# Upload manifest
subprocess.run(
    f'npx wrangler r2 object put "{R2}/MIGRATION_MANIFEST.json" --file "{mf}" --remote',
    shell=True, capture_output=True, timeout=30)
print(f"\nManifest: {mf}")
print("Done.")
