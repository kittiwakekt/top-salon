import requests
from django.conf import settings
import json

BOT_TOKEN = settings.BOT_TOKEN
URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, reply_text, reply_markup=None):
        if not reply_markup:
            reply_markup = {'remove_keyboard': True}
        print(chat_id)
        requests.get(
        f'{URL}/sendMessage',
        params={
            'chat_id': chat_id, 
            'text': reply_text,
            'reply_markup': json.dumps(reply_markup)
            }
    )
