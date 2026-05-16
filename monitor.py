import requests
import time
import os
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8870056110:AAF5zT-mLKG1E6pQRSZnGf3M0SzlJwUxxvc")
CHAT_ID = os.environ.get("CHAT_ID", "394491586")
URL = "https://kids.stoyanie.ru/tickets"
CHECK_INTERVAL = 300  # 5 минут

def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

def check_tickets():
    try:
        r = requests.get(URL, timeout=20, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        text = r.text.lower()

        # Ищем паттерн: "распроданы" а потом в пределах 300 символов "входные билеты"
        # Это означает что входные билеты распроданы
        pattern = r'распроданы.{0,300}входные\s*билеты'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            print("Входные билеты распроданы — всё ок")
            return False
        else:
            print("Паттерн 'распроданы -> входные билеты' не найден — билеты могли появиться!")
            return True

    except Exception as e:
        print(f"Ошибка проверки страницы: {e}")
        return False

def main():
    print("Мониторинг запущен (v3)...")
    send_telegram(
        "✅ <b>Мониторинг билетов запущен (v3)!</b>\n\n"
        "Проверяю каждые 5 минут:\n"
        "https://kids.stoyanie.ru/tickets\n\n"
        "Как только появятся входные билеты — сразу напишу 🎟"
    )

    while True:
        available = check_tickets()
        if available:
            print("БИЛЕТЫ ПОЯВИЛИСЬ! Отправляю уведомление...")
            for _ in range(3):
                send_telegram(
                    "🚨🎟 <b>БИЛЕТЫ ПОЯВИЛИСЬ!</b> 🎟🚨\n\n"
                    "Входные билеты на Архстояние Детское доступны прямо сейчас!\n\n"
                    "👉 <a href='https://kids.stoyanie.ru/tickets'>КУПИТЬ БИЛЕТ</a>\n\n"
                    "Не медли — раскупают быстро!"
                )
                time.sleep(5)
            time.sleep(CHECK_INTERVAL)
        else:
            print(f"Билетов нет. Следующая проверка через {CHECK_INTERVAL // 60} мин.")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
