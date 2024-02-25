from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from telethon import TelegramClient

from MySQLStorage import MySQLStorage
from main_bot_iaogram.handlers_aiogram import router
from proxy_telethron.handlers_telethon import i_see_response_handler, i_see_edits_handler

load_dotenv('.venv/.env')
env_telethon_session = getenv('env_telethon_session')
env_telethon_api_id = getenv('env_telethon_api_id')
env_telethon_api_hash = getenv('env_telethon_api_hash')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')
env_server_mode = getenv('env_server_mode')
env_db_name = getenv('env_db_name')
env_db_username = getenv('env_db_username')
env_db_pass = getenv('env_db_pass')
env_db_host = getenv('env_db_host')

# В этом глобальном словаре хранятся айдишники сообщений, чтобы бот мог к правильному сообщению отвечать
memory_msgs_ids_dict = dict()

# Создаем бота и диспетчера Иаограмм, чтобы потом ими пользоваться везде
bot = Bot(token=env_main_tg_bot_token,
          parse_mode=ParseMode.HTML)

# Для локального запуска без базы данных
if env_server_mode == "PROD":
    aiogram_storage = MySQLStorage(host=env_db_host,
                                   user=env_db_username,
                                   password=env_db_pass,
                                   database=env_db_name)
elif env_server_mode == "TEST":
    aiogram_storage = MemoryStorage()

dp = Dispatcher(storage=aiogram_storage)

# Создаем клиента telethron, чтобы потом ими пользоваться везде
client_telethron = TelegramClient(session=env_telethon_session,
                                  api_id=int(env_telethon_api_id),
                                  api_hash=env_telethon_api_hash)

# Асинхронная функция для запуска главного бота
async def main_aiogram_bot():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

# Асинхронная функция для запуска бота Telethron, который будет общаться с другим ботом
async def main_telethron_bot():
    client_telethron.add_event_handler(i_see_response_handler)
    client_telethron.add_event_handler(i_see_edits_handler)
    await client_telethron.start()
    try:
        await client_telethron.run_until_disconnected()
    finally:
        await client_telethron.disconnect()
