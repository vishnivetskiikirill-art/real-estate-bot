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
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Varna", callback_data="city_Varna")],
        [InlineKeyboardButton(text="Burgas", callback_data="city_Burgas")],
        [InlineKeyboardButton(text="Sofia", callback_data="city_Sofia")],
    ])


def districts(items: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i, callback_data=f"district_{i}")]
            for i in items
        ]
    )


def request_btn(pid: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Связаться", callback_data=f"request_{pid}")]
    ])
