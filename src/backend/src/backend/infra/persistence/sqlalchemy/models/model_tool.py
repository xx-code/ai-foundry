from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.model_tool import ModelTool
from backend.domain.enums.ai_tool import AiToolType

from .base import Base


class ModelToolModel(Base):
    __tablename__ = "model_tools"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    model_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("models.id", ondelete="CASCADE"),
    )
    tool_id: Mapped[str] = mapped_column(String(100))
    tool_type: Mapped[AiToolType] = mapped_column(Enum(AiToolType))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> ModelTool:
        return ModelTool(
            id=self.id,
            model_id=self.model_id,
            tool_id=self.tool_id,
            tool_type=self.tool_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, entity: ModelTool) -> ModelToolModel:
        return cls(
            id=entity.id,
            model_id=entity.model_id,
            tool_id=entity.tool_id,
            tool_type=entity.tool_type,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )