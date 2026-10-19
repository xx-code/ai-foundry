from dataclasses import dataclass

from backend.domain.enums.ai_provider import OnlineAiProvider

@dataclass
class ListAiProviderModelDto:
    provider: OnlineAiProvider
    ApiKey: str 

@dataclass
class AiProviderModelDto:
    model_id: str 
    type: str
    input_price: str
    output_price: str