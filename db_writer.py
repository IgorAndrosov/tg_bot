import sqlite3 
import telebot
from telebot import types

bot = telebot.TeleBot('5965053048:AAFHcfnh0S3fbMhEofqHzvB-9eKE5xv1rUs')

conn = sqlite3.connect('db/db.db', check_same_thread=False)
cursor = conn.cursor()

def new_users(user_id: int):
    cursor.execute('insert into users (user_id) values(?)', (user_id,))
    conn.commit()

def read_users(user_id):
    cursor.execute('select * from users where user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.commit()
    return result

def new_callback(message: int):
    cursor.execute('insert into callback (user_id, user_name, message_id) values (?,?,?)', (message.from_user.id, message.from_user.first_name, message.id))
    conn.commit()

def read_callback():
    cursor.execute('select * from callback where status is Null')
    result = cursor.fetchall()
    conn.commit()
    return result

def complete_callback(mass):
    cursor.execute('update callback set status = 1 where id = ?', (mass[0],))
    conn.commit()

def read_status(user_id: int):
    cursor.execute('select status from users where user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.commit()
    return result

def read_psw_val(user_id: int):
    cursor.execute('select val from users where user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.commit()
    return result

def trying(user_id: int, val: int):
    cursor.execute('UPDATE users SET val = ? WHERE user_id = ?;', (val, user_id,))
    conn.commit()

def edit_users(user_id: int, coloumn: str, value: int):
    cursor.execute(f'update users set {coloumn} = ? where user_id = ?', (value, user_id,))
    conn.commit()