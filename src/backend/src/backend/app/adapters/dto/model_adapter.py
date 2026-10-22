from dataclasses import dataclass

from backend.domain.enums.ai_provider import AiProvider

@dataclass
class ListAiProviderModelDto:
    provider: AiProvider
    api_key: str 

@dataclass
class AiProviderModelDto:
    model_id: str 
    type: str
    input_price: str
    output_price: str