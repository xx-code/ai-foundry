from __future__ import annotations
from dataclasses import dataclass

from backend.domain.entities.model import Model
from backend.domain.value_objects.model_params import ModelParams

@dataclass
class DeployModelDto: 
    name: str
    user_id: str
    provider_key_id: str
    provider_model_id: str
    params: ModelParams | None = None 
    default_instruction: str | None = None

@dataclass
class UpdateModelDto:
    model_id: str
    name: str | None = None
    params: ModelParams | None = None
    default_instruction: str | None = None

@dataclass
class ModelDto:
    model_id: str
    name: str
    provider_id: str
    provider_model_id: str
    default_instruction: str
    params: ModelParams

    @classmethod
    def from_model(cls, model: Model) -> ModelDto:
        return ModelDto(
            model_id=str(model.id),
            name=model.name,
            provider_id=str(model.provider_key_id),
            provider_model_id=model.provider_model_id,
            params=model.params,
            default_instruction=model.default_instruction
        )
