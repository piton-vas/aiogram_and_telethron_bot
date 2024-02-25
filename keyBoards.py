from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

mainMenu = [
    [InlineKeyboardButton(text="Попробовать free", callback_data="try_free"),
    InlineKeyboardButton(text="Профиль", callback_data="profile")],
]
mainMenu = InlineKeyboardMarkup(inline_keyboard=mainMenu)


gpt_response_poll = [
    [   InlineKeyboardButton(text="🔥 Отличный ответ", callback_data="poll_good"),
        InlineKeyboardButton(text="🙅‍♂️ Совсем не то", callback_data="poll_bad"),
        InlineKeyboardButton(text="📝 Дать обратную связь", callback_data="give_feedback"),
        InlineKeyboardButton(text="⛔️ Астанавитесь", callback_data="stop")
     ],
]
gpt_response_poll = InlineKeyboardMarkup(inline_keyboard=gpt_response_poll)



