from dataclasses import dataclass

from backend.domain.enums.ai_provider import OnlineAiProvider


@dataclass
class AddOnlineProviderKeyDto:
    user_id: str
    provider: OnlineAiProvider
    name: str
    api_key: str