import requests
import re

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://kids.stoyanie.ru/",
    "Origin": "https://kids.stoyanie.ru",
    "Accept": "application/json",
    "X-Application-Key": "e0dff602-86e5-46e2-92f5-c21c3b0b8f1d",
}
SID = "123102883"
BASE = "https://mapi.afisha.ru/api/v21"

print("=== Пробуем endpoints списка товаров ===")
candidates = [
    f"{BASE}/sessions/{SID}/products",
    f"{BASE}/sessions/{SID}/tickets",
    f"{BASE}/sessions/{SID}/places",
    f"{BASE}/sessions/{SID}/categories",
    f"{BASE}/sessions/{SID}/store",
    f"{BASE}/products?sessionId={SID}",
    f"{BASE}/store/{SID}",
    f"{BASE}/store?sessionId={SID}",
]
for u in candidates:
    try:
        r = requests.get(u, headers=H, timeout=15)
        print(f"\n{u}\n  -> {r.status_code}: {r.text[:600]}")
    except Exception as e:
        print(f"\n{u}\n  -> ERR {e}")

print("\n\n=== Пути API в app.js ===")
js = requests.get("https://www.afisha.ru/w/app.b2ae2665d8454d5e2b3c.js", headers=H, timeout=20).text
# Ищем строки-шаблоны путей
paths = set()
for m in re.finditer(r'["`](/[a-zA-Z0-9${}/._:-]*(?:session|product|ticket|place|stor)[a-zA-Z0-9${}/._:-]*)["`]', js, re.IGNORECASE):
    paths.add(m.group(1))
for p in sorted(paths):
    print(p)
