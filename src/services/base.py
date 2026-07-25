from src.utlils.db_manager import DBManager


class BaseServie:
    db: DBManager | None

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db