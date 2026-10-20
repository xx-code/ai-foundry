from typing import Protocol

from backend.app.adapters.dto.model_adapter import ListAiProviderModelDto, AiProviderModelDto
from backend.app.services.dto.base import ListDto
from backend.domain.enums.ai_provider import AiProvider


class ProviderAiModelRepository(Protocol):
    def list_model(self, input: ListAiProviderModelDto) -> ListDto[AiProviderModelDto]: ...
    def exist_model(self, input: ListAiProviderModelDto, model_id: str) -> bool: ...