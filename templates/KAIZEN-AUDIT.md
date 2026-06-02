---
template: KAIZEN-AUDIT
version: 1.0
---

# KAIZEN-AUDIT TEMPLATE v1.0

> **Purpose:** Structured improvement audit report for continuous self-enhancement
> **Cadence:** Every session start (automated) + weekly deep audit
> **Output:** Saved to `audit/kaizen/kaizen_report_YYYY-MM-DD_HHMM.md`

---

## EXECUTIVE SUMMARY

| Metric | Value |
|:-------|:------|
| System Health Score | {{health_score}}% |
| Total Improvement Opportunities | {{total_findings}} |
| Auto-Applied This Run | {{auto_applied_count}} |
| Conversations Analyzed | {{conversations_analyzed}} |
| R2 Projects Tracked | {{r2_projects}} |
| Last Deployment | {{last_deploy}} |

---

## 1. CONVERSATION PATTERNS

### 1.1 Error Patterns (7-Day Window)

{{#if repeated_errors}}
| Pattern | Frequency | Severity | Root Prompt Section |
|:--------|:----------|:---------|:--------------------|
{{#each repeated_errors}}
| {{pattern}} | {{frequency}} | {{severity}} | {{root_section}} |
{{/each}}
{{else}}
No repeated error patterns detected.
{{/if}}

### 1.2 Success Patterns

| Pattern | Evidence | Can Encode in Prompt? |
|:--------|:---------|:----------------------|
{{#each success_patterns}}
| {{pattern}} | {{evidence}} | {{encodable}} |
{{/each}}

### 1.3 User Friction Signals

{{#if frustration_signals}}
Conversations with explicit frustration/confusion signals: {{frustration_count}}
- Root cause analysis needed for sessions: {{frustration_sessions}}
{{else}}
No friction signals in recent conversations.
{{/if}}

---

## 2. SYSTEM AUDIT RESULTS

| Check | Status | Detail |
|:------|:-------|:-------|
| PART A: Git Contamination | {{a_status}} | {{a_detail}} |
| PART B: Prompt Consistency | {{b_status}} | {{b_detail}} |
| PART C: Documentation Drift | {{c_status}} | {{c_detail}} |
| PART D: Archive Integrity | {{d_status}} | {{d_detail}} |
| PART E: Cross-File Versions | {{e_status}} | {{e_detail}} |
| PART F: Template Integration | {{f_status}} | {{f_detail}} |
| PART K: KAIZEN Health | {{k_status}} | {{k_detail}} |

---

## 3. PROMPT GAP ANALYSIS

### 3.1 Rules Effectiveness

| Rule | Effective? | Evidence | Recommendation |
|:-----|:-----------|:---------|:---------------|
| Rule 1: Do Not Simulate Tools | {{r1_eff}} | {{r1_ev}} | {{r1_rec}} |
| Rule 2: Verify Quantitative Claims | {{r2_eff}} | {{r2_ev}} | {{r2_rec}} |
| Rule 5: Never Invent Data | {{r5_eff}} | {{r5_ev}} | {{r5_rec}} |
| Rule 14: ANTI-PHANTOM | {{r14_eff}} | {{r14_ev}} | {{r14_rec}} |

### 3.2 Workflow Bottlenecks

| Phase | Bottleneck | Impact | Fix |
|:-----|:-----------|:-------|:----|
{{#each workflow_bottlenecks}}
| {{phase}} | {{bottleneck}} | {{impact}} | {{fix}} |
{{/each}}

### 3.3 Undocumented Patterns

Successful behavior patterns observed in conversations but NOT encoded in any system prompt:

| Pattern | Observed In | Should Be In |
|:--------|:------------|:-------------|
{{#each undocumented_patterns}}
| {{pattern}} | {{observed_in}} | {{target_prompt}} |
{{/each}}

---

## 4. MODEL CONFIGURATION OPTIMIZATION

### 4.1 Current vs Recommended

| Model | Parameter | Current | Recommended | Rationale | Auto-Apply |
|:------|:----------|:--------|:------------|:----------|:-----------|
{{#each model_recs}}
| {{model}} | {{parameter}} | {{current}} | {{recommended}} | {{rationale}} | {{auto_apply}} |
{{/each}}

### 4.2 Context Utilization

| Agent | Prompt Size | Model Context | Utilization % |
|:------|:------------|:--------------|:--------------|
| Projects | {{projects_prompt_size}} | 1,048,576 | {{projects_util}}% |
| Prompts | {{prompts_prompt_size}} | 1,048,576 | {{prompts_util}}% |
| QWAV | {{qwav_prompt_size}} | 1,048,576 | {{qwav_util}}% |

---

## 5. SKILL & TEMPLATE AUDIT

### 5.1 Skill Usage

| Skill | Last Loaded | Usage Count (est.) | Needs Update? |
|:------|:------------|:-------------------|:--------------|
{{#each skills}}
| {{name}} | {{last_loaded}} | {{usage_count}} | {{needs_update}} |
{{/each}}

### 5.2 Template Health

| Template | Exists | Used? | Stale? |
|:---------|:-------|:------|:-------|
{{#each templates}}
| {{name}} | {{exists}} | {{used}} | {{stale}} |
{{/each}}

---

## 6. R2 CLOUDFLARE STATUS

| Resource | Status | Detail |
|:---------|:-------|:-------|
| Discovery Index | {{di_status}} | {{di_detail}} |
| Audit Trails | {{at_status}} | {{at_detail}} |
| Decision Log | {{dl_status}} | {{dl_detail}} |
| Project States | {{ps_status}} | {{ps_detail}} |
| Backlogs | {{bl_status}} | {{bl_detail}} |

---

## 7. IMPROVEMENT BACKLOG

### 7.1 This Run — Applied

{{#each applied_this_run}}
- [x] {{.}}
{{/each}}

### 7.2 Next Run — Queued

{{#each queued_next}}
- [ ] [{{priority}}] [{{category}}] {{description}}
{{/each}}

### 7.3 Future — Requires Manual Review

{{#each manual_review}}
- [ ] [{{category}}] {{description}} — *needs human decision on: {{decision_point}}*
{{/each}}

---

## 8. KAIZEN ENGINE SELF-ASSESSMENT

| Question | Answer |
|:---------|:-------|
| Did the engine identify real issues? | {{real_issues}} |
| Were any false positives flagged? | {{false_positives}} |
| Did auto-apply cause any regressions? | {{regressions}} |
| Should any category weights be adjusted? | {{weight_adjust}} |
| Is the health score trending up? | {{trending}} |

---

*Generated by Kaizen Engine v1.0 at {{timestamp}}*
*Next scheduled run: {{next_run}}*
