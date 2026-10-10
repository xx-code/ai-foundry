from uuid import UUID

from backend.domain.entities.user_password import UserPassword
from backend.domain.repositories.user_password_repository import UserPasswordRepository
from backend.infra.persistence.local_storage.repositories.base import LocalStorageRepository


class LocalUserPasswordRepository(LocalStorageRepository[UserPassword], UserPasswordRepository): # type: ignore
    def get_by_user_id(self, id: UUID) -> UserPassword | None:
        for pwd in self._db.values():
            if pwd.user_id == id:
                return pwd
        return None