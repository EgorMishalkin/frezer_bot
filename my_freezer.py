import telebot
from telebot import types
import sqlite3
import sys
import pymorphy2

bot = telebot.TeleBot('1446473769:AAEI5XlIHW56g0yl-reM6x1ZP3ciy8MfOB8')

morph = pymorphy2.MorphAnalyzer()


# функция подключния к бд
def ensure_connection(func):
    def inner(*args, **kwargs):
        global conn
        with sqlite3.connect('users.db', check_same_thread=False) as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


# создание бд
@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS users')

    c.execute('''
		CREATE TABLE IF NOT EXISTS users (
			user_id     INTEGER NOT NULL,
			freezer     TEXT,
			remain INTEGER)
	''')
    conn.commit()


@bot.message_handler(commands=['start'])
def do_start(message):
    global keyboard1
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('/добавить', '/удалить')
    keyboard1.row('/список', '/помощь')
    keyboard1.row('/обновление')
    bot.send_message(message.chat.id, 'Привет, я твой холодильник \n'
                                      'напиши свои продукты и сколько они хранятся,'
                                      'а я буду следить чтобы они не протухли)', reply_markup=keyboard1)
    # создание клавиатуры


# функция подсказки пользователю
@bot.message_handler(commands=['помощь'])
def help_user(message):
    bot.send_message(message.chat.id, 'Бот, следящий за сроками продуктов. \n' +
                     'Функции: \n' +
                     '/добавить - добавление вашего продукта \n' +
                     '/удалить - удаление вашего продукта \n' +
                     '/список - выводит все содержимое вашего холодильника)')


# функция добавления продукта
@bot.message_handler(commands=['добавить'])
def add_product(message):
    sent = bot.send_message(message.chat.id, 'Введите продукт и срок годности через пробел')
    bot.register_next_step_handler(sent, add_product_to_db)


def add_product_to_db(message):
    try:
        c = conn.cursor()
        prod, rem = message.text.split(' ')
        sql = f'INSERT INTO users (user_id, freezer, remain) VALUES ({message.chat.id}, "{prod}", {rem})'
        c.execute(sql)
        conn.commit()
        bot.send_message(message.chat.id, 'Продукт успешно добавлен!')
    except ValueError:
        bot.send_message(message.chat.id, 'Введены неверные данные!')


@bot.message_handler(commands=['удалить'])
def del_product(message):
    c = conn.cursor()
    prod = message.text
    sql = f'SELECT freezer, remain FROM users WHERE user_id = {message.chat.id}'
    c.execute(sql)
    string = ''

    for name, key in c.fetchall():
        string += name + ' '

    sent = bot.send_message(message.chat.id, 'Введите продукт, который надо удалить: ' + string)
    bot.register_next_step_handler(sent, del_product_from_db)


def del_product_from_db(message):
    c = conn.cursor()
    prod = message.text
    sql = f'DELETE FROM users WHERE user_id = {message.chat.id} AND freezer = "{prod}"'
    c.execute(sql)
    conn.commit()
    bot.send_message(message.chat.id, 'Продукт удален!')


@bot.message_handler(commands=['обновление'])
def show_product(message):
    c = conn.cursor()
    prod = message.text
    sql1 = f'UPDATE users SET remain = remain - 1 WHERE user_id = {message.chat.id}'
    c.execute(sql1)
    sql2 = f'DELETE FROM users WHERE user_id = {message.chat.id} AND remain = 0'
    c.execute(sql2)
    conn.commit()
    sql = f'SELECT freezer, remain FROM users WHERE user_id = {message.chat.id}'
    c.execute(sql)

    non_pull = 0
    for key, value in c.fetchall():
        p = morph.parse(key)[0]
        if 'plur' in p.tag:
            verb = 'испортятся'
        else:
            verb = 'испортится'
        if value == 3:
            non_pull = 1
            bot.send_message(message.chat.id, f'{key} {verb} через 3 дня! поторопитесь съесть/выпить)')
        elif value == 2:
            non_pull = 1
            bot.send_message(message.chat.id, f'{key} {verb} через 2 дня! поторопитесь съесть/выпить!!')
        elif value == 1:
            non_pull = 1
            bot.send_message(message.chat.id, f'{key} {verb} завтра! поторопитесь съесть/выпить!!!')
        elif value == 0:
            non_pull = 1
            if 'plur' in p.tag:
                bot.send_message(message.chat.id, f'{key} испортились! обязательно выкиньте продукт')
            else:
                bot.send_message(message.chat.id, f'{key} испортился! обязательно выкиньте продукт')

    if non_pull == 0:
        bot.send_message(message.chat.id, 'Поздравляю, ни один продукт не протух! Вы большой молодец!')
    else:
        pass


@bot.message_handler(commands=['список'])
def show_product(message):
    c = conn.cursor()
    prod = message.text
    sql = f'SELECT freezer, remain FROM users WHERE user_id = {message.chat.id}'
    c.execute(sql)
    string = ''

    for name, key in c.fetchall():
        string += name + ' ' + str(key) + '\n'

    if string == '':
        bot.send_message(message.chat.id, 'В вашем холодильнике ничего нет. Скорее сходите закупиться!')
    else:
        bot.send_message(message.chat.id, 'Список продуктов в холодильнике: \n' + string)


if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)
