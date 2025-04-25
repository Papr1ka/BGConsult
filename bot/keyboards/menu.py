from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🎲 Спросить про правила")]],
        resize_keyboard=True
    )

def get_games_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Манчкин", callback_data="game_Манчкин")],
        [InlineKeyboardButton(text="Каркассон", callback_data="game_Каркассон")],
        [InlineKeyboardButton(text="Колонизаторы", callback_data="game_Колонизаторы")]
    ])

def get_back_to_games_button():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔁 Выбрать другую игру")]],
        resize_keyboard=True
    )
