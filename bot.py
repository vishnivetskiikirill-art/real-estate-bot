from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN, DATABASE_URL
from db import init_db, close_db, fetch_properties

dp = Dispatcher()


# --- Клавиатуры ---
def kb_languages() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇧🇬 Български", callback_data="lang:bg")],
    ])


def kb_main(lang: str) -> InlineKeyboardMarkup:
    caption = {
        "ru": "🏠 Показать квартиры",
        "en": "🏠 Show listings",
        "bg": "🏠 Покажи обяви",
    }[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=caption, callback_data="show")],
    ])


# --- Память по пользователям (простая) ---
user_lang: dict[int, str] = {}


def get_lang(uid: int) -> str:
    return user_lang.get(uid, "ru")


def pick_desc(row: dict, lang: str) -> str:
    # если пусто — fallback на ru
    if lang == "ru":
        return row.get("description_ru") or ""
    if lang == "en":
        return row.get("description_en") or row.get("description_ru") or ""
    if lang == "bg":
        return row.get("description_bg") or row.get("description_ru") or ""
    return row.get("description_ru") or ""


# --- Handlers ---
@dp.startup()
async def on_startup():
    await init_db(DATABASE_URL)


@dp.shutdown()
async def on_shutdown():
    await close_db()


@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "Выберите язык / Choose language / Изберете език:",
        reply_markup=kb_languages(),
    )


@dp.callback_query(F.data.startswith("lang:"))
async def set_language(call: CallbackQuery):
    lang = call.data.split(":")[1]
    user_lang[call.from_user.id] = lang

    welcome = {
        "ru": "Готово ✅ Нажмите кнопку, чтобы посмотреть квартиры.",
        "en": "Done ✅ Tap the button to see listings.",
        "bg": "Готово ✅ Натиснете бутона за обяви.",
    }[lang]

    await call.message.answer(welcome, reply_markup=kb_main(lang))
    await call.answer()


@dp.callback_query(F.data == "show")
async def show_listings(call: CallbackQuery):
    uid = call.from_user.id
    lang = get_lang(uid)

    rows = await fetch_properties(limit=10)

    if not rows:
        msg = {
            "ru": "Пока нет объявлений в базе.",
            "en": "No listings in the database yet.",
            "bg": "Все още няма обяви в базата.",
        }[lang]
        await call.message.answer(msg, reply_markup=kb_main(lang))
        await call.answer()
        return

    for r in rows:
        title = (r.get("title") or f"Объект #{r.get('id')}").strip()
        price = r.get("price")
        city = (r.get("city") or "Varna").strip()
        district = (r.get("district") or "").strip()
        photo_link = (r.get("photo") or "").strip()
        desc = pick_desc(r, lang).strip()

        # безопасно на случай None
        price_text = str(price) if price is not None else "—"

        text_lines = [
            f"<b>{title}</b>",
            f"💶 Цена: <b>{price_text}</b>",
            f"📍 {city}" + (f" • {district}" if district else ""),
        ]
        if desc:
            text_lines.append("")
            text_lines.append(desc)

        if photo_link:
            text_lines.append("")
            # ссылка на папку/фото
            label = {"ru": "Фото/папка", "en": "Photos/folder", "bg": "Снимки/папка"}[lang]
            text_lines.append(f"📸 {label}: {photo_link}")

        await call.message.answer("\n".join(text_lines))

    await call.answer()


if __name__ == "__main__":
    import asyncio

    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
