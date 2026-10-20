from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid
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

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> Model:
        return Model(
            id=self.id,
            provider_key_id=self.provider_key_id,
            user_id=self.user_id,
            name=self.name,
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
            name=entity.name,
            provider_model_id=entity.provider_model_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
