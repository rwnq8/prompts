---
template: SMOKE-TEST
version: "1.0"
description: "HTTP-level + browser-level smoke test for web artifact deployments"
parameters:
  PROJECT_NAME:
    description: "Name of the project being tested"
    required: true
  ARTIFACT_URLS:
    description: "One or more live artifact URLs (comma-separated)"
    required: true
  EXPECTED_FEATURES:
    description: "Comma-separated expected features: buttons, canvas, animation, video, audio, forms"
    required: false
    default: "buttons"
  TIMEOUT_SECONDS:
    description: "HTTP request timeout in seconds"
    required: false
    default: "15"
---

# SMOKE TEST — {{PROJECT_NAME}}

**Date:** {{CURRENT_DATE}}
**Artifacts:** {{ARTIFACT_URLS}}
**Expected Features:** {{EXPECTED_FEATURES}}

---

## 1. SMOKE TEST PURPOSE

This smoke test verifies that deployed web artifacts are LIVE, LOADING, and FUNCTIONALLY INTACT by performing:

| Layer | Tool | What It Checks |
|:------|:-----|:---------------|
| **Layer 1: HTTP** | `tools/smoke_test_artifacts.py` | Status codes, HTML structure, interactive elements, assets, meta tags, error indicators |
| **Layer 2: Browser** | YoBrowser (`load_url` + `cdp_send`) | JS console errors, DOM mutations, canvas rendering, animation playback, button click output |

**HARD RULE:** Both layers must pass before declaring an artifact smoke-test-clean.

---

## 2. LAYER 1: HTTP SMOKE TEST (Python)

### 2.1 Quick Run (Single URL)

```powershell
python "G:\My Drive\prompts\tools\smoke_test_artifacts.py" --url "{{ARTIFACT_URLS}}"
```

### 2.2 Config-Based Run (Multiple Artifacts With Expectations)

Create a temp config file and execute:

```python
# _smoke_config.py — generates config, writes to disk, then executes smoke test
import json, subprocess, sys

config = {
    "project": "{{PROJECT_NAME}}",
    "artifacts": [
        {
            "name": "Main App",
            "url": "{{ARTIFACT_URLS}}",
            "expected": {
                {% if "buttons" in EXPECTED_FEATURES %}"has_buttons": true,{% endif %}
                {% if "canvas" in EXPECTED_FEATURES %}"has_canvas": true,{% endif %}
                {% if "animation" in EXPECTED_FEATURES %}"has_animation": true,{% endif %}
                "min_scripts": 1,
                "min_stylesheets": 1
            }
        }
    ],
    "timeout_seconds": {{TIMEOUT_SECONDS}}
}

config_path = "G:\\My Drive\\projects\\{{PROJECT_NAME}}\\_smoke_config.json"
with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

# Execute smoke test
result = subprocess.run(
    ["python", r"G:\My Drive\prompts\tools\smoke_test_artifacts.py", config_path],
    capture_output=True, text=True
)
print(result.stdout)
if result.returncode != 0:
    print("SMOKE TEST FAILED", file=sys.stderr)
    sys.exit(1)
```

### 2.3 What HTTP Layer Checks

| Category | Checks |
|:---------|:-------|
| **HTTP** | Status code = 200, Content-Type, response size, fetch time |
| **Interactive** | `<button>` count and details (type, id, disabled, onclick), `<input>` count and types, `<select>`, `<textarea>`, `on*` event handlers |
| **Media** | `<canvas>` count and dimensions, `<video>`, `<audio>`, `<img>` count (missing alt flagged), `<svg>` elements |
| **Animation** | `@keyframes` rules extracted from CSS, `animation:` and `transition:` properties, HTML classes with animation terms |
| **Assets** | `<script>` tags (inline + external sources), `<link rel="stylesheet">` count, `<style>` blocks |
| **SEO/Meta** | `<title>`, `<meta name="description">`, `<meta name="viewport">`, Open Graph tags |
| **Errors** | Console.error-like patterns in visible text, error patterns in inline scripts |
| **Expectations** | Validates `has_buttons`, `has_canvas`, `has_animation`, `title_contains`, `min_scripts`, `min_stylesheets` |

---

## 3. LAYER 2: BROWSER SMOKE TEST (YoBrowser)

Layer 1 cannot detect JavaScript runtime errors, canvas rendering, or animation playback. Layer 2 fills this gap using YoBrowser's full browser.

### 3.1 Browser Test Protocol

For EACH artifact URL, execute the following YoBrowser sequence:

```
STEP 1: load_url → "{{ARTIFACT_URL}}"
STEP 2: wait 3 seconds for JS execution
STEP 3: Runtime.evaluate → check console errors
STEP 4: Runtime.evaluate → query DOM for interactive elements
STEP 5: Input.dispatchMouseEvent → click first button (if present)
STEP 6: Runtime.evaluate → verify DOM changed after click
STEP 7: Page.captureScreenshot → save evidence
```

### 3.2 Detailed CDP Commands

**Step 1 — Load Page:**
```json
{ "method": "load_url", "params": { "url": "{{ARTIFACT_URLS}}" } }
```

**Step 2 — Wait for JS (using Runtime.evaluate with delay):**
```json
{
  "method": "Runtime.evaluate",
  "params": {
    "expression": "new Promise(r => setTimeout(r, 3000)).then(() => 'ready')",
    "awaitPromise": true
  }
}
```

**Step 3 — Check Console Errors:**
```json
{
  "method": "Runtime.evaluate",
  "params": {
    "expression": "JSON.stringify(window.__smokeErrors || [])"
  }
}
```

