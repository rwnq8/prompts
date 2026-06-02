import re, json

# FIX 1: Check DEFINITION-OF-DONE.md
with open(r'G:\My Drive\prompts\templates\DEFINITION-OF-DONE.md', 'r', encoding='utf-8') as f:
    content = f.read()
refs = re.findall(r'fill_prompt_template\("([^"]+)"', content)
print('DEFINITION-OF-DONE.md refs:', refs)
for ref in refs:
    tmpl_path = f'G:\\My Drive\\prompts\\templates\\{ref}.md'
    import os
    if os.path.exists(tmpl_path):
        print(f'  {ref}: EXISTS')
    else:
        print(f'  {ref}: MISSING')

# FIX 2: Check KAIZEN-AUTONOMOUS-UPDATE.md
with open(r'G:\My Drive\prompts\templates\KAIZEN-AUTONOMOUS-UPDATE.md', 'r', encoding='utf-8') as f:
    content = f.read()
refs = re.findall(r'fill_prompt_template\("([^"]+)"', content)
print('\nKAIZEN-AUTONOMOUS-UPDATE.md refs:', refs)

# FIX 3: Check email-composer SKILL.md
with open(r'G:\My Drive\prompts\skills\email-composer\SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()
refs = re.findall(r'fill_prompt_template\("([^"]+)"', content)
print('\nemail-composer SKILL.md refs:', refs)
for ref in refs:
    tmpl_path = f'G:\\My Drive\\prompts\\templates\\{ref}.md'
    if os.path.exists(tmpl_path):
        print(f'  {ref}: EXISTS')
    else:
        print(f'  {ref}: MISSING')

# FIX 4: Check app-settings.json
with open(r'G:\My Drive\prompts\app-settings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)
deployed_len = len(settings.get('default_system_prompt', ''))
with open(r'G:\My Drive\prompts\DEFAULT.md', 'r', encoding='utf-8') as f:
    canonical = f.read()
print(f'\napp-settings.json: {deployed_len} chars')
print(f'DEFAULT.md: {len(canonical)} chars')
print(f'STALE: {deployed_len != len(canonical)}')
