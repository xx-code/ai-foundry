from datetime import datetime
from uuid import UUID

from backend.domain.entities.entity import Entity


class Model(Entity):
    def __init__(
            self, 
            user_id: UUID,
            provider_id: UUID,
            provider_name: str,
            name: str,
            id: UUID | None = None, 
            created_at: datetime | None = None, 
            updated_at: datetime | None = None
        ):
        super().__init__(id, created_at, updated_at)
        self._provider_id = provider_id
        self._provider_name = provider_name
        self._name = name
        self._user_id = user_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def provider_id(self) -> UUID:
        return self._provider_id

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def name(self) -> str:
        return self._name