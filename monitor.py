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

candidates = [
    f"https://mapi.afisha.ru/api/v21/session/{SID}",
    f"https://mapi.afisha.ru/api/v21/sessions/{SID}",
    f"https://mapi.afisha.ru/api/v21/session/{SID}/tickets",
    f"https://mapi.afisha.ru/api/v21/sessions/{SID}/tickets",
    f"https://mapi.afisha.ru/api/v21/session/{SID}?widgetKey={KEY}",
    f"https://mapi.afisha.ru/api/v21/widget/session/{SID}?widgetKey={KEY}",
]

print("=== Пробуем API endpoints ===")
for u in candidates:
    try:
        r = requests.get(u, headers=H, timeout=15)
        print(f"\n{u}\n  -> {r.status_code}: {r.text[:400]}")
    except Exception as e:
        print(f"\n{u}\n  -> ERROR: {e}")

print("\n=== Страница виджета ===")
for wu in [
    f"https://www.afisha.ru/w/session/{SID}?widget-key={KEY}",
    f"https://www.afisha.ru/w/session/{SID}",
]:
    try:
        r = requests.get(wu, headers=H, timeout=15)
        print(f"\n{wu}\n  -> {r.status_code}, длина {len(r.text)}")
        if r.status_code == 200:
            srcs = re.findall(r'src=["\']([^"\']+)["\']', r.text)
            print("  Скрипты:", srcs[:15])
            for m in list(re.finditer(r'v21', r.text))[:5]:
                print("  ", repr(r.text[max(0,m.start()-150):m.start()+150]))
    except Exception as e:
        print(f"\n{wu}\n  -> ERROR: {e}")
