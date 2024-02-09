from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

mainMenu = [
    [InlineKeyboardButton(text="Попробовать free", callback_data="generate_text"),
    InlineKeyboardButton(text="Подписка", callback_data="generate_image")],
]
mainMenu = InlineKeyboardMarkup(inline_keyboard=mainMenu)


openAIpoll = [
    [   InlineKeyboardButton(text="🔥 Отличный ответ", callback_data="poll_good"),
        InlineKeyboardButton(text="🙅‍♂️ Совсем не то", callback_data="poll_bad"),
        InlineKeyboardButton(text="📝 Дать обратную связь", callback_data="give_feedback"),
        InlineKeyboardButton(text="⛔️ Астанавитесь", callback_data="stop")
     ],
]
openAIpoll = InlineKeyboardMarkup(inline_keyboard=openAIpoll)
