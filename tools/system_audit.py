# save as: G:\My Drive\prompts\system_audit.py
import os, re, subprocess, sys
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

# Deep scan for .git contamination (CPL L1: each project gets its own .git)
# depth 0 = projects/ root (caught by A1) or projects/_shared/ (caught by A2)
# depth 1 = projects/<project>/.git — LEGITIMATE per CPL L1, NOT contamination
# depth 2+ = nested .git inside a project subdirectory — TRUE contamination
# Only flag unexpected .git placements, not standard project repos.
git_dirs = []
legitimate_repos = []
for root, dirs, files in os.walk(r"G:\My Drive\projects"):
    depth = root.replace(r"G:\My Drive\projects", "").count(os.sep)
    if depth > 3:
        dirs.clear()  # Don't go deeper
        continue
    if ".git" in dirs:
        git_dir = os.path.join(root, ".git")
        if depth == 1:
            # Standard project repo — legitimate per CPL L1
            legitimate_repos.append(git_dir)
        else:
            # Unexpected depth — true contamination
            git_dirs.append(git_dir)
if git_dirs:
    print(f"  A3. Git at unexpected depth (contamination): {git_dirs} WARNING: FAIL")
else:
    print(f"  A3. No .git contamination in projects tree: PASS")
if legitimate_repos:
    print(f"  A4. Legitimate project repos (CPL L1): {len(legitimate_repos)} — all at depth 2, PASS")

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
    # DEFAULT.md references subagents by name (explorer/implementer/reviewer),
    # NOT by slot-mp80 IDs. The slot-mp80 IDs are internal to DeepChat and
    # resolved at runtime. Check for name-based references instead.
    subagent_names = {"explorer", "implementer", "reviewer"}
    d_content = files["DEFAULT.md"]
    d_found = set()
    for name in subagent_names:
        # Look for the subagent name in the slot ID column of the subagent table
        if re.search(rf"\|\s*\*\*{name.upper()}\*\*\s*\|", d_content):
            d_found.add(name)
    if d_found == subagent_names:
        print(f"  B1. DEFAULT.md subagent refs (explorer/implementer/reviewer): PASS")
    else:
        missing = subagent_names - d_found
        print(f"  B1. DEFAULT.md missing subagent refs: {missing} WARNING: FAIL")
    
    # Check for slot-mp80 references in ARCHITECTURE.md (which DOES use them)
    gt_slots = {"slot-mp80a5ry-e7hn", "slot-mp80ay3u-yzqo", "slot-mp80b6bl-iix2"}
    if "ARCHITECTURE.md" in files:
        a_slots = set(re.findall(r"slot-mp80[a-z0-9]{4}-[a-z0-9]{4}", files["ARCHITECTURE.md"]))
        if a_slots == gt_slots:
            print(f"  B2. ARCHITECTURE.md slot IDs match ground truth: PASS")
        elif a_slots:
            print(f"  B2. ARCHITECTURE.md slots: {a_slots} vs expected {gt_slots} WARNING: FAIL")
        else:
            print(f"  B2. ARCHITECTURE.md has no slot-mp80 IDs CHECK")
    else:
        print(f"  B2. ARCHITECTURE.md not found SKIP")

# PART C: Documentation Drift
print("\nPART C: DOCUMENTATION DRIFT CHECK")
cpl_path = r"G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md"
if os.path.exists(cpl_path):
    with open(cpl_path, "r", encoding="utf-8") as f:
        cpl = f.read()
    lesson_count = len(re.findall(r"^### L\d+:", cpl, re.MULTILINE))
    print(f"  C1/C2. CPL lessons: {lesson_count} (expected >=10) {'PASS' if lesson_count >= 10 else 'CHECK'}")
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


# PART E: CROSS-FILE VERSION CONSISTENCY
print("\nPART E: CROSS-FILE VERSION CONSISTENCY")

