from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """
    Модель запроса для получения ответа на вопрос о игре.

    Attributes:
    - game_name (str): Название игры, по которой нужно получить ответ.
    - question (str): Вопрос, на который нужно найти ответ.
    """
    game_name: str
    question: str
    user_id: int
    user_name: str

class AnswerResponse(BaseModel):
    """
    Модель ответа, которая содержит ответ на заданный вопрос.

    Attributes:
    - answer (str): Ответ на вопрос, связанный с игрой.
    """
    answer: str


class DialogRatingRequest(BaseModel):
    user_id: int
    rating: int