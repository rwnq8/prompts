# save as: G:\My Drive\prompts\system_audit.py
import os, re, subprocess
from datetime import datetime

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

print(f"=== SYSTEM HEALTH AUDIT — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

# PART A: Git Contamination
print("PART A: GIT CONTAMINATION CHECK")
parent_git = os.path.exists(r"G:\My Drive\projects\.git")
print(f"  A1. Parent .git exists: {parent_git} {'WARNING: FAIL' if parent_git else 'PASS'}")
shared_git = os.path.exists(r"G:\My Drive\projects\_shared\.git")
print(f"  A2. _shared .git exists: {shared_git} {'WARNING: FAIL' if shared_git else 'PASS'}")

# Deep scan for .git contamination
git_dirs = []
for root, dirs, files in os.walk(r"G:\My Drive\projects"):
    depth = root.replace(r"G:\My Drive\projects", "").count(os.sep)
    if depth > 3:
        dirs.clear()  # Don't go deeper
        continue
    if ".git" in dirs:
        git_dirs.append(os.path.join(root, ".git"))
if git_dirs:
    print(f"  A3. Found .git contamination: {git_dirs} WARNING: FAIL")
else:
    print(f"  A3. No .git contamination in projects tree: PASS")

# PART B: Prompt Consistency
print("\nPART B: PROMPT CONSISTENCY CHECK")
prompts_dir = r"G:\My Drive\prompts"
files = {}
for fname in ["DEFAULT.md", "ARCHITECTURE.md", "AGENT-CONFIG.md"]:
    fpath = os.path.join(prompts_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            files[fname] = f.read()

if "DEFAULT.md" in files:
    d_slots = set(re.findall(r"slot-mp80[a-z0-9]{4}-[a-z0-9]{4}", files["DEFAULT.md"]))
    # Ground truth from live tool definitions — update this when slot IDs change
    gt_slots = {"slot-mp80a5ry-e7hn", "slot-mp80ay3u-yzqo", "slot-mp80b6bl-iix2"}
    if d_slots == gt_slots:
        print(f"  B1. DEFAULT.md slots match ground truth: PASS")
    else:
        print(f"  B1. DEFAULT.md slots: {d_slots} vs expected {gt_slots} WARNING: FAIL")

for fname in ["ARCHITECTURE.md", "AGENT-CONFIG.md"]:
    if fname in files:
        f_slots = set(re.findall(r"slot-mp80[a-z0-9]{4}-[a-z0-9]{4}", files[fname]))
        if f_slots == gt_slots:
            print(f"  B2/B3. {fname} slots match DEFAULT.md: PASS")
        elif f_slots == set():
            print(f"  B2/B3. {fname} has no slot IDs (may use 'self'): CHECK")
        else:
            print(f"  B2/B3. {fname} MISMATCH: {f_slots} vs {gt_slots} WARNING: FAIL")

# PART C: Documentation Drift
print("\nPART C: DOCUMENTATION DRIFT CHECK")
cpl_path = r"G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md"
if os.path.exists(cpl_path):
    with open(cpl_path, "r", encoding="utf-8") as f:
        cpl = f.read()
    lesson_count = len(re.findall(r"^### L\d+:", cpl, re.MULTILINE))
    print(f"  C1/C2. CPL lessons: {lesson_count} (expected >=30) {'PASS' if lesson_count >= 30 else 'CHECK'}")
else:
    print(f"  C1. CROSS-PROJECT-LEARNINGS.md MISSING WARNING: FAIL")

# PART D: Archive Integrity
print("\nPART D: ARCHIVE INTEGRITY CHECK")
projects_root = r"G:\My Drive\projects"
if os.path.exists(projects_root):
    orphans = [f for f in os.listdir(projects_root) 
               if f not in ["_shared", ".git", "__pycache__"] 
               and os.path.isfile(os.path.join(projects_root, f))]
    if orphans:
        print(f"  D2. Orphan files at projects root: {orphans} WARNING: FAIL")
    else:
        print(f"  D2. No orphan files at projects root: PASS")

# Count releases
releases_dir = r"G:\My Drive\Obsidian\releases"
if os.path.exists(releases_dir):
    release_count = 0
    for root, dirs, files in os.walk(releases_dir):
        release_count += len([f for f in files if f.endswith('.md')])
    print(f"  D4/D5. Release documents: {release_count}")

print(f"\n=== AUDIT COMPLETE ===")
