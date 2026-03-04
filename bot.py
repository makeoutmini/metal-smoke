import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

# Токен из Render Environment Variable
TOKEN = os.getenv("8448786511:AAFwRxSC1kbWM0W6jLxWwrH_3ARmUQ8BokQ")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Цены в тенге
prices = {
    2500: 5500,
    6000: 7500,
    8000: 9000,
    10000: 11000,
    18000: 12000,
    20000: 13000,
    25000: 13500,
    28000: 14000,
    35000: 15000,
    38000: 15500,
    41000: 16000
}

# Стартовое меню
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📝 Условия заказа 📝", callback_data="terms"))
    kb.add(InlineKeyboardButton("Выбрать бренд", callback_data="brands"))
    await message.answer("Привет! Добро пожаловать в Metal Smoke", reply_markup=kb)

# Условия заказа
@dp.callback_query_handler(lambda c: c.data == "terms")
async def terms(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = "🔒 Условия заказа:\n• Минимальный заказ: 5000 тенге\n• Доставка: бесплатная от 10000 тенге"
    await bot.send_message(callback_query.from_user.id, text)

# Меню брендов
@dp.callback_query_handler(lambda c: c.data == "brands")
async def brands(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    kb = InlineKeyboardMarkup()
    for brand in ["COOLPLAY", "ELFBAR", "JACKBAR", "PLONQ", "RABBEATS", "WAKA"]:
        kb.add(InlineKeyboardButton(brand, callback_data=f"brand_{brand}"))
    await bot.send_message(callback_query.from_user.id, "Выберите бренд:", reply_markup=kb)

# Выбор конкретного бренда
@dp.callback_query_handler(lambda c: c.data.startswith("brand_"))
async def show_brand(callback_query: types.CallbackQuery):
    brand = callback_query.data.replace("brand_", "")
    await bot.answer_callback_query(callback_query.id)
    text = f"🏷️ Бренд: {brand}\n💨 Затяжки: выберите ниже\n💰 Цена: зависит от кол-ва\n🚬 Никотин: 5%\n📦 Наличие: 50+ шт."
    kb = InlineKeyboardMarkup()
    for qty, price in prices.items():
        kb.add(InlineKeyboardButton(f"{qty} затяжек - {price} ₸", callback_data=f"buy_{brand}_{qty}"))
    await bot.send_message(callback_query.from_user.id, text, reply_markup=kb)

# Кнопки покупки (только сообщение)
@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def buy_item(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    brand, qty = data[1], data[2]
    price = prices[int(qty)]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        f"Вы выбрали {brand} {qty} затяжек.\n💰 Цена: {price} ₸\n👤 Для заказа пишите: @cruiveil")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
