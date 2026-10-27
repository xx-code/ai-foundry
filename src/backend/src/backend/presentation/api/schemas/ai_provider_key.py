from __future__ import annotations
from pydantic import BaseModel

from backend.app.services.dto.provider_key import AiProviderKeyDto
from backend.domain.enums.ai_provider import AiProvider

class AddAiProviderKeyRequest(BaseModel):
    name: str
    api_key: str
    provider: AiProvider

class AiProviderKeyResponse(BaseModel):
    id: str
    name: str
    provider: AiProvider
    api_key: str

    @classmethod
    def from_service(cls, dto: AiProviderKeyDto) -> AiProviderKeyResponse:
        return AiProviderKeyResponse(
            id=dto.provider_id,
            name=dto.name,
            api_key=dto.api_key,
            provider=dto.provider
        )