from pathlib import Path
from threading import Lock

class Settings:
    """Singleton folosit pentru configurarea comună a microserviciilor.

    Este șablon creațional: există o singură instanță Settings în proces,
    iar toate serviciile folosesc aceeași logică pentru a calcula locația bazelor de date.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.base_dir = Path(__file__).resolve().parents[1]
                cls._instance.data_dir = cls._instance.base_dir / 'databases'
                cls._instance.data_dir.mkdir(parents=True, exist_ok=True)
                cls._instance.exports_dir = cls._instance.base_dir / 'exports'
                cls._instance.exports_dir.mkdir(parents=True, exist_ok=True)
            return cls._instance

    def sqlite_url(self, db_name: str) -> str:
        return f"sqlite:///{self.data_dir / db_name}"

    def export_path(self, file_name: str) -> str:
        path = self.exports_dir / file_name
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)


def get_settings() -> Settings:
    return Settings()
