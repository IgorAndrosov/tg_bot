import telebot 
import db_writer as db
import admin
import keyboard
<<<<<<< HEAD
=======
import loyal
>>>>>>> 3f398878cbbc4f69bd214ff2d4f2980956d63433
from telebot import types

bot = telebot.TeleBot('5965053048:AAFHcfnh0S3fbMhEofqHzvB-9eKE5xv1rUs')

@bot.message_handler(commands=['start'])
def welcome(message):
   user_id = message.from_user.id
   
   if db.read_users(user_id) == None:
       db.new_users(user_id=user_id)
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   item1 = types.KeyboardButton('Что ты умеешь?')
   markup.add(item1)
   bot.send_message(user_id, '''Привет!
Что ты хочешь узнать?''', reply_markup = markup)

@bot.message_handler(commands=['admin'])
def validation(message):
    user_id = message.from_user.id

    val = db.read_psw_val(user_id = user_id)[0]

    if db.read_status(user_id = user_id) == 1:
        bot.send_message(user_id, f'{message.from_user.first_name}, ты администратор!')
        keyboard.admin(message)
    elif val < 3:
        msg = bot.send_message(user_id, f'Попытка {val+1}\nВведите пароль:')
        db.trying(user_id = user_id, val = val+1)
        bot.register_next_step_handler(msg, enter_psswrd)
    else:
        bot.send_message(user_id, 'Превышено количество попыток. Обратитесь к администратору.')

def enter_psswrd(message):
    user_id = message.from_user.id
    pas = message.text
    if pas == '33133313':
        bot.send_message(user_id, 'Поздравляю, ты администратор!')
        db.edit_users(user_id = user_id, coloumn = 'status', value = 1)
        db.edit_users(user_id = user_id, coloumn = 'val', value = 0)
        keyboard.admin(message)
    else:
        msg = bot.send_message(user_id, 'Пароль неверный')

@bot.message_handler(content_types=['text'])
def buttons(message):
    user_id = message.from_user.id

    global user
    value = message.text.lower()

    match value:
        case 'что ты умеешь?':
            with open('messages/welcome.txt', 'r', encoding='utf-8') as f:
                message_text = f.read()
            bot.send_message(user_id, message_text)
            keyboard.user(message)
        case 'адреса':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Ворошилова", callback_data='Ворошилова')
            item2 = types.InlineKeyboardButton("Кирова", callback_data='Кирова')
            item3 = types.InlineKeyboardButton("Памятник Славы", callback_data='Памятник Славы')
            item4 = types.InlineKeyboardButton("Плехановская", callback_data='Плехановская')

            markup.add(item1, item2, item3, item4)

            bot.send_message(user_id, 'Выбери адрес', reply_markup = markup)
        case 'обратная связь':
            msg = bot.send_message(user_id, 'Напиши о своих впечатлениях')
            bot.register_next_step_handler(msg, callback)
        case 'баллы':
            keyboard.webAppKeyboard(message)
        case 'о нас':
            with open('messages/about_us.txt', 'r', encoding='utf-8') as f:
                message_text = f.read()
            bot.send_message(user_id, message_text)
        case 'оставить чаевые':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Иван', callback_data='ivan')
            button2 = types.InlineKeyboardButton('Мария', callback_data='maria')
            button3 = types.InlineKeyboardButton('Петр', callback_data='petr')
            markup.add(button1, button2, button3)
                
            bot.send_message(user_id, 'Выберите бариста:', reply_markup=markup)
        case 'вернуться назад':
            keyboard.user(message)
        case 'баланс':
<<<<<<< HEAD
=======
            inf = db.read_users(user_id = message.chat.id)
            msg = f'''🌟 Ваши баллы: {inf[4]}
🎯 До следующего уровня: {loyal.level(inf[4])}
💰 Текущая скидка: {loyal.discount(inf[4])}%'''
>>>>>>> 3f398878cbbc4f69bd214ff2d4f2980956d63433
            bot.send_message(user_id, f'Ваш баланс: {db.read_users(user_id=user_id)[4]}')

    if db.read_status(user_id) == 1:
        match value:
            case 'отчет по списку пользователей':
                bot.send_message(user_id, 'Yes')
            case 'посмотреть новые отзывы':
                bot.send_message(user_id, 'Yes')
            case 'посмотреть статистику':
                bot.send_message(user_id, 'Yes')
            case 'вернуться в меню гостя':
                keyboard.user(message)

def callback(message):
    user_id = message.from_user.id
    db.new_callback(message=message)
    admin.callback_notify(message)
    bot.send_message(user_id, "Спасибо за обращение!")

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id
    global sum
    global user

    value = call.data
    match value:
        case 'Ворошилова':
            bot.send_message(user_id, 'Ворошилова:')
            bot.send_location(user_id, 51.654749, 39.178763)
        case 'Кирова':
            bot.send_message(user_id, 'Кирова:')
            bot.send_location(user_id, 51.659781, 39.195710)
        case 'Памятник Славы':
            bot.send_message(user_id, 'Памятник Славы:')
            bot.send_location(user_id, 51.702425, 39.182282)
        case 'Плехановская':
            bot.send_message(user_id, 'Плехановская:')
            bot.send_location(user_id, 51.668416, 39.192764)
        case 'read':
            miss = db.read_callback()
            db.complete_callback(mass=miss)
            bot.forward_message(user_id, from_chat_id=miss[1], message_id=miss[3])
        case 'ivan':
            bot.send_message(user_id, 'Бариста: Иван\nРеквизиты: 1234567890')
        case 'maria':
            bot.send_message(user_id, 'Бариста: Мария\nРеквизиты: 0987654321')
        case 'petr':
            bot.send_message(user_id, 'Бариста: Петр\nРеквизиты: 5555555555')
        case 'accept':
            addit(user_id, sum)
            bot.send_message(user_id, f'Зарос от пользователя {user} на сумму {sum} принят')
            bot.send_message(user, 'Баллы успешно начислены🎆')
        case 'decline':
            bot.send_message(user_id, f'Зарос от пользователя {user} на сумму {sum} отклонен')
            bot.send_message(user, 'Запрос отклонен😥')

    bot.delete_message(user_id, call.message.id)

def addit(webAppMes, sum):
    global user
    inf = db.read_users(user_id=user)
    sum = int(sum)
    sum = sum + inf[4]
    db.edit_users(user_id=user, coloumn='sum', value=sum)

@bot.message_handler(content_types=['web_app_data']) #получаем отправленные данные 
def answer(webAppMes):
    global user
    user = webAppMes.chat.id
    global sum
    sum = webAppMes.web_app_data.data
    bot.send_message(webAppMes.chat.id, f"Запрос на начисление баллов по заказц на сумму {sum} принят. Бонусы начислятся после оплаты.") 
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Подтвердить', callback_data='accept')
    button2 = types.InlineKeyboardButton('Отклонить', callback_data='decline')
    markup.add(button1, button2)
        
<<<<<<< HEAD
    bot.send_message(491276678, '''Заказ оплачен?''', reply_markup=markup)
=======
    bot.send_message(706589393, '''Заказ оплачен?''', reply_markup=markup)
>>>>>>> 3f398878cbbc4f69bd214ff2d4f2980956d63433

bot.infinity_polling()