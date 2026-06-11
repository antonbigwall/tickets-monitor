import requests

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://kids.stoyanie.ru/",
    "Origin": "https://kids.stoyanie.ru",
    "Accept": "application/json",
    "X-Application-Key": "e0dff602-86e5-46e2-92f5-c21c3b0b8f1d",
}
SID = "123102883"
BASE = "https://mapi.afisha.ru/api/v21"

candidates = [
    f"{BASE}/availabletickets?sessionId={SID}",
    f"{BASE}/sessions/{SID}/availabletickets",
    f"{BASE}/availabletickets/{SID}",
    f"{BASE}/tickettypes?sessionId={SID}",
    f"{BASE}/sessions/{SID}/tickettypes",
    f"{BASE}/tickettypes/{SID}",
    f"{BASE}/relatedproducts?sessionId={SID}",
    f"{BASE}/sessions/{SID}/relatedproducts",
    f"{BASE}/ticketsset?sessionId={SID}",
    f"{BASE}/sessions/{SID}/ticketsset",
]
for u in candidates:
    try:
        r = requests.get(u, headers=H, timeout=15)
        body = r.text[:800]
        print(f"\n{u}\n  -> {r.status_code}: {body}")
    except Exception as e:
        print(f"\n{u}\n  -> ERR {e}")
