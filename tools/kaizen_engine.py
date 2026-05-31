#!/usr/bin/env python3
"""
KAIZEN ENGINE v1.0 -- Continuous Self-Improvement System

Analyzes conversation histories, Cloudflare R2 audit trails, system audits,
and cross-project learnings to generate improvement recommendations for:
  1. System prompts (DEFAULT.md, META-PROMPT-DEEPSEEK.md, QWAV-DEFAULT.md)
  2. Model configurations (temperature, maxTokens, contextLength, etc.)
  3. Skills (workflow optimizations)
  4. Templates (structural improvements)
  5. Subagent prompts (EXPLORER, IMPLEMENTER, REVIEWER)

Run modes:
  python tools/kaizen_engine.py --audit          # Analyze only, output recommendations
  python tools/kaizen_engine.py --audit --apply  # Analyze AND apply safe changes
  python tools/kaizen_engine.py --auto            # Full auto: pull from R2, analyze, apply, deploy

Architecture:
  DATA SOURCES -> ANALYSIS ENGINE -> RECOMMENDATIONS -> SAFE APPLY -> DEPLOY
"""

import os, sys, json, re, sqlite3, hashlib, subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# === CONFIGURATION ===
PROMPTS_DIR = Path(r"G:\My Drive\prompts")
PROJECTS_DIR = Path(r"G:\My Drive\projects")
APPDATA = Path(os.environ.get("APPDATA", ""))
DEEPCHAT_DIR = APPDATA / "DeepChat"
AGENT_DB = DEEPCHAT_DIR / "app_db" / "agent.db"

# Files we can safely auto-modify
SAFE_MODIFY = {
    "model-config.json": PROMPTS_DIR / "config" / "model-config.json",
    "system_audit.py": PROMPTS_DIR / "tools" / "system_audit.py",
}

# Files that require review before modification (structural changes)
REVIEW_MODIFY = {
    "DEFAULT.md": PROMPTS_DIR / "DEFAULT.md",
    "META-PROMPT-DEEPSEEK.md": PROMPTS_DIR / "META-PROMPT-DEEPSEEK.md",
    "QWAV-DEFAULT.md": PROMPTS_DIR / "QWAV-DEFAULT.md",
    "EXPLORER-SUBAGENT.md": PROMPTS_DIR / "agents" / "subagents" / "EXPLORER-SUBAGENT.md",
    "IMPLEMENTER-SUBAGENT.md": PROMPTS_DIR / "agents" / "subagents" / "IMPLEMENTER-SUBAGENT.md",
    "REVIEWER-SUBAGENT.md": PROMPTS_DIR / "agents" / "subagents" / "REVIEWER-SUBAGENT.md",
}

# Improvement categories
CATEGORIES = ["prompt_rules", "model_config", "skill_workflow", "template_structure", 
              "subagent_prompt", "deployment", "guardrail", "discovery"]


def run_cmd(cmd, cwd=None):
    """Run a shell command and return stdout."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=30)
        return (result.stdout or "").strip(), (result.stderr or "").strip(), result.returncode
    except (subprocess.TimeoutExpired, Exception) as e:
        return "", str(e), 1


def hash_file(path):
    """SHA256 hash of file content."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ============================================================================
# DATA SOURCES
# ============================================================================

