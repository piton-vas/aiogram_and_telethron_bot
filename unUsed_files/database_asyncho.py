import asyncio
import aiomysql
from os import getenv
from dotenv import load_dotenv
load_dotenv('../.venv/.env')
env_db_host = getenv('env_db_host')
env_db_username = getenv('env_db_username')
env_db_pass = getenv('env_db_pass')
env_db_name = getenv('env_db_name')


# async def select(loop, sql, pool):
#     async with pool.acquire() as conn:
#         async with conn.cursor() as cur:
#             await cur.execute(sql)
#             r = await cur.fetchone()
#             print(r)


async def db_asynch_add_to_cashe_user_massage_id_2(user_chat_id, user_massage_id, pool):
    user_chat_and_massage_id = str(user_chat_id) + str(user_massage_id)
    sql = f"""INSERT INTO `messege_id_cashe`(
                    `user_chat_and_massage_id`,
                    `china_message_id`,
                    `bot_message_id`,
                    `reply_to_id`,
                    `user_chat_id`
                )
                VALUES('{user_chat_and_massage_id}', NULL, NULL, NULL, NULL)"""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            await conn.commit()


async def main(loop):
    pool = await aiomysql.create_pool(host=env_db_host, port=3306,
                                      user=env_db_username, password=env_db_pass,
                                      db=env_db_name, loop=loop)

    c2 = db_asynch_add_to_cashe_user_massage_id_2(user_chat_id=12345, user_massage_id=456, pool=pool)

    tasks = [asyncio.ensure_future(c2)]
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    cur_loop = asyncio.get_event_loop()
    cur_loop.run_until_complete(main(cur_loop))




#
# async def db_asynch_add_to_cashe_user_massage_id(user_chat_id, user_massage_id):
#     conn = await aiomysql.connect(host=db_host, port=3306,
#                                        user=db_username, password=db_pass,
#                                        db=db_name, loop=loop)
#     cur = await conn.cursor()
#     async with conn.cursor() as cur:
#         user_chat_and_massage_id = (user_chat_id + "_" + user_massage_id)
#         await cur.execute("INSERT INTO messege_id_cashe (user_chat_and_massage_id) VALUES " + user_chat_and_massage_id)
#         await conn.commit()
#
#         #
#         # await cur.execute("""CREATE TABLE music_style
#         #                           (id INT,
#         #                           name VARCHAR(255),
#         #                           PRIMARY KEY (id));""")
#         #
#         # # insert 3 rows one by one
#         # await cur.execute("INSERT INTO music_style VALUES(1,'heavy metal')")
#         # await cur.execute("INSERT INTO music_style VALUES(2,'death metal');")
#         # await cur.execute("INSERT INTO music_style VALUES(3,'power metal');")
#         # await conn.commit()
#
#         # insert 3 row by one long query using *executemany* method
#         # data = [(4, 'gothic metal'), (5, 'doom metal'), (6, 'post metal')]
#         # await cur.executemany(
#         #     "INSERT INTO music_style (id, name)"
#         #     "values (%s,%s)", data)
#         # await conn.commit()
#         #
#         # # fetch all insert row from table music_style
#         # await cur.execute("SELECT * FROM music_style;")
#         result = await cur.fetchall()
#         print(result)
#
#     conn.close()
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(db_asynch_add_to_cashe_user_massage_id(loop))



