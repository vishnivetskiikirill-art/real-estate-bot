import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import TELEGRAM_TOKEN, DATABASE_URL
from keyboards import (
    language_keyboard,
    city_keyboard,
    varna_districts_keyboard,
    property_type_keyboard,
)
from db import (
    init_db,
    close_db,
    get_user_lang,
    set_user_lang,
    set_user_city,
    set_user_district,
    set_user_property_type,
    get_user_filters,
    fetch_properties,
)

# ❗ ОБЯЗАТЕЛЬНО ДО ХЕНДЛЕРОВ
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


TEXTS = {
    "choose_lang": {
        "ru": "Добро пожаловать! Выберите язык:",
        "en": "Welcome! Choose a language:",
        "bg": "Добре дошли! Изберете език:",
        "he": "ברוכים הבאים! בחרו שפה:",
    },
    "choose_city": {
        "ru": "Выберите город:",
        "en": "Choose a city:",
        "bg": "Изберете град:",
        "he": "בחרו עיר:",
    },
    "choose_district": {
        "ru": "Выберите район:",
        "en": "Choose a district:",
        "bg": "Изберете район:",
        "he": "בחרו אזור:",
    },
    "choose_type": {
        "ru": "Выберите тип недвижимости:",
        "en": "Choose property type:",
        "bg": "Изберете тип имот:",
        "he": "בחרו סוג נכס:",
    },
    "done": {
        "ru": "Готово ✅ Теперь нажмите /list",
        "en": "Done ✅ Now type /list",
        "bg": "Готово ✅ Сега натиснете /list",
        "he": "מוכן ✅ עכשיו כתבו /list",
    },
}


async def resolve_lang(user_id: int) -> str:
    return await get_user_lang(user_id) or "ru"


# ---------- LIFECYCLE ----------

@dp.startup()
async def on_startup():
    await init_db(DATABASE_URL)


@dp.shutdown()
async def on_shutdown():
    await close_db()


# ---------- START ----------

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)

    if not lang:
        await message.answer(TEXTS["choose_lang"]["ru"], reply_markup=language_keyboard())
        return

    await message.answer(TEXTS["choose_city"][lang], reply_markup=city_keyboard(lang))


# ---------- LANGUAGE ----------

@dp.callback_query(F.data.startswith("lang:"))
async def on_lang(call: CallbackQuery):
    await call.answer()
    lang = call.data.split(":")[1]
    await set_user_lang(call.from_user.id, lang)

    await call.message.answer(TEXTS["choose_city"][lang], reply_markup=city_keyboard(lang))


# ---------- CITY ----------

@dp.callback_query(F.data == "city:varna")
async def on_city(call: CallbackQuery):
    await call.answer()
    lang = await resolve_lang(call.from_user.id)

    await set_user_city(call.from_user.id, "varna")
    await call.message.answer(TEXTS["choose_district"][lang], reply_markup=varna_districts_keyboard(lang))


# ---------- DISTRICT ----------

@dp.callback_query(F.data.startswith("district:varna:"))
async def on_district(call: CallbackQuery):
    await call.answer()
    lang = await resolve_lang(call.from_user.id)

    district = call.data.split(":")[2]
    await set_user_district(call.from_user.id, district)

    await call.message.answer(TEXTS["choose_type"][lang], reply_markup=property_type_keyboard(lang))


# ---------- TYPE ----------

@dp.callback_query(F.data.startswith("type:"))
async def on_type(call: CallbackQuery):
    await call.answer()
    lang = await resolve_lang(call.from_user.id)

    property_type = call.data.split(":")[1]
    await set_user_property_type(call.from_user.id, property_type)

    await call.message.answer(TEXTS["done"][lang])


# ---------- LIST ----------

@dp.message(Command("list"))
async def cmd_list(message: Message):
    user_id = message.from_user.id
    lang = await resolve_lang(user_id)

    filters = await get_user_filters(user_id)
    items = await fetch_properties(
        city=filters["city"],
        district=filters["district"],
        property_type=filters["property_type"],
        limit=5,
    )

    if not items:
        await message.answer("Нет объявлений")
        return

    for p in items:
        await message.answer(
            f"#{p['id']}\n"
            f"Цена: {p.get('price')}\n"
            f"{p.get('description_ru', '')}"
        )


# ---------- MAIN ----------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
