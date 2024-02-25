import logging
from os import getenv
from pprint import pprint

from dotenv import load_dotenv
from telethon import TelegramClient

import loader as ld

load_dotenv('.venv/.env')

from telethon import events

env_chat_for_exchenge_with_coze_bot = -1002023371936
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = getenv('env_telethon_session')
env_coze_bot_id = getenv('env_coze_bot_id')
env_coze_bot_id_id = int(getenv('env_coze_bot_id_id'))




# TODO:Вот этот запрос бы прикрутить к готовеньким TelegramClient
async def send_msg_to_coze_bot_via_tg(message, user_chat_id, user_message_id):
    logging.info(f"Отправляем сообщение в Telethron. send_msg_to_coze_bot_via_tg{message}")
    await ld.client_telethron.start()
    message = "@" + env_coze_bot_id + " " + message
    await ld.client_telethron.send_message(entity=env_chat_for_exchenge_with_coze_bot,
                                        message=message)



# ________________ Стандартные Ручки тг клиента

# Тестовая ручка, чтобы наскоряк что-то проверить
@events.register(events.NewMessage(chats="v_karpyuk"))  # chats=('v_karpyuk')
async def start_go_test_handler(event):
    message = str(event.message.to_dict()['message'])
    if message.startswith("Го") or message.startswith("Uj"):
        logging.info("Увидели сообщение с текстом 'Го' или 'Uj' ")
        pass


@events.register(events.NewMessage())   #from_users=env_coze_bot_id, chats=env_chat_for_exchenge_with_coze_bot
async def i_see_response_handler(event):


    message_to_dict = event.message.to_dict()
    # pprint(message_to_dict)
    user_id = message_to_dict["from_id"]["user_id"]
    # print(user_id)
    if user_id == env_coze_bot_id_id:

        print("i_see_response_handler: " + message_to_dict["message"])
        from main_bot_iaogram.handlers_aiogram import \
            send_response_from_bot_to_user

        await send_response_from_bot_to_user(user_chat_id=env_chat_for_exchenge_with_coze_bot,
                                             message_text=message_to_dict["message"])


@events.register(events.MessageEdited())
async def i_see_edits_handler(event):                     #     TODO: Добавить send_edits_from_bot_to_user или типа того
    arr = event.message.to_dict()
    print("i_see_edits_handler: " + arr["message"])
