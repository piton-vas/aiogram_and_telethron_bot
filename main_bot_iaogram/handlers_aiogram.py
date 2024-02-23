import logging
from os import getenv
from pprint import pprint
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
load_dotenv('.venv/.env')

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

# from aiogram.fsm.context import FSMContext
env_main_tg_bot_token = getenv('env_main_tg_bot_token')
env_chat_for_exchenge_with_coze_bot_id = getenv('env_chat_for_exchenge_with_coze_bot_id')


from fsm import UserState
from keyBoards import mainMenu
from proxy_telethron.handlers_telethon import send_msg_to_coze_bot_via_tg
# from local_cache import memory_dict


# TODO: Вот этот запрос бы прикрутить к готовеньким bot, Dispatcher
async def send_response_from_bot_to_user(user_chat_id, message_text):
    print("send_response_from_bot_to_user - Отправка ботом ответа, Но пока pass")
    pass
    bot = Bot(token=env_main_tg_bot_token,
              parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    await bot.send_message(chat_id=user_chat_id,
                           text=message_text)

    # await bot.close()

#________________ Стандартные ручки aiogram

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: UserState):

    await message.answer("Привет, путник, это Помошник Нейроконсультант", reply_markup=mainMenu)


@router.message(Command("go"))
async def go_handler(message: Message):
    message_text = message.text[3:]    # Убираем команду /go
    logging.info(f"go_handler. We have new message from user: {message_text}")
    await send_msg_to_coze_bot_via_tg(message=message_text,
                                      user_chat_id=message.chat.id,
                                      user_message_id=message.message_id)


@router.message(Command("neuroZakupki_bot", prefix="@"))
async def cmd_custom1(message: Message):
    await message.reply("Вижу команду!")


@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()





@router.message()
async def message_handler(message: Message):

    if message.from_user.id != 6927113111:
        logging.info(f"message_handler. We have new message from user: {message.text}")
        # await send_msg_to_coze_bot_via_tg(message=message.text,
        #                                   user_chat_id=message.chat.id,
        #                                   user_message_id=message.message_id)
