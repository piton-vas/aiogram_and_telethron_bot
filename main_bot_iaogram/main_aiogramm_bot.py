from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from main_bot_iaogram.handlers_aiogram import main_aiogram_router

load_dotenv('venv/.env_sending')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')



async def main_aiogram_bot():


    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_aiogram_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def send_response_from_bot_to_user(user_chat_id, message_text, reply_to_msg_id):
    # print("send_response_from_bot_to_user")
    # dp = Dispatcher(storage=MemoryStorage())

    await bot.send_message(chat_id=user_chat_id,
                           text=message_text,
                           reply_to_message_id=reply_to_msg_id)


    #TODO Как логи то нормально сделать в асинхр?
    # await logging.INFO(f"send_response_from_bot_to_user. We have resend response from coze_bot to user")
    await bot.close()
