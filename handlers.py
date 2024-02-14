from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import database
from database import add_new_user
from neuroThings import add_user_messege_and_run

import keyBoards
# from keyBoards import mainMenu


router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет, путник, это Помошник Нейроконсультант", reply_markup=keyBoards.mainMenu)
    add_new_user(message.from_user.id, message.from_user.full_name)

@router.message(Command("neuroZakupki_bot", prefix="@"))
async def cmd_custom1(message: Message):
    await message.reply("Вижу команду!")

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    await message.reply("Профиль")

@router.message(F.text == "Меню")
async def menu(message: Message):
    await message.answer('Привет, вот меню', reply_markup=keyBoards.mainMenu)

# Отвечать openAI
@router.message()
async def message_handler(message: Message):
    user_id = message.from_user.id
    thread_id = "thread_tjXAUQjpkW5E824feP25CIlR"
    if thread_id: # Убедились, что доступ есть.
        # print(thread_id, message.text)
        responce_from_openAI = add_user_messege_and_run(thread_id, message.text)
        await message.reply(responce_from_openAI, reply_markup=keyBoards.openAIpoll)
    else:
        await message.answer("На сегодня бесплатные запросы закончились. Приходите завтра или оплатите подписку",
                             reply_markup=keyBoards.mainMenu)

@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()


# @router.callback_query(F.data == "profile")
# async def send_random_value(callback: types.CallbackQuery):
#     await callback.message.answer("А здесь у нас будет про баланс и вообще личный кабинет", reply_markup=keyBoards.profile_menu)
#     await callback.answer()
#
# @router.callback_query(F.data == "profile")
# async def send_random_value(callback: types.CallbackQuery):
#     await callback.message.answer("А здесь у нас будет про баланс и вообще личный кабинет", reply_markup=keyBoards.profile_menu)
#     await callback.answer()
#
# china_proxy_router = Router()
#
# @china_proxy_router.message(Command("listen_china_bot", prefix="@"))
# async def cmd_custom1(message: Message):
#     await message.answer("@neuro44fz_bot Что такое обеспечение контракта?")
#
# @china_proxy_router.message()
# async def echo(message: types.Message):
#     print(message)
# # async def message_handler(message: Message):
# #     user_id = message.from_user.id
# #
# #     responce = "Ответ " + str(user_id)
# #     await message.reply(responce)


#Ручки тг клиента

from telethon import TelegramClient, sync, events
import asyncio

async def send_msg_to_china(client, messege ):
    messege = "@neuro44fz_bot " + messege
    send_message_to_china = await client.send_message('NeuroBot2NeuroBot', messege)
    id_message_to_china = send_message_to_china.to_dict()["id"]
    print("Сообщение отправили, его id:" + str(id_message_to_china))
    return id_message_to_china

@events.register(events.MessageEdited(chats=('neuro44fz_bot')))
async def edits_handler(event):
    arr = event.message.to_dict()
    print(arr)
    print(arr['message'])   #.message.to_dict()['message']
    # print(arr[0])   #.message.to_dict()['message']

@events.register(events.NewMessage(chats=('neuro44fz_bot')))
async def i_see_response_handler(event):
    arr = event.message.to_dict()
    print(arr)
    print(arr['message'])   #.message.to_dict()['message']

    # print(arr[0])   #.message.to_dict()['message']


@events.register(events.NewMessage(chats=('v_karpyuk')))
async def normal_handler(event):
    if str(event.message.to_dict()['message']).startswith("Го") or str(event.message.to_dict()['message']).startswith("Uj"):
        print("Погнали")
        client = event.client
        await send_msg_to_china(client, "Что такое обеспечение заявки")

        # send_message_to_china = await client.send_message('neuro44fz_bot', 'Что такое обеспечение контракта?')
        # id_message_to_china = send_message_to_china.to_dict()["id"]
        # print(send_message_to_china.to_dict()["id"])

        pass


