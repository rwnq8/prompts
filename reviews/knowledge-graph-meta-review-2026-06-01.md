# QNFO Knowledge Graph — META Review

**Author:** META-PROMPT Agent (System Prompt Generator v5.3) | **Date:** 2026-06-01 | **License:** CC BY 4.0

---

## Part 1: Systemic Lessons Extracted

The `qnfo-knowledge-graph` project reveals several patterns that should be encoded into system prompts, templates, and agent architecture. These lessons are universal — they apply to ALL projects, not just the knowledge graph.

### Lesson 1: "What Depends On X?" Is a Universal Due Diligence Question

**Pattern observed:** The project's core value proposition is answering "If I update X, what breaks?" — a question that EVERY agent session should ask before modifying any shared asset (template, skill, prompt, API, script).

**Current state:** The Due Diligence Protocol (§3 in DEFAULT.md) tells agents to pull the Discovery Index and check for prior work. But it has no mechanism for IMPACT ANALYSIS — identifying downstream dependents.

**Systemic fix implemented:** Added §3.1.5 "Query Knowledge Graph (Impact Analysis)" to DEFAULT.md v3.13. This makes impact queries a standard part of due diligence before modifying any asset.

**Remaining gap:** The impact analysis relies on the graph API being available and seeded. A local fallback (filesystem grep for template/skill references) should eventually be built as Phase 2.

### Lesson 2: Siloed Data Creates Blind Spots

