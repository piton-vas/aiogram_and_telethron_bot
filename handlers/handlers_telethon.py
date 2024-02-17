from os import getenv
import logging

from dotenv import load_dotenv
load_dotenv('../.venv/.env')

from telethon import TelegramClient, events
env_chat_for_exchenge_with_coze_bot = getenv('env_chat_for_exchenge_with_coze_bot')
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = ".venv/session_name.session"
env_coze_bot_id = getenv('env_coze_bot_id')

from database import db_add_new_cashe_user_message_id, db_check_cache_replay_messege_id


# TODO:Вот этот запрос бы прикрутить к готовеньким TelegramClient
async def send_msg_to_coze_bot_via_tg(message, user_chat_id, user_message_id):
    client = TelegramClient(session=".venv/send_msg_to_coze_bot_via_tg.session",
                            api_id=int(env_telethon_api_id),
                            api_hash=env_telethon_api_hash)
    await client.start()
    message = "@neuro44fz_bot " + message
    send_message_to_china = await client.send_message(entity=env_chat_for_exchenge_with_coze_bot,
                                                      message=message)
    proxy_messege_id = send_message_to_china.to_dict()["id"]
    db_add_new_cashe_user_message_id(user_chat_id=user_chat_id,
                                     user_message_id=user_message_id,
                                     proxy_messege_id=proxy_messege_id)

    # logging.INFO(f"send_msg_to_coze_bot_via_tg. We have send message to coze_bot by telethon") #TODO: TypeError: 'int' object is not callable

    await client.disconnect()

# ________________ Ручки тг клиента


@events.register(events.NewMessage(from_users=env_coze_bot_id,
                                   chats=env_chat_for_exchenge_with_coze_bot))
async def i_see_response_handler(event):
    message_to_dict = event.message.to_dict()
    user_id = message_to_dict["from_id"]["user_id"]             # TODO: Сделать проверку. чтобы только бота читать
    if True:
        reply_to_msg_id = message_to_dict['reply_to']['reply_to_msg_id']
        msg_id_dict = db_check_cache_replay_messege_id(reply_to_msg_id)

        user_chat_id = msg_id_dict["user_chat_id"]
        user_message_id = msg_id_dict["user_message_id"]

        message_text = message_to_dict["message"]
                                                        # TODO: Перенести импорт наверх (исправить ошибку рекурсивности)
        from handlers.handlers_aiogram import send_response_from_bot_to_user

        await send_response_from_bot_to_user(user_chat_id=user_chat_id,
                                       message_text=message_text,
                                       reply_to_msg_id=user_message_id)




@events.register(events.MessageEdited())
async def i_see_edits_handler(event):                     #     TODO: Добавить send_edits_from_bot_to_user или типа того
    arr = event.message.to_dict()
    print(event.message.to_dict())
    pass



# @events.register(events.NewMessage(chats=('v_karpyuk')))
# async def start_go_test_handler(event):
#     if str(event.message.to_dict()['message']).startswith("Го") or str(event.message.to_dict()['message']).startswith("Uj"):
#         print("Погнали")
#         # client = event.client
#         await send_msg_to_china( "Что такое обеспечение заявки") # client,
#
#         # send_message_to_china = await client.send_message('neuro44fz_bot', 'Что такое обеспечение контракта?')
#         # id_message_to_china = send_message_to_china.to_dict()["id"]
#         # print(send_message_to_china.to_dict()["id"])
#


