from dataclasses import dataclass

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