First, inject console error capture BEFORE page load:
```javascript
// Inject via Runtime.evaluate BEFORE navigating
window.__smokeErrors = [];
const origError = console.error;
console.error = function(...args) {
    window.__smokeErrors.push(args.map(String).join(' '));
    origError.apply(console, args);
};
```

**Step 4 — Query DOM for Interactive Elements:**
```json
{
  "method": "Runtime.evaluate",
  "params": {
    "expression": "JSON.stringify({ buttons: document.querySelectorAll('button').length, canvases: document.querySelectorAll('canvas').length, inputs: document.querySelectorAll('input').length, videos: document.querySelectorAll('video').length })"
  }
}
```

**Step 5 — Click First Button:**
```json
{
  "method": "DOM.querySelector",
  "params": { "selector": "button" }
}
```
→ If nodeId returned:
```json
{
  "method": "Input.dispatchMouseEvent",
  "params": { "type": "mousePressed", "x": 10, "y": 10, "button": "left", "clickCount": 1 }
}
```
```json
{
  "method": "Input.dispatchMouseEvent",
  "params": { "type": "mouseReleased", "x": 10, "y": 10, "button": "left", "clickCount": 1 }
}
```
**IMPORTANT:** Get actual button coordinates via `DOM.getBoxModel` first — do not guess coordinates.

**Step 6 — Verify DOM Changed:**
```json
{
  "method": "Runtime.evaluate",
  "params": {
    "expression": "JSON.stringify({ domChanged: window.__smokeDomChanged || false })"
  }
}
```

Inject MutationObserver BEFORE interactions:
```javascript
window.__smokeDomChanged = false;
const observer = new MutationObserver(() => { window.__smokeDomChanged = true; });
observer.observe(document.body, { childList: true, subtree: true, attributes: true });
```

**Step 7 — Screenshot Evidence:**
```json
{
  "method": "Page.captureScreenshot",
  "params": { "format": "png" }
}
```

### 3.3 Canvas Rendering Check

For artifacts with `<canvas>` elements:

```json
{
  "method": "Runtime.evaluate",
  "params": {
    "expression": "(() => { const canvases = document.querySelectorAll('canvas'); const results = []; canvases.forEach((c, i) => { const ctx = c.getContext('2d'); if (!ctx) { results.push({index: i, rendered: false, reason: 'no 2d context'}); return; } const data = ctx.getImageData(0, 0, Math.min(c.width, 10), Math.min(c.height, 10)).data; const hasContent = Array.from(data).some(v => v !== 0); results.push({index: i, width: c.width, height: c.height, rendered: hasContent}); }); return JSON.stringify(results); })()"
  }
}
```

### 3.4 Animation Playback Check

```json
{
  "method": "Runtime.evaluate",
  "params": {
    "expression": "JSON.stringify({ animations: document.getAnimations ? document.getAnimations().length : -1, animationCount: document.querySelectorAll('[class*=\"animate\"], [class*=\"anim-\"]').length })"
  }
}
```

---

## 4. PASS/FAIL CRITERIA

### Layer 1 (HTTP) — ALL of:
- [ ] HTTP status = 200
- [ ] HTML contains expected interactive elements (per EXPECTED_FEATURES)
- [ ] Zero console.error-like patterns in visible text
- [ ] All expectation checks pass
- [ ] `<title>` tag present

### Layer 2 (Browser) — ALL of:
- [ ] Page loads without JS console errors
- [ ] At least one button clickable (if buttons expected)
- [ ] DOM mutation detected after interaction (if buttons clicked)
- [ ] Canvas has non-blank content (if canvas expected)
- [ ] Animations detected (if animation expected)
- [ ] Screenshot captured as evidence

### Overall: BOTH layers must return ALL pass.

---

## 5. FAILURE RESPONSE

If ANY check fails:

1. **Document the failure** — which layer, which URL, what failed
2. **Capture evidence** — screenshot (Layer 2), HTTP response (Layer 1)
3. **Do NOT proceed** to deployment or user communication
4. **File as P1 BLOCKER** in project BACKLOG.md
5. **Cross-reference** with CROSS-PROJECT-LEARNINGS.md for similar patterns

### Common Failure Patterns

| Symptom | Likely Cause | Fix |
|:--------|:-------------|:----|
| HTTP 404 | Wrong URL, GitHub Pages not deployed | Verify URL, check Actions tab |
| HTTP 200 but no buttons found | Static HTML, JS not loaded | Check script src paths, CDN availability |
| Canvas present but blank | JS rendering not executed | Check for JS errors, verify init code |
| Console errors | Missing dependencies, syntax errors | Check Network tab for 404s on JS/CSS |
| No DOM change on click | Event handler not bound, JS error | Check console after click event |

---

## 6. EVIDENCE REQUIREMENTS

After testing, save to project directory:

```
{{PROJECT_NAME}}/
  _smoke_config.json          ← Config used for Layer 1
  _smoke_report.txt           ← Layer 1 output report
  _smoke_screenshot.png       ← Layer 2 screenshot evidence
  _smoke_browser_console.txt  ← Layer 2 console output
```

---

## 7. INTEGRATION WITH RELEASE CHECKLIST

This smoke test is a PREREQUISITE for the WEB-APP-RELEASE-CHECKLIST:

```
SMOKE TEST (this template)
    └─→ Both layers PASS
        └─→ WEB-APP-RELEASE-CHECKLIST (full 9-section)
            └─→ Deploy to production
```

Do NOT skip smoke testing and go directly to the release checklist. Smoke tests catch 80% of deployment failures in under 60 seconds.

---

*Generated from SMOKE-TEST.md v1.0. Execute Layer 1 via `tools/smoke_test_artifacts.py`. Execute Layer 2 via YoBrowser CDP commands.*