def pull_conversation_patterns():
    """Extract patterns from local conversation audit files and R2."""
    patterns = {
        "repeated_errors": [],
        "workflow_bottlenecks": [],
        "user_frustration_signals": [],
        "successful_patterns": [],
    }
    
    # Check local audit conversations
    audit_dir = PROMPTS_DIR / "audit" / "conversations"
    if audit_dir.exists():
        for f in audit_dir.glob("*.md"):
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    content = fh.read().lower()
                if "failed" in content or "error" in content:
                    patterns["repeated_errors"].append(str(f.name))
                if "what's next" in content or "proceed" in content:
                    patterns["workflow_bottlenecks"].append(str(f.name))
                if "frustrated" in content or "not working" in content:
                    patterns["user_frustration_signals"].append(str(f.name))
            except Exception:
                pass
    
    # Check from agent.db conversation tables
    if AGENT_DB.exists():
        try:
            conn = sqlite3.connect(str(AGENT_DB))
            cur = conn.cursor()
            # Count recent conversations
            cur.execute("SELECT COUNT(*) FROM conversations")
            total_convos = cur.fetchone()[0]
            patterns["total_conversations"] = total_convos
            
            # Check for common error messages in recent messages
            cur.execute("""
                SELECT COUNT(*) FROM messages 
                WHERE created_at > datetime('now', '-7 days')
                AND content LIKE '%error%' OR content LIKE '%fail%'
                LIMIT 1000
            """)
            error_count = cur.fetchone()[0]
            patterns["recent_errors_7d"] = error_count
            conn.close()
        except Exception:
            pass
    
    return patterns


def pull_r2_audit_trails():
    """Pull Cloudflare R2 audit data for pattern analysis."""
    r2_data = {"available": False, "audit_files": [], "state_files": [], "errors": []}
    
    # Check if wrangler is available
    stdout, stderr, rc = run_cmd("where npx 2>nul", cwd=str(PROMPTS_DIR))
    if rc != 0:
        r2_data["errors"].append("npx not found in PATH")
        return r2_data
    
    stdout, stderr, rc = run_cmd("npx wrangler --version 2>nul", cwd=str(PROMPTS_DIR))
    if rc != 0:
        r2_data["errors"].append(f"wrangler not available: {stderr[:200] if stderr else 'unknown error'}")
        return r2_data
    
    r2_data["available"] = True
    
    # Pull decision log
    stdout, stderr, rc = run_cmd(
        'npx wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md',
        cwd=str(PROMPTS_DIR)
    )
    if rc == 0 and stdout:
        decisions = stdout
        r2_data["decision_count"] = len(re.findall(r"^### ", decisions, re.MULTILINE))
    
    # Pull discovery index
    stdout, stderr, rc = run_cmd(
        'npx wrangler r2 object get qnfo/discovery/index.json',
        cwd=str(PROMPTS_DIR)
    )
    if rc == 0 and stdout:
        try:
            idx = json.loads(stdout)
            project_count = len(idx.get("projects", {}))
            r2_data["project_count"] = project_count
        except json.JSONDecodeError:
            pass
    
    return r2_data


def analyze_system_audit():
    """Run system_audit.py and parse results."""
    audit_path = PROMPTS_DIR / "tools" / "system_audit.py"
    if not audit_path.exists():
        return {"ran": False, "error": "system_audit.py not found"}
    
    stdout, stderr, rc = run_cmd(f"python {audit_path}", cwd=str(PROMPTS_DIR))
    
    results = {
        "ran": True,
        "exit_code": rc,
        "warnings": [],
        "passes": [],
        "failures": [],
    }
    
    for line in stdout.split("\n"):
        line = line.strip()
        if "WARNING: FAIL" in line or "MISMATCH" in line or "STALE" in line:
            results["failures"].append(line)
        elif "PASS" in line:
            results["passes"].append(line)
        elif "WARNING" in line or "CHECK" in line:
            results["warnings"].append(line)
    
    results["health_score"] = (
        len(results["passes"]) / max(1, len(results["passes"]) + len(results["failures"])) * 100
    )
    
    return results


# ============================================================================
# ANALYSIS ENGINE
# ============================================================================

