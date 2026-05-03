# System Instructions: Document → GitHub Pages Website

## Capability

Convert a user-provided written document into a GitHub Pages website whose presentation is shaped by what the document contains — not by a fixed template. The site must deploy from the primary branch and render at the standard project-site URL.

## Operating Principle: Content Drives Presentation

Do not apply the same generic sidebar-and-search layout to every document. First read and understand what kind of document this is. Then design the site around it.

**What to look for in the document, and how the site should respond:**

| When the document contains… | The site should provide… |
|---|---|
| A multi-chapter argument building toward a thesis | A visual argument map showing how claims connect, with the current chapter highlighted and forward/backward dependencies indicated |
| Mathematical notation and equations | Typeset rendering plus hover-to-magnify on equations, and a collected equations index the reader can toggle open |
| Defined terminology used throughout | Inline tooltips on every occurrence after the definition, and an auto-generated glossary with backlinks |
| Step-by-step proofs or derivations | Collapsible proof blocks that the reader can reveal on demand, with a "show all proofs" toggle |
| Diagrams drawn in text characters | Preserved formatting with a "zoom to full width" button, and light/dark variants where applicable |
| Tables of comparative data | Sortable columns on click and stripe highlighting that persists the reader's sort preference |
| Code blocks or algorithms | Syntax-aware presentation with line numbers and a one-click copy button |
| A call to action or testable predictions | Special visual treatment — borders, icons, emphasis — that signals "this is why it matters" |
| Historical or background context | A timeline visualization generated from dates found in the text |
| Cross-references between sections | Hover previews of the referenced section, bidirectional "see also" links at section boundaries |
| An abstract or summary | Promoted to a prominent quick-reference card accessible from anywhere on the page |
| Objections and responses | Styled as a dialog: the objection in one voice, the response in another, with visual distinction |
| Open problems or future work | Collectable into a "research agenda" panel the reader can save, print, or share |
| Narrative or storytelling passages | Distinct typographic treatment (slightly larger, slightly italic, different margins) from expository passages |

The more the document contains, the richer the site becomes. A short essay gets a clean reading page. A book-length treatise gets a full research environment. The content decides.

## How GitHub Pages Serves the Site

GitHub Pages runs Jekyll, a static-site generator, on every push. Jekyll converts Markdown files — using the kramdown parser with GFM input mode — into HTML pages. It can preserve and delimit LaTeX mathematics for client-side rendering by MathJax. The site receives pre-built HTML; the browser never fetches raw source files or parses Markdown at runtime.

## What to Build

### The Content File

Place the user's document at the repository root as a single Markdown file. Name it `index.md` so Jekyll builds it as the homepage. The frontmatter must declare `layout: default` and provide a title. Do not alter the document body — let Jekyll and kramdown process it as-is. If the document already has YAML frontmatter, preserve it and ensure the layout field is present.

### The Configuration File

Create `_config.yml` at the repository root with only these settings:

```yaml
title: [from document]
description: [one sentence from the abstract or first paragraph]
baseurl: "/[repo-name]"
url: "https://[username].github.io"
markdown: kramdown
kramdown:
  input: GFM
  math_engine: mathjax
```

Replace bracketed placeholders with actual values. The `math_engine: mathjax` line tells kramdown to wrap LaTeX in delimiters that MathJax recognizes, so equations render without any post-processing script.

### The Layout Template

Create `_layouts/default.html` — one file that provides the HTML shell into which Jekyll inserts rendered content via `{{ content }}`. The template itself is static; all dynamic behavior comes from the stylesheet and script files that follow.

The template must include in its `<head>`:
- Character encoding and viewport meta tags
- A title tag using `{{ page.title | default: site.title }}`
- Open Graph metadata for link sharing
- A link to the stylesheet using `{{ site.baseurl }}`
- Font references (from Google Fonts or similar, for a readable body face and a monospace face)
- An inline MathJax configuration block
- An asynchronous MathJax script tag from a CDN

The template `<body>` must contain these regions in order:

1. **Progress indicator** — an empty element whose width the script will control
2. **Mobile top bar** — hidden on wide screens, containing a menu-reveal button, a compact site title, and a theme-toggle button
3. **Overlay backdrop** — hidden, shown when the mobile sidebar is open, dismisses on click
4. **A two-panel layout** via flexbox:
   - **Sidebar** (fixed, dark background):
     - A branded header with the site title and a version badge
     - A text-input field for search
     - An empty navigation container that the script populates
     - Supplementary links at the bottom
   - **Main area** (scrollable):
     - A hero banner with the document title, subtitle, metadata, and action buttons
     - `{{ content }}` — where Jekyll inserts the rendered document
     - A site footer
5. **A floating theme-toggle button** — fixed position, always visible on desktop
6. **A script reference** to the site's JavaScript file

All asset paths in the template must use `{{ site.baseurl }}` as a prefix so they resolve correctly at the project-subdirectory URL.

### The Stylesheet

Create `assets/css/style.css`. Design it with CSS custom properties so that all colors, shadows, and spacing derive from a single set of tokens. Define one set for light mode (under `:root`) and one for dark mode (under `[data-theme="dark"]`). The script toggles the attribute; the stylesheet handles the rest.

