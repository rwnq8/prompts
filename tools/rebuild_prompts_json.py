#!/usr/bin/env python3
r"""rebuild_prompts_json.py -- Scan template source directories and rebuild prompts.json.

Produces TWO files:
  1. prompts.json — Wrapped format ({"prompts": [...]}) — CANONICAL, matches
     DeepChat's internal custom_prompts.json storage.
  2. prompts_bare.json — Bare array ([...]) — IMPORT FORMAT. DeepChat's
     Prompt Templates import dialog rejects {"prompts": [...]} with
     "Invalid format: not an array" and expects a bare array at top level.

Source directories: templates/, projects/research-pipeline/, agents/
Deduplicated by name with required DeepChat fields.

Canonical source: G:\My Drive\prompts\tools\rebuild_prompts_json.py
v1.2 — 2026-06-02: Dual output (wrapped canonical + bare import). DeepChat
  import requires bare array format; wrapped is internal storage only.
"""
import os
import json
import glob
import time
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.dirname(SCRIPT_DIR)  # G:\My Drive\prompts

# Directories relative to prompts/
DIRS = ['templates', 'agents']
# Also scan projects/research-pipeline if it exists
RESEARCH_PIPELINE = os.path.join(os.path.dirname(PROMPTS_DIR), 'projects', 'research-pipeline')

OUTPUT = os.path.join(PROMPTS_DIR, 'prompts.json')


def rebuild():
    entries = []
    seen = set()

    # Scan directories
    scan_dirs = [os.path.join(PROMPTS_DIR, d) for d in DIRS]
    if os.path.exists(RESEARCH_PIPELINE):
        scan_dirs.append(RESEARCH_PIPELINE)

    now = str(int(time.time() * 1000))

    for scan_dir in scan_dirs:
        if not os.path.exists(scan_dir):
            print(f"  [SKIP] Directory not found: {scan_dir}")
            continue

        for md_file in sorted(glob.glob(os.path.join(scan_dir, '**', '*.md'), recursive=True)):
            name = os.path.splitext(os.path.basename(md_file))[0]

            # Deduplicate by name (first occurrence wins)
            if name in seen:
                print(f"  [SKIP DUPLICATE] {name} <- {md_file}")
                continue
            seen.add(name)

            with open(md_file, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Skip empty files
            if not content.strip():
                print(f"  [SKIP EMPTY] {name} <- {md_file}")
                continue

            entry_id = str(len(entries) + 1)
            entries.append({
                'id': entry_id,
                'name': name,
                'description': f'Auto-regenerated from {os.path.relpath(md_file, PROMPTS_DIR)}',
                'content': content,
                'parameters': [],
                'enabled': True,
                'source': 'local',
                'createdAt': now,
                'updatedAt': now,
            })
            print(f"  [{len(entries)}] {name} <- {os.path.relpath(md_file, PROMPTS_DIR)}")

    # Write as wrapped format (canonical, matches DeepChat internal storage)
    output_data = {"prompts": entries}
    with open(OUTPUT, 'w', encoding='utf-8') as fh:
        json.dump(output_data, fh, indent=2, ensure_ascii=False)

    # Verify written file
    with open(OUTPUT, 'r', encoding='utf-8') as fh:
        verify = json.load(fh)
    if not isinstance(verify, dict) or 'prompts' not in verify:
        print("ERROR: Output validation failed - not wrapped format!")
        return 0

    # Also write bare array format for DeepChat import dialog
    BARE_OUTPUT = os.path.join(PROMPTS_DIR, 'prompts_bare.json')
    with open(BARE_OUTPUT, 'w', encoding='utf-8') as fh:
        json.dump(entries, fh, indent=2, ensure_ascii=False)

    # Verify bare file
    with open(BARE_OUTPUT, 'r', encoding='utf-8') as fh:
        verify_bare = json.load(fh)
    if not isinstance(verify_bare, list):
        print("ERROR: Bare output validation failed - not a list!")
        return 0

    print(f"\nRebuilt {OUTPUT} (wrapped) and {BARE_OUTPUT} (bare import) with {len(entries)} unique entries from {len(scan_dirs)} directories.")
    return len(entries)


if __name__ == '__main__':
    count = rebuild()
    sys.exit(0 if count > 0 else 1)
