# Document → GitHub Pages Website

Convert any written document into a polished, distinctive GitHub Pages website that deploys from the primary branch. The site's presentation should be shaped by what the document contains — not by a generic template.

## Phase 0: Read the Document

Read the document first. Never create files before understanding the content. Answer:

- Is this a single document or multi-chapter?
- Does it contain math ($...$, $$...$$, LaTeX)?
- Does it contain code blocks?
- Does it contain tables, diagrams, proofs?
- What is the tone — academic, technical, informal?

**Architecture decision:**

| Document type | Build |
|---|---|
| Single doc, <3 major sections | Single page, `default` layout |
| Single doc, many sections | Single page with sidebar nav, `chapter` layout |
| Multi-chapter book | Multi-page: landing + `chapters/` dir, prev/next nav |
| Collection of topics | Hub-and-spoke with topic cards |

## Phase 1: Core Files (Non-Negotiable)

### `_config.yml`
```yaml
title: [DOCUMENT TITLE]
description: [ONE SENTENCE]
baseurl: "/[REPO-NAME]"
url: "https://[USERNAME].github.io"
markdown: kramdown
highlighter: rouge
kramdown:
  input: GFM
  syntax_highlighter: rouge
plugins:
  - jekyll-sitemap
```

### `Gemfile`
```ruby
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
gem "webrick"
```

### `index.md`
Place the document at repo root as `index.md` with YAML frontmatter:
```yaml
---
layout: chapter       # or "default" for simple pages
title: "Title"
description: "One sentence"
math: true            # loads MathJax
search: true          # enables search
clipboard: true       # copy buttons on code
toc: true             # in-page table of contents
sidebar: true         # navigation sidebar
js: true              # interactive features
---
```
Do not alter the document body. Jekyll/kramdown processes it as-is.

## Phase 2: Layout

Create `_layouts/default.html` — the universal HTML shell. Must contain:

**`<head>`:**
- Meta charset, viewport
- Title, description (Open Graph + Twitter Card)
- Structured data (`ScholarlyArticle`)
- Fonts: Inter (body) + JetBrains Mono (code) via Google Fonts with `display=swap`
- Favicon as emoji SVG data URI
- Site stylesheet: `<link rel="stylesheet" href="{{ site.baseurl }}/assets/css/style.css">`
- Conditional MathJax: `{% if page.math %}` with inline config before the CDN script
- MathJax config: `inlineMath: [['$','$']]`, `displayMath: [['$$','$$']]`, `processEscapes: true`

**`<body>`:**
- Skip-to-content link (first focusable element)
- Progress bar (JS-driven width)
- Mobile top bar (hidden on desktop): menu + title + theme toggle
- Sidebar overlay (mobile dismissal)
- Flex container: sidebar + main content
- Floating action button (scroll-to-top, long-press theme toggle)
- `<noscript>` banner
- Theme init script (before first paint): read localStorage, set `data-theme`

Create `_layouts/chapter.html` for reading-optimized pages. Extends `default.html`. Contains:
- Hero with title, subtitle, author, date, reading time
- In-page TOC (between hero and content)
- Chapter navigation (prev/next if multi-page)
- `{{ content }}`

## Phase 3: Design System

### CSS Architecture
Use SCSS with CSS custom properties for theming. Minimum files:

- `assets/css/style.scss` — imports all partials (requires empty `---\n---\n` frontmatter)
- `_sass/_theme.scss` — all colors as CSS custom properties in `:root` and `[data-theme="dark"]`
- `_sass/_typography.scss` — heading scale, body text, code, blockquotes
- `_sass/_layout.scss` — `.app-container` flex, `.main-content` max-width ~780px
- `_sass/_sidebar.scss` — fixed left sidebar, mobile slide-out
- `_sass/_content.scss` — tables, TOC, spacing
- `_sass/_components.scss` — progress bar, FAB, copy buttons, search, proof blocks, etc.
- `_sass/_syntax.scss` — Rouge token highlighting (light + dark)
- `_sass/_responsive.scss` — tablet 1024px, phone 640px
- `_sass/_print.scss` — hide chrome, display content cleanly

