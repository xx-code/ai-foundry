from sqlalchemy import or_, select

from backend.domain.entities.user import User
from backend.domain.repositories.user_repository import UserRepository
from backend.infra.persistence.sqlalchemy.models.user import UserModel
from backend.infra.persistence.sqlalchemy.repositories.base import SqlAlchemyRepository


class SqlAlchemyUserRepository(SqlAlchemyRepository[User, UserModel], UserRepository):
    model = UserModel

    def get_by_email_or_user_name(self, email_or_username: str) -> User | None:
        stmt = select(UserModel).where(
            or_(
                UserModel.email == email_or_username,
                UserModel.user_name == email_or_username,
            )
        )
        model = self._session.scalars(stmt).first()
        return model.to_domain() if model else None