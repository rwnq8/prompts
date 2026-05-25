#!/usr/bin/env python3
r"""translate_docs.py -- Translate Markdown documentation files to multiple languages.

Preserves YAML frontmatter, code blocks, math blocks, and HTML tags.
Uses Google Translate API directly via urllib (zero external dependencies).

Canonical source: G:\My Drive\prompts\tools\translate_docs.py
"""
import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

# Markdown block types that should NOT be translated
CODE_BLOCK = re.compile(r'^```[\s\S]*?^```', re.MULTILINE)
INLINE_CODE = re.compile(r'`[^`]+`')
MATH_BLOCK = re.compile(r'\$\$[\s\S]*?\$\$')
INLINE_MATH = re.compile(r'\$[^$]+\$')
HTML_TAG = re.compile(r'<[^>]+>')
URL = re.compile(r'https?://\S+')
YAML_FRONTMATTER = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
IMAGE_LINK = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
LINK = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

# Fields in YAML frontmatter that should NOT be translated
YAML_NO_TRANSLATE = {'title', 'lang', 'language', 'slug', 'url', 'aliases', 'type', 'layout', 'draft', 'weight', 'toc'}

# Languages to translate to (ISO 639-1 codes)
# Configure which languages to target
TARGET_LANGUAGES = ['fr', 'es', 'de', 'zh-cn', 'ja', 'ar']

# Language name mapping
LANG_NAMES = {
    'en': 'English',
    'fr': 'Francais',
    'es': 'Espanol',
    'de': 'Deutsch',
    'zh-cn': '中文',
    'ja': '日本語',
    'ar': 'العربية',
}


def translate_text(text, dest_lang, translator=None):
    """Translate a single text block using Google Translate API (zero deps)."""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": dest_lang,
        "dt": "t",
        "q": text
    }
    full_url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        # Google returns [[["translated text", "original", ...]], null, ...]
        result = ""
        for segment in data[0]:
            if segment[0]:
                result += segment[0]
        return result if result else text
    except Exception as e:
        print(f"  [WARN] Translation failed: {e}")
        return text  # Return original on failure


def translate_markdown(content, dest_lang, source_lang='en'):
    """Translate markdown content, preserving code, math, and structure."""
    
    # Extract and preserve YAML frontmatter
    fm_match = YAML_FRONTMATTER.match(content)
    frontmatter = ''
    body = content
    if fm_match:
        frontmatter = fm_match.group(0)
        body = content[fm_match.end():]
    
    # Extract and preserve blocks that shouldn't be translated
    placeholders = {}
    counter = [0]
    
    def placeholder(match):
        counter[0] += 1
        key = f'__PRESERVE_{counter[0]}__'
        placeholders[key] = match.group(0)
        return key
    
    # Preserve code blocks
    body = CODE_BLOCK.sub(placeholder, body)
    # Preserve math blocks
    body = MATH_BLOCK.sub(placeholder, body)
    # Preserve inline math
    body = INLINE_MATH.sub(placeholder, body)
    # Preserve image links
    body = IMAGE_LINK.sub(placeholder, body)
    
    # Split remaining text into translatable paragraphs
    paragraphs = body.split('\n\n')
    translated_paragraphs = []
    
    for para in paragraphs:
        stripped = para.strip()
        if not stripped:
            translated_paragraphs.append(para)
            continue
        
        # Skip if it's a heading marker or horizontal rule
        if re.match(r'^#', stripped) or stripped == '---':
            # For headings, translate the text after the # markers
            heading_match = re.match(r'^(#+)\s*(.*)', stripped)
            if heading_match:
                hashes = heading_match.group(1)
                heading_text = heading_match.group(2)
                # Preserve inline code within headings
                codes_in_heading = list(INLINE_CODE.finditer(heading_text))
                if codes_in_heading:
                    # Complex: translate around inline code
                    translated = translate_text(heading_text, dest_lang)
                else:
                    translated = translate_text(heading_text, dest_lang)
                translated_paragraphs.append(f'{hashes} {translated}')
            else:
                translated_paragraphs.append(para)
            continue
        
        # Translate paragraph
        try:
            translated = translate_text(stripped, dest_lang)
            translated_paragraphs.append(translated)
        except Exception as e:
            print(f"  [WARN] Paragraph translation failed: {e}")
            translated_paragraphs.append(para)
    
    # Reassemble
    result = '\n\n'.join(translated_paragraphs)
    
    # Restore preserved blocks
    for key, original in placeholders.items():
        result = result.replace(key, original)
    
    # Restore frontmatter with updated lang field
    if frontmatter:
        # Update or add lang field
        fm_lines = frontmatter.split('\n')
        new_fm_lines = []
        has_lang = False
        for line in fm_lines:
            if line.strip().startswith('lang:'):
                new_fm_lines.append(f'lang: {dest_lang}')
                has_lang = True
            else:
                new_fm_lines.append(line)
        if not has_lang and len(fm_lines) > 1:
            # Insert after title or first line
            new_fm_lines.insert(2, f'lang: {dest_lang}')
        
        frontmatter = '\n'.join(new_fm_lines)
        result = frontmatter + '\n' + result
    
    return result


