#!/usr/bin/env python3
"""
SMOKE TEST FOR WEB ARTIFACTS -- v1.0
====================================
HTTP-level functional smoke test for live artifact pages (GitHub Pages, etc.).
Does NOT require a browser. Checks HTML for functional indicators:
  - Interactive elements (buttons, inputs, event handlers)
  - Canvas elements
  - Animation/CSS indicators
  - JavaScript presence
  - Asset loading (CSS, JS, images)
  - SEO/meta basics
  - Common error patterns

Usage:
  python smoke_test_artifacts.py [config.json]
  python smoke_test_artifacts.py --url https://example.com/artifact/

Config JSON format:
{
  "project": "My Project",
  "artifacts": [
    {
      "name": "Main App",
      "url": "https://username.github.io/project/",
      "expected": {
        "has_buttons": true,
        "has_canvas": false,
        "has_animation": false,
        "title_contains": "My Project"
      }
    }
  ],
  "timeout_seconds": 15,
  "user_agent": "SmokeTest/1.0"
}

If no config provided, runs in single-URL mode with --url.
"""

import json
import sys
import time
import urllib.request
import urllib.error
import html.parser
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


# -- HTML Parser: extract functional indicators --------------------------
class FunctionalIndicatorParser(html.parser.HTMLParser):
    """Parse HTML to find interactive elements, assets, and error patterns."""

    def __init__(self):
        super().__init__()
        self.buttons = 0
        self.button_details: List[str] = []
        self.inputs = 0
        self.input_details: List[str] = []
        self.selects = 0
        self.textareas = 0
        self.canvases = 0
        self.canvas_details: List[str] = []
        self.videos = 0
        self.audios = 0
        self.scripts = 0
        self.script_sources: List[str] = []
        self.inline_scripts = 0
        self.stylesheets = 0
        self.stylesheet_hrefs: List[str] = []
        self.inline_styles = 0
        self.images = 0
        self.images_missing_alt = 0
        self.links = 0
        self.onclick_elements = 0
        self.animation_classes: List[str] = []
        self._in_title = False
        self._title_data = ""
        self.title_tag = ""
        self.meta_description = ""
        self.meta_viewport = ""
        self.open_graph: Dict[str, str] = {}
        self.svg_elements = 0

        # Error indicators
        self.console_error_like: List[str] = []
        self._in_script = False
        self._script_content = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "button":
            self.buttons += 1
            btn_type = attrs_dict.get("type", "button")
            btn_id = attrs_dict.get("id", "(no id)")
            onclick = "onclick" in attrs_dict
            disabled = "disabled" in attrs_dict
            self.button_details.append(
                f"id={btn_id} type={btn_type}"
                f"{' onclick' if onclick else ''}"
                f"{' DISABLED' if disabled else ''}"
            )

        elif tag == "input":
            self.inputs += 1
            inp_type = attrs_dict.get("type", "text")
            inp_id = attrs_dict.get("id", "(no id)")
            self.input_details.append(f"id={inp_id} type={inp_type}")

        elif tag == "select":
            self.selects += 1

        elif tag == "textarea":
            self.textareas += 1

        elif tag == "canvas":
            self.canvases += 1
            cid = attrs_dict.get("id", "(no id)")
            cw = attrs_dict.get("width", "?")
            ch = attrs_dict.get("height", "?")
            self.canvas_details.append(f"id={cid} {cw}x{ch}")

        elif tag == "video":
            self.videos += 1

        elif tag == "audio":
            self.audios += 1

        elif tag == "script":
            self.scripts += 1
            src = attrs_dict.get("src", "")
            if src:
                self.script_sources.append(src)
            else:
                self.inline_scripts += 1
                self._in_script = True
                self._script_content = ""

        elif tag == "link":
            rel = attrs_dict.get("rel", "")
            if "stylesheet" in rel:
                self.stylesheets += 1
                href = attrs_dict.get("href", "")
                if href:
                    self.stylesheet_hrefs.append(href)

        elif tag == "style":
            self.inline_styles += 1

        elif tag == "img":
            self.images += 1
            if "alt" not in attrs_dict:
                self.images_missing_alt += 1

        elif tag == "a":
            self.links += 1

        elif tag == "title":
            self._in_title = True
            self._title_data = ""

        elif tag == "meta":
            name = attrs_dict.get("name", "")
            content = attrs_dict.get("content", "")
            prop = attrs_dict.get("property", "")
            if name == "description":
                self.meta_description = content
            elif name == "viewport":
                self.meta_viewport = content
            elif prop.startswith("og:"):
                self.open_graph[prop] = content

        elif tag == "svg":
            self.svg_elements += 1

        # Check for onclick and other event handlers
        for attr_name in attrs_dict:
            if attr_name.startswith("on"):
                self.onclick_elements += 1
                break

        # Check for animation-related classes
        cls = attrs_dict.get("class", "")
        if cls:
            cls_lower = cls.lower()
            for anim_term in ["animate", "animation", "transition", "fade",
                              "slide", "spin", "pulse", "bounce", "shake",
                              "rotate", "scale", "morph", "reveal"]:
                if anim_term in cls_lower:
                    self.animation_classes.append(f"{tag}.{cls}")
                    break

    def handle_data(self, data):
        if self._in_script:
            self._script_content += data

        if getattr(self, '_in_title', False):
            self._title_data += data

        # Check for console.error-like patterns in visible text
        data_stripped = data.strip()
        if data_stripped and any(err in data_stripped.lower() for err in [
            "console.error", "console.warn", "uncaught typeerror",
            "uncaught referenceerror", "cannot read property",
            "undefined is not", "failed to load",
        ]):
            self.console_error_like.append(data_stripped[:200])

    def handle_endtag(self, tag):
        if tag == "script" and self._in_script:
            self._in_script = False
            # Check inline script for error-like patterns
            sc_lower = self._script_content.lower()
            for err_pat in [
                "console.error", "console.warn",
                "throw new error", "throw error",
                "try {", "catch (",
            ]:
                if err_pat in sc_lower:
                    if err_pat not in [x[:50] for x in self.console_error_like]:
                        self.console_error_like.append(
                            f"[inline script] {err_pat} found"
                        )
            self._script_content = ""

        elif tag == "title":
            self._in_title = False
            self.title_tag = getattr(self, '_title_data', '').strip()


