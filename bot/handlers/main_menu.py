import logging

import aiohttp
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiohttp import FormData

from bot.create_bot import cfg, logger

# user интерфейс
from bot.keyboards.user_keyboards import (
    get_main_keyboard, get_back_to_games_button, get_grade_keyboard, create_games_keyboard
)

# админ интерфейс
from bot.keyboards.admin_keyboards import (
    get_admin_panel_keyboard, create_delete_games_keyboard
)


menu_router = Router()

class AskRules(StatesGroup):
    choosing_game = State()
    waiting_for_question = State()
    awaiting_rating = State()

class AdminPanel(StatesGroup):
    waiting_for_game_name = State()
    waiting_for_game_url = State()
    waiting_for_pdf = State()
    choosing_game_to_delete = State()


@menu_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    logger.error(f"cfg {cfg.admin_whitelist}")
    logger.error(f"message.from_user.id {message.from_user.id}")
    logger.error(f"message.from_user.id in cfg.admin_whitelist {message.from_user.id in cfg.admin_whitelist}")
    await state.clear()
    await message.answer("Привет! Я консультант по настольным играм.", reply_markup=get_main_keyboard(message.from_user.id in cfg.admin_whitelist))

@menu_router.message(F.text == "🔁 Выбрать другую игру")
@menu_router.message(F.text == "🎲 Спросить про правила")
async def ask_rules(message: Message, state: FSMContext):
    await state.set_state(AskRules.choosing_game)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.api_url}/list_games") as resp:
            games = await resp.json()

    await message.answer("Выбери игру:", reply_markup=create_games_keyboard(games))


@menu_router.callback_query(F.data.startswith("game_"))
async def handle_game_choice(callback: CallbackQuery, state: FSMContext):
    game = callback.data.removeprefix("game_")
    await state.update_data(game=game)
    await state.set_state(AskRules.waiting_for_question)
    await callback.message.answer(
        f"Ты выбрал: <b>{game}</b>. Задавай свой вопрос.",
        reply_markup=get_back_to_games_button()
    )
    await callback.answer()

@menu_router.message(F.text == "Завершить диалог")
async def finish_dialog(message: Message, state: FSMContext):
    await state.set_state(AskRules.awaiting_rating)
    await message.answer("Пожалуйста, оцени мою работу от 1 до 5", reply_markup=get_grade_keyboard())

@menu_router.message(AskRules.waiting_for_question)
async def handle_question(message: Message, state: FSMContext):
    data = await state.get_data()
    game = data["game"]
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{cfg.api_url}/get_answer", json={
            "game_name": game,
            "question": message.text,
            "user_id": message.from_user.id,
            "user_name": message.from_user.username
        }) as resp:
            answer = (await resp.json()).get("answer", "Ошибка получения ответа.")
    await message.answer(f"<b>Ответ по игре {game}:</b>\n\n{answer}", reply_markup=get_back_to_games_button())


@menu_router.callback_query(F.data.startswith("grade_"))
async def handle_rating(callback: CallbackQuery, state: FSMContext):
    rating = int(callback.data.removeprefix("grade_"))
    await callback.answer("Спасибо за оценку!")
    async with aiohttp.ClientSession() as session:
        await session.post(f"{cfg.api_url}/rate/", json={
            "user_id": callback.from_user.id,
            "rating": rating
        })
    await state.clear()
    await callback.message.answer("Спасибо за участие! Нажми /start, чтобы начать заново.")


@menu_router.message(F.text == "🛠 Админ панель")
async def admin_panel(message: Message, state: FSMContext):
    if message.from_user.id not in cfg.admin_whitelist:
        return await message.answer("Нет доступа.")

    await message.answer("Админ панель:", reply_markup=get_admin_panel_keyboard())


@menu_router.message(F.text == "➕ Добавить игру (PDF)")
async def start_add_game(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.waiting_for_game_name)
    await message.answer("Введите название игры:")


@menu_router.message(AdminPanel.waiting_for_game_name)
async def receive_game_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AdminPanel.waiting_for_game_url)
    await message.answer("Теперь введите URL с правилами игры:")

@menu_router.message(AdminPanel.waiting_for_game_url)
async def receive_game_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text.strip())
    await state.set_state(AdminPanel.waiting_for_pdf)
    await message.answer("Отправьте PDF-файл с правилами:")


@menu_router.message(AdminPanel.waiting_for_pdf)
async def receive_game_pdf(message: Message, state: FSMContext):
    if not message.document or not message.document.file_name.endswith(".pdf"):
        return await message.answer("Файл должен быть в формате PDF.")

    file = await message.bot.download(message.document)
    data = await state.get_data()

    from aiohttp import FormData
    form = FormData()
    form.add_field("name", data["name"])
    form.add_field("url", data["url"])
    form.add_field(
        name="file",
        value=file,
        filename=message.document.file_name,
        content_type="application/pdf"
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{cfg.api_url}/upload_pdf/", data=form) as resp:
            status = "Файл загружен." if resp.status == 200 else f"Ошибка загрузки. Статус: {resp.status}"

    await message.answer(status)
    await state.clear()




@menu_router.message(F.text == "➖ Удалить игру")
async def delete_game_prompt(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.choosing_game_to_delete)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.api_url}/list_games") as resp:
            games = await resp.json()

    await message.answer("Выбери игру для удаления:", reply_markup=create_delete_games_keyboard(games))

@menu_router.callback_query(F.data.startswith("delete_"))
async def delete_game(callback: CallbackQuery, state: FSMContext):
    filename = callback.data.removeprefix("delete_")
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{cfg.api_url}/delete_pdf/{filename}") as resp:
            msg = "Удалено." if resp.status == 200 else "Ошибка удаления."
    await callback.message.answer(msg)
    await state.clear()
