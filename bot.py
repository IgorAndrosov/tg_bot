import telebot 
import db_writer as db
import admin
import keyboard
from telebot import types

bot = telebot.TeleBot('5965053048:AAFHcfnh0S3fbMhEofqHzvB-9eKE5xv1rUs')

@bot.message_handler(commands=['start'])
def welcome(message):
   
   if db.read_users(message.from_user.id) == None:
       db.new_users(user_id=message.from_user.id)
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   item1 = types.KeyboardButton('Что ты умеешь?')
   markup.add(item1)
   bot.send_message(message.chat.id, '''Привет!
Что ты хочешь узнать?''', reply_markup = markup)

@bot.message_handler(commands=['admin'])
def validation(message):
    
    val = db.read_psw_val(user_id = message.from_user.id)[0]

    if db.read_status(user_id = message.from_user.id)[0] == 1:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, ты администратор!')
        keyboard.admin(message)
    elif val < 3:
        msg = bot.send_message(message.chat.id, f'Попытка {val+1}\nВведите пароль:')
        db.trying(user_id = message.from_user.id, val = val+1)
        bot.register_next_step_handler(msg, enter_psswrd)
    else:
        bot.send_message(message.chat.id, 'Превышено количество попыток. Обратитесь к администратору.')

def enter_psswrd(message):
    pas = message.text
    if pas == '33133313':
        bot.send_message(message.chat.id, 'Поздравляю, ты администратор!')
        db.edit_users(user_id = message.from_user.id, coloumn = 'status', value = 1)
        db.edit_users(user_id = message.from_user.id, coloumn = 'val', value = 0)
        keyboard.admin(message)
    else:
        msg = bot.send_message(message.chat.id, 'Пароль неверный')

@bot.message_handler(content_types=['text'])
def buttons(message):

    value = message.text.lower()

    match value:
        case 'что ты умеешь?':
            with open('messages/welcome.txt', 'r', encoding='utf-8') as f:
                message_text = f.read()
            bot.send_message(message.chat.id, message_text)
            keyboard.user(message)
        case 'адреса':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Ворошилова", callback_data='1')
            item2 = types.InlineKeyboardButton("Кирова", callback_data='2')
            item3 = types.InlineKeyboardButton("Памятник Славы", callback_data='3')
            item4 = types.InlineKeyboardButton("Плехановская", callback_data='4')

            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Выбери адрес', reply_markup = markup)
        case 'обратная связь':
            msg = bot.send_message(message.chat.id, 'Напиши о своих впечатлениях')
            bot.register_next_step_handler(msg, callback)
        case 'баллы':
            bot.send_message(message.chat.id, "Программа лояльности работает в тестовом режиме")
        case 'о нас':
            with open('messages/about_us.txt', 'r', encoding='utf-8') as f:
                message_text = f.read()
            bot.send_message(message.chat.id, message_text)
        case 'оставить чайвые':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Иван', callback_data='ivan')
            button2 = types.InlineKeyboardButton('Мария', callback_data='maria')
            button3 = types.InlineKeyboardButton('Петр', callback_data='petr')
            markup.add(button1, button2, button3)
                
            bot.send_message(message.chat.id, 'Выберите бариста:', reply_markup=markup)

        case 'стоп':
            bot.stop_polling()

    if db.read_status(message.from_user.id)[0] == 1:
        match value:
            case 'отчет по списку пользователей':
                bot.send_message(message.chat.id, 'Yes')
            case 'посмотреть новые отзывы':
                bot.send_message(message.chat.id, 'Yes')
            case 'посмотреть статистику':
                bot.send_message(message.chat.id, 'Yes')
            case 'вернуться в меню гостя':
                keyboard.user(message)

def callback(message):
    db.new_callback(message=message)
    admin.callback_notify(message)
    bot.send_message(message.chat.id, "Спасибо за обращение!")

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    value = call.data
    match value:
        case '1':
            bot.send_location(call.message.chat.id, 51.654749, 39.178763)
        case '2':
            bot.send_location(call.message.chat.id, 51.659781, 39.195710)
        case '3':
            bot.send_location(call.message.chat.id, 51.702425, 39.182282)
        case '4':
            bot.send_location(call.message.chat.id, 51.668416, 39.192764)
        case 'read':
            missed_callback = db.read_callback()
            for mass in missed_callback:
                db.complete_callback(mass=mass)
                bot.forward_message(call.message.chat.id, from_chat_id=mass[1], message_id=mass[3])
        case 'ivan':
            bot.send_message(call.message.chat.id, 'Бариста: Иван\nРеквизиты: 1234567890')
        case 'maria':
            bot.send_message(call.message.chat.id, 'Бариста: Мария\nРеквизиты: 0987654321')
        case 'petr':
            bot.send_message(call.message.chat.id, 'Бариста: Петр\nРеквизиты: 5555555555')
    bot.delete_message(call.message.chat.id, call.message.id)

import json
from flask import Flask, request

bot.infinity_polling()