# -- CSS Parser: extract animation rules ---------------------------------
def extract_css_animations(css_text: str) -> Dict[str, List[str]]:
    """Scan CSS text for animation/transition rules."""
    result = {
        "keyframes": [],
        "animation_properties": [],
        "transition_properties": [],
    }

    # Find @keyframes rules
    kf_matches = re.findall(r'@keyframes\s+([a-zA-Z_][\w-]*)', css_text)
    result["keyframes"] = list(set(kf_matches))

    # Find animation property usage
    anim_matches = re.findall(r'animation:\s*([^;}]*)', css_text)
    result["animation_properties"] = [a.strip()[:80] for a in anim_matches]

    # Find transition property usage
    trans_matches = re.findall(r'transition:\s*([^;}]*)', css_text)
    result["transition_properties"] = [t.strip()[:80] for t in trans_matches]

    return result


# -- Core: fetch and analyze a single URL --------------------------------
def fetch_and_analyze(url: str, timeout: int = 15, user_agent: str = "SmokeTest/1.0") -> Dict[str, Any]:
    """Fetch a URL via HTTP and analyze HTML for functional indicators.

    Returns a dict with all findings.
    """
    result = {
        "url": url,
        "status": "unknown",
        "http_code": None,
        "content_type": None,
        "content_length": 0,
        "fetch_time_ms": 0,
        "error": None,
        "html_analysis": {},
        "warnings": [],
        "passed": False,
    }

    # Fetch
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result["http_code"] = resp.status
            result["content_type"] = resp.headers.get("Content-Type", "")
            raw = resp.read()
            result["content_length"] = len(raw)
            text = raw.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        result["http_code"] = e.code
        result["error"] = f"HTTP {e.code}: {e.reason}"
        result["fetch_time_ms"] = int((time.time() - start) * 1000)
        return result
    except urllib.error.URLError as e:
        result["error"] = f"URL Error: {e.reason}"
        result["fetch_time_ms"] = int((time.time() - start) * 1000)
        return result
    except Exception as e:
        result["error"] = str(e)
        result["fetch_time_ms"] = int((time.time() - start) * 1000)
        return result

    result["fetch_time_ms"] = int((time.time() - start) * 1000)
    result["status"] = "fetched"

    # Analyze HTML
    parser = FunctionalIndicatorParser()
    parser.feed(text)

    # Extract CSS for animation analysis
    css_text = ""
    style_matches = re.findall(r'<style[^>]*>(.*?)</style>', text, re.DOTALL | re.IGNORECASE)
    for m in style_matches:
        css_text += m + "\n"

    css_analysis = extract_css_animations(css_text)

    html_analysis = {
        "interactive": {
            "buttons": parser.buttons,
            "button_details": parser.button_details,
            "inputs": parser.inputs,
            "input_details": parser.input_details,
            "selects": parser.selects,
            "textareas": parser.textareas,
            "onclick_elements": parser.onclick_elements,
        },
        "media": {
            "canvases": parser.canvases,
            "canvas_details": parser.canvas_details,
            "videos": parser.videos,
            "audios": parser.audios,
            "images": parser.images,
            "images_missing_alt": parser.images_missing_alt,
            "svg_elements": parser.svg_elements,
        },
        "animation": {
            "css_keyframes": css_analysis["keyframes"],
            "css_animation_count": len(css_analysis["animation_properties"]),
            "css_transition_count": len(css_analysis["transition_properties"]),
            "html_animation_classes": parser.animation_classes,
        },
        "assets": {
            "scripts": parser.scripts,
            "script_sources": parser.script_sources,
            "inline_scripts": parser.inline_scripts,
            "stylesheets": parser.stylesheets,
            "stylesheet_hrefs": parser.stylesheet_hrefs,
            "inline_styles": parser.inline_styles,
        },
        "seo_meta": {
            "title": parser.title_tag,
            "meta_description": parser.meta_description,
            "meta_viewport": parser.meta_viewport,
            "open_graph": parser.open_graph,
        },
        "error_indicators": parser.console_error_like,
        "links_count": parser.links,
    }

    result["html_analysis"] = html_analysis

    # Generate warnings
    warnings = []

    if parser.buttons == 0 and parser.inputs == 0:
        warnings.append("No interactive elements (buttons/inputs) found")
    if parser.canvases == 0 and parser.videos == 0 and parser.audios == 0:
        warnings.append("No canvas/video/audio elements found")
    if parser.scripts == 0:
        warnings.append("No <script> tags found -- page may be static")
    if parser.stylesheets == 0 and parser.inline_styles == 0:
        warnings.append("No CSS found -- page may be unstyled")
    if not parser.title_tag:
        warnings.append("No <title> tag -- SEO and UX issue")
    if parser.images > 0 and parser.images_missing_alt == parser.images:
        warnings.append(f"All {parser.images} image(s) missing alt text")
    if parser.console_error_like:
        warnings.append(
            f"Potential JS error indicators found: "
            f"{len(parser.console_error_like)} pattern(s)"
        )
    if result["http_code"] != 200:
        warnings.append(f"HTTP status {result['http_code']} (not 200)")

    result["warnings"] = warnings
    result["passed"] = (result["http_code"] == 200 and len(parser.console_error_like) == 0)

    return result


