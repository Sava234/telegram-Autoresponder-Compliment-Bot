from telethon import TelegramClient, events, utils, types
import asyncio
import random
import datetime
from telethon.errors import SessionPasswordNeededError

# --- ВАШИ ДАННЫЕ ---
api_id_x = 
api_hash_x = '-'
session_name_x = 'sender_x'

client_x = TelegramClient(session_name_x, api_id_x, api_hash_x)

# --- НАСТРОЙКИ РЕЖИМА ---
MODE = 'autoreply'  # Возможные значения: 'compliment', 'autoreply', 'autoreply_once', 'autoreply_timed'

# --- ВРЕМЯ ОЖИДАНИЯ МЕЖДУ ОТВЕТАМИ (в секундах) ---
REPLY_TIMEOUT = 60 * 60 * 24  # 24 часа (пример)

# --- ШАБЛОНЫ ОТВЕТОВ ---
autoreply_templates = [
    "Привет! Сейчас не могу ответить, но скоро вернусь.",
    "Спасибо за сообщение! Я прочитаю его позже.",
    "Здравствуйте! Ваше сообщение получено.",
    "Извините, я занят(а). Отвечу, как только смогу.",
    "Приветствую! Благодарю за ваше обращение."
]

autoreply_once_templates = [
    "Привет! Спасибо за ваше сообщение.",
    "Я получил ваше сообщение и скоро отвечу.",
    "Здравствуйте! Ваше сообщение принято.",
    "Благодарю за ваше обращение!",
    "Приветствую!"
]

autoreply_timed_templates = [
    "Привет! Спасибо за ваше сообщение.",
    "Я получил ваше сообщение и отвечу позже.",
    "Здравствуйте!",
    "Благодарю за ваше обращение!",
    "Приветствую!"
]

# --- СПИСОК КОМПЛИМЕНТОВ ---
compliments_list = [
    "Ты сегодня выглядишь просто восхитительно!",
    "Твой ум и сообразительность поражают!",
    "Ты очень добрый, отзывчивый и чуткий человек.",
    "Твоя энергия и оптимизм вдохновляют!",
    "С тобой всегда интересно и приятно общаться.",
    "У тебя прекрасное чувство юмора!",
    "Твоя креативность не знает границ!",
    "Ты умеешь видеть прекрасное в мелочах.",
    "Твоя настойчивость помогает тебе достигать целей.",
    "Ты излучаешь позитив!",
    "Твоя доброта делает мир лучше.",
    "Ты очень талантливый человек во многих отношениях.",
    "Твоя улыбка может поднять настроение кому угодно.",
    "Ты обладаешь невероятной харизмой.",
    "Твоя мудрость превосходит твои годы.",
    "Ты всегда готов прийти на помощь.",
    "Твое чувство стиля безупречен.",
    "Ты умеешь слушать и поддерживать.",
    "Твоя целеустремленность достойна восхищения.",
    "Ты настоящий друг!",
    "Ты делаешь этот мир ярче!",
    "Твои идеи всегда свежи и оригинальны.",
    "Ты обладаешь внутренней силой и стойкостью.",
    "Твое присутствие делает любое место лучше.",
    "Ты замечательный собеседник.",
    "Твоя эмпатия позволяет тебе понимать других.",
    "Ты всегда стремишься к самосовершенствованию.",
    "Твоя уверенность в себе заразительна.",
    "Ты умеешь находить выход из сложных ситуаций.",
    "Ты просто великолепен!",
    "Твой взгляд наполнен добротой.",
    "Ты очень внимательный к деталям.",
    "Твоя страсть к жизни вдохновляет.",
    "Ты умеешь ценить прекрасные моменты.",
    "Твоя открытость новому впечатляет.",
    "Ты обладаешь редким даром убеждения.",
    "Твоя преданность своим принципам вызывает уважение.",
    "Ты умеешь создавать уют и гармонию вокруг себя.",
    "Твоя щедрость не знает границ.",
    "Ты настоящий лидер!",
    "Твоя способность к обучению поразительна.",
    "Ты умеешь находить общий язык с разными людьми.",
    "Твоя жизнерадостность заражает.",
    "Ты обладаешь особым шармом.",
    "Твоя честность вызывает доверие.",
    "Ты умеешь мечтать по-крупному!",
    "Твоя способность прощать делает тебя сильнее.",
    "Ты умеешь наслаждаться каждым днем.",
    "Ты просто чудо!",
]

