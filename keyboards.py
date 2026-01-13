from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts import TEXTS

# Районы Варны: id -> (ru, en, bg)
VARNA_DISTRICTS = {
    "center": ("Центр", "Center", "Център"),
    "asparuhovo": ("Аспарухово", "Asparuhovo", "Аспарухово"),
    "galata": ("Галата", "Galata", "Галата"),
    "briz": ("Бриз", "Briz", "Бриз"),
    "chayka": ("Чайка", "Chayka", "Чайка"),
    "levski": ("Левски", "Levski", "Левски"),
    "mladost": ("Младост", "Mladost", "Младост"),
    "vazrazhdane": ("Возрождение", "Vazrazhdane", "Възраждане"),
    "vladislavovo": ("Владиславово", "Vladislavovo", "Владислав Варненчик"),
    "kaisieva": ("Кайсиева градина", "Kaisieva gradina", "Кайсиева градина"),
    "troshevo": ("Трошево", "Troshevo", "Трошево"),
    "pobeda": ("Победа", "Pobeda", "Победа"),
    "izgrev": ("Изгрев", "Izgrev", "Изгрев"),
    "tsveten": ("Цветен квартал", "Tsveten kvartal", "Цветен квартал"),
    "hr_botev": ("Христо Ботев", "Hristo Botev", "Христо Ботев"),
    "kolhozen": ("Колхозен пазар", "Kolhozen pazar", "Колхозен пазар"),
    "pogrebite": ("Погребите", "Pogrebite", "Погребите"),
    "greek": ("Греческий квартал", "Greek quarter", "Гръцката махала"),
    "maksuda": ("Максуда", "Maksuda", "Максуда"),
    "morska": ("Морской сад", "Sea Garden", "Морската градина"),
    "vinitsa": ("Виница", "Vinitsa", "Виница"),
    "alenmak": ("Ален мак", "Alen Mak", "Ален мак"),
    "euxino": ("Евксиноград", "Euxinograd", "Евксиноград"),
    "trakata": ("Траката", "Trakata", "Траката"),
    "golden": ("Золотые пески", "Golden Sands", "Златни пясъци"),
    "konst": ("Константин и Елена", "St. Constantine & Helena", "Св. св. Константин и Елена"),
}

# Типы: id -> (ru, en, bg)
PROPERTY_TYPES = {
    "apartment": ("🏢 Квартира", "🏢 Apartment", "🏢 Апартамент"),
    "house": ("🏠 Дом", "🏠 House", "🏠 Къща"),
    "studio": ("🏬 Студия", "🏬 Studio", "🏬 Студио"),
}


def _idx(lang: str) -> int:
    return {"ru": 0, "en": 1, "bg": 2}.get(lang, 0)


def languages():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇧🇬 Български", callback_data="lang:bg")],
    ])


def main_menu(lang: str = "ru"):
    t = TEXTS.get(lang, TEXTS["ru"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["buy"], callback_data="act:buy")],
        [InlineKeyboardButton(text=t["contact"], callback_data="act:contact")],
    ])


def cities(lang: str = "ru"):
    i = _idx(lang)
    city_name = ("Варна", "Varna", "Варна")[i]
    back = ("⬅️ Назад", "⬅️ Back", "⬅️ Назад")[i]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=city_name, callback_data="city:varna")],
        [InlineKeyboardButton(text=back, callback_data="nav:menu")],
    ])


def districts_varna(lang: str = "ru"):
    i = _idx(lang)
    back = ("⬅️ Назад", "⬅️ Back", "⬅️ Назад")[i]

    kb = []
    for did, names in VARNA_DISTRICTS.items():
        kb.append([InlineKeyboardButton(text=names[i], callback_data=f"dist:{did}")])

    kb.append([InlineKeyboardButton(text=back, callback_data="nav:city")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def property_types(lang: str = "ru"):
    i = _idx(lang)
    back = ("⬅️ Назад", "⬅️ Back", "⬅️ Назад")[i]

    kb = []
    for tid, labels in PROPERTY_TYPES.items():
        kb.append([InlineKeyboardButton(text=labels[i], callback_data=f"type:{tid}")])

    kb.append([InlineKeyboardButton(text=back, callback_data="nav:dist")])
    return InlineKeyboardMarkup(inline_keyboard=kb)
