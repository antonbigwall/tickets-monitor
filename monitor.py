import requests
import re
import os
import sys

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://kids.stoyanie.ru/tickets"

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"},
        timeout=10
    )

r = requests.get(URL, timeout=20, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
})

print(f"Status: {r.status_code}, Length: {len(r.text)}")

if r.status_code != 200:
    print("Ошибка загрузки — пропускаем")
    sys.exit(0)

text = r.text.lower()

# Выводим контекст вокруг ключевых слов для диагностики
for kw in ['распроданы', 'входные билеты', 'soldout']:
    idx = text.find(kw)
    if idx >= 0:
        print(f"НАЙДЕНО '{kw}' на позиции {idx}:")
        print(repr(text[max(0,idx-150):idx+150]))
    else:
        print(f"НЕ НАЙДЕНО: '{kw}'")

# Проверка: билеты распроданы если "распроданы" встречается раньше "входные билеты"
idx_sold = text.find('распроданы')
idx_tickets = text.find('входные билеты')

print(f"\nПозиция 'распроданы': {idx_sold}")
print(f"Позиция 'входные билеты': {idx_tickets}")
print(f"Разница: {idx_tickets - idx_sold if idx_sold >= 0 and idx_tickets >= 0 else 'N/A'}")

if idx_sold >= 0 and idx_tickets >= 0 and idx_tickets > idx_sold:
    print("Билеты РАСПРОДАНЫ — молчим")
    sys.exit(0)

print("БИЛЕТЫ ПОЯВИЛИСЬ — отправляем уведомление!")
for _ in range(3):
    send_telegram(
        "🚨🎟 <b>БИЛЕТЫ ПОЯВИЛИСЬ!</b> 🎟🚨\n\n"
        "Входные билеты на Архстояние Детское доступны прямо сейчас!\n\n"
        "👉 <a href='https://kids.stoyanie.ru/tickets'>КУПИТЬ БИЛЕТ</a>\n\n"
        "Не медли — раскупают быстро!"
    )
    import time; time.sleep(5)
