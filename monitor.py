import requests
import re

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://kids.stoyanie.ru/",
    "Accept": "application/json",
    "X-Application-Key": "e0dff602-86e5-46e2-92f5-c21c3b0b8f1d",
}
SID = "123102883"
BASE = "https://mapi.afisha.ru/api/v21"

print("=== Пробуем кандидатов ===")
for u in [
    f"{BASE}/sessions/{SID}/hall",
    f"{BASE}/sessions/{SID}/halls",
    f"{BASE}/sessions/{SID}/levels",
    f"{BASE}/sessions/{SID}/scheme",
    f"{BASE}/sessions/{SID}/plan",
    f"{BASE}/sessions/{SID}/seats",
    f"{BASE}/sessions/{SID}/seattypes",
]:
    try:
        r = requests.get(u, headers=H, timeout=15)
        print(f"{u}\n  -> {r.status_code}: {r.text[:500]}\n")
    except Exception as e:
        print(f"{u}\n  -> ERR {e}\n")

print("\n=== ВСЕ пути API в app.js ===")
js = requests.get("https://www.afisha.ru/w/app.b2ae2665d8454d5e2b3c.js", headers=H, timeout=20).text
paths = set()
# Шаблоны вида "/xxx/".concat(...)
for m in re.finditer(r'["\'`](/[a-zA-Z0-9/._-]{2,50})["\'`]\s*\)?\.concat', js):
    paths.add(m.group(1) + "{id}")
# Просто строки путей
for m in re.finditer(r'["\'`](/[a-zA-Z][a-zA-Z0-9/._-]{2,50})["\'`]', js):
    paths.add(m.group(1))
for p in
