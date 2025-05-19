import logging

import aiohttp
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.create_bot import cfg, logger
from bot.keyboards.menu import get_main_keyboard, get_games_keyboard, get_back_to_games_button, get_grade_keyboard
from bot.db_service.db_manager import db

menu_router = Router()

async def get_current_dialog(input_obj):
    """
    Вспомогательная функция, возвращающая id текущего диалога в БД. Если активного диалога нет, то он создаётся.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    username = input_obj.from_user.username
    user_id = input_obj.from_user.id
    
    dialog_id = await db.get_active_dialog_by_username(username)
    if not dialog_id:
        dialog_id = await db.start_dialog(user_id=user_id, user_name=username)
    
    return dialog_id

async def if_new_dialog_without_grade(input_obj, state: FSMContext):
    state = await state.get_state()
    if state == AskRules.waiting_for_grade:
        dialog_id = await get_current_dialog(input_obj)
        await db.end_dialog(dialog_id)


class AskRules(StatesGroup):
    """
    Класс состояний для процесса запроса правил игры.

    Attributes:
        choosing_game (State): Состояние, когда пользователь выбирает игру.
        waiting_for_question (State): Состояние, когда пользователь вводит свой вопрос.
    """
    choosing_game = State()
    waiting_for_question = State()
    waiting_for_grade = State()

@menu_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start. Сбрасывает состояние и показывает главное меню.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояний пользователя.
    """
    await if_new_dialog_without_grade(message, state)
    dialog_id = await get_current_dialog(message)

    await db.add_message(dialog_id, message.text, True)

    answer = "Привет! Я консультант по настольным играм."
    await db.add_message(dialog_id, answer, False)

    await state.clear()
    await message.answer(answer, reply_markup=get_main_keyboard())

@menu_router.message(F.text == "🎲 Спросить про правила")
@menu_router.message(F.text == "🔁 Выбрать другую игру")
async def show_game_list(message: Message, state: FSMContext):
    """
    Показывает пользователю список доступных игр для выбора.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояний пользователя.
    """
    await if_new_dialog_without_grade(message, state)

    dialog_id = await get_current_dialog(message)
    await db.add_message(dialog_id, message.text, True)

    answer = "Выбери игру:"
    await db.add_message(dialog_id, answer, False)

    await state.set_state(AskRules.choosing_game)
    await message.answer(answer, reply_markup=get_games_keyboard())

@menu_router.message(F.text == "Завершить диалог")
async def close_dialog(message: Message, state: FSMContext):
    """
    Завершает текущий диалог пользователя.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояний пользователя.
    """
    dialog_id = await get_current_dialog(message)
    await db.add_message(dialog_id, message.text, True)

    answer = "Диалог завершён! Пожалуйста, оцените работу бота"
    await db.add_message(dialog_id, answer, False)

    await state.set_state(AskRules.waiting_for_grade)
    await message.answer(answer, reply_markup=get_grade_keyboard())

@menu_router.callback_query(F.data.startswith("game_"))
async def handle_game_choice(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор игры пользователем и переводит в состояние ввода вопроса.

    Args:
        callback (CallbackQuery): Объект callback-запроса от inline-кнопки.
        state (FSMContext): Контекст состояний пользователя.
    """
    await if_new_dialog_without_grade(callback, state)
    game = callback.data.removeprefix("game_")

    dialog_id = await get_current_dialog(callback)
    await db.add_message(dialog_id, game, True)

    await state.update_data(game=game)
    await state.set_state(AskRules.waiting_for_question)

    answer = f"Ты выбрал игру: <b>{game}</b>.\n\nВведи свой вопрос по правилам."
    await db.add_message(dialog_id, answer, False)

    await callback.message.answer(
        answer,
        reply_markup=get_back_to_games_button()
    )
    await callback.answer()

@menu_router.callback_query(F.data.startswith("grade_"), AskRules.waiting_for_grade)
async def handle_game_choice(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор оценки пользователем и переводит в состояние ввода вопроса.

    Args:
        callback (CallbackQuery): Объект callback-запроса от inline-кнопки.
        state (FSMContext): Контекст состояний пользователя.
    """
    grade = int(callback.data.removeprefix("grade_"))

    dialog_id = await get_current_dialog(callback)
    await db.add_message(dialog_id, str(grade), True)

    answer = f"Выставленная оценка: {grade}."

    await db.add_message(dialog_id, answer, False)
    await db.add_rating(dialog_id, grade)
    await db.end_dialog(dialog_id)

    await state.set_state(AskRules.waiting_for_question)
    await callback.message.answer(
        f"Выставленная оценка: {grade}.",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@menu_router.callback_query(F.data.startswith("grade_"))
async def handle_game_choice(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор оценки пользователя не по сценарию и переводит в состояние ввода вопроса.

    Args:
        callback (CallbackQuery): Объект callback-запроса от inline-кнопки.
        state (FSMContext): Контекст состояний пользователя.
    """
    await if_new_dialog_without_grade(callback, state)
    dialog_id = await get_current_dialog(callback)
    await db.add_message(dialog_id, callback.message.text, True)

    answer = f"Вы не завершили активный диалог"
    await db.add_message(dialog_id, answer, False)

    await callback.message.answer(
        answer,
        reply_markup=get_main_keyboard()
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
    dialog_id = await get_current_dialog(message)
    await db.add_message(dialog_id, message.text, True)

    data = await state.get_data()
    game = data.get("game")
    question = message.text

    # Запрос к бэкенду
    async with aiohttp.ClientSession() as session:
        try:
            logger.log(logging.INFO, f"Отправляю запрос: {cfg.api_url}/get_answer/ с данными {game}, {question}")
            async with session.post(f"{cfg.api_url}/get_answer/",
                                    json={"game_name": game, "question": question}) as resp:
                if resp.status == 200:
                    answer = (await resp.json()).get("answer", "Ответ не найден.")
                else:
                    answer = f"Не удалось получить ответ. Статус: {resp.status}"
        except Exception as e:
            logger.log(logging.ERROR, f"Ошибка при запросе: {e}")

            answer = "Непредвиденная ошибка"

    answer = f"<b>Ответ по игре {game}:</b>\n\n{answer}"
    await db.add_message(dialog_id, answer, False)
    await message.answer(answer)
