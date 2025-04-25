import aiohttp
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.create_bot import cfg
from bot.keyboards.menu import get_main_keyboard, get_games_keyboard, get_back_to_games_button

menu_router = Router()

class AskRules(StatesGroup):
    choosing_game = State()
    waiting_for_question = State()

@menu_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Я консультант по настольным играм.", reply_markup=get_main_keyboard())


@menu_router.message(F.text == "🎲 Спросить про правила")
@menu_router.message(F.text == "🔁 Выбрать другую игру")
async def show_game_list(message: Message, state: FSMContext):
    await state.set_state(AskRules.choosing_game)
    await message.answer("Выбери игру:", reply_markup=get_games_keyboard())


@menu_router.callback_query(F.data.startswith("game_"))
async def handle_game_choice(callback: CallbackQuery, state: FSMContext):
    game = callback.data.removeprefix("game_")
    await state.update_data(game=game)
    await state.set_state(AskRules.waiting_for_question)

    await callback.message.answer(
        f"Ты выбрал игру: <b>{game}</b>.\n\nВведи свой вопрос по правилам.",
        reply_markup=get_back_to_games_button()
    )
    await callback.answer()


@menu_router.message(AskRules.waiting_for_question)
async def handle_question(message: Message, state: FSMContext):
    data = await state.get_data()
    game = data.get("game")
    question = message.text

    # Запрос к бэкенду
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{cfg.api_url}/ask", json={"game": game, "question": question}) as resp:
                if resp.status == 200:
                    answer = (await resp.json()).get("answer", "Ответ не найден.")
                else:
                    answer = "Не удалось получить ответ. Попробуйте позже."
        except Exception as e:
            answer = f"Непредвиденная ошибка"

    await message.answer(f"<b>Ответ по игре {game}:</b>\n\n{answer}")
