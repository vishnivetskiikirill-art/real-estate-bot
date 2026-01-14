import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from config import TELEGRAM_TOKEN
from texts import TEXTS
from keyboards import languages

# ВАЖНО: импорт именно так, из db/db.py
from db.db import init_db, close_db, fetch_properties


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Храним язык/город пользователя (по user_id)
user_lang: dict[int, str] = {}
user_city: dict[int, str] = {}


@dp.startup()
async def on_startup():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set in Railway Variables")

    await init_db(database_url)
    logging.info("DB connected")


@dp.shutdown()
async def on_shutdown():
    await close_db()
    logging.info("DB closed")


@dp.message(CommandStart())
async def start_cmd(message: Message):
    # язык по умолчанию ru
    user_lang[message.from_user.id] = "ru"
    await message.answer(TEXTS["ru"]["start"], reply_markup=languages())


@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(callback: CallbackQuery):
    lang = callback.data.split("_", 1)[1]  # lang_ru / lang_en
    user_lang[callback.from_user.id] = lang

    await callback.message.answer(TEXTS[lang].get("lang_set", "Язык выбран ✅"))
    await callback.answer()


# Пример команды, чтобы проверить что БД реально работает:
# (можешь потом убрать)
@dp.message(F.text == "тест")
async def test_db(message: Message):
    rows = await fetch_properties()  # без фильтров
    await message.answer(f"В базе объявлений: {len(rows)}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
