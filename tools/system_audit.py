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
    "SPRINT-BACKLOG": "SPRINT.md",
    "PRODUCT-BACKLOG": "BACKLOG.md",
    "CHANGELOG": "CHANGELOG.md",
    "CONTRIBUTING": "CONTRIBUTING.md",
    "HANDOFF": "handoff document",
    "ADR": "DECISIONS.md",
    "PROJECT-STATE": "PROJECT STATE.md",
    "LEARNINGS": "LEARNINGS.md",
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
    status = "WIRED" if tmpl in qwav_wired else "MISSING"
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

# PART I: ANTI-PHANTOM EXECUTION AUDIT (Rule 14 Enforcement)
print("\nPART I: ANTI-PHANTOM EXECUTION AUDIT (GitHub Issues Integrity)")

# Check GitHub Issues for Rule 14 violations: closed without deliverable evidence
import json as _json
i_issues = []
try:
    result = subprocess.run(
        ["gh", "issue", "list", "--repo", "QNFO/qwav", "--state", "closed", "--limit", "30", "--json", "title,body,number,closedAt,comments"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode == 0:
        closed = _json.loads(result.stdout)
        # Red flags: closed with minimal body, no comments, no file references, no commit hashes
        for issue in closed:
            flags = []
            body = (issue.get("body") or "").strip()
            num = issue["number"]
            title = issue["title"]
            
            if len(body) < 100 and "TEST" not in title.upper():
                flags.append("MINIMAL-BODY")
            if issue.get("comments", 0) == 0:
                flags.append("NO-COMMENTS")
            if not re.search(r"(?:Test-Path|git log|commits|verified|smoke_test|system_audit)", body):
                if not re.search(r"`[a-f0-9]{7}`", body):  # No commit hash
                    flags.append("NO-EVIDENCE")
            if "Token" in title and "scope" in title.lower() and not re.search(r"(?:refreshed|added scope|now has)", body):
                flags.append("TOKEN-NOT-UPGRADED")
            if "Project board" in title and not re.search(r"(?:created|board exists)", body):
                flags.append("BOARD-NOT-CREATED")
            
            if flags:
                i_issues.append((num, title, flags))
        
        if i_issues:
            print(f"  I1. ANTI-PHANTOM detections: {len(i_issues)} closed Issues lack execution evidence")
            for num, title, flags in i_issues:
                print(f"    #{num}: {title} — {', '.join(flags)}")
            print(f"  I_RESULT: {len(i_issues)} Rule 14 violations found FAIL")
        else:
            print("  I1. No ANTI-PHANTOM patterns detected PASS")
            print("  I_RESULT: GitHub Issues execution integrity PASS")
    else:
        print(f"  I1. Could not query GitHub Issues: {result.stderr[:100]} SKIP")
except Exception as e:
    print(f"  I1. GitHub Issues check error: {e} SKIP")

# I2: Token scope gap check
i2_issues = []
try:
    # Check current token scopes
    tresult = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=10)
    scopes = tresult.stdout + tresult.stderr
    missing_scopes = []
    # Note: discussions:write is NOT a valid GitHub OAuth scope. repo scope covers all Discussion CRUD.
    if "project" not in scopes:
        missing_scopes.append("project")
    
    if missing_scopes:
        i2_issues.append(f"Missing token scopes: {', '.join(missing_scopes)}")
        print(f"  I2. Token scope gaps: {missing_scopes} FAIL")
        print(f"     Fix: gh auth refresh -h github.com -s {','.join(missing_scopes)}")
        print(f"     Note: repo scope already covers Discussions CRUD. discussions:write is not a valid scope.")
    else:
        print("  I2. Token scopes complete PASS")
except Exception as e:
    print(f"  I2. Token scope check error: {e} SKIP")

# I3: Wiki content vs push state
try:
    wiki_pages_dir = r"G:\My Drive\projects\wiki-pages"
    if os.path.exists(wiki_pages_dir):
        page_files = [f for f in os.listdir(wiki_pages_dir) if f.endswith('.md')]
        if page_files:
            print(f"  I3. Wiki pages ready: {len(page_files)} files ({sum(os.path.getsize(os.path.join(wiki_pages_dir, f)) for f in page_files)} bytes) — NOT PUSHED")
            print(f"     Action: Initialize wiki via web UI then push wiki-pages/")
        else:
            print("  I3. Wiki pages directory empty CHECK")
    else:
        print("  I3. No wiki-pages directory CHECK")
except Exception as e:
    print(f"  I3. Wiki check error: {e} SKIP")

# I4: GitHub Releases vs CHANGELOG
try:
    rresult = subprocess.run(["gh", "release", "list", "--repo", "QNFO/qwav", "--limit", "5"], 
                            capture_output=True, text=True, timeout=10)
    releases = rresult.stdout.strip()
    if not releases:
        print("  I4. No GitHub Releases found — CHANGELOG migration not done FAIL")
    else:
        rc = len(releases.split('\n'))
        print(f"  I4. {rc} GitHub Releases found PASS")
except Exception as e:
    print(f"  I4. Releases check error: {e} SKIP")

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
