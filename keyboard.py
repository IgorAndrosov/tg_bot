import telebot 
import loyal
import db_writer as db
from telebot import types

bot = telebot.TeleBot('5965053048:AAFHcfnh0S3fbMhEofqHzvB-9eKE5xv1rUs')

def user(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Адреса')
    item2 = types.KeyboardButton('Обратная связь')
    item3 = types.KeyboardButton('Баллы')
    item4 = types.KeyboardButton('О нас')
    item5 = types.KeyboardButton('Оставить чаевые')

    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, 'Приятного использования!', reply_markup=markup)

def admin(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = ('Отчет по списку пользователей')
    item2 = ('Посмотреть новые отзывы')
    item3 = ('Посмотреть статистику')
    item4 = ('Создать рассылку')
    item5 = ('Вернуться в меню гостя')

    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, 'Клавиатура администратора активирована!', reply_markup=markup)

def barista(message):
    a = 1

def sys(message):
    a = 1

def webAppKeyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    webAppTest = types.WebAppInfo("https://igorandrosov.github.io/tg_web_app/")
    item1 = types.KeyboardButton(text="Меню", web_app=webAppTest)
    item2 = types.KeyboardButton(text="Баланс")
    item3 = types.KeyboardButton(text="Вернуться назад")
    markup.add(item1, item2, item3)
    inf = db.read_users(user_id = message.chat.id)
    f = "messages/loyal.txt"
    encoding = "utf-8"

    with open(f, 'r', encoding=encoding) as file:
        text = file.read()

    msg = f'''☕️ Программа лояльности в кофейне ☕️
    👤 Ваш айди: 706589393

🌟 Ваши баллы: {inf[4]}''' + text
    bot.send_message(message.chat.id, msg, reply_markup = markup)