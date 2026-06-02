#!/usr/bin/env python3
"""
build_pdf.py — Markdown/HTML to PDF converter for QNFO publications.
Uses reportlab for PDF generation, markdown for MD→HTML conversion.
v1.0 — 2026-05-31

Usage:
  python build_pdf.py --input paper.md --output paper.pdf
  python build_pdf.py --input paper.html --output paper.pdf --title "Paper Title"
  python build_pdf.py --input paper.md --output paper.pdf --author "Rowan Quni-Gudzinas" --date "2026-05-31"
"""

import argparse
import re
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# --- PDF generation with reportlab ---
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import black, grey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.platypus.flowables import KeepTogether

# --- TTF Font Registration (for Unicode glyph coverage) ---
# Standard PDF Type 1 fonts (Helvetica, Courier) have limited Unicode support.
# We register system TTF fonts to guarantee proper rendering of curly quotes,
# em dashes, and other Unicode characters in PDF output.
FONT_MAPPING = {}  # style_name -> registered_font_name

def _discover_and_register_fonts():
    """Discover available TTF fonts and register with reportlab.
    
    Priority: Calibri (Windows) > DejaVu Sans (cross-platform) > Helvetica (fallback)
    Returns dict mapping style roles to registered font names.
    """
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os as _os
    
    registered = {}
    
    # Try Calibri (Windows - excellent Unicode coverage)
    calibri_paths = [
        r'C:\Windows\Fonts\calibri.ttf',
        r'C:\Windows\Fonts\calibrib.ttf',   # Bold
        r'C:\Windows\Fonts\calibrii.ttf',   # Italic
        r'C:\Windows\Fonts\calibriz.ttf',   # Bold-Italic
    ]
    
    if _os.path.exists(calibri_paths[0]):
        try:
            pdfmetrics.registerFont(TTFont('CalibriTTF', calibri_paths[0]))
            registered['sans'] = 'CalibriTTF'
            registered['sans_bold'] = 'CalibriTTF'  # reportlab will faux-bold
            registered['sans_italic'] = 'CalibriTTF'  # reportlab will faux-italic
            print(f"[FONTS] Registered Calibri TTF from {calibri_paths[0]}")
            return registered
        except Exception as e:
            print(f"[FONTS] Calibri registration failed: {e}")
    
    # Try DejaVu Sans (cross-platform, open-source)
    dejavu_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/TTF/DejaVuSans.ttf',
        '/System/Library/Fonts/DejaVuSans.ttf',
    ]
    for dp in dejavu_paths:
        if _os.path.exists(dp):
            try:
                pdfmetrics.registerFont(TTFont('DejaVuTTF', dp))
                registered['sans'] = 'DejaVuTTF'
                registered['sans_bold'] = 'DejaVuTTF'
                registered['sans_italic'] = 'DejaVuTTF'
                print(f"[FONTS] Registered DejaVu Sans TTF from {dp}")
                return registered
            except Exception as e:
                print(f"[FONTS] DejaVu registration failed: {e}")
    
    # Fallback: use standard PDF fonts (limited Unicode)
    print("[FONTS] No TTF fonts found. Using standard PDF fonts (limited Unicode support).")
    registered['sans'] = 'Helvetica'
    registered['sans_bold'] = 'Helvetica-Bold'
    registered['sans_italic'] = 'Helvetica-Oblique'
    return registered

# Register fonts at module load
FONT_MAPPING = _discover_and_register_fonts()

def _font(name):
    """Lookup registered font name or fallback to standard."""
    return FONT_MAPPING.get(name, name)

# --- Markdown to reportlab flowables ---
try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


def strip_html_tags(text):
    """Remove HTML tags, leaving plain text."""
    return re.sub(r'<[^>]+>', '', text)


def sanitize_unicode_escapes(text, source_label=""):
    """Detect and fix literal \\uXXXX escape sequences in text.
    
    These sequences appear when JSON-serialized content (with ensure_ascii=True)
    is rendered as plain text. They produce garbled output in PDFs.
    
    Returns: (sanitized_text, fix_count, report_lines)
    """
    import re as _re
    pattern = _re.compile(r'\\u[0-9a-fA-F]{4}')
    matches = pattern.findall(text)
    
    if not matches:
        return text, 0, []
    
    # Build replacement map
    from collections import Counter as _Counter
    fix_counts = _Counter()
    replacements = {}
    for m in set(matches):
        try:
            decoded = m.encode('ascii').decode('unicode_escape')
            replacements[m] = decoded
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    
    # Apply replacements
    fixed = text
    for escape_seq, real_char in replacements.items():
        count = fixed.count(escape_seq)
        fix_counts[escape_seq] = count
        fixed = fixed.replace(escape_seq, real_char)
    
    # Build report
    report = []
    label = f" [{source_label}]" if source_label else ""
    report.append(f"[UNICODE-FIX{label}] Found {len(matches)} literal Unicode escape sequences:")
    for seq, count in fix_counts.most_common():
        real = replacements.get(seq, '?')
        report.append(f"  {count:4d}x {seq} -> {real!r} (U+{ord(real):04X})")
    report.append(f"[UNICODE-FIX{label}] All sequences resolved. Sanitized text ready for PDF generation.")
    
    return fixed, len(matches), report


