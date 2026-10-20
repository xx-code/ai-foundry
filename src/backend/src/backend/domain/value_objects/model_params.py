from dataclasses import dataclass

from backend.domain.enums.model_reasoning import ModelReasoning


@dataclass(frozen=True)
class ModelParams:
    temperature: float
    max_tokens: int
    timeout: int
    reasoning: ModelReasoning = ModelReasoning.NONE