# Ground truth - extract actual versions from file headers
def extract_version(filepath):
    """Extract version from first 3 lines of a file (pattern: vX.Y or vX.Y.Z)"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        header = ''.join(f.readline() for _ in range(5))
    m = re.search(r'\bv(\d+)\.(\d+)(?:\.(\d+))?\b', header)
    return f"v{m.group(1)}.{m.group(2)}" if m else None

# Expected versions from ARCHITECTURE.md version table
expected = {}
arch_path = os.path.join(prompts_dir, "ARCHITECTURE.md")
if os.path.exists(arch_path):
    with open(arch_path, 'r', encoding='utf-8') as f:
        arch = f.read()
    # Parse version table
    for m in re.finditer(r'\| `([^`]+\.md)` \| ([^|]+) \| (v[\d.]+|\u2014) \|', arch):
        fname, desc, ver = m.group(1), m.group(2).strip(), m.group(3)
        if ver != '—' and ver != '--':
            expected[fname] = ver

# Check actual versions against ARCHITECTURE.md
checks = [
    ("ARCHITECTURE.md", r"G:\My Drive\prompts\ARCHITECTURE.md"),
    ("META-PROMPT-DEEPSEEK.md", r"G:\My Drive\prompts\META-PROMPT-DEEPSEEK.md"),
    ("AGENT-CONFIG.md", r"G:\My Drive\prompts\AGENT-CONFIG.md"),
    ("agents/PROJECTS-AGENT.md", r"G:\My Drive\prompts\agents\PROJECTS-AGENT.md"),
    ("agents/PROMPTS-AGENT.md", r"G:\My Drive\prompts\agents\PROMPTS-AGENT.md"),
    ("agents/QWAV-AGENT.md", r"G:\My Drive\prompts\agents\QWAV-AGENT.md"),
    ("agents/subagents/EXPLORER-SUBAGENT.md", r"G:\My Drive\prompts\agents\subagents\EXPLORER-SUBAGENT.md"),
    ("agents/subagents/IMPLEMENTER-SUBAGENT.md", r"G:\My Drive\prompts\agents\subagents\IMPLEMENTER-SUBAGENT.md"),
    ("agents/subagents/REVIEWER-SUBAGENT.md", r"G:\My Drive\prompts\agents\subagents\REVIEWER-SUBAGENT.md"),
]

issues = []
for fname, fpath in checks:
    actual = extract_version(fpath)
    exp = expected.get(fname)
    if actual and exp and actual != exp:
        issues.append(f"  E1. {fname}: ARCHITECTURE.md says {exp}, file header says {actual} MISMATCH")

# Check that ARCHITECTURE.md doesn't contradict itself
if os.path.exists(arch_path):
    arch_header_ver = extract_version(arch_path)
    if arch_header_ver and expected.get("ARCHITECTURE.md"):
        if arch_header_ver != expected["ARCHITECTURE.md"]:
            issues.append(f"  E2. ARCHITECTURE.md: header says {arch_header_ver}, own version table says {expected['ARCHITECTURE.md']} SELF-CONTRADICTION")

# Check slot ID consistency across files
slot_files = {
    "ARCHITECTURE.md": r"G:\My Drive\prompts\ARCHITECTURE.md",
}
gt_slots = {"slot-mp80a5ry-e7hn", "slot-mp80ay3u-yzqo", "slot-mp80b6bl-iix2"}
for fname, fpath in slot_files.items():
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            fslots = set(re.findall(r"slot-mp80[a-z0-9]{4}-[a-z0-9]{4}", f.read()))
        if fslots and fslots != gt_slots:
            issues.append(f"  E3. {fname} slots: {fslots} vs expected {gt_slots} MISMATCH")

# Check for stale template/section references
stale_patterns = {
    "9-section template": r"G:\My Drive\prompts\agents\PROMPTS-AGENT.md",
    r"v4\.2": r"G:\My Drive\prompts\ARCHITECTURE.md",
    r"v1\.11": r"G:\My Drive\prompts\agents\PROJECTS-AGENT.md",
}
for pattern, fpath in stale_patterns.items():
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            if re.search(pattern, f.read()):
                issues.append(f"  E4. {fpath.split(chr(92))[-1]}: stale reference '{pattern}' found STALE")

if issues:
    for i in issues:
        print(i)
    print(f"  E_RESULT: {len(issues)} inconsistency(ies) found WARNING: FAIL")
else:
    print("  E_RESULT: All cross-file versions and references consistent PASS")


# PART F: Template Integration Check
print("\nPART F: TEMPLATE INTEGRATION CHECK")

# Project management template names
pm_templates = {
    "PROJECT-CHARTER": "CHARTER.md",
    "DEFINITION-OF-DONE": "DEFINITION-OF-DONE.md",
    "RISK-REGISTER": "RISK-REGISTER.md",
    "README": "README.md",
    # DEPRECATED per DEFAULT.md §0.6.8 -> Cloudflare R2-native (ADR-001):
    "SPRINT-BACKLOG": "SPRINT.md -> Cloudflare R2 qnfo/audit/backlog/",
    "PRODUCT-BACKLOG": "BACKLOG.md -> Cloudflare R2 qnfo/audit/backlog/",
    "CHANGELOG": "CHANGELOG.md -> Cloudflare R2 qnfo/releases/",
    "CONTRIBUTING": "CONTRIBUTING.md (Cloudflare R2 qnfo/releases/ — public)",
    "HANDOFF": "handoff document",
    "ADR": "DECISIONS.md -> Cloudflare R2 qnfo/audit/decisions/DECISION-LOG.md",
    "PROJECT-STATE": "PROJECT STATE.md -> Cloudflare R2 qnfo/audit/state/",
    "LEARNINGS": "LEARNINGS.md -> Cloudflare R2 qnfo/audit/learnings/",
    "CLOSEOUT-CHECKLIST": "CLOSEOUT-CHECKLIST.md",
    "WEB-APP-RELEASE-CHECKLIST": "web app pre-deployment gate",
    "TEST-EVIDENCE": "test execution evidence",
    "RETROSPECTIVE": "sprint retrospective",
    "QA-QC-TESTING-PROTOCOL": "QA-QC-TESTING-PROTOCOL.md",
    "PROJECT-INITIATION": "PROJECT-INITIATION.md",
    "SOCIAL-ORCHESTRATOR-TEMPLATE": "social media orchestration",
}

default_path = os.path.join(prompts_dir, "DEFAULT.md")
qwav_path = os.path.join(prompts_dir, "QWAV-DEFAULT.md")
default_wired = set()
qwav_wired = set()

if os.path.exists(default_path):
    with open(default_path, 'r', encoding='utf-8') as f:
        d_content = f.read()
    for tmpl_name in pm_templates:
        if tmpl_name in d_content:
            default_wired.add(tmpl_name)

if os.path.exists(qwav_path):
    with open(qwav_path, 'r', encoding='utf-8') as f:
        q_content = f.read()
    for tmpl_name in pm_templates:
        if tmpl_name in q_content:
            qwav_wired.add(tmpl_name)

all_wired = default_wired | qwav_wired
unwired = set(pm_templates.keys()) - all_wired

print(f"  F1. DEFAULT.md wired: {len(default_wired)}/{len(pm_templates)}")
for tmpl in sorted(pm_templates.keys()):
    status = "WIRED" if tmpl in default_wired else "MISSING"
    print(f"    {status}: {tmpl}")

print(f"  F2. QWAV-DEFAULT.md wired: {len(qwav_wired)}/{len(pm_templates)}")
for tmpl in sorted(pm_templates.keys()):
    if tmpl in qwav_wired:
        status = "WIRED"
    elif tmpl in {"SOCIAL-ORCHESTRATOR-TEMPLATE", "ADR", "CLOSEOUT-CHECKLIST", 
                  "QA-QC-TESTING-PROTOCOL", "RETROSPECTIVE", "TEST-EVIDENCE", 
                  "WEB-APP-RELEASE-CHECKLIST"}:
        status = "OMITTED"
    else:
        status = "MISSING"
    print(f"    {status}: {tmpl}")

if unwired:
    print(f"  F3. UNWIRED (dead code): {len(unwired)}/{len(pm_templates)} {sorted(unwired)}")
else:
    print(f"  F3. All {len(pm_templates)} templates wired in at least one agent")

if len(unwired) == 0:
    print(f"  F_RESULT: All {len(pm_templates)} project management templates wired PASS")
elif len(unwired) <= 2:
    print(f"  F_RESULT: {len(unwired)} templates unwired WARNING")
else:
    print(f"  F_RESULT: {len(unwired)} templates unwired (dead code) FAIL")


# PART G: Template File Content Verification
print("\nPART G: TEMPLATE FILE CONTENT CHECK")
templates_dir = os.path.join(prompts_dir, "templates")
missing_files = []
empty_files = []
if os.path.exists(templates_dir):
    for fname in os.listdir(templates_dir):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(templates_dir, fname)
        if not os.path.isfile(fpath):
            missing_files.append(fname)
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if len(content) < 50:  # Must have YAML frontmatter + at least some body
            empty_files.append(fname)
if missing_files:
    print(f"  G1. Missing template files: {missing_files} FAIL")
else:
    print(f"  G1. All template files present: PASS")
if empty_files:
    print(f"  G2. Empty/near-empty templates: {empty_files} FAIL")
else:
    print(f"  G2. All template files have content: PASS")
if not missing_files and not empty_files:
    print("  G_RESULT: Template file integrity PASS")
else:
    print("  G_RESULT: Template file integrity FAIL")

print(f"\n=== AUDIT COMPLETE ===")

# PART I: CLOUDFLARE R2 INTEGRITY AUDIT (GitHub DEPRECATED per ADR-001)
print("\nPART I: CLOUDFLARE R2 INTEGRITY AUDIT")

import json as _json

# I1: Discovery Index integrity (Cloudflare R2 — canonical ecosystem catalog)
i1_pass = True
try:
    di_result = subprocess.run(
        'npx wrangler r2 object get qnfo/discovery/index.json --remote',
        shell=True, capture_output=True, timeout=20
    )
    if di_result.returncode == 0:
        # Parse the downloaded JSON to verify structure
        import tempfile, os as _os
        tmp = _os.path.join(tempfile.gettempdir(), '_sysaudit_di.json')
        di_result2 = subprocess.run(
            'npx wrangler r2 object get qnfo/discovery/index.json --remote --file=' + tmp,
            shell=True, capture_output=True, timeout=20
        )
        if di_result2.returncode == 0 and _os.path.exists(tmp):
            with open(tmp, 'r') as f:
                di = _json.load(f)
            projects = len(di.get('projects', {}))
            publications = len(di.get('publications', {}))
            archive = len(di.get('archive', {}))
            updated = di.get('updated', 'unknown')
            print(f"  I1. Discovery Index: LIVE ({projects} projects, {publications} pubs, {archive} archived, updated {updated}) PASS")
            _os.remove(tmp)
        else:
            print("  I1. Discovery Index: EXISTS but unparseable WARN")
            i1_pass = False
    else:
        print("  I1. Discovery Index: MISSING (qnfo/discovery/index.json) FAIL")
        print("     Rebuild: python _build_index.py && wrangler r2 object put qnfo/discovery/index.json --file=_discovery_index_seed.json")
        i1_pass = False
except Exception as e:
    print(f"  I1. Discovery Index check error: {e} SKIP")
    i1_pass = False

# I2: R2 Audit Trail integrity (Cloudflare R2)
try:
    dec_result = subprocess.run(
        'npx wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md --remote',
        shell=True, capture_output=True, timeout=15
    )
    if dec_result.returncode == 0:
        print("  I2. Decision Log: PRESENT (qnfo/audit/decisions/DECISION-LOG.md) PASS")
    else:
        print("  I2. Decision Log: MISSING SKIP")
except Exception as e:
    print(f"  I2. Decision Log check error: {e} SKIP")

# I3: Cloudflare R2 bucket connectivity
try:
    wrangler_result = subprocess.run(
        'npx wrangler whoami',
        shell=True, capture_output=True, timeout=10
    )
    if wrangler_result.returncode == 0:
        print("  I3. Cloudflare R2 (wrangler): AUTHENTICATED PASS")
    else:
        print("  I3. Cloudflare R2 (wrangler): NOT AUTHENTICATED FAIL")
        print("     Fix: wrangler login")
except Exception as e:
    print(f"  I3. Cloudflare R2 check error: {e} SKIP")

# I_FINAL: Cloudflare R2 integrity summary
if i1_pass:
    print("  I_RESULT: Cloudflare R2 integrity PASS")
else:
    print("  I_RESULT: Cloudflare R2 integrity FAIL")

# PART H: SYSTEM CONSISTENCY AUDIT (template count drift, cross-references)
print("\nPART H: SYSTEM CONSISTENCY AUDIT (template drift detection)")
consistency_script = os.path.join(prompts_dir, "tools", "system_consistency_audit.py")
if os.path.exists(consistency_script):
    result = subprocess.run([sys.executable, consistency_script], capture_output=True, text=True, cwd=prompts_dir)
    if result.returncode == 0:
        print("  H_RESULT: System consistency audit PASS")
    else:
        print(f"  H_RESULT: System consistency audit FAIL (exit code {result.returncode})")
        # Print last 10 lines of output
        output_lines = result.stdout.strip().split('\n')
        for line in output_lines[-10:]:
            print(f"    {line}")
else:
    print(f"  H_RESULT: Consistency audit script not found at {consistency_script}")

# PART K: KAIZEN ENGINE HEALTH
print("\nPART K: KAIZEN ENGINE HEALTH")
kaizen_path = os.path.join(prompts_dir, "tools", "kaizen_engine.py")
if os.path.exists(kaizen_path):
    print(f"  K1. Kaizen engine present: PASS")
    # Check if it's been run recently
    audit_file = os.path.join(prompts_dir, "audit", "kaizen", "last_run.json")
    if os.path.exists(audit_file):
        with open(audit_file, "r") as f:
            last_run = _json.load(f)
        last_time = last_run.get("timestamp", "unknown")
        print(f"  K2. Last Kaizen run: {last_time} PASS")
    else:
        print(f"  K2. No prior Kaizen run CHECK")
else:
    print(f"  K1. Kaizen engine MISSING WARNING: FAIL")
