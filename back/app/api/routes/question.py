from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["question"])

class QuestionRequest(BaseModel):
    """
    Модель запроса для получения ответа на вопрос о игре.

    Attributes:
    - game_name (str): Название игры, по которой нужно получить ответ.
    - question (str): Вопрос, на который нужно найти ответ.
    """
    game_name: str
    question: str

class AnswerResponse(BaseModel):
    """
    Модель ответа, которая содержит ответ на заданный вопрос.

    Attributes:
    - answer (str): Ответ на вопрос, связанный с игрой.
    """
    answer: str

@router.post("/get_answer", response_model=AnswerResponse)
async def get_answer(request: QuestionRequest):
    """
    Ручка для получения ответа на вопрос о конкретной игре.

    Принимает запрос с названием игры и вопросом, ищет ответ в базе данных
    и возвращает его. В случае ошибки (не найдена игра или вопрос) возвращает ошибку 404.

    Args:
    - request (QuestionRequest): Объект, содержащий название игры и вопрос.

    Returns:
    - AnswerResponse: Ответ на вопрос, связанный с игрой.

    Raises:
    - HTTPException: Если игра или вопрос не найдены, возвращается ошибка 404.
    """
    question = request.question
    game_name = request.game_name

    if game_name == "" or question == "":
        raise HTTPException(status_code=404, detail="Ответ на этот вопрос не найден")


    answer = f'game_name={game_name} question={question}'

    return AnswerResponse(answer=answer)