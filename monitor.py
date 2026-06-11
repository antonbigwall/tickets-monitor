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
candidates = [
    BASE + "/sessions/" + SID + "/hall",
    BASE + "/sessions/" + SID + "/halls",
    BASE + "/sessions/" + SID + "/levels",
    BASE + "/sessions/" + SID + "/scheme",
    BASE + "/sessions/" + SID + "/plan",
    BASE + "/sessions/" + SID + "/seats",
    BASE + "/sessions/" + SID + "/seattypes",
]
for u in candidates:
    try:
        r = requests.get(u, headers=H, timeout=15)
        print(u + "\n  -> " + str(r.status_code) + ": " + r.text[:500] + "\n")
    except Exception as e:
        print(u + "\n  -> ERR " + str(e) + "\n")

print("\n=== ВСЕ пути API в app.js ===")
js = requests.get("https://www.afisha.ru/w/app.b2ae2665d8454d5e2b3c.js", headers=H, timeout=20).text
paths = set()
for m in re.finditer(r'["\'`](/[a-zA-Z0-9/._-]{2,50})["\'`]\s*\)?\.concat', js):
    paths.add(m.group(1) + "{id}")
for m in re.finditer(r'["\'`](/[a-zA-Z][a-zA-Z0-9/._-]{2,50})["\'`]', js):
    paths.add(m.group(1))
for p in sorted(paths):
    if not p.startswith("/w/") and not p.startswith("/img") and not p.startswith("/css") and not p.startswith("/fonts"):
        print(p)
