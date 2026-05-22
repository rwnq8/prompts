#!/usr/bin/env python3
"""
SYSTEM CONSISTENCY AUDIT — v1.0
================================
Proactively detects hardcoded numeric claims about templates/documentation
files that have drifted from reality. Run this after any template is added,
removed, or renamed.

Trigger: "SYSTEM CONSISTENCY AUDIT" command, or as part of SYSTEM HEALTH CHECK.

Checks:
  A. Hardcoded counts in system prompts vs actual template count
  B. Cross-references between templates (does template A reference a file
     that template B should generate?)
  C. Template-to-file mapping consistency
  D. Stale CPL lesson references

Output: Pass/Fail per check with specific line numbers for violations.
"""

import os
import re
import json
from pathlib import Path

# === CONFIGURATION ===

PROMPTS_DIR = Path(r'G:\My Drive\prompts')
SHARED_DIR = Path(r'G:\My Drive\projects\_shared')

# Known template-to-file mapping (all file-generating templates)
# Update this when templates are added/removed
TEMPLATE_FILE_MAP = {
    # Tier 1: Core Initialization
    'README-TEMPLATE': 'README.md',
    'PROJECT-STATE-TEMPLATE': 'PROJECT STATE.md',
    'SPRINT-BACKLOG-TEMPLATE': 'SPRINT.md',
    'CHANGELOG-TEMPLATE': 'CHANGELOG.md',
    'PRODUCT-BACKLOG-TEMPLATE': 'BACKLOG.md',
    'LEARNINGS-TEMPLATE': 'LEARNINGS.md',
    'ADR-TEMPLATE': 'DECISIONS.md',
    # Tier 2: Phase-Gated
    'DEFINITION-OF-DONE-TEMPLATE': 'DEFINITION-OF-DONE.md',
    'CONTRIBUTING-TEMPLATE': 'CONTRIBUTING.md',
    'PROJECT-CHARTER-TEMPLATE': 'PROJECT-CHARTER.md',
    'RISK-REGISTER-TEMPLATE': 'RISK-REGISTER.md',
    'CLOSEOUT-CHECKLIST-TEMPLATE': 'CLOSEOUT-CHECKLIST.md',
    # Tier 3: Situational
    'QA-QC-TESTING-PROTOCOL': 'QA-QC-TESTING-PROTOCOL.md',
    'TEST-EVIDENCE-TEMPLATE': 'test-evidence-*.md',
    'WEB-APP-RELEASE-CHECKLIST': 'RELEASE-CHECKLIST-*.md',
    'RETROSPECTIVE-TEMPLATE': 'RETROSPECTIVE-*.md',
    'HANDOFF-TEMPLATE': 'HANDOFF-*.md',
}

# All 27 templates
ALL_TEMPLATES = [
    'STAGE-1-SETUP', 'STAGE-2-DRAFT', 'STAGE-3-REVIEW', 'STAGE-4-PUBLISH',
    'SPRINT-BACKLOG-TEMPLATE', 'PROJECT-CHARTER-TEMPLATE', 'PRODUCT-BACKLOG-TEMPLATE',
    'RISK-REGISTER-TEMPLATE', 'RETROSPECTIVE-TEMPLATE', 'README-TEMPLATE',
    'HANDOFF-TEMPLATE', 'DEFINITION-OF-DONE-TEMPLATE', 'CONTRIBUTING-TEMPLATE',
    'CHANGELOG-TEMPLATE', 'ADR-TEMPLATE', 'QA-QC-TESTING-PROTOCOL',
    'TEST-EVIDENCE-TEMPLATE', 'WEB-APP-RELEASE-CHECKLIST', 'CLOSEOUT-CHECKLIST-TEMPLATE',
    'LEARNINGS-TEMPLATE', 'PROJECT-STATE-TEMPLATE',
    'EMAIL-AGENT-TEMPLATE', 'SOCIAL-ORCHESTRATOR-TEMPLATE', 'image-gen-banner-prompt',
    # 3 non-standard names:
    '1. What explicit choices were made, by whom, and when? 2. What implicit choices went unnoticed? 3. What connections could have been made but weren\u2019t?',
    'A first-principles convergence/consilience; no jargon, no esoteric terminology, no domain siloes, no proper names/nouns as authorities; it must be supported entirely but its own logic and clarity of its arguments. The language must be plain and self-contained, accessible to anyone with no prior knowledge.',
    'Cleanup Actions \u2014 What to do about root .git, projects directory  New Cross-Project Lessons \u2014 From the archive LEARNINGS review  System Prompt Updates \u2014 What needs updating  Process Enhancements \u2014 What can be improved in project lifecycle',
]

