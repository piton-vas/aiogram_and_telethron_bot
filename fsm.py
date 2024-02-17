from aiogram.fsm.state import State, StatesGroup

# from aiogram import Bot, Dispatcher #, executor, types
# # from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.fsm.context import FSMContext
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class UserState(StatesGroup):
    #  Состояния пользователей 
    NEW = State()
    FREE_TRIAL = State()
    PAYED = State()
    ADMIN = State()
