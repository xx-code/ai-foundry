from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from backend.domain.enums.model_reasoning import ModelReasoning
from backend.domain.value_objects.model_params import ModelParams
from sqlalchemy import JSON, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.model import Model

from .base import Base


class ModelModel(Base):
    __tablename__ = "models"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    provider_key_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_provider_keys.id", ondelete="CASCADE"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(String(100))
    provider_model_id: Mapped[str] = mapped_column(String(100))
    default_instruction: Mapped[str] = mapped_column(String(500))
    params: Mapped[dict[str, Any]] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> Model:
        params = ModelParams(
            temperature=self.params["temperature"],
            max_tokens=self.params["max_tokens"],
            timeout=self.params["timeout"],
            reasoning=ModelReasoning(
                self.params.get("reasoning", ModelReasoning.NONE.value)
            ),
        )
        return Model(
            id=self.id,
            provider_key_id=self.provider_key_id,
            user_id=self.user_id,
            name=self.name,
            default_instruction=self.default_instruction,
            params=params,
            provider_model_id=self.provider_model_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, entity: Model) -> ModelModel:
        return cls(
            id=entity.id,
            provider_key_id=entity.provider_key_id,
            user_id=entity.user_id,
            default_instruction=entity.default_instruction,
            params={
                "temperature": entity.params.temperature,
                "max_tokens": entity.params.max_tokens,
                "timeout": entity.params.timeout,
                "reasoning": entity.params.reasoning.value,
            },
            name=entity.name,
            provider_model_id=entity.provider_model_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
