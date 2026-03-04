import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Вставь сюда токен твоего бота
BOT_TOKEN = "8448786511:AAFwRxSC1kbWM0W6jLxWwrH_3ARmUQ8BokQ"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Простой обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот, работающий 24/7 на Render!")

# Обработчик простого текста
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# Основная функция
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
