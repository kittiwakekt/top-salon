import requests
import time

BOT_TOKEN = "8469283248:AAHKj5I5L6qlh9_tqj6Vur-22hsRyZDROEQ"
LAST_UPDATE_ID = 0

while True:
    # 1. Спрашиваем у Telegram: "Есть новости?"
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={LAST_UPDATE_ID + 1}').json()
    
    if not response['ok'] or not response['result']:
        time.sleep(2) # Ждем 2 секунды, чтобы не спамить API
        continue

    # 2. Обрабатываем каждое новое сообщение
    for update in response['result']:
        LAST_UPDATE_ID = update['update_id']
        chat_id = update['message']['chat']['id']
        text = update['message']['text']
        
        # 3. Применяем правило: отвечаем эхом
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Ты сказал: {text}')
    
    time.sleep(1)