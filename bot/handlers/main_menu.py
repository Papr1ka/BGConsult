import logging

import aiohttp
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.create_bot import cfg, logger
from bot.keyboards.menu import get_main_keyboard, get_games_keyboard, get_back_to_games_button

menu_router = Router()

class AskRules(StatesGroup):
    """
    Класс состояний для процесса запроса правил игры.

    Attributes:
        choosing_game (State): Состояние, когда пользователь выбирает игру.
        waiting_for_question (State): Состояние, когда пользователь вводит свой вопрос.
    """
    choosing_game = State()
    waiting_for_question = State()

@menu_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start. Сбрасывает состояние и показывает главное меню.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояний пользователя.
    """
    await state.clear()
    await message.answer("Привет! Я консультант по настольным играм.", reply_markup=get_main_keyboard())

@menu_router.message(F.text == "🎲 Спросить про правила")
@menu_router.message(F.text == "🔁 Выбрать другую игру")
async def show_game_list(message: Message, state: FSMContext):
    """
    Показывает пользователю список доступных игр для выбора.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояний пользователя.
    """
    await state.set_state(AskRules.choosing_game)
    await message.answer("Выбери игру:", reply_markup=get_games_keyboard())

@menu_router.callback_query(F.data.startswith("game_"))
async def handle_game_choice(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор игры пользователем и переводит в состояние ввода вопроса.

    Args:
        callback (CallbackQuery): Объект callback-запроса от inline-кнопки.
        state (FSMContext): Контекст состояний пользователя.
    """
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
    """
    Обрабатывает вопрос пользователя и отправляет его на бэкенд для получения ответа.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояний пользователя.
    """
    data = await state.get_data()
    game = data.get("game")
    question = message.text

    # Запрос к бэкенду
    async with aiohttp.ClientSession() as session:
        try:
            logger.log(logging.INFO, f"Отправляю запрос: {cfg.api_url}/get_answer с данными {game}, {question}")
            async with session.post(f"{cfg.api_url}/get_answer",
                                    json={"game_name": game, "question": question}) as resp:
                if resp.status == 200:
                    answer = (await resp.json()).get("answer", "Ответ не найден.")
                else:
                    answer = f"Не удалось получить ответ. Статус: {resp.status}"
        except Exception as e:
            logger.log(logging.ERROR, f"Ошибка при запросе: {e}")

            answer = "Непредвиденная ошибка"

    await message.answer(f"<b>Ответ по игре {game}:</b>\n\n{answer}")
