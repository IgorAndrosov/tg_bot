import sqlite3 
import telebot
from telebot import types

bot = telebot.TeleBot('5965053048:AAFHcfnh0S3fbMhEofqHzvB-9eKE5xv1rUs')

conn = sqlite3.connect('db/db.db', check_same_thread=False)
cursor = conn.cursor()

def new_users(user_id: int, username: int):
    cursor.execute('insert into users (user_id, username) values(?,?)', (user_id, username,))
    conn.commit()

def read_users(user_id):
    cursor.execute('select * from users where user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.commit()
    return result

def read_all_users():
    cursor.execute('SELECT user_id FROM users')
    result = cursor.fetchall()
    conn.commit()
    return result

def new_callback(message: int):
    cursor.execute('insert into callback (user_id, user_name, message_id) values (?,?,?)', (message.from_user.id, message.from_user.first_name, message.id))
    conn.commit()

def read_callback():
    cursor.execute('select * from callback where status is Null')
    result = cursor.fetchone()
    conn.commit()
    return result

def complete_callback(mass):
    cursor.execute('update callback set status = 1 where id = ?', (mass[0],))
    conn.commit()

def read_status(user_id: int, table: str):
    cursor.execute(f'select val from {table} where user_id = {user_id}')
    result = cursor.fetchone()
    conn.commit()
    if result is not None:
        return result[0]
    else:
        return 0

def new_admin(user_id: int, username: int):
    cursor.execute('insert into admin (user_id, username) values(?,?)', (user_id, username,))
    conn.commit()

def new_barista(user_id: int, username: int):
    cursor.execute('insert into barista (user_id, username) values(?,?)', (user_id, username,))
    conn.commit()

def read_psw_val(user_id: int, username: int, table: str):
    cursor.execute(f'select val from {table} where user_id = {user_id}')
    result = cursor.fetchone()
    conn.commit()
    if result is not None:
        return result[0]
    elif table == 'admin':
        new_admin(user_id=user_id, username=username)
        result = 0
        return result
    elif table == 'barista':
        new_barista(user_id=user_id, username=username)
        result = 0
        return result

def trying(user_id: int, val: int, table: str):
    cursor.execute(f'update {table} set val = {val} WHERE user_id = {user_id};')
    conn.commit()

def edit_table(user_id: int, table: str, coloumn: str, value: int):
    cursor.execute(f'update {table} set {coloumn} = {value} where user_id = {user_id}')
    conn.commit()