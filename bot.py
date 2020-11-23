import config
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardButton
import time
import datetime

# create lvl of logs
logging.basicConfig(level=logging.INFO)
# inicial bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
# btn
button_hi = KeyboardButton('Привет! 👋')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb.greet_kb)
    	
@dp.message_handler(commands = ["add"])
async def text(message: types.Message):
    await message.answer("Добавление...")

@dp.message_handler(commands = ["delete"])
async def text(message: types.Message):
    await message.answer("Удаление...")
# start лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

