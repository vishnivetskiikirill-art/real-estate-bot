answer(msg, reply_markup=main_menu(lang))
    await call.answer()


# ----------- Назад -----------

@dp.callback_query(F.data == "back_menu")
async def back_menu(call: CallbackQuery):
    uid = call.from_user.id
    lang = lang_of(uid)
    await call.message.answer(TEXTS.get(lang, TEXTS["ru"])["menu"], reply_markup=main_menu(lang))
    await call.answer()


@dp.callback_query(F.data == "back_city")
async def back_to_city(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.answer(t(uid)["city"], reply_markup=cities())
    await call.answer()


@dp.callback_query(F.data == "back_district")
async def back_to_district(call: CallbackQuery):
    uid = call.from_user.id
    profile = get_profile(uid)
    city = profile.get("city")
    items = CITY_DISTRICTS.get(city, [])
    await call.message.answer(t(uid)["district"], reply_markup=districts(items))
    await call.answer()


# ----------- Контакты -----------

@dp.callback_query(F.data == "contact")
async def contact(call: CallbackQuery):
    uid = call.from_user.id
    lang = lang_of(uid)
    if lang == "en":
        txt = "📞 Contact agent: @your_agent_username"
    elif lang == "bg":
        txt = "📞 Контакт: @your_agent_username"
    else:
        txt = "📞 Связаться с агентом: @your_agent_username"

    await call.message.answer(txt, reply_markup=main_menu(lang))
    await call.answer()


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set in environment variables")

    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())