# -- Validate against expected behaviors ---------------------------------
def validate_expectations(analysis: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
    """Check actual findings against expected behaviors.

    Returns a dict of expectation checks.
    """
    checks = {}
    html = analysis.get("html_analysis", {})

    if "has_buttons" in expected:
        actual = html["interactive"]["buttons"] > 0
        checks["has_buttons"] = {
            "expected": expected["has_buttons"],
            "actual": actual,
            "pass": actual == expected["has_buttons"],
        }

    if "has_canvas" in expected:
        actual = html["media"]["canvases"] > 0
        checks["has_canvas"] = {
            "expected": expected["has_canvas"],
            "actual": actual,
            "pass": actual == expected["has_canvas"],
        }

    if "has_animation" in expected:
        actual = (
            len(html["animation"]["css_keyframes"]) > 0
            or html["animation"]["css_animation_count"] > 0
            or html["animation"]["css_transition_count"] > 0
            or len(html["animation"]["html_animation_classes"]) > 0
        )
        checks["has_animation"] = {
            "expected": expected["has_animation"],
            "actual": actual,
            "pass": actual == expected["has_animation"],
        }

    if "title_contains" in expected:
        actual = expected["title_contains"].lower() in html["seo_meta"]["title"].lower()
        checks["title_contains"] = {
            "expected": f'contains "{expected["title_contains"]}"',
            "actual": f'"{html["seo_meta"]["title"]}"',
            "pass": actual,
        }

    if "min_scripts" in expected:
        actual = html["assets"]["scripts"] >= expected["min_scripts"]
        checks["min_scripts"] = {
            "expected": f'>= {expected["min_scripts"]}',
            "actual": html["assets"]["scripts"],
            "pass": actual,
        }

    if "min_stylesheets" in expected:
        actual = html["assets"]["stylesheets"] >= expected["min_stylesheets"]
        checks["min_stylesheets"] = {
            "expected": f'>= {expected["min_stylesheets"]}',
            "actual": html["assets"]["stylesheets"],
            "pass": actual,
        }

    return checks


# -- Report Generation ---------------------------------------------------
def generate_report(
    config: Dict[str, Any],
    results: List[Dict[str, Any]],
) -> str:
    """Generate a formatted smoke test report."""
    lines = []
    sep = "=" * 70

    lines.append(sep)
    lines.append(f"SMOKE TEST REPORT: {config.get('project', 'Web Artifacts')}")
    lines.append(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Artifacts tested: {len(results)}")
    lines.append(sep)

    total_passed = 0
    total_checks = 0
    total_checks_passed = 0

    for i, result in enumerate(results, 1):
        lines.append(f"\n{'-' * 70}")
        lines.append(f"[{i}/{len(results)}] {result.get('name', result['url'])}")
        lines.append(f"    URL: {result['url']}")
        lines.append(f"    HTTP: {result['http_code']} ({result['fetch_time_ms']}ms)")
        lines.append(f"    Size: {result['content_length']:,} bytes")

        if result["error"]:
            lines.append(f"    ERROR: {result['error']}")
            lines.append(f"    RESULT: FAIL")
            continue

        html = result["html_analysis"]

        # Interactive elements
        inter = html["interactive"]
        lines.append(f"\n  [Interactive Elements]")
        lines.append(f"    Buttons: {inter['buttons']}  |  Inputs: {inter['inputs']}"
                     f"  |  Selects: {inter['selects']}  |  Textareas: {inter['textareas']}")
        lines.append(f"    On* handlers: {inter['onclick_elements']}")
        if inter["button_details"]:
            for bd in inter["button_details"]:
                lines.append(f"      - {bd}")

        # Media elements
        media = html["media"]
        lines.append(f"\n  [Media Elements]")
        lines.append(f"    Canvases: {media['canvases']}  |  Videos: {media['videos']}"
                     f"  |  Audio: {media['audios']}  |  SVGs: {media['svg_elements']}")
        lines.append(f"    Images: {media['images']} (missing alt: {media['images_missing_alt']})")
        if media["canvas_details"]:
            for cd in media["canvas_details"]:
                lines.append(f"      - {cd}")

        # Animation
        anim = html["animation"]
        lines.append(f"\n  [Animation Indicators]")
        lines.append(f"    @keyframes: {len(anim['css_keyframes'])}  |  "
                     f"animation props: {anim['css_animation_count']}  |  "
                     f"transition props: {anim['css_transition_count']}")
        if anim["css_keyframes"]:
            lines.append(f"    Keyframe names: {', '.join(anim['css_keyframes'][:10])}")
        if anim["html_animation_classes"]:
            lines.append(f"    Animation classes: {len(anim['html_animation_classes'])} found")

        # Assets
        assets = html["assets"]
        lines.append(f"\n  [Assets]")
        lines.append(f"    Scripts: {assets['scripts']} ({assets['inline_scripts']} inline)"
                     f"  |  Stylesheets: {assets['stylesheets']}"
                     f"  |  Inline styles: {assets['inline_styles']}")
        if assets["script_sources"]:
            for ss in assets["script_sources"][:5]:
                lines.append(f"      - {ss}")

        # SEO / Meta
        seo = html["seo_meta"]
        lines.append(f"\n  [Meta / SEO]")
        lines.append(f"    Title: \"{seo['title'][:100]}\"")
        lines.append(f"    Description: \"{seo['meta_description'][:100]}\"")
        lines.append(f"    Viewport: \"{seo['meta_viewport'][:80]}\"")
        lines.append(f"    OG tags: {len(seo['open_graph'])}")

        # Error indicators
        errs = html["error_indicators"]
        if errs:
            lines.append(f"\n  [!] POTENTIAL ERROR INDICATORS: {len(errs)}")
            for e in errs[:5]:
                lines.append(f"      - {e[:120]}")

        # Warnings
        if result["warnings"]:
            lines.append(f"\n  [Warnings]")
            for w in result["warnings"]:
                lines.append(f"    ! {w}")

        # Expectation checks
        if result.get("expectation_checks"):
            checks = result["expectation_checks"]
            lines.append(f"\n  [Expectation Checks]")
            for check_name, check_data in checks.items():
                status = "PASS" if check_data["pass"] else "FAIL"
                marker = "[OK]" if check_data["pass"] else "[ERR]"
                lines.append(f"    {marker} {check_name}: expected={check_data['expected']}"
                             f" actual={check_data['actual']}")

        # Overall
        passed = result["passed"]
        if passed:
            total_passed += 1
        lines.append(f"\n  RESULT: {'PASS' if passed else 'FAIL (warnings present)'}")

        if result.get("expectation_checks"):
            for c in result["expectation_checks"].values():
                total_checks += 1
                if c["pass"]:
                    total_checks_passed += 1

    # Summary
    lines.append(f"\n{sep}")
    lines.append(f"SUMMARY")
    lines.append(f"  Artifacts tested: {len(results)}")
    lines.append(f"  Passed: {total_passed}/{len(results)}")
    lines.append(f"  Failed: {len(results) - total_passed}/{len(results)}")
    if total_checks > 0:
        lines.append(f"  Expectation checks: {total_checks_passed}/{total_checks} passed")
    lines.append(sep)

    return "\n".join(lines)


# -- Main -----------------------------------------------------------------
def main():
    config = None
    urls_to_test = []

    # Parse arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--url" and len(sys.argv) > 2:
            urls_to_test = [{"name": sys.argv[2], "url": sys.argv[2]}]
            config = {"project": "Single URL Test", "artifacts": urls_to_test}
        elif arg.endswith(".json"):
            config_path = Path(arg)
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                print(f"ERROR: Config file not found: {arg}")
                sys.exit(1)
        else:
            # Treat as single URL
            urls_to_test = [{"name": arg, "url": arg}]
            config = {"project": "Single URL Test", "artifacts": urls_to_test}
    else:
        # Interactive mode
        print("Smoke Test for Web Artifacts v1.0")
        print("Usage: python smoke_test_artifacts.py [config.json | --url URL | URL]")
        print("\nNo arguments provided. Enter URLs to test (one per line, empty to finish):")
        urls = []
        while True:
            try:
                u = input("  URL> ").strip()
                if not u:
                    break
                urls.append({"name": u, "url": u})
            except (EOFError, KeyboardInterrupt):
                break
        if not urls:
            print("No URLs provided. Exiting.")
            sys.exit(0)
        config = {"project": "Interactive Test", "artifacts": urls}

    artifacts = config.get("artifacts", urls_to_test)
    timeout = config.get("timeout_seconds", 15)
    user_agent = config.get("user_agent", "SmokeTest/1.0")

    print(f"Testing {len(artifacts)} artifact(s)...")
    results = []

    for artifact in artifacts:
        url = artifact["url"]
        name = artifact.get("name", url)
        print(f"  [{len(results)+1}/{len(artifacts)}] {name} ... ", end="", flush=True)

        analysis = fetch_and_analyze(url, timeout=timeout, user_agent=user_agent)
        analysis["name"] = name

        # Check expectations if provided
        expected = artifact.get("expected", {})
        if expected:
            checks = validate_expectations(analysis, expected)
            analysis["expectation_checks"] = checks
            all_pass = all(c["pass"] for c in checks.values())
            analysis["passed"] = analysis["passed"] and all_pass

        results.append(analysis)
        status = "PASS" if analysis["passed"] else "FAIL"
        print(f"{status} (HTTP {analysis.get('http_code', '?')})")

    # Generate and print report
    report = generate_report(config, results)
    print("\n" + report)

    # Save report if config provided
    if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        report_path = Path(sys.argv[1]).with_suffix(".report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport saved to: {report_path}")

    # Exit code
    all_passed = all(r["passed"] for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
