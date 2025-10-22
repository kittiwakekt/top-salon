from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from time import sleep
from bot.models import TgUser, Message
from salon.models import Master, Salon
from datetime import datetime
import json
from bot.utils import send_message

class Command(BaseCommand):
    help = 'Запускает бота в режиме Long-Polling'

    def handle(self, *args, **options):
        self.stdout.write('Бот запущен...')
        BOT_TOKEN = settings.BOT_TOKEN
        URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
        offset = 0

        def answer_callback_query(callback_id, text=None):
            """Отвечает на callback query - УБИРАЕМ ЧАСИКИ"""
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
            payload = {'callback_query_id': callback_id}
            if text:
                payload['text'] = text  # Для всплывающего уведомления
            requests.post(url, json=payload)    

        def handle_callback_query(callback_query):
            callback_id = callback_query['id']
            chat_id = callback_query['message']['chat']['id']
            callback_data = callback_query['data']
            message_id = callback_query['message']['message_id']

            answer_callback_query(callback_id)

            # 2. Получаем пользователя из БД
            user = TgUser.objects.get(chat_id=chat_id)
            if callback_data.startswith('salon-'):
                salon_id = int(callback_data.split('-')[1])
                user.set_master_salon(salon_id)
                user.save()

                edit_message(chat_id, message_id, f"Ok! мастер добавлен")

        def edit_message(chat_id, message_id, new_text, new_buttons=None):
            """Изменяет существующее сообщение с inline-кнопками"""
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"

            payload = {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": new_text
            }

            if new_buttons:
                payload["reply_markup"] = json.dumps({"inline_keyboard": new_buttons})

            requests.post(url, json=payload)

        while True:
            try:
                # 1. Получаем обновления
                updates = requests.get(
                    f'{URL}/getUpdates',
                    params={'offset': offset + 1, 'timeout': 30}
                ).json()

                if not updates['ok'] or not updates['result']:
                    sleep(2)
                    continue

                # 2. Обрабатываем каждое обновление
                for update in updates['result']:
                    offset = update['update_id'] # Обновляем offset

                    if 'callback_query' in update:
                        # Нажатие на inline-кнопку!
                        handle_callback_query(update['callback_query'])
                    else:
                        message = update.get('message')
                        if not message:
                            continue

                        chat_id = message['chat']['id']
                        text = message.get('text', '')
                        user_info = message['from']

                        # 3. Находим или создаем пользователя в БД
                        user, created = TgUser.objects.get_or_create(
                            chat_id=chat_id,
                            defaults={
                                'username': user_info.get('username'),
                                'first_name': user_info.get('first_name'),
                                'last_name': user_info.get('last_name'),
                            }
                        )
                        # 4. Сохраняем в БД сообщение от пользователя
                        Message.objects.create(user=user, text=text, is_bot=False)
                        reply_markup = {'remove_keyboard': True}
                        if text == '/cancel':
                            user.reset_state()
                            user.save()
                            reply_text = "Диалог прерван."
                            # ... отправляем сообщение ...
                            return
                        # fsm
                        available_transitions = user.get_available_state_transitions()
                        if text == '/addmaster':
                            # if user.can_start_adding_master():  # can_* методы создаются автоматически!
                                user.start_adding_master()      # Вызываем метод перехода
                                user.save()
                                reply_text = "Отлично! Введите имя мастера."
                            # else:
                            #     reply_text = "Сейчас нельзя начать добавление мастера."

                        elif user.state == 'wating_master_first_name':
                            # Данные для перехода 'set_master_name'
                            # if user.can_set_master_name():
                                user.set_master_name(name=text)  # Вызываем переход, передаем данные
                                user.save()
                                reply_text = "Принято! Теперь введите фамилию"
                            # else:
                            #     reply_text = "Ошибка: невозможен переход в текущем состоянии."

                        elif user.state == 'wating_master_last_name':
                            # Данные для перехода 'set_master_name'
                            # if user.can_set_master_last_name():
                                user.set_master_last_name(name=text)  # Вызываем переход, передаем данные
                                user.save()
                                reply_text = "Принято! Теперь введите специализацию"
                                reply_markup = {
                                    'keyboard': [
                                        ['Парикмахер', 'Маникюр'],
                                        ['Косметолог', 'Массажист'],
                                        ['Барбер']
                                    ],
                                    'resize_keyboard': True,    # Подгоняет размер кнопок
                                    'one_time_keyboard': True,  # Скрывает после нажатия
                                    'selective': False 
                                }

                            # else:
                            #     reply_text = "Ошибка: невозможен переход в текущем состоянии."
                        elif user.state == 'wating_specialization':
                            # Данные для перехода 'set_master_name'
                            # if user.can_set_master_specialization():
                                user.set_master_specialization(specialization=text)  # Вызываем переход, передаем данные
                                user.save()

                                reply_text = "Принято! Теперь введите опыт работы мастера (в годах)."
                            # else:
                            #     reply_text = "Ошибка: невозможен переход в текущем состоянии."

                        elif user.state == 'wating_experience':
                            # Данные для перехода 'set_experience_and_finish'
                            # if user.can_set_master_experience():
                                try:
                                    experience = int(text)  # Преобразуем в число
                                    if experience < 0 or experience > 50:
                                        reply_text = "Пожалуйста, введите реалистичный опыт работы (0-50 лет)."
                                    else:
                                        user.set_master_experience(experience=experience)
                                        user.save()
                                        reply_text = f"В какой салон?"
                                        salons = Salon.objects.filter(is_active=True)
                                        board = []
                                        for salon in salons:
                                            board.append([{"text": salon.name, "callback_data": f"salon-{salon.id}"}])
                                        reply_markup = {
                                                "inline_keyboard": board
                                            }
                                except ValueError:
                                    reply_text = "Пожалуйста, введите опыт работы числом (например: 5)."
                            # else:
                            #     reply_text = "Ошибка: невозможен переход в текущем состоянии."
                        elif user.state == 'wating_salon':
                            reply_text = f"Спасибо! Мастер успешно добавлен в базу!"

                        elif user.state == 'start':
                            if text == '/start':
                                reply_text = f'Приветствую {user_info.get('first_name')}. Если хотите добавить специалиста, введите /addmaster'
                            else:
                                reply_text = "Не понимаю. Используйте /start или /addmaster"

                        # 6. Отправляем ответ
                        send_message(chat_id, reply_text, reply_markup)
                        # requests.get(
                        #     f'{URL}/sendMessage',
                        #     params={
                        #         'chat_id': chat_id, 
                        #         'text': reply_text,
                        #         'reply_markup': json.dumps(reply_markup)
                        #         }
                        # )
                        # 7. Сохраняем в БД ответ бота
                        Message.objects.create(user=user, text=reply_text, is_bot=True)

                        self.stdout.write(f'Обработано сообщение от {user}: {text}')

            except requests.exceptions.RequestException as e:
                self.stderr.write(f'Ошибка сети: {e}')
                sleep(5)
            except Exception as e:
                self.stderr.write(f'Неизвестная ошибка: {e}')
                sleep(1)