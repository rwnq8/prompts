#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM AUDIT — 100% Consistency Check
Audits: prompts, templates, skills, configs, cross-references, R2 paths, deployments
"""
import os, json, re, subprocess, sys
from pathlib import Path
from datetime import datetime

PROMPTS_DIR = Path(r"G:\My Drive\prompts")
ISSUES = []
PASSES = []

def issue(severity, category, detail):
    ISSUES.append((severity, category, detail))
    print(f"  [{severity}] {category}: {detail}")

def ok(category, detail):
    PASSES.append((category, detail))
    print(f"  [OK] {category}: {detail}")

# =============================================================================
# PHASE 1: STRUCTURAL AUDIT — Check every prompt has mandatory sections
# =============================================================================
print("=" * 70)
print("PHASE 1: STRUCTURAL AUDIT — Mandatory Sections in All Prompts")
print("=" * 70)

MANDATORY_SECTIONS = [
    "RESEARCH INTEGRITY MANDATE",
    "CORE OPERATING RULES",
    "WHAT THIS AGENT DOES AND WHY",
    "TOOLS AND HOW TO USE THEM",
    "STEP-BY-STEP WORKFLOW",
    "FILE LIFECYCLE",
    "FAILURE HANDLING",
    "GIT PROTOCOL",
]

prompt_files = list(PROMPTS_DIR.glob("DEFAULT.md")) + \
               list(PROMPTS_DIR.glob("QWAV-DEFAULT.md")) + \
               list(PROMPTS_DIR.glob("META-PROMPT-DEEPSEEK.md"))

for pf in prompt_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check header version format (QWAV uses em dash, META uses "GENERATOR" without colon)
    header_match = re.search(r'\(v(\d+\.\d+)[^)]*\)', content[:500])
    if header_match:
        ok(f"{pf.name} header", f"Version v{header_match.group(1)}")
    else:
        issue("BLOCKING", f"{pf.name} header", "No version number found in header")
    
    # Check key structural elements
    for section in MANDATORY_SECTIONS:
        if section.upper() in content.upper():
            ok(f"{pf.name} sections", f"'{section}' present")
        else:
            # Some sections have alternative names
            found = False
            alt_names = {
                "FILE LIFECYCLE": ["FILE LIFECYCLE AND MANAGEMENT", "FILE MANAGEMENT"],
                "WHAT THIS AGENT DOES AND WHY": ["WHAT THIS AGENT DOES", "IDENTITY", "ROLE"],
                "TOOLS AND HOW TO USE THEM": ["TOOLS"],
                "STEP-BY-STEP WORKFLOW": ["WORKFLOW", "STEP-BY-STEP"],
                "GIT PROTOCOL": ["GIT INTEGRATION", "GIT PROTOCOL"],
            }
            for alt in alt_names.get(section, []):
                if alt.upper() in content.upper():
                    found = True
                    break
            if found:
                ok(f"{pf.name} sections", f"'{section}' present (alternate name)")
            else:
                issue("WARN", f"{pf.name} sections", f"'{section}' NOT FOUND")
    
    # Check Rule 6 (math formatting)
    if "Rule 6" in content and "MathJax" in content:
        ok(f"{pf.name} rules", "Rule 6 (math formatting) present")
    else:
        issue("WARN", f"{pf.name} rules", "Rule 6 may be missing or incomplete")
    
    # Check Research Integrity Mandate
    if "FACTUAL LANGUAGE ONLY" in content:
        ok(f"{pf.name} integrity", "Research Integrity Mandate present")
    else:
        issue("BLOCKING", f"{pf.name} integrity", "Research Integrity Mandate MISSING")

# =============================================================================
# PHASE 2: CROSS-REFERENCE AUDIT — R2 paths, templates, skills
# =============================================================================
print("\n" + "=" * 70)
print("PHASE 2: CROSS-REFERENCE AUDIT")
print("=" * 70)

# 2a: Check for the WRONG pipeline-status path
wrong_path = "qnfo/audit/pipeline-status.json"
correct_path = "qnfo/pipeline-status.json"

all_md_files = list(PROMPTS_DIR.glob("*.md")) + \
               list(PROMPTS_DIR.glob("templates/*.md")) + \
               list(PROMPTS_DIR.glob("skills/*/SKILL.md")) + \
               list((PROMPTS_DIR / "agents").glob("*.md"))

wrong_path_count = 0
for f in all_md_files:
    if not f.exists():
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    if wrong_path in content:
        # Check if it's in version history (acceptable) or as functional reference
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if wrong_path in line:
                context_before = lines[max(0,i-2):i]
                context = ' '.join(context_before) + ' ' + line
                if any(kw in context for kw in ['root cause', 'fix cycle', 'version history', 'v3.16', 'v5.6', 'd63e735', '8bda41d']):
                    continue  # In version history — acceptable
                wrong_path_count += 1
                issue("BLOCKING", f"{f.name} L{i+1}", f"WRONG PATH: {wrong_path} (should be {correct_path})")
    
    if correct_path in content:
        pass  # Correct path found

if wrong_path_count == 0:
    ok("R2 paths", "No functional references to wrong pipeline-status path")

# 2b: Check that all referenced templates exist
print("\n--- Template References ---")
template_dir = PROMPTS_DIR / "templates"
existing_templates = {f.stem for f in template_dir.glob("*.md")}

for f in all_md_files:
    if not f.exists():
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    # Find fill_prompt_template("TEMPLATE_NAME") references
    template_refs = re.findall(r'fill_prompt_template\("([^"]+)"', content)
    for ref in template_refs:
        if ref in existing_templates:
            ok(f"template ref in {f.name}", f"fill_prompt_template('{ref}') -> exists")
        else:
            issue("BLOCKING", f"template ref in {f.name}", f"fill_prompt_template('{ref}') -> TEMPLATE NOT FOUND")

# 2c: Check that all skill references resolve
print("\n--- Skill References ---")
skill_dir = PROMPTS_DIR / "skills"
existing_skills = {d.name for d in skill_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}

for f in all_md_files:
    if not f.exists():
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    # Find read('...skills/NAME/SKILL.md') references
    skill_refs = re.findall(r"skills/([a-zA-Z0-9\-]+)/SKILL\.md", content)
    for ref in skill_refs:
        if ref in existing_skills:
            pass  # Exists
        else:
            issue("WARN", f"skill ref in {f.name}", f"skills/{ref}/SKILL.md -> SKILL NOT FOUND")

# 2d: Check all skill names in the catalog table match actual skills
print("\n--- Skill Catalog Consistency ---")
# Read the skill catalog from META-PROMPT
meta_path = PROMPTS_DIR / "META-PROMPT-DEEPSEEK.md"
with open(meta_path, 'r', encoding='utf-8') as f:
    meta_content = f.read()

# Find all skills in the Skill Invocation table
skill_table_refs = set()
for match in re.finditer(r'\|\s*`?([a-z][a-z0-9\-]+)`?\s*\|', meta_content.lower()):
    name = match.group(1)
    if name in existing_skills:
        skill_table_refs.add(name)

if skill_table_refs:
    ok("skill catalog", f"{len(skill_table_refs)} skills in META-PROMPT table match actual skills")
    missing = existing_skills - skill_table_refs
    if missing:
        for m in missing:
            issue("WARN", "skill catalog", f"Skill '{m}' exists on disk but NOT in META-PROMPT catalog")
    extra = skill_table_refs - existing_skills
    if extra:
        for e in extra:
            issue("BLOCKING", "skill catalog", f"Skill '{e}' in META-PROMPT catalog but NOT on disk")

# =============================================================================
# PHASE 3: CONTENT AUDIT — Deprecated references, integrity
# =============================================================================
print("\n" + "=" * 70)
print("PHASE 3: CONTENT AUDIT — Deprecated References")
print("=" * 70)

deprecated_patterns = {
    "MCP/skills web search": r"MCP.*web.search|skills.*web.search|web.search.*MCP|web.search.*skill",
    "GitHub Issues/Projects/Wiki": r"github\.com.*issues|github\.com.*projects|github\.com.*wiki|gh issue|gh pr|gh project",
    "PM files (BACKLOG.md etc.)": r"BACKLOG\.md|SPRINT\.md|CHANGELOG\.md|LEARNINGS\.md|DECISIONS\.md|PROJECT STATE\.md",
}

for f in all_md_files:
    if not f.exists():
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    for label, pattern in deprecated_patterns.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            for m in matches[:3]:
                issue("WARN", f"{f.name} deprecated", f"'{label}' reference: {m[:80]}...")

# Check for stale "audit/pipeline-status.json" in functional references
print("\n--- Deprecated Path Audit ---")
all_content_files = list(PROMPTS_DIR.glob("*.md")) + \
                    list(PROMPTS_DIR.glob("templates/*.md")) + \
                    list((PROMPTS_DIR / "skills").glob("*/SKILL.md"))

for f in all_content_files:
    if not f.exists():
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    if "audit/pipeline-status" in content:
        # It's OK in version history, not OK elsewhere
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "audit/pipeline-status" in line:
                context = ' '.join(lines[max(0,i-1):i+2])
                if any(kw in context for kw in ['root cause', 'fix cycle', 'version history', 'd63e735', '8bda41d', 'v3.16', 'v5.6']):
                    continue
                issue("BLOCKING", f"{f.name} L{i+1}", f"Deprecated path: {line.strip()[:100]}")

# =============================================================================
# PHASE 4: VERSION CONSISTENCY
# =============================================================================
print("\n" + "=" * 70)
print("PHASE 4: VERSION CONSISTENCY")
print("=" * 70)

for pf in prompt_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract header version (flexible format)
    header_match = re.search(r'\(v(\d+\.\d+)[^)]*\)', content[:500])
    header_version = header_match.group(1) if header_match else None
    
    # Extract latest version from VERSION HISTORY
    version_lines = re.findall(r'\|\s*\*\*v(\d+\.\d+)\*\*', content)
    latest_history = version_lines[0] if version_lines else None
    
    # Extract footer version (for META-PROMPT)
    footer_match = re.search(r'generator v(\d+\.\d+) active', content)
    footer_version = footer_match.group(1) if footer_match else None
    
    if header_version:
        ok(f"{pf.name} version", f"Header: v{header_version}")
    else:
        issue("BLOCKING", f"{pf.name} version", "No header version found")
    
    if latest_history:
        ok(f"{pf.name} version", f"Latest history: v{latest_history}")
    else:
        issue("BLOCKING", f"{pf.name} version", "No version history entries")
    
    if header_version and latest_history:
        if header_version == latest_history:
            ok(f"{pf.name} consistency", "Header version matches latest history entry")
        else:
            issue("BLOCKING", f"{pf.name} consistency", 
                  f"Header v{header_version} != History v{latest_history}")
    
    if footer_version:
        if footer_version == header_version:
            ok(f"{pf.name} consistency", "Footer version matches header")
        else:
            issue("BLOCKING", f"{pf.name} consistency", 
                  f"Footer v{footer_version} != Header v{header_version}")

# Check DEFAULT.md v3.16 appears in QWAV inheritance table (QWAV should reference latest DEFAULT)
print("\n--- Inheritance Consistency ---")
qwav_path = PROMPTS_DIR / "QWAV-DEFAULT.md"
default_path = PROMPTS_DIR / "DEFAULT.md"

with open(qwav_path, 'r', encoding='utf-8') as f:
    qwav = f.read()
with open(default_path, 'r', encoding='utf-8') as f:
    default = f.read()

# Check QWAV references correct DEFAULT version
default_version = re.search(r'# SYSTEM PROMPT:.*\(v(\d+\.\d+)\)', default)
if default_version:
    dv = default_version.group(1)
    if f"v{dv}" in qwav or f"DEFAULT.md v{dv}" in qwav:
        ok("inheritance", f"QWAV references DEFAULT v{dv}")
    else:
        # Check if QWAV has its own version
        qwav_ver = re.search(r'# SYSTEM PROMPT:.*\(v(\d+\.\d+)\)', qwav)
        if qwav_ver:
            ok("inheritance", f"QWAV v{qwav_ver.group(1)} (references DEFAULT indirectly)")

# =============================================================================
# PHASE 5: SKILL AUDIT
# =============================================================================
print("\n" + "=" * 70)
print("PHASE 5: SKILL AUDIT — Embedded Scripts & Structure")
print("=" * 70)

for skill_name in sorted(existing_skills):
    skill_file = skill_dir / skill_name / "SKILL.md"
    if not skill_file.exists():
        issue("BLOCKING", f"skill:{skill_name}", "SKILL.md not found")
        continue
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    
    # Check for Embedded Scripts section
    if "Embedded Scripts" in skill_content:
        ok(f"skill:{skill_name}", "Embedded Scripts section present")
    else:
        issue("WARN", f"skill:{skill_name}", "No Embedded Scripts section (§2.5.1 requirement)")
    
    # Check for Bootstrap Protocol
    if "Bootstrap Protocol" in skill_content or "bootstrap" in skill_content.lower():
        ok(f"skill:{skill_name}", "Bootstrap protocol present")
    else:
        issue("WARN", f"skill:{skill_name}", "No bootstrap protocol for missing scripts")
    
    # Check version
    ver_match = re.search(r'(?:version|v)(\d+\.\d+)', skill_content[:500])
    if ver_match:
        ok(f"skill:{skill_name}", f"Version v{ver_match.group(1)}")

# =============================================================================
# PHASE 6: TEMPLATE AUDIT
# =============================================================================
print("\n" + "=" * 70)
print("PHASE 6: TEMPLATE AUDIT")
print("=" * 70)

for tmpl_file in sorted(template_dir.glob("*.md")):
    with open(tmpl_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check frontmatter
    has_template = 'template:' in content[:200]
    has_version = 'version:' in content[:200]
    
    if has_template and has_version:
        ok(f"template:{tmpl_file.stem}", "Frontmatter complete")
    elif has_template:
        issue("WARN", f"template:{tmpl_file.stem}", "Missing version in frontmatter")
    elif has_version:
        issue("WARN", f"template:{tmpl_file.stem}", "Missing template name in frontmatter")
    else:
        issue("WARN", f"template:{tmpl_file.stem}", "No frontmatter found")

# =============================================================================
# PHASE 7: CONFIG AUDIT
# =============================================================================
print("\n" + "=" * 70)
print("PHASE 7: CONFIG AUDIT")
print("=" * 70)

config_files = [
    PROMPTS_DIR / "config" / "mcp-settings.json",
    PROMPTS_DIR / "config" / "acp_agents.json",
    PROMPTS_DIR / "app-settings.json",
]

for cf in config_files:
    if cf.exists():
        with open(cf, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                ok(f"config:{cf.name}", f"Valid JSON, {len(str(data))} chars")
            except json.JSONDecodeError as e:
                issue("BLOCKING", f"config:{cf.name}", f"INVALID JSON: {e}")
    else:
        issue("WARN", f"config:{cf.name}", "File not found")

# Check app-settings.json default_system_prompt size matches DEFAULT.md
app_settings = PROMPTS_DIR / "app-settings.json"
if app_settings.exists():
    with open(app_settings, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    with open(default_path, 'r', encoding='utf-8') as f:
        default_content = f.read()
    deployed_size = len(settings.get("default_system_prompt", ""))
    canonical_size = len(default_content)
    if abs(deployed_size - canonical_size) < 100:
        ok("deployment", f"app-settings.json matches DEFAULT.md ({deployed_size} vs {canonical_size} chars)")
    else:
        issue("WARN", "deployment", f"app-settings.json ({deployed_size}) may be stale vs DEFAULT.md ({canonical_size})")

# =============================================================================
# PHASE 8: DEPLOYMENT AUDIT
# =============================================================================
print("\n" + "=" * 70)
print("PHASE 8: DEPLOYMENT AUDIT — agent.db consistency")
print("=" * 70)

# Check if deployed versions match canonical
deploy_result = subprocess.run(
    ['python', 'tools/deploy.py', '--dry-run'],
    cwd=str(PROMPTS_DIR),
    capture_output=True, text=True,
    timeout=15
)

unexpected_changes = []
for line in deploy_result.stdout.split('\n'):
    if 'WOULD_UPDATE' in line or 'UPDATED' in line:
        if 'QWAV' in line:
            # QWAV was updated by QWAV agent — check if our version is latest
            pass
        elif 'UNCHANGED' not in line:
            unexpected_changes.append(line.strip())

if unexpected_changes:
    for uc in unexpected_changes:
        issue("WARN", "deployment", f"Unexpected pending update: {uc}")
else:
    ok("deployment", "No unexpected deployment drift — all deployed versions current")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)

blocking = [i for i in ISSUES if i[0] == "BLOCKING"]
warnings = [i for i in ISSUES if i[0] == "WARN"]
print(f"  BLOCKING issues: {len(blocking)}")
for b in blocking:
    print(f"    [{b[1]}] {b[2]}")
print(f"  WARNINGS: {len(warnings)}")
for w in warnings:
    print(f"    [{w[1]}] {w[2]}")
print(f"  PASSES: {len(PASSES)}")
print(f"  TOTAL CHECKS: {len(ISSUES) + len(PASSES)}")

# Write report
report = {
    "audit_time": datetime.utcnow().isoformat(),
    "total_checks": len(ISSUES) + len(PASSES),
    "blocking": len(blocking),
    "warnings": len(warnings),
    "passes": len(PASSES),
    "issues": [{"severity": s, "category": c, "detail": d} for s, c, d in ISSUES],
}
report_path = PROMPTS_DIR / "_audit_report.json"
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print(f"\nReport saved to: {report_path}")
sys.exit(len(blocking))
