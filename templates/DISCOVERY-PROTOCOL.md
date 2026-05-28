# DISCOVERY-PROTOCOL TEMPLATE — v1.0

> **Purpose:** Unified information discovery for LLM due diligence during project execution.
> **Used by:** ALL agents (DEFAULT, QWAV, Projects, Subagents).
> **Invocation:** `fill_prompt_template("DISCOVERY-PROTOCOL", {scope: "...", topic: "..."})`

---

## Parameters

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `scope` | `"session"|"project"|"cross-project"` | Yes | Breadth of discovery: session startup, project due diligence, or portfolio-wide |
| `topic` | string | Yes | What the agent is looking for (project name, research topic, artifact type) |
| `project_name` | string | No | Current project context (for `session` scope) |

---

## Protocol Output

### Scope: `session` — Startup Discovery (every agent, every session)

Before beginning any significant work, the agent MUST:

```
[EXECUTED] Session Startup Discovery

1. PULL DISCOVERY INDEX (Cloudflare R2):
   npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json
   
   The index is a unified catalog of ALL projects, publications, decisions, 
   templates, skills, and archived work. It is the single entry point 
   for discovering what exists in the QNFO ecosystem.

2. IF current project {{project_name}} is in the index:
   - Read state: npx wrangler r2 object get qnfo/audit/state/{{project_name}}.json --remote
   - Read backlog: npx wrangler r2 object get qnfo/audit/backlog/{{project_name}}.json --remote
   
3. IF topic {{topic}} is NEW (not in index):
   - Search index for related projects by topic tags
   - Search R2 releases for related publications
   - Search Archive for related completed work
   - Search Decision Log for applicable decisions
   
4. CROSS-REFERENCE against local filesystem:
   - Test-Path "G:\My Drive\projects\{{project_name}}"
   - Test-Path "G:\My Drive\Archive\{{project_name}}"

5. REPORT DISCOVERY RESULTS:
   - [EXECUTED] Discovery complete
   - Related projects found: [count]
   - Related publications: [count]
   - Applicable decisions: [count]
   - Prior work in Archive: [yes/no]
   - [NEXT] Proceed to work with this context
```

### Scope: `project` — Due Diligence (before any significant task)

```
[EXECUTED] Project Due Diligence Discovery

1. SEARCH DISCOVERY INDEX for {{topic}}:
   python -c "
   import json, sys
   with open('_discovery_index.json') as f:
       idx = json.load(f)
   
   results = []
   query_terms = '{{topic}}'.lower().split()
   
   # Search projects by name, topics, summary
   for name, proj in idx.get('projects', {}).items():
       if any(t in name.lower() or t in ' '.join(proj.get('topics',[])).lower() 
              or t in proj.get('summary','').lower() for t in query_terms):
           results.append({'name': name, 'source': 'project', 'match': proj})
   
   # Search publications
   for pub_name, pub in idx.get('publications', {}).items():
       if any(t in pub_name.lower() or t in pub.get('summary','').lower() 
              for t in query_terms):
           results.append({'name': pub_name, 'source': 'publication', 'match': pub})
   
   # Search archive
   for arch_name, arch in idx.get('archive', {}).items():
       if any(t in arch_name.lower() for t in query_terms):
           results.append({'name': arch_name, 'source': 'archive', 'match': arch})
   
   json.dump(results, sys.stdout, indent=2)
   "

2. CROSS-REFERENCE results against local filesystem:
   For each result: verify files exist at claimed paths.

3. LOAD RELEVANT ARTIFACTS:
   - Read project states for related active projects
   - Load applicable decisions from Decision Log
   - Read Archive README for completed related work

4. REPORT:
   - [EXECUTED] Due diligence complete
   - Prior work found: [list with source labels]
   - Gaps identified: [what the index doesn't cover]
   - [PROCEED] with informed context
```

### Scope: `cross-project` — Portfolio-Level Discovery (QWAV agent)

