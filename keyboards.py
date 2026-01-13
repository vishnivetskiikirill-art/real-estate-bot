from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts import TEXTS


def languages():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇧🇬 Български", callback_data="lang_bg")],
    ])


def main_menu(lang: str = "ru"):
    t = TEXTS.get(lang, TEXTS["ru"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["buy"], callback_data="buy")],
        [InlineKeyboardButton(text=t["contact"], callback_data="contact")],
    ])


def cities():
    # Города можно оставить как есть (названия латиницей)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Varna", callback_data="city_Varna")],
        [InlineKeyboardButton(text="Burgas", callback_data="city_Burgas")],
        [InlineKeyboardButton(text="Sofia", callback_data="city_Sofia")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back_menu")],
    ])


def districts(items: list[str]):
    # items = ["Center", "Lozenets", ...]
    kb = [[InlineKeyboardButton(text=i, callback_data=f"district_{i}")] for i in items]
    kb.append([InlineKeyboardButton(text="⬅️ Back", callback_data="back_city")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def property_types(lang: str = "ru"):
    # Типы локализуем прямо тут
    if lang == "en":
        apt, house, studio = "Apartment", "House", "Studio"
        back = "Back"
    elif lang == "bg":
        apt, house, studio = "Апартамент", "Къща", "Студио"
        back = "Назад"
    else:
        apt, house, studio = "Квартира", "Дом", "Студия"
        back = "Назад"

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🏢 {apt}", callback_data="type_apartment")],
        [InlineKeyboardButton(text=f"🏠 {house}", callback_data="type_house")],
        [InlineKeyboardButton(text=f"🏬 {studio}", callback_data="type_studio")],
        [InlineKeyboardButton(text=f"⬅️ {back}", callback_data="back_district")],
    ])
