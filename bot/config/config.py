import os

from dotenv import dotenv_values


class Cfg:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_path = os.path.join(base_dir, '.env')
        env_vars = dotenv_values(env_path)
        self.token = env_vars['TOKEN']
        self.api_url = env_vars['API_URL']

