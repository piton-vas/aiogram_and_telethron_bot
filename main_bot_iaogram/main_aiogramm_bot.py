from os import getenv
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager

from loguru import logger

from aiogram import Bot, Dispatcher
from handlers.handlers_aiogram import router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage



load_dotenv('../.venv/.env')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')

async def main_aiogram_bot():
    bot = Bot(token=env_main_tg_bot_token,
              parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



    # if __name__ == "__main__":
    #     logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    #                         level=logging.INFO)
    #     if env_server_mode=="PROD":
    #         asyncio.run(main())
    #     elif env_server_mode=="TEST":
    #         asyncio.run(main())