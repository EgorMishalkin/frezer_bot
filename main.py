import telebot
from telebot import types
bot = telebot.TeleBot('1415966035:AAG6D1ybRJWEO5JNQvWR7pV0c8gTzJ6KRDI')
bot.message_handler(commands=['start'])


def start_message(message):
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('Добавить', 'Удалить')
    bot.send_message(message.chat.id, 'Привет, я твой холодильник \n'
                                      'напиши свои продукты и сколько они хранятся,'
                                      'а я буду следить чтобы они не протухли)', reply_markup=keyboard1)


# функция отправки сообщения
def send_text(message, text):
    bot.send_message(message.chat.id, text)


# функция получения
@bot.message_handler(content_types=['text'])
def gettext(message):
    send_text(message, 'сообщение')

bot.polling(none_stop=True)
