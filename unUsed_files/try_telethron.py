from os import getenv
from telethon import TelegramClient


from dotenv import load_dotenv
load_dotenv('../.venv/.env')

from telethon import events
env_chat_for_exchenge_with_coze_bot = getenv('env_chat_for_exchenge_with_coze_bot')
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = ".venv/session_name.session"
env_coze_bot_id = getenv('env_coze_bot_id')

from local_cache import memory_dict_add_new_cashe, memory_check_cache_replay_message_id



# TODO:Вот этот запрос бы прикрутить к готовеньким TelegramClient
async def send_msg_to_coze_bot_via_tg(message, user_chat_id, user_message_id):
    client_telethron = TelegramClient(session=".venv/session_name.session",
                                      api_id=int(env_telethon_api_id),
                                      api_hash=env_telethon_api_hash)
    await client_telethron.start()
    message = "@neuro44fz_bot " + message
    await client_telethron.send_message(entity=env_chat_for_exchenge_with_coze_bot,
                                                            message=message)



    await client_telethron.disconnect()








