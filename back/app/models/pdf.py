from pydantic import BaseModel

class Document(BaseModel):
    link: str  # Ссылка на документ
    filename: str  # Имя файла документа
    title: str  # Заголовок документа
    text: str  # Текстовое содержимое документа