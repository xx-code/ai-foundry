from datetime import datetime
from uuid import UUID

from backend.domain.entities.entity import Entity
from backend.domain.exception import ValidationException
from backend.domain.value_objects.model_params import ModelParams


class Model(Entity):
    def __init__(
            self, 
            provider_key_id: UUID,
            user_id: UUID,
            name: str,
            provider_model_id: str,
            default_instruction: str,
            params: ModelParams,
            id: UUID | None = None, 
            created_at: datetime | None = None, 
            updated_at: datetime | None = None):
        super().__init__(id, created_at, updated_at)
        self._provider_key_id = provider_key_id
        self._user_id = user_id
        self._name = name
        self._provider_model_id = provider_model_id
        self._default_instruction = default_instruction
        self._params = self._validation_params(params)

    @property
    def default_instruction(self) -> str:
        return self._default_instruction

    def set_default_instruction(self, default_instruction: str):
        if self._default_instruction != default_instruction:
            self._default_instruction = default_instruction
            self._mark_changed()

    @property
    def provider_key_id(self) -> UUID:
        return self._provider_key_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    def set_name(self, name: str):
        if self._name != name:
            self._name = name
            self._mark_changed()

    @property
    def provider_model_id(self) -> str:
        return self._provider_model_id

    @property
    def params(self) -> ModelParams:
        return self._params

    def set_params(self, params: ModelParams):
        if self._params != params:
            self._params = params
            self._mark_changed()

    @staticmethod
    def _validation_params(params: ModelParams) -> ModelParams:
        if params.temperature <= 0 or params.temperature >= 1 :
            raise ValidationException("MODEL_PARAMS_TEMPERATURE_MUST_BETWEEN_ZERO_ONE", "Model must be betwee 0.0 in 1.0") 

        if params.max_tokens <= 0:
            raise ValidationException("MODEL_PARAMS_MAX_TOKEN_MUST_BE_GREATER_THAN_ZERO", "Models parmas max_token muste be greater than 0")
        
        if params.timeout <= 0:
            raise ValidationException("MODEL_PARAMS_TIMEOUT_MUST_BE_GREATER_THAN_ZERO", "Models timeout must be greater than zero")

        return params