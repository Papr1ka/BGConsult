from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Возвращает главное меню с кнопкой для запроса правил настольной игры.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с одной кнопкой "🎲 Спросить про правила".
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🎲 Спросить про правила")]],
        resize_keyboard=True
    )

def get_games_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает inline-клавиатуру со списком настольных игр для выбора.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками для выбора игр.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Манчкин", callback_data="game_Манчкин")],
        [InlineKeyboardButton(text="Каркассон", callback_data="game_Каркассон")],
        [InlineKeyboardButton(text="Колонизаторы", callback_data="game_Колонизаторы")]
    ])

def get_back_to_games_button() -> ReplyKeyboardMarkup:
    """
    Возвращает клавиатуру с кнопкой для выбора другой игры.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопкой "🔁 Выбрать другую игру".
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔁 Выбрать другую игру")]],
        resize_keyboard=True
    )
