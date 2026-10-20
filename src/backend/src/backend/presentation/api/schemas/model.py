from __future__ import annotations
from pydantic import BaseModel

from backend.app.adapters.dto.model_adapter import AiProviderModelDto


class ModelResponse(BaseModel):
    model_id: str
    type: str

    @classmethod
    def from_service(cls, dto: AiProviderModelDto) -> ModelResponse: 
        return ModelResponse(
            model_id=dto.model_id,
            type=dto.type
        )
