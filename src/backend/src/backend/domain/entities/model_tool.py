from datetime import datetime
from uuid import UUID

from backend.domain.entities.entity import Entity
from backend.domain.enums.ai_tool import AiToolType


class ModelTool(Entity):

    def __init__(self, 
        model_id: UUID,
        tool_id: str,
        tool_type: AiToolType,
        id: UUID | None = None, 
        created_at: datetime | None = None, 
        updated_at: datetime | None = None):
        super().__init__(id, created_at, updated_at)
        self._model_id = model_id
        self._tool_id = tool_id
        self._tool_type = tool_type

    @property
    def model_id(self) -> UUID:
        return self._model_id 

    @property
    def tool_id(self) -> str:
        return self._tool_id

    @property
    def tool_type(self) -> AiToolType:
        return self._tool_type