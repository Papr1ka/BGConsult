from pydantic.v1 import BaseSettings

from back.app.models.pdf import Game


class Settings(BaseSettings):
    database_url: str
    hf_token: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()


games_info_by_name = {
    "Манчкин": Game("Манчкин", "https://www.bgames.com.ua/rules/munkin_color.pdf", "munchkin.pdf"),
    "Шахматы": Game("Шахматы", "https://example/chess.pdf", "chess.pdf"),
}

games_info_by_file = {game.file_name: game for game in games_info_by_name.values()}
