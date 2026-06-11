import requests

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://kids.stoyanie.ru/",
    "Accept": "application/json",
    "X-Application-Key": "e0dff602-86e5-46e2-92f5-c21c3b0b8f1d",
}
SID = "123102883"
BASE = "https://mapi.afisha.ru/api/v21"

candidates = [
    BASE + "/hall/" + SID,
    BASE + "/session/" + SID,
    BASE + "/sector/" + SID,
    BASE + "/sessions/" + SID + "?include=hall",
]
for u in candidates:
    try:
        r = requests.get(u, headers=H, timeout=15)
        print(u + "\n  -> " + str(r.status_code) + ": " + r.text[:3000] + "\n")
    except Exception as e:
        print(u + "\n  -> ERR " + str(e) + "\n")
