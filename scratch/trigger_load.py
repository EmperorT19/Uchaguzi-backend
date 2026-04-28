import urllib.request
import urllib.error
import json

url = 'https://web-production-a0d6df.up.railway.app/system-admin/candidates/force-load'
data = json.dumps({'admin_key': 'IEBC2026'}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

print(f"Triggering force load at {url}...")
try:
    with urllib.request.urlopen(req, timeout=600) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Response Content:")
        print(json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Error occurred: {e}")
