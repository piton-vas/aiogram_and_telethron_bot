from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from main_bot_iaogram.handlers_aiogram import main_aiogram_router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage



load_dotenv('../.venv/.env')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')

async def main_aiogram_bot():
    bot = Bot(token=env_main_tg_bot_token,
              parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_aiogram_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

