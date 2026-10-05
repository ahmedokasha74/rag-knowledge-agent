from helpers.config import get_settings, Settings
from pathlib import Path


class BaseController:

    def __init__(self):
        self.app_settings: Settings = get_settings()

    def get_database_path(self, db_name: str) -> str:
        database_path = Path("data") / db_name
        database_path.mkdir(parents=True, exist_ok=True)
        return str(database_path)