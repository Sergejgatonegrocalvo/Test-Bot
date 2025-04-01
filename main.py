import logging
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# 🔹 Токен бота (замени на свой!)
TOKEN = "7600848578:AAH__wUdYmeRYZ751qNssAs8x_K1ubn2mJE"

# 🔹 Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔹 Главное меню с кнопками (не меняю "Контакты"!)
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🩺 Терапевт"), KeyboardButton(text="🦷 Стоматология")],
        [KeyboardButton(text="👁 Офтальмология"), KeyboardButton(text="❤️ Кардиология")],
        [KeyboardButton(text="📞 Администратор"), KeyboardButton(text="📍 Контакты")]
    ],
    resize_keyboard=True
)

# 🔹 База специалистов и ключевых слов
SCENARIOS = {
    "терапевт": ["терапевт", "врач", "простуда", "температура", "болит горло"],
    "стоматология": ["стоматолог", "зуб", "болит зуб", "кариес", "зубной"],
    "офтальмология": ["офтальмолог", "глаз", "зрение", "плохо вижу"],
    "кардиология": ["кардиолог", "сердце", "давление", "тахикардия"]
}

RESPONSES = {
    "терапевт": "Вы записаны к терапевту! Врач скоро подключится.",
    "стоматология": "🦷 Вас перевели в отдел стоматологии. Ожидайте ответа специалиста.",
    "офтальмология": "👁 Вас перевели в офтальмологию. Врач свяжется с вами в ближайшее время.",
    "кардиология": "❤️ Вас переключили на кардиолога. Ожидайте ответа.",
    "администратор": "📞 Сейчас Вам перезвонит Администратор.",
    "не найдено": "📞 Сейчас с Вами свяжется Администратор.",
    "контакты": "📌 Адрес клиники: ул. Примерная, 10. Телефон: +7 (900) 123-45-67."
}

# 🔹 Загрузка базы FAQ
def load_faq():
    try:
        with open("faq.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка при загрузке FAQ: {e}")
        return {}

# 🔹 Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("👋 Добрый день! Какой у вас вопрос?", reply_markup=menu)

# 🔹 Обработка кнопки "📞 Администратор"
@dp.message(lambda message: message.text == "📞 Администратор")
async def admin_contact(message: types.Message):
    await message.answer(RESPONSES["администратор"])
    await message.answer("Если вам нужно что-то другое, выберите специалиста из меню.", reply_markup=menu)  # Возвращаем меню

# 🔹 Обработка кнопки "📍 Контакты"
@dp.message(lambda message: message.text == "📍 Контакты")
async def contacts_info(message: types.Message):
    await message.answer(RESPONSES["контакты"])
    await message.answer("Если вам нужно что-то другое, выберите специалиста из меню.", reply_markup=menu)  # Возвращаем меню

# 🔹 Обработка сообщений (поиск врача или вызов администратора)
@dp.message()
async def handle_user_message(message: types.Message):
    user_message = message.text.lower().strip()
    faq = load_faq()

    # Проверяем FAQ
    if user_message in faq:
        await message.answer(faq[user_message])
        await message.answer("Если вам нужно что-то другое, выберите специалиста из меню.", reply_markup=menu)
        return

    # Проверяем, есть ли специалист в базе
    for specialist, keywords in SCENARIOS.items():
        if any(keyword in user_message for keyword in keywords):
            await message.answer(RESPONSES[specialist])
            await message.answer("Если вам нужно что-то другое, выберите специалиста из меню.", reply_markup=menu)
            return

    # Если специалист не найден — отвечает администратор
    await message.answer(RESPONSES["не найдено"])
    await message.answer("Если вам нужно что-то другое, выберите специалиста из меню.", reply_markup=menu)  # Возвращаем меню

# 🔹 Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())