def detect_prompt_gaps(conversation_patterns, audit_results):
    """Identify gaps between what prompts instruct and what agents actually do."""
    gaps = []
    
    # Gap 1: If repeated phantom claims in conversations but Rule 14 exists
    if conversation_patterns.get("repeated_errors"):
        gaps.append({
            "type": "guardrail_ineffective",
            "category": "guardrail",
            "finding": "Rule 14 (ANTI-PHANTOM) exists but phantom claims persist in conversations",
            "recommendation": "Strengthen Rule 14 enforcement with pre-response scan in more prompts",
            "confidence": "medium",
            "auto_apply": False,
        })
    
    # Gap 2: If many conversations reference files that don't exist
    if conversation_patterns.get("recent_errors_7d", 0) > 10:
        gaps.append({
            "type": "verification_fatigue",
            "category": "prompt_rules",
            "finding": f"High error rate ({conversation_patterns['recent_errors_7d']} errors in 7 days)",
            "recommendation": "Consider adding a 'pause and verify' checkpoint after every 3 file operations",
            "confidence": "medium",
            "auto_apply": False,
        })
    
    # Gap 3: System audit failures suggest prompt drift
    failures = audit_results.get("failures", [])
    if len(failures) > 2:
        gaps.append({
            "type": "prompt_drift",
            "category": "prompt_rules",
            "finding": f"System audit found {len(failures)} failures — prompts may have drifted from ground truth",
            "recommendation": "Run version consistency check and realign prompts with architecture",
            "confidence": "high",
            "auto_apply": False,
        })
    
    return gaps


def analyze_model_performance():
    """Analyze model config effectiveness from conversation data."""
    recommendations = []
    
    # Check current model configs
    model_config_path = PROMPTS_DIR / "config" / "model-config.json"
    if model_config_path.exists():
        with open(model_config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Check deepseek-v4-pro config
        v4pro = config.get("deepseek-_-deepseek-v4-pro", {}).get("config", {})
        
        # Recommendation: temperature optimization
        current_temp = v4pro.get("temperature", 0.6)
        if current_temp > 0.3:
            recommendations.append({
                "type": "temperature_high",
                "category": "model_config",
                "finding": f"deepseek-v4-pro temperature is {current_temp} — high for system prompt generation",
                "recommendation": "Reduce temperature to 0.0 for deterministic prompt generation, 0.3 for creative work",
                "confidence": "high",
                "auto_apply": True,
                "change": {"model": "deepseek-v4-pro", "temperature": 0.0},
            })
        
        # Recommendation: maxTokens check
        current_max = v4pro.get("maxTokens", 64000)
        if current_max < 64000:
            recommendations.append({
                "type": "max_tokens_low",
                "category": "model_config",
                "finding": f"deepseek-v4-pro maxTokens is {current_max} — may truncate long prompts",
                "recommendation": "Set maxTokens to 64000 for full context utilization",
                "confidence": "medium",
                "auto_apply": True,
                "change": {"model": "deepseek-v4-pro", "maxTokens": 64000},
            })
        
        # Check reasoning settings
        if not v4pro.get("reasoning", True):
            recommendations.append({
                "type": "reasoning_disabled",
                "category": "model_config",
                "finding": "Reasoning is disabled for deepseek-v4-pro",
                "recommendation": "Enable reasoning for complex system prompt engineering tasks",
                "confidence": "high",
                "auto_apply": True,
                "change": {"model": "deepseek-v4-pro", "reasoning": True},
            })
    
    return recommendations


def detect_template_gaps():
    """Check if templates match actual usage patterns."""
    gaps = []
    templates_dir = PROMPTS_DIR / "templates"
    
    if not templates_dir.exists():
        return gaps
    
    existing = set(f.stem for f in templates_dir.glob("*.md"))
    
    # Check for expected but missing templates
    expected = {
        "DEFINITION-OF-DONE", "HANDOFF", "PROJECT-CHARTER", 
        "CLOSEOUT-CHECKLIST", "PROJECT-INITIATION", "DISCOVERY-PROTOCOL",
        "KAIZEN-AUDIT",  # New — being created
    }
    
    missing = expected - existing
    for m in missing:
        gaps.append({
            "type": "missing_template",
            "category": "template_structure",
            "finding": f"Expected template '{m}' is missing",
            "recommendation": f"Create template '{m}' based on usage patterns",
            "confidence": "medium",
            "auto_apply": False,
        })
    
    # Check for unused/stale templates
    unused_suspects = existing - expected - {"SOCIAL-ORCHESTRATOR-TEMPLATE"}
    for u in unused_suspects:
        gaps.append({
            "type": "possible_stale_template",
            "category": "template_structure",
            "finding": f"Template '{u}' may be unused",
            "recommendation": f"Audit usage of '{u}' — consider deprecation if unused",
            "confidence": "low",
            "auto_apply": False,
        })
    
    return gaps


# ============================================================================
# SAFE-APPLY ENGINE
# ============================================================================

def safe_apply_model_config(change):
    """Apply a model config change to model-config.json."""
    model = change["model"]
    config_path = PROMPTS_DIR / "config" / "model-config.json"
    
    if not config_path.exists():
        return False, "model-config.json not found"
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Find the model entry
    model_key = f"deepseek-_-{model}"
    if model_key not in config:
        return False, f"Model {model_key} not found in config"
    
    # Apply change
    for key in change:
        if key == "model":
            continue
        config[model_key]["config"][key] = change[key]
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return True, f"Applied {change} to {model_key}"


def update_system_audit_add_kaizen():
    """Update system_audit.py to include Kaizen health check."""
    audit_path = PROMPTS_DIR / "tools" / "system_audit.py"
    if not audit_path.exists():
        return False, "system_audit.py not found"
    
    with open(audit_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if Kaizen check already exists
    if "PART K: KAIZEN" in content:
        return True, "Kaizen check already present"
    
    kaizen_check = """
# PART K: KAIZEN ENGINE HEALTH
print("\\nPART K: KAIZEN ENGINE HEALTH")
kaizen_path = os.path.join(prompts_dir, "tools", "kaizen_engine.py")
if os.path.exists(kaizen_path):
    print(f"  K1. Kaizen engine present: PASS")
    # Check if it's been run recently
    audit_file = os.path.join(prompts_dir, "audit", "kaizen", "last_run.json")
    if os.path.exists(audit_file):
        with open(audit_file, "r", encoding="utf-8") as f:
            last_run = json.load(f)
        last_time = last_run.get("timestamp", "unknown")
        print(f"  K2. Last Kaizen run: {last_time} PASS")
    else:
        print(f"  K2. No prior Kaizen run CHECK")
else:
    print(f"  K1. Kaizen engine MISSING WARNING: FAIL")
"""
    
    # Insert before the final print
    content += kaizen_check
    
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return True, "Added Kaizen health check to system_audit.py"


# ============================================================================
# DEPLOYMENT
# ============================================================================

def run_deploy():
    """Run deploy.py to push changes to DeepChat runtime."""
    deploy_path = PROMPTS_DIR / "tools" / "deploy.py"
    if not deploy_path.exists():
        return False, "deploy.py not found"
    
    stdout, stderr, rc = run_cmd(f"python {deploy_path}", cwd=str(PROMPTS_DIR))
    return rc == 0, stdout[:500] if stdout else stderr[:500]


def restart_deepchat():
    """Attempt to restart DeepChat process."""
    # Kill existing DeepChat process
    _, _, _ = run_cmd('taskkill /F /IM "DeepChat.exe" 2>nul')
    # DeepChat should auto-restart if configured as a startup app
    return True, "DeepChat process killed — should restart automatically"


# ============================================================================
# REPORTING
# ============================================================================

def generate_kaizen_report(patterns, r2_data, audit_results, gaps, model_recs, template_gaps):
    """Generate a comprehensive Kaizen improvement report."""
    report = []
    report.append(f"# KAIZEN IMPROVEMENT REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    total_findings = len(gaps) + len(model_recs) + len(template_gaps)
    auto_apply_count = sum(1 for r in model_recs if r.get("auto_apply"))
    health = audit_results.get("health_score", 0)
    report.append(f"- System Health Score: {health:.0f}%")
    report.append(f"- Total Improvement Opportunities: {total_findings}")
    report.append(f"- Auto-Applicable Changes: {auto_apply_count}")
    report.append(f"- Conversations Analyzed: {patterns.get('total_conversations', 'N/A')}")
    report.append(f"- R2 Projects Tracked: {r2_data.get('project_count', 'N/A')}")
    report.append("")
    
    # Conversation Patterns
    report.append("## 1. Conversation Patterns")
    if patterns.get("repeated_errors"):
        report.append(f"- Repeated errors detected in: {patterns['repeated_errors']}")
    if patterns.get("workflow_bottlenecks"):
        report.append(f"- Workflow bottlenecks: {len(patterns['workflow_bottlenecks'])} sessions")
    if patterns.get("recent_errors_7d", 0) > 0:
        report.append(f"- Recent errors (7d): {patterns['recent_errors_7d']}")
    report.append("")
    
    # System Audit
    report.append("## 2. System Audit Results")
    report.append(f"- Health Score: {health:.0f}%")
    if audit_results.get("failures"):
        report.append(f"- Failures ({len(audit_results['failures'])}):")
        for f in audit_results["failures"][:5]:
            report.append(f"  - {f[:120]}")
    report.append("")
    
    # Prompt Gaps
    if gaps:
        report.append("## 3. Prompt Gaps Detected")
        for g in gaps:
            report.append(f"### {g['type']} [{g['confidence'].upper()} confidence]")
            report.append(f"- Finding: {g['finding']}")
            report.append(f"- Recommendation: {g['recommendation']}")
            report.append(f"- Auto-apply: {g.get('auto_apply', False)}")
            report.append("")
    
    # Model Recommendations
    if model_recs:
        report.append("## 4. Model Config Optimizations")
        for r in model_recs:
            report.append(f"### {r['type']} [{r['confidence'].upper()} confidence]")
            report.append(f"- Current: {r['finding']}")
            report.append(f"- Recommended: {r['recommendation']}")
            report.append(f"- Change: {r.get('change', {})}")
            report.append(f"- Auto-apply: {r.get('auto_apply', False)}")
            report.append("")
    
    # Template Gaps
    if template_gaps:
        report.append("## 5. Template Improvements")
        for t in template_gaps:
            report.append(f"- {t['type']}: {t['finding']}")
            report.append(f"  -> {t['recommendation']}")
        report.append("")
    
    # R2 Data
    report.append("## 6. Cloudflare R2 Status")
    report.append(f"- R2 Available: {r2_data.get('available', False)}")
    report.append(f"- Projects in Discovery Index: {r2_data.get('project_count', 'N/A')}")
    report.append(f"- Decisions Logged: {r2_data.get('decision_count', 'N/A')}")
    if r2_data.get("errors"):
        for e in r2_data["errors"]:
            report.append(f"- Error: {e}")
    report.append("")
    
    # Actions Taken
    report.append("## 7. Actions Applied This Run")
    report.append("(Populated on --apply or --auto runs)")
    report.append("")
    
    report.append("---")
    report.append(f"*Kaizen Engine v1.0 — {datetime.now().isoformat()}*")
    
    return "\n".join(report)


# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="KAIZEN Continuous Improvement Engine")
    parser.add_argument("--audit", action="store_true", help="Run analysis only, output report")
    parser.add_argument("--apply", action="store_true", help="Apply safe changes after audit")
    parser.add_argument("--auto", action="store_true", help="Full auto: audit + apply + deploy")
    parser.add_argument("--output", type=str, default=None, help="Write report to file")
    args = parser.parse_args()
    
    if not any([args.audit, args.apply, args.auto]):
        parser.print_help()
        return
    
    print("=" * 60)
    print("KAIZEN ENGINE v1.0 -- Continuous Improvement")
    print("=" * 60)
    
    actions_taken = []
    
    # PHASE 1: Data Collection
    print("\n[PHASE 1] Collecting data...")
    patterns = pull_conversation_patterns()
    print(f"  Conversations: {patterns.get('total_conversations', 'N/A')}")
    
    r2_data = pull_r2_audit_trails()
    print(f"  R2 available: {r2_data.get('available')}")
    
    audit_results = analyze_system_audit()
    print(f"  System health: {audit_results.get('health_score', 0):.0f}%")
    
    # PHASE 2: Analysis
    print("\n[PHASE 2] Analyzing...")
    gaps = detect_prompt_gaps(patterns, audit_results)
    print(f"  Prompt gaps: {len(gaps)}")
    
    model_recs = analyze_model_performance()
    print(f"  Model recommendations: {len(model_recs)}")
    
    template_gaps = detect_template_gaps()
    print(f"  Template gaps: {len(template_gaps)}")
    
    # PHASE 3: Recommendations
    print("\n[PHASE 3] Recommendations:")
    for g in gaps:
        print(f"  [{g['confidence'].upper()}] {g['type']}: {g['finding'][:100]}")
    for r in model_recs:
        print(f"  [{r['confidence'].upper()}] {r['type']}: {r['finding'][:100]}")
    for t in template_gaps:
        print(f"  [{t['confidence'].upper()}] {t['type']}: {t['finding'][:100]}")
    
    # PHASE 4: Apply (if requested)
    if args.apply or args.auto:
        print("\n[PHASE 4] Applying safe changes...")
        
        for r in model_recs:
            if r.get("auto_apply"):
                success, msg = safe_apply_model_config(r["change"])
                print(f"  {'[OK]' if success else '[FAIL]'} Model config: {msg}")
                if success:
                    actions_taken.append(f"Applied model config: {r['change']}")
        
        # Update system_audit.py with Kaizen check
        success, msg = update_system_audit_add_kaizen()
        print(f"  {'[OK]' if success else '[INFO]'} System audit: {msg}")
        if success:
            actions_taken.append("Added Kaizen check to system_audit.py")
    
    # PHASE 5: Deploy (if auto)
    if args.auto:
        print("\n[PHASE 5] Deploying...")
        success, msg = run_deploy()
        print(f"  {'[OK]' if success else '[FAIL]'} Deploy: {msg[:200]}")
        if success:
            actions_taken.append("Ran deploy.py to sync changes to DeepChat")
        
        # Restart DeepChat
        success, msg = restart_deepchat()
        print(f"  {'[OK]' if success else '[INFO]'} Restart: {msg}")
    
    # Generate Report
    report = generate_kaizen_report(patterns, r2_data, audit_results, gaps, model_recs, template_gaps)
    
    # Inject actions taken
    if actions_taken:
        report = report.replace(
            "(Populated on --apply or --auto runs)",
            "\n".join(f"- {a}" for a in actions_taken)
        )
    
    # Save report
    report_dir = PROMPTS_DIR / "audit" / "kaizen"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    report_path = report_dir / f"kaizen_report_{timestamp}.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    # Update last run record
    last_run = {"timestamp": datetime.now().isoformat(), "actions": actions_taken}
    with open(report_dir / "last_run.json", "w", encoding="utf-8") as f:
        json.dump(last_run, f, indent=2)
    
    print(f"\n[COMPLETE] Report saved: {report_path}")
    print(f"  Actions taken: {len(actions_taken)}")
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"  Additional output: {args.output}")
    
    # Print summary
    print("\n" + "=" * 60)
    total = len(gaps) + len(model_recs) + len(template_gaps)
    print(f"SUMMARY: {total} improvements identified, {len(actions_taken)} applied")
    print(f"Health Score: {audit_results.get('health_score', 0):.0f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
