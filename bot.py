import asynciofrom aiogram.fsm.context 
import FSMContext
from states import SearchState
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from config import BOT_TOKEN, ADMIN_ID
from texts import TEXTS
from keyboards import *
from database import connect_db, fetch, execute
from models import CREATE_PROPERTIES, CREATE_REQUESTS

bot = Bot(BOT_TOKEN)
from aiogram.fsm.storage.memory import MemoryStorage

dp = Dispatcher(storage=MemoryStorage())

user_lang = {}
user_city = {}

@dp.startup()
async def startup():
    await connect_db()
    await execute(CREATE_PROPERTIES)
    await execute(CREATE_REQUESTS)

@dp.message(F.text == "/start")
@dp.message(F.text == "Купить недвижимость")
async def start_search(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SearchState.city)

    await message.answer(
        "Выберите город:",
        reply_markup=city_keyboard  )
async def start(msg: Message):
    await msg.answer(TEXTS["ru"]["start"], reply_markup=languages())

@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(cb: CallbackQuery):
    lang = cb.data.split("_")[1]
    user_lang[cb.from_user.id] = lang
    await cb.message.edit_text(
        TEXTS[lang]["menu"],
        reply_markup=main_menu(TEXTS[lang])
    )

@dp.callback_query(F.data == "buy")
async def buy(cb: CallbackQuery):
    lang = user_lang.get(cb.from_user.id, "ru")
    await cb.message.edit_text(
        TEXTS[lang]["city"],
        reply_markup=cities()
    )

@dp.callback_query(F.data.startswith("city_"))
async def choose_city(cb: CallbackQuery):
    city = cb.data.replace("city_", "")
    user_city[cb.from_user.id] = city

    rows = await fetch(
        "SELECT DISTINCT district FROM properties WHERE city=$1",
        city
    )
    districts_list = [r["district"] for r in rows]

    await cb.message.edit_text(
        TEXTS[user_lang.get(cb.from_user.id, "ru")]["district"],
        reply_markup=districts(districts_list)
    )

@dp.callback_query(F.data.startswith("district_"))
async def show_properties(cb: CallbackQuery):
    district = cb.data.replace("district_", "")
    city = user_city.get(cb.from_user.id)

    props = await fetch(
        "SELECT * FROM properties WHERE city=$1 AND district=$2",
        city, district
    )

    for p in props:
        await bot.send_photo(
            cb.from_user.id,
            p["photo"],
            caption=f"🏠 {p['title']}\n💰 {p['price']}",
            reply_markup=request_btn(p["id"])
        )

@dp.callback_query(F.data.startswith("req_"))
async def request(cb: CallbackQuery):
    pid = int(cb.data.split("_")[1])

    await execute(
        "INSERT INTO requests (property_id, user_id, username) VALUES ($1,$2,$3)",
        pid,
        cb.from_user.id,
        cb.from_user.username
    )

    await bot.send_message(
        ADMIN_ID,
        f"📩 Новая заявка\nОбъект #{pid}\n@{cb.from_user.username}"
    )

    await cb.message.answer("✅ Заявка отправлена")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
