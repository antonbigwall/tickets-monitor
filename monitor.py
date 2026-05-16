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

def check_tickets():
    r = requests.get(URL, timeout=20, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9",
    })
    
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    
    if r.status_code != 200:
        print(f"Ошибка: статус {r.status_code}")
        sys.exit(0)  # не шлём уведомление при ошибке

    text = r.text.lower()
    
    # Точная проверка: ищем "распроданы" и сразу после (в пределах 500 символов) "входные билеты"
    # Это означает что входные билеты распроданы
    match = re.search(r'распроданы.{0,500}входные\s+билеты', text, re.DOTALL)
    
    if match:
        print("Входные билеты РАСПРОДАНЫ — всё спокойно")
        return False
    
    # Дополнительная проверка: если страница вообще загрузилась нормально
    # (есть ключевые слова сайта) но паттерна нет — значит билеты появились
    if "архстояние" not in text:
        print("Страница загрузилась некорректно — пропускаем")
        sys.exit(0)
    
    print("Паттерн не найден — БИЛЕТЫ ПОЯВИЛИСЬ!")
    return True

if check_tickets():
    for _ in range(3):
        send_telegram(
            "🚨🎟 <b>БИЛЕТЫ ПОЯВИЛИСЬ!</b> 🎟🚨\n\n"
            "Входные билеты на Архстояние Детское доступны прямо сейчас!\n\n"
            "👉 <a href='https://kids.stoyanie.ru/tickets'>КУПИТЬ БИЛЕТ</a>\n\n"
            "Не медли — раскупают быстро!"
        )
        import time; time.sleep(5)
