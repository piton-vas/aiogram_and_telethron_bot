import logging
from os import getenv
from dotenv import load_dotenv
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
import loader as ld

from fsm import UserState
from keyBoards import mainMenu, gpt_response_poll
from local_cache import memory_check_cache_replay_message_id, memory_dict_update_replay_message_id
from proxy_telethron.handlers_telethon import send_msg_to_3th_party_bot_via_tg

load_dotenv('.venv/.env')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')

# Произошло внешнее событие (Telethron увидел сообщение от стороннего бота) Можно переслать нашему юзеру
async def send_response_from_bot_to_user(reply_to_msg_id, message_text):
    cache_dict = memory_check_cache_replay_message_id(reply_to_msg_id)
    replay_massage_id = cache_dict["user_message_id"]
    user_chat_id = cache_dict["user_chat_id"]
    bot_replay_message = await ld.bot.send_message(chat_id=user_chat_id,
                                                   text=message_text,
                                                   reply_to_message_id=replay_massage_id,
                                                   reply_markup=gpt_response_poll)
    replay_bot_message_id = bot_replay_message.message_id
    memory_dict_update_replay_message_id(proxy_message_id=reply_to_msg_id,
                                         replay_bot_message_id=replay_bot_message_id)

# Произошло внешнее событие (Telethron увидел изменения сообщения от стороннего бота) Можно переслать изменения нашему юзеру
async def edit_response_from_bot_to_user(replay_massage_id, message_text):
    cache_dict = memory_check_cache_replay_message_id(replay_massage_id)
    user_chat_id = cache_dict["user_chat_id"]
    replay_bot_message_id = cache_dict["replay_bot_message_id"]
    if replay_bot_message_id:
        await ld.bot.edit_message_text(chat_id=user_chat_id,
                                       message_id=replay_bot_message_id,
                                       text=message_text,
                                       reply_markup=gpt_response_poll)

# Стандартные ручки аиограмм бота
router = Router()

# Обычная команда старт
@router.message(Command("start"))
async def start_handler(message: Message, state: UserState):
    await message.answer("Привет, путник, сейчас мы будем общаться с другим ботом", reply_markup=mainMenu)

# Временная ручка Го, для теста (работает и в личке и в групповом чате)
@router.message(Command("go"))
async def go_handler(message: Message):
    message_text = message.text[3:]    # Убираем команду /go
    logging.info(f"go_handler. We have new message from user: {message_text}")
    await send_msg_to_3th_party_bot_via_tg(message=message_text,
                                           user_chat_id=message.chat.id,
                                           user_message_id=message.message_id)


# Еще одна ручка на всякий случай
@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь")
    await callback.answer()
