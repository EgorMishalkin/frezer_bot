import config
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types

# create lvl of logs
logging.basicConfig(level=logging.INFO)
# inicial bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ["delete"])
async def food_step_1(message: types.Message):
    await message.answer("Удаление")

@dp.message_handler(commands = ["enter"])
async def food_step_1(message: types.Message):
    await message.answer("Добавление")

# start лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

