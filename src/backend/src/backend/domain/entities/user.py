from datetime import datetime
from ..exception import ValidationException
from .entity import Entity

import uuid

class User(Entity):

    def __init__(
        self,
        email: str,
        user_name: str,
        external_id: str,
        id: uuid.UUID | None = None, 
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self._email = self._validate_email(email)
        self._user_name = user_name
        self._external_id = external_id

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def external_id(self) -> str:
        return self._external_id

    def set_email(self, email: str):
        email = self._validate_email(email)

        if email != self._email:
            self._email = email
            self._mark_changed()

    def set_user_name(self, user_name: str):
        if user_name != self._user_name:
            self._user_name = user_name
            self._mark_changed()

    @staticmethod
    def _validate_email(email: str) -> str:
        if not email:
            raise ValidationException("INVALID_EMAIL", "email est invalide")

        return email