def md_to_plain_flowables(text, styles):
    """Parse markdown text into reportlab flowables (paragraphs, headings).
    
    Uses the markdown library for AST parsing if available,
    falls back to regex-based conversion.
    """
    flowables = []
    
    if HAS_MARKDOWN:
        # Use proper markdown parser
        md = md_lib.Markdown(extensions=['extra', 'codehilite', 'toc'])
        html = md.convert(text)
        # Strip unsupported attributes - reportlab Paragraph parser only supports
        # backColor, color, face, fontName, fontSize, name, size, style, textColor
        html = re.sub(r'\s+class="[^"]*"', '', html)
        html = re.sub(r'\s+id="[^"]*"', '', html)
        return html_to_flowables(html, styles)
    
    # Fallback: regex-based markdown parsing
    lines = text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    
    while i < len(lines):
        line = lines[i]
        
        # Code block toggle
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_lines)
                flowables.append(Paragraph(
                    f'<pre><font face="Courier" size="8">{code_text}</font></pre>',
                    styles['Code']
                ))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        stripped = line.strip()
        
        # Blank line
        if not stripped:
            flowables.append(Spacer(1, 6))
            i += 1
            continue
        
        # Headings
        if stripped.startswith('# '):
            flowables.append(Paragraph(strip_html_tags(stripped[2:]), styles['Heading1']))
        elif stripped.startswith('## '):
            flowables.append(Paragraph(strip_html_tags(stripped[3:]), styles['Heading2']))
        elif stripped.startswith('### '):
            flowables.append(Paragraph(strip_html_tags(stripped[4:]), styles['Heading3']))
        elif stripped.startswith('#### '):
            flowables.append(Paragraph(strip_html_tags(stripped[5:]), styles['Heading4']))
        # Horizontal rule
        elif stripped in ('---', '***', '___', '* * *'):
            flowables.append(HRFlowable(width="100%", thickness=0.5, color=grey))
        # Unordered list
        elif re.match(r'^[\*\-\+]\s', stripped):
            flowables.append(Paragraph(
                f'&bull; {_format_inline_markdown(stripped[2:])}',
                styles['BodyText']
            ))
        # Ordered list
        elif re.match(r'^\d+\.\s', stripped):
            num = re.match(r'^(\d+)\.', stripped).group(1)
            flowables.append(Paragraph(
                f'{num}. {_format_inline_markdown(stripped[stripped.index(". ")+2:])}',
                styles['BodyText']
            ))
        # Regular paragraph
        else:
            flowables.append(Paragraph(_format_inline_markdown(stripped), styles['BodyText']))
        
        i += 1
    
    return flowables


def _format_inline_markdown(text):
    """Convert inline markdown to HTML for reportlab Paragraph."""
    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    # Italic: *text* or _text_
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    # Inline code: `text`
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    # Links: [text](url)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" color="blue">\1</a>', text)
    return text


def html_to_flowables(html_text, styles):
    """Parse HTML into reportlab flowables (simplified)."""
    flowables = []
    
    # Split on block-level elements
    blocks = re.split(r'(</?h[1-4][^>]*>|</?p>|</?pre>|</?blockquote>|<hr\s*/?>)', html_text)
    
    current_tag = None
    buffer_text = ""
    
    for block in blocks:
        if re.match(r'<h([1-4])[^>]*>', block):
            current_tag = f'h{re.match(r"<h([1-4])[^>]*>", block).group(1)}'
            buffer_text = ""
        elif re.match(r'</h[1-4]>', block):
            if buffer_text.strip():
                style_key = f'Heading{current_tag[1]}'
                flowables.append(Paragraph(strip_html_tags(buffer_text), styles[style_key]))
            current_tag = None
            buffer_text = ""
        elif block == '<p>':
            current_tag = 'p'
            buffer_text = ""
        elif block == '</p>':
            if buffer_text.strip():
                flowables.append(Paragraph(buffer_text.strip(), styles['BodyText']))
            current_tag = None
            buffer_text = ""
        elif block == '<pre>':
            current_tag = 'pre'
            buffer_text = ""
        elif block == '</pre>':
            flowables.append(Paragraph(
                f'<font face="Courier" size="8">{buffer_text}</font>',
                styles['Code']
            ))
            current_tag = None
            buffer_text = ""
        elif re.match(r'<hr\s*/?>', block):
            flowables.append(HRFlowable(width="100%", thickness=0.5, color=grey))
        else:
            buffer_text += block
    
    # Any remaining text
    if buffer_text.strip():
        flowables.append(Paragraph(buffer_text.strip(), styles['BodyText']))
    
    return flowables