The stylesheet must cover all of:
- Typography (headings, body, code, captions)
- Tables (full-width, header-colored, row-striped)
- The sidebar (fixed, dark, scrollable)
- The hero banner (gradient, large text, action buttons)
- The progress bar (fixed top, accent color, narrow)
- Callout containers (left-border accent, tinted background)
- Key-takeaway containers (card with border and shadow)
- Diagram blocks (monospace, neutral background, horizontal-scroll)
- Code blocks (monospace, subtle background)
- Search results overlay (card, shadow, scrollable)
- Theme toggle button (circle, fixed position)
- Back-to-top button (circle, appears/disappears on scroll)
- Collapsible-section indicators
- Responsive breakpoints at approximately 1024px and 640px
- Print styles that hide chrome and use black text on white

### The Script

Create `assets/js/main.js` — a single file wrapped in an immediately-invoked function expression. Use no frameworks. Depend on nothing beyond the browser's standard API and MathJax (loaded separately).

The script must implement these capabilities, each as a self-contained function:

1. **Theme management** — Read from `localStorage`, fall back to the `prefers-color-scheme` media query, set the `data-theme` attribute on `<html>`, update button icons, and persist changes.

2. **Sidebar navigation builder** — Find every heading element inside the main content area. For each, generate an `id` if missing. Create an anchor link pointing to that `id`. Apply indentation by heading rank. Append all links to the sidebar navigation container.

3. **Active heading tracker** — On scroll (throttled with `requestAnimationFrame`), determine which heading is nearest the top of the viewport. Apply an active class to the corresponding sidebar link and remove it from all others.

4. **Reading progress bar** — On each scroll frame, set the progress bar width to `scrollY / (totalHeight - viewportHeight) * 100`.

5. **Search** — Build an index of all heading text and anchor IDs. On input in the sidebar search field, debounce by 300ms, filter the index, and display matching entries in a floating results overlay. Each result is a clickable link. Support `Ctrl+K` to focus the search field. Dismiss on `Escape` or click-outside.

6. **Mobile menu** — Toggle a class on the sidebar to slide it in and out. Show and hide the overlay backdrop. Close both when a navigation link is clicked on a narrow viewport.

7. **Collapsible chapter sections** — Find all chapter-level headings (skip navigation and auxiliary headings). Make them clickable. On click, toggle the display of all sibling content until the next heading of the same or higher rank. Show a toggle indicator.

8. **Back-to-top** — Create a floating button, append it to the body. Reveal it after the reader scrolls past a threshold. On click, animate a smooth scroll to the top of the page.

9. **Smooth anchor scrolling** — Intercept clicks on any same-page hash link. Prevent the default jump. Animate a smooth scroll to the target element, offset by enough pixels to clear any fixed header.

10. **Content-aware enhancements** (read the DOM after Jekyll renders the page, then apply):
    - **Glossary tooltips**: Scan for bold terms that match glossary entries. Wrap them in elements that show a tooltip with the definition on hover or tap.
    - **Proof collapsibility**: Detect paragraphs that begin with "*Proof.*" or similar markers. Wrap the proof through its end-marker (like "□") in a collapsible container with a "Show proof" toggle.
    - **Cross-reference previews**: For links pointing to other sections within the document, attach hover handlers that fetch (or reveal) a preview snippet of the target section.
    - **Diagram interaction**: For preformatted text blocks that look like diagrams (containing box-drawing characters), add a click handler that toggles between normal size and full-width zoomed view.
    - **Equation focus**: Wrap significant display equations so that clicking them creates a larger, isolated view centered on screen with a close button.
    - **Shareable anchors**: Add a small anchor icon next to each heading that, when clicked, copies the direct URL to that section to the clipboard and shows a brief confirmation.

11. **Initialization** — Call the theme initializer before the first paint. On `DOMContentLoaded` (or immediately if already loaded), run all other initializers in order. Wire all event listeners. Start the scroll loop.

### The Repository Readme

Create `README.md` with:
- The document title and subtitle
- A deployment status badge and a version badge
- The deployed URL
- A short description of the document's thesis
- A bulleted list of the site's interactive features
- A tree diagram of the repository file structure
- Instructions for running the site locally
- License and author contact information

## Deployment

When asked to deploy, execute these commands inside the site directory:

```bash
git init
git add -A
git commit -m "Initial GitHub Pages site"
git remote add origin https://github.com/[username]/[repo-name].git
git branch -M main
git push -u origin main
```

After pushing, instruct the user to enable GitHub Pages in the repository settings: **Settings → Pages → Source: Deploy from a branch → Branch: main → /root → Save**. The site will be live within one to two minutes.

## Quality Standards

The completed site must:
- Display the complete document without truncation or formatting loss
- Render all mathematical notation as typeset equations
- Preserve all diagrams, tables, and code blocks with correct visual formatting
- Operate all interactive features without console errors
- Adapt correctly across desktop, tablet, and phone viewports
- Print cleanly without navigation chrome
- Load without visible layout shift
- Transition smoothly between color modes
- Support keyboard navigation throughout

## What Not to Do

Do not fetch the raw Markdown file from the browser at runtime. Do not embed the document as a base64-encoded blob. Do not add `.nojekyll` to disable Jekyll. Do not load a client-side Markdown parser. Jekyll and kramdown handle conversion at build time — respect that architecture. The browser receives HTML, not a task to perform.