### Design Principles
**Do not ship generic-looking sites.** The design should have character:

1. **Distinctive color palette** — not generic blue/slate. Use warm tones, rich accents, unique combinations. Every color references a CSS custom property — never hardcode hex values in components.
2. **Bold typography** — 800-weight headings, generous spacing, clear hierarchy. Use `clamp()` for responsive type.
3. **Thoughtful details** — accent underlines on h2, rounded tables, soft shadows, smooth transitions.
4. **Dark mode** — every color in `:root` must have a `[data-theme="dark"]` counterpart.
5. **Print** — clean single-column black-on-white. Hide all chrome.

### MathJax
- Config block BEFORE the CDN script tag
- `processEscapes: true` to handle `$p$-adic` style prose
- `ignoreHtmlClass: 'no-mathjax'` on code blocks
- CDN fallback: if MathJax fails to load in 5s, show raw LaTeX

### Syntax Highlighting
Jekyll + Rouge is built into GitHub Pages. Style both light and dark token maps:
```scss
.highlight {
  .c { color: #...; }  // comment
  .k { color: #...; }  // keyword
  .s { color: #...; }  // string
}
[data-theme="dark"] .highlight { ... }
```

## Phase 4: JavaScript

`assets/js/main.js` — single IIFE, no frameworks. Core features:

- **Theme**: read localStorage, fallback to `prefers-color-scheme`, apply before paint
- **Sidebar**: fetch `sidebar.json`, build nav tree, IntersectionObserver for active heading
- **Progress bar**: `requestAnimationFrame` scroll handler
- **Mobile**: toggle sidebar open/close
- **FAB**: short click = scroll to top, long press (>500ms) = toggle theme
- **Smooth scroll**: intercept hash links, `scrollTo({behavior:'smooth'})`
- **Copy buttons**: attach to `<pre><code>`, show "Copied!" for 2s
- **Reading time**: word count ÷ 200 WPM
- **Search**: fetch `search-data.json`, debounced input, keyboard navigation (Ctrl+K, ↑↓, Enter, Esc)

`assets/js/search.js` — standalone search module:
- Fetch `search-data.json`, build inverted index
- Debounce 300ms, return top 20 results
- Display: linked title + highlighted content snippet

## Phase 5: Data Files

Precompute navigation and search — never build them from DOM at runtime.

### `assets/js/nav/sidebar.json`
```json
[{ "id": "section-id", "title": "Title", "level": "h2", "children": [...] }]
```
One entry per h2/h3 in the document. `id` matches the HTML element ID.

### `assets/search/search-data.json`
```json
[{ "id": "id", "title": "Title", "content": "First 200 chars...", "url": "/#id", "level": "h2" }]
```

## Phase 6: SEO and Robustness

- `404.md` — friendly message + search + links to home
- `robots.txt` — full allow + sitemap URL
- `sitemap.xml` — auto-generated by `jekyll-sitemap` plugin
- Canonical URL in `<head>`
- OG image: create a 1200×630 SVG with the document title on a colored background. Place at `assets/img/og-image.svg`. Convert to PNG for production social cards.

## Phase 7: Deploy

```bash
git init && git add -A
git commit -m "Initial GitHub Pages site"
git remote add origin https://github.com/[USERNAME]/[REPO-NAME].git
git branch -M main && git push -u origin main
```

Then: **Settings → Pages → Deploy from branch → main → /root → Save**

---

## What Not To Do

- Don't fetch the raw Markdown at runtime. Jekyll builds it into HTML.
- Don't add `.nojekyll`. Let Jekyll process the site.
- Don't load client-side Markdown parsers (marked.js, showdown).
- Don't build navigation/search by traversing DOM. Precompute static JSON.
- Don't ship generic-looking designs. Make it distinctive.
- Don't hardcode colors in components. Use CSS custom properties.
- Don't skip dark mode. Every light color needs a dark counterpart.
- Don't skip print styles. Research documents are often printed.
- Don't forget the 404 page. Broken links happen.
- Don't over-engineer. 10 SCSS partials is enough. 14 JS features is enough.
