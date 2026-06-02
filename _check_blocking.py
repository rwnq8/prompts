import json
with open(r'G:\My Drive\prompts\_audit_report.json', 'r', encoding='utf-8') as f:
    r = json.load(f)
print('BLOCKING:', r['blocking'])
print('WARNINGS:', r['warnings'])
print('PASSES:', r['passes'])
print()
for i in r['issues']:
    if i['severity'] == 'BLOCKING':
        print('  BLOCKING [{}]: {}'.format(i['category'], i['detail']))