```
[EXECUTED] Cross-Project Discovery

1. PULL DISCOVERY INDEX (full catalog):
   npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json

2. AUDIT index for:
   - ACTIVE projects: all projects with status "active" in index
   - STALE projects: active but no recent audit trail
   - DUPLICATION: projects with overlapping topic tags
   - ORPHAN releases: publications without active project
   - UNINDEXED local projects: projects in G:\My Drive\projects\ not in index
   - UNINDEXED archive: projects in G:\My Drive\Archive\ not in index

3. CROSS-REFERENCE:
   - Compare index against G:\My Drive\projects\ listing
   - Compare index against G:\My Drive\Archive\ listing
   - Compare index against GitHub repo listing

4. REPORT:
   - [EXECUTED] Portfolio discovery complete
   - Active: [count] | Stale: [count] | Archived: [count]
   - Unindexed: [count] projects missing from index
   - Duplication risks: [list]
   - [NEXT] Index unindexed projects, flag stale projects
```

---

## Index Structure (qnfo/discovery/index.json on R2)

```json
{
  "version": "1.0",
  "updated": "ISO-8601 timestamp",
  "updated_by": "agent + session ID",
  "projects": {
    "<project-name>": {
      "status": "active|archived|complete",
      "repo": "qnfo/<repo-name>",
      "state_r2": "qnfo/audit/state/<project>.json",
      "backlog_r2": "qnfo/audit/backlog/<project>.json",
      "releases_r2": "qnfo/releases/<project>/",
      "pages_url": "deep.qwav.tech/<path>/",
      "local_path": "G:/My Drive/projects/<project>/",
      "archive_path": "G:/My Drive/Archive/<project>/",
      "topics": ["tag1", "tag2"],
      "summary": "One-line description",
      "last_active": "ISO-8601",
      "last_audit": "ISO-8601"
    }
  },
  "decisions": {
    "r2_path": "qnfo/audit/decisions/DECISION-LOG.md",
    "last_updated": "ISO-8601",
    "key_topics": ["tag1"]
  },
  "publications": {
    "<pub-name>": {
      "project": "<parent-project>",
      "r2_path": "qnfo/releases/<project>/<file>",
      "pages_url": "deep.qwav.tech/<path>/",
      "zenodo_doi": "10.5281/zenodo.xxxxx",
      "topics": ["tag1"],
      "summary": "One-line description",
      "published": "ISO-8601"
    }
  },
  "archive": {
    "<archived-project>": {
      "local_path": "G:/My Drive/Archive/<project>/",
      "r2_path": "qnfo/archive/<project>/",
      "topics": ["tag1"],
      "summary": "One-line description",
      "archived": "ISO-8601"
    }
  },
  "templates": {
    "source": "prompts.json + templates/ directory",
    "count": 12
  },
  "skills": {
    "source": "skills/ directory",
    "count": 7
  },
  "infrastructure": {
    "workers": ["ask-qwav", "github-sync", "qwav-email"],
    "pages_sites": ["deep.qwav.tech", "..."],
    "domains": ["qwav.tech", "quniverse.cc", "..."],
    "vectorize_indexes": ["qwav-research"],
    "d1_databases": ["qwav-db"]
  }
}
```

---

## Automatic Indexing (embedded in Session Close-Out)

Every session close-out MUST update the discovery index:

1. **If new project created:** Add project entry to index
2. **If new publication:** Add publication entry to index
3. **If project archived:** Move from `projects` to `archive` in index
4. **If project state changed:** Update status + last_active in index
5. **If new decisions added:** Update decisions.last_updated in index

**Index update command:**
```bash
npx wrangler r2 object put qnfo/discovery/index.json --file=_updated_index.json --remote
```

---

## Fallback: When Discovery Index Is Not Available

If `qnfo/discovery/index.json` is missing or corrupt:

1. **Rebuild from sources:**
   - Enumerate R2 objects: check `qnfo/audit/state/`, `qnfo/audit/backlog/`, `qnfo/releases/`
   - Enumerate local: `G:\My Drive\projects\`, `G:\My Drive\Archive\`
   - Enumerate GitHub: `gh repo list rwnq8 --json name,description`
   - Build fresh index and upload

2. **If wrangler not available:**
   - Manual discovery: search local filesystem + Archive + R2 individually
   - Flag as `[DISCOVERY-DEGRADED]` in session output
   - Rebuild index at earliest opportunity

---

*DISCOVERY-PROTOCOL template v1.0 — Unified information discovery for LLM agents*