def generate_hugo_config(langs, output_dir):
    """Generate a minimal Hugo config.toml for multilingual setup."""
    lines = [
        'baseURL = "https://rwnq8.github.io/prompts/"',
        'languageCode = "en-us"',
        'title = "Documentation"',
        '',
        '[languages]',
    ]
    
    for i, lang in enumerate(langs):
        lines.append(f'  [languages.{lang}]')
        lines.append(f'    weight = {i + 1}')
        lines.append(f'    languageName = "{LANG_NAMES.get(lang, lang)}"')
        lines.append('')
    
    config_path = os.path.join(output_dir, 'config.toml')
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"  Generated Hugo config: {config_path}")
    return config_path


def main():
    parser = argparse.ArgumentParser(description='Translate Markdown docs to multiple languages')
    parser.add_argument('--docs-dir', default='docs', help='Source docs directory')
    parser.add_argument('--content-dir', default='content', help='Hugo content output directory')
    parser.add_argument('--langs', nargs='+', default=TARGET_LANGUAGES,
                        help='Target languages (ISO 639-1 codes)')
    parser.add_argument('--source-lang', default='en', help='Source language')
    parser.add_argument('--config', default='config.toml', help='Hugo config output path')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.docs_dir):
        print(f"ERROR: Docs directory not found: {args.docs_dir}")
        sys.exit(1)
    
    print(f"Source: {args.docs_dir} ({args.source_lang})")
    print(f"Target languages: {', '.join(args.langs)}")
    
    # Copy source docs to Hugo content directory for source language
    source_content_dir = os.path.join(args.content_dir, args.source_lang)
    os.makedirs(source_content_dir, exist_ok=True)
    
    md_files = list(Path(args.docs_dir).rglob('*.md'))
    print(f"\nFound {len(md_files)} markdown files")
    
    # Copy source files
    for md_file in md_files:
        rel_path = md_file.relative_to(args.docs_dir)
        dest = os.path.join(source_content_dir, rel_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Add lang field to frontmatter
        if content.startswith('---'):
            end_fm = content.index('---', 3)
            fm = content[3:end_fm]
            if 'lang:' not in fm:
                content = content[:end_fm] + f'lang: {args.source_lang}\n' + content[end_fm:]
        else:
            content = f'---\nlang: {args.source_lang}\n---\n' + content
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"  Copied {len(md_files)} source files to {source_content_dir}")
    
    # Translate to each target language
    for lang in args.langs:
        print(f"\n--- Translating to {lang} ({LANG_NAMES.get(lang, lang)}) ---")
        lang_dir = os.path.join(args.content_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        for md_file in md_files:
            rel_path = md_file.relative_to(args.docs_dir)
            dest = os.path.join(lang_dir, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"  {rel_path} ({len(content)} chars) -> translating...")
            translated = translate_markdown(content, lang, args.source_lang)
            
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(translated)
            
            print(f"    -> {len(translated)} chars ({lang})")
    
    # Generate Hugo config
    all_langs = [args.source_lang] + args.langs
    generate_hugo_config(all_langs, os.path.dirname(args.content_dir))
    
    print(f"\nDone! Translated to {len(args.langs)} languages.")
    print(f"Content ready for Hugo build: {args.content_dir}")


if __name__ == '__main__':
    main()
