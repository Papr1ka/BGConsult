from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_panel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="➕ Добавить игру (PDF)")],
        [KeyboardButton(text="➖ Удалить игру")],
    ], resize_keyboard=True)

def create_delete_games_keyboard(games: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=game, callback_data=f"delete_{game}")]
        for game in games
    ])
    return keyboard

