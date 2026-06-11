import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://kids.stoyanie.ru/",
}

# Качаем скрипт виджета Афиши
r = requests.get("https://afisha.ru/w/afishaWidgetManager.global.js", headers=HEADERS, timeout=20)
js = r.text
print(f"Status: {r.status_code}, Length: {len(js)}")

# Все URL внутри скрипта
print("\n=== Все URL в скрипте ===")
urls = sorted(set(re.findall(r'https?://[^"\'\s\\)]+', js)))
for u in urls:
    print(u)

# Контекст вокруг слов api / session
for kw in ['api', 'session']:
    print(f"\n=== Контекст '{kw}' (первые 10) ===")
    for m in list(re.finditer(kw, js, re.IGNORECASE))[:10]:
        print(repr(js[max(0, m.start()-120):m.start()+180]))
        print("---")
