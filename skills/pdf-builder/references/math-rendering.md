# Math Rendering Reference — pdf-builder v1.0

## Rendering Engine

`build_pdf.py` uses **matplotlib mathtext** for math rendering. Mathtext is not full LaTeX —
it supports a subset of LaTeX math commands. This document catalogs known limitations
and provides troubleshooting guidance.

---

## Supported LaTeX Commands

### Greek Letters

| LaTeX | Rendered | LaTeX | Rendered |
|:------|:---------|:------|:---------|
| `\alpha` | α | `\beta` | β |
| `\gamma` | γ | `\delta` | δ |
| `\epsilon` | ε | `\varepsilon` | ε |
| `\zeta` | ζ | `\eta` | η |
| `\theta` | θ | `\vartheta` | ϑ |
| `\iota` | ι | `\kappa` | κ |
| `\lambda` | λ | `\mu` | μ |
| `\nu` | ν | `\xi` | ξ |
| `\pi` | π | `\varpi` | ϖ |
| `\rho` | ρ | `\varrho` | ϱ |
| `\sigma` | σ | `\varsigma` | ς |
| `\tau` | τ | `\upsilon` | υ |
| `\phi` | φ | `\varphi` | φ |
| `\chi` | χ | `\psi` | ψ |
| `\omega` | ω | | |
| `\Gamma` | Γ | `\Delta` | Δ |
| `\Theta` | Θ | `\Lambda` | Λ |
| `\Xi` | Ξ | `\Pi` | Π |
| `\Sigma` | Σ | `\Upsilon` | Υ |
| `\Phi` | Φ | `\Psi` | Ψ |
| `\Omega` | Ω | | |

### Operators

`\times` (×), `\cdot` (·), `\pm` (±), `\mp` (∓), `\div` (÷),
`\ast` (∗), `\star` (⋆), `\circ` (∘), `\bullet` (•),
`\oplus` (⊕), `\ominus` (⊖), `\otimes` (⊗), `\odot` (⊙)

### Relations

`\leq` (≤), `\geq` (≥), `\neq` (≠), `\approx` (≈), `\equiv` (≡),
`\sim` (∼), `\simeq` (≃), `\propto` (∝), `\ll` (≪), `\gg` (≫)

### Arrows

`\to` / `\rightarrow` (→), `\Rightarrow` (⇒),
`\leftarrow` (←), `\Leftarrow` (⇐),
`\leftrightarrow` (↔), `\mapsto` (↦)

### Sets and Symbols

`\infty` (∞), `\partial` (∂), `\nabla` (∇), `\emptyset` (∅),
`\in` (∈), `\notin` (∉), `\subset` (⊂), `\subseteq` (⊆),
`\cup` (∪), `\cap` (∩)

### Quantifiers

`\forall` (∀), `\exists` (∃)

### Special

`\hbar` (ħ), `\ell` (ℓ), `\Re` (ℜ), `\Im` (ℑ),
`\int` (∫), `\sum` (∑), `\prod` (∏),
`\dots` / `\ldots` (…), `\cdots` (⋯)

### Blackboard Bold

`\mathbb{N}` (ℕ), `\mathbb{Z}` (ℤ), `\mathbb{Q}` (ℚ),
`\mathbb{R}` (ℝ), `\mathbb{C}` (ℂ), `\mathbb{H}` (ℍ)

### Accents

`\hat{x}` (x̂), `\bar{x}` (x̄), `\tilde{x}` (x̃),
`\vec{x}` (x⃗), `\dot{x}` (ẋ), `\ddot{x}` (ẍ)

### Fractions, Roots, Subscripts, Superscripts

`\frac{a}{b}`, `\sqrt{x}`, `\sqrt[n]{x}`, `x^2`, `x_n`, `x_i^j`

---

## Known Limitations

### Not Supported by Mathtext

