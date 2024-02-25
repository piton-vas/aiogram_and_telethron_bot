import logging
from os import getenv
from dotenv import load_dotenv
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
import loader as ld

from fsm import UserState
from keyBoards import mainMenu
from local_cache import memory_check_cache_replay_message_id, memory_dict_update_replay_message_id
from proxy_telethron.handlers_telethon import send_msg_to_3th_party_bot_via_tg


load_dotenv('.venv/.env')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')
env_chat_for_exchenge_with_coze_bot_id = getenv('env_chat_for_exchenge_with_coze_bot_id')

async def send_response_from_bot_to_user(reply_to_msg_id, message_text):
    print("send_response_from_bot_to_user reply_to_msg_id: " + str(reply_to_msg_id))
    cache_dict = memory_check_cache_replay_message_id(reply_to_msg_id)

    replay_massage_id = cache_dict["user_message_id"]
    bot_replay_message = await ld.bot.send_message(chat_id=cache_dict["user_chat_id"],
                                                   text=message_text,
                                                   reply_to_message_id=replay_massage_id)
    replay_bot_message_id = bot_replay_message.message_id
    memory_dict_update_replay_message_id(proxy_message_id=reply_to_msg_id,
                                         replay_bot_message_id=replay_bot_message_id)


async def edit_response_from_bot_to_user(replay_massage_id, message_text):
    cache_dict = memory_check_cache_replay_message_id(replay_massage_id)
    print(replay_massage_id)
    print(cache_dict)
    user_chat_id = cache_dict["user_chat_id"]
    replay_bot_message_id = cache_dict["replay_bot_message_id"]
    if replay_bot_message_id:
        await ld.bot.edit_message_text(chat_id=user_chat_id,
                                       message_id=replay_bot_message_id,
                                       text=message_text)




router = Router()
@router.message(Command("start"))
async def start_handler(message: Message, state: UserState):

    await message.answer("Привет, путник, сейчас мы будем общаться с другим ботом", reply_markup=mainMenu)


@router.message(Command("go"))
async def go_handler(message: Message):
    message_text = message.text[3:]    # Убираем команду /go
    logging.info(f"go_handler. We have new message from user: {message_text}")
    await send_msg_to_3th_party_bot_via_tg(message=message_text,
                                           user_chat_id=message.chat.id,
                                           user_message_id=message.message_id)




@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()