**Pattern observed:** The project documents 6 separate tracking systems (discovery/index.json, DECISION-LOG.md, conversations/*.md, local project dirs, git repos, Cloudflare dashboard) — none of which can answer cross-system queries.

**Current state:** Agents navigate this by manually checking each silo. This is $O(n)$ and error-prone.

**Systemic fix:** The knowledge graph provides a unified query layer. But the lesson is broader: ANY system with >3 data silos should have a unified access layer. This principle should be encoded in the Architecture Compliance Gate (§3.2 step 1.5 in DEFAULT.md v3.13) which already enforces Cloudflare-native services.

**Template recommendation:** Future project proposals should include a "Data Unification" section identifying what silos the project bridges and how.

### Lesson 3: Audit Scripts Are Graph Seed Sources

**Pattern observed:** The project includes multiple audit scripts (`audit_cloudflare.py`, `dns_pages_crossref.py`, `pages_dir_audit.py`) that query the Cloudflare API for live infrastructure state. These are EXACTLY the kind of data that should seed the knowledge graph.

**Current state:** These audit scripts output markdown reports. They could also output graph seed data.

**Systemic fix:** The knowledge graph Phase 2 (Live Sync Pipeline) should consume these audit scripts as data sources. Every audit script should have a `--graph-output` flag that produces graph-compatible seed data.

**Skill integration:** The `cloudflare-deployer` skill should be updated to optionally write deployment events to the graph on deploy.

### Lesson 4: DNS-Pages Cross-Reference Is a Graph Problem

**Pattern observed:** The `dns_pages_crossref.py` script manually maps 46 CNAME records to 25 Pages projects by iterating through API calls — essentially doing graph traversal without a graph.

**Current state:** The script found 5 broken/dead assets that no one knew about because there was no centralized cross-reference.

**Systemic fix:** With the knowledge graph seeded, the query becomes trivial: `MATCH (d:Domain)-[:POINTS_TO]->(a:CloudflareAsset) WHERE a.status = 'broken' RETURN d.name`. This is orders of magnitude faster and catches issues automatically.

**Lesson for prompts:** Generated prompts should include a "dead asset check" as part of ecosystem health monitoring, powered by the graph.

### Lesson 5: Agent Sessions Are Temporal Graph Nodes

**Pattern observed:** The `ingest_session.py` script parses DeepChat exports and creates AgentSession nodes with MENTIONS edges to projects and templates. This turns conversation history into a queryable knowledge graph.

**Current state:** Session audit trails are currently exported as markdown files to R2. They're searchable only via full-text grep.

**Systemic fix:** The close-out pipeline should automatically write graph events. The `closeout-manager` skill should be updated to call the graph API on session close-out (Phase 3 integration).

**Value:** After enough sessions are ingested, queries like "Which templates caused the most agent errors?" and "What was the impact of the v3.10 EXECUTE MODE hardening?" become answerable.

### Lesson 6: Graph Fallback Is Essential

**Pattern observed:** The knowledge graph is Phase 1 (seed data only). Phase 2 (live sync) and Phase 3 (agent integration) are pending. Agents CANNOT rely on the graph being up-to-date.

**Systemic fix:** All graph queries in DEFAULT.md §3.1.5 are wrapped in try/except with `[GRAPH-UNAVAILABLE]` fallback. The explicit rule is: "Graph results are advisory — always cross-reference with filesystem."

**This is the correct pattern for ALL new infrastructure:** Always provide a fallback path. Never make a new system a single point of failure for agents.

---

## Part 2: Architecture Alignment Audit

### 2.1 Data Model vs. Architecture Wiki

**Entity types in graph schema (14):** Organization, Project, Paper, AgentSession, CloudflareAsset, GitCommit, Decision, Template, Skill, Person, Issue, Domain, Deployment, Concept

**Entities in Architecture Wiki:** Projects, Agents, Subagents, Skills, Templates, Deployments, Audit Trail, Discovery Index

**Alignment:** The graph model is a SUPERSET of the Architecture wiki. Every Architecture wiki entity has a corresponding graph node type. The graph adds: Organization, Paper, CloudflareAsset, GitCommit, Decision, Person, Issue, Domain, Concept.

**Gap:** The Architecture wiki documents "Subagent slots" (explorer, implementer, reviewer) — these are not explicit node types in the graph. They should be modeled as Agent nodes with a `role` property, or as a separate SubagentSlot node type.

### 2.2 Agent Configuration Mapping

**Agent Configuration wiki documents:** Slot IDs, write boundaries, tool lists, sandboxing model.

**Graph coverage:** AgentSession nodes exist, but they don't encode slot ID or tool availability. The graph currently treats all agents generically.

**Recommendation:** Add `slot_id` and `tools_available` properties to AgentSession nodes. This enables queries like "Which sessions used the EXPLORER slot?" and "How often do subagents lack file I/O tools?"

### 2.3 Technology Stack Consistency

**Graph implementation:** Uses BOTH Neo4j (schema.cypher, seed scripts) and D1/Cloudflare Worker (graph API at `graph-api.q08.workers.dev`).

**Architecture Compliance Gate (§3.2 step 1.5 in DEFAULT.md v3.13) states:** PROHIBITED: external cloud services (Neo4j AuraDB, AWS, GCP, Azure, etc.). Embedded/local DBs (Kuzu, SQLite, DuckDB) = development only — production must be Cloudflare-hosted, Worker-queryable.

**Finding:** The Neo4j schema and seed scripts target Neo4j AuraDB (external cloud service). However, the project also has a D1-backed Cloudflare Worker (`graph-api.q08.workers.dev`) which IS Cloudflare-native and compliant.

**Resolution path:**
- **Short term:** The D1 Worker is the canonical API. Neo4j Cypher schema is a REFERENCE — not deployed infrastructure.
- **Medium term:** Port the full graph to D1 (already done — `schema.sql`, `seed_d1.sql`, `seed_d1.py`). The D1 schema uses a universal nodes/edges pattern that supports all 14 node types and 16 relationship types.
- **Long term:** The `kuzu_graph.py` embedded database provides a LOCAL development option (acceptable per compliance gate as "development only"). Production queries go through the D1 Worker.

**Compliance status:** PASSES with caveat. The deployed API is Cloudflare-native (D1 + Worker). Neo4j Cypher files are reference/development artifacts, not production infrastructure.

### 2.4 Discovery Index Integration

**Discovery Index** (`qnfo/discovery/index.json` on R2) is the canonical ecosystem catalog. The knowledge graph seed scripts (`seed_from_discovery.py`, `seed_graph.py`) consume the Discovery Index as their primary data source.

**Alignment:** Perfect. The graph is a DERIVED view of the Discovery Index + additional sources (DECISION-LOG.md, Cloudflare API). The Discovery Index remains the single source of truth; the graph is a query layer.

**Gap:** The seed scripts pull the Discovery Index from a local file. They should pull directly from R2 (`npx wrangler r2 object get`) for a fully automated pipeline.

---

## Part 3: Quality Review

### 3.1 Proposal (0.1-proposal.md) — Rating: 8/10

**Strengths:**
- Clear problem statement with concrete examples (6 silos, impact analysis query)
- Comprehensive data model (14 entity types, 16 relationship types)
- Phased implementation plan (4 phases, realistic scope)
- Technology comparison with criteria (Neo4j vs. alternatives)
- Integration architecture diagram
- Cost estimates for hosting options
- Concrete Cypher query examples for each use case
- Research Integrity compliance — no promotional language, claims traceable to sources

**Gaps:**
- No explicit failure modes documented (what happens when Neo4j is down? What if the graph is stale?)
- No security/access control model (who can query the graph? Is the API public?)
- Phase 3 "Agent Integration" is described as "1 session" — likely underestimated
- No data retention/pruning strategy (graph grows unboundedly)

### 3.2 Schema (schema.cypher) — Rating: 9/10

**Strengths:**
- Complete constraints and indexes for all 14 node types
- Well-commented with clear label summary
- Performance indexes on frequently queried properties (status, date, timestamp)
- Composite unique constraints (template name+version, asset type+name)
- Claim node with certainty calibration (aligns with Research Integrity Mandate)

**Gaps:**
- Missing relationship constraints (no uniqueness constraints on edges — could create duplicate MERGEs)
- Claim node references papers but doesn't have a `source` property for verification traceability

### 3.3 D1 Worker API (src/index.js) — Rating: 9/10

**Strengths:**
- Clean REST API with 7 endpoints
- CORS support
- Proper error handling with 404/500 responses
- Impact analysis endpoint (the killer feature)
- Arbitrary query support via POST /query
- Well-documented with inline endpoint listing at GET /

**Gaps:**
- No authentication — API is fully public
- No rate limiting
- POST /query accepts arbitrary SQL — injection risk (mitigated by parameterized queries in examples, but not enforced)
- No pagination on /nodes and /edges endpoints (could return large results)

### 3.4 Seed Scripts — Rating: 7/10

**Strengths:**
- `seed_from_discovery.py` — comprehensive parsing of Discovery Index
- `seed_graph.py` — clean generation of Cypher MERGE statements
- `kuzu_graph.py` — embedded database option for local development
- `ingest_session.py` — parses DeepChat exports into structured data

**Gaps:**
- `seed_from_discovery.py` and `seed_graph.py` are DUPLICATE implementations — both generate Cypher but with different approaches
- `seed_d1.py` generates SQL but wasn't fully reviewed (truncated content)
- Hard-coded known project names in `ingest_session.py` — should pull from Discovery Index dynamically
- No test coverage for any seed script

### 3.5 Audit Scripts — Rating: 8/10

**Strengths:**
- `audit_cloudflare.py` — comprehensive inventory of all Cloudflare resources
- `dns_pages_crossref.py` — systematic CNAME-to-Pages verification with HTTP checks
- `pages_dir_audit.py` — deployment detail extraction
- All use the Cloudflare API token correctly

**Gaps:**
- All scripts are standalone — none output graph-compatible data
- No unified runner — each must be invoked separately
- Results are printed to stdout, not stored (no audit trail)
- `pages_dir_audit.py` hard-codes `[:8]` limit — only checks 8 of 25 Pages projects

### 3.6 Overall Project Health — Rating: 8/10

| Dimension | Score | Notes |
|:----------|:-----:|:------|
| **Problem clarity** | 10/10 | Perfectly articulated with concrete examples |
| **Data model** | 9/10 | Comprehensive, well-normalized, extensible |
| **Implementation** | 8/10 | Working D1 API + multiple seed options; duplicates exist |
| **Testing** | 4/10 | Only `test_api.py` exists; no unit/integration tests |
| **Documentation** | 9/10 | Excellent README, proposal, decision log, audit reports |
| **Architecture compliance** | 8/10 | D1 Worker is compliant; Neo4j reference is acceptable as dev-only |
| **Security** | 5/10 | No auth on API, no rate limiting, SQL injection surface |
| **Operability** | 6/10 | Manual seed; no live sync; no monitoring; no alerting |

---

## Part 4: Recommendations

### Immediate (this session)
1. **DONE** — Created `knowledge-graph` skill (v1.0)
2. **DONE** — Integrated graph queries into DEFAULT.md Due Diligence (§3.1.5)
3. **DONE** — Added skill to both DEFAULT.md and META-PROMPT skill tables

### Short-term (next 1-2 sessions)
4. Add authentication to graph API Worker (API token or Cloudflare Access)
5. Add rate limiting to graph API Worker
6. Consolidate `seed_from_discovery.py` and `seed_graph.py` into single canonical seeder
7. Add `--graph-output` flag to audit scripts
8. Fix `pages_dir_audit.py` hard-coded limit (check all 25 Pages projects)

### Medium-term (Phase 2-3)
9. Implement live sync pipeline (git hooks to graph events)
10. Update `closeout-manager` skill to write graph events on session close-out
11. Add AgentSession `slot_id` and `tools_available` properties
12. Add SubagentSlot node type to graph schema

### Long-term (Phase 4-5)
13. Build Graph Explorer UI (Cytoscape.js — reuse from concept-graph)
14. Populate Concept and Claim nodes from research papers (Phase 5)
15. Implement data retention/pruning strategy

---

*META Review complete. All immediate actions executed. Remaining items tracked as Cloudflare tasks.*
