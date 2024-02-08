from aiogram import Bot, Dispatcher
import env.config
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

#
# bot = Bot(token=env.config.BOT_TOKEN, parse_mode=ParseMode.HTML)
# dp = Dispatcher(storage=MemoryStorage())