TOTAL_TEMPLATES = len(ALL_TEMPLATES)
TOTAL_FILE_GENERATING = len(TEMPLATE_FILE_MAP)
TIER1_COUNT = 7  # Core initialization files
TIER2_COUNT = 5  # Phase-gated files
TIER3_COUNT = 5  # Situational files

# System prompts to audit
SYSTEM_PROMPTS = [
    'DEFAULT.md',
    'QWAV-DEFAULT.md',
    'META-PROMPT-DEEPSEEK.md',
    'ARCHITECTURE.md',
]

# === AUDIT FUNCTIONS ===

class AuditResult:
    def __init__(self):
        self.passes = []
        self.warnings = []
        self.failures = []

    def add_pass(self, msg):
        self.passes.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_failure(self, msg):
        self.failures.append(msg)

    def summary(self):
        lines = []
        lines.append(f'PASS: {len(self.passes)}')
        lines.append(f'WARN: {len(self.warnings)}')
        lines.append(f'FAIL: {len(self.failures)}')
        return '\n'.join(lines)

    def is_clean(self):
        return len(self.failures) == 0 and len(self.warnings) == 0


def check_hardcoded_counts(result):
    """A. Check for hardcoded numeric claims about docs/templates in system prompts."""
    patterns = [
        # (regex, description, expected_context)
        (r'\b7\s+mandatory\s+doc', 'Hardcoded "7 mandatory doc(s)"', 'Should be "Tier 1 core files" or tiered reference'),
        (r'\bALL\s+7\s+MANDATORY\s+DOCS', 'Hardcoded "ALL 7 MANDATORY DOCS"', 'Should be "ALL CORE + PHASE DOCS"'),
        (r'\ball\s+7\s+docs?\b', 'Hardcoded "all 7 docs"', 'Should reference tiered model'),
        (r'\b7-file\s+documentation', 'Hardcoded "7-file documentation"', 'Should be "tiered documentation"'),
        (r'\bThese\s+7\s+files\s+use\s+fixed\s+names', 'Hardcoded "These 7 files use fixed names"', 'Should be "Tier 1 core files"'),
    ]

    for fname in SYSTEM_PROMPTS:
        fpath = PROMPTS_DIR / fname
        if not fpath.exists():
            result.add_warning(f'System prompt not found: {fname}')
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern, desc, suggestion in patterns:
            for m in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:m.start()].count('\n') + 1
                ctx = content[max(0, m.start()-20):m.end()+30].replace('\n', ' ')
                result.add_failure(
                    f'{fname}:{line_num}: {desc} -- found: "...{ctx}..." -- {suggestion}'
                )

    if not any('Hardcoded' in f for f in result.failures):
        result.add_pass('A. No stale hardcoded "7" references found in system prompts')


def check_template_count_claims(result):
    """B. Check if any system prompt claims a specific template count that's wrong."""
    # Look for patterns like "X mandatory documentation files" where X != TIER1_COUNT
    # or "X templates" where X != TOTAL_TEMPLATES
    count_claim = re.compile(r'(\d+)\s+(mandatory|required|documentation)\s+(files?|docs?)')

    for fname in SYSTEM_PROMPTS:
        fpath = PROMPTS_DIR / fname
        if not fpath.exists():
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        for m in count_claim.finditer(content):
            claimed = int(m.group(1))
            line_num = content[:m.start()].count('\n') + 1
            if claimed != TIER1_COUNT and 'Tier 1' not in content[max(0,m.start()-50):m.end()+50]:
                result.add_warning(
                    f'{fname}:{line_num}: Claims "{m.group(0)}" -- actual Tier 1 count is {TIER1_COUNT}'
                )

    result.add_pass('B. Template count claims verified')


