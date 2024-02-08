from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import keyBoards
from keyBoards import mainMenu


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет, путник, это Помошник Нейроконсультант", reply_markup=keyBoards.mainMenu)


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
    await message.reply(f"Твой ID: {message.from_user.id}")
