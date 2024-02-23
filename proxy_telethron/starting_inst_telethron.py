# from proxy_telethron.handlers_telethon import i_see_response_handler, i_see_edits_handler, start_go_test_handler
from telethon import TelegramClient


from os import getenv
from dotenv import load_dotenv

load_dotenv('.venv/.env')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_api_id = getenv('env_telethon_api_id')


async def main_telethron_bot():
    client_telethron = TelegramClient(session=".venv/session_name2.session",
                                      api_id=int(env_telethon_api_id),
                                      api_hash=env_telethon_api_hash)
    from proxy_telethron.handlers_telethon import i_see_response_handler, i_see_edits_handler, start_go_test_handler

    client_telethron.add_event_handler(i_see_response_handler)
    client_telethron.add_event_handler(i_see_edits_handler)
    client_telethron.add_event_handler(start_go_test_handler)
    await client_telethron.start()  #  Class 'TelegramClient' does not define '__await__', so the 'await' operator cannot be used on its instances
    try:
        await client_telethron.run_until_disconnected()
    finally:
        await client_telethron.disconnect()
