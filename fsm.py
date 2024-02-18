from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    #  Состояния пользователей 
    NEW = State()
    FREE_TRIAL = State()
    PAYED = State()
    ADMIN = State()
