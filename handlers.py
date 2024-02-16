import asyncio
from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')

from aiogram import types, F, Router, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
BOT_TOKEN = getenv('BOT_TOKEN')

from telethon import TelegramClient, sync, events
telethron_chat_for_exchenge_with_china = getenv('telethron_chat_for_exchenge_with_china')
telethon_api_id = getenv('telethon_api_id')
telethon_api_hash = getenv('telethon_api_hash')

env_china_bot_id = getenv('env_china_bot_id')

from database import add_new_user, db_new_cashe_user_message_id, cache_or_db_check_replay_messege_id, db_check_cache_replay_messege_id
from neuroThings import add_user_messege_and_run

from keyBoards import mainMenu, openAIpoll



router = Router()

async def send_msg_to_china(message, user_chat_id, user_message_id):
    client = TelegramClient('.venv/session_name.session', telethon_api_id, telethon_api_hash)
    await client.start()
    # print("send_msg_to_china + user_chat_id " + str(user_chat_id))
    # await asyncio.sleep(1)

    message = "@neuro44fz_bot " + message
    # print("Сча будем засылать в чат: " + str(telethron_chat_for_exchenge_with_china))

    send_message_to_china = await client.send_message(telethron_chat_for_exchenge_with_china, message)
    # print(send_message_to_china)
    proxy_messege_id = send_message_to_china.to_dict()["id"]

    # print("Сообщение отправили, сча будет кешью сохранять его id:" + str(proxy_messege_id))

    db_new_cashe_user_message_id(user_chat_id=user_chat_id,
                                 user_message_id=user_message_id,
                                 proxy_messege_id=proxy_messege_id)

    # db_add_to_cache_proxy_messege_id(user_chat_and_massage_id, proxy_messege_id)

    client.disconnect()

    # return id_message_to_china
    # for dialog in client.iter_dialogs():
    #     print(dialog)


async def send_response_from_bot_to_user(user_chat_id, message_text, reply_to_msg_id):
    print("send_response_from_bot_to_user")
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    print("chat_id=" + str(user_chat_id) + ", text=" + str(message_text) + ", reply_to_message_id=" + str(reply_to_msg_id))

    await bot.send_message(chat_id=user_chat_id, text=message_text, reply_to_message_id=reply_to_msg_id)
    await bot.close()


send_response_from_bot_to_user(user_chat_id="243697626", message_text="Кажется, вы ввели некорректную команду или запрос. Пожалуйста, уточните ваш вопрос",reply_to_msg_id="503")

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


@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()









@router.message()
async def message_handler(message: Message):
    # Пока основная точка входа в бота, потом надо поменять
    # user_chat_and_massage_id = str(message.chat.id) + str(message.message_id)
    # print("ПОЛучили сообщение, погнали")
    await send_msg_to_china(message=message.text,
                            user_chat_id=message.chat.id,
                            user_message_id=message.message_id)


    #
    # print(message.chat.id)
    print("user_message_id" + str(message.message_id))
    print(message)




    # user_id = message.from_user.id
    # thread_id = "thread_tjXAUQjpkW5E824feP25CIlR"
    # if thread_id: # Убедились, что доступ есть.
    #     # print(thread_id, message.text)
    #     responce_from_openAI = add_user_messege_and_run(thread_id, message.text)
    #     await message.reply(responce_from_openAI, reply_markup=openAIpoll)
    # else:
    #     await message.answer("На сегодня бесплатные запросы закончились. Приходите завтра или оплатите подписку",
    #                          reply_markup=mainMenu)







#________________Ручки тг клиента


# @events.NewMessage()
# async def my_event_handler(event):
#     print("hello666")


@events.register(events.NewMessage(from_users=env_china_bot_id, chats=telethron_chat_for_exchenge_with_china))  # chats=telethron_chat_for_exchenge_with_china
async def i_see_response_handler(event):
    # print("i_see_response_handler")
    message_to_dict = event.message.to_dict()
    # channel_id = message_to_dict["peer_id"]
    user_id = message_to_dict["from_id"]["user_id"] # Сделать проверку. чтобы только бота читать
    # print(user_id)
    # print(message_to_dict)
    if True:

        reply_to_msg_id = message_to_dict['reply_to']['reply_to_msg_id']
        message_text = message_to_dict["message"]
        message_id = message_to_dict["id"]
        # print(channel_id)

        # Сбегать в базу с кешем проверить его reply_to_msg_id
        msg_id_dict = db_check_cache_replay_messege_id(reply_to_msg_id)
        user_chat_id = msg_id_dict["user_chat_id"]
        user_message_id = msg_id_dict["user_message_id"]
        await send_response_from_bot_to_user(user_chat_id=user_chat_id,
                                       message_text=message_text,
                                       reply_to_msg_id=user_message_id)
        # print(msg_id_dict)


    # Ответить в боте

    # print(arr['message'])   #.message.to_dict()['message']

    # print(arr[0])   #.message.to_dict()['message']


@events.register(events.MessageEdited())
async def i_see_edits_handler(event):
    arr = event.message.to_dict()
    print(arr)
    print(arr['message'])   #.message.to_dict()['message']
    # print(arr[0])   #.message.to_dict()['message']


# @events.register(events.NewMessage(chats=('v_karpyuk')))
# async def start_go_test_handler(event):
#     if str(event.message.to_dict()['message']).startswith("Го") or str(event.message.to_dict()['message']).startswith("Uj"):
#         print("Погнали")
#         # client = event.client
#         await send_msg_to_china( "Что такое обеспечение заявки") # client,
#
#         # send_message_to_china = await client.send_message('neuro44fz_bot', 'Что такое обеспечение контракта?')
#         # id_message_to_china = send_message_to_china.to_dict()["id"]
#         # print(send_message_to_china.to_dict()["id"])
#
#         pass


@events.register(events.NewMessage())
async def handler_test(event):
    client = event.client
    await event.respond('Hey!')
    await client.send_message('me', 'I said hello to someone')

