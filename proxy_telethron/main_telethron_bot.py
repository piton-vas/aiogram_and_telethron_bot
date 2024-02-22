from telethon import TelegramClient

load_dotenv('venv/.env_sending')
env_server_mode = getenv('env_server_mode')

env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')


from handlers_telethon import env_chat_for_exchenge_with_coze_bot

from main import client_telethron

async def main_telethron_bot():
    # client_telethron.add_event_handler(i_see_response_handler)
    # client_telethron.add_event_handler(i_see_edits_handler)
    # client_telethron.add_event_handler(start_go_test_handler)
    await client_telethron.start()  #  Class 'TelegramClient' does not define '__await__', so the 'await' operator cannot be used on its instances
    try:
        await client_telethron.run_until_disconnected()
    finally:
        await client_telethron.disconnect()

async def send_msg_to_coze_bot_via_tg(message, user_chat_id, user_message_id):

    await client_telethron.start()
    message = "@neuro44fz_bot " + message
    send_msg_to_coze = await client_telethron.send_message(entity=env_chat_for_exchenge_with_coze_bot,
                                                      message=message)
    proxy_message_id = send_msg_to_coze.to_dict()["id"]
    # db_add_new_cashe_user_message_id(user_chat_id=user_chat_id,
    #                                  user_message_id=user_message_id,
    #                                  proxy_message_id=proxy_message_id)

    # memory_dict_add_new_cashe(user_chat_id=user_chat_id,
    #                           user_message_id=user_message_id,
    #                           proxy_message_id=proxy_message_id)
