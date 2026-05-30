"""
Batch-update all QNFO custom skills with:
- Version header
- Tools Required section
- Read-based loading note
"""
import os, re

skills_dir = r'G:\My Drive\prompts\skills'
read_note = """

## Tools Required

This skill is designed for use with QNFO agent tools. When loaded by a DEFAULT.md agent, the full tool suite (read, write, edit, exec, process, brave_web_search, YoBrowser, subagent_orchestrator) is available.

## QNFO Custom Skill Note

This is a QNFO custom skill deployed via `tools/deploy.py`. It is NOT accessible via `skill_view()` (which only indexes DeepChat's built-in registry). Load it with:

```
read('G:\\My Drive\\prompts\\skills\\{skill_name}\\SKILL.md')
```

"""

results = []
for skill_name in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, skill_name, 'SKILL.md')
    if not os.path.exists(skill_path):
        results.append(f"  [MISSING] {skill_name}: no SKILL.md")
        continue
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has version
    has_version = bool(re.search(r'(?:v|version[:\s]*)(\d+\.\d+)', content[:500]))
    
    # Check if already has tools section
    has_tools = 'Tools Required' in content or '## Tools' in content
    
    # Check if already has read-based loading note
    has_read_note = 'read(' in content and 'G:\\My Drive\\prompts\\skills' in content
    
    changes = []
    
    # 1. Add version header if missing
    if not has_version:
        # Extract existing title (first # line)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            # Replace the title line with versioned title
            new_title = f'# {title.strip()} (v1.0)'
            content = content.replace(title_match.group(0), new_title, 1)
            changes.append('version')
    
    # 2. Add Tools Required section if missing
    if not has_tools:
        # Insert after the first section (find second ## heading)
        sections = list(re.finditer(r'^## ', content, re.MULTILINE))
        if len(sections) >= 1:
            # Insert after the first ## section's content block
            # Find the double newline before the next ##
            insert_after = sections[0].end()
            next_section = content.find('\n## ', insert_after)
            if next_section == -1:
                next_section = content.find('\n---', insert_after)
            if next_section > 0:
                insert_pos = next_section
            else:
                insert_pos = insert_after
            
            tools_text = read_note.replace('{skill_name}', skill_name)
            content = content[:insert_pos] + '\n' + tools_text + '\n' + content[insert_pos:]
            changes.append('tools')
    
    # 3. Add read-based loading note if missing
    if not has_read_note:
        # Add at the end
        note = f"""

---

*{skill_name} v1.0 — QNFO custom skill. Load via read('G:\\\\My Drive\\\\prompts\\\\skills\\\\{skill_name}\\\\SKILL.md'). Not accessible via skill_view().*
"""
        content = content.rstrip() + note
        changes.append('read-note')
    
    # Write back
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    results.append(f"  [{'FIXED' if changes else 'OK'}] {skill_name}: {', '.join(changes) if changes else 'no changes needed'} ({len(content)} chars)")

print('\n'.join(results))
print(f'\n[DONE] {len(results)} skills processed')
