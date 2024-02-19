import asyncio
import logging

from os import getenv
from dotenv import load_dotenv

from main_bot_iaogram.starting_inst_iaogram import main_aiogram_bot
from proxy_telethron.starting_inst_telethron import main_telethron_bot

load_dotenv('.venv/.env')
env_server_mode = getenv('env_server_mode')


env_main_tg_bot_token = getenv('env_main_tg_bot_token')

from telethon import TelegramClient

env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_telethon_session = ".venv/session_name.session"

env_db_host = getenv('env_db_host')
env_db_username = getenv('env_db_username')
env_db_pass = getenv('env_db_pass')
env_db_name = getenv('env_db_name')

# cache_dict = dict()
# cache_dict = {'dict': 1, 'dictionary': 2}

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)








async def main():
    await asyncio.gather(main_telethron_bot(), main_aiogram_bot())   # m


if __name__ == "__main__":

    if env_server_mode=="PROD":
        asyncio.run(main())
    elif env_server_mode=="TEST":
        asyncio.run(main())
