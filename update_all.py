import json

# PowerShell restriction block to add to each prompt
ps_restriction = """## 0. PERSISTENT PREFERENCES

1. **Git:** Use git for all projects individually to track/annotate changes and allow undo of agent operations.
2. **MathJax:** Format ALL variable names and math expressions as MathJax (e.g., $E = mc^2$).
3. **PowerShell Text Corruption:**
   - PowerShell FREQUENTLY mangles multiline Python code, regex patterns, and Unicode/UTF-8 strings when executing inline via `python -c`.
   - **NEVER execute Python inline via PowerShell.** Always write Python to a `.py` file first, then execute the file.
   - **NEVER use PowerShell for text processing** (sed, grep, regex, string replacement). Use Python scripts instead.
   - PowerShell's handling of double quotes in nested strings causes `SyntaxError: unterminated string literal` errors.
   - PowerShell's default encoding (cp1252) corrupts characters like em-dash, smart quotes, and non-Latin scripts (e.g., Chinese characters in MCP server descriptions).
   - **Python encoding:** Always use `encoding='utf-8'` in `open()`. Add `sys.stdout.reconfigure(encoding='utf-8')` for scripts that output Unicode.
4. **Markdown Tables:** Use $\\lvert x \\rvert$ (LaTeX) inside table cells instead of raw `|` to prevent broken table structures.
5. **Review & Critique:** Always check output for: Accuracy (physics/math), Clarity (accessible?), Completeness (what's missing?), Structure and flow.

---

"""

# Read current files
default_content = open(r'G:\My Drive\prompts\DEFAULT.md', 'r', encoding='utf-8').read()
meta_content = open(r'G:\My Drive\prompts\META-PROMPT-DEEPSEEK.md', 'r', encoding='utf-8').read()
s1 = open(r'G:\My Drive\prompts\scholar\STAGE-1-SETUP.md', 'r', encoding='utf-8').read()
s2 = open(r'G:\My Drive\prompts\scholar\STAGE-2-DRAFT.md', 'r', encoding='utf-8').read()
s3 = open(r'G:\My Drive\prompts\scholar\STAGE-3-REVIEW.md', 'r', encoding='utf-8').read()
s4 = open(r'G:\My Drive\prompts\scholar\STAGE-4-PUBLISH.md', 'r', encoding='utf-8').read()

def inject_ps_restriction(content):
    """Add PowerShell restriction after the codename line but before Section 1."""
    lines = content.split('\n')
    # Find the Constitutional Mandates section
    for i, line in enumerate(lines):
        if 'CONSTITUTIONAL MANDATES' in line:
            # Insert ps_restriction before this line
            return '\n'.join(lines[:i]) + '\n' + ps_restriction + '\n'.join(lines[i:])
    # If not found, insert after codename
    for i, line in enumerate(lines):
        if line.startswith('CODENAME:'):
            return '\n'.join(lines[:i+1]) + '\n\n' + ps_restriction + '\n'.join(lines[i+1:])
    return ps_restriction + content

# Update files
for filepath, content, name in [
    (r'G:\My Drive\prompts\DEFAULT.md', default_content, 'DEFAULT.md'),
    (r'G:\My Drive\prompts\META-PROMPT-DEEPSEEK.md', meta_content, 'META-PROMPT-DEEPSEEK.md'),
    (r'G:\My Drive\prompts\scholar\STAGE-1-SETUP.md', s1, 'STAGE-1-SETUP.md'),
    (r'G:\My Drive\prompts\scholar\STAGE-2-DRAFT.md', s2, 'STAGE-2-DRAFT.md'),
    (r'G:\My Drive\prompts\scholar\STAGE-3-REVIEW.md', s3, 'STAGE-3-REVIEW.md'),
    (r'G:\My Drive\prompts\scholar\STAGE-4-PUBLISH.md', s4, 'STAGE-4-PUBLISH.md'),
]:
    if 'PowerShell' in content and 'NEVER execute Python inline' in content:
        print(f'{name}: Already has PowerShell restriction')
        updated = content
    else:
        updated = inject_ps_restriction(content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f'{name}: PowerShell restriction added ({len(updated)} chars)')

# Re-read updated content for registries
default_content = open(r'G:\My Drive\prompts\DEFAULT.md', 'r', encoding='utf-8').read()
meta_content = open(r'G:\My Drive\prompts\META-PROMPT-DEEPSEEK.md', 'r', encoding='utf-8').read()
s1 = open(r'G:\My Drive\prompts\scholar\STAGE-1-SETUP.md', 'r', encoding='utf-8').read()
s2 = open(r'G:\My Drive\prompts\scholar\STAGE-2-DRAFT.md', 'r', encoding='utf-8').read()
s3 = open(r'G:\My Drive\prompts\scholar\STAGE-3-REVIEW.md', 'r', encoding='utf-8').read()
s4 = open(r'G:\My Drive\prompts\scholar\STAGE-4-PUBLISH.md', 'r', encoding='utf-8').read()

# Sync registries
print()

# system_prompts.json
spp = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\system_prompts.json'
with open(spp, 'r', encoding='utf-8') as f:
    sp = json.load(f)
for p in sp['prompts']:
    if 'DEFAULT' in p.get('name', ''):
        p['content'] = default_content
    elif 'META-PROMPT' in p.get('name', ''):
        p['content'] = meta_content
with open(spp, 'w', encoding='utf-8') as f:
    json.dump(sp, f, ensure_ascii=False, indent=2)
print(f'system_prompts.json: {len(sp["prompts"])} entries synced')

# custom_prompts.json
cpp = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\custom_prompts.json'
with open(cpp, 'r', encoding='utf-8') as f:
    cp = json.load(f)
for p in cp['prompts']:
    n = p.get('name', '')
    if 'DEFAULT' in n:
        p['content'] = default_content
    elif 'META-PROMPT' in n:
        p['content'] = meta_content
    elif 'STAGE 1' in n:
        p['content'] = s1
    elif 'STAGE 2' in n:
        p['content'] = s2
    elif 'STAGE 3' in n:
        p['content'] = s3
    elif 'STAGE 4' in n:
        p['content'] = s4
with open(cpp, 'w', encoding='utf-8') as f:
    json.dump(cp, f, ensure_ascii=False, indent=2)
print(f'custom_prompts.json: {len(cp["prompts"])} templates synced')

# app-settings.json
asp = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json'
with open(asp, 'r', encoding='utf-8') as f:
    app = json.load(f)
app['default_system_prompt'] = default_content
with open(asp, 'w', encoding='utf-8') as f:
    json.dump(app, f, ensure_ascii=False, indent=2)
print(f'app-settings.json: default -> DEFAULT.md ({len(default_content)} chars)')

print('\nAll updates applied and registries synced.')
