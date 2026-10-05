from uuid import UUID

from sqlalchemy import select

from backend.domain.entities.user_password import UserPassword
from backend.domain.repositories.user_password_repository import UserPasswordRepository
from backend.infra.persistence.sqlalchemy.models.user_password import UserPasswordModel
from backend.infra.persistence.sqlalchemy.repositories.base import SqlAlchemyRepository


class SqlAlchemyUserPasswordRepository(
    SqlAlchemyRepository[UserPassword, UserPasswordModel], UserPasswordRepository
):
    model = UserPasswordModel

    def get_by_user_id(self, id: UUID) -> UserPassword | None:
        stmt = select(UserPasswordModel).where(UserPasswordModel.user_id == id)
        model = self._session.scalars(stmt).first()
        return model.to_domain() if model else None