import asyncio
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')
server_mode = getenv('server_mode')

BOT_TOKEN = getenv('BOT_TOKEN')
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

telethon_api_id = getenv('telethon_api_id')
telethon_api_hash = getenv('telethon_api_hash')
from handlers import router, i_see_edits_handler, i_see_response_handler, handler_test
from telethon import TelegramClient  #, sync, events

async def main_aiogram_bot():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def proxi_to_china():
    client_proxy_to_telegram = TelegramClient('.venv/send_msg_to_china', telethon_api_id, telethon_api_hash)
    client_proxy_to_telegram.add_event_handler(i_see_response_handler)
    await  client_proxy_to_telegram.start()
    try:
        await client_proxy_to_telegram.run_until_disconnected()
    finally:
        await client_proxy_to_telegram.disconnect()

async def main():
    await asyncio.gather(main_aiogram_bot(), proxi_to_china())   #


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if server_mode=="PROD":
        asyncio.run(main())
    elif server_mode=="TEST":
        asyncio.run(main())
