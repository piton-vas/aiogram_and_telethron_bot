from os import getenv

from dotenv import load_dotenv

load_dotenv('.env_sending')

from telethon import TelegramClient, events

from main import client_telethron

env_chat_for_exchenge_with_coze_bot = getenv('env_chat_for_exchenge_with_coze_bot')
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = "venv/session_name.session"
env_coze_bot_id = getenv('env_coze_bot_id')


from local_cache import (memory_check_cache_replay_message_id,
                         memory_dict_add_new_cashe)

# TODO:Вот этот запрос бы прикрутить к готовеньким TelegramClient


    # logging.INFO(f"send_msg_to_coze_bot_via_tg. We have send message to coze_bot by telethon") #TODO: TypeError: 'int' object is not callable


# ________________ Ручки тг клиента

@events.register(events.NewMessage(from_users=env_coze_bot_id,
                                   chats=env_chat_for_exchenge_with_coze_bot))
async def i_see_response_handler(event):
    # from main import cache_dict
    # global cache_dict
    # print(cache_dict)
    # cache_dict.update(i_see_response_handler=12345)

    message_to_dict = event.message.to_dict()
    user_id = message_to_dict["from_id"]["user_id"]             # TODO: Сделать проверку. чтобы только бота читать
    if True:
        reply_to_msg_id = message_to_dict['reply_to']['reply_to_msg_id']
        # msg_id_dict = db_check_cache_replay_messege_id(reply_to_msg_id)
        msg_id_dict = memory_check_cache_replay_message_id(reply_to_msg_id)


        user_chat_id = msg_id_dict["user_chat_id"]
        user_message_id = msg_id_dict["user_message_id"]

        message_text = message_to_dict["message"]
                                                        # TODO: Перенести импорт наверх (исправить ошибку рекурсивности)
        from main_bot_iaogram.handlers_aiogram import \
            send_response_from_bot_to_user

        await send_response_from_bot_to_user(user_chat_id=user_chat_id,
                                       message_text=message_text,
                                       reply_to_msg_id=user_message_id)




@events.register(events.MessageEdited())
async def i_see_edits_handler(event):                     #     TODO: Добавить send_edits_from_bot_to_user или типа того
    arr = event.message.to_dict()
    print(event.message.to_dict())
    pass
