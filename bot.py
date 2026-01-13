import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery

from texts import TEXTS
from keyboards import languages, main_menu, cities, districts, property_types

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

CITY_DISTRICTS = {
    "Varna": [
        "Center (Център)",
        "Asparuhovo (Аспарухово)",
        "Galata (Галата)",
        "Briz (Бриз)",
        "Chayka (Чайка)",
        "Levski (Левски)",
        "Mladost (Младост)",
        "Vazrazhdane (Възраждане)",
        "Vladislav Varnenchik / Vladislavovo (Владислав Варненчик)",
        "Kaisieva Gradina (Кайсиева градина)",
        "Troshevo (Трошево)",
        "Pobeda (Победа)",
        "Izgrev (Изгрев)",
        "Tsveten kvartal (Цветен квартал)",
        "Hristo Botev (Христо Ботев)",
        "Kolhozen pazar (Колхозен пазар)",
        "Pogrebite (Погребите)",
        "Greek quarter (Гръцката махала)",
        "Maksuda (Максуда)",
        "Morska gradina (Морска градина)",
        "Vinitsa (Виница)",
        "Alen Mak (Ален мак)",
        "Euxinograd (Евксиноград)",
        "Trakata (Траката)",
        "Zapadna promishlena zona (Западна промишлена зона)",
        "St. Ivan Rilski (Свети Иван Рилски)",
        "Golden Sands (Златни пясъци)",
        "Golden Sands Park (Златни пясъци - парк)",
        "Riviera (Ривиера)",
        "Konstantin i Elena (Константин и Елена)",
        "Slanchev den (Слънчев ден)",
        "Chayka resort (Чайка - курорт)",
    ]
}

def get_profile(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "lang": "ru",
            "city": None,
            "district": None,
            "type": None,
        }
    return user_data[user_id]

def get_lang(user_id):
    return get_profile(user_id)["lang"]

def tr(user_id):
    return TEXTS.get(get_lang(user_id), TEXTS["ru"])

dp = Dispatcher()

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(TEXTS["ru"]["start"], reply_markup=languages())

@dp.callback_query(F.data.startswith("city_"))
async def pick_city(call: CallbackQuery):
    uid = call.from_user.id
    city = call.data.replace("city_", "")
    p = get_profile(uid)
    p["city"] = city

    await call.message.answer(
        tr(uid)["district"],
        reply_markup=districts(CITY_DISTRICTS[city])
    )

    # ВАЖНО: закрываем "Загрузка..."
    await call.answer()
@dp.callback_query(F.data == "buy")
async def buy(call: CallbackQuery):
    uid = call.from_user.id
    p = get_profile(uid)
    p["city"] = None
    p["district"] = None
    p["type"] = None
    await call.message.answer(tr(uid)["city"], reply_markup=cities())
    await call.answer()

@dp.callback_query(F.data.startswith("city_"))
async def pick_city(call: CallbackQuery):
    uid = call.from_user.id
    city = call.data.replace("city_", "")
    p = get_profile(uid)
    p["city"] = city
    await call.message.answer(tr(uid)["district"], reply_markup=districts(CITY_DISTRICTS[city]))
    await call.answer()

@dp.callback_query(F.data.startswith("district_"))
async def pick_district(call: CallbackQuery):
    uid = call.from_user.id
    p = get_profile(uid)
    p["district"] = call.data.replace("district_", "")
    lang = get_lang(uid)
    txt = "Выберите тип недвижимости:" if lang == "ru" else "Choose property type:"
    await call.message.answer(txt, reply_markup=property_types(lang))
    await call.answer()

@dp.callback_query(F.data.startswith("type_"))
async def pick_type(call: CallbackQuery):
    uid = call.from_user.id
    p = get_profile(uid)
    p["type"] = call.data.replace("type_", "")
    lang = get_lang(uid)
    await call.message.answer(
        f"✅ {p['city']} / {p['district']} / {p['type']}",
        reply_markup=main_menu(lang)
    )
    await call.answer()

async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
