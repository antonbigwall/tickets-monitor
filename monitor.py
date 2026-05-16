import requests
import re
import os
import sys

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://kids.stoyanie.ru/tickets"

r = requests.get(URL, timeout=20, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9",
})

print(f"Status: {r.status_code}, Length: {len(r.text)}")

text = r.text.lower()

# Ищем все вхождения ключевых слов и печатаем контекст
for kw in ['распроданы', 'входные билеты', 'входные\xa0билеты', 'soldout', 'sold_out']:
    idx = text.find(kw)
    if idx >= 0:
        print(f"\n=== '{kw}' найдено на позиции {idx} ===")
        print(repr(text[max(0,idx-200):idx+200]))
    else:
        print(f"\n=== '{kw}' НЕ НАЙДЕНО ===")
