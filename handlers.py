from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from telethon import TelegramClient, sync, events
telethron_chat_for_exchenge_with_china = getenv('telethron_chat_for_exchenge_with_china')
telethon_api_id = getenv('telethon_api_id')
telethon_api_hash = getenv('telethon_api_hash')

from database import add_new_user, db_add_to_cashe_user_massage_id
from neuroThings import add_user_messege_and_run

from keyBoards import mainMenu, openAIpoll



router = Router()

async def send_msg_to_china(message, user_chat_and_massage_id):
    print("сча отправим " + message)
    client = TelegramClient('.venv/session_name', telethon_api_id, telethon_api_hash)
    await client.start()
    message = "@neuro44fz_bot " + message
    # print("Сча будем засылать в чат: " + str(telethron_chat_for_exchenge_with_china))
    send_message_to_china = await client.send_message(telethron_chat_for_exchenge_with_china, message)
    print(send_message_to_china)
    id_message_to_china = send_message_to_china.to_dict()["id"]
    print("Сообщение отправили, его id:" + str(id_message_to_china))
    # client.disconnect()

    # return id_message_to_china
    # for dialog in client.iter_dialogs():
    #     print(dialog)

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет, путник, это Помошник Нейроконсультант", reply_markup=mainMenu)
    add_new_user(message.from_user.id, message.from_user.full_name)

@router.message(Command("neuroZakupki_bot", prefix="@"))
async def cmd_custom1(message: Message):
    await message.reply("Вижу команду!")

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    await message.reply("Профиль")

@router.message(F.text == "Меню")
async def menu(message: Message):
    await message.answer('Привет, вот меню', reply_markup=mainMenu)


@router.message()
async def message_handler(message: Message):

    user_chat_and_massage_id = str(message.chat.id) + str(message.message_id)

    print(message.chat.id)
    print(message.message_id)

    await send_msg_to_china(message.text, user_chat_and_massage_id)

    db_add_to_cashe_user_massage_id(message.chat.id, message.message_id)

    # user_id = message.from_user.id
    # thread_id = "thread_tjXAUQjpkW5E824feP25CIlR"
    # if thread_id: # Убедились, что доступ есть.
    #     # print(thread_id, message.text)
    #     responce_from_openAI = add_user_messege_and_run(thread_id, message.text)
    #     await message.reply(responce_from_openAI, reply_markup=openAIpoll)
    # else:
    #     await message.answer("На сегодня бесплатные запросы закончились. Приходите завтра или оплатите подписку",
    #                          reply_markup=mainMenu)







#Ручки тг клиента


@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()

@events.register(events.MessageEdited(chats=telethron_chat_for_exchenge_with_china))
async def i_see_edits_handler(event):
    arr = event.message.to_dict()
    print(arr)
    print(arr['message'])   #.message.to_dict()['message']
    # print(arr[0])   #.message.to_dict()['message']

@events.register(events.NewMessage(chats=telethron_chat_for_exchenge_with_china))
async def i_see_response_handler(event):
    arr = event.message.to_dict()
    print(arr)
    print(arr['message'])   #.message.to_dict()['message']

    # print(arr[0])   #.message.to_dict()['message']


@events.register(events.NewMessage(chats=('v_karpyuk')))
async def start_go_test_handler(event):
    if str(event.message.to_dict()['message']).startswith("Го") or str(event.message.to_dict()['message']).startswith("Uj"):
        print("Погнали")
        # client = event.client
        await send_msg_to_china( "Что такое обеспечение заявки") # client,

        # send_message_to_china = await client.send_message('neuro44fz_bot', 'Что такое обеспечение контракта?')
        # id_message_to_china = send_message_to_china.to_dict()["id"]
        # print(send_message_to_china.to_dict()["id"])

        pass