def build_styles():
    """Create publication-quality paragraph styles."""
    base = getSampleStyleSheet()
    
    styles = {
        'Title': ParagraphStyle(
            'CustomTitle', parent=base['Title'],
            fontName=_font('sans_bold'), fontSize=20, leading=26,
            spaceAfter=6, alignment=TA_CENTER
        ),
        'Author': ParagraphStyle(
            'Author', parent=base['Normal'],
            fontName=_font('sans'), fontSize=12, leading=16,
            spaceAfter=24, alignment=TA_CENTER, textColor=grey
        ),
        'Heading1': ParagraphStyle(
            'CustomH1', parent=base['Heading1'],
            fontName=_font('sans_bold'), fontSize=16, leading=22,
            spaceBefore=18, spaceAfter=8
        ),
        'Heading2': ParagraphStyle(
            'CustomH2', parent=base['Heading2'],
            fontName=_font('sans_bold'), fontSize=14, leading=19,
            spaceBefore=14, spaceAfter=6
        ),
        'Heading3': ParagraphStyle(
            'CustomH3', parent=base['Heading3'],
            fontName=_font('sans_italic'), fontSize=12, leading=16,
            spaceBefore=10, spaceAfter=4
        ),
        'Heading4': ParagraphStyle(
            'CustomH4', parent=base['Heading4'],
            fontName=_font('sans_italic'), fontSize=11, leading=14,
            spaceBefore=8, spaceAfter=3
        ),
        'BodyText': ParagraphStyle(
            'CustomBody', parent=base['BodyText'],
            fontName=_font('sans'), fontSize=10, leading=15,
            spaceBefore=2, spaceAfter=8, alignment=TA_JUSTIFY
        ),
        'Code': ParagraphStyle(
            'CodeBlock', parent=base['Code'],
            fontName='Courier', fontSize=8, leading=10,
            leftIndent=12, rightIndent=12, spaceBefore=6, spaceAfter=6,
            backColor='#f5f5f5'
        ),
        'Bullet': ParagraphStyle(
            'BulletItem', parent=base['BodyText'],
            fontName=_font('sans'), fontSize=10, leading=15,
            leftIndent=20, bulletIndent=10, spaceBefore=1, spaceAfter=4
        ),
    }
    return styles


def add_page_number(canvas, doc):
    """Add page number to footer."""
    canvas.saveState()
    canvas.setFont(_font('sans'), 8)
    canvas.setFillColor(grey)
    canvas.drawCentredString(A4[0] / 2.0, 0.75 * cm, f"— {canvas.getPageNumber()} —")
    canvas.restoreState()


def add_header_footer(canvas, doc):
    """Add header line and page number."""
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(grey)
    canvas.setLineWidth(0.3)
    canvas.line(2 * cm, A4[1] - 1.5 * cm, A4[0] - 2 * cm, A4[1] - 1.5 * cm)
    # Footer
    canvas.setFont(_font('sans'), 8)
    canvas.setFillColor(grey)
    canvas.drawCentredString(A4[0] / 2.0, 1 * cm, f"— {canvas.getPageNumber()} —")
    canvas.restoreState()