# --- ЦЕЛИ ДЛЯ РЕЖИМА "КОМПЛИМЕНТЫ" ---
targets = [
    {'type': 'username', 'value': '@username1'},
    {'type': 'id', 'value': 123456789},
    # Добавьте сюда username'ы (с @) и ID нужных пользователей
]
sent_online_or_recent = {}

# --- СЛОВАРЬ ДЛЯ ОТСЛЕЖИВАНИЯ ПОСЛЕДНЕГО СООБЩЕНИЯ (КТО КОМУ НАПИСАЛ) ---
last_interaction = {}  # {user_id: 'sent' или 'received'}
replied_users = {}
last_reply_time = {}

async def generate_compliment():
    return random.choice(compliments_list)

async def generate_autoreply():
    return random.choice(autoreply_templates)

async def generate_autoreply_once():
    return random.choice(autoreply_once_templates)

async def generate_autoreply_timed():
    return random.choice(autoreply_timed_templates)

async def get_target_entity(client, target):
    try:
        if target['type'] == 'username':
            entity = await client.get_entity(target['value'])
        elif target['type'] == 'id':
            entity = await client.get_entity(int(target['value']))
        return entity
    except Exception as e:
        print(f"Ошибка при получении entity для {target}: {e}")
        return None

async def main():
    global last_interaction
    global replied_users
    global last_reply_time
    global sent_online_or_recent
    await client_x.connect()
    if not await client_x.is_user_authorized():
        phone_number_x = input("Пожалуйста, введите номер телефона вашего аккаунта X: ")
        await client_x.send_code_request(phone_number_x)
        code = input("Пожалуйста, введите код, который вы получили в Telegram: ")
        try:
            await client_x.sign_in(phone_number_x, code)
        except SessionPasswordNeededError:
            password = input("Пожалуйста, введите пароль от вашей двухэтапной аутентификации: ")
            await client_x.sign_in(phone_number_x, code, password=password)
        print("Авторизация аккаунта X прошла успешно.")

    @client_x.on(events.NewMessage(outgoing=True, chats=None))
    async def outgoing_message_handler(event):
        if event.is_private:
            target_id = event.chat_id
            last_interaction[target_id] = 'sent'
            await asyncio.sleep(1) # Небольшая задержка

    if MODE == 'compliment':
        target_entities = {}
        for target in targets:
            entity = await get_target_entity(client_x, target)
            if entity:
                target_entities[entity.id] = entity
                sent_online_or_recent[entity.id] = False

        @client_x.on(events.UserUpdate(chats=list(target_entities.values())))
        async def compliment_handler(event):
            if event.user_id in target_entities:
                user = target_entities[event.user_id]
                if event.status:
                    if (isinstance(event.status, types.UserStatusOnline) or isinstance(event.status, types.UserStatusRecently)) and not sent_online_or_recent[user.id]:
                        compliment = await generate_compliment()
                        try:
                            await client_x.send_message(user, compliment)
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Отправлен комплимент пользователю {utils.get_display_name(user)} (ID: {user.id}, статус: {event.status}): '{compliment}'")
                            sent_online_or_recent[user.id] = True
                            await asyncio.sleep(2)
                        except Exception as e:
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка при отправке комплимента: {e}")
                    elif not (isinstance(event.status, types.UserStatusOnline) or isinstance(event.status, types.UserStatusRecently)):
                        sent_online_or_recent[user.id] = False
                        await asyncio.sleep(1)

        print(f"Скрипт запущен в режиме 'комплимент'. Ожидание входа в сеть...")
        await client_x.run_until_disconnected()

    elif MODE == 'autoreply':
        @client_x.on(events.NewMessage(incoming=True, from_users=None))
        async def autoreply_handler(event):
            if event.is_private:
                sender = await event.get_sender()
                if sender and not sender.bot:
                    sender_id = event.sender_id
                    if sender_id not in last_interaction or last_interaction[sender_id] == 'received':
                        reply_text = await generate_autoreply()
                        try:
                            await event.reply(reply_text)
                            last_interaction[sender_id] = 'replied' # Чтобы не отвечать несколько раз сразу
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Отвечено пользователю {utils.get_display_name(sender)} (ID: {sender_id}): '{reply_text}'")
                            await asyncio.sleep(random.randint(1, 3))
                        except Exception as e:
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка при отправке автоответчика: {e}")
                    else:
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Исходящее сообщение найдено для {utils.get_display_name(sender)} (ID: {sender_id}), автоответ пропущен.")
                    last_interaction[sender_id] = 'received'

        print(f"Скрипт запущен в режиме 'автоответчик' с функцией стоп-ответа...")
        await client_x.run_until_disconnected()

    elif MODE == 'autoreply_once':
        @client_x.on(events.NewMessage(incoming=True, from_users=None))
        async def autoreply_once_handler(event):
            if event.is_private:
                sender = await event.get_sender()
                if sender and not sender.bot:
                    sender_id = event.sender_id
                    if sender_id not in last_interaction or last_interaction[sender_id] == 'received':
                        if sender_id not in replied_users:
                            reply_text = await generate_autoreply_once()
                            try:
                                await event.reply(reply_text)
                                replied_users[sender_id] = True
                                last_interaction[sender_id] = 'replied'
                                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Однократно отвечено пользователю {utils.get_display_name(sender)} (ID: {sender_id}): '{reply_text}'")
                                await asyncio.sleep(random.randint(1, 3))
                            except Exception as e:
                                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка при отправке однократного автоответчика: {e}")
                        else:
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Пользователю {utils.get_display_name(sender)} (ID: {sender_id}) уже был дан ответ.")
                    else:
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Исходящее сообщение найдено для {utils.get_display_name(sender)} (ID: {sender_id}), автоответ пропущен.")
                    last_interaction[sender_id] = 'received'

        print(f"Скрипт запущен в режиме 'один ответ всем' с функцией стоп-ответа...")
        await client_x.run_until_disconnected()

    elif MODE == 'autoreply_timed':
        @client_x.on(events.NewMessage(incoming=True, from_users=None))
        async def autoreply_timed_handler(event):
            if event.is_private:
                sender = await event.get_sender()
                if sender and not sender.bot:
                    sender_id = event.sender_id
                    now = datetime.datetime.now().timestamp()
                    if sender_id not in last_interaction or last_interaction[sender_id] == 'received':
                        if sender_id not in last_reply_time or (now - last_reply_time[sender_id]) >= REPLY_TIMEOUT:
                            reply_text = await generate_autoreply_timed()
                            try:
                                await event.reply(reply_text)
                                last_reply_time[sender_id] = now
                                last_interaction[sender_id] = 'replied'
                                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Отвечено пользователю {utils.get_display_name(sender)} (ID: {sender_id}). Следующий ответ через {REPLY_TIMEOUT} секунд.")
                                await asyncio.sleep(random.randint(1, 3))
                            except Exception as e:
                                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка при отправке временного автоответчика: {e}")
                        else:
                            time_left = REPLY_TIMEOUT - (now - last_reply_time[sender_id])
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] До следующего ответа пользователю {utils.get_display_name(sender)} (ID: {sender_id}) осталось {int(time_left)} секунд.")
                    else:
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Исходящее сообщение найдено для {utils.get_display_name(sender)} (ID: {sender_id}), автоответ пропущен.")
                    last_interaction[sender_id] = 'received'

        print(f"Скрипт запущен в режиме 'автоответчик с временем' с функцией стоп-ответа...")
        await client_x.run_until_disconnected()

    else:
        print(f"Неизвестный режим: '{MODE}'. Пожалуйста, выберите режим автоответчика.")

    await client_x.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
