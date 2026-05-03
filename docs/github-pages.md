# System Instructions: Document → GitHub Pages Website

## Capability

Convert a user-provided written document into a GitHub Pages website whose presentation is shaped by what the document contains. The site must deploy from the primary branch and render at the standard project-site URL. These instructions are a **build checklist** — follow every phase, check every box, in order.

## Phase 0: Pre-Flight — Read the Document First

Do not create any files yet. Read the document and answer:

- [ ] Is this a single document or a multi-chapter book?
- [ ] Does it contain mathematical notation? ($...$, $$...$$, LaTeX)
- [ ] Does it contain text diagrams? (box-drawing characters: ┌ ┐ └ ┘ ├ ┤ │ ─)
- [ ] Does it contain code blocks? (fenced with ```)
- [ ] Does it contain tables?
- [ ] Does it define terminology used throughout?
- [ ] Does it contain proofs or step-by-step derivations?
- [ ] Does it cross-reference its own sections? ("see §4.2")
- [ ] Does it contain objections/dialogue? (argument and counter-argument)
- [ ] Does it list open problems or future work?
- [ ] Does the author permit analytics? (If not, note `no-tracking: true`)

**Architecture decision based on answers:**

| If... | Then build... |
|---|---|
| Single document, < 3 major sections | Single-page site (`index.md` → `default.html` layout) |
| Single document, > 3 major sections | Single-page site with in-page chapter navigation (`index.md` → `chapter.html` layout) |
| Multi-chapter book or collection | Multi-page site: landing page (`index.md` → `home.html`), chapters in `chapters/` directory (`chapter.html` layout), previous/next navigation |
| Collection of independent topics | Hub-and-spoke: landing page with topic cards, each linking to a dedicated page |

---

## Phase 1: Foundation — The Non-Negotiable Core

### 1.1 — `_config.yml`

Create at the repo root. Copy exactly, replacing bracketed placeholders:

```yaml
title: [DOCUMENT TITLE]
description: [ONE SENTENCE FROM ABSTRACT]
baseurl: "/[REPO-NAME]"
url: "https://[USERNAME].github.io"
markdown: kramdown
highlighter: rouge
kramdown:
  input: GFM
  syntax_highlighter: rouge
  footnote_backlink: "↩"
sass:
  style: compressed
plugins:
  - jekyll-sitemap
  - jekyll-redirect-from
defaults:
  - scope:
      path: ""
    values:
      layout: default
```

- [ ] `highlighter: rouge` + `syntax_highlighter: rouge` — built into GitHub Pages, zero config
- [ ] `footnote_backlink: "↩"` — returns reader from footnote to their place in the text
- [ ] `sass: style: compressed` — minifies CSS output
- [ ] `jekyll-sitemap` — auto-generates `sitemap.xml` for search engines
- [ ] `jekyll-redirect-from` — enables `redirect_from` frontmatter for moved pages
- [ ] `defaults` — every `.md` file gets `layout: default` without declaring it

### 1.2 — `Gemfile`

Create at the repo root:

```ruby
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
gem "webrick"
```

- [ ] `github-pages` gem — matches the GitHub Pages build environment exactly
- [ ] `webrick` — required for Ruby 3.x local development

### 1.3 — `_layouts/default.html`

The universal HTML shell. Every page uses this layout directly or extends it.

**`<head>` must contain (in this order):**

- [ ] `<meta charset="UTF-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- [ ] `<title>{{ page.title | default: site.title }}</title>`
- [ ] `<meta name="description">` — `{{ page.description | default: site.description }}`
- [ ] Open Graph: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`
- [ ] Twitter Card: `twitter:card`, `twitter:title`, `twitter:description`
- [ ] Structured data: `<script type="application/ld+json">` with `ScholarlyArticle` type (headline, author, datePublished, description, url, inLanguage)
- [ ] Canonical URL: `<link rel="canonical" href="{{ site.url }}{{ site.baseurl }}{{ page.url }}">`
- [ ] Favicon: emoji SVG data URI (`<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,...">`)
- [ ] Font preconnects: `<link rel="preconnect" href="https://fonts.googleapis.com">` and `fonts.gstatic.com` with `crossorigin`
- [ ] Font stylesheet: Inter (body) + JetBrains Mono (code)
- [ ] `font-display: swap` on the font stylesheet URL or in an inline `<style>` for the `@font-face`
- [ ] Site stylesheet: `<link rel="stylesheet" href="{{ site.baseurl }}/assets/css/style.scss">`
- [ ] Conditional KaTeX CSS: `{% if page.katex %}<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">{% endif %}`
- [ ] Conditional MathJax config + script: `{% if page.math %}` — inline config (BEFORE the CDN script), then `<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">`
- [ ] Conditional KaTeX autorender: `{% if page.katex %}<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js">`
- [ ] Conditional clipboard.js: `{% if page.clipboard %}<script src="https://cdn.jsdelivr.net/npm/clipboard@2.0.11/dist/clipboard.min.js">`
- [ ] Conditional Google Analytics: `{% if page.analytics and page.no-tracking != true %}{% include google-analytics.html %}{% endif %}`

**`<body>` must contain (in this order):**

- [ ] Skip-to-content link: `<a href="#main-content" class="skip-link">Skip to content</a>` — first focusable element
- [ ] Progress indicator: `<div class="progress-bar" id="progress-bar"></div>` — empty, JS fills width
- [ ] Mobile top bar (hidden on desktop): menu button, site title, theme toggle
- [ ] Sidebar overlay (hidden, for mobile dismissal)
- [ ] Flex container (`.app-container`):
  - [ ] **Sidebar** (fixed, dark background):
    - Branded header: site title + version badge
    - Search input: `<input type="text" placeholder="Search… (Ctrl+K)" id="search-input">`
    - Navigation container: `<nav id="sidebar-nav"></nav>` — populated by JS from `sidebar.json`
    - Footer links: repository, raw markdown, contact
  - [ ] **Main content** (scrollable, `.main-content`, `id="main-content"`):
    - Breadcrumbs include: `{% if page.chapter %}{% include breadcrumbs.html %}{% endif %}`
    - Hero banner: title, subtitle, metadata row (author, date, version), action buttons
    - Content: `{{ content }}`
    - Chapter navigation include (top): `{% if page.prev or page.next %}{% include chapter-nav.html position="top" %}{% endif %}`
    - Chapter navigation include (bottom): `{% if page.prev or page.next %}{% include chapter-nav.html position="bottom" %}{% endif %}`
    - Footer include: `{% include footer.html %}`
- [ ] Floating action button: `<div class="fab" id="fab">↑</div>` — scroll-to-top, long-press theme toggle
- [ ] Conditional site script: `{% if page.js %}<script src="{{ site.baseurl }}/assets/js/main.js"></script>{% endif %}`
- [ ] Conditional search script: `{% if page.search %}<script src="{{ site.baseurl }}/assets/js/search.js"></script>{% endif %}`

### 1.4 — `assets/css/style.scss`

Create this file with empty YAML frontmatter (required for Jekyll Sass compilation):

```scss
---
---
@import 'variables';
@import 'reset';
@import 'typography';
@import 'layout';
@import 'header';
@import 'sidebar';
@import 'content';
@import 'components';
@import 'syntax';
@import 'images';
@import 'theme';
@import 'responsive';
@import 'print';
```

Create the following partials in `_sass/`:

| Partial | Must Include |
|---|---|
| `_variables.scss` | Color tokens (light + dark-ready as CSS custom properties in `_theme.scss`), font stacks, spacing scale `$sp-xs` through `$sp-3xl`, breakpoints `$bp-tablet: 1024px` `$bp-phone: 640px`, shadow scale, transition speed |
| `_reset.scss` | `box-sizing: border-box`, `margin: 0; padding: 0`, `scroll-behavior: smooth`, `-webkit-font-smoothing: antialiased` |
| `_typography.scss` | Heading scale (h1–h4), body text, code, blockquotes, links, `scroll-margin-top: 80px` on all headings |
| `_layout.scss` | `.app-container` flex, `.main-content` offset, max-width ~860px |
| `_header.scss` | `.hero` gradient, title, subtitle, metadata, `.hero-cta` buttons |
| `_sidebar.scss` | Fixed position, dark background, search input, nav links with `.active` and `.read` states, `.nav-h1/.nav-h2/.nav-h3` indentation |
| `_content.scss` | Section spacing, tables (full-width, header accent, row striped, hover), blockquotes, vertical rhythm |
| `_components.scss` | Progress bar, callout boxes, key-takeaway cards, chapter abstract, diagram blocks, proof blocks, glossary tooltips, equation modal, search results overlay, chapter-nav buttons (`.chapter-nav` `.prev` `.next`), floating action button (`.fab`), back-to-top (`.back-to-top`), breadcrumbs (`.breadcrumbs`), reading time badge (`.reading-time`), fragment highlight (`:target` glow), skip-link, footnote popovers |
| `_syntax.scss` | Rouge token maps for light AND dark themes. Minimum: `.highlight` wrapper, `.c` (comment), `.k` (keyword), `.s` (string), `.n` (name), `.m` (number), `.o` (operator). Wrap dark tokens in `[data-theme="dark"] .highlight { ... }` |
| `_images.scss` | `max-width: 100%`, `height: auto`, lightbox overlay (`.lightbox` fixed fullscreen dark backdrop, `.lightbox-content` centered max-90vw max-90vh, close button), `img[loading="lazy"]` |
| `_theme.scss` | `:root` with all light CSS custom properties, `[data-theme="dark"]` with all dark overrides. EVERY color in every partial must reference a custom property from here — never hardcode a hex value in a component |
| `_responsive.scss` | Tablet `@media (max-width: $bp-tablet)`: sidebar slides off, main content fills, top bar visible. Phone `@media (max-width: $bp-phone)`: tighter spacing, smaller headings. |
| `_print.scss` | `@media print`: hide all chrome, display content single-column, black text on white, diagrams `white-space: pre-wrap`, proof bodies forced open |

### 1.5 — The Document as `index.md`

Place the user's document at the repo root as `index.md`. If the document already has YAML frontmatter, keep it and add `layout: default` plus any feature flags it needs:

```yaml
---
layout: default
title: [DOCUMENT TITLE]
description: [ONE SENTENCE]
math: true
search: true
clipboard: true
toc: true
sidebar: true
js: true
---
```

- [ ] `math: true` → MathJax loaded
- [ ] `search: true` → search.js loaded, search-data.json built
- [ ] `clipboard: true` → clipboard.js CDN loaded
- [ ] `toc: true` → in-page TOC rendered
- [ ] `sidebar: true` → sidebar component rendered
- [ ] `js: true` → main.js loaded
- [ ] If the author specifies no tracking: add `no-tracking: true`
- [ ] If analytics are desired: add `analytics: true` (must also include `google-analytics.html`)

Do not alter the document body. The body stays exactly as the user provided it — Jekyll and kramdown process it.

---

## Phase 2: Layouts, Includes, Components

### 2.1 — `_layouts/home.html`

For multi-page sites. Extends `default.html`. Contains:

- [ ] Hero section with document title, subtitle, metadata
- [ ] Brief introduction (first 2-3 paragraphs of the document, or custom content)
- [ ] Chapter/section grid: `{% for chapter in site.chapters %}` loop generating cards with title + description linking to `chapter.url`
- [ ] Call-to-action: "Start Reading → Chapter 1"

### 2.2 — `_layouts/chapter.html`

For individual chapter pages. Extends `default.html`. Contains:

- [ ] `{% include breadcrumbs.html %}` above the hero
- [ ] Chapter number + title in hero
- [ ] Reading time badge: `{% include reading-time.html %}`
- [ ] Previous/Next chapter navigation: `{% include chapter-nav.html position="top" %}`
- [ ] `{{ content }}`
- [ ] Previous/Next chapter navigation: `{% include chapter-nav.html position="bottom" %}`
- [ ] In-page TOC: `{% if page.toc %}{% include toc.html %}{% endif %}`

### 2.3 — `_includes/head.html`

- [ ] All `<meta>` tags, font preconnects, font stylesheet, site stylesheet link
- [ ] Conditional KaTeX CSS link
- [ ] Inline critical CSS for above-the-fold content (hero, loading state) — at minimum, set `body { visibility: hidden }` and reveal it with JS on load to prevent FOUC

### 2.4 — `_includes/sidebar.html`

- [ ] Branded header: emoji icon + site title + `<span class="version-badge">`
- [ ] Search input: `type="text"`, `id="search-input"`, `placeholder="Search… (Ctrl+K)"`, `aria-label="Search document"`
- [ ] Navigation: `<nav id="sidebar-nav"></nav>` — empty, populated by JS
- [ ] Footer: link to repository, link to raw markdown, link to author contact

### 2.5 — `_includes/footer.html`

- [ ] Copyright line with year and author
- [ ] ORCID link
- [ ] Repository link
- [ ] Signature tagline from the document's epilogue or closing

### 2.6 — `_includes/chapter-nav.html`

- [ ] Two buttons: `← Previous` and `Next →`
- [ ] Disabled state when at first/last chapter (`.chapter-nav .prev.disabled`, `.chapter-nav .next.disabled`)
- [ ] Reads `{{ page.prev }}` and `{{ page.next }}` from frontmatter
- [ ] Reads chapter titles from `chapter-nav.json`
- [ ] Rendered at both `position="top"` and `position="bottom"`

### 2.7 — `_includes/toc.html`

- [ ] In-page table of contents for the current page
- [ ] Built by JavaScript from the page's heading structure
- [ ] Each entry is an anchor link, indented by heading level
- [ ] Highlighted item tracks scroll position via IntersectionObserver

### 2.8 — `_includes/breadcrumbs.html`

- [ ] Horizontal breadcrumb trail: `Home → Chapter 3 → §3.2`
- [ ] Reads hierarchy from `chapter-nav.json`
- [ ] Each segment is a link (except the last, which is plain text)
- [ ] Uses `aria-label="Breadcrumb"` and structured data: `application/ld+json` `BreadcrumbList`

### 2.9 — `_includes/google-analytics.html`

- [ ] Google Analytics 4 tracking snippet
- [ ] Measurement ID inserted via `{{ site.google_analytics }}` or passed through `_config.yml`
- [ ] Wrapped in `{% if page.analytics and page.no-tracking != true %}` — respects opt-out
- [ ] If `_config.yml` has no measurement ID: include nothing, produce no console errors

### 2.10 — `_includes/reading-time.html`

- [ ] Displays estimated reading time for the current page
- [ ] Format: `<span class="reading-time">~X min read</span>`
- [ ] Computed by JavaScript: word count ÷ 200 WPM, minimum 1 minute
- [ ] Placed in the hero metadata row

---

## Phase 3: Data Files and Scripts

### 3.1 — `assets/js/nav/sidebar.json`

Precomputed navigation tree. Structure:

```json
[
  {
    "id": "section-id",
    "title": "Section Title",
    "level": "h2",
    "children": [
      { "id": "subsection-id", "title": "Subsection", "level": "h3" }
    ]
  }
]
```

- [ ] One entry per major heading (h2) in the document
- [ ] Each h2 may have `children` (h3 headings under it)
- [ ] `id` matches the `id` attribute of the corresponding HTML element

### 3.2 — `assets/js/nav/chapter-nav.json`

Chapter adjacency data:

```json
{
  "chapters": [
    { "id": "01-title", "title": "Chapter Title", "url": "/chapter-url/" }
  ]
}
```

- [ ] One entry per chapter in reading order
- [ ] `url` matches the chapter's `permalink`
- [ ] Used by `chapter-nav.html` to look up titles for previous/next buttons

### 3.3 — `assets/search/search-data.json`

Pre-built search index. Structure:

```json
[
  {
    "id": "section-id",
    "title": "Section Title",
    "content": "First 200 characters of body text, markup stripped...",
    "url": "/page-url/#section-id",
    "level": "h2"
  }
]
```

- [ ] One entry per section (h2 + h3) in the entire document
- [ ] `content` truncated to ~200 characters for snippet display
- [ ] `url` is the full path including hash fragment

### 3.4 — `assets/js/main.js`

Single file, immediately-invoked function expression. No frameworks. Features:

- [ ] **Theme**: Read `localStorage`, fallback `prefers-color-scheme`, set `data-theme` on `<html>`, call before first paint
- [ ] **Sidebar**: Fetch `sidebar.json`, build nav tree, insert into `#sidebar-nav`
- [ ] **Active heading**: IntersectionObserver — not scroll handler — tracks which heading is in view, applies `.active`
- [ ] **Progress bar**: `requestAnimationFrame` scroll handler, width = `scrollY / (totalHeight - viewportHeight) * 100`
- [ ] **Mobile menu**: Toggle sidebar `.open`, show/hide overlay, close on link click
- [ ] **Collapsible sections**: h2 headings — click toggles sibling content, ▸/▾ indicator
- [ ] **Floating action button**: Short click → scroll to top. Long press (>500ms) → toggle theme
- [ ] **Smooth scrolling**: Intercept hash links, `scrollTo({ behavior: 'smooth', top: targetTop - 80 })`
- [ ] **Fragment highlight**: On hash navigation, add `.highlight-target` class to target, remove after 2s
- [ ] **Copy buttons**: `clipboard.js` — attach to `<pre><code>`, show "Copied!" feedback, revert after 2s
- [ ] **Glossary tooltips**: Scan bold terms, match against glossary index, `title` attribute or hover popover
- [ ] **Proof collapsibility**: Detect `*Proof.*` → wrap in `.proof-block`, estimated reading time badge, toggle
- [ ] **Diagram zoom**: Click `.diagram` → toggle `.zoomed` (fullscreen overlay)
- [ ] **Equation modals**: Click display equations → isolate in centered modal with close button
- [ ] **Footnote popovers**: Click footnote reference → show content in popover; click again → close
- [ ] **Image lightbox**: Click images → open in fullscreen overlay with close button
- [ ] **Reading time**: Word count ÷ 200 WPM → update `.reading-time` elements
- [ ] **Section anchors**: Add `#` icon to each heading, click → copy URL to clipboard, show "✓" for 1.5s

- [ ] **Initialization order**: Theme → sidebar → search → mobile → collapse → back-to-top → FAB → smooth scroll → content-aware enhancements (deferred 500ms for DOM stability)

### 3.5 — `assets/js/search.js`

- [ ] Fetch `search-data.json` on first search activation (or on page load)
- [ ] Build in-memory index: tokenize, lowercase, remove punctuation
- [ ] Search input handler: debounce 300ms, query index, return top 20 results
- [ ] Results display: title (linked), content snippet with query terms highlighted, relevance indicator
- [ ] Keyboard: `Ctrl+K` → focus input, `↑/↓` → navigate results, `Enter` → go, `Escape` → close
- [ ] Click outside → close

### 3.6 — `_sass/_syntax.scss`

Rouge syntax highlighting tokens for both themes:

```scss
// Light
.highlight {
  background: $color-code-bg;
  .c { color: #6a737d; font-style: italic; }  // comment
  .k { color: #d73a49; font-weight: bold; }    // keyword
  .s { color: #032f62; }                       // string
  .n { color: #24292e; }                       // name
  .m { color: #005cc5; }                       // number
  .o { color: #d73a49; }                       // operator
}

// Dark
[data-theme="dark"] .highlight {
  .c { color: #8b949e; }
  .k { color: #ff7b72; }
  .s { color: #a5d6ff; }
  .n { color: #c9d1d9; }
  .m { color: #79c0ff; }
  .o { color: #ff7b72; }
}
```

- [ ] At minimum: comment, keyword, string, name, number, operator tokens
- [ ] Both light and dark token maps

---

## Phase 4: Multi-Page Architecture (if applicable) and SEO

### 4.1 — `chapters/` directory

For multi-chapter documents. Each chapter is a Markdown file:

```yaml
---
layout: chapter
title: "Chapter N: Title"
description: "One-line chapter summary"
permalink: /chapter-url/
prev: /previous-chapter-url/
next: /next-chapter-url/
math: true
toc: true
search: true
---
```

- [ ] `layout: chapter` — uses the reading-optimized chapter template
- [ ] `permalink` — clean URL for the chapter
- [ ] `prev` / `next` — adjacency for previous/next navigation buttons
- [ ] First chapter: `prev` is the homepage (`/`)
- [ ] Last chapter: `next` is absent or empty (buttons show disabled state)
- [ ] Appendices: optional `appendix: true` flag for distinct styling

### 4.2 — `404.md`

```yaml
---
layout: default
title: "Page Not Found"
permalink: /404.html
sitemap: false
---
```

- [ ] Friendly message: "The page you're looking for doesn't exist."
- [ ] Search box (so the reader can find what they need)
- [ ] Links to: homepage, chapter index, sitemap
- [ ] `sitemap: false` in frontmatter — don't index the 404 page

### 4.3 — `robots.txt`

```
User-agent: *
Allow: /
Sitemap: https://[USERNAME].github.io/[REPO-NAME]/sitemap.xml
```

- [ ] Full allow for all crawlers
- [ ] Sitemap URL matches the deployed location
- [ ] `jekyll-sitemap` plugin auto-generates `sitemap.xml` — no manual file needed

### 4.4 — Frontmatter Flags Reference

Every page supports these flags. The layout conditionally activates features:

| Flag | Effect |
|---|---|
| `layout: [default\|home\|chapter]` | Which template to use |
| `title: "..."` | Page title (browser tab + hero) |
| `description: "..."` | Meta description + Open Graph |
| `math: true` | Loads MathJax |
| `katex: true` | Loads KaTeX (faster, use INSTEAD of MathJax when possible) |
| `toc: true` | Renders in-page table of contents |
| `search: true` | Enables search feature |
| `sidebar: true` | Renders sidebar |
| `clipboard: true` | Loads clipboard.js for copy buttons |
| `js: true` | Loads main.js |
| `analytics: true` | Enables Google Analytics |
| `no-tracking: true` | DISABLES analytics (overrides `analytics: true`) |
| `sitemap: false` | Excludes page from sitemap |
| `permalink: /url/` | Custom URL for the page |
| `prev: /url/` | Previous chapter URL |
| `next: /url/` | Next chapter URL |
| `appendix: true` | Distinct styling for appendix pages |
| `redirect_from: /old-url/` | Redirects from old URL to this page |

---

## Phase 5: Validate Before Deploying

Run every check locally before pushing:

- [ ] `bundle exec jekyll serve` — site builds without errors
- [ ] Visit `http://localhost:4000/[repo-name]/` — page renders
- [ ] Math rendering: at least one `$...$` and one `$$...$$` renders correctly (no raw `\(` showing)
- [ ] Search: type 3+ characters, results appear
- [ ] Theme toggle: switches light ↔ dark, persists on refresh
- [ ] Mobile: resize to 400px wide, sidebar slides in/out, top bar visible
- [ ] Print: print preview shows content without chrome
- [ ] 404: visit `/nonexistent` → shows 404 page with search
- [ ] Sitemap: visit `/sitemap.xml` → valid XML with all page URLs
- [ ] Performance: Lighthouse audit → ≥ 90 Performance, ≥ 90 Accessibility, ≥ 90 SEO

**Performance targets:**
- [ ] Total page weight ≤ 200KB (HTML + CSS + JS + fonts)
- [ ] Largest Contentful Paint ≤ 2 seconds
- [ ] No render-blocking CSS (all stylesheets loaded with `<link>` or inlined critical CSS)
- [ ] All CDN scripts loaded with `async` or `defer`
- [ ] Images have `loading="lazy"` and explicit `width`/`height`
- [ ] Fonts use `font-display: swap`

---

## Phase 6: Deploy and Verify

```bash
cd [site-directory]
git init
git add -A
git commit -m "Initial GitHub Pages site"
git remote add origin https://github.com/[USERNAME]/[REPO-NAME].git
git branch -M main
git push -u origin main
```

Then:

- [ ] **Settings → Pages → Source: Deploy from a branch → Branch: main → /root → Save**
- [ ] Wait 1-2 minutes for build
- [ ] Visit the live URL — all Phase 5 checks pass on production
- [ ] Submit `sitemap.xml` URL to Google Search Console (optional)

---

## What Not to Do

- [ ] Do not `fetch()` the raw Markdown file from the browser at runtime. Jekyll builds it into the HTML.
- [ ] Do not embed the document as a base64-encoded blob. It is fragile, unmaintainable, and bloats the HTML.
- [ ] Do not add `.nojekyll`. Let Jekyll process the site.
- [ ] Do not load a client-side Markdown parser (marked.js, showdown, etc.). The browser receives HTML.
- [ ] Do not set `math_engine: mathjax` in `_config.yml`. It wraps math in backslash delimiters that Liquid mangles. Handle math in the layout template with MathJax or KaTeX config.
- [ ] Do not build navigation or search by traversing the DOM at runtime. Precompute the data as static JSON files.
- [ ] Do not scatter interactive controls across the page. Unify scroll-to-top, theme toggle, and menu into the floating action button.
- [ ] Do not ship one monolithic layout. At minimum, create `default.html` + `chapter.html`.
- [ ] Do not ignore SEO. Every page needs a unique `<title>`, `<meta name="description">`, canonical URL, and structured data.
- [ ] Do not load Google Analytics unconditionally. Respect `no-tracking: true` and `analytics: true` frontmatter flags.
- [ ] Do not skip the custom 404 page. Broken links happen — guide the reader back.
- [ ] Do not ship a site without a `Gemfile`. Local development requires `github-pages` gem and `webrick`.
