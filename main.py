import asyncio
import logging
from contextlib import asynccontextmanager
from os import getenv

import uvicorn
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv
from telethon import TelegramClient

from routers_fastAPI import root_router

# from db.config import engine, Base
# from routers import book_route
load_dotenv('.env_sending')
env_server_mode = getenv('env_server_mode')

env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')

client_telethron = TelegramClient(session="venv/session_name.session",
                                      api_id=int(env_telethon_api_id),
                                      api_hash=env_telethon_api_hash)

bot = Bot(token=env_main_tg_bot_token,
        parse_mode=ParseMode.HTML)

@asynccontextmanager
async def lifespan1():
    logging.info("🚀 asyncio.gather")
    # from main_bot_iaogram.main_aiogramm_bot import main_aiogram_bot
    # await main_aiogram_bot()
    from main_bot_iaogram.main_aiogramm_bot import main_aiogram_bot
    from proxy_telethron.main_telethron_bot import main_telethron_bot
    await asyncio.gather(main_telethron_bot(), main_aiogram_bot())
    yield
    logging.info("⛔ Stopping asyncio.gather")


def main():
    uvicorn.run(
        "main:lifespan1",
        workers=1,
        factory=True,
        host="localhost",
        port=8088,
        log_level="debug",
    )

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                        level=logging.INFO)
    main()
