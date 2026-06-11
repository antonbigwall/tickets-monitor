import requests
import json
import os
import sys
import time
from datetime import datetime, timezone

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
STATE_FILE = "last_hash.txt"

SID = "123102883"
API = "https://mapi.afisha.ru/api/v21/hall/" + SID
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://kids.stoyanie.ru/",
    "Origin": "https://kids.stoyanie.ru",
    "Accept": "application/json",
    "X-Application-Key": "e0dff602-86e5-46e2-92f5-c21c3b0b8f1d",
}
PAGE = "https://kids.stoyanie.ru/tickets"

def send_telegram(msg):
    try:
        requests.post(
            "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML",
                  "disable_web_page_preview": True},
            timeout=10,
        )
    except Exception as e:
        print("Telegram error: " + str(e))

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except Exception:
        return {}

def save_state(s):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(s, ensure_ascii=False, sort_keys=True))

state = load_state()
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
hour_utc = datetime.now(timezone.utc).hour

# --- Запрос списка позиций ---
data = None
try:
    r = requests.get(API, headers=HEADERS, timeout=15)
    print("API status: " + str(r.status_code))
    if r.status_code == 200:
        data = r.json()
except Exception as e:
    print("API error: " + str(e))

if data is None:
    fails = state.get("fails", 0) + 1
    state["fails"] = fails
    print("Сбой #" + str(fails))
    if fails == 12:
        send_telegram("⚠️ <b>Мониторинг: API Афиши не отвечает уже ~час.</b> Проверь GitHub Actions.")
    save_state(state)
    sys.exit(0)

state["fails"] = 0

# --- Собираем позиции: имя -> цена ---
items = {}
for level in data.get("levels", []):
    for st in level.get("seatTypes", []):
        name = (st.get("name") or "").strip()
        price = st.get("price")
        qty = st.get("quantity")
        if name:
            items[name] = price
            print("- " + name + " | " + str(price) + " ₽ | остаток " + str(qty))

prev_items = state.get("items")
first_run = prev_items is None
state["items"] = items

new_names = [] if first_run else [n for n in items if n not in prev_items]
gone_names = [] if first_run else [n for n in prev_items if n not in items]
price_changed = [] if first_run else [
    n for n in items if n in prev_items and items[n] != prev_items[n]
]

# --- Ежедневный пульс (09:00 МСК) ---
if hour_utc == 6 and state.get("hb") != today:
    state["hb"] = today
    listing = "\n".join("• " + n + " — " + str(p) + " ₽" for n, p in items.items())
    send_telegram("✅ Мониторинг жив. Позиции в виджете сейчас:\n" + listing +
                  "\n\nВходных билетов пока нет." )

# --- Уведомления ---
if first_run:
    print("Первый запуск финальной версии")
    listing = "\n".join("• " + n + " — " + str(p) + " ₽" for n, p in items.items())
    send_telegram("🔄 <b>Мониторинг переключён на список позиций виджета Афиши.</b>\n"
                  "Текущие позиции:\n" + listing +
                  "\n\nКак только появится НОВАЯ позиция (входной билет) — закричу 3 раза.")
elif new_names:
    print("НОВЫЕ ПОЗИЦИИ: " + str(new_names))
    listing = "\n".join("• <b>" + n + "</b> — " + str(items[n]) + " ₽" for n in new_names)
    for _ in range(3):
        send_telegram(
            "🚨🎟 <b>НОВАЯ ПОЗИЦИЯ В ПРОДАЖЕ!</b> 🎟🚨\n\n" + listing +
            "\n\n👉 " + PAGE + "\n\nБеги покупать!"
        )
        time.sleep(3)
else:
    msgs = []
    if gone_names:
        msgs.append("➖ Исчезли позиции: " + ", ".join(gone_names))
    if price_changed:
        msgs.append("💸 Изменились цены: " + ", ".join(
            n + " (" + str(prev_items[n]) + "→" + str(items[n]) + " ₽)" for n in price_changed))
    if msgs:
        send_telegram("🔔 <b>Изменения в виджете билетов:</b>\n\n" + "\n".join(msgs) +
                      "\n\n👉 " + PAGE)
        print("Изменения: " + "; ".join(msgs))
    else:
        print("Изменений нет — молчим")

save_state(state)
