import asyncio

import uvicorn
from fastapi import FastAPI
import logging

from main_bot_iaogram.handlers_aiogram import main_aiogram_router
from main_bot_iaogram.main_aiogramm_bot import main_aiogram_bot

# from db.config import engine, Base
# from routers import book_router

from fastapi import APIRouter, Depends

from contextlib import asynccontextmanager

from proxy_telethron.main_telethron_bot import main_telethron_bot
from routers_fastAPI import root_router


@asynccontextmanager
async def lifespan1(application: FastAPI):
    logging.info("🚀 asyncio.gather")
    # from main_bot_iaogram.main_aiogramm_bot import main_aiogram_bot
    # await main_aiogram_bot()

    await asyncio.gather(main_telethron_bot(), main_aiogram_bot())
    yield
    logging.info("⛔ Stopping asyncio.gather")



def start():
    app = FastAPI(lifespan=lifespan1)
    app.include_router(root_router)
    # app.include_router(main_aiogram_router)

    # @app.get("/")
    # def home():
    #     return {"Hello": "World"}

    return app


def main():
    uvicorn.run(
        "main:start",
        workers=1,
        factory=True,
        host="localhost",
        port=8088,
        log_level="debug",
    )

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                        level=logging.INFO)
    main()

