from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- Локализованные подписи ----------

LANG_LABELS = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "bg": "🇧🇬 Български",
    "he": "🇮🇱 עברית",
}

CITY_LABELS = {
    "varna": {
        "ru": "🏙 Варна",
        "en": "🏙 Varna",
        "bg": "🏙 Варна",
        "he": "🏙 ורנה",
    }
}

DISTRICT_LABELS = {
    # КОД -> подписи на 4 языках
    "center": {
        "ru": "Центр",
        "en": "Center",
        "bg": "Център",
        "he": "מרכז",
    },
    "levski": {
        "ru": "Левски",
        "en": "Levski",
        "bg": "Левски",
        "he": "לבסקי",
    },
    "chaika": {
        "ru": "Чайка",
        "en": "Chayka",
        "bg": "Чайка",
        "he": "צ'איקה",
    },
    "vladislavovo": {
        "ru": "Владиславово",
        "en": "Vladislavovo",
        "bg": "Владиславово",
        "he": "ולדיסלבובו",
    },
    "asparuhovo": {
        "ru": "Аспарухово",
        "en": "Asparuhovo",
        "bg": "Аспарухово",
        "he": "אספרוחובו",
    },
    "briz": {
        "ru": "Бриз",
        "en": "Briz",
        "bg": "Бриз",
        "he": "בריז",
    },
    "mladost": {
        "ru": "Младост",
        "en": "Mladost",
        "bg": "Младост",
        "he": "מלאדוסט",
    },
    "troshevo": {
        "ru": "Трошево",
        "en": "Troshevo",
        "bg": "Трошево",
        "he": "טרושבו",
    },
    "galata": {
        "ru": "Галата",
        "en": "Galata",
        "bg": "Галата",
        "he": "גלאטה",
    },
    "vinitsa": {
        "ru": "Виница",
        "en": "Vinitsa",
        "bg": "Виница",
        "he": "ויניצה",
    },
}

TYPE_LABELS = {
    "apartment": {
        "ru": "🏠 Квартира",
        "en": "🏠 Apartment",
        "bg": "🏠 Апартамент",
        "he": "🏠 דירה",
    },
    "house": {
        "ru": "🏡 Дом",
        "en": "🏡 House",
        "bg": "🏡 Къща",
        "he": "🏡 בית",
    },
    "studio": {
        "ru": "🏢 Студия",
        "en": "🏢 Studio",
        "bg": "🏢 Студио",
        "he": "🏢 סטודיו",
    },
    "commercial": {
        "ru": "🏬 Коммерческая",
        "en": "🏬 Commercial",
        "bg": "🏬 Търговски",
        "he": "🏬 מסחרי",
    },
}

UI = {
    "back_city": {"ru": "↩️ Назад к городу", "en": "↩️ Back to city", "bg": "↩️ Назад към града", "he": "↩️ חזרה לעיר"},
    "back_district": {"ru": "↩️ Назад к районам", "en": "↩️ Back to districts", "bg": "↩️ Назад към районите", "he": "↩️ חזרה לאזורים"},
}


# ---------- Клавиатуры ----------

def language_keyboard() -> InlineKeyboardMarkup:
    # выбор языка одинаковый для всех
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=LANG_LABELS["ru"], callback_data="lang:ru")],
            [InlineKeyboardButton(text=LANG_LABELS["en"], callback_data="lang:en")],
            [InlineKeyboardButton(text=LANG_LABELS["bg"], callback_data="lang:bg")],
            [InlineKeyboardButton(text=LANG_LABELS["he"], callback_data="lang:he")],
        ]
    )


def city_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CITY_LABELS["varna"][lang], callback_data="city:varna")],
        ]
    )


def varna_districts_keyboard(lang: str) -> InlineKeyboardMarkup:
    # порядок районов — как ты хочешь показывать
    order = ["center", "levski", "chaika", "vladislavovo", "asparuhovo", "briz", "mladost", "troshevo", "galata", "vinitsa"]

    keyboard = []
    for code in order:
        keyboard.append([InlineKeyboardButton(text=DISTRICT_LABELS[code][lang], callback_data=f"district:varna:{code}")])

    keyboard.append([InlineKeyboardButton(text=UI["back_city"][lang], callback_data="back:city")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def property_type_keyboard(lang: str) -> InlineKeyboardMarkup:
    order = ["apartment", "house", "studio", "commercial"]
    keyboard = []
    for code in order:
        keyboard.append([InlineKeyboardButton(text=TYPE_LABELS[code][lang], callback_data=f"type:{code}")])

    keyboard.append([InlineKeyboardButton(text=UI["back_district"][lang], callback_data="back:district")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
