from typing import Protocol

from .repository import Repository
from ..entities.user_password import UserPassword

import uuid

class UserPasswordRepository(Repository[UserPassword], Protocol):
    def get_by_user_id(self, id: uuid.UUID) -> UserPassword | None:...