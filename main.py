import telebot
from telebot import types

bot = telebot.TeleBot('1415966035:AAG6D1ybRJWEO5JNQvWR7pV0c8gTzJ6KRDI')
add_or_not = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    # создание клавиатуры
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('Добавить', 'Удалить')
    # создание клавиатуры
    bot.send_message(message.chat.id, 'Привет, я твой холодильник \n'
                                      'напиши свои продукты и сколько они хранятся,'
                                      'а я буду следить чтобы они не протухли)', reply_markup=keyboard1)


# функция добавления продукта
@bot.message_handler(commands=['add'])
def start_message(message):
    global add_or_not
    bot.send_message(message.chat.id, 'Введите продукт и срок годности через пробел')
    add_or_not = 1


# функция отправки сообщения
def send_text(message, text):
    bot.send_message(message.chat.id, text)


# функция получения
@bot.message_handler(content_types=['text'])
def gettext(message):
    global add_or_not
    mess = message.text.split(' ')
    if add_or_not == 1:
        send_text(message, mess[0])
        add_or_not = 0
    else:
        send_text(message, 'сообщение')


bot.polling(none_stop=True)
