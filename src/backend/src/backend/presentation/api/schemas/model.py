from __future__ import annotations
from typing import Optional
from backend.app.services.dto.model import DeployModelDto, ModelDto, UpdateModelDto
from backend.domain.enums.ai_tool import AiToolType
from backend.domain.enums.model_reasoning import ModelReasoning
from pydantic import BaseModel

from backend.app.adapters.dto.model_adapter import AiProviderModelDto
from backend.domain.value_objects.model_params import ModelParams


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
    timeout: int
    reasoning: ModelReasoning

    def to_domain(self) -> ModelParams:
        return ModelParams(
            temperature=self.temparature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            reasoning=self.reasoning
        )

class DeployModelRequest(BaseModel):
    name: str
    provider_key_id: str
    provider_model_id: str
    default_instruction: Optional[str] = ""
    params: Optional[ModelParamsResponse] = None

    def to_domain(self, user_id: str) -> DeployModelDto:
        input_params = None
        if self.params is not None:
            input_params = self.params.to_domain()

        return DeployModelDto(
            user_id=user_id,
            provider_key_id=self.provider_key_id,
            provider_model_id=self.provider_model_id,
            name=self.name,
            default_instruction=self.default_instruction,
            params= input_params 
        )

class UpdateModelRequest(BaseModel):
    name: Optional[str] = None
    default_instruction: Optional[str] = None
    params: Optional[ModelParamsResponse] = None 

    def to_domain(self, id: str) -> UpdateModelDto:
        return UpdateModelDto(
            model_id=id,
            name=self.name,
            params=self.params.to_domain() if self.params is not None else None,
            default_instruction= self.default_instruction
        )

class AddModelToolRequest(BaseModel):
    tool_id: str
    tool_type: AiToolType

class ModelToolResponse(BaseModel):
    id: str
    tool_id: str
    tool_type: AiToolType

class ModelResponse(BaseModel):
    id: str
    provider_key_id: str
    provider_model_id: str
    name: str
    default_instruction: str
    params: ModelParamsResponse
    tools: list[ModelToolResponse] 
    

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
            ),
            tools=[
                ModelToolResponse(
                    id=str(tool.id),
                    tool_id=tool.tool_id,
                    tool_type=tool.tool_type
                )
                for tool in dto.tools
            ]
        )
