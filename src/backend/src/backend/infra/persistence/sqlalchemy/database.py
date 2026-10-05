
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker


class Database:
    """Détient la session de la transaction en cours (une par contexte d'exécution)."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.session_factory = sessionmaker(engine, expire_on_commit=False)

    def dispose(self) -> None:
        self.engine.dispose()