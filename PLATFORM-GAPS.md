# PLATFORM GAPS — DeepChat Limitations Preventing Reliable Autonomous Execution

> **Date:** 2026-06-05 | **Author:** QNFO/QWAV System | **Status:** Open

---

## Gap 1: No Response Interception Hooks (CRITICAL)

### What We Need
A pre-response hook that programmatically checks whether the agent has pending executable tasks and, if so, forces tool invocation instead of text generation.

### What Exists
- **ACP agents** — Disabled. Agent registry only, no hook capability.
- **MCP servers** — Tool integration only. No response interception middleware.
- **Skills** — Prompt-level instructions. The LLM can "think" about the instructions without acting on them.

### Impact
The 2026-06-04 failure test case: 19/24 user messages (79%) were EXECUTE/RESUME/PROCEED/HANDOFF demands. Every response had ZERO tool invocations. The agent self-diagnosed the planning spiral but couldn't break out of it because "thinking about executing" is not "executing."

### Mitigation (RESOLVED — DeepChat Hooks)

**DeepChat supports lifecycle hooks on 8 events.** We now deploy:

| Hook Event | What It Does |
|:-----------|:-------------|
| **SessionStart** | Initialize audit trail, create `_session_meta.json` with tool_count=0 |
| **PostToolUse** | Log every tool invocation — ground-truth execution counter |
| **ToolUseFailure** | Track failures, detect 3x same tool+error → anti-loop alert |
| **SessionEnd** | Compute execution_ratio, tool_count, failure_count, severity automatically |

**Unlike prompt-level instructions, these hooks execute as code-level commands and cannot be ignored by the LLM.** The SessionEnd hook provides ground-truth execution statistics that feed the Kaizen engine and closeout audit.

**Setup:** See `HOOKS-REFERENCE.md`. Command: `python "G:\My Drive\prompts\hooks\deepchat_hooks.py" {{event}} {{conversationId}}`

### Feature Request for DeepChat
Add a **PreResponse hook** that fires before the agent's response is delivered to the user. This hook would receive:
- The pending response text
- Tool invocation history for the session
- The current `update_plan` state (via stdin JSON or environment variable)

The hook could then:
- **Block** text generation if tasks are pending (exit code 1 → DeepChat suppresses response)
- **Append** `[AUTO-CONTINUE]` tags before delivery
- **Flag** banned words before they reach the user

This would close the gap between prompt-level guards and code-level enforcement.

---

## Gap 2: No Scheduled/Background Task Polling (HIGH)

### What We Need
A mechanism to periodically poll the R2 backlog for new tasks and auto-trigger execution without user prompting. Similar to cron but within the chat session.

### What Exists
- `subagent_orchestrator` with `background: true` — Can run subagents in background, but the PARENT agent still controls when subagents are spawned.
- `exec` with `background: true` — Can run background processes, but there's no trigger mechanism.
- `tape_handoff` — Can checkpoint session state, but can't trigger actions.

### Impact
The user must manually type EXECUTE/RESUME/PROCEED to trigger the next task. Between user messages, the system is idle even when tasks are known to be pending.

### Mitigation (RESOLVED — DeepChat Hooks)

**DeepChat lifecycle hooks now provide scheduled execution at SessionStart and SessionEnd.** The SessionStart hook initializes audit tracking and can pull the R2 backlog for pending tasks. The SessionEnd hook runs cleanup and computes execution statistics.

**These are code-level triggers, not prompt-level.** The LLM cannot ignore them.

**Setup:** See `HOOKS-REFERENCE.md`. Both hooks use the same dispatcher: `python hooks/deepchat_hooks.py {{event}} {{conversationId}}`

### Feature Request for DeepChat
Add a `sessionHook` configuration that supports:
- `onSessionStart` — Run script at session initialization (pull backlog, populate plan)
- `onToolComplete` — Run script after every tool invocation (check plan, auto-execute)
- `onSessionEnd` — Run script at session closeout (cleanup, audit, Discovery Index update)

---

## Gap 3: No Programmatic Tool Invocation (MEDIUM)

### What We Need
The ability for a hook or script to FORCE a tool invocation regardless of what the LLM decides. If the pre-response hook detects pending tasks, it should be able to invoke `exec`, `write`, or `subagent_orchestrator` without the LLM's cooperation.

### What Exists
Nothing. All tool invocations flow through the LLM's output. There is no API or mechanism for external code to invoke tools within a DeepChat session.

### Impact
Even with Priority 0 instructions, the LLM retains final control. It can produce text that says "I should execute" instead of actually invoking a tool.

### Feature Request for DeepChat
Add a `forceToolInvocation` API that hook scripts can call to inject a tool invocation into the agent's response pipeline.

---

## Gap 4: No Per-Session Execution Audit (MEDIUM)

### What We Need
After every session, automatically run `execution_audit.py` against the conversation export to compute plan:execution ratios and flag sessions that degenerated into planning spirals.

### What Exists
`conversation-search-server` MCP — Can search conversation history but cannot compute metrics automatically.

### Mitigation (Implemented)
- `execution_audit.py` — Post-hoc analysis script (must be run manually or by closeout)
- Kaizen integration — Statistics fed to Kaizen engine at closeout

---

## Gap 5: Cannot Pin Skills Programmatically (LOW)

### What We Need
The ability to programmatically pin a skill (like execution-guard) so it's always loaded at session start, without requiring manual user action in the DeepChat UI.

### What Exists
Skills must be pinned manually via the DeepChat UI. There is no API or configuration option to auto-pin skills.

### Mitigation
The execution-guard skill description includes trigger conditions for "session start" and "any response." If DeepChat evaluates skill descriptions at session start, this may auto-trigger. Otherwise, the user must manually pin it.

---

## Summary

| Gap | Severity | Mitigation Status |
|:----|:---------|:------------------|
| Response Interception Hooks | CRITICAL | PARTIAL — DeepChat hooks (PostToolUse) provide execution tracking; cannot block responses |
| Scheduled/Background Polling | HIGH | RESOLVED — DeepChat SessionStart + SessionEnd hooks provide lifecycle automation |
| Programmatic Tool Invocation | MEDIUM | None — requires DeepChat API; hooks observe but cannot inject tools |
| Per-Session Execution Audit | MEDIUM | RESOLVED — SessionEnd hook computes execution_ratio and severity automatically |
| Auto-Pin Skills | LOW | Manual pinning required |

---

*PLATFORM-GAPS.md v1.0 — Documenting what DeepChat lacks for truly autonomous execution. Feature requests included.*
