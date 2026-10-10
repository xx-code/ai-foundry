from datetime import datetime
from .entity import Entity
import uuid


class UserPassword(Entity): 

    def __init__(
            self, 
            user_id: uuid.UUID,
            hashed_pwd: str,
            id: uuid.UUID | None = None, 
            created_at: datetime = datetime.now(), 
            updated_at: datetime = datetime.now()):
        super().__init__(id, created_at, updated_at)
        self._user_id = user_id
        self._hashed_pwd = hashed_pwd

    @property
    def user_id(self) -> uuid.UUID:
        return self._user_id

    @property
    def hashed_pwd(self) -> str:
        return self._hashed_pwd

    def set_crypt_pwd(self, hashed_pwd: str):
        if self._hashed_pwd != hashed_pwd:
            self._hashed_pwd = hashed_pwd
            self._mark_changed()