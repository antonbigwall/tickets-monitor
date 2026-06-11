import requests
import re

URL = "https://kids.stoyanie.ru/tickets"

r = requests.get(URL, timeout=20, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
})

print(f"Status: {r.status_code}, Length: {len(r.text)}")
text = r.text

# Ищем виджет Афиши
for kw in ['afisha', 'kassa', 'rambler', 'widget', 'iframe']:
    positions = [m.start() for m in re.finditer(kw, text, re.IGNORECASE)]
    print(f"\n=== '{kw}': {len(positions)} вхождений ===")
    for pos in positions[:5]:
        print(repr(text[max(0,pos-200):pos+300]))
        print("---")

print("\n=== Все SCRIPT/IFRAME src ===")
for m in re.finditer(r'<(script|iframe)[^>]*src=["\']([^"\']+)["\']', text, re.IGNORECASE):
    print(m.group(2))
