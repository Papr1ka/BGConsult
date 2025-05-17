import os
from dotenv import load_dotenv

load_dotenv("/app/back/.env")
class Cfg:
    """
    Класс конфигурации для загрузки переменных окружения из .env файла.

    Атрибуты:
        token (str): Токен для бота Telegram.
        api_url (str): URL бэкенд-сервиса для обработки вопросов.
    """

    def __init__(self):
        """
        Инициализирует конфигурацию, загружая переменные из .env файла,
        расположенного в корне проекта.
        """
        self.hf_token = os.getenv('HF_TOKEN')

config = Cfg()