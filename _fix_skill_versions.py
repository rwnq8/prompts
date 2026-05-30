"""
Fix skill versioning: Add version field to YAML frontmatter
"""
import os, re

skills_dir = r'G:\My Drive\prompts\skills'

for skill_name in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, skill_name, 'SKILL.md')
    if not os.path.exists(skill_path):
        continue
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Only process frontmatter-based skills
    if not content.startswith('---'):
        # Has markdown title - check if versioned
        if not re.search(r'\(v\d+\.\d+\)', content[:200]):
            print(f'  [SKIP] {skill_name}: no frontmatter, no version pattern')
        continue
    
    # Check if version field already exists in frontmatter
    if re.search(r'^version:', content, re.MULTILINE):
        print(f'  [OK] {skill_name}: version field exists')
        continue
    
    # Find the end of frontmatter (second ---)
    fm_end = content.find('---', 3)
    if fm_end == -1:
        print(f'  [WARN] {skill_name}: could not find end of frontmatter')
        continue
    
    # Extract frontmatter
    frontmatter = content[3:fm_end].strip()
    
    # Add version field before the closing ---
    new_fm = '---\n' + frontmatter + '\nversion: 1.0\n---'
    new_content = new_fm + content[fm_end + 3:]
    
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'  [FIXED] {skill_name}: added version: 1.0 to frontmatter')

print('\n[DONE] Skill versioning fix complete')
