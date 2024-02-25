import logging
from os import getenv
from pprint import pprint
from dotenv import load_dotenv
from telethon import events
import loader as ld
from local_cache import memory_dict_add_new_cashe

load_dotenv('.venv/.env')
env_chat_for_exchenge_with_coze_bot = -1002023371936
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = getenv('env_telethon_session')
env_3th_party_bot = getenv('env_3th_party_bot')
env_3th_party_bot_id = int(getenv('env_3th_party_bot_id'))

# Пересылаем сообщение от пользователя в телеграмме в группу со сторонним ботом
async def send_msg_to_3th_party_bot_via_tg(message, user_chat_id, user_message_id):
    logging.info(f"Отправляем сообщение в Telethron. send_msg_to_3th_party_bot_via_tg{message}")
    message = "@" + env_3th_party_bot + " " + message
    proxy_message = await ld.client_telethron.send_message(entity=env_chat_for_exchenge_with_coze_bot,
                                                           message=message)
    proxy_message_id = proxy_message.to_dict()["id"]
    memory_dict_add_new_cashe(user_chat_id, user_message_id, proxy_message_id)

# ________________ Стандартные Ручки Telethron клиента
# Получаем сообщение от стороннего бота, можем отправлять нашему юзеру
@events.register(events.NewMessage())
async def i_see_response_handler(event):
    message_to_dict = event.message.to_dict()
    user_id = message_to_dict["from_id"]["user_id"]
    if user_id == env_3th_party_bot_id:
        reply_to_msg_id = message_to_dict["reply_to"]["reply_to_msg_id"]
        message = message_to_dict["message"]
        # print("i_see_response_handler: " + message)

        from main_bot_iaogram.handlers_aiogram import send_response_from_bot_to_user
        await send_response_from_bot_to_user(reply_to_msg_id=reply_to_msg_id,
                                             message_text=message)

# Получаем изменения сообщения от стороннего бота, отправляем изменения нашему юзеру
@events.register(events.MessageEdited())
async def i_see_edits_handler(event):

    message_to_dict = event.message.to_dict()
    user_id = message_to_dict["from_id"]["user_id"]

    if user_id == env_3th_party_bot_id:
        reply_to_msg_id = message_to_dict["reply_to"]["reply_to_msg_id"]
        message = message_to_dict["message"]
        # print("i_see_edits_handler: " + str(reply_to_msg_id))
        from main_bot_iaogram.handlers_aiogram import edit_response_from_bot_to_user
        await edit_response_from_bot_to_user(replay_massage_id=reply_to_msg_id,
                                             message_text=message)
