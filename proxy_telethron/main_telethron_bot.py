from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv('.venv/.env')
env_server_mode = getenv('env_server_mode')

env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')

async def main_telethron_bot():
    client_telethron = TelegramClient(session=".venv/session_name.session",
                                      api_id=int(env_telethon_api_id),
                                      api_hash=env_telethon_api_hash)
    # client_telethron.add_event_handler(i_see_response_handler)
    # client_telethron.add_event_handler(i_see_edits_handler)
    # client_telethron.add_event_handler(start_go_test_handler)
    await client_telethron.start()  #  Class 'TelegramClient' does not define '__await__', so the 'await' operator cannot be used on its instances
    try:
        await client_telethron.run_until_disconnected()
    finally:
        await client_telethron.disconnect()