import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot('1475424111:AAFuKG7yrCjbQe9yE41LBYkKhYESt_AHO7g')
freezer1 = {}


# функция отправки сообщения
def send_text(message, text):
    bot.send_message(message.chat.id, text)


# функция подключния к бд
def ensure_connection(func):
	def inner(*args, **kwargs):
		global conn
		with sqlite3.connect('o.db', check_same_thread=False) as conn:
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
			add_or_not     INT,
			del_or_not     INT,
			show_or_not     INT
		)
	''')
	conn.commit()


# добавение значений в бд
@ensure_connection
def add_user(conn, user_id: int, freezer, add_or_not: int, del_or_not: int, show_or_not: int):
	c = conn.cursor()
	c.execute('INSERT INTO users (user_id, freezer, add_or_not, del_or_not, show_or_not) VALUES (?, ?, ?, ?, ?)', (user_id, freezer, add_or_not, del_or_not, show_or_not))
	conn.commit()


#
@ensure_connection
def list_db(conn, user_id: int, limit: int = 1):
	c = conn.cursor()
	c.execute('SELECT user_id FROM users WHERE user_id = ? ORDER BY user_id DESC LIMIT ?', (user_id, limit))
	return c.fetchall()


@bot.message_handler(commands=['start'])
def do_start(message):
	global keyboard1
	keyboard1 = telebot.types.ReplyKeyboardMarkup()
	keyboard1.row('/добавить', '/удалить')
	keyboard1.row('/список', '/помощь')
	# создание клавиатуры
	get_user = list_db(user_id = message.from_user.id)
	try:
		if get_user[0][0]:
			bot.send_message(message.chat.id, 'Приветствую, ' + str(message.from_user.first_name) +'. Вы уже существуете в базе', reply_markup=keyboard1)
		else:
			add_user(user_id = message.from_user.id, freezer = '', add_or_not = 0, del_or_not = 0, show_or_not = 0)
			bot.send_message(message.chat.id, str(message.from_user.first_name) + ', регистрация прошла успешно!', reply_markup=keyboard1)
	except IndexError: 
		add_user(user_id = message.from_user.id, freezer = '', add_or_not = 0, del_or_not = 0, show_or_not = 0)
		bot.send_message(message.chat.id, str(message.from_user.first_name) + ', регистрация прошла успешно!', reply_markup=keyboard1)


# функция подсказки пользователю
@bot.message_handler(commands=['помощь'])
def help_user(message):
	bot.send_message(message.chat.id, 'Бот, следящий за сроками продуктов. \n' +
					 'Функции: \n' +
					 '/добавить - добавление вашего продукта \n' +
					 '/удалить - удаление вашего продукта \n' +
					 'Так же бот каждый день будет уведомлять вас о том, какие продукты стоит съесть быстрее, а какие выкинуть)')


@bot.message_handler(commands=['список'])
def food(message):
	string = ''
	# в
	c = conn.cursor()
	user = message.from_user.id
	value = c.execute(f'SELECT * FROM users WHERE user_id = {user}').fetchone()
	freezer = value[1]
	print(freezer)
	if freezer == '':
		bot.send_message(message.chat.id, 'В вашем холодильнике ничего нет. Скорее сходите закупиться!')
	else:
			c = conn.cursor()
			user = message.from_user.id
			value = c.execute(f'SELECT * FROM users WHERE user_id = {user}').fetchone()
			freezer = value[1]
			# выводим начение столбца freezer
			bot.send_message(message.chat.id, 'Ваша еда в холодильнике:\n' + freezer)


# функция добавления продукта
@bot.message_handler(commands=['добавить'])
def add_product(message):
	bot.send_message(message.chat.id, 'Введите продукт и срок годности через пробел')
# если эта переменная равна 1, то мы понимаем, что надо выполнить функцию
	c = conn.cursor()
	user = message.from_user.id
	value = c.execute(f'SELECT * FROM users WHERE user_id = {user}').fetchone()
	add_or_not = value[2]
	c.execute(f'UPDATE users SET add_or_not = 1 WHERE user_id = {user}')
	conn.commit()


# функция удаления продукта
@bot.message_handler(commands=['удалить'])
def del_product(message):
	food(message)
	bot.send_message(message.chat.id, 'Введите продукт и срок годности через пробел который надо удалить')
	# если эта переменная равна 1, то мы понимаем, что надо выполнить функцию
	c = conn.cursor()
	user = message.from_user.id
	value = c.execute(f'SELECT * FROM users WHERE user_id = {user}').fetchone()
	del_or_not = value[3]
	c.execute(f'UPDATE users SET del_or_not = 1 WHERE user_id = {user}')
	conn.commit()


# функция получения любого текста
@bot.message_handler(content_types=['text'])
def gettext(message):
	c = conn.cursor()
	user = message.from_user.id
	value = c.execute(f'SELECT * FROM users WHERE user_id = {user}').fetchone()
	add_or_not = value[2]
	del_or_not = value[3]
	show_or_not = value[4]
	freezer = value[1]
	# тут происходит обработка добавления
	if add_or_not == 1:
		mess = message.text
		food = ''
		# mess[0:-1] - название продукта
		for i in mess[0:-1].split(' '):
			food += f'{i} '
		food = food[0:-1]
		how_long = mess.split(' ')[-1]
		try:
			a = freezer + mess + '\n'
			c.execute(f'UPDATE users SET freezer = "{a}" WHERE user_id = {user}')
			conn.commit()
			send_text(message, 'Успешно добавлено!')

			c = conn.cursor()
			user = message.from_user.id
			value = c.execute(f'SELECT * FROM users WHERE user_id = {user}').fetchone()
			add_or_not = value[2]
			c.execute(f'UPDATE users SET add_or_not = 0 WHERE user_id = {user}')
			conn.commit()
		# ошибка при вводе
		except IndexError:
			send_text(message, 'Введены неверные данные!')
		add_or_not = 0

	# тут происходит обработка удаления
	elif del_or_not == 1:
		mess = message.text
		food = ''
		# mess[0:-1] - название продукта
		for i in mess[0:-1].split(' '):
			food += f'{i} '
		food = food[0:-1]
		how_long = mess.split(' ')[-1]
		try:
			a = freezer - mess + '\n'
			c.execute(f'UPDATE users SET freezer = "{a}" WHERE user_id = {user}')
			conn.commit()
			# mess = 'банан 4'
			# mess[0:-1] - название продукта
			# for i in mess[0:-1]:
			#	string += f'{i} '
			# строка string[0:-1] убирает лишний пробел в конце
			# freezer[string[0:-1]] = mess[-1]
			# freezer = mess
			send_text(message, 'Удалено успешно!')

			c = conn.cursor()
			user = message.from_user.id
			value = c.execute(f'SELECT * FROM users WHERE user_id = {user}').fetchone()
			add_or_not = value[2]
			c.execute(f'UPDATE users SET add_or_not = 0 WHERE user_id = {user}')
			conn.commit()
		# ошибка при вводе
		except TypeError:
			send_text(message, 'Неизвестная ошибка!')

		del_or_not = 0
	else:
		send_text(message, 'Неизвестная команда')


if __name__ == '__main__':
	init_db()
	bot.polling(none_stop=True, interval = 0)
