import pymysql
from pymysql.cursors import DictCursor


def create_connection():
    return pymysql.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="shoe_shop",
        cursorclass=DictCursor,
    )
