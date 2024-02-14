import asyncio
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

import os
from dotenv import load_dotenv
load_dotenv('.venv/.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')
server_mode = os.getenv('server_mode')

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

telethon_api_id = os.getenv('telethon_api_id')
telethon_api_hash = os.getenv('telethon_api_hash')

from handlers import router, normal_handler

from telethon import TelegramClient, sync, events



async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    # dp.message.register(cmd_profile)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async  def proxi_to_china():
    client = TelegramClient('session_name', telethon_api_id, telethon_api_hash)
    client.add_event_handler(normal_handler)

    await client.start()

    try:
        # await plugins.init(client) # хз что это
        await client.run_until_disconnected()
    finally:
        await client.disconnect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if server_mode=="PROD":
        asyncio.run(main())
    elif server_mode=="TEST":
        asyncio.run(proxi_to_china())



