from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

mainMenu = [
    [InlineKeyboardButton(text="Попробовать free", callback_data="generate_text"),
    InlineKeyboardButton(text="Подписка", callback_data="generate_image")],
]
mainMenu = InlineKeyboardMarkup(inline_keyboard=mainMenu)

