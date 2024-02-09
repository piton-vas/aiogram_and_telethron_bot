import logging

import mysql.connector
from mysql.connector import Error
import env.config


def mydbConnection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=env.config.db_host,
            user=env.config.db_name,
            passwd=env.config.db_pass,
            database=env.config.db_name
        )
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
        sql = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"
        val = (user_id, user_name)
        cursor.execute(sql, val)
        connection.commit()
        logging.info('New user has been registred, iser_id:' + str(user_id) + ' User_name:' + user_name)


def check_user_status(user_id, user_name=''):
    connection = mydbConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id, status from users WHERE user_id='{user_id}'")
    myresult = cursor.fetchall()
    # print(myresult)
    return myresult[0][1]


    # if myresult=cursor.fetchall():  # checking if something found with this username
    #     logging.info('User_id:' + str(user_id) + ' already exists. His user_name is:' + user_name)
    # else:
    #     logging.error('Error while shecking status, iser_id:' + str(user_id) + ' User_name:' + user_name)

myresult1 = check_user_status(243697626, 'Василий')
print(myresult1)
