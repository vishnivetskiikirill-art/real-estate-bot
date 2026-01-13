import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery

from texts import TEXTS
from keyboards import (
    languages,
    main_menu,
    cities,
    districts_varna,
    property_types,
    VARNA_DISTRICTS,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

# user_id -> {"lang": "ru", "city": "varna", "district_id": "center", "type": "apartment"}
user_state: dict[int, dict] = {}


def profile(uid: int) -> dict:
    if uid not in user_state:
        user_state[uid] = {"lang": "ru", "city": None, "district_id": None, "type": None}
    return user_state[uid]


def lang(uid: int) -> str:
    return profile(uid).get("lang", "ru")


def tr(uid: int) -> dict:
    return TEXTS.get(lang(uid), TEXTS["ru"])


# ---------- /start ----------
@dp.message(F.text == "/start")
async def start_cmd(message: Message):
    # показываем выбор языка
    await message.answer(TEXTS["ru"]["start"], reply_markup=languages())


# ---------- language ----------
@dp.callback_query(F.data.startswith("lang:"))
async def cb_lang(call: CallbackQuery):
    uid = call.from_user.id
    p = profile(uid)

    p["lang"] = call.data.split(":", 1)[1]  # ru/en/bg
    p["city"] = None
    p["district_id"] = None
    p["type"] = None

    await call.message.answer(TEXTS[p["lang"]]["menu"], reply_markup=main_menu(p["lang"]))
    await call.answer()


# ---------- menu actions ----------
@dp.callback_query(F.data == "act:buy")
async def cb_buy(call: CallbackQuery):
    uid = call.from_user.id
    p = profile(uid)

    p["city"] = None
    p["district_id"] = None
    p["type"] = None

    await call.message.answer(tr(uid)["city"], reply_markup=cities(lang(uid)))
    await call.answer()


@dp.callback_query(F.data == "act:contact")
async def cb_contact(call: CallbackQuery):
    uid = call.from_user.id
    l = lang(uid)

    if l == "en":
        txt = "📞 Contact agent: @your_agent_username"
    elif l == "bg":
        txt = "📞 Контакт: @your_agent_username"
    else:
        txt = "📞 Связаться с агентом: @your_agent_username"

    await call.message.answer(txt, reply_markup=main_menu(l))
    await call.answer()


# ---------- city ----------
@dp.callback_query(F.data == "city:varna")
async def cb_city(call: CallbackQuery):
    uid = call.from_user.id
    p = profile(uid)

    p["city"] = "varna"
    p["district_id"] = None
    p["type"] = None

    await call.message.answer(tr(uid)["district"], reply_markup=districts_varna(lang(uid)))
    await call.answer()


# ---------- district ----------
@dp.callback_query(F.data.startswith("dist:"))
async def cb_district(call: CallbackQuery):
    uid = call.from_user.id
    p = profile(uid)

    dist_id = call.data.split(":", 1)[1]
    if dist_id not in VARNA_DISTRICTS:
        await call.answer("Unknown district", show_alert=True)
        return

    p["district_id"] = dist_id
    p["type"] = None

    l = lang(uid)
    if l == "en":
        prompt = "Choose property type:"
    elif l == "bg":
        prompt = "Изберете тип имот:"
    else:
        prompt = "Выберите тип недвижимости:"

    await call.message.answer(prompt, reply_markup=property_types(l))
    await call.answer()


# ---------- type ----------
@dp.callback_query(F.data.startswith("type:"))
async def cb_type(call: CallbackQuery):
    uid = call.from_user.id
    p = profile(uid)

    ptype = call.data.split(":", 1)[1]
    p["type"] = ptype

    l = lang(uid)

    # Красивое название района по языку
    names = VARNA_DISTRICTS.get(p["district_id"])
    if names:
        district_title = names[{"ru": 0, "en": 1, "bg": 2}.get(l, 0)]
    else:
        district_title = p["district_id"]

    # Название города по языку
    city_title = "Varna" if l == "en" else "Варна"

    if l == "en":
        msg = (
            f"✅ Selected:\n"
            f"City: {city_title}\n"
            f"District: {district_title}\n"
            f"Type: {ptype}\n\n"
            f"Next: show listings from DB."
        )
    elif l == "bg":
        msg = (
            f"✅ Избрано:\n"
            f"Град: {city_title}\n"
            f"Квартал: {district_title}\n"
            f"Тип: {ptype}\n\n"
            f"Следващо: обяви от базата."
        )
    else:
        msg = (
            f"✅ Выбрано:\n"
            f"Город: {city_title}\n"
            f"Район: {district_title}\n"
            f"Тип: {ptype}\n\n"
            f"Дальше: покажем объекты из базы."
        )

    await call.message.answer(msg, reply_markup=main_menu(l))
    await call.answer()


# ---------- navigation (back) ----------
@dp.callback_query(F.data == "nav:menu")
async def nav_menu(call: CallbackQuery):
    uid = call.from_user.id
    l = lang(uid)
    await call.message.answer(TEXTS.get(l, TEXTS["ru"])["menu"], reply_markup=main_menu(l))
    await call.answer()


@dp.callback_query(F.data == "nav:city")
async def nav_city(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.answer(tr(uid)["city"], reply_markup=cities(lang(uid)))
    await call.answer()


@dp.callback_query(F.data == "nav:dist")
async def nav_dist(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.answer(tr(uid)["district"], reply_markup=districts_varna(lang(uid)))
    await call.answer()


# ---------- entry ----------
async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
