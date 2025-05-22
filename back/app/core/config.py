from functools import lru_cache

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_url: str
    hf_token: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()


class Game:
    def __init__(self, name, url, file_name):
        self.name = name
        self.url = url
        self.file_name = file_name


games_info = {
    "Манчкин": Game("Манчкин", "https://www.bgames.com.ua/rules/munkin_color.pdf", "munchkin.pdf")
}