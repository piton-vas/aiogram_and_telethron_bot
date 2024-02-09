from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

mainMenu = [
    [InlineKeyboardButton(text="Попробовать free", callback_data="try_free"),
    InlineKeyboardButton(text="Профиль", callback_data="profile")],
]
mainMenu = InlineKeyboardMarkup(inline_keyboard=mainMenu)


openAIpoll = [
    [   InlineKeyboardButton(text="🔥 Отличный ответ", callback_data="poll_good"),
        InlineKeyboardButton(text="🙅‍♂️ Совсем не то", callback_data="poll_bad"),
        InlineKeyboardButton(text="📝 Дать обратную связь", callback_data="give_feedback")
        # InlineKeyboardButton(text="⛔️ Астанавитесь", callback_data="stop") Включить когда будет поэтапный вывод
     ],
]
openAIpoll = InlineKeyboardMarkup(inline_keyboard=openAIpoll)


profile_menu = [
    [InlineKeyboardButton(text="Ввести промо-код", callback_data="enter_promo"),
    InlineKeyboardButton(text="Оформить подписку", callback_data="subscribe")],
]
profile_menu = InlineKeyboardMarkup(inline_keyboard=profile_menu)
