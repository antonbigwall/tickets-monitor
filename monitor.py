import requests
import re

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://kids.stoyanie.ru/",
    "Origin": "https://kids.stoyanie.ru",
    "Accept": "application/json",
}
KEY = "e0dff602-86e5-46e2-92f5-c21c3b0b8f1d"
SID = "123102883"
API = f"https://mapi.afisha.ru/api/v21/sessions/{SID}"

print("=== Пробуем с X-Application-Key = widget-key ===")
r = requests.get(API, headers={**H, "X-Application-Key": KEY}, timeout=15)
print(f"{r.status_code}: {r.text[:1500]}")

print("\n=== Ищем ключ в app.js виджета ===")
js = requests.get("https://www.afisha.ru/w/app.b2ae2665d8454d5e2b3c.js", headers=H, timeout=20).text
print(f"app.js length: {len(js)}")

for kw in ["X-Application-Key", "application-key", "applicationKey", "appKey"]:
    for m in list(re.finditer(re.escape(kw), js, re.IGNORECASE))[:5]:
        print(f"\n[{kw}]")
        print(repr(js[max(0,m.start()-200):m.start()+300]))

print("\n=== UUID-подобные строки в app.js (первые 20) ===")
uuids = sorted(set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', js)))
for u in uuids[:20]:
    print(u)

print("\n=== Пробуем найденные UUID как ключ ===")
for u in uuids[:10]:
    try:
        r = requests.get(API, headers={**H, "X-Application-Key": u}, timeout=15)
        print(f"{u} -> {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"{u} -> ERR {e}")
