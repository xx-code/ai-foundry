from sqlalchemy.orm import Session

from backend.domain.repositories.unit_of_work import UnitOfWork



class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, sesion: Session) -> None:
        self._session = sesion

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()