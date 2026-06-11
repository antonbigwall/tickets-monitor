import requests
import re

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://kids.stoyanie.ru/",
    "Accept": "application/json",
    "X-Application-Key": "e0dff602-86e5-46e2-92f5-c21c3b0b8f1d",
}

js = requests.get("https://www.afisha.ru/w/app.b2ae2665d8454d5e2b3c.js", headers=H, timeout=20).text
print(f"app.js: {len(js)}")

for kw in ['availabletickets', 'ticketsset', 'tickettypes', 'relatedproducts', '"/tickets"', '/tickets/']:
    print(f"\n\n######## Контекст '{kw}' ########")
    for m in list(re.finditer(re.escape(kw), js, re.IGNORECASE))[:6]:
        print(repr(js[max(0,m.start()-350):m.start()+350]))
        print("---")
