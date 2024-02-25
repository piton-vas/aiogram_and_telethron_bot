import logging
from os import getenv
from pprint import pprint

from dotenv import load_dotenv

load_dotenv('.venv/.env')
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message

import loader as ld

env_main_tg_bot_token = getenv('env_main_tg_bot_token')
env_chat_for_exchenge_with_coze_bot_id = getenv('env_chat_for_exchenge_with_coze_bot_id')


from fsm import UserState
from keyBoards import mainMenu
from proxy_telethron.handlers_telethon import send_msg_to_coze_bot_via_tg



# TODO: Вот этот запрос бы прикрутить к готовеньким bot, Dispatcher
async def send_response_from_bot_to_user(user_chat_id, message_text):
    await ld.bot.send_message(chat_id=user_chat_id,
                           text=message_text)

#________________ Стандартные ручки aiogram

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: UserState):

    await message.answer("Привет, путник, сейчас мы будем общаться с другим ботом", reply_markup=mainMenu)


@router.message(Command("go"))
async def go_handler(message: Message):
    message_text = message.text[3:]    # Убираем команду /go
    logging.info(f"go_handler. We have new message from user: {message_text}")
    await send_msg_to_coze_bot_via_tg(message=message_text,
                                      user_chat_id=message.chat.id,
                                      user_message_id=message.message_id)




@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()
