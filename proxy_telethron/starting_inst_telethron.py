from os import getenv

from dotenv import load_dotenv

import loader as ld

load_dotenv('.venv/.env')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_api_id = getenv('env_telethon_api_id')


async def main_telethron_bot():

    from proxy_telethron.handlers_telethon import (i_see_edits_handler,
                                                   i_see_response_handler,
                                                   start_go_test_handler)
    ld.client_telethron.add_event_handler(i_see_response_handler)
    ld.client_telethron.add_event_handler(i_see_edits_handler)
    ld.client_telethron.add_event_handler(start_go_test_handler)
    await ld.client_telethron.start()  #  Class 'TelegramClient' does not define '__await__', so the 'await' operator cannot be used on its instances
    try:
        await ld.client_telethron.run_until_disconnected()
    finally:
        await ld.client_telethron.disconnect()
