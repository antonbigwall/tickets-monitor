import requests
import hashlib
import os
import sys

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://kids.stoyanie.ru/tickets"
HASH_FILE = "last_hash.txt"

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

if 'архстояние' not in text:
    print("Страница загрузилась некорректно — пропускаем")
    sys.exit(0)

# Вырезаем только блок статусов: от "в наличии" до "категории билетов"
idx_start = text.find('в наличии')
idx_end = text.find('категории билетов')
if idx_start == -1 or idx_end == -1:
    print("Не нашли блок статусов — пропускаем")
    sys.exit(0)

block = text[idx_start:idx_end]
print(f"Блок статусов ({len(block)} символов):")
print(block[:300])

current_hash = hashlib.md5(block.encode()).hexdigest()
print(f"Текущий хэш: {current_hash}")

# Читаем предыдущий хэш
try:
    with open(HASH_FILE, 'r') as f:
        last_hash = f.read().strip()
    print(f"Предыдущий хэш: {last_hash}")
except:
    last_hash = None
    print("Первый запуск — запоминаем состояние")

# Сохраняем текущий хэш
with open(HASH_FILE, 'w') as f:
    f.write(current_hash)

if last_hash is None or current_hash == last_hash:
    print("Изменений нет — молчим")
    sys.exit(0)

# Изменения есть!
print("ИЗМЕНЕНИЯ В БЛОКЕ СТАТУСОВ!")

idx_sold = text.find('распроданы')
idx_tickets = text.find('входные билеты')
if idx_sold >= 0 and idx_tickets > idx_sold:
    ticket_status = "⚠️ Входные билеты пока ещё распроданы, но что-то изменилось"
else:
    ticket_status = "🎟 ВХОДНЫЕ БИЛЕТЫ ПОЯВИЛИСЬ!"

send_telegram(
    f"🔔 <b>На сайте что-то изменилось!</b>\n\n"
    f"{ticket_status}\n\n"
    f"👉 <a href='https://kids.stoyanie.ru/tickets'>Проверить сайт</a>"
)