def build_pdf(input_path, output_path, title=None, author=None, date_str=None):
    """Main PDF builder. Converts input .md or .html to PDF."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)
    
    text = input_path.read_text(encoding='utf-8')
    
    # --- Unicode escape sequence sanitization (QC check) ---
    text, fix_count, fix_report = sanitize_unicode_escapes(text, source_label=input_path.name)
    if fix_count > 0:
        for line in fix_report:
            print(f"  {line}", file=sys.stderr)
        print(f"  [UNICODE-FIX] Auto-corrected {fix_count} escape sequences in source. "
              f"Regenerate the source file to prevent this warning in future builds.",
              file=sys.stderr)
    
    styles = build_styles()
    
    # Build flowables list
    flowables = []
    
    # Title page
    if title:
        flowables.append(Spacer(1, 2 * inch))
        flowables.append(Paragraph(title, styles['Title']))
        if author or date_str:
            author_line = []
            if author:
                author_line.append(author)
            if date_str:
                author_line.append(date_str)
            flowables.append(Paragraph(' | '.join(author_line), styles['Author']))
        flowables.append(Spacer(1, 0.5 * inch))
        flowables.append(HRFlowable(width="60%", thickness=1, color=black))
        flowables.append(Spacer(1, 0.3 * inch))
        flowables.append(Paragraph(
            '<i>License: CC BY 4.0 • Published via QNFO Research Infrastructure</i>',
            ParagraphStyle('LicenseNote', parent=styles['BodyText'],
                          fontSize=9, alignment=TA_CENTER, textColor=grey)
        ))
        flowables.append(PageBreak())
    
    # Parse and append content
    suffix = input_path.suffix.lower()
    if suffix == '.md':
        content_flowables = md_to_plain_flowables(text, styles)
    elif suffix in ('.html', '.htm'):
        content_flowables = html_to_flowables(text, styles)
    else:
        # Treat as plain text
        for para in text.split('\n\n'):
            if para.strip():
                content_flowables.append(Paragraph(para.strip(), styles['BodyText']))
    
    flowables.extend(content_flowables)
    
    # Build the PDF
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=title or input_path.stem,
        author=author or 'QNFO Research',
    )
    
    doc.build(flowables, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"[OK] PDF built: {output_path} ({output_path.stat().st_size:,} bytes, {doc.page} pages)")


def main():
    parser = argparse.ArgumentParser(description="Build PDF from Markdown or HTML")
    parser.add_argument('--input', '-i', required=True, help='Input file (.md or .html)')
    parser.add_argument('--output', '-o', help='Output PDF file path')
    parser.add_argument('--title', '-t', help='Publication title (auto-detected from first H1 if omitted)')
    parser.add_argument('--author', '-a', help='Author name')
    parser.add_argument('--date', '-d', help='Publication date (YYYY-MM-DD, defaults to today)')
    parser.add_argument('--check-unicode', action='store_true',
                        help='Scan input for literal \\uXXXX escape sequences and report (no PDF build)')
    parser.add_argument('--fix-unicode', action='store_true',
                        help='Auto-correct \\uXXXX sequences in the source file IN PLACE')
    args = parser.parse_args()

    input_path = Path(args.input)

    # --- Unicode pre-flight check ---
    if args.check_unicode:
        if not input_path.exists():
            print(f"[ERROR] Input file not found: {input_path}")
            sys.exit(1)
        text = input_path.read_text(encoding='utf-8')
        _, fix_count, fix_report = sanitize_unicode_escapes(text, source_label=input_path.name)
        if fix_count > 0:
            for line in fix_report:
                print(line)
            print(f"\n[RESULT] {fix_count} escape sequences found in source file.")
            print("[ACTION] Run with --fix-unicode to auto-correct the source file, or rebuild the source.")
            sys.exit(1)
        else:
            print(f"[OK] No Unicode escape sequences found in {input_path.name}")
            sys.exit(0)

    # --- Unicode fix-in-place ---
    if args.fix_unicode:
        if not input_path.exists():
            print(f"[ERROR] Input file not found: {input_path}")
            sys.exit(1)
        text = input_path.read_text(encoding='utf-8')
        fixed, fix_count, fix_report = sanitize_unicode_escapes(text, source_label=input_path.name)
        if fix_count > 0:
            input_path.write_text(fixed, encoding='utf-8')
            for line in fix_report:
                print(line)
            print(f"[FIXED] {fix_count} escape sequences corrected in {input_path.name}")
        else:
            print(f"[OK] No Unicode escape sequences found in {input_path.name}")
        sys.exit(0)

    # Auto-detect title from first H1 in markdown
    title = args.title
    if not title:
        try:
            text = input_path.read_text(encoding='utf-8')
            # Sanitize before extraction (in case title itself has escapes)
            text, _, _ = sanitize_unicode_escapes(text, source_label=input_path.name)
            m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
            if m:
                title = m.group(1).strip()
        except Exception:
            pass
    
    
    # Validate --output is provided for PDF builds
    if not args.output:
        print("[ERROR] --output/-o is required for PDF generation")
        sys.exit(1)
    date_str = args.date or datetime.now().strftime('%Y-%m-%d')
    
    build_pdf(args.input, args.output, title=title, author=args.author, date_str=date_str)


if __name__ == '__main__':
    main()
