# CPL NEW LESSONS — Promote from QWAV LEARNINGS L16-L20

> **Target file:** `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md`
> **Action:** Append these 5 lessons (L50-L54) to the CPL file, after L49.
> **Created:** 2026-05-23 from `G:\My Drive\QWAV\LEARNINGS.md`
> **Scope note:** System Prompt Generator write boundary is `G:\My Drive\prompts\` — this file created here for manual copy.

---

### L50: CPL numbering gap L8-L12 — intentionally skipped, documented here

- **Category:** METHODOLOGY
- **Issue:** The CPL file has 44 lessons numbered L1-L49, but L8, L9, L10, L11, and L12 do not exist. The numbering jumps from L7 (Inline Python through PowerShell) directly to L13 (git log verification). These 5 slots were either never written or were deleted/merged into other lessons. The gap creates ambiguity for audits that expect sequential numbering.
- **Solution:** Document the gap explicitly. The 5 missing slots are intentionally left empty — no content was lost. Future audits should expect and tolerate non-sequential numbering in the CPL. New lessons append at the end (highest L-number) regardless of gaps.
- **Prevention:** When deleting or merging CPL lessons, leave a tombstone entry (like this one) documenting the gap. Never renumber existing CPL lessons — the L-number is a stable identifier used across BACKLOG, system prompts, and audit references.
- **Cross-Project:** YES — any project that uses sequential lesson numbering should have a gap-tolerance policy.

---

### L51: Formal verification collaborations need explicit scope/value-exchange spec before commitment

- **Category:** METHODOLOGY
- **Issue:** The Richard Goodman collaboration on Lean formalization of ultrametric error confinement was approached without first establishing: (a) what exactly would be formalized (AGP specialization or stronger claim?), (b) what value each party would derive, and (c) whether the artifact would be a classical or quantum theorem. These ambiguities surfaced as "objections" mid-exchange, making it impossible to proceed. The collaboration was terminated ("not a fit," 2026-05-17). The same pattern applies to any external collaboration proposal — formal verification, co-authorship, user testing, domain expert review.
- **Root cause:** Enthusiasm for the collaboration opportunity preceded rigorous scoping. The agent initiated contact before defining the terms of engagement. Without a spec, the collaborator's legitimate questions appeared as objections rather than scoping clarifications.
- **Rule:** Before approaching any external collaborator, produce a one-page spec containing: (1) exact statement to be proved/verified/reviewed, (2) assumptions inventory with correspondence to physical or domain reality, (3) what the artifact means for your program, and (4) what the collaborator receives (co-authorship, citation, payment, acknowledgment). Treat collaboration like any other external dependency — spec first, approach second.
- **Detection:** Before any `fill_prompt_template("EMAIL-AGENT-TEMPLATE")` call for collaboration outreach, verify a spec document exists in the project directory. If no spec → block the outreach. The spec must be a standalone file, not an inline paragraph in an email draft.
- **Cross-Project:** YES — any program that proposes external collaborations (co-authorship, formal verification, user testing, domain expert review) must require a spec before outreach. The "enthusiasm before scoping" failure mode is universal.

---

### L52: Mathematical proof proves consistency, not physical reality — the "assumptions gap" is ineradicable

- **Category:** METHODOLOGY
- **Issue:** The formal verification collaboration with Richard Goodman (L51) surfaced a deeper methodological tension: a mathematical proof of a theorem proves internal consistency of the axiomatic system, not correspondence to physical reality. The assumptions gap — the distance between the mathematical assumptions (e.g., AGP specialization) and the physical claims (e.g., "ultrametric error confinement is physically realizable") — cannot be closed by formal verification alone. The collaborator's questions about whether the theorem was "classical or quantum" and what "error confinement" physically meant were not objections to the proof — they were questions about the assumptions gap. The agent treated them as obstacles rather than as the core methodological challenge.
- **Root cause:** The agent's default frame is "prove the theorem → claim validated." But in applied mathematics / theoretical physics, proof of consistency is necessary but insufficient. The real work is establishing that the assumptions correspond to physical reality — and this work requires experimental evidence or computational validation, not more proofs.
- **Rule:** For any deliverable that makes a physical claim (not just a mathematical one), include an "Assumptions Inventory" section that: (1) lists every mathematical assumption, (2) states the physical correspondence (or lack thereof) for each, and (3) identifies which assumptions require experimental validation. Never claim a mathematical proof validates a physical claim without this inventory.
- **Detection:** Reader testing (CPL L26-L28): ask a first-time reader "What assumptions does this claim rest on, and which ones are physically verified?" If they can't answer, the assumptions gap is invisible — the document is not publication-ready.
- **Cross-Project:** YES — any program that produces mathematical or theoretical deliverables with physical claims must explicitly address the assumptions gap. The "proof → validated" shortcut is a universal failure mode in applied mathematics.

---

### L53: Legal, financial, and jurisdictional decisions require exogenous verification — the agent cannot self-certify

- **Category:** METHODOLOGY
- **Issue:** In the QWAV program, tasks involving legal compliance (patent filing strategy, IP assessment), financial decisions (pricing models, grant eligibility), and jurisdictional applicability (which country's patent/tax law applies) arose from strategy documents, not from user directives. The agent began analyzing and making recommendations based on information available in project files — but the critical facts (legal precedents, tax codes, institutional policies) exist outside the project files and are inaccessible to the agent. This creates a structural information asymmetry: the agent cannot distinguish between "confident recommendation based on incomplete information" and "correct recommendation."
- **Root cause:** The system prompt had no protocol for recognizing when a task requires exogenous (outside-project-files) information. The agent's default behavior is to answer questions using available information, even when the available information is structurally insufficient. This is the same failure mode as fabricating citations — the agent fills gaps with plausible-sounding but unverifiable content.
- **Rule:** Any task involving legal, financial, or jurisdictional decisions must trigger the Exogenous Information Protocol: (1) DETECT — scan for legal/financial/jurisdictional implications, (2) FLAG — mark the task `[EXOGENOUS — REQUIRES USER INPUT]`, (3) SPECIFY — list what specific exogenous information is needed, (4) BLOCK — do not execute until user provides the information, (5) DOCUMENT — record the user's input and decision in DECISIONS.md. The anti-pattern: "Based on standard practice..." or "Typically this would..." — these are guesses about exogenous information.
- **Detection:** Pre-Send Checklist (DEFAULT.md §E.5.1): scan for legal/financial/jurisdictional claims. If any are present, verify the Exogenous Information Protocol was followed and user input is documented.
- **Cross-Project:** YES — any agent that operates on project files must recognize that some decisions require information that exists only outside those files. The "confident answer from incomplete data" pattern is universal.

---

### L54: Multi-agent systems require explicit prompt-level role boundaries — manager agents must not become executor agents

- **Category:** METHODOLOGY
- **Issue:** The QWAV agent (Strategy Program Manager) repeatedly crossed from portfolio-level strategy/direction into individual project execution — suggesting specific implementation details, micro-managing what a Projects thread should do, rather than defining the handoff and trusting the Projects agent to execute. Root cause: the QWAV system prompt initially positioned the agent as a generalist ("equally capable of creative ideation, rigorous research, structured writing") with no role-boundary language. The same underlying model is used for both QWAV and Projects threads, making the structural distinction invisible to the model without explicit prompt enforcement.
- **Root cause:** Without explicit role-boundary language, the model defaults to its generalist training — it tries to be helpful across all domains. In a multi-agent system, this causes role confusion: the Strategy Program Manager starts executing, and the Project Executor starts strategizing. The prompt must encode the structural separation that the multi-agent architecture intends.
- **Rule:** Every agent in a multi-agent system must have an explicit role definition that specifies: (1) what this agent DOES (its domain of action), (2) what this agent DOES NOT DO (its boundary), and (3) what to do when a task crosses the boundary (handoff protocol). The role definition must be prominent (near the top of the prompt) and use imperative language ("You are the X. Your scope is Y. You do NOT do Z. When Z arises, delegate to W.").
- **Detection:** Agent output audit: if an agent's output contains content that belongs to another agent's role, the role boundary definition is insufficient. For QWAV specifically: if QWAV output contains implementation-level code, file paths under `projects/`, or specific commit messages, it has crossed the boundary.
- **Cross-Project:** YES — any multi-agent setup with different roles (manager vs. executor, researcher vs. reviewer) needs explicit prompt-level role definitions. The "generalist default" is a universal failure mode in multi-agent LLM systems.

---

*Lessons L50-L54 added 2026-05-23 from QWAV/LEARNINGS.md L16-L20. Promote to CROSS-PROJECT-LEARNINGS.md by appending after L49. L50 documents the L8-L12 numbering gap for audit tolerance.*
