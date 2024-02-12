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
        await message.reply(f"Ответ ОпенАИ: {responce_from_openAI}", reply_markup=keyBoards.openAIpoll)
    else:
        await message.answer("На сегодня бесплатные запросы закончились. Приходите завтра или оплатите подписку",
                             reply_markup=keyBoards.mainMenu)

@router.callback_query(F.data == "try_free")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Спроси меня что-нибудь про законы о закупках")
    await callback.answer()


@router.callback_query(F.data == "profile")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("А здесь у нас будет про баланс и вообще личный кабинет", reply_markup=keyBoards.profile_menu)
    await callback.answer()