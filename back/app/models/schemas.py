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