from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from back.app.core.config import games_info
from back.app.core.storage.postgres import get_db
from back.app.models.pg_data import Message, Dialog
from back.app.models.schemas import QuestionRequest, AnswerResponse
from back.app.services.llm import llm
from back.app.services.statistic import DialogService, MessageService, RatingService
from loguru import logger


router = APIRouter(tags=["question"])

def get_dialogs_service(db: Session = Depends(get_db)):
    return DialogService(db)

def get_message_service(db: Session = Depends(get_db)):
    return MessageService(db)

def get_rating_service(db: Session = Depends(get_db)):
    return RatingService(db)

@router.post("/get_answer/", response_model=AnswerResponse)
async def get_answer(
    request: QuestionRequest,
    dialog_service: DialogService = Depends(get_dialogs_service),
    message_service: MessageService = Depends(get_message_service),
):
    """
    Ручка для получения ответа на вопрос о конкретной игре и сохранения диалога.
    """
    try:
        question = request.question.strip()
        game_name = request.game_name.strip()
        user_id = request.user_id  # Предположим, что в запросе есть user_id
        user_name = request.user_name or "Anonymous"

        if not game_name or not question:
            raise HTTPException(status_code=400, detail="Название игры и вопрос обязательны")

        # Найти активный диалог или создать новый
        dialog = dialog_service.get_active_dialog_by_username(user_name)
        if dialog is None:
            dialog_id = dialog_service.start_dialog(Dialog(user_id=user_id, user_name=user_name, status="active"))
        else:
            dialog_id = dialog.dialog_id

        logger.info(dialog_id)
        logger.info(f"question: {question}\ngame_name: {game_name}\nuser_id: {user_id}\nuser_name: {user_name}")
        # Получение ответа
        answer = llm.answer(question, games_info[game_name].file_name).strip()

        logger.info(answer)


        # Сохранить вопрос и ответ в сообщения
        message_service.add_message(Message(dialog_id=dialog_id, text=question, is_from_user=True))
        message_service.add_message(Message(dialog_id=dialog_id, text=answer, is_from_user=False))

        return AnswerResponse(answer=answer)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


# @router.post("/rate/", status_code=204)
# async def rate_dialog(
#     rating: DialogRatingRequest,
#     dialog_service: DialogService = Depends(get_dialogs_service)
# ):
#     """
#     Ручка для сохранения оценки диалога
#     """
#     try:
#         if not dialog_service.get_dialog_by_id(rating.dialog_id):
#             raise HTTPException(status_code=404, detail="Диалог не найден")
#
#         dialog_service.add_rating(dialog_id=rating.dialog_id, score=rating.score)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


