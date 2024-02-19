import asyncio

from fastapi import FastAPI
import logging

from main_aiogramm_bot import main_aiogram_bot

# from db.config import engine, Base
# from routers import book_router

from fastapi import APIRouter, Depends


app = FastAPI()
router = APIRouter()

app.include_router(router)


# @app.on_event("startup")
# async def startup():
#     print('event("startup")')
#     # create db tables
#     pass
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    print("__main__")
    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                        level=logging.INFO)
    asyncio.run(main_aiogram_bot())
    # uvicorn.run("app:app", port=1111, host='127.0.0.1')
