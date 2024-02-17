from os import getenv
import logging
from dotenv import load_dotenv
load_dotenv('../.venv/.env')

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
env_main_tg_bot_token = getenv('env_main_tg_bot_token')

from keyBoards import mainMenu
from handlers.handlers_telethon import send_msg_to_coze_bot_via_tg
from database import add_new_user


# TODO: Вот этот запрос бы прикрутить к готовеньким bot, Dispatcher
async def send_response_from_bot_to_user(user_chat_id, message_text, reply_to_msg_id):
    # print("send_response_from_bot_to_user")
    bot = Bot(token=env_main_tg_bot_token,
              parse_mode=ParseMode.HTML)
    # dp = Dispatcher(storage=MemoryStorage())

    await bot.send_message(chat_id=user_chat_id,
                           text=message_text,
                           reply_to_message_id=reply_to_msg_id)


    #TODO Как логи то нормально сделать в асинхр?
    # await logging.INFO(f"send_response_from_bot_to_user. We have resend response from coze_bot to user")
    await bot.close()

#________________ Стандартные ручки aiogram

router = Router()
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет, путник, это Помошник Нейроконсультант", reply_markup=mainMenu)
    add_new_user(message.from_user.id, message.from_user.full_name)

@router.message(Command("neuroZakupki_bot", prefix="@"))
async def cmd_custom1(message: Message):
    await message.reply("Вижу команду!")


@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()


@router.message()
async def message_handler(message: Message):

    # Пока основная точка входа в бота, потом надо поменять
    await send_msg_to_coze_bot_via_tg(message=message.text,
                                      user_chat_id=message.chat.id,
                                      user_message_id=message.message_id)
