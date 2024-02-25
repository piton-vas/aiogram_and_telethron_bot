from os import getenv

from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

import loader as ld
from main_bot_iaogram.handlers_aiogram import router

load_dotenv('.venv/.env')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')



async def main_aiogram_bot():

    ld.dp.include_router(router)
    await ld.bot.delete_webhook(drop_pending_updates=True)
    await ld.dp.start_polling(ld.bot, allowed_updates=ld.dp.resolve_used_update_types())
