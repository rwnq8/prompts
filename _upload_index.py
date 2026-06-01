import json, urllib.request, ssl
ctx = ssl.create_default_context()

with open(r'G:\My Drive\prompts\_discovery_index.json', 'rb') as f:
    data = f.read()

token = open(r'C:\Users\LENOVO\.cloudflare\api-token').read().strip()
account_id = 'edb167b78c9fb901ea5bca3ce58ccc4b'
url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/r2/buckets/qnfo/objects/discovery/index.json'
req = urllib.request.Request(url, data=data, method='PUT')
req.add_header('Authorization', f'Bearer {token}')
req.add_header('Content-Type', 'application/json')

resp = urllib.request.urlopen(req, timeout=30, context=ctx)
result = json.loads(resp.read())
success = result['success']
size = result['result']['size']
print(f'R2 upload: success={success}, size={size} bytes')
