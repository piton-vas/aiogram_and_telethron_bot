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
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection




def add_new_user(user_id, user_name):
    connection = mydbConnection()
    cursor = connection.cursor()
    sql = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"
    val = (user_id, user_name)

    cursor.execute(sql, val)
    connection.commit()
    print("Появился новый пользователь " + user_name)



