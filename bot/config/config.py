import os

from dotenv import dotenv_values


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
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(base_dir, '.env')
        env_vars = dotenv_values(env_path)
        self.token = env_vars['TOKEN']
        self.api_url = env_vars['API_URL']
