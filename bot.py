import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_ID
from texts import TEXTS
from keyboards import *
from database import connect_db, fetch, execute
from models import CREATE_PROPERTIES, CREATE_REQUESTS
from states import SearchState


# --- BOT & DISPATCHER ---
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# --- STARTUP ---
@dp.startup()
async def startup():
    await connect_db()
    await execute(CREATE_PROPERTIES)
    await execute(CREATE_REQUESTS)


# --- /start ---
@dp.message(F.text == "/start")
async def start(msg: Message):
    await msg.answer(TEXTS["ru"]["start"], reply_markup=languages())


# --- LANGUAGE ---
user_lang = {}

@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(cb: CallbackQuery):
    await cb.answer()  # 🔴 ОБЯЗАТЕЛЬНО

    lang = cb.data.split("_")[1]
    user_lang[cb.from_user.id] = lang

    await cb.message.edit_text(
        TEXTS[lang]["menu"],
        reply_markup=main_menu(lang)
    )

# --- BUY PROPERTY (START FSM) ---
@dp.message(F.text == "Купить недвижимость")
async def start_search(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SearchState.city)

    await message.answer(
        "Выберите город:",
        reply_markup=city_keyboard
    )


# --- CITY ---
@dp.message(SearchState.city)
async def choose_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(SearchState.district)

    await message.answer(
        "Выберите район:",
        reply_markup=district_keyboard
    )


# --- DISTRICT ---
@dp.message(SearchState.district)
async def choose_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(SearchState.property_type)

    await message.answer(
        "Тип недвижимости:",
        reply_markup=type_keyboard
    )


# --- TYPE ---
@dp.message(SearchState.property_type)
async def choose_type(message: Message, state: FSMContext):
    await state.update_data(property_type=message.text)
    await state.set_state(SearchState.price)

    await message.answer(
        "Выберите бюджет:",
        reply_markup=price_keyboard
    )


# --- PRICE (TEST OUTPUT) ---
@dp.message(SearchState.price)
async def choose_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()

    await message.answer(
        "🔎 Поиск недвижимости:\n\n"
        f"Город: {data['city']}\n"
        f"Район: {data['district']}\n"
        f"Тип: {data['property_type']}\n"
        f"Бюджет: {data['price']}"
    )

    await state.clear()


# --- RUN ---
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