| Feature | Alternative |
|:--------|:------------|
| `\begin{align}...\end{align}` | Use separate `$$...$$` blocks per line |
| `\begin{cases}...\end{cases}` | Use `\left\{ \begin{array}...` (mathtext syntax) |
| `\begin{matrix}...\end{matrix}` | Use `\begin{array}...` instead |
| `\text{...}` inside math | Works in mathtext with `\mathrm{...}` |
| `\bm{...}` (bold math) | Not supported — use `\mathbf{...}` |
| `\mathcal{...}` | Limited mathtext support |
| `\mathscr{...}` | Not supported |
| `\tag{...}` (equation numbers) | Add manually after the equation |
| `\label{...}` / `\ref{...}` | Not supported |
| `\ce{...}` (chemical) | Not supported |
| `\si{...}` (SI units) | Not supported |

### Rendering Edge Cases

1. **Very long expressions** (>200 chars): Mathtext may render with incorrect line breaks.
   Split into multiple display math blocks.

2. **Nested fractions**: Deep nesting (>3 levels) produces tiny text. Restructure.

3. **Special characters**: `%`, `#`, `&`, `_` inside math must be escaped with `\`.

4. **Unicode in math**: Mathtext is ASCII-based. Use LaTeX commands, not Unicode characters.

5. **Inline math height**: Expressions taller than ~14pt are scaled down to fit inline.
   This may make complex inline expressions hard to read. Consider moving to display math.

---

## --no-math Unicode Fallback

When `--no-math` is used, LaTeX commands are converted to Unicode characters using
a static mapping table. This is a lossy conversion:

### Works Well

- Greek letters: `\alpha` → α, `\Gamma` → Γ
- Simple operators: `\times` → ×, `\pm` → ±
- Common symbols: `\infty` → ∞, `\hbar` → ħ
- Relations: `\leq` → ≤, `\approx` → ≈

### Works Poorly

- Fractions: `\frac{a}{b}` → `a/b` (loss of vertical layout)
- Sums/Integrals: `\sum_{n=1}^\infty` → `Σ_{n=1}^∞` (subscript/superscript positioning lost)
- Accents: `\hat{H}` → `Ĥ` (if available) or `Ĥ` (combining character, may not render)
- Multi-character subscripts: `x_{ij}` → `x_{ij}` (no subscript rendering)

### Not Converted

- `\begin`/`\end` environments → shown as raw text
- `\left`/`\right` delimiters → shown as raw text
- `\mathcal`, `\mathbf`, `\mathit` → shown as raw text

---

## Troubleshooting

### "Could not render: ..." in output

Mathtext encountered invalid LaTeX. Check:
- Unescaped special characters (`%`, `#`, `&`)
- Unmatched braces `{...}`
- Unsupported environments (`\begin{align}`, etc.)
- Missing `\right` for a `\left`

### Math images appear but are too small/large

Mathtext auto-sizes to the expression. For fine control:
- Inline math: font_size=10, images capped at 14pt height (source: `_make_math_inline_flowables()`)
- Display math: font_size=12, no height cap

### PDF has Unicode replacement characters (�)

Font encoding issue with non-ASCII characters. Run font check:
```bash
python "G:\My Drive\prompts\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf
```
The script registers Calibri TTF → DejaVu Sans → Helvetica (fallback).
If all three fail, Unicode support is limited.

### Math renders but surrounding text is fragmented

This is expected behavior. Inline math uses 1-row Tables to embed images alongside text.
PDF text extraction shows words on separate lines because each cell is extracted independently.
The visual output is correct — this is a text extraction artifact, not a rendering bug.

---

## Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| v1.1 | 2026-06-03 | Math rendering via matplotlib mathtext (inline + display). --no-math flag with Unicode fallback. 28 expressions tested. |
| v1.0 | 2026-05-31 | Initial release. Markdown→PDF via reportlab. No math rendering. |

---

*math-rendering.md v1.0 — Reference for pdf-builder skill*
