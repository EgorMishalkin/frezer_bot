import telebot
import schedule
import time
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


bot = telebot.TeleBot('1446473769:AAEI5XlIHW56g0yl-reM6x1ZP3ciy8MfOB8')
add_or_not = 0
del_or_not = 0
show_or_not = 0
id = ""
freezer = {}


# функция отправки сообщения
def send_text(message, text):
    bot.send_message(message.chat.id, text)


# функция подсказки пользователю
@bot.message_handler(commands=['обновить'])
def notice(message):
    # создаем новый словарь, где будем записывать
    non_pull = 0
    global freezer
    clear_freezer = {}
    for key, value in freezer.items():
        value -= 1
        p = morph.parse(key)[0]
        if 'plur' in p.tag:
            verb = 'испортятся'
        else:
            verb = 'испортится'
        if value == 3:
            non_pull = 1
            send_text(message, f'{key} {verb} через 3 дня! поторопитесь съесть/выпить)')
            clear_freezer[key] = value
        elif value == 2:
            non_pull = 1
            send_text(message, f'{key} {verb} через 2 дня! поторопитесь съесть/выпить!!')
            clear_freezer[key] = value
        elif value == 1:
            non_pull = 1
            send_text(message, f'{key} {verb} завтра! поторопитесь съесть/выпить!!!')
            clear_freezer[key] = value
        elif value == 0:
            non_pull = 1
            if 'plur' in p.tag:
                send_text(message, f'{key} испортились! обязательно выкиньте продукт')
            else:
                send_text(message, f'{key} испортился! обязательно выкиньте продукт')
        else:
            clear_freezer[key] = value

    if non_pull == 0:
        send_text(message, 'Поздравляю, ни один продукт не протух! Вы большой молодец!')
        freezer = clear_freezer
    else:
        freezer = clear_freezer


@bot.message_handler(commands=['start'])
def start_message(message):
    global id
    # создание клавиатуры
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('/добавить', '/удалить')
    keyboard1.row('/список', '/помощь')
    keyboard1.row('/обновить')
    # создание клавиатуры
    id = message
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
def show_dict(message):

    string = ''
    # проверка на пустой холодос
    if freezer == {}:
        bot.send_message(message.chat.id, 'В вашем холодильнике ничего нет. Скорее сходите закупиться!')
    else:
        for key, value in freezer.items():
            # строка - ключ значение переход на другую строку
            part_string = f'{key} {value} \n'
            # записываем это все в большую строку
            string += part_string
        # выводим значение
        bot.send_message(message.chat.id, string)


# функция подсказки пользователю
@bot.message_handler(commands=['помощь'])
def help_user(message):
    bot.send_message(message.chat.id, 'Бот, следящий за сроками продуктов. \n' +
                     'Функции: \n' +
                     '/добавить - добавление вашего продукта \n' +
                     '/удалить - удаление вашего продукта \n' +
                     '/обновить - начало нового дня. Бот автоматически обновляет данные насчет ваших продуктов)')


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
            string = ''
            # mess[0:-1] - название продукта
            for i in mess[0:-1]:
                string += f'{i} '
            # строка string[0:-1] убирает лишний пробел в конце
            freezer[string[0:-1]] = int(mess[-1])
            send_text(message, 'Успешно добавлено!')
        # ошибка при вводе
        except ValueError:
            send_text(message, 'Введены неверные данные!')
        add_or_not = 0
    # тут происходит обработка удаления
    elif del_or_not == 1:
        mess = message.text
        try:
            del freezer[mess]
            send_text(message, 'Удалено!')
        except KeyError:
            send_text(message, 'такого продукта нет!')
        del_or_not = 0
    else:
        send_text(message, 'Неизвестная команда')


while True:
    schedule.run_pending()
    time.sleep(1)
    bot.polling(none_stop=True)
    
