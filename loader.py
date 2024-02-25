from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv('.venv/.env')

env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')

client_telethron = TelegramClient(session="session_name2.session",
                                      api_id=int(env_telethon_api_id),
                                      api_hash=env_telethon_api_hash)

bot = Bot(token=env_main_tg_bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
