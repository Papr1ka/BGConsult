from pydantic import BaseModel

class UserQuery(BaseModel):
    user_id: int
    text: str

class UserResponse(BaseModel):
    user_id: int
    answer: str

class RAGQuery(BaseModel):
    text: str

class RAGResponse(BaseModel):
    answer: str


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