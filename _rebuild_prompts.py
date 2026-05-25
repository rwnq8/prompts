import json, os, time
PROMPTS_DIR = r"G:\My Drive\prompts"
SYSTEM_PROMPTS = {
    "DEFAULT.md": {"name": "DEFAULT (Projects Agent)", "slot": "projects", "description": "General-purpose assistant for brainstorming, research, writing, and project execution across all domains."},
    "META-PROMPT-DEEPSEEK.md": {"name": "META-PROMPT-DEEPSEEK (Prompt Generator)", "slot": "prompts", "description": "System prompt generator for other agents; maintains templates and architecture."},
    "QWAV-DEFAULT.md": {"name": "QWAV-DEFAULT (Program Agent)", "slot": "qwav", "description": "Portfolio/Program Manager coordinating multiple projects via GitHub-native infrastructure."},
}
prompts_path = os.path.join(PROMPTS_DIR, "prompts.json")
with open(prompts_path, "r", encoding="utf-8") as f:
    data = json.load(f)
for sp_name, sp_meta in SYSTEM_PROMPTS.items():
    filepath = os.path.join(PROMPTS_DIR, sp_name)
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()
    updated = False
    for i, entry in enumerate(data):
        if entry.get("name") == sp_meta["name"]:
            entry["content"] = content
            entry["updatedAt"] = int(time.time() * 1000)
            updated = True
            print(f"  UPDATED: {sp_meta['name']} (idx {i}, {len(content):,} chars)")
            break
    if not updated:
        print(f"  NOT FOUND: {sp_meta['name']}")
with open(prompts_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())
print(f"prompts.json: {os.path.getsize(prompts_path):,} bytes ({len(data)} entries)")
