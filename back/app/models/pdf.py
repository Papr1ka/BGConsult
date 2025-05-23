from pydantic import BaseModel

class Document(BaseModel):
    link: str  # Ссылка на документ
    filename: str  # Имя файла документа
    title: str  # Заголовок документа
    text: str  # Текстовое содержимое документа


class Game:
    def __init__(self, name, url, file_name):
        self.name = name
        self.url = url
        self.file_name = file_name