def check_cross_references(result):
    """C. Check template cross-references for broken links."""
    # Templates that reference files generated by OTHER templates
    cross_refs = {
        'SPRINT-BACKLOG-TEMPLATE': ['DEFINITION-OF-DONE.md'],
        'PROJECT-STATE-TEMPLATE': ['RISK-REGISTER.md'],
        'CONTRIBUTING-TEMPLATE': ['DEFINITION-OF-DONE.md', 'RISK-REGISTER.md'],
        'PROJECT-CHARTER-TEMPLATE': ['DEFINITION-OF-DONE.md'],
    }

    # Verify each referenced file has a generating template
    all_generated_files = set(TEMPLATE_FILE_MAP.values())
    # Also add wildcard patterns
    static_files = {f for f in all_generated_files if '*' not in f}

    for template, refs in cross_refs.items():
        for ref in refs:
            if ref not in static_files:
                result.add_failure(
                    f'Cross-ref: {template} references "{ref}" but no template generates it'
                )

    result.add_pass('C. Template cross-references verified')


def check_template_registry(result):
    """D. Verify template registry is complete."""
    expected = len(ALL_TEMPLATES)
    file_gen = len(TEMPLATE_FILE_MAP)

    result.add_pass(f'D. Template registry: {expected} total, {file_gen} file-generating')

    # Check that all Tier 1-3 counts add up
    tier_total = TIER1_COUNT + TIER2_COUNT + TIER3_COUNT
    if tier_total != file_gen:
        result.add_failure(
            f'Tier counts ({TIER1_COUNT}+{TIER2_COUNT}+{TIER3_COUNT}={tier_total}) '
            f'do not match TEMPLATE_FILE_MAP count ({file_gen})'
        )
    else:
        result.add_pass(f'D. Tier counts consistent: {TIER1_COUNT}+{TIER2_COUNT}+{TIER3_COUNT}={file_gen}')


def check_cpl_references(result):
    """E. Check CROSS-PROJECT-LEARNINGS.md for stale references."""
    cpl_path = SHARED_DIR / 'CROSS-PROJECT-LEARNINGS.md'
    if not cpl_path.exists():
        result.add_warning('CROSS-PROJECT-LEARNINGS.md not found')
        return

    with open(cpl_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check L21 specifically
    l21_match = re.search(r'L21.*?(?=L22|\Z)', content, re.DOTALL)
    if l21_match:
        l21_text = l21_match.group()
        if re.search(r'\ball 7 docs\b', l21_text, re.IGNORECASE):
            result.add_failure('CPL L21: Still references "all 7 docs" instead of tiered model')
        else:
            result.add_pass('E. CPL L21 updated to tiered model')

    # Check for any other stale "7" references in CPL
    stale_7 = re.findall(r'(?:^|\n)\| L\d+.*?\b7\s+(?:mandatory\s+)?docs?\b', content)
    for match in stale_7:
        result.add_failure(f'CPL: Stale "7 docs" reference: {match.strip()[:100]}')


def run_full_audit():
    """Run all consistency checks."""
    result = AuditResult()

    print('=' * 60)
    print('SYSTEM CONSISTENCY AUDIT v1.0')
    print(f'Templates: {TOTAL_TEMPLATES} total, {TOTAL_FILE_GENERATING} file-generating')
    print(f'Tiers: {TIER1_COUNT} core + {TIER2_COUNT} phase + {TIER3_COUNT} situational = {TIER1_COUNT+TIER2_COUNT+TIER3_COUNT}')
    print('=' * 60)
    print()

    check_hardcoded_counts(result)
    check_template_count_claims(result)
    check_cross_references(result)
    check_template_registry(result)
    check_cpl_references(result)

    print()
    print('--- RESULTS ---')
    for p in result.passes:
        print(f'  [PASS] {p}')
    for w in result.warnings:
        print(f'  [WARN] {w}')
    for f in result.failures:
        print(f'  [FAIL] {f}')

    print()
    print(result.summary())

    if result.is_clean():
        print('\n*** AUDIT CLEAN: No consistency violations detected. ***')
        return 0
    else:
        print('\n*** AUDIT FAILED: Consistency violations found. Fix before proceeding. ***')
        return 1


if __name__ == '__main__':
    exit(run_full_audit())
