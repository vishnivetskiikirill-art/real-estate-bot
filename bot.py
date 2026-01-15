from keyboards import (
    language_keyboard, city_keyboard, varna_districts_keyboard, property_type_keyboard,
    CITY_LABELS, DISTRICT_LABELS, TYPE_LABELS
)

# ... + твои импорты db: get_user_lang, set_user_lang, set_user_city, set_user_district, set_user_property_type, get_user_filters

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
}

async def resolve_lang(user_id: int) -> str:
    lang = await get_user_lang(user_id)
    return lang or "ru"


@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)

    if not lang:
        await message.answer(TEXTS["choose_lang"]["ru"], reply_markup=language_keyboard())
        return

    await message.answer(TEXTS["choose_city"][lang], reply_markup=city_keyboard(lang))


@dp.callback_query(F.data.startswith("lang:"))
async def on_lang_selected(call: CallbackQuery):
    await call.answer()
    lang = call.data.split(":", 1)[1]
    if lang not in ("ru", "en", "bg", "he"):
        lang = "ru"
    await set_user_lang(call.from_user.id, lang)

    await call.message.answer(TEXTS["choose_city"][lang], reply_markup=city_keyboard(lang))


@dp.callback_query(F.data == "city:varna")
async def on_city_selected(call: CallbackQuery):
    await call.answer()
    lang = await resolve_lang(call.from_user.id)

    await set_user_city(call.from_user.id, "varna")
    await call.message.answer(TEXTS["choose_district"][lang], reply_markup=varna_districts_keyboard(lang))


@dp.callback_query(F.data.startswith("district:varna:"))
async def on_district_selected(call: CallbackQuery):
    await call.answer()
    lang = await resolve_lang(call.from_user.id)

    district_code = call.data.split(":", 2)[2]  # center/levski/...
    await set_user_district(call.from_user.id, district_code)

    await call.message.answer(TEXTS["choose_type"][lang], reply_markup=property_type_keyboard(lang))


@dp.callback_query(F.data.startswith("type:"))
async def on_type_selected(call: CallbackQuery):
    await call.answer()
    property_type_code = call.data.split(":", 1)[1]
    await set_user_property_type(call.from_user.id, property_type_code)

    lang = await resolve_lang(call.from_user.id)
    # Можно сразу вызвать list или просто сказать
    msg = {
        "ru": "Готово ✅ Теперь нажмите /list чтобы увидеть объявления по выбранным фильтрам.",
        "en": "Done ✅ Now type /list to see listings for your filters.",
        "bg": "Готово ✅ Сега натиснете /list за обявите по филтрите.",
        "he": "מוכן ✅ עכשיו כתבו /list כדי לראות מודעות לפי המסננים.",
    }
    await call.message.answer(msg[lang])


@dp.callback_query(F.data == "back:city")
async def back_to_city(call: CallbackQuery):
    await call.answer()
    lang = await resolve_lang(call.from_user.id)
    await call.message.answer(TEXTS["choose_city"][lang], reply_markup=city_keyboard(lang))


@dp.callback_query(F.data == "back:district")
async def back_to_district(call: CallbackQuery):
    await call.answer()
    lang = await resolve_lang(call.from_user.id)
    await call.message.answer(TEXTS["choose_district"][lang], reply_markup=varna_districts_keyboard(lang))
