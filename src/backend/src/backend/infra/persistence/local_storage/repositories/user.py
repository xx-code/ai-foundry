from backend.domain.entities.user import User
from backend.domain.repositories.user_repository import UserRepository
from backend.infra.persistence.local_storage.repositories.base import LocalStorageRepository

class LocalUserRepository(LocalStorageRepository[User], UserRepository): # type: ignore
    def get_by_email_or_user_name(self, email_or_username: str) -> User | None:
        for user in self._db.values():
            if email_or_username in (user.email, user.user_name):
                return user
        return None

