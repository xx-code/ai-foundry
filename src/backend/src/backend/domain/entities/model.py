from datetime import datetime
from uuid import UUID

from backend.domain.entities.entity import Entity


class Model(Entity):
    def __init__(
            self, 
            provider_key_id: UUID,
            user_id: UUID,
            name: str,
            provider_model_id: str,
            id: UUID | None = None, 
            created_at: datetime | None = None, 
            updated_at: datetime | None = None):
        super().__init__(id, created_at, updated_at)
        self._provider_key_id = provider_key_id
        self._user_id = user_id
        self._name = name
        self._provider_model_id = provider_model_id

    @property
    def provider_key_id(self) -> UUID:
        return self._provider_key_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def provider_model_id(self) -> str:
        return self._provider_model_id
        