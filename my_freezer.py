import telebot
from telebot import types
import sqlite3
import sys

bot = telebot.TeleBot('1446473769:AAEI5XlIHW56g0yl-reM6x1ZP3ciy8MfOB8')


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
                     '/удалить - удаление вашего продукта')


# функция добавления продукта
@bot.message_handler(commands=['добавить'])
def add_product(message):
    sent = bot.send_message(message.chat.id, 'Введите продукт и сколько дней еще будет храниться:')
    bot.register_next_step_handler(sent, add_product_to_db)


def add_product_to_db(message):
    try:
        c = conn.cursor()
	# достаем продукт и срок годности
        prod, rem = message.text.split(' ')
        sql = f'INSERT INTO users (user_id, freezer, remain) VALUES ({message.chat.id}, "{prod}", {rem})'
        c.execute(sql)
        conn.commit()
        bot.send_message(message.chat.id, 'Продукт успешно добавлен!')
    except ValueError:
        bot.send_message(message.chat.id, 'Введены неверные данные!')


@bot.message_handler(commands=['удалить'])
def del_product(message):
    sent = bot.send_message(message.chat.id, 'Введите продукт, который надо удалить')
    # перекидываем на другую функцию
    bot.register_next_step_handler(sent, del_product_from_db)


def del_product_from_db(message):
    c = conn.cursor()
    prod = message.text
    # удаляем значение из таблицы	
    sql = f'DELETE FROM users WHERE user_id = {message.chat.id} AND freezer = "{prod}"'
    print(sql, file=sys.stderr)
    c.execute(sql)
    conn.commit()
    bot.send_message(message.chat.id, 'Продукт удален!')


@bot.message_handler(commands=['список'])
def show_product(message):
    c = conn.cursor()
    prod = message.text
    sql = f'SELECT freezer, remain FROM users WHERE user_id = {message.chat.id}'
    c.execute(sql)
    string = ''
	
    # создаем красивую строчку 	
    for name, key in c.fetchall():
        string += name + ' ' + str(key) + '\n'

    bot.send_message(message.chat.id, 'Список продуктов в холодильнике: \n' + string)


if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)
