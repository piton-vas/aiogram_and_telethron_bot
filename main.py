import asyncio
import logging
from os import getenv
from dotenv import load_dotenv
from loader import main_aiogram_bot, main_telethron_bot

load_dotenv('.venv/.env')
env_server_mode = getenv('env_server_mode')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = ".venv/session_name.session"

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

async def main():
    await asyncio.gather(main_telethron_bot(), main_aiogram_bot())   # Запускаем оба бота асинхронно


if __name__ == "__main__":
    if env_server_mode=="PROD":   # Сейчас одинаковое, но на потом может быть разное
        asyncio.run(main())
    elif env_server_mode=="TEST":
        asyncio.run(main())
