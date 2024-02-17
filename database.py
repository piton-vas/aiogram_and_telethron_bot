import logging
logging.basicConfig(level=logging.INFO)  # Отключить после дебага

import mysql.connector
from mysql.connector import Error
from os import getenv
from dotenv import load_dotenv
load_dotenv('.venv/.env')
env_db_host = getenv('env_db_host')
env_db_username = getenv('env_db_username')
env_db_pass = getenv('env_db_pass')
env_db_name = getenv('env_db_name')

from functools import lru_cache

from datetime import datetime
from dateutil.relativedelta import relativedelta


def mydbConnection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=env_db_host,
            user=env_db_username,
            passwd=env_db_pass,
            database=env_db_name)
    except Error as e:
        logging.error(f"The error '{e}' occurred")

    return connection

def add_new_user(user_id, user_name):
    connection = mydbConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from users WHERE user_id='{user_id}'")
    if cursor.fetchall():  # checking if something found with this username
        logging.info('User_id:' + str(user_id) + ' already exists. His user_name is:' + user_name)
    else:
        sql = "INSERT INTO users (user_id, user_name, subscribe_until, count_request) VALUES (%s, %s, %s, %s)"
        val = (user_id, user_name, datetime.now().date(), 0)
        cursor.execute(sql, val)
        connection.commit()
        logging.info('New user has been registred, iser_id:' + str(user_id) + ' User_name:' + user_name)

def check_user_status(user_id, user_name=''):
    connection = mydbConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id, status from users WHERE user_id='{user_id}'")
    myresult = cursor.fetchall()
    return myresult[0][1]

def new_free_day(user_id, connection):
    cursor = connection.cursor()
    sql = f"""UPDATE users
            SET subscribe_until='{datetime.now().date()}',
                count_request=1
            WHERE user_id='{user_id}'"""
    try:
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        logging.error(f"DB append failed! new_free_day '{e}'new_free_day'")
        connection.rollback()

def new_try_counter(user_id, connection):
    cursor = connection.cursor()
    sql = f"""UPDATE users
            SET count_request = count_request + 1
            WHERE user_id='{user_id}'"""
    try:
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        logging.error(f"DB append failed! new_try_counter '{e}' ")
        connection.rollback()

def change_user_status_to_free(user_id, connection):
    cursor = connection.cursor()
    sql = f"""UPDATE users
            SET status = 'free',
            count_request = 1,
            subscribe_until='{datetime.now().date()}'
            WHERE user_id='{user_id}'"""
    try:
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        logging.error(f"DB append failed! change_user_status_to_free '{e}'")
        connection.rollback()

def can_user_make_openAI_request(user_id):
    return True
    connection = mydbConnection()
    cursor = connection.cursor()
    sql = f"SELECT user_id, status, subscribe_until, count_request, thread_id from users WHERE user_id='{user_id}'"
    cursor.execute(sql)
    myresult = cursor.fetchall()[0]
    status = myresult[1]
    subscribe_until = myresult[2]
    count_request = myresult[3]
    thread_id = myresult[4]

    if status=='admin':
        return True
    elif status=='paid':
        if subscribe_until >= datetime.now().date(): # Если подписка не закончилась
            logging.info("User_id:" + str(user_id) + " payed trying")
            return True, thread_id
        else:                                        # Подписка закончилась, но еще можно бесплатно
            logging.info("User_id:" + str(user_id) + " trying, but subscribe finishing. Free try #1")
            change_user_status_to_free(user_id, connection)
            return True, thread_id
    elif status=='free':
        if subscribe_until < datetime.now().date():  # Если сегодня не было попыток, снова бесплатные запросы
            new_free_day(user_id, connection)
            logging.info("User_id:" + str(user_id) + " obnulil his free days, Free try#1")
            return True, thread_id
        else:                                        # Попытки сегодня были уже. Сча будем считать их
            if count_request < count_request_maximum_free: # Бесплатных попыток хватает,
                new_try_counter(user_id, connection)
                logging.info("User_id:" + str(user_id) + ". Free try#" + str(count_request+1))
                return True, thread_id
            else:                                     # Бесплатные попытки закончились
                logging.info("User_id:" + str(user_id) + " free try finished")
                return False


    # print(myresult)

