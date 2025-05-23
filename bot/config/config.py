import os
from dotenv import load_dotenv

load_dotenv("/bot/.env")
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
        self.token = os.getenv('TOKEN')
        self.api_url = os.getenv('API_URL')
        self.admin_whitelist = [int(admin) for admin in os.getenv('ADMIN_WHITELIST', '').split(',') if admin.strip()]
