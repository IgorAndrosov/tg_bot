import telebot
import db_writer as db
import keyboard
from telebot import types

bot = telebot.TeleBot('5965053048:AAFHcfnh0S3fbMhEofqHzvB-9eKE5xv1rUs')

def validation(message):

    if db.read_admin(message.from_user.id) == None:
        k = db.read_pre_admin(message.from_user.id)[2]
        if k < 3:
            msg = bot.send_message(message.chat.id, f'Попытка {k+1}\nВведите пароль:')
            db.plus_k(user_id=message.from_user.id, val=k+1)
            bot.register_next_step_handler(msg, enter_psswrd)
        else:
            bot.send_message(message.chat.id, 'Превышено количество попыток. Обратитесь к администратору.')
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, ты администратор!')
        keyboard.admin(message)

def enter_psswrd(message):
    print(message)
    pas = message.text
    k = db.read_pre_admin(message.from_user.id)[2]
    if pas == '33133313':
        bot.send_message(message.chat.id, 'Поздравляю, ты администратор!')
        db.write_admin(user_id = message.from_user.id, username = message.from_user.first_name)
        db.del_pre_admin(user_id = message.from_user.id)
        keyboard.admin(message)
    else:
        msg = bot.send_message(message.chat.id, 'Пароль неверный')

def admin_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

def callback_notify(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Посмотреть", callback_data='read')
    markup.add(item1)

    bot.send_message(706589393, 'Появилось новое обращение!', reply_markup = markup)

def mailing(message):

    user_id = db.read_all_users()
    
    for user in user_id:
        try:
            bot.send_message(user[0], message.text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user[0]}: {str(e)}")
