import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from config import TELEGRAM_TOKEN, DATABASE_URL
from db import init_db, close_db, fetch_properties


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.startup()
async def on_startup() -> None:
    await init_db(DATABASE_URL)


@dp.shutdown()
async def on_shutdown() -> None:
    await close_db()


@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот недвижимости.\n\n"
        "Команды:\n"
        "/list — показать последние объявления"
    )


@dp.message(F.text == "/list")
async def cmd_list(message: Message):
    items = await fetch_properties(limit=5)

    if not items:
        await message.answer("Пока нет объявлений в базе.")
        return

    text_parts = []
    for p in items:
        text_parts.append(
            f"#{p['id']} • {p.get('property_type') or '—'}\n"
            f"{p.get('city') or '—'}, {p.get('district') or '—'}\n"
            f"Цена: {p.get('price') or '—'}\n"
            f"{(p.get('description_ru') or '').strip()}\n"
        )

    await message.answer("\n\n".join(text_parts))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