def make_one_month_subscribe(user_id):
    connection = mydbConnection()
    cursor = connection.cursor()

    one_month_later = datetime.now() + relativedelta(months=+1)
    str_one_month_later = one_month_later.strftime("%Y-%m-%d")

    sql = f"UPDATE users SET status = 'paid', subscribe_until='{str_one_month_later}' WHERE user_id='{user_id}'"

    try:
        cursor.execute(sql)
        logging.info("One month subscribe, user_id:" + str(user_id))
        connection.commit()
    except Error as e:
        logging.error(f"DB append failed! make_one_month_subscribe '{e}'")
        connection.rollback()

def add_thread_id_to_user(user_id, thread_id):
    connection = mydbConnection()
    cursor = connection.cursor()

    sql = f"UPDATE users SET thread_id='{thread_id}' WHERE user_id='{user_id}'"

    try:
        cursor.execute(sql)
        logging.info("make thread for user_id:" + str(user_id))
        connection.commit()
    except Error as e:
        logging.error(f"DB append failed! add_thread_id_to_user '{e}'" )
        connection.rollback()

def db_add_new_cashe_user_message_id(user_chat_id, user_message_id, proxy_messege_id):
    user_chat_and_massage_id = str(user_chat_id) + str(user_message_id)
    connection = mydbConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from messege_id_cashe WHERE user_chat_and_massage_id={user_chat_and_massage_id}")
    if cursor.fetchall():  # checking if something found with this username
        logging.info(f"messege_id_cashe already exists. user_chat_and_massage_id:'{user_chat_and_massage_id}'")
    else:
        sql = f"""INSERT INTO `messege_id_cashe`(`user_chat_and_massage_id`, `user_chat_id`, `user_message_id`, `proxy_message_id`) 
                VALUES ({user_chat_and_massage_id}, {user_chat_id}, {user_message_id}, {proxy_messege_id})"""
        try:
            cursor.execute(sql)
            connection.commit()
            logging.info(f"messege_id_cashe created. user_chat_and_massage_id:'{user_chat_and_massage_id}'  proxy_messege_id:'{proxy_messege_id}'")
            connection.close()
        except Error as e:
            logging.error(f"DB append failed! db_add_to_cashe_user_message_id '{e}'")
            connection.rollback()
            connection.close()


@lru_cache(maxsize=128)
def db_check_cache_replay_messege_id(proxy_message_id):

    try:
        sql = f"""SELECT
                `user_chat_id`,
                `user_message_id`,
                `proxy_message_id`
            FROM
                `messege_id_cashe`
            WHERE
                `proxy_message_id` = {proxy_message_id}"""

        connection = mydbConnection()
        cursor = connection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()
        if len(myresult)==0:
            return False
        user_chat_id = myresult[0][0]
        user_message_id = myresult[0][1]
        return {'user_chat_id':user_chat_id,
                "user_message_id":user_message_id}
    except Error as e:
        logging.WARN(f"We does not found cache for user. db_check_cache_replay_messege_id Error:{e}")
        connection.rollback()
        connection.close()
        return False


# ХЗ, не работает TODO: Почитнить кэшью
def cache_or_db_check_replay_messege_id(proxy_message_id):
    proxy_message_id = str(proxy_message_id)
    try:
        try_cache = db_check_cache_replay_messege_id(proxy_message_id)
        if try_cache != False:
            # print("Уже есть кэш")
            logging.INFO(f"cache_or_db_check_replay_messege_id. We found cache for user. proxy_message_id:")
            return try_cache
        else:
            # print("кэша нет")
            logging.INFO(f"We does not find cache for user, trying find in db. proxy_message_id:")
            return db_check_cache_replay_messege_id.__wrapped__(proxy_message_id)  # Принудительно без кеша

    except Error as e:
        logging.WARN(f"We does not found cache for user. db_check_cache_replay_messege_id Error:{e}")




# print(cache_or_db_check_replay_messege_id(999))
