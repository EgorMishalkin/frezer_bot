import telebot

bot = telebot.TeleBot('1415966035:AAG6D1ybRJWEO5JNQvWR7pV0c8gTzJ6KRDI')
add_or_not = 0
del_or_not = 0
show_or_not = 0
freezer = {}


# функция отправки сообщения
def send_text(message, text):
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    # создание клавиатуры
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('/добавить', '/удалить', '/список', '/помощь')
    # создание клавиатуры
    bot.send_message(message.chat.id, 'Привет, я твой холодильник \n'
                                      'напиши свои продукты и сколько они хранятся,'
                                      'а я буду следить чтобы они не протухли)', reply_markup=keyboard1)


# функция добавления продукта
@bot.message_handler(commands=['добавить'])
def add_product(message):
    global add_or_not
    bot.send_message(message.chat.id, 'Введите продукт и срок годности через пробел')
    # если эта переменная равна 1, то мы понимаем, что надо выполнить функцию
    add_or_not = 1


# функция удаления продукта
@bot.message_handler(commands=['удалить'])
def start_message(message):
    global del_or_not
    string = ''
    # цикл который делает строчку со значениями словаря
    for i in freezer.keys():
        string += f'{i} '
    # вывод сообщения
    bot.send_message(message.chat.id, 'Введите продукт который надо удалить: ' + string)
    # если эта переменная равна 1, то мы понимаем, что надо выполнить функцию
    del_or_not = 1


# функция показа всех продуктов
@bot.message_handler(commands=['список'])
def start_message(message):
    bot.send_message(message.chat.id, freezer.keys())


# функция подсказки
@bot.message_handler(commands=['помощь'])
def help_user(message):
    bot.send_message(message.chat.id, 'Бот, следящий за сроками продуктов')


# функция получения
@bot.message_handler(content_types=['text'])
def gettext(message):
    global add_or_not
    global del_or_not
    global show_or_not

    # тут происходит обработка добавления
    if add_or_not == 1:
        mess = message.text.split(' ')
        try:
            # пробуем добавить в слоарь значение
            freezer[mess[0]] = mess[1]
            send_text(message, 'Успешно добавлено!')
        # ошибка при вводе
        except IndexError:
            send_text(message, 'Введены неверные данные!')
        add_or_not = 0
    # тут происходит обработка удаления
    elif del_or_not == 1:
        mess = message.text
        del freezer[mess]
        send_text(message, 'Удалено!')
        del_or_not = 0
    else:
        send_text(message, 'Неизвестная команда')


bot.polling(none_stop=True)
