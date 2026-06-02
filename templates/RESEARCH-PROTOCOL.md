---
template: RESEARCH-PROTOCOL
version: 1.0
---

# RESEARCH-PROTOCOL: Deep-Dive Paper Research Methodology (v1.0)

> **Purpose:** Shared research protocol template applicable to any research domain/subject. Defines the standard six-phase deep-dive methodology for retrieving, reading, verifying, and synthesizing published papers (arXiv, journals, conference proceedings). All STAGE prompts (1-4) reference this protocol.

---

## Phase A: Paper Discovery & Multi-Source Retrieval

### A.1 Targeted arXiv/DOI Search
Use `brave_web_search` with the paper's arXiv ID or DOI plus domain-specific keywords:
```
query: "arXiv:<ID> <domain keyword 1> <domain keyword 2>"
count: 5-10
```

### A.2 Multi-Source Verification
Retrieve the paper from multiple independent sources:
- **arXiv abstract page:** `https://arxiv.org/abs/<ID>` — confirms metadata, provides abstract
- **arXiv HTML full-text:** `https://arxiv.org/html/<ID>v<N>` — provides full structured content
- **Supplementary sources:** ResearchGate, publisher pages, Semantic Scholar — cross-reference metadata

### A.3 Source Documentation
Document every retrieval:
```
[WEB-SEARCH: "arXiv:<ID> <keywords>"]
Source: <URL>
Retrieved: <ISO 8601 timestamp>
```

---

## Phase B: Deep Reading via YoBrowser

### B.1 Page Loading
```
load_url: "https://arxiv.org/html/<ID>v<N>"
```

### B.2 Structured Content Extraction
Use `cdp_send` with `Runtime.evaluate` to extract paper content by section:

```javascript
// Extract abstract
document.querySelector('blockquote.abstract')?.innerText

// Extract section by heading text
Array.from(document.querySelectorAll('h2'))
  .find(h => h.textContent.includes('Introduction'))
  ?.parentElement?.innerText

// Extract math/equations
Array.from(document.querySelectorAll('.MathJax'))
  .map(m => m.textContent)

// Extract references/bibliography
Array.from(document.querySelectorAll('li'))
  .filter(li => li.textContent.match(/\[\d+\]/))
  .map(li => li.textContent)
```

### B.3 Local File Preservation
Save ALL extracted text to a versioned local file for audit trail:
```
<paper_id>_text.txt  (full extracted text)
```

### B.4 Reference Parsing
Parse the bibliography to identify cited papers requiring follow-up retrieval. For each relevant cited paper, repeat Phase A.

---

## Phase C: Cross-Paper Retrieval & Synthesis

### C.1 Reference Chain
For each cited paper identified as relevant in Phase B:
1. `brave_web_search` for the cited paper by title/authors
2. Retrieve full text via YoBrowser or direct PDF
3. Extract key claims, equations, and parameters
4. Save to local file with traceable filename: `src_<paper_id>.txt`

### C.2 Cross-Paper Comparison Matrix
Build a structured comparison:
| Parameter/Claim | Paper A | Paper B | Paper C | Consensus |
|:---------------|:--------|:--------|:--------|:----------|
| Claim 1 | Value | Value | Value | Agreed/Disputed |
| Claim 2 | ... | ... | ... | ... |

### C.3 Contradiction Documentation
Explicitly document where papers disagree. Label:
- `[CONSENSUS]` — >=2 independent papers agree
- `[DISPUTED]` — papers disagree; document both positions
- `[SINGLE-SOURCE]` — only one paper makes this claim

---

## Phase D: Quantitative Verification

### D.1 Claim Extraction
Use Python to parse extracted paper text and identify ALL quantitative claims:
- Numeric parameters (coupling constants, energies, timescales)
- Equations with numeric coefficients
- Statistical results (p-values, confidence intervals)
- Order-of-magnitude estimates

### D.2 Independent Verification Scripts
For EVERY quantitative claim:
1. Write a self-contained Python script that independently calculates/reproduces the claim
2. Use only standard library Python
3. Document all assumptions and intermediate steps
4. Execute the script and capture output
5. Label: `[CODE-EXECUTED]`

