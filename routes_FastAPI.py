from typing import Annotated

from fastapi import APIRouter, Header
from loguru import logger
from aiogram import types

from main_aiogramm_bot import bot, dp


from os import getenv
from dotenv import load_dotenv

load_dotenv('.venv/.env')
env_main_tg_bot_token = getenv('env_main_tg_bot_token')


base_webhook_url = 'https://b775-112-134-147-111.ngrok-free.app'

webhook_path = "/webhook"

root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}



