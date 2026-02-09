import json
import http.client
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("key")

conn = http.client.HTTPSConnection("scraperapi.thordata.com")
params = {
    "engine": "google_scholar",
    "q": "Andrew Ng",
    "json": "1",
    "start": "0"
}
payload = urlencode(params)
headers = {
    'Authorization': f'Bearer {KEY}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

conn.request("POST", "/request", payload, headers)
res = conn.getresponse()
raw = res.read().decode("utf-8")

print("Raw response:")
print(raw[:500])
print("\n" + "="*60 + "\n")

try:
    data = json.loads(raw)
    if isinstance(data, str):
        data = json.loads(data)
    
    print("Parsed JSON structure:")
    print(json.dumps(data, indent=2)[:2000])
except Exception as e:
    print(f"Error: {e}")
