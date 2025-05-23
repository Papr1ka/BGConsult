from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text="🎲 Спросить про правила")]]
    if is_admin:
        buttons.append([KeyboardButton(text="🛠 Админ панель")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_back_to_games_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Выбрать другую игру")],
            [KeyboardButton(text="Завершить диалог")]
        ],
        resize_keyboard=True
    )

def get_grade_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f"grade_{i}")] for i in range(1, 6)
    ])

def create_games_keyboard(games: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=game, callback_data=f"game_{game}")] for game in games]
    )
