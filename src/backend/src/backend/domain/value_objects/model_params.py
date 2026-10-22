from dataclasses import dataclass

from backend.domain.enums.model_reasoning import ModelReasoning


@dataclass(frozen=True)
class ModelParams:
    temperature: float=0.7
    max_tokens: int=1000
    timeout: int=30
    reasoning: ModelReasoning = ModelReasoning.NONE