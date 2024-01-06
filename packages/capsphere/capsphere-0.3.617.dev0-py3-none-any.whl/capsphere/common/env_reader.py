import os

from dotenv import load_dotenv


class EnvReader:
    def __init__(self, env_file_path=".env"):
        self.env_file_path = env_file_path
        load_dotenv(env_file_path)

    @staticmethod
    def get_variable(self, key):
        return os.getenv(key)