### D.3 Back-of-Envelope Sanity Checks
For every quantitative result:
- Compare against known physical constants/relationships
- Verify order-of-magnitude consistency
- Check for physically impossible values (negative probabilities, >1 fidelities)
- Document any anomalies

### D.4 Discrepancy Handling
If independent verification disagrees with the source paper:
1. Re-extract the claim from the source text (possible misreading)
2. Check unit conversions
3. Try alternate calculation approaches
4. Document as `[DISCREPANCY: source claims X, verification yields Y]`
5. Flag for Stage 3 review

---

## Phase E: Structured Output with Source Labels

### E.1 Document Structure
Every research output document must include:
```
# [Title]
**Date:** <ISO 8601>
**Sources:** <list of source papers with identifiers>

## Executive Summary
## Methodology
## Results (with labeled claims)
## Discussion
## References
```

### E.2 Source Labeling Protocol
Every claim in the output MUST carry one of:
- `[CODE-EXECUTED]` — Python-verified quantitative result (include script reference)
- `[EXTERNAL-SOURCE: filename]` — derived from a specific source file
- `[LLM-INFERRED]` — agent reasoning, synthesis, or interpretation
- `[WEB-SEARCH: query]` — retrieved via web search (requires cross-reference verification)
- `[UNVERIFIED-LLM]` — claim from training data, not independently verified
- `[CONSENSUS]` — independently confirmed by >=2 papers
- `[DISPUTED]` — conflicting claims across sources
- `[SINGLE-SOURCE]` — only one paper supports this claim

### E.3 Citation Format
```
[EXTERNAL-SOURCE: swift2018.txt] — Swift et al. (2018), PCCP 20, 12373
Page/section reference where claim appears: Section 3.2, Table 1
```

---

## Phase F: Post-Write Audit & Verification

### F.1 Filesystem Verification
After EVERY file write:
```
Test-Path <file>
Get-Content <file> -First 5
```
Never trust tool success messages alone — verify on disk.

### F.2 Git Commit Protocol
After each research document is written and verified:
```
git add <file>
git commit -m "ACTION:CREATE FILE: <path> RATIONALE: <summary of findings>"
git log -1 --oneline  # verify commit exists
```

### F.3 Claim-Evidence Mapping
For the completed document, map every claim to its evidence:
| Claim | Source Label | Evidence |
|:------|:-------------|:---------|
| "J1 = 0.178 Hz" | [CODE-EXECUTED: _verify_j_coupling.py] | Python output matches Swift et al. Table 1 |
| "Posner molecule has 6 31P nuclei" | [EXTERNAL-SOURCE: swift2018.txt] | Swift et al. Section 2.1 |

### F.4 Reproducibility Check
Re-execute ALL Python scripts. Confirm identical output to what appears in the document.
If output differs: `[NON-REPRODUCIBLE: artifact <ID> — output changed from X to Y]`

### F.5 Cross-Document Consistency Audit
Verify no contradictions between sequential research documents (0.3.md, 0.4.md, 0.5.md).
If contradiction found: `[CONTRADICTION: <doc A> claims X, <doc B> claims Y]`

---

## Tool Reference

| Phase | Tools Used | Purpose |
|:------|:-----------|:--------|
| A — Discovery | `brave_web_search`, `brave_local_search` | Find papers by ID, title, or domain keywords |
| B — Deep Read | `load_url`, `cdp_send` (Runtime.evaluate) | Structured extraction from arXiv HTML |
| C — Cross-Paper | `brave_web_search`, `load_url`, `cdp_send` | Retrieve cited papers, compare claims |
| D — Verification | Python `exec` | Independent calculation, back-of-envelope checks |
| E — Output | `write` | Structured document with source labels |
| F — Audit | `exec` (`Test-Path`, `git log`), Python | Filesystem verification, reproducibility, consistency |

---

## Domain Applicability

This protocol is **domain-agnostic**. Replace:
- "arXiv ID" -> publisher DOI for non-arXiv papers
- "YoBrowser CDP extraction" -> direct PDF text extraction for non-HTML papers
- "physical constants" -> domain-specific known references
- "coupling constants" -> domain-specific quantitative parameters

The six-phase structure (Discovery -> Deep Read -> Cross-Paper -> Verify -> Output -> Audit) applies to ALL research domains.
