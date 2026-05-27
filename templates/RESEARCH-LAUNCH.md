---
template: RESEARCH-LAUNCH
version: 1.0
description: "Research project launcher — single entry point for all research. Takes a research idea and generates the complete project initialization prompt for the Projects agent. Hides ALL pipeline complexity (STAGE-1 through STAGE-4)."
---

# RESEARCH LAUNCHER

> **Fill this out.** The output is a complete prompt you paste into a Projects agent conversation. Everything else — STAGE pipeline, templates, git, publication — is automatic.

## 1. What's the core research question?

<!-- One sentence. What are you trying to figure out? -->
{{ RESEARCH_QUESTION }}

## 2. What domain/tags?

<!-- e.g., quantum computing, trapped ions, geometric phases, number theory -->
{{ DOMAIN_TAGS }}

## 3. What output do you want?

<!-- paper | report | analysis | simulation | all -->
{{ OUTPUT_TYPE }}

## 4. Key sources or starting points?

<!-- arXiv IDs, DOIs, papers you already know about, or leave blank for auto-discovery -->
{{ STARTING_SOURCES }}

## 5. Priority?

<!-- now | this-week | backlog -->
{{ PRIORITY }}

---

## GENERATED PROMPT (paste into Projects agent)

```
RESEARCH PROJECT: {{ RESEARCH_QUESTION }}

DOMAIN: {{ DOMAIN_TAGS }}
OUTPUT: {{ OUTPUT_TYPE }}
PRIORITY: {{ PRIORITY }}
STARTING SOURCES: {{ STARTING_SOURCES }}

---

EXECUTE THE FULL RESEARCH PIPELINE:

PHASE 1 — DISCOVERY
- Search arXiv, journals, and web for relevant papers using brave_web_search
- Retrieve papers via YoBrowser or direct download
- Build a source catalog with DOIs, arXiv IDs, and key claims

PHASE 2 — DEEP READING
- Read each source via YoBrowser or local PDF
- Extract: key claims, methods, data, limitations
- Cross-reference claims across sources

PHASE 3 — SYNTHESIS
- Identify patterns, contradictions, gaps across sources
- Verify ALL quantitative claims via Python execution
- Draft findings with [EXTERNAL-SOURCE] and [CODE-EXECUTED] labels

PHASE 4 — OUTPUT
- Produce {{ OUTPUT_TYPE }} with full source traceability
- Run STAGE-3 REVIEW (blind validation, fabrication audit)
- Run STAGE-4 PUBLISH (Zenodo DOI, GitHub release)

PHASE 5 — CLOUDFLARE HOSTING
- Deploy paper as HTML page to Cloudflare Pages (qwav project → deep.qwav.tech/papers/)
- Backup all files (md, html, pdf) to R2 bucket (qnfo) for audit trail
- Index paper in Vectorize (qwav-research, 768d) for semantic search
- Update sitemap.xml, robots.txt, and llms.txt for search engine + AI crawler discovery
- Add Schema.org/JSON-LD markup (ScholarlyArticle) for Google Scholar indexing
- Deploy via: python tools/publish-to-cloudflare.py <project-dir>

PROJECT SETUP (automatic):
- Create project directory: G:\My Drive\projects\<kebab-case-name>\
- Initialize git with feature branch
- GitHub-native project management (Issues, Projects, no local PM files)

QWAV PORTFOLIO TRACKING:
- Register project in QWAV portfolio
- Tag with {{ DOMAIN_TAGS }}
- Link to program strategy
- Add to QWAV/papers/index.html catalog

PROCEED. Execute Phase 1 immediately.
```
