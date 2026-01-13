from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts import TEXTS

# --- Справочник районов Варны: id -> отображаемое имя
VARNA_DISTRICTS = {
    "center": "Center (Център)",
    "asparuhovo": "Asparuhovo (Аспарухово)",
    "galata": "Galata (Галата)",
    "briz": "Briz (Бриз)",
    "chayka": "Chayka (Чайка)",
    "levski": "Levski (Левски)",
    "mladost": "Mladost (Младост)",
    "vazrazhdane": "Vazrazhdane (Възраждане)",
    "vladislavovo": "Vladislav Varnenchik (Владислав Варненчик)",
    "kaisieva": "Kaisieva gradina (Кайсиева градина)",
    "troshevo": "Troshevo (Трошево)",
    "pobeda": "Pobeda (Победа)",
    "izgrev": "Izgrev (Изгрев)",
    "tsveten": "Tsveten kvartal (Цветен квартал)",
    "hr_botev": "Hristo Botev (Христо Ботев)",
    "kolhozen": "Kolhozen pazar (Колхозен пазар)",
    "pogrebite": "Pogrebite (Погребите)",
    "greek": "Greek quarter (Гръцката махала)",
    "maksuda": "Maksuda (Максуда)",
    "morska": "Morska gradina (Морска градина)",
    "vinitsa": "Vinitsa (Виница)",
    "alenmak": "Alen mak (Ален мак)",
    "euxino": "Euxinograd (Евксиноград)",
    "trakata": "Trakata (Траката)",
    "zprom": "Zapadna prom. zona (Западна пром. зона)",
    "st_ivan": "St. Ivan Rilski (Св. Иван Рилски)",
    "golden": "Golden Sands (Златни пясъци)",
    "konst": "Konstantin i Elena (Константин и Елена)",
}

# --- Типы: id -> (ru, en, bg)
PROPERTY_TYPES = {
    "apartment": ("🏢 Квартира", "🏢 Apartment", "🏢 Апартамент"),
    "house": ("🏠 Дом", "🏠 House", "🏠 Къща"),
    "studio": ("🏬 Студия", "🏬 Studio", "🏬 Студио"),
}


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


def cities():
    # Пока только Варна
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Varna", callback_data="city:varna")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="nav:menu")],
    ])


def districts_varna():
    kb = []
    for did, title in VARNA_DISTRICTS.items():
        kb.append([InlineKeyboardButton(text=title, callback_data=f"dist:{did}")])
    kb.append([InlineKeyboardButton(text="⬅️ Back", callback_data="nav:city")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def property_types(lang: str = "ru"):
    if lang not in ("ru", "en", "bg"):
        lang = "ru"
    idx = {"ru": 0, "en": 1, "bg": 2}[lang]

    kb = []
    for tid, labels in PROPERTY_TYPES.items():
        kb.append([InlineKeyboardButton(text=labels[idx], callback_data=f"type:{tid}")])
    kb.append([InlineKeyboardButton(text="⬅️ Back", callback_data="nav:dist")])
    return InlineKeyboardMarkup(inline_keyboard=kb)
