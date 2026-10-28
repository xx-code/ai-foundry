from __future__ import annotations
from dataclasses import dataclass

from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.enums.ai_provider import AiProvider

@dataclass
class AddProviderKeyDto:
    user_id: str
    provider: AiProvider
    name: str
    api_key: str

@dataclass
class AiProviderKeyDto:
    provider_id: str
    provider: AiProvider
    name: str
    api_key: str

    @classmethod
    def from_model(cls, model: AiProviderKey) -> AiProviderKeyDto:
        return AiProviderKeyDto(
            provider_id=str(model.id),
            provider=model.provider,
            name=model.name,
            api_key=model.api_key
        )