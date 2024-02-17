import asyncio
import logging

from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')
env_server_mode = getenv('env_server_mode')

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
env_main_tg_bot_token = getenv('env_main_tg_bot_token')
from handlers.handlers_aiogram import router

from telethon import TelegramClient  #, sync, events
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = ".venv/session_name.session"
from handlers.handlers_telethon import i_see_edits_handler, i_see_response_handler

async def main_aiogram_bot():
    bot = Bot(token=env_main_tg_bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



async def main_telethron_bot():
    client_proxy_to_telegram = TelegramClient(session=".venv/session_name.session",
                                              api_id=int(env_telethon_api_id),
                                              api_hash=env_telethon_api_hash)
    client_proxy_to_telegram.add_event_handler(i_see_response_handler)
    client_proxy_to_telegram.add_event_handler(i_see_edits_handler)
    await  client_proxy_to_telegram.start()  #  Class 'TelegramClient' does not define '__await__', so the 'await' operator cannot be used on its instances
    try:
        await client_proxy_to_telegram.run_until_disconnected()
    finally:
        await client_proxy_to_telegram.disconnect()



async def main():
    await asyncio.gather(main_aiogram_bot(), main_telethron_bot())   #


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                        level=logging.INFO)
    if env_server_mode=="PROD":
        asyncio.run(main())
    elif env_server_mode=="TEST":
        asyncio.run(main())
