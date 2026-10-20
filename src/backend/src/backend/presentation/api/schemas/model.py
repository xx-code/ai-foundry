from __future__ import annotations
from typing import Optional
from backend.app.services.dto.model import ModelDto
from backend.domain.enums.model_reasoning import ModelReasoning
from pydantic import BaseModel

from backend.app.adapters.dto.model_adapter import AiProviderModelDto


class AiProviderModelResponse(BaseModel):
    model_id: str
    type: str

    @classmethod
    def from_service(cls, dto: AiProviderModelDto) -> AiProviderModelResponse: 
        return AiProviderModelResponse(
            model_id=dto.model_id,
            type=dto.type
        )


class ModelParamsResponse(BaseModel):
    temparature: float
    max_tokens: int
    timeout: float
    reasoning: ModelReasoning

class DeployModelRequest(BaseModel):
    name: str
    provider_key_id: str
    provider_model_id: str
    params: ModelParamsResponse
    default_instruction: Optional[str] = ""

class UpdateModelRequest(BaseModel):
    name: Optional[str] = None
    params: Optional[ModelParamsResponse] = None 

class ModelResponse(BaseModel):
    id: str
    provider_key_id: str
    provider_model_id: str
    name: str
    default_instruction: str
    params: ModelParamsResponse
    

    @classmethod
    def from_service(cls, dto: ModelDto) -> ModelResponse:
        return ModelResponse(
            id=dto.model_id,
            provider_model_id=dto.provider_model_id,
            provider_key_id=dto.provider_id,
            name=dto.name,
            default_instruction=dto.default_instruction,
            params=ModelParamsResponse(
                temparature=dto.params.temperature,
                max_tokens=dto.params.max_tokens,
                timeout=dto.params.timeout,
                reasoning=dto.params.reasoning,
            )
        )
