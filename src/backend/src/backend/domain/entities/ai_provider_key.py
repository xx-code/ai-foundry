from datetime import datetime
from backend.domain.entities.entity import Entity
from uuid import UUID
from backend.domain.enums.ai_provider import OnlineAiProvider


class AiProviderKey(Entity):

    def __init__(
            self, 
            user_id: UUID,
            provider: OnlineAiProvider,
            api_key: str, 
            memo_key: str,
            name: str,
            id: UUID | None = None, 
            created_at: datetime | None = None, 
            updated_at: datetime | None = None):
        super().__init__(id, created_at, updated_at)
        self._provider = provider
        self._api_key = api_key
        self._name = name
        self._user_id = user_id
        self._memo_key = memo_key

    @property
    def memo_key(self) -> str:
        return self._memo_key

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def provider(self) -> OnlineAiProvider:
        return self._provider

    @property
    def api_key(self) -> str:
        return self._api_key