import telebot

bot = telebot.TeleBot('1415966035:AAG6D1ybRJWEO5JNQvWR7pV0c8gTzJ6KRDI')
add_or_not = 0
del_or_not = 0
show_or_not = 0


# функция отправки сообщения
def send_text(message, text):
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    # создание клавиатуры
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('/add', '/delete', '/show', '/help')
    # создание клавиатуры
    bot.send_message(message.chat.id, 'Привет, я твой холодильник \n'
                                      'напиши свои продукты и сколько они хранятся,'
                                      'а я буду следить чтобы они не протухли)', reply_markup=keyboard1)


# функция добавления продукта
@bot.message_handler(commands=['add'])
def add_product(message):
    global add_or_not
    bot.send_message(message.chat.id, 'Введите продукт и срок годности через пробел')
    add_or_not = 1


# функция удаления продукта
@bot.message_handler(commands=['delete'])
def start_message(message):
    global del_or_not
    bot.send_message(message.chat.id, 'Введите продукт который надо удалить')
    del_or_not = 1


# функция показа всех продуктов
@bot.message_handler(commands=['show'])
def start_message(message):
    bot.send_message(message.chat.id, 'тут будем показывать словарь')


# функция подсказки
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Бот, следящий за сроками продуктов')


# функция получения
@bot.message_handler(content_types=['text'])
def gettext(message):
    global add_or_not
    global del_or_not
    global show_or_not

    if add_or_not == 1:
        mess = message.text.split(' ')
        send_text(message, mess[0])
        add_or_not = 0
    if del_or_not == 1:
        mess = message.text
        send_text(message, 'delete')
        del_or_not = 0
    else:
        send_text(message, 'Неизвестная команда')


bot.polling(none_stop=True)
