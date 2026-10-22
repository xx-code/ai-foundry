from __future__ import annotations
from dataclasses import dataclass, field

from backend.domain.entities.model import Model
from backend.domain.entities.model_tool import ModelTool
from backend.domain.enums.ai_tool import AiToolType
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
class AddModelToolDto:
    model_id: str
    tool_id: str
    type: AiToolType

@dataclass
class ModelToolDto:
    id: str
    tool_id: str
    tool_type: AiToolType

    @classmethod
    def from_model(cls, model: ModelTool) -> ModelToolDto:
        return ModelToolDto(
            id=str(model.id),
            tool_id=model._tool_id,
            tool_type=model.tool_type
        )

@dataclass
class ModelDto:
    model_id: str
    name: str
    provider_id: str
    provider_model_id: str
    default_instruction: str
    params: ModelParams
    tools: list[ModelToolDto] = field(default_factory=list)

    @classmethod
    def from_model(
        cls,
        model: Model,
        model_tools: list[ModelTool] | None = None,
    ) -> ModelDto:
        return ModelDto(
            model_id=str(model.id),
            name=model.name,
            provider_id=str(model.provider_key_id),
            provider_model_id=model.provider_model_id,
            params=model.params,
            default_instruction=model.default_instruction,
            tools=[
                ModelToolDto.from_model(model_tool)
                for model_tool in (model_tools or [])
            ]
        )
